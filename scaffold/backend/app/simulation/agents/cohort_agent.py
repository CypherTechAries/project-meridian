"""Meso-tier cohort agent (Mesa Agent subclass).

P0.4 (19 July 2026): this agent no longer writes belief values in place. Belief is authoritative
state and lives in `AuthoritativeState.cohorts`; the agent submits a transition and the boundary
applies it. Before P0.4, `step()` mutated `self.cohort.beliefs.government_competence` directly,
bypassing every check.

The `Cohort` record held here remains the cohort's STATIC configuration — demographics, media
exposure, susceptibility, grievances, `represents_population`. Nothing mutates it, and it is not
authoritative runtime state.
"""

from __future__ import annotations

import mesa

from ..schemas.agent_schema import Cohort


class CohortAgent(mesa.Agent):
    """Wraps a `Cohort` configuration record inside the Mesa model."""

    def __init__(self, unique_id: str, model: mesa.Model, cohort: Cohort) -> None:
        super().__init__(unique_id, model)
        self.cohort = cohort

    @property
    def susceptibility(self) -> float:
        """Composite susceptibility used by the diffusion model (mean of appeal channels)."""
        s = self.cohort.influence_susceptibility
        return (s.authority_appeal + s.identity_appeal + s.economic_appeal) / 3.0

    def step(self) -> None:
        """Per-tick meso update.

        Grievance-driven drift: cohorts with active grievances lose a little belief in government
        competence each tick. A deterministic/stochastic rule — NOT an LLM call.

        Note the draw is conditional on `grievances` being non-empty. That conditionality is
        exactly the RNG-contamination vector A3 demonstrated: changing how many cohorts have
        grievances changes how many draws are consumed, shifting every later draw in the shared
        stream and moving macro numbers for reasons unrelated to any modelled cause. P0.4A
        (ADR-010) is what fixes this; P0.4 deliberately does not change the draw pattern, because
        changing it would alter existing tested numeric outputs.
        """
        if not self.cohort.grievances:
            return

        # Imported here rather than at module scope to avoid a circular import.
        from ..transitions import Transition, TransitionOrigin, TransitionType

        drift = 0.005 + self.model.rng.uniform(0.0, 0.005)
        cid = self.cohort.cohort_id
        current = self.model.state.cohorts[cid].beliefs["government_competence"]
        self.model.submit(
            Transition(
                type=TransitionType.SET_COHORT_BELIEF,
                origin=TransitionOrigin.ENGINE_RULE,
                payload={
                    "cohort_id": cid,
                    "belief": "government_competence",
                    "value": max(0.0, current - drift),
                },
                actor=cid,
                mechanism="grievance_drift (belief decays while grievances are active)",
            )
        )
