"""
Virtual Person VP-4 — typed relationships and ordered, append-only history.

VP-4 RECORDS. It does not cause. It represents declared fictional relationships and ordered,
append-only records of information exposure and belief observations, so a person's connections and
what they received and believed can be inspected — without any of it changing behaviour.

CLAIM BOUNDARY (repeat wherever history is shown):

    Virtual Person History v0.1 records declared fictional relationships, information exposure and
    belief observations in a deterministic, ordered and inspectable form. It does not model a
    complete life history, social network or psychological trajectory.

WHAT VP-4 DOES NOT DO. No relationship influences behaviour. No social transmission between people.
No changing trust, decay, reputation or source-learning. No memory model — history is an engine audit
record, not recall. No API route, no LLM, no UI. No VP-3 action is executed. Relationship and history
data cannot alter VP-2 transitions, VP-3 decisions or belief outputs — proven by test.

HISTORY IS APPEND-ONLY. Every append preserves prior entries byte-for-byte, rejects duplicate ids,
enforces stable ordering (tick, event_order, id) and returns a NEW immutable history plus a trace of
the decision. There is no update or delete. Correction, if ever needed, is a future explicit
correction entry — not implemented here.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

from ..belief.classification import BeliefOutcome
from ..belief.provenance import Origin
from .schema import RelationshipType, resolve_person_ref

_FROZEN = ConfigDict(extra="forbid", frozen=True)

HISTORY_VERSION = "vp4-history-v0.1"

CLAIM_BOUNDARY = (
    "Virtual Person History v0.1 records declared fictional relationships, information exposure and "
    "belief observations in a deterministic, ordered and inspectable form. It does not model a "
    "complete life history, social network or psychological trajectory."
)

#: Which relationship kinds are directional (source → target). colleague is symmetric via a
#: documented normalisation; family carries no implied direction or role.
DIRECTIONAL = frozenset({RelationshipType.reports_to, RelationshipType.member_of,
                         RelationshipType.represents, RelationshipType.receives_from,
                         RelationshipType.trusts_for})
SYMMETRIC = frozenset({RelationshipType.colleague})
UNDIRECTED = frozenset({RelationshipType.family})


class LifecycleStatus(str, Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"       # the declared relationship is no longer active — NOT hostility/distrust
    unknown = "UNKNOWN"
    unavailable = "UNAVAILABLE"
    not_modelled = "NOT_MODELLED"


# ── Relationships ─────────────────────────────────────────────────────────────────────────────────


class RelationshipEdge(BaseModel):
    """
    A declared fictional connection. NOT a numerical measure of one person's power over another —
    there is no influence, trust, strength, closeness, susceptibility, persuadability or loyalty
    score of any kind. `trusts_for` must name a subject; a numeric trust value is never added.
    """

    model_config = _FROZEN

    relationship_id: str
    source_ref: str
    target_ref: str
    relationship_kind: RelationshipType
    subject: Optional[str] = None
    status: LifecycleStatus = LifecycleStatus.active
    start_tick: Optional[int] = None
    end_tick: Optional[int] = None
    origin: Origin = Origin.fixture
    supporting_refs: tuple[str, ...] = ()
    description: str = ""
    #: True only for an engine-normalised reverse edge, never a fixture-authored one.
    reverse_of: Optional[str] = None

    @model_validator(mode="after")
    def _valid(self) -> "RelationshipEdge":
        if self.relationship_kind is RelationshipType.trusts_for and not (self.subject or "").strip():
            raise ValueError(
                "trusts_for must be scoped to a proposition/subject/domain/verification/source "
                "process; a missing subject is invalid, not UNKNOWN"
            )
        if self.reverse_of is not None and self.origin is not Origin.engine:
            raise ValueError("a normalised reverse edge must be engine-derived (ENGINE)")
        return self


class RelationshipEventKind(str, Enum):
    activated = "activated"
    deactivated = "deactivated"


class RelationshipHistoryEntry(BaseModel):
    model_config = _FROZEN

    history_entry_id: str
    relationship_id: str
    tick: int
    event_order: int = 0
    event_kind: RelationshipEventKind
    previous_status: LifecycleStatus
    new_status: LifecycleStatus
    origin: Origin = Origin.engine
    reason: str = ""
    supporting_refs: tuple[str, ...] = ()


# ── Information ───────────────────────────────────────────────────────────────────────────────────


class ExposureStatus(str, Enum):
    received = "RECEIVED"
    #: "Not received through tick N" — a time-bounded observation, NOT rejected/ignored/disbelieved/
    #: opposed/unavailable-in-the-world. A later record may show subsequent receipt.
    not_received_through_tick = "NOT_RECEIVED_THROUGH_TICK"
    unknown = "UNKNOWN"
    unavailable = "UNAVAILABLE"
    not_modelled = "NOT_MODELLED"


class InformationRecord(BaseModel):
    """A declared exposure fact or engine-recorded receipt. Absence is first-class, never inferred."""

    model_config = _FROZEN

    information_record_id: str
    person_ref: str
    proposition_ref: str
    source_ref: Optional[str] = None
    channel: Optional[str] = None
    tick: int
    event_order: int = 0
    exposure_status: ExposureStatus
    #: REQUIRED for NOT_RECEIVED_THROUGH_TICK. No permanent NEVER_RECEIVED without a time boundary.
    through_tick: Optional[int] = None
    origin: Origin = Origin.fixture
    supporting_refs: tuple[str, ...] = ()
    description: str = ""
    evidence_ref: Optional[str] = None

    @model_validator(mode="after")
    def _valid(self) -> "InformationRecord":
        if self.exposure_status is ExposureStatus.not_received_through_tick:
            if self.through_tick is None:
                raise ValueError("NOT_RECEIVED_THROUGH_TICK requires a through_tick time boundary")
            # a not-received record must itself have evidence or a fixture origin — never silently derived
            if self.origin not in (Origin.fixture, Origin.engine) and not (self.evidence_ref or self.supporting_refs):
                raise ValueError("a NOT_RECEIVED_THROUGH_TICK record needs evidence or fixture origin")
        resolve_person_ref(self.person_ref)   # typed fictional id; cross-world / free text rejected
        return self


# ── Belief history ────────────────────────────────────────────────────────────────────────────────


# BeliefOutcome is the CANONICAL enum from the belief package — VP-4 defines no second
# outcome vocabulary. Re-exported so existing imports keep working.


class BeliefHistoryEntry(BaseModel):
    """
    One observation of belief state, reusing the existing belief slice's values and vocabulary — VP-4
    computes no belief of its own and changes no frozen value.
    """

    model_config = _FROZEN

    belief_history_entry_id: str
    person_ref: str
    proposition_ref: str
    tick: int
    event_order: int = 0
    previous_state: Optional[str] = None
    retained_prior_ref: Optional[str] = None
    updated_state: Optional[str] = None
    classification: BeliefOutcome
    confidence_status: str = "UNAVAILABLE"
    exposure_ref: Optional[str] = None
    update_trace_ref: Optional[str] = None
    value_origin: Origin = Origin.engine
    decision_origin: Origin = Origin.engine
    supporting_refs: tuple[str, ...] = ()
    no_update_reason: Optional[str] = None
    #: Honesty disclosures carried on every belief observation.
    result_kind: str = "packaged-belief-snapshot"
    connected_to_authoritative_run: bool = False
    observation_count: int = 1
    trajectory_available: bool = False

    @model_validator(mode="after")
    def _valid(self) -> "BeliefHistoryEntry":
        resolve_person_ref(self.person_ref)
        if self.trajectory_available and self.observation_count < 2:
            raise ValueError("a trajectory needs at least two observations")
        if self.classification in (BeliefOutcome.never_received_through_tick, BeliefOutcome.retained_prior):
            # never-received / retained-prior implies NO belief update happened
            if self.updated_state is not None and self.updated_state != self.previous_state:
                raise ValueError("a not-received/retained-prior observation must not carry a belief update")
        return self


# ── Append-only histories ─────────────────────────────────────────────────────────────────────────


class AppendTrace(BaseModel):
    model_config = _FROZEN
    accepted: bool
    entry_id: str
    position: int
    reason: str
    history_version: str = HISTORY_VERSION


def _append(entries: tuple, entry, *, id_attr: str, sort_key, conflict=None):
    """
    Generic pure append. Preserves prior entries byte-for-byte, rejects duplicate ids, keeps stable
    order, runs an optional conflict check, and returns (new_tuple, AppendTrace).
    """
    ids = {getattr(e, id_attr) for e in entries}
    if getattr(entry, id_attr) in ids:
        raise ValueError(f"duplicate history id '{getattr(entry, id_attr)}'")
    if conflict is not None:
        conflict(entries, entry)
    combined = tuple(sorted((*entries, entry), key=sort_key))
    pos = combined.index(entry)
    return combined, AppendTrace(accepted=True, entry_id=getattr(entry, id_attr), position=pos,
                                 reason="appended; prior entries preserved and re-sorted stably")


def _info_conflict(entries: tuple[InformationRecord, ...], new: InformationRecord) -> None:
    for e in entries:
        if (e.person_ref == new.person_ref and e.proposition_ref == new.proposition_ref
                and e.tick == new.tick and e.event_order == new.event_order
                and e.exposure_status != new.exposure_status):
            raise ValueError(
                f"conflicting information records at tick {new.tick}: "
                f"{e.exposure_status.value} vs {new.exposure_status.value} (no reconciliation rule)"
            )


class RelationshipHistory(BaseModel):
    model_config = _FROZEN
    entries: tuple[RelationshipHistoryEntry, ...] = ()

    def append(self, entry: RelationshipHistoryEntry) -> tuple["RelationshipHistory", AppendTrace]:
        new, trace = _append(self.entries, entry, id_attr="history_entry_id",
                             sort_key=lambda e: (e.tick, e.event_order, e.history_entry_id))
        return RelationshipHistory(entries=new), trace


class InformationHistory(BaseModel):
    model_config = _FROZEN
    entries: tuple[InformationRecord, ...] = ()

    def append(self, entry: InformationRecord) -> tuple["InformationHistory", AppendTrace]:
        new, trace = _append(self.entries, entry, id_attr="information_record_id",
                             sort_key=lambda e: (e.tick, e.event_order, e.information_record_id),
                             conflict=_info_conflict)
        return InformationHistory(entries=new), trace

    @property
    def observation_count(self) -> int:
        return len(self.entries)


class BeliefHistory(BaseModel):
    model_config = _FROZEN
    entries: tuple[BeliefHistoryEntry, ...] = ()

    def append(self, entry: BeliefHistoryEntry) -> tuple["BeliefHistory", AppendTrace]:
        new, trace = _append(self.entries, entry, id_attr="belief_history_entry_id",
                             sort_key=lambda e: (e.tick, e.event_order, e.belief_history_entry_id))
        return BeliefHistory(entries=new), trace

    @property
    def observation_count(self) -> int:
        return len(self.entries)

    @property
    def trajectory_available(self) -> bool:
        return len(self.entries) >= 2   # one observation is never a trajectory

    def summary_sentence(self) -> str:
        n = len(self.entries)
        if n == 1:
            return ("MERIDIAN has one recorded belief update for this proposition. It does not yet "
                    "have enough history to describe a longer-term pattern.")
        if n == 0:
            return "MERIDIAN has no recorded belief update for this proposition."
        return f"MERIDIAN has {n} recorded belief observations for this proposition."
