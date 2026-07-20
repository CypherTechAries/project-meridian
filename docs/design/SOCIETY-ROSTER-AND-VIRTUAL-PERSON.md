# Society Roster, revised dossiers, and Virtual Person v0.1 — design for review

**DESIGN ONLY. Nothing here is implemented.** No frontend code, no engine change, no new
simulation behaviour, no real-person data of any kind.

Source: [`mockups/roster-and-dossiers.html`](mockups/roster-and-dossiers.html)

## The finding that governs everything below

**The engine holds no names.** `cast.py` declares `display_name: "Correspondent, Northshore
Broadcast"` — a role label. There is no name, no age, no household, no goal, no pressure, no
relationship and no history for any person.

So "Mara Venn", her portrait, her priority and her pressure are **proposals**, not data. Every one
carries a violet `P` marker meaning *proposed — does not exist yet*, distinct from `F` (in the story
today) and `E` (engine result). Without that distinction the revised dossier would look four times
deeper than the engine actually is, which is the exact failure the correction warns against.

## 1–5. The five mockups

| # | Screen | File |
|---|---|---|
| 1 | Society Roster | [`v2-1-society-roster.png`](mockups/v2-1-society-roster.png) |
| 2 | Person Dossier — Mara Venn | [`v2-2-person-dossier-mara-venn.png`](mockups/v2-2-person-dossier-mara-venn.png) |
| 3 | Organisation Dossier | [`v2-3-organisation-dossier.png`](mockups/v2-3-organisation-dossier.png) |
| 4 | Population Group | [`v2-4-population-group.png`](mockups/v2-4-population-group.png) |
| 5 | Society Belief Landscape | [`v2-5-belief-landscape.png`](mockups/v2-5-belief-landscape.png) |

### What changed

**People became people.** Portrait, name, role, organisation, priority, pressure and latest event —
scannable in a card, deeper one click away. The dossier now opens on *"Why she acted as she did"*
rather than on a belief delta.

**Groups became unmistakably groups.** A population group's symbol is **many small marks, never one
figure and never one face**. Every group card carries a `GROUP-LEVEL MODEL` chip. The population
screen states the caveat four times — banner, kind label, headline, closing note:

> On average, the port-worker group moved a little towards the claim. **MERIDIAN does not yet know
> how individual port workers differ.**

**Absence became structural.** Three ghosted panels — Relationships, Recent History, What MERIDIAN
Does Not Know — occupy a full row at the same visual weight as the results, hatched and labelled
`NOT MODELLED`.

**The landscape became character-led.** Three portraits carry the story. Twelve text cards are gone;
in their place, a `HOW THE CLAIM TRAVELLED` path showing direct hops, relays and the group no route
reached. Filters replace scrolling.

**Organisations gained one honest line:** *"These are declared groups, not named people. MERIDIAN
does not model who inside holds which view."*

### Portraits

Original geometric vector art, drawn as inline SVG. **Deliberately not photorealistic** — a
photographic face would imply a real person, which the fictional-world controls exist to prevent.
No Metal Gear Solid asset, visual identity or trade dress is used or referenced.

**Honest assessment:** the portraits are the weakest element. At roster size they read closer to
a friendly avatar than to a character in a serious simulation. They prove the *layout* — that a
portrait-led roster works — but they are not the final art. A real character-art pass should
replace them: stronger silhouettes, more individuality, less symmetry, no smile.

## 6. Field-by-field source

`E` engine · `F` fixture today · **`P` proposed, does not exist** · `?` not modelled

### Person dossier

| Field | Source |
|---|---|
| Role label, biography, organisation | `F` |
| Claim, prior view, current view, movement, confidence | `E` |
| Received / not received, exposure path | `E` + `F` |
| Reason 1 (verification rule) | `F` threshold rationale |
| Reasons 2–3 (evidence strength, prior distance) | `E` band reading |
| "Why she acted" headline | `E` derived |
| **Name, portrait, community** | **`P`** |
| **Priority, pressure, goals, responsibilities** | **`P`** |
| Life stage, household | `?` |
| Relationships, recent history, memories, emotions, stress, changing trust | `?` |

### Organisation dossier

| Field | Source |
|---|---|
| Name, biography, objectives | `F` |
| Internal blocs, cohesion, official position, strength, direction, force, derivation | `E` |
| Emblem | `P` |
| Internal politics, past decisions, named individuals inside | `?` |

### Population group

| Field | Source |
|---|---|
| Name | `F` · population, exposure, average before/after, change | `E` |
| Symbol | `P` |
| Internal breakdown | `?` `UNAVAILABLE` · confidence | `?` `NOT_MODELLED` |

### Roster and landscape

Names and portraits `P`; statuses and the travel path `E`; roles and organisation names `F`; the
substitution claim `E` and test-verified.

## 7. Virtual Person v0.1 — minimum engine requirements

The smallest layer that supports the dossier honestly. **Not memory, not path dependence, not
psychology.**

| # | Requirement | Notes |
|---|---|---|
| 1 | **Stable fictional identity within a run** | id, name, portrait ref. Does **not** claim persistence across runs |
| 2 | **Declared identity fixtures** | role, organisation, community, short biography — all `FIXTURE` |
| 3 | **Goals** | declared, ordered, no numeric weight — a weight would imply optimisation |
| 4 | **Responsibilities** | institutional obligations that constrain action |
| 5 | **Current pressures** | declared constraints; **never** a susceptibility or vulnerability score |
| 6 | **Declared relationships** | typed edges (employs, represents, reports to). Not trust, not influence |
| 7 | **Recent-event records** | append-only, ordered, no decay and no effect on belief in v0.1 |
| 8 | **Information-exposure history** | what reached them, by which route, when |
| 9 | **Proposition beliefs** | already exists |
| 10 | **Decision records** | what was chosen, from which options, under which constraints |
| 11 | **Reasons and constraints** | structured, derived, not authored prose |
| 12 | **Per-field origin** | every field carries `ENGINE` / `FIXTURE` / `UNKNOWN` / `UNAVAILABLE` |

**Four separations enforced structurally, not by convention:** fixture identity · engine state ·
derived explanation · unmodelled absence. A dossier response must be unable to present one as
another.

**Prohibited in v0.1 and after:** background, education, occupation or wealth as a shortcut for
competence, intelligence, morality or belief. Any susceptibility, persuadability, influence-rank or
conversion field. Any real-person data.

## 8. Sections that cannot yet be populated honestly

| Section | Status | Needs |
|---|---|---|
| Name, portrait, visual identity | **Cannot** | v0.1 #1–2 |
| Community, household, life stage | **Cannot** | v0.1 #2 |
| Goals, responsibilities, pressures | **Cannot** | v0.1 #3–5 |
| Relationships | **Cannot** | v0.1 #6 |
| Recent events, previous decisions | **Cannot** | v0.1 #7, #10 |
| Information timeline beyond one event | **Partial** | one event exists; a timeline needs #8 |
| Conflicting information | **Cannot** | needs a second event |
| Belief history | **Cannot** | one update exists, so there is no history |
| Accumulated pressures | **Cannot** | needs cumulative state — deliberately out of scope |
| Emotional state | **Cannot** | not in scope |
| Why they acted | **Available now** | derived from threshold, evidence, prior |
| Belief before/after, confidence, exposure | **Available now** | `E` |
| Organisation internal vs official | **Available now** | `E` |
| Group average and unavailable breakdown | **Available now** | `E` |

**Seven of the fourteen desired sections cannot be populated at all today.** That is why the
mockups show them ghosted rather than filled with plausible text.

## 9. Navigation

```
  BRIEFING          SOCIETY                    ANALYSIS
     │                 │                          │
     │        ┌────────┴────────┐                 │
     │        │  Society Roster │◄────────────────┘  (by entity id)
     │        └────────┬────────┘
     │                 │ select a portrait, emblem or group
     │        ┌────────┴────────────────────────┐
     │        │ Person / Organisation / Group   │
     │        │ Dossier    ‹ SOCIETY to return  │
     │        └────────┬────────────────────────┘
     │                 │ "see everyone's response to this claim"
     │        ┌────────┴────────┐
     └───────►│ Belief Landscape│  ← one entry point from Briefing
              └─────────────────┘
```

**Roster is the Society landing screen**, not the Landscape: *who is in this society* precedes *how
they reacted to one claim*. The Landscape is claim-scoped and belongs one level in. No modals — a
dossier is a place.

## 10. Public hero and demo

**Hero: keep the Briefing View.** It is the product's front door and the only fully implemented
screen. **Second image should become the Society Roster** once built — it communicates "a society of
people you can inspect" in one glance, which is the differentiator. Analysis moves third.

Do not use these mockups as README screenshots. They are labelled `DESIGN MOCKUP — NOT IMPLEMENTED
SOFTWARE` for that reason.

**Demo, about four minutes:**

1. **Briefing** — a blockade, and what it does to people.
2. **Counterfactual** — remove one step, watch downstream collapse.
3. **Society Roster** — "this is who lives here." Portraits, names, roles.
4. **Belief Landscape** — one claim enters. Three portraits, three different results.
5. **Mara Venn's dossier** — "why is she still unsure?" End on the three ghosted panels.
6. **Port workers** — "and this is a group, not a person. We know the average; we do not know the
   people."

Ending on two different kinds of ignorance — what we do not know about a person, and what we cannot
know from an average — is the most credible note available, and the hardest for anyone else to
imitate honestly.

## AI data boundary

Recorded as binding. MERIDIAN is **not** designed around importing private real-person AI
conversation histories. The public platform remains fictional-only.

AI may later assist with **fictional** biography generation, dialogue, memory summaries,
interpretation and proposed actions. **Authoritative state remains owned by the deterministic
engine** — an assisting model may propose, never decide.

**Never introduced:** real-person personality profiling · inferred private vulnerabilities ·
susceptibility scores · persuasion targeting · audience optimisation · real-population behavioural
maps. Any future real-data research would require separate explicit consent, privacy, deletion and
governance controls, and is outside the current public scope.

## Sequencing

1. **Belief read-model API** — PR #15, done, awaiting review. Foundational and independent of these
   mockups.
2. **Virtual Person v0.1 data boundary** — specified above, not built.
3. **Revised visual mockups approved** — this document.
4. **Then** frontend implementation.

**No frontend work has begun and none should begin until 1–3 are settled.**
