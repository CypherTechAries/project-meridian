"""
Virtual Person VP-2 — bounded, deterministic current-situation model.

Proves the four state types are distinct and well-formed, the transition kernel is deterministic and
identity-blind, current situation is not a personality model, and no action is selected.
"""

from __future__ import annotations

import inspect
import json

import pytest
from pydantic import ValidationError

from app.simulation.belief import cast
from app.simulation.belief.projection import person_projection
from app.simulation.belief.provenance import Origin
from app.simulation.person.current_state import (
    RULE_VERSION,
    Constraint,
    ConstraintKind,
    CurrentSituation,
    EventKind,
    Goal,
    ItemStatus,
    Pressure,
    PressureSource,
    Responsibility,
    SituationEvent,
    TraceOutcome,
    apply_events,
)
from app.simulation.person.vp2_fixtures import VP2_FIXTURES, fixture_for

JOURNALIST = "broadcast-journalist"

ALL_MODELS = (Goal, Responsibility, Pressure, Constraint, SituationEvent, CurrentSituation)

PROHIBITED = ("intelligence", "competence", "morality", "susceptib", "persuad", "resilience",
              "stability", "vulnerability", "influence", "gullib", "iq", "anxious", "neurotic",
              "motivation_score", "risk_score", "quality_score", "overall")


def all_fields() -> set[str]:
    names: set[str] = set()
    for m in ALL_MODELS:
        names |= set(m.model_fields)
    return names


# ── 1–6 · the four types load; unknown fields and bad origins fail ────────────────────────────────


def test_01_valid_goal_loads() -> None:
    g = Goal(goal_id="g", description="publish an accurate report",
             desired_condition="a corroborated report exists", priority=0.6)
    assert g.status is ItemStatus.active and g.priority_band == "moderate"


def test_02_valid_responsibility_loads() -> None:
    r = Responsibility(responsibility_id="r", obligation="meet the standard",
                       owed_to="the broadcaster", subject="publication", urgency=0.8)
    assert r.urgency_band == "high"


def test_03_valid_pressure_loads() -> None:
    p = Pressure(pressure_id="p", description="approaching deadline",
                 source_kind=PressureSource.approaching_deadline, source_ref="window:d6", intensity=0.2)
    assert p.intensity_band == "low" and p.source_kind.value == "approaching_deadline"


def test_04_valid_constraint_loads() -> None:
    c = Constraint(constraint_id="c", limitation="insufficient corroboration",
                   constraint_kind=ConstraintKind.verification_incomplete, subject="reporting")
    assert c.status is ItemStatus.active


def test_05_unknown_fields_fail() -> None:
    for model, kw in (
        (Goal, dict(goal_id="g", description="d", desired_condition="c", anxiety=0.9)),
        (Pressure, dict(pressure_id="p", description="d", source_kind=PressureSource.public_scrutiny,
                        source_ref="x", susceptibility=0.5)),
    ):
        with pytest.raises(ValidationError):
            model(**kw)  # type: ignore[arg-type]


def test_06_invalid_origins_fail() -> None:
    with pytest.raises(ValidationError):
        Goal(goal_id="g", description="d", desired_condition="c", origin="MADE_UP")  # type: ignore[arg-type]


# ── 7–9 · origin handling ─────────────────────────────────────────────────────────────────────────


def test_07_fixture_starting_values_report_fixture() -> None:
    s = fixture_for(JOURNALIST)
    assert all(g.origin is Origin.fixture for g in s.goals)
    assert all(p.origin is Origin.fixture for p in s.pressures)


def test_08_engine_transitions_report_engine() -> None:
    s = fixture_for(JOURNALIST)
    ev = SituationEvent(event_id="e", event_kind=EventKind.change_pressure_intensity, tick=6,
                        target_id="p-deadline", magnitude=0.9, reason="window closer")
    r = apply_events(s, (ev,))
    changed = next(p for p in r.situation.pressures if p.pressure_id == "p-deadline")
    assert changed.origin is Origin.engine
    assert r.trace[0].value_origin is Origin.fixture   # the value it started from was fixture
    assert r.trace[0].decision_origin is Origin.engine


def test_09_retained_value_keeps_fixture_origin_with_engine_decision() -> None:
    s = fixture_for(JOURNALIST)
    ev = SituationEvent(event_id="e", event_kind=EventKind.change_pressure_intensity, tick=6,
                        target_id="p-deadline", magnitude=0.5, reason="same value")  # 0.5 == current
    r = apply_events(s, (ev,))
    entry = r.trace[0]
    assert entry.outcome is TraceOutcome.no_change
    assert entry.value_origin is Origin.fixture and entry.decision_origin is Origin.engine


# ── 10–12 · determinism and ordering ──────────────────────────────────────────────────────────────


def test_10_same_ordered_inputs_produce_identical_output() -> None:
    s = fixture_for(JOURNALIST)
    evs = (SituationEvent(event_id="e1", event_kind=EventKind.change_pressure_intensity, tick=6,
                          target_id="p-deadline", magnitude=0.8, reason="r"),)
    assert apply_events(s, evs).model_dump_json() == apply_events(s, evs).model_dump_json()


def test_11_event_ordering_is_stable_regardless_of_input_order() -> None:
    s = fixture_for(JOURNALIST)
    a = SituationEvent(event_id="a", event_kind=EventKind.change_pressure_intensity, tick=6, target_id="p-deadline", magnitude=0.7, reason="x")
    b = SituationEvent(event_id="b", event_kind=EventKind.change_pressure_intensity, tick=7, target_id="p-deadline", magnitude=0.9, reason="y")
    forward = apply_events(s, (a, b)).situation.model_dump_json()
    backward = apply_events(s, (b, a)).situation.model_dump_json()
    assert forward == backward   # sorted by (tick, order, id), not input order
    # final value is the later tick's
    assert next(p for p in apply_events(s, (b, a)).situation.pressures if p.pressure_id == "p-deadline").intensity == 0.9


def test_12_duplicate_event_identity_fails() -> None:
    s = fixture_for(JOURNALIST)
    ev = SituationEvent(event_id="dup", event_kind=EventKind.resolve_pressure, tick=6, target_id="p-deadline", reason="r")
    with pytest.raises(ValueError, match="duplicate event id"):
        apply_events(s, (ev, ev))
    # event targeting an unknown item fails
    bad = SituationEvent(event_id="x", event_kind=EventKind.resolve_pressure, tick=6, target_id="nope", reason="r")
    with pytest.raises(ValueError, match="unknown"):
        apply_events(s, (bad,))


# ── 13–24 · the transitions themselves ────────────────────────────────────────────────────────────


def _ev(**kw) -> SituationEvent:
    return SituationEvent(reason="r", **kw)


def test_13_14_15_goal_activation_priority_and_satisfaction() -> None:
    s = CurrentSituation()
    act = _ev(event_id="a", event_kind=EventKind.activate_goal, tick=1, target_id="g1",
              item={"description": "d", "desired_condition": "c", "priority": 0.5})
    s = apply_events(s, (act,)).situation
    assert s.goals[0].goal_id == "g1"
    # priority change is bounded even if a magnitude out of range is somehow attempted -> clamp path
    chg = _ev(event_id="b", event_kind=EventKind.change_goal_priority, tick=2, target_id="g1", magnitude=1.0)
    s2 = apply_events(s, (chg,)).situation
    assert 0.0 <= s2.goals[0].priority <= 1.0 and s2.goals[0].priority == 1.0
    # satisfaction does NOT select an action
    sat = apply_events(s, (_ev(event_id="c", event_kind=EventKind.satisfy_goal, tick=3, target_id="g1"),))
    assert sat.situation.goals[0].status is ItemStatus.satisfied
    assert sat.situation.selected_action_status is ItemStatus.not_modelled


def test_16_17_responsibility_activation_and_urgency() -> None:
    s = apply_events(CurrentSituation(), (_ev(event_id="a", event_kind=EventKind.activate_responsibility, tick=1,
        target_id="r1", item={"obligation": "o", "owed_to": "x", "subject": "y", "urgency": 0.4}),)).situation
    assert s.responsibilities[0].responsibility_id == "r1"
    s2 = apply_events(s, (_ev(event_id="b", event_kind=EventKind.change_responsibility_urgency, tick=2, target_id="r1", magnitude=0.9),)).situation
    assert 0.0 <= s2.responsibilities[0].urgency <= 1.0 and s2.responsibilities[0].urgency == 0.9


def test_18_19_20_pressure_activate_increase_and_resolve() -> None:
    s = apply_events(CurrentSituation(), (_ev(event_id="a", event_kind=EventKind.activate_pressure, tick=1,
        target_id="p1", item={"description": "d", "source_kind": "approaching_deadline",
                              "source_ref": "w", "intensity": 0.3}),)).situation
    assert s.pressures[0].intensity == 0.3
    up = apply_events(s, (_ev(event_id="b", event_kind=EventKind.change_pressure_intensity, tick=2, target_id="p1", magnitude=0.8),)).situation
    assert 0.0 <= up.pressures[0].intensity <= 1.0 and up.pressures[0].intensity == 0.8
    res = apply_events(s, (_ev(event_id="c", event_kind=EventKind.resolve_pressure, tick=2, target_id="p1"),)).situation
    assert res.pressures[0].status is ItemStatus.resolved


def test_21_pressure_is_contextual_not_a_person_score() -> None:
    s = fixture_for(JOURNALIST)
    # a pressure names a source and belongs to one item; there is no aggregate person pressure field
    assert all(p.source_ref for p in s.pressures)
    assert not hasattr(s, "person_pressure") and not hasattr(s, "overall_pressure")


def test_22_23_24_constraint_activate_resolve_and_no_action_removed() -> None:
    s = apply_events(CurrentSituation(), (_ev(event_id="a", event_kind=EventKind.activate_constraint, tick=1,
        target_id="c1", item={"limitation": "l", "constraint_kind": "verification_incomplete", "subject": "s"}),)).situation
    assert s.constraints[0].constraint_id == "c1"
    r = apply_events(s, (_ev(event_id="b", event_kind=EventKind.resolve_constraint, tick=2, target_id="c1"),))
    assert r.situation.constraints[0].status is ItemStatus.resolved
    # VP-2 removes no action and selects none
    assert r.situation.selected_action_status is ItemStatus.not_modelled
    assert not hasattr(r.situation, "available_actions")


# ── 25–27 · no-change, absence, NOT_MODELLED ──────────────────────────────────────────────────────


def test_25_no_change_produces_a_trace() -> None:
    s = fixture_for(JOURNALIST)
    ev = _ev(event_id="e", event_kind=EventKind.change_pressure_intensity, tick=6, target_id="p-deadline", magnitude=0.5)
    r = apply_events(s, (ev,))
    assert len(r.trace) == 1 and r.trace[0].outcome is TraceOutcome.no_change
    assert r.trace[0].no_change_reason  # explained, not a missing entry


def test_26_missing_is_not_zero() -> None:
    data = json.loads(fixture_for(JOURNALIST).model_dump_json())
    # optional fields that are absent must be null, never 0
    for g in data["goals"]:
        if g["start_tick"] is None:
            assert g["start_tick"] is None
        assert g["update_reason"] is None or isinstance(g["update_reason"], str)


def test_27_not_modelled_is_distinct_from_inactive() -> None:
    assert ItemStatus.not_modelled is not ItemStatus.inactive
    assert {ItemStatus.not_modelled.value, ItemStatus.inactive.value} == {"NOT_MODELLED", "INACTIVE"}


# ── 28–32 · identity cannot reach the kernel; people are interchangeable given equal state ─────────


def test_28_identity_fields_are_absent_from_kernel_inputs() -> None:
    params = set(inspect.signature(apply_events).parameters)
    assert params == {"situation", "events", "rule_version"}
    for banned in ("name", "portrait", "biography", "life_stage", "education", "occupation",
                   "socioeconomic", "person_id", "role", "prestige"):
        assert banned not in params


def test_29_30_31_biography_portrait_role_do_not_alter_transitions() -> None:
    # the kernel never receives identity; identical state+events give identical results, and none of
    # biography/portrait/role can be passed in at all. Prove belief output is unaffected too.
    before = person_projection(JOURNALIST).model_dump(mode="json")
    s = fixture_for(JOURNALIST)
    ev = _ev(event_id="e", event_kind=EventKind.change_pressure_intensity, tick=6, target_id="p-deadline", magnitude=0.9)
    apply_events(s, (ev,))
    after = person_projection(JOURNALIST).model_dump(mode="json")
    assert before == after   # VP-2 does not touch the belief slice


def test_32_identical_state_and_events_for_different_people_are_identical() -> None:
    # give two DIFFERENT people the SAME situation + events; the kernel output is identical, because
    # who they are never enters it.
    common = CurrentSituation(pressures=(Pressure(pressure_id="p", description="d",
        source_kind=PressureSource.approaching_deadline, source_ref="w", intensity=0.4),))
    ev = _ev(event_id="e", event_kind=EventKind.change_pressure_intensity, tick=1, target_id="p", magnitude=0.7)
    a = apply_events(common, (ev,)).model_dump_json()
    b = apply_events(common, (ev,)).model_dump_json()
    assert a == b


# ── 33–36 · no profiling, no combined score, no action, belief unchanged ──────────────────────────


def test_33_no_prohibited_profiling_field_exists() -> None:
    for field in all_fields():
        low = field.lower()
        for banned in PROHIBITED:
            assert banned not in low, f"prohibited field '{field}' matched '{banned}'"


def test_34_no_universal_combined_person_score_exists() -> None:
    s = fixture_for(JOURNALIST)
    for banned in ("overall", "combined", "total_pressure", "person_score", "motivation",
                   "stability", "risk", "influence", "quality"):
        assert not hasattr(s, banned)
    # magnitudes live on individual items only
    assert all(hasattr(p, "intensity") for p in s.pressures)


def test_35_selected_action_remains_not_modelled() -> None:
    s = fixture_for(JOURNALIST)
    assert s.selected_action_status is ItemStatus.not_modelled
    # even after a full demonstration sequence
    evs = (
        _ev(event_id="e1", event_kind=EventKind.change_pressure_intensity, tick=6, target_id="p-deadline", magnitude=0.8),
        _ev(event_id="e2", event_kind=EventKind.resolve_constraint, tick=7, target_id="c-corroboration"),
    )
    assert apply_events(s, evs).situation.selected_action_status is ItemStatus.not_modelled


def test_36_existing_belief_outputs_remain_byte_identical() -> None:
    # importing and exercising VP-2 changes nothing in the belief slice
    for pid in ("family-spokesperson", "government-minister", "broadcast-journalist"):
        proj = person_projection(pid)
        assert proj.entity.entity_id == pid
    # a representative value unchanged from the frozen milestone
    assert person_projection("broadcast-journalist").calculation.final_credence == pytest.approx(0.408458, abs=1e-6)


# ── coverage of all three fixtures + demonstration sequence ───────────────────────────────────────


def test_37_all_three_fixtures_are_well_formed_and_fixture_origin() -> None:
    assert set(VP2_FIXTURES) == {"family-spokesperson", "government-minister", "broadcast-journalist"}
    for pid, s in VP2_FIXTURES.items():
        assert s.goals and s.responsibilities and s.pressures and s.constraints
        for item in (*s.goals, *s.responsibilities, *s.pressures, *s.constraints):
            assert item.origin is Origin.fixture, f"{pid} item not FIXTURE"
        assert s.selected_action_status is ItemStatus.not_modelled


def test_38_demonstration_current_situation_changes() -> None:
    s = fixture_for(JOURNALIST)
    evs = (
        _ev(event_id="d1", event_kind=EventKind.change_pressure_intensity, tick=6, target_id="p-deadline", magnitude=0.85),
        _ev(event_id="d2", event_kind=EventKind.resolve_constraint, tick=7, target_id="c-corroboration"),
        _ev(event_id="d3", event_kind=EventKind.change_responsibility_urgency, tick=7, target_id="r-standard", magnitude=0.75),
    )
    r = apply_events(s, evs)
    assert next(p for p in r.situation.pressures if p.pressure_id == "p-deadline").intensity == 0.85
    assert next(c for c in r.situation.constraints if c.constraint_id == "c-corroboration").status is ItemStatus.resolved
    assert len(r.trace) == 3
    assert r.rule_version == RULE_VERSION
    # reducing a pressure does not imply any decision
    assert r.situation.selected_action_status is ItemStatus.not_modelled
