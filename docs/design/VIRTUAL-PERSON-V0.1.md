# Virtual Person v0.1 — design proposal

**DESIGN ONLY. No engine behaviour added.** This document is a reviewed design proposal on the
`design/virtual-person-v0.1` branch, created from `main` after PR #15 merged. It defines what would
be built; it builds nothing. No `virtual-person@0.1` code, fixture, transition or test exists in the
engine — the schemas and traces below are illustrative.

## Goal

The smallest believable fictional person MERIDIAN can simulate **honestly** — more than a name, a
portrait, a role and one belief number. It must be able to answer: what does this person know, want,
fear; who do they know; what happened to them; what did they consider; why did they act; what
changed.

**And it must never turn appearance, background, education, occupation or wealth into a shortcut for
intelligence, competence, morality or belief.** That rule survives from the belief slice unchanged.

## Four layers, kept structurally separate

A response must be unable to present one layer as another.

### 1 · FIXTURE IDENTITY — authored, never changes during a run

| Field | Origin |
|---|---|
| `person_id` (typed: `fict:<scenario>:person:<id>`) | FIXTURE |
| `display_name` | FIXTURE (**PROPOSED** until adopted) |
| `portrait_ref` | FIXTURE (**PROPOSED**; may be null — none exist yet) |
| `life_stage` (band, not a number) | FIXTURE |
| `role`, `organisation`, `home_community` | FIXTURE |
| `biography` (short, inert prose) | FIXTURE |

Biography and role are **display-only**. A test must prove they cannot reach any calculation — the
`test_descriptive_metadata` invariant, extended.

### 2 · ENGINE STATE — authoritative, changes only through the transition boundary

| Field | Notes |
|---|---|
| `goals` (2–3, ordered, **no numeric weight**) | A weight implies optimisation |
| `responsibilities` | Institutional obligations that constrain action |
| `pressures` | Declared constraints — **never** a susceptibility or vulnerability score |
| `proposition_beliefs` | The existing belief slice, per proposition |
| `information_received` / `information_not_received` | Exposure history, by route and tick |
| `recent_events` | Append-only, ordered; **no decay, no effect on belief in v0.1** |
| `available_actions` | Options open to the person now |
| `selected_action` | What was chosen |
| `constraints_removing_options` | Why an option was unavailable |
| `relationships` | Typed edges (see below) |

### 3 · DERIVED EXPLANATIONS — computed from layers 1–2, never authored

Why a belief changed · why an action was selected · which pressures mattered · which information was
lacking · which constraint removed an option. These reuse the existing wording-band approach: keyed
by structured state, never by entity id.

### 4 · NOT MODELLED — returned explicitly, at equal weight

Complete lifetime history · full psychology · unconscious motivation · unrestricted memory ·
**changing trust** · **cumulative stress** · personalised feeds · complete social networks ·
**intelligence · competence · moral worth** · **susceptibility** · **persuadability**. Present in
every response's `not_modelled` list so a client cannot silently omit it. The last four are never
modelled at any version, not merely deferred — they are the belief slice's standing prohibition
carried up to the person.

## Proposed schema (illustrative)

```jsonc
{
  "schema": "virtual-person@0.1",
  "identity": {                                  // FIXTURE
    "person_id": "fict:kestral-strait:person:broadcast-journalist",
    "display_name": "Mara Venn",                 // PROPOSED FIXTURE
    "portrait_ref": null,                        // PROPOSED; none exists yet
    "life_stage": "adult-30s", "role": "Correspondent",
    "organisation": "fict:kestral-strait:organisation:public-broadcaster",
    "home_community": "Northshore",
    "biography": "Covers the strait for the public broadcaster.",
    "origin": "FIXTURE"
  },
  "state": {                                     // ENGINE
    "goals": [
      {"id": "g1", "text": "report only what is verified", "origin": "FIXTURE-declared"},
      {"id": "g2", "text": "protect the broadcaster's credibility", "origin": "FIXTURE-declared"}
    ],
    "responsibilities": ["uphold the publication standard"],
    "pressures": [{"id": "p1", "text": "needs a second source", "origin": "ENGINE-derived"}],
    "beliefs": [{"proposition_id": "P-WARNINGS-IGNORED", "credence_band": "unsure",
                 "history_ref": "belief-history:mara:P-WARNINGS-IGNORED", "origin": "ENGINE"}],
    "information": {
      "received": [{"event_id": "E-ALLEGATION-01", "route": "newsroom wire",
                    "direct": true, "tick": 6, "origin": "ENGINE"}],
      "not_received": [{"description": "no corroborating second source", "origin": "ENGINE"}]
    },
    "recent_events": [{"tick": 6, "text": "took the allegation off the wire", "origin": "ENGINE"}],
    "available_actions": [
      {"id": "a1", "text": "report as established", "available": false,
       "blocked_by": "c1"},
      {"id": "a2", "text": "hold pending corroboration", "available": true}
    ],
    "selected_action": {"id": "a2", "origin": "ENGINE"},
    "constraints": [{"id": "c1", "text": "publication standard requires more proof",
                     "removes": ["a1"], "origin": "FIXTURE-rule"}],
    "relationships": [
      {"type": "reports_to", "target": "fict:kestral-strait:organisation:public-broadcaster",
       "origin": "FIXTURE"}
    ]
  },
  "explanations": {                              // DERIVED
    "decision": {"ref": "decision-trace:mara:day6"}
  },
  "not_modelled": ["lifetime history", "complete psychology", "unconscious motivation",
    "emotional complexity", "unrestricted memory", "personalised feeds", "complete social networks",
    "intelligence", "competence", "moral worth"]
}
```

## State-transition proposal

All person-state change flows through the existing single mutation boundary (`TransitionService`
pattern), never directly. v0.1 transitions:

| Transition | Effect | Determinism |
|---|---|---|
| `EXPOSE(person, event)` | appends to `information.received`, records the route | deterministic |
| `UPDATE_BELIEF(person, proposition)` | the existing belief kernel; unchanged | deterministic |
| `RECORD_EVENT(person, text)` | appends to `recent_events`; **no belief effect in v0.1** | deterministic |
| `SELECT_ACTION(person)` | resolves `available_actions` against `constraints`, records choice | deterministic |

**Explicitly not in v0.1:** no cumulative-stress transition, no trust-change transition, no
event→belief coupling, no cross-person social transmission. Recent events are *recorded*, not yet
*causal* — that honesty is the whole point of v0.1.

## Decision-trace proposal

A deterministic trace answering the nine questions, each field origin-marked:

```jsonc
{
  "schema": "decision-trace@0.1", "person_id": "...", "tick": 6,
  "wanted":        ["report only what is verified", "protect credibility"],   // from goals
  "knew":          ["an allegation arrived over the wire"],                   // from information.received
  "did_not_know":  ["whether a second source would corroborate it"],         // from information.not_received
  "pressures":     ["the publication standard"],                             // from pressures
  "options":       ["report as established", "hold pending corroboration"],  // available_actions
  "removed":       [{"option": "report as established",
                     "by": "publication standard requires more proof"}],     // constraints
  "selected":      "hold pending corroboration",
  "because":       "the only option the standard left open, given no corroboration",  // DERIVED
  "afterward":     "belief moved a small step; still short of established",   // from belief history
  "origin_note":   "biography and role were not inputs to this decision"
}
```

The last line is enforced structurally: the decision function's inputs are goals, responsibilities,
information, pressures, constraints and available actions. Its input signature **structurally
excludes** portrait, biography, display name, occupation description, education, socioeconomic
description and life stage. A proposed test asserts the signature excludes every one of them,
mirroring the belief-kernel invariant. Biography may provide *visible context* in the dossier, but
it can never become an input to the calculation.

## Relationship model — typed edges, no universal score

```jsonc
{"type": "reports_to",   "target": "<org id>",    "origin": "FIXTURE"}
{"type": "member_of",    "target": "<org id>",    "origin": "FIXTURE"}
{"type": "represents",   "target": "<cohort id>", "origin": "FIXTURE"}
{"type": "colleague",    "target": "<person id>", "origin": "FIXTURE"}
{"type": "trusts_for",   "target": "<source>",    "subject": "<proposition/topic>", "origin": "FIXTURE"}
{"type": "receives_from","target": "<source>",    "origin": "ENGINE"}
```

**No single "influence score."** Trust is `trusts_for` — bound to a declared subject, exactly as the
belief slice already scopes source trust per proposition. A relationship is a stated edge, never a
number that ranks how manipulable someone is.

## Information-history model

Ordered, append-only, per person: `{event_id, proposition_id, route, direct|relayed, tick,
origin}`. `not_received` carries `{description, origin}` — the absence is first-class, so "never
heard it" stays distinct from "heard and rejected it", which is the belief slice's core honesty
property carried up to the person.

## Belief-history model

Per `(person, proposition)`: an ordered list of `{tick, credence_band, confidence_band, event_id,
origin}`. v0.1 will usually hold **one** entry, because the current kernel updates once — and the
history says so rather than implying a trajectory that was never computed.

## Current vs unmodelled

| Answerable in v0.1 | Not modelled in v0.1 |
|---|---|
| Who is this person (fixture identity) | Their lifetime before the scenario |
| What they want (declared goals) | Unconscious or hidden motivation |
| What pressure they are under | Cumulative stress over time |
| What information they received / did not | Personalised information feeds |
| Why a belief changed | Emotional complexity |
| What options they had and which were removed | The full space of possible actions |
| Why they chose an action | Trust that changes over time |
| Their typed relationships | Complete social network |
| What MERIDIAN does not know about them | Intelligence, competence, moral worth (never modelled) |

## Implementation milestones (proposed, post-merge)

1. **VP-1 Schema + fixtures** — `virtual-person@0.1` types; author the three existing people. No behaviour.
2. **VP-2 State + transitions** — the four transitions through the mutation boundary; belief kernel reused unchanged.
3. **VP-3 Decision trace** — the deterministic trace; input-signature invariant test.
4. **VP-4 Relationships + histories** — typed edges, information and belief history.
5. **VP-5 API exposure** — extend the read-model API (PR #15's projection layer) with a person-state projection; same origin/absence rules.
6. **VP-6 Ask MERIDIAN Phase 1** — deterministic structured answers to "who is this / what do they want / why did they act / what does MERIDIAN not know", no LLM.

## Estimated test additions

~55–75 tests: schema/origin (~12), transitions incl. determinism and mutation-safety (~15),
decision-trace correctness + biography-exclusion invariant (~12), relationships incl. no-universal-
score (~8), information/belief history incl. absence-not-zero (~10), API projection parity + jargon/
layer checks (~12). Rough; firmed up per milestone.

## Ask MERIDIAN connection

VP v0.1 is what lets Phase 1 answer, deterministically: who is this person · what are they trying to
achieve · what pressure are they under · what information have they received · why did their belief
change · why did they choose this action · who shaped the information they got · what does MERIDIAN
not know about them. **The engine stays the authority; a later LLM may translate questions and
explanations but must never invent person state.**

## Portraits

**Portrait work remains deferred.** MERIDIAN may use manually selected temporary portrait assets for
recognisable fictional identities; automated character-image generation is deferred until population
scale makes it necessary. No Colab, hosted image API, ComfyUI, Character Foundry, Blender or
model-licensing work is restarted, and **no portrait asset is created on this branch.** `portrait_ref`
is a nullable FIXTURE field and is currently null for all three people — none exists.

## History semantics — the four states kept distinct

Information history must never collapse these into one another:

| State | Meaning |
|---|---|
| **never received** | no route carried the claim to this person |
| **received but remained unsure** | encountered it; credence sits in the uncertain band |
| **received and rejected** | encountered it; credence moved against |
| **received and accepted** | encountered it; credence moved toward |

Ordered, append-only, origin-aware. **A single recorded update must not be rendered as a
trajectory** — where belief history holds one entry, the response says so.

## Confirmation

**No Virtual Person engine behaviour was implemented during this design step.** This is a proposal
document only. The belief kernel, fixtures and frozen commits are untouched, and no
`virtual-person@0.1` type, transition, fixture or test exists in the engine.
