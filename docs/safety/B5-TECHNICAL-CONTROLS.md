# B5 — technical control baseline

> # FOUNDER-APPROVED CONTROL BASELINE — IMPLEMENTATION REQUIRED
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

A strict allowlist enforces this. **Heuristic real-world detection is not used**, because an
allowlist enforces the boundary more reliably than name inspection. The allowlist also closes path
traversal: an identifier that is not a member is rejected before any filesystem access.

---

## B5-03 — Fictional target registry

Every influence, narrative, intervention or command target must use a **typed identifier that
resolves inside the active fictional-world registry**.

Rejected: free-text person targets · free-text organisation targets · free-text
political-population targets · unresolved external identifiers · targets from another world or
scenario · real persons, organisations, governments or political populations.

Validation **fails closed**: an unresolvable identifier is an error, never a silently ignored or
best-effort match.

**Typed identifier form.** `fict:<scenario_id>:<kind>:<entity_id>`, where `kind` is a closed
vocabulary (`cohort`, `agent`, `institution`). The `fict:` prefix and the scenario segment make a
cross-world or real-world reference structurally impossible to express, not merely disallowed.

---

## B5-04 — Protected-trait exclusion

Protected or sensitive traits, and **project-declared proxies** for those traits, must not be
accepted as: targeting criteria · ranking criteria · optimisation variables ·
intervention-selection variables · susceptibility weights · audience-segmentation controls.

**Identity may still affect** lived experience, relationships, discrimination, institutional access,
media exposure and cultural interpretation. That is modelling, and it stays permitted.

**Identity must never encode inherent** competence · morality · loyalty · violence · truthfulness ·
manipulability.

The distinction is the point: identity may shape *what happens to* an entity and *what it sees*; it
may never be a coefficient on what the entity *is worth* or *how easily it can be moved*.

---

## B5-05 — No persuadability optimisation

MERIDIAN must not calculate, expose or recommend: susceptibility scores · persuadability rankings ·
"most influenceable" people or cohorts · optimal audiences for persuasion · optimal message
targeting · exploitation of vulnerability · automated audience selection intended to maximise belief
change.

This prohibition applies to **fictional and real audiences alike** for public v0.1.

**Aggregate fictional belief propagation remains permitted** — see the safe-harbor statement below.
The prohibited thing is ranking or selecting audiences *in order to* move them, not modelling that
belief spreads.

---

## B5-06 — No real-population manipulation recommendations

APIs, command interpretation, model prompts, model outputs and UI features must not produce
recommendations or operational instructions for persuading or manipulating real people or
populations.

Requests naming real-world population targets are **rejected, not silently transformed into a
fictional analogue**. Automatic rewriting would teach the caller that the request was acceptable and
would obscure the refusal.

No live model integration exists today, so this control is currently enforced at the schema and
gateway boundary. Those boundaries must preserve the restriction when a model is eventually wired.

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

Crop survival is a real requirement, not a stylistic one: a screenshot of a single panel is the unit
in which this interface will actually be shared, so per-panel marking is mandatory and a global
banner alone is insufficient.

---

## B5-08 — Per-element provenance and origin

Every user-visible claim, metric, assessment or record must support: origin · epistemic status ·
scenario identity · scenario version · last-updated tick or time where applicable · fixture/live
distinction.

**Approved origin vocabulary — closed set:**

| Value | Meaning |
|---|---|
| `ENGINE` | computed by the deterministic engine this run |
| `FIXTURE` | hand-authored content the engine does not model |
| `UNKNOWN` | origin not established |
| `UNAVAILABLE` | the value could not be obtained |

**Fixture information must never be presented as computed engine output.**

**`UNKNOWN` and `UNAVAILABLE` must never silently render as zero.** Zero is a number the engine
computed; absence is not. Collapsing them is the specific dishonesty this control exists to prevent.

---

## Safe-harbor statement

Recorded explicitly, so that enforcement does not over-reach into the modelling the project exists
to do:

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
| B5-01 | | | pending |
| B5-02 | | | pending |
| B5-03 | | | pending |
| B5-04 | | | pending |
| B5-05 | | | pending |
| B5-06 | | | pending |
| B5-07 | | | pending |
| B5-08 | | | pending |

---

## Required tests

1. A valid packaged fictional scenario loads.
2. A manifest without `world_mode` is rejected.
3. A non-fictional `world_mode` is rejected.
4. A scenario outside the allowlist is rejected.
5. Arbitrary file, URL and real-world import paths are unavailable or rejected.
6. A valid fictional registry target is accepted.
7. Free-text and unresolved targets are rejected.
8. Cross-world target identifiers are rejected.
9. Protected-trait targeting fields are rejected.
10. Persuadability and susceptibility-ranking fields are rejected.
11. Real-population manipulation requests are rejected.
12. Fictional aggregate narrative propagation remains allowed.
13. API responses contain fictional-world metadata.
14. Every visible value contains or inherits origin information.
15. Fixture values cannot be labelled `ENGINE`.
16. `UNKNOWN` and `UNAVAILABLE` do not render as zero.
17. Global and crop-safe fictional disclosures remain visible.
18. Existing P0.4, P0.4A, P0.5, API and frontend tests remain passing.

---

## Stop condition

B5 may be marked **technically enforced** only when all eight controls have code paths, all eight
have tests, hosted CI is green, and the map above cites implementation and evidence for each.

**Do not mark B5 complete merely because this document exists.**
