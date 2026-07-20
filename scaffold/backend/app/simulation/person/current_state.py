"""
Virtual Person VP-2 — a bounded, deterministic current-situation model.

VP-2 answers, for a fictional person, four questions about NOW:

  - what are they currently trying to achieve?   (goals)
  - what are they responsible for?                (responsibilities)
  - what pressure are they currently under?       (pressures)
  - what currently limits their choices?          (constraints)

and: what changed those conditions? (a typed transition trace).

THE ONE RULE THAT SHAPES EVERYTHING. These are CURRENT-SITUATION data, not personality traits.

  acceptable   : "the journalist is under deadline pressure because a broadcast window is approaching"
  NOT acceptable: "the journalist is naturally anxious and therefore easier to influence"

A pressure is an active circumstance with a declared source, not a diagnosis, a weakness, a
susceptibility or a permanent emotional label. A goal is what the person is trying to achieve now,
not what "this type of person always wants". Every populated value comes from an explicit fixture, a
declared event, or a deterministic transition — never inferred from role, biography, portrait,
education, wealth, occupation or apparent age.

WHAT VP-2 DOES NOT DO. It selects no action, removes no option, scores no person, and computes no
combined motivation/stability/influence/risk number. Constraints are RECORDED; VP-3 decides how they
affect available actions. The reserved selected-action fields from VP-1 stay NOT_MODELLED.

DETERMINISM. `apply_events(state, events, rule_version)` is a pure function: same current state +
same ordered declared events + same rule version → identical updated state + identical trace. No
LLM, no RNG, no wall-clock, no network, no hidden global state. Events are applied in a declared
stable order (tick, then event_order, then event_id), never dictionary or filesystem order.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..belief.provenance import Origin

_FROZEN = ConfigDict(extra="forbid", frozen=True)

RULE_VERSION = "vp2-current-state-v1"

#: Bounded [0,1]. A contextual reading of ONE named goal / responsibility / pressure — never a
#: measure of the person. "This deadline pressure is high", never "this person is highly pressured".
Magnitude = float


class ItemStatus(str, Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"        # declared but not currently in force
    satisfied = "SATISFIED"      # goals
    resolved = "RESOLVED"        # pressures / constraints
    not_modelled = "NOT_MODELLED"


def _band(x: Optional[float]) -> str:
    """Plain-language display band. The number stays in the record; the band is what a screen shows."""
    if x is None:
        return "not recorded"
    if x < 0.34:
        return "low"
    if x < 0.67:
        return "moderate"
    return "high"


# ── The four current-situation state types (distinct, never generic key-value) ────────────────────


class Goal(BaseModel):
    """What the person is trying to achieve NOW. Not a trait, not a moral judgement, not a prediction."""

    model_config = _FROZEN

    goal_id: str
    description: str
    desired_condition: str
    #: Contextual salience of THIS goal, 0–1. Not ambition, drive, intelligence or determination.
    priority: Magnitude = Field(0.5, ge=0.0, le=1.0)
    status: ItemStatus = ItemStatus.active
    origin: Origin = Origin.fixture
    supporting_refs: tuple[str, ...] = ()
    start_tick: Optional[int] = None
    update_reason: Optional[str] = None

    @property
    def priority_band(self) -> str:
        return _band(self.priority)


class Responsibility(BaseModel):
    """A declared obligation. Explicitly authored or activated — never derived from a role string."""

    model_config = _FROZEN

    responsibility_id: str
    obligation: str
    owed_to: str                     # institution / person / process the duty runs to
    subject: str                     # the domain it covers
    #: Contextual urgency of THIS obligation, 0–1.
    urgency: Magnitude = Field(0.5, ge=0.0, le=1.0)
    status: ItemStatus = ItemStatus.active
    origin: Origin = Origin.fixture
    supporting_refs: tuple[str, ...] = ()
    update_reason: Optional[str] = None

    @property
    def urgency_band(self) -> str:
        return _band(self.urgency)


class PressureSource(str, Enum):
    approaching_deadline = "approaching_deadline"
    missing_information = "missing_information"
    household_concern = "household_concern"
    organisational_demand = "organisational_demand"
    public_scrutiny = "public_scrutiny"
    resource_shortage = "resource_shortage"
    conflicting_obligations = "conflicting_obligations"


class Pressure(BaseModel):
    """
    An active circumstance affecting the current situation. NOT a diagnosis, a permanent emotional
    trait, instability, weakness, susceptibility or persuadability. It always names a declared source.
    """

    model_config = _FROZEN

    pressure_id: str
    description: str
    source_kind: PressureSource
    source_ref: str                  # the declared event/obligation/circumstance it comes from
    #: Contextual intensity of THIS pressure, 0–1.
    intensity: Magnitude = Field(0.5, ge=0.0, le=1.0)
    onset_tick: Optional[int] = None
    status: ItemStatus = ItemStatus.active
    origin: Origin = Origin.fixture
    update_reason: Optional[str] = None

    @property
    def intensity_band(self) -> str:
        return _band(self.intensity)


class ConstraintKind(str, Enum):
    verification_incomplete = "verification_incomplete"
    lacks_record_access = "lacks_record_access"
    legal_procedure_unmet = "legal_procedure_unmet"
    communications_window_closed = "communications_window_closed"
    resource_unavailable = "resource_unavailable"


class Constraint(BaseModel):
    """
    A current limitation. VP-2 RECORDS it. VP-3 will decide how it affects available actions —
    VP-2 removes and selects nothing.
    """

    model_config = _FROZEN

    constraint_id: str
    limitation: str
    constraint_kind: ConstraintKind
    subject: str                     # the process/action the limit bears on
    #: Declared only if it has a defined future use. Recorded, not yet acted on.
    hardness: Optional[str] = None   # "hard" | "soft"
    status: ItemStatus = ItemStatus.active
    origin: Origin = Origin.fixture
    source_ref: Optional[str] = None
    update_reason: Optional[str] = None

    @model_validator(mode="after")
    def _hardness_valid(self) -> "Constraint":
        if self.hardness is not None and self.hardness not in ("hard", "soft"):
            raise ValueError("hardness, if declared, must be 'hard' or 'soft'")
        return self


class CurrentSituation(BaseModel):
    """The four typed collections. Distinct types, never flattened into generic records."""

    model_config = _FROZEN

    goals: tuple[Goal, ...] = ()
    responsibilities: tuple[Responsibility, ...] = ()
    pressures: tuple[Pressure, ...] = ()
    constraints: tuple[Constraint, ...] = ()
    #: VP-1's reserved decision output stays untouched. VP-3 owns it.
    selected_action_status: ItemStatus = ItemStatus.not_modelled


# ── Events (a small typed set; unrestricted prose is never authoritative input) ───────────────────


class EventKind(str, Enum):
    activate_goal = "activate_goal"
    change_goal_priority = "change_goal_priority"
    satisfy_goal = "satisfy_goal"
    activate_responsibility = "activate_responsibility"
    change_responsibility_urgency = "change_responsibility_urgency"
    activate_pressure = "activate_pressure"
    change_pressure_intensity = "change_pressure_intensity"
    resolve_pressure = "resolve_pressure"
    activate_constraint = "activate_constraint"
    resolve_constraint = "resolve_constraint"


class SituationEvent(BaseModel):
    """
    A declared change to current state. Carries the item it targets and the declared magnitude/
    status change. Unknown fields fail; an invalid transition fails.

    `payload` is a typed-by-convention dict validated per kind by the kernel — kept as a mapping only
    so one event model serves ten kinds; the kernel rejects anything it does not recognise.
    """

    model_config = _FROZEN

    event_id: str
    event_kind: EventKind
    tick: int = Field(..., ge=0)
    target_id: str
    reason: str
    origin: Origin = Origin.engine
    event_order: int = 0                       # tie-break within a tick
    magnitude: Optional[float] = Field(None, ge=0.0, le=1.0)
    item: Optional[dict] = None                # full item for activation events
    supporting_refs: tuple[str, ...] = ()


# ── Trace ─────────────────────────────────────────────────────────────────────────────────────────


class TraceOutcome(str, Enum):
    activated = "ACTIVATED"
    changed = "CHANGED"
    satisfied = "SATISFIED"
    resolved = "RESOLVED"
    no_change = "NO_CHANGE"


class TransitionEntry(BaseModel):
    """One inspectable step. No-change is a real outcome, not a missing entry."""

    model_config = _FROZEN

    event_id: str
    event_kind: EventKind
    tick: int
    target_id: str
    outcome: TraceOutcome
    previous: Optional[str] = None       # previous value/status, textual
    updated: Optional[str] = None        # new value/status, textual
    rule_version: str = RULE_VERSION
    reason: str = ""
    #: FIXTURE where the starting value was authored; ENGINE where this step computed the change.
    value_origin: Origin = Origin.engine
    #: A retained value keeps its fixture origin while the ENGINE made the no-change decision.
    decision_origin: Origin = Origin.engine
    no_change_reason: Optional[str] = None
    references: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _no_change_is_explained(self) -> "TransitionEntry":
        if self.outcome is TraceOutcome.no_change and not self.no_change_reason:
            raise ValueError("a no-change outcome must state why nothing changed")
        return self


class TransitionResult(BaseModel):
    model_config = _FROZEN
    situation: CurrentSituation
    trace: tuple[TransitionEntry, ...]
    rule_version: str = RULE_VERSION


# ── The deterministic transition kernel ───────────────────────────────────────────────────────────
#
# INPUTS ARE STRUCTURALLY LIMITED to current state + ordered declared events + rule version. There is
# no parameter for name, portrait, biography, life stage, education, occupation, socioeconomic
# description or organisation prestige, and no intelligence/competence/personality field — a person
# cannot be profiled through this signature. target_id is a keyed lookup, not a trait.


def _clamp(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def _sorted(events: tuple[SituationEvent, ...]) -> list[SituationEvent]:
    """Declared stable order: tick, then event_order, then event_id. Never dict/filesystem order."""
    return sorted(events, key=lambda e: (e.tick, e.event_order, e.event_id))


def apply_events(
    situation: CurrentSituation,
    events: tuple[SituationEvent, ...],
    *,
    rule_version: str = RULE_VERSION,
) -> TransitionResult:
    """Pure. Same inputs → identical result. Applies each event, records a trace entry for every one."""
    seen: set[str] = set()
    goals = {g.goal_id: g for g in situation.goals}
    resp = {r.responsibility_id: r for r in situation.responsibilities}
    pres = {p.pressure_id: p for p in situation.pressures}
    cons = {c.constraint_id: c for c in situation.constraints}
    trace: list[TransitionEntry] = []

    for ev in _sorted(events):
        if ev.event_id in seen:
            raise ValueError(f"duplicate event id '{ev.event_id}'")
        seen.add(ev.event_id)
        k = ev.event_kind
        entry = dict(event_id=ev.event_id, event_kind=k, tick=ev.tick,
                     target_id=ev.target_id, reason=ev.reason, references=ev.supporting_refs)

        if k is EventKind.activate_goal:
            if ev.item is None:
                raise ValueError(f"{ev.event_id}: activate_goal needs an item")
            g = Goal(**{**ev.item, "goal_id": ev.target_id, "origin": Origin.engine})
            goals[ev.target_id] = g
            trace.append(TransitionEntry(outcome=TraceOutcome.activated, updated=f"goal active p={g.priority:.2f}", **entry))
        elif k is EventKind.change_goal_priority:
            g = _require(goals, ev.target_id, "goal")
            new = _clamp(ev.magnitude if ev.magnitude is not None else g.priority)
            goals[ev.target_id] = g.model_copy(update={"priority": new, "origin": Origin.engine, "update_reason": ev.reason})
            trace.append(TransitionEntry(outcome=TraceOutcome.changed, previous=f"{g.priority:.2f}", updated=f"{new:.2f}",
                         value_origin=g.origin, **entry))
        elif k is EventKind.satisfy_goal:
            g = _require(goals, ev.target_id, "goal")
            goals[ev.target_id] = g.model_copy(update={"status": ItemStatus.satisfied, "origin": Origin.engine, "update_reason": ev.reason})
            trace.append(TransitionEntry(outcome=TraceOutcome.satisfied, previous=g.status.value, updated="SATISFIED",
                         value_origin=g.origin, **entry))

        elif k is EventKind.activate_responsibility:
            if ev.item is None:
                raise ValueError(f"{ev.event_id}: activate_responsibility needs an item")
            r = Responsibility(**{**ev.item, "responsibility_id": ev.target_id, "origin": Origin.engine})
            resp[ev.target_id] = r
            trace.append(TransitionEntry(outcome=TraceOutcome.activated, updated=f"responsibility active u={r.urgency:.2f}", **entry))
        elif k is EventKind.change_responsibility_urgency:
            r = _require(resp, ev.target_id, "responsibility")
            new = _clamp(ev.magnitude if ev.magnitude is not None else r.urgency)
            resp[ev.target_id] = r.model_copy(update={"urgency": new, "origin": Origin.engine, "update_reason": ev.reason})
            trace.append(TransitionEntry(outcome=TraceOutcome.changed, previous=f"{r.urgency:.2f}", updated=f"{new:.2f}",
                         value_origin=r.origin, **entry))

        elif k is EventKind.activate_pressure:
            if ev.item is None:
                raise ValueError(f"{ev.event_id}: activate_pressure needs an item")
            p = Pressure(**{**ev.item, "pressure_id": ev.target_id, "origin": Origin.engine})
            pres[ev.target_id] = p
            trace.append(TransitionEntry(outcome=TraceOutcome.activated, updated=f"pressure active i={p.intensity:.2f}", **entry))
        elif k is EventKind.change_pressure_intensity:
            p = _require(pres, ev.target_id, "pressure")
            new = _clamp(ev.magnitude if ev.magnitude is not None else p.intensity)
            if new == p.intensity:
                trace.append(TransitionEntry(outcome=TraceOutcome.no_change, previous=f"{p.intensity:.2f}", updated=f"{new:.2f}",
                             value_origin=p.origin, no_change_reason="intensity unchanged by this event", **entry))
            else:
                pres[ev.target_id] = p.model_copy(update={"intensity": new, "origin": Origin.engine, "update_reason": ev.reason})
                trace.append(TransitionEntry(outcome=TraceOutcome.changed, previous=f"{p.intensity:.2f}", updated=f"{new:.2f}",
                             value_origin=p.origin, **entry))
        elif k is EventKind.resolve_pressure:
            p = _require(pres, ev.target_id, "pressure")
            pres[ev.target_id] = p.model_copy(update={"status": ItemStatus.resolved, "origin": Origin.engine, "update_reason": ev.reason})
            trace.append(TransitionEntry(outcome=TraceOutcome.resolved, previous=p.status.value, updated="RESOLVED",
                         value_origin=p.origin, **entry))

        elif k is EventKind.activate_constraint:
            if ev.item is None:
                raise ValueError(f"{ev.event_id}: activate_constraint needs an item")
            c = Constraint(**{**ev.item, "constraint_id": ev.target_id, "origin": Origin.engine})
            cons[ev.target_id] = c
            trace.append(TransitionEntry(outcome=TraceOutcome.activated, updated="constraint active", **entry))
        elif k is EventKind.resolve_constraint:
            c = _require(cons, ev.target_id, "constraint")
            cons[ev.target_id] = c.model_copy(update={"status": ItemStatus.resolved, "origin": Origin.engine, "update_reason": ev.reason})
            trace.append(TransitionEntry(outcome=TraceOutcome.resolved, previous=c.status.value, updated="RESOLVED",
                         value_origin=c.origin, **entry))
        else:  # pragma: no cover - EventKind is exhaustive
            raise ValueError(f"unhandled event kind {k}")

    updated = CurrentSituation(
        goals=tuple(goals[k] for k in sorted(goals)),
        responsibilities=tuple(resp[k] for k in sorted(resp)),
        pressures=tuple(pres[k] for k in sorted(pres)),
        constraints=tuple(cons[k] for k in sorted(cons)),
        selected_action_status=situation.selected_action_status,   # stays NOT_MODELLED
    )
    return TransitionResult(situation=updated, trace=tuple(trace), rule_version=rule_version)


def _require(store: dict, key: str, kind: str):
    if key not in store:
        raise ValueError(f"event targets unknown {kind} '{key}'")
    return store[key]
