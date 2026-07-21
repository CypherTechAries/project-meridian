# Real-Geography Scenarios

**Status: UNDER RESEARCH**
**Last reviewed: 21 July 2026** (against `main` at `38e81b7`)

> **NOT IMPLEMENTED.** MERIDIAN's map is an invented diagram drawn in hand-written SVG. There is
> **no** map library, **no** geodata, **no** real geography, **no** projection, **no** tile source
> and **no** geography manifest. The engine has **no concept of space at all** — nothing in the
> causal chain reads a distance, a route or a location.
>
> **No dependency was added and no map code was written by this research.**

## In one sentence

Set fictional societies on real physical geography — real coastlines, terrain, distances and
transport networks — while keeping every government, organisation, person and event invented.

## The problem

MERIDIAN's current map failed its first cold usability test. A first-time reader found it artificial
and could not say what it meant, and it is now hidden behind a control with a stated limitation.

The deeper problem is that an invented coastline carries no intuition. The reader has no prior
knowledge to bring, so every fact — that this route is longer, that this port matters, that this
detour is expensive — has to be stated in words. That is how you end up with a decorative diagram
nobody can read in five seconds.

## How MERIDIAN could help

Use real geography as the physical stage and keep the society fictional.

> **GEOGRAPHICALLY REAL, INSTITUTIONALLY FICTIONAL**

A reader looking at a real strait already knows that going the long way round takes longer. That
understanding is free, and it is exactly what the map has to deliver.

**Real:** geography, distance, terrain, transport networks, physical constraints.
**Fictional:** identities, organisations, political systems, relationships, decisions, events,
economic conditions, outcomes.

## A simple example

A blockade closes a channel. The map shows the blocked route, the longer way round, and the two
ports that depend on the channel — on real coastline, with invented names. The reader understands
the physical situation immediately. The government, the shipping companies, the port authority and
everyone affected are invented, and the interface says so.

## Who might use it

Crisis and resilience planners; logistics and supply-chain analysts; emergency planners; training
providers. The strongest fit is **anywhere physical constraint is the subject** — distance, route
and capacity.

## What MERIDIAN already has

- A working SVG rendering approach that `d3-geo` would extend rather than replace.
- Declared fictional-world metadata on every response — the pattern the geography manifest follows.
- An origin vocabulary and an absence vocabulary that already refuse to render absence as zero.
- A persistent, non-dismissible fictional-simulation disclosure.
- A demonstrated willingness to state a limitation on screen rather than hide it — the map already
  says it has not passed the five-second test.

**That is all.** None of it is geographic.

## What is still missing

Everything: geodata; a projection; a rendering path for real geometry; the geography manifest;
geography modes; alteration marking; a bounded layer set; a legend component; sensitive-location
review; attribution rendering; version pinning; and any spatial concept in the engine.

## What it must never claim

- That a scenario **predicts** anything about a real location, its government, its institutions or
  its people.
- That real geography makes the **simulation** more accurate. It makes the *stage* accurate. The
  behaviour on the stage is exactly as invented as before.
- That renaming a place makes it **unidentifiable**. Coastline shape is among the most recognisable
  data in existence.
- That MERIDIAN holds real-world **operational** information.
- That any real organisation, official or resident is represented, consulted or implicated.

## Key risks

- **False authority — the defining risk.** A real coastline is checkable and true, so readers extend
  that trust to the fiction drawn on it. Recognition does the persuading, and **no disclaimer
  competes with recognition.** This can be reduced but not closed.
- **Accidental representation of real institutions.** In a small region there is often exactly one
  port operator, and renaming does not fix a role that maps one-to-one.
- **Map detail overwhelming the reader** — the exact failure that started this work. Real basemaps
  are dense, and showing everything available is the path of least resistance.
- **Leakage from FORSYTE.** The only risk here whose containment does not work after the fact:
  publishing is permanent, and it would combine a proprietary-licence breach, GPLv3 contamination and
  a possible export-control event.
- Political sensitivity; outdated data; licensing breach; commercial-provider dependency;
  simulated and operational layers becoming confused.

**Three risks sit on the critical path — false authority, FORSYTE leakage, and map detail — and none
is closed.**

## Supporting research

[Real Geography, Fictional Worlds](../research/REAL-GEOGRAPHY-FICTIONAL-WORLDS.md) — the main report ·
[Mapping stack and data sources](../research/MAPPING-STACK-AND-DATA-SOURCES.md) ·
[FORSYTE map reuse assessment](../research/FORSYTE-MAP-REUSE-ASSESSMENT.md) ·
[Risk register](../research/REAL-GEOGRAPHY-RISK-REGISTER.md) ·
[Scenario Geography Manifest](../design/SCENARIO-GEOGRAPHY-MANIFEST.md) ·
[Kestral Strait map direction](../design/KESTRAL-STRAIT-MAP-DIRECTION.md) ·
[Clean-room implementation plan](../design/CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN.md) ·
[Issue #30](https://github.com/CypherTechAries/project-meridian/issues/30)

## Next proof required

**One afternoon, one reader, no dependency.**

Redraw the Kestral map as an **abstract diagram** showing only the blocked route, the alternative
route and two or three affected ports — no geodata, no map library, no licence surface. Put it in
front of someone who has not seen MERIDIAN and ask them to explain it after five seconds.

**If it passes, MERIDIAN does not need a mapping stack for this scenario**, and avoids the
false-authority risk entirely. **If it fails, that is decisive**: the failure is one of category
rather than execution, and real geography is the answer. Only then is the second proof worth
building — one real geographic base area, fictional names, static data only, the same engine state,
no engine changes.

The cost of finding out is a few hours, and it is the cheapest decisive experiment available.
