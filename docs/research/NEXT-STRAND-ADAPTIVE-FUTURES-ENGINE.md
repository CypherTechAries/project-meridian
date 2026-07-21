# Next research strand — the Adaptive Futures Engine

**Status: QUEUED, NOT STARTED.** This is a placeholder written on 21 July 2026 so the idea is not
lost, and so that the research already done for the simulation-born-entities strand is attached to
it while it is fresh. **No research task has been run on this yet.**

The founder's framing, recorded as given:

> MERIDIAN should not claim "this is what will happen". It should say: these are the futures that
> repeatedly emerge from the situation you described, these are the conditions that create them, and
> these are the points where a small change sends the world down a different path.
>
> **Less a crystal ball, more a wind tunnel for possible futures.**

---

## Why this note exists now

The simulation-born-entities research turned up material that bears directly on this idea — some of
it strongly supportive, some of it a serious warning. Recording it here means the next strand starts
from evidence rather than from scratch.

## 1. The framing is supported by the literature, and there is a citation for it

**RESEARCH FINDING.** Edmonds et al. (2019), *"Different Modelling Purposes"*, JASSS 22(3):6, DOI
`10.18564/jasss.3993`, identifies **seven distinct purposes** a social simulation can serve —
prediction, explanation, description, theoretical exploration, illustration, analogy, and social
interaction — and argues that a model built for one purpose and used for another **must be
re-justified, re-checked and possibly rebuilt**. Verbatim:

> "It also looks at the ways that a confusion of modelling purposes can fatally weaken modelling
> projects, whilst giving a false sense of their quality."

The instinct that MERIDIAN should describe mechanisms rather than assert outcomes is **the same
distinction that paper draws**, and it is the distinction the field says is most often collapsed.
The founder's phrasing — *"this outcome appeared often when X, Y and Z; it rarely appeared when W"* —
is explanation-and-exploration, not prediction. That is defensible. **"Outcome A: 62%" is not**, and
the founder's own instinct to reject it is correct on the evidence.

## 2. The hardest warning, and it is aimed straight at this idea

**RESEARCH FINDING.** Edmonds et al. define prediction strictly — reliably anticipating *unknown*
data — and report that of 40 econometric models claiming to predict a time series, **37 failed
completely when tested against newly available data from that same series.** Verbatim:

> "**Fitting known data is simply not a sufficient test for predictive ability.**"

And on the specific move this strand is most tempted to make:

> "**Explanation → Prediction.** … the model is fitted to that particular set of data. Model fitting
> is not a good way to construct a model useful for prediction… This is especially true for social
> systems, where we often cannot predict events, but we can explain them after they have occurred."

**INFERENCE.** An adaptive futures engine that runs thousands of variations and reports which
outcomes recur is producing a distribution *over its own assumptions*, not over the world. The
number of runs does not change that. Ten thousand runs of a model with the wrong mechanism produce a
confident wrong answer faster.

## 3. Three specific technical hazards already evidenced

**(a) Under-dispersion — the one that matters most here.** An independent pre-registered study across
164 outcomes found synthetic populations were **less varied than the real humans they modelled in
93.9% of outcomes**, with average individual-level correlation r = 0.197. A separate 2025 study
across 8 models found simulations produce *"artificially harmonious societies"* through social
desirability bias.

**Crises are tail events.** They are driven by defectors, outliers, panics and people who do not
behave like the average. A futures engine built on components that systematically narrow variance
and bias toward harmony will **systematically under-produce exactly the futures it exists to find** —
and it will do so while appearing well-calibrated on the mean.

**(b) Robustness.** A 2026 study found that perturbations to *persona formatting and instruction
framing* shifted cooperation rates by **up to 76 percentage points** in one model while moving
another by 1 point. If "which outcomes recur" is sensitive to formatting at that magnitude, the
recurrence statistic is measuring the implementation, not the world.

**(c) Equifinality.** Beven's equifinality thesis and Windrum et al.'s identification problem both
say the same thing: **many different parameter sets and structures produce the same output**, so
matching observed data does not identify the mechanism that produced it. Verbatim, Windrum et al.
(2007):

> "there are, in principle, a great many combinations of alternative parameter settings that can
> produce an identical output trace. We cannot deduce which combination of parameter settings is
> correct, let alone the appropriate set of structural assumptions."

This bites hardest on the founder's most valuable proposed output — *"which decision mattered most"*.
That is a causal-attribution claim, and equifinality is precisely the reason it may not be
identifiable from the runs alone.

## 4. What the evidence says the engine can honestly claim

Ordered from safest to most dangerous:

| Claim | Verdict on current evidence |
|---|---|
| "These are mechanisms by which the situation could develop" | **Defensible** — theoretical exploration / explanation |
| "This outcome recurred under these conditions in our model" | **Defensible if stated as a fact about the model** |
| "This is where a small change alters the path in our model" | **Defensible, with the equifinality caveat stated** |
| "These choices performed acceptably across many of our runs" | **Defensible** — this is robust-decision-making, and it is the strongest framing available |
| "Outcome A occurs 62% of the time" | **Not defensible** without stating it is 62% of *our runs under our assumptions* |
| "This is what will happen" | **Not defensible.** Ever |

**INFERENCE.** The most defensible product framing is not probability at all — it is **robustness**:
*which choices do acceptably across many different futures?* That question survives every objection
above, because it does not require the distribution to be right. It only requires the futures
explored to be diverse.

## 5. The novelty problem — the founder's sharpest point

The observation that real people invent options no designer imagined is correct, and it has a
verified counterpart in the literature. The most-publicised "AI civilisation" demonstration
**supplied its constitution and voting system in advance** and prompted designated agents to
campaign; its authors concede the agents *"cannot simulate de novo emergence of societal
innovations"* because they are built on models trained on existing human knowledge.

**OPEN QUESTION.** Whether an LLM can propose genuinely novel options, or only recombine recorded
ones, is unresolved — and the founder's proposed architecture (the model *proposes*, the simulation
*tests*) is the right shape regardless, because it does not require the answer. It is also the same
shape as MERIDIAN's existing rule: the model may propose; the engine decides.

## 6. What good practice looks like, from the ensemble evidence

**RESEARCH FINDING.** The COVID modelling hubs are the closest large-scale precedent for "run many
models, report the pattern", and their results are instructive in both directions:

- Multi-model ensembles **beat essentially every individual contributor** on consistency and
  calibration — while rarely being the single best forecast.
- **All of them failed at turning points.** Error at a 20-week horizon was **3–5× that at 1 week**.
  Scenarios stayed close to reality **~22 weeks on average** before new variants invalidated their
  assumptions.
- UK SPI-M-O published its projections with the standing caveat that they are **"not forecasts or
  predictions"**, combined six independent models into a consensus, disciplined its language with a
  formal probability lexicon, and published **projection-versus-outturn charts** afterwards.

**INFERENCE.** That last practice — publishing what you said against what happened — is the single
most transferable idea for this strand, and it is cheap. It is also the mechanism by which the
founder's "learn without rewriting history" requirement becomes real rather than aspirational.

## 7. The contrast worth internalising

**RESEARCH FINDING.** UK transport appraisal (DfT TAG Unit M3.1) has, for models used in government
decisions: a named statistic (GEH), numeric thresholds, stated hit-rates (85%/95%), convergence
targets, a mandatory validation report, and an explicit duty to **explain your misses**. Epidemic
microsimulation used for the largest peacetime policy intervention in UK history had none of those.

Part of that gap is a fact about the problem — transport models validate against an observed base
year, which a novel-crisis model does not have. But the direction is clear: **the mature regimes
regulate the credibility argument, not the model.**

## 8. How this connects to the first strand

The founder's connection is real: an adaptive futures engine could discover promising organisations,
products and ideas inside simulated futures, and the graduation framework is how the strongest ones
would cross into reality.

**But note the compounding risk.** Strand 1's central hazard is that simulated success is mistaken
for evidence. Strand 2 **multiplies the apparent evidence** — "this design survived 8,000 futures"
is far more persuasive than "this design survived one run", and no more valid. If both strands are
built, the honesty controls must be strengthened, not reused.

## 9. Questions the next research task should answer

1. Can a recurrence statistic over runs be reported without implying a probability about the world?
2. Does robustness framing ("works across many futures") survive the equifinality objection where
   probability framing does not?
3. How is variance restored to simulated populations that systematically under-disperse?
4. What is the minimum robustness-audit standard before any run-frequency claim is shown to a user?
5. Can causal attribution — "which decision mattered most" — be identified from runs, or only from
   designed interventions within them?
6. What does the simulated/real event separator need to look like for outcome tracking to be honest?
7. Is there a defensible way to represent novelty, or must the engine declare it a known blind spot?
8. What would MERIDIAN's equivalent of a published projection-versus-outturn record be?

## 10. Recommended posture

**Do not start this until the current usability work lands.** The evidence in §3 says the components
this engine would be built from currently narrow variance and bias toward harmony — which is the
opposite of what a crisis futures engine needs. That is a research problem to be solved *before* the
engine is designed, not after.

The single most useful early action is not to build anything. It is to **test whether MERIDIAN's
existing runs under-disperse**, because if they do, that finding governs the whole strand.
