# B5 — technical control baseline

> # FOUNDER-APPROVED CONTROL BASELINE — IMPLEMENTED AND TESTED
>
> **Canonical** B5 control set for public v0.1, approved 19 July 2026. Supersedes every scattered
> reference to "the eight controls". No agent may substitute, reorder, extend, narrow or
> reconstruct a different list.
>
> **Technical enforcement is primary.** Licence wording, acceptable-use language, documentation and
> disclosures are supplementary and cannot clear B5 without code and tests.

**Blocker:** B5 — *dual-use influence-targeting schema with no acceptable-use terms.*
**Decided:** 18 July 2026 (policy). **Baseline approved:** 19 July 2026 (this document).
**Clears when:** all eight controls have code paths, have tests, and hosted CI is green.
**Status:** all eight implemented, tested and merged; hosted CI green.
**Related:** [`../delivery/PUBLICATION-EXIT-CRITERIA.md`](../delivery/PUBLICATION-EXIT-CRITERIA.md) ·
[`../delivery/CAPABILITY-CLAIMS.md`](../delivery/CAPABILITY-CLAIMS.md) ·
[`../../PROJECT-ROADMAP.md`](../../PROJECT-ROADMAP.md)

---

## B5-01 — Fail-closed fictional manifest

Every runnable scenario must declare `"world_mode": "fictional"`. Missing, unknown, malformed or
non-fictional values are **rejected before scenario loading or simulation execution**.

**No default-to-fictional behaviour.** A scenario omitting the field is invalid, not assumed safe.
Rejection precedes construction of any engine object.

---

## B5-02 — Packaged fictional scenarios only

Public v0.1 may run **only repository-bundled, allowlisted** fictional scenario packages.

Disabled: uploads · URL loading · external datasets · real-world import · conversion of news,
documents or public datasets into runnable scenarios.

A strict allowlist enforces this — **not heuristic real-world detection**, which can be talked
around. It also closes path traversal: a non-member is rejected before any filesystem access.

---

## B5-03 — Fictional target registry

Every influence, narrative, intervention or command target must use a **typed identifier resolving
inside the active fictional-world registry**.

Rejected: free-text person, organisation or political-population targets · unresolved external
identifiers · targets from another world · real persons, organisations, governments or populations.

Validation **fails closed** — an unresolvable identifier is an error, never a best-effort match.

**Typed identifier form.** `fict:<scenario_id>:<kind>:<entity_id>`. The `fict:` prefix and the
scenario segment make a cross-world or real-world reference structurally impossible to express, not
merely disallowed.

**Target-kind taxonomy — closed set, each kind means one thing.**

| Kind | Meaning | Resolves from |
|---|---|---|
| `person` | A fictional individual with **stable identity within the active scenario and run**. Carries beliefs, attitudes, bounded emotions, stance and behaviour propensities. **Persistence across saved sessions or runs is not implemented** | `scenario.people[].person_id` |
| `organisation` | A fictional formal collective actor: membership, official position, internal position distribution, objectives, cohesion, posture. **No emotion vector** | `scenario.organisations[].organisation_id` |
| `cohort` | An aggregate fictional population group for population-weighted modelling. Not a person, not a list of persons | `scenario.cohorts[].cohort_id` |
| `agent` | **Legacy P0.5 scenario-actor type.** Resolves only to the existing `institutional_agents` registry. **Not a generic target kind and not used for belief-slice entities** | `scenario.institutional_agents[].agent_id` |

**What the six legacy `agent` records are.** Verified against scenario data, not assumed: each is
**role-scoped — identified by office, not by person — and none carries a personal name**. Four are
singular offices; `intelligence_lead` and `strategic_comms` denote a lead function that may be a
post or a team. They are **heterogeneous** and deliberately not forced into `person` or
`organisation`; the type stays isolated as legacy.

The belief-divergence slice uses **only** `person`, `organisation` and `cohort`. No new `agent`
entities are created.

**Vocabulary change, 20 July 2026** (`0c4f696`, hardened in `5146379`): **added** `person` and
`organisation` — the belief slice models fictional people and organisations, inexpressible before;
**removed** `institution` — no scenario ever declared an `institutions` collection, so it resolved
to nothing and could never appear in a valid target.

Net: **two added, one removed.** Fictional-only resolution is unweakened — a target must still carry
the `fict:` prefix, name the **active** world, and **resolve** in that world's scenario-built
registry. No real entity becomes addressable, whatever its kind.

**Evidence.** `tests/test_b5_target_kinds.py` — 55 cases covering both new kinds directly:
registered accept · unregistered reject · cross-world reject · identifying extra fields
(`name`, `real_name`, `social_handle`, `external_id`) rejected by schema · free text reject ·
unknown kind reject, including the removed `institution` · malformed identifier reject · case,
whitespace, homoglyph and zero-width bypass reject · cross-kind collision isolation · audience
ranking proven **absent**, not merely refused. The pre-existing suite was not treated as evidence
for vocabulary it never exercised.

---

## B5-04 — Protected-trait exclusion

Protected or sensitive traits, and **declared proxies**, must never be targeting, ranking,
optimisation, intervention-selection, susceptibility or segmentation inputs.

**Identity may still affect** lived experience, relationships, discrimination, institutional access,
media exposure and cultural interpretation. That is modelling, and stays permitted.

**Identity must never encode inherent** competence · morality · loyalty · violence · truthfulness ·
manipulability.

The distinction is the point: identity may shape *what happens to* an entity and *what it sees*;
never what it *is worth* or *how easily it can be moved*.

---

## B5-05 — No persuadability optimisation

MERIDIAN must not calculate, expose or recommend: susceptibility scores · persuadability rankings ·
"most influenceable" people or cohorts · optimal audiences or message targeting · exploitation of
vulnerability · automated audience selection to maximise belief change.

Applies to **fictional and real audiences alike**.

**Aggregate fictional belief propagation remains permitted** (see safe harbor). The prohibition is
on ranking or selecting audiences *in order to* move them, not on modelling that belief spreads.

---

## B5-06 — No real-population manipulation recommendations

APIs, command interpretation, model prompts, outputs and UI must not produce recommendations or
operational instructions for persuading or manipulating real people or populations.

Requests naming real-world populations are **rejected, not silently rewritten into a fictional
analogue** — rewriting would teach the caller the request was acceptable and hide the refusal.

No live model exists yet, so this is enforced at the schema and gateway boundary — which must
preserve the restriction when a model is wired. The belief-slice schemas make real-person,
real-organisation and real-population targeting structurally inexpressible rather than filtered.

---

## B5-07 — Persistent fictional-world disclosure

Every runnable UI surface must visibly identify the product as a fictional simulation using the
exact wording `FICTIONAL SIMULATION — NOT REAL-WORLD INTELLIGENCE OR PREDICTION`. API responses must
carry structured fictional-world metadata.

The disclosure must survive navigation, dossier and modal views, screenshots, ordinary cropping and
mixed engine/fixture screens.

Crop survival is required: a single-panel screenshot is the unit this interface is shared in, so
per-panel marking is mandatory and a global banner alone is insufficient.

---

## B5-08 — Per-element provenance and origin

Every user-visible claim, metric, assessment or record must carry: origin · epistemic status ·
scenario id and version · last-updated tick where applicable · fixture/live distinction.

**Approved origin vocabulary — closed set:** `ENGINE` (computed this run) · `FIXTURE`
(hand-authored, not modelled) · `UNKNOWN` (origin not established) · `UNAVAILABLE` (could not be
obtained).

**Fixture content must never be presented as computed engine output**, and **`UNKNOWN` /
`UNAVAILABLE` must never render as zero** — zero is a computed number, absence is not. Collapsing
them is the specific dishonesty this control prevents.

---

## Safe-harbor statement

So enforcement does not over-reach into the modelling the project exists to do:

> Fictional aggregate narrative propagation, adoption, belief divergence, defensive
> counter-messaging and comparison of pre-authored defensive interventions **are permitted** when
> the eight controls are enforced.

They must not become audience-targeting optimisation, susceptibility ranking, real-world influence
recommendations or protected-trait exploitation.

This bounds the [belief slice](../design/BELIEF-SENTIMENT-VERTICAL-SLICE.md): B5 is a
**precondition** for it, not permission to add the capabilities its §5 defers.

---

## Enforcement principle

**Technical enforcement is primary.** Documentation and disclosures are supplementary and cannot
clear B5 without code and tests.

Preference order: strict typed schemas → allowlists → registry resolution. **Name-detection
heuristics are not an acceptable substitute.** MERIDIAN constrains what can be *expressed* to the
engine rather than moderating content.

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
