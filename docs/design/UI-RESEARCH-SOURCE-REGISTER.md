# UI-RESEARCH-SOURCE-REGISTER — sources, verification status and reliability assessment

> # ⚠ DRAFTED — NOT FOUNDER-APPROVED — NOT IMPLEMENTED
>
> This register records the evidence base behind
> [`UI-RESEARCH-HANDOFF.md`](UI-RESEARCH-HANDOFF.md) and
> [`UI-VERTICAL-SLICE-RECOMMENDATION.md`](UI-VERTICAL-SLICE-RECOMMENDATION.md). It exists so that no
> recommendation in either document can be cited without its evidence status being visible.
>
> Drafted by an AI agent. Nothing here is founder-approved.

**Dated:** 19 July 2026 · **Unique sources:** 724 · **Full structured corpus:**
`docs/design/research-evidence/CORPUS.json`

---

## 1. How to read this register

### 1.1 Labels

| Label | Meaning | How it was reached |
|---|---|---|
| **VERIFIED** | An independent adversarial fact-checker searched for disconfirming evidence and returned CONFIRMED. | 47 claims |
| **PARTLY SUPPORTED** | The underlying pattern holds, but the study's statement of it was over-precise, mis-attributed, or partly unsupported. A correction exists. | 48 claims |
| **UNVERIFIED** | The fact-checker could not obtain evidence either way, *or* the study received no fact-check at all because the research pass was stopped early. | 41 checked-but-unresolvable claims, plus **all claims in 16 unchecked studies** |
| **DISPUTED** | The underlying research literature itself is unsettled, and the study said so. | See §4 |
| **INFERENCE** | An agent's own reasoning extrapolating to MERIDIAN, explicitly labelled as such by the agent. | See §5 |
| **REFUTED** | Disconfirmed. Must not be cited. | 1 claim — see §3 |

### 1.2 The one rule this register enforces

> **A recommendation may not carry more confidence than its weakest load-bearing source.**

Where the handoff makes a strong recommendation on a PARTLY SUPPORTED or UNVERIFIED basis, it says so
inline. Where it does not, that is a defect in the handoff and should be reported against it.

---

## 2. Corpus reliability — stated plainly

**This is a moderately reliable corpus with well-sourced standards work and thinly-sourced game-UI
work. It is adequate for design direction and inadequate for factual assertions about specific
products.**

| Measure | Value |
|---|---|
| Research studies completed | 41 of 41 (27 products, 14 threads) |
| Studies independently fact-checked | **25 of 41** |
| Studies with **no** verification | **16** |
| Claims checked | 137 |
| CONFIRMED | 47 (34%) |
| PARTLY_TRUE | 48 (35%) |
| UNVERIFIABLE | 41 (30%) |
| REFUTED | 1 (<1%) |

### 2.1 Four structural weaknesses

**W1 — The verification stage was cut mid-flight.** The research pass was stopped by founder
cost-control decision while fact-checkers were still running. Sixteen studies are single-sourced to
one agent with no adversarial check. **Their claims should be treated as UNVERIFIED regardless of how
confidently they are written.**

**W2 — Several threads ran with an exhausted web-search budget.** Nine of the fourteen cross-cutting
threads report that their search allocation was consumed before they issued a query, forcing them to
work from direct URL fetches of sources they already knew. Affected: uncertainty visualisation,
causal explanation, alerts and attention, situation awareness, map and layers, onboarding, time and
branching, visual language, frontend technical feasibility.

*Consequence:* their **standards and primary-source claims are generally strong** (W3C, HSE, WCAG,
MapLibre, MDN and similar were fetched and read directly, several in full). Their **player-experience,
practitioner-commentary and market-context claims are thin**, and most say so explicitly in their own
method notes. Several named specific sources they wanted and could not obtain — ICD 203 (403 from both
dni.gov and mirrors), Budescu et al. on cross-national probability-word interpretation (paywalled),
Sherman Kent's original essay (403), the Joint Commission alert advisory (403), the USENIX SOC-analyst
study (403), FAA alerting guidance (403), and Bainbridge's *Ironies of Automation* (downloaded but
unparseable). **Claims that would have rested on those are flagged in their own reports and must not be
upgraded.**

**W3 — Source mix is uneven.** 79 Wikipedia URLs and 56 Steam-community URLs against 27 arXiv and 18
W3C. Wikipedia and Steam are acceptable as evidence of *player experience* and as secondary summaries,
and were mostly used that way — but the game-UI strand is materially less well-sourced than the
standards strand, and at least one study was told to remove Wikipedia as support for a factual claim
about a game's mechanics.

**W4 — Over-precision is the dominant error mode.** Most PARTLY_TRUE verdicts are not fabrications;
they are a real feature described with an invented exact string, a pattern generalised past its
evidence, or a reasonable inference presented as an observed fact. Corrections in §3.

---

## 3. Corrections — claims that must not be repeated as stated

### 3.1 REFUTED — do not cite

| Claim | Finding |
|---|---|
| A verbatim sentence attributed to a named developer's blog explaining why an approval-distribution visualisation was *relocated*. | **The sentence does not appear in the post.** The fact-checker retrieved the full body of both the original and follow-up posts. The framing is also wrong: nothing was relocated — a **new optional view, disabled by default**, was added, and the stated motivation was partly that the data had only ever been an instant snapshot rather than a time series. **Treat the quotation as fabricated or mis-transcribed until someone produces its source.** |

This is the single most important entry in the register. It is direct evidence that an unverified
study can produce a confident, plausible, fabricated quotation — and therefore direct evidence for
treating the 16 unchecked studies with caution.

### 3.2 PARTLY SUPPORTED — corrected versions

| Original claim | Corrected version |
|---|---|
| Democracy 4 encodes influence strength as arrow animation speed and *sign as arrow colour*. | Hover-reveal of a node's local neighbourhood and speed-encoded strength are confirmed. That arrow **colour** encodes the sign of that specific influence — rather than the valence of the connected factor — is **not** confirmed. |
| Approval distribution shown as *green* blobs. | Blobs are **party-coloured**, sized by voter count, plotted over time with party-threshold lines; the whole layer is optional and off by default. |
| Paradox tooltip content "cannot be picked up by a screen reader at all". | The **inputs** are script/localisation data; the **composed runtime tooltip** is exposed only as pixels, with no accessibility tree or export API — evidenced by player forum posts, **not** by vendor documentation. |
| Suzerain: "Alignment, Unrest and Opinion are hidden with no numeric display anywhere." | Opinion appears tracked qualitatively with no in-run popularity gauge evidenced — but "no numeric display anywhere" is **contradicted by the endgame results screen**, and Wikipedia must be dropped as a source for this. |
| Suzerain: constitutional reform requires a specific two-thirds assembly plus simple court majority. | Amendment-package composition and named leaders attaching stated conditions are confirmed. **The specific numeric thresholds are not** and must be dropped or re-sourced. |
| Dwarf Fortress: "Kitfox did absolutely no design or UX work"; the redesign was a two-person retrofit with zero UX input. | Kitfox-as-publisher contributed no design/UX. The work was done by the Adams brothers **with named collaborators and a UX professional consulted late in development**. "Zero UX input" overstates it. |
| Victoria 3 "adopted the same tooltip system wholesale from CK3". | Soften to an **observed similarity**; the wholesale-adoption claim is unsupported. |
| In-game cost strings quoted verbatim (e.g. a specific bracketed budget cost). | Wiki transcriptions show the **pattern** of bracketed inline costs. The specific exemplar strings should not be presented as verbatim in-game text without a current screenshot. |

**Standing rule derived from these:** *do not quote in-game text, exact thresholds, or developer
statements without a directly retrievable source.* Describe the pattern instead.

---

## 4. DISPUTED — the research literature itself is unsettled

These are not weaknesses in the corpus; they are genuine scientific disagreements, and MERIDIAN must
not silently pick a side.

| Topic | The dispute | Implication |
|---|---|---|
| **Layout stability / "mental map preservation"** | A survey of pre-2012 results found no evidence it helps; two later studies found conditional benefit, specifically for map-like tasks involving five or more pertinent nodes. | Adopt stable layout **for determinism reasons** (D-2). Do not document it as empirically necessary. |
| **Hypothetical outcome plots** | Markedly better for relational/probability judgements; markedly **worse** for mean estimation under high variance. The two strongest papers point in different directions. | Task-conditional tool, never a house style. |
| **Dark mode** | Controlled evidence tends to favour light mode for normal or corrected vision; dark benefits a specific low-vision population. | Dark is defensible on ambience; **dark-only cannot be called accessible**. |
| **The WCAG 2.x contrast formula near black** | Credibly disputed as overstating contrast for dark surfaces — but the critique's main source is partisan and the proposed replacement is not a standard. | Dual-gate. Never claim APCA as WCAG conformance. |
| **Minimalism vs embellishment ("chartjunk")** | Genuinely unsettled; no practitioner consensus on the definition. | Do not adopt data-ink maximisation as a constitution-level rule and then cite it to strip affordances. |
| **Interruption content-relevance** | Whether the *content* of an interruption affects its disruption cost is contested; one study found any discontinuity carries the cost regardless. | Relevance-matching will not buy back interruption cost. Reduce **count**. |
| **Typed confirmation ("type the name to proceed")** | Contested as good design. | Defensible only where reversal is genuinely impossible and the typed token disambiguates. |
| **Situation-awareness theory** | Charged with circularity and unfalsifiability; the SA-to-performance link is probabilistic. | Use SA as design vocabulary and evaluation scaffold. Never claim an SA-grounded design "ensures" good decisions. |
| **Cytoscape.js performance flags** | Its own documentation describes its published performance flags as "largely moot" and states no WebGL renderer. | Do not select it on performance grounds. |
| **Nielsen's progressive-disclosure benefit claim** | The canonical article contains **no study, sample or effect size**. | Adopt the practice; never cite the claim. Citing it would reproduce this project's named defect. |

---

## 5. INFERENCE — agent reasoning, not research findings

Explicitly labelled as inference by the agents that produced them, and carried forward as *proposals*:

- The mapping of Rasmussen's abstraction hierarchy onto a **society** (functional purpose → conservation
  laws → institutions → …). Its own author flags that ecological interface design was built for
  law-governed physical domains, and that a socio-political domain's means-ends links are intentional
  and defeasible, so the display guarantees do not transfer.
- The claim that MERIDIAN's two open critical findings are both abstraction-hierarchy failures.
- Scoring a SAGAT harness against the player-intelligence projection rather than authoritative reality
  — sound reasoning, unverified against the measurement literature.
- The proposed glyph assignments for the eight confidence labels.
- The proposed binding of each of the Eight Questions to a specific shell region.
- The F6 region-cycling keybinding (flagged by its agent as desktop convention, not a standard).
- The fixture-labelling mechanism proposed in the handoff §8.1.
- The reframing of the 70/20/10 thesis in handoff §5.

---

## 6. UNVERIFIED — must be re-checked before it reaches an ADR

| Claim | Why it matters | Action |
|---|---|---|
| React vs Svelte runtime performance ranking | Feeds the framework ADR | **Only the benchmark methodology was confirmed, not any ranking.** Re-run the check. Do not claim React is faster. |
| MapLibre gzipped bundle size | Feeds performance budgets | Re-measure. |
| ICD 203's exact probability table | Underpins the confidence-model recommendation (D2) | Retrieved only via secondary sources; the primary returned 403. Obtain before finalising D2. |
| Sherman Kent's original wording | Same | Available only via a secondary summary. |
| The FUI / film-interface critique | Underpins the "not sci-fi pastiche" position | **Weakest strand in the corpus.** The usual primary source domain no longer resolves. No quotation was verified; none was invented. |
| All Palantir capability descriptions | Informs the entity-centric and lineage recommendations | Treat vendor marketing as marketing. The corpus itself records claims withdrawn under scrutiny. |
| Every claim in the 16 unchecked studies | Various | See §7 for which studies these are. |

---

## 7. Verification coverage by study

**Fact-checked (25).** Democracy 4 · Paradox tooltip system · Crusader Kings III · Terra Invicta ·
Suzerain · Victoria 3 · Dwarf Fortress · Shadows of Doubt · Command: Modern Operations ·
Power & Revolution · Football Manager · Shadow Empire · Old World · Frostpunk · deduction games ·
RimWorld · Hearts of Iron IV · Disco Elysium · Cities: Skylines · link-analysis tooling ·
Palantir · C2/TAK · Bloomberg · intelligence tradecraft standards · security-operations consoles.

**Not fact-checked (16) — treat as UNVERIFIED.** Control-room and alarm-management canon ·
C2PA and AI-labelling · and the fourteen cross-cutting threads (uncertainty visualisation ·
provenance UI · progressive disclosure · causal explanation · alerts and attention · graph
visualisation · situation awareness · natural-language command · map and layers · onboarding ·
time and branching · accessibility · visual language · frontend feasibility).

**Note the asymmetry, and its direction.** The unchecked set contains most of the *standards-based*
work — which is the better-sourced material, since standards documents were fetched and read
directly. The checked set contains most of the *game-UI* work — which is where the errors were
actually found. This is fortunate but not a reason for complacency: the threads' MERIDIAN-specific
recommendations are agent reasoning layered on top of standards, and that reasoning has had no
adversarial review at all.

---

## 8. Deduplicated source list

724 unique URLs, sorted by domain. "Used by" names the study or studies that cited the source.

**Caveats that apply to the whole table.** Titles are as recorded by the citing agent and are not
independently normalised. Some entries are explicitly annotated by their agent as *cited but not
fetched* (typically HTTP 403) — those are not evidence, and are retained only so the attempt is
visible rather than silently dropped. Presence in this table indicates a source was **cited**, not
that its claim was verified; verification status is per-claim and lives in §3–§7 and in
`docs/design/research-evidence/FACT-CHECK-NON-CONFIRMED.json`.

<!-- BEGIN GENERATED SOURCE TABLE -->
<!-- Generated from CORPUS.json; do not hand-edit. -->

| # | Source | Domain | Used by |
|---|---|---|---|
| 1 | [9puz guide: Solve Cases Without Getting Lost — CITED BUT NOT FETCHED (HTTP 403); source of the ](https://9puz.com/2569-shadows-of-doubt-guide) | 9puz.com | Shadows of Doubt |
| 2 | [Meta — Labeling AI-Generated Images on Facebook, Instagram and Threads](https://about.fb.com/news/2024/02/labeling-ai-generated-images-on-facebook-instagram-and-threads) | about.fb.com | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 3 | [St. John & Smallman, 'Supporting Situation Awareness Under Data Overload in Command and Control](https://www.academia.edu/47508646/Supporting_Situation_Awareness_Under_Data_Overload_in_Command_and_Control_Visualizations) | academia.edu | Military & emergency command-and-control interfaces: ATAK/Wi |
| 4 | [Labeling AI-generated media online (PNAS Nexus pgaf170; n=3,223 and n=4,356)](https://academic.oup.com/pnasnexus/article/4/6/pgaf170/8151894) | academic.oup.com | Provenance and fact-versus-narration separation in an interf |
| 5 | [The Case of the Golden Idol review — Adventure Game Hotspot (thinking panel, word collection, p](https://adventuregamehotspot.com/review/119/the-case-of-the-golden-idol) | adventuregamehotspot.com | Evidence, deduction and document-verification interfaces |
| 6 | [AG Grid — licence and pricing](https://www.ag-grid.com/license-pricing) | ag-grid.com | Frontend technical feasibility for MERIDIAN: framework, pack |
| 7 | [Understanding AI transparency (AlgoSoc) — label design under the EU AI Act](https://algosoc.org/results/understanding-ai-transparency) | algosoc.org | Provenance and fact-versus-narration separation in an interf |
| 8 | [Aza Raskin, 'Never Use a Warning When You Mean Undo' (A List Apart)](https://alistapart.com/article/neveruseawarning) | alistapart.com | Natural-language command and action-confirmation interfaces  |
| 9 | [Ancient World Magazine — 'Old World (2021): A deeply flawed historical strategy game' (the prin](https://www.ancientworldmagazine.com/reviews/old-world-2021) | ancientworldmagazine.com | Old World |
| 10 | [Compare Bloomberg, Capital IQ, and Refinitiv/LSEG — University of Florida Business Library](https://answers.businesslibrary.uflib.ufl.edu/genai/faq/401428) | answers.businesslibrary.uflib.ufl.edu | Bloomberg Terminal |
| 11 | [Anthropic Engineering, 'Building effective agents'](https://www.anthropic.com/engineering/building-effective-agents) | anthropic.com | Natural-language command and action-confirmation interfaces  |
| 12 | ['Improving Situation Awareness with the Android Team Awareness Kit (ATAK)', AFRL (Kohler, Sterl](https://apps.dtic.mil/sti/tr/pdf/ADA617401.pdf) | apps.dtic.mil | Military & emergency command-and-control interfaces: ATAK/Wi |
| 13 | [Command: Modern Air-Naval Operations – PC Game Review (Armchair General; review plus reader com](http://armchairgeneral.com/command-modern-air-naval-operations-pc-game-review.htm) | armchairgeneral.com | Command: Modern Operations |
| 14 | [Suzerain — Articy showcase: how Torpor built the branching narrative and variable system (devel](https://www.articy.com/en/showcase/suzerain) | articy.com | Suzerain |
| 15 | [EU AI Act, Article 14 — Human Oversight](https://artificialintelligenceact.eu/article/14) | artificialintelligenceact.eu | Natural-language command and action-confirmation interfaces  |
| 16 | [EU AI Act Article 50 — Transparency Obligations](https://artificialintelligenceact.eu/article/50) | artificialintelligenceact.eu | C2PA / Content Credentials, plus the AI-labelling and over-r; Provenance and fact-versus-narration separation  |
| 17 | [NodeTrix — arXiv preprint](https://arxiv.org/abs/0705.0599) | arxiv.org | Relationship graph visualisation at scale — node-link vs mat |
| 18 | [Miller, T. — Explanation in Artificial Intelligence: Insights from the Social Sciences (arXiv:1](https://arxiv.org/abs/1706.07269) | arxiv.org | Causal explanation interfaces for MERIDIAN — "why did this c |
| 19 | [Wachter, Mittelstadt & Russell — Counterfactual Explanations without Opening the Black Box (arX](https://arxiv.org/abs/1711.00399) | arxiv.org | Causal explanation interfaces for MERIDIAN — "why did this c; Time, pause, replay, branching and counterfactua |
| 20 | [Poursabzi-Sangdeh et al. — Manipulating and Measuring Model Interpretability (arXiv:1802.07810)](https://arxiv.org/abs/1802.07810) | arxiv.org | Causal explanation interfaces for MERIDIAN — "why did this c |
| 21 | [Zhang, Liao, Bellamy — Effect of Confidence and Explanation on Accuracy and Trust Calibration](https://arxiv.org/abs/2001.02114) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 22 | [Liao, Gruen & Miller — Questioning the AI: Informing Design Practices for Explainable AI User E](https://arxiv.org/abs/2001.02478) | arxiv.org | Causal explanation interfaces for MERIDIAN — "why did this c |
| 23 | [Bansal et al. — Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary](https://arxiv.org/abs/2006.14779) | arxiv.org | Causal explanation interfaces for MERIDIAN — "why did this c |
| 24 | [Bucinca, Malaya, Gajos — To Trust or to Think: Cognitive Forcing Functions Can Reduce Overrelia](https://arxiv.org/abs/2102.09692) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 25 | [Vasconcelos et al. — Explanations Can Reduce Overreliance on AI Systems During Decision-Making](https://arxiv.org/abs/2212.06823) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 26 | [Gelman, Taoufiq, Vörös, Berlin — 'That Escalated Quickly: An ML Framework for Alert Prioritizat](https://arxiv.org/abs/2302.06648) | arxiv.org | Security operations, observability and incident-response con |
| 27 | [Greshake et al., 'Not what you've signed up for: Compromising Real-World LLM-Integrated Applica](https://arxiv.org/abs/2302.12173) | arxiv.org | Natural-language command and action-confirmation interfaces  |
| 28 | [Liu, Zhang, Liang — Evaluating Verifiability in Generative Search Engines](https://arxiv.org/abs/2304.09848) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 29 | [Reingold, Shen, Talati — Dissenting Explanations: Leveraging Disagreement to Reduce Model Overr](https://arxiv.org/abs/2307.07636) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 30 | [Subramonyam et al., 'Bridging the Gulf of Envisioning: Cognitive Design Challenges in LLM Inter](https://arxiv.org/abs/2309.14459) | arxiv.org | Natural-language command and action-confirmation interfaces  |
| 31 | [Si et al. — Large Language Models Help Humans Verify Truthfulness, Except When They Are Convinc](https://arxiv.org/abs/2310.12558) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 32 | [Kim et al. — 'I'm Not Sure, But...': Examining the Impact of LLM Uncertainty Expression](https://arxiv.org/abs/2405.00623) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 33 | [Debenedetti et al., 'AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and ](https://arxiv.org/abs/2406.13352) | arxiv.org | Natural-language command and action-confirmation interfaces  |
| 34 | [Gamage et al. — Labeling Synthetic Content: User Perceptions of Warning Label Designs (metadata](https://arxiv.org/abs/2503.05711) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 35 | [Debenedetti et al., 'Defeating Prompt Injections by Design' (CaMeL)](https://arxiv.org/abs/2503.18813) | arxiv.org | Natural-language command and action-confirmation interfaces  |
| 36 | [Holtervennhoff et al. — A User Study on AI Labels as a Safeguard Against Image-Based Misinforma](https://arxiv.org/abs/2505.22845) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 37 | [Ibrahim et al. — Measuring and Mitigating Overreliance to Build Human-Compatible AI (abstract o](https://arxiv.org/abs/2509.08010) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 38 | [Chen et al. — Label Detail and Content Stakes in User Perceptions of AI-Generated Images](https://arxiv.org/abs/2510.19024) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 39 | [Ghosh, Sarkar, Lindley, Poelitz — Cognitive Forcing Functions for Execution Plans in AI-Assiste](https://arxiv.org/abs/2601.18033) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 40 | [Martin-Boyle et al. — PaperTrail: A Claim-Evidence Interface](https://arxiv.org/abs/2602.21045) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 41 | [Moller et al. — Overreliance on AI in Information-seeking from Video Content (metadata only, no](https://arxiv.org/abs/2603.19843) | arxiv.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 42 | [Ndichu, Ban, Ozawa, Takahashi, Inoue — 'AI-Driven Security Alert Screening and Alert Fatigue Mi](https://arxiv.org/abs/2605.08316) | arxiv.org | Security operations, observability and incident-response con |
| 43 | [Labeling Synthetic Content: User Perceptions of Warning Label Designs for AI-Generated Content ](https://arxiv.org/html/2503.05711v1) | arxiv.org | Provenance and fact-versus-narration separation in an interf |
| 44 | [CAP Code Section 2 — Recognition of marketing communications (ASA)](https://www.asa.org.uk/type/non_broadcast/code_section/02.html) | asa.org.uk | Provenance and fact-versus-narration separation in an interf |
| 45 | [Suzerain: Personal Politics, the Global Community, and Empathy in Games — A.V. Club interview w](https://www.avclub.com/suzerain-interview) | avclub.com | Suzerain |
| 46 | [Command: Modern Operations Review – Commanding from a Dark Room (The Avid Wargamer, Max Chee; c](https://avidwargamer.com/command-modern-operations-review-commanding-from-a-dark-room-max-chee) | avidwargamer.com | Command: Modern Operations |
| 47 | [Holten, Isenberg, Fekete & van Wijk — Performance Evaluation of Tapered, Curved, and Animated D](https://aviz.fr/wiki/uploads/Research/Holten_2010_DirectedEdges.pdf) | aviz.fr | Relationship graph visualisation at scale — node-link vs mat |
| 48 | [Awkward Mixture — Disco Elysium: Skill Checks, Conversations, and Thoughts (critique: outfit-sw](https://awkwardmixture.blogspot.com/2020/03/disco-elysium-skill-checks.html) | awkwardmixture.blogspot.com | Disco Elysium |
| 49 | [Axis Maps — Cartography Guide (topic index)](https://www.axismaps.com/guide) | axismaps.com | Map and layer design for multi-domain data — cartographic ba |
| 50 | [Axis Maps — Cartography Guide: Choropleth Maps](https://www.axismaps.com/guide/choropleth) | axismaps.com | Map and layer design for multi-domain data — cartographic ba |
| 51 | [Axis Maps — Cartography Guide: Dot Density Maps](https://www.axismaps.com/guide/dot-density) | axismaps.com | Map and layer design for multi-domain data — cartographic ba |
| 52 | [Axis Maps — Cartography Guide: Labeling](https://www.axismaps.com/guide/labeling) | axismaps.com | Map and layer design for multi-domain data — cartographic ba |
| 53 | [Axis Maps — Cartography Guide: Proportional Symbol Maps](https://www.axismaps.com/guide/proportional-symbols) | axismaps.com | Map and layer design for multi-domain data — cartographic ba |
| 54 | [Axis Maps — Cartography Guide: Should a Map Be Interactive?](https://www.axismaps.com/guide/should-a-map-be-interactive) | axismaps.com | Map and layer design for multi-domain data — cartographic ba |
| 55 | [Axis Maps — Cartography Guide: Visual Hierarchy](https://www.axismaps.com/guide/visual-hierarchy) | axismaps.com | Map and layer design for multi-domain data — cartographic ba |
| 56 | [Blockint, 'Critical review of the Admiralty Code' — Baker et al. (1968) diagonal finding, Irwin](https://www.blockint.nl/intel-analysis/critical-review-of-the-admiralty-code) | blockint.nl | Intelligence-analysis tradecraft standards for expressing un |
| 57 | [Palantir blog — On dataset versioning in Palantir Foundry (immutability, branching)](https://blog.palantir.com/on-dataset-versioning-in-palantir-foundry-8f23de22cc4c) | blog.palantir.com | Palantir Gotham and Foundry |
| 58 | [Boiling Steam review (fetched in full — auto-connection on body, unknown-name behaviour, name a](https://boilingsteam.com/shadows-of-doubt) | boilingsteam.com | Shadows of Doubt |
| 59 | [Friedman & Zeckhauser, 'Assessing Uncertainty in Intelligence' (Intelligence and National Secur](https://bpb-us-e1.wpmucdn.com/sites.dartmouth.edu/dist/0/433/files/2014/07/Friedman-and-Zeckhauser-Assessing-Uncertainty-in-Intelligence.pdf) | bpb-us-e1.wpmucdn.com | Intelligence-analysis tradecraft standards for expressing un |
| 60 | [Brendan Gregg — Flame Graphs](https://www.brendangregg.com/flamegraphs.html) | brendangregg.com | Causal explanation interfaces for MERIDIAN — "why did this c |
| 61 | [Cambridge / Judgment and Decision Making: 'The effect of source reliability and information cre](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/effect-of-source-reliability-and-information-credibility-on-judgments-of-information-quality-in-intelligence-analysis/E67548E8010A47345C3439D45D9EC6B3) | cambridge.org | Intelligence-analysis tradecraft standards for expressing un |
| 62 | [Bloomberg Terminal reviews — Capterra (USER EXPERIENCE evidence; 4.4/5, 15 verified reviews; 'n](https://www.capterra.com/p/230048/Bloomberg-Terminal/reviews) | capterra.com | Bloomberg Terminal |
| 63 | [AI label component usage (IBM Carbon Design System)](https://carbondesignsystem.com/components/ai-label/usage) | carbondesignsystem.com | Provenance and fact-versus-narration separation in an interf |
| 64 | [Archambault & Purchase — On the Application of Experimental Results in Dynamic Graph Drawing (G](https://ceur-ws.org/Vol-1244/GViP-paper5.pdf) | ceur-ws.org | Relationship graph visualisation at scale — node-link vs mat |
| 65 | [Suzerain PC review — Chalgyr's Game Room (portrait behaviour, codex/journal tabs, textbox size,](https://www.chalgyr.com/2020/12/review-pc-suzerain.html) | chalgyr.com | Suzerain |
| 66 | [CIA Center for the Study of Intelligence: 'Words of Estimative Probability', Studies in Intelli](https://www.cia.gov/resources/csi/studies-in-intelligence/archives/vol-8-no-4/words-of-estimative-probability) | cia.gov | Intelligence-analysis tradecraft standards for expressing un |
| 67 | [Character — CK3 Wiki](https://ck3.paradoxwikis.com/Character) | ck3.paradoxwikis.com | Crusader Kings III |
| 68 | [Crusader Kings III Community Wiki — main page (beginner's guide, tutorial videos, FAQ)](https://ck3.paradoxwikis.com/Crusader_Kings_III_Wiki) | ck3.paradoxwikis.com | Onboarding and learnability for very deep simulations — evid |
| 69 | [Events — CK3 Wiki](https://ck3.paradoxwikis.com/Events) | ck3.paradoxwikis.com | Crusader Kings III |
| 70 | [Map mode — CK3 Wiki](https://ck3.paradoxwikis.com/Map_mode) | ck3.paradoxwikis.com | Crusader Kings III |
| 71 | [Modifiers — CK3 Wiki](https://ck3.paradoxwikis.com/Modifiers) | ck3.paradoxwikis.com | Crusader Kings III |
| 72 | [Opinion — CK3 Wiki](https://ck3.paradoxwikis.com/Opinion) | ck3.paradoxwikis.com | Causal explanation interfaces for MERIDIAN — "why did this c; Crusader Kings III |
| 73 | [Relations — CK3 Wiki](https://ck3.paradoxwikis.com/Relations) | ck3.paradoxwikis.com | Crusader Kings III |
| 74 | [Schemes — CK3 Wiki](https://ck3.paradoxwikis.com/Schemes) | ck3.paradoxwikis.com | Crusader Kings III |
| 75 | [Bainbridge, 'Ironies of Automation', Automatica 1983 — PDF fetched (615KB) but NOT PARSED (popp](https://ckrybus.com/static/papers/Bainbridge_1983_Automatica.pdf) | ckrybus.com | Situation awareness and the command shell: SA theory, ecolog |
| 76 | [Song & Szafir, Where's My Data? Evaluating Visualizations with Missing Data, IEEE VIS 2018 / TV](http://cmci.colorado.edu/visualab/papers/song_VIS_2018.pdf) | cmci.colorado.edu | Uncertainty visualisation research and its practical encodin |
| 77 | [Claude Code documentation — Common workflows (plan before editing)](https://code.claude.com/docs/en/common-workflows) | code.claude.com | Natural-language command and action-confirmation interfaces  |
| 78 | [Claude Code documentation — Choose a permission mode (plan mode, auto mode, protected paths)](https://code.claude.com/docs/en/permission-modes) | code.claude.com | Natural-language command and action-confirmation interfaces  |
| 79 | [Claude Code documentation — Security (permission architecture, prompt-injection safeguards, iso](https://code.claude.com/docs/en/security) | code.claude.com | Natural-language command and action-confirmation interfaces  |
| 80 | [Suzerain Universe Codex (official, Torpor Games)](https://codex.torporgames.com) | codex.torporgames.com | Suzerain |
| 81 | [Cabinet — Suzerain Universe Codex (official)](https://codex.torporgames.com/cabinet) | codex.torporgames.com | Suzerain |
| 82 | [Wildland Fire Pilot Project for Development of the Team Awareness Kit & Deployment on the Grizz](https://cofiretech.org/wp-content/uploads/tak-wildland-fire-pilot-project-report.pdf) | cofiretech.org | Military & emergency command-and-control interfaces: ATAK/Wi |
| 83 | [ColePowered Shadows of Doubt devblog archive (fetched — index of DevBlogs 36-45)](https://colepowered.com/category/shadows-of-doubt) | colepowered.com | Shadows of Doubt |
| 84 | [ColePowered DevBlog 10: Gameplay Loop (fetched in full — primary developer source)](https://colepowered.com/shadows-of-doubt-devblog-10-gameplay-loop) | colepowered.com | Shadows of Doubt |
| 85 | [ColePowered DevBlog 4: Case Folders & Cork Boards (fetched in full — primary developer source)](https://colepowered.com/shadows-of-doubt-devblog-4-case-folders-cork-boards) | colepowered.com | Shadows of Doubt |
| 86 | [ColePowered DevBlog 7: There's Been a (Procedurally Generated) Murder (fetched — crime-scene pl](https://colepowered.com/shadows-of-doubt-devblog-7-theres-been-a-procedurally-generated-murder) | colepowered.com | Shadows of Doubt |
| 87 | [ColePowered DevBlog 8: Simulating a City (fetched in full — citizen memory/decay/lying)](https://colepowered.com/shadows-of-doubt-devblog-8-simulating-a-city) | colepowered.com | Shadows of Doubt |
| 88 | [ColePowered DevBlog 30: Top Development Challenges Part I (fetched — save/object persistence, n](https://colepowered.itch.io/shadows/devlog/354045/shadows-of-doubt-devblog-30-the-top-shadows-of-doubt-development-challenges-part-i) | colepowered.itch.io | Shadows of Doubt |
| 89 | [Colour Blind Awareness — Colour Blindness (prevalence)](https://www.colourblindawareness.org/colour-blindness) | colourblindawareness.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 90 | [Colour Blind Awareness — Types of Colour Blindness (breakdown by type)](https://www.colourblindawareness.org/colour-blindness/types-of-colour-blindness) | colourblindawareness.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 91 | [New in v1.07: Mission Editor 2.0 (official developer blog)](https://command.matrixgames.com/?p=3653) | command.matrixgames.com | Command: Modern Operations |
| 92 | [Command: Modern Operations – User interface and experience, Part I (official developer blog)](https://command.matrixgames.com/?p=4954) | command.matrixgames.com | Command: Modern Operations |
| 93 | [Command: Modern Operations – User interface and experience, Part II (official developer blog)](https://command.matrixgames.com/?p=4975) | command.matrixgames.com | Command: Modern Operations |
| 94 | [Command: Modern Operations — official Manual Addendum: User Interface](https://command.matrixgames.com/?page_id=2697) | command.matrixgames.com | Command: Modern Operations |
| 95 | [Command: Modern Operations — official Manual Addendum: AI & Mechanics](https://command.matrixgames.com/?page_id=2711) | command.matrixgames.com | Command: Modern Operations |
| 96 | [Inbox and News — SI official FM2024 manual (SEARCH SNIPPET ONLY — 403; Must Respond, red accent](https://community.sports-interactive.com/sigames-manual/football-manager-2024/inbox-and-news-r4956) | community.sports-interactive.com | Football Manager |
| 97 | [Players — SI official FM2024 manual (SEARCH SNIPPET ONLY — 403; profile anatomy, Squad screen)](https://community.sports-interactive.com/sigames-manual/football-manager-2024/players-r4958) | community.sports-interactive.com | Football Manager |
| 98 | [Transfers, Recruitment, and Scouting — SI official FM2024 manual (SEARCH SNIPPET ONLY — 403; Sc](https://community.sports-interactive.com/sigames-manual/football-manager-2024/transfers-recruitment-and-scouting-r4962) | community.sports-interactive.com | Football Manager |
| 99 | [The Reign of Play: 'Suzerain' and Practicing Politics — Cosmonaut Magazine (critical essay)](https://cosmonautmag.com/2024/10/the-reign-of-play-suzerain-and-practicing-politics) | cosmonautmag.com | Suzerain |
| 100 | [Shneiderman, B. — The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf) | cs.umd.edu | Progressive disclosure and information density in expert int; Relationship graph visualisation at scale — node |
| 101 | [Shneiderman, B. — Promoting Universal Usability with Multi-Layer Interface Design (ACM CUU'03, ](https://www.cs.umd.edu/~ben/papers/Shneiderman2003Promoting.pdf) | cs.umd.edu | Progressive disclosure and information density in expert int |
| 102 | [Cities: Skylines II Wiki — main page / navigation index](https://cs2.paradoxwikis.com) | cs2.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 103 | [Cities: Skylines II Wiki — Beginner's guide (green-road coverage on service placement)](https://cs2.paradoxwikis.com/Beginner%27s_guide) | cs2.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 104 | [Cities: Skylines II Wiki — Citizens (life stages, happiness factors, condition badges, educatio](https://cs2.paradoxwikis.com/Citizens) | cs2.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 105 | [Cities: Skylines II Wiki — Developer diaries index](https://cs2.paradoxwikis.com/Developer_diaries) | cs2.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 106 | [Cities: Skylines II Wiki — Economy (economy panel tabs, company efficiency contributors)](https://cs2.paradoxwikis.com/Economy) | cs2.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 107 | [Cities: Skylines II Wiki — Info views (33 views, opening control, per-channel recolouring, colo](https://cs2.paradoxwikis.com/Info_views) | cs2.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 108 | [Cities: Skylines II Wiki — Services (Selected Info Panel / SIP, hover-to-decompose, budget-effi](https://cs2.paradoxwikis.com/Services) | cs2.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 109 | [Cities: Skylines II Wiki — Traffic (flow vs volume legend toggle; no individual route visualisa](https://cs2.paradoxwikis.com/Traffic) | cs2.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 110 | [Cities: Skylines II Wiki — Zoning (demand drivers per zone type; absence of documented reason-b](https://cs2.paradoxwikis.com/Zoning) | cs2.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 111 | [Frostpunk 2 Review — DailyGamingTech [CRITIC, direct quote: 'Overlay tooltips, shifting panels,](https://dailygamingtech.com/2025/10/05/frostpunk-2-review) | dailygamingtech.com | Frostpunk |
| 112 | [Szafir publications index (source for the Where's My Data record and project page)](https://danielleszafir.com/publications.html) | danielleszafir.com | Uncertainty visualisation research and its practical encodin |
| 113 | [Data-to-Viz — Sankey diagram: uses, pitfalls, alternatives](https://www.data-to-viz.com/graph/sankey.html) | data-to-viz.com | Causal explanation interfaces for MERIDIAN — "why did this c |
| 114 | [dbltap interview with Cole Jefferies — via search summary only; source of the Sherlock Holmes: ](https://www.dbltap.com/posts/blade-runner-meets-sherlock-holmes-in-shadows-of-doubt-01g1v0r94s9w) | dbltap.com | Shadows of Doubt |
| 115 | [deck.gl — Coordinate Systems (developer guide)](https://deck.gl/docs/developer-guide/coordinate-systems) | deck.gl | Frontend technical feasibility for MERIDIAN: framework, pack |
| 116 | [GOV.UK Design System — Details component (guidance and user research findings)](https://design-system.service.gov.uk/components/details) | design-system.service.gov.uk | Progressive disclosure and information density in expert int |
| 117 | [Inset text component (GOV.UK Design System)](https://design-system.service.gov.uk/components/inset-text) | design-system.service.gov.uk | Provenance and fact-versus-narration separation in an interf |
| 118 | [GOV.UK Design System — Notification banner component; concurrency limits, channel separation, b](https://design-system.service.gov.uk/components/notification-banner) | design-system.service.gov.uk | Alerts, attention and time pressure: an evidence base and co |
| 119 | [Warning text component (GOV.UK Design System)](https://design-system.service.gov.uk/components/warning-text) | design-system.service.gov.uk | Provenance and fact-versus-narration separation in an interf |
| 120 | [GOV.UK Design System — Check answers pattern](https://design-system.service.gov.uk/patterns/check-answers) | design-system.service.gov.uk | Natural-language command and action-confirmation interfaces  |
| 121 | [GOV.UK Design System — Type scale (7 steps, desktop/mobile, paired line-heights)](https://design-system.service.gov.uk/styles/type-scale) | design-system.service.gov.uk | Building an original "near-future command system" visual lan |
| 122 | [Designer Notes — Mohawk category index (post list)](http://www.designer-notes.com/category/mohawk) | designer-notes.com | Old World |
| 123 | [Soren Johnson, 'Old World Designer Notes #9: Events' (trigger/requirement/effect, subjects, wei](http://www.designer-notes.com/old-world-designer-notes-9-events) | designer-notes.com | Old World |
| 124 | [Soren Johnson, 'My Elephant in the Room, Part 1' — Designer Notes (orders system, infinite tool](https://www.designer-notes.com/my-elephant-in-the-room-part-1) | designer-notes.com | Old World |
| 125 | [Soren Johnson, 'My Elephant in the Room, Part 2' — Designer Notes (characters, 10 archetypes, '](https://www.designer-notes.com/my-elephant-in-the-room-part-2) | designer-notes.com | Old World |
| 126 | [Soren Johnson, 'My Elephant in the Room, Part 3' — Designer Notes (event system scale, loose co](https://www.designer-notes.com/my-elephant-in-the-room-part-3) | designer-notes.com | Old World |
| 127 | [Soren Johnson, 'Old World Designer Notes #11: The End' (ambitions, tier ranges, leader-scoped g](https://www.designer-notes.com/old-world-designer-notes-11-the-end) | designer-notes.com | Old World |
| 128 | [US Web Design System — Design tokens (8 categories, 8px spacing rationale)](https://designsystem.digital.gov/design-tokens) | designsystem.digital.gov | Building an original "near-future command system" visual lan |
| 129 | [Design Tokens Format Module 2025.10 (Design Tokens Community Group)](https://www.designtokens.org/TR/drafts/format) | designtokens.org | Building an original "near-future command system" visual lan; Frontend technical feasibility for MERIDIAN: fra |
| 130 | [Android Developers — Create and manage notification channels; five importance levels and immuta](https://developer.android.com/develop/ui/views/notifications/channels) | developer.android.com | Alerts, attention and time pressure: an evidence base and co |
| 131 | [Chrome DevTools — Performance panel reference (timeline overview minimap, range selection, brea](https://developer.chrome.com/docs/devtools/performance/reference) | developer.chrome.com | Time, pause, replay, branching and counterfactual presentati |
| 132 | [MDN — Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) | developer.mozilla.org | Frontend technical feasibility for MERIDIAN: framework, pack |
| 133 | [MDN — ARIA live regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions) | developer.mozilla.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma; Building an original "near-future command system |
| 134 | [forced-colors CSS media feature (MDN Web Docs)](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors) | developer.mozilla.org | Building an original "near-future command system" visual lan; Provenance and fact-versus-narration separation  |
| 135 | [MDN — prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) | developer.mozilla.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma; Building an original "near-future command system |
| 136 | [MDN — font-variant-numeric (tabular-nums, lining-nums, slashed-zero)](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric) | developer.mozilla.org | Building an original "near-future command system" visual lan |
| 137 | [DHS S&T, Android Team Awareness Kit for Wildland Fire Incident Response — identified via search](https://www.dhs.gov/science-and-technology/publication/android-team-awareness-kit-wildland-fire-incident-response) | dhs.gov | Military & emergency command-and-control interfaces: ATAK/Wi |
| 138 | [van Ham & Perer — publication record (CMU DIG)](https://dig.cmu.edu/publications/2009-doigraphs.html) | dig.cmu.edu | Relationship graph visualisation at scale — node-link vs mat |
| 139 | [Frostpunk 2 Review — Digital Trends [CRITIC: hidden locked-tech effects; cannot parse failure c](https://www.digitaltrends.com/gaming/frostpunk-2-review-pc) | digitaltrends.com | Frostpunk |
| 140 | [Disco Elysium Wiki (wiki.gg) — Checks (white vs red, modifier sources, up to ten modifiers, 2d6](https://discoelysium.wiki.gg/wiki/Checks) | discoelysium.wiki.gg | Disco Elysium |
| 141 | [Disco Elysium Wiki (wiki.gg) — Skills (attributes, 24 skills as voices, difficulty tiers and ta](https://discoelysium.wiki.gg/wiki/Skills) | discoelysium.wiki.gg | Disco Elysium |
| 142 | [Disco Elysium Wiki (wiki.gg) — Thought Cabinet (slots, research times, temporary vs fixed bonus](https://discoelysium.wiki.gg/wiki/Thought_Cabinet) | discoelysium.wiki.gg | Disco Elysium |
| 143 | [Elmqvist & Fekete — Hierarchical Aggregation for Information Visualization: Overview, Technique](https://dl.acm.org/doi/10.1109/TVCG.2009.84) | dl.acm.org | Relationship graph visualisation at scale — node-link vs mat |
| 144 | [Holten & van Wijk — A User Study on Visualizing Directed Edges in Graphs (CHI 2009)](https://dl.acm.org/doi/10.1145/1518701.1519054) | dl.acm.org | Relationship graph visualisation at scale — node-link vs mat |
| 145 | [McGee & Dingliana — An empirical study on the impact of edge bundling on user comprehension of ](https://dl.acm.org/doi/10.1145/2254556.2254670) | dl.acm.org | Relationship graph visualisation at scale — node-link vs mat |
| 146 | [Cockburn, Gutwin, Scarr & Malacria, 'Supporting Novice to Expert Transitions in User Interfaces](https://dl.acm.org/doi/10.1145/2659796) | dl.acm.org | Bloomberg Terminal |
| 147 | [Wallinger, Akbulut et al. — How Do People Perceive Bundling? An Experiment (CHI 2025) — NOT VER](https://dl.acm.org/doi/full/10.1145/3706598.3713444) | dl.acm.org | Relationship graph visualisation at scale — node-link vs mat |
| 148 | [Linkurious Enterprise User Manual — Expand nodes (expandThreshold, superNodeThreshold)](https://doc.linkurious.com/user-manual/latest/expand) | doc.linkurious.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 149 | [Linkurious Enterprise User Manual — Filter panel](https://doc.linkurious.com/user-manual/latest/filter-panel) | doc.linkurious.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 150 | [Linkurious Enterprise User Manual — Timeline](https://doc.linkurious.com/user-manual/latest/timeline) | doc.linkurious.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 151 | [Watchdog (Datadog docs) — 'Datadog's AI engine', Watchdog Alerts feed, Watchdog Insights in das](https://docs.datadoghq.com/watchdog) | docs.datadoghq.com | Security operations, observability and incident-response con |
| 152 | [DFHack documentation — tool index (400+ tools; referenced via search, not fetched in full)](https://docs.dfhack.org/en/stable/docs/Tools.html) | docs.dfhack.org | Dwarf Fortress |
| 153 | [DFHack documentation — sort (search and sort overlays for v50 screens; fetched)](https://docs.dfhack.org/en/stable/docs/tools/sort.html) | docs.dfhack.org | Dwarf Fortress |
| 154 | [i2 Analyst's Notebook 10.1.2 — About conditional formatting](https://docs.i2group.com/anb/10.1.2/about_conditional_formatting.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 155 | [i2 Analyst's Notebook 10.1.2 — About entities (representations and types)](https://docs.i2group.com/anb/10.1.2/about_entities.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 156 | [i2 Analyst's Notebook 10.1.2 — About social network analysis](https://docs.i2group.com/anb/10.1.2/about_social_network_analysis.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 157 | [i2 Analyst's Notebook 10.1.2 — Investigate item activity (Activity View)](https://docs.i2group.com/anb/10.1.2/activity_view_investigate.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 158 | [i2 Analyst's Notebook 10.1.2 — Adding link weightings](https://docs.i2group.com/anb/10.1.2/adding_link_weightings.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 159 | [i2 Analyst's Notebook 10.1.2 — Analytical chart layouts](https://docs.i2group.com/anb/10.1.2/analytical_chart_layouts.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 160 | [i2 Analyst's Notebook 10.1.2 — Filter and drill down](https://docs.i2group.com/anb/10.1.2/filter_drill_down.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 161 | [i2 Analyst's Notebook 10.1.2 — Find networks](https://docs.i2group.com/anb/10.1.2/find_networks.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 162 | [i2 Analyst's Notebook 10.1.2 — Focus on items of interest](https://docs.i2group.com/anb/10.1.2/focus_on_items_of_interest.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 163 | [i2 Analyst's Notebook 10.1.2 — Selecting centrality measures](https://docs.i2group.com/anb/10.1.2/selecting_centrality_measures.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 164 | [i2 Analyst's Notebook 10.1.2 — Setting clustering and centrality measures](https://docs.i2group.com/anb/10.1.2/setting_centrality_measures.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 165 | [i2 Analyst's Notebook 10.1.2 — Centrality and centrality measures](https://docs.i2group.com/anb/10.1.2/sna_centrality.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 166 | [i2 Analyst's Notebook 10.1.2 — Statistical views of chart data](https://docs.i2group.com/anb/10.1.2/statistical_views_of_chart_data.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 167 | [i2 Analyst's Notebook 10.1.2 — Working with the Time Wheel](https://docs.i2group.com/anb/10.1.2/time_wheel.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 168 | [i2 Analyst's Notebook 10.1.2 — Working with bar charts and histograms](https://docs.i2group.com/anb/10.1.2/working_with_bar_charts_and_histograms.html) | docs.i2group.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 169 | [Mapbox Style Specification — Symbol layer collision properties (symbol-sort-key, text-optional,](https://docs.mapbox.com/style-spec/reference/layers) | docs.mapbox.com | Map and layer design for multi-domain data — cartographic ba |
| 170 | [ORBAT Mapper military symbology guide — corroborates the 20-digit SIDC structure; page itself r](https://docs.orbat-mapper.app/guide/military-symbology) | docs.orbat-mapper.app | Military & emergency command-and-control interfaces: ATAK/Wi |
| 171 | [ICD 203: Analytic Standards — independent transcription (used to cross-check the percentage ran](https://docslib.org/doc/1758313/icd-203-analytic-standards) | docslib.org | Intelligence-analysis tradecraft standards for expressing un |
| 172 | [Cramming 'Papers, Please' Onto Phones — Lucas Pope mobile devlog (NOT DIRECTLY FETCHABLE, HTTP ](https://dukope.com/devlogs/papers-please/mobile) | dukope.com | Evidence, deduction and document-verification interfaces |
| 173 | [Dwarf Fortress Wiki — Legends (v50; fetched)](http://dwarffortresswiki.org/legends) | dwarffortresswiki.org | Dwarf Fortress |
| 174 | [Dwarf Fortress Wiki — Announcements (v50; fetched)](https://dwarffortresswiki.org/index.php/Announcements) | dwarffortresswiki.org | Dwarf Fortress |
| 175 | [Dwarf Fortress Wiki — DF2014:Military interface (classic-era; fetched)](https://dwarffortresswiki.org/index.php/DF2014:Military_interface) | dwarffortresswiki.org | Dwarf Fortress |
| 176 | [Dwarf Fortress Wiki — Main Page (10,116 articles; Quickstart guide)](https://dwarffortresswiki.org/index.php/Main_Page) | dwarffortresswiki.org | Onboarding and learnability for very deep simulations — evid |
| 177 | [Dwarf Fortress Wiki — Thoughts and preferences (v50 namespace; fetched)](https://dwarffortresswiki.org/index.php/Thoughts_and_preferences) | dwarffortresswiki.org | Dwarf Fortress |
| 178 | [Dwarf Fortress Wiki — Unit list (v50; fetched)](https://dwarffortresswiki.org/index.php/Unit_list) | dwarffortresswiki.org | Dwarf Fortress |
| 179 | [Dwarf Fortress Wiki — Utility:DFHack (fetched)](https://dwarffortresswiki.org/index.php/Utility:DFHack) | dwarffortresswiki.org | Dwarf Fortress |
| 180 | [Dwarf Fortress Wiki — Utility:Dwarf therapist (fetched)](https://dwarffortresswiki.org/index.php/Utility:Dwarf_therapist) | dwarffortresswiki.org | Dwarf Fortress |
| 181 | [Dwarf Fortress Wiki — Utility:Legends viewer (fetched)](https://dwarffortresswiki.org/index.php/Utility:Legends_viewer) | dwarffortresswiki.org | Dwarf Fortress |
| 182 | [Dwarf Fortress Wiki — Work detail (v50; fetched)](https://dwarffortresswiki.org/index.php/Work_detail) | dwarffortresswiki.org | Dwarf Fortress |
| 183 | [Dwarf Fortress Wiki — Interface (v50; fetched)](https://dwarffortresswiki.org/interface) | dwarffortresswiki.org | Dwarf Fortress |
| 184 | [FETCH FAILED (302 redirect to an unblock interstitial) — 14 CFR 25.1322, Flightcrew alerting, v](https://www.ecfr.gov/current/title-14/section-25.1322) | ecfr.gov | Alerts, attention and time pressure: an evidence base and co |
| 185 | [Hoekstra, Morey, Rouder & Wagenmakers, Robust misinterpretation of confidence intervals, Psycho](https://www.ejwagenmakers.com/inpress/HoekstraEtAlPBR.pdf) | ejwagenmakers.com | Uncertainty visualisation research and its practical encodin |
| 186 | [Attack Discovery (Elastic Security docs) — LLM correlation of up to 100 alerts from the last 24](https://www.elastic.co/docs/solutions/security/ai/attack-discovery) | elastic.co | Security operations, observability and incident-response con |
| 187 | [Manage detection alerts (Elastic Security docs) — Group alerts by (up to three nested fields), ](https://www.elastic.co/docs/solutions/security/detect-and-alert/manage-detection-alerts) | elastic.co | Security operations, observability and incident-response con |
| 188 | [Suppress detection alerts (Elastic Security docs) — suppression fields, per-rule-execution vs p](https://www.elastic.co/docs/solutions/security/detect-and-alert/suppress-detection-alerts) | elastic.co | Security operations, observability and incident-response con |
| 189 | [Wikipedia: Admiralty code — A–F reliability and 1–6 credibility definitions](https://en.wikipedia.org/wiki/Admiralty_code) | en.wikipedia.org | Intelligence-analysis tradecraft standards for expressing un |
| 190 | [Wikipedia — After-action review](https://en.wikipedia.org/wiki/After-action_review) | en.wikipedia.org | Onboarding and learnability for very deep simulations — evid; Time, pause, replay, branching and counterfactua |
| 191 | [Wikipedia — Air traffic control radar beacon system (data block fields)](https://en.wikipedia.org/wiki/Air_traffic_control_radar_beacon_system) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 192 | [Wikipedia — Alarm fatigue (TERTIARY SOURCE; used only for the cross-domain incident and regulat](https://en.wikipedia.org/wiki/Alarm_fatigue) | en.wikipedia.org | Alerts, attention and time pressure: an evidence base and co |
| 193 | [Wikipedia — Alarm management (alarm flood, historical colour convention)](https://en.wikipedia.org/wiki/Alarm_management) | en.wikipedia.org | Alerts, attention and time pressure: an evidence base and co; Safety-critical control-room interface design ca |
| 194 | [Wikipedia: Analysis of competing hypotheses — seven-step process, matrix orientation, diagnosti](https://en.wikipedia.org/wiki/Analysis_of_competing_hypotheses) | en.wikipedia.org | Intelligence-analysis tradecraft standards for expressing un |
| 195 | [Android Team Awareness Kit — Wikipedia (confirms APP-6 symbology use and plugin architecture; c](https://en.wikipedia.org/wiki/Android_Team_Awareness_Kit) | en.wikipedia.org | Military & emergency command-and-control interfaces: ATAK/Wi |
| 196 | [Wikipedia — Apollo Guidance Computer (DSKY, 1201/1202 program alarms, ICD root cause)](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 197 | [Apple Computer, Inc. v. Microsoft Corp. — analytic dissection, virtual identity standard](https://en.wikipedia.org/wiki/Apple_Computer,_Inc._v._Microsoft_Corp.) | en.wikipedia.org | Building an original "near-future command system" visual lan |
| 198 | [Wikipedia — Automation bias (commission/omission errors, empirical findings, mitigations)](https://en.wikipedia.org/wiki/Automation_bias) | en.wikipedia.org | Safety-critical control-room interface design canon; Situation awareness and the command shell: SA theory, eco |
| 199 | [Bloomberg Terminal — Wikipedia (interface, keyboard, panels, Launchpad, pricing, subscribers)](https://en.wikipedia.org/wiki/Bloomberg_Terminal) | en.wikipedia.org | Bloomberg Terminal |
| 200 | [Wikipedia — Brushing and linking (Becker & Cleveland, 'Brushing Scatterplots', Technometrics 19](https://en.wikipedia.org/wiki/Brushing_and_linking) | en.wikipedia.org | Map and layer design for multi-domain data — cartographic ba |
| 201 | [Wikipedia — Chartjunk (secondary source for Bateman et al. 2010 'Useful Junk?', Kosara, Few, Pa](https://en.wikipedia.org/wiki/Chartjunk) | en.wikipedia.org | Progressive disclosure and information density in expert int |
| 202 | [Wikipedia — Christopher C. Kraft Jr. Mission Control Center (four-tier auditorium, map screen, ](https://en.wikipedia.org/wiki/Christopher_C._Kraft_Jr._Mission_Control_Center) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 203 | [Wikipedia — Circular error probable (CEP, R95, DRMS, error ellipse)](https://en.wikipedia.org/wiki/Circular_error_probable) | en.wikipedia.org | Map and layer design for multi-domain data — cartographic ba |
| 204 | [Wikipedia — Cities: Skylines II (reception; IGN and PCGamesN quotes; Hallikainen 'toxic levels'](https://en.wikipedia.org/wiki/Cities:_Skylines_II) | en.wikipedia.org | Cities: Skylines 1 & 2 |
| 205 | [Wikipedia: Classified information in the United States — portion marking, banner lines, dissemi](https://en.wikipedia.org/wiki/Classified_information_in_the_United_States) | en.wikipedia.org | Intelligence-analysis tradecraft standards for expressing un |
| 206 | [Wikipedia — Cognitive load (intrinsic/extraneous/germane, expertise reversal, split attention, ](https://en.wikipedia.org/wiki/Cognitive_load) | en.wikipedia.org | Onboarding and learnability for very deep simulations — evid |
| 207 | [Wikipedia — Cognitive work analysis (Rasmussen/Vicente five phases, formative approach)](https://en.wikipedia.org/wiki/Cognitive_work_analysis) | en.wikipedia.org | Safety-critical control-room interface design canon; Situation awareness and the command shell: SA theory, eco |
| 208 | [Wikipedia — Combat Mission (video game series) (WEGO orders/execution phases, 60-second turn, s](https://en.wikipedia.org/wiki/Combat_Mission_(video_game_series)) | en.wikipedia.org | Hearts of Iron IV |
| 209 | [Wikipedia — Command: Modern Air/Naval Operations (preset missions vs direct orders, Professiona](https://en.wikipedia.org/wiki/Command:_Modern_Operations) | en.wikipedia.org | Hearts of Iron IV |
| 210 | [Wikipedia — Counterfactual conditional (Lewis variably strict conditional, Stalnaker uniqueness](https://en.wikipedia.org/wiki/Counterfactual_conditional) | en.wikipedia.org | Time, pause, replay, branching and counterfactual presentati |
| 211 | [Wikipedia — Debriefing (simulation-based training; ~25% team performance finding)](https://en.wikipedia.org/wiki/Debriefing) | en.wikipedia.org | Onboarding and learnability for very deep simulations — evid |
| 212 | [Wikipedia — Disco Elysium (skills as internal voices, 2d6, Thought Cabinet, power coupled to li](https://en.wikipedia.org/wiki/Disco_Elysium) | en.wikipedia.org | Disco Elysium |
| 213 | [Wikipedia — Dwarf Fortress (interface criticism; Adams on tutorial and UI priority; community d](https://en.wikipedia.org/wiki/Dwarf_Fortress) | en.wikipedia.org | Onboarding and learnability for very deep simulations — evid |
| 214 | [Wikipedia — Ecological interface design (abstraction hierarchy, SRK, limitations)](https://en.wikipedia.org/wiki/Ecological_interface_design) | en.wikipedia.org | Progressive disclosure and information density in expert int; Safety-critical control-room interface design ca |
| 215 | [Wikipedia — Edward Tufte (secondary source for data-ink ratio 1982, small multiples 1990, lie f](https://en.wikipedia.org/wiki/Edward_Tufte) | en.wikipedia.org | Progressive disclosure and information density in expert int |
| 216 | [Eikon (software) — Wikipedia (Thomson Reuters → Refinitiv → LSEG Workspace)](https://en.wikipedia.org/wiki/Eikon) | en.wikipedia.org | Bloomberg Terminal |
| 217 | [Wikipedia — Electronic centralised aircraft monitor (ECAM level 3/2/1 tiering, QF32 80+ alerts)](https://en.wikipedia.org/wiki/Electronic_centralised_aircraft_monitor) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 218 | [Wikipedia — Experiential learning (Kolb's cycle; learning-styles neuromyth critique)](https://en.wikipedia.org/wiki/Experiential_learning) | en.wikipedia.org | Onboarding and learnability for very deep simulations — evid |
| 219 | [Wikipedia — Flight controller (FCR/MPSR, report-by-exception, go/no-go poll, abort authority)](https://en.wikipedia.org/wiki/Flight_controller) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 220 | [Google LLC v. Oracle America, Inc. (2021) — fair use of declaring code; copyrightability expres](https://en.wikipedia.org/wiki/Google_LLC_v._Oracle_America,_Inc.) | en.wikipedia.org | Building an original "near-future command system" visual lan |
| 221 | [Wikipedia — Ground proximity warning system (TERTIARY; used only for the observation that alert](https://en.wikipedia.org/wiki/Ground_proximity_warning_system) | en.wikipedia.org | Alerts, attention and time pressure: an evidence base and co |
| 222 | [Wikipedia — Hearts of Iron IV (systems overview and critical reception: IGN, GameSpot, PC Gamer](https://en.wikipedia.org/wiki/Hearts_of_Iron_IV) | en.wikipedia.org | Hearts of Iron IV; Onboarding and learnability for very deep simulations — evid |
| 223 | [Her Story — Wikipedia (L.O.G.I.C. database, 271 clips, user tags, red/green database checker)](https://en.wikipedia.org/wiki/Her_Story_(video_game)) | en.wikipedia.org | Evidence, deduction and document-verification interfaces |
| 224 | [Wikipedia — Human reliability (THERP, SPAR-H, CREAM, performance-shaping factors)](https://en.wikipedia.org/wiki/Human_reliability) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 225 | [Immortality — Wikipedia (match-cut click-a-person-or-object navigation)](https://en.wikipedia.org/wiki/Immortality_(video_game)) | en.wikipedia.org | Evidence, deduction and document-verification interfaces |
| 226 | [Influence diagram — node shapes and arc semantics](https://en.wikipedia.org/wiki/Influence_diagram) | en.wikipedia.org | Causal explanation interfaces for MERIDIAN — "why did this c |
| 227 | [Wikipedia — Instructional scaffolding (ZPD, fading, Bruner, Vygotsky)](https://en.wikipedia.org/wiki/Instructional_scaffolding) | en.wikipedia.org | Onboarding and learnability for very deep simulations — evid |
| 228 | [Wikipedia: Intelligence analysis — source reliability vs credibility vs denial-and-deception, f](https://en.wikipedia.org/wiki/Intelligence_analysis) | en.wikipedia.org | Intelligence-analysis tradecraft standards for expressing un |
| 229 | [Wikipedia: Intelligence source and information reliability — grading tables, FM 2-22.3 referenc](https://en.wikipedia.org/wiki/Intelligence_source_and_information_reliability) | en.wikipedia.org | Intelligence-analysis tradecraft standards for expressing un |
| 230 | [Jens Rasmussen (human factors expert) — Wikipedia (dynamic safety model, migration to boundarie](https://en.wikipedia.org/wiki/Jens_Rasmussen_(human_factors_expert)) | en.wikipedia.org | Situation awareness and the command shell: SA theory, ecolog |
| 231 | [Layered graph drawing (Sugiyama method) — stages and complexity](https://en.wikipedia.org/wiki/Layered_graph_drawing) | en.wikipedia.org | Causal explanation interfaces for MERIDIAN — "why did this c; Time, pause, replay, branching and counterfactua |
| 232 | [Lotus Dev. Corp. v. Borland Int'l, Inc. — menu hierarchy as uncopyrightable method of operation](https://en.wikipedia.org/wiki/Lotus_Dev._Corp._v._Borland_Int%27l,_Inc.) | en.wikipedia.org | Building an original "near-future command system" visual lan |
| 233 | [Mica Endsley — Wikipedia (biography and publication list; confirmed to contain no documented cr](https://en.wikipedia.org/wiki/Mica_Endsley) | en.wikipedia.org | Situation awareness and the command shell: SA theory, ecolog |
| 234 | [Mode (user interface) — Wikipedia (mode error definition and causes; AF447, Asiana 214, USS Joh](https://en.wikipedia.org/wiki/Mode_(user_interface)) | en.wikipedia.org | Situation awareness and the command shell: SA theory, ecolog |
| 235 | [Wikipedia — Modifiable areal unit problem (scale effect, zone effect, Openshaw)](https://en.wikipedia.org/wiki/Modifiable_areal_unit_problem) | en.wikipedia.org | Map and layer design for multi-domain data — cartographic ba |
| 236 | [NASA-TLX — Wikipedia (six subscales, pairwise weighting procedure, Raw TLX and its reported val](https://en.wikipedia.org/wiki/NASA-TLX) | en.wikipedia.org | Situation awareness and the command shell: SA theory, ecolog |
| 237 | [NATO Joint Military Symbology — Wikipedia (frame shapes, affiliations, solid/dashed status, 'Fu](https://en.wikipedia.org/wiki/NATO_Joint_Military_Symbology) | en.wikipedia.org | Building an original "near-future command system" visual lan; Map and layer design for multi-domain data — car |
| 238 | [Wikipedia: National Intelligence Estimate — key judgements, per-judgement confidence assignment](https://en.wikipedia.org/wiki/National_Intelligence_Estimate) | en.wikipedia.org | Intelligence-analysis tradecraft standards for expressing un |
| 239 | [OODA loop — Wikipedia (four stages, primacy of orientation, late commitment, Hankins' vagueness](https://en.wikipedia.org/wiki/OODA_loop) | en.wikipedia.org | Situation awareness and the command shell: SA theory, ecolog |
| 240 | [Wikipedia — Palantir Technologies (deployments, contracts, criticism)](https://en.wikipedia.org/wiki/Palantir_Technologies) | en.wikipedia.org | Palantir Gotham and Foundry |
| 241 | [Papers, Please — Wikipedia (workstation layout, citations by fax, HyperCard-inspired clunkiness](https://en.wikipedia.org/wiki/Papers,_Please) | en.wikipedia.org | Evidence, deduction and document-verification interfaces |
| 242 | [Wikipedia — Pentiment (video game) (backgrounds affecting resolution; accusation mechanic; PC G](https://en.wikipedia.org/wiki/Pentiment_(video_game)) | en.wikipedia.org | Disco Elysium |
| 243 | [Wikipedia — Provenance, data provenance section (documentation sufficient to allow reproducibil](https://en.wikipedia.org/wiki/Provenance) | en.wikipedia.org | Time, pause, replay, branching and counterfactual presentati |
| 244 | [Wikipedia — Qantas Flight 32 (~100 ECAM checklists, limitations of current alerting systems)](https://en.wikipedia.org/wiki/Qantas_Flight_32) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 245 | [Wikipedia — Real-time with pause (TERTIARY AND WEAK; active vs passive pause, games using it; n](https://en.wikipedia.org/wiki/Real-time_with_pause) | en.wikipedia.org | Alerts, attention and time pressure: an evidence base and co; Time, pause, replay, branching and counterfactua |
| 246 | [Refinitiv — Wikipedia (Blackstone/LSEG acquisition, Workspace rebrand)](https://en.wikipedia.org/wiki/Refinitiv) | en.wikipedia.org | Bloomberg Terminal |
| 247 | [Wikipedia — Replay (gaming) (input-log vs video capture; TrackMania, Doom, N; proprietary forma](https://en.wikipedia.org/wiki/Replay_(gaming)) | en.wikipedia.org | Time, pause, replay, branching and counterfactual presentati |
| 248 | [Return of the Obra Dinn — Wikipedia (logbook, rule of three, last six in twos, development hist](https://en.wikipedia.org/wiki/Return_of_the_Obra_Dinn) | en.wikipedia.org | Evidence, deduction and document-verification interfaces |
| 249 | [Wikipedia: Richards Heuer — mindsets, bias resistance, methodology as remedy](https://en.wikipedia.org/wiki/Richards_Heuer) | en.wikipedia.org | Intelligence-analysis tradecraft standards for expressing un |
| 250 | [Rise of the Golden Idol — Wikipedia (chapter-spanning narrative blocks; contains no UI-specific](https://en.wikipedia.org/wiki/Rise_of_the_Golden_Idol) | en.wikipedia.org | Evidence, deduction and document-verification interfaces |
| 251 | [Wikipedia — Save scumming (seeded deterministic PRNG, permadeath, NetHack filesystem protection](https://en.wikipedia.org/wiki/Save_scumming) | en.wikipedia.org | Time, pause, replay, branching and counterfactual presentati |
| 252 | [Wikipedia — Shadow Empire (background, release, reception)](https://en.wikipedia.org/wiki/Shadow_Empire) | en.wikipedia.org | Shadow Empire |
| 253 | [Wikipedia: Shadows of Doubt (fetched — resolution form with per-element bonuses, aggregate rece](https://en.wikipedia.org/wiki/Shadows_of_Doubt) | en.wikipedia.org | Shadows of Doubt |
| 254 | [Wikipedia: Sherman Kent — WEP, Office of National Estimates, the Kent School](https://en.wikipedia.org/wiki/Sherman_Kent) | en.wikipedia.org | Intelligence-analysis tradecraft standards for expressing un |
| 255 | [Wikipedia — Short-term conflict alert (~2 minute look-ahead ceiling, nuisance alerts)](https://en.wikipedia.org/wiki/Short-term_conflict_alert) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 256 | [Wikipedia — Situation awareness (Endsley three levels, SAGAT, circularity critique)](https://en.wikipedia.org/wiki/Situation_awareness) | en.wikipedia.org | Progressive disclosure and information density in expert int; Safety-critical control-room interface design ca |
| 257 | [Suzerain (video game) — Wikipedia](https://en.wikipedia.org/wiki/Suzerain_(video_game)) | en.wikipedia.org | Disco Elysium; Suzerain |
| 258 | [Terra Invicta — Wikipedia (fetched; systems overview and attributed critical reception incl. IG](https://en.wikipedia.org/wiki/Terra_Invicta) | en.wikipedia.org | Terra Invicta |
| 259 | [The Roottrees are Dead — Wikipedia (evidence-board family tree, name/picture/occupation slots, ](https://en.wikipedia.org/wiki/The_Roottrees_are_Dead) | en.wikipedia.org | Evidence, deduction and document-verification interfaces |
| 260 | [Wikipedia — Three Mile Island accident (PORV lamp, Kemeny Commission 'cacophony of undifferenti](https://en.wikipedia.org/wiki/Three_Mile_Island_accident) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 261 | [Trade dress — Lanham Act §43(a), distinctiveness, secondary meaning (Wal-Mart v Samara), functi](https://en.wikipedia.org/wiki/Trade_dress) | en.wikipedia.org | Building an original "near-future command system" visual lan |
| 262 | [Wikipedia — Traffic collision avoidance system (TA 40s / RA 25s, no-manoeuvre-on-TA rule)](https://en.wikipedia.org/wiki/Traffic_collision_avoidance_system) | en.wikipedia.org | Safety-critical control-room interface design canon |
| 263 | [Wikipedia — Undo (linear, multilevel, non-linear/selective undo; US&R history tree "hard to com](https://en.wikipedia.org/wiki/Undo) | en.wikipedia.org | Time, pause, replay, branching and counterfactual presentati |
| 264 | [Wikipedia — Verification and validation of computer simulation models (validity determined for ](https://en.wikipedia.org/wiki/Verification_and_validation_of_computer_simulation_models) | en.wikipedia.org | Time, pause, replay, branching and counterfactual presentati |
| 265 | [Wikipedia — Visual variable (Bertin's variables; crispness for uncertainty)](https://en.wikipedia.org/wiki/Visual_variable) | en.wikipedia.org | Map and layer design for multi-domain data — cartographic ba |
| 266 | [Wikipedia: Words of estimative probability — Kent's 1964 chart, poets vs mathematicians, NIC an](https://en.wikipedia.org/wiki/Words_of_estimative_probability) | en.wikipedia.org | Intelligence-analysis tradecraft standards for expressing un; Uncertainty visualisation research and its pract |
| 267 | [Wikipedia — Working memory (secondary source for Miller 1956 seven chunks; Cowan 2001 four chun](https://en.wikipedia.org/wiki/Working_memory) | en.wikipedia.org | Progressive disclosure and information density in expert int |
| 268 | [Iqbal, S. T. & Horvitz, E. — Disruption and Recovery of Computing Tasks: Field Study, Analysis,](https://erichorvitz.com/CHI_2007_Iqbal_Horvitz.pdf) | erichorvitz.com | Alerts, attention and time pressure: an evidence base and co |
| 269 | [Ledger — Europa Universalis 4 Wiki (page taxonomy, 'L' hotkey, income/cost/trade/charts tabs)](https://eu4.paradoxwikis.com/Ledger) | eu4.paradoxwikis.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 270 | [Europa Universalis IV Wiki — Map modes (shipped 40+ switchable thematic views; persistent invar](https://eu4.paradoxwikis.com/Map_modes) | eu4.paradoxwikis.com | Map and layer design for multi-domain data — cartographic ba |
| 271 | [Province interface — Europa Universalis 4 Wiki (panel-by-panel layout; institution tooltips exp](https://eu4.paradoxwikis.com/Province_interface) | eu4.paradoxwikis.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 272 | [Eversim — company site](https://eversim-sas.com) | eversim-sas.com | Power & Revolution / Geopolitical Simulator 4 |
| 273 | [eXplorminate — 'What to eXpect: Shadow Empire's Initial Review'](https://explorminate.org/what-to-expect-shadow-empire) | explorminate.org | Shadow Empire |
| 274 | [FETCH FAILED (HTTP 403) — FAA Advisory Circular 25.1322-1, Flightcrew Alerting. Would supply th](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_25.1322-1.pdf) | faa.gov | Alerts, attention and time pressure: an evidence base and co |
| 275 | [FastAPI — WebSockets (advanced)](https://fastapi.tiangolo.com/advanced/websockets) | fastapi.tiangolo.com | Frontend technical feasibility for MERIDIAN: framework, pack |
| 276 | [Papers, Please TIGSource devlog (third-party scrape of Lucas Pope's original devlog; dukope.com](https://fguillen.github.io/PapersPleaseDevlogScrap) | fguillen.github.io | Evidence, deduction and document-verification interfaces |
| 277 | [Bloomberg Terminal releases document search and analysis feature — The Fixed Income Desk](https://www.fi-desk.com/bloomberg-terminal-releases-document-search-and-analysis-feature) | fi-desk.com | Bloomberg Terminal |
| 278 | [Current & Potential Ability — FMInside (SEARCH SNIPPET ONLY — 403; star colour semantics incl. ](https://fminside.net/guides/basic-guides/76-current-potential-ability) | fminside.net | Football Manager |
| 279 | [Scouting Reports: Why do some players have black stars? — FM Scout (SEARCH SNIPPET ONLY — 403; ](https://www.fmscout.com/a-black-stars-in-scouting-reports.html) | fmscout.com | Football Manager |
| 280 | [Gameplay Upgrades / Football Manager 26 — official (PRIMARY — fetched; Touchline Tablet, Match ](https://www.footballmanager.com/features/gameplay-upgrades) | footballmanager.com | Football Manager |
| 281 | [Development Update: Football Manager 25 — Sports Interactive (PRIMARY — fetched; tile-and-card ](https://www.footballmanager.com/news/development-update-football-manager-25) | footballmanager.com | Football Manager |
| 282 | ['Football Manager 26': Is It As Bad As The Steam Reviews Suggest? — Forbes, Barry Collins (fetc](https://www.forbes.com/sites/barrycollins/2025/11/08/football-manager-26-is-it-as-bad-as-the-steam-reviews-suggest) | forbes.com | Football Manager |
| 283 | ['With Symphony, financial firms strike back at Bloomberg terminals' — Fortune, 10 May 2015 (Per](https://fortune.com/2015/05/10/perzo-symphony-bloomberg) | fortune.com | Bloomberg Terminal |
| 284 | [Victoria 3 Dev Diary #104 - Quality of Life improvements in 1.6 (official; Census Data panel, O](https://forum.paradoxplaza.com/forum/developer-diary/victoria-3-dev-diary-104-quality-of-life-improvements-in-1-6.1622790) | forum.paradoxplaza.com | Victoria 3 |
| 285 | [Victoria 3 Dev Diary #143 - Trade Rework: The World Market (official; placeholder UI admissions](https://forum.paradoxplaza.com/forum/developer-diary/victoria-3-dev-diary-143-trade-rework-the-world-market.1733205) | forum.paradoxplaza.com | Victoria 3 |
| 286 | [Victoria 3 Dev Diary #163 - The Fine Print (official; IG negotiation, Amenability, law amendmen](https://forum.paradoxplaza.com/forum/developer-diary/victoria-3-dev-diary-163-the-fine-print.1867438) | forum.paradoxplaza.com | Victoria 3 |
| 287 | [Victoria 3 Dev Diary #30 — 'User Interface Overview' (Paradox forums) — panels, buttons, three ](https://forum.paradoxplaza.com/forum/developer-diary/victoria-3-dev-diary-30-user-interface-overview.1507166) | forum.paradoxplaza.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 288 | [Victoria 3 Dev Diary #6 - Interest Groups (official; clout computation, Powerful/Influential/Ma](https://forum.paradoxplaza.com/forum/developer-diary/victoria-3-dev-diary-6-interest-groups.1481423) | forum.paradoxplaza.com | Victoria 3 |
| 289 | [Paradox forum thread for City Corner #1 (dev quotes plus player replies on UI aesthetics) — PLA](https://forum.paradoxplaza.com/forum/index.php?threads/1897715) | forum.paradoxplaza.com | Cities: Skylines 1 & 2 |
| 290 | ['Accessibility in Paradox Games' — Paradox forums](https://forum.paradoxplaza.com/forum/threads/accessibility-in-paradox-games.1280232) | forum.paradoxplaza.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 291 | [Can I see the opinion of one character for another? (Paradox forum — player experience; documen](https://forum.paradoxplaza.com/forum/threads/can-i-see-the-opinion-of-one-character-for-another.1540279) | forum.paradoxplaza.com | Crusader Kings III |
| 292 | [CK3 Dev Diary #07 — Characters & Portraits (Paradox forum)](https://forum.paradoxplaza.com/forum/threads/ck3-dev-diary-07-characters-portraits.1295264) | forum.paradoxplaza.com | Crusader Kings III |
| 293 | [CK3 Dev Diary #16 — 'Tutorials and Tooltips and Encyclopedias, Oh My!' (Paradox forums) — prima](https://forum.paradoxplaza.com/forum/threads/ck3-dev-diary-16-tutorials-and-tooltips-and-encyclopedias-oh-my.1345581) | forum.paradoxplaza.com | Crusader Kings III; Paradox Interactive's nested tooltip and modifier-breakdown  |
| 294 | [CK3 Feature Request: Find Character Filter and Sort (Paradox forum — player experience)](https://forum.paradoxplaza.com/forum/threads/ck3-feature-request-find-character-filter-and-sort.1450955) | forum.paradoxplaza.com | Crusader Kings III |
| 295 | [CKIII Dev Diary #25 — Map Features and Map Modes (Paradox forum)](https://forum.paradoxplaza.com/forum/threads/ckiii-dev-diary-25-map-features-and-map-modes.1388210) | forum.paradoxplaza.com | Crusader Kings III |
| 296 | ['Locking a tooltip should prevent other tooltips from opening for a brief moment' — Paradox for](https://forum.paradoxplaza.com/forum/threads/locking-a-tooltip-should-prevent-other-tooltips-from-opening-for-a-brief-moment.1554097) | forum.paradoxplaza.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 297 | ['[MOD] Accessibility - Army Watch' — Paradox forums; screen-reader gaps, OCR dependence, 'outpu](https://forum.paradoxplaza.com/forum/threads/mod-accessibility-army-watch.1421626) | forum.paradoxplaza.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 298 | ['Nested tooltips are nice, but...' — Paradox forums (Europa Universalis V); null-hop layers and](https://forum.paradoxplaza.com/forum/threads/nested-tooltips-are-nice-but.1869808) | forum.paradoxplaza.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 299 | ['Reminder to the devs that nested tooltips is bad UX design' — Paradox forums (Victoria 3); inc](https://forum.paradoxplaza.com/forum/threads/reminder-to-the-devs-that-nested-tooltips-is-bad-ux-design.1702017) | forum.paradoxplaza.com | Crusader Kings III; Paradox Interactive's nested tooltip and modifier-breakdown  |
| 300 | ['Request: implementing accessibility features for the visually impaired?' — Paradox forums](https://forum.paradoxplaza.com/forum/threads/request-implementing-accessibility-features-for-the-visually-impaired.1402061) | forum.paradoxplaza.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 301 | ['Suggestions for how to improve the UI/UX design from previous Paradox games (screenshot heavy)](https://forum.paradoxplaza.com/forum/threads/suggestions-for-how-to-improve-the-ui-ux-design-from-previous-paradox-games-screenshot-heavy.1626069) | forum.paradoxplaza.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 302 | [Paradox forum - 'The Fundamentally Broken Economics of Victoria 3' (PLAYER OPINION; invisible c](https://forum.paradoxplaza.com/forum/threads/the-fundamentally-broken-economics-of-victoria-3.1733170) | forum.paradoxplaza.com | Victoria 3 |
| 303 | [Paradox forum - 'User Inter-fiasco: Victoria III's Abysmal UI' (PLAYER/CRITIC OPINION; action-t](https://forum.paradoxplaza.com/forum/threads/user-inter-fiasco-victoria-iiis-abysmal-ui.1561896) | forum.paradoxplaza.com | Victoria 3 |
| 304 | [Shadow Empire Developer Logs — index thread (Matrix Games forums)](https://forums.matrixgames.com/viewtopic.php?p=4638324) | forums.matrixgames.com | Shadow Empire |
| 305 | [Matrix Games forums — 'Enjoying Shadow Empire While Totally Blind' (accessibility thread)](https://forums.matrixgames.com/viewtopic.php?t=351069) | forums.matrixgames.com | Shadow Empire |
| 306 | [Matrix Games forums — 'What Regime Profiles and Combinations to go for?' (regime profile suppre](https://forums.matrixgames.com/viewtopic.php?t=353267) | forums.matrixgames.com | Shadow Empire |
| 307 | [Matrix Games official forums: '[Q] Unknown contact identification methods' (community thread; I](https://forums.matrixgames.com/viewtopic.php?t=408111) | forums.matrixgames.com | Command: Modern Operations |
| 308 | [Positech Forums — [1.128a] various UI element bugs [returned HTTP 403; not usable as evidence]](https://forums.positech.co.uk/t/1-128a-various-ui-element-bugs/16387) | forums.positech.co.uk | Democracy 4 |
| 309 | [Positech Forums — Building a Neural Network on top of Democracy 4's simulation [forum returned ](https://forums.positech.co.uk/t/building-a-neural-network-on-top-of-democracy-4s-simulation/16784) | forums.positech.co.uk | Democracy 4 |
| 310 | [Council — Frostpunk 2 Wiki (Game Vault) [community wiki; primary mechanical source for delegate](https://frostpunk-2.game-vault.net/wiki/Council) | frostpunk-2.game-vault.net | Frostpunk |
| 311 | [Factions — Frostpunk 2 Wiki (Game Vault) [Faction vs Community distinction, rosters, relations ](https://frostpunk-2.game-vault.net/wiki/Factions) | frostpunk-2.game-vault.net | Frostpunk |
| 312 | [Laws — Frostpunk 2 Wiki (Game Vault) [four categories, law card contents, synergy/contradiction](https://frostpunk-2.game-vault.net/wiki/Laws) | frostpunk-2.game-vault.net | Frostpunk |
| 313 | [Steward — Frostpunk 2 Wiki (Game Vault) [fetched but thin; only confirms pressure-lowers-trust]](https://frostpunk-2.game-vault.net/wiki/Steward) | frostpunk-2.game-vault.net | Frostpunk |
| 314 | [Tension — Frostpunk 2 Wiki (Game Vault) [orb display, road recolouring, UI-occluding top tier, ](https://frostpunk-2.game-vault.net/wiki/Tension) | frostpunk-2.game-vault.net | Frostpunk |
| 315 | [Trust — Frostpunk 2 Wiki (Game Vault) [0–100 scale, five named tiers, raise/lower lists, Despis](https://frostpunk-2.game-vault.net/wiki/Trust) | frostpunk-2.game-vault.net | Frostpunk |
| 316 | [Book of Laws — Official Frostpunk Wiki (Fandom) [ATTEMPTED, returned HTTP 402; NOT used as evid](https://frostpunk.fandom.com/wiki/Book_of_Laws) | frostpunk.fandom.com | Frostpunk |
| 317 | [Book of laws — Frostpunk Wiki (Game Vault) [Adaptation vs Purpose split, branching tree, irreve](https://frostpunk.game-vault.net/wiki/Book_of_laws) | frostpunk.game-vault.net | Frostpunk |
| 318 | [Shadow Empire full manual (EBOOK PDF, Matrix Games FTP) — referenced, exceeded fetch size limit](https://ftp.matrixgames.com/pub/ShadowEmpire/Shadow%20Empire%20manual%20EBOOK.pdf) | ftp.matrixgames.com | Shadow Empire |
| 319 | [Shadow Empire official changelog / Read Me — whatsnew.pdf, v1.32.264, 28 May 2026 (Matrix Games](https://ftp.matrixgames.com/pub/ShadowEmpire/whatsnew.pdf) | ftp.matrixgames.com | Shadow Empire |
| 320 | [Gabriel Chauri — Disco Elysium RPG System Analysis (skill voices in conflict, passive-check cho](https://www.gabrielchauri.com/disco-elysium-rpg-system-analysis) | gabrielchauri.com | Disco Elysium |
| 321 | [Game Accessibility Guidelines — Full List](https://gameaccessibilityguidelines.com/full-list) | gameaccessibilityguidelines.com | Accessibility for MERIDIAN's dark, dense, colour-coded comma; Onboarding and learnability for very deep simula |
| 322 | [Gamecritics review, Mitch Zehe (CRITIC OPINION; 'serious detective work' on blocked actions, po](https://gamecritics.com/mitch-zehe/victoria-3-review) | gamecritics.com | Victoria 3 |
| 323 | [Gamecritics review by Ryan Nalley (fetched in full — UI friction, no hint system, fizzled cases](https://gamecritics.com/ryan-nalley/shadows-of-doubt-review) | gamecritics.com | Shadows of Doubt |
| 324 | [Game Developer — How Citizen Sleeper was inspired by tabletop RPGs and gig work (identified as ](https://www.gamedeveloper.com/business/how-citizen-sleeper-was-inspired-by-tabletop-rpgs-and-gig-work) | gamedeveloper.com | Disco Elysium |
| 325 | [Believing is seeing: Orwell and surveillance sims (Game Developer)](https://www.gamedeveloper.com/design/believing-is-seeing-i-orwell-i-and-surveillance-sims) | gamedeveloper.com | Evidence, deduction and document-verification interfaces |
| 326 | [Pursuing the "Aha!" moment with deductive reasoning game The Case of the Golden Idol (Game Deve](https://www.gamedeveloper.com/design/case-of-the-golden-idol) | gamedeveloper.com | Evidence, deduction and document-verification interfaces |
| 327 | [Deep Dive: Modeling the global economy in Victoria 3 - Mikael Andersson, Lead Designer (develop](https://www.gamedeveloper.com/design/deep-dive-modeling-the-global-economy-in-victoria-3) | gamedeveloper.com | Victoria 3 |
| 328 | [Game Design Deep Dive: Decisions that matter in Orwell (Osmotic Studios, Game Developer)](https://www.gamedeveloper.com/design/game-design-deep-dive-decisions-that-matter-in-i-orwell-i-) | gamedeveloper.com | Evidence, deduction and document-verification interfaces |
| 329 | [How RimWorld fleshes out the Dwarf Fortress formula — Game Developer (Tynan Sylvester quotes on](https://www.gamedeveloper.com/design/how-i-rimworld-i-fleshes-out-the-i-dwarf-fortress-i-formula) | gamedeveloper.com | RimWorld |
| 330 | [Game Developer — Pentiment director explains how going all-in on fonts helped elevate the medie](https://www.gamedeveloper.com/design/pentiment-director-explains-how-going-all-in-on-fonts-helped-elevate-the-medieval-detective-rpg-) | gamedeveloper.com | Disco Elysium |
| 331 | [Ernest Adams — The Designer's Notebook: Eight Ways To Make a Bad Tutorial (Game Developer)](https://www.gamedeveloper.com/design/the-designer-s-notebook-eight-ways-to-make-a-bad-tutorial) | gamedeveloper.com | Onboarding and learnability for very deep simulations — evid |
| 332 | [Video: How RimWorld found success through ridiculous, contrarian design — Game Developer](https://www.gamedeveloper.com/design/video-how-i-rimworld-i-found-success-through-ridiculous-contrarian-design) | gamedeveloper.com | RimWorld |
| 333 | [How Tarn Adams upgraded and optimized Dwarf Fortress for its official Steam release — Game Deve](https://www.gamedeveloper.com/programming/how-tarn-adams-upgraded-and-optimized-dwarf-fortress-for-its-official-steam-release) | gamedeveloper.com | Dwarf Fortress |
| 334 | [gameplay.tips mirror — Democracy 4 Basic Gameplay Guide [returned HTTP 403; content reached onl](https://gameplay.tips/guides/8590-democracy-4.html) | gameplay.tips | Democracy 4 |
| 335 | [Crusader Kings 3: Interface Guide — gamepressure.com (third-party guide, 2020-era build)](https://www.gamepressure.com/crusader-kings-3/interface-description/z2f0f6) | gamepressure.com | Crusader Kings III |
| 336 | [Crusader Kings 3: Map modes — gamepressure.com (third-party guide)](https://www.gamepressure.com/crusader-kings-3/map-modes/z3f0f7) | gamepressure.com | Crusader Kings III |
| 337 | [Gamepressure — Disco Elysium: Skill checks (probability box on hover, white/red retry rules, 2d](https://www.gamepressure.com/disco-elysium/skill-tests/zfe3e2) | gamepressure.com | Disco Elysium |
| 338 | [Frostpunk 2: Tips for the Council — gamepressure.com [Council entry point in lower-left, four l](https://www.gamepressure.com/frostpunk-2/council/zf115fb) | gamepressure.com | Frostpunk |
| 339 | [GamePretty mirror — Democracy 4 Basic Gameplay Guide [fetched; source of left-rail voter groups](https://gamepretty.com/democracy-4-basic-gameplay-guide) | gamepretty.com | Democracy 4 |
| 340 | [Dwarf Fortress Interview: The Ever-Changing World of Dwarf Fortress Continues to Evolve After R](https://gamerant.com/dwarf-fortress-interview-evolution-after-release) | gamerant.com | Dwarf Fortress |
| 341 | [Football Manager 26 Review - Back To The Drawing Board — GameSpot (SEARCH SNIPPET ONLY — 403; i](https://www.gamespot.com/reviews/football-manager-26-review-back-to-the-drawing-board/1900-6418437) | gamespot.com | Football Manager |
| 342 | [Crusader Kings 3's New Player Experience Is a Vast Improvement — GameWatcher (hands-on; tooltip](https://www.gamewatcher.com/news/crusader-kings-3-tutorials-highlighted-text-encyclopedia) | gamewatcher.com | Crusader Kings III |
| 343 | [GameWatcher — Democracy 4 PC Review (hover/arrow system praise, arrow speed = intensity) [fetch](https://www.gamewatcher.com/reviews/democracy-4-review/13223) | gamewatcher.com | Democracy 4 |
| 344 | [Frostpunk 2 PC Review — GameWatcher [CRITIC: encyclopedia-style non-interactive tutorial; UI cl](https://www.gamewatcher.com/reviews/frostpunk-2-review/13431) | gamewatcher.com | Frostpunk |
| 345 | [GDC Vault session page — 'RimWorld': Contrarian, Ridiculous, and Impossible Game Design Methods](https://www.gdcvault.com/play/1024232/-RimWorld-Contrarian-Ridiculous-and) | gdcvault.com | RimWorld |
| 346 | [OWASP Top 10 for LLM Applications — LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection) | genai.owasp.org | Natural-language command and action-confirmation interfaces  |
| 347 | [Geo-Political Simulator 5 — official new-features page (complete interface redesign, generalize](https://www.geo-political-simulator-5.com/new_features.php?langue=en) | geo-political-simulator-5.com | Power & Revolution / Geopolitical Simulator 4 |
| 348 | [Revolutionizing UI Design in Football Manager: A Deep Dive into Unity & UI Toolkit — summary of](https://gist.ly/youtube-summarizer/revolutionizing-ui-design-in-football-manager-a-deep-dive-into-unity-ur-toolkit) | gist.ly | Football Manager |
| 349 | [Git — git-bisect documentation](https://git-scm.com/docs/git-bisect) | git-scm.com | Causal explanation interfaces for MERIDIAN — "why did this c |
| 350 | [APCA — Easy Intro (Lc threshold levels and font pairings)](https://git.apcacontrast.com/documentation/APCAeasyIntro.html) | git.apcacontrast.com | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 351 | [APCA — Why APCA (rationale and criticism of WCAG 2.x contrast math)](https://git.apcacontrast.com/documentation/WhyAPCA.html) | git.apcacontrast.com | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 352 | [Ludeon Studios official GitHub organisation (source of the shipped string tables used throughou](https://github.com/Ludeon) | github.com | RimWorld |
| 353 | [Ludeon official translation repo — RimWorld-fr (repository structure: Core/Royalty/Ideology/Bio](https://github.com/Ludeon/RimWorld-fr) | github.com | RimWorld |
| 354 | [Core/DefInjected/ThoughtDef/ — directory listing confirming the Memory vs Situation thought arc](https://github.com/Ludeon/RimWorld-fr/tree/master/Core/DefInjected/ThoughtDef) | github.com | RimWorld |
| 355 | [tutorial-gui-of-golden-idol (YuriSizov, GitHub) — Godot reverse-engineering of the thinking-boa](https://github.com/YuriSizov/tutorial-gui-of-golden-idol/blob/main/TUTORIAL.md) | github.com | Evidence, deduction and document-verification interfaces |
| 356 | [Zylleon/ExtraAlerts (GitHub) — mod adding alerts absent from the base game (repo confirmed; REA](https://github.com/Zylleon/ExtraAlerts) | github.com | RimWorld |
| 357 | [cosmos.gl / Cosmograph — GPU force-graph engine](https://github.com/cosmograph-org/cosmos) | github.com | Frontend technical feasibility for MERIDIAN: framework, pack |
| 358 | [AndroidTacticalAssaultKit-CIV source repository (deptofdefense) — fetched; confirms no user gui](https://github.com/deptofdefense/AndroidTacticalAssaultKit-CIV) | github.com | Military & emergency command-and-control interfaces: ATAK/Wi |
| 359 | [uPlot — README, size and performance benchmarks](https://github.com/leeoniya/uPlot) | github.com | Frontend technical feasibility for MERIDIAN: framework, pack |
| 360 | [Melt UI — headless component builders for Svelte](https://github.com/melt-ui/melt-ui) | github.com | Frontend technical feasibility for MERIDIAN: framework, pack |
| 361 | [Redux DevTools — repository (action list, skip/toggle actions, state diff, action replay, persi](https://github.com/reduxjs/redux-devtools) | github.com | Time, pause, replay, branching and counterfactual presentati |
| 362 | [GitUp — product site (vendor marketing; live graph, snapshots as Time-Machine-like history, cmd](https://gitup.co) | gitup.co | Time, pause, replay, branching and counterfactual presentati |
| 363 | [Suzerain release notes (all patches) — GOG Database](https://www.gogdb.org/product/1963625960/releasenotes) | gogdb.org | Suzerain |
| 364 | [Explaining uncertainty in UK intelligence assessment (GOV.UK) — the PHIA probability yardstick ](https://www.gov.uk/government/publications/explaining-uncertainty-in-uk-intelligence-assessment/explaining-uncertainty-in-uk-intelligence-assessment) | gov.uk | Intelligence-analysis tradecraft standards for expressing un |
| 365 | [Group alert notifications (Grafana Alerting docs) — Group by defaults, Group wait 30s, Group in](https://grafana.com/docs/grafana/latest/alerting/fundamentals/notifications/group-alert-notifications) | grafana.com | Security operations, observability and incident-response con |
| 366 | [Correll & Gleicher, Error Bars Considered Harmful: Exploring Alternate Encodings for Mean and E](https://graphics.cs.wisc.edu/Papers/2014/CG14) | graphics.cs.wisc.edu | Uncertainty visualisation research and its practical encodin |
| 367 | [Launchpad — Bloomberg Help Guide, Penn Libraries](https://guides.library.upenn.edu/bloomberg/launchpad) | guides.library.upenn.edu | Bloomberg Terminal |
| 368 | [Getting Started with Bloomberg at Yale: Basics — Yale University Library](https://guides.library.yale.edu/Bloomberg_Basics) | guides.library.yale.edu | Bloomberg Terminal |
| 369 | [Scout Reports / Football Manager 2022 Guide — guidetofm.com (SEARCH SNIPPET ONLY — 403; Pros/Co](https://www.guidetofm.com/squad/scout-reports) | guidetofm.com | Football Manager |
| 370 | [Uber H3 — Tiling the world / hexagon aggregation rationale](https://h3geo.org/docs/highlights/aggregation) | h3geo.org | Map and layer design for multi-domain data — cartographic ba |
| 371 | [Uber H3 — Indexing: approximate hierarchical containment caveat](https://h3geo.org/docs/highlights/indexing) | h3geo.org | Map and layer design for multi-domain data — cartographic ba |
| 372 | [Ghoniem, Fekete & Castagliola — A Comparison of the Readability of Graphs Using Node-Link and M](https://hal.science/hal-00343819v1) | hal.science | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 373 | [FAA Human Factors Design Standard HF-STD-001B landing page — confirms existence and scope; deta](https://hf.tc.faa.gov/hfds) | hf.tc.faa.gov | Safety-critical control-room interface design canon |
| 374 | [Hearts of Iron IV Wiki — Battle plan (drawing tools, execute button, planning bonus, naval inva](https://hoi4.paradoxwikis.com/Battle_plan) | hoi4.paradoxwikis.com | Hearts of Iron IV |
| 375 | [Hearts of Iron IV Wiki — Division designer (panel layout, slot rules, live stats, min/max cost)](https://hoi4.paradoxwikis.com/Division_designer) | hoi4.paradoxwikis.com | Hearts of Iron IV |
| 376 | [Hearts of Iron IV Wiki — Intel (intel thresholds, ± bands, acquisition, decay, Intel Ledger)](https://hoi4.paradoxwikis.com/Intel) | hoi4.paradoxwikis.com | Hearts of Iron IV |
| 377 | [Hearts of Iron IV Wiki — Intelligence agency (agency upgrades, four intel categories, counter-i](https://hoi4.paradoxwikis.com/Intelligence_agency) | hoi4.paradoxwikis.com | Hearts of Iron IV |
| 378 | [Hearts of Iron IV Wiki — Interface (top bar contents, menu hotkeys, left national panel)](https://hoi4.paradoxwikis.com/Interface) | hoi4.paradoxwikis.com | Hearts of Iron IV |
| 379 | [Hearts of Iron IV Wiki — Logistics (supply map-mode colour ramp, hub/rail numbers, diagnostic t](https://hoi4.paradoxwikis.com/Logistics) | hoi4.paradoxwikis.com | Hearts of Iron IV |
| 380 | [Hearts of Iron IV Wiki — Map (full map-mode list and colour semantics)](https://hoi4.paradoxwikis.com/Map) | hoi4.paradoxwikis.com | Hearts of Iron IV |
| 381 | [Hearts of Iron IV Wiki — National focus (AND/OR line grammar, 70-day/70-PP identity, hover prev](https://hoi4.paradoxwikis.com/National_focus) | hoi4.paradoxwikis.com | Hearts of Iron IV |
| 382 | [Hearts of Iron IV Wiki — Production (production lines, efficiency, resource shortage indicators](https://hoi4.paradoxwikis.com/Production) | hoi4.paradoxwikis.com | Hearts of Iron IV |
| 383 | [User interface — Hearts of Iron 4 Wiki (top bar contents, Q/W/E/R... menu hotkeys, alert tabs, ](https://hoi4.paradoxwikis.com/User_interface) | hoi4.paradoxwikis.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 384 | [How To Make An RPG — Case study: Citizen Sleeper (dice pool at top-centre, drag-into-slot besid](https://howtomakeanrpg.com/r/a/case-study-citizen-sleeper.html) | howtomakeanrpg.com | Disco Elysium |
| 385 | [HSE COMAH case study — Texaco Refinery, Milford Haven, 24 July 1994](https://www.hse.gov.uk/comah/sragtech/casetexaco94.htm) | hse.gov.uk | Safety-critical control-room interface design canon |
| 386 | [HSE COMAH technical measures — Alarms (pointer page; confirmed HSE's alarm guidance lineage, co](https://www.hse.gov.uk/comah/sragtech/techmeasalarm.htm) | hse.gov.uk | Alerts, attention and time pressure: an evidence base and co |
| 387 | [HSE Information Sheet, Chemicals Sheet No 6 — 'Better alarm handling' (CHIS6, 3/00) — PRIMARY; ](https://www.hse.gov.uk/pubns/chis6.pdf) | hse.gov.uk | Alerts, attention and time pressure: an evidence base and co; Progressive disclosure and information density i |
| 388 | [Mark, G., Gudith, D. & Klocke, U. — The Cost of Interrupted Work: More Speed and Stress (CHI 20](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) | ics.uci.edu | Alerts, attention and time pressure: an evidence base and co |
| 389 | [Correll, Moritz & Heer, Value-Suppressing Uncertainty Palettes, ACM CHI 2018](https://idl.uw.edu/papers/uncertainty-palettes) | idl.uw.edu | Uncertainty visualisation research and its practical encodin |
| 390 | [Archambault, Purchase & Pinaud — Animation, Small Multiples, and the Effect of Mental Map Prese](https://ieeexplore.ieee.org/document/5473226) | ieeexplore.ieee.org | Relationship graph visualisation at scale — node-link vs mat |
| 391 | [Song & Szafir — Where's My Data? Evaluating Visualizations with Missing Data (IEEE TVCG / InfoV](https://ieeexplore.ieee.org/document/8807226) | ieeexplore.ieee.org | Relationship graph visualisation at scale — node-link vs mat |
| 392 | [ICD 203, Analytic Standards (Intelligence Community Directive, effective 2 January 2015) — full](https://www.intelligence.gov/assets/documents/intelligence-community-directives/ICD_203.pdf) | intelligence.gov | Intelligence-analysis tradecraft standards for expressing un |
| 393 | [ICD 206, Sourcing Requirements for Disseminated Analytic Products — source descriptors, source ](https://www.intelligence.gov/assets/documents/intelligence-community-directives/ICD_206.pdf) | intelligence.gov | Intelligence-analysis tradecraft standards for expressing un |
| 394 | [Interactive Pasts — Old World review (counter-view: UI 'intuitive', tooltip freezing praised, u](https://interactivepasts.com/old-world-review) | interactivepasts.com | Old World |
| 395 | [Confirmation in The Return of Obra Dinn (Intermittent Mechanism, 2024) — critique of the rule o](https://intermittentmechanism.blog/2024/05/21/confirmation-in-the-return-of-obra-dinn) | intermittentmechanism.blog | Evidence, deduction and document-verification interfaces |
| 396 | [IPCC AR6 WG1 Chapter 1 — calibrated language, evidence x agreement framework](https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-1) | ipcc.ch | Uncertainty visualisation research and its practical encodin |
| 397 | [IPCC AR5 Guidance Note for Lead Authors on Consistent Treatment of Uncertainties (Mastrandrea e](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf) | ipcc.ch | Uncertainty visualisation research and its practical encodin |
| 398 | [FAS Intelligence Resource Program: index of Intelligence Community Directives (used to confirm ](https://irp.fas.org/dni/icd) | irp.fas.org | Intelligence-analysis tradecraft standards for expressing un |
| 399 | [ISA — ISA101 standards committee page (scope: graphics and colour conventions, alarming convent](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa101) | isa.org | Safety-critical control-room interface design canon |
| 400 | [Terminal Bloomberg — Performing analysis (EQS, DES, YA; colour/affordance conventions) — ISEG L](https://iseg.libguides.com/c.php?g=706923&p=5094209) | iseg.libguides.com | Bloomberg Terminal |
| 401 | [Terra Invicta: How to Adapt Excel for a War over the Solar System — ixbt.games (fetched in full](https://ixbt.games/en/reviews/2026/02/01/terra-invicta-kak-prisposobit-excel-dlia-voiny-za-solnecnuiu-sistemu.html) | ixbt.games | Terra Invicta |
| 402 | [Bloomberg Guide: Color Scheme Options (PDFU COLORS, deuteranopia/protanomaly, coverage limits) ](https://johncabot.libguides.com/bloomberg/color-scheme) | johncabot.libguides.com | Bloomberg Terminal |
| 403 | [FETCH FAILED (HTTP 403) — Joint Commission Sentinel Event Alert 50, Medical device alarm safety](https://www.jointcommission.org/-/media/tjc/documents/resources/patient-safety-topics/sentinel-event/sea_50_alarms_4_5_13_final1.pdf) | jointcommission.org | Alerts, attention and time pressure: an evidence base and co |
| 404 | [Drew, B. J. et al. — Insights into the Problem of Alarm Fatigue with Physiologic Monitor Device](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0110274) | journals.plos.org | Alerts, attention and time pressure: an evidence base and co |
| 405 | [Hullman, Resnick & Adar, Hypothetical Outcome Plots Outperform Error Bars and Violin Plots for ](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0142444) | journals.plos.org | Time, pause, replay, branching and counterfactual presentati; Uncertainty visualisation research and its pract |
| 406 | [Ghoniem et al. — journal version record (Information Visualization / SAGE)](https://journals.sagepub.com/doi/10.1057/palgrave.ivs.9500092) | journals.sagepub.com | Relationship graph visualisation at scale — node-link vs mat |
| 407 | [Smallman & St. John (2005), 'Naive Realism: Misplaced Faith in Realistic Displays', Ergonomics ](https://journals.sagepub.com/doi/10.1177/106480460501300303) | journals.sagepub.com | Military & emergency command-and-control interfaces: ATAK/Wi |
| 408 | [St. John, Smallman, Manes, Feher & Morrison (2005), 'Heuristic Automation for Decluttering Tact](https://journals.sagepub.com/doi/10.1518/001872005774860014) | journals.sagepub.com | Military & emergency command-and-control interfaces: ATAK/Wi |
| 409 | [St. John & Smallman (2008), 'Staying Up to Speed: Four Design Principles for Maintaining and Re](https://journals.sagepub.com/doi/abs/10.1518/155534308X284408) | journals.sagepub.com | Military & emergency command-and-control interfaces: ATAK/Wi |
| 410 | [Cytoscape.js — documentation](https://js.cytoscape.org) | js.cytoscape.org | Frontend technical feasibility for MERIDIAN: framework, pack |
| 411 | [The Implied Truth Effect (Pennycook, Bear, Collins & Rand, Management Science)](https://www.jstor.org/stable/48814593) | jstor.org | Provenance and fact-versus-narration separation in an interf |
| 412 | [Khemitron Industries — 'Quality of Life Improvements: Nested Tooltips' (NOT FETCHABLE: HTTP 403](https://khemitron-industries.net/quality-of-life-improvements-nested-tooltips) | khemitron-industries.net | Old World |
| 413 | [Language at Play — The Talking Scripts of Obsidian's Pentiment (font reflects Andreas's opinion](https://languageatplay.de/2023/01/09/the-talking-scripts-of-obsidians-pentiment) | languageatplay.de | Disco Elysium |
| 414 | [Leaflet — Layer Groups and Layers Control (base layers vs overlays; radio vs checkbox)](https://leafletjs.com/examples/layers-control) | leafletjs.com | Map and layer design for multi-domain data — cartographic ba |
| 415 | [Entity pages in Microsoft Sentinel (Microsoft Learn) — three-panel entity page, timeline item t](https://learn.microsoft.com/en-us/azure/sentinel/entity-pages) | learn.microsoft.com | Security operations, observability and incident-response con |
| 416 | [Basic incident tasks for Microsoft Sentinel incidents in the Azure portal (Microsoft Learn) — i](https://learn.microsoft.com/en-us/azure/sentinel/incident-navigate-triage) | learn.microsoft.com | Security operations, observability and incident-response con |
| 417 | [Investigate Microsoft Sentinel incidents in depth in the Azure portal (Microsoft Learn) — incid](https://learn.microsoft.com/en-us/azure/sentinel/investigate-incidents) | learn.microsoft.com | Security operations, observability and incident-response con |
| 418 | [Application card — Microsoft Security Copilot (Microsoft Learn) — Limitations section, overreli](https://learn.microsoft.com/en-us/copilot/security/security-copilot-application-card) | learn.microsoft.com | Security operations, observability and incident-response con |
| 419 | [Summarize incidents with Microsoft Copilot in Microsoft Defender (Microsoft Learn) — incident s](https://learn.microsoft.com/en-us/defender-xdr/security-copilot-m365d-incident-summary) | learn.microsoft.com | Security operations, observability and incident-response con |
| 420 | [Microsoft Learn — Xbox Accessibility Guideline 107 (input mechanisms of choice)](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/107) | learn.microsoft.com | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 421 | [Bloomberg for beginners: Display and navigation — Imperial College London Library Guides](https://library-guides.imperial.ac.uk/bloomberg/display-and-navigation) | library-guides.imperial.ac.uk | Bloomberg Terminal |
| 422 | [Bloomberg for beginners: Getting started — Imperial College London Library Guides](https://library-guides.imperial.ac.uk/bloomberg/getting-started) | library-guides.imperial.ac.uk | Bloomberg Terminal |
| 423 | [Archambault & Purchase — Mental Map Preservation Helps User Orientation in Dynamic Graphs (Grap](https://link.springer.com/chapter/10.1007/978-3-642-36763-2_42) | link.springer.com | Relationship graph visualisation at scale — node-link vs mat |
| 424 | [Martin Brueckner, 'I Have Been Testing Bloomberg's New AI Tool ASKB; My Take', LinkedIn (PRACTI](https://www.linkedin.com/pulse/i-have-been-testing-bloombergs-new-ai-tool-askb-my-take-brueckner-sluwf) | linkedin.com | Bloomberg Terminal |
| 425 | [Bloomberg Launchpad Part One: Basics — Lippincott Library blog (Monitor / Component / View / Gr](https://lippincottlibrary.wordpress.com/2013/03/11/bloomberg-launchpad-part-one) | lippincottlibrary.wordpress.com | Bloomberg Terminal |
| 426 | [Magic Game World — Shadow Empire hotkeys / keyboard shortcuts reference (map layer hotkeys 1-6)](https://www.magicgameworld.com/shadow-empire-hotkeys-keyboard-shortcuts) | magicgameworld.com | Shadow Empire |
| 427 | [map.army symbol gallery documentation (MIL-STD-2525C baseline; hierarchical symbol tree plus se](https://www.map.army/doc/en/symbols/symbol-gallery) | map.army | Military & emergency command-and-control interfaces: ATAK/Wi |
| 428 | [MapLibre Style Spec — overview](https://maplibre.org/maplibre-style-spec) | maplibre.org | Frontend technical feasibility for MERIDIAN: framework, pack |
| 429 | [MapLibre Style Spec — Sources](https://maplibre.org/maplibre-style-spec/sources) | maplibre.org | Frontend technical feasibility for MERIDIAN: framework, pack |
| 430 | [MIL-STD-2525D, Department of Defense Interface Standard: Joint Military Symbology (full 885-pag](http://www.mapsymbs.com/MilStd2525D.pdf) | mapsymbs.com | Military & emergency command-and-control interfaces: ATAK/Wi |
| 431 | [Martin Fowler — Event Sourcing (Complete Rebuild, Temporal Query, Event Replay; external update](https://martinfowler.com/eaaDev/EventSourcing.html) | martinfowler.com | Time, pause, replay, branching and counterfactual presentati |
| 432 | [Martin Fowler — Parallel Model (hypothetical state, Parallel System vs embedded models, object ](https://martinfowler.com/eaaDev/ParallelModel.html) | martinfowler.com | Time, pause, replay, branching and counterfactual presentati |
| 433 | [Martin Fowler — Retroactive Event (branch point, rebuild vs rewind/replay, external-system warn](https://martinfowler.com/eaaDev/RetroactiveEvent.html) | martinfowler.com | Time, pause, replay, branching and counterfactual presentati |
| 434 | [Command: Modern Operations — official game manual (PDF; fetched and text-extracted in full, ~11](https://www.matrixgames.com/amazon/PDF/CMO/CMO_manual_EBOOK.pdf) | matrixgames.com | Command: Modern Operations |
| 435 | [Matrix Games forums — Stratagem generation rules](https://www.matrixgames.com/forums/viewtopic.php?t=364617) | matrixgames.com | Shadow Empire |
| 436 | [Matrix Games — Command: Modern Operations (doctrine and rules of engagement, crew proficiency, ](https://www.matrixgames.com/game/command-modern-operations) | matrixgames.com | Hearts of Iron IV |
| 437 | [Matrix Games — Flashpoint Campaigns: Southern Storm (asynchronous variable-length WEGO, SOPs, h](https://www.matrixgames.com/game/flashpoint-campaigns-southern-storm) | matrixgames.com | Hearts of Iron IV |
| 438 | [Shadow Empire Developer Log #4: Leaders and Factions (Matrix Games news)](https://www.matrixgames.com/news/shadow-empire-developer-log-4-leaders-and-factions) | matrixgames.com | Shadow Empire |
| 439 | [Matrix Games — Shadow Empire 'Morale & Makeover' update announcement](https://www.matrixgames.com/news/shadow-empire-morale-and-makeover-update) | matrixgames.com | Shadow Empire |
| 440 | [RimWorld: Contrarian, Ridiculous, and Impossible Game Design Methods — Tynan Sylvester, GDC 201](https://media.gdcvault.com/gdc2017/Presentations/Sylvester_Tynan_RimWorld_Contrarian_Ridiculous.pdf) | media.gdcvault.com | RimWorld |
| 441 | [When a Game You've Played for 15 Years Suddenly Feels Foreign — UX designer's analysis, Bootcam](https://medium.com/design-bootcamp/when-a-game-youve-played-for-15-years-suddenly-feels-foreign-fa779d1b9d2d) | medium.com | Football Manager |
| 442 | [Dwarf Fortress: 2 Months Later — Kitfox Games post-mortem, Medium (fetched in full)](https://medium.com/kitfox-games-shenanigans/dwarf-fortress-2-months-later-648d1c4f34d2) | medium.com | Dwarf Fortress |
| 443 | [Power & Revolution — Metacritic (SpazioGames 60 'awkward interface'; 4P.de 51 'interface is pla](https://www.metacritic.com/game/power-and-revolution) | metacritic.com | Power & Revolution / Geopolitical Simulator 4 |
| 444 | [Terra Invicta user reviews — Metacritic (fetched; verbatim user quotes on tutorial and UI/UX wi](https://www.metacritic.com/game/terra-invicta/user-reviews) | metacritic.com | Terra Invicta |
| 445 | [Microsoft HAX Toolkit — Guidelines for Human-AI Interaction (landing page)](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines) | microsoft.com | Causal explanation interfaces for MERIDIAN — "why did this c |
| 446 | [Microsoft HAX Toolkit — Guideline 11: Make clear why the system did what it did](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-why-the-system-did-what-it-did) | microsoft.com | Causal explanation interfaces for MERIDIAN — "why did this c |
| 447 | [Guidelines for Human-AI Interaction — HAX Design Library (Microsoft)](https://www.microsoft.com/en-us/haxtoolkit/library) | microsoft.com | Natural-language command and action-confirmation interfaces ; Provenance and fact-versus-narration separation  |
| 448 | [Kaur et al. — Interpreting Interpretability: Understanding Data Scientists' Use of Interpretabi](https://www.microsoft.com/en-us/research/publication/interpreting-interpretability-understanding-data-scientists-use-of-interpretability-tools-for-machine-learning) | microsoft.com | Causal explanation interfaces for MERIDIAN — "why did this c |
| 449 | [Mittelalter (hypotheses.org) — Interview and Q&A with Josh Sawyer, Game Director of Pentiment (](https://mittelalter.hypotheses.org/31324) | mittelalter.hypotheses.org | Disco Elysium |
| 450 | [ggdist documentation (Matthew Kay) — slab+interval, dots+interval/quantile dotplots, lineribbon](https://mjskay.github.io/ggdist) | mjskay.github.io | Uncertainty visualisation research and its practical encodin |
| 451 | [Mohawk Games — Old World Update #100 patch notes (opinion triangle on portrait, family tree hig](https://mohawkgames.com/2022/11/10/old-world-update-100) | mohawkgames.com | Old World |
| 452 | [Mohawk Games — Old World Update #120 patch notes (portrait interpolation/ageing, F1 context enc](https://mohawkgames.com/2024/03/06/old-world-update-120) | mohawkgames.com | Old World |
| 453 | [Mohawk Games — Old World Update #132 patch notes (role-contextual trait effects in character to](https://mohawkgames.com/2025/02/19/old-world-update-132) | mohawkgames.com | Old World |
| 454 | [Mohawk Games — Old World Update #141 patch notes (relatives panel shows dead characters, ambiti](https://mohawkgames.com/2025/11/26/old-world-update-141) | mohawkgames.com | Old World |
| 455 | [Mohawk Games — Old World Update #143 patch notes (trait opinion shown without advanced help tex](https://mohawkgames.com/2026/02/18/old-world-update-143) | mohawkgames.com | Old World |
| 456 | [Mohawk Games — Old World official gameplay page (Orders, families, legitimacy, ambitions, '1,00](https://mohawkgames.com/oldworld/gameplay) | mohawkgames.com | Old World |
| 457 | [Mock Service Worker — documentation](https://mswjs.io/docs) | mswjs.io | Frontend technical feasibility for MERIDIAN: framework, pack |
| 458 | [MU Collective (Hullman/Kay lab) publications index — source for In Dice We Trust (CHI 2024), Su](https://mucollective.northwestern.edu) | mucollective.northwestern.edu | Uncertainty visualisation research and its practical encodin |
| 459 | [Kale, Nguyen, Kay & Hullman, Hypothetical Outcome Plots Help Untrained Observers Judge Trends i](https://mucollective.northwestern.edu/project/hops-trends) | mucollective.northwestern.edu | Map and layer design for multi-domain data — cartographic ba; Uncertainty visualisation research and its pract |
| 460 | [Kay, Kola, Hullman & Munson, When(ish) is My Bus? User-centered Visualizations of Uncertainty i](https://mucollective.northwestern.edu/project/when-ish-is-my-bus) | mucollective.northwestern.edu | Uncertainty visualisation research and its practical encodin |
| 461 | [Neo4j Bloom User Guide — Scene interactions, and Slicer](https://neo4j.com/docs/bloom-user-guide/current/bloom-visual-tour/bloom-scene-interactions) | neo4j.com | Link-analysis and investigative graph tooling: IBM/i2 Analys |
| 462 | [City-Building in Your Hands: Adapting Frostpunk 2's Depth to a Gamepad — Xbox Wire, 18 Sep 2025](https://news.xbox.com/en-us/2025/09/18/adapting-frostpunk-2s-depth-to-a-gamepad) | news.xbox.com | Frostpunk |
| 463 | [Terra Invicta mods tagged Quality of Life — Nexus Mods (NOT FETCHED: HTTP 403; used only via se](https://www.nexusmods.com/games/terrainvicta/mods?tag=Quality+of+Life) | nexusmods.com | Terra Invicta |
| 464 | [NOAA National Hurricane Center, About the Cone of Uncertainty (definition and error-derived rad](https://www.nhc.noaa.gov/aboutcone.shtml) | nhc.noaa.gov | Uncertainty visualisation research and its practical encodin |
| 465 | [Loranger, H. — Accordions Are Not Always the Answer for Complex Content on Desktops (Nielsen No](https://www.nngroup.com/articles/accordions-complex-content) | nngroup.com | Progressive disclosure and information density in expert int |
| 466 | [Nielsen Norman Group — Executing UX Animations: Duration and Motion Characteristics](https://www.nngroup.com/articles/animation-duration) | nngroup.com | Building an original "near-future command system" visual lan |
| 467 | [Banner Blindness: Old and New Findings (Nielsen Norman Group; eyetracking 1997/2007/2018)](https://www.nngroup.com/articles/banner-blindness-old-and-new-findings) | nngroup.com | Provenance and fact-versus-narration separation in an interf |
| 468 | [Nielsen Norman Group — Confirmation dialogs guidance](https://www.nngroup.com/articles/confirmation-dialog) | nngroup.com | Natural-language command and action-confirmation interfaces  |
| 469 | [Nielsen Norman Group — Dark Mode vs. Light Mode: Which Is Better? (Budiu, 2020)](https://www.nngroup.com/articles/dark-mode) | nngroup.com | Accessibility for MERIDIAN's dark, dense, colour-coded comma; Building an original "near-future command system |
| 470 | [Nielsen Norman Group — Indicators, Validations, and Notifications: Pick the Correct Communicati](https://www.nngroup.com/articles/indicators-validations-notifications) | nngroup.com | Alerts, attention and time pressure: an evidence base and co |
| 471 | [Nielsen Norman Group — Instructional Overlays and Coach Marks for Mobile Apps](https://www.nngroup.com/articles/mobile-instructional-overlay) | nngroup.com | Onboarding and learnability for very deep simulations — evid |
| 472 | [Nielsen Norman Group — Modes in User Interfaces (PRIMARY; when modes help/hurt, mode slips, two](https://www.nngroup.com/articles/modes) | nngroup.com | Situation awareness and the command shell: SA theory, ecolog |
| 473 | [Nielsen, J. — Progressive Disclosure (Nielsen Norman Group, 2006)](https://www.nngroup.com/articles/progressive-disclosure) | nngroup.com | Building an original "near-future command system" visual lan; Causal explanation interfaces for MERIDIAN — "wh |
| 474 | [Nielsen, J. — Response Times: The 3 Important Limits (citing Miller 1968; Card, Robertson & Mac](https://www.nngroup.com/articles/response-times-3-important-limits) | nngroup.com | Progressive disclosure and information density in expert int |
| 475 | [Nielsen, J. — Short-Term Memory and Web Usability (Nielsen Norman Group, 6 Dec 2009)](https://www.nngroup.com/articles/short-term-memory-and-web-usability) | nngroup.com | Progressive disclosure and information density in expert int |
| 476 | [Nielsen Norman Group — 10 Usability Heuristics for User Interface Design (PRIMARY; visibility o](https://www.nngroup.com/articles/ten-usability-heuristics) | nngroup.com | Onboarding and learnability for very deep simulations — evid; Situation awareness and the command shell: SA th |
| 477 | [Kendrick, A. — Tooltip Guidelines (Nielsen Norman Group, 27 Jan 2019)](https://www.nngroup.com/articles/tooltip-guidelines) | nngroup.com | Progressive disclosure and information density in expert int |
| 478 | [Noisy Pixel — Democracy 4 Review (bubble grid, seven categories, filters critique, 'difficult t](https://noisypixel.net/democracy-4-review-pc) | noisypixel.net | Democracy 4 |
| 479 | [Old World Wiki (Fandom) — Opinion / Traits / Ratings (NOT FETCHABLE: HTTP 402; trait counts and](https://oldworld.fandom.com/wiki/Opinion) | oldworld.fandom.com | Old World |
| 480 | [Smallman & St. John (2010), 'Naïve Realism: Folk Fallacies in the Design and Use of Visual Disp](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1756-8765.2010.01114.x) | onlinelibrary.wiley.com | Military & emergency command-and-control interfaces: ATAK/Wi |
| 481 | [Wood, Isenberg, Isenberg, Dykes, Boukhelifa & Slingsby, Sketchy rendering for information visua](https://openaccess.city.ac.uk/id/eprint/1274) | openaccess.city.ac.uk | Uncertainty visualisation research and its practical encodin |
| 482 | [OpenTelemetry — Observability Primer (traces, spans, attributes)](https://opentelemetry.io/docs/concepts/observability-primer) | opentelemetry.io | Causal explanation interfaces for MERIDIAN — "why did this c |
| 483 | [Google PAIR, People + AI Guidebook — Errors + Graceful Failure](https://pair.withgoogle.com/chapter/errors-failing) | pair.withgoogle.com | Natural-language command and action-confirmation interfaces  |
| 484 | [Google PAIR — People + AI Guidebook, Explainability + Trust chapter](https://pair.withgoogle.com/chapter/explainability-trust) | pair.withgoogle.com | Causal explanation interfaces for MERIDIAN — "why did this c; Natural-language command and action-confirmation |
| 485 | [Google PAIR, People + AI Guidebook — Mental Models](https://pair.withgoogle.com/chapter/mental-models) | pair.withgoogle.com | Natural-language command and action-confirmation interfaces  |
| 486 | [Palantir docs — Action Types overview](https://palantir.com/docs/foundry/action-types/overview) | palantir.com | Palantir Gotham and Foundry |
| 487 | [Palantir docs — AIP overview (audit trails, explanations; citations referenced but not fetchabl](https://palantir.com/docs/foundry/aip/overview) | palantir.com | Palantir Gotham and Foundry |
| 488 | [Palantir docs — Data Lineage overview](https://palantir.com/docs/foundry/data-lineage/overview) | palantir.com | Palantir Gotham and Foundry |
| 489 | [Palantir docs — Notepad overview (embedded widgets, lock widget data)](https://palantir.com/docs/foundry/notepad/overview) | palantir.com | Palantir Gotham and Foundry |
| 490 | [Palantir docs — Object Explorer overview](https://palantir.com/docs/foundry/object-explorer/overview) | palantir.com | Palantir Gotham and Foundry |
| 491 | [Palantir docs — Object Views overview](https://palantir.com/docs/foundry/object-views/overview) | palantir.com | Palantir Gotham and Foundry |
| 492 | [Palantir docs — The Ontology (overview)](https://palantir.com/docs/foundry/ontology/overview) | palantir.com | Palantir Gotham and Foundry |
| 493 | [Palantir docs — Quiver overview (cards, graph mode, time series)](https://palantir.com/docs/foundry/quiver/overview) | palantir.com | Palantir Gotham and Foundry |
| 494 | [Palantir docs — Markings](https://palantir.com/docs/foundry/security/markings) | palantir.com | Palantir Gotham and Foundry |
| 495 | [Palantir docs — Foundry security overview (mandatory vs discretionary controls)](https://palantir.com/docs/foundry/security/overview) | palantir.com | Palantir Gotham and Foundry |
| 496 | [Palantir docs — Vertex overview (graphs, events, time selection, scenarios)](https://palantir.com/docs/foundry/vertex/overview) | palantir.com | Palantir Gotham and Foundry |
| 497 | [Palantir docs — Workshop overview (widgets, variables, object sets, scenarios)](https://palantir.com/docs/foundry/workshop/overview) | palantir.com | Palantir Gotham and Foundry |
| 498 | [Palantir docs — Gotham security overview](https://palantir.com/docs/gotham/security/overview) | palantir.com | Palantir Gotham and Foundry |
| 499 | [Colossal Order dev diary — Feature #11: Citizen Simulation & Lifepath (Lifepath Journal, Follow](https://www.paradoxinteractive.com/games/cities-skylines-ii/features/citizen-simulation-lifepath) | paradoxinteractive.com | Cities: Skylines 1 & 2 |
| 500 | [Colossal Order dev diary — City Corner #1: Upcoming Visual Updates (UI makeover; 'the UI can so](https://www.paradoxinteractive.com/games/cities-skylines-ii/news/upcoming-visual-updates) | paradoxinteractive.com | Cities: Skylines 1 & 2 |
| 501 | [Victoria 3 Dev Diary #80 - Law Enactment and Revolution Clock in 1.3 (official)](https://www.paradoxinteractive.com/games/victoria-3/news/dev-diary-80-law-enactment-and-revolution-clock-in-13) | paradoxinteractive.com | Victoria 3 |
| 502 | [Victoria 3 Dev Diary #61 - Data Visualization (official; market panel redesign, red/green remov](https://www.paradoxinteractive.com/games/victoria-3/news/victoria-3-dev-diary-61-data-visualization) | paradoxinteractive.com | Victoria 3 |
| 503 | [All you need to know about STAR RATINGS on Football Manager — Passion4FM (SEARCH SNIPPET ONLY —](https://www.passion4fm.com/football-manager-guide-star-ratings) | passion4fm.com | Football Manager |
| 504 | [Football Manager Player Attributes Explained — Passion4FM (SEARCH SNIPPET ONLY — 403; 1-20 scal](https://www.passion4fm.com/football-manager-player-attributes) | passion4fm.com | Football Manager |
| 505 | [Scouting in Football Manager 2024: The Definitive Guide — Passion4FM (SEARCH SNIPPET ONLY — HTT](https://www.passion4fm.com/scouting-in-football-manager) | passion4fm.com | Football Manager |
| 506 | [Dwarf Fortress sells 1 million copies on Steam — PC Gamer (body NOT fetched; headline figure on](https://www.pcgamer.com/games/sim/dwarf-fortress-sells-1-million-copies-on-steam-so-now-bay-12-games-can-afford-that-little-party-it-planned) | pcgamer.com | Dwarf Fortress |
| 507 | [PCGamesN — Cities Skylines 2 review ('the drop-down that shows precisely what's affecting citiz](https://www.pcgamesn.com/cities-skylines-2/review) | pcgamesn.com | Cities: Skylines 1 & 2 |
| 508 | [Dwarf Fortress compiles detailed dwarf medical records — PCGamesN (search summary only; charact](https://www.pcgamesn.com/dwarf-fortress/medical-history-character-sheet) | pcgamesn.com | Dwarf Fortress |
| 509 | [Dwarf Fortress has a much better UI on Steam — PCGamesN (fetched; new menus, tabs, scrollbars, ](https://www.pcgamesn.com/dwarf-fortress/menus) | pcgamesn.com | Dwarf Fortress |
| 510 | [Victoria 3 will use Crusader Kings 3's tooltip system — PCGamesN (confirms the CK3→Vic3 lineage](https://www.pcgamesn.com/victoria-3/nested-tooltip-system) | pcgamesn.com | Crusader Kings III; Victoria 3 |
| 511 | [Power & Revolution — PCGamingWiki](https://www.pcgamingwiki.com/wiki/Power_&_Revolution) | pcgamingwiki.com | Power & Revolution / Geopolitical Simulator 4 |
| 512 | [van Ham & Perer — 'Search, Show Context, Expand on Demand': Supporting Large Graph Exploration ](https://perer.org/papers/adamPerer-DOIGraphs-InfoVis2009.pdf) | perer.org | Relationship graph visualisation at scale — node-link vs mat |
| 513 | [Pernosco — About / Overview (precomputed program states, dataflow to sources, critique of singl](https://pernos.co/about/overview) | pernos.co | Time, pause, replay, branching and counterfactual presentati |
| 514 | [Holten, Isenberg, van Wijk & Fekete — An Extended Evaluation of the Readability of Tapered, Ani](http://petra.isenberg.cc/publications/papers/Holten_2011_AEP.pdf) | petra.isenberg.cc | Relationship graph visualisation at scale — node-link vs mat |
| 515 | [Philip Ardeljan, 'Tooltips in tooltips' — designer blog analysing CK3's pattern for web use; no](https://philip.design/blog/tooltips-in-tooltips) | philip.design | Crusader Kings III; Paradox Interactive's nested tooltip and modifier-breakdown  |
| 516 | [DayOne review — CITED BUT NOT FETCHED (HTTP 403); source of the 'nothing auto-pins / tutorial m](https://playday.one/2024/09/23/shadows-of-doubt-review) | playday.one | Shadows of Doubt |
| 517 | [Playwright — visual comparisons / toHaveScreenshot](https://playwright.dev/docs/test-snapshots) | playwright.dev | Frontend technical feasibility for MERIDIAN: framework, pack |
| 518 | [Cliffski's Blog — Democracy 4 GUI update (9 Nov 2019) [fetched]](https://www.positech.co.uk/cliffsblog/2019/11/09/democracy-4-gui-update) | positech.co.uk | Democracy 4 |
| 519 | [Cliffski's Blog — Democracy 4: new UI stuff (16 Feb 2020) [fetched; content is a video link, li](https://www.positech.co.uk/cliffsblog/2020/02/16/democracy-4-new-ui-stuff) | positech.co.uk | Democracy 4 |
| 520 | [Cliffski's Blog — Democracy 4: The fixed income rewrite (23 Jun 2020) [fetched]](https://www.positech.co.uk/cliffsblog/2020/06/23/democracy-4-the-fixed-income-rewrite) | positech.co.uk | Democracy 4 |
| 521 | [Cliffski's Blog — On the visualization of voter approval distribution in Democracy 4 (2 Mar 202](https://www.positech.co.uk/cliffsblog/2022/03/02/on-the-visualization-of-voter-approval-distribution-in-democracy-4) | positech.co.uk | Democracy 4 |
| 522 | [Cliffski's Blog — Democracy 4's overcomplexity is by design (19 Feb 2023) [fetched]](https://www.positech.co.uk/cliffsblog/2023/02/19/democracy-4s-overcomplexity-is-by-design) | positech.co.uk | Democracy 4 |
| 523 | [Cliffski's Blog — Democracy 4 category archive, page 13 (neural-network architecture, 'why is B](https://www.positech.co.uk/cliffsblog/category/democracy-4/page/13) | positech.co.uk | Democracy 4 |
| 524 | [Positech — Democracy 4 official product page (feature list incl. 'Icons resize on the main scre](https://www.positech.co.uk/democracy4) | positech.co.uk | Cities: Skylines 1 & 2; Democracy 4 |
| 525 | [Positech — Democracy 4 Modding: Policies (official; MinCost/MaxCost, Implementation turns, slid](https://www.positech.co.uk/democracy4/mod_policies.html) | positech.co.uk | Democracy 4 |
| 526 | [Positech — Democracy 4 Modding: Simulation (official data model; Zone, Emotion, inputs/outputs)](https://www.positech.co.uk/democracy4/mod_simulation.html) | positech.co.uk | Democracy 4 |
| 527 | [Power & Revolution — official new-features page ('New redesigned and optimized interface', 4K/m](http://www.power-and-revolution.com/new_features.php?langue=en) | power-and-revolution.com | Power & Revolution / Geopolitical Simulator 4 |
| 528 | [Power & Revolution — official manuals index](https://www.power-and-revolution.com/manuel.php?langue=en) | power-and-revolution.com | Power & Revolution / Geopolitical Simulator 4 |
| 529 | [Power & Revolution — official user manual (Eversim, 2016), 68pp PDF — primary source for all sc](https://www.power-and-revolution.com/manuel/user_manual_EN.pdf) | power-and-revolution.com | Power & Revolution / Geopolitical Simulator 4 |
| 530 | [God'N Spy Add-on — official user manual (Eversim, 2016) PDF — the ~28-panel hidden-variable lis](https://www.power-and-revolution.com/manuel/user_manual_GS_EN.pdf) | power-and-revolution.com | Power & Revolution / Geopolitical Simulator 4 |
| 531 | [Power & Revolution — official presentation page (3D world map, thematic maps, ministry menus, 1](https://www.power-and-revolution.com/presentation.php) | power-and-revolution.com | Power & Revolution / Geopolitical Simulator 4 |
| 532 | [Power & Revolution — official simulation model page (600+ variables per country, 150+ economic ](https://www.power-and-revolution.com/simulation.php?langue=en) | power-and-revolution.com | Power & Revolution / Geopolitical Simulator 4 |
| 533 | [Bloomberg press release: Document Search & Analysis / AI research offering — PR Newswire](https://www.prnewswire.com/news-releases/investors-to-streamline-alpha-generating-research-with-bloombergs-latest-ai-offering-302482328.html) | prnewswire.com | Bloomberg Terminal |
| 534 | [ASM Consortium (now hosted by Honeywell) — ATTEMPTED AND NOT RETRIEVED (timeout / ECONNRESET / ](https://process.honeywell.com/us/en/site/asm-consortium) | process.honeywell.com | Safety-critical control-room interface design canon |
| 535 | [Henry, Fekete & McGuffin — NodeTrix: a Hybrid Visualization of Social Networks (IEEE TVCG 2007)](https://profs.etsmtl.ca/mmcguffin/research/nodetrix/nodetrix.pdf) | profs.etsmtl.ca | Relationship graph visualisation at scale — node-link vs mat |
| 536 | [Alertmanager (Prometheus docs) — grouping, inhibition and silences with stated rationales and e](https://prometheus.io/docs/alerting/latest/alertmanager) | prometheus.io | Security operations, observability and incident-response con |
| 537 | [Tannenbaum & Cerasoli — Do team and individual debriefs enhance performance? A meta-analysis, H](https://pubmed.ncbi.nlm.nih.gov/23516804) | pubmed.ncbi.nlm.nih.gov | Time, pause, replay, branching and counterfactual presentati |
| 538 | [Pennycook, Bear, Collins, Rand — The Implied Truth Effect, Management Science](https://pubsonline.informs.org/doi/10.1287/mnsc.2019.3478) | pubsonline.informs.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 539 | [Behrisch, Bach, Henry Riche, Schreck & Fekete — Matrix Reordering Methods for Table and Network](https://www.pure.ed.ac.uk/ws/files/37069720/Behrisch2016matrixordering.pdf) | pure.ed.ac.uk | Relationship graph visualisation at scale — node-link vs mat |
| 540 | [Radix Primitives — introduction](https://www.radix-ui.com/primitives/docs/overview/introduction) | radix-ui.com | Frontend technical feasibility for MERIDIAN: framework, pack |
| 541 | [Core/DefInjected/StorytellerDef/Storytellers.xml — Cassandra, Phoebe, Randy, Tutor definitions ](https://raw.githubusercontent.com/Ludeon/RimWorld-fr/master/Core/DefInjected/StorytellerDef/Storytellers.xml) | raw.githubusercontent.com | RimWorld |
| 542 | [Core/DefInjected/ThoughtDef/Thoughts_Memory_Social.xml — thought stages, label vs labelSocial s](https://raw.githubusercontent.com/Ludeon/RimWorld-fr/master/Core/DefInjected/ThoughtDef/Thoughts_Memory_Social.xml) | raw.githubusercontent.com | RimWorld |
| 543 | [Core/Keyed/Alerts.xml — full alert key list, label/Desc pairing, ClickToJumpToProblem, BreakRis](https://raw.githubusercontent.com/Ludeon/RimWorld-fr/master/Core/Keyed/Alerts.xml) | raw.githubusercontent.com | RimWorld |
| 544 | [Core/Keyed/Dialog_StatsReports.xml — the universal stat derivation format: BaseValue, RelevantT](https://raw.githubusercontent.com/Ludeon/RimWorld-fr/master/Core/Keyed/Dialog_StatsReports.xml) | raw.githubusercontent.com | RimWorld |
| 545 | [Core/Keyed/ITabs.xml — inspection pane tab roster and health/gear/social/prisoner sub-labels (f](https://raw.githubusercontent.com/Ludeon/RimWorld-fr/master/Core/Keyed/ITabs.xml) | raw.githubusercontent.com | RimWorld |
| 546 | [Core/Keyed/MainTabs.xml — ManualPriorities and Unchangeable keys (fetched)](https://raw.githubusercontent.com/Ludeon/RimWorld-fr/master/Core/Keyed/MainTabs.xml) | raw.githubusercontent.com | RimWorld |
| 547 | [IBM Carbon Design System — motion package source (productive vs expressive cubic-bezier curves)](https://raw.githubusercontent.com/carbon-design-system/carbon/main/packages/motion/src/index.ts) | raw.githubusercontent.com | Building an original "near-future command system" visual lan |
| 548 | [Getting Started on Bloomberg Launchpad (Bloomberg guide, third-party hosted) — components, brow](https://www.readkong.com/page/getting-started-on-bloomberg-launchpad-start-your-day-8978557) | readkong.com | Bloomberg Terminal |
| 549 | [Reddit — 'A complete list of red and white checks, ripped from game's files' (evidence the two ](https://www.reddit.com/r/DiscoElysium/comments/nnjq0r/a_complete_list_of_red_and_white_checks_ripped) | reddit.com | Disco Elysium |
| 550 | [Redux — Fundamentals Part 4: Store (DevTools, action log, deterministic replay)](https://redux.js.org/tutorials/fundamentals/part-4-store) | redux.js.org | Causal explanation interfaces for MERIDIAN — "why did this c |
| 551 | [Alerting Principles (PagerDuty Incident Response documentation) — alert vs notification definit](https://response.pagerduty.com/oncall/alerting_principles) | response.pagerduty.com | Security operations, observability and incident-response con |
| 552 | [RimWorld Wiki — Mental break (NOT fetchable: HTTP 403; referenced for break threshold definitio](https://rimworldwiki.com/wiki/Mental_break) | rimworldwiki.com | RimWorld |
| 553 | [RimWorld Wiki — Mood (source of the mood-target-marker and 35%/20%/5% break threshold figures; ](https://rimworldwiki.com/wiki/Mood) | rimworldwiki.com | RimWorld |
| 554 | [RimWorld Wiki — Thoughts (NOT fetchable: HTTP 403; listed for follow-up verification)](https://rimworldwiki.com/wiki/Thoughts) | rimworldwiki.com | RimWorld |
| 555 | [Inter typeface — design intent, tabular numbers, slashed zero, ss02 disambiguation](https://rsms.me/inter) | rsms.me | Building an original "near-future command system" visual lan |
| 556 | [Major Update: overhauled UI and exofighters — Saving Content (fetched; press-release quotes on ](https://www.savingcontent.com/2025/04/03/major-update-for-sci-fi-grand-strategy-early-access-hit-terra-invicta-brings-an-overhauled-ui-and-introduces-exofighters-today) | savingcontent.com | Terra Invicta |
| 557 | [From Warning to Wallpaper: Why the Brain Habituates to Security Warnings (Anderson, Vance et al](https://scholarsarchive.byu.edu/facpub/1955) | scholarsarchive.byu.edu | Provenance and fact-versus-narration separation in an interf |
| 558 | [Archambault & Purchase — The 'Map' in the mental map: Experimental results in dynamic graph dra](https://www.sciencedirect.com/science/article/pii/S107158191300102X) | sciencedirect.com | Relationship graph visualisation at scale — node-link vs mat |
| 559 | [ScreenRant — Disco Elysium: Dice Guide (percentage plus difficulty rating shown pre-roll)](https://screenrant.com/disco-elysium-dice-guide-uses) | screenrant.com | Disco Elysium |
| 560 | [Frostpunk 2 Review: The City Builder That Made Me Evil — ScreenRant [CRITIC: promise webs spira](https://screenrant.com/frostpunk-2-pc-review) | screenrant.com | Frostpunk |
| 561 | [Fandom wiki: Case Board — CITED BUT NOT FETCHED, returned HTTP 402 on every attempt including ?](https://shadows-of-doubt.fandom.com/wiki/Case_Board) | shadows-of-doubt.fandom.com | Shadows of Doubt |
| 562 | [Fandom wiki: Citizen Profile — CITED BUT NOT FETCHED (HTTP 402); source of the unverified '23 a](https://shadows-of-doubt.fandom.com/wiki/Citizen_Profile) | shadows-of-doubt.fandom.com | Shadows of Doubt |
| 563 | [sigma.js — official site and FAQ](https://www.sigmajs.org) | sigmajs.org | Frontend technical feasibility for MERIDIAN: framework, pack |
| 564 | [Simon Willison, 'CaMeL offers a promising new direction for mitigating prompt injection attacks](https://simonwillison.net/2025/Apr/11/camel) | simonwillison.net | Natural-language command and action-confirmation interfaces  |
| 565 | [Simon Willison, 'Design Patterns for Securing LLM Agents against Prompt Injections'](https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns) | simonwillison.net | Natural-language command and action-confirmation interfaces  |
| 566 | [Simon Willison, 'The lethal trifecta for AI agents'](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta) | simonwillison.net | Natural-language command and action-confirmation interfaces  |
| 567 | [FM21 Match Screens Mod — michaeltmurrayuk FM Skinning site (SEARCH SNIPPET ONLY; eight touchlin](https://sites.google.com/site/michaeltmurrayuk/fm2021/skin/fm21-match-screens-mod) | sites.google.com | Football Manager |
| 568 | [FETCH FAILED (HTTP 403) — SKYbrary article on alert fatigue. Aviation nuisance-alert evidence c](https://skybrary.aero/articles/alert-fatigue) | skybrary.aero | Alerts, attention and time pressure: an evidence base and co |
| 569 | [SKYbrary — Mode Awareness. ATTEMPTED AND FAILED (HTTP 403). Not consulted; listed so the gap is](https://skybrary.aero/articles/mode-awareness) | skybrary.aero | Situation awareness and the command shell: SA theory, ecolog |
| 570 | [Cities: Skylines Wiki — main page / navigation index](https://skylines.paradoxwikis.com/Cities:_Skylines_Wiki) | skylines.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 571 | [Cities: Skylines Wiki — Happiness (overlay only; no documented cause breakdown)](https://skylines.paradoxwikis.com/Happiness) | skylines.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 572 | [Cities: Skylines Wiki — Info views (all 37 views, per-view recolouring and panels)](https://skylines.paradoxwikis.com/Info_views) | skylines.paradoxwikis.com | Cities: Skylines 1 & 2 |
| 573 | [C2PA Harms Modelling 1.4 (over-trust, absence-of-credentials misreading, provenance vs veracity](https://spec.c2pa.org/specifications/specifications/1.4/security/Harms_Modelling.html) | spec.c2pa.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 574 | [C2PA User Experience Guidance 2.0 (disclosure levels L1-L4, icon, terminology, invalid states)](https://spec.c2pa.org/specifications/specifications/2.0/ux/UX_Recommendations.html) | spec.c2pa.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 575 | [C2PA specifications index 2.1 (document map)](https://spec.c2pa.org/specifications/specifications/2.1/index.html) | spec.c2pa.org | C2PA / Content Credentials, plus the AI-labelling and over-r |
| 576 | [C2PA User Experience Guidance v2.2 (L1–L4 progressive disclosure)](https://spec.c2pa.org/specifications/specifications/2.2/ux/UX_Recommendations.html) | spec.c2pa.org | Provenance and fact-versus-narration separation in an interf |
| 577 | [C2PA AI/ML Guidance v2.3 (model, prompt and training assertions)](https://spec.c2pa.org/specifications/specifications/2.3/ai-ml/ai_ml.html) | spec.c2pa.org | Provenance and fact-versus-narration separation in an interf |
| 578 | [A Message from Sports Interactive, An Update on Football Manager 25 (PRIMARY — fetched in full;](https://www.sports-interactive.com/news/message-sports-interactive-update-football-manager-25) | sports-interactive.com | Football Manager |
| 579 | [Monitoring Distributed Systems (Google SRE Book, Ch. 6) — symptoms vs causes, 'every page shoul](https://sre.google/sre-book/monitoring-distributed-systems) | sre.google | Alerts, attention and time pressure: an evidence base and co; Security operations, observability and incident- |
| 580 | [Google SRE Workbook — Alerting on SLOs; precision/recall/detection time/reset time and the mult](https://sre.google/workbook/alerting-on-slos) | sre.google | Alerts, attention and time pressure: an evidence base and co |
| 581 | [NASA-STD-7009 — standards landing page (scope and keywords only; the requirements PDF was not r](https://standards.nasa.gov/standard/nasa/nasa-std-7009) | standards.nasa.gov | Time, pause, replay, branching and counterfactual presentati |
| 582 | [Geo-Political Simulator 5 — Steambase review aggregate (213 positive / 358 negative of 571)](https://steambase.io/games/geo-political-simulator-5/reviews) | steambase.io | Power & Revolution / Geopolitical Simulator 4 |
| 583 | [Power & Revolution 2023 Edition — Steambase review aggregate (310 positive / 236 negative of 54](https://steambase.io/games/power-revolution-2023-edition/reviews) | steambase.io | Power & Revolution / Geopolitical Simulator 4 |
| 584 | [Developer Log #4: Leaders and Factions (Steam Community mirror)](https://steamcommunity.com/app/1154840/discussions/0/1750151146488506727) | steamcommunity.com | Shadow Empire |
| 585 | [Steam Community — 'Logistic overlay' discussion thread (player-experience evidence)](https://steamcommunity.com/app/1154840/discussions/0/3826413307978525076) | steamcommunity.com | Shadow Empire |
| 586 | [Steam Community — 'Someone please explain supply to me like im 5' (player-experience evidence)](https://steamcommunity.com/app/1154840/discussions/0/595136312034525807) | steamcommunity.com | Shadow Empire |
| 587 | [Steam discussion: How do you assign mission to the councilor? (fetched in full; the full assign](https://steamcommunity.com/app/1176470/discussions/0/3426690848063055621) | steamcommunity.com | Terra Invicta |
| 588 | [Steam discussion: Help with Nations' Priorities (fetched in full; players cannot determine allo](https://steamcommunity.com/app/1176470/discussions/0/4755326650052953544) | steamcommunity.com | Terra Invicta |
| 589 | [Steam discussion: Do codex updates work? (fetched in full; codex unlocks fire silently, alien m](https://steamcommunity.com/app/1176470/discussions/0/603035981320486635) | steamcommunity.com | Terra Invicta |
| 590 | [Steam discussion: Brutal Learning Curve (fetched in full; tech-tree ROI opacity, the 2035-40 wa](https://steamcommunity.com/app/1176470/discussions/0/783166115771613556) | steamcommunity.com | Terra Invicta |
| 591 | [Steam discussion: Control points not showing (fetched in full; developer explanation of automat](https://steamcommunity.com/app/1176470/discussions/1/4337609007228696790) | steamcommunity.com | Terra Invicta |
| 592 | [Steam Community discussion: 'Thoughts on the new UI' (player experience)](https://steamcommunity.com/app/1207650/discussions/0/3806156528939612945) | steamcommunity.com | Disco Elysium; Suzerain |
| 593 | [Steam Community discussion: 'Hard to make an informed decision if the game doesn't tell you eve](https://steamcommunity.com/app/1207650/discussions/0/4358994946499894354) | steamcommunity.com | Suzerain |
| 594 | [Steam Community discussion: 'Where to find public opinion?' (player experience)](https://steamcommunity.com/app/1207650/discussions/0/5143704785442630702) | steamcommunity.com | Suzerain |
| 595 | [Steam discussion thread title: 'Deposed with 100% popularity' (2021 Edition) — player-experienc](https://steamcommunity.com/app/1683320/discussions/0/5221372225828579720) | steamcommunity.com | Power & Revolution / Geopolitical Simulator 4 |
| 596 | [Steam discussion: 'As bad as the reviews suggest?' (2023 Edition) — learning curve, tutorial de](https://steamcommunity.com/app/2392520/discussions/0/4033601393692510955) | steamcommunity.com | Power & Revolution / Geopolitical Simulator 4 |
| 597 | [Geo-Political Simulator 5 — top-rated English Steam reviews (UI cramped, options cut off, no sa](https://steamcommunity.com/app/3107770/reviews/?browsefilter=toprated&l=english) | steamcommunity.com | Power & Revolution / Geopolitical Simulator 4 |
| 598 | [Steam discussion: 'Terminology questions' (player thread; Skunk/Bogey/Goblin definitions and id](https://steamcommunity.com/app/321410/discussions/0/613937306795379420) | steamcommunity.com | Command: Modern Operations |
| 599 | ['Concern about the ending description' — Frostpunk Steam Community discussion [PLAYER-EXPERIENC](https://steamcommunity.com/app/323190/discussions/0/3211505894139569798/?ctp=3) | steamcommunity.com | Frostpunk |
| 600 | ['UI is criminal' — Europa Universalis V Steam Community discussion (player-experience evidence)](https://steamcommunity.com/app/3450310/discussions/0/667222787666165479) | steamcommunity.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 601 | [Steam discussion thread title: 'Kicked out of office at 100% popularity' (base game)](https://steamcommunity.com/app/467520/discussions/0/2860219962083510284) | steamcommunity.com | Power & Revolution / Geopolitical Simulator 4 |
| 602 | [Power & Revolution — top-rated positive Steam reviews (meetings system, newspaper, depth praise](https://steamcommunity.com/app/467520/positivereviews/?p=1&browsefilter=toprated) | steamcommunity.com | Power & Revolution / Geopolitical Simulator 4 |
| 603 | [Power & Revolution — top-rated English Steam reviews (UI clunky, relationships not explained, m](https://steamcommunity.com/app/467520/reviews/?browsefilter=toprated&l=english) | steamcommunity.com | Power & Revolution / Geopolitical Simulator 4 |
| 604 | [Steam Community - 'Cant work out why my economy collapsed' (PLAYER EXPERIENCE; six-screen diagn](https://steamcommunity.com/app/529340/discussions/0/3470612993472730888) | steamcommunity.com | Victoria 3 |
| 605 | [Victoria 3 Dev Diary #128 - Political Movement Rework (official; summary only, NOT fetched in f](https://steamcommunity.com/app/529340/eventcomments/4846525460215806885) | steamcommunity.com | Victoria 3 |
| 606 | [Steam Community, Old World Gameplay Discussion — 'Event logs and/or family trees' (developer: S](https://steamcommunity.com/app/597180/discussions/0/3815166629925906635) | steamcommunity.com | Old World |
| 607 | [Steam Community, Old World Gameplay Discussion — 'Question about inheritance' (succession, chan](https://steamcommunity.com/app/597180/discussions/0/595139465034350879) | steamcommunity.com | Old World |
| 608 | [Steam Community, Old World General Discussion — 'this or civ4 if i turn off characters events?'](https://steamcommunity.com/app/597180/discussions/2/4299321616499803136) | steamcommunity.com | Old World |
| 609 | [Steam Community — 'Save/Load feature trivializes the game' (PLAYER EXPERIENCE: save-scumming vs](https://steamcommunity.com/app/632470/discussions/0/1644304412654563574) | steamcommunity.com | Disco Elysium |
| 610 | [Steam Community — '[Spoilers] How Reliable ARE the Skills?' (PLAYER EXPERIENCE: skills as compe](https://steamcommunity.com/app/632470/discussions/0/4328600953646840584) | steamcommunity.com | Disco Elysium |
| 611 | [Steam Community: What do the different colour stars mean? (FM2019) (fetched; PLAYER-EXPERIENCE ](https://steamcommunity.com/app/872790/discussions/0/1734343065627563910) | steamcommunity.com | Football Manager |
| 612 | [Dwarf Fortress General Discussions — Steam Community (PLAYER-EXPERIENCE EVIDENCE ONLY; threads ](https://steamcommunity.com/app/975370/discussions) | steamcommunity.com | Dwarf Fortress |
| 613 | [Steam Discussion: Problem with non-unique descriptions (fetched in full — the discriminating-po](https://steamcommunity.com/app/986130/discussions/0/3833172420312730510) | steamcommunity.com | Shadows of Doubt |
| 614 | [Steam Discussion: Combine two case files? (fetched in full — no merge, F1 notebook, search icon](https://steamcommunity.com/app/986130/discussions/0/3833172420319524019) | steamcommunity.com | Shadows of Doubt |
| 615 | [Dwarf Fortress review: the legendary colony sim gets a welcome facelift for Steam — Rock Paper ](https://steamcommunity.com/groups/rps/announcements/detail/3627116886085233354) | steamcommunity.com | Dwarf Fortress |
| 616 | [Steam community guide: 'Start Here: The Step-by-Step, Just Bought It, Read This First Guide' (p](https://steamcommunity.com/sharedfiles/filedetails/?id=1374061499) | steamcommunity.com | Command: Modern Operations |
| 617 | [Steam community guide: 'Why won't my units attack?!' (player-authored troubleshooting guide)](https://steamcommunity.com/sharedfiles/filedetails/?id=1383544306) | steamcommunity.com | Command: Modern Operations |
| 618 | [Extra Alerts (Steam Workshop) — modder evidence of missing base-game alerts](https://steamcommunity.com/sharedfiles/filedetails/?id=1926923167) | steamcommunity.com | RimWorld |
| 619 | [Democracy 4 — Basic Gameplay Guide, Steam (Positech-derived; screen-by-screen detail). Steam or](https://steamcommunity.com/sharedfiles/filedetails/?id=2242836711) | steamcommunity.com | Democracy 4 |
| 620 | [Steam Community guide: How to get the best Squad view (FM2021) (fetched; column categories, aut](https://steamcommunity.com/sharedfiles/filedetails/?id=2283420716) | steamcommunity.com | Football Manager |
| 621 | [Steam Community Guide — Grognerd's Guide to Human Resources Administration](https://steamcommunity.com/sharedfiles/filedetails/?id=2307478602) | steamcommunity.com | Shadow Empire |
| 622 | [Steam Community Guide — Logistics 101 (Shadow Empire)](https://steamcommunity.com/sharedfiles/filedetails/?id=2308877114) | steamcommunity.com | Shadow Empire |
| 623 | [Steam Community Guide — 'The User Interface explained' (Shadow Empire)](https://steamcommunity.com/sharedfiles/filedetails/?id=2326245400) | steamcommunity.com | Shadow Empire |
| 624 | [Steam Community Guide — Complete guide on Logistics (Shadow Empire)](https://steamcommunity.com/sharedfiles/filedetails/?id=2545048007) | steamcommunity.com | Shadow Empire |
| 625 | [Steam Community Guide: Terra Invicta Beginner's Guide, Part 2 (fetched in full; on-map CP statu](https://steamcommunity.com/sharedfiles/filedetails/?id=2868145461) | steamcommunity.com | Terra Invicta |
| 626 | [Steam Community Guide: Simplified flowchart of nation priorities and its effects (fetched in fu](https://steamcommunity.com/sharedfiles/filedetails/?id=2879615573) | steamcommunity.com | Terra Invicta |
| 627 | [Custom Alerts (Steam Workshop) — evidence that base-game alerts lack debounce and player-set cr](https://steamcommunity.com/sharedfiles/filedetails/?id=2895301341) | steamcommunity.com | RimWorld |
| 628 | [Steam Guide: How to find Information on any citizen (fetched — Government Database workflow; pl](https://steamcommunity.com/sharedfiles/filedetails/?id=2967470946) | steamcommunity.com | Shadows of Doubt |
| 629 | [Steam Guide: All Profile Clues, and how to track people down with them (fetched in full — actio](https://steamcommunity.com/sharedfiles/filedetails/?id=3017947856) | steamcommunity.com | Shadows of Doubt |
| 630 | [Advanced Character Search — Steam Workshop (mod; documents vanilla finder gaps and v1.19 Scribe](https://steamcommunity.com/sharedfiles/filedetails/?id=3084203091) | steamcommunity.com | Crusader Kings III |
| 631 | [Steam Workshop — 'More Informative Panel Tooltips' (Victoria 3); mod adding data the engine alr](https://steamcommunity.com/sharedfiles/filedetails/?id=3132089695) | steamcommunity.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 632 | [Events Without Tooltips — Steam Workshop (mod; evidence that full pre-commit outcome disclosure](https://steamcommunity.com/sharedfiles/filedetails/?id=3140405364) | steamcommunity.com | Crusader Kings III |
| 633 | [Steam Workshop: Outliner Overhaul Mod (fetched in full; complete sorting/highlighting/badging s](https://steamcommunity.com/sharedfiles/filedetails/?id=3243201397) | steamcommunity.com | Terra Invicta |
| 634 | [Steam Community guide: Situations guide (community-authored)](https://steamcommunity.com/sharedfiles/filedetails/?id=3486843361) | steamcommunity.com | Suzerain |
| 635 | [Steam Workshop - Advanced Market Panel (community-built sortable market view, price graphs, wee](https://steamcommunity.com/sharedfiles/filedetails/?id=3676318398) | steamcommunity.com | Victoria 3 |
| 636 | [Steam Community Guide: HOW TO PLAY TERRA INVICTA — THE COMPLETE GUIDE (fetched in full; success](https://steamcommunity.com/sharedfiles/filedetails/?id=3686982036) | steamcommunity.com | Terra Invicta |
| 637 | [Steam Global Achievement Stats — Terra Invicta (app 1176470)](https://steamcommunity.com/stats/1176470/achievements) | steamcommunity.com | Onboarding and learnability for very deep simulations — evid |
| 638 | [Steam Global Achievement Stats — Victoria 3 (app 529340)](https://steamcommunity.com/stats/529340/achievements) | steamcommunity.com | Onboarding and learnability for very deep simulations — evid |
| 639 | [Steam Workshop search for RimHUD — showing extensive community translation of the UI-overhaul m](https://steamcommunity.com/workshop/browse/?appid=294100&searchtext=RimHUD) | steamcommunity.com | RimWorld |
| 640 | [Outliner — Stellaris Wiki (four tabs, right edge, per-row name and system location)](https://stellaris.paradoxwikis.com/Outliner) | stellaris.paradoxwikis.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 641 | [NATO STO, 'Visualisation and the Common Operational Picture' — INACCESSIBLE (HTTP 403); the mos](https://www.sto.nato.int/document/visualisation-and-the-common-operational-picture) | sto.nato.int | Military & emergency command-and-control interfaces: ATAK/Wi |
| 642 | [Command: Modern Operations on Steam (store page; product framing)](https://store.steampowered.com/app/1076160/Command_Modern_Operations) | store.steampowered.com | Command: Modern Operations |
| 643 | [Shadow Empire on Steam — store page (review score, systems description)](https://store.steampowered.com/app/1154840/Shadow_Empire) | store.steampowered.com | Shadow Empire |
| 644 | [Suzerain on Steam — official store page and feature list](https://store.steampowered.com/app/1207650/Suzerain) | store.steampowered.com | Suzerain |
| 645 | [Steam — Sea Power: Naval Combat in the Missile Age (sensor modelling, ROE, contact-classificati](https://store.steampowered.com/app/1286220/Sea_Power__Naval_Combat_in_the_Missile_Age) | store.steampowered.com | Hearts of Iron IV |
| 646 | [Steam — Democracy 4 store page ('a custom-built neural network designed to model the opinions, ](https://store.steampowered.com/app/1410710/Democracy_4) | store.steampowered.com | Cities: Skylines 1 & 2 |
| 647 | [Steam — WARNO (battlegroup customisation, Army General turn-based campaigns; store copy proved ](https://store.steampowered.com/app/1611600/WARNO) | store.steampowered.com | Hearts of Iron IV |
| 648 | [Power & Revolution 2023 Edition on Steam — edition feature list](https://store.steampowered.com/app/2392520/Power__Revolution_2023_Edition) | store.steampowered.com | Power & Revolution / Geopolitical Simulator 4 |
| 649 | [Geo-Political Simulator 5 on Steam — store description and Mostly Negative review summary](https://store.steampowered.com/app/3107770/GeoPolitical_Simulator_5) | store.steampowered.com | Power & Revolution / Geopolitical Simulator 4 |
| 650 | [Steam — NEBULOUS: Fleet Command (radar shadows, signature management, run-cool, per-hardpoint c](https://store.steampowered.com/app/887570/NEBULOUS_Fleet_Command) | store.steampowered.com | Hearts of Iron IV |
| 651 | [Steam — Dwarf Fortress store page ("Learn the basics with in-game tutorials"; 94% Very Positive](https://store.steampowered.com/app/975370/Dwarf_Fortress) | store.steampowered.com | Onboarding and learnability for very deep simulations — evid |
| 652 | [Steam News — Democracy 4 updated to build 1.130 (search bar for main-screen icons; NOT fetched ](https://store.steampowered.com/news/app/1410710/view/2923359684772984021) | store.steampowered.com | Democracy 4 |
| 653 | [Victoria 3 Dev Diary #29 — 'User Experience' (Steam News) — attempted fetch returned only navig](https://store.steampowered.com/news/app/529340/view/3123809822934720292) | store.steampowered.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 654 | [Steam news: V39.07 (1.0 Release) patch notes — attempted fetch returned navigation chrome only;](https://store.steampowered.com/news/app/986130/view/4694529606299954722) | store.steampowered.com | Shadows of Doubt |
| 655 | [Storybook — documentation](https://storybook.js.org/docs) | storybook.js.org | Frontend technical feasibility for MERIDIAN: framework, pack |
| 656 | [Style Dictionary](https://styledictionary.com) | styledictionary.com | Frontend technical feasibility for MERIDIAN: framework, pack |
| 657 | [Decision — Suzerain Wiki (wiki.gg)](https://suzerain.wiki.gg/wiki/Decision) | suzerain.wiki.gg | Suzerain |
| 658 | [Endings — Suzerain Wiki (wiki.gg)](https://suzerain.wiki.gg/wiki/Endings) | suzerain.wiki.gg | Suzerain |
| 659 | [Reform — Suzerain Wiki (wiki.gg)](https://suzerain.wiki.gg/wiki/Reform) | suzerain.wiki.gg | Suzerain |
| 660 | [Turn — Suzerain Wiki (wiki.gg)](https://suzerain.wiki.gg/wiki/Turn) | suzerain.wiki.gg | Suzerain |
| 661 | [TanStack Query — overview (server state vs client state)](https://tanstack.com/query/latest/docs/framework/react/overview) | tanstack.com | Frontend technical feasibility for MERIDIAN: framework, pack |
| 662 | [TanStack Virtual — introduction](https://tanstack.com/virtual/latest/docs/introduction) | tanstack.com | Frontend technical feasibility for MERIDIAN: framework, pack |
| 663 | [TheGamer — How The Dice System Works In Citizen Sleeper (five-die pool, condition reduces dice,](https://www.thegamer.com/citizen-sleeper-dice-explained-guide) | thegamer.com | Disco Elysium |
| 664 | [Frostpunk: Everything You Need To Know About The Book Of Laws — TheGamer [red/blue effect bulle](https://www.thegamer.com/frostpunk-book-of-laws-guide) | thegamer.com | Frostpunk |
| 665 | [The Register — MPs tell NHS to start packing Palantir's bags ahead of 2027 contract break (2026](https://www.theregister.com/public-sector/2026/07/09/mps-tell-nhs-to-start-packing-palantirs-bags-ahead-of-2027-contract-break/5269146) | theregister.com | Palantir Gotham and Foundry |
| 666 | [The Register — Some English hospitals doubt Palantir's utility: We'd 'lose functionality rather](https://www.theregister.com/software/2025/05/16/nhs-england-hospitals-cast-doubt-on-palantir-use-case/696899) | theregister.com | Palantir Gotham and Foundry |
| 667 | [The Register — Write-back to aging UK health systems lessens benefits of Palantir-based platfor](https://www.theregister.com/software/2025/07/10/write-back-to-aging-nhs-systems-limits-palantir-platform/697492) | theregister.com | Palantir Gotham and Foundry |
| 668 | [The Register — NHS staff resist using Palantir software (2026-04-03)](https://www.theregister.com/software/2026/04/03/nhs-staff-resist-using-palantir-software/5226660) | theregister.com | Palantir Gotham and Foundry |
| 669 | [Crusader Kings 3 Console Review — TheSixthAxis (nested tooltips behind a left-stick tooltip mod](https://www.thesixthaxis.com/2022/03/29/crusader-kings-3-console-review) | thesixthaxis.com | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 670 | [Review: As President in Suzerain You Make the Tough Choices — Third Coast Review (Overview pane](https://thirdcoastreview.com/2020/12/03/game-review-suzerain) | thirdcoastreview.com | Suzerain |
| 671 | [Thunderstore mod database for Shadows of Doubt (fetched — mod landscape; no dominant case-board](https://thunderstore.io/c/shadows-of-doubt) | thunderstore.io | Shadows of Doubt |
| 672 | [Torpor Games & Fellow Traveller Unveil Suzerain 2.0 'Amendment' Update (press release)](https://www.torporgames.com/press-releases-new/2023/07/31/torpor-games-fellow-traveller-unveil-suzerain-20-amendment-update) | torporgames.com | Suzerain |
| 673 | [Suzerain – 3.1 'Sovereign' Major Update is OUT NOW (press release)](https://www.torporgames.com/press-releases-new/2025/5/13/sovereign-update) | torporgames.com | Suzerain |
| 674 | [ATAK Civilian Software User Manual, Version 4.5, 22 November 2021 (60 pp.) — fetched and text-e](https://toyon.github.io/LearnATAK/atak_resource/v4.5/ATAK_User_Guide.pdf) | toyon.github.io | Military & emergency command-and-control interfaces: ATAK/Wi |
| 675 | [LearnATAK developer quick reference — definitions of toolbar, toolbar item, pane (right in land](https://toyon.github.io/LearnATAK/docs/atak_development/atak_quick_reference) | toyon.github.io | Military & emergency command-and-control interfaces: ATAK/Wi |
| 676 | [Turn Based Lovers — Shadow Empire review](https://turnbasedlovers.com/review/shadow-empire) | turnbasedlovers.com | Shadow Empire |
| 677 | [Terra Invicta 1.0 Review: From Long War Trauma to Solar-System Strategy Survival — Turn Based L](https://turnbasedlovers.com/review/terra-invicta-1-0-impressions) | turnbasedlovers.com | Terra Invicta |
| 678 | [Frostpunk 2 Council Voting Explained — Twinfinite [ATTEMPTED, returned HTTP 403; listed for com](https://twinfinite.net/guides/frostpunk-2-council-voting-explained-how-to-pass-every-vote-negotiate-more) | twinfinite.net | Frostpunk |
| 679 | [FETCH FAILED (HTTP 403) — Alahmadi, Legg & Nurse, '99% False Positives: A Qualitative Study of ](https://www.usenix.org/system/files/sec22-alahmadi.pdf) | usenix.org | Alerts, attention and time pressure: an evidence base and co |
| 680 | [Nur Khamran, 'How do I play this? A case study looking into information overload within the gra](https://uu.diva-portal.org/smash/get/diva2:1773220/FULLTEXT01.pdf) | uu.diva-portal.org | Paradox Interactive's nested tooltip and modifier-breakdown  |
| 681 | [Dominique Leca, 'The Impossible Bloomberg Makeover', UX Magazine, 24 March 2010 (OPINION; IDEO ](https://uxmag.com/articles/the-impossible-bloomberg-makeover) | uxmag.com | Bloomberg Terminal |
| 682 | [Victoria 3 Community Wiki — Achievements (Ironman not required)](https://vic3.paradoxwikis.com/Achievements) | vic3.paradoxwikis.com | Onboarding and learnability for very deep simulations — evid |
| 683 | [Victoria 3 Wiki - Building (buildings panel, balance sheet, predictive production-method toolti](https://vic3.paradoxwikis.com/Building) | vic3.paradoxwikis.com | Victoria 3 |
| 684 | [Victoria 3 Community Wiki — Journal entries (visibility/activation/completion conditions, timer](https://vic3.paradoxwikis.com/Journal_entries) | vic3.paradoxwikis.com | Onboarding and learnability for very deep simulations — evid |
| 685 | [Victoria 3 Wiki - Market (mechanics only; contains no UI description, noted as a source gap)](https://vic3.paradoxwikis.com/Market) | vic3.paradoxwikis.com | Victoria 3 |
| 686 | [Victoria 3 Wiki - Pops (pop definition, wealth, political strength, qualifications, loyalty sta](https://vic3.paradoxwikis.com/Pops) | vic3.paradoxwikis.com | Victoria 3 |
| 687 | [Victoria 3 Wiki - Production method](https://vic3.paradoxwikis.com/Production_method) | vic3.paradoxwikis.com | Victoria 3 |
| 688 | [User interface — Victoria 3 Wiki (top bar rows, left panel destinations, situation button count](https://vic3.paradoxwikis.com/User_interface) | vic3.paradoxwikis.com | Onboarding and learnability for very deep simulations — evid; Paradox Interactive's nested tooltip and modifie |
| 689 | [Vice/Motherboard — Revealed: This Is Palantir's Top-Secret User Manual for Cops (leaked Gotham ](https://www.vice.com/en/article/revealed-this-is-palantirs-top-secret-user-manual-for-cops) | vice.com | Palantir Gotham and Foundry |
| 690 | [Return of the Obra Dinn: A Lesson on Detective Games and Hands-Off Design (Vicious Undertow)](https://viciousundertow.wordpress.com/2018/11/08/return-of-the-obra-dinn-a-lesson-on-detective-games-and-hands-off-design) | viciousundertow.wordpress.com | Evidence, deduction and document-verification interfaces |
| 691 | [Terra Invicta: Beginner Tips — Nation Control and Councilors, Vortex Gaming (fetched; councillo](https://vortexgaming.io/en/postdetail/634901) | vortexgaming.io | Terra Invicta |
| 692 | [W3C — Making Content Usable for People with Cognitive and Learning Disabilities (COGA)](https://www.w3.org/TR/coga-usable) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 693 | [W3C — PROV-OVERVIEW (PROV family of documents)](https://www.w3.org/TR/prov-overview) | w3.org | Causal explanation interfaces for MERIDIAN — "why did this c |
| 694 | [W3C — PROV-PRIMER (provenance core concepts and relations)](https://www.w3.org/TR/prov-primer) | w3.org | Causal explanation interfaces for MERIDIAN — "why did this c |
| 695 | [W3C, Understanding WCAG 2.1 Success Criterion 1.4.1 Use of Color](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html) | w3.org | Uncertainty visualisation research and its practical encodin |
| 696 | [W3C — Understanding SC 2.3.3: Animation from Interactions (WCAG 2.2, Level AAA)](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) | w3.org | Building an original "near-future command system" visual lan |
| 697 | [W3C — Understanding SC 1.4.13: Content on Hover or Focus (WCAG 2.2, Level AA)](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html) | w3.org | Progressive disclosure and information density in expert int |
| 698 | [WCAG 2.2 Understanding SC 1.4.3 Contrast (Minimum) (W3C WAI)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma; Provenance and fact-versus-narration separation  |
| 699 | [W3C — Understanding SC 2.4.13 Focus Appearance, WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 700 | [W3C — Understanding SC 2.4.11 Focus Not Obscured (Minimum), WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 701 | [WCAG 2.2 Understanding SC 1.3.1 Info and Relationships (W3C WAI)](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html) | w3.org | Provenance and fact-versus-narration separation in an interf |
| 702 | [WCAG 2.2 Understanding SC 3.1.2 Language of Parts (W3C WAI)](https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html) | w3.org | Provenance and fact-versus-narration separation in an interf |
| 703 | [WCAG 2.2 Understanding SC 1.4.11 Non-text Contrast (W3C WAI)](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma; Building an original "near-future command system |
| 704 | [W3C — Understanding SC 1.4.4 Resize Text, WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 705 | [W3C — Understanding SC 4.1.3 Status Messages, WCAG 2.2 (PRIMARY NORMATIVE; role=status / role=a](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) | w3.org | Situation awareness and the command shell: SA theory, ecolog |
| 706 | [W3C — Understanding SC 2.5.8: Target Size (Minimum) (WCAG 2.2, Level AA)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma; Progressive disclosure and information density i |
| 707 | [WCAG 2.2 Understanding SC 1.4.1 Use of Color (W3C WAI)](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma; Building an original "near-future command system |
| 708 | [W3C WAI — Complex Images (charts, diagrams, maps)](https://www.w3.org/WAI/tutorials/images/complex) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 709 | [W3C WAI — Tables Tutorial](https://www.w3.org/WAI/tutorials/tables) | w3.org | Accessibility for MERIDIAN's dark, dense, colour-coded comma |
| 710 | [Command: Modern Operations review – prettier and smarter (Wargamer; critic review)](https://www.wargamer.com/command-modern-operations/review) | wargamer.com | Command: Modern Operations |
| 711 | [Wargamer - 'Victoria 3's top mods turn it back into a spreadsheet simulator' (mod-popularity ev](https://www.wargamer.com/victoria-3/spreadsheet-mods) | wargamer.com | Victoria 3 |
| 712 | [Notes on Heuer & Pherson, 'Structured Analytic Techniques for Intelligence Analysis' — ACH matr](https://warnerchad.medium.com/structured-analytic-techniques-for-intelligence-analysis-notes-f11c9a8c934c) | warnerchad.medium.com | Intelligence-analysis tradecraft standards for expressing un |
| 713 | [Frostpunk 2 review — wccftech [ATTEMPTED, returned HTTP 403; NOT used as evidence]](https://wccftech.com/review/frostpunk-2-day-after-tomorrow) | wccftech.com | Frostpunk |
| 714 | [web.dev — Interaction to Next Paint (INP)](https://web.dev/articles/inp) | web.dev | Frontend technical feasibility for MERIDIAN: framework, pack |
| 715 | [Phenixx Gaming — Democracy 4 (PC) Review [fetched; contained no UI criticism, contrary to searc](https://web.phenixxgaming.com/2024/07/05/democracy-4-pc-review) | web.phenixxgaming.com | Democracy 4 |
| 716 | [WFTAK (Wildland Fire TAK) programme portal — identified via search, NOT fetched](https://wftak.wildfire.gov/pages/wftak-overview) | wftak.wildfire.gov | Military & emergency command-and-control interfaces: ATAK/Wi |
| 717 | [Colin Nagy, 'The Bloomberg Terminal Edition', Why Is This Interesting (OPINION essay; culture/l](https://whyisthisinteresting.substack.com/p/the-bloomberg-terminal-edition) | whyisthisinteresting.substack.com | Bloomberg Terminal |
| 718 | [Old World Official Wiki (Hooded Horse) — Characters / Opinion (NOT FETCHABLE: HTTP 403; referen](https://wiki.hoodedhorse.com/Old_World/Characters) | wiki.hoodedhorse.com | Old World |
| 719 | [Control Point Capacity — Terra Invicta Official Wiki (NOT FETCHED: HTTP 403; used only via sear](https://wiki.hoodedhorse.com/Terra_Invicta/Control_Point_Capacity) | wiki.hoodedhorse.com | Terra Invicta |
| 720 | [Councilors — Terra Invicta Official Wiki (NOT FETCHED: HTTP 403 on every attempt; used only via](https://wiki.hoodedhorse.com/Terra_Invicta/Councilors) | wiki.hoodedhorse.com | Terra Invicta |
| 721 | [Nations — Terra Invicta Official Wiki (NOT FETCHED: HTTP 403; used only via search-result summa](https://wiki.hoodedhorse.com/Terra_Invicta/Nations) | wiki.hoodedhorse.com | Terra Invicta |
| 722 | [Ghoniem, Fekete & Castagliola — Readability of Graphs Using Node-Link and Matrix-Based Represen](https://www-sop.inria.fr/orion/COGC/teams/INSITUghoniem-fivj05-final.pdf) | www-sop.inria.fr | Relationship graph visualisation at scale — node-link vs mat |
| 723 | [Terra Invicta Early Game Walkthrough — xcom.substack.com (fetched; Relations tab usage, players](https://xcom.substack.com/p/terra-invicta-early-game-walkthrough) | xcom.substack.com | Terra Invicta |
| 724 | [Tackling UI challenges in Football Manager 25 / Unite 2024 — Sports Interactive (PRIMARY talk; ](https://www.youtube.com/watch?v=im49swPfWIo) | youtube.com | Football Manager |

<!-- END GENERATED SOURCE TABLE -->

---

**End of register.** Verification status is per-claim, not per-source. A recommendation may not carry more confidence than its weakest load-bearing source.
