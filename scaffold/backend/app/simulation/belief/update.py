"""
The belief update mechanism.

Implements `docs/design/BELIEF-UPDATE-RULE.md` (`belief-update-v1`) exactly.

GENERIC BY CONSTRUCTION. There is no branch on any entity id, no branch on a display name, and no
per-entity coefficient. Every function below takes declared numeric inputs and returns a result; an
entity's identity reaches this module only as a label carried through to the trace. Swap two
entities' declared inputs and their outputs swap with them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

RULE_VERSION = "belief-update-v1"

# Declared coefficients, frozen in the rule specification before any outcome was inspected.
LAMBDA_CONFIDENCE = 0.6
MU_SALIENCE = 0.5
UNCERTAIN_LOW = 0.35
UNCERTAIN_HIGH = 0.65
UNCERTAIN_CONFIDENCE = 0.5


def _clamp(v: float) -> float:
    return 0.0 if v < 0.0 else 1.0 if v > 1.0 else v


@dataclass(frozen=True)
class UpdateInput:
    """
    Everything the rule is allowed to see.

    NOTE WHAT IS ABSENT: no entity id, no display name, no biography, no protected trait, no
    susceptibility. The dataclass is the enforcement - a value that is not a field here cannot
    influence the result.
    """

    prior_credence: Optional[float]
    prior_confidence: Optional[float]
    prior_salience: Optional[float]
    evidentiary_threshold: float
    source_trust: Optional[float]
    evidence_strength: float
    exposure_intensity: Optional[float]
    relay_factor: float
    relevance: Optional[float]
    claim_direction: int


@dataclass(frozen=True)
class UpdateResult:
    credence: Optional[float]
    confidence: Optional[float]
    salience: Optional[float]
    signal_weight: Optional[float]
    delta_credence: float
    delta_confidence: float
    delta_salience: float
    evidence_status: str
    skipped_reason: Optional[str] = None
    trace: dict = field(default_factory=dict)

    @property
    def is_uncertain(self) -> bool:
        """
        Continued uncertainty: a derived reading of the credence/confidence pair, not a fourth
        label. Must be presented as 'uncertain pending evidence', never as weak acceptance.
        """
        if self.credence is None or self.confidence is None:
            return False
        return (
            UNCERTAIN_LOW <= self.credence <= UNCERTAIN_HIGH
            and self.confidence < UNCERTAIN_CONFIDENCE
        )


def apply_update(i: UpdateInput) -> UpdateResult:
    """
    One bounded, deterministic belief update.

    Order matters: MISSING is checked before zero. `w = 0` means "exposed, nothing moved"; missing
    means "we do not know" - and the two must not collapse into the same trace.
    """
    missing = [
        name
        for name, value in (
            ("prior_credence", i.prior_credence),
            ("prior_confidence", i.prior_confidence),
            ("prior_salience", i.prior_salience),
            ("source_trust", i.source_trust),
            ("relevance", i.relevance),
        )
        if value is None
    ]
    if i.exposure_intensity is None:
        # No exposure record at all. Not zero belief - unexposed.
        return UpdateResult(
            credence=i.prior_credence,
            confidence=i.prior_confidence,
            salience=i.prior_salience,
            signal_weight=None,
            delta_credence=0.0,
            delta_confidence=0.0,
            delta_salience=0.0,
            evidence_status="UNEXPOSED",
            skipped_reason="no exposure record",
            trace={"rule_version": RULE_VERSION, "skipped": "unexposed"},
        )
    if missing:
        return UpdateResult(
            credence=i.prior_credence,
            confidence=i.prior_confidence,
            salience=i.prior_salience,
            signal_weight=None,
            delta_credence=0.0,
            delta_confidence=0.0,
            delta_salience=0.0,
            evidence_status="UNKNOWN",
            skipped_reason=f"missing declared input: {', '.join(missing)}",
            trace={"rule_version": RULE_VERSION, "skipped": "missing_input", "missing": missing},
        )

    # Multiplicative: any zero factor yields no update, structurally.
    w = (
        i.exposure_intensity
        * i.relay_factor
        * float(i.source_trust)
        * i.evidence_strength
        * float(i.relevance)
    )

    target = 0.5 + 0.5 * i.claim_direction
    c0 = float(i.prior_credence)
    f0 = float(i.prior_confidence)
    s0 = float(i.prior_salience)

    d_c = w * (1.0 - i.evidentiary_threshold) * (target - c0)
    # Confidence is independent of source trust: exposure to weakly evidenced material may move
    # what is thought likely without resolving how firmly it is held.
    d_f = i.exposure_intensity * i.relay_factor * i.evidence_strength * (1.0 - f0) * LAMBDA_CONFIDENCE
    d_s = w * (1.0 - s0) * MU_SALIENCE

    c1, f1, s1 = _clamp(c0 + d_c), _clamp(f0 + d_f), _clamp(s0 + d_s)

    return UpdateResult(
        credence=c1,
        confidence=f1,
        salience=s1,
        signal_weight=w,
        delta_credence=c1 - c0,
        delta_confidence=f1 - f0,
        delta_salience=s1 - s0,
        evidence_status="EXPOSED" if w > 0 else "EXPOSED_NO_SIGNAL",
        trace={
            "rule_version": RULE_VERSION,
            "x": i.exposure_intensity,
            "rho": i.relay_factor,
            "t": i.source_trust,
            "e": i.evidence_strength,
            "r": i.relevance,
            "theta": i.evidentiary_threshold,
            "w": w,
            "d": i.claim_direction,
            "target": target,
            "prior_credence": c0,
            "delta_credence": c1 - c0,
            "resulting_credence": c1,
            "prior_confidence": f0,
            "delta_confidence": f1 - f0,
            "resulting_confidence": f1,
        },
    )


def apply_stance_update(
    prior_intensity: Optional[float],
    prior_confidence: Optional[float],
    evidentiary_threshold: float,
    signal_weight: Optional[float],
) -> dict:
    """
    Evaluative propositions carry STANCE, never credence.

    No truth value, no factual correctness, no population error rate. A holder is never recorded as
    wrong for holding a value judgement.
    """
    if signal_weight is None or prior_intensity is None or prior_confidence is None:
        return {
            "stance_intensity": prior_intensity,
            "confidence": prior_confidence,
            "evidence_status": "UNKNOWN" if signal_weight is not None else "UNEXPOSED",
            "rule_version": RULE_VERSION,
        }
    d = signal_weight * (1.0 - evidentiary_threshold) * (1.0 - prior_intensity)
    return {
        "stance_intensity": _clamp(prior_intensity + d),
        "confidence": prior_confidence,
        "delta_intensity": d,
        "evidence_status": "EXPOSED",
        "rule_version": RULE_VERSION,
    }


def population_weighted(values: list[tuple[Optional[float], int]]) -> Optional[float]:
    """
    Population-weighted aggregate over cohorts.

    Entries with a missing value are EXCLUDED from both numerator and denominator - an unexposed
    cohort must not be averaged in as though it held zero belief.
    """
    usable = [(v, p) for v, p in values if v is not None]
    if not usable:
        return None
    total = sum(p for _, p in usable)
    return sum(v * p for v, p in usable) / total if total else None
