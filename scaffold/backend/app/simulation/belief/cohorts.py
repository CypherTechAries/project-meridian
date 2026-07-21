"""
Cohort exposure coverage and belief reporting.

THREE SEPARATE DIMENSIONS, deliberately not one flat partition:

  1. EXPOSURE COVERAGE  — did this cohort encounter the event? (exposed / unexposed / unknown)
  2. BELIEF STATE       — what position does it hold? (leaning toward / uncertain / leaning against)
  3. DATA AVAILABILITY  — is the value known at all? (known / missing)

Collapsing these would produce the specific error the model must avoid. An unexposed cohort is not
uncertain, is not neutral, and does not hold zero credence — it may hold a firm prior it simply has
not revised. "Not seeing a claim is not the same as rejecting it" only holds if exposure and belief
are separate axes.

INTERNAL DISTRIBUTION IS UNAVAILABLE, AND SAYS SO. Each cohort carries a single credence. One mean
cannot recover how many members lean toward, remain uncertain or lean against — those are different
populations that can produce the same average. Reverse-engineering shares from a mean would
manufacture precision the data does not contain, so `distribution_status` reports UNAVAILABLE with
the reason. Organisations model internal blocs because they declare them; cohorts do not.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

RULE_VERSION = "cohort-report-v1"
RECONCILE_TOLERANCE = 1e-9

#: Credence band read as genuine uncertainty rather than a weak lean. Defined ONCE in update.py
#: and re-exported here for callers; never restated as a literal.
from .update import UNCERTAIN_HIGH, UNCERTAIN_LOW


class ExposureCoverage(str, Enum):
    exposed = "exposed"
    unexposed = "unexposed"
    unknown = "unknown"


class BeliefLean(str, Enum):
    toward = "leaning_toward"
    uncertain = "uncertain"
    against = "leaning_against"
    missing = "missing"


class DistributionStatus(str, Enum):
    available = "available"
    unavailable = "unavailable"


@dataclass(frozen=True)
class CohortInput:
    """Declared inputs. No cohort id — identity cannot reach the calculation."""

    represents_population: int
    prior_credence: Optional[float]
    resulting_credence: Optional[float]
    exposure_intensity: Optional[float]
    exposure_declared: bool
    #: Explicit member masses, if the model ever declares them. None today — see module docstring.
    state_masses: Optional[dict[str, float]] = None


@dataclass(frozen=True)
class CohortReport:
    # Identity is attached by the caller, not used in calculation.
    population_weight: int

    # 1 — exposure coverage
    exposure_coverage: ExposureCoverage
    total_denominator: int
    exposed_denominator: int
    unexposed_denominator: int
    exposure_missing_denominator: int
    exposed_share: Optional[float]
    unexposed_share: Optional[float]
    exposure_missing_share: Optional[float]

    # 2 — belief state
    belief_lean: BeliefLean
    belief_known_denominator: int
    credence: Optional[float]
    #: Named explicitly so an exposed-only figure can never be read as a whole-population one.
    aggregate_basis: str

    # 3 — availability
    distribution_status: DistributionStatus
    distribution_unavailable_reason: Optional[str]
    leaning_toward_share: Optional[float]
    uncertain_share: Optional[float]
    leaning_against_share: Optional[float]
    belief_missing_share: Optional[float]

    # change
    event_driven_delta: Optional[float]

    explanation: dict = field(default_factory=dict)
    public_sentence: str = ""


def _lean(credence: Optional[float]) -> BeliefLean:
    if credence is None:
        return BeliefLean.missing
    if UNCERTAIN_LOW <= credence <= UNCERTAIN_HIGH:
        return BeliefLean.uncertain
    return BeliefLean.toward if credence > UNCERTAIN_HIGH else BeliefLean.against


def report(i: CohortInput, *, display_name: str) -> CohortReport:
    """
    One cohort's exposure and belief state.

    `display_name` is used ONLY to compose the public sentence. It never touches a number.
    """
    total = int(i.represents_population)

    # ── Dimension 1: exposure coverage ───────────────────────────────────────────────────────────
    if not i.exposure_declared:
        coverage = ExposureCoverage.unknown
        exposed_n, unexposed_n, missing_n = 0, 0, total
    elif i.exposure_intensity is None:
        # Declared, and declared as no contact.
        coverage = ExposureCoverage.unexposed
        exposed_n, unexposed_n, missing_n = 0, total, 0
    else:
        coverage = ExposureCoverage.exposed
        exposed_n, unexposed_n, missing_n = total, 0, 0

    def share(n: int) -> Optional[float]:
        return (n / total) if total else None

    # ── Dimension 2: belief state, independent of exposure ───────────────────────────────────────
    #
    # An unexposed cohort keeps its prior. That is the whole point: it has a position, it simply
    # has not revised it.
    credence = i.resulting_credence if coverage is ExposureCoverage.exposed else i.prior_credence
    lean = _lean(credence)
    belief_known_n = total if credence is not None else 0

    if credence is None:
        basis = "belief unavailable"
    elif coverage is ExposureCoverage.exposed:
        basis = "post-event credence for this cohort (exposed)"
    else:
        basis = "retained prior credence for this cohort (not exposed to this event)"

    # ── Dimension 3: internal distribution ───────────────────────────────────────────────────────
    if i.state_masses:
        total_mass = sum(i.state_masses.values())
        if abs(total_mass - 1.0) > RECONCILE_TOLERANCE:
            raise ValueError(f"state masses must sum to 1.0, got {total_mass!r}")
        status = DistributionStatus.available
        reason = None
        toward = i.state_masses.get(BeliefLean.toward.value)
        unc = i.state_masses.get(BeliefLean.uncertain.value)
        against = i.state_masses.get(BeliefLean.against.value)
        missing_share = i.state_masses.get(BeliefLean.missing.value, 0.0)
    else:
        # The honest answer. One mean cannot recover three populations.
        status = DistributionStatus.unavailable
        reason = (
            "this cohort declares a single credence and no member state masses; an internal "
            "distribution cannot be recovered from a mean without inventing it"
        )
        toward = unc = against = missing_share = None

    delta = (
        (i.resulting_credence - i.prior_credence)
        if (coverage is ExposureCoverage.exposed
            and i.resulting_credence is not None
            and i.prior_credence is not None)
        else (0.0 if coverage is ExposureCoverage.unexposed else None)
    )

    # ── Public sentence — only what the data supports ────────────────────────────────────────────
    if coverage is ExposureCoverage.unknown:
        sentence = f"It is not recorded whether {display_name.lower()} encountered this claim."
    elif coverage is ExposureCoverage.unexposed:
        sentence = (
            f"{display_name} did not encounter this information event; their earlier views "
            f"remain unchanged."
        )
    elif lean is BeliefLean.uncertain:
        sentence = f"{display_name} encountered the claim and remain uncertain about it."
    elif lean is BeliefLean.toward:
        sentence = f"{display_name} encountered the claim and lean towards accepting it."
    elif lean is BeliefLean.against:
        sentence = f"{display_name} encountered the claim and lean against it."
    else:
        sentence = f"{display_name} encountered the claim, but their position is not recorded."

    return CohortReport(
        population_weight=total,
        exposure_coverage=coverage,
        total_denominator=total,
        exposed_denominator=exposed_n,
        unexposed_denominator=unexposed_n,
        exposure_missing_denominator=missing_n,
        exposed_share=share(exposed_n),
        unexposed_share=share(unexposed_n),
        exposure_missing_share=share(missing_n),
        belief_lean=lean,
        belief_known_denominator=belief_known_n,
        credence=credence,
        aggregate_basis=basis,
        distribution_status=status,
        distribution_unavailable_reason=reason,
        leaning_toward_share=toward,
        uncertain_share=unc,
        leaning_against_share=against,
        belief_missing_share=missing_share,
        event_driven_delta=delta,
        explanation={
            "rule_version": RULE_VERSION,
            "population_weight": total,
            "exposure_denominator": exposed_n,
            "belief_denominator": belief_known_n,
            "prior_treatment": (
                "retained; unexposed members keep their prior and receive zero event-driven change"
                if coverage is not ExposureCoverage.exposed
                else "updated by the event"
            ),
            "unexposed_treatment": "counted in population coverage; never mapped to zero or uncertain",
            "missing_treatment": "reported as missing; never zero",
            "aggregation_basis": basis,
            "distribution_status": status.value,
            "distribution_unavailable_reason": reason,
            "reconcile_tolerance": RECONCILE_TOLERANCE,
        },
        public_sentence=sentence,
    )


def population_exposure_coverage(reports: list[CohortReport]) -> dict:
    """Society-level exposure coverage. Every component names its denominator."""
    total = sum(r.total_denominator for r in reports)
    exposed = sum(r.exposed_denominator for r in reports)
    unexposed = sum(r.unexposed_denominator for r in reports)
    unknown = sum(r.exposure_missing_denominator for r in reports)
    assert exposed + unexposed + unknown == total
    return {
        "total_population": total,
        "exposed_population": exposed,
        "unexposed_population": unexposed,
        "exposure_unknown_population": unknown,
        "exposed_share_of_total": (exposed / total) if total else None,
        "unexposed_share_of_total": (unexposed / total) if total else None,
        "basis": "share of total represented population",
    }


def weighted_aggregate(reports: list[CohortReport], *, exposed_only: bool) -> dict:
    """
    Population-weighted credence over a NAMED denominator.

    `exposed_only=True` covers only cohorts that encountered the event; `False` covers every cohort
    with a known belief, including unexposed ones holding a retained prior. The two are different
    numbers and the returned `basis` says which is which, so an exposed-only figure can never be
    presented as the belief of the whole society.
    """
    selected = [
        r for r in reports
        if r.credence is not None
        and (r.exposure_coverage is ExposureCoverage.exposed if exposed_only else True)
    ]
    denom = sum(r.population_weight for r in selected)
    if not denom:
        return {"value": None, "denominator_population": 0, "cohorts_included": 0,
                "basis": "no cohorts met the denominator; no aggregate is available"}
    value = sum(r.credence * r.population_weight for r in selected) / denom
    return {
        "value": value,
        "denominator_population": denom,
        "cohorts_included": len(selected),
        "basis": (
            "mean credence among exposed cohorts with known belief, weighted by represented population"
            if exposed_only
            else "mean credence among all cohorts with known belief, weighted by represented population"
        ),
    }
