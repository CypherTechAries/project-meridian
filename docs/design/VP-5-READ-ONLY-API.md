# VP-5 — the read-only Virtual Person API

VP-5 exposes everything VP-1 to VP-4 implemented through two read-only endpoints. It **composes; it
never recomputes** — no belief is re-derived, no option is re-scored, no history is re-sorted.

Code: `app/simulation/person/projection.py`, `app/api/routes_virtual_person.py` ·
Tests: `tests/test_virtual_person_vp5_api.py`

## Claim boundary

> The Virtual Person API exposes deterministic fictional fixture information, current-situation
> state, option comparisons, selected-but-unexecuted decisions, declared relationships and bounded
> history records. It does not expose a complete psychological model or live authoritative person
> state.

## Endpoints

| Method | Path |
|---|---|
| `GET` | `/api/virtual-person/kestral-strait/roster` |
| `GET` | `/api/virtual-person/kestral-strait/dossier/{typed_person_id}` |

No POST, PUT, PATCH or DELETE. No request body. No action-selection or command endpoint.

```
GET /api/virtual-person/kestral-strait/roster
GET /api/virtual-person/kestral-strait/dossier/fict:kestral-strait:person:broadcast-journalist
```

## What the roster returns

The implemented people with a short current-situation summary, record counts, decision status and
selected action label. **In declaration order, never ranked** — not by influence, susceptibility,
movement, risk, importance, ability to persuade or likelihood of compliance. There is no overall
person score anywhere.

```jsonc
{
  "people": [{
    "person_ref": "fict:kestral-strait:person:broadcast-journalist",
    "display_name": "Correspondent, Northshore Broadcast",
    "portrait_ref": null,
    "current_situation_summary": "The person is trying to publish an accurate report, while an
       approaching publication deadline keeps pressure moderate, and insufficient corroboration…",
    "goal_count": 1, "active_pressure_count": 1, "active_constraint_count": 1,
    "latest_decision_status": "SELECTED_NOT_EXECUTED",
    "selected_action_label": "seek additional corroboration",
    "execution_status": "NOT_EXECUTED",
    "belief_observation_count": 1, "trajectory_available": false
  }],
  "ordering": "declaration order; never ranked"
}
```

## What the dossier returns

Eight distinct sections: **identity** (fixture, display only — missing fields stay `null`, never
invented prose) · **current situation** (goals, responsibilities, pressures, constraints, each with
value, plain-language band, origin, references) · **decision** · **relationships** · **information
history** · **belief history** · **explanations** · **model boundary**.

**`option_labels`** maps every considered action id to its declared fixture label, so that a raw
internal id such as `a-publish-now` never reaches a reader where an option name belongs. It is an
additive projection field: the projection already held these labels, nothing is rescored, no decision
is recomputed, and no engine state changes. It does **not** belong in the engine schema. The id-keyed
fields remain unchanged and authoritative — evidence and traces still address options by id.

```jsonc
{
  "decision": {
    "selected_action_label": "seek additional corroboration",
    "execution_status": "NOT_EXECUTED",
    "default_statement": "Selected by the declared rule. Not executed.",
    "unavailable_options": ["a-publish-now"],
    "blocking_constraints": {"a-publish-now": ["c-corroboration"]},
    "option_labels": {"a-publish-now": "publish the claim immediately", /* … */ },
    "decision_trace": { /* exact component totals live ONLY here */ }
  },
  "belief_history": {
    "observation_count": 1, "trajectory_available": false,
    "trajectory_explanation": "MERIDIAN has one recorded belief update for this proposition. It
       does not yet have enough history to describe a longer-term pattern."
  }
}
```

## What the API cannot change

Nothing. Every projection function is pure over frozen fixtures. A deep-copy test snapshots the VP-2
fixtures, VP-4 relationships and the belief cast's people, priors and exposures, exercises every
route, and asserts byte-equality afterwards. All response models are immutable (`extra="forbid"`,
`frozen=True`).

## Why it is a packaged snapshot, not live run state

The Virtual Person material is composed on request from frozen fixtures and deterministic rules. No
simulation run is read, advanced or written. Every response carries
`result_kind: "packaged-virtual-person-snapshot"` and `connected_to_authoritative_run: false`, plus
the existing scenario-id disclosure. The phrases *live person state*, *current authoritative person*,
*persisted person memory*, *executed decision history* and *real-time society state* appear **only
inside an explicit denial** — a test enforces that.

## Why selection is not execution

The decision section is copied from VP-3 exactly: same selected action, same unavailable options,
same component totals, same tie status. `execution_status` is always `NOT_EXECUTED`, and the default
display line is *"Selected by the declared rule. Not executed."* No world-state, belief, pressure or
relationship consequence is applied or exposed.

## Why history is not memory

The histories are engine audit records. The API implies no recall, forgetting or retrieval, and
carries no field suggesting the person remembers anything.

## Why relationships do not imply influence

A relationship is a declared connection with no strength, trust, influence, loyalty or closeness
score. A `receives_from` edge is rendered with an explicit caveat: *"This does not mean every report
from that source is believed, or that any particular message was received."* Receipt appears only as
an explicit information record.

## Why one observation is not a trend

`observation_count: 1` and `trajectory_available: false`. Trend words appear only inside the denial
sentence — a test asserts they are never used as an assertion about the person.

## Origins and missing information

`FIXTURE` / `ENGINE` / `UNKNOWN` / `UNAVAILABLE` / `NOT_MODELLED` are preserved from the owning
milestone — identity is FIXTURE, situation starting values FIXTURE, transitions ENGINE, decisions
ENGINE, relationships FIXTURE, and belief keeps its separate `value_origin` and `decision_origin`.
Nothing is relabelled ENGINE merely because the API assembled it. Absence is never `0`, `false` or
an empty string pretending to be a value.

Belief classification comes from the **one canonical classifier** — a parity test asserts the belief
read-model, VP-4 history and the VP-5 dossier all classify the same frozen observation identically.

## Default text versus technical detail

Default fields use ordinary language and contain none of: alignment, propensity, aggregation,
credence, provenance, state mass, utility, susceptibility. Exact values live in nested
`decision_trace` and are never rounded, never presented as probabilities.

## Two defects found during this milestone

1. **Four copies of the uncertain band.** Fixed before PR #21 merged — one canonical classifier now
   serves every surface (see the VP-4 PR).
2. **A vacuous test on `main`.** The belief API's no-targeting test iterated `app.routes`, which in
   this FastAPI version wraps included routers in `_IncludedRouter` objects with no `.path`. The list
   was always empty, so the assertions passed while proving nothing. Both that test and the VP-5
   equivalent now enumerate the **OpenAPI schema** — the real public surface — and assert the routes
   are actually discoverable first.

## What VP-6 will add

Ask MERIDIAN Phase 1: deterministic structured answers built on this API, with **no LLM**.
