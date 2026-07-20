"""
Cohort exposure and belief — three separate dimensions.

The central proof here is negative: with only a mean per cohort, an internal distribution is
UNAVAILABLE and says so. Manufacturing shares from an average would invent precision the data does
not contain.
"""

from __future__ import annotations

import pytest

from app.simulation.belief import cast
from app.simulation.belief.cohorts import (
    BeliefLean,
    CohortInput,
    CohortReport,
    DistributionStatus,
    ExposureCoverage,
    population_exposure_coverage,
    report,
    weighted_aggregate,
)
from app.simulation.belief.update import UpdateInput, apply_update

P = "P-WARNINGS-IGNORED"
EV = cast.SHARED_EVENT
EXPOSURE = {e["entity_id"]: e for e in cast.EXPOSURES}
COHORT_IDS = [c["cohort_id"] for c in cast.COHORTS]


def build(cid: str, **over) -> CohortInput:
    c = next(x for x in cast.COHORTS if x["cohort_id"] == cid)
    prior = cast.PRIORS.get((cid, P))
    e = EXPOSURE.get(cid)
    resulting = None
    if e and prior:
        resulting = apply_update(
            UpdateInput(
                prior_credence=prior["credence"], prior_confidence=prior["confidence"],
                prior_salience=prior["salience"], evidentiary_threshold=0.45,
                source_trust=cast.SOURCE_TRUST[cid][EV["source_category"]],
                evidence_strength=EV["evidence_strength"], exposure_intensity=e["intensity"],
                relay_factor=e["relay"], relevance=cast.RELEVANCE[cid],
                claim_direction=EV["claim_direction"],
            )
        ).credence
    base = dict(
        represents_population=c["represents_population"],
        prior_credence=prior["credence"] if prior else None,
        resulting_credence=resulting,
        exposure_intensity=e["intensity"] if e else None,
        exposure_declared=True,
    )
    base.update(over)
    return CohortInput(**base)


def run(cid: str, **over) -> CohortReport:
    name = next(x["display_name"] for x in cast.COHORTS if x["cohort_id"] == cid)
    return report(build(cid, **over), display_name=name)


def all_reports() -> list[CohortReport]:
    return [run(c) for c in COHORT_IDS]


# ══ DIMENSION SEPARATION ═════════════════════════════════════════════════════════════════════════


def test_01_exposure_and_belief_are_separate_fields() -> None:
    fields = set(CohortReport.__dataclass_fields__)
    assert {"exposure_coverage", "belief_lean"} <= fields
    for r in all_reports():
        assert isinstance(r.exposure_coverage, ExposureCoverage)
        assert isinstance(r.belief_lean, BeliefLean)


def test_02_an_exposed_cohort_may_remain_uncertain() -> None:
    r = run("port-workers")
    assert r.exposure_coverage is ExposureCoverage.exposed
    assert r.belief_lean is BeliefLean.uncertain


def test_03_an_unexposed_cohort_retains_a_prior_leaning() -> None:
    """The whole point of separating the axes."""
    r = run("inland-households")
    assert r.exposure_coverage is ExposureCoverage.unexposed
    assert r.credence == cast.PRIORS[("inland-households", P)]["credence"]
    assert r.credence is not None and r.credence != 0.0
    assert r.belief_lean is not BeliefLean.missing


def test_04_missing_exposure_is_distinct_from_unexposed() -> None:
    unknown = run("port-workers", exposure_declared=False)
    unexposed = run("port-workers", exposure_intensity=None)
    assert unknown.exposure_coverage is ExposureCoverage.unknown
    assert unexposed.exposure_coverage is ExposureCoverage.unexposed
    assert unknown.exposure_coverage is not unexposed.exposure_coverage
    assert unknown.exposure_missing_denominator > 0
    assert unexposed.exposure_missing_denominator == 0


def test_05_missing_belief_is_distinct_from_uncertainty() -> None:
    missing = run("port-workers", prior_credence=None, resulting_credence=None)
    uncertain = run("port-workers")
    assert missing.belief_lean is BeliefLean.missing
    assert uncertain.belief_lean is BeliefLean.uncertain


def test_06_missing_never_serialises_as_zero() -> None:
    r = run("port-workers", prior_credence=None, resulting_credence=None)
    assert r.credence is None and r.credence != 0.0
    assert r.belief_known_denominator == 0
    assert r.leaning_toward_share is None


# ══ DISTRIBUTION HONESTY ═════════════════════════════════════════════════════════════════════════


def test_07_no_distribution_is_inferred_from_a_mean() -> None:
    """The decisive negative test."""
    for r in all_reports():
        assert r.distribution_status is DistributionStatus.unavailable
        assert r.leaning_toward_share is None
        assert r.uncertain_share is None
        assert r.leaning_against_share is None


def test_08_unavailable_distribution_states_its_reason() -> None:
    for r in all_reports():
        assert r.distribution_unavailable_reason
        assert "mean" in r.distribution_unavailable_reason


def test_09_explicit_masses_drive_shares_when_declared() -> None:
    masses = {"leaning_toward": 0.5, "uncertain": 0.3, "leaning_against": 0.2}
    r = run("port-workers", state_masses=masses)
    assert r.distribution_status is DistributionStatus.available
    assert r.leaning_toward_share == 0.5
    assert r.uncertain_share == 0.3
    assert r.leaning_against_share == 0.2


def test_10_declared_masses_must_reconcile() -> None:
    with pytest.raises(ValueError, match="sum to 1.0"):
        run("port-workers", state_masses={"leaning_toward": 0.5, "uncertain": 0.2})


def test_11_reordering_masses_does_not_change_output() -> None:
    a = run("port-workers", state_masses={"leaning_toward": 0.5, "uncertain": 0.3, "leaning_against": 0.2})
    b = run("port-workers", state_masses={"leaning_against": 0.2, "uncertain": 0.3, "leaning_toward": 0.5})
    assert (a.leaning_toward_share, a.uncertain_share, a.leaning_against_share) == (
        b.leaning_toward_share, b.uncertain_share, b.leaning_against_share
    )


# ══ DENOMINATORS ═════════════════════════════════════════════════════════════════════════════════


def test_12_all_denominators_are_explicit() -> None:
    for r in all_reports():
        assert r.total_denominator > 0
        assert (r.exposed_denominator + r.unexposed_denominator
                + r.exposure_missing_denominator) == r.total_denominator
        assert r.aggregate_basis


def test_13_exposed_only_and_whole_population_cannot_be_confused() -> None:
    """
    A DEFECT THIS TEST FIXES. The figure 0.3989 was previously described as an exposed-only
    aggregate. It is not — the earlier helper excluded only MISSING values, and inland households
    hold a retained prior, so all six cohorts were included. The exposed-only figure is 0.4317.
    """
    reports = all_reports()
    exposed = weighted_aggregate(reports, exposed_only=True)
    everyone = weighted_aggregate(reports, exposed_only=False)

    assert exposed["value"] != everyone["value"]
    assert exposed["cohorts_included"] == 5
    assert everyone["cohorts_included"] == 6
    assert exposed["denominator_population"] == 599_000
    assert everyone["denominator_population"] == 1_001_000
    assert everyone["value"] == pytest.approx(0.3989, abs=5e-4)
    assert exposed["value"] == pytest.approx(0.4317, abs=5e-4)
    assert "exposed cohorts" in exposed["basis"]
    assert "all cohorts" in everyone["basis"]


def test_14_zero_exposed_denominator_does_not_divide_or_fake_a_zero() -> None:
    unexposed_only = [run("inland-households")]
    agg = weighted_aggregate(unexposed_only, exposed_only=True)
    assert agg["value"] is None
    assert agg["value"] != 0.0
    assert agg["denominator_population"] == 0


def test_15_population_weights_reconcile_independently() -> None:
    reports = all_reports()
    cov = population_exposure_coverage(reports)
    expected_total = sum(c["represents_population"] for c in cast.COHORTS)
    assert cov["total_population"] == expected_total
    assert (cov["exposed_population"] + cov["unexposed_population"]
            + cov["exposure_unknown_population"]) == expected_total
    assert cov["unexposed_population"] == 402_000


# ══ INLAND HOUSEHOLDS ════════════════════════════════════════════════════════════════════════════


def test_16_to_20_inland_households_unexposed_but_present() -> None:
    r = run("inland-households")
    assert r.exposure_coverage is ExposureCoverage.unexposed          # 16
    assert r.event_driven_delta == 0.0                                # 17
    assert r.credence == cast.PRIORS[("inland-households", P)]["credence"]  # 18
    assert r.belief_lean is not BeliefLean.against                    # 19
    assert "did not encounter" in r.public_sentence

    cov = population_exposure_coverage(all_reports())                 # 20
    assert cov["total_population"] == 1_001_000
    assert cov["unexposed_share_of_total"] == pytest.approx(402_000 / 1_001_000)


# ══ REGRESSION AND GENERICITY ════════════════════════════════════════════════════════════════════


def test_21_all_six_cohorts_produce_output() -> None:
    assert len(all_reports()) == 6


def test_22_registry_order_does_not_affect_results() -> None:
    forward = {c: run(c).credence for c in COHORT_IDS}
    backward = {c: run(c).credence for c in reversed(COHORT_IDS)}
    assert forward == backward


def test_23_cohort_id_is_not_a_calculation_input() -> None:
    fields = set(CohortInput.__dataclass_fields__)
    for forbidden in ("cohort_id", "id", "display_name", "name"):
        assert forbidden not in fields


def test_24_25_no_protected_trait_or_ranking_field() -> None:
    import inspect
    from app.simulation.belief import cohorts as cmod

    src = inspect.getsource(cmod).lower()
    for banned in ("susceptib", "persuad", "conversion", "ethnic", "religion", "gender", "gullib"):
        assert banned not in src
    fields = set(CohortInput.__dataclass_fields__) | set(CohortReport.__dataclass_fields__)
    for banned in ("susceptibility", "persuadability", "rank", "priority"):
        assert not any(banned in f for f in fields)


def test_26_public_sentences_avoid_technical_vocabulary() -> None:
    for r in all_reports():
        s = r.public_sentence.lower()
        assert s
        for jargon in ("denominator", "weighted mean", "state mass", "tolerance",
                       "aggregate", "credence", "coefficient"):
            assert jargon not in s, f"public sentence contains jargon: {jargon}"
