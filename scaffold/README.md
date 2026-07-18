# MERIDIAN — Synthetic Society Crisis Simulator (Scaffold)

> Working title. Fictional scenarios only — no real nations, organisations, or individuals.

This repository is a **runnable skeleton**, not a finished product. It exists to hand to
AI coding agents (e.g. Claude Code) so they can build the system out from a clean,
opinionated architectural base. Everything here runs with **no API keys** — the LLM layer
is stubbed so the engine, API, and tests work offline.

## What MERIDIAN is

A three-tier agent-based simulation of a nation in crisis:

- **MACRO** — national indicators (inflation, approval, readiness…). Deterministic rules +
  seeded stochastic draws. **No LLM.**
- **MESO** — cohorts (representative agents standing for N citizens) and institutions.
  Belief propagation over a network graph. **No LLM for the numbers.**
- **MICRO** — individually simulated institutional agents (ministers, commanders). The LLM
  *proposes* actions; the engine validates legality and computes effects.

The single most important architectural commitment is the **determinism boundary**:

> The LLM never mutates macro or meso numeric state directly. It only returns structured
> *proposals* that `engine.py` accepts, rejects, or scales.

This is enforced structurally in code (see `llm_gateway.py` — it returns `ActionProposal`
objects and has no reference to any state object), not just documented.

## Architecture at a glance

```
FastAPI (REST + WebSocket)
        │
        ▼
MeridianModel  (Mesa ABM, seeded)  ──tick──►  MacroState (deterministic)
   │                                              ▲
   ├─ CohortAgent (meso)  ──diffusion.py──────────┤  (belief spread over networkx graph)
   └─ InstitutionalAgent (micro) ──llm_gateway──► ActionProposal ──validated by engine──┘
        │
        ▼
PostgreSQL (simulation_run, state_snapshot, event_log)
```

## Quick start (Docker)

```bash
cp .env.example .env
docker-compose up --build
# API:      http://localhost:8000
# API docs: http://localhost:8000/docs
```

## Quick start (local, no Docker)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run the tests

The test suite proves the reproducibility commitment: two runs with the same seed produce
identical macro state after N ticks.

```bash
cd backend
pip install -r requirements.txt
python -m pytest tests -v
```

## Layout

| Path | Purpose |
|---|---|
| `backend/app/main.py` | FastAPI entrypoint |
| `backend/app/simulation/engine.py` | `MeridianModel` — Mesa model + tick loop, the only writer of `MacroState` |
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

Nation types are **data, not code** (PLAN.pdf §9): adding an archetype means adding a
scenario-template JSON, never editing the engine.

## License note

Stack chosen for permissive licensing (Mesa Apache-2.0, FastAPI MIT, LiteLLM MIT). See
`docs/ARCHITECTURE_DECISIONS.md`.
