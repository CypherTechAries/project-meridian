# Entity graduation — concept note

**Status: CONCEPT ONLY.** Nothing described here exists. MERIDIAN cannot graduate an entity today
and is a long way from being able to. This note explains the idea and where it might eventually
fit; the detailed research is in [docs/research/SIMULATION-BORN-ENTITIES.md](../research/SIMULATION-BORN-ENTITIES.md).

---

## The idea in one paragraph

MERIDIAN invents things: companies, people, products, institutions, and the histories that go with
them. Right now those things exist only inside the simulation and stop when the run stops. The idea
is that some of them might be worth keeping — that a fictional company which was designed carefully,
stress-tested repeatedly and documented honestly is not just a story, but a **design**. Entity
graduation is the controlled process of taking the parts of such an entity that can survive contact
with reality — the brand, the written procedures, the product specification, the software — and
using them to build something real, while leaving behind the parts that cannot: the invented
revenue, the invented customers, the invented track record.

## The idea in one sentence

**A simulation can produce a blueprint. It cannot produce a business.**

---

## Why it is interesting

Most simulations are consumed and discarded. Their output is a report. If MERIDIAN's entities are
persistent, versioned, and carry an honest record of what was tested and what failed, then the
simulation stops being a report generator and becomes something closer to a **design workshop** —
somewhere you can develop an organisation or a product cheaply, break it many times, and only then
decide whether to build it.

That reframing is worth more than any individual graduated entity. It changes the answer to "what is
MERIDIAN for?" from *understanding a crisis* to *designing things that have to survive one*.

## Why it is dangerous

The same properties that make it interesting make it a very effective way to mislead people,
including ourselves.

A fictional company with five years of invented history, invented customers and invented revenue
reads exactly like a real one. Hand that document to an investor, a partner or a journalist and the
fiction does not announce itself. The most likely failure of this concept is not a technical one —
it is that somebody, in good faith, comes to believe that a thing which was tested in a model was
tested in the world.

MERIDIAN's whole value rests on being careful about what it claims. This concept puts commercial
pressure on exactly that. It should only be built by a project that is willing to make the resulting
product less impressive on purpose.

---

## What crosses, and what does not

| Crosses | Does not cross |
|---|---|
| Brand, name, visual identity | Simulated revenue |
| Written procedures and policies | Simulated customers and demand |
| Organisational design | Simulated reputation |
| Product specifications and requirements | Simulated competence or track record |
| Software | Simulated regulatory approval |
| Test scenarios and training material | Simulated legal authority |
| The record of what failed | Any claim about a real thing |

The right-hand column is the more important one, and every honest version of this product has to put
it in front of the reader, not in an appendix.

---

## What it is not

**It is not a digital twin.** A digital twin is a model of *one specific real thing* — this port,
this factory — kept in step with it and validated against it. A simulation-born entity has no real
counterpart to be a twin of. Calling an exported fiction a digital twin borrows credibility the
thing has not earned, and the research report sets out the standards definitions that make this a
real distinction rather than a preference about words.

**It is not a claim to legal personhood.** A graduated entity is never the legal actor. A real
company or a real person owns the assets, signs the contracts and carries the responsibility. The
entity is a collection of assets and software operated by somebody accountable.

**It is not autonomy.** Nothing in this concept requires — or permits — an entity to act on its own.
The safest and most valuable version has a human deciding everything that touches the world.

---

## How it would fit MERIDIAN

MERIDIAN already has, and did not build for this reason, several things this concept needs:

- Entities with stable, typed identifiers that carry their fictional world in the identifier itself.
- A strict separation between what the engine produced and what a human authored.
- Decisions that are selected and explicitly **never executed** — a boundary this concept would have
  to preserve.
- Append-only histories, so a record cannot be quietly rewritten.
- Declared model boundaries: a vocabulary for saying "not modelled" rather than implying zero.
- Read-only interfaces to entity records.
- Controls that refuse protected-trait targeting and persuasion optimisation.

It is missing everything else: persistent entities across scenarios, organisations and products as
first-class things, ownership, permissions, lineage, validation, and any notion of the outside world.
That gap is years of work, not months, and most of it is not simulation work at all.

---

## The safest first experiment

Deliberately unexciting, and chosen because it can fail cheaply.

1. Take one simulated **organisation or product** — not a person.
2. Export a static Graduation Evidence Pack: identity, brand, goals, procedures, decision history,
   failures, assumptions, specification, and a permission manifest containing **no permissions at
   all**.
3. A human reads it and builds one harmless real artefact by hand — a landing page, a handbook, a
   training exercise, a small internal tool.
4. Compare the real result with the simulated design and write down where the fiction was useful,
   where it was misleading, and what it did not tell us.

No software leaves the building. No account, no email, no money, no publication. The experiment's
purpose is to answer one question — *does the pack tell a human anything they could not have got
faster from a conversation?* — and a "no" is a perfectly good result that saves years.

---

## Where this should sit

Not on the roadmap. The current work — making the product understandable to a first-time user — is
the thing that determines whether MERIDIAN is worth anything at all, and it is unfinished. This
concept is worth keeping as a written direction because it changes how the entity model should be
designed *when it is designed*, and that is a reason to have read it, not a reason to start it.

The full recommendation, with the reasoning and the sources, is in the research report.
