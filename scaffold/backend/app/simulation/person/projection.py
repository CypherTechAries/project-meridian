"""
Virtual Person VP-5 — read-only projection layer.

Composes the implemented VP-1..VP-4 records into typed response shapes. It COMPOSES; it never
recomputes. No belief is re-derived, no option is re-scored, no history is re-sorted, no fixture or
engine structure is mutated.

CLAIM BOUNDARY (returned on every response):

    The Virtual Person API exposes deterministic fictional fixture information, current-situation
    state, option comparisons, selected-but-unexecuted decisions, declared relationships and bounded
    history records. It does not expose a complete psychological model or live authoritative person
    state.

RUN INTEGRATION. This material is NOT connected to authoritative live simulation state. Every
response carries `result_kind: "packaged-virtual-person-snapshot"` and
`connected_to_authoritative_run: false`. It must never be described as live person state, current
authoritative person, persisted person memory, executed decision history or real-time society state.

PARITY IS THE POINT. Current situation comes from the VP-2 fixtures, decisions from `select_action`,
relationships and histories from the VP-4 records, belief classification from the ONE canonical
classifier. If this layer ever disagreed with those, the disagreement would be the bug.

HOW THE DECISION IS OBTAINED — the exact behaviour, stated plainly:

    The dossier decision is deterministically derived from the packaged VP-2 situation and VP-3
    option fixtures when the read model is assembled. It is not persisted live person state and
    nothing has been executed.

The projection CALLS the canonical `select_action` over the frozen packaged fixtures. It holds no
second scoring rule, no copy of the formula and no cached decision. Because both the situation and
the options are frozen, the derivation is deterministic — the same assembly always yields the same
result — but the result is computed at read time, not stored by a living person.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

from ..belief.classification import BeliefOutcome
from ..belief.projection import SCENARIO_ID_NOTE
from ..belief.provenance import Origin
from .current_state import CurrentSituation, ItemStatus
from .decision import CLAIM_BOUNDARY as DECISION_CLAIM_BOUNDARY
from .decision import DecisionResult, select_action
from .history import CLAIM_BOUNDARY as HISTORY_CLAIM_BOUNDARY
from .history import BeliefHistory, InformationHistory, LifecycleStatus, RelationshipEdge
from .history import DIRECTIONAL, SYMMETRIC, UNDIRECTED
from .schema import NOT_MODELLED_LAYERS as NOT_MODELLED, from_cast, resolve_person_ref
from .vp2_fixtures import fixture_for
from .vp3_decisions import FIXTURE_DECISIONS
from .vp4_fixtures import PEOPLE, RELATIONSHIPS, belief_history_for, information_history_for

_FROZEN = ConfigDict(extra="forbid", frozen=True)

PROJECTION_VERSION = "virtual-person-projection-v0.1"

CLAIM_BOUNDARY = (
    "The Virtual Person API exposes deterministic fictional fixture information, current-situation "
    "state, option comparisons, selected-but-unexecuted decisions, declared relationships and "
    "bounded history records. It does not expose a complete psychological model or live "
    "authoritative person state."
)

RUN_INTEGRATION = {
    "result_kind": "packaged-virtual-person-snapshot",
    "connected_to_authoritative_run": False,
    "execution_status": "NOT_EXECUTED",
    "explanation": (
        "Composed on request from frozen packaged fixtures and deterministic rules. This is not "
        "live person state, not a current authoritative person, not persisted person memory, not "
        "executed decision history and not real-time society state. No simulation run is read, "
        "advanced or written."
    ),
    "scenario_id_note": SCENARIO_ID_NOTE,
}


class LayerStatus(str, Enum):
    """Whether a layer is present, modelled-but-empty, unknown, unavailable or not modelled."""

    modelled_and_empty = "MODELLED_AND_EMPTY"
    unknown = "UNKNOWN"
    unavailable = "UNAVAILABLE"
    not_modelled = "NOT_MODELLED"
    present = "PRESENT"


# ── Shared display helpers (deterministic, template-driven — never per-person prose) ──────────────


def _direction_of(kind) -> str:
    if kind in DIRECTIONAL:
        return "directional (source to target)"
    if kind in SYMMETRIC:
        return "symmetric by documented normalisation"
    if kind in UNDIRECTED:
        return "no implied direction or role"
    return "unspecified"


def _situation_sentence(sit: CurrentSituation) -> str:
    """Composed from typed fields only. No hard-coded per-person sentence exists anywhere."""
    goal = next((g for g in sit.goals if g.status is ItemStatus.active), None)
    pressure = next((p for p in sit.pressures if p.status is ItemStatus.active), None)
    constraint = next((c for c in sit.constraints if c.status is ItemStatus.active), None)
    parts = []
    if goal:
        parts.append(f"is trying to {goal.description}")
    if pressure:
        parts.append(f"while {pressure.description} keeps pressure {pressure.intensity_band}")
    if constraint:
        parts.append(f"and {constraint.limitation}")
    return ("The person " + ", ".join(parts) + ".") if parts else "No current situation is recorded."


def _history_sentence(bh: BeliefHistory) -> str:
    return bh.summary_sentence()


def _relationship_sentence(edge: RelationshipEdge) -> str:
    base = edge.description or f"{edge.relationship_kind.value} {edge.target_ref}"
    if edge.relationship_kind.value == "receives_from":
        return (f"{base}. This does not mean every report from that source is believed, or that "
                f"any particular message was received.")
    if edge.relationship_kind.value == "trusts_for":
        return f"{base}, for: {edge.subject}. Trust is scoped to that subject only."
    return base


# ── Response models ───────────────────────────────────────────────────────────────────────────────


class RosterItem(BaseModel):
    model_config = _FROZEN

    person_ref: str
    display_name: str
    portrait_ref: Optional[str] = None
    role: Optional[str] = None
    organisation_ref: Optional[str] = None
    community_ref: Optional[str] = None
    current_situation_summary: str
    goal_count: int
    responsibility_count: int
    active_pressure_count: int
    active_constraint_count: int
    latest_decision_status: str
    selected_action_label: Optional[str]
    execution_status: str = "NOT_EXECUTED"
    relationship_count: int
    information_observation_count: int
    belief_observation_count: int
    trajectory_available: bool
    identity_origin: Origin = Origin.fixture
    result_kind: str = "packaged-virtual-person-snapshot"
    connected_to_authoritative_run: bool = False


class Roster(BaseModel):
    model_config = _FROZEN
    projection_version: str = PROJECTION_VERSION
    claim_boundary: str = CLAIM_BOUNDARY
    run_integration: dict = RUN_INTEGRATION
    people: tuple[RosterItem, ...]
    model_boundary: tuple[str, ...] = NOT_MODELLED
    #: Declaration order is preserved. The roster is never sorted by any person property.
    ordering: str = "declaration order; never ranked"


class IdentitySection(BaseModel):
    model_config = _FROZEN
    person_ref: str
    display_name: str
    portrait_ref: Optional[str] = None
    life_stage: Optional[str] = None
    role: Optional[str] = None
    organisation_ref: Optional[str] = None
    community_ref: Optional[str] = None
    biography: Optional[str] = None
    origin: Origin = Origin.fixture


class SituationItem(BaseModel):
    model_config = _FROZEN
    item_id: str
    description: str
    value: Optional[float] = None
    band: Optional[str] = None
    status: str
    origin: Origin
    references: tuple[str, ...] = ()
    update_reason: Optional[str] = None


class CurrentSituationSection(BaseModel):
    model_config = _FROZEN
    summary: str
    goals: tuple[SituationItem, ...]
    responsibilities: tuple[SituationItem, ...]
    pressures: tuple[SituationItem, ...]
    constraints: tuple[SituationItem, ...]
    state_status: str
    layer_status: str = LayerStatus.present.value


class DecisionSection(BaseModel):
    model_config = _FROZEN
    decision_id: str
    considered_options: tuple[str, ...]
    available_options: tuple[str, ...]
    unavailable_options: tuple[str, ...]
    #: Declared display label for every considered option id, so a reader is never shown a raw
    #: identifier such as "a-publish-now" where a readable option name belongs. Copied from the
    #: VP-3 request; nothing is invented here.
    option_labels: dict
    blocking_constraints: dict
    selected_action_id: Optional[str]
    selected_action_label: Optional[str]
    execution_status: str
    default_statement: str = "Selected by the declared rule. Not executed."
    explanation: str
    tie_occurred: bool
    tie_break_rule: Optional[str]
    claim_boundary: str = DECISION_CLAIM_BOUNDARY
    #: Exact scores live here only — never in default display text, never as probabilities.
    decision_trace: dict


class RelationshipItem(BaseModel):
    model_config = _FROZEN
    relationship_id: str
    source_ref: str
    target_ref: str
    relationship_kind: str
    subject: Optional[str] = None
    status: LifecycleStatus
    direction: str
    origin: Origin
    references: tuple[str, ...] = ()
    description: str


class InformationItem(BaseModel):
    model_config = _FROZEN
    information_record_id: str
    proposition_ref: str
    exposure_status: str
    tick: int
    through_tick: Optional[int] = None
    source_ref: Optional[str] = None
    channel: Optional[str] = None
    evidence_ref: Optional[str] = None
    origin: Origin
    description: str


class BeliefObservation(BaseModel):
    model_config = _FROZEN
    belief_history_entry_id: str
    proposition_ref: str
    tick: int
    before: Optional[str]
    after: Optional[str]
    classification: BeliefOutcome
    confidence_status: str
    exposure_ref: Optional[str]
    update_trace_ref: Optional[str]
    value_origin: Origin
    decision_origin: Origin
    no_update_reason: Optional[str] = None


class BeliefHistorySection(BaseModel):
    model_config = _FROZEN
    observations: tuple[BeliefObservation, ...]
    observation_count: int
    trajectory_available: bool
    trajectory_explanation: str
    claim_boundary: str = HISTORY_CLAIM_BOUNDARY


class ExplanationsSection(BaseModel):
    model_config = _FROZEN
    current_situation: str
    selected_action: str
    blocked_actions: str
    missing_information: str
    retained_beliefs: str


class Dossier(BaseModel):
    model_config = _FROZEN
    projection_version: str = PROJECTION_VERSION
    claim_boundary: str = CLAIM_BOUNDARY
    run_integration: dict = RUN_INTEGRATION
    identity: IdentitySection
    current_situation: CurrentSituationSection
    decision: DecisionSection
    relationships: tuple[RelationshipItem, ...]
    information_history: tuple[InformationItem, ...]
    belief_history: BeliefHistorySection
    explanations: ExplanationsSection
    model_boundary: tuple[str, ...] = NOT_MODELLED


# ── Builders (compose only) ───────────────────────────────────────────────────────────────────────


def _situation_items(sit: CurrentSituation) -> CurrentSituationSection:
    return CurrentSituationSection(
        summary=_situation_sentence(sit),
        goals=tuple(SituationItem(item_id=g.goal_id, description=g.description, value=g.priority,
                    band=g.priority_band, status=g.status.value, origin=g.origin,
                    references=g.supporting_refs, update_reason=g.update_reason) for g in sit.goals),
        responsibilities=tuple(SituationItem(item_id=r.responsibility_id, description=r.obligation,
                    value=r.urgency, band=r.urgency_band, status=r.status.value, origin=r.origin,
                    references=r.supporting_refs, update_reason=r.update_reason) for r in sit.responsibilities),
        pressures=tuple(SituationItem(item_id=p.pressure_id, description=p.description,
                    value=p.intensity, band=p.intensity_band, status=p.status.value, origin=p.origin,
                    references=(p.source_ref,), update_reason=p.update_reason) for p in sit.pressures),
        constraints=tuple(SituationItem(item_id=c.constraint_id, description=c.limitation,
                    value=None, band=None, status=c.status.value, origin=c.origin,
                    references=(c.source_ref,) if c.source_ref else (),
                    update_reason=c.update_reason) for c in sit.constraints),
        state_status=sit.selected_action_status.value,
    )


def _decision_section(person_id: str) -> tuple[DecisionSection, DecisionResult]:
    request = FIXTURE_DECISIONS[person_id]()
    result = select_action(request)          # VP-3 owns the rule; nothing is re-scored here
    labels = {o.action_id: o.label for o in request.options}
    blocking = {c.action_id: list(c.blocking_constraints) for c in result.comparisons if not c.available}
    section = DecisionSection(
        decision_id=result.decision_id,
        considered_options=result.considered_options,
        available_options=result.available_options,
        unavailable_options=result.unavailable_options,
        option_labels=dict(labels),
        blocking_constraints=blocking,
        selected_action_id=result.selected_action_id,
        selected_action_label=labels.get(result.selected_action_id or ""),
        execution_status=result.execution_status.value,
        explanation=result.explanation,
        tie_occurred=result.tie_occurred, tie_break_rule=result.tie_break_rule,
        decision_trace=result.model_dump(mode="json"),
    )
    return section, result


def dossier(person_id: str) -> Dossier:
    """Compose one person. Every section is copied from the owning milestone, never recomputed."""
    vp = from_cast(person_id)
    sit = fixture_for(person_id)
    decision, _ = _decision_section(person_id)
    info: InformationHistory = information_history_for(person_id)
    bh: BeliefHistory = belief_history_for(person_id)
    pref = vp.identity.person_ref.typed_id()
    rels = tuple(r for r in RELATIONSHIPS if r.source_ref == pref)

    return Dossier(
        identity=IdentitySection(
            person_ref=pref, display_name=vp.identity.display_name,
            portrait_ref=vp.identity.portrait_ref, life_stage=vp.identity.life_stage,
            role=vp.identity.role, organisation_ref=vp.identity.organisation_ref,
            community_ref=vp.identity.community_ref, biography=vp.identity.biography,
            origin=vp.identity.origin),
        current_situation=_situation_items(sit),
        decision=decision,
        relationships=tuple(RelationshipItem(
            relationship_id=r.relationship_id, source_ref=r.source_ref, target_ref=r.target_ref,
            relationship_kind=r.relationship_kind.value, subject=r.subject, status=r.status,
            direction=_direction_of(r.relationship_kind), origin=r.origin,
            references=r.supporting_refs, description=_relationship_sentence(r)) for r in rels),
        information_history=tuple(InformationItem(
            information_record_id=i.information_record_id, proposition_ref=i.proposition_ref,
            exposure_status=i.exposure_status.value, tick=i.tick, through_tick=i.through_tick,
            source_ref=i.source_ref, channel=i.channel, evidence_ref=i.evidence_ref,
            origin=i.origin, description=i.description) for i in info.entries),
        belief_history=BeliefHistorySection(
            observations=tuple(BeliefObservation(
                belief_history_entry_id=e.belief_history_entry_id, proposition_ref=e.proposition_ref,
                tick=e.tick, before=e.previous_state, after=e.updated_state,
                classification=e.classification, confidence_status=e.confidence_status,
                exposure_ref=e.exposure_ref, update_trace_ref=e.update_trace_ref,
                value_origin=e.value_origin, decision_origin=e.decision_origin,
                no_update_reason=e.no_update_reason) for e in bh.entries),
            observation_count=bh.observation_count,
            trajectory_available=bh.trajectory_available,
            trajectory_explanation=_history_sentence(bh)),
        explanations=ExplanationsSection(
            current_situation=_situation_sentence(sit),
            selected_action=decision.explanation,
            blocked_actions=(", ".join(f"{k} blocked by {', '.join(v)}"
                                       for k, v in decision.blocking_constraints.items())
                             or "no option was blocked"),
            missing_information=(", ".join(i.description for i in info.entries
                                           if i.exposure_status != "RECEIVED")
                                 or "no missing-information record"),
            retained_beliefs=_history_sentence(bh)),
    )


def roster() -> Roster:
    """All implemented people, in declaration order. Never ranked by any person property."""
    items = []
    for pid in PEOPLE:
        vp = from_cast(pid)
        sit = fixture_for(pid)
        decision, _ = _decision_section(pid)
        info = information_history_for(pid)
        bh = belief_history_for(pid)
        pref = vp.identity.person_ref.typed_id()
        items.append(RosterItem(
            person_ref=pref, display_name=vp.identity.display_name,
            portrait_ref=vp.identity.portrait_ref, role=vp.identity.role,
            organisation_ref=vp.identity.organisation_ref, community_ref=vp.identity.community_ref,
            current_situation_summary=_situation_sentence(sit),
            goal_count=len(sit.goals), responsibility_count=len(sit.responsibilities),
            active_pressure_count=sum(1 for p in sit.pressures if p.status is ItemStatus.active),
            active_constraint_count=sum(1 for c in sit.constraints if c.status is ItemStatus.active),
            latest_decision_status=decision.execution_status if decision.selected_action_id is None
                                    else "SELECTED_NOT_EXECUTED",
            selected_action_label=decision.selected_action_label,
            relationship_count=sum(1 for r in RELATIONSHIPS if r.source_ref == pref),
            information_observation_count=info.observation_count,
            belief_observation_count=bh.observation_count,
            trajectory_available=bh.trajectory_available))
    return Roster(people=tuple(items))
