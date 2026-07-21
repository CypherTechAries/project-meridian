"""
Read-only Virtual Person endpoints (VP-5).

Two GET routes exposing the implemented VP-1..VP-4 material through the projection layer.

NOT LIVE STATE. Every response carries `result_kind: "packaged-virtual-person-snapshot"` and
`connected_to_authoritative_run: false`. This is composed on request from frozen fixtures and
deterministic rules — never live person state, a current authoritative person, persisted person
memory, executed decision history or real-time society state.

READ-ONLY. No POST/PUT/PATCH/DELETE, no request body, no action-selection or command endpoint.
Every projection function is pure over frozen module-level fixtures; nothing here can mutate
identity fixtures, situation state, transition traces, decision records, relationship records,
information or belief histories, or the frozen belief fixtures — asserted by deep-copy tests.

B5. Typed fictional person ids only, resolved against the Kestral registry. Organisations, cohorts,
the legacy `agent` kind, cross-world ids, unknown people, free text and real-person identifiers are
all refused. Unknown query parameters fail rather than being ignored. No route ranks people, finds
influential people, identifies who is easiest to persuade, compares susceptibility, recommends
targeting, optimises audiences or generates persuasion strategies.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from ..safety.controls import TARGET_PREFIX, B5Violation
from ..safety.targets import (
    assert_no_persuasion_optimisation,
    assert_no_protected_traits,
    assert_not_real_population,
)
from ..simulation.belief import cast
from ..simulation.person.projection import Dossier, Roster, dossier, roster
from ..simulation.person.vp4_fixtures import PEOPLE

router = APIRouter(prefix="/api/virtual-person", tags=["virtual-person"])


def _reject_unknown_query_params(request: Request) -> None:
    """Unknown fields are refused, never silently ignored — the failure B5-06 exists to prevent."""
    unknown = sorted(set(request.query_params))
    if unknown:
        raise HTTPException(
            status_code=422,
            detail=f"unknown query parameter(s): {', '.join(unknown)}; this route accepts none",
        )


def _resolve_person(typed_id: str) -> str:
    """Resolve a typed fictional person id, refusing everything that is not one."""
    for guard in (assert_no_protected_traits, assert_no_persuasion_optimisation,
                  assert_not_real_population):
        try:
            guard({"target": typed_id}, path="person_id")
        except B5Violation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    parts = typed_id.split(":")
    if len(parts) != 4 or parts[0] != TARGET_PREFIX:
        raise HTTPException(
            status_code=422,
            detail=(f"person id must be '{TARGET_PREFIX}:<scenario_id>:person:<entity_id>'; "
                    f"free text is not accepted"),
        )
    _, scenario_id, kind, entity_id = parts
    if scenario_id != cast.SCENARIO_ID:
        raise HTTPException(
            status_code=422,
            detail=(f"cross-world reference: '{scenario_id}' is not the active fictional world "
                    f"'{cast.SCENARIO_ID}'"),
        )
    if kind != "person":
        raise HTTPException(
            status_code=422,
            detail=(f"'{kind}' is not a Virtual Person kind; organisations, cohorts and the legacy "
                    f"agent kind are not exposed by this route"),
        )
    if entity_id not in PEOPLE:
        raise HTTPException(
            status_code=404,
            detail=f"no person '{entity_id}' is implemented in the Virtual Person slice",
        )
    return entity_id


@router.get("/kestral-strait/roster", response_model=Roster,
            summary="Every implemented fictional person, in declaration order")
def get_roster(request: Request) -> Roster:
    """
    The implemented people with a short current-situation summary and record counts.

    Returned in **declaration order and never ranked** — not by influence, susceptibility, movement,
    risk, importance, ability to persuade or likelihood of compliance. There is no overall person
    score. Not live run state: see `run_integration`.
    """
    _reject_unknown_query_params(request)
    return roster()


@router.get("/kestral-strait/dossier/{typed_person_id}", response_model=Dossier,
            summary="One fictional person: identity, situation, decision, relationships, history")
def get_dossier(typed_person_id: str, request: Request) -> Dossier:
    """
    One person, e.g. `fict:kestral-strait:person:broadcast-journalist`.

    Sections stay distinct: identity (fixture, display only) · current situation · decision
    (selected, **never executed**) · relationships (declared connections, no scores) · information
    history (absence is time-bounded, never rejection) · belief history (one observation is never a
    trajectory) · explanations · model boundary.
    """
    _reject_unknown_query_params(request)
    return dossier(_resolve_person(typed_person_id))
