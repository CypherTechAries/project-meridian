"""P0.4 — authoritative state and the transition boundary.

These test the CONTRACT, not the simulation's behaviour: that one structure holds authoritative
state, that one path mutates it, that rejected transitions change nothing, and that reads never
write.

They do not test legality, authority, resource or feasibility validation, because none exists.
`test_validation_scope_is_declared_honestly` asserts that absence is recorded rather than implied.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.simulation.engine import MeridianModel
from app.simulation.state import (
    STATE_SCHEMA_VERSION,
    AuthoritativeState,
    canonical_json,
)
from app.simulation.transitions import (
    UNIMPLEMENTED_VALIDATION,
    Transition,
    TransitionOrigin,
    TransitionService,
    TransitionType,
)

SCENARIO_PATH = Path(__file__).resolve().parents[2] / "scenarios" / "kestral-strait.json"


@pytest.fixture()
def scenario() -> dict:
    return json.loads(SCENARIO_PATH.read_text())


@pytest.fixture()
def model(scenario: dict) -> MeridianModel:
    return MeridianModel(scenario=scenario, seed=88213)


# --------------------------------------------------------------------------- #
# 1. Construction and validation
# --------------------------------------------------------------------------- #
def test_authoritative_state_constructs_with_required_sections(model: MeridianModel) -> None:
    s = model.state
    assert isinstance(s, AuthoritativeState)
    assert s.schema_version == STATE_SCHEMA_VERSION
    assert s.scenario.scenario_id == "kestral-strait"
    assert s.run.seed == 88213
    assert s.tick == 0
    assert s.state_revision == 0
    assert s.macro is not None
    assert len(s.cohorts) > 0
    assert len(s.institutions) > 0
    assert len(s.narrative_adoption) == len(s.cohorts)


def test_unbuilt_sections_are_declared_and_empty(model: MeridianModel) -> None:
    """Entities, relationships and the external-input cursor are versioning hooks.

    They must exist so successor work has a defined home, and must be EMPTY because MERIDIAN
    models no persistent entities, no relationship graph and records no external input. A
    populated field here would be a claim the engine cannot support.
    """
    s = model.state
    assert s.entities == {}
    assert s.relationships == []
    assert s.external_input_cursor is None
    assert s.run.named_substreams is False  # P0.4A has not happened


# --------------------------------------------------------------------------- #
# 2. Determinism of an accepted transition
# --------------------------------------------------------------------------- #
def test_same_transition_on_same_state_gives_same_result(scenario: dict) -> None:
    a = MeridianModel(scenario=scenario, seed=4242)
    b = MeridianModel(scenario=scenario, seed=4242)

    t = Transition(
        type=TransitionType.APPLY_MACRO_DELTAS,
        origin=TransitionOrigin.ENGINE_RULE,
        payload={"deltas": {"government_approval": 0.01}},
        mechanism="test",
    )
    ra = a.submit(t)
    rb = b.submit(t)

    assert ra.applied and rb.applied
    assert ra.delta == rb.delta
    assert canonical_json(a.state) == canonical_json(b.state)


def test_state_version_increments_only_on_applied_transitions(model: MeridianModel) -> None:
    start = model.state.state_revision

    ok = model.submit(
        Transition(
            type=TransitionType.APPLY_MACRO_DELTAS,
            origin=TransitionOrigin.ENGINE_RULE,
            payload={"deltas": {"government_approval": 0.001}},
        )
    )
    assert ok.applied
    assert model.state.state_revision == start + 1

    bad = model.submit(
        Transition(
            type=TransitionType.APPLY_MACRO_DELTAS,
            origin=TransitionOrigin.ENGINE_RULE,
            payload={"deltas": {"not_a_real_indicator": 1.0}},
        )
    )
    assert not bad.applied
    assert model.state.state_revision == start + 1  # unchanged by the rejection


# --------------------------------------------------------------------------- #
# 3. Rejected transitions leave state untouched
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "transition",
    [
        # Unknown indicator — previously a SILENT skip that produced no error and no effect.
        Transition(
            type=TransitionType.APPLY_MACRO_DELTAS,
            origin=TransitionOrigin.ENGINE_RULE,
            payload={"deltas": {"misspelled_indicator": 0.5}},
        ),
        # Nested block, not a top-level scalar — the fiscal-state gap.
        Transition(
            type=TransitionType.APPLY_MACRO_DELTAS,
            origin=TransitionOrigin.ENGINE_RULE,
            payload={"deltas": {"public_finances": 1.0}},
        ),
        Transition(
            type=TransitionType.SET_COHORT_BELIEF,
            origin=TransitionOrigin.ENGINE_RULE,
            payload={"cohort_id": "no-such-cohort", "belief": "government_competence", "value": 0.5},
        ),
        Transition(
            type=TransitionType.SET_NARRATIVE_ADOPTION,
            origin=TransitionOrigin.ENGINE_RULE,
            payload={"adoption": {"no-such-cohort": 0.9}},
        ),
        # Stale optimistic-concurrency token.
        Transition(
            type=TransitionType.ADVANCE_TICK,
            origin=TransitionOrigin.ENGINE_RULE,
            expected_state_revision=9999,
        ),
    ],
)
def test_rejected_transition_leaves_state_byte_identical(
    model: MeridianModel, transition: Transition
) -> None:
    before = canonical_json(model.state)
    record = model.submit(transition)
    assert not record.applied
    assert record.validation.errors
    assert canonical_json(model.state) == before


def test_unknown_macro_key_is_rejected_not_silently_skipped(model: MeridianModel) -> None:
    """The audit recorded that `apply_deltas` silently ignored unrecognised keys.

    A misspelled or nested indicator produced no error, no warning and no effect, so a rule pack
    could author an effect that never applied and nothing would report it. It is now an error.
    """
    record = model.submit(
        Transition(
            type=TransitionType.APPLY_MACRO_DELTAS,
            origin=TransitionOrigin.ENGINE_RULE,
            payload={"deltas": {"govrenment_approval": 0.01}},  # deliberate typo
        )
    )
    assert not record.applied
    assert any("unknown macro indicator" in e for e in record.validation.errors)


# --------------------------------------------------------------------------- #
# 4 & 5. Reads never write; model output cannot mutate state
# --------------------------------------------------------------------------- #
def test_presentation_origin_is_rejected(model: MeridianModel) -> None:
    """A read path must never mutate authoritative state, even with a well-formed payload."""
    before = canonical_json(model.state)
    record = model.submit(
        Transition(
            type=TransitionType.APPLY_MACRO_DELTAS,
            origin=TransitionOrigin.PRESENTATION,
            payload={"deltas": {"government_approval": 0.5}},
        )
    )
    assert not record.applied
    assert any("presentation" in e for e in record.validation.errors)
    assert canonical_json(model.state) == before


def test_derived_reads_do_not_mutate_state(model: MeridianModel) -> None:
    """Snapshots, canonical serialisation and briefings are derived reads."""
    from app.simulation.llm_gateway import generate_briefing

    model.run(3)
    before = canonical_json(model.state)

    model.macro_snapshot()
    model.canonical_state()
    generate_briefing(model.macro_snapshot())
    _ = model.state.cohorts
    _ = model.narrative_adoption

    assert canonical_json(model.state) == before


def test_llm_proposal_cannot_carry_state_authority(model: MeridianModel) -> None:
    """The gateway returns a proposal; the engine owns the magnitude.

    An LLM-origin transition is permitted — that is how a priced proposal reaches state — but the
    proposal itself cannot name a magnitude, and an unknown action type yields no effect.
    """
    from app.simulation.llm_gateway import propose_action

    proposal = propose_action(
        agent={"agent_id": "min-defence-oduya", "role": "minister_of_defence"},
        context={"tick": 0, "scenario_id": "kestral-strait"},
    )
    assert not hasattr(proposal, "apply_deltas")
    assert not hasattr(proposal, "macro_state")

    before = canonical_json(model.state)
    # An action type absent from ACTION_EFFECTS prices to nothing.
    assert model._price(type(proposal)(**{**proposal.model_dump(), "action_type": "invented"})) == {}
    assert canonical_json(model.state) == before


# --------------------------------------------------------------------------- #
# 6. Engine behaviour still routed and covered
# --------------------------------------------------------------------------- #
def test_every_engine_mutation_passes_through_the_boundary(model: MeridianModel) -> None:
    model.run(3)
    assert model.transition_log, "engine produced no transitions"
    # Every applied transition carries a declared type and origin.
    for r in model.transition_log:
        assert r.type in set(TransitionType)
        assert r.origin in set(TransitionOrigin)
    applied = [r for r in model.transition_log if r.applied]
    kinds = {r.type for r in applied}
    assert TransitionType.ADVANCE_TICK in kinds
    assert TransitionType.APPLY_MACRO_DELTAS in kinds
    # state_revision counts applied transitions exactly.
    assert model.state.state_revision == len(applied)


def test_applied_transitions_carry_mechanism_attribution(model: MeridianModel) -> None:
    """Every aggregate change should name the mechanism that produced it."""
    model.run(2)
    for r in model.transition_log:
        if r.applied and r.type is not TransitionType.ADVANCE_TICK:
            assert r.mechanism, f"{r.type} applied with no mechanism attribution"


def test_tick_advances_only_through_a_transition(model: MeridianModel) -> None:
    assert model.tick == 0
    model.step()
    assert model.tick == 1
    assert model.state.macro.tick == 1  # macro's tick copy stays in step
    ticks = [r for r in model.transition_log if r.type is TransitionType.ADVANCE_TICK and r.applied]
    assert len(ticks) == 1


def test_cohort_belief_changes_go_through_the_boundary(model: MeridianModel) -> None:
    """Belief was previously written in place by the agent, bypassing every check."""
    model.run(5)
    belief_txns = [
        r for r in model.transition_log if r.type is TransitionType.SET_COHORT_BELIEF and r.applied
    ]
    assert belief_txns, "no cohort belief transition recorded"
    for r in belief_txns:
        assert r.delta  # before/after captured
        assert r.mechanism


def test_player_decision_is_recorded_but_not_applied(model: MeridianModel) -> None:
    """The decision endpoint's write now lands in pending_actions, and applies nothing."""
    before_macro = model.macro_snapshot()
    record = model.submit(
        Transition(
            type=TransitionType.RECORD_PLAYER_DECISION,
            origin=TransitionOrigin.PLAYER_DECISION,
            payload={
                "action_id": "act-1",
                "actor_role": "janitor_with_no_authority",
                "action_type": "nationalise_everything",
                "client_supplied": {"legal_check": "LEGAL_AND_APPROVED"},
            },
        )
    )
    assert record.applied  # recorded
    assert len(model.state.pending_actions) == 1
    action = model.state.pending_actions[0]
    assert action.applied is False
    # The client's own legality assertion is preserved verbatim and NOT trusted.
    assert action.client_supplied["legal_check"] == "LEGAL_AND_APPROVED"
    # Recording changed no macro value.
    assert model.macro_snapshot() == before_macro


# --------------------------------------------------------------------------- #
# 7. Canonical serialisation
# --------------------------------------------------------------------------- #
def test_canonical_serialisation_is_stable_across_repeated_calls(model: MeridianModel) -> None:
    model.run(5)
    assert len({model.canonical_state() for _ in range(20)}) == 1


def test_canonical_serialisation_is_key_order_independent(model: MeridianModel) -> None:
    """Serialisation must not depend on dict insertion order.

    Tested on the serialiser directly rather than through a transition: applying a transition
    legitimately increments `state_revision`, so two states would differ for a valid reason and
    the comparison would prove nothing about key ordering.
    """
    model.run(2)
    original = model.state

    reordered = original.model_copy(deep=True)
    # Rebuild both dict-valued sections in reverse insertion order.
    reordered.narrative_adoption = dict(reversed(list(original.narrative_adoption.items())))
    reordered.cohorts = dict(reversed(list(original.cohorts.items())))
    reordered.institutions = dict(reversed(list(original.institutions.items())))
    for cid, cohort in reordered.cohorts.items():
        cohort.beliefs = dict(reversed(list(original.cohorts[cid].beliefs.items())))

    # Insertion order differs; canonical output must not.
    assert list(reordered.narrative_adoption) != list(original.narrative_adoption)
    assert canonical_json(reordered) == canonical_json(original)


def test_canonical_serialisation_contains_no_object_identity(model: MeridianModel) -> None:
    """No memory addresses, no type reprs, no wall-clock timestamps."""
    model.run(3)
    blob = model.canonical_state()
    assert "0x" not in blob
    assert "object at" not in blob
    assert "<" not in blob
    json.loads(blob)  # must be valid JSON


def test_two_runs_same_seed_serialise_identically(scenario: dict) -> None:
    a = MeridianModel(scenario=scenario, seed=88213)
    b = MeridianModel(scenario=scenario, seed=88213)
    a.run(10)
    b.run(10)
    # Stronger than the existing macro-only determinism test: this compares the WHOLE
    # authoritative state, including cohort beliefs and narrative adoption, which the original
    # same-seed test never inspected.
    assert a.canonical_state() == b.canonical_state()


# --------------------------------------------------------------------------- #
# Honesty of the validation scope
# --------------------------------------------------------------------------- #
def test_validation_scope_is_declared_honestly(model: MeridianModel) -> None:
    """Structural acceptance must never be mistakeable for policy approval."""
    record = model.submit(
        Transition(
            type=TransitionType.APPLY_MACRO_DELTAS,
            origin=TransitionOrigin.ENGINE_RULE,
            payload={"deltas": {"government_approval": 0.001}},
        )
    )
    assert record.applied
    # The result carries what was NOT checked.
    assert record.validation.unimplemented == UNIMPLEMENTED_VALIDATION
    joined = " ".join(UNIMPLEMENTED_VALIDATION)
    for missing in ("legality", "authority", "resource", "feasibility"):
        assert missing in joined


def test_transition_service_rejects_unknown_type_by_construction() -> None:
    """The transition type set is closed: a new mutation path cannot appear undeclared."""
    with pytest.raises(Exception):
        Transition(type="quietly_invented_type", origin=TransitionOrigin.ENGINE_RULE)  # type: ignore[arg-type]


def test_service_is_the_only_documented_writer(model: MeridianModel) -> None:
    """`TransitionService.state` is a read view; enforcement is by test, not by the type system.

    Recorded as a known limitation: Python cannot prevent a caller mutating the returned Pydantic
    model without freezing it, which would break in-place application inside the service.
    """
    assert isinstance(model._transitions, TransitionService)
    assert model._transitions.state is model.state


def test_retired_macro_state_holder_is_a_tripwire() -> None:
    """The old mutation path must fail loudly rather than sit dormant and reusable."""
    from app.simulation.agents.macro_state import MacroStateHolder

    with pytest.raises(NotImplementedError, match="retired by Phase 0 item P0.4"):
        MacroStateHolder(None)
    with pytest.raises(NotImplementedError):
        MacroStateHolder.apply_deltas(object(), {"government_approval": 1.0})  # type: ignore[arg-type]
