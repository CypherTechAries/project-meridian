# DeterministicDrawService — interface specification and isolation test plan

**Status: DRAFT.** Drafted by an AI agent, 19 July 2026. Carries no authority. Nothing here
approves a decision, closes an open question or authorises implementation.

**Nothing in this document is implemented.** No `DeterministicDrawService` exists in the codebase.
No stream key, no draw record, no isolation test and no run-metadata field described below is
present in `scaffold/`. Every statement about the service is written in the specification voice —
"would", "must", "shall" — deliberately, because a specified interface is not a delivered one. Where
this document describes the *current* engine it says so explicitly and cites `path:line`.

**Authority.** This document discharges work items 2, 3, 4 and 5 of P0.4A
(`PHASE-0-REMEDIATION-PLAN.md`:768-777), under the architecture the founder accepted on 19 July 2026
(Founder Decision 3, recorded at `docs/adr/ADR-010-deterministic-randomness-architecture.md`).
ADR-010 selected **keyed / counter-based deterministic draws** over stateful named substreams. This
document specifies the interface that decision implies. It does **not** re-open the decision, and it
does not settle the questions ADR-010 left open.

**Inputs read.** `docs/delivery/RNG-INVENTORY.md` (the enumeration of all three draw sites),
`docs/adr/ADR-010-deterministic-randomness-architecture.md`, `PHASE-0-REMEDIATION-PLAN.md` §P0.4A,
`A3-VERIFICATION-RESULTS.md`:142-175, and the source at `scaffold/backend/app/simulation/`. No file
under `scaffold/` was modified. No command was run against the simulation.

**Owner decisions this document does NOT make.** Four questions are surfaced and left open, marked
**[OWNER]** at the point they arise: the macro tier's entity identity (§2.4), whether diffusion
jitter is per-node or per-edge (§2.4), the exact versioned algorithm (§4), and the ADR-007
supersession question already recorded as `RAID-REGISTER.md` DEC8. An agent may not close any of them.

---

## 1. Plain-English layer

Today the engine keeps one bag of random numbers and every part of the simulation reaches into the
same bag in whatever order the code happens to run. There is exactly one such bag —
`self.rng = random.Random(resolved_seed)` at `scaffold/backend/app/simulation/engine.py`:83 — and
three places that reach into it. If any one of them takes one extra number, every part of the
simulation that draws afterwards gets a different number than it otherwise would. Not a wrong
number: a different one, silently, with nothing in the output to say why.

This specification replaces the bag with a **calculator**. Instead of asking "give me the next
number", code would ask "give me *the* number for this exact question" — and the question is written
out in full: which run, which rule-pack, which subsystem, which entity, what the draw is for, which
tick, and which repeat if the same question is asked more than once. The same question always yields
the same number. A different question yields an unrelated number. Crucially, asking one extra
question over here cannot change the answer to a question over there, because answers are computed
from the question rather than handed out in sequence.

Two consequences are worth stating plainly, because they are the point of the exercise:

- **Order stops mattering** where the model says it should not matter. A cohort that draws and a
  cohort that skips no longer shift anything downstream, because nothing is downstream of anything.
- **Every number becomes attributable.** Because the question is the key, a recorded draw carries
  its own explanation: this value came from *this* subsystem, about *this* entity, for *this*
  purpose, at *this* tick. That is the substrate exit criterion 9 currently lacks entirely —
  stream, index, distribution, parameters and value are all discarded at all three draw sites today
  (`PHASE-0-REMEDIATION-PLAN.md`:772-775, citing `CURRENT-STATE-AUDIT.md`:304).

The founder's governing statement, which this design exists to satisfy:

> "Materialising a background citizen must not change tomorrow's weather, market behaviour,
> government approval or another person's decision merely because it consumed extra draws."

One honest limitation, stated up front rather than buried: the property above is a property of the
*design*. Whether an implementation achieves it is decided by the tests in Part 2, not by this
document. And reproducibility across Python versions, platforms and languages is written here as a
**target with a stated verification method** (§4.4), not as a claim.

---

# PART 1 — THE INTERFACE

## 2. The key

### 2.1 Shape

A draw is identified by a **`DrawKey`**: an immutable value object with a fixed set of fields, all of
which participate in the derivation. The key is the whole of the input. No draw may depend on
generator position, call order, wall-clock time, object identity, memory address, or `hash()`.

| # | Field | Type | Required | Notes |
|---|---|---|---|---|
| 1 | `key_encoding_version` | `str` | yes | Literal, currently `"k1"`. Bumped if §3 changes in any way |
| 2 | `run_seed` | `int` | yes | The run's root seed. Today `engine.py`:81 resolves this |
| 3 | `ruleset_version` | `str` | yes | Rule-pack / scenario-schema version. No such identifier exists today — see §2.5 |
| 4 | `subsystem` | `Subsystem` | yes | Closed vocabulary, §2.2 |
| 5 | `scope_kind` | `"entity" \| "interaction" \| "subsystem"` | yes | Discriminator for field 6 |
| 6 | `scope_id` | `str` | conditional | Entity id, interaction composite, or empty when `scope_kind == "subsystem"` |
| 7 | `purpose` | `Purpose` | yes | Closed vocabulary, §2.3 |
| 8 | `context_kind` | `"tick" \| "event" \| "none"` | yes | Discriminator for field 9 |
| 9 | `context_id` | `str` | conditional | Canonical decimal tick, or event id, or empty when `"none"` |
| 10 | `draw_index` | `int` | yes | Defaults to `0`. Distinguishes repeated draws for one otherwise-identical question |

The `subsystem`/`scope`/`purpose`/`context` quartet is the five-axis isolation requirement at
`PHASE-0-REMEDIATION-PLAN.md`:700-714, with entity and interaction collapsed into one discriminated
`scope` field rather than two mutually-exclusive optional fields. The reason is encoding safety: two
optional fields admit the ambiguous state where both are populated, and an ambiguous key is a silent
reproducibility break. A discriminated union makes that state unrepresentable.

**`draw_index` is not a counter the caller increments across calls.** It is part of the question. A
rule needing three draws for one cohort at one tick asks three fully-specified questions with
indices 0, 1 and 2. It does not hold a cursor.

### 2.2 Subsystem vocabulary

`Subsystem` shall be a closed enumeration, not a free string. Free strings permit typos that produce
silently-disjoint streams. Against the current engine the initial members would be:

| Member | Wire value | Current draw site |
|---|---|---|
| `MACRO_INDICATORS` | `macro.indicators` | `engine.py`:135 |
| `MESO_COHORT` | `meso.cohort` | `cohort_agent.py`:36 |
| `DIFFUSION_NARRATIVE` | `diffusion.narrative` | `diffusion.py`:75 |
| `MICRO_INSTITUTIONAL` | `micro.institutional` | **none — this tier draws nothing today** |

`MICRO_INSTITUTIONAL` is listed because the tier exists, not because it draws. The micro tier makes
no random draw whatsoever: `InstitutionalAgent.step` resolves its action through a fixed dict lookup
on role (`llm_gateway.py`:41-51) and returns hard-coded `parameters={"intensity": 0.5}`
(`llm_gateway.py`:80-81). Registering an empty subsystem is deliberate — an empty stream is a fact
about the architecture, and reserving the name prevents a later collision.

### 2.3 Purpose vocabulary, and how a caller expresses purpose

`Purpose` shall likewise be a closed enumeration, declared per subsystem in one registry module. A
caller expresses purpose by **naming a registered constant**, never by passing a literal:

```python
service.for_subsystem(Subsystem.MESO_COHORT)          # capability handle
       .entity(cohort_id)                              # scope
       .at_tick(tick)                                  # context
       .uniform(Purpose.GRIEVANCE_DRIFT, 0.0, 0.005)   # purpose + distribution
```

Initial members, mapped from `RNG-INVENTORY.md` §6:

| Purpose | Subsystem | Replaces |
|---|---|---|
| `GRIEVANCE_DRIFT` | `MESO_COHORT` | `cohort_agent.py`:36 |
| `ADOPTION_JITTER` | `DIFFUSION_NARRATIVE` | `diffusion.py`:75 |
| `SHIPPING_THROUGHPUT_NOISE` | `MACRO_INDICATORS` | `engine.py`:135 |

The registry must enforce that a `Purpose` is used only under the `Subsystem` it is declared against.
This is the specific defence against the failure the plan names at
`PHASE-0-REMEDIATION-PLAN.md`:716-718 and which `RNG-INVENTORY.md` §6 observation 1 found live in
this scaffold: `GRIEVANCE_DRIFT` and `ADOPTION_JITTER` are both keyed to a cohort id, so per-entity
streams *alone* would place both on one stream and reintroduce exactly the order-dependence being
removed. Purpose is what separates them, and it is load-bearing rather than documentary.

### 2.4 Scope

**Entity.** `scope_id` is the entity's stable identifier — for cohorts, `cohort.cohort_id`
(`agent_schema.py`:94), which is scenario-supplied and stable. Identifiers must be stable across
runs and across processes. A Python object id, a list position, an insertion counter or anything
derived from iteration order is prohibited: it would make the key a function of order, which is the
defect being removed.

**Interaction.** For a draw about a tie rather than a node, `scope_id` is a composite of the two
participant ids:

- **Directed** (`A→B` differs from `B→A`): `escape(a) + ">" + escape(b)`.
- **Undirected** (`A–B` is one tie): `escape(lo) + "~" + escape(hi)`, where `lo` and `hi` are the two
  ids ordered by **UTF-8 byte sequence**, ascending.

The byte-order rule is not pedantry. Ordering by locale collation, by `str` comparison under an
unspecified normalisation, or by insertion order would make the key environment-dependent, and an
environment-dependent key is a reproducibility break that no same-seed test would ever catch.

> **[OWNER] Open — diffusion jitter is per-node or per-edge.** The interaction axis has no user in
> the current code; no draw today concerns an A→B tie. `RNG-INVENTORY.md` §6 records that
> `diffusion.py`:75 draws jitter **per node** while the quantity it perturbs is computed from that
> node's **edges** (`diffusion.py`:65-71), and states that whether jitter belongs per-node or
> per-edge is a modelling question P0.4A surfaces but does not own. This specification therefore
> defines the interaction encoding and leaves the diffusion mapping to the owner. §7 below shows the
> per-node form because that is what the code does today, not because it is endorsed.

**Subsystem scope.** `scope_kind == "subsystem"` with an empty `scope_id`, for draws with no entity.

> **[OWNER] Open — the macro tier has no entity identifier.** `MacroStateHolder` is a singleton
> holder (`macro_state.py`:13), deliberately not an agent (`macro_state.py`:1-5), so there is no
> stable entity id for `engine.py`:135 to key on. `RNG-INVENTORY.md` §6 observation 2 records the
> choice as an owner decision: either the macro tier acquires a stable entity identity, or the key
> scheme admits a subsystem-level stream with no entity component. This specification provides the
> *mechanism* for the second option — `scope_kind == "subsystem"` — without selecting it. If the
> owner instead gives the macro tier an identity, the mechanism is unaffected and the macro call
> sites change from `.subsystem_scope()` to `.entity(...)`.

### 2.5 Fields the scaffold cannot yet supply

Two key fields have no source in the current code and would have to be created:

- **`ruleset_version`** — no rule-pack or scenario-schema version identifier exists.
  `ACTION_EFFECTS` (`engine.py`, consumed at `_validate_and_price`, `engine.py`:121-130) is an
  unversioned module constant. Without this field, changing an effect table silently reuses old
  keys and yields identical draws for a materially different rule-set.
- **`context_id` for diffusion** — `linear_threshold_step` does **not** currently receive the tick
  (`diffusion.py`:40-46). Threading it in is a signature change, shown in §7.2.

Stating these as gaps is part of the specification. Neither is a detail that surfaces during
implementation; each is a prerequisite.

---

## 3. Canonical serialisation — the documented encoding

An underspecified key encoding is the most likely silent reproducibility break in the entire design,
because it fails without an exception: two encoders that disagree produce different numbers from
what the reader believes is the same question. This section is therefore normative and exhaustive.

### 3.1 Procedure

1. **Field order is fixed** and is exactly the numbered order of §2.1, fields 1 through 10. All ten
   fields are always emitted. Optional fields emit the empty string; they are never omitted, because
   omission would let a ten-field key and a nine-field key collide.
2. **Integers** (`run_seed`, `draw_index`, and `context_id` when `context_kind == "tick"`) are
   rendered as canonical decimal: no leading zeros (except the single digit `0`), no `+`, `-` only
   for negatives, no separators, no exponent. Non-integer types are rejected at construction.
3. **Floats are prohibited in keys**, in every field, without exception. Float formatting is not
   stable enough to key on. A rule needing a continuous quantity in its key must quantise it to an
   integer explicitly, at the call site, where the choice is visible.
4. **Strings** are Unicode-normalised to **NFC**, then encoded **UTF-8**. No case folding is
   applied — comparison is case-sensitive — because folding is locale-sensitive and can collide two
   distinct identifiers. A static check (§10, criterion 3) shall assert every vocabulary member is
   lowercase ASCII, so the question of folding never arises for enumerations; free-form entity ids
   are compared as normalised bytes.
5. **Escaping**, applied to every field's rendered value, in this order and no other:
   1. every `\` (U+005C) becomes `\\`
   2. every `|` (U+007C) becomes `\p`
   Applying the backslash rule first is required. Reversing the two produces an ambiguous encoding.
6. **Joining**: the ten escaped fields are joined with a single `|` (U+007C). No leading separator,
   no trailing separator, no whitespace, no newline.
7. The result is the **canonical key string**. Its UTF-8 bytes are the input to the derivation
   function of §4.

### 3.2 Worked example

The cohort drift draw for `coastal-creole-fishing` at tick 7, run seed 88213, rule-pack `rp-1`:

```
k1|88213|rp-1|meso.cohort|entity|coastal-creole-fishing|grievance_drift|tick|7|0
```

The macro noise draw at the same tick, under the subsystem-scope option of §2.4:

```
k1|88213|rp-1|macro.indicators|subsystem||shipping_throughput_noise|tick|7|0
```

Note the empty field between `subsystem` and `shipping_throughput_noise`: the doubled separator is
correct and required.

### 3.3 Prohibitions

| Prohibited | Reason |
|---|---|
| Python `hash()` anywhere in key construction | Process-randomised under `PYTHONHASHSEED`. Founder exit criterion 3 |
| `str()` of a container, dataclass or Pydantic model as a field | `repr` is not a stability contract |
| Any float in any field | See §3.1 rule 3 |
| Locale-dependent ordering or case operations | Environment-dependent keys |
| JSON, pickle or `repr` as the canonical encoding | Key ordering, separator and float formatting are all under-specified or version-dependent |

`hash()` has zero occurrences in `scaffold/backend/` today (`RNG-INVENTORY.md` §5), so criterion 3
currently has nothing to violate — for the simple reason that stream keys do not exist yet. The
prohibition is stated because this document is what creates the surface it could be violated on.

---

## 4. Derivation — deliberately deferred

### 4.1 What is settled and what is not

**Settled** (ADR-010, Founder Decision 3, 19 July 2026): the architecture is keyed / counter-based
deterministic draws. Ordinary sequential calls to a single shared PRNG are explicitly rejected for
authoritative behaviour.

**NOT settled here, and deferred to implementation: the exact versioned algorithm.** This document
does not select it, and no reader should treat the sketch below as a selection. The preference
recorded in ADR-010 — a counter-based or keyed-hash construction — is carried forward as a
preference.

### 4.2 The shape a candidate must have

Whatever is chosen must be a pure function of the canonical key bytes and the root seed, yielding a
fixed-width bit string, from which typed draws are derived:

```
raw_bits = F(root_seed, canonical_key_bytes) -> 256 bits (or wider)
```

Two families satisfy this: keyed cryptographic-hash constructions over the key bytes, and
counter-based generators of the Philox/Threefry family with the key bytes compressed into the key
and counter inputs. Selection criteria to be weighed at implementation: bit-exact specification
independent of any library's internals, availability in the standard library or in an already-approved
dependency (a new dependency requires human approval per `HANDOFF.md`), throughput under bulk
materialisation (§6), and the strength of its published test vectors.

### 4.3 Distribution transforms must be implemented in-repo

This constraint follows from a limitation `RNG-INVENTORY.md` §7 item 3 recorded honestly: whether
`random.Random.uniform` consumes exactly one 53-bit draw per call is CPython implementation
behaviour and was not verified. The consequence for this design is direct — **the service must not
delegate its distribution transforms to `random.Random` methods.** `uniform`, `normal`, `choice`,
`shuffle` and `sample` shall each be implemented in-repo, over raw bits, with the bit-consumption
and rejection-sampling rules written down. Delegating would inherit CPython's algorithm stability as
an unstated dependency, and CPython does not offer that as a contract.

### 4.4 Reproducibility scope — a target, with a verification method

**No claim of cross-language or cross-version reproducibility is made.** It is a target.

| Scope | Status | How it would be verified |
|---|---|---|
| Same process, same key ⇒ same value | Design intent, testable immediately | Property test over generated keys |
| Same repository, different process, same Python | Target | Golden-vector file: a committed table of key → value, asserted in CI |
| Across supported Python versions | Target | The same golden-vector file, run on each version in the CI matrix |
| Across OS / CPU architecture | Target | The same golden-vector file, on each supported platform in CI |
| Across languages | **Explicitly out of scope.** Not claimed, not targeted, not tested | — |

The golden-vector file is the mechanism for all three targets. It is a frozen artefact: changing any
value in it is a breaking change requiring a `key_encoding_version` or algorithm-version bump, and a
CI failure against it is a genuine reproducibility regression rather than a flaky test.

### 4.5 What the run records

Run metadata shall record, per run: `rng_algorithm` (name), `rng_algorithm_version`,
`key_encoding_version` (§3), `root_seed`, `ruleset_version`, and the version of the subsystem/purpose
vocabulary. There is no substrate for this today — no run records any RNG state, `getstate` and
`hashlib` both have zero occurrences across `backend/app` (`PHASE-0-REMEDIATION-PLAN.md`:776-777),
and `MacroState` carries only `seed` (`macro_schema.py`:82). This is founder exit criterion 4.

---

## 5. Service interface

### 5.1 Confinement of the root

The root seed and the derivation function shall be private to the service instance. The service is
constructed once per run. **No method on the service or on any handle it issues may return a
`random.Random`, a generator, an iterator of draws, or the root seed.** This is founder exit
criterion 2, and it is an interface property rather than a convention: if no method has such a
return type, no subsystem can obtain unrestricted access, and the static check of §10 criterion 2
becomes a signature check rather than a hunt.

### 5.2 Signatures

Written as a specification of shape. Type parameters are indicative.

```python
@dataclass(frozen=True, slots=True)
class DrawKey:
    """Immutable, fully-specified question. See §2.1. Validates on construction:
    rejects floats, rejects unregistered purpose/subsystem pairings, rejects a
    populated scope_id when scope_kind == 'subsystem'."""
    def canonical(self) -> str: ...          # §3


class DeterministicDrawService:
    def for_subsystem(self, subsystem: Subsystem) -> SubsystemHandle: ...
    def metadata(self) -> RngMetadata: ...   # §4.5; contains no seed-bearing generator


class SubsystemHandle:
    def entity(self, entity_id: str) -> ScopedHandle: ...
    def interaction(self, a: str, b: str, *, directed: bool) -> ScopedHandle: ...
    def subsystem_scope(self) -> ScopedHandle: ...


class ScopedHandle:
    def at_tick(self, tick: int) -> DrawHandle: ...
    def at_event(self, event_id: str) -> DrawHandle: ...
    def without_context(self) -> DrawHandle: ...   # explicit, never a default


class DrawHandle:
    # Continuous
    def uniform(self, purpose: Purpose, low: float, high: float, *, index: int = 0) -> float: ...
    def normal(self, purpose: Purpose, mu: float, sigma: float, *, index: int = 0) -> float: ...
    def exponential(self, purpose: Purpose, lambd: float, *, index: int = 0) -> float: ...

    # Discrete
    def integer(self, purpose: Purpose, low: int, high: int, *, index: int = 0) -> int: ...
    def bernoulli(self, purpose: Purpose, p: float, *, index: int = 0) -> bool: ...

    # Selection — all return NEW objects; none mutates its argument
    def choice(self, purpose: Purpose, population: Sequence[T], *, index: int = 0) -> T: ...
    def weighted_choice(self, purpose: Purpose, population: Sequence[T],
                        weights: Sequence[float], *, index: int = 0) -> T: ...
    def sample(self, purpose: Purpose, population: Sequence[T], k: int,
               *, index: int = 0) -> list[T]: ...
    def shuffled(self, purpose: Purpose, population: Sequence[T],
                 *, index: int = 0) -> list[T]: ...

    # Bounded bulk — §6
    def bulk(self, purpose: Purpose, count: int) -> BulkDraws: ...
```

Three deliberate choices, each with a reason:

- **`shuffled`, not `shuffle`.** It returns a new list rather than mutating in place. In-place
  mutation of a caller-owned sequence is how iteration order becomes load-bearing without anyone
  noticing, and `RNG-INVENTORY.md` §5 already records three undeclared dict-ordering assumptions in
  the current engine.
- **`without_context()` is explicit.** A context-free draw is legitimate — one-off world generation,
  for instance — but it must be stated, never reached by leaving an argument off. A defaulted context
  is how a per-tick draw silently becomes a once-per-run draw.
- **`index` is keyword-only.** It prevents a positional argument sliding into it from a signature
  change, which would silently re-key an entire subsystem's draws.

### 5.3 Recording

Every draw shall be recordable: the canonical key, the distribution name, its parameters and the
resulting value. Recording may be disabled for performance in ordinary runs but must be enabled
under test, because it is the substrate for founder exit criteria 9 and 10. Without it, criterion 10
cannot be written at all — there is nothing to compare.

---

## 6. Bounded bulk draws — the only permitted stateful path

`PHASE-0-REMEDIATION-PLAN.md` permits a stateful named substream **only** as an internal
optimisation behind the service, for bounded bulk operations. Domain code must never receive or
advance an unrestricted generator. The constraints:

1. `bulk()` returns a `BulkDraws` object, not a generator and not a `random.Random`.
2. It is **bounded at construction**: `count` is declared up front, and the object refuses draw
   `count + 1` by raising. An exhausted bulk object is an error, never a silent top-up from the root.
3. It is **keyed**: the object is derived from a `DrawKey` exactly as any other draw is, with the
   sequence position folded into `draw_index`. Draw *i* from the bulk object is bit-identical to the
   individually-keyed draw at `index = i`. This is a testable equivalence and shall be tested.
4. It is **scoped**: it may not outlive the operation it was created for, and it may not be stored on
   a domain object or returned from one.
5. It carries no cross-tick state. Two ticks are two bulk objects.

The intended use is materialising a large bounded population in one pass — the world-model case at
`PHASE-0-REMEDIATION-PLAN.md`:696-698 — where per-draw key construction would dominate cost. It is a
performance affordance with the isolation property preserved by construction, not an exception to it.

---

## 7. How a call site changes — before and after

Real examples from the current engine. The "before" blocks are the code as it stands today; the
"after" blocks are specification, and are not implemented.

### 7.1 Cohort grievance drift — the contamination vector

This is the draw whose *conditionality* causes the defect. `RNG-INVENTORY.md` §2 identifies the guard
at `cohort_agent.py`:35 as the contamination vector demonstrated in `A3-VERIFICATION-RESULTS.md`:170.

**Before** — `scaffold/backend/app/simulation/agents/cohort_agent.py`:35-38:

```python
if self.cohort.grievances:
    drift = 0.005 + self.model.rng.uniform(0.0, 0.005)
    b = self.cohort.beliefs
    b.government_competence = max(0.0, b.government_competence - drift)
```

**After** (specification):

```python
if self.cohort.grievances:
    drift = 0.005 + (
        self.model.draws
            .for_subsystem(Subsystem.MESO_COHORT)
            .entity(self.cohort.cohort_id)
            .at_tick(self.model.tick)
            .uniform(Purpose.GRIEVANCE_DRIFT, 0.0, 0.005)
    )
    b = self.cohort.beliefs
    b.government_competence = max(0.0, b.government_competence - drift)
```

**What changes, precisely.** The guard stays. The conditionality stays. What stops mattering is the
*consequence* of the conditionality: the value returned depends on `cohort_id` and `tick`, not on how
many cohorts drew before this one. Adding a grievance to `urban-professional-vantaran` — the one
cohort of five that currently has none, and the exact perturbation A3 used — would add a fifth draw
under the key `…|meso.cohort|entity|urban-professional-vantaran|grievance_drift|tick|n|0` and would
leave every other cohort's drift and the macro noise **bit-identical**. That is the specific
behaviour A3 measured as broken, where the observed movement was
`shipping_throughput_pct_of_baseline: 0.6080711379477878 -> 0.5973599412373322`
(`A3-VERIFICATION-RESULTS.md`:162).

### 7.2 Diffusion jitter — with the signature change

**Before** — `scaffold/backend/app/simulation/diffusion.py`:44 and :75:

```python
def linear_threshold_step(
    graph: nx.Graph,
    adoption: dict[str, float],
    susceptibility: dict[str, float],
    rng: random.Random,
    seed_pressure: float = 0.05,
) -> dict[str, float]:
    ...
    jitter = rng.uniform(-0.01, 0.01)
```

**After** (specification):

```python
def linear_threshold_step(
    graph: nx.Graph,
    adoption: dict[str, float],
    susceptibility: dict[str, float],
    draws: SubsystemHandle,        # DIFFUSION_NARRATIVE; no generator is passed
    tick: int,                     # NEW — the function does not receive this today
    seed_pressure: float = 0.05,
) -> dict[str, float]:
    ...
    jitter = draws.entity(node).at_tick(tick).uniform(Purpose.ADOPTION_JITTER, -0.01, 0.01)
```

Two changes beyond the draw itself. The `rng: random.Random` parameter is replaced by a capability
handle — this is founder exit criterion 2 enforced at the signature, and it also removes the
`import random` at `diffusion.py`:13, which exists solely for that type annotation. And `tick` is
threaded in, because `RNG-INVENTORY.md` §6 records that this function does not currently receive it
(`diffusion.py`:40-46) and a per-tick draw cannot be keyed without it.

A secondary effect worth noting: the loop at `diffusion.py`:64 iterates `graph.nodes` and relies on
NetworkX insertion order tracking scenario cohort order. `RNG-INVENTORY.md` §5 flags this as
load-bearing for draw order and documented nowhere. Under this design it stops being load-bearing for
*values* — each node's jitter is keyed to the node — though it remains load-bearing for the order in
which the returned dict is built, which §10 criterion 7 addresses.

### 7.3 Macro noise

**Before** — `scaffold/backend/app/simulation/engine.py`:134-136:

```python
# Small seeded macro noise, e.g. shipping variance around the crisis baseline.
noise = self.rng.uniform(-0.002, 0.002)
self.macro.apply_deltas({"shipping_throughput_pct_of_baseline": noise})
```

**After** (specification, using the subsystem-scope option pending the **[OWNER]** decision of §2.4):

```python
noise = (
    self.draws
        .for_subsystem(Subsystem.MACRO_INDICATORS)
        .subsystem_scope()
        .at_tick(self.tick)
        .uniform(Purpose.SHIPPING_THROUGHPUT_NOISE, -0.002, 0.002)
)
self.macro.apply_deltas({"shipping_throughput_pct_of_baseline": noise})
```

This is the clearest demonstrator. Today this value is "entirely determined by how many draws D1 and
D2 consumed earlier in the same tick" (`RNG-INVENTORY.md` §2, D3). Under the specification it is
determined by the root seed, the rule-pack version and the tick number, and by nothing else.

### 7.4 Construction

**Before** — `engine.py`:82-83:

```python
super().__init__(seed=resolved_seed)
self.rng = random.Random(resolved_seed)  # the ONLY source of engine randomness
```

**After** (specification):

```python
super().__init__(seed=resolved_seed)
self.draws = DeterministicDrawService(
    root_seed=resolved_seed,
    ruleset_version=scenario["ruleset_version"],   # field does not exist today — §2.5
)
# no self.rng
```

Removing `self.rng` is part of the specification, not a tidy-up. While it exists, any code can draw
from it and the static check of §10 criterion 2 cannot be made total.

**A hazard this does not fix.** `super().__init__(seed=resolved_seed)` at `engine.py`:82 constructs a
second, differently-seeded Mesa generator. `RNG-INVENTORY.md` §4 records that no application code
reads it, that it may be inert on mesa 2.4.0 because seeding happens in `Model.__new__`, and that the
inventory could not verify this because Mesa is not installed and the pin `mesa>=2.1,<3.0` is a range.
A one-character slip from `self.model.rng` to `self.model.random` would route a draw to it. Under this
specification that slip becomes *more* dangerous, not less, because `self.rng` no longer exists as the
correct-looking neighbour. The static check of §10 criterion 1 must therefore cover `.random` on Mesa
objects explicitly, and is specified to do so.

---

# PART 2 — THE ISOLATION TEST PLAN

## 8. Why the existing test cannot be cited as evidence

`test_same_seed_is_deterministic` (`scaffold/backend/tests/test_engine.py`:34-41) constructs two
models at seed 88213, runs both for 20 ticks, and asserts `a.macro_snapshot() == b.macro_snapshot()`.

It is a **same-seed repetition** test, and that shape cannot detect draw-order contamination.
Contamination does not break same-seed repetition: both runs consume the draws in the same order, so
both agree. A3 states the consequence directly — the no-substreams defect "means the existing
determinism test would mask such a change as 'expected divergence'"
(`A3-VERIFICATION-RESULTS.md`:170-175). The audit records the same blindness from the other side:
injecting global randomness into `CohortAgent.step` leaves macro equality **True** while cohort
beliefs diverge, and reversing cohort order leaves macro byte-identical while all meso output
changes — "the named guardrail test stays green through both" (`CURRENT-STATE-AUDIT.md`:140).

There is a second, narrower problem with citing it. It compares `macro_snapshot()` only. The meso
tier — where four of the ten per-tick draws land — is not compared at all.

**Consequently: passing `test_same_seed_is_deterministic` is not evidence for any of the ten criteria
below, and no record may cite it as such.** The structural difference is that criteria 5, 6, 7 and 10
are differential tests between two *different* runs.

## 9. Machinery the plan requires first

Three pieces of test infrastructure, none of which exists:

- **`DrawRecorder`** — captures `(canonical_key, distribution, parameters, value)` in issue order for
  a run. Criteria 9 and 10 are unwritable without it.
- **`StreamView`** — groups a recorder's output by key prefix (`subsystem|scope_kind|scope_id|purpose`),
  yielding a per-stream ordered sequence of `(draw_index, value)`. "Another stream is unchanged" is a
  statement about this object.
- **`FullStateDigest`** — a canonical serialisation of *all* authoritative state, macro **and** meso
  **and** micro, not `macro_snapshot()`. Every differential test below compares this. Using
  `macro_snapshot()` would reproduce the §8 blindness inside the new suite.

`FullStateDigest` has a dependency worth naming: it needs the authoritative-state contract from
**P0.4**, which is the declared prerequisite of P0.4A (`PHASE-0-REMEDIATION-PLAN.md`, Dependencies).
A digest cannot canonically serialise authoritative state before authoritative state is defined.

## 10. The ten criteria

Each entry states what it asserts, how it is constructed, what failure looks like, and whether it is
a static check or a runtime test.

### Criterion 1 — no authoritative code calls the global `random` API directly

**Type: STATIC** (lint / CI).

**Asserts.** Within the authoritative packages, there is no `from random import …`, no module-level
`random.<method>(…)` draw call, and no attribute access to `.random` on a Mesa model or agent.

**Construction.** An AST check, not a grep — a grep for `random.` matches type annotations and
comments and produces false positives that erode the check's credibility. The AST walk flags:
`ImportFrom(module='random')`; any `Call` whose function resolves to an attribute of the `random`
module other than the constructor used inside the service; and any `Attribute` access named `random`
on `self`, `self.model`, or a `mesa.Model`/`mesa.Agent`-typed name. An explicit, enumerated
allow-list names the single service-internal module permitted to import `random` at all, if the
chosen algorithm needs it.

**Failure.** A file:line list of violations. The Mesa clause is the one expected to earn its keep:
it is the check that would catch the `self.model.random` slip described in §7.4.

**Present state.** `RNG-INVENTORY.md` §4 records that the scaffold satisfies this today — `import
random` appears twice, both legitimate (`engine.py`:15, `diffusion.py`:13), with zero module-level
draw calls and zero `.random` attribute reads. The check protects a property currently held, and
§7.4 explains why the risk rises rather than falls after migration.

### Criterion 2 — no subsystem receives unrestricted access to the root generator

**Type: STATIC, with a runtime complement.**

**Asserts.** The root seed and derivation state are reachable from exactly one place, and no public
method of the service or its handles returns a generator, a `random.Random`, the root seed, or an
unbounded draw sequence.

**Construction.** *Static:* a signature check over the service's public API asserting no return
annotation is `random.Random` or a `Generator`/`Iterator` of draws, and that `BulkDraws` (§6) is the
only sequence-like return type. Plus a reference check that the root state has one construction site.
*Runtime:* a test walks the public attributes of a `SubsystemHandle` and a `DrawHandle` and asserts
none is an instance of `random.Random`; and a test asserts `BulkDraws` raises on over-draw rather than
continuing.

**Failure.** A method returning a generator, or a handle exposing a private generator through an
undunder attribute.

**Note.** This is why §5.1 is written as an interface property. A convention would need a reviewer;
a signature is decidable.

### Criterion 3 — stream keys use stable identifiers, not Python `hash()`

**Type: STATIC plus RUNTIME.** The runtime half is the stronger one.

**Asserts.** *(a)* `hash(` does not appear in key construction. *(b)* Two runs executed under
**different `PYTHONHASHSEED` values** produce identical stream keys and identical full-state digests.

**Construction.** *(a)* AST check over the key module and all call sites. *(b)* A subprocess test:
spawn the same run twice with `PYTHONHASHSEED=0` and `PYTHONHASHSEED=1` — and, since these must be
set before interpreter start, as genuine subprocesses rather than by mutating `os.environ` in-process
— then compare the serialised recorder output and the digest byte for byte. A third run under
`PYTHONHASHSEED=random` is a useful addition.

**Failure.** *(a)* is a file:line. *(b)* is a diff of two key lists, and it catches more than `hash()`
alone: it catches set iteration, and any dict keyed by an object whose `__hash__` is identity-based.

**Present state.** `hash()` has zero occurrences in `backend/` (`RNG-INVENTORY.md` §5) and stream keys
do not exist, so there is nothing to violate yet. The only set literal, `bounded` at
`macro_state.py`:30-35, is used solely for `in` membership and never iterated, so there is no current
`PYTHONHASHSEED` exposure.

### Criterion 4 — the run records RNG algorithm and version

**Type: RUNTIME.**

**Asserts.** A completed run's metadata contains a non-empty `rng_algorithm`, a non-empty
`rng_algorithm_version`, a `key_encoding_version`, and the `root_seed` — and the values are not
placeholder defaults.

**Construction.** Execute a short run; read its metadata; assert presence, non-emptiness, and
inequality against a sentinel set (`""`, `"unknown"`, `"TODO"`, `"0"`). A second assertion pins the
recorded `key_encoding_version` to the constant the encoder actually applies, so the two cannot drift.

**Failure.** Absent field, empty field, or a version string that does not track the encoder.

**Present state.** No substrate. `MacroState` carries `seed` (`macro_schema.py`:82) and nothing else;
`getstate` and `hashlib` have zero occurrences across `backend/app`
(`PHASE-0-REMEDIATION-PLAN.md`:776-777).

### Criterion 5 — adding an unrelated entity does not alter unrelated subsystem results

**Type: RUNTIME, differential.**

**Asserts.** Given run A on a scenario and run B on the same scenario plus one extra entity that no
declared causal channel connects to the subsystem under test, that subsystem's outputs and its stream
values are byte-identical between A and B.

**Construction.** Build B by adding a sixth cohort with no `bridges_to` edges to or from the existing
five, so it is isolated in the graph built at `diffusion.py`:30-36. Run both for *n* ticks with
recording on. Assert: every `MACRO_INDICATORS` stream value identical; every pre-existing cohort's
`MESO_COHORT` stream values identical; every pre-existing node's `DIFFUSION_NARRATIVE` values
identical. The new cohort's own streams are expected to exist in B and not in A — the assertion is
over the intersection, and the test must state that explicitly rather than comparing set equality.

**Failure.** Today's engine fails this on the macro assertion, and the failure is quantified: A3
recorded `shipping_throughput_pct_of_baseline` moving `0.6080711379477878 -> 0.5973599412373322` when
a cohort was added or its grievance list changed (`A3-VERIFICATION-RESULTS.md`:153-162).

**Caution — this test must be written to distinguish two cases.** After P0.5 builds real cross-tier
channels, a *connected* entity legitimately changes downstream results. The test is only meaningful
for an entity the model declares unconnected, and the declaration has to come from the P0.4/P0.5
contract, not from the test author's assumption. A test that asserts "adding any entity changes
nothing" would be asserting that the product does not work.

### Criterion 6 — promoting one background person does not alter previously established entities

**Type: RUNTIME, differential.**

**Asserts.** Control run C proceeds to tick *n* and continues to tick *m* with no promotion. Run P is
identical to tick *n*, promotes one background person, and continues to *m*. Every entity established
before *n* has identical state at *m* in both runs, unless a declared channel connects it to the
promoted person.

**Construction.** Deferred: promotion, background persons and entity materialisation do not exist.
The world model is explicitly backlogged (`HANDOFF.md`, *Backlog — captured, deliberately not
started*), and P0.4A is the gate that must pass **before** entity promotion may begin
(`PHASE-0-REMEDIATION-PLAN.md`, sequencing rule).

**Status.** Specified now, unwritable now. It must be recorded as *not yet implemented* rather than
skipped silently, and it must not be counted towards P0.4A passing. This is the criterion that
carries the founder's governing sentence about materialising a background citizen most directly, and
a green suite that quietly omits it would be exactly the class of false impression this project
exists to stop producing.

### Criterion 7 — reordering entity iteration does not alter outcomes where order is declared irrelevant

**Type: RUNTIME, differential.**

**Asserts.** For each subsystem the P0.4 contract marks order-irrelevant, reversing or shuffling
iteration order leaves the full-state digest identical.

**Construction.** Run the scenario with cohorts in file order; run again with the cohort list reversed
and once with it shuffled under a fixed permutation seed. Compare `FullStateDigest`. Subsystems
declaring order *relevant* are excluded **by name in an explicit list**, never by silence — an
exclusion list that grows without review is how this criterion becomes decorative.

**Failure.** Today's engine fails, and the audit records the shape of the failure precisely: reversing
cohort order leaves macro byte-identical while all meso output changes, and the existing guardrail
test stays green through it (`CURRENT-STATE-AUDIT.md`:140). That is also the reason this test compares
the full digest rather than `macro_snapshot()`.

**Note.** Passing requires more than keyed draws. Float addition is not associative, so an
order-dependent accumulation can still differ. `apply_deltas` (`macro_state.py`:23-47) mutates in
place and the same indicator can be written twice in one tick (`RNG-INVENTORY.md` §5). This criterion
may therefore require an accumulation-order rule — sorting deltas by key before application, or
accumulating then applying once. That is a design consequence this test would surface, and it is
noted, not resolved.

### Criterion 8 — repeating the same promotion event produces the same profile and history

**Type: RUNTIME, cross-process.**

**Asserts.** Promoting the same person from the same state twice, in two separate OS processes,
produces field-for-field identical profile and life history.

**Construction.** Cross-process, not two calls in one interpreter: the in-process version cannot catch
dependence on interpreter-global state, which is a substantial part of what it exists to catch. Each
subprocess runs to the same state, promotes, serialises the profile canonically, and the parent
compares bytes.

**Status.** Deferred with criterion 6 — promotion does not exist. Same recording rule: not implemented,
not skipped, not counted.

### Criterion 9 — every random outcome is attributable to subsystem/entity/interaction and purpose

**Type: RUNTIME, with a static complement.**

**Asserts.** Every draw in a run carries a complete, well-formed key: a registered `Subsystem`, a
`scope_kind` consistent with its `scope_id`, a `Purpose` registered against that subsystem, and a
context consistent with its `context_kind`. No draw is unattributed.

**Construction.** *Runtime:* run with recording on; enumerate every record; assert each key parses,
each field validates against the vocabulary, and no field is null or empty except where §2.1 permits.
Add an assertion that no two *distinct* draws share a canonical key — a collision means two questions
are being treated as one, and it would surface as a mysterious correlation rather than as an error.
*Static:* assert every `Purpose` member is used under exactly one `Subsystem`, and flag registered
purposes with no call site.

**Failure.** An unattributed draw, an unregistered purpose, or a key collision with its two call
sites named.

**Present state.** No substrate whatever. Stream, index, distribution, parameters and value are all
discarded at all three draw sites (`PHASE-0-REMEDIATION-PLAN.md`:772-775, citing
`CURRENT-STATE-AUDIT.md`:304).

### Criterion 10 — injecting extra draws into one stream leaves other streams unchanged

**Type: RUNTIME, differential. This is the load-bearing test.**

This is the criterion that "does not exist today in any form"
(`PHASE-0-REMEDIATION-PLAN.md`, closing line of the exit-criteria table), and it is the one that
directly encodes the founder's governing statement. It is specified concretely below.

**What it asserts.** For a control run *C* and a perturbed run *P* identical to *C* except that one
named stream *S* has *k* additional draws issued against it: every stream other than *S* has an
identical ordered sequence of `(draw_index, value)` pairs, and `FullStateDigest(P)` restricted to
state not causally downstream of *S* equals the same restriction of `FullStateDigest(C)`.

**Construction, step by step.**

1. Run *C* for *n* ticks with `DrawRecorder` enabled. Build `StreamView(C)`.
2. Run *P* identically, with one test-only injection hook active. The hook is supplied at service
   construction — it is **not** a public method on the service, because a public "consume extra
   draws" method would be an isolation hole in production code. It takes a target stream prefix, a
   tick, and *k*, and at that tick issues *k* additional draws against that stream at
   `draw_index` values beyond those the model itself uses.
3. Build `StreamView(P)`.
4. Assert `StreamView(P)[s] == StreamView(C)[s]` for every stream *s* ≠ *S*, comparing full ordered
   sequences of `(draw_index, value)` — not counts, not sums, not final values.
5. Assert `StreamView(P)[S]` equals `StreamView(C)[S]` **on the indices *C* used**. The injected
   draws occupy fresh indices; the model's own draws on *S* must be unmoved. This sub-assertion is
   the one that proves the mechanism rather than the outcome.
6. Assert the restricted full-state digests are equal.

**Choice of *S*.** The test shall be parameterised over every registered stream, not written once
against a convenient one. At minimum it must cover `meso.cohort` for a grievance-bearing cohort —
the exact vector A3 demonstrated — and `macro.indicators`.

**Why this passes by construction, and why it must still be tested.** Under a keyed design there is no
queue position to shift, so *P* and *C* agree trivially. That is the point: the test asserts the
architecture is actually keyed everywhere, not merely intended to be. Any single site that kept a
stateful generator — one surviving `self.rng`, one bulk object leaked across an operation, one draw
delegated to `random.Random` — would fail step 4 immediately.

**What failure looks like.** Under the *current* engine, failure is total and instructive: injecting
*k* draws before `engine.py`:135 changes the macro noise value at that tick and every tick after, and
step 4's diff shows the same key sequence with values offset by *k* positions. That offset signature —
identical keys, shifted values — is the visual fingerprint of shared-stream contamination, and it is
what A3 was untangling by hand at `A3-VERIFICATION-RESULTS.md`:156-168.

**Mandatory negative control.** The test suite must include a **meta-test proving this test can
fail.** It runs the criterion-10 assertions against a deliberately-shared-stream test double — an
implementation that mimics `engine.py`:83 by serving all keys from one sequential generator — and
asserts the criterion-10 test **fails** against it.

Without this, criterion 10 is unfalsifiable. A test that passes because the recorder captured nothing,
because the injection hook was silently inert, or because `StreamView` grouped everything into one
bucket would be indistinguishable from a test that passes because the architecture works. Given that
this project's defining defect is documentation claiming properties the code lacks, an
unfalsifiable test asserting the central property would be that same defect in executable form. The
negative control is not optional and must not be marked `xfail` and forgotten; it must assert the
failure actively.

## 11. Summary

| # | Criterion | Type | Writable today? |
|---|---|---|---|
| 1 | No direct global `random` | Static | Yes |
| 2 | No unrestricted root access | Static + runtime | After the service exists |
| 3 | Stable keys, not `hash()` | Static + runtime (subprocess) | After keys exist |
| 4 | Run records algorithm + version | Runtime | After metadata exists |
| 5 | Unrelated entity changes nothing | Runtime, differential | After the service exists |
| 6 | Promotion preserves established entities | Runtime, differential | **No — promotion does not exist** |
| 7 | Order-irrelevant reordering | Runtime, differential | After P0.4 declares order-relevance |
| 8 | Repeat promotion is identical | Runtime, cross-process | **No — promotion does not exist** |
| 9 | Every draw attributable | Runtime + static | After recording exists |
| 10 | **Extra draws leave other streams unchanged** | Runtime, differential | After the service exists |

**P0.4A passes only when all ten pass.** Criteria 6 and 8 are unwritable until entity promotion
exists, and promotion is itself gated behind P0.4A passing
(`PHASE-0-REMEDIATION-PLAN.md`, sequencing rule). That ordering must be resolved by the owner — either
P0.4A passes on eight criteria with 6 and 8 recorded as deferred and re-tested when promotion lands,
or promotion is admitted in a minimal test-only form to satisfy them. **This document does not choose.
[OWNER]**

## 12. Provenance

- **Read:** `docs/delivery/RNG-INVENTORY.md`; `docs/adr/ADR-010-deterministic-randomness-architecture.md`;
  `docs/delivery/PHASE-0-REMEDIATION-PLAN.md` §P0.4A; `HANDOFF.md`;
  `scaffold/backend/app/simulation/engine.py`, `agents/cohort_agent.py`, `diffusion.py`,
  `schemas/macro_schema.py`, `tests/test_engine.py`.
- **Cited, not re-verified:** `A3-VERIFICATION-RESULTS.md`:142-175 and `CURRENT-STATE-AUDIT.md`:140,
  259, 304, 319-320, carried forward as existing recorded findings.
- **Not executed.** No virtual environment exists, dependencies are not installed, and no command was
  run against the simulation. Every statement about current behaviour is read off source or carried
  from a cited record.
- **No file under `scaffold/` was modified.** No commit, push or repository change was made.
