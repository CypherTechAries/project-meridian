"""
Read-only projection of belief results for API consumption.

WHAT THIS IS
------------
A one-way mapping from engine results to typed response models. It reads what the belief engine
already computes and presents it. It does not decide anything.

WHAT THIS IS NOT — read before describing it anywhere
-----------------------------------------------------
**These results are NOT connected to the authoritative simulation run.** The belief slice is a
self-contained deterministic computation over frozen fixtures in `cast.py`. It shares nothing with
`MeridianModel`, reads no run state, and is not advanced by ticks. Two facts make that concrete:

  1. Nothing outside this package and its tests imports the belief engine. There is no wiring.
  2. `cast.py` declares `scenario_id = "kestral-strait"` — the SAME id as the packaged scenario
     file — but a DISJOINT entity set. The packaged scenario declares five cohorts
     (`coastal-creole-fishing`, `inland-highland-minority`, …); the belief cast declares six
     entirely different ones (`port-workers`, `inland-households`, …) plus three people and three
     organisations the scenario file does not contain.

So this is a **packaged belief snapshot**, not live run state, and `RUN_INTEGRATION` says so in
every response. It must never be labelled live, current, authoritative or persisted. The shared
scenario id is recorded as a known defect rather than smoothed over — see `SCENARIO_ID_NOTE`.

THREE RULES
-----------
1. **No engine model is returned directly.** Every response is a distinct projection type.
2. **Display text is derived, never authored per entity.** Wording comes from the band tables
   below, keyed by structured state. There is no lookup from entity id to sentence.
3. **Absence stays textual.** `UNKNOWN`, `UNAVAILABLE` and `NOT_MODELLED` are statuses. None ever
   becomes `0`.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ...safety.controls import TARGET_PREFIX
from .cohorts import CohortInput, ExposureCoverage, report
from .organisations import OrganisationInput, aggregate
from .provenance import Origin
from .thresholds import ThresholdKind
from .update import UpdateInput, apply_update
from . import cast

PROJECTION_VERSION = "belief-projection-v1"
WORDING_VERSION = "belief-wording-v1"

_FROZEN = ConfigDict(extra="forbid", frozen=True)

#: The truthful description of what these results are. Not live, not authoritative, not persisted.
RUN_INTEGRATION = {
    "connected_to_authoritative_run": False,
    "result_kind": "packaged-belief-snapshot",
    "label": "Deterministic belief-divergence slice — engine-computed demonstration result",
    "explanation": (
        "These results are computed on request from frozen packaged fixtures. They are not live "
        "run state, not current authoritative belief state, and not persisted person state. No "
        "simulation run is read, advanced or written. The same request always returns the same "
        "answer because the mechanism is deterministic, not because anything was stored."
    ),
}

#: A real defect, recorded rather than hidden. Two casts share one scenario id.
SCENARIO_ID_NOTE = (
    "The belief cast declares scenario_id 'kestral-strait', the same id as the packaged scenario "
    "file, but declares a disjoint entity set: six cohorts none of which appear in the scenario "
    "file, plus three people and three organisations the file does not contain. Until the two are "
    "reconciled, belief entity ids resolve against the belief cast registry only."
)


class DisplayStatus(str, Enum):
    ok = "OK"
    unavailable = "UNAVAILABLE"
    not_modelled = "NOT_MODELLED"
    unknown = "UNKNOWN"


#: Layers this slice genuinely models, by entity kind.
MODELLED = {
    "person": (
        "prior view", "current view", "exposure to this event", "contextual source trust",
        "contextual threshold for this claim and process", "confidence", "calculation origin",
    ),
    "organisation": (
        "internal views", "official position", "cohesion", "action direction", "action strength",
        "governance process", "calculation origin",
    ),
    "cohort": (
        "whether the group received the claim", "retained prior view", "event-driven change",
        "current average view", "population represented", "calculation origin",
    ),
}

#: Layers no entity kind models. Returned in every dossier so a client cannot omit them by accident.
NOT_MODELLED = (
    "personal history", "memory", "relationships", "changing trust", "emotional state",
    "cumulative stress", "personalised information feeds", "order in which information arrived",
    "path dependence", "social interaction", "stochastic choice", "persistent life history",
    "intelligence", "competence", "life trajectory",
)

#: Additional absences specific to a kind.
NOT_MODELLED_EXTRA = {
    "organisation": ("internal politics", "who persuades whom", "past decisions",
                     "named individuals inside", "how the internal groups formed"),
    "cohort": ("internal belief breakdown", "confidence", "individual members"),
}

# ── Wording bands ────────────────────────────────────────────────────────────────────────────────
#
# Deterministic, versioned, and keyed ONLY by structured state. No entity id appears in any of
# these tables, so no sentence can be authored for one entity and bypass the engine result.

#: The uncertain band is defined ONCE, in update.py. Never restate it — four copies of this
#: threshold was a real defect found during VP-4 review.
from .update import UNCERTAIN_HIGH as _UNCERTAIN_HIGH, UNCERTAIN_LOW as _UNCERTAIN_LOW


def _view_words(credence: Optional[float]) -> str:
    if credence is None:
        return "not recorded"
    if credence < _UNCERTAIN_LOW:
        return "Doubted it"
    if credence <= _UNCERTAIN_HIGH:
        return "Unsure"
    return "Leaned towards it"


def _movement_words(delta: Optional[float]) -> str:
    if delta is None:
        return "not recorded"
    size = abs(delta)
    if size == 0.0:
        return "did not move at all"
    direction = "towards believing it" if delta > 0 else "away from believing it"
    if size < 0.02:
        return f"barely moved {direction}"
    if size < 0.10:
        return f"took a small step {direction}"
    return f"moved clearly {direction}"


def _confidence_words(before: Optional[float], after: Optional[float]) -> str:
    if before is None or after is None:
        return "not recorded"
    if after >= 0.7:
        settled = "and now feels settled"
    elif after >= 0.5:
        settled = "and is moderately settled"
    else:
        settled = "but is still short of sure"
    moved = "More settled than before" if after > before else "No more settled than before"
    return f"{moved}, {settled}"


def _cohesion_words(cohesion: Optional[float]) -> str:
    if cohesion is None:
        return "not recorded"
    if cohesion >= 0.8:
        return "Strongly united"
    if cohesion >= 0.6:
        return "United enough to speak firmly"
    return "Moderately divided — not united enough to speak firmly"


_POSITION_WORDS = {
    "support": "Officially supports the claim",
    "oppose": "Officially rejects the claim",
    "uncertain": "No firm position",
}
_DIRECTION_WORDS = {
    "support": "Would act in support",
    "oppose": "Would act in opposition",
    "withhold": "Neither — it is holding back",
}


def _force_words(direction: str, intensity: Optional[float]) -> str:
    if direction == "withhold" or not intensity:
        return "None. A withheld position carries no force."
    if intensity >= 0.15:
        return "Prepared to act firmly."
    return "Prepared to act, but not forcefully."


# ── Projection models ────────────────────────────────────────────────────────────────────────────


class OriginRef(BaseModel):
    """Where a value came from, kept separate from who decided not to change it."""

    model_config = _FROZEN
    value_origin: Origin
    decision_origin: Optional[Origin] = None
    note: Optional[str] = None


class Layers(BaseModel):
    """Both lists, always. A client that omits the limitation must choose to."""

    model_config = _FROZEN
    modelled: tuple[str, ...]
    not_modelled: tuple[str, ...]


class EntityHeader(BaseModel):
    model_config = _FROZEN
    typed_id: str
    entity_kind: str
    entity_id: str
    display_name: str
    description: Optional[str] = None
    description_origin: Origin = Origin.fixture
    scenario_id: str
    scenario_version: str


class ClaimRef(BaseModel):
    model_config = _FROZEN
    proposition_id: str
    claim_text: str
    proposition_kind: str
    truth_applicability: str
    event_id: str
    introduced_at_tick: int


class PersonCalculation(BaseModel):
    """Exact values. Reached only through this nested object, never through a display field."""

    model_config = _FROZEN
    prior_credence: float
    final_credence: float
    delta_credence: float
    prior_confidence: float
    final_confidence: float
    final_salience: float
    contextual_threshold: float
    threshold_kind: str
    threshold_setting_process: str
    source_trust: float
    evidence_strength: float
    exposure_intensity: Optional[float]
    relay_factor: Optional[float]
    relevance: float
    signal_weight: Optional[float]
    evidence_status: str
    rule_version: str


class PersonProjection(BaseModel):
    model_config = _FROZEN
    entity: EntityHeader
    claim: ClaimRef
    headline: str
    view_before: str
    view_now: str
    movement: str
    confidence_statement: str
    received_the_claim: bool
    exposure_statement: str
    still_unsure: bool
    reasons: tuple[str, ...] = Field(..., max_length=3)
    verification_process: str
    layers: Layers
    origin: OriginRef
    calculation: PersonCalculation


class OrganisationCalculation(BaseModel):
    model_config = _FROZEN
    internal_blocs: dict[str, float]
    cohesion: float
    prior_alignment: float
    resulting_alignment: float
    delta_alignment: float
    uncertain_bloc_share: float
    decisive_margin: float
    action_intensity: float
    update_weight: Optional[float]
    position_derivation: str
    action_intensity_derivation: str
    governance_rule: str
    rule_version: str


class OrganisationProjection(BaseModel):
    """Internal views and official position are separate fields and never merge into one number."""

    model_config = _FROZEN
    entity: EntityHeader
    claim: ClaimRef
    headline: str
    internal_views: dict[str, float]
    internal_views_statement: str
    cohesion_statement: str
    official_position: str
    official_position_statement: str
    position_strength: str
    action_direction: str
    action_direction_statement: str
    action_strength_statement: str
    governance_process: str
    objectives: tuple[str, ...]
    received_the_claim: bool
    layers: Layers
    origin: OriginRef
    calculation: OrganisationCalculation
    #: Organisations have no emotion, no personal confidence and no single human-like belief.
    confidence_status: DisplayStatus = DisplayStatus.not_modelled


class CohortCalculation(BaseModel):
    model_config = _FROZEN
    prior_credence: Optional[float]
    current_credence: Optional[float]
    event_driven_delta: Optional[float]
    population_weight: int
    total_denominator: int
    exposed_denominator: int
    unexposed_denominator: int
    exposure_missing_denominator: int
    belief_known_denominator: int
    aggregate_basis: str
    rule_version: str


class CohortProjection(BaseModel):
    model_config = _FROZEN
    entity: EntityHeader
    claim: ClaimRef
    headline: str
    received_the_claim: bool
    exposure_status: str
    exposure_statement: str
    view_before: str
    view_now: str
    change_statement: str
    population_represented: int
    #: Always UNAVAILABLE for the current cast. No shares are returned and no chart is implied.
    breakdown_status: DisplayStatus = DisplayStatus.unavailable
    breakdown_reason: str
    #: Cohorts carry no confidence. Shown as an absence rather than borrowed from the person shape.
    confidence_status: DisplayStatus = DisplayStatus.not_modelled
    confidence_reason: str
    layers: Layers
    origin: OriginRef
    calculation: CohortCalculation


class LandscapeEntry(BaseModel):
    model_config = _FROZEN
    typed_id: str
    entity_kind: str
    entity_id: str
    display_name: str
    received_the_claim: bool
    exposure_status: str
    result_statement: str
    reason: Optional[str]
    reason_status: DisplayStatus
    breakdown_status: Optional[DisplayStatus] = None
    origin: OriginRef


class LandscapeProjection(BaseModel):
    model_config = _FROZEN
    projection_version: str
    wording_version: str
    run_integration: dict
    scenario_id_note: str
    claim: ClaimRef
    source_statement: str
    people: tuple[LandscapeEntry, ...]
    organisations: tuple[LandscapeEntry, ...]
    cohorts: tuple[LandscapeEntry, ...]
    population_total: int
    population_reached: int
    population_not_reached: int
    exposure_statement: str
    not_modelled: tuple[str, ...]


# ── Builders ─────────────────────────────────────────────────────────────────────────────────────

_P = "P-WARNINGS-IGNORED"
_EXPOSURE = {e["entity_id"]: e for e in cast.EXPOSURES}
_THRESHOLDS = {
    (t["entity_id"], t["threshold_kind"]): t
    for t in cast.THRESHOLD_RECORDS
    if t["proposition_id"] == _P
}
_COHORT_THRESHOLD = 0.45  # declared group-level threshold; not a person threshold


def _typed(kind: str, entity_id: str) -> str:
    return f"{TARGET_PREFIX}:{cast.SCENARIO_ID}:{kind}:{entity_id}"


def _claim() -> ClaimRef:
    prop = next(p for p in cast.PROPOSITIONS if p["proposition_id"] == _P)
    ev = cast.SHARED_EVENT
    return ClaimRef(
        proposition_id=_P,
        claim_text=prop["claim_text"],
        proposition_kind=prop["kind"],
        truth_applicability=prop["truth_value"],
        event_id=ev["event_id"],
        introduced_at_tick=ev["introduced_at_tick"],
    )


def _header(kind: str, entity_id: str, name: str, desc: Optional[str]) -> EntityHeader:
    return EntityHeader(
        typed_id=_typed(kind, entity_id), entity_kind=kind, entity_id=entity_id,
        display_name=name, description=desc, scenario_id=cast.SCENARIO_ID,
        scenario_version=cast.SCENARIO_VERSION,
    )


def _layers(kind: str) -> Layers:
    return Layers(
        modelled=MODELLED[kind],
        not_modelled=NOT_MODELLED + NOT_MODELLED_EXTRA.get(kind, ()),
    )


def person_projection(entity_id: str) -> PersonProjection:
    person = next(p for p in cast.PEOPLE if p["person_id"] == entity_id)
    prior = cast.PRIORS[(entity_id, _P)]
    exposure = _EXPOSURE.get(entity_id)
    threshold_rec = _THRESHOLDS[(entity_id, "verification")]
    ev = cast.SHARED_EVENT
    trust = cast.SOURCE_TRUST[entity_id][ev["source_category"]]

    result = apply_update(UpdateInput(
        prior_credence=prior["credence"], prior_confidence=prior["confidence"],
        prior_salience=prior["salience"], evidentiary_threshold=threshold_rec["value"],
        source_trust=trust, evidence_strength=ev["evidence_strength"],
        exposure_intensity=exposure["intensity"] if exposure else None,
        relay_factor=exposure["relay"] if exposure else 1.0,
        relevance=cast.RELEVANCE[entity_id], claim_direction=ev["claim_direction"],
    ))
    received = exposure is not None

    # Up to three reasons, each derived from a structured input. The first quotes the declared
    # process; the other two are band readings of evidence strength and prior distance.
    reasons = [threshold_rec["rationale"]]
    if ev["evidence_strength"] < 0.6:
        reasons.append("The evidence behind the claim was only moderately strong.")
    if prior["credence"] < 0.5:
        reasons.append("They had not previously accepted the claim, so there was further to travel.")

    headline = (
        f"{person['display_name'].split(',')[0]} "
        + (_movement_words(result.delta_credence) if received else "did not receive the claim")
        + (", and is still unsure." if result.is_uncertain else ".")
    )

    return PersonProjection(
        entity=_header("person", entity_id, person["display_name"], person["bio"]),
        claim=_claim(),
        headline=headline,
        view_before=_view_words(prior["credence"]),
        view_now=_view_words(result.credence),
        movement=_movement_words(result.delta_credence),
        confidence_statement=_confidence_words(prior["confidence"], result.confidence),
        received_the_claim=received,
        exposure_statement=(
            f"Received it — {exposure['path']}." if received else "Never received the claim."
        ),
        still_unsure=result.is_uncertain,
        reasons=tuple(reasons[:3]),
        verification_process=threshold_rec["setting_process"],
        layers=_layers("person"),
        origin=OriginRef(value_origin=Origin.engine, decision_origin=Origin.engine),
        calculation=PersonCalculation(
            prior_credence=prior["credence"], final_credence=result.credence,
            delta_credence=result.delta_credence, prior_confidence=prior["confidence"],
            final_confidence=result.confidence, final_salience=result.salience,
            contextual_threshold=threshold_rec["value"], threshold_kind=ThresholdKind.verification.value,
            threshold_setting_process=threshold_rec["setting_process"], source_trust=trust,
            evidence_strength=ev["evidence_strength"],
            exposure_intensity=exposure["intensity"] if exposure else None,
            relay_factor=exposure["relay"] if exposure else None,
            relevance=cast.RELEVANCE[entity_id], signal_weight=result.signal_weight,
            evidence_status=result.evidence_status, rule_version=cast.RULE_VERSION,
        ),
    )


def organisation_projection(entity_id: str) -> OrganisationProjection:
    org = next(o for o in cast.ORGANISATIONS if o["organisation_id"] == entity_id)
    exposure = _EXPOSURE[entity_id]
    ev = cast.SHARED_EVENT
    weight = (
        exposure["intensity"] * exposure["relay"]
        * cast.SOURCE_TRUST[entity_id][ev["source_category"]]
        * ev["evidence_strength"] * cast.RELEVANCE[entity_id]
    )
    result = aggregate(OrganisationInput(
        internal_blocs=org["internal_blocs"], cohesion=org["cohesion"],
        prior_alignment=org["official_alignment"], update_weight=weight,
        target_alignment=1.0, objectives=tuple(org["objectives"]),
    ))
    x = result.explanation
    position = result.official_position.value
    direction = result.action_direction.value
    uncertain_pct = int(round(x["uncertain_share"] * 100))

    headline = (
        f"{org['display_name']} does not take a firm public position, because "
        f"{uncertain_pct}% of the people inside it are still undecided."
        if position == "uncertain"
        else f"{org['display_name']}: {_POSITION_WORDS[position].lower()}."
    )

    return OrganisationProjection(
        entity=_header("organisation", entity_id, org["display_name"], org["bio"]),
        claim=_claim(),
        headline=headline,
        internal_views=dict(result.internal_distribution),
        internal_views_statement=(
            f"{int(round(org['internal_blocs'].get('support', 0) * 100))}% lean towards it, "
            f"{uncertain_pct}% are undecided, "
            f"{int(round(org['internal_blocs'].get('oppose', 0) * 100))}% lean against it."
        ),
        cohesion_statement=_cohesion_words(result.cohesion),
        official_position=position,
        official_position_statement=_POSITION_WORDS[position],
        position_strength=result.position_strength.value,
        action_direction=direction,
        action_direction_statement=_DIRECTION_WORDS[direction],
        action_strength_statement=_force_words(direction, result.action_intensity),
        governance_process=x["position_derivation"],
        objectives=result.objectives,
        received_the_claim=True,
        layers=_layers("organisation"),
        origin=OriginRef(value_origin=Origin.engine, decision_origin=Origin.engine),
        calculation=OrganisationCalculation(
            internal_blocs=dict(result.internal_distribution), cohesion=result.cohesion,
            prior_alignment=result.prior_alignment, resulting_alignment=result.resulting_alignment,
            delta_alignment=result.delta_alignment, uncertain_bloc_share=x["uncertain_share"],
            decisive_margin=x["decisive_margin"], action_intensity=result.action_intensity,
            update_weight=x["update_weight"], position_derivation=x["position_derivation"],
            action_intensity_derivation=x["action_intensity_derivation"],
            governance_rule=result.governance_rule, rule_version="org-aggregate-v1",
        ),
    )


def cohort_projection(entity_id: str) -> CohortProjection:
    cohort = next(c for c in cast.COHORTS if c["cohort_id"] == entity_id)
    prior = cast.PRIORS.get((entity_id, _P))
    exposure = _EXPOSURE.get(entity_id)
    ev = cast.SHARED_EVENT
    resulting = None
    if exposure and prior:
        resulting = apply_update(UpdateInput(
            prior_credence=prior["credence"], prior_confidence=prior["confidence"],
            prior_salience=prior["salience"], evidentiary_threshold=_COHORT_THRESHOLD,
            source_trust=cast.SOURCE_TRUST[entity_id][ev["source_category"]],
            evidence_strength=ev["evidence_strength"], exposure_intensity=exposure["intensity"],
            relay_factor=exposure["relay"], relevance=cast.RELEVANCE[entity_id],
            claim_direction=ev["claim_direction"],
        )).credence

    rep = report(CohortInput(
        represents_population=cohort["represents_population"],
        prior_credence=prior["credence"] if prior else None, resulting_credence=resulting,
        exposure_intensity=exposure["intensity"] if exposure else None, exposure_declared=True,
    ), display_name=cohort["display_name"])

    received = rep.exposure_coverage is ExposureCoverage.exposed

    # No invented psychological reason. The explanation is the real exposure path, or its absence.
    if received:
        exposure_statement = f"Received it — {exposure['path']}."
        change_statement = _movement_words(rep.event_driven_delta)
    else:
        exposure_statement = "No route carried this claim to them."
        change_statement = "Their earlier view carried forward untouched."

    return CohortProjection(
        entity=_header("cohort", entity_id, cohort["display_name"], None),
        claim=_claim(),
        headline=rep.public_sentence,
        received_the_claim=received,
        exposure_status=rep.exposure_coverage.value,
        exposure_statement=exposure_statement,
        view_before=_view_words(prior["credence"] if prior else None),
        view_now=_view_words(rep.credence),
        change_statement=change_statement,
        population_represented=rep.population_weight,
        breakdown_status=DisplayStatus.unavailable,
        breakdown_reason=(
            rep.distribution_unavailable_reason
            or "no member state masses are declared for this group"
        ),
        confidence_status=DisplayStatus.not_modelled,
        confidence_reason="This slice does not model confidence for population groups.",
        layers=_layers("cohort"),
        origin=OriginRef(
            value_origin=Origin.fixture if not received else Origin.engine,
            decision_origin=Origin.engine,
            note=(
                "The earlier view came from the packaged story; the engine decided not to change "
                "it because the group never received the claim."
                if not received else None
            ),
        ),
        calculation=CohortCalculation(
            prior_credence=prior["credence"] if prior else None,
            current_credence=rep.credence, event_driven_delta=rep.event_driven_delta,
            population_weight=rep.population_weight, total_denominator=rep.total_denominator,
            exposed_denominator=rep.exposed_denominator,
            unexposed_denominator=rep.unexposed_denominator,
            exposure_missing_denominator=rep.exposure_missing_denominator,
            belief_known_denominator=rep.belief_known_denominator,
            aggregate_basis=rep.aggregate_basis, rule_version="cohort-report-v1",
        ),
    )


def landscape_projection() -> LandscapeProjection:
    people = tuple(
        LandscapeEntry(
            typed_id=p.entity.typed_id, entity_kind="person", entity_id=p.entity.entity_id,
            display_name=p.entity.display_name, received_the_claim=p.received_the_claim,
            exposure_status="exposed" if p.received_the_claim else "unexposed",
            result_statement=p.movement if not p.still_unsure else "Still unsure",
            reason=p.reasons[0] if p.reasons else None, reason_status=DisplayStatus.ok,
            origin=p.origin,
        )
        for p in (person_projection(x["person_id"]) for x in cast.PEOPLE)
    )
    organisations = tuple(
        LandscapeEntry(
            typed_id=o.entity.typed_id, entity_kind="organisation", entity_id=o.entity.entity_id,
            display_name=o.entity.display_name, received_the_claim=True, exposure_status="exposed",
            result_statement=o.official_position_statement,
            reason=o.cohesion_statement, reason_status=DisplayStatus.ok, origin=o.origin,
        )
        for o in (organisation_projection(x["organisation_id"]) for x in cast.ORGANISATIONS)
    )
    # Cohorts get the real exposure path, never an invented psychological reason. Where a group was
    # reached by a relay the path is the honest explanation; where it was not, the absence is.
    cohorts = tuple(
        LandscapeEntry(
            typed_id=c.entity.typed_id, entity_kind="cohort", entity_id=c.entity.entity_id,
            display_name=c.entity.display_name, received_the_claim=c.received_the_claim,
            exposure_status=c.exposure_status, result_statement=c.change_statement,
            reason=c.exposure_statement, reason_status=DisplayStatus.ok,
            breakdown_status=DisplayStatus.unavailable, origin=c.origin,
        )
        for c in (cohort_projection(x["cohort_id"]) for x in cast.COHORTS)
    )

    total = sum(c.population_represented for c in
                (cohort_projection(x["cohort_id"]) for x in cast.COHORTS))
    reached = sum(
        c.population_represented
        for c in (cohort_projection(x["cohort_id"]) for x in cast.COHORTS)
        if c.received_the_claim
    )
    ev = cast.SHARED_EVENT

    return LandscapeProjection(
        projection_version=PROJECTION_VERSION,
        wording_version=WORDING_VERSION,
        run_integration=RUN_INTEGRATION,
        scenario_id_note=SCENARIO_ID_NOTE,
        claim=_claim(),
        source_statement=(
            "Everyone below received the same words, from the same source, at the same moment."
        ),
        people=people, organisations=organisations, cohorts=cohorts,
        population_total=total, population_reached=reached,
        population_not_reached=total - reached,
        exposure_statement=(
            f"{total - reached:,} of {total:,} people never received the claim. Their views are "
            f"unchanged, which is not the same as disagreeing."
        ),
        not_modelled=NOT_MODELLED,
    )
