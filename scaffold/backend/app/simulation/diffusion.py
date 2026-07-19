"""Narrative-spread diffusion over a cohort network.

A minimal, seeded Linear Threshold Model (LTM) intended to spread a narrative between cohorts.
This computes the *numbers* for information-campaign effectiveness — the LLM never does.

P0.1 correction (19 July 2026): this module previously stated that "the engine calls this to
update `Narrative.adoption_by_cohort`". It does not. `MeridianModel._step_diffusion`
(`engine.py:138-145`) assigns the result to `model.narrative_adoption`, a plain dict, which is
read only by the run-state API response (`api/routes_simulation.py:75`). It reaches no
`Narrative` object, no cohort belief and no macro indicator. Wiring diffusion output to belief
is a target (Phase 0 item P0.5), not current behaviour.

Determinism (P0.4A, 19 July 2026): jitter is drawn from the keyed `DeterministicDrawService`, not
from a shared sequential stream. Each cohort's jitter is a pure function of (run seed, cohort id,
tick), so it does not depend on graph traversal order, on how many other cohorts were processed
first, or on draws made by any other subsystem. Previously this module consumed a shared
`random.Random` in traversal order, which made its results sensitive to unrelated changes
elsewhere in the engine. See `docs/adr/ADR-010-deterministic-randomness-architecture.md`.
"""

from __future__ import annotations


import networkx as nx

from .draws import DeterministicDrawService


def build_cohort_graph(cohorts: list[dict]) -> nx.Graph:
    """Build an undirected influence graph from cohort records.

    Nodes are cohort ids; edges come from `network_position.bridges_to`. Edge weight is the
    mean internal cohesion of the two endpoints (a stand-in for tie strength).
    """
    g = nx.Graph()
    cohesion = {
        c["cohort_id"]: c.get("network_position", {}).get("internal_cohesion", 0.5)
        for c in cohorts
    }
    for cid in cohesion:
        g.add_node(cid)
    for c in cohorts:
        cid = c["cohort_id"]
        for other in c.get("network_position", {}).get("bridges_to", []):
            if other in cohesion:
                w = (cohesion[cid] + cohesion[other]) / 2.0
                g.add_edge(cid, other, weight=w)
    return g


def linear_threshold_step(
    graph: nx.Graph,
    adoption: dict[str, float],
    susceptibility: dict[str, float],
    draws: DeterministicDrawService,
    context: object = "",
    seed_pressure: float = 0.05,
) -> dict[str, float]:
    """Advance narrative adoption by one diffusion step (Linear Threshold style).

    For each cohort, incoming influence is the cohesion-weighted mean adoption of its
    neighbours, scaled by that cohort's susceptibility. A small seeded jitter keeps runs
    stochastic-but-reproducible. Adoption is clamped to [0, 1].

    P0.1 correction (19 July 2026): this docstring previously claimed adoption is "monotonic
    non-decreasing". It is not. `gain` is `suscept * (influence + seed_pressure) + jitter` with
    `jitter` drawn uniformly from [-0.01, 0.01], so whenever
    `suscept * (influence + seed_pressure) < |jitter|` and the jitter is negative, `gain` is
    negative and adoption DECREASES for that cohort. This is reachable for any low-susceptibility
    or weakly-connected cohort. The [0, 1] clamp masks it only at the lower bound. No test
    asserts monotonicity, so the property was never checked.

    Args:
        graph: Cohort influence graph from :func:`build_cohort_graph`.
        adoption: Current per-cohort adoption fraction, 0..1.
        susceptibility: Per-cohort susceptibility scalar, 0..1.
        draws: Keyed deterministic draw service (P0.4A). Replaces the shared RNG stream.
        context: Tick or transition context, included in every draw key.
        seed_pressure: Baseline external push toward adoption per step.

    Returns:
        New per-cohort adoption mapping.
    """
    new_adoption: dict[str, float] = {}
    for node in graph.nodes:
        neighbours = list(graph.neighbors(node))
        if neighbours:
            total_w = sum(graph[node][n].get("weight", 1.0) for n in neighbours)
            influence = (
                sum(graph[node][n].get("weight", 1.0) * adoption.get(n, 0.0) for n in neighbours)
                / total_w
            )
        else:
            influence = 0.0
        suscept = susceptibility.get(node, 0.5)
        # P0.4A: keyed on the cohort and tick, so each cohort's jitter is independent of how many
        # other cohorts were processed first, and of graph iteration order. Previously this drew
        # from a shared stream in traversal order.
        jitter = draws.jitter(
            0.01,
            subsystem="diffusion",
            purpose="adoption_jitter",
            entity=str(node),
            context=str(context),
        )
        gain = suscept * (influence + seed_pressure) + jitter
        updated = adoption.get(node, 0.0) + gain * (1.0 - adoption.get(node, 0.0))
        new_adoption[node] = max(0.0, min(1.0, updated))
    return new_adoption
