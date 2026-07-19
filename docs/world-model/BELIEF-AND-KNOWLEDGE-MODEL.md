# Belief and knowledge model

> # ⚠ SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing in this document exists in code.** Not one field, not one function, not one label.
> Every mechanism described here is a statement of intent for a future architecture. Where this
> document describes something that *does* exist today, it says so explicitly and cites the file
> and line, so the boundary between what exists and what is specified is always visible.
>
> This document is written in "will", "must" and "is intended to". If any sentence in it reads as
> a description of working software, that sentence is a defect and should be corrected. MERIDIAN's
> defining problem is documentation that claims properties the code does not have; this document
> must not add to it.

**Status:** DRAFT, pending owner review.
**Date:** 18 July 2026.
**Amended:** 19 July 2026, to apply founder ownership ruling 1A. Observation and perception are no
longer owned here; they are owned by
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md). This document owns what
happens **after** an observation exists. A mechanism register was added as Part 0, because this
document previously had none — which is why `M-OBS` was assigned to it and then had no register to
land in. The amendment adds ownership statements and a register; it withdraws no specification and
resolves no open question.
**Disposition:** **BACKLOG. This must not interrupt Phase 0 remediation.** Per
[`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md) lines 5-6 and 340-341, and
[`../../HANDOFF.md`](../../HANDOFF.md) lines 99-112, this is captured now so that the intent is
explicit and dated before the replacement simulation architecture is designed. **Do not start
building any of it.** Several of its hard prerequisites are themselves unbuilt, and at least one
requires an owner decision that no agent may take.

**Authority:** [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md) is the
source record. Where this document and that record disagree, that record is right and this document
is wrong. [`../../CHARTER.md`](../../CHARTER.md) governs both.

**Sibling documents** (verified present on disk, 18 July 2026; all backlog, all DRAFT, none
reviewed by the owner and none describing implemented software):
[`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) ·
[`PERSON-MODEL.md`](PERSON-MODEL.md) ·
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) (added 19 July 2026;
DRAFT, verified present on disk that date) ·
[`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) ·
[`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) ·
[`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) ·
[`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) ·
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md)

---

## Contents

- [Part 0 — Ownership boundary and mechanism register](#part-0--ownership-boundary-and-mechanism-register)
- [Part 1 — Plain English](#part-1--plain-english)
- [Part 2 — What exists today](#part-2--what-exists-today)
- [Part 3 — Prerequisites this document depends on and cannot satisfy](#part-3--prerequisites-this-document-depends-on-and-cannot-satisfy)
- [Part 4 — Technical specification](#part-4--technical-specification)
- [Part 5 — Mechanism map: every specified attribute and what it feeds](#part-5--mechanism-map-every-specified-attribute-and-what-it-feeds)
- [Part 6 — Rejected as fake depth](#part-6--rejected-as-fake-depth)
- [Part 7 — Attributes specified whose mechanism is unresolved](#part-7--attributes-specified-whose-mechanism-is-unresolved)
- [Part 8 — Invariants and test obligations](#part-8--invariants-and-test-obligations)
- [Part 9 — Open questions for the owner](#part-9--open-questions-for-the-owner)

---

# Part 0 — Ownership boundary and mechanism register

**Added 19 July 2026, applying founder ownership ruling 1A.** It is numbered 0 rather than inserted
as a new Part 5 because Parts 1-9 are cited by number from sibling documents and from
[`../delivery/`](../delivery/) records; renumbering them would silently break those citations.

## 0.1 What this document does not own: observation and perception

Observation is owned by
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) (DRAFT, 19 July 2026),
per founder decision 1A.

That document owns observation opportunity, sensor and source access, direct versus mediated
observation, visibility, range, latency and degradation, source attribution, observation confidence
at acquisition, observation events, and the transformation of a world event into an entity-specific
observation. It defines `M-OBS` as the umbrella mechanism and decomposes it into `M-OBS-EXP`
(exposure and observation opportunity), `M-OBS-ACQ` (acquisition, relay and degradation),
`M-OBS-ATTR` (source attribution and identity resolution) and `M-OBS-SURF` (observable surface).

**This document owns what happens after an observation exists:** belief updating and knowledge
storage, and the player-facing confidence labelling computed over a role's observation set (4.7).

## 0.2 The boundary chain

Each stage has exactly one owner. The handover point is the `Observation` record: everything upstream
of it is the observation model, everything downstream is this document until the projection step.

```text
  world event
      │   exposure — observation opportunity          OBSERVATION-AND-PERCEPTION-MODEL  M-OBS-EXP
      ▼
  observation opportunity
      │   acquisition, relay, attribution             OBSERVATION-AND-PERCEPTION-MODEL  M-OBS-ACQ
      ▼                                                                                 M-OBS-ATTR
  entity-specific observation        ← HANDOVER POINT
      │   belief update                               THIS DOCUMENT  4.5  (M-BEL-UPD)
      ▼
  belief and knowledge state                          THIS DOCUMENT  4.2-4.6  (M-BEL-STO)
      │   view projection                             ENTITY-ONTOLOGY.md §9.2
      ▼                                               + the access/role layer, which does not exist
  role-filtered projection
      │   rendering and narration                     ../design/ENTITY-PROFILE-EXPERIENCE.md
      ▼
  dossier presentation
```

Two consequences bind the rest of this document.

- **This document is not a writer of `Observation` records.** `M-OBS-ACQ` is their sole writer. Where
  Part 4.3 specifies the record, it specifies a record it *consumes*; the schema's ownership of
  record is an open question in the owning document (its Q3), not settled here.
- **The confidence labels in 4.7 remain here.** They are a property of the disclosure view, computed
  per role over that role's observation set. They are distinct from the observation model's
  *observation confidence at acquisition*, which is an evidential property of the acquisition itself.
  Two different quantities; neither may be computed from the other without an owner ruling.

## 0.3 Mechanism register

**This document previously had no mechanism register.** That absence is why `M-OBS` — defined in
[`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md):390 and assigned to this document by that
document's §20 — had nowhere to land: an assignment to a document with no register cannot be
checked, and the mechanism disappeared. That assignment is superseded by founder decision 1A. The
register below exists so the same failure cannot recur here.

Every mechanism must name what reads it. A mechanism with no reader is the same defect as an
attribute with no reader (Part 5, and audit 5.10), and is a candidate for striking under the rule
proposed for owner ratification in Part 9 question 6.

**None of these is implemented.** Each is specified in the section cited.

| Id | Name | What it must do | What reads it |
|---|---|---|---|
| `M-BEL` | **Belief and knowledge** (umbrella) | Must maintain, per entity, what that entity holds to be true and on what recorded evidence, given the observations delivered to it by `M-OBS-ACQ`. Decomposes into the six below; not a buildable unit on its own | — (umbrella) |
| `M-BEL-STO` | **Knowledge storage** | Must store `Proposition` (4.2), the retained per-entity `Observation` set (4.3), `Belief` (4.5), `InterpretivePrior` (4.4), `PropositionLink` (4.5) and `DecisionDriver` (4.9) as authoritative, append-only-where-specified state, and must never delete an observation | `M-BEL-UPD`; `M-BEL-CONF`; the `factually_wrong()` query (4.6); the self-understanding projection (4.9); view projection, [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2 |
| `M-BEL-UPD` | **Belief update** | Must apply the signed, floored, bidirectional update rule (4.5) when an observation reaches a holder, must hold credence in the open interval `[ε, 1−ε]`, must update `stability` and `salience`, and must emit a `BeliefUpdated` event carrying every coefficient used | Decision gating (**no reader exists — no decision model is built**, Part 7); cohort→macro aggregation (4.8, P0.5, [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md)); the divergence query (4.6); the self-understanding comparison (4.9) |
| `M-BEL-EVW` | **Evidence weighting** | Must compute the non-source terms of the update gain: `congruence` against `commitment_set(h)` via `PropositionLink.alignment`, `prior_gain(h, topic)` from `InterpretivePrior`, and the `(1 − stability)` term, each bounded by `RESISTANCE_FLOOR`, `δ` and the `InterpretivePrior` bounds | `M-BEL-UPD` only. It has exactly one reader by design: a weighting term that anything else could read would be a second, uncontrolled route into belief |
| `M-BEL-SRC` | **Source-trust weighting** | Must compute `source_weight(h, o)` from directional trust, channel credibility, directness and fidelity, bounded strictly within `(0, 1]`. **B5-gated:** the perceived-independence term and the corroboration-defeat rule are deferred to an unwritten annex; see the gate at the head of 4.5 and Part 9 question 7 | `M-BEL-UPD` only |
| `M-BEL-RUM` | **Rumour propagation through a population** | Must propagate credence across cohort-tier holders over relayed observations (4.8), carrying a `(mean_credence, dispersion)` distribution rather than a scalar, and applying the same signed, floored rule as `M-BEL-UPD`. **Scope limit:** this is the belief-side spread of a claim through holders. The transmission itself — relay, latency, fidelity loss, distortion — is `M-OBS-ACQ` and is not owned here | Cohort→macro aggregation (P0.5); materialisation sampling for tier promotion ([`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) §5.5) |
| `M-BEL-CONF` | **Confidence assignment** | Must compute the eight player-facing labels (4.7) per attribute, per viewing role, deterministically over that role's own observation set, and must never be produced by the LLM | The disclosure view, rendered by [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md). **`Restricted` has no reader until the access and role layer exists** (3.6, Part 7) |

**Naming convention, not settled here.** `M-BEL*` follows the `M-OBS*` form adopted by
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5 and the
`ORGANISATION-MODEL.md` convention; [`PERSON-MODEL.md`](PERSON-MODEL.md) uses `M<n>`. Whether the
registers are unified or bridged by a crosswalk is [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md)
§19 **Q12**, an open owner decision. This document does not take it, and the identifiers above must
be treated as provisional until it is taken. It is restated as Part 9 question 12.

---

# Part 1 — Plain English

## The problem this solves

In a crisis, almost nobody has the facts. People act on what they have seen, what they have been
told, what they suspect, and what they want to be true. A minister orders a deployment because
intelligence said something that later turns out to be wrong. A fishing community believes the
government closed the strait deliberately, when in fact the government could not prevent it. A
politician genuinely believes they are acting in the national interest while everyone around them
sees career protection.

MERIDIAN cannot represent any of that today. It has exactly one copy of the truth, and every entity
in the simulation has perfect access to it — or, more precisely, no access to it at all, because
nothing reads anything.

This document specifies four things that must be kept strictly apart, and never collapsed into one
another.

| Layer | Plain meaning | Example |
|---|---|---|
| **Truth** | What is actually the case in the simulated world. | The strait closed because a cargo vessel grounded in the channel. |
| **Knowledge** | What a particular entity has observed or been told, and from whom. | The harbour master saw the vessel. The minister was told about it by an aide, second-hand. A fishing cohort heard a rumour on a messaging app. |
| **Belief** | What that entity currently holds to be true, which may be false. | The fishing cohort believes the closure was ordered by the government. |
| **Disclosure** | What a given player, in a given role, is shown — labelled with how well it is evidenced. | The player sees: *"Cause of closure — Reported"*, not *"Cause of closure — vessel grounding"*. |

The rule that makes this coherent:

> **Truth is authoritative. Knowledge is a record of what reached whom. Belief is computed from
> knowledge. Disclosure is computed from belief, knowledge and role. Only the first three are state.
> Disclosure is a view, and it is never written back.**

## Why belief must be able to be wrong

The founder record asks that the profile interface support the question *"What does this person
believe that is factually wrong?"*
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):189). That question is
only answerable if three conditions hold at once:

1. Beliefs are **about something identifiable** — a claim with a stable identity, not a free-text
   sentence, so the same claim can be compared across entities and against the truth.
2. The claim has an **authoritative truth value** that is recorded separately from anyone's opinion
   of it.
3. Some claims are **not truth-apt at all**. "The government is incompetent" is a judgement, not a
   fact. The system must never report an entity as *factually wrong* about a value judgement. This
   is not a technicality: four of the five belief fields that exist today are judgements of exactly
   this kind, and treating them as facts with truth values would manufacture certainty the CHARTER
   forbids ([`../../CHARTER.md`](../../CHARTER.md):56, "contestable where the real world is
   contested").

## Why belief must be able to resist evidence

People do not update cleanly. Evidence that fits what someone already believes lands harder than
evidence that contradicts it. Evidence from a trusted source lands harder than the same evidence
from a distrusted one. Someone who lived through political violence reads an ambiguous security
report differently from someone who did not.

The specified model must reproduce that — **and must do so without ever making a belief
unchangeable.** This is the single most important constraint imposed by the existing audit, and it
is explained in the next section.

## The one-way ratchet: the failure this model must not reproduce

Audit finding 5.9 ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md):205-211)
records that the only belief dynamic in MERIDIAN today is a decay toward zero that nothing can
reverse. Cohorts with grievances lose belief in government competence every tick; no code path
anywhere increases it; no player or agent action can recover it. Measured at seed 88213 over 100
ticks, four of five demonstration cohorts reach 0.0 and stay there. The fifth never moves at all,
because it has no grievance and therefore no dynamic.

Two consequences follow, and both bind this document.

**First: the specified update rule must be signed and bidirectional.** Every belief change must be
able to move in either direction, and the direction must be determined by the evidence, not by the
sign of a constant.

**Second: no belief may reach an absorbing state.** A belief pinned at 0.0 or 1.0 cannot be moved by
any subsequent evidence, which makes the rest of this model decorative. Credence must be held inside
an open interval, strictly away from both bounds. The audit's own Phase 4 exit criterion already
requires this: *"A 500-tick run has no indicator at a clamp boundary and no cohort belief at 0.0 or
1.0, asserted by a test"* ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md):484).

There is a related trap worth naming now. Any model of motivated reasoning — the mechanism by which
belief resists inconvenient evidence — is one careless coefficient away from re-creating the
ratchet. If contradicting evidence is discounted to zero for a sufficiently entrenched belief, the
belief has become unrevisable, and the system has reproduced 5.9 in a more sophisticated disguise.
The specification therefore sets a floor on the weight of contradicting evidence, and requires it to
be tested.

## The politician who believes their own account

The founder record's example
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):151-152): a politician may
genuinely think they are acting patriotically while the public views them as opportunistic.

For this to be simulation rather than prose, three separate records must exist and must be allowed
to disagree:

- **What actually drove the decision** — recorded by the engine at the moment of decision: which
  objective or pressure dominated.
- **What the entity believes drove it** — the entity's own belief about itself, which is a genuine
  belief and is genuinely held.
- **What others believe drove it** — other entities' beliefs about that same decision, formed from
  what they observed of it.

The politician is not lying. Their self-account is authoritative as a *belief*, and false as a
*description of the decision*. That gap is what the dossier's self-understanding panel shows, and it
is generated by comparing two recorded values, not by an LLM writing a characterisation.

## What the LLM may and may not do here

**It may:** read a disclosure view and write it up as a briefing; explain why an entity believes
something by walking the recorded chain; hold a conversation about a dossier.

**It must never:** decide that an entity believes something; change a credence; create a claim;
create an observation; assign a confidence label; or resolve a contradiction.

This specification proposes that beliefs be treated as authoritative state — a position P0.4 must
confirm, and which this document must not assume (see Part 3.1 and Part 9 question 2). If that
position holds, beliefs sit squarely inside the determinism boundary that
[`../../CHARTER.md`](../../CHARTER.md):37-44 states and that ADR-006
(`scaffold/docs/ARCHITECTURE_DECISIONS.md`:50-58) enforces. The narration limits above do not
depend on how P0.4 rules: whatever layer belief ends up in, the LLM must not author it.

---

# Part 2 — What exists today

Everything in this part **does exist** in the repository at commit `71fa329`, and is cited so the
reader can check it. Nothing in Part 4 exists.

## 2.1 The only belief structures in the codebase

**`CohortBeliefs`** — `scaffold/backend/app/simulation/schemas/agent_schema.py:56-69`. Five fixed
float fields, each 0..1: `government_competence`, `foreign_interference_probability`,
`trust_in_military`, `support_for_western_alignment`, `support_for_eastern_alignment`. The docstring
at `:57` states they are "Updated by the diffusion model, not the LLM". In fact only
`government_competence` is ever written, by `cohort_agent.py:38`, and only downward; the other four
are written by nothing (audit 5.9).

**`MicroAgent.beliefs`** — `agent_schema.py:170-172`. A free-form `dict[str, float]`, "each value
0..1". Populated from scenario data; read by no code path.

These two representations are mutually incompatible — one is a closed five-field record, the other
an open map — and there is no shared identifier namespace binding a `cohort_id` (`:94`) to an
`agent_id` (`:161`). Neither carries a source, a provenance, a confidence, an observation, or any
distinction between what is believed and what is true.

## 2.2 The only structure that separates truth from belief

**`Narrative`** — `agent_schema.py:261-277`. It carries `truth_status`
(`true` / `false` / `unverified`, defined at `:253-259`) alongside `adoption_by_cohort` and
`resistance_by_cohort`. This is the **one existing precedent in the entire project** for keeping
what is true apart from what is believed, and the model specified here is a generalisation of it
from campaign claims to propositions of every kind.

The class is declared and never instantiated. `engine.py:112` initialises a separate
`narrative_adoption` dict keyed by cohort id with all values at 0.0, and the `Narrative` model plays
no part in it.

## 2.3 The only belief dynamic

**`CohortAgent.step()`** — `scaffold/backend/app/simulation/agents/cohort_agent.py:28-38`:

```python
if self.cohort.grievances:
    drift = 0.005 + self.model.rng.uniform(0.0, 0.005)
    b = self.cohort.beliefs
    b.government_competence = max(0.0, b.government_competence - drift)
```

Three properties of this code bind the specification. It is **unsigned** — the operator is
subtraction, so no evidence can raise the value. It is **absorbing** — `max(0.0, ...)` pins the
value at zero permanently. And it is **unrecorded** — it mutates a live Pydantic object in place,
emits no event, records no cause, and appears in no snapshot, because `MeridianModel.snapshots`
holds macro dicts only (`engine.py:116`, `:180`).

## 2.4 The diffusion model

**`build_cohort_graph`** — `scaffold/backend/app/simulation/diffusion.py:18-37`. Builds an
`nx.Graph()` at `:24` — **undirected**. Edge weight is the mean `internal_cohesion` of the two
endpoints (`:35`). Population is not a term; audit 5.10 records that `represents_population`
(`agent_schema.py:95`) is read by nothing, so a cohort of 14,200 carries the same weight as one of
620,000.

**`linear_threshold_step`** — `diffusion.py:40-79. Advances a single per-cohort adoption scalar.
Its docstring at `:51` states that "Adoption is monotonic non-decreasing"; audit item 25 notes the
jitter at `:75` does not actually guarantee that. There is no source, no provenance, no truth
comparison and no resistance term in the computation — `resistance_by_cohort` exists only on the
uninstantiated `Narrative` model. The output is read only by the API response
(`routes_simulation.py:75`) and never reaches any belief field or macro indicator.

## 2.5 The visibility construct

**`EventVisibility`** — `agent_schema.py:203-208`: `public` / `classified` / `leaked`. It is the only
role-asymmetry primitive in the project. It is never populated (audit item 20), it is attached to
events rather than to facts or attributes, and there is no authentication or authorisation layer of
any kind against which a "role" could be resolved (audit §7, IAM row).

It must not be extended in place to carry the eight confidence labels. Observability ("who may see
this") and evidential confidence ("how well is this evidenced") are two different axes, and
overloading one enum with both would make each unusable.

> **Amended 19 July 2026.** `EventVisibility` is no longer this document's to give a reader. Under
> founder decision 1A its sole future reader is `M-OBS-EXP`, specified in
> [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5. The two-axis rule
> above is unchanged and is restated by that document (§8): `EventVisibility` is an observability
> axis only, and must stay distinct from the confidence axis in 4.7, which remains here.

## 2.6 The determinism boundary, which genuinely works

**`ActionProposal`** — `agent_schema.py:374-393`, and `llm_gateway.py:35`, which imports it as the
only simulation type in the module. The gateway's header comment (`llm_gateway.py:7-15`) states the
rule plainly and the module obeys it. This is the existing, honoured implementation of "the LLM may
narrate, never author", and every narration path specified in Part 4.9 must route through the same
pattern.

Two caveats the specification must respect. Audit 5.2
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md):118) records that the
guarding test is tautological and cannot detect the regression it is cited as preventing. And the
gateway is a stub returning a lookup table (`llm_gateway.py:42-54`), so the boundary has not yet
been exercised against a real model.

## 2.7 The single shared RNG

**`engine.py:83`** — `self.rng = random.Random(resolved_seed)`, commented "the ONLY source of engine
randomness". Every draw in the system comes off this one stream: `cohort_agent.py:36` (drawn only
when a cohort has grievances), `diffusion.py:75` (once per graph node), `engine.py:135` (once per
tick).

A3 §6 ([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):170-175)
demonstrated the consequence: adding a grievance to the one grievance-free cohort moved
`shipping_throughput_pct_of_baseline` from `0.6080711379477878` to `0.5973599412373322`, purely
because it changed how many draws were consumed per tick. Changing cohort belief *values* by two
orders of magnitude changed macro by exactly nothing. The apparent meso→macro coupling is shared-RNG
contamination, not causality.

This is a hard blocker on the model specified here, and Part 3.4 states why.

---

# Part 3 — Prerequisites this document depends on and cannot satisfy

**None of these are met. Several are not yet scheduled. One conflicts with a recorded architecture
decision and requires an owner ruling.**

## 3.1 P0.4 — the authoritative-state contract (hard dependency)

P0.4 is *"Define the authoritative-state contract across macro/meso/micro"*
([`../../HANDOFF.md`](../../HANDOFF.md):75). Today that contract is implicitly macro-only:
`macro_snapshot()` returns `MacroState.model_dump()` and nothing else (`agents/macro_state.py:49-51`),
and the determinism test asserts exactly one thing, that two runs' macro snapshots match (audit 5.3).

This document takes a **position** on the question P0.4 must settle, and that position must be
confirmed by the owner rather than assumed:

> Five record types are **authoritative state**, and must be snapshotted, hashed and replayed:
> `Proposition` (which carries truth in its `truth_value` field), `Observation` (what reached whom),
> `Belief` (credence records), `InterpretivePrior` (how an entity reads evidence) and
> `DecisionDriver` (what actually drove a decision). Self-understanding, the public profile and the
> player intelligence profile are **derived views**, computed on read, never written, and never part
> of the hash.

That list of five is the whole of the position, and it is stated identically in the Part 4.1 diagram
and the Part 4.1 mapping table. If those three enumerations ever diverge, the owner is being asked to
ratify something the document does not state consistently, and the divergence is the defect.

Note also that there is **no separate world-fact store.** Authoritative truth is carried by
`Proposition.truth_value` (4.2) plus the event log, and by nothing else. An earlier draft of this
document named a `WorldFact` type alongside `Proposition`; it was never specified, and two homes for
the truth layer is precisely the parallel-construct problem 4.2 warns about.

Note the subtlety, because it is easy to get wrong: an entity's belief is *not* a derived view. It
is a fact about the world that a particular entity holds a particular credence, and it must be
recorded as such. "Self-understanding" is a *projection* over that recorded belief set — the subset
whose subject is the entity itself — not a second store.

This document **must not be built on an assumed answer.** If P0.4 rules that meso and micro state
are derived from macro, most of Part 4 is invalid.

## 3.2 P0.6 — event, snapshot and replay foundations (hard dependency)

P0.6 is *"Repair event, snapshot and replay foundations. Central transition mechanism, full
snapshots, replay makes zero model/network calls"* ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.6 (`:87-88`)).

Belief here is specified as event-sourced, so it inherits every part of P0.6. None of the three
parts exists:

- **No central transition mechanism.** `Event` (`agent_schema.py:211-229`) is never instantiated;
  `engine.py:165-173` appends raw unvalidated dicts carrying only `event_id`, `tick`, `type`,
  `actors_involved` and `effects`. `causal_parents` (`:224`) — the declared explainability spine —
  is assigned nowhere (audit item 13).
- **No full snapshots.** No RNG state is captured anywhere (no `getstate` call exists in
  `backend/app`); `derivation` is a frozen constant set once at `engine.py:68` (audit item 16); no
  random draw is ever recorded (audit item 17).
- **No replay.** Nothing is persisted at all. `SimulationRun`, `StateSnapshot` and `EventLog`
  (`db/models.py:23`, `:42`, `:56`) are never instantiated; runs live in a process-local dict
  (`runs.py:18`).

The founder's six questions
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):289-291) are a strict
superset of what `causal_parents` alone could answer. *"What evidence did the entity observe"*
requires per-entity observation records, which nothing has. *"What alternative reactions were
possible"* requires the counterfactual set to be recorded at decision time, which nothing does.

**Belief history is not merely unbuilt. It is unbuildable until P0.6 lands.**

One existing hook is worth naming: `StateSnapshot.meso_state` (`db/models.py:51`, JSON, default
dict) is already declared and written by nothing. It is the natural landing site for entity belief
state, and this specification should extend it rather than introduce a parallel store.

## 3.3 P0.5 — cross-tier causal channels (soft dependency, cohort tier only)

P0.5 is *"Design explicit cross-tier causal channels. No arbitrary coupling.
`represents_population` must affect aggregation"* ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.5 (`:84-86`)).
The cohort-tier belief model in Part 4.8 aggregates upward and therefore sits directly on P0.5's
channel. It must take that channel as given and layer above it, not restate or redesign it. See
[`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md), which is the design successor to that item.

One warning belongs here rather than there. Population-weighted aggregation over the *current*
belief dynamic would **amplify** finding 5.9 rather than expose it: a monotone collapse to zero,
weighted by cohort size, would drag national approval down deterministically and in proportion to
population. Aggregation is only valid on top of a bidirectional belief model. The audit sequences
both in the same phase for this reason
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md):480, `:485`).

## 3.4 Deterministic randomness isolation (hard blocker, owned by P0.4A, conflicts with ADR-007)

> **Corrected 19 July 2026.** This section previously read "in no P0 item". The founder decision of
> 18 July 2026 created **P0.4A — establish a deterministic randomness architecture** as its own
> Phase 0 workstream, ordered `P0.4 → P0.4A → P0.5 → P0.6`
> ([`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md) §P0.4A).
> The mechanism — stateful named substreams or keyed / counter-based deterministic draws — is **not**
> chosen; "substream" below names the problem, not the solution. Isolation is required across five
> axes (subsystem, entity, relationship or interaction, purpose, tick or event context), and
> per-entity streams alone are insufficient. Specification such as this document may proceed;
> world-model materialisation may not, until P0.4A passes.

Nearly every mechanism in Part 4 is stochastic: whether an entity observes an event, how a rumour
distorts in transmission, the jitter in a belief update. On the single shared stream at
`engine.py:83`, every one of those draws shifts every later draw in every other subsystem — the
effect A3 demonstrated numerically
([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):161-163).

The specific failure this creates for the belief model:

> An entity's belief state would depend on **how many other entities happened to hear something
> first**, because draw order is global. Two runs identical in every respect except the order in
> which two unrelated rumours propagated would diverge in macro indicators for reasons unconnected
> to any modelled cause. The existing determinism test would report this as expected divergence
> (A3:174-175).

The requirement is that every stochastic draw in this model be taken from a **named substream** keyed
on stable inputs — run seed, entity id, purpose, tick — so that a draw's value does not depend on
global draw order.

**This conflicts with a recorded architecture decision.** ADR-007
(`scaffold/docs/ARCHITECTURE_DECISIONS.md`:60-67) accepts one seed threaded to one `random.Random`,
and audit item 28 explicitly records that the shared stream "is not currently a defect (the design is
documented as one RNG in ADR-007)". Introducing substreams supersedes an accepted ADR and is
"anything affecting determinism or authoritative state", for which
[`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`) requires human approval.

**No agent may take this decision.** It is raised as an open question in Part 9.

## 3.5 RELATIONSHIP-GRAPH (hard dependency)

Source trust weighting — Part 4.5 — reads a **directional** trust value from the receiving entity
toward the source. Neither existing structure can supply it. `Relationship`
(`agent_schema.py:190-200`) is a single record per pair carrying one shared `trust` and one shared
`valence`; direction is implied only by the field names `agent_a` / `agent_b`.
`MicroAgent.relationships` (`:175-177`) is weaker still: one float per counterpart. Both are
unpopulated, and the demonstration scenario contains no `relationships` key on any of its six
institutional agents.

[`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) specifies the replacement. This document assumes
only the minimum from it: a directional, tick-stamped `trust` value readable as
`trust(holder → source)`, and a record of whether that trust has previously been violated.

## 3.5A Observation and perception (hard dependency, added 19 July 2026)

**Added by founder ownership ruling 1A.** It is numbered 3.5A rather than inserted as a new 3.6 for
the same reason Part 0 is numbered 0: the subsections below it are cited by number.

The update rule in 4.5 fires when "an `Observation` o reaches holder h". Nothing in this document
produces that arrival, and after ruling 1A nothing in it may. Production is
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md), whose `M-OBS-ACQ` is the
sole writer of `Observation` records and whose `M-OBS-EXP` decides which entities are in a position
to observe an event at all.

This document assumes the minimum from it, and nothing more: that an `Observation` arrives at a named
holder, immutable, carrying the fields specified in 4.3, and that whether it arrived at all was a
computed step rather than an assumption. Every mechanism in Part 0's register is inert until that
holds. Its own prerequisites are P0.4, P0.4A and P0.6 — the same three this document already depends
on — so the dependency adds no new Phase 0 item, only a new document between this one and the event
stream.

Two items in that document bear directly on Part 4 and are **not** resolved here, because they are
open questions in the owning document:

- **Its Q3 — where the four acquisition fields live.** `opportunity_id`, `attributed_source_id`,
  `attribution_confidence` and `acquisition_rule_id` either extend the `Observation` class specified
  in 4.3 or are carried alongside it. Until that is ruled on, 4.3's field list is this document's
  consumption view of the record, not a claim to own its schema.
- **Its Q4 — how coarse exposure is at scale.** 4.8 already contemplates cohort-level exposure
  standing in for per-person observation. Where that boundary sits, and what happens when an entity
  is promoted across it mid-run, is that document's question and
  [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md)'s tiering, not this document's to settle.

## 3.6 A role layer, for disclosure only (hard dependency for Part 4.7)

The eight confidence labels are computed per player role. There is no authentication or authorisation
layer anywhere in the project (audit §7, IAM row; item 20). "Player role" today resolves against
nothing — `Intervention.actor_role` (`agent_schema.py:237`) is a free string supplied by the client,
and A3 check 5 drove `"janitor_with_no_authority"` through the real API and received `200
{"accepted": true}` ([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):120-140).

Until a role layer exists, the confidence vocabulary can be specified but cannot be computed for
anybody.

## 3.7 B5 / P0.8 — the dual-use decision: DECIDED, and not thereby cleared

Blocker B5 is *"Dual-use influence-targeting schema with no acceptable-use terms"*. **It was settled
by founder decision on 18 July 2026.** An earlier draft of this section described it as the one
publication blocker requiring an owner decision, citing
[`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):245 and
[`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.8 (`:90`); **both anchors predate the decision and are superseded.**

**The decision did not clear B5 — it changed what clears it.** B5 now clears only when the **eight
controls** the decision names are **implemented and verified**, because control 8 states that
disclosure and any future acceptable-use language are *supplementary* while **technical enforcement
is mandatory**. **None of the eight exists in code.** So B5 is still a publication blocker, and it is
now the most expensive of the five rather than the cheapest.

This document is coupled to it in a specific and directional way. `Campaign`
(`agent_schema.py:320-346`) targets audience attributes; the belief model **is** the mechanism those
attributes are targeted through. Specifically, `messenger.perceived_independence` (`:287-293`) is
meaningless unless something computes belief updates weighted by perceived source independence —
which is precisely Part 4.5. Specifying source-trust weighting in operational detail therefore
enlarges the dual-use surface **the eight controls were written against, none of which is built**.
The coupling is not discharged by the decision; if anything the decision sharpens it, because it
names the enforcement that does not yet exist.

**Two things the decision does settle for this document.** Control 5 — protected characteristics may
never be optimisation criteria for persuasion or manipulation — and the not-permitted identity list
(competence, morality, loyalty, violence, manipulability) bind Part 4.5's weighting terms directly.
A source-trust or susceptibility term may **never** be read off an identity label.

**What it does not settle is how coarse Part 4.5 must stay while the controls remain unbuilt.** That
is Part 9 question 7, restated there against the decided position. **This document applies the
decision; it does not reopen, extend or reinterpret it, and no agent may do so.** It flags the
coupling in Part 4.5 and Part 4.7 and defers to
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md).

## 3.8 Dependency order

Substreams → P0.4 → P0.6 → (belief history, disclosure) and P0.5 → (cohort aggregation). Nothing in
Part 4 is buildable out of that order. Establishing this is a reason to specify carefully, not a
reason to start.

> **Amended 19 July 2026.** One link is inserted, per 3.5A: `M-OBS-EXP` and `M-OBS-ACQ`
> ([`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md)) sit between P0.6 and
> every mechanism in Part 0's register, because belief update consumes a record this document no
> longer produces. The Phase 0 order itself is unchanged; the insertion is a document dependency, not
> a new Phase 0 item.

---

# Part 4 — Technical specification

**Everything below is specified, not implemented.** Schema sketches use Pydantic-v2-style notation
to match the existing schema layer's conventions; they are illustrative shapes, not proposed code.

## 4.1 The four layers, and which of them are state

```text
  ┌──────────────────────────────────────────────────────────────┐
  │  AUTHORITATIVE STATE  (snapshotted · hashed · replayed)       │
  │                                                              │
  │   Proposition        the claim, and its authoritative truth   │
  │   Observation        what reached whom, from whom, when      │
  │   Belief             what an entity holds, and how firmly    │
  │   InterpretivePrior  how an entity reads new evidence        │
  │   DecisionDriver     what actually drove a decision          │
  └──────────────────────────────────────────────────────────────┘
                              │  pure functions, computed on read
                              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  DERIVED VIEWS  (never written · never hashed)                │
  │                                                              │
  │   SelfUnderstanding    projection of Belief onto self        │
  │   PublicProfile        population-weighted aggregate belief  │
  │   IntelligenceProfile  role-scoped, confidence-labelled      │
  └──────────────────────────────────────────────────────────────┘
```

Mapping to the founder's four profile views
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):147-165):

| Founder's view | Specified as |
|---|---|
| Authoritative reality | `Proposition.truth_value` for every claim, plus the full `Observation`, `Belief`, `InterpretivePrior` and `DecisionDriver` records of every entity. There is no separate world-fact store; see 3.1. |
| The entity's self-understanding | A derived projection over that entity's own `Belief` records, restricted to propositions whose subject is the entity. |
| Public profile | A derived, population-weighted aggregate of cohort-tier belief plus the set of publicly asserted claims. |
| Player intelligence profile | A derived, role-scoped view over the player's own `Observation` set, confidence-labelled by the function in 4.7. |

**The invariant:** the derived views must be recomputable from authoritative state alone. If any
view holds information that cannot be recomputed, it has become state by accident and the contract
is broken. Part 8 states this as a test obligation.

## 4.2 Propositions: what beliefs are about

A belief must attach to an identified claim, not a sentence, so that two entities' beliefs about the
same thing are comparable and so that belief can be compared against truth at all.

```python
class PropositionKind(str, Enum):
    fact        = "fact"         # about world state
    attribution = "attribution"  # who caused what
    disposition = "disposition"  # what an entity intends or values
    evaluative  = "evaluative"   # a judgement — NOT truth-apt

class TruthValue(str, Enum):
    true          = "true"
    false         = "false"
    indeterminate = "indeterminate"   # genuinely unsettled in-world
    not_truth_apt = "not_truth_apt"   # evaluative propositions only

class Proposition(BaseModel):
    proposition_id: str
    kind: PropositionKind
    subject_entity_id: str | None      # the entity the claim is about, if any
    topic: str                         # topic tag; scopes interpretive priors
    truth_value: TruthValue            # AUTHORITATIVE. Never LLM-set.
    truth_resolved_at_tick: int | None
    claim_text: str                    # PRESENTATION ONLY — see note
    scenario_authored: bool
```

**Design rules.**

- `truth_value` is authoritative state. Only the engine may set it, and only from recorded world
  state or the event log. It generalises `Narrative.truth_status` (`agent_schema.py:269-271`) from
  campaign claims to propositions of every kind, and that existing field must be folded into it
  rather than left as a parallel construct.
- **`kind == evaluative` implies `truth_value == not_truth_apt`**, enforced as a model validator.
  Evaluative propositions are excluded from the "factually wrong" query in 4.6 by construction. Four
  of the five existing `CohortBeliefs` fields (`agent_schema.py:59-69`) are evaluative in exactly
  this sense, and this rule is what stops the model from asserting that a population is *factually
  wrong* to distrust its government.
- `topic` is load-bearing, not a label. It is what interpretive priors (4.4) scope to. A proposition
  with no topic cannot be differentially interpreted and must be rejected at load.
- `claim_text` is **presentation only** and carries no causal claim. It exists so the LLM has
  something to narrate. It is declared as such here so it is not mistaken for a modelled attribute;
  see Part 7.
- Propositions must be **minted by the engine or authored in scenario data**, never by the LLM. A
  narration surface that wants to introduce a new claim must submit it as a proposal for engine
  validation, exactly as `ActionProposal` (`agent_schema.py:374-393`) does for actions.

**A proposition schema does not exist today.** Nothing in `agent_schema.py` or in the nine published
mirrors under `scaffold/schemas/` resembles it.

## 4.3 Knowledge: observations with provenance

> **Amended 19 July 2026, per founder ownership ruling 1A.** The production of `Observation` records
> is owned by [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md);
> `M-OBS-ACQ` is their sole writer. This document owns their consumption: belief updating (§4.5),
> knowledge storage and confidence labelling (§4.7). The exposure rule contemplated at §4.3 is
> `M-OBS-EXP`. Whether the four acquisition fields extend this class or are carried alongside it is
> open question Q3 in the owning document.
>
> The schema sketch below is retained unchanged. It is now this document's **consumption view** of a
> record it does not write: the fields it names are the fields belief updating and confidence
> labelling read.

An `Observation` must record that a claim reached an entity, and must be **immutable and
append-only.** It is not a belief; hearing is not believing.

```python
class Directness(str, Enum):
    witnessed   = "witnessed"     # the entity was present
    documentary = "documentary"   # the entity read a record
    testimony   = "testimony"     # another entity told it directly
    rumour      = "rumour"        # reached it through an unattributed chain
    inference   = "inference"     # produced by an engine inference rule

class Observation(BaseModel):
    observation_id: str
    holder_entity_id: str
    proposition_id: str
    asserted_value: float          # what the source asserted, 0..1
    directness: Directness
    source_entity_id: str | None   # None for witnessed
    channel_id: str | None         # media/comms channel, if carried by one
    received_tick: int
    origin_event_id: str           # the event that produced this observation
    parent_observation_id: str | None   # the observation this was relayed from
    fidelity: float                # 0..1, how intact the claim arrived
    engine_rule_id: str | None     # required when directness == inference
```

**Design rules.**

- `parent_observation_id` makes provenance a walkable chain. It is what answers *"how did this
  spread?"* and *"who told them that?"* without an LLM reconstructing it.
- `asserted_value` is what the *source* claimed, and is deliberately separate from what the holder
  ends up believing. A distorted relay must record a different `asserted_value` from its parent, so
  that the difference is inspectable rather than silent.
- `directness` must weight the update in 4.5 and is specified as a required input to the confidence
  labelling in 4.7.
- Observations are **never deleted**. Memory decay is modelled on the belief, not by destroying the
  record — the founder requires that formative experience persists
  ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):236-237, :290), and
  `AgentMemory` (`agent_schema.py:143-151`) currently models memory as a decaying list of event ids
  with no experience and no interpretation, which contradicts that.
- **Whether an entity observes an event at all must be a modelled step, not an assumption.**
  Observation must be generated by an exposure rule over the event's visibility, the entity's channel access
  (`MicroAgent.information_access`, `agent_schema.py:178-180`, currently read by nothing), its
  network position and its media exposure. This is the point at which `EventVisibility`
  (`:203-208`) finally acquires a reader — and note that it must remain the *observability* axis
  only, distinct from the confidence axis in 4.7.

  > **Superseded as to ownership, 19 July 2026.** The requirement stands and is unchanged; the
  > mechanism is not this document's. That exposure rule is `M-OBS-EXP`, specified at
  > [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5, which takes the
  > same four inputs and emits an `ObservationOpportunity` per admitted (event, entity) pair. This
  > document states the requirement as a consumer: an `Observation` that did not originate in an
  > admitted opportunity is a defect wherever it is produced.

## 4.4 Interpretive priors: how prior experience shapes reading of new evidence

The founder's causal-value requirement
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):241-271) is that biography
must feed a mechanism. `InterpretivePrior` is the named mechanism through which life history reaches
belief. It is the difference between a biography that changes the simulation and a biography that
produces adjectives.

```python
class InterpretivePrior(BaseModel):
    prior_id: str
    holder_entity_id: str
    derived_from_event_ids: list[str]   # MUST be non-empty
    topic_scope: list[str]              # MUST be non-empty
    evidence_gain: float                # multiplier on evidence strength, bounded
                                        # read by prior_gain(h, topic) in 4.5
    threat_asymmetry: float             # NOT YET COMPUTABLE — see note below and Part 7
    source_class_modifier: dict[str, float]  # per source class, bounded
                                        # NO INSERTION POINT in 4.5 as written — see Part 7
    formed_at_tick: int
```

**Design rules.**

- **Both list fields must be non-empty, enforced at load.** A prior derived from nothing is not
  event-sourced. A prior scoped to nothing applies everywhere and is therefore a personality
  adjective, which is the fake-depth failure mode the founder names as the largest risk.
- Priors modify the *weighting* of evidence, never the *outcome* of a decision. This is where the
  probabilistic-not-deterministic rule
  ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):87-91) is enforced
  structurally rather than by good intentions: a prior can only ever adjust a coefficient inside a
  bounded range, and there must be no code path by which a prior selects an action.
- All multipliers are **bounded away from 0 and from extreme values**. An unbounded gain would let
  one biographical fact dominate all evidence, which is a stereotype switch by arithmetic.
- Worked example, drawn from the founder record (`:264-268`): a recorded event
  `survived-political-violence` produces a prior with `topic_scope = ["internal_security",
  "protest"]` and a raised `evidence_gain`. The mechanism is the one the update rule actually
  consumes: `prior_gain(h, p.topic)` in 4.5 returns a higher multiplier for propositions in that
  topic scope, so this entity's credence in an internal-security proposition moves faster on the same
  evidence than a colleague's. It does **not** select "impose curfew". It changes the belief that a
  decision model then reads.

  This example is deliberately anchored on `evidence_gain` rather than on `threat_asymmetry`, and the
  reason is worth stating plainly, because this is the passage that is supposed to demonstrate that
  biography is causal rather than decorative.

  **`threat_asymmetry` is not currently computable, and specifying it here would be fake depth of
  exactly the kind Part 6 rejects.** Two structures it needs are missing. First, nothing marks a
  proposition or an observation as *threatening*: `PropositionKind` has four values, none
  threat-related, and `topic` is a free tag whose only declared role is scoping priors — so the
  engine has no field to read in order to decide that a reading is threatening, and the asymmetry can
  never fire. Second, the update rule consumes `prior_gain(h, p.topic)`, a function of holder and
  topic only, with no valence argument; an asymmetry between threatening and reassuring readings of
  the *same* proposition is not expressible in it. Closing this needs a valence term on the
  proposition or on the observation's asserted direction, plus an extended
  `prior_gain(h, topic, valence)` signature that 4.5 actually reads. Until that structure is
  specified and the owner has ruled on it, the field is retained as a shape only and is declared in
  Part 7, **not** claimed in Part 5.

**Sensitive identity.** Interpretive priors are the only sanctioned route by which ethnic, cultural
or religious identity may affect belief, and the permitted route is exclusively via *social
experience* — exposure, network composition, channel access, discrimination experienced, solidarity
— never via inherent competence, morality or intelligence
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):298-316;
[`../../CHARTER.md`](../../CHARTER.md):137). The enforceable form of this rule, and the tests for it,
belong to [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md)
and are not settled here. Note also that
`Demographics.religion_majority` and `primary_language` (`agent_schema.py:27-28`) are majority labels
on a statistical aggregate, which cannot express a minority inside a cohort at all.

## 4.5 Belief, and the update rule

```python
class Belief(BaseModel):
    holder_entity_id: str
    proposition_id: str
    credence: float          # subjective probability, held in [ε, 1-ε]
    stability: float         # 0..1, resistance to revision
    salience: float          # 0..1, how active in current decisions
    last_update_tick: int
    supporting_observation_ids: list[str]
    contradicting_observation_ids: list[str]
```

### B5 gate — read before the arithmetic below

**The level of detail permitted in `w_source` is an open owner question, not a drafting choice — and
settling B5 did not answer it.** Part 3.7 records that source-trust weighting is the arithmetic
through which an influence campaign becomes effective, and that specifying it in operational detail
enlarges the dual-use surface **the eight B5 controls were written against, none of which is built**.
The founder decision of 18 July 2026 settled *what* the controls are and bound the weighting terms
(no protected characteristic may be an optimisation criterion; no identity label may set a
susceptibility coefficient) — it said nothing about *how much operational detail* may be specified
before enforcement exists. **Why this gate stays shut when the sibling documents' equivalent gates have opened.**
[`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §10.4, [`PERSON-MODEL.md`](PERSON-MODEL.md) §7,
[`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) Q5 and
[`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) Q6 each record
that their "hold coarse until B5 is decided" instruction is **spent**, because the decision supplies
a substantive bound in its place — the permitted / not-permitted identity list and control 5. **That
reasoning does not transfer to this section, and the difference is not a disagreement between
documents.** Those four defer *identity-attribute detail*, which the decision's lists bound directly.
This one defers *the arithmetic of how a source-trust weighting makes an influence campaign
effective*, which no clause of the decision bounds: an independence term and a corroboration-defeat
rule are not identity attributes and are not made safe by the not-permitted list. The bound the
sibling documents rely on therefore does not exist here, and nothing has replaced the deferral.
Part 9 question 7 asks how coarse it must stay. That question is stated
**here, before the specification**, rather than at the end of the document, because a ruling to hold
this coarse cannot un-write a detailed specification that has already been published.

Accordingly this section is deliberately split:

- **Not gated, and specified in full below:** the signed, floored, bidirectional update rule. This is
  the correction of audit finding 5.9 and carries no dual-use content — it is the part that stops
  beliefs ratcheting, and it is needed whatever B5 rules.
- **Gated, and deliberately held at the level of a named function:** how source weight is computed.
  The factors it must consider are named so the schema fields have declared readers, but the
  arithmetic combining them — in particular the perceived-independence term and the
  corroboration-defeat rule — is **deferred to a B5-gated annex.** B5 has been decided (18 July
  2026); the annex nonetheless stays unwritten, because the gate was never really waiting on the
  *policy* — it is waiting on the **enforcement**, and none of the decision's eight controls is
  built. **The annex must not be written until the owner rules on Part 9 question 7 as restated.**

An earlier draft of this document specified that arithmetic in full while simultaneously warning
against doing so. That was the defect this gate exists to prevent.

### The update

When an `Observation` o reaches holder h about proposition p, the engine — and only the engine —
must compute:

```text
w_source   = source_weight(h, o)     # B5-GATED. Named, not decomposed. See gate above.
                                     # Factors it must consider, and no others without
                                     # an owner ruling:
                                     #   trust(h → o.source)      directional; RELATIONSHIP-GRAPH
                                     #   channel_credibility(h, o.channel)
                                     #   directness_weight(o.directness)
                                     #   o.fidelity
                                     #   a provenance-independence term  [DEFERRED — B5 annex]
                                     # Bounded strictly within (0, 1]; never 0, so no source
                                     # is infinitely discounted.

congruence = 1                            if support(h, p, d) > 0
             c                            otherwise, where RESISTANCE_FLOOR ≤ c < 1
                                          (see "What congruence is measured against", below)

gain       = k × w_source × congruence × (1 − stability) × prior_gain(h, p.topic)

Δcredence  = gain × (o.asserted_value − credence)

credence'  = clamp(credence + Δcredence, ε, 1 − ε)
```

### What congruence is measured against

`congruence` is the most dangerous coefficient in the model, so its trigger condition must be
decidable from named, schema-backed quantities rather than from an informal phrase. An earlier draft
defined it against "h's prior commitments", which named no field in any schema here — and which, if
read as the holder's current credence on p, is degenerate: `sign(o.asserted_value − credence)` points
away from current credence by construction, so every observation would be uniformly congruent or
uniformly incongruent and the resistance mechanism would never discriminate.

The specified definition measures congruence against the holder's **other** commitments, via a
declared relation between propositions:

```text
PropositionLink                     # authoritative; engine- or scenario-authored, never LLM
    from_proposition_id: str
    to_proposition_id: str
    alignment: float                # ∈ [−1, 1]. +1 = believing one supports the other;
                                    # −1 = believing one undermines the other.
                                    # alignment(p, p) ≡ 1. An absent link ≡ 0.

commitment_set(h) = { beliefs b of h : b.stability ≥ COMMITMENT_STABILITY_THRESHOLD }

d = sign(o.asserted_value − credence(h, p))      # the direction o would push p

support(h, p, d) = d × Σ  alignment(p, q) × (credence(h, q) − 0.5) × stability(h, q)
                        over q ∈ commitment_set(h)
```

An observation is **congruent** when `support > 0` — that is, when moving p in the direction the
observation asserts would increase agreement with the entrenched beliefs the holder already has —
and **incongruent** otherwise, in which case it is discounted by `c`, floored at `RESISTANCE_FLOOR`.

This is decidable, and it is not degenerate: the sign depends on which side of 0.5 each commitment
sits and on how entrenched it is, not on p's own current credence alone. Where p is itself in the
commitment set, the `alignment(p, p) ≡ 1` term supplies ordinary motivated reasoning — a firmly held
belief resists evidence against it — without a special case. **This is the term Part 4.9's
self-serving-belief claim is derived from**, and it must remain strong enough to derive it: if the
definition is ever changed, 4.9 must be re-checked against it, because 4.9 cites it as the sole
mechanism and specifies no fallback.

`PropositionLink` is a new authoritative structure with an unresolved authoring vocabulary; it is
declared in Part 7 for that reason.

**Every clause below is load-bearing, and each is there for a stated reason.**

- `(o.asserted_value − credence)` is **signed**. Belief moves toward what the evidence asserts,
  in either direction. This is the direct correction of the unsigned subtraction at
  `cohort_agent.py:38`.
- `clamp(..., ε, 1 − ε)` keeps credence in an **open interval**. No belief may reach 0.0 or 1.0, so
  no belief may become unrevisable. This is the direct correction of `max(0.0, ...)` at the same
  line, and it satisfies the audit's Phase 4 exit criterion at
  [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md):484.
- `congruence` implements **resistance**: evidence that cuts against a prior commitment is
  discounted. `RESISTANCE_FLOOR` must be strictly greater than zero and must be a declared,
  tested constant. Without that floor, an entrenched belief becomes unrevisable and the ratchet
  returns in disguise. **This is the most dangerous coefficient in the model and must be treated as
  such.**
- `(1 − stability)` is why long-held, identity-linked beliefs move more slowly than casual ones. It
  is also the second way this model could reproduce finding 5.9, and it is specified in full below
  for that reason.
- `trust(h → o.source)` is **directional**. A distrusting B does not imply B distrusting A. The
  existing single-`trust` pair record (`agent_schema.py:196`) cannot express this; see 3.5.
- The provenance-independence term is where `CampaignMessenger.perceived_independence`
  (`agent_schema.py:287-293`) would eventually acquire a reader. **This is the specific point of
  coupling to blocker B5** — it is the arithmetic that makes an influence campaign effective — and it
  is therefore named but **not specified** here, per the gate above.
- **Corroboration must not be counted naively.** Two observations sharing a `parent_observation_id`
  ancestry are not independent evidence, and repetition must not function as confirmation, or a
  coordinated amplification network becomes arbitrarily persuasive by volume alone. This is stated as
  a **design constraint the eventual rule must satisfy**; the rule itself is deferred to the B5-gated
  annex, because a specification of how amplification is defeated is also a specification of how it
  works.

### `stability`, and why it needs its own bound

`stability` is a multiplier on the same `gain` that `RESISTANCE_FLOOR` and `ε` exist to protect, and
it can defeat both: as `stability → 1`, `gain → 0` regardless of either constant, and the belief
becomes unrevisable by a route neither Part 8 test 1 nor test 3 would catch. Naming that hazard
without closing it — as an earlier draft did — leaves the anti-ratchet guarantee incomplete. It is
therefore specified on the same footing as the other two constants:

- **Bounded.** `stability ≤ 1 − δ`, with `δ` a declared, tested constant strictly greater than zero,
  exactly as `ε` bounds credence. This is what makes Part 8 test 3's phrase "the most entrenched
  belief the model permits" refer to something declared rather than assumed.
- **Updatable, and able to fall.** Sustained disconfirmation must reduce `stability`. Inputs to the
  update are: accumulated contradicting evidence weight since the last rise, `salience`, and the age
  of the belief. Confirmation and age may raise it, bounded by `1 − δ`; disconfirmation must lower
  it. A `stability` that can only rise is a second absorbing state through the back door.
- **May be initialised by biography, never fixed by it.** [`PERSON-MODEL.md`](PERSON-MODEL.md) may
  set an entity's initial `stability` from its history. It must never pin it. Part 4.4 bounds every
  `InterpretivePrior` multiplier away from extremes precisely so that one biographical fact cannot
  dominate all evidence; an authored `stability` at its bound would evade that rule and make an
  entity permanently unpersuadable **by authorship rather than by evidence** — identity mechanically
  determining behaviour, which the founder record forbids
  ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):87-91).

### Salience, decay and forgetting

`salience` must decay per tick and must be refreshed by new observations and by the belief being
used in a decision. Its specified mechanisms are: (a) gating which beliefs enter an entity's decision
context, so an entity is not modelled as reasoning over its entire belief set every tick, and (b)
determining which beliefs surface in the dossier's "current concerns" panel. Both mechanisms are
themselves unbuilt — see the `Belief.salience` row in Part 7, which records that no decision model
exists to gate.

**Decay applies to salience, never to credence, and never to the observation record.** A belief that
stopped being talked about is not a belief that was abandoned. This is a deliberate departure from
`AgentMemory.decay_rate` (`agent_schema.py:149-151`), which decays remembered event ids and would
make formative experience expire.

### Every update must emit an event

Each belief change must emit a `BeliefUpdated` event carrying: holder, proposition, prior credence,
new credence, the observation id that caused it, every coefficient used, the interpretive prior ids
applied, and the substream and draw index of any random component. This is what makes the founder's
six questions answerable and what makes replay possible. It is also the reason this work sits
strictly downstream of P0.6 (see 3.2), and the reason it must **not** follow the current pattern at
`engine.py:163-173`, which logs only non-empty deltas, records intent rather than realised outcome
(audit item 15), and discards rationale entirely (item 12).

## 4.6 The query: "what does this person believe that is factually wrong?"

Specified as a pure function over authoritative state, computed on read, never stored:

```text
factually_wrong(entity) =
    for each Belief b held by entity:
        p = proposition(b)
        include if  p.kind != evaluative
                and p.truth_value in {true, false}
                and |b.credence − truth_as_scalar(p)| > DIVERGENCE_THRESHOLD
        ordered by  b.salience × divergence
        each row carrying: the observations that produced the belief,
                           the source of each, and the tick it arrived
```

**Design rules.**

- Evaluative propositions are excluded by construction. The system may report that a minister
  believes the strait was closed deliberately when it was not; it must never report that a
  population is factually wrong to think the government incompetent.
- `indeterminate` propositions are excluded. Being confident about a genuinely unsettled question is
  overconfidence, not error, and conflating the two would manufacture certainty
  ([`../../CHARTER.md`](../../CHARTER.md):56).
- Every row must be **explainable to its source observations.** A row with no supporting observation
  is a bug, not a mystery — it would mean a belief exists that nothing produced.
- This function is specified to read authoritative reality, and would therefore be available to the
  designer and to tooling. It must **not** be automatically available to a player. What a player sees is the disclosure view in 4.7,
  and no player role may be granted a direct read of `truth_value` without an explicit owner
  decision recorded against the role model. Otherwise the intelligence product collapses back into
  the omniscient encyclopaedia the founder record rejects (`:165`).

## 4.7 Confidence and source tracking: the eight labels

The eight labels from
[`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):157-159 are a property of
the **disclosure view**, not of the world and not of anyone's belief. They are computed
**per attribute**, not per entity, by a deterministic function over the viewing role's own
observation set. They are never stored, never hashed, and never chosen by the LLM.

> **Retained here, 19 July 2026.** Founder ownership ruling 1A assigns observation and perception to
> [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md); the labels below are
> **not** part of that transfer, and that document (§4) excludes them explicitly. They are `M-BEL-CONF`
> in Part 0's register. They must not be confused with that document's *observation confidence at
> acquisition* (its §3, item 8), which is an evidential property of how a single observation was
> acquired.
> The labels here are computed over a role's whole observation set, per attribute, and neither
> quantity may be derived from the other without an owner ruling.

Three axes must be kept apart, and today the project has one enum being asked to cover two of them:

| Axis | Question | Where it lives |
|---|---|---|
| Observability | May this role see it at all? | `M-OBS-EXP`, [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5, reading `EventVisibility` (`agent_schema.py:203-208`) extended to facts and attributes. **Amended 19 July 2026:** this axis is no longer owned here |
| Credence | How firmly does the entity hold it? | `Belief.credence` (4.5) |
| Evidential confidence | How well evidenced is what this role has? | The eight labels below |

| Label | Assignment rule (specified) |
|---|---|
| **Confirmed** | ≥2 provenance-disjoint observations in the role's set, each `witnessed` or `documentary`, with no contradicting observation of comparable weight. |
| **Reported** | ≥1 observation asserts it; independence or corroboration is not established. |
| **Assessed** | Not directly observed. Produced by a named engine inference rule over the role's observations. The rule id must be shown with the label. |
| **Disputed** | The role's set contains conflicting assertions whose aggregate weights fall within a declared margin of each other. |
| **Unknown** | The attribute is in scope for this dossier and the role's set contains nothing bearing on it. **Must be displayed, not hidden** — an absent field and an unknown one are different statements. |
| **Possibly deceptive** | ≥1 contributing observation traces to a source with a recorded deception act, or to a messenger whose asserted independence is contradicted by authoritative reality. |
| **Outdated** | The newest contributing observation predates the most recent authoritative change to the underlying fact by more than a declared staleness horizon. **The player is told the basis is stale; never what changed.** |
| **Restricted** | The attribute exists and this role is not cleared for it. |

**Design rules and cautions.**

- Labels must be computed from the role's own `Observation` set. A role that has observed nothing
  must receive `Unknown` everywhere. That is the specified behaviour rather than a degenerate case,
  and it is what would make the interface an intelligence product rather than an encyclopaedia.
- **`Outdated` requires care.** Computing it needs the engine to know the underlying fact changed —
  which is knowledge the role does not have. The label must leak the *existence* of a change and
  nothing about its content, and the rule must be tested for that.
- **`Restricted` leaks by existing.** Showing "Restricted" tells the player there is something there.
  For some roles that is correct; for others the attribute should render as `Unknown` and be
  indistinguishable from absence. **This is a genuine design decision with a security character and
  is left open in Part 9.**
- Labels must never be produced by the LLM. If a briefing says "confirmed", that word must have come
  from a computed label passed into the prompt as data, not from the model's own assessment. This
  requires a test, because it is exactly the kind of boundary violation that reads as fluent prose.
- The labels' honesty depends on the provenance chain in 4.3 being complete. If observations can be
  minted without a parent, "Confirmed" becomes forgeable — and note that the current decision
  endpoint already permits a client to mint event identifiers and assert its own verdict
  (audit 5.11; A3 check 5). The wire model must be split from the state model before any of this
  becomes trustworthy.

## 4.8 Cohort-tier belief and the diffusion model

Tier-4 cohorts ([`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md)) cannot carry per-person
observation records. The specified compromise:

- A cohort holds, per proposition, a **distribution** rather than a scalar: at minimum
  `(mean_credence, dispersion)`. Dispersion is required because a cohort split 50/50 and a cohort
  uniformly ambivalent behave completely differently, and the existing single adoption scalar
  (`engine.py:112`) cannot tell them apart. Its mechanisms are: the fraction of the cohort above a
  mobilisation threshold, and candidate selection for tier promotion.
- The cohort update applies the same signed, floored, bidirectional rule as 4.5, with source trust
  read at the level of channel and messenger rather than per person.
- Exposure replaces per-person observation: `MediaExposure` (`agent_schema.py:42-53`) and
  `NetworkPosition` (`:80-88`) determine what fraction of the cohort receives an observation, which
  is where those two currently-unread structures acquire readers.
- Aggregation upward to macro is **population-weighted**, and belongs to P0.5 and
  [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md). This document must not restate that channel.

**Against the existing diffusion model.** `linear_threshold_step` (`diffusion.py:40-79`) is not an
ancestor of this design so much as a counter-example to it, in four specific ways:

1. Its graph is **undirected** (`diffusion.py:24`), so every social tie is symmetric by
   construction. Influence is not symmetric, and the demonstration data already contains one-sided
   `bridges_to` entries that the builder silently symmetrises.
2. Its documented behaviour is **monotonic non-decreasing** (`:51`). Adoption that cannot fall
   cannot represent a population that stops believing something.
3. It has **no source and no truth**. A cohort's adoption cannot be compared against reality, and no
   one can be shown to be wrong.
4. Edge weight ignores **population** entirely (`:35`), per audit 5.10.

The specified model replaces it rather than extending it. Because its only consumer today is the API
response (`routes_simulation.py:75`), replacement breaks nothing.

## 4.9 Self-understanding, and its divergence from reality

Self-understanding is **not a store.** It is the projection of an entity's own `Belief` records onto
propositions whose `subject_entity_id` is that entity, presented alongside its recorded objectives.

To make the founder's politician example
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):151-152) mechanical rather
than literary, one additional authoritative record is required:

```python
class DecisionDriver(BaseModel):
    decision_event_id: str
    entity_id: str
    dominant_objective_id: str      # which objective actually prevailed
    dominant_pressure_id: str       # identified reference into a declared pressure
                                    # taxonomy — NOT free text. Taxonomy undefined; Part 7.
    considered_alternatives: list[str]   # CHARTER question 7
    tick: int
```

`DecisionDriver` must be recorded by the engine at the moment of decision. It is specified as the
answer to CHARTER questions 2, 3 and 7 ([`../../CHARTER.md`](../../CHARTER.md):118-127) for entity
behaviour, and it is
the existing `Outcome.explanation_trace` idea (`agent_schema.py:363-365`, "Ordered causal steps
(data, not LLM prose)") given a machine-readable shape — the current `list[str]` cannot answer which
rule applied or what alternatives existed.

The divergence the founder describes is then a comparison of three recorded values:

| Record | Content in the worked example |
|---|---|
| `DecisionDriver.dominant_objective_id` | `retain-office` |
| The entity's own belief about its motive | high credence on `acted-in-national-interest` |
| Other entities' beliefs about the same decision | high credence on `acted-opportunistically` |

**Design rules.**

- `dominant_pressure_id` is an **identified reference, never a free-text string.** An earlier draft
  declared it as `str`, which made it a stored prose attribute on an authoritative record that the
  LLM is forbidden to write — the same failure Part 6 rejects twice, and a conspicuous one on a
  record whose whole purpose is to be machine-readable. The pressure taxonomy it references does not
  exist in any document; it is declared in Part 7 alongside `source_class_modifier`, whose vocabulary
  gap is identical.
- The entity is **not** lying. Its self-belief is authoritative as a belief and was formed by the
  same update rule from the observations available to it — including the ones it generated itself.
- Self-serving self-belief must arise from the **congruence** term in 4.5, not from a special case.
  Concretely, under the definition in "What congruence is measured against": a firmly held
  self-belief such as `acted-in-national-interest` sits in the entity's own `commitment_set` once its
  `stability` passes `COMMITMENT_STABILITY_THRESHOLD`, so an observation pushing that credence up
  yields `support > 0` and is taken at full weight, while one pushing it down is discounted to `c`.
  No "self-deception" flag is required, and none is specified. **This is the only mechanism specified
  for the founder's politician example**, so if the congruence definition changes, this claim must be
  re-derived rather than assumed to survive.
- Mechanism, so this is not decoration: an observable mismatch between an entity's stated rationale
  and its recorded behaviour is itself observable to *other* entities, generating observations that
  lower trust on the directional edge and change how that entity's future assertions are weighted.
  Hypocrisy is intended to carry a cost, and that cost is intended to be computed rather than
  narrated.
- The dossier's self-understanding panel is generated by comparing recorded values. **An LLM may
  phrase the comparison. It may not perform it.**

## 4.10 The determinism boundary — beliefs are authoritative state

This section restates the one rule in this document that is not open to negotiation. It is the
entity-layer application of [`../../CHARTER.md`](../../CHARTER.md):37-44 and ADR-006
(`scaffold/docs/ARCHITECTURE_DECISIONS.md`:50-58).

**The LLM may:**

- read a disclosure view (4.7) and narrate it as a briefing, biography or dossier passage;
- explain a recorded belief chain conversationally, using recorded events, observations and
  coefficients as its source material;
- propose an action, exactly as `ActionProposal` (`agent_schema.py:374-393`) already permits;
- **select among propositions the engine has already minted** — for instance, to choose which
  existing claim a narrated conversation refers to. Selection carries no authority to create.

**Removed from this list, deliberately.** An earlier draft also permitted the LLM to "propose a
*candidate* proposition or observation, which the engine validates, mints or rejects". That
permission is withdrawn, for three reasons that cannot all be satisfied at once:

- 4.2 states that `truth_value` may be set by the engine **only from recorded world state or the
  event log**. A claim the LLM has invented has, by construction, no antecedent in recorded world
  state, so the engine has no oracle against which to validate it. Either every such proposal is
  rejected — making the permission dead — or the engine originates a truth value on the LLM's
  prompting, in which case the LLM decides which facts exist in the world by choosing which claims to
  submit. [`../../CHARTER.md`](../../CHARTER.md):37-40 forbids exactly that: "Generated narrative
  alone must never alter authoritative state."
- The `ActionProposal` analogy does not transfer. ADR-006 works because the engine holds an
  independent legality and pricing rule set and treats proposal numerics as advisory. No equivalent
  adjudication rule exists for propositions, and none is specified here.
- It contradicts Part 8 invariant 7, which requires that belief, observation and proposition types
  not be importable from the gateway module. A gateway that may return a candidate proposition either
  imports a proposition type — failing invariant 7 — or returns an untyped blob, defeating the
  validation the permission depended on.

If a claim-introduction path is genuinely wanted, it needs an adjudication rule stating what evidence
in recorded state licences a `truth_value`, and a named boundary type permitted to cross the gateway.
Both weaken ADR-006, so both are an owner decision: **Part 9 question 10.**

**The LLM must never:**

- write or alter a `credence`, `stability` or `salience`;
- create a `Proposition`, set or change a `truth_value`;
- create an `Observation` or alter its provenance;
- assign a confidence label;
- resolve a `Disputed` state, or decide which of two conflicting reports is correct;
- create or modify an `InterpretivePrior`.

**Structural enforcement, matching what already works.** `llm_gateway.py:35` imports exactly one
simulation type, and the module header (`:7-15`) states why. The belief layer must be unreachable
from that module in the same way: no belief, observation or proposition type may be importable there.
Any narration surface must take a read-only, already-computed disclosure view as input and return
text plus, at most, proposal objects carrying no authority.

**The guard must not be tautological.** Audit 5.2
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md):118) records that the
existing boundary test cannot detect the regression it is cited as preventing. The belief-layer guard
must be written to fail if a belief type becomes importable, and that failure must be demonstrated
once, deliberately, before the test is trusted.

**Why this matters more here than elsewhere.** A fluent model asked "what does this minister believe?"
will produce an excellent answer whether or not the belief state exists. Of every subsystem in
MERIDIAN, this is the one where a fabricated output is least distinguishable from a computed one.
That is precisely why the boundary must be structural rather than behavioural.

## 4.11 The eight questions, applied to a belief change

[`../../CHARTER.md`](../../CHARTER.md):118-127 applies to a belief change exactly as to any other
state change.

| CHARTER question | Answered by |
|---|---|
| 1. What happened? | `BeliefUpdated` event: holder, proposition, prior and new credence |
| 2. What caused it? | The causing `Observation`, and its `origin_event_id` |
| 3. Which rule or mechanism applied? | The update rule id, plus every coefficient recorded on the event |
| 4. Which actors reacted? | Every `BeliefUpdated` event sharing the same `origin_event_id` |
| 5. What assumptions were used? | The `InterpretivePrior` ids applied, each traceable to its source events |
| 6. What uncertainty existed? | `credence` before and after; source independence; `fidelity` |
| 7. What alternative outcomes were possible? | `DecisionDriver.considered_alternatives`; the recorded substream and draw index |
| 8. What future options changed? | Beliefs are inputs to decision gating; the change in the gated set is computable |

Question 7 deserves a note. It cannot be answered by recording an outcome after the fact — the
alternative set must be recorded **at decision time**, because reconstructing it afterwards is
inference, not evidence. Nothing in the current engine records it.

---

# Part 5 — Mechanism map: every specified attribute and what it feeds

Per the founder's first design principle
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):241-254), each attribute
must connect to at least one named mechanism that changes simulation behaviour. Audit 5.10 is the
empirical case for enforcing this strictly: `represents_population` is declared, read by nothing,
and wrong by 63x in the demonstration data — and because nothing read it, being wrong produced no
symptom at all.

**Proposed rule, for owner ratification:** an attribute with no named reader is **struck**, not
deferred.

> **Amended 19 July 2026.** The `Observation.*` rows below are retained and unchanged, but they now
> name **consumption** only: each states which of this document's mechanisms reads the field. The
> records themselves are written by `M-OBS-ACQ`
> ([`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md)), per founder
> ownership ruling 1A. A reader named here is therefore evidence that this document consumes the
> field, and is not a claim on the field's definition. Part 0's register applies the same
> named-reader test one level up, to the mechanisms themselves.

**Completeness statement.** Every field of every schema sketch in Part 4 appears either in the table
below or in Part 7, with one declared exemption: **identifier fields** that name the record itself or
its owner (`proposition_id`, `observation_id`, `prior_id`, `holder_entity_id`, `entity_id`,
`decision_event_id`, and the foreign keys linking a record to its subject). Those are structural
keys, not modelled attributes, and the striking rule does not apply to them. Note that tick stamps
are **not** exempt — each is listed with the mechanism that reads it, because a tick stamp nothing
compares against is exactly the kind of plausible-looking dead field this part exists to catch. This
statement exists because an
earlier draft of this document left five fields — `truth_resolved_at_tick`, `scenario_authored`,
`received_tick`, `last_update_tick` and `formed_at_tick` — appearing only in their schema sketch,
listed in neither table. That is the precise shape of audit 5.10, which this part cites as its own
justification: `represents_population` was declared, read by nothing, and wrong by 63x with no
symptom, because nothing read it. A mechanism map with silent exemptions cannot detect the failure it
exists to detect.

| Attribute | Named mechanism it feeds |
|---|---|
| `Proposition.kind` | Gates the "factually wrong" query (4.6); enforces `not_truth_apt` for evaluatives |
| `Proposition.truth_value` | The divergence comparison in 4.6; outcome divergence when an entity acts on false belief |
| `Proposition.topic` | Scopes `InterpretivePrior` application in the update rule (4.5) |
| `Proposition.subject_entity_id` | Selects the self-understanding projection (4.9) |
| `Proposition.truth_resolved_at_tick` | The `Outdated` label (4.7): it is the "most recent authoritative change" that the newest contributing observation is compared against |
| `Proposition.scenario_authored` | Load-time validation that every proposition was engine-minted or scenario-authored, never LLM-introduced (4.2, 4.10) |
| `PropositionLink.alignment` | The `support()` term that decides congruence in 4.5 |
| `Observation.asserted_value` | The `(asserted − credence)` term in the update rule |
| `Observation.directness` | `directness_weight` in `w_source`; input to `Confirmed` labelling |
| `Observation.source_entity_id` | Looks up directional trust on the relationship edge |
| `Observation.channel_id` | Channel credibility term; cohort exposure fraction (4.8) |
| `Observation.parent_observation_id` | The provenance walk ("who told them that?"); `Confirmed` labelling's provenance-disjointness test (4.7); Part 8 invariant 9. It is also the input to the deferred independence term — that use is B5-gated and is **not** claimed here |
| `Observation.fidelity` | Multiplier in `w_source`; records rumour distortion |
| `Observation.origin_event_id` | CHARTER question 2; groups simultaneous reactions for question 4 |
| `Observation.engine_rule_id` | Required for `Assessed` labelling; CHARTER question 3 |
| `Observation.received_tick` | The `Outdated` label (4.7): the staleness horizon is measured from the newest contributing observation's `received_tick`; also orders the provenance walk |
| `Belief.credence` | Decision gating; divergence query; aggregation to cohort and macro |
| `Belief.stability` | `(1 − stability)` in the update gain; membership of `commitment_set(h)` and the weighting inside `support()` (4.5) |
| `Belief.last_update_tick` | Salience decay is computed from ticks elapsed since last update; orders the belief history for replay reconstruction (Part 8 test 4) |
| `Belief.salience` | Gates which beliefs enter the decision context; drives "current concerns" |
| `Belief.supporting/contradicting_observation_ids` | Explanation trace; `Disputed` labelling |
| `InterpretivePrior.evidence_gain` | `prior_gain(h, p.topic)` in the 4.5 update rule — the one prior-derived term the formula currently consumes |
| `InterpretivePrior.topic_scope` | Restricts where the prior applies; load-time rejection if empty |
| `InterpretivePrior.derived_from_event_ids` | Event-sourcing guarantee; CHARTER question 5 |
| `InterpretivePrior.formed_at_tick` | Orders competing priors on the same topic; establishes that a prior predates the belief it weights, which Part 8 test 4's replay reconstruction requires |
| `DecisionDriver.dominant_objective_id` | Self-understanding divergence (4.9); CHARTER question 2 |
| `DecisionDriver.considered_alternatives` | CHARTER question 7 |
| `DecisionDriver.tick` | CHARTER question 1 ("when"); orders a decision against the observations available at that tick, which is what makes the 4.9 divergence comparison well-defined |
| Cohort `dispersion` | Materialisation sampling for tier promotion ([`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) §5.5) |
| `RESISTANCE_FLOOR` | Guarantees no incongruent evidence is discounted to nothing — the anti-ratchet constant |
| `ε` (credence bound) | Guarantees no absorbing state; satisfies the audit's Phase 4 exit criterion |
| `δ` (`stability` bound) | Guarantees `gain` cannot be driven to zero via `stability`; closes the second route to an absorbing state (4.5) |
| `COMMITMENT_STABILITY_THRESHOLD` | Selects `commitment_set(h)`, which congruence is evaluated against (4.5) |

Two fields that appeared in this table in an earlier draft have been moved to Part 7, because the
mechanisms claimed for them do not exist in the specification as written:
`InterpretivePrior.threat_asymmetry` (no computable trigger — nothing marks a reading as threatening,
and `prior_gain` takes no valence argument) and `InterpretivePrior.source_class_modifier` (no
insertion point — `w_source`'s factor list does not contain a source-class term). Part 5 is offered
as the evidence that the causal-value test was actually applied; a row naming a reader that does not
exist would weaken the warrant of every other row in it.

---

# Part 6 — Rejected as fake depth

Each of the following was considered and is **rejected**, because no mechanism could be named for it.
Recording the rejections is part of the specification: it is the evidence that the causal-value test
was actually applied rather than asserted.

| Rejected | Why |
|---|---|
| A free-text "worldview" or "outlook" field per entity | Produces prose only. The LLM can generate this on demand from `Belief` and `InterpretivePrior` records; storing it would create a second, unfalsifiable source of truth. |
| `emotional_tone` / `mood` per belief | No mechanism reads it. Where affect matters it is already carried by relationship dimensions (fear, resentment) in [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md). |
| A "certainty" field separate from `credence` | Duplicates `credence` and `stability`. Two fields that move together are one field with a synonym. |
| Per-belief "importance to the entity" separate from `salience` | Same reason. One field. |
| Free-text rumour bodies as state | The claim is the `proposition_id`; the wording is presentation. Storing the wording as state invites the LLM to alter meaning by editing text. |
| A "lie detector" or deception-detection scalar | Deception detection must be a computed outcome of contradicting observations and provenance, not a stored attribute. |
| Per-belief "source reliability" cached on the belief | It belongs on the relationship edge, where it is directional and has history. Caching it here would silently fork the truth. |
| A `self_deception_level` flag | Self-serving belief must emerge from the congruence term (4.9). A flag would make it an authored property instead of a modelled outcome. |
| Belief "colour"/tag vocabularies for display grouping | Presentation. Derivable from `Proposition.topic`. |
| Per-entity "IQ", "rationality" or "gullibility" scalar | Rejected on two grounds: no mechanism that is not already covered by `stability` and source weighting, and it invites exactly the essentialist modelling that [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):298-316 forbids. |

---

# Part 7 — Attributes specified whose mechanism is unresolved

These are specified above but **could not be mapped to a mechanism that changes engine state today
or under any currently scheduled work.** They are listed here rather than quietly retained, because
under the rule proposed in Part 5 each one is a candidate for striking, and that is an owner decision.

| Item | Status of its mechanism |
|---|---|
| `Proposition.claim_text` | **Presentation only, by declaration.** Feeds LLM narration and nothing else. Retained because narration needs a referent, and declared non-causal so it cannot be mistaken for a modelled attribute. |
| The eight confidence labels, as a set | Their "mechanism" is **player decision quality**, not engine state. That is only a real mechanism once player actions are gated by what the player knows. Today the intervention path is a no-op that accepts any actor and any action (A3 check 5). Until that is fixed, the labels are an interface feature, not a simulation mechanism. |
| `Restricted` specifically | Requires a role layer. None exists (audit §7, IAM row; item 20). Its display rule is also an open decision (Part 9). |
| `Outdated` specifically | **Computable, and the inputs are named:** the comparison is `Proposition.truth_resolved_at_tick` against the newest contributing `Observation.received_tick`, against a declared staleness horizon. What is unresolved is not the arithmetic but the disclosure policy — the label leaks existence-of-change by design, and the acceptable leakage has not been decided. |
| `Belief.salience` | Mechanism is gating a decision context. **No decision model exists.** `InstitutionalAgent.step()` (`institutional_agent.py:28-40`) passes a three-key stub containing no world knowledge at all, so there is currently no context to gate. |
| Cohort `dispersion` | Two mechanisms are claimed for it. The materialisation-sampling mechanism is specified in [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) §5.5 (dispersion as the sampling parameter for tier promotion), and that document states the requirement in the opposite direction — §5.5's dispersion requirement is an input to *this* document. The mobilisation-threshold mechanism asserted in 4.8 is specified nowhere, here or there: no mobilisation model exists in any document. Both mechanisms are specified-not-implemented, so neither can be validated until both documents are built. |
| `DecisionDriver.considered_alternatives` | Requires alternatives to be enumerated at decision time. Nothing enumerates them; `_validate_and_price` (`engine.py:121-130`) is a dict lookup that receives only the proposal. |
| `InterpretivePrior.source_class_modifier` | **Two gaps, not one.** Its vocabulary is undecided — no document defines a source-class taxonomy. More basically, it has **no insertion point in the arithmetic as written**: `w_source` (4.5) names its factors exhaustively and no source-class term is among them. Adding one is B5-gated, since it is a source-weighting term. Specified as a shape only. |
| `InterpretivePrior.threat_asymmetry` | **No computable trigger and no consumer.** Nothing in the `Proposition` schema marks a claim as threatening, and `prior_gain(h, topic)` takes no valence argument, so an asymmetry between threatening and reassuring readings of the same proposition is not expressible in the 4.5 update rule. Needs a valence term plus an extended `prior_gain(h, topic, valence)` signature before it can be claimed. Retained as a shape; see the note in 4.4. |
| `PropositionLink.alignment` authoring | The `support()` term in 4.5 reads it, so the field has a genuine reader — but **who authors the links, and against what vocabulary, is undecided.** Engine-derived, scenario-authored or both is an owner decision. If left to scenario authors it becomes a large authoring burden; if engine-derived it needs a rule that does not exist. |
| `DecisionDriver.dominant_pressure_id` | Requires a declared pressure taxonomy. No document defines one. The same gap as `source_class_modifier`, and declared here rather than left as the free-text string an earlier draft specified. |
| Self-understanding divergence as a *consequence* | Divergence is displayable immediately, but its stated mechanism — an entity acting on false belief gets outcomes it did not expect — requires expected-versus-realised outcome comparison. No such comparison exists; the event log currently records intent rather than realised outcome (audit item 15). |
| `channel_credibility(h, channel)` | Requires channels to be scenario data. `MediaExposure` (`agent_schema.py:42-53`) hardcodes five channels as schema fields, so channels cannot currently be declared per scenario at all. |

---

# Part 8 — Invariants and test obligations

Specified for whenever this is built. None of these tests exist; the entire current suite is five
tests in one file of 78 lines (audit item 32), and there are no invariant tests at all (item 34).

1. **No absorbing state.** Over a long run, no `credence` sits at 0.0 or 1.0. Directly mirrors the
   audit's Phase 4 exit criterion at
   [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md):484.
2. **Bidirectionality.** For some proposition, some sequence of observations raises a credence that a
   different sequence lowers. This is the explicit anti-5.9 test.
3. **Resistance has a floor.** For the most entrenched belief the model permits — `stability` at its
   bound `1 − δ`, congruence at `RESISTANCE_FLOOR` — sustained contradicting evidence still moves
   credence measurably. Fails if `RESISTANCE_FLOOR` is ever set to zero.

   **Companion obligation — `stability` has a ceiling, and it is not reached.** Over a long run, no
   `stability` reaches `1 − δ`, and some sustained sequence of disconfirming observations lowers a
   `stability` that a confirming sequence raised. Without this, a `stability` that only rises drives
   `gain` toward zero regardless of `RESISTANCE_FLOOR` or `ε`, reproducing finding 5.9 through the
   one term neither constant protects.
4. **Belief is reconstructible.** Replaying an entity's observations from tick 0 through the update
   rule reproduces its stored credence bit-for-bit. This is the oracle that proves belief is genuinely
   event-sourced rather than merely accompanied by events.
5. **Views are derived.** Recomputing every disclosure view from authoritative state alone reproduces
   it exactly. Fails if a view has quietly become state.
6. **Evaluatives are never "wrong".** No proposition with `kind == evaluative` ever appears in the
   output of `factually_wrong()`.
7. **The LLM cannot write belief.** Belief, observation and proposition types are not importable from
   the gateway module. Must be demonstrated to fail once before being trusted (audit 5.2).
8. **Labels are computed.** No confidence label appears in generated text that was not passed in as
   computed data.
9. **Provenance is acyclic and complete.** Every non-witnessed observation has a resolvable parent;
   no cycles.

   **Amended 19 July 2026 — this invariant is now shared, and asserted against records this document
   does not write.** `M-OBS-ACQ` is the sole writer of `Observation`
   ([`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md)), so the test must
   be written against the produced record set rather than against any belief-layer code path. It is
   retained here because the honesty of `Confirmed` (4.7) depends on it: a forgeable provenance chain
   makes `M-BEL-CONF` produce a label it has not earned. Which document's suite owns the test is
   unresolved; see Part 9 question 12.
10. **Determinism under substreams.** Adding a belief-layer draw does not alter any macro indicator.
    This is the regression A3 §6 demonstrated, run as a standing test.

---

# Part 9 — Open questions for the owner

**AI agents may draft records but may not approve decisions**
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)). None of the following is resolved here.

1. **Deterministic randomness isolation versus ADR-007 — narrowed, 19 July 2026.** The placement
   half of this question is **answered**: the founder decision of 18 July 2026 made it a new Phase 0
   item, **P0.4A**, and explicitly ruled out folding it into replay or treating it as a world-model
   detail. What remains for the owner is the **mechanism** — stateful named substreams or keyed /
   counter-based deterministic draws — and the **disposition of ADR-007**, which the drafted
   [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
   (Status *Proposed*, AI-drafted, unapproved) would narrow rather than supersede, while
   `PHASE-0-REMEDIATION-PLAN.md` §P0.4A says supersede. Both sit with `RAID-REGISTER.md` DEC8 and
   `PUBLICATION-EXIT-CRITERIA.md` open question 15. Either choice affects determinism and
   authoritative state and requires human approval
   ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`)). Nothing in this document is buildable until
   P0.4A passes. A3 §6 establishes the current design as a latent reproducibility hazard
   independently of any entity work.
2. **Does P0.4 make belief authoritative state?** This document's position, stated identically in
   3.1 and 4.1, is that exactly five record types are authoritative — `Proposition` (carrying truth
   in `truth_value`), `Observation`, `Belief`, `InterpretivePrior` and `DecisionDriver` — and that the
   four profile views are derived. P0.4 must confirm or reject it. If rejected, Part 4 is invalid.
3. **Is `Restricted` visible?** Displaying it reveals that something exists. Should some roles see
   `Restricted`, and others see the same attribute as `Unknown`, indistinguishable from absence? This
   has a security character, not merely a design one.
4. **May any player role read `truth_value` directly?** A designer or instructor mode plausibly
   should. Granting it to a player role collapses the intelligence product into the omniscient
   encyclopaedia the founder record rejects (`:165`).

   **Confirmed still open and unresolved, 19 July 2026.** The founder ownership rulings of that date
   took **no decision** on this question and expressly retained it as a later owner decision. Four
   things are settled and constrain any future answer; the question itself is not among them:
   authoritative reality exists internally; players ordinarily receive role-, access-, evidence- and
   confidence-filtered projections; there is no automatic omniscient browsing; and a clearance-gated
   projection must **never** be described as a raw ground-truth read. Nothing in this document's
   amendment of 19 July 2026 narrows the question, and no agent may resolve it. The related
   statement in 4.6 — that `factually_wrong()` reads authoritative reality and must not be
   automatically available to a player — stands unchanged and is not an answer to this question.
5. **Is the existing `CohortBeliefs` five-field vector (`agent_schema.py:56-69`) migrated to
   propositions, or retained as a derived summary view over them?** Migration is a breaking change
   to a published mirror (`scaffold/schemas/cohort.schema.json`) with no generator and no sync test
   (audit 5.13).
6. **Ratify the striking rule?** "Any specified attribute with no named reading mechanism is struck,
   not deferred." Audit 5.10 is the empirical case for it. This is a specification-process decision.
7. **How coarse should source-trust weighting stay — restated 19 July 2026, because its original
   trigger has already fired?** The question was originally worded "until B5 is decided". **B5 was
   decided on 18 July 2026, and that did not answer this.** The decision settled the policy — eight
   controls, technical enforcement mandatory — and bound the weighting terms substantively (no
   protected characteristic as an optimisation criterion; no susceptibility coefficient read off an
   identity label). It said nothing about how much operational detail may be written down before
   enforcement exists, and **none of the eight controls is built**. The live question is therefore:
   should Part 4.5 stay coarse until the eight controls are **implemented and verified**? Part 4.5 is
   the arithmetic that makes an influence campaign effective, and specifying it in operational detail
   enlarges precisely the surface those unbuilt controls are meant to cover. **This is an owner
   question. It is not resolved here, and the decision must not be read as permission to resolve
   it.** **It is also stated at the head of Part 4.5, as a gate rather than as an afterthought**, and
   `w_source` is held there at the level of a named function with the independence and
   corroboration-defeat terms deferred to a B5-gated annex. If the owner rules that fuller detail is
   acceptable, the annex can be written; a ruling in the other direction cannot un-write a detailed
   specification, which is why the coarse form is the default.
8. **What is the fate of the strikes in Part 7?** Each is either accepted as a forward-looking
   specification awaiting its mechanism, or struck now. Under the rule in question 6 the default
   would be to strike.
9. **Should the demonstration scenario's real-world religious label be replaced?** `sunni-mixed`
   appears in four of five cohorts (`kestral-strait.json:45`, `:85`, `:168`, `:208`). The founder
   record prefers fictional identities for the default scenario (`:315-316`) and
   [`../../CHARTER.md`](../../CHARTER.md):137 forbids real entities. This couples to
   [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) and is an
   owner decision affecting existing scenario data.
10. **May the LLM ever introduce a new claim?** Part 4.10 withdraws the permission an earlier draft
    granted, because the engine has no oracle by which to validate an invented claim, the
    `ActionProposal` analogy does not transfer without an adjudication rule, and a gateway returning
    candidate propositions contradicts Part 8 invariant 7. Restoring any claim-introduction path
    requires two things the owner must decide: what evidence in recorded state licences a
    `truth_value`, and which boundary type may cross the gateway. Both weaken ADR-006, so both need
    human approval ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`)).
11. **Who authors `PropositionLink.alignment`?** The congruence definition in 4.5 — and therefore the
    anti-ratchet resistance guarantee, the emergent self-serving belief in 4.9, and Part 8 test 3 —
    all rest on this relation. Scenario-authored is transparent but a large authoring burden;
    engine-derived needs a derivation rule that no document specifies. This is a new authoritative
    structure introduced by this revision and should be reviewed as such.
12. **How are the mechanism registers named, and who owns the shared tests? — raised 19 July 2026.**
    Part 0 introduces `M-BEL*` identifiers for this document's six mechanisms, following the `M-OBS*`
    form. Whether the project's registers are unified or bridged by a crosswalk is
    [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) §19 **Q12**, which
    [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5.1 also defers to.
    This document does not take that decision, and the `M-BEL*` identifiers are provisional until it
    is taken. A second, smaller part rides on it: Part 8 invariant 9 asserts a property of records
    this document no longer writes, and which document's test suite owns such shared invariants is
    unsettled. It is raised here so it is not settled by whichever document is built first.

---

**End of specification.** Nothing described above is implemented. This document is BACKLOG and must
not interrupt Phase 0.
