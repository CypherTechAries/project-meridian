# VP-6 — Ask MERIDIAN, Phase 1

Status: implemented on `feat/ask-meridian-phase-1`.
Catalogue version: `ask-meridian-catalogue@0.1`.

Chat is the doorway. Visuals are the evidence. The deterministic engine is the authority.

---

## 1. What this is

A conversational doorway into the existing fictional scenario. A reader types a question; MERIDIAN
matches it against a small declared catalogue and returns an answer assembled from engine output and
declared fixtures, together with the components that show the evidence behind it.

## 2. What this is not

**No language model is used.** Phase 1 does not pretend to understand unrestricted natural language.
There is no embedding, no similarity score, no remote language service and no open-ended entity
extraction anywhere in the path. Matching is normalisation plus a declared phrase table, and the
longest declared phrase wins.

When nothing matches, the answer says so and offers the supported questions. It never guesses, and it
never produces a plausible-sounding answer it cannot ground.

**Nothing is executed and nothing is changed.** The single network call is a POST to
`/api/ask-meridian/query`, which computes an explanation and returns it. No run advances, no belief
moves, no decision executes. Session messages are display context only: they live in a module
variable, are not persisted, and are gone on reload — they were never state.

## 3. Where it sits

Briefing remains the default landing screen. Ask MERIDIAN is a prominent control in the top bar, and
the Briefing control returns from it. It is a destination, not the front door.

## 4. The catalogue

Eight intents, declared once in `app/simulation/ask/catalogue.py`:

| Intent | Target | Offered on the home screen |
| --- | --- | --- |
| `BRIEF_CURRENT_SITUATION` | none | yes |
| `EXPLAIN_ECONOMY_AND_SUPPLY_CHAINS` | none | yes |
| `SHOW_PUBLIC_REACTION` | none | yes |
| `SHOW_WHAT_IS_UNKNOWN` | none | yes |
| `EXPLAIN_PERSON_CURRENT_SITUATION` | person | no |
| `EXPLAIN_PERSON_DECISION` | person | no |
| `SHOW_PERSON_INFORMATION_AND_BELIEF_HISTORY` | person | no |
| `OPEN_EVIDENCE` | none | no |

Every entry declares a `question_label` — the readable phrasing used when the intent is offered as a
follow-up. The four home starters carry an additional `starter_label`. No starter names a fictional
person, because a name with no context is not a question a first-time reader can ask.

Person questions resolve through a declared alias table, typed ids and fixture labels only. A typed
id is accepted only when **every** segment matches, including the scenario — a person reference from
another world does not resolve to a local person. When a person question cannot be resolved, the
answer asks which person is meant and lists them; it does not pick one.

## 5. Honesty properties held by the screen

- Every answer carries the read-only speaker header and its own limitations.
- A decision answer always states `NOT_EXECUTED`: *"Selected by the declared rule. Not executed."*
- Population-group cards state that they are group-level averages and that the individuals inside
  them are not modelled; the per-individual breakdown is shown as `UNAVAILABLE`, never as zero.
- The model-boundary card is present on every substantive answer. Appearance is never associated
  with intelligence, competence, moral worth, susceptibility or persuadability; those are listed as
  things MERIDIAN does not model.
- One belief observation exists per person, and the answer says so rather than implying a trend.
- If the engine cannot be reached, the screen says the answer is `UNAVAILABLE`. It does not render
  silence, and it does not substitute a neutral value.

## 6. The canonical map

The context panel and the situation answers draw **the Briefing's own `briefingMap` component**, at a
smaller displayed size. It is not a simplified redraw, and it is not a placeholder frame.

`bmap` carries `preserveAspectRatio="…slice"`, so the card is given the component's own 960×430
ratio; at any other ratio the slice would silently crop the coastline labels off the edges. Where no
run is loaded there is no engine state to draw, and the card says `UNAVAILABLE` rather than showing
an empty frame a reader could mistake for a map with nothing on it.

## 7. Defects found and fixed during this milestone

Recorded because each one passed a green test suite before visual review.

1. **The screen was unreachable.** Nothing imported `ask-meridian.ts` except its own test file. The
   nav control was an anchor to `#ask` that no handler answered. Every unit test passed while the
   screen could not be opened in the running application. Fixed by adding an `ask` mode to the shell
   and wiring the form, starters, follow-up chips, reset and evidence controls. Two tests now drive
   the real control rather than calling the module directly.
2. **The map card was an empty box.** It emitted a `div` that nothing ever painted into, in the live
   application as well as in the screenshots. The test asserted on its data attribute, which the
   empty div satisfied. Fixed as described above; the test now compares the rendered markup against
   `briefingMap` output and counts drawn elements.
3. **A raw intent identifier was shown to the reader.** Follow-ups fell back to `intent.value`, so a
   chip read `SHOW_PERSON_INFORMATION_AND_BELIEF_HISTORY`. Fixed by requiring `question_label` on
   every catalogue entry, with a validator that rejects an identifier-shaped label.
4. **A raw action id was shown to the reader.** The decision card listed the unavailable option as
   `a-publish-now`. The projection had the declared labels and dropped them; `DecisionSection` now
   carries `option_labels` and the card renders the label.

## 8. Not in Phase 1

Issue #16 is not resolved here. There is no cabinet, no person speaking in their own voice, no
free-form dialogue, no memory across sessions and no ability to act on the world. The screen does not
claim any of them.

## 9. Screens

| File | Screen |
| --- | --- |
| `mockups/v7-1-ask-home.png` | Home — four starters, canonical map in context |
| `mockups/v7-2-current-situation.png` | Current-situation answer |
| `mockups/v7-3-person-decision.png` | Person-decision answer, `NOT_EXECUTED` |
| `mockups/v7-4-public-reaction.png` | Public-reaction answer, group averages |
| `mockups/v7-5-unknowns.png` | Unknowns answer |

Captured from the real render path using real backend responses.

## 10. Tests

- Backend: 635 pass, of which 37 are Ask MERIDIAN Phase 1.
- Frontend: 87 pass, of which 23 are Ask MERIDIAN Phase 1.
