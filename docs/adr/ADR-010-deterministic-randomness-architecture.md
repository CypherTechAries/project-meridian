# ADR-010 — Deterministic randomness architecture

> **The architecture below is now decided. Nothing in it is implemented.**
> The founder accepted the architecture on 19 July 2026 (Founder Decision 3). No code exists for
> anything described below. Every sentence about the accepted architecture is written in the
> conditional or the future tense deliberately, because acceptance of a design is not delivery of
> one. Where this document describes the *current* system it says so explicitly and cites
> `path:line`.
>
> **Amendment history.** This ADR was drafted on 19 July 2026 with status *Proposed*. On the same
> date the founder accepted it, and the Decision section, the status line, the Approval block and
> open question 1 were amended accordingly. The comparison of the two candidate architectures, the
> ten exit criteria and all consequences — including the negative ones — are carried forward
> unchanged; the decision was added, not substituted for the record of how it was reached.

**Where this file sits, and an open question about that.** The project's existing ADR log is a
single flat file at [`scaffold/docs/ARCHITECTURE_DECISIONS.md`](../../scaffold/docs/ARCHITECTURE_DECISIONS.md),
holding ADR-001 to ADR-009. This ADR is written to `docs/adr/` and continues that numbering at 010,
per [`ADR-TEMPLATE.md`](../delivery/ADR-TEMPLATE.md) §1.6. **Whether ADR-010 is eventually
consolidated into `scaffold/docs/ARCHITECTURE_DECISIONS.md`, or whether `docs/adr/` becomes the
permanent home, is OPEN QUESTION 2 of the template and is the owner's to decide. It is not decided
here.** This run did not edit `scaffold/docs/ARCHITECTURE_DECISIONS.md`; Phase C owns that file.

**Authority for this ADR's existence.** The founder instruction of 18 July 2026 (Decision 1)
creates P0.4A as a Phase 0 workstream in its own right, positioned between P0.4 and P0.5, and
requires that an ADR select an approach deliberately and explicitly reject ordinary sequential
calls to a single shared PRNG for authoritative behaviour. This document discharged the drafting
half of that requirement. **The selecting half was the owner's, and the owner has now performed it:
Founder Decision 3, 19 July 2026, selects the keyed / counter-based architecture.**

---

## ADR-010 — Deterministic randomness architecture: isolate every authoritative random draw by subsystem, entity, interaction, purpose and context

**Status:** **Accepted** — architecture selected by the founder on 19 July 2026 (Founder Decision 3).
Accepted as the architecture for P0.4A. **Not implemented.** No code, test or schema exists for any
of it, and acceptance does not by itself authorise a dependency, a schema change or a commit.
**Date:** 19 July 2026 (drafted); **accepted** 19 July 2026
**Drafted by:** an AI agent. **Accepted by:** the founder.
**Supersedes:** None. **Relates to** ADR-007 (`scaffold/docs/ARCHITECTURE_DECISIONS.md:60-67`),
which this ADR would narrow rather than supersede — see *Relationship to ADR-007* below.

---

### Context

#### Plain English

MERIDIAN draws random numbers to decide small uncertain things: how fast a cohort loses faith in
its government, how far a narrative spreads, how much a shipping indicator wobbles this tick. Today
every one of those draws comes out of a single queue. The first thing that asks gets the first
number, the second thing gets the second number, and so on.

That works only for as long as nothing changes how many times anything asks. The moment one part of
the simulation asks for one extra number — because a scenario gained a cohort, because a background
person was promoted into a detailed individual, because someone refactored a loop — every later part
of the simulation receives a *different* number than it would have. Not a wrong number. A different
one, silently, with nothing in the output to indicate why.

This has already happened here and has been measured. It is not a theoretical hazard.

The founder's statement of the requirement is the governing one:

> "Materialising a background citizen must not change tomorrow's weather, market behaviour,
> government approval or another person's decision merely because it consumed extra draws."

That property does not hold today and cannot be made to hold by tuning, testing or discipline. It
requires an architectural decision about where random numbers come from, which is what this ADR is
for.

#### The evidence

There is exactly one `random.Random` created in application code
(`scaffold/backend/app/simulation/engine.py:83`, commented in source as "the ONLY source of engine
randomness"), and three sites consume it:

| Draw site | What it decides |
|---|---|
| `scaffold/backend/app/simulation/agents/cohort_agent.py:36` | per-cohort belief drift, **only if that cohort has a non-empty grievance list** (`cohort_agent.py:35`) |
| `scaffold/backend/app/simulation/diffusion.py:75` | per-node jitter in narrative diffusion |
| `scaffold/backend/app/simulation/engine.py:135` | macro noise on `shipping_throughput_pct_of_baseline` |

The exhaustiveness of that list rests on a search, not on the three positive citations. The command
a reader can run to check it:

```
grep -rn "random\.Random(\|\.rng\." scaffold/backend/app
```

A3 demonstrated the consequence by execution, not inspection
(`docs/delivery/A3-VERIFICATION-RESULTS.md:142-175`; script `docs/delivery/evidence/a3_rng_isolation.py`).
Perturbing a cohort's *values* by two orders of magnitude changed macro output by **exactly nothing**
(`A3-VERIFICATION-RESULTS.md:152`). But **adding a grievance to the one cohort that had none**
changed macro output (`:153`), and **deleting a cohort entirely** changed macro output (`:154`).

The observed movement:

```
shipping_throughput_pct_of_baseline: 0.6080711379477878 -> 0.5973599412373322
```

(`A3-VERIFICATION-RESULTS.md:162`)

The mechanism is stated at `A3-VERIFICATION-RESULTS.md:156-168`. `cohort_agent.step()` draws only
if the cohort has grievances (`cohort_agent.py:35`). Changing how many cohorts have grievances
changes how many draws are consumed per tick, which shifts every later draw in the shared stream,
which changes the macro noise value at `engine.py:135`.

**This matters more than a number moving.** The apparent meso→macro coupling that this produces is
**contamination, not causality**. A3's corrected statement is explicit: "Macro→meso is dead.
Meso→macro is also dead; the apparent influence is an artefact of a single shared RNG stream, not a
causal channel" (`A3-VERIFICATION-RESULTS.md:167-168`). A reader watching a demo would see cohort
grievance move a national indicator and reasonably conclude the tiers are wired together. They are
not. That is precisely the class of false impression this project exists to stop producing.

A3 recorded the underlying defect as new and not previously in the audit
(`A3-VERIFICATION-RESULTS.md:170-175`): "There are no named RNG substreams. Adding or removing a
single random draw in one subsystem silently changes every subsequent draw in every other
subsystem." The broad audit had recorded the same structural fact more mildly as informational item
28 — "One shared RNG stream, no named substreams … Not currently a defect (the design is documented
as one RNG in ADR-007) but it means seeds are not comparable across code versions or scenario
variants" (`docs/delivery/CURRENT-STATE-AUDIT.md:320`). A3's execution is what moved it from
"informational" to "demonstrated reproducibility hazard".

#### Why the current determinism test does not catch this

`test_same_seed_is_deterministic` (`scaffold/backend/tests/test_engine.py:34-40`) constructs two
models at seed 88213, runs each 20 ticks, and asserts the final macro snapshots are equal. It is a
**same-seed repetition test**. It answers "does this build reproduce itself?" and nothing else.

It cannot detect draw-order contamination, and the reason is structural rather than a matter of
coverage. Contamination shows up as *divergence between two different configurations* — a scenario
with an extra cohort versus one without, a build before a refactor versus after. The test compares
two runs of the **same** configuration, which agree in both the contaminated and the uncontaminated
world. Its sibling `test_different_seed_diverges` (`test_engine.py:43-49`) asserts that different
configurations *do* differ, which if anything encodes divergence-under-change as the expected
outcome.

So the suite would accept draw-order contamination as ordinary divergence. A3 states this directly:
"the existing determinism test would mask such a change as 'expected divergence'"
(`A3-VERIFICATION-RESULTS.md:174-175`). **P0.4A therefore requires isolation tests, not merely
same-seed repetition tests.** Isolation tests are the ones described in exit criteria 5 to 10 below,
and they are a different shape: they hold one thing constant and perturb another, then assert the
constant thing did not move.

The two tests also inspect only the final macro snapshot and no meso state at all
(`test_engine.py:36-40`; audit finding 5.3 at `CURRENT-STATE-AUDIT.md:136`), so per-cohort belief
and narrative adoption are unguarded by anything today.

#### Why this cannot wait, and why it is not part of the world model

Two forces make this a Phase 0 item rather than a later tidy-up.

**The world model would make it much worse.** The founder requirement of 18 July 2026 specifies
fidelity tiers and tier promotion: "A background person may become important … At that point, the
system can deterministically expand them into a more detailed individual" and "Once materialised,
their identity and history must remain stable"
(`docs/world-model/FOUNDER-REQUIREMENT-2026-07-18.md:230-237`). Under a single shared stream,
materialising one background citizen consumes an unbounded number of extra draws at an arbitrary
point in the tick, which under the mechanism demonstrated above would move every unrelated
subsequent outcome in the run. The requirement of stable materialised identity and the current RNG
design are not merely in tension; they are incompatible.

**It is not a world-model detail and must not hide inside replay.** Founder Decision 1 places it as
its own workstream, P0.4A, between P0.4 (define authoritative state) and P0.5 (cross-tier causal
channels), and ahead of P0.6 (events, snapshots and replay). Replay would *record* the contaminated
values faithfully; it would not make them isolated, and burying the problem there would leave the
architecture unfixed behind a mechanism that appears to solve it.

#### Relationship to ADR-007

ADR-007 (`scaffold/docs/ARCHITECTURE_DECISIONS.md:60-67`) records the decision that every run has
one seed threaded into `MeridianModel.__init__` → `self.rng`, and that "All engine, agent, and
diffusion randomness draws from that one RNG — never the global `random` or unseeded `numpy`."

**The part of ADR-007 that this ADR keeps** is the prohibition: no global `random`, no unseeded
`numpy`, one root of seeded entropy per run. That prohibition is correct and this ADR strengthens it
into testable exit criteria 1 and 2.

**The part this ADR would narrow** is "that one RNG" read as *one sequential stream shared by all
consumers*. This ADR proposes that the run keeps a single root seed but that no subsystem consumes
the root generator directly.

ADR-007 also states that the property is "proven by `test_same_seed_is_deterministic`"
(`:65`). Per the analysis above, that test proves same-seed repetition and does not prove isolation.
Whether ADR-007 is corrected in place, superseded, or left as historical record is **not decided
here** — it is open question 3 of `ADR-TEMPLATE.md` §4, it concerns a file this run must not edit,
and Phase C owns the ADR log.

---

### Decision

**Decided by the founder on 19 July 2026.** This ADR was drafted as a recommendation; an AI agent
may draft such a record but may not approve it (`HANDOFF.md` § Standing constraints (`:138`); `ADR-TEMPLATE.md` §1.5). The
founder instruction of 18 July 2026 required that the ADR "must select one deliberately". Founder
Decision 3 performs that selection.

The decision, as adopted:

> MERIDIAN adopts **keyed / counter-based deterministic randomness** (Alternative B) as its
> primary authoritative randomness architecture. Every authoritative random value is derived as a
> pure function of a run-level root seed and an explicit, stable **draw key** naming the subsystem,
> the entity or interaction, the simulation purpose, and the tick or event context, with an
> explicit draw index where a purpose requires repeated draws. **Ordinary sequential calls to a
> single shared PRNG are rejected for authoritative behaviour.** Authoritative code obtains draws
> from a central **`DeterministicDrawService`**, never from a raw generator: no authoritative code
> holds, is handed, or advances a generator, and the root seed is never consumed directly by a
> subsystem. Direct calls to the global `random` API are prohibited in authoritative code. Draw
> keys are built from stable canonical domain identifiers under a documented canonical encoding,
> and never from Python's `hash()`, which is process-randomised and therefore unusable for stable
> keys. Each run records the derivation algorithm and its version alongside the seed. Deterministic
> test vectors are published with the implementation. The architecture must make it structurally
> impossible for an unrelated added draw to shift an unrelated outcome, and impossible for entity
> promotion to alter unrelated entities or macro state.

**Decided?** Yes — the architecture. **Built?** No. This is *accepted; not implemented as of 19 July
2026.* No code, test or schema exists for any of it, and no claim about the running system may be
made on the strength of this acceptance.

#### What the accepted design must satisfy

These are properties of the accepted architecture, not descriptions of anything that runs. Each is
carried into the ten exit criteria in *Verification*, which remain the definition of P0.4A done.

1. One shared sequential PRNG is rejected for authoritative behaviour. The prohibition inherited
   from ADR-007 — no global `random`, no unseeded `numpy` — is kept and strengthened.
2. Authoritative code calls a central `DeterministicDrawService`. It receives values, not
   generators.
3. Draws are derived from stable canonical keys, deterministically and without hidden state.
4. Keys isolate subsystem, entity, interaction, purpose, and the relevant tick or event context.
5. Python `hash()` is prohibited anywhere in key construction.
6. Direct global `random` calls are prohibited in authoritative code.
7. The run record carries the derivation algorithm identifier and its version.
8. Deterministic test vectors exist and are checked in CI.
9. Adding an unrelated draw cannot shift an unrelated outcome.
10. Entity promotion cannot alter unrelated entities or macro state.
11. Reproducibility across supported environments is a **target** with a stated verification
    method — see *Reproducibility is a target, not a claim* below.

#### Key shape and canonical encoding

The founder-specified key shape is:

```
root seed
  + ruleset version
  + subsystem
  + entity or interaction identifier
  + purpose identifier
  + tick or event identifier
  + draw index          (explicit, required wherever a purpose draws more than once)
```

**The encoding must be documented precisely, because an underspecified key encoding is the most
likely source of a silent reproducibility break.** The implementation plan must therefore specify,
and its documentation must state, at least:

- **Field order** — fixed, in the order above, and never reordered once published; the order is part
  of the versioned derivation, so changing it is an algorithm-version change.
- **Field presence** — every field is always present. An inapplicable field takes an explicit
  documented empty marker rather than being omitted, so that two different keys can never collapse
  into the same byte string by omission.
- **Normalisation** — for each field: its type, its text form, its case treatment, its Unicode
  normalisation form, and the byte encoding used (a single documented encoding, applied uniformly).
  Numeric fields state their integer form and width; no locale-dependent or platform-dependent
  formatting is permitted anywhere in a key.
- **Separator and escaping** — a single documented separator, with a documented escaping rule that
  makes the encoding injective: it must be impossible for two distinct field tuples to produce the
  same serialised key. The plan must state the escaping rule and show why it is unambiguous, not
  merely assert that a separator is "unlikely" to appear in a field.
- **Versioning** — the encoding itself carries a version, recorded in run metadata alongside the
  algorithm version, so that a future encoding change is visible in the record rather than silent.

#### Stateful substreams — a constraint on implementation, not a second architecture

A named stateful substream **may exist only as an internal optimisation inside the
`DeterministicDrawService`**, for bounded bulk operations where deriving each value independently is
demonstrably wasteful. It is a private implementation detail with no standing as an architecture.

The constraint that follows is absolute: **domain code must never receive or advance an
unrestricted generator.** No substream object may cross the service boundary. Any such optimisation
must be bounded, must be keyed and reproducible on its own terms, and must produce exactly the
values the pure keyed derivation would produce for the same keys — verified by test vectors, not
assumed. Alternative A is **not** adopted; this clause does not readmit it.

#### Algorithm selection is deferred

**The specific derivation algorithm is not settled by this ADR.** It is deferred to the
implementation plan, which must select and document one exact, versioned algorithm. The preference
recorded here is a counter-based or keyed-hash construction with stable test vectors that a reader
can check by hand. Adding or changing a dependency to obtain it remains an ADR-triggering decision
in its own right (`ADR-TEMPLATE.md` §1.2).

#### Reproducibility is a target, not a claim

**No cross-language, cross-platform or cross-version reproducibility property may be claimed until
it is measured.** Nothing has been measured. The target is that the same run seed, ruleset version,
scenario and key set produce identical authoritative values across the supported environments. The
verification method is stated so the target is falsifiable: the implementation plan publishes a
fixed set of deterministic test vectors — key tuples and their expected derived values — and CI
executes them on each supported environment, with any additional language or runtime required to
demonstrate its agreement with the same vectors before any statement about it is written down.
Until those vectors run green on a given environment, that environment is unverified and must be
described as such. This ADR licenses no new claim about the current system, whose permitted wording
remains exactly as fixed in `HANDOFF.md:52-62` and reproduced in *Determinism impact* below.

**Scope limit.** This ADR governs **authoritative** randomness — any draw whose value can reach
authoritative state, an event record, a snapshot, or a player-visible outcome. It deliberately does
not govern non-authoritative randomness such as UI-only presentation jitter, test fixture
generation, or sampling inside developer tooling. Whether a given draw is authoritative is decided
by whether its value can influence recorded state, not by which module it lives in. Where the
boundary is unclear, the draw is authoritative until the owner rules otherwise.

**Sequencing that this decision sits inside** (Founder Decision 1 and 3, carried here so the
constraint travels with the ADR):

```
P0.1 truthful claims
  → P0.2 reproducible installation
  → P0.3 honest CI
  → P0.4 authoritative state
  → P0.4A deterministic randomness      ← this ADR
  → P0.5 cross-tier causality
  → P0.6 events, snapshots and replay
```

P0.5 **specification** may proceed in parallel now. **Neither P0.5 implementation, nor entity
promotion, nor world-model materialisation may proceed until P0.4A passes.**

---

### Alternatives considered

Both live candidates are presented in full before the comparison, because the founder instruction
requires that at least two valid approaches be considered seriously and the "Why rejected" column
alone cannot carry that. **This section is retained unchanged after acceptance.** The record of why
Alternative A was not chosen is the substance of an ADR, and Alternative A's genuine strengths are
left standing rather than trimmed to flatter the decision.

#### Alternative A — stateful named substreams — *considered, not adopted*

The run holds a registry of named generators. A caller asks for the generator belonging to a key —
`("cohort_belief_drift", "coastal-creole-fishing")` — and receives a `random.Random`-like object
seeded deterministically from the root seed and that key. Each generator advances its own internal
position as it is used.

*How it behaves.* Draws in one named stream do not disturb another, so the headline defect is
closed. It is close to the existing mental model: callers still hold something that looks like
`self.rng` and call `.uniform()` on it, so the call sites at `cohort_agent.py:36`,
`diffusion.py:75` and `engine.py:135` change shape only modestly.

*Where it strains.* Each stream carries mutable position state, which becomes part of what must be
snapshotted if replay or mid-run fork is ever to work — and the audit already records that the
current snapshot payload carries no RNG state, so a fork "would resume the generator at position 0
and diverge silently from its parent" (`CURRENT-STATE-AUDIT.md:259`). Under substreams that problem
does not disappear; it multiplies by the number of live streams. Determinism under *reordering* is
achieved only if the key set is fixed independently of iteration order, and the position within a
stream still depends on how many times that stream was used, so contamination is contained rather
than eliminated: two draws sharing a key still contend. Parallel execution requires either locking
per stream or partitioning strictly by key. Materialising an entity mid-run means allocating new
streams during the run, which is workable, but the new stream's seeding must not depend on
allocation order or the founder's governing statement fails again.

*Where it is genuinely better.* Debugging is more familiar. Sequence-heavy uses — draw a value, then
another, then another, within one entity's decision — are natural, because the stream remembers
where it is. Per-draw cost is a normal PRNG step, with no hashing.

#### Alternative B — keyed / counter-based deterministic draws — **selected, 19 July 2026**

There is no advancing stream. A value is a pure function of the root seed and a fully-specified key:

```
value = derive(root_seed, algorithm_version, subsystem, entity, interaction, purpose, context, draw_index)
```

The same key always yields the same value; different keys yield independent values; a key is never
"used up".

*How it behaves.* Isolation is **structural rather than disciplinary**. Adding a draw somewhere else
cannot perturb this draw, because this draw never depended on how many draws preceded it — there is
no "preceded". Iteration order is irrelevant by construction, not by convention. Promoting a
background person is a pure key expansion, so re-promoting the same person at the same event yields
the same profile, which is exactly what
`docs/world-model/FOUNDER-REQUIREMENT-2026-07-18.md:236-237` demands. Parallelism is free, because
nothing is shared and nothing mutates. Replay carries no generator position, because there is none
to carry.

*Where it strains.* Sequences within one entity require the caller to manage an explicit
`draw_index`, which is the discipline this approach substitutes for stream position; a caller who
reuses an index silently reuses a value, and the failure is quiet unless it is tested for. Every key
component must be a **stable domain identifier**, which forces an entity-identity design decision
earlier than it would otherwise arrive — a cost here, though it is work P0.4 and the entity ontology
require regardless. Per-draw cost includes a hash or block-cipher step rather than a bare PRNG
advance; whether that matters at MERIDIAN's tick rate has **not been measured** and is listed under
*Consequences we do not yet know*. Debugging a wrong value means reasoning about a key rather than
stepping a stream, which is less familiar, though it is also more inspectable: the key is printable
and reproducible in isolation, so a single suspicious draw can be re-derived by hand without
replaying the run that produced it.

#### The comparison, on the dimensions the founder named

| Dimension | A — stateful named substreams | B — keyed / counter-based |
|---|---|---|
| Isolation between subsystems | Yes, if keys are correctly partitioned | Yes, structurally |
| Determinism under reordering | Only if the key set is order-independent; position within a stream still depends on use count | Yes by construction; order cannot matter |
| Parallelism | Needs locking or strict partition; streams are mutable | Free; pure functions, nothing shared |
| Replay cost | Must snapshot every live stream's position (cf. `CURRENT-STATE-AUDIT.md:259`) | Nothing to snapshot beyond the seed and algorithm version |
| Debuggability | Familiar; sequences read naturally | Key is printable and a single draw is re-derivable standalone; less familiar |
| Implementation complexity | Lower initially; a registry plus disciplined key use | Higher initially; needs a keyed derivation function, stable identifiers and explicit `draw_index` |
| Mid-run entity materialisation | Allocates new streams during the run; seeding must not depend on allocation order | Pure key expansion; nothing is allocated and nothing else is disturbed |
| Failure mode when a developer gets it wrong | Two consumers share a stream → contamination returns, locally | Two consumers share a key → duplicated value, locally |

Both failure modes are local rather than global, which is the point of the whole exercise. Under
today's design a mistake anywhere contaminates everywhere.

#### Why Alternative A was not chosen

Recorded for the ADR's own sake, so the reasoning survives the decision. Alternative A closes the
headline defect and is the cheaper first move, and those advantages are real. It was not chosen on
four grounds. First, its isolation is **contained rather than eliminated**: position within a stream
still depends on how many times that stream was used, so two purposes sharing a stream still
contend, and the founder's governing statement then holds only by convention. Second, it carries
mutable position state, which must be captured for replay or mid-run fork — the defect at
`CURRENT-STATE-AUDIT.md:259` multiplied by the number of live streams — where B has no position to
carry. Third, mid-run entity materialisation allocates streams during the run, and their seeding
must not depend on allocation order or the governing statement fails again; under B promotion is a
pure key expansion that disturbs nothing. Fourth, B's isolation is structural rather than
disciplinary, and this project's recorded defect is precisely that discipline was relied upon where
a structural guarantee was needed.

The costs of that choice are not waived by choosing it: explicit draw indices, stable identifiers
required earlier, an unmeasured per-draw derivation cost, and a new silent failure mode when two
consumers share a key. They are carried in *Consequences* below and are not softened.

#### The alternatives that are rejected

| Alternative | Why rejected |
|---|---|
| **Do nothing — keep ordinary sequential calls to one shared PRNG for authoritative behaviour** | **Explicitly rejected. The founder requires this rejection to be on the record.** Reasoning below. |
| Global `random` module API for authoritative behaviour | Already prohibited by ADR-007 (`scaffold/docs/ARCHITECTURE_DECISIONS.md:63-64`) and by `scaffold/CLAUDE.md`. Unseeded and process-global, so it defeats reproducibility outright. Retained here only so exit criterion 1 has a named target. |
| Fix it inside P0.6 replay instead | Replay records what happened; it does not make unrelated outcomes independent. A faithfully replayed contaminated run is still contaminated. Founder Decision 1 states the problem "must NOT be hidden inside replay". |
| Freeze draw counts by making every conditional draw unconditional (e.g. draw for every cohort whether or not it has grievances) | Would neutralise the specific A3 result — the contamination there comes from the guard at `cohort_agent.py:35` — but it is a workaround, not an architecture. It fails the moment entity counts vary, which is the entire premise of the world model, and it constrains model logic to preserve an RNG accident. |
| Per-entity streams only, without subsystem, interaction, purpose or context in the key | Founder Decision 1 states directly that "Per-entity streams alone are insufficient." Two different purposes drawing for the same entity would still contend, so isolation would hold between entities and fail within them. |

#### Explicit rejection of ordinary sequential calls to a single shared PRNG

**Ordinary sequential calls to one shared PRNG are rejected for authoritative behaviour.** The
reasoning, on the record:

1. **It has already produced a measured false result.** The apparent meso→macro coupling is
   contamination, not causality (`A3-VERIFICATION-RESULTS.md:156-168`), with the movement observed
   at `:162`. This is not a predicted risk; it is a recorded one.
2. **It makes seeds incomparable across versions and scenario variants.** The audit records this at
   `CURRENT-STATE-AUDIT.md:320`. Any refactor that adds or removes a draw invalidates every recorded
   figure, so no numeric result can be cited across a code change.
3. **Ordinary sequential calls cannot satisfy the founder's governing statement.** Under a shared
   stream, materialising a background citizen *necessarily* shifts every later draw, because
   position is the only thing that individuates a draw. The property required is not merely
   unimplemented; it is unreachable by this design.
4. **It is untestable in the way P0.4A requires.** Exit criterion 10 asks for a test that injects
   extra draws into one stream and verifies other streams are unchanged. Under a single shared
   stream that test's expected outcome is failure by construction — there is only one stream to
   inject into.
5. **The existing test suite cannot detect the defect**, per the analysis above, so discipline is
   the only safeguard, and discipline is not a control.
6. **The charter forbids the resulting output class.** `CHARTER.md:118-131` requires every material
   outcome to answer "What caused it?" and "Which rule or mechanism applied?", and states that
   output which cannot answer those questions is flavour text that must not modify the simulation.
   A macro indicator that moved because an unrelated cohort consumed an extra draw cannot answer
   either question truthfully.

This rejection covers **authoritative** behaviour, per the scope limit in the Decision.

---

### Consequences

**Positive.**

- The founder's governing statement becomes achievable and, under criteria 5 to 10, testable:
  materialising a background citizen would not change tomorrow's weather, market behaviour,
  government approval or another person's decision.
- The false meso→macro appearance disappears. A future cross-tier coupling built under P0.5 could
  then be demonstrated to be real, because the contamination channel that currently mimics it would
  be gone. **P0.5's central claim is not honestly demonstrable until this lands** — which is why
  the founder's sequencing gates P0.5 implementation behind P0.4A.
- Seeds become comparable across code versions and scenario variants, closing
  `CURRENT-STATE-AUDIT.md:320`.
- Recorded numeric results survive refactors that add or remove unrelated draws, so an audit figure
  stays citable.
- Entity promotion becomes specifiable at all. Requirement "Once materialised, their identity and
  history must remain stable" (`FOUNDER-REQUIREMENT-2026-07-18.md:236-237`) has a mechanism.
- Under Alternative B specifically: parallel execution and mid-run fork become tractable, and the
  no-RNG-state-in-snapshot defect at `CURRENT-STATE-AUDIT.md:259` is dissolved rather than fixed,
  because there is no generator position to snapshot.

**Negative.** *Required, and stated at least as fully as the positives.*

- **Every recorded numeric result in this repository would be invalidated.** Changing how draws are
  derived changes the values. Every figure in `CURRENT-STATE-AUDIT.md` §4 and in
  `A3-VERIFICATION-RESULTS.md` — the tick-61 clamp, the 0.6080→0.5973 shipping movement, the
  100-tick trajectories, the 40-tick hashes at `A3-VERIFICATION-RESULTS.md:96-97` — would cease to
  be reproducible against the new engine. They remain valid as a record of the *audited* build and
  must be relabelled as such rather than silently carried forward. **The audit must not be
  re-opened to regenerate them** (`HANDOFF.md` § Standing constraints (`:137`)); this is a labelling obligation, not a
  re-verification one.
- **The existing test suite is affected, and the five passing tests must be looked at
  individually.** These are *predictions from reading the tests*; nothing was executed for this
  document.
  - `test_same_seed_is_deterministic` (`test_engine.py:34-40`) — expected to keep passing, since
    same-seed repetition holds under any of these designs. **Its continued passing must not be
    read as evidence that P0.4A succeeded.** It is necessary and nowhere near sufficient, and it is
    the test whose insufficiency motivates this ADR. It should be supplemented by isolation tests,
    and its docstring claim that the seeded RNG "fully determines the numbers"
    (`test_engine.py:3-5`) should be revisited under P0.1 for a separate reason recorded at
    `CURRENT-STATE-AUDIT.md:110-117`.
  - `test_different_seed_diverges` (`:43-49`) — expected to keep passing; two different root seeds
    should still produce different derived values. If it were ever to fail, that would indicate the
    key derivation is ignoring the root seed, which is worth knowing.
  - `test_macro_state_actually_changes` (`:52-58`) — expected to keep passing, since it asserts
    movement in `military_readiness`, which is driven by the action table (`engine.py:35-43`) and
    not by any draw.
  - `test_runs_a_few_ticks` (`:25-31`) and `test_llm_gateway_cannot_write_state` (`:61-77`) —
    expected to be unaffected; neither touches the RNG.
  - **Any test asserting a specific numeric value would break.** A reading of the file suggests none
    currently does. That reading was not confirmed by execution.
- **Migration cost lands on three call sites plus their construction path** (`cohort_agent.py:36`,
  `diffusion.py:75`, `engine.py:135`, constructed at `engine.py:83`). The call-site count is small
  today. The real cost is not the edit; it is that under Alternative B every call site must acquire
  a stable key, which forces entity-identity decisions that P0.4 and the entity ontology were going
  to have to make anyway but which would now be **on P0.4A's critical path**.
- **`diffusion.py` needs the most thought.** `linear_threshold_step` takes the shared `rng` as a
  parameter and draws once per graph node inside a loop over `graph.nodes`
  (`diffusion.py:64-75`). Its signature changes, and each node's draw needs a key built from that
  node's cohort identity plus a purpose plus the tick. This is also where the reordering criterion
  bites hardest, since `networkx` node traversal order is exactly the kind of incidental ordering
  criterion 7 exists to neutralise. Whether traversal order is currently stable was **not
  investigated**.
- **It adds a new way to be wrong.** Under B, two consumers that accidentally share a key get the
  same value silently; under A, two consumers that share a stream contend silently. Neither failure
  is loud without a test for it. This ADR does not remove the need for discipline; it narrows the
  blast radius of an indiscipline from global to local.
- **`hash()` becomes a live hazard rather than a latent one.** Criterion 3 exists because Python
  randomises `str` hashing per process unless `PYTHONHASHSEED` is fixed, so a key built from
  `hash()` would produce different values on different runs of the same code. Nothing in the current
  three draw sites uses `hash()` — they do not build keys at all — but a keyed design invites it,
  and it would fail in a way that only shows up across process boundaries.
- **Mesa's second generator remains a live trap and is not fixed by this ADR.** Audit finding 27
  (`CURRENT-STATE-AUDIT.md:319`) records that the `seed=` kwarg at `engine.py:82` is inert, that
  Mesa seeds its own `self.random` in `Model.__new__` — from entropy on the API path — and that "a
  one-character typo (`self.model.random` for `self.model.rng`) would break reproducibility
  silently." Under this ADR the correct object stops being called `.rng`, so the typo surface
  changes shape but does not close. Criterion 2 is the control that addresses it. Whether Mesa
  remains the substrate at all is open audit decision 8.3 (`CURRENT-STATE-AUDIT.md:405`), and this
  ADR does not decide it. *(Mesa's internals were not re-verified here; this is inherited from the
  audit.)*
- **It enlarges Phase 0.** P0.4A is a new workstream with implementation and a ten-part test
  obligation, and it gates P0.5 implementation, entity promotion and world-model materialisation.
  Phase 0 finishes later than it would have without it.
- **It may pull a schema change forward.** If draw keys are to be recorded per criterion 9, event
  and snapshot records need somewhere to put them, which touches P0.6's territory from inside
  P0.4A. Whether keys are recorded on every draw or only derivable on demand is an open question
  below.

**Consequences we do not yet know.**

- **Whether any measurable performance cost exists.** Alternative B replaces a PRNG advance with a
  keyed derivation per draw. At three draws per tick this is certainly irrelevant; at world-model
  scale, with per-entity draws across a large population, it may not be. **Not measured. No
  benchmark exists.** Finding out requires a prototype and a representative population size,
  neither of which exists.
- **Which derivation primitive to use.** The choice between a cryptographic hash construction, a
  counter-based generator of the Philox/Threefry family (available via `numpy.random`), and a
  keyed block cipher has not been made. It bears on criterion 4, on the dependency question, and on
  cross-language reproducibility if a non-Python component ever consumes the same stream. Adding a
  dependency is itself an ADR-triggering decision (`ADR-TEMPLATE.md` §1.2).
- **Whether the resulting numbers differ materially from today's**, in the sense of changing any
  conclusion in the audit. They will certainly differ; whether any *finding* changes is unknown and
  would require re-running `docs/delivery/evidence/` against an implementation that does not exist.
- **How the key schema interacts with the entity ontology.** The key needs stable entity
  identifiers, and `docs/world-model/ENTITY-ONTOLOGY.md` is itself specification-only. If identifiers
  change shape later, keys change, and derived values change with them. There may need to be a rule
  that entity identifiers are immutable once issued. **That rule is not proposed here** — it is
  flagged as an open question below.
- **Whether the ten criteria are jointly sufficient.** They are the founder's minimum. Nothing has
  been executed against them, and their sufficiency is untested by construction, since no
  implementation exists to test.

---

### Determinism impact

*(Required by the template. This ADR is about determinism, so no answer here is a plain "No", and
each is justified.)*

| Question | Answer | Justification |
|---|---|---|
| Does this change what counts as authoritative state, or what may write it? | **Unknown** | The set of writers is unchanged — `engine.py` remains the sole writer of numeric state (ADR-006). But if draw keys are recorded per criterion 9, the *record* of a state change gains a field, and whether that record is authoritative is a P0.4 question that P0.4A follows and does not pre-empt. Expected, not measured; nothing is implemented. |
| Does this change the number, order or source of RNG draws? | **Yes** | The **source** changes fundamentally: from one shared sequential `random.Random` (`engine.py:83`) to per-key derived values. Under Alternative B, "order" ceases to be a meaningful property of a draw, which is the entire point. Draw *count* per tick may be unchanged at the three current sites, but the values they produce would differ. Expected from design, not measured — no implementation exists to measure. |
| Does this change snapshot contents, event records, or any future ability to replay? (No replay capability currently exists — answer for the target contract, not a delivered one.) | **Yes, for the target contract** | Under Alternative B a snapshot need not carry generator position, which removes the fork-diverges-silently defect at `CURRENT-STATE-AUDIT.md:259` — under Alternative A that position must instead be captured per stream. Criterion 4 adds algorithm and version to what a run records. Criterion 9 may add key provenance to draw records, which bears directly on audit finding 17, "No random draw is ever recorded" (`CURRENT-STATE-AUDIT.md:304`). **No replay capability exists to affect today**; this is about what P0.6 would build on top. |
| Does this change a claim the project makes about determinism or reproducibility? | **Yes** | ADR-007's "All engine, agent, and diffusion randomness draws from that one RNG" (`scaffold/docs/ARCHITECTURE_DECISIONS.md:63-64`) would no longer describe the design, and its "proven by `test_same_seed_is_deterministic`" (`:65`) does not prove isolation regardless. `scaffold/CLAUDE.md`'s instruction to "Use `self.rng`" would cease to be correct guidance. What the project may claim **today** is unchanged by this ADR and remains exactly the founder-fixed wording: *"The existing stubbed execution path reproduces the same tested numeric outputs when the seed, scenario and stubbed agent outputs remain identical."* The target contract remains, and remains labelled a target: *"Given the same scenario version, rule-pack version, seed, ordered player inputs and recorded external-agent inputs, the engine is intended to reproduce identical authoritative state hashes."* **This ADR does not license any new claim.** Correcting ADR-007 and `CLAUDE.md` is Phase C / P0.1 work in files this run must not touch. |

Every "Yes" and "Unknown" above is **expected from design, not measured.** Nothing was executed for
this document and no implementation exists.

---

### Verification — the ten exit criteria

These are the founder's minimum exit criteria for P0.4A, reproduced in full and restated so each is
testable. **None is met today.** The right-hand column is how a reader could check the criterion
once an implementation exists; it describes tests that do not exist.

| # | Criterion | How it would be verified |
|---|---|---|
| 1 | No authoritative code calls the global `random` API directly. | Static check over the authoritative tree for `random.random`, `random.uniform`, `random.choice`, `random.seed` and siblings called on the module rather than an instance. Enforceable in CI (P0.3) as a lint rule or AST check, so it cannot regress silently. Note the current design already intends this (ADR-007 `:63-64`) but nothing enforces it. |
| 2 | No subsystem receives unrestricted access to the root generator. | Structural test: the root seed/generator is not reachable as a public attribute a subsystem can draw from. Contrast with today, where `self.model.rng` is read directly at `cohort_agent.py:36` and the object is passed wholesale into `linear_threshold_step` (`engine.py:143-144`). A test that fails when a subsystem is handed the root object. |
| 3 | Stream keys use stable identifiers — **not** Python's process-randomised `hash()`. | Two-part. Static: no `hash(` in key construction. Behavioural: run the same scenario in two processes started with different `PYTHONHASHSEED` values and assert identical authoritative output. The second part is the one that actually catches it. |
| 4 | The run records the RNG algorithm and version. | Assert the run record contains a non-empty algorithm identifier and version, and that changing the algorithm changes the recorded value. Today `derivation` is a frozen constant, `"rules_engine_v1 + seed_init"`, set once at `engine.py:68` (audit finding 16, `CURRENT-STATE-AUDIT.md:303`), so every snapshot reports identical provenance — this criterion is a direct answer to that finding. |
| 5 | Adding an unrelated entity does not alter unrelated subsystem results. | The direct regression test for the A3 result. Run a scenario; run it again with one extra cohort added; assert macro output is **identical**. Under today's engine this test fails — that failure is what `A3-VERIFICATION-RESULTS.md:153` and the movement at `:162` record. |
| 6 | Promoting one background person does not alter previously established entities. | Requires entity promotion, which does not exist and is gated behind this criterion. Stated now so promotion is built against it: promote one background person mid-run; assert every previously established entity's state is bit-identical to a control run without the promotion. This is the founder's governing statement rendered as a test. |
| 7 | Reordering entity iteration does not alter outcomes **where the model declares order irrelevant**. | Two obligations. First the model must *declare*, per collection, whether order is material — that declaration does not exist today and is part of the work. Then: shuffle the declared-order-irrelevant collections and assert identical output. Note the qualifier: this is not a claim that order never matters, and a collection where order is material must say so rather than be silently shuffled. Compare `CURRENT-STATE-AUDIT.md:457`, which already asks that reversing cohort order be a detectable condition. |
| 8 | Repeating the same promotion event produces the same profile and history. | Promote the same background person from the same event twice, in separate processes; assert the generated profile and history are identical. This is `FOUNDER-REQUIREMENT-2026-07-18.md:236-237` — "Once materialised, their identity and history must remain stable" — as a test. |
| 9 | Every random outcome can be associated with a subsystem, entity or interaction, and a purpose. | Every authoritative draw is attributable to its key. Verified either by recording the key with the draw or by a deterministic re-derivation path from the record. This closes audit finding 17: "No random draw is ever recorded. Stream, index, distribution, parameters and value are all discarded" (`CURRENT-STATE-AUDIT.md:304`). Whether keys are stored or re-derived is an open question below. |
| 10 | Tests deliberately inject extra draws into one stream and verify other streams remain unchanged. | The isolation test proper, and the one the current suite most conspicuously lacks. Inject N extra draws into one subsystem's stream; assert every other subsystem's output is bit-identical. Must be run for each pair of subsystems that could contend, not once globally, or it proves less than it appears to. |

**The relationship between these tests and the existing suite must be stated plainly.**
`test_same_seed_is_deterministic` (`test_engine.py:34-40`) is a same-seed repetition test. It would
accept draw-order contamination as ordinary divergence
(`A3-VERIFICATION-RESULTS.md:174-175`). Criteria 5 to 10 are **isolation** tests: they perturb one
thing and assert another did not move. **P0.4A is not satisfied by the existing test continuing to
pass.** Whether the isolation tests supplement the existing determinism test or replace it is a
judgement for whoever implements P0.4A, but the existing test alone must never be cited as evidence
that isolation holds.

---

### Evidence

| Claim | Evidence |
|---|---|
| There is exactly one `random.Random` in application code, described in source as the only source of engine randomness | `scaffold/backend/app/simulation/engine.py:83`. Exhaustiveness rests on `grep -rn "random\.Random(\|\.rng\." scaffold/backend/app`, not on the single citation |
| Three sites consume it | `scaffold/backend/app/simulation/agents/cohort_agent.py:36`; `scaffold/backend/app/simulation/diffusion.py:75`; `scaffold/backend/app/simulation/engine.py:135` |
| The cohort draw is conditional on a non-empty grievance list — the mechanism behind the A3 result | `scaffold/backend/app/simulation/agents/cohort_agent.py:35-36` |
| Diffusion draws once per graph node, inside a loop over `graph.nodes`, with the shared generator passed in as a parameter | `scaffold/backend/app/simulation/diffusion.py:64-75`; passed at `scaffold/backend/app/simulation/engine.py:143-144` |
| Changing cohort *values* by two orders of magnitude changed macro by nothing | `docs/delivery/A3-VERIFICATION-RESULTS.md:152`, `:165` |
| Adding a grievance to the one cohort that had none changed macro; deleting a cohort changed macro | `docs/delivery/A3-VERIFICATION-RESULTS.md:153-154` |
| The observed movement: `shipping_throughput_pct_of_baseline` 0.6080711379477878 → 0.5973599412373322 | `docs/delivery/A3-VERIFICATION-RESULTS.md:162` |
| The apparent meso→macro coupling is contamination, not causality | `docs/delivery/A3-VERIFICATION-RESULTS.md:156-168`, corrected statement at `:167-168` |
| There are no named RNG substreams; adding or removing a draw in one subsystem silently changes every subsequent draw everywhere | `docs/delivery/A3-VERIFICATION-RESULTS.md:170-175`; audit informational item 28 at `docs/delivery/CURRENT-STATE-AUDIT.md:320` |
| The existing determinism test would mask such a change as expected divergence | `docs/delivery/A3-VERIFICATION-RESULTS.md:174-175` |
| A3's results are from execution, not inspection | `docs/delivery/A3-VERIFICATION-RESULTS.md:23`; script `docs/delivery/evidence/a3_rng_isolation.py` |
| The determinism test compares two same-seed runs and inspects only the final macro snapshot | `scaffold/backend/tests/test_engine.py:34-40`; meso is uninspected per audit 5.3, `docs/delivery/CURRENT-STATE-AUDIT.md:136` |
| The suite is five tests in one file | `scaffold/backend/tests/test_engine.py`; audit finding 32, `docs/delivery/CURRENT-STATE-AUDIT.md:329` |
| No random draw is ever recorded — stream, index, distribution, parameters and value all discarded | audit finding 17, `docs/delivery/CURRENT-STATE-AUDIT.md:304` |
| `derivation` is a frozen constant, identical in every snapshot | audit finding 16, `docs/delivery/CURRENT-STATE-AUDIT.md:303`; set at `scaffold/backend/app/simulation/engine.py:68` |
| A snapshot carries no RNG state, so a fork would resume at position 0 and diverge silently | audit 5.14, `docs/delivery/CURRENT-STATE-AUDIT.md:259` |
| Mesa's `seed=` kwarg is inert; Mesa keeps a second generator seeded from entropy on the API path; a one-character typo would break reproducibility silently | audit finding 27, `docs/delivery/CURRENT-STATE-AUDIT.md:319`; kwarg at `scaffold/backend/app/simulation/engine.py:82` |
| Whether Mesa remains the ABM substrate is an open owner decision | `docs/delivery/CURRENT-STATE-AUDIT.md:405` (audit §8.3) |
| ADR-007 records one seed threaded into `self.rng`, prohibits global `random` and unseeded `numpy`, and cites `test_same_seed_is_deterministic` as proof | `scaffold/docs/ARCHITECTURE_DECISIONS.md:60-67` |
| ADR-006 makes `engine.py` the sole writer of numeric state | `scaffold/docs/ARCHITECTURE_DECISIONS.md:50-58` |
| Entity promotion must be deterministic and materialised identity must remain stable | `docs/world-model/FOUNDER-REQUIREMENT-2026-07-18.md:230-237` |
| Every material outcome must answer what caused it and which rule applied; output that cannot is flavour text and must not modify the simulation | `CHARTER.md:118-131` |
| An ADR is required for anything changing the RNG or the number or order of random draws | `docs/delivery/ADR-TEMPLATE.md` §1.2, final row; `HANDOFF.md` § Standing constraints (`:139-140`) |
| The two fixed determinism wordings | `HANDOFF.md:52-62`; reproduced verbatim in the Determinism impact table |
| The broad audit is closed and must not be re-opened | `HANDOFF.md` § Standing constraints (`:137`); `docs/delivery/A3-VERIFICATION-RESULTS.md:253-257` |

**Not verified.**

- **No code was executed for this document. No test was run. No benchmark was taken.** Every
  statement about how the proposed architecture would behave is reasoning from design, not
  observation, and may be wrong.
- The predicted effect on each of the five existing tests is a reading of `test_engine.py`, not a
  measurement. In particular, the claim that no existing test asserts a specific numeric value is a
  reading of that one file and was not confirmed by a search across the tests directory.
- The A3 results, the audit findings and the movement figure at `A3-VERIFICATION-RESULTS.md:162`
  are **inherited** from those documents. They were read at the cited lines; they were not
  re-derived, and re-deriving them would mean re-opening a closed audit (`HANDOFF.md` § Standing constraints (`:137`)).
- Mesa's internals were not re-verified. Finding 27 is inherited from the audit.
- Whether `networkx` node traversal order is stable across runs or versions was **not
  investigated**, though criterion 7 bears on it directly.
- Whether the ten criteria are jointly sufficient to establish isolation is untested, necessarily,
  since no implementation exists.
- The performance characteristics of any keyed derivation primitive at world-model scale are
  unmeasured, and no candidate primitive has been benchmarked or selected.
- Whether any audit *conclusion* would change under a corrected RNG architecture is unknown.

---

### Open questions for the owner

*(Raised, not decided. An AI agent may not resolve any of these. The template has no field for this
section — see the template note below.)*

1. ~~**Approach.** Adopt Alternative B (keyed / counter-based), as recommended? Or Alternative A
   (stateful named substreams)?~~ **RESOLVED by the founder, 19 July 2026 (Founder Decision 3):
   Alternative B, keyed / counter-based deterministic randomness, is adopted as the primary
   authoritative randomness architecture.** Retained struck through rather than deleted, so the
   question and its resolution both stay on the record. The remaining questions below are still
   open.
2. **Consolidation of this ADR.** Does ADR-010 stay at `docs/adr/`, or is it consolidated into
   `scaffold/docs/ARCHITECTURE_DECISIONS.md` alongside ADR-001 to ADR-009? This is open question 2
   of `ADR-TEMPLATE.md` §4 and is unresolved. This run did not touch that file.
3. **ADR-007's disposition.** Corrected in place, superseded by this ADR, or left as historical
   record with a status note? This is open question 3 of the template, applied to ADR-007
   specifically. It affects a file under `scaffold/` that Phase C owns.
4. **Derivation primitive.** Cryptographic hash, counter-based generator (Philox/Threefry, e.g. via
   `numpy.random`), or keyed block cipher? If it introduces or changes a dependency, that is itself
   an ADR-triggering decision (`ADR-TEMPLATE.md` §1.2).
5. **Are draw keys recorded, or re-derived on demand?** Criterion 9 requires attribution, not
   necessarily storage. Recording every key touches event and snapshot shape, which is P0.6
   territory reached from inside P0.4A.
6. **Must entity identifiers be immutable once issued?** Keys built from entity identifiers change
   if the identifiers change, and derived values change with them. This looks like a necessary rule
   but it constrains the entity ontology, so it is put to the owner rather than assumed.
7. **What is the authoritative boundary, precisely?** This ADR scopes itself to draws that can reach
   authoritative state, an event, a snapshot or a player-visible outcome, and treats unclear cases
   as authoritative by default. Confirm or narrow.
8. **Does the existing determinism test survive alongside the isolation tests, or is it replaced?**
   This ADR states only that it must never be cited as evidence of isolation.
9. **What happens to the recorded audit figures?** They were produced by the audited build and would
   not reproduce against a corrected engine. Relabel them as belonging to that build — the
   recommended reading, since the audit is closed — or something else?

---

### Approval

**AI agents may draft this record. Under `HANDOFF.md` § Standing constraints (`:138`) an AI agent may not approve its own
decisions; under `ADR-TEMPLATE.md` §1.5 no AI agent approves any ADR. The approval below is the
founder's, recorded by an agent; the agent did not make it.**

- **Approved by:** the founder (Founder Decision 3)
- **Date:** 19 July 2026
- **Approval covers:** the selection of keyed / counter-based deterministic randomness as the
  primary authoritative randomness architecture; the rejection of ordinary sequential calls to a
  single shared PRNG for authoritative behaviour; the founder-specified key shape; the requirement
  for a central `DeterministicDrawService`; the restriction of stateful substreams to an internal
  optimisation that never crosses the service boundary; and the ten exit criteria as the definition
  of P0.4A done.
- **Approval explicitly does not cover:** implementation; the selection of a derivation algorithm or
  primitive, which is deferred to the implementation plan; the addition or change of any dependency;
  any schema change; any commit or push; any change to a file under `scaffold/`; the disposition of
  ADR-007; or any new claim about what the current system does. Open questions 2 to 9 below remain
  open.

**The architecture is decided. Nothing is implemented, and implementation is not yet authorised.**

---

## Note on the template — its first real exercise

`ADR-TEMPLATE.md` was applied as written. It held up: the Context/Decision/Alternatives/
Consequences/Determinism-impact/Evidence/Approval spine fitted this decision without strain, the
mandatory "Not verified" heading caught several claims that would otherwise have been asserted
flatly, and the four determinism questions were the right four. Three gaps surfaced, reported here
rather than silently worked around.

1. **No verification or exit-criteria field.** The founder requires ten testable exit criteria for
   P0.4A, and the template has nowhere to put them. They do not belong in Consequences (they are
   not consequences) or in Evidence (they describe tests that do not exist, and the Evidence table
   is for checkable claims about what *does*). A **Verification** section was added between
   Determinism impact and Evidence. **Recommendation: add an optional Verification field to the
   template**, required for any ADR whose approval depends on a testable exit condition. This is a
   recommendation to the owner, not a change to the template — the template was not edited.

2. **No open-questions field.** The template's §4 carries open questions for the *template*, and
   §1 requires that any new decision surface be raised for the owner, but an individual ADR has no
   field for the questions it raises. Nine surfaced here. An **Open questions for the owner**
   section was added before Approval. **Recommendation: make it a standard field**, with "None" as
   an acceptable entry, so the absence of open questions is visible rather than merely unwritten.

3. **The Alternatives table cannot express "recommended but not selected".** Its two columns are
   *Alternative* and *Why rejected*, which presumes the decision has been taken. Where an AI agent
   drafts, the decision has not been taken, so both live candidates would have to be listed as
   rejected or omitted. Alternatives A and B are therefore presented in prose above the table with
   a comparison matrix, and the table carries only the genuinely rejected options. **Recommendation:
   the template should say explicitly how a Proposed ADR presents candidates it has not chosen
   between** — this is not an edge case, it is the normal shape of every AI-drafted ADR.

A fourth, smaller observation: the template's guidance to state whether a decision is "taken" or
"taken and built" has no third setting for "drafted, recommended, not taken". The wording
*"Proposed; not decided and not implemented as of \<date\>"* was used. Worth adding to §1 as the
standard form, since it will be the most common one.

None of these required deviating from the template's substance, and no field was dropped.
