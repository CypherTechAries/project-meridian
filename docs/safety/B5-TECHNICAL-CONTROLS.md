# B5 — technical control baseline

> # FOUNDER-APPROVED CONTROL BASELINE — IMPLEMENTED AND TESTED
>
> This is the **canonical** B5 control set for public v0.1, approved by the founder on
> 19 July 2026. It supersedes every scattered reference to "the eight controls". No agent may
> substitute, reorder, extend, narrow or reconstruct a different list from other documents.
>
> **Technical enforcement is primary.** Licence wording, acceptable-use language, documentation and
> disclosures are **supplementary** and cannot clear B5 without code and tests. B5 is not complete
> because this document exists.

**Blocker:** B5 — *dual-use influence-targeting schema with no acceptable-use terms.*
**Decided:** 18 July 2026 (policy). **Baseline approved:** 19 July 2026 (this document).
**Clears when:** all eight controls have code paths, have tests, and hosted CI is green.
**Status 19 July 2026:** all eight implemented and tested locally (backend 187, frontend 52).
Awaiting hosted CI and founder review on `feat/b5-publication-controls`; **not yet merged**.
**Related:** [`../delivery/PUBLICATION-EXIT-CRITERIA.md`](../delivery/PUBLICATION-EXIT-CRITERIA.md) ·
[`../delivery/CAPABILITY-CLAIMS.md`](../delivery/CAPABILITY-CLAIMS.md) ·
[`../../PROJECT-ROADMAP.md`](../../PROJECT-ROADMAP.md)

---

## B5-01 — Fail-closed fictional manifest

Every runnable scenario must declare:

```json
"world_mode": "fictional"
```

Missing, unknown, malformed or non-fictional values are **rejected before scenario loading or
simulation execution**.

**No default-to-fictional behaviour is permitted.** A scenario that omits the field is invalid, not
assumed safe. Rejection happens before any engine object is constructed.

---

## B5-02 — Packaged fictional scenarios only

Public v0.1 may run **only repository-bundled, explicitly allowlisted** fictional scenario packages.

Disabled: arbitrary scenario uploads · URL-based scenario loading · external scenario datasets ·
real-world scenario import · conversion of news, documents or public datasets into runnable
scenarios.

A strict allowlist enforces this — **not heuristic real-world detection**, which can be talked
around. It also closes path traversal: a non-member is rejected before any filesystem access.

---

## B5-03 — Fictional target registry

Every influence, narrative, intervention or command target must use a **typed identifier that
resolves inside the active fictional-world registry**.

Rejected: free-text person targets · free-text organisation targets · free-text
political-population targets · unresolved external identifiers · targets from another world or
scenario · real persons, organisations, governments or political populations.

Validation **fails closed**: an unresolvable identifier is an error, never a silently ignored or
best-effort match.

**Typed identifier form.** `fict:<scenario_id>:<kind>:<entity_id>`. The `fict:` prefix and the
scenario segment make a cross-world or real-world reference structurally impossible to express, not
merely disallowed.

**Target-kind taxonomy — closed set, each kind means one thing.**

| Kind | Meaning | Resolves from |
|---|---|---|
| `person` | A persistent fictional individual with beliefs, attitudes, bounded emotions, stance and behaviour propensities | `scenario.people[].person_id` |
| `organisation` | A fictional formal collective actor with membership, official position, internal position distribution, objectives, cohesion and posture. **No emotion vector** | `scenario.organisations[].organisation_id` |
| `cohort` | An aggregate fictional population group for population-weighted modelling. Not a person, not a list of persons | `scenario.cohorts[].cohort_id` |
| `agent` | **Legacy and narrow.** An institutional office-holder declared by the P0.5 scenario. Retained only because the shipped causal slice references those six records. **Not a generic target type**; new work uses `person` or `organisation` | `scenario.institutional_agents[].agent_id` |

`organisation` and `agent` are **not synonyms**: an agent is an individual office-holder, an
organisation is a collective body.

**Vocabulary change, 20 July 2026** (commit `0c4f696`, hardened in the following commit), for the
Belief Formation and Divergence Slice:

- **Added `person` and `organisation`.** That milestone models named fictional people and
  organisations, which the previous vocabulary could not express at all.
- **Removed `institution`.** No scenario ever declared an `institutions` collection, so the kind
  resolved to nothing and could never appear in a valid target. A kind that cannot resolve is
  surface area with no purpose.

Net effect: **two added, one removed.** It does not weaken fictional-only resolution — a target must
still carry the `fict:` prefix, name the **active** world, and **resolve** in that world's registry,
which is built solely from scenario data. No real person or organisation becomes addressable,
whatever its kind.

**Evidence.** `tests/test_b5_target_kinds.py` — 55 cases covering both new kinds directly:
registered accept · unregistered reject · cross-world reject · identifying extra fields
(`name`, `real_name`, `social_handle`, `external_id`) rejected by schema · free text reject ·
unknown kind reject, including the removed `institution` · malformed identifier reject · case,
whitespace, homoglyph and zero-width bypass reject · cross-kind collision isolation · audience
ranking proven **absent**, not merely refused. The pre-existing suite was not treated as evidence
for vocabulary it never exercised.

---

## B5-04 — Protected-trait exclusion

Protected or sensitive traits, and **project-declared proxies** for those traits, must not be
accepted as: targeting criteria · ranking criteria · optimisation variables ·
intervention-selection variables · susceptibility weights · audience-segmentation controls.

**Identity may still affect** lived experience, relationships, discrimination, institutional access,
media exposure and cultural interpretation. That is modelling, and it stays permitted.

**Identity must never encode inherent** competence · morality · loyalty · violence · truthfulness ·
manipulability.

The distinction is the point: identity may shape *what happens to* an entity and *what it sees*;
never what it *is worth* or *how easily it can be moved*.

---

## B5-05 — No persuadability optimisation

MERIDIAN must not calculate, expose or recommend: susceptibility scores · persuadability rankings ·
"most influenceable" people or cohorts · optimal audiences for persuasion · optimal message
targeting · exploitation of vulnerability · automated audience selection intended to maximise belief
change.

This prohibition applies to **fictional and real audiences alike** for public v0.1.

**Aggregate fictional belief propagation remains permitted** (see safe harbor). The prohibition is
on ranking or selecting audiences *in order to* move them, not on modelling that belief spreads.

---

## B5-06 — No real-population manipulation recommendations

APIs, command interpretation, model prompts, model outputs and UI features must not produce
recommendations or operational instructions for persuading or manipulating real people or
populations.

Requests naming real-world population targets are **rejected, not silently transformed into a
fictional analogue**. Automatic rewriting would teach the caller that the request was acceptable and
would obscure the refusal.

No live model exists yet, so this is enforced at the schema and gateway boundary — which must
preserve the restriction when a model is wired. The belief-slice schemas make real-person,
real-organisation and real-population targeting structurally inexpressible rather than filtered.

---

## B5-07 — Persistent fictional-world disclosure

Every runnable UI surface must visibly identify the product as a fictional simulation, using the
approved wording exactly:

```text
FICTIONAL SIMULATION — NOT REAL-WORLD INTELLIGENCE OR PREDICTION
```

API responses must also carry structured fictional-world metadata.

The disclosure must survive: normal navigation · dossier and modal views where applicable ·
screenshots · ordinary cropping · mixed engine/fixture screens.

Crop survival is a real requirement: a single-panel screenshot is the unit in which this interface
is actually shared, so per-panel marking is mandatory and a global banner alone is insufficient.

---

## B5-08 — Per-element provenance and origin

Every user-visible claim, metric, assessment or record must support: origin · epistemic status ·
scenario identity · scenario version · last-updated tick or time where applicable · fixture/live
distinction.

**Approved origin vocabulary — closed set:** `ENGINE` (computed this run) · `FIXTURE`
(hand-authored, not modelled) · `UNKNOWN` (origin not established) · `UNAVAILABLE` (could not be
obtained).

**Fixture information must never be presented as computed engine output.**

**`UNKNOWN` and `UNAVAILABLE` must never silently render as zero.** Zero is a number the engine
computed; absence is not. Collapsing them is the specific dishonesty this control exists to prevent.

---

## Safe-harbor statement

Recorded so enforcement does not over-reach into the modelling the project exists to do:

> Fictional aggregate narrative propagation, adoption, belief divergence, defensive
> counter-messaging, and comparison of pre-authored defensive interventions **are permitted** when
> the eight controls above are enforced.

They must not become: audience-targeting optimisation · susceptibility ranking · real-world
influence recommendations · protected-trait exploitation.

This is the boundary the
[`../design/BELIEF-SENTIMENT-VERTICAL-SLICE.md`](../design/BELIEF-SENTIMENT-VERTICAL-SLICE.md)
milestone must be built inside. B5 enforcement is a **precondition** for that milestone, and is not
permission to add the capabilities its §5 defers.

---

## Enforcement principle

**Technical enforcement is primary.** Licence wording, acceptable-use language, documentation and
disclosures are supplementary and cannot clear B5 without code and tests.

Implementation preferences, in order: strict typed schemas → allowlists → registry resolution.
**Name-detection heuristics are not an acceptable substitute** for any of the three. MERIDIAN does
not build a general content-moderation system; it constrains what can be *expressed* to the engine.

---

## Control-to-implementation map

Populated by the enforcement branch. A control is not enforced until it has both a code path and a
test, and CI is green.

| Control | Implementation | Tests | Status |
|---|---|---|---|
| B5-01 | `app/safety/scenarios.py::assert_fictional_manifest` | 1, 2, 3 | **enforced** |
| B5-02 | `app/safety/scenarios.py::assert_packaged_scenario`, `load_packaged_scenario` (sole load path; `api/runs.py` and `api/routes_demo.py` both route through it) | 1, 4, 5 | **enforced** |
| B5-03 | `app/safety/targets.py::FictionalTargetRegistry.resolve` | 6, 7, 8 | **enforced** |
| B5-04 | `app/safety/targets.py::assert_no_protected_traits` | 9, 9b | **enforced** |
| B5-05 | `app/safety/targets.py::assert_no_persuasion_optimisation` | 10, 12 | **enforced** |
| B5-06 | `app/safety/targets.py::assert_not_real_population`; `DemoRunRequest.model_config = extra="forbid"` | 11, 11b | **enforced** |
| B5-07 | `app/safety/scenarios.py::fictional_world_metadata`; `controls.FICTION_DISCLOSURE`; frontend per-panel marks | 13, 17 + frontend `honesty.test.ts` "crop safety" | **enforced** |
| B5-08 | `app/safety/provenance.py` (`assert_origin`, `ProvenancedValue`, `assert_projection_provenance`) | 14, 15, 16 | **enforced** |

**Evidence, 19 July 2026:** backend `187 passed` (70 B5 + 117 pre-existing), frontend `52 passed`.


---


## Stop condition

B5 may be marked **technically enforced** only when all eight controls have code paths, all eight
have tests, hosted CI is green, and the map above cites implementation and evidence for each.

**Do not mark B5 complete merely because this document exists.**
