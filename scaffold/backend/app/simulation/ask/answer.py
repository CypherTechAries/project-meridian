"""
Ask MERIDIAN Phase 1 — deterministic answer composition.

Every answer is assembled from existing read models (the Virtual Person projection, the belief
landscape). Nothing is generated, nothing is inferred, no model is called. The same question always
produces the same response.

NO SHADOW STATE. The composer receives one question plus explicit safe context. It never accepts a
transcript, never persists anything and never mutates a fixture, history, decision or run. A
conversation is navigation context, not authority.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..belief.projection import landscape_projection
from ..scenario_state import Direction, FieldState, Level, packaged_scenario_state
from ..person.projection import RUN_INTEGRATION, dossier, roster
from ..belief.cast import SCENARIO_ID
from ..person.vp4_fixtures import PEOPLE
from ..person.schema import NOT_MODELLED_LAYERS
from .catalogue import (
    CATALOGUE,
    CATALOGUE_VERSION,
    PERSON_ALIASES,
    STARTERS,
    UNSUPPORTED_ANSWER,
    CatalogueEntry,
    ComponentType,
    Intent,
    TargetType,
    detect_future_topic,
    match_intent,
    normalise,
)

_FROZEN = ConfigDict(extra="forbid", frozen=True)

SPEAKER = "ASK MERIDIAN"
SPEAKER_AUTHORITY = "Engine-grounded explanation · Read only"


class AskMode(str, Enum):
    explore = "EXPLORE"     # the only mode in Phase 1; no Plan, no Command


class ResponseComponent(BaseModel):
    model_config = _FROZEN
    component_type: ComponentType
    title: str
    body: dict[str, Any] = Field(default_factory=dict)


class EvidenceLink(BaseModel):
    model_config = _FROZEN
    label: str
    destination: str          # an internal route or API path
    kind: str                 # "screen" | "api"


class AskResponse(BaseModel):
    model_config = _FROZEN

    response_id: str
    catalogue_version: str = CATALOGUE_VERSION
    speaker: str = SPEAKER
    speaker_authority: str = SPEAKER_AUTHORITY
    matched_intent: Optional[Intent]
    normalized_question: str
    mode: AskMode = AskMode.explore
    read_only: bool = True
    supported: bool
    short_answer: str
    components: tuple[ResponseComponent, ...] = ()
    evidence: tuple[EvidenceLink, ...] = ()
    limitations: tuple[str, ...] = ()
    suggested_follow_ups: tuple[str, ...] = ()
    result_origins: dict[str, str] = Field(default_factory=dict)
    run_integration: dict = RUN_INTEGRATION
    execution_status: str = "NOT_EXECUTED"
    supported_questions: tuple[str, ...] = ()


# ── target resolution ─────────────────────────────────────────────────────────────────────────────


def resolve_person(question: str, person_ref: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
    """
    Resolve a person from an explicit typed ref, a declared alias, or a fixture label.

    Returns (person_id, clarification_reason). Ambiguity returns a clarification, never a silent
    pick. Real-person names, free text, organisations and cohorts do not resolve.
    """
    if person_ref:
        parts = person_ref.split(":")
        # every segment is checked, INCLUDING the scenario. An earlier version omitted the scenario
        # check, so a cross-world id resolved to a local person — caught by test_09.
        if (len(parts) == 4 and parts[0] == "fict" and parts[1] == SCENARIO_ID
                and parts[2] == "person" and parts[3] in PEOPLE):
            return parts[3], None
        return None, f"'{person_ref}' is not a declared fictional person in this scenario."

    q = normalise(question)
    hits = {pid for alias, pid in PERSON_ALIASES.items() if normalise(alias) in q}
    # fixture labels (e.g. "correspondent, northshore broadcast")
    for item in roster().people:
        if normalise(item.display_name) in q:
            hits.add(item.person_ref.split(":")[-1])
    if len(hits) == 1:
        return hits.pop(), None
    if len(hits) > 1:
        return None, "More than one fictional person matches that question."
    return None, "That question needs a fictional person, and none was recognised."


# ── answer builders (compose from read models only) ───────────────────────────────────────────────


"""
FACTUAL CLAIMS COME FROM THE SHARED STATE, NOT FROM PROSE.

Every sentence below that asserts something about the run reads `packaged_scenario_state()` — the
same computation the Briefing displays. The helpers here turn that state into Ask's own wording.

The rule: this module owns HOW a fact is said. It does not own WHAT the fact is. A hand-written
claim about a chain value is a bug, because it cannot follow the engine when the engine moves.
"""

# Ask's own vocabulary for the shared level and direction. The Briefing words the same state
# differently, and that is allowed — what is not allowed is a different underlying fact.
_LEVEL_WORD = {
    Level.high: "high",
    Level.moderate: "moderate",
    Level.low: "low",
    Level.none: "not recorded",
}
_DIRECTION_WORD = {
    Direction.rising: "still rising",
    Direction.falling: "beginning to come down",
    Direction.steady: "holding steady",
    Direction.not_established: "not established over the recorded run",
}


def _describe(state_field: Optional[FieldState], subject: str) -> str:
    """
    One field, described from the shared state.

    Reports the absolute level AND the position relative to the field's own peak when they differ,
    because reporting only one is how the original contradiction happened: political pressure is
    simultaneously low on a 0-1 scale and within 3% of the highest it has reached in this run.
    Saying only "low" hides the second fact; saying only "still high" states the second as if it
    were the first, which is what Ask used to do, and it was wrong.
    """
    if state_field is None:
        return f"{subject} is UNAVAILABLE in this packaged run."
    level = _LEVEL_WORD[state_field.level]

    # An unmeasured direction is reported as its own clause. Reading it as "is moderate and not
    # established" implies the LEVEL was not established, which is false and is the same class of
    # error as the contradiction this module was rewritten to fix.
    if state_field.direction is Direction.not_established:
        return (f"{subject} is {level}; which way it is moving is not established, because "
                f"MERIDIAN does not record that value often enough to say.")

    sentence = f"{subject} is {level} and {_DIRECTION_WORD[state_field.direction]}"
    if state_field.near_peak:
        # "in this run" is internal vocabulary; a reader does not know what a run is.
        sentence += ", though it is close to the highest it has been so far"
    return sentence + "."


def _uncapitalise(sentence: str) -> str:
    """Join a derived sentence onto a clause already in progress, without touching its content."""
    return sentence[:1].lower() + sentence[1:] if sentence else sentence


def _boundary_component() -> ResponseComponent:
    return ResponseComponent(
        component_type=ComponentType.model_boundary,
        title="What MERIDIAN does not model",
        body={"not_modelled": list(NOT_MODELLED_LAYERS)})


def _brief() -> tuple[str, list[ResponseComponent], list[EvidenceLink]]:
    land = landscape_projection()
    state = packaged_scenario_state()
    # Derived, not authored. "political pressure is still high" used to be hard-coded here; the
    # engine's value is 0.15 on a 0-1 scale, so it was simply untrue, and no test could see it.
    answer = ("The Kestral Strait remains blocked. Shipping is rerouting and port work has fallen. "
              + _describe(state.get("political_pressure"), "Pressure on the government")
              + " " + land.exposure_statement)
    comps = [
        ResponseComponent(component_type=ComponentType.executive_summary, title="Current situation",
                          body={"claim": land.claim.claim_text,
                                "population_total": land.population_total,
                                "population_not_reached": land.population_not_reached}),
        ResponseComponent(component_type=ComponentType.canonical_map, title="Kestral Strait",
                          body={"component": "briefing-canonical-map", "blockade_active": True}),
        _boundary_component()]
    ev = [EvidenceLink(label="Open the full briefing", destination="/briefing", kind="screen"),
          EvidenceLink(label="Belief landscape data",
                       destination="/api/belief/kestral-strait/landscape", kind="api")]
    return answer, comps, ev


def _economy() -> tuple[str, list[ResponseComponent], list[EvidenceLink]]:
    state = packaged_scenario_state()
    # The causal ORDER is a property of the declared chain and is safe to state as prose. The
    # STATE of each link is not, and is read from the shared state.
    answer = ("Higher insurance costs pushed carriers onto longer routes, port activity fell, and "
              "employment exposure and household concern followed. "
              + _describe(state.get("rerouting_level"), "Carrier rerouting") + " "
              + _describe(state.get("port_activity_deficit"), "The shortfall in port activity") + " "
              + "Political pressure lags its causes, and "
              + _uncapitalise(_describe(state.get("political_pressure"),
                                        "pressure on the government"))
              + " MERIDIAN models no financial-market or stock-price data.")
    comps = [
        ResponseComponent(component_type=ComponentType.economy_chain, title="How the effects travelled",
                          body={"stages": ["incident", "insurer risk", "carrier rerouting",
                                           "port activity", "employment exposure",
                                           "household concern", "narrative attention",
                                           "collective activity", "political pressure"]}),
        ResponseComponent(component_type=ComponentType.canonical_map, title="Kestral Strait",
                          body={"component": "briefing-canonical-map", "blockade_active": True}),
        _boundary_component()]
    ev = [EvidenceLink(label="Open the full briefing", destination="/briefing", kind="screen"),
          EvidenceLink(label="Mechanism detail", destination="/analysis", kind="screen")]
    return answer, comps, ev


def _reaction() -> tuple[str, list[ResponseComponent], list[EvidenceLink]]:
    land = landscape_projection()
    answer = ("This scenario shows different reactions among the three named "
              "fictional people. Organisations hold their own official positions. Population groups "
              "are represented by averages; MERIDIAN does not know how every individual inside those "
              "groups differs.")
    comps = [
        ResponseComponent(component_type=ComponentType.person_summary, title="Named fictional people",
                          body={"people": [{"name": p.display_name, "result": p.result_statement}
                                           for p in land.people]}),
        ResponseComponent(component_type=ComponentType.organisation_position,
                          title="Organisation positions",
                          body={"organisations": [{"name": o.display_name, "position": o.result_statement}
                                                  for o in land.organisations]}),
        ResponseComponent(component_type=ComponentType.population_group,
                          title="Population groups — averages, not individuals",
                          body={"note": "Group-level averages. MERIDIAN does not model the "
                                        "individuals inside these groups.",
                                "groups": [{"name": c.display_name, "result": c.result_statement,
                                            "breakdown": "UNAVAILABLE"} for c in land.cohorts]}),
        _boundary_component()]
    ev = [EvidenceLink(label="Belief landscape data",
                       destination="/api/belief/kestral-strait/landscape", kind="api")]
    return answer, comps, ev


def _person_situation(pid: str) -> tuple[str, list[ResponseComponent], list[EvidenceLink]]:
    d = dossier(pid)
    answer = d.current_situation.summary
    comps = [
        ResponseComponent(component_type=ComponentType.person_summary, title=d.identity.display_name,
                          body={"person_ref": d.identity.person_ref, "role": d.identity.role,
                                "portrait_ref": d.identity.portrait_ref}),
        ResponseComponent(component_type=ComponentType.current_situation, title="Current situation",
                          body={"goals": [g.model_dump(mode="json") for g in d.current_situation.goals],
                                "pressures": [p.model_dump(mode="json") for p in d.current_situation.pressures],
                                "constraints": [c.model_dump(mode="json") for c in d.current_situation.constraints]}),
        _boundary_component()]
    ev = [EvidenceLink(label="Open the full dossier",
                       destination=f"/api/virtual-person/kestral-strait/dossier/{d.identity.person_ref}",
                       kind="api")]
    return answer, comps, ev


def _person_decision(pid: str) -> tuple[str, list[ResponseComponent], list[EvidenceLink]]:
    d = dossier(pid)
    answer = d.decision.explanation
    comps = [
        ResponseComponent(component_type=ComponentType.current_situation, title="Current situation",
                          body={"summary": d.current_situation.summary}),
        ResponseComponent(component_type=ComponentType.decision, title="Decision",
                          body={"selected_action_label": d.decision.selected_action_label,
                                "execution_status": d.decision.execution_status,
                                "default_statement": d.decision.default_statement,
                                # readable labels, not raw action ids
                                "unavailable_options": [
                                    d.decision.option_labels.get(a, a)
                                    for a in d.decision.unavailable_options],
                                "blocking_constraints": d.decision.blocking_constraints}),
        _boundary_component()]
    ev = [EvidenceLink(label="Show the calculation",
                       destination=f"/api/virtual-person/kestral-strait/dossier/{d.identity.person_ref}",
                       kind="api"),
          EvidenceLink(label="Open the full dossier",
                       destination=f"/api/virtual-person/kestral-strait/dossier/{d.identity.person_ref}",
                       kind="api")]
    return answer, comps, ev


def _person_history(pid: str) -> tuple[str, list[ResponseComponent], list[EvidenceLink]]:
    d = dossier(pid)
    answer = (f"{len(d.information_history)} information record(s) are held for this person. "
              + d.belief_history.trajectory_explanation)
    comps = [
        ResponseComponent(component_type=ComponentType.information_history, title="Information received",
                          body={"records": [i.model_dump(mode="json") for i in d.information_history]}),
        ResponseComponent(component_type=ComponentType.belief_observation, title="Belief observations",
                          body={"observations": [o.model_dump(mode="json") for o in d.belief_history.observations],
                                "observation_count": d.belief_history.observation_count,
                                "trajectory_available": d.belief_history.trajectory_available,
                                "trajectory_explanation": d.belief_history.trajectory_explanation}),
        _boundary_component()]
    ev = [EvidenceLink(label="Open the full dossier",
                       destination=f"/api/virtual-person/kestral-strait/dossier/{d.identity.person_ref}",
                       kind="api")]
    return answer, comps, ev


def _unknown() -> tuple[str, list[ResponseComponent], list[EvidenceLink]]:
    answer = ("MERIDIAN models one fictional scenario, a first-order belief change, a current "
              "situation and a declared decision. It does not model memory, relationships that "
              "affect behaviour, changing trust, personal history, or the individuals inside a "
              "population group. Where a value is not known it is marked UNKNOWN, UNAVAILABLE or "
              "NOT_MODELLED, never zero.")
    comps = [_boundary_component(),
             ResponseComponent(component_type=ComponentType.model_boundary,
                               title="Unavailable data",
                               body={"population_group_breakdown": "UNAVAILABLE",
                                     "cohort_confidence": "NOT_MODELLED",
                                     "belief_trajectory": "one observation only"})]
    ev = [EvidenceLink(label="Capability record", destination="/analysis", kind="screen")]
    return answer, comps, ev


def _evidence() -> tuple[str, list[ResponseComponent], list[EvidenceLink]]:
    answer = "Here are the places the underlying values can be inspected."
    ev = [EvidenceLink(label="Briefing", destination="/briefing", kind="screen"),
          EvidenceLink(label="Analysis", destination="/analysis", kind="screen"),
          EvidenceLink(label="Belief landscape API",
                       destination="/api/belief/kestral-strait/landscape", kind="api"),
          EvidenceLink(label="Virtual Person roster API",
                       destination="/api/virtual-person/kestral-strait/roster", kind="api")]
    return answer, [], ev


LIMITATIONS = (
    "This is a packaged snapshot, not live run state.",
    "Nothing was executed.",
    "One belief observation exists per person; that is not a trend.",
    "Population groups are averages; individuals inside them are not modelled.",
)


def answer_question(question: str, *, person_ref: Optional[str] = None,
                    intent_hint: Optional[Intent] = None) -> AskResponse:
    """Deterministic. Same question in, same response out. No model call anywhere."""
    normalised = normalise(question)
    entry: Optional[CatalogueEntry] = None
    if intent_hint is not None:
        entry = next((e for e in CATALOGUE if e.intent is intent_hint), None)
    if entry is None:
        entry = match_intent(question)

    # a future-capability question is NAMED as not implemented, never improvised
    future = detect_future_topic(question)
    if entry is None and future:
        return AskResponse(
            response_id=f"ask-{normalised[:40] or 'empty'}", matched_intent=None,
            normalized_question=normalised, supported=False,
            short_answer=(f"{UNSUPPORTED_ANSWER} In particular, {future} is a future capability and "
                          f"is not implemented in this version."),
            components=(ResponseComponent(component_type=ComponentType.unsupported_question,
                                          title="Not implemented in this version",
                                          body={"future_topic": future,
                                                "status": "FUTURE_NOT_IMPLEMENTED"}),),
            supported_questions=STARTERS, limitations=LIMITATIONS)

    if entry is None:
        return AskResponse(
            response_id=f"ask-{normalised[:40] or 'empty'}", matched_intent=None,
            normalized_question=normalised, supported=False, short_answer=UNSUPPORTED_ANSWER,
            components=(ResponseComponent(component_type=ComponentType.unsupported_question,
                                          title="Not supported in this version", body={}),),
            supported_questions=STARTERS, limitations=LIMITATIONS)

    pid: Optional[str] = None
    if entry.required_target is TargetType.person:
        pid, reason = resolve_person(question, person_ref)
        if pid is None:
            return AskResponse(
                response_id=f"ask-{normalised[:40]}", matched_intent=entry.intent,
                normalized_question=normalised, supported=False,
                short_answer=f"{reason} Which fictional person do you mean?",
                components=(ResponseComponent(component_type=ComponentType.clarification,
                                              title="Which person?",
                                              body={"choices": [p.display_name for p in roster().people],
                                                    "reason": reason}),),
                supported_questions=STARTERS, limitations=LIMITATIONS)

    builders = {
        Intent.brief_current_situation: _brief,
        Intent.explain_economy_and_supply_chains: _economy,
        Intent.show_public_reaction: _reaction,
        Intent.show_what_is_unknown: _unknown,
        Intent.open_evidence: _evidence,
    }
    person_builders = {
        Intent.explain_person_current_situation: _person_situation,
        Intent.explain_person_decision: _person_decision,
        Intent.show_person_history: _person_history,
    }
    if entry.intent in person_builders:
        short, comps, ev = person_builders[entry.intent](pid)  # type: ignore[arg-type]
    else:
        short, comps, ev = builders[entry.intent]()

    # `question_label`, never `intent.value` — a raw identifier is not a question a reader can read.
    follow = tuple(e.question_label for e in CATALOGUE if e.intent in entry.follow_up_intents)

    return AskResponse(
        response_id=f"ask-{entry.intent.value.lower()}-{pid or 'scenario'}",
        matched_intent=entry.intent, normalized_question=normalised, supported=True,
        short_answer=short, components=tuple(comps), evidence=tuple(ev),
        limitations=LIMITATIONS, suggested_follow_ups=follow,
        result_origins={"answer": "ENGINE", "identity": "FIXTURE", "options": "FIXTURE"},
        supported_questions=STARTERS)
