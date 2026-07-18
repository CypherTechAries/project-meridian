"""Narrative-spread diffusion over a cohort network.

A minimal, seeded Linear Threshold Model (LTM) used to spread a narrative between cohorts.
This computes the *numbers* for information-campaign effectiveness — the LLM never does. The
engine calls this to update `Narrative.adoption_by_cohort`.

Determinism: all randomness comes from the caller-supplied `rng` (the model's seeded RNG),
so results are reproducible for a given seed.
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
    stochastic-but-reproducible. Adoption is monotonic non-decreasing and clamped to [0, 1].

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
