"""Authoritative simulation state — Phase 0 item P0.4.

WHAT THIS IS
------------
One explicit, versioned structure holding everything the engine treats as authoritative, plus
canonical serialisation for it. Before P0.4, authoritative values were scattered across model
attributes (`model.tick`, `model.narrative_adoption`), a holder object (`MacroStateHolder.state`)
and agent-owned Pydantic records (`CohortAgent.cohort.beliefs`), each mutated in place by whoever
happened to hold a reference.

WHAT THIS IS NOT
----------------
This is **not** an event store, a replay system, a snapshot/restore mechanism or a causal
reconstruction system. `canonical_json` is deterministic serialisation groundwork usable for
equality assertions; it is **not** authoritative state hashing, and no replay claim may rest on
it until P0.6 delivers events, snapshots and replay.

Nothing here persists. All state remains in process memory.

DERIVED vs AUTHORITATIVE
------------------------
Only the fields on `AuthoritativeState` are authoritative. Briefings, the narrative-adoption
readout in API responses, and every UI projection are DERIVED views computed from this state.
A derived value must never be written back.
"""

from __future__ import annotations

import json
from typing import Any, Optional

from pydantic import BaseModel, Field

from .schemas.macro_schema import MacroState

# Bumped when the SHAPE of AuthoritativeState changes. Distinct from `state_revision`, which
# counts accepted transitions within a single run.
STATE_SCHEMA_VERSION = "0.4.0"

# The engine's ACTION_EFFECTS table is still unversioned inline code. The P0.5 causal slice, by
# contrast, has a real versioned rule pack, and a run carrying that slice must report it - a
# version field that misreports the rules actually running is worse than no field at all.
RULE_PACK_VERSION = "unversioned-inline-0"


class ScenarioIdentity(BaseModel):
    """Which scenario this run is of, and at what version."""

    scenario_id: str
    # Scenario files carry no version field today; recorded as unknown rather than invented.
    scenario_version: str = "unversioned"


class RunMetadata(BaseModel):
    """Seed and randomness-architecture metadata for the run.

    P0.4A (19 July 2026): these fields now record the ARCHITECTURE ACTUALLY IN USE, not a
    placeholder. Authoritative randomness is keyed and derived (ADR-010, accepted) — every draw is
    a pure function of (run seed, canonical key). There is no shared sequential stream, so no draw
    can displace another.

    `named_substreams` was removed rather than set true. It would have been misleading: keys
    contain a subsystem field, but there are no *stateful* substreams to name — nothing
    accumulates and nothing advances. `randomness_architecture` says what is true instead.
    """

    seed: int
    randomness_architecture: str = "keyed_counter_v1"
    rng_algorithm: str = "hmac-sha256-v1"
    rng_algorithm_version: str = "hmac-sha256-v1"
    key_encoding_version: str = "meridian-key-v1"


class CohortRuntimeState(BaseModel):
    """The MUTABLE runtime values for one cohort, plus the weights aggregation needs.

    The cohort's static configuration (demographics, media exposure, susceptibility, grievances)
    stays in the scenario-derived `Cohort` spec. Two scenario values are copied here because
    authoritative aggregation must read them: `represents_population` and
    `income_sensitivity_to_shipping_disruption`.

    `represents_population` being read at all is new in P0.5. The audit recorded it as declared
    but read by NO code, with the demo data wrong by 63x and nothing detecting it. It now weights
    every society-wide aggregate.
    """

    cohort_id: str
    beliefs: dict[str, float] = Field(default_factory=dict)
    # Population this cohort stands for. Affects AGGREGATE MAGNITUDE ONLY — never truth,
    # morality, or what an individual does.
    represents_population: int = 0
    # This cohort's own declared exposure to shipping disruption, from the scenario. Why the
    # fishing cohort and the urban professional cohort respond differently to the same shock.
    income_sensitivity: float = 0.0
    # Stage 5 output: this cohort's economic concern, 0..1.
    economic_concern: float = 0.0


class ScenarioTiming(BaseModel):
    """What a tick MEANS in this scenario.

    Scenario-scoped by design (founder decision, 19 July 2026). Kestral Strait uses six-hour
    ticks; another scenario may use any duration. Nothing in the engine assumes six hours, and no
    document may imply every MERIDIAN scenario does.
    """

    tick_duration_minutes: int = 360  # 6 simulated hours
    demonstration_horizon_ticks: int = 20  # 5 simulated days

    def simulated_hours(self, ticks: int) -> float:
        return ticks * self.tick_duration_minutes / 60.0


class ChainState(BaseModel):
    """The Kestral Strait causal slice — Phase 0 item P0.5.

    One narrow cross-tier channel, not a society model. Every scalar is bounded 0..1 by its
    mechanism, so repeated shocks converge instead of accumulating.

    `previous` holds last tick's values for the fields whose mechanisms declare a lag, so a lag is
    an explicit read of a recorded prior value rather than an accident of stage ordering.
    """

    # Stage 1 — external input. Never spontaneously arises.
    incident_severity: float = 0.0
    incident_active: bool = False
    # Stage 2
    insurer_risk: float = 0.0
    # Stage 3
    premium_pressure: float = 0.0
    rerouting_level: float = 0.0
    rerouting_ticks_committed: int = 0
    # Stage 4
    port_activity_deficit: float = 0.0
    employment_pressure: float = 0.0
    # Stage 5 — population-weighted aggregate over per-cohort concern
    household_expectation_pressure: float = 0.0
    # Stage 6 — attention-like; the only quantities permitted to decay on "no new stimulus"
    narrative_attention: float = 0.0
    collective_activity: float = 0.0
    # Stage 7
    political_pressure: float = 0.0
    government_options: dict[str, str] = Field(default_factory=dict)

    # Recorded prior-tick values for lagged reads.
    previous: dict[str, float] = Field(default_factory=dict)


class InstitutionRecord(BaseModel):
    """An institutional actor currently represented in the run.

    Identity and role only. No authority model, no jurisdiction, no delegation — those belong to
    ORGANISATION-MODEL's M-AUTH mechanism, which is specified but not built.
    """

    agent_id: str
    role: str


class AcceptedAction(BaseModel):
    """A player decision the API accepted and recorded.

    IMPORTANT HONESTY NOTE: accepted means *recorded*, not validated, priced, legal or applied.
    Nothing in the tick loop reads this list, and no effect follows from it. It exists so the
    decision endpoint has a legitimate authoritative home instead of appending directly to the
    engine's event log from a presentation route. Applying these is P0.5 work and requires the
    validation this phase deliberately does not implement.
    """

    action_id: str
    actor_role: str
    action_type: str
    recorded_at_tick: int
    applied: bool = False
    # Deliberately preserved verbatim, and deliberately NOT trusted. On this path the client
    # supplies `legal_check` and the engine has no legality gate to overwrite it with.
    client_supplied: dict[str, Any] = Field(default_factory=dict)


class GovernmentResources(BaseModel):
    """
    What the government can actually spend. Added for Kestral Consequence Slice v0.2.

    Minimal on purpose: enough for one decision to have a cost and a limit, not a fiscal model.
    Every field is read by the declared resolution rule and by nothing else.
    """

    budget_reserve_m: float = 0.0
    political_capital: float = 0.0
    implementation_capacity: float = 0.0
    intelligence_confidence: float = 0.0


class QueuedDecision(BaseModel):
    """A submitted decision awaiting consumption. Queued, never applied on submission."""

    submission_id: str
    option_id: str
    submitted_tick: int
    #: The tick at which the engine will consume it. Never earlier than submission.
    apply_at_tick: int


class DelayedEffect(BaseModel):
    """An effect scheduled by a resolved decision, due at a declared future tick."""

    due_tick: int
    kind: str
    field: str
    value: float
    cause_submission_id: str
    why: str


class AuthoritativeState(BaseModel):
    """The single authoritative state object for one simulation run."""

    # --- versioning hooks ---
    schema_version: str = STATE_SCHEMA_VERSION
    rule_pack_version: str = RULE_PACK_VERSION
    # Monotonic count of accepted transitions. Increments once per applied transition, never
    # decrements, and is not a tick count.
    state_revision: int = 0

    # --- identity ---
    scenario: ScenarioIdentity
    run: RunMetadata

    # --- clock ---
    tick: int = 0
    timing: ScenarioTiming = Field(default_factory=ScenarioTiming)

    # --- the P0.5 causal slice ---
    chain: ChainState = Field(default_factory=ChainState)

    # --- tiers ---
    macro: MacroState
    cohorts: dict[str, CohortRuntimeState] = Field(default_factory=dict)
    narrative_adoption: dict[str, float] = Field(default_factory=dict)
    institutions: dict[str, InstitutionRecord] = Field(default_factory=dict)

    # Scenario-authored adversarial campaign configuration. Read by nothing today.
    campaign: Optional[dict[str, Any]] = None

    # --- pending, unapplied ---
    pending_actions: list[AcceptedAction] = Field(default_factory=list)

    # --- Kestral Consequence Slice v0.2 ---
    #: What the government can spend. Declared by the scenario; read by the resolution rule.
    government: GovernmentResources = Field(default_factory=GovernmentResources)
    #: Decisions waiting to be consumed. The tick loop drains this; nothing else writes it.
    decision_queue: list[QueuedDecision] = Field(default_factory=list)
    #: Submission ids already consumed. IDEMPOTENCY: a repeat submission is refused, so the same
    #: decision cannot apply its effects twice.
    consumed_submissions: list[str] = Field(default_factory=list)
    #: Effects scheduled by a resolved decision, applied when their tick arrives.
    delayed_effects: list[DelayedEffect] = Field(default_factory=list)
    #: Append-only trace: what was decided, what it resolved to, and exactly why.
    decision_log: list[dict[str, Any]] = Field(default_factory=list)

    # --- versioning hooks for capabilities that do NOT exist yet ---
    # These are deliberately empty. They are declared so the successor work has a defined home
    # and so no future change silently invents a new top-level state section. An empty dict here
    # is an honest statement that MERIDIAN models no persistent entities and no relationships.
    entities: dict[str, Any] = Field(
        default_factory=dict,
        description="P0.5/world-model hook. EMPTY: no persistent entity model exists.",
    )
    relationships: list[Any] = Field(
        default_factory=list,
        description="P0.5/world-model hook. EMPTY: no relationship graph exists.",
    )
    external_input_cursor: Optional[str] = Field(
        default=None,
        description="P0.6 hook. Always None: no external input is recorded and no replay exists.",
    )

    model_config = {"validate_assignment": True}


def canonical_json(state: AuthoritativeState) -> str:
    """Deterministic serialisation of authoritative state.

    Guarantees, so this is stable across runs and processes:
      * keys sorted at every level (`sort_keys=True`);
      * no whitespace variation (fixed separators);
      * no object identity, memory address or type repr;
      * no wall-clock timestamp — authoritative state contains none by construction;
      * `ensure_ascii` fixed so escaping cannot vary by environment.

    NOT a state hash and NOT a replay mechanism. Float formatting follows CPython's repr, which
    is stable within a build but is not a cross-language guarantee — do not claim one.
    """
    return json.dumps(
        state.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def build_initial_state(
    scenario: dict[str, Any],
    macro: MacroState,
    cohorts: list[Any],
    institutions: list[Any],
    seed: int,
) -> AuthoritativeState:
    """Assemble the authoritative state for a new run from scenario configuration."""
    from .rules.kestral_v1 import RULE_PACK

    return AuthoritativeState(
        rule_pack_version=RULE_PACK,
        scenario=ScenarioIdentity(
            scenario_id=scenario["scenario_id"],
            scenario_version=str(scenario.get("scenario_version", "unversioned")),
        ),
        run=RunMetadata(seed=seed),
        tick=0,
        macro=macro,
        timing=ScenarioTiming(**scenario.get("timing", {})),
        cohorts={
            c.cohort_id: CohortRuntimeState(
                cohort_id=c.cohort_id,
                beliefs=c.beliefs.model_dump(),
                # P0.5: copied into authoritative state because aggregation must read them.
                # `represents_population` was declared but read by NO code before this.
                represents_population=c.represents_population,
                income_sensitivity=float(
                    c.economic_profile.income_sensitivity_to_shipping_disruption
                ),
            )
            for c in cohorts
        },
        narrative_adoption={c.cohort_id: 0.0 for c in cohorts},
        institutions={
            i.agent_id: InstitutionRecord(agent_id=i.agent_id, role=i.role) for i in institutions
        },
        campaign=scenario.get("hidden_campaign"),
        government=GovernmentResources(**(scenario.get("government_resources") or {})),
    )
