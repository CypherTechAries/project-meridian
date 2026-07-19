# Belief and sentiment vertical slice — decision document

> **⚠ SPECIFICATION — NOT IMPLEMENTED.** Nothing described here exists in code. There is no
> proposition, belief, attitude, emotion, stance or propensity structure in the engine today. The
> only belief-adjacent structures that exist are `CohortBeliefs` and `narrative_adoption`
> (`scaffold/backend/app/simulation/schemas/agent_schema.py`), neither of which is
> proposition-scoped. This document proposes a milestone. It does not describe working software.

**Status:** DRAFT — founder review required before any implementation.
**Dated:** 19 July 2026.
**Owns:** the implementable subset of belief/sentiment for one vertical slice, and its UI fields.
**Does not own:** the belief model itself, entity ontology, observation, or the dossier interface —
those are owned by [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md),
[`ENTITY-ONTOLOGY`](../world-model/ENTITY-ONTOLOGY.md),
[`OBSERVATION-AND-PERCEPTION-MODEL`](../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md) and
[`ENTITY-PROFILE-EXPERIENCE`](ENTITY-PROFILE-EXPERIENCE.md). Where this document and those
disagree, they govern and this one is wrong.

---

## 1. Blocking conflict the founder must resolve first

**The slice as briefed cannot be built as briefed without reopening a publication blocker.**

The brief asks for a "first information-warfare slice" implementing
`message → exposure → source credibility evaluation → belief update`, where entities diverge by
source trust and information access. That chain **is** blocker **B5**.

What the repository already records:

- B5 is *"dual-use influence-targeting schema with no acceptable-use terms"*. It was **decided** on
  18 July 2026, and the decision **did not clear it** — B5 now clears only when the **eight named
  controls are implemented and verified**, because control 8 makes technical enforcement mandatory
  and disclosure merely supplementary.
- **None of the eight controls exists in code.** B5 is therefore still a publication blocker and is
  now "the most expensive of the five" (`BELIEF-AND-KNOWLEDGE-MODEL.md` §3.7).
- `BELIEF-AND-KNOWLEDGE-MODEL.md` §4.5 **deliberately holds the source-trust arithmetic at the level
  of a named function** — specifically deferring the perceived-independence term and the
  corroboration-defeat rule to a "B5-gated annex" that is still unwritten, on the reasoning that
  *"specifying source-trust weighting in operational detail enlarges the dual-use surface the eight
  controls were written against, none of which is built."*

So the project's own prior specification declines to write the exact mechanism this milestone is
asking me to implement. I am not able to resolve that by choosing; it is a founder decision, and
per standing constraint an agent may draft a record but may not settle a policy question.

### 1.1 Three routes, with a recommendation

**Route A — enforcement first (recommended).** Build the eight B5 controls (P0.8) as its own short
milestone, then build this slice against them. Cost: delays the portfolio hero. Benefit: the slice
ships with its safety story already true, and B5 stops being a publication blocker — which is
required for public v0.1 anyway.

**Route B — coarse slice, no targeting surface.** Build the slice now, but hold source trust exactly
as coarse as §4.5 already permits:

- source trust is a **declared per-entity scalar in scenario data**, not computed from attributes;
- **no** perceived-independence term, **no** corroboration-defeat rule;
- **no** query, endpoint, projection field or UI affordance that ranks audiences by persuadability,
  susceptibility, or expected belief movement;
- **no** optimisation loop, and no "which message works best on whom" capability, in code or UI.

This demonstrates *differential interpretation* — the portfolio point — without building a targeting
optimiser. It is the smallest honest version, and it is what I would build if told to start now.

**Route C — defer the slice.** Not recommended; the founder's product judgement that this beats
further Command Centre polish is, in my view, correct.

**Also to settle:** the internal name. "Information warfare slice" describes a targeting capability;
"belief formation and divergence slice" describes what Route B actually builds. Naming matters for
the dual-use posture and for anything later published or shown in an interview.

### 1.2 Second blocking dependency

`BELIEF-AND-KNOWLEDGE-MODEL.md` §3.2 declares **P0.6 (event, snapshot, replay) a hard dependency**,
and P0.6 is not built — the founder has separately ruled it is *not* required for public v0.1. A
belief-change timeline therefore cannot be reconstructed from a persisted history. The slice must
either run within a single ephemeral run (acceptable, matches the current engine, must never be
called replay) or wait for P0.6. This document assumes the ephemeral option and says so on screen.

---

## 2. Scope of the slice

One fictional information event, propagated through a small declared entity set, producing
divergent belief, attitude, emotion, stance and behaviour propensity — then a population-weighted
societal effect that reaches the existing P0.5 political-pressure chain.

**The event.** A fictional family spokesperson alleges the government ignored advance warnings about
the Kestral Strait closure. All content is invented; no real person, outlet or state is depicted.

---

## 3. Model — five distinct layers, never one scalar

The founder's core rule: belief, attitude, emotion, stance and propensity are **separate**. A single
"sentiment" number is the failure mode this slice exists to disprove.

### 3.1 Proposition

Adopted unchanged from `BELIEF-AND-KNOWLEDGE-MODEL.md` §4.2 — this document does not redefine it:
`proposition_id`, `kind` (fact / attribution / disposition / evaluative), `subject_entity_id`,
`topic`, `truth_value`, `claim_text` (presentation only), `scenario_authored`.

Invariant retained: `kind == evaluative` ⟹ `truth_value == not_truth_apt`. The slice needs both
kinds — the negligence allegation is an **attribution** with a real truth value; "the government is
untrustworthy" is **evaluative** and must never be scored as factually wrong.

Slice propositions (≈4): government ignored advance warnings (attribution); closure will last beyond
30 days (fact); emergency powers are legitimate (evaluative); families were denied information
(attribution).

### 3.2 Belief

`credence` (0..1), `confidence` (0..1, distinct from credence), `salience` (0..1),
`supporting_observation_ids`, `contradicting_observation_ids`, `last_update_tick`, `contested`.

Credence is *what they think is true*; confidence is *how firmly*; salience is *whether they
currently care*. Three numbers, because collapsing them is what produces fake certainty.

### 3.3 Attitude — target-specific, never a global mood

`(holder, target_entity_id, dimension) → value`, dimensions: trust, legitimacy, threat, sympathy.
A cohort may trust the broadcaster and distrust the government simultaneously; one mood scalar
cannot express that.

### 3.4 Emotion — declared affective state, decaying fastest

Slice set: fear, anger, anxiety, hope, urgency. Bounded 0..1, per entity, with a **faster decay than
belief or attitude** — that ordering is the modelled claim.

> **Honesty bound.** These are *declared scalar states in a fictional model*, not psychological
> measurement and not a claim about real human affect. The UI must say so. Organisations get **no**
> emotion vector — an insurer updates risk posture, not fear.

### 3.5 Stance

Per (entity, issue): `support | oppose | neutral | uncertain` plus intensity 0..1. Issues map to the
existing government options, so stance connects to what the Command Centre already shows.

### 3.6 Behaviour propensity

Per (entity, action): 0..1, **never a guaranteed action**. Slice actions: share, protest, contact
official, withdraw support, organisational statement, reroute. An action occurs only when propensity
crosses a declared threshold **and** constraints allow; crossing is a necessary, not sufficient,
condition, and the UI must not render a propensity as an intention.

---

## 4. Mechanism chain

Nine mechanisms, each with a stable id and version, each executing through `TransitionService`,
each declaring inputs, outputs, bounds, lag and decay, each emitting causal parents — matching the
P0.5 pattern already shipped.

| # | Mechanism | Produces |
|---|---|---|
| 1 | `M-MESSAGE-INTRODUCE` | information event in world state |
| 2 | `M-CHANNEL-EXPOSURE` | observation events (who saw it) |
| 3 | `M-SOURCE-EVALUATION` | per-observation source weight **(B5-gated — see §1)** |
| 4 | `M-BELIEF-UPDATE` | credence/confidence/salience deltas |
| 5 | `M-EMOTION-RESPONSE` | emotion deltas (fastest decay) |
| 6 | `M-ATTITUDE-SHIFT` | target-specific attitude deltas |
| 7 | `M-STANCE-RESOLVE` | stance + intensity |
| 8 | `M-PROPENSITY` | behaviour propensities |
| 9 | `M-SOCIETAL-PRESSURE` | population-weighted aggregate → P0.5 chain |

**Belief update — direction and bounds.** Signed and bidirectional (no one-way ratchet, per §4.5),
floored and capped, saturating, with prior strength and contradicting evidence resisting revision.
Coefficients live in a **versioned rule pack**, as `kestral-causal-slice@1.0.0` already does.

**Exposure.** Declared channel membership and reach in scenario data. Unexposed is a first-class
state — "unaware" is not zero belief, and the UI must distinguish them.

**Divergence sources** (declared, never inferred from identity): prior beliefs, declared source
trust, economic relevance, relationship graph, channel access, organisation membership.

---

## 5. Aggregation — distribution, never a national average

Society views must preserve the distribution: strongly supportive / leaning supportive / uncertain /
leaning opposed / strongly opposed / **unexposed**. Every aggregate carries: group size, population
weight, internal disagreement, change since previous tick, and which narrative drove the change.

A single national mean may not be the only figure shown, anywhere.

---

## 6. Entity set — minimum for the slice

**People (6):** family spokesperson, government minister, opposition politician, broadcaster
journalist, union representative, shipping executive.
**Organisations (7):** national government, opposition party, broadcaster, port authority, shipping
company, maritime insurer, family campaign group.
**Cohorts (6):** port workers, coastal households, governing-party supporters, opposition
supporters, inland households, small-business owners.

No population generation. All entities fictional, scenario-authored, with invented names unattached
to any real person or organisation.

---

## 7. UI fields

**Person dossier:** deterministic abstract avatar; role; affiliations; objectives and pressures;
relationships; belief cards (proposition, credence, confidence, salience, evidence, contested);
attitudes by target; emotional state; stance; propensities; recent exposures; change this tick.

**Organisation dossier:** official position; leadership; factions; internal distribution;
objectives; influence; relationships; recent actions; public position vs internal assessment.

**Country/state dossier:** government, opposition, institutions, media, business, public
distribution and foreign posture rendered **separately** — never one national mind.

**Society belief landscape:** proposition × cohort belief matrix; stance distributions; exposed vs
unexposed; narrative reach; belief-change timeline (within-run only, §1.2); baseline vs incident vs
counterfactual comparison.

**Portraits.** Deterministic abstract avatars generated from `entity_id` — no illustrated faces, no
generated likenesses, no real-person imagery. This avoids likeness risk entirely and stays
reproducible from the seed.

Every field carries origin (engine / fixture) and the two-axis epistemic marking already shipped.

---

## 8. Deterministic and safety boundaries

- The **LLM decides nothing**: not credence, not exposure, not stance, not whether an action occurs.
  It may later narrate wording from recorded authoritative state. No network call during
  authoritative execution.
- All variation via **keyed deterministic draws** (P0.4A, `hmac-sha256-v1`), named substreams per
  mechanism, so adding a draw in one subsystem cannot shift another.
- **Protected characteristics may never** be optimisation criteria, nor set susceptibility,
  competence, morality, loyalty or manipulability coefficients (B5 control 5, and the founder's
  restatement). Identity may affect *exposure and lived experience* only, declared in scenario data.
- **No targeting surface** under Route B: nothing ranks audiences by persuadability.
- Emotion is a declared fictional scalar, never presented as psychological measurement.

---

## 9. Tests

Property tests, not screenshot tests:

1. Two entities receiving the **same** message with different declared trust reach **different**
   credence — the divergence claim, proven not asserted.
2. Belief moves **both ways**; contradicting evidence lowers credence (no ratchet).
3. Unexposed entities are unchanged, and render as unaware rather than as zero.
4. Evaluative propositions are never reported as factually wrong.
5. Propensity crossing a threshold does **not** by itself produce an action.
6. Emotion decays faster than attitude, which decays faster than belief.
7. Aggregates are population-weighted and expose distribution, not just a mean.
8. Same seed + same scenario ⟹ identical belief state (determinism).
9. No protected characteristic appears in any weighting term (static check over the rule pack).
10. No module in the authoritative path imports an HTTP or model client (AST import-graph check, as
    already used).

---

## 10. Non-goals

Not a psychological model. Not a persuasion optimiser or campaign planner. Not a real-world
influence-operations tool. No real people, organisations, states or outlets. No population
generation. No replay or persistence (§1.2). No LLM-authored authoritative state. No claim of
predictive validity — the engine computes a fictional world, it does not estimate this one.

---

## 11. Open questions for the founder

1. **Route A, B or C** (§1.1)? Nothing should start until this is answered.
2. If Route B: confirm the coarse source-trust bound is the intended reading of §4.5's gate.
3. Confirm the milestone name (§1.1).
4. Confirm ephemeral, within-run belief timeline is acceptable without P0.6 (§1.2).
5. Does the Command Centre keep its current place in the nav once the dossier becomes the hero?
6. Is the ~19-entity set the right size, or should the first slice be narrower still?
