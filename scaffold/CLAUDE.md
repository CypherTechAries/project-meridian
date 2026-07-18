# CLAUDE.md — MERIDIAN project briefing for AI coding agents

Short, non-obvious project rules. General Python knowledge is assumed.

Read [`../CHARTER.md`](../CHARTER.md) before designing anything. It defines the causal
vocabulary that player actions compile into, and the eight questions every state change must
be able to answer. Output that cannot answer them is flavour text and must not modify the
simulation.

## The one rule you must never break

**The LLM gateway must never mutate macro or meso numeric state directly.** It only returns
*proposal* objects (`ActionProposal`, briefing strings). Only `engine.py`'s tick-processing
code writes to `MacroState` and cohort numbers. If you find yourself importing a state object
into `llm_gateway.py`, stop — you are breaking the determinism boundary that the entire
architecture rests on. See `docs/ARCHITECTURE_DECISIONS.md` (ADR-006).

## Determinism

- Every run has a `seed` threaded through `MeridianModel(seed=...)`.
- Same seed + same scenario + same decisions ⇒ **identical** macro/meso numbers.
- Never introduce unseeded randomness (`random.random()`, `numpy.random.*` without the
  model's RNG, `time`-based values, `dict` ordering assumptions, `set` iteration). Use
  `self.rng` (the model's seeded `random.Random`).
- LLM text is NOT part of reproducible state — it is an interpretive layer, logged
  separately by `model_id + prompt_version + temperature`.
- `tests/test_engine.py` enforces this. Do not weaken it.

## Build / run / test

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
  files and `db/models.py` mirror them — keep all three in sync when you change a field.
- Type-hint everything. Keep the engine free of archetype-specific branches: new nation
  types are data (`scenarios/*.json`), never new code paths (see `design_nation_expansion.md`).

## Adding a nation archetype

Add a `scenarios/<name>.json` following the existing `kestral-strait.json` shape. Do **not**
edit the engine. If the engine seems to need a special case, the schema is incomplete — fix
the schema instead.

## Branch / PR conventions

<!-- PLACEHOLDER: fill in with the team's real conventions -->
- Branch: `feature/<short-slug>` or `fix/<short-slug>`.
- PRs must keep `pytest` green and must not weaken the determinism test.
- One logical change per PR; describe the determinism impact if any.
