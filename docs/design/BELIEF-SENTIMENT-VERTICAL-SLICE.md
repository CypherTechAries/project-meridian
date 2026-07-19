# Belief Formation and Divergence Slice — decision document

> **⚠ POST-v0.1 MILESTONE — NO IMPLEMENTATION STARTED.** Nothing here exists in code. There is no
> proposition, belief, attitude, emotion, stance or propensity structure in the engine. The only
> belief-adjacent structures are `CohortBeliefs` and `narrative_adoption`
> (`scaffold/backend/app/simulation/schemas/agent_schema.py`), neither proposition-scoped. This
> document plans a milestone. It does not describe working software.

**Status:** founder-decided 19 July 2026 — planning approved, implementation **not** authorised yet.
**Sequence:** B5 controls → public v0.1 → this slice. It must **not** expand v0.1 scope or delay it.
**Renamed** from "information warfare slice" by founder decision. Information operations and
defensive intervention comparison are **longer-term product context**, not this milestone's framing.
**Owns:** the implementable subset of belief/sentiment for one slice, and its UI fields.
**Does not own:** the belief model, entity ontology, observation, or the dossier interface — owned by
[`BELIEF-AND-KNOWLEDGE-MODEL`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md),
[`ENTITY-ONTOLOGY`](../world-model/ENTITY-ONTOLOGY.md),
[`OBSERVATION-AND-PERCEPTION-MODEL`](../world-model/OBSERVATION-AND-PERCEPTION-MODEL.md),
[`ENTITY-PROFILE-EXPERIENCE`](ENTITY-PROFILE-EXPERIENCE.md). Where they disagree with this, they
govern. Release context: [`PROJECT-ROADMAP.md`](../../PROJECT-ROADMAP.md).

---

## 1. Prerequisite: B5 controls, implemented and verified

**This milestone may not begin until the eight B5 technical controls exist and are verified.**

The chain it implements — `message → exposure → source evaluation → belief update`, with entities
diverging by source trust — is the mechanism blocker **B5** was written about. The repository
records that B5 was *decided* on 18 July 2026 and **not thereby cleared**: it now clears only when
the eight controls are **implemented and verified**, because control 8 makes technical enforcement
mandatory and disclosure supplementary. **None of the eight exists in code.**

Consistently, [`BELIEF-AND-KNOWLEDGE-MODEL`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md) §4.5
deliberately holds the source-trust arithmetic at the level of a named function, deferring the
perceived-independence term and corroboration-defeat rule to a B5-gated annex, because specifying
them *"enlarges the dual-use surface the eight controls were written against, none of which is
built."*

**That annex is not to be written during this milestone.** B5 enforcement is a *necessary
precondition*, not permission to add the deferred capabilities automatically.

B5 already blocks public v0.1, so building it serves both objectives.

**Second dependency — P0.6.** Not built, and explicitly not required for v0.1. See §7.

---

## 2. Scope

One fictional information event propagated through a small declared entity set, producing divergent
belief, attitude, emotion, stance and behaviour propensity, then a population-weighted societal
effect reaching the existing P0.5 political-pressure chain.

**The event.** A fictional family spokesperson alleges the government ignored advance warnings about
the Kestral Strait closure. All content invented; no real person, outlet or state depicted.

**The demonstration.** The *same* event produces *different* beliefs and behaviour across people,
organisations and cohorts, for declared and inspectable reasons.

**What it is not.** Not an audience-targeting or persuasion-optimisation tool. See §6.

---

## 3. Model — five distinct layers, never one scalar

Collapsing belief, attitude, emotion, stance and behaviour into a single "sentiment" score is the
failure this slice exists to disprove.

### 3.1 Proposition

Adopted unchanged from `BELIEF-AND-KNOWLEDGE-MODEL` §4.2, not redefined here: `proposition_id`,
`kind` (fact / attribution / disposition / evaluative), `subject_entity_id`, `topic`, `truth_value`,
`claim_text` (presentation only), `scenario_authored`.

Invariant retained: `kind == evaluative` ⟹ `truth_value == not_truth_apt`. The slice needs both —
the negligence allegation is an **attribution** with a real truth value; "the government is
untrustworthy" is **evaluative** and must never be scored as factually wrong.

Slice propositions (≈4): government ignored advance warnings (attribution); closure will last beyond
30 days (fact); emergency powers are legitimate (evaluative); families were denied information
(attribution).

### 3.2 Belief

`credence` · `confidence` · `salience` (each 0..1, distinct) · supporting and contradicting
observation ids · `last_update_tick` · `contested`.

Credence is *what they think is true*; confidence *how firmly*; salience *whether they currently
care*. Three numbers, because collapsing them manufactures false certainty.

### 3.3 Attitude — target-specific, never a global mood

`(holder, target_entity_id, dimension) → value`; dimensions: trust, legitimacy, threat, sympathy. A
cohort may trust the broadcaster and distrust the government at once; one mood scalar cannot say so.

### 3.4 Emotion — people only, bounded, fastest decay

Slice set: fear, anger, anxiety, hope, urgency. Bounded 0..1, decaying **faster** than attitude,
which decays faster than belief — that ordering is the modelled claim.

> **Honesty bound.** Declared scalar states in a fictional model. Not psychological measurement, not
> a claim about real human affect. The UI must say so.

**Organisations have no emotion vector** (founder decision). They carry: official position, internal
position distribution, institutional posture, risk posture, objectives, priorities, cohesion, action
propensity. An insurer updates risk posture, not fear.

**Countries are composite views only** — government, opposition, institutions, business, media and
public cohorts shown separately. No unified national belief or emotion, ever.

### 3.5 Stance

Per (entity, issue): `support | oppose | neutral | uncertain` + intensity 0..1. Issues map to the
existing government options, connecting stance to what the Command Centre already shows.

### 3.6 Behaviour propensity

Per (entity, action), 0..1, **never a guaranteed action**. Slice actions: share, protest, contact
official, withdraw support, organisational statement, reroute. An action occurs only when propensity
crosses a declared threshold **and** constraints allow. Crossing is necessary, not sufficient; the
UI must never render a propensity as an intention.

---

## 4. Mechanism chain

Nine mechanisms, each with stable id and version, executing through `TransitionService`, declaring
inputs, outputs, bounds, lag and decay, emitting causal parents — the P0.5 pattern already shipped.

| # | Mechanism | Produces |
|---|---|---|
| 1 | `M-MESSAGE-INTRODUCE` | information event in world state |
| 2 | `M-CHANNEL-EXPOSURE` | observation events (who saw it) |
| 3 | `M-SOURCE-EVALUATION` | coarse source weight — **bounded by §5** |
| 4 | `M-BELIEF-UPDATE` | credence / confidence / salience deltas |
| 5 | `M-EMOTION-RESPONSE` | emotion deltas, people only |
| 6 | `M-ATTITUDE-SHIFT` | target-specific attitude deltas |
| 7 | `M-STANCE-RESOLVE` | stance + intensity |
| 8 | `M-PROPENSITY` | behaviour propensities |
| 9 | `M-SOCIETAL-PRESSURE` | population-weighted aggregate → P0.5 chain |

**Belief update.** Signed and bidirectional — no one-way ratchet — floored, capped, saturating, with
prior strength and contradicting evidence resisting revision. Coefficients live in a **versioned
rule pack**, as `kestral-causal-slice@1.0.0` already does.

**Exposure.** Declared channel membership and reach in scenario data. **Unexposed is a first-class
state**: "unaware" is not zero belief, and the UI must distinguish them.

---

## 5. Source trust — coarse, declared, bounded (founder decision)

For the first slice, source trust is a **coarse, declared, proposition- or source-specific value in
scenario data**. It is never computed from entity attributes.

**Permitted inputs:** prior belief · coarse source trust · evidence strength · exposure intensity ·
personal or economic relevance · relationship-based exposure · bounded openness to revision ·
explicit uncertainty · population-weighted aggregation.

**Deferred — not to be built in this milestone:** perceived-source-independence arithmetic ·
corroboration-defeat rules · audience persuadability scores · susceptibility rankings · optimisation
over audience segments · automated selection of the most influenceable people or cohorts ·
recommendations for maximising persuasion · protected-characteristic targeting or optimisation.

---

## 6. Safety boundaries

- **No targeting surface.** No query, endpoint, projection field or UI affordance may rank entities
  or cohorts by persuadability, susceptibility or expected belief movement.
- **Protected characteristics** may never be optimisation criteria, nor set susceptibility,
  competence, morality, loyalty or manipulability coefficients (B5 control 5). Identity may affect
  *exposure and lived experience only*, declared in scenario data.
- **The LLM decides nothing** — not credence, exposure, stance, or whether an action occurs. It may
  later narrate wording from recorded authoritative state. No network call in authoritative
  execution.
- **Deterministic draws only** (P0.4A, `hmac-sha256-v1`), named substreams per mechanism, so adding
  a draw in one subsystem cannot shift another.
- **Later intervention comparison** may evaluate a small set of pre-authored fictional *defensive*
  actions — publish verified evidence, issue a correction through a trusted fictional institution,
  remain silent, hold an open public briefing — and may compare aggregate fictional outcomes and
  unintended consequences. It must never identify the easiest audience to manipulate, optimise
  wording for persuasion, rank people by susceptibility, generate targeted influence instructions,
  or recommend exploiting identity or vulnerability.

---

## 7. Current-run trace, not replay (P0.6 dependency)

P0.6 (events, snapshots, hashes, restore) remains required for persistent historical reconstruction
and is **not built**. Before it exists, the belief UI may show only a **"Current run belief-change
trace"**, displaying: observations generated during the current in-memory run; before and after
proposition values; source and exposure references; immediate mechanism parents; current-run tick
order.

It must **never** be described as replay, persistent history, event sourcing, restored timeline or
authoritative run reconstruction — and must not be persisted or reloaded as though P0.6 existed.
"Replay-capable" is already a standing prohibited phrase.

---

## 8. Entity set — minimum for the slice

**People (6):** family spokesperson, government minister, opposition politician, broadcaster
journalist, union representative, shipping executive.
**Organisations (7):** national government, opposition party, broadcaster, port authority, shipping
company, maritime insurer, family campaign group.
**Cohorts (6):** port workers, coastal households, governing-party supporters, opposition
supporters, inland households, small-business owners.

No population generation. All fictional and scenario-authored, with invented names unattached to any
real person or organisation.

---

## 9. UI fields

**Person dossier:** deterministic abstract avatar; role; affiliations; objectives and pressures;
relationships; belief cards (proposition, credence, confidence, salience, evidence, contested);
attitudes by target; bounded emotional state; stance; propensities; recent exposures; change this
tick.

**Organisation dossier:** official position; leadership; factions; internal position distribution;
institutional and risk posture; objectives; priorities; cohesion; influence; relationships; action
propensity; public position vs internal assessment. **No emotion vector.**

**Country/state view:** government, opposition, institutions, media, business, public distribution
and foreign posture rendered **separately**.

**Society belief landscape:** proposition × cohort belief matrix; stance distributions; exposed vs
unexposed; narrative reach; current-run belief-change trace (§7); baseline vs incident vs
counterfactual comparison. Distribution always preserved — a single national mean may never be the
only figure shown.

**Avatars.** Deterministic abstract avatars generated from `entity_id`. **No generated human faces**
in the initial implementation (founder decision) — this avoids likeness risk entirely and stays
reproducible from the seed.

Every field carries origin (engine / fixture) and the two-axis epistemic marking already shipped.

---

## 10. Tests

1. Same message, different declared trust ⟹ different credence — divergence proven, not asserted.
2. Belief moves both ways; contradicting evidence lowers credence (no ratchet).
3. Unexposed entities unchanged, rendered as unaware rather than zero.
4. Evaluative propositions never reported as factually wrong.
5. Propensity crossing a threshold does not by itself produce an action.
6. Emotion decays faster than attitude, which decays faster than belief.
7. Aggregates population-weighted and distribution-preserving.
8. Same seed + scenario ⟹ identical belief state.
9. No protected characteristic in any weighting term (static check over the rule pack).
10. No authoritative-path module imports an HTTP or model client (AST import-graph check).
11. No projection field, endpoint or UI element ranks entities by persuadability or susceptibility.
12. Organisations carry no emotion vector.

---

## 11. Non-goals

Not a psychological model. Not a persuasion optimiser, campaign planner or audience-targeting
system. Not a real-world influence-operations tool. No real people, organisations, states or
outlets. No population generation. No replay or persistence (§7). No LLM-authored authoritative
state. No claim of predictive validity — the engine computes a fictional world, it does not estimate
this one. **Not required for, and must not delay, public v0.1.**

---

## 12. Remaining open questions

1. Does the Command Centre keep its nav position once the dossier becomes the hero screen?
2. Is ~19 entities right, or should the first slice be narrower still?
3. Which of the eight B5 controls bind this milestone directly, and which are release-only? To be
   answered by the B5 enforcement milestone, not here.
