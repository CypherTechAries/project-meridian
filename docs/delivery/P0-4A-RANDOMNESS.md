# P0.4A — deterministic randomness architecture: status and evidence

**Status:** DRAFT, pending owner review · **Date:** 19 July 2026 · **Phase 0 item:** P0.4A
**Implements:** ADR-010 (Accepted, keyed/counter-based)

---

## What changed, in one paragraph

Authoritative randomness is no longer a shared sequential stream. Every draw is now a pure
function of `(run seed, canonical key)` via HMAC-SHA-256. Nothing accumulates and nothing
advances, so a draw added, removed or reordered in one subsystem **cannot** shift a value in
another. This removes the mechanism behind A3's finding that apparent meso→macro coupling was
stream displacement rather than causality.

**This is not replay.** It is the determinism replay will depend on. No inputs are recorded and no
run can be reconstructed — that is P0.6.

---

## Two bounded checks (performed before implementation)

**1. `transition_id` — already deterministic, refined.** Produced as
`f"txn-{tick}-{counter:04d}"` from a monotonic per-service counter. **No** UUID4, wall-clock time,
process identity, object identity, `hash()`, unordered iteration or global randomness. Two
properties recorded: the counter increments on rejections too (so the id sequence depends on
rejection history — deterministic, but order-sensitive), and ids are minted after application, so
an `ADVANCE_TICK` id names the tick it produced. Both are stable given identical inputs.

**2. `schema_version` vs `state_revision` — were separate, now unambiguously named.** They were
never overloaded: `schema_version` describes the state *shape*, the other counts accepted
transitions. But `state_version` sat confusingly close to `schema_version`, so it is renamed
**`state_revision`** throughout, along with `expected_state_revision` and
`state_revision_before`/`after`.

---

## Algorithm — fully specified

| | |
|---|---|
| Algorithm | **HMAC-SHA-256** (stdlib `hmac` + `hashlib`; **no new dependency**) |
| Algorithm version | `hmac-sha256-v1` |
| Key encoding version | `meridian-key-v1` |
| HMAC key | `b"meridian-rng-v1|seed=<run_seed>"` (UTF-8) |
| HMAC message | canonical key encoding (UTF-8) |
| Byte→integer | `int.from_bytes(digest[0:8], "big")` → unsigned 64-bit |
| Float mapping | `(u64 >> 11) / 2**53` → `[0.0, 1.0)`, 53-bit exact — every representable double reachable, no modulo |
| Bounded integer | **rejection sampling**: reject at/above the largest exact multiple of `bound`, retry at a derived sub-index. Never `% bound`, which would favour low residues |
| Repeated draws | explicit `index` field in the key; **never** implicit advancement |

### Canonical key encoding

Fields in **fixed order** — `scenario, rule_pack, subsystem, entity, purpose, context, index` —
each **length-prefixed in bytes** so the encoding is injective:

```
meridian-key-v1<len>:<field>=<len>:<value>;   … per field, fixed order
```

Length-prefixing means two different field sets cannot collide (`purpose="b=c"` is distinguishable
from `purpose="b", entity="c"` — asserted by test). Field order comes from a module constant, not
dict iteration. **Python `hash()` is never used** — it is randomised per process.

Appending a new key field changes every derived value and is a breaking change requiring a
`KEY_ENCODING_VERSION` bump.

### Published test vectors

Seed `88213`, scenario `kestral-strait`, rule pack `unversioned-inline-0`:

| Key | uint64 | unit_float |
|---|---|---|
| `macro / shipping_noise / — / 1 / 0` | `9516692881769196066` | `0.5159009548645749` |
| `cohort / grievance_drift / coastal-creole-fishing / 1 / 0` | `13743487525525919111` | `0.7450359516351315` |

**Reproducibility claim, precisely.** Deterministic on the tested CPython implementation, verified
in-process and across subprocesses with `PYTHONHASHSEED` of `0`, `1` and `12345`.
**Cross-language and cross-version reproducibility is NOT claimed** — these vectors have not been
reproduced outside Python. Do not widen this claim until they have been.

---

## Draw API — only what current behaviour needs

`scaffold/backend/app/simulation/draws.py` — `DeterministicDrawService`

`uint64` · `unit_float` · `uniform(low, high)` · `jitter(magnitude)` · `bounded_int(bound)` ·
`reference(...)`

Every method takes `(subsystem, purpose, entity="", context="", index=0)`. **No weighted choice
and no distributions were added** — nothing currently requires them.

**Draw reference** (`DrawReference`, for `Transition.draw_refs`): `ref` string, `algorithm`,
`key_encoding`, `subsystem`, `purpose`, `entity`, `context`, `index`, `digest` (first 4 bytes hex).
`reference()` consumes nothing — asserted by test. Recording a reference is **not** replay.

---

## Randomness inventory

| Site | Classification | Disposition |
|---|---|---|
| `engine._step_macro_rules` — shipping noise | **authoritative** | **migrated** → `macro/shipping_noise`, keyed on tick |
| `cohort_agent.step` — grievance drift | **authoritative** | **migrated** → `cohort/grievance_drift`, keyed on cohort + tick |
| `diffusion.linear_threshold_step` — per-node jitter | **authoritative** | **migrated** → `diffusion/adoption_jitter`, keyed on cohort + tick |
| `MeridianModel.rng = random.Random(seed)` | **authoritative — the shared stream itself** | **removed**; `self.rng` no longer exists |
| `mesa.Model.__init__(seed=…)` → `Model.random` | dependency-internal | **excluded** — mesa seeds its own generator; MERIDIAN never uses it for authoritative values |
| `runs.py` — `uuid.uuid4().hex` for `run_id` | infrastructure, **not authoritative state** | **excluded** — the registry key is not in `AuthoritativeState`; recorded as a known non-determinism outside the contract |
| `llm_gateway` stub | no randomness (fixed role lookup) | n/a |
| Tests / fixtures | test-only | n/a |
| C0 frontend | presentation-only, fixture data | **excluded** — must stay outside authoritative state |

**Enforcement** is by AST-based test, not regex: `test_no_global_random_calls_in_authoritative_modules`
walks the parsed tree of seven authoritative modules and fails on any `import random`,
`from random import`, or `random.*` attribute access; `test_python_hash_is_not_used_in_authoritative_modules`
fails on any `hash()` call. AST rather than text because these modules *discuss* `hash()` and
`random` in their docstrings — a text search would flag the explanation as a violation.
`test_engine_exposes_no_unrestricted_generator` asserts `model.rng` does not exist and the draw
service exposes no `random`/`getrandbits`/`shuffle`/`choice`.

---

## Deterministic outputs DID change — intentionally

Replacing the shared stream necessarily changes every drawn number. Old numbers were **not**
preserved, because preserving them would have required keeping the stream that caused the defect.

Seed `88213`, 20 ticks, after P0.4A:

| Indicator | Value |
|---|---|
| `military_readiness` | `0.5900000000000002` |
| `government_approval` | `0.48000000000000004` |
| `social_stability_index` | `0.5700000000000001` |
| `shipping_throughput_pct_of_baseline` | `0.6121662567595042` |
| `state_revision` | `260` |

**No golden expectations needed updating**: the existing five tests compare two runs to each other,
or compare before/after within a run — none hardcodes a literal. That is why they pass unchanged.

Two saturating indicators remain saturating. **P0.4A did not and could not fix that** — macro
saturation is a separate open critical finding with no decay, cost or cooldown mechanism anywhere,
and it still has no Phase 0 owner.

---

## Adversarial tests — 30 new, all passing

`tests/test_deterministic_draws.py`. Against the founder's required list:

| # | Property | Test |
|---|---|---|
| 1 | Same key + seed ⇒ same output | `test_same_key_same_seed_is_stable`, `test_two_services_same_seed_agree` |
| 2 | Purpose isolation | `test_different_purposes_are_isolated` |
| 3 | Entity isolation | `test_different_entities_are_isolated` (+ subsystem, context) |
| 4 | Seed divergence | `test_different_seeds_produce_different_outputs` (+ scenario/rule-pack) |
| 5 | **Extra unrelated draw shifts nothing** | `test_extra_unrelated_draw_does_not_shift_another_value` — 500 unrelated draws, target unmoved |
| 6 | Reordering changes nothing | `test_reordering_independent_entity_draws_changes_nothing` |
| 7 | Adding an entity changes nothing | `test_adding_an_unrelated_entity_does_not_change_existing_entities` |
| 8 | Rejected transitions consume nothing | `test_rejected_transition_does_not_affect_future_draws` — 12 rejections, state identical to a clean run |
| 9 | Repeated draws need explicit indices | `test_repeated_draws_need_an_explicit_index` |
| 10 | Promotion draws disturb nothing | `test_promotion_style_draw_does_not_alter_unrelated_results` |
| 11 | Key encoding stable + injective | `test_canonical_key_encoding_is_stable`, `…_is_injective_across_field_boundaries`, `…_field_order_is_fixed_not_dict_order` |
| 12 | No `hash()` | `test_python_hash_is_not_used_in_authoritative_modules` (AST) |
| 13 | No global `random` | `test_no_global_random_calls_in_authoritative_modules` (AST) |
| 14 | Two runs serialise identically | `test_two_complete_runs_serialise_identically`, `test_determinism_survives_a_different_process_hash_seed` (3 subprocesses) |
| 15 | Original tests present and passing | `tests/test_engine.py` — 5, unchanged |

Plus numeric-property tests: `unit_float` in range and reasonably distributed across 10 buckets;
`bounded_int` hits every value in `[0, 7)` and rejects a non-positive bound; `jitter` symmetric and
bounded.

**Full suite: 62 passed** — 5 original + 27 P0.4 + 30 P0.4A.

---

## Run metadata

`named_substreams` was **removed, not set true**. It would have been misleading: keys contain a
subsystem field, but there are no *stateful* substreams to name — nothing accumulates and nothing
advances. Replaced with fields that state what is true:

```
randomness_architecture : "keyed_counter_v1"
rng_algorithm           : "hmac-sha256-v1"
rng_algorithm_version   : "hmac-sha256-v1"
key_encoding_version    : "meridian-key-v1"
```

---

## Blockers to P0.5

1. **No cross-tier read path is defined.** A transition can write any tier; nothing reads one tier
   to compute another. P0.5 must define the channel, not just the write. *(Unchanged from P0.4.)*
2. **`represents_population` is still read by nothing** — population weighting does not affect
   aggregation. P0.5's named commitment.
3. **No decay, cost or cooldown anywhere, and no Phase 0 owner.** A causal channel feeding a
   monotonically saturating macro tier saturates faster. This is the most consequential
   unassigned gap.
4. `entities` and `relationships` remain empty — a chain through named people needs the world model.

**P0.4A is no longer a blocker.** A new conditional draw in a causal channel can now be added
without displacing anything, so a P0.5 effect is distinguishable from stream noise — which was the
precondition for building the first honest causal chain.

---

## Known limitations

- Cross-language reproducibility unverified; vectors not reproduced outside Python.
- `run_id` (`uuid4`) remains non-deterministic. It is a registry key, not authoritative state, and
  appears nowhere in `AuthoritativeState` — but it is non-determinism in the process and is
  recorded here rather than hidden.
- `bounded_int` retries at `index * 1000 + attempt`, so an index above ~9.2e15 could theoretically
  collide with another index's retry space. Unreachable in practice; noted for completeness.
- Mesa still seeds its own generator via `super().__init__(seed=…)`. Unused for authoritative
  values, but it exists — and whether mesa is retained at all is still an open owner decision.
