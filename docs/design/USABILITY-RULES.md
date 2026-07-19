# MERIDIAN usability rules

> **FOUNDER-APPROVED DESIGN AUTHORITY.** These rules govern every player-facing screen. Where a
> screen and these rules disagree, the screen is wrong. Approved 19 July 2026 after the Strategic
> Command Centre — technically sound but structurally over-exposed — failed rule 1.

**Applies to:** all primary player-facing views.
**Does not apply to:** developer tools, and the optional Analysis View, which exists precisely so
that depth has somewhere to live.

---

## 1. The 10-year-old, 10-minute test

A first-time user should be able to **understand the purpose of a screen**, **identify what
matters**, **locate the primary interaction** and **complete the screen's basic task** after no more
than ten minutes of guided use.

If that cannot be achieved, the screen is too complex and must be simplified.

**This does not mean the simulation must be childish.** MERIDIAN models lags, cohort weighting and
counterfactual causality, and none of that is being removed. It means complexity is **progressively
disclosed** rather than presented all at once. A sophisticated engine may sit under a simple screen;
a simple screen may not sit under a confused one.

---

## 2. The 5-second orientation test

Within five seconds a user should be able to answer:

- **Where am I?**
- **What is happening?**
- **What needs my attention?**

If any of the three requires reading a legend, decoding a number or comparing panels, the screen
fails.

---

## 3. Three-question screen rule

Every primary screen must clearly answer:

1. **What happened?**
2. **Why does it matter?**
3. **What can I do?**

A panel that answers none of the three does not belong on a primary screen. It belongs in Analysis
View, or nowhere.

---

## 4. Complexity must be earned

Advanced information must not appear by default merely because it exists.

Technical detail appears **only after the user asks for it**. The existence of a value is not a
reason to render it. Every element on a default screen must justify its own presence against rule 3.

---

## 5. One primary action

Every primary view must have **one obvious next action or decision**.

Where several actions are possible, one is primary and the rest are visibly secondary. A screen with
eight equally weighted affordances has no primary action and therefore fails.

---

## 6. Human language first

Raw engine values, mechanism identifiers, source-field names, rule-pack versions and state revisions
**must not be the primary presentation**.

| Not this | This |
|---|---|
| `Political pressure 0.1495 / 1.000` | **Political pressure is holding near its peak** |
| `Household concern 0.1416` | **Concern is highest among coastal fishing families** |
| `Rerouting 0.5875 — upstream easing` | **Most carriers are still avoiding the strait** |
| `M-POLITICAL-PRESSURE@1.0.0`, `NOT_APPLICABLE` | *(Analysis View only)* |

The engine keeps its precision. The interface translates it.

### 6a. Translation must be derived, never narrated

**A plain-language sentence is a claim, and claims must be true of the current run.** Human-readable
copy must be generated from the projection and trajectory, under stated conditions, and must change
or disappear when the underlying values change. Hard-coding a sentence because it reads well on one
screenshot is a **honesty defect**, not a copy decision.

Worked example, and the reason this clause exists: at tick 20 of the Kestral run, political pressure
has **peaked at tick 17 and is easing slightly**. The sentence "Political pressure is rising" would
be *false* for that run, however natural it sounds. The interface must say what is true.

---

## 7. Game-usability principles

Borrow the qualities that make complex game systems approachable:

clear objectives · contextual prompts · immediate feedback · progressive disclosure · familiar
controls · strong visual hierarchy · safe experimentation · minimal required reading.

**Do not copy the visual identity, assets or trade dress** of Call of Duty, Battlefield or any other
product. Borrow interaction principles, never appearance.

---

## 8. The two views

**Briefing View — default.** The player experience and the primary public screenshot. Scenario and
day · one dominant crisis visual · one plain-language situation summary · three consequence cards
(People / Economy / Politics) · at most two decisions · a short "what changed" line · Inspect and Why
affordances · compact fictional-world and origin disclosure.

**Analysis View — optional.** Exact values · mechanism identifiers · rule-pack information ·
provenance detail · cohort weighting · technical trends · causal parents · tick-level changes · state
revision · seed and run metadata.

The existing detailed dashboard is **adapted into Analysis View, not discarded.** It is correct
work; it was simply the wrong default.

---

## 9. What honesty requires even at low fidelity

Simplification must never remove an honesty property. These survive into Briefing View intact:

- the fictional-simulation disclosure, and its survival under cropping;
- the engine-versus-fixture distinction on any value shown;
- absence rendered as absence — **`UNKNOWN` and `UNAVAILABLE` never become `0`**;
- no implication that a decision can be executed, priced or validated when it cannot;
- no invented urgency, deadline or countdown the engine does not model.

Plain language is a translation of the truth, never a softening of it. If a simplification would
make a false statement easier to read, the simplification is rejected.

---

## 10. How these rules are applied

A screen is reviewed against rules 1–6 **before** visual polish, not after. Polishing an
over-exposed information architecture produces a better-looking version of the same failure — which
is exactly what happened to the Command Centre across three passes and a polish pass.

After any significant change to a primary screen, run an actual first-use walkthrough, record where
the user hesitated or needed explanation, and simplify again where they did.
