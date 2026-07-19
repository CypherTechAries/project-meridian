# Observation and perception model

> # ⚠ SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing in this document exists in code.** Not one field, not one function, not one label. No
> observation is produced, recorded, relayed or degraded anywhere in the MERIDIAN codebase. Every
> mechanism described here is a statement of intent for a future architecture. Where this document
> refers to something that *does* exist today, it says so explicitly and cites `file:line`, so the
> boundary between the built and the specified is always visible.
>
> This document is written in "must", "will" and "is specified as". If any sentence in it reads as a
> description of working software, that sentence is a defect and should be raised. MERIDIAN's
> defining defect is documentation that claimed properties the code did not have; this document must
> not add to it.

**Status:** DRAFT, pending owner review. Not reviewed. Not approved.
**Date:** 19 July 2026.
**Disposition:** **BACKLOG. This must not interrupt Phase 0 remediation.** It is captured now
because two existing specifications assign observation to documents that do not own it, and one of
them says so in terms ([`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md):1455 — "`M-OBS` is specified
in **no** document"). Recording ownership is not scheduling work. **Do not start building any of
it.** Its hard prerequisites — P0.4, P0.4A and P0.6 — are themselves unbuilt.

**Authority.** [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md) is the
source record; where it and this document disagree, it is right and this document is wrong.
[`../../CHARTER.md`](../../CHARTER.md) governs both, then
[`../../HANDOFF.md`](../../HANDOFF.md). Permitted wording is bounded by
[`../delivery/CAPABILITY-CLAIMS.md`](../delivery/CAPABILITY-CLAIMS.md).

**Why this document exists.** Founder decision 1A, 19 July 2026: create one narrowly scoped
specification that owns the observation and perception mechanisms currently orphaned, and **do not
assign simulation mechanisms to a UI specification merely because it displays their output.**

**Siblings** (all DRAFT, all backlog, none implemented):
[`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) ·
[`PERSON-MODEL.md`](PERSON-MODEL.md) ·
[`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) ·
[`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) ·
[`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) ·
[`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) ·
[`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) ·
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md)

---

## Contents

- [1. Plain English](#1-plain-english)
- [2. The spine: the six-stage boundary and who owns each part](#2-the-spine-the-six-stage-boundary-and-who-owns-each-part)
- [3. What this document owns](#3-what-this-document-owns)
- [4. What this document does not own](#4-what-this-document-does-not-own)
- [5. Mechanism register](#5-mechanism-register)
- [6. Invariants](#6-invariants)
- [7. Schema sketch](#7-schema-sketch)
- [8. What exists today](#8-what-exists-today)
- [9. Prerequisites this document cannot satisfy](#9-prerequisites-this-document-cannot-satisfy)
- [10. Open questions for the owner](#10-open-questions-for-the-owner)

---

## 1. Plain English

A crisis is not decided by what is true. It is decided by what reached whom, when, through whom, and
in what condition.

Something happens in the world. Only some entities are in a position to notice it: they were there,
they hold the clearance, they read the channel it was carried on, they know someone who was there.
Of those, some notice it late, some receive a version that has been softened, exaggerated or
misattributed on the way, and some cannot tell who told them. That gap — between an event and what
any particular entity ends up holding about it — is the thing this document specifies.

It is deliberately a narrow document. It stops at the moment an observation is recorded. What the
entity then *believes*, and what a player is then *shown*, belong to other documents. The reason for
drawing the line there is that the same defect keeps recurring in this project: a mechanism gets
attached to whichever document happens to display its output, and then nobody builds it. Observation
is a simulation mechanism. It is owned here, and it is owned here whether or not any interface ever
renders it.

Two things this document must never allow. A player opening a profile must not thereby cause a
simulated entity to have noticed anything — reading is not observing. And opening a profile must not
consume randomness, because if it did, looking at the world would change it.

---

## 2. The spine: the six-stage boundary and who owns each part

This chain is the spine of the whole entity model. Each stage has exactly one owner. Where an owner
is contested today, that is recorded, not papered over.

```
  world event
      │  ── arrow A: exposure ──────────────────────  THIS DOCUMENT (M-OBS-EXP)
      ▼
  observation opportunity
      │  ── arrow B: acquisition and relay ─────────  THIS DOCUMENT (M-OBS-ACQ, M-OBS-ATTR)
      ▼
  entity-specific observation          ← the handover point
      │  ── arrow C: belief update ─────────────────  BELIEF-AND-KNOWLEDGE-MODEL.md §4.5
      ▼
  belief / knowledge state
      │  ── arrow D: view projection ───────────────  ENTITY-ONTOLOGY.md §9.2 (+ access layer, unbuilt)
      ▼
  role-filtered projection
      │  ── arrow E: rendering and narration ───────  ENTITY-PROFILE-EXPERIENCE.md
      ▼
  dossier presentation
```

| Stage or arrow | Owner | Reference |
|---|---|---|
| World event (production, ordering, persistence) | Event/snapshot foundation, **P0.6** | [`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md); [`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.6 (`:87`) |
| **Arrow A — exposure** | **This document** | [§5](#5-mechanism-register) `M-OBS-EXP` |
| **Observation opportunity** (the record) | **This document** | [§7.1](#71-observationopportunity) |
| **Arrow B — acquisition, relay, degradation, attribution** | **This document** | `M-OBS-ACQ`, `M-OBS-ATTR` |
| **Entity-specific observation** (the record) | **Shared, and unreconciled.** The `Observation` schema is already specified in [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md):586-599. This document specifies its **production**; that document specifies its **consumption**. See [Q3](#10-open-questions-for-the-owner) | [§7.2](#72-observation) |
| Arrow C — belief update | [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) §4.5 | — |
| Belief / knowledge storage | [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) §4.3-4.6 | — |
| Arrow D — view projection | [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2 (`ViewKind`, projector) | :854 |
| Role-filtering / player access authorisation | **No document, and no code. The access and role-authorisation layer does not exist.** Not claimed here | [§4](#4-what-this-document-does-not-own) |
| Arrow E — rendering, confidence display, narration | [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) | §3 D-1/D-2/D-3 |

**The handover point is the `Observation` record.** Everything upstream of it is this document.
Everything downstream is not. An engineer building arrow C should need nothing from this document
beyond the record's contents and the guarantee that it is immutable.

---

## 3. What this document owns

1. **What an entity can potentially observe** — the observable surface an entity, event or act
   presents, and to which observer classes.
2. **Observation opportunities** — the modelled step between an event occurring and any entity
   noticing it. Whether an entity observes at all is a computed step, never an assumption.
3. **Source and sensor access** — channel access, network position, media exposure, physical
   presence, clearance. Which access an entity holds is *state* owned by the entity documents; what
   that access **entitles it to observe** is owned here.
4. **Direct versus mediated observation** — presence, documents, testimony, rumour chains, engine
   inference.
5. **Information acquisition** — turning an opportunity into a recorded observation.
6. **Visibility, range, latency and degradation** — whether it reaches, how far, how late, and how
   intact.
7. **Source attribution** — who the receiver believes told it, including failed and mistaken
   attribution, alias resolution and concealed identity.
8. **Observation confidence at acquisition** — the evidential quality of the acquisition itself.
   Distinct from the player-facing confidence *labels*, which are
   [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) §4.7.
9. **Observation events** — observation as an authoritative, replayable simulation event.
10. **The transformation from a world event into an entity-specific observation** — arrows A and B
    in full.

---

## 4. What this document does not own

Each exclusion names its owner. Where the owner does not exist, that is stated rather than assigned.

| Excluded | Owner |
|---|---|
| Belief updating after an observation — credence arithmetic, interpretive priors, congruence, corroboration, salience decay | [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) §4.4-4.6 |
| Knowledge storage — propositions, beliefs, contradiction sets, the belief audit trail | [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) §4.3-4.6 |
| Player-facing confidence labels (Confirmed / Reported / Assessed / Possibly deceptive / Outdated) | [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) §4.7 |
| Dossier rendering, tabs, layout, disclosure UX, prose narration | [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) |
| The four profile views and the view-projection function | [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §8, §9.2 |
| Player access-control decisions — which human player may open which record, authorisation, audit of player access | **The future access and role-authorisation layer, which does not exist.** No document specifies it; no code implements it. This document must not be read as supplying it |
| Narrative prose of any kind | [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) §3 D-3, under [`../../CHARTER.md`](../../CHARTER.md):37-44 (ADR-006) |
| Event production, ordering, hashing, snapshot and replay | **P0.6**, unbuilt |
| Sensitive identity attributes as observation inputs | [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) governs; see [Q5](#10-open-questions-for-the-owner) |

**On the UI exclusion specifically.** [`PERSON-MODEL.md`](PERSON-MODEL.md):504 assigns **M12
OBSERVABILITY** to [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md),
which claims no such ownership and contains no mechanism register. That assignment is the defect
founder decision 1A corrects. A specification that renders a mechanism's output does not own the
mechanism.

---

## 5. Mechanism register

`M-OBS` is adopted here as the umbrella identifier, keeping continuity with
[`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md):390, which defines it as "must determine which
entities observe a decision, an implementation and a divergence, and with what evidential quality".
That definition is **retained and widened**: it is not restricted to decisions, and it covers any
world event. Four sub-mechanisms carry the parts.

| Id | Name | What it must do | Depends on |
|---|---|---|---|
| `M-OBS` | **Observation and evidence emission** (umbrella) | Must determine which entities observe which world events, when, through what path, and with what evidential quality. Decomposes into the four below; `M-OBS` alone is not a buildable unit | P0.4, P0.4A, P0.6 |
| `M-OBS-EXP` | **Exposure and observation opportunity** | Must compute, for a world event, the set of entities in a position to observe it, from event visibility, physical presence, channel access, network position, media exposure and clearance. Must emit an `ObservationOpportunity` per (event, entity) pair it admits, and must emit nothing for entities it does not admit | P0.6; entity access fields |
| `M-OBS-ACQ` | **Acquisition, relay and degradation** | Must convert an opportunity into an immutable `Observation`, setting directness, latency, fidelity and asserted value, including distortion on relay. Must be the only writer of `Observation` records | `M-OBS-EXP`, P0.4A |
| `M-OBS-ATTR` | **Source attribution and identity resolution** | Must determine who the receiver takes the source to be, including anonymity, alias non-resolution, mistaken attribution and deliberate misattribution. Must be able to fail | `M-OBS-ACQ`, [`PERSON-MODEL.md`](PERSON-MODEL.md) identity fields |
| `M-OBS-SURF` | **Observable surface** | Must determine what an entity exposes to a given observer class — public versus concealed identity, contact patterns, holdings, position — supplying the evidence base that distinguishes public from private reputation | [`PERSON-MODEL.md`](PERSON-MODEL.md), [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) |

### 5.1 Supersession of M12 OBSERVABILITY

**`M12` (`PERSON-MODEL.md`:504) is superseded.** Its function is absorbed here and split, because it
was one label over three unrelated jobs:

| M12's function as written | Successor here |
|---|---|
| "what other entities can learn about this person" | `M-OBS-SURF` |
| alias, concealed identity, exposure and attribution failure (`PERSON-MODEL.md`:532, :543) | `M-OBS-ATTR` |
| clearance gating which classified events are observable (`PERSON-MODEL.md`:661) | `M-OBS-EXP` |
| "produces the public profile and the player intelligence profile" | **Not a successor of anything here.** View production is [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2; presentation is [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md). This clause is what wrongly pulled a simulation mechanism into a UI document |

`PERSON-MODEL.md` field rows citing M12 must be re-pointed to the specific sub-mechanism. That
amendment belongs to the `PERSON-MODEL.md` owner, not to this document; the exact wording to use is
given in the handoff note at the end of [§10](#10-open-questions-for-the-owner).

**Naming convention.** `M-OBS*` follows the `ORGANISATION-MODEL.md` convention; `PERSON-MODEL.md`
uses `M<n>`. Whether the two registers are unified or bridged by a crosswalk is
[`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) §19 **Q12**, an open owner decision. This document
does not take it and must not be cited as having taken it.

---

## 6. Invariants

These are correctness properties, not preferences. Each is stated with the test that must eventually
demonstrate it. **None of these tests exists.**

> **O-1. Opening or rendering a dossier consumes zero randomness.** No projection, rendering or
> inspection path may draw from any RNG stream. Identical to
> [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) **D-2**, restated
> here because this document owns the only mechanism that legitimately consumes randomness anywhere
> near a profile.
> *Test:* record RNG draw counts; open N dossiers; assert the count is unchanged.

> **O-2. Reading a projection never creates an observation.** No read path may invoke `M-OBS-ACQ`.
> An `Observation` exists only because `M-OBS-EXP` admitted an opportunity from a world event.
> *Test:* open every dossier of every entity at a tick; assert the observation store is byte-identical.

> **O-3. Observation is an authoritative simulation event.** Observations are authoritative state:
> snapshotted, hashed, replayed. They are not a view, not a cache and not derived from a view. This
> places them inside [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §8.2 **V-1** and depends on P0.4
> settling what authoritative state is.
> *Test:* an observation appears in the snapshot hash; replay from seed reproduces it exactly.

> **O-4. Player UI inspection never mutates simulated entity knowledge.** Nothing a human player
> does in an interface may cause a simulated entity to know, notice or believe anything. Identical
> in force to [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md)
> **D-1**.
> *Test:* full-state hash before and after an arbitrary sequence of player reads is unchanged.

> **O-5. All observation behaviour is deterministic under recorded inputs.** Given the same seed,
> the same event stream and the same entity state, `M-OBS-EXP`, `M-OBS-ACQ`, `M-OBS-ATTR` and
> `M-OBS-SURF` must produce identical outputs.
> *Test:* two runs from one seed produce identical observation streams.

> **O-6. Observations are append-only.** A correction is a new observation, never an edit or a
> deletion. Consistent with [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) **G-3** and
> [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md):610.

> **O-7. Failure to observe is modelled, not assumed.** An entity not observing an event must be the
> recorded outcome of `M-OBS-EXP`, never an omission. Silence must be explicable.

### 6.1 The P0.4A dependency, stated plainly

`M-OBS-ACQ` and `M-OBS-ATTR` are expected to consume randomness — whether a rumour reaches, how far
a claim degrades, whether attribution fails. **Any such draw must come from a named, isolated
substream.** That capability does not exist. There are no named RNG substreams
([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):168-175), and a
draw added in one subsystem silently shifts every later draw everywhere else.

Without P0.4A, adding one observation draw would perturb macro indicators for reasons unrelated to
the model — the exact contamination A3 demonstrated, where changing how many cohorts hold grievances
moved shipping throughput through nothing but draw ordering. It would also make O-1 and O-4
untestable, because a hash difference could not be attributed. **`M-OBS-ACQ` and `M-OBS-ATTR` must
not be built before P0.4A lands** (P0.4A is a founder decision of 18 July 2026, sequenced between
P0.4 and P0.5; the substream mechanism is itself unchosen and no agent may adopt one).

---

## 7. Schema sketch

Illustrative only. Field names are proposals for owner review; nothing below is implemented, and no
migration, table or model corresponds to it.

### 7.1 `ObservationOpportunity`

Emitted by `M-OBS-EXP`. Records that an entity was *in a position* to observe — not that it did.
Whether opportunities are persisted or are a transient per-tick intermediate is [Q1](#10-open-questions-for-the-owner).

```python
class AccessBasis(str, Enum):
    presence   = "presence"     # physically or organisationally present
    clearance  = "clearance"    # entitled by security clearance
    channel    = "channel"      # subscribes to / reads a carrying channel
    network    = "network"      # via a relationship edge to a prior observer
    role       = "role"         # entitled by role occupancy

class ObservationOpportunity(BaseModel):
    opportunity_id: str
    event_id: str                  # the world event (P0.6)
    candidate_entity_id: str
    basis: AccessBasis
    basis_record_ref: str          # the clearance / channel / edge / role record relied on
    earliest_tick: int             # first tick acquisition could occur
    reach_strength: float          # 0..1, propensity for acquisition
    max_fidelity: float            # 0..1, ceiling on how intact it could arrive
    admits_attribution: bool       # can the source be identified through this basis at all
    rule_id: str                   # the M-OBS-EXP rule that admitted it — required
```

`rule_id` is mandatory. Every opportunity must be explicable to the named rule that produced it; an
opportunity with no rule is a defect, not a default.

### 7.2 `Observation`

**This document does not redefine the record.** The `Observation` schema is already specified at
[`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md):586-599, with `Directness`,
`asserted_value`, `parent_observation_id`, `fidelity` and `engine_rule_id`. That specification
stands. What this document adds is that **`M-OBS-ACQ` is its sole writer**, plus four acquisition
fields it lacks:

```python
    opportunity_id: str            # the admitted opportunity this came from — required
    attributed_source_id: str | None   # who the HOLDER takes the source to be
    attribution_confidence: float      # 0..1; may be high and wrong
    acquisition_rule_id: str           # the M-OBS-ACQ rule that produced it — required
```

`source_entity_id` (authoritative) and `attributed_source_id` (as received) must be separate fields
and must be permitted to differ. **That divergence is the whole point.** It is what makes
misattribution, laundered sourcing and covert influence simulation outcomes rather than narration.
Whether these four fields are added to the existing class or carried alongside it is
[Q3](#10-open-questions-for-the-owner).

### 7.3 Observation as an event

Under O-3, an acquisition is itself a recordable occurrence with `event_id`, `tick`, `causal_parents`
(the originating world event, and the parent observation on a relay) and no effects on any other
entity's state. Its representation depends entirely on the P0.6 event foundation and is not fixed
here.

---

## 8. What exists today

Verified 19 July 2026 against the scaffold at baseline.

| Construct | Location | Status |
|---|---|---|
| `EventVisibility` enum — `public` / `classified` / `leaked` | `scaffold/backend/app/simulation/schemas/agent_schema.py:203-208` | Exists. The project's only visibility construct |
| `Event.visibility` field | `scaffold/backend/app/simulation/schemas/agent_schema.py:221-223` | Exists, defaults to `public` |
| `EventVisibility` in the JSON schema | `scaffold/schemas/event.schema.json:3-10`, `:54` | Exists |
| `MicroAgent.information_access` | `scaffold/backend/app/simulation/schemas/agent_schema.py:178-180` | Exists; read by nothing |
| `MediaExposure` | `scaffold/backend/app/simulation/schemas/agent_schema.py:42-53` | Exists |
| Any reader of `visibility` | — | **None.** `grep -rn "visibility" scaffold/backend/app --include=*.py`, excluding the schema file itself, returns no results |
| Observation record, opportunity, exposure rule, relay, attribution | — | **None. Nothing corresponding to this document is implemented** |

Reproduce:

```bash
grep -rn "visibility" scaffold/backend/app --include=*.py
grep -rni "observation" scaffold/backend --include=*.py
```

`EventVisibility` is where `M-OBS-EXP` would finally acquire a reader. It is an *observability* axis
only and must stay distinct from the confidence axis
([`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) §4.7).

---

## 9. Prerequisites this document cannot satisfy

| Prerequisite | Why it blocks | Owner |
|---|---|---|
| **P0.4** authoritative state | O-3 asserts observations are authoritative state. Until P0.4 settles what that is, the assertion has nothing to attach to | Phase 0 |
| **P0.4A** deterministic randomness | [§6.1](#61-the-p04a-dependency-stated-plainly). Blocks `M-OBS-ACQ` and `M-OBS-ATTR` outright | Phase 0; mechanism unchosen — **no agent may adopt one** |
| **P0.6** events, snapshots, replay | There is no event stream to observe, and no replay against which O-5 could be demonstrated | Phase 0 |
| Access and role-authorisation layer | Arrow D's role filter has no owner | **Does not exist. Not specified anywhere** |
| `ViewKind` gap — no kind for entity B's view of entity A | `M-OBS-SURF` output must be readable by a mechanism; [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §8.2 **V-3** and its `ViewKind` enum do not currently admit it | Owner decision **Q-R**, [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §12 |
| Register unification | `M-OBS*` versus `M<n>` | Owner decision **Q12**, [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) §19 |

---

## 10. Open questions for the owner

Unresolved by design. **No agent may resolve any of these.**

**Q1 — Are `ObservationOpportunity` records persisted, or transient?** Persisting them makes "who
could have known?" answerable and every non-observation explicable, at a cost of one record per
(event, candidate) pair per tick — potentially the largest table in the system. Transient
opportunities are cheap but make O-7 hard to evidence.

**Q2 — Is `M-OBS-SURF` a mechanism here, or entity state elsewhere?** The observable surface could be
computed on demand from `PERSON-MODEL.md` / `ORGANISATION-MODEL.md` identity fields, or maintained as
a standing per-entity surface record. This bears directly on
[`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) §15-R9, where `reputation_private` was held
"conditional, and currently unowned" pending exactly this.

**Q3 — Where do the four acquisition fields live?** Extend `Observation` in
[`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md):586-599, or carry an
`ObservationAcquisition` record keyed to it? The first keeps one record; the second keeps each
document's schema its own. Related: which document is the schema's owner of record once two
documents write to it.

**Q4 — How coarse is exposure at scale?**
[`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) tiers entities by fidelity, and
[`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md):978-987 already contemplates
cohort-level exposure standing in for per-person observation. At which fidelity tier does per-entity
observation stop and cohort-level exposure begin, and what happens when an entity is promoted across
that boundary mid-run?

**Q5 — May any sensitive identity attribute enter an exposure or attribution rule?**
[`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) §15-R14 leaves open whether `M-OBS` should be
extended to cover language-gated media reach and comprehension. There is a real mechanism there
(you cannot read what you cannot read) and a real hazard: it is precisely where a stereotype could be
built into arithmetic. Governed by
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md). **Left
struck by default until the owner decides.**

**Q6 — Does an entity observe its own acts, and does it observe non-events?** Self-observation, and
whether the *absence* of an expected event (a signal that did not come) is observable, both change
the shape of `M-OBS-EXP` considerably.

**Q7 — Is `M-OBS` still the right identifier?** It is retained for continuity with
[`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md):390, but its definition there is scoped to
decisions and is widened here. Confirm or rename before anything cites it.

---

### Handoff note for sibling amendments

Sibling documents are amended by their own owners, not by this one. Amendments must be
**amendments or supersession notices, never silent rewrites**
([`../../HANDOFF.md`](../../HANDOFF.md), standing constraints). The wording each sibling should use
to reference this document as owner is set out in the return note accompanying founder decision 1A,
and must be used verbatim so that all registers stay consistent.
