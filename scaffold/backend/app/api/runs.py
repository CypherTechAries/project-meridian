"""In-memory registry of active simulation runs.

A deliberately simple store so the scaffold runs without a database session. A real build
would persist via `app/db/models.py`; this keeps the demo self-contained. Runs are keyed by a
generated run id.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Optional

from ..config import SCENARIOS_DIR
from ..simulation.engine import MeridianModel

_RUNS: dict[str, MeridianModel] = {}


def load_scenario(scenario_id: str) -> dict:
    """Load a scenario template JSON from the scenarios directory."""
    path: Path = SCENARIOS_DIR / f"{scenario_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"scenario '{scenario_id}' not found at {path}")
    return json.loads(path.read_text())


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
