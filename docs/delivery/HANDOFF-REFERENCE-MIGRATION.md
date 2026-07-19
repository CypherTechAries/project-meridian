# HANDOFF.md reference migration — P0.4A sequence insert

**DRAFT — 19 July 2026.**
**Drafted by:** an AI agent. Under `HANDOFF.md` § Standing constraints (`:138`) an AI agent may draft
records but may not approve decisions. **This document approves nothing.** It records a mechanical
migration carried out under founder decision 2 of 19 July 2026 and the verification performed on it.
Nothing here alters the Phase 0 order, P0.4A's scope, or any open question.

---

## 1. Plain English

`HANDOFF.md` is the governing record of the founder-set Phase 0 order. Its canonical list ran
P0.4 → P0.5 and did not contain P0.4A, even though P0.4A was created by founder decision on
18 July 2026 and every other record in the repository — the remediation plan, the corrective
backlog, the RAID register, the publication exit criteria, ADR-010 and the world-model documents —
ran P0.4 → P0.4A → P0.5. Worse, several of those documents cited `HANDOFF.md` *by line number* as the
authority for the very list that omitted the item.

The founder ruled that this be fixed by coordinated correction rather than by appending a workaround.
In one pass:

1. P0.4A was inserted into the canonical sequence in its correct position, between P0.4 and P0.5.
2. Every citation elsewhere in the repository that pointed at a line which moved was re-pointed.
3. Every re-pointed citation was verified by reading the new target line and checking it says what
   the citing document claims about it.
4. Where practical, brittle bare line numbers were replaced with **stable section anchors**, so that
   the next insert into `HANDOFF.md` does not break them again.
5. Four documents asserted, as a statement of fact, that `HANDOFF.md` does not list P0.4A. Those
   statements are now false. They were **not** deleted. Each carries a dated amendment recording
   what is superseded and what still stands.

Nothing under `scaffold/` was modified. No commit was made. No decision was resolved.

## 2. What changed in HANDOFF.md

| | |
|---|---|
| Item inserted | `HANDOFF.md:76-83`, between P0.4 (`:75`) and P0.5 (`:84-86`) |
| Lines added in the sequence | 8 |
| Shift applied | every line formerly numbered **76 or higher** moved down by exactly **8** |
| Lines 1-75 | unchanged, byte for byte |
| Amendment record appended | `HANDOFF.md` § Amendment record (`:156` onward) |
| Historical notices preserved | yes — including the B5 supersession note, now at `:104-105`, carried forward verbatim |

The inserted wording is drawn from `docs/adr/ADR-010-deterministic-randomness-architecture.md` and
`docs/delivery/PHASE-0-REMEDIATION-PLAN.md` §P0.4A. It states the item, its lettering rationale, its
sequencing rule, and — explicitly — that **it is not implemented and no code exists for it**.

**New line map for the Phase 0 priority order:**

| Item | Old lines | New lines |
|---|---|---|
| P0.1 | 70-71 | 70-71 |
| P0.2 | 72-73 | 72-73 |
| P0.3 | 74 | 74 |
| P0.4 | 75 | 75 |
| **P0.4A** | — (absent) | **76-83** |
| P0.5 | 76-78 | 84-86 |
| P0.6 | 79-80 | 87-88 |
| P0.7 | 81 | 89 |
| P0.8 | 82 | 90 |

**New section map (use these anchors in preference to line numbers):**

| Section | New lines |
|---|---|
| § Repository status | 11-25 |
| § Where the work stopped | 26-40 |
| § Current state of the code, stated honestly | 41-67 |
| § Phase 0 priority order (founder-set) | 68-91 |
| § Publication exit criteria | 92-106 |
| § Backlog — captured, deliberately not started | 107-132 |
| § Standing constraints | 133-141 |
| § Reproducing the evidence | 142-155 |
| § Amendment record | 156-188 |

## 3. Counts

| | Count |
|---|---|
| `HANDOFF.md` citations found across the repository (excluding `scaffold/`) | **349** |
| Of those, pointing at a line that moved (line ≥ 76) | **200** |
| Updated | **200** |
| Verified against the new target line | **349** (all citations re-checked, not only the updated ones) |
| Verification failures after migration | **0** |
| Converted to a stable section anchor | **198** |
| Left as a bare line number by deliberate choice | **2** |
| Unresolved | **0** |
| Citing files touched | **21** |
| Files under `scaffold/` modified | **0** |

The founder's estimate was roughly 77 citations, about 63 of them in the shifted region. The true
figures are higher — 349 and 200 — because three distinct citation forms exist in the tree, and the
initial estimate appears to have counted only the first:

| Form | Example | Count found |
|---|---|---|
| A — bare | `` `HANDOFF.md:130` `` | 267 |
| B — linked | ``[`../../HANDOFF.md`](../../HANDOFF.md):79-80`` | 79 |
| C — backtick-closed | `` `HANDOFF.md`:130 `` | 3 |

Form B is used almost exclusively by the world-model, design and safety documents. Form C occurs
three times and is the form most easily missed by a naive search.

## 4. Verification method

Two-layer, as required.

**Plain English.** Every citation in the tree was re-read after migration, its target line opened in
the corrected `HANDOFF.md`, and the text of that line compared against what the citing sentence
claims the source says.

**Technical evidence.** Reproduce with:

```
python scratch/verify.py        # the checker used; see the checks it applies below
```

The checker derives the section boundaries and the P0 item boundaries from the live `HANDOFF.md`
rather than from a hard-coded table, then asserts, for every citation:

1. the target line number is within the file;
2. the target line is not blank;
3. if the citation carries a section anchor, the cited line falls inside that section's live range;
4. if the citation carries a P0 item anchor, the cited line falls inside that item's live range.

Result: **349 checked, 349 passed, 0 failed.** Checks 3 and 4 are the substantive ones — they are why
a silently mis-anchored citation cannot survive this migration. A citation claiming
`§ Phase 0 priority order, P0.5` that landed on P0.4A's text would fail check 4.

Beyond the automated checks, every distinct `(line range, target text)` pair was read by hand. The
highest-frequency targets, which carry most of the migration's risk, verified as follows:

| New ref | Occurrences | Target text | Verdict |
|---|---|---|---|
| `:139-140` | 27 | "Human approval required for architecture, dependencies, licence, migrations, auth, security controls, public releases…" | correct |
| `:138` | 22 | "AI agents may draft records but may not approve their own decisions." | correct |
| `:135` | 18 | "Do not describe the codebase as execution-ready, replay-capable or fully deterministic." | correct |
| `:87-88` | 17 | P0.6 — "Repair event, snapshot and replay foundations…" | correct |
| `:84-86` | 17 | P0.5 — "Design explicit cross-tier causal channels…" | correct |
| `:104-105` | 9 | the B5 supersession note | correct |
| `:96-102` | 7 | the seven publication exit criteria | correct |
| `:90` | 7 | P0.8 — "Review the influence-operations targeting schema before publication." | correct |
| `:89` | 8 | P0.7 — "Define simulation time and horizon **before** touching saturation." | correct |
| `:137` | 4 | "Do not launch another unrestricted multi-agent audit. The broad audit is closed." | correct |

## 5. Citations deliberately NOT converted to an anchor

Two, both left as bare updated line numbers with reason:

| File:line | Ref | Why not anchored |
|---|---|---|
| `docs/world-model/ORGANISATION-MODEL.md`:994 | `HANDOFF.md:87-88` | Inside a fenced code block. Injecting anchor prose would corrupt the block. |
| `docs/world-model/ORGANISATION-MODEL.md`:1974 | `HANDOFF.md:87-88` | Inside an ASCII diagram where character alignment is load-bearing. |

Both were verified: `:87-88` is P0.6, "replay makes zero model/network calls", which is exactly what
both passages assert.

## 6. Citations that required judgement, not mechanical rewriting

These were handled by hand because a mechanical shift would have produced a true line number
attached to a false statement.

### 6.1 Documents asserting that HANDOFF.md omits P0.4A — now false

Four. In each case the original sentence was **preserved** and a dated amendment appended beneath it.
Per the standing constraint against rewriting history, none was silently corrected.

| File:line | What it asserted | Treatment |
|---|---|---|
| `docs/delivery/CORRECTIVE-BACKLOG.md`:10 | "`HANDOFF.md:70-82` … does not yet list P0.4A, so no citation into `HANDOFF.md` should be read as supporting the new workstream's existence" | Amended. `HANDOFF.md` is now a citable authority for the item's **existence and position**; the 18 July decision remains the only source for its **scope** and ten exit criteria. |
| `docs/delivery/CAPABILITY-CLAIMS.md`:383 | "…therefore does not list **P0.4A** … Cite `PHASE-0-REMEDIATION-PLAN.md` §P0.4A for that ownership, not `HANDOFF.md`" | Amended. Same split: `HANDOFF.md` for existence and position, the plan and ADR-010 for detail. |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:40 | "`HANDOFF.md:68-82` does not yet list it; where the two disagree on the item list, this amendment is the later record" | Amended. The two records no longer disagree. |
| `docs/delivery/PROJECT-LOG.md`:680 | "still lists P0.1 to P0.8 without P0.4A and predates the decision" | Amended **partially**. The item-list half is superseded. **The sourcing limitation is expressly not closed:** `HANDOFF.md` cites the 18 July decision by date, so there is still no founder source record in the tree for that decision's scope or exit criteria. |

### 6.2 Continuation and multi-reference forms

Bare `` `:NN` `` continuations that inherit their file from an earlier reference on the same line are
invisible to a search for `HANDOFF.md:NN`. Seven lines contained such references into the shifted
region and were corrected by hand:

| File:line | Old | New |
|---|---|---|
| `docs/delivery/RAID-REGISTER.md`:755 | `:84-94` | § Publication exit criteria (`:92-102`) |
| `docs/delivery/RAID-REGISTER.md`:772 | `:76-78`, `:79-80` | P0.5 (`:84-86`), P0.6 (`:87-88`) |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:670 | `:79-80`, `:90`, `:120`, `:122` | `:87-88`, `:98`, `:128`, `:130` |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:1066 | `:94`, `:113` | `:102`, `:121` |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:1223 | `:96-97` | § Publication exit criteria (`:104-105`) |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1788 | `:96-97` | § Publication exit criteria (`:104-105`) |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:2363 | `:127` | § Standing constraints (`:135`) |
| `docs/world-model/ENTITY-ONTOLOGY.md`:1363 | `:68-82`, `:99-112`, `:127-132` | `:68-90`, § Backlog (`:107-120`), § Standing constraints (`:135-140`) |
| `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`:32 | `` `HANDOFF.md`:82 ``, `:96-97` | P0.8 (`:90`), § Publication exit criteria (`:104-105`) |
| `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`:1347 | `:82`, `:96-97` | P0.8 (`:90`), § Publication exit criteria (`:104-105`) |

`docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:1066 deserves note: the file name sat in one table cell
and the line numbers in another. No regex over `HANDOFF.md:NN` would have found it. It was caught by
a second sweep for bare `:NN` on any line mentioning `HANDOFF.md`.

### 6.3 Ranges whose meaning drifted because the insert landed inside them

| File:line | Ref | Issue | Treatment |
|---|---|---|---|
| `docs/delivery/RAID-REGISTER.md`:746 | old `:75-78`, "the text of P0.4 and P0.5" | The shifted range `:75-86` now also spans P0.4A, so the description was no longer accurate | Split into two precise anchors: P0.4 (`:75`) and P0.5 (`:84-86`) |
| `docs/delivery/RAID-REGISTER.md`:772 | P0.4A "by the founder decision of 18 July 2026" | P0.4A is now citable in `HANDOFF.md` | Re-anchored to `:76-83` with a dated amendment noting why the row originally cited a date rather than a line |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:562 | old `:75-81` → `:75-89`, "gives the text of P0.4 to P0.7" | The range now also contains P0.4A | **Left as-is.** The statement remains true — the range does give the text of P0.4 to P0.7 — and the paragraph immediately following it discusses P0.4A explicitly, so no reader is misled. Flagged here rather than edited. |

## 7. Unresolved citations

**None.** Every citation found was resolved, updated where it needed updating, and verified.

Two limitations are recorded rather than hidden:

1. **`scaffold/` was excluded by instruction.** `scaffold/CLAUDE.md:140-141` cites `../HANDOFF.md:21`
   and `:23`. Both are below line 76, both are therefore still correct, and neither was touched.
   Verified, not migrated — no migration was needed. Had they pointed into the shifted region they
   would have been reported here as unresolved, because this pass had no authority to edit them.
2. **Only markdown was swept.** Non-markdown files were not searched for `HANDOFF.md:NN` citations.
   A `grep` over the tree for the pattern outside `*.md` would close this; it was not run.

## 8. Open questions for the owner

Drafted, not resolved. An AI agent may not answer these.

1. **Does the inserted P0.4A wording accurately state the founder's intent?** The text was
   synthesised from ADR-010 and the remediation plan, both of which are themselves drafter-written
   records of a decision issued verbally. `HANDOFF.md` is a governing authority and its wording of a
   founder decision should be confirmed by the founder, not inherited from a downstream document.
2. **Should the anchor convention become a standing requirement?** This pass converted 198 citations
   to `§ Section` form but did not convert the 149 citations below line 76, which remain bare line
   numbers and will break on the next insert above them. Converting them is a mechanical follow-up
   this pass did not have authority to perform, since it would touch citations the founder decision
   did not reach.
3. **Should `HANDOFF.md` carry stable anchor identifiers** (for example `[P0.4A]` tags) so that
   citations need no line numbers at all? That is a change to the governing document's format and is
   the owner's to decide.

---

## Appendix A — full migration table

200 rows: every citation whose target line moved. Columns: citing file and line, the reference before
migration, the reference after, what the new target line actually says, and whether the citation was
converted to a stable anchor.

| Citing file:line | Old reference | New reference | Verification — what the new target says | Stable anchor |
|---|---|---|---|---|
| `docs/adr/ADR-010-deterministic-randomness-architecture.md`:195 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/adr/ADR-010-deterministic-randomness-architecture.md`:506 | `HANDOFF.md:129` | `HANDOFF.md` § Standing constraints (`:137`) | Target reads: "- Do not launch another unrestricted multi-agent audit. The broad audit is closed." — matches the citing claim | yes |
| `docs/adr/ADR-010-deterministic-randomness-architecture.md`:665 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/adr/ADR-010-deterministic-randomness-architecture.md`:667 | `HANDOFF.md:129` | `HANDOFF.md` § Standing constraints (`:137`) | Target reads: "- Do not launch another unrestricted multi-agent audit. The broad audit is closed." — matches the citing claim | yes |
| `docs/adr/ADR-010-deterministic-randomness-architecture.md`:679 | `HANDOFF.md:129` | `HANDOFF.md` § Standing constraints (`:137`) | Target reads: "- Do not launch another unrestricted multi-agent audit. The broad audit is closed." — matches the citing claim | yes |
| `docs/adr/ADR-010-deterministic-randomness-architecture.md`:730 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:6 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:62 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:124 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:130 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:145 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:182 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:187 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:340 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:478 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:494 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:574 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:579 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:600 | `HANDOFF.md:130-132` | `HANDOFF.md` § Standing constraints (`:138-140`) | Target reads: "- AI agents may draft records but may not approve their own decisions. / - Human approval required for architecture, dep" — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:602 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:608 | `HANDOFF.md:125-132` | `HANDOFF.md` § Standing constraints (`:133-140`) | Target reads: "## Standing constraints / - Do not describe the codebase as execution-ready, replay-capable or fully deterministic. / - " — matches the citing claim | yes |
| `docs/delivery/ADR-TEMPLATE.md`:638 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:43 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:103 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:103 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:103 | `HANDOFF.md:120` | `HANDOFF.md` § Backlog (`:128`) | Target reads: "- **Replay requirement (expands `ExternalAgentInput`, do not implement in Phase 0):** every text turn," — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:104 | `HANDOFF.md:104-106` | `HANDOFF.md` § Backlog (`:112-114`) | Target reads: "exploits, fears and responds to a crisis, not only how the command room manages it. Crises must / propagate through popu" — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:108 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:108 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:147 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:215 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:229 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:232 | `HANDOFF.md:104-106` | `HANDOFF.md` § Backlog (`:112-114`) | Target reads: "exploits, fears and responds to a crisis, not only how the command room manages it. Crises must / propagate through popu" — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:280 | `HANDOFF.md:104-106` | `HANDOFF.md` § Backlog (`:112-114`) | Target reads: "exploits, fears and responds to a crisis, not only how the command room manages it. Crises must / propagate through popu" — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:299 | `HANDOFF.md:144` | `HANDOFF.md` § Reproducing the evidence (`:152`) | Target reads: "\| `probe.py` \| determinism regression probes; changing only the LLM's action choice moves macro numbers 0.59 → 0.39 \|" — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:372 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:372 | `HANDOFF.md:120-123` | `HANDOFF.md` § Backlog (`:128-131`) | Target reads: "- **Replay requirement (expands `ExternalAgentInput`, do not implement in Phase 0):** every text turn, / voice transcrip" — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:382 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:383 | `HANDOFF.md:68-82` | `HANDOFF.md` § Phase 0 priority order (`:68-90`) | Target reads: "## Phase 0 priority order (founder-set) / - **P0.1** Correct live false claims (CI, legality validation, persistence, re" — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:456 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:489 | `HANDOFF.md:141` | `HANDOFF.md` § Reproducing the evidence (`:149`) | Target reads: "\| `verify_criticals.py` \| 14/18 macro scalars frozen; readiness pegs at tick 61; tiers move in opposite directions \|" — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:522 | `HANDOFF.md:96-97` | `HANDOFF.md` § Publication exit criteria (`:104-105`) | Target reads: "Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. " — matches the citing claim | yes |
| `docs/delivery/CAPABILITY-CLAIMS.md`:523 | `HANDOFF.md:96-97` | `HANDOFF.md` § Publication exit criteria (`:104-105`) | Target reads: "Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. " — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:10 | `HANDOFF.md:70-82` | `HANDOFF.md` § Phase 0 priority order (`:70-90`) | Target reads: "- **P0.1** Correct live false claims (CI, legality validation, persistence, replay, archetype / extensibility, execution" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:33 | `HANDOFF.md:70-82` | `HANDOFF.md` § Phase 0 priority order (`:70-90`) | Target reads: "- **P0.1** Correct live false claims (CI, legality validation, persistence, replay, archetype / extensibility, execution" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:77 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:99 | `HANDOFF.md:90-91` | `HANDOFF.md` § Publication exit criteria (`:98-99`) | Target reads: "- [ ] False determinism and replay claims corrected / - [ ] Existing tests and their actual scope accurately described" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:141 | `HANDOFF.md:70-82` | `HANDOFF.md` § Phase 0 priority order (`:70-90`) | Target reads: "- **P0.1** Correct live false claims (CI, legality validation, persistence, replay, archetype / extensibility, execution" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:141 | `HANDOFF.md:70-82` | `HANDOFF.md` § Phase 0 priority order (`:70-90`) | Target reads: "- **P0.1** Correct live false claims (CI, legality validation, persistence, replay, archetype / extensibility, execution" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:774 | `HANDOFF.md:76` | `HANDOFF.md` § Phase 0 priority order (`:84`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population`" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:778 | `HANDOFF.md:76` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population`" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:919 | `HANDOFF.md:84-94` | `HANDOFF.md` § Publication exit criteria (`:92-102`) | Target reads: "## Publication exit criteria / Do not create a public repository until all of these pass: / - [ ] Documented clean insta" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1085 | `HANDOFF.md:92` | `HANDOFF.md` § Publication exit criteria (`:100`) | Target reads: "- [ ] Unused installation-blocking dependencies removed or made optional" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1103 | `HANDOFF.md:92` | `HANDOFF.md` § Publication exit criteria (`:100`) | Target reads: "- [ ] Unused installation-blocking dependencies removed or made optional" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1191 | `HANDOFF.md:101` | `HANDOFF.md` § Backlog (`:109`) | Target reads: "Do not begin these until the foundation is honest and testable:" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1230 | `HANDOFF.md:70-82` | `HANDOFF.md` § Phase 0 priority order (`:70-90`) | Target reads: "- **P0.1** Correct live false claims (CI, legality validation, persistence, replay, archetype / extensibility, execution" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1602 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1603 | `HANDOFF.md:76` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population`" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1621 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1644 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1654 | `HANDOFF.md:81` | `HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`) | Target reads: "- **P0.7** Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion." — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1656 | `HANDOFF.md:81` | `HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`) | Target reads: "- **P0.7** Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion." — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1689 | `HANDOFF.md:96-97` | `HANDOFF.md` § Publication exit criteria (`:104-105`) | Target reads: "Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. " — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:1793 | `HANDOFF.md:82` | `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) | Target reads: "- **P0.8** Review the influence-operations targeting schema before publication." — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:2205 | `HANDOFF.md:70-82` | `HANDOFF.md` § Phase 0 priority order (`:70-90`) | Target reads: "- **P0.1** Correct live false claims (CI, legality validation, persistence, replay, archetype / extensibility, execution" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:2323 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:2358 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:2368 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/delivery/CORRECTIVE-BACKLOG.md`:2427 | `HANDOFF.md:70-82` | `HANDOFF.md` § Phase 0 priority order (`:70-90`) | Target reads: "- **P0.1** Correct live false claims (CI, legality validation, persistence, replay, archetype / extensibility, execution" — matches the citing claim | yes |
| `docs/delivery/P0-1-CHANGE-REPORT.md`:42 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/P0-1-CHANGE-REPORT.md`:64 | `HANDOFF.md:90` | `HANDOFF.md` § Publication exit criteria (`:98`) | Target reads: "- [ ] False determinism and replay claims corrected" — matches the citing claim | yes |
| `docs/delivery/P0-1-CHANGE-REPORT.md`:116 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:31 | `HANDOFF.md:68-82` | `HANDOFF.md` § Phase 0 priority order (`:68-90`) | Target reads: "## Phase 0 priority order (founder-set) / - **P0.1** Correct live false claims (CI, legality validation, persistence, re" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:40 | `HANDOFF.md:68-82` | `HANDOFF.md` § Phase 0 priority order (`:68-90`) | Target reads: "## Phase 0 priority order (founder-set) / - **P0.1** Correct live false claims (CI, legality validation, persistence, re" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:95 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:99 | `HANDOFF.md:125-132` | `HANDOFF.md` § Standing constraints (`:133-140`) | Target reads: "## Standing constraints / - Do not describe the codebase as execution-ready, replay-capable or fully deterministic. / - " — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:120 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:465 | `HANDOFF.md:131` | `HANDOFF.md` § Standing constraints (`:139`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:562 | `HANDOFF.md:75-81` | `HANDOFF.md` § Phase 0 priority order (`:75-89`) | Target reads: "- **P0.4** Define the authoritative-state contract across macro/meso/micro. / - **P0.4A** Establish a deterministic rand" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:566 | `HANDOFF.md:81` | `HANDOFF.md` § Phase 0 priority order (`:89`) | Target reads: "- **P0.7** Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion." — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:856 | `HANDOFF.md:128` | `HANDOFF.md` § Standing constraints (`:136`) | Target reads: "- Do not modify simulation behaviour merely to make an audit finding disappear." — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:857 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:868 | `HANDOFF.md:76-77` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-85`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:990 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:1087 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:1094 | `HANDOFF.md:81` | `HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`) | Target reads: "- **P0.7** Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion." — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:1166 | `HANDOFF.md:82` | `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) | Target reads: "- **P0.8** Review the influence-operations targeting schema before publication." — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:1180 | `HANDOFF.md:96-97` | `HANDOFF.md` § Publication exit criteria (`:104-105`) | Target reads: "Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. " — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:1227 | `HANDOFF.md:82` | `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) | Target reads: "- **P0.8** Review the influence-operations targeting schema before publication." — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:1770 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`:1801 | `HANDOFF.md:84-94` | `HANDOFF.md` § Publication exit criteria (`:92-102`) | Target reads: "## Publication exit criteria / Do not create a public repository until all of these pass: / - [ ] Documented clean insta" — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:8 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:90 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:94 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:367 | `HANDOFF.md:134-144` | `HANDOFF.md` § Reproducing the evidence (`:142-152`) | Target reads: "## Reproducing the evidence / Scripts in [`docs/delivery/evidence/`](docs/delivery/evidence/). From `scaffold/backend`, " — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:560 | `HANDOFF.md:68-82` | `HANDOFF.md` § Phase 0 priority order (`:68-90`) | Target reads: "## Phase 0 priority order (founder-set) / - **P0.1** Correct live false claims (CI, legality validation, persistence, re" — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:561 | `HANDOFF.md:84-94` | `HANDOFF.md` § Publication exit criteria (`:92-102`) | Target reads: "## Publication exit criteria / Do not create a public repository until all of these pass: / - [ ] Documented clean insta" — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:562 | `HANDOFF.md:125-132` | `HANDOFF.md` § Standing constraints (`:133-140`) | Target reads: "## Standing constraints / - Do not describe the codebase as execution-ready, replay-capable or fully deterministic. / - " — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:671 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:680 | `HANDOFF.md:68-82` | `HANDOFF.md` § Phase 0 priority order (`:68-90`) | Target reads: "## Phase 0 priority order (founder-set) / - **P0.1** Correct live false claims (CI, legality validation, persistence, re" — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:774 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:900 | `HANDOFF.md:96-97` | `HANDOFF.md` § Publication exit criteria (`:104-105`) | Target reads: "Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. " — matches the citing claim | yes |
| `docs/delivery/PROJECT-LOG.md`:907 | `HANDOFF.md:96-97` | `HANDOFF.md` § Publication exit criteria (`:104-105`) | Target reads: "Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. " — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:85 | `HANDOFF.md:88-94` | `HANDOFF.md` § Publication exit criteria (`:96-102`) | Target reads: "- [ ] Documented clean installation works on a supported environment / - [ ] README accurately states what is and is not" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:237 | `HANDOFF.md:88` | `HANDOFF.md` § Publication exit criteria (`:96`) | Target reads: "- [ ] Documented clean installation works on a supported environment" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:660 | `HANDOFF.md:127` | `HANDOFF.md` § Standing constraints (`:135`) | Target reads: "- Do not describe the codebase as execution-ready, replay-capable or fully deterministic." — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:780 | `HANDOFF.md:143` | `HANDOFF.md` § Reproducing the evidence (`:151`) | Target reads: "\| `a3_rng_isolation.py` \| meso→macro coupling is shared-RNG contamination, not causality \|" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:793 | `HANDOFF.md:88-94` | `HANDOFF.md` § Publication exit criteria (`:96-102`) | Target reads: "- [ ] Documented clean installation works on a supported environment / - [ ] README accurately states what is and is not" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:968 | `HANDOFF.md:93` | `HANDOFF.md` § Publication exit criteria (`:101`) | Target reads: "- [ ] Current-state audit and known-limitations document committed" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:1118 | `HANDOFF.md:88-94` | `HANDOFF.md` § Publication exit criteria (`:96-102`) | Target reads: "- [ ] Documented clean installation works on a supported environment / - [ ] README accurately states what is and is not" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:1173 | `HANDOFF.md:88-94` | `HANDOFF.md` § Publication exit criteria (`:96-102`) | Target reads: "- [ ] Documented clean installation works on a supported environment / - [ ] README accurately states what is and is not" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:1188 | `HANDOFF.md:88-94` | `HANDOFF.md` § Publication exit criteria (`:96-102`) | Target reads: "- [ ] Documented clean installation works on a supported environment / - [ ] README accurately states what is and is not" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:1376 | `HANDOFF.md:88` | `HANDOFF.md` § Publication exit criteria (`:96`) | Target reads: "- [ ] Documented clean installation works on a supported environment" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:1380 | `HANDOFF.md:93` | `HANDOFF.md` § Publication exit criteria (`:101`) | Target reads: "- [ ] Current-state audit and known-limitations document committed" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:1388 | `HANDOFF.md:88-94` | `HANDOFF.md` § Publication exit criteria (`:96-102`) | Target reads: "- [ ] Documented clean installation works on a supported environment / - [ ] README accurately states what is and is not" — matches the citing claim | yes |
| `docs/delivery/PUBLICATION-EXIT-CRITERIA.md`:1401 | `HANDOFF.md:88-94` | `HANDOFF.md` § Publication exit criteria (`:96-102`) | Target reads: "- [ ] Documented clean installation works on a supported environment / - [ ] README accurately states what is and is not" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:238 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:494 | `HANDOFF.md:129` | `HANDOFF.md` § Standing constraints (`:137`) | Target reads: "- Do not launch another unrestricted multi-agent audit. The broad audit is closed." — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:563 | `HANDOFF.md:88` | `HANDOFF.md` § Publication exit criteria (`:96`) | Target reads: "- [ ] Documented clean installation works on a supported environment" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:724 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:734 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:740 | `HANDOFF.md:96-97` | `HANDOFF.md` § Publication exit criteria (`:104-105`) | Target reads: "Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. " — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:749 | `HANDOFF.md:81` | `HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`) | Target reads: "- **P0.7** Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion." — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:754 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:755 | `HANDOFF.md:84-94` | `HANDOFF.md` § Publication exit criteria (`:92-102`) | Target reads: "## Publication exit criteria / Do not create a public repository until all of these pass: / - [ ] Documented clean insta" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:825 | `HANDOFF.md:84-94` | `HANDOFF.md` § Publication exit criteria (`:92-102`) | Target reads: "## Publication exit criteria / Do not create a public repository until all of these pass: / - [ ] Documented clean insta" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:866 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:1015 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:1027 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/delivery/RAID-REGISTER.md`:1113 | `HANDOFF.md:96-97` | `HANDOFF.md` § Publication exit criteria (`:104-105`) | Target reads: "Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. " — matches the citing claim | yes |
| `docs/design/ENTITY-PROFILE-EXPERIENCE.md`:43 | `HANDOFF.md:99-112` | `HANDOFF.md` § Backlog (`:107-120`) | Target reads: "## Backlog — captured, deliberately not started / Do not begin these until the foundation is honest and testable: / - **" — matches the citing claim | yes |
| `docs/design/ENTITY-PROFILE-EXPERIENCE.md`:49 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/design/ENTITY-PROFILE-EXPERIENCE.md`:201 | `HANDOFF.md:113-115` | `HANDOFF.md` § Backlog (`:121-123`) | Target reads: "- **Visual system:** `VISUAL-CONSTITUTION`, `DESIGN-TOKENS`, `MOTION-SYSTEM`, `INTERACTION-PATTERNS`, / `SCREEN-SPECIFIC" — matches the citing claim | yes |
| `docs/design/ENTITY-PROFILE-EXPERIENCE.md`:616 | `HANDOFF.md:113-115` | `HANDOFF.md` § Backlog (`:121-123`) | Target reads: "- **Visual system:** `VISUAL-CONSTITUTION`, `DESIGN-TOKENS`, `MOTION-SYSTEM`, `INTERACTION-PATTERNS`, / `SCREEN-SPECIFIC" — matches the citing claim | yes |
| `docs/design/ENTITY-PROFILE-EXPERIENCE.md`:682 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/design/ENTITY-PROFILE-EXPERIENCE.md`:991 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/design/ENTITY-PROFILE-EXPERIENCE.md`:1075 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/design/ENTITY-PROFILE-EXPERIENCE.md`:1093 | `HANDOFF.md:113-115` | `HANDOFF.md` § Backlog (`:121-123`) | Target reads: "- **Visual system:** `VISUAL-CONSTITUTION`, `DESIGN-TOKENS`, `MOTION-SYSTEM`, `INTERACTION-PATTERNS`, / `SCREEN-SPECIFIC" — matches the citing claim | yes |
| `docs/design/UI-RESEARCH-HANDOFF.md`:12 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md`:7 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`:32 | `HANDOFF.md:82` | `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) | Target reads: "- **P0.8** Review the influence-operations targeting schema before publication." — matches the citing claim | yes |
| `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`:44 | `HANDOFF.md:99-112` | `HANDOFF.md` § Backlog (`:107-120`) | Target reads: "## Backlog — captured, deliberately not started / Do not begin these until the foundation is honest and testable: / - **" — matches the citing claim | yes |
| `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`:53 | `HANDOFF.md:130-132` | `HANDOFF.md` § Standing constraints (`:138-140`) | Target reads: "- AI agents may draft records but may not approve their own decisions. / - Human approval required for architecture, dep" — matches the citing claim | yes |
| `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`:1033 | `HANDOFF.md:96-97` | `HANDOFF.md` § Publication exit criteria (`:104-105`) | Target reads: "Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. " — matches the citing claim | yes |
| `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`:1083 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`:1136 | `HANDOFF.md:130-132` | `HANDOFF.md` § Standing constraints (`:138-140`) | Target reads: "- AI agents may draft records but may not approve their own decisions. / - Human approval required for architecture, dep" — matches the citing claim | yes |
| `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`:1209 | `HANDOFF.md:130-132` | `HANDOFF.md` § Standing constraints (`:138-140`) | Target reads: "- AI agents may draft records but may not approve their own decisions. / - Human approval required for architecture, dep" — matches the citing claim | yes |
| `docs/world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`:435 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`:466 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`:513 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`:578 | `HANDOFF.md:82` | `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) | Target reads: "- **P0.8** Review the influence-operations targeting schema before publication." — matches the citing claim | yes |
| `docs/world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`:1497 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`:1509 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`:1569 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/ENTITY-ONTOLOGY.md`:26 | `HANDOFF.md:99-112` | `HANDOFF.md` § Backlog (`:107-120`) | Target reads: "## Backlog — captured, deliberately not started / Do not begin these until the foundation is honest and testable: / - **" — matches the citing claim | yes |
| `docs/world-model/ENTITY-ONTOLOGY.md`:31 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/world-model/ENTITY-ONTOLOGY.md`:127 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/world-model/ENTITY-ONTOLOGY.md`:528 | `HANDOFF.md:77` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:85`) | Target reads: "must affect aggregation. *(Note: this is arguably the highest-value item, since it is the product's" — matches the citing claim | yes |
| `docs/world-model/ENTITY-ONTOLOGY.md`:649 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/ENTITY-ONTOLOGY.md`:1146 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/world-model/ENTITY-ONTOLOGY.md`:1258 | `HANDOFF.md:130-132` | `HANDOFF.md` § Standing constraints (`:138-140`) | Target reads: "- AI agents may draft records but may not approve their own decisions. / - Human approval required for architecture, dep" — matches the citing claim | yes |
| `docs/world-model/OBSERVATION-AND-PERCEPTION-MODEL.md`:111 | `HANDOFF.md:79` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full" — matches the citing claim | yes |
| `docs/world-model/ORGANISATION-MODEL.md`:26 | `HANDOFF.md:99-112` | `HANDOFF.md` § Backlog (`:107-120`) | Target reads: "## Backlog — captured, deliberately not started / Do not begin these until the foundation is honest and testable: / - **" — matches the citing claim | yes |
| `docs/world-model/ORGANISATION-MODEL.md`:35 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/world-model/ORGANISATION-MODEL.md`:994 | `HANDOFF.md:79-80` | `HANDOFF.md:87-88` | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | no |
| `docs/world-model/ORGANISATION-MODEL.md`:1664 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/world-model/ORGANISATION-MODEL.md`:1875 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/ORGANISATION-MODEL.md`:1899 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/world-model/ORGANISATION-MODEL.md`:1974 | `HANDOFF.md:79-80` | `HANDOFF.md:87-88` | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | no |
| `docs/world-model/ORGANISATION-MODEL.md`:2018 | `HANDOFF.md:82` | `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) | Target reads: "- **P0.8** Review the influence-operations targeting schema before publication." — matches the citing claim | yes |
| `docs/world-model/ORGANISATION-MODEL.md`:2076 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/PERSON-MODEL.md`:32 | `HANDOFF.md:99-112` | `HANDOFF.md` § Backlog (`:107-120`) | Target reads: "## Backlog — captured, deliberately not started / Do not begin these until the foundation is honest and testable: / - **" — matches the citing claim | yes |
| `docs/world-model/PERSON-MODEL.md`:143 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/PERSON-MODEL.md`:146 | `HANDOFF.md:81` | `HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`) | Target reads: "- **P0.7** Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion." — matches the citing claim | yes |
| `docs/world-model/PERSON-MODEL.md`:1147 | `HANDOFF.md:81` | `HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`) | Target reads: "- **P0.7** Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion." — matches the citing claim | yes |
| `docs/world-model/PERSON-MODEL.md`:1318 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/PERSON-MODEL.md`:1464 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:25 | `HANDOFF.md:99-112` | `HANDOFF.md` § Backlog (`:107-120`) | Target reads: "## Backlog — captured, deliberately not started / Do not begin these until the foundation is honest and testable: / - **" — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:33 | `HANDOFF.md:130-132` | `HANDOFF.md` § Standing constraints (`:138-140`) | Target reads: "- AI agents may draft records but may not approve their own decisions. / - Human approval required for architecture, dep" — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:107 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:177 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:178 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:294 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:649 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:657 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:962 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/world-model/POPULATION-FIDELITY.md`:1047 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/README.md`:29 | `HANDOFF.md:99-112` | `HANDOFF.md` § Backlog (`:107-120`) | Target reads: "## Backlog — captured, deliberately not started / Do not begin these until the foundation is honest and testable: / - **" — matches the citing claim | yes |
| `docs/world-model/README.md`:37 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
| `docs/world-model/README.md`:75 | `HANDOFF.md:103` | `HANDOFF.md` § Backlog (`:111`) | Target reads: "- **Synthetic-society correction.** MERIDIAN must simulate how an entire society perceives, debates," — matches the citing claim | yes |
| `docs/world-model/README.md`:133 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/README.md`:135 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/world-model/README.md`:136 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/world-model/README.md`:137 | `HANDOFF.md:81` | `HANDOFF.md` § Phase 0 priority order (`:89`) | Target reads: "- **P0.7** Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion." — matches the citing claim | yes |
| `docs/world-model/README.md`:138 | `HANDOFF.md:82` | `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) | Target reads: "- **P0.8** Review the influence-operations targeting schema before publication." — matches the citing claim | yes |
| `docs/world-model/RELATIONSHIP-GRAPH.md`:663 | `HANDOFF.md:79-80` | `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) | Target reads: "- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full / snapshots, replay makes z" — matches the citing claim | yes |
| `docs/world-model/RELATIONSHIP-GRAPH.md`:1017 | `HANDOFF.md:76-78` | `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) | Target reads: "- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population` / must affect aggr" — matches the citing claim | yes |
| `docs/world-model/RELATIONSHIP-GRAPH.md`:1349 | `HANDOFF.md:131-132` | `HANDOFF.md` § Standing constraints (`:139-140`) | Target reads: "- Human approval required for architecture, dependencies, licence, migrations, auth, security / controls, public release" — matches the citing claim | yes |
| `docs/world-model/RELATIONSHIP-GRAPH.md`:1457 | `HANDOFF.md:82` | `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) | Target reads: "- **P0.8** Review the influence-operations targeting schema before publication." — matches the citing claim | yes |
| `docs/world-model/RELATIONSHIP-GRAPH.md`:1547 | `HANDOFF.md:130` | `HANDOFF.md` § Standing constraints (`:138`) | Target reads: "- AI agents may draft records but may not approve their own decisions." — matches the citing claim | yes |
