"""
Virtual Person VP-3 — deterministic action selection and decision trace.

Given a declared current situation and a declared set of fictional options, VP-3 selects one
available option and explains the selection. It SELECTS; it never EXECUTES.

CLAIM BOUNDARY (repeat wherever a decision is shown):

    Virtual Person Decision Rule v0.1 is a deterministic mechanism for comparing declared fictional
    options against declared goals, responsibilities, pressures and constraints. It is not a
    complete model or prediction of human decision-making.

A selected option means "the declared rule ranked this option highest under these declared inputs."
It does not mean the option is objectively best, that every similar person would choose it, or
anything about intelligence, competence, morality or free will. Every result carries
`execution_status = NOT_EXECUTED`.

THE INPUT BOUNDARY, AND A REPORTED GAP.
VP-1 defined `DecisionInputs` carrying string *refs* as placeholders. The comparison formula needs
the actual magnitudes those refs point at (a goal's priority, a pressure's intensity) plus each
option's declared contributions. Rather than reach around the boundary by passing a whole
`VirtualPerson`, VP-3 takes a `DecisionRequest` that carries the concrete VP-2 engine-state items —
Goals, Responsibilities, Pressures, Constraints — and the ActionOptions. It has NO field for name,
portrait, biography, role, occupation, education, socioeconomic description, life stage, community or
prestige. `subject_ref` exists only to stamp the returned record and is never read by the scoring
rule. Two different people with identical requests get identical results.

WHAT VP-3 DOES NOT DO. No execution, no world-state/belief/relationship consequences, no event
emission into any run, no history (VP-4), no relationships-with-effect, no API route, no LLM, no UI.
It compares options for ONE fictional person; it never ranks people, chooses audiences, optimises
persuasion or accepts a real-person target.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..belief.provenance import Origin
from .current_state import Constraint, Goal, ItemStatus, Pressure, Responsibility

_FROZEN = ConfigDict(extra="forbid", frozen=True)

RULE_VERSION = "vp3-decision-rule-v0.1"
TIE_BREAK_RULE = "lowest action_id (lexicographic)"

CLAIM_BOUNDARY = (
    "Virtual Person Decision Rule v0.1 is a deterministic mechanism for comparing declared fictional "
    "options against declared goals, responsibilities, pressures and constraints. It is not a "
    "complete model or prediction of human decision-making."
)

#: What the decision does NOT mean. Returned on every result so a score cannot be misread.
DECISION_MODEL_BOUNDARY: tuple[str, ...] = (
    "not a probability the person will choose this",
    "not a likelihood of success",
    "not moral value or policy quality",
    "not intelligence or competence",
    "not overall motivation or person quality",
    "not comparable across unrelated decisions",
)


# ── Contributions (distinct typed records; every value explicitly declared) ───────────────────────


class GoalContribution(BaseModel):
    """How well an option supports or conflicts with one NAMED current goal. Not a person measure."""

    model_config = _FROZEN
    goal_id: str
    alignment: float = Field(..., ge=-1.0, le=1.0)
    rationale: str
    origin: Origin = Origin.fixture
    references: tuple[str, ...] = ()


class ResponsibilityContribution(BaseModel):
    """How well an option supports or conflicts with one NAMED obligation."""

    model_config = _FROZEN
    responsibility_id: str
    alignment: float = Field(..., ge=-1.0, le=1.0)
    rationale: str
    origin: Origin = Origin.fixture
    references: tuple[str, ...] = ()


class PressureResponse(BaseModel):
    """
    How an option is declared to respond to one NAMED current pressure. NOT resilience, emotional
    stability, susceptibility or a general ability to cope.
    """

    model_config = _FROZEN
    pressure_id: str
    response: float = Field(..., ge=-1.0, le=1.0)
    rationale: str
    origin: Origin = Origin.fixture
    references: tuple[str, ...] = ()


class ConstraintRequirement(BaseModel):
    """
    An option's relationship to one NAMED constraint. If it is blocked while the constraint is
    active, the option is UNAVAILABLE (hard). A soft penalty, if declared, is explicit and bounded.
    """

    model_config = _FROZEN
    constraint_id: str
    blocked_while_active: bool
    soft_penalty: Optional[float] = Field(None, ge=0.0, le=1.0)
    rationale: str
    origin: Origin = Origin.fixture
    references: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _hard_has_no_soft_penalty(self) -> "ConstraintRequirement":
        if self.blocked_while_active and self.soft_penalty is not None:
            raise ValueError("a hard-blocking requirement must not also declare a soft penalty")
        return self


# ── Option ────────────────────────────────────────────────────────────────────────────────────────


class ActionOption(BaseModel):
    """
    An authored fictional option. Its declared contributions are COMPARISON INPUTS, not predicted
    consequences. Not an executable instruction; unrestricted prose is never accepted as one.
    """

    model_config = _FROZEN

    action_id: str
    label: str
    description: str
    origin: Origin = Origin.fixture
    supporting_refs: tuple[str, ...] = ()
    goal_contributions: tuple[GoalContribution, ...] = ()
    responsibility_contributions: tuple[ResponsibilityContribution, ...] = ()
    pressure_responses: tuple[PressureResponse, ...] = ()
    constraint_requirements: tuple[ConstraintRequirement, ...] = ()
    display_order: Optional[int] = None


# ── Kernel input (identity-free) ──────────────────────────────────────────────────────────────────


class DecisionRequest(BaseModel):
    """
    Everything the decision rule may read. The concrete realization of VP-1 `DecisionInputs`: it
    carries the actual VP-2 engine-state items the refs pointed at, plus the options. It has NO
    identity field. `subject_ref` only labels the returned record and is never read by scoring.
    """

    model_config = _FROZEN

    decision_id: str
    goals: tuple[Goal, ...] = ()
    responsibilities: tuple[Responsibility, ...] = ()
    pressures: tuple[Pressure, ...] = ()
    constraints: tuple[Constraint, ...] = ()
    options: tuple[ActionOption, ...] = ()
    #: Only to associate the returned record with a person; never an input to the comparison.
    subject_ref: Optional[str] = None


# ── Trace + result ────────────────────────────────────────────────────────────────────────────────


class ComponentProduct(BaseModel):
    """One (magnitude × declared value) term, shown so the total can be re-derived by eye."""

    model_config = _FROZEN
    item_id: str
    magnitude: float
    declared_value: float
    product: float
    rationale: str


class OptionComparison(BaseModel):
    model_config = _FROZEN

    action_id: str
    available: bool
    blocking_constraints: tuple[str, ...] = ()
    goal_products: tuple[ComponentProduct, ...] = ()
    responsibility_products: tuple[ComponentProduct, ...] = ()
    pressure_products: tuple[ComponentProduct, ...] = ()
    soft_penalties: tuple[ComponentProduct, ...] = ()
    goal_component: Optional[float] = None
    responsibility_component: Optional[float] = None
    pressure_component: Optional[float] = None
    soft_penalty_total: Optional[float] = None
    #: None when unavailable — an unavailable option is NOT scored zero.
    total: Optional[float] = None
    origin: Origin = Origin.engine
    references: tuple[str, ...] = ()


class DecisionStatus(str, Enum):
    selected_not_executed = "SELECTED_NOT_EXECUTED"
    no_available_action = "NO_AVAILABLE_ACTION"
    insufficient_inputs = "INSUFFICIENT_INPUTS"
    not_modelled = "NOT_MODELLED"


class ExecutionStatus(str, Enum):
    not_executed = "NOT_EXECUTED"   # the only value VP-3 ever produces


class DecisionResult(BaseModel):
    model_config = _FROZEN

    decision_id: str
    rule_version: str = RULE_VERSION
    status: DecisionStatus
    considered_options: tuple[str, ...]
    available_options: tuple[str, ...]
    unavailable_options: tuple[str, ...]
    selected_action_id: Optional[str]
    execution_status: ExecutionStatus = ExecutionStatus.not_executed
    comparisons: tuple[OptionComparison, ...]
    tie_occurred: bool = False
    tie_break_rule: Optional[str] = None
    origin: Origin = Origin.engine
    subject_ref: Optional[str] = None
    supporting_refs: tuple[str, ...] = ()
    explanation: str = ""
    claim_boundary: str = CLAIM_BOUNDARY
    model_boundary: tuple[str, ...] = DECISION_MODEL_BOUNDARY

    @model_validator(mode="after")
    def _selection_is_never_executed(self) -> "DecisionResult":
        if self.execution_status is not ExecutionStatus.not_executed:
            raise ValueError("VP-3 selects but never executes; execution_status must be NOT_EXECUTED")
        if self.status is DecisionStatus.no_available_action and self.selected_action_id is not None:
            raise ValueError("no available action means no selected action")
        if self.status is DecisionStatus.selected_not_executed and self.selected_action_id is None:
            raise ValueError("a selection status must name a selected action")
        return self


# ── The deterministic decision kernel ─────────────────────────────────────────────────────────────


def select_action(request: DecisionRequest, *, rule_version: str = RULE_VERSION) -> DecisionResult:
    """
    Pure. Same request → identical result. Reads ONLY the request; identity cannot enter.

    Availability is decided before ranking: an option blocked by an ACTIVE constraint it declares
    blocked_while_active is UNAVAILABLE and is not scored. Available options are scored by the
    versioned formula; the highest total wins, ties broken by lowest action_id.
    """
    goals = {g.goal_id: g for g in request.goals}
    resp = {r.responsibility_id: r for r in request.responsibilities}
    pres = {p.pressure_id: p for p in request.pressures}
    cons = {c.constraint_id: c for c in request.constraints}

    comparisons: list[OptionComparison] = []

    for opt in request.options:
        # -- validate references (unknown reference fails, never silently ignored) --------------
        for gc in opt.goal_contributions:
            if gc.goal_id not in goals:
                raise ValueError(f"{opt.action_id}: unknown goal reference '{gc.goal_id}'")
        for rc in opt.responsibility_contributions:
            if rc.responsibility_id not in resp:
                raise ValueError(f"{opt.action_id}: unknown responsibility reference '{rc.responsibility_id}'")
        for pr in opt.pressure_responses:
            if pr.pressure_id not in pres:
                raise ValueError(f"{opt.action_id}: unknown pressure reference '{pr.pressure_id}'")
        for cr in opt.constraint_requirements:
            if cr.constraint_id not in cons:
                raise ValueError(f"{opt.action_id}: unknown constraint reference '{cr.constraint_id}'")

        # -- availability (hard constraints, evaluated first) -----------------------------------
        blocking = tuple(sorted(
            cr.constraint_id for cr in opt.constraint_requirements
            if cr.blocked_while_active and cons[cr.constraint_id].status is ItemStatus.active
        ))
        if blocking:
            comparisons.append(OptionComparison(
                action_id=opt.action_id, available=False, blocking_constraints=blocking,
                total=None))   # unavailable → not scored, not zero
            continue

        # -- score (only declared contributions; missing is absent, not fabricated zero) --------
        gp = tuple(ComponentProduct(item_id=gc.goal_id, magnitude=goals[gc.goal_id].priority,
                   declared_value=gc.alignment, product=goals[gc.goal_id].priority * gc.alignment,
                   rationale=gc.rationale) for gc in opt.goal_contributions)
        rp = tuple(ComponentProduct(item_id=rc.responsibility_id, magnitude=resp[rc.responsibility_id].urgency,
                   declared_value=rc.alignment, product=resp[rc.responsibility_id].urgency * rc.alignment,
                   rationale=rc.rationale) for rc in opt.responsibility_contributions)
        pp = tuple(ComponentProduct(item_id=pr.pressure_id, magnitude=pres[pr.pressure_id].intensity,
                   declared_value=pr.response, product=pres[pr.pressure_id].intensity * pr.response,
                   rationale=pr.rationale) for pr in opt.pressure_responses)
        sp = tuple(ComponentProduct(item_id=cr.constraint_id, magnitude=1.0,
                   declared_value=cr.soft_penalty, product=cr.soft_penalty, rationale=cr.rationale)
                   for cr in opt.constraint_requirements
                   if cr.soft_penalty is not None and cons[cr.constraint_id].status is ItemStatus.active)

        goal_c = round(sum(x.product for x in gp), 12)
        resp_c = round(sum(x.product for x in rp), 12)
        pres_c = round(sum(x.product for x in pp), 12)
        soft_t = round(sum(x.product for x in sp), 12)
        total = round(goal_c + resp_c + pres_c - soft_t, 12)

        comparisons.append(OptionComparison(
            action_id=opt.action_id, available=True, goal_products=gp, responsibility_products=rp,
            pressure_products=pp, soft_penalties=sp, goal_component=goal_c,
            responsibility_component=resp_c, pressure_component=pres_c, soft_penalty_total=soft_t,
            total=total))

    considered = tuple(o.action_id for o in request.options)
    available = tuple(c.action_id for c in comparisons if c.available)
    unavailable = tuple(c.action_id for c in comparisons if not c.available)

    if not available:
        return DecisionResult(
            decision_id=request.decision_id, status=DecisionStatus.no_available_action,
            considered_options=considered, available_options=(), unavailable_options=unavailable,
            selected_action_id=None, comparisons=tuple(comparisons), subject_ref=request.subject_ref,
            explanation=_explain(None, comparisons, request), )

    # -- rank: highest total, tie-break by lowest action_id --------------------------------------
    ranked = sorted(((c.total, c.action_id) for c in comparisons if c.available),
                    key=lambda t: (-t[0], t[1]))
    best_total = ranked[0][0]
    tied = [aid for tot, aid in ranked if tot == best_total]
    tie = len(tied) > 1
    selected = min(tied)   # documented stable tie-break

    return DecisionResult(
        decision_id=request.decision_id, status=DecisionStatus.selected_not_executed,
        considered_options=considered, available_options=available, unavailable_options=unavailable,
        selected_action_id=selected, comparisons=tuple(comparisons),
        tie_occurred=tie, tie_break_rule=TIE_BREAK_RULE if tie else None,
        subject_ref=request.subject_ref, explanation=_explain(selected, comparisons, request), )


def _explain(selected: Optional[str], comparisons: tuple[OptionComparison, ...],
             request: DecisionRequest) -> str:
    """
    Deterministic from structured state. No per-character authored sentence. At most three reasons.
    Never references personality, profession-as-capability, intelligence or emotion.
    """
    labels = {o.action_id: o.label for o in request.options}
    if selected is None:
        blocked = [f"'{labels[c.action_id]}' was unavailable ({', '.join(c.blocking_constraints)})"
                   for c in comparisons if not c.available]
        return ("No option was available. " + "; ".join(blocked[:3]) + ". Nothing was executed.").strip()

    comp = next(c for c in comparisons if c.action_id == selected)
    reasons: list[str] = []
    top_goal = max(comp.goal_products, key=lambda x: x.product, default=None)
    if top_goal and top_goal.product > 0:
        g = next(g for g in request.goals if g.goal_id == top_goal.item_id)
        reasons.append(f"it best supported the goal to {g.description}")
    top_resp = max(comp.responsibility_products, key=lambda x: x.product, default=None)
    if top_resp and top_resp.product > 0:
        r = next(r for r in request.responsibilities if r.responsibility_id == top_resp.item_id)
        reasons.append(f"the responsibility to {r.obligation}")
    blocked = [labels[c.action_id] for c in comparisons if not c.available]
    parts = [f"The person selected '{labels[selected]}'"]
    if reasons:
        parts.append("because " + " and ".join(reasons[:3]))
    text = " ".join(parts) + "."
    if blocked:
        text += f" '{blocked[0]}' was unavailable because a required condition was not met."
    text += " Nothing was executed."
    return text
