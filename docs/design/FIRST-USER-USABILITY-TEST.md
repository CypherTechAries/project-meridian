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

---

## Third pass — the two screens contradicted each other

Real-browser verification found the Briefing and Ask MERIDIAN making **different factual claims about
the same run**. The Briefing said political pressure was low and falling. Ask said it was "still
high". Both were describing the same deterministic 20-tick run, in the same session.

### Why it happened

The Briefing **derived** its claim from the run. Ask **did not derive its claim from anything** — the
sentence was hand-written in `ask/answer.py` and shipped as prose. This was never two derivations
disagreeing; it was one derivation and one authored string. A string cannot follow the engine when
the engine moves, and no test could see the drift because no test compared the two surfaces.

Underneath it sat a second mistake. Political pressure at the end of the run is **0.1495 on a 0–1
scale** — which is genuinely LOW — and **97% of the highest it has been in this run** — which is
genuinely NEAR ITS PEAK. Both statements are true. They measure different things. Reported as though
they were the same measure, they read as a flat contradiction.

### The fix

A single authoritative reading of the packaged run now lives in
`backend/app/simulation/scenario_state.py`. It reports `level` and `near_peak` as **separate**
fields, so a surface cannot state one while implying the other. It computes no simulation value and
changes no engine behaviour.

- The run endpoint returns it, so the Briefing does not re-derive it.
- Ask reads the **same object** through the same default run, so it cannot describe a different run.
- The frontend's plain-language layer reads it. With the shared state absent it **withholds the
  claim** rather than falling back to a private calculation, because a silent fallback would
  recreate the second source of truth.
- Both surfaces now state both facts: low, falling, and still close to its own peak.

Each surface still owns its **wording**. The shared layer owns the **fact**.

### Also fixed by the same work

A field the trajectory does not record — `port_activity_deficit`, `premium_pressure` — previously
had its direction silently computed from a series of zeros and reported as steady. It is now
`NOT_ESTABLISHED`, and the interface says the direction is not established rather than claiming it
looked and found no movement.

### Known, not fixed

**The Briefing and Ask use two different population taxonomies.** The Briefing's People section reads
the projection's cohorts (`coastal-creole-fishing`, `urban-professional-vantaran`, …). Ask reads the
belief landscape's groups (`Port workers`, `Coastal households`, …). These are different group sets
from different models in the same scenario. They do not contradict each other — they are different
quantities over different populations — but a reader who asks "how are people reacting?" gets a
different list of groups from the one the Briefing shows. Unifying them means changing scenario data,
which is out of scope here and needs a founder decision.

---

## Fourth pass — Ask-first, and the test that ended the UI phase

The interface was rebuilt again: **Ask MERIDIAN became the landing screen and the Briefing became
its first answer.** The permanent context rail was removed, "Exact numbers" was removed from
primary navigation, evidence became claim-driven, and the causal explanation was cut from roughly
thirty simultaneous facts to five beats behind one control.

Measured: the landing screen went from **2,635px and 2.9 screenfuls to 1.0**, and the one decision
waiting moved from **257px below the fold** to above it.

### The founder test, 21 July 2026

The founder tested the merged interface as head of state. **No interface failure was reported** —
nothing could not be found, clicked, read or navigated, and for the first time there was no
dashboard, debug-screen or wall-of-information complaint. The tester went straight past the
interface and began arguing with the product.

That is the result that ended this phase:

> **The interface is no longer the main problem. The world is too shallow and the decisions do
> nothing.**

One explanation failure was found and fixed: the situation read as *"halfway into the simulation"*
when it is the **last** recorded point, three ticks past the peak. The card said "Day 5" and never
said day five *of what*. It now states its position in the scenario, derived from the shared state.

Everything else the test surfaced was **capability**, not interface:

- The only decision offered was whether to publish a legal assessment — *"the general public do not
  give a single flying fuck about the government's legal assessment"*. All three government options
  are posture and communications, because nothing else exists for a decision to touch.
- Nine reasonable questions about the fishing industry, the economy, the source of pressure, the
  antagonist and how to end the blockade. The product answers roughly one and a half.
- The scenario declares a **foreign proxy running a knowingly false campaign** against the fishing
  cohort, and **win conditions** — and surfaces neither.

### What this phase established

The usability work succeeded, and the evidence is that it stopped being the thing people talk
about. A cold usability test was never run against the final build, and is now **lower value than
the capability work**: it would rediscover gaps already documented in
[#40](https://github.com/CypherTechAries/project-meridian/issues/40),
[#41](https://github.com/CypherTechAries/project-meridian/issues/41) and
[#42](https://github.com/CypherTechAries/project-meridian/issues/42).

**The next milestone is Kestral Consequence Slice v0.2**, and its acceptance test is not a usability
test at all:

> I make one meaningful decision, the simulated world changes, and MERIDIAN can explain exactly why.
