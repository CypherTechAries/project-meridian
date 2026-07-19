# RELATIONSHIP-GRAPH — the temporal relationship graph

> ## ⚠ SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing in this document exists in MERIDIAN's code.** Not one field, not one mechanism,
> not one query. This is a specification of intent for a future architecture. Every statement
> about the relationship graph's behaviour is written in the future or obligatory tense
> (*will*, *must*, *is specified as*) because none of it describes working software.
>
> Where this document describes something that **does** exist today, it says so explicitly and
> cites `file:line`, so the boundary between the built and the specified is always visible.

**Status:** DRAFT — pending owner review.
**Date:** 18 July 2026.
**Amended:** 19 July 2026 — the founder ownership rulings of 19 July 2026 are applied. This document
**gains** ownership of two mechanisms: the directed, historied person-to-faction alignment edge
(ruling 1C, §5.2 and §5.4) and the obligation ledger that [`./PERSON-MODEL.md`](./PERSON-MODEL.md)
consumes (§6.4, rule RG-T11). Both are additions. Nothing previously specified in this document is
withdrawn by them, and no open question in §14 is closed by them. One question is **opened** by them
— **OQ-17**, the placement of per-person dissent and defection probability, which ruling 1C's split
does not unambiguously assign to any of the three documents it names.
**Disposition:** **BACKLOG. This work must not interrupt Phase 0 remediation.** No part of it is
proposed for implementation now. See [`../../HANDOFF.md`](../../HANDOFF.md) §"Backlog — captured,
deliberately not started" and
[`./FOUNDER-REQUIREMENT-2026-07-18.md`](./FOUNDER-REQUIREMENT-2026-07-18.md) lines 5–6 and 340–341.
**Source record:** [`./FOUNDER-REQUIREMENT-2026-07-18.md`](./FOUNDER-REQUIREMENT-2026-07-18.md).
Where this document and the source record disagree, the source record is right and this document
is wrong. **Two carve-outs:** where the source record and the **founder decision of 18 July 2026 on
dual-use influence targeting (B5)** differ *on the subject of that decision*, the decision governs,
because it is the later instruction (§13.4 applies the decision on that basis); and where the source
record and the **founder ownership rulings of 19 July 2026** differ *on the subject of those
rulings*, the rulings govern, on the same later-instruction ground (§5.4 and rule RG-T11 apply them).
Each carve-out is confined to its own instruction's subject; everywhere else the source record
governs without qualification. In particular, `faction_alignment` is **not** one of the source
record's thirteen relationship kinds (lines 73–75), and §5.4 states that fact rather than implying
otherwise.
**Authority:** governed by [`../../CHARTER.md`](../../CHARTER.md). Nothing specified here may
weaken the determinism boundary (ADR-006) or the eight-question standard
([`../../CHARTER.md`](../../CHARTER.md) lines 118–133).

---

## Table of contents

1. [Plain-English layer](#1-plain-english-layer)
2. [What exists today](#2-what-exists-today-the-honest-boundary)
3. [Why symmetric edges are inadequate](#3-why-symmetric-edges-are-inadequate)
4. [The specified edge model](#4-the-specified-edge-model)
5. [Relationship kinds](#5-relationship-kinds)
6. [The temporal model — the hard part](#6-the-temporal-model--the-hard-part)
7. [Causal use — how edges must change behaviour](#7-causal-use--how-edges-must-change-behaviour)
8. [Graph scale and fidelity tiers](#8-graph-scale-and-fidelity-tiers)
9. [Schema sketch](#9-schema-sketch)
10. [Query patterns](#10-query-patterns-the-player-facing-social-graph-requires)
11. [Determinism, RNG substreams and replay](#11-determinism-rng-substreams-and-replay)
12. [Dependencies and sequencing](#12-dependencies-and-sequencing)
13. [Attributes that failed the causal-value test](#13-attributes-that-failed-the-causal-value-test)
14. [Open questions for the owner](#14-open-questions-for-the-owner)
15. [Cross-references](#15-cross-references)

---

## 1. Plain-English layer

### What this document is about

MERIDIAN is intended to simulate a society, not a command room. Societies run on relationships:
who trusts whom, who owes whom, who is afraid of whom, who will take a phone call at two in the
morning. The source record requires that these relationships have **direction** and **history**.

Direction means the obvious real-world fact that feelings are not mutual. A junior officer may
deeply respect a general who barely knows the officer's name. A minister may fear a newspaper
editor who regards the minister as harmless. If the simulation stores one number for "the
relationship between A and B", both of those situations become impossible to express, and the
resulting world will feel wrong in a way players cannot name but will notice.

History means that a relationship is not a snapshot. It is the accumulated residue of everything
that has happened between two entities. Two people with identical current trust scores are not
interchangeable if one pair has been friends for thirty years and the other met last week. And
crucially: a relationship should be able to carry **unfinished business** — a favour never repaid,
a betrayal never acknowledged, a promise made in a crisis and quietly forgotten. That unfinished
business must be able to lie dormant for a long time and then resurface when circumstances make it
relevant.

### Why this is its own document

Direction is a small change: store two records instead of one. **Time is the hard part**, and it is
the reason the source record's relationship requirement cannot be folded into the person or
organisation models.

Storing a relationship's history is not the same as storing its current value. If the graph only
holds current values, the simulation can answer "does A trust B?" but not "how did these two come to
distrust one another?" — which is one of the questions the source record explicitly requires profiles
to support ([`./FOUNDER-REQUIREMENT-2026-07-18.md`](./FOUNDER-REQUIREMENT-2026-07-18.md) line 189).
It also cannot answer "did A trust B at the time A made that decision?", which is the question that
makes an after-action review meaningful. A player reconstructing why a minister ignored a warning
needs the state of the world *as it was then*, not as it is now.

So the graph must be queryable at a point in time, not only in its current state. That is a
different data structure and a different set of costs, and it depends entirely on an event log the
project does not yet have.

### What this document does not do

It does not propose starting the work. It does not decide anything requiring a human choice.
Everything needing a decision is written as an open question in §14.

---

## 2. What exists today (the honest boundary)

Everything in this section **does** exist in the repository at commit `71fa329`. It is stated here
so that the rest of the document can be read as an extension of a known baseline rather than as a
description of capability.

### 2.1 The declared edge schema — exists, never used

`Relationship` at
`scaffold/backend/app/simulation/schemas/agent_schema.py:190-200` is a Pydantic model with six
fields:

| Field | Type | Declared at |
|---|---|---|
| `agent_a` | `str` — "Source agent/cohort id." | `agent_schema.py:193` |
| `agent_b` | `str` — "Target agent/cohort id." | `agent_schema.py:194` |
| `valence` | `float`, −1..1 | `agent_schema.py:195` |
| `trust` | `float`, 0..1 | `agent_schema.py:196` |
| `dependency` | `float`, 0..1, "Dependency of a on b" | `agent_schema.py:197` |
| `last_interaction_tick` | `int`, ≥0 | `agent_schema.py:198-200` |

It is **declared only**. It is instantiated nowhere in `scaffold/backend/app`. It is populated in no
scenario. It is nonetheless mirrored into a published JSON Schema at
`scaffold/schemas/relationship.schema.json` (54 lines), which nothing validates anything against
(audit §5.13, `docs/delivery/CURRENT-STATE-AUDIT.md:241`).

Two observations matter for this specification:

- Direction is **implied by field naming only** (`agent_a`/`agent_b`, and the `dependency`
  docstring "of a on b"). `valence` and `trust` carry no directional marker at all, so the model
  cannot express "A trusts B but B does not trust A" without storing two records and leaving a
  reader to guess whether both were intended.
- `last_interaction_tick` is the entire temporal content. There is no history, no prior value, no
  event reference and no unresolved-event record.

### 2.2 The per-agent relationship map — exists, never populated

`MicroAgent.relationships` at `agent_schema.py:175-177` is `dict[str, float]`, documented as
"Valence toward other agents/roles, −1..1". This is weaker than `Relationship`: one scalar per
counterpart, no trust, no dependency, no time.

It is directional by construction (the map belongs to one agent), which is the single correct
instinct in the existing design. It is populated for **none** of the six institutional agents in
`scaffold/scenarios/kestral-strait.json` — the scenario contains no `relationships` key at all.

### 2.3 The graph that running code actually uses — exists, and is undirected

The only social topology consumed by executing code is `NetworkPosition.bridges_to`
(`agent_schema.py:86-88`), read by `build_cohort_graph` (`scaffold/backend/app/simulation/diffusion.py:18-37`).

Facts, each verifiable:

- The graph is `nx.Graph()` — **undirected** (`diffusion.py:24`, and the docstring at `:19` says so
  plainly: "Build an undirected influence graph"). Every declared tie is therefore symmetric by
  construction.
- Edge weight is the **mean internal cohesion of the two endpoints** (`diffusion.py:35`). It ignores
  population entirely, ignores tie type entirely, and ignores direction entirely.
- The docstring at `:87` says `bridges_to` holds "IDs of cohorts/institutions this cohort bridges
  to", but institution targets are silently dropped by the `if other in cohesion` guard at
  `diffusion.py:34` — `cohesion` is built from cohorts only (`diffusion.py:25-28`).

The demo data already contains an asymmetry that the graph builder silently erases. In
`scaffold/scenarios/kestral-strait.json`:

| Declared edge | Reciprocal declared? |
|---|---|
| `urban-professional-vantaran` → `urban-nationalist-youth` (`:74`) | yes (`:237`) |
| `coastal-creole-fishing` → `military-veteran-families` (`:117`) | yes (`:197`) |
| `coastal-creole-fishing` → `urban-nationalist-youth` (`:117`) | **no** — `:237` lists only `urban-professional-vantaran` |
| `inland-highland-minority` → *(none)* (`:157`) | n/a — isolated node |

The third row is a one-sided declaration that `diffusion.py:36` converts into a mutual influence
channel. Nothing reports this. The fourth row means the 451,000-person highland cohort (`:121-122`)
is an isolated node: at `diffusion.py:72-73` its neighbour influence is `0.0`, so it can only move
through `seed_pressure` and jitter, never through the society around it.

### 2.4 What is absent

There is, today, **no** temporal graph, no edge history, no unresolved-event record, no point-in-time
query, no edge typing, no per-dimension confidence, no observer-relative view of any edge, and no
mechanism anywhere that reads a relationship in order to change a simulation outcome. `Relationship`
and `MicroAgent.relationships` are both read by zero code paths outside their own schema
declarations and JSON mirrors.

**This is an advantage, and the specification should exploit it.** The audit records the same point
in the project's favour (`docs/delivery/CURRENT-STATE-AUDIT.md` §3, lines 43–44: "the shape of the
thing that is missing has already been thought about, and that materially reduces the cost of
building it"). Because nothing reads either structure, replacing them costs nothing at the call
sites. There are no call sites.

**Consequence for this document:** what follows is specified as a **replacement** of `Relationship`,
not an extension of it. Turning a per-counterpart `float` into an object is in any case a breaking
change to a published mirror (`scaffold/schemas/micro_agent.schema.json`), so the extension framing
would be false comfort.

---

## 3. Why symmetric edges are inadequate

The source record states the requirement in one line
([`./FOUNDER-REQUIREMENT-2026-07-18.md`](./FOUNDER-REQUIREMENT-2026-07-18.md) line 77):

> Relationships should have direction and history. "A trusts B" does not imply that B trusts A.

This section sets out why that is a modelling necessity rather than a fidelity preference, because
the cheaper symmetric design will otherwise keep re-proposing itself.

### 3.1 Asymmetry is where the interesting mechanisms live

A symmetric graph cannot represent any of the following, and each is a mechanism the charter's
causal vocabulary already implies:

| Real configuration | Requires | Charter primitive it feeds |
|---|---|---|
| Officer reveres a general who does not know them | asymmetric `respect` | *Change institutional behaviour* |
| Minister fears an editor who considers them irrelevant | asymmetric `fear` | *Create public exposure* |
| A supplier depends on a buyer who has three alternatives | asymmetric `dependency` | *Create an obligation* |
| A is B's trusted source; B is not A's | asymmetric `trust` on an information channel | *Change a belief* |
| A holds compromising knowledge of B; B holds none of A | asymmetric `leverage` | *Enable or remove future options* |

Every one of those is a *power gradient*. Power gradients are asymmetries by definition. A symmetric
graph is structurally incapable of representing power, and a crisis simulation that cannot represent
power gradients is modelling a different thing from the one the charter describes.

### 3.2 Symmetric edges produce a specific, silent failure mode

The failure is not that the world feels flat. It is that **the graph averages away the very thing
the player is trying to find**. In a symmetric model, the natural authoring instinct is to store the
mean of two directional values. A relationship where A trusts B completely and B trusts A not at all
becomes indistinguishable from one where both parties are mildly suspicious. The first is a
recruitment opportunity, a leak vector and a betrayal waiting to happen. The second is nothing. The
model would render them identically.

The existing code demonstrates the mechanism by which such errors go unnoticed: the one-sided
`coastal-creole-fishing` → `urban-nationalist-youth` declaration at `kestral-strait.json:117` is
symmetrised at `diffusion.py:36` with no warning, no log line and no test. This is the same class of
silent failure the audit documents for `represents_population` (§5.10,
`docs/delivery/CURRENT-STATE-AUDIT.md:213`), where an inert field allowed a 63× data error to survive
undetected. **An unread or lossy relationship attribute produces no error when it is wrong.**

### 3.3 Asymmetry must be structural, not conventional

Storing two `Relationship` rows and relying on authors to keep them coherent is not sufficient. The
specification requires that direction be **structural**: an edge belongs to a `(source, target)`
ordered pair and there is no such thing as an undirected edge in the model. A reciprocal
relationship must be represented as two edges that may be created, updated, decayed and destroyed
independently, and the schema must make it impossible to express a relationship without stating
whose view it is.

**Specified invariant RG-1.** Every relationship record must name a `source_entity_id` and a
`target_entity_id`, and every attribute on that record must be read as *the source's orientation
toward the target*. No attribute on an edge may describe a mutual property. Where a genuinely mutual
property is needed (for example, "these two entities have a shared employment history"), it must be
recorded as an event both edges reference, never as a field on one edge.

---

## 4. The specified edge model

### 4.1 Plain-English layer

An edge is one entity's stance toward another. It carries a set of scored dimensions (how much do I
trust them, how much do I fear them, what do I owe them), a set of relationship kinds (are they
family, a rival, my employer), and a link back into the history that produced those scores.

Nothing on an edge may be a number that exists only to be displayed. Each dimension below is
specified together with the mechanism that must read it. Where no mechanism could be named, the
attribute is struck rather than deferred — see §13.

### 4.2 Edge dimensions

The source record specifies twelve items
([`./FOUNDER-REQUIREMENT-2026-07-18.md`](./FOUNDER-REQUIREMENT-2026-07-18.md) lines 79–80): trust;
affection; fear; respect; dependency; ideological alignment; resentment; familiarity; leverage;
shared history; last interaction; important unresolved events.

Nine are specified below as scored dimensions. Three are specified as **structural, not scalar** —
`shared history`, `last interaction` and `important unresolved events` are temporal constructs and
are specified in §6, not here. Reducing them to numbers is precisely the fake-depth failure the
source record warns against (lines 241–254).

| # | Dimension | Range | The source's orientation toward the target | Mechanism that must read it | Consumer document |
|---|---|---|---|---|---|
| D1 | `trust` | 0..1 | Belief that the target will tell the truth and honour commitments | **Source credibility weighting**: an incoming claim's belief update must be scaled by the receiver's trust in the sender. **Disclosure gate**: the probability that an entity shares restricted information across an edge must fall steeply with trust, approaching but not reaching zero. Dispositional, therefore RG-3b — a curve, not a wall. | [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md) |
| D2 | `respect` | 0..1 | Assessment that the target's judgement is worth weighting, independent of honesty | **Advice weighting** in decision formation: competing internal recommendations must be weighted by respect before an organisation resolves an action. Distinct from D1: an entity may believe an adviser is honest but wrong. | [`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md) |
| D3 | `affection` | 0..1 | Willingness to bear personal cost on the target's behalf without expectation of return | **Cost-tolerance modifier** on actions that harm the source but benefit the target; **loss reaction** magnitude when the target is harmed. ⚠ Collinearity risk with D1/D2 — see §13. | [`./PERSON-MODEL.md`](./PERSON-MODEL.md) |
| D4 | `fear` | 0..1 | Expectation that the target can and will impose serious cost on the source | **Compliance probability** under an instruction or threat from the target; **upward-reporting suppression**: high fear must reduce the probability that the source transmits unwelcome true information to the target. | [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md) |
| D5 | `dependency` | 0..1 | Degree to which the source's resources, position or safety rest on the target | **Defection cost** in coalition resolution; **constraint on opposition**: an entity's ability to act against a target must be reduced in proportion to dependency. Feeds the charter's *Create an obligation* primitive. | this document §7.3 |
| D6 | `ideological_alignment` | −1..1 | Agreement on the value dimensions the scenario defines | **Coalition formation affinity** and **narrative resonance**: alignment must modulate how readily a claim from the target is accepted on identity grounds rather than evidential grounds. | [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md) |
| D7 | `resentment` | 0..1 | Accumulated unaddressed grievance toward the target | **Defection, leak and retaliation probability** when an opportunity arises. Specified as the primary channel by which a dormant history produces a sudden action. | this document §6.4 |
| D8 | `familiarity` | 0..1 | Cumulative depth of contact — how well the source knows the target | **Contact reachability**: whether the source can initiate direct communication at all, and through which channel. Gates the graph's information paths before any trust weighting applies. | [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md) |
| D9 | `leverage` | 0..1 | Capacity to compel the target through knowledge, obligation or material control | **Coercive action availability**: an action requiring compliance from the target must become steeply improbable and heavily priced as leverage falls. Dispositional, therefore RG-3b — never removed from the action space outright. Feeds *Enable or remove future options*. | this document §7.3 |

**Specified invariant RG-2 — two admissible categories, and no third.** Every field specified anywhere
in this document must satisfy exactly one of:

- **Category (a) — mechanism-backed.** The field is read by at least one **named mechanism that
  changes authoritative simulation state**. All nine dimensions above are category (a).
- **Category (b) — explainability-backed.** The field is **required by a named question in
  CHARTER.md's eight-question standard** ([`../../CHARTER.md`](../../CHARTER.md):118-133) and the
  specific question must be cited at the field. Provenance and causal-chain fields
  (`causal_parents`, `evidence_observed`, `alternatives_considered`) are category (b): they change no
  simulation outcome, and the charter nonetheless requires them.

Anything satisfying neither is **struck** from the schema, not marked "future use". A field that
renders in the interface and satisfies neither category is struck regardless of how useful the
rendering is. The empirical justification is audit §5.10: an attribute nothing reads produces no
error when it is wrong, and MERIDIAN has no invariant tests to catch a repeat (audit §6.34).

Category (b) is **not** a general exemption. It admits only the causal-explanation spine the charter
demands. It must never be used to retain a field on the ground that a dossier tab displays it — the
schema sketch in §9 annotates every field with the category it satisfies precisely so that this
distinction can be audited field by field, and §13's rejection list must be checked against those
annotations, not against §4.2 alone.

**Specified invariant RG-3a — structural gates may be absolute, and must be enumerated.** A gate that
turns on the *existence* of a path, a channel or a formal relation may select an outcome outright,
because the limit it expresses is structural rather than dispositional: an entity cannot telephone
someone whose number it does not have. Every such gate must appear in the exhaustive list below, and
no mechanism anywhere may introduce an absolute gate that is not on it. The list is auditable by
construction; adding to it is a specification change requiring owner review.

| Absolute structural gate | Where specified |
|---|---|
| Edge existence — no edge and no institutional channel, no direct transmission | RG-M1 step 1; §5.2 `friend` / `professional_contact` |
| Path existence — no path of any kind from a holder, no acquisition of the information | RG-M5 *Knowledge*, subject to RG-3c |
| Reach — no edge and no institutional route toward the target, no direct action upon it | RG-M5 *Reach*, subject to RG-3c |
| Formal-relation existence for chain-of-command instruction | RG-M5 *Authority* — the `employer` / `political_patron` kind. Whether an instruction is **obeyed** is dispositional and falls under RG-3b |

**Specified invariant RG-3b — dispositional dimensions may only modulate.** `trust` (D1), `respect`
(D2), `affection` (D3), `fear` (D4), `dependency` (D5), `ideological_alignment` (D6), `resentment`
(D7), `familiarity` (D8) and `leverage` (D9) are dispositions, not structures. None may select an
outcome outright. Each may only modulate a probability, a weight or a threshold. **This reclassifies
two gates stated elsewhere in this document as steep probability curves rather than hard cut-offs:**

- D1's disclosure gate (§4.2) — low trust must drive the probability of disclosing restricted
  information toward zero, not set availability to false.
- D9's coercive-availability gate (§4.2, RG-M3, RG-M5 *Recruitment*) — low leverage must make a
  compliance-requiring action steeply improbable and heavily priced, not remove it from the action
  space.

The distinction is not pedantry. "Modulate a threshold" and "be a threshold" are different things,
and the earlier drafting of this document used one phrase for both. A reader must be able to tell,
for every gate, whether it is an absolute structural limit or a disposition rendered as a wall.
Dispositions rendered as walls are stereotype switches wearing a threshold.

**Specified invariant RG-3c — no categorical capability may fall out of a chain.** RG-3b constrains
each mechanism individually. It does not constrain their composition, and composition is where the
rule is actually defeated. Consider the chain this document itself specifies: shared identity raises
the prior probability that an edge exists (§13.4) → edge existence and `familiarity` gate contact
reachability (D8, RG-M1 step 1) → reachability bounds knowledge acquisition and reach (RG-M5). Every
step is probabilistic; the terminus is absolute; and the composite result is that group membership
structurally determines what an entity can ever learn or do. That is the stereotype switch arrived at
by composition, and no per-attribute test will catch it.

Therefore: **no chain of mechanisms may make a categorical capability — knowledge acquisition, reach,
or action availability — a function of group membership, even where every individual step is
probabilistic.** The concrete guards are:

1. **Residual-path guarantee.** Every entity must retain at least one non-zero-probability
   information and contact path that is independent of identity-correlated edges — institutional
   routes, media channels, or weak ties. An entity whose entire reachable set is identity-correlated
   is a specification defect, not a modelling result.
2. **Penalised, not absolute, where the gating set is identity-correlated.** Wherever an RG-3a gate's
   gating edge set is identity-correlated, that gate must be specified as heavily penalised rather
   than absolute. RG-3a's *Knowledge* and *Reach* rows are explicitly subject to this.
3. **Compositional test, owned elsewhere.** The test is a **requirement on**
   [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md), not a
   per-attribute check: over generated graphs, the reachable information set and action set of
   otherwise-matched entities must not differ systematically by group membership. This document
   states the requirement; it does not specify the test.

RG-3a–c are the source record's rule at lines 87–91 and 271 applied to the relationship layer.

### 4.3 Edges are not ground truth either

The source record's four-view model (lines 147–165) applies to edges, and this is not a refinement
that can be added later — it changes the storage shape.

**Five views must be distinguished — four from the source record, plus one addition this document
argues for separately.** An earlier draft of this section claimed the source record's four views
applied "exactly" while silently substituting a different set: it dropped the **public profile** view
and put "A's model of the reciprocal edge" in its place. That was a divergence presented as fidelity,
and under the standing rule that where this document and the source record disagree the source record
is right, it is corrected here.

| View | Source | What it holds | Authoritative? |
|---|---|---|---|
| **Authoritative edge** | Source record line 149 | What is actually true of A's stance toward B | The authoritative **projection** — see the note below and OQ-2 |
| **A's self-understanding of the edge** | Source record lines 151–152 | What A believes about their own stance. A may sincerely believe they trust B while behaving otherwise. | Derived projection |
| **Public view of the edge** | Source record lines 154–155 | What is publicly reported or commonly believed about the tie between A and B — "this minister is widely believed to be in the shipping company's pay". May contain propaganda, errors, omissions and outdated information. | Derived projection |
| **Player intelligence view of the edge** | Source record lines 157–159 | What the player's role has evidence for, labelled *Confirmed · Reported · Assessed · Disputed · Unknown · Possibly deceptive · Outdated · Restricted* | Derived projection |
| **A's model of the reciprocal edge** | **Not in the source record — an addition by this document** | What A believes B's stance toward A to be. The gap between this and the authoritative reciprocal edge is where betrayal, misjudged alliance and failed recruitment live. | Derived projection |

**The public view is not an observer view, and that distinction is load-bearing.** It is the only one
of the five that is a property of the *world* rather than of a single observer: it is what "everyone
knows", correct or not. It is also the exact surface an influence campaign manufactures and attacks —
a campaign does not change what a minister actually owes a shipping company, it changes what is
commonly believed about it. Whether it is stored as a distinct projection type or as a designated
pseudo-observer instance of the observer-view type is an implementation decision with real cost
consequences and is recorded as **OQ-13**. This document's position is that it must be a first-class
projection, because a pseudo-observer would have no natural owner for propaganda-driven drift and no
place to record the campaign that caused it.

**The fifth view is an addition and is justified separately.** "A's model of the reciprocal edge" is
not in the source record's list. It is retained because it is the only one of the five that is read by
a named simulation mechanism — RG-M4 coalition formation and RG-M2 influence weighting both consult
it — which places it in RG-2 category (a). It is labelled an addition rather than folded silently into
the source record's four. Note that the source record's wording is "**at least** four different
versions of an entity's profile" (line 147): it enumerates four and does not close the set at four,
so a fifth view is not contrary to the source record — it is simply unenumerated there and must be
justified on its own merits, which is what this paragraph does. Whether the owner accepts the addition
is **OQ-14**.

**Specified invariant RG-4.** Confidence labels must attach **per dimension**, not per edge. A
player may have confirmed that two ministers are related by marriage while only having an assessed
view of whether one resents the other. Attaching a single label to the whole edge would collapse
exactly the distinction the intelligence-product framing exists to make.

**Dependency, stated plainly — and the question is not the one it looks like.** It is tempting to ask
which of the five views is authoritative. That framing is wrong, and an earlier draft of this document
asked it. Under rule RG-T1 (§6.2), **none of the five views is primary state**: the authoritative
record of a relationship is the ordered `RelationshipEvent` stream, and *all five views, including the
"authoritative edge", are projections of it*. What distinguishes the authoritative edge from the other
four is not primacy but filtering — it is the **unfiltered** projection, computed from the whole event
stream with no observer restriction, no self-serving distortion and no propagation delay. The other
four are projections of restricted, distorted or delayed subsets of the same stream.

This document states that one position consistently in §4.3, §6.2, §6.3 and §9. It follows that the
question for P0.4 is not "which view wins" but whether the authoritative-state contract admits an
**event stream** as authoritative state with all edge values derived — and if it does, what artefact
is hashed when two runs are compared for reproducibility. That is recorded as open question **OQ-2**,
reworded accordingly. P0.4 ("Define the authoritative-state contract across macro/meso/micro",
[`../../HANDOFF.md`](../../HANDOFF.md):75) must settle it; this document's position is a claim about
the P0.4 contract, not a substitute for it.

Note also that today there is exactly one copy of the truth for every structure in the system, and
the only role-asymmetry primitive that exists at all is `EventVisibility`
(`agent_schema.py:203-208`, values `public`/`classified`/`leaked`), which is never populated
(audit §6.20). There is no authentication or authorisation layer of any kind (audit §7, IAM row), so
"the player's role" currently has nothing to resolve against. The player intelligence view therefore
has **no attachment point today**, and this document must not be read as describing a layer over
existing records. There is nothing to layer over.

**Specified invariant RG-5.** Observability and evidential confidence are two axes and must not be
overloaded onto one enum. `EventVisibility`'s three values answer *who may observe*. The eight
confidence labels answer *how well the observation is evidenced*. An edge may be freely observable
and poorly evidenced, or restricted and confirmed. The schema must carry both independently.

---

## 5. Relationship kinds

### 5.1 Plain-English layer

Dimensions say *how* A feels about B. Kinds say *what B is to A*. The source record lists thirteen
(lines 73–75). On inspection four of those are not kinds at all — they are questions you can answer
by looking at the dimensions and the obligation ledger. Specifying them as stored kinds would create
two sources of truth that can disagree, which is a defect, not depth.

### 5.2 Structural kinds

These must be stored, because each carries structure that cannot be reconstructed from the
dimensions.

| Kind | Directional? | What it adds beyond dimensions | Mechanism it must feed |
|---|---|---|---|
| `family` | Symmetric role, asymmetric obligation | Household membership, inheritance, kin obligation independent of affection | Household co-location and shared economic exposure ([`./POPULATION-FIDELITY.md`](./POPULATION-FIDELITY.md)); hostage/casualty reaction magnitude |
| `friend` | Directional (A may consider B a friend and not vice versa) | Informal contact channel outside institutional routes | ⚠ Flagged — the named mechanism is **the same mechanism named for `familiarity` (D8)**. See §13.3 and OQ-6 |
| `rival` | Directional | Active competition for a specific contested position or resource | Blocking-action availability; coalition exclusion |
| `mentor` / `protégé` | Strictly directional pair | Transmission of judgement and career dependency | Succession and replacement modelling. ⚠ The advice-weighting uplift originally named here duplicates D2 — see §13.3 and OQ-6 |
| `employer` / `employee` | Strictly directional pair | Formal authority, compensation, and a chain of command | Instruction compliance; organisational membership ([`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md)) |
| `political_patron` / `client` | Strictly directional pair | Sponsorship of position, contingent on continued loyalty | Position stability; defection cost; the charter's *Change institutional behaviour* primitive |
| `faction_alignment` | Strictly directional | The source's alignment with, and loyalty to, a faction it may or may not formally belong to. The target is a faction entity whose **definition, membership rules, formal positions and internal structure are owned by** [`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md) and are not specified here | Coalition formation (RG-M4); influence weighting (RG-M2); defection and recruitment (RG-M5). Specified in full at **§5.4** — assigned to this document by **founder ruling 1C, 19 July 2026** |
| `financial_dependency` | Strictly directional | Material flow that stops if the relationship stops | Economic exposure propagation; feeds D5 rather than duplicating it |
| `professional_contact` | Directional | Weak-tie access to another institution or sector | Cross-institutional information paths; the "elite foreign education → international professional network" chain in the source record (lines 256–262). ⚠ Flagged — the path mechanism is **the same mechanism named for D8**. See §13.3 and OQ-6 |
| `romantic_partner` | Symmetric role, asymmetric commitment | Household entanglement and a concealed-versus-public identity surface | ⚠ Flagged — see §13 and OQ-6 |

**One row in that table is an addition to the source record and is marked as such.**
`faction_alignment` is not among the thirteen relationship kinds the source record lists
([`./FOUNDER-REQUIREMENT-2026-07-18.md`](./FOUNDER-REQUIREMENT-2026-07-18.md) lines 73–75). It enters
this document by **founder ruling 1C of 19 July 2026**, which is a later founder instruction and
governs its own subject under the second carve-out stated in the header. Its nearest source-record
anchors are *political patrons* (line 74), *political involvement* (line 61), *loyalty* (line 65),
*internal factions* (line 99) and *parties and factions* (line 116) — none of which is a
person-to-faction relationship kind. The addition is labelled here for the same reason the fifth edge
view is labelled in §4.3: an addition presented as fidelity to the source record is a divergence, and
this document has made that error once already.

### 5.3 Derived predicates — must NOT be stored as kinds

The remaining four items in the source record's list must be specified as **queries over the graph**,
computed on read:

| Source record term | Specified as | Derivation |
|---|---|---|
| "trusted sources" | derived predicate | edges where `trust` ≥ scenario threshold **and** an information channel exists (`familiarity` above the contact floor) |
| "people they distrust" | derived predicate | edges where `trust` ≤ scenario threshold, optionally ranked by `resentment` |
| "people to whom they owe favours" | derived predicate | outstanding obligation records where the source is the debtor (§6.4) |
| "people who owe them favours" | derived predicate | outstanding obligation records where the source is the creditor (§6.4) |

**Rationale.** Storing "trusted source" as a flag alongside a `trust` score creates two facts that
can contradict each other and no rule for which wins. Deriving it guarantees the interface can never
show a trusted-source badge on an edge whose trust score does not support it.

**Specified invariant RG-6.** Kinds must be a set, not a single value. A person may simultaneously be
an entity's employer, rival and former mentor, and it is precisely that combination that generates
interesting behaviour. Any schema that forces one kind per edge must be rejected.

**The same derived-not-stored rule is applied a third time at rule RG-T11 (§6.4)**, to
[`./PERSON-MODEL.md`](./PERSON-MODEL.md)'s `relationships.obligation_ledger[]`. The two entries above
for favours owed and favours owed-to are the person-side face of that ledger, and RG-T11 states in
full what this table states in outline: the ledger is a projection over `OpenThread` records, not a
second store.

### 5.4 `faction_alignment` — the person-to-faction edge

**Assigned to this document by founder ruling 1C, 19 July 2026.** The ruling splits what
[`./PERSON-MODEL.md`](./PERSON-MODEL.md) registers as **M14 FACTION-ALIGNMENT** three ways, and it
must not be duplicated:

| Half | Owner | What it covers |
|---|---|---|
| Faction definitions, membership rules, formal positions, faction structure | [`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md) | Specified there as `M-FAC` (§7.4), with the bloc record at its §8.2 |
| The **directional, historied alignment and loyalty relationship**, and its changing strength | **This document** | This section, specified as an edge kind on the model of §4 |
| Consumption of the resulting projection | [`./PERSON-MODEL.md`](./PERSON-MODEL.md) | Reads the projection; owns neither half |

**This document specifies no faction structure.** It does not define what a faction is, who belongs to
one, what offices it holds or how it is internally organised. Every such question resolves against
[`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md), and a reader finding faction structure specified
here has found a defect.

**Plain-English layer.** A person's relationship to a faction is a relationship, not an attribute of
the person. It runs one way: a junior official may be fiercely loyal to a faction that has never
heard of them, and a faction
may count someone as its own who privately despises it. It has a history: loyalty earned over twenty
years and loyalty bought last month are not the same thing, and the difference is exactly what
predicts who defects under pressure. And it can hold unfinished business — a promotion promised and
never delivered is the kind of open item that turns a loyalist into a leak.

Storing this as a number on the person would lose all three properties. That is why the ruling put it
here.

**Specified rule RG-F1 — a faction alignment is an ordinary directed edge, not a special case.** A
`faction_alignment` edge is a `RelationshipEdge` (§9) whose `kinds` set contains `faction_alignment`.
It carries the same nine dimensions (§4.2), the same five views (§4.3), the same event stream and
projection rule (RG-T1), the same open-thread ledger (§6.4), the same point-in-time query obligation
(RG-T9) and the same per-edge RNG substream requirement (RG-R1) as every other edge. No dimension,
view, invariant or update rule is added for it, and none is disapplied. **The specification of a new
edge kind must not become the specification of a second edge model.**

Consequently:

- `source_entity_id` is the aligning entity. `target_entity_id` is the faction entity, whose identity
  and identifier are [`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md)'s (`InternalBloc.bloc_id`
  at its §8.2, or a party or movement organisation record) resolved in the shared namespace
  [`./ENTITY-ONTOLOGY.md`](./ENTITY-ONTOLOGY.md) owns. **Whether a faction is an entity that may be an
  edge endpoint at all must be settled in that document, not here** — today `cohort_id`
  (`agent_schema.py:94`) and `agent_id` (`:161`) are separate namespaces and nothing binds them, and
  there is no faction, bloc, department or membership field anywhere in `agent_schema.py`.
- The reciprocal edge — the faction's stance toward the person — is a **separate edge** under
  invariant RG-1, created, updated and dissolved independently. A faction that trusts a member who
  does not trust it back is the ordinary case, not an exception, and it is the configuration in which
  infiltration and disillusionment live.
- Alignment strength is **not a new scalar.** It is read off the existing dimensions: `dependency`
  (D5) for what the person stands to lose by leaving, `ideological_alignment` (D6) for agreement with
  the faction's positions, `respect` (D2) for the faction's judgement, `fear` (D4) for what it can do
  to defectors, and `resentment` (D7) for accumulated grievance against it. Adding an
  `alignment_strength` field would be a stored summary of dimensions that already exist, which is the
  two-sources-of-truth shape §13.1 struck `shared_history` for.

**Specified rule RG-F2 — loyalty is not agreement, and the pair must remain separable.** `dependency`
(D5) and `ideological_alignment` (D6) must be able to move in opposite directions on the same edge. A
person who has stopped agreeing with a faction but cannot afford to leave it, and a person who agrees
completely but owes it nothing, are different actors with different failure modes, and collapsing the
pair into one loyalty number makes both inexpressible. This is the discriminating structure that keeps
`faction_alignment` out of §13.3: it is not a duplicate of D6, because D6 is one of its inputs rather
than its equivalent.

**Specified rule RG-F3 — alignment must be historied, and its history is the same event stream.**
`faction_alignment` edges are projections of `RelationshipEvent` records under rule RG-T1. The events
that matter for this kind are the ordinary ones already enumerated in §9 —
`obligation_incurred` and `obligation_discharged` for patronage, `betrayal` for a promise broken,
`coercion_applied` for discipline, `kind_added` and `kind_removed` for joining and leaving. **Joining
and leaving a faction are events on this edge; formal membership is a fact owned by
[`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md).** The two are not the same thing and must not be
conflated: a person may remain formally a member long after the alignment edge has collapsed, and that
gap is a mechanism, not an inconsistency.

**Specified rule RG-F4 — the mechanisms are the existing ones.** `faction_alignment` earns its place
under RG-2 category (a) by feeding mechanisms this document already specifies, not by acquiring its
own: coalition formation (RG-M4, where faction alignment bounds which coalitions are candidates),
influence weighting (RG-M2, where an entity's factional ties weight the pressure it transmits and
receives), and recruitment (RG-M5, where turning an entity means turning it away from an alignment it
already holds). No new mechanism is introduced here, and none may be introduced without satisfying
RG-2.

**Specified rule RG-F5 — tier treatment follows §8 unchanged.** Individual `faction_alignment` edges
exist at Tiers 1 and 2. At Tier 3 they exist only for named representatives. At Tier 4 there are no
individual edges: a cohort's alignment to a faction is a directed aggregate channel with a strength
distribution, population-weighted per RG-S3, exactly as rule RG-S1 requires for every cross-tier edge.
The tier definitions remain [`./POPULATION-FIDELITY.md`](./POPULATION-FIDELITY.md)'s and are not
restated here.

**What this document does not decide.**
[`./PERSON-MODEL.md`](./PERSON-MODEL.md) records that one clause of the superseded M14 definition —
**per-person dissent and defection probability** — is not unambiguously placed by ruling 1C, since it
is a probability attached to a person, computed from an alignment edge, against an organisational
position, and therefore plausibly belongs to any of the three documents the ruling names. That
document raises it as its own open question and states that until it is placed, no document should
assume it holds it. **This document makes no claim to it.** RG-M4's defection rule (§7.4) reads the
alignment edge; it does not thereby own the person-side probability. Recorded here as **OQ-17**.

---

## 6. The temporal model — the hard part

### 6.1 Plain-English layer

This is the section that justifies a separate document.

The naive design stores a current number for each dimension and updates it when something happens.
That design can answer "does A trust B *now*". It cannot answer any of the questions the source
record actually requires:

- *How did these two individuals come to distrust one another?* (source record, line 189)
- *Did A trust B at tick 40, when A ignored B's warning?*
- *What is still unresolved between them?*
- *Which prior experience shaped this reaction?* (line 291)

The specified design therefore treats the relationship graph as a **projection of an event log**,
not as a set of stored numbers that happen to have a history attached. The numbers are a cache. The
events are the truth.

### 6.2 Edges are projections, not primary state

**Specified rule RG-T1.** The authoritative record of a relationship is the ordered set of
`RelationshipEvent` records that reference it. The scored dimensions in §4.2 are a **materialised
projection** of that set at a given tick. The projection must be reproducible: replaying the events
from scenario initialisation must reconstruct the identical dimension values, bit for bit, with no
model calls and no network calls.

**This applies to the "authoritative edge" of §4.3 as well, and the naming must not obscure it.** The
authoritative edge is the **authoritative projection** — the unfiltered one — not primary state. All
five views in §4.3 are projections of this one stream, differing in which subset of it they are
computed from and what distortion is applied. There is exactly one authoritative record in the
relationship layer and it is the event stream. Consequences: a snapshot that captures edge dimensions
without the events that produced them captures a cache, not state; and two runs compared for
reproducibility must be compared on the stream, or on a projection derived from it by a stated rule,
never on stored dimension values alone (OQ-2).

This is a direct application of P0.6 ("Repair event, snapshot and replay foundations. Central
transition mechanism, full snapshots, replay makes zero model/network calls",
[`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.6 (`:87-88`)), and it is why the temporal graph is **unbuildable**
until P0.6 lands. Stated concretely, all three parts of P0.6 are prerequisites and none exists:

| P0.6 part | Current state | Why the temporal graph needs it |
|---|---|---|
| Central transition mechanism | None. `engine.py:165-173` appends raw unvalidated dicts; `Event` (`agent_schema.py:211-229`) is never instantiated (audit §6.13) | Without one, edge updates would be written by whatever code happened to touch them, exactly as `cohort_agent.py:38` writes `government_competence` in place today |
| Complete event emission | Events are emitted only when a delta is non-empty (`engine.py:163`), so no-ops, rejections, cohort drift and every diffusion step produce no record at all (audit §6.14) | A relationship's history must include the interactions that changed nothing. "They met and nothing was resolved" is a fact about the relationship |
| Realised-effect recording | Logged effects are the *requested* delta, not the realised one — summed `military_readiness` effects imply 1.59 against an actual 1.0 over 120 ticks at seed 88213 (audit §6.15) | A projection built from requested deltas would diverge from the stored dimensions and produce two disagreeing histories |
| Full snapshots | No RNG state is captured anywhere (audit §5.14); no random draw is ever recorded | Point-in-time reconstruction of a stochastically-updated edge is impossible without them |
| Persistence | Nothing is written to any table; runs live in a process-local dict (`runs.py:18`), and `StateSnapshot.meso_state` (`scaffold/backend/app/db/models.py:51`) is declared with `default=dict` and written by nothing (audit §5.14) | The graph cannot outlive a process |

**There is a further prerequisite the audit records separately.** The existing event log is
client-forgeable: `routes_simulation.py:81` binds the entire `Intervention` model from the request
body and `:91-100` writes `model_dump()` verbatim into `model.event_log`, so a client can assert its
own `legal_check` and mint colliding event ids through the interpolated `action_id` at `:93`
(audit §5.11; A3 check 5, `docs/delivery/A3-VERIFICATION-RESULTS.md:120-140`, driven through the real
API). An entity history built on that log would inherit forgeable provenance. Splitting the wire
model from the state model is a precondition, and the audit sequences it after P0.6.

### 6.3 The dual representation and its consistency rule

Rebuilding every edge from the full event log on every read is not affordable at graph scale
(§8). The specification therefore requires two representations with a strict relationship between
them:

| Representation | Contents | Role |
|---|---|---|
| **Event stream** | Append-only `RelationshipEvent` records | **The single authoritative record** (rule RG-T1, §4.3). Never mutated, never deleted. |
| **Current projection** | Materialised dimension values per edge at the current tick — the *authoritative projection* of §4.3, and the four filtered views alongside it | Cache. Rebuildable from the stream at any time. **Not primary state**, notwithstanding the name "authoritative edge". |
| **Checkpoint projections** | Materialised dimension values at snapshot ticks | Performance aid for point-in-time queries. Rebuildable. |

**Specified invariant RG-T2.** A consistency test must exist that, for a given seed and scenario,
rebuilds every edge projection from the event stream and asserts equality with the stored projection
at every snapshot tick. If this test cannot be written, the dual representation must not be built.
MERIDIAN currently has no invariant tests of any kind (audit §6.34), and this is the first one the
relationship layer requires.

**Specified invariant RG-T3.** Edge projections must never be mutated in place by subsystem code.
The existing counter-example is `cohort_agent.py:35-38`, which writes `b.government_competence`
directly on a live Pydantic object with no event emitted, no cause recorded and no possibility of
recovery. Every edge change must be expressed as an emitted event that the projection then consumes.

### 6.4 Unresolved events — the obligation and grievance ledger

This is the mechanism the source record names as "important unresolved events" (line 80), and it is
the one that makes history *matter* rather than merely exist.

**Specified structure.** An `OpenThread` is a record attached to a directed edge representing
business between two entities that has not been closed. It must carry:

| Field | Purpose |
|---|---|
| `thread_id` | Stable identifier |
| `edge_ref` | The directed edge it belongs to (creditor's edge; the debtor's edge carries the mirror reference) |
| `thread_kind` | `favour_owed`, `debt`, `unpunished_betrayal`, `unacknowledged_harm`, `unfulfilled_promise`, `unreturned_information`, `contested_claim` |
| `originating_event_id` | The `RelationshipEvent` that opened it — the provenance link |
| `opened_tick` | When |
| `magnitude` | How large the outstanding item is, on a scenario-defined scale |
| `salience` | How present it currently is in the entity's reasoning — **decays; magnitude does not** |
| `resurfacing_conditions` | Structured trigger predicates (see below) |
| `resolution` | `null` while open; otherwise a closing event reference, a resolution kind and the closing tick |

**Specified rule RG-T4 — magnitude persists, salience decays.** A favour owed in year one is still
owed in year ten. What changes is how present it is. Modelling the whole thing as a single decaying
number would erase the source record's requirement that formative experiences persist, and it would
repeat the defect in the existing `AgentMemory` (`agent_schema.py:143-151`), which models memory as
`recent_events` plus a `decay_rate` and therefore cannot represent a formative experience at all.
Decay must apply to attention, never to obligation.

**Specified rule RG-T5 — resurfacing is condition-driven, not random.** An open thread must resurface
— its salience must be restored — when a structured condition is met. Conditions must be predicates
over recorded world state, not narrative triggers, so that the resurfacing is explainable under the
charter's eight questions. Specified condition classes:

| Condition class | Example |
|---|---|
| Counterparty state change | The debtor gains the capacity to repay; the creditor loses the position that made repayment unnecessary |
| Topical relevance | An event occurs whose type matches the thread's originating context |
| Third-party prompting | Another entity with a path to the creditor raises it |
| Decision adjacency | The creditor is about to take an action the debtor could assist or block |
| Scheduled maturity | A promise with a stated horizon reaches it |

**Specified rule RG-T6 — resurfacing changes behaviour or it does not exist.** A resurfaced thread
must produce at least one of: an increase in the probability that the creditor initiates contact; a
modifier on the debtor's compliance probability if approached; an unlocked coercive option gated on
`leverage` (D9); an increase in `resentment` (D7) if the thread ages past a scenario-defined
threshold without resolution. A resurfaced thread that only generates a line of prose is fake depth
and must be struck.

**Specified rule RG-T10 — the D7 / ledger precedence rule must be stated before either is built.**
RG-T6 has open threads writing into `resentment` (D7), and D7 is defined as "accumulated unaddressed
grievance toward the target". That is the same two-sources-of-truth shape this document rejects
elsewhere: §13.1 strikes `shared_history` on the ground that "storing it would create a value that can
disagree with the events it summarises, with no rule for which wins", and §13.2 strikes four kinds as
derived predicates on the same reasoning. **The derived-not-stored test was applied rigorously to
kinds and not at all to dimensions, and D7 is where that omission shows.**

Two dispositions are available and this document does not choose between them:

- **D7 as a derived predicate** over unresolved-thread magnitude, thread age and `trust` — consistent
  with the §5.3 treatment of "people they distrust", and eliminating the disagreement by construction.
- **D7 as stored state**, on the ground that it carries content the ledger cannot reconstruct.
  Grievance with no discrete originating event — accumulated slight, structural humiliation,
  resentment of a class of treatment rather than an act — is the candidate case, and it is a real one:
  the ledger records *threads*, and a thread requires an originating event id (§9, never null).

Whichever the owner takes, **the precedence rule must be stated explicitly**: when the stored D7 value
and the open-thread ledger imply different grievance levels, which governs behaviour, and what
reconciles them. A specification that leaves this unstated ships the defect it struck `shared_history`
to avoid. Recorded as **OQ-15**, and D7 is moved out of §13.5 into §13.3 accordingly.

**Specified rule RG-T11 — the obligation ledger is owned here, and PERSON-MODEL's is a projection of
it.** *(Added 19 July 2026, applying the coherence finding the ownership pass returned as unambiguous.)*

[`./PERSON-MODEL.md`](./PERSON-MODEL.md) specifies `relationships.obligation_ledger[]` as a list of
`{counterpart_ref, direction, magnitude, origin_event_ref, expiry, discharged}` entries, required to
be **callable, expiring and discharge-tracked**. That is the same content as the `OpenThread` records
above, held per person instead of per edge. Two stores of the same facts is the two-sources-of-truth
shape this document strikes elsewhere — §13.1 struck `shared_history` on exactly that ground, and
§5.3 struck four kinds on it — and the same treatment applies here.

**Specified: `relationships.obligation_ledger[]` is a derived projection, not stored state.** It is a
query over this document's `OpenThread` records, filtered to the three obligation-side thread kinds,
scoped to one person as creditor or debtor. It must not be stored separately in the person record.
This document is the **owner** of the underlying records; `PERSON-MODEL.md` is a **consumer** of the
projection. That is the same disposition `PERSON-MODEL.md` already takes for
`relationships.trusted_sources[]` ("must not be stored separately; a derived projection; storing it
independently would drift from the graph") and that this document already takes for `shared_history`,
so the resolution is a consistent application of an existing precedent rather than a new rule.

The crosswalk, field by field:

| `obligation_ledger[]` field | Projected from | Note |
|---|---|---|
| `counterpart_ref` | The other endpoint of `edge_ref` — the debtor where the person is creditor, the creditor where the person is debtor | Direction is carried by the edge, per invariant RG-1 |
| `direction` | Whether the person is the `edge_ref` source (creditor) or holds the mirror reference (debtor) | Not a stored flag; read off the edge |
| `magnitude` | `OpenThread.magnitude` | Persists and does not decay (rule RG-T4). `salience` has **no** counterpart in the person-side ledger and must not be projected into one — it is attention, not obligation |
| `origin_event_ref` | `OpenThread.originating_event_id` | Required, never null (§9). Matches `PERSON-MODEL.md`'s own rule that every `obligation_ledger` append carries its originating event |
| `expiry` | A `scheduled maturity` entry in `resurfacing_conditions` (rule RG-T5) plus a `lapsed` resolution kind | See the reservation below |
| `discharged` | `OpenThread.resolution is not null` | A boolean read of the resolution record, not a separately maintained flag |

**Which thread kinds project.** Only `favour_owed`, `debt` and `unfulfilled_promise` are obligation
threads and appear in this projection. The remaining four — `unpunished_betrayal`,
`unacknowledged_harm`, `unreturned_information` and `contested_claim` — are grievance-side, and they
feed `resentment` (D7) through rule RG-T6 rather than the obligation ledger. **Whether D7 is itself
derived from those four is not settled here and remains OQ-15**; RG-T11 settles the obligation half
only, and the two halves must not be assumed to resolve together.

**Two reservations, stated rather than assumed away.**

- **`expiry` has no direct `OpenThread` field.** The mapping above expresses it as a resurfacing
  condition plus a resolution kind, which is consistent with rules RG-T4 and RG-T5 and adds no state.
  If the owner prefers an explicit `expires_tick` field on `OpenThread`, it must satisfy RG-2 like any
  other field — a named mechanism must read it — and the candidate mechanism is the same one the
  condition-plus-resolution form already serves. This document specifies the derived form and does not
  treat the alternative as closed.
- **`PERSON-MODEL.md` classes the ledger as accreting, append-only state.** That classification is
  correct and is preserved: the append-only record is the `RelationshipEvent` stream and the
  `OpenThread` records it opens, which are never mutated and never deleted (rule RG-T1, §6.3). What is
  derived is the person-scoped *view* of them. Append-only and derived are not in tension here; the
  ledger accretes because the stream underneath it does.

### 6.5 Consolidation — how history compresses without being lost

An entity that has interacted with two hundred counterparts for four hundred ticks will accumulate an
unbounded event stream. The specification must bound growth without destroying the property that
makes the graph worth having.

**Specified rule RG-T7 — three retention classes.**

| Class | Retention | Rationale |
|---|---|---|
| **Formative** | Never compressed, never decayed out | Events flagged as identity-shaping — the source record's "previous crises they experienced" (line 62) and "which prior experiences shaped the reaction" (line 291). These must remain individually addressable forever |
| **Consequential** | Retained in full while any open thread references them, or while they lie between two checkpoints being compared | Ordinary interactions that changed a dimension materially |
| **Routine** | Compressible into periodic aggregate records after a scenario-defined horizon | Low-magnitude contacts whose only lasting effect is on `familiarity` |

**Specified invariant RG-T8.** Compression must be lossless with respect to the projection: replaying
compressed history must reproduce the same dimension values as replaying the uncompressed history,
within a declared tolerance of zero for dimensions and exactly for open threads. If that cannot be
guaranteed, routine events must not be compressed. Compression is an optimisation and must never be
allowed to change simulation results — the same standard the charter applies to reproducibility
generally ([`../../CHARTER.md`](../../CHARTER.md):58).

### 6.6 Point-in-time query

**Specified rule RG-T9.** Every graph read must accept an `as_of` tick and default to the current
tick. There must be no read path that can only return current state. A query that cannot be answered
historically must fail explicitly rather than silently return current values, because a silently
current answer to a historical question is worse than an error — it produces confident, wrong
after-action analysis.

Reconstruction is specified as: take the nearest checkpoint projection at or before `as_of`, then
apply the event stream forward to `as_of`. This requires checkpoints, which requires snapshots, which
is P0.6 again.

**Point-in-time queries must include the derived views.** "What did the player's role know about this
edge at tick 40?" is a different question from "what was true of this edge at tick 40?", and both must
be answerable. The intelligence view is itself event-sourced: each item of evidence the player's role
observed is an event, and the confidence label at a given tick is a projection of the evidence
available by that tick. This is what makes an *Outdated* label meaningful — it is the assertion that
the player's projection is stale relative to the authoritative edge.

---

## 7. Causal use — how edges must change behaviour

The source record's warning at lines 241–254 applies to this document more sharply than to any other:
a relationship graph is unusually easy to build as decoration. This section names the mechanisms.
Each is **specified, not implemented** — the mechanisms themselves must be built, and none exists.

### 7.1 Information flow

**Specified mechanism RG-M1.** The relationship graph must be the substrate over which claims
propagate between entities. Propagation must be gated in a fixed order:

1. **Reachability** — is there an edge with `familiarity` above the contact floor, or a shared
   institutional channel? No edge, no direct transmission. This is an **RG-3a** structural gate and
   may be absolute — **except where the reachable edge set is identity-correlated**, in which case
   RG-3c applies: the gate becomes a heavy penalty, and the residual-path guarantee must hold.
2. **Willingness** — will the source transmit? Modulated by `trust` (D1) for restricted information,
   suppressed by `fear` (D4) where the content is unwelcome to the target, and by the disclosure
   rules in [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md).
3. **Weighting** — how strongly does the receiver update? Scaled by the **receiver's** `trust` in the
   sender, not the sender's in the receiver. This asymmetry is the single clearest demonstration of
   why the graph must be directed: propagation and credibility run in opposite directions along the
   same tie.
4. **Distortion** — what arrives is not necessarily what was sent. Specified in
   [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md); this document specifies only
   that the edge must supply the distortion inputs (`ideological_alignment` for motivated
   reinterpretation, `familiarity` for shared context that reduces literal misunderstanding).

**Relationship to what exists.** The current diffusion model (`diffusion.py:40-79`) is a linear
threshold step over an undirected cohort graph whose adoption is documented as "monotonic
non-decreasing" (`diffusion.py:51`). It is the ancestor of RG-M1 and it is inadequate on three counts
simultaneously: undirected (`:24`), monotone (`:51`, `:77`), and disconnected from belief — the
output reaches only the API response (`routes_simulation.py:75`) and never touches `CohortBeliefs`
or macro state.

**The monotonicity constraint is load-bearing and must be stated.** Audit §5.9 establishes that
cohort belief is a one-way ratchet: `cohort_agent.py:35-38` only ever decreases
`government_competence`; no code path anywhere increases it; four of five demo cohorts reach 0.0 and
stay there at seed 88213 over 100 ticks. A relationship graph layered over a monotone belief model
would propagate collapse and nothing else. **RG-M1 is specified as valid only against a bidirectional
belief model**, and takes the audit's own Phase 4 exit criterion — "a counter-narrative action
measurably raises at least one cohort's belief"
(`docs/delivery/CURRENT-STATE-AUDIT.md` §9, line 485) — as a precondition on its own operation.

### 7.2 Influence

**Specified mechanism RG-M2.** Where an entity forms a decision, the inbound edges from other
entities must contribute weighted pressure. The weight of entity B's pressure on entity A must be a
function of A's edge toward B — `respect` (D2) for judgement-based pressure, `dependency` (D5) and
`fear` (D4) for coercive pressure, `affection` (D3) for personal pressure — and never of B's
self-assessed importance.

For organisations, this is the mechanism by which the source record's requirement that "an
organisation should not behave like one person" (line 104) is realised: the internal factions
specified in [`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md) are connected by intra-organisational
edges, and the organisation's action must emerge from the weighted resolution of those pressures.
The existing `InstitutionalAgent` (`scaffold/backend/app/simulation/agents/institutional_agent.py:18-41`)
produces exactly one proposal per role per tick from a three-key context stub (`:33-37`: `tick`,
`scenario_id`, `primary_target=None`), so it contradicts this at the behavioural level.

### 7.3 Obligation and leverage

**Specified mechanism RG-M3.** Open threads (§6.4) must appear in the action-availability layer.
Concretely: an action of the form "obtain compliance from B" must consult the source's `leverage`
(D9) toward B and any open threads where the source is creditor. Where neither supports the action, it
must become steeply improbable and heavily priced — not silently succeed. Per RG-3b this is a curve,
not a wall: leverage is a disposition, and a disposition rendered as a hard availability gate is a
stereotype switch wearing a threshold.

This connects directly to the charter's causal vocabulary
([`../../CHARTER.md`](../../CHARTER.md):93-111): *Create an obligation* (Legal), *Alter a
relationship* (Relational) and *Enable or remove future options* (Optionality) are three primitives
that currently have no state to act upon. The relationship graph is specified as the state those
three primitives read and write.

**Honest note on the current gate.** There is no action-availability layer to attach to. A3 check 5
proved the decision endpoint accepts any actor, any action and any cost, and trusts a client-supplied
`legal_check` (`docs/delivery/A3-VERIFICATION-RESULTS.md:120-140`). `_validate_and_price`
(`engine.py:121-130`) receives only the proposal and never the agent spec, so it could not consult a
relationship even if one existed.

### 7.4 Coalition formation

**Specified mechanism RG-M4.** Coalitions must be **derived from the graph at a point in time**, never
authored as scenario data. A candidate coalition is a set of entities with mutually positive
`ideological_alignment` (D6) above a threshold, low `resentment` (D7) between members, and no member
whose `dependency` (D5) on an outside party exceeds their dependency on the coalition.

Coalition stability must be recomputed each tick, and defection must be probabilistic, driven by
`resentment` (D7), a competing `dependency` (D5), or a resurfaced open thread (§6.4). The observable
consequence — the reason this mechanism earns its cost — is that alliances must be able to collapse
for reasons recorded in history rather than by author fiat, and the collapse must be explainable
backwards under the charter's eight questions.

### 7.5 Gating what an entity can learn or do

**Specified mechanism RG-M5.** The graph must bound the action and knowledge space, not merely tint
it:

| Gate | Rule | RG-3 classification |
|---|---|---|
| **Knowledge** | An entity must not acquire information for which no path exists from a holder, through edges with sufficient `familiarity` and `trust`, within the elapsed time | **RG-3a** structural (path existence) — but **subject to RG-3c**: where the gating edge set is identity-correlated, this must be specified as heavily penalised, not absolute, and the residual-path guarantee applies |
| **Reach** | An entity must not act upon a target it has no edge to and no institutional route toward | **RG-3a** structural — **subject to RG-3c** on the same terms |
| **Authority** | The *existence* of an `employer`/`political_patron` kind is a structural precondition for chain-of-command instruction. Whether the instruction is **obeyed** must be a probability driven by `fear` (D4), `dependency` (D5), `respect` (D2) and `leverage` (D9). Position title alone must not be sufficient, and kind-membership alone must not compel | **RG-3a** for existence; **RG-3b** for compliance. An earlier draft ran the two together, which made categorical kind-membership determine behaviour |
| **Recruitment** | Turning an entity requires a path (RG-3a), and is then a probability steeply shaped by the trust gradient, `leverage` (D9) and any open thread — not a hard gate on leverage, and not a die roll against a global difficulty number | **RG-3a** for the path; **RG-3b** for the outcome |

**Specified invariant RG-7.** Every gate above must be *explainable*: when an action is unavailable,
the system must be able to state which edge, which dimension and which threshold produced the
refusal, in structured form. This is the charter's eight-question standard
([`../../CHARTER.md`](../../CHARTER.md):118-133) applied to relationship-mediated refusals, and it
maps onto the existing `Outcome.explanation_trace` field (`agent_schema.py:363-365`, documented as
"Ordered causal steps (data, not LLM prose)"). That field is `list[str]` and is never constructed,
so it cannot answer "which rule applied" in machine-readable form; the relationship layer requires it
to become a structured record.

---

## 8. Graph scale and fidelity tiers

### 8.1 Plain-English layer

A society of four million people has an unrepresentable number of possible relationships. The graph
must not attempt individual edges everywhere. The source record's fidelity tiers (lines 217–232)
determine where individual edges are affordable and where the graph must hold aggregate structure
instead. This section states which tier carries what; the tier definitions themselves belong to
[`./POPULATION-FIDELITY.md`](./POPULATION-FIDELITY.md) and must not be restated or redefined here.

### 8.2 What each tier carries

| Tier (source record lines 217–228) | Edge representation | Rationale |
|---|---|---|
| **Tier 1 — focal individuals** | Full individual directed edges, all dimensions, full event history, open threads | These are the entities whose decisions the player interrogates. The dossier's relationship tab (source record line 176) is a Tier-1 surface |
| **Tier 2 — named secondary individuals** | Individual directed edges, full dimensions, **bounded** event history (formative plus recent-consequential), open threads retained | Substantial profiles at lower continuous cost |
| **Tier 3 — households and local networks** | Individual edges **only** for named representatives; the group's internal structure held as aggregate parameters (density, cohesion, leadership concentration) | The source record's "behaviour partly aggregated while retaining named representatives" (line 225) |
| **Tier 4 — population cohorts** | **No individual edges.** Directed cohort-to-cohort channels with a strength distribution, plus directed channels to institutions and to Tier 1/2 individuals | Individual edges at this tier are neither affordable nor meaningful |

**Specified rule RG-S1 — cross-tier edges are directed and asymmetric by nature.** An edge from a
Tier-1 individual to a Tier-4 cohort ("this activist is trusted by the fishing communities") and its
reciprocal are fundamentally different objects: one is a person's stance toward a population, the
other a population's aggregate stance toward a person, with a distribution rather than a scalar. The
schema must not force them into the same shape.

**Specified rule RG-S2 — promotion must preserve edges.** When an entity is promoted between tiers
(source record lines 230–237), its existing edges must be preserved and expanded, never regenerated.
A Tier-4 background person promoted to Tier 1 after recording a viral video must retain the
relationships implied by their cohort membership; expansion adds specificity, it must not replace
history. This is the graph-layer statement of the source record's rule that "once materialised, their
identity and history must remain stable" (line 236).

**Specified rule RG-S3 — aggregate channels must be population-weighted.** A Tier-4 channel's
influence must scale with the population behind it. This is the design successor to P0.5
([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.5 (`:84-86`), "`represents_population` must affect aggregation") and
to audit finding §5.10, and is specified in detail in
[`./POPULATION-FIDELITY.md`](./POPULATION-FIDELITY.md). **This document takes P0.5's aggregation
channel as given and must not redesign or restate it.**

Two facts must be carried forward without being re-litigated here:

- The current graph ignores population entirely. `diffusion.py:35` weights edges by mean
  `internal_cohesion` alone, and `engine.py:142` builds the susceptibility map with no population
  term. A cohort of 14,200 (`kestral-strait.json:79`) therefore carries identical weight to one of
  620,000 (`:39`).
- Population weight must be **one term among several**, not the aggregation rule itself. The source
  record requires that "a small group may have disproportionate influence through wealth,
  organisation, strategic position or political access" (lines 137–139). None of those four has any
  field in any schema at cohort or agent level. A literal, minimal reading of P0.5 as pure
  proportional weighting would have to be unpicked later. This tension is recorded as OQ-4 and is
  flagged for the owner because **P0.5 is in flight and this document is not**.

### 8.3 Complexity bounds

**Specified rule RG-S4.** The specification must declare per-tier edge budgets before implementation,
not discover them afterwards. Individual-edge count is the dominant cost, and it grows with the square
of the individually-modelled population if unbounded. Bounds must be enforced structurally — an
entity's edge set must be capped and the cap must be a scenario parameter — rather than left to
authoring discipline.

**Specified rule RG-S5.** Graph traversal in any per-tick mechanism must be bounded in depth. Player
queries may traverse further, because they run on demand; per-tick mechanisms must not, because they
run always.

---

## 9. Schema sketch

**This is a sketch for review, not code to be added.** It must not be written into `scaffold/`.
Field names, ranges and shapes are all subject to owner review. Pydantic-flavoured syntax is used
only because the existing schema layer is Pydantic v2 (`agent_schema.py:16`).

Note the cost this incurs, which no generator currently absorbs: the project maintains nine
hand-written JSON Schema mirrors under `scaffold/schemas/` plus SQLAlchemy models in
`scaffold/backend/app/db/models.py`, with **no generator and no sync test** (audit §5.13). Every
structure below would need three hand-maintained copies under the present arrangement. That cost is
noted, not assumed away — see OQ-8.

**Every field below is annotated `(a)` or `(b)` for the RG-2 category it satisfies** — `(a)`
mechanism-backed, `(b)` required by a named charter question. A field carrying neither annotation is
a specification defect. §13's rejection list must be auditable against these annotations, not against
the §4.2 dimension table alone.

```python
# SPECIFICATION SKETCH — NOT IMPLEMENTED. Do not add to scaffold/.

class EdgeDimensions(BaseModel):
    """Source's orientation toward target. Every field is directional (invariant RG-1).
    Every field is RG-2 category (a); the reading mechanism is named inline and in §4.2.
    Every field is dispositional and therefore governed by RG-3b: modulation only, no
    outright outcome selection.

    This is a PROJECTION of the edge's event stream, not primary state (rule RG-T1).
    """
    trust: float                  # 0..1   D1 -> source credibility weighting, disclosure gate
    respect: float                # 0..1   D2 -> advice weighting in decision formation
    affection: float              # 0..1   D3 -> cost tolerance, loss reaction  [collinearity risk]
    fear: float                   # 0..1   D4 -> compliance probability, upward-reporting suppression
    dependency: float             # 0..1   D5 -> defection cost, constraint on opposition
    ideological_alignment: float  # -1..1  D6 -> coalition affinity, narrative resonance
    resentment: float             # 0..1   D7 -> defection / leak / retaliation probability
    familiarity: float            # 0..1   D8 -> contact reachability, channel availability
    leverage: float               # 0..1   D9 -> coercive action availability


class ConfidenceLabel(str, Enum):
    """Per-DIMENSION evidential confidence (invariant RG-4).

    Distinct axis from observability (invariant RG-5); the existing EventVisibility
    (agent_schema.py:203-208) answers WHO MAY OBSERVE and must not be overloaded.
    """
    confirmed = "confirmed"
    reported = "reported"
    assessed = "assessed"
    disputed = "disputed"
    unknown = "unknown"
    possibly_deceptive = "possibly_deceptive"
    outdated = "outdated"
    restricted = "restricted"


class OpenThread(BaseModel):
    """Unresolved business on a directed edge. Magnitude persists; salience decays (rule RG-T4).

    Note rule RG-T10: the precedence between this ledger and resentment (D7) is UNRESOLVED
    and is open question OQ-15.

    Rule RG-T11: PERSON-MODEL.md's relationships.obligation_ledger[] is a DERIVED PROJECTION
    over these records, filtered to favour_owed | debt | unfulfilled_promise and scoped to one
    person. It is not separately stored state. This document owns the records; PERSON-MODEL
    consumes the projection. Crosswalk at §6.4.
    """
    thread_id: str                # (a)
    thread_kind: str              # (a) favour_owed | debt | unpunished_betrayal
                                  # | unacknowledged_harm | unfulfilled_promise
                                  # | unreturned_information | contested_claim
    originating_event_id: str     # (b) charter Q3 — provenance; required, never null
    opened_tick: int              # (a)
    magnitude: float              # (a) 0..1 — DOES NOT DECAY
    salience: float               # (a) 0..1 — decays; restored by resurfacing (rule RG-T5)
    resurfacing_conditions: list[dict]   # (a) structured predicates over world state, never prose
    resolution: Optional[dict] = None    # (a) {closing_event_id, resolution_kind, closed_tick}


class RelationshipEdge(BaseModel):
    """A DIRECTED relationship. Replaces Relationship (agent_schema.py:190-200), which is
    declared-but-unused and can therefore be replaced at zero call-site cost.

    There is no undirected edge in this model. A mutual relationship is two edges that may
    be created, updated, decayed and destroyed independently.
    """
    edge_id: str
    source_entity_id: str         # whose view this is — never optional
    target_entity_id: str         # may be a FACTION entity where kinds contains faction_alignment
                                  # (§5.4, rule RG-F1). The faction's identity and structure are
                                  # ORGANISATION-MODEL's; whether a faction may be an edge endpoint
                                  # at all is ENTITY-ONTOLOGY's to settle. No faction structure
                                  # is specified in this document.
    kinds: set[str]               # structural kinds only (invariant RG-6); derived predicates
                                  # such as "trusted source" are computed, never stored (§5.3).
                                  # Includes faction_alignment (§5.4) — an ordinary kind on an
                                  # ordinary edge; no dimension or rule is added or disapplied
                                  # for it, and there is no alignment_strength field (RG-F1)
    dimensions: EdgeDimensions
    open_threads: list[OpenThread]
    # first_contact_tick: STRUCK. Introduced by an earlier draft, not in the source record's
    #   twelve items, and read by no mechanism anywhere in this document. RG-2 admits no third
    #   category, so it is struck rather than deferred (§13.1). Relationship age as a resistance
    #   term on familiarity decay would be a candidate mechanism, but no such mechanism is
    #   specified, and inventing one to save a field is the failure this document exists to avoid.
    last_interaction_tick: Optional[int]   # (a) decay clock + staleness of the source's model
    projection_as_of_tick: int    # (a) the tick this projection is valid for — mandatory
    source_substream_id: str      # (a) named RNG substream for this edge (§11) — hard prerequisite


class RelationshipEventKind(str, Enum):
    edge_created = "edge_created"
    interaction = "interaction"           # includes interactions that changed nothing
    obligation_incurred = "obligation_incurred"
    obligation_discharged = "obligation_discharged"
    betrayal = "betrayal"
    reconciliation = "reconciliation"
    information_shared = "information_shared"
    information_withheld = "information_withheld"
    coercion_applied = "coercion_applied"
    kind_added = "kind_added"
    kind_removed = "kind_removed"
    edge_dissolved = "edge_dissolved"     # dissolution is an event; the history survives it


class RelationshipEvent(BaseModel):
    """AUTHORITATIVE record. The edge projection is derived from these (rule RG-T1).

    Must be emitted through the P0.6 central transition mechanism, which does not exist.
    Must extend, not parallel, the existing Event (agent_schema.py:211-229) — in particular
    causal_parents (:224), which is the declared explainability chain and is assigned nowhere.
    """
    event_id: str                       # (a)
    tick: int                           # (a)
    kind: RelationshipEventKind         # (a)
    edge_ref: str                       # (a) the DIRECTED edge affected
    reciprocal_edge_ref: Optional[str]  # (a) the other direction, where it was also affected
    causal_parents: list[str]           # (b) charter Q3 "what caused it" — inherited from Event:224
    evidence_observed: list[str]        # (b) charter Q4 "what evidence did the entity observe";
                                        #     source record line 290
    dimension_deltas: dict[str, float]  # (a) REALISED deltas, not requested (cf. audit 6.15)
    alternatives_considered: list[dict] # (b) charter Q7 "what alternative reactions were possible";
                                        #     source record line 291
    retention_class: str                # (a) formative | consequential | routine (rule RG-T7)
    visibility: EventVisibility         # (a) WHO MAY OBSERVE — orthogonal to confidence (RG-5)


# The observer-relative views are TWO types, not one. An earlier draft collapsed them, which let a
# mechanism justification written for the causal half be inherited by the presentational half —
# fake depth laundered through a shared schema. They have different RG-2 categories and different
# read permissions, and must not share a type.

class EntityHeldEdgeBelief(BaseModel):
    """What entity O believes about an edge. SIMULATION STATE, read by RG-M4 (coalition
    formation) and RG-M2 (influence weighting). RG-2 category (a).

    The gap between this and the authoritative projection is where betrayal, misjudged alliance
    and failed recruitment live (§4.3). A derived projection, not primary state (rule RG-T1).
    """
    holder_entity_id: str               # (a) the ENTITY holding the belief — never a player role
    edge_id: str                        # (a)
    believed_dimensions: dict[str, Optional[float]]        # (a) None where unmodelled
    belief_as_of_tick: int              # (a) staleness of the holder's model


class PlayerIntelligenceEdgeView(BaseModel):
    """What the player's ROLE has evidence for. An INTELLIGENCE PRODUCT, read by the dossier.
    RG-2 category (b): required by the source record's four-view model (lines 157-159) and by
    charter Q4 (evidence observed). Explicitly NOT justified by a behaviour-changing mechanism,
    and it must not be given one.

    HARD RULE: no simulation mechanism may read this type. A mechanism that reads it would let
    the PLAYER'S knowledge leak into WORLD behaviour, which is a different defect from fake
    depth and a worse one. If a mechanism needs an observer's belief, it needs
    EntityHeldEdgeBelief.
    """
    observer_role_id: str               # (b) the player role — resolves against nothing today
    edge_id: str                        # (b)
    observed_dimensions: dict[str, Optional[float]]        # (b) None where unobserved
    dimension_confidence: dict[str, ConfidenceLabel]       # (b) per dimension (invariant RG-4)
    supporting_evidence: dict[str, list[str]]              # (b) charter Q4; event ids per dimension
    contradictions: list[dict]                             # (b) charter Q4 — conflicting evidence,
                                                           #     surfaced at dossier tab 9
    view_as_of_tick: int                                   # (b) staleness -> the "outdated" label


class PublicEdgeView(BaseModel):
    """What is COMMONLY BELIEVED about a tie (§4.3; source record lines 154-155). A property of
    the world, not of an observer — the surface an influence campaign manufactures and attacks.

    RG-2 category (a): read by narrative resonance and by reputational cost in RG-M2/RG-M4.
    Whether this is a distinct type or a pseudo-observer instance is OQ-13.
    """
    edge_id: str                        # (a)
    publicly_believed_dimensions: dict[str, Optional[float]]  # (a) None where no public belief
    belief_prevalence: dict[str, float] # (a) how widely held, per dimension — feeds Q12
    originating_claims: list[str]       # (b) charter Q3 — the narrative/campaign event ids that
                                        #     produced the public belief, true or otherwise
    view_as_of_tick: int                # (a)
```

---

## 10. Query patterns the player-facing social graph requires

The dossier's relationship tab is item 4 of the ten specified in the source record (line 176); the
tab design itself belongs to
[`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md). This section
specifies only what the graph layer must be able to answer.

**Specified rule RG-Q1.** Every query below must accept an `as_of` tick (rule RG-T9) and an
`observer` (the role whose intelligence view applies). There must be no omniscient read path exposed
to the interface. An interface query returning authoritative edges rather than the observer's view
would turn the intelligence product back into the encyclopaedia the source record explicitly rejects
(line 165).

| # | Query | Shape | Source-record question it serves |
|---|---|---|---|
| Q1 | Ego network of entity E at depth *k*, as of tick *t*, as seen by observer *O* | Directed subgraph, edges labelled per-dimension with confidence | Tab 4, the interactive social graph (line 176) |
| Q2 | Who influences E? | Inbound edges to E ranked by the RG-M2 influence weight, decomposed by dimension | "Who influences this chief executive?" (line 187) |
| Q3 | Why does E hold position P? | Inbound edges plus open threads plus belief provenance, joined to the decision event | "Why does this minister oppose the operation?" (line 186) |
| Q4 | Edge timeline between A and B | Ordered `RelationshipEvent` stream for both directions, with the dimension trajectory | "How did these two individuals come to distrust one another?" (line 189) |
| Q5 | Which groups trust entity X? | Aggregate Tier-4 directed channels into X, population-weighted per RG-S3 | "Which communities trust this media outlet?" (line 188) |
| Q6 | Who benefits if event Z occurs? | Traversal over `financial_dependency` and `dependency` (D5), forward from Z's economic effects | "Who benefits financially if the strait closes?" (line 188) |
| Q7 | Open threads involving E | Creditor and debtor threads, filtered by salience, with resurfacing conditions | The obligation ledger (§6.4) |
| Q8 | Reachability: can E learn fact F, or reach entity T? | Path existence under the RG-M5 gates, returning the gating dimension when the answer is no | Gate explainability (invariant RG-7) |
| Q9 | Diff a view: what changed between tick *t1* and *t2*? | Dimension deltas plus the causal events between the two ticks | "What changed? When? What caused it?" (lines 289–291) |
| Q10 | Contradiction set for an edge | Where the observer's evidence conflicts, with per-source confidence | Tab 9, intelligence assessment (line 181) |
| Q11 | Trajectory of a dimension | Time series of one dimension on one edge, with the events that moved it | Tab 10, timeline (line 182) |
| Q12 | What is *publicly believed* about E's ties, and how widely? | Public edge views involving E, per dimension, with prevalence and the originating claims — **distinct from Q5**, which returns authoritative aggregate trust, not public belief about a tie | Tab 8, public perception — "sentiment by community, country or platform" (line 180) |
| Q13 | Faction alignment: which entities are aligned to faction F, and how strongly — and to which factions is E aligned? | Directed `faction_alignment` edges in either direction, decomposed by dimension (D5, D6, D2, D4, D7 per rule RG-F1), with open threads, at `as_of` and under observer *O*. Aggregate directed channels for Tier 4 per RG-F5 | **Not a source-record question.** Serves founder ruling 1C (19 July 2026): this is the projection [`./PERSON-MODEL.md`](./PERSON-MODEL.md) consumes and does not own (§5.4) |
| Q14 | Obligation ledger for person P | Open threads of kind `favour_owed`, `debt` and `unfulfilled_promise` where P is creditor or debtor, projected to the crosswalk in rule RG-T11 | The person-side ledger [`./PERSON-MODEL.md`](./PERSON-MODEL.md) consumes rather than stores (§6.4). Q7 is the edge-scoped form of the same read |

**Note on Q12.** An earlier draft of this document omitted the public view from §4.3, and the omission
propagated here: tab 8 had no view and no query, and Q5 was doing duty it cannot do. Q5 answers "which
groups actually trust X"; Q12 answers "what is commonly said about X's ties, whether or not it is
true". An influence campaign moves the second without touching the first, and a graph that cannot
express that difference cannot represent the thing the scenario is about.

**Specified rule RG-Q2 — no LLM in the query path.** Graph queries must return structured data. The
LLM may narrate the result. It must never author an edge, a dimension, an open thread or a confidence
label. This is the charter's determinism boundary
([`../../CHARTER.md`](../../CHARTER.md):37-44, ADR-006) applied to the relationship layer, and the
existing, working implementation of that boundary is `ActionProposal` (`agent_schema.py:374-393`),
the only type the LLM gateway may return (`scaffold/backend/app/simulation/llm_gateway.py:35`). Any
generated relationship narration must route through that same boundary.

**Specified rule RG-Q3 — presentation is not state.** Graph layout, clustering, node placement and
visual emphasis are presentation concerns with no causal role, and must be computed in the interface
layer. They must never be persisted as entity or edge state, because a stored layout attribute would
be exactly the kind of attribute that feeds no mechanism.

---

## 11. Determinism, RNG substreams and replay

**This section describes a hard prerequisite, and it is owned by P0.4A.** *(Corrected 19 July 2026;
an earlier draft said no Phase 0 item covered it.)* The founder decision of 18 July 2026 created
**P0.4A — establish a deterministic randomness architecture** between P0.4 and P0.5
(`../delivery/PHASE-0-REMEDIATION-PLAN.md` §P0.4A). Relationships are one of the founder's five
named isolation axes — a draw about the A→B tie must be separable from draws about A and about B —
so this document's requirements sit inside P0.4A rather than beside it. The mechanism (stateful
named substreams versus keyed / counter-based draws) is unchosen; "substream" below names the
problem, not the solution.

A3 §6 (`docs/delivery/A3-VERIFICATION-RESULTS.md:170-175`) records a defect that was not in the
original audit:

> There are no named RNG substreams. Adding or removing a single random draw in one subsystem
> silently changes every subsequent draw in every other subsystem.

It is demonstrated, not inferred. Adding a grievance to the one grievance-free cohort moved
`shipping_throughput_pct_of_baseline` from `0.6080711379477878` to `0.5973599412373322`
(`A3-VERIFICATION-RESULTS.md:161-163`), while changing cohort belief *values* by two orders of
magnitude changed macro by exactly nothing (`:151-153`, `:165`). The mechanism is visible in four
lines: `engine.py:83` creates the single generator (commented "the ONLY source of engine
randomness"); `cohort_agent.py:36` draws only if the cohort has grievances; `diffusion.py:75` draws
once per graph node; `engine.py:135` draws once per tick.

**Why this is fatal to the relationship graph specifically.** The graph is a per-node draw consumer
whose node count changes at runtime:

1. `diffusion.py:75` already draws **once per graph node**. Any mechanism that adds or removes a node
   or an edge changes the per-tick draw count and therefore shifts every subsequent draw in every
   other subsystem.
2. Edge formation, decay and dissolution are runtime events. Under the current design, forming one
   new relationship would perturb national macro indicators for reasons unconnected to any model.
3. Tier promotion (§8, rule RG-S2) must consume draws to materialise an entity and its edges. On a
   shared stream, **national indicators would move because the player looked at someone.**
4. Stable identity is impossible. The draws an entity or edge receives depend on its position in the
   global draw order, which depends on everything that happened before it. The same edge generated
   at a different tick, or after a branch, would receive different values.

**Specified prerequisite RG-R1.** Named per-entity and per-edge RNG substreams must exist before any
part of this specification is implemented. Substreams must be keyed on something stable — run seed,
entity or edge identity, and purpose — so that generation is independent of global draw order. The
sketch in §9 reserves `source_substream_id` for this.

**This conflicts with a recorded architecture decision.** Audit §6.28 notes the single shared stream
is not currently classed as a defect precisely because "the design is documented as one RNG in
ADR-007". Introducing substreams therefore requires superseding an ADR, and
[`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`) requires human approval for architecture decisions and
for "anything affecting determinism or authoritative state". This is squarely both. **No agent may
make this call.** It is recorded as OQ-1.

**A compounding hazard.** Audit §5.9 notes that `grievances` (`agent_schema.py:103-105`) is currently
the *gate* on a random draw (`cohort_agent.py:35`). Making grievances mutable — which the source
record's causal chain requires (lines 280–287) — converts the substream problem from a
scenario-authoring hazard into a per-tick runtime one. The relationship graph does the same thing at
larger scale. The two dependencies compound and must not be treated separately.

**Specified prerequisite RG-R2.** Replay must reconstruct every edge projection with zero model calls
and zero network calls, per P0.6. Where an edge's history includes an interaction whose content was
LLM-narrated, the narration must be excluded from the reproducible state and logged separately, as
`scaffold/CLAUDE.md` already requires for LLM text generally.

---

## 12. Dependencies and sequencing

**Nothing in this document may begin before Phase 0 completes.** This is disposition, not sequencing
advice. The ordering below exists so the specification can be written correctly, not so that it can
be started.

The prerequisites are not independent and resolve in a fixed order:

```text
Named RNG substreams (RG-R1)   ← sits under everything; in NO P0 item; conflicts with ADR-007
  └─> P0.4  authoritative-state contract     ← decides which of the four edge views is authoritative
        └─> P0.6  event / snapshot / replay  ← the temporal graph is UNBUILDABLE before this
              └─> wire-model / state-model split  ← the event log is client-forgeable until then
                    └─> RELATIONSHIP-GRAPH (this document)

P0.5  cross-tier causal channels  ──> POPULATION-FIDELITY ──> §8 tier rules (RG-S1..S5)
  (P0.5's own aggregation is only meaningful once the audit 5.9 belief ratchet is fixed;
   audit §9 Phase 4, line 480, sequences both in the same phase)

B5 / P0.8  dual-use  DECIDED 18 Jul 2026, NOT cleared: 8 controls, none built, no P0 item owns them
  └─> the decided envelope constrains the identity-adjacent detail this graph exposes (§13, OQ-7)
```

**Relative sequencing note.** Of the eight world-model documents, this one and
[`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md) are the least blocked *as specifications*,
because their attachment points (`Relationship` at `agent_schema.py:190-200`, `MicroAgent` at
`:154-184`) are declared-but-unused rather than declared-and-wrong: nothing has to be undone to
replace them. That is a statement about specification cost, not about readiness to build. The
*temporal* half of this document is among the most blocked of all, because it depends on the whole of
P0.6.

---

## 13. Attributes that failed the causal-value test

The source record names the failure mode this section exists to prevent: "There is a danger of
producing enormous biographies that never affect the simulation. That would be fake depth"
(lines 243–244). Audit §5.10 is the empirical case — an attribute nothing reads let a 63× data error
survive undetected — and there are no invariant tests to catch a repeat (audit §6.34).

Applying invariant RG-2 to the source record's own list produced the following results. **These are
findings for owner review, not decisions.** An AI agent may draft the rejection list; only the owner
may approve it (OQ-5).

### 13.1 Struck — restructured, because no mechanism could read the scalar form

| Item | Source | Finding | Specified replacement |
|---|---|---|---|
| **`shared_history`** | line 80 | As a scalar, no mechanism could be named that reads it which is not already served by `familiarity` (D8) or by the event stream itself. A number summarising a history is a *summary of the mechanism*, not a mechanism. Storing it would create a value that can disagree with the events it summarises, with no rule for which wins | Not a field. Specified as the **derived event set** for the edge (§6.2) — the provenance, queried, not a stored number |
| **`last_interaction` as the sole temporal content** | line 80; exists today at `agent_schema.py:198-200` | An `int` tick alone cannot answer any of the source record's six history questions (lines 289–292) | Retained as `last_interaction_tick` **only** as a decay clock and staleness marker (§9), with the substantive temporal model in the event stream and open threads |
| **`important unresolved events` as an edge attribute** | line 80 | Modelled as a field on the edge, it would decay with the edge projection and lose the property that makes it matter | Promoted to first-class `OpenThread` records with independent lifecycle: magnitude persists, salience decays (rule RG-T4) |
| **`first_contact_tick`** | **Not in the source record** — introduced by an earlier draft of this document | No mechanism anywhere in this document reads it. It was not justified in §4.2, carried no inline mechanism annotation, and appeared in no rejection list — while its neighbour `last_interaction_tick` was put through the test and retained on a named ground. Under RG-2 it satisfies neither category (a) nor (b). Audit §5.10 is the exact precedent: an attribute nothing reads produces no error when it is wrong | **Struck.** Removed from the §9 sketch. Relationship age as a resistance term on `familiarity` decay would be a candidate mechanism, but no such mechanism is specified anywhere, and specifying one in order to save a field is the fake-depth move in reverse. If the owner wants relationship age, it must return as a named mechanism first and a field second |

### 13.2 Struck — derived, not stored

Four of the source record's thirteen relationship kinds (lines 73–75) are predicates over other
state, not kinds: *trusted sources*, *people they distrust*, *people to whom they owe favours*,
*people who owe them favours*. Storing them would create a second source of truth that can contradict
the first. Specified as derived queries in §5.3. **No information is lost**; the interface can render
all four.

### 13.3 Flagged — mechanism named but weak, needs owner ruling

| Item | Concern | Recommendation for the owner |
|---|---|---|
| **`affection` (D3)** | A mechanism was named (cost tolerance on the other's behalf; loss reaction magnitude), but it is **collinear** with `trust` (D1) and `respect` (D2) in most configurations. Three near-identical dials produce the appearance of depth with the behaviour of one | Retain **only** if a discriminating test can be written: a scenario configuration where affection alone changes an outcome, holding trust and respect constant. If that test cannot be written, merge D3 into D1 and D2 |
| **`romantic_partner` kind** | The only mechanisms found are household entanglement (already covered by `family`) and exposure to coercion (already covered by `leverage`, D9). The residual distinct content is a concealed-versus-public identity surface, which is exactly the dual-use-adjacent territory flagged below | Either name a mechanism no other kind provides, or strike the kind. Do not retain it for narrative colour. Couples to OQ-6 |
| **`ideological_alignment` (D6)** | The mechanism is real but **entirely dependent** on a value dimension set that [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md) has not yet defined. Until it does, D6 has nothing to compare | Conditional retention. Do not specify a range or semantics until the belief model defines the value space |
| **`EntityHeldEdgeBelief`** | The mechanism is real (misjudged coalitions, betrayal surprise, failed recruitment — RG-M4, RG-M2) but the storage cost is *holders × edges* | Retain as specification, RG-2 category (a). Flag that a materialisation strategy — which held beliefs are stored versus computed on read — is an implementation decision that must be taken with the P0.4 contract in hand, not before |
| **`PlayerIntelligenceEdgeView`** | **No simulation mechanism reads it, and none may.** An earlier draft modelled it as one type with `EntityHeldEdgeBelief`, which let the coalition/betrayal justification written for the causal half be silently inherited by the presentational half. Split in §9. It is retained on RG-2 category (b) alone — the source record's four-view requirement (lines 157–159) and charter Q4 | Retain **only** as an intelligence product with the hard rule that no simulation mechanism reads it. Storage cost is *roles × edges*, and there is no auth or role layer to resolve "observer" against today (audit §7, IAM row), so it has no attachment point at all (§4.3). If the owner ever wants a mechanism to consult an observer's belief, it must consult `EntityHeldEdgeBelief` — routing world behaviour through the player's view is a worse defect than fake depth |
| **`friend` kind** | The mechanism named for it — "informal contact channel outside institutional routes" — is **the same mechanism named for `familiarity` (D8)**: contact reachability and channel availability. This is the identical collinearity ground on which `affection` was flagged, and the test was not applied here | Apply the same discriminating test: name a configuration where `friend` changes an outcome that D8 held constant does not, or strike the kind and let D8 carry it. Do not retain it because the word is familiar |
| **`professional_contact` kind** | Same defect: "cross-institutional information paths" is D8's mechanism with an institutional adjective. The weak-tie *structure* may well be irreducible — a weak tie into another sector is not the same object as a strong tie within one — but the document did not say so, and an unstated justification is not a justification | Either state the structure D8 provably cannot reconstruct (candidate: the tie's *destination sector* is what carries the value, not its strength), or strike |
| **`mentor` / `protégé` kind** | Two mechanisms were named. The first, "advice weighting (D2) uplift", is **a second dial on the mechanism D2 already owns** and is duplicative. The second, succession and replacement modelling, is genuinely irreducible: no dimension encodes who is positioned to inherit whose role | Recommend retaining the kind on **succession and replacement modelling as the sole mechanism**, and striking the advice-weighting uplift as duplicative of D2. Recorded for owner ruling rather than applied, because striking a stated mechanism is a design decision |
| **`resentment` (D7)** | Moved here from §13.5 by rule RG-T10. D7 is defined as accumulated grievance and is driven by ageing open threads — making it a stored summary of the thread ledger, which is the two-sources-of-truth shape §13.1 struck `shared_history` for and §13.2 struck four kinds for. The derived-not-stored test was applied to kinds and not to dimensions | Either specify D7 as a derived predicate over unresolved-thread magnitude, age and `trust`, or state the content the ledger cannot reconstruct (candidate: grievance with no discrete originating event, which no thread can hold since `originating_event_id` is never null). **Either way, state the precedence rule.** See OQ-15 |

### 13.4 Flagged — safety coupling, deliberately not resolved

The relationship graph is a **strict refinement of the audience-segmentation half** of the dual-use
pair the audit identifies at §5.12 (`docs/delivery/CURRENT-STATE-AUDIT.md:231`). Today, segmentation
operates over five aggregate cohorts (`InfluenceSusceptibility` at `agent_schema.py:72-77`,
`MediaExposure` at `:42-53`, `Demographics` at `:22-28`). This document specifies directed,
asymmetric, historied ties between named individuals, plus `leverage`, an obligation ledger, and
explicit recruitment and coercion gates (RG-M3, RG-M5).

**The dual-use surface this creates is strictly larger than the one the B5 controls were written
against.** `Campaign.target_cohorts` and `Campaign.existing_grievance` (`agent_schema.py:326-331`,
the latter documented as "Pre-existing grievance the campaign exploits") target exactly the
attributes this graph refines.

**B5 / P0.8 is DECIDED** (founder decision, 18 July 2026). An earlier draft of this section
described it as an open owner decision, citing `docs/delivery/A3-VERIFICATION-RESULTS.md:245`,
[`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.8 (`:90`) and audit §8 decision 6; **all three of those anchors
predate the decision and are superseded.** Two consequences for this graph, and they pull in
opposite directions:

- **The envelope now exists, so it constrains this document rather than being awaited by it.** The
  decision's not-permitted list and its control 5 — protected characteristics may never be
  optimisation criteria for persuasion or manipulation — bind the identity-adjacent attributes
  specified here. §13.4's design rule below is consistent with it and is not weakened by it.
- **B5 did not clear, and it did not become cheaper.** It now clears only when the eight controls
  are **implemented and verified**, none of which exists in code. So the coupling this section
  records is *not* discharged: this graph still enlarges a dual-use surface whose controls are
  entirely unbuilt.

**The decision is applied here, not reinterpreted or extended, and no agent may do either.** What
the decision does **not** settle is how coarse this graph's recruitment, coercion and leverage
mechanics should be held while the controls remain unbuilt — that remains OQ-7, restated below
against the decided position rather than against a pending one, and cross-referenced to
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md).

**Design rule carried forward from the source record (lines 303–316), applying to this graph.**
Sensitive identity may affect *networks* — who knows whom, who trusts whom, who has access — because
that is social structure. It must never affect an edge dimension as an inherent property of a group.
Concretely: shared identity may raise the **prior probability** that an edge exists and may modulate
`familiarity` (D8) through residential and institutional proximity; it must never set `trust`,
`respect` or `leverage` as a function of group membership alone. That would be the stereotype switch
invariant RG-3b forbids.

**That rule is satisfied literally and defeated compositionally, and stating it alone is not enough.**
The chain is set out at RG-3c: identity shifts the edge-existence prior → edge existence and
`familiarity` gate reachability → reachability bounds knowledge and reach absolutely. Each step obeys
the rule above; the composite makes group membership a structural determinant of what an entity can
ever learn or do. A per-attribute bias test cannot detect this, because no single attribute is wrong.

Enforcement therefore belongs to
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) as **two**
requirements, not one: a per-attribute bias test over generated graphs, **and** a compositional test
over reachable information and action sets (RG-3c guard 3). This document specifies both constraints
and neither test.

### 13.5 Retained without reservation

`trust` (D1), `respect` (D2), `fear` (D4), `dependency` (D5), `familiarity` (D8) and `leverage` (D9)
each map to at least one named mechanism that is not served by another dimension. `resentment` (D7)
was previously listed here and has been **moved to §13.3** under rule RG-T10.

Of the structural kinds in §5.2, the following are retained without reservation: `family`, `rival`,
`employer`/`employee`, `political_patron`/`client` and `financial_dependency`. Each carries structure
no dimension can reconstruct, and in each case that structure is stated in the §5.2 table rather than
asserted.

**`faction_alignment` is retained here, and the discriminating structure is stated rather than
assumed.** *(Added 19 July 2026 with the kind itself.)* The kind was assigned to this document by
founder ruling 1C, but a ruling on *ownership* is not a ruling on *causal value*, and the ruling did
not exempt the kind from RG-2 or from the §13.3 test. Applying that test: the collinearity candidate
is `ideological_alignment` (D6), and the kind is not a duplicate of it, because **D6 is an input to a
faction alignment rather than its equivalent** — rule RG-F2 requires that agreement (D6) and what is
at stake in leaving (D5) move independently on the same edge, and it is the divergence between them
that produces the loyalist who has stopped believing. The structure no dimension reconstructs is the
**target**: the counterpart is a corporate entity owned by
[`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md), and an edge to a faction is a different object
from the aggregate of a person's edges to its members. The kind adds no dimension, no view and no
mechanism of its own (RG-F1, RG-F4), so it incurs no fake-depth cost beyond a membership test on an
existing set field.

**Two caveats on that retention, which the owner should see rather than infer.** First, it is a
retention this document is making about a kind the founder ruling introduced, so if the test above is
judged not to hold, the remedy is an owner ruling and not a silent strike — the kind exists by
instruction. Second, `faction_alignment` inherits the standing caveat below in full: RG-M2, RG-M4 and
RG-M5 are specified and unimplemented, so "feeds three mechanisms" means "feeds three mechanisms this
specification requires to be built".

**Four kinds have been moved out of this list.** `romantic_partner`, `friend`, `professional_contact`
and `mentor`/`protégé` are all in §13.3 pending an owner ruling. An earlier draft retained the last
three here on the blanket assertion that they "each carry structure the dimensions cannot reconstruct"
without saying what that structure was in those three cases — while §13.3 demanded a discriminating
test of `affection` on identical collinearity grounds. **The causal-value test had been applied
unevenly, and the rejection list is the one artefact in this document the owner is asked to approve,
so uneven application is a defect in the deliverable itself.** The test is now applied uniformly: a
kind whose named mechanism duplicates a dimension's is flagged, whatever the kind is called.

**Standing caveat, stated once and applying to all of the above.** Every mechanism named in this
document is itself **specified and unimplemented**. "Maps to a mechanism" means "maps to a mechanism
this specification requires to be built", not "maps to a mechanism that exists". No mechanism named
here exists in MERIDIAN today.

---

## 14. Open questions for the owner

AI agents may draft records but may not approve decisions
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)). Each item below requires a human choice and none is
resolved in this document.

| # | Question | Why it must be the owner's |
|---|---|---|
| **OQ-1** | **Narrowed 19 July 2026.** Placement is decided: the founder decision of 18 July 2026 made deterministic randomness isolation a new Phase 0 item, **P0.4A**, between P0.4 and P0.5, and ruled out folding it into P0.6 or deferring it. What remains open is the **mechanism** — stateful named substreams (including the per-edge keying this document assumes) or keyed / counter-based deterministic draws, per `RAID-REGISTER.md` DEC8 and the drafted, unapproved [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md) — and whether the ADR supersedes or narrows ADR-007. Relationships are one of the founder's five named isolation axes, so this document's per-edge requirement is inside P0.4A's scope rather than additional to it. | Architecture and determinism; explicit human-approval requirement (HANDOFF:131-132). The temporal graph, tier promotion and stable identity are all unbuildable without it, and A3:170-175 establishes it as a latent hazard independent of any entity work |
| **OQ-2** | Does P0.4's authoritative-state contract admit an **event stream** as authoritative state, with **all** edge values — including the so-called "authoritative edge" — derived from it? And if so, what artefact is hashed when two runs are compared for reproducibility: the stream, or a projection derived from it by a stated rule? | P0.4's contract; it constrains snapshot shape and replay. **An earlier draft asked which of the four views is authoritative. That question presupposed its own answer and concealed the real one:** under rule RG-T1 no view is authoritative — the stream is, and every view including the unfiltered one is a projection. A ruling taken on the old wording would have settled the wrong question and constrained snapshots incorrectly. This document's position is stated in §4.3 and §6.2 but must not be assumed |
| **OQ-3** | Is `Relationship` (`agent_schema.py:190-200`) **replaced** by `RelationshipEdge`, and its published mirror `scaffold/schemas/relationship.schema.json` replaced with it — or is a new type added alongside? | Schema-governance decision affecting a published mirror. This document recommends replacement (nothing reads either) but does not decide |
| **OQ-4** | Should P0.5 be scoped now to anticipate multi-term influence weighting (wealth, organisation, strategic position, political access), or executed as pure population-proportional weighting? | **P0.5 is in flight and this document is not.** Its literal wording admits the narrower reading, and the source record requires the wider one (lines 137–139). If the narrow reading ships, POPULATION-FIDELITY will have to unpick it |
| **OQ-5** | Is the rejection rule adopted — any specified attribute satisfying **neither** RG-2 category (a) nor category (b) is **struck**, not deferred? And is the §13 rejection list approved as revised? | A specification-process decision, not a technical one. Audit §5.10 is the empirical case for the rule. Depends on OQ-16 |
| **OQ-6** | Applying the §13.3 discriminating test uniformly: which of `affection` (D3), `romantic_partner`, `friend`, `professional_contact` and `mentor`/`protégé` are retained, on what mechanism each, and is the advice-weighting uplift struck from `mentor` as duplicative of D2? | All five are causal-value judgements with a fake-depth risk and, for `romantic_partner`, a safety adjacency. **The first draft applied the test to two of them and retained the other three without stating their justification**, so the rejection list — the artefact the owner is being asked to approve — was internally inconsistent |
| **OQ-7** | **Restated 19 July 2026 — its trigger condition has been met.** The original question asked whether the recruitment, coercion and leverage mechanics (RG-M3, RG-M5) should be held deliberately coarse **until B5 / P0.8 is decided**. B5 was decided on 18 July 2026, so that wording no longer states a live question. What remains genuinely open, and is **not** answered by the decision: should those mechanics be held coarse until the eight controls are **implemented and verified**, given that the decision settled the policy but left every control unbuilt? | **B5 is decided; it is not cleared.** The eight controls exist as requirements and none exists in code, and this graph's dual-use surface is strictly larger than the one those controls were written against (§13.4). The decision constrains *what* may be specified (control 5; the not-permitted identity list) but says nothing about *how much operational detail* to specify before enforcement exists. **An agent must not settle this by reading the decision as permission.** **Not inconsistent with the sibling documents that record their equivalent question as spent** (ENTITY-ONTOLOGY §10.4, PERSON-MODEL §7, POPULATION-FIDELITY Q5, ENTITY-PROFILE-EXPERIENCE Q6): those defer *identity-attribute detail*, which the decision's permitted / not-permitted lists bound directly. RG-M3 and RG-M5 are recruitment and coercion mechanics — no clause of the decision bounds them, so nothing has replaced the deferral here. |
| **OQ-8** | Given nine hand-maintained JSON Schema mirrors and SQLAlchemy models with no generator and no sync test (audit §5.13), does an entity and relationship ontology of this size justify building the generator first? | Sequencing decision outside Phase 0 |
| **OQ-9** | Do the existing one-sided `bridges_to` declarations in `kestral-strait.json` (notably `:117` → `urban-nationalist-youth`, with no reciprocal at `:237`) become genuinely one-directional edges, or were they authoring omissions to be made reciprocal? And should the isolated 451,000-person highland cohort (`:121-122`, `bridges_to: []` at `:157`) remain isolated? | Every current edge must be re-authored with direction. These are scenario-content decisions with modelling consequences |
| **OQ-10** | Does the schema use one edge object carrying all dimensions, or a separate directed edge type per relationship dimension? | Determines whether `relationship.schema.json` is amended or replaced. This document sketches the single-object form (§9) but does not decide |
| **OQ-11** | What are the per-tier edge budgets and the maximum per-tick traversal depth (RG-S4, RG-S5)? | Performance envelope, and it constrains what the tier model in POPULATION-FIDELITY may promise |
| **OQ-12** | Should these eight world-model documents be written now against prerequisites that have not landed, accepting that none can be validated against an implementation? | The source record requires capture before the replacement architecture is designed (lines 340–341) while requiring no interruption to Phase 0. The trade should be confirmed explicitly |
| **OQ-13** | Is the **public view** of an edge (§4.3) a first-class stored projection, or a designated pseudo-observer instance of the observer-view type? | Storage-shape decision with real cost. This document's position is first-class, because a pseudo-observer has no natural owner for propaganda-driven drift and nowhere to record the campaign that caused it — but the cost of a fifth projection per edge is not this document's to accept |
| **OQ-14** | Is "A's model of the reciprocal edge" accepted as a **fifth** view, beyond the source record's four? | It is an addition to the source record and is labelled as such rather than folded in silently. It is the only view read by a simulation mechanism (RG-M4, RG-M2), which is the argument for it; the argument against is that it is not among the four the source record enumerates, and the burden is on the addition. The burden is not that the source record forbids a fifth: its wording is "at least four" (line 147), which anticipates additions rather than closing the set |
| **OQ-15** | Is `resentment` (D7) a **derived predicate** over the open-thread ledger, or **stored state** carrying grievance the ledger cannot hold? And in either case, what is the precedence rule when the stored value and the ledger disagree? | Rule RG-T10. The document struck `shared_history` and four kinds for exactly this two-sources-of-truth shape, then left D7 in it. The derived-not-stored test was applied to kinds and not to dimensions, and this is the gap |
| **OQ-16** | Is the two-category form of RG-2 adopted — mechanism-backed **or** charter-question-backed, and nothing else? | **RG-2 as first drafted admitted only mechanism-backed fields, which condemned four of this document's own fields** (`causal_parents`, `evidence_observed`, `alternatives_considered`, and the contradiction set). A later reviewer applying it literally would have struck the explainability spine the charter requires. The invariant is only usable as a fake-depth defence if it is true as written |
| **OQ-17** | **Opened 19 July 2026 by founder ruling 1C.** Where does **per-person dissent and defection probability** belong? It is a probability attached to a person, computed from an alignment edge this document now owns, against an organisational position [`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md) owns — so the ruling's three-way split does not place it. [`./PERSON-MODEL.md`](./PERSON-MODEL.md) raises the same gap as its own open question and cites the clause at `psychology.values[]`, `psychology.attitude_to_authority` and `state.loyalty`. **This document makes no claim to it** (§5.4): RG-M4 reads the alignment edge, which is not the same thing as owning the person-side probability | An ownership gap the ruling left open, not a technical choice. All three documents can defensibly claim it, which is precisely why none may take it unilaterally — a clause each document assumes another holds is a clause nobody specifies. Until it is placed, no document should assume it holds it. Note that this document's §5.4 is otherwise complete without it: the edge, its dimensions, its history and its projection are all specified, and only the person-side probability computed *from* them is unplaced |

---

## 15. Cross-references

### Source and governance

| Document | Relationship to this one |
|---|---|
| [`./FOUNDER-REQUIREMENT-2026-07-18.md`](./FOUNDER-REQUIREMENT-2026-07-18.md) | **The source record.** Where this document and it disagree, it is right |
| [`../../CHARTER.md`](../../CHARTER.md) | Non-negotiable. Supplies the causal vocabulary (`:93-111`), the eight-question standard (`:118-133`), the determinism boundary (`:37-44`) and the fictional-entities constraint (`:137`) |
| [`../../HANDOFF.md`](../../HANDOFF.md) | Phase 0 order, standing constraints, backlog disposition |
| [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) | The closed audit. Cited throughout for what is and is not built |
| [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) | The RNG-substream defect (§6) and the forgeable-decision-endpoint evidence (check 5) |

### Sibling world-model documents

**None of the following is implemented.** Each is a specification document in the same backlog set,
drafted from the set the source record specifies at lines 345–352. All were present on disk at the
time of this revision; drafting status is not restated per row here because it changes, and a claim
about repository state is only worth making if it is re-checked at review time. **This document must
not assert what does or does not exist on disk without checking** — an earlier draft claimed none of
these files existed, which was false when written, in the one document class where such claims must
be exact.

| Document | Boundary with this one |
|---|---|
| [`./ENTITY-ONTOLOGY.md`](./ENTITY-ONTOLOGY.md) | Defines what an entity *is* and the shared identifier namespace. This document assumes edge endpoints are entity ids in that namespace; today `cohort_id` (`agent_schema.py:94`) and `agent_id` (`:161`) are separate and nothing binds them. **Must be settled there, not here** |
| [`./PERSON-MODEL.md`](./PERSON-MODEL.md) | Owns the person record. This document owns the ties between people. `affection` (D3) and family obligation are the shared surface. **Two boundaries were settled on 19 July 2026:** it **consumes** the person-to-faction alignment projection this document owns (ruling 1C, §5.4), and its `relationships.obligation_ledger[]` is a **derived projection** over this document's `OpenThread` records, not separately stored state (rule RG-T11, §6.4). One clause of its superseded M14 — per-person dissent and defection probability — is claimed by neither document and is OQ-17 here and an open question there |
| [`./ORGANISATION-MODEL.md`](./ORGANISATION-MODEL.md) | Owns internal factions and the decision process. This document supplies the intra-organisational edges those factions resolve pressure across (RG-M2). **Under ruling 1C it owns faction definitions, membership rules, formal positions and faction structure** (its `M-FAC`, §7.4, with the bloc record at its §8.2); this document owns only the directional, historied alignment **edge** to a faction (§5.4). **No faction structure is specified in this document**, and formal membership there is a distinct fact from the alignment edge here — the two must be able to diverge |
| [`./BELIEF-AND-KNOWLEDGE-MODEL.md`](./BELIEF-AND-KNOWLEDGE-MODEL.md) | **Tightest coupling.** It owns what an entity believes and how belief updates; this document owns the paths belief travels along and the credibility weighting applied on arrival (RG-M1). The existing precedent it must generalise is `Narrative.truth_status` versus `Narrative.adoption_by_cohort` (`agent_schema.py:269-274`), the only structure in the codebase that separates what is true from what is believed |
| [`./POPULATION-FIDELITY.md`](./POPULATION-FIDELITY.md) | Owns the tier definitions, promotion and demotion rules, and population weighting. This document takes them as given (§8) and **must not restate or redesign them** |
| [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) | Owns the ten-tab dossier. This document supplies the queries behind tab 4 (relationships), tab 9 (intelligence assessment) and tab 10 (timeline) — see §10 |
| [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) | Owns the identity design rule and its enforcement. This document specifies the constraint (§13.4) and defers the test to it. **B5 / P0.8 is decided (18 July 2026) and its envelope is applied in both; it is reopened in neither. B5 itself is not cleared — its eight controls are unbuilt — and neither document may treat the decision as discharging them** |

### Code referenced in this document

All paths relative to the repository root, at commit `71fa329`. Every one describes something that
**exists today**.

```text
scaffold/backend/app/simulation/schemas/agent_schema.py
  :22-28    Demographics                    — identity as a per-cohort majority label
  :42-53    MediaExposure                   — fixed five-channel reach, no trust term
  :72-77    InfluenceSusceptibility         — the audience-attribute surface coupled to B5
  :80-88    NetworkPosition / bridges_to    — the only topology running code consumes
  :94,:161  cohort_id / agent_id            — separate namespaces, nothing binds them
  :103-105  Cohort.grievances               — free-form tags; also the gate on an RNG draw
  :143-151  AgentMemory                     — decay-only; cannot hold a formative experience
  :154-184  MicroAgent                      — the only individual-actor structure
  :175-177  MicroAgent.relationships        — dict[str, float], populated by nothing
  :190-200  Relationship                    — declared, never instantiated  ← REPLACED by §9
  :203-208  EventVisibility                 — the only role-asymmetry primitive; never populated
  :211-229  Event (:224 causal_parents)     — declared; never instantiated
  :269-274  Narrative truth vs adoption     — the one truth/belief separation that exists
  :326-331  Campaign target/grievance       — the B5 targeting surface
  :363-365  Outcome.explanation_trace       — list[str]; never constructed
  :374-393  ActionProposal                  — the working determinism boundary

scaffold/backend/app/simulation/diffusion.py
  :18-37    build_cohort_graph              — nx.Graph, UNDIRECTED (:24); weight = mean cohesion (:35)
  :34       institution targets silently dropped
  :40-79    linear_threshold_step           — monotonic non-decreasing (:51, :77); draws at :75

scaffold/backend/app/simulation/engine.py
  :83       the single shared RNG           — hard prerequisite blocker (§11)
  :102      cohort_graph built once at init — no runtime edge formation
  :121-130  _validate_and_price             — never receives the agent spec
  :135      one macro-noise draw per tick
  :142      susceptibility map, no population term
  :163-173  events emitted only on non-empty delta; raw unvalidated dicts

scaffold/backend/app/simulation/agents/cohort_agent.py
  :35-38    in-place mutation, no event, one-way ratchet   ← the anti-pattern RG-T3 forbids

scaffold/backend/app/simulation/agents/institutional_agent.py
  :18-41    one role, one proposal per tick; three-key context stub at :33-37

scaffold/backend/app/db/models.py
  :51       StateSnapshot.meso_state        — declared, written by nothing

scaffold/schemas/relationship.schema.json    — 54-line mirror of a type nothing uses
scaffold/scenarios/kestral-strait.json
  :74,:117,:157,:197,:237   bridges_to declarations — one is one-sided, one node isolated
  :79,:39,:121-122          the population figures behind audit §5.10
```

---

**END — SPECIFICATION, NOT IMPLEMENTED. DRAFT pending owner review. BACKLOG; does not interrupt
Phase 0.**
