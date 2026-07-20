"""
Virtual Person v0.1 — schemas, fixture identity, origins and invariants (VP-1).

FOUR LAYERS, KEPT STRUCTURALLY SEPARATE. A `VirtualPerson` has:

  1. identity        — fixture-authored descriptive context. Display only. NEVER a calculation input.
  2. state           — the TYPED SHAPE of future engine state. VP-1 populates none of it; every
                       section reports NOT_MODELLED. It must never report ENGINE before the engine
                       produces a value.
  3. explanations    — the typed container for future engine-grounded explanations. Empty in VP-1.
  4. model_boundary  — what MERIDIAN does not model, as typed values rather than one vague string.

WHY THIS FILE ADDS NO BEHAVIOUR. VP-1 answers "what is a person in the data", not "how does a person
think". There is deliberately no transition, no formula and no scoring here. Reserved collections are
empty tuples whose meaning is documented; an empty collection is not zero and is not an engine result.

VOCABULARY IS REUSED, NOT REINVENTED. Origins are the belief slice's `Origin`
(FIXTURE/ENGINE/UNKNOWN/UNAVAILABLE). Layer status uses `LayerStatus`, which reuses those four and
adds NOT_MODELLED — the one documented addition, because "the engine does not model this yet" is a
distinct claim from "unavailable" and there was no existing enum carrying all five together.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ...safety.controls import TARGET_KINDS, TARGET_PREFIX
from ..belief import cast
from ..belief.provenance import Origin

_FROZEN = ConfigDict(extra="forbid", frozen=True)

SCHEMA_VERSION = "virtual-person@0.1"


class LayerStatus(str, Enum):
    """
    Status of a value or a reserved layer.

    The first four mirror `Origin` exactly. `not_modelled` is the single documented addition: a
    reserved section that the engine does not compute yet is NOT the same as an unavailable value,
    and no existing enum carried all five.
    """

    fixture = "FIXTURE"
    engine = "ENGINE"
    unknown = "UNKNOWN"
    unavailable = "UNAVAILABLE"
    not_modelled = "NOT_MODELLED"


#: Everything VP-0.1 does not model. Typed values, not a disclaimer string. The last five are never
#: modelled at any version — the belief slice's standing prohibition carried up to the person.
NOT_MODELLED_LAYERS: tuple[str, ...] = (
    "complete lifetime history",
    "full psychology",
    "unconscious motivation",
    "unrestricted memory",
    "changing trust",
    "cumulative stress",
    "personalised feeds",
    "complete social networks",
    "intelligence",
    "competence",
    "moral worth",
    "susceptibility",
    "persuadability",
)

#: Field-name fragments that must never appear on a public Virtual Person model. A schema that ranks
#: people for influence, or scores them for susceptibility, is the exact thing B5 forbids.
PROHIBITED_FIELD_FRAGMENTS: tuple[str, ...] = (
    "intelligence", "competence", "morality", "moral_score", "susceptib", "persuad",
    "influence_rank", "influence_score", "vulnerability", "targetab", "universal_trust",
    "generic_influence", "gullib", "iq",
)

#: A future decision function may read ONLY these. Identity fields are excluded by construction.
DECISION_INPUT_FIELDS: frozenset[str] = frozenset({
    "goal_refs", "responsibility_refs", "pressure_refs", "constraint_refs",
    "information_refs", "available_action_refs",
})

#: Identity fields a decision must never receive. Enforced by `DecisionInputs` and by test.
EXCLUDED_FROM_DECISIONS: frozenset[str] = frozenset({
    "portrait_ref", "biography", "display_name", "occupation", "occupation_description",
    "education", "socioeconomic", "socioeconomic_description", "life_stage",
})


# ── Typed identifier ──────────────────────────────────────────────────────────────────────────────


class PersonRef(BaseModel):
    """
    A typed reference to a fictional person, resolved against the belief cast registry.

    Reuses the established `fict:<scenario>:person:<id>` format. Construction refuses a wrong
    scenario, a wrong kind, the legacy `agent` kind, and any id the fictional world does not declare.
    """

    model_config = _FROZEN

    scenario_id: str
    entity_id: str
    entity_kind: str = "person"

    @model_validator(mode="after")
    def _valid(self) -> "PersonRef":
        if self.entity_kind != "person":
            raise ValueError(
                f"a Virtual Person reference must be kind 'person', not '{self.entity_kind}'"
            )
        if self.entity_kind not in TARGET_KINDS:
            raise ValueError(f"'{self.entity_kind}' is not a known entity kind")
        if self.scenario_id != cast.SCENARIO_ID:
            raise ValueError(
                f"cross-world reference: '{self.scenario_id}' is not the active fictional world "
                f"'{cast.SCENARIO_ID}'"
            )
        if self.entity_id not in {p["person_id"] for p in cast.PEOPLE}:
            raise ValueError(
                f"no person '{self.entity_id}' is declared in the active fictional world"
            )
        return self

    def typed_id(self) -> str:
        return f"{TARGET_PREFIX}:{self.scenario_id}:{self.entity_kind}:{self.entity_id}"


def resolve_person_ref(typed_id: str) -> PersonRef:
    """
    Parse and validate a typed fictional person id.

    Rejects free text, cross-world ids, unknown kinds and unknown people. This is the same discipline
    as the belief read-model API, without the HTTP layer.
    """
    if not isinstance(typed_id, str):
        raise ValueError("a person id must be a typed fictional string")
    parts = typed_id.split(":")
    if len(parts) != 4 or parts[0] != TARGET_PREFIX:
        raise ValueError(
            f"person id must be '{TARGET_PREFIX}:<scenario>:person:<id>'; free text is not accepted"
        )
    _, scenario_id, kind, entity_id = parts
    return PersonRef(scenario_id=scenario_id, entity_kind=kind, entity_id=entity_id)


# ── 1 · FIXTURE IDENTITY ──────────────────────────────────────────────────────────────────────────


class FixtureIdentity(BaseModel):
    """
    Authored fictional context. DISPLAY ONLY.

    Nothing here is an input to a belief calculation, a decision, competence, intelligence, morality,
    trust or action availability. Missing descriptive fields stay `None` — never invented prose,
    never a numeric zero. `origin` is fixed at FIXTURE because every field is authored.
    """

    model_config = _FROZEN

    person_ref: PersonRef
    #: May remain the existing cast role label; a rich name is not invented to fill the schema.
    display_name: str
    #: Null until a real approved fixture asset exists. None does not invalidate a person.
    portrait_ref: Optional[str] = None
    life_stage: Optional[str] = None
    role: Optional[str] = None
    organisation_ref: Optional[str] = None
    community_ref: Optional[str] = None
    biography: Optional[str] = None
    origin: Origin = Origin.fixture

    @model_validator(mode="after")
    def _identity_is_fixture(self) -> "FixtureIdentity":
        if self.origin is not Origin.fixture:
            raise ValueError("identity is authored context and must report FIXTURE origin")
        return self


# ── 2 · ENGINE STATE (reserved shape, unpopulated in VP-1) ────────────────────────────────────────


class RelationshipType(str, Enum):
    family = "family"
    colleague = "colleague"
    reports_to = "reports_to"
    member_of = "member_of"
    represents = "represents"
    trusts_for = "trusts_for"
    receives_from = "receives_from"


class Relationship(BaseModel):
    """
    A typed fictional edge. VP-1 defines the shape and the trusts_for invariant; it computes no
    relationship effect. There is deliberately no strength/score field of any kind.
    """

    model_config = _FROZEN

    relationship_type: RelationshipType
    target: str
    #: REQUIRED for trusts_for: the declared subject, proposition, domain or process the trust is
    #: bound to. An unscoped "A trusts B" is refused at construction.
    subject: Optional[str] = None
    origin: Origin = Origin.fixture

    @model_validator(mode="after")
    def _trust_must_be_scoped(self) -> "Relationship":
        if self.relationship_type is RelationshipType.trusts_for and not (self.subject or "").strip():
            raise ValueError(
                "a trusts_for relationship must name a subject/proposition/domain/process; "
                "an unscoped general trust score is not permitted"
            )
        return self


class PersonState(BaseModel):
    """
    The TYPED SHAPE of future engine state. VP-1 populates none of it.

    Every collection is an empty tuple and `status` is NOT_MODELLED, so nothing here can be mistaken
    for an engine result. When VP-2+ implement a section it will carry real values and an ENGINE
    origin; until then it must never report ENGINE.
    """

    model_config = _FROZEN

    goals: tuple[str, ...] = ()
    responsibilities: tuple[str, ...] = ()
    pressures: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    proposition_beliefs: tuple[str, ...] = ()
    information_records: tuple[str, ...] = ()
    recent_events: tuple[str, ...] = ()
    available_actions: tuple[str, ...] = ()
    selected_actions: tuple[str, ...] = ()
    relationships: tuple[Relationship, ...] = ()
    #: The whole layer's status. Reserved-and-empty in VP-1 → NOT_MODELLED, never ENGINE.
    status: LayerStatus = LayerStatus.not_modelled

    @model_validator(mode="after")
    def _reserved_state_is_not_engine(self) -> "PersonState":
        if self.status is LayerStatus.engine:
            raise ValueError(
                "VP-1 state is a reserved shape; it must not report ENGINE before the engine "
                "produces a value"
            )
        return self


# ── 3 · DERIVED EXPLANATIONS (container only) ─────────────────────────────────────────────────────


class Explanations(BaseModel):
    """
    The typed container for future engine-grounded explanations. VP-1 authors none — every field is
    None and `status` is NOT_MODELLED. No sentence pretends a decision was calculated.
    """

    model_config = _FROZEN

    belief_explanation: Optional[str] = None
    decision_explanation: Optional[str] = None
    missing_information_explanation: Optional[str] = None
    constraint_explanation: Optional[str] = None
    status: LayerStatus = LayerStatus.not_modelled

    @model_validator(mode="after")
    def _no_authored_explanation_reports_engine(self) -> "Explanations":
        populated = any((self.belief_explanation, self.decision_explanation,
                         self.missing_information_explanation, self.constraint_explanation))
        if populated and self.status is not LayerStatus.engine:
            raise ValueError("a populated explanation must be engine-derived and report ENGINE")
        if not populated and self.status is LayerStatus.engine:
            raise ValueError("an empty explanation container must not report ENGINE")
        return self


# ── 4 · MODEL BOUNDARY ────────────────────────────────────────────────────────────────────────────


class ModelBoundary(BaseModel):
    """What MERIDIAN does not model, as typed values. Present on every Virtual Person."""

    model_config = _FROZEN

    not_modelled: tuple[str, ...] = NOT_MODELLED_LAYERS


# ── The future decision-input shape (defined now, so exclusion is structural) ─────────────────────


class DecisionInputs(BaseModel):
    """
    The shape a future decision function may receive. Decisions are VP-3; nothing computes here.

    It carries ONLY references to engine state (goals, responsibilities, pressures, constraints,
    information, available actions). It has NO field for portrait, biography, display name,
    occupation, education, socioeconomic description or life stage — so a decision cannot receive
    those even by accident. A test asserts the field set.
    """

    model_config = _FROZEN

    goal_refs: tuple[str, ...] = ()
    responsibility_refs: tuple[str, ...] = ()
    pressure_refs: tuple[str, ...] = ()
    constraint_refs: tuple[str, ...] = ()
    information_refs: tuple[str, ...] = ()
    available_action_refs: tuple[str, ...] = ()


# ── Root ──────────────────────────────────────────────────────────────────────────────────────────


class VirtualPerson(BaseModel):
    """A fictional person as data: identity, reserved state, explanation container, boundary."""

    model_config = _FROZEN

    schema_version: str = SCHEMA_VERSION
    identity: FixtureIdentity
    state: PersonState = PersonState()
    explanations: Explanations = Explanations()
    model_boundary: ModelBoundary = ModelBoundary()

    @model_validator(mode="after")
    def _version(self) -> "VirtualPerson":
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"unexpected schema version '{self.schema_version}'")
        return self


# ── Fixture adapter ───────────────────────────────────────────────────────────────────────────────


def from_cast(person_id: str) -> VirtualPerson:
    """
    Build a Virtual Person from the EXISTING belief cast — the migration path.

    Reuses existing fictional ids and cast descriptions. It does not rename any public id, invent a
    biography, or duplicate an identity. `display_name` stays the existing role label; `portrait_ref`
    stays null; unimplemented state stays NOT_MODELLED. This is the only bridge between the belief
    cast and Virtual Person, and it adds nothing the cast did not already declare.
    """
    person = next((p for p in cast.PEOPLE if p["person_id"] == person_id), None)
    if person is None:
        raise ValueError(f"no person '{person_id}' in the belief cast")
    ref = PersonRef(scenario_id=cast.SCENARIO_ID, entity_id=person_id)
    return VirtualPerson(
        identity=FixtureIdentity(
            person_ref=ref,
            display_name=person["display_name"],   # existing role label, not invented
            portrait_ref=None,                      # none exists
            role=person["display_name"],
            biography=person.get("bio"),
            # life_stage, organisation_ref, community_ref left None — not invented to fill the schema
        ),
    )
