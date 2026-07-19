# MERIDIAN — Simulated-Society Crisis Simulator (Scaffold)

> Working title. Fictional scenarios only — no real nations, organisations, or individuals.

> **Corrected 19 July 2026** under Phase 0 item P0.1, to remove present-tense claims the code
> does not support. Where a capability is intended but not built, it is labelled **target**.
> The authority for what may be claimed is `../docs/delivery/CAPABILITY-CLAIMS.md`.

This repository is a **runnable skeleton**, not a finished product. It exists to hand to
AI coding agents (e.g. Claude Code) so they can build the system out from a clean,
opinionated architectural base. The LLM layer is stubbed: no language model is called, no
module under `backend/app/` imports a model client or any HTTP client, and no API key is
required.

**Caveat on "runs".** The documented install path below is recorded as failing on a clean
machine, and the five tests are recorded as passing only in a hand-assembled environment that
departed from it in two ways — one declared dependency was deliberately omitted, and another
was installed without its dependency tree to avoid a platform failure. See `../HANDOFF.md`.
Making a clean-environment install succeed is Phase 0 item P0.2.

## What MERIDIAN is

A three-tier agent-based simulation of a nation in crisis. All three tiers exist as objects in
the scaffold. **No tier reads another tier's state** — cross-tier causality is a target
(Phase 0 item P0.5), not a delivered capability, and any apparent macro↔meso movement in this
scaffold is shared-random-stream contamination rather than a modelled cause.

- **MACRO** — national indicators (inflation, approval, readiness…). Deterministic rules +
  seeded stochastic draws: in the scaffold, one seeded uniform draw per tick applied to one
  indicator. **No LLM.**
- **MESO** — cohorts (representative agents standing for N citizens) and institutions.
  Belief propagation over a network graph is a **target**: today the only cohort field written
  anywhere is `government_competence`, decremented by grievance drift, and diffusion adoption
  is computed but not wired to beliefs. **No LLM for the numbers.**
- **MICRO** — individually simulated institutional agents (ministers, commanders). The stub
  gateway returns an action type by looking the agent's role up in a fixed table; the engine
  then looks that action type up in a fixed seven-entry effects table and applies the
  resulting constant deltas. It performs **no legality check, no feasibility check and no cost
  computation**, and the function that would do so is never passed the agent specification, so
  an agent's declared constraints cannot be consulted.

The single most important architectural commitment is the **determinism boundary**:

> The LLM never mutates macro or meso numeric state directly. It only returns structured
> *proposals*.

The architectural mutation boundary exists in scaffold form, but live model integration,
external-input recording and replay have not yet been implemented. Today `llm_gateway.py`
returns `ActionProposal` objects and imports no state object — but the boundary is satisfied
trivially, because no model is invoked at all, and **there is no structural guard** preventing
a model call path from being added (`config.py` already declares an `llm_mode` of "stub" or
"live"). "Accepts, rejects, or scales" describes a **target**: the engine neither rejects nor
scales anything today.

## Architecture at a glance

```
FastAPI (REST + WebSocket)
        │
        ▼
MeridianModel  (Mesa ABM, seeded)  ──tick──►  MacroState (deterministic)
   │                                              ▲
   │                                              │
   ├─ CohortAgent (meso) ──grievance drift──► cohort.beliefs.government_competence
   │        │                                     ✗ no path to MacroState
   │        └─ diffusion.py ──► model.narrative_adoption
   │                              ← COMPUTED, NOT WIRED TO BELIEFS OR MACRO (P0.5 target)
   │
   └─ InstitutionalAgent (micro) ──llm_gateway──► ActionProposal ──effects-table lookup──┘
        │
        ▼
PostgreSQL (simulation_run, state_snapshot, event_log)   ← PLANNED, NOT WIRED
```

**Reading the diagram honestly.** Only two paths write `MacroState`: the per-tick seeded macro
noise the model applies to itself (`engine.py:136`), and the effects-table lookup on the micro
path (`engine.py:164`). There is **no meso→macro arrow**, because there is no meso→macro
mechanism — this is open critical finding 1, and presenting any apparent macro↔meso movement as
tier interaction is the single most misleading claim available about this codebase.
`diffusion.py` computes `model.narrative_adoption`, which is read only by the API response
(`routes_simulation.py:75`); it reaches no belief and no indicator. The one belief written
anywhere is `government_competence`, decremented by grievance drift (`agents/cohort_agent.py:38`),
which is **not** diffusion.

**On the Postgres node.** Nothing is written to a database. The three model classes are
defined and instantiated nowhere, and no session write call exists anywhere in the scaffold.
The only database operation attempted is table creation at start-up, inside an exception
handler that logs a warning and continues, so the application starts identically with or
without a database. All run state lives in an in-process dictionary that does not survive a
restart.

## Quick start (Docker)

```bash
cp .env.example .env
docker-compose up --build
# API:      http://localhost:8000
# API docs: http://localhost:8000/docs
```

## Quick start (local, no Docker)

**The install is TWO commands, and the second one needs `--no-deps`.** This is deliberate — see
the note below.

```bash
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install --no-deps -r requirements-mesa.txt
uvicorn app.main:app --reload
```

> **Verified by execution on 19 July 2026** — CPython **3.12.10**, Windows 10 with
> `LongPathsEnabled=0`, from an empty virtual environment. Both install commands exit 0 and
> `python -m pytest tests -q` reports **5 passed**. Re-run this check and update the date whenever
> the dependency set changes.
>
> **Why two commands (Phase 0 item P0.2).** The single documented command used to fail outright on
> a clean machine, for two independent reasons, and because pip resolves before installing, either
> one caused *nothing* to install:
> 1. `litellm` was a required dependency but is **imported by no code** — it appears only inside a
>    docstring sketch at `app/simulation/llm_gateway.py:15-24`. On CPython 3.13 it resolved to
>    1.92.0, which publishes no cp313 wheel, fell back to an sdist and demanded a Rust toolchain.
>    It has been moved to the optional `requirements-llm.txt`.
> 2. `mesa` declares `solara`, `matplotlib` and `mesa-viz-tornado`, and the solara/Jupyter tree
>    writes paths longer than the Windows 260-character limit, aborting the install with an
>    `OSError`. MERIDIAN imports none of that tree — mesa is a vestigial base class here — so mesa
>    is installed with `--no-deps` and its three genuine import-time requirements (`tqdm`, `numpy`,
>    `pandas`) are pinned in `requirements.txt` instead.
>
> `pip check` will report `matplotlib`, `solara` and `mesa-viz-tornado` as missing. **That is
> expected and intended, not a broken install.**
>
> Not verified: Linux, macOS, or any Python version other than 3.12.10. No lockfile exists and
> every requirement is an open-ended range, so an install performed on a different date may resolve
> to different versions. There is no `pyproject.toml` and no pinned `requires-python` — adopting
> those is an open owner decision (current-state audit section 8, item 5).

## Run the tests

The test suite is five tests in a single file. Stated precisely: the existing stubbed
execution path reproduces the same tested numeric outputs when the seed, scenario and stubbed
agent outputs remain identical. The same-seed test compares the **final macro dictionary
only** — no cohort belief, no narrative adoption, no event log, no snapshot history — and both
runs call the same in-process stub, so agent output is held constant rather than varied. There
is no continuous integration, so nothing runs these automatically.

```bash
cd backend
pip install -r requirements.txt
pip install --no-deps -r requirements-mesa.txt
python -m pytest tests -v
```

Last run from a clean virtual environment on **19 July 2026**: **5 passed in 0.93s** (CPython
3.12.10, Windows 10). If `import mesa` fails with `ModuleNotFoundError: No module named 'tqdm'`,
the second install command was run without the first.

## Layout

| Path | Purpose |
|---|---|
| `backend/app/main.py` | FastAPI entrypoint |
| `backend/app/simulation/engine.py` | `MeridianModel` — Mesa model + tick loop. The engine is the only component that *decides* numeric state; the assignments themselves execute in `agents/macro_state.py` and `agents/cohort_agent.py`. |
| `backend/app/simulation/agents/` | macro state object + meso/micro agent classes |
| `backend/app/simulation/schemas/` | Pydantic v2 schemas (source of truth for objects) |
| `backend/app/simulation/llm_gateway.py` | **stub** LLM interface — where LiteLLM plugs in |
| `backend/app/simulation/diffusion.py` | narrative-spread diffusion over a networkx graph |
| `backend/app/api/` | REST + WebSocket routes |
| `backend/app/db/` | SQLAlchemy models + session |
| `schemas/` | JSON Schema mirrors for cross-language tooling |
| `scenarios/kestral-strait.json` | the "Republic of Vantara" demo scenario as data |
| `docs/` | ADR log + AI-agent task template |
| `frontend/index.html` | minimal static dev stub (create run, stream ticks over WS) |
| `CLAUDE.md` | project briefing for AI coding agents |

The frontend is a deliberately tiny stub — open `frontend/index.html` in a browser with the
backend running. The full UI (scenario selector, role dashboards, decision composer) is
specified in [`../docs/PLAN.pdf`](../docs/PLAN.pdf) §5 and left for a later build.

## Design docs (source of truth)

This scaffold is derived from the research + design phase. The canonical specs are
consolidated one level up:

- [`../CHARTER.md`](../CHARTER.md) — **the governing design principle.** Read first.
- [`../docs/PLAN.pdf`](../docs/PLAN.pdf) — the full execution-ready plan. Section 3 covers
  schemas and the determinism boundary table, Section 4 the "Kestral Strait" demo scenario,
  Section 5 the 25-screen UX system, Section 6 the stack rationale, and Section 9 the
  nation-archetype expansion framework.

Nation types are **intended** to be data, not code (PLAN.pdf §9): adding an archetype should
mean adding a scenario-template JSON, never editing the engine. **That is a target, and it
does not hold today.** Only one scenario file exists in the tree, and whether a second one
loads and completes a run has never been tested. What is verified is that most scenario
content is read by no code: population weight, demographics, media exposure, campaign data and
the fiction disclaimer are parsed and then never consulted, so two archetypes differing only in
those fields will behave identically. The failure is silent — an action type absent from
`ACTION_EFFECTS` (`backend/app/simulation/engine.py:35-43`) produces an empty delta, and
`apply_deltas` (`backend/app/simulation/agents/macro_state.py:36-41`) skips any key it does not
recognise and any value that is not a top-level number, with no error, no warning and no return
value.

## License note

Stack chosen for permissive licensing: Mesa Apache-2.0, FastAPI MIT, LiteLLM MIT. **That list
is incomplete.** `psycopg2-binary` (`backend/requirements.txt:17`) is **LGPL**, not permissive,
and is absent from the `PLAN.pdf` §2 licence audit. Under the SaaS model `PLAN.pdf` assumes —
dynamic linking, no distribution — the closed audit records it as commercially benign, but the
unqualified sentence was inaccurate. See `docs/ARCHITECTURE_DECISIONS.md`.

There is no licence for MERIDIAN itself, deliberately; the all-rights-reserved position is in
`../NOTICE.md`.
