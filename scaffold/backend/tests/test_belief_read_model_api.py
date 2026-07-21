"""
Read-only belief API — projection, honesty and B5 route evidence.

The central properties: the API returns engine-backed data, never mutates anything, never presents
a packaged snapshot as live run state, keeps the three entity kinds structurally distinct, and
refuses anything that is not a declared fictional entity.
"""

from __future__ import annotations

import copy

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.simulation.belief import cast
from app.simulation.belief.organisations import OrganisationInput, aggregate
from app.simulation.belief.projection import (
    NOT_MODELLED,
    CohortProjection,
    OrganisationProjection,
    PersonProjection,
    cohort_projection,
    landscape_projection,
    organisation_projection,
    person_projection,
)
from app.simulation.belief.thresholds import ThresholdKind
from app.simulation.belief.update import UpdateInput, apply_update

client = TestClient(app)

LANDSCAPE = "/api/belief/kestral-strait/landscape"
DOSSIER = "/api/belief/kestral-strait/dossier/{}"
JOURNALIST = "fict:kestral-strait:person:broadcast-journalist"
BROADCASTER = "fict:kestral-strait:organisation:public-broadcaster"
INLAND = "fict:kestral-strait:cohort:inland-households"
P = "P-WARNINGS-IGNORED"

#: Never permitted in a default display field. Exact values live in `calculation`.
JARGON = ("credence", "provenance", "contextual threshold", "update weight", "alignment",
          "aggregation", "state mass", "denominator", "propensity", "epistemic")

#: Fields a client renders directly. `calculation` is deliberately excluded.
DISPLAY_FIELDS = ("headline", "view_before", "view_now", "movement", "confidence_statement",
                  "exposure_statement", "reasons", "internal_views_statement",
                  "cohesion_statement", "official_position_statement",
                  "action_direction_statement", "action_strength_statement", "change_statement",
                  "result_statement", "reason", "source_statement", "exposure_statement")


def display_text(obj, path="") -> list[tuple[str, str]]:
    """Every string in a display field, with its path. Skips `calculation` entirely."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "calculation":
                continue
            if k in DISPLAY_FIELDS and isinstance(v, str):
                found.append((f"{path}.{k}", v))
            elif k in DISPLAY_FIELDS and isinstance(v, list):
                found += [(f"{path}.{k}[{i}]", s) for i, s in enumerate(v) if isinstance(s, str)]
            else:
                found += display_text(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            found += display_text(item, f"{path}[{i}]")
    return found


# ══ ENGINE-BACKED ═══════════════════════════════════════════════════════════════════════════════


def test_01_landscape_returns_engine_backed_data() -> None:
    body = client.get(LANDSCAPE).json()
    ev = cast.SHARED_EVENT
    prior = cast.PRIORS[("broadcast-journalist", P)]
    expected = apply_update(UpdateInput(
        prior_credence=prior["credence"], prior_confidence=prior["confidence"],
        prior_salience=prior["salience"],
        evidentiary_threshold=cast.threshold_registry().value_for(
            "broadcast-journalist", P, expect=ThresholdKind.verification),
        source_trust=cast.SOURCE_TRUST["broadcast-journalist"][ev["source_category"]],
        evidence_strength=ev["evidence_strength"], exposure_intensity=0.95, relay_factor=1.0,
        relevance=cast.RELEVANCE["broadcast-journalist"], claim_direction=1))
    dossier = client.get(DOSSIER.format(JOURNALIST)).json()
    assert dossier["calculation"]["final_credence"] == pytest.approx(expected.credence)
    assert body["claim"]["proposition_id"] == P


def test_02_all_twelve_entities_appear_in_the_landscape() -> None:
    body = client.get(LANDSCAPE).json()
    assert len(body["people"]) == 3
    assert len(body["organisations"]) == 3
    assert len(body["cohorts"]) == 6
    ids = {e["entity_id"] for group in ("people", "organisations", "cohorts") for e in body[group]}
    assert ids == (
        {p["person_id"] for p in cast.PEOPLE}
        | {o["organisation_id"] for o in cast.ORGANISATIONS}
        | {c["cohort_id"] for c in cast.COHORTS}
    )
    assert len(ids) == 12


def test_03_landscape_answers_who_received_and_who_did_not() -> None:
    body = client.get(LANDSCAPE).json()
    cohorts = {c["entity_id"]: c for c in body["cohorts"]}
    assert cohorts["inland-households"]["received_the_claim"] is False
    assert cohorts["port-workers"]["received_the_claim"] is True
    assert body["population_not_reached"] == 402_000
    assert body["population_total"] == 1_001_000


def test_04_landscape_shows_support_oppose_and_withhold() -> None:
    orgs = {o["entity_id"]: o for o in client.get(LANDSCAPE).json()["organisations"]}
    assert "supports" in orgs["coastal-workers-union"]["result_statement"].lower()
    assert "rejects" in orgs["national-government"]["result_statement"].lower()
    assert "no firm position" in orgs["public-broadcaster"]["result_statement"].lower()


def test_05_all_three_dossier_shapes_validate() -> None:
    PersonProjection.model_validate(client.get(DOSSIER.format(JOURNALIST)).json())
    OrganisationProjection.model_validate(client.get(DOSSIER.format(BROADCASTER)).json())
    CohortProjection.model_validate(client.get(DOSSIER.format(INLAND)).json())


def test_06_the_three_kinds_are_structurally_distinct() -> None:
    """Not one generic profile with blank fields."""
    person = set(client.get(DOSSIER.format(JOURNALIST)).json())
    org = set(client.get(DOSSIER.format(BROADCASTER)).json())
    cohort = set(client.get(DOSSIER.format(INLAND)).json())
    assert person != org != cohort != person
    assert "confidence_statement" in person and "confidence_statement" not in org
    assert "internal_views" in org and "internal_views" not in person
    assert "breakdown_status" in cohort and "breakdown_status" not in person
    assert "population_represented" in cohort and "population_represented" not in org


def strip_layers(body: dict) -> dict:
    """
    Drop the declared-absence lists before scanning for banned words.

    Those lists NAME the things that are not modelled - 'intelligence', 'competence',
    'emotional state' - so scanning them for those words finds the honesty mechanism and calls
    it a violation. An earlier version of this test did exactly that.
    """
    out = {k: v for k, v in body.items() if k not in ("layers", "not_modelled")}
    return out


def test_07_person_carries_no_capability_or_influence_field() -> None:
    flat = str(strip_layers(client.get(DOSSIER.format(JOURNALIST)).json())).lower()
    for banned in ("intelligence", "competence", "susceptib", "persuad", "influence_rank",
                   "influence rank", "audience"):
        assert banned not in flat


def test_08_organisation_has_no_emotion_or_personal_confidence() -> None:
    body = client.get(DOSSIER.format(BROADCASTER)).json()
    assert body["confidence_status"] == "NOT_MODELLED"
    flat = str(strip_layers(body)).lower()
    for banned in ("emotion", "feels", "mood", "memory of"):
        assert banned not in flat


# ══ RUN-INTEGRATION HONESTY ═════════════════════════════════════════════════════════════════════


def test_09_response_never_claims_to_be_live_run_state() -> None:
    body = client.get(LANDSCAPE).json()
    ri = body["run_integration"]
    assert ri["connected_to_authoritative_run"] is False
    assert ri["result_kind"] == "packaged-belief-snapshot"
    assert "not live run state" in ri["explanation"].lower()
    assert "not persisted" in ri["explanation"].lower()
    # The forbidden labels may appear ONLY inside an explicit denial.
    denial = ri["explanation"].lower()
    for forbidden in ("live run state", "current authoritative belief state",
                      "persisted person state"):
        assert f"not {forbidden}" in denial, f"'{forbidden}' is not explicitly denied"
    outside = str({k: v for k, v in body.items() if k != "run_integration"}).lower()
    for forbidden in ("live run state", "authoritative belief state", "persisted person"):
        assert forbidden not in outside


def test_10_the_shared_scenario_id_defect_is_disclosed() -> None:
    note = client.get(LANDSCAPE).json()["scenario_id_note"]
    assert "disjoint" in note and "kestral-strait" in note


# ══ B5 ROUTE CONTROLS ═══════════════════════════════════════════════════════════════════════════


def test_11_typed_fictional_ids_resolve() -> None:
    for tid in (JOURNALIST, BROADCASTER, INLAND):
        assert client.get(DOSSIER.format(tid)).status_code == 200


def test_12_cross_world_ids_fail() -> None:
    r = client.get(DOSSIER.format("fict:some-other-world:person:broadcast-journalist"))
    assert r.status_code == 422
    assert "cross-world" in r.json()["detail"]


def test_13_free_text_targets_fail() -> None:
    for target in ("BBC News", "the BBC", "Reuters", "a real journalist", "broadcast-journalist"):
        assert client.get(DOSSIER.format(target)).status_code == 422


def test_14_unknown_entities_fail() -> None:
    assert client.get(DOSSIER.format("fict:kestral-strait:person:nobody")).status_code == 404
    assert client.get(DOSSIER.format("fict:kestral-strait:cohort:invented")).status_code == 404


def test_15_the_legacy_agent_kind_is_refused() -> None:
    r = client.get(DOSSIER.format("fict:kestral-strait:agent:national-government"))
    assert r.status_code == 422
    assert "belief-slice entity kind" in r.json()["detail"]


def test_16_unknown_query_fields_fail_rather_than_being_ignored() -> None:
    for params in ("?rank=influence", "?optimise=audience", "?limit=3", "?world=real_world"):
        assert client.get(LANDSCAPE + params).status_code == 422
    assert client.get(DOSSIER.format(JOURNALIST) + "?susceptibility=true").status_code == 422


def test_17_no_route_accepts_a_body_or_mutating_method() -> None:
    assert client.post(LANDSCAPE).status_code == 405
    assert client.put(DOSSIER.format(JOURNALIST)).status_code == 405
    assert client.delete(DOSSIER.format(JOURNALIST)).status_code == 405


def test_18_no_ranking_or_targeting_operation_is_exposed() -> None:
    # DEFECT FOUND IN VP-5 REVIEW: this previously iterated `app.routes`, which in this FastAPI
    # version wraps included routers in `_IncludedRouter` objects carrying no `.path`. The list was
    # always EMPTY, so the assertions below passed vacuously and proved nothing. The OpenAPI schema
    # is the real public surface.
    paths = [p for p in app.openapi()["paths"] if "/belief" in p]
    assert paths, "the belief routes must actually be discoverable"
    joined = " ".join(paths).lower()
    for banned in ("rank", "target", "influence", "persuad", "optimis", "audience", "segment"):
        assert banned not in joined
    body = client.get(LANDSCAPE).json()
    # Entities are returned in declaration order, never sorted by movement — a sorted list is a
    # ranking whatever it is called.
    assert [p["entity_id"] for p in body["people"]] == [p["person_id"] for p in cast.PEOPLE]
    assert [c["entity_id"] for c in body["cohorts"]] == [c["cohort_id"] for c in cast.COHORTS]


# ══ MUTATION SAFETY AND DETERMINISM ═════════════════════════════════════════════════════════════


def test_19_responses_are_deterministic() -> None:
    a = client.get(LANDSCAPE).json()
    b = client.get(LANDSCAPE).json()
    assert a == b
    assert client.get(DOSSIER.format(JOURNALIST)).json() == \
           client.get(DOSSIER.format(JOURNALIST)).json()


def test_20_the_api_mutates_no_fixture_state() -> None:
    """Deep-copy every fixture, exercise every route, compare."""
    before = {
        name: copy.deepcopy(getattr(cast, name))
        for name in ("PEOPLE", "ORGANISATIONS", "COHORTS", "PRIORS", "EXPOSURES", "SOURCE_TRUST",
                     "RELEVANCE", "THRESHOLD_RECORDS", "SHARED_EVENT", "PROPOSITIONS", "DESCRIPTIVE")
    }
    client.get(LANDSCAPE)
    for tid in (JOURNALIST, BROADCASTER, INLAND):
        client.get(DOSSIER.format(tid))
    for name, snapshot in before.items():
        assert getattr(cast, name) == snapshot, f"{name} was mutated by a read-only request"


def test_21_projections_are_immutable() -> None:
    person = person_projection("broadcast-journalist")
    with pytest.raises(Exception):
        person.headline = "something else"  # type: ignore[misc]


def test_22_no_engine_model_is_returned_directly() -> None:
    """The response is a projection type, not an engine result."""
    from app.simulation.belief.update import UpdateResult
    from app.simulation.belief.cohorts import CohortReport
    from app.simulation.belief.organisations import OrganisationResult
    assert not issubclass(PersonProjection, UpdateResult.__class__)
    for engine_field in ("signal_weight", "skipped_reason", "trace"):
        assert engine_field not in set(client.get(DOSSIER.format(JOURNALIST)).json())
    assert "explanation" not in set(client.get(DOSSIER.format(BROADCASTER)).json())
    assert "public_sentence" not in set(client.get(DOSSIER.format(INLAND)).json())


# ══ PLAIN LANGUAGE MATCHES STRUCTURED STATE ═════════════════════════════════════════════════════


def test_23_person_text_matches_the_structured_result() -> None:
    body = client.get(DOSSIER.format(JOURNALIST)).json()
    assert body["still_unsure"] is True
    assert "unsure" in body["headline"].lower()
    assert body["view_now"] == "Unsure"
    assert body["calculation"]["delta_credence"] > 0
    assert "towards" in body["movement"]
    assert body["received_the_claim"] is True


def test_24_organisation_text_matches_the_structured_result() -> None:
    body = client.get(DOSSIER.format(BROADCASTER)).json()
    assert body["official_position"] == "uncertain"
    assert body["official_position_statement"] == "No firm position"
    assert body["position_strength"] == "withheld"
    assert body["action_direction"] == "withhold"
    assert body["calculation"]["action_intensity"] == 0.0
    assert "no force" in body["action_strength_statement"].lower()
    assert "50%" in body["headline"] and "undecided" in body["headline"]


def test_25_cohort_text_matches_exposure_and_retained_prior() -> None:
    body = client.get(DOSSIER.format(INLAND)).json()
    assert body["received_the_claim"] is False
    assert body["exposure_status"] == "unexposed"
    assert body["calculation"]["event_driven_delta"] == 0.0
    assert body["calculation"]["current_credence"] == cast.PRIORS[("inland-households", P)]["credence"]
    assert body["view_before"] == body["view_now"]
    assert "carried forward" in body["change_statement"]
    assert body["origin"]["value_origin"] == "FIXTURE"
    assert body["origin"]["decision_origin"] == "ENGINE"


def test_26_wording_is_derived_not_authored_per_entity() -> None:
    """No entity id may appear in the wording tables."""
    import inspect
    from app.simulation.belief import projection as mod
    source = inspect.getsource(mod)
    table_src = source[source.index("# ── Wording bands"):source.index("# ── Projection models")]
    for entity in ([p["person_id"] for p in cast.PEOPLE]
                   + [o["organisation_id"] for o in cast.ORGANISATIONS]
                   + [c["cohort_id"] for c in cast.COHORTS]):
        assert entity not in table_src, f"wording is keyed to '{entity}' rather than to state"


def test_27_identical_structured_state_produces_identical_wording() -> None:
    """Two organisations with the same declared inputs must read the same, whoever they are."""
    a = aggregate(OrganisationInput(internal_blocs={"support": .7, "oppose": .1, "uncertain": .2},
                                    cohesion=.81, prior_alignment=.62, update_weight=.26928,
                                    target_alignment=1.0))
    b = aggregate(OrganisationInput(internal_blocs={"support": .7, "oppose": .1, "uncertain": .2},
                                    cohesion=.81, prior_alignment=.62, update_weight=.26928,
                                    target_alignment=1.0))
    assert a.official_position is b.official_position
    assert a.action_intensity == b.action_intensity


# ══ EXACT VALUES, JARGON AND ABSENCE ════════════════════════════════════════════════════════════


def test_28_exact_values_are_only_in_technical_detail_fields() -> None:
    body = client.get(DOSSIER.format(JOURNALIST)).json()
    assert body["calculation"]["final_credence"] == pytest.approx(0.408458, abs=1e-6)
    for _, text in display_text(body):
        assert "0.40" not in text and "0.058" not in text, f"a raw value leaked into: {text}"


def test_29_default_display_fields_contain_no_prohibited_jargon() -> None:
    for payload in (client.get(LANDSCAPE).json(),
                    client.get(DOSSIER.format(JOURNALIST)).json(),
                    client.get(DOSSIER.format(BROADCASTER)).json(),
                    client.get(DOSSIER.format(INLAND)).json()):
        for path, text in display_text(payload):
            lowered = text.lower()
            for term in JARGON:
                assert term not in lowered, f"{path} contains '{term}': {text}"


def test_30_cohort_breakdown_stays_unavailable_and_no_shares_are_returned() -> None:
    for cohort in cast.COHORTS:
        body = client.get(DOSSIER.format(f"fict:kestral-strait:cohort:{cohort['cohort_id']}")).json()
        assert body["breakdown_status"] == "UNAVAILABLE"
        assert body["breakdown_reason"]
        for invented in ("leaning_toward_share", "uncertain_share", "leaning_against_share",
                         "state_masses", "breakdown_shares"):
            assert invented not in str(body), f"{invented} was returned for a group with no masses"


def test_31_cohort_confidence_stays_not_modelled() -> None:
    body = client.get(DOSSIER.format(INLAND)).json()
    assert body["confidence_status"] == "NOT_MODELLED"
    assert body["confidence_reason"]
    assert "confidence_statement" not in body


def test_32_both_layer_lists_are_always_returned() -> None:
    for tid in (JOURNALIST, BROADCASTER, INLAND):
        layers = client.get(DOSSIER.format(tid)).json()["layers"]
        assert layers["modelled"] and layers["not_modelled"]
        for absent in ("memory", "relationships", "changing trust", "path dependence"):
            assert any(absent in item for item in layers["not_modelled"])
    assert set(NOT_MODELLED) <= set(client.get(LANDSCAPE).json()["not_modelled"])


def test_33_fixture_and_engine_origins_stay_distinct() -> None:
    """The engine deciding not to change a value is not the engine producing it."""
    inland = client.get(DOSSIER.format(INLAND)).json()
    assert inland["origin"]["value_origin"] == "FIXTURE"
    assert inland["origin"]["decision_origin"] == "ENGINE"
    assert "never received" in inland["origin"]["note"] or "never received the claim" in \
        inland["origin"]["note"].lower() or "did not" in inland["origin"]["note"].lower()
    person = client.get(DOSSIER.format(JOURNALIST)).json()
    assert person["origin"]["value_origin"] == "ENGINE"
    assert person["entity"]["description_origin"] == "FIXTURE"


def test_34_unknown_and_unavailable_never_serialise_as_zero() -> None:
    def walk(node, path=""):
        if isinstance(node, dict):
            statuses = "".join(str(v) for k, v in node.items()
                               if isinstance(v, str)
                               and (k.endswith("status") or k.endswith("origin")))
            if "UNAVAILABLE" in statuses or "UNKNOWN" in statuses or "NOT_MODELLED" in statuses:
                for k, v in node.items():
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        assert v != 0 or k in ("introduced_at_tick", "exposed_denominator",
                                               "exposure_missing_denominator",
                                               "unexposed_denominator", "event_driven_delta"), \
                            f"{path}.{k} is 0 on a record whose status is an absence"
            for k, v in node.items():
                walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, f"{path}[{i}]")

    for tid in (JOURNALIST, BROADCASTER, INLAND):
        walk(client.get(DOSSIER.format(tid)).json())


def test_35_projection_functions_agree_with_the_routes() -> None:
    """The route adds nothing the projection layer did not produce."""
    assert client.get(DOSSIER.format(JOURNALIST)).json() == \
        person_projection("broadcast-journalist").model_dump(mode="json")
    assert client.get(DOSSIER.format(BROADCASTER)).json() == \
        organisation_projection("public-broadcaster").model_dump(mode="json")
    assert client.get(DOSSIER.format(INLAND)).json() == \
        cohort_projection("inland-households").model_dump(mode="json")
    assert client.get(LANDSCAPE).json() == landscape_projection().model_dump(mode="json")
