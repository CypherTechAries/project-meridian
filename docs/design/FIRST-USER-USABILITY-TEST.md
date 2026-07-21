# First user usability test — result: FAILED

Date: 21 July 2026. Build tested: `main` at `b8811e1`, running locally against the live engine.
Participant: a first-time user with no prior exposure to the project.

The founder rule this is measured against:

> **If a 10-year-old cannot be taught to use it in 10 minutes, it fails.**

It failed. This document records what was observed, without softening it. The engine is not the
problem. The presentation is the problem.

---

## Observations

1. **The interface did not explain itself within five seconds.** Nothing on first paint stated what
   had happened or why it mattered. The user had to hunt for the situation rather than be told it.

2. **The Analysis page was overwhelming and unintelligible.** The first-time user described it as
   "absolute nonsense". It presents a wall of panels with no entry point and no reading order.

3. **Most panels contained too much information for their available space.** Cards carried a label,
   an origin badge, a statement, a trend strip and an inspect affordance in a box sized for about
   half of that.

4. **Some content was visibly cropped.** Text was cut off inside fixed-height containers rather than
   the container growing to fit it.

5. **Decimal engine values had no understandable meaning.** A reader shown `0.1495` for political
   pressure has no way to know whether that is high, low, alarming or routine. The number is precise
   and uninformative at the same time.

6. **Engine vocabulary created unnecessary cognitive load.** "peaked", "lagged", "tick", rule-pack
   identifiers such as `M-GOV-OPTIONS@1.0.0`, and raw action identifiers all appeared in the default
   view. Each one is a term the reader must learn before the sentence containing it means anything.

7. **The map looked artificial and did not help.** It reads as decoration from a film set. A new
   user could not say what it was telling them, which is the only thing a diagram is for.

8. **"Publish Legal Advice" did not explain what decision was being made.** It is an internal action
   label presented as user-facing language. Nothing said what the advice is, why publishing it
   matters, or what turns on the choice.

9. **The secondary decision was cropped and could not be read.** A second option competed for
   attention with the first and then failed to display its own content.

10. **Ask MERIDIAN did not look clickable.** Oversized, centred and styled unlike every other
    control, it read as a logo or a heading rather than a button.

11. **The chat screen was the only part that did not feel intimidating.** It was the one place the
    user was willing to ask a question rather than retreat.

12. **The People, Economy and Politics summaries were the clearest part of the application.** Three
    named areas, each with a plain sentence, were understood without help.

---

## What this means

Items 11 and 12 are the product. Items 1 to 10 are what has to go.

The correct response is not to restyle the existing screens. Fixing individual crops, font sizes and
cards would preserve the design that failed. The Analysis card wall is rejected as a default
experience and is removed from the normal user journey until it is redesigned from first principles.

Nothing here is a criticism of the simulation. Every value on screen was correct. The reader could
not tell what any of it meant.

## What survives

- The plain statement that the strait has been blocked for five days.
- The three plain sections: People, Economy, Politics.
- The Ask MERIDIAN conversation.
- The deterministic engine and the technical evidence underneath it.

## What this reset does not touch

No simulation behaviour, belief calculation or Virtual Person calculation is changed by the work
that follows. The engine produces exactly the values it produced before; only what is shown by
default, and in what words, changes.

---

## Second pass — the defects the first pass left behind

The first pass rebuilt the Briefing. Verifying it in a real browser, rather than in tests, found
three things the tests could not see and one they had actively locked in place.

### Ask MERIDIAN did not work at all

Ask MERIDIAN posted to a **page-relative** path while the Briefing used an absolute one. In the dev
server that means every question went to Vite on port 5173 instead of the backend on 8000 and came
back as a 404 HTML page, which the screen honestly reported as UNAVAILABLE. So the interface told
the truth, and the truth was that the headline feature was broken.

**No test caught it.** One test asserted the endpoint equalled the relative path — it encoded the
defect as the expected result. Both screens now resolve every request through a single shared API
base (`src/engine/api.ts`), and the regression tests assert the two screens agree, that neither URL
is page-relative, and that the requested origin is not the page's own.

A second defect was introduced and caught during the same verification: a guard meant to reject
non-catalogue responses keyed on `matched_intent`, which is legitimately `null` when the catalogue
**declines** a question. That turned every honest "I cannot answer that" into a false claim that the
engine was unreachable. Declining to answer is an answer; only a transport failure is UNAVAILABLE.

### Technical evidence clipped text

Measured, not eyeballed. At 1366×768 the technical-evidence screen had panels holding 312px of
content in a 200px box, Key metrics labels truncated to `…`, causal stage names truncated, the
transition strip cut off at the right edge, and a 667px scroll region nested inside a 248px card.

The cause was the same viewport lock that caused the original cropping: the screen was forced to
window height, so content had nowhere to go. It now grows and the page scrolls. Labels wrap instead
of truncating. Measurement at all three sizes reports zero clipped elements, zero nested scroll
boxes and no horizontal overflow. **The screen was not redesigned** — it remains secondary, behind a
control, and out of the primary navigation.

### The map

Unchanged, and still behind "Show where this is happening". It now states its own limitation above
the drawing: it is supporting evidence and has **not** passed the five-second comprehension test.
Redesign is tracked as follow-up work. Nothing on the Briefing depends on reading it.

### Politics reads "low" and "falling" during a blockade

The engine value is unchanged and unsoftened. The section now states plainly that this is what this
packaged fictional run shows at the point the scenario has reached — not a prediction of what comes
next, and not a judgement about how a real government would handle a real crisis.

## Still open

- **The map redesign.**
- **No second cold usability test has been run.** Everything above is mechanical verification. It
  confirms the reported defects are gone; it cannot tell anyone that a ten-year-old could use this.
  That test is required before this work is merged.
