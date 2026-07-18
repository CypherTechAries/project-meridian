"""Micro-tier institutional agent (Mesa Agent subclass).

Individually simulated actors (ministers, commanders). On each step the agent asks the LLM
gateway for an *action proposal* — the engine (not the agent, not the LLM) validates legality
and computes effects. The agent stores the latest proposal for the engine to process.
"""

from __future__ import annotations

from typing import Optional

import mesa

from .. import llm_gateway
from ..schemas.agent_schema import ActionProposal, MicroAgent


class InstitutionalAgent(mesa.Agent):
    """Wraps a `MicroAgent` schema record inside the Mesa scheduler."""

    def __init__(self, unique_id: str, model: mesa.Model, spec: MicroAgent) -> None:
        super().__init__(unique_id, model)
        self.spec = spec
        self.last_proposal: Optional[ActionProposal] = None

    def step(self) -> None:
        """Per-tick micro update: request a proposal from the LLM gateway.

        The agent passes only *serialized, read-only* data to the gateway and receives an
        `ActionProposal` back. It does NOT apply any numeric effect — that happens in
        `engine.py` after validation. This is the determinism boundary in action.
        """
        context = {
            "tick": self.model.tick,
            "scenario_id": self.model.scenario_id,
            "primary_target": None,
        }
        self.last_proposal = llm_gateway.propose_action(
            agent=self.spec.model_dump(),
            context=context,
        )
