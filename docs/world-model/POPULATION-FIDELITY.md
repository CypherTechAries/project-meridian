# POPULATION FIDELITY — the scale problem, the tier system and population weighting

> # ⚠ SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing in this document exists in MERIDIAN's code.** Not one tier, not one promotion
> trigger, not one weighting term, not one RNG substream. This is a specification of intent for
> a future architecture. Every behavioural sentence below is written in "will", "must" or "is
> specified as" deliberately. Where this document describes something that **does** exist today,
> it says so explicitly and cites `file:line`.
>
> MERIDIAN's defining defect is documentation that claims properties the code does not have. If
> any sentence here reads as a description of working software, that sentence is wrong and should
> be reported as a defect against this document.

**Status:** DRAFT, pending owner review.
**Dated:** 18 July 2026.
**Type:** Backlog specification. Derived from
[`./FOUNDER-REQUIREMENT-2026-07-18.md`](./FOUNDER-REQUIREMENT-2026-07-18.md) (the source record).
**Authority:** Where this document and the source record disagree, the source record is right and
this document is wrong. Where this document and
[`../../CHARTER.md`](../../CHARTER.md) disagree, the charter governs.

**Disposition — read this before acting on anything below.**
This work is **BACKLOG**. The founder was explicit: it **must not interrupt Phase 0 remediation**
(source record lines 5-6 and 340-341; [`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:107-120`)). This
document does not authorise, schedule or begin any implementation. Nothing in it should be
started now. Its only purpose is to capture the requirement precisely enough that the replacement
simulation architecture can be designed against it later, and to record — in one place — which
Phase 0 items it depends on and must not disturb.

**Decision authority.** AI agents may draft this record. They may not approve it, and they may not
resolve any of the questions in §11. Those are owner decisions
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138-140`)).

---

## Contents

1. [Plain-English layer: what problem this solves](#1-plain-english-layer-what-problem-this-solves)
2. [Relationship to P0.5 — who owns what](#2-relationship-to-p05--who-owns-what)
3. [Hard prerequisites — none of which is met today](#3-hard-prerequisites--none-of-which-is-met-today)
4. [What exists today](#4-what-exists-today)
5. [The four fidelity tiers](#5-the-four-fidelity-tiers)
6. [Promotion between tiers](#6-promotion-between-tiers)
7. [Deterministic materialisation and named RNG substreams](#7-deterministic-materialisation-and-named-rng-substreams)
8. [Demotion, retention and re-promotion](#8-demotion-retention-and-re-promotion)
9. [Population weighting](#9-population-weighting)
10. [The causal-value test applied to this document](#10-the-causal-value-test-applied-to-this-document)
11. [Open questions for the owner](#11-open-questions-for-the-owner)
12. [Related documents](#12-related-documents)

---

## 1. Plain-English layer: what problem this solves

MERIDIAN is intended to simulate a society, not a command room. A society has millions of people
in it. It is neither practical nor necessary to simulate all of them in the same detail every
tick, and pretending otherwise would produce a system that is slow, expensive and no more
truthful.

The specified answer is **fidelity tiers**. A small number of people will be simulated in full
detail — cabinet ministers, commanders, journalists, activists, the relative of a hostage. A
larger number will be simulated in substantial but cheaper detail. Households and local networks
will be simulated partly in aggregate, but with named representatives so they are not faceless.
The rest of the population will be represented statistically, as groups.

Two things make this hard, and both are specified in detail below.

**First, people must be able to move between tiers.** Someone who is nobody in particular at
09:00 records a video that reaches two million people by 18:00. The simulation must be able to
turn that statistical background person into a fully detailed individual **on demand** — and the
individual it produces must be the same individual every time. If the player closes the session
and returns, that person must have the same name, the same history, the same face and the same
past. The system must never be able to regenerate a different biography for someone it has already
materialised.

That "same individual every time" requirement is the hard technical problem, and MERIDIAN's
current architecture cannot satisfy it. The engine draws all its randomness from a single generator
(`engine.py:83`, commented "the ONLY source of engine randomness"). Every part of the simulation
draws from that one stream in sequence. (A second generator also exists but is read by nothing
today — see §7.1.) The A3 verification demonstrated — by execution, not by
inspection — that adding or removing a single random draw anywhere silently changes every
subsequent draw everywhere else
([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):170-175).
Generating a person's biography would consume draws. So, on today's architecture, **the national
economy would move because the player looked at somebody.** That is not a tuning problem; it makes
this entire document unbuildable until it is fixed. See §7.

**Second, size must matter — but size must not be the only thing that matters.** A group of
twenty thousand people must not push the national mood around as hard as a group of two million.
Equally, twenty thousand people who own the ports, fund the governing party or control the
refinery must be able to exert influence far beyond their headcount. The specification therefore
separates two different weights — how many people a group contains, and how much leverage it has —
and keeps both visible in the explanation of every outcome. See §9.

---

## 2. Relationship to P0.5 — who owns what

This is the tightest coupling in this document and it is handled first, deliberately.

**P0.5 already exists as a Phase 0 remediation item.** It is worded:

> **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population`
> must affect aggregation. *(Note: this is arguably the highest-value item, since it is the
> product's core mechanism, not a tidiness fix.)*
> — [`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.5 (`:84-86`)

The audit records why it exists. `represents_population` is declared at
`scaffold/backend/app/simulation/schemas/agent_schema.py:95` with a docstring at `:92` reading
"One record stands for `represents_population` citizens", and **no code reads it**.
`scaffold/backend/app/simulation/diffusion.py:25-36` weights influence edges by
`internal_cohesion` alone; `scaffold/backend/app/simulation/engine.py:142` builds the
susceptibility map with no population term. A cohort of 14,200 therefore carries identical weight
to one of 620,000 (audit §5.10, `../delivery/CURRENT-STATE-AUDIT.md`:213-219).

Because the weight is inert, a data error produced no symptom: `coastal-creole-fishing` is set to
`14200` (`scaffold/scenarios/kestral-strait.json:79`) against roughly 900,000 implied by the
project's own planning figures — understated by about 63×, undetected. The five demo cohorts sum
to 1,488,200 (`:39`, `:79`, `:122`, `:162`, `:202`) against a stated 4.1 million, and no
total-population field exists in any scenario or any schema.

**POPULATION-FIDELITY is the design successor to that commitment. It is not a replacement for it,
it does not supersede it, and it must not be read as re-opening it.** The split is:

| Concern | Owner | Status |
|---|---|---|
| Make `represents_population` actually participate in at least one aggregation path | **P0.5 — Phase 0** | **Not started** ([`../../HANDOFF.md`](../../HANDOFF.md):34-38 lists Phase 0 correction as not begun); fifth in the P0.1-P0.8 order. Not this document. |
| Correct the `coastal-creole-fishing` 63× population error in the demo scenario | **Phase 0** (audit §9 Phase 0 work list, `../delivery/CURRENT-STATE-AUDIT.md`:427) | Already assigned. Not this document. |
| Declare a scenario total population so coverage is checkable | **Open** — see §11 Q4 | Neither item currently owns it. |
| Make cohort belief bidirectional and grievances mutable | **Phase 4** (audit §9, `:480`) | Precondition on §9 here. Not this document. |
| The four-tier fidelity model, its cadences and its costs | **This document** | Backlog. |
| Promotion and demotion between tiers | **This document** | Backlog. |
| Deterministic randomness isolation (the prerequisite of deterministic materialisation) | **P0.4A — Phase 0**, created by founder decision of 18 July 2026 and placed between P0.4 and P0.5 | **Not started.** No longer unowned: see [`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md) §P0.4A. **Binding on this document — promotion, demotion and materialisation may not be built until P0.4A passes.** Specification may proceed. See §7 and §11 Q1. |
| Multi-term influence weighting (wealth, organisation, strategic position, political access) | **This document** | Backlog. |
| Aggregation explanation records satisfying `CHARTER.md`:118-127 | **This document** | Backlog. |

**Two warnings to the owner about the seam.**

**(a) P0.5's literal wording admits a narrower reading than the source record requires.**
"`represents_population` must affect aggregation" is satisfied completely by pure
population-proportional weighting. The source record requires the opposite to remain possible:
"a small group may have disproportionate influence through wealth, organisation, strategic
position or political access" (source record lines 137-139). These are not in conflict in intent,
but they are in tension in wording, and P0.5 is sequenced ahead of this document. §9 of this
document specifies population weight as **one term among several**, not as the aggregation rule
itself. If P0.5 were to land as a hard-coded proportional weighting with no extension point, this
document would have to unpick it. **No P0 item has started** ([`../../HANDOFF.md`](../../HANDOFF.md):34-38),
so there is no schedule pressure here: the scoping question can be settled at leisure, before P0.5
begins. This is a flag, not an instruction: **P0.5 remains Phase 0 and this document does not
direct its implementation.**

**(b) Population weighting will amplify the existing belief ratchet, not expose it.**
Audit §5.9 (`../delivery/CURRENT-STATE-AUDIT.md`:205-211) establishes that
`scaffold/backend/app/simulation/agents/cohort_agent.py:35-38` is the entire meso dynamic, that it
is irreversible and absorbing, and that four of five demo cohorts reach `0.0` and stay there
within 100 ticks at seed 88213. Nothing anywhere increases `government_competence`; nothing ever
adds or clears a grievance. Aggregating a monotone collapse upward, weighted by headcount, would
drag national approval down **deterministically and in proportion to cohort size** — producing a
confident-looking national number generated by a defect. Therefore: **the weighting mechanism in
§9 must be specified as valid only against a bidirectional belief model.** Its own precondition is
the audit's Phase 4 exit criterion that "a counter-narrative action measurably raises at least one
cohort's belief" (`../delivery/CURRENT-STATE-AUDIT.md`:485). That criterion is not this document's
to deliver, but this document must not be implemented before it passes.

---

## 3. Hard prerequisites — none of which is met today

Every prerequisite below is currently unmet. They resolve in a fixed order; the chain is not
optional and the items are not independent.

| # | Prerequisite | Owner today | Why this document depends on it |
|---|---|---|---|
| PR-1 | **Deterministic randomness isolation** (this document's "named per-entity RNG substreams" is one candidate mechanism, not the decided one) | **P0.4A**, a Phase 0 workstream created by founder decision of 18 July 2026 and ordered `P0.4 → P0.4A → P0.5 → P0.6`. *(An earlier draft of this row said "Nobody. Not in any P0 item.")* Not started; mechanism unchosen; relationship to ADR-007 an open owner question. **Promotion, demotion and materialisation may not be built until P0.4A passes.** | Materialisation would consume random draws. On the single shared stream (`engine.py:83`) those draws shift every later draw in every subsystem (A3 §6). Without substreams, promotion perturbs macro results and identity is not stable. **This is the hard blocker.** See §7. |
| PR-2 | **P0.4 — authoritative-state contract across macro/meso/micro** | Phase 0, [`../../HANDOFF.md`](../../HANDOFF.md):75 | Tiers must know which of an entity's records is authoritative state and which are derived views. The four-view model (authoritative reality / self-understanding / public profile / player intelligence) is a proposed *extension* of a contract P0.4 has not yet written. This document must not assume a shape for it. |
| PR-3 | **P0.6 — event, snapshot and replay foundations** | Phase 0, [`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:87-88`) | Demotion retains history; re-promotion restores it; the charter's eight questions must be answerable about a promotion. None of that is possible while the engine appends raw unvalidated dicts (`engine.py:165-173`), captures no RNG state, and persists nothing (audit §5.14). |
| PR-4 | **P0.5 — one working population-weighted aggregation channel** | Phase 0, [`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:84-86`) | §9 layers a multi-term influence weight **above** P0.5's channel. It takes that channel as given. |
| PR-5 | **Bidirectional cohort belief and mutable grievances** | Phase 4 (audit §9, `:480`, `:485`) | See §2(b). Weighted aggregation over a monotone ratchet manufactures a confident wrong number. |
| PR-6 | **A declared scenario total population** | Unowned. See §11 Q4. | Weight denominators and tier-4 coverage invariants are uncheckable without it. No such field exists in any schema or scenario. Also blocked behind the missing scenario schema (audit §5.13). |
| PR-7 | **A decision on the agent substrate** | Open owner decision 3 (audit §8, `:405`) | Tier records should not assume `mesa.Agent`. See §11 Q6. |
| PR-8 | **B5 / P0.8 — eight required dual-use controls** | **DECIDED** (founder decision, 18 July 2026). **Not an open decision.** The controls it requires are **unbuilt**, and no P0 item owns them. | Tier 4 cohorts carry the audience-segmentation attributes an influence model targets, and promotion turns those aggregates into named individuals — so the dual-use surface is **larger**, not smaller. B5 now clears by **technical enforcement being implemented and verified**, not by a decision, so this is a prerequisite of the same kind as PR-1: something that must exist before any of this may ship. The binding controls here are **B5-1** (influence mechanics only in fictional worlds), **B5-2** (`world_mode: fictional` required, fail closed), **B5-4** (no real political populations as influence targets — a cohort *is* a political population), **B5-5** (no protected characteristic as an optimisation criterion) and **B5-6** (fictional aggregate diffusion, exposure, adoption and counter-messaging remain **allowed**). Enumerated in [`./ENTITY-ONTOLOGY.md`](./ENTITY-ONTOLOGY.md) §10.4 and [`./PERSON-MODEL.md`](./PERSON-MODEL.md) Part 7. See §6.3, §9.3, §11 Q5 and [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md). |

**Ordering.** PR-1 sits underneath everything. PR-2 precedes PR-3, because what is snapshotted
depends on what is authoritative. PR-3 precedes any retained entity history, and therefore precedes
demotion (§8). PR-4 and PR-5 precede §9. PR-8 no longer gates *how much* identity detail may be
specified — that question was settled with B5 — but its controls must be **built and verified**
before anything specified here is published or shipped, and its permitted / not-permitted line
bounds what may be specified at any level of detail. This ordering is a reason to write the
specification carefully now — it is **not** a reason to start building any of it.

---

## 4. What exists today

Stated exactly, so the boundary between fact and specification stays visible.

**Fidelity tiers do not exist as a concept.** There is no tier field, no tier enum, no promotion
path, no demotion path and no materialisation mechanism anywhere in the codebase.

What exists is **two hard-coded populations**, instantiated in fixed loops in
`scaffold/backend/app/simulation/engine.py:95-108`:

| Existing structure | Location | What it is | Nearest specified tier |
|---|---|---|---|
| `Cohort` | `agent_schema.py:91-109` | A statistical population record. Fields: `cohort_id`, `represents_population`, `region`, `demographics`, `economic_profile`, `media_exposure`, `beliefs`, `grievances`, `influence_susceptibility`, `network_position`. | **Tier 4** only |
| `CohortAgent` | `agents/cohort_agent.py:15-38` | Mesa wrapper. Its entire per-tick behaviour is a one-way grievance-driven decay of `government_competence` (`:35-38`), mutated in place, with no event emitted. | Tier 4 runtime |
| `MicroAgent` | `agent_schema.py:154-184` | An institutional role. No name, no age, no residence, no identity, no family, no life history, no portrait, no location, and no separation between the person and the office. | **Tier 1** only, and thinly |
| `InstitutionalAgent` | `agents/institutional_agent.py:18-41` | Mesa wrapper that asks the LLM gateway for one `ActionProposal` per tick, with a three-key context stub (`:33-37`). | Tier 1 runtime |

**Tier 2 (named secondary individuals) and Tier 3 (households and local networks) have no
representation of any kind.** No schema, no scenario data, no runtime object.

Two existing hooks are worth naming because this specification extends them rather than
introducing parallel structures:

- `StateSnapshot.meso_state` (`scaffold/backend/app/db/models.py:51`) is a declared JSON column
  that nothing writes. It is the natural landing site for tiered entity state.
- `MicroAgent.biography_ref` (`agent_schema.py:166-168`) is the only existing link from structured
  data to a biography. It is set once, to `"bios/oduya.md"`
  (`scaffold/scenarios/kestral-strait.json:268`), and **that file does not exist anywhere in the
  repository**. The field is read by no code. Materialisation must produce structured data, not a
  prose pointer — see [`./PERSON-MODEL.md`](./PERSON-MODEL.md).

The audit is correct that declared-but-unwired structures count in the project's favour: "the
shape of the thing that is missing has already been thought about, and that materially reduces the
cost of building it" (`../delivery/CURRENT-STATE-AUDIT.md`, §3).

---

## 5. The four fidelity tiers

Specified exactly as the source record defines them (lines 217-228). Tier names and membership are
the source record's; cadence, cost and aggregation-loss statements below are this document's
specification and are subject to owner review.

### 5.1 Plain-English summary

- **Tier 1** is the cast. Perhaps a few dozen people who are individually consequential. They are
  simulated every tick, in full, and they are expensive.
- **Tier 2** is the supporting cast. Hundreds of people with real profiles who are simulated when
  something involves them, not continuously.
- **Tier 3** is the social fabric. Families, workplaces, neighbourhoods and professional networks,
  simulated mostly in aggregate but with named representatives so the player can talk to someone.
- **Tier 4** is everybody else. Large populations described statistically.

The point of the tiers is not to save money for its own sake. It is that **simulation effort must
be spent where it changes outcomes.**

### 5.2 Tier 1 — focal individuals

**Membership (source record line 217).** Cabinet members, commanders, executives, journalists,
activists, family representatives, militia leaders and other directly consequential actors.

**Indicative population.** Tens. The specification will set a scenario-declared soft cap
(recommended default: 50) with a named overflow policy, because Tier 1 cost is the dominant term
in per-tick cost and an unbounded Tier 1 will make the tick budget unpredictable.

**What must be simulated.**

| Simulated | Cadence |
|---|---|
| Individual decision model producing proposals | Every tick |
| Full belief and knowledge state, including what the entity believes that is false | Every tick |
| Full directional relationship edges with history | On interaction; decayed on a declared schedule |
| Event-sourced personal history, retained indefinitely | On every state change |
| Current state: location, health, stress, fatigue, financial pressure, confidence, exposure — **attribute set delegated, see note below** | Every tick |
| Stable identity, structured biography and portrait reference | Materialised once, immutable |

**Note on the current-state attribute set.** This document commits to the *cadence* — Tier 1
current state is specified to be recomputed every tick — and to nothing else. The attribute list
above is indicative only. **With the partial exception of `location`, which trigger T5 reads
(§6.2), none of these attributes is mapped to a named simulation mechanism anywhere in this
document, and they are recorded as unmapped in §10.2.** Specifying a per-tick computation with no
declared consumer is precisely the pattern that let `represents_population` sit inert for the life
of the project (audit §5.10). The attribute set and its causal mappings belong to
[`./PERSON-MODEL.md`](./PERSON-MODEL.md), which now exists in DRAFT and is unreviewed; **any attribute it cannot map
to a named reading mechanism must be struck rather than carried forward here** (§11 Q8).

**Cost.** One decision-model evaluation per entity per tick, plus at most one narration call per
emitted proposal. This is the only tier permitted to make a model call on a regular cadence.
Narration must be subject to the same determinism boundary that `ActionProposal` enforces today:
generated text carries no authority to change authoritative state. That boundary is one of the few
things in MERIDIAN that genuinely works today, and this specification must not weaken it.

**But narration cannot be carried by `ActionProposal`, and this document must say so plainly.**
`ActionProposal` (`agent_schema.py:374-393`) is an action-shaped object — `proposing_agent_id`,
`action_type`, `target`, `rationale`, `parameters`, `confidence` — whose docstring states it is
"deliberately NOT a state object". A biography, briefing or dossier narration is not an action and
cannot be expressed as one. Narration will therefore require a **distinct, equally authority-free
gateway return type**. Adding one amends the ADR-006 invariant that `ActionProposal` is the only
type the gateway may return (`scaffold/backend/app/simulation/llm_gateway.py:35`;
`scaffold/CLAUDE.md`, "The one rule you must never break"). That is an architecture change
requiring owner approval ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`)) and is raised as §11 Q11.
It is **not** resolved here.

**What is aggregated away.** Nothing. Tier 1 is the reference fidelity; every other tier is
defined by what it drops relative to Tier 1.

### 5.3 Tier 2 — named secondary individuals

**Membership (source record lines 221-222).** Local officials, employees, relatives, experts and
influential citizens. "Substantial profiles but less expensive continuous simulation."

**Indicative population.** Hundreds.

**What must be simulated.**

| Simulated | Cadence |
|---|---|
| Identity, structured biography, portrait reference | Materialised once, immutable |
| Belief state | Slow cadence (scenario-declared, recommended every *k* ticks) **and** on any event naming the entity |
| Relationship edges | Only to Tier 1 and Tier 2 entities, and to their own Tier 3 group |
| Personal event history | Retained, but only for events the entity was named in or observed |
| Current state | Reduced set: location, availability, financial pressure, loyalty — same delegation and same unmapped status as §5.2; see §10.2 |

**Cost.** No per-tick decision model. Tier 2 entities are **reactive**: they are evaluated when an
event names them, when a Tier 1 entity interacts with them, or on their slow cadence. Model calls
occur only on player engagement.

**What is aggregated away relative to Tier 1.** Continuous intention formation; stress and fatigue
dynamics; relationships to Tier 3 and Tier 4 members other than their own group; the
counterfactual set ("what alternative reactions were possible") for routine ticks — retained only
for evaluated ticks.

### 5.4 Tier 3 — households and local networks

**Membership (source record lines 224-225).** Families, workplaces, neighbourhood groups and
professional networks. "Behaviour partly aggregated while retaining named representatives."

**Indicative population.** Thousands of groups, each standing for a small number of people
(recommended order: 2-500 people per group).

**This tier does not exist in any form today** — no schema, no data, no runtime object. Whether the
default scenario needs it at all is an open owner question (§11 Q7).

**What must be simulated.**

| Simulated | Cadence |
|---|---|
| Group-level aggregate state: income, exposure, insecurity, institutional trust, grievances — `institutional_trust` and `grievances` feed §9 aggregation and the T3/T5 triggers; `income`, `exposure` and `insecurity` are **not** mapped to a named mechanism here (§10.2) | Every tick, vectorised; no per-member arithmetic |
| **Named representative** — one materialised individual per group, held at Tier 2 or Tier 4 detail | Materialised on first need |
| Directional edges to the cohort above and to the Tier 1/2 entities its representative knows | On change |
| Group event history | Retained at group granularity, not per member |

**The named representative must be a mechanism, not decoration.** It is specified to exist because
it must serve three functions: (a) it must be the promotion candidate when the group produces
someone consequential (§6); (b) it must be the endpoint of relationship edges, so that a Tier 1
minister can have a real constituent rather than an abstraction; and (c) it must be the
transmission point for a grievance from a lived event into the belief model. A representative with
none of those three connections must not be materialised.

**What is aggregated away relative to Tier 2.** Per-member identity for everyone except the
representative; per-member belief; per-member relationships; individual life history for
non-representatives.

### 5.5 Tier 4 — population cohorts

**Membership (source record lines 227-228).** Large background populations represented
statistically through geography, demographics, values, economic exposure, social networks and
sentiment.

**Indicative population.** A handful of records covering the remainder of the declared national
population. The demo has five (`scaffold/scenarios/kestral-strait.json:36-240`).

**This is the one tier with an existing implementation.** `Cohort`
(`agent_schema.py:91-109`) is its direct ancestor. The shortfalls this specification must address
are recorded in §4 and in [`./ENTITY-ONTOLOGY.md`](./ENTITY-ONTOLOGY.md).

**What must be simulated.**

| Simulated | Cadence |
|---|---|
| Distributional state: income distribution, age structure, employment, exposure | Every tick, arithmetic only |
| Belief distributions — **not** a single scalar per belief | Every tick |
| Narrative adoption | Every tick (a diffusion step exists today, `diffusion.py:40-79`) |
| Grievance set with onset, cause and resolution | On event |
| Membership accounting: how many represented people have been promoted out and are now simulated individually | On every promotion and demotion |

**What is aggregated away.** All individual identity. No person exists at Tier 4. This is the
defining property of the tier and it is the reason promotion (§6) has to **create** a person rather
than retrieve one.

**A specified change from today's structure.** Cohort belief is currently a single scalar per
belief (`CohortBeliefs`, `agent_schema.py:56-69`). A scalar cannot support promotion: if every
member of a cohort holds the mean belief, then every promoted individual is the average person and
the world becomes uniform. Tier 4 belief must therefore be specified as a **distribution** (at
minimum a central tendency plus a dispersion term), so that materialisation can draw an individual
from within the group's actual spread. **Mechanism this feeds:** the dispersion term is the
sampling parameter for §7 materialisation, and it is also what allows a minority position inside a
cohort to exist at all.

### 5.6 Tier summary

| | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Unit | Person / organisation | Person | Household, workplace, network | Statistical cohort |
| Order of count | Tens | Hundreds | Thousands | Handful of records |
| Decision model | Every tick | On event / slow cadence | Group rules only | Distribution rules only |
| Model call permitted | Yes, per tick | On engagement only | Representative only | **Never** |
| Individual identity | Full | Full | Representative only | **None** |
| Relationship edges | Full graph, directional, historied | To Tier 1/2 and own group | To cohort and representative's contacts | Inter-cohort only |
| Event history | Indefinite, full | Named/observed events | Group granularity | Cohort granularity |
| Exists today | Partly (`MicroAgent`) | **No** | **No** | Partly (`Cohort`) |

---

## 6. Promotion between tiers

### 6.1 Plain-English layer

A person who is currently just part of a statistic can become important. The source record gives
seven ways (lines 230-232). When that happens, the simulation must be able to expand them into a
detailed individual **on the spot** — and the individual it produces must be consistent with where
they came from, and must never change afterwards.

The single most important rule in this document, stated in the source record's own words
(lines 236-237):

> Once materialised, their identity and history must remain stable. The system cannot regenerate an
> entirely different biography later.

### 6.2 Promotion triggers

The source record's seven triggers, each specified as a **detectable simulation condition**, not a
narrative label. A trigger that cannot be detected from recorded state is not a trigger; it is
flavour text, and per `CHARTER.md`:129-130 flavour text must not modify the simulation.

| # | Source-record trigger | Specified detectable condition | Target tier |
|---|---|---|---|
| T1 | Records a viral video | An information-environment event originating in a Tier 3/4 group whose modelled reach crosses a scenario-declared threshold within a declared window | 1 |
| T2 | Becomes the relative of a hostage | A Tier 1/2 entity enters a hostage/casualty/detention state **and** a relationship edge of type `family` terminates in a Tier 3 group | 2 |
| T3 | Organises a protest | A collective-action event is instantiated with a Tier 3 group as origin and no existing Tier 1/2 organiser | 2 |
| T4 | Leaks information | A restricted-visibility record transitions to `leaked` and the transition is attributed to a group rather than to a named entity | 1 |
| T5 | Witnesses a military operation | An operation event's location intersects a Tier 3 group's location **and** the group's observation record is non-empty | 2 |
| T6 | Becomes a political candidate | A political-process event requires a named candidate for a constituency whose only representation is Tier 3/4 | 1 |
| T7 | Gains a large online following | A modelled audience-reach attribute for a Tier 2/3 entity crosses a scenario-declared threshold | 1 (from 2) |

**Mechanism each trigger feeds.** Every trigger above produces a *named individual who did not
previously exist as an individual*, and that individual then becomes: an endpoint for directional
relationship edges (see [`./RELATIONSHIP-GRAPH.md`](./RELATIONSHIP-GRAPH.md)); a carrier of belief
that is not the cohort mean; an addressable target of player action; and a term in the influence
weighting of §9 (a promoted individual with a large following adds media-reach capacity to their
group). A trigger that produces a person who feeds none of these must be struck under §10.

**Three specified constraints on triggers.**

1. **Triggers must not be evaluated stochastically on the shared engine stream.** If a trigger has
   a probabilistic component, it must draw from a named promotion substream (§7). Otherwise the
   number of promotion checks per tick becomes a function of scenario shape, and MERIDIAN
   reproduces the exact defect A3 demonstrated at
   [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):161-163.
2. **Promotion must be budgeted.** A scenario must declare a maximum promotions-per-tick and a
   maximum Tier 1 population. Exceeding the budget must produce a recorded deferral event, not a
   silent drop. Silent skipping is the failure mode that let a 63× data error survive undetected
   (audit §5.10).
3. **Promotion is an authoritative state change and must emit an event.** It must answer all eight
   charter questions (`CHARTER.md`:118-127): what happened, what caused it, which rule applied,
   which actors reacted, what assumptions were used, what uncertainty existed, what alternative
   outcomes were possible, what future options changed. In practice this means the promotion event
   must record the trigger id, the source group, the substream key, the candidate-selection draw,
   and the alternative candidates that were not selected.

### 6.3 Deterministic expansion of a background person

Specified as a strictly ordered, side-effect-free procedure. Every step is deterministic given its
inputs; the only randomness comes from named substreams (§7).

```text
PROMOTE(source_group, trigger_id, tick)

 1. RESOLVE  entity_id  = H(run_seed, scenario_version, source_group_id, trigger_id, slot_index)
             — H is a declared, versioned hash. NOT derived from tick, wall-clock,
               dict iteration order, or the count of prior promotions.

 2. LOOKUP   if entity_id already exists in the materialisation register:
                 RE-ATTACH the existing record. STOP.            <-- the stability rule
             Materialisation must happen at most once per entity_id, ever.

 3. DRAW     open named substreams keyed on (entity_id, purpose):
                 identity | life_history | psychology | capabilities | appearance
             Each purpose has its own stream so that adding an attribute to one
             purpose later cannot shift the values already drawn for another.

 4. SAMPLE   draw the individual FROM THE SOURCE GROUP'S DISTRIBUTIONS,
             not from a global prior. Age from the group's age structure; income
             from its income distribution; language, identity and media exposure
             from its distributions; belief from its belief distribution including
             its dispersion (§5.5).
             The individual must be a plausible member of the group they came from.

 5. CONSTRAIN apply the trigger's own implications as hard constraints, not as
             re-rolls. T2 (relative of a hostage) must produce a family edge to the
             hostage. T6 (candidate) must produce residency in the constituency.

 6. RECORD   write an immutable materialisation record: entity_id, source_group_id,
             trigger_id, tick, substream keys, draw indices, generator version,
             and the resulting authoritative identity block.

 7. ACCOUNT  decrement the source group's represented headcount by 1 and record it,
             so the population denominators in §9 stay exact.

 8. EMIT     a promotion event satisfying CHARTER.md:118-127.
```

**Step 2 is the stability rule and it is absolute.** Regeneration must be structurally impossible,
not merely discouraged. The specification requires an invariant test: materialising the same
`entity_id` twice, in two processes, at two different ticks, under two different `PYTHONHASHSEED`
values, must produce byte-identical identity blocks — or must be refused outright by the register.
Portraits inherit this directly: the portrait is generated once from the stable entity
specification and versioned (source record lines 201-206), and it must not change between sessions.

**Step 4 is the anti-stereotype rule in mechanical form.** Sampling from the group's distributions
makes identity **probabilistic, not determining** — the source record is explicit that a religious
person must not automatically behave in a particular political way and that identity "changes
probabilities, social connections and lived experience", never becoming "a stereotype switch"
(lines 87-91). The dispersion term of §5.5 is what makes a promoted individual able to dissent from
their own group. Constraints on how sensitive identity attributes may be sampled and used are the
subject of [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md).
They are **no longer gated on an undecided B5**: the founder settled B5 on 18 July 2026, and the
line it fixes applies to sampling directly —

> **Permitted:** identity affects lived experience, relationships, discrimination, institutional
> access, media exposure and cultural interpretation.
>
> **Not permitted:** identity acts as an inherent competence, morality, loyalty, violence or
> manipulability coefficient.

so a sampled identity attribute must not be allowed to condition a competence, morality, loyalty,
violence or manipulability value on the individual it produces. **Two further requirements bind
this procedure, and neither is built:**

> **B5-2 (fail-closed world mode).** Materialisation must be reachable only inside a world loaded
> with `world_mode: fictional`. The scenario loader must require that field and **fail closed**
> when it is absent, before any entity — Tier 4 cohort or promoted individual — is constructed. No
> such field, and no scenario schema to declare it in, exists today (audit §5.13); the demo's
> `fiction_disclaimer` (`scaffold/scenarios/kestral-strait.json:7`) is read by nothing.
>
> **B5-4 (no real targets).** A promoted individual must be a fictional person. Real persons,
> organisations and political populations may not be influence-target entities, and promotion is
> precisely the step that turns a statistical political population into a named individual. Nothing
> validates entity content against anything today.

Where these two checks attach — loader, entity register, or the targeting surface — is recorded as
an open question in [`./ENTITY-ONTOLOGY.md`](./ENTITY-ONTOLOGY.md) §12 Q-H, and is **not** resolved
here.

**Step 7 exists to prevent double-counting.** If a person is promoted out of a cohort and the
cohort's `represents_population` is not decremented, that person is simulated individually *and*
counted statistically. The error is small per promotion and unbounded in aggregate. Given that the
project has already shipped one silently-wrong population figure, the accounting must be explicit
and testable.

**Promotion between adjacent tiers must use the same procedure.** Tier 3 → 2 and Tier 2 → 1 differ only
in which substream purposes are opened and which attribute blocks are filled. A Tier 2 entity
promoted to Tier 1 must **not** re-draw identity, life history or appearance — those are already
materialised and are immutable. It draws only the purposes it does not yet have.

---

## 7. Deterministic materialisation and named RNG substreams

**This is the hardest technical problem in this document, and it is a hard prerequisite for the
whole of it.**

> **Ownership and sequencing, added 19 July 2026.** This problem is **not** this document's to solve
> and is no longer unowned. The founder decision of 18 July 2026 created **P0.4A — establish a
> deterministic randomness architecture** as a Phase 0 workstream in its own right, between P0.4 and
> P0.5, and ruled that it is neither a world-model detail nor something to be hidden inside replay
> ([`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md) §P0.4A).
> Three riders bind this section:
>
> - **The mechanism is unchosen.** P0.4A requires an ADR selecting deliberately between stateful
>   named substreams and keyed / counter-based deterministic draws. §7.3 below specifies the first;
>   that is this document's *recommendation*, not the project's decision. The drafted, unapproved
>   candidate ADR recommends the second
>   ([`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md),
>   Status *Proposed*).
> - **Per-entity, per-purpose keying is not by itself sufficient.** The founder scope requires
>   isolation by subsystem, entity, relationship or interaction, purpose, and tick or event context.
> - **Sequencing.** Entity promotion and world-model materialisation — the subject of this entire
>   document — **may not proceed until P0.4A passes.** Two of P0.4A's ten exit criteria are stated
>   against promotion (promoting one background person must not alter previously established
>   entities; repeating the same promotion event must produce the same profile and history), and how
>   that circularity is resolved is itself an open question (`CORRECTIVE-BACKLOG.md` CB-39,
>   `PUBLICATION-EXIT-CRITERIA.md` open question 14). Specification may proceed; building may not.

### 7.1 What exists today

MERIDIAN draws all simulation randomness from exactly one generator.
`scaffold/backend/app/simulation/engine.py:83`:

```python
self.rng = random.Random(resolved_seed)  # the ONLY source of engine randomness
```

Note the precise scope of that comment: it says this is the only source *drawn from*, not the only
generator that exists. A second `random.Random` also exists on every live `MeridianModel` — Mesa
materialises one in `Model.__new__`, reachable as `self.random`, and on the API path (`seed=None`)
it is seeded from entropy rather than from the run seed (audit §6.27,
`../delivery/CURRENT-STATE-AUDIT.md`:319). Nothing currently reads it, which is why it is not a
live defect; the audit records the one-character typo hazard (`self.model.random` for
`self.model.rng`) that would make it one silently. See §11 Q6.

Every draw in the system comes off that one stream, in sequence: `cohort_agent.py:36` draws once
per cohort **but only if that cohort has grievances**; `diffusion.py:75` draws once per graph node;
`engine.py:135` draws once per tick. Per-tick draw count is therefore a function of scenario shape.

There are **no named substreams**. A3 §6 demonstrated the consequence by execution
([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):170-175):

> There are no named RNG substreams. Adding or removing a single random draw in one subsystem
> silently changes every subsequent draw in every other subsystem.

Concretely: adding a grievance to the one grievance-free cohort moved
`shipping_throughput_pct_of_baseline` from `0.6080711379477878` to `0.5973599412373322`
(A3:161-163), while changing cohort belief *values* by two orders of magnitude changed macro by
exactly nothing (A3:151-153, 165). The apparent meso→macro coupling is shared-RNG contamination,
not causality.

### 7.2 Why this makes the present document unbuildable

Two consequences, both fatal as currently specified.

**(a) Tier promotion would move the national economy.** Materialising a person would consume draws.
On a shared stream, those draws shift every subsequent macro noise value and every diffusion jitter
for the remainder of the run. National indicators would change **because the player looked at
somebody**. That is the same spurious coupling A3 demonstrated, triggered by attention rather than
by scenario editing. Worse, the existing determinism test would mask it as expected divergence
(A3:174-175).

**(b) Stable identity would be impossible.** On a shared stream, the draws an entity receives
depend on its position in the global draw order, which depends on everything that happened before
it. The same person materialised at a different tick, or after a branch, or after any unrelated
change to cohort logic, receives a different biography and a different face. That directly
contradicts the source record's absolute rule at lines 236-237.

### 7.3 What is specified

**Named per-entity, per-purpose RNG substreams.**

| Requirement | Specification |
|---|---|
| Derivation | A substream is derived deterministically from a declared key: `substream(run_seed, namespace, entity_id, purpose, generator_version)`. It must not be derived from tick, wall-clock time, insertion order, iteration order or the count of prior draws. |
| Isolation | Draws from one substream must be provably unable to affect any other substream or the engine stream. Materialising an entity must consume **zero** draws from the engine stream. |
| Purpose scoping | Each generation purpose (identity, life history, psychology, capabilities, appearance) gets its own substream, so that adding an attribute to one purpose in a future version cannot shift values already drawn for another. |
| Versioning | `generator_version` is part of the key. A change to the generator produces a different stream by construction and is therefore a detectably different run, never a silently comparable one. |
| Recording | Every draw must record stream key, index, distribution, parameters and value, so that replay is exact and the charter's "what uncertainty existed" question is answerable. Nothing of this kind is recorded today (audit §6.17). |
| Replay | Replay must reconstruct substreams from keys, and must make zero model or network calls — the P0.6 requirement ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:87-88`)). |
| Invariant test | Materialising the same `entity_id` in two processes, at two ticks, under differing `PYTHONHASHSEED`, must produce byte-identical output. No such test exists today (audit §6.34 records zero invariant tests). |

### 7.4 This conflicts with a recorded decision and requires an owner ruling

The single shared stream is not an accident. Audit §6.28 records that it is **not currently graded
as a defect precisely because "the design is documented as one RNG in ADR-007"** — a settled,
recorded architecture decision. Introducing named substreams therefore requires **superseding an
ADR**, and [`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`) requires human approval for
"architecture … and anything affecting determinism or authoritative state". This is squarely both.

**No AI agent may make this call.** It is raised as §11 Q1, and it is raised early and prominently
because A3 already establishes the current design as a latent reproducibility hazard
**independently of any entity work** — the hazard exists today, in Phase 0's own subject matter,
whether or not this document is ever built.

There is a compounding interaction the owner should see plainly. Making grievances mutable — which
the source record's causal chain requires (lines 280-287: factory closes → income falls →
insecurity rises → trust falls) — changes per-tick draw counts **dynamically at runtime**, because
`cohort_agent.py:35` gates its draw on whether the cohort has grievances. That converts the
substream problem from a scenario-authoring hazard into a per-tick one. The two dependencies
compound; they should not be assessed separately.

---

## 8. Demotion, retention and re-promotion

### 8.1 Plain-English layer

If a person stops being important, the simulation should stop spending effort on them. But it must
not forget them. If they become important again — the protest organiser who resurfaces six months
later as a candidate — they must be **the same person**, with the same name, the same face and the
same past. Demotion must change only how often someone is simulated. It must never change who they
are.

### 8.2 Specified demotion rules

**Demotion must change cadence and evaluation scope only. It must never alter, truncate or
regenerate an entity's authoritative record.**

Demotion triggers (all scenario-declared, all deterministic):

- Relevance decay: no event has named the entity for *n* ticks and it holds no active relationship
  above a declared strength.
- Role loss: the entity no longer occupies the institutional role that qualified it for Tier 1.
  **This trigger assumes person and role occupancy are separable, so that losing office demotes the
  person's *cadence* rather than deleting the person. That separability is an unresolved owner
  decision, not a finding of this document** — see §11 Q12, and
  [`./ENTITY-ONTOLOGY.md`](./ENTITY-ONTOLOGY.md) / [`./PERSON-MODEL.md`](./PERSON-MODEL.md), which
  own it. If the owner decides instead to extend `MicroAgent` in place, this trigger must be
  revisited.
- Budget pressure: Tier 1 is at its declared cap and a higher-priority promotion is pending.
  Demotion by budget must be recorded with the priority comparison that caused it.

### 8.3 The retention set — what must survive demotion

A demoted entity retains **all** of the following. This list is the contract that makes
re-promotion identity-preserving.

| Retained | Why it must be retained (mechanism) |
|---|---|
| `entity_id` and the materialisation record | The stability rule (§6.3 step 2). Without it, re-promotion re-draws and produces a different person. |
| Full identity block | Same. Also the anchor for existing relationship edges held by other entities. |
| Structured life history | The source record requires that formative experiences do not expire (contra `AgentMemory`'s decay-only model, `agent_schema.py:143-151`). Read by the belief model when explaining a reaction. |
| Portrait reference and generation provenance | Portraits must not change between sessions (source record 201-206). |
| All substream keys and final draw indices | Re-promotion must resume, never restart. A restarted stream re-draws already-materialised attributes. |
| Directional relationship edges, in both directions | Other entities' edges point at this one. Dropping them would silently rewrite *their* histories, not just this one's. |
| Belief state at the moment of demotion, plus its provenance | Re-promotion must not resurrect the entity holding the group mean. |
| Full event history | `CHARTER.md`:118-127 must remain answerable about the demoted period. Depends on P0.6. |
| Headcount accounting flag | The entity is still promoted-out of its source group; §9's denominators must not double-count on re-promotion. |

### 8.4 What demotion may discard

Only derived and re-computable material: cached views, cached narration, per-tick intention state,
counterfactual sets for unevaluated ticks, and transient current-state values that a re-promotion
would recompute from world state anyway (for example, fatigue — which, per §5.2 and §10.2, has no
declared consumer in this document and may not survive PERSON-MODEL's causal-value test at all).

**Invariant.** `promote → demote → re-promote` must yield an identity block byte-identical to the
original. This must be asserted by a test that does not yet exist (audit §6.34,
`../delivery/CURRENT-STATE-AUDIT.md`:331, records zero invariant tests today). If the invariant
does not hold, the retention set is wrong.

---

## 9. Population weighting

### 9.1 The requirement, verbatim

> Population weighting is essential. A group of 20,000 people should not automatically exert the
> same aggregate influence as a group of two million, although a small group may have
> disproportionate influence through wealth, organisation, strategic position or political access.
> — source record lines 137-139

Both halves are binding. A design satisfying only the first half is wrong.

### 9.2 What exists today: nothing

`represents_population` is read by no code (audit §5.10). The only weight in the influence graph is
`internal_cohesion` (`diffusion.py:25-36`). And beyond that gap, **no field exists anywhere, at any
tier, for wealth, organisation, strategic position or political access.** The second half of the
requirement has no attachment surface at all.

### 9.3 Specified: two distinct weights, never conflated

**Weight A — demographic weight.** Headcount share. Used for anything that is a per-capita fact:
consumption, unemployment counts, protest turnout, casualty counts, votes, tax base. **P0.5 owns
delivering the first working instance of this.** This document does not redesign it.

```text
demographic_share(g) = represented_headcount(g) / declared_total_population
```

`declared_total_population` does not exist today (PR-6). Without it, coverage is uncheckable — the
demo's five cohorts sum to 1,488,200 against a stated 4.1 million and nothing notices. The
specification requires an explicit **unrepresented remainder**, so that shares always sum to 1 and
absent population is visible rather than silently ignored.

**Weight B — influence weight.** Used for aggregation into *political, perceptual and institutional*
indicators, where a headcount is the wrong unit. Specified as headcount modulated by named
capacities, per channel:

```text
influence_weight(g, channel c) =
      demographic_share(g) ** alpha_c
    * PRODUCT over k of ( 1 + beta_ck * capacity_k(g) )

normalised so that SUM over g of influence_weight(g, c) = 1
```

| Symbol | Meaning | Constraint |
|---|---|---|
| `alpha_c` | Channel-specific headcount exponent. `1.0` = purely proportional; lower values reduce, but must not eliminate, the effect of headcount. | Scenario/rule-pack data, `alpha_min <= alpha_c <= 1`, where `alpha_min` is scenario-declared and **must be greater than zero**. Never hard-coded in the engine. `alpha_c = 0` renders a channel headcount-blind — a group of 20,000 and one of 2,000,000 with identical capacities would contribute identically — which contradicts source record lines 137-138 and invariant 1 of §9.4. It is therefore permitted only as an explicit scenario-authored override, recorded in the §9.5 explanation record with its justification, mirroring the treatment invariant 3 gives to ceiling overrides. The default value of `alpha_min` is an owner decision (§11 Q10). |
| `capacity_k(g)` | One of the four named capacities below, normalised `0..1`. | Must be authored per group; must have a declared source. |
| `beta_ck` | How much capacity *k* amplifies influence on channel *c*. | Rule-pack data with declared bounds. |

**The channel set is not defined, by this document or by any other.** `influence_weight(g, c)` is
specified above as per-channel, and the capacities below are justified by reference to named
channel families — economic-confidence, collective-action, physical-throughput, institutional and
legitimacy. **None of those channels exists in the codebase, none is enumerated here, and §12
assigns none of them to a companion specification.** This matters more than it may appear: until
the channel set is enumerated, the causal-value test of §10 **cannot be applied to the four
capacities at all**, because a reader cannot check whether any named mechanism will ever read them.
A capacity mapped to a mechanism that is itself only a name is the subtler form of fake depth. The
channel set is specified as scenario/rule-pack-declared data rather than engine code, but who owns
enumerating it, and with what required properties per channel, is an open owner question (§11 Q10).
This gap is recorded again in §10.2.

**The four capacities, each with the mechanism it is intended to feed.** These are the source
record's four named routes to disproportionate influence; none exists as a field today. Per
invariant 7 (§9.4), each must act as a modifier on a probability, weight or magnitude — never as a
switch.

| Capacity | What it represents | Named mechanism it must feed |
|---|---|---|
| `wealth_capacity` | Concentrated financial resource relative to group size | Amplifies the group's weight in economic-confidence and investment channels; raises the ceiling on campaign amplification the group can fund; raises the probability that legal and media capability is available to it |
| `organisation_capacity` | Ability to act collectively — unions, parties, congregations, professional bodies | Amplifies collective-action channels (strike, protest, coordinated non-compliance); raises the probability that a T3 trigger fires from this group |
| `strategic_position` | Control of a chokepoint the rest of the system depends on — ports, refineries, power, transport, communications | Modulates the **probability and magnitude** of a throughput or supply effect *conditional on a modelled group decision* — a strike, a closure, a refusal to comply. It must not act independent of opinion: structural position determines how much a group's decision moves the physical channels, never whether a decision was taken. A group with `strategic_position = 0` retains a non-zero decision-mediated route (invariant 7) |
| `political_access` | Direct routes to decision-makers | Amplifies the group's weight in the institutional and legitimacy channels; **raises the probability and salience weight** with which the group's grievance enters a Tier 1 entity's information set. It must not determine that set: a declared non-zero floor applies, so no group's grievance is categorically unreachable by any route (invariant 7) |

**How the settled B5 decision binds the capacities.** All four are **non-sensitive** factors, and
that is deliberate: they correspond to the economic-exposure, institutional-affiliation and
political-behaviour factors the founder's decision expressly permits a campaign model to use where
the fictional scenario justifies them. Two requirements follow, and neither is implemented:

> **W-B5-1.** No capacity may be authored as a function of, or a stand-in for, a protected
> characteristic. `wealth_capacity`, `organisation_capacity`, `strategic_position` and
> `political_access` must be derivable from the group's economic, organisational, geographic and
> institutional record — never from `Demographics.religion_majority`
> (`agent_schema.py:27`), `primary_language` (`:28`) or any successor identity field. Authoring a
> capacity from an identity label would make a protected characteristic an optimisation criterion
> by the back door, which control **B5-5** prohibits.
>
> **W-B5-2.** Aggregation and diffusion themselves are **not** in question. Control **B5-6**
> expressly permits fictional **aggregate** narrative diffusion, exposure, adoption and
> counter-messaging. What is prohibited is optimising them against protected traits, and targeting
> a real political population at all (**B5-4**). The weighting specified in this section is
> therefore permitted machinery operating under a constraint, not machinery in doubt.

**A limit of W-B5-1 that must not be assumed away.** Several capacities are *correlated* with
protected characteristics wherever a scenario models historical exclusion — that correlation is the
intended output of the discrimination mechanisms, not a defect. A rule forbidding a capacity from
being *authored from* an identity field therefore does not prevent a campaign model from
approximating identity-based targeting through a correlated capacity. Detecting proxy optimisation
is a measurement problem and belongs to
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md); it is
raised as §11 Q5 and is **not** solved here.

**Worked illustration (illustrative arithmetic only — nothing here is implemented).** On a
political-legitimacy channel with `alpha_c = 1.0`, a group of 20,000 in a 4,000,000 population has
a demographic share of 0.005 against 0.5 for a group of 2,000,000 — a 100× difference, which
satisfies the first half of the requirement. If the small group holds `strategic_position = 0.9`
and `political_access = 0.8` with strong `beta` terms, and the large group holds neither, the small
group's influence weight rises by a bounded multiple. It should be able to matter far more than its
size. It should not be able to out-weigh a hundredfold larger group **silently**, which is why §9.5
requires the dominant term to be named in the explanation record.

### 9.4 Specified invariants

**None of these invariants is currently asserted anywhere. Each is specified as a test to be
written; audit §6.34 (`../delivery/CURRENT-STATE-AUDIT.md`:331) records that the project has zero
invariant tests today, and that "every defect in sections 4 and 5 survived the suite."**

1. **Size must matter.** On any channel where `alpha_c > 0`, two groups identical in every capacity
   but differing in headcount must produce different aggregate contributions. Must be asserted by a
   test that does not yet exist. Paired with invariant 1a, which is what keeps the scoping of this
   invariant from hollowing it out.
   1a. **At least one channel must be headcount-sensitive.** A scenario in which every aggregation
   channel carries `alpha_c = 0` must be refused at load, because it would satisfy invariant 1
   vacuously while violating source record lines 137-138 outright.
2. **Size must not be everything.** A group must be able to exceed the influence of a larger group
   through capacities alone, on at least one channel. Must be asserted by a test that does not yet
   exist.
3. **Bounded.** Influence weights must be normalised, and no single group may exceed a declared
   ceiling without an explicit scenario-authored override that is recorded.
4. **Total-conserving.** Weights must sum to 1 across groups plus the unrepresented remainder.
5. **Promotion-neutral.** Promoting an individual out of a group must not change that group's
   aggregate influence by more than that individual's own share. Promotion must be a change of
   representation, not a change of society.
6. **No aggregation over an absorbing variable.** Aggregation must be refused, at load, for any
   belief that is currently monotone by construction. See §2(b) and audit §5.9.
7. **No capacity may hard-gate a channel to zero.** Every capacity must act as a modifier on a
   probability, a weight or a magnitude, never as a switch that makes an outcome categorically
   unreachable for a group. A group with `political_access = 0` must retain a declared non-zero
   floor on grievance salience; a group with `strategic_position = 0` must retain a non-zero,
   decision-mediated route to the physical channels. This is the anti-stereotype rule of §6.3 step 4
   applied at group level, and it follows source record line 271: these attributes "should influence
   behaviour probabilistically. They should not force a single predetermined choice."

### 9.5 Explanation is mandatory, not optional

Every aggregation must emit a structured record naming, per contributing group: the demographic
share, each capacity value, each `beta` applied, the resulting influence weight, and **which term
dominated**. This is `CHARTER.md`:118-127 applied to aggregation — specifically questions 2, 3 and
5. The existing intended shape is `Outcome.explanation_trace` (`agent_schema.py:363-365`,
documented as "Ordered causal steps (data, not LLM prose)"), which is never constructed today. The
specification notes the trace must be structured records rather than `list[str]`, because a list of
strings cannot answer "which rule applied" in machine-readable form.

**The reason this is mandatory rather than nice-to-have** is audit §5.10. An inert weight let a 63×
data error survive undetected. A weight that is used but unexplained is only marginally better: it
produces a confident national number nobody can check.

---

## 10. The causal-value test applied to this document

The source record names the failure mode this specification is most likely to produce:

> There is a danger of producing enormous biographies that never affect the simulation. That would
> be fake depth. — source record lines 243-244

Audit §5.10 is the empirical proof that this is not theoretical: an attribute that feeds no
mechanism produces no error when it is wrong. There are no invariant tests anywhere in the project
to catch a repeat (audit §6.34).

**Proposed rule, for owner decision (§11 Q8): any attribute specified in the world-model documents
that has no named reading mechanism is struck, not deferred.** "Deferred" is how
`represents_population` came to sit inert in the schema for the entire life of the project.

### 10.1 Attributes and features specified here, with the mechanism each feeds

| Specified item | § | Mechanism it feeds |
|---|---|---|
| Tier assignment | 5 | Selects cadence, evaluation scope and whether a model call is permitted |
| Tier 1 soft cap | 5.2 | Bounds per-tick cost; triggers budget-pressure demotion (§8.2) |
| Tier 3 named representative | 5.4 | Promotion candidate; relationship endpoint; grievance transmission point |
| Tier 4 belief **dispersion** | 5.5 | Sampling parameter for materialisation (§6.3 step 4); makes intra-group minority positions representable |
| Represented-headcount accounting | 5.5, 6.3 | Denominator for §9 weights; prevents double-counting a promoted person |
| Seven promotion triggers T1-T7 | 6.2 | Each creates a named individual who becomes a relationship endpoint, a non-mean belief carrier, a player-addressable target, and a capacity term in §9 |
| Promotion budget and deferral event | 6.2 | Bounds cost; makes skipped promotions visible rather than silent |
| `entity_id` derivation | 6.3 | The stability rule; the substream key; the materialisation-register lookup |
| Materialisation register | 6.3 | Enforces at-most-once materialisation; the mechanism that makes regeneration structurally impossible |
| Named per-purpose RNG substreams | 7 | Isolates generation from engine randomness; makes identity reproducible; makes replay exact |
| Recorded draw metadata | 7.3 | Answers `CHARTER.md` Q6 ("what uncertainty existed"); enables exact replay |
| `generator_version` in the key | 7.3 | Makes a generator change a detectably different run, never a silently comparable one |
| Demotion retention set | 8.3 | Guarantees re-promotion identity; preserves counterparties' relationship histories |
| Retained substream cursors | 8.3 | Re-promotion resumes rather than restarts, so materialised attributes are never re-drawn |
| `demographic_share` | 9.3 | Per-capita aggregation (P0.5's channel) |
| `declared_total_population` + unrepresented remainder | 9.3 | Weight denominator; tier-4 coverage invariant |
| `wealth_capacity` | 9.3 | Economic-confidence and investment channels; raises the ceiling on fundable campaign amplification; raises the probability of available legal and media capability. **Channel undefined — see §10.2** |
| `organisation_capacity` | 9.3 | Collective-action channels; raises T3 trigger probability. **Channel undefined — see §10.2** |
| `strategic_position` | 9.3 | Modulates probability and magnitude of a throughput or supply effect, conditional on a modelled group decision; never independent of opinion, never a zero-gate (invariant 7). **Channel undefined — see §10.2** |
| `political_access` | 9.3 | Institutional and legitimacy channels; raises the probability and salience weight with which a grievance enters a Tier 1 information set, subject to a non-zero floor (invariant 7). **Channel undefined — see §10.2** |
| `alpha_c`, `beta_ck` | 9.3 | Per-channel tuning held as rule-pack data, keeping archetype specifics out of the engine |
| Eight weighting invariants (1, 1a, 2-7) | 9.4 | Each is specified as a test assertion that does not yet exist; invariant 6 is the guard against aggregating an absorbing variable, and invariant 7 is the group-level anti-stereotype guard |

### 10.2 Items specified here that I could NOT map to a simulation mechanism

Recorded explicitly rather than buried, because concealing them would be the exact defect this
document exists to avoid. Each is either presentation, governance or dependent on a document not
yet written. **None of them should be built as a behaviour-affecting attribute, and the owner
should decide whether each is retained on its stated non-simulation grounds or struck.**

| Item | § | Honest status |
|---|---|---|
| **Portrait reference** | 5.2, 5.3, 8.3 | **No simulation mechanism.** The source record itself classifies portraits as presentation (line 208). It is retained in the specification solely because identity stability requires it not to change between sessions. It must never be read by any behavioural rule. |
| **Portrait generation provenance and metadata** | 8.3 | **No simulation mechanism.** Governance and safety only (source record 204-206). Justified by [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md), not by causal value. |
| **Aggregation explanation records** | 9.5 | **No behavioural mechanism.** They change no outcome. They are mandatory under `CHARTER.md`:118-127 and as the guard against a repeat of audit §5.10 — but they are explainability, and the distinction should stay visible. |
| **Promotion event's "alternative candidates not selected"** | 6.2 | **Mechanism unproven.** Required by `CHARTER.md` Q7. Whether counterfactual candidates ever feed a later mechanism depends on [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md), which now exists in DRAFT and specifies no such reader. Currently explainability only. |
| **Retained full event history for a demoted entity** | 8.3 | **Mechanism pending another document.** It is intended to feed "which prior experiences shaped the reaction" (source record 290-292), but that reader lives in the belief-and-knowledge model and is blocked behind P0.6. Until that reader is specified, retention is justified by explainability alone. |
| **Tier 3 as a tier at all** | 5.4 | **Mechanism stated but unvalidated.** The three mechanisms given in §5.4 are genuine, but nothing resembling Tier 3 exists today and no scenario demands it. Whether the default scenario needs Tier 3 is §11 Q7. It may be correct to defer the entire tier. |
| **`region` as carried today** | 4 | **Existing field, no reader.** `Cohort.region` (`agent_schema.py:98`) is read by no code today. This document assumes location matters for trigger T5 (witnessing an operation), but does not specify a spatial model, and without one `region` remains a label. |
| **Tier 1 per-tick current state: `health`, `stress`, `fatigue`, `financial_pressure`, `confidence`, `exposure`** | 5.2 | **No named mechanism, and this document commits to computing them every tick.** That combination is the `represents_population` failure pattern exactly (audit §5.10): a per-tick computation with no declared consumer. `location` is the partial exception — trigger T5 (§6.2) reads location. The rest are carried here only because the source record's tier definitions imply a current-state block; the attribute set is delegated to [`./PERSON-MODEL.md`](./PERSON-MODEL.md), which must map each one to a named reading mechanism or strike it (§11 Q8). **None should be built as a behaviour-affecting attribute on this document's authority.** |
| **Tier 2 reduced current state: `availability`, `financial_pressure`, `loyalty`** | 5.3 | **Same status as the Tier 1 row above**, and delegated the same way. |
| **Tier 3 group aggregate state: `income`, `exposure`, `insecurity`** | 5.4 | **No named mechanism in this document.** `institutional_trust` and `grievances` in the same row are mapped (they feed §9 aggregation and the T3/T5 triggers); these three are not. The source record's causal chain at lines 280-287 (factory closes → income falls → insecurity rises → trust falls) is the obvious intended reader, but that chain lives in [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md), which now exists in DRAFT and does not specify it. Until it does, these are unmapped. |
| **The channel set that `influence_weight(g, c)` aggregates over** | 9.3 | **Named but never defined, and unowned.** The four capacities are justified by reference to economic-confidence, collective-action, physical-throughput, institutional and legitimacy channels. None exists in code, none is enumerated in this document, and §12 assigns none to a companion specification. The consequence is that the causal-value test **cannot be applied to the four capacities**: the reader cannot check whether any named mechanism will ever read them, so the mapping in §10.1 is currently unfalsifiable. Since these capacities are the entire attachment surface for the second half of the source record's population-weighting requirement (§9.2), this gap is load-bearing. Channel ownership is raised as §11 Q10. |

---

## 11. Open questions for the owner

Drafted, not resolved. AI agents may not answer these
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)).

**Q1 — deterministic randomness versus ADR-007. Narrowed 19 July 2026; the sub-question is
answered.** The founder decision of 18 July 2026 added it to Phase 0 as a new item, **P0.4A**, and
explicitly rejected both alternatives the old sub-question offered — it is not folded into P0.6 and
not deferred to the replacement architecture. **What remains for the owner:** (a) the mechanism —
stateful named substreams (this document's §7.3 recommendation) or keyed / counter-based
deterministic draws (the drafted
[`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)'s
recommendation, Status *Proposed*, unapproved); and (b) whether the resulting ADR supersedes ADR-007
or narrows it — `PHASE-0-REMEDIATION-PLAN.md` §P0.4A says supersede, ADR-010 says narrow, and
`RAID-REGISTER.md` DEC8 holds the question. Either is a determinism and authoritative-state change
requiring human approval. Everything in this document is unbuildable until P0.4A passes, and A3
establishes the current design as a latent reproducibility hazard *independently* of any entity
work.

**Q2 — Substream ownership and granularity.** Who owns the substream naming scheme, and is a
substream allocated per entity, per entity type, per purpose, or per subsystem? This document
specifies per-entity-per-purpose and gives its reasoning (§7.3), but the decision is the owner's.

**Q3 — P0.5's scope.** Should P0.5 be executed as pure population-proportional weighting, or scoped
now to leave an extension point for the multi-term influence weighting of §9? **P0.5 has not
started** ([`../../HANDOFF.md`](../../HANDOFF.md):34-38); its literal wording admits the narrower
reading, so the extension point can be settled before it does. **This is a flag, not a request to
change P0.5.**

**Q4 — Total population.** What total-population field, if any, should a scenario declare, and who
owns adding it — P0.5, the missing scenario schema work (audit §5.13, Phase 4), or this backlog?
Tier-4 coverage and the 1,488,200-versus-4.1-million discrepancy are uncheckable without it.

**Q5 — B5 / P0.8 is DECIDED; the residual question is proxy detection.** B5 was settled by the
founder on 18 July 2026 and is **not re-opened here**. The earlier form of this question — should
the tier and materialisation specification be held deliberately coarse until B5 is decided? — is
spent, and the answer it was waiting for has arrived: detail is bounded by the permitted /
not-permitted line (§6.3), not by deferral. Two things remain genuinely open, and both are owner
decisions:

- **(a) What detects optimisation on a permitted capacity that is a close proxy for a protected
  characteristic?** (§9.3.) W-B5-1 forbids authoring a capacity *from* an identity field, but
  correlation between the two is the intended output of modelled discrimination, so a static rule
  cannot catch it. Who owns the detection method, and what threshold fails a build?
- **(b) Does a Tier 4 cohort count as a "political population" for control B5-4 in every case, or
  only when it is named as a campaign target?** A cohort is a statistically represented population
  group with political tendencies, so on a plain reading every cohort is one. The distinction
  decides whether B5-4's check runs at cohort construction, at targeting, or both — which is the
  same seam recorded as Q-H in [`./ENTITY-ONTOLOGY.md`](./ENTITY-ONTOLOGY.md) §12.

The owner should still be aware that promotion converts aggregate audience-segmentation attributes
into named individuals with portraits and an asymmetric social graph, so the dual-use surface this
document creates is **strictly larger** than the one B5 was originally raised on — and that under
B5-8 none of it may be discharged by documentation.

**Q6 — Agent substrate.** Does Mesa remain the ABM substrate (audit §8 decision 3)? Tier records in
this document are specified substrate-neutral on purpose: Mesa is currently vestigial, it
materialises a second entropy-seeded `random.Random` on the API path (audit §6.27), and it carries a
`Model.rng` attribute-collision hazard on any 3.x upgrade — a hazard that a per-entity RNG layer
would multiply across a far larger entity population.

**Q7 — Does the default scenario need Tier 3?** Nothing resembling households or local networks
exists today. Starting at Tiers 1, 2 and 4 and deferring Tier 3 is a defensible reduction in scope.

**Q8 — The rejection rule.** Should the world-model documents adopt an explicit rule that any
specified attribute with no named reading mechanism is **struck rather than deferred**? Audit §5.10
is the empirical case for it. This is a specification-process decision, not a technical one.

**Q9 — Promotion budgets.** What are the defaults for maximum Tier 1 population and maximum
promotions per tick, and what is the correct behaviour on overflow — defer, demote-to-make-room, or
refuse? §6.2 specifies that overflow must be recorded; it does not choose the policy.

**Q10 — Who owns the aggregation channel set, and what is the `alpha_min` floor?** §9.3 specifies
`influence_weight(g, c)` per channel and justifies all four capacities by reference to channel
families that exist nowhere: not in code, not enumerated in this document, and not assigned to any
companion specification in §12. Until the channel set is enumerated, the causal-value test cannot be
applied to the four capacities at all. Two sub-questions: (a) which document owns enumerating the
channel set and the required properties of each channel; (b) what non-zero value should
`alpha_min` take by default, given that `alpha_c = 0` makes a channel headcount-blind and
contradicts source record lines 137-138.

**Q11 — A second gateway return type for narration.** §5.2 requires narration of authoritative
records into readable biographies and briefings. `ActionProposal` cannot carry it: it is
action-shaped and its docstring states it is "deliberately NOT a state object"
(`agent_schema.py:374-393`). Narration therefore needs a distinct, equally authority-free return
type — which amends the ADR-006 invariant that `ActionProposal` is the only type the gateway may
return. Should that amendment be made, and if so, does the new type carry the same
no-authority-over-state guarantee structurally, or only by convention? This affects the determinism
boundary and so requires human approval ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`)).

**Q12 — Is a person separable from the role they occupy?** Does a person become a first-class
entity distinct from institutional role occupancy, or is `MicroAgent` (`agent_schema.py:154-184`)
extended in place? The two answers have materially different migration costs and give different
answers to "what happens when a minister is replaced". §8.2's role-loss demotion trigger **assumes
separability** and must be revisited if the owner decides otherwise. Owned by
[`./ENTITY-ONTOLOGY.md`](./ENTITY-ONTOLOGY.md) and [`./PERSON-MODEL.md`](./PERSON-MODEL.md); flagged
here because this document depends on the answer.

---

## 12. Related documents

**Source and governing records.**

- [`./FOUNDER-REQUIREMENT-2026-07-18.md`](./FOUNDER-REQUIREMENT-2026-07-18.md) — the source record.
  Verbatim founder requirement. Where this document disagrees with it, this document is wrong.
- [`../../CHARTER.md`](../../CHARTER.md) — non-negotiable. The eight-question standard
  (`:118-127`) applies to promotion, demotion and aggregation exactly as to any other state change.
  `:137` forbids real nations, organisations, named individuals and real operational
  vulnerabilities, which constrains what materialisation may generate.
- [`../../HANDOFF.md`](../../HANDOFF.md) — Phase 0 order, standing constraints, backlog disposition.
- [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) and
  [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) — the CLOSED
  audit. Not to be re-opened; cited here as evidence only.

**Companion world-model specifications.** These are backlog documents from the same source record
(lines 345-352). Verified against the working tree, 18 July 2026: all seven now exist on disk. All
are DRAFT, none has been reviewed by the owner, and none describes implemented software.

- [`./ENTITY-ONTOLOGY.md`](./ENTITY-ONTOLOGY.md) — the common ontology every tier record must
  conform to. Tier is specified as a property *within* that ontology, not as a parallel type system.
- [`./PERSON-MODEL.md`](./PERSON-MODEL.md) — what a materialised person contains. §6.3 produces a
  record of that shape; the attribute set and its causal mappings belong there, not here.
- [`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md) — organisations are specified to occupy tiers
  too, and an organisation's internal factions are intended as the organisational analogue of
  intra-cohort dispersion (§5.5).
- [`./RELATIONSHIP-GRAPH.md`](./RELATIONSHIP-GRAPH.md) — directional, historied edges. Tier will
  determine how much of the graph an entity carries (§5.6); the retention set (§8.3) is specified to
  preserve edges in both directions.
- [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md) — owns belief distributions,
  provenance and the "what does this entity believe that is false" question. §5.5's dispersion
  requirement is an input to it; §2(b)'s bidirectionality precondition must be enforced by it.
- [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) — the dossier.
  Tier will determine how much of a dossier can be populated at all.
- [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) —
  governs how sensitive identity may be sampled at §6.3 step 4 and how capacities at §9.3 may be
  authored. B5 / P0.8 is **decided** (18 July 2026) and is not re-opened by this document; what
  this document defers to the safety guidelines is the **proxy-optimisation measurement problem**
  (§9.3, §11 Q5), which the decision does not answer.

---

**End of specification. Nothing described above is implemented. This work is backlog and must not
interrupt Phase 0 remediation.**
