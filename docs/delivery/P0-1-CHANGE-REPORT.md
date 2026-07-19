# P0.1 Change Report — Track A truth correction

**Status:** DRAFT. Pending owner review. Drafted by an AI agent; not approved. No decision recorded
here is settled, and nothing in this document authorises further work.
**Date:** 19 July 2026
**Baseline:** commit `71fa329`, the single commit on `main`. No commit, push or repository
visibility change was made. All edits are uncommitted working-tree changes.
**Authority for what may be claimed:** `docs/delivery/CAPABILITY-CLAIMS.md`.

---

## Plain-English layer — what this pass did and did not do

MERIDIAN's defining defect is that its documents claim properties its code does not have. Phase 0
item P0.1 exists to remove that gap from the front-door documents — the files a reader meets first.
The goal is narrow and testable: **no present-tense claim in those documents may be contradicted by
the code.**

This pass covered five files: `CHARTER.md`, the root `README.md`, `scaffold/README.md`,
`scaffold/docs/ARCHITECTURE_DECISIONS.md` and `scaffold/CLAUDE.md`. `HANDOFF.md` was deliberately
untouched — a separate later pass performs its sequence insert and citation migration. Nothing
under `docs/` was touched, and **no `.py` file, test, JSON schema or behaviour was modified.**

Three of the five files had already been corrected in earlier P0.1 work before this pass began:
`CHARTER.md` (amended in place with dated `[P0.1 amendment]` notes), the root `README.md`, and
`scaffold/README.md`. This pass verified those corrections against the code and found them sound;
it then completed the two files that had **not** been swept — `scaffold/CLAUDE.md`, which was
entirely uncorrected, and the three remaining unamended ADRs. It also added one caveat the root
`README.md` was still missing.

**Historical preservation.** No ADR body was rewritten and no charter decision was reversed. ADRs
record why a decision was taken at a point in time; each affected one now carries a dated
**Amendment** block stating what was believed, what is now known from the code, and the date. The
decision text remains authoritative on *what was decided and why*; the amendment is authoritative
on *current fact*. The same principle governs `scaffold/CLAUDE.md`, which is a briefing of rules to
follow rather than a description of software: no rule was weakened. Where a rule stated a property
the code does not hold, the property was labelled — the rule stayed binding.

**What this pass could not do.** Four items require an owner decision and were left alone rather
than resolved. They are listed in § Blocked on an owner decision. The most consequential is that
three live instances of "the full execution-ready plan" remain in the tree: they describe the
*plan document*, not the codebase, and whether the standing constraint at `HANDOFF.md` § Standing constraints (`:135`) reaches
them is open question OQ-2. Changing them would have decided OQ-2 by default.

**Classification vocabulary.** Every claim below is classified as exactly one of: IMPLEMENTED /
PARTIALLY IMPLEMENTED / STUBBED / PLANNED / NOT IMPLEMENTED. The classification describes the
*capability the claim asserted*, not the quality of the wording.

---

## Technical-evidence layer — the claim-by-claim table

Line numbers in the **before** column are as of the state of each file at the start of this pass.
Where a file had already been corrected in earlier P0.1 work, that is stated in the row and the
row is marked *(verified, not changed by this pass)*. Evidence paths are relative to the repository
root. Every claim in the **after** column was checked against source during this pass.

### Group A — `scaffold/CLAUDE.md` (was entirely uncorrected)

| file:line (before) | exact claim before | classification | exact claim after | evidence | clears a publication blocker? |
|---|---|---|---|---|---|
| `scaffold/CLAUDE.md:13-14` | "Only `engine.py`'s tick-processing code writes to `MacroState` and cohort numbers." | PARTIALLY IMPLEMENTED — the ownership model is real; the literal file claim is false | "`engine.py` is the only component that *decides* numeric state; the assignments themselves execute in `app/simulation/agents/macro_state.py:47` (macro) and `app/simulation/agents/cohort_agent.py:38` (cohort beliefs), both reached only from `engine.py:136` and `:164`." | Macro assignment `setattr(ind, key, updated)` at `scaffold/backend/app/simulation/agents/macro_state.py:47`; cohort assignment at `scaffold/backend/app/simulation/agents/cohort_agent.py:38`; the only `apply_deltas` call sites are `engine.py:136` and `:164` (`grep -rn "apply_deltas" scaffold/backend/`) | No — CB-11, audit §6.1 item 8 |
| `scaffold/CLAUDE.md:12-16` (the rule as a whole) | Stated as an architectural property the reader is protected by | STUBBED — the boundary is satisfied trivially, no model is invoked | Added: "**Do not read this rule as a property the code currently guarantees.** … there is no structural guard preventing a model call path from being added — `app/config.py:23-25` already declares an `llm_mode` of 'stub' or 'live'. The rule is binding on you; it is not enforced by the code." | No module under `scaffold/backend/app/` imports a model or HTTP client; `llm_mode`/`llm_model` declared at `config.py:23-25`, read only at `main.py:45` | Contributes to B2 |
| `scaffold/CLAUDE.md:21` | "Same seed + same scenario + same decisions ⇒ **identical** macro/meso numbers." | NOT IMPLEMENTED as stated — submitted decisions never reach the tick loop | Replaced by the founder-settled cleared sentence, verbatim: "The existing stubbed execution path reproduces the same tested numeric outputs when the seed, scenario and stubbed agent outputs remain identical." Plus an explicit prohibition on the "+ same decisions" form, and the founder-settled TARGET sentence carrying its label. | `POST /runs/{id}/decision` appends to an in-memory list at `scaffold/backend/app/api/routes_simulation.py:80-101`; `step()` at `scaffold/backend/app/simulation/engine.py:147-180` never reads it. Determinism test compares the final macro dictionary only, `scaffold/backend/tests/test_engine.py:34-40`. Cleared and target wording quoted from `HANDOFF.md:56-57` and `:61-62` | Contributes to B2 (`HANDOFF.md` § Publication exit criteria (`:98`)) |
| `scaffold/CLAUDE.md:20-24` (RNG rules) | Single seeded RNG described as sufficient for determinism | PARTIALLY IMPLEMENTED — the seed threading is real; isolation does not exist | Added: "**There are no named RNG substreams.** … adding a draw in one subsystem silently shifts every later draw everywhere else … Replacing it is Phase 0 item **P0.4A**, ordered P0.4 → P0.4A → P0.5. **Nothing of P0.4A is implemented.**" | Exactly one `random.Random` at `scaffold/backend/app/simulation/engine.py:83`; exactly three draw sites — `agents/cohort_agent.py:36`, `diffusion.py:75`, `engine.py:135`; contamination result at `docs/delivery/A3-VERIFICATION-RESULTS.md:142-175` | No — records the P0.4A defect |
| `scaffold/CLAUDE.md:25-26` | "logged separately by `model_id + prompt_version + temperature`" | NOT IMPLEMENTED | Made conditional: "It is **intended** to be logged separately by … that is the contract for when a live model is wired, not current behaviour. `PROMPT_VERSION = 'v1'` is declared once … and read by nothing, and neither `model_id` nor temperature is logged anywhere." | `PROMPT_VERSION = "v1"` at `scaffold/backend/app/simulation/llm_gateway.py:38`; `grep -rn "PROMPT_VERSION" scaffold/backend/app scaffold/scenarios scaffold/schemas` returns that one line | No — CB-06, audit §6.1 item 2 |
| `scaffold/CLAUDE.md:27` | "`tests/test_engine.py` enforces this. Do not weaken it." | NOT IMPLEMENTED as an enforcement claim | Replaced with a precise description of both tests, ending: "a gateway that mutated authoritative state by any other route would pass it unchanged. **Do not weaken either test** — the weakness is a reason to strengthen them, not to relax them." | Whole suite is five tests in `scaffold/backend/tests/test_engine.py` (77 lines); boundary test body `:61-77`, its three assertions at `:74`, `:76`, `:77`; determinism test `:34-40` | Contributes to B2 |
| `scaffold/CLAUDE.md` (absent) | No statement about CI anywhere in the file | NOT IMPLEMENTED | Added: "**There is no continuous integration**, so nothing runs these automatically. No CI configuration of any kind exists in the repository." | `ls -a .github` → no such directory; `find . -path ./.git -prune -o \( -name "*.yml" -o -name "*.yaml" \) -print` → `./scaffold/docker-compose.yml` only | Contributes to B2 |
| `scaffold/CLAUDE.md:32` | "# tests (must pass before any PR)" presented with no install caveat | PARTIALLY IMPLEMENTED — recorded as passing only in a non-reconstructible environment | Added a caveat block above the code fence naming both departures from the documented install and P0.2, ending "Expect the first command to fail." | Clean-machine install failure recorded at `HANDOFF.md:45-48`; the two departures at `HANDOFF.md:49-50`; "5 passed" at `HANDOFF.md:43`, `:51` | No — execution-readiness category, `HANDOFF.md:70-71` |
| `scaffold/CLAUDE.md:46-47` | "The `/schemas/*.schema.json` files and `db/models.py` mirror them — keep all three in sync" | PARTIALLY IMPLEMENTED — the instruction is right, the machinery implied does not exist | Added: "**The mirrors are hand-maintained, not generated:** no `model_json_schema()` call and no generation script exists in the tree, and no JSON Schema validation library is present, so the nine files under `/schemas` validate nothing at runtime and can drift undetected." | `grep -rn "model_json_schema\|json_schema" scaffold/backend/app` returns nothing; `grep -rn "jsonschema" scaffold/` returns nothing; nine files in `scaffold/schemas/` | No |
| `scaffold/CLAUDE.md:49` | "(see `design_nation_expansion.md`)" | NOT IMPLEMENTED — dangling citation to a file that has never existed | Repointed: "(see `../docs/PLAN.pdf` §9, the nation-archetype expansion framework — a previous version of this line cited `design_nation_expansion.md`, which does not exist and never has)" | `ls scaffold/design_nation_expansion.md` → no such file; no such path anywhere in the tree; audit exit criterion at `docs/delivery/CURRENT-STATE-AUDIT.md:431` | No — CB-12; partially advances the §9 exit criterion |
| `scaffold/CLAUDE.md:53-55` | "Add a `scenarios/<name>.json` … Do **not** edit the engine." presented as a working extensibility guarantee | NOT IMPLEMENTED as a capability; the rule itself is retained | Rule kept verbatim, followed by: "**That is the rule to follow, not a description of what works.** It is publication blocker B4" plus three bullets — one scenario file only and a second never tested; most scenario content read by no code; the failure is silent — and "If you add a scenario, verify its effect by comparing runs, not by observing that it loaded." | `scaffold/scenarios/` contains one file; twelve-term zero-hit search over `scaffold/backend/app/`; silent skip at `scaffold/backend/app/simulation/agents/macro_state.py:36-41`; empty-delta path at `engine.py:35-43` | **Yes — contributes to B4** |
| `scaffold/CLAUDE.md:59` | `<!-- PLACEHOLDER: fill in with the team's real conventions -->` | NOT IMPLEMENTED — unresolved marker, Phase 0 cannot exit while it stands | **Not resolved.** Marker left in place; an annotation added stating that an AI agent may not settle a policy decision, naming what *is* settled (`HANDOFF.md:21`, `:23`), retaining the three original bullets unchanged as a draft awaiting the owner, and recording that no CI enforces them. | `grep -rn "PLACEHOLDER" --include="*.md" .` outside `docs/delivery/` returns exactly this one line; exit criterion at `docs/delivery/CURRENT-STATE-AUDIT.md:433` | No — **CB-18, blocked on owner decision** |

### Group B — `scaffold/docs/ARCHITECTURE_DECISIONS.md` (three remaining unamended ADRs)

| file:line (before) | exact claim before | classification | exact claim after | evidence | clears a publication blocker? |
|---|---|---|---|---|---|
| `scaffold/docs/ARCHITECTURE_DECISIONS.md:33-34` (ADR-001) | "its models generate the JSON Schema mirrors in `/schemas` and validate every object crossing the API and LLM boundaries." | PARTIALLY IMPLEMENTED — REST validation is real; generation and LLM-boundary validation are not | ADR body unchanged. Dated **Amendment** added: the mirrors "are not generated by anything in the tree … hand-maintained and can drift from the Pydantic models without detection"; and "no JSON Schema validation library is present … so those nine files validate nothing" and "nothing currently crosses an LLM boundary … so the LLM half of the sentence is untested rather than enforced. Read the sentence as the intended contract." | `grep -rn "model_json_schema\|json_schema" scaffold/backend/app` → nothing; `grep -rn "jsonschema" scaffold/` → nothing; no model or HTTP client import under `scaffold/backend/app/` | No — new instance of an already-identified claim class (C14/C10 register rows) |
| `scaffold/docs/ARCHITECTURE_DECISIONS.md:167-174` (ADR-008) | "The engine contains **no** archetype-specific branches. … Adding an eighth archetype must require only a new `scenarios/*.json`." | NOT IMPLEMENTED as a delivered capability — one half untested, one half false | ADR body unchanged. Dated **Amendment** added in four numbered parts: the eighth-archetype promise is **untested** (one scenario file, never a second); the no-branch check covered `engine.py` only; **most archetype content is read by no code at all** (twelve-term zero-hit search enumerated); and **the failure is silent**. Closes with an explicit "**TARGET, not delivered.**" | Load path at `scaffold/backend/app/api/runs.py:21-26`; Pydantic parse at `engine.py:98-101`; `scenario_id` read-and-stored only at `engine.py:52`, `:86`; `represents_population` declared at `agent_schema.py:95` with no read site; silent skip at `agents/macro_state.py:36-41` | **Yes — B4** (this is the ADR-008 site the audit's §9 work item names, `CURRENT-STATE-AUDIT.md:427`) |
| `scaffold/docs/ARCHITECTURE_DECISIONS.md:176-182` (ADR-009) | "Information-campaign effectiveness is computed by a seeded Linear Threshold diffusion … The LLM may compose campaign *content* … the engine decides whether and how far it spreads." | PARTIALLY IMPLEMENTED — diffusion runs but reaches nothing; campaign composition does not exist | ADR body unchanged. Dated **Amendment** added in three numbered parts: the diffusion output "does not reach cohort beliefs" and is assigned to a plain dictionary; "'The LLM may compose campaign *content*' is a target — no such function exists"; and "'Adoption is monotonic non-decreasing' … does not hold". Closes by confirming the decision itself is unchanged and must not be weakened. | `_step_diffusion` assigns to `self.narrative_adoption` at `engine.py:138-145`; only cohort write is `government_competence` at `agents/cohort_agent.py:35-38`; gateway defines exactly three functions — `llm_gateway.py:41`, `:54`, `:85`; `Campaign`/`Narrative`/`Outcome` never instantiated (`grep -rn "Campaign(\|Narrative(\|Outcome(" scaffold/backend/app` returns class definitions only); jitter at `diffusion.py:75-76` | No — CB-09, CB-15 sites |

### Group C — root `README.md`

| file:line (before) | exact claim before | classification | exact claim after | evidence | clears a publication blocker? |
|---|---|---|---|---|---|
| `README.md:60-76` (Quick start) | Install and test commands presented with no caveat in the section itself | PARTIALLY IMPLEMENTED | Caveat block added above the Docker fence: the install path "is recorded as failing on a clean machine", both departures named, "Expect these commands to fail", plus the absence of any machine-readable Python version, `pyproject.toml`, lockfile or `.python-version`, and that all thirteen declared dependencies are open-ended ranges. | `HANDOFF.md:45-50`; `grep -c -E '^[^#[:space:]]' scaffold/backend/requirements.txt` → `13`; no `pyproject.toml`, lockfile, `.python-version` or `setup.cfg` anywhere in the tree | No — execution-readiness category, `HANDOFF.md:70-71` |

### Group D — verified against the code, not changed by this pass

These were corrected in earlier P0.1 work. This pass re-read each against source and found no
present-tense claim contradicted by the code. Recorded so that "not changed" is not mistaken for
"not checked".

| file | what was verified | classification of the corrected state |
|---|---|---|
| `CHARTER.md` | Five dated `[P0.1 amendment]` blocks: the mechanism list (`:37-44`), the deleted "enforces in code … guards in CI" clause (`:65-79`), the reproducibility and distribution bullets (`:99-128`), "then priced, validated and resolved" (`:182-195`), and the scope-and-honesty bullets (`:225-240`). The one inline deletion is the CI clause, made on the closed audit's explicit instruction (`docs/delivery/CURRENT-STATE-AUDIT.md:427`). `CHARTER.md:94` ("Capable of producing unintended consequences") is correctly left un-annotated per OQ-6. | Amendments accurate; no further edit made — see § Blocked on an owner decision, item 1 |
| `README.md` (rest of file) | The header warning (`:6-11`), the "**intended**" framing of the three-tier and LLM paragraphs, the founder-approved gateway sentence reproduced verbatim, the determinism table's Status column, the two precise test descriptions, the "there is no continuous integration" statement, the archetype paragraph, and the footer pointing at `NOTICE.md` rather than the non-existent `COPYRIGHT.md` | Corrected; CB-13 (broken `COPYRIGHT.md` link) is **already closed** — `ls COPYRIGHT.md` → no such file, and no reference to it remains in `README.md` |
| `scaffold/README.md` | The correction header (`:5-7`), the "Caveat on 'runs'" block (`:15-19`), the no-cross-tier-causality statement, the per-tier descriptions, the founder-approved gateway sentence, the "← PLANNED, NOT WIRED" annotation on the Postgres node and the paragraph beneath it, the archetype paragraph, and the psycopg2 LGPL correction | Corrected; CB-16's licence correction is **closed**. ⚠️ **CB-04 was WRONGLY recorded as closed — see amendment below** |

> **Amendment, 19 July 2026 — CB-04 was not closed.**
> The row above originally recorded CB-04's diagram annotation as "already closed". That was
> **wrong**, and the error is preserved here rather than rewritten because the mistake is itself
> evidence about how partial corrections get mistaken for complete ones.
>
> P0.1 annotated only the **Postgres node** of the `scaffold/README.md` architecture diagram. The
> more consequential falsehood in the same diagram was left unannotated: the `CohortAgent`
> arrow ran through `diffusion.py` into `MacroState`, drawing a **meso→macro causal channel that
> does not exist**, and labelled diffusion as "belief spread over networkx graph". Both are
> contradicted by the code, and by the prose twelve lines above them in the same file
> (`:24-26` "No tier reads another tier's state"; `:32-34` diffusion "computed but not wired to
> beliefs").
>
> This corresponds to **open critical finding 1**, and `CAPABILITY-CLAIMS.md` C8 names presenting
> apparent meso→macro movement as tier interaction "the single most misleading claim available
> about this codebase". Severity: **blocking**.
>
> **Evidence, verified by execution-free code reading on 19 July 2026:**
> `model.narrative_adoption` is written only at `engine.py:143` and read only at
> `routes_simulation.py:75` — it reaches no belief and no indicator. The only two `apply_deltas`
> call sites are `engine.py:136` (macro self-noise) and `engine.py:164` (micro effects-table
> lookup); neither involves cohorts or diffusion. The sole belief write in the tree is
> `government_competence` at `agents/cohort_agent.py:38`, driven by grievance drift, not diffusion.
>
> **Fixed 19 July 2026:** the diagram now terminates diffusion at `model.narrative_adoption`
> marked "← COMPUTED, NOT WIRED TO BELIEFS OR MACRO (P0.5 target)", marks the cohort path
> "✗ no path to MacroState", and carries a "Reading the diagram honestly" paragraph naming the
> only two writers of `MacroState`. **CB-04 is now closed.**

---

## Blocked on an owner decision — not corrected

1. **`CHARTER.md` — scope of permitted edits (OQ-6).** The charter self-declares non-negotiable and
   governing over every other document (`CHARTER.md:3-5`). Its existing amendments were made by a
   prior pass; this pass made none. The owner's decision is needed on (i) whether charter lines may
   be edited under P0.1 at all, (ii) whether the test is "contradicted by the code" or the narrower
   "identified by the closed audit", and (iii) whether charter bullets read as stated intent or as
   capability claims. `CHARTER.md:94` — "Capable of producing unintended consequences" — is the
   live instance: it is contradicted by the code but is **not** audit-identified, and annotating it
   would expand the false-claims population without the owner.

2. **"The full execution-ready plan" — three live instances (OQ-2).** `README.md:41`,
   `README.md:130` and `scaffold/README.md:138` (line numbers as of the end of this pass). All three attach the phrase to `docs/PLAN.pdf` —
   the *document* — not to the codebase, and `HANDOFF.md` § Standing constraints (`:135`) on its face governs descriptions of
   the codebase. Whether the constraint reaches them is a question about the constraint's scope.
   **Not changed**, because changing them would decide OQ-2 by default. The drafter's observation,
   offered as such and not as a finding: a reader meeting "execution-ready" in a table row that
   sits directly above a link to the scaffold may reasonably carry the phrase across.

3. **`scaffold/CLAUDE.md:59` — the branch and PR placeholder (CB-18).** Left in place and
   annotated. What the conventions should be is a policy decision, and an AI agent may draft a
   record but may not settle one. Phase 0 cannot exit while the marker stands
   (`docs/delivery/CURRENT-STATE-AUDIT.md:433`).

4. **Whether this register-driven pass is authoritative (OQ-5, OQ-5a).** Every correction above
   cites `docs/delivery/CAPABILITY-CLAIMS.md`, which is itself DRAFT and whose binding status is
   unanswered. If the owner answers OQ-5 no, the wording chosen here is a recommendation rather
   than a clearance. OQ-5a bears specifically on the word "runnable", live at `README.md:42` and
   `scaffold/README.md:9`, which a prior verification pass expressly cleared
   (`docs/delivery/A3-VERIFICATION-RESULTS.md:87-88`) and which this pass therefore did not touch.

---

## Out of scope for this pass — named so the silence is not read as clearance

- **`HANDOFF.md`** — excluded by instruction; its sequence insert and citation migration belong to
  a separate later pass.
- **Anything under `docs/`** — excluded by instruction.
- **All `.py` files, tests, JSON schemas and behaviour** — excluded by instruction. This leaves the
  fourteen-site B1 claim population **only partly corrected**: the front-door instances are done,
  but eleven code-docstring and comment sites remain live, among them
  `scaffold/backend/app/simulation/engine.py:3-4` and `:158`,
  `scaffold/backend/app/simulation/agents/institutional_agent.py:4-5`,
  `scaffold/backend/app/simulation/schemas/agent_schema.py:8`, `:157-158`, `:181-183`, `:242-244`,
  `:307`, `:350`, and `scaffold/backend/app/api/routes_simulation.py:4-5`, `:82-84`. **B1 is not
  cleared by this pass.** See CB-01, CB-02, CB-15.
- **`scaffold/docs/AGENT_TASK_TEMPLATE.md`** — not in the named scope. It carries two of the
  remaining dangling design-document citations (`:25`, `:54`), so the audit's §9 exit criterion at
  `docs/delivery/CURRENT-STATE-AUDIT.md:431` still fails after this pass. So do the citations at
  `scaffold/backend/app/simulation/schemas/agent_schema.py:3`,
  `scaffold/backend/app/simulation/schemas/macro_schema.py:3` and
  `scaffold/frontend/index.html:18`.
- **`docs/PLAN.pdf`** — not text-extracted. `README.md:41` presents it as a primary document and
  any capability claim inside it is uncovered by this pass or by the capability register.
- **Completeness.** This is not a fresh search for undiscovered false claims, which the standing
  constraints prohibit. It corrects the enumerated P0.1 population in the five named files. It is
  not proof that no other overstatement exists in them.

---

## Verification status of this report

**No code was executed during this pass.** Every code-side statement above rests on reading source
in the working tree, on absence of call sites confirmed by search, or on execution results already
recorded in `docs/delivery/A3-VERIFICATION-RESULTS.md`. Statements sourced from that document —
the 40-tick constraint hash, the perturbation matrix, the `TestClient` decision-endpoint run — were
not re-run and are second-hand here. That the five tests currently pass is **not** claimed: it is
unknown, and the environment in which they were recorded as passing is not reconstructible from
anything in this repository.

---

## Addendum — 19 July 2026: in-code corrections and two findings

**Supersedes the paragraph immediately above on one point.** The five tests *have* now been run:
**5 passed**, from a fresh virtual environment on Windows 10 / CPython 3.12.10, following the
documented two-command install. Evidence in `docs/delivery/P0-3-CI-STATUS.md`. The rest of the
"not verified" note stands.

### Docstring corrections (comment-only; no logic, test or schema changed)

Audit §9's P0.1 work list names these; the earlier pass was scoped away from `.py` files.

| Location | Claim before | Class | Claim after | Evidence |
|---|---|---|---|---|
| `app/api/routes_simulation.py:82` | "The engine records it; validation/pricing happens on tick." | **NOT IMPLEMENTED** | States the endpoint records only, appends `"effects": []`, returns `accepted: true` unconditionally, and stores the client's `legal_check` unexamined | `routes_simulation.py:80-101`; tick loop never reads `event_log` |
| `app/simulation/diffusion.py:5` | "The engine calls this to update `Narrative.adoption_by_cohort`." | **NOT IMPLEMENTED** | States output goes to `model.narrative_adoption`, read only by the API response, reaching no belief and no indicator | write `engine.py:143`; sole read `routes_simulation.py:75` |
| `app/simulation/diffusion.py:60` | "Adoption is monotonic non-decreasing" | **NOT IMPLEMENTED** | States the condition under which adoption decreases | derived below |
| `app/simulation/schemas/agent_schema.py:242` | "Legal-check outcome set by the engine (null until validated)." | **NOT IMPLEMENTED** | States nothing sets it; on the player path it is client-supplied and echoed unexamined | no legality check exists; `engine.py:121-130` |

### Finding 1 — the architecture diagram asserted a meso→macro channel (BLOCKING)

Recorded in full in the CB-04 amendment above. `scaffold/README.md:61-64` drew `CohortAgent`
through `diffusion.py` into `MacroState` and labelled diffusion "belief spread over networkx
graph" — twelve lines below prose stating the opposite. This is open critical finding 1 rendered
as a diagram, and `CAPABILITY-CLAIMS.md` C8 calls presenting apparent meso→macro movement as tier
interaction "the single most misleading claim available about this codebase". **Fixed.**

### Finding 2 — adoption is not monotonic non-decreasing (NEW; not audit-identified)

`diffusion.py:60` claimed monotonicity. The code contradicts it:

```python
jitter  = rng.uniform(-0.01, 0.01)                      # diffusion.py:84
gain    = suscept * (influence + seed_pressure) + jitter # diffusion.py:85
updated = adoption + gain * (1.0 - adoption)             # diffusion.py:86
```

Whenever `suscept * (influence + seed_pressure) < |jitter|` **and** the jitter draw is negative,
`gain` is negative, so `updated < adoption` and that cohort's adoption **decreases**. This is
reachable for any low-susceptibility or weakly-connected cohort. The `[0, 1]` clamp at `:87` masks
it only at the lower bound.

**No test asserts monotonicity**, so the property was never checked — the claim appeared in a
docstring and in ADR-009 and was never exercised. Docstring corrected; ADR-009 carries a dated
amendment. **Behaviour deliberately unchanged** — whether adoption *should* be monotonic is a
modelling decision for P0.5/P0.7, not a P0.1 truth correction, and the standing constraint forbids
changing simulation behaviour to make a finding disappear.
