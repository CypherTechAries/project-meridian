"""Engine tests — the reproducibility commitment is the headline test.

Two runs with the same seed must produce identical macro state after N ticks. This proves the
determinism boundary: because the LLM never writes numeric state, the seeded RNG fully
determines the numbers.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.simulation.engine import MeridianModel

SCENARIO_PATH = Path(__file__).resolve().parents[2] / "scenarios" / "kestral-strait.json"


@pytest.fixture()
def scenario() -> dict:
    return json.loads(SCENARIO_PATH.read_text())


def test_runs_a_few_ticks(scenario: dict) -> None:
    """The model advances and records a snapshot per tick plus the initial one."""
    model = MeridianModel(scenario=scenario, seed=123)
    model.run(5)
    assert model.tick == 5
    assert len(model.snapshots) == 6  # initial + 5 ticks
    assert model.macro_snapshot()["tick"] == 5


def test_same_seed_is_deterministic(scenario: dict) -> None:
    """Same seed + scenario ⇒ byte-identical macro state after N ticks."""
    a = MeridianModel(scenario=scenario, seed=88213)
    b = MeridianModel(scenario=scenario, seed=88213)
    a.run(20)
    b.run(20)
    assert a.macro_snapshot() == b.macro_snapshot()


def test_different_seed_diverges(scenario: dict) -> None:
    """Different seeds should (almost certainly) produce different macro state."""
    a = MeridianModel(scenario=scenario, seed=1)
    b = MeridianModel(scenario=scenario, seed=2)
    a.run(20)
    b.run(20)
    assert a.macro_snapshot() != b.macro_snapshot()


def test_macro_state_actually_changes(scenario: dict) -> None:
    """Sanity: macro indicators should move over 20 ticks (engine is doing work)."""
    model = MeridianModel(scenario=scenario, seed=88213)
    before = model.macro_snapshot()["indicators"]["military_readiness"]
    model.run(20)
    after = model.macro_snapshot()["indicators"]["military_readiness"]
    assert before != after


def test_llm_gateway_cannot_write_state() -> None:
    """Structural check of the determinism boundary: the gateway returns a proposal, not state.

    `propose_action` must return an `ActionProposal` and must not expose any state-mutation
    surface. This guards the single most important architectural rule.
    """
    from app.simulation.llm_gateway import propose_action
    from app.simulation.schemas.agent_schema import ActionProposal

    proposal = propose_action(
        agent={"agent_id": "min-defence-oduya", "role": "minister_of_defence"},
        context={"tick": 0, "scenario_id": "kestral-strait"},
    )
    assert isinstance(proposal, ActionProposal)
    # A proposal carries no authority over macro state — it has no such fields.
    assert not hasattr(proposal, "apply_deltas")
    assert not hasattr(proposal, "macro_state")
