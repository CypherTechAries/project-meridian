"""The authoritative state transition boundary — Phase 0 item P0.4.

Every accepted change to authoritative state passes through `TransitionService.apply`. Nothing
else may write to an `AuthoritativeState`.

WHAT THIS IS NOT — read before naming anything in here.
------------------------------------------------------
This is **not** an event store, **not** event sourcing, **not** a replay system and **not** a
causal reconstruction system. It applies one validated transition to one state object and returns
the result. `TransitionRecord` is a return value, not a persisted log entry: nothing is written to
a database, nothing survives the process, and no transition can be re-applied to rebuild state.
Those are P0.6.

VALIDATION HONESTY
------------------
`validate` performs STRUCTURAL validation only — is the transition well-formed, is the type known,
do the referenced targets exist, does the state version match, is the tick sane. It does NOT
implement legality, authority, resource, fiscal or feasibility checking. Those do not exist
anywhere in MERIDIAN (publication blocker B1), and this module must not be described as though
they do. Unimplemented policy validation is enumerated in `UNIMPLEMENTED_VALIDATION`.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

from .state import AcceptedAction, AuthoritativeState

# The P0.5 chain scalars the boundary will accept, and their declared bounds. Listing them here
# rather than deriving them by reflection means a new field cannot become writable by accident.
_CHAIN_BOUNDED_01: frozenset[str] = frozenset({
    "incident_severity",
    "insurer_risk",
    "premium_pressure",
    "rerouting_level",
    "port_activity_deficit",
    "employment_pressure",
    "household_expectation_pressure",
    "narrative_attention",
    "collective_activity",
    "political_pressure",
})
_CHAIN_NON_NEGATIVE_INT: frozenset[str] = frozenset({"rerouting_ticks_committed"})
_CHAIN_SCALARS: frozenset[str] = _CHAIN_BOUNDED_01 | _CHAIN_NON_NEGATIVE_INT

# Fields whose prior-tick value a lagged mechanism may read.
_CHAIN_LAGGED_FIELDS: tuple[str, ...] = tuple(sorted(_CHAIN_BOUNDED_01))

_OPTION_STATUSES: frozenset[str] = frozenset({"AVAILABLE", "CONSTRAINED", "ENABLED"})

# Policy validation that deliberately does NOT exist after P0.4. Enumerated in code so it cannot
# be quietly forgotten, and so a reader of this module is told what it does not do.
UNIMPLEMENTED_VALIDATION: tuple[str, ...] = (
    "legality — no rule evaluates whether an action is permitted (blocker B1)",
    "authority — no check that the actor holds the power to act (ORGANISATION-MODEL M-AUTH, unbuilt)",
    "resource/fiscal — no engine action touches fiscal state; no treasury path exists",
    "feasibility — no capability, capacity or logistics model exists",
    "temporal — Intervention.timeline_days is never read; effects apply immediately",
    "scenario constraints — proven causally inert by substitution (A3 check 3)",
)


class TransitionType(str, Enum):
    """The closed set of authoritative changes the engine can currently make.

    Closed deliberately: an unknown type is rejected rather than applied, so a new mutation path
    cannot appear without being declared here.
    """

    ADVANCE_TICK = "advance_tick"
    APPLY_MACRO_DELTAS = "apply_macro_deltas"
    SET_COHORT_BELIEF = "set_cohort_belief"
    SET_NARRATIVE_ADOPTION = "set_narrative_adoption"
    RECORD_PLAYER_DECISION = "record_player_decision"
    # --- P0.5 causal slice ---
    APPLY_INCIDENT = "apply_incident"
    SET_CHAIN_SCALAR = "set_chain_scalar"
    SET_COHORT_CONCERN = "set_cohort_concern"
    SET_OPTION_STATUS = "set_option_status"
    SNAPSHOT_CHAIN_PREVIOUS = "snapshot_chain_previous"
    # --- Kestral Consequence Slice v0.2 ---
    # Declared here because the type set is closed on purpose: a decision cannot reach state
    # through a path that was never named. Consequences themselves still flow through the
    # EXISTING types above (set_chain_scalar, set_cohort_concern) - there is no second pathway.
    QUEUE_PLAYER_DECISION = "queue_player_decision"
    CONSUME_PLAYER_DECISION = "consume_player_decision"
    SPEND_GOVERNMENT_RESOURCE = "spend_government_resource"
    SCHEDULE_DELAYED_EFFECT = "schedule_delayed_effect"
    RETIRE_DELAYED_EFFECT = "retire_delayed_effect"


class TransitionOrigin(str, Enum):
    """Who or what proposed this transition.

    `LLM_PROPOSAL` records that a model *proposed* the action. It never means a model wrote
    state: the engine owns the magnitude via its effects table, and the proposal's own parameters
    are not trusted. `PRESENTATION` is present so that any attempt to mutate from a read path is
    visible and rejectable, not so that it is permitted.
    """

    ENGINE_RULE = "engine_rule"
    LLM_PROPOSAL = "llm_proposal"
    PLAYER_DECISION = "player_decision"
    PRESENTATION = "presentation"
    # An input arriving from outside the simulation, e.g. a scenario-authored incident. Recorded
    # distinctly so that "the world did this to us" is never confused with "a rule did this".
    EXTERNAL_INPUT = "external_input"


class Transition(BaseModel):
    """A structured, validated-on-entry request to change authoritative state."""

    type: TransitionType
    origin: TransitionOrigin
    payload: dict[str, Any] = Field(default_factory=dict)
    # Optimistic-concurrency guard. When supplied it must match the state's current version.
    expected_state_revision: Optional[int] = None
    # Attribution, where the engine can currently supply it. Often a table name rather than a
    # modelled mechanism — recorded as whatever is true.
    mechanism: Optional[str] = None
    actor: Optional[str] = None
    # Keyed draw references (P0.4A). Each identifies a draw precisely enough to reproduce it.
    draw_refs: list[str] = Field(default_factory=list)
    # Mechanism version, so a transition records WHICH version of a rule produced it.
    mechanism_version: Optional[str] = None
    # P0.6 groundwork: the transition ids this one causally follows from. Recording a parent is
    # NOT causal reconstruction and NOT event sourcing - nothing replays from these.
    causal_parents: list[str] = Field(default_factory=list)
    # Which authoritative fields this transition read to decide its effect.
    source_fields: list[str] = Field(default_factory=list)


class ValidationResult(BaseModel):
    ok: bool
    errors: list[str] = Field(default_factory=list)
    # Checks deliberately not performed, echoed per-transition so a caller inspecting a result
    # cannot mistake structural acceptance for policy approval.
    unimplemented: tuple[str, ...] = UNIMPLEMENTED_VALIDATION


class TransitionRecord(BaseModel):
    """The outcome of one attempted transition. A return value, NOT a persisted event."""

    transition_id: str
    type: TransitionType
    origin: TransitionOrigin
    applied: bool
    validation: ValidationResult
    tick: int
    state_revision_before: int
    state_revision_after: int
    # Field-level before/after for what actually changed. Empty when nothing changed.
    delta: dict[str, Any] = Field(default_factory=dict)
    mechanism: Optional[str] = None
    mechanism_version: Optional[str] = None
    actor: Optional[str] = None
    draw_refs: list[str] = Field(default_factory=list)
    causal_parents: list[str] = Field(default_factory=list)
    source_fields: list[str] = Field(default_factory=list)


class TransitionService:
    """The sole writer of authoritative state.

    Holds one `AuthoritativeState` and applies transitions to it. Mutation is in place on the
    held object; `TransitionRecord.delta` carries the before/after. A copy-on-write variant is
    deliberately not implemented — that decision belongs with P0.6 snapshots.
    """

    def __init__(self, state: AuthoritativeState) -> None:
        self._state = state
        self._counter = 0

    @property
    def state(self) -> AuthoritativeState:
        """Read access. Callers must treat this as read-only and must not mutate it.

        Python cannot enforce that on a Pydantic model without freezing it, which would break
        in-place application here. Enforcement is therefore by test, not by the type system —
        see `test_state_transitions.py`. This is recorded as a known limitation, not a guarantee.
        """
        return self._state

    def _next_id(self) -> str:
        self._counter += 1
        return f"txn-{self._state.tick}-{self._counter:04d}"

    # ------------------------------------------------------------------ #
    # Validation — structural only.
    # ------------------------------------------------------------------ #
    def validate(self, transition: Transition) -> ValidationResult:
        errors: list[str] = []
        s = self._state

        if transition.type not in set(TransitionType):
            errors.append(f"unknown transition type: {transition.type!r}")

        if transition.origin is TransitionOrigin.PRESENTATION:
            # A read path must never mutate authoritative state.
            errors.append("presentation origin may not mutate authoritative state")

        if (
            transition.expected_state_revision is not None
            and transition.expected_state_revision != s.state_revision
        ):
            errors.append(
                f"state version mismatch: expected {transition.expected_state_revision}, "
                f"actual {s.state_revision}"
            )

        p = transition.payload
        t = transition.type

        if t is TransitionType.APPLY_MACRO_DELTAS:
            deltas = p.get("deltas")
            if not isinstance(deltas, dict):
                errors.append("apply_macro_deltas requires a 'deltas' mapping")
            else:
                ind = s.macro.indicators
                for key, value in deltas.items():
                    if not hasattr(ind, key):
                        # Previously a silent skip. A misspelled indicator produced no error,
                        # no warning and no effect (audit sub-finding). Now it is a rejection.
                        errors.append(f"unknown macro indicator: {key!r}")
                    elif not isinstance(getattr(ind, key), (int, float)):
                        errors.append(f"macro indicator is not a top-level scalar: {key!r}")
                    elif not isinstance(value, (int, float)):
                        errors.append(f"delta for {key!r} is not numeric")

        elif t is TransitionType.SET_COHORT_BELIEF:
            cid = p.get("cohort_id")
            belief = p.get("belief")
            if cid not in s.cohorts:
                errors.append(f"unknown cohort: {cid!r}")
            elif belief not in s.cohorts[cid].beliefs:
                errors.append(f"unknown belief {belief!r} for cohort {cid!r}")
            if not isinstance(p.get("value"), (int, float)):
                errors.append("set_cohort_belief requires a numeric 'value'")

        elif t is TransitionType.SET_NARRATIVE_ADOPTION:
            adoption = p.get("adoption")
            if not isinstance(adoption, dict):
                errors.append("set_narrative_adoption requires an 'adoption' mapping")
            else:
                for cid in adoption:
                    if cid not in s.cohorts:
                        errors.append(f"adoption references unknown cohort: {cid!r}")

        elif t is TransitionType.RECORD_PLAYER_DECISION:
            if not p.get("action_id"):
                errors.append("record_player_decision requires 'action_id'")

        elif t is TransitionType.ADVANCE_TICK:
            if p and "to" in p and p["to"] != s.tick + 1:
                errors.append("advance_tick may only advance by exactly one tick")

        # ------------------------------------------------------------------ #
        # P0.5 causal slice. Every chain scalar is bounded 0..1 by construction, so an
        # out-of-range value is a rule-pack bug and is rejected rather than clamped silently.
        # ------------------------------------------------------------------ #
        elif t is TransitionType.APPLY_INCIDENT:
            sev = p.get("severity")
            if not isinstance(sev, (int, float)):
                errors.append("apply_incident requires a numeric 'severity'")
            elif not (0.0 <= sev <= 1.0):
                errors.append(f"incident severity out of bounds [0,1]: {sev}")
            if transition.origin is not TransitionOrigin.EXTERNAL_INPUT:
                errors.append("an incident may only arrive as EXTERNAL_INPUT")

        elif t is TransitionType.SET_CHAIN_SCALAR:
            field = p.get("field")
            value = p.get("value")
            if field not in _CHAIN_SCALARS:
                errors.append(f"unknown chain scalar: {field!r}")
            elif not isinstance(value, (int, float)):
                errors.append(f"chain scalar {field!r} requires a numeric value")
            elif field in _CHAIN_BOUNDED_01 and not (0.0 <= value <= 1.0):
                errors.append(f"chain scalar {field!r} out of declared bounds [0,1]: {value}")
            elif field in _CHAIN_NON_NEGATIVE_INT and (value < 0 or int(value) != value):
                errors.append(f"chain scalar {field!r} must be a non-negative integer: {value}")

        elif t is TransitionType.QUEUE_PLAYER_DECISION:
            from .decisions import DECLARED_OPTIONS
            sid, oid = p.get("submission_id"), p.get("option_id")
            if not isinstance(sid, str) or not sid:
                errors.append("queue_player_decision requires a submission_id")
            if oid not in DECLARED_OPTIONS:
                errors.append(f"unknown or unavailable option: {oid!r}")
            if isinstance(sid, str) and sid in s.consumed_submissions:
                errors.append(f"submission {sid!r} has already been consumed")
            if isinstance(sid, str) and any(q.submission_id == sid for q in s.decision_queue):
                errors.append(f"submission {sid!r} is already queued")

        elif t is TransitionType.CONSUME_PLAYER_DECISION:
            sid = p.get("submission_id")
            if not any(q.submission_id == sid for q in s.decision_queue):
                errors.append(f"submission {sid!r} is not queued and cannot be consumed")
            if sid in s.consumed_submissions:
                errors.append(f"submission {sid!r} has already been consumed")

        elif t is TransitionType.SPEND_GOVERNMENT_RESOURCE:
            field, amount = p.get("field"), p.get("amount")
            if field not in {"budget_reserve_m", "political_capital"}:
                errors.append(f"unknown government resource: {field!r}")
            elif not isinstance(amount, (int, float)) or amount < 0:
                errors.append("spend_government_resource requires a non-negative amount")
            elif amount > getattr(s.government, field):
                errors.append(
                    f"cannot spend {amount} of {field}: only {getattr(s.government, field)} held"
                )

        elif t is TransitionType.SCHEDULE_DELAYED_EFFECT:
            if not isinstance(p.get("due_tick"), int) or p["due_tick"] <= s.tick:
                errors.append("schedule_delayed_effect requires a due_tick in the future")
            if p.get("field") not in _CHAIN_SCALARS:
                errors.append(f"unknown chain scalar for delayed effect: {p.get('field')!r}")

        elif t is TransitionType.RETIRE_DELAYED_EFFECT:
            if not isinstance(p.get("index"), int):
                errors.append("retire_delayed_effect requires an index")

        elif t is TransitionType.SET_COHORT_CONCERN:
            cid = p.get("cohort_id")
            value = p.get("value")
            if cid not in s.cohorts:
                errors.append(f"unknown cohort: {cid!r}")
            if not isinstance(value, (int, float)):
                errors.append("set_cohort_concern requires a numeric 'value'")
            elif not (0.0 <= value <= 1.0):
                errors.append(f"cohort concern out of bounds [0,1]: {value}")

        elif t is TransitionType.SET_OPTION_STATUS:
            if not p.get("option_id"):
                errors.append("set_option_status requires 'option_id'")
            if p.get("status") not in _OPTION_STATUSES:
                errors.append(f"unknown option status: {p.get('status')!r}")

        elif t is TransitionType.SNAPSHOT_CHAIN_PREVIOUS:
            pass  # bookkeeping; no payload

        return ValidationResult(ok=not errors, errors=errors)

    # ------------------------------------------------------------------ #
    # Application.
    # ------------------------------------------------------------------ #
    def apply(self, transition: Transition) -> TransitionRecord:
        """Validate and, if valid, apply. A rejected transition leaves state untouched."""
        s = self._state
        before_version = s.state_revision
        result = self.validate(transition)

        if not result.ok:
            return TransitionRecord(
                transition_id=self._next_id(),
                type=transition.type,
                origin=transition.origin,
                applied=False,
                validation=result,
                tick=s.tick,
                state_revision_before=before_version,
                state_revision_after=before_version,
                mechanism=transition.mechanism,
                mechanism_version=transition.mechanism_version,
                actor=transition.actor,
                draw_refs=list(transition.draw_refs),
                causal_parents=list(transition.causal_parents),
                source_fields=list(transition.source_fields),
            )

        delta = self._apply_validated(transition)
        s.state_revision = before_version + 1

        return TransitionRecord(
            transition_id=self._next_id(),
            type=transition.type,
            origin=transition.origin,
            applied=True,
            validation=result,
            tick=s.tick,
            state_revision_before=before_version,
            state_revision_after=s.state_revision,
            delta=delta,
            mechanism=transition.mechanism,
            mechanism_version=transition.mechanism_version,
            actor=transition.actor,
            draw_refs=list(transition.draw_refs),
            causal_parents=list(transition.causal_parents),
            source_fields=list(transition.source_fields),
        )

    def _apply_validated(self, transition: Transition) -> dict[str, Any]:
        s = self._state
        p = transition.payload
        t = transition.type
        delta: dict[str, Any] = {}

        if t is TransitionType.ADVANCE_TICK:
            before = s.tick
            s.tick = before + 1
            # The macro record carries its own tick copy; kept in step here rather than by a
            # separate direct write in the engine.
            s.macro.tick = s.tick
            delta["tick"] = {"before": before, "after": s.tick}

        elif t is TransitionType.APPLY_MACRO_DELTAS:
            ind = s.macro.indicators
            bounded = {
                "government_approval",
                "military_readiness",
                "social_stability_index",
                "shipping_throughput_pct_of_baseline",
            }
            for key, value in p["deltas"].items():
                current = getattr(ind, key)
                updated = current + value
                if key in bounded:
                    updated = max(0.0, min(1.0, updated))
                elif key == "fuel_reserve_days":
                    updated = max(0.0, updated)
                setattr(ind, key, updated)
                delta[f"macro.{key}"] = {"before": current, "after": updated}

        elif t is TransitionType.SET_COHORT_BELIEF:
            cid, belief, value = p["cohort_id"], p["belief"], float(p["value"])
            before = s.cohorts[cid].beliefs[belief]
            s.cohorts[cid].beliefs[belief] = value
            delta[f"cohorts.{cid}.{belief}"] = {"before": before, "after": value}

        elif t is TransitionType.SET_NARRATIVE_ADOPTION:
            before = dict(s.narrative_adoption)
            s.narrative_adoption = dict(p["adoption"])
            changed = {
                k: {"before": before.get(k), "after": v}
                for k, v in s.narrative_adoption.items()
                if before.get(k) != v
            }
            if changed:
                delta["narrative_adoption"] = changed

        elif t is TransitionType.RECORD_PLAYER_DECISION:
            action = AcceptedAction(
                action_id=str(p["action_id"]),
                actor_role=str(p.get("actor_role", "")),
                action_type=str(p.get("action_type", "")),
                recorded_at_tick=s.tick,
                applied=False,  # nothing applies these; see AcceptedAction docstring
                client_supplied=dict(p.get("client_supplied", {})),
            )
            s.pending_actions.append(action)
            delta["pending_actions"] = {
                "added": action.action_id,
                "count_after": len(s.pending_actions),
            }

        # ------------------------------------------------------------------ #
        # P0.5 causal slice
        # ------------------------------------------------------------------ #
        elif t is TransitionType.APPLY_INCIDENT:
            before_sev = s.chain.incident_severity
            before_act = s.chain.incident_active
            # An incident REINFORCES rather than replaces: a second incident while one is live
            # raises severity toward the new level rather than resetting it.
            s.chain.incident_severity = max(before_sev, float(p["severity"]))
            s.chain.incident_active = True
            delta["chain.incident_severity"] = {"before": before_sev, "after": s.chain.incident_severity}
            delta["chain.incident_active"] = {"before": before_act, "after": True}

        elif t is TransitionType.SET_CHAIN_SCALAR:
            field, value = p["field"], p["value"]
            before = getattr(s.chain, field)
            setattr(s.chain, field, type(before)(value) if isinstance(before, int) and not isinstance(before, bool) else float(value))
            delta[f"chain.{field}"] = {"before": before, "after": getattr(s.chain, field)}

        elif t is TransitionType.QUEUE_PLAYER_DECISION:
            from .state import QueuedDecision
            q = QueuedDecision(
                submission_id=p["submission_id"],
                option_id=p["option_id"],
                submitted_tick=s.tick,
                apply_at_tick=int(p.get("apply_at_tick", s.tick + 1)),
            )
            s.decision_queue = [*s.decision_queue, q]
            delta["decision_queue"] = {"before": len(s.decision_queue) - 1, "after": len(s.decision_queue)}

        elif t is TransitionType.CONSUME_PLAYER_DECISION:
            sid = p["submission_id"]
            s.decision_queue = [q for q in s.decision_queue if q.submission_id != sid]
            s.consumed_submissions = [*s.consumed_submissions, sid]
            delta["consumed_submissions"] = {"before": None, "after": sid}

        elif t is TransitionType.SPEND_GOVERNMENT_RESOURCE:
            field, amount = p["field"], float(p["amount"])
            before = getattr(s.government, field)
            setattr(s.government, field, round(before - amount, 6))
            delta[f"government.{field}"] = {"before": before, "after": getattr(s.government, field)}

        elif t is TransitionType.SCHEDULE_DELAYED_EFFECT:
            from .state import DelayedEffect
            e = DelayedEffect(
                due_tick=int(p["due_tick"]), kind=str(p.get("kind", "chain_scalar")),
                field=str(p["field"]), value=float(p["value"]),
                cause_submission_id=str(p["cause_submission_id"]), why=str(p.get("why", "")),
            )
            s.delayed_effects = [*s.delayed_effects, e]
            delta["delayed_effects"] = {"before": len(s.delayed_effects) - 1, "after": len(s.delayed_effects)}

        elif t is TransitionType.RETIRE_DELAYED_EFFECT:
            idx = int(p["index"])
            remaining = [e for i, e in enumerate(s.delayed_effects) if i != idx]
            delta["delayed_effects"] = {"before": len(s.delayed_effects), "after": len(remaining)}
            s.delayed_effects = remaining

        elif t is TransitionType.SET_COHORT_CONCERN:
            cid, value = p["cohort_id"], float(p["value"])
            before = s.cohorts[cid].economic_concern
            s.cohorts[cid].economic_concern = value
            delta[f"cohorts.{cid}.economic_concern"] = {"before": before, "after": value}

        elif t is TransitionType.SET_OPTION_STATUS:
            oid, status = p["option_id"], p["status"]
            before = s.chain.government_options.get(oid)
            s.chain.government_options[oid] = status
            delta[f"chain.government_options.{oid}"] = {"before": before, "after": status}

        elif t is TransitionType.SNAPSHOT_CHAIN_PREVIOUS:
            # Record this tick's values so next tick's lagged mechanisms read a recorded prior
            # value rather than depending on stage ordering.
            s.chain.previous = {f: float(getattr(s.chain, f)) for f in _CHAIN_LAGGED_FIELDS}
            delta["chain.previous"] = {"snapshot_at_tick": s.tick}

        return delta
