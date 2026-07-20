# Conversational command interface — design for review

**DESIGN ONLY. Nothing here is implemented.** No conversational UI, no live language model, no
cabinet dialogue, no person dialogue, no conversation memory, no natural-language planning and no
natural-language command path exists in MERIDIAN today.

Mockups: [`v4-1-ask-meridian-home.png`](mockups/v4-1-ask-meridian-home.png) ·
[`v4-2-what-is-going-on.png`](mockups/v4-2-what-is-going-on.png) ·
[`v4-3-why-is-mara-unsure.png`](mockups/v4-3-why-is-mara-unsure.png) ·
[`v4-4-cabinet-room-future.png`](mockups/v4-4-cabinet-room-future.png) ·
source [`conversational-interface.html`](mockups/conversational-interface.html)

## The two rules

> **Chat is the doorway. Visuals are the evidence. The deterministic engine is the authority.**

> **The user should be able to ask an embarrassingly simple question without feeling embarrassed.**

"What the hell is going on?" is a first-class supported request. It appears as a *starter* on the
empty home screen — not as a fallback for when someone fails to find the right dashboard.

## Chat-first, not chat-only

The conversation does not replace the screens. It summons them. **The same component renders in
three places** — inline in a reply, in the right-hand context panel, and full-screen — so a person
card in a chat answer is the same object as a person card on the roster. That constraint is what
stops the chat becoming a parallel, weaker product with its own drifting vocabulary.

## Layout

```
┌─ FICTIONAL SIMULATION ────────────────────────────────────────────────┐
│ MERIDIAN · Kestral Strait · Day 5      [EXPLORE] [PLAN] [COMMAND]     │
├────────────┬────────────────────────────────────┬────────────────────┤
│ CONVERSATIONS │  conversation thread             │ CURRENT CONTEXT   │
│  Ask MERIDIAN │  · plain-English answer first    │  map              │
│  Cabinet   P  │  · then inline evidence cards    │  selected person  │
│ ─────────     │  · then follow-up chips          │  selected claim   │
│ SURFACES      │                                  │  run context      │
│  Briefing     │                                  │                   │
│  Society      │                                  │  follows the      │
│  People       │                                  │  conversation     │
│  Organisations│                                  │                   │
│  Events       │                                  │                   │
│  Analysis     │                                  │                   │
├────────────┴────────────────────────────────────┴────────────────────┤
│ Ask anything…                                              [SEND]     │
└──────────────────────────────────────────────────────────────────────┘
```

**Narrow screens:** the context column collapses into the thread. Context cards appear inline after
the answer they belong to, in the same order. Nothing is lost — only repositioned — because context
is composed of the same components.

## Three conversation types, never styled alike

| | Marker | Meaning |
|---|---|---|
| **MERIDIAN guide** | green `ENGINE RESULT` | Outside the fiction. Explains what the engine actually computed, and what it does not know |
| **Cabinet room** | violet `SIMULATED CHARACTER — NOT ENGINE TRUTH` | Inside the fiction. A character may be mistaken, biased, or working from incomplete information |
| **Direct person** | violet, plus a modelled-layer disclosure | Future. Must not be presented as a fully modelled person until the layers exist |

**A character's statement is never engine truth.** The mockup gives them different avatar colours,
different name colours and different message tags — three redundant signals, because one is easy to
lose in a redesign.

## Explore / Plan / Command

**EXPLORE** — read-only. Cannot change anything. This is the only mode Phase 1 needs.

**PLAN** — produces structured proposals, changes nothing. Every plan carries a visible
`◈ NOT EXECUTED — nothing has changed in the simulation` banner. In the cabinet mockup that banner
sits *above* the three options, not below, so it is read before them.

**COMMAND** — attempts to change authoritative state. The required path:

```
user language → interpret → decompose → resolve fictional targets → identify missing information
→ structured action → validate → SHOW THE INTERPRETED ACTION → explicit confirmation
→ deterministic engine → record event
```

**No natural-language message may silently change state.** The confirmation step shows the user what
MERIDIAN thinks they meant, in structured form, before anything executes.

## Conversation object types

Crisis Summary · Person Card · Organisation Card · Population Group Card · Dossier Preview · Belief
Comparison · Exposure Path · Timeline · Counterfactual Comparison · Decision Card · Missing
Information · What MERIDIAN Does Not Know

**Every object preserves** the fictional disclosure, its `ENGINE` / `FIXTURE` / `PROPOSED` origin
marker, `UNAVAILABLE` and `NOT MODELLED` states, and a link to deeper evidence.

The *What MERIDIAN Does Not Know* card is not optional decoration. In mockup 3 it sits beside the
answer at equal weight, because a conversational reply is the easiest place in the whole product to
quietly drop a limitation the full dossier shows.

## Current versus future capability

| | Status |
|---|---|
| Briefing View · Analysis View | **IMPLEMENTED** |
| Deterministic crisis engine · nine linked steps · counterfactuals | **IMPLEMENTED** |
| Belief divergence · organisation positions · cohort results · typed explanations | **IMPLEMENTED** |
| Read-only belief API | **IN DEVELOPMENT** — PR #15, draft |
| Society Roster · Entity Dossier · Belief Landscape | **PLANNED** — designed, not built |
| Ask MERIDIAN (read-only) | **PLANNED** |
| LLM as interpreter | **PLANNED** |
| Plan mode · Command mode | **PLANNED** |
| Cabinet dialogue · person dialogue · conversation memory | **LONG-TERM VISION** |

**The chat interface must not be described as current capability anywhere public.**

## Safe implementation sequence

**Phase 1 — read-only Ask MERIDIAN, no LLM at all.** A controlled question set answered from the
same structured data the screens use. Deterministic responses. This is worth doing on its own: it
proves the component-reuse model and the answer vocabulary before any model is involved.

**Phase 2 — LLM as interpreter only.** `user language → structured query → validation → read-only
projection → response components`. **The model never owns a fact.** It selects a query; the engine
answers it. A hallucinated number is impossible because the model never produces numbers.

**Phase 3 — Plan.** Structured proposals, comparison, no execution.

**Phase 4 — Command.** Validation and explicit confirmation before deterministic execution.

**Phase 5 — In-world dialogue**, only after virtual people have goals, memory, relationships and
state. Until then a generated conversation would be a performance of depth the engine does not have.

## Risks of a pure-chat interface

| Risk | Mitigation |
|---|---|
| **Chat is bad at comparison.** Twelve people, a full timeline, a map, two runs side by side — all worse as text | Chat summons the visual surface rather than describing it. The screens remain first-class |
| **A fluent answer feels authoritative.** Prose hides uncertainty that a marked-up card exposes | Origin markers and the *does not know* card travel with every answer, in the same component |
| **Conversation history becomes shadow state.** "You said earlier…" starts behaving like a fact | **Chat history never creates authoritative state.** Only a validated, confirmed structured action does |
| **The model becomes the authority.** Users trust the sentence, not the engine | Phase 2 forbids the model producing facts. It selects a query; the engine answers |
| **Character output reads as truth.** A minister's opinion is not a result | Three redundant visual signals, and the guide explicitly frames disagreement as disagreement |
| **Silent execution.** A sentence changes the world | Interpret → show → confirm. Ten steps, one of which is the user's |

## Should Ask MERIDIAN be the default landing screen?

**Recommendation: not yet — and then yes.**

**Not for v0.1.** Briefing is the only fully implemented surface, and landing on an empty chat box
that can answer six questions would make MERIDIAN look less capable than it is. An empty prompt is
an invitation to ask something the system cannot do.

**Yes once Phase 2 ships.** At that point the conversation can reach every surface, and the first
screen should be the one that requires no prior knowledge. The Briefing becomes what the chat opens
first, not what the user must decode alone.

**The test for making the switch:** a first-time user can ask what is happening, open a person,
inspect why something changed, see what MERIDIAN does not know, and return to the briefing —
**within ten minutes, without being told where to click.** Until that passes, Briefing stays the
front door.

## Scope

No frontend code. No simulation behaviour changed. No engine change. PR #14 and PR #15 unmerged and
unaffected.
