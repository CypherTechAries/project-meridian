# ENTITY-PROFILE-EXPERIENCE — the player-facing dossier as an intelligence product

> # ⚠ SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing in this document exists in MERIDIAN's code.** There is no dossier interface, no
> profile screen, no role-based view, no confidence label, no provenance badge and no portrait.
> **No endpoint serves entity state.** The closest thing that exists today is `get_state`, which
> returns the macro snapshot, a per-cohort `narrative_adoption` dict and a stub briefing string
> (`scaffold/backend/app/api/routes_simulation.py:63-77`), and the only front-end artefact
> in the repository is a minimal development stub
> (`scaffold/frontend/index.html`). This document specifies a future interface. It does not
> describe working software.
>
> Every behavioural sentence below is written in **will**, **must** or **is specified as**,
> deliberately. Where this document describes something that **does** exist today, it says so
> explicitly and cites `file:line`, so the boundary between what is built and what is specified
> stays visible on every page. MERIDIAN's defining defect is documentation that claims properties
> the code does not have. If any sentence here reads as a description of a working screen, that
> sentence is wrong and should be reported as a defect against this document.

**Status:** DRAFT, pending owner review.
**Dated:** 18 July 2026.
**Amended:** 19 July 2026, in two respects, both marked in place rather than silently absorbed.
First, **founder ruling 1A** — observation and perception are owned by
[`../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md`](../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md)
and this document owns dossier rendering only ([§3.1](#31-what-this-document-owns-and-what-it-does-not),
[§4.2](#42-two-axes-never-one-enum), [§4.3](#43-how-the-player-intelligence-profile-is-assembled),
PR-1 and PR-5 in [§11](#11-hard-prerequisites--none-of-which-is-met-today),
[§14](#14-related-documents)). Second, a **documentation fix identified by adjudication** — the
conditional in [§7.2](#72-the-sections-that-carry-the-most-design-weight) and
[§9.6](#96-what-does-this-person-believe-that-is-factually-wrong) now cites the open owner decision
that gates it, recorded as [§13](#13-open-questions) **Q11**. Neither amendment adds a claim or
changes any specified behaviour, and neither resolves an owner decision. Nothing in this document is
implemented, before or after them.
**Type:** Design specification. Backlog. Placed in `docs/design/` rather than `docs/world-model/`
because it specifies an interface, not a world model.
**Source record:** [`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md).
Where this document and the source record disagree, the source record is right and this document is
wrong. Where this document and [`../../CHARTER.md`](../../CHARTER.md) disagree, the charter governs.

**Disposition — read this before acting on anything below.**
This work is **BACKLOG**. The founder was explicit: it **must not interrupt Phase 0 remediation**
(source record lines 5-6 and 340-341; [`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:107-120`)). This document
does not authorise, schedule or begin any implementation. Nothing in it should be started now. Its
purpose is to capture the intent precisely enough that the interface can be designed against it
later, and to record which Phase 0 items it depends on and must not disturb.

**Decision authority.** This record is drafted by an AI agent. AI agents may draft records but may
not approve decisions ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)). Every point requiring a human
choice is recorded in [§13 Open questions](#13-open-questions) and left unresolved.

---

## Contents

1. [Plain-English layer](#1-plain-english-layer)
2. [What exists today](#2-what-exists-today)
3. [The governing idea, in technical form](#3-the-governing-idea-in-technical-form)
4. [Role-based visibility](#4-role-based-visibility)
5. [Confidence labels at the interface](#5-confidence-labels-at-the-interface)
6. [Provenance at the interface](#6-provenance-at-the-interface)
7. [The ten person dossier sections](#7-the-ten-person-dossier-sections)
8. [How the tabs differ for an organisation, a business and a state](#8-how-the-tabs-differ-for-an-organisation-a-business-and-a-state)
9. [The questions the dossier must answer](#9-the-questions-the-dossier-must-answer)
10. [Portrait progression](#10-portrait-progression)
11. [Hard prerequisites — none of which is met today](#11-hard-prerequisites--none-of-which-is-met-today)
12. [The causal-value test applied to this document](#12-the-causal-value-test-applied-to-this-document)
13. [Open questions](#13-open-questions)
14. [Related documents](#14-related-documents)

---

## 1. Plain-English layer

### What this document is for

When a player clicks on a person, an organisation, a business, a community or a country in
MERIDIAN, a **dossier** is specified to open: a structured, multi-tab profile of that entity. This
document defines what those tabs are, where each tab's information comes from, what the player's own
role is and is not allowed to see, and how the interface must make honest what it is showing —
including the difference between a fact the engine computed and a sentence a language model wrote.

### The one idea that governs everything

The source record states it plainly (line 165):

> The profile interface therefore becomes an intelligence product, not an omniscient encyclopaedia.

An encyclopaedia tells you what is true. An intelligence product tells you **what you have been able
to establish, how confident you are, where it came from, and what is still unknown or contested**.
The same minister looks different to a prime minister, to a journalist and to a rival state, because
each has seen different evidence. The dossier must reproduce that. A profile that simply reveals the
simulation's ground truth to everyone would be the encyclopaedia the source record rejects, and it
would also destroy the entire premise of intelligence failure, deception and misperception as
things a player can experience.

### The profile is not the truth

This follows the four-view model specified in
[`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §8. Every entity is
specified to have **at least four** versions of its profile — the source record's wording is "at
least four" ([`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md):147),
so the four it enumerates are a minimum, not a closed set. The four enumerated are:

1. **Authoritative reality** — what is actually true. The player may never see all of it.
2. **The entity's self-understanding** — what it believes about itself.
3. **Public profile** — what is publicly reported or commonly believed, including propaganda,
   error and stale information.
4. **Player intelligence profile** — what the player's role has been able to establish.

The dossier is specified to render primarily the **fourth** view, drawing on the second and third
where the player's role has access to them, and **never** the first except where the player's role
has legitimately established a fact. Only authoritative reality is specified as simulation state; the
other three are specified as derived views
([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §8.2).

**None of this has a representation anywhere in the codebase.** The four-view split has **no
attachment point** today: every state record holds exactly one copy of the truth, as recorded in the
[§2](#2-what-exists-today) table. The numbered list above describes a specified model, not an
existing one.

This document specifies how those derived views are presented; it does not specify what is
authoritative — that is P0.4's job, and it has not been done (see [§11](#11-hard-prerequisites--none-of-which-is-met-today)).

### The honesty rule that is specific to an interface

The charter requires ([`../../CHARTER.md`](../../CHARTER.md):141):

> Every AI-generated advisory text carries a visible provenance tag distinguishing it from
> engine-computed fact, at the interface level and not merely in a documentation footnote.

A dossier **would be** the single place in MERIDIAN where this rule bites hardest, because a dossier
is specified to mix the two: a numeric belief the engine will have computed, rendered beside a
paragraph of biography a language model will have narrated. **Neither producer exists today** — no
engine computes an entity belief, and no language model writes biographies (the gateway returns a
canned `ActionProposal` and a canned briefing string, `llm_gateway.py:35`). If the interface renders
them in the same style, the player cannot
tell the audited fact from the plausible-sounding prose — which is the exact failure the charter and
this whole remediation phase exist to prevent. [§6](#6-provenance-at-the-interface) specifies the
visual separation in detail.

### What this depends on that does not exist

This specification cannot be built on the current foundations, and it is important to say so up
front rather than discover it later. In brief (the full table is [§11](#11-hard-prerequisites--none-of-which-is-met-today)):

- There is **no authentication or authorisation layer of any kind**
  ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §7). "Player role" —
  the thing the entire intelligence-product premise turns on — currently has nothing to resolve
  against.
- **P0.4** has not defined what counts as authoritative state, so the four views this dossier
  renders have no settled contract underneath them.
- **P0.6** has not repaired events, snapshots and replay, so the Activity, Timeline, Beliefs-and-why
  and Intelligence-assessment tabs — all of which read recorded history and evidence — are not
  merely unbuilt but **unbuildable**.
- **Deterministic randomness isolation** does not exist, which matters here in a specific way:
  opening a dossier must not change the simulation, and stable portraits are impossible without it.
  It is owned by **P0.4A**, a Phase 0 workstream created by founder decision of 18 July 2026 and
  ordered `P0.4 → P0.4A → P0.5 → P0.6`
  ([`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md) §P0.4A).
  The mechanism — stateful named substreams or keyed / counter-based draws — is an unmade owner
  decision, so "substream" elsewhere in this document names the problem rather than the solution.
  Entity promotion and world-model materialisation, on which stages 2-3 of the portrait progression
  depend, may not proceed until P0.4A passes.
- **B5 / P0.8 is DECIDED** (founder decision, 18 July 2026) and binds this document directly, in two
  ways it must not be allowed to blur. First, the dossier is the surface on which
  audience-segmentation attributes become individually queryable, so the decision's targeting
  constraints apply to the queries it serves ([§9.9](#99-the-dual-use-warning-that-runs-through-this-section)).
  Second, the decision places a requirement **on this document specifically**: the API and the UI
  must **disclose that the active world is fictional** ([§6.5](#65-fictional-world-disclosure)).
  **No disclosure of any kind exists** — there is no UI, and the scenario's own
  `fiction_disclaimer` is read by nothing. B5 no longer clears by a decision; it clears when its
  controls are built and verified.

---

## 2. What exists today

Stated exactly, so the boundary between fact and specification stays visible. Line citations are as
of commit `71fa329`.

**There is no dossier, and no interface that could hold one.**

| Concern | What exists today | Location |
|---|---|---|
| State-serving endpoint | `get_state`, returning the macro snapshot, a per-cohort `narrative_adoption` dict (`:75`) and a bare stub briefing string (`:76`). No entity records, no cohort attributes, no role parameter. `narrative_adoption` is the **only sub-macro value any endpoint currently serves** — and it is the sole existing precedent for the Public perception tab's subject matter. | `scaffold/backend/app/api/routes_simulation.py:63-77` |
| Event-serving endpoint | `get_events`, returning the whole raw event log unfiltered — no visibility filter, no role parameter, no causal structure. | `scaffold/backend/app/api/routes_simulation.py:104-111` |
| Role / auth layer | **None of any kind.** No authentication, no authorisation, no notion of a player role to resolve visibility against. | audit §7 (IAM row) |
| Front end | A single minimal development stub with a "Create run" button and a raw JSON view. No profile screen, no tabs, no graph. | `scaffold/frontend/index.html` |
| Fictional-world disclosure | **None.** No schema field asserts that a scenario is fictional; there is no `world_mode` field and no scenario schema to declare one in (audit §5.13). The demo's `fiction_disclaimer` is read by no code, appears in no API response, and appears nowhere in the front-end stub (audit §5.12). Control B5-7 ([§6.5](#65-fictional-world-disclosure)) has nothing to build on. | `scaffold/scenarios/kestral-strait.json:7`; audit §5.12 |
| Provenance marker | The briefing is returned as a **bare string** beside the macro state. The only marker is the literal `[STUB briefing — …]` prefix (`llm_gateway.py:100`), which vanishes the moment a real model is wired in. `CHARTER.md:141` requires a tag "at the interface level"; there is no interface. | audit §6.49; `scaffold/backend/app/api/routes_simulation.py:76` |
| Cross-origin access | No CORS middleware, so even the documented "open the stub in a browser" workflow is blocked before the server sees the request. | audit §6.50 |
| The four views | **No attachment point.** Every state record holds exactly one copy of the truth. `MacroState`, `Cohort` and `MicroAgent` are single records with no believed-versus-actual split. | [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §8 |
| Visibility primitive | `EventVisibility` — `public` / `classified` / `leaked` — is the only role-asymmetry construct. It is never populated, it sits on *events* not entity attributes, and its three values do not map onto the source record's eight confidence labels. | `scaffold/backend/app/simulation/schemas/agent_schema.py:203-208` |
| Truth-vs-belief precedent | `Narrative.truth_status` versus `Narrative.adoption_by_cohort` is the one existing structure that separates what is true from what is believed. It exists for claims only, not for entities. | `agent_schema.py:269-274` |
| Snapshot slot | `StateSnapshot.meso_state` is a declared JSON column that nothing writes — the natural landing site for entity-tier state a dossier would read. | `scaffold/backend/app/db/models.py:51` |
| The LLM boundary | `ActionProposal` is the only type the LLM gateway may return, and it carries no authority to change numbers. This is the one existing structure this document builds on directly. | `agent_schema.py:374-393`; `llm_gateway.py:35` |

**On the "25-screen UX".** A separate visual-system track is intended to specify MERIDIAN's full
screen set (the backlog documents `SCREEN-SPECIFICATIONS` and siblings,
[`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:121-123`)). That work is **not part of this document and is not
built**. This document specifies only the dossier's *information architecture, visibility rules,
provenance rules and model bindings* — what each tab means, where it draws from, and who may see it.
It does not specify visual design, layout, motion or the wider screen inventory. Neither the screen
specifications nor this dossier exists as software. Nothing in this section should be read as
implying otherwise.

---

## 3. The governing idea, in technical form

The dossier is specified as a **rendering of derived views**, and it inherits three hard constraints
from the view-projection mechanism in
[`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §9.2. These are not
interface preferences; they are correctness properties.

> **D-1. A dossier is a projection, never a mutation.** Rendering a profile must be a pure function
> of authoritative reality, observation history and the observer. It must never write to
> authoritative state. Opening, reading, closing and re-opening a dossier any number of times must
> leave the simulation byte-identical.

> **D-2. A dossier must consume zero randomness.** Projection must not draw from any RNG stream. If
> it did, *looking at an entity would change the simulation* — a variant of the
> attention-perturbs-the-world defect A3 demonstrated for the shared RNG stream
> ([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):156-175, and
> [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §7.3). A player who opens
> ten dossiers must not thereby move the national economy.

> **D-3. Projection and narration are two separate steps, and only the second may call a model.**
> The projector computes the structured view — values, confidence labels, evidence links,
> contradictions — with no language model involved. A *later, separate* step may render parts of
> that structured view into readable prose through the LLM boundary. The model narrates a view it is
> handed; it never assembles the view, never authors a confidence label, and never invents a fact.
> This is [`../../CHARTER.md`](../../CHARTER.md):37-44 (ADR-006) applied to the dossier.

The reason D-1 and D-2 are stated as first-class requirements is that the interface is the place a
future contributor is most tempted to break them — caching a generated biography by writing it back
onto the entity, or drawing a "random flavour detail" at render time. Both would convert a read
surface into a silent writer. The dossier must be structurally incapable of it.

### 3.1 What this document owns, and what it does not

**Amendment, 19 July 2026 — founder ruling 1A.** This subsection is new. It records an ownership
boundary that was previously implicit, and it is placed in §3 because the boundary is a correctness
property of the same kind as D-1 to D-3, not an editorial note.

This document specifies presentation only. Observation is a simulation mechanism owned by
[`../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md`](../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md);
this document neither owns nor implies it, and any assignment of an observation mechanism here is a
defect. Invariants O-1 and O-4 in that document restate D-2 and D-1 in mechanism terms.

**What this document owns: dossier rendering, and nothing else.** Its subject matter is the
information architecture, role-based visibility rules, provenance rules and model bindings of a
player-facing dossier — what each tab means, where it draws from, who may see it, and how the
interface stays honest about what it is showing. It owns no state, no schema, no mechanism and no
draw.

**Why this needed saying.** [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md):504
previously assigned mechanism **M12 OBSERVABILITY** in part to this document, on the ground that this
document produces the public profile and the player intelligence profile. **This document never
claimed that mechanism, and could not have held it.** Founder ruling 1A of 19 July 2026 withdraws the
assignment. M12 is superseded and split between `M-OBS-SURF`, `M-OBS-ATTR` and `M-OBS-EXP` in the
owning document; view *production* is
[`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §9.2, and only view
*presentation* is this document's.

> **D-4. A UI specification does not own a simulation mechanism merely because it displays that
> mechanism's output.** Rendering is not authorship. A document that specifies how a value is shown
> acquires no authority over how the value comes to exist, and a mechanism assigned to a
> presentation document is a mechanism with no owner — which is how a specification comes to assert
> a property that nothing computes. Any future assignment of a simulation mechanism to this document
> must be rejected and reported as a defect against the assigning document.

**The boundary chain, stated once.** Each link has exactly one owner. This document is the last link
and reads only what the link before it hands over.

| # | Link | Owner |
|---|---|---|
| 1 | World event occurs | The tier mechanisms (unbuilt; P0.6 for the event stream) |
| 2 | Event → observation *opportunity*: who was in a position to observe it | `M-OBS-EXP` — [`../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md`](../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md). Sole future reader of `EventVisibility` |
| 3 | Opportunity → entity-specific `Observation`: directness, latency, fidelity, distortion, source attribution | `M-OBS-ACQ` and `M-OBS-ATTR` — the same document. `M-OBS-ACQ` is the **sole writer** of `Observation` |
| 4 | Observation → belief update, knowledge storage, confidence labelling | [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md) §4.5, §4.7 |
| 5 | Role-filtered projection of the resulting state | View production is [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §9.2; **player access control is the future access/role layer, which does not exist and is not owned by any Phase 0 item** (PR-1, [§13](#13-open-questions) Q1) |
| 6 | Presentation of that projection as a dossier | **This document** |

Two consequences follow, and both are already the position taken elsewhere in this document rather
than a change to it. First, [§4.3](#43-how-the-player-intelligence-profile-is-assembled) step 2
*gathers* observation records; it does not specify how they are produced, and must never be read as
doing so — their production is link 3. Second, the eight confidence labels
([§5](#5-confidence-labels-at-the-interface)) are computed from an evidence base this document does
not own, which is why C-2 forbids anyone at this layer authoring one.

**D-1 and D-2 checked against the owning document's invariants.** Both hold, and neither needs
amending:

| This document | Owning document | Finding |
|---|---|---|
| **D-2** — a dossier must consume zero randomness | **O-1** — opening or rendering a dossier consumes zero randomness | **Consistent.** O-1 states it is "identical to D-2" and adds the test: record RNG draw counts, open N dossiers, assert the count is unchanged. That document's §6.1 records that without **P0.4A** both O-1 and O-4 are untestable, because a hash difference could not be attributed to a cause. P0.4A has not been done (PR-4). |
| **D-1** — a dossier is a projection, never a mutation | **O-4** — player UI inspection never mutates simulated entity knowledge | **Consistent.** O-4 states it is "identical in force to D-1" and adds the test: the full-state hash is unchanged across an arbitrary sequence of player reads. |
| — | **O-2** — reading a projection never creates an observation | **Consistent, and stronger than anything stated here.** O-2 forbids a read path invoking `M-OBS-ACQ` at all: an `Observation` exists only because `M-OBS-EXP` admitted an opportunity from a world event. D-1 forbids the dossier writing authoritative state, which already forbids it writing an observation, so no new constraint is needed at this layer. The property is recorded here so that a future contributor adding a "mark as seen" affordance to a dossier can see that it is prohibited by the owning document, not merely undesirable. |

No conflict was found. Note what this does **not** establish: the invariants agree, but **none of
the tests behind them exists**, in either document. O-1 and O-4 are stated with tests that have not
been written, against code that has not been written.

---

## 4. Role-based visibility

### 4.1 Plain-English

The same entity must look different to different players, because each player's role has seen
different things. The source record's own examples (lines 160-163):

- **A prime minister** might see a security assessment that ordinary players cannot.
- **A journalist** might see sources and public records, but not classified intelligence.
- **A business leader** might know market relationships, but not classified intelligence.

The dossier must enforce this at the point of projection, not by hiding rendered content in the
browser. A value the player's role may not see must never be sent to the client at all.

### 4.2 Two axes, never one enum

This document adopts the ontology's insistence
([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §8.4) that **visibility and
confidence are different questions and must be modelled separately**:

- **Visibility** — *may this observer see this attribute at all?* Answered per role. Its refusal
  outcome is the label **Restricted**.
- **Confidence** — *how well is this attribute evidenced for this observer?* Answered from evidence.
  Its outcomes are the other seven labels.

Overloading one enum with both would make "observable but poorly evidenced" and "well-evidenced but
withheld" inexpressible. The existing `EventVisibility` enum (`agent_schema.py:203-208`) is on the
visibility axis only, sits on events rather than entity attributes, and must be extended along the
visibility axis alone — confidence is modelled independently ([§5](#5-confidence-labels-at-the-interface)).

*(Amended 19 July 2026, founder ruling 1A.)* The sentence above states an interface **requirement
on** `EventVisibility`, not authority **over** it. Under D-4
([§3.1](#31-what-this-document-owns-and-what-it-does-not)) this document owns no schema: the enum,
its future reader and any extension of it belong to `M-OBS-EXP` in
[`../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md`](../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md),
which that document names the **sole future reader** of `EventVisibility` — link 2 of the boundary
chain. What this document requires is only that whatever the owning mechanism yields does not fold
confidence into the visibility axis, because a dossier must be able to render "observable but poorly
evidenced" and "well-evidenced but withheld" as different rows. If the two documents disagree on the
shape of the enum, the owning document decides and this one is amended.

### 4.3 How the player intelligence profile is assembled

Specified as a pure projection. Restating the ontology's sketch
([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §9.2) in the terms this
document uses:

```text
project_player_view(entity, observer_role, as_of_tick) -> Dossier

 For each candidate attribute of the entity's authoritative_state:
   1. VISIBILITY  decide, from observer_role and the attribute's visibility class,
                  whether this role may see it at all.
                  If not -> emit a Restricted row (label shown, value withheld). Continue.
   2. EVIDENCE    gather the observation records this role has accumulated about the
                  attribute (source, corroboration count, recency, known deception).
                  DEPENDS ON P0.6 — no observation record exists today.
   3. CONFIDENCE  COMPUTE one of the seven evidence labels from that evidence.
                  Never authored by a scenario or a model (§5).
   4. VALUE       the value as this role currently understands it — which may be the
                  public/propagated value, not authoritative reality, when that is all
                  the role has seen. An entity acting on this view is INTENDED as the
                  mechanism by which deception becomes an outcome (ENTITY-ONTOLOGY V-3)
                  — but see the Q-R caveat below: V-3 does not currently admit this
                  path, and every V-3 citation in this document is PROVISIONAL.
   5. CONTRADICTIONS attach any observations that disagree -> drives `Disputed`.

 Emit the assembled rows. Consume no RNG (D-2). Call no model (D-3).
```

The projector's output is structured data. Prose narration of it is the separate, provenance-tagged
step of [§6](#6-provenance-at-the-interface).

*(Amended 19 July 2026, founder ruling 1A.)* Step 2 **gathers** observation records; it does not
produce them, and no reader may take it as specifying how they come to exist. Their production is
link 3 of the boundary chain ([§3.1](#31-what-this-document-owns-and-what-it-does-not)), where
`M-OBS-ACQ` is the **sole writer** of `Observation`
([`../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md`](../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md)).
The step's `DEPENDS ON P0.6` note stays correct and is now joined by that dependency: P0.6 must
supply the recorded history, and the observation model must supply the records themselves. Neither
exists. A further consequence of that document's invariant **O-2** is that this gathering step is a
**read**: it must never cause an `Observation` to come into being, and a "mark as seen" affordance
on a dossier is prohibited, not merely undesirable
([§3.1](#31-what-this-document-owns-and-what-it-does-not)).

> **Every citation of V-3 in this document is provisional, and this document does not resolve why.**
> [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md):608-616 records that
> "**V-3 and the public profile do not currently fit together, and this document does not resolve
> it.**" V-3 as written admits a derived view as a mechanism input only where the observer is itself
> the holder of that view, and `ViewKind` offers no kind for *simulated entity B's view of entity A*
> — which the ontology calls "precisely the input V-3's exception licenses". The resolution is owner
> decision **Q-R** (ontology §12, `:1108`), which concludes: "**The view taxonomy must not be
> implemented until this is taken.**"
>
> Step 4 above, the deception mechanism it names, the Beliefs tab's mechanism claim
> ([§7.1](#71-the-ten-sections) row 5), the Public perception row (row 8) and the
> [§12.1](#121-dossier-elements-that-trace-to-a-simulation-mechanism) rows that cite V-3 all rest on
> a rule flagged as internally contradictory and blocked on an owner decision. **None of them may be
> read as settled.** Recorded as prerequisite PR-8 ([§11](#11-hard-prerequisites--none-of-which-is-met-today))
> and open question Q9 ([§13](#13-open-questions)). **No agent may resolve Q-R.**

### 4.4 A worked visibility matrix (illustrative — nothing here is built)

Using the demo scenario's own roles and information holdings. The `information_access` and
`constraints` arrays already in the scenario are the natural seed for a visibility model, though they
are read by no code today (audit §5.4). Consider the intelligence lead's raw attribution holding —
`raw_attribution_lead_55pct` (`scaffold/scenarios/kestral-strait.json:363`) — as an attribute of the
`intel-lead-navarro` entity (`:345`):

| Observer role | Sees the raw 55% attribution lead? | Sees the *existence* of an assessment? | Rationale |
|---|---|---|---|
| Head of government (`head-of-government-varo`, `:243`, holds `full_cabinet_visibility` `:262`) | **Yes**, value + `Assessed` label | Yes | Cabinet-level security access. The source record's "prime minister sees a security assessment". |
| Intelligence lead (`intel-lead-navarro`, `:345`) | **Yes** — it is their own holding | Yes | The originator. |
| A journalist role | **No** → `Restricted` row | Possibly, if the *existence* has leaked | Sources and public records only — the source record's journalist. |
| A business-leader role | **No** → `Restricted` row | No | Market relationships, not classified intelligence — the source record's business leader. |

The same matrix run over the strategic-communications entity's public narrative-tracking holding
(`narrative_tracking_dashboard`, `:385`) inverts several cells: the journalist role sees the public
narrative environment that the classified attribution stays hidden from. Different roles, different
dossiers, same entity.

### 4.5 The dependency this rests on

**None of §4 can be built until an authorisation layer exists.** There is no auth of any kind today
(audit §7), so `observer_role` has nothing to resolve against, and every visibility decision above is
a decision with no subject. This is a hard prerequisite ([§11](#11-hard-prerequisites--none-of-which-is-met-today)),
and it is one the wider Phase 0 work does not currently own — the audit records IAM as a Phase 2
concern.

---

## 5. Confidence labels at the interface

### 5.1 The eight labels

The player intelligence profile must label every assertion with exactly one of the eight labels from
the source record (lines 157-159):

**Confirmed · Reported · Assessed · Disputed · Unknown · Possibly deceptive · Outdated · Restricted**

> **C-1.** Every value the dossier shows on the player-intelligence view carries exactly one label.
> A value with no label must never be rendered.
>
> **C-2.** Labels are **computed** by the projector from recorded evidence — source reliability,
> corroboration count, staleness, known deception, and visibility class. They must never be authored
> by a scenario author or by a language model
> ([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §8.4, V-4).

### 5.2 What each label means, and how it is surfaced

| Label | Axis | Computed from | Interface treatment (specified) |
|---|---|---|---|
| **Confirmed** | evidence | Multiple independent, reliable observations agree | Value shown plain, with an evidence-count affordance opening the supporting records |
| **Reported** | evidence | A single source, or sources of unestablished reliability | Value shown with a single-source marker |
| **Assessed** | evidence | The engine's analytic derivation, not a direct observation | Value shown as an assessment, visually distinct from a directly observed fact |
| **Disputed** | evidence | Two or more observations contradict | Value shown alongside the contradicting value(s); the player is never handed a false resolution |
| **Unknown** | evidence | No observation exists for this attribute | Row present but value absent — the *absence* is information and must be shown, not hidden |
| **Possibly deceptive** | evidence | The source is flagged as a known or suspected deception vector | Value shown with an explicit deception warning; never silently trusted |
| **Outdated** | evidence | The most recent observation is older than a staleness threshold | Value shown with its as-of tick and an explicit staleness marker |
| **Restricted** | **visibility** | The observer's role may not see this attribute | Row present, **value withheld**, labelled Restricted — the player learns the attribute *exists* but not its value, unless even existence is withheld |

Two design points that follow directly:

- **Unknown and Restricted must both be rendered as present rows.** An intelligence product's most
  important content is often what it does *not* know or *may not* see. Hiding those rows entirely
  would turn the dossier back into an encyclopaedia that simply looks complete — the same
  false-completeness failure that let a 63× population error read as fine because nothing surfaced
  it (audit §5.10).
- **Possibly deceptive is the label that makes deception playable.** It is specified as the interface
  expression of the V-3 mechanism (provisional — see the Q-R caveat at
  [§4.3](#43-how-the-player-intelligence-profile-is-assembled)): an entity (or a player) may be
  acting on a value that authoritative reality
  contradicts. The label warns; it does not correct, because correcting it would leak authoritative
  reality the role has not earned.

### 5.3 The precedent to extend

`Narrative` already separates `truth_status` from `adoption_by_cohort` (`agent_schema.py:269-274`) —
the only place in the codebase that distinguishes what is true from what is believed. The confidence
model generalises that split from claims to every entity attribute. It is an extension of an existing
idea, not a new invention.

---

## 6. Provenance at the interface

This is the charter requirement that a dossier makes unavoidable, and it is the section most likely
to be skimmed and then got wrong. It is specified in full.

### 6.1 The rule

> **P-1.** Every element the dossier renders is exactly one of two kinds: an **engine-computed
> assertion** or an **AI-generated narration**. The two must be visually distinguishable at a glance,
> per element, with no reliance on a page-level caption or a documentation footnote
> ([`../../CHARTER.md`](../../CHARTER.md):141).
>
> **P-2.** No AI-generated narration may ever be rendered in the visual style of an engine-computed
> assertion, and no engine-computed assertion may borrow the styling of narration to look more
> readable. The distinction is load-bearing and must not be softened for aesthetics.
>
> **P-3.** A confidence label ([§5](#5-confidence-labels-at-the-interface)) belongs **only** to an
> engine-computed assertion. Narration never carries a confidence label, because it is not evidence;
> it carries a provenance tag instead. Conflating the two would let generated prose inherit the
> authority of computed fact.
>
> **P-4. Every narration block must pass the pre-display bias filter, and the dossier must not
> juxtapose identity with judgement.** P-1 to P-3 govern *provenance* and the never-author boundary.
> Neither catches **stereotyped inference from facts that are true**: a biography narrated from a
> truthful ethnic, religious or class identity field can imply competence, morality or reliability
> without inventing a single fact, so it passes the never-author test and still commits the failure
> the source record names (`:305-306`). Therefore:
>
> - Every generated narration block the dossier renders must pass the prohibited-construction
>   detector of [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md)
>   §6.4 **before display**, not only in offline tests (that document's §7.3 places the obligation on
>   this surface). A block that fails the filter must not be rendered.
> - No dossier prompt may instruct or invite the model to infer character, competence or morality
>   from identity (§7.2 of the same document).
> - **Display rule.** The dossier must not place a sensitive-identity attribute adjacent to a
>   competence, reliability or morality assessment in a way that implies causation between them —
>   the juxtaposition itself carries the inference, whether or not either element is individually
>   honest.
>
> The filter is a **heuristic** and the safety document says so: it will miss stereotypes it has no
> pattern for. It is a required gate, not a proof of safety. Recorded as prerequisite PR-9
> ([§11](#11-hard-prerequisites--none-of-which-is-met-today)).

### 6.2 How the two are visually distinguished (specified)

| | Engine-computed assertion | AI-generated narration |
|---|---|---|
| **What it is** | A value read from authoritative reality through the projector | Prose rendered from a structured view by the LLM boundary |
| **Container** | Plain data row / field | A visibly distinct container — tinted panel, ruled edge, or equivalent — that reads as "not a fact panel" without needing to be read |
| **Persistent tag** | Confidence label chip (§5) | A persistent "AI-generated" provenance badge on the block itself, so a screenshot of the block alone still carries its provenance |
| **Grounding affordance** | Evidence affordance opening the observation records behind the value | A "grounded in" affordance listing the record IDs the narration was rendered from, so the player can check the prose against the audited facts |
| **Versioning shown** | Tick and derivation | `model_id + prompt_version + temperature` of the generation, so two narrations are comparable and a regeneration is detectable |
| **May change numbers?** | The value *is* state (read-only here) | **Never.** If narration and the facts it cites disagree, the facts win and the narration is flagged as stale and regenerated |

### 6.3 Why this is essential specifically in a dossier

In the code that exists today, engine fact and model prose live in different places — numbers in the
state object, the briefing in a separate string. A dossier is specified to **interleave** them: the
Biography tab will render model prose grounded in structured life-history facts; the Motivations tab
must pair computed objective priorities with a written explanation; the Intelligence-assessment tab
must show computed confidence beside a narrated summary of the contradictions. **None of these tabs
exists.** Interleaving is what would make a dossier readable, and it is exactly the condition under
which an untagged interface would let a player mistake a fluent paragraph for an audited result.

The current code shows the failure mode in miniature: `get_state` returns the briefing as a bare
string next to the macro numbers (`scaffold/backend/app/api/routes_simulation.py:76`), and the only
thing marking it as
generated is a `[STUB briefing — …]` prefix (`llm_gateway.py:100`) that disappears when a real model
is connected (audit §6.49). The dossier must not inherit that pattern at ten times the surface area.

### 6.4 The boundary this builds on

All dossier narration must route through an equivalently constrained boundary to `ActionProposal`
(`agent_schema.py:374-393`), the only type the LLM gateway may return today (`llm_gateway.py:35`).
The gateway that produces a biography, a briefing or a conversational answer about an entity must, by
construction, be handed a structured view and be able to return **only rendered prose** — never a new
or altered fact. This is the one part of the dossier with a working implementation pattern to copy.

> **P-5. Grounding citations must be emitted by the projector, never returned by the model.** The
> "grounded in" affordance (§6.2) is specified as the player's means of checking prose against
> audited facts. If the model returned the citation set, the model would be attesting to its own
> grounding and the check would be **circular**: a model can cite record IDs it did not use, or that
> do not exist, and the interface would render that attestation with the authority of a verification
> affordance. A claim about which evidence records support a paragraph is a factual assertion of
> exactly the kind ENTITY-ONTOLOGY V-5 forbids the model to make, and P-3 already reserves
> evidence-bearing labels to engine computation.
>
> Therefore: the boundary object hands the model a structured view whose record IDs are **already
> known to the projector**, and the narration return type carries **prose only**. If a future design
> needs the model to indicate which of the supplied records it drew on, that returned set must be
> validated as a **subset of the supplied set**, and any unrecognised ID must **reject the
> narration** rather than be displayed.

### 6.5 Fictional-world disclosure

This subsection exists because the settled B5 decision (18 July 2026) places control **B5-7**
directly on this surface: **the API and the UI must disclose that the active world is fictional.**
It is a distinct obligation from the AI-provenance rule above — P-1 to P-5 separate *engine fact
from generated prose*; B5-7 separates *the whole simulated world from the real one* — and the two
must not be collapsed into a single badge, because a reader who learns a paragraph was written by a
model has learned nothing about whether the minister it describes is a real person.

> **P-6. Every surface that serves entity state must disclose that the active world is fictional.**
> The disclosure must be carried by the **API response** and by the **UI**, not by one of them.
> It must be present on the dossier itself — a dossier is the surface on which a fictional person is
> most easily mistaken for a real one — and it must survive the same test as the provenance badge in
> [§6.2](#62-how-the-two-are-visually-distinguished-specified): a screenshot of a dossier, taken
> alone, must still carry it.
>
> **P-7. The disclosure is a rendering of an enforced fact, never a caption.** The interface must
> display it because the run was loaded under `world_mode: fictional` and the loader **failed
> closed** without it (control B5-2), not because an interface author wrote the words. Control B5-8
> makes technical enforcement mandatory and disclosure supplementary: a disclosure rendered without
> the enforcement behind it would assert a property nothing checks, which is this project's
> defining defect in miniature.

**Nothing here exists, and the gap is larger than a missing component.** There is no UI at all
([§2](#2-what-exists-today)), no endpoint that serves entity state, no `world_mode` field, no
scenario schema to declare one in, and no loader validation. The demo's `fiction_disclaimer`
(`scaffold/scenarios/kestral-strait.json:7`) is the nearest existing artefact and is read by no
code — it is a string in a file, not a control. P-6 and P-7 are requirements on a future interface.

**Where this document stops.** P-6 states that the disclosure must be present and where; it
deliberately does **not** specify its wording, placement or visual treatment, which belong to the
visual-system track ([`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:121-123`)) and are raised alongside the
provenance visual language in [§13](#13-open-questions) Q4. Nor does it specify what the loader
checks or where the check lives — that is [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md)
§12 Q-H, an open owner decision.

---

## 7. The ten person dossier sections

The source record lists ten sections for a person (lines 171-182). Each is specified below with:
what it shows; which underlying model supplies it; how role-based visibility filters it; and —
because this document is bound by the causal-value discipline just like the world-model documents —
whether the section feeds a simulation mechanism or is presentation and explainability only. That
last column is answered honestly and is summarised again in [§12](#12-the-causal-value-test-applied-to-this-document).

**A framing point that applies to the whole table.** The dossier **introduces no new authoritative
attributes.** Every field it shows must trace to a field specified in one of the world-model
documents, and *that* model carries the causal justification for the field's existence. The dossier's
own honesty obligation is therefore inverted relative to the world-model documents: it must never
*invent* a field to display, and any tab content that does not trace to a named underlying attribute
is fake depth and must be struck.

### 7.1 The ten sections

| # | Section | What it shows | Underlying model (supplier) | Role-based filtering | Feeds a mechanism, or presentation? |
|---|---|---|---|---|---|
| 1 | **Overview** | Role, location, status, portrait, current relevance | Base entity + current-state block ([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §6); role via `occupies_role_in`; portrait ref (§10) | Location/status may be Restricted per role; relevance ranking is the player's own | **Presentation.** Relevance is a UX salience ranking, not a state change. Portrait feeds no mechanism (§10). |
| 2 | **Biography** | Life history and career, as readable prose | [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md) structured life-history records, rendered via the LLM boundary (§6) | Sensitive history (e.g. a disciplinary record) may be Restricted or Reported per role | **Both.** The *narration* is presentation; the *structured life-history attributes* must feed decision probabilities in PERSON-MODEL. Narration here is subject to the **P-4 pre-display bias gate** ([§6.1](#61-the-rule)) — this is the tab most exposed to stereotyped inference from truthful identity fields. |
| 3 | **Motivations** | Goals, fears, values, pressures | PERSON-MODEL psychology and worldview (objectives, aspirations, fears, values); current pressures from current-state | Private motivations may show only as Assessed to observers who cannot see self-understanding | **Mechanism.** Objectives and their priorities must feed the individual decision model that produces `ActionProposal`s (no individual decision model exists today — `InstitutionalAgent.step` asks the stub gateway for a canned action from a fixed role table, `llm_gateway.py:41-51`). |
| 4 | **Relationships** | Interactive, **directional** social graph | [`../world-model/RELATIONSHIP-GRAPH.md`](../world-model/RELATIONSHIP-GRAPH.md) directional historied edges | An edge is shown only if the role may see it; inbound and outbound filtered separately | **Mechanism.** Edges must feed influence propagation and decision inputs (no influence propagation over entity edges exists today — `Relationship` is instantiated nowhere, `agent_schema.py:190-200`, and `MicroAgent.relationships` is populated for no demo agent). Asymmetry is the point: A→B may be visible while B→A is not. |
| 5 | **Beliefs and knowledge** | What the entity believes, and **why** | [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md); the "why" is observation provenance | The entity's *true* beliefs may differ from its public position; role decides which the player sees | **Mechanism, provisional.** Beliefs must feed the entity's own decisions on incomplete information (V-3 — **provisional, gated on ontology owner decision Q-R**, see §4.3). No entity belief model exists today; cohort belief is a one-way decay of a single scalar. The "why" (evidence) **depends on P0.6.** |
| 6 | **Activity** | Recent movements, communications, decisions | Event-sourced history ([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §6, `history_ref`) | Each activity item filtered by the visibility of the underlying event | **Presentation.** A read of the event log. The underlying events drive state; the *tab* changes nothing. **Depends on P0.6.** |
| 7 | **Resources and capabilities** | What the entity can actually do | PERSON-MODEL capabilities + resource ledger | Financial and clearance detail commonly Restricted to most roles | **Mechanism.** Capabilities and resources feed action feasibility and pricing (the cost/cooldown mechanism the engine currently lacks, audit §4.2). |
| 8 | **Public perception** | Sentiment by community, country or platform | The **public profile** view + per-community belief/adoption ([`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md); `Narrative.adoption_by_cohort`, `agent_schema.py:272-274`) | Public by definition; a role may additionally see private reputation | **Presentation, pending Q-R.** This tab renders the **public profile** view, which the ontology records as **unresolved**: it is defined as observer-independent, so "V-3 admits no path by which a mechanism may read it into a state change. Its only unambiguous reader is presentation… It must not be implemented before Q-R is taken, and it must not be described as causal in the interim" (ENTITY-ONTOLOGY §13). The causal half of this row — reputation feeding legitimacy/decision mechanisms — is **conditional on resolution (a) of Q-R** and must not be assumed. Per-community belief aggregation is separately supplied by POPULATION-FIDELITY. |
| 9 | **Intelligence assessment** | Confidence, sources, contradictions | The player-intelligence projector (§4.3): confidence labels, evidence links, `contradicted_by` | This tab **is** the role filter made visible | **Presentation/explainability.** It renders the projection; it changes no state. **Depends on P0.6** for evidence. |
| 10 | **Timeline** | Every important interaction and state-changing event, causally linked | Event-sourced history with `causal_parents` (`agent_schema.py:224`) and the eight-question record | Each event filtered by visibility; causal parents the role cannot see appear as Restricted links | **Presentation/explainability.** The charter's eight-question surface (§7.3). **Depends on P0.6.** |

### 7.2 The sections that carry the most design weight

- **Relationships (4)** must be **directional and historied**, because the source record requires
  that "A trusts B" does not imply "B trusts A" (line 77). The interactive graph must therefore show
  inbound and outbound edges as distinct, must be able to render one direction while withholding the
  other under role filtering, and must expose an edge's history (shared history, last interaction,
  unresolved events) so that the "how did these two come to distrust one another" question (§9) is
  answerable by clicking the edge. The existing structures cannot support this — `Relationship`
  (`agent_schema.py:190-200`) carries one shared trust and no history, and `MicroAgent.relationships`
  (`agent_schema.py:175-177`) is a single scalar per counterpart — which is why
  [`../world-model/RELATIONSHIP-GRAPH.md`](../world-model/RELATIONSHIP-GRAPH.md) specifies a
  replacement.

- **Beliefs and knowledge (5)** is specified as the tab on which "what does this person believe that
  is factually wrong" must be answerable. It must show the entity's belief **and**, for a role with
  sufficient access, the
  authoritative reality it diverges from — never silently reconciling the two. This is the direct
  interface expression of the four-view model and it is unbuildable until the belief model and P0.6
  exist.

  **"A role with sufficient access" names an owner decision that has not been taken** (citation
  added 19 July 2026; the conditional was previously stated with no reference to what gates it).
  The query is specified in
  [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md)
  §4.6, whose design rules state that it "must **not** be automatically available to a player" and
  that "no player role may be granted a direct read of `truth_value` without an explicit owner
  decision recorded against the role model". Whether any player role ever receives such access is
  that document's **Part 9 question 4**, open. Until it is taken, no role satisfies this condition,
  and this bullet must not be read as asserting that one does. **No agent may take it**
  ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)).

- **Intelligence assessment (9)** is the section specified to define the dossier as an intelligence
  product rather than an encyclopaedia. It must surface the confidence labels, the sources behind each,
  and the contradictions between them, and it must make **Unknown** and **Disputed** first-class,
  visible content rather than gaps.

### 7.3 The eight-question standard on the Timeline

The charter's eight questions ([`../../CHARTER.md`](../../CHARTER.md):118-127) apply to every entity
state change exactly as to any other. The Timeline tab is where they are surfaced to the player. For
a selected event, the tab must be able to show: what happened, what caused it (its `causal_parents`),
which rule or mechanism applied, which actors reacted, what assumptions were used, what uncertainty
existed, what alternative outcomes were possible, and what future options changed. The existing
intended shape — `Outcome.explanation_trace`, documented as "Ordered causal steps (data, not LLM
prose)" (`agent_schema.py:363-365`) — is a `list[str]` today and cannot answer "which rule applied"
or "what alternatives were possible" in machine-readable form, so the Timeline depends on that trace
becoming structured records, which depends on P0.6.

---

## 8. How the tabs differ for an organisation, a business and a state

The source record says only that "for a business, country or organisation, the tabs would change
appropriately" (line 184). This document specifies the changes, because the differences are where the
source record's structural rules — "an organisation should not behave like one person" (line 104),
"the country should not be a single agent" (lines 121-122) — become visible to the player.

The rule for adapting the tab set: **a tab must map onto a capability the entity type actually
carries** ([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §5). A community
does not `act`, so a community dossier has no Motivations-as-individual-goals tab; a state is a
composition, so a state dossier is a portal, not a single profile.

### 8.1 Organisation

Person tabs that change, and why:

| Person tab | Becomes, for an organisation | Why |
|---|---|---|
| Biography | **Founding history and institutional memory** | Organisations have a founding, a culture and an institutional memory, not a childhood (source record 99-102). **Two supplier dispositions bind this tab.** (a) [`../world-model/ORGANISATION-MODEL.md`](../world-model/ORGANISATION-MODEL.md) §15-R1 strikes the founding *narrative* as state: "Keep the seeds; **strike the narrative field**. Generate founding prose from the seeds at display time via the LLM and never store it as state." This tab must therefore render founding prose at display time only — **writing generated prose back onto the entity would violate D-1** ([§3](#3-the-governing-idea-in-technical-form)), which names this exact temptation. (b) §15-R6 makes institutional memory **conditional on P0.6** — "Keep, sequenced after P0.6. Must not be built earlier." |
| Motivations | **Internal factions and decision process** | The load-bearing change. An organisation's stance must be shown as **emerging from competing internal pressures**, not as one set of goals. The shipping-company example (source record 106-111) — chief executive, operations, insurers, lawyers, investors, unions, regional managers — must be renderable as distinct internal positions that resolve into an action. Supplied by [`../world-model/ORGANISATION-MODEL.md`](../world-model/ORGANISATION-MODEL.md). |
| Resources and capabilities | **Assets, funding, capabilities, legal exposure** | Organisational capability and legal exposure replace personal capability. |
| — (new) | **Leadership and membership** | Who leads, who belongs, via `occupies_role_in` and `member_of` relations. |
| — (new) | **Cohesion and morale** | The organisation's internal cohesion — the analogue of a person's stress — which conditions how reliably it can act. |

Public perception, Relationships, Activity, Intelligence assessment and Timeline carry over with the
same meaning.

### 8.2 Business

A business is a commercially-governed organisation
([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §4.2). It carries every
organisation tab and adds commercial ones:

- **Ownership and shareholders** — who controls it, via directional edges.
- **Financials** — revenue sources, debt, market confidence.
- **Supply chain and facilities** — physical dependencies and exposure.
- **Labour relations** — workforce and unions as internal factions.
- **Exposure** — regulatory, insurance and operational exposure. **CHARTER constraint:** these must
  be fictional exposures of a fictional business ([`../../CHARTER.md`](../../CHARTER.md):137); the
  charter forbids real operational vulnerabilities, and the dossier must not become a place where a
  real one could be authored and surfaced.

The business tabs are what make "who benefits financially if the strait closes" (§9) answerable: the
question is a query over business exposure, and the answer lives on these tabs.

### 8.3 State (country)

A state is **not one agent** (source record 121-122); it is a composition
([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §4.4). Its dossier is
therefore specified as a **portal into constituent entities**, not a single-subject profile:

| State dossier section | What it shows | Supplier |
|---|---|---|
| **National indicators** | The macro numbers, shown explicitly as a **derived aggregate view** over lower-tier entities, not as a primary record | The demoted `MacroState` (`macro_schema.py:73-87`) recast as an aggregate — see [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §4.4 |
| **Government and institutions** | The governing organisations and the institutions that constrain them | ORGANISATION-MODEL; institution entities |
| **Political system and factions** | Parties, coalitions and their fracture lines | ORGANISATION-MODEL internal factions |
| **Population groups** | The communities, each a dossier of its own | [`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md) |
| **Economy and industries** | Major businesses and sectors | BUSINESS entities |
| **Media environment** | Outlets, reach and per-community trust | BELIEF-AND-KNOWLEDGE-MODEL; community media exposure |
| **Alliances and rivalries** | Relationships to other states, directional | RELATIONSHIP-GRAPH |
| **Elite cohesion and state capacity** | How unified the elite is and how much the state can actually do | ORGANISATION-MODEL cohesion; capability |
| **Historical grievances** | Structured grievance records with onset, cause and parties, biasing precedent priors | `historical_grievances` → `M-MEM` ([`../world-model/ORGANISATION-MODEL.md`](../world-model/ORGANISATION-MODEL.md):1386, §13 row 17). **Conditional on P0.6** (§15-R7) — grievance records are event-sourced and cannot exist before P0.6. |
| **National myths** | — | **No supplier and no mechanism.** ORGANISATION-MODEL §13 row 18 records "**No mechanism specified**", and §15-R5 proposes "**Strike, or merge** into `historical_grievances` + narrative-credibility priors. Owner decision." The belief-model candidate "is not specified there yet". **Active strike candidate**; listed in [§12.2](#122-items-i-could-not-map-to-a-simulation-mechanism), not claimed as a tab. |

The defining requirement of the state dossier is that it must make **internal disagreement visible**.
A player must be able to see that the government, the public, the military, the courts, businesses and
regional authorities hold different positions on the same crisis — because they do, and because a
single national number that hides that is the "country as one agent" the source record rejects.

---

## 9. The questions the dossier must answer

The source record lists seven questions a profile must support (lines 186-189), plus the financial
one it raises separately. For each, this document names the tab, the underlying model, the query and
the dependency. **Several of these are also targeting queries. B5 / P0.8 is decided, so they are
bounded by its controls rather than deferred pending it — and none of those controls is built** —
see [§9.9](#99-the-dual-use-warning-that-runs-through-this-section).

### 9.1 "Why does this minister oppose the operation?"

- **Tab:** Motivations (3), supported by Beliefs (5) and Relationships (4).
- **Model:** PERSON-MODEL objectives and psychology; BELIEF-AND-KNOWLEDGE-MODEL.
- **Query:** the decision model's explanation trace for the entity's stance — which high-priority
  objective the operation threatens, which belief makes it look costly, which relationship pressures
  push against it. Worked on the demo: `min-defence-oduya` (`kestral-strait.json:266`) holds
  `avoid_blame_for_shipping_losses` at priority 0.8 (`:272`) and believes
  `reliability_of_western_ally` is only 0.44 (`:277`); a stance against a Western-dependent operation
  is explainable from those recorded values plus the `procurement_law_18mo_minimum` constraint
  (`:292`), not from prose.
- **Depends on:** the decision model producing a structured explanation trace (P0.6 for the record
  shape; the belief model for the reasoning).

### 9.2 "Who influences this chief executive?"

- **Tab:** Relationships (4).
- **Model:** RELATIONSHIP-GRAPH.
- **Query:** the **inbound** edges terminating on the executive, ranked by an influence measure
  (trust, dependency, leverage). Directionality is essential: inbound influence is a different set
  from outbound, and the graph must not symmetrise them as the current undirected diffusion graph
  does (`diffusion.py:24`).
- **Depends on:** directional edges (RELATIONSHIP-GRAPH), which replace the current scalar map.

### 9.3 "Which communities trust this media outlet?"

- **Tab:** Public perception (8) on the outlet's dossier.
- **Model:** BELIEF-AND-KNOWLEDGE-MODEL (per-community trust in the outlet) + community entities
  ([`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md)).
- **Query:** over community entities, their trust edge toward the outlet entity. **Note a current
  gap:** `MediaExposure` (`agent_schema.py:42-53`) carries per-channel *reach* but **no
  trust-in-channel term**, so today's schema literally cannot answer this — the belief model must add
  a trust term for the question to be answerable. This is flagged in
  [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §10.1 as a restructure.

### 9.4 "What caused this organisation to radicalise?"

- **Tab:** Timeline (10) on the organisation's dossier.
- **Model:** event-sourced history with `causal_parents`; ORGANISATION-MODEL strategy/culture state.
- **Query:** walk the causal chain backwards over the organisation's ideology/strategy state changes,
  each event answering the eight questions. "Radicalise" is a trajectory of a modelled attribute, not
  a label — a trajectory that cannot be reconstructed from recorded events is flavour text and, per
  [`../../CHARTER.md`](../../CHARTER.md):129-130, must not be presented as a cause.
- **Depends on:** P0.6 (there is no event-sourced history today; the engine appends raw dicts and
  discards `causal_parents`, audit §6.13).

### 9.5 "Who benefits financially if the strait closes?"

- **Tab:** a **what-if query** surfaced across Business dossiers (8.2) and Public perception (8).
- **Model:** BUSINESS exposure (revenue sources, supply chain, competitors, insurance) + the
  cross-tier economic channel. The cohort analogue already exists as a declared-but-unread field,
  `income_sensitivity_to_shipping_disruption` (`agent_schema.py:36`), which is the single explicit
  cross-tier channel in the schema layer and is read by no code (audit §4.1).
- **Query:** entities whose modelled financial outcome is *negatively* correlated with
  `shipping_throughput_pct_of_baseline` — competitors on alternative routes, insurers repricing risk,
  holders of substitute capacity. This is a genuine economic-exposure query, not prose.
- **Depends on:** the cross-tier causal channel actually being wired (P0.5) and business entities
  existing (ORGANISATION-MODEL). **Dual-use flag:** this is also a "who has motive" query — see §9.9.

### 9.6 "What does this person believe that is factually wrong?"

- **Tab:** Beliefs and knowledge (5).
- **Model:** the four-view model — the entity's belief (authoritative reality's belief record) versus
  the authoritative reality of the referenced fact.
- **Query:** attributes where the entity's held value diverges from authoritative reality, shown
  **only** to a role permitted to see the reality; to other roles the divergence itself may be
  Restricted or Unknown. The query is specified — as a pure function over authoritative state,
  computed on read and never stored — in
  [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md)
  §4.6, which also excludes evaluative and `indeterminate` propositions by construction. **"A role
  permitted to see the reality" presupposes a decision nobody has taken**: §4.6 rules the function
  available to the designer and to tooling, states it "must **not** be automatically available to a
  player", and requires "an explicit owner decision recorded against the role model" before any
  player role gets a direct read of `truth_value`. That decision is that document's **Part 9
  question 4**. It is open, and this document does not take it.
- **Depends on:** the four-view split (P0.4 to make it authoritative; the belief model to populate
  it); **and an unmade owner decision — whether any player role may read `truth_value` directly
  ([`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md)
  §4.6 and Part 9 question 4)**, without which the query has no player-facing form at all. This
  question has **no attachment point today** — every entity holds exactly one copy of the truth
  (audit; [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §8).

### 9.7 "How did these two individuals come to distrust one another?"

- **Tab:** Relationships (4) — the specific edge, opened.
- **Model:** RELATIONSHIP-GRAPH edge history (shared history, last interaction, unresolved events) +
  the event log.
- **Query:** the ordered events on the directed edge(s) between the two, showing where trust moved
  and what moved it. Because relationships are directional, the answer may be asymmetric: A came to
  distrust B for reasons that are not the reasons B distrusts A.
- **Depends on:** historied directional edges (RELATIONSHIP-GRAPH) and P0.6.

### 9.8 Summary table

| Question | Tab | Model | Hard dependency |
|---|---|---|---|
| Why does this minister oppose the operation? | Motivations | PERSON + BELIEF | P0.6 (trace) |
| Who influences this chief executive? | Relationships | RELATIONSHIP-GRAPH | directional edges |
| Which communities trust this media outlet? | Public perception | BELIEF + community | trust-in-channel term (missing) |
| What caused this organisation to radicalise? | Timeline | events + ORGANISATION | P0.6 |
| Who benefits financially if the strait closes? | Business what-if | BUSINESS + cross-tier channel | P0.5; **B5 controls 1, 2, 4, 5, 7 — all unbuilt** (§9.9) |
| What does this person believe that is wrong? | Beliefs and knowledge | four-view model | P0.4; belief model; **unmade role-grant decision** (BELIEF §4.6, Part 9 q4 — §9.6) |
| How did these two come to distrust one another? | Relationships (edge) | edge history + events | P0.6 |

### 9.9 The dual-use warning that runs through this section

Several of these questions are, in a different framing, **targeting questions**. "Which communities
trust this media outlet", "who benefits financially if the strait closes" and — most sharply — the
per-community grievance and susceptibility a campaign could exploit are the exact inputs an influence
operation needs. The demo scenario already contains the operational half of that pairing: a hidden
campaign with `target_cohorts` and an `existing_grievance` it exploits (`kestral-strait.json:389-418`,
`existing_grievance` at `:394`), matched to the audience-segmentation attributes on the cohorts it
targets.

The dossier is the surface on which this coupling becomes most concrete, because it turns aggregate
audience attributes into **individually queryable** intelligence about named people and named
communities. That makes the dual-use surface of the dossier **strictly larger** than the one blocker
B5 / P0.8 was originally raised on.

**B5 is decided, and the queries above are bounded by it rather than waiting on it.** The founder
settled B5 on 18 July 2026. It must not be described anywhere in this document as an open decision.
Four of the eight controls bear on the queries in this section, and **not one of them exists in
code**:

| Control | What it requires of this section |
|---|---|
| **B5-1 / B5-2** | These queries may run only inside a world loaded with `world_mode: fictional`, with the loader failing closed when the field is absent. A dossier served from a world that did not pass that gate must not exist. |
| **B5-4** | The people, organisations and communities these queries range over must be fictional. Real persons, organisations and political populations may not be influence-target entities, and a per-community grievance-and-susceptibility query over a real population is exactly the prohibited use. |
| **B5-5** | No query, ranking or filter the dossier offers may use a protected characteristic as an **optimisation criterion** for persuasion or manipulation. Permitted non-sensitive factors — geography, institutional affiliation, economic exposure, political behaviour, media consumption — remain available where the fictional scenario justifies them. This is the constraint that bites hardest on §9.3 ("which communities trust this outlet") and §9.5 ("who benefits financially"). |
| **B5-7** | Every response serving these queries must disclose that the active world is fictional ([§6.5](#65-fictional-world-disclosure)). |

Because **B5-8** makes technical enforcement mandatory and disclosure supplementary, none of these
can be discharged by a caption on a screen or a paragraph in this document. The full enumeration is
in [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §10.4 and
[`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md) Part 7.

**Two things the decision does not settle, recorded rather than papered over.** Neither is resolved
here and no agent may resolve them. First, a dossier query filtering on a *permitted* factor that
correlates strongly with a protected characteristic — residence where segregation is modelled,
media consumption where language predicts channel — can approximate a prohibited optimisation
without ever reading a protected field. Second, the distinction between an *intelligence* query the
product exists to support and a *targeting* query B5-5 prohibits is, for several of the questions
above, a matter of the asker's intent rather than of the query's shape. How sensitive-identity
queries may be phrased, filtered and detected is deferred to
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) and raised
as [§13](#13-open-questions) Q6.

---

## 10. Portrait progression

### 10.1 A staged roadmap, not a commitment

The source record gives a sensible progression for faces (lines 194-199). This document records it as
a **staged roadmap** — each stage is a defensible stopping point, and nothing here commits to
reaching a later stage.

| Stage | What it is | What it needs | Stability guarantee |
|---|---|---|---|
| **0. Abstract avatars** | A deterministic geometric mark derived from `entity_id` | Nothing beyond the entity id — no asset store, no generation | Identical every session by construction (a pure function of the id) |
| **1. Consistent illustrated portraits** | A fixed curated library, assigned deterministically | A portrait library and a deterministic assignment | Stable while the library and assignment are versioned |
| **2. Generated fictional faces with expressions** | Faces generated once from a stable entity specification, with expression/context states | An asset store, a generator, and named RNG substreams | Stable **only** if generation is keyed on a stable substream (see below) |
| **3. Contextual visual change** | Sophisticated change for age, injury, role and circumstance, derived from current state | All of stage 2 plus a mapping from current-state to visual variant | Base identity stable; variants derived, not re-drawn |

### 10.2 The non-negotiable constraints on every stage

From the source record (lines 201-208):

- **A portrait must not change between sessions.** The same entity, in the same run replayed, must
  show the same face. At stages 2 and 3 this is impossible without named RNG substreams
  ([§11](#11-hard-prerequisites--none-of-which-is-met-today);
  [`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md) §7): on the single
  shared stream, the draws a face receives depend on global draw order, so the same person generated
  at a different tick gets a different face.
- **Generated once from a stable entity specification, stored and versioned, with provenance and
  generation metadata.**
- **Clearly fictional; not derived from or intentionally resembling a real person.** What *enforces*
  this is unresolved and is a safety matter, not an interface one — deferred to
  [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md). **The
  settled B5 decision raises its priority without answering it:** control B5-4 requires that real
  persons cannot be entities, a portrait resembling a real person is one route by which a nominally
  fictional entity acquires a real likeness, and control B5-8 forbids discharging the requirement
  with a stated intention. A rendered portrait is also a surface B5-7's fictional-world disclosure
  must reach ([§6.5](#65-fictional-world-disclosure)), since a face is the element most readily
  screenshotted out of context.
- **Consistent with age, geography, family resemblance and life history** — i.e. generated from the
  same structured identity that drives behaviour, not independently.

### 10.3 The honest status of portraits

**A portrait feeds no simulation mechanism.** The source record itself classifies portraits as
presentation: "Portraits are presentation. The underlying identity must still be structured data"
(line 208). Portraits are retained in the specification **only** because identity stability requires
them not to change, and they must never be read by any behavioural rule. There is **no asset
reference field anywhere in the schema layer today and no asset store in the project**, so even stage
0 has nothing to attach to yet. Portraits are listed among the items with no causal mechanism in
[§12.2](#122-items-i-could-not-map-to-a-simulation-mechanism), deliberately and visibly.

---

## 11. Hard prerequisites — none of which is met today

Every prerequisite below is currently unmet. They are stated here so the document cannot be mistaken
for something buildable now.

| # | Prerequisite | Owner today | Why this document depends on it |
|---|---|---|---|
| PR-1 | **An authentication / authorisation layer** | Not in Phase 0; audit records IAM as Phase 2 (§7). It is link 5 of the boundary chain ([§3.1](#31-what-this-document-owns-and-what-it-does-not)) and is owned by no document — the observation model explicitly does not own player access control | Role-based visibility ([§4](#4-role-based-visibility)) is the entire premise. Today "player role" has nothing to resolve against. **This is the blocker unique to this document.** *(Amended 19 July 2026:)* building the layer would still not settle **what any role may be granted**. Whether any player role may read `truth_value` directly is [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md) §4.6 and Part 9 question 4, open, and it gates [§7.2](#72-the-sections-that-carry-the-most-design-weight) and [§9.6](#96-what-does-this-person-believe-that-is-factually-wrong). |
| PR-2 | **P0.4 — authoritative-state contract** | Phase 0 ([`../../HANDOFF.md`](../../HANDOFF.md):75) | The dossier renders four views of which only authoritative reality is state. Which view is authoritative, and what is snapshotted, is P0.4's to decide. This document must not assume it. |
| PR-3 | **P0.6 — event, snapshot and replay foundations** | Phase 0 ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:87-88`)) | Activity (6), Timeline (10), the "why" in Beliefs (5) and the evidence in Intelligence assessment (9) all read recorded history and observations. None exists; the engine appends raw dicts and discards `causal_parents` (audit §6.13). These tabs are **unbuildable** until P0.6 lands. |
| PR-4 | **Deterministic randomness isolation** (mechanism unchosen; "named RNG substreams" is one candidate) | **P0.4A** (founder decision, 18 July 2026), between P0.4 and P0.5. *(An earlier draft of this row said "Nobody".)* Not started; its relationship to ADR-007 is an open owner question | D-2 (a dossier consumes zero randomness) and stable portraits at stages 2-3 both require them. Raised in full in [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §7.3 and [`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md) §7. **No agent may adopt this.** |
| PR-5 | **The four-view model with an evidence/observation layer** | Depends on PR-2, PR-3; belief model. *(Amended 19 July 2026, founder ruling 1A: the observation half now has a named owner — [`../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md`](../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md), in which `M-OBS-ACQ` is the sole writer of `Observation`. An earlier draft of this row named no owner for it. It is specified, not built.)* | The player-intelligence projector (§4.3) needs observation records to compute confidence labels. This document consumes those records and does not produce them ([§3.1](#31-what-this-document-owns-and-what-it-does-not) link 3). The truth-vs-belief split has no attachment point today (audit; ontology §8). |
| PR-6 | **The world-model entity schemas** | Backlog. All five now exist in DRAFT, unreviewed; none is implemented | Every tab must bind to a model — PERSON, ORGANISATION, RELATIONSHIP-GRAPH, BELIEF-AND-KNOWLEDGE, POPULATION-FIDELITY. The dossier is specified as a **view over** those; it cannot precede them. None of them is implemented. |
| PR-7 | **B5 / P0.8 — eight required dual-use controls** | **DECIDED** (founder decision, 18 July 2026). **Not an open decision.** The controls are **unbuilt** and no Phase 0 item owns them. | B5 now clears by technical enforcement being implemented and verified, not by a decision, so it is a prerequisite of the same kind as PR-1. Five controls bear on this document: **B5-1/B5-2** (the dossier may exist only inside a fail-closed fictional world), **B5-4** (every entity a dossier renders must be fictional), **B5-5** (no query, ranking or filter may optimise on a protected characteristic), and **B5-7** (the API and UI must disclose that the active world is fictional — [§6.5](#65-fictional-world-disclosure), P-6/P-7). **B5-8** forbids satisfying any of them with wording alone. There is no UI, no entity endpoint, no `world_mode` field and no loader check, so all five are new work. See §9.9. |
| PR-8 | **ENTITY-ONTOLOGY Q-R — how an entity legally reads public information** | Open owner decision (ontology §12, `:1108`) | The ontology records that **V-3 and the public profile do not fit together** (`:608-616`) and rules that "**the view taxonomy must not be implemented until this is taken**". This document's deception mechanism (§4.3 step 4), its Beliefs and Public perception tab claims (§7.1 rows 5, 8) and two §12.1 rows all cite V-3. **Every V-3 citation here is provisional until Q-R is taken.** The public profile "must not be described as causal in the interim" (ontology §13). **Not resolved here, and no agent may resolve it.** |
| PR-9 | **The pre-display bias filter** ([`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) §6.4) | Safety document; unbuilt | P-4 ([§6.1](#61-the-rule)) requires every narration block to pass the prohibited-construction detector **before display**. No detector exists, and the safety document states plainly that it is a heuristic that will miss patterns it does not know. Without it, a biography narrated from truthful identity fields can imply competence or morality while passing every provenance rule in §6. |

**Ordering.** PR-4 sits under everything (it is a determinism property). PR-2 precedes PR-3. PR-6
precedes any tab binding. PR-8 gates the view taxonomy that §4 and the four-view model rest on. PR-1
is the prerequisite unique to this document and is not currently owned by Phase 0. This ordering is a reason to write the specification carefully now; it is **not** a reason
to start building any of it.

---

## 12. The causal-value test applied to this document

The source record names the failure mode this whole project is trying to correct (lines 243-244):
enormous depth that never affects the simulation is **fake depth**. A dossier is unusually exposed to
it, because a dossier is *made of* presentation.

This document's discipline, stated once: **the dossier introduces no new authoritative attributes.**
Every value a tab shows must trace to a field specified in a world-model document, and that document
carries the causal justification for the field. The dossier's job is to *surface* attributes that
already earn their place, filtered by role and labelled by confidence. A tab that shows something
tracing to no underlying attribute is fake depth and must be struck.

That framing makes the dossier's causal honesty **inverted** relative to the world-model documents: a
large fraction of the dossier is legitimately presentation and explainability, and it is legitimate
precisely because it invents nothing. The two lists below make that split explicit rather than
burying it — concealment would be the exact defect this document exists to avoid.

### 12.1 Dossier elements that trace to a simulation mechanism

Each of these surfaces an attribute whose causal justification lives in the cited model. The dossier
does not create the mechanism; it renders its inputs or outputs.

| Dossier element | Section | Mechanism it surfaces (owned by the cited model) |
|---|---|---|
| Motivations: objectives and priorities | 7 (3) | Individual decision model → `ActionProposal` (PERSON-MODEL). *No individual decision model exists today* (`llm_gateway.py:41-51`). |
| Beliefs: the entity's held beliefs | 7 (5) | Decision on incomplete information, V-3 (BELIEF-AND-KNOWLEDGE-MODEL). **Provisional — gated on Q-R** (§4.3). *No entity belief model exists today.* |
| Relationships: directional edges | 7 (4) | Influence propagation; decision inputs (RELATIONSHIP-GRAPH). *No influence propagation over entity edges exists today; `Relationship` is uninstantiated, `agent_schema.py:190-200`.* |
| Resources and capabilities | 7 (7) | Action feasibility and pricing (PERSON/ORGANISATION-MODEL) — the cost/cooldown mechanism the engine currently lacks (audit §4.2). |
| Public perception: per-community belief | 7 (8) | Community belief aggregation, weighted (POPULATION-FIDELITY). **The public-profile view itself is unresolved — ontology §13 forbids describing it as causal until Q-R is taken;** this row is limited to the per-community belief aggregation, which POPULATION-FIDELITY supplies independently. |
| Organisation Motivations: internal factions | 8.1 | Action emerges from competing internal pressures (ORGANISATION-MODEL) |
| Business exposure | 8.2, 9.5 | Cross-tier economic channel (P0.5; `income_sensitivity_to_shipping_disruption`, `agent_schema.py:36`) |
| Structured life-history attributes rendered on Biography | 7 (2) | Biography → behaviour probabilities (PERSON-MODEL) |
| Confidence-label computation **when the observer is a simulated entity** | 5 | The label feeds that entity's belief update and decision (V-3, BELIEF-AND-KNOWLEDGE-MODEL). **Provisional — gated on ontology owner decision Q-R** (§4.3): V-3 as written admits no `ViewKind` for one entity's view of another. The **player-facing** label is *not* in this table; it is presentation, see [§12.2](#122-items-i-could-not-map-to-a-simulation-mechanism). |
| Entity-facing view projection | 4 | The projection an *entity* acts on, which is the specified deception mechanism (V-3). **Provisional — gated on Q-R.** The **player-facing** role filter is *not* in this table; it is presentation, see [§12.2](#122-items-i-could-not-map-to-a-simulation-mechanism). |

### 12.2 Items I could NOT map to a simulation mechanism

Recorded explicitly. **None of these should be built as a behaviour-affecting attribute.** Each is
presentation, explainability or governance, and each is retained (if at all) on that basis alone, for
the owner to confirm or strike. This is the same treatment portraits receive in
[`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md) §10.2, applied to the
interface.

| Item | Section | Honest status |
|---|---|---|
| **The dossier interface as a whole** | all | **No simulation mechanism, by design.** A dossier is a read surface. Per D-1/D-2 it must change no state and consume no randomness. Its value is to the *player's* decisions (out-of-simulation) and, via V-3 — **provisional, gated on ontology owner decision Q-R** (§4.3) — to a *simulated entity's* decisions on its own view. The player-facing rendering itself feeds no mechanism. |
| **Overview "current relevance" ranking** | 7 (1) | **Presentation.** A UX salience score (recent event involvement, relationship centrality) that orders what the player sees. It changes no state and must not. |
| **Portrait (all stages)** | 10 | **No simulation mechanism.** Presentation only (source record line 208). Retained solely so identity stays stable; must never be read by a behavioural rule. No asset field or store exists today. |
| **Portrait provenance and generation metadata** | 10.2 | **No simulation mechanism.** Governance and safety (source record 204-206); justified by the safety guidelines, not by causal value. |
| **AI-generated narration (biography prose, briefing prose, conversational answers)** | 6, 7 (2) | **Presentation by definition, and it must stay that way.** It renders structured views into readable text and may never author or alter a fact (D-3, P-2). The *facts* it renders feed mechanisms; the *prose* feeds none. |
| **Activity feed** | 7 (6) | **Presentation/explainability.** A read of the event log. The events drive state; the tab does not. |
| **Intelligence-assessment tab** | 7 (9) | **Presentation/explainability.** Renders the projection (labels, sources, contradictions). Changes no state. |
| **Timeline tab** | 7 (10) | **Presentation/explainability.** The eight-question surface. It reads recorded causal history; it does not create it. Depends on P0.6 for the structured trace. |
| **Fictional-world disclosure (P-6)** | 6.5 | **No simulation mechanism, and it must never acquire one.** It is a required governance control (B5-7), and it is a *rendering* of an enforced fact, not the enforcement itself: the enforcement is the loader's fail-closed `world_mode` check (B5-2), which is not this document's to build and does not exist. Listing it here is not a downgrade — under B5-8 a disclosure with no enforcement behind it is precisely what does **not** satisfy the control. |
| **Provenance badges and "grounded in" affordances** | 6 | **No behavioural mechanism.** Mandatory under `CHARTER.md:141` and as the guard against a player mistaking prose for fact — but they are interface honesty, not simulation behaviour, and the distinction should stay visible. |
| **Confidence labels, *when the observer is the player*** | 5, 5.2 | **No simulation mechanism**, per [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) §13, quoted verbatim: "When the observer is a simulated entity, the labels feed that entity's belief update and decision (V-3) — a real mechanism. When the observer is the **player**, the label is a display property of an intelligence product and changes no simulation state… the specification must **not** claim the player-facing labels are causal. They are honest presentation of derived state. **Any future feature that lets a player-facing label alter state would violate V-2 and V-3.**" The dossier is player-facing by definition ([§1](#1-plain-english-layer)), so the labels it renders sit **here**, not in §12.1. Only the simulated-entity-observer computation is a mechanism (§12.1), and that is itself provisional on Q-R. The chip's visual treatment is likewise presentation. |
| **Player-facing role-based visibility filtering** | 4, 4.3 | **Presentation.** `project_player_view` filters what the *player* may see; it changes no simulation state. The entity-facing projection is the mechanism claim (§12.1) and is gated on Q-R. |
| **The standalone public-profile view** | 7 (8), 8 | **Unresolved — ontology owner decision Q-R.** ENTITY-ONTOLOGY §13: "Its only unambiguous reader is presentation… It must not be implemented before Q-R is taken, and it must not be described as causal in the interim." Recorded here rather than in §12.1 for exactly that reason. |
| **National myths (state dossier)** | 8.3 | **No mechanism specified.** ORGANISATION-MODEL §13 row 18 and §15-R5: "**Strike, or merge** into `historical_grievances` + narrative-credibility priors. Owner decision." **Active strike candidate** — must not be built as a behaviour-affecting attribute, and must not be presented as a tab with a supplier it does not have. |
| **"Alternative outcomes" shown on the Timeline** | 7.3 | **Mechanism unproven.** Required by `CHARTER.md` Q7. Whether the recorded counterfactual set ever feeds a later mechanism depends on the belief model, which is unwritten. Currently explainability only. |

The size of §12.2 is expected and correct. A dossier *should* be mostly presentation; the test it must
pass is not "does the tab change the simulation" but "does every value the tab shows trace to an
attribute that earns its place elsewhere." Where the answer is no, the element is struck.

---

## 13. Open questions

Drafted, not resolved. AI agents may not answer these ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)).

**Q1 — The authorisation layer.** Role-based visibility is the dossier's whole premise and there is
no auth layer of any kind (audit §7). Who owns building it, and does the dossier wait on the Phase 2
IAM work or on something earlier? Until it exists, none of [§4](#4-role-based-visibility) has a
subject.

**Q2 — Player role model.** What is the set of player roles, and is a role a fixed seat (prime
minister, journalist, business leader) or a configurable clearance profile? The source record gives
three examples but not a model. Visibility rules cannot be authored until the role set is decided.

**Q3 — Where do confidence labels come from before P0.6?** The labels must be computed from
observation records that do not exist until P0.6. Is there an interim in which the dossier renders
only `Confirmed`/`Unknown` from authoritative reality directly, clearly marked as pre-evidence, or
does the whole player-intelligence view wait on P0.6?

**Q4 — Provenance visual language.** P-1/P-2 require engine fact and AI narration to be
distinguishable at a glance, but this document deliberately does not prescribe the visual design —
that belongs to the visual-system track ([`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:121-123`)). Who owns
reconciling the two so the provenance distinction is not lost in visual styling?

**Q5 — Portrait stage and asset store.** Which portrait stage (§10) is the target, and does an asset
store, a generator and an asset-reference field get built at all? All three are absent today, and
stages 2-3 are gated on named RNG substreams and on the safety decision about "clearly fictional".

**Q6 — B5 / P0.8 is DECIDED; the residual questions are about queries, not policy.** B5 was settled
on 18 July 2026 and is **not re-opened here**. The earlier form of this question — should the
queryable intelligence surface be held coarse *until B5 is decided*? — is spent. Three things the
decision does not answer, each an owner decision:

- **(a) What separates a permitted intelligence query from a prohibited targeting query**, when
  several of §9's questions have the same shape and differ only in the asker's purpose? B5-5
  prohibits optimising on protected characteristics, which is a property of a ranking function, not
  of a question a player types.
- **(b) What detects a query filtering on a permitted factor that is a close proxy for a protected
  characteristic** — residence where segregation is modelled, media consumption where language
  predicts channel (§9.9)?
- **(c) Where does the B5-7 disclosure live in the response contract** — a field on every entity
  payload, a run-level attribute the client must render, or both — and who owns failing a client
  that does not render it? P-6 requires the API *and* the UI to carry it; nothing specifies how the
  API compels the second.

**Q7 — State-dossier depth.** A state dossier is a portal into potentially hundreds of constituent
entities (§8.3). How deep does it go by default, and how is the "make internal disagreement visible"
requirement reconciled with not overwhelming the player? This is a design question the visual-system
track must answer alongside this one.

**Q8 — Does the self-understanding view get its own tab, or is it folded into Beliefs?** The
four-view model treats self-understanding as distinct (source record 151-152). Whether it earns a
dedicated surface, or is shown as a lens on the Beliefs and Motivations tabs, is unresolved and
touches how "what does this person believe that is wrong" (§9.6) is presented.

**Q9 — ENTITY-ONTOLOGY Q-R, and what this document must do until it is taken.** Not resolved here.
The ontology records that V-3 and the public profile do not fit together (`:608-616`), that
`ViewKind` has no kind for one entity's view of another, and that "the view taxonomy must not be
implemented until this is taken" (`:1108`). This document's central deception mechanism and two of
its §12.1 mechanism rows cite V-3. Until Q-R is taken: should the Public perception tab be specified
as **presentation-only**, and the Beliefs tab's mechanism claim held in abeyance — or is the
specification allowed to stand provisionally on resolution (a), clearly marked, as it currently
does? The owner should also confirm that the provisional markings added throughout this document are
the right treatment rather than deferring the affected sections entirely.

**Q10 — National myths on the state dossier.** ORGANISATION-MODEL §15-R5 records this as "**Strike,
or merge**… Owner decision", with no mechanism specified and the belief-model candidate unspecified in
[`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md) as that
document now stands.
This document has moved it out of the state tab list and into §12.2 as a strike candidate. Should it
be struck outright, merged into `historical_grievances`, or kept pending a belief-model
specification that gives it a mechanism?

**Q11 — May any player role be shown authoritative reality, and if so which?** *(Recorded 19 July
2026. This decision was always required by [§7.2](#72-the-sections-that-carry-the-most-design-weight)
and [§9.6](#96-what-does-this-person-believe-that-is-factually-wrong), which each made a feature
conditional on "a role with sufficient access" without naming what grants it. The omission was a
documentation gap; recording it here restores this document's own rule that every point requiring a
human choice appears in §13. Nothing about the specified behaviour changes.)* The decision is
[`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md)
**Part 9 question 4**, whose §4.6 requires "an explicit owner decision recorded against the role
model" before any player role receives a direct read of `truth_value`, on the ground that granting it
collapses the intelligence product into the omniscient encyclopaedia the source record rejects
(`:165`). The founder position of 19 July 2026 is that authoritative reality exists internally, that
players ordinarily receive role-, access-, evidence- and confidence-filtered projections, that there
is no automatic omniscient browsing, and that **whether any privileged role may receive fields
equivalent to authoritative reality remains an explicit later owner decision**. A clearance-gated
projection must not be described as a raw ground-truth read. This question is therefore **owned by
the belief model and duplicated here only as a pointer** — it must be answered once, there, not twice.
It interacts with Q2 (what the role set is) and Q8 (whether self-understanding gets its own surface).
**Not resolved here. No agent may resolve it.**

---

## 14. Related documents

**Source and governing records.**

- [`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md)
  — the source record. Verbatim founder requirement. Where this document disagrees with it, this
  document is wrong. The ten dossier sections (lines 171-182), the four views (145-165), the seven
  questions (186-189), the portrait progression (194-208) and the intelligence-product framing (165)
  are all specified there.
- [`../../CHARTER.md`](../../CHARTER.md) — non-negotiable. The provenance rule (`:141`), the
  eight-question standard (`:118-127`) and the fictional-only constraint (`:137`) all bind this
  document.
- [`../../HANDOFF.md`](../../HANDOFF.md) — Phase 0 order, standing constraints, backlog disposition.
- [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) and
  [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) — the CLOSED
  audit. Not to be re-opened; cited here as evidence only. §6.49 (provenance gap), §6.50 (CORS), §7
  (no IAM), §4.1 (dead cross-tier channel), §6.13 (`causal_parents` discarded) bear directly on this
  document.

**Companion specifications this dossier is a view over.** Some may not yet be written.

- [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) — the four-view model
  (§8), the view-projection mechanism (§9.2) and the visibility-versus-confidence separation (§8.4)
  that this document renders. The dossier is the interface expression of that ontology.
- [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md) — supplies Biography (2),
  Motivations (3), Resources and capabilities (7).
- [`../world-model/ORGANISATION-MODEL.md`](../world-model/ORGANISATION-MODEL.md) — supplies the
  organisation, business and state tab sets (§8), including internal factions and decision emergence.
- [`../world-model/RELATIONSHIP-GRAPH.md`](../world-model/RELATIONSHIP-GRAPH.md) — supplies the
  Relationships tab (4) and its directional, historied, asymmetric edges.
- [`../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md`](../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md)
  — **owns observation and perception** (DRAFT, 19 July 2026), per founder decision 1A. It owns
  observation opportunity, sensor and source access, direct versus mediated observation,
  visibility, range, latency and degradation, source attribution, observation confidence,
  observation events, and the transformation of a world event into an entity-specific observation
  (`M-OBS-EXP`, `M-OBS-ACQ`, `M-OBS-ATTR`, `M-OBS-SURF`). This document owns **dossier rendering
  only** and is the last link of the chain in [§3.1](#31-what-this-document-owns-and-what-it-does-not).
  Its invariants **O-1** and **O-4** restate this document's **D-2** and **D-1** in mechanism terms,
  and **O-2** — reading a projection never creates an observation — binds every read path this
  document specifies. `M12 OBSERVABILITY` is superseded there; its earlier partial assignment to this
  document is withdrawn.
- [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md) —
  supplies Beliefs and knowledge (5), the "why", and the "what does this person believe that is
  wrong" question (§4.6). It owns the **consumption** of observations — belief updating (§4.5),
  knowledge storage and confidence labelling (§4.7) — not their production. Its **Part 9 question
  4** is the open owner decision gating [§7.2](#72-the-sections-that-carry-the-most-design-weight),
  [§9.6](#96-what-does-this-person-believe-that-is-factually-wrong) and [§13](#13-open-questions) Q11.
- [`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md) — supplies Public
  perception (8) and the community entities the state dossier is a portal into; its §10.2 is the model
  for this document's [§12.2](#122-items-i-could-not-map-to-a-simulation-mechanism).
- [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) — governs
  how sensitive-identity attributes may be queried and displayed, and how "clearly fictional" portraits
  are enforced. Its §6.4 prohibited-construction detector and §7.2 prompt constraints are a **hard
  pre-display gate on every narration block this dossier renders** (P-4, [§6.1](#61-the-rule); PR-9),
  not merely a query-phrasing reference: its §7.3 places that obligation on this surface explicitly.
  B5 / P0.8 is **decided** (18 July 2026) and is not re-opened by this document; what is deferred to
  the safety guidelines is how sensitive-identity queries may be phrased and filtered, and the
  proxy-detection problem the decision does not answer (§9.9, §13 Q6).

---

**End of specification. Nothing described above is implemented. There is no dossier, no role-based
view, no confidence label, no provenance badge and no portrait in the MERIDIAN codebase. This work is
backlog and must not interrupt Phase 0 remediation.**
