"""REST endpoints for scenario runs.

Create a run, advance ticks, read state snapshots, submit a player decision, and read the
event log. Player decisions are parsed into `Intervention` objects — the engine validates and
prices them; the LLM never writes numeric state.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..simulation.llm_gateway import generate_briefing
from ..simulation.schemas.agent_schema import Intervention
from . import runs

router = APIRouter(prefix="/api/simulation", tags=["simulation"])


class CreateRunRequest(BaseModel):
    """Request body to create a new scenario run."""

    scenario_id: str = Field(..., description="Scenario template id, e.g. 'kestral-strait'.")
    seed: Optional[int] = Field(default=None, description="Override RNG seed (else scenario default).")


class CreateRunResponse(BaseModel):
    run_id: str = Field(..., description="Generated run id.")
    scenario_id: str
    seed: int
    tick: int


class AdvanceRequest(BaseModel):
    ticks: int = Field(default=1, ge=1, le=1000, description="Number of ticks to advance.")


@router.post("/runs", response_model=CreateRunResponse)
def create_run(req: CreateRunRequest) -> CreateRunResponse:
    """Create a new simulation run from a scenario template."""
    try:
        run_id, model = runs.create_run(req.scenario_id, req.seed)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return CreateRunResponse(
        run_id=run_id, scenario_id=model.scenario_id, seed=model.seed, tick=model.tick
    )


@router.post("/runs/{run_id}/advance")
def advance(run_id: str, req: AdvanceRequest) -> dict:
    """Advance a run by N ticks and return the resulting macro snapshot."""
    try:
        model = runs.get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found")
    model.run(req.ticks)
    return {"run_id": run_id, "tick": model.tick, "macro_state": model.macro_snapshot()}


@router.get("/runs/{run_id}/state")
def get_state(run_id: str) -> dict:
    """Return the current macro state snapshot and a stub natural-language briefing."""
    try:
        model = runs.get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found")
    snapshot = model.macro_snapshot()
    return {
        "run_id": run_id,
        "tick": model.tick,
        "macro_state": snapshot,
        "narrative_adoption": model.narrative_adoption,
        "briefing": generate_briefing(snapshot),  # interpretive layer only
    }


@router.post("/runs/{run_id}/decision")
def submit_decision(run_id: str, intervention: Intervention) -> dict:
    """Submit a player decision. The engine records it; validation/pricing happens on tick.

    In this stub we simply log the intervention as an event. A full build would route it
    through the same validate-and-price gate that micro-agent proposals pass through.
    """
    try:
        model = runs.get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found")
    model.event_log.append(
        {
            "event_id": f"decision-{model.tick}-{intervention.action_id}",
            "tick": model.tick,
            "type": "player_decision",
            "actors_involved": [intervention.actor_role],
            "effects": [],
            "intervention": intervention.model_dump(),
        }
    )
    return {"run_id": run_id, "accepted": True, "tick": model.tick}


@router.get("/runs/{run_id}/events")
def get_events(run_id: str) -> dict:
    """Return the event log for a run."""
    try:
        model = runs.get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found")
    return {"run_id": run_id, "events": model.event_log}
