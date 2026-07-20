"""
Belief Formation and Divergence Slice — minimal proposition, exposure and belief-state schemas.

Canonical plan: `docs/design/BELIEF-SENTIMENT-VERTICAL-SLICE.md`.

FIVE SEPARATE LAYERS, never one scalar. Belief (what they think is true), attitude (how they
evaluate a target), emotion (immediate affect, people only), stance (position on an issue) and
behaviour propensity (what becomes more likely) are distinct structures here because collapsing them
into a single "sentiment" number is the failure this slice exists to disprove.

B5 IS ENFORCED IN THE TYPES, NOT ONLY IN VALIDATORS. Note in particular:

  - `MessageTarget` can only be constructed from a typed `fict:` identifier that resolves in the
    active world's registry, so a real person, organisation or population is not merely rejected -
    there is no field that could carry one (B5-03, B5-06).
  - No model here has a susceptibility, persuadability or priority field. An audience cannot be
    ranked because nothing to rank on exists (B5-05).
  - `Belief.credence` is bounded and `confidence` is separate, so certainty cannot be manufactured
    by moving one number (B5-08 in spirit).
  - Absence is `None`, never `0.0` (B5-08).
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ...safety.controls import (
    PERSUASION_OPTIMISATION_TERMS,
    PROHIBITED_IDENTITY_INFERENCES,
    PROTECTED_TRAIT_PROXIES,
    PROTECTED_TRAITS,
    TARGET_KINDS,
    TARGET_PREFIX,
    B5Violation,
)

# Every model in this module forbids unknown fields. B5-06's lesson from the demo endpoint: an
# ignored field is a control that silently does not fire.
_STRICT = ConfigDict(extra="forbid")


# ── Propositions ─────────────────────────────────────────────────────────────────────────────────


class PropositionKind(str, Enum):
    """Adopted unchanged from BELIEF-AND-KNOWLEDGE-MODEL section 4.2."""

    fact = "fact"
    attribution = "attribution"
    disposition = "disposition"
    evaluative = "evaluative"


class TruthValue(str, Enum):
    true = "true"
    false = "false"
    indeterminate = "indeterminate"
    not_truth_apt = "not_truth_apt"


class Proposition(BaseModel):
    """
    An identified claim. Beliefs attach to these, never to free text, so two entities' beliefs about
    the same thing are comparable and can be compared against truth at all.
    """

    model_config = _STRICT

    proposition_id: str
    kind: PropositionKind
    topic: str = Field(..., min_length=1, description="Scopes interpretive priors. Load-bearing.")
    truth_value: TruthValue = Field(..., description="AUTHORITATIVE. Engine or scenario only.")
    claim_text: str = Field(..., description="PRESENTATION ONLY. Carries no causal weight.")
    subject_entity_id: Optional[str] = None
    scenario_authored: bool = True

    @model_validator(mode="after")
    def _evaluative_is_not_truth_apt(self) -> "Proposition":
        """
        An evaluative claim has no truth value.

        This is what stops the model asserting that a population is *factually wrong* to distrust
        its government - a judgement is not a fact, and the "factually wrong" query must exclude
        these by construction rather than by remembering to filter.
        """
        if self.kind is PropositionKind.evaluative and self.truth_value is not TruthValue.not_truth_apt:
            raise ValueError(
                f"proposition '{self.proposition_id}' is evaluative, so truth_value must be "
                f"'not_truth_apt', not '{self.truth_value.value}'"
            )
        if self.kind is not PropositionKind.evaluative and self.truth_value is TruthValue.not_truth_apt:
            raise ValueError(
                f"proposition '{self.proposition_id}' is {self.kind.value}, which is truth-apt; "
                f"'not_truth_apt' is reserved for evaluative claims"
            )
        return self


# ── Targets: B5-03 and B5-06 enforced structurally ───────────────────────────────────────────────


class MessageTarget(BaseModel):
    """
    A resolved reference to an entity inside ONE fictional world.

    There is deliberately no `name`, `description` or `external_id` field. A real person or
    organisation cannot be addressed because no field exists that could carry one - B5-06 is
    satisfied by the shape of the type, not by a rejection list that must stay current.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    scenario_id: str
    kind: str
    entity_id: str

    @field_validator("kind")
    @classmethod
    def _known_kind(cls, v: str) -> str:
        if v not in TARGET_KINDS:
            raise ValueError(f"target kind '{v}' is not one of {sorted(TARGET_KINDS)}")
        return v

    @classmethod
    def parse(cls, raw: Any, *, scenario_id: str) -> "MessageTarget":
        """Parse `fict:<scenario>:<kind>:<entity>`, or fail closed."""
        if not isinstance(raw, str) or raw.count(":") != 3:
            raise B5Violation(
                "B5-03",
                f"target must be '{TARGET_PREFIX}:<scenario_id>:<kind>:<entity_id>'. "
                f"Free-text person, organisation and population targets are rejected.",
            )
        prefix, sid, kind, eid = raw.split(":")
        if prefix != TARGET_PREFIX:
            raise B5Violation(
                "B5-03",
                f"target '{raw}' lacks the fictional-world prefix '{TARGET_PREFIX}:'. Real persons, "
                f"organisations, governments and political populations cannot be addressed.",
            )
        if sid != scenario_id:
            raise B5Violation(
                "B5-03", f"target '{raw}' belongs to world '{sid}'; active world is '{scenario_id}'"
            )
        return cls(scenario_id=sid, kind=kind, entity_id=eid)

    def __str__(self) -> str:
        return f"{TARGET_PREFIX}:{self.scenario_id}:{self.kind}:{self.entity_id}"


# ── Information events and exposure ──────────────────────────────────────────────────────────────


class Channel(str, Enum):
    """Declared channels. Exposure is a property of channel membership, never of identity."""

    broadcast = "broadcast"
    workplace = "workplace"
    community = "community"
    official_briefing = "official_briefing"
    union_network = "union_network"


class InformationEvent(BaseModel):
    """
    A fictional message introduced into the world.

    NO audience-selection field exists. A message declares which channels carry it; who is exposed
    follows from declared channel membership. There is no way to express "send this to whoever is
    most persuadable" because no such field is available (B5-05).
    """

    model_config = _STRICT

    event_id: str
    proposition_id: str
    source_entity: MessageTarget = Field(..., description="Who made the claim, inside this world.")
    channels: list[Channel] = Field(..., min_length=1)
    evidence_strength: float = Field(..., ge=0.0, le=1.0, description="Declared in scenario data.")
    introduced_at_tick: int = Field(..., ge=0)


class Observation(BaseModel):
    """One entity's exposure to one event. Produced by the engine, never authored per entity."""

    model_config = _STRICT

    observation_id: str
    observer: MessageTarget
    event_id: str
    channel: Channel
    exposure_intensity: float = Field(..., ge=0.0, le=1.0)
    tick: int = Field(..., ge=0)


# ── Belief, attitude, emotion, stance, propensity ────────────────────────────────────────────────


class Belief(BaseModel):
    """
    Three separate numbers, deliberately.

    `credence` is what the holder thinks is true; `confidence` is how firmly; `salience` is whether
    they currently care. Collapsing them manufactures false certainty - a holder can be very unsure
    about something they think is probably true, and the interface must be able to say so.
    """

    model_config = _STRICT

    holder: MessageTarget
    proposition_id: str
    credence: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    salience: float = Field(..., ge=0.0, le=1.0)
    last_update_tick: Optional[int] = None
    supporting_observation_ids: list[str] = Field(default_factory=list)
    contradicting_observation_ids: list[str] = Field(default_factory=list)
    contested: bool = False

    @property
    def is_uncertain(self) -> bool:
        """
        Continued uncertainty is a FIRST-CLASS OUTCOME, not a failure to decide.

        The journalist is expected to land here: mid credence held with low confidence. The
        interface must render this as 'uncertain pending evidence', never as a weak yes or no.
        """
        return 0.35 <= self.credence <= 0.65 and self.confidence < 0.5


class AttitudeDimension(str, Enum):
    trust = "trust"
    legitimacy = "legitimacy"
    threat = "threat"
    sympathy = "sympathy"


class Attitude(BaseModel):
    """Target-specific, never a global mood. An entity may trust one source and distrust another."""

    model_config = _STRICT

    holder: MessageTarget
    target: MessageTarget
    dimension: AttitudeDimension
    value: float = Field(..., ge=0.0, le=1.0)
    last_update_tick: Optional[int] = None


class Emotion(str, Enum):
    fear = "fear"
    anger = "anger"
    anxiety = "anxiety"
    hope = "hope"
    urgency = "urgency"


class EmotionalState(BaseModel):
    """
    PEOPLE ONLY. Founder decision: organisations carry posture and risk assessment, never affect.

    These are declared scalar states in a fictional model. They are not psychological measurement
    and make no claim about real human affect; the interface must say so.
    """

    model_config = _STRICT

    holder: MessageTarget
    values: dict[Emotion, float] = Field(default_factory=dict)
    last_update_tick: Optional[int] = None

    @model_validator(mode="after")
    def _people_only_and_bounded(self) -> "EmotionalState":
        if self.holder.kind != "person":
            raise ValueError(
                f"emotion is modelled for people only; '{self.holder}' is a {self.holder.kind}. "
                f"Organisations carry posture, priorities and risk assessment instead."
            )
        for emotion, v in self.values.items():
            if not 0.0 <= v <= 1.0:
                raise ValueError(f"emotion {emotion.value} out of bounds: {v}")
        return self


class StancePosition(str, Enum):
    support = "support"
    oppose = "oppose"
    neutral = "neutral"
    uncertain = "uncertain"


class Stance(BaseModel):
    model_config = _STRICT

    holder: MessageTarget
    issue_id: str
    position: StancePosition
    intensity: float = Field(..., ge=0.0, le=1.0)
    last_update_tick: Optional[int] = None


class BehaviourAction(str, Enum):
    share = "share"
    protest = "protest"
    contact_official = "contact_official"
    withdraw_support = "withdraw_support"
    organisational_statement = "organisational_statement"
    reroute = "reroute"


class BehaviourPropensity(BaseModel):
    """
    NEVER a guaranteed action.

    Crossing `threshold` is a necessary condition, not a sufficient one - `would_act` reports only
    that the bar is met. The interface must not render a propensity as an intention.
    """

    model_config = _STRICT

    holder: MessageTarget
    action: BehaviourAction
    propensity: float = Field(..., ge=0.0, le=1.0)
    threshold: float = Field(..., ge=0.0, le=1.0)
    last_update_tick: Optional[int] = None

    @property
    def would_act(self) -> bool:
        return self.propensity >= self.threshold


# ── Organisations: posture, not affect ───────────────────────────────────────────────────────────


class OrganisationPosture(BaseModel):
    """
    What an organisation has instead of emotions.

    `internal_distribution` is the point of this model: an organisation is not of one mind, and its
    official position may differ from where its members actually sit.
    """

    model_config = _STRICT

    holder: MessageTarget
    official_position: StancePosition
    internal_distribution: dict[StancePosition, float] = Field(default_factory=dict)
    cohesion: float = Field(..., ge=0.0, le=1.0)
    risk_posture: float = Field(..., ge=0.0, le=1.0)
    objectives: list[str] = Field(default_factory=list)
    last_update_tick: Optional[int] = None

    @model_validator(mode="after")
    def _checks(self) -> "OrganisationPosture":
        if self.holder.kind != "organisation":
            raise ValueError(f"'{self.holder}' is a {self.holder.kind}, not an organisation")
        if self.internal_distribution:
            total = sum(self.internal_distribution.values())
            if abs(total - 1.0) > 1e-6:
                raise ValueError(f"internal_distribution must sum to 1.0, got {total:.6f}")
        return self


# ── B5 guard over any authored belief-slice content ──────────────────────────────────────────────

_BANNED_FIELD_NAMES = frozenset(
    {t.lower() for t in PROTECTED_TRAITS}
    | {t.lower() for t in PROTECTED_TRAIT_PROXIES}
    | {t.lower() for t in PROHIBITED_IDENTITY_INFERENCES}
    | {t.lower() for t in PERSUASION_OPTIMISATION_TERMS}
)


def assert_slice_content_permitted(payload: Any, *, path: str = "content") -> None:
    """
    B5-04 / B5-05 / B5-06 over authored scenario content for this slice.

    Applied to entity and message fixtures at load, so a protected trait or a persuadability score
    cannot enter the world through scenario data - the route the request-side controls do not cover.
    """

    def walk(node: Any, where: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if str(key).strip().lower().replace("-", "_") in _BANNED_FIELD_NAMES:
                    raise B5Violation(
                        "B5-04",
                        f"'{key}' at {where} is a protected trait, declared proxy, identity "
                        f"inference or persuasion-optimisation term, and may not appear in "
                        f"belief-slice content.",
                    )
                walk(value, f"{where}.{key}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, f"{where}[{i}]")

    walk(payload, path)
