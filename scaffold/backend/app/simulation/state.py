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

# The engine's behavioural rules are not yet packaged or versioned independently of the code.
# Recorded honestly as a placeholder so the field exists for the first real rule pack.
RULE_PACK_VERSION = "unversioned-inline-0"


class ScenarioIdentity(BaseModel):
    """Which scenario this run is of, and at what version."""

    scenario_id: str
    # Scenario files carry no version field today; recorded as unknown rather than invented.
    scenario_version: str = "unversioned"


class RunMetadata(BaseModel):
    """Seed and generator metadata for the run.

    `rng_algorithm` records what actually produced the draws. It is `python-random-Mersenne`
    today because the engine uses `random.Random`. P0.4A replaces this with a keyed/counter-based
    draw service (ADR-010) and this field becomes the recorded algorithm + version.
    """

    seed: int
    rng_algorithm: str = "python-random-Mersenne"
    rng_algorithm_version: str = "cpython-stdlib"
    # P0.4A: there are NO named draw substreams today. A draw added anywhere shifts every later
    # draw everywhere else. This field exists so the successor architecture has a home.
    named_substreams: bool = False


class CohortRuntimeState(BaseModel):
    """The MUTABLE belief values for one cohort.

    The cohort's static configuration (demographics, media exposure, susceptibility, grievances,
    `represents_population`) stays in the scenario-derived `Cohort` spec and is NOT authoritative
    runtime state — nothing mutates it. Only the beliefs below change during a run.
    """

    cohort_id: str
    beliefs: dict[str, float] = Field(default_factory=dict)


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

    # --- tiers ---
    macro: MacroState
    cohorts: dict[str, CohortRuntimeState] = Field(default_factory=dict)
    narrative_adoption: dict[str, float] = Field(default_factory=dict)
    institutions: dict[str, InstitutionRecord] = Field(default_factory=dict)

    # Scenario-authored adversarial campaign configuration. Read by nothing today.
    campaign: Optional[dict[str, Any]] = None

    # --- pending, unapplied ---
    pending_actions: list[AcceptedAction] = Field(default_factory=list)

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
    return AuthoritativeState(
        scenario=ScenarioIdentity(
            scenario_id=scenario["scenario_id"],
            scenario_version=str(scenario.get("scenario_version", "unversioned")),
        ),
        run=RunMetadata(seed=seed),
        tick=0,
        macro=macro,
        cohorts={
            c.cohort_id: CohortRuntimeState(
                cohort_id=c.cohort_id, beliefs=c.beliefs.model_dump()
            )
            for c in cohorts
        },
        narrative_adoption={c.cohort_id: 0.0 for c in cohorts},
        institutions={
            i.agent_id: InstitutionRecord(agent_id=i.agent_id, role=i.role) for i in institutions
        },
        campaign=scenario.get("hidden_campaign"),
    )
