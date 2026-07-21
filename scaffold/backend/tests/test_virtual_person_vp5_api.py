"""
Virtual Person VP-5 — read-only API.

Proves the API composes rather than recomputes (parity with VP-2/VP-3/VP-4 and the canonical belief
classifier), mutates nothing, refuses anything that is not a declared fictional person, never ranks
people, and never presents a packaged snapshot as live person state.
"""

from __future__ import annotations

import copy
import json

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.simulation.belief import cast
from app.simulation.belief.classification import classify_belief_outcome
from app.simulation.belief.projection import person_projection
from app.simulation.person import vp2_fixtures, vp3_decisions, vp4_fixtures
from app.simulation.person.decision import select_action
from app.simulation.person.projection import Dossier, Roster, dossier, roster
from app.simulation.person.vp2_fixtures import fixture_for
from app.simulation.person.vp4_fixtures import belief_history_for, information_history_for

client = TestClient(app)

ROSTER = "/api/virtual-person/kestral-strait/roster"
DOSS = "/api/virtual-person/kestral-strait/dossier/{}"
JOURNALIST = "fict:kestral-strait:person:broadcast-journalist"
PEOPLE = ("family-spokesperson", "government-minister", "broadcast-journalist")

JARGON = ("alignment", "propensity", "aggregation", "credence", "provenance", "state mass",
          "utility", "susceptibility")

DISPLAY_KEYS = ("current_situation_summary", "summary", "default_statement", "explanation",
                "trajectory_explanation", "description", "band")


def display_strings(node, path="", skip=("decision_trace",)) -> list[tuple[str, str]]:
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k in skip:
                continue
            if k in DISPLAY_KEYS and isinstance(v, str):
                out.append((f"{path}.{k}", v))
            else:
                out += display_strings(v, f"{path}.{k}", skip)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            out += display_strings(item, f"{path}[{i}]", skip)
    return out


# ── 1–3 · roster ──────────────────────────────────────────────────────────────────────────────────


def test_01_roster_returns_all_three_people() -> None:
    body = client.get(ROSTER).json()
    assert len(body["people"]) == 3
    assert {p["person_ref"].split(":")[-1] for p in body["people"]} == set(PEOPLE)


def test_02_roster_preserves_declaration_order() -> None:
    body = client.get(ROSTER).json()
    assert [p["person_ref"].split(":")[-1] for p in body["people"]] == list(PEOPLE)
    assert "never ranked" in body["ordering"]


def test_03_roster_does_not_rank_people() -> None:
    body = client.get(ROSTER).json()
    # scan the PEOPLE payload; `ordering` and `model_boundary` deliberately NAME ranking to deny it
    flat = json.dumps(body["people"]).lower()
    for banned in ("rank", "score", "influence", "susceptib", "persuad", "importance",
                   "compliance", "risk_level"):
        assert banned not in flat, f"roster exposes '{banned}'"
    assert "never ranked" in body["ordering"]
    for item in body["people"]:
        for f in item:
            assert "score" not in f.lower()


# ── 4–12 · request validation ─────────────────────────────────────────────────────────────────────


def test_04_dossier_returns_a_person() -> None:
    assert client.get(DOSS.format(JOURNALIST)).status_code == 200


def test_05_06_07_organisation_cohort_and_agent_ids_fail() -> None:
    for bad in ("fict:kestral-strait:organisation:public-broadcaster",
                "fict:kestral-strait:cohort:port-workers",
                "fict:kestral-strait:agent:national-government"):
        r = client.get(DOSS.format(bad))
        assert r.status_code == 422, bad


def test_08_cross_world_ids_fail() -> None:
    r = client.get(DOSS.format("fict:some-other-world:person:broadcast-journalist"))
    assert r.status_code == 422 and "cross-world" in r.json()["detail"]


def test_09_free_text_names_fail() -> None:
    for bad in ("BBC News", "a real journalist", "broadcast-journalist", "Reuters"):
        assert client.get(DOSS.format(bad)).status_code == 422


def test_10_unknown_person_ids_fail() -> None:
    assert client.get(DOSS.format("fict:kestral-strait:person:nobody")).status_code == 404


def test_11_unknown_query_parameters_fail() -> None:
    for q in ("?rank=influence", "?sort=movement", "?limit=2", "?susceptibility=true"):
        assert client.get(ROSTER + q).status_code == 422
    assert client.get(DOSS.format(JOURNALIST) + "?optimise=audience").status_code == 422


def test_12_mutating_methods_fail() -> None:
    for method in (client.post, client.put, client.patch, client.delete):
        assert method(ROSTER).status_code == 405
        assert method(DOSS.format(JOURNALIST)).status_code == 405


# ── 13–15 · determinism, immutability, mutation safety ────────────────────────────────────────────


def test_13_responses_are_deterministic() -> None:
    assert client.get(ROSTER).json() == client.get(ROSTER).json()
    assert client.get(DOSS.format(JOURNALIST)).json() == client.get(DOSS.format(JOURNALIST)).json()


def test_14_responses_are_immutable() -> None:
    d = dossier("broadcast-journalist")
    with pytest.raises(ValidationError):
        d.identity.display_name = "changed"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        roster().people[0].goal_count = 99   # type: ignore[misc]


def test_15_route_calls_do_not_mutate_fixtures_or_records() -> None:
    snapshot = {
        "vp2": copy.deepcopy(vp2_fixtures.VP2_FIXTURES),
        "relationships": copy.deepcopy(vp4_fixtures.RELATIONSHIPS),
        "cast_people": copy.deepcopy(cast.PEOPLE),
        "cast_priors": copy.deepcopy(cast.PRIORS),
        "cast_exposures": copy.deepcopy(cast.EXPOSURES),
    }
    client.get(ROSTER)
    for pid in PEOPLE:
        client.get(DOSS.format(f"fict:kestral-strait:person:{pid}"))
    assert vp2_fixtures.VP2_FIXTURES == snapshot["vp2"]
    assert vp4_fixtures.RELATIONSHIPS == snapshot["relationships"]
    assert cast.PEOPLE == snapshot["cast_people"]
    assert cast.PRIORS == snapshot["cast_priors"]
    assert cast.EXPOSURES == snapshot["cast_exposures"]


# ── 16–18 · identity ──────────────────────────────────────────────────────────────────────────────


def test_16_identity_origin_remains_fixture() -> None:
    assert client.get(DOSS.format(JOURNALIST)).json()["identity"]["origin"] == "FIXTURE"


def test_17_null_portrait_remains_null() -> None:
    for p in client.get(ROSTER).json()["people"]:
        assert p["portrait_ref"] is None
    assert client.get(DOSS.format(JOURNALIST)).json()["identity"]["portrait_ref"] is None


def test_18_missing_fixture_identity_is_not_invented() -> None:
    ident = client.get(DOSS.format(JOURNALIST)).json()["identity"]
    for field in ("life_stage", "organisation_ref", "community_ref"):
        assert ident[field] is None, f"{field} was invented"


# ── 19–20 · VP-2 parity ───────────────────────────────────────────────────────────────────────────


def test_19_current_state_matches_vp2_exactly() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()["current_situation"]
    sit = fixture_for("broadcast-journalist")
    assert [g["item_id"] for g in body["goals"]] == [g.goal_id for g in sit.goals]
    assert [g["value"] for g in body["goals"]] == [g.priority for g in sit.goals]
    assert [p["value"] for p in body["pressures"]] == [p.intensity for p in sit.pressures]
    assert [r["value"] for r in body["responsibilities"]] == [r.urgency for r in sit.responsibilities]
    assert [c["item_id"] for c in body["constraints"]] == [c.constraint_id for c in sit.constraints]


def test_20_situation_origins_and_bands_match_vp2() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()["current_situation"]
    sit = fixture_for("broadcast-journalist")
    assert [p["origin"] for p in body["pressures"]] == [p.origin.value for p in sit.pressures]
    assert [p["band"] for p in body["pressures"]] == [p.intensity_band for p in sit.pressures]


# ── 21–25 · VP-3 parity, execution, no consequence ────────────────────────────────────────────────


def test_21_22_23_decision_matches_vp3_exactly() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()["decision"]
    truth = select_action(vp3_decisions.journalist_decision())
    assert body["selected_action_id"] == truth.selected_action_id
    assert tuple(body["unavailable_options"]) == truth.unavailable_options
    assert tuple(body["available_options"]) == truth.available_options
    # component totals identical, not rescored
    api_totals = {c["action_id"]: c["total"] for c in body["decision_trace"]["comparisons"]}
    vp3_totals = {c.action_id: c.total for c in truth.comparisons}
    assert api_totals == vp3_totals
    assert body["tie_occurred"] == truth.tie_occurred


def test_24_execution_status_remains_not_executed() -> None:
    for pid in PEOPLE:
        body = client.get(DOSS.format(f"fict:kestral-strait:person:{pid}")).json()
        assert body["decision"]["execution_status"] == "NOT_EXECUTED"
        assert body["decision"]["default_statement"] == "Selected by the declared rule. Not executed."
        assert body["run_integration"]["execution_status"] == "NOT_EXECUTED"


def test_25_no_world_consequence_is_exposed() -> None:
    flat = json.dumps(client.get(DOSS.format(JOURNALIST)).json()).lower()
    for banned in ("apply_to_run", "emit_event", "world_state", "run_id", "macro_state",
                   "tick_applied", "consequence_applied"):
        assert banned not in flat


# ── 26–27 · relationships ─────────────────────────────────────────────────────────────────────────


def test_26_relationship_records_match_vp4_exactly() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()["relationships"]
    truth = [r for r in vp4_fixtures.RELATIONSHIPS if r.source_ref == JOURNALIST]
    assert [r["relationship_id"] for r in body] == [r.relationship_id for r in truth]
    assert [r["relationship_kind"] for r in body] == [r.relationship_kind.value for r in truth]
    for r in body:
        for banned in ("strength", "trust_value", "influence", "loyalty", "closeness", "susceptib"):
            assert banned not in json.dumps(r).lower()


def test_27_receives_from_does_not_imply_receipt() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()
    edge = next(r for r in body["relationships"] if r["relationship_kind"] == "receives_from")
    assert "does not mean" in edge["description"]
    # receipt appears only as an explicit information record
    assert all("exposure_status" not in r for r in body["relationships"])


# ── 28–36 · histories and canonical classification ────────────────────────────────────────────────


def test_28_information_history_is_canonically_ordered() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()["information_history"]
    truth = information_history_for("broadcast-journalist")
    assert [i["information_record_id"] for i in body] == [e.information_record_id for e in truth.entries]


def test_29_not_received_remains_distinct_from_rejection() -> None:
    from app.simulation.person.history import ExposureStatus
    assert "REJECTED" not in {s.value for s in ExposureStatus}
    body = client.get(DOSS.format(JOURNALIST)).json()["information_history"]
    for rec in body:
        assert rec["exposure_status"] in ("RECEIVED", "NOT_RECEIVED_THROUGH_TICK", "UNKNOWN",
                                          "UNAVAILABLE", "NOT_MODELLED")


def test_30_belief_history_is_canonically_ordered() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()["belief_history"]["observations"]
    truth = belief_history_for("broadcast-journalist")
    assert [o["belief_history_entry_id"] for o in body] == [e.belief_history_entry_id for e in truth.entries]


def test_31_canonical_belief_classification_parity() -> None:
    """belief read-model == VP-4 history == VP-5 dossier, for the same frozen observation."""
    for pid in PEOPLE:
        proj = person_projection(pid)
        from_canonical, _ = classify_belief_outcome(
            received=proj.received_the_claim, credence=proj.calculation.final_credence,
            is_uncertain=proj.still_unsure)
        from_vp4 = belief_history_for(pid).entries[0].classification
        from_api = client.get(DOSS.format(f"fict:kestral-strait:person:{pid}")
                              ).json()["belief_history"]["observations"][0]["classification"]
        assert from_canonical.value == from_vp4.value == from_api, f"{pid} classification drift"


def test_32_belief_values_remain_exact() -> None:
    for pid, expected in (("family-spokesperson", 0.688510), ("government-minister", 0.171946),
                          ("broadcast-journalist", 0.408458)):
        assert person_projection(pid).calculation.final_credence == pytest.approx(expected, abs=1e-6)


def test_33_value_and_decision_origins_remain_distinct() -> None:
    obs = client.get(DOSS.format(JOURNALIST)).json()["belief_history"]["observations"][0]
    assert "value_origin" in obs and "decision_origin" in obs
    truth = belief_history_for("broadcast-journalist").entries[0]
    assert obs["value_origin"] == truth.value_origin.value
    assert obs["decision_origin"] == truth.decision_origin.value


def test_34_35_36_observation_count_and_no_trend_language() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()["belief_history"]
    assert body["observation_count"] == 1
    assert body["trajectory_available"] is False
    text = body["trajectory_explanation"].lower()
    assert "one recorded belief update" in text
    # trend words may appear ONLY inside a denial ("does not yet have enough history to describe a
    # longer-term pattern"), never as an assertion about the person.
    for banned in ("trend", "trajectory", "pattern", "persistent tendency", "long-term movement"):
        if banned in text:
            assert ("not " in text.split(banned)[0][-60:]
                    or "enough history to describe" in text), f"'{banned}' asserted, not denied"


# ── 37–41 · absence and boundary ──────────────────────────────────────────────────────────────────


def test_37_38_39_absence_statuses_remain_distinct() -> None:
    from app.simulation.person.history import ExposureStatus, LifecycleStatus
    for enum in (ExposureStatus, LifecycleStatus):
        vals = {s.value for s in enum}
        assert "UNKNOWN" in vals and "UNAVAILABLE" in vals and "NOT_MODELLED" in vals
        assert len({"UNKNOWN", "UNAVAILABLE", "NOT_MODELLED"} & vals) == 3


def test_40_absence_never_serialises_as_zero() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()
    ident = body["identity"]
    for f in ("portrait_ref", "life_stage", "organisation_ref", "community_ref"):
        assert ident[f] is None and ident[f] != 0
    for rec in body["information_history"]:
        if rec["exposure_status"] != "NOT_RECEIVED_THROUGH_TICK":
            assert rec["through_tick"] is None


def test_41_model_boundary_list_is_returned() -> None:
    for body in (client.get(ROSTER).json(), client.get(DOSS.format(JOURNALIST)).json()):
        mb = body["model_boundary"]
        for trait in ("intelligence", "competence", "moral worth", "susceptibility", "persuadability"):
            assert trait in mb


# ── 42–46 · plain language and technical detail ───────────────────────────────────────────────────


def test_42_situation_text_matches_state() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()
    summary = body["current_situation"]["summary"]
    sit = fixture_for("broadcast-journalist")
    assert sit.goals[0].description in summary
    assert sit.pressures[0].intensity_band in summary


def test_43_decision_text_matches_the_trace() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()["decision"]
    assert body["selected_action_label"] in body["explanation"]
    assert "nothing was executed" in body["explanation"].lower()
    blocked_label = "publish the claim immediately"
    assert blocked_label in body["explanation"]


def test_44_history_text_matches_observation_count() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()["belief_history"]
    assert ("one recorded belief update" in body["trajectory_explanation"].lower()) == (body["observation_count"] == 1)


def test_45_default_text_contains_no_prohibited_jargon() -> None:
    for body in (client.get(ROSTER).json(), client.get(DOSS.format(JOURNALIST)).json()):
        for path, text in display_strings(body):
            low = text.lower()
            for term in JARGON:
                assert term not in low, f"{path} contains '{term}': {text}"


def test_46_technical_values_remain_available_in_nested_detail() -> None:
    trace = client.get(DOSS.format(JOURNALIST)).json()["decision"]["decision_trace"]
    totals = [c["total"] for c in trace["comparisons"] if c["total"] is not None]
    assert totals and all(isinstance(t, float) for t in totals)


# ── 47–56 · B5, no implied causation, run-integration honesty ─────────────────────────────────────


def test_47_48_no_person_ranking_or_targeting_route_exists() -> None:
    # app.routes wraps included routers in _IncludedRouter (no .path) in this FastAPI version, so
    # iterating it finds nothing and proves nothing. The OpenAPI schema is the real public surface.
    paths = [p for p in app.openapi()["paths"] if "virtual-person" in p]
    assert paths, "the virtual-person routes must actually be discoverable"
    joined = " ".join(paths).lower()
    for banned in ("rank", "target", "influence", "persuad", "optimis", "audience", "segment",
                   "vulnerab", "profile"):
        assert banned not in joined
    assert len(paths) == 2   # roster + dossier only


def test_49_no_persuasion_or_susceptibility_field_exists() -> None:
    flat = json.dumps(client.get(DOSS.format(JOURNALIST)).json()).lower()
    boundary = json.dumps(client.get(DOSS.format(JOURNALIST)).json()["model_boundary"]).lower()
    # the words appear ONLY inside the model-boundary denial list
    for banned in ("susceptibility", "persuadability"):
        assert flat.count(banned) == boundary.count(banned), f"'{banned}' outside the boundary list"


def test_50_51_52_53_no_effect_transmission_trust_or_memory_implied() -> None:
    flat = json.dumps(client.get(DOSS.format(JOURNALIST)).json()).lower()
    for banned in ("influences", "propagate", "transmit", "cascade", "trust_updated",
                   "remembers", "recall", "memory_of"):
        assert banned not in flat


def test_54_55_result_kind_and_run_integration() -> None:
    for body in (client.get(ROSTER).json(), client.get(DOSS.format(JOURNALIST)).json()):
        ri = body["run_integration"]
        assert ri["result_kind"] == "packaged-virtual-person-snapshot"
        assert ri["connected_to_authoritative_run"] is False
        assert "scenario_id_note" in ri


def test_56_live_state_language_appears_only_inside_denial() -> None:
    body = client.get(DOSS.format(JOURNALIST)).json()
    denial = body["run_integration"]["explanation"].lower()
    for phrase in ("live person state", "current authoritative person", "persisted person memory",
                   "executed decision history", "real-time society state"):
        assert (f"not {phrase}" in denial or f"not a {phrase}" in denial),             f"'{phrase}' is not explicitly denied"
    outside = json.dumps({k: v for k, v in body.items() if k != "run_integration"}).lower()
    for phrase in ("live person state", "persisted person memory", "real-time society state"):
        assert phrase not in outside


# ── parity with the projection functions themselves ───────────────────────────────────────────────


def test_57_routes_add_nothing_the_projection_did_not_produce() -> None:
    assert client.get(ROSTER).json() == roster().model_dump(mode="json")
    assert client.get(DOSS.format(JOURNALIST)).json() == dossier("broadcast-journalist").model_dump(mode="json")


def test_58_all_three_dossiers_validate() -> None:
    for pid in PEOPLE:
        Dossier.model_validate(client.get(DOSS.format(f"fict:kestral-strait:person:{pid}")).json())
    Roster.model_validate(client.get(ROSTER).json())
