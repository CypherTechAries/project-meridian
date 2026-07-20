"""
Typed provenance and calculation traces.

Every belief-slice output must answer where its value came from, which rule produced it, what was
unavailable, and over what denominator — without re-running the engine.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.safety.controls import B5Violation
from app.simulation.belief import cast
from app.simulation.belief.cohorts import (
    CohortInput,
    ExposureCoverage,
    report,
    weighted_aggregate,
)
from app.simulation.belief.organisations import OrganisationInput, aggregate
from app.simulation.belief.provenance import (
    CohortTrace,
    EntityRef,
    Origin,
    OrganisationTrace,
    PersonUpdateTrace,
    Provenance,
    ResultStatus,
    RetainedPrior,
    assert_no_zero_for_absence,
    canonical_json,
)
from app.simulation.belief.schemas import PropositionKind
from app.simulation.belief.thresholds import ThresholdKind
from app.simulation.belief.update import UpdateInput, apply_update

SID, SVER = cast.SCENARIO_ID, cast.SCENARIO_VERSION
FACTUAL = "P-WARNINGS-IGNORED"
EV = cast.SHARED_EVENT
EXPOSURE = {e["entity_id"]: e for e in cast.EXPOSURES}
REG = cast.threshold_registry()


def ref(kind: str, eid: str, scenario: str = SID) -> EntityRef:
    return EntityRef(scenario_id=scenario, entity_kind=kind, entity_id=eid)


def prov(kind: str, eid: str, status: ResultStatus = ResultStatus.updated, **over) -> Provenance:
    base = dict(
        scenario_id=SID, scenario_version=SVER, entity=ref(kind, eid),
        proposition_id=FACTUAL, proposition_kind=PropositionKind.attribution,
        tick=EV["introduced_at_tick"], origin=Origin.engine, result_status=status,
        rule_id="belief-update", rule_version="belief-update-v1",
        created_from=(f"event:{EV['event_id']}",),
    )
    base.update(over)
    return Provenance(**base)


def person_trace(eid: str) -> PersonUpdateTrace:
    e = EXPOSURE.get(eid)
    p = cast.PRIORS[(eid, FACTUAL)]
    t = REG.value_for(eid, FACTUAL, expect=ThresholdKind.verification)
    r = apply_update(UpdateInput(
        prior_credence=p["credence"], prior_confidence=p["confidence"],
        prior_salience=p["salience"], evidentiary_threshold=t,
        source_trust=cast.SOURCE_TRUST[eid][EV["source_category"]],
        evidence_strength=EV["evidence_strength"],
        exposure_intensity=e["intensity"] if e else None,
        relay_factor=e["relay"] if e else 1.0,
        relevance=cast.RELEVANCE[eid], claim_direction=EV["claim_direction"]))
    exposed = e is not None
    return PersonUpdateTrace(
        provenance=prov("person", eid,
                        ResultStatus.updated if exposed else ResultStatus.unexposed),
        prior_state_reference=f"prior:{eid}:{FACTUAL}",
        information_event_reference=EV["event_id"],
        exposure_reference=f"exposure:{eid}:{EV['event_id']}" if exposed else None,
        contextual_threshold_reference=f"threshold:{eid}:{FACTUAL}:verification",
        source_trust_reference=f"trust:{eid}:{EV['source_category']}",
        prior_credence=p["credence"], prior_confidence=p["confidence"],
        source_trust=cast.SOURCE_TRUST[eid][EV["source_category"]],
        contextual_threshold=t, evidence_strength=EV["evidence_strength"],
        exposure_intensity=e["intensity"] if e else None,
        relay_factor=e["relay"] if e else None, relevance=cast.RELEVANCE[eid],
        evidence_status=r.evidence_status, update_weight=r.signal_weight,
        target_value=0.5 + 0.5 * EV["claim_direction"],
        raw_credence_delta=r.delta_credence, raw_confidence_delta=r.delta_confidence,
        clamped=False, final_credence=r.credence, final_confidence=r.confidence,
        result_classification="material" if r.delta_credence >= 0.10 else "limited",
        uncertainty_status="uncertain" if r.is_uncertain else "resolved",
        no_update_reason=None if exposed else "no exposure record for this event",
    )


def org_trace(oid: str) -> OrganisationTrace:
    o = next(x for x in cast.ORGANISATIONS if x["organisation_id"] == oid)
    e = EXPOSURE[oid]
    w = (e["intensity"] * e["relay"] * cast.SOURCE_TRUST[oid][EV["source_category"]]
         * EV["evidence_strength"] * cast.RELEVANCE[oid])
    r = aggregate(OrganisationInput(
        internal_blocs=o["internal_blocs"], cohesion=o["cohesion"],
        prior_alignment=o["official_alignment"], update_weight=w,
        target_alignment=1.0, objectives=tuple(o["objectives"])))
    x = r.explanation
    return OrganisationTrace(
        provenance=prov("organisation", oid, rule_id="org-aggregate",
                        rule_version="org-aggregate-v1"),
        exposure_references=(f"exposure:{oid}:{EV['event_id']}",),
        prior_official_alignment=r.prior_alignment, update_weight=x["update_weight"],
        target_alignment=x["target_alignment"], cohesion=r.cohesion,
        cohesion_contribution=x["cohesion_contribution"],
        raw_alignment_delta=r.delta_alignment, resulting_alignment=r.resulting_alignment,
        internal_distribution=r.internal_distribution,
        uncertain_bloc_share=x["uncertain_share"], decisive_margin=x["decisive_margin"],
        governance_rule=r.governance_rule, official_position=r.official_position.value,
        official_position_derivation=x["position_derivation"],
        official_position_equals_weighted_mean=False,
        action_direction=r.action_direction.value, action_intensity=r.action_intensity,
        action_intensity_derivation=x["action_intensity_derivation"],
        objectives=r.objectives,
    )


def cohort_trace(cid: str) -> CohortTrace:
    c = next(x for x in cast.COHORTS if x["cohort_id"] == cid)
    p = cast.PRIORS.get((cid, FACTUAL))
    e = EXPOSURE.get(cid)
    resulting = None
    if e and p:
        resulting = apply_update(UpdateInput(
            prior_credence=p["credence"], prior_confidence=p["confidence"],
            prior_salience=p["salience"], evidentiary_threshold=0.45,
            source_trust=cast.SOURCE_TRUST[cid][EV["source_category"]],
            evidence_strength=EV["evidence_strength"], exposure_intensity=e["intensity"],
            relay_factor=e["relay"], relevance=cast.RELEVANCE[cid],
            claim_direction=EV["claim_direction"])).credence
    rep = report(CohortInput(
        represents_population=c["represents_population"],
        prior_credence=p["credence"] if p else None, resulting_credence=resulting,
        exposure_intensity=e["intensity"] if e else None, exposure_declared=True),
        display_name=c["display_name"])
    unexposed = rep.exposure_coverage is ExposureCoverage.unexposed
    return CohortTrace(
        provenance=prov("cohort", cid,
                        ResultStatus.unexposed if unexposed else ResultStatus.updated,
                        rule_id="cohort-report", rule_version="cohort-report-v1"),
        population_weight=rep.population_weight, total_denominator=rep.total_denominator,
        exposed_denominator=rep.exposed_denominator,
        unexposed_denominator=rep.unexposed_denominator,
        exposure_missing_denominator=rep.exposure_missing_denominator,
        belief_known_denominator=rep.belief_known_denominator,
        exposure_status=rep.exposure_coverage.value,
        retained_prior=RetainedPrior(
            value=rep.credence, prior_origin=Origin.fixture,
            reason="not exposed to this event; prior carried forward unchanged",
        ) if unexposed else None,
        event_driven_delta=rep.event_driven_delta, aggregate_value=rep.credence,
        aggregate_basis=rep.aggregate_basis,
        distribution_status=rep.distribution_status.value,
        distribution_unavailable_reason=rep.distribution_unavailable_reason,
        reconciliation_tolerance=1e-9,
    )


# ══ COMMON ═══════════════════════════════════════════════════════════════════════════════════════


def test_01_every_result_kind_has_typed_provenance() -> None:
    assert person_trace("family-spokesperson").provenance.entity.entity_kind == "person"
    assert org_trace("national-government").provenance.entity.entity_kind == "organisation"
    assert cohort_trace("port-workers").provenance.entity.entity_kind == "cohort"


def test_02_calculated_outputs_use_engine_origin() -> None:
    for t in (person_trace("family-spokesperson"), org_trace("public-broadcaster"),
              cohort_trace("port-workers")):
        assert t.provenance.origin is Origin.engine


def test_03_a_retained_prior_records_the_priors_own_origin() -> None:
    """
    The distinction that matters: the engine decided not to update, but the NUMBER is a fixture
    value. Labelling it ENGINE would claim the engine computed it.
    """
    t = cohort_trace("inland-households")
    assert t.retained_prior is not None
    assert t.retained_prior.prior_origin is Origin.fixture
    assert t.retained_prior.decision_origin is Origin.engine
    assert t.provenance.result_status is ResultStatus.unexposed


def test_04_05_references_resolve_and_cross_world_fails() -> None:
    good = ref("person", "family-spokesperson")
    assert good.typed_id().startswith("fict:kestral-strait:person:")
    with pytest.raises(ValidationError, match="cross-world"):
        prov("person", "family-spokesperson", entity=ref("person", "x", scenario="other-world"))


def test_06_entity_kind_mismatches_fail() -> None:
    with pytest.raises(ValidationError, match="cannot describe"):
        OrganisationTrace(
            provenance=prov("cohort", "port-workers"),
            prior_official_alignment=0.1, update_weight=0.1, target_alignment=1.0,
            cohesion=0.5, cohesion_contribution=0.05, raw_alignment_delta=0.0,
            resulting_alignment=0.1, internal_distribution={"support": 1.0},
            uncertain_bloc_share=0.0, decisive_margin=1.0, governance_rule="r",
            official_position="support", official_position_derivation="d",
            action_direction="support", action_intensity=0.1,
            action_intensity_derivation="d")
    with pytest.raises(ValidationError, match="not a belief-slice entity kind"):
        ref("agent", "head-of-government-varo")


def test_07_unknown_fields_are_forbidden() -> None:
    with pytest.raises(ValidationError):
        EntityRef(scenario_id=SID, entity_kind="person", entity_id="x", susceptibility=0.4)


def test_08_records_are_immutable() -> None:
    t = person_trace("family-spokesperson")
    with pytest.raises(ValidationError):
        t.final_credence = 0.99


def test_09_canonical_serialisation_is_deterministic() -> None:
    for build in (lambda: person_trace("government-minister"),
                  lambda: org_trace("coastal-workers-union"),
                  lambda: cohort_trace("coastal-households")):
        assert len({canonical_json(build()) for _ in range(5)}) == 1


def test_10_absence_never_serialises_as_zero() -> None:
    t = cohort_trace("inland-households")
    assert_no_zero_for_absence(t)
    unexposed_person = PersonUpdateTrace(
        provenance=prov("person", "family-spokesperson", ResultStatus.unexposed,
                        origin=Origin.unavailable),
        prior_state_reference="p", information_event_reference=None, exposure_reference=None,
        contextual_threshold_reference=None, source_trust_reference=None,
        prior_credence=None, prior_confidence=None, source_trust=None,
        contextual_threshold=None, evidence_strength=None, exposure_intensity=None,
        relay_factor=None, relevance=None, evidence_status="UNEXPOSED",
        update_weight=None, target_value=None, raw_credence_delta=None,
        raw_confidence_delta=None, clamped=False, final_credence=None, final_confidence=None,
        result_classification=None, uncertainty_status=None,
        no_update_reason="no exposure record")
    payload = canonical_json(unexposed_person)
    assert '"final_credence":null' in payload
    assert '"update_weight":null' in payload
    assert '"final_credence":0' not in payload


# ══ PEOPLE ═══════════════════════════════════════════════════════════════════════════════════════


def test_11_12_person_traces_and_no_update_reasons() -> None:
    for eid in ("family-spokesperson", "government-minister", "broadcast-journalist"):
        assert isinstance(person_trace(eid), PersonUpdateTrace)
    with pytest.raises(ValidationError, match="must state why"):
        PersonUpdateTrace(
            provenance=prov("person", "family-spokesperson", ResultStatus.unexposed),
            prior_state_reference="p", information_event_reference=None, exposure_reference=None,
            contextual_threshold_reference=None, source_trust_reference=None,
            prior_credence=0.5, prior_confidence=0.5, source_trust=None,
            contextual_threshold=None, evidence_strength=None, exposure_intensity=None,
            relay_factor=None, relevance=None, evidence_status="UNEXPOSED",
            update_weight=None, target_value=None, raw_credence_delta=None,
            raw_confidence_delta=None, clamped=False, final_credence=0.5,
            final_confidence=0.5, result_classification=None, uncertainty_status=None)


def test_13_threshold_reference_names_the_proposition_and_kind() -> None:
    t = person_trace("broadcast-journalist")
    assert FACTUAL in t.contextual_threshold_reference
    assert "verification" in t.contextual_threshold_reference


def test_14_15_no_descriptive_or_capability_fields_in_a_person_trace() -> None:
    fields = set(PersonUpdateTrace.model_fields)
    for banned in ("display_name", "bio", "biography", "occupation", "education",
                   "socioeconomic", "role_narrative", "intelligence", "competence",
                   "susceptibility", "persuadability", "audience_rank"):
        assert not any(banned in f for f in fields)
    payload = canonical_json(person_trace("broadcast-journalist")).lower()
    for record in cast.DESCRIPTIVE.values():
        for text in record.values():
            assert text.lower() not in payload


def test_16_17_18_identical_inputs_identical_traces_and_frozen_values() -> None:
    a, b = person_trace("government-minister"), person_trace("government-minister")
    assert canonical_json(a) == canonical_json(b)
    assert a.final_credence == pytest.approx(0.1719459375, abs=1e-9)
    assert a.final_confidence == pytest.approx(0.7688499999999999, abs=1e-9)
    assert a.update_weight == pytest.approx(0.103275, abs=1e-9)


# ══ ORGANISATIONS ════════════════════════════════════════════════════════════════════════════════


def test_19_20_21_organisation_traces_separate_the_concepts() -> None:
    for oid in ("national-government", "public-broadcaster", "coastal-workers-union"):
        t = org_trace(oid)
        assert t.internal_distribution and t.official_position
        assert t.official_position_equals_weighted_mean is False
        assert t.action_direction is not None
        assert t.action_intensity is not None
        assert "intensity" in t.action_intensity_derivation


def test_22_mirrored_intensity_is_symmetric_in_the_trace() -> None:
    gov, union = org_trace("national-government"), org_trace("coastal-workers-union")
    assert gov.action_direction == "oppose"
    assert union.action_direction == "support"
    assert gov.action_intensity > 0.0 and union.action_intensity > 0.0


def test_23_withheld_position_records_zero_intensity_with_a_reason() -> None:
    t = org_trace("public-broadcaster")
    assert t.action_direction == "withhold"
    assert t.action_intensity == 0.0
    assert "withheld" in t.action_intensity_derivation


def test_24_25_no_emotion_or_credence_and_missing_stays_unavailable() -> None:
    fields = set(OrganisationTrace.model_fields)
    for banned in ("emotion", "mood", "personality", "credence", "memory", "intelligence"):
        assert not any(banned in f for f in fields)
    r = aggregate(OrganisationInput(internal_blocs=None, cohesion=None, prior_alignment=None,
                                    update_weight=None, target_alignment=1.0))
    assert r.status == "UNAVAILABLE" and r.action_intensity is None


# ══ COHORTS ══════════════════════════════════════════════════════════════════════════════════════


def test_26_all_six_cohorts_have_typed_traces() -> None:
    assert len([cohort_trace(c["cohort_id"]) for c in cast.COHORTS]) == 6


def test_27_28_inland_households_and_denominators() -> None:
    t = cohort_trace("inland-households")
    assert t.exposure_status == "unexposed"
    assert t.event_driven_delta == 0.0
    assert t.retained_prior.value == 0.35
    assert t.total_denominator == 402_000
    assert t.unexposed_denominator == 402_000


def test_29_aggregate_bases_are_distinct() -> None:
    reports = [
        report(CohortInput(
            represents_population=c["represents_population"],
            prior_credence=cast.PRIORS[(c["cohort_id"], FACTUAL)]["credence"],
            resulting_credence=(None if c["cohort_id"] == "inland-households" else 0.5),
            exposure_intensity=(None if c["cohort_id"] == "inland-households" else 0.8),
            exposure_declared=True), display_name=c["display_name"])
        for c in cast.COHORTS
    ]
    exposed = weighted_aggregate(reports, exposed_only=True)
    everyone = weighted_aggregate(reports, exposed_only=False)
    assert exposed["basis"] != everyone["basis"]
    assert exposed["denominator_population"] != everyone["denominator_population"]


def test_30_31_32_distribution_remains_unavailable() -> None:
    for c in cast.COHORTS:
        t = cohort_trace(c["cohort_id"])
        assert t.distribution_status == "unavailable"
        assert t.distribution_unavailable_reason
        assert t.state_mass_references == ()


def test_33_denominators_must_reconcile() -> None:
    with pytest.raises(ValidationError, match="do not reconcile"):
        CohortTrace(
            provenance=prov("cohort", "port-workers"), population_weight=100,
            total_denominator=100, exposed_denominator=50, unexposed_denominator=10,
            exposure_missing_denominator=0, belief_known_denominator=60,
            exposure_status="exposed", retained_prior=None, event_driven_delta=0.0,
            aggregate_value=0.5, aggregate_basis="b", distribution_status="unavailable",
            distribution_unavailable_reason="r", reconciliation_tolerance=1e-9)


def test_34_registry_order_does_not_affect_traces() -> None:
    ids = [c["cohort_id"] for c in cast.COHORTS]
    forward = {c: canonical_json(cohort_trace(c)) for c in ids}
    backward = {c: canonical_json(cohort_trace(c)) for c in reversed(ids)}
    assert forward == backward


def test_35_b5_absence_guard_catches_a_zero_on_an_absent_record() -> None:
    bad = RetainedPrior(value=0.0, prior_origin=Origin.unavailable, reason="r")
    with pytest.raises(B5Violation):
        assert_no_zero_for_absence(bad)
