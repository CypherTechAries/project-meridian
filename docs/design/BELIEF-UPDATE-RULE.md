# Belief update rule — specification

> **Written before implementation.** This document is the contract the code must satisfy. It is
> frozen together with the input fixtures **before** any outcome is inspected, so that divergence
> cannot be produced by tuning values until three desired labels appear.
>
> **Rule version:** `belief-update-v1`. Any change to a coefficient or term increments it.

**Status:** specification. **Scope:** Belief Formation and Divergence Slice, steps 2–5.

---

## 1. Variables

All values are bounded `[0, 1]` unless stated. `None` means **missing**, and missing is never `0.0`.

| Symbol | Name | Range | Source |
|---|---|---|---|
| `c₀` | prior credence | 0–1 | declared prior, per entity × proposition |
| `f₀` | prior confidence | 0–1 | declared prior |
| `s₀` | prior salience | 0–1 | declared prior |
| `θ` | evidentiary threshold | 0–1 | declared per entity. Resistance to revision |
| `t` | source trust | 0–1 | declared per entity × **source category** |
| `e` | evidence strength | 0–1 | property of the **event** — identical for all recipients |
| `x` | exposure intensity | 0–1 | exposure record |
| `ρ` | relay factor | 0–1 | `1.0` direct, `< 1.0` relayed |
| `r` | relevance | 0–1 | declared per entity × proposition topic |
| `d` | claim direction | `+1` / `−1` | the event **asserts** or **denies** the proposition |

**Not variables, and deliberately absent:** susceptibility, persuadability, influenceability,
conversion probability, target value, influence rank, or any protected trait or declared proxy.
Entity identity is **not** an input — `entity_id` never appears in the formula.

---

## 2. Signal weight

```
w = x · ρ · t · e · r
```

Multiplicative on purpose: **any** factor at zero produces `w = 0` and therefore no update. This is
how the "no exposure ⇒ no update" and "zero evidence ⇒ no evidence-driven movement" invariants are
satisfied structurally rather than by a guard clause that could be forgotten.

`w ∈ [0, 1]` because every factor is.

---

## 3. Credence update

```
target = 0.5 + 0.5 · d          # 1.0 for an asserting claim, 0.0 for a denying one
Δc     = w · (1 − θ) · (target − c₀)
c₁     = clamp(c₀ + Δc, 0, 1)
```

**Properties this shape gives us:**

- **Asymptotic, never overshooting.** Movement is a fraction of the remaining distance to `target`,
  so `c₁` can approach but never pass it. No clamping artefacts at the boundary.
- **Direction is set by `d` alone.** `t`, `x`, `e`, `r` scale *magnitude*. Higher trust can never
  reverse the direction of an update — it can only move further toward what the claim asserts.
- **`θ` is resistance, not disbelief.** A high evidentiary threshold shrinks every update equally;
  it does not bias toward rejection.
- **Continuity.** `Δc` is linear in `w` and in `(target − c₀)`, so a small input change produces a
  small output change. No thresholds, no step functions, no branches.

---

## 4. Confidence update

```
Δf = x · ρ · e · (1 − f₀) · λ        # λ = 0.6, declared in the rule pack
f₁ = clamp(f₀ + Δf, 0, 1)
```

**Confidence is deliberately independent of source trust.** Being exposed to a weakly evidenced
claim from a source you trust should not make you *certain* — it may move what you think is likely
(`c`) without resolving how firmly you hold it (`f`). Separating these is what allows **continued
uncertainty** to be a real outcome rather than a midpoint artefact.

Confidence only ever rises here: exposure to evidence resolves uncertainty, it does not create it.
Evidence *against* a held belief is modelled as a claim with `d = −1`, which moves `c`, not as
negative confidence.

---

## 5. Salience update

```
Δs = w · (1 − s₀) · μ                # μ = 0.5
s₁ = clamp(s₀ + Δs, 0, 1)
```

Salience is how much the holder currently *cares*, and rises with relevant exposure.

---

## 6. Uncertainty

Not a separate field — a **derived reading** of the pair:

```
uncertain ⟺ 0.35 ≤ c₁ ≤ 0.65  AND  f₁ < 0.5
```

An entity in this state must be presented as **"uncertain pending evidence"**, never as weak
acceptance or weak rejection. This is a first-class outcome.

---

## 7. Evaluative propositions

Evaluative propositions carry **stance, confidence and supporting reasons** — never credence,
truth score, factual correctness or population error rate.

```
Δstance_intensity = w · (1 − θ) · (1 − stance_intensity₀)
```

The *position* (`support` / `oppose` / `neutral` / `uncertain`) changes only when intensity crosses
a declared threshold and the claim direction opposes the held position. **No evaluative proposition
is ever marked true or false**, and no holder is ever recorded as factually wrong for holding one.

---

## 8. Missing and unavailable

- A missing prior stays missing. **No prior ⇒ no update ⇒ no belief record is invented.**
- A missing trust, relevance or exposure value makes `w` undefined, not zero — the update is
  **skipped and recorded as skipped**, rather than silently treated as `w = 0`.
- `UNKNOWN` and `UNAVAILABLE` never render as `0.0`.

The distinction matters: `w = 0` means *"exposed, but nothing moved"*; missing means *"we do not
know"*. These produce different traces.

---

## 9. Organisations

Organisations receive **no emotion vector and no personal belief**. Their update is over posture:

```
Δofficial_alignment = w · cohesion · (target − alignment₀)
```

Internal position distribution shifts by the same rule applied per internal bloc, then
`official_position` is derived from the **plurality bloc**, subject to `cohesion`: a low-cohesion
organisation may hold an official position that a minority of its members support, and the interface
must be able to show that gap.

---

## 10. Cohorts

Cohort update uses the identical credence rule. Aggregation is **population-weighted**:

```
aggregate = Σ(cᵢ · populationᵢ) / Σ(populationᵢ)
```

The aggregate **accompanies** the distribution across `unexposed`, `uncertain`, `leaning toward`,
`leaning against` and `missing` — it never replaces it. Unexposed is not zero belief; it is a
separate category.

---

## 11. Update trace

Every update emits a trace recording each term's contribution, so any result can be explained
without re-running:

```
{ rule_version, entity_id, entity_kind, proposition_id, proposition_kind, tick,
  prior_ref, exposure_ref, x, ρ, t, e, r, θ, w, d, target,
  delta_credence, delta_confidence, delta_salience,
  resulting_credence, resulting_confidence, evidence_status, origin,
  scenario_id, scenario_version }
```

---

## 12. Invariants

The implementation must satisfy all of these, and each has a test:

1. **Deterministic** — identical inputs produce byte-identical outputs, repeatably.
2. **Bounded** — `c`, `f`, `s` never leave `[0, 1]`.
3. **Continuous** — a small input change produces a proportionally small output change.
4. **No exposure ⇒ no update.**
5. **Zero exposure intensity ⇒ no update** (`w = 0`).
6. **Zero evidence strength ⇒ no evidence-driven movement** (`w = 0`).
7. **Trust cannot reverse direction** — `d` alone sets sign; `t` only scales magnitude.
8. **Identity-independent** — `entity_id` and display names never enter the formula. Two entities
   with identical declared inputs receive identical outputs.
9. **Order-independent** — registry ordering does not affect results.
10. **Missing stays missing** — never coerced to `0.0`.
11. **Evaluative never truth-valued.**
12. **No protected trait or declared proxy** appears in any term.
13. **Organisations receive no emotion vector.**
14. **No susceptibility, persuadability, conversion or ranking field exists** anywhere in the module.
15. **Biography and descriptive fixture fields never enter the update input.**

---

## 13. Declared coefficients

Rule-pack constants, versioned with the rule. **These are set once, before any outcome is
inspected**, and may not be adjusted to obtain a desired label:

| Constant | Value | Meaning |
|---|---|---|
| `λ` | 0.6 | confidence gain per unit evidenced exposure |
| `μ` | 0.5 | salience gain per unit weighted exposure |
| `UNCERTAIN_BAND` | 0.35–0.65 | credence range for the uncertain reading |
| `UNCERTAIN_CONFIDENCE` | 0.5 | confidence below which uncertainty holds |

If the first principled run does not produce adoption, resistance and uncertainty across the three
people, **that result is reported as it stands**, with an explanation of what the mechanism did and
why — before any change is considered. A change is justified only by a documented modelling defect
or a violated invariant, never by the absence of a desired label.
