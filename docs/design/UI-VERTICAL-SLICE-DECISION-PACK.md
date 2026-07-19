# UI vertical slice — decision pack

**Status:** DRAFT, pending founder review · **Date:** 19 July 2026
**Scope:** the five C0 screens only. Nothing here is implemented except where explicitly stated.

> Derived from `UI-RESEARCH-HANDOFF.md` and `UI-VERTICAL-SLICE-RECOMMENDATION.md`, reconciled in
> `UI-RESEARCH-INTEGRATION-MEMO.md`. Where research and founder decision conflict, **the founder
> decision is implemented** and the conflict is recorded in the memo, §2.

---

## 0. Rules binding every screen

**Disclosures — verbatim, persistent, non-dismissible, visible in every viewport and screenshot:**

```
FICTIONAL SIMULATION — NOT REAL-WORLD INTELLIGENCE OR PREDICTION
INTERACTIVE PROTOTYPE — FIXTURE DATA — NOT CONNECTED TO THE SIMULATION ENGINE
```

The fictional-world disclosure must survive **cropping** — so it cannot be a single page-level
banner. Every panel carries a crop-invariant marker (a left gutter rule plus a text token), so a
cropped screenshot of one card still declares itself.

**Epistemic vocabulary — exactly these, no others:**
`AUTHORITATIVE` · `ASSESSED` · `DISPUTED` · `UNKNOWN` · `PRESENTATION_ONLY`
Confidence: `HIGH` · `MEDIUM` · `LOW` · `NOT_APPLICABLE`

- `AUTHORITATIVE` describes **state quality, not player access**.
- **No numeric confidence percentages.** No number appears unless a documented mechanism produced it.
- **Unknown ≠ unavailable ≠ zero.** All three render distinctly.
- Disputed information preserves competing assessments.
- One compact visible treatment; detail on expansion. Do not overload every card.

**Must never be implied, on any screen:** live model calls · authoritative validation · real
cross-tier propagation · event sourcing · replay · state hashing · persistence · role-based access
enforcement · tier promotion · real benchmarks.

**Every aggregate exposes a ranked contributor list naming the mechanism behind each contributor**,
or it does not ship (research T18 — fact-checked).

**Accessibility floor for C0:** semantic landmarks, keyboard reachability, focus visibility, text
alternatives, no colour-only encoding. **No conformance claim is made** — light and high-contrast
themes do not exist yet, and dark-only cannot be called accessible.

---

## 1. Strategic Command Centre — **implemented in this block**

**Primary user question:** *"What is happening, what is urgent, and what am I being asked to decide?"*

**Essential information.** One active fictional maritime crisis; civilian and hostage-family
reactions; media and social narratives; shipping and insurer behaviour; economic and employment
exposure; domestic political pressure; foreign governments; foreign-public reactions; uncertainty and
provenance on every claim; decisions awaiting the player.

**Critical interactions.** Select any card → the right context panel shows its full provenance,
epistemic status, visibility basis and last-updated tick. Expand the propagation chain to see each
hop. Keyboard reachable throughout; five landmark regions.

**Fixture requirements.** One versioned scenario file containing the crisis, eight propagation-chain
hops, entity references, narrative items, market and insurer effects, political pressure items,
foreign reactions, and a decision queue. Every record carries the full envelope (§6).

**Future engine dependency.** C1 — indicators from a versioned authoritative snapshot (P0.4).
C2 — the propagation chain computed rather than authored (P0.4A + P0.5). C3 — decision queue with
real dedup, resume and causal grouping (P0.6). Decay/cooldown before any threshold alerting.

**Provenance and epistemic treatment.** Every card carries a status chip and a provenance line.
Fixture origin is marked on the card itself, not only in the page banner.

**Explicit exclusions.** Map engine; substrate switcher; time controls; branching; save/load;
multi-role; settings; onboarding; notifications; alert priority mechanics; live indicators.

**Must not imply.** That the propagation chain was computed, simulated, emergent or live; that any
indicator came from the engine; that a decision can be executed.

---

## 2. Entity Dossier — *specified, not implemented in this block*

**Primary user question:** *"Who is this, what do I actually know about them, and how do I know it?"*

**Essential information.** Overview; biography; motivations; relationships; beliefs and knowledge;
activity; resources and capabilities; public perception; intelligence assessment; timeline —
preserved as **information architecture**, not necessarily as ten tabs (research C8).

**Critical interactions.** Open from any entity reference. Inspect any field's provenance. Follow a
relationship edge. **Opening a dossier must never materialise, promote or mutate an entity, and must
consume zero randomness** (founder G1; dossier property D-2).

**Fixture requirements.** Pre-materialised fixture entities only, explicitly declared materialised.
Non-materialised individuals appear as aggregate or minimal-reference records with an honest
unavailable state — never silently generated biography, beliefs or identity.

**Future engine dependency.** Auth layer for role-filtered views (no Phase 0 owner — audit places IAM
in Phase 2); P0.4 for what the projection is *of*; P0.6 for evidence behind assessments.

**Provenance treatment.** Every field row carries epistemic status and visibility basis. `UNKNOWN`
and `Restricted` render as present rows, never omissions — and the virtualiser's item count must be
the count of **fields**, not known fields, or those rows vanish from the scroll model.

**Explicit exclusions.** Generated portraits beyond a deterministic geometric mark (D6 stage 0);
promotion presentation; multi-role comparison.

**Must not imply.** Role-based access enforcement; that any assessment has evidence behind it.

---

## 3. Society Pulse — *specified, not implemented in this block*

**Primary user question:** *"Who is this crisis reaching, through what channel, and who is it reaching next?"*

**Essential information.** The eight-hop chain: maritime crisis → insurer risk assessment → carrier
rerouting → port and employment exposure → household expectations → media and family activity →
political pressure → government options. Cohorts and organisations at each hop, with population
weighting.

**Critical interactions.** Follow a hop; open a named entity at any hop; inspect why a hop occurred.

**Fixture requirements.** A **hand-authored, versioned fixture trace** (founder G3). Every hop
carries provenance and is marked fixture-origin.

**Future engine dependency.** **P0.5 is the whole screen.** Until cross-tier causal channels exist,
this is an illustration. C2 is the first point at which MERIDIAN may truthfully claim it simulates a
societal response.

**Explicit exclusions.** Computed propagation; tier promotion; live cohort state.

**Must not imply — the sharpest constraint in the pack.** The trace must **never** be described as
computed, simulated, live or emergent. The tiers do not causally influence one another today, and the
apparent meso→macro movement in the scaffold is shared-RNG contamination, not causality.

---

## 4. Conversational Command Interface — *specified, not implemented in this block*

**Primary user question:** *"Can I attempt this, what would it cost, and who would resist?"*

**Essential information.** Free-text intent; the interpreted **plan as an inspectable artefact**;
required resources; likely resistance; blockers.

**Critical interactions.** Compose intent → render an editable structured plan → explicit approval
gate. **Plan-as-artifact, not chat.** Research F10: the failure mode is capability envisioning, not
parsing — a perfect parser on an unknowable capability space collapses into the pre-authored menu the
charter forbids. Modes EXPLORE / PLAN / COMMAND indicated redundantly, never by colour alone; COMMAND
is non-sticky.

**Fixture requirements.** Canned interpretations for a small set of demonstration intents, each
visibly marked as a fixture interpretation.

**Future engine dependency.** Live gateway; validation and pricing (blocker B1 — `_validate_and_price`
is a seven-entry dict lookup that never receives the agent specification). Refusals must return the
**full** blocker set, not the first failure.

**Explicit exclusions.** Live model calls; execution; voice; image input; multimodal ingestion.

**Must not imply.** That anything is validated, priced, legal or executable. C0 reaches the
**DRAFTED** state only. Approved wording: *"The architectural mutation boundary exists in scaffold
form, but live model integration, external-input recording and replay have not yet been implemented."*

---

## 5. Causal Timeline — *specified, not implemented in this block*

**Primary user question:** *"Why did this number move, and what would have happened otherwise?"*

**Essential information.** Events with parent/child relationships; rule and mechanism attribution;
before/after state; assumptions and uncertainty.

**Critical interactions.** Select an outcome → follow contributing chains **multi-hop**. Research F1:
no shipped product solves multi-hop tracing — Democracy 4 reveals exactly one hop. This is MERIDIAN's
whitespace **and** its principal risk, and it is the least evidence-supported screen in the slice.
Ship a ranked **path view**, not neighbour-reveal.

**Fixture requirements.** A labelled fixture causal trace with parent/child links.

**Future engine dependency.** **P0.6 is the whole screen** — `causal_parents` are discarded and
nothing persists, so these surfaces are *unbuildable*, not merely unbuilt.

**Explicit exclusions.** Counterfactual branch UI — gated on P0.4A, because a counterfactual re-run
that does not consume identical substream draws presents resampling noise as causation, which is
precisely the class of unfounded claim this project exists to eliminate.

**Must not imply.** Causal reconstruction, event sourcing, state hashing or replay. Call it a
**prototype trace**. No replay claim before P0.6 evidence exists.

---

## 6. Fixture envelope — required on every record

```ts
{
  prototype_data: true,          // literal true; build asserts it
  scenario_id: string,
  scenario_version: string,      // semver; fixtures are versioned artefacts
  simulation_tick: number,
  player_role: string,           // single-role interim; no auth exists
  visibility_basis: string,      // why this role can see this
  epistemic_status: 'AUTHORITATIVE'|'ASSESSED'|'DISPUTED'|'UNKNOWN'|'PRESENTATION_ONLY',
  confidence: 'HIGH'|'MEDIUM'|'LOW'|'NOT_APPLICABLE',
  provenance: string,            // what produced this claim
  last_updated: string,          // tick or ISO time
  origin: 'fixture'              // 'engine' only when genuinely from the engine
}
```

`origin` is what makes a mixed fixture/live build honest at C1, when some values become real and
most do not. It must be per-record, never per-page.

---

## 7. Build order and honest effort

1. **Strategic Command Centre** — this block
2. **Entity Dossier** — next; highest value per unit effort once the shell exists
3. **Society Pulse** — after the dossier; reuses entity cards
4. **Causal Timeline** — needs the most original design work, least precedent
5. **Conversational Command Interface** — most likely to overreach; build last

The research's warning stands: a studio with thirty years of domain expertise could not rebuild its
interface on schedule. Five screens is a real budget, not a sprint.

---

## 8. Open founder decisions — none blocking this block

| # | Decision | Blocks |
|---|---|---|
| D1 | Primary surface: map / society / substrate switcher | Centre-region architecture beyond C0 |
| D3 | Does the auth layer move into Phase 0? | All role-filtered rendering; the dossier's premise |
| D5 | Target platform — browser-only, Tauri deferred? | Packaging |
| D8 | Dossier information architecture — how many tabs? | Dossier layout |
| D9 | Design thesis — retain 70/20/10, or adopt "conventional interaction, original information design, rationed ceremony"? | Visual direction |
| D12 | Operational military layer — confirm it stays out | Scope |
| — | **Likelihood axis** — revisit when the engine can produce a probability | Confidence model completeness |
| — | **Decay / cost / cooldown has no Phase 0 owner** | The entire alert model |

The last one is worth attention: it blocks an interface surface and belongs to nobody.
