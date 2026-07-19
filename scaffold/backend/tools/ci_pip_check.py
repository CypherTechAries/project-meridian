"""Run `pip check` and evaluate it against MERIDIAN's recorded packaging exception.

Phase 0 item P0.3. Run by CI and runnable identically by hand:

    python tools/ci_pip_check.py

WHY THIS IS NOT JUST `pip check`
--------------------------------
MERIDIAN installs mesa with `--no-deps` (see requirements-mesa.txt), because mesa's declared
visualisation dependencies pull a solara/Jupyter tree whose paths exceed the Windows
260-character limit and abort the install. MERIDIAN imports none of that tree.

That makes the environment genuinely dependency-INCONSISTENT by pip's metadata rules, and
`pip check` correctly exits non-zero. Two dishonest responses were rejected:

  * suppressing the check, or `|| true` in CI — this hides real future breakage;
  * installing the whole visualisation tree to silence it — this reintroduces the P0.2 install
    failure to satisfy a metadata check for packages nothing imports.

Instead, the four known-missing packages are listed below as an explicit, dated exception. Any
OTHER inconsistency fails the check. So this script does not claim the environment is consistent;
it claims the inconsistency is exactly the one we accepted, and nothing more.

REVIEW TRIGGER: if this script fails because a NEW package appears, do not add it to the
allowlist reflexively. Establish first whether MERIDIAN's code path actually needs it.
"""

from __future__ import annotations

import re
import subprocess
import sys

# Packages knowingly absent because mesa is installed with --no-deps.
# Verified 19 July 2026 by grep over app/, tests/ and tools/: none is imported by MERIDIAN.
# mesa APIs actually used are only mesa.Agent, mesa.Model and Model.__init__(seed=...).
ACCEPTED_MISSING = {
    "cookiecutter",       # mesa project scaffolding CLI; unused
    "matplotlib",         # mesa visualisation; unused
    "mesa-viz-tornado",   # mesa visualisation server; unused
    "solara",             # mesa visualisation UI; unused — the long-path offender
}

# "mesa 2.4.0 requires solara, which is not installed."
MISSING_RE = re.compile(r"^(?P<pkg>\S+) \S+ requires (?P<dep>[A-Za-z0-9._-]+), which is not installed\.$")


def main() -> int:
    proc = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        capture_output=True,
        text=True,
    )
    output = (proc.stdout + proc.stderr).strip()

    print("--- pip check output (verbatim) ---")
    print(output or "(no output)")
    print(f"--- pip check exit code: {proc.returncode} ---")

    if proc.returncode == 0:
        # The exception may have become unnecessary — worth knowing, not a failure.
        print("\npip check reports a fully consistent environment.")
        print("NOTE: the recorded mesa --no-deps exception appears no longer to apply.")
        print("Consider re-testing whether the exception is still needed.")
        return 0

    unexpected: list[str] = []
    accepted: list[str] = []

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        m = MISSING_RE.match(line)
        if m and m.group("dep").lower() in ACCEPTED_MISSING:
            accepted.append(line)
        else:
            unexpected.append(line)

    print("\n--- disposition ---")
    for line in accepted:
        print(f"  ACCEPTED (recorded mesa --no-deps exception): {line}")
    for line in unexpected:
        print(f"  UNEXPECTED: {line}")

    if unexpected:
        print(
            "\nFAIL: pip check reported an inconsistency outside the recorded exception.\n"
            "Do not add it to ACCEPTED_MISSING without first establishing that MERIDIAN's code "
            "path genuinely does not need the package."
        )
        return 1

    print(
        f"\nPASS WITH RECORDED EXCEPTION: {len(accepted)} missing package(s), all of them the "
        "known mesa visualisation dependencies.\n"
        "The environment is NOT dependency-consistent by pip's metadata rules. It is consistent "
        "with MERIDIAN's actual imports, which is a weaker and honest claim."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
