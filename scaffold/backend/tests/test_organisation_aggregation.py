"""
Organisation aggregation — a collective actor, not a person with one mind.

The twenty required proofs, including the one that matters most: the official position is NOT the
weighted mean. The broadcaster is the demonstration — its mean reads as leaning supportive while
half the body is undecided, and the governance rule correctly withholds a position.
"""

from __future__ import annotations

import ast
import inspect
import io
import tokenize

import pytest

from app.simulation.belief import cast
from app.simulation.belief import organisations as orgmod
from app.simulation.belief.organisations import (
    FIRM_POSITION_COHESION,
    OfficialPosition,
    OrganisationInput,
    OrganisationResult,
    PositionStrength,
    aggregate,
)

ORG_IDS = ["national-government", "public-broadcaster", "coastal-workers-union"]
EV = cast.SHARED_EVENT
EXPOSURE = {e["entity_id"]: e for e in cast.EXPOSURES}


def weight(oid: str) -> float:
    e = EXPOSURE[oid]
    return (
        e["intensity"] * e["relay"]
        * cast.SOURCE_TRUST[oid][EV["source_category"]]
        * EV["evidence_strength"] * cast.RELEVANCE[oid]
    )


def build(oid: str, **over) -> OrganisationInput:
    o = next(x for x in cast.ORGANISATIONS if x["organisation_id"] == oid)
    base = dict(
        internal_blocs=dict(o["internal_blocs"]),
        cohesion=o["cohesion"],
        prior_alignment=o["official_alignment"],
        update_weight=weight(oid),
        target_alignment=1.0,
        objectives=tuple(o["objectives"]),
    )
    base.update(over)
    return OrganisationInput(**base)


def run(oid: str, **over) -> OrganisationResult:
    return aggregate(build(oid, **over))


def executable_source(module) -> str:
    src = inspect.getsource(module)
    toks = [t for t in tokenize.generate_tokens(io.StringIO(src).readline)
            if t.type != tokenize.COMMENT]
    tree = ast.parse(tokenize.untokenize(toks))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            b = node.body
            if (b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant)
                    and isinstance(b[0].value.value, str)):
                b.pop(0)
    return ast.unparse(tree)


def test_01_all_three_organisations_produce_structured_results() -> None:
    for oid in ORG_IDS:
        r = run(oid)
        assert r.status == "AGGREGATED"
        assert r.official_position is not None
        assert r.position_strength is not None
        assert r.governance_rule
        assert r.objectives
        assert r.explanation["rule_version"] == "org-aggregate-v1"


def test_02_internal_distributions_reconcile() -> None:
    for oid in ORG_IDS:
        assert sum(run(oid).internal_distribution.values()) == pytest.approx(1.0, abs=1e-6)


def test_03_official_alignment_is_bounded() -> None:
    for oid in ORG_IDS:
        for w in (0.0, 0.5, 1.0):
            r = run(oid, update_weight=w)
            assert 0.0 <= r.resulting_alignment <= 1.0


def test_04_action_propensity_is_bounded() -> None:
    for oid in ORG_IDS:
        for w in (0.0, 1.0):
            assert 0.0 <= run(oid, update_weight=w).action_propensity <= 1.0


def test_05_identical_inputs_give_identical_outputs() -> None:
    common = dict(internal_blocs={"support": 0.6, "oppose": 0.2, "uncertain": 0.2},
                  cohesion=0.7, prior_alignment=0.4, update_weight=0.2)
    outs = [run(o, **common) for o in ORG_IDS]
    assert len({r.resulting_alignment for r in outs}) == 1
    assert len({r.official_position for r in outs}) == 1


def test_06_07_organisation_id_and_display_name_do_not_affect_calculation() -> None:
    """Identity reaches the calculation nowhere — OrganisationInput has no id or name field."""
    fields = set(OrganisationInput.__dataclass_fields__)
    for forbidden in ("organisation_id", "id", "display_name", "name", "bio", "type"):
        assert forbidden not in fields
    a = aggregate(build("national-government"))
    b = aggregate(build("national-government"))
    assert a == b


def test_08_reordering_internal_blocs_gives_the_same_result() -> None:
    o = next(x for x in cast.ORGANISATIONS if x["organisation_id"] == "public-broadcaster")
    forward = run("public-broadcaster", internal_blocs=dict(o["internal_blocs"]))
    reversed_blocs = dict(reversed(list(o["internal_blocs"].items())))
    backward = run("public-broadcaster", internal_blocs=reversed_blocs)
    assert forward.official_position == backward.official_position
    assert forward.resulting_alignment == backward.resulting_alignment
    assert forward.action_propensity == backward.action_propensity


def test_09_10_cohesion_moves_position_strength_monotonically() -> None:
    blocs = {"support": 0.6, "oppose": 0.2, "uncertain": 0.2}
    propensities = [
        run("national-government", internal_blocs=blocs, cohesion=c).action_propensity
        for c in (0.2, 0.4, 0.6, 0.8, 1.0)
    ]
    assert propensities == sorted(propensities), "higher cohesion did not strengthen capacity to act"

    low = run("national-government", internal_blocs=blocs, cohesion=0.3)
    high = run("national-government", internal_blocs=blocs, cohesion=0.9)
    assert low.position_strength is PositionStrength.qualified
    assert high.position_strength is PositionStrength.firm
    assert low.action_propensity < high.action_propensity


def test_11_large_uncertain_bloc_constrains_a_firm_position() -> None:
    """
    The broadcaster case, reached through the generic rule with no special-casing: half the body is
    undecided, so no position is available to assert however the rest leans.
    """
    r = run("public-broadcaster")
    assert r.internal_distribution["uncertain"] == 0.50
    assert r.cohesion == 0.55
    assert r.official_position is OfficialPosition.uncertain
    assert r.position_strength is PositionStrength.withheld
    assert r.action_propensity == 0.0

    # Shrink the uncertain bloc and a position becomes available — the constraint is the bloc,
    # not the organisation.
    decided = run("public-broadcaster",
                  internal_blocs={"support": 0.6, "oppose": 0.2, "uncertain": 0.2},
                  cohesion=0.75)
    assert decided.official_position is OfficialPosition.support
    assert decided.position_strength is PositionStrength.firm


def test_12_official_position_is_not_the_weighted_mean() -> None:
    """
    The decisive test. The broadcaster's weighted mean is 0.55 — above the midpoint, so a mean-based
    reading would call it leaning SUPPORT. The governance rule says UNCERTAIN/WITHHELD, because a
    body that is half undecided has no position to assert. Those disagree, which is the point.
    """
    r = run("public-broadcaster")
    mean = r.explanation["weighted_mean_for_comparison"]
    assert mean == pytest.approx(0.55, abs=1e-9)
    assert mean > 0.5, "precondition: the mean reads as leaning supportive"
    assert r.official_position is not OfficialPosition.support
    assert r.official_position is OfficialPosition.uncertain
    assert r.explanation["official_position_equals_weighted_mean"] is False

    # And the alignment number is not the mean either.
    for oid in ORG_IDS:
        res = run(oid)
        assert res.resulting_alignment != pytest.approx(
            res.explanation["weighted_mean_for_comparison"], abs=1e-9
        )


def test_13_missing_internal_distribution_is_unavailable_not_zero() -> None:
    r = run("national-government", internal_blocs=None)
    assert r.status == "UNAVAILABLE"
    assert r.official_position is None
    assert r.resulting_alignment is None
    assert r.action_propensity is None
    assert r.action_propensity != 0.0
    assert "internal_blocs" in r.unavailable_reason


def test_14_missing_cohesion_is_unavailable_not_defaulted() -> None:
    r = run("national-government", cohesion=None)
    assert r.status == "UNAVAILABLE"
    assert r.cohesion is None
    assert r.resulting_alignment is None
    assert "cohesion" in r.unavailable_reason


def test_15_16_17_no_emotion_credence_or_capability_field() -> None:
    result_fields = set(OrganisationResult.__dataclass_fields__)
    input_fields = set(OrganisationInput.__dataclass_fields__)
    for banned in ("emotion", "mood", "personality", "memory", "credence", "belief",
                   "intelligence", "competence", "susceptibility", "persuadability",
                   "gullibility", "education", "wealth"):
        assert not any(banned in f for f in result_fields), f"result carries '{banned}'"
        assert not any(banned in f for f in input_fields), f"input accepts '{banned}'"

    from app.simulation.belief.schemas import EmotionalState, MessageTarget

    org = MessageTarget(scenario_id=cast.SCENARIO_ID, kind="organisation",
                        entity_id="national-government")
    with pytest.raises(Exception):
        EmotionalState(holder=org, values={})


def test_18_registry_order_does_not_affect_results() -> None:
    forward = {o: run(o).resulting_alignment for o in ORG_IDS}
    backward = {o: run(o).resulting_alignment for o in reversed(ORG_IDS)}
    assert forward == backward


def test_19_no_organisation_specific_branch_in_executable_code() -> None:
    src = executable_source(orgmod).lower()
    for oid in ORG_IDS:
        assert oid not in src
    for word in ("government", "broadcaster", "union", "ministry"):
        assert word not in src, f"aggregation branches on '{word}'"


def test_20_explanation_contains_the_required_derivations() -> None:
    for oid in ORG_IDS:
        e = run(oid).explanation
        for key in ("prior_alignment", "target_alignment", "update_weight", "cohesion",
                    "cohesion_contribution", "delta_alignment", "resulting_alignment",
                    "internal_distribution", "governance_rule", "position_derivation",
                    "action_propensity_derivation", "objectives"):
            assert key in e, f"{oid} explanation missing {key}"
        # Biography must never enter a calculation explanation.
        flat = " ".join(str(v) for v in e.values()).lower()
        for record in cast.DESCRIPTIVE.values():
            for text in record.values():
                assert text.lower() not in flat


def test_21_unexposed_organisation_holds_its_distribution_without_moving() -> None:
    r = run("national-government", update_weight=None)
    assert r.delta_alignment == 0.0
    assert r.resulting_alignment == r.prior_alignment
    assert r.official_position is not None


def test_22_non_reconciling_distribution_is_refused() -> None:
    with pytest.raises(ValueError, match="sum to 1.0"):
        run("national-government", internal_blocs={"support": 0.5, "oppose": 0.2, "uncertain": 0.1})
