# Agent Task Template

Copy this block into the ticket/prompt you hand an AI coding agent (e.g. Claude Code) working
in this repo. Keep it short: state only what is non-obvious or specific to *this* task. The
agent already reads `CLAUDE.md` for project-wide rules — do not repeat those here.

Follows Anthropic's CLAUDE.md guidance: brief the agent like a smart colleague who just walked
in. Give the goal, the constraints, and how to verify — not a step-by-step script.

---

## Ticket: <short imperative title>

**Goal (why this matters):**
<1–3 sentences. What outcome are we after and why. Not the implementation.>

**Scope — in:**
- <file/module/endpoint the change should touch>

**Scope — out (do not touch):**
- <areas explicitly off-limits, e.g. "do not change the diffusion math">

**Non-obvious context:**
- <anything the agent can't infer from the code: a hidden constraint, a past incident, a
  design nuance from the workspace `design_*.md` docs>

**Determinism check (mandatory for engine/agent/diffusion changes):**
- Does this change introduce randomness? If so, it MUST draw from `self.rng`, never the global
  `random`/`numpy`. Confirm `test_same_seed_is_deterministic` still passes.
- Does this change let the LLM write numeric state? If so, STOP — that violates ADR-006.

**Acceptance criteria:**
- [ ] `cd backend && python -m pytest tests -v` is green.
- [ ] If a schema field changed, the Pydantic model, `/schemas/*.schema.json`, and
      `db/models.py` are all updated in sync.
- [ ] No new archetype-specific branch in the engine (ADR-008) — new nation behaviour is data.
- [ ] <task-specific check>

**How to verify manually (if applicable):**
- <e.g. "run `uvicorn app.main:app`, POST to /api/simulation/runs, confirm ...">

---

### Worked example

## Ticket: Apply campaign diffusion to cohort belief updates

**Goal:** Hostile campaigns currently spread narrative adoption but don't yet move cohort
beliefs. Wire adoption into `support_for_western_alignment` so the demo scenario's info-op has
a visible, explainable effect.

**Scope — in:** `engine.py` (`_step_diffusion`), `cohort_agent.py`.
**Scope — out:** `diffusion.py` math, the macro rules.
**Non-obvious context:** `design_simulation_schemas.md` says the LLM may *label* a belief shift
but must not compute it — the number comes from diffusion output only.
**Determinism check:** adoption already uses `self.rng`; keep belief update a pure function of
adoption so reproducibility holds.
**Acceptance:** pytest green; add a test asserting a targeted cohort's belief moves after 10
ticks with the campaign present and does not when it's absent.
