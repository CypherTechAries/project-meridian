"""Import and API smoke checks for MERIDIAN's core dependency set.

Phase 0 item P0.3. Run by CI and runnable identically by hand, so a local run and a hosted run
exercise the same code path:

    python tools/ci_smoke.py

Exits non-zero on the first failure, printing what failed and why.

WHY THIS EXISTS BEYOND `import mesa`
------------------------------------
MERIDIAN installs mesa with `--no-deps` (see requirements-mesa.txt), so mesa's declared
dependencies matplotlib, solara and mesa-viz-tornado are deliberately absent. A bare `import mesa`
would not prove that the specific mesa APIs this codebase depends on still resolve under that
exception. This script checks those three symbols by name.

This script imports and constructs. It asserts nothing about simulation behaviour, and it is not
a test of correctness — `python -m pytest tests -q` remains the behavioural check.
"""

from __future__ import annotations

import importlib
import platform
import sys

# The complete set of mesa APIs MERIDIAN uses. Verified by grep over app/ and tests/ on
# 19 July 2026: mesa.Agent (agents/cohort_agent.py:15, agents/institutional_agent.py:18),
# mesa.Model (simulation/engine.py:72), and Model.__init__(seed=...) (engine.py:82).
# If this list grows, the --no-deps exception in requirements-mesa.txt must be re-justified.
MESA_APIS_USED = ("Agent", "Model")

# Third-party packages that must import. mesa's genuine import-time requirements are included
# because --no-deps means pip will not fetch them for us.
REQUIRED_MODULES = ("mesa", "numpy", "pandas", "tqdm", "networkx", "fastapi", "pydantic")

# MERIDIAN's own package: the module tree must import with no side effects.
APP_MODULES = (
    "app.main",
    "app.simulation.engine",
    "app.simulation.diffusion",
    "app.simulation.llm_gateway",
    "app.simulation.agents.cohort_agent",
    "app.simulation.agents.institutional_agent",
    "app.simulation.agents.macro_state",
)


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    print(f"platform : {platform.system()} {platform.release()}")
    print(f"python   : {sys.version.split()[0]}")
    print("-" * 60)

    for name in REQUIRED_MODULES:
        try:
            mod = importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001 - we want the reason, whatever it is
            _fail(f"could not import {name!r}: {type(exc).__name__}: {exc}")
        version = getattr(mod, "__version__", "(no __version__)")
        print(f"  ok  import {name:<12} {version}")

    print("-" * 60)

    # mesa is installed with --no-deps, so check the specific attributes we rely on.
    import mesa

    for api in MESA_APIS_USED:
        if not hasattr(mesa, api):
            _fail(
                f"mesa.{api} is missing. MERIDIAN subclasses it. The --no-deps install in "
                f"requirements-mesa.txt may no longer be viable for this mesa version."
            )
        print(f"  ok  mesa.{api} present")

    # Model(seed=...) is the constructor signature the engine relies on (engine.py:82).
    try:
        probe = mesa.Model(seed=12345)
    except Exception as exc:  # noqa: BLE001
        _fail(f"mesa.Model(seed=...) failed: {type(exc).__name__}: {exc}")
    print(f"  ok  mesa.Model(seed=...) constructs -> {type(probe).__name__}")

    print("-" * 60)

    for name in APP_MODULES:
        try:
            importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001
            _fail(f"could not import {name!r}: {type(exc).__name__}: {exc}")
        print(f"  ok  import {name}")

    print("-" * 60)
    print("SMOKE OK")


if __name__ == "__main__":
    main()
