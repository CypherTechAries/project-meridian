"""Meso-tier cohort agent (Mesa Agent subclass).

A cohort is a weighted representative agent standing for N citizens. Its belief numbers are
updated by the diffusion model + rules, never by the LLM. The LLM may only *label* a shift in
a briefing sentence.
"""

from __future__ import annotations

import mesa

from ..schemas.agent_schema import Cohort


class CohortAgent(mesa.Agent):
    """Wraps a `Cohort` schema record inside the Mesa scheduler."""

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

        Grievance-driven drift: cohorts with active grievances lose a little belief in
        government competence each tick. Uses the model's seeded RNG so results are
        reproducible. This is a deterministic/stochastic rule — NOT an LLM call.
        """
        if self.cohort.grievances:
            drift = 0.005 + self.model.rng.uniform(0.0, 0.005)
            b = self.cohort.beliefs
            b.government_competence = max(0.0, b.government_competence - drift)
