# Adaptive Futures Engine

**Status: UNDER RESEARCH**
**Last reviewed: 21 July 2026** (against `main` at `bfd2aa7`)

> **NOT IMPLEMENTED.** MERIDIAN runs single scenarios. It has no ensembles, no controlled parameter
> variation, and **no dispersion testing**.
>
> **MERIDIAN does not generate calibrated real-world probabilities, and must not use probability
> language until outcome dispersion and calibration have been studied.**

## In one sentence

Run many controlled variations of a scenario to understand plausible outcomes, risks,
opportunities, critical decisions, and the points where a small change sends the world down a
different path.

## The problem

A single run of a simulation answers one question: what happens under these exact assumptions. That
is rarely the question anyone has. The useful questions are *what could happen*, *what decides
which*, and *which choices hold up regardless* — and none of them is answerable from one run.

## How MERIDIAN could help

Run the same scenario many times with controlled differences — different decisions, different
timing, different information reaching different people, institutional delay, unexpected events —
and report the patterns: which outcomes recur, under what conditions, and where a small change
flips the path.

**It is a wind tunnel for possible futures, not a crystal ball.** The output is not *"Outcome A:
62%"* — a number that means almost nothing alone. It is:

> This outcome appeared often when verification was delayed, coastal employment fell quickly, and
> the broadcaster published the unverified claim. It rarely appeared when records were released
> before day seven.

That tells you the mechanism, which is the part you can act on.

## A simple example

Run the blockade a thousand times, varying when the government publishes its legal assessment and
how quickly employment effects land. Report which combinations produced escalation in the model,
which produced settlement, and which single choice separated them most often — **stated as a fact
about the runs, not about the world.**

## Who might use it

Planners and analysts weighing options; anyone who needs to know which decisions are robust rather
than which outcome is likeliest.

## What MERIDIAN already has

- **Deterministic single runs** — same seed, same inputs, same result.
- A ten-stage causal chain with declared lag.
- A trajectory recorded per run.
- Inspectable decisions and traces.

**That is all.** Reproducibility is the foundation this would need; it is not a version of it.

## What is still missing

- **Scenario ensembles** — running many variations at all.
- **Controlled parameter variation** — a declared, versioned grid.
- **Outcome classification** — deciding what counts as the same outcome.
- **Dispersion testing** — measuring whether the range is wide enough. *This is the blocker.*
- **Calibration.**
- **Sensitivity analysis.**
- **Rare-event handling.**
- **Novelty generation** — agents that create options nobody designed in.
- **Named RNG substreams.** Adding a draw in one subsystem currently shifts every later draw
  everywhere, which makes controlled variation impossible to interpret.

## What it must never claim

- **Real-world probabilities.** Not until dispersion and calibration are studied. Run frequency is a
  fact about the model, not about the world.
- That more runs mean more meaningful futures. Ten thousand runs of a model with the wrong mechanism
  produce a confident wrong answer faster.
- That reproducibility implies adequate variation. **They are different requirements**, and
  MERIDIAN has only the first.
- That fitting known history demonstrates anything about new events.
- That it identifies which decision "mattered most" — that is a causal-attribution claim, and
  equifinality means many parameter sets produce the same output.

## Key risks

- **Under-dispersion, and it is evidenced.** A pre-registered study across 164 outcomes found
  synthetic populations were **less varied than the real humans they modelled in 93.9% of
  outcomes**; a separate study found simulations produce "artificially harmonious societies".
  **Crises are tail events** — driven by outliers, defectors and panics. A system that smooths the
  tails loses the phenomenon it exists to study.
- **False confidence from good presentation.** A well-designed screen reading "this recurred in 62%
  of runs" is persuasive whether or not the runs explored anything.
- **Equifinality.** Many different parameter sets produce identical output, so matching data does
  not identify the mechanism.
- **Compounding with other strands.** "This design survived 8,000 futures" is far more persuasive
  than "it survived one run", and no more valid.

## Supporting research

[Next-strand note](../research/NEXT-STRAND-ADAPTIVE-FUTURES-ENGINE.md) — including §8a, the first
research question, and the ten-part evaluation proposed.

[Issue #26 — Measure outcome dispersion before building the Adaptive Futures Engine](https://github.com/CypherTechAries/project-meridian/issues/26)

Related: [Narrative and Incentive Intelligence §20](../research/NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md),
on supplying simulated information environments as inputs.

[Real-Geography Scenarios](REAL-GEOGRAPHY-SCENARIOS.md) — real geography would constrain what
varies, but it does **not** help with dispersion, which is this strand's actual blocker.

## Next proof required

**One measurement, before any implementation:**

> **Do MERIDIAN's existing scenario runs under-disperse?**

Repeated runs across declared seeds and parameter variations; the distribution of final outcomes and
important intermediate states; sensitivity to small changes; frequency of rare outcomes; diversity of
decision paths; and **explicit identification of the mechanisms that force convergence**.

**Either answer is useful.** If it under-disperses, that is the strand's first real finding and it
governs everything designed afterwards. If it does not, that is a citable result worth having before
anything is built.

**No probability language until that measurement exists.**
