"""Read-only presentation projection for the P0.5 causal slice — Phase 0 item P0.5.

Produces a structured, derived view of the chain for a LATER UI-integration block. Nothing here is
connected to the frontend during P0.5, and C0 remains fixture-only until that integration is
reviewed.

READ-ONLY BY CONSTRUCTION. This module never writes, never submits a transition, never draws
randomness and never calls a model. Rendering a projection any number of times must leave the
simulation byte-identical — asserted by test.

EVERY VALUE IS MARKED. Each entry carries `origin: "engine"` because it genuinely came from the
engine, alongside an epistemic status. That matters because the UI currently renders fixtures
marked `origin: "fixture"`: when the two are shown together, the distinction must be per-record,
never per-page, or a live build silently launders fixture values into apparent engine output.

WHAT THIS IS NOT
----------------
Not replay and not causal reconstruction. `causal_parents` records which transition a later one
followed from within a tick — adjacency, not a reconstructed graph. Nothing here can rebuild a
run, and no state hash is computed. That is P0.6.
"""

from __future__ import annotations

from typing import Any

from .mechanisms import CHAIN
from .state import AuthoritativeState

# Epistemic status for engine-computed chain values, using the founder's D2 vocabulary.
# AUTHORITATIVE describes STATE QUALITY, not player access.
_ENGINE_STATUS = "AUTHORITATIVE"

# The chain, expressed for presentation. Ordered by stage so a UI can render it as a sequence
# without re-deriving the order.
_STAGE_FIELDS: tuple[tuple[int, str, str, str], ...] = (
    (1, "incident observation", "incident_severity", "Maritime incident severity"),
    (2, "institutional risk assessment", "insurer_risk", "Insurer risk posture"),
    (3, "market response", "premium_pressure", "Insurance-cost pressure"),
    (3, "logistics response", "rerouting_level", "Carrier rerouting"),
    (4, "port and employment exposure", "port_activity_deficit", "Port activity deficit"),
    (4, "port and employment exposure", "employment_pressure", "Employment exposure"),
    (5, "household and cohort response", "household_expectation_pressure",
        "Household expectation pressure (population-weighted)"),
    (6, "narrative and family activity", "narrative_attention", "Narrative attention"),
    (6, "narrative and family activity", "collective_activity", "Collective activity"),
    (7, "political pressure", "political_pressure", "Political pressure"),
)


def _entry(label: str, value: Any, status: str, provenance: str, tick: int, **extra: Any) -> dict:
    return {
        "label": label,
        "value": value,
        "epistemic_status": status,
        # Confidence is NOT_APPLICABLE for engine-computed values: the engine computes a value, it
        # does not estimate one, and no mechanism produces a confidence. Inventing one here would
        # be exactly the fabricated-precision the project forbids.
        "confidence": "NOT_APPLICABLE",
        "provenance": provenance,
        "last_updated_tick": tick,
        "origin": "engine",
        **extra,
    }


def project_causal_slice(state: AuthoritativeState, transition_log: list | None = None) -> dict:
    """Build the read-only presentation projection. Pure: reads state, writes nothing."""
    c = state.chain
    tick = state.tick

    mechanisms_by_target: dict[str, Any] = {}
    for m in CHAIN:
        for target in m.target_fields:
            mechanisms_by_target[target.replace("chain.", "")] = m

    stages = []
    for stage_no, stage_name, field, label in _STAGE_FIELDS:
        mech = mechanisms_by_target.get(field)
        stages.append(
            _entry(
                label=label,
                value=round(float(getattr(c, field)), 6),
                status=_ENGINE_STATUS,
                provenance=(
                    f"{mech.id}@{mech.version}" if mech else "engine"
                ),
                tick=tick,
                stage=stage_no,
                stage_name=stage_name,
                field=field,
                mechanism=mech.id if mech else None,
                mechanism_version=mech.version if mech else None,
                source_fields=list(mech.source_fields) if mech else [],
                lag_ticks=mech.lag_ticks if mech else 0,
                lifecycle=mech.lifecycle if mech else "",
            )
        )

    cohorts = []
    total_population = sum(x.represents_population for x in state.cohorts.values())
    for cid in sorted(state.cohorts):
        co = state.cohorts[cid]
        cohorts.append(
            _entry(
                label=cid,
                value=round(co.economic_concern, 6),
                status=_ENGINE_STATUS,
                provenance="M-HOUSEHOLD-EXPECT@1.0.0",
                tick=tick,
                cohort_id=cid,
                represents_population=co.represents_population,
                # Share of society-wide pressure this cohort contributes. Magnitude only — it says
                # nothing about whether the cohort is right, and nothing about any individual.
                population_share=round(
                    co.represents_population / total_population, 6
                ) if total_population else 0.0,
                income_sensitivity=co.income_sensitivity,
            )
        )

    options = [
        _entry(
            label=oid,
            value=status,
            status=_ENGINE_STATUS,
            provenance="M-GOV-OPTIONS@1.0.0",
            tick=tick,
            option_id=oid,
            driven_by="chain.political_pressure",
        )
        for oid, status in sorted(c.government_options.items())
    ]

    # Recent chain transitions, for a future Causal Timeline. Adjacency only — NOT a reconstructed
    # causal graph, and nothing replays from it.
    recent: list[dict] = []
    if transition_log:
        for r in transition_log[-60:]:
            if not r.applied or not r.mechanism_version:
                continue
            recent.append(
                {
                    "transition_id": r.transition_id,
                    "tick": r.tick,
                    "mechanism": r.mechanism,
                    "mechanism_version": r.mechanism_version,
                    "source_fields": list(r.source_fields),
                    "causal_parents": list(r.causal_parents),
                    "draw_refs": list(r.draw_refs),
                    "delta": r.delta,
                    "origin": "engine",
                }
            )

    return {
        "origin": "engine",
        "scenario_id": state.scenario.scenario_id,
        "scenario_version": state.scenario.scenario_version,
        "rule_pack_version": state.rule_pack_version,
        "tick": tick,
        "simulated_hours": state.timing.simulated_hours(tick),
        "tick_duration_minutes": state.timing.tick_duration_minutes,
        "demonstration_horizon_ticks": state.timing.demonstration_horizon_ticks,
        "state_revision": state.state_revision,
        "incident_active": c.incident_active,
        "stages": stages,
        "cohorts": cohorts,
        "government_options": options,
        "recent_transitions": recent,
        # Stated in the payload itself so a consumer cannot infer capabilities from its shape.
        "not_implemented": [
            "replay", "event sourcing", "state hashing", "persistence",
            "causal reconstruction", "live model integration", "role-based access enforcement",
        ],
    }
