"""
Read-only belief projection endpoints.

WHAT THESE ARE
--------------
Two GET routes exposing the already-implemented belief slice through a projection layer. They read
frozen packaged fixtures, compute deterministically, and return typed projections.

WHAT THESE ARE NOT — read before describing them anywhere
---------------------------------------------------------
**Not connected to the authoritative simulation run.** No run is read, advanced, created or
written. `run_integration.connected_to_authoritative_run` is `false` in every landscape response
and the label says `packaged-belief-snapshot`. These results must never be described as live run
state, current authoritative belief state, or persisted person state.

WHY GET RATHER THAN POST
------------------------
Unlike `/api/demo/kestral-strait/run`, these routes execute no simulation work in the sense that
matters: they build no model, step no ticks and touch no run registry. They read fixtures and apply
a pure function. A GET is honest here, and repeated GETs return byte-identical bodies.

MUTATION SAFETY
---------------
Every projection function is pure over frozen module-level fixtures. No module-level mutable state
exists in this router, nothing is cached between requests, and no request can alter what another
request sees — asserted by test, including a fixture-identity check before and after a call.

B5
--
Entity ids arrive as typed fictional references and are resolved against a registry built from the
belief cast. Cross-world ids, unknown ids, free-text targets and unknown query fields are refused.
No route ranks people, identifies who is easiest to influence, optimises an audience or accepts a
real-population request. There is no request body anywhere in this module.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from ..safety.controls import TARGET_KINDS, TARGET_PREFIX, B5Violation
from ..safety.targets import (
    assert_no_persuasion_optimisation,
    assert_no_protected_traits,
    assert_not_real_population,
)
from ..simulation.belief import cast
from ..simulation.belief.projection import (
    CohortProjection,
    LandscapeProjection,
    OrganisationProjection,
    PersonProjection,
    cohort_projection,
    landscape_projection,
    organisation_projection,
    person_projection,
)

router = APIRouter(prefix="/api/belief", tags=["belief"])

#: Built from the belief cast, not the packaged scenario file. The two declare disjoint entity sets
#: under the same scenario id — see `projection.SCENARIO_ID_NOTE`. Resolving against the scenario
#: file would refuse every belief entity, so the registry is built from what the slice declares.
_REGISTRY: dict[str, frozenset[str]] = {
    "person": frozenset(p["person_id"] for p in cast.PEOPLE),
    "organisation": frozenset(o["organisation_id"] for o in cast.ORGANISATIONS),
    "cohort": frozenset(c["cohort_id"] for c in cast.COHORTS),
}

_BUILDERS = {
    "person": person_projection,
    "organisation": organisation_projection,
    "cohort": cohort_projection,
}


def _reject_unknown_query_params(request: Request, allowed: frozenset[str] = frozenset()) -> None:
    """
    Unknown fields are refused rather than ignored.

    A control that silently drops what it does not recognise is the exact failure B5-06 exists to
    prevent, and it has already happened once in this project.
    """
    unknown = sorted(set(request.query_params) - set(allowed))
    if unknown:
        raise HTTPException(
            status_code=422,
            detail=f"unknown query parameter(s): {', '.join(unknown)}; this route accepts none",
        )


def _resolve(typed_id: str) -> tuple[str, str]:
    """
    Resolve a typed fictional id against the active registry.

    Refuses anything that is not `fict:<scenario>:<kind>:<entity>` naming a declared entity of this
    fictional world. Free text, real organisations and cross-world references all fail here.
    """
    for guard in (assert_no_protected_traits, assert_no_persuasion_optimisation,
                  assert_not_real_population):
        try:
            guard({"target": typed_id}, path="entity_id")
        except B5Violation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    parts = typed_id.split(":")
    if len(parts) != 4 or parts[0] != TARGET_PREFIX:
        raise HTTPException(
            status_code=422,
            detail=(
                f"entity id must be a typed fictional reference "
                f"'{TARGET_PREFIX}:<scenario_id>:<kind>:<entity_id>'; free text is not accepted"
            ),
        )

    _, scenario_id, kind, entity_id = parts

    if scenario_id != cast.SCENARIO_ID:
        raise HTTPException(
            status_code=422,
            detail=(
                f"cross-world reference: '{scenario_id}' is not the active fictional world "
                f"'{cast.SCENARIO_ID}'"
            ),
        )
    if kind not in TARGET_KINDS:
        raise HTTPException(status_code=422, detail=f"'{kind}' is not a known entity kind")
    if kind not in _REGISTRY:
        raise HTTPException(
            status_code=422,
            detail=f"'{kind}' is not a belief-slice entity kind; use person, organisation or cohort",
        )
    if entity_id not in _REGISTRY[kind]:
        raise HTTPException(
            status_code=404,
            detail=f"no {kind} '{entity_id}' is declared in the active fictional world",
        )
    return kind, entity_id


@router.get(
    "/kestral-strait/landscape",
    response_model=LandscapeProjection,
    summary="Belief landscape for one claim across the whole fictional society",
)
def get_landscape(request: Request) -> LandscapeProjection:
    """
    Every declared entity's response to one claim.

    Returns three people, three organisations and six population groups, each with whether it
    received the claim, what it did, and what is unavailable. Not live run state — see
    `run_integration` in the body.
    """
    _reject_unknown_query_params(request)
    return landscape_projection()


@router.get(
    "/kestral-strait/dossier/{typed_id}",
    response_model=PersonProjection | OrganisationProjection | CohortProjection,
    summary="One entity's belief result by typed fictional id",
)
def get_dossier(
    typed_id: str, request: Request
) -> PersonProjection | OrganisationProjection | CohortProjection:
    """
    One person, organisation or population group.

    `typed_id` must be a typed fictional reference, for example
    `fict:kestral-strait:person:broadcast-journalist`. The three kinds return three structurally
    distinct shapes — they are deliberately not flattened into one generic profile.
    """
    _reject_unknown_query_params(request)
    kind, entity_id = _resolve(typed_id)
    return _BUILDERS[kind](entity_id)
