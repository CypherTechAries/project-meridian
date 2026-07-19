# Architecture Decision Record — template and usage guide

**Status:** DRAFT pending owner review.
**Date:** 19 July 2026 (revised).
**Drafted by:** an AI agent. The standing constraint reads: "AI agents may draft records but may not
approve **their own decisions**" ([`HANDOFF.md` § Standing constraints (`:138`)](../../HANDOFF.md)). This template applies the
stricter rule that **no AI agent approves any ADR**, whether it drafted it or not. That stricter
reading is this draft's extension of the cited text, not the cited text itself, and is open question
8 in §4. Nothing in this document is approved until the owner marks it so — including the template
itself.

This document has five parts. Part 1 is the guide: what an ADR is here, what requires one, and how
it is approved. Part 2 is the template, given as a copy-paste block. Part 3 is one worked example,
which is **illustrative only and is not a decision anyone has taken**. Part 4 lists the questions
this document deliberately does not answer, which are for the owner. Part 5 records what was and was
not verified in drafting it.

The template deliberately does not match a generic internet ADR format. It follows the shape, tone
and numbering already established by the nine ADRs in
[`scaffold/docs/ARCHITECTURE_DECISIONS.md`](../../scaffold/docs/ARCHITECTURE_DECISIONS.md), and adds
the fields this project specifically needs: a determinism-impact section, an evidence section, and a
human-approval section.

---

# Part 1 — The guide

## 1.1 What an ADR is here (plain English)

An ADR is a short written record of a decision that would be expensive to reverse, written at the
time the decision is made, so that whoever inherits the project inherits the *reasoning* and not
just the result. The existing file states this purpose directly: each decision is recorded "so
future contributors — human or AI — inherit the *why*, not just the *what*"
(`scaffold/docs/ARCHITECTURE_DECISIONS.md:3-5`).

On this project an ADR carries a second job that is unusual, and it is the reason this template
exists in the form it does.

MERIDIAN's worst defect is that its documentation has claimed properties its code does not have.
Four of the five publication blockers recorded in
[`A3-VERIFICATION-RESULTS.md:237-247`](A3-VERIFICATION-RESULTS.md) clear by correcting text rather
than by writing code. Some of those false claims live inside the existing ADRs. For example
`scaffold/docs/ARCHITECTURE_DECISIONS.md:29` states in the present tense that the project persists
three tables, while nothing is written to the database (blocker B3,
`A3-VERIFICATION-RESULTS.md:243`); `:75` states that adding an eighth archetype "must require only a
new `scenarios/*.json`" (blocker B4, `A3-VERIFICATION-RESULTS.md:244`). Both code-side facts are
inherited from the audit and from A3; neither was re-verified against source for this document.

The ADRs state these things as present fact. Whether they were *intended* as statements of intent is
not recorded anywhere and is not something this document can establish — the record shows the
wording only. What can be said is that nothing in their format required the author to distinguish
the two.

So this template forces the distinction. Every ADR must separate what has been decided from what has
been built, must cite evidence in a form a reader can check, and must be signed off by a human.

## 1.2 What requires an ADR

An ADR is required before any change in the following categories.

**The left-hand column only** is taken directly from the standing constraint at
`HANDOFF.md` § Standing constraints (`:139-140`), which states that human approval is required for "architecture, dependencies,
licence, migrations, auth, security controls, public releases, and anything affecting determinism or
authoritative state." The eight category names are taken from that line. Seven are reproduced
verbatim; the last is abbreviated in the table below from "anything affecting determinism or
authoritative state" to fit the column, and is to be read with the full breadth of the original
wording.

**The right-hand column is not.** It is this draft's proposed reading of what each category covers on
this project. It is drafter-authored, carries no founder citation, and in places takes a position the
constraint does not take — for example treating the packaging tool as a Dependencies matter, when
packaging tooling is itself an open audit decision (§8.5). The right-hand column is therefore subject
to owner approval along with the rest of this template (§4).

| Category | Examples on this project |
|---|---|
| **Architecture** | Replacing or removing the ABM substrate; changing the tick loop's structure; introducing a new tier or a new transition mechanism |
| **Dependencies** | Adding, removing or unpinning any package; changing the packaging tool or the supported Python version |
| **Licence** | Any change to the all-rights-reserved position recorded in `NOTICE.md`; any acceptable-use or field-of-use terms; accepting external contributions |
| **Migrations** | Any database schema change; any change to the shape of a snapshot or event record (note: nothing is currently written to the database — blocker B3, `A3-VERIFICATION-RESULTS.md:243`) |
| **Auth** | Introducing authentication or authorisation of any kind, including API keys for the LLM path |
| **Security controls** | Secret handling, input validation at a trust boundary, scenario-content restrictions, anything gating dual-use capability |
| **Public releases** | Repository visibility changes; any tagged or published build; anything that puts an artefact in front of a reader |
| **Determinism or authoritative state** | Anything that changes what is authoritative, what writes it, the RNG, the number or order of random draws, snapshot contents, or replay |

The last row is the widest and the least intuitive, so it is stated explicitly. An ADR is required
for a change that adds, removes or reorders a random draw, even if the change looks local and even
if it looks like a refactor.

There is exactly one `random.Random` created in **application code**
(`scaffold/backend/app/simulation/engine.py:83`), and exactly three draw sites consume it
(`scaffold/backend/app/simulation/agents/cohort_agent.py:36`,
`scaffold/backend/app/simulation/diffusion.py:75`,
`scaffold/backend/app/simulation/engine.py:135`). Those citations are positive instances and cannot
by themselves establish the words "exactly one" and "exactly three"; the exhaustiveness claim rests
on a search, and the command a reader can run to check it is:

```
grep -rn "random\.Random(\|\.rng\." scaffold/backend/app
```

It is not the only RNG object in the backend. `scaffold/backend/app/simulation/engine.py:82` passes
`seed=resolved_seed` to `super().__init__()`, but the audit records that **this kwarg is inert**:
mesa 2.4.0 seeds in `Model.__new__` from the original constructor call and `Model.__init__` ignores
the argument, so on the API path (`seed=None`) Mesa's own `self.random` is seeded from entropy
(`CURRENT-STATE-AUDIT.md:319`, audit finding 27; the audit describes this elsewhere as Mesa
"materialis[ing] a second `random.Random`", `CURRENT-STATE-AUDIT.md:405`). Nothing in application
code reads it — that negative is the audit's, at `CURRENT-STATE-AUDIT.md:319` ("nothing reads it"),
and was not independently re-derived here. Mesa's internals were not re-verified for this document;
Mesa is not installed in the environment this was drafted in.

The unqualified phrase "one RNG in the backend" is wrong; "one RNG in application code" is the
checkable claim.

Because the three application draw sites share one stream, a change to draw *counts* in one
subsystem shifts every subsequent draw in every other subsystem. A3 demonstrated exactly this:
adding a grievance to a single cohort changed a national macro indicator, with no causal channel
between them (`A3-VERIFICATION-RESULTS.md:153-168` — the perturbation result is the table row at
`:153`, the mechanism is explained at `:156-168`).

## 1.3 What does not require an ADR

Prose edits and typo fixes that do not change engine behaviour. These fall outside all eight
categories at `HANDOFF.md` § Standing constraints (`:139-140`), so stating them here is a restatement of that line rather than a
new exemption.

**Test additions are a drafter-proposed exemption, not a settled one.** An added test does not
obviously fall outside "anything affecting determinism or authoritative state" — a test that calls
into the engine consumes nothing from the shared stream in a separate process, but the judgement of
where that boundary sits is reserved to the owner by `HANDOFF.md` § Standing constraints (`:139-140`). This draft proposes
treating a test addition that changes no engine code as exempt; that proposal is subject to owner
approval along with the rest of this template, and is folded into open question 1 in §4.

If you are unsure whether something is a correction or a decision, apply this test: a correction
makes a document agree with the code as it already is; a decision changes what the code will do, or
changes what the project permits itself to do. If it is both, it is a decision.

**Phase 0 documentary corrections are deliberately NOT resolved here.** An earlier draft of this
section ruled that they do not each need an ADR. That ruling is withdrawn, because this document may
not make it. It collides with two rules in this same template: the final row of §1.2 makes "anything
affecting determinism or authoritative state" ADR-triggering, and determinism question 4 in the Part
2 template asks whether a change alters "a claim the project makes about determinism or
reproducibility". Correcting the CI claim (blocker B2), the persistence claim (B3), or the
reproducibility wording is simultaneously a correction of record *and* a change to a public-facing
determinism claim. `HANDOFF.md` § Standing constraints (`:139-140`) reserves that class of judgement to the owner. It is
therefore open question 7 in §4, and until the owner answers it, treat a documentary correction that
touches a determinism, reproducibility or replay claim as requiring approval rather than as exempt.

## 1.4 The two-layer requirement

Every governance record on this project is **required** to carry two layers — "Every record needs a
plain-English layer and a technical-evidence layer" (`HANDOFF.md:37`) — and an ADR is no
exception. Whether every existing record already satisfies that requirement has not been checked
here.

**Layer 1, plain English.** A reader with no Python and no knowledge of this codebase must be able
to read the Context, the Decision and the Consequences and understand what was chosen and what it
costs. Write it for that reader first. Do not put a claim in this layer that is not supported in
layer 2.

**Layer 2, technical evidence.** Every factual claim about the current code must carry a `path:line`
citation or a command a reader can run. A claim about future behaviour cannot carry evidence, and
must therefore be marked as intended rather than delivered. Where a claim has not been verified,
write that it has not been verified. An honest "not verified" is a correct entry; a confident
overstatement is a project-level failure.

Two specific wordings are fixed by founder decision and must be used verbatim where they apply
(`HANDOFF.md:52-62`).

The claim that may be made about what exists today:

> "The existing stubbed execution path reproduces the same tested numeric outputs when the seed,
> scenario and stubbed agent outputs remain identical."

The target contract, which **must always be labelled a target and never presented as a delivered
capability**:

> "Given the same scenario version, rule-pack version, seed, ordered player inputs and recorded
> external-agent inputs, the engine is intended to reproduce identical authoritative state hashes."

Do not describe the codebase as execution-ready, replay-capable or fully deterministic
(`HANDOFF.md` § Standing constraints (`:135`)).

## 1.5 Approval

**An AI agent may draft an ADR.** The cited constraint is that AI agents "may not approve **their own
decisions**" (`HANDOFF.md` § Standing constraints (`:138`)); this template applies the stricter rule that no AI agent approves
any ADR (open question 8, §4). A drafted ADR sits at status **Proposed** until a named human writes
their name and a date into the Approval block.

An ADR written under this template with an empty Approval block has no authority, whatever its
Status field says, and work must not proceed on it.

**Pending open question 4, treat this rule as prospective only.** That is an interim default this
draft adopts so that work is not blocked while the question is open — it is not a settled property
of the rule. The nine existing ADRs predate the template and contain no approver field at all, so
reading the rule backwards would de-authorise the entire existing architecture record; that is the
reason for the interim default, not an argument that resolves the question. Whether the rule binds
them — and whether they are retrospectively signed or simply recorded as predating the requirement —
is the owner's call, and is open question 4 in §4. Until it is answered, the existing nine keep
whatever standing they had before this document was written.

This is the reason the Approval block is the last field and not the first: it should be the thing a
reader checks after they have read the reasoning, and it should be visibly empty when it is empty.

## 1.6 Numbering, status and lifecycle

- **Numbering** is a single ascending sequence, zero-padded to three digits, matching the existing
  file: `ADR-001` through `ADR-009` are taken. `ADR-010` was claimed on 19 July 2026 by
  [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
  (Status *Proposed*), which is drafted against this template and filed outside the existing log
  pending open question 2 below. **The next new ADR is therefore `ADR-011`.** Numbers are never
  reused and never renumbered, including for ADRs that end up Rejected or Superseded.
- **Statuses.** The existing legend defines only one: "**Accepted** = committed for v1; do not
  re-litigate without a new ADR" (`scaffold/docs/ARCHITECTURE_DECISIONS.md:7`). That is sufficient
  for a closed set of nine historical decisions but not for a live process, so this template uses
  five. Adding the four new ones to the published legend is an open question (§4), because the
  legend lives under `scaffold/`. The standing constraint on this phase is *do not edit code under
  `scaffold/`* — documents only. It does not by its terms forbid documentary edits under
  `scaffold/`, and it cannot: founder-set P0.1 requires correcting live false claims that sit in
  that tree (`scaffold/docs/ARCHITECTURE_DECISIONS.md:29` and `:75`, blockers B3 and B4). Whether
  editing the published legend counts as in-scope documentary correction for this phase is a scope
  question for the owner, raised as open question 5. Note that this constraint is not stated in
  `HANDOFF.md`, `CHARTER.md` or `NOTICE.md`, so a future reader cannot check it against the
  repository; it comes from the phase brief.

  | Status | Meaning |
  |---|---|
  | **Proposed** | Drafted, not yet approved by a human. No authority. Work must not proceed. |
  | **Accepted** | Approved by a named human. Committed. Do not re-litigate without a new ADR. |
  | **Rejected** | Considered and declined. Kept, with its number, because the reasoning is the value. |
  | **Superseded by ADR-NNN** | Was Accepted, now replaced. Never deleted, never edited into agreement with its successor. |
  | **Illustrative** | Not a decision. Used only by the worked example in Part 3. |

- **Lifecycle.** An Accepted ADR is not edited to change its decision. It is superseded by a new
  ADR that cites it. The only permitted edits to an Accepted ADR are the Status line when it is
  superseded, and correction of a factually wrong evidence citation — which must itself be noted in
  the project log.

  **Carve-out pending §4.3.** As written, this rule would forbid correcting a false *claim* in an
  Accepted ADR in place, since that is a wrong claim rather than a wrong evidence citation. That
  would decide §4.3 by side effect: §4.3 offers the owner a genuine choice between correcting
  ADR-003/006/007/008 in place and superseding them, and adopting this lifecycle rule unamended
  removes the first option. This rule is therefore **suspended for those four ADRs** until §4.3 is
  answered. The owner should note that the template as drafted otherwise leans toward supersession.

## 1.7 Where ADRs live

Undecided, and deliberately not decided here — see the open questions in §4. The nine existing ADRs
are a single flat file under `scaffold/docs/`. This template does not assume either that new ADRs
append to that file or that they become separate files, and nothing in the template depends on the
answer.

---

# Part 2 — The template

Copy everything between the rules. Delete the parenthetical guidance as you fill each field. Do not
delete a field: if it does not apply, write "None" or "Not applicable" and say why in one line. A
field left blank is indistinguishable from a field nobody thought about.

---

```markdown
## ADR-NNN — <short decision title, stated as the decision, not the problem>

**Status:** Proposed | Accepted | Rejected | Superseded by ADR-NNN
**Date:** <D Month YYYY>
**Drafted by:** <name, or "an AI agent">
**Supersedes:** <ADR-NNN, or "None">

### Context

(Plain English. What situation forces a decision now? What is true today, and what breaks or stays
broken if nothing is decided? State the constraint that makes this a decision rather than a
preference. Cite current behaviour as `path:line` — this is a claim about the code and must be
checkable. If a fact here is inherited from an earlier document rather than verified now, say so.)

### Decision

(Plain English, one paragraph, present tense, unambiguous. Say what is being adopted, not what is
being explored. If the decision has conditions or a scope limit, state them here rather than
burying them in Consequences.

State explicitly whether this decision is *taken* or *taken and built*. These are different, and
conflating them is the defect this project exists to correct. If the decision is taken but not yet
implemented, write: "Decided; not implemented as of <date>.")

### Alternatives considered

(One row per real alternative. "Do nothing" is a real alternative and should usually appear. Do not
list a strawman — an alternative nobody would choose teaches a future reader nothing.)

| Alternative | Why rejected |
|---|---|
| <alternative> | <the actual reason, including anything that would make it the right choice later> |

### Consequences

**Positive.** (What this buys, concretely.)

**Negative.** (Required, and not optional. What this costs, what it forecloses, what it makes
harder, and what new risk it introduces. An ADR with no negative consequences has not been thought
about. If a consequence is a risk rather than a certainty, name it as a risk and cross-reference the
RAID register.)

**Consequences we do not yet know.** (Explicit. What would have to be measured or executed to find
out, and whether that has been done.)

### Determinism impact

(Required. Answer all four, each with Yes / No / Unknown, and justify anything that is not a plain
"No". "Unknown" is an acceptable answer; an unjustified "No" is not.)

| Question | Answer | Justification |
|---|---|---|
| Does this change what counts as authoritative state, or what may write it? | | |
| Does this change the number, order or source of RNG draws? | | |
| Does this change snapshot contents, event records, or any future ability to replay? (No replay capability currently exists — answer for the target contract in §1.4, not for a delivered one.) | | |
| Does this change a claim the project makes about determinism or reproducibility? | | |

(If any answer is Yes or Unknown: state whether the effect has been *measured* or is *expected*.
An expected effect is a prediction and must be labelled as one. Where a determinism claim is made,
use the fixed wordings in §1.4 verbatim.)

### Evidence

(Every factual claim above about current behaviour, restated as a checkable citation or a
reproducible command. Not a summary — a list a reader can work through.)

| Claim | Evidence |
|---|---|
| <claim as stated above> | `path:line`, or the exact command and its observed output |

**Not verified.** (List every claim in this ADR that rests on inference, on an earlier document, or
on something nobody has run. If the list is empty, say "None" — do not delete the heading.)

### Approval

**AI agents may draft this record. Under `HANDOFF.md` § Standing constraints (`:138`) an AI agent may not approve its own
decisions; under this template no AI agent approves any ADR (see §1.5, and open question 8).**

- **Approved by:** <name — leave blank until a human signs>
- **Date:** <leave blank until a human signs>
- **Approval covers:** <the decision as written above, and nothing implied beyond it>

An empty Approval block means this ADR has no authority and work must not proceed on it.
```

---

# Part 3 — Worked example

> **This example is illustrative only. It is NOT a decision anyone has taken, is not proposed, is
> not on any backlog, and must not be implemented.** It exists solely to show what a filled-in
> template looks like. It carries no number in the live sequence — `ADR-010` is taken (see §1.6) and
> the next real ADR is `ADR-011`.
> The evidence citations inside it are real, so that the citation style is realistic; the decision
> is not.

---

## ADR-EXAMPLE — *Illustrative only* — iterate cohorts in sorted `cohort_id` order

**Status:** Illustrative. Not a decision. Do not implement.
**Date:** 19 July 2026
**Drafted by:** an AI agent, as a template example
**Supersedes:** None

### Context

The tick loop iterates cohorts by plain list iteration over `self.cohorts`
(`scaffold/backend/app/simulation/engine.py:152`), and `self.cohorts` is built by appending one
`CohortAgent` per entry of the scenario file's `cohorts` array
(`scaffold/backend/app/simulation/engine.py:98-101`). Editing a scenario JSON therefore changes
iteration order. **Whether iteration order is load-bearing is not established.** Each cohort draws
from the shared RNG only if it has a non-empty grievance list
(`scaffold/backend/app/simulation/agents/cohort_agent.py:35-36`), so reordering matters only insofar
as it reorders the *drawing* cohorts relative to one another; a cohort with no grievances consumes no
draw and can be moved anywhere without effect. A3's executed result covers a change to draw *count*
(`A3-VERIFICATION-RESULTS.md:153-168`), not a change to consumer order, and so does not settle this.
Sorting by `cohort_id` would make iteration independent of file layout.

### Decision

*(Illustrative.)* Cohorts would be iterated in ascending `cohort_id` order rather than scenario-file
order. Decided; not implemented — and in this example, not decided at all.

### Alternatives considered

| Alternative | Why rejected |
|---|---|
| Do nothing; keep file order | File order is invisible in the data model, so a cosmetic JSON reorder could change which cohort receives which drawn drift value (`cohort_agent.py:35-38`). Whether any recorded figure actually moves is not established — see Consequences and Not verified |
| Give each cohort its own named RNG substream | Larger change; would make iteration order irrelevant rather than merely stable, so it addresses the cause instead of the symptom, but it is a separate decision |

### Consequences

**Positive.** Reordering a scenario file would stop changing results. Scenario authoring becomes
safe to tidy.

**Negative.** *(All of the following is reasoning from source structure. Nothing was executed — see
Not verified.)*

Per-cohort belief drift values would change **only if sorting changes the relative order of the
cohorts that actually draw** — those with a non-empty grievance list
(`scaffold/backend/app/simulation/agents/cohort_agent.py:35-36`). Cohorts with no grievances consume
no draw and can be reordered freely. Note that this is a narrower condition than "sorted order
differs from file order": the two can come apart, and a reader applying the looser test would reach
the wrong conclusion. Where the narrower condition does hold, each affected cohort receives a
different value from the same, unchanged sequence of draws
(`cohort_agent.py:35-38`) — what is drawn does not change; who receives it does.

For the shipped scenario, a reading of the file suggests the condition **does not** hold and the
effect may be nil. `kestral-strait.json` lists cohorts as `urban-professional-vantaran` (grievances
`[]` at `:66`), `coastal-creole-fishing`, `inland-highland-minority`, `military-veteran-families`,
`urban-nationalist-youth` (`:38`, `:78`, `:121`, `:161`, `:201`). Sorting ascending by `cohort_id`
moves only the grievance-free cohort, from first to last; the four drawing cohorts keep the same
relative sequence, so each would receive the value it receives today. This is static reading of the
scenario file, not a measurement, and it was not executed.

**Whether any macro output changes is NOT established, and the earlier draft of this example claimed
it did.** Reading the source suggests it may not: the number of cohort draws per tick depends on how
many cohorts have grievances, not on their order, so the macro noise draw
(`scaffold/backend/app/simulation/engine.py:135`) appears to land at an identical stream position;
and a snapshot contains macro state only (`scaffold/backend/app/simulation/agents/macro_state.py:49-51`),
which cohort beliefs do not write. On that reading the recorded macro figures would be unchanged and
would remain citable. This has not been measured and the prediction may be wrong in either
direction.

`test_same_seed_is_deterministic` compares only the final macro snapshot
(`scaffold/backend/tests/test_engine.py:36-40`) and inspects no cohort belief or narrative-adoption
value, so it would not detect this change regardless of whether the macro numbers move. That is a
gap in test coverage, not evidence either way about the macro values.

**Consequences we do not yet know.** Whether any recorded macro result changes at all, and if so
whether by an amount large enough to alter a conclusion in the audit; and whether per-cohort
narrative adoption changes — the diffusion graph is built once at construction from the scenario
array (`scaffold/backend/app/simulation/engine.py:102`) and is iterated by graph node
(`scaffold/backend/app/simulation/diffusion.py:64`, `for node in graph.nodes`) rather than by
`self.cohorts`, which suggests it may be unaffected, but this was not traced through and not
measured. Determining any of it requires re-running the evidence scripts in
`docs/delivery/evidence/`; that has not been done.

### Determinism impact

*(Filenames are shortened in these table cells for width. Every one of them resolves to a full path
in the Evidence table below, which is where a reader checks them.)*

| Question | Answer | Justification |
|---|---|---|
| Does this change what counts as authoritative state, or what may write it? | No | Iteration order only; the writers are unchanged (`engine.py:136`, `:164`, `:179`) |
| Does this change the number, order or source of RNG draws? | **Unknown** | Draw count, source, and the sequence of values pulled from the stream are all unchanged. Whether *which* cohort receives which value changes depends on whether sorting alters the relative order of the cohorts that actually draw — those with a non-empty grievance list (`cohort_agent.py:35`, iterated at `engine.py:152`). For `kestral-strait.json` a reading of the file suggests it does not: sorting moves only the grievance-free cohort, so the effect may be nil. Expected, not measured. Answered Unknown rather than No because a reordering of consumers would still be a change to draw order and must not be waved through |
| Does this change snapshot contents, event records, or any future ability to replay? | Unknown | Snapshot *shape* is unchanged — a snapshot is `self.state.model_dump()`, macro state only (`macro_state.py:49-51`), appended at `engine.py:180`. Whether snapshot *values* change is not established: macro state is not written by cohort beliefs, so it appears unaffected, but this has not been measured. No replay capability exists to affect |
| Does this change a claim the project makes about determinism or reproducibility? | **Unknown** | The fixed §1.4 wording remains literally true under either ordering. But if macro values did move, every reproducibility figure recorded in the audit and in A3 would need re-deriving before it could be cited again — a change to what the project can currently evidence, even though the permitted wording survives. Not measured |

The RNG effect is **expected, not measured.** Nothing was executed for this example.

A caution on the evidence, because getting this wrong is the failure mode this template exists to
prevent: A3's shared-stream result (`A3-VERIFICATION-RESULTS.md:153-168`) demonstrates that changing
the **number** of draws shifts every later draw. It does **not** cover a change in the **order of
consumers**, which is what this illustrative decision would do. Citing A3 here would be applying
evidence to a claim it does not support. It is named only to mark the distinction.

### Evidence

| Claim | Evidence |
|---|---|
| Cohorts are iterated by plain list order | `scaffold/backend/app/simulation/engine.py:152` |
| The three macro write paths are unchanged by this decision | `scaffold/backend/app/simulation/engine.py:136`, `:164`, `:179` |
| `self.cohorts` is built in scenario-file array order | `scaffold/backend/app/simulation/engine.py:98-101` |
| The cohort draw is conditional on a non-empty grievance list | `scaffold/backend/app/simulation/agents/cohort_agent.py:35-36` |
| The drift draw writes only that cohort's own belief | `scaffold/backend/app/simulation/agents/cohort_agent.py:35-38` |
| There is one RNG instance in application code | `scaffold/backend/app/simulation/engine.py:83` |
| Mesa maintains its own RNG, seeded in `Model.__new__` (from entropy on the API path) and read by no application code; the `seed=` kwarg at `engine.py:82` is **inert** | `CURRENT-STATE-AUDIT.md:319` (audit finding 27); `scaffold/backend/app/simulation/engine.py:82`. Inherited from the audit; Mesa is not installed here and its internals were not re-verified |
| There are three draw sites sharing the application RNG | `scaffold/backend/app/simulation/agents/cohort_agent.py:36`, `scaffold/backend/app/simulation/diffusion.py:75`, `scaffold/backend/app/simulation/engine.py:135` |
| A snapshot contains macro state only, so its shape is unchanged by cohort ordering | `scaffold/backend/app/simulation/agents/macro_state.py:49-51`; appended at `scaffold/backend/app/simulation/engine.py:180` |
| The diffusion graph is built once at construction, not per tick | `scaffold/backend/app/simulation/engine.py:102` |
| No replay capability exists | **Inherited, not re-verified, and not established by the citations below.** `A3-VERIFICATION-RESULTS.md:243` records that nothing is written to the database, which is a fact about persistence rather than about replay. `HANDOFF.md` § Standing constraints (`:135`) forbids *describing* the codebase as replay-capable, which is a constraint on wording and is not evidence about the code. No positive check for a replay path was run for this document |
| The determinism test compares only the final macro snapshot | `scaffold/backend/tests/test_engine.py:36-40` |
| Shifting draw **counts** moves macro indicators (not applicable to a consumer-order change) | `A3-VERIFICATION-RESULTS.md:153-168` |

**Not verified.** Whether sorting would in fact reorder the *drawing* cohorts relative to one another
for the shipped scenario. Reading `kestral-strait.json` suggests it would not — sorting moves only
the grievance-free cohort — in which case this decision changes nothing at all; but that is static
reading of a JSON file, not a measurement, and the relevant condition is the relative order of
drawing cohorts, not the looser question of whether sorted order differs from file order at all.
Whether any macro value moves.
The magnitude of any resulting change. Whether per-cohort narrative adoption is affected. Whether
`networkx` node traversal order would be affected. Nothing in this example was executed, and no
claim above was confirmed by running code.

### Approval

**AI agents may draft this record. Under `HANDOFF.md` § Standing constraints (`:138`) an AI agent may not approve its own
decisions; under this template no AI agent approves any ADR (see §1.5, and open question 8).**

- **Approved by:** *(none — this is an example and must never be signed)*
- **Date:** —
- **Approval covers:** nothing. This is not a decision.

---

# Part 4 — Open questions for the owner

These are decisions this document deliberately does not make. An AI agent may not resolve them.

1. **Adopt this template?** It is longer than the nine existing ADRs, which are roughly one
   paragraph each. The added length is the determinism, evidence and approval sections. Confirm the
   trade is worth it, or direct which sections to cut.

2. **Where do new ADRs live?** Append to `scaffold/docs/ARCHITECTURE_DECISIONS.md`, or start a new
   location such as `docs/adr/`? The existing file sits under `scaffold/`. The standing constraint
   on this phase forbids editing *code* under `scaffold/`; whether it extends to documentary edits
   in that tree is itself unsettled (see §1.6), and it bears on this answer. Numbering continues at
   `ADR-011` either way, but confirm that too. **This question is now live rather than hypothetical:**
   [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
   was filed at `docs/adr/` on 19 July 2026 and raises the same question as its own open question 2.
   Whether it is consolidated into `scaffold/docs/ARCHITECTURE_DECISIONS.md` or `docs/adr/` becomes
   the permanent home is unresolved and is the owner's to settle.

3. **Retrofit the existing nine?** ADR-003 (`:29`), ADR-006 (`:53-54`), ADR-007 (`:66-67`) and
   ADR-008 (`:75`) each state as present fact something the audit found the code does not do
   (section 6.1 of `CURRENT-STATE-AUDIT.md`, row 2 covering ADR-007; blockers B3 and B4 at
   `A3-VERIFICATION-RESULTS.md:243-244` covering ADR-003 and ADR-008; and blocker B1 at
   `A3-VERIFICATION-RESULTS.md:241` covering ADR-006's "validates a proposal's legality/feasibility"
   clause. Note that audit row 8, which covers ADR-006's *other* claim — the "sole writer of numeric
   state" phrasing — does **not** find that claim false: it records ownership as correct, calls the
   literal file-scoping wrong, and recommends rewording rather than refactoring. The
   "states as present fact something the code does not do" characterisation holds for ADR-006 via
   B1, not via row 8).
   **The four ADR line references were checked against the
   file; the code-side falsity is inherited from the audit and from A3 and was not re-verified for
   this document.** Two routes: correct them in place as Phase 0 documentary corrections, or leave
   them as the historical record and supersede them with new ADRs that state the position
   accurately. Note that §1.6's lifecycle rule as drafted would rule out the first route, which is
   why it is suspended for these four pending this answer. These produce very different histories.
   The choice is the owner's.

4. **Retrospective approval.** The existing nine carry no approver. Sign them retrospectively, or
   record explicitly that they predate the approval requirement?

5. **Extend the published status legend?** The legend at
   `scaffold/docs/ARCHITECTURE_DECISIONS.md:7` defines only "Accepted". Adding Proposed, Rejected,
   Superseded and Illustrative requires a documentary edit to a file under `scaffold/`, which is
   itself a scope question (see §1.6 and open question 2).

6. **Do the open section-8 decisions become ADRs?** Section 8 of the audit
   (`CURRENT-STATE-AUDIT.md:397-413`) lists seven items requiring human decision. **Four** have
   since been settled by founder decision — the licence, repository visibility, and the
   reproducibility wording (`HANDOFF.md:22-23`, `:13-19`, `:52-62`), and **the dual-use policy
   (8.6), settled on 18 July 2026**. The **two** that remain unsettled are the ABM substrate (8.3)
   and packaging tooling (8.5), plus the canonical plan format (8.7). *This draft reads 8.3 and 8.5
   as falling inside the categories in §1.2 and so as each needing an ADR on this template, and does
   not read 8.7 as doing so — but that reading rests on §1.2's right-hand column, which is itself
   drafter-authored and subject to owner approval. The owner should confirm or correct it rather
   than treat it as settled.*

   **On 8.6 specifically, and it does not behave like the other settled three.** It is publication
   blocker B5, and it is still the only blocker that cannot be cleared by correcting text —
   **settling it did not clear it.** The decision names eight controls and makes technical
   enforcement mandatory while disclosure and acceptable-use wording are supplementary, so B5 now
   clears by those controls being **implemented and verified**, none of which exists in code. For
   this template that raises a question rather than closing one: the licence, visibility and
   reproducibility decisions are settled *and discharged*, whereas 8.6 is settled and **outstanding
   as work**. Whether it still warrants an ADR — and whether one ADR covers all eight controls or
   each control that changes code needs its own — is not settled here. The framing at
   `A3-VERIFICATION-RESULTS.md:245-247` predates the decision; see the amendment appended to that
   file, and `PUBLICATION-EXIT-CRITERIA.md` C6.

7. **Does a documentary correction to a determinism or reproducibility claim require an ADR, or is
   it a correction of record?** An earlier draft of §1.3 answered this in its own voice, exempting
   Phase 0 documentary corrections. That answer has been withdrawn as outside an AI agent's
   authority, because it conflicts with the final row of §1.2 and with determinism question 4 in the
   template, and because `HANDOFF.md` § Standing constraints (`:139-140`) reserves "anything affecting determinism or
   authoritative state" for human approval. Concretely: does correcting `CHARTER.md:44`'s "guards in
   CI" (blocker B2), or ADR-003's persistence claim (B3), need sign-off? The question is live now —
   it governs P0.1 work already in the priority order. Stated neutrally, with no recommendation.

8. **Confirm the stricter approval reading.** `HANDOFF.md` § Standing constraints (`:138`) says AI agents may not approve
   **their own decisions**. This template applies the broader rule that no AI agent approves any
   ADR, drafted by itself or otherwise. The broader rule is the safer one, but it is this draft's
   extension of the cited text rather than the cited text itself, so it is put to the owner rather
   than assumed. Confirm the stricter reading is intended, or narrow it to the cited wording.

---

# Part 5 — Provenance of this document

This document was drafted on 18 July 2026 and revised on 19 July 2026 after adversarial review. The
provenance below describes the revised version. An earlier version of this section claimed a broader
act of verification than had taken place; that is the exact conflation this template exists to
prevent, and it is corrected here rather than quietly dropped.

**Verified by opening the file and reading the cited lines**, during the original draft or the
revision:

- the ADR count, numbering and status legend (`scaffold/docs/ARCHITECTURE_DECISIONS.md:1-83` — the
  file is 83 lines; an earlier version of this section cited `:1-84`, a line that does not exist)
- the four ADR lines carrying blocker-related claims (`:29`, `:53-54`, `:66-67`, `:75`)
- the approval and category constraints (`HANDOFF.md` § Standing constraints (`:138-140`)), including the exact wording "may not
  approve their own decisions" at `:130`
- the fixed determinism wordings (`HANDOFF.md:52-62`) and the standing constraint at `HANDOFF.md` § Standing constraints (`:135`)
- the blocker table (`A3-VERIFICATION-RESULTS.md:237-247`) and the shared-stream result and
  mechanism (`A3-VERIFICATION-RESULTS.md:153-168`)
- audit finding 27 on Mesa's second RNG (`CURRENT-STATE-AUDIT.md:319`) and the section 6.1 table,
  including row 8 on ADR-006, whose Reality column recommends rewording rather than finding the
  claim false
- the two-layer requirement (`HANDOFF.md:37`) and the standing-constraints block (`HANDOFF.md` § Standing constraints (`:133-140`))
- audit section 8 (`CURRENT-STATE-AUDIT.md:397-413`), confirmed as seven items, not four
- for the revision specifically, four source files re-read to check the worked example's reasoning:
  `scaffold/backend/app/simulation/engine.py`, `agents/cohort_agent.py`, `agents/macro_state.py` and
  `diffusion.py`
- for the second revision, the cohort ordering in `scaffold/scenarios/kestral-strait.json`
  (`:38`, `:66`, `:78`, `:121`, `:161`, `:201`), read to test the worked example's stated condition

**Not verified.**

- **No code was executed for this document, and no test was run.** Every code-side statement rests on
  reading source, not on observed runtime behaviour.
- The worked example's determinism reasoning is inference from source structure. Its central
  prediction — that macro output appears unaffected by cohort iteration order — is unmeasured and may
  be wrong in either direction. An earlier version of the example asserted the opposite conclusion
  with equal confidence, which is why the prediction is now stated conditionally.
- A second revision corrected the *condition* under which the example's effect would occur. An
  earlier version stated it as "if sorted order differs from file order"; the operative condition is
  narrower — whether sorting reorders the cohorts that actually draw. For `kestral-strait.json` the
  two come apart, and under the narrower condition the example's effect appears to be nil. That
  reading is from the scenario file and the guard at `cohort_agent.py:35`; nothing was executed.
- Mesa's internals were not re-verified. The statement that the `seed=` kwarg at `engine.py:82` is
  inert is inherited from audit finding 27; Mesa is not installed in the drafting environment. An
  earlier version of this document asserted the opposite — that the call seeds Mesa's RNG — while
  citing the finding that says it does not.
- **§4 item 3 rests on inherited findings, not on re-verification.** The claim that ADR-003, 006, 007
  and 008 state as present fact something the code does not do comes from the audit and from A3. The
  ADR line references were checked; the code-side falsity was not re-derived, because re-deriving it
  would mean reopening a closed audit.
- Likewise the statements that nothing is written to the database (B3) and that no replay capability
  exists are inherited from A3 and from `HANDOFF.md` § Standing constraints (`:135`), not verified here.
- Whether every existing governance record satisfies the two-layer requirement in §1.4 was not
  checked.
- Whether this template is workable in practice is untested — it has been applied to one illustrative
  example and to no real decision.
