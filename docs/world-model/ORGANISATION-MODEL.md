# ORGANISATION MODEL — organisations, businesses, countries and institutions

> # SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing in this document exists in MERIDIAN's code.** Not one field, not one mechanism, not
> one line. This is a specification of intended future architecture. Every behavioural statement
> below is written as *will*, *must* or *is specified as*, never in the present indicative, because
> MERIDIAN's defining defect — the reason the repository is private and the reason a Phase 0
> remediation exists — is documentation that claimed properties the code did not have.
>
> Where this document describes something that **does** exist today, it says so explicitly and
> cites `file:line`, so the boundary between what exists and what is merely specified is always
> visible.

**Status:** DRAFT, pending owner review.
**Date:** 18 July 2026.
**Amended:** 19 July 2026, to apply four founder ownership rulings of that date — 1A (observation is
owned by [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md)), 1B (M13
ROLE-AUTHORITY is assigned here), 1C (M14 FACTION-ALIGNMENT is split, the organisation half here),
and 1D (the base `InstitutionState` schema and lifecycle are assigned here). The amendments are §6
(register), §7.3, §7.4, §7.5, §12 row 5, §15-R9, §15-R12, §19 Q12, §19 Q18 and §20. Nothing that was
open before those rulings has been deleted; each is superseded in place with the date, because the
record of a question having been open is itself evidence.
**Disposition:** **BACKLOG. This work must not interrupt Phase 0 remediation.** The founder was
explicit ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):5-6, :340-341;
[`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:107-120`)). Nothing in this document is proposed for
implementation now. It is captured so that the intent is explicit and dated before the replacement
simulation architecture is designed.

**Authority:** [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md) is the
source record. Where this document and that record disagree, that record is right and this document
is wrong. [`../../CHARTER.md`](../../CHARTER.md) governs both.

**Decisions:** AI agents may draft records but may not approve decisions
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)). Everything in this document requiring a human choice is
written as an **OPEN QUESTION** in §19 and is deliberately left unresolved.

---

## Contents

1. [How to read this document](#1-how-to-read-this-document)
2. [Scope, and the other seven world-model documents](#2-scope-and-the-other-seven-world-model-documents)
3. [Plain-English summary](#3-plain-english-summary)
4. [The central principle: an organisation is not a person](#4-the-central-principle-an-organisation-is-not-a-person)
5. [What exists today, and where this contradicts it](#5-what-exists-today-and-where-this-contradicts-it)
6. [The mechanism register](#6-the-mechanism-register)
7. [The composite organisation entity](#7-the-composite-organisation-entity)
8. [Internal blocs and pressure resolution](#8-internal-blocs-and-pressure-resolution)
9. [Worked example: the shipping company](#9-worked-example-the-shipping-company)
10. [Public mission versus actual priorities](#10-public-mission-versus-actual-priorities)
11. [The country as a composed entity](#11-the-country-as-a-composed-entity)
12. [Attribute lists — organisations](#12-attribute-lists--organisations)
13. [Attribute lists — countries](#13-attribute-lists--countries)
14. [Attribute lists — businesses](#14-attribute-lists--businesses)
15. [Attributes with no mechanism: rejection candidates](#15-attributes-with-no-mechanism-rejection-candidates)
16. [Determinism, RNG substreams and the LLM boundary](#16-determinism-rng-substreams-and-the-llm-boundary)
17. [Eight-question conformance](#17-eight-question-conformance)
18. [Dependencies and sequencing](#18-dependencies-and-sequencing)
19. [Open questions for the owner](#19-open-questions-for-the-owner)
20. [What this document does not specify](#20-what-this-document-does-not-specify)

---

## 1. How to read this document

Per the founder's format requirement, every section carries two layers.

**The plain-English layer** — marked *In plain English* — is written for a reader with no Python
and no knowledge of the codebase. It should be readable on its own, end to end.

**The technical layer** carries schema sketches, field tables, mechanism mappings and `file:line`
citations. Every citation of the form `path/file.py:12-34` refers to code that **exists today** in
this repository. Every schema sketch is labelled `SKETCH — NOT IMPLEMENTED` and describes something
that does not exist.

A note on terminology, per the founder decision of 18 July 2026. Public-facing language is
**simulated society** — never "synthetic society" or "artificial society", which imply the world is
merely generated content. Internal and technical language retains **synthetic population**,
**synthetic agent** and **synthetic data**, which remain correct. This document is internal and
technical, and uses both registers accordingly.

---

## 2. Scope, and the other seven world-model documents

This document specifies the model for **organisations, businesses, countries and institutions**. The
source record gives separate attribute lists for organisations
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):97-111), countries
(:113-122) and businesses (:124-128), and this document treats them as three **profiles of one
composite structure** rather than three unrelated schemas, because they share the same skeleton: an
entity that contains other entities, holds internal disagreement, and produces an action that no
single member of it chose.

An **institution** — a ministry, a court, a central bank, a religious body, a state broadcaster — is
specified here as an organisation with a legal mandate and a constitutional position, not as a
distinct fourth type. **This sense of the word is this document's own, not the source record's.** The
source record names institutions among the entity kinds MERIDIAN must represent
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):356) but supplies neither a
definition of an institution nor an attribute list for one, in contrast to the separate lists it gives
for organisations, countries, businesses and communities. Nothing in the source record settles the
question below; it is open on the source, not resolved by it. §11 explains why a country is nevertheless
handled separately: it is not one organisation but a *federation of organisations plus populations*
that may openly contradict one another.

> **⚠ Unresolved divergence from [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md), recorded not resolved.**
> **Superseded in part, 19 July 2026 — the ownership half has been answered by the founder. This box
> is retained verbatim as the record of what was open, and must be read together with the resolution
> box immediately below it.**
>
> The paragraph above and the ontology use the word *institution* for two different things, and the
> two definitions are not compatible.
>
> [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §4.2 makes `institution` a **distinct entity type**
> whose authoritative state is "a set of *rules constraining other entities*", surviving complete
> turnover of the people associated with it, and it gives the worked contrast directly: "A ministry
> is an organisation; procurement law is an institution." It further assigns that type a trait set
> that carries neither `holds_beliefs` nor `possesses_resources` (its §5.3). This document, by
> contrast, treats a ministry, a court and a central bank as *institutions* and models them as
> organisations with mandates — entities that plainly do hold beliefs and budgets.
>
> The two are therefore not merely differently worded. Under the ontology's definition this
> document specifies no `InstitutionState` at all, while [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md)
> §14 lists this document as the specifier of one.
>
> The table below records that "where the two disagree on the base, the ontology governs", and the
> type taxonomy is part of the base. This note does **not** apply that precedence unilaterally,
> because doing so would silently delete a modelling position this document argues for throughout
> §§11-13. **It is an owner decision** and belongs with the ontology's own taxonomy questions
> (its §12). Until it is taken, a reader must resolve the word *institution* against the document
> they are reading, not across the set.

> **✔ RESOLUTION — founder decision, 19 July 2026. `InstitutionState` is owned here.**
> The box above asked who specifies `InstitutionState` and whether an institution is a distinct kind.
> The founder has ruled: **the base `InstitutionState` schema and its lifecycle are assigned to this
> document**, and **for current scope an institution is a specialised organisation** — not a fourth
> entity type and not a separate specification. The base state must support twelve things: mandate,
> authority, capacity, legitimacy, leadership, staffing, budget and resources, procedures,
> jurisdiction, cohesion, internal factions, and current operational posture. **Versioned subtype
> extensions are permitted later.** A separate institution specification **must not** be created
> unless implementation evidence proves the organisation abstraction insufficient — evidence, not
> argument, is the trigger.
>
> §7.5 specifies that base state and lifecycle. [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §14 lists
> this document as the specifier of an `InstitutionState`, and as of this ruling that listing is
> correct.
>
> **What this resolution does not settle, and the reader must not read into it.** The ruling assigns
> *ownership and shape*. It does not state what becomes of the ontology's own sense of the word —
> `institution` as "a set of rules constraining other entities" ([`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md)
> §4.2), with a trait set carrying neither `holds_beliefs` nor `possesses_resources` (its §5.3). Two
> readings survive: either that sense is renamed (to *rule regime*, *instrument* or similar) and
> `institution` means the specialised organisation specified here, or both senses persist under one
> word and the taxonomy conflict remains. **That residue is still an owner decision** and still
> belongs with the ontology's taxonomy questions (its §12). Note the concrete consequence if it is
> left: `constitutional_order: list[Instrument]` (§11.2) is closer to the ontology's rule-set sense
> than to §7.5's, so a reader meeting both in one sentence still has to disambiguate by document.

The document set this one sits in, and the boundary with each:

| Document | Its relationship to this one |
|---|---|
| [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md) | The source record. Authority over this document. |
| [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) | Defines the common entity base — identity, the four profile views, event participation, the type system. This document specialises that base. Where the two disagree on the base, the ontology governs. |
| [`PERSON-MODEL.md`](PERSON-MODEL.md) | Specifies people. An organisation's blocs are **led and staffed by persons**; a person's role occupancy is what connects the two. The attribute-to-mechanism mapping discipline used here is the discipline defined there. |
| [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) | Specifies the directional, historied edge. Every rivalry, partnership, dependency, patronage and supply-chain link named in this document is an edge in that graph, not a field here. **Added 19 July 2026 (founder decision 1C):** the person-to-faction alignment and loyalty edge, and its changing strength, is likewise that document's. This document owns only the faction itself (`M-FAC`, §7.4), and [`PERSON-MODEL.md`](PERSON-MODEL.md) consumes the projection. The mechanism must not be duplicated in any of the three. |
| [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) | Specifies what an entity believes, on what evidence, with what confidence. A bloc's *reading of the situation* is a belief record owned by that model, not by this one. |
| [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) | **Added 19 July 2026.** Specifies observation: who is in a position to observe an event, through what source, with what latency, fidelity and attribution. Owns `M-OBS` (§6) and everything upstream of belief updating. This document is a client: it emits decisions, implementations and divergences as world events, and that document determines who sees them. |
| [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) | Specifies the four fidelity tiers, population weighting, and promotion/demotion. Organisational influence weighting (§6, `M-INF`) is a **client** of that document's weighting model and must not restate it. |
| [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) | Specifies the player-facing dossier. The organisation dossier tabs derive from §10 and §12-14 here. |
| [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) | Governs sensitive-identity modelling and the dual-use question. §18 flags the coupling; this document does not resolve it. |

Supporting records: [`../../CHARTER.md`](../../CHARTER.md),
[`../../HANDOFF.md`](../../HANDOFF.md), [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md),
[`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md).

> **Note — verified against the working tree, 18 July 2026.** All seven sibling documents listed
> above exist on disk and every link in the table resolves:
> `docs/world-model/ENTITY-ONTOLOGY.md`, `PERSON-MODEL.md`, `RELATIONSHIP-GRAPH.md`,
> `BELIEF-AND-KNOWLEDGE-MODEL.md`, `POPULATION-FIDELITY.md`, `docs/design/ENTITY-PROFILE-EXPERIENCE.md`
> and `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`. Several were written in the same session as this
> one. **All eight, including this one, are DRAFT and BACKLOG; none has been reviewed by the owner,
> and none describes implemented software.** Existence on disk is not review, and is not
> implementation.
>
> **Amended 19 July 2026.** An eighth sibling now exists and has been added to the table:
> `docs/world-model/OBSERVATION-AND-PERCEPTION-MODEL.md`, verified on disk on 19 July 2026. It too is
> DRAFT and BACKLOG, and it too describes no implemented software, so the sentence above holds
> unchanged in substance for nine documents rather than eight. The §2 heading still reads "the other
> seven"; it is left as written rather than silently recounted, and the accurate count is eight
> siblings plus the source record.

> **Note — mechanism register incompatibility.** The sentence above says this document uses the
> attribute-to-mechanism discipline defined in [`PERSON-MODEL.md`](PERSON-MODEL.md). It uses the
> *discipline* but **not the register**, and the two registers are not currently reconcilable.
> [`PERSON-MODEL.md`](PERSON-MODEL.md):458-479 defines `M1`-`M20`; this document defines a
> differently-shaped register of twenty-one `M-*` mechanisms (§6), one of which (`M-AUTH`)
> decomposes into named sub-mechanisms in §7.3. Neither document references the other's identifiers
> anywhere.
>
> **Amended 19 July 2026.** The register was nineteen mechanisms when this note was written. It is
> twenty-one because founder rulings 1B and 1C assigned two further mechanisms to this document, and
> §6 now carries `M-AUTH` and `M-FAC`. That is a change of size, not of kind: the two registers are
> still not reconciled, and the naming question below is still open.
>
> **There is in fact a third register, and the problem is larger than two documents.**
> [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) defines `RG-M1`-`RG-M5` (its §7), which is a third
> naming scheme again. Two further orphaned assignments follow from that:
> `PERSON-MODEL.md`:465-466 assigns **M6 TIE-FORMATION** and **M7 TIE-UPDATE** to
> [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md), which specifies neither identifier; and
> `PERSON-MODEL.md`:470, :474 assign **M11 INFLUENCE-WEIGHT** and **M15 PROMOTION-SALIENCE** to
> [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md), which specifies the corresponding *substance*
> (its §9 weighting, its §6.2 promotion triggers) but under neither identifier. Those are naming
> failures rather than missing mechanisms, and they are recorded so that a crosswalk, if one is
> adopted, is scoped to all three registers rather than to two.
>
> Three specific breakages follow. **Two of the three were answered by the founder on 19 July 2026
> and are marked below; the third is unchanged and is still not resolved by this document
> (§19 Q12).**
>
> 1. [`PERSON-MODEL.md`](PERSON-MODEL.md):472-473 assigns **M13 ROLE-AUTHORITY** and
>    **M14 FACTION-ALIGNMENT** to *this* document, and this document specifies neither. It has
>    `role_occupancies` as a field and `M-SUCC` for transitions, but no mechanism resolving powers
>    through role occupancy; and `M-LEAD` (§6) covers only how a role occupant modulates a bloc's
>    interest weights, not which bloc a person aligns with or their individual defection
>    probability. `PERSON-MODEL.md`:694 maps `state.current_role` to M13, so a central person
>    attribute is currently mapped to a mechanism that exists in **no** document. By the founder's
>    definition (:243-244) and by this document's own rejection rule (§6), that is fake depth, and
>    it is recorded here rather than quietly absorbed.
>
>    **✔ ANSWERED — founder decisions 1B and 1C, 19 July 2026.** The assignment stands and is now
>    discharged. **M13 ROLE-AUTHORITY is this document's**, specified as `M-AUTH` at §7.3, covering
>    roles and offices, authority attached to a role, jurisdiction, delegation, appointment and
>    removal, acting authority, conflicts between formal and practical authority, organisational
>    command chains, and authority expiry and suspension.
>    [`PERSON-MODEL.md`](PERSON-MODEL.md) may *reference* a person's current role but must not own
>    the mechanism, so `PERSON-MODEL.md`:694's mapping of `state.current_role` now points at a
>    mechanism that exists — here. **M14 FACTION-ALIGNMENT is split three ways and must not be
>    duplicated**: faction definitions, membership rules, formal positions and faction structure are
>    this document's, specified as `M-FAC` at §7.4; the directional, historied person-to-faction
>    alignment and loyalty **edge**, and its changing strength, are
>    [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md)'s; and
>    [`PERSON-MODEL.md`](PERSON-MODEL.md) **consumes** the resulting relationship projection rather
>    than owning either half. What remains open is the register-naming question itself — whether
>    `M-AUTH`/`M-FAC` or `M13`/`M14` survives a crosswalk — which is still §19 Q12.
> 2. Ownership of observation is contradicted. §20 of this document states that `M-OBS` and all
>    belief scoring belong to [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md).
>    [`PERSON-MODEL.md`](PERSON-MODEL.md):471 assigns the same function (**M12 OBSERVABILITY**,
>    "produces the public profile and the player intelligence profile") to
>    [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md). Verified:
>    `BELIEF-AND-KNOWLEDGE-MODEL.md` contains no `M-OBS` and no mechanism register at all.
>
>    **✔ ANSWERED — founder decision 1A, 19 July 2026.** Observation is owned by
>    [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) (DRAFT, 19 July
>    2026). `M-OBS` is specified in [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md)
>    §5, which retains this document's §6 definition and widens it from decisions to any world
>    event. It decomposes into `M-OBS-EXP`, `M-OBS-ACQ`, `M-OBS-ATTR` and `M-OBS-SURF`. §20's
>    assignment of `M-OBS` to [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) is
>    superseded. **M12 OBSERVABILITY is superseded** and split: the observable surface is
>    `M-OBS-SURF`, alias and concealed-identity resolution is `M-OBS-ATTR`, and clearance-gated event
>    observability is `M-OBS-EXP`; M12's clause assigning view production to
>    [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) is withdrawn,
>    because view production is [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2 and presentation is
>    that design document, and neither is a simulation mechanism. This document is a **client**: it
>    emits decisions, implementations and divergences as world events, and that document determines
>    who observes them.
> 3. Both documents claim to succeed the same inert field. §8.4 step 3 and §14 row 11 here name
>    `M-VETO`/`M-LEG` as the successor to `MicroAgent.constraints`;
>    [`PERSON-MODEL.md`](PERSON-MODEL.md):461 names **M2 FEASIBILITY-GATE** as succeeding the same
>    field. At most one can be the successor, or the succession must be explicitly split.
>
> The founder requires "a common entity ontology" under which mechanisms are consistent (:322-334).
> Two sibling specifications with incompatible registers and orphaned cross-ownership do not deliver
> one. The natural owner of a single shared register, or of an explicit identifier crosswalk, is
> [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) — but that is an owner decision, not one this document
> may take.

---

## 3. Plain-English summary

Today, MERIDIAN represents a government department as a single record with a job title, four
personality numbers and three resource numbers, and once per tick it asks a language model what that
department would like to do. Whatever comes back is looked up in a small table of pre-written
effects and applied to the country's national statistics. There is one voice, one opinion, one
action, and no possibility of internal disagreement.

That is not how organisations behave. A shipping company deciding whether to keep sailing through a
dangerous strait does not have *an opinion*. Its chief executive is thinking about the company's
reputation. Its operations division is thinking about whether crews will be killed. Its insurers are
thinking about how much exposure they are carrying and whether to keep covering the route at all.
Its lawyers are thinking about who gets sued if a vessel is lost after a warning was ignored. Its
investors are thinking about the share price this quarter. Its crew union is thinking about whether
to refuse to sail. Its regional managers are thinking about the local officials they have to keep on
side, and about what happens to them personally if head office issues an order the port authority
resents.

The company's decision comes out of that argument. Sometimes it is a decision nobody in the room
actually wanted. Sometimes it is announced and then quietly not implemented, because the people who
would have to implement it disagree. Sometimes it leaks, because the division that lost the argument
wants the outside world to know it lost.

This document specifies how MERIDIAN will represent that. The core of it is:

- An organisation will be made of **internal blocs** — departments, factions, professional
  communities, ownership interests, labour interests — each with its own preferences, its own formal
  power and its own informal leverage.
- An organisation's action will be **computed by an arbitration procedure** over those blocs, not
  chosen by a single decision-maker. The procedure itself differs by organisation: a family firm, a
  board-governed company, a ministry bound by statute and a militia do not resolve internal
  disagreement the same way.
- Losing an internal argument will have **consequences**: dissent is recorded, cohesion falls, leaks
  become more likely, and implementation of the decision can be slow-rolled by the bloc that has to
  carry it out.
- What an organisation **says** it is for and what it is **actually** optimising will be separate
  fields, and the gap between them will be discoverable by the player only through evidence, never
  handed over as fact.
- A country will not be one agent. Its government, courts, military, regional authorities,
  businesses and public will each be their own entity, each running their own arbitration, and they
  will be permitted to contradict each other — including in ways that make a policy fail after it
  has been lawfully ordered.

The single greatest risk to this specification is **fake depth**: writing beautiful attribute lists
that produce nothing but text. The founder names it as the main failure mode
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):241-254), and MERIDIAN
already has a proven instance of it — a cohort's population figure that nothing reads, which allowed
a demo value to sit in the repository wrong by a factor of about sixty-three without producing a
single symptom ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.10).
Every attribute in §12-14 therefore names the mechanism that reads it. §15 lists, without excuse,
every attribute from the source record that this specification **could not** connect to a mechanism.

---

## 4. The central principle: an organisation is not a person

The source record states it flatly:

> An organisation should not behave like one person. Different departments and factions should
> disagree.
> — [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):104

This is not a richness requirement. It is a **causal** requirement, and it is the difference between
an organisation being a source of surprise and an organisation being a mouthpiece. Four consequences
follow, and each is specified in this document:

**(a) An organisation's action must be an output, not an input.** No field on an organisation will
say what it does. The action must be produced by `M-ARB` (§8) from bloc preferences, formal power,
informal leverage and the decision procedure. If a designer wants an organisation to behave
differently, they must change a pressure, not the outcome.

**(b) The losing side must persist.** A decision must emit a **dissent record** naming which blocs
opposed it, how strongly, and on what grounds. That record is what makes later leaks, resignations,
splits, slow-rolling and internal sabotage explainable rather than arbitrary.

**(c) Deciding and doing must be separable.** An organisation deciding on a course of action does
not mean the action occurs. Implementation is specified as a separate step (`M-CONT`, §11) performed
by whichever bloc or subordinate entity actually has to carry it out, and their compliance is
probabilistic and traceable.

**(d) The organisation's own belief about itself must be a separate object from the truth.** A
ministry may genuinely believe it is protecting the public while actually optimising for the
minister's survival. That is not deception; it is self-understanding, and §10 specifies it as one of
the four views.

**In plain English:** we are specifying a machine that argues with itself, records who lost, and
lets the losers make trouble afterwards.

---

## 5. What exists today, and where this contradicts it

This section is the honest boundary. Everything cited here **exists** in the repository now.

### 5.1 What exists

| Structure | Location | What it actually is today |
|---|---|---|
| `MicroAgent` | `scaffold/backend/app/simulation/schemas/agent_schema.py:154-184` | The only individual/institutional actor structure. Fuses a *person* and an *institutional role* into one record: `agent_id`, `role`, `agent_class`, `biography_ref`, `objectives`, `beliefs`, `traits`, `resources`, `relationships`, `information_access`, `constraints`, `memory`. |
| `AgentTraits` | `agent_schema.py:122-130` | Four scalars: `risk_tolerance`, `status_seeking`, `institutional_trust`, `corruption_susceptibility`. |
| `AgentResources` | `agent_schema.py:133-140` | Three scalars: `budget_control_usd_m`, `political_capital`, `personal_network_reach`. |
| `Objective` | `agent_schema.py:115-119` | `goal` (string tag) plus `priority` (0..1). |
| `MicroAgent.constraints` | `agent_schema.py:181-183` | `list[str]`, documented as "Hard legal/procedural constraints on the agent". |
| `InstitutionalAgent` | `scaffold/backend/app/simulation/agents/institutional_agent.py:18-41` | A Mesa `Agent` wrapper. Its entire per-tick behaviour is to call `llm_gateway.propose_action` and store the result. |
| `MeridianModel.step` | `scaffold/backend/app/simulation/engine.py:147-180` | Iterates institutions in list order; for each, takes at most one proposal, prices it, applies it. |
| `_validate_and_price` | `engine.py:121-130` | `ACTION_EFFECTS.get(proposal.action_type, {})` — a dictionary lookup. |
| `ACTION_EFFECTS` | `engine.py:35-43` | Seven action types, each mapped to a fixed macro delta. The entire action vocabulary of the simulation. |
| `MacroState` / `MacroIndicators` | `scaffold/backend/app/simulation/schemas/macro_schema.py:73-87`, `:40-70` | A country as 18 national scalars in one flat object. |
| `MacroStateHolder.apply_deltas` | `scaffold/backend/app/simulation/agents/macro_state.py:23-47` | The only write path for national numbers. Applies **top-level scalars only**; silently skips nested blocks (`:40-41`) and silently skips unknown keys (`:37-38`). |
| `Relationship` | `agent_schema.py:190-200` | A schema only. Never instantiated anywhere in `scaffold/backend/app`. One `valence`, one `trust`, one `dependency`, one `last_interaction_tick`. |
| `ActionProposal` | `agent_schema.py:374-393` | The only object the LLM gateway may return (`llm_gateway.py:35`). Carries no authority to change numbers. **This works, and this document builds on it.** |
| Scenario agents | `scaffold/scenarios/kestral-strait.json:241-388` | Six institutional agents: `head-of-government-varo` (`:243`), `min-defence-oduya` (`:266`), `min-finance-serel` (`:298`), `min-foreign-affairs-lind` (`:320`), `intel-lead-navarro` (`:345`), `strat-comms-adeyemi` (`:367`). None carries a `relationships` key. |

### 5.2 Where this specification contradicts what exists

These are contradictions, not extensions. They are stated plainly so that no reader mistakes this
document for a description of an incremental change.

**C1 — One role, one action, no disagreement.** `InstitutionalAgent.step`
(`institutional_agent.py:26-41`) produces **exactly one** `ActionProposal` per tick from **one**
role, with no internal structure of any kind. `MicroAgent` has no faction field, no department
field, no membership field, no cohesion field and no decision-process field. The source record
requires the opposite (:104-111). This is a behavioural contradiction, not a missing column: the
one-agent-one-proposal loop at `engine.py:159-173` would have to be replaced by a two-stage
arbitration-then-implementation loop.

**C2 — A country is one flat object.** `MacroState` (`macro_schema.py:73-87`) is a single
undifferentiated national aggregate. The source record states that the country "should not be a
single agent" and that "the government, public, military, courts, businesses and regional
authorities may all react differently" (:121-122). §11 therefore specifies a **decomposition**: the
existing 18 indicators are demoted to a *derived aggregate view* over lower-tier entities. That is
not an added field; it inverts what is authoritative. **It cannot be decided by this document** —
P0.4 (the authoritative-state contract, [`../../HANDOFF.md`](../../HANDOFF.md):75) must settle it.

**C3 — Entity-owned state is unreachable by the only write path.** Any organisation state is
inherently nested. `apply_deltas` (`macro_state.py:23-47`) handles top-level scalars only and skips
nested blocks and unknown keys **in silence** (`:37-41`). An organisational effect written through
that path would produce no error, no warning and no symptom — the same silent-failure class the
audit records at §5.10 and A3 §1. Organisation state therefore requires a different write path, and
that path must be strict: unknown or unroutable keys must raise, not continue.

**C4 — The organisation's action vocabulary is hardcoded in engine code.** `ACTION_EFFECTS`
(`engine.py:35-43`) contains seven actions and their magnitudes. An arbitration mechanism produces
decisions over an option set that must be scenario data, not engine constants (audit §5.7). Note
also that `_validate_and_price` (`engine.py:121-130`) is passed only the proposal and never the
agent spec, so an organisation's own constraints are structurally *unreachable* from the gate
(A3 §3, structural note) — not merely unconsulted.

**C5 — `constraints` is documented as hard and is inert.** `agent_schema.py:181-183` describes
"Hard legal/procedural constraints". A3 proved by substitution that removing them changes nothing:
the 40-tick state hash is identical with and without (`1af9170525db` in both cases, A3 §3). The veto
and legality mechanisms specified here (`M-VETO`, `M-LEG`) are the intended successors to that
field, and must not be described as extending a working feature.

**C6 — There is no separation between a person and the role they occupy.** `MicroAgent`
(`agent_schema.py:154-184`) has an `agent_id` that encodes a surname (`min-defence-oduya`,
`kestral-strait.json:266`) but no person record: no name field, no age, no history. This document
depends on [`PERSON-MODEL.md`](PERSON-MODEL.md) resolving that separation, because a bloc is led by
a *person* whose biography shapes the preference they bring into the room, and the organisation must
survive that person being replaced.

**C7 — Mesa as the substrate is an open decision.** `InstitutionalAgent` extends `mesa.Agent`
(`institutional_agent.py:18`), but the audit records as an open owner decision whether Mesa remains
the ABM substrate at all (audit §8, decision 3), noting it is currently vestigial. This document is
therefore written **substrate-neutral**: it specifies arbitration as a pure function over records,
not as agent-class behaviour, so that it does not prejudge that decision.

---

## 6. The mechanism register

**In plain English:** this is the list of moving parts. Every attribute specified later in the
document must point at one of these. If an attribute cannot point at one, it is decoration, and §15
lists it as a candidate for deletion rather than quietly keeping it.

Every mechanism below is **specified, not implemented**. The "Prerequisite" column names what must
land first; "—" means the mechanism depends only on other mechanisms in this table.

| ID | Mechanism | What it must do | Prerequisite |
|---|---|---|---|
| `M-ARB` | **Internal arbitration** | Must resolve competing bloc preferences into one organisational decision plus a dissent record, using the organisation's own decision procedure. The core mechanism of this document. | Named RNG substreams (§16) |
| `M-VETO` | **Veto and blocking rights** | Must allow a named bloc, external dependency or legal instrument to remove an option from the option set before arbitration, or to nullify a decision after it. | `M-ARB` |
| `M-CAP` | **Capability feasibility gate** | Must reject options the organisation cannot physically, technically or geographically perform, before they are voted on. | — |
| `M-RES` | **Resource pricing and depletion** | Must price a decision in money, staff, political capital and time, deplete it, and make the organisation unable to act when depleted. | P0.7 (time semantics) |
| `M-LEG` | **Legal exposure and liability** | Must accumulate liability from decisions taken against recorded advice or obligation, and convert it into future cost, constraint and reputational risk. | `M-ARB` dissent record |
| `M-COH` | **Cohesion, morale, defection and split** | Must update cohesion and morale from arbitration outcomes and outcomes-in-the-world, and trigger resignation, defection, industrial action or organisational split at thresholds. | `M-ARB` |
| `M-LEAK` | **Dissent-driven disclosure** | Must convert unresolved internal dissent into a probabilistic disclosure event that changes what other entities know. | `M-COH`, P0.6 |
| `M-REP` | **Reputation update** | Must maintain public reputation and private (elite/peer) reputation as separate values updated by different evidence. | `M-DIV` |
| `M-DEP` | **Dependency propagation** | Must propagate shocks along funding, supply, insurance, licensing, patronage and alliance edges, including withdrawal of a dependency as a coercive act. | [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) |
| `M-MEM` | **Institutional memory and precedent** | Must bias bloc preferences toward or against options that resemble recorded past decisions and their recorded outcomes. | P0.6 |
| `M-RECR` | **Membership and recruitment flow** | Must move persons and cohort weight into and out of an organisation over time, changing bloc composition and therefore future arbitration outcomes. | [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) |
| `M-GEO` | **Geographic presence gating** | Must determine where an organisation can act, be observed, be regulated and be disrupted. | — |
| `M-INF` | **Influence weighting into aggregation** | Must convert an organisation's wealth, organisation, strategic position and political access into aggregate influence that is *not* proportional to its headcount. | P0.5, [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) |
| `M-DIV` | **Mission-versus-priority divergence** | Must compute the gap between stated justification and actual objective for each decision, accumulate it, and make it discoverable through evidence rather than declaration. | `M-ARB` |
| `M-SUCC` | **Role occupancy and succession** | Must handle a person entering, leaving or being removed from an organisational role, carrying the organisation's state forward while changing the preferences brought into arbitration. | [`PERSON-MODEL.md`](PERSON-MODEL.md) |
| `M-CONT` | **Implementation compliance and contradiction** | Must model the gap between an entity deciding something and a subordinate or peer entity actually doing it, including refusal, delay and partial compliance. | `M-ARB`, `M-COH` |
| `M-OBS` | **Observation and evidence emission** — *specified elsewhere; see the note below* | Must determine which entities observe a decision, an implementation and a divergence, and with what evidential quality. **Owned by [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5 as of 19 July 2026.** This document is a client and must not respecify it. | [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md), P0.6 |
| `M-AUTH` | **Role authority** (umbrella; discharges `PERSON-MODEL.md`'s **M13 ROLE-AUTHORITY**) | Must resolve what an entity is *empowered* to do through the office it holds — offices and attached powers, jurisdiction, delegation and acting authority, appointment, removal, expiry and suspension, command chains, and the gap between formal and practical authority. Decomposes into four sub-mechanisms in §7.3. Not a buildable unit on its own. | [`PERSON-MODEL.md`](PERSON-MODEL.md), `M-SUCC` |
| `M-FAC` | **Faction definition, membership and structure** (discharges the *organisation half* of `PERSON-MODEL.md`'s **M14 FACTION-ALIGNMENT**) | Must define what a faction is, who may belong to it and on what rule, what formal positions it holds, and how it is structured — and must supply that structure to `M-ARB` as bloc composition. **It must not carry the person-to-faction alignment edge**, which is [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md)'s. §7.4. | [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) |
| `M-EST` | **Option outcome estimation** ⚠ | Must produce `outcome_estimate(o, d)` — the estimated consequence of option `o` on interest dimension `d`, with a variance term — for consumption by `M-ARB` step 4. **Specified as a requirement, not as a design.** See the note below: this mechanism is named because `M-ARB` cannot function without it, and its interior is not settled here. | `M-ARB`, [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md), [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) |
| `M-LEAD` | **Role-occupant modulation of bloc interests** ⚠ | Must specify, and **bound**, how the person occupying a bloc's leading role modulates that bloc's `interest_vector`. See the constraints below, which are mandatory. | [`PERSON-MODEL.md`](PERSON-MODEL.md), `M-SUCC` |

**`M-EST` is a hole this document names rather than hides.** `outcome_estimate(o, d)` is the
load-bearing term of the whole arbitration mechanism: it is what converts an option into a
per-dimension consequence, and every bloc score in §8.4 step 4 depends on it. Before this revision
the register contained no mechanism producing it, while three attributes were nonetheless marked
mapped on its strength. Naming `M-EST` does **not** repair that — a mechanism that is named but
undefined is a weaker claim than a mapping (the test this document already applies at §15-R3), and
`M-EST` must be treated as undefined until the following four questions are answered, which is
§19 Q13:

1. What produces the estimate — a scenario-authored consequence table, a forward model, or a
   propagation over dependency edges?
2. **Whose beliefs is it evaluated under?** Step 4 requires scoring on the bloc's beliefs, not
   ground truth, so `M-EST` must be evaluable per-observer or the belief requirement is cosmetic.
3. Where does the variance term consumed by `risk_posture` come from?
4. How do relationship edges (rivals, competitors, customers, suppliers) enter it? §12 row 16,
   §14 row 10 and §14 row 16 all depend on this and are marked ⚠ accordingly (§15-R10).

Until those are answered, `M-ARB` is a formula with an unspecified term in it, and §9's numbers are
**author-supplied illustrations, not computed outputs**. That is stated plainly in §9.

**`M-LEAD` is where identity enters the arithmetic, and it is therefore fenced.** The bloc sketch
(§8.2) carries the comment that a leader's "biography shapes interest weights". That is the bridge
between [`PERSON-MODEL.md`](PERSON-MODEL.md) and organisational behaviour, and §12 row 5 depends on
it — but before this revision it was stated only in a code comment and specified nowhere. Both
failure modes were live: if nothing implements it, `led_by` is decoration and §12 row 5's causal
claim is false; if something implements it unspecified, the person→interest map is exactly where the
founder's stereotype switch gets built. The following constraints are therefore mandatory on any
implementation of `M-LEAD`:

- Modulation must be **additive and bounded**, never assignment. A leader shifts a bloc's existing
  interest weights within a stated ceiling; a leader must never *set* an interest vector.
- Modulation must act on **weights**, never on options. `M-LEAD` must not make any option more or
  less likely to be selected except through the weights it shifts, and must never select.
- **No sensitive identity attribute may enter `M-LEAD` directly.** Ethnicity, religion, nationality
  and language must not appear as inputs. Only **lived-experience records that are themselves
  event-sourced** — a recorded prior posting, a recorded loss, a recorded professional formation —
  may modulate weights, which is the same indirection layer
  [`PERSON-MODEL.md`](PERSON-MODEL.md) requires at M17.
- This is the organisational instance of the founder's rules at
  [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):90-91 ("changes
  probabilities … should not become a stereotype switch") and :305-306 (sensitive identity affects
  social experience, never competence, morality or intelligence). Those rules bind here, at the
  interface, not only at §18.

`M-LEAD` does **not** discharge [`PERSON-MODEL.md`](PERSON-MODEL.md):473's **M14
FACTION-ALIGNMENT**, which assigns to this document the separate problems of which bloc a person
aligns with and their individual defection probability. ~~Neither M14 nor **M13 ROLE-AUTHORITY** is
specified here.~~ See §2 and §19 Q12.

> **Superseded 19 July 2026 — founder decisions 1B and 1C.** The struck sentence was true when
> written and is retained as the record of it. It is no longer true. **M13 ROLE-AUTHORITY is
> specified here as `M-AUTH` (§7.3)**, and the **organisation half of M14 is specified here as
> `M-FAC` (§7.4)**. The first sentence of this paragraph still holds and is load-bearing: `M-LEAD`
> remains a distinct mechanism from both, and none of the three may absorb the others.
>
> The boundaries, stated so that no reader collapses them:
>
> - `M-LEAD` modulates a bloc's `interest_vector` from the biography of the person leading it. It
>   changes **what a bloc wants**.
> - `M-AUTH` resolves what an office **empowers its holder to do**, and therefore whether an act is
>   valid, delegable, expired or suspended. It changes **what an act is worth in law and in the
>   chain of command**, not what anybody wants.
> - `M-FAC` defines factions and the rule for who may belong. It changes **which blocs exist and who composes
>   them**.
> - The remaining half of M14 — the directional, historied person-to-faction alignment and loyalty
>   edge, and its changing strength — is **not here at all**. It is
>   [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md)'s, and duplicating it here would create two
>   sources of truth for one fact, which §7.1 already refuses for every other edge.
>   [`PERSON-MODEL.md`](PERSON-MODEL.md) consumes the projection of that edge and owns neither half.
> - **Individual defection probability**, which the struck sentence named as part of M14, is
>   therefore *not* `M-FAC`. It is a function of the alignment edge (owned by the graph), the
>   grievance ledger and `M-COH`. `M-FAC` supplies only the faction a person could defect *to*.

**The rejection rule.** This document proposes — and flags in §19 as an owner decision — that any
attribute which cannot name a reading mechanism from this table is **struck from the specification,
not deferred**. The empirical case is audit §5.10: an unread attribute produced no error when it was
wrong by 63×, and MERIDIAN currently has no invariant tests at all (audit §6.34) that would catch a
repeat.

---

## 7. The composite organisation entity

**In plain English:** an organisation record will hold three things — what it is, what it is made
of, and how it decides. Almost nothing about its behaviour will be written into it directly.

### 7.1 Shape

```python
# SKETCH — NOT IMPLEMENTED. Illustrative only; field names, types and bounds are not settled.
# This does not exist in scaffold/ and must not be added there while Phase 0 is in progress.

class OrganisationEntity(EntityBase):        # EntityBase is specified in ENTITY-ONTOLOGY.md
    org_id: EntityId
    org_kind: OrgKind                        # ministry | court | armed_service | firm | union |
                                             # party | media_outlet | religious_body | militia |
                                             # ngo | regulator | central_bank | regional_authority
    legal_status: LegalStatus                # incorporation/charter/mandate + jurisdiction refs
    founding: FoundingRecord                 # founding tick-or-date, founding doctrine refs,
                                             # founding relationship seeds  -> M-MEM
    public_mission: MissionStatement         # DECLARED. Never read by M-ARB. See §10.
    actual_priorities: list[WeightedObjective]   # AUTHORITATIVE. Read by M-ARB. See §10.
    self_understanding: SelfUnderstanding    # what the org believes it is optimising. See §10.
                                             # ⚠ READ BY NO MECHANISM AS SPECIFIED. See §15-R11.
                                             # Rendered in the §10.3 view table and the dossier and
                                             # nowhere else, which is this document's own definition
                                             # of fake depth. Disposition is an owner decision.

    blocs: list[InternalBloc]                # §8. Minimum 1; a one-bloc org is a modelled
                                             # special case, not the default.
    decision_procedure: DecisionProcedure    # §8.3
    offices: list[Office]                    # ADDED 19 July 2026 (founder decision 1B). The office
                                             # exists independently of who holds it: attached
                                             # powers, jurisdiction, expiry, suspension  -> M-AUTH
    role_occupancies: list[RoleOccupancy]    # role -> person_id, authority, tenure  -> M-SUCC,
                                             # and -> M-AUTH for the powers that occupancy confers
    factions: list[FactionRecord]            # ADDED 19 July 2026 (founder decision 1C). Faction
                                             # definitions, membership rules, formal positions and
                                             # structure  -> M-FAC, M-ARB (bloc composition).
                                             # The person-to-faction ALIGNMENT EDGE IS NOT HERE:
                                             # it is RELATIONSHIP-GRAPH.md's. See §7.4.
    command_chain: list[CommandEdge]         # ADDED 19 July 2026 (founder decision 1B). Which
                                             # office may direct which  -> M-AUTH, M-CONT

    capabilities: list[Capability]           # -> M-CAP
    assets: AssetLedger                      # -> M-RES, M-CAP
    funding: list[FundingSource]             # -> M-RES, M-DEP
    geographic_presence: list[PresenceRecord]  # -> M-GEO
    obligations: list[Obligation]            # statutory, contractual, treaty  -> M-LEG, M-VETO
    legal_exposure: LegalExposureLedger      # -> M-LEG

    cohesion: float                          # 0..1  -> M-ARB (dissent tolerance), M-COH
    morale: float                            # 0..1  -> M-COH, M-CONT
    reputation_public: ReputationRecord      # -> M-REP
    reputation_private: ReputationRecord     # -> M-REP  (distinct evidence base)

    standing_strategy: StandingStrategy      # current posture; biases option generation -> M-ARB
    open_disputes: list[DisputeRecord]       # unresolved internal arguments -> M-COH, M-LEAK
    memory: InstitutionalMemory              # precedent index -> M-MEM
```

Deliberately **absent** from this sketch, and the absences matter:

- **No `action` field, and no `preferred_action` field.** Actions are outputs of `M-ARB` only (§4a).
- **No relationships block.** Rivals, partners, patrons, suppliers, regulators, insurers and
  competitors are all directional edges owned by [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md).
  Duplicating them here would create two sources of truth for the same fact, and this document
  chooses the graph.
- **No belief map.** What the organisation *knows* is owned by
  [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md). What it *wants* (`actual_priorities`)
  and what it *thinks it wants* (`self_understanding`) live here, because those are properties of
  the organisation's constitution rather than of its information state.
- **No free-text description as authoritative state.** Prose is generated from this record by the
  LLM and never read back (§16).

### 7.2 Relationship to `MicroAgent`

`MicroAgent` (`agent_schema.py:154-184`) is a **person-and-role fused into one record**. This
document's position is that it decomposes into three things: a person
([`PERSON-MODEL.md`](PERSON-MODEL.md)), a `RoleOccupancy` linking that person to an organisation,
and the organisation itself. Whether that decomposition happens or `MicroAgent` is extended in place
is an owner decision (§19, Q1), because the two produce very different migration costs and different
answers to "what happens when a minister is replaced".

Note that `MicroAgent.objectives` (`agent_schema.py:169`) is the nearest existing analogue of
`actual_priorities`, and `MicroAgent.constraints` (`:181-183`) of `obligations`. Both are read by
nothing today (audit §5.4; A3 §3).

### 7.3 Role authority (`M-AUTH`) — added 19 July 2026, founder decision 1B

**In plain English:** a job comes with powers. A minister may sign a thing a civil servant may not.
A deputy may sign it only while the minister is abroad, and only up to a limit. A suspended officer
may not sign it at all, even though the post is still theirs. Somebody who has been in post for
twenty years and knows everyone may in practice get things done that the person formally above them
cannot. All of that is about the **office**, not about the person's opinions — and it is a different
thing from what the person *wants*, which is `M-LEAD`.

This subsection specifies **M13 ROLE-AUTHORITY**, which
[`PERSON-MODEL.md`](PERSON-MODEL.md):472 assigned to this document and which this document did not
previously specify. The founder ruled on 19 July 2026 that the assignment stands and named nine
things it must own: roles and offices, authority attached to a role, jurisdiction, delegation,
appointment and removal, acting authority, conflicts between formal and practical authority,
organisational command chains, and authority expiry and suspension.
[`PERSON-MODEL.md`](PERSON-MODEL.md) may **reference** a person's current role — that is what
`state.current_role` (`PERSON-MODEL.md`:694) is for — but must not own the mechanism.

`M-AUTH` is an **umbrella and is not a buildable unit on its own**, on the same footing as `M-OBS`
in [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5. It decomposes
into four sub-mechanisms, each of which names its readers and the behaviour it changes, because a
mechanism that cannot name those is fake depth by this document's own rule (§6).

> ### SPECIFICATION — NOT IMPLEMENTED
> No office, authority, delegation or command-chain structure exists anywhere in MERIDIAN's code.
> `MicroAgent.role` (`agent_schema.py:154-184`) is a bare string, and nothing reads it to determine
> what its holder may do. The "What it must do" column below states a requirement, not a behaviour.

| Id | Sub-mechanism | What it must do | What reads it, and what changes |
|---|---|---|---|
| `M-AUTH-OFF` | **Office, attached powers and jurisdiction** | Must hold the office as a structure independent of its occupant: which acts it may authorise, over which entities, in which territory or subject domain, and to what magnitude. Sole writer of `Office`. | `M-CONT` step 1 (§11.3): an act taken outside the office's powers or jurisdiction must fail the authority check and become **challengeable**, which opens the §11.3 step 2 challenge window and admits a court's own `M-ARB`. `M-VETO` at `M-ARB` step 3: an option requiring authority the organisation does not hold must have its threshold raised and liability attached under `M-LEG` if taken anyway. |
| `M-AUTH-DEL` | **Delegation and acting authority** | Must permit a holder to transfer a bounded subset of an office's powers to another occupant for a bounded period, and must record the narrowing. Acting authority (a deputy standing in) is specified as delegation with an automatic expiry, not as a distinct kind. | `M-CONT` step 1: a delegate's act must pass the authority check **only within the delegated subset**, so an act valid for the principal can be ultra vires for the delegate. `M-ARB` step 5: where the procedure is `command` or names a `chair_bloc`, the acting occupant exercises the chair or command position, so the same bloc scores can resolve differently while a principal is absent. |
| `M-AUTH-TEN` | **Appointment, removal, expiry and suspension** | Must make entry to and exit from an office an **event with a cause**, and must distinguish four exits that are not the same: term expiry, removal, suspension (the post is retained, the powers are not), and vacancy. | `M-SUCC` consumes it and carries organisational state across the transition. `M-LEAD` re-derives the bloc `interest_vector` modulation from the new occupant's biography, within its §6 bounds, so **replacing a person changes future decisions without changing the organisation**. `M-COH`: a removal that a bloc opposed must register as dissent and cost cohesion. A suspended office must fail `M-AUTH-OFF`'s check for the duration, which is how an organisation can be lawfully paralysed. |
| `M-AUTH-PRAC` | **Formal versus practical authority** | Must carry the gap between what an office is empowered to do and what its holder can actually get done, and must derive that gap **only** from recorded state: tenure length, precedent of compliance (`M-MEM`), patronage and dependency edges ([`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md)), and private reputation. | `M-CONT` step 3: `compliance_propensity(Y)` must read practical authority, not formal authority alone, so a formally superior organ can issue a lawful order that is nominally complied with. `M-REP` private reputation: an order that is refused must damage the ordering office's practical authority, making the next refusal more likely — a feedback loop, not a constant. |

**Three boundaries, stated because each is a live double-counting hazard.**

1. **`M-AUTH` versus `M-VETO`.** They act on different objects. `M-VETO` acts on an **option**,
   inside arbitration, before the organisation has decided. `M-AUTH` acts on an **act**, after the
   decision, and determines whether it was valid. An organisation may lawfully decide to attempt
   something it has no authority to do; that is the §11.3 ultra vires case, which this document
   already permits, and it must not be foreclosed by routing authority through the veto gate.
2. **`M-AUTH-PRAC` versus `InternalBloc.informal_leverage`.** Both model power the rules do not
   grant, and they must not be summed. `informal_leverage` operates **inside** one organisation's
   arbitration, bounded by `leverage_admissibility` (§8.3). `M-AUTH-PRAC` operates **between**
   entities, at implementation, and is read by `M-CONT` and `M-REP` only. Any implementation that
   lets one feed the other must state the transfer explicitly; none is specified here.
3. **`M-AUTH` versus `M-LEAD`.** `M-AUTH` must never modify an `interest_vector`, and `M-LEAD` must
   never modify an office's powers. The §6 bounds on `M-LEAD` — additive, bounded, no sensitive
   identity attribute as a direct input — are **not** inherited by `M-AUTH`, because `M-AUTH` takes
   no biographical input at all. That is deliberate: authority must attach to the office, and an
   implementation in which who a person *is* changes what their office *may do* is the founder's
   stereotype switch in its most consequential form. Sensitive identity attributes must not appear
   as inputs to any sub-mechanism above, including `M-AUTH-PRAC`, whose inputs are enumerated in
   its row precisely to close that gap.

### 7.4 Factions (`M-FAC`) — added 19 July 2026, founder decision 1C

**In plain English:** a faction is a named group with a shape — who is allowed in, who holds which
position in it, how it is organised. Whether a *particular person* is loyal to it, how loyal, and
whether that loyalty is rising or falling, is a different kind of fact: it is a link between two
things, it has a direction and it has a history. This document owns the group. The relationship
graph owns the link. Neither may hold the other's half.

The founder split **M14 FACTION-ALIGNMENT** three ways on 19 July 2026, with an explicit instruction
that the mechanism must **not** be duplicated:

| Half | Owner | What it holds |
|---|---|---|
| Faction definitions, membership rules, formal positions, faction structure | **This document**, as `M-FAC` | What the faction is and how it is composed. |
| The directional, historied person-to-faction alignment and loyalty relationship, and its changing strength | [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) | Who is aligned to it, how strongly, since when, and on what history. |
| — | [`PERSON-MODEL.md`](PERSON-MODEL.md) | **Consumes** the resulting relationship projection. Owns neither half. |

> ### SPECIFICATION — NOT IMPLEMENTED
> No faction, party or membership structure exists in MERIDIAN's code or in
> `kestral-strait.json:241-388`. `Relationship` (`agent_schema.py:190-200`) is a schema that is
> never instantiated anywhere in `scaffold/backend/app`, so the edge half has no carrier either.

```python
# SKETCH — NOT IMPLEMENTED.

class FactionRecord(BaseModel):
    faction_id: EntityId
    label: str                          # presentation only; never read by any mechanism
    membership_rule: MembershipRule     # who may belong: by office, by cohort, by patron,
                                        # by profession, by region, or by invitation
                                        # -> M-FAC, M-RECR
    formal_positions: list[Office]      # positions the faction itself confers -> M-AUTH
    structure: FactionStructure         # cellular | hierarchical | patronage_network |
                                        # caucus | tendency  -> M-FAC, M-LEAK, M-COH
    hosted_in: Optional[EntityId]       # the organisation it sits inside, if any.
                                        # None => a cross-organisational faction; see Q18.

    # DELIBERATELY ABSENT: no members list, no loyalty scores, no alignment strengths.
    # Those are edges in RELATIONSHIP-GRAPH.md. Putting them here would create two
    # sources of truth for one fact, which §7.1 refuses for every other edge.
```

**What `M-FAC` must do, and what changes because of it.** `M-FAC` must resolve a faction's
definition and structure into **bloc composition** for `M-ARB`. That is its causal payload and it is
the reason it is not decoration:

- **Membership rule → who is in the bloc → what the bloc wants.** A faction recruiting by office
  and a faction recruiting by region produce different `InternalBloc.membership`, therefore
  different `interest_vector` aggregates, therefore different scores at `M-ARB` step 4 and different
  outcomes at step 6. Changing the rule must change decisions.
- **Formal positions → `M-AUTH`.** A faction that controls appointments to an office controls, via
  `M-AUTH-TEN`, who exercises that office's powers. This is the specified route by which factional
  capture of an institution becomes observable rather than asserted.
- **Structure → `M-LEAK` and `M-COH`.** A cellular faction and an open caucus must not have the
  same disclosure hazard or the same split threshold. `structure` is where that difference lives, on
  the same discipline §8.3 applies to `decision_procedure`: culture and shape as parameters, never
  as prose.
- **Alignment strength → read, never written.** `M-ARB` step 5's `power(b)` and `M-COH`'s defection
  threshold must read alignment **from the relationship graph's projection**. `M-FAC` must never
  write it. An implementation in which `M-FAC` stores a loyalty number is a duplication defect and
  must be raised, not absorbed.

**Individual defection probability is not `M-FAC`.** `PERSON-MODEL.md`:473 bundled it into M14. On
the founder's split it is a function of the alignment edge (the graph), the `grievance_ledger`
(§8.2) and `M-COH` thresholds. `M-FAC` supplies only the faction a person could defect *to*, and
the structure that determines what defecting costs.

**Unresolved, and referred rather than taken:** a faction inside one organisation is representable
today as an `InternalBloc` of kind `personal_faction` (§8.2), and a faction spanning organisations
is representable as an `OrganisationEntity` of kind `party` (§7.1). `FactionRecord` is a third
shape, and whether all three are needed is not settled by the founder's ruling, which assigned
ownership rather than shape. This is §19 **Q18**, and it is adjacent to Q8.

### 7.5 `InstitutionState` — added 19 July 2026, founder decision 1D

**In plain English:** a ministry, a court, a central bank and a state broadcaster are organisations
with a legal mandate. They are not a different species. So MERIDIAN will not have a second, parallel
description of them — it will have the organisation record, plus the handful of things that are
specifically true of a body that holds a public mandate.

The founder ruled on 19 July 2026 that **the base `InstitutionState` schema and its lifecycle are
assigned to this document**, and that **for current scope an institution is a specialised
organisation**. [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §14 lists this document as the specifier
of an `InstitutionState`, and as of that ruling the listing is correct. The §2 resolution box carries
the ruling in full, including what it deliberately does **not** settle.

**Two standing constraints from the ruling, which bind any later work:**

1. **Versioned subtype extensions are permitted later.** A court and a central bank may each gain a
   versioned extension over this base. The base must not be widened to accommodate them
   speculatively.
2. **A separate institution specification must not be created unless implementation evidence proves
   the organisation abstraction insufficient.** Evidence, not argument, is the trigger. An
   architectural preference is not evidence; a mechanism that demonstrably cannot be expressed over
   `OrganisationEntity` is.

> ### SPECIFICATION — NOT IMPLEMENTED
> No institution record of any kind exists in MERIDIAN's code. The nearest structure is
> `MicroAgent` (`agent_schema.py:154-184`), which fuses a person and an institutional role into one
> record and carries none of the twelve fields below. The table states requirements.

**The base state.** The founder named twelve things the base must support. Each is given below with
the field that must carry it and the mechanism that must read it. Note the finding that falls out of
the table and is the substantive evidence for the ruling: **eleven of the twelve are already carried
by `OrganisationEntity` (§7.1) with no new field at all**, and the twelfth is one field. That is
what "an institution is a specialised organisation" means concretely, rather than as a preference.

| # | Required by the ruling | Carried by | Reading mechanism(s) | What must change because of it |
|---|---|---|---|---|
| 1 | **Mandate** | `legal_status` + `public_mission` + `mandate_instrument` **(new)** | `M-VETO`, `M-LEG`, `M-AUTH-OFF`, `M-ARB` step 1 | Must bound which options are generated at all, and make acting outside the mandate ultra vires and challengeable (§11.3), not impossible. |
| 2 | **Authority** | `offices` + `role_occupancies` + `command_chain` | `M-AUTH` (§7.3) | Must determine whether an act is valid, delegable, expired or suspended, and therefore whether it survives the §11.3 challenge window. |
| 3 | **Capacity** | `capabilities` + `assets` | `M-CAP` at `M-ARB` step 2, `M-CONT` | Must remove options the institution cannot perform, and must set the conversion rate from decision to implemented fact. |
| 4 | **Legitimacy** | `legitimacy: LegitimacyRecord` (as §11.2 carries for a country) | `M-CONT` step 3, `M-COH` | Must determine whether orders become facts. An institution with a valid mandate and no legitimacy must be able to be lawfully ignored. |
| 5 | **Leadership** | `role_occupancies` | `M-SUCC`, `M-AUTH-TEN`, `M-LEAD` | Replacing the leadership must change future arbitration outcomes without changing the institution's identity, mandate or memory. |
| 6 | **Staffing** | `blocs[].membership` | `M-RECR` ⚠, `M-CAP`, `M-INF`, `M-COH` | Must set what the institution can actually do and what a walkout removes. **Conditional**: `M-RECR` is undefined in the document set (§15-R3). |
| 7 | **Budget and resources** | `funding` + `assets` | `M-RES`, `M-DEP` | Must make the institution unable to act when depleted, and must make a funder's withdrawal a coercive act with a named actor behind it. |
| 8 | **Procedures** | `decision_procedure` (§8.3) | `M-ARB` step 5 | Must make the same bloc scores resolve differently in a court, a ministry and a central bank. This is where "a statutory body decides differently from a firm" is carried, as parameters rather than as prose. |
| 9 | **Jurisdiction** | `offices[].jurisdiction` + `geographic_presence` | `M-AUTH-OFF`, `M-GEO`, `M-VETO` | Must determine over whom and where the institution's acts bind, and must make an act outside jurisdiction challengeable. |
| 10 | **Cohesion** | `cohesion`, `morale` | `M-COH`, `M-ARB` steps 5 and 8, `M-CONT` | Must determine whether the institution survives overriding its own members, and whether its decisions are implemented or slow-rolled. |
| 11 | **Internal factions** | `blocs` + `factions` (§7.4) | `M-ARB` steps 4-7, `M-FAC`, `M-LEAK` | The pressures a decision must emerge from (§8). An institution must be able to be factionally captured, and that must be discoverable through evidence rather than declared. |
| 12 | **Current operational posture** | `standing_strategy` | `M-ARB` step 1 | Must bias which options are generated; changing posture must itself be an arbitrated decision with a dissent record, never a setting. |

**The one new field.** `mandate_instrument: Optional[InstrumentRef]` is the only addition the twelve
require: a reference to the statute, charter or constitutional provision that created the
institution and states what it is for. It is what distinguishes an institution from a firm with a
mission statement, and it is read by `M-LEG` (breach accrues exposure), by `M-AUTH-OFF` (it is the
source of the office's powers) and by `M-VETO` (an obligation in the instrument raises an option's
threshold at `M-ARB` step 3). Everything else in the table is `OrganisationEntity` unchanged.

```python
# SKETCH — NOT IMPLEMENTED.

class InstitutionState(OrganisationEntity):    # a SPECIALISED ORGANISATION, not a fourth type
    mandate_instrument: Optional[InstrumentRef]   # the statute/charter/provision that created it
                                                  # -> M-LEG, M-AUTH-OFF, M-VETO
    constitutional_position: Optional[str]        # structured enum, not prose; where it sits in
                                                  # the constitutional order -> M-AUTH-OFF, M-VETO
    lifecycle_state: InstitutionLifecycleState    # see below  -> M-AUTH-OFF, M-CAP, M-CONT
    subtype_extension: Optional[VersionedExtension]   # permitted later per the ruling; MUST be
                                                      # versioned and MUST NOT widen the base
```

**The lifecycle.** Five states, and every transition between them is specified as an **event with a
recorded cause**, on the same footing as an organisational decision. A lifecycle that is a field
nothing writes would be exactly the fake depth this document rejects, so each transition names what
produces it and what it changes.

| State | Entered by | What must change on entry |
|---|---|---|
| `establishing` | An act of a body with authority to create it (`M-AUTH-OFF` on the creating entity), recorded with the creating instrument. | The institution exists as an entity but its offices confer no powers yet, so `M-CONT` step 1 must fail for any act it attempts. |
| `operating` | Commencement of the mandate instrument. | Offices confer powers; `M-ARB` runs; `M-MEM` begins accumulating precedent from its own decisions. |
| `mandate_amended` | A decision by a body with authority to amend, itself arbitrated and dissented. | `mandate_instrument` is superseded, **not replaced silently**: the prior instrument must remain in `memory` as precedent, because an institution's history of mandate change is what makes its drift (§10.4) legible. Option generation at `M-ARB` step 1 must change. |
| `suspended` | Suspension by a superior authority, or by a court under §11.3 step 2. | Offices retain occupancy and lose powers (`M-AUTH-TEN`). `M-CONT` must refuse implementation. Staff, budget, memory and factions persist — a suspended institution is not a deleted one, and its blocs continue to hold grievances. |
| `dissolved` | Dissolution by a body with authority, or collapse via `M-COH` at threshold. | Powers, capacity and funding cease. **Memory, legal exposure and grievance ledgers must not be discarded**: they must transfer to a named successor entity or persist as unowned records, because "what caused this institution to fail" (:188's sibling question) is unanswerable if the evidence is deleted with the entity. |

**What this subsection does not settle.** The residue recorded in the §2 resolution box stands
unchanged: [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §4.2 uses *institution* for a set of rules
constraining other entities, with a trait set carrying neither `holds_beliefs` nor
`possesses_resources` (its §5.3), and this subsection uses it for a mandated organisation that
plainly has both. The ruling assigned ownership and shape; it did not rename the ontology's sense.
`constitutional_order: list[Instrument]` (§11.2) remains closer to that sense than to this one, and
`mandate_instrument` above points into it — so a reader meeting both in one sentence must still
disambiguate by document. **That remains an owner decision** and belongs with the ontology's
taxonomy questions (its §12).

---

## 8. Internal blocs and pressure resolution

This is the heart of the document.

### 8.1 In plain English

An organisation will be made of blocs. A bloc is any group inside — or attached to — the
organisation that has a coherent interest and some way of getting it: a division, a professional
class, an ownership interest, a union, a regional office, a faction loyal to a particular person, or
an external body whose consent is required.

Each bloc has three kinds of power, and they are not the same thing:

- **Formal weight** — the votes, seats or signatures it controls. What the rules say it can do.
- **Informal leverage** — what it can do regardless of the rules: refuse to implement, resign in
  public, leak, strike, withhold expertise, call a friendly politician.
- **Blocking rights** — a hard veto over specific classes of decision. A lawyer's veto over an
  illegal act, an insurer's veto over an uninsurable route, a coalition partner's veto over a
  budget.

A decision is produced by putting the available options in front of the blocs, letting each score
them by its own interests, applying the organisation's decision procedure, and recording what
happened — including who lost and by how much.

### 8.2 The bloc record

```python
# SKETCH — NOT IMPLEMENTED.

class InternalBloc(BaseModel):
    bloc_id: EntityId
    org_id: EntityId
    bloc_kind: BlocKind          # department | profession | ownership | labour | regional |
                                 # personal_faction | external_stakeholder
    label: str                   # presentation only; never read by any mechanism

    interest_vector: dict[InterestDimension, float]
        # e.g. {reputation: .9, safety_of_personnel: .1, liability: .2,
        #       financial_return: .3, political_standing: .6}
        # -> M-ARB. This is what the bloc optimises. It is NOT a preferred action.

    formal_weight: float         # 0..1, normalised within the org  -> M-ARB
    informal_leverage: float     # 0..1  -> M-ARB (procedure-dependent), M-CONT, M-LEAK
    blocking_rights: list[OptionPredicate]   # -> M-VETO

    led_by: Optional[EntityId]   # person_id -> PERSON-MODEL, via M-LEAD (§6), which is the ONLY
                                 # specified route by which a person's biography may modulate this
                                 # bloc's interest_vector, and which is bounded and additive.
                                 # M-LEAD is named-but-undefined; see §6, §15-R12 and §19 Q12.
    membership: MembershipRecord # headcount, cohort composition -> M-RECR, M-INF
    internal_cohesion: float     # 0..1; a divided bloc bargains worse -> M-ARB, M-COH
    risk_posture: float          # 0..1 -> M-ARB scoring of uncertain options
    external_patrons: list[EntityId]   # edges into RELATIONSHIP-GRAPH -> M-DEP

    grievance_ledger: list[GrievanceRecord]   # event-sourced, with onset, cause, evidence,
                                              # resolution -> M-COH, M-LEAK
```

Two notes on this sketch:

- `interest_vector` holds **interests, not actions**. A bloc that prefers a specific action is a
  stereotype switch; a bloc that has interests and scores options against them is a model. This is
  the organisational form of the founder's rule that identity "changes probabilities … it should not
  become a stereotype switch" ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):90-91).
- `grievance_ledger` is deliberately **not** the free-form `list[str]` that
  `Cohort.grievances` uses today (`agent_schema.py:103-105`), because that structure records no
  cause, no onset, no evidence and no resolution, and nothing in the codebase ever adds to it or
  clears it.

### 8.3 The decision procedure

Organisations do not resolve disagreement the same way, and the procedure must therefore be
**data on the organisation**, not a branch in engine code (this is the same discipline
`scaffold/CLAUDE.md` already applies to nation archetypes).

```python
# SKETCH — NOT IMPLEMENTED.

class DecisionProcedure(BaseModel):
    kind: ProcedureKind
        # autocratic        — one occupant decides; other blocs act only through M-CONT/M-LEAK
        # collegial         — weighted mean of bloc scores; chair breaks ties
        # board_vote        — formal_weight only; informal leverage acts before/after, not during
        # bureaucratic      — precedent-dominant; M-MEM weight high, deviation costs cohesion
        # consensus         — requires no bloc below an objection threshold; else deadlock
        # command           — hierarchical; subordinate compliance handled by M-CONT
    chair_bloc: Optional[EntityId]
    quorum: float
    veto_holders: list[EntityId]
    deviation_cost: float        # cohesion penalty for overriding a strongly-objecting bloc
    deadlock_action: DeadlockPolicy   # status_quo | escalate_to_parent | defer_n_ticks | split
    leverage_admissibility: float     # 0..1 — how much informal leverage counts *inside* the room
```

`kind` is the organisation's **culture** expressed as parameters rather than adjectives. This is how
"organisational culture" earns its place in §12 instead of being struck under §15: culture is not a
paragraph, it is `deviation_cost`, `leverage_admissibility`, `risk_posture` distribution across
blocs, and `M-MEM` weight.

### 8.4 The arbitration mechanism (`M-ARB`), step by step

```text
SPECIFIED PROCEDURE — NOT IMPLEMENTED

Input:  organisation record, bloc records, world state, triggering event,
        option set proposed for this decision point
Output: OrganisationDecision + DissentRecord + cohesion/morale deltas + emitted events

1. OPTION GENERATION
   Options are drawn from the scenario's option catalogue, filtered by the organisation's
   org_kind, standing_strategy and the triggering event class.
   The LLM MAY propose an additional option as an ActionProposal (agent_schema.py:374-393).
   It never scores, never weights and never selects. See §16.

   DETERMINISM HAZARD — this is NOT the existing LLM boundary applied unchanged.
   An LLM-proposed option changes BOTH the membership of the set step 6 draws over AND
   the number of draws consumed, so the numeric outcome of arbitration would depend on
   non-deterministic model output. The existing boundary is safe precisely because
   _validate_and_price (engine.py:121-130) maps a proposal onto a FIXED engine-owned
   table; it never enlarges an option space that a seeded draw ranges over. This is a
   materially different exposure and it must be stated rather than inherited.
   P0.6 requires that replay make ZERO model or network calls (HANDOFF.md:87-88).
   Therefore:
     · An LLM-proposed option MUST be captured as a recorded, versioned external input,
       carrying its interpreted structured form and its provenance.
     · Replay MUST consume the recorded option and MUST NOT re-invoke the model.
     · UNTIL that recorded-external-input mechanism exists, step 1 must be specified as
       SCENARIO-CATALOGUE-ONLY, and LLM option proposal must not be built.
   See §16.2 and the §18 dependency diagram.

2. FEASIBILITY GATE  (M-CAP, M-GEO, M-RES)
   Remove options the organisation cannot perform, cannot reach, or cannot afford.
   Removal is recorded with its reason. A removed option is still reportable in the
   explanation trace as an alternative that was possible in principle — this is what
   CHARTER question 7 requires.

3. VETO GATE  (M-VETO)  — RAISES A THRESHOLD; DOES NOT, BY DEFAULT, REMOVE
   A veto by a veto holder, a statutory obligation or an external dependency's stated
   condition is recorded with the vetoing entity's id and must:
     · raise the aggregate score threshold the vetoed option has to clear, and
     · attach, IF the veto is overridden: legal liability (M-LEG), a cohesion cost
       (M-COH) and challenge exposure (the §11.3 challenge window).
   The override is itself an arbitrated, recorded decision, not a silent bypass.
   HARD REMOVAL is reserved for M-CAP physical, technical or geographic infeasibility
   at step 2. An organisation that CANNOT do a thing is different in kind from an
   organisation that MAY NOT do a thing.

   Rationale, stated because this reverses an earlier draft of this step.
   Absolute removal would make it impossible for an organisation ever to act
   unlawfully, breach a statutory obligation or override its own lawyers. That
   mechanically determines the option set from an attribute, which the founder forbids:
   pressures "should not force a single predetermined choice"
   (FOUNDER-REQUIREMENT-2026-07-18.md:271). It also contradicted §11.3 step 1, where a
   country organ MAY act beyond its authority ("ultra vires: the act is challengeable,
   not void") — unlawful action possible at country level and impossible at
   organisation level, with no stated reason for the asymmetry. And it foreclosed
   §10.4's own headline case: an organisation that cannot cross its own veto lines
   cannot radicalise in any observable way.
   The audit criticism this gate succeeds (C5 — `constraints` documented as hard and
   behaviourally inert) must not be over-corrected into hard-and-absolute.

   WHERE THE LINE SITS IS AN OWNER DECISION (§19 Q14): which vetoes, if any, are truly
   absolute (a physical impossibility is; a constitutional prohibition may not be), and
   what override threshold and liability each carries.

   NOTE: this step is specified as a successor to MicroAgent.constraints
   (agent_schema.py:181-183), which is documented as "hard" and is behaviourally inert
   (A3 §3). PERSON-MODEL.md:461 names its own M2 FEASIBILITY-GATE as succeeding the SAME
   field. At most one may be the successor, or the succession must be split explicitly.
   Unreconciled; see §2 and §19 Q12.

4. BLOC SCORING
   For each surviving option o and each bloc b:
       raw(b,o)   = Σ_d  interest_vector[b][d] · outcome_estimate(o, d)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    outcome_estimate is produced by M-EST (§6), which is NAMED BUT
                    UNDEFINED. Until §19 Q13 is answered this whole line has an
                    unspecified term in it, and M-ARB is not yet a mechanism.
       memory(b,o)= M-MEM prior from precedent records resembling o
       belief(b,o)= scored under the BLOC'S beliefs, not ground truth
                    (owned by BELIEF-AND-KNOWLEDGE-MODEL.md)
       risk(b,o)  = risk_posture[b] applied to the variance of outcome_estimate
       score(b,o) = raw + memory + risk, evaluated on belief

   A bloc that is wrong about the world will argue sincerely for the wrong option.
   This is required, not a defect.

5. AGGREGATION  (procedure-dependent)
   power(b) = formal_weight[b]
            + leverage_admissibility · informal_leverage[b]
            · internal_cohesion[b]
   Aggregate per procedure kind; apply quorum, chair tiebreak, consensus objection
   threshold, or command override as the procedure specifies.

6. STOCHASTIC RESOLUTION
   The winning option is drawn from a distribution over aggregate scores — NOT argmax.
   Rationale: CHARTER.md:60-62 requires the system to model a distribution rather than
   pretending there is one objectively correct future, and the founder requires
   probabilistic rather than deterministic-by-identity behaviour (:271).
   The draw MUST come from a named per-organisation RNG substream. See §16.

   THE SCORE->PROBABILITY TRANSFORM IS NOT YET SPECIFIED, AND THE GAP IS LOAD-BEARING.
   Aggregate scores are SIGNED and UNBOUNDED (§9.6 shows −0.929 alongside +0.683), so
   "a distribution over aggregate scores" is undefined as written: negative values are
   not probabilities. The result depends entirely on an unstated choice — softmax at
   some temperature, clamp-and-normalise, rank-based sampling — and each yields a
   materially different chance of the runner-up option. This is the single point at
   which the founder's "probabilistic, not deterministic-by-identity" requirement
   (:271) is actually implemented, and the point CHARTER.md:58 binds hardest
   ("same seed, same scenario, same decisions ⇒ identical numeric state").

   Requirements on any transform adopted:
     · It MUST be monotonic in aggregate score and MUST assign non-zero probability to
       every surviving option, so that no option is silently unreachable.
     · Its parameters (e.g. a temperature) MUST live in organisation or scenario DATA,
       never as engine constants — the same discipline §8.3 applies to decision
       procedure, and the defect audit §5.7 records for ACTION_EFFECTS.
     · The transform id, its parameter values, the resulting probability vector, the
       rng_substream and the rng_draw_index MUST ALL be recorded on the decision record,
       so the draw is replayable and question 6 of the Charter is answerable from state
       rather than by re-derivation.
   WHICH TRANSFORM FAMILY IS AN OWNER DECISION (§19 Q15). This document does not choose
   one, because choosing sets the system's entire sensitivity to bloc power.

7. DISSENT RECORD
   For every bloc: its score for the chosen option, its score for its own best option,
   the deficit between them, and whether it was overridden despite a strong objection.
   Emitted as authoritative state, not as narrative.

8. CONSEQUENCE APPLICATION
   M-COH  cohesion/morale fall in proportion to aggregate dissent × deviation_cost
   M-LEG  liability accrues if the decision ran against recorded legal advice
   M-LEAK leak hazard rises for strongly-dissenting blocs with external patrons
   M-DIV  divergence between the stated justification and actual_priorities is scored
   M-CONT the decision enters implementation; it has NOT yet happened

9. EVENT EMISSION  (P0.6)
   organisation_decision, with causal_parents linking the triggering event, the
   precedent records consulted, and the dissent record.
```

**Nothing in this procedure may be performed by a language model.** Steps 2-8 are arithmetic over
records. Step 1 may accept an LLM-proposed option; step 9's prose rendering may be LLM-written. That
is the whole of the model's involvement.

It would be convenient to describe this as the existing determinism boundary (ADR-006,
`llm_gateway.py:35`) applied *unchanged* to the entity layer. **That would be wrong, and the
difference is stated rather than glossed.** The existing boundary holds because a proposal is mapped
onto a fixed engine-owned effects table and can only ever select from it. Step 1 as specified would
let a proposal *enlarge the option space that a seeded stochastic draw ranges over*, which changes
both the draw's support and the number of draws consumed. The boundary is therefore **extended**,
and the extension carries a determinism obligation that the current boundary does not: see the
hazard note at step 1, and §16.2.

---

## 9. Worked example: the shipping company

The source record gives this example directly
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):106-111):

> a chief executive concerned about reputation; an operations division concerned about vessel
> safety; insurers concerned about financial exposure; lawyers concerned about liability; investors
> concerned about share price; crew unions concerned about worker protection; regional managers with
> local political relationships. The company's action should emerge from those pressures.

This section specifies that example in full, and works the resolution through concretely.

> # NOTHING IN THIS SECTION WAS EXECUTED
>
> **No code produced any value below.** Every number is hand-worked by the author to illustrate the
> arithmetic the specification calls for. **No MERIDIAN run has ever computed an organisational
> decision, and none can until §16.1 (named RNG substreams) and §18 (the dependency chain) are
> satisfied.** There is no organisation record, no bloc record, no arbitration code and no option
> catalogue anywhere in `scaffold/`.
>
> The numbers are additionally **illustrative placeholders**: not calibrated, not defaults, not
> proposed values. The entity is fictional, consistent with
> [`../../CHARTER.md`](../../CHARTER.md):137.
>
> The whole section is therefore written in the **conditional**: what *would* happen if the
> specified mechanism existed and were given these inputs. Any sentence here that reads as a report
> of something that happened is a defect in this document — the precise defect Phase 0 exists to
> correct — and should be raised.
>
> One further limit, stated because it bears on how much this example proves: `M-EST` (§6) is
> named but undefined, so `outcome_estimate(o, d)` — and therefore the §9.5 score matrix — is
> **author-supplied, not derived**. The aggregation arithmetic in §9.6 is checkable; the scores it
> operates on are not yet produced by any specified mechanism.

### 9.1 In plain English

Imagine a fictional shipping operator that has had a vessel damaged in the strait. It must decide
what to do with the twelve sailings it has scheduled over the next fortnight. Seven groups inside
and around the company want different things. None of them is in charge on their own. What follows
works through how a decision *would* come out of that under the specified mechanism, why the
decision would be one that neither the chief executive nor the operations director actually wanted,
and what would happen afterwards to the people who lost the argument.

None of this has been run. It is worked by hand, on paper, to show what the specification is asking
for and to let a reader check whether the arithmetic holds together.

### 9.2 The organisation

```text
org_id:          org-vantel-coastal-lines            (fictional)
org_kind:        firm
decision_procedure:
    kind:                     board_vote
    chair_bloc:               bloc-ceo
    quorum:                   0.6
    veto_holders:             [bloc-legal (legality only), bloc-insurer (insurability only)]
    deviation_cost:           0.35
    deadlock_action:          status_quo
    leverage_admissibility:   0.4       # a board room admits some, not all, informal pressure
cohesion:        0.71
morale:          0.58
public_mission:  "safe, reliable coastal freight for the region"
actual_priorities:
    [ {maintain_quarterly_dividend: 0.85},
      {retain_strait_route_licence:  0.70},
      {avoid_hull_loss:              0.55} ]
```

### 9.3 The blocs

| Bloc | Kind | Dominant interests | Formal weight | Informal leverage | Blocking rights |
|---|---|---|---|---|---|
| `bloc-ceo` | personal_faction | reputation 0.90, political standing 0.60, financial return 0.50 | 0.20 | 0.55 | — |
| `bloc-operations` | department | safety of personnel 0.90, operational continuity 0.55 | 0.15 | 0.65 | — |
| `bloc-insurer` | external_stakeholder | financial exposure 0.95 | 0.00 | 0.85 | may veto any option it declares uninsurable |
| `bloc-legal` | profession | liability 0.90, regulatory standing 0.60 | 0.10 | 0.45 | may veto any option assessed unlawful |
| `bloc-investors` | ownership | financial return 0.95, reputation 0.30 | 0.40 | 0.30 | — |
| `bloc-crew-union` | labour | safety of personnel 0.95, worker protection 0.90 | 0.05 | 0.80 | — |
| `bloc-regional-mgrs` | regional | political standing 0.70, operational continuity 0.60 | 0.10 | 0.50 | — |

Three of these are worth pausing on, because they are exactly the cases a single-agent model cannot
represent:

- **The insurer holds no votes and enormous power.** `formal_weight` 0.00, `informal_leverage` 0.85,
  and a conditional veto. It is modelled as an `external_stakeholder` bloc rather than as a separate
  organisation *for the purpose of this decision*; it is simultaneously its own `OrganisationEntity`
  with its own blocs, connected by a dependency edge (`M-DEP`). The bloc is the *interface*.
- **The crew union's power is almost entirely informal.** 0.05 formal against 0.80 leverage. In a
  `board_vote` procedure with `leverage_admissibility` 0.4, it will usually lose the vote — and then
  express its power through `M-CONT` (refusal to sail) and `M-COH` (industrial action), *after* the
  decision. That asymmetry is the point.
- **Regional managers are where the company meets local politics.** Their leverage runs through
  implementation compliance, not through the board room.

### 9.4 The option set, after gating

Six options would be generated. Two would be set aside before scoring:

| Option | Status under the specified gates |
|---|---|
| `continue_full_schedule` | would survive |
| `continue_with_naval_escort_request` | would survive |
| `suspend_strait_transits_14d` | would survive |
| `reroute_long_way_round` | would survive |
| `continue_with_reduced_crew_complement` | **would be vetoed at step 3** — `bloc-legal`: breaches a recorded crewing obligation. Under the revised step 3 the veto would *raise the threshold and attach liability*, not delete the option; on these numbers the option would not clear the raised threshold. Recorded with the obligation id. |
| `self_insure_and_continue` | **would be removed at step 2** — `M-RES`: capital reserve insufficient. This is hard removal, because it is infeasibility rather than prohibition. Recorded with the shortfall. |

Both would be retained in the explanation trace. `CHARTER.md`:126 requires the system to answer
"what alternative outcomes were possible", and an option that was blocked is a more interesting
answer than an option that was never considered.

For legibility the aggregation below is worked over the four surviving options only. A full
treatment would carry `continue_with_reduced_crew_complement` through step 6 with its raised
threshold, since under the revised step 3 a vetoed option is improbable rather than impossible.

### 9.5 Bloc scores

Scores would be on a −1..+1 scale, computed at step 4 from each bloc's `interest_vector` against its
**own beliefs** about each option's outcomes. The values below are **author-supplied**: they are
what `M-EST` would have to produce, and `M-EST` is undefined (§6, §19 Q13). They are chosen to be
plausible, not derived.

| Bloc | continue_full | continue_escort | suspend_14d | reroute_long |
|---|---|---|---|---|
| `bloc-ceo` | −0.20 | **+0.55** | −0.35 | +0.10 |
| `bloc-operations` | −0.85 | +0.20 | **+0.70** | +0.45 |
| `bloc-insurer` | −0.90 | +0.15 | **+0.60** | +0.40 |
| `bloc-legal` | −0.70 | +0.10 | **+0.65** | +0.35 |
| `bloc-investors` | **+0.60** | +0.35 | −0.75 | −0.40 |
| `bloc-crew-union` | −0.95 | +0.05 | **+0.85** | +0.55 |
| `bloc-regional-mgrs` | +0.15 | **+0.30** | −0.30 | −0.55 |

Read the columns, and the shape of the argument is visible: the people who bear the physical risk
and the people who bear the legal and financial risk both want to stop; the people who bear the
financial return want to continue; the chief executive wants the option that photographs best; the
regional managers do not want to explain a long reroute to the port authority they depend on.

### 9.6 Aggregation

`power(b) = formal_weight + 0.4 × informal_leverage × internal_cohesion`. Taking
`internal_cohesion` as 1.0 for all blocs for legibility:

| Bloc | power |
|---|---|
| `bloc-investors` | 0.40 + 0.4×0.30 = **0.520** |
| `bloc-ceo` | 0.20 + 0.4×0.55 = **0.420** |
| `bloc-insurer` | 0.00 + 0.4×0.85 = **0.340** |
| `bloc-crew-union` | 0.05 + 0.4×0.80 = **0.370** |
| `bloc-operations` | 0.15 + 0.4×0.65 = **0.410** |
| `bloc-legal` | 0.10 + 0.4×0.45 = **0.280** |
| `bloc-regional-mgrs` | 0.10 + 0.4×0.50 = **0.300** |

Weighted aggregate per option (Σ over blocs of power × score). Worked long-hand for
`suspend_strait_transits_14d`, so that a reader can verify the other three rather than trust them:

```text
suspend_strait_transits_14d
    bloc-investors      0.520 × −0.75 = −0.3900
    bloc-ceo            0.420 × −0.35 = −0.1470
    bloc-insurer        0.340 × +0.60 = +0.2040
    bloc-crew-union     0.370 × +0.85 = +0.3145
    bloc-operations     0.410 × +0.70 = +0.2870
    bloc-legal          0.280 × +0.65 = +0.1820
    bloc-regional-mgrs  0.300 × −0.30 = −0.0900
                                        ───────
                                        +0.3605
```

| Option | Aggregate |
|---|---|
| `continue_full_schedule` | **−0.929** |
| `continue_with_naval_escort_request` | **+0.683** |
| `suspend_strait_transits_14d` | **+0.361** |
| `reroute_long_way_round` | **+0.291** |

> **These four numbers were computed by hand and nothing in the repository can validate them.** They
> are reproducible from the §9.5 score matrix and the power column immediately above, using the
> stated formula and no other term. A reader who recomputes them and gets a different answer should
> raise it: an unreproducible worked example in *this* project would be the miniature form of the
> exact defect the repository is private over. (An earlier draft of this section published
> −0.752 / +0.720 / +0.560 / +0.301, which do not reproduce from these tables. They were wrong and
> have been corrected.)

At step 6 the outcome would be **drawn** from a distribution derived from these aggregates rather
than taken as the maximum — and, as step 6 now records, **the transform from these signed scores to
a probability vector is not yet specified** (§19 Q15), so the exact draw probabilities cannot be
stated here. What can be stated is the ordering and the margins: under any monotonic transform,
`continue_with_naval_escort_request` would be the most probable outcome by a wide margin;
`suspend_strait_transits_14d` and `reroute_long_way_round` would be near-equal and much weaker
alternatives, separated by only 0.07; and `continue_full_schedule` would be the least probable of
the four by a long way.

Note that the margin matters to how this example should be read. The escort option leads suspension
by 0.32 — roughly the gap between suspension and rerouting doubled, and comparable to suspension's
entire aggregate. Suspension is a **weak** alternative on these numbers, not a close-run one, and
this document should not be read as claiming the outcome is finely balanced. Whether a transform
should nevertheless leave a meaningful chance of it is exactly what Q15 decides.

**The leading option would be one that no bloc ranked first except the chief executive and the
regional managers.** The two blocs that most wanted to stop sailing — operations and the crew union
— would be outweighed. The insurer would not veto, because the escort request would change its
exposure enough to keep the route insurable, but it would score the option at only +0.15. That is
the "emerges from those pressures" behaviour the source record requires, and it is unreachable in a
model where one role emits one proposal (`institutional_agent.py:26-41`).

### 9.7 What would be emitted

```python
# SKETCH — NOT IMPLEMENTED.

OrganisationDecision(
    decision_id="dec-…",
    org_id="org-vantel-coastal-lines",
    tick=…,
    trigger_event_id="evt-…",                 # the vessel damage
    option_set=[...],                          # including the gated options + reasons
    chosen_option="continue_with_naval_escort_request",
    aggregate_scores={...},                    # the four numbers above
    probability_vector={...},                  # step 6 transform output — transform id and
    transform_id="…",                          # parameters recorded, per §19 Q15
    procedure_applied="board_vote",
    rng_substream="org:org-vantel-coastal-lines:arbitration",   # §16
    rng_draw_index=…,

    # AUTHORITATIVE, ENGINE-COMPUTED, READ BY M-DIV:
    justification_frame="crew_safety_secured",  # -> M-DIV. Selected by M-ARB from a
                                                # scenario-authored catalogue of frames.
                                                # A STRUCTURED VALUE, never generated prose.
    served_priorities=["maintain_quarterly_dividend",
                       "retain_strait_route_licence"],           # -> M-DIV
)

# PRESENTATION-ONLY, LLM-RENDERED, READ BY NO MECHANISM:
#     stated_justification: str
#         e.g. "crew safety assured through state escort"
#     Rendered by the LLM FROM justification_frame + served_priorities at display time.
#     Marked non-causal in the schema, exactly as InternalBloc.label is (§8.2).
#     It MUST NOT be read back by M-DIV or by anything else.
```

**Why this field is split, stated plainly.** An earlier draft of this document emitted a single
LLM-drafted `stated_justification` and annotated it `-> M-DIV`. That was a **breach of the
determinism boundary**, and it is corrected here rather than defended. The chain ran: a language
model writes a string → `M-DIV` scores divergence from it (§10.4) → divergence drives public
reputation loss, cohesion strain and a leak-hazard multiplier → §12 row 17 feeds reputation back
into `M-REP`, `M-DEP` and `M-CONT`. That is generated narrative altering authoritative state, which
[`../../CHARTER.md`](../../CHARTER.md):37-40 forbids outright ("Generated narrative alone must never
alter authoritative state"), which ADR-006 forbids, which the source record forbids at :46-48, and
which **this document's own §7.1 rule** forbids ("No free-text description as authoritative state.
Prose is generated from this record by the LLM and never read back"). The split above is the
minimum correction: the engine selects a structured frame, `M-DIV` reads the frame, and the prose is
downstream of both and read by nothing. §16.2 is corrected to match.

```python
DissentRecord(
    decision_id="dec-…",
    entries=[
        {bloc: "bloc-crew-union",  chosen_score: +0.05, best_score: +0.85, deficit: 0.80,
         overridden: True,  grounds: "safety_of_personnel"},
        {bloc: "bloc-operations",  chosen_score: +0.20, best_score: +0.70, deficit: 0.50,
         overridden: True,  grounds: "safety_of_personnel"},
        {bloc: "bloc-insurer",     chosen_score: +0.15, best_score: +0.60, deficit: 0.45,
         overridden: False, grounds: "financial_exposure"},
        …
    ],
)
```

### 9.8 What would happen next — the consequences of losing

This is where the model would earn its cost. A decision would not be the end of the tick.

| Mechanism | Specified consequence, were this example run |
|---|---|
| `M-COH` | Aggregate dissent 1.75 across three blocs × `deviation_cost` 0.35 → organisational cohesion falls; crew-union morale falls furthest. A further override on a related decision must be able to cross the industrial-action threshold. |
| `M-CONT` | The escort request must be *implemented* by regional managers (who scored it +0.30 and comply readily) and *sailed* by crews the union represents (deficit 0.80). Compliance is drawn per implementing bloc. Partial compliance — some sailings, not twelve — is a permitted and likely outcome, and is itself an event. |
| `M-LEAK` | `bloc-operations` holds a documented safety assessment and dissented at 0.50. Leak hazard rises. If it fires, a disclosure event enters the information environment and other entities' beliefs update through `M-OBS`. Note the connection to `EventVisibility` (`agent_schema.py:203-208`), which is the only visibility construct that exists today and is never populated. |
| `M-LEG` | The decision would be taken with a recorded safety objection on file. Liability would accrue **conditionally**: if a vessel were subsequently lost, the recorded dissent would convert prior objection into demonstrable foreseeability, and legal exposure would increase sharply. |
| `M-DEP` | An escort request creates a dependency on a state actor. The state's own arbitration (§11) may refuse it. If refused, the company's decision is void and re-arbitration is triggered — with the insurer's veto now live. |
| `M-DIV` | The `justification_frame` would be `crew_safety_secured`; `served_priorities` would be the dividend and the route licence. Divergence would be scored and accumulated from those two **structured** values (§10). The rendered prose plays no part. |
| `M-REP` | Public reputation would move on the announced decision; private reputation would move on what peer organisations and insurers *observe*, which is not the same evidence. |

### 9.9 Why this cannot be built on the current structure

- There is no bloc, faction, department or membership field anywhere in `agent_schema.py`.
- `InstitutionalAgent.step` (`institutional_agent.py:26-41`) produces one proposal and stores it;
  there is no arbitration stage and no place to put one. A3 §2 makes the same structural point about
  a different feature: `_validate_and_price` "has no access to sibling proposals".
- The context passed to the model (`institutional_agent.py:33-37`) is a three-key stub — `tick`,
  `scenario_id`, `primary_target=None` — so the agent has no world knowledge to score options
  against.
- The decision would have to write nested organisational state, which `apply_deltas`
  (`macro_state.py:23-47`) cannot reach and would skip in silence (C3, §5.2).
- Every stochastic draw in step 6 would come off the single shared RNG (`engine.py:83`), so adding
  one bloc to one company would shift every later draw in the entire simulation. See §16.

---

## 10. Public mission versus actual priorities

### 10.1 In plain English

Every organisation says what it is for. That statement is sometimes a lie, sometimes a sincere
belief that no longer matches behaviour, and sometimes simply out of date. A ministry founded to
protect fisheries may now mostly protect the minister. A charity may still describe itself by the
work it did fifteen years ago. A company's mission statement is marketing.

MERIDIAN will hold both — what the organisation says, and what it actually optimises — and will make
the gap between them something the player has to **work out**, not something they are told.

### 10.2 The two fields

| Field | Read by | Meaning |
|---|---|---|
| `public_mission` | `M-DIV`, `M-REP`, the profile surface | The declared purpose. **Never read by `M-ARB`.** It has no influence on any decision. |
| `actual_priorities` | `M-ARB` step 4 | The weighted objectives that genuinely enter arbitration. Authoritative. |
| `self_understanding` | **⚠ nothing, as specified** | What the organisation believes it is optimising. See §15-R11: this is one of the four founder-required views and no mechanism in §6 reads it. |

The design force here is that `public_mission` is *structurally incapable* of steering behaviour. If
it could, the divergence would be untrue.

`self_understanding` is a different problem and is not disguised. It is a first-class field on the
authoritative record (§7.1), a numbered consequence of the central principle (§4d), and one of the
four founder-required views (§10.3) — yet as specified it feeds nothing. `M-DIV` measures
`served_priorities` against `public_mission`, not against self-understanding. `M-REP` reads
reputation. It exists only to be rendered, which is this document's own definition of fake depth. It
cannot be deferred to [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) by omission,
because §7.1 explicitly places it in this document's scope. It is recorded as **§15-R11** with two
candidate dispositions and left for the owner (§19 Q16).

### 10.3 The four views

The founder requires **at least four** views of every entity — the source record's wording is "at
least four" ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):147-165), so
the four enumerated there are a minimum rather than a closed set. For an organisation the four
enumerated views carry the divergence as follows.

| View | Contains | Authoritative? |
|---|---|---|
| **Authoritative reality** | `actual_priorities`, real bloc powers, the full dissent record, real legal exposure, real funding sources. | **Yes** — this document's position. Subject to P0.4 (§18). |
| **Self-understanding** | What the organisation's dominant coalition believes it is optimising. Held as a belief record. May sincerely and wrongly equal `public_mission`. | Derived — but it is a *fact about a belief*, and §19 Q4 flags that P0.4 may need to treat it as authoritative in its own right. |
| **Public profile** | `public_mission`, announced decisions, `stated_justification`, reputation, publicly-known leadership. Contains propaganda, error, omission and staleness. | Derived |
| **Player intelligence profile** | What the player's role can currently support, per attribute, labelled: **Confirmed · Reported · Assessed · Disputed · Unknown · Possibly deceptive · Outdated · Restricted**. | Derived |

Applied to the hand-worked example in §9 — which, as that section states, **was not executed** — the
same fact would render four ways:

| View | "Why did they keep sailing?" |
|---|---|
| Authoritative reality | The dividend priority (0.85) and route licence (0.70) would outweigh a 0.80-deficit safety objection under a board-vote procedure with `leverage_admissibility` 0.4. |
| Self-understanding | The board would believe it had secured crew safety by obtaining an escort — a sincere reading, held by the blocs that won. ⚠ Note that as specified, no mechanism reads this view; see §15-R11. |
| Public profile | "Sailings continue under naval escort; crew safety assured." — LLM-rendered from `justification_frame`, and read back by nothing (§9.7). |
| Player intelligence profile | Continued sailings: **Confirmed**. Escort requested: **Confirmed**. Escort granted: **Reported**. The board's stated safety rationale: **Possibly deceptive** — but *only* if the player has obtained the dissent evidence. Otherwise: **Unknown**. |

### 10.4 The divergence mechanism (`M-DIV`)

```text
SPECIFIED — NOT IMPLEMENTED

Per decision:
    divergence(d) = distance( served_priorities(d), public_mission_alignment(d) )

    Both terms are STRUCTURED, ENGINE-COMPUTED values. M-DIV reads served_priorities and
    justification_frame (§9.7) and public_mission. It MUST NOT read the LLM-rendered
    stated_justification prose, or generated narrative would be altering authoritative
    state, contrary to CHARTER.md:37-40, ADR-006 and §7.1 of this document.

Accumulated:
    divergence_pressure(org) = decayed sum over recent decisions, weighted by public exposure

Discoverability:
    An observer may form an assessment of divergence only from evidence it actually holds:
      · behavioural inconsistency observed repeatedly over time  -> "Assessed"
      · a leaked dissent record (M-LEAK)                          -> "Confirmed" or "Disputed"
      · a whistleblower account (M-LEAK + PERSON-MODEL)           -> "Reported"
      · a regulator's finding (M-LEG)                             -> "Confirmed"
    Divergence is NEVER exposed as a number on the player-facing profile.

Consequences:
    Detected divergence  -> M-REP public reputation loss, asymmetric by observer community
    High internal divergence -> M-COH strain on blocs whose interests the mission actually served
    Sustained divergence -> M-LEAK hazard multiplier
```

The last line matters: an organisation that repeatedly acts against its stated mission generates its
own exposure from the inside. That is the mechanism behind the source record's question "What caused
this organisation to radicalise?" (:188) — a drift in `actual_priorities`, driven by bloc power
shifting through `M-RECR`, `M-SUCC` and `M-COH`, while `public_mission` stays where it was.

### 10.5 What this must not become

The player-facing profile must remain an **intelligence product, not an omniscient encyclopaedia**
(:165). Two prohibitions follow, and both are specification-level:

- A "true priorities" panel must never be rendered from `actual_priorities` directly, at any tier,
  for any role, without an evidence chain that supports each line.
- The confidence labels are a property of the **observer's evidence**, not a decoration on the
  attribute. `Confirmed` must mean *this player role holds evidence sufficient to confirm it*, and
  must be computed by `M-OBS`, not authored.

Note a structural point for [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md): the eight confidence labels
and the existing `EventVisibility` enum (`agent_schema.py:203-208`: `public`, `classified`,
`leaked`) are **two different axes** — who may observe, versus how well an observation is evidenced.
They must not be collapsed into one enum. `EventVisibility` is also attached to events rather than to
entity attributes, and is never populated by anything.

---

## 11. The country as a composed entity

### 11.1 In plain English

Today a country in MERIDIAN is eighteen numbers in a single object. The founder's requirement is
that it stop being one thing:

> The "country" should not be a single agent. The government, public, military, courts, businesses
> and regional authorities may all react differently.
> — [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):121-122

A country will therefore be a **container of entities that argue with each other in public**. The
government decides something. The court may strike it down. The regional authority may refuse to
implement it. The army may implement it slowly. The business affected may sue, relocate or comply
loudly while lobbying quietly. The public may or may not care, and different parts of the public may
disagree with each other more than they disagree with the government.

The eighteen national numbers do not disappear. They become a **summary** — something computed *from*
all of that, rather than the thing that is actually true.

### 11.2 Structure

```python
# SKETCH — NOT IMPLEMENTED.

class CountryEntity(EntityBase):
    country_id: EntityId
    political_system: PoliticalSystem        # -> M-ARB (which organ decides what), M-VETO
    constitutional_order: list[Instrument]   # -> M-VETO, M-LEG (what is lawful, who may block)
    organs: list[EntityId]                   # OrganisationEntity ids: executive, legislature,
                                             # judiciary, armed services, central bank, regulators
    parties: list[EntityId]                  # OrganisationEntity (party) ids
    regions: list[RegionRecord]              # -> M-GEO, M-CONT (implementation happens here)
    population: list[EntityId]               # cohort ids -> POPULATION-FIDELITY.md
    industries: list[EntityId]               # BusinessEntity ids
    infrastructure: list[InfrastructureRecord]   # -> M-CAP, M-DEP
    media_environment: list[EntityId]        # media OrganisationEntity ids -> M-OBS
    external_relations: [edges]              # alliances, rivalries -> RELATIONSHIP-GRAPH.md
    historical_grievances: list[GrievanceRecord]   # -> M-MEM, belief priors
    state_capacity: CapacityRecord           # -> M-CONT (how well orders become facts)
    elite_cohesion: float                    # -> M-ARB across organs, M-CONT
    legitimacy: LegitimacyRecord             # -> M-CONT (compliance), M-COH

    indicators_view: DerivedIndicators       # the existing 18 scalars, DEMOTED to derived
```

The last line is the whole contradiction in one field. `MacroState.indicators`
(`macro_schema.py:40-70`) is currently the only thing the system treats as authoritative:
`macro_snapshot()` is `MacroState.model_dump()` (`macro_state.py:49-51`), `self.snapshots` holds
macro dicts alone (`engine.py:116`, `:180`), and the determinism test compares exactly that one
object. This document specifies inverting that. **It does not have the authority to do so** — P0.4
must decide it (§18, §19 Q2).

Two further existing-code notes, recorded so the cost is visible:
`shipping_throughput_pct_of_baseline` (`macro_schema.py:46-48`) hardcodes a maritime strait into the
shared national schema (audit §5.8), and 14 of the 18 scalars never change at all (audit §4.2).

### 11.3 Contradiction between organs (`M-CONT`)

**In plain English:** in a real country, ordering something and it happening are different events,
and the space between them is where most political drama lives.

```text
SPECIFIED — NOT IMPLEMENTED

A decision by organ X that requires action by entity Y proceeds:

1. AUTHORITY CHECK        Does X have constitutional authority for this act?
                          (constitutional_order -> M-VETO; the office's own powers,
                           jurisdiction, delegation bounds and any suspension ->
                           M-AUTH-OFF / M-AUTH-DEL / M-AUTH-TEN, §7.3, added
                           19 July 2026 — this step previously named no mechanism
                           for the office half of the check)
                          Failure  -> ultra vires: the act is challengeable, not void.

2. CHALLENGE WINDOW       Any entity with standing may initiate a legal challenge.
                          The court is its own OrganisationEntity and runs its own M-ARB
                          over its own blocs. It may strike the act down, uphold it,
                          narrow it, or delay. The government does not control the outcome.

3. IMPLEMENTATION         Y runs its own M-ARB on whether and how to comply.
                          compliance_propensity(Y) = f( legitimacy of X in Y's assessment,
                                                        X's PRACTICAL authority (M-AUTH-PRAC,
                                                          §7.3, added 19 July 2026 — formal
                                                          authority alone is insufficient,
                                                          which is why a lawful order can be
                                                          complied with nominally),
                                                        Y's own bloc interests,
                                                        state_capacity,
                                                        M-DEP leverage X holds over Y,
                                                        sanction credibility )
                          Outcomes: full | partial | delayed | nominal | refused
                          Every outcome is an event with a recorded cause.

4. FEEDBACK               Refusal or nominal compliance is observable (M-OBS) and:
                            · damages X's authority (M-REP private reputation)
                            · alters other entities' compliance priors (M-MEM)
                            · may trigger escalation, which is a new decision, not a rule
```

Worked micro-example, using the existing demo scenario's cast for concreteness (all fictional,
`kestral-strait.json:241-388`): the head of government (`:243`) decides to requisition port capacity.
The finance ministry (`:298`) has an objective to block unfunded spending (`:302`) and will dissent
in cabinet arbitration. The court — which **does not exist as an entity today** — may hear a
challenge from the port operator. The coastal region must implement, and its regional authority has
its own electorate and its own relationship with the fishing cohort (`:79`). The order can therefore
be lawful, announced, and still not happen — and the reason it did not happen is recorded, walkable
and attributable.

That last property is what [`../../CHARTER.md`](../../CHARTER.md):64-83 describes as a credible
causal chain "without any of it being explicitly scripted". §17 maps it to the eight questions.

### 11.4 Population is not an organ

The public is not an organisation and must not be given an arbitration procedure. Public reaction is
owned by [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) and
[`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md). The interfaces between them and
this document are exactly four, and no more:

1. **Membership** — cohorts supply people to organisations (`M-RECR`), which changes bloc
   composition and therefore future decisions.
2. **Legitimacy** — cohort beliefs feed `legitimacy`, which feeds `M-CONT` compliance.
3. **Influence weighting** — an organisation's aggregate influence is computed by `M-INF`, which is
   defined in [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md), **not here**.
4. **Observation** — cohorts observe organisational behaviour through the media environment
   (`M-OBS`).

On (3), a hard boundary. P0.5 ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:84-86`)) commits that
`represents_population` must affect aggregation, and audit §5.10 records that the field
(`agent_schema.py:95`) is read by nothing today. **This document must not restate, redesign or
pre-empt that work.** It records only the requirement that lands on it: the founder requires that a
small group may hold disproportionate influence through wealth, organisation, strategic position or
political access (:137-139), which means population weight must be **one term among several** rather
than the aggregation rule itself. `M-INF` is where an organisation contributes the other terms.
[`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) is the design successor to that P0.5 item and
owns the model; this document is a client of it.

---

## 12. Attribute lists — organisations

The full list from [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):99-102,
each attribute mapped to the mechanism that must read it. Discipline per
[`PERSON-MODEL.md`](PERSON-MODEL.md): **an attribute that names no mechanism is fake depth**.

Legend: **✔** mapped · **⚠** mapped only conditionally, see note · **✘** unmapped, see §15.

> ### SPECIFICATION — NOT IMPLEMENTED
> No field, mechanism or effect in the table below exists in MERIDIAN's code. The final column
> states what the specification **requires a mechanism to do**; it is not a description of
> behaviour. Every ✔ in this table cites the `M-ARB` **step number** where the reader is a step of
> the §8.4 procedure, so that a reader can check the claim against that procedure.

| # | Source attribute | Specified field | Reading mechanism(s) | Specified causal effect |
|---|---|---|---|---|
| 1 | Founding history | `founding: FoundingRecord` | `M-MEM` ⚠ | Must seed the initial precedent set and founding relationship edges, and must bias early arbitration toward founding doctrine. Only the structured seeds are specified; founding *narrative* is §15-R1. |
| 2 | Legal status | `legal_status` | `M-LEG`, `M-VETO`, `M-CAP` ✔ | Must determine which acts are lawful for this org, who may challenge them, and what liability attaches. |
| 3 | Public mission | `public_mission` | `M-DIV`, `M-REP` ✔ | Must never be read by `M-ARB`, by design (§10.2). Must drive divergence scoring and public expectation. |
| 4 | Actual priorities | `actual_priorities` | `M-ARB` step 4 ✔ | The objective weights that must genuinely determine decisions. |
| 5 | Leadership | `role_occupancies` + `offices` + `command_chain` | `M-SUCC`, `M-AUTH` ✔, `M-LEAD` ⚠ | The person occupying a role must supply, within bounds, the interest weighting their bloc brings; replacing them must change outcomes without changing the organisation. The **powers** the role confers — jurisdiction, delegation, acting authority, expiry, suspension, command chain — are `M-AUTH` (§7.3). **Amended 19 July 2026**: the previous note recorded that [`PERSON-MODEL.md`](PERSON-MODEL.md):472-473's **M13 ROLE-AUTHORITY** and **M14 FACTION-ALIGNMENT** were assigned to this document and specified nowhere. Founder decisions 1B and 1C discharged both — M13 as `M-AUTH` (§7.3), M14's organisation half as `M-FAC` (§7.4), its alignment edge to [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md). **Still conditional**: the person→interest transfer is `M-LEAD`, which is named but undefined (§6). See §15-R12, §19 Q12. |
| 6 | Internal factions | `blocs` + `factions` | `M-ARB` steps 4-7, `M-COH`, `M-LEAK`, `M-CONT` ✔, `M-FAC` ✔ | The pressures a decision must emerge from (§8). **Amended 19 July 2026**: faction *definition, membership rule, formal positions and structure* are `M-FAC` (§7.4, founder decision 1C), which resolves them into bloc composition and therefore into arbitration outcomes. The person-to-faction alignment edge is **not** here: it is [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md)'s, and duplicating it is a defect. |
| 7 | Organisational culture | `decision_procedure` params + bloc `risk_posture` distribution | `M-ARB` steps 4-5 ✔ | Culture must be carried **as arbitration parameters** (`deviation_cost`, `leverage_admissibility`, `M-MEM` weight, quorum), not as prose. Free-text culture description is §15-R2. |
| 8 | Membership | `blocs[].membership` | `M-RECR`, `M-INF`, `M-COH` ⚠ | Size and composition must set bloc weight, labour-action capacity and aggregate influence. **Conditional**: `M-RECR` is undefined (§15-R3) and `M-INF` is owned by [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md), downstream of P0.5. |
| 9 | Recruitment methods | `MembershipRecord.intake_policy` | `M-RECR` ⚠ | Must determine which cohorts supply new members, shifting bloc interests over time. **Conditional**: `M-RECR` requires a membership-flow model that, verified against the sibling documents, no document specifies. See §15-R3. |
| 10 | Funding | `funding: list[FundingSource]` | `M-RES`, `M-DEP` ✔ | Must set what the org can afford; a funder must be able to withdraw as a coercive act, which is a dependency edge. |
| 11 | Assets | `assets: AssetLedger` | `M-RES`, `M-CAP` ✔ | Must determine affordability and physical feasibility; assets must be seizable, damageable and pledgeable. |
| 12 | Capabilities | `capabilities` | `M-CAP` at `M-ARB` step 2 ✔ | The feasibility gate. Must remove options outright — this is the one gate specified as hard removal (§8.4 step 3 rationale). |
| 13 | Geographic presence | `geographic_presence` | `M-GEO`, `M-CONT`, `M-OBS` ✔ | Must determine where it can act, where it is regulated, where it is seen, and where implementation occurs. |
| 14 | Decision-making process | `decision_procedure` | `M-ARB` step 5 ✔ | Must determine how the same bloc scores produce different outcomes in different organisations. |
| 15 | Dependencies | edges (`RELATIONSHIP-GRAPH`) | `M-DEP`, `M-VETO` at `M-ARB` step 3 ✔ | Must propagate shocks; must carry a dependency-holder's veto (the insurer in §9.3). |
| 16 | Rivals and partners | edges (`RELATIONSHIP-GRAPH`) | `M-DEP` ✔, `M-EST` ⚠ | Must alter the expected outcomes of options and enable coalition or retaliation. **Downgraded**: the option-outcome route runs through `M-EST`, which is named but undefined (§6), so the arbitration half of this mapping is currently a claim on an unspecified function. See §15-R10. |
| 17 | Reputation | `reputation_public`, `reputation_private` | `M-REP`, `M-DEP`, `M-CONT` ✔ | Two values, two evidence bases. Must affect who will deal with the organisation and whether its orders are obeyed. |
| 18 | Legal exposure | `legal_exposure` | `M-LEG` ✔, `M-ARB` ⚠ | Must accumulate from decisions taken against recorded advice, and must price and constrain future options. **Downgraded**: no step of the §8.4 procedure reads accumulated exposure — option pricing is `M-RES` at step 2 — so the `M-ARB` half is unverifiable against the specified procedure. See §15-R13. |
| 19 | Current strategy | `standing_strategy` | `M-ARB` step 1 ✔ | Must bias which options are generated at all; changing strategy must itself be an arbitrated decision. |
| 20 | Institutional memory | `memory: InstitutionalMemory` | `M-MEM` at `M-ARB` step 4 ⚠ | Must supply precedent priors in bloc scoring. **Conditional on P0.6** — precedent records are event-sourced and cannot exist before event/snapshot/replay foundations land. |
| 21 | Internal disputes | `open_disputes` | `M-COH`, `M-LEAK` ✔, `M-ARB` ⚠ | Unresolved disagreements must persist across ticks, degrade cohesion and raise disclosure hazard. **Downgraded**: no step of §8.4 reads `open_disputes`. See §15-R13. |
| 22 | Cohesion and morale | `cohesion`, `morale` | `M-COH`, `M-ARB` steps 5 and 8, `M-CONT` ✔ | Must determine whether the organisation survives being overridden, and whether decisions are implemented. |

---

## 13. Attribute lists — countries

From [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):115-119.

> ### SPECIFICATION — NOT IMPLEMENTED
> No field, mechanism or effect in the table below exists in MERIDIAN's code. The final column
> states what the specification **requires a mechanism to do**; it is not a description of
> behaviour. A country is not decomposed in the code at all — it is 18 flat scalars
> (`macro_schema.py:73-87`), and whether it is decomposed is an open owner decision (§19 Q2).

| # | Source attribute | Specified field | Reading mechanism(s) | Specified causal effect |
|---|---|---|---|---|
| 1 | Historical development | `founding` + `historical_grievances` | `M-MEM` ⚠ | Must seed precedent and grievance records. Narrative history beyond those seeds is §15-R1. |
| 2 | Political system | `political_system` | `M-ARB` step 5, `M-VETO`, `M-CONT` ✔ | Must determine which organ decides what, who may block, and how compliance is obtained. |
| 3 | Constitution and legal framework | `constitutional_order` | `M-VETO`, `M-LEG`, `M-AUTH-OFF` ✔ | Must supply the authority check at `M-CONT` step 1 and the challenge window at step 2. **Amended 19 July 2026**: the office half of that check — which office holds which power, over what jurisdiction, and whether it is delegated, expired or suspended — is `M-AUTH` (§7.3). |
| 4 | Government institutions | `organs` | `M-ARB`, `M-CONT`, `M-AUTH` ✔ | Each must be its own `OrganisationEntity` with its own blocs, and they must be able to contradict one another (§11.3). **Amended 19 July 2026**: an organ is an institution, and its base state and lifecycle are specified at §7.5 as a **specialised organisation** (founder decision 1D) — not as a distinct entity type and not in a separate specification. |
| 5 | Parties and factions | `parties` + `factions` | `M-ARB` steps 4-5 (within legislature/executive), `M-SUCC` ✔, `M-FAC` ✔ | Must supply blocs to governing organs; coalition arithmetic must become veto structure. **Amended 19 July 2026**: faction definition, membership rule, formal positions and structure are `M-FAC` (§7.4); the person-to-faction alignment edge that determines whether a coalition holds is [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md)'s and must not be duplicated here. |
| 6 | Regions and local authorities | `regions` | `M-GEO`, `M-CONT` ✔ | Implementation must happen here; a region must be able to comply nominally, partially or not at all. |
| 7 | Population groups | `population` (cohort ids) | `M-RECR` ⚠, `M-CONT` (legitimacy) ✔, [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) — **referred out** | Owned by [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md). Four interfaces only (§11.4). **Downgraded**: naming another document is not a mechanism (the §15-R4 test), and `M-RECR` is undefined. Recorded at §15-R14. |
| 8 | Languages and religions | cohort/person attributes | ⚠ **referred out** — see note | **Sensitive.** Governed by [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md). Must affect social experience, networks, exposure, discrimination and solidarity — never competence, morality or intelligence (:305-306). **Downgraded from ✔**: `M-OBS` as defined in §6 governs *which entities observe a decision*, and says nothing about language gating media reach or comprehension, so that mapping was asserted rather than supported by the register's own definition. See §15-R14 — an unmapped **sensitive** attribute must default to struck or gated, not retained. |
| 9 | Economic structure | `industries` + macro derivation | `M-RES`, `M-DEP` ✔ | Must determine what a shock to one sector propagates into. |
| 10 | Class structure | cohort attributes | ⚠ **referred out** | **Not specified here.** Referred to [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md); this document names no mechanism of its own. Verified as at 18 July 2026: that document specifies none either. See §15-R4. |
| 11 | Major industries | `industries` (BusinessEntity ids) | `M-DEP`, `M-RES`, `M-INF` ✔ | Businesses must be entities with their own arbitration, able to lobby, relocate, comply or resist. |
| 12 | Infrastructure | `infrastructure` | `M-CAP`, `M-DEP`, `M-GEO` ✔ | Must set what is physically possible and what a disruption disables. **Fictional only** — [`../../CHARTER.md`](../../CHARTER.md):137-138 forbids real operational vulnerabilities. |
| 13 | Military and security forces | `organs` (armed services) | `M-ARB`, `M-CONT`, `M-CAP` ✔ | An armed service must be an organisation with blocs; compliance with civilian direction must be modelled, not assumed. |
| 14 | Media environment | `media_environment` | `M-OBS`, `M-REP`, `M-DIV` ✔ | Must determine who observes what, with what evidential quality, and how divergence becomes discoverable. |
| 15 | Alliances | edges (`RELATIONSHIP-GRAPH`) | `M-DEP`, `M-VETO` ✔ | Support must be withholdable; alliance confidence must be a consequence, not an input. |
| 16 | Rivalries | edges (`RELATIONSHIP-GRAPH`) | `M-DEP` ✔, `M-EST` ⚠ | Must change expected outcomes and enable external retaliation. **Downgraded**: the outcome-estimate route runs through the undefined `M-EST` (§6, §15-R10). |
| 17 | Historical grievances | `historical_grievances` | `M-MEM`, belief priors ⚠ | Structured grievance records with onset, cause and parties. **Conditional on P0.6.** |
| 18 | National myths | — | ✘ | **No mechanism specified.** Verified as at 18 July 2026: none is specified in [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) either. See §15-R5. |
| 19 | Current public sentiment | cohort beliefs | `M-CONT` (legitimacy) ✔, [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) — **referred out** ⚠ | Must feed legitimacy and therefore compliance. **Partially downgraded**: the `M-CONT` route is a real mapping; the belief-structure half is a document reference, not a mechanism, and is recorded at §15-R14. |
| 20 | Government legitimacy | `legitimacy` | `M-CONT`, `M-COH` ✔ | Must determine whether orders become facts. The central country-level mechanism. |
| 21 | Elite cohesion | `elite_cohesion` | `M-CONT`, `M-LEAK` ✔, `M-ARB` ⚠ | Low elite cohesion must raise contradiction between organs and disclosure hazard. **Downgraded**: the §8.4 procedure is specified for a *single* organisation and has no cross-organ mode, so "`M-ARB` across organs" names a mode that does not exist in the specification. See §15-R13. |
| 22 | State capacity | `state_capacity` | `M-CONT`, `M-CAP` ✔ | Must set the conversion rate from decision to implemented fact. |
| 23 | International reputation | `reputation_public` (external observers) | `M-REP`, `M-DEP` ✔ | Must alter what external entities will offer, demand or withhold. |

---

## 14. Attribute lists — businesses

From [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):126-128. A
`BusinessEntity` is specified as an `OrganisationEntity` with `org_kind: firm` plus the fields below;
it is a profile, not a separate schema.

> ### SPECIFICATION — NOT IMPLEMENTED
> No field, mechanism or effect in the table below exists in MERIDIAN's code. There is no business
> entity of any kind in the codebase or in `kestral-strait.json`. The final column states what the
> specification **requires a mechanism to do**; it is not a description of behaviour.

| # | Source attribute | Specified field | Reading mechanism(s) | Specified causal effect |
|---|---|---|---|---|
| 1 | Ownership and shareholders | `ownership: list[OwnershipStake]` → `bloc-investors` | `M-ARB` step 5 (formal weight), `M-SUCC` ✔ | Ownership concentration must *be* formal voting weight in arbitration (§9.6). |
| 2 | Board members | `role_occupancies` (board) + `offices` | `M-ARB` step 4, `M-SUCC`, `M-AUTH` ✔, `M-LEAD` ⚠ | Board composition must set who scores options and with what interests. **Amended 19 July 2026**: what a board seat *empowers* its holder to do — and whether that power is delegated, expired or suspended — is `M-AUTH` (§7.3). **Still conditional** on `M-LEAD` (§6, §15-R12), which is what a board member's biography does to their bloc's interests. |
| 3 | Executives | `role_occupancies` (exec) + `command_chain` | `M-ARB` step 5 (chair), `M-CONT` ✔, `M-AUTH-DEL` ✔ | The chair must break ties under `board_vote`; executives must own implementation. **Amended 19 July 2026**: an acting or delegated executive must exercise the chair position only within the delegated subset (`M-AUTH-DEL`, §7.3), so the same bloc scores can resolve differently while a principal is absent. |
| 4 | Revenue sources | `funding` (revenue lines) | `M-RES`, `M-DEP` ✔ | Concentration must create vulnerability: losing one customer or route must be able to be existential. |
| 5 | Debt | `assets.liabilities` | `M-RES`, `M-DEP` ✔ | Must constrain affordable options; covenants must act as external vetoes at step 3. |
| 6 | Workforce | `blocs[].membership` (labour) | `M-COH`, `M-CONT` ✔, `M-RECR` ⚠ | Labour must be a bloc with informal leverage; refusal to work must be an implementation failure, not a mood. `M-RECR` is undefined (§15-R3). |
| 7 | Supply chain | edges (`RELATIONSHIP-GRAPH`) | `M-DEP`, `M-CAP` ✔ | Upstream disruption must remove options at the feasibility gate (step 2). |
| 8 | Facilities | `assets` + `geographic_presence` | `M-CAP`, `M-GEO` ✔ | Must determine where it can operate, and what can be seized, damaged or blockaded. |
| 9 | Customers | edges (`RELATIONSHIP-GRAPH`) | `M-RES`, `M-REP` ✔ | Demand must respond to reputation and disruption; customer loss must be a resource effect. |
| 10 | Competitors | edges (`RELATIONSHIP-GRAPH`) | `M-DEP` ✔, `M-EST` ⚠ | A competitor's action must change the expected value of options — notably "suspend" while a rival continues. **Downgraded**: that route is `M-EST`, which is named but undefined (§6, §15-R10). |
| 11 | Regulatory obligations | `obligations` | `M-LEG`, `M-VETO` at step 3 ✔ | Must raise the threshold at the veto gate and attach liability if overridden (§8.4 step 3); breach must accrue exposure. Specified as a successor to the inert `constraints` field (`agent_schema.py:181-183`) — but [`PERSON-MODEL.md`](PERSON-MODEL.md):461 claims the same succession for its M2, and the two are unreconciled (§2, §19 Q12). |
| 12 | Political relationships | edges (`RELATIONSHIP-GRAPH`) | `M-INF`, `M-DEP`, `M-CONT` ✔ | Must carry the founder's "political access" term in disproportionate influence (:137-139); also the regional-manager leverage in §9.3. |
| 13 | Labour relations | `blocs[].grievance_ledger` + relations edges | `M-COH`, `M-CONT` ✔ | Must determine the strike/refusal threshold. |
| 14 | Insurance exposure | `obligations` + insurer dependency edge | `M-DEP`, `M-VETO`, `M-RES` ✔ | Must carry the insurer's conditional veto and premium repricing (§9.3, §9.8). |
| 15 | Reputation | `reputation_public`, `reputation_private` | `M-REP` ✔ | As §12, row 17. |
| 16 | Market confidence | `market_confidence` | `M-RES` (financing cost) ✔, `M-ARB` ⚠ | Must raise the cost of capital, and is intended as the transmission channel from public events to boardroom pressure. **Downgraded**: bloc scoring at §8.4 step 4 reads `interest_vector`, `M-MEM` priors, `risk_posture` and beliefs — none of which is market confidence — so the "investor bloc scoring" route is not supported by the specified procedure. If it is to exist it must enter through `M-EST` or through an explicit new term. See §15-R13. |
| 17 | Operational vulnerabilities | `vulnerabilities: list[VulnerabilityRecord]` | `M-CAP`, `M-DEP` ⚠ | Determines what a disruption actually disables. **Charter-constrained**: [`../../CHARTER.md`](../../CHARTER.md):137-138 forbids real operational vulnerabilities. These must be fictional, mechanism-level and non-actionable. Flagged to [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) and §18. |

---

## 15. Attributes with no mechanism: rejection candidates

**In plain English:** this is the list of things the founder asked for that this specification could
not honestly connect to anything that changes the simulation. They are listed rather than quietly
included, because quietly including them is exactly the failure the founder warned about.

The founder's rule is unambiguous: an attribute that only produces prose "would be fake depth"
(:243-244). This document proposes striking these rather than deferring them (§6, rejection rule),
but **that is an owner decision and is not taken here** (§19 Q5).

| Ref | Attribute | Why it is unmapped | Proposed disposition |
|---|---|---|---|
| **R1** | **Founding history / historical development, as narrative** | The *structured seeds* (founding tick, founding doctrine as precedent records, founding relationship edges) map to `M-MEM`. The narrative history beyond those seeds reads into no mechanism. It would exist only to be rendered as text. | Keep the seeds; **strike the narrative field**. Generate founding prose from the seeds at display time via the LLM (§16) and never store it as state. |
| **R2** | **Organisational culture, as a free-text descriptor** | Culture is fully carried by `decision_procedure` parameters and the bloc `risk_posture` distribution (§12 row 7). A separate prose `culture` field would duplicate nothing and drive nothing. | **Strike the free-text field.** Retain culture only as parameters. |
| **R3** | **Recruitment methods** | Maps to `M-RECR`, but `M-RECR` itself is specified nowhere in the document set. **Checked, not assumed**, against the sibling documents as they stand on 18 July 2026: [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) uses "membership" only to mean *tier* membership (its §§ on the four fidelity tiers) and specifies no membership-flow, intake or recruitment mechanism; no other document in the set mentions `M-RECR` at all. The mechanism is named but undefined, which is a weaker claim than a mapping. | **Hold.** Either specify `M-RECR` properly in [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md), or strike the attribute. Owner decision. |
| **R4** | **Class structure** | Named in the country list. This document specifies no mechanism reading it and asserts no ownership of it. It plausibly belongs to [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md), but **naming another document is not a mechanism** — the test this document applies uniformly at R14. **Checked**: as at 18 July 2026 the only occurrence of "class structure" anywhere in `docs/` is the source record's own attribute list (`FOUNDER-REQUIREMENT-2026-07-18.md`:117); `POPULATION-FIDELITY.md` gives it no reading mechanism. | **Refer** to [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md). If that document does not give it a reading mechanism, strike it. On the check above, it currently does not. |
| **R5** | **National myths** | No mechanism. The nearest candidate is a belief prior on cohorts, which belongs to [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md). **Checked**: that document specifies no such prior as at 18 July 2026, and [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md):603 refers "historical grievances and national myths" *to* `BELIEF-AND-KNOWLEDGE-MODEL` — so the attribute is currently referred in a circle, with no document specifying it. Further, "a prior that makes certain narratives more credible" is not obviously distinct from `historical_grievances` and `M-MEM`. | **Strike, or merge** into `historical_grievances` + narrative-credibility priors. Owner decision. |
| **R6** | **Institutional memory** *(conditional, not unmapped)* | Maps cleanly to `M-MEM`, but `M-MEM` cannot exist before P0.6 delivers event, snapshot and replay foundations. Precedent records are event-sourced by definition. | **Keep, sequenced after P0.6.** Must not be built earlier. |
| **R7** | **Historical grievances (country)** *(conditional)* | Same as R6: structured grievance records with onset, cause, parties and evidence require event sourcing. | **Keep, sequenced after P0.6.** |
| **R8** | **Operational vulnerabilities (business)** *(constrained, not unmapped)* | Maps to `M-CAP`/`M-DEP`, but [`../../CHARTER.md`](../../CHARTER.md):137-138 forbids real operational vulnerabilities. The mechanism is sound; the *content* is charter-constrained and needs a safety rule this document cannot write. | **Keep the field, gate the content.** Requires a rule in [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md). |
| **R9** | **`reputation_private` as a distinct value** | Mapped to `M-REP` in §12, but honestly: the *distinct evidence base* that makes it different from `reputation_public` depends on `M-OBS`. **Checked (18 July 2026)**: `M-OBS` is specified in **no** document — it appears nowhere outside this one, and [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md), to which §20 assigns it, contains no mechanism register at all. [`PERSON-MODEL.md`](PERSON-MODEL.md):471 assigns the equivalent function (M12) to a *third* document. If nothing distinguishes observer classes, the two values will move together and one of them is redundant. **Superseded 19 July 2026 — founder decision 1A. `M-OBS` is no longer unowned**: it is specified in [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5, and the sub-mechanism that supplies the evidence base separating public from private reputation is **`M-OBS-SURF`** (the observable surface — what an entity exposes to a given observer class). The check above is retained as the record of what was true when it was made. | **Conditional, and now owned.** ~~Ownership of observation must be settled (§19 Q12) before this can be re-tested.~~ Ownership was settled on 19 July 2026 and this row is re-testable against [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md). It is **not yet re-tested and remains ⚠**, for a reason that document itself records: `reputation_private` stays conditional pending its open question Q2, and its `M-OBS-SURF` is blocked on a `ViewKind` gap (no kind exists for entity B's view of entity A), deferred to its owner decision Q-R. So the distinct evidence base is now *assigned* rather than *available*, and the redundancy risk named above is unchanged until that question is taken. |
| **R10** | **Option outcome estimation (`M-EST`)** | `outcome_estimate(o, d)` is the load-bearing term of `M-ARB` step 4 and no mechanism produced it. `M-EST` has now been added to the §6 register, but **naming is not specifying**: its interior, the beliefs it is evaluated under, its variance term and its treatment of relationship edges are all open (§19 Q13). Three attributes were marked ✔ on its strength — §12 row 16, §14 row 10, §14 row 16 — and are downgraded to ⚠. | **Hold, and specify or strike.** Until `M-EST` is specified, `M-ARB` is a formula with an unspecified term and the §9 example's scores are author-supplied. If `M-EST` cannot be specified in this document, name the owning document. |
| **R11** | **`self_understanding`** | One of the four founder-required views (§10.3), a first-class field on the authoritative record (§7.1) and a numbered consequence of the central principle (§4d) — and **no mechanism in §6 reads it**. `M-DIV` measures `served_priorities` against `public_mission`. `M-REP` reads reputation. It exists only to be rendered in the §10.3 table and the dossier, which is this document's own definition of fake depth. It cannot be deferred to [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) by omission, because §7.1 places it in this document's scope. | **Two candidate dispositions, neither taken here** (§19 Q16). **(a)** `M-COH` reads it: a coalition whose self-understanding diverges from its own `served_priorities` experiences internal strain — self-deception has a cohesion cost. **(b)** `M-ARB` step 4 reads it: self-understanding biases which options a bloc believes are *consistent with the organisation*, independently of interest. If neither is adopted, the field must be struck under the §6 rejection rule despite being founder-required — in which case the founder's four-view requirement needs re-reading, which is precisely why this is an owner decision. |
| **R12** | **`led_by` → interest-weight transfer (`M-LEAD`)** | The bridge between the person model and organisational behaviour was stated in a code comment ("biography shapes interest weights") and specified nowhere. §12 row 5 and `M-SUCC` both depend on it. `M-LEAD` has now been added to §6 **with mandatory bounds** — additive not assignment, weights not options, no sensitive identity attribute as a direct input — but the mechanism itself is undefined. Separately, [`PERSON-MODEL.md`](PERSON-MODEL.md):299-300 assigns **M13 ROLE-AUTHORITY** and **M14 FACTION-ALIGNMENT** to this document and neither is specified here, leaving `PERSON-MODEL.md`:694's mapping of `state.current_role` pointing at a mechanism in no document. **Superseded 19 July 2026 — founder decisions 1B and 1C.** That second half is discharged: M13 is specified as `M-AUTH` (§7.3), M14's organisation half as `M-FAC` (§7.4), and M14's alignment edge belongs to [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md); `state.current_role` now points at a mechanism that exists. **The first half is unchanged and is the reason this row is still open:** `M-LEAD` itself remains named-but-undefined, and nothing in the rulings specified it. | **Hold; specify with the §6 bounds intact, or strike `led_by`.** The bounds are not optional: this is the one place identity enters the arithmetic, and an unbounded person→interest map is where the founder's stereotype switch would be built. ~~M13/M14 ownership is §19 Q12.~~ M13/M14 ownership was answered on 19 July 2026 (§19 Q12); what survives here is `M-LEAD` alone. Note that §7.3's boundary rule tightens rather than relieves this: `M-AUTH` is specified to take **no** biographical input, so `M-LEAD` is now the *only* specified route from a person to organisational behaviour, and the case for bounding it is stronger, not weaker. |
| **R13** | **Attributes naming `M-ARB` that no step of §8.4 reads** | Four rows claimed `M-ARB` as a reader for fields the nine-step procedure never consults: `legal_exposure` (§12 row 18 — pricing is `M-RES` at step 2; no step reads accumulated exposure), `open_disputes` (§12 row 21), `elite_cohesion` (§13 row 21 — "across organs", a mode the single-organisation procedure does not have), and `market_confidence` (§14 row 16 — step 4 reads interest vector, memory, risk posture and beliefs, none of which is market confidence). This is **soft fake depth**: a plausible-sounding reader that does not, on the document's own specification, read it. All four are downgraded to ⚠. | **Add the step or strike the claim.** For each, either §8.4 gains an explicit step that consults the field, or the `M-ARB` mapping is removed and the attribute stands on its remaining readers alone. Owner decision under Q5. |
| **R14** | **Attributes mapped only by naming another document** | §15-R4 strikes class structure on the ground that "naming another document is not a mechanism", and that test was not applied uniformly. §13 rows 7, 8 and 19 were marked ✔ on the strength of a document reference. All three are downgraded to ⚠ and referred out with the same disposition as R4. **Row 8 (languages and religions) is the hazardous case** and is treated more strictly: the `M-OBS` half of its mapping is not supported by `M-OBS`'s own §6 definition, which concerns who observes a *decision* and says nothing about language gating reach or comprehension. A sensitive identity attribute that is retained in the schema, rendered into prose and read by no specified mechanism is exactly the configuration that produces stereotype-flavoured description with no causal justification for its presence. | **Refer, with the R4 rule: strike if the receiving document gives no mechanism.** For row 8 specifically, the safe default is **struck or gated, not retained** — and the choice is between extending `M-OBS`'s §6 definition to cover language-gated reach and comprehension explicitly, or handing the attribute to [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) with the referral recorded. Not resolved here (§19 Q17). |

A further item is recorded for completeness rather than as a rejection: **`label` on `InternalBloc`**
is explicitly presentation-only and is marked in the sketch as never read by any mechanism. It is
retained deliberately, because a human-readable name is needed for the interface, and marking it as
non-causal in the schema is preferable to pretending it does work.

---

## 16. Determinism, RNG substreams and the LLM boundary

### 16.1 Named RNG substreams are a hard prerequisite

**In plain English:** MERIDIAN currently draws every random number in the whole simulation from a
single sequence. If any part of the program draws one extra number, every later number everywhere
else changes. That has already been demonstrated, not merely suspected.

A3 §6 ([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):170-175)
records it as a defect nobody had previously identified:

> There are no named RNG substreams. Adding or removing a single random draw in one subsystem
> silently changes every subsequent draw in every other subsystem.

It was demonstrated by execution: adding a grievance to the one cohort that had none moved
`shipping_throughput_pct_of_baseline` from `0.6080711379477878` to `0.5973599412373322` (A3:161-163),
while changing cohort belief *values* by two orders of magnitude changed macro by exactly nothing
(A3:151-153). The single stream is created at `engine.py:83`, commented "the ONLY source of engine
randomness".

**This is fatal to the mechanism specified in §8, and it must be said plainly.** `M-ARB` step 6 draws
from a distribution for every organisational decision. On a shared stream:

- Adding **one bloc** to **one company** in a scenario would change the number of draws per tick and
  therefore shift every macro noise value for the rest of the run. National indicators would move
  because a designer gave a shipping firm a legal department.
- An organisation that arbitrates only when triggered would consume a variable number of draws per
  tick, making per-tick draw count a function of *events*, which is worse than the current situation
  where it is a function of scenario shape.
- The existing determinism test would mask the change as expected divergence (A3:174-175).

The requirement is therefore: **arbitration draws must come from a named substream keyed on
something stable** — run seed plus organisation id plus purpose, e.g.
`org:{org_id}:arbitration`. The same requirement is stated in
[`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) and [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md)
for profile generation and tier promotion, and is the same prerequisite.

Two facts about this prerequisite must not be lost:

1. **It is owned by P0.4A.** *(Corrected 19 July 2026; an earlier draft said it sat under no Phase 0
   item.)* The founder decision of 18 July 2026 created **P0.4A — establish a deterministic
   randomness architecture** as a Phase 0 workstream in its own right, ordered
   `P0.4 → P0.4A → P0.5 → P0.6`, and ruled that the problem is neither a world-model detail nor
   something to be hidden inside replay
   ([`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md) §P0.4A).
   Two riders bind this section: the required isolation is by subsystem, entity, relationship or
   interaction, purpose, and tick or event context — so **per-organisation streams alone are
   insufficient**, and `org:{org_id}:arbitration` above names a purpose-bearing key but not the full
   axis set; and the **mechanism is unchosen** between stateful named substreams and keyed /
   counter-based deterministic draws. **Nothing specified in §8 may be built until P0.4A passes.**
2. **It conflicts with a recorded architecture decision.** Audit §6.28 notes the single stream is
   not currently counted as a defect precisely because "the design is documented as one RNG in
   ADR-007". Introducing substreams supersedes an ADR, and
   [`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`) requires human approval for architecture and for
   "anything affecting determinism or authoritative state". This is squarely both. **No agent may
   make this call** (§19 Q3).

### 16.2 The LLM may narrate, never author

The existing determinism boundary works and this document does not weaken it. `ActionProposal`
(`agent_schema.py:374-393`) is the only type the gateway may return (`llm_gateway.py:35`), and it
carries no authority to change numbers. That is the honoured implementation of ADR-006 and of
[`../../CHARTER.md`](../../CHARTER.md):36-44.

**Two corrections to an earlier draft of this section are recorded here rather than silently
applied**, because both were breaches of the boundary this section claims to honour, and a
specification that quietly repairs its own violations teaches the reader nothing.

1. **`stated_justification` was LLM-drafted and read by `M-DIV`.** That is generated narrative
   altering authoritative state — forbidden by [`../../CHARTER.md`](../../CHARTER.md):37-40, by
   ADR-006, by the source record at :46-48, and by §7.1 of this document. The field is now split:
   `justification_frame` is engine-selected, structured and read by `M-DIV`; the prose is
   downstream, presentation-only and read by nothing (§9.7).
2. **LLM option proposal at `M-ARB` step 1 was described as the existing boundary "applied
   unchanged".** It is not: a proposed option enlarges the option space that a seeded draw ranges
   over, and changes the number of draws consumed, so a model call would influence numeric
   outcomes. P0.6 requires replay to make **zero** model or network calls
   ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.6 (`:87-88`)). Step 1 now carries the recorded-external-input
   requirement, and is specified as scenario-catalogue-only until that exists.

Applied to organisations:

| The LLM **may** | The LLM **must never** |
|---|---|
| Propose an additional option at `M-ARB` step 1, as an `ActionProposal` | Score an option, set a bloc weight, or select an outcome |
| Render a board meeting, a dissent, or a leaked memo as readable prose | Author a `DissentRecord` or alter one |
| Write an organisation's biography and briefing from its record | Invent a bloc, a founding fact, a relationship or an obligation |
| Explain a causal chain conversationally | Supply any link in that chain not present in recorded state |
| **Render** `stated_justification` prose from the engine-selected `justification_frame` and `served_priorities`, as presentation-only output read back by nothing (§9.7) | **Select or author `justification_frame`**, or change `actual_priorities` or `served_priorities`, or write any value that `M-DIV` reads |

The founder states this directly: the LLM "can turn that record into readable biographies, briefings
and conversations, but it must not invent or silently modify the authoritative facts" (:46-48), and
"the causal chain must come from recorded simulation state" (:293-294).

Every AI-generated advisory text must carry a visible provenance tag at the interface, not merely in
a documentation footnote ([`../../CHARTER.md`](../../CHARTER.md):141-142).

### 16.3 Stable identity

Once an organisation is materialised, its identity, founding record, bloc structure history and
decision history must never be regenerated differently (:236-237). This is the organisational form
of the person requirement that portraits must not change between sessions (:201-203). On a shared
RNG stream it is unachievable, because the draws an entity receives depend on its position in the
global draw order, which depends on everything that happened before it. §16.1 is the prerequisite
for this too.

---

## 17. Eight-question conformance

[`../../CHARTER.md`](../../CHARTER.md):118-130 requires every meaningful outcome to answer eight
questions, and states that output which cannot is flavour text that must not modify the simulation.
An organisational decision must answer all eight from recorded state. Using §9:

| # | Charter question | Answered from |
|---|---|---|
| 1 | What happened? | `OrganisationDecision.chosen_option` + the `M-CONT` implementation outcome. These are two answers, not one — deciding and doing are separate. |
| 2 | What caused it? | `trigger_event_id` + `causal_parents` on the emitted event (the declared field at `agent_schema.py:224`, currently never assigned — audit §6.13). |
| 3 | Which rule or mechanism applied? | `procedure_applied` + the mechanism ids that fired (`M-CAP`, `M-VETO`, `M-ARB`, `M-CONT`). |
| 4 | Which actors reacted? | `DissentRecord` entries + `M-CONT` compliance records per implementing entity + `M-OBS` observation records. |
| 5 | What assumptions were used? | Each bloc's scoring was performed on that bloc's **beliefs**, recorded as belief references, not on ground truth. |
| 6 | What uncertainty existed? | ⚠ **Not yet answerable.** The intended answer is the probability vector at step 6, plus the recorded `transform_id`, its parameters, `rng_substream` and `rng_draw_index`. But the score→probability transform is **not specified** (§8.4 step 6, §19 Q15), so this answer is currently circular: the trace would record a distribution the specification never defines. Aggregate scores alone are signed and unbounded and are not a distribution. |
| 7 | What alternative outcomes were possible? | The full option set including the two removed options and their removal reasons (§9.4). |
| 8 | What future options changed? | `M-LEG` exposure accrued, `M-COH` cohesion lost, `M-DEP` edges altered, `M-LEAK` hazard raised. |

Question 6 is worth a note. The founder additionally requires the system to answer "what evidence
did the entity observe" and "which prior experiences shaped the reaction" (:290-292). Those are a
strict **superset** of what `causal_parents` can answer, and they require per-entity observation
records (`M-OBS`) and precedent records (`M-MEM`) that do not exist in any form today. Both sit
downstream of P0.6.

---

## 18. Dependencies and sequencing

**In plain English:** none of this can be built yet, and the order in which the missing pieces have
to arrive is fixed. That is a reason to write the specification carefully, not a reason to start
building.

```text
Named RNG substreams  (under NO P0 item; supersedes ADR-007; owner decision required)
        │
        ▼
P0.4  authoritative-state contract  ──────►  which of the four views is authoritative (§10.3)
        │                                    whether MacroState is decomposed (§11.2)
        ▼
P0.6  event / snapshot / replay  ─────────►  M-MEM, M-LEAK, M-OBS, dissent history,
        │                                    institutional memory, grievance ledgers
        │                                    AND: recorded versioned external inputs, without
        │                                    which M-ARB step 1 must be scenario-catalogue-only
        │                                    (an LLM-proposed option changes both the support
        │                                    of the step-6 draw and the draw count, and replay
        │                                    must make ZERO model calls — HANDOFF.md:87-88)
        ▼
P0.5  cross-tier causal channels  ────────►  POPULATION-FIDELITY.md  ────►  M-INF
        │
        ▼
P0.7  simulation time and horizon  ───────►  M-RES (cost over time), M-CONT (delay is a
                                             first-class outcome, and timeline_days is
                                             currently never read — A3 §4)

P0.8 / B5  dual-use decision  ────────────►  gates §14 row 17 and §13 row 8 detail (§19 Q6)
```

Specific blocking statements, each stated once and plainly:

- **`M-ARB` cannot be built before named RNG substreams exist.** §16.1.
- **`M-ARB` is not fully specified even on paper.** Two of its terms are holes, not details:
  `outcome_estimate(o, d)` at step 4 (`M-EST`, §19 Q13) and the score→probability transform at
  step 6 (§19 Q15). Neither is a tuning parameter; the first is what makes arbitration causal and
  the second is what makes it probabilistic. Until both are answered, no implementation should be
  attempted from this document even if every P0 prerequisite were met.
- **LLM option proposal at step 1 must not be built before recorded versioned external inputs
  exist.** Otherwise arbitration outcomes depend on non-deterministic model output and replay
  cannot reproduce them.
- **`M-MEM`, `M-LEAK` and dissent history cannot be built before P0.6.** Precedent, leak and
  observation records are event-sourced by definition, and today the engine appends raw unvalidated
  dicts (`engine.py:165-173`) rather than instantiating the declared `Event` model, emits nothing
  when a delta is empty (`engine.py:163`), and persists nothing at all (audit §5.14).
- **The four-view model cannot be finalised before P0.4.** §10.3 states this document's *position* —
  that only authoritative reality is authoritative state — but a position is not a contract, and
  P0.4 owns the contract ([`../../HANDOFF.md`](../../HANDOFF.md):75).
- **`M-INF` is owned by [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md), downstream of P0.5.**
  This document must not restate it (§11.4).
- **Entity state cannot be written through `apply_deltas`.** `macro_state.py:23-47` handles top-level
  scalars only and skips nested blocks and unknown keys in silence (`:37-41`). A new, strict write
  path is required.
- **Three-way schema sync is a real, unautomated cost.** Any new schema must be hand-mirrored into
  `scaffold/schemas/*.schema.json` and `scaffold/backend/app/db/models.py`, with no generator and no
  sync test (audit §5.13). An entity ontology of this size may justify building the generator first —
  a sequencing decision for the owner, outside Phase 0.

**Safety coupling — apply the decision, do not reopen it.** Blocker B5 / P0.8 concerns the dual-use
influence-operations targeting schema (audit §5.12). **It was settled by founder decision on 18 July
2026.** An earlier draft of this section called it an open owner decision and cited
[`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):245 and
[`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.8 (`:90`) for it; **both anchors predate the decision and are
superseded.**

**Settling it did not clear it.** B5 now clears only when the **eight controls** the decision names
are **implemented and verified** — disclosure and any future acceptable-use wording are
supplementary, technical enforcement is mandatory — and **none of the eight exists in code**. The
coupling below is therefore live, not discharged. This document is coupled to it in two places:

1. **Organisations as messengers and amplifiers.** The existing `Campaign` schema
   (`agent_schema.py:320-346`) models a sponsor, a messenger with `perceived_independence`, and an
   amplification network. This document turns those into full entities with real internal structure,
   real dependency edges and real credibility mechanisms. That makes the influence model materially
   more capable, and therefore enlarges the surface the eight B5 controls were written against —
   controls that are, as at this document's date, entirely unbuilt.
2. **Operational vulnerabilities.** §14 row 17 / §15-R8.

Sensitive identity attributes appearing in the country list (§13 row 8) are governed by
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md), and the
founder's design rule applies without exception: sensitive identity affects social experience,
networks, exposure, discrimination, solidarity and cultural interpretation — never inherent
competence, morality or intelligence (:305-306). **The founder decision of 18 July 2026 states the
same rule in a wider form, and the wider form governs:** identity may affect lived experience,
relationships, discrimination, institutional access, media exposure and cultural interpretation, and
must never act as an inherent **competence, morality, loyalty, violence or manipulability**
coefficient. The three additions — loyalty, violence, manipulability — bear directly on this
document: **loyalty** because bloc cohesion and defection are core organisational mechanics, and an
identity-conditioned loyalty term is the fifth-column stereotype in schema form. At the
organisational level the rule means: an organisation's culture, cohesion, loyalty, propensity to
violence and decision quality **must never** be derived from the ethnic, religious or national
identity of its members. They must derive from `decision_procedure`,
`cohesion`, `morale`, `M-MEM` and recorded events only.

---

## 19. Open questions for the owner

Every question below requires a human decision. None is resolved in this document.

**Q1 — Person and role.** Does a person become a first-class entity distinct from the organisational
role they occupy, or is `MicroAgent` (`agent_schema.py:154-184`) extended in place? This determines
whether `RoleOccupancy` and `M-SUCC` exist as specified in §7.2, and it determines what happens when
a minister is replaced. Also relevant to [`PERSON-MODEL.md`](PERSON-MODEL.md).

**Q2 — Is a country decomposed?** Is `MacroState` (`macro_schema.py:73-87`) decomposed into a
composed `CountryEntity` with the 18 indicators demoted to a derived view (§11.2), or retained as
authoritative with entities hanging off it? P0.4 must settle this before §11 can be built.

**Q3 — deterministic randomness. Narrowed 19 July 2026.** The placement half is **answered**: the
founder decision of 18 July 2026 added it to Phase 0 as a new item, **P0.4A**, between P0.4 and P0.5,
and ruled out folding it into P0.6 or deferring it to the replacement architecture. **Still open:**
the mechanism — stateful named substreams or keyed / counter-based deterministic draws
(`RAID-REGISTER.md` DEC8; drafted, unapproved candidate
[`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)) —
whether the resulting ADR supersedes or narrows ADR-007 (audit §6.28;
`PUBLICATION-EXIT-CRITERIA.md` open question 15), and who owns the key scheme. Note that
"per entity, per entity type, or per subsystem" is no longer the full question: the founder scope
requires isolation across subsystem, entity, relationship or interaction, purpose, and tick or event
context, and **per-entity streams alone are insufficient**. This is a determinism and authoritative-state change requiring human
approval ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`)), and §16.1 shows `M-ARB` cannot be built
without an answer.

**Q4 — Is self-understanding authoritative?** An organisation's belief about its own priorities is a
*fact about a belief*. Is it authoritative state in its own right, or a derived projection of
authoritative reality? This constrains snapshot shape and replay, and belongs to P0.4.

**Q5 — The rejection rule.** Should this specification adopt the rule that any attribute with no
named reading mechanism is **struck rather than deferred** (§6)? The empirical case is audit §5.10 —
an inert weight let a 63× data error survive undetected — and there are no invariant tests at all
(audit §6.34). If adopted, §15 items R1, R2 and R5 are deleted rather than parked. This is a
specification-process decision, not a technical one.

**Q6 — B5 coupling. Restated 19 July 2026: the original trigger has already fired.** The question was
worded "held deliberately coarse **until B5 / P0.8 is decided**". **B5 was decided on 18 July 2026**,
so that wording no longer states a live question, and the risk it named — that a later B5 decision
invalidates a detailed specification — is no longer the risk that applies. The live question is:
should the detail level of §14 row 17 (operational vulnerabilities) and the organisational-messenger
modelling flagged in §18 be held deliberately coarse **until the decision's eight controls are
implemented and verified**, given that the policy is settled but **not one control is built**? The
decision binds *what* may be specified — control 5 forbids protected characteristics as optimisation
criteria for persuasion, and the not-permitted identity list applies — but says nothing about *how
much operational detail* may be written before enforcement exists. **That remains an owner question.
The decision must not be read as permission to resolve it, and no agent may resolve it.**

**This does not conflict with the sibling documents that record their equivalent question as spent**
([`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §10.4, [`PERSON-MODEL.md`](PERSON-MODEL.md) §7,
[`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) Q5). Those defer *identity-attribute* detail,
which the decision's permitted and not-permitted lists bound directly, so a substantive constraint
replaced the deferral. §14 row 17 is operational vulnerabilities and §18 is organisational
messenger and amplifier structure; no clause of the decision bounds either, so here nothing has
replaced the deferral.

**Q7 — Mesa.** Does Mesa remain the agent substrate (audit §8, decision 3)? This document is written
substrate-neutral (§5.2 C7), but if Mesa is retained, arbitration has to be reconciled with the Mesa
agent lifecycle, and the `Model.random` / `Model.rng` collision hazard (audit §6.27) is multiplied
across a much larger entity layer.

**Q8 — Bloc granularity.** Is a bloc always internal, or may an external stakeholder be modelled as
a bloc *of another organisation* for arbitration purposes, as §9.3 specifies for the insurer? The
alternative is to model every external pressure purely as a dependency edge. The chosen answer
determines whether `InternalBloc` is misnamed and whether one entity can appear inside another's
decision structure.

**Q9 — Who owns `M-RECR`?** This is no longer an open *question of fact*: it has been checked. As at
18 July 2026, no document in the set defines a membership-flow model — `M-RECR` appears nowhere
outside this document, and [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) uses "membership" only
in the sense of *fidelity-tier* membership. The open question is therefore the decision, not the
fact: **which document takes ownership, or is the attribute struck?** If none takes ownership, §12
row 9 (recruitment methods), §12 row 8, §13 row 7 and §14 row 6 all lose a named reader and must be
struck under Q5.

**Q10 — Does the default scenario need organisations at all in its first pass?** No business,
community organisation, foreign state, media outlet, court or regional authority exists as an entity
in `kestral-strait.json` today. Building §11 requires authoring a substantial amount of new scenario
data, and there is no scenario schema to validate it against (audit §5.13).

**Q11 — Should these documents be written at all before their prerequisites land?** They can be
written but not validated against any implementation. The founder requires capture before the
replacement architecture is designed (:340-341) while also requiring no interruption to Phase 0. The
owner should confirm that is the intended trade.

**Q12 — One mechanism register, or a crosswalk? Partially answered 19 July 2026; the register
question itself is still open.** [`PERSON-MODEL.md`](PERSON-MODEL.md):458-479
defines `M1`-`M20`; this document defines a twenty-one-entry `M-*` register (§6); neither references the other's
identifiers. The founder requires "a common entity ontology" under which mechanisms are consistent
(:322-334). Does the set adopt **one shared register** (the natural owner being
[`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md)), or an explicit **identifier crosswalk table**? Three
sub-decisions rode on this. **Two were taken by the founder on 19 July 2026 and are marked below.
The head question — one register or a crosswalk — was not, and no agent may take it.** The
sub-decisions are retained in their original wording, because what was open and when it closed is
itself evidence.

- **M13 ROLE-AUTHORITY and M14 FACTION-ALIGNMENT** are assigned to this document by
  `PERSON-MODEL.md`:472-473 and are specified nowhere. Are they specified here, reassigned, or
  recorded as unowned — noting that `PERSON-MODEL.md`:694 currently maps `state.current_role` to a
  mechanism that exists in no document?

  **✔ ANSWERED — founder decisions 1B and 1C, 19 July 2026. Specified here, with M14 split.**
  **M13 is this document's** and is specified as `M-AUTH` (§7.3): roles and offices, authority
  attached to a role, jurisdiction, delegation, appointment and removal, acting authority,
  conflicts between formal and practical authority, organisational command chains, and authority
  expiry and suspension. [`PERSON-MODEL.md`](PERSON-MODEL.md) may reference a person's current role
  but must not own the mechanism, so `state.current_role` now maps to a mechanism that exists.
  **M14 is split three ways and must not be duplicated**: faction definitions, membership rules,
  formal positions and faction structure are this document's as `M-FAC` (§7.4); the directional,
  historied person-to-faction alignment and loyalty edge and its changing strength are
  [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md)'s; and [`PERSON-MODEL.md`](PERSON-MODEL.md)
  consumes the resulting relationship projection. **What is still open on this bullet is naming
  only**: whether the surviving identifiers are `M-AUTH`/`M-FAC`, `M13`/`M14`, or a crosswalk entry
  binding them. That is the head question above, and it is unresolved. Note that
  [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) records the same
  deferral for its own `M-OBS*` identifiers, so three documents now await one naming decision rather
  than two.
- **Observation ownership.** §20 here assigns `M-OBS` to
  [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md); `PERSON-MODEL.md`:471 assigns
  M12 to [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md);
  `BELIEF-AND-KNOWLEDGE-MODEL.md` has no register at all. Which document owns observation?

  **✔ ANSWERED — founder decision 1A, 19 July 2026.**
  [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) owns it. `M-OBS` is
  specified in its §5, which retains this document's §6 definition and widens it from decisions to
  any world event, decomposing into `M-OBS-EXP`, `M-OBS-ACQ`, `M-OBS-ATTR` and `M-OBS-SURF`. §20's
  assignment to [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) is superseded, and
  that document owns *consumption* — belief updating, knowledge storage, confidence labelling — not
  production. `PERSON-MODEL.md`:471's M12 is superseded and split, and its clause assigning view
  production to [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md)
  is withdrawn. The chain is: world event → observation opportunity → entity-specific observation →
  belief/knowledge update → role-filtered projection → dossier presentation. This document sits at
  the first arrow only, as an emitter of world events.
- **Succession of `constraints`.** §8.4 step 3 and §14 row 11 here, and `PERSON-MODEL.md`:461 (M2
  FEASIBILITY-GATE), both claim to succeed `MicroAgent.constraints`. Which is the successor, or how
  is the succession split?

  **Still open. No ruling of 19 July 2026 touched it**, and it must not be read as having been
  swept up by the other two. At most one of `M-VETO`/`M-LEG` and M2 FEASIBILITY-GATE can be the
  successor to `agent_schema.py:181-183`, or the succession must be split explicitly.

**Q13 — What specifies `M-EST`?** `outcome_estimate(o, d)` is the load-bearing term of `M-ARB`
step 4 and is currently a hole with a name on it (§6, §15-R10). Four sub-questions: what produces
the estimate; whose beliefs it is evaluated under; where the variance term consumed by
`risk_posture` comes from; and how relationship edges enter it. If it is not specified in this
document, which document owns it? Until answered, §12 row 16, §14 row 10 and §14 row 16 are mapped
to nothing.

**Q14 — Is a veto absolute or costly?** §8.4 step 3 has been rewritten so that a veto raises an
option's threshold and attaches liability, cohesion cost and challenge exposure if overridden,
rather than deleting the option. Hard removal is reserved for `M-CAP` infeasibility. Is that the
right line? The founder forbids pressures that "force a single predetermined choice" (:271), and
§11.3 already allows a country organ to act ultra vires — but some prohibitions may genuinely be
absolute, and the owner must decide which, with what override thresholds. Note the failure mode on
each side: absolute vetoes make radicalisation (§10.4) unobservable; soft vetoes make an
organisation that never respects its own lawyers.

**Q15 — Which score→probability transform?** Step 6 draws from "a distribution over aggregate
scores", and aggregate scores are signed and unbounded, so the transform is undefined as written.
Softmax at some temperature, clamp-and-normalise and rank-based sampling each give materially
different odds for the runner-up option. This choice sets the system's entire sensitivity to bloc
power, it is where the founder's probabilistic requirement (:271) is actually implemented, and it is
where CHARTER.md:58 binds hardest. Which family, with what parameters, and where do the parameters
live? (§8.4 step 6 requires that they live in data, not engine constants, and that they be recorded
on the decision record.)

**Q16 — What reads `self_understanding`?** One of the four founder-required views is read by no
mechanism (§15-R11). Two candidates are offered — a `M-COH` strain term when self-understanding
diverges from served priorities, or an `M-ARB` step 4 consistency bias — and neither is adopted
here. If neither is taken, the field must be struck under the §6 rejection rule **despite being
founder-required**, which would mean the four-view requirement needs re-reading rather than the
field quietly kept. This is exactly the case where an agent must not choose.

**Q17 — Unmapped sensitive attributes: struck, gated or referred?** §13 row 8 (languages and
religions) is retained in the schema, rendered into prose, and read by no mechanism that this
document's own §6 definitions support (§15-R14). The general R4 rule says strike; the sensitivity of
the attribute arguably says strike *harder*, because an unmapped sensitive attribute is the exact
configuration that produces stereotype-flavoured description with no causal justification. But
languages and religions plainly *should* have causal effects — on media reach, comprehension,
network formation, exposure and solidarity. So: extend `M-OBS`'s §6 definition to cover
language-gated reach and comprehension explicitly, hand the attribute to
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md), or strike
it pending a mechanism? This is coupled to B5 / P0.8 (§18) and must not be resolved in isolation.

**Q18 — Is a faction a bloc, an organisation, or a third structure? Raised 19 July 2026.** Founder
decision 1C assigned faction definitions, membership rules, formal positions and faction structure
to this document, and §7.4 specifies them as `M-FAC` with a `FactionRecord`. The ruling assigned
**ownership**, not **shape**, and this document now carries three candidate representations of the
same thing: an `InternalBloc` of kind `personal_faction` (§8.2), an `OrganisationEntity` of kind
`party` (§7.1), and `FactionRecord` (§7.4). Three questions follow, and none may be taken by an
agent:

- May a faction span organisations — a tendency present in a ministry, an armed service and a party
  at once — and if so, does it appear as a bloc inside each host's arbitration? That is Q8's
  external-stakeholder question in a second form, and the two should be decided together.
- Does `FactionRecord` earn its existence, or is it `InternalBloc` plus a membership rule and an
  `OrganisationEntity` of kind `party` with a structure field? A third structure that adds nothing
  causal is fake depth by this document's own rule (§6), and §15 would have to carry it.
- If a faction is both a bloc of organisation A and a bloc of organisation B, which arbitration owns
  its `internal_cohesion`, and does dissent in A cost cohesion in B? An answer that says yes makes
  factional structure a genuine cross-entity causal channel; an answer that says no makes a
  cross-organisational faction a labelling convenience.

Whichever way it is taken, the boundary from decision 1C is **not** in question and is not reopened
by this: the person-to-faction alignment and loyalty edge stays in
[`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) under every candidate shape.

---

## 20. What this document does not specify

Stated explicitly, so that no reader assumes coverage that is not here.

- **It does not specify the person model.** Bloc leaders, executives and role occupants are
  specified in [`PERSON-MODEL.md`](PERSON-MODEL.md).
- **It does not specify the relationship edge.** Every dependency, rivalry, partnership, patronage
  and supply link named here is owned by [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md), including
  the requirement that edges be directional with history — "A trusts B" not implying the reverse
  (:77). Note that the social graph actually used by running code today is **undirected**
  (`nx.Graph()` at `scaffold/backend/app/simulation/diffusion.py:24`), so every tie is symmetric by
  construction.
- **It does not specify beliefs, evidence or confidence computation.** ~~This document's *position*
  is that `M-OBS` and all belief scoring belong to
  [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md).~~ ⚠ **That position is
  contradicted and currently unowned.** Verified as at 18 July 2026: `BELIEF-AND-KNOWLEDGE-MODEL.md`
  contains no `M-OBS` and no mechanism register at all, and
  [`PERSON-MODEL.md`](PERSON-MODEL.md):471 assigns the equivalent function (**M12 OBSERVABILITY**,
  "produces the public profile and the player intelligence profile") to
  [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md). Observation is
  therefore claimed by two documents and specified by neither. §19 Q12.

  > **Superseded 19 July 2026 — founder decision 1A.** The paragraph above is retained as the record
  > of what was true when written. It is no longer true, and this document's position is withdrawn
  > rather than corrected, because it was a position this document had no authority to hold.
  > **`M-OBS` is specified in [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md)
  > §5**, which retains this document's §6 definition and widens it from decisions to any world
  > event. It decomposes into `M-OBS-EXP`, `M-OBS-ACQ`, `M-OBS-ATTR` and `M-OBS-SURF`. This
  > document's assignment of `M-OBS` to
  > [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) is superseded. §15-R9's
  > `reputation_private` remains conditional pending open question Q2 in the owning document, but is
  > **no longer unowned**.
  >
  > Belief scoring is unaffected and this bullet's heading still holds:
  > [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) owns the **consumption** of
  > observations — belief updating, knowledge storage and confidence labelling — and this document
  > specifies none of it. What changed is that it does not own their **production**.

- **It does not specify observation.** Added 19 July 2026. Observation is owned by
  [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) (DRAFT, 19 July
  2026), per founder decision 1A: observation opportunity, sensor and source access, direct versus
  mediated observation, visibility, range, latency, degradation, source attribution, observation
  confidence, observation events, and the transformation from a world event into an
  entity-specific observation. This document is a **client** of it and must not respecify any of
  those. Its role is to emit decisions (§8.4 step 9), implementations (§11.3) and divergences
  (§10.4) as world events; which entities come to observe them, through what source and with what
  fidelity, is not determined here. Every `M-OBS` reference in this document — §10.5, §11.4,
  §12 row 13, §13 row 14, §17 questions 4 and 6, §18 — is to be read as a call into that document.
- **It does not specify population weighting.** `M-INF` is named as a client requirement only; the
  model belongs to [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md), downstream of P0.5.
- **It does not specify the dossier interface.** Tab structure, layout and interaction belong to
  [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md).
- **It does not resolve B5 / P0.8**, and must not be read as having done so.
- **It does not propose an implementation order, a schedule or an estimate.** The work is backlog.
- **It does not modify any code, any schema, anything under `scaffold/`, or anything under
  `docs/delivery/`.** No such change was made in producing this document.

---

*End of specification. DRAFT — pending owner review. Written 18 July 2026; amended 19 July 2026 to
apply founder ownership rulings 1A, 1B, 1C and 1D. Still DRAFT, still BACKLOG, and still describing
no implemented software.*
