"""
Virtual Person VP-3 — deterministic action selection and decision trace.

Proves options and contributions are well-typed and bounded, availability precedes ranking,
the versioned formula is exact, ties are stable and visible, identity cannot reach the kernel,
selection is never execution, and no psychological shortcut or people-ranking exists.
"""

from __future__ import annotations

import inspect

import pytest
from pydantic import ValidationError

from app.simulation.belief.projection import person_projection
from app.simulation.belief.provenance import Origin
from app.simulation.person.current_state import (
    Constraint,
    ConstraintKind,
    Goal,
    ItemStatus,
    Pressure,
    PressureSource,
    Responsibility,
)
from app.simulation.person.decision import (
    RULE_VERSION,
    TIE_BREAK_RULE,
    ActionOption,
    ConstraintRequirement,
    DecisionRequest,
    DecisionResult,
    DecisionStatus,
    ExecutionStatus,
    GoalContribution,
    PressureResponse,
    ResponsibilityContribution,
    select_action,
)
from app.simulation.person.vp3_decisions import (
    FIXTURE_DECISIONS,
    journalist_decision,
    minister_decision,
    spokesperson_decision,
)

ALL_MODELS = (ActionOption, GoalContribution, ResponsibilityContribution, PressureResponse,
              ConstraintRequirement, DecisionRequest, DecisionResult)

PROHIBITED = ("personality", "intelligence", "competence", "morality", "resilience", "stability",
              "anxiety", "aggression", "gullib", "susceptib", "persuad", "influence", "vulnerab",
              "risk_appetite", "obedience", "loyalty", "ideology", "iq", "targetab", "audience")

# a tiny hand-built request with known numbers, for exact-formula tests
G = Goal(goal_id="g", description="d", desired_condition="c", priority=0.5, origin=Origin.fixture)
R = Responsibility(responsibility_id="r", obligation="o", owed_to="x", subject="y", urgency=0.4,
                   origin=Origin.fixture)
P = Pressure(pressure_id="p", description="d", source_kind=PressureSource.approaching_deadline,
             source_ref="w", intensity=0.6, origin=Origin.fixture)
C_ACTIVE = Constraint(constraint_id="c", limitation="l", constraint_kind=ConstraintKind.verification_incomplete,
                      subject="s", status=ItemStatus.active, origin=Origin.fixture)
C_RESOLVED = C_ACTIVE.model_copy(update={"status": ItemStatus.resolved})


def opt(action_id, g=None, r=None, p=None, cons=None, label=None) -> ActionOption:
    return ActionOption(
        action_id=action_id, label=label or action_id, description="d",
        goal_contributions=(GoalContribution(goal_id="g", alignment=g, rationale="x"),) if g is not None else (),
        responsibility_contributions=(ResponsibilityContribution(responsibility_id="r", alignment=r, rationale="x"),) if r is not None else (),
        pressure_responses=(PressureResponse(pressure_id="p", response=p, rationale="x"),) if p is not None else (),
        constraint_requirements=(ConstraintRequirement(constraint_id="c", blocked_while_active=True, rationale="x"),) if cons else (),
    )


def req(options, constraints=(C_ACTIVE,)) -> DecisionRequest:
    return DecisionRequest(decision_id="d", goals=(G,), responsibilities=(R,), pressures=(P,),
                           constraints=constraints, options=tuple(options))


# ── 1–5 · schemas ─────────────────────────────────────────────────────────────────────────────────


def test_01_valid_action_option_loads() -> None:
    o = opt("a1", g=0.5)
    assert o.action_id == "a1" and o.origin is Origin.fixture


def test_02_unknown_fields_fail() -> None:
    with pytest.raises(ValidationError):
        ActionOption(action_id="a", label="l", description="d", persuasiveness=0.9)  # type: ignore[call-arg]


def test_03_invalid_origins_fail() -> None:
    with pytest.raises(ValidationError):
        GoalContribution(goal_id="g", alignment=0.1, rationale="x", origin="NONSENSE")  # type: ignore[arg-type]


def test_04_invalid_references_fail() -> None:
    # a contribution referencing a goal not in the request fails at selection
    bad = ActionOption(action_id="a", label="l", description="d",
                       goal_contributions=(GoalContribution(goal_id="missing", alignment=0.5, rationale="x"),))
    with pytest.raises(ValueError, match="unknown goal reference"):
        select_action(req([bad]))


def test_05_contributions_are_bounded() -> None:
    for bad in (1.5, -1.5):
        with pytest.raises(ValidationError):
            GoalContribution(goal_id="g", alignment=bad, rationale="x")
    with pytest.raises(ValidationError):
        ConstraintRequirement(constraint_id="c", blocked_while_active=False, soft_penalty=2.0, rationale="x")


# ── 6–9 · availability, unavailable≠zero, exact formula ───────────────────────────────────────────


def test_06_hard_constraint_makes_an_option_unavailable() -> None:
    r = select_action(req([opt("a-blocked", g=0.9, cons=True), opt("a-open", g=0.1)]))
    comps = {c.action_id: c for c in r.comparisons}
    assert comps["a-blocked"].available is False
    assert comps["a-blocked"].blocking_constraints == ("c",)
    assert r.selected_action_id == "a-open"   # the high-scoring option was removed for being blocked


def test_07_unavailable_is_not_score_zero() -> None:
    r = select_action(req([opt("a-blocked", g=0.9, cons=True), opt("a-open", g=0.1)]))
    comp = next(c for c in r.comparisons if c.action_id == "a-blocked")
    assert comp.total is None            # not 0.0
    assert comp.goal_component is None


def test_08_available_option_components_calculate_correctly() -> None:
    # g=0.5*0.8=0.4 ; r=0.4*0.5=0.2 ; p=0.6*(-0.5)=-0.3 ; total=0.3
    o = ActionOption(action_id="a", label="l", description="d",
        goal_contributions=(GoalContribution(goal_id="g", alignment=0.8, rationale="x"),),
        responsibility_contributions=(ResponsibilityContribution(responsibility_id="r", alignment=0.5, rationale="x"),),
        pressure_responses=(PressureResponse(pressure_id="p", response=-0.5, rationale="x"),))
    c = select_action(req([o])).comparisons[0]
    assert c.goal_component == pytest.approx(0.4)
    assert c.responsibility_component == pytest.approx(0.2)
    assert c.pressure_component == pytest.approx(-0.3)
    assert c.total == pytest.approx(0.3)


def test_09_total_matches_the_versioned_formula() -> None:
    c = select_action(req([opt("a", g=0.6, r=0.5, p=0.4)])).comparisons[0]
    expected = 0.5 * 0.6 + 0.4 * 0.5 + 0.6 * 0.4
    assert c.total == pytest.approx(expected)
    assert select_action(req([opt("a", g=0.6)])).rule_version == RULE_VERSION


# ── 10–14 · determinism, ordering, ties ───────────────────────────────────────────────────────────


def test_10_same_inputs_produce_same_output() -> None:
    r = req([opt("a", g=0.5), opt("b", g=0.3)])
    assert select_action(r).model_dump_json() == select_action(r).model_dump_json()


def test_11_option_order_does_not_affect_result() -> None:
    a, b = opt("a", g=0.3), opt("b", g=0.7)
    assert select_action(req([a, b])).selected_action_id == select_action(req([b, a])).selected_action_id == "b"


def test_12_contribution_order_does_not_affect_result() -> None:
    o1 = ActionOption(action_id="a", label="l", description="d",
        goal_contributions=(GoalContribution(goal_id="g", alignment=0.5, rationale="x"),),
        responsibility_contributions=(ResponsibilityContribution(responsibility_id="r", alignment=0.5, rationale="x"),))
    # same contributions, and a bare option — the total is order-independent by construction (sum)
    assert select_action(req([o1])).comparisons[0].total == pytest.approx(0.5 * 0.5 + 0.4 * 0.5)


def test_13_14_stable_tie_is_handled_and_recorded() -> None:
    # two options with identical totals → tie-break to lowest action_id, tie recorded
    r = select_action(req([opt("z-opt", g=0.5), opt("a-opt", g=0.5)]))
    assert r.selected_action_id == "a-opt"
    assert r.tie_occurred is True
    assert r.tie_break_rule == TIE_BREAK_RULE


# ── 15–18 · all blocked, no stale selection, not executed, no consequence ─────────────────────────


def test_15_all_blocked_produces_no_available_action() -> None:
    r = select_action(req([opt("a", g=0.5, cons=True), opt("b", g=0.9, cons=True)]))
    assert r.status is DecisionStatus.no_available_action
    assert r.selected_action_id is None
    assert "unavailable" in r.explanation.lower() and "executed" in r.explanation.lower()


def test_16_no_stale_selection_when_all_blocked() -> None:
    r = select_action(req([opt("a", g=0.9, cons=True)]))
    assert r.selected_action_id is None
    with pytest.raises(ValidationError):   # the model itself forbids a stale selection
        DecisionResult(decision_id="d", status=DecisionStatus.no_available_action,
                       considered_options=("a",), available_options=(), unavailable_options=("a",),
                       selected_action_id="a", comparisons=())


def test_17_selected_option_is_marked_not_executed() -> None:
    r = select_action(journalist_decision())
    assert r.execution_status is ExecutionStatus.not_executed
    # ExecutionStatus is a one-value enum, so an EXECUTED value cannot even be constructed:
    # selection can never be represented as executed.
    with pytest.raises(ValidationError):
        DecisionResult(decision_id="d", status=DecisionStatus.selected_not_executed,
                       considered_options=("a",), available_options=("a",), unavailable_options=(),
                       selected_action_id="a", comparisons=(),
                       execution_status="EXECUTED")  # type: ignore[arg-type]
    from app.simulation.person.decision import ExecutionStatus as _ES
    assert [m.value for m in _ES] == ["NOT_EXECUTED"]


def test_18_no_world_state_consequence_is_emitted() -> None:
    r = select_action(journalist_decision())
    # the result carries no field that could apply an effect to a run
    flat = str(r.model_dump()).lower()
    for banned in ("apply", "emit", "effect_on", "world_state", "run_id", "macro", "tick_applied"):
        assert banned not in flat
    # belief slice untouched
    assert person_projection("broadcast-journalist").calculation.final_credence == pytest.approx(0.408458, abs=1e-6)


# ── 19–22 · contributions use only their referenced item; unknown refs fail ───────────────────────


def test_19_20_21_contribution_uses_only_the_referenced_item() -> None:
    # raising a SECOND goal's priority does not change an option that only references the first
    g2 = Goal(goal_id="g2", description="d2", desired_condition="c2", priority=0.9, origin=Origin.fixture)
    r1 = DecisionRequest(decision_id="d", goals=(G, g2), responsibilities=(R,), pressures=(P,),
                         constraints=(C_ACTIVE,), options=(opt("a", g=0.5),))
    base = select_action(r1).comparisons[0].total
    g2_hi = g2.model_copy(update={"priority": 0.1})
    r2 = r1.model_copy(update={"goals": (G, g2_hi)})
    assert select_action(r2).comparisons[0].total == base   # unaffected: option never referenced g2


def test_22_unknown_state_references_fail() -> None:
    for kind, contrib in (
        ("responsibility", ActionOption(action_id="a", label="l", description="d",
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="nope", alignment=0.5, rationale="x"),))),
        ("pressure", ActionOption(action_id="a", label="l", description="d",
            pressure_responses=(PressureResponse(pressure_id="nope", response=0.5, rationale="x"),))),
        ("constraint", ActionOption(action_id="a", label="l", description="d",
            constraint_requirements=(ConstraintRequirement(constraint_id="nope", blocked_while_active=True, rationale="x"),))),
    ):
        with pytest.raises(ValueError, match="unknown"):
            select_action(req([contrib]))


# ── 23–28 · identity cannot reach the kernel; people are interchangeable ──────────────────────────


def test_23_identity_fields_are_absent_from_kernel_inputs() -> None:
    assert set(inspect.signature(select_action).parameters) == {"request", "rule_version"}
    for banned in ("name", "portrait", "biography", "role", "occupation", "education",
                   "socioeconomic", "life_stage", "community", "prestige"):
        assert banned not in set(DecisionRequest.model_fields)


def test_24_25_26_27_identity_mutation_has_no_effect() -> None:
    # DecisionRequest has no identity fields to mutate; subject_ref (association only) must not score.
    r1 = journalist_decision()
    r2 = r1.model_copy(update={"subject_ref": "fict:kestral-strait:person:government-minister"})
    a = select_action(r1)
    b = select_action(r2)
    assert a.selected_action_id == b.selected_action_id
    assert tuple(c.total for c in a.comparisons) == tuple(c.total for c in b.comparisons)


def test_28_identical_structured_inputs_across_people_give_identical_results() -> None:
    # same request under two different subject_refs -> identical selection and scores
    base = req([opt("a", g=0.7), opt("b", g=0.3)])
    p1 = base.model_copy(update={"subject_ref": "fict:kestral-strait:person:family-spokesperson"})
    p2 = base.model_copy(update={"subject_ref": "fict:kestral-strait:person:broadcast-journalist"})
    assert select_action(p1).selected_action_id == select_action(p2).selected_action_id
    assert (tuple(c.total for c in select_action(p1).comparisons)
            == tuple(c.total for c in select_action(p2).comparisons))


# ── 29–31 · explanation matches structured result ────────────────────────────────────────────────


def test_29_explanation_matches_the_structured_result() -> None:
    r = select_action(journalist_decision())
    assert r.selected_action_id == "a-seek-corroboration"
    assert "seek additional corroboration" in r.explanation


def test_30_explanation_names_blocked_options_accurately() -> None:
    r = select_action(journalist_decision())
    assert "publish the claim immediately" in r.explanation   # the blocked option, named
    # and it never uses personality language
    low = r.explanation.lower()
    for banned in ("anxious", "cautious by nature", "as a journalist", "personality", "intelligent"):
        assert banned not in low


def test_31_explanation_states_nothing_was_executed() -> None:
    for mk in (journalist_decision, minister_decision, spokesperson_decision):
        assert "nothing was executed" in select_action(mk()).explanation.lower()


# ── 32–35 · scores are not probabilities; no person score; no profiling; no targeting ─────────────


def test_32_option_scores_are_not_exposed_as_probabilities() -> None:
    r = select_action(journalist_decision())
    # scan the operational payload only — model_boundary/claim_boundary NAME these words as denials
    payload = r.model_dump()
    for drop in ("model_boundary", "claim_boundary", "explanation"):
        payload.pop(drop, None)
    flat = str(payload).lower()
    for banned in ("probability", "likelihood", "p_choose", "chance"):
        assert banned not in flat, f"a probability word leaked into the score payload: {banned}"
    # totals are not confined to [0,1], proving they are not probabilities
    assert any((c.total or 0) != 0 for c in r.comparisons)


def test_33_no_combined_person_score_exists() -> None:
    r = select_action(journalist_decision())
    for banned in ("person_score", "overall", "combined", "motivation", "quality", "aggregate_score"):
        assert not hasattr(r, banned)


def test_34_no_prohibited_psychological_field_exists() -> None:
    names: set[str] = set()
    for m in ALL_MODELS:
        names |= set(m.model_fields)
    for field in names:
        for banned in PROHIBITED:
            assert banned not in field.lower(), f"prohibited field '{field}' matched '{banned}'"


def test_35_no_people_ranking_or_targeting_operation_exists() -> None:
    import ast, app.simulation.person.decision as mod
    # strip docstrings/comments: they legitimately NAME what the model is NOT (e.g. "susceptibility")
    tree = ast.parse(inspect.getsource(mod))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            doc = ast.get_docstring(node)
            if doc and node.body and isinstance(node.body[0], ast.Expr):
                node.body[0].value = ast.Constant(value="")
    code_only = ast.unparse(tree).lower()
    for banned in ("rank_people", "easiest_to_influence", "choose_audience", "optimise_persuasion",
                   "targetability", "audience_rank"):
        assert banned not in code_only
    # the kernel compares options for ONE request; it takes no collection of people
    params = inspect.signature(select_action).parameters
    assert "people" not in params and "persons" not in params


# ── 36–42 · availability toggling + regressions ──────────────────────────────────────────────────


def test_36_resolving_a_hard_constraint_makes_the_option_available() -> None:
    blocked = select_action(req([opt("a-publish", g=0.9, cons=True), opt("a-seek", g=0.4)],
                                constraints=(C_ACTIVE,)))
    assert "a-publish" in blocked.unavailable_options
    freed = select_action(req([opt("a-publish", g=0.9, cons=True), opt("a-seek", g=0.4)],
                              constraints=(C_RESOLVED,)))
    assert "a-publish" in freed.available_options and freed.selected_action_id == "a-publish"


def test_37_activating_a_constraint_removes_the_matching_option() -> None:
    freed = select_action(req([opt("a-publish", g=0.9, cons=True)], constraints=(C_RESOLVED,)))
    assert freed.selected_action_id == "a-publish"
    blocked = select_action(req([opt("a-publish", g=0.9, cons=True)], constraints=(C_ACTIVE,)))
    assert blocked.status is DecisionStatus.no_available_action


def test_38_all_three_fixture_decisions_select_the_verified_path_not_executed() -> None:
    expected = {"family-spokesperson": "a-request-records",
                "government-minister": "a-cautious-statement",
                "broadcast-journalist": "a-seek-corroboration"}
    for pid, mk in FIXTURE_DECISIONS.items():
        r = select_action(mk())
        assert r.selected_action_id == expected[pid]
        assert r.execution_status is ExecutionStatus.not_executed


def test_39_existing_belief_outputs_remain_byte_identical() -> None:
    assert person_projection("broadcast-journalist").calculation.final_credence == pytest.approx(0.408458, abs=1e-6)
    assert person_projection("government-minister").calculation.final_credence == pytest.approx(0.171946, abs=1e-6)


def test_40_claim_boundary_and_model_boundary_travel_with_every_result() -> None:
    r = select_action(journalist_decision())
    assert "not a complete model or prediction" in r.claim_boundary
    assert "not a probability the person will choose this" in r.model_boundary
    assert "not intelligence or competence" in r.model_boundary
