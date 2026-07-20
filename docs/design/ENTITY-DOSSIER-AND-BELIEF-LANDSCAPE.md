# Entity Dossier and Society Belief Landscape — design for review

**Status: DESIGN ONLY. Nothing here is implemented.** No application code was written, no simulation
functionality was added, no test was changed. The mockups are static HTML rendered to PNG and live in
`docs/design/mockups/`. They must never be presented as screenshots of working software — each one
carries a `DESIGN MOCKUP — NOT IMPLEMENTED SOFTWARE` banner for exactly that reason.

Every belief value, exposure state and organisation result shown comes from the merged engine on
`main`. Nothing was invented to improve a composition.

---

## 1–4. The four mockups

| # | Screen | File |
|---|---|---|
| 1 | Entity Dossier — **person** (broadcast journalist) | [`mockups/mockup-1-person-dossier.png`](mockups/mockup-1-person-dossier.png) |
| 2 | Entity Dossier — **organisation** (public broadcaster) | [`mockups/mockup-2-organisation-dossier.png`](mockups/mockup-2-organisation-dossier.png) |
| 3 | Entity Dossier — **population group** (inland households) | [`mockups/mockup-3-population-group-dossier.png`](mockups/mockup-3-population-group-dossier.png) |
| 4 | **Society Belief Landscape** | [`mockups/mockup-4-society-belief-landscape.png`](mockups/mockup-4-society-belief-landscape.png) |

Source: [`mockups/dossier-landscape.html`](mockups/dossier-landscape.html), using the existing
`tokens.css` palette so the design sits inside the approved Briefing View visual language rather than
beside it.

**The subjects were chosen to stress the design, not to flatter it.** The journalist is the person
whose result is *least* dramatic. The broadcaster is the organisation that *refuses* to take a
position. Inland households are the group the engine knows *least* about. If the design reads well
for these three, the confident cases are easy.

### Structural decisions worth flagging

**No decimals anywhere in the default view.** `0.408458` becomes "moved a little towards believing
it". The precise figures live behind `INSPECT CALCULATION`. A four-decimal number on a person's face
implies a precision about human beings that this engine does not have, and putting it in the default
view would undo the claim boundary the whole milestone rests on.

**"Not modelled yet" is a first-class panel, not a footnote.** On every dossier it occupies a full
column at the same visual weight as the results. This is the panel most likely to be quietly demoted
during implementation; the design deliberately makes that demotion visible.

**Cards, not a network graph.** The landscape question is "who saw it, and what did they make of
it" — a scanning question. A force-directed graph would look more technical and answer it worse.

**The organisation split is physical.** "What people inside think" and "what the organisation
officially says" are two panels side by side with a hard border between them, because the entire
point is that they are different things. They can never merge into one number.

**The empty space on the population screen is the design.** Where a pie chart would sit, there is a
hatched panel reading `BREAKDOWN NOT AVAILABLE`. Not drawing the chart is the feature.

---

## 5. Five-second orientation test

*What can a reader answer within five seconds of the screen appearing?*

| Screen | Verdict | What lands first |
|---|---|---|
| Person | **PASS** | Name, "PERSON", the claim in quotes, then one 25px sentence: *"The journalist moved a little towards believing the claim — but still does not have enough proof to report it as established."* Who, what claim, what happened. |
| Organisation | **PASS** | Same shape, and the answer sentence names the cause: *"…because half of the people inside it are still undecided."* The 30/50/20 bar is the only chart and reads instantly. |
| Population group | **PASS** | *"Inland households never received this claim…"* plus a `✕ DID NOT RECEIVE IT` chip. The most important fact is also the largest. |
| Landscape | **PASS, with one caveat** | The claim as a headline, then `SAME CLAIM — THREE RESPONSES` in three columns. A reader gets the whole thesis from that band alone. **Caveat:** the full screen is 1,700px tall, so bands below the fold need a deliberate scroll. The three-person comparison is placed above it precisely so the point survives without scrolling. |

**Residual risk.** On the person screen the eye may land on the portrait glyph before the answer
sentence. Worth checking with a real reader; if it happens, reduce the portrait to 96px.

## 6. Ten-year-old, ten-minute test

*Could a ten-year-old, given ten minutes, explain the main idea to someone else?*

| Screen | Verdict | The sentence they would repeat |
|---|---|---|
| Person | **PASS** | "He heard the story but his boss says you need more proof before you can say it on TV, so he's not sure yet." |
| Organisation | **PASS** | "Half the people there hadn't made up their minds, so the company didn't say anything." |
| Population group | **PASS** | "They never heard about it, so nothing changed for them. That's different from saying they didn't believe it." |
| Landscape | **PASS** | "Three people heard exactly the same thing and thought different things — and it wasn't because of their jobs." |

Words on screen that a ten-year-old may not know: *corroboration*, *allegation*, *undecided*,
*withholds*. **Recommendation:** replace *corroboration* with "more proof from somewhere else" and
*allegation* with "claim" at implementation. *Undecided* and *withholds* are worth keeping — they are
the right words and the surrounding sentence teaches them.

**Zero occurrences** on any default view of: credence · provenance · contextual threshold · update
weight · alignment · aggregation · state model · denominator · propensity · epistemic.

---

## 7. Every visible sentence and its source

`E` = computed by the merged engine · `F` = fixture (story text) · `?` = declared unavailable ·
**`P`** = **presentation wording that does not exist yet** — see §11.

### Mockup 1 — person

| Visible text | Source |
|---|---|
| "Correspondent, Northshore Broadcast" | `F` `cast.PEOPLE[2].display_name` |
| "Covers the strait for the public broadcaster." | `F` `cast.PEOPLE[2].bio` |
| The claim in quotes | `F` `cast.PROPOSITIONS` → `claim_text` |
| "moved a little towards believing the claim" | `E` Δ +0.058458 → **`P`** band wording |
| "still does not have enough proof to report it as established" | `E` `is_uncertain = True`, confidence 0.442375 → **`P`** |
| BEFORE "Doubted it" | `E` prior 0.35 → **`P`** band wording |
| NOW "Still unsure" | `E` final 0.408458 → **`P`** |
| "A **small step** towards believing it." + 41% bar | `E` 0.408458 → **`P`** |
| "More settled than before, but **still short of sure**." + 44% bar | `E` confidence 0.25 → 0.442375 |
| "**Yes** — over the newsroom wire." | `F` exposure path · `E` exposure state |
| Reason 1 — broadcaster requires corroboration | `F` threshold rationale, quoted nearly verbatim |
| Reason 2 — evidence only moderately strong | `E` evidence strength 0.45 → **`P`** |
| Reason 3 — had not previously accepted it | `E` prior 0.35 → **`P`** |
| "Not modelled yet" tag list | `F` static, from `WHAT-MERIDIAN-CAN-DO.md` |

### Mockup 2 — organisation

| Visible text | Source |
|---|---|
| "Northshore Public Broadcast" / bio | `F` `cast.ORGANISATIONS[1]` |
| "does not take a firm public position, because half of the people inside it are still undecided" | `E` position `uncertain`, strength `withheld`, uncertain bloc 0.50 → **`P`** |
| 30% / 50% / 20% bar | `E` `internal_blocs` |
| "Moderately divided — **not united enough** to speak firmly." + 55% bar | `E` cohesion 0.55 vs firm threshold 0.60 → **`P`** |
| "No firm position" | `E` `official_position = uncertain` |
| "Neither — it is holding back." | `E` `action_direction = withhold` |
| "None. A withheld position carries no force." | `E` `action_intensity = 0.0` |
| Decision reasons 1–3 | `E` position derivation + `F` objectives |

### Mockup 3 — population group

| Visible text | Source |
|---|---|
| "Inland households" / "402,000 people" | `F` name · `E` `represents_population` |
| "never received this claim, so their earlier view stayed exactly as it was" | `E` coverage `unexposed`, delta 0.0 → **`P`** |
| "✕ DID NOT RECEIVE IT" | `E` `ExposureCoverage.unexposed` |
| BEFORE / NOW "Unsure" → "Unsure" | `E` 0.35 retained, `belief_lean = uncertain` |
| "**None at all.** Their earlier view carried forward untouched." | `E` `event_driven_delta = 0.0` |
| "The fictional story `F` — not the engine. The engine only decided **not to change it**." | `E` `RetainedPrior.prior_origin = FIXTURE`, `decision_origin = ENGINE` |
| "BREAKDOWN NOT AVAILABLE" + reason | `?` `distribution_status = unavailable` + its stated reason |
| The 5-out-of-10 illustration | `F` from the approved message bank |

### Mockup 4 — landscape

All twelve cards: names `F`; received/not-received `E`; result wording `E` → **`P`**; one-line reasons
`F` (people, organisations, from threshold rationales and position derivations) but **`P` and
currently unsourced for the six population groups** — see §11. "Four in ten people never heard it"
is `E` (402,000 / 1,001,000). The substitution claim is `E` and verified by test.

---

## 8. What each screen says MERIDIAN does not know

| Screen | Where it appears | What it says |
|---|---|---|
| Person | Full third column, `NOT MODELLED YET` | Memories, relationships, changing trust, emotional state, personal history, what they saw before, order of earlier events, life beyond this run. Plus: *"MERIDIAN can explain how this claim changed their current view. It cannot yet explain how years of memories, relationships and earlier events shaped them."* |
| Organisation | Full panel, `NOT MODELLED YET` | Internal politics, who persuades whom, past decisions, changing trust, named individuals inside, how the groups formed. Plus: *"It is not a mind, and it has no institutional memory."* |
| Population group | Full third column, `WHAT WE DO NOT KNOW`, hatched | `BREAKDOWN NOT AVAILABLE` and the 5-out-of-10 explanation. |
| Landscape | Legend `?` marker; `Breakdown not available` on all six group cards; closing note on exposure vs belief | That four in ten people never heard the claim, and that unchanged is not the same as disagreeing. |

**No evaluative belief change appears anywhere**, because evaluative updating is not implemented. No
screen implies memory, path dependence, changing trust, personalised feeds, psychological
completeness or persistence across runs.

## 9. Navigation from the existing Command Centre

Today: **Briefing** ⇄ **Analysis**, a two-state switch. Proposal — add one peer, not a hierarchy:

```
  Briefing  |  Society  |  Analysis
     ↑          ↓ click any entity card
     |      Entity Dossier  ──  ‹ SOCIETY  returns
     └──────────────────────────────────┘
```

- **Society** becomes a third top-level tab. The Landscape is the society-wide view; a dossier is one
  entity within it.
- Entity cards on the Landscape are the only route into a dossier. Every dossier carries a
  `‹ SOCIETY` control back.
- Briefing gains **one** entry point — a "See how people responded" link on the narrative
  consequence card. One, not several: Briefing's discipline is a single primary action.
- Dossiers are reachable from Analysis via entity identifiers, for a technical reader arriving from
  the other direction.
- **No modal dialogs.** A dossier is a place, not an overlay.

## 10. Recommendations

**Default landing screen: keep Briefing.** The Landscape is the more novel screen, but Briefing
answers "what is going on" and the Landscape answers "how did people react to one claim" — which is a
second question. Landing on the Landscape would make MERIDIAN look like a belief-analysis tool rather
than a society simulator. Revisit once more than one claim exists.

**Public GitHub hero: keep the Briefing View for now; add the Landscape as the second image** once
implemented, replacing the current Analysis View position, with Analysis moving further down. The
Landscape is the better *story* image — twelve entities, one claim, visible divergence — but the hero
must show the product's front door, and that is Briefing.

**Primary demo sequence** (about three minutes):

1. **Briefing** — "a blockade, and here is what it is doing to people." Establish the world.
2. **Counterfactual** — remove carrier rerouting, watch downstream collapse. Establish that the
   causal chain is real.
3. **Society Belief Landscape** — "now one claim enters this society." Land on `SAME CLAIM — THREE
   RESPONSES`.
4. **Person Dossier (journalist)** — "why is he still unsure?" Three reasons, none of them his job.
5. **Population Group Dossier (inland households)** — "and four in ten people never heard it at
   all." Close on `BREAKDOWN NOT AVAILABLE`.

Ending on what the system does *not* know is deliberate. It is the most credible thing MERIDIAN can
show a sceptical audience, and it is the hardest thing for a competitor to imitate honestly.

---

## 11. Data the design needs that the engine does not currently provide

Six gaps. The first is structural and blocks everything else.

### A. There is no API route serving belief data at all — **BLOCKER**

The belief package is imported by **nothing** outside itself and its own tests. Verified:

```
grep -rln "simulation.belief" app | grep -v "app/simulation/belief/"   → no matches
```

Existing routes cover runs, state, mechanisms, decisions and events. **None returns a belief,
exposure state or organisation position.** The engine computes every value in these mockups and no
client can reach a single one of them. A route and a read-only projection must exist before any
screen can be built. This is the first implementation task, and it is larger than it looks.

### B. Plain-language band wording does not exist — every **`P`** above

"Doubted it", "Still unsure", "a small step", "Moderately divided" — none of these strings exists.
The engine emits numbers and enum values. Something must map value bands to approved words.

**Recommendation:** a versioned wording table in the presentation layer, tested, so the vocabulary is
reviewable and cannot drift per screen. It must be a *projection*, never a field on an engine result
— the engine must not start authoring prose about people.

### C. Population groups have no per-group reason

People carry threshold rationales and organisations carry position derivations, so their one-line
reasons are honestly sourced. **Cohorts carry no equivalent.** `public_sentence` describes the
outcome, not the cause. The six group cards on the Landscape currently show only
`Breakdown not available` in the reason slot, which is honest but thin.

**Options:** (i) accept the asymmetry and show exposure path instead; (ii) add declared reason text
to cohort fixtures, marked `F`; (iii) derive a reason from exposure intensity and relay. **(i) is
recommended** — it is the only option that adds no new claim.

### D. Cohorts carry no confidence

`CohortReport` has no confidence field, so the "how sure they are" row cannot appear on a population
dossier. The design omits it rather than borrowing the person shape. **No change requested** — this
is a real absence and the screen should keep showing it as one.

### E. No portrait or identity assets exist

The mockups use CSS glyphs (`◑ ▣ ◍`) as placeholders. Original fictional identity panels are needed —
**symbolic, never faces**. Photographic portraits of fictional people invite exactly the
real-person confusion the B5 controls exist to prevent, so this should be a deliberate house style:
geometric identity marks, not characters.

### F. No route or state for a third top-level tab

Briefing/Analysis is a two-state switch. Adding **Society** needs a third state, deep links to
individual dossiers, and a back-navigation contract.

**None of these gaps should be closed before this design is approved**, and closing A–B is itself a
milestone-sized piece of work that deserves its own review.

## 12. Confirmation

**No new simulation functionality was added.** This branch contains two files: one HTML mockup and
this document, plus four rendered PNGs. Nothing under `scaffold/` was touched. No engine code, no
frontend code, no test, no fixture, no rule pack. Backend 384 and frontend 64 are unchanged from
`main` and were not re-run, because nothing they cover was modified.

**Stopping here for founder visual review before any implementation begins.**
