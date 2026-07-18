"""MeridianModel — the Mesa ABM core and tick loop.

This module is the **single writer of numeric state**. The LLM gateway proposes; the engine
here validates legality and computes/applies effects. That separation is the determinism
boundary (see docs/ARCHITECTURE_DECISIONS.md ADR-006).

Reproducibility: a `seed` is threaded through the constructor into `self.rng`
(`random.Random`). Same seed + scenario + decisions ⇒ identical macro/meso numbers. All
stochastic draws in the engine, agents, and diffusion use this RNG — never the global
`random` module.
"""

from __future__ import annotations

import random
from typing import Any, Optional

import mesa

from .agents.cohort_agent import CohortAgent
from .agents.institutional_agent import InstitutionalAgent
from .agents.macro_state import MacroStateHolder
from .diffusion import build_cohort_graph, linear_threshold_step
from .schemas.agent_schema import ActionProposal, Cohort, MicroAgent
from .schemas.macro_schema import (
    AllianceConfidence,
    InstitutionalTrust,
    MacroIndicators,
    MacroState,
    PublicFinances,
)

# How the engine scales/validates each proposed action into a macro delta.
# The LLM cannot bypass this table — it only names an action_type; the engine owns magnitude.
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

    def __init__(self, scenario: dict, seed: Optional[int] = None) -> None:
        resolved_seed = seed if seed is not None else scenario.get("default_seed", 0)
        super().__init__(seed=resolved_seed)
        self.rng = random.Random(resolved_seed)  # the ONLY source of engine randomness

        self.scenario = scenario
        self.scenario_id: str = scenario["scenario_id"]
        self.seed: int = resolved_seed
        self.tick: int = 0

        # --- MACRO ---
        macro = _macro_from_scenario(scenario)
        macro.seed = resolved_seed
        self.macro = MacroStateHolder(macro)

        # --- MESO (cohorts) ---
        self.cohorts: list[CohortAgent] = []
        cohort_dicts: list[dict] = []
        for c in scenario.get("cohorts", []):
            cohort = Cohort(**c)
            self.cohorts.append(CohortAgent(cohort.cohort_id, self, cohort))
            cohort_dicts.append(cohort.model_dump())
        self.cohort_graph = build_cohort_graph(cohort_dicts)

        # --- MICRO (institutional agents) ---
        self.institutions: list[InstitutionalAgent] = []
        for a in scenario.get("institutional_agents", []):
            spec = MicroAgent(**a)
            self.institutions.append(InstitutionalAgent(spec.agent_id, self, spec))

        # --- Information environment ---
        self.campaign: Optional[dict] = scenario.get("hidden_campaign")
        self.narrative_adoption: dict[str, float] = {c.cohort.cohort_id: 0.0 for c in self.cohorts}

        # --- Logs ---
        self.event_log: list[dict] = []
        self.snapshots: list[dict] = [self.macro.snapshot()]

    # ------------------------------------------------------------------ #
    # Determinism boundary: proposals in, validated deltas out.
    # ------------------------------------------------------------------ #
    def _validate_and_price(self, proposal: ActionProposal) -> dict[str, float]:
        """Turn an LLM `ActionProposal` into a legal, engine-owned macro delta.

        This is the gate. The LLM chose an `action_type`; the engine decides the magnitude
        (and could reject it entirely). The proposal's own `parameters`/`confidence` are
        advisory and are deliberately NOT trusted as state.
        """
        base = ACTION_EFFECTS.get(proposal.action_type, {})
        # Engine-owned scaling; intentionally ignores proposal.parameters as authority.
        return dict(base)

    def _step_macro_rules(self) -> None:
        """Deterministic + seeded-stochastic macro drift applied every tick."""
        # Small seeded macro noise, e.g. shipping variance around the crisis baseline.
        noise = self.rng.uniform(-0.002, 0.002)
        self.macro.apply_deltas({"shipping_throughput_pct_of_baseline": noise})

    def _step_diffusion(self) -> None:
        """Advance narrative adoption across cohorts via the diffusion model."""
        if not self.cohorts:
            return
        susceptibility = {c.cohort.cohort_id: c.susceptibility for c in self.cohorts}
        self.narrative_adoption = linear_threshold_step(
            self.cohort_graph, self.narrative_adoption, susceptibility, self.rng
        )

    def step(self) -> None:
        """Advance the simulation by one tick, in a fixed deterministic order."""
        self.tick += 1

        # 1. Meso agents drift (fixed order for reproducibility).
        for cohort in self.cohorts:
            cohort.step()

        # 2. Narrative diffusion over the cohort graph.
        self._step_diffusion()

        # 3. Micro agents produce proposals; engine validates + applies. Fixed order.
        for inst in self.institutions:
            inst.step()
            if inst.last_proposal is not None:
                deltas = self._validate_and_price(inst.last_proposal)
                if deltas:
                    self.macro.apply_deltas(deltas)
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

        # 5. Snapshot.
        self.macro.state.tick = self.tick
        self.snapshots.append(self.macro.snapshot())

    def run(self, ticks: int) -> None:
        """Run `ticks` steps."""
        for _ in range(ticks):
            self.step()

    def macro_snapshot(self) -> dict[str, Any]:
        """Return the current macro state as a serializable dict."""
        return self.macro.snapshot()
