# Crisis Simulation and Decision Support

**Status: EARLY DEMONSTRATION**
**Last reviewed: 21 July 2026** (against `main` at `bfd2aa7`)

## In one sentence

Run a fictional crisis and inspect how events move through organisations, the economy, population
groups and individual decisions.

## The problem

When something goes wrong — a port closes, a supply route is cut, a claim spreads — the hard part is
rarely the event itself. It is working out how the effects travel: who finds out, who is hurt first,
which pressures build on which institutions, and which decisions are still open by the time anyone
is able to act. That reasoning usually happens in people's heads, in meetings, with no record of why
anyone believed what they believed.

## How MERIDIAN could help

It runs the chain explicitly. An event produces effects; effects reach people and organisations
differently; beliefs change or do not; options open or close as pressure builds. **Every step is
inspectable, and every value can be traced back to what caused it.** The same run produces the same
result every time.

## A simple example

In the current scenario a strait is blocked. Insurers reprice, carriers reroute, port activity
falls, employment exposure rises, households become concerned, attention builds, and political
pressure follows — several days behind the disruption that caused it. As that pressure crosses a
declared threshold, a government option changes status from constrained to open. You can ask *why*
and get the chain, not an opinion.

Separately, three fictional people receive — or do not receive — a claim about the government's
handling of it, and their recorded beliefs move differently as a result. One of them selects an
action. **It is never executed.**

## Who might use it

Analysts and planners reasoning about cascading effects; researchers who want a reproducible
environment; teams who need to explain *why* a projection says what it says rather than assert it.

## What MERIDIAN already has

Verified against `main`:

- One fictional scenario — the Kestral Strait — with a **ten-stage causal chain** from incident
  severity through to political pressure, including declared lag between stages.
- **Deterministic runs**: same seed, same inputs, same result.
- **Organisations, people and population groups modelled separately.**
- Government options whose status is driven by a named engine value.
- **Three virtual people** with current-situation records, action selection, relationships,
  information-exposure history and belief history.
- **Decisions that are selected and explicitly never executed** — the codebase refuses to construct
  one with any other status.
- **Append-only histories**, so a record cannot be quietly rewritten.
- **Origin and absence labels** — `ENGINE` / `FIXTURE` / `UNKNOWN` / `UNAVAILABLE` / `NOT_MODELLED`.
  Absence is never rendered as zero.
- **Read-only dossiers** and a read-only belief API.
- **Ask MERIDIAN Phase 1** — eight declared question types, matched without a language model.
- A **Briefing view and an Analysis view**, switchable. *On `main` these are the pre-reset versions:
  Briefing is a dashboard with a dominant map and a decision stack, and Analysis is the panel wall
  the first-time user could not read.*

## The limitation to read first

**Selected decisions do not yet change the run.** A submitted action is recorded and the tick loop
never reads it, so the demonstration explains a packaged state and supports inspectable but
unexecuted choices. The interface states this wherever a choice is shown. Closing it is
[#42](https://github.com/CypherTechAries/project-meridian/issues/42), and it is the difference
between a decision-support demonstration and a decision simulation.

## What is still missing

- **A second scenario.** One exists. Whether a second loads and completes has never been tested.
- **Scenario authoring** of any kind.
- Most scenario content is parsed and then **read by no code** — two scenarios differing only in
  those fields would behave identically.
- No persistence: nothing is saved, and there is no replay.
- No economic model beyond the declared chain.
- No user-submitted decisions reaching the engine. Submitted decisions are recorded and **never read
  by the tick loop**.
- No named RNG substreams, so adding a draw in one subsystem shifts every later draw everywhere.

## What it must never claim

- That it **predicts** anything. It describes what its rules produce.
- That its numbers correspond to any real place, organisation or person.
- That a decision was executed, or had a consequence. **Nothing is executed.**
- That reproducibility means accuracy. Same-seed-same-answer is a correctness property, not
  evidence about the world.
- That one scenario demonstrates a general capability.

## Key risks

- **Mistaking a readable sentence for a validated finding.** Every sentence on screen is derived
  from the run, but the run is a model of a fiction.
- **Under-dispersion** — the model may produce a narrower range of outcomes than reality. Untested;
  see [issue #26](https://github.com/CypherTechAries/project-meridian/issues/26).
- **Single-scenario overfit.** Rules tuned until one scenario looks right may not generalise, and
  nothing currently tests that.
- **Silent failure.** An action type absent from the effects table resolves to an empty delta with
  no error — a scenario can load cleanly and change nothing.

## Supporting research

[Belief read-model API](../design/BELIEF-READ-MODEL-API.md) ·
[VP-1 schema](../design/VP-1-SCHEMA.md) · [VP-2 current situation](../design/VP-2-CURRENT-SITUATION.md) ·
[VP-3 action selection](../design/VP-3-ACTION-SELECTION.md) ·
[VP-4 relationships and history](../design/VP-4-RELATIONSHIPS-AND-HISTORY.md) ·
[VP-5 read-only API](../design/VP-5-READ-ONLY-API.md) ·
[VP-6 Ask MERIDIAN](../design/VP-6-ASK-MERIDIAN-PHASE-1.md)

**Pending — not yet on `main`.** The first-user usability test record, the rebuilt plain-language
Briefing, and the removal of Analysis from primary navigation are on the unmerged branch
`fix/first-user-usability-reset`. **The "what exists today" list above describes `main`, which still
carries the pre-reset screens.** When that PR merges, this brief must be reviewed: the interface
description changes, and the usability-test link should be added.

## Next proof required

**Two, in order.**

1. **Make it understandable.** It failed its first usability test with a first-time user, who called
   the technical view "absolute nonsense". That work is under way and decides whether anything else
   matters.
2. **Load a second scenario and show it behaves differently for the right reasons.** Until then,
   "simulated-society engine" describes one crisis in one fictional strait.
