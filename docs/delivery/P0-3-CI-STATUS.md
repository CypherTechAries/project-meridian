# P0.3 — Continuous integration: status

**Status:** DRAFT. Pending owner review.
**Date:** 19 July 2026
**Phase 0 item:** P0.3 (honest CI)

---

## The one-line status

**HOSTED CI PASSES ON GITHUB ACTIONS `windows-latest` WITH CPYTHON 3.12.10.**

*(Updated 19 July 2026. The previous status line read "CI configuration prepared and locally
reproduced. Hosted CI has not run and has not passed." That is now superseded — see the hosted-run
record at the end of this document. The claim above is deliberately narrow: it says nothing about
any other operating system or Python version, because nothing else has been tested.)*

"Prepared", "locally reproduced" and "hosted and passing" are three different claims and must not
be conflated. All three are now true, in that order, and the evidence for the third is the run
record at the end of this document.

What this still does **not** license: no document may state that any check is "guarded in CI" in
the sense of the determinism boundary being protected. CI runs the tests that exist, and
`test_llm_gateway_cannot_write_state` remains the shallow attribute check `CAPABILITY-CLAIMS` C3
describes. Running a weak test on a hosted runner does not make it a strong test.

---

## Plain-English layer

The install was broken until today, so there was nothing CI could honestly run. Now that a clean
machine can install the project in two commands and get five passing tests, CI can reproduce
exactly that and nothing more.

The workflow deliberately does very little. It installs the project the documented way, checks
that the packages import, checks that the specific bits of `mesa` the code depends on are
present, and runs the five tests. It has no code-coverage target, no linter, no formatter, no
performance budget, no Docker build and no deployment — because none of those standards has been
adopted, and a check that fails on day one, or that asserts a standard nobody agreed, is worse
than no check.

One honest wrinkle is recorded rather than hidden: the packaging check does **not** pass cleanly,
and is not made to. See the exception below.

---

## Technical-evidence layer

### Workflow

`.github/workflows/ci.yml` — one job, `backend`, on `windows-latest`, Python pinned to `3.12.10`.
Triggers: push to `main`, pull request to `main`, and manual dispatch.

### Steps, and the exact commands

| # | Step | Command |
|---|---|---|
| 1 | Check out | `actions/checkout@v4` |
| 2 | Python | `actions/setup-python@v5`, `python-version: '3.12.10'` |
| 3 | Show environment | `python --version`; `platform.system()/release()`; `pip --version` |
| 4 | Install core | `python -m pip install -r requirements.txt` |
| 5 | Install mesa | `python -m pip install --no-deps -r requirements-mesa.txt` |
| 6 | Packaging check | `python tools/ci_pip_check.py` |
| 7 | Import smoke | `python tools/ci_smoke.py` |
| 8 | Tests | `python -m pytest tests -v` |
| 9 | Record versions | `python -m pip freeze` (runs on success **and** failure) |
| 10 | Diagnostics | upload `.pytest_cache/` on failure only, 7-day retention |

Steps 4 and 5 are the two documented install commands from `scaffold/README.md`, unchanged.

### Locally reproduced result

Every step above was executed in order, in a **fresh virtual environment**, on:

- **OS:** Windows 10 (build 19045), `LongPathsEnabled=0`
- **Python:** CPython **3.12.10**
- **pip:** 25.0.1
- **Date:** 19 July 2026

| Step | Exit | Result |
|---|---|---|
| Install core requirements | 0 | — |
| Install mesa `--no-deps` | 0 | — |
| Packaging check | 0 | pass with recorded exception (see below) |
| Import smoke test | 0 | `SMOKE OK` |
| `pytest tests -v` | 0 | **5 passed in 0.81s** |

Resolved versions at time of run: mesa 2.4.0, numpy 2.5.1, pandas 2.3.3, tqdm 4.69.0,
networkx 3.6.1, fastapi 0.139.2, pydantic 2.13.4.

**No logic was changed to make any of this pass.** The only `.py` edits in this phase were
docstrings and one field description.

### Import smoke test — `tools/ci_smoke.py`

Imports `mesa`, `numpy`, `pandas`, `tqdm`, `networkx`, `fastapi`, `pydantic`, then all seven
MERIDIAN modules (`app.main`, `app.simulation.engine`, `.diffusion`, `.llm_gateway`,
`.agents.cohort_agent`, `.agents.institutional_agent`, `.agents.macro_state`).

It also verifies the **specific mesa APIs MERIDIAN uses**, not merely that `import mesa` works —
necessary because mesa is installed with `--no-deps`. Established by grep over `app/` and
`tests/` on 19 July 2026, the complete set is:

| API | Used at |
|---|---|
| `mesa.Agent` | `agents/cohort_agent.py:15`, `agents/institutional_agent.py:18` |
| `mesa.Model` | `simulation/engine.py:72` |
| `mesa.Model.__init__(seed=...)` | `simulation/engine.py:82` |

The script constructs `mesa.Model(seed=12345)` to confirm the constructor signature still
resolves. If that list ever grows, the `--no-deps` exception must be re-justified.

### Packaging check — the recorded exception

`pip check` **exits 1**. Verbatim output:

```
mesa 2.4.0 requires cookiecutter, which is not installed.
mesa 2.4.0 requires matplotlib, which is not installed.
mesa 2.4.0 requires mesa-viz-tornado, which is not installed.
mesa 2.4.0 requires solara, which is not installed.
```

**Disposition: accepted exception, not a clean pass.**

- **Are they genuinely unused?** Yes. `grep -rn "matplotlib\|solara\|mesa_viz\|mesa-viz\|cookiecutter"` over `app/`, `tests/` and `tools/` returns no import. The only textual hit is a comment in `tools/ci_smoke.py` explaining this exception. `mesa` is a vestigial base class here — no scheduler, no `AgentSet`, no visualisation.
- **Why not just install them?** Because `solara` is the package whose Jupyter tree exceeds the Windows 260-character path limit and caused the original P0.2 install failure. Installing it to satisfy a metadata check for code nothing imports would reintroduce the defect this phase fixed.
- **Why not suppress the check?** Because `|| true` would hide genuine future breakage.

`tools/ci_pip_check.py` therefore allowlists **exactly those four** packages and **fails on any
other inconsistency**. It does not claim the environment is dependency-consistent. It claims the
inconsistency is exactly the one accepted and nothing more — a weaker and truthful statement.

**This is recorded packaging debt, not a solved problem.** See below.

### LLM dependencies

`requirements-llm.txt` is **not** installed in CI. No live model integration exists, so there is
nothing to smoke-test. An optional job may be added when a real gateway is implemented.

---

## Remaining packaging debt

1. **The environment is not dependency-consistent by pip's metadata rules.** Four mesa packages are deliberately absent. Tracked as an accepted exception with a named review trigger.
2. **Whether mesa is retained at all is an open owner decision** (current-state audit §8, item 3). Mesa contributes three symbols. Dropping it would remove this exception entirely.
3. **No lockfile, no pinned `requires-python`, no `pyproject.toml`.** Every requirement is an open-ended range, so two runs on different dates can resolve to different versions. Adopting `pyproject.toml`/`uv` is an open owner decision (audit §8, item 5). This is why `pip freeze` runs on every CI run.
4. **Single platform, single Python version.** Verified on Windows 10 (local) and Windows Server 2025 (hosted), both CPython 3.12.10. Linux, macOS and every other Python version remain **untested** and unclaimed.
5. **No linting, formatting, typing or coverage checks.** Deliberate. Adding them is a separate decision, and `ruff`/`mypy` have never been run against this codebase, so their current pass/fail state is unknown.

---

## What must happen to close P0.3

- [ ] Founder authorises a commit and push of `.github/workflows/ci.yml` and the two `tools/` scripts
- [ ] A hosted run completes on the repository
- [ ] The hosted run **passes**, or its failures are recorded and fixed
- [ ] The hosted result is recorded here with a run URL and date
- [ ] Only then may `CAPABILITY-CLAIMS.md` C9 change, and only to what the hosted run demonstrates
- [ ] Branch protection / required status check — a separate decision, not assumed by this file

Until every box is ticked, the honest status line remains the one at the top of this document.


---

## Hosted CI run record — first execution

**The workflow executed on GitHub Actions for the first time on 19 July 2026 and passed.**

| | |
|---|---|
| Workflow | `CI` |
| Run ID | `29699943680` |
| URL | https://github.com/CypherTechAries/project-meridian/actions/runs/29699943680 |
| Commit SHA | `5d37100cbc4798bfd9229927e860ef0feaca7fa9` |
| Trigger | `pull_request` (draft PR #1, `phase-0-foundation` → `main`) |
| Conclusion | **success** |
| Duration | 1m 15s |

### Environment actually used

| | |
|---|---|
| Runner OS | **Microsoft Windows Server 2025** (image `windows-2025-vs2026`) |
| Python | **CPython 3.12.10** (pinned; resolved exactly) |
| mesa | 2.4.0 |

Note the runner is Windows **Server 2025**, not the Windows 10 machine used for local
verification. That difference was flagged in advance as the reason a local pass was not evidence
for a hosted pass. Both now pass — which is a stronger result than either alone, because the
`--no-deps` mesa install works around a Windows long-path limit whose configuration differs
between the two environments.

### Step results

| Step | Result |
|---|---|
| Install core requirements | **pass** |
| Install mesa (`--no-deps`, recorded exception) | **pass** |
| Packaging check | **pass with recorded exception** — 4 missing mesa visualisation packages, exactly the allowlisted set |
| Import smoke test | **`SMOKE OK`** — all third-party and MERIDIAN modules, plus the three mesa APIs verified by name |
| Run tests | **62 passed in 3.45s** |

### What this does and does not license

**Permitted wording, verbatim:**

> "Hosted CI passes on GitHub Actions `windows-latest` with CPython 3.12.10."

**Not permitted.** Anything broader. Specifically: no claim of cross-platform support, no claim
about Linux or macOS, no claim about any other Python version, and no claim that CI *guards* the
determinism boundary — it runs the tests that exist, and `test_llm_gateway_cannot_write_state`
remains the shallow attribute check that `CAPABILITY-CLAIMS` C3 describes. Running a weak test on
a hosted runner does not make it a strong test.

### One non-blocking annotation

GitHub reports that `actions/checkout@v4` and `actions/setup-python@v5` target Node.js 20, which
is deprecated, and were forced onto Node.js 24. The run passed. Recorded rather than fixed: pinning
newer action majors is a change to make deliberately, not reflexively inside a status update.
