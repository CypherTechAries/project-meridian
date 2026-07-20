"""
Contextual thresholds — a threshold belongs to a proposition and a process, not to a person.

The twelve required proofs for the structural correction, including that the frozen factual run is
numerically unchanged by it.
"""

from __future__ import annotations

import inspect

import pytest
from pydantic import ValidationError

from app.safety.controls import B5Violation
from app.simulation.belief import cast
from app.simulation.belief.schemas import PropositionKind
from app.simulation.belief.thresholds import (
    ContextualThreshold,
    ThresholdKind,
    ThresholdRegistry,
)

FACTUAL = "P-WARNINGS-IGNORED"
EVALUATIVE = "P-EMERGENCY-LEGITIMATE"
PEOPLE = ["family-spokesperson", "government-minister", "broadcast-journalist"]


@pytest.fixture(scope="module")
def reg() -> ThresholdRegistry:
    return cast.threshold_registry()


def _record(**over) -> dict:
    base = dict(
        entity_id="family-spokesperson",
        proposition_id=FACTUAL,
        proposition_kind=PropositionKind.attribution,
        threshold_kind=ThresholdKind.verification,
        value=0.5,
        scenario_id=cast.SCENARIO_ID,
        scenario_version=cast.SCENARIO_VERSION,
        setting_process="test",
        rationale="test",
        source_reference="test",
    )
    base.update(over)
    return base


# 1 — one person, two propositions, two different KINDS of threshold
def test_01_same_person_holds_factual_and_evaluative_thresholds(reg: ThresholdRegistry) -> None:
    for eid in PEOPLE:
        factual = reg.resolve(eid, FACTUAL)
        evaluative = reg.resolve(eid, EVALUATIVE)
        assert factual.threshold_kind is ThresholdKind.verification
        assert evaluative.threshold_kind in (ThresholdKind.deliberation, ThresholdKind.commitment)
        assert factual.threshold_kind is not evaluative.threshold_kind


# 2 — a verification threshold cannot attach to an evaluative proposition
def test_02_verification_threshold_rejected_on_evaluative_proposition() -> None:
    with pytest.raises(ValidationError) as exc:
        ContextualThreshold(
            **_record(
                proposition_id=EVALUATIVE,
                proposition_kind=PropositionKind.evaluative,
                threshold_kind=ThresholdKind.verification,
            )
        )
    assert "not admissible" in str(exc.value)


# 3 — deliberation/commitment cannot stand in for verification
@pytest.mark.parametrize("kind", [ThresholdKind.deliberation, ThresholdKind.commitment])
def test_03_deliberation_cannot_substitute_for_verification(kind: ThresholdKind) -> None:
    with pytest.raises(ValidationError):
        ContextualThreshold(**_record(threshold_kind=kind))


def test_03b_expect_mismatch_is_refused(reg: ThresholdRegistry) -> None:
    with pytest.raises(ValueError):
        reg.resolve("family-spokesperson", EVALUATIVE, expect=ThresholdKind.verification)


# 4 — same role, different thresholds, for declared contextual reasons
def test_04_same_role_may_differ_for_declared_reasons() -> None:
    """The role label does not fix the number; the process does."""
    r2 = ThresholdRegistry(
        [
            ContextualThreshold(**_record(entity_id="journalist-a", value=0.55,
                                          setting_process="publication standard",
                                          rationale="requires corroboration")),
            ContextualThreshold(**_record(entity_id="journalist-b", value=0.30,
                                          setting_process="live desk standard",
                                          rationale="different editorial procedure")),
        ],
        {FACTUAL},
    )
    assert r2.value_for("journalist-a", FACTUAL) != r2.value_for("journalist-b", FACTUAL)


# 5 — role label alone does not change resolution
def test_05_role_label_does_not_change_threshold(reg: ThresholdRegistry) -> None:
    before = reg.value_for("broadcast-journalist", FACTUAL)
    originals = [p["display_name"] for p in cast.PEOPLE]
    try:
        for person in cast.PEOPLE:
            person["display_name"] = "Relabelled"
        assert cast.threshold_registry().value_for("broadcast-journalist", FACTUAL) == before
    finally:
        for person, original in zip(cast.PEOPLE, originals):
            person["display_name"] = original


# 6 — provenance names the proposition and the process
def test_06_provenance_identifies_proposition_and_process(reg: ThresholdRegistry) -> None:
    for eid in PEOPLE:
        for pid in (FACTUAL, EVALUATIVE):
            r = reg.resolve(eid, pid)
            assert r.proposition_id == pid
            assert r.setting_process.strip()
            assert r.rationale.strip()
            assert r.scenario_id == cast.SCENARIO_ID
            assert r.scenario_version == cast.SCENARIO_VERSION
            assert r.origin == "FIXTURE"
            assert r.source_reference


# 7 — unknown proposition fails closed
def test_07_unknown_proposition_fails_closed(reg: ThresholdRegistry) -> None:
    with pytest.raises(B5Violation) as exc:
        reg.resolve("family-spokesperson", "P-DOES-NOT-EXIST")
    assert exc.value.control == "B5-03"


# 8 — missing threshold is unavailable, not zero
def test_08_missing_threshold_is_unavailable_not_zero(reg: ThresholdRegistry) -> None:
    v = reg.value_for("port-workers", FACTUAL)
    assert v is None
    assert v != 0.0
    assert reg.resolve("port-workers", FACTUAL) is None


# 9 — unknown threshold kind fails closed
@pytest.mark.parametrize("bad", ["rigour", "critical_thinking", "rationality", "", "VERIFICATION"])
def test_09_unknown_threshold_kind_fails_closed(bad: str) -> None:
    with pytest.raises(ValidationError):
        ContextualThreshold(**_record(threshold_kind=bad))


# 10 — unknown fields forbidden
@pytest.mark.parametrize(
    "extra", ["intelligence", "competence", "education", "occupation", "wealth", "class_", "iq"]
)
def test_10_unknown_fields_are_forbidden(extra: str) -> None:
    with pytest.raises(ValidationError):
        ContextualThreshold(**_record(**{extra: 0.8}))


# 11 — no capability-like value can derive a threshold
def test_11_no_capability_field_exists_on_the_threshold() -> None:
    from app.simulation.belief import thresholds as th

    fields = set(ContextualThreshold.model_fields)
    for banned in (
        "intelligence", "competence", "education", "occupation", "wealth",
        "class", "status", "seniority", "rationality", "sophistication", "gullibility",
    ):
        assert banned not in fields
    src = inspect.getsource(th).lower()
    for prefix in ("susceptib", "persuad", "gullib"):
        assert prefix not in src


# 12 — the frozen factual run is numerically unchanged
def test_12_frozen_factual_run_is_numerically_unchanged() -> None:
    """
    The correction is SEMANTIC. Payload shape may change — provenance fields are new, and that is
    the point — but these six fields must equal the values recorded at 16f593c.
    """
    from app.simulation.belief.update import UpdateInput, apply_update

    # Full precision. The figures quoted in the first-run report were display-rounded to 4dp;
    # these are the actual values. `update.py` is unchanged since 16f593c (empty git diff) and the
    # verification thresholds are provably still 0.20 / 0.75 / 0.55, so the outputs cannot have
    # moved — only my transcription of them was imprecise.
    expected = {
        "family-spokesperson": (
            0.6885100000000001, 0.562, 0.13851000000000002, 0.16200000000000003, 0.38475, "material"
        ),
        "government-minister": (
            0.1719459375, 0.7688499999999999, 0.021945937500000012, 0.06884999999999997,
            0.103275, "limited"
        ),
        "broadcast-journalist": (
            0.408457953125, 0.44237499999999996, 0.05845795312500002, 0.19237499999999996,
            0.19985624999999999, "uncertain"
        ),
    }
    reg = cast.threshold_registry()
    exposures = {e["entity_id"]: e for e in cast.EXPOSURES}

    for eid, (c, f, dc, df, w, klass) in expected.items():
        prior = cast.PRIORS[(eid, FACTUAL)]
        ex = exposures[eid]
        r = apply_update(
            UpdateInput(
                prior_credence=prior["credence"],
                prior_confidence=prior["confidence"],
                prior_salience=prior["salience"],
                evidentiary_threshold=reg.value_for(
                    eid, FACTUAL, expect=ThresholdKind.verification
                ),
                source_trust=cast.SOURCE_TRUST[eid][cast.SHARED_EVENT["source_category"]],
                evidence_strength=cast.SHARED_EVENT["evidence_strength"],
                exposure_intensity=ex["intensity"],
                relay_factor=ex["relay"],
                relevance=cast.RELEVANCE[eid],
                claim_direction=cast.SHARED_EVENT["claim_direction"],
            )
        )
        assert r.credence == pytest.approx(c, abs=1e-6), f"{eid} credence moved"
        assert r.confidence == pytest.approx(f, abs=1e-6), f"{eid} confidence moved"
        assert r.delta_credence == pytest.approx(dc, abs=1e-6), f"{eid} credence delta moved"
        assert r.delta_confidence == pytest.approx(df, abs=1e-6), f"{eid} confidence delta moved"
        assert r.signal_weight == pytest.approx(w, abs=1e-6), f"{eid} update weight moved"
        actual = (
            "material" if r.delta_credence >= 0.10
            else "uncertain" if r.is_uncertain
            else "limited"
        )
        assert actual == klass, f"{eid} outcome classification changed: {actual} != {klass}"
