"""
B5-01 and B5-02 — fail-closed fictional manifest, and packaged scenarios only.

The single entry point for turning a scenario id into a runnable scenario dict. Nothing else in the
application may read the scenarios directory: `runs.py` and `routes_demo.py` both route through
`load_packaged_scenario`, so there is one place where the boundary is enforced and one place to
audit.

ORDER MATTERS. Allowlist membership is checked BEFORE any filesystem access, and the manifest is
validated BEFORE any engine object is constructed. A rejected scenario never touches the disk and
never reaches the simulation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..config import SCENARIOS_DIR
from .controls import (
    FICTIONAL_WORLD_MODE,
    PACKAGED_SCENARIOS,
    WORLD_MODE_KEY,
    B5Violation,
)


def assert_packaged_scenario(scenario_id: Any) -> str:
    """
    B5-02. Membership of the allowlist is the entire check.

    This also closes path traversal: '../../etc/passwd' is simply not a member, so the value never
    reaches `Path`. That is deliberate — a traversal filter would be a heuristic, and the control
    baseline prefers an allowlist precisely because an allowlist cannot be talked around.
    """
    if not isinstance(scenario_id, str) or not scenario_id:
        raise B5Violation("B5-02", "scenario id must be a non-empty string")
    if scenario_id not in PACKAGED_SCENARIOS:
        raise B5Violation(
            "B5-02",
            f"scenario '{scenario_id}' is not a packaged fictional scenario. "
            f"Public v0.1 runs only repository-bundled allowlisted scenarios: "
            f"{sorted(PACKAGED_SCENARIOS)}. Uploads, URLs, external datasets and real-world "
            f"imports are disabled.",
        )
    return scenario_id


def assert_fictional_manifest(scenario: Any, scenario_id: str) -> None:
    """
    B5-01. Fail closed on the world manifest.

    Missing, unknown, malformed or non-fictional values are all rejected. There is NO
    default-to-fictional path: omitting the declaration is an error, not an implicit safe value.
    """
    if not isinstance(scenario, dict):
        raise B5Violation("B5-01", f"scenario '{scenario_id}' is not an object")

    if WORLD_MODE_KEY not in scenario:
        raise B5Violation(
            "B5-01",
            f"scenario '{scenario_id}' does not declare '{WORLD_MODE_KEY}'. "
            f"There is no default: an undeclared world is rejected, not assumed fictional.",
        )

    declared = scenario[WORLD_MODE_KEY]
    if not isinstance(declared, str):
        raise B5Violation(
            "B5-01",
            f"scenario '{scenario_id}' declares a malformed '{WORLD_MODE_KEY}' "
            f"({type(declared).__name__}); a string is required",
        )
    if declared != FICTIONAL_WORLD_MODE:
        raise B5Violation(
            "B5-01",
            f"scenario '{scenario_id}' declares {WORLD_MODE_KEY}='{declared}'. "
            f"Only '{FICTIONAL_WORLD_MODE}' may run.",
        )


def load_packaged_scenario(scenario_id: Any) -> dict:
    """
    The ONLY supported way to obtain a runnable scenario.

    There is deliberately no companion that loads from a path, a URL, an upload or a dataset. The
    absence of those functions is the control: B5-02 is enforced by there being no other door, not
    by a check inside one.
    """
    resolved = assert_packaged_scenario(scenario_id)

    path: Path = SCENARIOS_DIR / f"{resolved}.json"
    if not path.exists():
        # An allowlisted scenario missing from the package is a build defect, not a user input
        # problem — but it still fails closed.
        raise B5Violation("B5-02", f"packaged scenario '{resolved}' is missing from the bundle")

    scenario = json.loads(path.read_text(encoding="utf-8"))
    assert_fictional_manifest(scenario, resolved)
    return scenario


def fictional_world_metadata(scenario: dict, scenario_id: str) -> dict:
    """
    B5-07. Structured fictional-world metadata for API responses.

    Carried on every response so a consumer never has to infer the world's status from prose, and
    so a machine reader cannot miss it.
    """
    from .controls import FICTION_DISCLOSURE

    return {
        "world_mode": scenario.get(WORLD_MODE_KEY),
        "fictional": scenario.get(WORLD_MODE_KEY) == FICTIONAL_WORLD_MODE,
        "scenario_id": scenario_id,
        "scenario_version": scenario.get("scenario_version", "unversioned"),
        "disclosure": FICTION_DISCLOSURE,
        "disclaimer": scenario.get("fiction_disclaimer", ""),
    }
