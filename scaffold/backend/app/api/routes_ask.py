"""
Ask MERIDIAN Phase 1 — the read-only query route.

WHY POST. The request submits a query DOCUMENT (question plus optional structured context). It does
not mutate simulation state: no fixture, history, decision or run is written, and every response
carries `read_only: true` and `execution_status: NOT_EXECUTED`.

NO SHADOW STATE. The route accepts one question and explicit safe context only. It does not accept a
transcript, does not persist anything, and has no conversation memory. A refresh clears the display
history because the display history was never authority.

NO LANGUAGE MODEL. Intent matching is a declared catalogue plus deterministic normalisation.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from ..simulation.ask.answer import AskResponse, answer_question
from ..simulation.ask.catalogue import CATALOGUE_VERSION, Intent

router = APIRouter(prefix="/api/ask-meridian", tags=["ask-meridian"])


class AskRequest(BaseModel):
    """Strict. Unknown fields fail; no workflow or command object is accepted."""

    model_config = ConfigDict(extra="forbid")

    catalogue_version: str = CATALOGUE_VERSION
    question: str = Field(..., min_length=1, max_length=500)
    scenario_id: str = "kestral-strait"
    intent_hint: Optional[Intent] = None
    person_ref: Optional[str] = None
    proposition_ref: Optional[str] = None


@router.post("/query", response_model=AskResponse,
             summary="Ask a supported question and receive a deterministic, read-only answer")
def query(body: AskRequest, request: Request) -> AskResponse:
    """
    Answers only the declared catalogue. Unsupported questions are named as unsupported and the
    supported set is offered — the engine never guesses at intent.
    """
    if request.query_params:
        raise HTTPException(status_code=422, detail="this route accepts no query parameters")
    if body.catalogue_version != CATALOGUE_VERSION:
        raise HTTPException(
            status_code=422,
            detail=f"unknown catalogue version '{body.catalogue_version}'; this build serves "
                   f"'{CATALOGUE_VERSION}'")
    if body.scenario_id != "kestral-strait":
        raise HTTPException(status_code=422,
                            detail=f"'{body.scenario_id}' is not the active fictional world")
    return answer_question(body.question, person_ref=body.person_ref, intent_hint=body.intent_hint)
