"""In-memory registry of active simulation runs.

A deliberately simple store so the scaffold runs without a database session. A real build
would persist via `app/db/models.py`; this keeps the demo self-contained. Runs are keyed by a
generated run id.
"""

from __future__ import annotations

import uuid
from typing import Optional

from ..safety import load_packaged_scenario
from ..simulation.engine import MeridianModel

_RUNS: dict[str, MeridianModel] = {}


def load_scenario(scenario_id: str) -> dict:
    """
    Load a packaged fictional scenario.

    B5-01/B5-02: this delegates to the single enforced loader. It does NOT read the scenarios
    directory itself - the allowlist is checked before any filesystem access and the fictional
    manifest before any engine object exists. Retained as a thin wrapper so existing callers keep
    working; there is deliberately no path-, URL- or upload-based alternative.
    """
    return load_packaged_scenario(scenario_id)


def create_run(scenario_id: str, seed: Optional[int] = None) -> tuple[str, MeridianModel]:
    """Instantiate a `MeridianModel` for a scenario and register it."""
    scenario = load_scenario(scenario_id)
    model = MeridianModel(scenario=scenario, seed=seed)
    run_id = uuid.uuid4().hex
    _RUNS[run_id] = model
    return run_id, model


def get_run(run_id: str) -> MeridianModel:
    """Fetch a registered run or raise KeyError."""
    return _RUNS[run_id]
