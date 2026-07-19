# UI-RESEARCH-HANDOFF — what MERIDIAN's interface should be, and what the evidence actually supports

> # ⚠ DRAFTED — NOT FOUNDER-APPROVED — NOT IMPLEMENTED
>
> **Nothing described in this document exists in MERIDIAN's code.** There is no interface, no shell,
> no dossier, no confidence chip, no provenance tag, no map and no command composer. The only
> state-serving endpoint returns the macro tier (`scaffold/backend/app/api/routes_simulation.py:64`);
> the only front-end artefact is a static development stub (`scaffold/frontend/index.html`).
>
> This is a **research and recommendation record**. Every behavioural sentence is written in *should*,
> *would* or *is proposed as*, deliberately. Drafted by an AI agent. **AI agents may draft records but
> may not approve decisions** (`HANDOFF.md` § Standing constraints (`:138`)) — every genuine choice is listed in §9 and left
> unresolved. This document does not authorise implementation.

**Dated:** 19 July 2026 · **Status:** DRAFT, pending founder review · **Disposition:** BACKLOG —
must not interrupt Phase 0 remediation.

> **Review status — disclosed because it affects how much weight this document carries.**
> A single consolidated independent review was commissioned as instructed. **It failed three times
> with the same infrastructure error** (stream idle timeout) and was not completed. The review was
> therefore performed by the document's own author, which is **weaker than independent review** and
> should be treated as such. It nonetheless found and corrected four real defects in this document:
> a verification status conflated with primary-source retrieval throughout §11 (the most serious —
> corrected); a fact-check attribution in §1 F2 that did not exist; a contradiction between the two
> statements of dossier property D-2 in the companion slice document; and two design patterns needing
> originality notes. **An independent review of these three documents is still outstanding and should
> be run before any of this informs implementation.**

---

## 0. What this is, and what it cost

A single broad comparative research pass was run: **27 product studies** (games and professional
command/intelligence systems) and **14 cross-cutting research threads** (HCI, standards, accessibility,
frontend feasibility), each with an adversarial fact-checker. The pass was **stopped early by founder
cost-control decision** before the long-form drafting and multi-critic phases.

| | |
|---|---|
| Research agents completed | **41 of 41** (27 products + 14 threads) — full coverage |
| Fact-check agents completed | **25 of 41** — **16 studies carry no independent verification** |
| Claims fact-checked | 137 |
| Verdicts | 47 CONFIRMED · 48 PARTLY_TRUE · 41 UNVERIFIABLE · **1 REFUTED** |
| Unique sources | 724 |
| Cancelled by founder decision | 4 distillation agents, 16 drafting agents, 4 critic passes (~24 agents) |

**Read §10 before treating any recommendation as settled.** A 34% outright-confirmation rate is not a
strong evidence base, and several threads report that their web-search budget was exhausted before
they began, forcing them to work from direct URL fetches only. This document labels accordingly. It
is deliberately not a research book; it is a decision aid.

---

## 1. The ten most consequential findings

**F1 — Having a causal model is not the same as the causality being traceable, and no shipped product
has solved multi-hop tracing.** Democracy 4 has the best causal-graph interface in the genre and
**only ever reveals one hop** — hovering a node shows its immediate neighbours, and long chains cannot
be followed. Victoria 3 shipped a rich causal economy that players demonstrably could not trace
backwards. Terra Invicta gives no causal feedback on outcomes at all. This is simultaneously
MERIDIAN's **whitespace** and its **principal risk**: the Eight Questions are the differentiator, and
the commercial precedent for delivering them is *absent*, not merely weak.

**F2 — Explanation does not automatically produce understanding, and can reduce it.** Explanations
increase acceptance of system output without increasing accuracy; more transparency has been measured
to make people *worse* at catching large errors via overload; trained practitioners over-trust and
misread interpretability visualisations. *(Evidence: XAI literature — Bansal, Poursabzi-Sangdeh, Kaur,
fetched as primary sources by the researching agent. **This thread received no independent
fact-check** — see §10.)* **Consequence:** MERIDIAN's causal surface must be an *interaction with a
forcing function*, not a wall of text, and it must be **evaluated**, not assumed.

**F3 — MERIDIAN's epistemic model already exists commercially, in Football Manager.** Unscouted
players show attribute *ranges* or hidden attributes; knowledge improves with scouting effort; a
star-rating carries an explicit confidence indicator; ground truth is *never* shown. This is a
20-year-playtested existence proof for the player-intelligence-profile view and the single strongest
argument that the dossier concept is viable rather than merely elegant.

**F4 — The eight confidence labels conflate independent axes and contain no likelihood axis.** Real
tradecraft separates *likelihood of a proposition* from *analytic confidence* from *source
reliability* from *information credibility*. The IPCC treats confidence and likelihood as orthogonal
and publishes fixed numeric bands. The 2007 Iran NIE is the documented failure of using "confidence"
to mean probability. MERIDIAN's set (Confirmed · Reported · Assessed · Disputed · Unknown · Possibly
deceptive · Outdated · Restricted) mixes evidence state, recency and access, and has **no way to say
how likely something is** — so `Assessed` and `Confirmed` will inevitably be read as probability
statements. **This needs a founder decision (D2), not a styling fix.**

**F5 — The obvious relationship-graph implementation silently violates dossier property D-2.** Nearly
all force-directed graph libraries are randomly seeded. D-2 requires a dossier to consume **zero
randomness**. A standard `d3-force` drop-in would appear to work correctly and would surface much
later as a failed replay-determinism test. Graph layout must be a pure function of (entity set, stable
sort key), or must draw from a dedicated *presentation* substream that is never the simulation RNG.

**F6 — Node-link readability collapses at roughly 20 vertices, and the real budget is edge density,
not node count.** Controlled comparison found matrices beat node-link on six of seven tasks above
~20 vertices — but node-link wins *path-finding* decisively on small sparse graphs (99% vs 70% at 20
nodes). MERIDIAN's Relationships tab is an ego-network and its signature task is chain-tracing, so
node-link is the right default — **capped**, with a matrix offered as a labelled second representation.

**F7 — Alarm-management standards supply the only hard numbers on human alert capacity, and they are
brutally low.** EEMUA 191: ≤1 alarm per 10 minutes in steady state; ≤10 in the first 10 minutes after
a major upset; ~3 priority levels distributed ~5% high / 15% medium / 80% low. Texaco Milford Haven,
1994: two operators faced **275 alarms in 11 minutes**. HSE's rule — *process status indicators must
not be designated as alarms* — maps directly onto MERIDIAN's queue/feed split.

**F8 — MERIDIAN cannot build its alert model on top of the open macro-saturation critical.** Macro
indicators rise monotonically because the engine has no cost, cooldown, decay, budget, prerequisite or
revert mechanism. **Any edge-triggered threshold alert would therefore fire every tick, on every
indicator, forever, from the first build.** Specify the alert model now; do not ship it until decay and
state-based alerting with stable dedup keys exist.

**F9 — Labelling only the AI text actively inflates the authority of everything else.** The implied
truth effect is well established: warning labels on a subset raise the perceived accuracy of the
unlabelled remainder. MERIDIAN's instinct — tag narration, leave engine output bare — would silently
promote unlabelled content, *including saturating macro indicators and scenario-authored seed values*,
to apparent verified status. **Both classes must be marked positively, and "unmarked" must be a build
failure.** Separately: gradient, glow and shadow AI-markers are forced to `none` in forced-colors mode,
so the fashionable treatments are technically void.

**F10 — The natural-language interface's failure mode is capability envisioning, not parsing.** Users
of NL interfaces cannot determine what the system can be asked to do, or evaluate whether the result
matched their intent. A perfect parser attached to an unknowable capability space **collapses into the
pre-authored-menu failure the charter explicitly forbids** — the player regresses to the safe subset
they have already seen work. Shipped agent products have converged on *plan-as-artifact*: a
structured, inspectable, editable object the deterministic system prices, with execution gated on
approval of that artifact.

---

## 2. The ten highest-risk UI failure modes for MERIDIAN

Ranked by probability × severity, each tied to MERIDIAN's actual architecture.

| # | Failure mode | Prior art | MERIDIAN's specific exposure | Counter-measure |
|---|---|---|---|---|
| **R1** | **Explanation exists but only one hop deep.** The causal model is real; the interface can only show immediate causes. | Democracy 4 (one hop only); Victoria 3 (untraceable backwards) | Eight Questions Q2 and Q8 are inherently multi-hop. Q2/Q3 must be **persisted per outcome**, not recomputed on demand. | Ship an explicit ranked **path view** (pick source → pick outcome → render contributing chains), not just neighbour reveal. |
| **R2** | **Tooltips as a dumping ground.** Information that should be layout gets pushed into nested hover chains. | Paradox titles ("Balrog tooltips", cyclic nesting, null hops); Victoria 3; Old World | MERIDIAN's causal graph is *more* cycle-prone than a glossary. Confidence labels and provenance tags are load-bearing and must never be hover-only. | Rule: *if a player needs a fact on every visit, it is layout, not a tooltip.* Cap nesting at 2; validate the explanation graph for cycles in CI; enforce a written **never-behind-hover list**. |
| **R3** | **Contrast that passes the checker and fails the eye.** | Documented WCAG 2.x formula behaviour near black | MERIDIAN is dark-first. **Invisible to the tooling the team will actually run** — the highest-probability accessibility failure. | Dual-gate: pass WCAG 2.2 AA *and* an APCA floor. Never claim APCA as WCAG conformance — it is a non-normative draft. |
| **R4** | **The relationship graph detonates.** Hairball above ~20 vertices; supernode expansion is the specific interaction that kills it. | i2 / Maltego / Linkurious | States, ministries and national media are supernodes by construction. | Cap the ego-net (≤12 alters default, ≤2 hops); show neighbour count *before* expansion; never ship an unbounded expand; deterministic layout only (see F5). |
| **R5** | **Alert flood built on the saturation bug.** | Texaco Milford Haven; Three Mile Island; Qantas 32 | See F8. Also: correlated events produce N correct alerts and one overwhelmed player without causal grouping. | State-based (not edge-based) alerting with stable dedup keys; root-cause collapsing; a rate budget instrumented against the *player's wall clock*. **Do not ship before decay exists.** |
| **R6** | **Provenance tag present, perceptually absent.** Boxed tinted rectangles are read as advertising and skipped; a government design system reports its own container-based differentiation is frequently not noticed. | Banner-blindness research; GOV.UK | The dossier deliberately *interleaves* engine fact and narration — the exact condition under which a fluent paragraph is mistaken for an audited result. | Three-signal redundancy with a **crop-invariant carrier** (a full-height left gutter rule survives screenshot cropping); mark both classes; CI assertion that no text node lacks a provenance class. |
| **R7** | **Search and filter under-budgeted as plumbing.** | CK3 (weak finder for the population it generates); Dwarf Fortress (2022 overhaul shipped without list search) | Persistent-entity simulations create a search problem proportional to population size. MERIDIAN has three tiers and four views per entity. | Treat the entity browser as a **primary screen**; global command palette over every named engine quantity and entity from day one. |
| **R8** | **Aggregates with no drill-down.** A headline number that modifies the simulation but cannot answer "what caused it". | Cities: Skylines ("why is nobody moving in?"); Power & Revolution's hero metric | Macro tier is exactly this shape. Making an unexplained number *more prominent* makes it worse. | Rule: **every aggregate exposes a ranked contributor list naming the mechanism behind each contributor**, or it does not ship. |
| **R9** | **Moral weight evaporates when people become populations.** | Frostpunk → Frostpunk 2 | MERIDIAN's differentiator is propagation through *real-seeming people*. The macro/meso tiers are where that dissolves into indicators. This is the strongest empirical support for the four-tier fidelity model — and the clearest warning about its interface. | Every aggregate must be able to surface at least one **named, materialised individual** it is about. Tier-promotion presentation is currently unspecified (see §9 D7). |
| **R10** | **Prompt injection via in-world content.** In-world documents, transcripts, images and annotations are attacker-authorable, and **human approval is documented as an insufficient defence** because approval fatigue produces reflexive consent. | Published indirect-injection literature | MERIDIAN plans exactly this ingestion path. | Architectural, not procedural: plan-then-execute with a hard reader/planner split; primitive composition fixed *before* untrusted content is read; quarantined reader extracting only into typed slots; taint chips escalating the confirmation ladder. |

**Two further failure modes worth naming, below the top ten:** *documentation dependence as an
externalised design cost* (Dwarf Fortress's 10,000-article wiki in the critical path — for MERIDIAN,
if the Eight Questions are answered in a wiki rather than the interface, the charter is unmet
regardless of wiki quality); and *the causal truth as a separable module* (Power & Revolution sells
explanation as a paid add-on — if explanation is architecturally separable, it *will* be separated
into a debug view).

---

## 3. Findings that SUPPORT the current MERIDIAN direction

- **The intelligence-product framing is vindicated by a shipped commercial product** (F3, Football
  Manager). This is the strongest positive finding in the corpus.
- **The two-axis visibility/confidence split is independently validated.** The IPCC treats confidence
  and likelihood as orthogonal metrics; MERIDIAN's insistence that visibility and confidence are
  different questions is structurally correct even though the label set needs work (F4).
- **"Unknown must be a present row" has direct empirical support.** Highlighting and annotating
  missing data produces higher perceived data quality *and* more accurate interpretation than
  downplaying or removing it; removal that breaks visual continuity produces outright wrong answers.
  This extends the rule from dossier tables to indicator time series.
- **Shape-before-colour is proven operational doctrine, not a design opinion.** NATO APP-6 /
  MIL-STD-2525 deliberately make shape and colour redundant so symbology survives monochrome. It is
  also trade-dress-safe — an open interoperability standard, not a product's visual identity.
- **The Eight Questions are structurally sound as a design instrument.** They map cleanly onto
  Endsley's three-level situation-awareness model and are a close cousin of the question-driven XAI
  framing. Terra Invicta's absence of causal feedback is the strongest negative argument *for* the rule.
- **Plan-as-artifact is a working existence proof for the PLAN→COMMAND boundary** (F10), including the
  detail that approval need not be binary.
- **Determinism doctrine has an off-the-shelf data model.** W3C PROV (Entity/Activity/Agent) turns
  ADR-006 from prose into a checkable graph invariant: *no authoritative entity may be generated by an
  activity whose agent is a language model.*
- **Event-sourced branching is a documented pattern**, not something MERIDIAN must invent — including
  the rule that replay must not re-fire external effects (for MERIDIAN, the external effect *is* the LLM).
- **Refusal-as-explanation is validated negatively across the corpus.** Victoria 3's unexplained
  blocked actions and CMO's one-blocker-at-a-time refusal window both map onto the charter promise
  "here is what is required, what may stop it" — which requires returning the **full** blocker set.

---

## 4. Findings that CONTRADICT or materially QUALIFY the current direction

**C1 — "The player can inspect why" is not self-justifying.** F2. Depth of explanation raises
acceptance without raising accuracy. The differentiator must be *tested*, not asserted, and the
inspection surfaces must earn their cost against measured behaviour.

**C2 — The eight confidence labels are not ready.** F4. They have no likelihood axis and conflate at
least four independent dimensions. Shipping them as-is would reproduce a documented intelligence
failure in miniature.

**C3 — Dark-first carries a measured legibility cost.** Controlled evidence tends to favour light
mode for users with normal or corrected vision; dark mode benefits a specific low-vision population.
Dark is defensible on ambience and low-light grounds but **cannot be shipped dark-only and called
accessible**. A light and a high-contrast theme are required, not optional.

**C4 — "Cinematic presentation" is a measured risk, not a garnish.** Naive-realism research found
richer, more realistic representations perform **worse** for identification tasks. This is the
allocation stakeholders will ask for and the one the evidence most directly challenges.

**C5 — The map should probably not be the primary surface.** MERIDIAN's macro tier is a set of
national scalars with no sub-national denominator, so the instinctive "crisis map" choropleth is
close to meaningless — choropleths require normalised rates and are actively wrong for raw counts.
Per-tick auto-classification would additionally *conceal* the open saturation critical behind a
permanently healthy-looking colour spread. Recommendation: the centre view is a **substrate switcher**
(Map / Society / Causal chain), with no substrate architecturally privileged.

**C6 — Progressive disclosure's canonical citation is unbacked.** Nielsen's progressive-disclosure
article contains no study, sample or effect size. Shneiderman explicitly limits his own "overview
first" mantra and defines details-on-demand as applying *after* a collection is trimmed to a few dozen
items — which is not a single-entity dossier. **Adopt the practice; do not cite the unbacked claim.**
Citing it would reproduce precisely the defect this project exists to correct.

**C7 — "Fewer screens" can increase click-depth.** Football Manager's consolidation increased
effective interactions-to-fact. Measure **interactions-to-fact for defined expert tasks**, not screen
count. Progressive disclosure must be additive (a summary that expands), never substitutive.

**C8 — Ten tabs per entity is unvalidated and probably too many at once.** No product in the corpus
supports a ten-tab default as a *first* experience. The evidence favours a small always-visible L1
strip with the rest reachable in exactly one activation. The ten sections should survive as an
*information architecture*; the tab count is a separate, open question (D8).

**C9 — Hidden thresholds are the recurring player complaint across political sims.** Suzerain's
decisive hidden variables produce trial-and-error and wiki dependency. *Uncertainty is legitimate;
invisibility is not.* If a variable determines an outcome, the player must be able to see that it
exists and roughly where they stand, even if the value stays uncertain.

**C10 — The interface is not a layer on the product; it is the product.** Football Manager cancelled
an entire annual release explicitly over interface quality, then shipped the rebuild and was rejected
by its existing user base. A studio with 30 years of domain expertise and a major publisher's
resources could not rebuild its interface on schedule. **Scope accordingly.**

---

## 5. Direct verdict on the 70 / 20 / 10 thesis

> *"Conventional usability underneath; near-future command-system styling on top."*
> *Roughly 70% familiar professional software, 20% tactical information design, 10% cinematic presentation.*

**Verdict: directionally right as a doctrine of restraint; wrong as a description of the work; and the
10% is the weakest-evidenced part of it.**

**What the evidence supports.** The restraint instinct is correct and well-supported. Command: Modern
Operations demonstrates that a dark theme buys real reviewer goodwill and changes nothing structural —
styling is cheap and safe. Conventional widget vocabulary is not a liability. The friction argument is
strongly supported from an unexpected direction: the interventions that most reduce over-reliance are
the ones users like least, so **friction must be rationed and spent only at the PLAN→COMMAND
boundary**. That is exactly the 70/20/10 instinct, correctly derived.

**Where it is wrong.**

1. **The styling/interaction split is a false separation for the parts that matter most.** The
   confidence chip, the provenance gutter, the Unknown row, the uncertain map contact and the causal
   ledger are not "tactical styling applied on top of conventional controls" — they are *load-bearing
   correctness surfaces* where the visual encoding **is** the honesty guarantee. Calling them the 20%
   understates their status: get them wrong and the charter is breached, not merely the aesthetic.

2. **The 70% is not available to be borrowed.** "Familiar professional software" implies established
   patterns exist for MERIDIAN's core loop. F1 says the central one — multi-hop causal tracing — has
   **no commercial precedent to be familiar with**. The genuinely conventional portion (tables,
   filters, tabs, search, panels) is real but smaller than 70%, and the residue is original design
   work that must be budgeted rather than assumed.

3. **The 10% cinematic allocation is the least defensible number in the thesis.** C4: naive realism
   measurably degrades identification performance. Frostpunk's own trajectory shows cinematic weight
   *evaporating* when the simulation moved from people to populations. Motion research is clear that
   motion should mean causality and nothing else, and that animating the digits of an authoritative
   value is actively harmful. **Recommendation: reframe the 10% from "cinematic presentation" to
   "reserved-moment ceremony" — a named, bounded, auditable second easing register spent at the
   commitment boundary and the after-action review, and nowhere else.**

**Proposed replacement framing, for founder decision (D9):**

> **Conventional interaction, original information design, rationed ceremony.**
> The interaction grammar should be unremarkable and learnable. The encodings that carry epistemic
> state — confidence, provenance, visibility, causality, absence — are original, load-bearing and
> non-negotiable. Ceremony is a budget, spent only where an action is irreversible or a run is being
> reviewed.

This preserves everything the original thesis got right (restraint, familiarity, rationed drama) while
removing the two claims the evidence contradicts (that the hard part is styling, and that cinematic
presentation is a proportion of the interface rather than a bounded budget).

---

## 6. The minimum five-screen vertical slice

Detailed specification is in **`docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md`**. Summary:

| Screen | Proposition demonstrated | Primary question |
|---|---|---|
| **Strategic Command Centre** | *(shell — holds the other four)* | "What is happening, what is urgent, and what am I being asked to decide?" |
| **Entity Dossier** | 1 — persistent, inspectable people and organisations | "Who is this, what do I actually know about them, and how do I know it?" |
| **Society Pulse** | 2 — a crisis propagates through society, media, markets, institutions | "Who is this crisis reaching, through what channel, and who is it reaching next?" |
| **Conversational Command Interface** | 3 — propose unexpected actions, inspect the interpreted plan | "Can I attempt this, what would it cost, and who would resist?" |
| **Causal Timeline** | 4 — understand why visible state changed | "Why did this number move, and what would have happened otherwise?" |

**Scope filter applied.** The research covered substantially more ground than these four propositions
(map layer taxonomy, onboarding architecture, time/branching, portrait pipelines, an operational
military layer, accessibility conformance strategy). That material is **preserved in the evidence
files but excluded from the slice** and belongs in the future backlog. It is not deleted, because it
will be needed — but nothing in it should be read as authorised for the first implementation.

---

## 7. Recommended frontend stack

| Layer | Recommendation | Alternative considered | Trade-off |
|---|---|---|---|
| Framework | **React 19 + TypeScript (strict) + Vite** | Svelte | Svelte would likely produce a smaller, faster runtime. React is recommended **for accessible headless-primitive maturity**, not speed. The leading Svelte headless library is pre-1.0 (v0.86.6, "under active development") — a pre-1.0 dependency underneath a mandatory accessibility guarantee is a real risk for a solo developer. **Do not claim React is faster; that comparison is UNVERIFIED.** |
| Components | **Radix headless primitives, 100% of visual identity from own tokens** | A styled component library | Headless-plus-own-tokens is the only combination satisfying *both* the no-trade-dress rule and the accessibility rule. |
| Packaging | **Browser-only, served from the existing FastAPI process via `StaticFiles`** | Tauri; Electron | Defer Tauri, reject Electron. Keep the Tauri path cheap by banning Node-only APIs, untested Chromium-only CSS, and any filesystem assumption. |
| Transport | **SSE (`EventSource`) for the simulation feed; ordinary POST for every command** | WebSocket | SSE is unidirectional, auto-reconnects, and its `Last-Event-ID` cursor maps directly onto the P0.6 event-sourced replay foundation. **Constraint:** HTTP/1.1 allows only 6 concurrent connections per browser+domain — serve over HTTP/2 or hold strictly one `EventSource` per tab. FastAPI's own docs warn that in-memory broadcast works only single-process; do not document "realtime" as delivered without stating that. |
| Map | **MapLibre GL JS driven by inline/authored GeoJSON — no tile server, no basemap, no attribution dependency** | deck.gl `cartesian` (non-geographic); a raster image source | Decisive feasibility fact: MapLibre renders a complete map from inline GeoJSON. A fictional country ships as versioned scenario data with zero external network dependency and zero risk of real-world geography leaking into a fictional world. Author in real WGS84 coordinates placed in open ocean so projection maths stays valid. **Map content authoring is a scheduled work item with its own budget, not an incidental asset.** |
| Graph | **Capped ego-network, deterministic layout, canvas-rendered** | sigma.js (WebGL, thousands of nodes); Cytoscape.js | Pick the *cap* first, then the cheapest library that clears it. Cytoscape.js's performance flags are described by its own docs as "largely moot" and it has no verified WebGL path. **Layout must be deterministic — see F5.** |
| Tables | **TanStack Virtual with own markup** for any list over 100 rows | AG Grid | Fix row height to a token constant so `estimateSize` is exact. **Critical: the virtualiser's item count is the count of FIELDS, not the count of KNOWN fields** — otherwise Unknown/Restricted rows vanish from the scroll model. |
| Charts | **uPlot for long time series; bespoke token-driven SVG for explanatory charts** | A general charting library | Pair every canvas chart with a visually-hidden screen-reader data table. |
| Tokens | **DTCG token *shape*, compiled by Style Dictionary to CSS custom properties** | Ad-hoc CSS variables | Adopt the shape; **do not claim DTCG conformance** — the spec explicitly disclaims its own authority ("Do not reference this version as authoritative in any way"). Pin an internal version. Lint-ban raw hex/px/ms literals in components. |
| Testing | Playwright + MSW fixtures + Storybook; visual-regression on the chip/row/provenance components | — | The encodings that carry epistemic state need visual regression specifically, because their correctness *is* visual. |

**One architectural rule above all of these:** the client is a **pure read-and-propose surface that
never holds authoritative state**. Proposed: type every network-derived value as
`Sourced<T> = { value, provenance: 'engine' | 'fixture' | 'advisory', asOfVersion }`, forbid components
from consuming bare values, and **ban optimistic updates for anything the engine prices** — a proposed
action renders in exactly four states (DRAFTED / SUBMITTED / PRICED / RESOLVED), with the first two
visually distinct from the last two and never displaying an engine-authoritative number. This is the
interface expression of ADR-006, and optimistic UI is the default frontend reflex that would violate it.

---

## 8. What can honestly be built now with fixtures — and what is gated

### 8.1 Buildable now

| Item | Honest claim | Must NOT claim |
|---|---|---|
| Design system: tokens, type scale, chip components, provenance containers, focus rings, themes | "A design system exists and is contrast-tested in light, dark and forced-colors" | That any of it is connected to the simulation |
| The five-region shell, keyboard model, landmark regions, mode indicator | "A navigable shell exists" | That mode changes affect any engine state |
| Entity Dossier rendered over **declared fixture entities** | "The dossier renders a fixture projection" | That it reflects simulation state, a player role, or computed confidence |
| Society Pulse over a **hand-authored fixture propagation trace** | "An illustrative propagation is rendered from fixture data" | That the propagation was computed by the engine — it was not, and cannot be until P0.5 |
| Command composer UI up to **DRAFTED** state | "Intent can be composed and displayed" | That the composition is validated, priced, legal, or executable |
| Macro indicator panel | **This one may use real data** — `get_state` exists and returns the macro tier | That the indicators are meaningful — they saturate monotonically (open critical) |
| Fictional-world GeoJSON and the map substrate | "A fictional world renders" | Any claim of geographic or logistical fidelity |

**The fixture-honesty mechanism (non-negotiable if any of this is built).** A fixture-backed build
must declare itself *in the interface*, not in a README, such that a screenshot cannot be mistaken for
a working simulation. Proposed: a persistent, non-dismissible status-bar band reading
`FIXTURE DATA — NOT A SIMULATION RUN`, rendered in the same region as the (also mandatory)
`FICTIONAL WORLD` disclosure, present in every screenshot, and a build-time assertion that the band
cannot be disabled in a fixture build. **This matters more here than in a normal project**: the entire
remediation phase exists because documentation claimed properties the code did not have. A polished
screenshot is documentation.

### 8.2 Gated

| Gate | What it blocks | Why |
|---|---|---|
| **Auth layer** *(not currently owned by Phase 0 — audit records IAM as Phase 2)* | Role-based visibility; the `Restricted` label; the player-intelligence view as a *real* projection; any four-view rendering | "Player role" has nothing to resolve against. This is the blocker unique to the dossier. |
| **P0.4 — authoritative-state contract** | Which of the four views is authoritative; what a dossier is a projection *of*; what the client may cache | The projection has no settled contract underneath it. |
| **P0.4A — deterministic randomness architecture** | Stable generated portraits (stages 2–3); **any counterfactual branch UI**; graph layouts drawn from a seeded stream; the D-2 guarantee in practice | A counterfactual re-run must consume identical substream draws or the "difference" is partly resampling noise presented as causation — the exact class of unfounded claim the project exists to eliminate. |
| **P0.6 — event, snapshot, replay** | Causal Timeline; Activity tab; the "why" in Beliefs; evidence behind Intelligence assessment; the decision queue's dedup/resume/replay; alert grouping by causal parent | `causal_parents` are discarded and nothing persists. These surfaces are **unbuildable**, not merely unbuilt. |
| **P0.5 — cross-tier causal channels** | Society Pulse as a *computed* propagation rather than an illustration | The tiers do not causally influence one another today. |
| **P0.7 — simulation time and horizon** | Any forecast band, projection horizon, or time-based alert threshold | Undefined horizon means an undefined forecast. |
| **Decay / cost / cooldown mechanisms** *(no P0 item currently owns this)* | The alert model; any threshold-based indicator warning | F8. |

---

## 9. Decisions requiring founder approval

Numbered for reference. None is resolved here.

**D1 — Primary surface.** Map-primary, society-graph-primary, or a co-equal substrate switcher
(Map / Society / Causal chain, one keystroke each, none architecturally privileged)?
*Recommendation: substrate switcher.* Confidence: **moderate**, resting on C5. Blocks: shell layout,
map budget, the Society Pulse design.

**D2 — The confidence model.** Defend the eight labels, or adopt a multi-axis model separating
likelihood / analytic confidence / source reliability / recency / access? *Recommendation: split the
axes; publish a versioned engine-owned probability lexicon with numeric bands; render word and band
together as one atomic string.* Confidence: **high** on the diagnosis (F4), **moderate** on the
proposed remedy. Blocks: the chip component, every dossier row, the Eight-Questions Q6 row.

**D3 — Does the auth layer move earlier?** Role-based visibility is the dossier's entire premise and
has no subject today. Either auth moves into Phase 0, or the dossier ships with an explicitly
single-role, clearly-labelled interim. *No recommendation — this is a sequencing decision with
resource implications.* Blocks: everything role-filtered.

**D4 — Interim confidence labels before P0.6.** Render only `Confirmed`/`Unknown` directly from
authoritative reality, clearly marked as pre-evidence — or wait for the evidence layer entirely?
*Recommendation: the marked interim*, on the condition that the marking is structural and not a
footnote. Confidence: **moderate**.

**D5 — Target platform.** Browser-only now with Tauri deferred, as §7 proposes? Confirm or redirect.

**D6 — Portrait stage.** Stage 0 (deterministic geometric mark from `entity_id`) is the only stage
with no unmet dependency and requires no asset store. Stages 2–3 are gated on P0.4A *and* on an
unresolved safety question about enforcing "clearly fictional". *Recommendation: stage 0 only, and
do not build an asset pipeline in the slice.* Confidence: **high**.

**D7 — Tier-promotion presentation.** How does an anonymous cohort member becoming a named individual
appear to the player? **No specification exists anywhere in the eight world-model documents.** The
binding constraint is that promotion must never be triggered by the player looking — which, with D-2,
means *opening a dossier must not materialise anyone* — and no document says what the dossier shows
instead for an unmaterialised individual. This is an open design hole, not a styling question.

**D8 — Dossier information architecture.** Do the ten sections render as ten tabs? C8 says the tab
count is unvalidated. *Recommendation: preserve the ten as an information architecture; render a small
L1 strip plus a smaller grouped tab set, with the count decided by task testing rather than by the
section list.* Confidence: **moderate**.

**D9 — The design thesis.** Adopt the reframing in §5 ("conventional interaction, original information
design, rationed ceremony") or retain 70/20/10?

**D10 — Is a fixture-backed prototype authorised before Phase 0 completes,** and is the labelling
mechanism in §8.1 sufficient? This is the decision that gates all implementation.

**D11 — Fictional-world disclosure. Now higher-stakes than when this research began.** The P0.1
charter amendment of 19 July 2026 (`CHARTER.md`:225-240) records that **no provenance tag exists at
any interface**, that the scenario's `fiction_disclaimer` is free text no code reads and no interface
displays, and that **none of the eight controls the founder named for B5 exists in code**. It further
records that **B5 is the one publication blocker that cannot be cleared by correcting text** — it
clears only when those controls are implemented and verified.

Two of those controls are *interface* controls. That means the fictional-world disclosure and the
per-element provenance tag specified in this research are **not merely design preferences — they are
components of a publication blocker**, and the first UI is the artefact that would clear part of B5.
The founder decision is therefore not only "where does the badge live" but whether the vertical slice
is scoped to satisfy the interface half of B5 deliberately, with verification, rather than incidentally.

**D12 — Scope of the operational military layer.** Excluded from the slice by the four-proposition
filter. Confirm it stays out of the first implementation.

---

## 10. Weak, disputed and unverified claims

**Read this before citing anything above.**

### 10.1 Corpus-level reliability

- **16 of 41 studies carry no independent fact-check** — the pass was stopped before verification
  completed. Those studies' claims are single-sourced to one agent.
- **Of 137 verified claims: 47 CONFIRMED, 48 PARTLY_TRUE, 41 UNVERIFIABLE, 1 REFUTED.** A 34%
  outright-confirmation rate. Most PARTLY_TRUE verdicts concern *over-precision* — a real feature
  described with an invented exact string, or a reasonable inference presented as an observed fact.
- **One fabricated quotation was caught.** A study attributed a verbatim sentence to a named developer's
  blog; the fact-checker retrieved the full post and the sentence does not appear in it. **This is
  exactly why the verification stage existed**, and it is the strongest argument for treating the 16
  unverified studies with caution.
- **Several threads report their web-search budget was exhausted before they began**, forcing them to
  work from direct URL fetches only. Affected: uncertainty visualisation, causal explanation, alerts,
  situation awareness, map/layers, onboarding, time/branching, visual language, frontend tech. Their
  standards and primary-source claims are generally well-grounded; their *player-experience* and
  *practitioner-commentary* claims are thin, and several say so explicitly.
- **Source mix is uneven:** 79 Wikipedia and 56 Steam-community URLs against 27 arXiv and 18 W3C. The
  standards and HCI strands are better sourced than the game-UI strands.

### 10.2 Specific claims that must NOT be cited as established

| Claim | Status |
|---|---|
| React is faster than Svelte | **UNVERIFIED.** Only the benchmark's *methodology* was confirmed, not any ranking. Re-check before writing the framework ADR. |
| Nielsen's "progressive disclosure improves 3 of usability's 5 components" | **Unbacked in its source.** No study, sample or effect size. Adopt the practice, not the citation. |
| Layout stability ("mental map preservation") is empirically necessary | **Contested.** A pre-2012 survey found no evidence it helps; later work found conditional benefit. Adopt stable layout for *determinism* reasons; do not claim empirical necessity. |
| Hypothetical outcome plots are superior | **Task-conditional.** Markedly better for relational/probability judgements, markedly *worse* for mean estimation under high variance. Not a house style. |
| The abstraction-hierarchy mapping of a society | **Explicit agent inference**, not a literature finding. The mapping of ecological interface design to a socio-political domain is flagged by its own author as unverified — EID was built for law-governed physical domains. |
| SAGAT scored against the player-intelligence projection rather than authoritative reality | **Agent inference**, unverified against the measurement literature — though the reasoning (that scoring against ground truth would penalise a correctly-designed interface) is sound. |
| Specific in-game strings quoted from Suzerain, Victoria 3 and Democracy 4 | **Several downgraded to PARTLY_TRUE.** Wiki transcriptions confirmed the *pattern*; the exact strings were over-precise. Do not quote in-game text without a screenshot. |
| The FUI / film-interface critique strand | **Weakest section of the corpus.** The usual primary source domain no longer resolves; no quotation could be verified and none was invented. |
| Any Palantir capability claim | Treat marketing material as marketing. The study flagged this explicitly and the corpus records withdrawn claims under scrutiny. |

### 10.3 Recommendations resting on inference rather than evidence

The §5 reframing of 70/20/10; the substrate-switcher recommendation (D1); the specific glyph
assignments proposed for the eight confidence labels; the proposed shell region-to-Eight-Questions
binding; and the fixture-labelling mechanism in §8.1. These are **reasoned design proposals**, not
research findings, and are marked as such wherever they appear.

---

## 11. Traceability for load-bearing recommendations

**Read the status column carefully — it distinguishes three different things that are easy to
conflate.** An earlier draft of this table labelled thread findings "CONFIRMED"; that was wrong, and
correcting it is the most important edit made to this document.

| Status | Meaning |
|---|---|
| **✅ CHECKED** | An independent adversarial fact-checker searched for disconfirming evidence and returned CONFIRMED. |
| **◐ CHECKED-PARTIAL** | Independently checked; the pattern holds but the study's statement was over-precise. Correction in the register. |
| **◻ PRIMARY-UNCHECKED** | The researching agent fetched and read a primary source (a standard, a spec, a paper), but **no independent verification ran** — the pass was stopped early. Generally trustworthy for standards text; not independently confirmed. |
| **△ INTERNAL** | Derived from MERIDIAN's own records, or agent inference. Not an external finding. |

| # | Recommendation | Rests on | Status |
|---|---|---|---|
| T1 | Ship a multi-hop **path view**, not neighbour-reveal | Democracy 4 one-hop limit; Victoria 3 untraceability | **✅ CHECKED** on the one-hop limit; **◐** on arrow-colour semantics |
| T2 | Causal surface must include a forcing function and be evaluated | XAI over-reliance literature (Bansal; Poursabzi-Sangdeh; Kaur) | **◻ PRIMARY-UNCHECKED** |
| T3 | Split likelihood from confidence; publish a numeric band lexicon | IPCC orthogonal metrics; 2007 Iran NIE; ICD 203 | **✅ CHECKED** (tradecraft study was verified). **ICD 203 itself could not be retrieved (403)** — cited via secondary sources. Obtain before finalising D2. |
| T4 | Deterministic graph layout; never a randomly-seeded force layout | Force-layout non-determinism + dossier property D-2 | **✅ CHECKED** (link-analysis study) for layout behaviour; **△** for D-2, which is MERIDIAN's own spec |
| T5 | Cap the ego-net; matrix as labelled second view | Ghoniem/Fekete/Castagliola controlled experiment | **◻ PRIMARY-UNCHECKED** (graph-viz thread); the adjacent hairball finding is **✅ CHECKED** |
| T6 | Alert budget ≤1 P1 per 10 min; 3 priorities at ~5/15/80 | EEMUA 191; HSE CHIS6; Texaco Milford Haven | **◻ PRIMARY-UNCHECKED** — HSE CHIS6 was read in full by the researching agent, but neither the alerts thread nor the control-room study was fact-checked. Verify the EEMUA figures before they become a build budget. |
| T7 | Do not ship alerts before decay exists | MERIDIAN's own open critical finding | **△ INTERNAL** — `CURRENT-STATE-AUDIT.md` |
| T8 | Mark both content classes; unmarked is a build failure | Implied truth effect | **◻ PRIMARY-UNCHECKED** — sample sizes quoted by the agent are not independently confirmed |
| T9 | Provenance carrier must be crop-invariant and forced-colors-safe | MDN forced-colors behaviour; GOV.UK component research | **◻ PRIMARY-UNCHECKED** |
| T10 | Dual-gate contrast (WCAG 2.2 AA + APCA floor); never claim APCA as conformance | WCAG 2.2 SC text; APCA self-described draft status | **◻ PRIMARY-UNCHECKED** — W3C text fetched directly; high confidence, no independent check |
| T11 | Plan-as-artifact; approval selects autonomy level | Shipped agent-product documentation | **◻ PRIMARY-UNCHECKED** |
| T12 | Plan-then-execute + quarantined reader; approval is not a defence | Indirect prompt-injection literature | **◻ PRIMARY-UNCHECKED** |
| T13 | MapLibre + inline GeoJSON, no tile server | MapLibre style spec | **◻ PRIMARY-UNCHECKED** — spec fetched directly; this is the load-bearing feasibility fact for the map and should be re-confirmed by building it |
| T14 | SSE with `Last-Event-ID` as replay cursor; 6-connection HTTP/1.1 limit | MDN SSE docs; FastAPI docs | **◻ PRIMARY-UNCHECKED** |
| T15 | Client never holds authoritative state; ban optimistic updates | ADR-006 applied to the client | **△ INTERNAL** — inference from `CHARTER.md` |
| T16 | Tabular numerals on engine values; never animate digits | Typographic behaviour of proportional figures | **◻ PRIMARY-UNCHECKED** |
| T17 | W3C PROV as the trace data model; CI invariant on LLM-generated entities | W3C PROV Recommendation | **◻ PRIMARY-UNCHECKED** — W3C primary fetched directly |
| T18 | Every aggregate exposes a ranked contributor list | Cities: Skylines; Power & Revolution | **✅ CHECKED** — both studies were fact-checked |
| T19 | Refusals return the full blocker set, not the first failure | CMO refusal-window behaviour | **◐ CHECKED-PARTIAL** |
| T20 | Fixture builds must declare themselves in-interface | MERIDIAN's private-until-honest doctrine | **△ INTERNAL** — inference |

**The pattern to notice:** the game-UI findings are the ones that were independently checked; the
standards and HCI findings — which carry most of the concrete numbers this document proposes as build
budgets — were **not**. They rest on primary documents the researching agents fetched and read, which
is a reasonable basis for design direction and **not** a sufficient basis for a hard build budget.
Before any figure in T5, T6, T8 or T10 is written into a specification or a CI gate, re-verify it
against the primary source directly.

---

## 12. Preserved research evidence — exact paths

| Artefact | Path |
|---|---|
| Full structured corpus (27 products + 14 threads + 25 fact-checks) | `docs/design/research-evidence/CORPUS.json` |
| Product studies digest | `docs/design/research-evidence/PRODUCT-STUDIES-DIGEST.md` |
| Cross-cutting threads digest | `docs/design/research-evidence/THREAD-STUDIES-DIGEST.md` |
| Non-confirmed fact-check verdicts (90 records) | `docs/design/research-evidence/FACT-CHECK-NON-CONFIRMED.json` |
| World-model interface obligations briefing | `docs/design/research-evidence/WORLD-MODEL-INTERFACE-OBLIGATIONS.md` |
| Source and citation register | `docs/design/UI-RESEARCH-SOURCE-REGISTER.md` |
| Vertical slice specification | `docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md` |
| Raw workflow journal and per-agent transcripts *(outside the repository, path redacted)* | Local agent-runtime workspace, run `wf_a22bb7f8-302`. **Not in source control and not intended for publication.** The absolute path was redacted on 19 July 2026 because it exposed a personal account name; the run identifier is retained so the artefacts remain locatable by their owner. |

---

## 13. Research gaps that genuinely block the first vertical slice

Only three, stated honestly. Everything else can proceed on fixtures.

**G1 — Tier-promotion presentation is unspecified, and Society Pulse touches it.** Demonstrating
propagation through *real-seeming people* (proposition 2) will surface the question of what happens
when an aggregate needs to show a named individual who has not been materialised. No world-model
document answers it, and the "opening a dossier must not materialise anyone" constraint means the
obvious implementation is forbidden. **The slice can proceed only if Society Pulse is scoped to
already-materialised fixture entities** and the promotion case is explicitly out of scope.

**G2 — The confidence model is undecided (D2), and every screen renders it.** Building the chip
component before D2 means building it twice. This is the single highest-value founder decision to
take before implementation starts.

**G3 — There is no computed propagation to render.** P0.5 is not built; the tiers do not causally
influence one another. Society Pulse can only display a hand-authored fixture trace. That is
demonstrable and honest **if and only if** the fixture labelling in §8.1 holds — otherwise the slice
would assert exactly the capability the audit found absent.

**Not a blocker but worth stating:** the corpus contains no direct research on multi-hop causal-trace
interfaces *because no product implements one*. F1 is a finding about absence. The Causal Timeline is
therefore the least evidence-supported screen in the slice and the one most likely to need iteration.

---

**End of handoff. Nothing described above is implemented. This document records research and proposes
design; it approves nothing. Decisions D1–D12 are open and belong to the founder.**
