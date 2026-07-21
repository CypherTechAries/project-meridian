# Simulation-Born Entities

**Status: FUTURE DIRECTION**
**Last reviewed: 21 July 2026** (against `main` at `bfd2aa7`)

> **MERIDIAN cannot currently graduate entities.** It cannot export an entity, and it has no concept
> of an entity that outlives a run. There is **no** code for ownership, permissions, lineage,
> graduation, revocation, validation envelopes, economic accounts or external connectors.

## In one sentence

Preserve useful organisations, products, processes or characters created in simulation, and
potentially export them as real-world blueprints, operating models or intellectual property.

## The problem

MERIDIAN invents companies, products and institutions, and gives them histories. Those inventions
stop existing when the run stops. Some of them are designed carefully, stress-tested repeatedly and
documented honestly — and then discarded.

## How MERIDIAN could help

Keep the ones worth keeping. A fictional company that survived repeated crises is not a business,
but it may be a **design**: a brand, a set of written procedures, an organisational shape, a product
specification, working software, a body of test scenarios — and, most valuable of all, **a record of
how it failed**.

> **A simulation can produce a blueprint. It cannot produce a business.**

## A simple example

A fictional freight cooperative survives repeated supply-chain crises. What could cross into
reality: its brand, its written cooperative rules, its dispatch procedure, its product concept, and
the record of the four simulated runs where it ran out of cash and the two where its voting rule
deadlocked.

What cannot cross: its revenue, its members, its customers, and any claim that the model works. The
only question that matters next — *would one real haulier join on those terms?* — is unanswered by
every hour of simulation.

## Who might use it

Founders developing an organisational design cheaply before committing; product teams using
simulation as a design workshop; training providers exporting fictional institutions as teaching
material.

## What MERIDIAN already has

- **Typed fictional entities** whose identifier carries the fictional world — `fict:<scenario>:<kind>:<entity>`.
- **Engine / fixture origin separation** on every record.
- **Append-only histories**, so a record cannot be quietly rewritten.
- **Declared model boundaries** — a working vocabulary for "we did not model this".
- **Decisions selected but never executed.**
- **B5 controls** — no protected-trait targeting, no persuasion optimisation.
- Read-only dossiers.

All of it exists **within a run**. Nothing persists across scenarios.

## What is still missing

- **Persistent cross-run entities.** Entities exist inside a run and end with it.
- **Asset manifests** — no export format of any kind.
- **Ownership** records.
- **Permissions** — no permission model exists.
- **Legal-wrapper records.**
- **Validation envelopes.**
- **Connectors** — no route to anything outside MERIDIAN.
- **Revocation** and shutdown.
- Organisations are aggregates, not modelled entities. **Products do not exist as a type at all.**
- The typed-ID system currently refuses any kind other than `person` for virtual people.

## What it must never claim

- That **simulated performance is real performance**. A simulated business is a blueprint, not a
  company.
- That simulated revenue, customers, reputation, competence or regulatory approval transfer. **They
  do not.**
- That a graduated entity has legal personality. A **simulated entity or software system does not
  itself have legal personality under UK law** — real-world operation would need an existing legal
  person, with accountable humans in the roles the law reserves to natural persons.
- That it is a **digital twin**. Under the international standards a digital twin requires a
  specific real counterpart and a live data connection. Association is not twinning.
- That an entity can consent, hold rights, or be responsible for anything.

## Key risks

- **Simulation overconfidence** — the central risk. A fictional company with five years of invented
  history reads exactly like a real one, and documents do not stop belief.
- **Weak IP protection where it matters most.** Assets are likely least protected exactly where they
  are most machine-generated; trade mark rights follow **actual trading**, not simulation richness.
  **IP strategy must precede public exposure of entity names.**
- **Reputation laundering** — simulated reputation presented as real.
- **Acting outside the validation envelope**, which is unsolved for anything but narrow domains.
- Six of seven risks identified as uncontrolled sit on this concept's critical path.

## Supporting research

[Simulation-Born Entities](../research/SIMULATION-BORN-ENTITIES.md) — the full 21-section report ·
[Entity graduation lifecycle](../research/ENTITY-GRADUATION-LIFECYCLE.md) ·
[Graduation Evidence Pack](../research/GRADUATION-EVIDENCE-PACK.md) ·
[Risk register](../research/ENTITY-GRADUATION-RISK-REGISTER.md) ·
[Source register](../research/SIMULATION-BORN-ENTITY-SOURCES.md) ·
[Concept note](../design/ENTITY-GRADUATION-CONCEPT.md)

## Next proof required

**A static export, read by a human, with nothing automated.**

Take **one simulated organisation or process** — explicitly **not a person**. Produce a static
Graduation Evidence Pack: identity, brand, goals, procedures, decision history, **failures**,
assumptions, specification, and a permission manifest with **no external permissions at all**. A
human reads it and builds one harmless artefact by hand — a landing page, a handbook, a training
exercise.

It answers one question: **does the pack tell a human something they could not have got faster from
a conversation?**

**A "no" is a good result.** It would save years.
