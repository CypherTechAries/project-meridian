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
    """Submit a player decision. The engine RECORDS it only — nothing validates or prices it.

    P0.1 correction (19 July 2026): this docstring previously said "validation/pricing happens
    on tick". That is false and was publication blocker B1. No validation or pricing happens on
    this call or on any later tick: the submission is appended to an in-memory event list with
    an empty `effects` array, `accepted: true` is returned unconditionally, and the tick loop
    never reads the event list. The endpoint accepts any actor role, any action type and any
    resource cost, and stores the client's own `legal_check` value unexamined. It is a logging
    endpoint.

    Routing this through the same validate-and-price gate that micro-agent proposals pass
    through is a target, not current behaviour — and note that gate performs no legality or
    feasibility check either (`engine.py:121-130`).
    """
    try:
        model = runs.get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found")
    # P0.4: this route previously appended directly to `model.event_log` — a presentation route
    # writing engine state. It now goes through the single mutation boundary, which records it in
    # `AuthoritativeState.pending_actions` with `applied=False`.
    from ..simulation.transitions import Transition, TransitionOrigin, TransitionType

    record = model.submit(
        Transition(
            type=TransitionType.RECORD_PLAYER_DECISION,
            origin=TransitionOrigin.PLAYER_DECISION,
            payload={
                "action_id": intervention.action_id,
                "actor_role": intervention.actor_role,
                "action_type": intervention.action_type,
                "client_supplied": intervention.model_dump(),
            },
            actor=intervention.actor_role,
            mechanism="recorded only — no validation, pricing or application exists (blocker B1)",
        )
    )

    return {
        "run_id": run_id,
        # "recorded", not "accepted": nothing validates, prices or applies this. The previous
        # unconditional `accepted: true` overstated what the endpoint does.
        "recorded": record.applied,
        "transition_id": record.transition_id,
        "tick": model.tick,
        "applied": False,
        "note": (
            "Recorded only. No legality, authority, resource or feasibility validation exists, "
            "and the tick loop does not read pending actions. This decision will have no effect."
        ),
    }


@router.get("/runs/{run_id}/events")
def get_events(run_id: str) -> dict:
    """Return the event log for a run."""
    try:
        model = runs.get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found")
    return {"run_id": run_id, "events": model.event_log}
