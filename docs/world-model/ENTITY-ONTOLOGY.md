# ENTITY-ONTOLOGY — the common entity ontology

> # ⚠ SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing in this document exists in the MERIDIAN codebase.** Not one type, field, rule,
> identifier, view or mechanism described here has been built. This document specifies a future
> architecture. It does not describe working software.
>
> Every statement about behaviour is written as **will**, **must** or **is specified as**. Where
> this document describes something that *does* exist today, it says so explicitly and cites
> `file:line` so the boundary between the built and the specified is always visible.

**Status:** DRAFT, pending owner review.
**Date:** 18 July 2026. **Amended 19 July 2026** to apply founder decisions 1A and 1D — see
[§4.2](#42-the-taxonomy), [§5.3](#53-trait-composition-per-type),
[§6.2](#62-the-base-fields-and-the-mechanism-each-must-feed), [§8.4](#84-confidence-labels),
[§9.2](#92-the-view-projection-mechanism), [§12](#12-open-questions),
[§13](#13-attributes-with-no-causal-mechanism) and [§14](#14-related-documents). Amendments are
marked in place; nothing has been rewritten to remove a superseded position.
**Source record:** [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md).
Where this document and the source record disagree, the source record is right and this document
is wrong.

**Disposition: BACKLOG. This work must not interrupt Phase 0 remediation.** The founder was
explicit ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):5-6, :340-341;
[`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:107-120`)). This document is written now so the intent is
captured and dated before the replacement simulation architecture is designed. **It is not a
proposal to start building any of it now, and nothing in it should be read as scheduling work.**

**Authority limit.** This document is drafted by an AI agent. AI agents may draft records but may
not approve decisions ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)). Every point requiring a human
choice is recorded in [§12 Open questions](#12-open-questions) and is left unresolved.

---

## Contents

1. [Plain-English layer](#1-plain-english-layer)
2. [The foundational rule](#2-the-foundational-rule)
3. [Terminology](#3-terminology)
4. [The entity type taxonomy](#4-the-entity-type-taxonomy)
5. [Capability traits and composition](#5-capability-traits-and-composition)
6. [The common base every entity shares](#6-the-common-base-every-entity-shares)
7. [Stable identity](#7-stable-identity)
8. [The four profile views](#8-the-four-profile-views)
9. [Schema sketch](#9-schema-sketch)
10. [Mapping the existing structures onto the ontology](#10-mapping-the-existing-structures-onto-the-ontology)
11. [The eight questions, applied to entity state changes](#11-the-eight-questions-applied-to-entity-state-changes)
12. [Open questions](#12-open-questions)
13. [Attributes with no causal mechanism](#13-attributes-with-no-causal-mechanism)
14. [Related documents](#14-related-documents)

---

## 1. Plain-English layer

### What this document is for

MERIDIAN is intended to simulate a society, not just a command room. For that to work, the
important people, organisations, businesses, communities, institutions and states in a scenario
must be *persistent things the simulation knows about* — each with an identity that does not
change, a history that is recorded, relationships with others, beliefs that can be wrong, things
they can do, and circumstances that change over time.

This document is the spine. It defines what an "entity" is, what every entity has in common, how
the different kinds of entity relate to one another, and — most importantly — how the same entity
can look different depending on who is looking at it. The other world-model documents each
take one part of this and specify it in detail. They all sit on top of this one. (This sentence
read "the seven other world-model documents" until 19 July 2026, when founder decision 1A added an
eighth, [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md). The count is
now kept in [§14](#14-related-documents) alone, so it has one place to be wrong rather than two.)

### The single rule that matters most

The founder named the biggest risk plainly: producing enormous, beautiful biographies that never
affect the simulation. That is **fake depth**, and it is worse than having no biography at all,
because it *looks* like substance.

So this specification adopts a hard rule:

> **Every attribute specified anywhere in the world-model documents must name at least one
> mechanism that reads it and changes simulation behaviour as a result. An attribute with no named
> reader is to be struck from the specification, not deferred.**

This is not a stylistic preference. MERIDIAN already has empirical proof of what happens when an
attribute feeds nothing. `represents_population` — the number of citizens a cohort stands for — is
declared in the schema today at
`scaffold/backend/app/simulation/schemas/agent_schema.py:95` and is read by no code at all. Because
nothing read it, nobody noticed that one cohort's population was set roughly **63 times too low**
(`scaffold/scenarios/kestral-strait.json:79`, 14,200 against roughly 900,000 implied). The error
produced no symptom, broke no test, and survived until an audit found it by inspection
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.10). An attribute
that feeds no mechanism cannot be wrong, because nothing can tell.

Whether that rejection rule is adopted as project policy is an owner decision, recorded in
[§12](#12-open-questions).

### The second rule that matters most

Biography must influence behaviour **probabilistically**. It must never determine it.

A religious person must not automatically behave one political way. A wealthy person must not
automatically be conservative, selfish or calm. Identity is specified to change *probabilities,
social connections and lived experience*. It must never become a stereotype switch. Any mechanism
that turns an identity attribute into a fixed behavioural outcome is a defect, regardless of how
plausible the outcome looks. See [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md).

### The third rule that matters most

**The profile is not the truth.** There are specified to be **at least** four different versions of
every entity — the source record's wording is "at least four" (:147), so four is the enumerated
minimum, not a closed set — namely: what is actually true; what the entity believes about itself;
what the public believes; and what the player's role has been able to establish. Only the first is authoritative simulation
state. The other three are *derived views* — and the player's view is an intelligence product, not
an encyclopaedia. This is [§8](#8-the-four-profile-views).

### What this depends on that does not exist

This specification cannot be built on the current foundations, and it is important to say so
plainly rather than discover it later:

- **P0.4** must first define what counts as authoritative state across the three tiers
  ([`../../HANDOFF.md`](../../HANDOFF.md):75). Today the answer is implicitly "the macro tier and
  nothing else". The four-view model is a proposed *extension* of a contract that has not been
  written. This document must not assume its shape.
- **P0.6** must first repair events, snapshots and replay
  ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.6 (`:87-88`)). Event-sourced entity history is not merely
  unbuilt but **unbuildable** until it lands.
- **Deterministic randomness isolation does not exist. It is now owned by P0.4A** — a Phase 0
  workstream created by founder decision of 18 July 2026 and placed between P0.4 and P0.5
  ([`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md) §P0.4A).
  This is the hardest dependency in the set and it is explained in
  [§7.3](#73-the-rng-substream-prerequisite). Deterministic profile generation, stable portraits and
  tier promotion are all impossible without it. **The founder sequencing rule is binding on this
  document: entity promotion and world-model materialisation may not proceed until P0.4A passes.**
  Specification work such as this document is not blocked.
- **B5 / P0.8 is DECIDED** (founder decision, 18 July 2026) — and the decision makes it a *harder*
  dependency, not a discharged one. B5 no longer clears by an owner decision. It clears only when
  the eight technical controls set out in [§10.4](#104-the-b5-coupling) are **implemented and
  verified**, because the founder ruled that disclosure and any future acceptable-use wording are
  supplementary and that **technical enforcement is mandatory**. **None of the eight exists in
  code.** The framing recorded in
  [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):245-248 —
  four blockers clearing by text correction, with only B5 awaiting a decision — is therefore
  superseded. The publication gate is now **larger**, not smaller. The decision also fixes the
  envelope this ontology's identity attributes must sit within, which [§10.4](#104-the-b5-coupling)
  states in normative form.

---

## 2. The foundational rule

The source record states the rule to be adopted
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):331-334):

> Every entity can act, be acted upon, hold beliefs, participate in relationships, possess
> resources, experience events and be perceived differently by different observers.
>
> Not every entity needs every capability, but the ontology should support them consistently.

Restated as the specification's normative form:

> **R-1.** The ontology must define seven capabilities — **act**, **be acted upon**, **hold
> beliefs**, **participate in relationships**, **possess resources**, **experience events**, **be
> perceived differently by different observers** — once, in one place, with one representation
> each.
>
> **R-2.** An entity type must be able to declare which of the seven it carries. No entity type is
> required to carry all seven.
>
> **R-3.** Where two entity types carry the same capability, they must carry it in the *same
> representation*. A belief held by a person and a belief held by a community must be the same
> kind of object, differing in scope and not in shape.
>
> **R-4.** Every mechanism in the engine that consumes a capability must consume it through the
> common representation, never through a type-specific one. A mechanism that special-cases a type
> is a defect in the ontology, not a feature of the mechanism.

**R-3 and R-4 are the load-bearing clauses.** They are what make this an *ontology* rather than a
list of schemas. The project has direct evidence of what their absence costs: belief is currently
modelled twice, incompatibly — as a closed five-field vector for cohorts
(`agent_schema.py:56-69`) and as an open free-form `dict[str, float]` for micro agents
(`agent_schema.py:170-172`) — with no shared identifier namespace binding `cohort_id`
(`agent_schema.py:94`) to `agent_id` (`agent_schema.py:161`). No mechanism can operate over both,
and in fact none does.

---

## 3. Terminology

**Public-facing language** (founder decision, 18 July 2026): **simulated society**. Not "synthetic
society" and not "artificial society", both of which imply the world is merely generated content.
What is specified is deeper: a persistent society in which entities have histories, incentives and
relationships that causally affect what happens.

**Internal and technical language:** **synthetic population**, **synthetic agent** and **synthetic
data** remain correct and should be used where they are technically accurate.

This document uses "simulated society" for the world. "Synthetic population" is the correct
technical name for the generated Tier-3 and Tier-4 population where one is needed; this document
says "cohort" or "population" and does not otherwise use the internal terms.

Further definitions used in this document:

| Term | Definition as used here |
|---|---|
| **Entity** | A persistent, individually identified thing in the simulated society, carrying one or more of the seven capabilities. |
| **Entity type** | A member of the closed taxonomy in [§4](#4-the-entity-type-taxonomy). |
| **Capability trait** | One of the seven capabilities of R-1, declared per entity type. |
| **Authoritative reality** | The one view that *is* simulation state. See [§8](#8-the-four-profile-views). |
| **View** | A derived projection of an entity, computed from authoritative reality plus an observer. Never authoritative. |
| **Fidelity tier** | Tier 1-4 as defined in the source record (:217-232). Specified in detail in [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md). |
| **Materialisation** | Creating a durable, individually identified entity record where previously only statistical representation existed. |
| **Mechanism** | A named, inspectable piece of engine logic that reads a specified attribute and changes simulation behaviour as a result. Prose generation is not a mechanism. |

---

## 4. The entity type taxonomy

### 4.1 Plain-English

There are six kinds of entity. They are not a hierarchy of importance and they are not
interchangeable — each exists because it answers a question the others cannot.

- A **person** is one human being.
- An **organisation** is a group of people acting under a shared decision process — a ministry,
  a union, a militia, a political party, a media outlet.
- A **business** is an organisation whose decision process is dominated by commercial pressure —
  ownership, revenue, debt, market confidence.
- A **community** is a population group defined by shared geography, identity, occupation or
  circumstance, represented statistically rather than person by person.
- An **institution** is a durable rule-bearing structure — a legal system, a constitution, a
  central bank's mandate — that constrains what others may do, and persists when the people
  staffing it change. **For current scope an institution is a *specialised organisation*, by
  founder decision 1D of 19 July 2026; see the amendment in [§4.2](#42-the-taxonomy).**
- A **state** is the composite entity that contains a territory, a population, institutions,
  organisations and a government.

The important design point is that **a state is not one agent**. The source record is explicit
(:121-122): the government, public, military, courts, businesses and regional authorities may all
react differently. A state in this ontology is specified as a *composition* of other entities, not
as a single decision-maker.

The equally important point is that **an organisation is not one person** (:104). A shipping
company must be able to contain a chief executive worried about reputation, an operations division
worried about vessel safety, insurers worried about exposure, lawyers worried about liability,
investors worried about share price, crew unions worried about worker protection, and regional
managers with local political relationships — and its action must *emerge* from those competing
pressures.

### 4.2 The taxonomy

| Type | What it individuates | Specified in |
|---|---|---|
| `person` | One human being | [`PERSON-MODEL.md`](PERSON-MODEL.md) |
| `organisation` | A group with a shared decision process | [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) |
| `business` | A commercially-governed organisation | [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) |
| `community` | A statistically represented population group | [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) |
| `institution` | A durable rule-bearing structure | [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) |
| `state` | A composite territorial polity | this document, [§4.4](#44-composition-not-inheritance) — **and** [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) §11, §13, which specify the country's composition and attribute list. This document owns only the type's place in the taxonomy and the composition rule; it enumerates no `StateState` fields (owner decision Q-S). |

`business` is specified as a **specialisation of `organisation`**: it carries every organisation
capability and adds commercial ones (ownership, revenue, debt, market confidence, supply chain,
insurance exposure). It is a separate type rather than a flag because the mechanisms that read the
commercial attributes must not have to test for their presence on every organisation.

`institution` was specified in the 18 July 2026 draft as **distinct from `organisation`** on one
criterion: an institution's authoritative state is a set of *rules constraining other entities*, and
it survives complete turnover of the people associated with it. A ministry is an organisation;
procurement law is an institution. The distinction was said to earn its place because they feed
different mechanisms — an organisation feeds the decision-emergence mechanism, an institution feeds
action legality and pricing. **That paragraph is superseded; see the amendment below. It is retained
because the position it states is what the founder ruled against, and the record of the disagreement
is itself evidence.**

> **⚠ [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) uses the word *institution* differently, and
> the divergence is unresolved.** That document's §2 treats a ministry, a court and a central bank
> as *institutions* and models them as organisations with legal mandates, explicitly "not as a
> distinct fourth type" — the opposite of the distinction drawn here, and it therefore specifies no
> `InstitutionState`, which [§14](#14-related-documents) nonetheless lists it as owning. Both
> documents record that where they disagree on the base, this one governs; **that precedence is not
> applied unilaterally here**, because doing so would delete a modelling position the organisation
> model argues for throughout its §§11-13. It is an owner decision, and it is added to the scope of
> [§12](#12-open-questions) rather than settled by either document.

> **AMENDMENT — 19 July 2026. Founder decision 1D. The warning above is answered and the
> divergence is closed.** The ruling, applied without reinterpretation:
>
> - The **base `InstitutionState` schema and its lifecycle are owned by
>   [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md).** This document owns neither, and
>   [§14](#14-related-documents) is corrected accordingly: that document's ownership of
>   `InstitutionState` is now a ruling, not an unmet listing.
> - **For current scope an institution is a *specialised organisation*** — the same relation
>   `business` bears to `organisation` in this section, not a separate ontological kind.
> - The base state is ruled to support: mandate, authority, capacity, legitimacy, leadership,
>   staffing, **budget and resources**, procedures, jurisdiction, cohesion, **internal factions**,
>   and current operational posture. Versioned subtype extensions are permitted later.
> - **No separate institution specification may be created** unless implementation evidence proves
>   the organisation abstraction insufficient.
>
> This closes **Q-U** ([§12](#12-open-questions)), which is marked RESOLVED rather than deleted.
> It does **not** close what the ruling opens: the base state the founder enumerated includes
> budget, resources and internal factions, and [§5.3](#53-trait-composition-per-type) grants
> `institution` neither `holds_beliefs` nor `possesses_resources`. **That tension is flagged, not
> resolved, and is recorded as owner decision Q-W.** The [§5.3](#53-trait-composition-per-type)
> table is left unchanged pending it. Nor does the ruling reassign the type's place in the
> [§4.2](#42-the-taxonomy) taxonomy table: `institution` remains an enumerated `EntityType`
> pointing at [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md), which is consistent with the
> ruling — `business` is likewise a specialisation and likewise a separate enumerated type — but
> whether a specialisation warrants its own `EntityType` member at all is part of Q-W.

### 4.3 The relationship between types

Types relate through four named, machine-readable structural relations. These are **not** social
relationships (which are directional, weighted and historied, and are specified in
[`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md)). These are structural facts about how the world
is put together.

| Relation | Meaning | Legal endpoints | Mechanism it must feed |
|---|---|---|---|
| `contains` | Structural composition | state → organisation, institution, community, business; organisation → organisation | Aggregation scope: which entities' state rolls up into a composite indicator |
| `member_of` | Individual belongs to a population or body | person → community, organisation, business | Exposure routing: which events and information reach which individuals |
| `occupies_role_in` | A person holds an institutional position | person → organisation, institution, business, state | Authority resolution: whether a proposed action is within the actor's authority |
| `governed_by` | Subject to a rule-bearing structure | any → institution | Legality gate: which constraints apply to an action |

`occupies_role_in` is the ontology's answer to a defect in the current code. Today a minister *is*
the ministry role: `MicroAgent` fuses the person and the post into one record
(`agent_schema.py:154-184`) and expresses the person's identity only in the primary key string —
`min-defence-oduya` (`scaffold/scenarios/kestral-strait.json:266`). Under this ontology a person
entity and a role occupancy must be separate, so that a minister can be replaced without
destroying the person, and a person can survive losing the post. Whether that separation is
adopted, or `MicroAgent` is extended in place, is an owner decision ([§12](#12-open-questions)).

### 4.4 Composition, not inheritance

A `state` must be specified as a composed entity: it holds no national behaviour of its own beyond
its own institutions, and its national indicators must be a **derived aggregate view** over the
entities it contains, not a primary record.

This **replaces** the current arrangement rather than extending it. `MacroState`
(`scaffold/backend/app/simulation/schemas/macro_schema.py:73-87`) is today a single flat object of
eighteen national scalars, and it is de facto the only state the system treats as authoritative:
`macro_snapshot()` returns `MacroState.model_dump()` and nothing else
(`scaffold/backend/app/simulation/agents/macro_state.py:49-51`). Turning that into a derived
aggregate is a decomposition, not an added column, and it directly touches what P0.4 must decide.
This document does not decide it.

**What `StateState` authoritatively contains is unspecified, and this section does not fill the
gap.** The taxonomy in [§4.2](#42-the-taxonomy) points `state` at this section, but this section
enumerates no authoritative fields, so `StateState` appears in the
[§9.1](#91-the-base-entity) union as a named block with no specified contents and no reader. That
is not an oversight to be patched by inventing fields: if every national indicator is a derived
aggregate over contained entities, and if `state` neither acts nor holds beliefs, then it is a
live possibility that `StateState` carries only territory and the structural relations already on
the base — in which case the block should be struck and `state` reduced to a composition root.
Deciding this requires P0.4 and is **owner decision Q-S** ([§12](#12-open-questions)). Until then,
`StateState` must not be implemented.

One structural warning that must be carried into any implementation: the only existing write path
for national numbers, `MacroStateHolder.apply_deltas`
(`scaffold/backend/app/simulation/agents/macro_state.py:23-47`), applies **top-level scalars only**.
It silently skips values that are not scalars (`:36-41`) and silently skips keys it does not
recognise (`:37-38`). Entity-owned state is inherently nested. A mis-keyed entity effect written
through that path would produce no error, no warning and no symptom — the same silent-failure mode
that let the 63× population error survive. Any entity write path must therefore either be a
different path or must raise on unknown and non-scalar keys.

---

## 5. Capability traits and composition

### 5.1 Plain-English

Rather than giving every entity type its own bespoke set of abilities, the ontology is specified to
define seven abilities once and to let each type declare which it has. A community will be able to
hold beliefs and experience events, but must not, by itself, take a deliberate action — its
individual members and its organisations must do that. An institution is specified to hold no
beliefs of its own, and instead to constrain every entity governed by it.

The practical benefit is that engine mechanisms need be written only once. The belief-update
mechanism will not need to know whether it is updating a person or a community; it will need to
know only that the entity carries the `holds_beliefs` trait. **No belief-update mechanism of this
kind exists.** The only belief write in the codebase today is the one-way ratchet at
`cohort_agent.py:35-38`, which is cohort-specific, unconditional on any trait, and can only
decrease a single field.

### 5.2 The seven traits

| Trait | Meaning | Mechanism that must read it |
|---|---|---|
| `acts` | May originate a proposed action | Tick scheduler: only entities with `acts` are offered to the decision stage |
| `is_acted_upon` | May be the target of an action | Action validation: rejects an action whose target lacks the trait |
| `holds_beliefs` | Carries a belief set | Belief-update mechanism; narrative diffusion |
| `participates_in_relationships` | May be an endpoint of a directional edge | Relationship graph construction; influence propagation |
| `possesses_resources` | Carries a resource ledger | Action feasibility and pricing; resource-transfer primitives |
| `experiences_events` | Receives observations and accumulates history | Event routing; observation records; history reconstruction |
| `is_perceived` | Has derived views computed for observers | View projector ([§8](#8-the-four-profile-views)) |

### 5.3 Trait composition per type

This table is a **proposed default**, not a settled decision. Each cell is a design claim that must
survive the causal-value test for the type in question — and "must survive the test" is not a
licence to defer. Cells that do not pass are named immediately below the table and carried into
[§13](#13-attributes-with-no-causal-mechanism), per the rejection rule.

| Type | acts | is_acted_upon | holds_beliefs | relationships | resources | experiences_events | is_perceived |
|---|---|---|---|---|---|---|---|
| `person` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `organisation` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `business` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `community` | — | ✓ | ✓ | ✓ | ✓ ⚠ | ✓ | ✓ |
| `institution` | — | ✓ | — | ✓ | — | ✓ ⚠ | ✓ |
| `state` | — | ✓ | — | ✓ | ✓ ⚠ | ✓ ⚠ | ✓ |

Three deliberate exclusions, each with a reason:

- **`community` does not `act`.** A community must not emit a unitary decision, because that would
  reintroduce exactly the group-essentialism the safety guidelines forbid — a community acting as
  one implies it thinks as one. Collective behaviour must instead emerge as an *aggregate rate*
  (protest participation, strike incidence, migration flow) computed from member state, and any
  deliberate action must be attributed to a named organisation or individual within it. This is a
  design claim that needs owner confirmation.
- **`institution` does not `hold_beliefs` or `possess_resources`.** An institution is rules. The
  organisation that administers it holds the beliefs and the budget. This keeps the legality gate
  free of psychology. **⚠ Contradicted by founder decision 1D of 19 July 2026, and left standing
  rather than silently corrected.** The ruled base `InstitutionState`
  ([§4.2](#42-the-taxonomy) amendment) includes **budget and resources** and **internal factions**,
  and makes an institution a specialised organisation. On the composition rule below, trait sets
  are a property of the type, so a specialisation of `organisation` that carries a budget and
  internal factions cannot obviously withhold `possesses_resources`, and internal factions are
  hard to represent without something belief-shaped. Three resolutions are available and choosing
  between them is **owner decision Q-W** ([§12](#12-open-questions)): grant `institution` both
  traits; keep the traits withheld and locate the budget and the factions on the administering
  organisation, treating the founder's enumeration as the *organisation* base that an institution
  inherits; or drop `institution` as a distinct `EntityType` so that the question does not arise.
  **The table above is unchanged until Q-W is taken, so as things stand the ruled base state has
  fields the trait defaults would forbid.** That inconsistency is stated, not hidden.
- **`state` does not `act`.** Its government organisation acts. This is the direct ontological
  expression of the source record's "the country should not be a single agent" (:121-122).

**Four cells marked ⚠ do not currently pass the causal-value test.** The rejection rule in
[§1](#1-plain-english-layer) says an attribute with no named reader is struck, not deferred, so
these are named here rather than left to "must survive the test", and each is carried into
[§13](#13-attributes-with-no-causal-mechanism):

- **`community.possesses_resources`.** The trait's named readers in
  [§5.2](#52-the-seven-traits) are action feasibility and pricing, and resource-transfer
  primitives. `community` does not carry `acts`, so feasibility and pricing can never read a
  community ledger. One reader does survive: a community is `is_acted_upon`, so its ledger may be
  the *target* of a transfer, and the resulting balance feeds `economic_weight` in
  `InfluenceWeightTerms` ([§9.1](#91-the-base-entity)) — disproportionate influence via wealth.
  **Retained on that reader alone**, and the specification must not claim feasibility or pricing
  reads it.
- **`state.possesses_resources`.** The same feasibility argument applies, and a *primary* state
  resource ledger additionally tensions with [§4.4](#44-composition-not-inheritance)'s requirement
  that national indicators be a derived aggregate view rather than a primary record. The obvious
  alternative — relocating the treasury to the government organisation, per the composition
  principle — is a design change, not a drafting fix. **Unresolved: owner decision Q-S.**
- **`institution.experiences_events` and `state.experiences_events`.** The trait as stated in
  [§5.2](#52-the-seven-traits) bundles two mechanisms that come apart for these two types.
  *History accumulation* (event-sourcing, explanation traces, G-3) has a reader for both and is
  retained. *Observation receipt* has no reader for either, because neither type carries
  `holds_beliefs`, so nothing consumes their observation records. Whether the trait is split into
  `accumulates_history` and `receives_observations`, or simply withdrawn from these two types, is
  **owner decision Q-T**. Until it is taken, `observation_log_ref`
  ([§6.2](#62-the-base-fields-and-the-mechanism-each-must-feed)) has no reader on `institution` or
  `state`.

**`is_acted_upon` is vacuous under these defaults, and this is stated rather than hidden.** All six
types are granted it, so its named mechanism — action validation rejecting an action whose target
lacks the trait — can never fire. It is a declared discriminator that discriminates nothing. It is
retained deliberately, as the gate that future types (or future instance-level restrictions) would
need, but the specification must not claim it as an active mechanism, and it must not be cited as
evidence that the trait system is load-bearing.

**Composition rule.** An entity's trait set must be a property of its *type*, fixed at definition
time, and must not vary per instance. Instance-level variation must be expressed as values within
a capability (a person with an empty resource ledger), never as absence of the capability. Without
this rule, every mechanism must defensively test for trait presence on every entity, and the
absence becomes indistinguishable from a data error — the failure mode of `represents_population`
again.

---

## 6. The common base every entity shares

### 6.1 Plain-English

Every entity, whatever its type, carries the same small core: who it is, what type it is, when it
existed, what tier of detail it is simulated at, where its randomness comes from, what has
happened to it, and what its current authoritative state is. Type-specific detail hangs off that
core; it never replaces it.

### 6.2 The base fields, and the mechanism each must feed

Per the rejection rule in [§1](#1-plain-english-layer), each field names its reader. A field with
no named reader must not enter the schema.

| Field | Type sketch | Mechanism that must read it |
|---|---|---|
| `entity_id` | `str`, opaque, stable | Identity resolution across the event log, relationship graph, snapshot keys and view projection. Every actor reference resolves through it. |
| `entity_type` | enum of [§4.2](#42-the-taxonomy) | Trait resolution — determines which behaviour modules the tick scheduler dispatches to this entity. |
| `capability_traits` | frozen set, derived from `entity_type` | Mechanism dispatch guard ([§5.2](#52-the-seven-traits)). |
| `fidelity_tier` | enum 1-4 | Simulation cost allocation: whether an individual decision model runs, or behaviour is drawn from an aggregate rate. Governs promotion and demotion. |
| `rng_substream_key` | `str`, derived, deterministic | Deterministic generation and per-entity stochastic draws ([§7.3](#73-the-rng-substream-prerequisite)). **Prerequisite does not exist.** |
| `existence_interval` | `{created_tick, dissolved_tick?}` | Aggregation denominators (a dissolved entity must leave the population weight); relationship-edge validity; rejection of actions targeting non-existent entities. |
| `containment` | list of structural relations ([§4.3](#43-the-relationship-between-types)) | Aggregation scope; exposure routing; authority resolution; legality gate. |
| `authoritative_state` | type-specific block | The only authoritative record. All mechanisms read here. |
| `history_ref` | append-only event stream handle | Explanation traces; the eight questions ([§11](#11-the-eight-questions-applied-to-entity-state-changes)); belief provenance. **Depends on P0.6.** |
| `observation_log_ref` | append-only observation stream handle | "What evidence did the entity observe" — belief updates must cite an observation, not a global fact. **Depends on P0.6.** |
| `relationship_edges_ref` | directional edge set handle | Influence propagation; the diffusion graph. Specified in [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md). |
| `influence_weight_terms` | named multi-term structure | Aggregation weighting — population size *and* wealth, organisation, strategic position and political access. Specified in [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md). |
| `generation_provenance` | `{spec_hash, substream_key, generated_at_tick, generator_version}` | Stability verification ([§7.2](#72-what-stability-must-guarantee)) and replay verification. |

**Amended 19 July 2026, founder decision 1A.** The `observation_log_ref` handle and observation
receipt are specified in [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md).
That document records the `ViewKind` gap (no kind for entity B's view of entity A) as blocking
`M-OBS-SURF`, and defers it to owner decision Q-R. This document continues to own the handle's
presence on the base entity and the requirement that belief updates cite an observation; it does not
own what an observation is, who is in a position to make one, or how it degrades on relay.

`influence_weight_terms` is deliberately a **multi-term** structure and not a single population
scalar. The source record requires both that 20,000 people must not exert the same aggregate
influence as two million, *and* that a small group may exert disproportionate influence through
wealth, organisation, strategic position or political access (:137-139). A single scalar can
express only the first. This is flagged again in [§12](#12-open-questions) because P0.5's literal
wording — "`represents_population` must affect aggregation"
([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.5 (`:85`)) — admits a narrower reading, and P0.5 is being executed
first.

### 6.3 What the base deliberately excludes

- **No display name in authoritative state.** Names are specified in the person and organisation
  models as identity attributes with their own mechanisms (naming conventions carrying cultural
  and regional signal that affects social network formation). The base carries only the opaque
  `entity_id`. Human-readable labels must never be load-bearing for identity resolution — the
  current scenario encodes a person's identity in the primary key string
  (`scaffold/scenarios/kestral-strait.json:243`, `:266`, `:298`, `:320`, `:345`, `:367`), which
  cannot satisfy stable identity under renaming.
- **No prose biography field.** `MicroAgent.biography_ref` (`agent_schema.py:166-168`) points at a
  path — set once to `"bios/oduya.md"` (`scaffold/scenarios/kestral-strait.json:268`) — and the
  referenced file does not exist anywhere in the repository, and the field is read by no code.
  Building on it as-is would institutionalise the fake-depth failure mode. Biography must be
  structured data; the readable version must be *generated from* the structure at read time,
  through the LLM boundary ([§8.5](#85-the-llm-boundary)).
- **No portrait in authoritative state.** See [§13](#13-attributes-with-no-causal-mechanism).

---

## 7. Stable identity

### 7.1 Plain-English

Once an entity has been made real, it must stay the same entity. Its identifier must not change,
its history must not be rewritten, and its biography must not be regenerated differently later.
The source record puts it bluntly (:236-237): "Once materialised, their identity and history must
remain stable. The system cannot regenerate an entirely different biography later." Portraits must
not change between sessions (:201-202).

This sounds obvious. It is, in fact, the hardest thing in this document to deliver, and the reason
is explained in [§7.3](#73-the-rng-substream-prerequisite).

### 7.2 What stability must guarantee

| Guarantee | Statement | How it must be verified |
|---|---|---|
| **G-1 Identifier stability** | An `entity_id`, once assigned, must never be reassigned, reused or altered for the life of the run, and must survive tier promotion and demotion unchanged. | Replay must reproduce identical `entity_id` sets at every tick. |
| **G-2 Generation stability** | Regenerating an entity from the same entity specification must produce a byte-identical authoritative record. | `generation_provenance.spec_hash` recomputed and compared. |
| **G-3 History immutability** | Recorded events and observations must be append-only. A correction must be a new event, never an edit. | Event-stream hash chain. **Depends on P0.6.** |
| **G-4 Promotion monotonicity** | Promoting an entity to a higher fidelity tier must only *add* detail. It must never contradict any attribute that was already materialised, and never re-draw one. | Pre- and post-promotion diff must be additive-only. |
| **G-5 Cross-session stability** | The same run, replayed, must produce the same entities with the same identities and the same generated assets. | Replay comparison. **Depends on P0.6 and on named substreams.** |

**G-4 is the subtle one.** A Tier-4 community carries statistical attributes. When a member is
promoted to Tier 1 — because they record a viral video, become the relative of a hostage, organise
a protest, leak information, or gain a following (:230-232) — the generated individual must be
*consistent with* the statistical parent, and any attribute the simulation had already committed
to must be preserved exactly. Promotion adds resolution; it must never revise history.

### 7.3 The RNG substream prerequisite

**This is the single hardest dependency in this specification. It is owned by P0.4A.**

> **Amended 19 July 2026.** An earlier draft of this section said the prerequisite "sits under no
> Phase 0 item". That is no longer true. The founder decision of 18 July 2026 created **P0.4A —
> establish a deterministic randomness architecture** as a Phase 0 workstream in its own right,
> positioned `P0.4 → P0.4A → P0.5 → P0.6`, and stated that the problem is **not** a detail of the
> world model and must **not** be hidden inside replay. Two consequences for this document:
>
> - The scope is **wider than substreams keyed on `(run_seed, entity_id, purpose)`**. Isolation is
>   required across all of: subsystem; entity; relationship or interaction; simulation purpose; and
>   tick or event context where appropriate. **Per-entity streams alone are insufficient.** S-1 to
>   S-4 below are a subset of that requirement, not a statement of it.
> - The **mechanism is not settled**. The founder decision requires an ADR choosing deliberately
>   between stateful named substreams and keyed / counter-based deterministic draws. The word
>   "substream" throughout this section should be read as naming the *problem*, not the chosen
>   solution. The drafted candidate is
>   [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
>   (Status *Proposed*, AI-drafted, unapproved), which recommends keyed / counter-based draws.
>
> **Binding sequencing rule.** Entity promotion and world-model materialisation may not proceed
> until P0.4A passes. Specification may.

What exists today: one shared random number generator, created at
`scaffold/backend/app/simulation/engine.py:83` and commented "the ONLY source of engine
randomness". Every draw in the system comes off that one stream — the cohort drift draw
(`scaffold/backend/app/simulation/agents/cohort_agent.py:36`), one draw per graph node in
diffusion (`scaffold/backend/app/simulation/diffusion.py:75`), and one macro noise draw per tick
(`engine.py:135`).

What A3 demonstrated by execution, not inspection
([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):156-175):
adding a grievance to the single grievance-free cohort changed `shipping_throughput_pct_of_baseline`
from `0.6080711379477878` to `0.5973599412373322` — while changing cohort belief *values* by two
orders of magnitude changed macro by exactly nothing. The apparent coupling is not causality. The
cohort drift draw is *conditional on the cohort having grievances* (`cohort_agent.py:35`), so
changing how many cohorts have grievances changes how many draws are consumed per tick, which
shifts every subsequent draw in the shared stream. A3 recorded the underlying defect as one nobody
had previously identified: **there are no named RNG substreams.**

Two consequences for this ontology, both fatal as currently specified:

1. **Tier promotion would silently corrupt macro results.** Materialising a background person into
   a Tier-1 individual mid-run must consume draws to generate the biography. On a shared stream
   those draws shift every subsequent macro noise value and every diffusion jitter for the rest of
   the run. **National indicators would move because the player looked at someone.** That is the
   same spurious coupling A3 demonstrated, triggered by attention rather than by scenario editing
   — and the existing determinism test would mask it as expected divergence
   ([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):174-175).

2. **Stable identity would be unachievable.** On a shared stream, the draws an entity receives
   depend on its position in the global draw order, which depends on everything that happened
   before it. The same entity generated at a different tick, or after a branch, would receive a
   different biography and a different face. G-2 and G-5 would both fail.

What must exist instead: a **named substream keyed on something stable** — run seed, entity id and
purpose — so that generation is independent of global draw order. Specified requirement:

> **S-1.** Every stochastic draw must be attributed to a named substream.
> **S-2.** An entity's generation draws must come from a substream deterministically derived from
> `(run_seed, entity_id, purpose)` and from nothing else.
> **S-3.** Consuming draws in one substream must not alter the sequence delivered by any other.
> **S-4.** Each draw must be recordable — stream, index, distribution, parameters, value — so that
> replay can verify it. Nothing is recorded today
> ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §6.17).

**This conflicts with a recorded architecture decision.** The audit notes that the single shared
stream is not currently classed as a defect precisely because one RNG is the documented design in
ADR-007 (§6.28). Introducing substreams therefore requires superseding an ADR, and
[`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`) requires human approval for architecture decisions
and for "anything affecting determinism or authoritative state". This is squarely both. **No agent
may make this call.** It is recorded as an open question and it should be raised early, because A3
establishes the current design as a latent reproducibility hazard independently of any entity work.

There is a further compounding effect worth stating. The source record's causal chain — factory
closes → income falls → insecurity rises → trust falls (:280-287) — requires grievances to become
*mutable at runtime*. Grievances are currently the gate on the conditional draw
(`cohort_agent.py:35`). Making them mutable converts the substream problem from a
scenario-authoring hazard into a per-tick one. The two dependencies compound; they must not be
treated separately.

---

## 8. The four profile views

### 8.1 Plain-English

The source record calls this the most important design point (:145), and it is the one with no
attachment point in the codebase at all.

Every entity is specified to have **at least four** versions of its profile. The source record's
wording is "There should be at least four different versions of an entity's profile" (:147): it
enumerates four and does not close the set at four. The four it enumerates are:

1. **Authoritative reality** — what is actually true in the simulation. The player may never see
   all of it.
2. **The entity's self-understanding** — what the person or organisation believes about itself. A
   politician may genuinely think they are acting patriotically while the public sees them as
   opportunistic.
3. **Public profile** — what is publicly reported or commonly believed. May contain propaganda,
   errors, omissions and outdated information.
4. **Player intelligence profile** — what the player's role currently knows or assesses.

A prime minister might see a security assessment ordinary players cannot. A journalist might see
sources and public records. A business leader might know market relationships but not classified
intelligence. **The profile interface must therefore be built as an intelligence product, not as an
omniscient encyclopaedia.**

### 8.2 Only authoritative reality is authoritative state

> **V-1.** Only **authoritative reality** is authoritative simulation state. It is the only view
> that is snapshotted, the only view that is hashed for reproducibility, and the only view any
> engine mechanism may read when computing an outcome.
>
> **V-2.** Self-understanding, public profile and player intelligence profile are **derived
> views**. They must be computed by a pure projection function from authoritative reality plus an
> observer, and must never be written to directly.
>
> **V-3.** A derived view must never be an input to a mechanism that changes authoritative state,
> **except** where the observer is itself a simulated entity and the mechanism is that entity's own
> belief update or decision. In that case the entity's own view is the correct and intended input —
> that is what it means for an entity to act on incomplete information — and the resulting state
> change must record which view, at which tick, it was computed from.

V-3's exception is the whole point of the model and must not be read as a loophole. An entity
acting on a profile it holds to be true, and which is in fact false, is intended to be the
mechanism by which intelligence failure, deception and misperception become simulation outcomes
rather than narration.

**V-3 and the public profile do not currently fit together, and this document does not resolve
it.** V-3 as written admits a derived view as a mechanism input only where "the observer is itself
a simulated entity and the mechanism is that entity's own belief update or decision". The public
profile is defined in [§8.1](#81-plain-english) as observer-*independent* — what is publicly
reported or commonly believed — so it is nobody's own view, and on a strict reading of V-3 no
mechanism may ever read it into a state change. The `ViewKind` enum in
[§9.2](#92-the-view-projection-mechanism) has the same gap from the other direction: it offers no
kind for *simulated entity B's view of entity A*, which is precisely the input V-3's exception
licenses. `self_understanding` is an entity's view of itself and `player_intelligence` is named for
the player.

Two mutually exclusive resolutions are available, and choosing between them is an owner decision
recorded as **Q-R** in [§12](#12-open-questions):

- **(a) Widen the exception and the taxonomy.** An entity's belief update or decision may consume
  any view projected *for it as observer*, including its own projection of the public record. This
  requires generalising `ViewKind` to an observer-scoped intelligence view of which the player's is
  one instance, or adding an explicit per-observer view kind.
- **(b) Keep the exception narrow and route public information through observation.** Public
  information reaches an entity only as observation records folded into that entity's own view. In
  that case the standalone public view has exactly one reader — presentation — and must be recorded
  as a display-only projection.

Until Q-R is taken, the standalone public view has **no specified legal reader inside a state
change**, and it is recorded as such in [§13](#13-attributes-with-no-causal-mechanism). Under the
rejection rule it cannot be assumed to have earned its place.

**One caution about V-2.** An entity's self-understanding is arguably a *fact about the entity* —
it is genuinely true that the minister believes she is acting patriotically — and therefore
arguably authoritative in its own right rather than derived. This document's position is that the
belief itself lives inside authoritative reality (as a belief record with provenance), and the
*self-understanding view* is the projection of authoritative reality through the entity's own
observation history. Whether that is the right decomposition is left open in
[§12](#12-open-questions).

### 8.3 The P0.4 dependency — stated explicitly

**The four-view model cannot be finalised until P0.4 lands.** P0.4 is "Define the
authoritative-state contract across macro/meso/micro"
([`../../HANDOFF.md`](../../HANDOFF.md):75).

Today that contract is implicitly macro-only, and the evidence is unambiguous:

- `macro_snapshot()` returns `MacroState.model_dump()` and nothing else
  (`scaffold/backend/app/simulation/agents/macro_state.py:49-51`).
- The snapshot list holds macro dictionaries alone (`engine.py:116`, `:180`).
- The determinism test asserts exactly one thing —
  `a.macro_snapshot() == b.macro_snapshot()` ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.3).
- Meanwhile cohort belief is mutated in place on a live Pydantic object with no snapshot and no
  event (`scaffold/backend/app/simulation/agents/cohort_agent.py:38`), and `narrative_adoption`
  (`engine.py:112`, `:143`) appears in neither the snapshot nor the event log.

P0.4 must answer three questions this document depends on and must not pre-empt:

1. Is meso and micro entity state authoritative, or derived from macro?
2. What is the snapshot boundary? `StateSnapshot` already reserves a `meso_state` JSON column
   (`scaffold/backend/app/db/models.py:51`) that nothing writes — the shape is anticipated, the
   contract is not.
3. Which view is hashed and compared for reproducibility?

**V-1 is a claim *about* the P0.4 contract, not a substitute for it.** It is offered as this
document's recommended position, for the owner to confirm or reject. If P0.4 decides otherwise,
this section is wrong and must be rewritten.

### 8.4 Confidence labels

The player intelligence profile must label every assertion with exactly one of the eight labels
from the source record (:158-159):

**Confirmed · Reported · Assessed · Disputed · Unknown · Possibly deceptive · Outdated ·
Restricted**

> **V-4.** Confidence labels must be **computed** by the view projector from recorded evidence —
> observation records, source reliability, corroboration count, staleness, and known deception —
> and must never be authored, either by a scenario author or by the LLM.

**These are two axes, not one, and the specification must keep them separate.** Whether an
observer *may* see an attribute (visibility) and how well the observation is *evidenced*
(confidence) are different questions. `Restricted` is a visibility outcome; `Disputed` is an
evidence outcome. Overloading one enum with both would produce a model that cannot express
"observable but poorly evidenced" or "well-evidenced but withheld".

The only visibility construct that exists today is `EventVisibility` — `public`, `classified`,
`leaked` (`agent_schema.py:203-208`). It is never populated, it sits on *events* rather than on
entity attributes, and its three values do not map onto the eight labels. It is the natural place
for role-based visibility to attach, but it must be extended along the visibility axis only, with
confidence modelled separately. **Amended 19 July 2026, founder decision 1A:** the sole future
reader of `EventVisibility` is `M-OBS-EXP`, specified in
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md); this document names
the field as an attachment point and does not specify the exposure rule that reads it. Note also that **no authentication or authorisation layer of any
kind exists** ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §7), so
"player role" currently has nothing to resolve against.

The one existing precedent worth extending is `Narrative`, which separates `truth_status` from
`adoption_by_cohort` (`agent_schema.py:269-274`) — the only structure in the project that
distinguishes what is true from what is believed. It exists for claims only. The four-view model
generalises that split from claims to entities.

### 8.5 The LLM boundary

> **V-5.** The LLM may render any view into readable prose — biographies, briefings, dossier text,
> conversation. It must never invent, add, remove or silently modify any fact in authoritative
> reality, and it must never author a confidence label.

This is the CHARTER's determinism boundary ([`../../CHARTER.md`](../../CHARTER.md):37-44, ADR-006)
applied to the entity layer. It is also the one part of this specification with a working
implementation to build on: `ActionProposal` (`agent_schema.py:374-393`) is the only type the LLM
gateway may return (`scaffold/backend/app/simulation/llm_gateway.py:35`), and it carries no
authority to change numbers. All generated entity prose must route through an equivalently
constrained boundary object. Per [`../../CHARTER.md`](../../CHARTER.md):141, every generated
advisory text must carry a visible provenance tag at the interface level, distinguishing it from
engine-computed fact.

---

## 9. Schema sketch

**This is a sketch for discussion, not an implementation instruction.** Nothing here is built. It
is written in Pydantic-flavoured pseudocode for legibility only, and it makes no commitment to
Pydantic, to Mesa or to any substrate — see [§12](#12-open-questions) on the open Mesa decision.

Field names are provisional. Every field carries its mechanism in a comment, per the rejection
rule.

### 9.1 The base entity

```python
# SPECIFICATION SKETCH — NOT IMPLEMENTED

class EntityType(str, Enum):
    person = "person"
    organisation = "organisation"
    business = "business"
    community = "community"
    institution = "institution"
    state = "state"


class CapabilityTrait(str, Enum):
    acts = "acts"
    is_acted_upon = "is_acted_upon"
    holds_beliefs = "holds_beliefs"
    participates_in_relationships = "participates_in_relationships"
    possesses_resources = "possesses_resources"
    experiences_events = "experiences_events"
    is_perceived = "is_perceived"


class ExistenceInterval(BaseModel):
    created_tick: int          # mechanism: aggregation denominator; edge validity
    dissolved_tick: int | None # mechanism: removes weight from aggregation on dissolution


class StructuralRelation(BaseModel):
    relation: Literal["contains", "member_of", "occupies_role_in", "governed_by"]
    target_entity_id: str
    since_tick: int
    until_tick: int | None
    # mechanisms, by relation:
    #   contains          -> aggregation scope
    #   member_of         -> exposure routing (which events reach which individuals)
    #   occupies_role_in  -> authority resolution (is this action within the actor's authority)
    #   governed_by       -> legality gate (which constraints apply)


class GenerationProvenance(BaseModel):
    spec_hash: str             # mechanism: G-2 stability verification
    substream_key: str         # mechanism: G-5 replay verification. PREREQUISITE MISSING (§7.3)
    generated_at_tick: int     # mechanism: G-4 promotion diff (what was already committed)
    generator_version: str     # mechanism: detects generator change across versions


class InfluenceWeightTerms(BaseModel):
    """Multi-term, NOT a single population scalar. Source record :137-139."""
    represented_population: int  # mechanism: population-weighted aggregation (successor to P0.5)
    economic_weight: float       # mechanism: disproportionate influence via wealth
    organisational_weight: float # mechanism: disproportionate influence via organisation
    positional_weight: float     # mechanism: disproportionate influence via strategic position
    access_weight: float         # mechanism: disproportionate influence via political access
    # Aggregation combines these by a named, inspectable rule. Population is one term, not the rule.


class Entity(BaseModel):
    """The common base. Type-specific detail hangs off `authoritative_state`."""

    entity_id: str                          # mechanism: identity resolution everywhere
    entity_type: EntityType                 # mechanism: behaviour-module dispatch
    capability_traits: frozenset[CapabilityTrait]   # derived from entity_type; mechanism: dispatch guard
    fidelity_tier: Literal[1, 2, 3, 4]      # mechanism: cost allocation; promotion/demotion
    rng_substream_key: str                  # mechanism: deterministic generation. PREREQUISITE MISSING
    existence_interval: ExistenceInterval
    structural_relations: list[StructuralRelation]
    influence_weight_terms: InfluenceWeightTerms

    authoritative_state: PersonState | OrganisationState | CommunityState | \
                         InstitutionState | StateState   # THE ONLY AUTHORITATIVE RECORD

    history_ref: str            # append-only event stream. DEPENDS ON P0.6
    observation_log_ref: str    # append-only observation stream. DEPENDS ON P0.6
    relationship_edges_ref: str # directional edges. See RELATIONSHIP-GRAPH.md

    generation_provenance: GenerationProvenance
```

### 9.2 The view-projection mechanism

```python
# SPECIFICATION SKETCH — NOT IMPLEMENTED

class ViewKind(str, Enum):
    authoritative = "authoritative"       # NOT a projection: this IS the state
    self_understanding = "self_understanding"   # the entity's view of ITSELF
    public = "public"                     # observer-independent. NO LEGAL READER UNDER V-3 (§8.2)
    player_intelligence = "player_intelligence" # named for the player (see Observer.observer_entity_id)
    # GAP: no kind expresses "simulated entity B's view of entity A" — the exact input V-3's
    # exception licenses. This enum cannot represent the model's central causal path as written.
    # Resolution is owner decision Q-R (§12). Do not implement this enum before Q-R is taken.


class Confidence(str, Enum):
    confirmed = "confirmed"
    reported = "reported"
    assessed = "assessed"
    disputed = "disputed"
    unknown = "unknown"
    possibly_deceptive = "possibly_deceptive"
    outdated = "outdated"
    restricted = "restricted"
    # mechanism: computed by the projector from evidence. NEVER authored. See V-4.


class Observer(BaseModel):
    """Who is looking. May be the player's role, or another simulated entity."""
    observer_entity_id: str | None   # None => the player's role
    role: str                        # mechanism: visibility gate. NO AUTH LAYER EXISTS TODAY
    as_of_tick: int                  # mechanism: staleness -> `outdated`


class AttributeAssertion(BaseModel):
    """One line of a derived view. Never authoritative."""
    path: str                        # dotted path into authoritative_state
    value: Any | None                # None when withheld
    confidence: Confidence           # evidence axis
    visible: bool                    # visibility axis — SEPARATE from confidence (§8.4)
    evidence_event_ids: list[str]    # mechanism: "what evidence was observed"; DEPENDS ON P0.6
    last_updated_tick: int
    contradicted_by: list[str]       # mechanism: drives `disputed`


class EntityView(BaseModel):
    """A DERIVED PROJECTION. Never snapshotted. Never hashed. Never written to."""
    entity_id: str
    view_kind: ViewKind
    observer: Observer
    assertions: list[AttributeAssertion]
    projector_version: str           # mechanism: replay verification of the projection itself


def project(entity: Entity, view_kind: ViewKind, observer: Observer) -> EntityView:
    """MUST be a pure function of (authoritative state, observation history, observer).

    MUST NOT read another view.
    MUST NOT write to authoritative state.
    MUST NOT consume RNG draws (a projection must not perturb the run; see §7.3).
    MUST NOT call the LLM. Rendering the result into prose is a separate, later step.
    """
    ...
```

The four constraints in that docstring are the whole mechanism. In particular, **projection must
consume no randomness**, or reading a profile would change the simulation — a variant of the same
attention-perturbs-the-world defect described in [§7.3](#73-the-rng-substream-prerequisite).

**Amended 19 July 2026, founder decision 1A.** The `ViewKind` gap recorded in the enum comment is
also recorded in [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md),
where it blocks `M-OBS-SURF`, and is deferred there to the same owner decision Q-R. The two records
must be resolved together: whichever way Q-R is taken, `ViewKind` here and the observable surface
there must change consistently or the model will carry two incompatible answers.

### 9.3 The three-way sync cost

This must be stated rather than assumed away. Schemas in the project are currently maintained by
hand in three places: the Pydantic models, the nine published JSON Schema mirrors in
`scaffold/schemas/`, and the SQLAlchemy models in `scaffold/backend/app/db/models.py`. There is no
generator and no sync test; the mandate is enforced by nothing
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.13). There is also
no scenario schema at all.

An entity ontology of this size would inherit a three-way hand-maintained sync obligation across
six type-specific state schemas plus the base, the view types and the relationship edge. Whether a
schema generator should be built *before* the ontology is a sequencing decision for the owner, and
it sits outside Phase 0 ([§12](#12-open-questions)).

---

## 10. Mapping the existing structures onto the ontology

**Everything in this section describes code that exists today.** Line citations are exact as of
commit `71fa329`.

### 10.1 Mapping table

| Exists today | Location | Maps to | Nature of the change |
|---|---|---|---|
| `Cohort` | `agent_schema.py:91-109` | `Entity(type=community, tier=4)` | **Extension.** Gains identity, history, structural relations, weight terms. Its statistical fields survive largely intact. |
| `Demographics` | `agent_schema.py:22-28` | `CommunityState` demography | **Restructure.** Single majority labels (`religion_majority`, `primary_language`, `:27-28`) make intra-cohort minorities unrepresentable. |
| `EconomicProfile` | `agent_schema.py:31-39` | `CommunityState` economy | **Extension.** `income_sensitivity_to_shipping_disruption` (`:36`) is the only declared cross-tier channel in the schema layer, and is read by no code. |
| `MediaExposure` | `agent_schema.py:42-53` | `CommunityState` information environment | **Restructure.** Five channels hardcoded in the schema rather than expressed as scenario data; reach carries no trust-in-channel term. |
| `CohortBeliefs` | `agent_schema.py:56-69` | belief records under `holds_beliefs` | **Restructure.** Closed five-field vector with no provenance, evidence, source or confidence. Only `government_competence` is ever written (`cohort_agent.py:38`). |
| `InfluenceSusceptibility` | `agent_schema.py:72-77` | `CommunityState` audience attributes | **Extension, and directly governed by the settled B5 decision.** This is a manipulability structure: under the decision's not-permitted list no identity attribute may act as a manipulability coefficient, and under control **B5-5** no protected characteristic may be an optimisation criterion for persuasion. Any successor must be derivable from permitted non-sensitive factors only. See [§10.4](#104-the-b5-coupling). |
| `NetworkPosition.bridges_to` | `agent_schema.py:86-88` | directional relationship edges | **Replacement.** See [§10.3](#103-the-relationship-structures). |
| `MicroAgent` | `agent_schema.py:154-184` | `Entity(type=person)` **+** an `occupies_role_in` relation | **Decomposition.** Currently fuses the person and the post into one record. |
| `MicroAgent.biography_ref` | `agent_schema.py:166-168` | replaced by structured biography | **Removal.** Dangling pointer; see [§6.3](#63-what-the-base-deliberately-excludes). |
| `MicroAgent.beliefs` | `agent_schema.py:170-172` | belief records under `holds_beliefs` | **Restructure.** Free-form `dict[str, float]` with no slot for source, evidence, confidence or deception. |
| `MicroAgent.relationships` | `agent_schema.py:175-177` | directional relationship edges | **Replacement.** One scalar per counterpart against roughly twelve required dimensions plus history. |
| `AgentTraits` / `AgentResources` | `agent_schema.py:122-130`, `:133-140` | `PersonState` psychology / resource ledger | **Extension.** Four traits and three resources against the source record's much larger sets — each new one must pass the causal-value test. |
| `AgentMemory` | `agent_schema.py:143-151` | `observation_log_ref` + formative-experience records | **Replacement.** Models memory as a decaying ID list; formative experiences must not expire. |
| `InstitutionalAgent` | `agents/institutional_agent.py:18-41` | `organisation` decision emergence | **Replacement.** One role emits exactly one proposal per tick, with no factions and no internal disagreement. |
| `MacroState` / `MacroIndicators` | `macro_schema.py:73-87`, `:40-70` | `Entity(type=state)` + a **derived aggregate view** | **Decomposition.** See [§4.4](#44-composition-not-inheritance). |
| `Relationship` | `agent_schema.py:190-200` | directional historied edge | **Replacement.** Free of cost — never instantiated anywhere. |
| `Event` / `EventVisibility` | `agent_schema.py:211-229`, `:203-208` | `history_ref` stream; visibility axis | **Extension, downstream of P0.6.** `causal_parents` (`:224`) is the declared explainability spine and is assigned nowhere. |
| `Narrative` | `agent_schema.py:261-277` | belief/knowledge model | **Extension.** `truth_status` vs `adoption_by_cohort` is the one existing truth-vs-belief precedent. |
| `Outcome.explanation_trace` | `agent_schema.py:363-365` | eight-question record | **Restructure.** `list[str]`, so it cannot answer "which rule applied" or "what alternatives were possible" in machine-readable form. |
| `Outcome.confidence` | `agent_schema.py:366-368` | the epistemic half of the Q6 record ([§11.0](#110-why-q6-must-carry-both-axes)) | **Extension.** The declared attachment point for recorded uncertainty, but a bare 0..1 scalar: it carries no contested-mechanism flag and no outcome distribution, both of which [`../../CHARTER.md`](../../CHARTER.md):56-57, `:61-62` require. |
| `ActionProposal` | `agent_schema.py:374-393` | the LLM boundary, unchanged | **Keep.** The one existing structure this specification adopts as-is. |
| `StateSnapshot.meso_state` | `db/models.py:51` | entity-tier snapshot slot | **Occupy.** Declared, defaulted to `{}`, written by nothing. |

### 10.2 What is missing entirely

- **No entity type ontology.** `agent_class` (`agent_schema.py:163-165`) is a single default
  string, `"micro_institutional"`. Person, organisation, business, community, institution and
  state are distinguished nowhere.
- **No businesses, media outlets, foreign states or families** in any schema or in any scenario.
- **No fidelity tiers.** Two hardcoded populations are instantiated in fixed loops
  (`engine.py:96-108`) with no tier field, no promotion path and no materialisation mechanism.
  Tier 2 and Tier 3 have no representation at all.
- **No total-population denominator** in any schema or scenario, so Tier-4 coverage cannot be
  checked by anything. The five demo cohorts sum to 1,488,200 against a stated 4.1 million.
- **No shared identifier namespace** binding `cohort_id` (`:94`) and `agent_id` (`:161`).
- **No asset reference field** anywhere, and no asset store in the project.

### 10.3 The relationship structures

The graph actually used by running code is **undirected**: `nx.Graph()` at
`scaffold/backend/app/simulation/diffusion.py:24`, with `bridges_to` treated symmetrically at
`:31-36` and edge weight synthesised from `internal_cohesion` alone (`:25-26`, `:35`). The source
record requires that "A trusts B" must not imply that B trusts A (:77).

Worth noting for whoever does the work: several `bridges_to` entries in the demo scenario are
already one-sided in the data and are silently symmetrised by the graph builder. Replacing the
undirected graph is the concrete integration step, and every existing edge would need re-authoring
with direction. Full specification is in [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md).

### 10.4 The B5 coupling

`InfluenceSusceptibility` (`agent_schema.py:72-77`), `MediaExposure` (`:42-53`) and `Demographics`
(`:22-28`) are the audience-segmentation half of the dual-use pair recorded in
[`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.12; `Campaign`
(`:320-346`) is the campaign-design half, with `target_cohorts` and `existing_grievance`
("Pre-existing grievance the campaign exploits") as the explicit targeting surface.

**This ontology refines the segmentation half.** It moves targetable audience attributes from five
aggregate cohorts to named individuals with portraits and an asymmetric social graph. **The
dual-use surface it creates is therefore strictly larger than the one B5 was originally raised
on.**

#### B5 is decided. It now clears by enforcement, not by decision

**Founder decision, 18 July 2026.** B5 is settled for the public MVP and must not be recorded
anywhere as an unresolved owner decision. It is no longer discharged by anyone choosing a policy;
it is discharged only when the controls below are **built and verified**. Disclosure and any future
acceptable-use language are **supplementary**; **technical enforcement is mandatory**.

The eight controls the decision requires. **Every one is a requirement on a future architecture.
Not one exists in the codebase**, and nothing in this section may be read as describing behaviour
the engine has:

| # | Required control | Attachment point in this ontology |
|---|---|---|
| B5-1 | Influence mechanics must operate **only** in explicitly fictional worlds. | The influence and diffusion mechanisms that read `holds_beliefs` and the relationship graph. |
| B5-2 | The scenario loader must **require** `world_mode: fictional` and must **fail closed** when it is missing. | Scenario load, ahead of any entity construction ([§10.2](#102-what-is-missing-entirely): there is no scenario schema at all today). |
| B5-3 | Real-world scenario import must remain **disabled**. | Scenario load. |
| B5-4 | Real persons, organisations and political populations must **not** be permitted as influence-target entities. | `person`, `organisation`, `business`, `community` and `state` entity construction; the targeting surface of any campaign mechanism. |
| B5-5 | Protected characteristics must **not** be usable as optimisation criteria for persuasion or manipulation. | `PersonState` and `CommunityState` identity attributes; any weight table an influence mechanism optimises over. |
| B5-6 | Fictional **aggregate** narrative diffusion, exposure, adoption and counter-messaging **remain allowed**. | The diffusion and adoption mechanisms; this is a permission, and it is the reason the world model's aggregate belief machinery is not itself in question. |
| B5-7 | The API and the UI must **disclose** that the active world is fictional. | Every entity-serving surface; specified for the dossier in [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md). |
| B5-8 | Technical enforcement is mandatory; disclosure and acceptable-use wording are supplementary and may not substitute for it. | A constraint on how B5-1 to B5-7 may be satisfied — no control may be discharged by documentation alone. |

*(The numbering B5-1 to B5-8 is this document's label for the founder's clauses, adopted so the
controls can be cited precisely. The founder's decision text is the authority; the numbering is
not.)*

**`world_mode` does not exist.** No schema field asserts that a scenario is fictional, no scenario
schema exists at all (audit §5.13), and the demo scenario's `fiction_disclaimer`
(`scaffold/scenarios/kestral-strait.json:7`) is read by no code, appears in no API response and
appears nowhere in the front-end stub (audit §5.12). B5-2's fail-closed requirement therefore has
no field to test and no loader stage to test it in. Building it is new work.

**Entity construction is a B5-4 attachment point, and the ontology must not pretend otherwise.**
Nothing in this document currently distinguishes a permitted fictional entity from a prohibited
real one: `entity_id` is opaque ([§6.2](#62-the-base-fields-and-the-mechanism-each-must-feed)), the
base carries no display name at all ([§6.3](#63-what-the-base-deliberately-excludes)), and nothing
validates entity content against anything. Under B5-4 the entity register must be able to refuse a
prohibited target, and under B5-2 that refusal must be reachable before entities are constructed.
Where that check lives, and what it checks against, is **not specified here** and is added to
[§12](#12-open-questions) as Q-H.

**The identity envelope, restated normatively.** The founder's distinction now governs every
type-specific state schema derived from this ontology:

> **Permitted:** identity affects lived experience, relationships, discrimination, institutional
> access, media exposure and cultural interpretation.
>
> **Not permitted:** identity acts as an inherent competence, morality, loyalty, violence or
> manipulability coefficient.

Two consequences bear directly on this ontology. First, the not-permitted list is **wider than the
source record's** "competence, morality or intelligence" (:305-306): it adds **loyalty**,
**violence** and **manipulability**. Any belief, trait or susceptibility attribute reachable through
the `holds_beliefs` capability must be checked against the wider list, not the narrower one.
Second, a campaign mechanism **may** use non-sensitive factors — geography, institutional
affiliation, economic exposure, political behaviour, media consumption — where the fictional
scenario justifies them, but **must not optimise against protected traits**. Those factors map onto
`CommunityState` and `PersonState` attributes and onto the structural relations in
[§4.3](#43-the-relationship-between-types); the protected traits map onto the sensitive-identity
attributes specified in [`PERSON-MODEL.md`](PERSON-MODEL.md) §3.2 and governed by
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md).

**What this changes for the derived documents.** The earlier instruction — hold per-person
sensitive-identity detail deliberately coarse until B5 is decided — is spent, because B5 is
decided. The constraint that replaces it is not a licence to specify freely: identity attributes
may be specified in whatever detail the permitted list supports, and must not be specified in any
form that would serve the not-permitted list or an optimisation criterion under B5-5.

### 10.5 Relationship to P0.5

[`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) is the **design successor** to the P0.5 item
"`represents_population` must affect aggregation" ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.5 (`:84-86`)),
and to audit finding §5.10.

**It succeeds P0.5; it does not duplicate or replace it.** P0.5 delivers the single
population-weighted aggregation channel for the five-cohort meso tier that exists today.
POPULATION-FIDELITY layers the four-tier fidelity model, promotion and demotion, and the multi-term
influence weighting above it, taking P0.5's channel as given. If the two records restate each
other they will drift, and the higher-value item is the one that loses.

One tension to raise with the owner rather than assume away: a literal reading of P0.5 admits pure
population-proportional weighting, which [§6.2](#62-the-base-fields-and-the-mechanism-each-must-feed)
would then have to unpick to restore disproportionate influence. They are not in conflict in
intent, only in wording — and P0.5 is being executed first.

One further constraint from audit §5.9: cohort belief is currently a **one-way ratchet to zero**
(`cohort_agent.py:35-38`), with no code path anywhere that increases it. Population weighting would
*amplify* that defect rather than expose it — aggregating a monotone collapse, weighted by
population, would drag national approval down deterministically and in proportion to cohort size.
Population-weighted aggregation is therefore valid only against a **bidirectional** belief model.
That is a precondition on the mechanism, not a separate concern.

---

## 11. The eight questions, applied to entity state changes

[`../../CHARTER.md`](../../CHARTER.md):118-127 sets the standard for every meaningful outcome. It
applies to entity state changes **in full and without exception**. The charter's own consequence
clause (`:129-130`) is the reason: if the system cannot answer these questions, the output is
flavour text, and flavour text must not be allowed to modify the simulation.

> **Q-1.** Every change to an entity's authoritative state must be recorded as an event that
> answers all eight questions. A change that cannot answer all eight must not be applied.

| # | Charter question | What an entity state change must record |
|---|---|---|
| 1 | What happened? | The entity id, the attribute path, the prior value and the new value. |
| 2 | What caused it? | `causal_parents` — the event ids that produced this change, plus the observation ids the entity actually observed. Not a prose sentence. |
| 3 | Which rule or mechanism applied? | The named mechanism identifier and its version. Required for every change without exception. |
| 4 | Which actors reacted? | The entity ids whose state changed as a consequence, and the edges the effect travelled along. |
| 5 | What assumptions were used? | The parameter set and the view the deciding entity acted on (per V-3), pinned by tick. |
| 6 | What uncertainty existed? | **Two axes, both required.** (a) *Stochastic:* the substream, draw index, distribution and parameters of every draw consumed. (b) *Epistemic:* the applied mechanism's confidence, whether that mechanism is flagged as contested, and the outcome distribution where one was modelled. **Neither is recorded today** (audit §6.17). |
| 7 | What alternative outcomes were possible? | The counterfactual set considered at decision time, recorded *at* decision time. Nothing records this today. |
| 8 | What future options changed? | Options opened or closed — the `Optionality` primitive from [`../../CHARTER.md`](../../CHARTER.md):110. |

### 11.0 Why Q6 must carry both axes

Narrowing Q6 to stochastic draws alone would make Q-1 a gate that a confidently wrong mechanism
passes. An entity state change produced by a genuinely contested mechanism, asserted with total
false certainty, would satisfy the gate so long as its RNG draws were logged. The charter forbids
exactly that: it treats "recorded uncertainty" and "seeded stochastic resolution" as two distinct
sources ([`../../CHARTER.md`](../../CHARTER.md):37-40), it requires results to be "contestable
where the real world is contested — the model does not manufacture certainty about genuinely
disputed mechanisms" (`:56-57`), and it requires the system to model "a **distribution**, rather
than pretending there is one objectively correct future" (`:61-62`).

The existing schema already declares the attachment point for the epistemic half.
`Outcome.confidence` (`agent_schema.py:366-368`) is an engine-set 0..1 confidence on an outcome —
credited in the audit as present — and it is the field the epistemic record must extend from. Note
what it is not: it carries no contested-mechanism flag and no distribution, so it can express *how
confident* but not *whether the mechanism itself is disputed*. Note also that the mapping table in
[§10.1](#101-mapping-table) carries `explanation_trace` forward and does not mention `confidence`
at all; that omission is a defect in the mapping, and the epistemic half of Q6 must be mapped onto
`Outcome.confidence` when the mapping is next revised.

### 11.1 The source record's six questions are a subset

The source record requires history to answer six questions (:289-291): what changed; when; what
caused it; what evidence the entity observed; which prior experiences shaped the reaction; what
alternative reactions were possible.

Mapping: *what changed* → Q1; *when* → the event tick; *what caused it* → Q2; *what alternatives
were possible* → Q7. Two have **no charter counterpart and no existing structure**:

- **"What evidence did the entity observe"** requires per-entity observation records. Nothing has
  this. `EventVisibility` is declared and never populated (`agent_schema.py:203-208`), and there is
  no auth or role layer of any kind (audit §7). This is why the base entity in
  [§9.1](#91-the-base-entity) carries `observation_log_ref` separately from `history_ref`: what
  happened and what the entity *saw* happen are different records, and belief updates must cite the
  latter.
- **"Which prior experiences shaped the reaction"** requires durable formative-experience records
  that never expire. `AgentMemory` models memory as decay only (`agent_schema.py:143-151`), which
  contradicts stable life history directly.

### 11.2 Why none of this is buildable yet

The eight-question record is downstream of P0.6 in every particular, and the current foundations
cannot carry it:

- **No central transition mechanism.** `engine.py:165-173` appends raw unvalidated dictionaries;
  the `Event` model (`agent_schema.py:211-229`) is never instantiated.
- **Events are emitted only when a delta is non-empty** (`engine.py:163`), so cohort drift, macro
  noise, every diffusion step and every no-op or rejection produce **no record at all**.
- **Logged effects are the requested delta, not the realised one** (audit §6.15).
- **No RNG state is captured anywhere** — no `getstate` call exists in `backend/app` (audit §5.14)
  — so Q6 cannot be answered and a fork would resume the generator at position 0.
- **Nothing is persisted.** `SimulationRun`, `StateSnapshot` and `EventLog` (`db/models.py:23`,
  `:42`, `:56`) are never instantiated; runs live in a process-local dictionary
  (`scaffold/backend/app/api/runs.py:18`).
- **The event log is client-forgeable.** `routes_simulation.py:81` binds the entire `Intervention`
  model from the request body and `:91-100` writes it verbatim into the log, so a client can assert
  its own `legal_check` and mint colliding event ids through the interpolated `action_id`
  (audit §5.11; A3 check 5). An entity history built on this log would inherit forgeable
  provenance. Splitting the wire model from the state model is a precondition.

**Entity history is not merely unbuilt. It is unbuildable until P0.6 lands.** Any plan that
schedules the entity layer before P0.6 is wrong on the sequencing.

---

## 12. Open questions

**Every item here requires a human decision. None is resolved by this document, and no agent may
resolve any of them** ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138-140`)).

**Amended 19 July 2026.** Q-U has been **resolved by the founder** (decision 1D). It is retained,
struck through, with the answer and the date recorded against it; it is not deleted, because the
record of it having been open is evidence. Q-W is **new**, raised by that same decision. Everything
else in this table remains open.

| # | Question | Why it must be decided before this ontology can be built |
|---|---|---|
| Q-A | **Partly answered, and narrowed. Placement is decided; mechanism is not.** The founder decision of 18 July 2026 made deterministic randomness isolation **a new Phase 0 item of its own, P0.4A**, between P0.4 and P0.5, and ruled explicitly that it is neither a world-model detail nor a sub-item of P0.6 — so the "folded into P0.6 / deferred" branches of the original question are closed. **What remains open:** whether the mechanism is stateful named substreams or keyed / counter-based deterministic draws, and whether the resulting ADR supersedes or merely narrows ADR-007. Both belong to `RAID-REGISTER.md` DEC8 and `PUBLICATION-EXIT-CRITERIA.md` open question 15; the drafted, unapproved candidate is [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md). Note the scope correction: per-entity streams alone are **insufficient**. | Deterministic generation, stable identity and tier promotion are all unbuildable without it ([§7.3](#73-the-rng-substream-prerequisite)). It is a determinism and authoritative-state change requiring human approval. A3 establishes the current design as a latent hazard independently of any entity work. |
| Q-B | **Does P0.4 treat meso and micro entity state as authoritative, or as derived from macro?** | The four-view model depends entirely on the answer. V-1 is a recommendation, not a decision ([§8.3](#83-the-p04-dependency--stated-explicitly)). |
| Q-C | **Is the entity's self-understanding authoritative state in its own right, or a derived projection?** | It is a *fact* about what the entity believes, which argues for authoritative; it is also computable from belief records plus observation history, which argues for derived ([§8.2](#82-only-authoritative-reality-is-authoritative-state)). It constrains snapshot shape. |
| Q-D | **Does a person become a first-class entity distinct from the role they occupy, or is `MicroAgent` extended in place?** | Different migration costs, and different answers to what happens when a minister is replaced ([§4.3](#43-the-relationship-between-types)). |
| Q-E | **Is `MacroState` decomposed into a composed state entity, or retained as a derived aggregate view?** | [§4.4](#44-composition-not-inheritance). Couples to Q-B. |
| Q-F | **Is the rejection rule adopted as policy — any attribute with no named reading mechanism is struck, not deferred?** | Audit §5.10 is the empirical case for it; there are no invariant tests to catch a repeat (audit §6.34). This is a specification-process decision, not a technical one. |
| Q-G | **Should P0.5 be scoped now to anticipate multi-term influence weighting, or executed as pure population-proportional weighting?** | P0.5 is in flight and its literal wording admits the narrower reading ([§10.5](#105-relationship-to-p05)). |
| Q-H | **B5 / P0.8 is DECIDED — the residual question is where the eight controls attach.** Which component owns the B5-2 fail-closed `world_mode` check, and which owns the B5-4 refusal of a prohibited influence target: the scenario loader alone, the entity register, the targeting surface of the campaign mechanism, or all three? | ([§10.4](#104-the-b5-coupling).) The decision itself is **not open and must not be re-opened**; only its attachment points are. It matters here because B5-2 must fire *before* entities are constructed while B5-4 must fire *at* construction and again at targeting, and this ontology specifies no register, no scenario schema and no name or content validation of any kind ([§10.2](#102-what-is-missing-entirely)). Placing all three in the loader would leave entities materialised later in a run unchecked; placing them only at targeting would let a prohibited entity exist and be observed. Owner decision. |
| Q-I | **Does Mesa remain the agent substrate?** (audit §8 decision 3) | This document is written substrate-neutral for that reason. Assuming Mesa agent classes would prejudge an open decision and would multiply the existing `self.model.random` / `self.model.rng` collision hazard across a much larger entity layer. |
| Q-J | **Does the default scenario need Tier 3 at all, or does it start at Tiers 1, 2 and 4?** | Nothing resembling Tier 3 exists today. |
| Q-K | **What total-population field should scenarios declare?** | None exists, so Tier-4 coverage cannot be checked. Touches the missing scenario schema (audit §5.13). |
| Q-L | **Is the 63× population error (`kestral-strait.json:79`) corrected under P0.5, or under the population-weighting work that succeeds it?** | The two must not both claim it. |
| Q-M | **Is `bios/oduya.md` (`kestral-strait.json:268`) an intended future artefact, or a dangling reference to remove?** | [§6.3](#63-what-the-base-deliberately-excludes). |
| Q-N | **Should the real-world religious label used across four of the five demo cohorts be replaced with a fictional identity?** | The source record prefers fictional cultural, ethnic and religious identities for the default scenario (:315-316), consistent with [`../../CHARTER.md`](../../CHARTER.md):137. This is existing scenario data and an owner decision. Couples to the safety document. |
| Q-O | **Is a schema generator built before the ontology, given the hand-maintained three-way sync with no generator and no sync test?** | [§9.3](#93-the-three-way-sync-cost). A sequencing decision outside Phase 0. |
| Q-P | **How are portraits and generated assets stored, versioned and provenance-tagged, and what enforces "clearly fictional, not resembling a real person"?** | No asset reference field exists anywhere and no asset store exists in the project. See [§13](#13-attributes-with-no-causal-mechanism). |
| Q-Q | **Should these eight documents be written now against prerequisites that have not landed?** | Each will state which prerequisites it assumes and that none is met. The owner should confirm that is the intended trade. |
| Q-R | **How does an entity legally read public information — (a) widen V-3 and generalise `ViewKind` to per-observer views, or (b) route public information to entities only as observation records, leaving the standalone public view display-only?** | V-3 as written gives the public profile no legal reader inside a state change, while [§8.2](#82-only-authoritative-reality-is-authoritative-state) claims acting on a false public profile is the model's central causal path. The two cannot both stand. `ViewKind` ([§9.2](#92-the-view-projection-mechanism)) additionally has no kind for one entity's view of another. **The view taxonomy must not be implemented until this is taken.** |
| Q-S | **What does `StateState` authoritatively contain, given that all national indicators are specified as derived aggregates — and does the state hold a primary resource ledger, or is the treasury relocated to the government organisation?** | [§4.4](#44-composition-not-inheritance), [§5.3](#53-trait-composition-per-type). `state` neither acts nor holds beliefs, so a state ledger has no feasibility or pricing reader, and a primary national record tensions with the derived-aggregate requirement. `StateState` may reduce to a composition root with no fields. Couples to Q-B and Q-E. |
| Q-T | **Is `experiences_events` split into `accumulates_history` and `receives_observations`, or withdrawn from `institution` and `state`?** | The trait bundles two mechanisms that come apart for types lacking `holds_beliefs`: history accumulation has a reader for both, observation receipt has none ([§5.3](#53-trait-composition-per-type)). Leaving it bundled grants `observation_log_ref` to two types where nothing reads it — the `represents_population` failure mode. |
| Q-U | ~~**Which definition of `institution` stands — this document's rule-bearing structure ([§4.2](#42-the-taxonomy)), or [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) §2's mandated organisation?**~~ **RESOLVED 19 July 2026 by founder decision 1D.** [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md)'s definition stands. It owns the base `InstitutionState` schema and lifecycle; for current scope an institution is a **specialised organisation**; no separate institution specification may be created unless implementation evidence proves the organisation abstraction insufficient. The question is retained, struck through rather than deleted, because the record of it having been open is evidence. | The original entry read: *the two are incompatible, not merely differently worded: one gives `institution` a trait set without `holds_beliefs` or `possesses_resources`, the other models ministries and courts — which plainly hold both — as institutions. [§14](#14-related-documents) lists `ORGANISATION-MODEL.md` as specifying an `InstitutionState` that, on its own definition, it does not specify. Both documents defer to this one on the base and neither applies that precedence unilaterally. Couples to Q-D and Q-S.* The ruling settles ownership and the base schema. **It does not settle the trait consequence the entry itself identified** — the ruled base state includes budget, resources and internal factions — which is now carried as **Q-W**. |
| Q-W | **Does the ruled `InstitutionState` base require `institution` to carry `holds_beliefs` and `possesses_resources`, does the budget and the internal factions belong to the administering organisation instead, or does `institution` cease to be a distinct `EntityType`?** | Founder decision 1D makes an institution a specialised organisation and enumerates budget, resources and internal factions in its base state, while [§5.3](#53-trait-composition-per-type) withholds both traits from the type. The composition rule in [§5.3](#53-trait-composition-per-type) fixes trait sets per type, so the two cannot both stand. This is a taxonomy and trait change, not a drafting fix, and no agent may take it: the [§5.3](#53-trait-composition-per-type) table is therefore left unchanged and the inconsistency is stated in place. Couples to Q-U (resolved), Q-T and Q-S, and bears on the [§13](#13-attributes-with-no-causal-mechanism) disposition of `institution` as a distinct type. |
| Q-V | **Does this document take ownership of a single mechanism register across the world-model set, or is an explicit identifier crosswalk adopted instead?** | Three incompatible registers now exist: `M1`-`M20` ([`PERSON-MODEL.md`](PERSON-MODEL.md):458-479), `M-ARB`-`M-LEAD` ([`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) §6), and `RG-M1`-`RG-M5` ([`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) §7). Several mechanisms are assigned across documents that specify them under no identifier at all — M6, M7, M11, M12, M13, M14, M15, M-OBS, M-RECR. **Amended 19 July 2026:** M-OBS is no longer among them — it is specified in [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5, which also supersedes M12 and decomposes M-OBS into `M-OBS-EXP`, `M-OBS-ACQ`, `M-OBS-ATTR` and `M-OBS-SURF`. That **adds a fourth identifier family**, so the question is made larger, not smaller, by the addition. That document explicitly leaves register naming (`M-OBS*` versus `M<n>`) to `ORGANISATION-MODEL.md` §19 Q12 and states that it has not taken it. `ORGANISATION-MODEL.md` §19 Q12 names **this document** as the natural owner of a shared register; that nomination is recorded here and is not accepted by any agent. The founder requires "a common entity ontology" under which mechanisms are consistent (:322-334), which a three-register set does not deliver. |

---

## 13. Attributes with no causal mechanism

Per the rejection rule in [§1](#1-plain-english-layer), this section is mandatory and must be
maintained. **These are the items specified in this document that could not be mapped to a named
mechanism that changes simulation behaviour.** They are listed so the owner can strike them, not
buried so they survive by inattention.

| Item | Where | Why it has no mechanism | Recommended disposition |
|---|---|---|---|
| **Portrait / avatar reference** | Not in the base schema sketch; referenced in the source record (:194-208) | The source record is explicit that portraits are presentation and the underlying identity must remain structured data (:208). A portrait feeds no engine mechanism. Nothing reads it. | Deliberately **excluded from `authoritative_state`**. Recommend a separate presentation-asset record keyed by `entity_id`, carrying generation provenance. Stability (G-2, G-5) still applies to it because the founder requires portraits not to change between sessions (:201-202) — but stability is a *guarantee about* the asset, not a simulation mechanism. **Owner decision Q-P.** |
| **Human-readable display name** | Excluded in [§6.3](#63-what-the-base-deliberately-excludes) | A label alone drives nothing. (Naming *conventions* carrying cultural or regional signal may drive network-formation probabilities — but that is a person-model attribute with its own mechanism, not a base field.) | Excluded from the base. Deferred to [`PERSON-MODEL.md`](PERSON-MODEL.md) where it must earn a mechanism or be struck. |
| **`generator_version` in `GenerationProvenance`** | [§9.1](#91-the-base-entity) | Feeds no simulation mechanism. It affects reproducibility diagnostics only. | **Keep with an honest label:** it is an operational/diagnostic field, not a simulation attribute. Flagged rather than struck because reproducibility auditing is a project requirement in its own right. |
| **`projector_version` in `EntityView`** | [§9.2](#92-the-view-projection-mechanism) | Same as above. Views are derived and never authoritative, so nothing downstream of it can change state. | Keep, labelled diagnostic. |
| **The eight confidence labels, *when the observer is the player*** | [§8.4](#84-confidence-labels) | When the observer is a simulated entity, the labels feed that entity's belief update and decision (V-3) — a real mechanism. When the observer is the **player**, the label is a display property of an intelligence product and changes no simulation state. | Keep, but the specification must **not** claim the player-facing labels are causal. They are honest presentation of derived state. Any future feature that lets a player-facing label alter state would violate V-2 and V-3. |
| **`entity_type` as a *human-meaningful category*** | [§4.2](#42-the-taxonomy) | The type drives trait dispatch, which is a genuine mechanism. But the *distinction between `organisation` and `business`* is currently justified by mechanism only for the commercial attributes; if those attributes are not built, the split collapses to a label. | Provisional. The `organisation`/`business` split must be re-tested against the causal-value rule once [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) enumerates the commercial mechanisms. If they do not materialise, merge the types. |
| **The standalone `public` view** | [§8.1](#81-plain-english), [§9.2](#92-the-view-projection-mechanism) | It is defined as observer-independent, so it is nobody's "own view" and V-3 admits no path by which a mechanism may read it into a state change. Its only unambiguous reader is presentation. | **Unresolved — owner decision Q-R.** Under resolution (a) it gains a legal reader and stays; under (b) it is honestly labelled display-only. It must not be implemented before Q-R is taken, and it must not be described as causal in the interim. |
| **`state.possesses_resources`** | [§5.3](#53-trait-composition-per-type) | `state` does not carry `acts`, so the trait's named readers — action feasibility and pricing — cannot fire. No transfer mechanism naming `state` is specified, and a primary ledger tensions with [§4.4](#44-composition-not-inheritance). | **Unresolved — owner decision Q-S.** Either name the reader or relocate the treasury to the government organisation and strike the cell. |
| **`observation_log_ref` on `institution` and `state`** | [§5.3](#53-trait-composition-per-type), [§6.2](#62-the-base-fields-and-the-mechanism-each-must-feed) | Both types are granted `experiences_events`, but neither carries `holds_beliefs`, so their observation records have no consumer. Only the history-accumulation half of the trait has a reader. | **Unresolved — owner decision Q-T.** Split the trait or withdraw it from these two types. |
| **`is_acted_upon` as an active gate** | [§5.3](#53-trait-composition-per-type) | Granted to all six types, so its named mechanism — rejecting an action whose target lacks the trait — can never fire under the proposed defaults. | **Keep, labelled vacuous.** Retained as the gate future types would need. The specification must not cite it as a working mechanism. |
| **`institution` as a distinct type** | [§4.2](#42-the-taxonomy) | Justified by feeding the legality gate — but **the legality gate does not exist**. `Intervention.legal_check` is documented as engine-set (`agent_schema.py:242-244`) and is never set; scenario constraints are behaviourally inert, proven by substitution (A3 check 3: 40-tick hash identical with and without them). **Amended 19 July 2026:** founder decision 1D makes an institution a *specialised organisation*, which weakens the case for a distinct type further — the distinctness now rests on the unbuilt legality gate alone, exactly as the `organisation`/`business` split rests on unbuilt commercial mechanisms in the row above. | Keep as specified, with the honest caveat that its mechanism is itself unbuilt. If the legality gate is never built, `institution` becomes fake depth and must be struck. **Whether the type survives decision 1D at all is owner decision Q-W**, which also governs whether it carries `holds_beliefs` and `possesses_resources`. |

**No other attribute specified in this document is known to be unmapped.** Every field in
[§6.2](#62-the-base-fields-and-the-mechanism-each-must-feed) and every relation in
[§4.3](#43-the-relationship-between-types) names a mechanism, and every granted cell in
[§5.3](#53-trait-composition-per-type) has been checked against the readers named in
[§5.2](#52-the-seven-traits). That is a claim about this draft's own review, not a guarantee: an
earlier draft asserted completeness while four trait cells and the public view were unmapped, and
those were found by adversarial review rather than by the drafting. This section must be re-tested
whenever a trait, view kind or base field is added.

Whether those mechanisms are *built* is a different question, and the answer for almost all of
them is no — which is what the banner at the top of this document says.

---

## 14. Related documents

### The world-model records

*(This heading read "The eight world-model records" until 19 July 2026. A ninth record —
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) — was created by
founder decision 1A, so the count is amended rather than left wrong.)*

| Document | Relationship to this one |
|---|---|
| [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md) | **The source record.** Verbatim founder requirement, 18 July 2026. Authoritative over this document. |
| [`PERSON-MODEL.md`](PERSON-MODEL.md) | Specifies `PersonState`. Bound by [§5.3](#53-trait-composition-per-type) traits and by the B5 envelope ([§10.4](#104-the-b5-coupling)). |
| [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) | Specifies `OrganisationState`, `BusinessState` and decision emergence from competing internal pressures. **Amended 19 July 2026, founder decision 1D:** it also owns the base `InstitutionState` schema and its lifecycle, an institution being a *specialised organisation* for current scope. The earlier revision of this row listed it as specifying `InstitutionState` while that document specified none and [§4.2](#42-the-taxonomy) disputed the definition; the ruling resolves the listing, and the residual trait consequence is owner decision Q-W ([§12](#12-open-questions)). |
| [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) | Specifies the directional, historied edges referenced by `relationship_edges_ref`. |
| [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) | Specifies the belief records under `holds_beliefs`, and the **consumption** of observations — belief updating, knowledge storage and confidence labelling. **Downstream of P0.6.** |
| [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) | **Added 19 July 2026 by founder decision 1A.** Owns observation and perception: observation opportunity, sensor and source access, direct versus mediated observation, visibility, range, latency and degradation, source attribution, observation confidence, observation events, and the transformation from a world event to an entity-specific observation. It is the sole specifier of the `observation_log_ref` handle's contents ([§6.2](#62-the-base-fields-and-the-mechanism-each-must-feed)) and the sole future reader of `EventVisibility` ([§8.4](#84-confidence-labels)). It does **not** own belief updating or knowledge storage ([`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md)), dossier rendering ([`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md)), or player access control (a future access and role layer). The chain is: world event → observation opportunity → entity-specific observation → belief and knowledge update → role-filtered projection → dossier presentation. It records the `ViewKind` gap ([§9.2](#92-the-view-projection-mechanism)) as blocking `M-OBS-SURF` and defers it to owner decision Q-R. |
| [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) | Specifies `CommunityState`, the four fidelity tiers, promotion and demotion, and multi-term influence weighting. **Successor to P0.5.** |
| [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) | Specifies the ten-tab dossier as a read surface over `EntityView`. Nothing may be shown that is not a projection of authoritative reality. |
| [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) | Governs sensitive identity attributes, the anti-stereotype rule, and the settled B5 envelope ([§10.4](#104-the-b5-coupling)) — including the wider not-permitted list (competence, morality, **loyalty, violence, manipulability**) and the B5-5 prohibition on optimising against protected traits. Constrains every type-specific schema. |

*(All derived documents are backlog items. Verified against the working tree, 18 July 2026: the
seven derived documents then specified all existed on disk, alongside this record and the source
record. **Existence on disk is neither owner review nor implementation** — every one is DRAFT,
pending owner review, and none describes implemented software. An earlier revision of this section
stated that this record and the source record were the only files present in `docs/world-model/`;
that was true when written and is now false, and it is corrected rather than left to mislead.
Amended 19 July 2026: [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md)
is an eighth derived document, DRAFT of 19 July 2026 and likewise backlog. This record has not
re-verified the working tree at that date and does not assert it.)*

### Governing and evidential records

| Document | Why it matters here |
|---|---|
| [`../../CHARTER.md`](../../CHARTER.md) | Non-negotiable. The eight questions (`:118-127`), the determinism boundary (`:37-44`), the causal vocabulary (`:87-114`), and the fictional-scenarios constraint (`:137`). |
| [`../../HANDOFF.md`](../../HANDOFF.md) | § Phase 0 priority order, P0.1-P0.8 **and P0.4A** (`:68-90`), § Backlog (`:107-120`), § Standing constraints (`:135-140`). *(Line refs re-anchored 19 July 2026 when P0.4A was inserted into the canonical sequence; see `docs/delivery/HANDOFF-REFERENCE-MIGRATION.md`.)* |
| [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) | The closed audit. Findings §5.9-§5.14, §6.x cited throughout. |
| [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) | Targeted re-verification. The no-substreams defect (`:170-175`) and blocker B5 (`:245`). **Note:** that record's B5 row ("Owner decision (P0.8)") and its closing line ("Four of five clear by telling the truth. Only B5 needs a decision") predate the founder decision of 18 July 2026 and are superseded by [§10.4](#104-the-b5-coupling). B5 now clears by technical enforcement being implemented and verified. |

---

**End of specification.** DRAFT, 18 July 2026, **amended 19 July 2026** to apply founder decisions
1A (observation ownership) and 1D (`InstitutionState` ownership; institution as a specialised
organisation). Pending owner review. Nothing described here is implemented. This work is backlog
and must not interrupt Phase 0 remediation.
