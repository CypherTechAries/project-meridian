# UI-VERTICAL-SLICE-RECOMMENDATION — the five screens of the first implementation

> # ⚠ DRAFTED — NOT FOUNDER-APPROVED — NOT IMPLEMENTED
>
> **Nothing in this document exists.** No screen, component, fixture contract or acceptance test has
> been built. This is a proposed specification, drafted by an AI agent, pending founder review. AI
> agents may draft records but may not approve decisions (`HANDOFF.md` § Standing constraints (`:138`)). Implementation is not
> authorised by this document and is gated on decision **D10** in
> [`UI-RESEARCH-HANDOFF.md`](UI-RESEARCH-HANDOFF.md) §9.

**Dated:** 19 July 2026 · **Companion:** [`UI-RESEARCH-HANDOFF.md`](UI-RESEARCH-HANDOFF.md) ·
**Evidence:** `docs/design/research-evidence/`

> **Review status.** The commissioned independent review failed three times with an infrastructure
> error and was replaced by author self-review — weaker, and disclosed as such. See
> [`UI-RESEARCH-HANDOFF.md`](UI-RESEARCH-HANDOFF.md) header. Self-review corrected the statement of
> dossier property D-2 in §0 and added the originality notes in §6a. **Independent review of this
> document is outstanding.**

---

## 0. Scope filter

The first implementation demonstrates **four propositions and nothing else**:

1. MERIDIAN contains persistent, inspectable people and organisations.
2. A crisis propagates through society, media, markets and institutions.
3. The player can propose unexpected actions in natural language and inspect the interpreted plan.
4. The player can understand why visible state changed.

Anything not materially supporting one of those four is **future backlog**. Explicit exclusions are
listed per screen and consolidated in §7.

**Three cross-cutting rules bind every screen below.**

- **P-1 Projection purity.** Every screen is a projection. Rendering, filtering, expanding, opening
  and closing must leave simulation state byte-identical and must consume **zero randomness**
  (dossier properties D-1/D-2, extended to the whole interface).
  **The required implementation is a pure function, not a substream.** Graph layout, ordering and any
  other presentational arrangement must be computed deterministically from (entity set, stable sort
  key) with no RNG call of any kind. A "dedicated presentation substream" is *not* an acceptable
  default reading of D-2 — D-2 says zero randomness, and any proposal to draw presentational
  randomness from a separate stream is a **deviation requiring founder approval**, not an
  implementation detail. *Note: even that fallback would be unavailable today — named substreams are
  P0.4A and do not exist.*
- **P-2 Dual marking.** Every text region resolves to exactly one of **engine fact** (carries a
  confidence label), **narration** (carries a provenance container), or **player input** (its own
  treatment). *Unmarked is a build failure*, enforced by a CI assertion. Marking only narration would
  inflate the authority of everything else (handoff F9).
- **P-3 Fixture honesty.** While any screen is fixture-backed, a persistent non-dismissible band reads
  `FIXTURE DATA — NOT A SIMULATION RUN`, adjacent to the mandatory `FICTIONAL WORLD` disclosure, in
  every viewport and therefore in every screenshot. A build-time assertion must prove it cannot be
  disabled in a fixture build.

---

## 1. Strategic Command Centre *(the shell)*

**Primary user question:** *"What is happening, what is urgent, and what am I being asked to decide?"*

### Essential components

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ STATUS BAR  FICTIONAL WORLD · FIXTURE DATA · HELD · Day 41 · tick 9,842      │
│             role: [single-role interim] · mode: EXPLORE · 2 decisions due    │
├────────────┬──────────────────────────────────────────┬──────────────────────┤
│ NAV        │ CENTRE — SUBSTRATE SWITCHER              │ CONTEXT PANEL        │
│            │  [M] Map  [S] Society  [C] Causal        │                      │
│ Situation  │                                          │ ── PROJECTION ────── │
│ Society    │  (one substrate at a time; none is       │ trajectory · horizon │
│ Entities   │   architecturally privileged — D1)       │ contested · foil     │
│ Timeline   │                                          │ ── WHY (Q2–Q5) ───── │
│ Composer   │                                          │ cause · rule ·       │
│            │                                          │ actors · assumptions │
├────────────┴──────────────────────────────────────────┴──────────────────────┤
│ DECISION QUEUE (≤3 + overflow)      │ EVENT STREAM (ranked, dimmed not hidden)│
└──────────────────────────────────────────────────────────────────────────────┘
```

Five landmark regions with accessible names (status / navigation / operational view / context /
event log), F6 cycling between them, roving tabindex within each so a region costs one tab stop
rather than forty, and skip links to each.

### Critical interactions

- **Substrate switch** — one keystroke each (M / S / C). Switching preserves selection.
- **Mode indication, redundantly, in three places, never colour alone**: a status-bar text chip
  carrying the literal word EXPLORE / PLAN / COMMAND plus a distinct glyph and border weight; the
  composer's own border treatment and placeholder; and the submit control's verb (*Ask* / *Draft
  order* / *Commit*). **COMMAND is non-sticky** — entered per action, self-reverting the instant an
  action resolves or is cancelled. There is no idle state in COMMAND. Mode never auto-switches; if the
  parser believes the player is attempting a mutation from EXPLORE, it offers an inline control and
  waits for a discrete act.
- **Queue vs stream are structurally different objects that never share a list.** An item may enter
  the **decision queue** only if the engine can enumerate at least one legal action composition the
  player could execute in response. Zero affordances ⇒ automatic downgrade to a stream event. This is
  HSE's rule — *status indicators must not be designated as alarms* — made machine-checkable.
- **Alerts are handled in the context panel, never a centre-screen modal**, because a suspended
  window less than 25% visible measurably raises resumption cost. Resolving or deferring restores the
  exact prior view state in one action.
- **Priorities: exactly three** (P1 IMMEDIATE / P2 SCHEDULED / P3 RECORD), defined by
  consequence-of-non-response, not drama. Priority is an immutable property of a registered alert
  class, never a per-instance field, and never model-writable.

### Fixture contracts

```ts
ShellState {
  world: { id, name, is_fictional: true }          // is_fictional must be literally true
  build: { data_source: 'fixture' | 'engine' }     // drives P-3 band
  clock: { mode: 'HELD'|'STEP'|'RUN'|'REVIEW', sim_label, tick }
  mode: 'EXPLORE' | 'PLAN' | 'COMMAND'
  queue: QueueItem[]      // ≤3 rendered + overflow count
  stream: StreamEvent[]   // ranked by engine salience; low-relevance DIMMED, never filtered out
}
QueueItem { id, alert_class_id, subject_entity_id, priority: 1|2|3,
            affordances: ActionStub[]   // MUST be non-empty or the item is not a QueueItem
            deadline_tick | null, provenance, confidence }
```

### Backend dependencies

Macro indicators may use the **real** `get_state` endpoint
(`scaffold/backend/app/api/routes_simulation.py:64`) — it exists.
Everything else is fixture. The queue/stream split is **specified but not shippable**: it depends on
stable event identity (P0.6) for dedup, resume and grouping, and on decay/cooldown mechanisms (no P0
owner) to avoid firing every tick forever against saturating indicators.

### Explicit exclusions

Time controls beyond a static clock display; branching; save/load; multi-role; settings beyond theme
and reduced-motion; onboarding; notifications outside the app; any layer taxonomy beyond the three
substrates.

### Acceptance criteria

1. Five landmark regions are reachable by keyboard; F6 cycles; each region costs one tab stop.
2. Mode is identifiable from a static greyscale screenshot without reading body text.
3. Entering COMMAND announces mode **and consequence** in one sentence via `role="alert"`.
4. No queue item renders without at least one affordance (assert in test).
5. Event stream is `role="log"` `aria-live="polite"`, present in the DOM from first paint, rate-limited
   to at most one announcement per 5 seconds, with a separate batched `role="status"` summary.
6. `FICTIONAL WORLD` and `FIXTURE DATA` are present in every viewport size tested and cannot be
   dismissed.
7. Focus is never obscured by the sticky status bar or event stream (WCAG 2.2 SC 2.4.11).

### What must be visible in screenshots

The fictional-world and fixture bands; the mode chip; the substrate switcher with the active substrate
named; a populated decision queue showing at least one affordance; an event stream showing a **dimmed**
low-relevance row beside a normal one; the context panel's projection band populated.

---

## 2. Entity Dossier

**Demonstrates proposition 1.**
**Primary user question:** *"Who is this, what do I actually know about them, and how do I know it?"*

### Essential components

**L1 — always visible, zero interaction, no scroll, no network call.** Fixed at six blocks; additions
require a documented removal:

1. Identity header — name, entity type, fidelity tier, stage-0 deterministic avatar mark.
2. **Observer banner** — *"Player intelligence profile · as assessed by [org] · last updated tick N"*.
   This is what stops the dossier reading as an omniscient encyclopaedia, and it is L1 precisely
   because it must appear in every screenshot.
3. Fictional-world badge.
4. **"Why this matters now"** — at most 5 engine-ranked rows, one sentence each. Ranked by engine-computed
   consequence weight, never by data category (Terra Invicta's failure: completeness is not a defence).
5. Confidence summary — counts by label across the visible attribute set.
6. Primary actions.

**L2 — one activation, URL-addressable, survives reload.** The ten specified sections
(Overview / Biography / Motivations / Relationships / Beliefs and knowledge / Activity / Resources
and capabilities / Public perception / Intelligence assessment / Timeline) as an **information
architecture**. Whether they render as ten tabs is **open (D8)** — the recommendation is a smaller
grouped tab set with the ten preserved underneath.

**Row anatomy — the load-bearing component of the whole slice.** Visibility and confidence are **two
structurally separate columns**, never merged into one chip:

```text
│ Attribute name        │ Visibility │ Value                    │ Confidence      │
│ Current location      │ Visible    │ Port of Kestral          │ [◧ Reported]    │
│ Security assessment   │ Restricted │ Not available to this observer │ —         │
│ Personal debt         │ Visible    │ ▨▨▨ Unknown — never observed   │ [□ Unknown] │
```

- **Unknown and Restricted are full-height rows** with the same label column and chip position as
  populated rows. The value cell renders a hatched or dotted fill — **never empty whitespace, never a
  bare em-dash** — plus a reason from a closed enum (never-observed / not-observable-to-you /
  source-lost-access / superseded-and-unrefreshed / conflicting-and-unresolved).
- **Confidence chip is triply redundant**: the full word (never abbreviated), a distinct glyph
  discriminable in silhouette at 16px, and a distinct border treatment (solid / dashed / dotted /
  double). Colour is an optional fourth channel and never the carrier. Minimum 11px, 4.5:1 text
  contrast, unambiguous in greyscale.
- **Each chip is a control, not decoration.** Activating it opens an evidence receipt: label
  definition, supporting observation count and type, age of the most recent observation, the named
  rule that produced the label, and *what would change it*.

**Relationships tab** — node-link ego-network, subject-centred, **distance 1 only, capped at 12 alters**,
with a persistent chip reading *"Showing 12 of 47 known relationships"* opening the full list.
Direction encoded by **tapered edges** (full weight at source, ~15% at target), not arrowheads.
An asymmetric pair is **one channel split lengthwise into two half-ribbons**, not two edges. Every row
in the list view renders two lines with independent confidence labels:

```text
Oduya → Navarro:  Trusts      [◧ Assessed]
Navarro → Oduya:  Distrusts   [◨ Reported]
```

Restricted edges render as **continuous, full-opacity, dashed connectors with a lock glyph** to a stub
node — never faded, never omitted. Fading is the visually obvious choice and the empirically wrong one.

### Fixture contracts

```ts
Dossier {
  entity: { id, type: 'person'|'organisation'|'business'|'community'|'institution'|'state',
            display_name, fidelity_tier: 1|2|3|4, avatar_seed: string }
  observer: { label: string, as_of_tick: number }   // drives the observer banner
  salience: SalienceRow[]                            // ≤5, engine-ranked, each names a mechanism
  sections: { [section_id]: AttributeRow[] }
}
AttributeRow {
  name, visibility: 'visible' | 'restricted',
  value: string | null,                    // null iff visibility==='restricted' or confidence==='unknown'
  confidence: 'confirmed'|'reported'|'assessed'|'disputed'|'unknown'|'possibly_deceptive'|'outdated'|'restricted',
  reason_code: string | null,              // required when value is null
  evidence: { count, kinds[], newest_tick, rule_id } | null,
  provenance: 'engine' | 'narration'
}
```

**Virtualiser rule:** the item count is the count of **fields**, not the count of *known* fields —
otherwise Unknown and Restricted rows silently vanish from the scroll model, voiding the honesty
guarantee at exactly the moment it matters.

### Backend dependencies

- **Gated on auth (D3):** the observer banner is currently a *label*, not a resolved role. Restricted
  rows in the slice are **fixture-authored**, not role-computed. This must be stated in the UI.
- **Gated on P0.4:** which view is authoritative.
- **Gated on P0.6:** Activity, Timeline, the "why" in Beliefs, and the evidence receipts behind
  confidence chips. In the slice these render with an explicit `NOT_MODELLED` reason code, not with
  fabricated evidence.
- **Gated on D2:** the label set itself.

### Explicit exclusions

Portrait stages 1–3 and any asset store (stage 0 deterministic mark only); tier promotion (**G1** — the
slice uses already-materialised fixture entities only); dossier comparison and pinning; the
self-understanding view as a separate surface (open question); community and state dossiers beyond a
stub; biography narration beyond one demonstration block.

### Acceptance criteria

1. Every rendered value carries exactly one confidence label; a value with no label fails the build.
2. Unknown and Restricted rows are present, full-height, and carry a reason code.
3. All eight labels remain distinguishable in a greyscale screenshot (rasterise-and-compare test).
4. Opening, closing and re-opening the dossier 100 times leaves fixture state byte-identical and the
   presentation RNG cursor unadvanced.
5. Screen reader announces a relationship row as direction, target, stance **and** confidence.
6. Graph layout is identical across reloads for identical input (determinism test).
7. No engine-fact and narration block share a container treatment.

### What must be visible in screenshots

The observer banner; at least one Restricted row and one Unknown row with reason codes; three
different confidence chips; the asymmetric relationship channel with both directions labelled; the
"showing 12 of 47" cap chip; a narration block with its provenance gutter beside an engine-fact row.

---

## 3. Society Pulse

**Demonstrates proposition 2.**
**Primary user question:** *"Who is this crisis reaching, through what channel, and who is it reaching next?"*

This is the differentiator screen. **It is also the one with the least evidence behind it** — no
studied product implements multi-hop propagation display, and P0.5 does not exist, so in the slice it
renders a **hand-authored fixture trace**.

### Essential components

- **Society substrate** — a **deterministic semantic-region layout, not a force-directed graph**.
  Nodes placed in fixed named bands by entity class (state organs / institutions / firms / media /
  communities / households / individuals), ordered within band by a stable engine key. Position is a
  pure function of (entity set, sort key). No physics.
- **Propagation ribbon** — the crisis's spread rendered as a **cascade over the bands**, each hop
  showing: source, channel (economic exposure / media reach / institutional obligation / social tie),
  magnitude, lag in ticks, and its own confidence label.
- **Named-individual anchor.** Every aggregate band must be able to surface **at least one named,
  materialised individual** it is about. This is the counter-measure to the Frostpunk failure —
  moral weight evaporating when people become populations (handoff R9).
- **Channel legend, permanently visible**, never hover-only.
- **"Reached / not reached / reached but unaware"** as three distinct states, with *unaware* rendered
  as content rather than absence.

### Critical interactions

- Select any node → context panel populates with that entity's exposure and the ranked list of hops
  that reached it.
- Select any hop → the causal ledger for that hop (see §5), reconciling to the stated magnitude.
- **Step the cascade** — advance hop-by-hop rather than animating continuously. Motion means causality;
  a continuously animated society view is a background attention tax.
- Any node → open its dossier. Any hop → open its causal trace. **Every inspection surface is an entry
  point to another**, not a dead end.

### Fixture contracts

```ts
Propagation {
  origin_event_id: string
  hops: Hop[]
}
Hop {
  id, from_entity_id, to_entity_id, tick_offset,
  channel: 'economic_exposure'|'media_reach'|'institutional_obligation'|'social_tie',
  magnitude: { value, unit },
  confidence: ConfidenceLabel,
  mechanism_id: string,           // must resolve; a hop with no mechanism does not render
  named_anchor_entity_id: string | null   // the individual this aggregate hop is "about"
}
```

**Hard rule:** a hop that cannot name a mechanism does not render. That is the charter's flavour-text
test applied to the propagation view.

### Backend dependencies

**Entirely fixture.** P0.5 is unbuilt — the tiers do not causally influence one another, so there *is*
no computed propagation. The screen may claim only *"an illustrative propagation, authored as fixture
data"*. Claiming otherwise would assert precisely the capability the audit found absent.

### Explicit exclusions

Map choropleths of any kind (handoff C5 — the macro tier has no sub-national denominator); market
microstructure; foreign publics beyond one stub; tier promotion (**G1**); any forecast of *future*
propagation (gated on P0.7 horizon).

### Acceptance criteria

1. Every rendered hop names a resolvable mechanism.
2. Every aggregate band surfaces at least one named individual.
3. Layout is byte-identical across reloads for identical input.
4. The screen states, in-interface, that the propagation is fixture-authored.
5. "Reached but unaware" is visually distinct from both "reached" and "not reached".
6. Stepping the cascade forward and back returns to an identical rendering.

### What must be visible in screenshots

The banded society layout; a cascade of at least four hops crossing at least three entity classes;
channel labels on each hop; a named individual anchored to an aggregate band; the fixture disclosure.

---

## 4. Conversational Command Interface

**Demonstrates proposition 3.**
**Primary user question:** *"Can I attempt this, what would it cost, and who would resist?"*

### Essential components

**The composer** — a single input, mode-scoped, with its mode carried in its own border treatment,
placeholder and submit verb.

**The Capability Index** — a persistent *"What can I attempt?"* control opening a browsable index
keyed on the 16 consequence primitives, each entry verb-first and plain-language (*"Seize an asset"*,
*"Create a legal obligation"*, *"Expose information"*) showing what it requires, who typically resists,
typical lead time, and two worked examples **drawn from current world state**. This is the answer to
handoff F10 — the capability-envisioning problem — and it is what stops a blank text box collapsing
into the pre-authored-menu failure the charter forbids. **Without it, proposition 3 is not
demonstrated; it is merely claimed.**

**The Command Card** — the only object that can be committed. Fixed section order, all sections always
present, never collapsed away when empty:

```text
┌─ COMMAND CARD ──────────────────────────── [DRAFTED] ─┐
│ 1 INTERPRETED INTENT   (one sentence, editable)       │
│ 2 COMPOSITION          ordered consequence primitives │
│ 3 AUTHORITY            legal basis, or NAMED MISSING  │
│ 4 REQUIREMENTS         what must be true              │
│ 5 COST                 resources, reserved vs spent   │
│ 6 TIME                 lead time, in ticks            │
│ 7 WHO WILL RESIST      ranked, each with a stake      │
│ 8 RISKS                                               │
│ 9 UNCERTAINTY          what the engine does not know  │
│10 FUTURE OPTIONS       enabled / removed              │
│11 REVERSIBILITY        engine-computed class          │
├───────────────────────────────────────────────────────┤
│ provenance per FIELD: solid=engine dashed=model        │
│ double=player   ·   [Commit] disabled while dashed     │
└───────────────────────────────────────────────────────┘
```

- **Provenance is tagged per field, not per card.** The commit control stays **disabled while any
  field in Composition, Authority, Requirements or Uncertainty carries a model-proposed treatment**.
  This makes the determinism boundary a mechanical property of the interface rather than a claim.
- **Four states, visually distinct**: DRAFTED (client-only) / SUBMITTED / PRICED / RESOLVED. The first
  two must never display an engine-authoritative number.
- **Refusal is a typed object, never a string** — `failed_check` (named rule id), `required_value`,
  `current_value`, `blocking_actor`, and at least one `remediation_path` with its own cost and lead
  time. The validator returns the **full blocker set**, not the first failure: "what may stop it" is a
  list, and a partial list implies a false remaining path.

### Critical interactions

- Edit any card field; the card re-prices. **Re-pricing consumes zero authoritative randomness**;
  forecast ranges draw from a substream seeded by (card id, revision), so re-opening shows identical
  numbers.
- Unresolved referents render as **UNRESOLVED SLOT** chips inline, resolved from an engine-enumerated
  candidate list drawn from the player's own intelligence view — never by model guessing. Cap at three.
- **Confirmation is graded by engine-computed reversibility class**, not applied uniformly — uniform
  confirmation modals are click-through within an hour and fail on the one order that mattered.
  **Until a real revert mechanism exists, no undo control may appear anywhere**, and the reversibility
  strip renders the engine-computed statement that the action cannot be un-ordered.
- Voice may **draft** but never commit.

### Fixture contracts

```ts
CommandCard {
  id, revision, state: 'DRAFTED'|'SUBMITTED'|'PRICED'|'RESOLVED'
  interpreted_intent: Field<string>
  composition: Field<Primitive[]>
  authority: Field<{ basis: string | null, missing: string | null }>
  requirements: Field<Requirement[]>
  cost: Field<Cost[]>; time: Field<{ lead_ticks }>
  resistance: Field<{ entity_id, stake, strength }[]>
  risks: Field<string[]>; uncertainty: Field<string[]>
  future_options: Field<{ enabled: string[], removed: string[] }>
  reversibility: Field<{ class: 'R0'|'R1'|'R2'|'R3', statement: string }>
}
Field<T> = { value: T, provenance: 'engine'|'model'|'player', confidence?: ConfidenceLabel }
Refusal { failed_checks: FailedCheck[] }   // plural, always
```

### Backend dependencies

The engine cannot validate legality, price actions, or enumerate resistance today — documentation
claiming it does is publication blocker **B1**. In the slice, pricing and resistance are **fixture**,
and the card must say so. Commit is **not wired**: the demonstration ends at PRICED. Wiring commit
requires the authoritative-state contract (P0.4) and event-sourced history (P0.6).

### Explicit exclusions

Voice input; image and document ingestion (**and with it the entire prompt-injection surface** — this
exclusion is deliberate and load-bearing: the quarantined-reader architecture in handoff R10 must
exist *before* any in-world content is ingested); multi-step plans; delegation; scheduling; staged
orders; undo.

### Acceptance criteria

1. Commit is mechanically disabled while any load-bearing field is model-proposed (assert in test).
2. A refusal renders every failed check, with a remediation path for at least one.
3. The Capability Index is reachable in one activation from the composer and lists all 16 primitives,
   inactive ones included with a reason.
4. Re-opening a card at the same revision renders identical numbers.
5. Mode is unambiguous in a greyscale screenshot of the composer alone.
6. No card in DRAFTED or SUBMITTED displays a number styled as engine-authoritative.

### What must be visible in screenshots

A command card with mixed per-field provenance and a **disabled** commit control; a refusal card
showing multiple blockers and a remediation path; the Capability Index open with active and inactive
primitives; the composer in COMMAND mode with its distinct treatment.

---

## 5. Causal Timeline

**Demonstrates proposition 4.**
**Primary user question:** *"Why did this number move, and what would have happened otherwise?"*

**This is the least evidence-supported screen in the slice** (handoff F1 / G-note): no studied product
implements multi-hop causal tracing, so this is original design and should be expected to iterate.

### Essential components

**Layer 1 — one contrastive sentence, hard-capped at two named causes**, using a fixed engine template:

```text
Port throughput fell 12% rather than holding near baseline,
because insurer repricing raised transit cost and two operators rerouted.
```

Human explanation is contrastive and selective — leading with a complete modifier ledger is the wrong
layer-one artefact. The *foil* is not authored: it is the engine's already-computed no-action baseline.

**Layer 2 — a reconciling ledger, not a chart.** Every contributing term is a row: name, signed value,
unit, mechanism id, provenance badge. **The ledger must sum exactly to the displayed delta.** Terms
below threshold collapse into *"N smaller contributions, totalling ±X"* — never silently dropped. Any
arithmetic gap renders as an explicit **UNEXPLAINED RESIDUAL** row. That row is the honesty mechanism:
it makes an incomplete model visible instead of plausible.

**The Eight Questions as a fixed eight-row scaffold**, always rendering all eight, never as prose. A
question the engine cannot answer renders as a present row with a machine-set reason code —
`NOT_MODELLED` / `INSUFFICIENT_EVIDENCE` / `RESTRICTED_TO_THIS_OBSERVER` / `DEFERRED_TO_TICK_N`. A
build test asserts no shipped outcome renders an empty row without a reason code.

**Layer 3 — the trace view**, a separate route (`/run/{id}/trace/{event_id}`), not a third nested
disclosure. Layered DAG with a fixed spatial grammar: **x = tick, y-band = tier** (macro / meso /
micro as three lanes), all edges one direction. **Bounded in the data layer, not the layout layer** —
default to the k highest-contribution ancestors (k=7 proposed) plus one aggregate node. Every node
carries an origin badge (ENGINE / INPUT / PROPOSED / **NARRATED**), and **NARRATED nodes render
outside the graph in a side rail, structurally incapable of appearing on a causal path**, enforced by
a test asserting no rendered path traverses a narrated node.

### Critical interactions

- **The path view** — pick a source, pick an outcome, render the ranked contributing chains. This is
  the specific answer to the one-hop limit that defeated every studied product, and it is the
  screen's reason to exist.
- Pin any explanation as a persistent panel. Explanation surfaces must be as persistent as the
  decisions they inform — hover-only causal derivations are the recurring failure across the corpus.
- Any ledger row → the entity or mechanism behind it. **Act on a row in place** where possible; an
  explanation the player cannot act on from where they read it becomes read-only trivia.

### Fixture contracts

```ts
CausalTrace {
  event_id, tick, subject: { metric, delta, unit }
  contrastive: { statement: string, foil: string, causes: [string, string?] }
  ledger: { name, signed_value, unit, mechanism_id, provenance }[]
  residual: { value, unit } | null      // rendered explicitly when non-zero
  eight_questions: { [q1..q8]: { answer: string | null, reason_code: string | null } }
  ancestors: TraceNode[]                 // capped; origin badge per node
}
```

### Backend dependencies

**Gated on P0.6 — hard.** There is no event-sourced history; `causal_parents` are discarded; nothing
persists. Q2 and Q3 must be **persisted per outcome**, not recomputed on demand. In the slice the
entire trace is fixture.

**Q7 (alternative outcomes) is gated on P0.4A and must ship in `NOT_MODELLED` state.** A counterfactual
re-run must consume identical RNG substream draws so the perturbed input is the *only* difference.
Without named substreams, "if X had been different, Y would have been" is partly resampling noise
presented as causation — the exact class of unfounded claim this project exists to eliminate.
**Shipping a plausible-looking counterfactual before substreams exist would be the single most damaging
thing this interface could do.**

### Explicit exclusions

Branching and branch comparison; time-travel scrubbing; after-action review mode; annotation;
bisect ("when did this become inevitable"); counterfactual execution of any kind.

### Acceptance criteria

1. The ledger sums to the displayed delta, or an explicit residual row renders.
2. All eight question rows always render; none is empty without a reason code.
3. No rendered causal path traverses a narrated node (assert in test).
4. Layer 1 never exceeds one sentence and two named causes.
5. The trace is reachable by keyboard and its DAG has a screen-reader-available tabular equivalent.
6. Q7 renders `NOT_MODELLED` — and there is a test asserting it *cannot* render a counterfactual value
   while named RNG substreams are absent.

### What must be visible in screenshots

The contrastive sentence; the reconciling ledger with a visible residual row; all eight question rows
including at least two carrying reason codes; the layered trace with tier lanes and a narrated node
visibly outside the graph.

---

## 6. Build order

| Stage | Contents | Unlocked by | May claim |
|---|---|---|---|
| **S0** | Tokens, chips, rows, provenance containers, themes, contrast gates | Nothing — buildable now | "A contrast-tested design system exists" |
| **S1** | Shell + macro indicator panel | S0; `get_state` exists | "A shell renders real macro state" — *and that the state saturates* |
| **S2** | Entity Dossier over fixtures | S0, S1, **D2** | "The dossier renders a fixture projection" |
| **S3** | Command composer + Capability Index to PRICED | S2 | "Intent can be composed, interpreted and inspected" |
| **S4** | Society Pulse over a fixture trace | S2 | "An illustrative propagation is rendered from fixture data" |
| **S5** | Causal Timeline over a fixture trace | S2, S4 | "A causal trace is rendered from fixture data" |
| — | Anything role-filtered | **auth (D3)** | — |
| — | Activity, Timeline, evidence receipts as *real* | **P0.6** | — |
| — | Counterfactuals, stable generated portraits | **P0.4A** | — |
| — | Computed propagation | **P0.5** | — |
| — | Alerts, thresholds, forecasts | **decay/cooldown + P0.7** | — |

**S2 should not begin before D2 is taken.** The confidence chip appears on every screen; building it
before the label model is decided means building it twice.

### 6b. Effort realism — read before committing to all five screens

This specification is written with more confidence than a solo effort can execute quickly, and that
should be said plainly rather than discovered later. Football Manager cancelled an entire annual
release over interface quality with a studio and a major publisher behind it (handoff C10).

Rough solo estimates, offered as **order-of-magnitude only** and not as a plan:

| Stage | Rough solo effort | Note |
|---|---|---|
| S0 design system + contrast gates + themes | 2–3 weeks | Front-loaded; everything else depends on it |
| S1 shell + macro panel | 1–2 weeks | The only stage touching real engine data |
| S2 dossier | 3–5 weeks | The row/chip/evidence-receipt component is the expensive part, not the tabs |
| S3 composer + Capability Index | 3–5 weeks | The Capability Index is a content-authoring job as much as a build |
| S4 Society Pulse | 2–4 weeks | Plus fixture-trace authoring |
| S5 Causal Timeline | 3–5 weeks | Least precedent, most iteration |
| Fictional-world GeoJSON authoring | 1 week | Scheduled work item, not an incidental asset |

**Total: roughly 4–6 months of solo effort**, against a Phase 0 that is unfinished and takes priority.

**If the slice must be smaller, cut in this order.** Society Pulse (S4) first — it is entirely
fixture, has the least evidence behind it, and its proposition can be partly carried by the dossier's
relationship tab plus the causal ledger. Then the Capability Index's *content* (ship the surface with
four primitives rather than sixteen). Do **not** cut the confidence/provenance row component: it is
the honesty layer, it appears on every screen, and it is what makes the difference between a demo and
a defensible claim.

**Minimum subset still demonstrating all four propositions:** S0 + S1 + S2 + a reduced S3 (composer to
PRICED, four primitives) + a reduced S5 (contrastive sentence, reconciling ledger, eight-question
scaffold — no trace DAG). That is roughly 9–14 weeks and demonstrates persistent inspectable entities,
natural-language proposal with an inspectable plan, and understanding why state changed. **Proposition
2 (propagation) would be demonstrated weakly**, through relationship and ledger surfaces rather than a
dedicated screen — which is an honest trade to put to the founder, not a decision to take here.

---

## 6a. Originality notes — trade-dress review of the named patterns

Self-reviewed against the no-trade-dress rule. **Nothing here must be struck; two patterns need an
explicit originality discipline recorded before they are designed.**

| Pattern | Verdict | Note |
|---|---|---|
| Confidence chip | **Clear** | Derived from open standards (shape-before-colour redundancy in NATO APP-6 / MIL-STD-2525; WCAG redundancy rules), not from any product's visual identity. |
| Ego-network tapered / split-channel edge encoding | **Clear** | Tapered-edge direction encoding comes from published visualisation research, not a product. The split-channel asymmetric ribbon is original to this specification. |
| Substrate switcher | **Clear** | A generic pattern. Must not adopt any product's *naming* for its views. |
| Capability Index | **Clear** | Original. The underlying idea (make the action vocabulary browsable) is generic. |
| Observer banner | **Clear** | Original to MERIDIAN's four-view model. |
| **Reconciling ledger** | **Needs originality note** | The *function* — itemised modifier breakdown summing to a delta — is a well-established convention with a strong association to one publisher's tooltip idiom. Take the function; do not reproduce its visual signature (the nested hover-chain, the bracketed modifier styling, the tooltip-within-tooltip presentation). MERIDIAN's ledger is a **persistent panel**, not a hover artefact, which is both a usability improvement and the clearest point of visual divergence. |
| **Command card** | **Needs originality note** | The plan-as-artifact structure is convergent across several shipped agent products. The *structure* is functional and freely transferable; the section naming, ordering and visual treatment must be MERIDIAN's own and derive from the 16 consequence primitives and the Eight Questions rather than from any product's card layout. Do not reproduce a recognisable approval-prompt idiom. |

**Standing rule for the visual-system track:** every pattern that originated in analysis of a named
product must carry a recorded note stating what was taken (the principle) and what was deliberately
not taken (the expression). That record is the project's evidence of originality.

---

## 7. Consolidated exclusions — future backlog

Map layer taxonomy beyond three substrates; choropleths; hexbin and fidelity-bound rendering;
onboarding, tutorial and codex; the adviser rail; time controls, pause semantics, branching, replay,
after-action review, bisect; portraits beyond stage 0 and any asset pipeline; tier promotion
presentation (**G1**); voice; image and document ingestion and the quarantined-reader architecture;
multi-role and multiplayer; scenario authoring; save/load and run management; the operational military
layer (**D12**); localisation; the matrix relationship view; SAGAT harness and formal evaluation
tooling; light theme beyond token support; export.

**None of this is rejected.** It is researched, preserved in `docs/design/research-evidence/`, and
deferred because it does not materially support one of the four propositions.

---

**End of specification. Nothing described above is implemented. Implementation is gated on founder
decision D10, and D2 should be taken before S2 begins.**
