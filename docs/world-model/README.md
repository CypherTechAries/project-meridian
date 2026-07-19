# World-model document set — index

> # ⚠ SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing described in this document set exists in the MERIDIAN codebase.** Not one entity type,
> field, view, mechanism, tier, edge, test or portrait pipeline has been built. These are
> specifications of a future architecture. They do not describe working software.
>
> Every document in the set is written in *will* / *must* / *is specified as*, never in the present
> indicative about behaviour. Where a document describes something that **does** exist today, it
> says so explicitly and cites `file:line`, so the boundary between the built and the specified is
> always visible.
>
> MERIDIAN's defining defect — the reason its repository is private and the reason a Phase 0
> remediation phase exists — is documentation that claimed properties the code did not have. If any
> sentence in this set reads as a report of working software, that sentence is a defect and should
> be raised.

**Status:** DRAFT, pending owner review. All nine documents. None has been reviewed by the owner.
**Date:** 18 July 2026.
**Amended 19 July 2026 — index entry added for the ninth document.** Founder decision 1A created
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md), which every other
document in the set already cites as the owner of observation and perception, but which this index
omitted. It is added below in both tables. The counts "eight" in this file are corrected to "nine"
for the same reason. Nothing else in this index is changed, and no open question is closed by the
addition.
**Existence on disk is neither review nor implementation.**

---

## Disposition: BACKLOG. This work must not interrupt Phase 0 remediation.

The founder was explicit
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):5-6, :340-341;
[`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:107-120`)): the world model must be captured **before** the
replacement simulation architecture is designed, and capturing it must **not** displace P0.1-P0.8.

Nothing in this set is a proposal to begin building. Nothing in it should be read as scheduling
work. It exists so that the intent is explicit and dated, and so that it is held until the
foundation is honest and testable.

**AI agents may draft these records but may not approve decisions**
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)). Every point requiring a human choice is recorded as an
open question inside the document it arises in, and is deliberately left unresolved.

---

## The canonical requirement statement

Verbatim from the source record
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):356-361):

> MERIDIAN will represent consequential people, organisations, businesses, communities, institutions
> and states as persistent simulated entities. Each entity will have a type-appropriate identity,
> history, motivations, relationships, capabilities, beliefs, resources and evolving state. Profiles
> will expose information according to player role, evidence and confidence rather than revealing
> omniscient ground truth. Profile details must influence simulation behaviour through explicit
> causal mechanisms and must not exist solely as generated narrative.

---

## Terminology

**Public-facing language is "simulated society"** — a founder decision of 18 July 2026. Not
"synthetic society" and not "artificial society", both of which imply the world is merely generated
content.

**Internal and technical language retains "synthetic population", "synthetic agent" and "synthetic
data"**, which remain correct.

This set uses "simulated society" for the world. The internal terms are recorded here because they
remain correct where technically accurate; they are not otherwise used in these documents.

The superseded wording survives outside this set, in files this set does not change:

| Site | Wording |
|---|---|
| `README.md:3` (repository root) | "A synthetic-society crisis simulation engine" |
| `scaffold/README.md:1` | "MERIDIAN — Synthetic Society Crisis Simulator (Scaffold)" |
| `scaffold/backend/app/main.py:21` | `title="MERIDIAN — Synthetic Society Crisis Simulator"` — the FastAPI title, so this one is served to API users |
| `HANDOFF.md` § Backlog (`:111`) | "**Synthetic-society correction.**" |
| GitHub repository description | "synthetic-society crisis simulation engine" |

Changing the repository description is an owner action. The in-repository wording is **not currently
covered by any Phase 0 work item**: P0.1 is scoped to correcting *false claims*
([`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md):130-134), and
a superseded naming preference is not a false claim. It is therefore unowned rather than scheduled.

> **OPEN QUESTION (owner).** Where should the terminology correction be carried — inside P0.1's
> scope, as a separate corrective-backlog item, or deferred until after publication? Not decided
> here. No agent may decide it.

---

## Reading order

Read the source record first. It is the authority: where a derived document and it disagree, it is
right and the derived document is wrong.

| Order | Document | Why here |
|---|---|---|
| 1 | [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md) | The verbatim source record. **Do not edit.** |
| 2 | [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) | The spine. Everything else sits on it. |
| 3 | [`PERSON-MODEL.md`](PERSON-MODEL.md) | The type the rest of the set is most often read against. |
| 4 | [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) | Organisations, businesses, countries, institutions. |
| 5 | [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) | The edges persons and organisations are connected by. |
| 6 | [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) | What entities believe, and why they can be wrong. |
| 7 | [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) | How a world event becomes an entity-specific observation — the stage upstream of belief. Placed here to match [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §14, which lists it directly after the belief model. |
| 8 | [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) | How the set scales to a whole society. |
| 9 | [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) | The read surface over everything above. Lives in `docs/design/`. |
| 10 | [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) | Constrains every document above. Lives in `docs/safety/`. Read last, then re-read the person model. |

Two of the nine deliberately live outside `docs/world-model/`, per the source record's own file
list (:345-352): the dossier is a design record and the identity guidelines are a safety record.

---

## The nine documents, one line each

| Document | What it specifies |
|---|---|
| [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) | The common base every entity shares — six entity types, seven capability traits, stable identity, and the four profile views of which only *authoritative reality* is simulation state. |
| [`PERSON-MODEL.md`](PERSON-MODEL.md) | What a person record contains, with every attribute paired to the mechanism it must drive, and six enforcement rules that make "biography shifts the odds, never picks the answer" structurally hard to violate. |
| [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) | Organisations, businesses and countries as composites of internal blocs whose competing pressures are arbitrated into an action nobody chose — plus the gap between what an organisation says it is for and what it optimises. |
| [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) | Directional, historied edges — "A trusts B" never implying the reverse — with nine scored dimensions, an unresolved-business ledger, and point-in-time query over an event stream. |
| [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) | Truth, knowledge, belief and disclosure kept strictly apart, with a signed bidirectional update rule that must never reach an absorbing state, and the eight confidence labels computed rather than authored. |
| [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) | **Added 19 July 2026 by founder decision 1A.** Exposure, acquisition, relay, degradation and source attribution — the transformation from a world event into an entity-specific observation, stopping at the moment an observation is recorded. Supersedes `M12 OBSERVABILITY` and decomposes `M-OBS` into `M-OBS-EXP`, `M-OBS-ACQ`, `M-OBS-ATTR` and `M-OBS-SURF`. It exists because observation had been assigned to a user-interface specification that cannot own a simulation mechanism. |
| [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) | The four fidelity tiers, deterministic promotion and demotion between them, and multi-term influence weighting in which headcount is one term rather than the rule. |
| [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) | The ten-tab dossier as an **intelligence product, not an omniscient encyclopaedia** — role-scoped, confidence-labelled, provenance-tagged, and introducing no authoritative attribute of its own. |
| [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) | The rule that sensitive identity may affect social experience, networks, exposure, discrimination and solidarity but never inherent competence, morality or intelligence — made checkable through quantity kinds, effect classes and four bias test classes. **The founder decision of 18 July 2026 widens the prohibited list to competence, morality, loyalty, violence or manipulability**, and forbids protected characteristics as optimisation criteria for persuasion (control 5); that document's §9 carries the wider form. |

---

## Phase 0 items that are hard prerequisites

**None of this specification is buildable until these land.** Each is stated once here; each
document states its own dependency in detail.

| Prerequisite | Status | Why the set depends on it |
|---|---|---|
| **Deterministic randomness isolation — P0.4A** | **Does not exist. Owned by P0.4A**, a Phase 0 workstream created by founder decision of 18 July 2026 and ordered `P0.4 → P0.4A → P0.5 → P0.6` ([`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md) §P0.4A). *(An earlier draft of this table said it sat under no Phase 0 item.)* Isolation is required by subsystem, entity, relationship or interaction, purpose, and tick or event context — **per-entity streams alone are insufficient** — and the mechanism (stateful named substreams versus keyed / counter-based draws) is an unmade owner decision; the drafted, unapproved candidate is [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md). Either way it changes determinism and authoritative state, so it requires owner approval ([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`)). **Binding sequencing rule: entity promotion and world-model materialisation may not proceed until P0.4A passes; specification may.** | The hardest dependency in the set. Every draw comes off one shared stream (`engine.py:83`), and A3 demonstrated **by execution** that one added draw shifts every later draw everywhere ([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):170-175). Materialising an entity consumes draws, so on today's architecture **national indicators would move because a player opened a dossier**, and the same person generated at a different tick would receive a different biography and a different face. Deterministic generation, stable identity, tier promotion and the identity-swap bias tests are all unbuildable without it. |
| **P0.4 — the authoritative-state contract across macro/meso/micro** | Not started ([`../../HANDOFF.md`](../../HANDOFF.md):75). | The four-view model is an *extension* of a contract that has not been written. Today the contract is implicitly macro-only. Every document's position that only authoritative reality is authoritative state is a claim **about** P0.4, not a substitute for it. |
| **P0.6 — event, snapshot and replay foundations** | Not started ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:87-88`)). | Event-sourced entity history, observation provenance, institutional memory, dissent history, grievance ledgers and the charter's eight-question record are not merely unbuilt but **unbuildable** before it. Replay must make zero model or network calls, which also gates any LLM-proposed option entering a seeded draw. |
| **P0.5 — explicit cross-tier causal channels** | Not started ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:84-86`)). | [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) is the **design successor** to P0.5's "`represents_population` must affect aggregation", and layers above the single channel P0.5 delivers. It does not duplicate, replace or re-open it. One flag: P0.5's literal wording admits pure population-proportional weighting, which the source record's disproportionate-influence requirement (:137-139) would then have to unpick. |
| **P0.7 — simulation time and horizon** | Not started ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:89`)). | "Per tick" has no defined meaning to specify against, and every per-tick decay-toward-baseline rule in the set is mean reversion, which P0.7 forbids until time and horizon are defined. Those rules must be re-derived from P0.7, not implemented as written. |
| **B5 / P0.8 — the dual-use influence-targeting decision** | **DECIDED** (founder decision, 18 July 2026) — **and still outstanding, as work rather than as a judgement.** B5 did not clear when the decision was taken. It now clears only when the **eight controls** the decision names are **implemented and verified**; disclosure and any future acceptable-use wording are supplementary, technical enforcement is mandatory. **None of the eight exists in code, and no Phase 0 item owns them.** The "open owner decision" framing at [`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.8 (`:90`) and [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):245 predates the decision and is superseded. | Coupling, not sequencing. This set refines targetable audience attributes from five aggregate cohorts to named individuals with portraits and an asymmetric social graph, so **the dual-use surface it creates is strictly larger than the one the eight controls were written against.** The decision now *supplies* the envelope the identity attributes must sit within, rather than being awaited for it — in particular control 5 (protected characteristics may never be optimisation criteria for persuasion or manipulation) and the not-permitted identity list. **The decision's content is applied across this set; the decision itself is not reopened, extended or reinterpreted anywhere in it, and must not be by any agent.** |

A further precondition that is not a Phase 0 item: population-weighted aggregation is valid only
against a **bidirectional** belief model. Cohort belief today is a one-way ratchet to zero
(audit §5.9), and weighting a monotone collapse by headcount would manufacture a confident national
number generated by a defect.

---

## Governing records

- [`../../CHARTER.md`](../../CHARTER.md) — non-negotiable. The eight-question standard (`:118-127`),
  the determinism boundary (`:37-44`, ADR-006), and the fictional-scenarios constraint (`:137`).
- [`../../HANDOFF.md`](../../HANDOFF.md) — Phase 0 order P0.1-P0.8, the backlog disposition, the
  standing constraints and the approval boundaries.
- [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) and
  [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) — the **CLOSED**
  audit. Cited throughout as evidence. Not to be re-opened, and no new audit is to be launched.
- [`../delivery/CAPABILITY-CLAIMS.md`](../delivery/CAPABILITY-CLAIMS.md) — what may and may not
  currently be claimed about MERIDIAN.

---

**End of index. DRAFT, 18 July 2026, pending owner review. Nothing described in this set is
implemented. This work is backlog and must not interrupt Phase 0 remediation.**
