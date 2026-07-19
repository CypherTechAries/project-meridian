# Publication Exit Criteria

**Status:** DRAFT — pending owner review. Nothing in this document is approved.
**Date drafted:** 19 July 2026 (revised). All statuses observed 19 July 2026 against the working
tree at commit `71fa329` (committed 18 July 2026 22:41 +0100) **plus ten untracked paths** — not
against the commit alone. See C12 check 4.
**Amended:** 19 July 2026, to carry founder decision **P0.4A — deterministic randomness
architecture** (issued 18 July 2026) into this gate. The amendment adds criterion **C8A**, a note
under C8, a clause to C9, three open questions (13–15) and one sign-off row. Nothing else was
changed, and **no pre-existing status was re-verified as part of it** — the statuses above C8A
still date from the original draft.
**Amended again:** 19 July 2026, to carry founder decision **B5 / P0.8 — dual-use position**
(issued 18 July 2026) into this gate. That amendment rewrites **C6**, corrects the blocker table and
the plain-English summary, replaces open question 1 with four narrower ones (16–19) and adds a
per-control sign-off table. **It enlarges this gate.** B5 previously cleared when the owner made a
judgement; it now clears only when eight named controls are implemented and verified. No status
recorded before this amendment was re-verified as part of it, and no code was executed for it.
**Amended a third time:** 19 July 2026, to record the founder correction on **Track C — the
interview-demonstration programme** (issued 19 July 2026). That amendment adds **one** criterion,
**C13A**, covering fixture-backed prototype artefacts *inside the repository*; a paragraph to the
plain-English summary; three open questions (20–22); one sign-off row; and three conforming
mentions of C13A where the document enumerates its own criteria (C14, the visibility flip, and step
1 of the flip sequence). **It deliberately does not add the five Track C gates C0–C4 to this gate**
— the reasoning is stated under C13A and in the summary below, and it is a scope judgement the owner
may reverse. No pre-existing status was re-verified as part of it, and no code was executed for it.
**Conforming corrections, 19 July 2026.** Three cross-references the third amendment left
one-directional were completed. C13A is now named alongside C2, C3, C5, C8 and C13 in the
`grep`-exclusion consequence note and in open question 11 — C13A's own text already asserted that
relationship, and neither of those two places acknowledged it. The C14 attestation sentence in the
sign-off block, which read "C1 to C13 pass", now names C8A and C13A, which the visibility-flip
section and C14 itself already required of it. **No criterion was added, no pass condition was
changed, no status was re-verified, and no code was executed.**
**Phase:** B (governance bootstrap)
**Drafted by:** AI agent. An AI agent may draft this record. An AI agent may not approve it,
and may not tick criterion C14.

Source documents: [`../../HANDOFF.md`](../../HANDOFF.md) (publication exit criteria, standing
constraints), [`A3-VERIFICATION-RESULTS.md`](A3-VERIFICATION-RESULTS.md) (blockers B1–B5),
[`CURRENT-STATE-AUDIT.md`](CURRENT-STATE-AUDIT.md) (§8 human decisions, §9 phased correction).
Three further sources are **not** documents in this repository: the founder decision of 18 July 2026
establishing P0.4A; the founder decision of the same date settling B5 and specifying its eight
controls; and the founder correction of 19 July 2026 on Track C. None has a source record in the
tree. See C8A, C6, C13A and open question 13.

---

## Plain-English summary

This is the gate. The MERIDIAN repository is private on purpose. It becomes public only when
every criterion below passes **and** the owner signs off in writing.

The reason the gate exists is narrow and specific. The code in this repository is an early
scaffold, and that is fine — a scaffold is allowed to be incomplete. What is not allowed is
documentation that describes capabilities the code does not have. That is the project's worst
defect, and publishing it would put the weakest artefact in front of the audience the project
is meant to impress.

Much of this gate was originally about correcting sentences rather than building anything. **That is
no longer an accurate description of it, and the change is not cosmetic.** Four of the five
publication blockers — B1 to B4 — are still cleared by correcting sentences. The fifth is not, and
it is no longer cleared by a decision either.

**B5 is decided, and deciding it made the gate bigger.** On 18 July 2026 the founder settled the
dual-use position that B5 was waiting on. The earlier framing in this file and in its sources — "four
of five clear by telling the truth, only B5 needs a decision" — described a gate in which the
expensive-looking blocker was in fact one signature away from closing. That framing is now wrong.
The decision names **eight controls**, and the eighth states that disclosure and any future
acceptable-use language are *supplementary* while **technical enforcement is mandatory**. So B5 now
clears only when the other seven controls are implemented in code and verified by test. None of them
is built. Reading the old framing forward would understate the remaining work by the entire
enforcement effort. **C6** carries the eight controls and a verifiable criterion for each.

The gate also carries a second condition that no amount of editing can satisfy. On 18 July 2026 the
founder established **P0.4A — deterministic randomness architecture** as a Phase 0 workstream,
sitting between P0.4 and P0.5. `HANDOFF.md:13` makes publication conditional on Phase 0 corrections
passing, so a new Phase 0 workstream is by that route a new publication dependency. **C8A** records
it. Most of its pass conditions are isolation tests that do not exist over an architecture that has
not been built, which makes C8A the first criterion in this file whose pass condition requires
working code rather than corrected prose. That is a real enlargement of the gate, and it is stated
here rather than absorbed quietly.

**Track C was assessed against this gate and mostly kept out of it, deliberately.** The founder
correction of 19 July 2026 establishes Track C — the interview-demonstration programme — as two
lanes and five gates, C0 to C4. Those five are gates on a *demonstration*, not on publication.
Publication does not wait for a demonstration, `HANDOFF.md` § Publication exit criteria (`:96-102`) does not mention one, and A3
records no blocker that a demonstration would clear. Adding C0–C4 here would inflate this gate with
conditions no source asks of it, and this draft does not do that. **One part of Track C is
genuinely publication-relevant, and only one.** Lane C-VISUAL may build screens on fixture data
long before the engine can produce what they show, on the condition that every fixture-backed
surface visibly states that it is a prototype not connected to the simulation engine. If such an
artefact is committed, it publishes with the repository — an unlabelled one would then be exactly
the defect B1 to B4 exist to correct, in a form a reader believes faster than prose. **C13A**
carries that one condition and nothing else. It is drafter-proposed and reaches only what is in the
tree; the wider exposure — a cropped screenshot circulating outside the repository — is not
something a repository gate can close, and is recorded as risk R10 in `RAID-REGISTER.md` rather
than pretended away here.

Every criterion below is written so that a reader can check it themselves. Each one gives an
exact command and states what output counts as a pass. Where a criterion cannot yet be reduced
to a command — because a prerequisite decision is still open, or because the code it would exercise
does not exist yet — that is said plainly rather than papered over.

---

## How to read a criterion

| Field | Meaning |
|---|---|
| **Source** | Which document requires it (HANDOFF checklist item, blocker BN, or audit §9). |
| **Plain English** | What the criterion is actually protecting against. |
| **Verify by** | The exact command to run, from the repository root unless stated otherwise. |
| **Passes when** | The output that counts as a pass. Where a criterion needs a human judgement rather than a command result, this is stated in the criterion and the judgement must be recorded. |
| **Status today** | Observed on 19 July 2026 against the working tree at commit `71fa329` **plus ten untracked paths** (see C12 check 4) — not against the commit alone. Counts that depend on untracked content are marked where they occur. Re-run before sign-off. |

Commands are given in POSIX shell (Git Bash on Windows, or any Linux shell).

**On the `grep` exclusions. [drafter-proposed] — this is a gate-design change, not a sourced
requirement.** Greps that hunt for false *claims* exclude `./docs/`, because the records under
`docs/delivery/`, `docs/design/`, `docs/safety/` and `docs/world-model/` quote those claims in
order to correct or build on them; a hit inside them is not a defect. This exclusion was widened
from `./docs/delivery/` by the drafter on 19 July 2026, after new planning directories appeared in
the working tree and began tripping the detectors.

> **Consequence, stated explicitly.** The widening materially narrows what this gate can detect.
> C2, C3, C5, C8, C13 and — since the Track C amendment — **C13A** now structurally cannot surface a
> false capability claim written into
> `docs/design/`, `docs/safety/` or `docs/world-model/` — all three of which are intended for
> commit (C12 check 4 lists them as paths to be "committed or removed") and will therefore publish
> with the repository. C3's status section already shows the effect: `docs/world-model/PERSON-MODEL.md:168`
> is surfaced only as a manual aside, not by the criterion's own command. **C13A's exposure is the
> sharpest of the six**, and it is a target rather than an observed failure because nothing in Track
> C is built: `docs/design/` is precisely where a fixture-backed mock-up would be placed, so the one
> class of surface C13A exists to catch is the class this exclusion would hide. See open question 21.
> Note also that the
> audit's own Phase 0 exit criterion at `CURRENT-STATE-AUDIT.md:433` specifies the `in CI` grep
> with **no exclusion at all**. "They were tripping the detectors" is the reasoning that turns a
> gate into a formality, and changing a gate's sensitivity is an owner decision, not a drafter's.
> Whether the exclusion should be narrowed back to `./docs/delivery/` plus a per-file allowlist,
> so that publishable planning records remain in scope, is recorded as **open question 11** and is
> not settled here.

Greps that establish facts about the repository as a whole — C11 and all of C12 — deliberately do
**not** exclude anything, since a secrets or content review must cover everything. C10's second
check excludes nothing under `docs/` but is **scoped to `scaffold/backend/app`**; it does not cover
`scaffold/backend/tests/` or any `.py` elsewhere under `scaffold/`. See C10.

**Sourcing marker.** Some criteria below record process steps (who adjudicates, what gets written
into the sign-off block). Where a step is *not* required by `HANDOFF.md`, the audit or A3, it is
labelled **[drafter-proposed]** and is for the owner to accept, amend or drop.

---

## Blocker position, stated once

Two verbatim statements from [`A3-VERIFICATION-RESULTS.md`](A3-VERIFICATION-RESULTS.md), quoted
separately because they sit at different locations:

> **Publication blockers after A3: 5 (unchanged).** No new blocker was created. No result forces
> the broad audit back open.

— `A3-VERIFICATION-RESULTS.md:17`.

> Four of five clear by telling the truth. Only B5 needs a decision.

— `A3-VERIFICATION-RESULTS.md:247`. **This second sentence is superseded and must not be carried
forward.** It is quoted here because it is what the source says, not because it is still true. See
the correction under the table.

| # | Blocker | Clears by | This gate |
|---|---|---|---|
| B1 | Documents claim the engine validates legality and feasibility. It does not. | Text correction. Implementing the evaluator is **not** required. | C2 |
| B2 | Determinism boundary claimed as guarded in CI. There is no CI and no `.git`. [†] | Text correction, or build the guard. | C3 |
| B3 | Three tables claimed persisted. Nothing is written to the database. | Text correction. | C4 |
| B4 | "Adding an archetype requires only a new JSON" is false and fails silently. | Text correction. | C5 |
| B5 | Dual-use influence-targeting schema with no acceptable-use terms. | ~~**Owner decision** (P0.8)~~ **Superseded [‡].** The owner decision was taken on 18 July 2026 and B5 did **not** clear with it. B5 now clears only when the eight controls that decision names are **implemented and verified**. | C6 |

**[†]** The B1–B4 rows above reproduce `A3-VERIFICATION-RESULTS.md:239-245` verbatim, including B2's
`.git` clause, which is now stale. Those rows are left unedited so a reader comparing this table to
A3 finds them identical; the correction is immediately below.

**[‡] B5's "clears by" column is deliberately *not* left verbatim**, and it is the one row in this
table that departs from A3. Leaving "Owner decision" in place would tell a reader that the most
expensive remaining blocker is one signature from closing, which is the opposite of the position
after 18 July 2026. A stale citation is a nuisance; a stale *clearance route* would misdirect the
work. The verbatim A3 wording is preserved in the quotation above the table so nothing is lost.

**The correction, stated once and in full.** A3 says four of five blockers clear by telling the
truth and only B5 needs a decision. As of 18 July 2026:

- The first half still holds. B1, B2, B3 and B4 clear by text correction (B2 alternatively by
  building the guard).
- **The second half does not.** B5's decision has been taken. It did not clear B5. The decision
  requires that influence mechanics run only in explicitly fictional worlds; that the scenario
  loader require `world_mode: fictional` and fail closed without it; that real-world scenario
  import stay disabled; that real persons, organisations and political populations not be
  influence-target entities; that protected characteristics not be optimisation criteria for
  persuasion or manipulation; that fictional aggregate diffusion, exposure, adoption and
  counter-messaging remain allowed; that the API and UI disclose that the active world is
  fictional; and that **disclosure and any future acceptable-use language be treated as
  supplementary, with technical enforcement mandatory.**
- **The gate is therefore larger than it was, not smaller.** Of the fourteen criteria in this file,
  two — C6 and C8A — now require working code. Before 18 July 2026, one did.

One correction to B2's own wording, recorded here so the gate is not checked against a stale
premise. B2 as written says "There is no CI **and no `.git`**". The `.git` half is now false:
the repository is under version control at commit `71fa329` on branch `main`, with a remote
`origin` configured. The "no CI" half is still true and is what C3 tests.

> **Verify:** `git log --oneline` → `71fa329 Initial commit: MERIDIAN scaffold, charter, and
> current-state audit`; `ls -a .github` → `No such file or directory`.

---

## The criteria

### C1 — Documented clean installation works on a supported environment

**Source:** HANDOFF checklist item 1; P0.2.

**Plain English.** Somebody who clones this repository and follows the README must end up with a
working environment. Whether they do is **not established here**. The dependency list declares a
package the code never imports, and `HANDOFF.md:45-48` reports that this package breaks the
install — `litellm` resolving to 1.92.0, which has no cp313 wheel, falls back to sdist and needs a
Rust toolchain; because pip resolves before installing, nothing installs. **That report was not
reproduced for this draft.**

**Verify by.** On a clean machine with no existing virtual environment, follow the README's
install section verbatim, then:

```
cd scaffold/backend && python -m pytest tests -v
```

**Passes when.** The documented install command completes with exit code 0 on a supported
environment, and the test command reports `5 passed`.

> **Scope not settled — owner decision.** `HANDOFF.md` § Publication exit criteria (`:96`) reads "Documented clean installation
> works on a supported environment" — singular, and it does not name one. (No emphasis in the
> source; the quotation is plain there.) But `HANDOFF.md:72-73`, item P0.2 in the founder-set
> priority order, requires a "Clean-environment command that succeeds on **Windows and Linux**."
> Whether that Phase 0 work requirement carries into this publication exit criterion, or whether
> one environment suffices at the gate, is the open question — this draft does not decide it, and
> notes that C1's pass condition as written is weaker than what P0.2 already requires. The
> question also interacts with the still-open audit §8.5 (packaging). See open question 7.
> **[drafter-proposed]** Whatever is run should be recorded in the sign-off block with the
> interpreter version used.

**Status today: NOT VERIFIED — cannot be ticked.** Not "failing": no environment was created and
nothing was installed for this draft, so whether the documented install succeeds, and whether the
suite reports the `5 passed` this criterion's pass condition specifies, is **unknown**. What is
verified is only the precondition: `litellm>=1.34,<2.0` is still declared at
`scaffold/backend/requirements.txt:20` and is imported by no executable code — its only textual
occurrences are inside the module docstring at `scaffold/backend/app/simulation/llm_gateway.py:17-18`.
The five test *functions* exist (`test_engine.py:25,34,43,52,61`, confirmed by grep at C9); whether
they currently pass is verified nowhere in this draft.

> **Not verified by this draft.** Whether `pip install -r requirements.txt` in fact fails, and
> whether `litellm` resolves to 1.92.0, is reported at `HANDOFF.md:45-48` and was not reproduced
> here — no environment was created and nothing was installed. Treat the failure mode as
> second-hand until C1 is actually executed at gate time.

> **Depends on an open decision.** Audit §8 item 5 (adopt `uv` and `pyproject.toml`) is
> unresolved, so the exact install command cannot be fixed in this draft. Whoever resolves 8.5
> must write the resulting command into this criterion before it can be ticked.

---

### C2 — B1: no document claims the engine validates legality or feasibility

**Source:** Blocker B1; HANDOFF checklist item 2; P0.1.

**Plain English.** `_validate_and_price` does not validate anything. It looks up the action name
in a seven-row table and returns a copy of the row (`scaffold/backend/app/simulation/engine.py:121-130`).
There is no legality check, no feasibility check and no cost computation. Documents and docstrings
that say otherwise must be corrected. A3 is explicit that **building the evaluator is not
required** to clear this — only telling the truth is.

**Verify by.**

```
grep -rn "validates legality\|engine validates\|priced, validated\|rejects invalid" \
  --include="*.md" --include="*.py" . | grep -v "^./docs/"
```

**Passes when.** Every remaining line is either absent, or reworded so the claim is conditional,
aspirational or explicitly labelled as not implemented. A zero-hit result is sufficient but not
necessary. **[drafter-proposed]** A reviewer adjudicates each line individually and records the
disposition.

**Status today: NOT PASSING.** As of 19 July 2026 the grep returns 10 lines outside `./docs/`
(with the narrower `./docs/delivery/` exclusion it returns 11, the extra being a planning record
under `docs/world-model/`):

| Location | Text |
|---|---|
| `CHARTER.md:112-113` | "then priced, validated and / resolved by the engine" (the claim spans two lines; the grep matches `:112`) |
| `README.md:38` | "LLM proposes; engine validates legality and computes cost/effect" |
| `README.md:41` | "engine rejects invalid actions" |
| `scaffold/README.md:19` | "the engine validates legality and computes effects" |
| `scaffold/backend/app/api/routes_simulation.py:4` | "the engine validates and prices them" |
| `scaffold/backend/app/simulation/engine.py:4` | "the engine here validates legality and computes/applies effects" |
| `scaffold/backend/app/simulation/engine.py:158` | "engine validates + applies" (comment) |
| `scaffold/backend/app/simulation/agents/institutional_agent.py:4` | "the engine ... validates legality and computes effects" |
| `scaffold/backend/app/simulation/llm_gateway.py:60` | "The engine validates legality" |
| `scaffold/backend/app/simulation/schemas/agent_schema.py:8` | "the engine validates and applies effects" |

**Provenance of these ten.** Seven are instances already enumerated in the audit and A3. Three —
`llm_gateway.py:60`, `agent_schema.py:8` and `engine.py:158` — were surfaced by this criterion's
own grep. They are further instances of the same already-identified B1 claim, not new findings,
and no new investigation was opened to produce them.

Note the counterpart at `CHARTER.md:113-114` — "The LLM may *propose* a composition; it never
decides whether the composition is legal" — is **true** and must not be edited. A3 correction 4
makes this distinction explicitly: `:112` is the false clause, `:114` is the sound one.

Two adjacent claims share the same root and should be corrected in the same pass, though they do
not match the grep above:

- `scaffold/backend/app/simulation/schemas/agent_schema.py:181-183` describes `constraints` as
  "Hard legal/procedural constraints on the agent". A3 §3 recorded a substitution result — a
  40-tick hash identical with and without them — concluding they are causally inert. **Carried
  from A3, not reproduced here** (that result required executing the engine; this draft ran no
  code).
- `scaffold/backend/app/simulation/schemas/agent_schema.py:242-244` and its published mirror
  `scaffold/schemas/intervention.schema.json:50` describe `legal_check` as "set by the engine".
  That it is set by no code is confirmed here by grep. That the client's own value is echoed back
  and trusted was recorded by A3 §5 from a `TestClient` run and is **carried from A3, not
  reproduced here**.

---

### C3 — B2: no document claims a CI guard that does not exist

**Source:** Blocker B2; P0.1 and P0.3.

**Plain English.** The charter says a test "guards in CI". There is no CI. Either delete the
claim or build the pipeline — HANDOFF's P0.3 permits building it, but only with "checks that
genuinely exist and pass".

**Verify by.**

```
grep -rn "in CI" --include="*.md" --include="*.py" --include="*.html" . \
  | grep -v "^./docs/"
ls -a .github
find . -path ./.git -prune -o \( -name "*.yml" -o -name "*.yaml" \) -print
```

**Passes when.** Either (a) the grep returns no lines outside `docs/`, or (b) a CI
workflow exists under `.github/workflows/`. **[drafter-proposed]** A3 records only that B2 clears
by "Text correction, or build the guard"; the drafter suggests that under (b) the workflow should
additionally have run green on `main`, that every check the documents claim should actually be one
of the jobs in it, and that the workflow run URL should be recorded in the sign-off block. None of
those three is traceable to A3, `HANDOFF.md` or the audit — they are the drafter's additions and
are for the owner to accept, amend or drop.

**Status today: NOT PASSING.** As of 19 July 2026 the grep returns one line outside `./docs/`,
`CHARTER.md:44`:
"(ADR-006) enforces in code and `test_llm_gateway_cannot_write_state` guards in CI." `ls -a .github`
returns `No such file or directory`, and the `find` above returns exactly one path,
`./scaffold/docker-compose.yml` — the only YAML anywhere in the tree.

With the narrower `./docs/delivery/` exclusion the grep returns a second line,
`docs/world-model/PERSON-MODEL.md:168` ("Sensitivity tests must run in CI"). **This draft does not
adjudicate that line.** The drafter's earlier characterisation of it as a forward-looking planning
record was made without opening the file (C12 check 4 records that none of the `docs/world-model/`
files was opened), and the criterion's own pass condition reserves per-line adjudication to a
reviewer. It is flagged, not disposed of. Its visibility to this gate at all depends on open
question 11.

---

### C4 — B3: no document claims persistence that does not happen

**Source:** Blocker B3; P0.1.

**Plain English.** Three database tables are defined. Nothing ever writes a row to any of them.
The architecture record states in the present tense that the system persists them.

**Verify by.**

```
grep -rn "We persist three things" --include="*.md" . | grep -v "^./docs/"
grep -rn "SimulationRun\|StateSnapshot\|EventLog\|get_db" scaffold/backend/app
```

**Passes when.** The first grep returns no unqualified present-tense persistence claim — the
wording must be either removed or marked as a target rather than a delivered capability. The
second grep is a supporting check, not a pass condition: as long as it returns only definitions
in `db/models.py` and `db/session.py` with no call sites, the persistence claim must stay
qualified.

**Status today: NOT PASSING.** `scaffold/docs/ARCHITECTURE_DECISIONS.md:29` (ADR-003, status
*Accepted*, present tense) reads "We persist three things: `simulation_run` (seed + scenario),
immutable `state_snapshot` per tick, and an append-only `event_log`."
`scaffold/README.md:41` likewise places "PostgreSQL (simulation_run, state_snapshot, event_log)"
at the end of the architecture diagram with no "planned" annotation.

---

### C5 — B4: the archetype-extensibility claim is corrected

**Source:** Blocker B4; P0.1.

**Plain English.** The documents say adding a nation archetype needs only a new JSON file and
never an engine change. A3 recorded that this is false and, worse, fails silently — an unknown
key in a delta is skipped without error, warning or log
(`scaffold/backend/app/simulation/agents/macro_state.py:36-38`).

**Verify by.**

```
grep -rn "data, not code\|only a new" --include="*.md" . | grep -v "^./docs/"
```

**Passes when.** Each remaining line is either removed or carries an explicit caveat naming the
silent-failure behaviour. **[drafter-proposed]** A reviewer records the disposition of each line.

**Status today: NOT PASSING.** As of 19 July 2026 the grep returns 5 lines. All five are listed;
the first four state the claim in terms the audit and A3 already identified:

- `README.md:72-74` — "Nation archetypes are **data, not code**. Adding one means adding a
  scenario-template JSON ... never editing the engine."
- `scaffold/README.md:106-107` — "Nation types are **data, not code** (PLAN.pdf §9)"
- `scaffold/docs/ARCHITECTURE_DECISIONS.md:69` — the ADR-008 heading itself, "Nation types are
  data, not code"
- `scaffold/docs/ARCHITECTURE_DECISIONS.md:75` — "eighth archetype must require only a new
  `scenarios/*.json`"
- `scaffold/docs/ARCHITECTURE_DECISIONS.md:31` — "generic across nation archetypes (data, not code —
  see ADR-007)". Quoted so the reviewer has the text, not to pre-judge it. *(An earlier draft said
  "All five are listed" but listed only four, omitting this line even though the provenance paragraph
  below names it.)*

**Provenance of these five.** Three — `README.md:72-74`, `scaffold/README.md:106-107` and
`scaffold/docs/ARCHITECTURE_DECISIONS.md:75` — are instances already enumerated in the audit and
A3. Two — `scaffold/docs/ARCHITECTURE_DECISIONS.md:69` (the ADR-008 heading) and `:31` — were
surfaced by this criterion's own grep. They are further instances of the same already-identified
B4 claim, not new findings, and no new investigation was opened to produce them. **This draft does
not adjudicate the disposition of any of the five**; per the pass condition above, a reviewer
records each.

`scaffold/CLAUDE.md:53-55` ("Do **not** edit the engine") restates the same instruction and
should be corrected in the same pass.

---

### C6 — B5: the eight dual-use controls are implemented and verified

**Source:** Blocker B5; audit §8 decision 6; P0.8; **founder decision of 18 July 2026, which settled
the policy and specified the eight controls.**

> **Criterion rewritten 19 July 2026, and its nature changed.** This criterion was previously titled
> "dual-use policy decided by the owner" and passed when a dated owner decision existed in the tree.
> The owner decision was taken on 18 July 2026. **The criterion did not thereby pass.** The decision
> makes technical enforcement mandatory and disclosure supplementary, so C6 now passes only when
> eight controls exist in code and are demonstrated by test. This is the single largest change to
> this gate since it was drafted, and it is an enlargement.
>
> **Sourcing gap, same as C8A.** The founder decision of 18 July 2026 has **no source record in the
> repository**; `../world-model/FOUNDER-REQUIREMENT-2026-07-18.md` is the world-model record and does
> not contain it. The eight controls below are therefore cited by date, not by file and line, and a
> reviewer cannot verify this criterion's authority from the tree alone. See open question 13, which
> asks the same thing for P0.4A and applies here unchanged.

**Plain English.** MERIDIAN ships a schema that can express an influence operation in
operational detail: which population segments to target, which pre-existing grievance to exploit,
which media channels reach them, how persuadable each segment is to authority, identity or
economic appeals, a claim explicitly markable `truth_status: "false"`, a messenger with a
`perceived_independence` score, a count of coordinated amplification accounts, and a
`desired_behaviour` to produce. The demo scenario populates all of it.

The **campaign object itself** is loaded and read by no code
(`scaffold/backend/app/simulation/engine.py:111` is its only occurrence), so no campaign field —
targeting, narrative, messenger, amplification, `truth_status`, `desired_behaviour` — currently
affects any computation.

The **cohort-side targeting fields are not all inert**, and this criterion must not be read as
saying they are. `influence_susceptibility`'s three appeal channels (authority, identity, economic)
are averaged into a single susceptibility score
(`scaffold/backend/app/simulation/agents/cohort_agent.py:22-26`) and that score drives the
per-cohort gain in the diffusion model
(`scaffold/backend/app/simulation/diffusion.py:74-76`: `gain = suscept * (influence +
seed_pressure) + jitter`). `network_position.internal_cohesion` and `bridges_to` build the
influence graph and weight its edges (`scaffold/backend/app/simulation/diffusion.py:18-37`).

`grievances` is a further, partial exception, and it must not be omitted from this list. Its
*contents* drive nothing — no grievance string is read — but the **non-emptiness of the list** gates
a per-tick decrement of `beliefs.government_competence` and one RNG draw
(`scaffold/backend/app/simulation/agents/cohort_agent.py:35-38`: `if self.cohort.grievances:`).
That makes it, besides susceptibility and cohesion, the only cohort field that writes authoritative
meso state, and it also shifts the shared RNG stream — a cohort with an empty grievance list
consumes zero draws that tick.

The remaining segmentation fields — demographics, media exposure and the campaign vocabulary — are
parsed and range-checked but drive nothing further.

Both of those are facts about today's engine, not safeguards. They matter more after 18 July 2026
than before it: control B5-5 forbids protected characteristics from acting as optimisation criteria
for persuasion, and an appeal channel literally named *identity* already feeds a persuasion
computation. Whether that is inside the prohibition is open question 17.

This criterion **cannot be cleared by an AI agent, and cannot be cleared by editing text.** It
previously could not be cleared because the owner had not chosen a position. It now cannot be
cleared because the position the owner chose requires code that does not exist.

**Superseded framing.** The audit's four options (`CURRENT-STATE-AUDIT.md:411`) — an acceptable-use
or field-of-use restriction in the licence; an enforced `fictional: true` assertion plus a
real-entity check at scenario load; surfacing the fiction disclaimer in every API response and the
UI; or keeping the repository private — are no longer the live menu. The decision is broader than
any of them, and its eighth control reclassifies the licence-side and disclosure-side options as
*supplementary*. Keeping the repository private is not among the adopted controls; it remains the
present state under settled audit decision 8.2, not a substitute for enforcement.

#### The decision, in the founder's terms

| # | Control | Class |
|---|---|---|
| B5-1 | Influence mechanics operate **only** in explicitly fictional worlds. | Enforcement |
| B5-2 | The scenario loader **requires** `world_mode: fictional` and **fails closed** when it is missing. | Enforcement |
| B5-3 | Real-world scenario import remains **disabled**. | Enforcement |
| B5-4 | Real persons, organisations and political populations **cannot** be influence-target entities. | Enforcement |
| B5-5 | Protected characteristics **cannot** be used as optimisation criteria for persuasion or manipulation. | Enforcement |
| B5-6 | Fictional **aggregate** narrative diffusion, exposure, adoption and counter-messaging **remain allowed**. | Permitted scope — a boundary, not a restriction |
| B5-7 | API and UI **disclose** that the active world is fictional. | Enforcement (API) + interface obligation (UI) |
| B5-8 | Disclosure and any future acceptable-use language are **supplementary. Technical enforcement is mandatory.** | Governing rule over B5-1 to B5-7 |

**The identity and bias distinction, quoted rather than paraphrased:**

> **Permitted:** identity affects lived experience, relationships, discrimination, institutional
> access, media exposure and cultural interpretation.
>
> **Not permitted:** identity acts as an inherent competence, morality, loyalty, violence or
> manipulability coefficient.

The campaign model **may** use non-sensitive factors — geography, institutional affiliation,
economic exposure, political behaviour, media consumption — where justified by the fictional
scenario. It **must not** optimise against protected traits.

**Two of the eight are not enforcement controls, and this criterion does not pretend otherwise.**
B5-6 states what remains permitted, so its verifiable form is a non-regression check: enforcing the
other seven must not disable aggregate diffusion. B5-8 governs how the other seven may be
discharged, so its verifiable form is a rule about evidence. Both are given criteria below, but a
reader should not expect them to look like B5-1 to B5-5.

#### Verifiable criterion for each control

**Nothing in this table exists.** Every "Passes when" describes a test or a check that must be
built. The "Today" column records what the tree contains as of 19 July 2026, established by reading
and `grep`; **no code was executed for this amendment.**

| # | Passes when | Today |
|---|---|---|
| B5-1 | A test loads a scenario whose world is not marked fictional and asserts that **no influence or diffusion code path executes at all** — the run is refused, not merely annotated. A second test asserts the fictional case still runs, so the check is shown to discriminate rather than to block everything. | No world-mode concept exists. `MeridianModel._step_diffusion` (`engine.py:138-145`) is called unconditionally from `step()` at `engine.py:156`. |
| B5-2 | `load_scenario` rejects, with a typed error surfaced as a 4xx rather than a 500, a scenario in which `world_mode` is (a) absent, (b) null, (c) any value other than `fictional`. A test covers all three. **No default value is supplied anywhere in the load path** — a default would convert fail-closed into fail-open, and a grep for a default must return nothing. | `world_mode` appears in no schema, model or scenario file. `load_scenario` (`scaffold/backend/app/api/runs.py:21-26`) performs a path-existence check and `json.loads` with no validation. |
| B5-3 | There is no code path that constructs a scenario from user-supplied, uploaded or remote content: no import or upload endpoint exists, and a test asserts the loader refuses any path resolving outside the vetted scenario directory (path traversal included). The disabled state is asserted by a test, not merely by the absence of a feature — absence is not enforcement, because the next contributor may add one. | No import surface was found. That is an absence of a feature, **not** a verified control: nothing asserts it stays absent. |
| B5-4 | A validation step at scenario load rejects a scenario in which a real person, organisation or political population appears as an influence-target entity, and a test demonstrates the rejection failing closed. **The method by which "real" is determined must be written down and must not be author attestation alone**, since B5-8 makes technical enforcement mandatory. See open question 16 — the method is not settled, and this criterion cannot be reduced to a command until it is. | No entity, name or content validation of any kind at load. No real-entity concept in any schema. |
| B5-5 | The enumerated list of protected characteristics is recorded in the repository; **no field in that list is read by any targeting, ranking, susceptibility or campaign-effect path** (verified by call-site enumeration, not by grep alone); and a test asserts that changing *only* a protected-characteristic attribute of a cohort leaves campaign targeting and effect outputs **bit-identical**. That test is the mechanical form of the permitted/not-permitted distinction above: identity may shape exposure and interpretation, and may not act as a coefficient. | `Demographics` declares `religion_majority` and `primary_language` (`agent_schema.py:22-28`). Both are inert today. `InfluenceSusceptibility`'s three appeal scalars (`:72-77`) are **not** inert — they are averaged at `cohort_agent.py:22-26` and drive diffusion gain at `diffusion.py:74-76`. Whether an appeal scalar is a protected-trait proxy is open question 17. |
| B5-6 | With the other seven controls in force, a fictional scenario still produces non-zero aggregate narrative diffusion, exposure and adoption, and a counter-messaging action still measurably changes an aggregate outcome — asserted by test. This is a **non-regression** criterion: it fails if enforcement over-blocks. | Aggregate diffusion exists (`diffusion.py:63-79`) and writes `narrative_adoption`. Counter-messaging has no implementation to regress. |
| B5-7 | Every REST response carries an explicit world-mode / fiction field, asserted by a contract test covering **all five** endpoints (`routes_simulation.py:47-49`, `:60`, `:71-77`, `:101`, `:111`) rather than a sample of them; and the interface displays the disclosure where a user reaches it without interaction. The UI half is **not command-verifiable** — see open question 18. | No API response carries any such field. `scaffold/frontend/` holds one file and contains no fiction, provenance, AI-generated or disclaimer text. `fiction_disclaimer` (`scaffold/scenarios/kestral-strait.json:7`) is read by nothing. |
| B5-8 | **Evidence rule, checked at sign-off rather than by a command.** Each of B5-1 to B5-5 and the API half of B5-7 is ticked against a **test reference**. No document, disclaimer, charter bullet or acceptable-use text may be recorded as the evidence closing any of them. If acceptable-use language is written later, it is recorded as supplementary and closes none of the eight. A reviewer confirms this by reading the per-control sign-off table: any row whose evidence is a document rather than a test fails B5-8. | Not applicable until there is evidence to check. The current safeguards are three prose bullets at `CHARTER.md:135-142`, which under B5-8 are supplementary and close nothing. |

**Verify by.** Every check in the table above, plus:

```
# The controls must be discoverable as tests, not asserted in prose
grep -rn "def test_" scaffold/backend/tests/

# Fail-closed means no default: a default world_mode would silently defeat B5-2
grep -rn "world_mode" scaffold/
```

**Passes when.** All eight rows pass as stated, the tests they name exist in the tree and are
passing, and their output is recorded in the per-control sign-off table. **This criterion cannot be
cleared by text correction, by policy language, or by a decision record.** The decision has already
been made; what remains is enforcement.

**Status today: NOT PASSING, and mostly NOT TESTABLE.** No control is implemented, so seven of the
eight have no substrate to test against and B5-8 has no evidence to check. Supporting observations,
all made 19 July 2026 by reading and `grep`, **no code executed**:

- `NOTICE.md`, read in full, contains no acceptable-use, field-of-use or dual-use restriction.
- `CHARTER.md:135-142` carries exactly three scope bullets, all prose. The third promises "a
  visible provenance tag" on AI-generated text at the interface level. No such tag is
  implemented: the only marker is the literal string `[STUB briefing — tick {tick}]` inside the
  stub's return value (`scaffold/backend/app/simulation/llm_gateway.py:100`), and no
  provenance field appears in any of the five API responses. (`llm_gateway.py` is 103 lines; the
  prefix is at `:100`, within the return expression spanning `:99-103` — the `:100-104` cited in an
  earlier draft over-ran the file.)
- No `fictional: true` assertion exists anywhere — nor a `world_mode` field, which is what the
  decision actually requires and which is the more exacting of the two, since it must fail closed
  rather than merely be present. The scenario's `fiction_disclaimer`
  (`scaffold/scenarios/kestral-strait.json:7`) is read by nothing and surfaced in no API response
  and in no part of the frontend.
- Scenario loading performs a path check and `json.loads` with no entity or content validation.
  No JSON Schema validation library is present in the tree.

> **Not verified by this draft.** Whether `docs/PLAN.pdf` still asserts the DISARM Red Framework
> correspondence the audit quoted. The PDF retains two DISARM link annotations, but the
> surrounding prose sits in compressed content streams that were not extracted, and the audit's
> citation for the sentence pointed at `scaffold/backend/plan.txt`, which no longer exists.

---

### C7 — README accurately states what is and is not implemented

**Source:** HANDOFF checklist item 2; P0.1.

**Plain English.** The root README's determinism-boundary table describes LLM functions the code
does not contain, and macro rules richer than the one line of noise the engine actually applies.

**Verify by.** A reviewer reads `README.md` line by line against the code and records a
disposition for each capability claim. As a mechanical floor, these four rows must be reconciled:

| Line | Claim | Code |
|---|---|---|
| `README.md:36` | "Deterministic rules + seeded Monte Carlo draws" | One `rng.uniform(-0.002, 0.002)` applied to one indicator, `engine.py:132-136`. No ensembles. |
| `README.md:37` | "Cohort belief updates \| Seeded diffusion over the social graph" | Diffusion writes `narrative_adoption`, not cohort beliefs (`engine.py:137-145`). `scaffold/docs/AGENT_TASK_TEMPLATE.md:48-49` says so internally. |
| `README.md:39` | "Adversary campaign design \| LLM composes content" | No such function. `llm_gateway.py` defines `propose_action` (`:54`) and `generate_briefing` (`:85`) only. |
| `README.md:40` | "Advisor dialogue ... grounded by retrieval over true state" | No retrieval. `generate_briefing` reads two keys from a passed-in mapping (`:95-96`) plus two values from the nested `indicators` dict (`:97-98`) and returns an f-string (`:85-103`; the file is 103 lines, so the `:85-104` of an earlier draft over-ran it). |

**Passes when.** No row of the determinism-boundary table describes a function that does not
exist, and no capability sentence in `README.md` is contradicted by an internal document.

**Status today: NOT PASSING.** All four rows above are present as quoted.

---

### C8 — False determinism and replay claims corrected

**Source:** HANDOFF checklist item 3; audit §8 decision 4 (settled); standing constraints.

**Plain English.** The determinism claim must shrink to what was actually tested. The founder has
already settled the exact wording; it is not for a drafting agent to reword.

The claim to use, verbatim:

> "The existing stubbed execution path reproduces the same tested numeric outputs when the seed,
> scenario and stubbed agent outputs remain identical."

The target contract, which **must always be labelled a target and never a delivered capability**:

> "Given the same scenario version, rule-pack version, seed, ordered player inputs and recorded
> external-agent inputs, the engine is intended to reproduce identical authoritative state hashes."

> **Note added 19 July 2026 (founder decision P0.4A). C8 does not cover the isolation defect.**
> The settled wording above is compatible with a single shared, unisolated random stream: it holds
> seed, scenario and stubbed agent outputs identical, so it says nothing about whether draws
> consumed by one subsystem shift the values another subsystem receives. That is a separate
> property and it is tested by **C8A**, not here. Neither criterion may be read as covering the
> other, and passing C8 must not be reported as evidence for C8A.

**Verify by.**

```
grep -rn "stubbed execution path" --include="*.md" . | grep -v "^./docs/"
grep -rniE "identical macro|proves reproducibility|fully deterministic|replay|execution.?ready|replay.?capable" \
  --include="*.md" . | grep -v "^./docs/"
```

The standing constraint this criterion enforces (`HANDOFF.md` § Standing constraints (`:135`)) names three terms —
"execution-ready, replay-capable or fully deterministic" — so all three must be in the pattern.
An earlier revision omitted `execution.?ready`, which meant the three hits reported below could not
be reproduced by the command the criterion tells a reviewer to run.

**Passes when.** The first grep finds the settled wording in `README.md` (and anywhere else the
claim is made). The second returns no unqualified determinism or replay claim; every surviving
line is either removed or explicitly marked as a target.

> **This grep cannot be adjudicated by its exit status.** The `replay` alternative is broad, and
> the standing constraint trips its own detector: `HANDOFF.md:70`, `:87-88`, `:98`, `:128`, `:130`
> and `:127` all match, and all are expected hits stating the constraint rather than violating it.
> **[drafter-proposed]** A reviewer records the disposition of each line. Without the `./docs/`
> exclusion the same command returned 49 lines on 19 July 2026, almost all from planning records.

**Status today: NOT PASSING.** The settled wording appears nowhere outside `HANDOFF.md`. As of
19 July 2026 the second grep (with `execution.?ready` included) returns 12 lines outside `./docs/`:
seven are the expected `HANDOFF.md` constraint lines above; two are defects — `scaffold/README.md:65`
("identical macro state after N ticks") and `README.md:61` ("proves reproducibility"); and three
describe `docs/PLAN.pdf` as "the full execution-ready plan" (`README.md:27`, `README.md:80`,
`scaffold/README.md:101`). Those last three describe a *plan document*, not the codebase, so they
may not violate the standing constraint against calling the codebase execution-ready. **This draft
does not adjudicate them** — flagged for the reviewer to decide.

---

### C8A — P0.4A: deterministic randomness architecture

**Source:** Founder decision of 18 July 2026 establishing **P0.4A** as a Phase 0 workstream
(`P0.4` → **`P0.4A`** → `P0.5` → `P0.6`); publication dependency by way of `HANDOFF.md:13`, which
conditions publication on Phase 0 corrections passing. Evidence for the underlying defect:
`A3-VERIFICATION-RESULTS.md:170-175` (the no-substreams defect, demonstrated by execution) and
audit finding 28, `CURRENT-STATE-AUDIT.md:320`.

> **Sourcing gap, stated plainly.** Every other criterion in this file cites a file and a line.
> This one cannot. The P0.4A decision was issued as an instruction to a workflow and **no source
> record for it exists in the repository as of 19 July 2026**;
> `docs/world-model/FOUNDER-REQUIREMENT-2026-07-18.md` is the world-model source record and does not
> contain P0.4A. Until a dated founder record exists in the tree, a reviewer cannot verify this
> criterion's authority from the repository, and this criterion is therefore not independently
> checkable in the way C1–C13 are. **[drafter-proposed]** such a record should be created and the
> citation above replaced with a file and line. This document does not create it. See open
> question 13.
>
> **This gap is not closed by ADR-010.**
> [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
> (19 July 2026) records the same founder instruction as its authority and is the fullest derived
> statement of it in the tree, but it was drafted by an AI agent and cites the decision by date in
> the same way this criterion does. A derived record cannot verify its own source. The gap stands.

**Plain English.** There is one random-number generator in application code
(`scaffold/backend/app/simulation/engine.py:83`) and every subsystem draws from it in sequence.
That means the number of draws one part of the simulation consumes changes the values every later
part receives. A3 demonstrated the effect by execution: adding a grievance to a single cohort moved
a national indicator from `0.6080711379477878` to `0.5973599412373322`, and that looked like the
meso tier influencing the macro tier when in fact nothing causal had happened at all
(`A3-VERIFICATION-RESULTS.md:157-168`).

The founder's statement of the problem, quoted so it is not paraphrased away:

> "Materialising a background citizen must not change tomorrow's weather, market behaviour,
> government approval or another person's decision merely because it consumed extra draws."

Isolation must hold across **all** of: subsystem; entity; relationship or interaction; simulation
purpose; and tick or event context where appropriate. **Per-entity streams alone are insufficient.**

**Why the existing determinism test does not cover this.** `test_same_seed_is_deterministic` runs
the same seed twice and compares the result. Draw-order contamination survives that test untouched,
because both runs consume the same draws in the same order. The founder's note, carried here
verbatim in substance: the current determinism test is **insufficient**, because it would accept
draw-order contamination as ordinary divergence. A3 says the same thing at `:174` — "the existing
determinism test would mask such a change as 'expected divergence'". **P0.4A requires isolation
tests, not same-seed repetition tests.** See also the clause added to C9.

**An ADR is required.** At least two valid approaches exist — stateful named substreams, or keyed /
counter-based deterministic draws — and the ADR must select one deliberately. It must **explicitly
reject ordinary sequential calls to a single shared PRNG for authoritative behaviour**. Note that
this is the architecture `scaffold/docs/ARCHITECTURE_DECISIONS.md:60-67` (ADR-007, status
*Accepted*) currently documents and endorses: ":63" reads "All engine, agent, and diffusion
randomness draws from that one RNG". ADR-007 therefore stands to be superseded or annotated by the
P0.4A ADR. Whether superseding it is required *before* publication, or whether annotating it as
superseded suffices, is open question 15.

#### The ten exit criteria, and which of them gate publication

The founder set ten exit criteria. They are reproduced with their founder numbering (`P0.4A-1` …
`P0.4A-10`), plus the ADR requirement (`P0.4A-ADR`). **Default in force: all ten are gate
conditions.** A drafting agent may not shrink a founder-set gate, so where this draft judges an
item is better placed later, that is recorded as a recommendation and an open question, not applied.

| # | Criterion | Demonstrated by | Passes when | Gate disposition |
|---|---|---|---|---|
| P0.4A-1 | No authoritative code calls the global `random` API directly | `grep -rnE "random\.(random\|uniform\|choice\|seed\|randint\|shuffle\|gauss\|sample\|betavariate\|normalvariate)\(" --include="*.py" scaffold/` | Returns no line in which the receiver is the `random` *module* rather than a generator instance. Module-level `import random` used only to construct or type a generator is not a hit. | **In gate.** Testable today. |
| P0.4A-2 | No subsystem receives unrestricted access to the root generator | Reviewer traces every draw site and records which stream object it holds, then: `grep -rn "self.model.rng\|self.rng\|\.random\b" --include="*.py" scaffold/backend/app` | No draw site holds the root generator; each holds a derived, named stream. Mesa's own `Model.random` (audit finding 27, `CURRENT-STATE-AUDIT.md:319`) must be either removed, replaced or shown unreachable from authoritative code. | **In gate.** Testable today. |
| P0.4A-3 | Stream keys use stable identifiers, **not** Python's process-randomised `hash()` | `grep -rn "hash(" --include="*.py" scaffold/` and a reviewer reading the key-derivation function | No `hash()` result reaches a stream key. Keys derive from scenario-stable identifiers (entity id, subsystem name, purpose, tick). A stated stability rule accompanies them. | **In gate.** Testable today. |
| P0.4A-4 | The run records the RNG algorithm and version | Create a run, then inspect the run record / snapshot payload for the fields | The recorded run carries an explicit algorithm name and version. No such field exists today (`getstate`: zero occurrences under `scaffold/backend`). | **In gate.** Testable once the field exists. |
| P0.4A-5 | Adding an unrelated entity does not alter unrelated subsystem results | The isolation test suite P0.4A must produce. Reference method: `docs/delivery/evidence/a3_rng_isolation.py` already performs this class of perturbation. | Adding the entity leaves the unrelated subsystem's outputs **bit-identical**, not merely close. | **In gate.** Requires code that does not exist. |
| P0.4A-6 | Promoting one background person does not alter previously established entities | The isolation test suite | Promotion leaves previously established entities bit-identical | **Recommended out of gate — NOT decided. Remains in gate by default.** See below and open question 14. |
| P0.4A-7 | Reordering entity iteration does not alter outcomes where the model declares order irrelevant | The isolation test suite, plus the model's own written declaration of where order is and is not significant | Reordering produces identical outputs wherever the model declares order irrelevant, and the declaration exists in writing. Without the declaration this criterion is untestable. | **In gate.** Requires code that does not exist. |
| P0.4A-8 | Repeating the same promotion event produces the same profile and history | The isolation test suite | The repeated promotion yields an identical profile and identical history | **Recommended out of gate — NOT decided. Remains in gate by default.** See below and open question 14. |
| P0.4A-9 | Every random outcome can be associated with a subsystem, entity or interaction, and a purpose | Reviewer inspects the draw-provenance record emitted by a run | Every draw in a run resolves to a `(subsystem, entity-or-interaction, purpose)` triple. Nothing in the tree emits this today. | **In gate.** Requires code that does not exist. |
| P0.4A-10 | Tests deliberately inject extra draws into one stream and verify other streams remain unchanged | The isolation test suite | A test exists that consumes extra draws from one named stream, and asserts other streams' outputs are bit-identical. This is the direct inverse of the A3 finding and is the single most load-bearing test in P0.4A. | **In gate.** Requires code that does not exist. |
| P0.4A-ADR | An ADR selects an approach deliberately and explicitly rejects sequential shared-PRNG use for authoritative behaviour | Read [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md), written against [`ADR-TEMPLATE.md`](ADR-TEMPLATE.md), **and read its Approval block** | The ADR exists, names the chosen approach, records the rejected alternative, contains an explicit rejection of ordinary sequential calls to a single shared PRNG for authoritative behaviour, **and is approved by the owner**. ADR-010 satisfies the first three as drafted; its Approval block is empty, so the criterion is **not** met. | **In gate.** Testable today (it is a document). |

**Two further conditions, documentary. [drafter-proposed] — these are the drafter's construction,
not part of the founder's ten.** They are the same class as B1–B4 and P0.1: a document must not
assert a property the code lacks. They are put to the owner to accept, amend or drop.

```
# D1 — no document claims randomness isolation that does not exist
grep -rniE "substream|rng.?isolation|isolated (random|rng)|independent (random|rng)" \
  --include="*.md" --include="*.py" . | grep -v "^./docs/"

# D2 — the single-shared-stream architecture is not presented as an adequate
#      reproducibility foundation
grep -rn "ONLY source of engine randomness\|one RNG\|one seed, threaded everywhere\|that one RNG" \
  --include="*.md" --include="*.py" . | grep -v "^./docs/"
```

- **D1 passes when** the grep returns no line asserting that MERIDIAN has isolated or named random
  streams. As of 19 July 2026 it returns **one line**, `HANDOFF.md` § Reproducing the evidence (`:151`), which names the evidence
  script `a3_rng_isolation.py` and describes the coupling as *contamination*. That is an expected
  hit stating the defect, not claiming the property. **D1 passes today** and is recorded so that a
  future edit cannot introduce the claim unnoticed.
- **D2 passes when** each remaining line is either removed or carries an explicit caveat that a
  single shared stream provides no isolation between subsystems. As of 19 July 2026 the grep
  returns **three lines outside `./docs/`**, none caveated: `scaffold/backend/app/simulation/engine.py:83`
  ("`# the ONLY source of engine randomness`" — contradicted by Mesa's second generator, audit
  finding 27), `scaffold/docs/ARCHITECTURE_DECISIONS.md:60` (the ADR-007 heading) and `:63`.
  **D2 does not pass today.**

#### The scope judgement, stated rather than made silently

`HANDOFF.md` § Publication exit criteria (`:96-102`) lists seven publication exit criteria and A3 lists five blockers. Neither
mentions randomness architecture. C8A enters this gate solely by the Phase 0 route: P0.4A is a
Phase 0 workstream, and `HANDOFF.md:13` conditions publication on Phase 0 passing. That is a real
dependency and this draft does not weaken it.

What this draft does flag is the reach of two of the ten. **P0.4A-6 and P0.4A-8 both test entity
promotion** — materialising a background person into a detailed individual. **No promotion
mechanism exists**, and the entity model that would define one is explicitly backlog: the founder's
own record states it is "Backlog. **Does not interrupt Phase 0 remediation**"
(`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md:5`). Read strictly as publication preconditions,
P0.4A-6 and P0.4A-8 would pull world-model materialisation into the publication gate, which no
source asks for and which the world-model record appears to exclude.

The drafter's recommendation is that P0.4A-6 and P0.4A-8 be verified when the entity model is
built, and that publication be gated on the other eight plus the ADR. **This is a recommendation
only.** It is not applied: the table above leaves both in the gate, because shrinking a founder-set
gate is an owner decision and this draft has no authority to make it. Recorded as open question 14.

Note also the founder's sequencing rule, which is a *development* gate rather than a publication
one and is recorded here so the two are not conflated: P0.5 **specification** may proceed in
parallel before P0.4A is implemented, but neither P0.5 **implementation** nor entity promotion nor
world-model materialisation may proceed until P0.4A passes.

**Verify by.** All of the commands and observations in the table and the two documentary greps
above, plus:

```
# The isolation test suite must exist and be named, so a reviewer can find it
ls scaffold/backend/tests/
grep -rn "def test_" scaffold/backend/tests/
```

**Passes when.** Every item marked *in gate* in the table passes as stated there; D1 and D2 pass if
the owner accepts them; and the isolation tests are present in the tree and passing, with their
output recorded in the sign-off block. **This criterion cannot be cleared by text correction
alone.** D1 and D2 can; nothing else can.

**Status today: NOT PASSING, and mostly NOT TESTABLE.** Observed 19 July 2026 by reading and
`grep`; **no code was executed and no test was written or run for this amendment.**

- `scaffold/backend/app/simulation/engine.py:83` constructs one `random.Random` and comments it as
  the only source of engine randomness. It is the only generator constructed in application code.
- Three draw sites share it: `agents/cohort_agent.py:36`, `diffusion.py:75`, `engine.py:135`.
  `diffusion.py:44` receives the root generator as a parameter — unrestricted access, so
  **P0.4A-2 fails today**.
- **P0.4A-1 appears to hold today**, verified by grep: no call to the global `random` module API
  occurs anywhere under `scaffold/`. `import random` appears at `diffusion.py:13` and
  `engine.py:15` and is used only to construct or type a generator. This is a grep, not an AST
  parse; treat it as a fast negative check, not a proof, exactly as C10 treats its equivalent.
- **P0.4A-3 has nothing to check yet**: `grep -rn "hash(" --include="*.py" scaffold/` returns
  nothing, because there are no stream keys at all.
- **P0.4A-4 fails**: no RNG algorithm or version is recorded anywhere; `getstate` has zero
  occurrences under `scaffold/backend`, so the generator's state is not captured either.
- **P0.4A-5, -6, -7, -8, -9 and -10 are not testable today.** The isolation test suite does not
  exist; `scaffold/backend/tests/test_engine.py` contains five tests, none of which is an isolation
  test. -6 and -8 additionally have no promotion mechanism to exercise.
- **P0.4A-ADR fails**: no *approved* ADR selecting a randomness architecture exists. A **drafted**
  one does: [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md),
  dated 19 July 2026, **Status: Proposed — drafted by an AI agent, Approval block empty, no
  authority**. It recommends keyed / counter-based deterministic draws and contains the required
  explicit rejection of sequential shared-PRNG use, but the founder decision requires that the ADR
  *select* an approach, and selection is the owner's act. **The criterion therefore remains failed
  until the owner signs it.**
  [`ADR-TEMPLATE.md`](ADR-TEMPLATE.md) is a template and its worked examples are illustrative, not
  decisions. The accepted ADR that does bear on this — ADR-007, `scaffold/docs/ARCHITECTURE_DECISIONS.md:60-67`
  — records the architecture P0.4A's ADR must reject, not the one it must select.

---

### C9 — Existing tests and their actual scope accurately described

**Source:** HANDOFF checklist item 4; P0.1.

**Plain English.** There are five tests in one file. The README says one of them "proves
reproducibility". It compares one dictionary — the final macro snapshot after 20 ticks — between
two runs that both call the same in-process stub. It does not compare cohort beliefs, narrative
adoption, the event log or the snapshot history, and it does not vary the agent output.

**Verify by.**

```
grep -n "def test_" scaffold/backend/tests/test_engine.py
grep -rn "proves reproducibility\|the test suite is the point" --include="*.md" . \
  | grep -v "^./docs/"
```

**Passes when.** No document claims a test proves more than it asserts. Specifically, any
description of `test_same_seed_is_deterministic` states that it compares final macro state only,
under a held-constant stub; and any description of `test_llm_gateway_cannot_write_state` states
that it is an attribute-presence check, not an import-graph or mutation test.

> **Clause added 19 July 2026 (founder decision P0.4A).** No description of
> `test_same_seed_is_deterministic` may present it as evidence of random-stream isolation. The
> founder's note is that the current determinism test is **insufficient**, because it would accept
> draw-order contamination as ordinary divergence; A3 records the same thing at
> `A3-VERIFICATION-RESULTS.md:174`. A same-seed repetition test cannot detect the defect, since
> both runs consume the same draws in the same order. This clause is documentary and clears by text
> correction. The property itself is C8A's, not C9's. One line is presently in scope:
> `scaffold/docs/ARCHITECTURE_DECISIONS.md:65` states that identical macro/meso numbers are "proven
> by `test_same_seed_is_deterministic`". **This draft does not adjudicate it** — per this
> criterion's own pass condition, a reviewer records the disposition.

**Status today: NOT PASSING.** `README.md:61-63` reads "The test suite is the point:
`test_same_seed_is_deterministic` proves reproducibility and `test_llm_gateway_cannot_write_state`
guards the determinism boundary against regression. Neither may be weakened." The first grep
confirms five tests, at lines 25, 34, 43, 52 and 61 of the single test module.

---

### C10 — Unused installation-blocking dependencies removed or made optional

**Source:** HANDOFF checklist item 5; P0.2.

**Plain English.** A package that no code imports should not be able to stop the install.

**Verify by.**

```
grep -rn "litellm" scaffold/backend/requirements.txt
grep -rn "^import litellm\|^from litellm\|^\s*import litellm" scaffold/backend/app
```

**Passes when.** Either `litellm` is absent from the default install path, or it is moved behind
an explicitly optional extra that the documented install does not pull in.

The second grep **returns exactly one line today**, and a verifier should expect it:

```
scaffold/backend/app/simulation/llm_gateway.py:17:    import litellm
```

That is the indented sketch inside the module docstring spanning `:1-29` — not an executable
import. The `^\s*import litellm` alternative in the pattern is what matches it. That single known
line is the expected result; **any additional line is a real import and blocks this criterion.**

It remains a **fast negative check, not a proof of non-use**, for four reasons. It does not match
an indented `from litellm import ...`; nor an aliased or conditional import; nor a dynamic one
(`importlib.import_module("litellm")`); and — the largest gap — it is **scoped to
`scaffold/backend/app`**, so it does not cover `scaffold/backend/tests/` or any `.py` elsewhere
under `scaffold/`. The AST parse it stands in for covered every `.py` under `scaffold/`. Before
removal, re-run that AST parse — walk `ast.Import` / `ast.ImportFrom` over every `.py` under
`scaffold/` — and record its output in the sign-off block.

**Status today: NOT PASSING.** `scaffold/backend/requirements.txt:20` declares
`litellm>=1.34,<2.0`. **Carried from an earlier verification pass, not re-run here:** an AST parse
of every `.py` file under `scaffold/` scanned 78 import statements and found zero importing
`litellm`. Independently re-confirmed here by grep: its only occurrences in code are the module
docstring sketch at `scaffold/backend/app/simulation/llm_gateway.py:17-18`.

Two related observations, recorded but **not** made pass conditions, because the audit's remedy
for them is not settled: not one of the 13 requirements is exactly pinned (all are open ranges,
no hashes, no lockfile), and `websockets>=12.0` has no upper bound at all. The supported Python
version is declared only in prose and in the Docker base image (`python:3.11-slim`); there is no
machine-readable `requires-python` anywhere, which follows from there being no `pyproject.toml`.
P0.2 requires pinning a supported Python; whoever does that should decide whether pinning the
dependency set belongs in the same change.

---

### C11 — Current-state audit and known-limitations document committed

**Source:** HANDOFF checklist item 6.

**Plain English.** The honest account of the project's defects must ship *with* the project, not
be discoverable only by reading the code.

**Verify by.**

```
git ls-files docs/delivery/
```

**Passes when.** The listing includes `CURRENT-STATE-AUDIT.md`, `A3-VERIFICATION-RESULTS.md` and
a known-limitations document.

> **[drafter-proposed] Not required by the source.** `HANDOFF.md` § Publication exit criteria (`:101`) requires only that the
> current-state audit and a known-limitations document be *committed*. This draft additionally
> suggests that the root `README.md` link to the known-limitations document from a position a
> first-time reader will reach. That is the drafter's addition, it is a subjective siting test that
> no command can verify, and it is for the owner to accept or drop. See open question 8.

**Status today: PARTIALLY PASSING.** The audit and the A3 results are tracked. **No
known-limitations document exists** — `docs/` contains `PLAN.pdf`, the two tracked delivery
records, the five evidence artefacts under `docs/delivery/evidence/`, and a number of untracked
paths (see C12 check 4).

> **[drafter-proposed] RECOMMENDED, not required by HANDOFF — owner to confirm whether this
> becomes a gate condition.** The drafter's view is that the audit's own stale citations should be
> reconciled before this criterion is ticked, because a committed record that cites files which no
> longer exist is a weaker record than it could be. This is editorial judgement, not a requirement
> traceable to `HANDOFF.md`, the audit or A3 — and it touches the standing constraint that the
> broad audit is closed. It is recorded as open question 9, not applied as a pass condition.

Known drift in the audit's citations, all observed 19 July 2026:

- `CURRENT-STATE-AUDIT.md:339` and `:372` state the repository is not under version control. It is.
- `CURRENT-STATE-AUDIT.md:349` describes `backend/plan.txt`. The file does not exist, so the Phase 0
  instruction at `:427` to delete it is already satisfied. Whether that line should be *marked* done
  in the audit is not for this draft to direct — amending the audit at all is the subject of open
  question 9, and issuing a specific instruction while deferring the general permission would be
  inconsistent. Recorded as an observation for the owner, folded under open question 9.
- Citations anchored to `plan.txt:221` and `plan.txt:229` are unresolvable.
- `CURRENT-STATE-AUDIT.md:237` and `:403` cite `README.md:92` as claiming the repository is
  public. `README.md` has been rewritten to 96 lines and makes no such claim. The wording has
  migrated to `NOTICE.md:11`; see C12.
- `CURRENT-STATE-AUDIT.md:237` cites `COPYRIGHT.md`. That file does not exist; the licensing
  position lives in `NOTICE.md`. The substantive point — that it contains no acceptable-use or
  field-of-use restriction — still holds against `NOTICE.md`.

---

### C12 — Secret, personal-data and repository-content review passes

**Source:** HANDOFF checklist item 7.

**Plain English.** Once a repository is public, its whole history is public. This review must
cover what is committed *and* what is about to be committed, and it must be re-run immediately
before the visibility flip, not once and forgotten.

**Verify by.** All six checks, from the repository root. Note that checks 1–5 scan tracked file
*contents* only; check 6 covers commit metadata, which is part of the published history and cannot
be edited after publication without rewriting history.

```
# 1. Credential-shaped strings in tracked files
git ls-files -z | xargs -0 grep -lniE "api[_-]?key|secret|password|token|BEGIN [A-Z ]*PRIVATE KEY"

# 2. Email addresses and personal identifiers in tracked files
git ls-files -z | xargs -0 grep -rhoE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" | sort -u

# 3. No real .env is tracked; only the example is
git ls-files | grep -i env

# 4. Nothing unreviewed is about to be committed
git status --short

# 5. The example environment file contains no real credential
cat scaffold/.env.example

# 6. Commit metadata that becomes permanently public at the flip
git log --format='%an <%ae> | %cn <%ce>' | sort -u
```

**Passes when.**

1. Every file the first check returns has been opened and each hit adjudicated as a benign
   keyword match rather than credential material. Record the adjudication.
2. Returns no address the owner does not intend to publish.
3. Returns `scaffold/.env.example` and nothing else.
4. Returns empty, or every listed path has been deliberately reviewed and either committed or
   removed.
5. `scaffold/.env.example` is confirmed to contain **no real credentials** — placeholders and
   local development defaults only.
6. Returns no name or address the owner does not intend to publish permanently.

**Status today: NOT PASSING.** Checks 1, 2, 3 and 5 **return clean results — against tracked
content only**, and cannot be treated as passing while ten untracked paths remain unreviewed: none
of that content was scanned by any of these checks, and three whole directories among it were never
opened (see check 4). Check 4 fails: the working tree is not clean. Check 6 is undecided — it
requires an owner judgement that has not been made.

Pass or fail for each check is recorded in the sign-off table by the owner, not here. This
criterion is `HANDOFF.md` checklist item 7, and the sign-off block asks the owner to verify and
date it; what follows is the *evidence*, not an adjudication of it. C12 cannot be ticked until
check 4 passes and check 6 is decided, and all six must be re-run immediately before the flip —
this is the only criterion whose result can change without anyone editing a document.

Check 1 returns 7 files. Each was opened, and the specific matching line is named below for every
one, since the pass condition requires the adjudication to be *recorded*, not asserted:

| File | Matching line(s) | Adjudication |
|---|---|---|
| `.gitignore` | the ignore patterns `*.pem`, `*.key` | Ignore rules naming credential file types; no credential. |
| `HANDOFF.md` | `:102` "Secret, personal-data and repository-content review passes"; `:121` "`DESIGN-TOKENS`" (matches on the substring `TOKEN`) | Prose about this checklist item, and a document name. No credential. |
| `CURRENT-STATE-AUDIT.md` | `:176` ("`secretary_minister_of_defence`", matching `secret`); `:339`, `:372`, `:383` (secret scanning / secrets management prose); `:509` ("no secrets in history"); `:579`, `:584` (compose default credentials and API-key discussion) | Audit prose discussing secret handling, plus a role name containing the substring. No credential. |
| `docs/delivery/evidence/a3_direct.py:173` | a loop variable literally named `token` | Identifier name. No credential. |
| `docs/delivery/evidence/probe.py:12-13` | role-rename strings containing "secretary" | Substring match on `secret`. No credential. |
| `scaffold/docker-compose.yml:6,23` | `POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-meridian}` | Local development default, documented as such. No credential. |
| `scaffold/.env.example` | database defaults and two commented-out, empty API-key lines | Re-read in full at check 5; see below. |

Check 2 returns nothing — no email address appears in any tracked *file*. Commit metadata is not
covered by this check; it is covered separately by check 6.

Check 3 returns `scaffold/.env.example` only. `.gitignore:24-26` ignores `.env` and `.env.*` and
re-admits `.env.example`. This is an observation about the ignore rules, **not a guarantee that a
credential file cannot be committed**: filenames outside those two patterns (`.envrc`, `env`,
`local.env`, `backend.env`) are not covered, `git add -f` bypasses ignore rules entirely, and
`.env.example` is deliberately committable and so must be re-read at check 5.

Check 5: **`scaffold/.env.example` was read in full (27 lines) and contains no real credentials.**
Its database values are the local default `meridian` / `meridian` / `meridian`; `LLM_MODE=stub`;
and the two API-key lines (`ANTHROPIC_API_KEY=`, `OPENAI_API_KEY=`) are **commented out and
empty**. Line 1 states "All values below are safe local defaults; the scaffold runs without
secrets", which matches what the file contains. This must be re-read and re-confirmed immediately
before the flip, since the file may change.

Check 6 returns a single identity: `Aries Russell <ariesd.russell@gmail.com>`, on commit
`71fa329`. This is a personal email address that becomes permanently public at the flip. Whether
that is intended is an owner judgement, not a defect this draft can adjudicate — see open
question 6.

Three items requiring action:

- **Check 4 does not return empty.** As of 19 July 2026 `git status --short` reports ten untracked
  paths, not one: seven files under `docs/delivery/` (including this document), plus the
  directories `docs/design/`, `docs/safety/` and `docs/world-model/`. `ls docs/world-model`
  enumerates seven files (`BELIEF-AND-KNOWLEDGE-MODEL.md`, `ENTITY-ONTOLOGY.md`,
  `FOUNDER-REQUIREMENT-2026-07-18.md`, `ORGANISATION-MODEL.md`, `PERSON-MODEL.md`,
  `POPULATION-FIDELITY.md`, `RELATIONSHIP-GRAPH.md`). That is a directory listing, **not a review**
  — none of these files was opened for this criterion, because no criterion required their
  contents. Every one of the ten paths must be reviewed and either committed or removed before
  this criterion is ticked. This list is a point-in-time snapshot and changes as work continues.
- **Check 6 is undecided.** See above and open question 6.
- **`NOTICE.md:11` states, in the present indicative, "The source code is publicly visible for
  evaluation and portfolio purposes."** The repository is private (`HANDOFF.md:13`). This is the
  same defect class Phase 0 exists to correct, sitting inside the document that records the
  licence decision. Whether it was written as a statement of fact or as a description of the
  intended post-publication position is a question for the owner, and this draft does not
  recommend a resolution — see open question 2.

---

### C13 — Repository content resolves: no dangling references, no unresolved markers

**Source: [drafter-proposed] — this criterion is constructed, not sourced.** `CURRENT-STATE-AUDIT.md:431-433`
states these as **Phase 0** exit criteria, not as publication conditions. `HANDOFF.md` § Publication exit criteria (`:96-102`) lists
exactly seven publication exit criteria and does not adopt them; C1 and C7–C12 map onto those seven,
and C2–C6 map onto A3's five blockers. C13 maps onto neither. Adding a precondition to a gate is as
much an owner decision as removing one, so this is put to the owner to accept, amend or drop rather
than presented as required. See open question 12.

**Plain English.** The repository cites design documents that were never written, contains an
unfilled placeholder, and links to a file that does not exist. A reader who follows any of these
learns that the documentation is not maintained.

**Verify by.**

```
grep -rn "design_[a-z_]*\.md\|research_[a-z_]*\.md" --include="*.md" --include="*.py" \
  --include="*.html" . | grep -v "^./docs/"
grep -rn "PLACEHOLDER" --include="*.md" --include="*.py" --include="*.html" . \
  | grep -v "^./docs/"
grep -rn "COPYRIGHT.md" --include="*.md" . | grep -v "^./docs/"

# Link enumeration supporting the count below
grep -rnoE "\[\`?[^]]+\`?\]\(([^)]+)\)" --include="*.md" . | grep -v "^./docs/"
```

**Passes when.** The first grep returns no hits, or only hits pointing at files that now exist.
The second returns no hits. The third returns no hits, or only hits pointing at a file that
exists.

**Status today: NOT PASSING** on all three.

The first returns 8 lines referencing five files that do not exist —
`design_simulation_schemas.md`, `design_nation_expansion.md`, `design_ux_screens.md`,
`research_architecture.md`, `research_licensing.md` — at
`scaffold/backend/app/simulation/schemas/agent_schema.py:3`,
`scaffold/backend/app/simulation/schemas/macro_schema.py:3`, `scaffold/CLAUDE.md:49`,
`scaffold/docs/AGENT_TASK_TEMPLATE.md:54`, `scaffold/docs/ARCHITECTURE_DECISIONS.md:4`, `:25`,
`:71`, and `scaffold/frontend/index.html:18`. A ninth reference is a glob at
`scaffold/docs/AGENT_TASK_TEMPLATE.md:25` ("the workspace `design_*.md` docs") which the grep
above does not catch.

The second returns one line: `scaffold/CLAUDE.md:59`,
`<!-- PLACEHOLDER: fill in with the team's real conventions -->`.

The third returns one line: `README.md:96`, which links to `COPYRIGHT.md`. That file does not
exist; the licensing position is in `NOTICE.md`.

On coverage: the link enumeration above returns **16 links total** in `*.md` files outside
`./docs/`, of which `README.md:96` is the one that does not resolve — so **15 resolve, not 16**.
No broader link check was performed: links inside `./docs/`, inside untracked files, and inside
HTML (for example `scaffold/frontend/index.html`) were not enumerated.

---

### C13A — Fixture-backed prototype artefacts in the tree are labelled and claim no connected behaviour

**Source: [drafter-proposed] — constructed from the founder correction of 19 July 2026 on Track C.**
It is not one of the seven exit criteria at `HANDOFF.md` § Publication exit criteria (`:96-102`) and it clears no A3 blocker. Like
C13, it is put to the owner to accept, amend or drop rather than presented as required. See open
question 20.

> **Sourcing gap, the same one recorded at C6 and C8A.** The Track C correction was issued as an
> instruction to a workflow and **has no source record in the repository as of 19 July 2026**. This
> criterion therefore cites it by date, not by file and line, and a reviewer cannot verify its
> authority from the tree alone. Open question 13 asks for such a record for P0.4A and applies here
> unchanged. The derived records that now carry Track C — `RAID-REGISTER.md` R10 and D14–D19 — cite
> it the same way, so none of them can serve as its source.

#### What this criterion covers, and what it deliberately does not

Track C is a **demonstration** programme. Its five gates C0–C4 are conditions on a demonstration
being truthful, not on the repository being publishable. Publication does not wait for a
demonstration: `HANDOFF.md` § Publication exit criteria (`:96-102`) does not mention one, A3 records no blocker a demonstration would
clear, and none of the five gates is a Phase 0 workstream, so none reaches this gate by the
`HANDOFF.md:13` route that C8A uses. **C0, C1, C2, C3 and C4 are therefore not publication
criteria and are not reproduced here.** They are recorded as decisions D14–D19 in
`RAID-REGISTER.md`, which is where they are tracked. Stating that plainly is the point of this
section: the alternative was to add five gates this document has no source for, which would inflate
the gate and make it harder, not more honest.

One part of Track C does reach the repository. Lane C-VISUAL may build screens on fixture data long
before the engine can produce what they show, on the founder's condition that every fixture-backed
surface visibly states:

> INTERACTIVE PROTOTYPE — FIXTURE DATA — NOT CONNECTED TO THE SIMULATION ENGINE

If such a surface is committed, it publishes with the repository. An unlabelled one would be a
capability claim the code does not support — the same defect B1 to B4 exist to correct, in the form
a reader believes fastest, because a screen showing populated indicators asserts a working engine
more convincingly than any sentence. That, and only that, is what C13A gates.

**What it cannot reach.** A screenshot or recording cropped above the label and circulated outside
the repository is the larger exposure and no repository gate closes it. It is recorded as risk
**R10** in `RAID-REGISTER.md`. This criterion does not pretend to cover it.

**Plain English.** If there are fixture-backed prototype screens in the repository at the moment of
the flip, each must carry the label where a viewer reaches it without interacting, and nothing in
the tree may describe them as connected to the engine. If there are none, the criterion passes and
carries no work.

**Verify by.**

```
# 1. Trigger: does any fixture-backed prototype surface exist in the tree?
git ls-files | grep -iE "fixture|mock-?data|prototype|storyboard|\.(png|jpg|jpeg|gif|webp|svg|mp4|webm)$"
git ls-files scaffold/frontend

# 2. If check 1 returns anything, every such surface must carry the label
grep -rniF "INTERACTIVE PROTOTYPE" --include="*.html" --include="*.md" --include="*.tsx" \
  --include="*.jsx" --include="*.ts" --include="*.js" . | grep -v "^./docs/"

# 3. No prose in the tree describes a prototype surface as connected to the engine
grep -rniE "live (data|engine)|connected to the (simulation|engine)|driven by the (engine|simulation)" \
  --include="*.md" --include="*.html" . | grep -v "^./docs/"
```

**Passes when.** Either:

- **(a) Check 1 returns nothing beyond the existing dev stub**, in which case the criterion passes
  because there is nothing to label. A vacuous pass is not evidence of compliance and expires: like
  C12, this criterion's result can change without anyone editing an existing document, so it must be
  re-run immediately before the flip; or
- **(b) every artefact check 1 returns carries the label** where a viewer reaches it without
  interaction, and check 3 surfaces no line describing any of them as connected. **[drafter-proposed]**
  A reviewer records the disposition of each artefact individually, as at C2 and C5.

Check 2 excludes `./docs/`, for the reason given under *How to read a criterion*: the planning
records quote the label in order to require it, and a hit inside them is not an artefact. Nine such
quotations exist today, in `CORRECTIVE-BACKLOG.md`, `PHASE-0-REMEDIATION-PLAN.md`,
`RAID-REGISTER.md` and this file. Open question 11 applies here as it does to C2, C3, C5, C8 and
C13: with the exclusion in force, a fixture-backed screen placed under `docs/design/` would be
invisible to this check.

Two further limits on check 2, stated so it is not over-trusted. It matches the label's opening words only,
not the full string, because the founder's wording contains em dashes whose byte sequence a `grep -F`
comparison will not survive every editor and encoding; a reviewer must confirm the full wording by
reading. And it establishes only that the label exists **somewhere in the file**, not that it is
visible without interaction — no command in this file can establish visibility. That is the same
evidence problem recorded for B5-7's UI half at open question 18, and this draft has not invented a
proxy for it. See open question 22.

**Status today: PASSING VACUOUSLY — there is nothing to label.** Observed 19 July 2026 by `git
ls-files`, `ls`, `wc` and `grep`; **no code was executed and no interface was rendered.**

- **Nothing in Track C is built.** None of the five C0 screens — Strategic Command Centre, Entity
  Dossier, Society Pulse, Conversational Command Interface, Causal Timeline — exists in any form.
- `scaffold/frontend/` contains exactly one file, `index.html`, 67 lines. It is a dev harness, not a
  fixture surface: it titles itself "MERIDIAN — dev stub" (`:6`), heads itself "MERIDIAN — frontend
  stub" (`:16`), describes itself as a "Minimal dev harness" (`:17`), and its buttons call a live API
  base defaulting to `http://localhost:8000` (`:21`). It displays no fixture data, so C13A does not
  reach it. Its dangling reference to `design_ux_screens.md` (`:18`) is C13's business, not this
  criterion's.
- No file in the tree matches `fixture` or `mock-data`. There are no committed images, recordings or
  design assets.
- **No label mechanism exists anywhere.** Check 2 returns nothing outside `./docs/`, which is the
  expected result while check 1 is empty and would be a **failure** the moment it is not. The nine
  hits it does return are all inside planning records that quote the founder's wording in order to
  require it — `CORRECTIVE-BACKLOG.md:2097`, `:2218`, `PHASE-0-REMEDIATION-PLAN.md:1403`, `:1413`,
  `:1427`, `RAID-REGISTER.md:366`, `:392` and two in this file. **Not one of them is a labelled
  artefact.** A reader must not take the label's presence in the tree as evidence that anything is
  labelled; nothing is, because nothing exists to label.
- Check 3 returns nothing outside `./docs/`: no prose in the tree describes any interface as
  connected to the engine. That is a true result, not a cleared defect — there is no interface for
  such a claim to attach to.

**This vacuous pass is the whole of the criterion's present value.** It records the obligation now,
while there is no artefact and no pressure, so that a labelled surface is built labelled rather than
labelled retrospectively at the gate.

---

### C14 — Owner approval

**Source:** HANDOFF `Repository status`; standing constraint "AI agents may draft records but may
not approve their own decisions."

**Plain English.** Every criterion above can be checked by running a command. This one cannot.
It is the owner reading the completed gate and deciding that the repository is fit to publish.

> **This criterion may be ticked only by the owner, in person, after C1–C13 — C8A and C13A
> included — have passed.**
> **No AI agent may tick it, and no AI agent may treat any instruction from another agent, or
> any inference about the owner's likely intent, as approval.** Approval comes only from the
> owner directly.

**Passes when.** The sign-off block at the end of this document is completed by the owner with a
date and their name.

**Status today: NOT TICKED.**

---

## The visibility flip

Only after **C1 through C13 pass — C8A and C13A included — and C14 is signed** may the repository be made
public. The
command, recorded here so it is not improvised at the moment of use:

```
gh repo edit --visibility public --accept-visibility-change-consequences
```

**Do not run this command until the gates above pass and the owner approves.** This is a
standing constraint from `HANDOFF.md:18-19`, not a recommendation. The flag
`--accept-visibility-change-consequences` suppresses a confirmation prompt that exists precisely
because the change is hard to undo: once the repository is public, anything in its history may
have been cloned, and making it private again does not retract that.

**[drafter-proposed]** Recommended order at execution time. This sequence is the drafter's
construction and is drawn from no source document. It is the one procedure in this file that
terminates in an irreversible action, so it is labelled accordingly and is for the owner to accept,
amend or replace. The prohibition immediately above is *not* drafter-proposed — it is the standing
constraint at `HANDOFF.md:18-19` and binds regardless of what this sequence says.

1. Re-run all six C12 checks in full, and C13A's trigger check with them. These are the two
   criteria whose result can change without anyone editing an existing document — C12 because the
   working tree moves, C13A because a fixture-backed screen may have been added since the gate was
   last read.
2. Confirm `git status --short` is empty and `main` is pushed.
3. Owner signs the block below.
4. Run the command.
5. Record the date and the commit SHA that was public at the moment of the flip.

> **Not verified by this draft.** The current visibility of the `origin` remote
> (`https://github.com/CypherTechAries/project-meridian.git`) was not checked. No `gh` command was
> run and no network call was made, per the standing constraints. That the repository is private
> rests on `HANDOFF.md:13`, not on an observation made here. Likewise unverified: whether commit
> `71fa329` has actually reached the server (the local tracking ref is consistent with a completed
> push, but no fetch was performed), and whether branch protection, CODEOWNERS, required checks or
> secret scanning are configured on the remote. There is no `CODEOWNERS` file in the local tree.

---

## Open questions for the owner

These are recorded, not resolved. A drafting agent may not answer them.

1. **B5 / C6 — dual-use position. ANSWERED 18 July 2026. Retained, not deleted, so the numbering
   holds and so the answer is visible where the question was.** The question asked what terms govern
   use of the influence-operations targeting schema and whether technical enforcement is required
   before publication. Both halves are settled: eight controls apply, and technical enforcement is
   mandatory while disclosure and acceptable-use language are supplementary. See C6. **The answer
   did not close C6** — it replaced a decision gate with an implementation gate. Four narrower
   questions arising from it are recorded as 16–19 below.
2. **`NOTICE.md:11`.** Was "The source code is publicly visible for evaluation and portfolio
   purposes" written as a present statement of fact, or as a description of the intended
   post-publication position? It currently contradicts `HANDOFF.md:13`.
3. **Audit §8 decision 5 (packaging).** `uv` and `pyproject.toml` remain undecided, and C1's
   exact install command cannot be fixed until it is settled.
4. **Untracked working-tree content.** As of 19 July 2026 there are ten untracked paths: seven
   files under `docs/delivery/` and the directories `docs/design/`, `docs/safety/` and
   `docs/world-model/`. Each must be committed or removed. C12 check 4 cannot pass while any of
   them sits unreviewed.
5. **Audit §8 decision 1, second half.** The licence decision is settled — none, deliberately,
   all rights reserved. But the audit's sub-instruction to "add the file so tooling can detect
   it" is unsatisfied: there is no `LICENSE` file at the root. Is a machine-detectable file
   wanted, or is `NOTICE.md` deliberately the only artefact?
6. **Commit metadata (C12 check 6).** Commit `71fa329` carries
   `Aries Russell <ariesd.russell@gmail.com>`, which becomes permanently public at the flip and
   cannot be changed afterwards without rewriting history. Is publishing that address intended?
7. **C1 scope.** `HANDOFF.md` § Publication exit criteria (`:96`) says "a supported environment", singular, without naming one.
   Which environments are supported, and whether verifying more than one is a publication
   precondition, is an owner scope decision. It interacts with question 3 (packaging).
8. **C11 README link.** Should the root `README.md` be required to link to the known-limitations
   document? `HANDOFF.md` § Publication exit criteria (`:101`) requires only that the document be committed. The drafter proposed
   the link; it is not sourced, and its siting test is not command-verifiable.
9. **Reconciling the audit's stale citations.** The drafter recommends fixing the audit's dead
   citations (listed under C11) before C11 is ticked. This is not required by `HANDOFF.md`, and
   amending a closed audit touches the standing constraint that the broad audit is closed. Should
   it become a gate condition, be done outside the gate, or not be done?
10. **Audit §8 decisions 3 and 7** (Mesa as ABM substrate; `PLAN.pdf` as canonical plan format)
    remain open. Neither is listed as a publication blocker in A3 nor as an exit criterion in
    `HANDOFF.md` § Publication exit criteria (`:96-102`). Whether either should nonetheless gate publication is for the owner to
    decide; this draft does not decide it.
11. **The `grep` exclusion scope.** The drafter widened the false-claim exclusion from
    `./docs/delivery/` to all of `./docs/` because new planning directories were tripping the
    detectors. This narrows what C2, C3, C5, C8, C13 and **C13A** can catch, and exempts
    `docs/design/`, `docs/safety/` and `docs/world-model/` — all intended for commit, so all will
    publish. C13A is the case to weigh hardest, because `docs/design/` is where a fixture-backed
    mock-up would sit and question 21 asks whether such an asset is a surface at all. The
    audit's own criterion at `CURRENT-STATE-AUDIT.md:433` uses no exclusion. Should the exclusion
    be narrowed back to `./docs/delivery/`, kept as widened, or replaced with a per-file allowlist
    so publishable planning records stay in scope? Changing a gate's sensitivity is an owner
    decision; the current setting is the drafter's and should be ratified or reversed.
12. **Whether C13 belongs in this gate at all.** C13 (dangling references, unresolved markers) is
    sourced to `CURRENT-STATE-AUDIT.md:431-433`, which are **Phase 0** exit criteria. `HANDOFF.md` § Publication exit criteria (`:96-102`)
    lists seven publication exit criteria and does not include it. Should C13 be a publication
    precondition, be moved to Phase 0 tracking, or be dropped from this gate?
13. **P0.4A has no source record in the repository.** C8A is the only criterion here that cannot
    cite a file and a line, because the founder decision establishing P0.4A was issued as an
    instruction to a workflow and exists nowhere in the tree **as a founder record**. Every other
    founder decision this gate relies on is recorded (`HANDOFF.md`, the audit, A3, the world-model
    requirement record). The derived records that now carry the decision —
    [`PHASE-0-REMEDIATION-PLAN.md`](PHASE-0-REMEDIATION-PLAN.md) §P0.4A, `RAID-REGISTER.md` R1/D10–D13,
    `CORRECTIVE-BACKLOG.md` CB-34 to CB-39 and
    [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
    — all cite it by date, so none of them can serve as its source. Should a dated P0.4A source
    record be created so C8A becomes independently verifiable?
14. **Do P0.4A-6 and P0.4A-8 gate publication?** Both test entity promotion, which does not exist,
    and the entity model that would define it is founder-designated backlog that "does not
    interrupt Phase 0 remediation" (`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md:5`). Read
    strictly, they pull world-model materialisation into the publication gate. The drafter
    recommends verifying them when the entity model is built and gating publication on the other
    eight plus the ADR — **but has not applied that**, because shrinking a founder-set gate is an
    owner decision. Both currently stand in the gate. Rule one way or the other.
15. **ADR-007 and the P0.4A ADR.** `scaffold/docs/ARCHITECTURE_DECISIONS.md:60-67` records the
    single-shared-RNG architecture as *Accepted*. P0.4A's ADR must explicitly reject sequential
    shared-PRNG use for authoritative behaviour, which puts the two in direct conflict. Must ADR-007
    be superseded before publication, or does annotating it as superseded-by-P0.4A suffice? This
    also bears on C8A's documentary check D2, which currently fails on `:60` and `:63`.
    **The records disagree on this and the disagreement is unresolved.**
    `PHASE-0-REMEDIATION-PLAN.md` §P0.4A and `CORRECTIVE-BACKLOG.md` CB-34 both state that the
    P0.4A ADR *supersedes* ADR-007; the drafted
    [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
    instead records "Supersedes: None … relates to ADR-007", which it would narrow rather than
    supersede. No agent may settle which is right; it is part of this question.

16. **B5-4 — by what test is an entity "real"?** The control forbids real persons, organisations and
    political populations as influence targets but does not state how realness is determined. A
    maintained denylist fails open on anything unlisted; author attestation fails open on a careless
    or dishonest author, and B5-8 rules it out as the *sole* mechanism since it is not technical
    enforcement; human review before admission does not fail open but does not scale. Until this is
    settled, B5-4 cannot be reduced to a command and C6 cannot be ticked.
17. **B5-5 — which attributes are protected characteristics, and what happens to the ones already
    declared?** `religion_majority` and `primary_language` exist in `Demographics`
    (`agent_schema.py:22-28`) and are inert. The three appeal scalars in `InfluenceSusceptibility`
    (`:72-77`) are **not** inert and already drive diffusion gain. The decision permits identity to
    affect exposure and cultural interpretation while forbidding it as an optimisation criterion,
    which is a real distinction but not yet a mechanical one. Does enforcement mean removing fields,
    gating their read sites, or asserting output invariance — and is an "identity appeal"
    persuadability scalar inside the prohibition or outside it?
18. **B5-7 — what evidence closes the UI half?** The API half is contract-testable across five
    endpoints. A rendered interface disclosure is verifiable by no command in this file, and this
    draft has not invented a proxy for it. A screenshot, a component test, or a reviewer's signed
    observation are all candidates and they are not equivalent.
19. **What authorises building the eight controls?** Controls B5-1 to B5-5 and B5-7 require changes
    under `scaffold/` — schema, loader, API responses and tests. The founder decision that settles
    the policy states explicitly that it authorises no feature implementation. So the decision is
    recorded and the work it implies is not yet commissioned. This is the same class of question
    already recorded against CB-17 in `CORRECTIVE-BACKLOG.md`, and it gates every row of C6 except
    B5-8.
20. **Does C13A belong in this gate, and do C0–C4 stay out of it?** C13A is drafter-proposed and
    sourced to no exit criterion or blocker — the same position as C13, and open question 12 applies
    to it in the same terms. The drafter's judgement is that the five Track C gates are conditions on
    a demonstration rather than on publication and belong in `RAID-REGISTER.md` (D14–D19) where they
    now sit, and that only the fixture-labelling obligation reaches the repository. **That is a scope
    judgement, and scope judgements are the owner's.** Confirm it, or direct that some or all of
    C0–C4 be added here.
21. **What counts as a fixture-backed surface, and how far does the label obligation reach?** The
    founder's condition names surfaces. It does not say whether a committed screenshot, a recording,
    a design mock-up under `docs/design/`, or a Markdown page embedding any of them is a surface for
    this purpose. The question is not academic: `docs/design/` is intended for commit, so it will
    publish, and the widened `grep` exclusion at open question 11 already exempts it from every
    false-claim detector in this file. If design assets are in scope, C13A's checks need a path that
    reaches them.
22. **Must the label be verbatim, and what evidence closes C13A when an artefact exists?** A
    character-exact label — em dashes included — is checkable by command; a conspicuous equivalent is
    not. And no command in this file can establish that a label is *visible without interaction*
    rather than merely present in the file. A screenshot, a component test, or a reviewer's signed
    observation are all candidates and they are not equivalent. This is open question 18's problem
    in a second place, and the two should probably be answered together.

Decisions 8.1 (licence), 8.2 (visibility and the publication gate), 8.4 (reproducibility wording)
and — since 18 July 2026 — **8.6 (dual-use)** are **settled** and are not reopened here. Note that
8.6 being settled is not the same as C6 passing; see C6 and question 19.

---

## Scope of this draft

Stated plainly, so the record is not read as claiming more than it did.

- Every status above was established by reading files and running `grep`, `git`, `ls`, `wc` and
  `find` on 19 July 2026 at commit `71fa329`. **No code from this repository was executed.** The
  test suite was not run, the engine was not run, no environment was created, nothing was
  installed, and none of the evidence scripts in `docs/delivery/evidence/` were re-run.
- Two classes of result quoted above were produced by earlier sessions and are **carried, not
  reproduced**: (a) the AST import parse cited in C10, which required executing Python and was not
  re-run here; and (b) the runtime figures from `A3-VERIFICATION-RESULTS.md` — the 40-tick hash
  equality and the `TestClient` result — which that document recorded from execution. The AST parse
  in C10 is labelled as carried at the point of use. Runtime figures drawn from A3 are attributed
  to A3 by section and, since this revision, carry a carried-not-reproduced marker at C2; **treat
  every A3-sourced figure anywhere in this document as carried**, whether or not the marker is
  repeated locally.
- No new audit was performed. Only the specific claims this gate needs to assert were verified.
- **C8A was added on 19 July 2026** to carry founder decision P0.4A into this gate. Its status was
  established the same way as every other: by reading files and running `grep` and `ls`. **No test
  was written, no test was run, and no isolation property was measured.** The isolation tests C8A
  specifies do not exist, so most of its criteria are recorded as *not testable today* rather than
  as failures. The A3 figures it quotes are carried, not reproduced. No status recorded before this
  amendment was re-verified as part of it.
- **C6 was rewritten on 19 July 2026** to carry the founder decision of 18 July 2026 settling B5.
  Its status was established the same way as every other: by reading files and running `grep`.
  **No test was written, no test was run, and no control was implemented or measured.** All eight
  controls are recorded as requirements. The "Today" column of C6's criterion table describes the
  tree as it stands and must not be read as partial compliance — nothing partially satisfies any
  control. No status recorded before this amendment was re-verified as part of it.
- **C13A was added on 19 July 2026** to carry the fixture-labelling condition of the Track C
  correction into this gate. Its status was established by `git ls-files`, `ls`, `wc` and `grep`.
  **No interface was rendered, no screenshot was taken, and no prototype exists to inspect** —
  `scaffold/frontend/` is a 67-line dev stub and none of the five C0 screens is built. C13A
  therefore passes **vacuously**, which is a statement about the absence of artefacts and not about
  compliance; it must be re-run before the flip. The five Track C gates C0–C4 were assessed and
  deliberately left out of this gate; that judgement is the drafter's and is open question 20. No
  status recorded before this amendment was re-verified as part of it.
- **The conforming corrections of 19 July 2026 verified only their own cross-references**, by
  `grep`: that `RAID-REGISTER.md` does carry R10 and D14–D19, so C13A's referral of gates C0–C4 to
  that register is not a dangling one; and that the nine quotations of the prototype label are
  distributed as C13A records them (two in `CORRECTIVE-BACKLOG.md`, three in
  `PHASE-0-REMEDIATION-PLAN.md`, two in `RAID-REGISTER.md`, two here). Nothing else was re-checked
  and no code was executed.
- No file other than this one was created or modified. No git write command was run.

---

## Sign-off

To be completed by the owner. **An AI agent must not fill in any field in this block.**

**Criteria status at sign-off** — re-run and record, do not copy the draft statuses above:

| # | Criterion | Pass / Fail | Verified by | Date |
|---|---|---|---|---|
| C1 | Clean installation works on a supported environment | | | |
| C2 | B1 — no false legality-validation claims | | | |
| C3 | B2 — no false CI claim | | | |
| C4 | B3 — no false persistence claim | | | |
| C5 | B4 — archetype-extensibility claim corrected | | | |
| C6 | B5 — the eight dual-use controls implemented and verified | | | |
| C7 | README accurate on what is implemented | | | |
| C8 | Determinism and replay claims corrected | | | |
| C8A | P0.4A — deterministic randomness architecture | | | |
| C9 | Test scope accurately described | | | |
| C10 | Install-blocking dependencies removed/optional | | | |
| C11 | Audit + known-limitations committed | | | |
| C12 | Secrets / personal-data / content review | | | |
| C13 | No dangling references or unresolved markers | | | |
| C13A | Fixture-backed prototype artefacts labelled *(drafter-proposed — see OQ 20)* | | | |

**Environment(s) used for C1** — which environments are supported is open question 7:

- Host / OS: ______________________  interpreter version: ____________  result: ____________
- Host / OS: ______________________  interpreter version: ____________  result: ____________

**AST import parse re-run for C10** (output, or "not re-run"): ______________________

**C8A — P0.4A item status.** Record each; do not tick C8A from a summary judgement. Open question 14
must be answered before P0.4A-6 and P0.4A-8 can be marked out of scope rather than failed.

| Item | Pass / Fail / Out of scope (per OQ 14) | Evidence |
|---|---|---|
| P0.4A-1 no global `random` API | | |
| P0.4A-2 no unrestricted root-generator access | | |
| P0.4A-3 stable stream keys, no `hash()` | | |
| P0.4A-4 RNG algorithm and version recorded | | |
| P0.4A-5 unrelated entity does not perturb | | |
| P0.4A-6 promotion does not perturb established entities | | |
| P0.4A-7 iteration reorder is inert where declared | | |
| P0.4A-8 repeated promotion is identical | | |
| P0.4A-9 every draw attributable to subsystem/entity/purpose | | |
| P0.4A-10 injected-draw isolation test exists and passes | | |
| P0.4A-ADR ADR selects an approach and rejects shared sequential PRNG | | |
| D1 no false isolation claim *(drafter-proposed)* | | |
| D2 shared-stream architecture not presented as sufficient *(drafter-proposed)* | | |

**Isolation test command and output for C8A** (or "not run"): ______________________

**C6 — B5 control status.** Record each; do not tick C6 from a summary judgement, and do not tick it
from the existence of the 18 July 2026 decision — that decision is what created these rows. Per
control B5-8, the evidence for B5-1 to B5-5 and for the API half of B5-7 must be a **test
reference**. A row whose evidence is a document, a disclaimer or a policy statement does not pass.

| Control | Pass / Fail | Evidence (test reference — not a document) |
|---|---|---|
| B5-1 influence mechanics only in explicitly fictional worlds | | |
| B5-2 loader requires `world_mode: fictional`, fails closed | | |
| B5-3 real-world scenario import disabled, asserted by test | | |
| B5-4 real persons/organisations/political populations not targetable *(blocked on open question 16)* | | |
| B5-5 protected characteristics not optimisation criteria *(blocked on open question 17)* | | |
| B5-6 fictional aggregate diffusion still works — non-regression | | |
| B5-7 API discloses fictional world (contract test, all five endpoints) | | |
| B5-7 UI discloses fictional world *(evidence form is open question 18)* | | |
| B5-8 no control closed by prose alone — reviewer confirms rows above | | |

**C14 — Owner approval**

I have reviewed the criteria above. C1 to C13 pass, **C8A and C13A included** — or, where I have
ruled a drafter-proposed criterion out of this gate (C13, C13A: open questions 12 and 20), I have
recorded that ruling above rather than left the row blank. I approve making the MERIDIAN repository
public.

- Owner name: ______________________________________________
- Signature: _______________________________________________
- Date: ____________________________________________________
- Commit SHA approved for publication: _____________________

**Post-flip record**

- Date and time of visibility change: _______________________
- Command run: `gh repo edit --visibility public --accept-visibility-change-consequences`
- Commit SHA public at the moment of the flip: ______________
