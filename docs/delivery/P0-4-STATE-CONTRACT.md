# P0.4 — authoritative state contract and mutation boundary

**Status:** DRAFT, pending owner review · **Date:** 19 July 2026 · **Phase 0 item:** P0.4

---

## What P0.4 delivered, and what it did not

**Delivered.** One versioned authoritative state structure, one controlled mutation path, an
explicit ownership map, structural validation, deterministic serialisation, and 26 new tests. The
existing five tests pass **unchanged** — no numeric output moved.

**NOT delivered, and not claimed.** No persistence. No event sourcing. No replay. No state
hashing. No cross-tier causality. No legality, authority, resource or feasibility validation. No
decay, cost or cooldown mechanism. Nothing survives the process.

`TransitionRecord` is a **return value, not a persisted event**. `transition_log` is an in-memory
diagnostic list from which no state can be rebuilt. Do not call any of this an event store, a
replay system or causal reconstruction — those are P0.6.

---

## Plain-English layer

Before P0.4, "the state of the simulation" was not one thing. The tick lived on the model, macro
indicators lived inside a holder object, cohort beliefs lived inside agent-owned records, and
narrative adoption was a dictionary on the model. Anything holding a reference could change any of
it, and several things did — including an API route that appended to the engine's event log while
serving a request.

Now there is one object that *is* the state, and one service that is the only thing allowed to
change it. Everything else reads. A change that is malformed, names an indicator that does not
exist, or arrives from a presentation path is rejected, and rejection leaves the state exactly as
it was.

This does not make the simulation more capable. It makes it possible to say *what the state is*
and *what changed it* — which is what replay, snapshots and cross-tier causality will need.

---

## 1. Authoritative state envelope

`scaffold/backend/app/simulation/state.py` — `AuthoritativeState`, schema version **0.4.0**.

| Section | Field | Notes |
|---|---|---|
| Versioning | `schema_version` | shape of this structure |
| | `rule_pack_version` | `"unversioned-inline-0"` — rules are hardcoded, not packaged |
| | `state_version` | monotonic count of **applied** transitions; not a tick count |
| Identity | `scenario.scenario_id` / `scenario_version` | version is `"unversioned"` — scenario files carry no version field |
| Run | `run.seed`, `rng_algorithm`, `rng_algorithm_version` | records `python-random-Mersenne` because that is what actually draws |
| | `run.named_substreams` | **`False`** — P0.4A has not happened |
| Clock | `tick` | |
| Macro | `macro` | the existing `MacroState` |
| Meso | `cohorts{id → CohortRuntimeState}` | **mutable beliefs only**; static cohort config stays in the scenario spec |
| | `narrative_adoption{id → float}` | reaches no belief and no indicator |
| Micro | `institutions{id → InstitutionRecord}` | identity and role only — no authority model |
| Scenario | `campaign` | read by nothing |
| Pending | `pending_actions[AcceptedAction]` | recorded, `applied=False`, nothing reads them |
| **Hooks** | `entities` | **`{}`** — no persistent entity model exists |
| | `relationships` | **`[]`** — no relationship graph exists |
| | `external_input_cursor` | **`None`** — no external input recorded, no replay |

The three hooks are deliberately empty and asserted empty by test. They exist so successor work
has a defined home and no future change silently invents a new top-level section. An empty
collection here is an honest statement that MERIDIAN models none of it.

---

## 2. State ownership map

| Section | Owner (writes) | Readers | Derived? |
|---|---|---|---|
| `tick` | `TransitionService` via `ADVANCE_TICK` | engine, agents, API, tests | authoritative |
| `macro.indicators` | `TransitionService` via `APPLY_MACRO_DELTAS` | `macro_snapshot()`, API, briefing | authoritative |
| `macro.tick` | `TransitionService` (kept in step with `tick`) | snapshot consumers | authoritative, redundant copy |
| `cohorts[*].beliefs` | `TransitionService` via `SET_COHORT_BELIEF` | `CohortAgent.step` reads current value | authoritative |
| `narrative_adoption` | `TransitionService` via `SET_NARRATIVE_ADOPTION` | API response | authoritative |
| `pending_actions` | `TransitionService` via `RECORD_PLAYER_DECISION` | nothing | authoritative |
| `institutions`, `campaign`, `scenario`, `run` | set at construction only | engine, tests | authoritative, immutable after init |
| Cohort static config (`demographics`, `grievances`, `represents_population`, susceptibility) | nobody — scenario-derived | `CohortAgent`, diffusion | **configuration, not runtime state** |
| `snapshots`, `event_log`, `transition_log` | engine, append-only | tests, diagnostics | **derived / diagnostic, NOT authoritative** |
| `macro_snapshot()`, `canonical_state()`, briefings, every UI projection | — | — | **derived; must never be written back** |

**Single writer:** `TransitionService.apply` (`transitions.py`). Nothing else may write.

---

## 3. Central transition service

`scaffold/backend/app/simulation/transitions.py`

**Accepts** a `Transition`: `type` (closed enum), `origin`, `payload`, optional
`expected_state_version` (optimistic concurrency), `mechanism`, `actor`, and `draw_refs` — a P0.4A
hook that is always empty, because with no named substreams a draw cannot yet be identified
independently of global stream position.

**Returns** a `TransitionRecord`: `transition_id`, `applied`, `validation`, `tick`,
`state_version_before`/`after`, field-level `delta` (before/after), `mechanism`, `actor`.

Transition types are a **closed set** — `ADVANCE_TICK`, `APPLY_MACRO_DELTAS`, `SET_COHORT_BELIEF`,
`SET_NARRATIVE_ADOPTION`, `RECORD_PLAYER_DECISION`. A new mutation path cannot appear without
being declared, and an undeclared type is rejected at construction.

---

## 4. Mutation paths — inventoried and redirected

| Path | Before | Now |
|---|---|---|
| `self.tick += 1` (`engine.step`) | direct write | `ADVANCE_TICK` |
| `macro.state.tick = self.tick` | second direct write | folded into `ADVANCE_TICK` |
| `MacroStateHolder.apply_deltas` ← macro noise | direct `setattr` | `APPLY_MACRO_DELTAS` |
| `MacroStateHolder.apply_deltas` ← priced action | direct `setattr` | `APPLY_MACRO_DELTAS`, origin `LLM_PROPOSAL` |
| `b.government_competence = …` (`cohort_agent.py:38`) | **in-place agent write** | `SET_COHORT_BELIEF` |
| `self.narrative_adoption = …` | wholesale replacement | `SET_NARRATIVE_ADOPTION` |
| **`model.event_log.append(...)` inside `POST /runs/{id}/decision`** | **presentation route writing engine state** | `RECORD_PLAYER_DECISION` → `pending_actions` |

**Verified by sweep** that no authoritative write remains outside the boundary. The remaining
`.append` calls are `snapshots`, `event_log` and `transition_log` — diagnostic, non-authoritative,
and documented as such.

### API response correction

`POST /runs/{id}/decision` previously returned `{"accepted": true}` unconditionally. It now
returns `recorded`, `applied: false`, a `transition_id`, and a note stating that no legality,
authority, resource or feasibility validation exists and the decision will have no effect. The
client-supplied `legal_check` is still preserved verbatim and still **not trusted**.

### Compatibility debt

**`MacroStateHolder`** (`agents/macro_state.py`) is orphaned but retained as a **tripwire**: every
method raises `NotImplementedError`. A live-but-unused mutation method is a second write path
waiting to be reintroduced, and a loud failure beats a silent bypass. Delete once no documentation
references it. Asserted by test.

---

## 5. Validation — implemented vs explicitly unimplemented

**Implemented (structural only):** known transition type · well-formed payload · target references
exist (cohort, belief, indicator) · indicator is a top-level numeric scalar · delta values numeric
· state-version match when supplied · tick advances by exactly one · presentation origin rejected.

**Explicitly NOT implemented** — enumerated in code as `UNIMPLEMENTED_VALIDATION` and echoed on
every `ValidationResult`, so structural acceptance can never be mistaken for policy approval:

- **legality** — no rule evaluates whether an action is permitted (blocker **B1**)
- **authority** — no check that the actor holds the power to act
- **resource / fiscal** — no engine action touches fiscal state
- **feasibility** — no capability, capacity or logistics model
- **temporal** — `Intervention.timeline_days` is never read; effects apply immediately
- **scenario constraints** — proven causally inert by substitution (A3 check 3)

**One behavioural improvement:** unknown macro keys are now **rejected**. Previously
`apply_deltas` silently skipped them, so a misspelled or nested indicator produced no error, no
warning and no effect. This is the audit's `apply_deltas` sub-finding, closed.

---

## 6. Canonical serialisation

`canonical_json(state)` — `json.dumps` with `sort_keys=True`, fixed separators, `ensure_ascii=True`,
over `model_dump(mode="json")`.

Guarantees: key order independent · no object identity, memory address or type repr · no wall-clock
timestamp (authoritative state contains none by construction) · stable across repeated calls.

**Not a state hash. Not replay.** Float formatting follows CPython's repr — stable within a build,
**not** a cross-language or cross-version guarantee. Do not claim one.

---

## 7. Tests — 31 total, all passing

`tests/test_engine.py` — **5, unchanged and not weakened.**
`tests/test_state_transitions.py` — **26 new.**

Construction and hook emptiness · same transition on same state gives identical result ·
`state_version` increments only on applied transitions · five parametrised rejection cases leave
state **byte-identical** · unknown key rejected not skipped · presentation origin rejected ·
derived reads (snapshot, canonical, briefing) mutate nothing · LLM proposal carries no state
authority · every engine mutation passes the boundary · applied transitions carry mechanism
attribution · tick advances only via transition · cohort belief changes routed · player decision
recorded but not applied · serialisation stable, key-order independent, free of object identity ·
**two same-seed runs serialise identically across the whole state** — strictly stronger than the
original macro-only determinism test, which never inspected cohort beliefs or narrative adoption ·
validation scope declared honestly · closed type set · retirement tripwire fires.

---

## 8. Blockers

**To P0.4A (deterministic randomness):** none from P0.4. The `draw_refs` hook and
`run.rng_algorithm` / `named_substreams` fields exist and are honestly populated. The draw pattern
was deliberately left unchanged, because altering it would move existing tested numeric outputs —
that change belongs to P0.4A with its isolation tests.

**To the first P0.5 causal chain:**

1. **No cross-tier read path is defined.** A transition can write any tier, but no mechanism reads
   one tier to compute another. P0.5 must define the channel, not just the write.
2. **`represents_population` is still read by nothing** — population weighting does not affect
   aggregation. This is P0.5's named commitment.
3. **No decay, cost or cooldown anywhere.** A causal channel feeding a monotonically saturating
   macro tier will saturate faster. This has **no Phase 0 owner** and is worth assigning.
4. **RNG contamination is unfixed until P0.4A.** Any new conditional draw in a causal channel
   shifts every later draw everywhere, so a P0.5 effect could not be distinguished from stream
   displacement. **P0.4A should land before P0.5 implementation** — as the founder's sequencing
   already requires.
5. `entities` and `relationships` are empty; a chain through named people needs the world model.

---

## 9. Known limitations

- `TransitionService.state` returns a live Pydantic model. Python cannot prevent a caller mutating
  it without freezing the model, which would break in-place application. **Enforcement is by test,
  not by the type system** — stated as a limitation, not a guarantee.
- Transitions apply **in place**. No copy-on-write, no rollback beyond "rejected changes nothing".
- `macro.tick` duplicates `state.tick`. Kept in step by the boundary; the duplication should be
  removed when `MacroState` is next revised.
- Nothing persists.
