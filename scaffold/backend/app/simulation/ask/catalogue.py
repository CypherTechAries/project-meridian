"""
Ask MERIDIAN Phase 1 — the supported-question catalogue and deterministic matcher.

NO LANGUAGE MODEL. Phase 1 does not pretend to understand unrestricted natural language. It matches
a question against a small, versioned, declared catalogue using normalisation and an alias table.
There are no embeddings, no remote language service, no opaque similarity score and no unrestricted
entity extraction. When nothing matches, it says so and offers the supported questions — it never
guesses.

Every supported behaviour is declared HERE, in one typed catalogue, rather than hidden in scattered
conditionals across the frontend.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

_FROZEN = ConfigDict(extra="forbid", frozen=True)

CATALOGUE_VERSION = "ask-meridian-catalogue@0.1"

UNSUPPORTED_ANSWER = (
    "I cannot answer that question in this version. I can currently explain the crisis, the economy "
    "and supply chain, recorded public reaction, a fictional person's current situation or decision, "
    "and what MERIDIAN does not know."
)


class Intent(str, Enum):
    brief_current_situation = "BRIEF_CURRENT_SITUATION"
    explain_economy_and_supply_chains = "EXPLAIN_ECONOMY_AND_SUPPLY_CHAINS"
    show_public_reaction = "SHOW_PUBLIC_REACTION"
    explain_person_current_situation = "EXPLAIN_PERSON_CURRENT_SITUATION"
    explain_person_decision = "EXPLAIN_PERSON_DECISION"
    show_person_history = "SHOW_PERSON_INFORMATION_AND_BELIEF_HISTORY"
    show_what_is_unknown = "SHOW_WHAT_IS_UNKNOWN"
    open_evidence = "OPEN_EVIDENCE"


class TargetType(str, Enum):
    none = "NONE"
    person = "PERSON"


class CapabilityStatus(str, Enum):
    implemented = "IMPLEMENTED"
    future_not_implemented = "FUTURE_NOT_IMPLEMENTED"


class ComponentType(str, Enum):
    executive_summary = "ExecutiveSummaryCard"
    canonical_map = "CanonicalMapCard"
    economy_chain = "EconomyChainCard"
    person_summary = "PersonSummaryCard"
    current_situation = "CurrentSituationCard"
    decision = "DecisionCard"
    belief_observation = "BeliefObservationCard"
    population_group = "PopulationGroupCard"
    organisation_position = "OrganisationPositionCard"
    information_history = "InformationHistoryCard"
    model_boundary = "ModelBoundaryCard"
    evidence_link = "EvidenceLinkCard"
    unsupported_question = "UnsupportedQuestionCard"
    clarification = "ClarificationCard"


class CatalogueEntry(BaseModel):
    model_config = _FROZEN

    intent: Intent
    phrase_patterns: tuple[str, ...]
    required_target: TargetType
    response_template_id: str
    data_sources: tuple[str, ...]
    components: tuple[ComponentType, ...]
    follow_up_intents: tuple[Intent, ...]
    capability_status: CapabilityStatus = CapabilityStatus.implemented

    #: How this intent is offered to a reader as a follow-up. REQUIRED on every entry. Follow-ups
    #: previously fell back to `intent.value`, which put the raw identifier
    #: SHOW_PERSON_INFORMATION_AND_BELIEF_HISTORY on screen as if it were a question.
    question_label: str

    #: Set only on the entries offered on the Ask MERIDIAN home screen.
    starter_label: Optional[str] = None

    @model_validator(mode="after")
    def _labels_are_readable(self) -> "CatalogueEntry":
        for field, value in (("question_label", self.question_label),
                             ("starter_label", self.starter_label)):
            if value is None:
                continue
            if value.strip() != value or not value:
                raise ValueError(f"{field} must be non-empty and trimmed")
            # An identifier, not a question: upper case with underscores and no spaces.
            if "_" in value and value == value.upper():
                raise ValueError(f"{field} must be a readable question, not an identifier: {value}")
        return self


CATALOGUE: tuple[CatalogueEntry, ...] = (
    CatalogueEntry(
        intent=Intent.brief_current_situation,
        question_label="Brief me on the current situation.",
        phrase_patterns=("brief me on the current situation", "what is happening",
                         "what is going on", "what is going on in the kestral strait",
                         "brief me", "current situation", "what the hell is going on"),
        required_target=TargetType.none,
        response_template_id="tpl-brief",
        data_sources=("belief landscape", "kestral crisis fixtures"),
        components=(ComponentType.executive_summary, ComponentType.canonical_map,
                    ComponentType.model_boundary, ComponentType.evidence_link),
        follow_up_intents=(Intent.explain_economy_and_supply_chains, Intent.show_public_reaction,
                           Intent.show_what_is_unknown),
        starter_label="Brief me on the current situation."),
    CatalogueEntry(
        intent=Intent.explain_economy_and_supply_chains,
        question_label="How are the economy and supply chains reacting?",
        phrase_patterns=("how are the economy and supply chains reacting",
                         "what is happening to shipping and port work",
                         "economy and supply chains", "shipping and ports", "the economy"),
        required_target=TargetType.none,
        response_template_id="tpl-economy",
        data_sources=("insurer, rerouting, port, employment, household and political-pressure stages",),
        components=(ComponentType.economy_chain, ComponentType.canonical_map,
                    ComponentType.model_boundary, ComponentType.evidence_link),
        follow_up_intents=(Intent.show_public_reaction, Intent.show_what_is_unknown),
        starter_label="How are the economy and supply chains reacting?"),
    CatalogueEntry(
        intent=Intent.show_public_reaction,
        question_label="How are people and groups reacting?",
        phrase_patterns=("how are people and groups reacting", "public reaction",
                         "what do the current belief observations show",
                         "how are people reacting", "how is public sentiment changing"),
        required_target=TargetType.none,
        response_template_id="tpl-reaction",
        data_sources=("belief landscape", "virtual person records"),
        components=(ComponentType.person_summary, ComponentType.organisation_position,
                    ComponentType.population_group, ComponentType.model_boundary,
                    ComponentType.evidence_link),
        follow_up_intents=(Intent.explain_person_current_situation, Intent.show_what_is_unknown),
        starter_label="How are people and groups reacting?"),
    CatalogueEntry(
        intent=Intent.explain_person_current_situation,
        question_label="What is affecting this person right now?",
        phrase_patterns=("what is affecting", "what pressures is", "what pressure is",
                         "current situation for", "what is the situation for"),
        required_target=TargetType.person,
        response_template_id="tpl-person-situation",
        data_sources=("virtual person dossier",),
        components=(ComponentType.person_summary, ComponentType.current_situation,
                    ComponentType.model_boundary, ComponentType.evidence_link),
        follow_up_intents=(Intent.explain_person_decision, Intent.show_person_history)),
    CatalogueEntry(
        intent=Intent.explain_person_decision,
        question_label="Why was that option selected?",
        phrase_patterns=("why did", "why was", "what did", "which option did",
                         "why did the journalist select", "explain the decision"),
        required_target=TargetType.person,
        response_template_id="tpl-person-decision",
        data_sources=("virtual person dossier decision section",),
        components=(ComponentType.current_situation, ComponentType.decision,
                    ComponentType.model_boundary, ComponentType.evidence_link),
        follow_up_intents=(Intent.show_person_history, Intent.show_what_is_unknown)),
    CatalogueEntry(
        intent=Intent.show_person_history,
        question_label="What information did they receive, and how did the recorded belief change?",
        phrase_patterns=("what information did", "what did they receive",
                         "how did the recorded belief change", "belief history",
                         "information history", "what information was received by"),
        required_target=TargetType.person,
        response_template_id="tpl-person-history",
        data_sources=("virtual person dossier history sections",),
        components=(ComponentType.information_history, ComponentType.belief_observation,
                    ComponentType.model_boundary, ComponentType.evidence_link),
        follow_up_intents=(Intent.explain_person_decision, Intent.show_what_is_unknown)),
    CatalogueEntry(
        intent=Intent.show_what_is_unknown,
        question_label="What does MERIDIAN know — and what remains uncertain?",
        phrase_patterns=("what does meridian not know", "what is missing from this model",
                         "what is unknown", "what does meridian know and what remains uncertain",
                         "what remains uncertain", "limitations"),
        required_target=TargetType.none,
        response_template_id="tpl-unknown",
        data_sources=("virtual person model boundary", "belief unavailable states"),
        components=(ComponentType.model_boundary, ComponentType.evidence_link),
        follow_up_intents=(Intent.brief_current_situation, Intent.show_public_reaction),
        starter_label="What does MERIDIAN know — and what remains uncertain?"),
    CatalogueEntry(
        intent=Intent.open_evidence,
        question_label="Show the underlying evidence.",
        phrase_patterns=("show the evidence", "open the technical explanation", "show evidence",
                         "show the calculation", "open analysis"),
        required_target=TargetType.none,
        response_template_id="tpl-evidence",
        data_sources=("briefing", "analysis", "virtual person api"),
        components=(ComponentType.evidence_link,),
        follow_up_intents=(Intent.brief_current_situation,)),
)

STARTERS: tuple[str, ...] = tuple(e.starter_label for e in CATALOGUE if e.starter_label)

#: Declared person aliases. Only these, plus typed ids and fixture labels, resolve to a person.
PERSON_ALIASES: dict[str, str] = {
    "the journalist": "broadcast-journalist",
    "broadcast journalist": "broadcast-journalist",
    "the correspondent": "broadcast-journalist",
    "the minister": "government-minister",
    "government minister": "government-minister",
    "minister for maritime affairs": "government-minister",
    "the spokesperson": "family-spokesperson",
    "family spokesperson": "family-spokesperson",
}

#: Terms whose presence means the question is a FUTURE concept, answered as not implemented rather
#: than improvised from general language.
FUTURE_TOPICS: dict[str, str] = {
    "intelligence": "intelligence assessments about external actors",
    "external actor": "intelligence assessments about external actors",
    "influence operation": "influence-operation analysis",
    "social media": "social-media analysis",
    "diplomatic": "diplomatic option generation",
    "diplomacy": "diplomatic option generation",
    "military": "military recommendations",
    "commander": "military recommendations",
    "target": "targeting suggestions",
    "persuade": "persuasion strategies",
    "persuasion": "persuasion strategies",
}

_CONTRACTIONS = {"what's": "what is", "whats": "what is", "who's": "who is", "it's": "it is",
                 "don't": "do not", "doesn't": "does not", "isn't": "is not",
                 "meridian's": "meridian", "i'd": "i would"}
_FILLER = ("please", "could you", "can you", "tell me", "just", "quickly", "hey", "hi")


def normalise(question: str) -> str:
    """Deterministic: lowercase, expand declared contractions, strip filler and punctuation."""
    q = question.lower().strip()
    for a, b in _CONTRACTIONS.items():
        q = q.replace(a, b)
    q = re.sub(r"[^\w\s-]", " ", q)
    for f in _FILLER:
        q = q.replace(f, " ")
    return re.sub(r"\s+", " ", q).strip()


def match_intent(question: str) -> Optional[CatalogueEntry]:
    """
    Longest declared phrase wins — deterministic and inspectable. No similarity score, no guessing.
    """
    q = normalise(question)
    best: Optional[tuple[int, CatalogueEntry]] = None
    for entry in CATALOGUE:
        for pattern in entry.phrase_patterns:
            p = normalise(pattern)
            if p and p in q:
                if best is None or len(p) > best[0]:
                    best = (len(p), entry)
    return best[1] if best else None


def detect_future_topic(question: str) -> Optional[str]:
    q = normalise(question)
    for term, label in FUTURE_TOPICS.items():
        if term in q:
            return label
    return None
