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
    # P0.4A hook. Deterministic draw references are not available: there are no named substreams,
    # so a draw cannot yet be identified or reproduced independently of global stream position.
    draw_refs: list[str] = Field(default_factory=list)


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
    actor: Optional[str] = None


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
                actor=transition.actor,
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
            actor=transition.actor,
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

        return delta
