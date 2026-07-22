"""MeridianModel — the Mesa ABM core and tick loop.

P0.4 (19 July 2026): the engine no longer writes authoritative state directly. All authoritative
changes are routed through `TransitionService` (`transitions.py`), which owns the single mutation
path. `state.py` holds the authoritative structure.

P0.4A (19 July 2026): authoritative randomness is KEYED, not sequential. `self.draws` is a
`DeterministicDrawService` (ADR-010, accepted) in which every value is a pure function of
(run seed, canonical key). There is no shared stream, nothing accumulates, and nothing advances —
so adding, removing or reordering a draw in one subsystem cannot shift results in another. This
replaces the previous single `random.Random`, whose call-order sensitivity was the mechanism
behind A3's finding that apparent meso→macro coupling was stream displacement rather than
causality. See `docs/adr/ADR-010-deterministic-randomness-architecture.md`.

Reproducibility, stated precisely: the existing stubbed execution path reproduces the same tested
numeric outputs when the seed, scenario and stubbed agent outputs remain identical. Determinism is
verified on the tested CPython implementation, including across a subprocess with a different
`PYTHONHASHSEED`. Cross-language reproducibility is **not** claimed and has not been measured.

The engine still contains no cost, cooldown, decay, budget, prerequisite or revert mechanism, and
no legality or feasibility validation. P0.4 did not add any of those.
"""

from __future__ import annotations

from typing import Any, Optional

import mesa

from .agents.cohort_agent import CohortAgent
from .agents.institutional_agent import InstitutionalAgent
from .diffusion import build_cohort_graph, linear_threshold_step
from .draws import DeterministicDrawService
from .schemas.agent_schema import ActionProposal, Cohort, MicroAgent
from .schemas.macro_schema import (
    AllianceConfidence,
    InstitutionalTrust,
    MacroIndicators,
    MacroState,
    PublicFinances,
)
from .pipeline import ChainRunner
from .rules.kestral_v1 import RULE_PACK
from .state import AuthoritativeState, build_initial_state, canonical_json
from .decisions import RESOLUTION_RULE_VERSION
from .transitions import Transition, TransitionOrigin, TransitionRecord, TransitionService, TransitionType

# The engine's entire action vocabulary and every magnitude, hardcoded here. This is not a rule
# pack, is not data-driven, and is not extensible without editing code — see CAPABILITY-CLAIMS C13.
ACTION_EFFECTS: dict[str, dict[str, float]] = {
    "request_procurement_acceleration": {"military_readiness": 0.01, "government_approval": -0.002},
    "block_unfunded_spending": {"government_approval": -0.003},
    "open_backchannel": {"government_approval": 0.001},
    "invest_in_attribution": {"social_stability_index": 0.002},
    "counter_narrative_briefing": {"government_approval": 0.004, "social_stability_index": 0.003},
    "convene_cabinet": {"government_approval": 0.002},
    "observe": {},
}


def _macro_from_scenario(scenario: dict) -> MacroState:
    """Build the initial `MacroState` from a scenario template's macro block."""
    m = scenario["initial_macro_state"]
    ind = m["indicators"]
    return MacroState(
        tick=0,
        scenario_id=scenario["scenario_id"],
        seed=scenario.get("default_seed", 0),
        indicators=MacroIndicators(
            inflation_rate=ind["inflation_rate"],
            unemployment_rate=ind["unemployment_rate"],
            gdp_growth_qoq=ind["gdp_growth_qoq"],
            shipping_throughput_pct_of_baseline=ind["shipping_throughput_pct_of_baseline"],
            government_approval=ind["government_approval"],
            institutional_trust=InstitutionalTrust(**ind["institutional_trust"]),
            military_readiness=ind["military_readiness"],
            alliance_confidence=AllianceConfidence(**ind["alliance_confidence"]),
            social_stability_index=ind["social_stability_index"],
            foreign_direct_investment_flow=ind["foreign_direct_investment_flow"],
            fuel_reserve_days=ind["fuel_reserve_days"],
            public_finances=PublicFinances(**ind["public_finances"]),
        ),
        derivation="rules_engine_v1 + seed_init",
    )


class MeridianModel(mesa.Model):
    """Three-tier crisis simulation model.

    Args:
        scenario: A loaded scenario template (see `scenarios/*.json`).
        seed: Deterministic RNG seed. If ``None``, falls back to the scenario default.
    """

    def __init__(
        self,
        scenario: dict,
        seed: Optional[int] = None,
        enabled_mechanisms: Optional[list[str]] = None,
    ) -> None:
        resolved_seed = seed if seed is not None else scenario.get("default_seed", 0)
        super().__init__(seed=resolved_seed)
        # P0.4A: authoritative randomness is KEYED, not sequential. There is no shared stream and
        # no `self.rng`. Every draw is a pure function of (run seed, canonical key), so no draw
        # can displace another. mesa's own `Model.random` is seeded by `super().__init__` above;
        # MERIDIAN never uses it for authoritative values.
        self.draws = DeterministicDrawService(
            seed=resolved_seed,
            scenario=scenario["scenario_id"],
            rule_pack=RULE_PACK,
        )

        self.scenario = scenario
        self.scenario_id: str = scenario["scenario_id"]
        self.seed: int = resolved_seed

        macro = _macro_from_scenario(scenario)
        macro.seed = resolved_seed

        # --- MESO (cohorts) ---
        self.cohorts: list[CohortAgent] = []
        cohort_specs: list[Cohort] = []
        cohort_dicts: list[dict] = []
        for c in scenario.get("cohorts", []):
            cohort = Cohort(**c)
            cohort_specs.append(cohort)
            self.cohorts.append(CohortAgent(cohort.cohort_id, self, cohort))
            cohort_dicts.append(cohort.model_dump())
        self.cohort_graph = build_cohort_graph(cohort_dicts)

        # --- MICRO (institutional agents) ---
        self.institutions: list[InstitutionalAgent] = []
        inst_specs: list[MicroAgent] = []
        for a in scenario.get("institutional_agents", []):
            spec = MicroAgent(**a)
            inst_specs.append(spec)
            self.institutions.append(InstitutionalAgent(spec.agent_id, self, spec))

        # --- AUTHORITATIVE STATE + the single mutation boundary (P0.4) ---
        initial = build_initial_state(
            scenario=scenario,
            macro=macro,
            cohorts=cohort_specs,
            institutions=inst_specs,
            seed=resolved_seed,
        )
        self._transitions = TransitionService(initial)

        # --- P0.5 causal slice ---
        # `enabled_mechanisms=None` runs the whole declared chain. Passing a subset is the
        # counterfactual switch used to prove a given link actually matters.
        self.chain = ChainRunner(self, enabled=enabled_mechanisms)
        # Incidents are EXTERNAL scenario input, scheduled by tick. Not hard-coded in the tick
        # loop, so a run with no incident is a genuine baseline.
        self._scheduled_incidents: list[dict] = list(scenario.get("incidents", []))

        # --- Logs (NOT authoritative state; see the P0.6 note below) ---
        # `transition_log` holds returned TransitionRecords. It is an in-memory diagnostic list,
        # not an event store: nothing persists, nothing is replayed from it, and no state can be
        # rebuilt from it. Event sourcing, snapshots and replay are P0.6.
        self.transition_log: list[TransitionRecord] = []
        self.event_log: list[dict] = []
        self.snapshots: list[dict] = [self.macro_snapshot()]

    # ------------------------------------------------------------------ #
    # Authoritative state access.
    # ------------------------------------------------------------------ #
    @property
    def state(self) -> AuthoritativeState:
        """Read-only view of authoritative state. Do not mutate — use `submit`."""
        return self._transitions.state

    @property
    def tick(self) -> int:
        """Derived from authoritative state. Kept as a property so `model.tick` still reads."""
        return self.state.tick

    @property
    def narrative_adoption(self) -> dict[str, float]:
        return self.state.narrative_adoption

    @property
    def campaign(self) -> Optional[dict]:
        return self.state.campaign

    def _consume_due_decisions(self) -> None:
        """Drain the decision queue for this tick, resolve deterministically, and apply.

        CONSUMED EXACTLY ONCE. The submission id moves to `consumed_submissions` inside the same
        transition sequence, and both the queue transition and this method refuse an id already
        there - so a repeat submission cannot apply its effects twice.

        NO RANDOM DRAW is taken here and the shared RNG is not touched.
        """
        from .decisions import ResolutionInputs, resolve

        due = [q for q in self.state.decision_queue if q.apply_at_tick <= self.tick]
        for queued in sorted(due, key=lambda q: (q.apply_at_tick, q.submission_id)):
            gov = self.state.government
            cohort_id = "coastal-creole-fishing"
            cohort = self.state.cohorts.get(cohort_id)
            campaign = self.state.campaign or {}
            targets = campaign.get("target_cohorts") or []

            inputs = ResolutionInputs(
                implementation_capacity=gov.implementation_capacity,
                budget_reserve_m=gov.budget_reserve_m,
                political_capital=gov.political_capital,
                affected_population=int(getattr(cohort, "represents_population", 0) or 0),
                adversary_targets_affected_cohort=cohort_id in targets,
            )
            resolution = resolve(
                queued.option_id,
                inputs,
                current_concern=float(getattr(cohort, "economic_concern", 0.0) or 0.0),
                current_employment_pressure=float(self.state.chain.employment_pressure),
            )

            trace = {
                "mechanism": resolution.rule + " option=" + queued.option_id,
                "mechanism_version": resolution.rule_version,
                "actor": "player",
                "source_fields": resolution.source_fields,
            }

            # Mark consumed FIRST, so nothing below can leave a decision replayable.
            self.submit(Transition(
                type=TransitionType.CONSUME_PLAYER_DECISION,
                origin=TransitionOrigin.PLAYER_DECISION,
                payload={"submission_id": queued.submission_id}, **trace))

            # Cost is paid on attempting, not on succeeding.
            for field, amount in (
                ("budget_reserve_m", resolution.budget_spent_m),
                ("political_capital", resolution.political_capital_spent),
            ):
                if amount > 0:
                    self.submit(Transition(
                        type=TransitionType.SPEND_GOVERNMENT_RESOURCE,
                        origin=TransitionOrigin.PLAYER_DECISION,
                        payload={"field": field, "amount": amount}, **trace))

            # Immediate effects, through the EXISTING declared types. No second pathway.
            for eff in resolution.immediate_effects:
                if eff["kind"] == "cohort_concern":
                    self.submit(Transition(
                        type=TransitionType.SET_COHORT_CONCERN,
                        origin=TransitionOrigin.PLAYER_DECISION,
                        payload={"cohort_id": eff["cohort_id"], "value": eff["value"]}, **trace))

            # Delayed effects are scheduled, not applied now.
            for eff in resolution.delayed_effects:
                self.submit(Transition(
                    type=TransitionType.SCHEDULE_DELAYED_EFFECT,
                    origin=TransitionOrigin.PLAYER_DECISION,
                    payload={
                        "due_tick": self.tick + int(eff["due_in_ticks"]),
                        "kind": eff["kind"], "field": eff["field"], "value": eff["value"],
                        "cause_submission_id": queued.submission_id, "why": eff["why"],
                    }, **trace))

            # The declared adversary reacts, where the scenario supports it.
            if resolution.adversary_response:
                a = resolution.adversary_response
                current = float(getattr(self.state.chain, a["field"]))
                self.submit(Transition(
                    type=TransitionType.SET_CHAIN_SCALAR,
                    origin=TransitionOrigin.EXTERNAL_INPUT,
                    payload={"field": a["field"], "value": min(1.0, round(current + a["delta"], 6))},
                    mechanism="declared adversary campaign response to " + queued.option_id,
                    mechanism_version=resolution.rule_version,
                    actor=str(campaign.get("campaign_id", "declared-campaign")),
                    source_fields=["chain." + a["field"], "campaign.target_cohorts"]))

            self.state.decision_log.append({
                "submission_id": queued.submission_id,
                "option_id": queued.option_id,
                "submitted_tick": queued.submitted_tick,
                "consumed_tick": self.tick,
                "rule": resolution.rule,
                "rule_version": resolution.rule_version,
                "inputs": resolution.inputs.model_dump(),
                "outcome": resolution.outcome.value,
                "effectiveness": resolution.effectiveness,
                "limiting_factor": resolution.limiting_factor,
                "budget_spent_m": resolution.budget_spent_m,
                "political_capital_spent": resolution.political_capital_spent,
                "immediate_effects": resolution.immediate_effects,
                "delayed_effects": resolution.delayed_effects,
                "adversary_response": resolution.adversary_response,
                "explanation": resolution.explanation,
            })
            self.event_log.append({
                "event_id": "evt-" + str(self.tick) + "-" + queued.submission_id,
                "tick": self.tick, "type": "decision_resolved",
                "actors_involved": ["player"],
                "effects": [{"outcome": resolution.outcome.value,
                             "effectiveness": resolution.effectiveness}],
            })

    def _apply_due_delayed_effects(self) -> None:
        """Apply scheduled effects whose tick has arrived, then retire them."""
        for idx in range(len(self.state.delayed_effects) - 1, -1, -1):
            eff = self.state.delayed_effects[idx]
            if eff.due_tick > self.tick:
                continue
            self.submit(Transition(
                type=TransitionType.SET_CHAIN_SCALAR,
                origin=TransitionOrigin.PLAYER_DECISION,
                payload={"field": eff.field, "value": eff.value},
                mechanism="delayed effect of decision " + eff.cause_submission_id + ": " + eff.why,
                mechanism_version=RESOLUTION_RULE_VERSION,
                actor="player",
                source_fields=["chain." + eff.field]))
            self.submit(Transition(
                type=TransitionType.RETIRE_DELAYED_EFFECT,
                origin=TransitionOrigin.ENGINE_RULE,
                payload={"index": idx}, mechanism="delayed effect applied"))

    def submit(self, transition: Transition) -> TransitionRecord:
        """Route a transition through the boundary and record the outcome."""
        record = self._transitions.apply(transition)
        self.transition_log.append(record)
        return record

    def canonical_state(self) -> str:
        """Deterministic serialisation of authoritative state.

        Serialisation groundwork only — NOT a state hash, NOT replay. See `state.canonical_json`.
        """
        return canonical_json(self.state)

    # ------------------------------------------------------------------ #
    # Determinism boundary: proposals in, validated deltas out.
    # ------------------------------------------------------------------ #
    def _price(self, proposal: ActionProposal) -> dict[str, float]:
        """Look the proposed action type up in the engine-owned effects table.

        Named `_price` rather than `_validate_and_price` since P0.4: this performs NO validation.
        It is a dict lookup returning constant deltas. The proposal's own `parameters` and
        `confidence` are advisory and deliberately not trusted. Structural validation now happens
        in `TransitionService.validate`; legality and feasibility validation still do not exist
        anywhere (blocker B1).
        """
        return dict(ACTION_EFFECTS.get(proposal.action_type, {}))

    def _step_macro_rules(self) -> None:
        """Seeded macro drift applied every tick, via the transition boundary."""
        noise = self.draws.jitter(
            0.002, subsystem="macro", purpose="shipping_noise", context=str(self.tick)
        )
        self.submit(
            Transition(
                type=TransitionType.APPLY_MACRO_DELTAS,
                origin=TransitionOrigin.ENGINE_RULE,
                payload={"deltas": {"shipping_throughput_pct_of_baseline": noise}},
                mechanism="macro_noise_rule (seeded uniform drift on one indicator)",
            )
        )

    def _step_diffusion(self) -> None:
        """Advance narrative adoption across cohorts, via the transition boundary.

        The result reaches no cohort belief and no macro indicator — it is read only by the API
        response. Wiring diffusion to belief is P0.5.
        """
        if not self.cohorts:
            return
        susceptibility = {c.cohort.cohort_id: c.susceptibility for c in self.cohorts}
        updated = linear_threshold_step(
            self.cohort_graph,
            self.state.narrative_adoption,
            susceptibility,
            self.draws,
            context=self.tick,
        )
        self.submit(
            Transition(
                type=TransitionType.SET_NARRATIVE_ADOPTION,
                origin=TransitionOrigin.ENGINE_RULE,
                payload={"adoption": updated},
                mechanism="linear_threshold_diffusion (not wired to beliefs or macro — P0.5)",
            )
        )

    def step(self) -> None:
        """Advance the simulation by one tick, in a fixed deterministic order."""
        self.submit(
            Transition(
                type=TransitionType.ADVANCE_TICK,
                origin=TransitionOrigin.ENGINE_RULE,
                mechanism="tick_advance",
            )
        )

        # 0. PLAYER DECISIONS, consumed at the authoritative boundary.
        #    Runs first so a decision taken this tick is visible to every rule below it, and so a
        #    reader can say "this tick is the one where the choice landed".
        self._consume_due_decisions()
        self._apply_due_delayed_effects()

        # 1. Meso agents drift (fixed order for reproducibility).
        for cohort in self.cohorts:
            cohort.step()

        # 2. Narrative diffusion over the cohort graph.
        self._step_diffusion()

        # 3. Micro agents propose; the engine prices and applies. Fixed order.
        for inst in self.institutions:
            inst.step()
            if inst.last_proposal is not None:
                deltas = self._price(inst.last_proposal)
                if deltas:
                    self.submit(
                        Transition(
                            type=TransitionType.APPLY_MACRO_DELTAS,
                            origin=TransitionOrigin.LLM_PROPOSAL,
                            payload={"deltas": deltas},
                            actor=inst.spec.agent_id,
                            mechanism=(
                                f"ACTION_EFFECTS table lookup for "
                                f"{inst.last_proposal.action_type!r} (constant deltas; no "
                                f"legality, cost or feasibility check)"
                            ),
                        )
                    )
                    self.event_log.append(
                        {
                            "event_id": f"evt-{self.tick}-{inst.spec.agent_id}",
                            "tick": self.tick,
                            "type": "action_applied",
                            "actors_involved": [inst.spec.agent_id],
                            "effects": [deltas],
                        }
                    )

        # 4. Deterministic macro rules/noise.
        self._step_macro_rules()

        # 5. External scenario inputs due this tick (P0.5). Applied before the chain runs so the
        #    incident is visible to stage 1 in the same tick it arrives.
        for incident in self._scheduled_incidents:
            if incident.get("at_tick") == self.tick:
                self.chain.apply_incident(
                    severity=float(incident["severity"]),
                    label=str(incident.get("label", "")),
                )

        # 6. The P0.5 societal-response chain, in fixed stage order.
        self.chain.run_tick()

        # 7. Snapshot (in-memory only; not persistence, not P0.6 snapshots).
        self.snapshots.append(self.macro_snapshot())

    def run(self, ticks: int) -> None:
        """Run `ticks` steps."""
        for _ in range(ticks):
            self.step()

    def macro_snapshot(self) -> dict[str, Any]:
        """Return the current macro state as a serializable dict. A DERIVED read."""
        return self.state.macro.model_dump()
