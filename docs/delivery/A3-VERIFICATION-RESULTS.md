# A3: Targeted Re-Verification Results

**Date:** 18 July 2026
**Status:** complete. Broad audit CLOSED.
**Scope:** the five validation/authority findings whose adversarial verifiers failed with API errors during the broad audit, plus one independent adversarial re-derivation of each of the two critical findings.

---

## Plain-English summary

Seven checks were run. Nothing was refuted outright. Two findings were corrected in an important way, and one of those corrections uncovered a defect nobody had identified before.

The headline correction: the audit said the three simulation tiers never influence one another. That is true in one direction and *misleadingly* true in the other. Changing a cohort's beliefs genuinely does change national indicators, which looks like the tiers are connected. They are not. The connection is an accident of how random numbers are drawn, not a modelled cause. A separate defect was found underneath it.

The second correction strengthens rather than weakens the audit: the runaway saturation of the macro indicators was suspected to be an artefact of the stub, which would have made it a minor problem that disappears once a real model is connected. It is not. It persists with varied actions, and the engine contains no cost, cooldown, decay or opposing-pressure mechanism of any kind. That moves it from a tuning problem to an architectural gap.

**Publication blockers after A3: 5 (unchanged).** No new blocker was created. No result forces the broad audit back open.

---

## Method note

Five of the seven checks were originally dispatched to adversarial verification agents, and five of those agents failed with API stream errors (the same failure mode that caused the original gap). Rather than a third dispatch, the remaining checks were executed directly against the code. Every result below is from execution, not inspection.

Evidence scripts are preserved in [`evidence/`](evidence/). Commands are given per check.

**Environment:** Windows 11 26200, CPython 3.13.9, mesa 2.4.0, pytest 8.4.2, `LongPathsEnabled=0`.
`litellm` deliberately absent (it breaks the documented install; see audit §5 and P0.2).

```
cd scaffold/backend
PYTHONPATH=<abs path to scaffold/backend>
.venv/Scripts/python.exe <script>
```

---

## Verdict table

| # | Finding | Original | Verdict | Final | Blocker |
|---|---|---|---|---|---|
| 1 | `no-budget-or-treasury-enforcement` | major | **confirmed** | major | no |
| 2 | `block-unfunded-spending-blocks-nothing` | major | **modified** | major | no |
| 3 | `scenario-legal-constraints-never-read` | critical | **modified** | major | **yes** (documentary) |
| 4 | `procurement-constraint-actively-contradicted` | critical | **confirmed** | major | **yes** (documentary) |
| 5 | `player-intervention-path-is-a-no-op` | major | **confirmed** | major | **yes** (documentary) |
| 6 | **CRITICAL 4.1** tiers structurally decoupled | critical | **modified** | **critical** | no (behavioural) |
| 7 | **CRITICAL 4.2** macro saturation | critical | **confirmed, escalated** | **critical** | no (behavioural) |

Refuted: **0**. Critical count: **2, unchanged**.

---

## 1. No budget or treasury enforcement — CONFIRMED

Every action in the engine touches only three keys, none of them fiscal:

```
ACTION_EFFECTS keys touched by ANY action:
   ['government_approval', 'military_readiness', 'social_stability_index']
   any fiscal/economic key present? False
```

Nested fiscal state cannot be reached by the engine's only delta path. `apply_deltas`
(`macro_state.py:23-47`) skips any value that is not a top-level scalar:

```
public_finances before: {'treasury_reserve_usd_m': 210.0, 'deficit_pct_gdp': 0.038, ...}
public_finances after  : {'treasury_reserve_usd_m': 210.0, 'deficit_pct_gdp': 0.038, ...}
-> nested fiscal state reachable by apply_deltas? False
```

**New sub-finding.** `apply_deltas` silently ignores unrecognised keys (`macro_state.py:37-38`,
`if not hasattr(ind, key): continue`). A misspelled or nested indicator name produces no error,
no warning and no effect. A future rule pack could author an effect that never applies, and
nothing would report it. Recommend a strict mode that raises on unknown keys.

## 2. `block_unfunded_spending` blocks nothing — MODIFIED

Substantive claim holds. `engine.py:37` gives the action `{"government_approval": -0.003}` and
nothing else. There is no arbitration stage: `_validate_and_price` has no access to sibling
proposals, and the tick loop applies each delta as it is priced.

Control run (from the surviving verifier): deleting the finance minister from the scenario
entirely leaves `military_readiness` at t5 **bit-identical** at `0.44000000000000006`.

Not a publication blocker: no document claims an interaction model exists, and
`scaffold/README.md:5-6` says "a runnable skeleton, not a finished product". Permitted incompleteness.

## 3. Scenario legal constraints never read — MODIFIED (critical → major)

Constraints are behaviourally inert, proven by substitution rather than grep:

```
40-tick hash WITH constraints   : 1af9170525db
40-tick hash WITHOUT constraints: 1af9170525db
-> constraints causally inert? True
```

Downgraded from critical because reproducibility, the determinism boundary and traceability are
all intact. A missing constraint check means the LLM does *less*, not more. What remains
impermissible is documentary, and that is why it is still a publication blocker.

Structural note: `_validate_and_price(self, proposal)` (`engine.py:121-130`) never receives the
agent spec, so constraints are unreachable from the gate, not merely unconsulted.

## 4. Procurement constraint actively contradicted — CONFIRMED

The scenario constrains the defence minister with `procurement_law_18mo_minimum`. The stub makes
that minister propose `request_procurement_acceleration` every tick, and the engine applies
`{"military_readiness": 0.01, ...}` immediately, with no delay, cost or check.

```
readiness: t1 0.40 | t10 0.49 | t30 0.69 | t60 0.99 | t61 1.00 | t120 1.00
first tick at clamp ceiling: 61
```

`Intervention.timeline_days` ("Days until the action takes effect") is never read.

## 5. Player intervention path is a no-op — CONFIRMED

Driven through the real API with `TestClient`:

```
POST /runs/{id}/decision
  actor_role  : "janitor_with_no_authority"
  action_type : "nationalise_every_foreign_asset_and_declare_war"
  legal_check : "LEGAL_AND_APPROVED"     <-- supplied by the client
  resource_cost: {"treasury_reserve_usd_m": 999999999}

-> 200 {"accepted": true}
-> macro state changed by the decision? False
-> player_decision events after 5 further ticks: 1, with effects: []
-> client-supplied legal_check echoed back and trusted: 'LEGAL_AND_APPROVED'
```

The endpoint accepts any actor, any action, any cost, and lets the client assert its own
legality verdict. It is a logging endpoint. The module docstring
(`routes_simulation.py:4-5`) says "the engine validates and prices them", which is false;
the function docstring says validation "happens on tick", and it does not.

## 6. CRITICAL 4.1 — tiers structurally decoupled — MODIFIED (important)

The audit's claim that no tier reads another tier's state is **half right, and the other half
was measuring the wrong thing.**

Perturbation tests at seed 88213, 40 ticks:

| Perturbation | Result |
|---|---|
| Macro hammered (shipping .61→.05, approval .44→.01, unemployment →.95) | cohort beliefs **unchanged**, narrative adoption **unchanged** |
| Cohort beliefs → 0.01, threat perception → 0.99, *grievance lists untouched* | macro **unchanged** |
| Added a grievance to the one cohort that had none | macro **changed** |
| Deleted a cohort entirely | macro **changed** |

The last two look like meso→macro coupling. They are not. `cohort_agent.step()` draws from the
RNG **only if the cohort has grievances**. Changing how many cohorts have grievances changes how
many draws are consumed per tick, which shifts every later draw in the shared stream, which
changes the macro noise value:

```
shipping_throughput_pct_of_baseline: 0.6080711379477878 -> 0.5973599412373322
```

Changing cohort *values* by two orders of magnitude changes macro by exactly nothing.

**Corrected statement.** Macro→meso is dead. Meso→macro is also dead; the apparent influence is
an artefact of a single shared RNG stream, not a causal channel. **The finding stands at critical.**

**New defect exposed (not previously in the audit).** There are no named RNG substreams. Adding
or removing a single random draw in one subsystem silently changes every subsequent draw in every
other subsystem. This is a latent reproducibility hazard: any future change to cohort logic will
perturb macro results for reasons that have nothing to do with the model. It also means the
existing determinism test would mask such a change as "expected divergence". This is the defect
the original external reviewer predicted on inspection; it is now demonstrated.

## 7. CRITICAL 4.2 — macro saturation — CONFIRMED and ESCALATED

The decisive question was whether saturation is an artefact of the stub choosing a fixed action
per role. It is not.

```
STUB (fixed action per role)          military_readiness 1.0000  social_stability 1.0000
VARIED (random legal action / tick)   military_readiness 1.0000  social_stability 1.0000
   indicators pinned at a clamp bound after 120 ticks, BOTH modes:
   ['military_readiness', 'social_stability_index']
```

Varied action selection, which is what a real model produces, does not prevent saturation. The
reason is that the engine has no opposing mechanism at all:

```
'cost'         appears in engine.py: False
'cooldown'     appears in engine.py: False
'decay'        appears in engine.py: False
'budget'       appears in engine.py: False
'resource'     appears in engine.py: False
'prerequisite' appears in engine.py: False
'revert'       appears in engine.py: False
```

**Escalation.** This is an architectural gap, not a calibration problem. No amount of tuning the
existing numbers fixes it, because there is no mechanism to tune. Per P0.7 it must not be patched
with arbitrary mean reversion; tick semantics and horizon come first.

---

## Corrections required in `CURRENT-STATE-AUDIT.md`

Carried from the surviving adjudicator, plus A3's own findings:

1. §4.1 — add the RNG-contamination distinction and the new no-substreams defect. The section
   currently implies meso→macro is simply absent; it is absent *and* spuriously coupled.
2. §4.2 — record that varied action selection was tested and does not prevent saturation, and
   that no cost/cooldown/decay mechanism exists. Escalate from calibration to architecture.
3. §5.4 `:156` — add: "The gate could not read them even if it wanted to: `_validate_and_price`
   (`engine.py:121-130`) is passed only the proposal, never the agent spec."
4. §5.4 `:158` and §5.5 `:168` — re-anchor the `CHARTER.md` citation. `CHARTER.md:114` ("the LLM
   never decides whether the composition is legal") is **true**. The false clause is
   `CHARTER.md:112`, "then priced, validated and resolved by the engine". Add `README.md:38` and
   `scaffold/README.md:19` as genuine front-door untruths not previously cited.
5. §5.7 `:188` — add the control-run evidence that `block_unfunded_spending` is causally inert.
6. §5.6 `:180` — add that there are **no terminal semantics at all**: `run(400)` completes with
   nothing evaluating win or loss.
7. §6.1 — flag `agent_schema.py:182`, which describes constraints as "Hard legal/procedural
   constraints" while they are inert.
8. New §6.x — `apply_deltas` silently ignores unknown keys.

Citation drift found in the incoming finding text, **not** present in the audit, so nothing to
edit: finance objective is `kestral-strait.json:302` not `:305`; `CHARTER.md:20` not `:21`;
`government_approval` is a shared national indicator, not per-actor.

---

## Publication blockers after A3

Unchanged at five. Deduplicated:

| # | Blocker | Clears by |
|---|---|---|
| B1 | Documents claim the engine validates legality and feasibility. It does not. | Text correction. Implementing the evaluator is **not** required. |
| B2 | Determinism boundary claimed as guarded in CI. There is no CI and no `.git`. | Text correction, or build the guard |
| B3 | Three tables claimed persisted. Nothing is written to the database. | Text correction |
| B4 | "Adding an archetype requires only a new JSON" is false and fails silently. | Text correction |
| B5 | Dual-use influence-targeting schema with no acceptable-use terms. | Owner decision (P0.8) |

Four of five clear by telling the truth. Only B5 needs a decision.

---

## Recommendation

**Close the broad audit.** Nothing refuted, no new blocker, critical count unchanged at 2, and the
two corrections both moved toward the audit's existing position rather than away from it. The
remaining work is editorial amendment plus Phase 0.

Do not launch another unrestricted multi-agent audit.
