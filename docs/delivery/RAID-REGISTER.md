# RAID Register — Risks, Assumptions, Issues, Dependencies, Decisions

**Date:** 19 July 2026
**Status:** **DRAFT — pending owner review.** Nothing in this register is approved. Every entry marked
OPEN is a question for the owner and has deliberately not been answered here.
**Scope:** seeded from the closed broad audit (`CURRENT-STATE-AUDIT.md`), the targeted re-verification
(`A3-VERIFICATION-RESULTS.md`), the five publication blockers B1–B5, the two critical behavioural
findings, and a direct grounding pass over the tree at commit `71fa329`.

Read [`../../HANDOFF.md`](../../HANDOFF.md) first. This register does not restate the Phase 0 plan; it
records what could go wrong, what is being taken on trust, what is already broken, what blocks what, and
what has been decided.

---

## How to read this document

Every entry has two layers, per the standing record requirement:

- **Plain English** — what it means, written for a reader who has not seen the code.
- **Evidence** — a `path:line` citation or a reproducible command.

Where the grounding pass could not establish something, it is recorded as an **Assumption** and labelled
as such, not asserted as fact. Absence of evidence is written as absence of evidence.

**Identifier convention.** Assumptions are numbered `AS1`–`AS14`. Where this register writes `A3 §6` or
similar with a section sign, it means a section of `A3-VERIFICATION-RESULTS.md`, never an assumption —
the two referents are kept apart deliberately.

**Status vocabulary:** `OPEN` (live, no mitigation landed), `MITIGATED` (a control exists and was
verified), `CLOSED` (no longer applies), `ACCEPTED` (owner has knowingly taken it on).

All owners are recorded as `Aries Russell (unassigned)` because no assignment record exists anywhere in
the tree. Do not read that as delegation.

---

## 1. Risks

Things that have not yet gone wrong, and what happens if they do.

### R1 — No named RNG substreams: a latent reproducibility hazard the determinism test cannot see

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** high · **Owning workstream:**
P0.4A (deterministic randomness architecture) · **Source:** A3 §6, new defect exposed during
re-verification; owning workstream assigned by founder decision, 18 July 2026

**Plain English.** The whole simulation draws its random numbers from one shared pool, in one fixed
order. Nothing labels which subsystem owns which draws. So if anyone later adds or removes a single
random draw anywhere — in the cohort logic, in the diffusion step, anywhere — every later number in that
tick shifts, in every other subsystem, for reasons that have nothing to do with the model. Results will
change and look like the model changed. Worse, the test that exists to protect reproducibility would
read that shift as ordinary divergence and pass, so the change would land unnoticed.

This is not hypothetical. It has already produced a false positive in the audit itself: adding a
grievance to one cohort visibly moved a national indicator, which looked like the meso tier influencing
the macro tier. It was not. It was the extra draw shifting the stream.

**Owning workstream (added 19 July 2026).** This risk is no longer unowned. The founder decision of
18 July 2026 created a dedicated Phase 0 item for it — **P0.4A, establish deterministic randomness
architecture** — sequenced between P0.4 (define authoritative state) and P0.5 (implement cross-tier
causal channels). The founder's own statement of the problem is: "Materialising a background citizen must
not change tomorrow's weather, market behaviour, government approval or another person's decision merely
because it consumed extra draws." The isolation P0.4A must achieve is by subsystem, by entity, by
relationship or interaction, by simulation purpose, and by tick or event context where appropriate; the
decision records per-entity streams alone as insufficient. **Nothing has been built.** P0.4A is a
scheduled workstream, not a control that exists, so this entry stays OPEN and is not MITIGATED. It
becomes MITIGATED only when P0.4A passes its stated exit criteria — not when an approach is chosen and
not when an ADR is written.

**Why the existing test does not cover this.** The founder decision records the current determinism test
as *insufficient*, because it would accept draw-order contamination as ordinary divergence. P0.4A
therefore requires **isolation tests** — deliberately injecting extra draws into one stream and verifying
that the others are unchanged — not merely same-seed repetition tests. The evidence for that sits in
A3 §6, cited below. This register does not restate the Phase 0 plan, so the ten exit criteria the founder
decision sets for P0.4A — each written so that it is testable — are not reproduced here.
`PHASE-0-REMEDIATION-PLAN.md` is where they belong; check that it carries them rather than assuming it
does, on the same live-document caution recorded under R6.

**Impact.** Any future work on cohorts, diffusion or macro rules can silently invalidate previously
recorded numeric outputs. It also means the honest reproducibility claim the founder settled on is
fragile against ordinary maintenance. It further means that cross-tier work (P0.5) cannot be validated
numerically until draws are separable from each other — a linkage that was inference from the two
verified mechanisms above when this register was first drafted, and that the founder decision of
18 July 2026 has since made an explicit sequencing rule; see D5, D10, D11 and D12.

**Evidence.**
- Exactly one generator is constructed in application code:
  `scaffold/backend/app/simulation/engine.py:83` (`random.Random(resolved_seed)`). A grep for
  `random.Random(` across `scaffold/` returns that one site.
- Exactly three draw sites share it: `scaffold/backend/app/simulation/agents/cohort_agent.py:36`,
  `scaffold/backend/app/simulation/diffusion.py:75`,
  `scaffold/backend/app/simulation/engine.py:135`.
- The cohort draw is conditional (`if self.cohort.grievances:`,
  `scaffold/backend/app/simulation/agents/cohort_agent.py:35`), so a meso configuration change alters how
  many draws are consumed before the macro draw in the same tick. Consumption order is fixed by
  `engine.py:152` → `:156` → `:176`.
- Demonstrated numerically at `A3-VERIFICATION-RESULTS.md:156-168`
  (`shipping_throughput_pct_of_baseline: 0.6080711379477878 -> 0.5973599412373322`).
- The masking property is stated at `A3-VERIFICATION-RESULTS.md:170-175`.
- The determinism test compares only the final macro dictionary after 20 ticks and nothing else:
  `scaffold/backend/tests/test_engine.py:34-40`. The masking property that makes it insufficient is
  stated at `A3-VERIFICATION-RESULTS.md:170-175`.
- The P0.4A workstream, its scope and its exit criteria come from the founder decision of 18 July 2026,
  applied to this register by the cross-workflow integration sweep of 19 July 2026. **That decision was
  issued directly and is not itself a file in the tree at the time of this amendment** — `grep -rn "P0\.4A"
  --include=*.md .` returned no lines when this entry was written. It is therefore cited by date and not by
  `path:line`. Re-run that grep and read whatever it returns — `PHASE-0-REMEDIATION-PLAN.md` and
  `PROJECT-LOG.md` are the expected homes — before treating any P0.4A wording as settled record.
- The single shared stream is the documented design in ADR-007
  (`scaffold/docs/ARCHITECTURE_DECISIONS.md:60-67`: "All engine, agent, and diffusion randomness draws
  from that one RNG"), which is why the audit graded it as a caveat rather than a defect
  (`CURRENT-STATE-AUDIT.md:320`, finding 28). P0.4A therefore lands against an accepted ADR — see DEC8.

---

### R2 — Publishing capability claims that the code does not support

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** high · **Source:**
`CURRENT-STATE-AUDIT.md` §6.1; blockers B1–B4

**Plain English.** The repository's documents currently state, in the present tense, that the engine
checks whether an action is legal, that three database tables are persisted, that a determinism test runs
in continuous integration, and that adding a new nation archetype needs only a new JSON file. None of
those four things is true of the code as written. This is the single defect the founder kept the
repository private to fix. If it is published in this state, the weakest artefact — documentation
accuracy — is what a reader inspects first, and the project's genuinely good idea (the determinism
boundary) is discredited by association.

**Impact.** Reputational. `HANDOFF.md:13-19` frames documentation accuracy as the reason the repository is
being held private, so the founder's own position treats this as the governing exposure; this register does
not independently grade how visible it would be, and identifies no audience of its own. Correcting it is
cheap: `A3-VERIFICATION-RESULTS.md:237-247` records that four of the five blockers clear by text correction
alone, with no engineering work required.

**Evidence.**
- B1 claims still live: `README.md:38`, `README.md:41`, `scaffold/README.md:19`, `CHARTER.md:112`, plus
  code-level siblings at `scaffold/backend/app/simulation/engine.py:3-4`,
  `scaffold/backend/app/simulation/agents/institutional_agent.py:4-5`,
  `scaffold/backend/app/simulation/schemas/agent_schema.py:157-158` and `:377-379`, and
  `scaffold/backend/app/api/routes_simulation.py:4-5`. The actual gate is a dictionary lookup returning a
  copy: `scaffold/backend/app/simulation/engine.py:121-130`.
- B2 claim still live: `CHARTER.md:44` ("guards in CI"). No CI exists — `ls -a .github` returns "No such
  file or directory", and the only YAML in the tree is `scaffold/docker-compose.yml`.
- B3 claim still live: `scaffold/docs/ARCHITECTURE_DECISIONS.md:29-31`; `scaffold/README.md:41` places
  PostgreSQL in the architecture diagram with no "planned" annotation. No code instantiates
  `SimulationRun`, `StateSnapshot` or `EventLog` outside their definitions in
  `scaffold/backend/app/db/models.py`.
- B4 claim still live: `scaffold/docs/ARCHITECTURE_DECISIONS.md:75`, `README.md:72-74`,
  `scaffold/README.md:106-107`.
- Blocker table and clearance routes: `A3-VERIFICATION-RESULTS.md:237-247`.
- No correction has landed in tracked content: every B1–B4 claim line cited above is still present
  verbatim in the tree, and the only commit is `71fa329` (`git -C <repo> log --oneline`). Working-tree
  cleanliness is deliberately **not** used as evidence here — untracked Phase B draft records, including
  this file, now exist under `docs/delivery/` and `git status --short` is no longer empty.

---

### R3 — Dual-use exposure: a fully specified but currently inert influence-operations targeting schema, with no acceptable-use terms and no technical enforcement

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** high · **Source:** blocker B5;
`CURRENT-STATE-AUDIT.md` §5.12 and decision 8.6; P0.8 · **Re-pointed 19 July 2026:** the policy
question this risk waited on was answered by founder decision of 18 July 2026 (DEC6). The risk did
not close with it. **What remains open is the enforcement, not the decision.**

**Plain English.** (`CURRENT-STATE-AUDIT.md:411` calls this "a working audience-targeting and
campaign-design template"; the code does not execute it, so this register does not repeat "working" in its
own voice.) The schemas provide, field by field, a structured vocabulary for describing a segmented
population and a designed influence campaign: audience demographics including language and majority religion, per-channel
media reach, three separate persuadability scores, social-graph bridges, pre-existing grievances to
exploit, a claim that can be explicitly marked false, a messenger chosen for how independent he appears,
a count of coordinated accounts, and estimated reach. The demo scenario ships a fully populated example.
The only safeguards anywhere are three sentences of prose in the charter, and there is no licence term,
no acceptable-use restriction and no technical check of any kind behind them.

Two facts bear on how this exposure sits today. First, the repository is assumed private (see AS1 — an
assumption, not something observed). Second, the schema is currently declarative: the campaign object is
loaded and never read again, so nothing in the code operationalises it.

**What changed on 18 July 2026, and what did not.** The founder settled the policy position (DEC6): for
the public MVP, influence mechanics are confined to explicitly fictional worlds, the scenario loader must
require `world_mode: fictional` and fail closed without it, real-world scenario import stays disabled,
real persons/organisations/political populations may not be influence targets, protected characteristics
may not be optimisation criteria, fictional aggregate diffusion remains allowed, the API and UI must
disclose that the active world is fictional, and **disclosure or acceptable-use wording is supplementary
— technical enforcement is mandatory.** **None of those eight controls is built.** The decision therefore
converts this entry from a risk awaiting a judgement into a risk awaiting engineering: every one of the
eight is a requirement, and the current tree satisfies none of them. The evidence below is unchanged by
the decision and describes what exists, not what is required.

**Impact.** This entry no longer clears when the owner speaks; it clears when the eight controls are
implemented and verified. That is a larger exposure than the one first recorded here, not a smaller one:
the decision moved B5 out of the "clears by writing" column entirely and did not put it in the "already
cleared" column. It also means the risk stays OPEN through implementation, and no drafting of any kind
can move it. See DEC6, D1 and `PUBLICATION-EXIT-CRITERIA.md` C6.

**Evidence.**
- Targeting fields: `scaffold/backend/app/simulation/schemas/agent_schema.py:22-28` (demographics,
  including `religion_majority`), `:42-53` (five media channels), `:72-77` (three appeal scores),
  `:80-88` (social graph), `:91-109` (the cohort).
- Campaign design fields: `agent_schema.py:320-346`, with `truth_status` ∈ {true, false, unverified} at
  `:253-258`, messenger `perceived_independence` at `:287-303`, and
  `detection_probability` / `attribution_probability` at `:306-318`.
- Published as a cross-language mirror: `scaffold/schemas/campaign.schema.json:223-235`,
  `scaffold/schemas/narrative.schema.json:14-66`.
- Populated demo campaign: `scaffold/scenarios/kestral-strait.json:389-418` (claim marked
  `truth_status: "false"`; 40 coordinated accounts; 210,000 estimated reach).
- Safeguards are three prose bullets only: `CHARTER.md:135-142`.
- No enforcement: `NOTICE.md` (read in full) contains no acceptable-use or field-of-use term;
  `grep -rn "jsonschema" scaffold/` → no output, so the published mirrors validate nothing at runtime;
  the scenario's own `fiction_disclaimer` (`scaffold/scenarios/kestral-strait.json:7`) is read by no code
  and surfaced in no API response (`routes_simulation.py:47-49`, `:60`, `:71-77`, `:111`).
- Currently inert: `self.campaign` is assigned at `engine.py:111` and read nowhere; `Campaign(` appears
  only as the class definition; a twelve-term grep for targeting field names across `scaffold/backend/app/`
  excluding the schema file returns zero hits.

---

### R4 — The product's core mechanism does not exist yet: the three tiers do not influence one another

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** critical (behavioural) ·
**Source:** critical finding 4.1, as corrected by A3 §6

**Plain English.** MERIDIAN is sold on the idea of a society where a crisis propagates across three
levels. Today the three levels run in the same loop but never read each other. Hammering the national
indicators leaves cohort beliefs untouched; changing cohort beliefs by two orders of magnitude leaves the
national indicators unchanged (`A3-VERIFICATION-RESULTS.md:152`, `:165`). The apparent coupling that does
show up is the RNG artefact described in R1.

**Impact.** This is a product risk, not a tidiness one. Any external claim about cross-tier dynamics is
unsupported until P0.5 lands. HANDOFF marks P0.5 as arguably the highest-value item for exactly this
reason.

**Evidence.** Perturbation table at `A3-VERIFICATION-RESULTS.md:147-168`. Structurally: exactly one
cohort field is ever written (`cohort_agent.py:35-38`), no `MicroAgent` field is ever written, and
`represents_population` — the field that would make a cohort a weighted representative of a population —
is read by no code (declared at `agent_schema.py:95`; `build_cohort_graph` at `diffusion.py:18-37` uses
only `cohort_id`, `internal_cohesion` and `bridges_to`). P0.5 wording at `HANDOFF.md` § Phase 0 priority order (`:84-86`).

---

### R5 — Macro indicators saturate with no opposing mechanism anywhere in the engine

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** critical (behavioural) ·
**Source:** critical finding 4.2, confirmed and escalated by A3 §7

**Plain English.** Left running, the nation in crisis becomes maximally ready and maximally stable and
pins at the ceiling. This was suspected to be an artefact of the placeholder agent always choosing the
same action; `A3-VERIFICATION-RESULTS.md` tested varied action selection and it saturates identically. That document
found none of `cost`, `cooldown`, `decay`, `budget`, `resource`, `prerequisite` or `revert` present
anywhere in `engine.py` (`:192-200`, a string-presence check), and on that basis together with the
seven-row fixed-scalar effect table (`engine.py:35-43`) concluded the engine has no opposing mechanism at
all — an architectural gap, not a calibration problem.

**Impact.** Architectural gap, not calibration. It also carries a second-order risk: the obvious fix
(mean reversion) would be arbitrary, and HANDOFF explicitly forbids patching it before tick semantics and
horizon are defined (P0.7).

**Evidence.** `A3-VERIFICATION-RESULTS.md:177-204`, including the mechanism-absence grep block at
`:192-200` and the clamp-ceiling result `first tick at clamp ceiling: 61` at `:114-116`. The full effect
table is seven rows of fixed scalars touching three keys: `engine.py:35-43`.

---

### R6 — Dependency ranges with no lockfile: the environment is not reproducible

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** medium · **Source:**
`CURRENT-STATE-AUDIT.md:338` (audit finding 36) — a restatement, not a new finding

**Plain English.** Every one of the thirteen declared dependencies is an open version range. There is no
lockfile and no hashes, so two people installing on two days can get different versions, and neither can
prove what the other had. The Python version is stated only in prose and in the Docker base image; there
is no machine-readable declaration of it.

**Impact.** Undermines any reproducibility claim above the level of the seed. Directly bears on decision
DEC5 (packaging) and on P0.2.

**Evidence.** `scaffold/backend/requirements.txt:1-24` (the file is 24 lines) — thirteen requirement
lines (`grep -c -E '^[^#[:space:]]' scaffold/backend/requirements.txt` → 13), not a single `==` pin;
`websockets>=12.0` at
`:13` has no upper bound at all. **Thirteen is the correct count.** It was inconsistent across the
Phase B drafts as at 19 July 2026 — `PHASE-0-REMEDIATION-PLAN.md`, `CORRECTIVE-BACKLOG.md` (CB-26)
and `CAPABILITY-CLAIMS.md` (row C12) each said twelve in at least one place. All were reconciled to
thirteen in the cross-document consistency pass of 19 July 2026. Sibling drafts are live documents;
re-run `grep -rn "twelve\|thirteen" docs/delivery/` before relying on any count rather than quoting
this one forward. No `pyproject.toml`, no lockfile of any kind, no
`.python-version`,
no `ruff`/`mypy`/`tox` config anywhere in the tree — 55 tracked files (`git ls-files | wc -l`), 71
files total excluding `.git/` as at 19 July 2026, the difference being untracked Phase B working
documents. Python version appears
only at `scaffold/backend/Dockerfile:1`, `scaffold/docs/ARCHITECTURE_DECISIONS.md:11` and
`scaffold/CLAUDE.md:44`. The Dockerfile installs with no lockfile and no hash verification
(`Dockerfile:10-11`) and copies the whole build context with no `.dockerignore` present (`:13`).

---

### R7 — No CI, so nothing prevents a regression from landing

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** medium · **Source:**
`CURRENT-STATE-AUDIT.md:340` (audit finding 38) — a restatement, not a new finding

**Plain English.** There is no automated check on any change. Combined with R1, this means a change that
silently alters numeric results has no barrier to entry at all. Note that the charter already claims the
opposite, which is why this is also part of R2.

**Impact.** Every control that would normally catch documentation drift, dependency drift or a
determinism regression is absent. P0.3 addresses it, and HANDOFF constrains it correctly: only checks
that genuinely exist and pass.

**Evidence.** No `.github/` directory; no workflow file; the only YAML in the tree is
`scaffold/docker-compose.yml`. `.gitignore:16-18` pre-ignores `.mypy_cache/` and `.ruff_cache/` for
tooling that is not configured anywhere. Version control itself now exists locally (one commit, `71fa329`,
branch `main`, remote `origin` configured), so the version-control precondition for CI is met in the tree —
this is the half of blocker B2 that has become stale. Whether the commit is actually present on the remote,
which a hosted runner would need, was not verified (see AS2).

---

### R8 — Two unsynchronised drivers mutate the same in-memory run object

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** not graded in any source —
the audit records the mechanism but assigns it no severity; any grading below is this register's
reading, not the audit's · **Source:** `CURRENT-STATE-AUDIT.md:318` (audit finding 26, which already
records "The sync REST `advance` handler and the async WS handler can also interleave `step()` on one
shared model with no lock") — a restatement, not a new finding

**Plain English.** A run advances either by a REST call or by a WebSocket message, and both reach into
the same shared in-process dictionary of live models with no lock between them. Run state is not
persisted, is never evicted, and does not survive a process restart.

**Impact.** Interleaved use of both paths against one run has unverified behaviour — no test exercises it
and the grounding pass could not execute anything. That it is bounded today by the scaffold being
single-user, and that it would become a correctness risk if determinism claims were attached to a hosted
demo, are this register's readings; neither is graded in the audit or in `A3-VERIFICATION-RESULTS.md`.

**Evidence.** `scaffold/backend/app/api/runs.py:18` (`_RUNS: dict[str, MeridianModel]`), `:29-35`, `:38-40`;
REST driver at `scaffold/backend/app/api/routes_simulation.py:59`; WebSocket driver calling `model.step()`
directly at `scaffold/backend/app/api/routes_ws.py:41-46`. No lock appears in either path.

---

### R9 — Licence-adjacent claim in the stack description is incomplete

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** low · **Source:**
`CURRENT-STATE-AUDIT.md:341` (audit finding 39, the LGPL finding proper); the same constraint is
restated in decision 8.1 at `:401` — a restatement, not a new finding

**Plain English.** The scaffold README says the stack was chosen for permissive licensing and names three
permissive dependencies. It does not mention `psycopg2-binary`, which is LGPL. The audit's own note is
that LGPL is benign for a non-distributed service and not benign if a binary is ever shipped.

**Evidence.** `scaffold/README.md:111`; `scaffold/backend/requirements.txt:17`; audit finding at
`CURRENT-STATE-AUDIT.md:341`, restated as a decision constraint at `:401`.

---

### R10 — A prototype screenshot that escapes its fixture label becomes a capability overclaim outside the repository

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Severity:** high · **Owning workstream:**
Track C, lane C-VISUAL (gate C0) · **Source:** founder Track C correction, 19 July 2026 — issued directly
and not itself a file in the tree, so cited by date and not by `path:line`, per the note under R1's
evidence

**Plain English.** Gate C0 permits five screens to be built on fixture data long before the engine can
produce any of what they show. The correction makes that permissible only on one condition: every
fixture-backed surface must state, visibly, `INTERACTIVE PROTOTYPE — FIXTURE DATA — NOT CONNECTED TO THE
SIMULATION ENGINE`, and that label must remain visible in screenshots and recordings. The honesty of the
whole prototype lane therefore rests on a label surviving a crop, a slide paste, a compression pass and a
retelling.

An image travels without the repository attached. A cropped or unlabelled prototype screenshot says to
whoever sees it that MERIDIAN displays a working simulation of a society — and none of the mechanism
behind that impression exists: the tiers do not influence one another (R4), there is no replay path, and
the demonstration may not truthfully claim a simulated societal response until gate C2. That is exactly
the defect class recorded in R2, with one difference that makes it worse: it occurs outside the tree,
where correcting a file corrects nothing, and where the project has no way to reach the person who saw it.

**Impact.** The exposure opens the moment the first C0 screen renders and does not close when C2 lands,
because images already in circulation are not recalled by later capability. It is also the one risk in
this register that no in-repository control can fully close: a build-time assertion can keep the band on
the screen, but nothing can keep it inside the frame of someone else's crop. Treat the label as a
necessary control, not a sufficient one, and treat the handling of recordings and slide decks as part of
the control rather than as distribution hygiene.

**Evidence.**
- **Nothing in Track C is built, so the control has nothing to attach to yet.** `scaffold/frontend/`
  holds exactly one file, `index.html` (67 lines). It titles itself "MERIDIAN — frontend stub" (`:16`)
  and describes itself as a "Minimal dev harness" whose full UI is "left for a later build" (`:17-18`).
  Its whole interactive surface is three buttons and a log element (`:20-29`). None of the five gate-C0
  screens — Strategic Command Centre, Entity Dossier, Society Pulse, Conversational Command Interface,
  Causal Timeline — exists in any form.
- **No label mechanism exists anywhere.** `grep -rn "INTERACTIVE PROTOTYPE" .` returns no lines, and a
  case-insensitive grep for fiction, provenance, AI-generated or disclaimer text across
  `scaffold/frontend/` returns zero hits (the same check recorded under DEC6).
- **A divergence that must be reconciled rather than silently resolved.** Two untracked UI drafts already
  specify a fixture band, but with different wording from the founder correction:
  `docs/design/UI-RESEARCH-HANDOFF.md:335-342` and
  `docs/design/UI-VERTICAL-SLICE-RECOMMENDATION.md:39-42` both propose `FIXTURE DATA — NOT A SIMULATION
  RUN`, adjacent to a mandatory `FICTIONAL WORLD` disclosure, with a build-time assertion that it cannot
  be disabled. The founder wording is longer and says more — it names the artefact an interactive
  prototype and states that it is not connected to the engine. Which string governs, and whether the
  drafts are amended to the founder wording or the two are combined, is not settled here. This register
  does not choose.
- **The failure class this repeats:** R2 above, and `HANDOFF.md:13-19`, which records documentation
  accuracy as the reason the repository is held private. `CAPABILITY-CLAIMS.md` is the authority on
  permitted wording and governs any caption, title or narration accompanying a prototype image.

---

## 2. Assumptions

Everything here is **an assumption, not a verified fact.** Each is something a decision may rest on that
the grounding pass could not establish from the tree. None should be repeated as fact in any external
document without first being checked.

### AS1 — ASSUMPTION: the GitHub repository is private

**Owner:** Aries Russell (unassigned) · **Status:** unverified · **If wrong:** R2 and R3 are already
realised, not prospective — the highest-consequence assumption in this register.

**Plain English.** Every risk position in this document assumes the repository is not publicly visible.
That assumption comes from the handoff document, not from an observation. No `gh` command was run
(prohibited by the standing constraints) and no network call was made. A remote URL exists; its
visibility setting was not checked.

**Evidence.** `HANDOFF.md:13` ("**PRIVATE.** Deliberately."); remote confirmed by
`git -C C:\Users\daijo\project-meridian remote -v` →
`origin  https://github.com/CypherTechAries/project-meridian.git`. Visibility: not observed.

### AS2 — ASSUMPTION: the local commit has been pushed to the remote

**Owner:** Aries Russell (unassigned) · **Status:** unverified. The local remote-tracking ref `origin/main` points at the same object as `HEAD`
(`git rev-parse HEAD origin/main` → both `71fa329bd09506e8c657428cf92073ec1dda1bed`), which is consistent
with a completed push, but no fetch was performed. This reflects last-known local state, not the server.

### AS3 — ASSUMPTION: `pip install -r requirements.txt` fails on a clean machine because of `litellm`

**Owner:** Aries Russell (unassigned) · **Status:** reported second-hand, not reproduced. `HANDOFF.md:45-48` states that `litellm` resolves to
1.92.0, has no cp313 wheel, falls back to sdist and needs a Rust toolchain, so nothing installs. The
grounding pass did not create a virtual environment or install anything, so the failure mode and the
resolved version are both unconfirmed. What *was* verified directly: `litellm>=1.34,<2.0` is declared at
`scaffold/backend/requirements.txt:20`, and it is imported by no executable code anywhere — an AST parse
of every `.py` file under `scaffold/` scanned 78 import statements and found zero importing it. Its only
textual occurrence is inside the module docstring at
`scaffold/backend/app/simulation/llm_gateway.py:17-18`, which spans `:1-29`.

### AS4 — ASSUMPTION: the Docker build's behaviour on Linux / Python 3.11 is unknown

**Owner:** Aries Russell (unassigned) · **Status:** explicitly Unknown, and was already marked Unknown by the audit at
`CURRENT-STATE-AUDIT.md:29`. No build was run. Do not assert either that it works or that it fails.

### AS5 — ASSUMPTION: the five tests still pass

**Owner:** Aries Russell (unassigned) · **Status:** not re-run. `HANDOFF.md:51` records "5 passed" and `A3-VERIFICATION-RESULTS.md:23` records
that those results came from execution. The grounding pass could not execute anything: `import mesa` fails
with `ModuleNotFoundError` and the virtual environment that run used no longer exists under
`scaffold/backend/`. The test *count and names* were verified statically —
`grep -n "def test_" scaffold/backend/tests/test_engine.py` returns five definitions at lines 25, 34, 43,
52, 61 — but their current pass/fail state was not observed.

### AS6 — ASSUMPTION: no repository-level controls are configured on the remote

**Owner:** Aries Russell (unassigned) · **Status:** unverified. Branch protection, required status checks and secret scanning could not be checked
without a network or `gh` call. What is verifiable locally: there is no `CODEOWNERS` file in the tree
(absent from the exhaustive 55-file listing).

### AS7 — ASSUMPTION: `docs/PLAN.pdf` still contains the DISARM Red Framework correspondence claim

**Owner:** Aries Russell (unassigned) · **Status:** partially verified only. The audit anchored this claim to `scaffold/backend/plan.txt:221`, and
that file no longer exists. `DISARM` now has zero occurrences in any `.md`, `.txt`, `.py` or `.json` file
outside the audit itself. The PDF does still carry two DISARM link annotations —
`grep -aon ".\{0,120\}DISARM.\{0,120\}" docs/PLAN.pdf` returns two `/URI` annotations, one to the DISARM
frameworks repository and one to `disarm_red_framework.md`. The *prose* of the correspondence claim lives
in compressed content streams and was not extracted. Do not quote the audit's wording of it as current.

### AS8 — ASSUMPTION: no concrete dependency version can be stated

**Owner:** Aries Russell (unassigned) · **Status:** verified as unknowable from the tree. Every requirement is a range, nothing is installed, and
no lockfile exists. The only concrete versions recorded anywhere are the A3 environment note
(`A3-VERIFICATION-RESULTS.md:27`: CPython 3.13.9, mesa 2.4.0, pytest 8.4.2), which describes one past
session on one machine — two minor Python versions above the 3.11 the Dockerfile pins — and not a
supported configuration.

### AS9 — ASSUMPTION: audit §6.1 is the complete population of false claims

**Owner:** Aries Russell (unassigned) · **Status:** unverified, and deliberately so. The grounding pass re-checked only the already-identified
list. It did not search for additional untrue statements, because the broad audit is closed and hunting
for new findings is outside the constraints. It follows that "all false claims are corrected" cannot be
asserted after P0.1 — only "all *identified* false claims are corrected."

**Evidence.** This is a statement about the *scope of a process*, so the only citable artefacts are the
scope itself and the constraint that fixed it: the identified population is `CURRENT-STATE-AUDIT.md:283-293`
(§6.1, items 1–11), extended by the corrections list in `A3-VERIFICATION-RESULTS.md`. The audit is recorded
as closed at `HANDOFF.md:30`, and the standing constraint against reopening it is `HANDOFF.md` § Standing constraints (`:137`) ("Do not
launch another unrestricted multi-agent audit. The broad audit is closed."). No command can evidence a search that was deliberately not
run; a reader wanting assurance would have to commission that search as new work.

### AS10 — ASSUMPTION: Mesa does not draw from or touch the project's own RNG

**Owner:** Aries Russell (unassigned) · **Status:** unverified. Mesa is not installed, so its `Model.__init__(seed=...)` internals could not be
inspected. Two RNGs are seeded from the same value at `engine.py:81-83`, and no application code reads
Mesa's `self.random` (grep returns zero hits) — but that Mesa never touches `self.rng` was not confirmed.
Bears directly on R1 and on decision DEC3.

### AS11 — ASSUMPTION: the per-tick RNG draw count for the demo scenario is ten

**Owner:** Aries Russell (unassigned) · **Status:** arithmetic from source, not a measurement. Four cohort draws (four of five cohorts have
non-empty `grievances`; `urban-professional-vantaran` has `"grievances": []` at
`scaffold/scenarios/kestral-strait.json:66`), five diffusion draws, one macro draw. NetworkX node
iteration order at `diffusion.py:64` was read as insertion order from `diffusion.py:29-30` but not
executed to confirm.

### AS12 — ASSUMPTION: no decision has been taken outside this repository

**Owner:** Aries Russell (unassigned) · **Status:** unverified. The decision statuses in section 5 were derived from case-insensitive searches over
`HANDOFF.md`, `CHARTER.md`, `NOTICE.md`, `README.md` and `docs/` — reproducible as
`grep -rniE "mesa|uv\b|pyproject|PLAN\.pdf|plan\.txt|acceptable.use|field.of.use" HANDOFF.md CHARTER.md NOTICE.md README.md docs/`.
Absence of a written decision in the tree is not
proof that no decision was taken. **This assumption was borne out for DEC6**, which was settled by a
founder decision issued on 18 July 2026 outside the tree and unknown to the searches above; it is
recorded as SETTLED as of 19 July 2026. If any of DEC3, DEC5 or DEC7 has likewise been settled elsewhere,
this register is wrong and should be corrected rather than the decision re-made.

### AS13 — ASSUMPTION: the removal of `plan.txt` and the rewrite of `README.md` were deliberate

**Owner:** Aries Russell (unassigned) · **Status:** unverifiable. History is a single commit — `git -C <repo> log --oneline` returns exactly
`71fa329 Initial commit: MERIDIAN scaffold, charter, and current-state audit` — so there is no
before-and-after to diff, and `git log --follow -- scaffold/backend/plan.txt` can return no deletion event.
That the file is absent is checkable (`find . -path ./.git -prune -o -name "plan.txt" -print` → no
results); that its absence was deliberate is not. Both changes happen to satisfy audit work items
(`CURRENT-STATE-AUDIT.md:427`), but intent cannot be established.

### AS14 — ASSUMPTION: nothing outside this repository consumes the published JSON Schema mirrors

**Owner:** Aries Russell (unassigned) · **Status:** unverifiable from inside the tree. Nothing inside the repository reads
`scaffold/schemas/*.schema.json` (`grep -rn "jsonschema" scaffold/` → no output). External consumption is
outside what can be observed here, and matters to R3 if the schemas have been shared anywhere.

---

## 3. Issues

Live defects observed in the tree. These are not risks; they have already occurred — with the single
exception of I2, whose failure mode is reported second-hand and was not reproduced in this pass (see AS3).

### I1 — Four publication blockers remain uncorrected in the tree

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Blocks:** publication

B1, B2, B3 and B4 all clear by text correction, and none has been corrected. Verified claim by claim in the
tracked source files — citations for each blocker are given under R2 — not inferred from repository state.

Note that the presence or absence of Phase B governance artefacts is **not** a reliable proxy for whether
Phase 0 correction has begun: `docs/delivery/` now contains untracked drafts including
`PHASE-0-REMEDIATION-PLAN.md`, `CAPABILITY-CLAIMS.md`, `CORRECTIVE-BACKLOG.md`, `PROJECT-LOG.md`,
`PUBLICATION-EXIT-CRITERIA.md`, `ADR-TEMPLATE.md` and this file, alongside untracked `docs/design/`,
`docs/safety/` and `docs/world-model/` directories (`git status --short`). Phase B is therefore visibly in
progress, which supersedes the "Not started" state recorded at `HANDOFF.md:34-38`.

### I2 — The documented installation path is reported broken

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Blocks:** publication exit criterion 1
(`HANDOFF.md` § Publication exit criteria (`:96`)). It plausibly also blocks P0.3, on the reasoning that CI cannot run a check on an
install that fails — *that is inference, not a documented dependency; see D2.*

All three documented install paths route through the same unpinned `requirements.txt`: Docker
(`scaffold/README.md:44-51`), local venv (`:53-60`) and tests (`:62-71`), restated at
`scaffold/CLAUDE.md:32-42`. The `litellm` pin at `requirements.txt:20` is present, and no code imports it.
**The failure itself is second-hand — see AS3.** State it as "reported to fail, not reproduced in this
pass" until someone runs it on a clean machine.

### I3 — `CHARTER.md:44` asserts a CI guard that does not exist

**Owner:** Aries Russell (unassigned) · **Status:** OPEN

Exact wording: "(ADR-006) enforces in code and `test_llm_gateway_cannot_write_state` guards in CI." No CI
exists. This is blocker B2's live half. Note the referenced test is also weaker than the sentence implies:
it asserts only that the returned object is an `ActionProposal` and that the instance lacks attributes
literally named `apply_deltas` and `macro_state` (`scaffold/backend/tests/test_engine.py:61-77`) — it
performs no import-graph analysis and attempts no mutation.

### I4 — Nine citations point at five documents that do not exist

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Blocks:** Phase 0 exit criterion at
`CURRENT-STATE-AUDIT.md:431`

Missing: `design_simulation_schemas.md`, `design_nation_expansion.md`, `design_ux_screens.md`,
`research_architecture.md`, `research_licensing.md`. Cited at
`scaffold/backend/app/simulation/schemas/agent_schema.py:3`, `.../macro_schema.py:3`,
`scaffold/CLAUDE.md:49`, `scaffold/docs/AGENT_TASK_TEMPLATE.md:54`,
`scaffold/docs/ARCHITECTURE_DECISIONS.md:4` (two files on one line), `:25`, `:71`, and
`scaffold/frontend/index.html:18`; plus a glob reference at `scaffold/docs/AGENT_TASK_TEMPLATE.md:25`.
The audit says ten references; it is now nine, because the two anchored in `plan.txt` went with the file.

### I5 — `README.md:96` links to `COPYRIGHT.md`, which does not exist

**Owner:** Aries Russell (unassigned) · **Status:** OPEN

Exact wording: "Licensing and contribution terms are under review. See [`COPYRIGHT.md`](COPYRIGHT.md)."
The file holding that position is `NOTICE.md`. Of the 16 markdown link targets in `README.md`,
`CHARTER.md`, `NOTICE.md`, `HANDOFF.md` and `scaffold/`, this is the only one that does not resolve. Links
inside the untracked `docs/design/`, `docs/safety/` and `docs/world-model/` directories were not surveyed,
so this is not asserted as the only broken link in the tree as a whole.

### I6 — `NOTICE.md:11` states the source is publicly visible; the repository is private

**Owner:** Aries Russell (unassigned) · **Status:** OPEN

Exact wording: "The source code is publicly visible for evaluation and portfolio purposes." Written in the
present indicative, and it contradicts `HANDOFF.md:13`. This is the same defect class Phase 0 exists to
correct, sitting inside the document that records the licence position. **Whether it was meant as a
present statement or as a description of the intended post-publication position is a question for the
owner — see OQ1 under Decisions. It is not resolved here.**

### I7 — The audit's own citations have drifted and no longer resolve

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Impact:** anyone re-checking the audit
against the tree will hit dead references and may wrongly conclude a finding was withdrawn

Confirmed drift: `scaffold/backend/plan.txt` no longer exists, so `plan.txt:221` (cited twice) and
`plan.txt:229` are unresolvable — `CURRENT-STATE-AUDIT.md:235`, `:291`, `:217`, `:349`, `:413`.
`README.md` was rewritten and is now 96 lines, so `README.md:92` (`:237`, `:342`, `:393`, `:403`),
`README.md:106-107` (`:174`, `:219`), `README.md:25` (`:84`) and `README.md:19`/`:24` (`:158`) all point
at different content than the audit describes. `COPYRIGHT.md` (`:237`) does not exist. The "no `.git`"
clause is now false wherever it appears (`:13`, `:283`, `:339`, `:372`, and
`A3-VERIFICATION-RESULTS.md:242`).

The findings themselves are unaffected by any of this; only the anchors have moved. **Whether the closed
audit document may itself be edited to re-point its citations — or whether the drift should instead be
recorded in a separate erratum, or left as it stands with this entry as the only record — is an owner
decision and is not settled here. See OQ3.** Note that the audit already schedules "repoint the ten dangling
design-doc citations" as Phase 0 work (`CURRENT-STATE-AUDIT.md:427`), but that authorises repointing
citations in the codebase; it does not speak to editing the audit's own evidence lines.

### I8 — One unresolved placeholder marker remains

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Blocks:** Phase 0 exit criterion at
`CURRENT-STATE-AUDIT.md:433`

`scaffold/CLAUDE.md:59`: `<!-- PLACEHOLDER: fill in with the team's real conventions -->`. It is the only
`PLACEHOLDER` marker anywhere in the tree.

### I9 — The player decision endpoint accepts anything and validates nothing

**Owner:** Aries Russell (unassigned) · **Status:** OPEN (documentary half is blocker B1; behavioural half
is permitted scaffold incompleteness)

`POST /runs/{id}/decision` appends a raw dict to an in-memory list and returns `{"accepted": true}`
unconditionally. It calls neither `_validate_and_price` nor `apply_deltas`, and `step()` never reads
`event_log`, so a submitted decision cannot influence any later tick. The client's own `legal_check`
verdict is stored verbatim and echoed back. Driven through the real API at
`A3-VERIFICATION-RESULTS.md:120-141`. Code: `scaffold/backend/app/api/routes_simulation.py:80-101`
(effects hard-coded to `[]` at `:97`); `engine.py:147-180` never reads `event_log`.

### I10 — Nothing is ever written to the database

**Owner:** Aries Russell (unassigned) · **Status:** OPEN (blocker B3's factual basis)

Three ORM classes are defined and none is instantiated; there is no `session.add`, `.commit` or `.merge`
anywhere in the scaffold. The only database interaction possible is DDL via `init_db()`, invoked from a
startup hook wrapped in a bare `except Exception` that logs a warning and continues
(`scaffold/backend/app/db/session.py:37-41`; `scaffold/backend/app/main.py:30-39`). The session dependency
`get_db()` is defined at `session.py:44-50` and used by no route. The app therefore boots identically with
or without Postgres, and persists zero rows either way.

### I11 — `apply_deltas` silently discards unknown and nested keys

**Owner:** Aries Russell (unassigned) · **Status:** OPEN · **Source:** A3 §1 sub-finding

A misspelled or nested indicator name produces no error, no warning and no effect. This makes the three
nested state blocks (`institutional_trust`, `alliance_confidence`, `public_finances`) structurally
unreachable through the engine's only delta path. Code:
`scaffold/backend/app/simulation/agents/macro_state.py:36-41`; nested blocks declared at
`scaffold/backend/app/simulation/schemas/macro_schema.py:52-54`, `:58-60`, `:70`. Sub-finding recorded at
`A3-VERIFICATION-RESULTS.md:73-76`. Note the counterpart docstring defect: `macro_state.py:26-27` says
nested blocks "are handled explicitly by the engine, not here" — no code anywhere writes any nested block.

### I12 — No `LICENSE` file exists; whether one should is itself open

**Owner:** Aries Russell (unassigned) · **Status:** OPEN as a *question*, not graded as a defect ·
**See:** OQ2

Observed fact: a directory listing of the repository root shows `.git`, `.gitignore`, `CHARTER.md`,
`HANDOFF.md`, `NOTICE.md`, `README.md`, `docs`, `scaffold` — and no `LICENSE`.

This entry deliberately does **not** assert that a `LICENSE` file ought to exist. The audit's
sub-instruction "add the file so tooling can detect it" (`CURRENT-STATE-AUDIT.md:401`) was written on the
assumption that a licence would be selected; DEC1 records that none will be. Whether the instruction still
applies once no licence is being chosen — and whether an all-rights-reserved position should nonetheless
be expressed as a machine-detectable file — is the owner's call (OQ2). If the owner answers no, this entry
closes as never having been an issue.

### I13 — All three Phase 0 exit-criterion greps currently fail

**Owner:** Aries Russell (unassigned) · **Status:** OPEN

As run against the current tree, per `CURRENT-STATE-AUDIT.md:431-433`:
`grep -rn "design_[a-z_]*\.md\|research_[a-z_]*\.md" . | grep -v "^./docs/delivery/"` → 8 lines, all
pointing at files that do not exist (criterion requires zero, or only hits at existing files);
`grep -rn "in CI" --include="*.md" --include="*.py" --include="*.html" . | grep -v "^./docs/delivery/"` →
**2 lines**, not one: `CHARTER.md:44`, which is false; and `docs/world-model/PERSON-MODEL.md:168`
("Sensitivity tests must run in CI"), which is a forward-looking rule in an untracked draft rather than a
present-tense claim, and which therefore needs adjudicating against the criterion's wording at
`CURRENT-STATE-AUDIT.md:432` ("returns nothing that is false") rather than being silently omitted;
`grep -rn "PLACEHOLDER" …` → 1 line, `scaffold/CLAUDE.md:59`.

All three criteria therefore fail as at the date of this register. One audit work item is already
satisfied: "delete `backend/plan.txt`" (`CURRENT-STATE-AUDIT.md:427`) is a no-op, because the file is gone.

---

## 4. Dependencies

What must happen before what, and what waits on someone else.

| ID | Dependency | Type | Status | Owner |
|---|---|---|---|---|
| D1 | **B5 / P0.8 cannot be cleared by any amount of drafting.** *Re-pointed 19 July 2026: the owner policy decision it waited on was taken on 18 July 2026 (DEC6), so this row no longer depends on a person. It now depends on work.* B5 clears only when the eight controls the decision names are **implemented and verified**; the decision states that disclosure and acceptable-use wording are supplementary and technical enforcement is mandatory. Everything else in the publication gate can be completed without it; publication cannot. | ~~Owner decision~~ → Implementation + verification | BLOCKING | Aries Russell (unassigned) |
| D2 | **P0.3 (real CI) probably depends on P0.2 (working install).** CI that cannot install the project cannot run a check, and HANDOFF constrains CI to "only checks that genuinely exist and pass". *HANDOFF does not state this as a dependency; the cited lines are the text of P0.2 and P0.3 themselves. The linkage is inference from their content.* | Internal, **inferred** | OPEN | Aries Russell (unassigned) |
| D3 | **P0.5 (cross-tier causal channels) depends on P0.4 (authoritative-state contract).** Causal channels need a defined thing to write to and read from before they can be designed without arbitrary coupling. *When first drafted this was the weakest link in the table, derived from the order of the two items in the HANDOFF list and nothing more. The founder decision of 18 July 2026 restated the full Phase 0 order and stated that P0.5 implementation "waits for state ownership and randomness isolation", so the linkage is now documented rather than inferred. HANDOFF itself still states no dependency; see D10.* | Internal, sequencing — **documented 18 July 2026**, previously inferred | OPEN | Aries Russell (unassigned) |
| D4 | **Any saturation fix depends on P0.7 (simulation time and horizon), stated explicitly as "before touching saturation" with "no arbitrary mean reversion".** | Internal, sequencing | OPEN | Aries Russell (unassigned) |
| D5 | **Numeric validation of R4's cross-tier work depends on resolving R1, now owned by P0.4A.** Until draws are separable per subsystem, a change in cohort logic and a change in macro logic are indistinguishable in the output. *This linkage was inference from the two verified mechanisms when first drafted. The founder decision of 18 July 2026 has since made it explicit and given it an owning workstream; D10 records the resulting block.* | Internal, **documented 18 July 2026**, previously inferred | OPEN | Aries Russell (unassigned) |
| D6 | **How P0.2 is executed depends on DEC5 (uv / `pyproject.toml`).** The audit notes the migration changes four documented workflows and the Dockerfile, so it is a deliberate migration rather than a fix to slip in. | Decision → work | OPEN | Aries Russell (unassigned) |
| D7 | **DEC3 (Mesa) touches determinism.** The audit records that Mesa materialises a second `random.Random` seeded from entropy on the API path and introduces a `Model.rng` collision on a future 3.x upgrade. Under `HANDOFF.md` § Standing constraints (`:139-140`), anything affecting determinism or authoritative state requires human approval. AS10 (unverified Mesa RNG behaviour) sits underneath this. | Decision → work | OPEN | Aries Russell (unassigned) |
| D8 | **Publication depends on all seven exit criteria plus explicit owner approval**, and the visibility command must not be run before both. | Gate | BLOCKING | Aries Russell (unassigned) |
| D9 | **External dependency on the remote host's configuration is unknown, not absent.** Branch protection, required checks and secret scanning could not be checked (AS6), and there is no `CODEOWNERS` file locally. | External, unverified | UNKNOWN | Aries Russell (unassigned) |
| D10 | **P0.5 *implementation* is blocked until P0.4A passes.** P0.5 *specification* is explicitly permitted to proceed in parallel beforehand — the block is on building the causal channels, not on designing them. The reason is R1/D5: while every subsystem shares one stream, a genuine cross-tier effect and a draw-order shift are indistinguishable in the output, so a causal channel could not be shown to work even if it did. | Internal, sequencing — **documented by founder decision, 18 July 2026** | BLOCKING | Aries Russell (unassigned) |
| D11 | **Entity promotion is blocked until P0.4A passes.** Promoting a background person to a detailed individual must consume draws to generate the profile; on the single shared stream those draws would shift every later draw in the run, so national indicators would move because the player looked at someone. Two of the P0.4A exit criteria address exactly this: promoting one background person must not alter previously established entities, and repeating the same promotion event must produce the same profile and history. | Internal, sequencing — **documented by founder decision, 18 July 2026** | BLOCKING | Aries Russell (unassigned) |
| D12 | **World-model materialisation is blocked until P0.4A passes.** The same mechanism as D11, applied to the world model as a whole: materialising entities is a draw-consuming operation, and on a shared stream it contaminates unrelated subsystems. This is a block on materialising the specified entities in code. It does **not** block further specification work under `docs/world-model/`. | Internal, sequencing — **documented by founder decision, 18 July 2026** | BLOCKING | Aries Russell (unassigned) |
| D13 | **P0.4A requires an ADR that deliberately selects an approach, and that selection is unmade (DEC8).** The founder decision states that an ADR is required because there are at least two valid approaches, that it must choose one deliberately, and that it must explicitly reject ordinary sequential calls to a single shared PRNG for authoritative behaviour. No agent may make that selection. **A drafted candidate exists — [`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md), 19 July 2026, Status *Proposed*, AI-drafted, Approval block empty — which recommends keyed / counter-based draws. It does not close this item: the selection is still unmade.** | Decision → work | OPEN | Aries Russell (unassigned) |
| D14 | **Gate C0 (visual proof) is unlocked by the UI-research handoff being received and reconciled, and by nothing in Phase 0.** Target: five connected fixture-backed screens — Strategic Command Centre, Entity Dossier, Society Pulse, Conversational Command Interface, Causal Timeline — in an original visual language, each carrying the prototype label, plus a five-minute scripted walkthrough that claims no connected simulation behaviour. C0 must **not** wait for P0.4–P0.6, and the absence of C3 is not a reason to delay it. **Nothing is built:** `scaffold/frontend/` is a 67-line dev stub and none of the five screens exists. R10 is the standing risk on this gate. | Gate — target, not progress | NOT STARTED | Aries Russell (unassigned) |
| D15 | **Gate C1 (live state connection) is blocked until P0.4 passes.** Target: the UI reads a versioned authoritative snapshot, holds no authoritative state client-side, shows at least one real entity, cohort, organisation and indicator drawn from the engine, and keeps fixture-only values visibly distinguished from live ones. P0.4 (define the authoritative-state contract, `HANDOFF.md:75`) is the unlock condition: there is no snapshot contract to read today, and nothing is persisted at all (I10). | Gate — blocked | BLOCKING | Aries Russell (unassigned) |
| D16 | **Gate C2 (live societal propagation) is blocked until *both* P0.4A and P0.5 pass.** Target: one real end-to-end chain — maritime crisis → insurer risk response → shipping-company rerouting → port-economic exposure → cohort belief and behaviour change → media and family reaction → political pressure → government state change — displayed **from the engine**, not from a fixture script. P0.5 is the unlock because no cross-tier channel exists (R4); P0.4A is an unlock in its own right and not a convenience, because on one shared stream a genuine cross-tier effect and a draw-order shift are indistinguishable in the output (R1, D5, D10) — the chain could not be shown to work even if it did. **C2 is the first point at which the demonstration may truthfully claim that MERIDIAN simulates a societal response.** Until it passes, no walkthrough, caption or recording may make that claim. | Gate — blocked, chain | BLOCKING | Aries Russell (unassigned) |
| D17 | **Gate C3 (explainability and replay) is blocked until P0.6 passes.** Target: causal events with causal parents, rule and mechanism attribution, before/after state, assumptions and uncertainty, state hashes, recorded external inputs, and replay performing **zero** model or network calls and yielding identical authoritative hashes. P0.6 (`HANDOFF.md` § Phase 0 priority order (`:87-88`)) is the unlock: there is no replay path, no state hashing and no capture of RNG state anywhere in the tree, and nothing is written to the database (I10). **Only after C3 may the project claim causal reconstruction or replay capability** — which is also why DEC4's target contract must stay labelled a target until then. | Gate — blocked | BLOCKING | Aries Russell (unassigned) |
| D18 | **Gate C4 (scale evidence) depends on a runnable engine, therefore on the same chain as C2 and C3.** Target: benchmarks across several entity and cohort counts recording tick time, memory, event volume and replay duration; MEASURED performance kept distinct from PROJECTED architecture; a documented path to partitioning or distributed execution **without** claiming it has been delivered. No benchmark of any kind exists, and no measurement can be taken today (AS5: the tests were not even re-run, `import mesa` fails). | Gate — blocked | BLOCKING | Aries Russell (unassigned) |
| D19 | **The demonstration's critical path is P0.4 → P0.4A → P0.5 → P0.6, which places Track B on the critical path rather than beside it.** The endpoint of the final demonstration requires three capabilities the audit found missing: that the engine validates and executes an action (blocker B1 — `_validate_and_price` is a seven-entry dictionary lookup), that the society reacts differently across entities (critical finding 4.1 — the tiers are causally decoupled), and that replay reproduces the authoritative state hash (no replay path, no state hashing, RNG state never captured). Lane C-ENGINE follows that chain in order; lane C-VISUAL runs alongside it on labelled fixture data and can never be described as the final functioning demonstration. Two walkthroughs result, and they must not be conflated: **PROTOTYPE WALKTHROUGH** (fixture-backed, early, product and design communication) and **INTEGRATED ENGINE WALKTHROUGH** (the real P0.5 chain plus P0.6 trace and replay — the final interview artefact). | Internal, sequencing — critical path | BLOCKING | Aries Russell (unassigned) |

Sources — every row, including the inferred ones, with the nature of the support stated:

- **D1** — documented: `HANDOFF.md` § Publication exit criteria (`:104-105`), `A3-VERIFICATION-RESULTS.md:245`. **Both of those lines are
  now stale in the same way**: they describe B5 as clearing by an owner decision. The decision was taken
  on 18 July 2026 and B5 did not clear with it. The founder decision of that date is the later record and
  is cited by date, not by `path:line`, for the reason given under R1's evidence.
- **D2** — **inferred.** `HANDOFF.md:72-74` is the text of P0.2 and P0.3; it does not assert a dependency
  between them.
- **D3** — **now documented.** `HANDOFF.md` § Phase 0 priority order, P0.4 (`:75`) and P0.5 (`:84-86`) is the text of both items and asserts no dependency;
  the founder decision of 18 July 2026 supplies the sequencing statement. Recorded as inferred-from-
  ordering-alone in the original draft of this register, and corrected on 19 July 2026.
- **D4** — documented, near-explicit: `HANDOFF.md` § Phase 0 priority order, P0.7 (`:89`) ("before touching saturation", "no arbitrary mean
  reversion").
- **D5** — mechanism verified in R1 and R4; the *linkage* was inferred in the original draft and is
  documented by the founder decision of 18 July 2026. See R1's Impact paragraph.
- **D6** — documented: `CURRENT-STATE-AUDIT.md:409`.
- **D7** — documented: `CURRENT-STATE-AUDIT.md:405`, `HANDOFF.md` § Standing constraints (`:139-140`); AS10 underneath.
- **D8** — documented: `HANDOFF.md:18-19`; `HANDOFF.md` § Publication exit criteria (`:92-102`).
- **D9** — not a sourced dependency but a recorded unknown; rests on AS6, plus the local absence of a
  `CODEOWNERS` file (exhaustive 55-file listing).
- **D10, D11, D12, D13** — documented by the founder decision of 18 July 2026, which is not itself a file
  in the tree at the time of this amendment; cited by date, per the note under R1's evidence. The
  underlying mechanism is verified and citable independently: `A3-VERIFICATION-RESULTS.md:156-175` for the
  contamination and its masking, and `docs/world-model/ENTITY-ONTOLOGY.md:509-563` (§7.3) for the
  promotion and stable-identity consequences that D11 and D12 rest on. Note that §7.3 records the
  prerequisite as sitting "under no Phase 0 item"; **P0.4A supersedes that sentence.** Whether that
  document has been amended to say so was not confirmed from this entry — re-read it rather than relying
  on its framing.
- **D14–D19** — documented by the founder Track C correction of 19 July 2026, which established that
  Track C is a two-lane programme (C-VISUAL and C-ENGINE) with five gates, and is **not** a UI
  workstream. That correction was issued directly and is not a file in the tree at the time of this
  amendment: `grep -rln "Track C" --include=*.md .` returned no lines when these rows were written, so it
  is cited by date, on the same basis as the P0.4A rows above. Re-run that grep and read whatever it
  returns before treating any Track C wording as settled record. The Phase 0 items each gate waits on are
  citable independently — all four in `HANDOFF.md` § Phase 0 priority order: P0.4 at `:75`, P0.4A at
  `:76-83`, P0.5 at `:84-86`, P0.6 at `:87-88`. *(Amended 19 July 2026: when this row was written P0.4A
  was citable only to the founder decision of 18 July 2026, because `HANDOFF.md`'s canonical sequence
  did not yet list it. The founder ordered that omission corrected on 19 July 2026 and P0.4A now sits
  in the sequence — see `HANDOFF.md` § Amendment record and
  `docs/delivery/HANDOFF-REFERENCE-MIGRATION.md`.)* The state of the tree they are measured against: no cross-tier
  effect (`A3-VERIFICATION-RESULTS.md:147-168`), no persistence (I10), no replay path or state hashing,
  and a frontend consisting of one 67-line stub file (`scaffold/frontend/index.html:16-18`). **Every one
  of D14–D19 records a target and an unlock condition. None records progress: no gate is open, no screen
  exists, and no benchmark has been taken.**
- **D14** — the fixture-labelling condition attached to C0 is carried as a risk, not as a row: see R10,
  including the wording divergence between the founder label and the two untracked UI drafts.

---

## 5. Decisions

DEC1–DEC7 are the seven items from `CURRENT-STATE-AUDIT.md` §8 (`:397-413`). **Four of those are settled
and cite where; three are OPEN.** DEC8 was appended on 19 July 2026 and is **not** a section-8 item: it is
a new decision surface created by the founder decision of 18 July 2026, which requires an ADR selecting a
deterministic-randomness approach. **Four entries are therefore OPEN and are written as questions for the
owner. They are not answered here, and no AI agent may answer them.**

*Amended 19 July 2026: DEC6 moved from OPEN to SETTLED by founder decision of 18 July 2026. The counts in
the paragraph above were adjusted for that and for nothing else. Settling DEC6 did **not** close R3, D1 or
publication blocker B5 — see DEC6's closing note.*

### DEC1 — Project licence · **SETTLED**

**Decision.** No licence. All rights reserved. No open-source licence is to be added, and external code
contributions are not accepted.

**Recorded at:** `HANDOFF.md:22-23` (the decision), `NOTICE.md:3` and `:29-31` (the position, and the
absence of inbound contribution terms).

**Caveats.**

(i) **Two documents describe the standing of this decision differently, and this register does not
reconcile them.** `HANDOFF.md:22-23` states the decision without qualification: "Licence: none,
deliberately." It contains no "for now" and does not describe itself as interim. `NOTICE.md` describes the
recorded position as provisional: "Licensing and contribution terms are under review" (`:16`) and "This is
a statement of the current position, not a final licensing decision" (`:41-43`). Whether the decision is
intended as final or as an interim position pending a commercial choice is for the owner to state — see
OQ4. This register deliberately does not restate the founder's decision in reworded form.

(ii) The audit's sub-instruction to add a detectable file is unsatisfied — see I12 and OQ2.

### DEC2 — Repository visibility and the publication gate · **SETTLED**

**Decision.** Private first, with a publication checklist as the gate. MERIDIAN becomes public only after
Phase 0 corrections pass **and** the owner approves. The visibility command is recorded but must not be
run before then.

**Recorded at:** `HANDOFF.md:13-19` (the decision and the prohibition); `HANDOFF.md` § Publication exit criteria (`:92-102`) (the gate — a
seven-item exit checklist). This satisfies the audit's "private first with a publication checklist as the
gate" option at `CURRENT-STATE-AUDIT.md:403`, and supersedes the audit's remark at `:393` that no
checklist exists.

**Note.** That the repository *is* private rests on `HANDOFF.md:13` and was not independently observed —
see AS1.

### DEC3 — Whether Mesa remains the ABM substrate · **OPEN**

> **Question for the owner:** Should Mesa remain the agent-based-modelling substrate, or should the
> dependency be dropped and the tick loop owned outright?

Constraints on the record, stated by the audit and not invented here: Mesa is used only as a vestigial
base class — no scheduler, no `AgentSet`, no `shuffle`, plain-list iteration at `engine.py:152` and `:159`;
it materialises a second `random.Random` whose seeding on the API path comes from entropy; it pulls a
large Jupyter/matplotlib dependency tree; and it introduces a `Model.rng` attribute collision on any
future 3.x upgrade. Against that, "Mesa buys credibility as a recognised ABM framework, and `ADR-002`
cites that." (`CURRENT-STATE-AUDIT.md:405`.)

Status derivation: no Mesa decision appears in `HANDOFF.md`, `CHARTER.md` or `NOTICE.md` — the only
occurrence in HANDOFF is an install instruction at `:49`. See also AS10 and AS12.

### DEC4 — How honest the public reproducibility claim should be · **SETTLED**

**Decision.** The audit's option (a), conditional restatement. The exact wording to use, per founder
decision:

> "The existing stubbed execution path reproduces the same tested numeric outputs when the seed, scenario
> and stubbed agent outputs remain identical."

And the **target** contract, which must always be labelled a target and never presented as a delivered
capability:

> "Given the same scenario version, rule-pack version, seed, ordered player inputs and recorded
> external-agent inputs, the engine is intended to reproduce identical authoritative state hashes."

**Recorded at:** `HANDOFF.md:52-62`. Options considered at `CURRENT-STATE-AUDIT.md:407`.

**Note — what is *not* settled here.** HANDOFF records a decision on the wording only. It says nothing
about the disposition of the audit's options (b) (build record/replay) or (c). P0.6 does schedule
record/replay foundations (`HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`)), but whether that constitutes acceptance of option (b), or
is unrelated to it, is not stated anywhere in the tree and is not decided here. Posed to the owner as OQ5.

R1 bears directly on how durable even the conditional claim is.

### DEC5 — Whether to adopt uv and `pyproject.toml` · **OPEN**

> **Question for the owner:** Should packaging move to `pyproject.toml` with a hash-pinned lockfile
> (uv or otherwise), or should the flat `requirements.txt` remain?

Constraints on the record: the flat file with open ranges and no lockfile is the direct cause of the
broken install and of the reproducibility caveat; migrating would fix both but changes four documented
workflows (`README.md:56-57`, `scaffold/README.md:58`, `:69-70`, `scaffold/CLAUDE.md:33`) and the
Dockerfile — "worth doing, but it is a deliberate migration, not a fix to slip in"
(`CURRENT-STATE-AUDIT.md:409`). *Re-anchoring note: the audit cites the last of these as a bare
`CLAUDE.md:33`; there is no `CLAUDE.md` at the repository root (`ls CLAUDE.md` → No such file). The file is
`scaffold/CLAUDE.md` and the line number is correct. This is an instance of the drift recorded at I7.*

Status derivation: `HANDOFF.md` contains no occurrence of "uv" or "pyproject". P0.2 commits only to the
outcome — "Remove/optionalise LiteLLM. Pin supported Python. Clean-environment command that succeeds on
Windows and Linux" (`HANDOFF.md:72-74`) — and leaves the tool choice unmade. The status quo is unchanged
in the tree: no `pyproject.toml`, and `litellm>=1.34,<2.0` still at `requirements.txt:20`. See R6 and D6.

### DEC6 — Dual-use and responsible-use policy for the influence-operations model · **SETTLED**

**Decision taken: 18 July 2026. Recorded here 19 July 2026.** This entry was OPEN in the original draft
of this register and is no longer a question for the owner. It is publication blocker B5 and Phase 0 item
P0.8.

**Decision.** For the public MVP, eight controls govern the influence-operations model. They are recorded
in the founder's own terms and are **not** reworded into a summary:

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

**The identity and bias distinction, as the decision states it.**

> **Permitted:** identity affects lived experience, relationships, discrimination, institutional access,
> media exposure and cultural interpretation.
>
> **Not permitted:** identity acts as an inherent competence, morality, loyalty, violence or
> manipulability coefficient.

The campaign model **may** use non-sensitive factors — geography, institutional affiliation, economic
exposure, political behaviour, media consumption — where justified by the fictional scenario. It **must
not** optimise against protected traits.

**Why the audit's option list no longer frames this.** `CURRENT-STATE-AUDIT.md:411` offered four
options — an acceptable-use restriction in the licence; an enforced fictional assertion plus a real-entity
check; surfacing `fiction_disclaimer` everywhere; or staying private — and noted they were not mutually
exclusive. The decision is broader than any of them and reorders their standing: control 8 makes the
licence-side and disclosure-side options *supplementary*, and makes the technical measures *mandatory*. A
reader coming to this entry from the audit should not treat that option list as the live menu.

**Consequence, stated plainly because it enlarges the gate.** DEC6 being settled does **not** clear B5.
The decision replaces "B5 needs an owner decision" with "B5 needs eight controls implemented and
verified". **Nothing in the eight is implemented.** The register's earlier framing — that four blockers
clear by telling the truth and only B5 needs a decision — is now wrong in its second half, and R3, D1 and
`PUBLICATION-EXIT-CRITERIA.md` C6 have been re-pointed accordingly. B5 was the cheapest-looking blocker to
close and is now the most expensive.

**Recorded at:** the founder decision of 18 July 2026, cited by date rather than by `path:line` for the
same reason given under R1's evidence — it was issued directly and is not a file in the tree at the time
of this amendment. Replace this with a `path:line` citation once a source record exists.

**New decision surfaces this creates — OPEN, and not answered here.** See OQ6, OQ7, OQ8 and OQ9 in
section 6. The decision fixes *what* must hold; it does not fix how "real", "protected characteristic" or
"disclosed in the UI" are determined in code, and an agent may not settle those.

Current state of every candidate safeguard, verified — **this is the evidence that none of the eight
controls exists, not a description of partial compliance**: `NOTICE.md` contains no acceptable-use or
field-of-use term; there is no `fictional: true` assertion in any schema or model (a case-insensitive grep
for "fictional" across all `.py`/`.json`/`.html`/`.js` under `scaffold/` returns exactly one hit — the
scenario's own free-text disclaimer at `scenarios/kestral-strait.json:7`); scenario load performs a
path-existence check and `json.loads` with no entity or content validation
(`scaffold/backend/app/api/runs.py:21-26`); no disclaimer is surfaced in any of the **five** REST
responses (`scaffold/backend/app/api/routes_simulation.py:47-49` `create_run`, `:60` `advance`,
`:71-77` `get_state`, `:101` `submit_decision`, `:111` `get_events` — an earlier draft said four,
omitting `submit_decision`; see `CORRECTIVE-BACKLOG.md` CB-33); and the frontend contains
no fiction, provenance, AI-generated or disclaimer text at all (`scaffold/frontend/` holds exactly one
file, `index.html`; a case-insensitive grep for those four terms across it returns zero hits). The charter's own third bullet — a visible provenance tag on AI-generated text at the
interface level (`CHARTER.md:141-142`) — has no implementation; the only marker is a literal prefix inside
the stub briefing string, `[STUB briefing — tick {tick}]` (`llm_gateway.py:100`, within the return
expression spanning `:99-103`; the file is 103 lines).

Two further facts bear on controls 2 and 5 specifically. There is **no `world_mode` field** in any schema,
model or scenario file — the nearest thing is the free-text `fiction_disclaimer` cited above, which is not
a mode, is not validated, and is read by nothing. And the schema **can currently express** targeting by
`religion_majority` and `primary_language` (`agent_schema.py:22-28`) alongside three persuadability
scalars (`:72-77`); those fields drive no campaign logic today, but control 5 governs what they may ever
be used for and control 4 governs who may ever be targeted. Neither control is expressible as a schema
comment: both need an enforced check.

See R3, D1 and OQ6–OQ9. **The policy is settled; the enforcement is not built.**

### DEC7 — Whether `PLAN.pdf` remains the canonical plan format · **OPEN**

> **Question for the owner:** Should `docs/PLAN.pdf` remain the canonical plan, or should markdown become
> the source with the PDF treated as a published artifact?

Constraints on the record: the PDF's prose extracts cleanly, its tables do not, and it cannot be
line-diffed in review (`CURRENT-STATE-AUDIT.md:413`).

One premise of the audit's argument has lapsed independently of any decision: the fourth constraint it
cited — "`backend/plan.txt` is already an uncontrolled duplicate of it inside the build context" — no
longer applies, because no `plan.txt` exists anywhere in the tree. `docs/PLAN.pdf` remains. The other three
constraints are untouched by that.

Status derivation: `HANDOFF.md` contains no occurrence of "PLAN.pdf" or "plan.txt", and no plan-format
decision appears in the settled-decisions section. See AS7 and AS12.

### DEC8 — Which deterministic-randomness architecture P0.4A adopts · **OPEN**

*Appended 19 July 2026. Not a `CURRENT-STATE-AUDIT.md` §8 item; it arises from the founder decision of
18 July 2026 that created P0.4A.*

> **Question for the owner:** Should P0.4A use stateful named substreams, or keyed / counter-based
> deterministic draws?

**Plain English.** Two designs would both fix the contamination in R1. One keeps a separate, named
generator per subsystem, entity, interaction and purpose, each carrying its own position in its own
sequence. The other keeps no per-stream position at all and instead computes each draw from a key — the
run seed plus identifiers for what the draw is for — so the same key always yields the same value
regardless of what else happened first. They differ in how they behave under replay, branching and
out-of-order execution, and the choice is not reversible cheaply once code depends on it. The founder
decision requires an ADR that picks one deliberately, and requires that ADR to state explicitly that
ordinary sequential calls to a single shared PRNG are **rejected** for authoritative behaviour.

**Constraints on the record.**

- A drafted requirement already exists and leans toward keying: `docs/world-model/ENTITY-ONTOLOGY.md:546-555`
  specifies S-1 to S-4, including that an entity's generation draws come from a substream "deterministically
  derived from `(run_seed, entity_id, purpose)` and from nothing else". **That is a drafted recommendation in
  an AI-drafted specification, not an approval, and it is recorded here as open precisely so that it is not
  mistaken for one.** The same document states the position directly: "**No agent may make this call**"
  (`:561-562`).
- Selecting either approach supersedes an accepted ADR. ADR-007 records one seed threaded to one
  `random.Random`, with "All engine, agent, and diffusion randomness draws from that one RNG"
  (`scaffold/docs/ARCHITECTURE_DECISIONS.md:60-67`). The audit relied on that when it graded the shared
  stream as a caveat rather than a defect (`CURRENT-STATE-AUDIT.md:320`). Whether the new ADR supersedes
  ADR-007 or amends it is part of this decision and is not settled here.
- `HANDOFF.md` § Standing constraints (`:139-140`) requires human approval for architecture decisions and for "anything affecting
  determinism or authoritative state". This is both.
- One constraint is *not* open, and is not restated as a question: the founder decision fixes P0.4A's
  placement, its scope and its exit criteria. Only the approach is open.

Status derivation: no **approved** deterministic-randomness ADR exists — the ADR log is
`scaffold/docs/ARCHITECTURE_DECISIONS.md`, whose nine entries end at ADR-009 (`:77`) and include no
randomness decision other than ADR-007. A drafted candidate was written on 19 July 2026 at
[`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md):
it recommends **keyed / counter-based deterministic draws** and states the required rejection of
sequential shared-PRNG use, but its Status is *Proposed*, it was drafted by an AI agent and its
Approval block is empty, so **it does not answer this question** — a recommendation is not a
selection, and `HANDOFF.md` § Standing constraints (`:138`) forbids an agent approving its own record. Note also that ADR-010
records "Supersedes: None" and would narrow ADR-007 rather than supersede it, which is the second
bullet above and remains part of this decision. See R1, D13 and AS10;
AS10 (unverified Mesa RNG behaviour) sits underneath this in the same way it sits under DEC3.

**Not answered here.**

---

## 6. Open questions arising from this register

None of these is a section-8 item; all surfaced while compiling or revising the register, and all need an
owner, not an agent. They are recorded here rather than resolved in the entries that raised them.

- **OQ1 — Was `NOTICE.md:11` ("The source code is publicly visible for evaluation and portfolio
  purposes") intended as a statement of present fact, or as a description of the intended
  post-publication position?** It reads in the present indicative and contradicts `HANDOFF.md:13`. The
  correction differs depending on the answer, so it is not corrected here. See I6.
- **OQ2 — Given DEC1 (no licence, all rights reserved), should a `LICENSE` file nonetheless exist so that
  tooling can detect the position?** The audit's sub-instruction at `CURRENT-STATE-AUDIT.md:401` assumed a
  licence would be selected; DEC1 settled that none will be. Whether an all-rights-reserved position
  should still be expressed as a detectable file is a separate question. See I12.
- **OQ3 — May the closed broad audit be edited in place to re-point its drifted citations?** I7 records
  confirmed drift: dead `plan.txt` anchors, `README.md` line numbers that no longer match, a `COPYRIGHT.md`
  that does not exist, and a "no `.git`" clause that is now false. The findings themselves are unaffected.
  But the standing constraint records the audit as closed, and whether "closed" permits editing its
  evidence lines — versus appending a dated erratum, versus leaving it untouched with the drift recorded
  only in this register — has consequences for the audit's evidentiary standing. That is a governance
  call for the owner. This register has not edited the audit and does not recommend a route.
- **OQ4 — Is DEC1 (no licence, all rights reserved) intended as final, or as an interim position?**
  `HANDOFF.md:22-23` states it without qualification; `NOTICE.md:16` and `:41-43` describe the recorded
  position as under review and not final. Both are quoted verbatim under DEC1. Which reading governs
  determines whether NOTICE's "under review" wording should stay, and this register has not chosen.
- **OQ5 — Is P0.6 intended as the owner's route to the audit's option (b) (build record/replay), or is
  option (b) still undecided?** DEC4 settled the *wording* of the reproducibility claim only. Nothing in
  the tree states what became of options (b) or (c). See DEC4.

**OQ6–OQ9 were appended on 19 July 2026.** They arise from DEC6 and are questions about *how* the eight
controls are enforced, not about whether they apply. The decision itself is settled and none of these
reopens it.

- **OQ6 — By what test is an entity determined to be "real" for control 4?** The control forbids real
  persons, organisations and political populations as influence targets. It does not state the detection
  method, and the three candidates differ enormously in cost and in failure mode: a maintained denylist
  (fails open on anything not listed), a scenario-author attestation (fails open on a dishonest or
  careless author), or human review before a scenario is admitted (does not scale, but does not fail
  open). Control 8 requires technical enforcement, which rules out attestation *alone*. Nothing in the
  tree implements any of the three; `load_scenario` (`scaffold/backend/app/api/runs.py:21-26`) performs a
  path check and `json.loads`.
- **OQ7 — Which attributes count as "protected characteristics" for control 5, and what happens to the
  fields that already exist?** The schema declares `religion_majority` and `primary_language`
  (`agent_schema.py:22-28`). Control 5 forbids optimising persuasion against protected traits; the
  permitted/not-permitted distinction in DEC6 explicitly *allows* identity to affect media exposure and
  cultural interpretation. Those two readings can coexist, but only if the enforced list is written down
  and the boundary between "affects lived experience" and "is an optimisation criterion" is made
  mechanical. Whether enforcement means removing fields, gating their read sites, or asserting invariance
  in tests is unresolved.
- **OQ8 — How is control 7's UI half verified?** The API half is contract-testable across the five REST
  endpoints. A rendered interface disclosure is not verifiable by any command, and this register does not
  invent a proxy for it. What evidence counts as proof that the UI discloses fictionality?
- **OQ9 — Does implementing the eight controls fall inside or outside the standing "documents only, no
  edits under `scaffold/`" constraint, and what authorises the change?** Controls 1–5 and 7 cannot be
  satisfied without code and schema changes under `scaffold/`. This is the same class of question as the
  one already recorded against CB-17 in `CORRECTIVE-BACKLOG.md`. Recording the decision is authorised;
  building against it is not authorised by the decision itself, which states that no feature
  implementation is authorised by it.

---

## 7. Register maintenance

- Entry IDs are stable. If an entry closes, mark it `CLOSED` with the evidence that closed it; do not
  delete it and do not reuse the ID.
- **Amendment of 19 July 2026 (P0.4A).** The founder decision of 18 July 2026 was applied to this
  register: R1 gained P0.4A as its owning workstream, D3 and D5 were re-graded from inferred to
  documented, D10–D13 were appended, and DEC8 was appended as an open decision. Nothing was renumbered
  and nothing was deleted. The decision itself is cited by date rather than by `path:line` because it is
  not a file in the tree — see the note under R1's evidence — and that citation should be replaced with a
  `path:line` reference once a source record for it exists.
- **Amendment of 19 July 2026 (B5 / DEC6).** The founder decision of 18 July 2026 settling the dual-use
  position was applied: DEC6 moved from OPEN to SETTLED and now records the eight controls verbatim; R3
  was re-pointed from "awaiting a policy position" to "awaiting enforcement" and stays OPEN; D1's type
  changed from *Owner decision* to *Implementation + verification* and stays BLOCKING; the section-5
  preamble counts were adjusted; and OQ6–OQ9 were appended. Nothing was renumbered and nothing was
  deleted. **Settling DEC6 did not close R3, D1 or blocker B5** — it changed what closes them, from
  writing to working code. Any reader carrying forward the phrase "only B5 needs a decision" from
  `HANDOFF.md` § Publication exit criteria (`:104-105`) or `A3-VERIFICATION-RESULTS.md:247` is quoting a superseded framing.
- **Amendment of 19 July 2026 (ownership-and-evidence sweep).** AS2–AS14 carried no `Owner` field while
  AS1, R1–R9, I1–I13 and every dependency row did. The register's own convention
  (`All owners are recorded as Aries Russell (unassigned)`, stated under "How to read this document") was
  applied to the thirteen, so the field is now present on every entry. **No owner was assigned and none was
  invented**; `unassigned` is the recorded state, not a delegation. Nothing else in section 2 was touched.
  Two gaps were found and deliberately **not** closed, because closing them requires drafting rather than
  applying a stated convention: **(i)** DEC1–DEC8 still carry no `Owner` field — they name the
  decision-maker in prose ("Question for the owner") but not as a field; **(ii)** issues I1–I13 do not
  cross-reference the `CORRECTIVE-BACKLOG.md` entry that would close each one, and the backlog does not
  systematically reference this register — as at 19 July 2026 the register cites three `CB-` IDs
  (CB-17, CB-26, CB-33) and the backlog cites two entries of this register in return (I5 in CB-13, DEC8 in
  CB-34), against 13 issues and 47 backlog entries. An issue and the work item that closes it therefore
  cannot generally be traced to one another.
- **Amendment of 19 July 2026 (Track C gates).** The founder Track C correction of 19 July 2026 was
  applied: R10 was appended as the fixture-labelling risk, and D14–D19 were appended recording gates
  C0–C4 and the critical-path relationship P0.4 → P0.4A → P0.5 → P0.6. Nothing was renumbered and nothing
  was deleted. **No Track C work exists in the tree**; every appended row is a target with an unlock
  condition, and none should be read as progress. The correction is cited by date rather than by
  `path:line` because it is not a file in the tree — the same treatment as the founder decisions of
  18 July 2026 — and that citation should be replaced with a `path:line` reference once a source record
  exists. Two things were deliberately **not** settled: which fixture-label wording governs, the
  founder's or the one in the untracked UI drafts (R10); and whether `PHASE-0-REMEDIATION-PLAN.md`,
  `CORRECTIVE-BACKLOG.md` and `PUBLICATION-EXIT-CRITERIA.md` should carry Track C entries of their own,
  which is a question for the owner and not for the register that raised it.
- Any new entry must carry both layers — plain English and a `path:line` citation or a reproducible
  command — before it is added.
- **Statuses in this register are as at commit `71fa329`, the only commit, checked on 19 July 2026.** The
  working tree is *not* clean: it carries untracked Phase B governance documents under `docs/delivery/`,
  `docs/design/`, `docs/safety/` and `docs/world-model/` (`git status --short`), and no tracked file is
  modified. Re-verify before relying on any status; several entries in the source audit are already stale
  for exactly this reason (see I7), and at least one entry in this register was stale within a day of
  drafting for the same reason.
- This register does not open new investigations. Where it records something the grounding pass could not
  establish, it records it as an Assumption rather than resolving it.
