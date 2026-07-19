# RNG inventory — every source of randomness in the scaffold

**Status: DRAFT.** Drafted by an AI agent, 19 July 2026. Carries no authority. Nothing here
approves a decision, closes an open question or authorises implementation. It is an enumeration of
what the code does today, produced as the prerequisite input to **P0.4A — establish deterministic
randomness architecture** (`PHASE-0-REMEDIATION-PLAN.md`:642).

**Method: reading only.** No code was executed and no file under `scaffold/` was modified. No
virtual environment exists and the dependencies are not installed — `python -c "import mesa"` fails
with `ModuleNotFoundError: No module named 'mesa'`. Every count and every order statement below is
derived by reading source and scenario data, not by running the engine. §7 lists what that leaves
undetermined.

Scope: all 23 Python files under `scaffold/backend/`. Draw counts are stated against the only
scenario that exists, `scaffold/scenarios/kestral-strait.json` (5 cohorts, 6 institutional agents).

---

## 1. Plain-English layer

The simulation draws all of its random numbers from one queue. There are exactly **three places in
the whole codebase that draw a random number**, and all three take from the same queue in the order
the tick loop happens to reach them.

For the one scenario that exists, a tick consumes **ten numbers** from that queue: four for cohort
grievance drift, five for narrative-diffusion jitter, one for macro shipping noise.

The four is the problem. A cohort only draws if it has at least one grievance listed in the scenario
file. One of the five cohorts has none, so it is skipped. That means **the scenario's content
decides how many numbers are consumed**, and every number drawn after that point shifts. This is
precisely the contamination A3 demonstrated: change the cohort data and the macro figures move, not
because the tiers influence one another — they do not — but because the macro draw is now taking a
different number out of a shifted queue.

Two further points worth stating plainly, because they are easy to assume the wrong way round:

- **The micro tier draws nothing at all.** The institutional agents — the ministers and commanders —
  make no random draw whatsoever. Their behaviour is a fixed lookup table in the stubbed LLM gateway:
  a given role always proposes the same action, every tick, forever. Any belief that the micro tier
  contributes variability to a run is mistaken.
- **The things people usually check for are genuinely absent.** There are no calls to the global
  `random` module, no numpy, no `hash()` in key construction, no time-based values inside the
  simulation, and no code that touches Mesa's own generator. The scaffold is clean on those counts.
  Its randomness defect is not carelessness; it is architecture — one undifferentiated stream, with
  a data-dependent consumption pattern running through it.

Two nondeterministic values do exist, both outside the simulated numbers: run identifiers are random
UUIDs, and database row timestamps are wall-clock. Neither affects a macro or meso figure today.
Both matter later, for P0.6 replay.

---

## 2. Technical-evidence layer — the three draw sites

Every draw in the codebase. All three are `uniform` calls on the single generator constructed at
`scaffold/backend/app/simulation/engine.py`:83.

| # | Site | Subsystem | Draws | Per-tick count (kestral-strait) | Data-dependent? |
|---|---|---|---|---|---|
| D1 | `app/simulation/agents/cohort_agent.py`:36 | meso / cohort | `rng.uniform(0.0, 0.005)` — additional grievance drift on top of a fixed 0.005 | **4** | **YES — critical** |
| D2 | `app/simulation/diffusion.py`:75 | diffusion / information environment | `rng.uniform(-0.01, 0.01)` — narrative-adoption jitter | **5** | **YES — by entity count** |
| D3 | `app/simulation/engine.py`:135 | macro | `rng.uniform(-0.002, 0.002)` — shipping-throughput noise | **1** | No — exactly one, unconditionally |

**Total: 10 draws per tick** for this scenario.

### The single generator

```
engine.py:83   self.rng = random.Random(resolved_seed)  # the ONLY source of engine randomness
```

Seeded from `resolved_seed = seed if seed is not None else scenario.get("default_seed", 0)`
(`engine.py`:81). The comment is accurate as to fact — it is the only generator any application code
draws from. It is also the whole of the architecture, which is the defect.

### D1 — cohort grievance drift (the contamination vector)

```
cohort_agent.py:35    if self.cohort.grievances:
cohort_agent.py:36        drift = 0.005 + self.model.rng.uniform(0.0, 0.005)
```

The guard at line 35 is the contamination vector named in the brief and demonstrated in
`A3-VERIFICATION-RESULTS.md`:170. The draw occurs **only when the cohort has a non-empty
`grievances` list**, which is scenario data (`agent_schema.py`:103, `default_factory=list`).

Against `kestral-strait.json`, in scenario list order:

| Cohort | Grievances | Draws? |
|---|---|---|
| `urban-professional-vantaran` | 0 | **no — skipped** |
| `coastal-creole-fishing` | 2 | yes |
| `inland-highland-minority` | 1 | yes |
| `military-veteran-families` | 1 | yes |
| `urban-nationalist-youth` | 2 | yes |

4 of 5 cohorts draw. Note that the *number* of grievances is irrelevant — the guard is truthiness,
so one grievance and five grievances both produce exactly one draw. What shifts the stream is
**how many cohorts have any grievance at all**. Adding a single grievance tag to
`urban-professional-vantaran` would add a fifth draw at the head of every tick and change every
subsequent number in the run, including D3's macro noise, with no causal channel involved.

### D2 — diffusion jitter

```
diffusion.py:75    jitter = rng.uniform(-0.01, 0.01)
```

Inside `for node in graph.nodes:` (`diffusion.py`:64). One draw per graph node, unconditionally —
the neighbour branch above it (`diffusion.py`:65-73) changes the *value* computed but not whether a
draw occurs. Guarded at the call site by `if not self.cohorts: return` (`engine.py`:139-140).

Node count equals cohort count: `build_cohort_graph` adds one node per cohort id
(`diffusion.py`:30-31) and adds edges only where the target id already exists in the cohort set
(`diffusion.py`:34-36), so `bridges_to` cannot introduce phantom nodes. 5 cohorts ⇒ **5 draws**.

Data-dependent in a second, weaker sense than D1: the count tracks the number of cohorts in the
scenario rather than a property of their content. Under the world model — where entities are
materialised and promoted on demand — this becomes the acute case the plan describes at
`PHASE-0-REMEDIATION-PLAN.md`:696-698.

### D3 — macro noise

```
engine.py:134    # Small seeded macro noise, e.g. shipping variance around the crisis baseline.
engine.py:135    noise = self.rng.uniform(-0.002, 0.002)
```

Exactly one draw per tick, no guard. It is therefore the clearest demonstrator of contamination: its
*value* is entirely determined by how many draws D1 and D2 consumed earlier in the same tick, and
D1's count is scenario content.

### Intra-tick draw order

`MeridianModel.step` (`engine.py`:147-180), fixed order:

1. `engine.py`:152-153 — cohort loop, list order, **D1** (conditional) — 4 draws
2. `engine.py`:156 → `_step_diffusion` → `linear_threshold_step`, graph node order, **D2** — 5 draws
3. `engine.py`:159-173 — institutional loop — **0 draws** (see §3)
4. `engine.py`:176 — `_step_macro_rules`, **D3** — 1 draw
5. `engine.py`:179-180 — snapshot, no draws

Initialisation (`engine.py`:80-116) performs **no draws**. The first draw of a run is D1 for the
first grievance-bearing cohort of tick 1.

---

## 3. Subsystems that draw nothing

Recording these is part of the inventory: an empty stream is a fact about the architecture, not an
omission.

- **Micro / institutional tier — zero draws.** `InstitutionalAgent.step` (`institutional_agent.py`:26-41)
  calls `llm_gateway.propose_action`, which resolves the action through a fixed dict lookup on the
  agent's role (`llm_gateway.py`:41-51) and returns hard-coded `parameters={"intensity": 0.5}` and
  `confidence=0.5` (`llm_gateway.py`:80-81). All six institutional agents propose the same action
  every tick for the life of the run. `_validate_and_price` (`engine.py`:121-130) then returns a copy
  of a constant table entry. This is the mechanism behind the saturation finding: a constant positive
  delta applied every tick against a clamp at `macro_state.py`:43-44.
- **Macro delta application** — `MacroStateHolder.apply_deltas` (`macro_state.py`:23-47): arithmetic
  and clamping only.
- **Persistence, API, WebSocket** — no draws (see §5 for their nondeterministic values).

---

## 4. Global `random`, numpy, and Mesa

**Global `random` module — not used for draws.** `import random` appears twice, both legitimate:
`engine.py`:15 (to construct `random.Random`) and `diffusion.py`:13 (for the `rng: random.Random`
type annotation only). There are no `random.uniform(...)`-style module-level draw calls and no
`from random import …`. P0.4A exit criterion 1 (`PHASE-0-REMEDIATION-PLAN.md`:799) is satisfied by
the code as it stands.

**numpy — absent.** `grep -rn -E "numpy|import np"` over `backend/` returns zero matches. numpy is
not in `requirements.txt`.

**networkx — present, no randomness used.** `networkx>=3.2,<4.0`. Only `Graph()`, `add_node`,
`add_edge`, `.nodes`, `.neighbors` and subscript access are called (`diffusion.py`:18-37, 64-71).
None is a randomised algorithm. It does, however, carry a dict-ordering assumption — §5.

**Mesa's own generator — untouched by application code, and I could not verify its behaviour.**

- `MeridianModel.__init__` calls `super().__init__(seed=resolved_seed)` (`engine.py`:82) before
  creating `self.rng`.
- `CohortAgent` and `InstitutionalAgent` are `mesa.Agent` subclasses calling
  `super().__init__(unique_id, model)` (`cohort_agent.py`:19, `institutional_agent.py`:22).
- **No application code reads `Model.random`, `Model.rng`, `self.random` or `self.model.random`.**
  `grep -rn -E "\.random\b|Model\.random|self\.random"` over `backend/` returns zero matches. Every
  agent-side draw goes through `self.model.rng` (`cohort_agent.py`:36) — the model's own
  `random.Random`, not Mesa's.

**Mesa is not installed and I cannot read its source, so I am not able to confirm what
`super().__init__(seed=...)` actually does.** `requirements.txt` pins `mesa>=2.1,<3.0`, a range, so
even the installed version is not determined by the repository. `CURRENT-STATE-AUDIT.md`:319 (item
27) records that on mesa 2.4.0 the call is inert because seeding happens in `Model.__new__`, and that
on the API path Mesa's `self.random` is therefore seeded from entropy. **I could not verify that
claim** and am carrying it forward as an existing recorded finding, not as something re-established
here. What I can establish by reading the scaffold alone: a second generator is constructed, nothing
in the scaffold reads it, and a one-character slip from `self.model.rng` to `self.model.random` would
route a draw to it. Whether that would be seeded or entropy-seeded is the unverified part.

---

## 5. Implicit nondeterminism

**`hash()` — zero occurrences.** No `hash(`, no `hashlib`, no `getstate`/`setstate` anywhere in
`backend/`. Stream keys do not exist yet, so criterion 3 has nothing to violate; it also means no run
records any RNG state (criterion 4 has no substrate — `PHASE-0-REMEDIATION-PLAN.md`:802).

**Dict-ordering assumptions — three, all currently safe, none declared.**

| Site | Assumption | Assessment |
|---|---|---|
| `diffusion.py`:64 | `for node in graph.nodes` follows insertion order, which follows the `cohesion` dict comprehension (`diffusion.py`:25-29), which follows scenario cohort list order | Holds on CPython 3.7+. **This is load-bearing for D2's draw order and is documented nowhere.** It is an implementation guarantee being relied on as a model contract |
| `engine.py`:152 | `self.cohorts` list order = scenario order | Genuinely a list; safe. Fixes D1's order |
| `macro_state.py`:36 | `for key, delta in deltas.items()` | Safe — distinct keys, independent additions, no draw |

**Set iteration — none.** The only set literal is `bounded` (`macro_state.py`:30-35), used solely for
`in` membership (`macro_state.py`:43). Never iterated, so no PYTHONHASHSEED exposure.

**Time-based values — one, outside the simulation.** `_utcnow()` (`db/models.py`:19-20) as the
`created_at` default (`db/models.py`:31). Wall-clock, non-reproducible. It never reaches a simulated
number, and per `ARCHITECTURE_DECISIONS.md`'s 19 July P0.1 amendment nothing is written to a database
at all, so it is presently inert.

**Random identifiers — one, outside the simulation.** `uuid.uuid4().hex` (`api/runs.py`:33) as the
run id. Genuinely nondeterministic (UUID4 draws from the OS CSPRNG, not from `self.rng`). It does not
enter any macro or meso figure. It does mean **two identical-seed runs are not identifiable as such
from their identifiers**, which is a P0.6 replay concern, not a P0.4A one. Event ids are derived and
deterministic: `f"evt-{self.tick}-{inst.spec.agent_id}"` (`engine.py`:167).

**Concurrency / interleaving — one hazard.** `routes_ws.py`:42 calls `model.step()` inside an async
handler on the shared `_RUNS` object (`api/runs.py`:18). Two WebSocket clients attached to one run id
would interleave `step()` calls against one generator. No lock exists. This introduces no new
randomness *source*, but it makes draw **order** dependent on connection scheduling. Not verifiable
without executing the server; recorded as a hazard, not a demonstrated defect.

**Float accumulation.** `apply_deltas` mutates in place and the same indicator can be written twice in
one tick (once by an institutional action, once by D3 at `engine.py`:176). Sum order is fixed by the
loop order above, so it is reproducible — but it is reproducible *because* of the iteration order,
which is the same undeclared dependency as everything else here.

---

## 6. Mapping to the founder's five-axis key shape

> **Superseded in part — see §9 (Amendment 1, 19 July 2026).** The governance statements in the
> paragraph immediately below — that ADR-010 is Proposed, that its approval block is empty, and that
> the substream-versus-keyed choice is unmade — were true when this section was drafted and are no
> longer true. The accepted key shape has **seven** fields, not five. The per-draw mapping in the
> table is unaffected and stands. The original text is retained unchanged below.

Against the axes at `PHASE-0-REMEDIATION-PLAN.md`:708-714. **This is a drafter's mapping offered as
input to P0.4A's work item 2, not a specification.** ADR-010 is Proposed only, its approval block is
empty, and the choice between stateful named substreams and keyed/counter-based draws is unmade
(`PHASE-0-REMEDIATION-PLAN.md`:737-744). The identifiers below are the ones the *existing* code
already has to hand; a key scheme may well require identifiers the scaffold does not yet possess.

| Axis | D1 `cohort_agent.py`:36 | D2 `diffusion.py`:75 | D3 `engine.py`:135 |
|---|---|---|---|
| Subsystem | `meso.cohort` | `diffusion.narrative` | `macro.indicators` |
| Entity | `self.cohort.cohort_id` — stable, from scenario (`agent_schema.py`:94) | `node` — the cohort id | **none exists.** Macro state is a singleton holder (`macro_state.py`:13) with no entity identifier; `scenario_id` is the nearest available |
| Relationship / interaction | not applicable — drift is intrinsic to the cohort | **unused, and arguably wrong.** The jitter is drawn per *node* though the quantity it perturbs is computed from the node's *edges* (`diffusion.py`:65-71). Whether jitter belongs per-node or per-edge is a modelling question P0.4A surfaces but does not own | not applicable |
| Purpose | `grievance_drift` | `adoption_jitter` | `shipping_throughput_noise` |
| Tick / event | `self.model.tick` (`engine.py`:88) | `model.tick`, passed implicitly — `linear_threshold_step` does **not currently receive the tick** (`diffusion.py`:40-46) and would need it added | `self.tick` |

Three observations that fall out of the mapping:

1. **D1 and D2 key identically on subsystem-and-entity but differ on purpose.** Both are keyed to a
   cohort id. Per-entity streams alone would place both draws on one stream and reintroduce exactly
   the order-dependence being removed — the failure mode the plan warns against at
   `PHASE-0-REMEDIATION-PLAN.md`:716-718. This scaffold contains a live instance of it.
2. **D3 has no entity identifier to key on.** The macro tier is a plain holder object, deliberately
   not an agent (`macro_state.py`:1-5). Either the macro tier acquires a stable entity identity, or
   the key scheme admits a subsystem-level stream with no entity component. That is an owner
   decision, and nothing here settles it.
3. **The interaction axis has no user in the current code.** No draw today concerns an A→B tie.
   Relationship schemas exist (`agent_schema.py`:190-200) but nothing draws against them.

The four candidate keys P0.4A would need to define, then, are three occupied and one empty:
`meso.cohort/<cohort_id>/grievance_drift/<tick>`, `diffusion.narrative/<cohort_id>/adoption_jitter/<tick>`,
`macro.indicators/<?>/shipping_throughput_noise/<tick>`, and the presently unused interaction axis.

---

## 7. What I could not determine

Stated explicitly, per the standing two-layer requirement.

1. **Anything requiring execution.** No venv, dependencies not installed. Every count in §2 is read
   off source and scenario JSON. I have not observed a single actual draw, verified the total of ten
   per tick empirically, or reproduced A3's demonstration.
2. **Mesa's behaviour.** Not installed, source unreadable, version pinned only as a range. The
   `super().__init__(seed=...)` question in §4 rests on `CURRENT-STATE-AUDIT.md`:319, which I carried
   forward rather than verified.
3. **Whether `random.Random.uniform` consumes exactly one 53-bit draw per call.** It is CPython
   implementation behaviour, and unverified here. It matters for any counter-based scheme, where the
   mapping from call to counter position must be exact.
4. **The WebSocket interleaving hazard** (§5) — reasoned from source, not demonstrated.
5. **Whether other scenarios exist or are planned.** Counts are for `kestral-strait.json`, the only
   file in `scaffold/scenarios/`. Every per-tick figure here changes with scenario content — which
   is the point of the inventory.

---

## 8. Provenance

- Read: all 23 `.py` files under `scaffold/backend/`, `scaffold/backend/requirements.txt`,
  `scaffold/scenarios/kestral-strait.json`, `scaffold/CLAUDE.md`.
- Consulted: `PHASE-0-REMEDIATION-PLAN.md` §P0.4A, `A3-VERIFICATION-RESULTS.md`:156-180,
  `CURRENT-STATE-AUDIT.md` items 17/27/28 (via the plan's citations),
  `scaffold/docs/ARCHITECTURE_DECISIONS.md` ADR-007 and its 19 July amendment.
- Verification greps run over `scaffold/backend/`, all returning zero matches:
  `\.random\b|Model\.random|self\.random` · `hashlib|getstate|setstate|hash\(` · `numpy|import np`.
- No file under `scaffold/` was modified. No command was run against the simulation.

---

## 9. Amendment 1 — 19 July 2026

**Status: DRAFT.** Drafted by an AI agent. Carries no authority and settles nothing. This amendment
corrects §6 only. **No enumeration in §§1-5 changed.** The three draw sites, the ten-draws-per-tick
count, the data-dependence findings and the implicit-nondeterminism findings were re-derived
independently by reading the same 23 files and agree with the original in every particular. Nothing
in §§1-5, §7 or §8 is withdrawn.

### 9.1 Plain English

Section 6 was written while the architecture decision was still a proposal. The founder has since
accepted it. Two things therefore need correcting: the decision is no longer open, and the shape of
the key is longer than §6 assumed — seven parts rather than five. The extra two parts at the front
identify *which run and which version of the rules* produced a number, and the extra one at the back
counts repeat draws. None of that changes what the code does. It changes what the eventual key for
each of the three draws has to contain.

### 9.2 What changed

| §6 statement | Status now | Evidence |
|---|---|---|
| "ADR-010 is Proposed only" | **Superseded.** Status is **Accepted**, by the founder, 19 July 2026 (Founder Decision 3) | `docs/adr/ADR-010-deterministic-randomness-architecture.md`:35-38 |
| "its approval block is empty" | **Superseded.** "Drafted by: an AI agent. **Accepted by:** the founder." | ADR-010:39 |
| "the choice between stateful named substreams and keyed/counter-based draws is unmade" | **Superseded.** Keyed / counter-based selected; sequential shared-PRNG use explicitly rejected for authoritative behaviour; stateful substreams permitted only as a private optimisation inside the service, never handed to domain code | ADR-010:204-215, :226-237, :275-282 |
| "five-axis key shape" | **Incomplete, not wrong.** The five axes at `PHASE-0-REMEDIATION-PLAN.md`:708-714 are all present in the accepted shape; the accepted shape adds two more fields | ADR-010:243-253 |

The accepted shape, reproduced from ADR-010:245-253:

```
root seed + ruleset version + subsystem + entity or interaction identifier
          + purpose identifier + tick or event identifier + draw index
```

Field order is fixed and versioned, every field is always present (an inapplicable field takes an
explicit empty marker rather than being omitted), and `hash()` is prohibited in key construction
(ADR-010:255-273, :232).

### 9.3 The two front fields — what the scaffold has to hand

Neither was covered by §6's table. Both are read off existing code.

| Field | Nearest existing value | Assessment |
|---|---|---|
| Root seed | `self.seed` (`engine.py`:87), mirrored to `MacroState.seed` (`engine.py`:92) and surfaced by the API (`routes_simulation.py`:32) | **Available.** Resolved once at `engine.py`:81 from the request or `default_seed` (`kestral-strait.json`, 88213). No further work to identify it |
| Ruleset version | **None exists.** The nearest thing in the tree is the free-text string `derivation="rules_engine_v1 + seed_init"` (`engine.py`:68), which is set once at construction, never updated, and read by no code | **Absent.** `ACTION_EFFECTS` (`engine.py`:35-43) carries no version; the scenario file carries no version key (its top-level keys are `scenario_id`, `title`, `archetype`, `government_structure`, `default_seed`, `fiction_disclaimer`, `initial_macro_state`, `cohorts`, `institutional_agents`, `hidden_campaign`, `win_conditions`). A ruleset-version identifier would have to be introduced. That is an owner decision and is not taken here |

### 9.4 The draw index — currently always zero

ADR-010:252 requires the draw index explicitly "wherever a purpose draws more than once".

**No purpose in the current code draws more than once per key.** Each of D1, D2 and D3 makes exactly
one `uniform` call per (subsystem, entity, purpose, tick) tuple: D1 once per grievance-bearing cohort
per tick (`cohort_agent.py`:36, inside no inner loop), D2 once per graph node per tick
(`diffusion.py`:75, one call in the body of the node loop at `diffusion.py`:64), D3 once per tick
(`engine.py`:135, unguarded and unlooped).

Two consequences worth recording, neither of which relaxes the requirement:

1. The draw index would be a constant `0` at all three sites on day one. The field is still mandatory
   under the presence rule (ADR-010:261-263) — omitting it because it is currently constant is
   exactly the collapse-into-the-same-byte-string failure that rule exists to prevent.
2. **The scaffold therefore offers no test case for the field that is most likely to be got wrong.**
   Multi-draw purposes are what the index exists for, and none exists to check an implementation
   against. Any test vectors published under ADR-010:235 would need a synthetic multi-draw purpose;
   the existing three sites cannot exercise it.

### 9.5 What this amendment does not do

- It does not re-open ADR-010, and does not touch the ADR-007 supersession question, which remains
  the owner's (`PHASE-0-REMEDIATION-PLAN.md`:744-748, open question 15, `RAID-REGISTER.md` DEC8).
- It does not resolve §6's observation 2 — the macro tier still has no entity identifier to key on
  (`macro_state.py`:13). That remains open and is marked **[OWNER]** in
  `DETERMINISTIC-DRAW-SERVICE.md` §2.4.
- It does not revisit the per-node-versus-per-edge diffusion question (§6, relationship axis).
- **It was produced by reading only.** No venv exists, dependencies are not installed
  (`python -c "import mesa"` → `ModuleNotFoundError: No module named 'mesa'`), no file under
  `scaffold/` was modified, and nothing was executed. Every limitation in §7 continues to apply
  unchanged, including the unverified Mesa behaviour and the unverified assumption that
  `random.Random.uniform` consumes exactly one draw per call — which §9.4's index reasoning does not
  depend on, since it counts *calls*, not underlying draws.
