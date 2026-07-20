"""
Organisation aggregation.

AN ORGANISATION IS A COLLECTIVE ACTOR, NOT A PERSON WITH ONE MIND. It has no emotion, no mood, no
personality, no memory, no intelligence and no personal credence. What it has is an internal
distribution of positions, a governance rule for turning that distribution into an official stance,
and a cohesion value describing how well it holds together.

THE OFFICIAL POSITION IS NOT ASSUMED TO BE THE WEIGHTED MEAN. An organisation's official position
need not equal the average position of its members; it depends on its governance process, mandate,
cohesion and internal distribution. Some bodies do aggregate by majority or weighted vote — this
model simply does not assume it. Here the governance rule reads the distribution, and cohesion
determines how strongly any position can be asserted. A body that is half undecided cannot speak
with conviction however its plurality leans, and that falls out of the arithmetic rather than being
written down as an outcome.

ACTION DIRECTION AND INTENSITY ARE SEPARATE. Alignment runs 0 = oppose, 0.5 = neutral, 1 = support,
so any propensity computed as `alignment x ...` is directionally asymmetric: a firmly opposing body
would score near zero purely because opposition sits at the bottom of the axis. Direction and
strength are different questions, and conflating them would make a determined opponent look
inactive. Intensity is therefore measured from DISTANCE FROM NEUTRALITY, which is symmetric.

Generic by construction: no branch on organisation id, display name, type or biography.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

RULE_VERSION = "org-aggregate-v1"

#: Distribution shares must sum to 1 within this tolerance.
RECONCILE_TOLERANCE = 1e-6

#: Below this cohesion, a body cannot assert a firm position however its plurality leans.
FIRM_POSITION_COHESION = 0.60

#: A plurality this large or larger is required before a firm position is available at all.
FIRM_POSITION_PLURALITY = 0.50


class OfficialPosition(str, Enum):
    support = "support"
    oppose = "oppose"
    uncertain = "uncertain"
    no_position = "no_position"


class ActionDirection(str, Enum):
    """Which way an organisation would act. Separate from how strongly."""

    support = "support"
    oppose = "oppose"
    withhold = "withhold"
    unavailable = "unavailable"


class PositionStrength(str, Enum):
    firm = "firm"
    qualified = "qualified"
    withheld = "withheld"


def _clamp(v: float) -> float:
    return 0.0 if v < 0.0 else 1.0 if v > 1.0 else v


@dataclass(frozen=True)
class OrganisationInput:
    """
    Declared inputs only.

    No id, no display name, no type, no biography — an organisation's identity cannot reach the
    calculation, exactly as a person's cannot.
    """

    internal_blocs: Optional[dict[str, float]]
    cohesion: Optional[float]
    prior_alignment: Optional[float]
    update_weight: Optional[float]
    target_alignment: float
    objectives: tuple[str, ...] = ()


@dataclass(frozen=True)
class OrganisationResult:
    internal_distribution: Optional[dict[str, float]]
    prior_alignment: Optional[float]
    resulting_alignment: Optional[float]
    delta_alignment: Optional[float]
    official_position: Optional[OfficialPosition]
    position_strength: Optional[PositionStrength]
    cohesion: Optional[float]
    action_direction: ActionDirection
    action_intensity: Optional[float]
    governance_rule: str
    objectives: tuple[str, ...]
    status: str
    unavailable_reason: Optional[str] = None
    explanation: dict = field(default_factory=dict)


def _plurality(blocs: dict[str, float]) -> tuple[str, float]:
    """Largest bloc. Ties resolve by sorted name so ordering never affects the result."""
    return max(sorted(blocs.items()), key=lambda kv: kv[1])


def aggregate(i: OrganisationInput) -> OrganisationResult:
    """
    One organisation's response, derived from its distribution and governance rule.

    Missing inputs stay missing. A body with no declared distribution has no official position —
    that is unavailable, not `no_position`, and not zero.
    """
    missing = [
        name
        for name, value in (
            ("internal_blocs", i.internal_blocs),
            ("cohesion", i.cohesion),
            ("prior_alignment", i.prior_alignment),
        )
        if value is None
    ]
    if missing:
        return OrganisationResult(
            internal_distribution=i.internal_blocs,
            prior_alignment=i.prior_alignment,
            resulting_alignment=None,
            delta_alignment=None,
            official_position=None,
            position_strength=None,
            cohesion=i.cohesion,
            action_direction=ActionDirection.unavailable,
            action_intensity=None,
            governance_rule="plurality-subject-to-cohesion",
            objectives=i.objectives,
            status="UNAVAILABLE",
            unavailable_reason=f"missing declared input: {', '.join(missing)}",
            explanation={"rule_version": RULE_VERSION, "skipped": "missing_input"},
        )

    blocs = dict(i.internal_blocs)
    total = sum(blocs.values())
    if abs(total - 1.0) > RECONCILE_TOLERANCE:
        raise ValueError(f"internal distribution must sum to 1.0, got {total:.9f}")

    w = i.update_weight
    if w is None:
        # Unexposed: the distribution stands, but nothing moved it.
        delta = 0.0
    else:
        delta = w * i.cohesion * (i.target_alignment - i.prior_alignment)
    resulting = _clamp(i.prior_alignment + delta)

    # ── Governance rule: plurality, subject to cohesion ──────────────────────────────────────────
    #
    # The uncertain bloc is counted as what it is — undecided — and never folded into either side.
    # A body that is half undecided has no firm position to assert, which is why the strength test
    # reads the plurality share and the cohesion together rather than the mean.
    lead_name, lead_share = _plurality(blocs)
    uncertain_share = blocs.get("uncertain", 0.0)

    if lead_name == "uncertain" or lead_share < FIRM_POSITION_PLURALITY:
        position = OfficialPosition.uncertain
    elif lead_name == "support":
        position = OfficialPosition.support
    elif lead_name == "oppose":
        position = OfficialPosition.oppose
    else:
        position = OfficialPosition.no_position

    if position is OfficialPosition.uncertain:
        strength = PositionStrength.withheld
    elif i.cohesion >= FIRM_POSITION_COHESION and lead_share >= FIRM_POSITION_PLURALITY:
        strength = PositionStrength.firm
    else:
        strength = PositionStrength.qualified

    # ── Action direction and intensity, kept separate ────────────────────────────────────────────
    #
    # Direction comes from the official position. Intensity is measured from DISTANCE FROM
    # NEUTRALITY, so a firmly opposing body and a firmly supporting body with the same cohesion and
    # the same decisive margin receive the SAME intensity. Using alignment directly would have made
    # opposition look inactive purely because it sits near zero on the support axis.
    decisive = max(0.0, lead_share - uncertain_share)
    distance_from_neutral = abs(2.0 * resulting - 1.0)

    if position is OfficialPosition.support:
        direction = ActionDirection.support
    elif position is OfficialPosition.oppose:
        direction = ActionDirection.oppose
    else:
        direction = ActionDirection.withhold

    if strength is PositionStrength.withheld:
        # A body with no position to assert is not positioned to act on it.
        action_intensity = 0.0
    else:
        action_intensity = _clamp(distance_from_neutral * i.cohesion * decisive)

    weighted_mean = sum(
        share * {"support": 1.0, "oppose": 0.0, "uncertain": 0.5}.get(name, 0.5)
        for name, share in blocs.items()
    )

    return OrganisationResult(
        internal_distribution=blocs,
        prior_alignment=i.prior_alignment,
        resulting_alignment=resulting,
        delta_alignment=resulting - i.prior_alignment,
        official_position=position,
        position_strength=strength,
        cohesion=i.cohesion,
        action_direction=direction,
        action_intensity=action_intensity,
        governance_rule="plurality-subject-to-cohesion",
        objectives=i.objectives,
        status="AGGREGATED",
        explanation={
            "rule_version": RULE_VERSION,
            "prior_alignment": i.prior_alignment,
            "target_alignment": i.target_alignment,
            "update_weight": w,
            "cohesion": i.cohesion,
            "cohesion_contribution": (w * i.cohesion) if w is not None else None,
            "delta_alignment": resulting - i.prior_alignment,
            "resulting_alignment": resulting,
            "internal_distribution": blocs,
            "plurality_bloc": lead_name,
            "plurality_share": lead_share,
            "uncertain_share": uncertain_share,
            "governance_rule": "plurality-subject-to-cohesion",
            "position_derivation": (
                f"plurality bloc '{lead_name}' at {lead_share:.2f}; "
                f"cohesion {i.cohesion:.2f} vs firm threshold {FIRM_POSITION_COHESION}; "
                f"position={position.value}, strength={strength.value}"
            ),
            "action_direction": direction.value,
            "distance_from_neutral": distance_from_neutral,
            "decisive_margin": decisive,
            "action_intensity_derivation": (
                f"direction={direction.value}; intensity = distance from neutrality "
                f"{distance_from_neutral:.4f} x cohesion {i.cohesion:.2f} x decisive margin "
                f"{decisive:.2f} = {action_intensity:.4f}"
                + (" (withheld position -> zero)" if strength is PositionStrength.withheld else "")
            ),
            "weighted_mean_for_comparison": weighted_mean,
            "official_position_equals_weighted_mean": False,
            "objectives": list(i.objectives),
        },
    )
