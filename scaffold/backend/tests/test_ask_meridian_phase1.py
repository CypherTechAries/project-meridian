"""
Ask MERIDIAN Phase 1 — deterministic, read-only, no language model.

Proves the catalogue is declared and versioned, matching is deterministic, unsupported and
future-capability questions are NAMED rather than improvised, targets resolve only to declared
fictional people, answers match the VP-5 read model exactly, and nothing mutates.
"""

from __future__ import annotations

import copy
import inspect
import json

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.simulation.ask.answer import answer_question, resolve_person
from app.simulation.ask.catalogue import (
    CATALOGUE,
    CATALOGUE_VERSION,
    STARTERS,
    UNSUPPORTED_ANSWER,
    CatalogueEntry,
    Intent,
    TargetType,
    match_intent,
    normalise,
)
from app.simulation.belief import cast
from app.simulation.person import vp2_fixtures, vp4_fixtures
from app.simulation.person.projection import dossier

client = TestClient(app)
ASK = "/api/ask-meridian/query"


def ask(q: str, **kw):
    r = client.post(ASK, json={"question": q, **kw})
    return r.status_code, r.json()


# ── 1-4 · catalogue and matching ──────────────────────────────────────────────────────────────────


def test_01_every_declared_intent_loads() -> None:
    assert len(CATALOGUE) == 8
    assert {e.intent for e in CATALOGUE} == set(Intent)
    for e in CATALOGUE:
        CatalogueEntry.model_validate(e.model_dump())
        assert e.phrase_patterns and e.data_sources and e.components


def test_02_unknown_intent_fields_fail() -> None:
    with pytest.raises(ValidationError):
        CatalogueEntry(intent=Intent.brief_current_situation, phrase_patterns=("x",),
                       required_target=TargetType.none, response_template_id="t",
                       data_sources=("d",), components=(), follow_up_intents=(),
                       persuasiveness=0.9)  # type: ignore[call-arg]


def test_03_known_starter_phrases_map_correctly() -> None:
    for starter in STARTERS:
        entry = match_intent(starter)
        assert entry is not None, starter
        assert entry.starter_label == starter


def test_04_normalisation_is_deterministic() -> None:
    variants = ["What is happening?", "what is happening", "WHAT IS HAPPENING!!",
                "Please tell me what is happening", "what's happening"]
    matched = {match_intent(v).intent if match_intent(v) else None for v in variants}
    assert matched == {Intent.brief_current_situation}
    assert normalise("What's  happening?!") == normalise("whats happening")


# ── 5-11 · unsupported, clarification, targets ────────────────────────────────────────────────────


def test_05_unsupported_question_returns_the_supported_set() -> None:
    s, j = ask("What is the airspeed velocity of a swallow?")
    assert s == 200 and j["supported"] is False
    assert j["short_answer"] == UNSUPPORTED_ANSWER
    assert tuple(j["supported_questions"]) == STARTERS
    assert j["matched_intent"] is None


def test_06_ambiguous_person_returns_clarification() -> None:
    s, j = ask("Why did they choose that?")
    assert j["supported"] is False
    assert any(c["component_type"] == "ClarificationCard" for c in j["components"])


def test_07_fictional_person_alias_resolves() -> None:
    for alias, expected in (("the journalist", "broadcast-journalist"),
                            ("the minister", "government-minister"),
                            ("the spokesperson", "family-spokesperson")):
        pid, reason = resolve_person("what is affecting " + alias)
        assert pid == expected and reason is None


def test_08_free_text_real_person_target_does_not_resolve() -> None:
    for bad in ("what is affecting a famous politician", "what is affecting a real journalist",
                "what is affecting the reporter from another network"):
        pid, reason = resolve_person(bad)
        assert pid is None and reason


def test_09_cross_world_target_fails() -> None:
    pid, reason = resolve_person("x", person_ref="fict:other-world:person:broadcast-journalist")
    assert pid is None and "not a declared fictional person" in reason


def test_10_organisation_cannot_resolve_as_a_person() -> None:
    pid, _ = resolve_person("x", person_ref="fict:kestral-strait:organisation:public-broadcaster")
    assert pid is None


def test_11_cohort_cannot_resolve_as_a_person() -> None:
    pid, _ = resolve_person("x", person_ref="fict:kestral-strait:cohort:port-workers")
    assert pid is None


# ── 12-15 · determinism, read-only, no shadow state ───────────────────────────────────────────────


def test_12_same_question_produces_the_same_response() -> None:
    a = ask("Brief me on the current situation.")[1]
    b = ask("Brief me on the current situation.")[1]
    assert a == b


def test_13_response_is_read_only() -> None:
    for q in ("What is happening?", "How are people and groups reacting?"):
        _, j = ask(q)
        assert j["read_only"] is True and j["mode"] == "EXPLORE"
        assert j["execution_status"] == "NOT_EXECUTED"
        assert j["run_integration"]["connected_to_authoritative_run"] is False


def test_14_query_does_not_mutate_any_fixture_history_or_decision() -> None:
    snap = {"vp2": copy.deepcopy(vp2_fixtures.VP2_FIXTURES),
            "rel": copy.deepcopy(vp4_fixtures.RELATIONSHIPS),
            "priors": copy.deepcopy(cast.PRIORS), "people": copy.deepcopy(cast.PEOPLE)}
    for q in ("What is happening?", "Why did the journalist seek another source?",
              "What information did the journalist receive?", "What does MERIDIAN not know?"):
        ask(q)
    assert vp2_fixtures.VP2_FIXTURES == snap["vp2"]
    assert vp4_fixtures.RELATIONSHIPS == snap["rel"]
    assert cast.PRIORS == snap["priors"] and cast.PEOPLE == snap["people"]


def test_15_no_conversation_transcript_is_accepted_as_state() -> None:
    r = client.post(ASK, json={"question": "What is happening?",
                               "transcript": [{"role": "user", "text": "earlier"}]})
    assert r.status_code == 422
    r2 = client.post(ASK, json={"question": "What is happening?", "history": ["a", "b"]})
    assert r2.status_code == 422


# ── 16-20 · parity with VP-5 ──────────────────────────────────────────────────────────────────────


def test_16_current_situation_answer_matches_vp5() -> None:
    _, j = ask("What is affecting the journalist?")
    d = dossier("broadcast-journalist")
    assert j["short_answer"] == d.current_situation.summary


def test_17_18_decision_answer_matches_vp5_and_is_not_executed() -> None:
    _, j = ask("Why did the journalist seek another source?")
    d = dossier("broadcast-journalist")
    assert j["short_answer"] == d.decision.explanation
    card = next(c for c in j["components"] if c["component_type"] == "DecisionCard")
    assert card["body"]["execution_status"] == "NOT_EXECUTED"
    assert card["body"]["selected_action_label"] == d.decision.selected_action_label
    # the declared LABEL for each unavailable option id, in the same order — never the raw id
    assert card["body"]["unavailable_options"] == [
        d.decision.option_labels[a] for a in d.decision.unavailable_options
    ]


def test_19_history_answer_matches_vp5() -> None:
    _, j = ask("What information did the journalist receive?")
    d = dossier("broadcast-journalist")
    card = next(c for c in j["components"] if c["component_type"] == "BeliefObservationCard")
    assert card["body"]["observation_count"] == d.belief_history.observation_count
    assert card["body"]["trajectory_available"] == d.belief_history.trajectory_available


def test_20_belief_classifications_match_the_canonical_classifier() -> None:
    from app.simulation.belief.classification import classify_belief_outcome
    from app.simulation.belief.projection import person_projection

    _, j = ask("What information did the journalist receive?")
    card = next(c for c in j["components"] if c["component_type"] == "BeliefObservationCard")
    proj = person_projection("broadcast-journalist")
    canonical, _reason = classify_belief_outcome(received=proj.received_the_claim,
                                                 credence=proj.calculation.final_credence,
                                                 is_uncertain=proj.still_unsure)
    assert card["body"]["observations"][0]["classification"] == canonical.value


# ── 21-23 · public reaction, no trend, unknowns ───────────────────────────────────────────────────


def test_21_public_reaction_distinguishes_people_orgs_and_group_averages() -> None:
    _, j = ask("How are people and groups reacting?")
    kinds = {c["component_type"] for c in j["components"]}
    assert {"PersonSummaryCard", "OrganisationPositionCard", "PopulationGroupCard"} <= kinds
    group = next(c for c in j["components"] if c["component_type"] == "PopulationGroupCard")
    assert "does not model the individuals" in group["body"]["note"]
    assert "averages" in j["short_answer"]


def test_22_one_observation_is_not_described_as_a_trend() -> None:
    _, j = ask("What information did the journalist receive?")
    flat = json.dumps(j).lower()
    for banned in ("sentiment trend", "trending", "the trend"):
        assert banned not in flat
    card = next(c for c in j["components"] if c["component_type"] == "BeliefObservationCard")
    assert card["body"]["trajectory_available"] is False


def test_23_unknowns_answer_contains_the_model_boundary() -> None:
    _, j = ask("What does MERIDIAN not know?")
    boundary = next(c for c in j["components"] if c["component_type"] == "ModelBoundaryCard")
    for trait in ("intelligence", "competence", "susceptibility", "persuadability"):
        assert trait in boundary["body"]["not_modelled"]


# ── 24-27 · future capabilities are named, never improvised ───────────────────────────────────────


def test_24_25_26_future_questions_are_not_improvised() -> None:
    for q in ("What are intelligence services assessing about external actors?",
              "What diplomatic options are available?",
              "What are the military commanders recommending?"):
        _, j = ask(q)
        assert j["supported"] is False, q
        assert "not implemented" in j["short_answer"].lower()
        card = next(c for c in j["components"] if c["component_type"] == "UnsupportedQuestionCard")
        assert card["body"].get("status") == "FUTURE_NOT_IMPLEMENTED"


def test_27_no_ranking_or_targeting_intent_exists() -> None:
    names = " ".join(i.value for i in Intent).lower()
    for banned in ("rank", "target", "persuad", "influence", "optimis", "audience"):
        assert banned not in names
    paths = [p for p in app.openapi()["paths"] if "ask-meridian" in p]
    assert paths == ["/api/ask-meridian/query"]


# ── 28-32 · absence, evidence, schema strictness, no model ────────────────────────────────────────


def test_28_29_absence_states_remain_distinct_and_never_zero() -> None:
    _, j = ask("What does MERIDIAN not know?")
    flat = json.dumps(j)
    assert "UNAVAILABLE" in flat and "NOT_MODELLED" in flat
    for c in j["components"]:
        for v in c["body"].values():
            assert v != 0, "an absence serialised as numeric zero"


def test_30_evidence_links_resolve_to_known_destinations() -> None:
    known_screens = {"/briefing", "/analysis"}
    api_paths = set(app.openapi()["paths"])
    for q in ("What is happening?", "Why did the journalist seek another source?"):
        _, j = ask(q)
        for ev in j["evidence"]:
            if ev["kind"] == "screen":
                assert ev["destination"] in known_screens, ev
            else:
                base = ev["destination"].split("fict:")[0].rstrip("/")
                assert any(p.startswith(base) or base.startswith(p.split("{")[0].rstrip("/"))
                           for p in api_paths), ev


def test_31_api_schema_rejects_unknown_request_fields() -> None:
    assert client.post(ASK, json={"question": "hi", "execute": True}).status_code == 422
    assert client.post(ASK, json={"question": "hi", "catalogue_version": "bogus@9"}).status_code == 422
    assert client.post(ASK, json={"question": "hi", "scenario_id": "other-world"}).status_code == 422
    assert client.post(ASK, json={}).status_code == 422
    assert client.get(ASK).status_code == 405


def test_32_no_language_model_is_used() -> None:
    from app.simulation.ask import answer as ans_mod
    from app.simulation.ask import catalogue as cat_mod

    import ast

    for mod in (ans_mod, cat_mod):
        # strip docstrings: they legitimately NAME what is not used ("no embeddings, no remote
        # language service"), and a naive scan flags the denial as a violation.
        tree = ast.parse(inspect.getsource(mod))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                if ast.get_docstring(node) and node.body and isinstance(node.body[0], ast.Expr):
                    node.body[0].value = ast.Constant(value="")
        code_only = ast.unparse(tree).lower()
        for banned in ("openai", "anthropic", "llm_client", "embedding", "completion(",
                       "httpx.post", "requests.post"):
            assert banned not in code_only, f"{mod.__name__} references '{banned}'"


def test_33_answer_function_is_pure_over_the_question() -> None:
    a = answer_question("What is happening?")
    b = answer_question("What is happening?")
    assert a.model_dump_json() == b.model_dump_json()
    assert a.catalogue_version == CATALOGUE_VERSION


# ── Reader-facing strings must never be raw identifiers ────────────────────────────────────────
#
# Found during visual review of the implemented screen: a follow-up chip rendered
# "SHOW_PERSON_INFORMATION_AND_BELIEF_HISTORY", and the decision card listed the unavailable option
# as "a-publish-now". Both were raw internal identifiers presented to a reader as text.

def test_34_no_answer_shows_a_raw_intent_identifier() -> None:
    from app.simulation.ask.catalogue import Intent

    identifiers = {i.value for i in Intent}
    for q in list(STARTERS) + ["why did the journalist seek another source",
                               "what information did they receive"]:
        r = answer_question(q)
        for text in (*r.suggested_follow_ups, *r.supported_questions, r.short_answer):
            assert text not in identifiers, f"raw intent identifier shown to a reader: {text}"


def test_35_every_catalogue_entry_declares_a_readable_question_label() -> None:
    for e in CATALOGUE:
        assert e.question_label
        assert e.question_label != e.intent.value
        assert " " in e.question_label


def test_36_a_catalogue_label_that_is_an_identifier_is_rejected() -> None:
    from app.simulation.ask.catalogue import CatalogueEntry

    base = CATALOGUE[0].model_dump()
    base["question_label"] = "SHOW_PERSON_INFORMATION_AND_BELIEF_HISTORY"
    with pytest.raises(ValidationError):
        CatalogueEntry(**base)


def test_37_unavailable_options_are_labels_not_action_ids() -> None:
    r = answer_question("why did the journalist seek another source")
    card = next(c for c in r.components if c.component_type.value == "DecisionCard")
    shown = card.body["unavailable_options"]
    assert shown, "the exemplar has one unavailable option"
    for option in shown:
        assert not option.startswith("a-"), f"raw action id shown to a reader: {option}"
    assert "publish the claim immediately" in shown
