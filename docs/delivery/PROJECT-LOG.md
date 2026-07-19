# Project log and logging policy

**Status:** DRAFT pending owner review.
**Date:** drafted 18 July 2026; revised 19 July 2026 after adversarial review.
**Date confidence:** the drafting date is **document-stated** — it is asserted by this record and was
not independently timestamped. The revision date is **exact**: system clock at revision, `date` →
`Sun Jul 19 11:50:28 2026`.
**Drafted by:** an AI agent. The standing constraint at `HANDOFF.md` § Standing constraints (`:138`) reads: "AI agents may draft
records but may not approve their own decisions." This document adopts a stricter reading — an agent
approves no decision, whether or not it is its own — and flags that widening as a drafting choice for
the owner to confirm or narrow. Nothing in this document is approved until the owner marks it so.

This document is in two parts. Part 1 is the policy: what gets logged, by whom, in what form, and
what counts as evidence. Part 2 is the log itself, backfilled from the documents and from git.

Where a date cannot be established from a document or from git history, this record says so rather
than estimating one. **One date is firm:** the git author timestamp of the single commit,
`2026-07-18T22:41:55+01:00`. Beyond that, 18 July 2026 appears as a *self-stated* date in the four
tracked governance documents — `HANDOFF.md:3`, `NOTICE.md:45`,
`docs/delivery/CURRENT-STATE-AUDIT.md:3` and `docs/delivery/A3-VERIFICATION-RESULTS.md:3` — which
establishes what those documents assert about themselves, not when the work was done. The same date
is also self-stated in numerous untracked Phase B and world-model records drafted alongside this one.
Command: `grep -rn "18 July 2026" --include=*.md .`

---

# Part 1 — The policy

**This policy is a draft proposal and is not in force.** It is written in the imperative below
because that is how a policy reads once adopted, but adopting a governance control is the owner's
decision. Nothing in Part 1 binds anyone until the owner approves it.

## 1.1 Why this policy exists (plain English)

This project's single worst defect is that its documentation has claimed properties the code does
not have. The audit found that pattern across CI, legality validation, database persistence and
archetype extensibility (`docs/delivery/CURRENT-STATE-AUDIT.md:13`; blockers B1 to B4 at
`docs/delivery/A3-VERIFICATION-RESULTS.md:241-244`). `HANDOFF.md:70` adds replay claims to the same
correction list under P0.1; the audit's verdict paragraph does not list replay among that set, so it
is cited separately here rather than attributed to the audit.

The repository is held private specifically so that this can be fixed before anyone reads it
(`HANDOFF.md:13-19`). **[unverified]** — that the repository is in fact private rests on that
assertion and was not independently observed; establishing it would require a `gh` visibility
command, which the standing constraints prohibit. See the closing section.

A project log is normally a convenience. Here it is a control. If the log is allowed to drift in the
same way the documentation drifted, the project loses the one record that is supposed to be able to
tell you what really happened. So the log has rules, and the rules are stricter than a project of
this size would usually need.

The short version: write down what you did, when, and how somebody else could check it. If you
cannot show how it could be checked, say that you cannot, and log it as unverified. An honest
"not verified" is a correct entry. A confident overstatement is a project-level failure.

## 1.2 What must be logged

An entry is required for each of the following:

| Event | Logged when |
|---|---|
| A decision that changes scope, architecture, dependencies, licence, or visibility | At the point of decision |
| Any change to a claim the project makes about its own capabilities | At the point of change |
| Completion or closure of an audit, review, or verification pass | At closure |
| Creation, publication, or supersession of a governance record | At creation |
| A handoff between machines, environments, or working sessions | At handoff |
| Discovery that a previously logged statement was wrong | On discovery, as a superseding entry |
| A phase transition in the Phase 0 remediation sequence | On entry to and exit from the phase |

Routine code edits do not need log entries; git history covers those. The log covers decisions,
claims, closures and handoffs — the things git does not record.

## 1.3 When entries are written

At the time of the event, or as a backfill entry that is explicitly labelled as a backfill. Part 2
of this document is a backfill in its entirety and is labelled as such. A backfilled entry must
state the evidence it was reconstructed from, because a backfill written from memory is exactly the
failure mode this policy exists to prevent.

## 1.4 Who may write, and who may approve

- **Anyone working on the project, including AI agents, may draft an entry.**
- **AI agents may not approve a decision, may not mark an open question resolved, and may not
  record their own output as owner-accepted.** Where an entry requires a human judgement, the agent
  writes it as an open question addressed to the owner and leaves it open.
- **Only the owner approves.** Approval is recorded by a superseding entry that states the approval.
  Whether the owner may instead amend a prior entry's status line in place is left open below (§1.7),
  because that is an exception to the append-only rule and its scope is the owner's to set.

The standing constraint at `HANDOFF.md` § Standing constraints (`:138`) reads, verbatim: "AI agents may draft records but may
not approve their own decisions." The rule stated above is **stricter** than that source — it denies
an agent approval of *any* decision, not only its own. The widening runs in the conservative
direction, but it is a drafting choice rather than a restatement, and is flagged here for the owner
to confirm or narrow rather than presented as what HANDOFF says. `HANDOFF.md` § Standing constraints (`:139-140`) separately
requires human approval for architecture, dependencies, licence, migrations, auth, security controls,
public releases, and anything affecting determinism or authoritative state.

## 1.5 The two-layer requirement

Every entry has two layers, and both are mandatory:

1. **A plain-English layer.** A non-technical reader must be able to follow what happened and why it
   mattered, without opening a source file.
2. **A technical-evidence layer.** File and line citations in `path:line` form, a reproducible
   command, or a recorded execution result.

The two layers are not a summary and a detail. They are two audiences. If the plain-English layer
cannot be written without becoming vague, that usually means the underlying claim is not yet
understood well enough to log.

## 1.6 What counts as evidence

Evidence is one of exactly three things:

- **A file and line reference** in `path:line` form, which a reader can open and check.
- **A reproducible command**, given exactly as run, including the working directory and any
  environment the command depends on.
- **An execution result**, quoted as produced rather than paraphrased.

The following are **not** evidence, and an entry resting on them must be marked unverified:

- An assertion, however confident, including one made by the owner or by a prior document.
- A claim in another document in this repository. Documents in this repository have been shown to
  contain untruths; citing one records where a claim came from, not that the claim is true.
- Inference from absence, unless the search that established the absence is given as a command.

**The two lists overlap, and the distinction matters.** A `path:line` citation is evidence that the
cited document *says* X. It is not evidence that X is true. Where an entry relies on a repository
document's assertion about the world — rather than about its own contents — the claim must be marked
**[unverified]** and the asserting document named. Part 2 cites repository documents constantly; the
marker, not the citation, is what distinguishes "this document says so" from "this is so."

Where an entry mixes verified and unverified material, it must separate them. The convention used in
Part 2 is a bracketed marker: **[verified]** for a claim backed by evidence of one of the three
kinds, **[unverified]** for a claim that rests on an assertion, and **[inference]** for a conclusion
drawn from verified facts by reasoning that is stated in the entry.

## 1.7 Append-only, and how corrections work

The log is append-only.

A previous entry is never edited to make it correct. A correction is a **new, dated entry** that
names the entry it supersedes and states what was wrong. The superseded entry stays where it is.

The reason is specific to this project rather than a general preference. The defect under
remediation is documents that were quietly brought into line with a story instead of with reality.
An append-only log makes the correction itself visible, so a reader can see that a claim was wrong,
when it was found to be wrong, and on what evidence. A silently edited log would reproduce the
defect inside the control designed to catch it.

Anything that changes what an entry asserts requires a superseding entry.

**Open question 5 — the scope of any in-place exception is an owner decision.** A draft of this
policy allowed two carve-outs: recording approval by amending an entry's status line, and making
typographical fixes in place. Both sit uneasily with an absolute append-only rule. Changing a status
line from `drafted` to `owner-approved` changes what the entry asserts, which the rule above says
requires a superseding entry. And a general permission to edit a governance record in place is
precisely the mechanism this control exists to catch, in a project whose stated failure mode is
documents quietly brought into line with a story. This draft therefore states the rule without
exceptions and refers the question to the owner: whether any in-place edit exception should exist,
and if so, exactly which. An agent must not settle this.

## 1.8 Entry format

```
### YYYY-MM-DD — Short title
**Type:** decision | closure | record | handoff | correction | backfill
**Status:** drafted | owner-approved | superseded by <entry>
**Date confidence:** exact | document-stated | unknown

Plain English: what happened and why it matters.

Evidence:
- path:line, or a command, or a quoted execution result.

Open questions for the owner, if any.
```

Where a date cannot be established, `**Date:**` reads `undated` and `**Date confidence:** unknown`,
with a statement of what is known about the ordering instead. Estimating a date is not permitted.

---

# Part 2 — The log

**This entire part is a backfill, drafted 18 July 2026 from the repository's documents and from git
history.** No entry here was written at the time of the event it describes. Each entry states what
it was reconstructed from.

A general limitation applies to every entry below: the reconstruction was made by reading documents
and running read-only git commands. No code was executed in the course of drafting this log, and no
network call was made. Claims about runtime behaviour are cited to the documents that recorded the
execution, and are marked accordingly.

---

### Undated (on or before 18 July 2026) — Broad audit conducted and closed

*(HANDOFF describes this as a "nine-dimension" audit; that descriptor is not corroborated by the
audit document and is confined to Open Question 2 below.)*

**Type:** closure (backfilled)
**Status:** drafted, pending owner review
**Date:** undated — see below
**Date confidence:** unknown

**Plain English.** An audit was run across the whole local tree, covering the backend, the schemas,
the scenarios, the frontend, the scaffold documentation and the root governance documents.

**[unverified — this is the audit's account of its own method, not an observation]** The audit
records that candidate findings were adversarially re-verified, each handed to a second pass whose
explicit job was to refute it, quote the contradicting line, or correct its severity; and that
claims were tested by execution where execution was possible
(`docs/delivery/CURRENT-STATE-AUDIT.md:23`). How the work was actually carried out is not
recoverable from the tree, which holds a single commit and no prior revision. **[unverified]** how
many agents were involved, and whether "multi-agent" is the right characterisation at all — see
Open Question 1.

The audit's verdict was that the repository is neither publishable nor execution-ready, and it
treated those as two separate judgements.

Not publishable, for **two** independent reasons, both given in the same paragraph at
`docs/delivery/CURRENT-STATE-AUDIT.md:13`. First, several documents state in the present indicative
properties the code does not have. Second, the campaign and cohort schemas are, in the audit's words,
"a field-for-field influence-operations targeting template", the plan claims a near one-to-one DISARM
Red Framework mapping, and "every stated safeguard is prose with no technical or licence enforcement
behind it". The second limb is publication blocker B5 and audit decision 8.6, and — unlike the first
— it does **not** clear by correcting text. A reader must not take this entry as saying publication is
gated only on claim accuracy.

Not execution-ready, because the three simulation tiers do not causally influence one another.

**Evidence.**
- Scope, method and verdict: `docs/delivery/CURRENT-STATE-AUDIT.md:1-27`.
- Adversarial re-verification method: `docs/delivery/CURRENT-STATE-AUDIT.md:23`.
- Refuted findings, listed with reasons: `docs/delivery/CURRENT-STATE-AUDIT.md:572-591`.
  **[verified]** Appendix A contains eleven data rows, and its own opening sentence at `:574` reads
  "Eleven candidate findings were raised during analysis and refuted on verification." Command:
  `sed -n '572,591p' docs/delivery/CURRENT-STATE-AUDIT.md | grep -c '^| [A-Za-z0-9\`]'` → `12`,
  which is eleven data rows plus the header row.
- Final severity counts: `docs/delivery/CURRENT-STATE-AUDIT.md:596` — "**2 critical, 15 major,
  approximately 50 minor and 45 informational, with 11 refuted**".

**Date.** The audit document states 18 July 2026 at `docs/delivery/CURRENT-STATE-AUDIT.md:3`. That
is the document's stated date, not an independently observable date of the work. The audit file is
contained in commit `71fa329`, authored `Sat Jul 18 22:41:55 2026 +0100`, which establishes that the
document existed by that timestamp. **[verified]** Command:
`git ls-tree -r --name-only 71fa329` lists `docs/delivery/CURRENT-STATE-AUDIT.md`. When the audit
work itself was carried out is not recoverable from the tree, because the history is a single commit
with no prior revision to compare against.

**Open question 1 — the finding counts do not reconcile.** Two documents in this repository give
different numbers for the same audit, and this record will not choose between them.

| Source | Statement |
|---|---|
| `HANDOFF.md:29` | "124 agents, 128 candidate findings, 112 survived, 11 refuted" |
| `CURRENT-STATE-AUDIT.md:25` | "**124 candidate findings were assessed. 11 were refuted and dropped**" |
| `CURRENT-STATE-AUDIT.md:596` | "2 critical, 15 major, approximately 50 minor and 45 informational, with 11 refuted" |

What appears to reconcile: the audit's own final counts sum to 112 (2 + 15 + 50 + 45), which matches
HANDOFF's "112 survived", and both sources agree on 11 refuted, which Appendix A's eleven rows
corroborate. **[verified]** that these figures appear as quoted at the cited lines, and that
2 + 15 + 50 + 45 = 112. **[inference]** that this amounts to a reconciliation — because one component
is given by the audit itself as approximate, as the next paragraph records.

What does not reconcile: HANDOFF attributes the number 124 to *agents* and gives 128 as the
candidate-finding count; the audit attributes 124 to *candidate findings* and gives no agent count
anywhere. Both cannot be right. Note also that the audit's own component figures are approximate
("approximately 50", and 45 given without qualification), so 112 is not a hard total either.
**[inference]** — this is a conflict between two written sources, resolved by neither.

**Owner decision required:** which figures are correct. Until that is settled, this log does not
assert an agent count or a candidate-finding count. This record additionally *recommends*, for the
owner's decision rather than as a standing rule, that no public description of the audit use either
number until the conflict is settled. Publication is owner-gated (`HANDOFF.md:13-19`, exit criteria
at `:84-94`), so an agent may propose this but cannot impose it.

**Open question 2 — "nine-dimension" is not corroborated.** `HANDOFF.md:29` calls this a
"nine-dimension audit". The audit document refers to "the dimensional analysis"
(`CURRENT-STATE-AUDIT.md:108`) and to "items that appeared under more than one analytical dimension"
(`:596`), but nowhere enumerates nine dimensions or names them. **[verified]** by
`grep -rni "dimension" docs/delivery/CURRENT-STATE-AUDIT.md`, which returns exactly the two lines
quoted. The count of nine therefore rests on the HANDOFF assertion alone and is marked
**[unverified]** here.

---

### 18 July 2026 — A3 targeted re-verification completed; broad audit CLOSED

**Type:** closure (backfilled)
**Status:** drafted, pending owner review
**Date confidence:** document-stated

**Everything in this section is reported from the A3 document
(`docs/delivery/A3-VERIFICATION-RESULTS.md`) and was not re-executed in drafting this log. Treat the
whole section as [unverified here]: the underlying results rest on A3's recorded execution, not on
any observation made while writing this entry. The supporting `path:line` anchors are in the Evidence
block below.**

**Plain English.** Five findings from the broad audit had never been properly checked, because the
verification agents assigned to them failed with API errors. Rather than dispatch a third round of
agents, those checks were run directly against the code, together with one independent re-derivation
of each of the two critical findings. Seven checks in total. Nothing was refuted. Two findings were
corrected in ways that mattered, and one of the corrections exposed a defect not previously
identified.

The first correction concerns whether the three simulation tiers influence one another. A3 found that
changing a cohort's configuration does change national indicators, which looks like the tiers are
connected, but that this is an artefact of how random numbers are drawn from a single shared stream
rather than a modelled cause. Underneath that sat the new defect: A3 found no named random-number
substreams, so adding or removing a single draw in one subsystem shifts every later draw in every
other subsystem.

The second correction strengthened the audit rather than weakening it. The runaway saturation of the
national indicators had been suspected of being an artefact of the placeholder agent behaviour, which
would have made it a tuning problem that disappears once a real model is connected. A3 found that it
persists under varied action selection, and that the engine contains no cost, cooldown, decay or
opposing-pressure mechanism. On A3's account that moves it from calibration to architecture.

A3 records the broad audit as closed on this basis: nothing refuted, no new publication blocker,
critical count unchanged at two. The closure itself is stated at
`docs/delivery/A3-VERIFICATION-RESULTS.md:3` ("**Status:** complete. Broad audit CLOSED."). The
passage at `:251-257` is headed "## Recommendation" and reads "**Close the broad audit.**" — that is
the recommendation to close, not the record of closure, and this log cites the two separately.

**Evidence.**
- Scope, status and the seven checks: `docs/delivery/A3-VERIFICATION-RESULTS.md:1-5`, verdict table
  at `:40-50`.
- Method, including the five failed verifier agents and the decision to execute directly:
  `docs/delivery/A3-VERIFICATION-RESULTS.md:23`.
- Environment recorded for the execution: `docs/delivery/A3-VERIFICATION-RESULTS.md:27` — "Windows
  11 26200, CPython 3.13.9, mesa 2.4.0, pytest 8.4.2, `LongPathsEnabled=0`", with `litellm`
  deliberately absent.
- RNG-contamination result: `docs/delivery/A3-VERIFICATION-RESULTS.md:142-175`.
- Saturation result and escalation: `docs/delivery/A3-VERIFICATION-RESULTS.md:177-204`.
- Closure, as stated: `docs/delivery/A3-VERIFICATION-RESULTS.md:3` — "**Status:** complete. Broad
  audit CLOSED."
- Closure *recommendation*, a separate passage: `docs/delivery/A3-VERIFICATION-RESULTS.md:251-257`,
  headed "## Recommendation".
- Evidence scripts are preserved and are in the commit: **[verified]** `git ls-tree -r --name-only
  71fa329` lists `docs/delivery/evidence/a3_direct.py`, `a3_rng_isolation.py`, `probe.py`,
  `verify_criticals.py` and `unverified5.json`.

**Limitation of this entry.** The A3 execution results are quoted from the A3 document. They were
not re-executed while drafting this log. **[verified]** there is no virtualenv at the conventional
location under `scaffold/backend`. Command, run from the repository root:

```
ls -a scaffold/backend
```

Output:

```
.
..
Dockerfile
app
requirements.txt
tests
```

**[inference]** Re-executing A3 therefore probably requires reconstructing an environment. This does
not establish that the scripts cannot be run: no search was made for a suitable interpreter or
virtualenv elsewhere on the machine or elsewhere in the tree, and the absence of this one directory
does not rule one out. The reproduction commands are recorded at `HANDOFF.md` § Reproducing the evidence (`:142-152`) and
`docs/delivery/A3-VERIFICATION-RESULTS.md:30-34`.

**Result recorded.** Publication blockers after A3: five, unchanged, deduplicated as B1 to B5
(`docs/delivery/A3-VERIFICATION-RESULTS.md:235-247`). Four clear by text correction. B5, the
dual-use influence-targeting schema, clears only by owner decision.

---

### Undated (on or before 18 July 2026) — Governance notices in place

**Type:** record (backfilled)
**Status:** drafted, pending owner review
**Date:** undated
**Date confidence:** unknown for the entry as a whole — `NOTICE.md` states its own review date of
18 July 2026; `CHARTER.md` and `README.md` carry no date, and only their presence in commit
`71fa329` is established. Per §1.8, the entry is therefore undated rather than dated to the one
document that carries a date.

**Plain English.** Three governing documents are present in the tree: a charter that states the
project's non-negotiable design principle and overrides every other document; a copyright and
licensing notice recording an all-rights-reserved position with no open-source licence; and a root
README. When any of the three was written is not recoverable from the tree.

The charter is explicit that where it and an implementation disagree, the implementation is wrong.
The notice is explicit that it is a statement of the current position rather than a final licensing
decision.

**Evidence.**
- Charter's governing status: `CHARTER.md:3-5`.
- Notice, all rights reserved: `NOTICE.md:3`. Position described as provisional: `NOTICE.md:16` and
  `NOTICE.md:41-43`. Stated review date: `NOTICE.md:45` — "Last reviewed: 18 July 2026."
- Licence decision **as recorded** (not as independently established): `HANDOFF.md:22-23` — "Licence:
  **none, deliberately.**" **[unverified]** that the decision is settled as a matter of fact; the
  citation evidences only that HANDOFF asserts it.
- All three files are in commit `71fa329`. **[verified]** by `git ls-tree -r --name-only 71fa329`.

**Dates.** `NOTICE.md` states its own review date. `CHARTER.md` and `README.md` carry no date at
all; the only thing established about them is that they existed by the commit timestamp. This log
does not estimate when they were written.

**Known defect in this record, carried forward not resolved.** `NOTICE.md:11` states in the present
indicative: "The source code is publicly visible for evaluation and portfolio purposes." The
repository is private per the settled decision at `HANDOFF.md:13-19`. **[verified]** that the two
sentences say these things; **[unverified]** whether the repository is in fact private, because
establishing that requires a `gh` visibility command, which the standing constraints prohibit. The
private status therefore rests on the HANDOFF assertion, not on an observation.

**Open question 3.** Was `NOTICE.md:11` intended as a present statement of fact, or as a description
of the position after publication? It reads as the former and contradicts `HANDOFF.md:13`. This is a
claim-accuracy defect of exactly the class Phase 0 exists to correct, sitting inside the document
that records the licensing decision. The owner should decide the intended reading; an agent must not.

**Stale citation, re-anchored.** The audit at `CURRENT-STATE-AUDIT.md:237` cites `COPYRIGHT.md` as
the file holding the licensing position. No `COPYRIGHT.md` is present in the repository; the position
now lives in `NOTICE.md`. `README.md:96` points at the same non-existent file, so that link does not
resolve. **[verified]** by two commands, both run from the repository root — the first establishing
absence from the 55-file tracked set, the second (added at the 19 July revision) establishing absence
from the working tree as a whole, tracked or not:

```
$ git ls-files | grep -i copyright
(no output)

$ find . -path ./.git -prune -o -iname "COPYRIGHT*" -print
(no output)
```

The second command matters because the first alone would be satisfied by an *untracked*
`COPYRIGHT.md`, which would make `README.md:96` resolve — and this tree does currently carry
untracked paths.

No claim is made here about whether other broken markdown links exist. No repository-wide link
enumeration was run in drafting this entry, and running one to support a superlative would exceed
what this record needs to assert. This is recorded as a re-anchoring of the audit's stale citation,
which the log legitimately needs in order to cite `:237` accurately — not as a new audit finding.
The broad audit is closed and this record does not reopen it.

---

### 18 July 2026, 22:41:55 +01:00 — Repository placed under version control; initial commit

**Type:** record (backfilled)
**Status:** drafted, pending owner review
**Date confidence:** exact — git author timestamp

**Plain English.** The project was put under version control. There is one commit. It contains the
scaffold, the charter, and the current-state audit, along with the handoff, the notice, the README,
the plan PDF and the A3 verification results and its evidence scripts. A remote is configured on
GitHub. The **local** branch is `main`, and the locally cached `origin/HEAD` points at `origin/main`;
the remote's actual default branch was **not** checked, no fetch having been performed. **[unverified]**
that `main` was a deliberate choice rather than a git default — that rests on the assertion at
`HANDOFF.md:21`, not on anything in the tree.

This matters beyond housekeeping: several audit findings were written at a time the audit records as
having had no `.git` directory at all (`docs/delivery/CURRENT-STATE-AUDIT.md:13`, `:339`).
**[unverified]** — that pre-commit state cannot now be observed, the history being a single commit
with no prior revision; it rests on the audit's own assertion. On that basis, a fact each of those
findings rests on has since changed. What changed is recorded
below rather than edited in, in keeping with the append-only rule. This log does not judge whether
those findings are thereby wholly stale, partly stale, or still open — that is Phase 0 work and an
owner call.

**Evidence.** **[verified]** Command, run from the repository root:

```
git log --format='%H%n%an <%ae>%n%aI%n%s'
```

Output:

```
71fa329bd09506e8c657428cf92073ec1dda1bed
Aries Russell <ariesd.russell@gmail.com>
2026-07-18T22:41:55+01:00
Initial commit: MERIDIAN scaffold, charter, and current-state audit
```

Further commands, run from the repository root, with output quoted as produced:

```
$ git remote -v
origin  https://github.com/CypherTechAries/project-meridian.git (fetch)
origin  https://github.com/CypherTechAries/project-meridian.git (push)

$ git ls-files | wc -l
55

$ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```

That `main` is a deliberate choice rather than a git default is **[unverified]** here: it rests on
the assertion at `HANDOFF.md:21`, a repository document, not on anything observable in the tree.

**What is not established.** **[unverified]** Whether the remote repository is private. No `gh`
command was run and no network call was made, per the standing constraints. **[unverified]** Whether
commit `71fa329` has actually been pushed to the server: the local tracking ref `origin/main` points
at the same commit, which is consistent with a completed push, but no fetch was performed, so this
reflects last-known local state rather than the server's current state.

**Note on three prior audit statements.** Recorded here rather than by editing the audit. This table
records what has changed in the tree; it assigns no status to any finding:

| Prior statement | What has changed |
|---|---|
| `CURRENT-STATE-AUDIT.md:339` — finding 37, "The repository is not under version control", evidenced as "`git rev-parse` returns \"fatal: not a git repository\". No history, no author, no diff, no remote." | **What has changed:** `.git` now exists, with commit `71fa329`, a named author, and a configured remote. Note that this is the finding itself, not merely a fact supporting it. Whether the finding is therefore wholly stale, partly stale, or still open is Phase 0 work and an owner call; this log does not decide it and takes no position on the framing. |
| `CURRENT-STATE-AUDIT.md:372` — "Version control \| Missing \| No `.git` anywhere." | **What has changed:** the same fact. `.git` exists at commit `71fa329`. Whether the controls-table row should be re-graded, and whether the GitHub-level controls it lists (branch protection, CODEOWNERS, required checks, secret scanning) are now configured, is not established here — checking the remote would require a `gh` call the standing constraints prohibit. Status of the row: unchanged, pending owner review. |
| `A3-VERIFICATION-RESULTS.md:242` — blocker B2, "There is no CI and no `.git`." | **What has changed:** the `.git` half only. The "no CI" half still holds, and B2 still stands as a blocker on that basis. The underlying false claim is still live at `CHARTER.md:44`, which says `test_llm_gateway_cannot_write_state` "guards in CI". **[verified]** by the commands below. |

**[verified]** Evidence for the surviving "no CI" half of B2. Commands, run from the repository root:

```
$ ls -a .github
ls: cannot access '.github': No such file or directory

$ find . -path ./.git -prune -o \( -name "*.yml" -o -name "*.yaml" \) -print
./scaffold/docker-compose.yml
```

**These entries close nothing.** They record what has changed in the tree since the audit was
written. Whether any of the three findings is closed, re-graded or left open is Phase 0 work and an
owner call, and an AI agent may not make it.

---

### 18 July 2026 — Handoff between machines

**Type:** handoff (backfilled)
**Status:** drafted, pending owner review
**Date confidence:** document-stated

**Plain English.** **[unverified — `HANDOFF.md:3-4` asserts this; it was not independently
observed]** Work moved from the original machine to a faster terminal, because the original machine
was too slow to continue. `HANDOFF.md` was written as the resume point: it records the
repository status, the founder decisions it records as already settled, the section headed "Current
state of the code, stated honestly" (`HANDOFF.md:41`), the Phase 0 priority order P0.1 to P0.8, the
publication exit criteria, the deliberately-not-started backlog, the standing constraints, and the
commands for reproducing the audit evidence. This log records what those sections *contain*; it does
not vouch for the accuracy of the section so headed.

**[unverified]** At the point of handoff, Phase B (governance bootstrap) had not been started. This
rests solely on `HANDOFF.md:34` ("Not started, in order: 1. **Phase B — governance bootstrap.**"), a
repository document asserting a fact about the world, and was not independently established. This
document is one of the Phase B records.

**Evidence.**
- Date and reason: `HANDOFF.md:3-4` — "**Last updated:** 18 July 2026 / **Reason for handoff:**
  original machine too slow to continue; work moved to a faster terminal."
- Work completed at handoff: `HANDOFF.md:28-32`.
- Work not started, in order (Phases B, C, D): `HANDOFF.md:34-39`.
- Phase 0 priority order: `HANDOFF.md` § Phase 0 priority order (`:68-90`).
- Publication exit criteria, seven items, all unchecked: `HANDOFF.md` § Publication exit criteria (`:92-102`).
- Standing constraints, including that AI agents may draft but not approve: `HANDOFF.md` § Standing constraints (`:133-140`).

**State at the time of drafting this log.** **[verified]** Four representative B1 to B4 claims were
checked and are still live and uncorrected in the tree: `README.md:38` ("LLM proposes; engine
validates legality and computes cost/effect"), `CHARTER.md:44` ("guards in CI"),
`scaffold/docs/ARCHITECTURE_DECISIONS.md:29` ("We persist three things"), and
`scaffold/docs/ARCHITECTURE_DECISIONS.md:75` ("eighth archetype must require only a new
`scenarios/*.json`").

**[inference]** No corrective work appears to have landed against B1 to B4. This rests on those four
spot checks plus the clean working tree at commit `71fa329`, not on an exhaustive sweep of every
claim in the B1 to B4 set. It is not established that nothing anywhere has been corrected.

**Point-in-time observation, since overtaken.** At the moment this entry was drafted,
`docs/delivery/` contained no `PHASE-0-REMEDIATION-PLAN.md`. That is no longer true: sibling Phase B
records drafted in the same session, including a remediation plan, now exist as untracked files.
Absence claims about a live tree are the most perishable evidence there is; this one is retained
with its timestamp rather than deleted, in keeping with the append-only rule, and should not be read
as a standing property. Re-run `find docs -type f` before relying on it.

---

### 18 July 2026 — Founder world-model requirement recorded; currently uncommitted

**Type:** record (backfilled)
**Status:** drafted, pending owner review
**Date confidence:** document-stated

**Plain English.** A founder requirement covering the simulated society and the entity model was
written down and preserved verbatim. Its own header disposes it to the backlog, states explicitly
that it must not interrupt Phase 0 remediation, and states that nothing described in it is
implemented.

This entry exists mainly to record a fact about the tree's state that the earlier handoff notes do
not cover: the file is **not** under version control. It is untracked, so it is not in commit
`71fa329`. **[unverified]** whether it is present on the remote in any form: no fetch was performed
and no network call was made, so nothing here establishes the server's contents.

**Evidence.** **[verified]**
- `git status --porcelain`, run during the drafting session, listed `?? docs/world-model/` among
  the untracked paths. This log file was itself untracked at that moment, and other Phase B records
  drafted in the same session are untracked too. The entry asserts only that `docs/world-model/` is
  not in commit `71fa329`; it does **not** assert an exhaustive untracked-file list. The untracked
  set is a point-in-time observation of a mutable tree, not a standing property — re-run the command
  to see it now.
- File: `docs/world-model/FOUNDER-REQUIREMENT-2026-07-18.md`.
- Stated date and disposition: that file's lines 3-6 — "**Recorded:** 18 July 2026", "**Status:**
  Founder decision. Source record.", "**Disposition:** Backlog. **Does not interrupt Phase 0
  remediation.**"
- Self-limiting statement: that file's line 12 — "**Nothing described in this document is
  implemented.**"

**Note.** That document cross-references `docs/delivery/CAPABILITY-CLAIMS.md`
(`docs/world-model/FOUNDER-REQUIREMENT-2026-07-18.md:14`). **[verified as at the drafting of this
entry]** `find docs -type f` returned nine files at that moment, not including
`CAPABILITY-CLAIMS.md`. That was a snapshot of a mutable tree, not a standing property, and it has
since been overtaken: the file now exists as an untracked sibling Phase B record, and
`find docs -type f` now returns considerably more than nine. `CAPABILITY-CLAIMS.md` is listed as
Phase B work at `HANDOFF.md:35-37` ("corrected capability claims"), so the cross-reference reads as a
forward reference to a record not yet written rather than a link to a deleted file. **[inference]** —
this rests on the Phase B listing at `HANDOFF.md:35-37` alone. The later creation of the file by this
session's own drafting is *not* corroboration: it says nothing about what the original author
intended when writing the cross-reference. Re-run the command before relying on any file count here.

**Open question 4.** Whether `docs/world-model/` should be committed. This log does not commit it;
the standing constraints prohibit git write commands, and in any case the decision is the owner's.

---

### 18 July 2026 — Founder decision: P0.4A added to Phase 0 (deterministic randomness architecture)

**Type:** decision (backfilled 19 July 2026)
**Status:** drafted, pending owner review
**Date confidence:** **document-stated by derived records only.** See the sourcing limitation below.

**Plain English.** The founder ruled that the RNG-isolation defect A3 exposed becomes its own
Phase 0 workstream, **P0.4A — establish a deterministic randomness architecture**, placed between
P0.4 and P0.5. It is explicitly **not** a detail of the world model and explicitly **not** to be
hidden inside replay. The full order is now
`P0.1 → P0.2 → P0.3 → P0.4 → P0.4A → P0.5 → P0.6 → P0.7 → P0.8`.

Three parts of the decision change what other records may say:

1. **Sequencing.** P0.5 *specification* may proceed in parallel now. **P0.5 implementation, entity
   promotion and world-model materialisation may not proceed until P0.4A passes.**
2. **Scope.** Isolation is required by subsystem, entity, relationship or interaction, simulation
   purpose, and tick or event context where appropriate. **Per-entity streams alone are
   insufficient**, so records that specify per-entity substreams describe less than the decision
   requires.
3. **Evidence standard.** The existing determinism test is **insufficient**, because it would accept
   draw-order contamination as ordinary divergence. P0.4A requires **isolation tests**, not
   same-seed repetition tests.

The decision also requires an ADR that deliberately selects between stateful named substreams and
keyed / counter-based deterministic draws, and that **explicitly rejects** ordinary sequential calls
to a single shared PRNG for authoritative behaviour.

**Nothing was implemented, decided by any agent, or committed under this entry.** P0.4A has not
started; none of its ten exit criteria has been run.

**Evidence.**
- Derived records carrying the decision, all created or amended 19 July 2026:
  `docs/delivery/PHASE-0-REMEDIATION-PLAN.md` §P0.4A; `docs/delivery/RAID-REGISTER.md` R1, D10–D13,
  DEC8; `docs/delivery/CORRECTIVE-BACKLOG.md` CB-34 to CB-39;
  `docs/delivery/PUBLICATION-EXIT-CRITERIA.md` §C8A and criteria `P0.4A-1` … `P0.4A-10`,
  `P0.4A-ADR`.
- Drafted, unapproved ADR: `docs/adr/ADR-010-deterministic-randomness-architecture.md`, dated
  19 July 2026, **Status: Proposed**, Approval block empty, recommending keyed / counter-based
  deterministic draws. A recommendation is not a selection
  (`HANDOFF.md` § Standing constraints (`:138`)), so the ADR requirement is not discharged.
- Underlying defect, demonstrated by execution: `docs/delivery/A3-VERIFICATION-RESULTS.md:170-175`;
  script `docs/delivery/evidence/a3_rng_isolation.py`. Prior, milder grading: audit item 28,
  `docs/delivery/CURRENT-STATE-AUDIT.md:320`.

**Sourcing limitation, stated plainly. [unverified]** The decision was issued as an instruction to a
workflow and **no founder source record for it exists in the tree**, unlike the world-model
requirement recorded at `docs/world-model/FOUNDER-REQUIREMENT-2026-07-18.md`. Every record above
cites it by date, so none of them can serve as its source, and this entry inherits that gap rather
than closing it. `HANDOFF.md` § Phase 0 priority order (`:68-90`) still lists P0.1 to P0.8 without P0.4A and predates the
decision.
**Amended 19 July 2026.** The second sentence is superseded as to the item list only. By founder
decision of 19 July 2026, P0.4A was inserted into the canonical sequence at `HANDOFF.md` § Phase 0
priority order, P0.4A (`:76-83`). **The sourcing limitation itself is not closed:** `HANDOFF.md`
records the item and cites the 18 July decision by date, so there is still no founder source record
in the tree for that decision's scope or its ten exit criteria.

**Open questions for the owner.** Whether a dated P0.4A source record should be created
(`PUBLICATION-EXIT-CRITERIA.md` open question 13); which randomness mechanism is adopted
(`RAID-REGISTER.md` DEC8); whether the resulting ADR supersedes or merely narrows ADR-007
(`PUBLICATION-EXIT-CRITERIA.md` open question 15 — `PHASE-0-REMEDIATION-PLAN.md` §P0.4A and ADR-010
currently disagree); how the numeric change P0.4A will cause at an unchanged seed is authorised
(`PHASE-0-REMEDIATION-PLAN.md` OQ-9); and whether exit criteria 6 and 8, which are stated against
entity promotion, gate publication (`CORRECTIVE-BACKLOG.md` CB-39,
`PUBLICATION-EXIT-CRITERIA.md` open question 14).

---

### 18 July 2026 (drafted) / 19 July 2026 (revised) — This document drafted, then revised

**Type:** record
**Status:** DRAFT, pending owner review
**Date confidence:** **document-stated** for the drafting date — it is asserted by this record and
was not independently timestamped, and an earlier version of this entry wrongly graded it `exact`.
**Exact** for the revision date: system clock at revision, `date` → `Sun Jul 19 11:50:28 2026`. The
sibling Phase B record `docs/delivery/ADR-TEMPLATE.md:497` likewise states "drafted on 18 July 2026
and revised on 19 July 2026 after adversarial review". Individual commands attributed elsewhere in
this log to "the drafting session" cannot now be pinned to a particular day.

**Plain English.** The project log and its policy were drafted as part of Phase B, the governance
bootstrap, and revised the following day after an adversarial review of the draft. The log was
backfilled from the repository's documents and from git; no entry in it was written
contemporaneously with the event it describes.

The 19 July revision corrected claims in this document that outran their evidence. The changes are
listed in the revision note at the end of this entry. They are recorded as amendments to an unapproved
draft rather than as superseding entries under §1.7, because nothing here has yet been approved; if
the owner would rather see them as superseding entries, that is the owner's call to make.

Five open questions are raised and left open, addressed to the owner: the finding-count conflict
between `HANDOFF.md` and the audit; the "nine-dimension" description that the audit does not
corroborate; the intended reading of `NOTICE.md:11`; whether `docs/world-model/` should be
committed; and the scope of any in-place edit exception to the append-only rule.

**Evidence.** This file, `docs/delivery/PROJECT-LOG.md`. Phase B scope including "project log +
policy": `HANDOFF.md:35-37`.

**On whether any other file was modified. [unverified]** An earlier version of this entry asserted
flatly that no other file was modified, that nothing under `scaffold/` was touched, that no git write
command was run, and that no simulation behaviour was changed — with no evidence of any kind and no
marker. Under §1.6 that is an assertion, not evidence, and it should have been marked. The command
that would have substantiated it (`git status --porcelain`) existed at drafting time and was not
quoted, and the claim can no longer be substantiated retrospectively: the tree has since accumulated
further untracked Phase B and world-model paths drafted in the same and subsequent sessions, so a
clean-scaffold observation made now would not speak to the state at drafting.

What can be said, and its limits:

- **[verified]** at the 19 July revision, the working tree at commit `71fa329` remains clean with
  respect to *tracked* files — every entry is `??` untracked, and no entry is `M`. Command, run from
  the repository root, output quoted as produced:

  ```
  $ git status --porcelain
  ?? docs/delivery/ADR-TEMPLATE.md
  ?? docs/delivery/CAPABILITY-CLAIMS.md
  ?? docs/delivery/CORRECTIVE-BACKLOG.md
  ?? docs/delivery/PHASE-0-REMEDIATION-PLAN.md
  ?? docs/delivery/PROJECT-LOG.md
  ?? docs/delivery/PUBLICATION-EXIT-CRITERIA.md
  ?? docs/delivery/RAID-REGISTER.md
  ?? docs/design/
  ?? docs/safety/
  ?? docs/world-model/
  ```

  Nothing under `scaffold/` appears, tracked-modified or untracked.
- **[unverified]** that nothing under `scaffold/` was touched at any point during drafting. The
  clean tracked tree is consistent with that but does not establish it for the drafting session as
  it stood, and the standing constraint against modifying `scaffold/` is a rule the drafter followed,
  not an observation this record can now evidence.

Recorded this way deliberately: this is the single most checkable claim in the document and it was
the one left unevidenced.

**Revision note — 19 July 2026, after adversarial review.** The following claims in the 18 July draft
outran their evidence and were corrected in place. Each is listed so a reader can see what the draft
originally said:

| Where | What the draft claimed | What it now says |
|---|---|---|
| Header, and this entry | Drafting date graded `exact` | `document-stated`; revision date `exact` per system clock |
| Preamble | "four governance documents" carry the date, "firm" | The four are named; only the git timestamp is called firm |
| §1.4 and header | Policy "mirrors" `HANDOFF.md` § Standing constraints (`:138`) | Source quoted verbatim; the widening flagged as a drafting choice |
| Entry 1 | Audit's "not publishable" given as one limb | Both limbs given; the second is B5 and does not clear by text |
| Entry 1 | Count reconciliation marked `[verified]` | Arithmetic `[verified]`; reconciliation `[inference]` |
| Entry 2 | Closure cited to `A3:251-257` | Closure cited to `A3:3`; `:251-257` cited as the recommendation |
| Entry 2 | Plain layer opened with four bracketed citation blocks | Disclaimer hoisted once; anchors carried in Evidence |
| Entry 3 | "Licence decision as settled" | "as recorded", with `[unverified]` |
| Entry 3 | "No `COPYRIGHT.md` exists", evidenced tracked-only | Tree-wide `find` added alongside `git ls-files` |
| Entry 4 | "The default branch is `main`" | Local branch and cached ref distinguished from the server's |
| Entry 4 | "written when there was no `.git` directory" | Attributed to the audit and marked `[unverified]` |
| Entry 5 | "the honest current state of the code" | Quoted as a section heading, with accuracy not vouched for |
| Entry 5 | Phase B "had not been started" | Marked `[unverified]`, resting on `HANDOFF.md:34` |
| Entry 6 | "and is not on the remote" | `[unverified]`; no fetch, no network call |
| Entry 6 | Forward reference "a reading the file's appearance bears out" | `[inference]`; later creation is not evidence of intent |
| Entry 7 | "No other file was modified" | `[unverified]`, with the limits stated and `git status` quoted |

No finding was accepted merely because it was raised; the reviewers' claims were re-checked against
the tree before each change.

---

### 19 July 2026 — CORRECTION: blocker B5 / audit decision 8.6 was settled on 18 July 2026

**Type:** correction
**Status:** drafted, pending owner review
**Date confidence:** **exact** for this entry's own date (system clock at writing). **Document-stated**
for the decision date of 18 July 2026 — the founder decision was issued directly and, at the time of
writing, exists as no file in the tree, so it is cited by date rather than by `path:line`. Replace
that citation once a source record exists.

**Supersedes**, in each case only as to B5's clearance route:

- the A3 entry's closing statement, "B5, the dual-use influence-targeting schema, clears only by
  owner decision" (entry *18 July 2026 — A3 targeted re-verification completed*);
- entry 1's summary line "The second limb is publication blocker B5 and audit decision 8.6", **only**
  in so far as it implies 8.6 is outstanding as a judgement — its substantive point, that this limb
  does not clear by correcting text, is unaffected and in fact strengthened;
- the preamble to *Open questions arising from this log*, which counts 8.6 among the audit's
  unsettled §8 items;
- that section's closing note, "it requires an owner decision".

Sites are named by section rather than by line number because this entry's own insertion moved the
later ones. **Per §1.7 none of the four is edited**; they stand as written, and this entry states
what is no longer true. The two in the open-questions section — which is a live register, not a
dated entry — carry an added pointer block, on the reading that §1.7 governs entries. That reading is
the drafter's, not the policy's, and open question 5 below is exactly the question of whether such an
annotation is permitted. **The two inside dated entries carry no annotation at all.**

**Plain English: what happened and why it matters.** The owner decision that publication blocker B5
was waiting on has been taken. **B5 did not clear.** That is the whole point of this entry, and it is
the opposite of what a reader would expect a settled decision to mean.

The founder settled the dual-use position for the public MVP and named **eight controls**: influence
mechanics only in explicitly fictional worlds; a scenario loader that requires `world_mode: fictional`
and **fails closed** without it; real-world scenario import disabled; real persons, organisations and
political populations barred from being influence targets; protected characteristics barred as
optimisation criteria for persuasion or manipulation; fictional **aggregate** narrative diffusion,
exposure, adoption and counter-messaging still permitted; API and UI disclosing that the active world
is fictional; and, governing the other seven, **disclosure and any future acceptable-use language are
supplementary — technical enforcement is mandatory**.

Because of that eighth control, B5 can no longer be closed by a signature or by a policy statement.
It closes when the eight controls are **implemented and verified**. **None of the eight exists in
code**, and no Phase 0 item currently owns them. So settling B5 **enlarged** the publication gate.
The blocker that looked cheapest is now the most expensive, and it is the only one of the five that
cannot be closed by writing.

The same decision states the identity boundary the specification work must sit inside: identity may
affect lived experience, relationships, discrimination, institutional access, media exposure and
cultural interpretation, but must never act as an inherent **competence, morality, loyalty, violence
or manipulability** coefficient. That list is wider than the source record's "competence, morality or
intelligence" — it adds loyalty, violence and manipulability.

**This entry records the decision. It does not approve, extend or interpret it, and no agent may.**

**Evidence:**
- The decision itself, recorded in the founder's own terms: `docs/delivery/RAID-REGISTER.md` DEC6.
- The eight controls as publication criteria B5-1 to B5-8, each with a verifiable test form and its
  status in the code today: `docs/delivery/PUBLICATION-EXIT-CRITERIA.md` C6.
- One backlog entry per control, each with an evidence requirement: `docs/delivery/CORRECTIVE-BACKLOG.md`
  CB-40 to CB-47.
- The rewritten Phase 0 item: `docs/delivery/PHASE-0-REMEDIATION-PLAN.md` §P0.8.
- The superseded framing, preserved in place: `docs/delivery/A3-VERIFICATION-RESULTS.md:245`, `:247`,
  with an amendment appended at the end of that file.
- **[unverified] by this log.** No code was executed in writing this entry. "None of the eight exists
  in code" is carried from the four records above, each of which cites `file:line` for the absence —
  principally that `world_mode` appears in no schema, model or scenario file. This entry does not
  independently confirm it.

**Open questions for the owner:**
1. **Does implementing the eight controls fall inside or outside the standing "documents only, no
   feature implementation" constraint?** Seven of the eight require code. The founder instruction that
   settled B5 states that it authorises no feature implementation, so the controls are specified and
   unauthorised at the same time. Recorded elsewhere as RAID OQ9 and PHASE-0 OQ-13; repeated here
   because a reader of this log alone would not otherwise see it.
2. **Which Phase 0 item owns them?** P0.8 names them; nothing schedules them.

---

## Open questions arising from this log

**This is not the project's open-decision register.** These are only the questions raised by *this
document*. `CURRENT-STATE-AUDIT.md` §8 (`:397-413`) carries seven items requiring a human decision,
of which four remain open and are **not** addressed anywhere in this log: 8.3 (whether Mesa remains
the ABM substrate, `:405`), 8.5 (whether to adopt uv and `pyproject.toml`, `:409`), 8.6 (dual-use and
responsible-use policy for the influence-operations model, `:411` — the same question as publication
blocker B5), and 8.7 (whether `PLAN.pdf` remains the canonical plan format, `:413`). A reader must
not take the table below as the full set of outstanding decisions.

> ⚠ **Superseded in part — see the correction entry of 19 July 2026 above.** **8.6 is settled**
> (founder decision, 18 July 2026), so **three** of the seven remain open, not four. Settling it did
> **not** clear publication blocker B5: B5 now clears only when the decision's eight controls are
> **implemented and verified**, and none is built. The paragraph is left unedited under §1.7; this
> pointer is added so that a reader does not act on the count.

Collected for the owner. None of these may be resolved by an AI agent.

| # | Question | Where it arises |
|---|---|---|
| 1 | Which audit figures are correct — 124 agents / 128 candidates (HANDOFF) or 124 candidates (audit)? Both cannot be right. | Entry 1 |
| 2 | Is "nine-dimension" the correct description of the audit? The audit does not enumerate nine dimensions. | Entry 1 |
| 3 | Was `NOTICE.md:11` ("publicly visible") meant as present fact or post-publication position? It contradicts `HANDOFF.md:13`. | Entry 3 |
| 4 | Should `docs/world-model/` be committed? | Entry 6 |
| 5 | Should any in-place edit exception to the append-only rule exist — status-line amendment, typographical fixes, or neither? | §1.7 |

On publication blocker B5, the dual-use influence-targeting schema: it requires an owner decision and
is the only one of the five that does not clear by correcting text
(`docs/delivery/A3-VERIFICATION-RESULTS.md:245-247`, `HANDOFF.md` § Publication exit criteria (`:104-105`)). It is the same question as
audit decision 8.6 above. It is recorded here for visibility, not resolved.

> ⚠ **Superseded — see the correction entry of 19 July 2026 above.** The decision was taken on
> 18 July 2026. **"It requires an owner decision" is no longer true; "it does not clear by correcting
> text" still is, and is now more true rather than less.** B5 clears only when the decision's eight
> controls are **implemented and verified**, and none of them exists in code. Both citations in the
> sentence above point at superseded text: `HANDOFF.md` § Publication exit criteria (`:104-105`) has since been corrected in place, and
> `A3-VERIFICATION-RESULTS.md:245-247` is corrected by an amendment appended to the end of that file.
> The paragraph is left unedited under §1.7; this pointer is added so that a reader does not act on
> it.

---

## What this log deliberately does not claim

Stated explicitly, because the project's failure mode is claiming more than is known:

- It does not claim the codebase is execution-ready, replay-capable, or fully deterministic.
- It does not claim any audit finding is closed, re-graded, or left open. It records only that a
  fact those findings rest on — the absence of `.git` — is no longer true. For finding 37 that fact
  *is* the finding rather than merely support for it; deciding what follows is the owner's call, and
  this log deliberately adopts neither the "wholly stale" nor the "partly stale" framing.
- It does not claim the repository is private. That rests on `HANDOFF.md:13` and was not observed.
- It does not claim commit `71fa329` has been pushed to the remote server, and makes no claim about
  the remote's contents at all — no fetch was performed and no network call was made. In particular
  it does not claim that any untracked file is absent from the remote, and it does not claim to know
  the remote's default branch.
- It does not claim its own drafting date is independently established. Only the git author timestamp
  of the commit, and the system clock at the 19 July revision, are firm dates in this document.
- It does not restate any runtime result as independently confirmed. No code was run in drafting
  this log. Every execution result is attributed inline, in the prose as well as in the evidence
  block, to the document that recorded it.
- It does not enumerate the project's open decisions. Four items from `CURRENT-STATE-AUDIT.md` §8
  are open and unaddressed here; see the open-questions section.
- Its point-in-time observations about untracked files and directory contents are labelled as such
  and were already overtaken by sibling Phase B records drafted in the same session. They are not
  standing properties of the tree.
