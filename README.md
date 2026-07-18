# Project MERIDIAN

**A synthetic-society crisis simulation engine — a fictional world governed by real-world
causal logic.**

MERIDIAN models a national population across three tiers — macro (national indicators),
meso (weighted cohorts and institutions), and micro (individually simulated key actors) —
using deterministic rules, seeded stochastic draws, agent-based modelling and
network-diffusion models as the computational substrate. A large language model is used
selectively: to interpret player decisions, propose actions for micro-tier agents, generate
advisor dialogue, and compose adversarial-campaign content.

**It never directly mutates macro or meso numeric state.** That boundary — enforced in code
and guarded by a test, not merely documented — is the single most important architectural
commitment in the project.

> **Status:** Independent R&D concept. Fictional simulation and training software — not a
> predictive intelligence tool, not a real-world forecasting system, and not built on or
> targeting real operational vulnerabilities. No real nations, organisations, or named
> individuals are used.

## Start here

| Document | What it is |
|---|---|
| [`CHARTER.md`](CHARTER.md) | **Read first.** The non-negotiable design principle, causal vocabulary, and the eight-question standard every state change must satisfy. |
| [`docs/PLAN.pdf`](docs/PLAN.pdf) | The full execution-ready plan: prior-art landscape, open-source licensing audit, simulation design, demo scenario, UX system, stack, security model, roadmap. |
| [`scaffold/`](scaffold/) | The runnable starter repository — FastAPI + Mesa backend with a passing test suite. |
| [`scaffold/CLAUDE.md`](scaffold/CLAUDE.md) | Project briefing for AI coding agents working in this repo. |
| [`scaffold/docs/ARCHITECTURE_DECISIONS.md`](scaffold/docs/ARCHITECTURE_DECISIONS.md) | Nine ADRs recording the *why* behind each stack choice. |

## The determinism boundary

| Layer | Computation mechanism | LLM involvement |
|---|---|---|
| Macro indicators | Deterministic rules + seeded Monte Carlo draws | None |
| Cohort belief updates | Seeded diffusion over the social graph | None for the numbers; may label the resulting shift |
| Institutional agent decisions | LLM proposes; engine validates legality and computes cost/effect | Proposes only |
| Adversary campaign design | LLM composes content within a fixed schema; diffusion computes spread | Creative content only |
| Advisor dialogue / briefings | LLM-generated, grounded by retrieval over true state | Primary generator, constrained to real state fields |
| Player decision interpretation | LLM parses input into a schema-validated `intervention` object | Primary interpreter; engine rejects invalid actions |

## Quick start

```bash
cd scaffold
cp .env.example .env
docker-compose up --build      # API on :8000, docs on :8000/docs
```

Or without Docker:

```bash
cd scaffold/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests -v      # no API keys required — the LLM gateway ships in stub mode
uvicorn app.main:app --reload
```

The test suite is the point: `test_same_seed_is_deterministic` proves reproducibility and
`test_llm_gateway_cannot_write_state` guards the determinism boundary against regression.
Neither may be weakened.

## Demo scenario

The v1 demo is **"Kestral Strait"** — the fictional Republic of Vantara, a 4.1-million-person
archipelago controlling a contested maritime chokepoint, facing a grey-zone crisis with a
hidden adversarial information campaign. It ships as structured data
([`scaffold/scenarios/kestral-strait.json`](scaffold/scenarios/kestral-strait.json)), not code.

Nation archetypes are **data, not code**. Adding one means adding a scenario-template JSON
that conforms to the existing schemas — never editing the engine. If the engine appears to
need an archetype-specific branch, the schema is incomplete.

## Repository layout

```
CHARTER.md                  governing design principle (non-negotiable)
docs/PLAN.pdf               full execution-ready plan
scaffold/
  backend/app/simulation/   engine, diffusion, LLM gateway, Pydantic schemas
  backend/tests/            determinism + boundary tests
  schemas/                  JSON Schema mirrors for cross-language tooling
  scenarios/                nation archetypes as data
  docs/                     ADR log + AI-agent task template
  frontend/                 minimal dev stub (the full 25-screen UX is specified, not built)
```

---

Copyright © 2026 Aries Russell. All rights reserved. An independently developed research and
demonstration project, not affiliated with, endorsed by, commissioned by, or produced for any
employer or prospective employer. No permission is granted to use, reproduce, modify or
distribute this software except as permitted by GitHub's Terms of Service. Licensing and
contribution terms are under review. See [`COPYRIGHT.md`](COPYRIGHT.md).
