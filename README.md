# Project MERIDIAN

**A simulated-society crisis simulation engine — a fictional world governed by real-world
causal logic.**

> **Read this before anything else.** MERIDIAN is at scaffold stage. What exists today is a
> skeleton with a five-test suite; the intended architecture below is described as an
> intention wherever it is not yet built. This README was corrected on 19 July 2026 under
> Phase 0 item P0.1 to remove present-tense claims the code does not support. Where a
> capability is a target, it is labelled **target**. The authority for what may be claimed is
> [`docs/delivery/CAPABILITY-CLAIMS.md`](docs/delivery/CAPABILITY-CLAIMS.md).

MERIDIAN is **intended** to model a national population across three tiers — macro (national
indicators), meso (weighted cohorts and institutions), and micro (individually simulated key
actors) — using deterministic rules, seeded stochastic draws, agent-based modelling and
network-diffusion models as the computational substrate. All three tiers exist in the current
scaffold as separate objects, but **no tier reads another tier's state**: the cross-tier
causal channels are a target (Phase 0 item P0.5), not a delivered capability.

A large language model is **intended** to be used selectively: to interpret player decisions,
propose actions for micro-tier agents, generate advisor dialogue, and compose
adversarial-campaign content. **None of that is built.** In the current scaffold no language
model is called: no module under `scaffold/backend/app/` imports a model client or any HTTP
client, and the gateway's two public functions are a role-lookup table and an f-string.

**The architectural mutation boundary exists in scaffold form, but live model integration,
external-input recording and replay have not yet been implemented.** The boundary is
currently satisfied trivially, because no model is invoked at all. There is no structural
guard preventing a model call path from being added.

> **Status:** Independent R&D concept. Fictional simulation and training software — not a
> predictive intelligence tool, not a real-world forecasting system, and not built on or
> targeting real operational vulnerabilities. No real nations, organisations, or named
> individuals are used.

## Start here

| Document | What it is |
|---|---|
| [`CHARTER.md`](CHARTER.md) | **Read first.** The non-negotiable design principle, causal vocabulary, and the eight-question standard every state change must satisfy. |
| [`docs/PLAN.pdf`](docs/PLAN.pdf) | The full execution-ready plan: prior-art landscape, open-source licensing audit, simulation design, demo scenario, UX system, stack, security model, roadmap. |
| [`scaffold/`](scaffold/) | The runnable starter repository — FastAPI + Mesa backend. Its five tests are *recorded as passing* in a hand-assembled environment that departs from the documented install; the documented install path is itself recorded as failing on a clean machine. See [`HANDOFF.md`](HANDOFF.md). |
| [`scaffold/CLAUDE.md`](scaffold/CLAUDE.md) | Project briefing for AI coding agents working in this repo. |
| [`scaffold/docs/ARCHITECTURE_DECISIONS.md`](scaffold/docs/ARCHITECTURE_DECISIONS.md) | Nine ADRs recording the *why* behind each stack choice. |

## The determinism boundary

The **Status** column is the load-bearing one. "Target" means the row describes an intended
capability that does not exist in the code today.

| Layer | Computation mechanism | Status |
|---|---|---|
| Macro indicators | Deterministic rules + seeded stochastic draws. In the scaffold this is one seeded uniform draw per tick, applied to one indicator. | Partially implemented |
| Cohort belief updates | Grievance-driven drift; diffusion adoption computed but not yet wired to beliefs. | Partially implemented |
| Institutional agent decisions | The engine looks the proposed action type up in a fixed seven-entry effects table and applies the resulting deltas. There is no legality check, no feasibility check and no cost computation. | Partially implemented |
| Adversary campaign design | LLM composes content within a fixed schema; diffusion computes spread. No campaign-composition function exists. | **Target — not implemented** |
| Advisor dialogue / briefings | LLM-generated, grounded by retrieval over true state. The stub briefing reads two keys from a dictionary it is handed and returns an f-string; there is no retrieval. | **Target — not implemented** |
| Player decision interpretation | LLM parses input into a schema-validated `intervention` object, validated and priced by the engine. Today the endpoint appends the submission to an in-memory list, returns `accepted: true` unconditionally, and the tick loop never reads that list. | **Target — not implemented** |

## Quick start

**Read this first.** The install path below is recorded as failing on a clean machine, and the
five tests are recorded as passing only in a hand-assembled environment that departed from it in
two ways — one declared dependency was deliberately omitted, and another was installed without its
dependency tree to avoid a platform failure. That environment is not reconstructible from anything
in this repository. Making a clean-environment install succeed on both Windows and Linux is
Phase 0 item P0.2, and it is not done. Expect these commands to fail. No supported Python version
is declared in machine-readable form: there is no `pyproject.toml`, no lockfile and no
`.python-version`, and every one of the thirteen declared dependencies is an open-ended range with
no exact pin. See [`HANDOFF.md`](HANDOFF.md).

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

The test suite is five tests in a single file, and every assertion in it concerns macro state,
tick counts or object attributes. Read precisely:

- `test_same_seed_is_deterministic` compares two same-seed runs' **final macro dictionaries
  only**. It compares no cohort belief, no narrative adoption, no event log and no snapshot
  history, and both runs call the same in-process stub, so agent output is held constant
  rather than varied. The cleared statement of what this supports is: "The existing stubbed
  execution path reproduces the same tested numeric outputs when the seed, scenario and
  stubbed agent outputs remain identical."
- `test_llm_gateway_cannot_write_state` calls the stub gateway once and asserts that the
  returned object is an `ActionProposal` and that this object has no attribute named
  `apply_deltas` and no attribute named `macro_state`. It performs no import-graph analysis,
  attempts no mutation, and exercises no real model. It is **not** a guard against regression
  of the determinism boundary: a gateway that mutated authoritative state by any other route
  would pass it unchanged.

Neither may be weakened. Note also that **there is no continuous integration**: no CI
configuration of any kind exists in the repository, so nothing runs automatically on change.

## Demo scenario

The v1 demo is **"Kestral Strait"** — the fictional Republic of Vantara, a 4.1-million-person
archipelago controlling a contested maritime chokepoint, facing a grey-zone crisis with a
hidden adversarial information campaign. It ships as structured data
([`scaffold/scenarios/kestral-strait.json`](scaffold/scenarios/kestral-strait.json)), not code.

Nation archetypes are **intended** to be data, not code: adding one should mean adding a
scenario-template JSON that conforms to the existing schemas, never editing the engine, and if
the engine appears to need an archetype-specific branch that is a signal the schema is
incomplete. **That is a target, and it does not hold today.** Only one scenario file exists in
the tree, and whether a second one loads and completes a run has never been tested. More
importantly, most scenario content is read by no code at all: population weight, demographics,
media exposure, campaign data and the fiction disclaimer are parsed and then never consulted.
Two archetypes that differ only in those fields will behave identically, and nothing reports
this — the engine's only effect-application path silently skips any key it does not recognise
and any value that is not a top-level number, so an effect that never applies produces no
error and no warning.

## Repository layout

```
CHARTER.md                  governing design principle (non-negotiable)
docs/PLAN.pdf               full execution-ready plan
scaffold/
  backend/app/simulation/   engine, diffusion, LLM gateway, Pydantic schemas
  backend/tests/            five tests: tick counting, same-seed and different-seed macro
                            comparison, one indicator moving, and the gateway attribute check
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
contribution terms are under review. See [`NOTICE.md`](NOTICE.md).
