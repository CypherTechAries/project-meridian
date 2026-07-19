# Corrective Backlog — deduplicated

**Status: DRAFT, pending owner review.** Drafted by an AI agent. No item here is approved, and no
open question in it has been answered. Nothing in this document constitutes a decision.

**Amended 19 July 2026** to apply the founder decision of 18 July 2026 establishing **P0.4A —
deterministic randomness architecture** as a Phase 0 workstream in its own right, sequenced between
P0.4 and P0.5. Entries CB-34 to CB-39 are new in that amendment; CB-20, CB-29 and CB-30 carry
cross-references added by it. The founder decision is the source for the P0.4A scope and its ten exit
criteria; `HANDOFF.md` § Phase 0 priority order (`:70-90`) predates the decision and does not yet list P0.4A, so no citation into
`HANDOFF.md` should be read as supporting the new workstream's existence.
**Amended 19 July 2026 — the sentence above is superseded on its second half.** By founder decision
of 19 July 2026, P0.4A was inserted into the canonical sequence at `HANDOFF.md` § Phase 0 priority
order, P0.4A (`:76-83`). `HANDOFF.md` is now a citable authority for the workstream's existence and
position. The founder decision of 18 July 2026 remains the source for P0.4A's **scope** and its ten
exit criteria, which `HANDOFF.md` does not restate. See `docs/delivery/HANDOFF-REFERENCE-MIGRATION.md`.

**Amended again 19 July 2026** to apply the founder decision of 18 July 2026 settling **B5 / P0.8 —
the dual-use position.** CB-32 was reclassified from an owner-decision item to a parent enforcement
item and now records the eight controls the decision names; entries **CB-40 to CB-47** are new,
one per control, all mapped to P0.8. **The decision did not clear B5.** It replaced "B5 needs a
decision" with "B5 needs eight controls implemented and verified", and its eighth control states
that disclosure and any future acceptable-use language are supplementary while technical enforcement
is mandatory. Anywhere in this document or its sources that reads "four of five clear by telling the
truth, only B5 needs a decision" is quoting a superseded framing. **None of the eight controls is
implemented**, and nothing in this amendment authorises building them.

**Amended a third time 19 July 2026** to record the founder correction on **Track C — the
interview-demonstration programme.** The correction states that Track C is **not** merely a
user-interface workstream: it has two converging lanes (**C-VISUAL** and **C-ENGINE**) and five gates
(**C0** to **C4**). Entries **CB-48 to CB-52** are new in that amendment, one per gate. They sit in a
new section placed after the P0.8 group, because Track C is not a Phase 0 item and does not appear in
`HANDOFF.md` § Phase 0 priority order (`:70-90`) at all — no citation into `HANDOFF.md` should be read as supporting its existence.
**Nothing in Track C is built.** No screen exists; `scaffold/frontend/` contains a single 67-line
development stub. Every entry below is written as a target with an unlock condition, and none of them
records progress. Three figures elsewhere in this document predate this amendment and were **not**
rewritten: the entry count reads "forty-seven" in the plain-English summary and under "Verification
status"; the field table states that an evidence requirement is present "on CB-32 and on CB-34 to
CB-47 only"; and the open-questions table opens with "Twelve." The count is now **fifty-two**, each of
CB-48 to CB-52 states an evidence requirement (so the number of entries without one remains
thirty-two), and three open questions are added by this amendment, making fifteen. **A follow-on pass
on 19 July 2026 reconciled two of those three figures and left one standing.** It added the three
Track C open questions to the open-questions table and reset its opening count from "Twelve" to
"Fifteen", because CB-48 and CB-51 both refer the reader to that table and the questions were not in
it; it added the Track C row to the summary tables, where CB-48 to CB-52 appeared nowhere; and it
added the Track C bullet to "Verification status of this record". The entry count "forty-seven" and
the field table's "CB-32 and CB-34 to CB-47 only" are still **not** rewritten. **Nothing in this
amendment authorises starting any Track C work, and the decision that gates all interface
implementation — D10, `docs/design/UI-RESEARCH-HANDOFF.md:405-406` — is unresolved.**

**Date:** 19 July 2026
**Baseline:** commit `71fa329` (authored 18 July 2026), branch `main`. No *tracked* file is
modified, but the tree carries untracked working documents — this record among them — so
`git status --short` is **not** empty. All file:line citations below are against the committed
content unless stated otherwise.

---

## Plain-English summary

This is a deduplicated list of the corrective items drawn from five named sources. It is not a new
audit and it contains no new findings: every item traces back to a document that already exists. It
is **not** a complete list of everything the project must fix before publication — see "What this
backlog does not contain".

**Known gaps — this backlog is not a complete sweep of P0.1.** `HANDOFF.md:70-71` defines P0.1 as
"Correct live false claims (CI, legality validation, persistence, replay, archetype extensibility,
execution readiness)". Six named categories. Four of them map onto entries here: CI (CB-03), legality
validation (CB-01, CB-02), persistence (CB-04) and archetype extensibility (CB-05). The other two
were **not swept**, and the omission is a hole in this record, not a finding that the categories are
clean:

- **Execution readiness has no entry, and the phrase appears nowhere in this document.** Five live
  instances sit in the front-door documents: `README.md:27` and `README.md:80` ("the full
  execution-ready plan"), `scaffold/README.md:101` ("the full execution-ready plan"),
  `scaffold/README.md:5` ("This repository is a **runnable skeleton**"), and `README.md:28` ("The
  runnable starter repository — FastAPI + Mesa backend with a passing test suite"). `HANDOFF.md` § Standing constraints (`:135`)
  makes this a named standing constraint: "Do not describe the codebase as execution-ready,
  replay-capable or fully deterministic." Note that three of the five attach "execution-ready" to
  `PLAN.pdf` — the *document* — rather than to the codebase, which may take them outside the
  constraint. That adjudication is exactly what an entry should surface; this record's silence must
  not be read as having made it.
- **`README.md:28` is the sharpest single instance.** "Runnable" and "a passing test suite" are both
  present-indicative capability claims. The first is contradicted by CB-25 (the documented install is
  broken); the second is contradicted by this record's own finding that **whether the five existing
  tests currently pass is unknown**, because no code was executed in this pass (see "Verification
  status of this record", and CB-27). An entry is needed, cross-referencing CB-25 and CB-27.
- **Replay** — no live replay claim was found in the tracked tree outside `HANDOFF.md`'s own
  instructions (`grep -rni "replay"` over `.md`/`.py`/`.json`/`.html`, excluding `docs/delivery/` and
  the untracked `docs/world-model/` and `docs/design/`, returns hits only in `HANDOFF.md`). That is an
  absence of hits, not a completed sweep: CB-04 covers the *persistence* claims that adjoin replay,
  and no entry here covers replay wording as such.

Separately, `README.md:61-63` ("The test suite is the point: `test_same_seed_is_deterministic`
proves reproducibility and `test_llm_gateway_cannot_write_state` guards the determinism boundary
against regression") is a live present-tense claim in the root front-door document, and it also has
no entry among the forty-seven, and CB-39 records a second live instance of the same defect in
`ADR-007`. It bears directly on two publication exit criteria
(`HANDOFF.md` § Publication exit criteria (`:98-99`), "False determinism and replay claims corrected" and "Existing tests and their
actual scope accurately described") and on the audit's §9 exit criterion at
`CURRENT-STATE-AUDIT.md:430`, which requires a reviewer to read both READMEs and find no
present-tense claim contradicted by the code. The founder-settled replacement wording is at
`HANDOFF.md:52-62`. This backlog, followed to completion, would close none of these gaps; entries
are needed.

The same defect tends to appear in several places under different names. A single false sentence —
"the engine validates legality" — is recorded as a publication blocker in one document, as a
finding in a second, as a correction instruction in a third, and it is physically present in fourteen
separate places in the repository. Left as four separate list items, it looks like four problems
and gets fixed once. So this backlog merges them: one entry per underlying defect, with every
source reference listed against it, so nothing looks dropped.

**Forty-seven entries.** Twenty-two of CB-01 to CB-24 are documentation corrections that change no
behaviour. The two exceptions in that range: **CB-17** is a correction to scenario data under
`scaffold/`, believed behaviour-neutral today on the basis that the field has no read site — grep
evidence, not an executed before/after comparison — and **CB-19** is already satisfied and requires
no action. Seven (CB-25 to CB-31) are packaging, CI or engineering-foundation items. Six (CB-34 to
CB-39) are the P0.4A deterministic-randomness workstream, added by the founder decision of
18 July 2026; they are engineering items and none of them is a documentation correction. Ten
(CB-32, CB-33 and CB-40 to CB-47) concern the influence-operations schema and its safeguards; **the
eight in CB-40 to CB-47 are engineering items, added by the founder decision of 18 July 2026 that
settled B5.** Cutting across those groups, eleven entries carry an open question that must be
answered before anyone can act (CB-14, CB-17, CB-18, CB-25, CB-26, CB-32, CB-39, CB-41, CB-43,
CB-44 and CB-46).

Four of the five publication blockers (B1-B4) clear by correcting text. **B5 does not, and — since
18 July 2026 — no longer clears by an owner decision either.** The decision was taken. It named
eight controls and made technical enforcement mandatory, so B5 now clears only when those controls
are implemented and verified. That enlarges the work behind the publication gate; it does not
shrink it.

---

## How to read an entry

| Field | Meaning |
|---|---|
| ID | Stable. Do not renumber. If an entry is dropped, mark it withdrawn rather than reusing the ID. |
| Owner | Who is accountable for the entry. **Every entry currently reads `Aries Russell (unassigned)`, because no assignment record exists anywhere in the tree** — the same convention `RAID-REGISTER.md` states for its own entries. Added by the cross-workflow integration sweep of 19 July 2026, which found the field absent from all forty-seven entries. **Do not read `unassigned` as delegation**, and do not read the uniform value as evidence that ownership has been considered per entry: it has not. |
| Clears blocker | `B1`-`B5` if completing this entry removes a publication blocker, otherwise `—`. |
| P0 | The Phase 0 priority item from `HANDOFF.md` § Phase 0 priority order (`:70-90`) that this belongs to, or **P0.4A**, which comes from the founder decision of 18 July 2026 and is not in `HANDOFF.md` at all. **Where `HANDOFF.md` § Phase 0 priority order (`:70-90`) names the category, the mapping is sourced. For CB-13, CB-14, CB-19 and CB-21 to CB-24 it is the drafter's classification** — all seven are false or stale claims, which is what P0.1 covers, but no source assigns them. CB-33 carries its own note for the same reason. CB-34 to CB-39 are mapped to P0.4A by the founder decision, which states the scope directly; their decomposition into six entries is the drafter's. |
| Effort | **The drafter's estimate. No source document assigns effort to any item.** trivial (single edit) / small (< 1 hour) / medium (a working session) / large (design work). These are for sequencing only and should be re-estimated by whoever executes. |
| Merged from | Every source item this entry absorbs. Nothing was discarded; it was consolidated here. |
| Evidence requirement | What would demonstrate the entry is done. **Present on CB-32 and on CB-34 to CB-47 only. The other thirty-two entries do not state one**, and the cross-workflow integration sweep of 19 July 2026 did not write them, because choosing what counts as proof for each is drafting work that belongs to whoever executes the entry. Read its absence as a gap in this record, not as an entry that needs no evidence. Workstream-level exit criteria do exist for the P0 items in `PHASE-0-REMEDIATION-PLAN.md` ("Testable exit criterion") and for the publication gate in `PUBLICATION-EXIT-CRITERIA.md` (C1-C14), but **neither maps to individual CB IDs**: the plan names nine of the forty-seven and the exit criteria name one, so no entry here can currently be closed against a stated test. |

**Sort order:** by P0 item, then blocker-clearing entries before non-blocker entries. Because the
sort is by P0 item and IDs are never reused or renumbered, CB-34 to CB-39 sit **between** CB-28 and
CB-29 in the document: P0.4A falls between P0.4 and P0.5 in the founder-set order, while the IDs
continue from the highest previously issued. The out-of-sequence numbering is deliberate, not an
error. The same applies inside P0.8: **CB-40 to CB-47 sit between CB-32 and CB-33**, because they
are the eight child entries of CB-32 and reading them apart from their parent would lose the
decision that created them. CB-33 therefore appears last in the P0.8 group despite its lower ID.

### What this backlog does *not* contain

It merges exactly five sources: audit §6.1, audit §9 Phase 0 work items, A3's "Corrections
required" list, the five publication blockers, and the stale-claim findings from the ground-truth
pass that preceded this record. It does **not** sweep in the rest of the audit wholesale. §6.2-§6.5
items appear here only where an audit §9 Phase 0 work item names them — CB-15, CB-16, CB-18, CB-19,
CB-25, CB-26, CB-27 and CB-33 each draw on §6.2-§6.5 on that basis, and two of them (CB-15's
citations of §6.22 and §6.25) absorb only part of the source finding, which is flagged in place. The
remaining §6.2-§6.5 findings and the §4/§5 behavioural findings are real, remain recorded in
`CURRENT-STATE-AUDIT.md`, and are Phase 1 and later. Items CB-28 to CB-31 hold their Phase 0
headings so the ordering stays visible.

**One later source was added by amendment.** CB-34 to CB-39 derive from a sixth source that did not
exist when the five above were merged: the founder decision of 18 July 2026 creating P0.4A. Their
evidence draws on audit items 17, 27 and 28 (`CURRENT-STATE-AUDIT.md:304, :319, :320`) and on
`A3-VERIFICATION-RESULTS.md` §6, which are pulled in on that basis rather than by the §6.2-§6.5
rule stated above.

---

## P0.1 — Correct live false claims

### CB-01 — Documents claim the engine validates legality and computes cost. It does not.

**Plain English.** The repository says in fourteen places that when the language model proposes an
action, the engine checks whether it is legal, whether it is feasible, and what it costs. The
engine does none of those things. The function that is supposed to do it looks the action up in a
seven-row table and returns a copy of the row.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** B1 · **P0:** P0.1 · **Effort:** medium

**Locations.** Front-door documents: `README.md:38` ("LLM proposes; engine validates legality and
computes cost/effect"); `README.md:41` ("engine rejects invalid actions"); `scaffold/README.md:19`
("*proposes* actions; the engine validates legality and computes effects"); `CHARTER.md:112`
("then priced, validated and"); `scaffold/docs/ARCHITECTURE_DECISIONS.md:54-55` (ADR-006,
"validates a proposal's legality/feasibility and computes magnitude itself (`_validate_and_price`)"
— the sentence begins on `:54` and ends on `:55`, which is the anchor audit §9 and audit `:158`
both use). Code docstrings:
`scaffold/backend/app/simulation/engine.py:3-4`;
`scaffold/backend/app/simulation/agents/institutional_agent.py:4-5`;
`scaffold/backend/app/simulation/schemas/agent_schema.py:157-158`;
`scaffold/backend/app/simulation/schemas/agent_schema.py:377-379`;
`scaffold/backend/app/api/routes_simulation.py:4-5`;
`scaffold/backend/app/api/routes_simulation.py:82-84`.

**Three further sites of the same claim**, surfaced by the `PUBLICATION-EXIT-CRITERIA.md` C2 grep and
re-confirmed against source on 19 July 2026. They are further instances of the already-identified B1
claim, not new findings, and no new investigation was opened to produce them:
`scaffold/backend/app/simulation/llm_gateway.py:60-61` ("The engine validates legality and computes
effects; this function never touches numeric state");
`scaffold/backend/app/simulation/schemas/agent_schema.py:8` ("the engine validates and applies
effects"); `scaffold/backend/app/simulation/engine.py:158` (comment: "Micro agents produce
proposals; engine validates + applies"). **The B1 population is therefore fourteen sites** — an
earlier draft of this entry listed eleven and omitted these three. This is the figure
`PHASE-0-REMEDIATION-PLAN.md` P0.1 Group A reconciles to. Note that
`PUBLICATION-EXIT-CRITERIA.md` C2's status section reports **ten** for a different reason: it counts
lines matched by one grep pattern, not enumerated claim sites, and that pattern does not match
`agent_schema.py:157-158`, `:377-379`, `routes_simulation.py:82-84` or the ADR-006 sentence. The
counts measure different things and neither is wrong.

**Evidence.** `scaffold/backend/app/simulation/engine.py:121-130` — the entire gate is
`base = ACTION_EFFECTS.get(proposal.action_type, {})` then `return dict(base)`. The signature
`_validate_and_price(self, proposal)` receives only the proposal, never the agent spec, so
constraints are structurally unreachable from it (`A3-VERIFICATION-RESULTS.md:104-105`). The
endpoint path was driven through the real API with `TestClient` and accepted an actor of
`janitor_with_no_authority` with a client-supplied `legal_check`
(`A3-VERIFICATION-RESULTS.md:120-141`).

**Correction required.** Reword each location to describe what the code does: the engine looks the
action type up in a fixed effects table and applies the resulting deltas. No legality check, no
feasibility check, no cost computation. A3 is explicit that implementing the evaluator is **not**
required to clear this blocker (`A3-VERIFICATION-RESULTS.md:241`).

**Do not touch `CHARTER.md:113-114`.** "The LLM may *propose* a composition; it never decides
whether the composition is legal, what it costs, or whether it succeeds" is **true** and is the
correctly-worded sibling of the false clause two lines above it.

**Merged from:** blocker B1 (`A3-VERIFICATION-RESULTS.md:241`); A3 correction 4
(`A3-VERIFICATION-RESULTS.md:218-221`); A3 check 5 (`:120-141`); audit §5.4, §5.5; audit §9 work
item "soften `ADR-006:54-55` and the six sibling claims to describe what `_validate_and_price`
actually does" (`CURRENT-STATE-AUDIT.md:427`).

---

### CB-02 — `legal_check` is documented as engine-set, in the schema and its published mirror.

**Plain English.** A field says the engine fills it in. Nothing ever fills it in, and the API will
accept and store whatever the client puts there. The same sentence has been published in a
cross-language JSON Schema, so it has left the codebase.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** contributes to B1 · **P0:** P0.1 · **Effort:** small

**Locations.** `scaffold/backend/app/simulation/schemas/agent_schema.py:242-244`
("Legal-check outcome set by the engine (null until validated).");
`scaffold/schemas/intervention.schema.json:50` (identical wording).

**Evidence.** `legal_check` occurs exactly twice across `backend/app`, `scenarios` and `schemas` —
both are declarations, neither is an assignment. Client-supplied values are echoed back and trusted
(`A3-VERIFICATION-RESULTS.md:134`).

**Correction required.** Reword both to state that the field is currently unused and set by
nothing. Keep the two in sync — the JSON mirror is published under
`https://meridian.example/schemas/`.

**Merged from:** audit §6.1 item 11 (`CURRENT-STATE-AUDIT.md:293`); audit §5.11; audit §9 work item
"reword `Intervention.legal_check` ... out of the present indicative"
(`CURRENT-STATE-AUDIT.md:427`).

**Uncertain.** Whether B1 is fully cleared by CB-01 alone or requires CB-02 as well is a judgement,
not something the source documents state. Treat them as a pair.

---

### CB-03 — `CHARTER.md` claims the determinism boundary is guarded in CI. There is no CI.

**Plain English.** The charter says an automated check runs on every change to stop the language
model writing simulation state. Two things are wrong with that sentence, not one. First, there is no
continuous integration of any kind, so nothing runs automatically. Second, the named test is not a
guard against state mutation: it checks that the object handed back does not happen to carry two
particular attribute names. It never attempts a mutation, and it examines nothing about what the
gateway imports or calls, so a gateway that wrote state by any other route would pass it. Building
CI (CB-27) would therefore make only the "runs automatically" half of the sentence true; the
"guards" half needs either a materially stronger test or a weaker claim.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** B2 · **P0:** P0.1 · **Effort:** small — two coupled edits: delete "in CI", and
weaken the "guards" clause to match what `test_llm_gateway_cannot_write_state` actually checks. (Not
"trivial": this entry's own **Correction required** section establishes that a single deletion leaves
the sentence still asserting more than the test delivers.)

**Location.** `CHARTER.md:44` — "(ADR-006) enforces in code and
`test_llm_gateway_cannot_write_state` guards in CI."

**Evidence — the "in CI" half.** No `.github/` directory exists. The only YAML file in the entire
tree is `scaffold/docker-compose.yml`. Reproducible check:

```
cd C:\Users\daijo\project-meridian
ls -a .github                                                    # No such file or directory
find . -path ./.git -prune -o \( -name "*.yml" -o -name "*.yaml" \) -print
```

**Evidence — the "guards" half.** `scaffold/backend/tests/test_engine.py:61-77`. The test calls
`propose_action` once and makes exactly three assertions: `isinstance(proposal, ActionProposal)`,
`not hasattr(proposal, "apply_deltas")`, and `not hasattr(proposal, "macro_state")`. That is an
attribute-presence check on a returned object. No mutation is attempted and no import-graph or
call-graph analysis is performed. The audit records the test as tautological (§5.3).

**Correction required.** The sourced instruction is narrow: audit §9 says delete "in CI" from
`CHARTER.md:44` (`CURRENT-STATE-AUDIT.md:427`). The alternative route is to build both the CI (CB-27)
and a genuine mutation guard; A3 accepts either route and expresses no preference between them
(`A3-VERIFICATION-RESULTS.md:242`). Note the audit also flags the same clause at
`CURRENT-STATE-AUDIT.md:362`, in the charter's deliverable-status row.

**Proposed scope expansion — drafter's judgement, not a source instruction.** Deleting "in CI" alone
leaves "guards" asserting more than the test delivers, so this record's view is that the surrounding
clause needs weakening too — for example, to describe the test as a structural check that the gateway
returns a proposal object rather than a state handle. The substance rests on an existing finding
(audit §5.3, the tautological test) and is not a new one, but no source asks for more than the
deletion. `CHARTER.md` is the project's non-negotiable governing text and the scope of an edit to it
is the owner's editorial call. This is offered as a proposal, not as what "needs" to happen.

**Drafter's judgement, not a source instruction.** The sources do not sequence these two routes.
This record's view is that the text correction should not wait for CI, because leaving a false claim
standing while infrastructure is built is the defect Phase 0 exists to remove — but that is the
drafter's reasoning on cost and risk, not something A3, the audit or `HANDOFF.md` states. The owner
may sequence it otherwise.

**Note on scope.** Deleting this clause is the *principal* edit needed to satisfy the audit's exit
criterion at `CURRENT-STATE-AUDIT.md:432` ("`grep -rn "in CI"` returns nothing that is false"), but
not the only line the criterion touches. As of this pass that grep over `.md`/`.py`/`.html`,
excluding `docs/delivery/`, returns **two** hits:

- `CHARTER.md:44` — false, and corrected by this entry.
- `docs/world-model/PERSON-MODEL.md:168` — "Sensitivity tests must run in CI." This states a
  *requirement* on future work rather than an accomplishment, so it may well pass the criterion's
  "nothing that is false" test; that assessment has not been made here and is left open.

Re-run the grep at the point of correction: the document set is still growing, and
`docs/world-model/` is untracked as of this baseline.

**Merged from:** blocker B2 (`A3-VERIFICATION-RESULTS.md:242`); audit §6.1 item 1
(`CURRENT-STATE-AUDIT.md:283`); audit §7 CI-pipeline row (`:373`); audit §7 charter row (`:362`);
audit §9 work item "delete 'in CI' from `CHARTER.md:44`" (`:427`); audit §9 exit criterion (`:432`).

---

### CB-04 — Three database tables are documented as persisted. Nothing is ever written.

**Plain English.** An architecture decision says the system stores each run, a snapshot of every
tick, and an append-only event log. The tables are defined in code but no row is ever created. The
only thing the application does with the database is try to create empty tables at startup, inside
an error handler that swallows the failure and carries on.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** B3 · **P0:** P0.1 · **Effort:** small

**Locations.** `scaffold/docs/ARCHITECTURE_DECISIONS.md:29-31` (ADR-003, present tense: "We persist
three things"; the "**Status:** Accepted." line is `:28`); `scaffold/README.md:41` (PostgreSQL shown as the terminus of the
architecture diagram, unannotated); `scaffold/backend/app/db/models.py:1-6` (module docstring,
"Three tables capture the reproducibility contract").

**Evidence.** `SimulationRun`, `StateSnapshot` and `EventLog` appear only as class definitions and
`relationship()` back-references in `scaffold/backend/app/db/models.py:23,34,37,42,53,56,66`. There
is no `session.add`, `.commit` or `.merge` call anywhere in the scaffold. `get_db()` is defined at
`scaffold/backend/app/db/session.py:44` and used by no route. `init_db()` is called once from
`scaffold/backend/app/main.py:30-39` inside a bare `except Exception` that logs "Running in-memory
only." and continues.

**Correction required.** Add an "in the scaffold" caveat to ADR-003, matching the convention
already used at `ADR-004:37` and `ADR-005:45`; annotate the Postgres node in the
`scaffold/README.md:41` diagram as planned; reword the `models.py` docstring to say the schema is
designed and unwired.

**Merged from:** blocker B3 (`A3-VERIFICATION-RESULTS.md:243`); audit §5.14; audit §7
persistence-strategy row (`:387`); audit §9 work items "add 'in the scaffold' caveats to `ADR-003`"
and "annotate the Postgres node in the `scaffold/README.md:41` diagram as planned" (`:427`).

---

### CB-05 — "Adding an archetype requires only a new JSON" is false and fails silently.

**Plain English.** Four documents promise that adding a new nation type means dropping in a data
file and never editing the engine. It does not hold, and when it fails it fails quietly rather than
raising an error.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** B4 · **P0:** P0.1 · **Effort:** small

**Locations.** `README.md:72-74` ("Nation archetypes are **data, not code**. Adding one means
adding a scenario-template JSON that conforms to the existing schemas — never editing the engine.");
`scaffold/README.md:106-107` ("Nation types are **data, not code** (PLAN.pdf §9)");
`scaffold/docs/ARCHITECTURE_DECISIONS.md:75` (ADR-008, "Adding an eighth archetype must require
only a new `scenarios/*.json`."); `scaffold/CLAUDE.md:53-55` ("Do **not** edit the engine.").

**Correction required.** Qualify all four to state the current archetype constraints: an action
type absent from `ACTION_EFFECTS` (`scaffold/backend/app/simulation/engine.py:35-43`) produces an
empty delta, and `apply_deltas` (`scaffold/backend/app/simulation/agents/macro_state.py:36-41`)
skips any key it does not recognise with no error, no warning and no return value. New scenario
data can therefore be loaded and have no effect, undetectably.

**Citation drift.** The audit cites this claim at `README.md:106-107`. The root `README.md` has
since been rewritten and is 96 lines; the claim now sits at `README.md:72-74` with different
wording. The `(PLAN.pdf §9)` phrasing the audit quotes survives only in `scaffold/README.md`. See
CB-21.

**Merged from:** blocker B4 (`A3-VERIFICATION-RESULTS.md:244`); audit §5.6; audit §9 work item
"qualify `README.md:106-107` and `ADR-008:75` to state the current archetype constraints" (`:427`).

---

### CB-06 — Prompt versioning is described in the present tense and does not happen.

**Plain English.** Two documents say generated text is logged and versioned by which model produced
it, which prompt version, and at what temperature. One constant is declared in the code and read by
nothing. No model id or temperature is recorded anywhere.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** trivial

**Locations.** `scaffold/docs/ARCHITECTURE_DECISIONS.md:66-67`; `scaffold/CLAUDE.md:25-26`.

**Evidence.** `PROMPT_VERSION = "v1"` is declared at
`scaffold/backend/app/simulation/llm_gateway.py:38` and has no read site: `grep -rn "PROMPT_VERSION"
backend/app scenarios schemas` from `scaffold/` returns that one line.

**Correction required.** Make both statements conditional — this is the intended contract when a
live model is wired, not current behaviour.

**Merged from:** audit §6.1 item 2 (`CURRENT-STATE-AUDIT.md:284`); audit §9 work item "make
`ARCHITECTURE_DECISIONS.md:66-67` and `CLAUDE.md:25-26` conditional" (`:427`).

---

### CB-07 — "Seeded Monte Carlo draws" overstates one uniform draw on one indicator.

**Plain English.** The README describes the macro tier as using Monte Carlo methods, which implies
running many simulated futures. There is one random number per tick, applied to a single indicator.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** trivial

**Location.** `README.md:36` — "| Macro indicators | Deterministic rules + seeded Monte Carlo draws
| None |".

**Evidence.** `scaffold/backend/app/simulation/engine.py:132-136` — the whole per-tick macro rule
set is `noise = self.rng.uniform(-0.002, 0.002)` applied to
`shipping_throughput_pct_of_baseline`. No ensembles.

**Correction required.** Replace with "seeded stochastic draws" per the audit's own wording.

**Merged from:** audit §6.1 item 3 (`CURRENT-STATE-AUDIT.md:285`); audit §9 work item "correct
`README.md:36` to 'seeded stochastic draws'" (`:427`).

---

### CB-08 — Three README rows describe language-model functions that do not exist.

**Plain English.** The determinism table promises the model designs adversary campaigns, writes
briefings grounded in retrieval over real state, and parses the player's typed input into a
validated action. None of those three functions exists.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** small

**Locations.** `README.md:39` (adversary campaign design); `README.md:40` (advisor dialogue
"grounded by retrieval over true state"); `README.md:41` (player decision interpretation).

**Evidence.** `scaffold/backend/app/simulation/llm_gateway.py` defines exactly three functions:
`_stub_action_type` (`:41`), `propose_action` (`:54`), `generate_briefing` (`:85`). There is no
campaign-composition function and no decision-parsing function. `generate_briefing`
(`:85-103`) performs no retrieval — it reads two keys from the mapping it is handed (`indicators`
and `tick`, at `:95-96`) and two values out of the nested `indicators` dict (`:97-98`), then returns
an f-string. (The audit states this as "two keys" at `CURRENT-STATE-AUDIT.md:287`; an earlier draft
of this entry said "three", which matches neither the code nor the source.)

**Correction required.** Mark the unimplemented rows as planned rather than describing them in the
present tense.

**Merged from:** audit §6.1 items 4 and 5 (`CURRENT-STATE-AUDIT.md:286-287`); audit §9 work item
"mark the unimplemented rows of the `README.md` determinism table as planned" (`:427`).

---

### CB-09 — README says diffusion updates cohort beliefs. It does not reach them.

**Plain English.** The README says cohort beliefs change through seeded diffusion across the social
graph. Diffusion runs and produces numbers, but those numbers are written to a separate variable
and never touch cohort beliefs. An internal document in the same repository already states the
truth and contradicts the README.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** trivial

**Location.** `README.md:37` — "| Cohort belief updates | Seeded diffusion over the social graph |
None for the numbers; may label the resulting shift |".

**Evidence.** `scaffold/backend/app/simulation/engine.py:137-145` assigns diffusion output to
`self.narrative_adoption`. The only cohort field ever written anywhere is
`beliefs.government_competence`, decremented by grievance drift at
`scaffold/backend/app/simulation/agents/cohort_agent.py:35-38`. The contradicting internal document
is `scaffold/docs/AGENT_TASK_TEMPLATE.md:48-49`: "Hostile campaigns currently spread narrative
adoption but don't yet move cohort beliefs."

**Correction required.** Per the audit's own wording: "grievance-driven drift, diffusion adoption
computed but not yet wired to beliefs."

**Merged from:** audit §6.1 item 7 (`CURRENT-STATE-AUDIT.md:289`); audit §9 work item "correct
`README.md:37`" (`:427`).

---

### CB-10 — The charter claims the system models a distribution of outcomes. Effects are constants.

**Plain English.** The charter says an action can have several plausible outcomes and that the
system models the spread rather than pretending one future is correct. Each action has exactly one
hard-coded effect.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** small

**Location.** `CHARTER.md:61-62` — "The system models a **distribution**, rather than pretending
there is one objectively correct future."

**Evidence.** `ACTION_EFFECTS` (`scaffold/backend/app/simulation/engine.py:35-43`) is a seven-row
table of fixed scalar constants, and `_validate_and_price` (`:121-130`) returns `dict(base)` — a
per-action constant. The audit adds that `Outcome.confidence` is never constructed.

**Correction required.** Restate as intent, or scope it to the target contract rather than current
behaviour.

**Uncertain — drafter's judgement, not a source position.** This record's reading is that a target
framing is available here because the charter declares itself normative, provided the target is
explicitly labelled as one. No source document says that. It is adjacent to founder decision 8.4,
which is settled precisely on what may be stated as delivered versus target
(`HANDOFF.md:52-62`), and 8.4's settled wording addresses reproducibility, not outcome
distributions. Whether a charter-level claim may be reframed as a target rather than simply
corrected is the owner's call, not this record's.

**Merged from:** audit §6.1 item 6 (`CURRENT-STATE-AUDIT.md:288`); audit §9 blanket instruction
"correct or caveat every item in 6.1" (`:427`).

---

### CB-11 — "Sole writer of numeric state" is right about ownership, wrong as a literal file claim.

**Plain English.** Three places say `engine.py` is the only file that writes simulation numbers.
The ownership model is correct and should be kept, but the sentence as written is literally false:
two other files perform the actual assignments.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** small

**Locations.** `scaffold/docs/ARCHITECTURE_DECISIONS.md:53-54`; `scaffold/CLAUDE.md:13-14`;
`scaffold/backend/app/simulation/engine.py:3`.

**Evidence.** Macro values are assigned at
`scaffold/backend/app/simulation/agents/macro_state.py:47`; cohort beliefs at
`scaffold/backend/app/simulation/agents/cohort_agent.py:38`
(`b.government_competence = max(0.0, b.government_competence - drift)`; `:37` is the preceding
binding `b = self.cohort.beliefs`). This is the anchor the audit's own item 8 uses
(`CURRENT-STATE-AUDIT.md:290`); an earlier draft of this entry cited `:37`, which is the line above
the assignment.

**Correction required.** Reword to describe ownership ("the engine is the only component that
*decides* numeric state") rather than file scoping. The audit is explicit: reword rather than
refactor.

**Merged from:** audit §6.1 item 8 (`CURRENT-STATE-AUDIT.md:290`); audit §9 work item "reword the
'sole writer' sentences" (`:427`).

---

### CB-12 — Nine citations point at five design documents that do not exist.

**Plain English.** Code and documentation cite five design and research files as sources of truth.
None of the five is in the repository. One citation even states they are "in the workspace root",
which is straightforwardly false.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** medium

**Missing files.** `design_simulation_schemas.md`, `design_nation_expansion.md`,
`design_ux_screens.md`, `research_architecture.md`, `research_licensing.md`.

**Locations (8 named + 1 glob).** `scaffold/backend/app/simulation/schemas/agent_schema.py:3`;
`scaffold/backend/app/simulation/schemas/macro_schema.py:3`; `scaffold/CLAUDE.md:49`;
`scaffold/docs/AGENT_TASK_TEMPLATE.md:54`; `scaffold/docs/ARCHITECTURE_DECISIONS.md:4` (cites two
of the five on one line); `scaffold/docs/ARCHITECTURE_DECISIONS.md:25`;
`scaffold/docs/ARCHITECTURE_DECISIONS.md:71`; `scaffold/frontend/index.html:18`. Glob reference:
`scaffold/docs/AGENT_TASK_TEMPLATE.md:25` ("design nuance from the workspace `design_*.md` docs").

**Correction required.** Repoint each at the corresponding `PLAN.pdf` section, per the audit.
`scaffold/README.md:95-104` records the consolidation itself — "The canonical specs are consolidated
one level up", listing `CHARTER.md` and `PLAN.pdf`. It says nothing about the citations. The claim
that they "were not updated" is the audit's own gloss (`CURRENT-STATE-AUDIT.md:292`), consistent
with the consolidation but not recorded in the README or anywhere else in the tree.

**Count correction.** The audit's item 10 is headed "Ten references" but its evidence column
actually enumerates **eleven** line-references: `ARCHITECTURE_DECISIONS.md:4, 25, 71`;
`CLAUDE.md:49`; `AGENT_TASK_TEMPLATE.md:25, 54`; `index.html:18`; `agent_schema.py:3`;
`macro_schema.py:3`; `plan.txt:138, 168` (`CURRENT-STATE-AUDIT.md:292`). Removing the two anchored
to the deleted `plan.txt` leaves nine, which matches direct observation of the current tree. So the
current count is nine — but note that this does not reconcile with the audit's stated "ten", because
the audit's own headline and enumeration disagree. See CB-22.

**Exit criterion.** `CURRENT-STATE-AUDIT.md:431` requires that
`grep -rn "design_.*\.md\|research_.*\.md"` over project files returns zero results, or only results
pointing at files that exist. Run verbatim (excluding `docs/delivery/`) it returns **nine** lines —
the eight named-file citations plus the glob at `AGENT_TASK_TEMPLATE.md:25`, which the criterion's
`.*` wildcard matches. This criterion fails today. (An earlier draft of this entry said eight; that
figure came from a narrower pattern, `design_[a-z_]*\.md`, than the criterion quotes.)

**Merged from:** audit §6.1 item 10 (`CURRENT-STATE-AUDIT.md:292`); audit §9 work item "repoint the
ten dangling design-doc citations at their `PLAN.pdf` sections" (`:427`); audit §9 exit criterion
(`:431`).

---

### CB-13 — `README.md` links to `COPYRIGHT.md`, which does not exist. The file is `NOTICE.md`.

**Plain English.** The last line of the README tells the reader to see `COPYRIGHT.md` for licensing
terms. There is no such file. The document that actually holds the licensing position is `NOTICE.md`.
As of this drafting date it is the only markdown link in the tree's **authored prose** that fails to
resolve. That scoping is load-bearing and not a hedge: this backlog itself creates a second
unresolvable target in this very entry, and `RAID-REGISTER.md` I5 a third, both by quoting the
README's link markup verbatim inside `docs/delivery/`, where `COPYRIGHT.md` does not resolve either.
*(Cited by entry ID rather than line number: sibling drafts are live documents and their line
numbers move.)*
Non-markdown link targets were not enumerated. Like every count in this record, this must be re-run
at the point of correction rather than quoted forward — the tree is still growing.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** trivial

**Location.** `README.md:96` — "Licensing and contribution terms are under review. See
[`COPYRIGHT.md`](COPYRIGHT.md)."

**Evidence.** A full-tree file listing shows `NOTICE.md` present and no `COPYRIGHT.md` at any path.
A resolution pass over every local (non-`http`) markdown link target in the tree finds exactly one
failure in authored prose — `README.md:96 -> COPYRIGHT.md` — plus two self-inflicted ones under
`docs/delivery/` where this record and `RAID-REGISTER.md` quote that same markup verbatim. Exclude
`docs/delivery/` when re-running, or the record reports its own quotations as defects. Reproducible
check — enumerate the targets,
then resolve each `](target)` relative to its containing file:

```
cd C:\Users\daijo\project-meridian
ls COPYRIGHT.md                          # No such file or directory
grep -rnoE "\]\(([^)]+)\)" --include="*.md" .
```

Do not quote a link *total* from this: the count is not stable while new documents are being added
to the tree, and it depends on which directories are excluded. Quote the failure, not the total. (An
earlier draft of this entry cited "16 links, fifteen resolve"; that figure is not reproducible with
the command above, which currently returns hundreds of matches across the whole tree. The
conclusion — one broken target, and it is this one — was re-verified independently.)

**Correction required.** Repoint the link to `NOTICE.md`. Also re-anchor the audit's citation at
`CURRENT-STATE-AUDIT.md:237`, which names `COPYRIGHT.md` as the file holding the licensing
position — the substance of that finding still holds against `NOTICE.md`, which likewise contains
no acceptable-use or field-of-use restriction; only the filename is wrong. See CB-21.

**Merged from:** verified directly in the ground-truth pass for this record; overlaps the stale
citation at `CURRENT-STATE-AUDIT.md:237`.

---

### CB-14 — `NOTICE.md` states the source is publicly visible. The repository is private.

**Plain English.** The document recording the licensing position says, in the present tense, that
the source code is publicly visible. The settled founder decision is that the repository is private
until Phase 0 passes. This is the same defect class Phase 0 exists to fix, sitting inside the
document that records the licence decision.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** trivial once the open question is answered

**Location.** `NOTICE.md:11` — "The source code is publicly visible for evaluation and portfolio
purposes."

**Evidence.** `HANDOFF.md:13` — "**PRIVATE.** Deliberately." The same wording previously sat at
`README.md:92` and the audit records it there at `CURRENT-STATE-AUDIT.md:237`, `:393` and `:403`
only; the README has since been rewritten and no longer claims public status. The wording migrated
rather than being removed. (An earlier draft also cited `:342` here. That is wrong: audit `:342` is
item 40, "No LICENSE file — `README.md:92-94` states an all-rights-reserved position in prose",
which is a different claim. It is correctly cited for that claim in CB-21's second row.)

**OPEN QUESTION for the owner.** Was this sentence written as a statement of present fact, or as a
description of the intended post-publication position? The correction differs: if the former,
delete or negate it now; if the latter, mark it explicitly as conditional on publication. An AI
agent cannot resolve authorial intent and this record does not attempt to.

**Merged from:** ground-truth stale-claim finding; related audit citations at
`CURRENT-STATE-AUDIT.md:237, :393, :403`.

---

### CB-15 — Six code docstrings describe unimplemented behaviour in the present indicative.

**Plain English.** Six comments in the source describe things the code does not do, written as
though it already does them. Each is a small edit; grouped here because the correction is the same
in every case — move the sentence out of the present tense, or delete it.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** small

| Location | Claim | Reality |
|---|---|---|
| `scaffold/backend/app/simulation/schemas/agent_schema.py:181-183` | `constraints`: "Hard legal/procedural constraints on the agent." | Causally inert. Proven by substitution: 40-tick state hash identical with and without them (`A3-VERIFICATION-RESULTS.md:92-98`). The gate never receives the agent spec. |
| `scaffold/backend/app/simulation/agents/macro_state.py:26-27` | "Nested blocks (e.g. institutional trust) are handled explicitly by the engine, not here." | No code anywhere writes any nested block. `apply_deltas` skips non-scalar attributes (`:39-41`), so `institutional_trust`, `alliance_confidence` and `public_finances` are structurally unreachable. |
| `scaffold/backend/app/simulation/diffusion.py:51` | "Adoption is monotonic non-decreasing and clamped to [0, 1]." | The jitter term at `:75` spans −0.01 to +0.01 and is added to `gain` at `:76`, so adoption can fall. Only the clamp half of the sentence holds. |
| `scaffold/backend/app/simulation/diffusion.py:5` | "The engine calls this to update `Narrative.adoption_by_cohort`." | The engine assigns the result to `self.narrative_adoption`, an unnamed dict (`engine.py:143-145`). The `Narrative` model is never instantiated. |
| `scaffold/backend/app/simulation/schemas/agent_schema.py:307` | `CampaignMetrics`: "Live campaign metrics, all computed by the diffusion model — never by the LLM." | Never computed. `exposure`, `belief_adoption`, `resistance`, `detection_probability` and `attribution_probability` all sit at their 0.0 defaults; `Campaign` is never instantiated. |
| `scaffold/backend/app/simulation/schemas/agent_schema.py:350` | `Outcome`: "The resolved result of a decision, with an explanation trace for the 'why' system." | `Outcome` is never constructed; there is no explanation trace and no "why" system. |

**Correction required.** Reword each to declarative-of-intent or mark unimplemented. The second half
of the `diffusion.py:51` sentence is true and should be kept.

**Merged from:** A3 correction 7 (`A3-VERIFICATION-RESULTS.md:225-226`); audit §6.22
(`CURRENT-STATE-AUDIT.md:314`) **in part**; audit §6.25 (`:317`) **in part**; audit §9 work item
"reword `Intervention.legal_check`, `CampaignMetrics`, `Outcome` and `diffusion.py:5` docstrings out
of the present indicative" (`:427` — the `legal_check` portion is CB-02).

**Partial absorption — flagged so it does not read as full coverage.** Two of the sources above are
absorbed only in part, and the remainder is *not* carried anywhere else in this backlog:

- Audit §6.22's headline finding is "Bounds enforcement is a four-name literal"
  (`macro_state.py:30-35`). This entry carries only its trailing clause about the `:26-27`
  nested-blocks docstring.
- Audit §6.25's headline finding is "Diffusion silently drops schema-valid edges" —
  `diffusion.py:33-36` guards with `if other in cohesion:` while `agent_schema.py:86-88` documents
  `bridges_to` as cohorts *or institutions*, so an institution target is discarded with no warning.
  This entry carries only its trailing clause about `diffusion.py:51` monotonicity.

Both dropped halves are behavioural findings rather than false documentary claims, so they sit
outside this record's P0.1 remit and remain recorded in `CURRENT-STATE-AUDIT.md` for Phase 1. They
are named here rather than left silent.

**Citation correction.** An earlier draft of this entry cited A3 correction 8 (`:227`). That is
wrong: A3 item 8 is "New §6.x — `apply_deltas` silently ignores unknown keys", which corresponds to
none of the six rows above and is correctly claimed by CB-20's table row 8. The attribution has been
removed here to avoid double-counting a single source item.

---

### CB-16 — "Stack chosen for permissive licensing" omits an LGPL dependency.

**Plain English.** The scaffold README says the technology stack was chosen for permissive
licensing and names three permissive packages. A fourth dependency, the Postgres driver, is LGPL,
and is not mentioned.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** trivial

**Locations.** `scaffold/README.md:111`; the dependency at `scaffold/backend/requirements.txt:17`
(`psycopg2-binary`).

**Correction required.** Acknowledge psycopg2's LGPL licence. The audit notes it is commercially
benign under the SaaS model `PLAN.pdf` assumes (dynamic linking, no distribution) but that the
sentence as written is inaccurate, and that psycopg2 is absent from the `PLAN.pdf` §2 licence audit.

**Merged from:** audit §6.5 item 39 (`CURRENT-STATE-AUDIT.md:341`); audit §7 licence-inventory row
(`:379`); audit §9 work item "correct `scaffold/README.md:111` to acknowledge psycopg2's LGPL"
(`:427`).

---

### CB-17 — A demo-scenario population figure is recorded by the audit as wrong by roughly 63×, undetectably. The intended value could not be re-verified.

**Plain English.** The audit records this cohort's population as 14,200 where it derives roughly
900,000 from the plan. The 14,200 is directly observed in the scenario file. The ~900,000 is the
audit's derivation, cited to a file that no longer exists, and was **not** re-verified in this pass —
so treat the 63× magnitude as the audit's claim rather than as an observation of this record.
Whatever the correct figure, the error produces no symptom today, because the field is read by no
code at all: every cohort carries identical weight regardless of the population it stands for.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** trivial to edit; blocked on an open question

**Location.** `scaffold/scenarios/kestral-strait.json:79` — `"represents_population": 14200` for
`coastal-creole-fishing`.

**Evidence.** `represents_population` has no read site. Its only occurrences across `backend/app`,
`scenarios` and `schemas` are the docstring at
`scaffold/backend/app/simulation/schemas/agent_schema.py:92`, the declaration at `:95`, the JSON
mirror, and the five scenario values (`kestral-strait.json:39, 79, 122, 162, 202`). Diffusion
weights edges by `internal_cohesion` only. The five cohorts sum to 1,488,200; no total-population
field exists in any scenario or schema.

**Behavioural safety — inferred, not executed.** `represents_population` has no read site anywhere
in `backend/app`: the only occurrences are the docstring, the declaration, the JSON mirror and the
five scenario values, all cited above. On that basis correcting the value is **not expected** to
change any simulation output. This rests on grep-verified absence of call sites and on source
reading — **not** on an executed before/after comparison, which this pass did not perform. It will
in any case become behaviour-affecting the moment P0.5 lands (CB-29), because `HANDOFF.md` § Phase 0 priority order (`:84`)
requires that `represents_population` affect aggregation.

**Sequencing — drafter's judgement, not a source instruction.** This record's view is that the data
correction should land before CB-29, while it is still behaviour-neutral. `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84`) establishes
the dependency but **no source sequences the data fix relative to P0.5**. The owner may sequence
otherwise.

**OPEN QUESTION for the owner — two parts, neither resolved here.**

1. *What is the correct value?* The audit derives ~900,000 from a "4.1-million-person archipelago"
   with a "22% Northern Creole minority", citing `plan.txt:229` (`CURRENT-STATE-AUDIT.md:217`).
   `plan.txt` no longer exists and the figure could not be re-verified from `docs/PLAN.pdf` in this
   pass. Confirm the intended figure, and decide whether a total-population field should exist at
   all.
2. *Is this edit permitted at all under the standing constraints?* This is the only entry in the
   backlog that would write a file under `scaffold/`. The standing constraints say both "do not
   modify simulation behaviour" and "do not edit any code under `scaffold/` — documents only".
   Whether scenario JSON counts as "code" for the second constraint is a question for the owner, and
   this record does **not** answer it. A future executing agent must treat CB-17 as unauthorised to
   write until the owner says otherwise, regardless of the behavioural-safety reasoning above.

**Merged from:** audit §5.10 (`CURRENT-STATE-AUDIT.md:215-221`); audit §9 work item "correct
`coastal-creole-fishing.represents_population` in the demo scenario" (`:427`).

---

### CB-18 — The branch and pull-request policy sits under an unresolved placeholder marker.

**Plain English.** The change-control section carries a note saying it should be filled in with the
team's real conventions. It is the only unresolved marker in the whole project, and Phase 0 cannot
exit while it stands.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** trivial to edit; blocked on an open question

**Location.** `scaffold/CLAUDE.md:59` — `<!-- PLACEHOLDER: fill in with the team's real conventions -->`.

**Evidence.** Reproducible check — returns exactly this one line:

```
cd C:\Users\daijo\project-meridian
grep -rn "PLACEHOLDER" --include="*.md" --include="*.py" --include="*.html" . | grep -v "^./docs/delivery/"
```

**Exit criterion.** `CURRENT-STATE-AUDIT.md:433` requires that no unresolved `PLACEHOLDER` marker
remains. Fails today.

**OPEN QUESTION for the owner.** What are the branch and pull-request conventions? `HANDOFF.md:21`
settles the default branch as `main` and `HANDOFF.md:23` settles that external code contributions
are not accepted, which narrows this considerably — but the review and merge policy for the owner's
own work is not recorded anywhere. Resolve it or delete the section; do not leave the marker.

**Merged from:** audit §6.5 item 45 (`CURRENT-STATE-AUDIT.md:347`); audit §7 change-control row
(`:371`); audit §9 work item "resolve or delete the `CLAUDE.md:59` placeholder" (`:427`); audit §9
exit criterion (`:433`).

---

### CB-19 — Delete `backend/plan.txt`. **ALREADY SATISFIED — no action required.**

**Plain English.** The audit found a 498-line uncontrolled duplicate of the plan sitting inside the
Docker build context, and Phase 0 scheduled its deletion. The file is no longer in the repository.
Recorded here so it stops appearing on work lists.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** none

**Evidence.** `find . -path ./.git -prune -o -name "plan.txt" -print` returns nothing. The full
55-file tracked-file listing contains no `scaffold/backend/plan.txt`.

**Consequential note.** Three of the audit's evidence citations were anchored to this file and are
now unresolvable — see CB-22. The audit's decision-7 argument that "`backend/plan.txt` is already an
uncontrolled duplicate of it inside the build context" (`CURRENT-STATE-AUDIT.md:413`) no longer
applies; the other arguments in that decision are untouched.

**Uncertain.** Whether the deletion was a deliberate corrective action or incidental to the initial
commit cannot be determined — the single-commit history offers no before-and-after to compare.

**Merged from:** audit §6.5 item 47 (`CURRENT-STATE-AUDIT.md:349`); audit §9 work item "delete
`backend/plan.txt`" (`:427`); audit §9 Phase 1 exit criterion referencing `plan.txt` (`:447`).

---

### CB-20 — Apply A3's six outstanding amendments to `CURRENT-STATE-AUDIT.md`.

**Plain English.** The A3 re-verification produced eight required amendments to the audit document.
Two of them are handled elsewhere in this backlog. The remaining six have not been applied — the
audit still reads as it did before A3 ran.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** medium

| A3 item | Target | Amendment |
|---|---|---|
| 1 | audit §4.1 | Add the RNG-contamination distinction and the newly exposed no-substreams defect. The section currently implies meso→macro influence is simply absent; it is absent *and* spuriously coupled through a shared RNG stream. **This row stays in P0.1: it is an amendment to the audit's text, not engineering work. The engineering response to the same defect is P0.4A — see CB-34 to CB-39.** |
| 2 | audit §4.2 | Record that varied action selection was tested and does not prevent saturation, and that no cost/cooldown/decay mechanism exists. Escalate from calibration to architecture. |
| 3 | audit §5.4 `:156` | Add: the gate could not read constraints even if it wanted to — `_validate_and_price` (`engine.py:121-130`) is passed only the proposal, never the agent spec. |
| 5 | audit §5.7 `:188` | Add the control-run evidence that `block_unfunded_spending` is causally inert (deleting the finance minister leaves `military_readiness` at t5 bit-identical at `0.44000000000000006`). |
| 6 | audit §5.6 `:180` | Add that there are no terminal semantics at all: `run(400)` completes with nothing evaluating win or loss. |
| 8 | new audit §6.x | Record that `apply_deltas` silently ignores unknown keys (`macro_state.py:37-38`). Recommend a strict mode that raises. |

**Handled elsewhere — partly.** A3 item 7 (`agent_schema.py:182` constraints docstring) is CB-15
row 1, fully.

A3 item 4 is **not** fully handled and an earlier draft booked it as though it were. Item 4
(`A3-VERIFICATION-RESULTS.md:218-221`) has two halves. Its second half — add `README.md:38` and
`scaffold/README.md:19` as front-door untruths — is carried by CB-01, which corrects that source
text. Its first half is a re-anchoring instruction against **two** audit locations: "§5.4 `:158` and
§5.5 `:168` — re-anchor the `CHARTER.md` citation. `CHARTER.md:114` ... is **true**. The false clause
is `CHARTER.md:112`." Neither is carried:

- `CURRENT-STATE-AUDIT.md:158` cites `CHARTER.md:113` in its seven-places list. CB-21's row for
  `:158` covers only the `README.md:19`/`:24` drift, **not** the CHARTER citation.
- `CURRENT-STATE-AUDIT.md:168` characterises `CHARTER.md:113-114` as the location of the claim. It
  appears **nowhere** in this backlog.

Both are now added to CB-21 as explicit rows. Recorded here rather than left silent, because booking
one of A3's eight amendments as handled when it is not is precisely the double-counting error CB-15's
**Citation correction** note exists to prevent.

**Merged from:** `A3-VERIFICATION-RESULTS.md:208-227` items 1, 2, 3, 5, 6, 8.

**Uncertain.** The line references in the first column are A3's own citations into the audit. They
were not individually re-verified in this pass; the audit has not been edited since (single commit,
clean tree), so they should still resolve.

---

### CB-21 — Re-anchor audit citations that drifted when `README.md` was rewritten.

**Plain English.** The root README has been rewritten since the audit was written. Several audit
findings still cite line numbers that now point at different text. The findings themselves are
mostly still true — only the addresses are wrong — but an unfixable citation reads as a refuted
finding.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** medium

| Audit location | Cites | Now |
|---|---|---|
| `:237, :393, :403` | "`README.md:92` states the repository is public" | `README.md:92` is the copyright paragraph. No public-status claim remains in the README. The wording migrated to `NOTICE.md:11` — see CB-14. (`:342` is **not** one of these locations; it carries the separate all-rights-reserved finding in the next row.) |
| `:342, :380` | "`README.md:92-94` states an all-rights-reserved position in prose" | Now `README.md:92-96`, and the position also lives in a dedicated `NOTICE.md` that did not exist at audit time. |
| `:237` | "`COPYRIGHT.md` states a licensing position" | No `COPYRIGHT.md` exists. The file is `NOTICE.md`. Substance holds — see CB-13. |
| `:174, :219` | "`README.md:106-107`: 'Nation types are data, not code'" and "`README.md:6` describes the meso tier as weighted cohorts" | `README.md` is 96 lines. The archetype claim is now `README.md:72-74`, reworded; the quoted `(PLAN.pdf §9)` phrasing survives only at `scaffold/README.md:106-107`. The meso description is now `README.md:6-7`. |
| `:84` | "`README.md:25` promises 'Every action creates second- and third-order effects'" | That sentence is not in `README.md` at all. It is at `CHARTER.md:25`. The claim stands; the citation must move. |
| `:158` | "`README.md:19` and `:24` ('accepts, rejects, or scales')" | `README.md:19` is now part of the status blockquote and `:24` is a table header. The engine-validates claim is now `README.md:38`; the "accepts, rejects, or scales" wording survives at `scaffold/README.md:24`. |
| `:158` | `CHARTER.md:113`, listed among the seven places the engine-validates claim appears | **A3 item 4, first half** (`A3-VERIFICATION-RESULTS.md:218-221`). Re-anchor to `CHARTER.md:112` ("then priced, validated and resolved by the engine"), which is the false clause. `:113-114` is the **true** sibling and must not be listed as an untruth — see CB-01's "Do not touch" note. Also add `README.md:38` and `scaffold/README.md:19` to this list as front-door untruths not previously cited. |
| `:168` | "`CHARTER.md:113-114` states the LLM 'never decides whether the composition is legal'" | **A3 item 4, first half**, second target. Same re-anchoring: the sentence quoted here is true; the audit's point about role authority stands, but the citation must move to `CHARTER.md:112` for the false-claim aspect. This location appeared in no earlier draft of this backlog. |
| `:393` | "No checklist exists" (publication readiness gate) | A publication checklist now exists at `HANDOFF.md` § Publication exit criteria (`:92-102`), seven exit criteria. |

**Correction required.** Re-anchor each citation. Where the underlying finding is now satisfied
(the publication checklist), mark it satisfied rather than deleting it.

**Merged from:** ground-truth stale-claim findings; A3 correction 4's re-anchoring instruction
(`A3-VERIFICATION-RESULTS.md:218-221`).

---

### CB-22 — Re-anchor audit citations pointing at the deleted `plan.txt`.

**Plain English.** Several audit findings cite line numbers inside a file that has since been
deleted. The claims may still be true — the same content is thought to be in `PLAN.pdf` — but they
currently point at nothing.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.1 · **Effort:** small

**Affected citations.** `CURRENT-STATE-AUDIT.md:235` and `:291` (both cite `plan.txt:221` for the
DISARM Red Framework correspondence — see CB-24); `:217` (cites `plan.txt:229` for the
4.1-million / 22% population figures — see CB-17); `:292` (cites `plan.txt:138, 168` among the ten
dangling design-doc references — see CB-12, which is why the count is now nine).

**Correction required.** Re-anchor each to the corresponding `docs/PLAN.pdf` section, or mark the
underlying claim as unverifiable pending PDF extraction.

**COULD NOT VERIFY.** `docs/PLAN.pdf` was not text-extracted in this pass. Whether it still contains
the DISARM correspondence sentence, the population figures, or the §2 licence audit is **unknown**
and must not be asserted either way. The one thing that was observed: the raw PDF bytes contain two
DISARM link annotations, to `https://github.com/DISARMFoundation/DISARMframeworks/` and to the
`disarm_red_framework.md` page. The surrounding prose lives in compressed content streams and was
not read.

**Merged from:** ground-truth stale-claim findings against `CURRENT-STATE-AUDIT.md:217, :235, :291,
:292`.

---

### CB-23 — The "no version control" findings are stale. The "no CI" findings are not.

**Plain English.** Several records say the project is not in version control and has no `.git`
directory. That was true when they were written and is now false — the repository is under git,
with one commit and a remote configured. The *other* half of the same sentences, that there is no
continuous integration, is still completely true. Correcting one half without the other would be a
new inaccuracy.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** supports B2 closure; does not itself clear it — **the drafter's classification,
not a source's.** A3 states neither that correcting B2's own stale justification bears on closing B2
nor that it does not. · **P0:** P0.1 · **Effort:** small

| Location | Stale clause | Status |
|---|---|---|
| `A3-VERIFICATION-RESULTS.md:242` (blocker B2) | "There is no CI and no `.git`." | "no CI" **stands**. "no `.git`" is **false**. Restate B2 as a CI-only blocker. |
| `CURRENT-STATE-AUDIT.md:339` (finding 37) | "The repository is not under version control. `git rev-parse` returns 'fatal: not a git repository'. No history, no author, no diff, no remote. The `.gitignore` is therefore inert." | **False in full.** The `.gitignore` is now live: 55 files tracked, clean status. |
| `CURRENT-STATE-AUDIT.md:13` | "there is no CI, and no `.git` directory at all" | Half stale, as B2. |
| `CURRENT-STATE-AUDIT.md:283` (§6.1 item 1) | "No CI configuration exists anywhere; no `.github/`, no workflow, no `.git` directory at all." | First three clauses **stand**. Final clause **false**. |
| `CURRENT-STATE-AUDIT.md:372` (§7) | "Version control \| Missing \| No `.git` anywhere. This blocks branch protection, CODEOWNERS, required checks and secret scanning as a class." | Status **stale**. Those controls are no longer inapplicable as a class. Whether any is configured is unverified — see below. |
| `CURRENT-STATE-AUDIT.md:403` (decision 8.2) | "It is not currently in git at all, so the claim is aspirational." | Both premises **stale** — see also CB-21. |

**Evidence.** Reproducible, read-only:

```
cd C:\Users\daijo\project-meridian
git log --oneline          # 71fa329 Initial commit: MERIDIAN scaffold, charter, and current-state audit
git status --short         # no tracked file modified; untracked working documents present
git branch -a              # * main / remotes/origin/HEAD -> origin/main / remotes/origin/main
git remote -v              # origin  https://github.com/CypherTechAries/project-meridian.git (fetch/push)
git ls-files | wc -l       # 55  (tracked files)
ls -a .github              # No such file or directory
```

Commit `71fa329`, authored by Aries Russell, Sat 18 Jul 2026 22:41:55 +0100.

**Note on "clean".** `git status --short` is **not** empty. It lists untracked entries under
`docs/delivery/` (including this record), plus `docs/design/`, `docs/safety/` and
`docs/world-model/`. The claim that holds is narrower: no *tracked* file is modified relative to
`71fa329`. Consequently two counts diverge and must not be used interchangeably — 55 is
`git ls-files | wc -l` (tracked), while a plain `find . -type f -not -path "./.git/*" | wc -l`
returns 71 at the time of writing. The difference is entirely untracked working documents.

**Correction required.** Amend each row so the version-control clause reflects the current state and
the CI clause is preserved intact. Update the §7 deliverable table: Version control moves from
Missing to Present; CI pipeline stays Missing; the GitHub-level controls move from "inapplicable" to
"applicable, status unverified".

**COULD NOT VERIFY.** No network or `gh` command was run, per the standing constraints. Therefore:
whether the remote repository is actually **private** is unverified and rests solely on the
assertion at `HANDOFF.md:13`; whether branch protection, CODEOWNERS, required status checks or
secret scanning are configured is **unknown** (there is no `CODEOWNERS` file in the local tree);
and whether commit `71fa329` has actually reached the server is **unknown** — the local tracking ref
is consistent with a completed push, but no fetch was performed, so this reflects last-known local
state, not the server.

**Merged from:** ground-truth findings verified directly for this record; blocker B2's justification
(`A3-VERIFICATION-RESULTS.md:242`); audit `:13, :283, :339, :372, :403`.

---

### CB-24 — The DISARM Red Framework claim is now unanchored.

**Plain English.** The audit records a claim that the campaign schema maps almost one-to-one onto a
published influence-operations framework. That claim was cited to a file that has since been
deleted, and the word "DISARM" now appears nowhere in the code, schemas, scenarios or markdown. The
claim matters because it is part of the dual-use argument in B5.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — (bears on B5 context) · **P0:** P0.1 · **Effort:** trivial

**Location.** `CURRENT-STATE-AUDIT.md:291` (§6.1 item 9), citing `plan.txt:221`; the same
correspondence is invoked in decision 6 at `:411`.

**Evidence.** `grep -rn "DISARM" --include=*.md --include=*.txt --include=*.py --include=*.json .`
returns four hits, all inside `CURRENT-STATE-AUDIT.md` itself (`:13, :235, :291, :411`). Zero hits
in any code, schema or scenario. No phase, tactic or technique field exists on `Campaign`.

**Correction required.** Re-anchor or withdraw the citation, and state plainly that no DISARM
vocabulary is adopted anywhere in the codebase.

**COULD NOT VERIFY.** Whether `docs/PLAN.pdf` still makes the correspondence claim in prose is
**unknown** — see CB-22. Two DISARM link annotations are present in the raw PDF bytes; the sentence
around them was not extracted. Do not assert either that the plan still makes the claim or that it
does not.

**Merged from:** audit §6.1 item 9 (`CURRENT-STATE-AUDIT.md:291`); audit §5.12 (`:235`); audit
decision 6 (`:411`); ground-truth stale-claim finding.

---

## P0.2 — Restore reproducible installation

### CB-25 — The documented install is broken by a package no code imports.

**Plain English.** Following the README's installation instructions fails, and the package that
breaks it — `litellm` — is a package nothing in the project imports. A second package,
`python-socketio`, is also never imported and also ships in the Docker image, but nothing in the
sources attributes any part of the install failure to it. The two share the property of being
unimported; they do not share the property of being install-blocking, and this entry keeps them
separate.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.2 · **Effort:** small · **carries an open question**

**Locations.** `scaffold/backend/requirements.txt:20` (`litellm>=1.34,<2.0`);
`scaffold/backend/requirements.txt:12` (`python-socketio>=5.11,<6.0`);
`scaffold/backend/Dockerfile:11`; documented install paths at `scaffold/README.md:58, :69` and
`scaffold/CLAUDE.md:32-42`.

**Evidence.** An AST parse of every `.py` file under `scaffold/` scanned 78 import statements and
found zero importing `litellm`. The only `import litellm` text in the tree sits inside the
`llm_gateway.py` module docstring, which spans lines 1-29 (the sketch is at `:17`); the module's
real imports begin at `:31`.

`python-socketio` is likewise **never imported** — but it does not have "zero occurrences outside
`requirements.txt`". `cd scaffold && grep -rn "socketio" .` returns three lines: the declaration at
`backend/requirements.txt:12`, a prose comment at `backend/app/api/routes_ws.py:5`
("python-socketio is already in requirements"), and ADR-005 at `docs/ARCHITECTURE_DECISIONS.md:46`.
The zero-occurrences phrasing is inherited from audit item 41 (`CURRENT-STATE-AUDIT.md:343`), where
it plainly means zero *import* occurrences; restated unqualified it is false, and this record does
not restate it.

**Correction required.** Remove `litellm` from the default install or make it an optional extra.
Then re-run the documented install end to end and record the command and the date it last
succeeded, per the Phase 1 exit criterion at `CURRENT-STATE-AUDIT.md:445`. `python-socketio` is
**not** included in this instruction — see the open question below.

**OPEN QUESTION for the owner — drop `python-socketio` or keep it?** No source instructs its
removal. Audit item 41 (`:343`) only *observes* that it is unimported; the package it names as
breaking the install is `litellm` alone, as does `HANDOFF.md:45-48`. The publication exit criterion
is scoped to "unused **installation-blocking** dependencies" (`HANDOFF.md` § Publication exit criteria (`:100`)), and
`python-socketio` is nowhere recorded as install-blocking. Against removal, ADR-005
(`scaffold/docs/ARCHITECTURE_DECISIONS.md:43-48`, **Status: Accepted**) retains it deliberately:
"`python-socketio` is already a dependency so a full build can move to rooms/namespaces for
multi-player shared runs without changing the engine." Removing it would therefore falsify a live
accepted ADR, and ADR-005:46 would need a corresponding edit. Keep the forward-looking dependency,
or drop it and supersede ADR-005? That is an architecture decision for the owner, and this record
does not make it.

**COULD NOT VERIFY.** The failure mode itself was **not** reproduced in this pass — no environment
was created and nothing was installed. `HANDOFF.md:45-48` reports that `litellm` resolves to 1.92.0,
has no cp313 wheel, falls back to sdist and requires a Rust toolchain, and that pip's
resolve-before-install behaviour means nothing installs at all. That is second-hand here. Whether
the Docker build fails on Linux/Python 3.11 for the same reason is recorded as **Unknown** at
`CURRENT-STATE-AUDIT.md:271` and remains unknown.

**Merged from:** audit §5.15 (`CURRENT-STATE-AUDIT.md:271`); audit §6.5 item 41 (`:343`);
`HANDOFF.md:45-48`; publication exit criterion "Unused installation-blocking dependencies removed or
made optional" (`HANDOFF.md` § Publication exit criteria (`:100`)).

---

### CB-26 — No pins, no lockfile, no machine-readable Python version.

**Plain English.** Every dependency is declared as an open-ended range, one with no upper bound at
all. There is no lockfile and no hashes, so an install today and an install in six months can
produce different software, and nothing records which set produced a given run. The supported Python
version exists only in prose and in the Docker base image.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.2 · **Effort:** medium · **blocked on decision 8.5**

**Evidence.** `scaffold/backend/requirements.txt` declares 13 packages, all as ranges
(`grep -c -E '^[^#[:space:]]' scaffold/backend/requirements.txt` → `13`, in a 24-line file; an
earlier draft of this entry said 12). Not one exact
pin, no hashes; `websockets>=12.0` has no upper bound. There is no `pyproject.toml`, no lockfile of
any kind, no `setup.cfg`, no `tox.ini`, no `.python-version` anywhere in the tree. The Python target
appears only at `scaffold/backend/Dockerfile:1` (`FROM python:3.11-slim`),
`scaffold/docs/ARCHITECTURE_DECISIONS.md:11` and `scaffold/CLAUDE.md:44` — all prose or image
pinning, no `requires-python`. Note that the A3 verification work ran on CPython 3.13.9
(`A3-VERIFICATION-RESULTS.md:27`), two minor versions above what the image pins.

**Correction required.** Add a hash-pinned lockfile and install from it in the Dockerfile; add
`requires-python`; cap `websockets`. Then update the four documented workflows the change touches:
`README.md:56-57`, `scaffold/README.md:58, 69-70`, `scaffold/CLAUDE.md:33`, and the Dockerfile.

**OPEN QUESTION for the owner — audit decision 8.5, still open.** Adopt `uv` and `pyproject.toml`,
or stay on `requirements.txt` with `pip-compile`? `HANDOFF.md` contains no occurrence of "uv" or
"pyproject"; P0.2 commits only to the outcome and leaves the tool unchosen. The audit's own note is
that this is "a deliberate migration, not a fix to slip in"
(`CURRENT-STATE-AUDIT.md:409`). Not resolved here.

**COULD NOT VERIFY.** No dependency was installed, so no concrete resolved version can be stated for
any package, and whether the thirteen declared ranges resolve cleanly together at all is **unknown**.

**Merged from:** audit §6.5 item 36 (`CURRENT-STATE-AUDIT.md:338`); audit §7 dependency-management
row (`:376`); audit decision 5 (`:409`); audit §9 Phase 1 work (`:441`); `HANDOFF.md:72-73`.

---

## P0.3 — Establish real CI

### CB-27 — No CI exists. Build one that runs only checks that genuinely pass.

**Plain English.** There is no automated checking of any kind. Building it is the alternative route
to closing blocker B2 — either delete the claim that CI guards the determinism boundary (CB-03), or
make the claim true.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** alternative route to B2 · **P0:** P0.3 · **Effort:** medium

**Evidence.** No CI artefact of any kind exists: no `.github/` directory, no workflow file, no
`.gitlab-ci.yml`, no `Jenkinsfile`, no `.circleci/`. The only YAML in the project is
`scaffold/docker-compose.yml`. `.gitignore:16-18` pre-ignores `.pytest_cache/`, `.mypy_cache/` and
`.ruff_cache/` — anticipating tooling that is not present: there is no ruff config, no mypy config,
no `setup.cfg`. (File counts, since two circulate: 55 tracked per `git ls-files`; 71 total in the
tree excluding `.git/` at the time of writing, the difference being untracked working documents.
Neither listing contains a CI artefact.)

**Correction required.** Per `HANDOFF.md:74`: only checks that genuinely exist and pass. The audit's
Phase 1 exit criteria (`CURRENT-STATE-AUDIT.md:446`) ask for CI green on a trivial PR and
demonstrably red when the determinism test is deliberately broken.

**COULD NOT VERIFY — the suite was not run.** No code was executed in this pass, so whether the five
existing tests currently pass is **unknown**. "Runs only checks that genuinely pass" is therefore an
instruction resting on an unconfirmed premise: establish that `python -m pytest tests -v` succeeds
in a clean environment (which itself depends on CB-25) before wiring anything into CI. Note also
that the "demonstrably red when the determinism test is deliberately broken" criterion interacts
with CB-03's second half: `test_llm_gateway_cannot_write_state` is an attribute-presence check, so
CI passing it does not demonstrate that the determinism boundary is guarded.

**Sequencing note — drafter's judgement, not a source instruction.** This record's view is that
CB-03 (delete "in CI") should not wait for this work: if CI is built later the charter sentence can
be reinstated accurately, whereas leaving a false claim standing meanwhile is the defect Phase 0
exists to remove. A3 offers the two routes without preference and no source sequences them. The
owner may sequence otherwise.

**Merged from:** audit §6.5 item 38 (`CURRENT-STATE-AUDIT.md:340`); audit §7 CI-pipeline and
lint/typecheck rows (`:373-374`); audit §9 Phase 1 work (`:441`); blocker B2's second clearing route
(`A3-VERIFICATION-RESULTS.md:242`); `HANDOFF.md:74`.

---

## P0.4 to P0.7 — Engineering foundations

These four are carried at their `HANDOFF.md` headings so the priority order stays visible and
nothing appears dropped. They change simulation behaviour and are therefore outside the remit of
this documentation phase. **None is decomposed into work items here, and none should be started
before the P0.1 corrections land** — `HANDOFF.md` § Backlog (`:109`) is explicit that the foundation must be honest
and testable first.

**P0.4A is the exception, and it is a deliberate one.** The founder decision of 18 July 2026 creates
a fifth engineering workstream between P0.4 and P0.5 and states its scope and exit criteria
directly, so it is decomposed below where CB-28 to CB-31 are not. Decomposing it does not authorise
starting it: the same "P0.1 corrections land first" constraint applies, and nothing in CB-34 to
CB-39 is approved.

### CB-28 — Define the authoritative-state contract across macro, meso and micro.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.4 · **Effort:** large

Plain English: write down exactly what counts as the simulation's official state, at all three
tiers, before anything else is built on top of it. Today the answer is uneven: macro state is a
single mutable object, meso state comes down to the one belief field that any code actually writes,
and there is no micro state at all — no field of the micro-agent specification is ever written by
any code path.

Evidence for those three statements. **Macro:** one mutable `MacroState` held at
`scaffold/backend/app/simulation/agents/macro_state.py:21`
(`self.state: MacroState = initial`), constructed once at model init
(`scaffold/backend/app/simulation/engine.py:91-93`) and mutated in place; history exists only as
`model_dump()` dicts appended to `self.snapshots` (`engine.py:116, :180`). **Meso:** the only cohort
field written anywhere is `beliefs.government_competence`, decremented at
`scaffold/backend/app/simulation/agents/cohort_agent.py:35-38`; the other four belief fields
declared at `scaffold/backend/app/simulation/schemas/agent_schema.py:56-69` are written by nothing
and read by nothing. **Micro:** `InstitutionalAgent` writes only `self.last_proposal`
(`scaffold/backend/app/simulation/agents/institutional_agent.py:24, :38`), overwritten each tick; no
field of the `MicroAgent` spec at `agent_schema.py:154-184` — beliefs, resources, political capital,
memory, relationships — is assigned by any code path. All three rest on source reading and
absence-of-call-sites, not on execution.

**Merged from:** `HANDOFF.md:75`.

---

## P0.4A — Establish deterministic randomness architecture

**Source: founder decision, 18 July 2026.** This workstream did not exist when `HANDOFF.md` § Phase 0 priority order (`:70-90`)
was written and does not appear there. It sits between P0.4 and P0.5 in the founder-set order:

> P0.4 define authoritative state → **P0.4A establish deterministic randomness architecture** →
> P0.5 implement cross-tier causal channels → P0.6 repair events, snapshots and replay.

**Why it is its own workstream and not a detail of something else.** The founder decision is
explicit that RNG isolation is neither a sub-task of the world model nor a sub-task of replay, and
must not be filed inside either. The governing statement of the problem, quoted from the decision:

> "Materialising a background citizen must not change tomorrow's weather, market behaviour,
> government approval or another person's decision merely because it consumed extra draws."

**Sequencing, as the decision states it.** P0.5 *specification* may proceed in parallel now, before
P0.4A is implemented. **P0.5 implementation, entity promotion and world-model materialisation may
not proceed until P0.4A passes.** Recorded here as a constraint on later work; nothing in this
backlog authorises starting any of it.

**Scope — five isolation axes, all of them required.** Deterministic randomness must be isolated by
subsystem; by entity; by relationship or interaction; by simulation purpose; and by tick or event
context where appropriate. The decision states directly that **per-entity streams alone are
insufficient**.

**What exists today.** One `random.Random`, constructed once at
`scaffold/backend/app/simulation/engine.py:83`
(`self.rng = random.Random(resolved_seed)  # the ONLY source of engine randomness`) and drawn from
at three sites: `engine.py:135` (macro noise), `cohort_agent.py:36`
(`self.model.rng.uniform(0.0, 0.005)`) and `diffusion.py:75` (adoption jitter), the last reached by
passing `self.rng` itself into `linear_threshold_step` (`diffusion.py:40-46`) at `engine.py:144`,
from inside `MeridianModel._step_diffusion` (`engine.py:138-145`). There are no named substreams —
audit item 28, `CURRENT-STATE-AUDIT.md:320`. This is not an accident of implementation: it is the
architecture `ADR-007` specifies and accepts, which is why CB-34 exists.

**The ten exit criteria and where each is carried.** The decision states all ten; the mapping to
entries is the drafter's decomposition. Every criterion is stated so it is testable, and each is
carried by exactly one entry so none can be assumed handled twice or dropped between two.

| # | Exit criterion (founder decision, 18 July 2026) | Carried by |
|---|---|---|
| 1 | No authoritative code calls the global `random` API directly. | CB-36 |
| 2 | No subsystem receives unrestricted access to the root generator. | CB-36 |
| 3 | Stream keys use stable identifiers — **not** Python's process-randomised `hash()`. | CB-35 |
| 4 | The run records the RNG algorithm and version. | CB-37 |
| 5 | Adding an unrelated entity does not alter unrelated subsystem results. | CB-39 |
| 6 | Promoting one background person does not alter previously established entities. | CB-39 |
| 7 | Reordering entity iteration does not alter outcomes where the model declares order irrelevant. | CB-39 (test); CB-35 (the declaration itself, which does not exist today) |
| 8 | Repeating the same promotion event produces the same profile and history. | CB-39 |
| 9 | Every random outcome can be associated with a subsystem, entity or interaction, and a purpose. | CB-38 |
| 10 | Tests deliberately inject extra draws into one stream and verify other streams remain unchanged. | CB-39 |

**Nothing in this workstream is implemented, and no part of it is approved.** Every entry below
describes work to be done, not behaviour that exists.

---

### CB-34 — Choose the randomness architecture deliberately, in an ADR that supersedes ADR-007.

**Plain English.** The project needs to pick how random numbers are organised, and write down why.
There are at least two respectable ways to do it and they have different costs, so the choice has to
be made on purpose rather than arrived at. The decision also has to say plainly what is being ruled
out: drawing from one shared generator in call order, which is what the code does today and what an
accepted architecture decision currently blesses.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.4A · **Effort:** large (design work, then an ADR)

**What the founder decision requires.** An ADR is required because at least two valid approaches
exist: **stateful named substreams**, or **keyed / counter-based deterministic draws**. The ADR must
select one deliberately, and must **explicitly reject ordinary sequential calls to a single shared
PRNG for authoritative behaviour**.

**Evidence — the rejected approach is currently the accepted one.**
`scaffold/docs/ARCHITECTURE_DECISIONS.md:60-66` is `ADR-007 — Reproducibility: one seed, threaded
everywhere`, **Status: Accepted**, and it states: "Every run has a `seed`, threaded into
`MeridianModel.__init__` → `self.rng` (`random.Random`). All engine, agent, and diffusion randomness
draws from that one RNG — never the global `random` or unseeded `numpy`." That is precisely the
single-shared-PRNG design the founder decision rules out for authoritative behaviour. A new ADR
cannot sit alongside it; it must supersede it, and ADR-007's status must change accordingly.

**Second, separate defect in ADR-007 — do not fix it here.** The same ADR claims the property is
"proven by `test_same_seed_is_deterministic`". CB-39 records why that test does not prove isolation.
The wording correction is a P0.1 documentary item and is **not** carried by any entry in this
backlog today — see the note in CB-39 and the "Known gaps" section.

**Use the ADR template.** `docs/delivery/ADR-TEMPLATE.md` exists for this purpose. Whether the ADR
is filed in `docs/delivery/`, in the project ADR log at
`scaffold/docs/ARCHITECTURE_DECISIONS.md`, or in both, is not settled by any source read for this
record.

**A draft exists as of 19 July 2026 — this entry is not closed by it.**
[`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
names both candidate approaches, recommends keyed / counter-based deterministic draws, and states
the explicit rejection of sequential shared-PRNG use for authoritative behaviour. **Status:
Proposed; drafted by an AI agent; Approval block empty; no authority.** It was filed at `docs/adr/`
and itself records that home as an open question for the owner. Two of this entry's four closing
conditions therefore remain unmet: owner approval, and the ADR-007 disposition — ADR-010 records
"Supersedes: None" and would narrow ADR-007 rather than supersede it, which contradicts the
paragraph above. That contradiction is an owner question (`PUBLICATION-EXIT-CRITERIA.md` open
question 15; `RAID-REGISTER.md` DEC8) and is deliberately left open here.

**Evidence requirement for closing this entry.** An ADR exists that names both candidate approaches,
records the selection with its reasoning, states the explicit rejection of sequential shared-PRNG
draws for authoritative behaviour, supersedes ADR-007, and is approved by the owner. **An AI agent
may draft it and may not approve it.**

**Merged from:** founder decision of 18 July 2026 (ADR requirement); audit §6.28
(`CURRENT-STATE-AUDIT.md:320`); `ADR-007` (`scaffold/docs/ARCHITECTURE_DECISIONS.md:60-66`).

---

### CB-35 — Define the stream key space across all five isolation axes, on stable identifiers.

**Plain English.** Once the approach is chosen, something has to say what a stream is *named after*.
The founder decision requires that randomness be separable by subsystem, by entity, by relationship
or interaction, by what the draw is *for*, and by when it happens. It also rules out one specific
convenient shortcut: Python's built-in `hash()`, which returns different values in different
processes and would make runs irreproducible across machines.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.4A · **Effort:** large

**What the key space must separate** — all five, per the decision, with per-entity streams stated to
be insufficient on their own:

| Axis | Meaning |
|---|---|
| Subsystem | macro drift, cohort belief drift, diffusion, and whatever replaces them |
| Entity | the specific person, organisation, cohort or institution the draw concerns |
| Relationship or interaction | a draw about the pair or the exchange, not about either party alone |
| Simulation purpose | what the draw is *for*, so two purposes touching one entity do not share a stream |
| Tick or event context | where appropriate — the decision qualifies this axis and does not make it unconditional |

**Evidence — nothing of this kind exists today.** There is no stream, key, substream or namespace
concept anywhere in the simulation package; there is one generator and three call sites (see the
section preamble). Audit item 28 records the absence directly (`CURRENT-STATE-AUDIT.md:320`).

**Evidence — the `hash()` constraint is forward-looking, not a repair.** `hash(` does not occur in
any `.py` file under `scaffold/` (verified by grep over the tree for this amendment). Criterion 3 is
therefore a constraint on a scheme that does not yet exist, not a correction to existing code. It is
still load-bearing: `CURRENT-STATE-AUDIT.md:39` records that current reproducibility "holds across
separate processes under differing `PYTHONHASHSEED`", and a `hash()`-keyed scheme would forfeit that
property.

**Also carries criterion 7's missing half.** Criterion 7 requires that reordering entity iteration
not change outcomes "where the model declares order irrelevant". **No such declaration exists
anywhere.** Iteration is plain-list and fixed at `engine.py:152` and `:159` (both with explicit
comments, per `CURRENT-STATE-AUDIT.md:405`), which makes order *stable* but never states where order
is *permitted* to be irrelevant. The key-space work must produce that declaration, or criterion 7's
test in CB-39 has no specification to test against.

**Evidence requirement for closing this entry.** A written key-space specification covering all five
axes; a stated rule that keys derive from stable identifiers with `hash()` named as excluded; and
the order-relevance declaration criterion 7 depends on. Design artefact, not code.

**Merged from:** founder decision of 18 July 2026, scope statement and exit criteria 3 and 7 (part);
audit §6.28 (`CURRENT-STATE-AUDIT.md:320`); audit `:39`; audit decision 3 (`:405`).

---

### CB-36 — Close the two access routes: no global `random` API, no unrestricted root generator.

**Plain English.** Two rules about who is allowed to draw random numbers. The first — never call
Python's global random functions in authoritative code — the codebase appears to follow already, but
follows by convention with nothing enforcing it. The second — no subsystem gets a free hand on the
root generator — the codebase currently breaks in two places.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.4A · **Effort:** medium

**Criterion 1 — apparently already satisfied, and unenforced.** `CURRENT-STATE-AUDIT.md:39` records
that the single seeded generator at `engine.py:83` "is the only generator drawn from anywhere in the
simulation package; there is no global `random`, no unseeded numpy, and no time-based value". The
`import random` statements at `engine.py:15` and `diffusion.py:13` are for the `random.Random`
constructor and type annotation (`diffusion.py:44`), not for module-level draws. So the work here is
**not** repairing a current violation: it is turning a convention into something checkable, since
nothing today would catch a reintroduction. Note that `diffusion.py:57` already states the rule in a
docstring — "Seeded RNG owned by the model (do not use the global `random`)" — which is a comment,
not an enforcement mechanism.

**Criterion 2 — currently violated, in two identified places.** Both subsystems that draw outside
the engine receive the root generator itself, with unrestricted access to it:

| Site | What it receives |
|---|---|
| `scaffold/backend/app/simulation/agents/cohort_agent.py:36` | reaches back through `self.model.rng` and draws directly from the root generator |
| `scaffold/backend/app/simulation/engine.py:144` → `diffusion.py:44, :75` | the root generator is passed into `linear_threshold_step` as the `rng` parameter and drawn from there |

**Related hazard, recorded not resolved.** Audit item 27 (`CURRENT-STATE-AUDIT.md:319`) records that
Mesa's `seed=` kwarg to `super().__init__` is inert and that on the API path Mesa's `self.random` is
seeded **from entropy** — a second, non-reproducible generator reachable as `self.model.random`, one
character away from `self.model.rng`. The audit calls it harmless today because nothing reads it.
Under criterion 2 it is an unrestricted generator inside the model object, so P0.4A must decide
whether it is removed, sealed or documented. This interacts with **audit decision 8.3** (whether
Mesa remains the substrate), which is open — see the closing note in "Open questions for the owner".

**Evidence requirement for closing this entry.** An automated check — not a code review and not a
docstring — that fails when authoritative code calls the global `random` API, and fails when a
subsystem is handed the root generator. `CURRENT-STATE-AUDIT.md:453` already proposes an AST import
check for the adjacent LLM-boundary problem; the same technique applies. Recording *how* the check
runs depends on CB-27 (there is no CI to run it in).

**Merged from:** founder decision of 18 July 2026, exit criteria 1 and 2; audit `:39`; audit §6.27
(`:319`); audit `:453`.

---

### CB-37 — Record the RNG algorithm and version with the run.

**Plain English.** A run currently records the seed it was given and nothing about the generator
that consumed it. A seed alone does not reproduce a run: the same seed through a different generator,
or a different version of the same generator, produces different numbers. Whichever architecture
CB-34 selects, the run has to say which one it used.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.4A · **Effort:** small

**Evidence.** `MacroState` records `seed` (`scaffold/backend/app/simulation/schemas/macro_schema.py:82`)
and a free-text `derivation` string defaulting to `"rules_engine_v1"` (`:85-88`, set to
`"rules_engine_v1 + seed_init"` at `engine.py:68`). Neither names a generator or a version. The
persistence schema is the same: `scaffold/backend/app/db/models.py:24, :30` pins reproducibility on
"`seed` + `scenario_id`". Audit `:387` records "no RNG state in the snapshot shape", and no
`getstate` or `setstate` call exists anywhere under `scaffold/` (verified by grep for this
amendment), so a snapshot cannot currently carry generator state either.

**Scope boundary — deliberate.** This entry covers recording the algorithm **identity and version**,
which is criterion 4. It does **not** cover capturing and restoring generator *state* into snapshots
for fork or replay: that is CB-30 (P0.6), and `CURRENT-STATE-AUDIT.md:259` and `:465` are its
sources. Keeping the two apart is the point of the founder decision's instruction that randomness
must not be filed inside replay.

**Evidence requirement for closing this entry.** A run record that names the generator algorithm and
its version, populated from the implementation rather than typed in as a literal, and a test that
fails if the two disagree.

**Merged from:** founder decision of 18 July 2026, exit criterion 4; audit §7 persistence row
(`CURRENT-STATE-AUDIT.md:387`).

---

### CB-38 — Make every random outcome attributable to a subsystem, entity or interaction, and a purpose.

**Plain English.** At the moment a random number is drawn, used and forgotten. Nothing records which
part of the simulation drew it, on whose behalf, or what it was for. Without that, no one can answer
why two runs differ, which is the question the whole workstream exists to make answerable.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.4A · **Effort:** medium

**Evidence.** Audit item 17, `CURRENT-STATE-AUDIT.md:304`: "No random draw is ever recorded —
Stream, index, distribution, parameters and value are all discarded at `engine.py:135`,
`diffusion.py:75`, `cohort_agent.py:36`." Those are the same three draw sites listed in the section
preamble; there is no fourth.

**Note on what "associated" requires — drafter's reading, flagged as such.** Criterion 9 says every
random outcome "can be associated with" a subsystem, entity or interaction, and a purpose. This
record reads that as satisfiable by a **structural** property — the draw is made through a keyed
interface that carries those attributes — and as **not** necessarily requiring a persisted per-draw
log. A per-draw log is one way to demonstrate it and is the heavier one. The founder decision does
not say which, and this record does not choose. Whoever executes should settle it in CB-34's ADR
rather than by implementation habit, because the two readings differ substantially in cost and in
what they make possible for CB-30.

**Dependency.** This entry cannot be specified before CB-35, since the attributes it attaches are the
key-space axes CB-35 defines.

**Evidence requirement for closing this entry.** For any draw the simulation makes, the subsystem,
the entity or interaction, and the purpose are recoverable — demonstrated on all draw sites then
existing, not only the three that exist today.

**Merged from:** founder decision of 18 July 2026, exit criterion 9; audit §6.17
(`CURRENT-STATE-AUDIT.md:304`).

---

### CB-39 — The existing determinism test is insufficient. Build isolation tests. **CARRIES AN OPEN QUESTION.**

**Plain English.** There is a test that runs the model twice with the same seed and checks the
numbers match. It is a real test and it passes for real reasons, but it cannot detect the problem
this workstream exists to fix. If a change somewhere causes an unrelated subsystem's numbers to
move, the test either does not look at those numbers or reads the movement as ordinary divergence.
The founder decision is explicit that P0.4A requires **isolation tests, not merely same-seed
repetition tests**.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.4A · **Effort:** large · **carries an open question**

**The existing test.** `scaffold/backend/tests/test_engine.py:34-40`,
`test_same_seed_is_deterministic`: constructs two `MeridianModel`s at seed 88213, runs both 20
ticks, asserts `a.macro_snapshot() == b.macro_snapshot()`. Its module docstring (`:3-6`) claims it
"proves the determinism boundary". Note the assertion compares **macro state only** — meso output is
not compared at all.

**Why it is insufficient — the demonstration already exists.** `A3-VERIFICATION-RESULTS.md` §6 shows
that adding a grievance to a cohort that had none changes the number of draws consumed per tick,
which shifts every later draw in the shared stream, which moves macro output:

```
shipping_throughput_pct_of_baseline: 0.6080711379477878 -> 0.5973599412373322
```

Changing cohort *values* by two orders of magnitude changes macro by exactly nothing. So the
apparent meso→macro influence is draw-order contamination, not causality. A3 records the consequence
in terms: "the existing determinism test would mask such a change as 'expected divergence'". That is
the evidence base the founder decision's critical note points at.

**The five test criteria this entry carries.** Each is a discrete test, not a restatement of one
test:

| # | Test to build | Status of what it tests |
|---|---|---|
| 5 | Adding an unrelated entity does not alter unrelated subsystem results | Currently **would fail** — this is exactly what A3 §6 demonstrates |
| 6 | Promoting one background person does not alter previously established entities | **Not testable today** — see the open question |
| 7 | Reordering entity iteration does not alter outcomes where the model declares order irrelevant | Blocked on CB-35: no order-relevance declaration exists to test against |
| 8 | Repeating the same promotion event produces the same profile and history | **Not testable today** — see the open question |
| 10 | Deliberately inject extra draws into one stream; verify other streams are unchanged | The direct isolation test; nothing of the kind exists |

**Disposition of the existing test — supplement, and correct its claims.** Nothing above argues for
deleting `test_same_seed_is_deterministic`. Same-seed repetition is a necessary property and the
test checks it. What must change is that it stops being cited as proof of a property it does not
establish. Two live claims rest on it and **neither has an entry in this backlog**:
`ADR-007` (`scaffold/docs/ARCHITECTURE_DECISIONS.md:65-66`, "proven by
`test_same_seed_is_deterministic`") and `README.md:61-63` ("the test suite is the point:
`test_same_seed_is_deterministic` proves reproducibility"). Both are P0.1 documentary corrections;
`README.md:61-63` is already named as a known gap in the plain-English summary above, and ADR-007 is
named in CB-34. Recorded here so the omission is visible rather than implied.

**An unresolved contradiction in the sources — do not rely on either side.**
`CURRENT-STATE-AUDIT.md:39` states that the test "does catch the two regression modes `CLAUDE.md`
names: injecting unseeded global randomness or a time-based value both make it fail", and `:527`
makes the same claim as a Phase 1 checklist item specifically about injection into
`CohortAgent.step`. But `CURRENT-STATE-AUDIT.md:140` records the opposite result for that same
injection: "patching `CohortAgent.step` to draw from global `random` instead of `self.model.rng`
leaves macro equality True while cohort beliefs diverge", and the test asserts on macro only. **This
record does not resolve which is correct** — no code was executed for this amendment. Both readings
are recorded so that P0.4A establishes the answer by running it rather than inheriting a claim. It
does not change this entry's conclusion, which rests on A3 §6, not on either of these lines.

**OPEN QUESTION for the owner — criteria 6 and 8 describe work the sequencing forbids.** Criterion 6
("promoting one background person does not alter previously established entities") and criterion 8
("repeating the same promotion event produces the same profile and history") are both stated in
terms of **entity promotion**, which does not exist and which the same founder decision says may not
proceed until P0.4A passes. Taken literally, P0.4A cannot exit until two criteria are met that
cannot be exercised until P0.4A has exited. Two readings are available and this record does not
choose between them:

1. **Build a minimal promotion harness inside P0.4A**, existing only as test scaffolding, so the two
   criteria are exercised against a stand-in rather than the real world-model implementation.
2. **Carry criteria 6 and 8 forward as a gate on entity promotion itself**, so P0.4A exits on the
   other eight and these two are verified at the point promotion is built.

Reading 1 keeps P0.4A's exit self-contained but builds promotion machinery earlier than the founder
sequencing envisages. Reading 2 respects the sequencing but means P0.4A "passes" without two of its
ten stated criteria having been demonstrated, which weakens the gate the decision creates. **This is
an owner decision. An AI agent must not resolve it, and no executing agent should assume either
reading.**

**Evidence requirement for closing this entry.** Each of the five criteria above exists as a named,
runnable test whose failure mode is demonstrated — the test is shown red against the current
shared-stream behaviour before it is shown green against the new architecture. A test that has only
ever been green proves nothing here, which is the specific defect this entry exists to correct.

**Merged from:** founder decision of 18 July 2026, exit criteria 5, 6, 7, 8 and 10, and its critical
note that the current determinism test is insufficient; `A3-VERIFICATION-RESULTS.md` §6; audit `:39`,
`:140`, `:527`.

---

## P0.5 to P0.7 — Engineering foundations, continued

The three entries below are carried at their `HANDOFF.md` headings under the terms stated in the
P0.4 to P0.7 preamble above. None is decomposed here.

### CB-29 — Design explicit cross-tier causal channels.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.5 · **Effort:** large

Plain English: the three tiers do not actually influence one another. Where they appear to, the
apparent link is an artefact of a single shared random-number stream, not a modelled cause. This is
one of the two critical findings and, per `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`), arguably the highest-value item in
Phase 0, because it is the product's core mechanism rather than a tidiness fix. `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84`)
requires that `represents_population` must affect aggregation, which creates a dependency on CB-17's
data correction.

**Re-filed by the founder decision of 18 July 2026 — the shared-RNG half of this entry is no longer
carried here.** Fixing the randomness architecture is **P0.4A** (CB-34 to CB-39), not part of P0.5.
What remains with this entry is the causal-channel design itself: building real macro↔meso↔micro
channels where today there are none. The distinction matters because the two are separable defects
that were previously described in one breath — removing the spurious coupling does not create a real
one, and creating a real one does not remove the spurious one.

**Sequencing — stated by the founder decision, not the drafter.** P0.5 **specification** may proceed
in parallel now, before P0.4A is implemented. **P0.5 implementation may not proceed until P0.4A
passes.** This is a source instruction and is not a judgement of this record. (The separate CB-17
sequencing preference below remains the drafter's.)

**Sequencing — drafter's judgement, not a source instruction.** This record's view is that CB-17
should land first, while that data fix is still behaviour-neutral. No source sequences the two. The
owner may sequence otherwise. **Merged from:** `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`); audit §4.1; A3 check 6
(`A3-VERIFICATION-RESULTS.md:142-175`); founder decision of 18 July 2026 (sequencing, and the
re-filing of the RNG defect to P0.4A).

### CB-30 — Repair event, snapshot and replay foundations.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.6 · **Effort:** large

Plain English: a central transition mechanism, full snapshots, and a replay that makes zero model or
network calls. This is where the *target* reproducibility contract becomes deliverable. Until then
the contract at `HANDOFF.md:61-62` must always be labelled a target and never described as a
delivered capability. Note that CB-04 (persistence claims) is the *documentary* half of this and is
in P0.1 — it must not wait for this work.

**Randomness isolation is not part of this entry, and the founder decision of 18 July 2026 is
explicit that it must not be hidden inside replay.** It is P0.4A (CB-34 to CB-39) and it sequences
*before* P0.5, not with P0.6. The boundary between the two: **naming** the generator algorithm and
version on a run is criterion 4 and belongs to CB-37; **capturing and restoring generator state**
into a snapshot so a fork or replay resumes correctly belongs here, and its evidence is
`CURRENT-STATE-AUDIT.md:259` (the snapshot payload carries no RNG state, so a fork built as ADR-003
specifies would resume the generator at position 0 and diverge silently from its parent) and `:465`.
P0.4A does not deliver that, and this entry must not be treated as delivering P0.4A.

**Merged from:** `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`); audit decision 4
option (b) (`CURRENT-STATE-AUDIT.md:407`); founder decision of 18 July 2026 (the boundary between
P0.4A and P0.6).

### CB-31 — Define simulation time and horizon before touching saturation.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** P0.7 · **Effort:** large

Plain English: indicators run to their maximum and stay there, because the engine has no cost,
cooldown, decay or opposing pressure of any kind. A3 escalated this from a calibration problem to an
architectural gap: there is no mechanism to tune. `HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`) is explicit that it must not be
patched with arbitrary mean reversion — tick semantics and horizon come first. **Merged from:**
`HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`); audit §4.2; A3 check 7 (`A3-VERIFICATION-RESULTS.md:177-204`).

---

## P0.8 — Review the influence-operations targeting schema

### CB-32 — Dual-use influence-targeting schema with no acceptable-use terms. **DECISION TAKEN 18 JULY 2026 — now an enforcement item.**

> **Amended 19 July 2026.** This entry was headed **OWNER DECISION** and its exit was a written
> policy position. The founder took that decision on 18 July 2026. **CB-32 did not close.** The
> decision names eight controls and states that technical enforcement is mandatory while disclosure
> and any future acceptable-use language are supplementary, so this entry's remaining work is
> engineering, carried by **CB-40 to CB-47**. CB-32 is retained as the parent entry — it holds the
> evidence and the decision record — and is closed only when all eight child entries are closed.
> The ID is unchanged and nothing below has been deleted.
>
> **The decision made this entry more expensive, not less.** Anyone reading the old heading would
> conclude that B5 was one signature from clearing. It was; the signature has been given; and B5 is
> still open, now behind eight controls that do not exist.

**Plain English.** The repository contains a working template for designing an influence campaign:
who to target, what they already resent, which media channels reach them, how persuadable they are
by which kind of appeal, who should carry the message and how independent that person should appear,
how many coordinated accounts to use, and what behaviour the campaign is meant to produce — with a
field for marking the campaign's central claim as knowingly false. It is declarative today: it
drives almost nothing in the simulation. That does not change what it is as a published artefact.
No licence restricts its use, and the only safeguards in the project are three sentences of prose.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** B5 — **only when CB-40 to CB-47 are all closed** · **P0:** P0.8 ·
**Effort:** ~~owner decision, then large~~ **large; the decision is done and the enforcement is not
started**

**This is the only publication blocker that cannot be cleared by correcting text**
(`A3-VERIFICATION-RESULTS.md:245, :247`; `HANDOFF.md` § Publication exit criteria (`:104-105`)). Those citations describe it as
clearing by an owner decision, and **that half of them is now stale**: the decision was taken on
18 July 2026 and B5 remained open. What follows was written as evidence *for* the decision; it is
retained because it is equally the evidence of what the eight controls must be built against.

#### The decision, in the founder's terms

| # | Control | Implementation entry |
|---|---|---|
| 1 | Influence mechanics operate **only** in explicitly fictional worlds. | CB-40 |
| 2 | The scenario loader **requires** `world_mode: fictional` and **fails closed** when it is missing. | CB-41 |
| 3 | Real-world scenario import remains **disabled**. | CB-42 |
| 4 | Real persons, organisations and political populations **cannot** be influence-target entities. | CB-43 |
| 5 | Protected characteristics **cannot** be used as optimisation criteria for persuasion or manipulation. | CB-44 |
| 6 | Fictional **aggregate** narrative diffusion, exposure, adoption and counter-messaging **remain allowed**. | CB-45 |
| 7 | API and UI **disclose** that the active world is fictional. | CB-46 |
| 8 | Disclosure and any future acceptable-use language are **supplementary. Technical enforcement is mandatory.** | CB-47 |

**The identity and bias distinction, quoted rather than summarised:**

> **Permitted:** identity affects lived experience, relationships, discrimination, institutional
> access, media exposure and cultural interpretation.
>
> **Not permitted:** identity acts as an inherent competence, morality, loyalty, violence or
> manipulability coefficient.

The campaign model **may** use non-sensitive factors — geography, institutional affiliation,
economic exposure, political behaviour, media consumption — where justified by the fictional
scenario. It **must not** optimise against protected traits. CB-44 carries this.

**Source.** Founder decision of 18 July 2026, cited by date. It is not a file in the tree; no
citation into `HANDOFF.md` or the audit supports it, and both of those still describe B5 as
awaiting a decision.

**What the schema can express.** `Campaign`
(`scaffold/backend/app/simulation/schemas/agent_schema.py:320-346`): sponsor, strategic objective,
target cohorts, the pre-existing grievance the campaign exploits, narrative, messenger, channels,
amplification network, trigger event, desired behaviour, metrics. `CampaignNarrative` (`:280-284`)
pairs a free-text claim with a `truth_status` enum whose members are exactly `true`, `false`,
`unverified` (`:253-258`). `CampaignMessenger` and `AmplificationNetwork` (`:287-303`) carry
`perceived_independence`, `coordinated_accounts`, `sympathetic_commentators` and `estimated_reach`. `CampaignMetrics` (`:306-318`) declares `detection_probability` and
`attribution_probability`. Audience segmentation lives in `Cohort` (`:91-109`) and its sub-models:
`Demographics` including `religion_majority` and `primary_language` (`:22-28`); `MediaExposure` as
five per-channel reach floats (`:42-53`); `InfluenceSusceptibility` as three persuadability scalars
— `authority_appeal`, `identity_appeal`, `economic_appeal` (`:72-77`); `NetworkPosition` (`:80-88`).
`Campaign` and `Narrative` are both published as cross-language JSON Schemas
(`scaffold/schemas/campaign.schema.json`, `narrative.schema.json`), under
`https://meridian.example/schemas/`.

**A fully worked example ships in the repository.** `scaffold/scenarios/kestral-strait.json:389-418`
— sponsor `regional_spoiler_power_proxy`, objective
`weaken_public_support_for_western_naval_cooperation`, two target cohorts, grievance
`historic_foreign_interference_resentment`, a claim with `truth_status: "false"`, a messenger at
`perceived_independence: 0.8`, three channels, 40 coordinated accounts, 6 sympathetic commentators,
210,000 estimated reach, desired behaviour `protest_and_parliamentary_pressure`.

**What safeguards actually exist.** Three prose bullets at `CHARTER.md:135-142` and nothing else.
There is no `fictional: true` assertion anywhere — a case-insensitive grep for "fictional" across all
`.py`, `.json`, `.html` and `.js` files under `scaffold/` returns exactly one hit, the scenario's own
free-text disclaimer string at `scaffold/scenarios/kestral-strait.json:7`, which is read by nothing.
`load_scenario` (`scaffold/backend/app/api/runs.py`) does a path-existence check and `json.loads`,
with no name, entity or content validation. No JSON Schema validation library is present anywhere —
`grep -rn "jsonschema" .` returns nothing — so the nine published mirrors validate nothing at
runtime. `NOTICE.md`, read in full, contains no acceptable-use, field-of-use or dual-use restriction.

**Options as the audit stated them — SUPERSEDED, retained for provenance.**
`CURRENT-STATE-AUDIT.md:411` listed four non-exclusive options: an explicit acceptable-use /
field-of-use restriction in the licence; an enforced `fictional: true` assertion plus a real-entity
check at scenario load; surfacing `fiction_disclaimer` in every API response and in the UI; or
keeping the repository private. The decision of 18 July 2026 is broader than that list and reorders
it: the second and third options are absorbed into controls 2, 4 and 7 as **mandatory**; the first is
reclassified as **supplementary** by control 8; and the fourth — staying private — is not among the
adopted controls at all. It remains the present state under audit decision 8.2, not a substitute for
enforcement. The audit's closing note that "the technical enforcement is worth building whichever way
the policy goes" has been overtaken: it is now required, not worth considering.

**Interaction with a settled decision — OPEN QUESTION, still not resolved here.** Control 8 makes
acceptable-use language supplementary rather than unnecessary, so if the owner later wants such
language it still needs a vehicle, and which vehicles exist turns entirely on how `HANDOFF.md:22` is
read. Note that no answer to this question can close CB-32 or any of CB-40 to CB-47, since none of
them may be discharged by prose.

> **Question for the owner:** does "Licence: none, deliberately... Do not add an open-source licence"
> (`HANDOFF.md:22-23`) rule out *any* licence file, or only an open-source one?

This record does **not** answer that, and nothing below should be read as an answer. Decision 8.1 is
settled and is not reopened here. Two observations only, offered because the answer bears on CB-32:

- Audit decision 8.1's sub-instruction to "add the file so tooling can detect it" is **conditional on
  its own opening clause**, "Decide the licence, then add the file"
  (`CURRENT-STATE-AUDIT.md:401`). `HANDOFF.md:22` settled that decision as "none". The absence of a
  `LICENSE` file in the tree is therefore recorded here as a fact, **not** as an unmet requirement,
  and this record makes no recommendation to create one.
- If the reading permits a licence file, a restriction could attach to one. If it does not, the
  candidate vehicles are `NOTICE.md` or a separate terms document. Either way the choice of vehicle
  is the owner's, and this record deliberately does not narrow it.

**Evidence requirement for closing this entry.** CB-40 to CB-47 are all closed, each on the evidence
its own entry requires. **No document, charter bullet, disclaimer or acceptable-use text may be
recorded as evidence closing any of them** — that is control 8, and CB-47 enforces it as a review
rule. CB-32 does not close on the existence of the 18 July 2026 decision; that decision is what
created the eight entries.

**Merged from:** blocker B5 (`A3-VERIFICATION-RESULTS.md:245`); audit decision 6 (`:411`); audit
§5.12; audit §7 responsible-use row (`:385`); `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) and § Publication exit criteria (`:104-105`); **founder decision of
18 July 2026 (the eight controls and the identity/bias distinction).**

---

### CB-40 — Confine influence mechanics to explicitly fictional worlds. *(Control 1)*

**Plain English.** The parts of the simulation that model persuasion must refuse to run at all
unless the world they are running in is declared fictional. Not warn, not annotate — refuse.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** contributes to B5 · **P0:** P0.8 · **Effort:** medium · **Parent:** CB-32

**What the control requires.** Influence mechanics operate **only** in explicitly fictional worlds.
This is a gate on execution, not a label on output. It depends on CB-41, which supplies the
declaration that this control reads.

**What exists today.** No world-mode concept exists anywhere in the tree.
`MeridianModel._step_diffusion` (`scaffold/backend/app/simulation/engine.py:138-145`) is called
unconditionally from `step()` at `engine.py:156`, and the cohort susceptibility path
(`cohort_agent.py:22-26` → `diffusion.py:74-76`) runs on every tick of every scenario. **There
is nothing to confine it, and nothing that could refuse.**

**Evidence requirement.** A test must load a scenario whose world is not declared fictional and
assert that no influence or diffusion code path executes — the run is refused, not annotated. A
second test must assert a fictional scenario still runs, so the check is shown to discriminate
rather than to block everything. Both tests must be in the suite and passing. **Neither test
exists today.**

**Merged from:** founder decision of 18 July 2026, control 1.

---

### CB-41 — Require `world_mode: fictional` at scenario load, failing closed. *(Control 2)*

**Plain English.** Every scenario must say, in a machine-readable field, that its world is
fictional. A scenario that does not say so must be rejected — and rejected *because* it did not say
so, rather than being given a helpful default. A default would quietly turn this control off.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** contributes to B5 · **P0:** P0.8 · **Effort:** medium · **Parent:** CB-32

**What the control requires.** The scenario loader **requires** `world_mode: fictional` and **fails
closed** when it is missing. Fail-closed is the operative word: absence must be a rejection, not a
fallback.

**What exists today.** `world_mode` appears in no schema, no Pydantic model and no scenario file.
`load_scenario` (`scaffold/backend/app/api/runs.py:21-26`) performs a path-existence check and
`json.loads` with no validation of any kind. The nearest existing artefact is the free-text
`fiction_disclaimer` at `scaffold/scenarios/kestral-strait.json:7`, which is not a mode, is declared
by no schema, and is read by no code. `routes_simulation.py:43-46` catches only `FileNotFoundError`,
so a malformed scenario currently surfaces as a 500 rather than a typed rejection.

**Evidence requirement.** A test asserts rejection for all three of: `world_mode` absent; `world_mode`
null; `world_mode` set to any value other than `fictional`. The rejection is a typed error surfaced
as a 4xx, not a 500. A grep over the load path returns **no default value** for the field — a default
converts fail-closed into fail-open and would defeat the control without failing any test that only
checks the happy path.

**Open question — see the summary table.** Adding a required field to scenario JSON and to the
loader is a change under `scaffold/`, which the standing "documents only" constraint does not permit
and which the founder decision does not authorise.

**Merged from:** founder decision of 18 July 2026, control 2.

---

### CB-42 — Keep real-world scenario import disabled, and assert that it stays disabled. *(Control 3)*

**Plain English.** There must be no way to feed the engine a scenario describing the real world. It
currently has no such feature — but "we never built one" is not a control, because the next
contributor may build one without knowing it was forbidden.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** contributes to B5 · **P0:** P0.8 · **Effort:** small · **Parent:** CB-32

**What the control requires.** Real-world scenario import remains **disabled**.

**What exists today.** No import or upload endpoint was found. **That is an absence, not an
enforcement**, and this entry exists to convert the one into the other. `load_scenario` builds a path
from a scenario id; whether it refuses a path resolving outside the vetted scenario directory was
**not tested** and is not asserted anywhere.

**Evidence requirement.** No code path constructs a scenario from user-supplied, uploaded or remote
content. A test asserts that the loader refuses any path resolving outside the vetted scenario
directory, path traversal included. The disabled state is asserted by a test that would fail if an
import surface were added, rather than being inferred from a grep returning nothing.

**Merged from:** founder decision of 18 July 2026, control 3.

---

### CB-43 — Prevent real persons, organisations and political populations from being influence targets. *(Control 4)* **CARRIES AN OPEN QUESTION.**

**Plain English.** Even inside a fictional world, the targeting fields must not be pointed at a real
person, a real organisation or a real political population. Something at load time has to catch that
and refuse.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** contributes to B5 · **P0:** P0.8 · **Effort:** large · **Parent:** CB-32

**What the control requires.** Real persons, organisations and political populations **cannot** be
influence-target entities.

**What exists today.** No entity, name or content validation of any kind occurs at scenario load. No
schema carries any concept of a real-world referent. `target_cohorts` (`agent_schema.py:320-346`)
accepts whatever the scenario names.

**The open question this entry cannot answer.** The decision states the prohibition, not the
detection method, and the candidates are not interchangeable:

> **Question for the owner:** by what test is an entity determined to be "real"? A maintained
> denylist fails open on anything unlisted. Scenario-author attestation fails open on a careless or
> dishonest author — and control 8 rules it out as the *sole* mechanism, since an attestation is not
> technical enforcement. Human review before a scenario is admitted does not fail open, but does not
> scale and is not a code control.

Until that is settled this entry has no testable exit, and **no agent may settle it.**

**Evidence requirement.** A validation step at scenario load rejects a scenario in which a real
person, organisation or political population appears as an influence-target entity, and a test
demonstrates that rejection failing closed. The determination method is written down in the
repository and is not attestation alone.

**Merged from:** founder decision of 18 July 2026, control 4.

---

### CB-44 — Bar protected characteristics from acting as persuasion optimisation criteria. *(Control 5)* **CARRIES AN OPEN QUESTION.**

**Plain English.** Identity may shape what a fictional person is exposed to, who they know and how
they read events. It may not become a dial the campaign model turns to find the most manipulable
group. The difference is real, and it has to be made mechanical rather than left as an intention.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** contributes to B5 · **P0:** P0.8 · **Effort:** large · **Parent:** CB-32

**What the control requires.** Protected characteristics **cannot** be used as optimisation criteria
for persuasion or manipulation. The decision's distinction, quoted:

> **Permitted:** identity affects lived experience, relationships, discrimination, institutional
> access, media exposure and cultural interpretation.
>
> **Not permitted:** identity acts as an inherent competence, morality, loyalty, violence or
> manipulability coefficient.

The campaign model **may** use non-sensitive factors — geography, institutional affiliation, economic
exposure, political behaviour, media consumption — where justified by the fictional scenario.

**What exists today.** `Demographics` declares `religion_majority` and `primary_language`
(`scaffold/backend/app/simulation/schemas/agent_schema.py:22-28`); both are inert, with zero read
sites outside the schema file. **`InfluenceSusceptibility` is not inert.** Its three appeal scalars
— `authority_appeal`, `identity_appeal`, `economic_appeal` (`:72-77`) — are averaged into a single
susceptibility score at `cohort_agent.py:22-26`, and that score drives per-cohort diffusion gain at
`diffusion.py:74-76`. A field named `identity_appeal` already feeds a persuasion computation. Whether
that is a protected-trait proxy or a permitted non-sensitive factor is **not decided by this record.**

**The open question this entry cannot answer.**

> **Question for the owner:** which attributes count as protected characteristics for this control,
> and does enforcement mean removing the declared fields, gating their read sites, or asserting
> output invariance? And is an "identity appeal" persuadability scalar inside the prohibition or
> outside it?

**Evidence requirement.** The enumerated list of protected characteristics is recorded in the
repository. No field in that list is read by any targeting, ranking, susceptibility or
campaign-effect path — verified by call-site enumeration, not by grep alone. A test asserts that
changing *only* a protected-characteristic attribute of a cohort leaves campaign targeting and effect
outputs **bit-identical**. That test is the mechanical form of the permitted/not-permitted
distinction; note it cannot be written until the isolation work in P0.4A lands, since on a single
shared RNG stream a bit-identical comparison is not meaningful evidence — see CB-39.

**Merged from:** founder decision of 18 July 2026, control 5, and its identity/bias distinction;
`docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md` is the specification-side record of the same rule.

---

### CB-45 — Keep fictional aggregate diffusion, exposure, adoption and counter-messaging working. *(Control 6)*

**Plain English.** The controls above are restrictions, and restrictions can over-shoot. This entry
is the opposite check: inside a properly declared fictional world, the legitimate aggregate
mechanics must still function.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** contributes to B5 · **P0:** P0.8 · **Effort:** small · **Parent:** CB-32

**What the control requires.** Fictional **aggregate** narrative diffusion, exposure, adoption and
counter-messaging **remain allowed**. This is a permitted-scope boundary, not a restriction, and its
verifiable form is a **non-regression** test rather than a rejection test.

**What exists today.** Aggregate diffusion exists and writes `narrative_adoption`
(`scaffold/backend/app/simulation/diffusion.py:63-79`). **Counter-messaging has no implementation**,
so there is nothing to regress on that half — the criterion applies to it prospectively.

**Evidence requirement.** With the other seven controls in force, a test asserts that a fictional
scenario still produces non-zero aggregate diffusion, exposure and adoption, and that a
counter-messaging action measurably changes an aggregate outcome once such an action exists. This
entry **fails if enforcement over-blocks**, which is the failure mode the other seven cannot detect.

**Merged from:** founder decision of 18 July 2026, control 6.

---

### CB-46 — Disclose in the API and the UI that the active world is fictional. *(Control 7)* **CARRIES AN OPEN QUESTION.**

**Plain English.** A user, and anything reading the API, must be told the world is fictional without
having to go looking for it.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** contributes to B5 · **P0:** P0.8 · **Effort:** medium · **Parent:** CB-32 ·
**Related:** CB-33 (provenance tag on generated text — a different charter obligation, in the same
interface surface, and not a substitute for this one)

**What the control requires.** API and UI **disclose** that the active world is fictional. Note
control 8: disclosure is **supplementary to** enforcement, not a substitute for it, so closing this
entry does not soften CB-40 to CB-44.

**What exists today.** No API response carries any world-mode or fiction field. None of the five REST
endpoints in `routes_simulation.py` returns one — `create_run` (`:47-49`), `advance` (`:60`),
`get_state` (`:71-77`), `submit_decision` (`:101`), `get_events` (`:111`). `scaffold/frontend/`
contains one file, `index.html`, with no fiction, provenance, AI-generated or disclaimer text. The
scenario's own `fiction_disclaimer` is read by nothing.

**The open question this entry cannot answer.**

> **Question for the owner:** what evidence closes the UI half? The API half is contract-testable.
> A rendered interface disclosure is verifiable by no command in this backlog, and a screenshot, a
> component test and a reviewer's signed observation are not equivalent.

**Evidence requirement.** Every REST response carries an explicit world-mode / fiction field,
asserted by a contract test covering **all five** endpoints rather than a sample. The interface
displays the disclosure where a user reaches it without interaction, evidenced in whichever form the
owner rules acceptable.

**Merged from:** founder decision of 18 July 2026, control 7.

---

### CB-47 — Enforce that no control is discharged by prose. *(Control 8)*

**Plain English.** The project's defining defect is documents claiming properties the code lacks.
This entry exists so that the fix for B5 cannot become another instance of it. A disclaimer is not a
control. A policy paragraph is not a control. Only working, tested code closes CB-40 to CB-44 and the
API half of CB-46.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** contributes to B5 · **P0:** P0.8 · **Effort:** trivial to state, ongoing to
enforce · **Parent:** CB-32

**What the control requires.** Disclosure and any future acceptable-use language are
**supplementary. Technical enforcement is mandatory.**

**What exists today.** The only safeguards in the repository are three prose bullets at
`CHARTER.md:135-142`, and `NOTICE.md` — read in full — contains no acceptable-use, field-of-use or
dual-use restriction. Under control 8, those three bullets close nothing.

**Evidence requirement.** This is a **review rule**, not a command, and it should be written into the
pull-request template so it is enforced rather than remembered. Each of CB-40 to CB-44 and the API
half of CB-46 is closed against a **test reference**. Any entry whose recorded evidence is a
document, a disclaimer, a charter bullet or an acceptable-use text fails this control and re-opens
the entry it purported to close. A reviewer confirms this by reading the per-control sign-off table
in `PUBLICATION-EXIT-CRITERIA.md` C6.

**Merged from:** founder decision of 18 July 2026, control 8.

---

### CB-33 — The charter requires a provenance tag on generated text. Nothing implements it.

**Plain English.** The charter commits to every piece of AI-generated advisory text carrying a
visible label at the interface, so a reader always knows what was machine-written. Nothing
implements this. The only marker that exists is a literal prefix hard-coded inside the stub's return
string, so on the swap to a live call that the code itself documents it would not survive unless
someone deliberately reinstated it.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — (supports whichever safeguard is chosen in CB-32) · **P0:** P0.8 ·
**Effort:** medium

**Note on classification.** This is a *requirement not met*, not a false claim — `CHARTER.md:141`
states an obligation, not an accomplishment. It sits here because it is one of the safeguards
in play for CB-32, not because it is a Phase 0 untruth.

**Evidence.** The only marker on generated text is a literal prefix inside the stub briefing string,
`[STUB briefing — tick {tick}]` (`scaffold/backend/app/simulation/llm_gateway.py:99-103`, the return
statement). That it would be lost when a live model is wired is an **inference**, not an observation
— the live path does not exist to observe. It follows from the marker being part of the canned return
value rather than applied by any wrapper, and from the function's own docstring at
`llm_gateway.py:93` ("Canned briefing text. Swap for a LiteLLM call grounded (RAG) on real state
fields."; `:94` is the closing `"""`). `routes_simulation.py:76` returns `briefing` as a bare string
beside `macro_state`; the "interpretive layer only" note there is a source comment that is never
transmitted. No provenance field exists in any API response. The bundled frontend contains no
fiction, disclaimer or provenance text at all: `grep -rni "fiction\|provenance\|AI-generated\|
disclaimer" frontend/` returns nothing, and `frontend/` contains one file, `index.html`. No API
response surfaces `fiction_disclaimer` — none of the **five** REST endpoints in
`routes_simulation.py` returns it: `create_run` (`:41-49`), `advance` (`:53-60`), `get_state`
(`:64-77`), `submit_decision` (`:81-101`) and `get_events` (`:105-111`). They return only
run/tick/macro-state/narrative-adoption/briefing/acceptance/event fields. (An earlier draft said
"four", omitting `submit_decision` — the endpoint CB-01 cites by line. The conclusion is unchanged
and holds for all five.)

**Merged from:** audit §6.5 item 49 (`CURRENT-STATE-AUDIT.md:351`); audit §5.12; `CHARTER.md:141`.

---

## Track C — the interview-demonstration programme

**Source: founder correction, 19 July 2026.** Like the founder decisions of 18 July 2026, this is
**not a file in the tree** and is cited by date throughout. The string "Track " occurs in exactly one
file under the whole tree outside this record — `docs/design/research-evidence/PRODUCT-STUDIES-DIGEST.md`,
once, in an unrelated sense — so nothing in `HANDOFF.md`, `CURRENT-STATE-AUDIT.md` or
`A3-VERIFICATION-RESULTS.md` describes Track A, B or C, and no citation into them should be read as
supporting this section's existence.

**The correction, in its own terms.** Track C is not merely a UI workstream. It has **two converging
lanes** and **five gates**.

| Lane | What it is | May proceed |
|---|---|---|
| **C-VISUAL** | Prototype and product communication | On explicitly labelled fixture data, once the separate UI-research handoff is received and reconciled. **Must not wait for P0.4 to P0.6** — and can never be described as the final functioning demonstration. |
| **C-ENGINE** | Executable product proof | On the real dependency chain: P0.4 → P0.4A → P0.5 → P0.6 → benchmarks and integrated UI. |

**The mandatory prototype label, quoted verbatim.** Every fixture-backed surface must visibly state:

> `INTERACTIVE PROTOTYPE — FIXTURE DATA — NOT CONNECTED TO THE SIMULATION ENGINE`

and that label must remain visible in screenshots and in recordings. See the open question in CB-48:
a **different** mandatory label text is already specified in the drafted slice specification, and the
two have not been reconciled.

**Critical-path relationship — recorded because it is easy to mistake Track C for a side workstream.**
The demonstration's endpoint requires three capabilities the audit found **missing**: that "the engine
validates and executes" (blocker B1 — `_validate_and_price` is a seven-entry dict lookup, CB-01); that
"society reacts differently across entities" (critical finding 4.1 — the tiers are causally decoupled,
CB-29); and that "replay reproduces the authoritative state hash" (there is no replay path, no state
hashing, and the RNG state is never captured — CB-30, CB-37). The critical path is therefore
**P0.4 → P0.4A → P0.5 → P0.6**, and Track B sits **on** that critical path rather than beside it.

**On the LLM gateway, use this wording and no stronger:**

> "The architectural mutation boundary exists in scaffold form, but live model integration,
> external-input recording and replay have not yet been implemented."

The existing stubbed gateway must **not** be described as demonstrating real LLM integration.

**What exists today — the whole of it.** `scaffold/frontend/` contains one file, `index.html`, 67
lines, titled `MERIDIAN — dev stub` (`:6`) and self-described as a "Minimal dev harness" whose "Full
UI (scenario selector, role dashboards, decision composer) is specified in `design_ux_screens.md` and
left for a later build" (`:17-18`) — a citation to one of the five design documents that do not exist
(CB-12). It renders three buttons and a log pane (`:24-29`), holds no state beyond `runId` and a
WebSocket handle (`:32`), and contains no fiction, provenance or disclaimer text (CB-33, CB-46). There
is no `package.json`, no framework and no build step anywhere under `scaffold/`. **None of the five
screens named below exists in any form.**

**The five screens, and where they are specified.** Strategic Command Centre, Entity Dossier, Society
Pulse, Conversational Command Interface and Causal Timeline are specified in
`docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md` §1-§5, which is **untracked, drafted by an AI agent,
not founder-approved and not implemented** — its own banner says so at `:3-9`. Its build order
(`:563-575`) already maps the same unlock chain this section records: role filtering on auth (D3),
"Activity, Timeline, evidence receipts as *real*" on P0.6, counterfactuals and stable generated
portraits on P0.4A, computed propagation on P0.5, and alerts, thresholds and forecasts on decay,
cooldown and P0.7.

### The scope filter for the first vertical slice

**Founder correction, 19 July 2026.** A feature enters the first vertical slice **only if all five
hold**. Any one failing keeps it out.

| # | Filter |
|---|---|
| 1 | It appears in the five-minute walkthrough. |
| 2 | It demonstrates one of the four primary product propositions. |
| 3 | It improves the main screenshot or the core interaction. |
| 4 | It can be implemented **honestly** — that is, without a present-indicative claim the code does not support. |
| 5 | It does **not** delay the first real cross-tier causal slice. |

The **four primary product propositions** are already written down in
`docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md:18-23`, and filter 2 should be read against that
list: persistent inspectable people and organisations; a crisis propagating through society, media,
markets and institutions; unexpected actions proposed in natural language with the interpreted plan
inspectable; and the player understanding why visible state changed. That document is a draft with no
authority, so if the founder's list of four differs, the founder's governs.

Filter 5 is the one that binds hardest on this backlog: it subordinates the whole of C-VISUAL to
CB-29 (P0.5), which is where the first real cross-tier causal slice is built.

### Do-not-build list for the interview phase

**Founder correction, 19 July 2026.** None of the following is to be built for the interview phase.
**None of it is rejected as a product direction** — the same distinction
`docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md:596` draws for its own consolidated exclusions. It is
excluded from this phase.

| # | Not for the interview phase |
|---|---|
| 1 | Production multiplayer |
| 2 | A complete scenario editor |
| 3 | Full voice and image processing |
| 4 | Photorealistic portraits at scale |
| 5 | A full military combat simulator |
| 6 | All planned screens |
| 7 | Real-world influence targeting |
| 8 | A distributed production platform |
| 9 | Every behavioural model |

Item 7 is not only a scope exclusion: it is also **prohibited** by the founder decision of 18 July
2026, controls 1 to 4, which CB-40 to CB-43 carry. Excluding it here does not discharge those entries,
and building it later would require them. Item 5 corresponds to the operational military layer that
`docs/design/UI-RESEARCH-HANDOFF.md:412-413` raises as decision **D12**, which is unresolved.

**Every entry below is a target.** None describes work in progress, and nothing in this section is
approved.

---

### CB-48 — Gate C0: five connected fixture-backed screens, honestly labelled. **CARRIES OPEN QUESTIONS.**

**Plain English.** Build five screens that hang together as one navigable prototype, running on
made-up data that is clearly marked as made up, and record a five-minute walkthrough of it. Nothing
about it may suggest a simulation is running underneath, because none is.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** — (Track C; not in `HANDOFF.md` § Phase 0 priority order (`:70-90`)) ·
**Lane:** C-VISUAL · **Effort:** large · **carries open questions**

**Unlocked by.** No engine work. The stated precondition is that the **separate UI-research handoff is
received and reconciled** — `docs/design/UI-RESEARCH-HANDOFF.md` exists in the tree, dated 19 July
2026, untracked, and its §9 records twelve decisions the founder has not taken. **Do not use the
absence of C3 to delay C0.**

**What the gate requires.** Five connected fixture-backed screens — Strategic Command Centre, Entity
Dossier, Society Pulse, Conversational Command Interface, Causal Timeline — in an original visual
language, with honest prototype labelling, a five-minute scripted walkthrough, and **no claim of
connected simulation behaviour**.

**Evidence requirement.** All five screens are navigable as one prototype. Every fixture-backed
surface carries the mandatory label, and a **build-time assertion** proves the label cannot be
disabled in a fixture build — the mechanism `UI-VERTICAL-SLICE-RECOMMENDATION.md:40-44` proposes for
its own variant of the label. The label is legible in every screenshot and throughout the recording,
not only on first paint. The five-minute walkthrough exists as a recorded artefact and is titled
**PROTOTYPE WALKTHROUGH**. A reviewer reads the script, the interface text and the recording and finds
no sentence claiming connected simulation behaviour, checked against
`docs/delivery/CAPABILITY-CLAIMS.md`. **No engine capability may be cited as evidence for this gate**,
and passing it establishes nothing about C1 to C4.

**OPEN QUESTION for the owner — two mandatory label texts now exist, and they differ.** The founder
correction requires `INTERACTIVE PROTOTYPE — FIXTURE DATA — NOT CONNECTED TO THE SIMULATION ENGINE`.
The drafted slice specification requires a persistent non-dismissible band reading `FIXTURE DATA — NOT
A SIMULATION RUN`, adjacent to a `FICTIONAL WORLD` disclosure
(`docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md:40-44`). These are different strings making
different assertions — the founder's names the engine connection, the draft's names the run — and a
build-time assertion can only be written against one of them. Which text governs, and does the
fictional-world disclosure (control 7, CB-46, and decision D11 at
`docs/design/UI-RESEARCH-HANDOFF.md:408-410`) sit inside it or beside it? **Not resolved here.**

**OPEN QUESTION for the owner — does the founder correction discharge D10?**
`docs/design/UI-RESEARCH-HANDOFF.md:405-406` records D10 — "Is a fixture-backed prototype authorised
before Phase 0 completes, and is the labelling mechanism in §8.1 sufficient? **This is the decision
that gates all implementation.**" The founder correction states that C-VISUAL may proceed on
explicitly labelled fixture data once the handoff is reconciled, which reads as an authorisation in
principle, but it does not cite D10 and does not rule on §8.1's labelling mechanism. Whether D10 is
now answered, partly answered, or still open is a question for the owner. **An AI agent must not treat
the correction as having closed it.**

**Related evidence-form question — same class as CB-46's.** A rendered interface and a recording are
verifiable by no command in this backlog. A screenshot, a component test and a reviewer's signed
observation are not equivalent. See the open-questions table.

**Merged from:** founder correction of 19 July 2026, gate C0 and the C-VISUAL lane definition;
`docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md` §0-§5 (drafted, unapproved);
`docs/design/UI-RESEARCH-HANDOFF.md` §9 (D10, D11).

---

### CB-49 — Gate C1: live state connection.

**Plain English.** The interface stops inventing its own numbers and starts reading the simulation's
official state instead. Not all of it — enough to prove the connection is real — and anything still
made up has to stay visibly marked as made up.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** — (Track C) · **Lane:** C-ENGINE ·
**Effort:** large

**Unlocked by.** **P0.4 — the authoritative-state contract, CB-28.** Note what that means today: CB-28
is carried whole, is not decomposed, and this record's own "Verification status" section records it as
**unactionable as written**. So C1's unlock condition is currently unspecifiable, not merely unmet.

**What the gate requires.** The UI reads a **versioned authoritative snapshot**. No authoritative state
is held client-side. At least one real entity, one cohort, one organisation and one indicator come
from the engine. Fixture-only values remain **visibly distinguished** from live values.

**Evidence requirement.** A named snapshot version is carried on the response and asserted by a
contract test. A test demonstrates that the client holds no authoritative state — for instance, that
discarding and rebuilding the client's view from the snapshot alone reproduces the same rendering. The
four required kinds of object are each traced to an engine source rather than a fixture file. The
live/fixture distinction is visible in a screenshot without interaction, and a test fails if a live
value renders in fixture treatment or the reverse. The C0 label remains on every surface still backed
by fixtures.

**Note on what C1 does not license.** Reading real state is not the same as showing real propagation.
Passing C1 permits no claim about societal response — that is C2 — and none about explanation or
replay, which is C3.

**Merged from:** founder correction of 19 July 2026, gate C1; `HANDOFF.md:75` (P0.4) via CB-28.

---

### CB-50 — Gate C2: live societal propagation, from the engine and not from a script.

**Plain English.** One crisis, followed all the way through: insurers react, shipping reroutes, a port
economy is exposed, people's beliefs and behaviour shift, media and families respond, political
pressure builds, and the government's state changes. Every one of those changes has to come out of the
engine. This is the first moment at which the demonstration may honestly say MERIDIAN simulates a
societal response.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** — (Track C) · **Lane:** C-ENGINE ·
**Effort:** large

**Unlocked by.** **P0.4A (CB-34 to CB-39) and P0.5 (CB-29).** Both. P0.4A first: the founder decision
of 18 July 2026 states that P0.5 implementation may not proceed until P0.4A passes, and without named
substreams an apparent cross-tier link cannot be distinguished from draw-order contamination — which
is exactly the mistake critical finding 4.1 records and `A3-VERIFICATION-RESULTS.md` §6 demonstrates.

**The chain the gate names.** Maritime crisis → insurer risk response → shipping-company rerouting →
port-economic exposure → cohort belief and behaviour changes → media and family reactions → political
pressure → government state change. The UI must display changes **from the engine**, not from fixture
scripts.

**Evidence requirement.** The chain runs end to end in a single run, and each displayed change is
traceable to an engine state change rather than to a fixture. A test asserts that altering the
initiating crisis alters downstream values, and that removing it removes them — the control-run form
A3 used to prove `block_unfunded_spending` inert
(`A3-VERIFICATION-RESULTS.md`, carried at CB-20 row 5). A test fails if any link in the chain is
fixture-fed. Because the comparison is bit-level, it is only meaningful once CB-39's isolation tests
pass — the same dependency CB-44's evidence requirement records.

**Wording gate.** **Only on passing this gate** may the demonstration claim that MERIDIAN simulates a
societal response. Until then that claim is unavailable in any script, screenshot, recording or
document; `docs/delivery/CAPABILITY-CLAIMS.md` is the authority on the permitted wording.

**Merged from:** founder correction of 19 July 2026, gate C2; `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) via CB-29; founder
decision of 18 July 2026 (P0.4A sequencing) via CB-34 to CB-39; audit §4.1;
`A3-VERIFICATION-RESULTS.md` §6.

---

### CB-51 — Gate C3: explainability and replay. **CARRIES AN OPEN QUESTION.**

**Plain English.** The demonstration can show why anything happened — what caused it, which rule fired,
what the state was before and after, what was assumed and how uncertain it is — and it can re-run a
recorded run from scratch, touching no language model and no network, and land on exactly the same
state.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** — (Track C) · **Lane:** C-ENGINE ·
**Effort:** large

**Unlocked by.** **P0.6 — events, snapshots and replay, CB-30.** CB-37 (recording the RNG algorithm and
version) and CB-30's own scope (capturing and restoring generator state into snapshots) are both
prerequisites of an identical-hash replay; the boundary between them is stated in CB-30 and must not
be blurred here.

**What the gate requires.** Causal events; causal parents; rule and mechanism attribution; before and
after state; assumptions and uncertainty; state hashes; recorded external inputs; replay with **zero**
model or network calls; and identical resulting authoritative hashes.

**Evidence requirement.** A recorded run and its replay produce identical authoritative state hashes,
demonstrated on more than one run. The zero-calls property is enforced by an automated check rather
than asserted — `CURRENT-STATE-AUDIT.md:453` already proposes an AST import check for the adjacent LLM
boundary, and CB-36 needs the same technique for the RNG boundary; the same approach applies here, and
a replay that merely *happens* not to call out proves nothing. Every displayed explanation resolves to
a recorded causal event with its parents, not to prose composed at render time. A test shows the
replay red — diverging hashes — when a recorded external input is withheld, so the recording is
demonstrated to be load-bearing.

**Wording gate.** **Only after this gate passes** may the project claim causal reconstruction or replay
capability. Until then `HANDOFF.md` § Standing constraints (`:135`) stands unchanged: the codebase is not to be described as
execution-ready, replay-capable or fully deterministic. On the model boundary, the approved wording is
verbatim: *"The architectural mutation boundary exists in scaffold form, but live model integration,
external-input recording and replay have not yet been implemented."*

**OPEN QUESTION — see the open-questions table.** What artefact closes a walkthrough gate? Both the
**PROTOTYPE WALKTHROUGH** (CB-48) and the **INTEGRATED ENGINE WALKTHROUGH** required here are recorded
performances, and no command in this backlog verifies one.

**Merged from:** founder correction of 19 July 2026, gate C3 and the two-walkthrough requirement;
`HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) and § Standing constraints (`:135`), via CB-30; audit `:259, :453, :465`.

---

### CB-52 — Gate C4: scale evidence, with measured and projected kept apart.

**Plain English.** Run the thing at several sizes and write down what actually happened — how long a
tick took, how much memory it used, how many events it produced, how long a replay took. Then describe
how it would scale further, and never let those two kinds of statement share a column.

**Owner:** Aries Russell (unassigned) · **Clears blocker:** — · **P0:** — (Track C) · **Lane:** C-ENGINE ·
**Effort:** large

**Unlocked by.** C3 (CB-51) for the replay-duration figure, which cannot be measured before a replay
path exists. The remaining figures depend on P0.4 (CB-28) for a defined state to measure and on P0.5
(CB-29) for a workload worth measuring.

**What the gate requires.** Benchmark several entity and cohort counts. Record tick time, memory, event
volume and replay duration. Distinguish **MEASURED** performance from **PROJECTED** architecture.
Document the path to partitioning or distributed execution **without claiming it has been delivered.**

**Evidence requirement.** A benchmark record states the machine, the configuration, the commit and the
date, and is reproducible by a stated command. Every figure is labelled measured or projected, and no
projected figure appears in the same column, table row or chart series as a measured one. The
partitioning and distributed-execution write-up contains no present-indicative sentence about
capability that does not exist — the standing constraint that governs this whole record, and the one a
scale section is most likely to breach. Zero benchmark figures exist today: no benchmark, harness or
timing artefact is present anywhere in the tree.

**Note on the endpoint.** The final interview demonstration is **C3 plus sufficient C4 evidence**.
"Sufficient" is not defined by the correction and is not defined here.

**Merged from:** founder correction of 19 July 2026, gate C4 and the definition of the final
demonstration.

---

## Summary tables

### By P0 item

| P0 | Entries | Of which clear a blocker |
|---|---|---|
| P0.1 — correct live false claims | CB-01 … CB-24 (24) | 5 (CB-01, CB-02\*, CB-03, CB-04, CB-05) |
| P0.2 — reproducible installation | CB-25, CB-26 | 0 |
| P0.3 — establish real CI | CB-27 | alternative route to B2 |
| P0.4 — authoritative state | CB-28 | 0 |
| **P0.4A — deterministic randomness** | **CB-34 … CB-39 (6)** | **0** |
| P0.5 … P0.7 — engineering foundations | CB-29 … CB-31 | 0 |
| **P0.8 — dual-use decision and enforcement** | **CB-32, CB-40 … CB-47, CB-33 (10)** | 1 (CB-32, **only when CB-40 … CB-47 all close**) |
| **Track C — interview demonstration (not a P0 item)** | **CB-48 … CB-52 (5)** | **0** |

P0.4A is listed in founder-set sequence position, between P0.4 and P0.5, not in ID order. Two
workstreams are decomposed into entries: P0.4A into CB-34 to CB-39, and **P0.8's enforcement into
CB-40 to CB-47, one per control**. CB-28 to CB-31 are carried whole. Note that P0.8 changed
character on 18 July 2026: it was a policy item with a single owner-decision exit, and it is now a
policy item with eight engineering exits behind it.

**Track C occupies the last row because it is not a Phase 0 item at all**, and its five entries carry
`—` in the `P0` field rather than a heading from `HANDOFF.md` § Phase 0 priority order (`:70-90`). Its ordering is by gate (C0 to
C4), which is an unlock chain rather than a priority list, and only the first gate — CB-48, lane
C-VISUAL — is unlocked by anything other than Phase 0 engineering work. **No Track C gate clears a
publication blocker**, which is why it does not appear in the "By blocker" table below; the
relationship runs the other way, since CB-50 and CB-51 cannot be reached until the work behind B1,
CB-29 and CB-30 is done. Nothing in Track C is built.

\* Whether CB-02 is required to clear B1, or whether CB-01 alone suffices, is a judgement this
record does not settle — see CB-02's **Uncertain** note. It is listed as blocker-clearing on the
conservative reading that it is needed.

### By blocker

| Blocker | Entries | Clears by |
|---|---|---|
| B1 | CB-01, and CB-02 **if required** — the coupling is unsettled, see CB-02's Uncertain note | Text correction. Implementing the evaluator is not required. |
| B2 | CB-03 (text) or CB-27 (build the guard); CB-23 corrects the blocker's own stale justification. Note CB-03 shows the sentence is doubly wrong, so building CI alone does not make it true | Text correction, or build CI *and* a genuine mutation guard |
| B3 | CB-04 | Text correction |
| B4 | CB-05 | Text correction |
| B5 | CB-32 (parent), closing only when **CB-40 … CB-47** all close | ~~Owner decision~~ **Superseded 18 July 2026.** The owner decision was taken and B5 did not clear. It now clears by **technical enforcement, implemented and verified** — eight controls, each closed against a test reference. No text correction clears it, and neither does a policy statement: control 8 makes disclosure and acceptable-use language supplementary. |

### Open questions for the owner

Fifteen. None is resolved in this record. **One question was removed from this table on 19 July 2026
because the owner answered it** — the dual-use policy itself, formerly listed against CB-32. Its
answer is recorded in CB-32 and generated the four new CB-41 / CB-43 / CB-44 / CB-46 questions
below, which are about *how* the eight controls are enforced and not about whether they apply.
**Three more were added the same day by the Track C amendment** (CB-48 twice, CB-51 once); the count
read "Twelve" until they were entered, and both entries referred the reader here while they were
absent.

| Ref | Question |
|---|---|
| CB-39 | P0.4A exit criteria 6 and 8 are stated in terms of entity promotion, which the same decision forbids until P0.4A passes. Build a minimal promotion harness inside P0.4A, or carry those two criteria forward as a gate on promotion itself? |
| CB-48 | Two mandatory prototype label texts now exist and they differ. The founder correction requires `INTERACTIVE PROTOTYPE — FIXTURE DATA — NOT CONNECTED TO THE SIMULATION ENGINE`; the drafted slice specification requires `FIXTURE DATA — NOT A SIMULATION RUN` beside a `FICTIONAL WORLD` disclosure (`docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md:40-44`). They assert different things — one names the engine connection, the other the run — and a build-time assertion can only be written against one. Which text governs, and does the fictional-world disclosure (control 7, CB-46; decision D11) sit inside it or beside it? |
| CB-48 | Does the founder correction discharge **D10** (`docs/design/UI-RESEARCH-HANDOFF.md:405-406`), the decision that gates all interface implementation? The correction authorises labelled fixture work in principle but does not cite D10 and does not rule on the §8.1 labelling mechanism. Answered, partly answered, or still open? An AI agent must not treat the correction as having closed it. |
| CB-51 | What artefact closes a walkthrough gate? Both the **PROTOTYPE WALKTHROUGH** (CB-48) and the **INTEGRATED ENGINE WALKTHROUGH** (CB-51) are recorded performances, and no command in this backlog verifies one. Same class as CB-46's question about a rendered UI disclosure: a screenshot, a component test and a reviewer's signed observation are not equivalent. |
| CB-41 | Adding a required `world_mode` field to the scenario schema, the scenario files and the loader is a change under `scaffold/`. Does the standing "documents only" constraint permit it, and what authorises the work — the founder decision states it authorises no feature implementation. Same class as CB-17's question, and it gates CB-40, CB-42, CB-43, CB-44 and CB-46 as well. |
| CB-43 | By what test is an entity determined to be "real"? Maintained denylist (fails open on anything unlisted), author attestation (fails open, and control 8 rules it out as the sole mechanism since it is not technical enforcement), or human review before admission (does not fail open, does not scale, is not a code control)? |
| CB-44 | Which attributes count as protected characteristics, and does enforcement mean removing the declared fields, gating their read sites, or asserting output invariance? Specifically: is `identity_appeal` — a persuadability scalar that already feeds diffusion gain — inside the prohibition or outside it? |
| CB-46 | What evidence closes the UI half of the disclosure control? The API half is contract-testable; a rendered interface disclosure is verifiable by no command, and a screenshot, a component test and a reviewer's signed observation are not equivalent. |
| CB-14 | Was `NOTICE.md:11` ("publicly visible") written as present fact or as the intended post-publication position? The correction differs. |
| CB-17 | What is the correct `represents_population` for `coastal-creole-fishing`, and should a total-population field exist at all? |
| CB-17 | Does the standing "no edits under `scaffold/`, documents only" constraint permit editing scenario JSON? Until answered, CB-17 is not authorised to write. |
| CB-18 | What are the branch and pull-request conventions? Resolve the placeholder or delete the section. |
| CB-25 | Drop the unimported-but-deliberate `python-socketio` dependency and supersede ADR-005, or keep it? Not an install-blocking question. |
| CB-26 | Adopt `uv` + `pyproject.toml`, or stay on `requirements.txt` + `pip-compile`? (Audit decision 8.5, open.) |
| CB-32 | Does "Licence: none, deliberately" (`HANDOFF.md:22`) rule out *any* licence file, or only an open-source one? Decision 8.1 is settled and is **not** reopened by asking this; the reading determines which vehicles exist for a field-of-use restriction, should the owner want one. Note that control 8 makes such a restriction **supplementary**, so no answer here closes CB-32 or any of CB-40 to CB-47. |

Further items are marked **Uncertain** or **drafter's judgement** rather than raised as questions,
because they are the drafter's reasoning rather than matters requiring an owner ruling before work
can proceed. The full list, so none reads as sourced:

- CB-02's coupling to B1.
- CB-10's judgement that a charter claim may be reframed as a labelled target.
- The sequencing preference for CB-03 over CB-27, labelled in both entries.
- The sequencing preference for CB-17 over CB-29, labelled in both entries.
- CB-03's proposed **scope expansion** beyond the sourced "delete 'in CI'" instruction — an editorial
  call on the charter's governing text, which is the owner's.
- CB-23's classification of its own relationship to blocker B2.
- CB-38's reading of what exit criterion 9's "can be associated with" requires — a structural keyed
  interface, or a persisted per-draw log. The founder decision does not say, and the two differ
  substantially in cost.
- The decomposition of P0.4A into six entries, and the assignment of each of the ten exit criteria to
  one of them. The scope and the criteria are the founder's; the shape of the entries is not.
- The decomposition of P0.8's enforcement into eight entries, one per control (CB-40 to CB-47), and
  every **evidence requirement** written into those entries. The eight controls and the
  identity/bias distinction are the founder's, verbatim; the tests proposed to verify them are the
  drafter's construction and are for the owner to accept, amend or replace. In particular, the
  "bit-identical" form of CB-44's test, the three-case rejection matrix in CB-41 and the
  no-default-value check are drafter's proposals, not founder-set exit criteria — B5 has no stated
  criteria list of the kind P0.4A has.
- The classification of CB-45 (control 6) as a non-regression criterion and CB-47 (control 8) as a
  review rule rather than a command. Both follow from the controls' wording, but the founder did not
  categorise them.
- Every `Effort` rating, and the seven `P0` assignments listed under "Verification status".

Audit decision 8.3 (whether Mesa remains the ABM substrate) is open. It generates no **P0.1
documentary correction**, which is why no entry appears above — but it does not follow that it is
irrelevant to this backlog, and an earlier draft dismissed it in a single clause. Two of the
constraints the audit records against Mesa are technical and bear directly on entries here: Mesa
"materialises a second `random.Random` whose seeding on the API path comes from entropy (6.27)" and
"introduces a `Model.rng` attribute collision on any future 3.x upgrade"
(`CURRENT-STATE-AUDIT.md:405`). An entropy-seeded second RNG on the API path touches CB-28 (the
authoritative-state contract), CB-29 (whose original premise was shared-RNG contamination) and CB-30
(replay foundations, where a non-reproducible RNG is disqualifying). Whether that interaction
warrants an entry, and whether 8.3 should be settled before P0.4-P0.6 begin, is the **owner's call**.
This record raises it and does not decide it.

**The founder decision of 18 July 2026 sharpens this, without settling it.** P0.4A exit criterion 2
requires that no subsystem receive unrestricted access to the root generator, and Mesa's
entropy-seeded `self.random` is exactly an unrestricted generator sitting on the model object — see
CB-36. So decision 8.3 now bears on a stated P0.4A exit criterion rather than only on a general
tidiness concern, and P0.4A cannot exit without deciding what happens to that second generator.
Whether that forces 8.3 to be settled, or is satisfiable by sealing the attribute while Mesa stays,
remains the **owner's call**. Still not decided here.

Audit decision 8.7 (whether `PLAN.pdf` remains the canonical plan format) is also open, but — unlike
8.3 — it **does** interact with this backlog, and the interaction is flagged rather than resolved.
CB-12 instructs "repoint each at the corresponding `PLAN.pdf` section" and CB-22 instructs
"re-anchor each to the corresponding `docs/PLAN.pdf` section". Both are source-sanctioned (audit §9
says the same), but both presuppose that `PLAN.pdf` remains the citation target, which is precisely
what 8.7 leaves open. Carrying them out would entrench `PLAN.pdf` while the decision stands
unmade. The owner may wish to settle 8.7 first, or accept the re-anchoring as reversible.

Decisions 8.1 (licence), 8.2 (visibility and the publication gate) and 8.4 (the reproducibility
claim wording) are settled per `HANDOFF.md:13-23, :52-62` and are not reopened here.

---

## Verification status of this record

Every file:line citation above was read directly during drafting or during the grounding pass that
preceded it, with these exceptions, which are stated in place and repeated here so they cannot be
missed:

- **No code was executed.** No test was run, no engine invoked, no evidence script in
  `docs/delivery/evidence/` re-run, no package installed. All code-side statements rest on reading
  source and on the absence of call sites, plus execution evidence already recorded in
  `CURRENT-STATE-AUDIT.md` and `A3-VERIFICATION-RESULTS.md`. In particular, **whether the five
  existing tests currently pass is unknown** (bears on CB-27), and **CB-17's behavioural-neutrality
  is inferred from absence of call sites, not from a before/after run**.
- **Counts and greps are time-sensitive.** The tree is growing: untracked documents exist under
  `docs/` that are not in commit `71fa329`. Any count in this record (files, links, grep hits) is
  stated as of the drafting date and must be re-run at the point of correction, not quoted forward.
- **`docs/PLAN.pdf` was not text-extracted.** Claims attributed to it are unverified (CB-22, CB-24).
- **No network or `gh` command was run.** Remote visibility and GitHub-level controls are unverified
  (CB-23).
- **The `litellm` install failure was not reproduced** (CB-25).
- **A3's line references into the audit** (CB-20) were not individually re-verified.
- **Every `Effort` rating is the drafter's unsourced estimate.** No source document assigns effort to
  any item. The ratings are for sequencing only and carry no more authority than a guess; whoever
  executes should re-estimate. They are presented in the same field table as cited evidence and must
  not be read with the same weight.
- **Seven `P0` assignments are the drafter's classification, not a sourced mapping:** CB-13, CB-14,
  CB-19 and CB-21 to CB-24, all routed to P0.1 on the grounds that they are false or stale claims,
  which is what `HANDOFF.md:70-71` says P0.1 covers. Defensible, but not stated by any source. CB-33
  carries the same disclosure in place.
- **This backlog does not sweep P0.1 completely.** Two of the six categories `HANDOFF.md:70-71` names
  — execution readiness and replay — have no entry. See "Known gaps" in the plain-English summary.
  The entry count (forty-seven) measures what was consolidated, not what P0.1 requires.
- **The P0.4A entries (CB-34 to CB-39) rest on the founder decision of 18 July 2026 plus source
  reading, and on no new execution.** No test was run and no RNG behaviour was reproduced for this
  amendment. The grep-verified statements added by it are narrow and are stated in place: `hash(` has
  zero occurrences in `.py` files under `scaffold/` (CB-35), and `getstate`/`setstate` likewise have
  zero occurrences (CB-37). Everything else is quoted from `CURRENT-STATE-AUDIT.md`,
  `A3-VERIFICATION-RESULTS.md` §6, `ADR-007` or the named source files.
- **The P0.8 enforcement entries (CB-40 to CB-47) rest on the founder decision of 18 July 2026 plus
  source reading, and on no new execution.** No test was written or run for that amendment, and no
  control was implemented or measured. Every "What exists today" paragraph in those entries
  describes an **absence**; none describes partial compliance, because nothing partially satisfies
  any of the eight. Two statements in them are the drafter's grep-and-read observations rather than
  quotations from a source: that `world_mode` appears nowhere in the tree, and that
  `InfluenceSusceptibility`'s appeal scalars reach `diffusion.py:74-76` through
  `cohort_agent.py:22-26` — the latter was already recorded in `PUBLICATION-EXIT-CRITERIA.md` C6 and
  is re-stated, not newly found. **The founder decision itself is not a file in the tree** and is
  cited by date throughout.
- **The Track C entries (CB-48 to CB-52) rest on the founder correction of 19 July 2026 plus source
  reading, and on no new execution.** No screen was built, no prototype rendered, no walkthrough
  recorded and no benchmark run. **Nothing in Track C exists**: the whole of the front end is
  `scaffold/frontend/index.html`, 67 lines, titled "MERIDIAN — dev stub", with no `package.json`, no
  framework and no build step anywhere under `scaffold/`; none of the five named screens exists in any
  form; and no benchmark, harness or timing artefact is present in the tree. Every gate below is
  therefore written as a target with an unlock condition, and **no sentence in those entries records
  progress**. Two further cautions. First, the **five gates are the founder's and their sequence is
  the founder's; every `Evidence requirement` written into them is the drafter's construction** — the
  correction states what each gate requires, not what test closes it — so those requirements are for
  the owner to accept, amend or replace, exactly as recorded for CB-40 to CB-47. Second, the two
  supporting documents cited throughout the section, `docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md`
  and `docs/design/UI-RESEARCH-HANDOFF.md`, are **untracked, drafted by an AI agent and not
  founder-approved**; they are cited as drafts and carry no authority, and where they differ from the
  founder correction the correction governs. **The founder correction itself is not a file in the
  tree** and is cited by date throughout. `docs/delivery/CAPABILITY-CLAIMS.md` remains the authority
  on permitted wording, and no gate below licenses wording ahead of the gate that unlocks it.
- **One contradiction between sources was found and deliberately left open.**
  `CURRENT-STATE-AUDIT.md:39` and `:527` state that `test_same_seed_is_deterministic` fails when
  global randomness is injected into `CohortAgent.step`; `:140` records that the same injection
  leaves macro equality True, and that test asserts on macro only. **CB-39 records both and resolves
  neither.** It should be settled by running it, not by choosing a citation.
- **P0.4A also touches documents this backlog does not correct.** `ADR-007` names
  `test_same_seed_is_deterministic` as proof of a property it does not establish, and
  `README.md:61-63` makes the same claim in the front door. Both are P0.1 documentary corrections and
  **neither has an entry**. They are flagged in CB-34, CB-39 and the "Known gaps" summary rather than
  silently absorbed into the engineering work.
- **Ownership and evidence, as found by the cross-workflow integration sweep of 19 July 2026.** No entry
  carried an `Owner` field before that sweep; all forty-seven now read `Aries Russell (unassigned)`, which
  is a recorded absence of assignment and **not** a delegation to anyone. Three related gaps were found and
  deliberately left open, because closing them is drafting work rather than the application of a stated
  convention: **(i)** thirty-two entries state no evidence requirement (see the field table); **(ii)**
  CB-28 to CB-31 state neither an evidence requirement nor any decomposition, and are therefore
  **unactionable as written** — deliberately so, and the preamble to that section says so, but a reader
  should not expect to be able to start them from this record; **(iii)** entries do not carry a
  prerequisite field, so where one entry blocks another the dependency is stated in prose if at all —
  CB-38's `Dependency` note, CB-29's and CB-17's sequencing notes, CB-32's parent relationship to CB-40 to
  CB-47, CB-41's note that its open question gates five sibling entries, and the P0.4A preamble's
  sequencing rule are examples, and they are not uniform in placement or wording.

This record asserts nothing beyond that evidence. Where a claim could not be verified it is marked
**COULD NOT VERIFY** or **unknown** rather than softened, and where a judgement was made rather than
observed it is marked **uncertain**.
