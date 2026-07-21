# Training, Exercises and Wargaming

**Status: FUTURE DIRECTION**
**Last reviewed: 21 July 2026** (against `main` at `bfd2aa7`)

> **NOT IMPLEMENTED.** Nothing exercise-specific exists. There is no scenario authoring, no
> participant roles, no facilitation, no replay, no after-action review, and **no multiplayer**.
> The engine and one fictional scenario exist; everything that would make them an exercise does not.

## In one sentence

Repeatable fictional exercises where participants explore decisions, consequences, information gaps
and competing organisational pressures.

## The problem

Crisis exercises are expensive to write, hard to repeat consistently, and usually resolved by a
facilitator's judgement. Two teams running "the same" exercise often face different worlds, so their
outcomes cannot be compared. And most exercises give participants clean information, which is the
one thing a real crisis never provides.

## How MERIDIAN could help

The engine already does the two things an exercise most needs: it is **deterministic**, so the same
scenario behaves identically for every team, and it tracks **who knew what, when** — including the
difference between someone who rejected information and someone who never received it.

**And this is the one use where the fiction is a feature, not a liability.** A training scenario is
*supposed* to be invented. Nothing has to cross the boundary between simulation and reality, so the
central risk of every other use case — mistaking simulated results for evidence — largely does not
arise.

## A simple example

Two teams run the same fictional blockade. Both see political pressure rising. One is told about a
disputed claim on day two; the other is not told until day five. Afterwards, the exercise can show
each team exactly what they knew at each point, what the engine did in response to their situation,
and where the two runs diverged — from records, not from a facilitator's recollection.

## Who might use it

Emergency services and resilience teams; corporate crisis and continuity teams; public-sector
planners; universities teaching crisis management; anyone who currently writes tabletop exercises by
hand.

## What MERIDIAN already has

- A deterministic engine: same seed and inputs produce the same run.
- One fictional scenario with a ten-stage causal chain.
- **Information-exposure records**, and the distinction between *not received* and *rejected*.
- Append-only belief and information histories.
- Government options that change status as pressure builds.
- A plain-language briefing view.
- Ask MERIDIAN Phase 1 for querying the situation in eight declared ways.

## What is still missing

Everything that makes this an exercise product rather than a simulation:

- **Scenario authoring tools.** Scenarios are hand-written files; one exists.
- **Participant roles.** No concept of a participant at all.
- **Facilitation** — no injects, no controller view, no pacing.
- **Replay.** Nothing is persisted.
- **Exercise objectives** and any way to assess whether they were met.
- **After-action review.**
- **Multiplayer.** MERIDIAN is single-user. There is no session, no shared state, no concurrency.
- Any way for a participant decision to reach the engine — submitted decisions are recorded and
  **never read by the tick loop**.

## What it must never claim

- That it is a **wargame**. It has no adversary, no turns, no adjudication.
- That it supports **multiple participants**. It does not.
- That exercise performance says anything about real-world readiness.
- That the scenario represents any real place, organisation or event.
- That an exercise outcome is a prediction.

## Key risks

- **Overclaiming to a serious buyer.** Emergency services and defence buyers know what a wargame is.
  Describing this as one, before roles, injects and adjudication exist, would be caught immediately
  and would cost credibility that is hard to recover.
- **Facilitator substitution.** A deterministic engine can make an exercise *feel* authoritative
  while modelling very little. The engine's boundaries must be visible to participants.
- **Content, not code, is the real cost.** Good exercises are good because of their scenarios. That
  is writing work, and it does not get cheaper because the engine is deterministic.
- **Single-scenario limitation.** Every exercise would currently be the same crisis.

## Supporting research

The entity-graduation research examined this as a commercial direction and rated it **the strongest
of twelve models** — because fiction is the intended form and no truth boundary is crossed:
[Simulation-Born Entities §12 and §13D](../research/SIMULATION-BORN-ENTITIES.md).

The narrative research identified **fictional misinformation exercises** as one of two uses needing
none of the risky capability: [Narrative and Incentive Intelligence §23](../research/NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md).

## Next proof required

**Someone paying for a scenario.** Not a pilot, not a letter of intent — a real exercise, run once,
for money, with a written account of what the participants got that a hand-written tabletop would
not have given them.

That test needs no multiplayer, no authoring tools and no new engine capability. It needs one good
scenario and one willing customer, and it would tell us more than a year of building would.
