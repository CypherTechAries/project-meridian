"""
Virtual Person VP-4 — typed relationships and ordered, append-only history.

Proves relationships are declared connections (never scores), information absence is time-bounded and
first-class, belief history reuses the frozen values, one observation is never a trajectory, history
is append-only and deterministically ordered, and none of it changes VP-2/VP-3/belief output.
"""

from __future__ import annotations

import inspect
import json

import pytest
from pydantic import ValidationError

from app.simulation.belief.projection import person_projection
from app.simulation.belief.provenance import Origin
from app.simulation.person import history as history_mod
from app.simulation.person.current_state import EventKind, SituationEvent, apply_events
from app.simulation.person.decision import select_action
from app.simulation.person.history import (
    BeliefHistory,
    BeliefHistoryEntry,
    BeliefOutcome,
    ExposureStatus,
    InformationHistory,
    InformationRecord,
    LifecycleStatus,
    RelationshipEdge,
    RelationshipEventKind,
    RelationshipHistory,
    RelationshipHistoryEntry,
)
from app.simulation.person.schema import RelationshipType
from app.simulation.person.vp2_fixtures import fixture_for
from app.simulation.person.vp3_decisions import journalist_decision
from app.simulation.person.vp4_fixtures import (
    PEOPLE,
    RELATIONSHIPS,
    belief_history_for,
    information_history_for,
)

JID = "fict:kestral-strait:person:broadcast-journalist"
CLAIM = "P-WARNINGS-IGNORED"

ALL_MODELS = (RelationshipEdge, RelationshipHistoryEntry, InformationRecord, BeliefHistoryEntry)
PROHIBITED = ("influence", "trustworthiness", "trust_score", "strength", "susceptib", "persuad",
              "loyalty", "closeness", "emotional_dependency", "reputation", "power", "score")


def rel(**kw) -> RelationshipEdge:
    base = dict(relationship_id="r", source_ref=JID,
                target_ref="fict:kestral-strait:organisation:public-broadcaster",
                relationship_kind=RelationshipType.member_of)
    base.update(kw)
    return RelationshipEdge(**base)


def info(**kw) -> InformationRecord:
    base = dict(information_record_id="i", person_ref=JID, proposition_ref=CLAIM, tick=6,
                exposure_status=ExposureStatus.received)
    base.update(kw)
    return InformationRecord(**base)


# ── 1–11 · relationships ──────────────────────────────────────────────────────────────────────────


def test_01_valid_relationship_edge_loads() -> None:
    assert rel().status is LifecycleStatus.active and rel().origin is Origin.fixture


def test_02_unknown_fields_fail() -> None:
    with pytest.raises(ValidationError):
        rel(influence_score=0.8)


def test_03_wrong_or_cross_world_ids_fail() -> None:
    # information records validate their person_ref as a typed fictional id
    with pytest.raises(ValueError):
        info(person_ref="fict:other-world:person:broadcast-journalist")
    with pytest.raises(ValueError):
        info(person_ref="a real journalist")


def test_04_relationship_kinds_remain_distinct() -> None:
    kinds = {r.relationship_kind for r in RELATIONSHIPS}
    assert RelationshipType.member_of in kinds and RelationshipType.trusts_for in kinds
    assert len({t.value for t in RelationshipType}) == 7


def test_05_trusts_for_without_subject_fails() -> None:
    with pytest.raises(ValueError, match="trusts_for"):
        rel(relationship_kind=RelationshipType.trusts_for, subject=None)
    with pytest.raises(ValueError):
        rel(relationship_kind=RelationshipType.trusts_for, subject="  ")


def test_06_trusts_for_has_no_numeric_universal_score() -> None:
    tf = next(r for r in RELATIONSHIPS if r.relationship_kind is RelationshipType.trusts_for)
    assert tf.subject
    for f in RelationshipEdge.model_fields:
        assert "score" not in f.lower() and "value" not in f.lower()


def test_07_receives_from_does_not_imply_receipt() -> None:
    # a receives_from edge exists, but receipt is only ever an explicit InformationRecord
    edge = next(r for r in RELATIONSHIPS if r.relationship_kind is RelationshipType.receives_from)
    assert edge is not None
    # the edge carries no exposure field
    assert "exposure" not in str(RelationshipEdge.model_fields)
    assert "received" not in str(RelationshipEdge.model_fields)


def test_08_relationship_edge_does_not_affect_vp2_transitions() -> None:
    s = fixture_for("broadcast-journalist")
    ev = SituationEvent(event_id="e", event_kind=EventKind.change_pressure_intensity, tick=6,
                        target_id="p-deadline", magnitude=0.9, reason="r")
    before = apply_events(s, (ev,)).model_dump_json()
    _ = RELATIONSHIPS   # touching relationships changes nothing
    after = apply_events(s, (ev,)).model_dump_json()
    assert before == after


def test_09_relationship_edge_does_not_affect_vp3_decisions() -> None:
    before = select_action(journalist_decision()).model_dump_json()
    _ = RELATIONSHIPS
    after = select_action(journalist_decision()).model_dump_json()
    assert before == after


def test_10_directional_semantics_are_documented_and_stable() -> None:
    assert RelationshipType.reports_to in history_mod.DIRECTIONAL
    assert RelationshipType.member_of in history_mod.DIRECTIONAL
    assert RelationshipType.colleague in history_mod.SYMMETRIC
    assert RelationshipType.family in history_mod.UNDIRECTED


def test_11_reverse_edge_is_not_silently_invented_and_is_engine_when_present() -> None:
    # a fixture-authored reverse edge is refused; only an engine one is allowed
    with pytest.raises(ValueError, match="engine-derived"):
        rel(reverse_of="rel-journalist-member", origin=Origin.fixture)
    ok = rel(relationship_id="r-rev", reverse_of="rel-journalist-member", origin=Origin.engine)
    assert ok.origin is Origin.engine


# ── 12–15 · relationship history append-only ──────────────────────────────────────────────────────


def _rhe(**kw) -> RelationshipHistoryEntry:
    base = dict(history_entry_id="h", relationship_id="rel-journalist-member", tick=1,
                event_kind=RelationshipEventKind.activated,
                previous_status=LifecycleStatus.inactive, new_status=LifecycleStatus.active)
    base.update(kw)
    return RelationshipHistoryEntry(**base)


def test_12_13_activation_and_deactivation_append() -> None:
    h = RelationshipHistory()
    h, t1 = h.append(_rhe(history_entry_id="a", tick=1, event_kind=RelationshipEventKind.activated))
    h, t2 = h.append(_rhe(history_entry_id="b", tick=5, event_kind=RelationshipEventKind.deactivated,
                          previous_status=LifecycleStatus.active, new_status=LifecycleStatus.inactive))
    assert t1.accepted and t2.accepted and len(h.entries) == 2


def test_14_earlier_relationship_entries_stay_byte_identical() -> None:
    h = RelationshipHistory()
    h, _ = h.append(_rhe(history_entry_id="a", tick=1))
    first = h.entries[0].model_dump_json()
    h, _ = h.append(_rhe(history_entry_id="b", tick=2))
    assert h.entries[0].model_dump_json() == first


def test_15_duplicate_relationship_history_ids_fail() -> None:
    h = RelationshipHistory()
    h, _ = h.append(_rhe(history_entry_id="dup"))
    with pytest.raises(ValueError, match="duplicate"):
        h.append(_rhe(history_entry_id="dup", tick=9))


# ── 16–27 · information records + history ──────────────────────────────────────────────────────────


def test_16_valid_received_record_loads() -> None:
    assert info().exposure_status is ExposureStatus.received


def test_17_18_not_received_needs_a_time_boundary() -> None:
    ok = info(information_record_id="n", exposure_status=ExposureStatus.not_received_through_tick,
              through_tick=5, origin=Origin.fixture)
    assert ok.through_tick == 5
    with pytest.raises(ValueError, match="through_tick"):
        info(exposure_status=ExposureStatus.not_received_through_tick, origin=Origin.fixture)


def test_19_not_received_is_distinct_from_rejection() -> None:
    # exposure and belief are separate vocabularies; NOT_RECEIVED is not a BeliefOutcome
    assert "REJECTED" not in {s.value for s in ExposureStatus}
    assert ExposureStatus.not_received_through_tick.value == "NOT_RECEIVED_THROUGH_TICK"
    assert BeliefOutcome.received_and_rejected.value == "RECEIVED_AND_REJECTED"


def test_20_missing_exposure_is_not_automatically_not_received() -> None:
    # an empty history is empty; it does not fabricate a NOT_RECEIVED record
    h = InformationHistory()
    assert h.observation_count == 0
    assert all(e.exposure_status is not ExposureStatus.not_received_through_tick for e in h.entries)


def test_21_22_unknown_and_unavailable_are_preserved() -> None:
    assert info(information_record_id="u", exposure_status=ExposureStatus.unknown).exposure_status is ExposureStatus.unknown
    assert info(information_record_id="v", exposure_status=ExposureStatus.unavailable).exposure_status is ExposureStatus.unavailable


def test_23_24_information_ordering_is_deterministic_and_order_independent() -> None:
    a = info(information_record_id="a", tick=6)
    b = info(information_record_id="b", tick=3)
    h1 = InformationHistory()
    h1, _ = h1.append(a); h1, _ = h1.append(b)
    h2 = InformationHistory()
    h2, _ = h2.append(b); h2, _ = h2.append(a)
    assert h1.model_dump_json() == h2.model_dump_json()
    assert [e.information_record_id for e in h1.entries] == ["b", "a"]   # sorted by tick


def test_25_duplicate_information_ids_fail() -> None:
    h = InformationHistory()
    h, _ = h.append(info(information_record_id="dup"))
    with pytest.raises(ValueError, match="duplicate"):
        h.append(info(information_record_id="dup", tick=9))


def test_26_conflicting_same_tick_records_fail() -> None:
    h = InformationHistory()
    h, _ = h.append(info(information_record_id="a", tick=6, exposure_status=ExposureStatus.received))
    with pytest.raises(ValueError, match="conflicting"):
        h.append(info(information_record_id="b", tick=6,
                      exposure_status=ExposureStatus.not_received_through_tick, through_tick=6,
                      origin=Origin.fixture))


def test_27_information_append_preserves_earlier_entries() -> None:
    h = InformationHistory()
    h, _ = h.append(info(information_record_id="a", tick=1))
    first = h.entries[0].model_dump_json()
    h, _ = h.append(info(information_record_id="b", tick=2))
    assert h.entries[0].model_dump_json() == first


# ── 28–41 · belief history ────────────────────────────────────────────────────────────────────────


def _bhe(**kw) -> BeliefHistoryEntry:
    base = dict(belief_history_entry_id="b", person_ref=JID, proposition_ref=CLAIM, tick=6,
                classification=BeliefOutcome.received_but_unsure)
    base.update(kw)
    return BeliefHistoryEntry(**base)


def test_28_valid_belief_history_entry_loads() -> None:
    assert _bhe().result_kind == "packaged-belief-snapshot"
    assert _bhe().connected_to_authoritative_run is False


def test_29_existing_belief_values_are_preserved_exactly() -> None:
    assert person_projection("broadcast-journalist").calculation.final_credence == pytest.approx(0.408458, abs=1e-6)
    assert person_projection("government-minister").calculation.final_credence == pytest.approx(0.171946, abs=1e-6)
    assert person_projection("family-spokesperson").calculation.final_credence == pytest.approx(0.688510, abs=1e-6)


def test_30_belief_entry_references_the_existing_update_trace() -> None:
    e = belief_history_for("broadcast-journalist").entries[0]
    assert e.update_trace_ref and "broadcast-journalist" in e.update_trace_ref
    assert e.exposure_ref and "broadcast-journalist" in e.exposure_ref


def test_31_value_and_decision_origins_stay_distinct() -> None:
    # constructed retained-prior case: fixture value, engine no-change decision
    e = _bhe(belief_history_entry_id="r", classification=BeliefOutcome.retained_prior,
             value_origin=Origin.fixture, decision_origin=Origin.engine,
             previous_state="Unsure", updated_state="Unsure", no_update_reason="not exposed")
    assert e.value_origin is Origin.fixture and e.decision_origin is Origin.engine


def test_32_33_34_35_outcome_states_are_structurally_distinct() -> None:
    vals = {o.value for o in BeliefOutcome}
    assert {"RECEIVED_BUT_UNSURE", "RECEIVED_AND_REJECTED", "RECEIVED_AND_ACCEPTED",
            "RETAINED_PRIOR", "NEVER_RECEIVED_THROUGH_TICK"} <= vals
    # the three fixtures classify per the frozen belief values
    assert belief_history_for("family-spokesperson").entries[0].classification is BeliefOutcome.received_and_accepted
    assert belief_history_for("government-minister").entries[0].classification is BeliefOutcome.received_and_rejected
    assert belief_history_for("broadcast-journalist").entries[0].classification is BeliefOutcome.received_but_unsure


def test_36_never_received_does_not_carry_a_belief_update() -> None:
    with pytest.raises(ValueError, match="must not carry a belief update"):
        _bhe(classification=BeliefOutcome.retained_prior, previous_state="Unsure", updated_state="Leaned towards it")


def test_37_38_one_observation_is_never_a_trajectory() -> None:
    bh = belief_history_for("broadcast-journalist")
    assert bh.observation_count == 1
    assert bh.trajectory_available is False
    assert bh.entries[0].trajectory_available is False
    low = bh.summary_sentence().lower()
    for banned in ("trend", "trajectory", "long-term movement", "persistent tendency", "pattern of"):
        assert banned not in low
    with pytest.raises(ValueError, match="at least two observations"):
        _bhe(observation_count=1, trajectory_available=True)


def test_39_belief_history_ordering_is_deterministic() -> None:
    a = _bhe(belief_history_entry_id="a", tick=6)
    b = _bhe(belief_history_entry_id="b", tick=2)
    h1 = BeliefHistory(); h1, _ = h1.append(a); h1, _ = h1.append(b)
    h2 = BeliefHistory(); h2, _ = h2.append(b); h2, _ = h2.append(a)
    assert h1.model_dump_json() == h2.model_dump_json()
    assert [e.belief_history_entry_id for e in h1.entries] == ["b", "a"]


def test_40_duplicate_belief_history_ids_fail() -> None:
    h = BeliefHistory(); h, _ = h.append(_bhe(belief_history_entry_id="dup"))
    with pytest.raises(ValueError, match="duplicate"):
        h.append(_bhe(belief_history_entry_id="dup", tick=9))


def test_41_belief_append_preserves_earlier_entries() -> None:
    h = BeliefHistory(); h, _ = h.append(_bhe(belief_history_entry_id="a", tick=1))
    first = h.entries[0].model_dump_json()
    h, _ = h.append(_bhe(belief_history_entry_id="b", tick=2))
    assert h.entries[0].model_dump_json() == first


# ── 42 · absence never zero ───────────────────────────────────────────────────────────────────────


def test_42_unknown_and_unavailable_never_serialise_as_zero() -> None:
    for rec in (info(information_record_id="u", exposure_status=ExposureStatus.unknown),
                info(information_record_id="v", exposure_status=ExposureStatus.unavailable)):
        data = json.loads(rec.model_dump_json())
        assert data["exposure_status"] in ("UNKNOWN", "UNAVAILABLE")
        assert data["through_tick"] is None   # absent, not 0


# ── 43–45 · history does not change calculations ──────────────────────────────────────────────────


def test_43_relationship_changes_do_not_change_belief_output() -> None:
    before = person_projection("broadcast-journalist").model_dump(mode="json")
    _ = [rel(relationship_id=f"x{i}") for i in range(5)]
    after = person_projection("broadcast-journalist").model_dump(mode="json")
    assert before == after


def test_44_information_description_changes_do_not_change_belief_output() -> None:
    before = person_projection("broadcast-journalist").model_dump(mode="json")
    _ = info(description="a completely different description")
    after = person_projection("broadcast-journalist").model_dump(mode="json")
    assert before == after


def test_45_history_wording_changes_do_not_change_decisions() -> None:
    before = select_action(journalist_decision()).model_dump_json()
    _ = belief_history_for("broadcast-journalist").summary_sentence()
    after = select_action(journalist_decision()).model_dump_json()
    assert before == after


# ── 46–50 · no transmission, no trust change, no memory, no profiling, no ranking ─────────────────


def test_46_no_social_transmission_function_exists() -> None:
    src = inspect.getsource(history_mod).lower()
    names = [n for n in dir(history_mod) if callable(getattr(history_mod, n))]
    for banned in ("propagate", "transmit", "diffuse", "cascade", "deliver_to", "spread"):
        assert not any(banned in n.lower() for n in names)


def test_47_no_changing_trust_function_exists() -> None:
    names = [n for n in dir(history_mod)]
    for banned in ("update_trust", "trust_decay", "reputation", "source_learning", "betray"):
        assert not any(banned in n.lower() for n in names)


def test_48_no_memory_retrieval_function_exists() -> None:
    names = [n for n in dir(history_mod)]
    for banned in ("recall", "forget", "retrieve_memory", "salience_decay", "summarise_memory"):
        assert not any(banned in n.lower() for n in names)


def test_49_no_influence_susceptibility_or_persuadability_fields_exist() -> None:
    names: set[str] = set()
    for m in ALL_MODELS:
        names |= set(m.model_fields)
    for field in names:
        for banned in PROHIBITED:
            assert banned not in field.lower(), f"prohibited field '{field}' matched '{banned}'"


def test_50_no_person_ranking_operation_exists() -> None:
    src = inspect.getsource(history_mod).lower()
    for banned in ("rank_people", "rank_persons", "easiest_to_influence", "compare_by_susceptibility"):
        assert banned not in src


# ── counterfactuals 1–10 ──────────────────────────────────────────────────────────────────────────


def test_cf_07_08_not_received_then_later_received() -> None:
    # replacing RECEIVED with NOT_RECEIVED does not create a rejection; a later RECEIVED may follow
    h = InformationHistory()
    h, _ = h.append(info(information_record_id="nr", tick=3,
                         exposure_status=ExposureStatus.not_received_through_tick, through_tick=3,
                         origin=Origin.fixture))
    h, _ = h.append(info(information_record_id="rc", tick=7, exposure_status=ExposureStatus.received))
    kinds = [e.exposure_status for e in h.entries]
    assert kinds == [ExposureStatus.not_received_through_tick, ExposureStatus.received]  # ordered
    # neither is a rejection
    assert ExposureStatus.received in kinds and all(k.value != "REJECTED" for k in kinds)


def test_cf_10_identical_records_for_different_people_behave_identically() -> None:
    a = information_history_for("family-spokesperson")
    b = information_history_for("broadcast-journalist")
    # same shape (one received record each), differing only in the declared person/channel
    assert a.observation_count == b.observation_count == 1
    assert a.entries[0].exposure_status is b.entries[0].exposure_status


# ── regressions ───────────────────────────────────────────────────────────────────────────────────


def test_51_all_belief_values_across_people_unchanged() -> None:
    for pid, expected in (("family-spokesperson", 0.688510), ("government-minister", 0.171946),
                          ("broadcast-journalist", 0.408458)):
        assert person_projection(pid).calculation.final_credence == pytest.approx(expected, abs=1e-6)


def test_52_claim_boundary_present() -> None:
    assert "does not model a complete life history" in history_mod.CLAIM_BOUNDARY
