# Phase 0 Remediation Plan

> **Status: DRAFT — pending owner review.** Drafted by an AI agent. Nothing in this document
> constitutes an approved decision. Every item marked *owner decision* stays open until the owner
> resolves it in writing.
>
> **Three exceptions, all founder decisions — the first two of 18 July 2026, the third of 19 July
> 2026.**
>
> 1. §P0.4A records a founder decision, not a drafter's proposal. The item's existence, placement,
>    scope, sequencing rule and ten exit criteria are decided. Its *approach* — the ADR — is not, and
>    neither is OQ-9. Nothing in this document authorises beginning P0.4A implementation.
> 2. §P0.8's **eight controls and the identity/bias distinction** are a founder decision. The
>    verification methods proposed against them are the drafter's, as are OQ-10 to OQ-13. Nothing in
>    this document authorises building any control.
> 3. The `# Track C` block's **two lanes, five gates C0–C4, C0's release from the P0.4–P0.6
>    dependency, the fixture-label requirement and the critical-path statement** are a founder
>    correction of 19 July 2026. Track C is **not** a P0 item; it consumes them. Gate-to-P0 unlock
>    mappings are the founder's where stated and are marked as the drafter's inference where not.
>    Nothing in this document authorises beginning work on any gate, C0 included.

**Date:** 18 July 2026
**Amended:** 19 July 2026 — **P0.4A added** by founder decision of 18 July 2026. See §P0.4A.
**Amended:** 19 July 2026 — **P0.8 rewritten** by founder decision of 18 July 2026 settling B5. The
item's blocker changed from an owner decision to eight enforcement controls that do not exist. **This
enlarges Phase 0 and the publication gate.** See §P0.8, the §5 dependency summary and OQ-8.
**Amended:** 19 July 2026 — **Track C recorded** by founder correction of 19 July 2026. Track C is a
delivery programme that **consumes** the P0 items; it is **not** a P0 item, adds no P0.x identifier and
renumbers nothing. See the `# Track C` block after P0.8, the note appended to §5, and §8 item 13.
**Scope:** the founder-set Phase 0 priority order, P0.1 to P0.8, exactly as stated in
[`HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:68-90`), **plus P0.4A**, which the founder added on 18 July 2026 after
that list was written. The full order is now:

> P0.1 truthful claims → P0.2 reproducible installation → P0.3 honest CI → P0.4 authoritative state →
> **P0.4A deterministic randomness** → P0.5 cross-tier causality → P0.6 events, snapshots and replay →
> P0.7 time and horizon → P0.8 dual-use review

P0.4A is deliberately **lettered, not numbered**, so that the founder-set numbering P0.1→P0.8 survives
unchanged and every existing citation of P0.5 to P0.8 elsewhere in the repository stays correct.
`HANDOFF.md` § Phase 0 priority order (`:68-90`) does not yet list it; where the two disagree on the item list, this amendment is the
later record. Nothing else about the founder-set order is changed.
**Amended 19 July 2026 — the clause "does not yet list it" is superseded.** By founder decision of
19 July 2026 the canonical sequence was corrected and P0.4A now sits at `HANDOFF.md` § Phase 0
priority order, P0.4A (`:76-83`). The two records no longer disagree on the item list. This plan
remains the fuller statement of P0.4A's scope, dependencies and sequencing rule.
**Inputs:** [`CHARTER.md`](../../CHARTER.md), [`HANDOFF.md`](../../HANDOFF.md),
[`CURRENT-STATE-AUDIT.md`](CURRENT-STATE-AUDIT.md) (audit CLOSED),
[`A3-VERIFICATION-RESULTS.md`](A3-VERIFICATION-RESULTS.md).

---

## 1. What this document is, in plain English

The repository currently contains documents that describe a system more capable than the code
actually is. That single defect is why the repository is private. Phase 0 is the work that makes the
documents true, makes the project installable and checkable, and writes down the contracts the
engine is supposed to honour.

Phase 0 is **not** the work that makes the simulation better. The two critical findings — the three
tiers do not causally influence one another, and the macro indicators saturate with no opposing
mechanism — are behavioural, and they are later-phase work.

## 2. The behaviour line, and why it must hold

The audit's own phased plan is explicit that Phase 0 "changes no behaviour and adds no features; it
makes the documents match the code" (`CURRENT-STATE-AUDIT.md:423`). The founder-set P0 list is
broader than documentation alone — it also covers installation, CI, written contracts and design —
so this plan describes Phase 0 as **documentation and foundations**.

What that means concretely:

| Category | Items | Changes simulation behaviour? |
|---|---|---|
| Documentary correction | P0.1 | No |
| Tooling and environment | P0.2, P0.3 | No |
| Written contract / design artefact | P0.4, P0.5, P0.7 | No — these produce specifications, not code |
| Foundations with a code surface | P0.4A, P0.6 | **Boundary cases — see the open questions in §P0.4A (OQ-9) and §P0.6 (OQ-7)** |
| Policy, governance and its enforcement | P0.8 | **Boundary case since 18 July 2026** — the decision itself changes nothing, but seven of its eight controls require code. See §P0.8 and OQ-13 |

P0.4A was added to Phase 0 by founder decision on 18 July 2026, after this plan's first draft. It is
the sharpest of the boundary cases: its exit criteria require code, and switching the randomness
architecture will change numeric outputs at an unchanged seed. That consequence is stated openly in
§P0.4A and raised as **OQ-9**; it is not treated here as authorised.

P0.8 became a boundary case on the same date and for a different reason. Its policy exit is satisfied,
but seven of its eight controls are checks and refusals in code — a loader that fails closed, a
validation that rejects, a field on every API response. Adding a control that refuses to run a
scenario is not "modifying simulation behaviour to make a finding disappear", but it is not a
documentation change either, and **OQ-13** asks what authorises it. Nothing here treats it as
authorised.

**The two critical findings (`A3-VERIFICATION-RESULTS.md:142-204`) must not be fixed in Phase 0.**
P0.5 designs the cross-tier channels; it does not build them. P0.7 defines tick semantics and
horizon; it does not touch saturation. If a Phase 0 change alters a numeric output, that change has
left Phase 0 and needs owner approval under `HANDOFF.md` § Standing constraints (`:139-140`).

## 3. Standing constraints that govern this plan

Carried from `HANDOFF.md` § Standing constraints (`:133-140`), restated because they bind every item below:

- Do not describe the codebase as execution-ready, replay-capable or fully deterministic.
- Do not modify simulation behaviour merely to make an audit finding disappear.
- The broad audit is closed. Do not open new investigations to service this plan.
- AI agents may draft records; they may not approve decisions.

The only reproducibility claim permitted in any corrected document is the founder-approved wording
at `HANDOFF.md:56-57`:

> "The existing stubbed execution path reproduces the same tested numeric outputs when the seed,
> scenario and stubbed agent outputs remain identical."

And the target contract, which must **always** be labelled a target and never a delivered
capability (`HANDOFF.md:61-62`):

> "Given the same scenario version, rule-pack version, seed, ordered player inputs and recorded
> external-agent inputs, the engine is intended to reproduce identical authoritative state hashes."

## 4. Sequencing note the owner must rule on

`HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) annotates P0.5 as follows: *"this is arguably the highest-value item, since it is
the product's core mechanism, not a tidiness fix."*

That annotation is surfaced here and **not acted on**. This plan preserves the founder-set order
P0.1 → P0.8 without reordering, because reordering the founder's own priority list is a decision an
agent may not take. See **Open Question OQ-1** in §6.

**Amendment, 18 July 2026.** The founder has since confirmed that P0.5's sequencing is **unchanged**,
and has separately ruled that P0.5's *specification* may proceed in parallel now while its
*implementation* waits for P0.4A. This narrows OQ-1 without closing it: the highest-value design work
is already unblocked, so promoting P0.5 wholesale is no longer the only way to get at it — and P0.5
implementation could not be promoted ahead of P0.4A in any case. OQ-1 remains open as a question about
ordering the *rest* of the list; the owner should re-read it in that narrower light.

---

# Phase 0 items

Each item states an objective in plain English, why it matters, the work, a testable exit
criterion, its dependencies, and whether it is blocked on an owner decision.

---

## P0.1 — Correct live false claims

> *"Correct live false claims (CI, legality validation, persistence, replay, archetype
> extensibility, execution readiness). Documentation must describe observed behaviour."*
> — `HANDOFF.md:70-71`

**Blocked on an owner decision:** No, with two narrow exceptions (OQ-2, OQ-3 below).
**Dependencies:** None. This is the entry item; everything else assumes the documents have stopped
asserting untrue things.

### Plain English

The README, the charter and the architecture decisions all state things about the engine that are
not true of the code as written. Fix the words. Do not fix the code to match the words — that is
later-phase work and would change behaviour.

### Why it matters

This is the defect the repository is private for. It is also the cheapest one: four of the five
publication blockers (`A3-VERIFICATION-RESULTS.md:241-244`) clear by text correction alone, and A3
states explicitly for B1 that "implementing the evaluator is **not** required."

### Work items — technical evidence layer

Each row is a live claim, verified present in the tree at the line given, with the observed code
behaviour that contradicts it.

**Group A — "the engine validates legality" (blocker B1). Seven live sites:**

| Claim site | Wording | Observed behaviour |
|---|---|---|
| `README.md:38` | "LLM proposes; engine validates legality and computes cost/effect" | `engine.py:121-130` — `_validate_and_price` is `base = ACTION_EFFECTS.get(...)` then `return dict(base)` |
| `README.md:41` | "engine rejects invalid actions" | No rejection path exists in `engine.py:121-130` |
| `scaffold/README.md:19` | "the engine validates legality and computes effects" | as above |
| `CHARTER.md:112` | "then priced, validated and resolved by the engine" | as above. Note `CHARTER.md:113-114` is **true** and must be kept |
| `scaffold/backend/app/simulation/engine.py:3-4` | "the engine here validates legality and computes/applies effects" | docstring of the module that does not |
| `scaffold/backend/app/simulation/agents/institutional_agent.py:4-5` | "the engine … validates legality and computes effects" | as above |
| `scaffold/backend/app/api/routes_simulation.py:4-5` | "the engine validates and prices them" | A3 §5 drove this through `TestClient`: endpoint appends to `event_log` and returns `{"accepted": true}` |

Two further sibling docstrings in the same family: `agent_schema.py:157-158` ("the engine decides
whether the action is legal") and `agent_schema.py:377-379` ("runs a legality/feasibility check").

**Three further sites of the same claim**, surfaced by the C2 grep in
`PUBLICATION-EXIT-CRITERIA.md` and re-confirmed against source on 19 July 2026. They are further
instances of the already-identified B1 claim, not new findings, and no new investigation was opened
to produce them. They must be corrected in the same pass or C2 cannot pass:

| Claim site | Wording |
|---|---|
| `scaffold/backend/app/simulation/llm_gateway.py:60-61` | "The engine validates legality and computes effects; this function never touches numeric state" |
| `scaffold/backend/app/simulation/schemas/agent_schema.py:8` | "the engine validates and applies effects" |
| `scaffold/backend/app/simulation/engine.py:158` | comment: "Micro agents produce proposals; engine validates + applies" |

Also in the same family, and listed by `CORRECTIVE-BACKLOG.md` CB-01 but not in the table above:
`scaffold/docs/ARCHITECTURE_DECISIONS.md:54-55` (ADR-006 — the legality/feasibility clause, which
begins on `:54` and ends on `:55`; `:53-54` is the adjacent *sole-writer* sentence handled in
Group H, and an earlier draft of this plan cited it here by mistake) and
`scaffold/backend/app/api/routes_simulation.py:82-84`. Taken together the B1 population is **14**
sites, which is the figure CB-01 and C2 should be reconciled to.

**Group B — "guarded in CI" (blocker B2):**

`CHARTER.md:44` reads "…`test_llm_gateway_cannot_write_state` guards in CI." There is no CI. No
`.github/` directory exists; the only YAML in the tree is `scaffold/docker-compose.yml`. This is the
single hit returned by `grep -rn "in CI"` over project files.

Note that the *other* half of B2's justification is now stale: B2 as written at
`A3-VERIFICATION-RESULTS.md:242` says "There is no CI and no `.git`." The repository **is** now under
version control at commit `71fa329` on branch `main`. B2 should be restated as a CI-only blocker.

**Group C — persistence (blocker B3):**

`scaffold/docs/ARCHITECTURE_DECISIONS.md:29-31` (ADR-003, Status: Accepted, present tense): "We
persist three things…". `scaffold/README.md:41` ends the architecture diagram at "PostgreSQL
(simulation_run, state_snapshot, event_log)" with no "planned" annotation. Observed: `SimulationRun`,
`StateSnapshot` and `EventLog` are defined at `db/models.py:23,42,56` and instantiated nowhere; there
is no `session.add`, `.commit` or `.merge` anywhere in the scaffold; `get_db()` (`db/session.py:44`)
is used by no route. The only DB interaction that can occur is `create_all` DDL, inside a swallowed
`except Exception` at `main.py:38-39`.

The audit's stated remedy is to add "in the scaffold" caveats to ADR-003 matching the existing
`ADR-004:37` and `ADR-005:45` convention (`CURRENT-STATE-AUDIT.md:427`).

**Group D — archetype extensibility (blocker B4). Three live sites:**

`README.md:72-74` ("Nation archetypes are **data, not code**… never editing the engine"),
`scaffold/README.md:106-107`, `scaffold/docs/ARCHITECTURE_DECISIONS.md:75` ("Adding an eighth
archetype must require only a new `scenarios/*.json`"), plus the supporting instruction at
`scaffold/CLAUDE.md:53-55`. A3 records this as false and, worse, silently false.

> **Citation drift note.** The audit cites this claim at `README.md:106-107`. The root `README.md`
> is now 96 lines; the claim is at `README.md:72-74` with different wording. The `(PLAN.pdf §9)`
> phrasing the audit quotes now survives only at `scaffold/README.md:106-107`. Several audit
> citations have drifted this way; see §7.

**Group E — determinism-table rows describing functions that do not exist:**

`README.md:36` claims "seeded Monte Carlo draws" for macro. Observed: the entire per-tick macro rule
set is one uniform draw applied to one indicator — `noise = self.rng.uniform(-0.002, 0.002)` then
`apply_deltas({"shipping_throughput_pct_of_baseline": noise})` (`engine.py:132-136`). No ensembles.
The audit's remedy is "seeded stochastic draws" (`CURRENT-STATE-AUDIT.md:427`).

`README.md:37` claims "Seeded diffusion over the social graph" moves cohort beliefs. Observed:
diffusion output is assigned to `self.narrative_adoption` (`engine.py:137-145`) and never reaches
`CohortBeliefs`. The repository's own internal note already says so:
`scaffold/docs/AGENT_TASK_TEMPLATE.md:48-49`, "Hostile campaigns currently spread narrative adoption
but don't yet move cohort beliefs."

`README.md:39`, `:40` and `:41` describe three LLM functions — adversary campaign design, advisor
dialogue grounded by retrieval, and player-decision parsing. Observed: `llm_gateway.py` defines
exactly two public functions, `propose_action` (`:54`) and `generate_briefing` (`:85`), plus a private
`_stub_action_type` (`:41`). There is no campaign-composition function and no decision-parsing
function. `generate_briefing` performs no retrieval — it reads two keys from the mapping passed to it
(`indicators` and `tick`, at `llm_gateway.py:95-96`) and two values out of the nested `indicators`
dict (`:97-98`), then returns an f-string (`llm_gateway.py:85-103`; the file is 103 lines, so the
`:85-104` cited in an earlier draft over-ran the end of the file). *(An earlier draft of this plan
said "three keys from the mapping", which matches neither the code nor
`CURRENT-STATE-AUDIT.md:287`; reconciled to `CORRECTIVE-BACKLOG.md` CB-08.)*

**Group F — distribution claim:**

`CHARTER.md:61-62`: "The system models a **distribution**, rather than pretending there is one
objectively correct future." Observed: `ACTION_EFFECTS` (`engine.py:35-43`) is a seven-row table of
fixed scalar constants, and the gate returns `dict(base)` — a per-action constant, not a
distribution.

**Group G — prompt versioning:**

`scaffold/docs/ARCHITECTURE_DECISIONS.md:66-67` ("versioned separately by `model_id + prompt_version +
temperature`") and `scaffold/CLAUDE.md:25-26` ("logged separately by `model_id + prompt_version +
temperature`") both state that LLM text is tracked by that triple. Observed: `PROMPT_VERSION = "v1"`
is declared once at `llm_gateway.py:38` and read by nothing; `model_id` and `temperature` are logged
nowhere.

**Group H — "sole writer of numeric state":**

Present at `scaffold/docs/ARCHITECTURE_DECISIONS.md:53-54`, `scaffold/CLAUDE.md:13-14` and
`engine.py:3`. This one is *nearly* true and needs rewording rather than deletion: `engine.py` is
indeed the only module that calls `apply_deltas` (call sites `engine.py:136` and `:164`, definition
`macro_state.py:23`), and the only other macro write is the direct `self.macro.state.tick = self.tick`
at `engine.py:179`. The inaccuracy is that meso state is written outside `engine.py`, at
`cohort_agent.py:35-38`.

**Group I — field descriptions written in the present indicative for fields nothing reads:**

- `agent_schema.py:242-244` and its published mirror `scaffold/schemas/intervention.schema.json:50`:
  "Legal-check outcome set by the engine (null until validated)." `legal_check` is written by no
  code; A3 §5 showed the client supplies it and the engine echoes it back.
- `agent_schema.py:181-183`: `constraints` described as "Hard legal/procedural constraints on the
  agent." A3 §3 proved by substitution that they are causally inert (40-tick hash identical with and
  without: `1af9170525db`).
- `macro_state.py:26-27`: "Nested blocks (e.g. institutional trust) are handled explicitly by the
  engine, not here." No code anywhere writes any nested block.
- `diffusion.py:51`: "Adoption is monotonic non-decreasing and clamped to [0, 1]." The jitter term at
  `diffusion.py:75` spans −0.01 to +0.01 and is added to `gain` at `:76`, so adoption can fall. Only
  the clamp half of the sentence holds.

**Group J — dangling references and housekeeping:**

- Five design/research documents are cited and none exists (`design_simulation_schemas.md`,
  `design_nation_expansion.md`, `design_ux_screens.md`, `research_architecture.md`,
  `research_licensing.md`), across 8 named-file citation lines plus 1 glob:
  `agent_schema.py:3`, `macro_schema.py:3`, `scaffold/CLAUDE.md:49`,
  `scaffold/docs/AGENT_TASK_TEMPLATE.md:54`, `scaffold/docs/ARCHITECTURE_DECISIONS.md:4`, `:25`,
  `:71`, `scaffold/frontend/index.html:18`, and the glob at
  `scaffold/docs/AGENT_TASK_TEMPLATE.md:25`.
  *(The audit says ten; it is now nine, because the two `plan.txt` anchors went with the file.)*
- `README.md:96` links to `COPYRIGHT.md`, which does not exist. The file holding that position is
  `NOTICE.md`. This is the only broken markdown link **outside `docs/`** — the enumeration behind that
  statement excluded the delivery and planning records, and no HTML or non-markdown link target
  anywhere was enumerated, so it is not asserted as the only broken link in the tree as a whole.
  Inside `docs/`, sibling Phase B drafts quote the defective link verbatim while documenting it
  (`CORRECTIVE-BACKLOG.md` CB-13, `RAID-REGISTER.md` I5), so a tree-wide link check reports further
  failures that are citations of the first. *(Cited here by entry ID rather than line number: an
  earlier draft gave `CORRECTIVE-BACKLOG.md:419` and `RAID-REGISTER.md:443`, and both records have
  since moved. Sibling drafts are live documents; do not line-cite them.)* Note that the **remedy** —
  re-point the link at `NOTICE.md`, or create a `COPYRIGHT.md` — is **not preselected here**; it is
  open question OQ-3 in `CAPABILITY-CLAIMS.md`.
- `scaffold/CLAUDE.md:59` still contains the repository's only unresolved marker:
  `<!-- PLACEHOLDER: fill in with the team's real conventions -->`.
- `scaffold/README.md:111` credits "permissive licensing (Mesa Apache-2.0, FastAPI MIT, LiteLLM MIT)"
  without mentioning psycopg2-binary, which is LGPL (`requirements.txt:17`).
- `README.md:61-63` describes the two named tests as proving reproducibility and guarding the
  boundary. Both tests exist (`test_engine.py:34`, `:61`), but per audit §5.2/§5.3 the first compares
  only the final macro dict and the second is an attribute-presence check. The description of test
  *scope* needs correcting, not the tests.

**Already satisfied, do not schedule:** the audit's Phase 0 instruction to "delete `backend/plan.txt`"
(`CURRENT-STATE-AUDIT.md:427`) is a no-op — the file is not in the tree. Mark it done.

### Testable exit criterion

All four must pass, run from the repository root:

1. `grep -rn "design_[a-z_]*\.md\|research_[a-z_]*\.md" . | grep -v "^./docs/delivery/"` returns zero
   results, or only results pointing at files that exist.
   *Currently returns 8 results, all dangling.*
2. `grep -rn "in CI" --include="*.md" --include="*.py" --include="*.html" . | grep -v "^./docs/delivery/"`
   returns nothing that is false.
   *Currently returns **2** results, re-run 19 July 2026: `CHARTER.md:44`, which is false and is the
   correction this criterion exists for; and `docs/world-model/PERSON-MODEL.md:168` ("Sensitivity
   tests must run in CI"), which states a requirement on future work in an untracked planning draft
   rather than a present-tense claim, and which therefore has to be adjudicated against the
   criterion's "nothing that is false" wording rather than silently omitted. This matches
   `RAID-REGISTER.md` I13 and `CORRECTIVE-BACKLOG.md` CB-03; an earlier draft of this plan said one
   result, which was wrong. Note that `PUBLICATION-EXIT-CRITERIA.md` C3 runs the same grep with the
   wider `^./docs/` exclusion and therefore correctly reports one hit — the counts differ by
   exclusion scope, not by fact.*
3. `grep -rn "PLACEHOLDER" --include="*.md" --include="*.py" --include="*.html" . | grep -v "^./docs/delivery/"`
   returns zero results.
   *Currently returns 1 result: `scaffold/CLAUDE.md:59`.*
4. Every markdown link **outside `docs/`** resolves to an existing path, because the delivery and
   planning records necessarily quote the defects they document.
   *Currently 16 markdown links in that scope, of which one fails: `README.md:96` → `COPYRIGHT.md`.
   Re-verified 19 July 2026; matches `PUBLICATION-EXIT-CRITERIA.md` C13. Non-markdown link targets —
   for example inside `scaffold/frontend/index.html` — were **not** enumerated, so this criterion does
   not certify the tree as a whole.*

Plus the audit's reviewer-level criterion (`CURRENT-STATE-AUDIT.md:430`): a reviewer reading
`CHARTER.md`, both READMEs, `scaffold/CLAUDE.md` and `ARCHITECTURE_DECISIONS.md` finds no
present-tense claim contradicted by the code, verified by re-running the §6.1 checks. This one is a
human judgement, not a command; it should be signed off by a named reviewer, not by the agent that
did the edits.

### Owner decisions touching P0.1

- **OQ-2 (`NOTICE.md:11`).** It states, present indicative: "The source code is publicly visible for
  evaluation and portfolio purposes." The repository is private (`HANDOFF.md:13`). Whether this was
  meant as a statement of current fact or as a description of the intended post-publication position
  is the author's intent, and an agent cannot resolve it. It is the same defect class Phase 0 exists
  to fix, sitting inside the document that records the licence decision.
- **OQ-3 (dangling citations).** The audit's remedy is to "repoint the ten dangling design-doc
  citations at their `PLAN.pdf` sections." That presumes `PLAN.pdf` stays canonical, which is
  **decision 8.7 and still open**. Until 8.7 is settled, the dangling citations can be removed but
  cannot be correctly repointed.

---

## P0.2 — Restore reproducible installation

> *"Restore reproducible installation. Remove/optionalise LiteLLM. Pin supported Python.
> Clean-environment command that succeeds on Windows and Linux."* — `HANDOFF.md:72-73`

**Blocked on an owner decision:** Partially. The *outcome* is not blocked. The *route* is —
decision 8.5 (`uv` / `pyproject.toml`) is open. See OQ-4.
**Dependencies:** P0.1 should land first so the README this item rewrites is already truthful.
P0.3 depends on this.

### Plain English

Per the founder handoff (`HANDOFF.md:45-47`), someone who clones the repository and follows the README
cannot currently install it — a failure this plan reports second-hand and did not reproduce. What is
directly verified is that one dependency no code uses (`litellm`) is declared and installed by every
documented path. Remove it from the default install **or** make it an optional extra — the founder's
instruction is "Remove/optionalise LiteLLM" (`HANDOFF.md:72`) and this plan does not pick between the
two routes; see OQ-4. Then state which Python versions are supported, and give one command that works.

### Why it matters

If the documented install fails — as the handoff reports — that is the first thing a reader
encounters, before any of the project's actual work is visible. It also bears on CI (P0.3): CI should
not be built on a dependency set whose resolvability has not been verified.

### Work items — technical evidence layer

- **LiteLLM.** `litellm>=1.34,<2.0` is declared at `scaffold/backend/requirements.txt:20`. No
  executable code imports it: an AST parse of every `.py` file under `scaffold/` scanned 78 import
  statements and found zero importing `litellm`. The only textual occurrences are inside the
  `llm_gateway.py` module docstring, which spans `:1-29`; the sketch line is `:17`, and the module's
  real imports begin at `:31`. It is nonetheless installed by all three documented paths, because it
  is an unconditional line in the single `requirements.txt` that both `scaffold/README.md` (`:58`,
  `:69`) and the Dockerfile (`:11`) consume.
  *Note: `HANDOFF.md:45-47` records the specific failure — resolves to 1.92.0, no cp313 wheel,
  sdist needs a Rust toolchain. That failure has not been independently re-observed for this plan;
  it is reported second-hand.*
- **Python version.** There is no machine-readable `requires-python` anywhere: no `pyproject.toml`,
  no `setup.cfg`, no `.python-version`. The version target exists only in prose
  (`ARCHITECTURE_DECISIONS.md:11`, `scaffold/CLAUDE.md:44`: "Python 3.11+") and in the Docker base
  image (`Dockerfile:1`, `python:3.11-slim`). A3 ran on CPython 3.13.9
  (`A3-VERIFICATION-RESULTS.md:27`) — two minor versions above what Docker pins. The supported range
  is therefore undeclared, and the *documented install path* has not been shown to work at either
  end: 3.11 exists only as the Docker base image, whose build outcome is Unknown
  (`CURRENT-STATE-AUDIT.md:29`), and 3.13.9 has been exercised only under a hand-built environment
  that excluded `litellm` (`A3-VERIFICATION-RESULTS.md:27`; `HANDOFF.md:49-51`).
- **Pinning.** All 13 declared packages are open-ended ranges. There is not one exact pin and no
  hashes; `websockets>=12.0` (`requirements.txt:13`) has no upper bound at all. There is no lockfile
  of any kind in the tree. *(Count reconciled 19 July 2026:
  `grep -c -E '^[^#[:space:]]' scaffold/backend/requirements.txt` → `13`, in a 24-line file. Earlier
  drafts of this plan and of `CORRECTIVE-BACKLOG.md` said twelve; thirteen is correct.)*
- **Docker.** `Dockerfile:13` is `COPY . .` with no `.dockerignore` present, so the whole build
  context enters the image. `docker-compose.yml:29` overrides the Dockerfile `CMD` to add `--reload`,
  and `:21-23` overrides `DATABASE_URL` regardless of `.env`. `docker-compose.yml:20` requires a
  `.env` file that is gitignored (`.gitignore:24-26`) and therefore never present in a fresh clone;
  `scaffold/README.md:47` instructs `cp .env.example .env` as the first step.

### Testable exit criterion

From a clean environment on **both** Windows and the Docker base image, a single documented command
completes and the suite runs:

```
<documented install command>
cd scaffold/backend && python -m pytest tests -v
```

The command and the date it was last run are recorded in the README, per
`CURRENT-STATE-AUDIT.md:445`. The exit condition is that the install completes and the suite result
is recorded honestly — **not** that a particular number of tests pass. `HANDOFF.md:51` records
"5 passed" under a hand-built environment excluding `litellm`; that has not been reproduced for this
plan.

Secondary check: `docker build` produces an image that does not contain `.venv`
(`CURRENT-STATE-AUDIT.md:447` also names `plan.txt`, which no longer exists).

### Owner decision

**OQ-4 — decision 8.5, still open.** `CURRENT-STATE-AUDIT.md:409` frames it: moving to
`pyproject.toml` plus a hash-pinned lock fixes both the broken install and the reproducibility
caveat, but changes four documented workflows and the Dockerfile — "a deliberate migration, not a fix
to slip in." P0.2's minimum (remove or optionalise `litellm`, declare a supported Python, verify one
clean command) can be delivered without settling 8.5. A hash-pinned lockfile cannot. Note that
remove-versus-optionalise is itself an unchosen sub-decision inside OQ-4: `HANDOFF.md:72` permits
either, and dependency changes sit on the human-approval list at `HANDOFF.md` § Standing constraints (`:139`).

---

## P0.3 — Establish real CI

> *"Establish real CI. Only checks that genuinely exist and pass."* — `HANDOFF.md:74`

**Blocked on an owner decision:** No for the workflow itself. Branch protection requires owner action
on the remote (OQ-5).
**Dependencies:** **Strong sequencing dependency on P0.2.** The documented install is *reported*
failing on Windows/CPython 3.13 (`HANDOFF.md:45-47` — second-hand, not reproduced for this plan), and
whether it fails the same way on the platform CI would actually run on (Linux/Python 3.11) is
explicitly **Unknown** (`CURRENT-STATE-AUDIT.md:29`; see also §8 items 1, 3 and 8). CI should not be
built on an install path whose resolvability is unverified; landing P0.2 first removes the risk either
way. It also bears on P0.1's B2 correction: B2 clears
by P0.1's text edit to `CHARTER.md:44`, and once CI exists and runs the boundary test the "in CI"
half of that sentence becomes literally true as well. The *strength* of the guard is still limited by
the test itself, which P0.1 records as a tautological attribute-presence check — CI does not turn it
into a strong guarantee.

### Plain English

There are no automated checks. Add some — and only ones that actually run and actually pass. A
workflow that claims to check something it does not check would recreate the exact defect this whole
phase exists to remove.

### Why it matters

The charter claims a determinism boundary is "guarded in CI" (`CHARTER.md:44`). The "in CI" half of
that claim can be made true two ways: delete it, or run the test in CI. This item takes the second
route, which adds genuine automated checks and is the one that leaves the project stronger. It does
**not**, on its own, make the test a substantive guard of the determinism boundary — P0.1 records the
test as a tautological attribute-presence check, and replacing it with a real import-plus-mutation
check is later-phase work (`CURRENT-STATE-AUDIT.md:453`).

### Work items — technical evidence layer

Current state, verified:

- No CI configuration exists anywhere. No `.github/`, no workflow file, no `.gitlab-ci.yml`, no
  `Jenkinsfile`, no `.circleci/`. Neither file listing contains a CI artefact of any kind. *(Two
  counts circulate and must not be used interchangeably: `git ls-files | wc -l` → **55** tracked
  files; `find . -type f -not -path "./.git/*" | wc -l` → **71** total as at 19 July 2026, the
  difference being untracked Phase B working documents under `docs/`. An earlier draft of this plan
  described 55 as an exhaustive listing of the tree, which is no longer true. See
  `CORRECTIVE-BACKLOG.md` CB-23 and CB-27.)*
- The only YAML in the entire project is `scaffold/docker-compose.yml`.
- No linter and no type checker is configured: no `ruff.toml`/`.ruff.toml`, no `mypy.ini`, no
  `setup.cfg`, no `tox.ini`. `.gitignore:16-18` nevertheless pre-ignores `.mypy_cache/` and
  `.ruff_cache/` — the ignore entries anticipate tooling that is not present.
- Version control **does** now exist: one commit `71fa329` ("Initial commit: MERIDIAN scaffold,
  charter, and current-state audit"), branch `main`, working tree clean of modifications to tracked
  files (the Phase B draft records, including this plan, are present as untracked files under
  `docs/`), remote `origin` at `https://github.com/CypherTechAries/project-meridian.git`. This
  satisfies the `git init` half of the audit's Phase 1 (`CURRENT-STATE-AUDIT.md:441`).

Work: add a workflow that installs from whatever P0.2 settles on and runs `pytest`. Add `ruff` and
`mypy` **only if** they are configured and passing — adding a check that is allowed to fail is worse
than adding none. Add `.dockerignore`.

### Testable exit criterion

Both, adapted from `CURRENT-STATE-AUDIT.md:446`:

1. CI is green on a trivial pull request.
2. CI is demonstrably **red** when a named test is deliberately broken. Demonstrate this in the PR
   that adds the workflow.
   *Attribution note: the audit's wording at `:446` is "demonstrably red when **the determinism
   test** is deliberately broken", and in the audit's own vocabulary "the determinism test" is
   `test_same_seed_is_deterministic` — it is named separately from the boundary test at `:453` and
   `:457`. This plan proposes demonstrating red on `test_llm_gateway_cannot_write_state` **as well**,
   since that is the test `CHARTER.md:44` claims is guarded and B2's corrected wording will rest on
   it. That extension is the drafter's proposal, not the audit's requirement.*

Criterion 2 is the one that matters. A green CI proves nothing about whether it is checking anything.

### Owner decision

**OQ-5 — remote-side controls.** `CURRENT-STATE-AUDIT.md:444` requires "the default branch is
protected with a required status check". Branch protection, CODEOWNERS and secret scanning are
settings on the GitHub remote, not files in the tree. Their current state was **not verified** —
no `gh` or network command was run, per the standing constraint. There is no CODEOWNERS file in the
local tree. The owner needs to confirm or configure these directly.

---

## P0.4 — Define the authoritative-state contract

> *"Define the authoritative-state contract across macro/meso/micro."* — `HANDOFF.md:75`

**Blocked on an owner decision:** No.
**Dependencies:** None to start. **P0.4A, P0.5, P0.6 and P0.7 are treated here as depending on this**,
on the reasoning that you cannot design causal channels between tiers, snapshot state for replay,
define what a tick advances, or decide what a randomness stream is keyed to, without first agreeing
what "the state" is.

> **This dependency is the drafter's inference, not a founder statement.** `HANDOFF.md` § Phase 0 priority order (`:75-89`) gives
> the text of P0.4 to P0.7 and asserts no dependency between them; the P0.4→P0.5 link in particular is
> derived from list ordering plus the reasoning above and nothing more. `RAID-REGISTER.md` D3 records
> it the same way and calls it the weakest link in its dependency table. The only near-explicit
> sequencing constraint in HANDOFF is D4 (nothing touches saturation before P0.7, `HANDOFF.md` § Phase 0 priority order (`:89`)).
>
> The P0.4 → **P0.4A** link is inferred the same way, from the founder's placement of P0.4A between
> P0.4 and P0.5. What the 18 July decision states *explicitly* is what P0.4A **blocks** — P0.5
> implementation, entity promotion, world-model materialisation — not what it depends on. Do not cite
> the P0.4 → P0.4A link as founder-stated.

### Plain English

Write down exactly what counts as the simulation's real state — the thing that must be reproduced,
snapshotted and replayed — and what is merely derived or decorative. Right now this is implied by the
code and stated nowhere.

### Why it matters

Every later item resolves to this question. Replay is meaningless without a definition of what must
match. Cross-tier causality is unspecifiable without a definition of what each tier owns.

### Work items — technical evidence layer

The contract must be written against observed behaviour, which is currently this:

**Macro.** A single mutable Pydantic `MacroState` held at `MacroStateHolder.state`
(`macro_state.py:21`), constructed once at model init (`engine.py:91-93`, builder at `:46-69`).
Exactly three write paths exist, all in `engine.py`: seeded noise via `apply_deltas` (`:136`), action
deltas via `apply_deltas` (`:164`), and a direct field assignment `self.macro.state.tick = self.tick`
(`:179`). No other module calls `apply_deltas`.

**Meso.** `CohortAgent.cohort`. Exactly **one** field of it is ever written anywhere:
`beliefs.government_competence`, decremented in `CohortAgent.step` (`cohort_agent.py:35-38`). The
other four belief fields defined at `agent_schema.py:56-69` are written by nothing and read by
nothing. A second, meso-adjacent structure `self.narrative_adoption` (`engine.py:112`) is wholesale
replaced each tick (`engine.py:143-145`) and is not part of any `Cohort` object.

**Micro.** There is **no authoritative micro state.** `InstitutionalAgent` writes exactly one
attribute, `self.last_proposal` (`institutional_agent.py:24`, `:38`), overwritten every tick. No field
of the `MicroAgent` spec (`agent_schema.py:154-184`) — beliefs, resources, political capital, memory,
relationships — is written by any code path.

**History.** Macro carries none; the live object is mutated in place. History exists only as
`self.snapshots`, a list of `model_dump()` dicts appended once per tick plus one at construction
(`engine.py:116`, `:180`).

The contract must also record these observed properties, because a contract that omits them will be
contradicted by the code on day one:

- `apply_deltas` **silently skips** unknown keys (`macro_state.py:36-38`) and any value that is not a
  top-level scalar (`:39-41`). A misspelled or nested indicator produces no error, no warning and no
  effect (A3 §1 sub-finding).
- The three nested blocks — `institutional_trust`, `alliance_confidence`, `public_finances`
  (`macro_schema.py:52-54`, `:58-60`, `:70`) — are therefore **structurally unreachable** through the
  only delta path.
- Clamping is applied to a hard-coded set: four keys clamped to [0,1] plus `fuel_reserve_days` floored
  at 0 (`macro_state.py:30-35`, `:43-46`). `inflation_rate`, `unemployment_rate`, `gdp_growth_qoq` and
  `foreign_direct_investment_flow` are written unbounded (`:47`).
- `shipping_throughput_pct_of_baseline` is clamped by the engine to an upper bound of 1.0
  (`macro_state.py:33-34`, `:43-44`) while its schema declares only `ge=0` with no upper bound
  (`macro_schema.py:46-48`) — the engine imposes a ceiling the schema does not.
- *(Inferred, not executed)* `macro_schema.py` contains no `model_config`, so Pydantic v2
  `validate_assignment` is at its default (off), and the plain `setattr` at `macro_state.py:47` does
  not enforce the schema's own `ge`/`le` constraints. The engine's `bounded` set is the only bound.
- Nothing is written to the database, ever (see P0.1 Group C). The in-process `_RUNS` dict
  (`api/runs.py:18`) is the whole of run storage and does not survive process restart.
- No state hash exists: `hashlib` has zero occurrences across `backend/app`, `scenarios` and
  `schemas`. Neither does RNG-state capture (`getstate`: zero occurrences). Nothing validates against
  the nine published JSON Schema mirrors either (`jsonschema`: zero occurrences).

### Testable exit criterion

A written contract document exists that, for each of macro / meso / micro, names: (a) which fields are
authoritative, (b) which are derived, (c) which are declared-but-inert, (d) the single permitted write
path, and (e) the bounding rules.

The document is testable when a reviewer can take any field in `agent_schema.py` or `macro_schema.py`
and find it classified in exactly one of those categories, with no field unclassified. That check can
be mechanised: enumerate every Pydantic field in both schema modules and assert each appears once in
the contract's field table.

---

## P0.4A — Establish deterministic randomness architecture

> *Founder decision, 18 July 2026.* The RNG-isolation problem is its own Phase 0 workstream. It is
> not a detail of the world model and it must not be hidden inside replay. It is lettered rather
> than numbered so that the founder-set numbering P0.1→P0.8 survives unchanged.

**Blocked on an owner decision:** No — the workstream itself is founder-directed. The *approach* is
an ADR that the owner must ratify, and there is a new behaviour-line question at OQ-9.
**Dependencies:** **P0.4.** Streams are keyed to subsystems, entities and interactions, so what
counts as an entity and which state is authoritative has to be settled first.

### The sequencing rule — stated here because it governs everything after it

**P0.5 *specification* may proceed in parallel, now, before P0.4A is implemented.**

**None of the following may begin until P0.4A passes:**

- P0.5 **implementation** — building the cross-tier causal channels;
- **entity promotion** — expanding a background person into a detailed individual
  ([`FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md), *The
  scale problem*);
- **world-model materialisation** — instantiating any persistent entity population.

The reason is stated in the founder's own governing statement, which every record touching this
item must carry:

> "Materialising a background citizen must not change tomorrow's weather, market behaviour,
> government approval or another person's decision merely because it consumed extra draws."

Building any of those three on top of a single shared stream would make the resulting behaviour
uninterpretable: a genuine causal effect and a draw-order artefact would be indistinguishable, which
is precisely the confusion A3 had to untangle at `A3-VERIFICATION-RESULTS.md:142-175`.

### Plain English

The simulation currently pulls all its random numbers from one queue, in whatever order the code
happens to ask. That means adding, removing or reordering a single random draw anywhere shifts every
number drawn after it, everywhere else. Two runs can differ for reasons that have nothing to do with
the model.

This item's job is to replace that with compartmentalised randomness: each subsystem, each entity,
each relationship or interaction and each distinct purpose would draw from its own isolated stream, so
that what happens in one compartment cannot leak into another. The item must also write down which of
the two reasonable ways of doing that MERIDIAN adopts, and why. **None of this exists today**; this
section describes work to be done, not a property the code has.

### Why it matters

Without this, no later claim about causality can be trusted and no later claim about reproducibility
can be made honestly.

- The two critical findings turn on it. The apparent meso→macro coupling A3 found was **not**
  causality; it was one subsystem's draw count shifting another subsystem's values through the shared
  stream (`A3-VERIFICATION-RESULTS.md:156-168`).
- The world model makes it acute rather than latent. A population in which entities are promoted,
  demoted and materialised on demand consumes a *variable* number of draws by design. On a single
  shared stream, variable consumption is not an edge case — it is the normal operating mode.
- It bounds P0.6. A snapshot that captures one generator's state cannot checkpoint a stream
  architecture that does not yet exist, and the audit already records that the specified
  fork-from-any-tick behaviour would resume at position 0 and diverge silently
  (`CURRENT-STATE-AUDIT.md:259`).

### Scope — five axes of isolation, not per-entity streams alone

The founder's scope statement requires isolation by **all** of:

| Axis | What it separates |
|---|---|
| Subsystem | macro, meso/cohort, diffusion, micro/institutional, and any later subsystem |
| Entity | each person, organisation, business, community, institution or state |
| Relationship or interaction | a draw about the A→B tie, distinct from draws about A and about B |
| Simulation purpose | e.g. a person's profile generation, distinct from that person's per-tick decision |
| Tick or event context | where appropriate, so a repeated event resolves identically |

**Per-entity streams alone are insufficient** and must not be treated as satisfying this item. An
entity that draws for two different purposes on one per-entity stream reintroduces the same
order-dependence at smaller scale.

### The ADR — required, and what it must decide

An ADR is required because at least two valid architectures exist:

1. **Stateful named substreams** — a derived generator per key, each carrying its own position.
2. **Keyed / counter-based deterministic draws** — a stateless function of (root seed, key, counter)
   producing the draw, with no per-stream position to keep.

The ADR must select one **deliberately**, with reasons, and must **explicitly reject** ordinary
sequential calls to a single shared PRNG for authoritative behaviour. That rejection is not
rhetorical: it is the currently accepted position. `scaffold/docs/ARCHITECTURE_DECISIONS.md:60-67`
(ADR-007, *Reproducibility: one seed, threaded everywhere*, Status: Accepted) states that "all
engine, agent, and diffusion randomness draws from that one RNG". P0.4A's ADR therefore supersedes
ADR-007, and ADR-007's status has to be changed rather than left standing alongside it.

Use [`ADR-TEMPLATE.md`](ADR-TEMPLATE.md). Ratification is the owner's; an agent may draft it.

> **A draft now exists, and it is only a draft.**
> [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
> was written on 19 July 2026 against that template. **Status: Proposed. Drafted by an AI agent.
> Approval block empty. It carries no authority and nothing may be built on it.** It recommends
> option 2 above — keyed / counter-based deterministic draws — and states the required explicit
> rejection of sequential shared-PRNG use for authoritative behaviour. Recommending is not
> selecting: exit criterion `P0.4A-ADR` is not met until the owner signs it
> (`PUBLICATION-EXIT-CRITERIA.md` §C8A).
>
> **One divergence to resolve, not resolved here.** The paragraph above states that the P0.4A ADR
> *supersedes* ADR-007. ADR-010 as drafted records "Supersedes: None" and treats ADR-007 as narrowed
> rather than superseded. That is an owner question — `PUBLICATION-EXIT-CRITERIA.md` open question 15
> and `RAID-REGISTER.md` DEC8 — and no agent may close it.

### Work items — technical evidence layer

Current state, verified by reading source:

- **One generator, no substreams.** Exactly one `random.Random` exists in application code,
  `self.rng = random.Random(resolved_seed)` at `engine.py:83`, commented "the ONLY source of engine
  randomness". Every draw site is on it: `cohort_agent.py:36`, `diffusion.py:75`, `engine.py:135` —
  all `uniform`, all one stream.
- **Draw order is load-bearing and undocumented as such.** Per tick: all cohort drift draws in list
  order, skipping grievance-free cohorts (`engine.py:152`); then all diffusion jitter draws in graph
  node order (`engine.py:156`); then exactly one macro noise draw (`engine.py:176`). The skip at
  `cohort_agent.py:35` (`if self.cohort.grievances:`) is what makes consumption
  scenario-content-dependent.
- **No draw is recorded.** Stream, index, distribution, parameters and value are all discarded at the
  three draw sites (`CURRENT-STATE-AUDIT.md:304`, item 17). There is therefore no way today to
  attribute an outcome to a subsystem, an entity or a purpose — exit criterion 9 has no substrate
  yet.
- **A second, differently-seeded generator exists.** `super().__init__(seed=resolved_seed)`
  (`engine.py:82`) is inert on mesa 2.4.0, which seeds in `Model.__new__`; on the API path Mesa's
  `self.random` is seeded from entropy. Nothing reads it today, and a one-character typo
  (`self.model.random` for `self.model.rng`) would break reproducibility silently
  (`CURRENT-STATE-AUDIT.md:319`, item 27).
- **No RNG state is captured anywhere.** `getstate`: zero occurrences across `backend/app`. No state
  hash either — `hashlib`: zero occurrences.
- **The audit already logged the defect at low severity.** `CURRENT-STATE-AUDIT.md:320` (item 28)
  records "One shared RNG stream, no named substreams" and judges it "not currently a defect (the
  design is documented as one RNG in ADR-007)". A3 demonstrated it, and this founder decision
  re-rates it. The audit's assessment is superseded, not contradicted on the facts.

The work itself:

1. Draft and obtain ratification of the ADR above.
2. Specify the key scheme — the identifier shape for subsystem, entity, relationship/interaction,
   purpose and tick/event context, and how they compose into a stream key.
3. Specify how streams are obtained, such that no subsystem can reach the root generator.
4. Specify what the run records about randomness: algorithm, version, root seed, and the key
   vocabulary in use.
5. Specify the isolation test suite required by criterion 10.
6. Record the migration consequence for ADR-007 and for any P0.1 wording that describes MERIDIAN's
   randomness as a single threaded seed.

### Testable exit criterion

All ten of the founder's criteria, each stated as something a test or a mechanical check can decide.
The item passes only when all ten pass.

| # | Criterion | How it is decided |
|---|---|---|
| 1 | No authoritative code calls the global `random` API directly | Static check over the authoritative packages: no `import random` used for module-level `random.*` draw calls, no `from random import …`. Zero hits required, with an explicit allow-list of any non-authoritative helper |
| 2 | No subsystem receives unrestricted access to the root generator | The root generator is reachable by exactly one factory; a test asserts that a subsystem handle exposes only its own stream and cannot obtain the root. Mechanically: the root object has one reference site |
| 3 | Stream keys use stable identifiers, **not** Python's process-randomised `hash()` | Grep for `hash(` in key construction returns zero. Stronger: two runs under different `PYTHONHASHSEED` values produce identical stream keys and identical results |
| 4 | The run records the RNG algorithm and version | A completed run's recorded metadata contains a non-empty algorithm name and version; a test asserts the fields are present and non-default |
| 5 | Adding an unrelated entity does not alter unrelated subsystem results | Run A; run B identical but with one extra entity that no channel connects to the subsystem under test; assert that subsystem's outputs are byte-identical |
| 6 | Promoting one background person does not alter previously established entities | Run to tick *n*, promote one background person, continue; assert every previously established entity's state matches the control run in which no promotion occurred |
| 7 | Reordering entity iteration does not alter outcomes where the model declares order irrelevant | For each subsystem the contract marks order-irrelevant, reverse or shuffle iteration order and assert identical outputs. Subsystems that declare order *relevant* are excluded by name, not by silence |
| 8 | Repeating the same promotion event produces the same profile and history | Promote the same person from the same state twice in separate processes; assert the generated profile and life history are identical field for field |
| 9 | Every random outcome can be associated with a subsystem, entity or interaction, and a purpose | Every draw carries its key; a test enumerates the draws of a run and asserts none has a null or unattributed key |
| 10 | Injecting extra draws into one stream leaves other streams unchanged | The direct isolation test: take a control run, deliberately consume *k* additional draws from one named stream, and assert every other stream's sequence and every dependent output is unchanged |

Criterion 10 is the one that matters, and it is the one that does not exist today in any form.

### The existing determinism test is insufficient — this item requires isolation tests

`test_same_seed_is_deterministic` (`test_engine.py:34`) is a **same-seed repetition** test: it runs
the model twice at one seed and compares the final macro dict. That shape of test cannot detect
draw-order contamination, because contamination does not break same-seed repetition — both runs
consume the draws in the same order, so both agree.

A3 states the consequence directly: the no-substreams defect "means the existing determinism test
would mask such a change as 'expected divergence'"
(`A3-VERIFICATION-RESULTS.md:170-175`, the *New defect exposed* paragraph in §6). The audit records
the same shape of blindness from the other side: injecting global randomness into `CohortAgent.step`
leaves macro equality **True** while cohort beliefs diverge, and reversing cohort order leaves macro
byte-identical while all meso output changes — "the named guardrail test stays green through both"
(`CURRENT-STATE-AUDIT.md:140`).

**P0.4A therefore requires isolation tests, not merely same-seed repetition tests.** Passing
`test_same_seed_is_deterministic` is not evidence for any of the ten criteria above, and no record
may cite it as such. Criteria 5, 6, 7 and 10 are all differential tests between two *different* runs;
that is the structural difference.

### What is blocked on P0.4A

| Blocked | Why |
|---|---|
| P0.5 **implementation** | A channel built on a shared stream cannot be distinguished from contamination, which is the exact failure A3 diagnosed. P0.5's own exit criterion already depends on freezing substreams — see the "with the RNG substreams frozen" clause in §P0.5 |
| Entity promotion | Promotion consumes a variable number of draws; on a shared stream it perturbs everything downstream. Criteria 6 and 8 exist for this |
| World-model materialisation | Same reason at population scale, and it is the case the founder's governing statement names |
| P0.6 replay | RNG state capture and the fork-from-any-tick behaviour claimed at `ADR-003:31-32` are both defined against the stream architecture. Specifying the snapshot before the architecture would specify the wrong snapshot |

**Not blocked:** P0.5 specification, P0.1, P0.2, P0.3, P0.7 and P0.8, all of which may proceed in
parallel.

### Owner decision

**OQ-9 — the behaviour line.** §2 of this plan states that Phase 0 changes no simulation behaviour.
Before this amendment it marked only P0.6 as a boundary case; §2 now lists P0.4A alongside it, because
P0.4A is the sharper of the two: any of the architectures above will change which number a given draw
returns, so **numeric outputs at an
unchanged seed will change** when it lands. That is unavoidable, not a defect, and it is not the
prohibited kind of change — it is not modifying behaviour to make a finding disappear
(`HANDOFF.md` § Standing constraints (`:136`)). But it does affect determinism and authoritative state, which sits on the
human-approval list at `HANDOFF.md` § Standing constraints (`:139-140`). The owner should rule on how P0.4A's numeric change is
authorised and recorded — in particular whether the pre-change tested values are captured as a
superseded baseline before the switch, so that the change is documented rather than merely absorbed.
This plan does not assume an answer. Related: **OQ-6** (Mesa) now bears on this item first and on
P0.5 second.

---

## P0.5 — Design explicit cross-tier causal channels

> *"Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` must
> affect aggregation."* — `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-85`)
> *Founder annotation: "this is arguably the highest-value item, since it is the product's core
> mechanism, not a tidiness fix."*

**Blocked on an owner decision:** Not directly. Interacts with decision 8.3 (Mesa) — see OQ-6.
**Dependencies:** **P0.4** (cannot specify channels between undefined states) — **inferred, not
documented**; see the note under P0.4 and `RAID-REGISTER.md` D3. **P0.4A for implementation only.**

> **Split dependency, founder-stated 18 July 2026.** This item's **specification may proceed in
> parallel now**, before P0.4A is implemented. This item's **implementation may not begin until
> P0.4A passes.** See the sequencing rule in §P0.4A. Nothing below authorises implementation.

### Plain English

The three tiers are supposed to influence each other — that is the entire product. They do not. Worse,
they *appear* to, and the appearance is an accident. This item designs how they should connect. It
does not build it.

### Why it matters

`CHARTER.md:37-40` states the governing principle that every material outcome must be traceable to
world state, rules, incentives, constraints, network effects or seeded stochastic resolution.
`CHARTER.md:25` promises "Every action creates second- and third-order effects." Neither is true of a
system whose tiers are causally disconnected. This is the gap between the charter and the code that is
not a wording problem.

### Why it must be a design, not an implementation, in Phase 0

Building the channels changes numeric outputs. That is the critical behavioural finding
(`A3-VERIFICATION-RESULTS.md:142-175`), and it is later-phase. Phase 0 produces the specification the
later phase implements.

### Work items — technical evidence layer

**The observed disconnection.** A3 perturbation tests at seed 88213, 40 ticks
(`A3-VERIFICATION-RESULTS.md:147-168`): hammering macro left cohort beliefs and narrative adoption
unchanged; setting cohort beliefs to 0.01 left macro unchanged. Two perturbations *did* move macro —
adding a grievance to the one cohort that had none, and deleting a cohort — and those are the
misleading ones.

**Why they are misleading.** `cohort_agent.py:35` guards the RNG draw with `if self.cohort.grievances:`,
so a cohort with no grievances consumes zero draws. Changing how many cohorts have grievances changes
how many draws are consumed before the macro noise draw in the same tick, shifting every later value in
the shared stream. Verified draw sites, all `uniform`, all on one stream: `cohort_agent.py:36`,
`diffusion.py:75`, `engine.py:135`. Verified per-tick order: all cohort drift draws in list order
(skipping grievance-free cohorts), then all diffusion jitter draws in graph node order, then exactly one
macro noise draw (`engine.py:152`, `:156`, `:176`).

**The named-substream defect.** There is exactly one `random.Random` instance in application code
(`engine.py:83`) and no named substreams. A3 flags this as a latent reproducibility hazard: any future
change to cohort logic perturbs macro results for reasons unrelated to the model, and the existing
determinism test would mask it as expected divergence (`A3-VERIFICATION-RESULTS.md:170-175`).

> **Superseded by founder decision, 18 July 2026.** An earlier draft of this plan raised
> per-subsystem substreams here as a *recommendation for owner ratification*. That framing is now
> wrong. The randomness architecture is a founder-directed Phase 0 workstream in its own right —
> **P0.4A** — with a required ADR, a five-axis isolation scope wider than per-subsystem substreams,
> and ten exit criteria. It is no longer this item's recommendation to make, and P0.5 must not
> restate it as an open choice. What survives from the original reasoning is the *justification*,
> which P0.4A carries: without isolation, the causal channels this item specifies will be
> indistinguishable from stream contamination once they are built. **OQ-6** (Mesa) still applies, but
> now bears on P0.4A first.

Each channel this item specifies must therefore name the stream it draws from in P0.4A's key
vocabulary. Where P0.4A's ADR is not yet ratified, the channel names the *purpose* the draw serves
and leaves the concrete key to be filled in — it does not invent a parallel scheme.

**`represents_population`.** The founder note requires it to affect aggregation. Observed: it is
declared at `agent_schema.py:95`, populated in the demo scenario at `kestral-strait.json:39, 79, 122,
162, 202`, and read by no code. It does not enter the diffusion graph — `build_cohort_graph`
(`diffusion.py:18-37`) uses only `cohort_id`, `internal_cohesion` and `bridges_to`. It does not enter
`cohort_agent.step` or any aggregation, because no aggregation exists.

**Other inert inputs the design should account for.** `self.campaign` — the scenario's
`hidden_campaign` block, populated at `kestral-strait.json:389-418` — is assigned at `engine.py:111`
and read by nothing; the `Campaign` model is never instantiated, so the block is never even validated.
`income_sensitivity_to_shipping_disruption` (`agent_schema.py:36`) has no read site. The full
susceptibility model collapses to one unweighted mean of three appeals (`cohort_agent.py:22-26`).

**"No arbitrary coupling"** — the founder's constraint. Each proposed channel should name the
real-world mechanism it represents, per `CHARTER.md:52` ("Grounded in recognised real-world
mechanisms — named, citable, and inspectable"), and should be answerable against the eight-question
standard at `CHARTER.md:118-127`.

### Testable exit criterion

A design document exists in which every proposed cross-tier channel specifies: source tier and field,
destination tier and field, the named real-world mechanism, the update rule's shape, and the RNG
substream it draws from (if any).

Mechanically testable at design stage: for each channel, the document states an observable
perturbation test that the future implementation must pass — of the form "change X by Δ, and Y must
move; change X by Δ with the RNG substreams frozen, and Y must **still** move." That second half is
what distinguishes a real channel from the contamination A3 found. The A3 method
(`docs/delivery/evidence/a3_rng_isolation.py`) is the template.

### Owner decisions

**OQ-1 — sequencing.** The founder annotation says P0.5 is arguably the highest-value item. This plan
has not reordered on that basis. The owner should rule: keep P0.1→P0.8 as ordered, or promote P0.5.
Note the constraint if promoted: P0.5 depends on P0.4, so promoting P0.5 means promoting P0.4 with it,
and neither can precede P0.1 without leaving false claims live while new design work is layered on top.
*Narrowed 18 July 2026:* only P0.5's **specification** is promotable at all. Its implementation sits
behind P0.4A by founder decision and cannot be moved ahead of it — and the specification is already
authorised to run in parallel, so promotion is no longer required to unblock it. See §4.

**OQ-6 — decision 8.3 (Mesa), still open.** *Now bears on **P0.4A** primarily, and on this item
second, since P0.4A is where the randomness architecture is chosen.* The stream design interacts with
it. Mesa is currently
a vestigial base class: no scheduler, no `AgentSet`, no `shuffle`, plain-list iteration at
`engine.py:152` and `:159`. Two RNGs are seeded at construction from the same resolved seed
(`engine.py:81-83`), and no application code reads mesa's `self.random` (zero hits across
`scaffold/backend/app`). The audit records that Mesa materialises a second `random.Random` seeded from
entropy on the API path, and introduces a `Model.rng` collision on any 3.x upgrade
(`CURRENT-STATE-AUDIT.md:405`). Designing named substreams while the substrate question is open risks
designing against a base class that may be removed.

---

## P0.6 — Repair event, snapshot and replay foundations

> *"Repair event, snapshot and replay foundations. Central transition mechanism, full snapshots,
> replay makes zero model/network calls."* — `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`)

**Blocked on an owner decision:** No, but see OQ-7 on scope.
**Dependencies:** **P0.4** (a snapshot cannot be "full" against an undefined state) and **P0.4A** (a
snapshot cannot capture randomness state until the randomness architecture is chosen — capturing one
generator's position would be the wrong checkpoint for either architecture in P0.4A's ADR). Benefits
from P0.3 (a replay test is only a guard if CI runs it).

### Plain English

Recording what happened, saving the state, and being able to re-run it and get the same result. Only
fragments of that exist today: events *are* logged every tick, but as unvalidated dicts with at least
one gap; state snapshots *do* exist, but cover macro only and live in memory; and replay does not
exist at all. The hard requirement from the founder is that a replay must not call a model or the
network at all — if it does, it is not a replay, it is a re-run.

### Why it matters

This is the item that converts the target reproducibility contract (`HANDOFF.md:61-62`) from aspiration
into something that could eventually be claimed. Until then, the permitted claim is the narrow one at
`HANDOFF.md:56-57`, and no document may say otherwise.

### Work items — technical evidence layer

**Events.** Event entries are raw dicts, never validated against the `Event` schema
(`agent_schema.py:211-229`). The engine appends at `engine.py:165-173`; the decision endpoint appends a
differently-shaped dict at `routes_simulation.py:91-100` that carries an `intervention` key `Event` does
not define and omits `visibility` and `causal_parents` which it does. The engine's append is also
conditional: `if deltas:` at `engine.py:163` means the `observe` action — mapped to an empty dict at
`engine.py:42`, which is falsy — produces **no event-log record at all**.

**The player path is a no-op.** `POST /runs/{id}/decision` appends a raw dict to the in-memory
`event_log` and returns `{"accepted": True}` unconditionally (`routes_simulation.py:80-101`, effects
hard-coded to `[]` at `:97`). It never calls `_validate_and_price` or `apply_deltas`. A submitted
decision cannot influence any later tick, because `step()` never reads `event_log` (`engine.py:147-180`
— `event_log` appears only as an append target at `:165`). Four stored fields are read by nothing:
`legal_check`, `resource_cost`, `timeline_days`, `second_order_hooks` (`agent_schema.py:232-250`).
`actor_role` is free-form and is not checked against the scenario's institutional agents.

**Snapshots.** `self.snapshots` holds `model_dump()` of macro only (`macro_state.py:49-51`,
`engine.py:116`, `:180`). Meso state, `narrative_adoption`, the event log and RNG state are all absent.
There is no RNG-state capture anywhere (`getstate`: zero occurrences) and no state hash (`hashlib`:
zero occurrences).

**Central transition mechanism.** There is none. Within the institutional loop there is no collection
or arbitration phase — each agent's delta is priced and applied to macro immediately inside the loop
before the next agent steps (`engine.py:159-164`), and `_validate_and_price` receives only the proposal
(`engine.py:121`), never sibling proposals, the agent spec, or current macro state.

**Two uncoordinated drivers.** The WebSocket endpoint calls `model.step()` directly in a client-driven
loop (`routes_ws.py:41-46`) while the REST route calls `model.run(req.ticks)`
(`routes_simulation.py:59`). Both resolve the same shared in-memory model object via `runs.get_run`
(`api/runs.py:38-40`) with no locking. Any transition mechanism must account for both.

**Persistence.** Zero rows are written (see P0.1 Group C). Phase 0's obligation here is the *documentary*
correction (B3); building the write path is later-phase.

### Testable exit criterion

**These criteria are conditional on the OQ-7 ruling, and this plan does not pre-empt it.** The three
criteria below are the *end-state* test. Note their provenance: criterion 1 is the audit's **Phase 2**
exit criterion (`CURRENT-STATE-AUDIT.md:458`), not a Phase 0 one, and is reproduced here rather than
silently promoted.

**If the owner rules OQ-7(b), implementation**, P0.6's Phase 0 exit is all three of:

1. A run recorded **with a non-deterministic stub** and then replayed produces byte-identical macro
   **and** meso **and** event-log state (`CURRENT-STATE-AUDIT.md:458`). The non-deterministic-stub
   qualifier is the audit's and is load-bearing: with the current fixed stub, a re-run is
   indistinguishable from a replay, which is exactly the false comfort this item exists to remove.
   Meeting this would require a state hash, which does not exist today; whether introducing one falls
   inside Phase 0 is itself part of OQ-7.
2. Every state-mutating path goes through the central transition mechanism. Mechanically checkable:
   `apply_deltas` and any direct authoritative-field assignment have exactly one call site each, inside
   that mechanism. *(Today: three write paths, `engine.py:136`, `:164`, `:179`, plus meso at
   `cohort_agent.py:35-38`.)*
3. **Replay makes zero model and zero network calls.** Testable by substituting the gateway module with
   an object that raises on any attribute access, and asserting the replay completes and its hashes
   match. If the replay touches the gateway, the test fails. This is stronger than mocking a return
   value, because it fails on *any* contact rather than on a wrong answer.

**If the owner rules OQ-7(a), design and specification only**, none of the three is meetable in
Phase 0, and the Phase 0 exit is instead — mirroring P0.5's pattern — a written specification from
which criteria 1-3 can later be implemented unchanged: it must name the full snapshot contents
(including RNG state), the hash construction, the single permitted write path, and the
gateway-substitution test, in enough detail that the later-phase implementer adds no new design
decisions.

### Owner decision

**OQ-7 — scope boundary.** P0.6 says "repair", which implies code change. A central transition
mechanism is a refactor of the authoritative write path. Introducing a state hash is additive and
read-only; consolidating the write paths is not, and even a behaviour-preserving refactor of the write
order could change numeric output through the shared RNG stream (see P0.4A, and OQ-9 there). The
owner should rule
whether P0.6 in Phase 0 means (a) design and specification only, with implementation in a later phase,
or (b) implementation, accepting that it needs the same approval gate as any determinism-affecting
change under `HANDOFF.md` § Standing constraints (`:139-140`). This plan does not assume either.

---

## P0.7 — Define simulation time and horizon

> *"Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion."*
> — `HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`)

**Blocked on an owner decision:** No.
**Dependencies:** **P0.4.** Also constrains later-phase work: nothing may touch saturation until this
item's output exists.

### Plain English

Nobody has written down what a tick *is*. An hour? A day? A quarter? Until that is decided, no
statement about how fast anything should change can be checked, because there is no unit to check it
against. And the tempting quick fix for the runaway indicators — pulling them back toward a baseline —
is explicitly forbidden, because it would fake a mechanism instead of building one.

### Why it matters

A3 escalated the saturation finding from calibration to architecture
(`A3-VERIFICATION-RESULTS.md:202-204`): "No amount of tuning the existing numbers fixes it, because
there is no mechanism to tune." A3 then repeats the founder's ordering: "Per P0.7 it must not be patched
with arbitrary mean reversion; tick semantics and horizon come first."

### The ordering constraint, stated as a rule

**No change to any saturation-related quantity — clamp bounds, `ACTION_EFFECTS` magnitudes, noise
ranges, or any new decay term — may be made until P0.7's output exists and is approved.** Mean reversion
toward a baseline is specifically forbidden as a patch. It would produce plausible-looking curves with no
causal account, which is precisely what `CHARTER.md:129-130` rules out: "If the system cannot answer these
questions, the output is flavour text, and flavour text must not be allowed to modify the simulation."

### Work items — technical evidence layer

The definition must be written against these observed facts:

- **Nothing defines what a tick represents.** The tick is an integer incremented at `engine.py:149` and
  stamped onto macro state at `:179`. No unit, no calendar, no duration.
- **The engine contains no opposing mechanism of any kind.** A3 §7 checked the source directly: the
  strings `cost`, `cooldown`, `decay`, `budget`, `resource`, `prerequisite` and `revert` all return
  False for `engine.py` (`A3-VERIFICATION-RESULTS.md:192-200`).
- **Saturation is not a stub artefact.** A3 tested varied action selection — what a real model would
  produce — and `military_readiness` and `social_stability_index` still pin at a clamp bound after 120
  ticks in both modes (`A3-VERIFICATION-RESULTS.md:182-187`).
- **The drift is structurally one-directional.** *(Inferred from source, not executed:)* the stub maps
  all six scenario roles to a non-`observe` action (`llm_gateway.py:43-51`; the six agents at
  `kestral-strait.json:243, 266, 298, 320, 345, 367`), and every one of those `ACTION_EFFECTS` entries
  (`engine.py:35-43`) is non-negative on the three keys it touches. So the summed per-tick delta is
  non-negative by construction, and the clamp is the only thing that ever stops it.
- **`ACTION_EFFECTS` touches only three keys** — `military_readiness`, `government_approval`,
  `social_stability_index`. No fiscal, economic, alliance or trust key appears in it at all
  (`engine.py:35-43`; corroborated by A3 §1's executed key dump).
- **`Intervention.timeline_days` ("Days until the action takes effect") is never read**
  (`A3-VERIFICATION-RESULTS.md:118`), which is the closest thing in the schema to a time semantic and is
  inert. The scenario constrains the defence minister with `procurement_law_18mo_minimum`, and the engine
  applies `request_procurement_acceleration` immediately with no delay
  (`A3-VERIFICATION-RESULTS.md:107-116`) — an 18-month statutory floor in a system with no concept of a
  month.
- **There are no terminal semantics at all**: per the A3 correction list (`:224`), `run(400)` completes
  with nothing evaluating win or loss.

### Testable exit criterion

A written definition exists that states: what one tick represents in world time; the default and maximum
horizon of a scenario run; what "the run ended" means and what evaluates it; and, for each authoritative
indicator, the time-scale on which it is expected to move.

Testable as a gate on later work: any later-phase pull request that changes a clamp bound, an
`ACTION_EFFECTS` magnitude, a noise range or adds a decay term must cite the section of this definition
that justifies the magnitude. A change that cannot cite one is rejected. That is a review rule, not a
command — it should be written into the PR template so it is enforced rather than remembered.

---

## P0.8 — Review the influence-operations targeting schema, and enforce the decision taken on it

> *"Review the influence-operations targeting schema before publication."* — `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`)

> **Amended 19 July 2026 — this item changed character.** It was headed "review… blocked on an owner
> decision", and its exit was a written policy position. The founder took that decision on
> 18 July 2026. **P0.8 did not thereby complete.** The decision names eight controls and states that
> technical enforcement is mandatory while disclosure and any future acceptable-use language are
> supplementary. So the review is done and the enforcement is not started. Like §P0.4A, this section
> records a founder decision rather than a drafter's proposal: the eight controls and the
> identity/bias distinction are decided. **The verification methods proposed below are the drafter's
> and are not.** Nothing in this section authorises implementation.

**Blocked on an owner decision: NO — taken 18 July 2026.** **Blocked on implementation and
verification: YES.** This is publication blocker B5 (`A3-VERIFICATION-RESULTS.md:245`) and section 8
decision 6 (`CURRENT-STATE-AUDIT.md:411`). The framing "Four of five clear by telling the truth. Only
B5 needs a decision" (`A3-VERIFICATION-RESULTS.md:247`, restated at `HANDOFF.md` § Publication exit criteria (`:104-105`)) is **half
superseded**: the first sentence still holds for B1–B4, the second does not. B5 needed a decision, got
one, and stayed open.
**Dependencies:** None technically. Gates publication, therefore gates the P0 phase exit. Note the
change this implies for §5: P0.8 was described there as blocked on a person rather than on work, and
that is no longer true.

### Plain English

The repository contains a complete, declarative template for designing an influence campaign against a
population: who to target, what they are susceptible to, which grievance to exploit, which channels
reach them, how independent the messenger should appear, and how likely the campaign is to be detected
or attributed. It is fictional and it is inert — nothing in the code uses it. But it is a schema, and a
schema is a design, and publishing it publishes the design.

The owner has now said what terms attach. Eight of them. Seven describe things the software must do
or refuse to do, and the eighth says that writing any of it down instead of building it does not
count. **None of the eight exists in the code.** That is the whole of the remaining work on this item.

### The decision — founder, 18 July 2026

For the public MVP:

| # | Control |
|---|---|
| 1 | Influence mechanics operate **only** in explicitly fictional worlds. |
| 2 | The scenario loader **requires** `world_mode: fictional` and **fails closed** when it is missing. |
| 3 | Real-world scenario import remains **disabled**. |
| 4 | Real persons, organisations and political populations **cannot** be influence-target entities. |
| 5 | Protected characteristics **cannot** be used as optimisation criteria for persuasion or manipulation. |
| 6 | Fictional **aggregate** narrative diffusion, exposure, adoption and counter-messaging **remain allowed**. |
| 7 | API and UI **disclose** that the active world is fictional. |
| 8 | Disclosure and any future acceptable-use language are **supplementary. Technical enforcement is mandatory.** |

**The identity and bias distinction, quoted rather than paraphrased:**

> **Permitted:** identity affects lived experience, relationships, discrimination, institutional
> access, media exposure and cultural interpretation.
>
> **Not permitted:** identity acts as an inherent competence, morality, loyalty, violence or
> manipulability coefficient.

The campaign model **may** use non-sensitive factors — geography, institutional affiliation, economic
exposure, political behaviour, media consumption — where justified by the fictional scenario. It
**must not** optimise against protected traits.

**Source.** Cited by date. The decision is not a file in the tree, exactly as with P0.4A; §8 item 12
records that. `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) and § Publication exit criteria (`:104-105`) predate it and still describe B5 as awaiting a judgement.

### Why it matters

`CHARTER.md:135-142` is the entire policy: three prose bullets, unenforced. `NOTICE.md`, read in full,
contains no acceptable-use, field-of-use or dual-use restriction — it asserts all rights reserved, grants
no permission beyond GitHub's ToS, and records that licensing terms are "under review"
(`NOTICE.md:11-16`).

### What the review must consider — technical evidence layer

**What the schema can express.** The `Cohort` model (`agent_schema.py:91-109`) carries
`represents_population`, `region`, `demographics`, `economic_profile`, `media_exposure`, `beliefs`,
`grievances`, `influence_susceptibility` and `network_position`. Underneath:

- `Demographics` (`:22-28`) — median age, urban/rural, primary language, and `religion_majority`
  ("Majority religious identity label").
- `MediaExposure` (`:42-53`) — per-channel reach as five floats 0..1: state TV, local radio, short-form
  social video, messaging apps, foreign-language channels.
- `InfluenceSusceptibility` (`:72-77`) — three persuadability scalars, "How persuadable the cohort is by
  each appeal type": authority, identity, economic.
- `NetworkPosition` (`:80-88`) — `internal_cohesion` and `bridges_to`, i.e. the social-graph edges.

**What a `Campaign` can express** (`agent_schema.py:320-346`): sponsor, strategic objective,
`target_cohorts`, `existing_grievance` ("Pre-existing grievance the campaign exploits"), narrative,
messenger, channels, amplification network, trigger event, `desired_behaviour` ("Behaviour the campaign
aims to produce"), and metrics. `CampaignNarrative` (`:280-284`) pairs free-text `claim` with a
`truth_status` enum whose members are `true` / `false` / `unverified` (`:253-258`) — the schema can mark
a claim as knowingly false. `CampaignMessenger` and `AmplificationNetwork` (`:287-303`) record
`perceived_independence` ("How independent the messenger appears"), coordinated accounts, sympathetic
commentators and estimated reach. `CampaignMetrics` (`:306-318`) declares `exposure`, `belief_adoption`,
`resistance`, `detection_probability` and `attribution_probability`.

**It is published as a portable contract**, not only as internal Python:
`scaffold/schemas/campaign.schema.json` carries `$id`
`https://meridian.example/schemas/campaign.schema.json`, draft 2020-12, with a `required` list of
`campaign_id`, `sponsor`, `strategic_objective`, `narrative`, `messenger`, `amplification_network`
(`:223-235`). `narrative.schema.json` mirrors `Narrative` with per-cohort adoption and resistance.

**The demo scenario ships a fully worked example** at `kestral-strait.json:389-418`: a sponsor, an
objective, two target cohorts, an exploited grievance, a claim with `truth_status: "false"`, a messenger
at `perceived_independence: 0.8`, three channels, 40 coordinated accounts, 6 sympathetic commentators,
210,000 estimated reach, and a desired behaviour of `protest_and_parliamentary_pressure`.

**Existing safeguards, verified:**

- `CHARTER.md:135-142` — three prose bullets. Unenforced.
- No `fictional: true` assertion exists in any schema or model. A case-insensitive grep for "fictional"
  across all `.py`, `.json`, `.html` and `.js` under `scaffold/` returns exactly one hit: the scenario's
  own free-text string.
- `fiction_disclaimer` (`kestral-strait.json:7`) is read by nothing; no schema declares the field.
- No real-entity check at scenario load: `load_scenario` (`api/runs.py`) does a path-existence check then
  `json.loads`, with no name, entity or content validation.
- No JSON Schema validation library is present anywhere (`jsonschema`: zero hits), so the nine published
  mirrors validate nothing at runtime. The `Campaign` model is never instantiated, so `hidden_campaign` is
  never even shape-checked.
- No disclaimer is surfaced in any API response. All **five** REST endpoints in `routes_simulation.py`
  return without one: `create_run` (`:47-49`), `advance` (`:60`), `get_state` (`:71-77`),
  `submit_decision` (`:101`) and `get_events` (`:111`). *(An earlier draft listed four, omitting
  `submit_decision`; see `CORRECTIVE-BACKLOG.md` CB-33.)* Nor anywhere in the frontend (grep for
  fiction/provenance/AI-generated/disclaimer across `frontend/`: zero hits).
- The charter's third bullet — a visible provenance tag on AI-generated text at the interface level — has
  **no implementation**. The only marker is a literal prefix inside the stub briefing string,
  `[STUB briefing — tick {tick}]` (`llm_gateway.py:100`, within the return expression spanning
  `:99-103`; the file is 103 lines, so the `:100-104` cited in an earlier draft over-ran it); the
  "interpretive layer only" note at
  `routes_simulation.py:76` is a source comment that is never transmitted.

**Mitigating fact, stated for balance and not as an argument.** Every targeting field is currently
declarative. Twelve targeting and campaign terms (media_exposure, demographics, religion_majority,
primary_language, existing_grievance, target_cohorts, amplification_network, detection_probability,
attribution_probability, desired_behaviour, perceived_independence, truth_status) return **zero** read
sites across `backend/app/` outside the schema definition file. `self.campaign` is assigned at
`engine.py:111` and read nowhere. Diffusion spreads one anonymous adoption number linked to no `Narrative`
and no `Campaign` record (`diffusion.py:63-79`). The schema is a design, not a working capability. Whether
that changes the answer is the owner's judgement.

### The options, as the audit stated them — SUPERSEDED, retained for provenance

`CURRENT-STATE-AUDIT.md:411` listed: an explicit acceptable-use / field-of-use restriction in the
licence; an enforced `fictional: true` assertion plus a real-entity check at scenario load; surfacing
`fiction_disclaimer` in every API response and in the UI; or keeping the repository private, adding that
these "are not mutually exclusive, and the technical enforcement is worth building whichever way the
policy goes."

That list is no longer the live menu. The decision of 18 July 2026 absorbs the second and third options
into controls 2, 4 and 7 as **mandatory**, reclassifies the first as **supplementary** under control 8,
and does not adopt the fourth: remaining private is the present state under settled decision 8.2, not a
control. The audit's closing note has been overtaken — technical enforcement is not *worth building*, it
is required.

Note the interaction with settled decision 8.1: the licence decision is *no licence, all rights reserved*
(`HANDOFF.md:22-23`). An acceptable-use restriction "in the licence" therefore has no licence to sit in,
and would need its own instrument. Under control 8 that instrument would be supplementary in any case,
and would close none of controls 1 to 7.

### What is required to satisfy each control — technical evidence layer

**Nothing below exists.** Each row states a requirement and the tree's current state, which in every
case is an absence rather than partial compliance. The verification methods are the **drafter's
proposals**; the founder decision states the controls, not a criteria list of the kind P0.4A carries.
Implementation entries are `CORRECTIVE-BACKLOG.md` CB-40 to CB-47; the publication-gate form is
`PUBLICATION-EXIT-CRITERIA.md` C6.

| # | What must hold | Current state of the tree |
|---|---|---|
| 1 | Influence and diffusion code paths refuse to execute unless the world is declared fictional. A test shows refusal in the non-fictional case and normal operation in the fictional one. | No world-mode concept exists. `MeridianModel._step_diffusion` (`engine.py:138-145`) is called unconditionally from `step()` at `engine.py:156`. |
| 2 | `load_scenario` rejects `world_mode` absent, null, or any value other than `fictional`, with a typed error surfaced as a 4xx. **No default anywhere in the load path** — a default silently converts fail-closed into fail-open. | `world_mode` appears in no schema, model or scenario file. `load_scenario` (`api/runs.py:21-26`) does a path check and `json.loads`. `routes_simulation.py:43-46` catches only `FileNotFoundError`, so malformed input surfaces as a 500. |
| 3 | No code path builds a scenario from uploaded, user-supplied or remote content, and a test asserts the loader refuses paths resolving outside the vetted scenario directory. Absence of a feature is not enforcement. | No import surface found. That is an absence; nothing asserts it stays absent. |
| 4 | A load-time validation rejects real persons, organisations and political populations in influence-target positions, failing closed, with the determination method written down and not attestation alone. | No entity, name or content validation of any kind. See OQ-10. |
| 5 | The protected-characteristic list is recorded; no listed field is read by any targeting, ranking, susceptibility or campaign-effect path (call-site enumeration, not grep alone); and a test shows that changing only a protected attribute leaves targeting and effect outputs bit-identical. | `religion_majority` and `primary_language` (`agent_schema.py:22-28`) are inert. `InfluenceSusceptibility`'s three appeal scalars (`:72-77`) are **not** — they are averaged at `cohort_agent.py:22-26` and drive diffusion gain at `diffusion.py:74-76`. See OQ-11. |
| 6 | With the other seven in force, a fictional scenario still produces aggregate diffusion, exposure and adoption, and counter-messaging still moves an aggregate outcome. A **non-regression** criterion: it fails if enforcement over-blocks. | Aggregate diffusion exists (`diffusion.py:63-79`). Counter-messaging has no implementation, so this applies to it prospectively. |
| 7 | Every REST response carries an explicit world-mode / fiction field, asserted by a contract test across **all five** endpoints; and the interface displays the disclosure where a user reaches it without interaction. | No API response carries such a field (`routes_simulation.py:47-49`, `:60`, `:71-77`, `:101`, `:111`). `frontend/` holds one file with no fiction, provenance or disclaimer text. `fiction_disclaimer` is read by nothing. See OQ-12. |
| 8 | Controls 1–5 and the API half of 7 are each closed against a **test reference**. No document, disclaimer, charter bullet or acceptable-use text may be recorded as evidence closing any of them. A **review rule**, best written into the PR template. | The only safeguards are three prose bullets at `CHARTER.md:135-142`; `NOTICE.md` carries no acceptable-use term. Under control 8 those close nothing. |

**One dependency across workstreams.** Control 5's bit-identical comparison is not meaningful evidence
while every subsystem draws from one shared RNG stream, because an unrelated change in draw count moves
the numbers on its own — that is the defect P0.4A exists to fix (`A3-VERIFICATION-RESULTS.md:170-175`).
Control 5's *test* therefore depends on P0.4A passing. Control 5's *prohibition* does not wait for
anything.

### Testable exit criterion

Two parts. **Part 1 is satisfied; part 2 is not started.**

1. **Decision recorded. — DONE, 18 July 2026.** The owner's decision exists and is reproduced above.
   *(It has no source record in the repository; see OQ-13 and §8 item 12.)* No agent may amend it.
2. **Enforcement matches the decision. — NOT STARTED.** All eight rows of the table above hold, each
   evidenced as that row requires, with controls 1–5 and the API half of 7 evidenced by tests that
   exist in the suite and pass. **Drafting cannot complete this item, and neither can the decision that
   completed part 1.**

P0.8 exits only on part 2. Recording the decision moved this item from "blocked on a person" to
"blocked on engineering"; it did not move it toward completion.

---

# Track C — the interview-demonstration programme

> *Founder correction, 19 July 2026.* Track C is **not** merely a UI workstream. It has two converging
> lanes and five gates. Like the P0.4A and P0.8 decisions, this correction was issued directly and **is
> not a file in the tree**; it is cited by date. See §8 item 13.

> **Nothing in Track C is built.** Not one of the five gate screens exists. The whole of the
> front end is a 67-line development stub, `scaffold/frontend/index.html`, which titles itself
> "MERIDIAN — dev stub" (`:6`), heads itself "MERIDIAN — frontend stub" (`:16`), describes itself as a
> "Minimal dev harness" whose full UI is "left for a later build" (`:17-18`), and whose entire
> interactive surface is three buttons and a `<pre>` log element (`:20-29`). **Every gate below is a
> target with an unlock condition. No sentence in this block describes a property the code has, and
> none of it may be read as progress.**

**Track C is not a Phase 0 item, and this section does not make it one.** It is a delivery programme
that *consumes* P0 outputs. It introduces no P0.x identifier, changes no P0 numbering, alters no P0
exit criterion and adds nothing to the publication gate. The P0.1→P0.8 structure above is untouched.
What is recorded here is which P0 item unlocks which gate, so that the demonstration programme is
sequenced against the founder-set order rather than beside it.

## Why this is recorded in this document

Because Track C's endpoint depends on P0 items, and the dependency runs one way. Every claim the final
demonstration needs to make is a claim P0 exists to make true. Recording the gates anywhere else would
separate the demonstration's schedule from the work that unlocks it, which is how a demonstration comes
to be scheduled against capabilities that do not exist — the defect class this whole plan exists to
remove (`HANDOFF.md:13-19`).

## The two lanes

Track C has two lanes that converge. They must not be conflated, and neither substitutes for the other.

### Lane C-VISUAL — prototype and product communication

**Purpose.** Prototype and product communication: showing what MERIDIAN is meant to be, before the
engine can produce any of it.

**Sequencing, founder-stated.** C-VISUAL **must not wait for P0.4, P0.4A, P0.5 or P0.6**. It may
proceed on explicitly labelled fixture data once the separate UI-research handoff is received **and
reconciled**. It **can never be described as the final functioning demonstration**.

**The labelling condition, which is not optional.** Every fixture-backed surface must visibly state:

> `INTERACTIVE PROTOTYPE — FIXTURE DATA — NOT CONNECTED TO THE SIMULATION ENGINE`

and **that label must remain visible in screenshots and recordings**. The obligation therefore extends
beyond the running page to every artefact cut from it — slides, video, stills. A cropped screenshot is
the failure mode, and it is a failure that occurs outside the repository, where correcting a file
corrects nothing. `RAID-REGISTER.md` **R10** carries this as an open high-severity risk and states the
control is necessary but not sufficient.

**Current state — technical evidence layer.**

- No label mechanism exists anywhere: `grep -rn "INTERACTIVE PROTOTYPE" .` returns no lines, and a
  case-insensitive grep for fiction, provenance, AI-generated or disclaimer text across
  `scaffold/frontend/` returns zero hits (the same check recorded in §P0.8).
- **The handoff exists and its reconciliation is not recorded.** `docs/design/UI-RESEARCH-HANDOFF.md`
  and its companion `docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md` are present, both dated
  19 July 2026, both headed *DRAFTED — NOT FOUNDER-APPROVED — NOT IMPLEMENTED*, the first with
  disposition **BACKLOG — must not interrupt Phase 0 remediation** and implementation gated on its own
  open decision **D10**. `docs/design/ENTITY-PROFILE-EXPERIENCE.md` covers the dossier surface on the
  same terms. All three are **untracked working files**: `git ls-files docs` returns only `PLAN.pdf`,
  the two audit records and `evidence/`. So the handoff is *received*; whether it is *reconciled* is
  not asserted here, and this section does not reconcile it. Cited by name, not by line — sibling
  drafts are live documents.
- **A wording divergence that must be reconciled and is not resolved here.** Both UI drafts propose the
  shorter band `FIXTURE DATA — NOT A SIMULATION RUN` adjacent to a `FICTIONAL WORLD` disclosure. The
  founder wording above is longer and says more: it names the artefact an interactive prototype and
  states that it is not connected to the engine. Which string governs is recorded as open at
  `RAID-REGISTER.md` R10. No agent may choose between them.

### Lane C-ENGINE — executable product proof

**Purpose.** Executable product proof. This lane follows the real dependency chain and cannot be
accelerated by anything C-VISUAL produces:

> P0.4 authoritative-state contract → P0.4A deterministic randomness → P0.5 first cross-tier causal
> mechanism → P0.6 events, causal trace, state hashing and replay → benchmarks and integrated UI.

**Note the constraint this inherits.** P0.5 *implementation* may not begin until P0.4A passes
(§P0.4A, sequencing rule), and P0.5 in Phase 0 is a **design**, not an implementation (§P0.5). C-ENGINE
therefore reaches past the end of Phase 0 by construction. Nothing in Phase 0 delivers gate C2.

## The five gates

Each gate is a **target**. The "Unlocked by" column names the P0 item that must land first; it does not
report that anything has landed.

| Gate | Target | Unlocked by | Current state of the tree |
|---|---|---|---|
| **C0** | Visual proof — five connected fixture-backed screens | **No P0 item.** Founder-stated: must not wait for P0.4–P0.6. Gated instead on the UI-research handoff being reconciled and on the label control | Not started. One 67-line dev stub; none of the five screens exists in any form |
| **C1** | Live state connection | **P0.4** — the authoritative-state contract | Not started. The only state-serving endpoint returns macro alone (`routes_simulation.py:71-77`) |
| **C2** | Live societal propagation | **P0.4A and P0.5** — and P0.5 *implementation*, which is itself behind P0.4A and outside Phase 0 | Not started. The tiers are causally decoupled (`A3-VERIFICATION-RESULTS.md:142-175`) |
| **C3** | Explainability and replay | **P0.6** — which in turn needs P0.4 and P0.4A | Not started. No replay path, no state hash, no RNG-state capture |
| **C4** | Scale evidence | No P0 item directly. Its replay-duration measurement needs **C3**; repeatable measurement needs **P0.3**. *Drafter's inference, not founder-stated* | Not started. No benchmark or timing harness exists |

### Gate C0 — Visual proof

**Unlocked by:** no P0 item. This is founder-stated and load-bearing: **the absence of C3 must not be
used to delay C0.**

**Plain English.** Five screens, connected to one another, drawn on fixture data, in an original visual
language, honestly labelled, walked through in five scripted minutes. It shows what the product is
meant to be. It shows nothing about what the engine does.

**Target — what C0 must produce.**

1. Five connected fixture-backed screens: **Strategic Command Centre**, **Entity Dossier**, **Society
   Pulse**, **Conversational Command Interface**, **Causal Timeline**.
2. An original visual language.
3. Honest prototype labelling, per the C-VISUAL condition above, surviving into screenshots and
   recordings.
4. A five-minute scripted walkthrough.
5. **No claim of connected simulation behaviour**, in the interface, the script or any artefact cut
   from either.

**Current state — technical evidence layer.** None of the five screens exists. `scaffold/frontend/`
holds exactly one file. Its three buttons call `POST /api/simulation/runs` (`index.html:41-45`), open a
WebSocket (`:54-55`) and send a tick request (`:62`); its own description points at
`design_ux_screens.md` (`:18`), which does not exist and is one of the dangling citations P0.1 Group J
must clear. The five screen names appear nowhere under `scaffold/`.

**Boundary to watch.** C0's *Conversational Command Interface* is the surface most likely to be
misread as evidence of live model integration. The approved wording applies without alteration:

> "The architectural mutation boundary exists in scaffold form, but live model integration,
> external-input recording and replay have not yet been implemented."

### Gate C1 — Live state connection

**Unlocked by: P0.4.** A UI cannot read an authoritative snapshot before the contract defining what is
authoritative exists; that is the same reasoning §P0.4 gives for P0.5, P0.6 and P0.7, and it carries
the same caveat — the dependency is the drafter's inference from the founder-set ordering, not a
founder statement. See the note under §P0.4 and `RAID-REGISTER.md` D3.

**Target.**

1. The UI reads a **versioned authoritative snapshot**.
2. **No client-side authoritative state.**
3. At least one real **entity**, **cohort**, **organisation** and **indicator**, each from the engine.
4. Fixture-only values remain **visibly distinguished** from live values — the C0 label does not simply
   disappear at C1; a mixed surface must show which half is which.

**Current state — technical evidence layer.** Of the four object kinds C1 requires, the engine can
serve one. `get_state` returns macro only (`routes_simulation.py:71-77`); no endpoint serves meso,
micro, entity or organisation state. There is **no authoritative micro state at all** — no field of the
`MicroAgent` spec (`agent_schema.py:154-184`) is written by any code path (§P0.4). No snapshot version
field exists. Run storage is the in-process `_RUNS` dict (`api/runs.py:18`), which does not survive a
process restart, and nothing is written to the database (§P0.1 Group C).

**One consequence worth stating now, because it constrains P0.4's scope.** *(Drafter's observation, not
a founder statement.)* C1 requires an **organisation** read from the engine. No organisation tier
exists in code: `InstitutionalAgent` writes exactly one attribute, `self.last_proposal`
(`institutional_agent.py:24`, `:38`). If P0.4's contract does not classify an organisation tier, C1 is
not reachable even once P0.4 lands. That is not a request to widen P0.4; it is a dependency the owner
should see before P0.4's scope is fixed.

### Gate C2 — Live societal propagation

**Unlocked by: P0.4A and P0.5.** Specifically P0.5 *implementation*, which §P0.4A places behind P0.4A
and §P0.5 places outside Phase 0. **C2 is therefore not reachable within Phase 0**, and no schedule may
assume otherwise.

**Plain English, and the reason this gate matters more than the other four.** **This is the first point
at which the demonstration may truthfully claim that MERIDIAN simulates a societal response.** Before
C2, that sentence is false. After C0 and C1 it is still false. No wording, label or caveat makes it
true earlier.

**Target — one real end-to-end chain, engine-produced at every hop:**

> maritime crisis → insurer risk response → shipping-company rerouting → port-economic exposure →
> cohort belief and behaviour changes → media and family reactions → political pressure → government
> state change

The UI must display changes **from the engine**, not from fixture scripts. A fixture-driven animation
of that chain is a C0 artefact, whatever it looks like.

**Current state — technical evidence layer.** Five of the eight hops have no representation in code at
all.

- **Insurers, shipping companies and ports do not exist as entities of any kind.** The demo scenario
  carries five cohorts (`kestral-strait.json:39, 79, 122, 162, 202`) and six institutional agents
  (`:243, 266, 298, 320, 345, 367`), and no organisation model is instantiated anywhere.
- **The tiers do not causally influence one another.** A3 hammered macro and cohort beliefs were
  unchanged; it set cohort beliefs to 0.01 and macro was unchanged
  (`A3-VERIFICATION-RESULTS.md:147-168`). The two perturbations that *did* move macro moved it through
  shared-RNG draw-count contamination, not causality (§P0.5) — which is why P0.4A, not P0.5 alone,
  unlocks this gate.
- **No aggregation exists.** `represents_population` (`agent_schema.py:95`) is populated in the
  scenario and read by no code, which is the founder constraint P0.5 exists to satisfy.
- **Media and family have no model.** `MediaExposure` (`agent_schema.py:42-53`) is declarative and sits
  among the twelve targeting terms with zero read sites recorded in §P0.8. There is no family or
  relationship structure in the scaffold.
- **Government state change** would land on `government_approval`, one of the three keys
  `ACTION_EFFECTS` touches (`engine.py:35-43`) — a key that saturates at a clamp bound with no opposing
  mechanism (§P0.7).

**Exit evidence C2 must carry.** Per §P0.5's exit criterion, each hop needs a perturbation test of the
form "change X by Δ and Y must move; change X by Δ **with the RNG substreams frozen** and Y must
**still** move." Without the second half, a C2 demonstration cannot be distinguished from the
contamination A3 found, and must not be presented as propagation.

### Gate C3 — Explainability and replay

**Unlocked by: P0.6** — and therefore by P0.4 and P0.4A behind it.

**Conditional on OQ-7.** If the owner rules P0.6 design-and-specification-only, **P0.6 delivers no
substrate for C3 and C3 does not unlock in Phase 0.** If the owner rules implementation, it does. This
section does not pre-empt that ruling, and no Track C schedule may assume either answer.

**Target — all of:** causal events; causal parents; rule and mechanism attribution; before/after state;
assumptions and uncertainty; state hashes; recorded external inputs; replay that makes **zero model and
zero network calls**; and identical resulting authoritative hashes.

**The claim boundary.** **Only after C3 may the project claim causal reconstruction or replay
capability.** Until then the sole permitted reproducibility claim is the founder-approved wording at
`HANDOFF.md:56-57`, quoted in §3, and the target contract at `HANDOFF.md:61-62` stays labelled a
target.

**Current state — technical evidence layer.**

- **No state hash and no RNG-state capture.** `hashlib` and `getstate` both return zero occurrences
  across `backend/app` (§P0.4, §P0.4A).
- **No replay path exists at all** (§P0.6).
- **Causal parents are declared and not populated.** `Event` defines `causal_parents`
  (`agent_schema.py:211-229`); the decision endpoint appends a differently-shaped dict that omits it
  (`routes_simulation.py:91-100`); no event is ever validated against the schema; and the `observe`
  action produces **no event-log record at all**, because its effect maps to an empty dict
  (`engine.py:42`) and the append is guarded by `if deltas:` (`engine.py:163`).
- **There is no rule to attribute.** `_validate_and_price` is a seven-entry dictionary lookup
  (`engine.py:35-43`, `:121-130`) — publication blocker B1.
- **Before/after state is macro-only and in memory.** `self.snapshots` holds `model_dump()` of macro
  (`engine.py:116`, `:180`); meso, `narrative_adoption`, the event log and RNG state are all absent.
- **Recorded external inputs do not exist.** The approved gateway wording in §Gate C0 states the
  position and must be used verbatim wherever this is described.

### Gate C4 — Scale evidence

**Unlocked by:** no P0 item directly. **Drafter's inference, stated as such:** replay duration is not
measurable before C3, and measurement that anyone can repeat wants the CI of P0.3 behind it. The
founder statement of C4 names no unlock, and none is invented here beyond what those two measurements
require.

**Target.**

1. Benchmark **several** entity and cohort counts.
2. Record **tick time, memory, event volume and replay duration**.
3. Distinguish **MEASURED** performance from **PROJECTED** architecture, explicitly and in the artefact
   itself.
4. Document the path to partitioning or distributed execution **without claiming it has been
   delivered**.

**Current state — technical evidence layer.** No benchmark or timing harness exists:
`grep -rn "perf_counter\|timeit\|benchmark\|memory_profiler" scaffold/` returns zero lines, re-run
19 July 2026. There is no CI to run one (§P0.3). Event volume is bounded by an in-memory list and run
storage does not survive a restart (`api/runs.py:18`), so nothing today measures a persisted workload.

**The wording risk this gate carries.** Item 3 is the whole of C4's honesty. A benchmark table that
does not separate measured from projected numbers reproduces the project's defining defect at a new
surface, and `CAPABILITY-CLAIMS.md` governs the wording.

## The two walkthroughs — they must not be conflated

| Walkthrough | Backed by | When | What it is for |
|---|---|---|---|
| **PROTOTYPE WALKTHROUGH** | Fixture data, labelled per C-VISUAL | Early — at C0 | Product and design communication |
| **INTEGRATED ENGINE WALKTHROUGH** | The real P0.5 chain plus P0.6 causal trace and replay | After C3 | **The final interview artefact** |

The final interview demonstration is **C3 plus sufficient C4 evidence**. A PROTOTYPE WALKTHROUGH
presented, described or captioned as the demonstration is an overclaim regardless of how the screens
are labelled, because the label describes the screen and the framing describes the project.

## The critical-path relationship

The demonstration's endpoint requires three capabilities the closed audit found **missing**:

| The demonstration needs | The audit found | Where |
|---|---|---|
| "the engine validates and executes" an action | `_validate_and_price` is a seven-entry dictionary lookup | Blocker B1; `engine.py:121-130` |
| "society reacts differently across entities" | The tiers are causally decoupled | Critical finding 4.1; `A3-VERIFICATION-RESULTS.md:142-175` |
| "replay reproduces the authoritative state hash" | No replay path, no state hashing, RNG state never captured | §P0.4, §P0.4A, §P0.6 |

**The critical path is therefore P0.4 → P0.4A → P0.5 → P0.6, and Track B sits *on* that critical path
rather than beside it as a side workstream.** Lane C-ENGINE follows that chain in order. Lane C-VISUAL
runs alongside it on labelled fixture data and can never be described as the final functioning
demonstration. `RAID-REGISTER.md` **D19** carries the same statement as a BLOCKING dependency.

The practical consequence: **no amount of C-VISUAL work shortens the path to the demonstration**, and
no C-VISUAL artefact may be scheduled, presented or counted as progress against it. The converse also
holds and is the reason C0 is unblocked — C-ENGINE work does not gate C0 either.

## The C-prefix collision — read this before citing any gate

**`C0`–`C4` here are Track C gates. `C1`–`C14` and `C8A` in
[`PUBLICATION-EXIT-CRITERIA.md`](PUBLICATION-EXIT-CRITERIA.md) are publication exit criteria. They are
different things and the numbers overlap.** Track C gate C1 is *live state connection*; publication
criterion C1 is *documented clean installation works on a supported environment*. Gate C2 is *live
societal propagation*; criterion C2 is *no document claims the engine validates legality*.

This matters immediately, because §P0.1 above already cites "the C2 grep in
`PUBLICATION-EXIT-CRITERIA.md`" and "`PUBLICATION-EXIT-CRITERIA.md` C3", and §P0.4A cites "C8A". Those
citations are correct and are **not** changed here — renumbering either series would break live
citations across several records, which is the outcome the append-don't-renumber rule exists to
prevent.

**Convention proposed to avoid the ambiguity, drafter's proposal and not a decision:** write **"gate
C2"** or **"Track C gate C2"** for this section, and **"criterion C2"** or
**"`PUBLICATION-EXIT-CRITERIA.md` C2"** for the publication gate. Never a bare `C2`. Existing bare
citations elsewhere refer to the publication criteria, since Track C had no record in this document
before this amendment.

## Owner decisions touching Track C

**No new OQ number is minted here, and that is deliberate — each open item already has a home.** They
are listed so that nothing is treated as settled by omission:

- **What authorises C0 to begin, and which label string governs.** Open at
  `docs/design/UI-RESEARCH-HANDOFF.md` decision **D10** ("Is a fixture-backed prototype authorised
  before Phase 0 completes, and is the labelling…") and at `RAID-REGISTER.md` **R10**. The founder
  correction states C0 must not wait for P0.4–P0.6; it does not by itself commission the work, and this
  section does not commission it either.
- **Whether C3 unlocks inside Phase 0.** Governed by **OQ-7** (§P0.6 scope: design-only or
  implementation). Unresolved.
- **How P0.4A's numeric change is authorised**, which sits ahead of C2 on the chain. Governed by
  **OQ-9**.
- **Whether P0.4's contract defines an organisation tier**, without which gate C1's organisation
  requirement has nothing to read. Raised under Gate C1 above as an observation for the owner; it is
  not a proposal to widen P0.4.
- **The critical-path statement itself** is recorded at `RAID-REGISTER.md` **D19** with status
  BLOCKING and no assigned owner.

## What this section does not authorise

It does not authorise building any screen, any fixture, any benchmark harness or any label mechanism.
It does not authorise beginning C-ENGINE work, which sits behind P0.4, P0.4A, P0.5 and P0.6 and is
separately unauthorised by §P0.4A and §P0.5. It does not reconcile the UI-research handoff, choose
between the two label strings, or move any gate's unlock condition. It records targets and the order in
which they can become reachable, and nothing else.

---

## 5. Dependency summary

```
P0.1  (documentary)          ── no dependencies ── entry item
  │
  ├─> P0.2  (install)        ── needs P0.1 so the README it rewrites is already true
  │      │
  │      └─> P0.3  (CI)      ── STRONG sequencing dependency: do not build CI on an
  │                             install path whose resolvability is unverified
  │
  └─> P0.4  (state contract) ── no technical dependency; foundational for all below
         │
         ├─> P0.4A (deterministic randomness) ── founder-added 18 Jul 2026; interacts with
         │      │                                 open decision 8.3 (Mesa); see OQ-9
         │      │
         │      ├─X  P0.5 IMPLEMENTATION      ── may NOT begin until P0.4A passes
         │      ├─X  entity promotion         ── may NOT begin until P0.4A passes
         │      ├─X  world-model materialisation ── may NOT begin until P0.4A passes
         │      └─X  P0.6 snapshot/replay     ── needs the stream architecture first
         │
         ├─> P0.5  (cross-tier design)   ── SPECIFICATION may proceed in parallel NOW,
         │                                  before P0.4A is implemented
         ├─> P0.6  (event/snapshot/replay) ── benefits from P0.3 for enforcement
         └─> P0.7  (time and horizon)    ── gates all later saturation work

P0.8  (dual-use)             ── independent; decision TAKEN 18 Jul 2026; now BLOCKED on
                                eight enforcement controls being built and verified;
                                gates publication. Control 5's *test* additionally needs
                                P0.4A, since a bit-identical comparison means nothing on a
                                shared RNG stream
```

P0.1 and P0.4 can proceed in parallel. **P0.8's description in the previous draft — "the long pole: it
is blocked on a person, not on work" — is now wrong and is corrected here.** The person has decided. It
is blocked on work: eight controls, none of them started, at least two of them (real-entity detection
and the protected-characteristic boundary) still needing a method before they can be built.

**Read the P0.4A branch carefully: it is a split dependency, not a simple one.** P0.5 appears on both
sides deliberately — its *specification* is unblocked and may run in parallel with P0.4A, while its
*implementation* sits behind the gate. The `─X` lines are hard stops, not preferences. The founder's
statement of why is in §P0.4A: "Materialising a background citizen must not change tomorrow's weather,
market behaviour, government approval or another person's decision merely because it consumed extra
draws."

**Track C consumes this graph; it does not appear in it.** The gates are not P0 items and add no node
above. Their unlock conditions read off it: gate C1 ← P0.4, gate C2 ← P0.4A **and** P0.5
implementation, gate C3 ← P0.6 (conditional on OQ-7), gate C4 ← gate C3 plus P0.3 for repeatable
measurement. **Gate C0 is unlocked by no P0 item** and must not wait for P0.4–P0.6. The critical path
to the demonstration is the P0.4 → P0.4A → P0.5 → P0.6 spine already drawn above. See the `# Track C`
block, and note the C-prefix collision recorded there before citing any gate by number.

## 6. Open questions for the owner

None of these is resolved in this document. All are addressed to the owner.

| # | Question | Bears on |
|---|---|---|
| OQ-1 | The founder annotation calls P0.5 arguably the highest-value item. Keep the order P0.1→P0.8, or promote P0.5 (and P0.4 with it, since P0.5 depends on it)? *Narrowed 18 July 2026: P0.5 sequencing is confirmed unchanged, its specification is already unblocked in parallel, and its implementation cannot precede P0.4A. Only the rest of the list remains orderable.* | Sequencing |
| OQ-2 | `NOTICE.md:11` states in the present indicative that the source is publicly visible. The repository is private (`HANDOFF.md:13`). Was this intended as current fact or as the post-publication position? | P0.1 |
| OQ-3 | The audit's remedy for the dangling design-doc citations is to repoint them at `PLAN.pdf` sections. That presumes decision 8.7 (`PLAN.pdf` stays canonical), which is open. Remove the citations, or hold until 8.7? | P0.1 |
| OQ-4 | Decision 8.5: adopt `uv` + `pyproject.toml` + a hash-pinned lock, or fix the install minimally within `requirements.txt`? | P0.2 |
| OQ-5 | Branch protection, required status checks, CODEOWNERS and secret scanning on the `origin` remote — their current state was **not verified** and no CODEOWNERS file exists locally. Confirm or configure. | P0.3 |
| OQ-6 | Decision 8.3: does Mesa remain the ABM substrate? Choosing a randomness architecture against a base class that may be removed — and which materialises a second, entropy-seeded generator — is wasted work. | **P0.4A**, then P0.5 |
| OQ-7 | Does P0.6 in Phase 0 mean design-only, or implementation? A central transition mechanism is a refactor of the authoritative write path and could shift numeric output through the shared RNG stream. | P0.6 |
| OQ-8 | ~~Decision 8.6 / blocker B5: the dual-use policy itself.~~ **ANSWERED 18 July 2026 — retained, not deleted, so the numbering holds.** Eight controls apply and technical enforcement is mandatory; see §P0.8. **The answer did not complete P0.8**, and B5 remains a publication blocker. It is still true that this item cannot be completed by drafting — now for a different reason. OQ-10 to OQ-13 arise from the answer. | P0.8 |
| OQ-9 | P0.4A will change numeric outputs at an unchanged seed, because any of the candidate architectures changes which number a given draw returns. That is unavoidable and is not behaviour-modification to bury a finding, but it affects determinism and authoritative state (`HANDOFF.md` § Standing constraints (`:139-140`)). How is that change authorised, and is the pre-change tested baseline captured as superseded before the switch? | **P0.4A** (new, 18 July 2026) |

| OQ-10 | **Control 4:** by what test is an entity determined to be "real"? A maintained denylist fails open on anything unlisted; author attestation fails open on a careless or dishonest author, and control 8 rules it out as the *sole* mechanism because an attestation is not technical enforcement; pre-admission human review does not fail open but does not scale and is not a code control. Until this is settled, control 4 has no testable exit. | **P0.8** (new, 19 July 2026) |
| OQ-11 | **Control 5:** which attributes count as protected characteristics, and does enforcement mean removing the declared fields, gating their read sites, or asserting output invariance? Specifically, `identity_appeal` is a persuadability scalar that already feeds diffusion gain (`cohort_agent.py:22-26` → `diffusion.py:74-76`) — is it inside the prohibition or outside it? The permitted/not-permitted distinction is clear in principle and not yet mechanical. | **P0.8** (new, 19 July 2026) |
| OQ-12 | **Control 7:** what evidence closes the UI half? The API half is contract-testable. A rendered interface disclosure is verifiable by no command in this plan, and a screenshot, a component test and a reviewer's signed observation are not equivalent. | **P0.8** (new, 19 July 2026) |
| OQ-13 | **What authorises building controls 1–5 and 7?** All of them require changes under `scaffold/` — schema, loader, API responses, tests. The founder decision settling the policy states that it authorises no feature implementation, so the decision is recorded and the work it implies is not yet commissioned. Same class as OQ-7's boundary question for P0.6. | **P0.8** (new, 19 July 2026) |

For the record, section 8 of the audit contains seven items. **Four are settled** (8.1 licence, 8.2
visibility and the publication gate, 8.4 reproducibility wording — all recorded in `HANDOFF.md` — and,
since 18 July 2026, **8.6 dual-use**, which is recorded in §P0.8 above and nowhere in `HANDOFF.md`).
**Three remain open:** 8.3 Mesa, 8.5 `uv`/`pyproject`, 8.7 `PLAN.pdf` format. Settling 8.6 did not clear
blocker B5; see §P0.8.

## 7. Stale citations in the source documents

Recorded so that whoever executes this plan is not sent to the wrong line. These are drift, not new
findings; the underlying claims are unchanged.

| Document | Says | Current reality |
|---|---|---|
| `A3-VERIFICATION-RESULTS.md:242` (B2) | "There is no CI and no `.git`" | No CI is still true. `.git` now exists at commit `71fa329`, branch `main`, remote `origin` configured |
| `CURRENT-STATE-AUDIT.md:13`, `:283`, `:339`, `:372` | "no `.git` directory at all" / "The repository is not under version control" | Now false. The no-CI clauses in the same sentences remain true |
| `CURRENT-STATE-AUDIT.md:349` (item 47) | `backend/plan.txt` is an uncontrolled duplicate | The file is not in the tree. Also voids the `plan.txt` argument in decision 8.7 (`:413`) |
| `CURRENT-STATE-AUDIT.md:235`, `:291` | Cites `plan.txt:221` for the DISARM Red Framework correspondence | Unresolvable — `plan.txt` is gone. `docs/PLAN.pdf` still contains two DISARM link annotations, but the surrounding prose was not extracted and the wording is **unverified** |
| `CURRENT-STATE-AUDIT.md:237`, `:403` | `README.md:92` states the repository is public | `README.md` is now 96 lines; `:92` is the copyright statement. No public-status claim remains in `README.md`. The wording migrated to `NOTICE.md:11` (see OQ-2) |
| `CURRENT-STATE-AUDIT.md:237` | `COPYRIGHT.md` states the licensing position | No `COPYRIGHT.md` exists; the file is `NOTICE.md`. The substantive point (no acceptable-use restriction) still holds |
| `CURRENT-STATE-AUDIT.md:174` | Archetype claim at `README.md:106-107` | Now `README.md:72-74`, reworded. The quoted phrasing survives at `scaffold/README.md:106-107` |
| `CURRENT-STATE-AUDIT.md:219` | Meso tier described as weighted cohorts at `README.md:6` and `scaffold/README.md:16` | Now `README.md:6-7`. A different claim from the archetype one at `:174` — do not conflate them |
| `CURRENT-STATE-AUDIT.md:84` | "`README.md:25` promises 'Every action creates second- and third-order effects'" | That sentence is at `CHARTER.md:25`, not in `README.md`. The claim stands; the citation does not |
| `CURRENT-STATE-AUDIT.md:158` | Engine-validates claim at `README.md:19` and `:24` | Now at `README.md:38`. `:19` is a status blockquote and `:24` is a table header |
| `CURRENT-STATE-AUDIT.md:292` | "Ten references to five files that do not exist" | Now nine reference lines (8 named + 1 glob). The five filenames are unchanged and all five still do not exist |
| `CURRENT-STATE-AUDIT.md:393` | "No checklist exists" | Seven publication exit criteria now exist at `HANDOFF.md` § Publication exit criteria (`:92-102`) |

## 8. What is asserted here without direct verification

Stated explicitly, because a plan written to fix overstated claims must not contain any.

1. **The install failure mode.** `HANDOFF.md:45-47` records that `litellm` resolves to 1.92.0, has no
   cp313 wheel, and needs a Rust toolchain. This was **not reproduced** for this plan; no environment was
   created and nothing was installed. That `litellm` is unimported and unpinned is directly verified;
   *why* the install fails is second-hand.
2. **"5 tests pass."** `HANDOFF.md:43` and `:51` record it. The suite was **not run**. What is verified is
   that five test functions exist in one file (`test_engine.py:25, 34, 43, 52, 61`) and that the two the
   README names by name are among them.
3. **Whether the Docker build succeeds** on Linux/Python 3.11. `CURRENT-STATE-AUDIT.md:29` already marks
   this Unknown; no build was run.
4. **The remote's visibility and its branch-level controls.** No `gh` or network command was run, per the
   standing constraint. That the repository is private rests on `HANDOFF.md:13`, not on an observation.
   Whether commit `71fa329` has actually reached the server is likewise inferred from a local
   remote-tracking ref, not from a fetch.
5. **The one-directional-drift argument in P0.7** is arithmetic over `ACTION_EFFECTS` (`engine.py:35-43`),
   the stub role table (`llm_gateway.py:43-51`) and the six scenario agents. It is **inferred from source,
   not executed.** The *observed* saturation evidence is A3's, at `A3-VERIFICATION-RESULTS.md:182-187`.
6. **Pydantic `validate_assignment` being off** at `macro_state.py:47` is inferred from the absence of any
   `model_config` in `macro_schema.py`, not from an executed out-of-range write.
7. **The DISARM correspondence claim in `docs/PLAN.pdf`.** Only two link-annotation URIs are extractable
   from the raw bytes. The surrounding sentence was not extracted, so the wording the audit quoted at
   `plan.txt:221` is **unconfirmed**.
8. **Resolved dependency versions.** Every requirement is a range, nothing is installed, and no lockfile
   exists, so no concrete installed version can be stated for any package. Whether the thirteen ranges even
   resolve together is undetermined.
9. **No code was executed in the preparation of this plan.** Every code-side statement rests on reading
   source, on grep call-site absence, or on execution evidence already recorded in
   `CURRENT-STATE-AUDIT.md` and `A3-VERIFICATION-RESULTS.md` and attributed to them where used.
10. **This plan is not a new audit.** No new findings were sought. Only the specific claims this record
    needed to assert were verified. Absence of a finding here is not evidence of absence.
11. **P0.4A's ten exit criteria have never been run**, and several have no substrate to run against.
    There is no stream architecture, no key scheme, no draw record and no isolation test in the tree
    today, so the criteria are stated as specifications of a future test suite, not as checks with a
    known current result. Where the P0.4A section reports a *current* fact — one generator at
    `engine.py:83`, three draw sites, `getstate` and `hashlib` absent — that is read from source, per
    item 9. The claim that the existing determinism test cannot detect draw-order contamination is
    **reasoned from its shape** plus the executed injection evidence already recorded at
    `CURRENT-STATE-AUDIT.md:140` and `A3-VERIFICATION-RESULTS.md:170-175`; no new test was written or
    run for this amendment.
12. **P0.8's eight controls have never been run, and none has a substrate to run against.** There is
    no world-mode field, no scenario validation, no real-entity check, no protected-characteristic
    list and no disclosure field in the tree, so the table in §P0.8 states requirements and current
    absences, never partial compliance. The verification methods in that table are the **drafter's
    proposals**: unlike P0.4A, the founder decision states controls rather than a numbered
    exit-criteria list, so nothing in that column should be read as founder-set. The decision itself,
    like P0.4A's, **is not a file in the tree** and is cited by date. No code was written or executed
    for this amendment.
13. **No Track C gate has ever been run, attempted or partially met.** Nothing in Track C is built, so
    the gate block states targets and current absences only, never partial progress. The founder
    correction of 19 July 2026 that established the two lanes and the five gates **is not a file in the
    tree** and is cited by date, as with P0.4A and P0.8. What was directly verified for that amendment
    is narrow and is listed here in full: `scaffold/frontend/` contains exactly one file, `index.html`,
    of 67 lines, read in full; `grep -rn "perf_counter\|timeit\|benchmark\|memory_profiler" scaffold/`
    returns zero lines; a grep for the five gate-C0 screen names under `scaffold/` returns nothing;
    `docs/design/UI-RESEARCH-HANDOFF.md`, `UI-VERTICAL-SLICE-RECOMMENDATION.md` and
    `ENTITY-PROFILE-EXPERIENCE.md` exist, are untracked, and carry the status headers quoted; and
    `PUBLICATION-EXIT-CRITERIA.md` uses the identifiers C1–C14 plus C8A, which is the basis of the
    collision warning. Every other code-side statement in the Track C block is carried from the P0
    sections above and attributed there. **No code was executed, no screen was built and no new
    investigation was opened for this amendment.** Whether the UI-research handoff has been
    *reconciled* — as distinct from received — is **not asserted**; the drafts' own status headers are
    quoted instead.

---

*End of draft. **Two exceptions to the line below, both founder decisions of 18 July 2026:** (i)
P0.4A's existence, its placement between P0.4 and P0.5, its five-axis scope, its sequencing rule and
its ten exit criteria; and (ii) P0.8's eight controls and its identity/bias distinction. Everything
else about P0.4A — the ADR's choice between stateful named substreams and keyed/counter-based draws,
the key scheme, the supersession of ADR-007, and OQ-9 — remains unapproved, as does everything else
about P0.8: the verification methods proposed for the eight controls, and OQ-10 to OQ-13.*

*A third exception, a founder correction of 19 July 2026: **Track C's two lanes, its five gates C0–C4,
their content, C0's release from the P0.4–P0.6 dependency, the fixture-label requirement and the
critical-path statement are founder-set.** The mapping of gates to unlocking P0 items is the founder's
where the founder stated it and is **marked as the drafter's inference where it is not** — C4's unlock
and the Gate C1 organisation observation in particular. The proposed "gate C2 / criterion C2" citation
convention is the drafter's and is not a decision.*

*No other item above is approved. Nothing in this document authorises a change to simulation
behaviour, a repository visibility change, or a licence change. In particular, nothing here authorises
beginning P0.4A implementation, nothing here authorises building any of P0.8's eight controls, and
nothing here authorises beginning work on any Track C gate, C0 included.*
