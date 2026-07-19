"""First live engine→UI integration — the demonstration API boundary.

These assert the properties that make the endpoint honest: that it is deterministic, that it
persists nothing, that a counterfactual is distinguishable from a baseline, and that no network
or model call happens on the path.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
RUN = "/api/demo/kestral-strait/run"


def post(mode: str, **kw) -> dict:
    r = client.post(RUN, json={"mode": mode, **kw})
    assert r.status_code == 200, r.text
    return r.json()


def test_baseline_response_is_zero_where_expected() -> None:
    p = post("baseline")["projection"]
    by_field = {s["field"]: s["value"] for s in p["stages"]}
    for field in ("incident_severity", "insurer_risk", "rerouting_level",
                  "employment_pressure", "political_pressure"):
        assert by_field[field] == 0.0, f"{field} moved in a baseline run"
    assert all(o["value"] == "AVAILABLE" for o in p["government_options"])


def test_incident_response_contains_real_downstream_effects() -> None:
    p = post("incident")["projection"]
    by_field = {s["field"]: s["value"] for s in p["stages"]}
    assert by_field["incident_severity"] > 0.0
    assert by_field["insurer_risk"] > 0.0
    assert by_field["rerouting_level"] > 0.0
    assert by_field["employment_pressure"] > 0.0
    assert by_field["political_pressure"] > 0.0
    assert any(o["value"] != "AVAILABLE" for o in p["government_options"])


def test_counterfactual_identifies_the_disabled_mechanism() -> None:
    body = post("counterfactual", disabled_mechanism="M-CARRIER-REROUTE")
    assert body["disabled_mechanism"] == "M-CARRIER-REROUTE"
    assert body["mode"] == "counterfactual"


def test_counterfactual_keeps_the_incident_and_is_not_the_baseline() -> None:
    """The distinction that makes a counterfactual meaningful."""
    cf = {s["field"]: s["value"] for s in
          post("counterfactual", disabled_mechanism="M-CARRIER-REROUTE")["projection"]["stages"]}
    base = {s["field"]: s["value"] for s in post("baseline")["projection"]["stages"]}
    full = {s["field"]: s["value"] for s in post("incident")["projection"]["stages"]}

    # Incident present in the counterfactual, absent in the baseline.
    assert cf["incident_severity"] > 0.0
    assert base["incident_severity"] == 0.0
    assert cf["incident_severity"] == pytest.approx(full["incident_severity"], abs=1e-12)
    # Upstream of the disabled mechanism preserved bit-identically.
    assert cf["insurer_risk"] == pytest.approx(full["insurer_risk"], abs=1e-12)
    assert cf["premium_pressure"] == pytest.approx(full["premium_pressure"], abs=1e-12)
    # The mechanism's own target, and everything downstream, prevented.
    assert cf["rerouting_level"] == 0.0
    assert cf["political_pressure"] == 0.0


def test_unknown_mechanism_is_rejected() -> None:
    r = client.post(RUN, json={"mode": "counterfactual", "disabled_mechanism": "M-INVENTED"})
    assert r.status_code == 422


def test_repeated_requests_produce_identical_responses() -> None:
    """Determinism, not caching: each request builds a fresh model from the same seed."""
    bodies = [post("incident") for _ in range(4)]
    first = bodies[0]["projection"]
    for b in bodies[1:]:
        assert b["projection"] == first


def test_api_execution_does_not_persist_or_mutate_shared_state() -> None:
    """A baseline run between two incident runs must not change the incident result."""
    a = post("incident")["projection"]
    post("baseline")
    post("counterfactual", disabled_mechanism="M-INSURER-RISK")
    b = post("incident")["projection"]
    assert a == b, "an intervening request changed a later result — shared state leaked"


def test_no_http_client_is_reachable_from_the_simulation_package() -> None:
    """No module on the authoritative path may import an HTTP client or model SDK.

    Patching `socket.connect` was tried first and is the wrong instrument here: TestClient's own
    in-process transport trips it, so the test would fail for a reason unrelated to the engine.
    Checking the import graph tests the actual property — that nothing on this path *can* reach
    the network — rather than observing one request that happened not to.
    """
    import ast
    from pathlib import Path

    forbidden = {"httpx", "requests", "aiohttp", "urllib", "urllib3", "http",
                 "openai", "anthropic", "litellm"}
    sim = Path(__file__).resolve().parents[1] / "app" / "simulation"
    offenders = []
    for path in sorted(sim.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    if a.name.split(".")[0] in forbidden:
                        offenders.append(f"{path.name}:{node.lineno}: import {a.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module.split(".")[0] in forbidden:
                    offenders.append(f"{path.name}:{node.lineno}: from {node.module}")
    assert not offenders, "network/model client reachable from the simulation path: " + "; ".join(offenders)


def test_the_gateway_used_during_a_demo_run_is_the_stub() -> None:
    """The gateway IS called each tick for micro-agent proposals — and it is a stub.

    The honest claim is not "the gateway is never called"; it is that calling it reaches no model
    and no network. Asserting the former would be false.
    """
    from app.simulation.llm_gateway import propose_action
    from app.simulation.schemas.agent_schema import ActionProposal

    proposal = propose_action(
        agent={"agent_id": "min-defence-oduya", "role": "minister_of_defence"},
        context={"tick": 0, "scenario_id": "kestral-strait"},
    )
    assert isinstance(proposal, ActionProposal)
    # And the run still completes with genuine engine output.
    assert post("incident")["projection"]["origin"] == "engine"


def test_response_validates_against_the_projection_shape() -> None:
    body = post("incident")
    assert body["contract_version"]
    for key in ("scenario_id", "rule_pack_version", "tick", "simulated_hours",
                "state_revision", "stages", "cohorts", "government_options",
                "recent_transitions", "not_implemented", "origin"):
        assert key in body["projection"], f"missing projection key: {key}"
    assert body["projection"]["origin"] == "engine"
    assert body["projection"]["rule_pack_version"] == "kestral-causal-slice@1.0.0"


def test_response_states_its_own_limitations() -> None:
    body = post("incident")
    joined = " ".join(body["limitations"]).lower()
    for missing in ("persistence", "replay", "registry", "authentication"):
        assert missing in joined
    for missing in ("replay", "event sourcing", "persistence", "state hashing"):
        assert missing in body["projection"]["not_implemented"]


def test_every_projection_value_is_marked_engine_origin() -> None:
    p = post("incident")["projection"]
    for group in ("stages", "cohorts", "government_options"):
        for entry in p[group]:
            assert entry["origin"] == "engine"


def test_transitions_carry_mechanism_and_causal_parents() -> None:
    p = post("incident")["projection"]
    assert p["recent_transitions"]
    assert any(t["causal_parents"] for t in p["recent_transitions"])
    for t in p["recent_transitions"]:
        assert t["mechanism"] and t["mechanism_version"]


def test_mechanisms_endpoint_lists_the_declared_chain() -> None:
    r = client.get("/api/demo/kestral-strait/mechanisms")
    assert r.status_code == 200
    body = r.json()
    ids = {m["id"] for m in body["mechanisms"]}
    assert {"M-INSURER-RISK", "M-CARRIER-REROUTE", "M-HOUSEHOLD-EXPECT"} <= ids
    for m in body["mechanisms"]:
        assert m["lifecycle"] and m["version"]
