# CLAUDE.md — MERIDIAN project briefing for AI coding agents

Short, non-obvious project rules. General Python knowledge is assumed.

> **Corrected 19 July 2026** under Phase 0 item P0.1, to remove present-tense claims the code does
> not support. This file is a **briefing of rules to follow**, not a description of working
> software. Where a rule states a property the code is meant to hold, that property is labelled
> **target** if it is not yet true. Nothing here has been weakened as a *rule*. The authority for
> what may be claimed is `../docs/delivery/CAPABILITY-CLAIMS.md`.
>
> Read this before trusting anything below: MERIDIAN is a scaffold with a five-test suite. No
> language model is called; no module under `backend/app/` imports a model client or any HTTP
> client. Nothing is written to a database. No tier reads another tier's state.

Read [`../CHARTER.md`](../CHARTER.md) before designing anything. It defines the causal
vocabulary that player actions compile into, and the eight questions every state change must
be able to answer. Output that cannot answer them is flavour text and must not modify the
simulation.

## The one rule you must never break

**The LLM gateway must never mutate macro or meso numeric state directly.** It only returns
*proposal* objects (`ActionProposal`, briefing strings). `engine.py` is the only component that
*decides* numeric state; the assignments themselves execute in
`app/simulation/agents/macro_state.py:47` (macro) and `app/simulation/agents/cohort_agent.py:38`
(cohort beliefs), both reached only from `engine.py:136` and `:164`. If you find yourself importing
a state object into `llm_gateway.py`, stop — you are breaking the determinism boundary that the
entire architecture rests on. See `docs/ARCHITECTURE_DECISIONS.md` (ADR-006).

**Do not read this rule as a property the code currently guarantees.** The boundary is at present
satisfied trivially, because no model is invoked at all, and **there is no structural guard**
preventing a model call path from being added — `app/config.py:23-25` already declares an
`llm_mode` of "stub" or "live". The rule is binding on you; it is not enforced by the code.

## Determinism

- Every run has a `seed` threaded through `MeridianModel(seed=...)`. There is exactly one
  `random.Random` in application code (`app/simulation/engine.py:83`) and exactly three draw
  sites (`agents/cohort_agent.py:36`, `diffusion.py:75`, `engine.py:135`).
- **What is true today**, and the cleared sentence to use verbatim: "The existing stubbed
  execution path reproduces the same tested numeric outputs when the seed, scenario and stubbed
  agent outputs remain identical." Note the condition — both runs call the same in-process stub,
  so agent output is held constant rather than varied.
- **The "+ same decisions" form is wrong and must not be written.** Submitted decisions never
  reach the tick loop: `POST /runs/{id}/decision` appends to an in-memory list
  (`app/api/routes_simulation.py:80-101`) that `step()` (`engine.py:147-180`) never reads.
- **TARGET, not delivered:** "Given the same scenario version, rule-pack version, seed, ordered
  player inputs and recorded external-agent inputs, the engine is intended to reproduce identical
  authoritative state hashes." Both this and the cleared sentence above are founder-settled — do
  not paraphrase or shorten either.
- Never introduce unseeded randomness (`random.random()`, `numpy.random.*` without the
  model's RNG, `time`-based values, `dict` ordering assumptions, `set` iteration). Use
  `self.rng` (the model's seeded `random.Random`).
- **CORRECTED 22 July 2026 — P0.4A IS IMPLEMENTED.** This entry previously read "Nothing of P0.4A
  is implemented", and that was stale: it caused an agent to advise the owner that randomness was
  blocked for a reason that no longer applied. `engine.py` builds a `DeterministicDrawService`
  (ADR-010, accepted) in which every draw is a pure function of (run seed, canonical key). There
  is **no shared stream**, nothing accumulates and nothing advances, so adding, removing or
  reordering a draw in one subsystem **cannot** shift results in another. That was the mechanism
  behind A3's finding that apparent meso→macro coupling was stream displacement rather than
  causality (`../docs/delivery/A3-VERIFICATION-RESULTS.md:142-175`), and it is fixed. There is no
  `self.rng`; mesa's own `Model.random` is seeded but never used for authoritative values.
- LLM text is NOT part of reproducible state — it is an interpretive layer. It is **intended** to
  be logged separately by `model_id + prompt_version + temperature`; that is the contract for when
  a live model is wired, not current behaviour. `PROMPT_VERSION = "v1"` is declared once
  (`app/simulation/llm_gateway.py:38`) and read by nothing, and neither `model_id` nor temperature
  is logged anywhere.
- `tests/test_engine.py` is five tests in one file, and every assertion in it concerns macro state,
  tick counts or object attributes. It does **not** enforce the above.
  `test_same_seed_is_deterministic` compares the final macro dictionary only (`:34-40`) — no cohort
  belief, no narrative adoption, no event log, no snapshot history — and
  `test_llm_gateway_cannot_write_state` calls the stub gateway once and asserts the returned object
  is an `ActionProposal` with no attribute named `apply_deltas` and no attribute named
  `macro_state` (`:61-77`). No import-graph analysis, no attempted mutation, no real model: a
  gateway that mutated authoritative state by any other route would pass it unchanged. **Do not
  weaken either test** — the weakness is a reason to strengthen them, not to relax them.
- **There is no continuous integration**, so nothing runs these automatically. No CI configuration
  of any kind exists in the repository.

## Build / run / test

**Caveat before you run any of this.** The documented install path below is recorded as failing on
a clean machine, and the five tests are recorded as passing only in a hand-assembled environment
that departed from it in two ways — one declared dependency was deliberately omitted, and another
was installed without its dependency tree to avoid a platform failure. See `../HANDOFF.md`. Making
a clean-environment install succeed is Phase 0 item P0.2. Expect the first command to fail.

```bash
# tests (must pass before any PR)
cd backend && pip install -r requirements.txt && python -m pytest tests -v

# run API locally
uvicorn app.main:app --reload

# full stack
docker-compose up --build
```

## Code style

- Python 3.11+, FastAPI, **Pydantic v2** (`model_config`, `Field(..., description=...)`,
  `model_dump()` — not the v1 `.dict()` API).
- Schemas in `app/simulation/schemas/` are the source of truth. The `/schemas/*.schema.json`
  files and `db/models.py` mirror them — keep all three in sync when you change a field. **The
  mirrors are hand-maintained, not generated:** no `model_json_schema()` call and no generation
  script exists in the tree, and no JSON Schema validation library is present, so the nine files
  under `/schemas` validate nothing at runtime and can drift undetected. Syncing them is your job,
  and nothing will tell you if you forget.
- Type-hint everything. Keep the engine free of archetype-specific branches: new nation
  types are data (`scenarios/*.json`), never new code paths (see `../docs/PLAN.pdf` §9, the
  nation-archetype expansion framework — a previous version of this line cited
  `design_nation_expansion.md`, which does not exist and never has).

## Adding a nation archetype

Add a `scenarios/<name>.json` following the existing `kestral-strait.json` shape. Do **not**
edit the engine. If the engine seems to need a special case, the schema is incomplete — fix
the schema instead.

**That is the rule to follow, not a description of what works.** It is publication blocker B4, and
you should expect to hit its limits immediately:

- Only one scenario file exists in the tree. Whether a second one loads and completes a run has
  never been tested.
- Most scenario content is read by **no code**. `represents_population`, demographics, media
  exposure, campaign fields and the fiction disclaimer are parsed and then never consulted. Two
  archetypes differing only in those fields will behave identically.
- The failure is **silent**. An action type absent from `ACTION_EFFECTS`
  (`app/simulation/engine.py:35-43`) resolves to an empty delta, and `apply_deltas`
  (`app/simulation/agents/macro_state.py:36-41`) skips any key it does not recognise and any value
  that is not a top-level number — no error, no warning, no return value. Your new scenario can
  load cleanly and change nothing.

If you add a scenario, verify its effect by comparing runs, not by observing that it loaded.

## Branch / PR conventions

<!-- PLACEHOLDER: fill in with the team's real conventions -->

> **Unresolved — owner decision required (19 July 2026, P0.1).** The `PLACEHOLDER` marker above is
> the only one left in the project and Phase 0 cannot exit while it stands
> (`../docs/delivery/CURRENT-STATE-AUDIT.md:433`; backlog entry CB-18). It has **not** been
> resolved here: an AI agent may draft a record but may not settle a policy decision. What is
> already settled is narrow — the default branch is `main` (`../HANDOFF.md:21`) and external code
> contributions are not accepted (`../HANDOFF.md:23`) — which leaves the review and merge policy
> for the owner's own work unrecorded. The three bullets below are the scaffold's original text
> and are retained unchanged; treat them as a draft awaiting the owner, not as agreed policy.
> Note also that **no CI enforces any of them**: there is no continuous integration in this
> repository, so "must keep `pytest` green" is a convention held by hand.

- Branch: `feature/<short-slug>` or `fix/<short-slug>`.
- PRs must keep `pytest` green and must not weaken the determinism test.
- One logical change per PR; describe the determinism impact if any.
