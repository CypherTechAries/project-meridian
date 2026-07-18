"""LLM gateway — STUB.

This module is where LiteLLM (MIT) would route prompts to local or frontier models. In this
scaffold every function returns canned output so the whole system runs with **no API keys**.

============================ THE DETERMINISM BOUNDARY ============================
This module MUST NOT import or mutate any state object (`MacroState`, `Cohort`, …). It only
returns *proposals* and *text*. Look at the imports below: the only simulation type imported
is `ActionProposal`, which carries no authority to change numbers. `engine.py` is the sole
writer of numeric state. If you ever need to `import MacroState` here — stop; you are about
to break the single most important architectural commitment in the project (see
docs/ARCHITECTURE_DECISIONS.md ADR-006 and CLAUDE.md).
=================================================================================

Wiring LiteLLM later (sketch):

    import litellm
    resp = litellm.completion(
        model=settings.llm_model,           # e.g. "anthropic/claude-opus-4-7" (frontier)
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
        temperature=0.4,
    )
    # LiteLLM lets you route micro-agent reasoning to a cheap/local model
    # (e.g. "ollama/llama3") and briefings to a frontier model, from one interface.

Every real LLM output would be logged verbatim, versioned by
`model_id + prompt_version + temperature`, and treated as an interpretive layer that is NOT
part of the reproducible numeric state.
"""

from __future__ import annotations

from typing import Any, Mapping

from .schemas.agent_schema import ActionProposal

# Bump when prompt wording changes; used to version logged LLM outputs.
PROMPT_VERSION = "v1"


def _stub_action_type(agent_role: str) -> str:
    """Deterministic canned action choice per role, so stub runs are reproducible."""
    table = {
        "minister_of_defence": "request_procurement_acceleration",
        "minister_of_finance": "block_unfunded_spending",
        "minister_of_foreign_affairs": "open_backchannel",
        "intelligence_lead": "invest_in_attribution",
        "strategic_comms": "counter_narrative_briefing",
        "head_of_government": "convene_cabinet",
    }
    return table.get(agent_role, "observe")


def propose_action(
    agent: Mapping[str, Any],
    context: Mapping[str, Any],
) -> ActionProposal:
    """Ask the (stub) LLM what a micro agent should do, given its state and context.

    Returns an :class:`ActionProposal` — a *suggestion only*. The engine validates legality
    and computes effects; this function never touches numeric state.

    Args:
        agent: Serialized ``MicroAgent`` (a plain mapping, not a live state object).
        context: Read-only snapshot of relevant world state (also a plain mapping).

    Returns:
        An advisory ``ActionProposal``.
    """
    role = str(agent.get("role", "unknown"))
    action_type = _stub_action_type(role)
    return ActionProposal(
        proposing_agent_id=str(agent.get("agent_id", "unknown")),
        action_type=action_type,
        target=context.get("primary_target"),
        rationale=(
            f"[STUB rationale] Given the current situation, {role} would most plausibly "
            f"pursue '{action_type}'. Replace this module with a LiteLLM call for real reasoning."
        ),
        parameters={"intensity": 0.5},
        confidence=0.5,
    )


def generate_briefing(state: Mapping[str, Any]) -> str:
    """Produce a natural-language situation briefing from a read-only state snapshot.

    Args:
        state: A plain mapping snapshot (e.g. ``MacroState.model_dump()``). Passing a mapping
            rather than the live object keeps this function unable to mutate state.

    Returns:
        Canned briefing text. Swap for a LiteLLM call grounded (RAG) on real state fields.
    """
    ind = state.get("indicators", {})
    tick = state.get("tick", "?")
    approval = ind.get("government_approval", "?")
    throughput = ind.get("shipping_throughput_pct_of_baseline", "?")
    return (
        f"[STUB briefing — tick {tick}] Government approval is at {approval}; strait shipping "
        f"throughput is {throughput} of baseline. Pressure is building for a decisive response. "
        f"(This text is illustrative; wire LiteLLM in llm_gateway.py for real briefings.)"
    )
