# Project MERIDIAN: Current-State Audit

**Date:** 18 July 2026
**Status:** draft for owner review
**Scope:** the complete local tree at the repository root *(absolute local path redacted 19 July 2026 — see the redaction note at the end of this file)*, including `scaffold/backend`, `scaffold/schemas`, `scaffold/scenarios`, `scaffold/frontend`, `scaffold/docs`, and the root governance documents.

---

## 1. Verdict

This repository is **not publishable in its current state**, and it is **not execution-ready**. Those are two separate judgements and both are negative for separate reasons.

It is not publishable because the repository contains live untruths. Several documents state, in the present indicative, properties the code does not have: that the determinism boundary is guarded in CI (there is no CI, and no `.git` directory at all), that the engine validates a proposal's legality and feasibility (`_validate_and_price` is a two-line dictionary lookup), that three tables are persisted (nothing is ever written to the database), and that adding a nation archetype requires only a new JSON file (a renamed institutional role silently produces zero events for the whole run). It is also not publishable because the campaign and cohort schemas are a field-for-field influence-operations targeting template, the plan itself claims a near one-to-one DISARM Red Framework mapping, and every stated safeguard is prose with no technical or licence enforcement behind it. That is a decision for you, not for me, but it should be made deliberately before a URL exists.

It is not execution-ready for a more fundamental reason than any documentation defect: the three-tier simulation is not a simulation of a system, it is three independent processes running in the same loop. No tier reads another tier's state. Macro effects are constants, so the same action produces the same delta in every possible world. Left to run for 100 ticks the "nation in crisis" becomes maximally ready, maximally stable and increasingly popular while every cohort's belief in government competence decays irreversibly to zero. The determinism boundary, which is the project's best idea and is genuinely well conceived, currently guards a pipe with nothing flowing through it.

The good news, and it is real, is that almost nothing here is structurally blocked. The schemas anticipate what is missing. The seams are in the right places. The corrections are additive far more often than they are rewrites.

---

## 2. What was actually verified

Findings were checked against the real files, line by line, and then adversarially re-verified: each candidate finding was given to a second pass whose explicit job was to refute it, quote the contradicting line, or correct its severity. Claims were tested by execution where execution was possible: the test suite was run (5 passed), the engine was run for 100 ticks at seed 88213 to observe saturation and belief collapse, regressions were injected in a scratchpad copy to test whether the determinism test would catch them (it does not catch meso regressions), the container filesystem layout was reproduced to confirm the Docker quick start fails, `pip install -r requirements.txt` was resolved on this machine, and `docs/PLAN.pdf` was text-extracted so its claims could be checked rather than assumed.

**124 candidate findings were assessed. 11 were refuted and dropped**; they are listed with reasons in Appendix A. A further large number were confirmed on the facts but downgraded in severity, because the original grading counted honestly-labelled scaffold omissions as defects. That distinction is applied throughout: a scaffold is permitted to be incomplete, and this one is unusually candid in several places (`llm_gateway.py:1` "LLM gateway — STUB", `runs.py:3-5` "A real build would persist via `app/db/models.py`", `routes_simulation.py:82-86` "In this stub we simply log the intervention"). What a scaffold is not permitted to do is claim a property it lacks, and that is where the reportable defects sit.

One note on provenance. An earlier external review of this project could not run the code, because the file set uploaded to it was incomplete. Its conclusions were therefore drawn from reading fragments. This audit read the complete local tree and executed it. Where the two disagree, prefer this one on matters of fact, and treat the earlier review's severity gradings as unverified.

Anything that could not be established is marked Unknown rather than guessed. Two such items are noted in place: whether the Docker build breaks on Linux/Python 3.11 for the same `litellm` reason it breaks on Windows/3.13, and whether the section 9 archetype table in `PLAN.pdf` reads correctly (its prose extracts cleanly, its tables interleave).

---

## 3. What is genuinely good

Credit where it is earned, because it makes the rest of this document credible.

**The determinism boundary is the right idea, correctly located, and honoured in code.** The concept, that the LLM returns proposals and the engine owns every number, is the single most valuable design decision in the project. It is not just documented: `llm_gateway.py:35` imports only `ActionProposal` and no state object; both public gateway functions are typed to accept `Mapping[str, Any]`; the sole production call site (`institutional_agent.py:38-41`) passes `self.spec.model_dump()` and a literal dict, that is, serialised copies rather than live objects; and `_validate_and_price` (`engine.py:128-130`) provably never reads `proposal.parameters` or `proposal.confidence` (a repo-wide grep for those attributes returns zero reads). `ACTION_EFFECTS` (`engine.py:35-43`) is a closed allowlist, so an invented action type produces no delta at all. The LLM genuinely cannot write a number. That property is real today.

**Reproducibility is real for the shipped configuration and is tested.** `engine.py:83` establishes a single seeded `random.Random` and it is the only generator drawn from anywhere in the simulation package; there is no global `random`, no unseeded numpy, and no time-based value. Iteration order is fixed everywhere it matters (`engine.py:152`, `engine.py:159`, both with explicit comments). Two runs at seed 88213 produce byte-identical macro state, narrative adoption, cohort beliefs and event log, and the identity holds across separate processes under differing `PYTHONHASHSEED`. `tests/test_engine.py:34-40` passes for real reasons, and it does catch the two regression modes `CLAUDE.md` names: injecting unseeded global randomness or a time-based value both make it fail.

**The ADR habit is worth keeping.** Nine ADRs recording the reason behind each stack choice, with an explicit "do not re-litigate without a new ADR" convention (`ARCHITECTURE_DECISIONS.md:7`) and one decision marked "Do not weaken" (`:51`), is more discipline than most projects at this stage have. The ADRs are missing metadata (section 6), but the instinct is sound and the rationale genuinely is preserved.

**The schema layer anticipates the explanation system.** `Event.causal_parents`, `Outcome.explanation_trace`, `Outcome.confidence`, `EventVisibility`, `CampaignMetrics.detection_probability` are all defined, mirrored in JSON Schema, and ready. They are unwired, which is a gap, but the shape of the thing that is missing has already been thought about, and that materially reduces the cost of building it.

**Stub mode is an honest design.** The system runs offline, with no API keys, deterministically, and says so. `_stub_action_type` (`llm_gateway.py:41-51`) carries the docstring "Deterministic canned action choice per role, so stub runs are reproducible", which is exactly right and exactly honest. Several of the harshest-sounding items in this audit exist only because the stub is deliberately doing the work a model will later do.

**Data-driven scenarios as an intent is the correct architecture,** and the engine contains no `if archetype ==` branch anywhere. The intent has not been delivered (sections 4 and 5), but nothing about the current design forecloses it.

---

## 4. Critical findings

Two findings are critical. Both are behavioural, not documentary, and neither has been reported before.

### 4.1 The three tiers are structurally decoupled: no tier ever reads another tier's state

**What the code does now.** `step()` (`engine.py:147-180`) runs three blocks that share no state.

The meso tier reads nothing from macro. `cohort_agent.py:28-38` is the entire cohort dynamic and touches only `self.cohort.grievances` and `self.model.rng`:

```
if self.cohort.grievances:
    drift = 0.005 + self.model.rng.uniform(0.0, 0.005)
    b = self.cohort.beliefs
    b.government_competence = max(0.0, b.government_competence - drift)
```

The micro tier is given no world state. `institutional_agent.py:33-37` passes the gateway a three-key stub:

```
context = {"tick": self.model.tick, "scenario_id": self.model.scenario_id, "primary_target": None}
```

No indicator, no cohort, no event. Even with a live model wired in, every institutional agent would be proposing blind.

The macro tier is a constant table. `engine.py:35-43` maps an action to a fixed delta, so `request_procurement_acceleration` yields exactly `{"military_readiness": 0.01, "government_approval": -0.002}` in every possible world state, at every tick, regardless of anything.

Diffusion output goes nowhere. `engine.py:143` assigns `self.narrative_adoption`, and the only reader in the codebase is the API response at `routes_simulation.py:75`. It never reaches `CohortBeliefs` or `MacroState`.

The one channel the schema explicitly promises is dead: `income_sensitivity_to_shipping_disruption` is declared at `agent_schema.py:36` and populated for all five demo cohorts, and a grep across `backend/app` returns only that declaration. The single macro indicator that actually moves under its own rule (shipping) therefore cannot reach the cohorts whose income the schema says depends on it.

Measured over 100 ticks at seed 88213: macro `government_approval` rose 0.44 to 0.64 while every grievance-bearing cohort's `government_competence` fell to 0.0. The tiers moved in opposite directions, with no interaction, for a hundred ticks.

**Why it matters.** `CHARTER.md:53` requires results "Sensitive to the facts of the scenario — the same action in a different world state produces a different outcome". With a constant effects table and zero cross-tier reads, that property is false by construction, not merely unimplemented. `README.md:25` promises "Every action creates second- and third-order effects"; there is no channel along which a first-order effect could propagate to become a second-order one. This is the finding that reframes several others: every complaint about the action table being small or the effects being crude implicitly assumes the wiring exists underneath. It does not.

**What correct looks like.** `CohortAgent.step` receives a read-only macro snapshot and uses `income_sensitivity_to_shipping_disruption` and `MediaExposure` as real inputs. Cohort beliefs, weighted by `represents_population`, aggregate into macro `government_approval` and `social_stability_index` at the end of each tick. `InstitutionalAgent` receives a real read-only world-state view in `context` rather than a three-key stub. `ACTION_EFFECTS` magnitudes become functions of current state (and, per section 5.5, move out of the engine into rule-pack data). Narrative adoption feeds belief.

### 4.2 The macro tier saturates monotonically: the crisis resolves itself

**What the code does now.** Every institutional agent proposes the same action every tick, forever. `llm_gateway.py:41-51` is a fixed role table; there is no cooldown, no cost, no political capital debit and no prerequisite anywhere in the codebase. `engine.py:159-164` applies whatever comes back, unconditionally, every tick.

The per-tick sums over the six demo agents (`engine.py:35-43`) are: `military_readiness` +0.01, `social_stability_index` +0.005, `government_approval` +0.002 (being -0.002, -0.003, +0.001, +0.004, +0.002).

Executed at seed 88213 for 100 ticks: `military_readiness` 0.39 to 1.0, pinned at the `apply_deltas` clamp ceiling (`macro_state.py:43-44`) from approximately tick 61 onwards; `social_stability_index` 0.47 to 0.97; `government_approval` 0.44 to 0.64.

Meanwhile 14 of the 18 macro scalars never change at all across those 100 ticks: `inflation_rate`, `unemployment_rate`, `gdp_growth_qoq`, `foreign_direct_investment_flow`, `fuel_reserve_days`, all four `institutional_trust` values, both `alliance_confidence` values, and all three `public_finances` values remain frozen at their scenario initial values. Of the four that do move, one (`shipping_throughput_pct_of_baseline`) only jitters on zero-mean noise, 0.6100 to 0.6090 across the full 100 ticks. So three indicators carry the entire dynamic behaviour of the simulation, and all three rise monotonically.

*(Owner-verified 18 July 2026 by independent re-execution: 18 scalars total, 14 frozen, 4 moved; `military_readiness` first touches the 1.0 clamp at tick 61. An earlier draft of this section said "13 of 18", which contradicted its own list. Corrected.)*

**Why it matters.** The default trajectory of a grey-zone crisis simulator is a nation that becomes maximally prepared, maximally stable and steadily more popular while nobody does anything and no adversary action has any effect. Any demonstration run past roughly sixty ticks displays a saturated, physically meaningless state. This is a distinct defect from "the action table is hardcoded": even with exactly the current table, adding cost, decay, diminishing returns or opposing crisis pressure would prevent it. It also means the demo's own win condition (`kestral-strait.json:421`, `shipping_throughput_pct_of_baseline_min: 0.85`) sits underneath a ceiling that exists only in code, not in the schema (section 6).

**What correct looks like.** Per-action resource cost and cooldown, drawn from `AgentResources` and `Intervention.resource_cost`, both of which are already declared and currently unread. Mean-reverting or crisis-driven downward pressure on the indicators actions push up, so that inaction has consequences. A test asserting that no indicator sits at a clamp boundary over a long run. Either a rule for each currently frozen indicator block, or their removal from the demo scenario so the state object stops advertising dynamics that do not exist.

---

## 5. Major findings

Fifteen, after merging items that the dimensional analysis surfaced twice. Ordered by consequence.

### 5.1 Reproducibility currently rests on the LLM stub being a lookup table, and no document says so

`engine.py:128` selects the macro delta by the LLM-returned `action_type`. The engine owns the magnitude; the caller owns the selection. Today the caller is `_stub_action_type` (`llm_gateway.py:41-51`), a pure dict on `agent_role`, so runs are reproducible. Verified experimentally: changing only the stub's choice for one role, holding seed at 99 over 10 ticks, moved `military_readiness` from 0.49 to 0.39, and in a separate probe from 0.59 to 0.39. Same seed, different numbers.

No document states the conditionality. `ARCHITECTURE_DECISIONS.md:64-65`, `CLAUDE.md:21` and `engine.py:8` all present reproducibility as an architectural property. `ADR-004:40-41` describes going live as "a localized change to one module", which is literally true and therefore dangerous: it invites a future contributor to flip the switch without realising they have just broken commitment 1. `llm_gateway.py:27-28` compounds this by describing LLM output as "an interpretive layer that is NOT part of the reproducible numeric state", which is false of `action_type` by construction. The boundary in the docs is described as text-versus-numbers; the boundary in the code is magnitude-versus-selection.

**What correct looks like.** State the claim conditionally ("same seed + same scenario + same recorded proposal stream"), and build the recorder that makes the condition satisfiable. The fix is cheap because the RNG draw count per tick is already invariant to proposal content: `_validate_and_price` draws nothing (`engine.py:121-130`), the cohort branch keys on static scenario data (`cohort_agent.py:35`), and diffusion draws once per node (`diffusion.py:64-75`). A record-and-replay mode would reproduce exactly.

### 5.2 The boundary test is tautological and cannot detect the regression it is cited as preventing

`tests/test_engine.py:74-77`:

```
assert isinstance(proposal, ActionProposal)
assert not hasattr(proposal, "apply_deltas")
assert not hasattr(proposal, "macro_state")
```

`ActionProposal` (`agent_schema.py:374-393`) declares six fields, no `model_config`, and Pydantic v2 defaults to `extra="ignore"`. The two `hasattr` assertions are therefore true by construction of the class under test and can never fail. Only the `isinstance` check is real, and it is narrow.

Verified by injection: a gateway that imports `MacroStateHolder` and calls `apply_deltas({"government_approval": 0.5})` before returning a well-formed `ActionProposal` passes all three assertions, and the entire five-test suite stays green (exit 0), because a deterministic illicit mutation is still deterministic.

Against this, `ARCHITECTURE_DECISIONS.md:56-57` says the boundary is "enforced *structurally* — `llm_gateway.py` imports no state object, and `test_engine.py::test_llm_gateway_cannot_write_state` guards it", `README.md:13-14` says "guarded by a test, not merely documented", and `CHARTER.md:44` says it "guards in CI". The import-hygiene half of that sentence is checked by nothing executable, and there is no CI at all.

**What correct looks like.** Parse `llm_gateway.py` with `ast` and fail if any import resolves into `app.simulation.agents.*`, `schemas.macro_schema` or `engine`. Add a behavioural test that snapshots `MacroState`, calls every public gateway function with a live model in scope, and asserts the snapshot is byte-identical afterwards. Both would pass today, so neither breaks anything. Then `ADR-006`'s wording is earned.

### 5.3 Meso reproducibility is claimed as proven by a test that never inspects meso state

`ARCHITECTURE_DECISIONS.md:64-65` states "identical macro/meso numbers, proven by `test_same_seed_is_deterministic`", `CLAUDE.md:21` and `:27` say the same and add "Do not weaken it", and `README.md:61-63` repeats it. The test asserts exactly one thing (`tests/test_engine.py:40`): `assert a.macro_snapshot() == b.macro_snapshot()`. `macro_snapshot()` is `MacroState.model_dump()` (`macro_state.py:49-51`) and contains no cohort field, no adoption field.

Verified by injection: patching `CohortAgent.step` to draw from global `random` instead of `self.model.rng` leaves macro equality True while cohort beliefs diverge. Separately, reversing the cohort order in the scenario leaves macro byte-identical while all meso output changes. Both are exactly the regression classes `CLAUDE.md:22-24` warns against, and the named guardrail test stays green through both.

Note that asserting on `a.snapshots == b.snapshots` would not close this: `self.snapshots` is macro-only too (`engine.py:116`, `:180`).

**What correct looks like.** Assert per-cohort `beliefs.model_dump()`, `narrative_adoption` and `event_log` alongside the macro snapshot. This passes today, so it is a two-line change that converts a false claim into a true one.

### 5.4 ADR-006 claims the engine validates legality and feasibility; `_validate_and_price` is a dict lookup

`engine.py:121-130` is the whole gate:

```
base = ACTION_EFFECTS.get(proposal.action_type, {})
# Engine-owned scaling; intentionally ignores proposal.parameters as authority.
return dict(base)
```

There is no legality check, no feasibility check, no resource debit, and no scaling: the returned delta is a per-action constant. `MicroAgent.constraints` ("Hard legal/procedural constraints on the agent", `agent_schema.py:181-183`) is populated for all six demo agents (`kestral-strait.json:263, 291, 317, 342, 364, 386`, including `procurement_law_18mo_minimum`) and read by zero code paths. `AgentResources.political_capital` and `budget_control_usd_m` are likewise never consulted. `Intervention.legal_check`, documented at `agent_schema.py:242-244` as "set by the engine", is never written.

The claim appears in seven places, all present indicative: `ARCHITECTURE_DECISIONS.md:54-55`, `CHARTER.md:113`, `engine.py:4`, `institutional_agent.py:4-5`, `agent_schema.py:157-158` and `:377-379`, `README.md:19` and `:24` ("accepts, rejects, or scales"), `scaffold/README.md:19`. Unlike `ADR-004` and `ADR-005`, which explicitly caveat their subjects as scaffold-level, `ADR-006` carries no such qualifier, and `engine.py` contains no stub or TODO marker.

The gate is not entirely absent: `ACTION_EFFECTS.get(action_type, {})` is a real allowlist, and `engine.py:163` (`if deltas:`) means an unrecognised action produces no state change. That is fail-closed and is the correct direction. But it also means an unknown action, a hallucinated action and a legitimate `observe` are indistinguishable, all producing no state change, no event, and no log line.

**What correct looks like.** A typed result (`applied` / `rejected-unknown` / `rejected-illegal` / `rejected-unaffordable`, with a reason code and rule id), evaluated against `spec.constraints` and `spec.resources`, with an event emitted for every branch including rejections and no-ops. Legality rules must live in scenario data, not engine conditionals, or the fix breaks commitment 3.

### 5.5 Actor authority is decided by the LLM stub, not the engine

`ACTION_EFFECTS` is keyed on `action_type` alone. A grep for `target|proposing_agent_id|role|rationale` in `engine.py` returns no functional hits: the engine never reads who proposed an action, their role, their resources, or the target. The only thing binding a role to a permitted action is the stub's table at `llm_gateway.py:43-50`.

`CHARTER.md:113-114` states the LLM "never decides whether the composition is legal". Role authority, which is the most basic legality question, is decided entirely inside `llm_gateway.py`. Wire a real model and if it returns `request_procurement_acceleration` for `strategic_comms`, the engine applies the full delta without objection.

**What correct looks like.** A role-to-permitted-action map in scenario data (not engine code), checked against `proposal.proposing_agent_id` before pricing, with refusals logged rather than silently returning `{}`.

### 5.6 "Adding an archetype requires only a new scenarios/\*.json" is false, and fails silently

`README.md:106-107`: "Nation types are **data, not code** (PLAN.pdf §9): adding an archetype means adding a scenario-template JSON, never editing the engine." `ARCHITECTURE_DECISIONS.md:75`: "Adding an eighth archetype must require only a new `scenarios/*.json`." `CLAUDE.md:53-55`: "Do **not** edit the engine."

Verified, seed 42, 10 ticks. A scenario identical to Kestral but with institutional roles renamed (`chancellor`, `secretary_minister_of_defence`) produced **0 events over 10 ticks** versus 60 for the original, with no exception and no warning: every agent fell through `table.get(agent_role, "observe")` at `llm_gateway.py:51` to a no-op. A landlocked scenario, with `shipping_throughput_pct_of_baseline` removed, raises `KeyError` at `engine.py:58` inside `_macro_from_scenario`, surfacing as an unhandled 500.

The escape hatch `ADR-008:73-74` offers ("extend the schema, not the engine") does not rescue the landlocked case: the field is required with no default in `macro_schema.py:46-48`, and `_step_macro_rules` (`engine.py:132-136`) applies its only per-tick macro noise to that indicator unconditionally, with no `if` around it. A strait is hardcoded into a shared schema in five further places (`engine.py:58`, `macro_state.py:34`, `agent_schema.py:36`, `llm_gateway.py:98-100`).

Additionally, the archetype data that does load is largely inert: `archetype`, `government_structure`, `win_conditions`, all agent `objectives`/`traits`/`resources`/`relationships`/`constraints`, and cohort `media_exposure`/`represents_population` are read by no code (grep in `backend/app` outside `schemas/` returns zero). `self.campaign = scenario.get("hidden_campaign")` (`engine.py:111`) is assigned and never read again anywhere.

Of the two failure modes, the `KeyError` is the safer one. The renamed-role case runs green, emits nothing, and looks like a working simulation.

### 5.7 ACTION_EFFECTS hardcodes the entire action vocabulary and every magnitude in engine code

`engine.py:35-43` defines all seven permissible actions as a module constant. Nothing in `scenarios/*.json` can add, remove, or reprice an action; there is no schema field for it, and `ActionProposal.action_type` (`agent_schema.py:383`) is a bare `str` with no scenario-supplied vocabulary. A second hardcoded table maps roles to actions at `llm_gateway.py:43-51`.

The vocabulary is itself institution-coupled: `convene_cabinet` and `block_unfunded_spending` presuppose a cabinet and a treasury veto that a junta, a monarchy or a single-party state does not have. This is not an `if archetype ==` branch, so `ADR-008`'s literal wording survives, but the property that wording exists to deliver does not.

`CHARTER.md:87-111` defines sixteen consequence primitives (Legal, Procedural, Temporal, Relational, Optionality and others). None of them has any representation in code: a grep for those terms across `backend/` returns nothing. The gap between a sixteen-primitive compositional design and a seven-row constant dict is the largest architecture-to-code divergence in the repository.

### 5.8 The macro noise rule is hardcoded to a maritime-strait indicator

`engine.py:132-136` is the entire per-tick macro rule set:

```
noise = self.rng.uniform(-0.002, 0.002)
self.macro.apply_deltas({"shipping_throughput_pct_of_baseline": noise})
```

`macro_schema.py:47` describes that field as "Strait shipping throughput as a fraction of pre-crisis baseline". A landlocked or Gulf archetype receives strait-shipping noise every tick and gets no macro dynamics of its own, because the rule is not selected by scenario data. It is unconditional.

**What correct looks like.** Per-tick drift expressed as data (`{indicator, distribution, params}` rules in the scenario or rule pack), iterated generically. The engine should know how to apply a seeded drift rule; it should not know which indicator drifts.

### 5.9 Cohort belief is a one-way ratchet to zero

`cohort_agent.py:35-38` is the entire meso dynamic and it is irreversible and absorbing. A grep for `government_competence` across `backend/app` returns exactly two hits: this write and the schema declaration at `agent_schema.py:59`. No code path anywhere increases it. No code path ever clears or adds a grievance.

Measured, 100 ticks, seed 88213: four of five demo cohorts reach 0.0 and stay there; only the grievance-free `urban-professional-vantaran` is unchanged at 0.52, because it has no dynamic at all. The other four `CohortBeliefs` fields (`foreign_interference_probability`, `trust_in_military`, `support_for_western_alignment`, `support_for_eastern_alignment`) are never written by anything.

`counter_narrative_briefing` exists in `ACTION_EFFECTS` but touches macro only, so no player or agent action can ever recover public belief. The "influence the population" premise is unwinnable by construction. `CHARTER.md:24` ("Public opinion changes through events, narratives, economic effects and trust") has one degenerate implementation: monotone decay toward zero.

### 5.10 `represents_population` is never read, and the demo data is wrong by 63x undetected

A grep for `represents_population` in `backend/app` returns only the declaration (`agent_schema.py:95`) and its docstring (`:92`, "One record stands for `represents_population` citizens"). `diffusion.py:25-37` weights edges by `internal_cohesion` only; `engine.py:142` builds susceptibility per cohort id with no population term. So a cohort of 14,200 carries identical weight to one of 620,000.

Because the weight is inert, a data error produces no symptom. `plan.txt:229` specifies a "4.1-million-person archipelago" with a "22% Northern Creole minority", roughly 900,000 people; the corresponding cohort `coastal-creole-fishing` is set to 14,200 (`kestral-strait.json:79`), understated by about 63x. The 11% highland figure (451,000) matches exactly, so this is an outlier rather than a different convention. The five cohorts sum to 1,488,200 against a stated 4.1 million, and no total-population field exists in any scenario or schema.

`README.md:6` and `scaffold/README.md:16` both describe the meso tier as weighted cohorts standing for N citizens. They are not weighted.

### 5.11 The decision endpoint lets the client set engine-owned fields, including `legal_check`

`routes_simulation.py:81` binds the entire `Intervention` model from the request body and `:91-100` writes `intervention.model_dump()` verbatim into `model.event_log`. Verified by construction: `Intervention.model_validate({"action_id":"x","actor_role":"anyone_i_type","action_type":"nuke_the_moon","legal_check":"APPROVED_BY_CLIENT","resource_cost":{"treasury_reserve_usd_m":-99999},"timeline_days":0})` is accepted unchanged.

`action_id` is also client-chosen and is interpolated directly into the event identifier (`routes_simulation.py:93`, `f"decision-{model.tick}-{intervention.action_id}"`) with no uniqueness check, so a caller can mint colliding or forged event ids.

This is distinct from 5.4. That finding is about the engine failing to judge. This one is about the client being able to state the verdict and forge log identity, in the record that `CHARTER.md:118-127` says must answer "which rule applied".

**What correct looks like.** Split the wire model from the state model. Accept an `InterventionRequest` carrying only `actor_role`, `action_type`, `target` and intent; have the engine mint `action_id`, `legal_check`, `resource_cost`, `timeline_days` and `second_order_hooks`.

### 5.12 A dual-use influence-targeting schema with no technical or policy safeguard

The schema pairs audience segmentation with operational campaign design. Segmentation: `InfluenceSusceptibility` with authority, identity and economic appeal channels (`agent_schema.py:72-78`); `MediaExposure` per channel (`:42-53`); `Demographics` including `religion_majority` and `primary_language` (`:22-28`). Campaign design: `target_cohorts`, `existing_grievance` ("Pre-existing grievance the campaign exploits"), `messenger.perceived_independence`, `amplification_network.coordinated_accounts`, `desired_behaviour`, `detection_probability`, `attribution_probability` (`:312-346`).

`plan.txt:221` states this schema "was independently found to map almost one-to-one onto the DISARM Red Framework", a real influence-operations kill chain, and proposes adopting its vocabulary for "STIX2-based threat-intelligence interoperability".

Safeguards claimed: `CHARTER.md:137` ("Fictional scenarios only. No real nations, organisations, named individuals") and `CHARTER.md:141` (a visible provenance tag "at the interface level and not merely in a documentation footnote"). Safeguards implemented: none. The scenario's own `fiction_disclaimer` (`kestral-strait.json:7`) is read by nothing (grep across `backend` returns zero hits), appears in no API response, and appears nowhere in `frontend/index.html`. No schema field asserts a scenario is fictional. Nothing validates entity names. `COPYRIGHT.md` states a licensing position and contains no acceptable-use or field-of-use restriction. `README.md:92` states the repository is public.

Nothing prevents a fork populated with a real state, real ethno-religious cohorts, real media channels and a real grievance. The engine will load it without complaint. This is a decision for you (section 8), not a bug to fix, but the technical enforcement gap is real and should be closed regardless of which way the policy decision goes.

### 5.13 No scenario schema exists, and nothing validates anything against the published schemas

`README.md:73` says an archetype author adds "a scenario-template JSON that conforms to the existing schemas". `scaffold/schemas/` contains nine files (campaign, cohort, event, intervention, macro_state, micro_agent, narrative, outcome, relationship) and no scenario schema. The top-level keys an author must supply, `scenario_id`, `default_seed`, `archetype`, `government_structure`, `initial_macro_state`, `hidden_campaign`, `win_conditions`, `fiction_disclaimer`, are described by nothing.

Nothing in the repository ever validates any artifact against `schemas/*.schema.json`: no `jsonschema` import anywhere, and no schema-validation library in `requirements.txt`. `hidden_campaign` is stored as a raw dict (`engine.py:111`), never parsed through the `Campaign` model. The failure mode is unhandled: `engine.py:52-66` indexes required keys directly and `routes_simulation.py:43-46` catches only `FileNotFoundError`, so a scenario missing an indicator raises a bare `KeyError` as a 500.

Consequently the nine JSON Schema mirrors are decorative, and the three-way sync mandate (`CLAUDE.md:46-47`, `AGENT_TASK_TEMPLATE.md:34-35`) is enforced by nothing: there is no generator script and no sync test. The mirrors happen to be in sync today; nothing keeps them there.

### 5.14 Nothing is ever persisted, while ADR-003 and the architecture diagram say otherwise

`ARCHITECTURE_DECISIONS.md:29-31` (Status: Accepted, present tense): "We persist three things: `simulation_run` (seed + scenario), immutable `state_snapshot` per tick, and an append-only `event_log`." `scaffold/README.md:41` places "PostgreSQL (simulation_run, state_snapshot, event_log)" as the terminus of the live data-flow diagram.

`SimulationRun`, `StateSnapshot` and `EventLog` (`db/models.py:23, 42, 56`) are never instantiated anywhere; the only DB call in the application is `init_db()` (`main.py:34-36`) running `Base.metadata.create_all`. `get_db()` (`session.py:44`) is used by no route. Runs live in `_RUNS: dict[str, MeridianModel]` (`runs.py:18`), a process-local dict with no eviction.

This is compounded by working infrastructure: `docker-compose.yml` stands up `postgres:16-alpine` with a persistent `meridian_pgdata` volume and a healthcheck, so on the documented Docker path the tables are physically created, `main.py:37` logs "Database initialised.", and they stay empty forever. An auditor connecting to the database sees a correct-looking schema and empty tables.

The code is honest where the documents are not: `runs.py:3-5` says "A real build would persist via `app/db/models.py`". `ADR-004:37` and `ADR-005:45` both carry explicit "in the scaffold" caveats, which is precisely why `ADR-003`'s absence of one reads as a claim.

Related: `ADR-003:31-32` claims "Snapshots make scenario branching and Monte-Carlo batch runs cheap: fork from any tick", and the snapshot payload carries no RNG state (no `getstate` call exists anywhere in `backend/app`), so a fork built as specified would resume the generator at position 0 and diverge silently from its parent.

### 5.15 The documented Docker quick start cannot create a run

`README.md:45-49` gives `cd scaffold` / `cp .env.example .env` / `docker-compose up --build` as the first quick start, without caveat.

Two independent causes. First, `docker-compose.yml:19` sets `build: ./backend`, so `scaffold/scenarios/` (a sibling of `backend/`) is never in the image, and the backend service declares no `volumes:`. Second, `config.py:10-11` computes `REPO_ROOT = Path(__file__).resolve().parents[2]`, which resolves to `/` in the container given `WORKDIR /app` and `COPY . .` (`Dockerfile:3, 13`), making `SCENARIOS_DIR = /scenarios`.

Verified by reproducing the container layout exactly: `SCENARIOS_DIR ... exists? False`, and `runs.load_scenario('kestral-strait')` raises `FileNotFoundError`, which `routes_simulation.py:45-46` turns into a 404. Docker itself was not executed; this is confirmed by faithful layout reproduction. Note that fixing only the build context would leave the bug in place, because `REPO_ROOT` would still resolve to `/`.

`/health` and `/docs` come up cleanly, so the failure presents as a scenario bug rather than a packaging bug, and the bundled frontend's "1. Create run" button simply fails.

The local quick start does work: `python -m pytest tests -v` passes 5/5. But `pip install -r requirements.txt` fails on this machine at `requirements.txt:20` (`litellm>=1.34,<2.0`), which resolves to litellm 1.92.0, has no cp313-win_amd64 wheel, falls back to the sdist, and dies with `error: metadata-generation-failed` requiring a Rust toolchain. Because pip resolves the whole graph before installing, nothing installs. The package that breaks the documented install is the one package no code imports: `litellm` appears only inside a docstring sketch at `llm_gateway.py:17`. Whether Linux/Python 3.11 (the Dockerfile base) is affected the same way is **Unknown**; it was not tested, and `Dockerfile:7` installs `build-essential` but no Rust.

---

## 6. Minor and informational findings

Grouped. Each is real and verified; none breaks a stated commitment on its own.

### 6.1 Documentation claims not backed by code

| # | Claim | Location | Reality |
|---|---|---|---|
| 1 | "guards in CI" | `CHARTER.md:44` | No CI configuration exists anywhere; no `.github/`, no workflow, no `.git` directory at all. |
| 2 | LLM text "is versioned separately by `model_id + prompt_version + temperature`" | `ARCHITECTURE_DECISIONS.md:66-67`, `CLAUDE.md:25-26` | Present tense, nothing does this. `PROMPT_VERSION = "v1"` (`llm_gateway.py:38`) is declared and never read. |
| 3 | "seeded Monte Carlo draws" | `README.md:36` | One `rng.uniform(-0.002, 0.002)` on one of twelve indicators. No ensembles. |
| 4 | LLM "parses input into a schema-validated `intervention`" and "composes campaign content" | `README.md:39`, `:41` | Neither function exists. `llm_gateway.py` has exactly two public functions. |
| 5 | briefings "grounded by retrieval over true state" | `README.md:40` | `generate_briefing` reads two keys from a dict passed in (`llm_gateway.py:95-98`). No retrieval. |
| 6 | "The system models a **distribution**" | `CHARTER.md:61` | Effects are fixed scalar constants. `Outcome.confidence` is never constructed. |
| 7 | "Cohort belief updates: seeded diffusion over the social graph" | `README.md:37` | Beliefs move only by grievance drift. `AGENT_TASK_TEMPLATE.md:48-49` states the truth and contradicts the README. |
| 8 | "the sole writer of numeric state" | `ARCHITECTURE_DECISIONS.md:53-54`, `CLAUDE.md:13-14`, `engine.py:3` | Ownership is correct; literal file-scoping is not. Macro is assigned at `macro_state.py:47`, cohorts at `cohort_agent.py:38`. Reword rather than refactor. |
| 9 | DISARM vocabulary adopted | `plan.txt:221` | Zero occurrences of "DISARM" in any code or schema. No phase, tactic or technique field on `Campaign`. |
| 10 | Five design/research documents cited as sources of truth | `ARCHITECTURE_DECISIONS.md:4, 25, 71`; `CLAUDE.md:49`; `AGENT_TASK_TEMPLATE.md:25, 54`; `index.html:18`; `agent_schema.py:3`; `macro_schema.py:3`; `plan.txt:138, 168` | Ten references to five files that do not exist. `scaffold/README.md:95-107` shows they were consolidated into `PLAN.pdf`; the citations were not updated. `ARCHITECTURE_DECISIONS.md:4`'s "in the workspace root" is straightforwardly false. |
| 11 | "Legal-check outcome set by the engine" | `agent_schema.py:243`, `intervention.schema.json:50` | Never set. Published in a cross-language mirror. |

### 6.2 Traceability and explainability gaps

| # | Item | Evidence |
|---|---|---|
| 12 | Event log records effects but not the cause | `engine.py:165-173` logs `event_id`, `tick`, `type`, `actors_involved`, `effects`. `action_type`, `rationale`, `parameters` and `confidence` are all discarded. |
| 13 | `causal_parents` never populated | Declared `agent_schema.py:224`, mirrored `event.schema.json:58`, assigned nowhere. `Event(` is never instantiated; the engine appends raw dicts, so the log is unvalidated. |
| 14 | Most state changes emit no event | Macro noise (`engine.py:135-136`), cohort drift (`cohort_agent.py:35-38`) and every diffusion step are unlogged. `observe` and unknown actions produce no record either, because `engine.py:163` gates logging on a non-empty delta. |
| 15 | Logged effects are intent, not outcome | `engine.py:171` logs the requested delta; `apply_deltas` clamps silently and returns `None` (`macro_state.py:23, 43-44`). Measured at seed 88213 over 120 ticks: summed `military_readiness` effects imply 1.59 against an actual 1.0. |
| 16 | `derivation` is a frozen constant | `engine.py:68` sets `"rules_engine_v1 + seed_init"` once. Every snapshot at every tick reports identical provenance. |
| 17 | No random draw is ever recorded | Stream, index, distribution, parameters and value are all discarded at `engine.py:135`, `diffusion.py:75`, `cohort_agent.py:36`. |
| 18 | No state hashing, no per-tick digest | No `hashlib`/`sha256` anywhere in `backend/app`. Divergence cannot be bisected. (A digest over floats is a poor fix; comparing `snapshots` plus meso is better.) |
| 19 | Snapshot series unreachable by any client | `self.snapshots` is appended at `engine.py:116`/`:180` and read only by `tests/test_engine.py:30`. No `/snapshots` route exists; the WS stream sends only the current tick. |
| 20 | Event log fully readable, `visibility` never set | `routes_simulation.py:104-111` returns everything. `EventVisibility` (`agent_schema.py:203-208`) is defined and never populated. Not a defect today (there is no auth layer at all, by design), but it is where the role-asymmetry mechanic will have to attach. |

### 6.3 Correctness and robustness

| # | Item | Evidence |
|---|---|---|
| 21 | Pydantic bounds are inert at runtime | No model sets `validate_assignment`. `apply_deltas({"inflation_rate": -5.0})` drives inflation to -4.959 with no error, and the snapshot still passes `model_validate`. |
| 22 | Bounds enforcement is a four-name literal | `macro_state.py:30-35`. The eight nested 0..1 values (institutional trust, alliance confidence) are structurally unreachable, because `:38-41` skips non-scalar attributes, despite `:26-27` claiming the engine handles nested blocks explicitly. It does not. |
| 23 | Shipping clamp contradicts its own published schema | `macro_schema.py:46-48` and `macro_state.schema.json` declare `minimum: 0` with no maximum; `macro_state.py:34, 44` clamps to 1.0. Recovery above pre-crisis baseline is unrepresentable in code and legal in the contract. |
| 24 | Diffusion divides by zero on schema-valid data | `diffusion.py:67-71` has no guard on `total_w`; `internal_cohesion` allows `ge=0` (`agent_schema.py:83-85`). Two zero-cohesion bridged cohorts raise `ZeroDivisionError` inside the tick loop: unhandled 500, dropped WebSocket. |
| 25 | Diffusion silently drops schema-valid edges | `diffusion.py:33-36` guards with `if other in cohesion:`, but `agent_schema.py:86-88` documents `bridges_to` as cohorts *or institutions*. An institution target is discarded with no warning. Also, `diffusion.py:51` claims adoption is monotonic non-decreasing; the jitter at `:75` does not guarantee that. |
| 26 | WebSocket accepts any origin and unbounded ticks | `routes_ws.py:26` accepts unconditionally; `:38, :41` read `ticks` with no cap, against `le=1000` on the REST path (`routes_simulation.py:37`). A large N grows `event_log` and `snapshots` without bound. The sync REST `advance` handler and the async WS handler can also interleave `step()` on one shared model with no lock. |
| 27 | Mesa's `seed=` kwarg to `super().__init__` is inert | mesa 2.4.0 seeds in `Model.__new__` from the original constructor call (`mesa/model.py:58-71`); `Model.__init__` ignores it. On the API path (`seed=None`) Mesa's `self.random` is seeded from entropy. Harmless today (nothing reads it, and no scheduler or `AgentSet.shuffle` is used), but a one-character typo (`self.model.random` for `self.model.rng`) would break reproducibility silently. |
| 28 | One shared RNG stream, no named substreams | Adding a draw in one subsystem shifts every later draw that tick. Not currently a defect (the design is documented as one RNG in ADR-007) but it means seeds are not comparable across code versions or scenario variants. |
| 29 | `DEFAULT_SEED` setting is read by nothing | Declared `config.py:27`, documented in `.env.example`; `settings.default_seed` has zero call sites. `engine.py:81` falls back to the scenario file instead. |
| 30 | `.env` is loaded from the wrong directory | `config.py:17` sets `env_file=".env"` (relative to cwd); both quick starts place it in `scaffold/` and run from `scaffold/backend`. Every documented local setting is silently ignored, with no error. |
| 31 | `llm_mode` is read only by `/health` | `main.py:45` echoes it. Setting `LLM_MODE=live` changes nothing except the health payload, which will report "live" for a stub run. |

### 6.4 Testing

| # | Item | Evidence |
|---|---|---|
| 32 | The suite is 5 tests in 1 file, 78 lines | `tests/test_engine.py`. Nothing imports `diffusion`, `cohort_agent`, `macro_state`, or any schema. |
| 33 | Zero API, WebSocket or DB tests | No `TestClient` anywhere, though `httpx` ships under `# Tests` (`requirements.txt:24`) for exactly that purpose. |
| 34 | Zero invariant tests | Nothing asserts bounds hold, that no indicator pins at a clamp, that a scenario validates, that mirrors match models, or that a malformed scenario is rejected. Every defect in sections 4 and 5 survived the suite. |
| 35 | `test_macro_state_actually_changes` depends on the stub's specific choice | `tests/test_engine.py:52-58` asserts `military_readiness` moves, reachable only via `request_procurement_acceleration` (`engine.py:36`). Honest for stub mode; will need revisiting when the gateway goes live. |

### 6.5 Dependencies, packaging and governance

| # | Item | Evidence |
|---|---|---|
| 36 | No lockfile, no hashes, no pins | Every line in `requirements.txt` is a range; `websockets>=12.0` has no upper bound at all. No `pyproject.toml`, no `*.lock`, no `--require-hashes`. A build today and in six months resolve differently, and nothing records which set produced a given run. |
| 37 | The repository is not under version control | `git rev-parse` returns "fatal: not a git repository". No history, no author, no diff, no remote. The `.gitignore` is therefore inert. This makes every GitHub-level control (CODEOWNERS, branch protection, secret scanning, required checks) not inadequate but inapplicable. |
| 38 | No CI, no lint, no typecheck, no SBOM, no CVE scan | The only YAML in the project is `docker-compose.yml`. `.gitignore:16-18` pre-ignores `.mypy_cache/` and `.ruff_cache/`; neither tool is installed or configured. `CLAUDE.md:48` mandates "Type-hint everything" with no enforcement (the code currently complies). |
| 39 | psycopg2-binary is LGPL, contradicting "permissive licensing" | `requirements.txt:17`; installed metadata reads "License: LGPL with exceptions". `scaffold/README.md:111` says "Stack chosen for permissive licensing". Commercially benign under the SaaS model `PLAN.pdf` assumes (dynamic linking, no distribution), but the sentence is inaccurate and psycopg2 is absent from the PLAN §2 licence audit. |
| 40 | No LICENSE file | `README.md:92-94` states an all-rights-reserved position in prose. The legal default happens to align, but the position is undiscoverable by tooling. See section 8, decision 1. |
| 41 | `litellm` and `python-socketio` ship in the image, imported by nothing | `Dockerfile:11` installs everything. `litellm` appears only in a docstring; `python-socketio` has zero occurrences outside `requirements.txt`. `litellm` also carries a large provider-SDK tree and is the package that breaks the documented install (5.15). |
| 42 | Container runs as root with a resident compiler | `Dockerfile` has no `USER`; `:6-8` installs `build-essential` and `libpq-dev` into the single final stage, both unnecessary given `psycopg2-binary`. There is no `.dockerignore`, so `COPY . .` would bake `backend/.venv/` into the image. Dev-only today; a pre-deployment item, not a live defect. |
| 43 | No Alembic, no migration path | `create_all` only (`session.py:37-41`). Inert while nothing is persisted; sequence this after persistence, not before. |
| 44 | ADRs carry no date, decider, consequences, reversal cost or review trigger | All nine follow title + "Status: Accepted" + prose. No supersession mechanism beyond "do not re-litigate without a new ADR" (`:7`). No ADR template file. |
| 45 | Branch/PR policy is three bullets under an unresolved marker | `CLAUDE.md:59`: `<!-- PLACEHOLDER: fill in with the team's real conventions -->`. This is the only unresolved marker in the whole project, which is a good result; the defect is what sits under it. |
| 46 | No requirement IDs, no traceability matrix | The four commitments and the eight questions carry no identifiers. Commitments 1 and 2 have tests; commitments 3 and 4 have none. |
| 47 | `backend/plan.txt` is an uncontrolled 498-line duplicate of `PLAN.pdf` | Referenced by no document, and baked into the Docker image by `COPY . .`. Two copies of the "source of truth" will drift, and the copy is the one that ships. |
| 48 | No CHANGELOG, no versioning policy, no scenario version field | The only version string is `main.py:22` `version="0.1.0"`. `SimulationRun` records `scenario_id` (a filename) with no content hash, so editing a scenario silently invalidates recorded runs with no signal. |
| 49 | No provenance tag on generated text at the interface | `routes_simulation.py:76` returns `briefing` as a bare string beside `macro_state`. The only marker is `[STUB briefing — ...]` (`llm_gateway.py:100`), which vanishes the moment a real model is wired in. `CHARTER.md:141` requires the tag "at the interface level". |
| 50 | No CORS middleware, so the documented frontend workflow fails | `scaffold/README.md:91-92` says to open `frontend/index.html` in a browser; `index.html:41-45` issues a cross-origin JSON POST, which preflights against an app with no `CORSMiddleware` and is blocked before the server sees it. |

---

## 7. Foundation deliverable status

Every required SDLC and governance deliverable, one status each.

| Deliverable | Status | Notes |
|---|---|---|
| Product charter / vision | Present and adequate | `CHARTER.md` is genuinely good and correctly declares itself normative. It needs a version, date and owner, and the "guards in CI" clause at line 44 removed. |
| Architecture decision record | Present but inadequate | Nine ADRs with sound rationale; no dates, deciders, alternatives, consequences, security/licence/operational impact, reversal cost, review trigger, or supersession states. ADR-003 and ADR-006 additionally overclaim (5.14, 5.4). |
| Requirements / PRD | Present but inadequate | `PLAN.pdf` §3 to §6 is the substance. Not decomposed into identified, traceable requirements. |
| Requirements traceability matrix | Missing | No IDs on the four commitments or eight questions; no mapping to modules or tests. |
| Roadmap / phase gates | Present but inadequate | `PLAN.pdf` §11 defines Phase 0/1/2 with explicit go/no-go gates. No dates, no owner, and it lives only inside a PDF. |
| Milestones | Missing | Phases exist; dated milestones do not. |
| RAID / risk register | Missing | Risks appear as prose plus a licensing risk table in `PLAN.pdf` §2.2-2.3. No register with owners, likelihood, mitigation and review dates. |
| Definition of Ready | Present but inadequate | `AGENT_TASK_TEMPLATE.md:12-40` is functionally a readiness structure; not named or adopted as one. |
| Definition of Done | Present but inadequate | `AGENT_TASK_TEMPLATE.md:32-37` acceptance criteria are good and include a mandatory determinism check. Not enforced anywhere. |
| Change control | Present but inadequate | `ARCHITECTURE_DECISIONS.md:7`, `CLAUDE.md:57-62` and `PLAN.pdf` §7.3 all specify controls; none is wired, and `CLAUDE.md:59` is an unresolved placeholder. |
| Version control | Missing | No `.git` anywhere. This blocks branch protection, CODEOWNERS, required checks and secret scanning as a class. |
| CI pipeline | Missing | No configuration of any kind. `CHARTER.md:44` claims otherwise. |
| Lint / typecheck / format config | Missing | `.gitignore` anticipates ruff and mypy; neither is installed or configured. |
| Test strategy | Present but inadequate | 5 tests, 1 file. Commitments 1 and 2 partially covered; 3 and 4 uncovered; meso, diffusion, API, DB and invariants entirely uncovered. |
| Dependency management policy | Missing | Ranges, no lockfile, no hashes, no upper bound on `websockets`, no dependency review, no Dependabot/Renovate. |
| SBOM | Missing | Specified in `PLAN.pdf` §7.6 as a future CI gate; not built. |
| Vulnerability management | Missing | Specified in `PLAN.pdf` §7.5 (Grype in CI); not built. |
| Licence inventory | Present but inadequate | `PLAN.pdf` §2 is a real audit with SPDX classification. psycopg2-binary (LGPL) is absent from it and contradicts `scaffold/README.md:111`. |
| Project licence file | Requires human decision | No LICENSE file. Position stated only in `README.md:92-94`. Deliberately not selected here: see section 8, decision 1. |
| Threat model | Present but inadequate | `PLAN.pdf` §8 maps OWASP LLM Top 10, MITRE ATLAS and NIST AI RMF. Not decomposed to this codebase's actual trust boundaries, and not implemented. |
| IAM / authorisation model | Present but inadequate | `PLAN.pdf` specifies Keycloak plus Postgres RLS for Phase 2. Zero implementation; no auth layer of any kind exists, which is acceptable for a scaffold but blocks the role-asymmetry mechanic. |
| Secrets management | Present and adequate | `.gitignore:24-28` covers `.env`, `.env.*`, `*.pem`, `*.key` with a correct `!.env.example` negation. No real secret exists, and no code reads an API key. Secret scanning is Missing (and inapplicable without git). |
| Incident response | Missing | No SECURITY.md, no reporting channel, no SLA, no owner. |
| Responsible-use / acceptable-use policy | Requires human decision | `CHARTER.md:135-142` is the entire policy and is unenforced prose. See 5.12 and section 8, decision 6. |
| Data classification / retention | Missing | Not addressed anywhere. |
| Persistence and migration strategy | Present but inadequate | Schema designed (`db/models.py`), ADR accepted, zero write path, no Alembic, no RNG state in the snapshot shape. |
| Scenario data contract | Missing | No scenario schema; nothing validates against the nine published mirrors (5.13). |
| Observability / logging | Present but inadequate | An in-memory event log exists and is exposed. No rule id, no causal parents, no uncertainty, no persistence, no structured logging config. |
| Release / versioning policy | Missing | No CHANGELOG, no SemVer policy, no tags, no scenario or rule-pack versioning. |
| Contribution guide | Missing | No CONTRIBUTING.md; `CLAUDE.md:57-62` is the substitute and is placeholder-marked. |
| Code of conduct | Missing | Not required pre-publication; required if the repository goes public and accepts contributions. |
| Publication readiness gate | Missing | No checklist exists, and `README.md:92` already states the repository is public. |

---

## 8. Requires human decision

These are yours. Each is stated as a question with the constraint that bears on it; none is answered here.

1. **Project licence.** No LICENSE file exists; `README.md:92-94` asserts all rights reserved in prose. Deliberately not selected in this audit, because the choice is commercial, not technical. The relevant constraints: `ADR-002:24-25` records that GPL engines were ruled out because "the product may be commercialised", the stack is otherwise permissive, and psycopg2-binary is LGPL (benign for non-distributed SaaS, not benign if you ever ship a binary). Decide the licence, then add the file so tooling can detect it, and add a NOTICE file if you keep Apache-2.0 dependencies.

2. **Repository visibility and the publication gate.** `README.md:92` states the repository is public. It is not currently in git at all, so the claim is aspirational. Given sections 5.12 and 6.1, publishing today would publish a set of documented claims that are false, and an influence-operations targeting schema with no acceptable-use terms. Decide: private first with a publication checklist as the gate, or public with the false claims corrected first. Do not do neither.

3. **Whether Mesa remains the ABM substrate.** Mesa is currently used only as a vestigial base class: no scheduler, no `AgentSet`, no `shuffle`, plain-list iteration in `engine.py:152` and `:159`. In exchange, it materialises a second `random.Random` whose seeding on the API path comes from entropy (6.27), pulls a large Jupyter/matplotlib dependency tree, and introduces a `Model.rng` attribute collision on any future 3.x upgrade. The alternative is dropping the dependency and owning the tick loop outright, which is roughly what the code already does. This is a real trade-off: Mesa buys credibility as a recognised ABM framework, and `ADR-002` cites that. Your call.

4. **How honest the public reproducibility claim should be.** Three options, in increasing order of both honesty and cost. (a) Restate the claim conditionally: "same seed + same scenario + same recorded proposal stream". Cheap, accurate, slightly less impressive. (b) Build record/replay so the unconditional claim becomes true once a live model is wired. Moderate cost, and the RNG stream is already invariant to proposal content, so it works. (c) Demote the LLM to ranking a candidate action set the engine enumerates, making selection an engine decision. Highest cost, strongest claim, and it changes the product's character. Decide before writing more marketing surface on top of the current wording.

5. **Whether to adopt uv and `pyproject.toml`.** The current flat `requirements.txt` with open ranges and no lockfile is the direct cause of the broken install in 5.15 and of the reproducibility caveat in 6.36. Moving to `pyproject.toml` plus a hash-pinned lock would fix both, but it changes four documented workflows (`README.md:56-57`, `scaffold/README.md:58, 69-70`, `CLAUDE.md:33`) and the Dockerfile. Worth doing, but it is a deliberate migration, not a fix to slip in.

6. **Dual-use and responsible-use policy for the influence-operations model.** The schema is a working audience-targeting and campaign-design template, the plan claims a DISARM Red Framework correspondence, and the only safeguards are three prose bullets. Decide what you actually want here: an explicit acceptable-use / field-of-use restriction in the licence, an enforced `fictional: true` assertion plus a real-entity check at scenario load, surfacing `fiction_disclaimer` in every API response and in the UI, or keeping the repository private. These are not mutually exclusive, and the technical enforcement is worth building whichever way the policy goes.

7. **Whether `PLAN.pdf` remains the canonical plan format.** Its prose extracts cleanly, its tables do not, it cannot be line-diffed in review, and `backend/plan.txt` is already an uncontrolled duplicate of it inside the build context. Converting to markdown would fix all three; keeping the PDF is defensible if it is treated as a published artifact with the markdown as source.

---

## 9. Phased correction plan

Ordered so that foundation precedes features, and so that the repository stops asserting untrue things before anything else happens. Every exit criterion is testable.

### Phase 0: Stop and tell the truth

The repository currently contains live untruths. This phase changes no behaviour and adds no features; it makes the documents match the code.

**Entry:** this audit accepted.

**Work:** correct or caveat every item in 6.1. Specifically: delete "in CI" from `CHARTER.md:44`; make `ARCHITECTURE_DECISIONS.md:66-67` and `CLAUDE.md:25-26` conditional; add "in the scaffold" caveats to `ADR-003` matching the existing `ADR-004:37` and `ADR-005:45` convention, and annotate the Postgres node in the `scaffold/README.md:41` diagram as planned; soften `ADR-006:54-55` and the six sibling claims to describe what `_validate_and_price` actually does; mark the unimplemented rows of the `README.md` determinism table as planned; correct `README.md:36` to "seeded stochastic draws"; correct `README.md:37` to "grievance-driven drift, diffusion adoption computed but not yet wired to beliefs"; qualify `README.md:106-107` and `ADR-008:75` to state the current archetype constraints; reword the "sole writer" sentences; repoint the ten dangling design-doc citations at their `PLAN.pdf` sections; reword `Intervention.legal_check`, `CampaignMetrics`, `Outcome` and `diffusion.py:5` docstrings out of the present indicative; correct `scaffold/README.md:111` to acknowledge psycopg2's LGPL; correct `coastal-creole-fishing.represents_population` in the demo scenario; resolve or delete the `CLAUDE.md:59` placeholder; delete `backend/plan.txt`.

**Exit:**
- A reviewer can read `CHARTER.md`, both READMEs, `CLAUDE.md` and `ARCHITECTURE_DECISIONS.md` and find no present-tense claim contradicted by the code. Verified by re-running the section 6.1 checks.
- `grep -rn "design_.*\.md\|research_.*\.md"` over project files returns zero results, or only results pointing at files that exist.
- `grep -rn "in CI"` returns nothing that is false.
- No unresolved `PLACEHOLDER` marker remains.

### Phase 1: Version control, CI and dependency floor

Nothing else is verifiable until changes are tracked and checks run.

**Entry:** Phase 0 exit met.

**Work:** `git init`, commit the tree as a documented baseline, push to a **private** remote. Add a hash-pinned lockfile (pip-compile or uv per decision 5) and install from it in the Dockerfile. Cap or remove `litellm` (nothing imports it) so the documented install resolves. Add `requires-python`. Add a CI workflow running pytest, ruff and mypy on push and PR, and make it required. Add a `.dockerignore`.

**Exit:**
- `git log` shows a baseline commit; the default branch is protected with a required status check.
- `pip install -r requirements.lock && python -m pytest tests -v` succeeds from a clean environment on both Windows and the Docker base image; the exact command is recorded in the README with the date it was last run.
- CI is green on a trivial PR, and demonstrably red when the determinism test is deliberately broken.
- `docker build` produces an image that does not contain `.venv` or `plan.txt`.

### Phase 2: Determinism, replay and the boundary guard

**Entry:** Phase 1 exit met.

**Work:** Add an `llm_interaction` record (run_id, tick, agent_id, call_index, model_id, prompt_version, temperature, prompt_hash, response_json, response_hash) written on every gateway call. Add a three-way gateway mode (live / record / replay) keyed off `settings.llm_mode`, which currently gates nothing. Replace the tautological boundary assertions with an AST import check plus a live-state mutation check. Extend the determinism test to cover meso. Fix or document the Mesa second-RNG hazard per decision 3.

**Exit:**
- `test_llm_gateway_cannot_write_state` **fails** when a gateway that imports `MacroStateHolder` and mutates it is substituted. Demonstrate this in the PR.
- `test_same_seed_is_deterministic` **fails** when `CohortAgent.step` is patched to draw from global `random`, and when the cohort order in the scenario is reversed. Demonstrate both.
- A run recorded with a non-deterministic stub replays to byte-identical macro, meso and event-log state.
- `LLM_MODE=live` either works or raises `NotImplementedError`; `/health` never reports a capability the gateway does not have.

### Phase 3: State completeness and event sourcing

**Entry:** Phase 2 exit met.

**Work:** Make the snapshot a full checkpoint: macro, meso (cohort beliefs, `narrative_adoption`), `rng.getstate()`, tick. Add `MeridianModel.from_snapshot`. Construct validated `Event` objects rather than raw dicts, carrying `action_type`, rule id, `causal_parents`, the RNG draw, the requested delta and the realised delta. Emit events for macro noise, cohort drift, diffusion, rejections and no-ops. Have `apply_deltas` return realised deltas and rejected keys. Wire persistence: a `SimulationRun` row on create, a `StateSnapshot` per tick, `EventLog` rows on append, with rehydration on cache miss. Add Alembic. Expose a snapshot-history endpoint.

**Exit:**
- `run(20)` equals `run(10)` then snapshot, then `from_snapshot`, then `run(10)`, asserted as a test.
- Every macro and meso mutation in a 100-tick run has a corresponding event; asserted by a test that counts mutations against events.
- Summing logged `effects` over a saturating run reproduces actual state exactly (this currently diverges by 0.59 on `military_readiness`).
- A run survives a process restart and is retrievable by id.
- Each of the eight `CHARTER.md:120-127` questions is answerable from a persisted event by a documented query; the ones that are not yet answerable are listed explicitly rather than implied.

### Phase 4: Real validation, cross-tier wiring and the two critical defects

This is where the simulation becomes a simulation.

**Entry:** Phase 3 exit met.

**Work:** Add `schemas/scenario.schema.json` and validate every scenario at load, returning 422 with the failing path rather than 500. Parse `hidden_campaign` through the `Campaign` model. Make `_validate_and_price` a real gate returning a typed verdict, reading `constraints`, `resources` and current world state. Split the wire model from the state model on `/decision`. Route player interventions through the same gate. Wire the tiers: macro snapshot into `CohortAgent.step` via `income_sensitivity_to_shipping_disruption`; cohort beliefs, weighted by `represents_population`, aggregating into macro; a real world-state view into `InstitutionalAgent` context; narrative adoption into belief. Make belief bidirectional and grievances mutable. Add cost, cooldown and decay. Enable `validate_assignment` (or per-tick snapshot validation), derive the clamp set from field constraints, support nested keys in `apply_deltas`, guard the diffusion zero-weight case.

**Exit:**
- The same action applied in two different world states produces different deltas, asserted by a test. This is `CHARTER.md:53`.
- A 500-tick run has no indicator at a clamp boundary and no cohort belief at 0.0 or 1.0, asserted by a test.
- A counter-narrative action measurably raises at least one cohort's belief, asserted by a test.
- Every currently frozen macro indicator either moves under some rule or is removed from the demo scenario.
- A malformed scenario returns 422 with a JSON pointer to the failing field; a zero-cohesion scenario runs without exception.
- A client cannot set `legal_check`, `resource_cost` or `action_id`; asserted by a test.

### Phase 5: Rule packs and archetype extensibility

**Entry:** Phase 4 exit met.

**Work:** Move the action catalogue (effects, costs, prerequisites, permitted roles, timelines) and the per-tick macro drift rules into scenario or rule-pack data with a schema and a version. Split macro indicators into a required core plus a scenario-declared extension map, so a landlocked nation need not declare strait shipping. Move the role-to-action mapping out of the gateway. Add a rule-pack id and content hash to `SimulationRun` and `MacroState`. Begin representing the sixteen `CHARTER.md:87-111` consequence primitives.

**Exit:**
- A second, deliberately dissimilar scenario (landlocked, non-parliamentary, different indicator set, different role names, at least one novel action) loads and produces a non-zero event count over 50 ticks, with **zero** changes to any file under `backend/app`. This is the real test of `ADR-008`, and it is the one that currently fails.
- Reproducibility holds across both scenarios.
- Two runs with the same seed and different rule-pack hashes are detectably different runs, not silently comparable ones.

### Phase 6: SDLC documentation and publication readiness

**Entry:** Phase 5 exit met, and decisions 1, 2, 4 and 6 taken.

**Work:** Author SECURITY.md, CONTRIBUTING.md, a RAID register with named owners, a dated roadmap, a CHANGELOG and a SemVer policy, an ADR template with the missing fields (and backfill dates and deciders for the existing nine, even as "2026-07, sole author"), a requirements traceability matrix with IDs for the four commitments and the eight questions, a responsible-use policy per decision 6, and the LICENSE file per decision 1. Implement the `CHARTER.md:141` provenance envelope on generated text and surface `fiction_disclaimer` at the interface. Add an enforced fictional-scenario assertion. Add SBOM generation, `pip-audit` and a licence allowlist to CI. Add CORS with an explicit allowlist, and auth if the role-asymmetry mechanic is being built. Convert `PLAN.pdf` per decision 7. Write the publication readiness checklist and run it.

**Exit:**
- Every row in the section 7 table reads Present and adequate, or has an explicit dated waiver signed off by you.
- The publication checklist passes: no false claims, no secrets in history, LICENSE present and detected, security contact present, provenance tag implemented, no real-world entities in any scenario, acceptable-use terms present.
- Only then does the repository go public.

---

## 10. Verification checklist for completion

Each item is a single assertion that either passes or fails. "The foundation is repaired" means all of these pass. Nothing short of that should be described as repaired.

**Truthfulness**

- [ ] No present-tense claim in `CHARTER.md`, `README.md`, `scaffold/README.md`, `CLAUDE.md` or `ARCHITECTURE_DECISIONS.md` is contradicted by code; each of the 11 items in section 6.1 has been individually re-checked.
- [ ] Every document citation resolves to a file that exists.
- [ ] Every ADR that describes unbuilt work carries an explicit scaffold caveat.

**Determinism and reproducibility**

- [ ] `test_same_seed_is_deterministic` compares macro, cohort beliefs, `narrative_adoption` and `event_log`.
- [ ] It fails when unseeded global randomness is injected into `CohortAgent.step`.
- [ ] It fails when the cohort order in the scenario is reversed.
- [ ] `test_llm_gateway_cannot_write_state` fails when the gateway imports and mutates `MacroStateHolder`.
- [ ] An AST check asserts `llm_gateway.py` imports no state object, and it fails when such an import is added.
- [ ] A recorded run replays byte-identically under a deliberately non-deterministic gateway.
- [ ] Two same-seed runs in separate processes under differing `PYTHONHASHSEED` hash identically over full state.

**State and traceability**

- [ ] `run(20) == run(10) -> snapshot -> from_snapshot -> run(10)`.
- [ ] A 100-tick run produces one event per state mutation, verified by count.
- [ ] Summing logged effects reproduces final macro state exactly.
- [ ] Every event validates against `Event`, and `causal_parents` is non-empty wherever a cause exists.
- [ ] A run survives a process restart and is retrievable.
- [ ] Each of the eight charter questions has a documented query, or is explicitly listed as not yet answerable.

**Behaviour**

- [ ] The same action in two different world states produces different deltas.
- [ ] No indicator sits at a clamp boundary over a 500-tick run.
- [ ] No cohort belief is absorbing: a counter-narrative action raises at least one cohort's belief.
- [ ] Every macro indicator either moves under some rule or has been removed from the demo scenario.
- [ ] Cohort aggregation is population-weighted, and the demo populations sum consistently with a declared total.

**Validation and safety**

- [ ] A malformed scenario returns 422 with the failing field path, never a 500.
- [ ] A zero-cohesion scenario does not raise.
- [ ] An unauthorised role-action pair is rejected with a reason code and a logged event.
- [ ] A client cannot set `legal_check`, `resource_cost`, `timeline_days` or `action_id`.
- [ ] An unknown action type produces a logged rejection, not silence.
- [ ] A scenario failing the fictional-entity assertion is refused at load.
- [ ] Generated text reaches the client inside a provenance envelope, and a test asserts no bare LLM string is ever returned.

**Build and governance**

- [ ] `pip install` from the lockfile, then `pytest`, succeeds from clean on Windows and in the container; the date of the last verification is in the README.
- [ ] Both documented quick starts (Docker and local) run end to end and successfully create a run; the date is recorded.
- [ ] CI is required, green on main, and demonstrably red when any determinism or boundary test is broken.
- [ ] SBOM generated per build; `pip-audit` and the licence allowlist pass.
- [ ] A second, deliberately dissimilar scenario runs with zero changes under `backend/app`.
- [ ] Every row in the section 7 table reads Present and adequate or carries a dated waiver.

---

## Appendix A: findings raised and dismissed

Eleven candidate findings were raised during analysis and refuted on verification. They are recorded so that they are not re-raised.

| Finding | Reason dismissed |
|---|---|
| Test dependencies ship in the production image | There is no production image. The Dockerfile's only consumer overrides the command with `--reload` and installs a compiler toolchain; it is a dev image by construction. No document claims dependency groups or minimal runtime images. |
| Compose uses `--reload` with default credentials and publishes 5432 | Correctly labelled local defaults (`.env.example:1`, "safe local defaults; the scaffold runs without secrets"), correctly gitignored, and no document claims deployment readiness. `--reload` is additionally inert, since no volume is mounted. |
| The reproducibility test cannot detect dependency drift | `scaffold/README.md:64-65` defines the claim in the same sentence ("two runs with the same seed produce identical macro state after N ticks"), which is exactly what the test does. No document claims cross-version stability. The related real issue (unpinned deps) is recorded separately at 6.36. |
| No model-weight or dataset licence inventory | No weights or datasets exist in the repository; nothing is downloaded, vendored or redistributed. `PLAN.pdf` contains a real licensing audit, and `README.md:92-94` states the licensing position. The finding also missed both. |
| Deprecated `@app.on_event` plus floating ranges makes a build break inevitable | Refuted empirically: the shipped `.venv` already runs fastapi 0.139.2 and websockets 16.1.1, the app starts, and the suite passes. The `<1.0` bound the finding indicts is precisely the guard against the failure it predicts. |
| Lint and typecheck are assumed but not configured | `.gitignore` pre-ignores absent tooling as a habit (it also ignores `.tox/`, `*.sqlite3` and `node_modules` for a Postgres-only project with one HTML file). No document claims lint or typecheck exists, and the code currently complies with the type-hint rule anyway. |
| The `.env` invites API keys that config silently discards | The keys are commented out, under a header reading "Example real values (unused while LLM_MODE=stub)", in a file whose first line says the scaffold runs without secrets. `extra="ignore"` is load-bearing: setting `extra="forbid"` raises eight validation errors against the project's own `.env.example` and breaks startup. |
| The event log is fully readable with no visibility filtering | No document claims per-role filtering, and there is no auth layer anywhere, so this is not endpoint-specific. Recorded instead as a forward item at 6.20. |
| Governance artifacts are locked in an undiffable binary PDF | `pdftotext` is available in this environment and extracts 61k characters of clean text; all seven section citations made by the READMEs check out exactly. Recorded instead as a format preference at decision 7 and a duplication issue at 6.47. |
| RAID, change control, definition of ready, roadmap and milestones are all missing | The roadmap (`PLAN.pdf` §11) and change control (§7.3, §7.4, plus `CLAUDE.md:57-62`) exist; the finding's file inventory omitted `PLAN.pdf` entirely. The genuine residue (no RAID register with owners) is recorded in section 7. |
| Full governance inventory: zero items present-adequate, 16 missing | The same omission. `PLAN.pdf` contains the threat model (§8), IAM model, vulnerability management and dependency review policy (§7.5-7.6) that this finding declared missing. |

---

## Appendix B: on severity

Roughly two thirds of the candidate findings were confirmed on the facts but downgraded, because the original grading counted honestly-labelled scaffold omissions as defects. That was corrected consistently: the test applied throughout is whether a document claims a property the code lacks, or whether a design choice actively blocks the stated architecture. Absence alone, when disclosed, is not a defect.

Final counts, after merging items that appeared under more than one analytical dimension: **2 critical, 15 major, approximately 50 minor and 45 informational, with 11 refuted**. The two critical findings are behavioural and were surfaced last, by asking what the system actually does when you run it rather than what the code says. That ordering is worth noting: the documentation defects are numerous and embarrassing, but they are cheap to fix. The two critical findings are the ones that determine whether this becomes a simulation.

---

## Amendment of 19 July 2026 — §8 decision 6 has been settled

**Appended, not applied in place.** Nothing above this heading has been altered and no line number above has moved, because many records cite this audit by `path:line` — including `:397-413`, `:405`, `:409`, `:411` and `:413`. This audit is a closed record and stays as written.

**§8 decision 6 — "Dual-use and responsible-use policy for the influence-operations model" (`:411`) — was settled by founder decision on 18 July 2026.** Three consequences a reader of §8 should carry:

1. **The option list at `:411` is no longer the live menu.** It offered an acceptable-use or field-of-use restriction in the licence, an enforced `fictional: true` assertion plus a real-entity check at load, surfacing `fiction_disclaimer` everywhere, or staying private, and noted they were not mutually exclusive. The decision is broader than any of them and **reorders their standing**: it names eight controls, and the eighth makes the licence-side and disclosure-side measures **supplementary** while **technical enforcement is mandatory**. The audit's closing sentence at `:411` — "the technical enforcement is worth building whichever way the policy goes" — has in effect been adopted as the policy.

2. **Settling it did not clear publication blocker B5.** The same question is B5 (`A3-VERIFICATION-RESULTS.md:245`). It now clears only when the eight controls are **implemented and verified**, and **none of the eight exists in code**. The gate is larger after the decision than before it.

3. **Of §8's seven items, four are now settled** — 8.1 licence, 8.2 visibility, 8.4 reproducibility wording, and 8.6 — **leaving 8.3 (ABM substrate), 8.5 (packaging tooling) and 8.7 (canonical plan format) open.** Any record that counts four §8 items as open is quoting the pre-decision position.

Where the settled position is recorded: `RAID-REGISTER.md` DEC6 (the decision in the founder's own terms), `PUBLICATION-EXIT-CRITERIA.md` C6 (the eight controls as criteria B5-1 to B5-8, each with a verifiable test form), `CORRECTIVE-BACKLOG.md` CB-40 to CB-47, `PHASE-0-REMEDIATION-PLAN.md` §P0.8, and `../safety/IDENTITY-AND-BIAS-GUIDELINES.md` §9.

**Nothing in this amendment reopens the audit, changes any finding, or alters any count in Appendix B.**

---

## Redaction note — 19 July 2026

**One redaction has been made to this document, recorded here rather than made silently.**

The `**Scope:**` line at the top originally named the auditor's absolute local filesystem path.
That path exposed a personal account name and local directory structure, and is incidental to the
audit rather than evidence for any finding: the scope it describes is the repository root, which is
unambiguous without it. It has been replaced with "the repository root".

**Nothing else in this document has been altered by this redaction.** No finding, no evidence, no
numeric result and no citation was changed, and no other absolute path appears in the file. The
redaction was made in preparation for the repository's first push, under the standing rule that
historical records are amended in the open and never quietly rewritten.
