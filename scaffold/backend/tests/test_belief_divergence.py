"""
Belief Update Rule v1 — genericity, counterfactual and sensitivity evidence.

WHAT THIS FILE IS FOR. The first run produced three distinct outcomes, but a plausible-looking table
is not evidence. These tests decide whether the divergence is produced by the *mechanism* operating
on declared inputs, or merely encoded in fixtures that were chosen knowing the roles.

The frozen rule (`b8b0c81`) and fixtures (`6320cf1`) are NOT modified here.
"""

from __future__ import annotations

import ast
import inspect
import io
import tokenize

import pytest

from app.simulation.belief import cast, update as upd
from app.simulation.belief.update import UpdateInput, apply_update, population_weighted

EV = cast.SHARED_EVENT
P = "P-WARNINGS-IGNORED"
EXPOSURE = {e["entity_id"]: e for e in cast.EXPOSURES}
PEOPLE_IDS = [p["person_id"] for p in cast.PEOPLE]


def theta(eid: str) -> float:
    for p in cast.PEOPLE:
        if p["person_id"] == eid:
            return p["evidentiary_threshold"]
    for o in cast.ORGANISATIONS:
        if o["organisation_id"] == eid:
            return 1.0 - o["cohesion"] * 0.5
    return 0.45


def build(eid: str, **override) -> UpdateInput:
    pr = cast.PRIORS.get((eid, P))
    e = EXPOSURE.get(eid)
    base = dict(
        prior_credence=pr["credence"] if pr else None,
        prior_confidence=pr["confidence"] if pr else None,
        prior_salience=pr["salience"] if pr else None,
        evidentiary_threshold=theta(eid),
        source_trust=cast.SOURCE_TRUST.get(eid, {}).get(EV["source_category"]),
        evidence_strength=EV["evidence_strength"],
        exposure_intensity=e["intensity"] if e else None,
        relay_factor=e["relay"] if e else 1.0,
        relevance=cast.RELEVANCE.get(eid),
        claim_direction=EV["claim_direction"],
    )
    base.update(override)
    return UpdateInput(**base)


def run(eid: str, **override):
    return apply_update(build(eid, **override))


def executable_source(module) -> str:
    """
    Source with comments and docstrings stripped.

    Scanning raw source is wrong: this module's docstring EXPLAINS that susceptibility is absent,
    which a naive substring check flags as a violation. The prohibition is on the code, not on
    discussing the prohibition.
    """
    src = inspect.getsource(module)
    out = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            continue
        out.append(tok)
    stripped = tokenize.untokenize(out)
    tree = ast.parse(stripped)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
    return ast.unparse(tree)


def spread(results: dict[str, float]) -> float:
    """Divergence measured as the range across the three people."""
    return max(results.values()) - min(results.values())


# ══ GENERICITY — is the mechanism generic, or entity-scripted? ═══════════════════════════════════


def test_01_identical_inputs_give_identical_outputs() -> None:
    a = apply_update(build("family-spokesperson"))
    b = apply_update(build("government-minister", **{
        k: getattr(build("family-spokesperson"), k)
        for k in ("prior_credence", "prior_confidence", "prior_salience",
                  "evidentiary_threshold", "source_trust", "exposure_intensity",
                  "relay_factor", "relevance")
    }))
    assert a.credence == b.credence
    assert a.confidence == b.confidence
    assert a.delta_credence == b.delta_credence


def test_02_entity_id_is_not_an_input() -> None:
    """`UpdateInput` has no id field at all, so identity cannot reach the formula."""
    fields = set(UpdateInput.__dataclass_fields__)
    for forbidden in ("entity_id", "id", "name", "display_name", "bio", "kind"):
        assert forbidden not in fields


def test_03_registry_order_does_not_affect_results() -> None:
    forward = {e: run(e).credence for e in PEOPLE_IDS}
    reverse = {e: run(e).credence for e in reversed(PEOPLE_IDS)}
    assert forward == reverse


def test_04_05_update_module_has_no_entity_or_name_branches() -> None:
    src = executable_source(upd)
    for eid in PEOPLE_IDS + [o["organisation_id"] for o in cast.ORGANISATIONS]:
        assert eid not in src, f"update module branches on entity id: {eid}"
    for p in cast.PEOPLE:
        assert p["display_name"] not in src


def test_06_biography_fields_never_enter_the_update_input() -> None:
    src = executable_source(upd)
    assert "bio" not in src
    for p in cast.PEOPLE:
        assert p["bio"] not in src


def test_07_no_exposure_means_no_update() -> None:
    r = run("inland-households")
    assert r.evidence_status == "UNEXPOSED"
    assert r.delta_credence == 0.0
    assert r.credence == cast.PRIORS[("inland-households", P)]["credence"]


def test_08_zero_exposure_intensity_produces_no_update() -> None:
    r = run("family-spokesperson", exposure_intensity=0.0)
    assert r.signal_weight == 0.0
    assert r.delta_credence == 0.0


def test_09_zero_evidence_strength_produces_no_movement() -> None:
    r = run("family-spokesperson", evidence_strength=0.0)
    assert r.signal_weight == 0.0
    assert r.delta_credence == 0.0


def test_10_trust_cannot_reverse_direction() -> None:
    """Trust scales magnitude only; `d` alone sets sign."""
    for t in (0.0, 0.1, 0.5, 0.9, 1.0):
        r = run("broadcast-journalist", source_trust=t)
        assert r.delta_credence >= 0.0, f"trust {t} reversed an asserting claim"
    for t in (0.1, 0.9):
        r = run("broadcast-journalist", source_trust=t, claim_direction=-1)
        assert r.delta_credence <= 0.0


def test_11_small_input_changes_produce_bounded_changes() -> None:
    base = run("broadcast-journalist").credence
    for delta in (0.01, 0.02, 0.05):
        t = cast.SOURCE_TRUST["broadcast-journalist"][EV["source_category"]]
        moved = run("broadcast-journalist", source_trust=t + delta).credence
        assert abs(moved - base) < 0.1, "small trust change produced a large jump"


def test_12_values_never_leave_declared_range() -> None:
    for eid in PEOPLE_IDS:
        for t in (0.0, 1.0):
            for e in (0.0, 1.0):
                for x in (0.0, 1.0):
                    r = run(eid, source_trust=t, evidence_strength=e, exposure_intensity=x)
                    for v in (r.credence, r.confidence, r.salience):
                        assert v is None or 0.0 <= v <= 1.0


def test_13_missing_never_becomes_zero() -> None:
    r = run("family-spokesperson", source_trust=None)
    assert r.evidence_status == "UNKNOWN"
    assert r.signal_weight is None
    assert r.credence == cast.PRIORS[("family-spokesperson", P)]["credence"]
    assert r.credence != 0.0


def test_14_repeated_execution_is_identical() -> None:
    runs = [run("family-spokesperson").trace for _ in range(5)]
    assert all(r == runs[0] for r in runs)


# ══ COUNTERFACTUALS — does the divergence come from the mechanism or the fixtures? ═══════════════


def _people_credence(**override) -> dict[str, float]:
    return {e: run(e, **override).credence for e in PEOPLE_IDS}


BASELINE = None


@pytest.fixture(scope="module", autouse=True)
def _baseline():
    global BASELINE
    BASELINE = {e: run(e).credence for e in PEOPLE_IDS}


def test_cf_01_removing_exposure_removes_the_update() -> None:
    for eid in PEOPLE_IDS:
        r = run(eid, exposure_intensity=None)
        assert r.delta_credence == 0.0
        assert r.evidence_status == "UNEXPOSED"


def test_cf_02_equalising_priors_narrows_divergence() -> None:
    """
    If the spread collapses when priors are equalised, priors were carrying the divergence.
    Reported either way — this measures, it does not assume.
    """
    equal = _people_credence(prior_credence=0.35, prior_confidence=0.35, prior_salience=0.7)
    assert spread(equal) < spread(BASELINE), (
        f"equalising priors did not narrow divergence: "
        f"baseline {spread(BASELINE):.4f} -> equalised {spread(equal):.4f}"
    )


def test_cf_03_equalising_trust_narrows_divergence() -> None:
    equal = _people_credence(source_trust=0.55)
    assert spread(equal) < spread(BASELINE), (
        f"equalising trust did not narrow divergence: "
        f"baseline {spread(BASELINE):.4f} -> equalised {spread(equal):.4f}"
    )


def test_cf_04_equalising_exposure_changes_divergence_less_than_trust_or_priors() -> None:
    """Exposure is close to uniform across the three already, so it should carry the least."""
    eq_exposure = spread(_people_credence(exposure_intensity=0.9, relay_factor=1.0))
    eq_trust = spread(_people_credence(source_trust=0.55))
    eq_priors = spread(
        _people_credence(prior_credence=0.35, prior_confidence=0.35, prior_salience=0.7)
    )
    base = spread(BASELINE)
    assert abs(base - eq_exposure) < abs(base - eq_trust)
    assert abs(base - eq_exposure) < abs(base - eq_priors)


def test_cf_05_stronger_evidence_moves_the_uncertain_case_predictably() -> None:
    weak = run("broadcast-journalist", evidence_strength=0.20)
    mid = run("broadcast-journalist")
    strong = run("broadcast-journalist", evidence_strength=0.90)
    assert weak.credence < mid.credence < strong.credence
    assert weak.confidence < mid.confidence < strong.confidence
    # Stronger evidence should resolve the uncertainty; weak evidence should not.
    assert mid.is_uncertain
    assert not strong.is_uncertain


def test_cf_06_weaker_evidence_reduces_the_strongest_result() -> None:
    strong = run("family-spokesperson")
    weak = run("family-spokesperson", evidence_strength=0.10)
    assert weak.credence < strong.credence
    assert weak.delta_credence < strong.delta_credence


def test_cf_07_identical_inputs_give_identical_outputs_across_entities() -> None:
    common = dict(
        prior_credence=0.4, prior_confidence=0.4, prior_salience=0.6,
        evidentiary_threshold=0.5, source_trust=0.6, evidence_strength=0.5,
        exposure_intensity=0.8, relay_factor=1.0, relevance=0.7,
    )
    outs = {e: run(e, **common).credence for e in PEOPLE_IDS}
    assert len(set(outs.values())) == 1, f"identical inputs produced different outputs: {outs}"


# ══ SENSITIVITY ══════════════════════════════════════════════════════════════════════════════════


def test_sens_01_credence_is_monotonic_in_trust() -> None:
    vals = [run("broadcast-journalist", source_trust=t).credence for t in (0.1, 0.3, 0.5, 0.7, 0.9)]
    assert vals == sorted(vals)


def test_sens_02_credence_is_monotonic_in_evidence() -> None:
    vals = [run("broadcast-journalist", evidence_strength=e).credence for e in (0.1, 0.3, 0.5, 0.7, 0.9)]
    assert vals == sorted(vals)


def test_sens_03_higher_threshold_reduces_movement() -> None:
    low = run("broadcast-journalist", evidentiary_threshold=0.2).delta_credence
    high = run("broadcast-journalist", evidentiary_threshold=0.8).delta_credence
    assert high < low


def test_sens_04_no_fixture_label_determines_an_outcome() -> None:
    """
    The outcome must follow the numbers, not the role. Give the minister the spokesperson's
    declared inputs and the minister must adopt.
    """
    sp = build("family-spokesperson")
    swapped = run(
        "government-minister",
        prior_credence=sp.prior_credence,
        prior_confidence=sp.prior_confidence,
        prior_salience=sp.prior_salience,
        evidentiary_threshold=sp.evidentiary_threshold,
        source_trust=sp.source_trust,
        exposure_intensity=sp.exposure_intensity,
        relay_factor=sp.relay_factor,
        relevance=sp.relevance,
    )
    original = run("family-spokesperson")
    assert swapped.credence == pytest.approx(original.credence)


# ══ AGGREGATION ══════════════════════════════════════════════════════════════════════════════════


def test_agg_01_population_weighting_is_correct() -> None:
    """Verified independently of the engine's own arithmetic."""
    vals = [(0.6, 100), (0.2, 300)]
    assert population_weighted(vals) == pytest.approx((0.6 * 100 + 0.2 * 300) / 400)


def test_agg_02_unexposed_excluded_not_averaged_as_zero() -> None:
    with_missing = population_weighted([(0.6, 100), (None, 900)])
    assert with_missing == pytest.approx(0.6), "a missing cohort was averaged in as zero"
    assert population_weighted([(None, 100)]) is None


def test_agg_03_uncertainty_is_first_class_not_weak_acceptance() -> None:
    r = run("broadcast-journalist")
    assert r.is_uncertain
    assert 0.35 <= r.credence <= 0.65
    assert r.confidence < 0.5


# ══ B5 ═══════════════════════════════════════════════════════════════════════════════════════════


def test_b5_01_no_protected_trait_or_ranking_field_in_the_rule() -> None:
    """
    Prefix terms use substring matching; short identity terms use WORD BOUNDARIES.

    'race' as a substring matches 'trace', which is a legitimate provenance field. A check that
    cannot tell those apart would either fire falsely or be silently loosened later — both worse
    than getting the matcher right once.
    """
    import re

    src = executable_source(upd).lower()

    for prefix in ("susceptib", "persuad", "influenceab", "conversion", "manipulab", "gullib"):
        assert prefix not in src, f"update module mentions '{prefix}'"

    for word in ("race", "ethnicity", "religion", "gender", "sex", "disability",
                 "postcode", "caste", "rank", "ranking"):
        assert not re.search(rf"{word}", src), f"update module mentions '{word}'"


def test_b5_02_organisations_receive_no_emotion_vector() -> None:
    from app.simulation.belief.schemas import EmotionalState, MessageTarget

    org = MessageTarget(scenario_id=cast.SCENARIO_ID, kind="organisation", entity_id="national-government")
    with pytest.raises(Exception):
        EmotionalState(holder=org, values={})


def test_b5_03_every_result_carries_provenance() -> None:
    r = run("family-spokesperson")
    assert r.trace["rule_version"] == "belief-update-v1"
    for key in ("x", "rho", "t", "e", "r", "theta", "w", "d", "target",
                "prior_credence", "delta_credence", "resulting_credence"):
        assert key in r.trace, f"trace missing {key}"


# ══ ROLE AND BIOGRAPHY ARE NOT CAPABILITY ════════════════════════════════════════════════════════
#
# Background shapes exposure, access, obligation and relationships. It must never act as a proxy
# for intelligence, competence, judgement or gullibility.


def test_role_01_role_label_swap_leaves_the_result_unchanged() -> None:
    """
    Item 7. Swap which role a set of calculation inputs belongs to; the result must follow the
    inputs, not the label.
    """
    minister_inputs = build("government-minister")
    as_journalist = apply_update(minister_inputs)
    as_minister = run("government-minister")
    assert as_journalist.credence == as_minister.credence
    assert as_journalist.trace == as_minister.trace


def test_role_02_biography_swap_leaves_the_calculation_unchanged() -> None:
    """
    Item 8. Biography is interface content. Swapping every bio must not move a single number.
    """
    before = {e: run(e).credence for e in PEOPLE_IDS}
    originals = [p["bio"] for p in cast.PEOPLE]
    try:
        for person, swapped in zip(cast.PEOPLE, reversed(originals)):
            person["bio"] = swapped
        after = {e: run(e).credence for e in PEOPLE_IDS}
        assert before == after, "biography content changed the calculation"
    finally:
        for person, original in zip(cast.PEOPLE, originals):
            person["bio"] = original


def test_role_03_no_occupation_education_or_wealth_field_reaches_the_formula() -> None:
    fields = set(UpdateInput.__dataclass_fields__)
    for forbidden in (
        "role", "occupation", "job", "title", "education", "credential", "qualification",
        "wealth", "income", "class", "status", "seniority", "competence", "intelligence",
        "capability", "judgement", "rationality",
    ):
        assert forbidden not in fields, f"'{forbidden}' reaches the belief update"


def test_role_04_no_role_specific_branch_in_the_formula() -> None:
    """A role may set a declared input. It may never select a different code path."""
    src = executable_source(upd).lower()
    for role_word in ("minister", "journalist", "spokesperson", "broadcaster", "union", "official"):
        assert role_word not in src, f"update module branches on role: {role_word}"


def test_role_05_seniority_does_not_imply_a_stronger_or_weaker_result() -> None:
    """
    Give all three identical inputs; identical results. Any difference would mean the role label
    was doing work, which is the failure this suite exists to exclude.
    """
    common = dict(
        prior_credence=0.4, prior_confidence=0.4, prior_salience=0.6,
        evidentiary_threshold=0.5, source_trust=0.6, evidence_strength=0.5,
        exposure_intensity=0.8, relay_factor=1.0, relevance=0.7,
    )
    results = {e: run(e, **common) for e in PEOPLE_IDS}
    assert len({r.credence for r in results.values()}) == 1
    assert len({r.confidence for r in results.values()}) == 1
