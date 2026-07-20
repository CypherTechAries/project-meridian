"""
B5-03 to B5-06 — target registry, protected-trait exclusion, persuasion-optimisation refusal,
and real-population refusal.

Everything here fails closed. An identifier that does not resolve inside the active fictional world
is an error; it is never best-effort matched, never fuzzy matched, and never rewritten into
something acceptable.

WHY THERE IS NO HEURISTIC HERE. The control baseline prefers typed schemas, allowlists and registry
resolution over name detection. So this module never asks "does this look like a real person?" —
it asks "does this resolve in the registry for this world?", which has an exact answer and cannot be
argued with.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .controls import (
    PERSUASION_OPTIMISATION_TERMS,
    PROHIBITED_IDENTITY_INFERENCES,
    PROTECTED_TRAIT_PROXIES,
    PROTECTED_TRAITS,
    REAL_POPULATION_SCOPES,
    TARGET_KINDS,
    TARGET_PREFIX,
    B5Violation,
)


@dataclass(frozen=True)
class TargetRef:
    """A resolved, typed reference to an entity inside one fictional world."""

    scenario_id: str
    kind: str
    entity_id: str

    def __str__(self) -> str:
        return f"{TARGET_PREFIX}:{self.scenario_id}:{self.kind}:{self.entity_id}"


class FictionalTargetRegistry:
    """
    The set of entities that may be named as a target, built from one loaded scenario.

    Construction is the only way entities enter the registry, so a target can never refer to
    something the active fictional world does not contain.
    """

    def __init__(self, scenario: dict, scenario_id: str) -> None:
        self.scenario_id = scenario_id
        self._entities: dict[str, set[str]] = {kind: set() for kind in TARGET_KINDS}

        for cohort in scenario.get("cohorts", []) or []:
            cid = cohort.get("cohort_id")
            if cid:
                self._entities["cohort"].add(str(cid))

        for agent in scenario.get("institutional_agents", []) or []:
            aid = agent.get("agent_id")
            if aid:
                self._entities["agent"].add(str(aid))

        for inst in scenario.get("institutions", []) or []:
            iid = inst.get("institution_id")
            if iid:
                self._entities["institution"].add(str(iid))

        # Belief-slice entities. Same rule as every other kind: an entity is targetable only
        # because the scenario declares it.
        for person in scenario.get("people", []) or []:
            pid = person.get("person_id")
            if pid:
                self._entities["person"].add(str(pid))

        for org in scenario.get("organisations", []) or []:
            oid = org.get("organisation_id")
            if oid:
                self._entities["organisation"].add(str(oid))

    def known(self, kind: str) -> frozenset[str]:
        return frozenset(self._entities.get(kind, set()))

    def resolve(self, raw: Any) -> TargetRef:
        """
        B5-03. Parse and resolve a typed identifier, or refuse.

        Accepts ONLY `fict:<scenario_id>:<kind>:<entity_id>`. Free text is refused by the parser
        before any lookup: a bare name cannot express a world, so it cannot be resolved in one.
        """
        if not isinstance(raw, str) or not raw:
            raise B5Violation("B5-03", "target must be a non-empty typed identifier string")

        parts = raw.split(":")
        if len(parts) != 4:
            raise B5Violation(
                "B5-03",
                f"target '{raw}' is not a typed identifier. Required form: "
                f"'{TARGET_PREFIX}:<scenario_id>:<kind>:<entity_id>'. Free-text person, "
                f"organisation and political-population targets are rejected.",
            )

        prefix, scenario_id, kind, entity_id = parts

        if prefix != TARGET_PREFIX:
            raise B5Violation(
                "B5-03",
                f"target '{raw}' does not carry the fictional-world prefix "
                f"'{TARGET_PREFIX}:'. Real persons, organisations, governments and political "
                f"populations cannot be addressed.",
            )
        if scenario_id != self.scenario_id:
            raise B5Violation(
                "B5-03",
                f"target '{raw}' belongs to world '{scenario_id}', but the active world is "
                f"'{self.scenario_id}'. Cross-world targeting is rejected.",
            )
        if kind not in TARGET_KINDS:
            raise B5Violation(
                "B5-03",
                f"target kind '{kind}' is not one of {sorted(TARGET_KINDS)}",
            )
        if entity_id not in self._entities[kind]:
            raise B5Violation(
                "B5-03",
                f"target '{raw}' does not resolve to a {kind} in world "
                f"'{self.scenario_id}'. Unresolved identifiers are rejected, not ignored.",
            )

        return TargetRef(scenario_id=scenario_id, kind=kind, entity_id=entity_id)

    def resolve_all(self, raws: Iterable[Any]) -> list[TargetRef]:
        return [self.resolve(r) for r in raws]


def _normalise(name: Any) -> str:
    return str(name).strip().lower().replace("-", "_").replace(" ", "_")


def assert_no_protected_traits(payload: Any, *, path: str = "request") -> None:
    """
    B5-04. Refuse protected traits, declared proxies and prohibited identity inferences wherever
    they appear as keys or as string values in a request payload.

    Scope note: this guards SELECTION and RANKING inputs. It does not constrain what the world model
    may represent — identity may still shape lived experience, relationships, discrimination,
    institutional access, media exposure and cultural interpretation.
    """
    banned = {
        *(_normalise(t) for t in PROTECTED_TRAITS),
        *(_normalise(t) for t in PROTECTED_TRAIT_PROXIES),
    }
    inferences = {_normalise(t) for t in PROHIBITED_IDENTITY_INFERENCES}

    def walk(node: Any, where: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                nk = _normalise(key)
                if nk in banned:
                    raise B5Violation(
                        "B5-04",
                        f"'{key}' at {where} is a protected trait or declared proxy and may not be "
                        f"used as a targeting, ranking, optimisation, intervention-selection, "
                        f"susceptibility or segmentation input.",
                    )
                if nk in inferences:
                    raise B5Violation(
                        "B5-04",
                        f"'{key}' at {where} would encode an inherent identity inference "
                        f"({', '.join(PROHIBITED_IDENTITY_INFERENCES)} are prohibited).",
                    )
                walk(value, f"{where}.{key}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, f"{where}[{i}]")
        elif isinstance(node, str):
            if _normalise(node) in banned:
                raise B5Violation(
                    "B5-04",
                    f"'{node}' at {where} names a protected trait or declared proxy and may not be "
                    f"used as a targeting or segmentation criterion.",
                )

    walk(payload, path)


def assert_no_persuasion_optimisation(payload: Any, *, path: str = "request") -> None:
    """
    B5-05. Refuse susceptibility scoring, persuadability ranking and audience optimisation.

    Applies to fictional and real audiences alike. Aggregate fictional belief propagation is NOT
    affected — the safe-harbor statement permits it, and none of these terms describes it.
    """
    banned = {_normalise(t) for t in PERSUASION_OPTIMISATION_TERMS}

    def walk(node: Any, where: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if _normalise(key) in banned:
                    raise B5Violation(
                        "B5-05",
                        f"'{key}' at {where} requests persuadability or susceptibility "
                        f"optimisation. MERIDIAN does not calculate, expose or recommend "
                        f"susceptibility scores, audience rankings or optimal targets.",
                    )
                walk(value, f"{where}.{key}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, f"{where}[{i}]")
        elif isinstance(node, str):
            if _normalise(node) in banned:
                raise B5Violation(
                    "B5-05",
                    f"'{node}' at {where} requests persuadability or susceptibility optimisation.",
                )

    walk(payload, path)


def assert_not_real_population(payload: Any, *, path: str = "request") -> None:
    """
    B5-06. Refuse requests scoped to real people or populations.

    REJECTED, never rewritten. Automatically substituting a fictional analogue would tell the caller
    the request was acceptable and would hide the refusal from anyone auditing the exchange.
    """
    banned = {_normalise(s) for s in REAL_POPULATION_SCOPES}
    scope_keys = {"world", "world_mode", "population", "population_scope", "audience_scope", "scope"}

    def walk(node: Any, where: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if _normalise(key) in scope_keys and isinstance(value, str):
                    if _normalise(value) in banned:
                        raise B5Violation(
                            "B5-06",
                            f"{where}.{key}='{value}' scopes this request to a real population. "
                            f"MERIDIAN produces no recommendations or operational instructions for "
                            f"persuading or manipulating real people. The request is rejected, not "
                            f"converted to a fictional analogue.",
                        )
                walk(value, f"{where}.{key}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, f"{where}[{i}]")

    walk(payload, path)


def assert_request_permitted(payload: Any, *, path: str = "request") -> None:
    """All request-side controls, in one call. Used by the API boundary."""
    assert_not_real_population(payload, path=path)
    assert_no_protected_traits(payload, path=path)
    assert_no_persuasion_optimisation(payload, path=path)
