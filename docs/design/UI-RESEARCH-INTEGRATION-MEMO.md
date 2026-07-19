# UI research — integration memo

**Status:** DRAFT, pending founder review · **Date:** 19 July 2026
**Purpose:** reconcile `UI-RESEARCH-HANDOFF.md` and `UI-VERTICAL-SLICE-RECOMMENDATION.md` against
current project authority, and record what is adopted for C0 and what is not.

> **The research is evidence, not authority.** Where it conflicts with the founder source record,
> the charter, Phase 0 governance, the world-model specifications, the determinism boundary or the
> B5 controls, the project authority wins and the conflict is recorded below rather than resolved
> silently.

**Nothing in the research is implemented.** This memo authorises nothing by itself.

---

## 1. Evidence quality — the ceiling on everything below

Recorded because it bounds how much weight any recommendation can carry.

| | |
|---|---|
| Research agents completed | 41 / 41 |
| Fact-check agents completed | **25 / 41** — 16 studies carry **no independent verification** |
| Claims checked | 137: **47 confirmed · 48 partly true · 41 unverifiable · 1 refuted** |
| Consolidated independent review | **failed** (stream-idle errors); author self-reviewed |

A **34% outright-confirmation rate is not a strong evidence base**. Author self-review is not
independent review. One **fabricated quotation** was caught by the verification stage, which is the
strongest argument for treating the 16 unverified studies with caution.

**Binding consequence, per founder instruction:** no numeric recommendation from this corpus may
become a CI gate, an acceptance threshold or an architectural requirement until independently
verified. Primary-source retrieval is **not** equivalent to independent confirmation. The pattern to
notice is that the game-UI findings were checked, while the standards and HCI findings — which carry
most of the concrete numbers — were **not**.

An independent review of the research documents remains outstanding.

---

## 2. Contradictions with current project authority

Surfaced, not silently resolved.

**X1 — Macro indicators from the live endpoint.** Research §8.1 says the macro panel "may use real
data" via `get_state`, which exists. This **conflicts with the founder's C0 instruction** that the
prototype render entirely from fixtures and carry
`NOT CONNECTED TO THE SIMULATION ENGINE`.
*Resolution: founder wins. C0 is fixtures only.* Connecting the real endpoint is C1, gated on P0.4.
Also note the research's own caveat: those indicators saturate monotonically, so displaying them
would render an open critical finding as if it were a working readout.

**X2 — Disclosure wording.** Research proposes `FICTIONAL WORLD` and
`FIXTURE DATA — NOT A SIMULATION RUN`. The founder specified different, longer strings.
*Resolution: founder wording is used verbatim.* It is also the safer choice — "NOT A SIMULATION RUN"
is ambiguous about whether a simulation exists at all.

**X3 — The confidence model.** Research finding F4 argues the eight labels conflate four axes and
lack a likelihood axis, and calls D2 "the single highest-value founder decision to take before
implementation". The founder has since decided D2 as a **two-axis model** (epistemic status ×
confidence). That decision **does not add a likelihood axis**.
*Resolution: the founder model is authority and is implemented.* The research's likelihood-axis
argument is recorded as **deferred**, not rejected — it becomes live when the engine can produce a
probability, which it cannot today. Until then there is nothing for a likelihood axis to report, so
adding one would invite fabricated numbers. This is consistent with the founder rule: no numeric
percentages unless produced by a documented mechanism.

**X4 — Dark-first and accessibility.** Research C3 states dark-only cannot be shipped and called
accessible; light and high-contrast themes are required, not optional.
*Resolution: C0 ships a dark theme and makes NO accessibility conformance claim.* Light and
high-contrast themes are recorded as required-before-any-conformance-claim. This is a limitation of
C0, stated plainly, not a dismissal of the finding.

**X5 — Decision queue and alerts.** Research R5/F8 shows an alert model cannot be built on the open
saturation critical: any edge-triggered threshold alert would fire every tick forever.
*Resolution: C0 renders a fixture decision queue as **display only**.* No alert engine, no
thresholds, no priorities-as-mechanism. The queue must not imply that anything computed it.

---

## 3. Recommendations — disposition

### 3.1 Accepted

| # | Recommendation | Why |
|---|---|---|
| A1 | **Intelligence-product framing** — never show ground truth; show what the role knows | F3: Football Manager is a 20-year-playtested commercial existence proof. Strongest positive finding in the corpus. |
| A2 | **Mark BOTH content classes; unmarked is a build failure** | F9/R6: labelling only AI text inflates the authority of everything unlabelled — including saturating indicators and authored seed values. Directly serves B5. |
| A3 | **Crop-invariant provenance carrier** (full-height gutter rule, not a tinted box) | R6: boxed tints read as advertising and are skipped; the founder additionally requires disclosure to survive cropping. |
| A4 | **Deterministic layout; never a randomly-seeded force layout** | F5: standard `d3-force` would appear to work and surface later as a failed replay-determinism test. Ties to dossier D-2 and P0.4A. |
| A5 | **Every aggregate exposes a ranked contributor list naming the mechanism** | R8/T18 — one of the few **fact-checked** findings. Directly serves the Eight Questions. |
| A6 | **Client never holds authoritative state; no optimistic updates** | T15: the interface expression of ADR-006. Optimistic UI is the default frontend reflex that would violate it. |
| A7 | **`Unknown` is a present row, never an omission** | Empirically supported; and unknown ≠ unavailable ≠ zero is already a founder D2 rule. |
| A8 | **Shape/text redundancy, never colour alone** | Proven operational doctrine (APP-6 style) and trade-dress-safe as an open standard. Also survives forced-colors mode. |
| A9 | **Adopt progressive disclosure as practice; do NOT cite the canonical source** | C6: Nielsen's article contains no study, sample or effect size. Citing it would reproduce the exact defect this project exists to correct. |

### 3.2 Accepted with modification

| # | Recommendation | Modification |
|---|---|---|
| B1 | Frontend stack: React 19 + TS + Vite + Radix | **Vite + TypeScript, no framework, for C0.** The founder's constraint is the smallest maintainable stack and explicitly forbids adding a large component framework for speed. The Strategic Command Centre is information display — panels, lists, chips — with no modal, combobox or tab widget where Radix earns its accessibility value. Revisit at the Dossier and Composer screens, which do have such widgets. Tokens and markup carry across if we adopt React later. Note the research's own admission that **"React is faster than Svelte" is UNVERIFIED** and must not appear in a framework ADR. |
| B2 | Centre view as a three-substrate switcher (D1) | **Single Situation view for C0.** D1 is undecided and the founder ruled that map engineering must not delay the first screenshot. The centre region is built as a slot so a switcher can be added without re-layout. |
| B3 | MapLibre GL + inline GeoJSON, no tile server | **Deferred.** C0 uses a simplified static situation panel. The MapLibre approach is recorded as the preferred route when a map is built — its no-tile-server property is what makes a fictional world safe — but it is a scheduled work item with its own budget, not part of this block. |
| B4 | Ten dossier sections as ten tabs (D8) | **Preserved as information architecture, not as a tab count.** C8: no product in the corpus supports a ten-tab default. |
| B5 | Two-axis epistemic model with a likelihood axis | Founder D2 adopted **without** the likelihood axis — see X3. |

### 3.3 Rejected for C0

| # | Recommendation | Why rejected *for this block* |
|---|---|---|
| C1 | Live macro indicators from `get_state` | Contradicts the founder's fixtures-only instruction (X1), and would surface a saturating indicator as a working readout. |
| C2 | Decision queue with a real priority model and alert classes | Unbuildable on the open saturation critical (X5). Rendered as fixture display only. |
| C3 | SSE / `EventSource` transport | No live data exists to stream. Adding transport now would imply a connected engine. |

Rejected for C0 ≠ rejected permanently. Each returns when its dependency lands.

### 3.4 Deferred to later blocks

Auth and role-based visibility (D3 — the dossier's entire premise has no subject today); the other
four screens; matrix view as a second graph representation; portrait stages 2–3 (stage 0
deterministic mark only, per D6); onboarding; time controls and branching; the operational military
layer (D12); map layer taxonomy; Tauri packaging (D5); visual-regression testing; light and
high-contrast themes; the 70/20/10 reframing (D9, undecided).

### 3.5 Requiring independent verification before use as any threshold

**None of these may become a CI gate, acceptance threshold or build budget until re-verified against
the primary source.** All are `PRIMARY-UNCHECKED` or worse in the research's own traceability table.

| Claim | Status |
|---|---|
| Node-link readability collapses at ~20 vertices | PRIMARY-UNCHECKED (graph-viz thread) |
| Alarm budget: ≤1 per 10 min; ~5/15/80 priority split (EEMUA 191) | PRIMARY-UNCHECKED — verify before it becomes a rate budget |
| Implied-truth-effect sample sizes | PRIMARY-UNCHECKED |
| APCA contrast floor | PRIMARY-UNCHECKED — and APCA is a non-normative draft; never claim it as WCAG conformance |
| "React is faster than Svelte" | **UNVERIFIED** — do not put in an ADR |
| Nielsen progressive-disclosure effect claim | **Unbacked in its own source** |
| Layout stability is empirically necessary | **Contested** — adopt stable layout for determinism reasons only |
| Exact in-game strings from Suzerain / Victoria 3 / Democracy 4 | Several downgraded to PARTLY_TRUE — do not quote without a screenshot |

---

## 4. The three research gaps that blocked the slice — all now resolved

The handoff §13 named three blockers. **All three are closed by founder decisions already taken**,
which is why C0 Block 2 proceeds without returning for a decision.

| Gap | Founder decision that resolves it |
|---|---|
| **G1** — tier-promotion presentation unspecified; "opening a dossier must not materialise anyone" forbids the obvious implementation | **G1 decision:** C0 uses only pre-materialised fixture entities; non-materialised entities appear as aggregate or minimal-reference records with an honest unavailable state; detailed promotion presentation deferred |
| **G2** — the confidence model is undecided and every screen renders it; building the chip before D2 means building it twice | **D2 decision:** two-axis epistemic status × confidence, with a fixed vocabulary |
| **G3** — no computed propagation exists to render | **G3 decision:** Society Pulse shows a hand-authored versioned fixture trace, explicitly labelled, never described as computed, simulated, live or emergent |

---

## 5. Implementation dependencies

| Dependency | Blocks |
|---|---|
| **P0.4** authoritative-state contract | C1 live state; what a projection is *of*; what the client may cache |
| **P0.4A** deterministic randomness | Stable generated portraits; any counterfactual branch UI; seeded layouts |
| **P0.5** cross-tier causality | Society Pulse as *computed* rather than illustrative |
| **P0.6** events, snapshots, replay | Causal Timeline; Activity tab; evidence behind assessments; queue dedup and resume |
| **P0.7** simulation time and horizon | Any forecast band or projection horizon |
| **Decay / cost / cooldown** (no P0 owner) | The alert model; any threshold indicator warning |
| **Auth layer** (audit records IAM as Phase 2) | Role-based visibility; the `Restricted` status as a real projection |

The last two have **no Phase 0 owner**. That is worth the founder's attention: the decay gap in
particular blocks a whole interface surface and is currently nobody's item.

---

## 6. Excluded by the five-screen scope filter

Preserved in the evidence files, excluded from implementation: map layer taxonomy, onboarding
architecture, time and branching UI, portrait generation pipelines, the operational military layer,
full accessibility conformance strategy, notification systems, save/load, multi-role, settings beyond
theme and reduced motion.

Not deleted — they will be needed. Nothing in them is authorised.

---

## 7. Standing warning carried from the research

> **C10 — the interface is not a layer on the product; it is the product.** Football Manager
> cancelled an entire annual release over interface quality, then shipped the rebuild and was
> rejected by its own user base. A studio with thirty years of domain expertise and a major
> publisher's resources could not rebuild its interface on schedule. **Scope accordingly.**

And the one that most directly governs this block:

> **A polished screenshot is documentation.** The entire remediation phase exists because
> documentation claimed properties the code did not have. A fixture-backed build must declare itself
> *in the interface*, such that a screenshot cannot be mistaken for a working simulation.
