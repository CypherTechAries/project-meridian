# Belief read-model API — contract

Two read-only routes exposing the already-implemented belief slice. **No new belief rules, no new
person behaviour, no cohort distributions, no memory, no path dependence, no personalised feeds, no
evaluative updating, no LLM call, no persistence and no UI code were added.**

## The run-integration boundary — read this first

**These results are not connected to the authoritative simulation run.**

Two facts establish it, and both are verifiable rather than asserted:

1. Before this milestone, nothing outside the belief package and its own tests imported it. There
   was no wiring, and this API does not create any — it reads fixtures and applies a pure function.
2. `cast.py` declares `scenario_id = "kestral-strait"`, the **same id** as the packaged scenario
   file, but a **disjoint entity set**. The scenario file declares five cohorts
   (`coastal-creole-fishing`, `inland-highland-minority`, `military-veteran-families`,
   `urban-nationalist-youth`, `urban-professional-vantaran`). The belief cast declares six entirely
   different ones (`port-workers`, `coastal-households`, `governing-party-supporters`,
   `opposition-supporters`, `inland-households`, `small-business-owners`) plus three people and
   three organisations the file does not contain.

Every landscape response therefore carries:

```json
"run_integration": {
  "connected_to_authoritative_run": false,
  "result_kind": "packaged-belief-snapshot",
  "label": "Deterministic belief-divergence slice — engine-computed demonstration result",
  "explanation": "These results are computed on request from frozen packaged fixtures. They are
    not live run state, not current authoritative belief state, and not persisted person state.
    No simulation run is read, advanced or written. The same request always returns the same
    answer because the mechanism is deterministic, not because anything was stored."
}
```

**These results must never be described as** live run state · current authoritative belief state ·
persisted person state. A test asserts each of those three phrases appears only inside an explicit
denial, and nowhere else in the response.

The shared-scenario-id collision is returned as `scenario_id_note` rather than quietly reconciled.
Until it is resolved, belief entity ids resolve against the belief cast registry only — resolving
them against the packaged scenario file would refuse all twelve.

## Endpoints

| Method | Path | Returns |
|---|---|---|
| `GET` | `/api/belief/kestral-strait/landscape` | All twelve entities' response to one claim |
| `GET` | `/api/belief/kestral-strait/dossier/{typed_id}` | One entity, in one of three distinct shapes |

Prefix `/api/belief`, tag `belief` — matching the existing `/api/simulation` and `/api/demo`
convention rather than inventing a parallel structure.

**Why `GET` and not `POST`.** `/api/demo/kestral-strait/run` is a `POST` because it executes
simulation work — it builds a model and steps ticks. These routes build nothing and step nothing.
They read frozen fixtures and apply a pure function, so a `GET` is the honest verb.

`{typed_id}` must be a typed fictional reference:
`fict:kestral-strait:person:broadcast-journalist`. Free text is refused.

## What the routes return

**Landscape** answers: who received the claim, who did not, who moved, who remained unsure, which
organisations support / oppose / withhold, and what is unavailable. Entities are returned in
**declaration order, never sorted by movement** — a sorted list is a ranking whatever it is called.

**Dossier** answers: who or what the entity is, which claim is selected, what it believed or
expressed before, what changed, why, what information it received, where the result came from, and
what MERIDIAN does not model.

## What the routes do not return

- No internal engine model. `UpdateResult`, `CohortReport` and `OrganisationResult` never cross the
  boundary; `signal_weight`, `trace`, `explanation` and `public_sentence` are absent from responses.
- No cohort internal breakdown, and no shares of any kind.
- No cohort confidence.
- No evaluative belief change — evaluative updating is not implemented.
- No intelligence, competence, susceptibility, persuadability or influence rank on any shape.
- No emotion, personal confidence, human memory or single human-like belief on an organisation.
- No ranking, targeting, audience optimisation or persuasion operation on any route.

## The three shapes are deliberately distinct

Flattening people, organisations and cohorts into one generic profile would require blank fields
that imply a missing value rather than an absent concept. So:

| | Person | Organisation | Cohort |
|---|---|---|---|
| `confidence_statement` | ✓ | — | — |
| `confidence_status` | — | `NOT_MODELLED` | `NOT_MODELLED` |
| `internal_views` / `official_position` | — | ✓ | — |
| `action_direction` / `action_strength_statement` | — | ✓ | — |
| `reasons` (≤3) | ✓ | — | — |
| `breakdown_status` | — | — | `UNAVAILABLE` |
| `population_represented` | — | — | ✓ |

A test asserts no two shapes share a field set.

## Origin semantics

Four values, preserved from the engine: `ENGINE` · `FIXTURE` · `UNKNOWN` · `UNAVAILABLE`.

`value_origin` and `decision_origin` are separate fields, because **the engine deciding not to
change a value is not the engine producing that value.** Inland households return:

```json
"origin": {
  "value_origin": "FIXTURE",
  "decision_origin": "ENGINE",
  "note": "The earlier view came from the packaged story; the engine decided not to change it
    because the group never received the claim."
}
```

Both facts stay visible. Neither can be read off the other.

## Missing-data semantics

Three distinct statuses, never collapsed and never numeric:

| Status | Meaning | Example |
|---|---|---|
| `UNAVAILABLE` | The concept applies; the value cannot be known from what is declared | cohort internal breakdown |
| `NOT_MODELLED` | The concept is not modelled in this slice at all | cohort confidence, organisation confidence |
| `UNKNOWN` | Declared but not recorded | reserved; unused by the current cast |

`UNKNOWN`, `UNAVAILABLE` and `NOT_MODELLED` never become `0`. Asserted by a walker that fails on any
zero-valued number sharing a record with an absence status.

## Modelled and unmodelled layers

Every dossier returns **both** lists in `layers`. They are part of the payload, not the
documentation, so a frontend cannot quietly omit the limitation without making a deliberate choice
to drop a field it was handed.

`not_modelled` is fifteen entries for every kind — personal history, memory, relationships, changing
trust, emotional state, cumulative stress, personalised feeds, information order, path dependence,
social interaction, stochastic choice, persistent life history, intelligence, competence, life
trajectory — plus per-kind additions (organisations add internal politics and past decisions;
cohorts add internal belief breakdown, confidence and individual members).

## Plain-language derivation

Display text is derived from structured state through versioned band tables
(`WORDING_VERSION = "belief-wording-v1"`). **No sentence is authored for a named entity.** A test
scans the wording tables' source and fails if any of the twelve entity ids appears in them.

| Band | Rule |
|---|---|
| View | `< 0.35` "Doubted it" · `0.35–0.65` "Unsure" · `> 0.65` "Leaned towards it" |
| Movement | `0` "did not move at all" · `< 0.02` "barely moved" · `< 0.10` "took a small step" · else "moved clearly" |
| Confidence | `≥ 0.7` settled · `≥ 0.5` moderately settled · else "still short of sure" |
| Cohesion | `≥ 0.8` strongly united · `≥ 0.6` united enough to speak firmly · else moderately divided |
| Position / direction | direct enum mapping |
| Action strength | withheld → "None. A withheld position carries no force." · `≥ 0.15` firmly · else not forcefully |

Cohorts use the **real exposure path** ("Received it — union relay", "No route carried this claim to
them"), never an invented psychological reason.

**No default display field may contain** credence · provenance · contextual threshold · update
weight · alignment · aggregation · state mass · denominator · propensity · epistemic. Exact values
are reachable only through the nested `calculation` object.

### One approved-design discrepancy, reported rather than tuned

The approved mockup shows the minister as **"Barely moved"**. The band table returns **"took a small
step"**, because the minister's movement is `+0.0219` and the "barely" band ends at `0.02`.

I have not moved the band to match the mockup. Choosing a threshold so a specific named entity
produces a specific desired word is the same error as tuning fixtures until three labels appear —
the bands are set at 2% and 10% of the credence scale because those are principled round numbers,
not because of what they make the minister say. **Founder decision:** accept "took a small step",
or move the boundary on a stated principle that is not "it reads better for the minister".

## B5 on every route

| Control | How |
|---|---|
| Typed fictional ids | `fict:<scenario>:<kind>:<entity>`; anything else is `422` |
| Registry resolution | Ids must name an entity the belief cast declares; unknown is `404` |
| Cross-world refusal | A different scenario id is `422` with "cross-world reference" |
| Free-text refusal | "BBC News", "Reuters", bare ids — all `422` |
| Unknown fields | Unknown **query parameters** are `422`, never ignored |
| Legacy `agent` kind | Refused on belief routes |
| No persuasion operation | `assert_no_protected_traits`, `assert_no_persuasion_optimisation`, `assert_not_real_population` run on every id |
| Read-only | `POST`/`PUT`/`DELETE` return `405`; there is no request body anywhere in the module |

Unknown query parameters are refused rather than ignored because a control that silently drops what
it does not recognise is exactly the failure B5-06 exists to prevent — and that has already happened
once in this project.

## Mutation safety

Every projection function is pure over frozen module-level fixtures. No module-level mutable state
exists in the router, nothing is cached between requests, and no request can alter what another
request sees.

Evidence: `test_20` deep-copies all eleven fixture structures, exercises every route, and asserts
byte-equality afterwards. `test_21` asserts projections are immutable. `test_19` asserts repeated
requests return identical bodies.

## Tests

**35 tests** in `tests/test_belief_read_model_api.py`. Backend total **419** (was 384), frontend
**64** unchanged.
