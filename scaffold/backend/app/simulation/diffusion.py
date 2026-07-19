"""Narrative-spread diffusion over a cohort network.

A minimal, seeded Linear Threshold Model (LTM) intended to spread a narrative between cohorts.
This computes the *numbers* for information-campaign effectiveness — the LLM never does.

P0.1 correction (19 July 2026): this module previously stated that "the engine calls this to
update `Narrative.adoption_by_cohort`". It does not. `MeridianModel._step_diffusion`
(`engine.py:138-145`) assigns the result to `model.narrative_adoption`, a plain dict, which is
read only by the run-state API response (`api/routes_simulation.py:75`). It reaches no
`Narrative` object, no cohort belief and no macro indicator. Wiring diffusion output to belief
is a target (Phase 0 item P0.5), not current behaviour.

Determinism: all randomness comes from the caller-supplied `rng` (the model's seeded RNG), so
results are reproducible for a given seed AND a given sequence of prior draws. Note that this
module draws from the same shared stream as every other subsystem, so adding or removing a draw
anywhere changes results here; named draw isolation is Phase 0 item P0.4A (see
`docs/adr/ADR-010-deterministic-randomness-architecture.md`).
"""

from __future__ import annotations


import random

import networkx as nx


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
    rng: random.Random,
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
        rng: Seeded RNG owned by the model (do not use the global `random`).
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
        jitter = rng.uniform(-0.01, 0.01)
        gain = suscept * (influence + seed_pressure) + jitter
        updated = adoption.get(node, 0.0) + gain * (1.0 - adoption.get(node, 0.0))
        new_adoption[node] = max(0.0, min(1.0, updated))
    return new_adoption
