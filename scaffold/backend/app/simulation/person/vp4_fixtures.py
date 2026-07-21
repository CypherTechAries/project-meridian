"""
VP-4 fixture slice — minimal declared relationships and history for the three fictional people.

No rich social networks, no interpersonal friendship/family/trust links unless authored. Only a few
organisational or process relationships, plus information and belief-history records ADAPTED from the
existing belief slice — the frozen belief values are reused, never recomputed.
"""

from __future__ import annotations

from ..belief import cast
from ..belief.projection import person_projection
from ..belief.provenance import Origin
from .history import (
    BeliefHistory,
    BeliefHistoryEntry,
    BeliefOutcome,
    ExposureStatus,
    InformationHistory,
    InformationRecord,
    LifecycleStatus,
    RelationshipEdge,
)
from .schema import RelationshipType

SID = cast.SCENARIO_ID
CLAIM = "P-WARNINGS-IGNORED"
EV = cast.SHARED_EVENT


def _pid(p: str) -> str:
    return f"fict:{SID}:person:{p}"


def _oid(o: str) -> str:
    return f"fict:{SID}:organisation:{o}"


# ── Relationships (organisational / process only, all FIXTURE) ────────────────────────────────────

RELATIONSHIPS: tuple[RelationshipEdge, ...] = (
    RelationshipEdge(relationship_id="rel-spokesperson-represents", relationship_kind=RelationshipType.represents,
        source_ref=_pid("family-spokesperson"), target_ref="fict:kestral-strait:group:affected-families",
        description="represents affected families", origin=Origin.fixture),
    RelationshipEdge(relationship_id="rel-minister-member", relationship_kind=RelationshipType.member_of,
        source_ref=_pid("government-minister"), target_ref=_oid("national-government"),
        description="member of the national government", origin=Origin.fixture),
    RelationshipEdge(relationship_id="rel-journalist-member", relationship_kind=RelationshipType.member_of,
        source_ref=_pid("broadcast-journalist"), target_ref=_oid("public-broadcaster"),
        description="reports for Northshore Public Broadcast", origin=Origin.fixture),
    RelationshipEdge(relationship_id="rel-journalist-receives", relationship_kind=RelationshipType.receives_from,
        source_ref=_pid("broadcast-journalist"), target_ref="fict:kestral-strait:process:broadcaster-verification",
        description="receives information from the broadcaster's verification process", origin=Origin.fixture),
    # a scoped trust, bound to a declared subject — never a numeric or general trust
    RelationshipEdge(relationship_id="rel-journalist-trusts-verification", relationship_kind=RelationshipType.trusts_for,
        source_ref=_pid("broadcast-journalist"), target_ref="fict:kestral-strait:process:broadcaster-verification",
        subject="corroboration of a factual allegation before publication",
        description="trusts the verification process for corroboration decisions", origin=Origin.fixture),
)


# ── Information records (adapted from the belief exposure slice) ───────────────────────────────────


def information_history_for(person_id: str) -> InformationHistory:
    """One received record per exposed person, grounded in the existing exposure evidence."""
    exposure = next((e for e in cast.EXPOSURES if e["entity_id"] == person_id), None)
    hist = InformationHistory()
    if exposure is not None:
        rec = InformationRecord(
            information_record_id=f"info-{person_id}-{EV['event_id']}",
            person_ref=_pid(person_id), proposition_ref=CLAIM,
            source_ref=f"fict:{SID}:person:family-spokesperson", channel=exposure["channel"],
            tick=EV["introduced_at_tick"], exposure_status=ExposureStatus.received,
            origin=Origin.fixture, description=f"received the allegation via {exposure['path']}",
            evidence_ref="cast.EXPOSURES", supporting_refs=(EV["event_id"],))
        hist, _ = hist.append(rec)
    return hist


def _classify(person_id: str) -> tuple[BeliefOutcome, str]:
    """Classify the existing first-order result using proposition-level belief semantics only."""
    proj = person_projection(person_id)
    if not proj.received_the_claim:
        return BeliefOutcome.retained_prior, "prior carried forward; not exposed"
    if proj.still_unsure:
        return BeliefOutcome.received_but_unsure, "in the uncertain band with low confidence"
    c = proj.calculation.final_credence
    if c > 0.65:
        return BeliefOutcome.received_and_accepted, "moved above the uncertain band"
    if c < 0.35:
        return BeliefOutcome.received_and_rejected, "moved below the uncertain band"
    return BeliefOutcome.received_but_unsure, "remained within the uncertain band"


def belief_history_for(person_id: str) -> BeliefHistory:
    """One belief observation per person, reusing the frozen belief value. observation_count = 1."""
    proj = person_projection(person_id)
    outcome, note = _classify(person_id)
    hist = BeliefHistory()
    entry = BeliefHistoryEntry(
        belief_history_entry_id=f"bh-{person_id}-{CLAIM}",
        person_ref=_pid(person_id), proposition_ref=CLAIM, tick=EV["introduced_at_tick"],
        previous_state=proj.view_before, updated_state=proj.view_now,
        classification=outcome, confidence_status="ENGINE",
        exposure_ref=f"info-{person_id}-{EV['event_id']}",
        update_trace_ref=f"belief-projection:{person_id}:{CLAIM}",
        value_origin=Origin.engine, decision_origin=Origin.engine,
        supporting_refs=(note,), observation_count=1, trajectory_available=False)
    hist, _ = hist.append(entry)
    return hist


PEOPLE = ("family-spokesperson", "government-minister", "broadcast-journalist")
