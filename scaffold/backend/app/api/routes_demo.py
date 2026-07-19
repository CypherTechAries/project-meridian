"""Ephemeral Kestral Strait demonstration endpoint — first live engine→UI integration.

WHAT THIS IS
------------
`POST /api/demo/kestral-strait/run` executes an in-memory, deterministic 20-tick run of the P0.5
causal slice and returns the read-only projection. It is the first path by which genuine engine
output reaches the interface.

WHAT THIS IS NOT — read before describing it anywhere
-----------------------------------------------------
* **No persistence.** Nothing is written to a database. The model is constructed, stepped and
  discarded within the request.
* **No run registry.** The run cannot be retrieved again; there is no run id to fetch. A second
  request builds a fresh model from the same seed and gets the same answer because the engine is
  deterministic, not because anything was stored.
* **No replay.** Transitions are returned from the run that just executed. Nothing is replayed and
  no state can be rebuilt from them. That is P0.6.
* **No auth boundary.** There is no user, no role and no access control. `player_role` in the
  projection is a placeholder string, not an enforced identity.
* **No production workload guarantee.** Each request does real CPU work. There is no queue, no
  cache, no rate limit and no concurrency control.

WHY POST RATHER THAN GET
------------------------
The request *executes simulation work*. A GET implying a cheap idempotent read of stored state
would misrepresent that, and would invite caching layers to treat computed output as a resource.
The run is deterministic, so repeated POSTs return identical bodies — that is a property of the
engine, not of a cache.

MUTATION SAFETY
---------------
Each request constructs its own `MeridianModel`. No module-level model exists, nothing is shared
between requests, and the endpoint cannot mutate any state visible to another caller — asserted by
test.
"""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import SCENARIOS_DIR
from ..simulation.engine import MeridianModel
from ..simulation.mechanisms import CHAIN
from ..simulation.projection import project_causal_slice

router = APIRouter(prefix="/api/demo", tags=["demonstration"])

DEMO_SCENARIO_ID = "kestral-strait"
DEMO_SEED = 88213
CONTRACT_VERSION = "0.5.0"


class RunMode(str, Enum):
    """The three runs the demonstration supports.

    `counterfactual` disables exactly one named mechanism while KEEPING the incident, which is
    what distinguishes it from `baseline` — baseline has no incident at all.
    """

    BASELINE = "baseline"
    INCIDENT = "incident"
    COUNTERFACTUAL = "counterfactual"


class DemoRunRequest(BaseModel):
    mode: RunMode = RunMode.INCIDENT
    ticks: int = Field(default=20, ge=1, le=200)
    # Only meaningful for `counterfactual`. Defaults to the carrier-rerouting link, which shows
    # the sharpest contrast: upstream preserved bit-identically, downstream collapsed.
    disabled_mechanism: str = "M-CARRIER-REROUTE"


class DemoRunResponse(BaseModel):
    """Typed, versioned response. The frontend consumes this, never internal state objects."""

    contract_version: str
    mode: RunMode
    disabled_mechanism: str | None
    ticks: int
    seed: int
    projection: dict[str, Any]
    # Per-tick values the run produced. Derived presentation data, not a stored history.
    trajectory: list[dict[str, Any]]
    # Restated in the response so a consumer cannot infer capabilities from the payload's shape.
    limitations: list[str]


_LIMITATIONS = [
    "Ephemeral: this run is discarded when the request completes.",
    "No persistence — nothing is written to a database.",
    "No run registry — the run cannot be retrieved again.",
    "No replay — transitions are from the run just executed; no state can be rebuilt from them.",
    "No authentication or role enforcement — player_role is a placeholder, not an identity.",
    "No production workload guarantees — no queue, cache, rate limit or concurrency control.",
    "Every rule-pack coefficient is an authored fictional value, calibrated against nothing.",
]


def _load_scenario() -> dict:
    path: Path = SCENARIOS_DIR / f"{DEMO_SCENARIO_ID}.json"
    if not path.exists():  # pragma: no cover - configuration error
        raise HTTPException(status_code=500, detail=f"demonstration scenario not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


@router.post("/kestral-strait/run", response_model=DemoRunResponse)
def run_demonstration(req: DemoRunRequest) -> DemoRunResponse:
    """Execute an ephemeral deterministic run and return the read-only projection."""
    scenario = _load_scenario()
    disabled: str | None = None
    enabled: list[str] | None = None

    if req.mode is RunMode.BASELINE:
        # The honest control: identical scenario with the incident removed entirely.
        scenario = {k: v for k, v in scenario.items() if k != "incidents"}
    elif req.mode is RunMode.COUNTERFACTUAL:
        known = {m.id for m in CHAIN}
        if req.disabled_mechanism not in known:
            raise HTTPException(
                status_code=422,
                detail=f"unknown mechanism {req.disabled_mechanism!r}; known: {sorted(known)}",
            )
        disabled = req.disabled_mechanism
        # The incident is KEPT. Only the mechanism is disabled.
        enabled = [m.id for m in CHAIN if m.id != disabled]

    model = MeridianModel(scenario=scenario, seed=DEMO_SEED, enabled_mechanisms=enabled)

    # Per-tick trajectory, recorded as the run executes. This is DERIVED PRESENTATION DATA - the
    # values the run actually produced at each tick - not a new engine capability and not a
    # stored history. It exists so a chart can show a trajectory instead of a single number.
    trajectory: list[dict[str, Any]] = []
    for _ in range(req.ticks):
        model.step()
        c = model.state.chain
        trajectory.append({
            "tick": model.tick,
            "incident_severity": round(c.incident_severity, 6),
            "insurer_risk": round(c.insurer_risk, 6),
            "rerouting_level": round(c.rerouting_level, 6),
            "employment_pressure": round(c.employment_pressure, 6),
            "household_expectation_pressure": round(c.household_expectation_pressure, 6),
            "narrative_attention": round(c.narrative_attention, 6),
            "collective_activity": round(c.collective_activity, 6),
            "political_pressure": round(c.political_pressure, 6),
        })

    return DemoRunResponse(
        contract_version=CONTRACT_VERSION,
        mode=req.mode,
        disabled_mechanism=disabled,
        ticks=req.ticks,
        seed=DEMO_SEED,
        projection=project_causal_slice(model.state, model.transition_log),
        trajectory=trajectory,
        limitations=list(_LIMITATIONS),
    )


@router.get("/kestral-strait/mechanisms")
def list_mechanisms() -> dict:
    """The declared chain, for a UI that wants to offer counterfactual choices."""
    return {
        "contract_version": CONTRACT_VERSION,
        "origin": "engine",
        "mechanisms": [
            {
                "id": m.id,
                "version": m.version,
                "stage": m.stage,
                "stage_name": m.stage_name,
                "source_fields": list(m.source_fields),
                "target_fields": list(m.target_fields),
                "lag_ticks": m.lag_ticks,
                "lifecycle": m.lifecycle,
            }
            for m in CHAIN
        ],
    }
