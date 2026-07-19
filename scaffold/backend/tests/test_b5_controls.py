"""
B5 technical controls — the eighteen tests required by the founder-approved baseline.

Canonical baseline: `docs/safety/B5-TECHNICAL-CONTROLS.md`.

Each test names the control it proves. A control is not enforced until it has both a code path and
a test here, and hosted CI is green — the document says so explicitly, and this file is the other
half of that statement.

Test numbering follows the baseline's "required tests" list exactly, so the mapping is auditable
without cross-referencing.
"""

from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.safety import (
    FICTION_DISCLOSURE,
    ORIGIN_VOCABULARY,
    B5Violation,
    FictionalTargetRegistry,
    absent_value,
    assert_fictional_manifest,
    assert_no_persuasion_optimisation,
    assert_no_protected_traits,
    assert_not_real_population,
    assert_origin,
    assert_packaged_scenario,
    assert_projection_provenance,
    engine_value,
    fictional_world_metadata,
    fixture_value,
    load_packaged_scenario,
)

client = TestClient(app)
SCENARIO_ID = "kestral-strait"


@pytest.fixture(scope="module")
def scenario() -> dict:
    return load_packaged_scenario(SCENARIO_ID)


@pytest.fixture(scope="module")
def registry(scenario: dict) -> FictionalTargetRegistry:
    return FictionalTargetRegistry(scenario, SCENARIO_ID)


# ── 1-5: B5-01 and B5-02 ─────────────────────────────────────────────────────────────────────────


def test_01_valid_packaged_fictional_scenario_loads(scenario: dict) -> None:
    """B5-01/B5-02: the allowlisted scenario loads and declares a fictional world."""
    assert scenario["world_mode"] == "fictional"
    assert scenario["scenario_id"] == SCENARIO_ID


def test_02_manifest_without_world_mode_is_rejected(scenario: dict) -> None:
    """B5-01: absence is rejected. There is NO default-to-fictional path."""
    stripped = {k: v for k, v in scenario.items() if k != "world_mode"}
    with pytest.raises(B5Violation) as exc:
        assert_fictional_manifest(stripped, SCENARIO_ID)
    assert exc.value.control == "B5-01"
    assert "does not declare" in str(exc.value)


@pytest.mark.parametrize(
    "bad_mode",
    ["real", "real_world", "historical", "FICTIONAL", "fictional ", "", None, 1, {"mode": "x"}],
)
def test_03_non_fictional_world_mode_is_rejected(scenario: dict, bad_mode: object) -> None:
    """B5-01: unknown, malformed and non-fictional values all fail closed."""
    with pytest.raises(B5Violation) as exc:
        assert_fictional_manifest({**scenario, "world_mode": bad_mode}, SCENARIO_ID)
    assert exc.value.control == "B5-01"


@pytest.mark.parametrize(
    "bad_id",
    ["not-a-scenario", "real-world-uk", "kestral-strait-copy", "", None, 42],
)
def test_04_scenario_outside_the_allowlist_is_rejected(bad_id: object) -> None:
    """B5-02: allowlist membership is the whole check."""
    with pytest.raises(B5Violation) as exc:
        assert_packaged_scenario(bad_id)
    assert exc.value.control == "B5-02"


@pytest.mark.parametrize(
    "hostile",
    [
        "../../etc/passwd",
        "../scenarios/kestral-strait",
        "/etc/passwd",
        "C:\\Windows\\win.ini",
        "https://example.invalid/scenario.json",
        "http://example.invalid/s.json",
        "file:///etc/passwd",
        "kestral-strait/../../secret",
    ],
)
def test_05_file_url_and_import_paths_are_unavailable(hostile: str) -> None:
    """
    B5-02: uploads, URLs, external datasets and traversal are refused.

    Note WHERE this is refused: the allowlist rejects these before any filesystem access, so the
    traversal strings never reach `Path`. There is also deliberately no loader that accepts a path,
    a URL or an upload — the absence of that function is itself the control.
    """
    with pytest.raises(B5Violation) as exc:
        load_packaged_scenario(hostile)
    assert exc.value.control == "B5-02"

    import app.safety.scenarios as scen

    for forbidden in ("load_from_path", "load_from_url", "load_from_upload", "import_scenario"):
        assert not hasattr(scen, forbidden), f"a non-packaged load path exists: {forbidden}"


# ── 6-8: B5-03 ───────────────────────────────────────────────────────────────────────────────────


def test_06_valid_fictional_registry_target_is_accepted(registry: FictionalTargetRegistry) -> None:
    """B5-03: a typed identifier resolving inside the active world is accepted."""
    cohort = sorted(registry.known("cohort"))[0]
    ref = registry.resolve(f"fict:{SCENARIO_ID}:cohort:{cohort}")
    assert ref.entity_id == cohort
    assert ref.kind == "cohort"
    assert str(ref) == f"fict:{SCENARIO_ID}:cohort:{cohort}"

    agent = sorted(registry.known("agent"))[0]
    assert registry.resolve(f"fict:{SCENARIO_ID}:agent:{agent}").kind == "agent"


@pytest.mark.parametrize(
    "bad_target",
    [
        "coastal fishing families",          # free-text population
        "The Prime Minister",                # free-text person
        "Reuters",                           # free-text organisation
        "fict:kestral-strait:cohort:nobody",  # unresolved entity
        "fict:kestral-strait:planet:earth",  # unknown kind
        "kestral-strait:cohort:port",        # missing prefix
        "",
        None,
        12345,
    ],
)
def test_07_free_text_and_unresolved_targets_are_rejected(
    registry: FictionalTargetRegistry, bad_target: object
) -> None:
    """B5-03: fails closed. Never best-effort matched, never fuzzy matched."""
    with pytest.raises(B5Violation) as exc:
        registry.resolve(bad_target)
    assert exc.value.control == "B5-03"


@pytest.mark.parametrize(
    "cross_world",
    [
        "fict:another-world:cohort:port-workers",
        "fict:real-world:cohort:voters",
        "real:kestral-strait:cohort:coastal-creole-fishing",
    ],
)
def test_08_cross_world_target_identifiers_are_rejected(
    registry: FictionalTargetRegistry, cross_world: str
) -> None:
    """B5-03: the world segment makes a cross-world reference structurally refusable."""
    with pytest.raises(B5Violation) as exc:
        registry.resolve(cross_world)
    assert exc.value.control == "B5-03"


# ── 9: B5-04 ─────────────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "payload",
    [
        {"segment_by": "ethnicity"},
        {"filters": {"religion": "any"}},
        {"targeting": [{"trait": "sexual_orientation"}]},
        {"rank_by": "disability"},
        {"audience": {"postcode": "KS1"}},           # declared proxy
        {"weights": {"language_spoken": 0.4}},       # declared proxy
        {"cohort_scores": {"manipulability": 0.7}},  # prohibited inference
        {"model": {"loyalty": 0.2}},                 # prohibited inference
    ],
)
def test_09_protected_trait_targeting_fields_are_rejected(payload: dict) -> None:
    """B5-04: protected traits, declared proxies and identity inferences all refused."""
    with pytest.raises(B5Violation) as exc:
        assert_no_protected_traits(payload)
    assert exc.value.control == "B5-04"


def test_09b_identity_may_still_shape_exposure_and_experience() -> None:
    """
    B5-04, second clause — the boundary this control must NOT over-reach past.

    Identity may affect lived experience, relationships, discrimination, institutional access and
    media exposure. Only SELECTION and RANKING inputs are refused. A control that blocked the
    modelling too would break the thing the project exists to do.
    """
    assert_no_protected_traits(
        {
            "cohort": {
                "media_exposure": 0.6,
                "institutional_access": 0.3,
                "experienced_discrimination": 0.4,
                "income_sensitivity": 0.8,
            }
        }
    )


# ── 10: B5-05 ────────────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "payload",
    [
        {"rank_by": "susceptibility"},
        {"compute": ["persuadability"]},
        {"sort": "most_influenceable"},
        {"optimise": {"audience_optimisation": True}},
        {"objective": "maximise_belief_change"},
        {"scores": {"vulnerability_score": 0.9}},
        {"select": {"optimal_audience": "any"}},
        {"metrics": {"conversion_likelihood": 0.5}},
    ],
)
def test_10_persuadability_and_susceptibility_fields_are_rejected(payload: dict) -> None:
    """B5-05: applies to fictional and real audiences alike for public v0.1."""
    with pytest.raises(B5Violation) as exc:
        assert_no_persuasion_optimisation(payload)
    assert exc.value.control == "B5-05"


# ── 11: B5-06 ────────────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "payload",
    [
        {"world": "real"},
        {"world_mode": "real_world"},
        {"population_scope": "actual"},
        {"audience_scope": "live_population"},
        {"nested": {"scope": "production"}},
    ],
)
def test_11_real_population_requests_are_rejected(payload: dict) -> None:
    """
    B5-06: rejected, NOT silently converted to a fictional analogue.

    Automatic rewriting would tell the caller the request was acceptable and would hide the refusal
    from anyone auditing the exchange.
    """
    with pytest.raises(B5Violation) as exc:
        assert_not_real_population(payload)
    assert exc.value.control == "B5-06"


def test_11b_demo_endpoint_refuses_a_real_population_request() -> None:
    """B5-06 at the API boundary, with the refusal visible in the response."""
    r = client.post(
        "/api/demo/kestral-strait/run",
        json={"mode": "incident", "ticks": 3, "world": "real_world"},
    )
    assert r.status_code in (400, 422)
    if r.status_code == 400:
        assert "B5-06" in r.json()["detail"]


# ── 12: safe harbor ──────────────────────────────────────────────────────────────────────────────


def test_12_fictional_aggregate_narrative_propagation_remains_allowed() -> None:
    """
    Safe harbor: enforcement must not over-reach into the modelling the project exists to do.

    Aggregate fictional propagation, adoption and belief divergence stay permitted. If this test
    ever fails, the controls have become too broad, not too narrow.
    """
    permitted = {
        "narrative_adoption": {"coastal-creole-fishing": 0.31},
        "collective_activity": 0.148,
        "narrative_attention": 0.145,
        "population_weighted_concern": 0.1416,
        "defensive_intervention": "publish_verified_evidence",
    }
    assert_no_protected_traits(permitted)
    assert_no_persuasion_optimisation(permitted)
    assert_not_real_population(permitted)

    r = client.post("/api/demo/kestral-strait/run", json={"mode": "incident", "ticks": 5})
    assert r.status_code == 200
    assert r.json()["projection"]["stages"]


# ── 13-16: B5-07 and B5-08 ───────────────────────────────────────────────────────────────────────


def test_13_api_responses_contain_fictional_world_metadata(scenario: dict) -> None:
    """B5-07: structured metadata on the response, not inferable prose."""
    r = client.post("/api/demo/kestral-strait/run", json={"mode": "incident", "ticks": 3})
    assert r.status_code == 200
    meta = r.json()["fictional_world"]
    assert meta["world_mode"] == "fictional"
    assert meta["fictional"] is True
    assert meta["scenario_id"] == SCENARIO_ID
    assert meta["disclosure"] == FICTION_DISCLOSURE
    assert meta["scenario_version"]

    direct = fictional_world_metadata(scenario, SCENARIO_ID)
    assert direct["disclosure"] == FICTION_DISCLOSURE


def test_14_every_visible_value_carries_origin_information() -> None:
    """B5-08: every user-visible record in the projection declares a valid origin."""
    r = client.post("/api/demo/kestral-strait/run", json={"mode": "incident", "ticks": 5})
    projection = r.json()["projection"]
    assert_projection_provenance(projection)

    for group in ("stages", "cohorts", "government_options"):
        entries = projection[group]
        assert entries, f"{group} is empty; coverage cannot be asserted over nothing"
        for entry in entries:
            # Canonicalised: the wire format is lowercase, the vocabulary is the closed set.
            assert assert_origin(entry["origin"]) in ORIGIN_VOCABULARY


def test_15_fixture_values_cannot_be_labelled_engine() -> None:
    """B5-08: the falsehood this control exists to prevent."""
    fixture = fixture_value(0.5, scenario_id=SCENARIO_ID, scenario_version="1.0.0")
    assert fixture.origin == "FIXTURE"

    # Invented origin variants are refused, so a fixture cannot be smuggled in under a
    # near-miss label. ('engine' IS valid - it is the wire spelling of ENGINE.)
    for invented in ("ENGINE_DERIVED", "engine-derived", "computed", "live", "real"):
        with pytest.raises(B5Violation):
            assert_origin(invented)
    with pytest.raises(B5Violation):
        assert_projection_provenance({"stages": [{"origin": "engine_derived", "value": 0.1}]})
    # A record with no origin at all is refused rather than defaulted to ENGINE.
    with pytest.raises(B5Violation):
        assert_projection_provenance({"stages": [{"value": 0.1}]})

    engine = engine_value(0.5, scenario_id=SCENARIO_ID, scenario_version="1.0.0", tick=3)
    assert engine.origin == "ENGINE"
    assert engine.as_dict()["origin"] != fixture.as_dict()["origin"]


@pytest.mark.parametrize("origin", ["UNKNOWN", "UNAVAILABLE"])
def test_16_unknown_and_unavailable_do_not_render_as_zero(origin: str) -> None:
    """
    B5-08: absence is not zero.

    `render()` returns None so a caller cannot format an absence as a number by accident, and
    constructing an absence WITH a value is refused outright.
    """
    absent = absent_value(origin, scenario_id=SCENARIO_ID, scenario_version="1.0.0")
    assert absent.render() is None
    assert absent.render() != 0
    assert absent.is_absent is True
    assert absent.as_dict()["value"] is None

    with pytest.raises(B5Violation):
        absent_value(origin, scenario_id=SCENARIO_ID, scenario_version="1.0.0").__class__(
            value=0.0,
            origin=origin,
            epistemic_status="UNKNOWN",
            scenario_id=SCENARIO_ID,
            scenario_version="1.0.0",
        )


# ── 17: B5-07 disclosure, including crop survival ────────────────────────────────────────────────


def test_17_global_and_crop_safe_disclosures_are_present() -> None:
    """
    B5-07: the disclosure reaches the client, and the frontend carries it per panel.

    The per-panel requirement is asserted in the frontend suite (tests/honesty.test.ts, 'crop
    safety'); this asserts the backend half — the wording is exact and travels on the payload, so a
    UI cannot paraphrase it into something weaker.
    """
    r = client.post("/api/demo/kestral-strait/run", json={"mode": "incident", "ticks": 3})
    body = r.json()
    assert body["fictional_world"]["disclosure"] == FICTION_DISCLOSURE
    assert any(FICTION_DISCLOSURE in line for line in body["limitations"])

    frontend_tests = (
        __import__("pathlib").Path(__file__).parents[2] / "frontend" / "tests" / "honesty.test.ts"
    )
    source = frontend_tests.read_text(encoding="utf-8")
    assert "crop safety" in source
    assert "fictional-world marker" in source


# ── 18: existing suites ──────────────────────────────────────────────────────────────────────────


def test_18_existing_engine_and_api_behaviour_is_unchanged() -> None:
    """
    B5-18: enforcement must not alter simulation behaviour.

    The full P0.4/P0.4A/P0.5/API suites run alongside this file; this asserts the specific property
    that matters — the run the controls now guard produces the same numbers as before.
    """
    r = client.post("/api/demo/kestral-strait/run", json={"mode": "incident", "ticks": 20})
    assert r.status_code == 200
    body = r.json()

    stages = {s["field"]: s["value"] for s in body["projection"]["stages"]}
    assert stages["political_pressure"] == pytest.approx(0.149509, abs=1e-6)
    assert stages["insurer_risk"] == pytest.approx(0.577273, abs=1e-6)
    assert body["seed"] == 88213
    assert body["projection"]["rule_pack_version"] == "kestral-causal-slice@1.0.0"

    # Determinism across two identical requests through the enforced path.
    again = client.post("/api/demo/kestral-strait/run", json={"mode": "incident", "ticks": 20})
    assert json.dumps(again.json()["projection"], sort_keys=True) == json.dumps(
        body["projection"], sort_keys=True
    )


def test_18b_any_chain_mechanism_may_be_disabled_independently() -> None:
    """
    Verifies the counterfactual claim the public messaging depends on: EVERY mechanism in the
    chain can be disabled, not only the default one.
    """
    from app.simulation.mechanisms import CHAIN

    for mech in CHAIN:
        r = client.post(
            "/api/demo/kestral-strait/run",
            json={"mode": "counterfactual", "ticks": 5, "disabled_mechanism": mech.id},
        )
        assert r.status_code == 200, f"{mech.id} could not be disabled: {r.text}"
        assert r.json()["disabled_mechanism"] == mech.id
