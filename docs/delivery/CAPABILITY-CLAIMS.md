# CAPABILITY CLAIMS — corrected register

**Status:** DRAFT. Pending owner review. Drafted by an AI agent; not approved.
**Date:** 19 July 2026
**Applies to:** commit `71fa329`, the single commit on `main`.

---

## Plain-English layer — what this document is for

MERIDIAN's worst defect is that its documents claim properties its code does not have. This register
exists so that nobody — including a future version of the founder, an AI agent, or a marketing page —
has to guess what is safe to say.

The rule is simple. **If you want to describe what MERIDIAN does, copy a sentence out of the
"accurate today" column of the table below, verbatim.** If the sentence you want to write is not in
that column, it has not been cleared, and you must either verify it yourself against the code or not
write it. If it appears in the "not permitted" column, it is known to be false or known to overstate,
and it must not be written anywhere — not in the README, not in a pitch, not in any external
description of the project.

Three columns describe reality; the fourth describes intention. The fourth column is always a
**target**. A target is a thing MERIDIAN is meant to become. It is never evidence of a thing MERIDIAN
is. Targets must always be written with the word "target" or "intended" attached, and never in the
present indicative.

This is deliberately the most conservative document in the repository. Where a phrase is arguably an
overstatement, it has been put in the not-permitted column rather than the accurate column. That is
the intended bias. An honest "we have not verified this" is a correct outcome here.

**Status of that rule.** The register is written in the imperative because that is how a clearance
list has to read to be usable. It is not yet in force. Whether this document becomes the authority
other documents are corrected against is OQ-5, and the owner has not answered it. Until then, treat
the table as a drafted recommendation: safe to rely on for what it *permits*, not yet binding for
what it *forbids*.

---

## Standing prohibitions

### In force — founder-set, non-negotiable

`HANDOFF.md` § Standing constraints (`:135`), quoted in full and without expansion:

> Do not describe the codebase as execution-ready, replay-capable or fully deterministic.

Note the exact scope: it governs **descriptions of the codebase**. It names three phrases. It does
not, on its face, extend to descriptions of other artefacts (such as `docs/PLAN.pdf`), nor does it
enumerate paraphrases.

A second prohibition follows from `HANDOFF.md:24`: **do not name the employer or job advert that
inspired the project**, in this or any other document.

### Proposed by this draft — NOT in force, owner decision required

The following is drafter-authored hardening, not founder text. It is recorded here as a proposal so
that it is not mistaken for a standing constraint. See OQ-7. **Do not apply it mechanically until
the owner has ruled.**

- That the three prohibitions extend beyond documents to commit messages, interface strings and
  external communications.
- That qualified constructions ("essentially deterministic", "deterministic in practice",
  "replay-ready", "ready to execute") are covered, on the reasoning that they leave a reader with
  the belief the constraint exists to prevent.
- That the prohibition attaches to the reader's takeaway rather than to the literal three phrases.

The drafter's view is that all three are the right reading of the founder's intent. That view is a
recommendation, not an authority.

---

## How to read the table

- **Claim area** — the subject being described.
- **Accurate today** — wording cleared for use. Copy verbatim.
- **Not permitted, and why** — wording that is false or overstates, with the reason.
- **Target (not delivered)** — the intended future capability, always labelled as such.

**Provenance of the targets.** Only C1's target is founder-settled wording (`HANDOFF.md:59-62`).
C7, C8, C9, C12 and C13 restate a `HANDOFF.md` P0 item and cite it. The targets in C2, C3, C4, C5,
C6, C10, C11, C14 and C15 are **drafter-composed** — they are the drafter's reading of what the
corresponding gap implies, not founder-stated intent, and some of them (notably C10's "strict mode
that raises on unknown or unreachable effect keys" and C3's boundary-guard specification) are
specific engine design commitments. Defining what MERIDIAN is meant to become is the owner's call.
If OQ-5 is answered yes, these drafter-composed targets should be reviewed one by one before they
become the repository's stated intentions by default.

Row identifiers `C1`–`C15` are stable. The technical-evidence layer for each row is in
[§ Evidence](#evidence-layer), keyed by the same identifier.

---

## The register

| # | Claim area | Accurate today — copy verbatim | Not permitted, and why | Target — **not a delivered capability** |
|---|---|---|---|---|
| **C1** | Reproducibility / determinism | "The existing stubbed execution path reproduces the same tested numeric outputs when the seed, scenario and stubbed agent outputs remain identical." *(Founder-settled wording. Use exactly this sentence; do not paraphrase, do not shorten.)* | *As a description of what the current codebase does:* "Fully deterministic." "Deterministic." "Same seed, same scenario, same decisions ⇒ identical numeric state." "Reproducible runs." — All omit the load-bearing condition that the agent outputs are held constant, which is the entire reason the current result holds. "Same decisions" is additionally misleading: submitted decisions do not reach the tick loop at all (C5). "Identical numeric state" overstates the test, which compares the final macro dictionary only and never compares cohort beliefs, narrative adoption, the event log or the snapshot history. **Scope note:** this row prohibits these phrases as *capability claims about the current codebase*. It does not rule on the design-principle bullet at `CHARTER.md:58`, which reads in full: "- **Reproducible** — same seed, same scenario, same decisions ⇒ identical numeric state." The audit-identified falsehood is the `⇒` clause, but it is not separable by line from the principle heading — both are on `:58`, the sixth of seven bullets in the list running `:52-59`. So the clause cannot be corrected without editing a design-principle bullet of the governing document. Whether that is permitted at all, and whether the bullet reads as stated intent or as a capability claim, is OQ-6 and is not settled here. | **TARGET, not delivered:** "Given the same scenario version, rule-pack version, seed, ordered player inputs and recorded external-agent inputs, the engine is intended to reproduce identical authoritative state hashes." *(Founder-settled target wording. Always carry the label.)* |
| **C2** | Determinism boundary — LLM never mutates authoritative state | "In the current scaffold no language model is called: no module under `scaffold/backend/app/` imports a model client or any HTTP client, the gateway imports only `annotations`, `typing` and `ActionProposal`, and the only `litellm` text in the module sits inside its docstring. The gateway's two public functions are a role-lookup table and an f-string. The gateway returns proposal objects and text strings and imports no state object. Every write to macro numeric state is made from `engine.py`: two delta applications routed through the single `apply_deltas` function in `agents/macro_state.py` (`engine.py:136`, `engine.py:164`), plus one direct assignment of the tick counter (`engine.py:179`) that does not pass through `apply_deltas`. The one meso write in the codebase, a decrement of `government_competence`, is made in `agents/cohort_agent.py`, not by the gateway. There is no structural guard preventing a model call path from being added: `config.py:23-25` already declares an `llm_mode` setting ("stub" or "live") and an `llm_model` value, and `llm_mode` is read at exactly one place, the health endpoint that echoes it (`main.py:45`)." | "Enforced in code and guarded by a test." "The LLM never directly mutates macro or meso numeric state" *stated as a proven property of a running system.* — The boundary is currently trivially satisfied because no model is invoked at all, so it has never been exercised against a real model. "Guarded by a test" overstates what the test does (C3). "Guarded in CI" is false outright (C9). | **TARGET, not delivered:** the boundary is intended to be enforced structurally and verified by a check that would fail if a gateway acquired a write path to authoritative state, including when a real model is connected. |
| **C3** | What the boundary test proves | "`test_llm_gateway_cannot_write_state` calls the stub gateway once and asserts that the returned object is an `ActionProposal` and that this object has no attribute named `apply_deltas` and no attribute named `macro_state`." | "Guards the determinism boundary against regression." "Proves the LLM cannot write state." "Structural check of the determinism boundary." — The test inspects two literal attribute names on a returned value. It performs no import-graph analysis, attempts no mutation, never touches `MacroState`, and exercises no real model. A gateway that mutated authoritative state by any other route would pass it unchanged. | **TARGET, not delivered:** a boundary guard that fails when the gateway package gains any import of, or reference to, an authoritative-state object, and that runs on every change. |
| **C4** | Legality and feasibility validation | "The engine does not check legality or feasibility. `_validate_and_price` looks the proposed action type up in a fixed seven-entry table and returns a copy of the constant effect found there. It is never passed the agent specification, so an agent's declared constraints cannot be consulted." | "The engine validates legality and computes cost/effect." "Engine rejects invalid actions." "Priced, validated and resolved by the engine." "Hard legal/procedural constraints on the agent." "Accepts, rejects, or scales." — No legality check, no feasibility check and no cost computation exists. Scenario constraints were proven causally inert by substitution: a 40-tick state hash is identical with and without them. | **TARGET, not delivered:** an evaluator that reads the agent specification and the scenario's constraints, and can reject or scale a proposal. **Note:** publication blocker B1 clears by correcting the text. Building the evaluator is *not* required for publication. |
| **C5** | Player decision path | "`POST /runs/{id}/decision` appends the submitted decision to an in-memory event list and returns a 200 response whose body reports `accepted: true` unconditionally once the run id resolves (`routes_simulation.py:101`). It applies no effect, and the tick loop never reads the event list, so a submitted decision cannot influence any later tick. The client's own `legal_check` value is stored and echoed back unexamined." | "Player decisions are parsed into `Intervention` objects — the engine validates and prices them." "The engine records it; validation/pricing happens on tick." "Player decision interpretation: LLM parses input into a schema-validated `intervention` object; engine rejects invalid actions." — Nothing is validated at submission or on any later tick. The endpoint accepted an actor role of `janitor_with_no_authority` and an action of `nationalise_every_foreign_asset_and_declare_war` with a 999,999,999 resource cost, returned 200, and changed no state. | **TARGET, not delivered:** player intent compiled into engine primitives, priced and validated by the engine, with the resulting effect applied on a defined tick. |
| **C6** | Persistence | "Nothing is written to a database. Three SQLAlchemy model classes are defined and are instantiated nowhere; no session write call exists anywhere in the scaffold. The only database operation attempted is table creation at start-up, inside an exception handler that logs a warning and continues, so the application starts identically with or without a database. All run state lives in an in-process dictionary that does not survive a restart." | "We persist three things: `simulation_run` (seed + scenario), immutable `state_snapshot` per tick, and an append-only `event_log`." "Three tables capture the reproducibility contract." Any architecture diagram terminating in "PostgreSQL (simulation_run, state_snapshot, event_log)" without a "planned" qualifier. — Stated in the present indicative as delivered behaviour; it is not implemented. | **TARGET, not delivered:** durable per-run persistence of seed and scenario, immutable per-tick snapshots and an append-only event log, written through a single transition point. |
| **C7** | Replay | "There is no replay capability. No mechanism exists to restore a run from a snapshot, no state hashing exists in the engine, schemas or scenario code (searched: `scaffold/backend/app`, `scaffold/scenarios`, `scaffold/schemas`), and the random number generator's internal state is never captured. Snapshots are dictionaries held in memory for the life of the process." | "Replay-capable." — Prohibited by the founder-set standing constraint at `HANDOFF.md` § Standing constraints (`:135`), which names this phrase. There is no restore path, no hash to compare against and no captured generator state, so no run can currently be replayed even in principle. **Drafter-proposed, NOT in force:** "Replayable runs." "Replay-ready foundations." These are drafter-formulated phrase-classes. Neither appears anywhere in the repository, neither is named at `HANDOFF.md` § Standing constraints (`:135`), and extending the prohibition to qualified constructions is exactly the hardening the standing-prohibitions section holds out of force pending OQ-7. They are recorded as a recommendation, not as a prohibition in force. See OQ-8. | **TARGET, not delivered:** replay that reconstructs authoritative state from recorded inputs and makes zero model or network calls (`HANDOFF.md` P0.6). Separately, and expressly **deferred — `HANDOFF.md` § Backlog (`:128`) marks it "expands `ExternalAgentInput`, do not implement in Phase 0"** — every text turn, transcript, uploaded file, map selection and confirmation is intended to become a versioned external input that replay preserves. |
| **C8** | Cross-tier causal coupling | "No tier reads another tier's state. Perturbing macro indicators leaves cohort beliefs and narrative adoption unchanged; changing cohort belief values by two orders of magnitude leaves macro state unchanged. Adding or removing a cohort *does* change macro numbers, but not causally: a cohort draws from the shared random stream only when it has grievances, so changing how many cohorts have grievances shifts every later draw in the same stream. In the shipped `kestral-strait` scenario, all six institutional agents map to a non-empty effect entry, so each writes to macro state on every tick — this is arithmetic over the role table and that one scenario file, not an executed count; an agent whose role is not in the stub's table resolves to `observe`, whose effect entry is empty, and writes nothing. Where that write occurs, it is not a causal channel: the action choice is a fixed lookup on the agent's role that reads no state at all, so it is a one-way open loop in which each action type maps to one constant, applied immediately and in full, with no cost, delay, prerequisite or reversal. The micro tier was never perturbation-tested." | "Every action creates second- and third-order effects." Any description of the observed meso→macro movement as evidence that the tiers interact. — The apparent macro↔meso coupling is shared-stream contamination, not a modelled cause. Presenting it as causality would be the single most misleading claim available about this codebase. **The micro→macro write is real and may be stated** — but never as modelled causality, and never as evidence that the simulation propagates effects: it is a constant-effect table lookup. **Drafter-proposed, NOT in force:** "Macro and meso are coupled." No such sentence exists anywhere in the repository; it is a drafter-formulated phrase-class recorded as a recommendation. It is substantively contradicted by the perturbation evidence below, but it is not an identified claim. See OQ-8. **Withdrawn from this column:** an earlier draft listed "Crises propagate through populations, media, networks and institutions." Its only source is `HANDOFF.md` § Backlog (`:112-114`), which is founder text under the heading "Backlog — captured, deliberately not started", written in the imperative as a requirement ("Crises **must** propagate through populations, families, media, networks, markets, political organisations, foreign publics and institutions") — not as a claim of current capability. The earlier draft rewrote it into the present indicative and truncated its list. Prohibiting it would risk reading as prohibiting the founder's own stated target. Raised as OQ-8 instead. | **TARGET, not delivered:** explicit, named cross-tier causal channels with no arbitrary coupling, in which `represents_population` genuinely affects aggregation (`HANDOFF.md` P0.5). Related target, and a **prerequisite of P0.5's implementation rather than a sibling of it**: deterministic randomness isolation, so that adding a draw in one subsystem cannot silently perturb another. That is **P0.4A**, a Phase 0 workstream created by founder decision of 18 July 2026 and ordered `P0.4 → P0.4A → P0.5 → P0.6` (`PHASE-0-REMEDIATION-PLAN.md` §P0.4A). The mechanism — stateful named substreams or keyed / counter-based deterministic draws — is an unmade owner decision, so no record may claim substreams as the chosen target. |
| **C9** | Continuous integration | "Hosted CI passes on GitHub Actions `windows-latest` with CPython 3.12.10." *(Updated 19 July 2026 — superseding "There is no continuous integration", which was true until the first hosted run. Evidence: run `29699943680`, commit `5d37100`, Windows Server 2025, 62 passed. See `P0-3-CI-STATUS.md`.)* The workflow installs via the two documented commands, runs an import smoke test, a bounded packaging check and the test suite. | "MERIDIAN has CI" *stated without qualification.* "Cross-platform CI." "Tested on Linux/macOS." "`test_llm_gateway_cannot_write_state` guards in CI" *in the sense that the determinism boundary is protected* — CI runs the tests that exist, and that test remains the shallow attribute check described in C3; running a weak test on a hosted runner does not make it a strong test. No lint, type, coverage or performance gate exists, so no claim about code quality follows from CI passing. | **TARGET, not delivered:** a boundary guard that fails when the gateway acquires a write path to authoritative state; checks on more than one OS and Python version; a lockfile so two runs resolve identically. |
| **C10** | Archetype extensibility via JSON | "Scenario loading performs a path-existence check and a `json.loads` with no content validation, and each cohort record is then parsed through Pydantic. `engine.py` contains no archetype-specific branch: `scenario_id` occurs there only as a value that is read and stored (`engine.py:52`, `:86`), never as a condition. This was checked in `engine.py` only, not across `agents/`, `diffusion.py` or the schema layer. **Whether a second scenario file loads and completes a run has not been tested — only one scenario file exists in the tree, and no second scenario was constructed or run.** What is directly verified is that most scenario content is read by no code: population weight, demographics, media exposure, campaign data and the fiction disclaimer are parsed and then never consulted. Two archetypes that differ only in those fields will behave identically, and nothing reports this. The engine's only effect-application path silently skips any key it does not recognise and any value that is not a top-level number, so an effect that never applies produces no error and no warning." | "Nation archetypes are data, not code. Adding one means adding a scenario-template JSON that conforms to the existing schemas — never editing the engine." "Adding an eighth archetype must require only a new `scenarios/*.json`." "Nation types are data, not code." — Unverified as a claim that a second file loads and runs, since no second file was ever built; false as a claim that the archetype's content shapes behaviour. The failure is silent, which is what makes the claim harmful rather than merely optimistic. | **TARGET, not delivered:** archetype content that causally drives behaviour, with a strict mode that raises on unknown or unreachable effect keys instead of skipping them. |
| **C11** | Test suite scope | "The test suite is five tests in a single file. Every assertion in it concerns macro state, tick counts or object attributes. One test advances five ticks and checks the tick counter and snapshot count. One compares two same-seed runs' final macro dictionaries. One asserts two different-seed runs' final macro dictionaries differ. One asserts a single indicator's value changed over twenty ticks, without asserting direction, magnitude or bound. One is the boundary test described in C3." | "The test suite is the point: `test_same_seed_is_deterministic` proves reproducibility." "Determinism + boundary tests." "A passing test suite" offered as evidence of correctness. — The suite contains no test of cross-tier causality, saturation or clamping, unknown-key handling, random-stream isolation, any API route, the decision endpoint, event-log contents, persistence, or restoring a run. The different-seed test cannot distinguish a modelled mechanism from a shift in the shared random stream. | **TARGET, not delivered:** tests that assert the authoritative-state contract across all three tiers, cover the API surface, and would fail on a determinism regression rather than absorbing it as expected divergence. |
| **C12** | Execution readiness | "The scaffold is a skeleton, not a finished product. Its five tests are recorded as passing in a hand-assembled environment that departs from the documented install in two ways: one declared dependency was deliberately omitted, and another was installed without its dependency tree to avoid a platform failure. The documented install path is itself recorded as failing on a clean machine, so the scaffold should not be described as runnable without naming that environment." | "Execution-ready." — Prohibited by the founder-set standing constraint at `HANDOFF.md` § Standing constraints (`:135`), which names this phrase. **Drafter-proposed, NOT in force:** "Production-ready." "Ready to run." Neither appears anywhere in the repository, neither is named at `HANDOFF.md` § Standing constraints (`:135`), and both are drafter-formulated phrase-classes recorded as a recommendation. See OQ-8. **Not ruled on here:** whether "runnable", unqualified, remains cleared. An earlier draft of this register removed it. That ruling has been withdrawn, because `A3-VERIFICATION-RESULTS.md:87-88` expressly classifies `scaffold/README.md:5-6`'s "a runnable skeleton, not a finished product" as "Permitted incompleteness" — a prior verification pass ruled on this wording and cleared it, and reversing that is not the drafter's to do. The evidentiary concern stands and is recorded: no code was executed while drafting this register, the environment the recorded pass came from no longer exists, and the documented install path is recorded as failing. The phrase is live at `README.md:28` and `scaffold/README.md:5`, so the answer has real correction consequences. Raised as a sub-question of OQ-5. Beyond that: no supported Python version is declared in machine-readable form (P0.2 requires pinning it), and no CI demonstrates that anything builds. **Not stated as defects here:** the absence of exact version pins and of a lockfile. Those are the substance of open audit decision §8 item 5 (whether to adopt `uv` and `pyproject.toml`) and are the owner's to settle, not this register's. | **TARGET, not delivered:** a clean-environment installation command that succeeds on both Windows and Linux, with the install-blocking dependency removed or made optional and the supported Python version pinned (`HANDOFF.md` P0.2). |
| **C13** | Outcome modelling | "Each action type maps to one fixed set of constant effects, applied immediately and in full. The action-effect table touches three national indicators in total. Separately, one seeded uniform draw per tick is applied to a fourth, `shipping_throughput_pct_of_baseline` (`engine.py:135-136`), and the tick counter is stamped at `engine.py:179`. The engine contains no cost, cooldown, decay, budget, prerequisite or reversal mechanism, and two indicators reach their clamp ceiling and stay there. Nothing evaluates a win or loss condition." | "The system models a **distribution**, rather than pretending there is one objectively correct future." (`CHARTER.md:61-62`, identified by the closed audit at §6.1 item 6.) "Deterministic rules + seeded Monte Carlo draws." (`README.md:36`, audit §6.1 item 3.) — There is no distribution: there is a constant per action. There is no Monte Carlo: there is a single uniform draw applied to one indicator per tick. Saturation persists under varied action selection, so it is an architectural gap rather than a tuning problem. **Withdrawn from this column:** an earlier draft also listed `CHARTER.md:59` ("Capable of producing unintended consequences"). That line is not in the closed audit's §6.1 set, not in the A3 corrections list, not among the five blockers, and not among P0.1's enumerated correction areas. Ruling on it would both expand the false-claims population and amend the governing document. It is raised as OQ-6 instead. | **TARGET, not delivered:** stochastic resolution over a distribution of plausible outcomes, with opposing mechanisms defined only after tick semantics and horizon are settled — explicitly **not** patched with arbitrary mean reversion (`HANDOFF.md` P0.7). |
| **C14** | Language-model feature surface | "The gateway module defines two public functions: one returns a proposed action type by looking the agent's role up in a fixed table, and one returns a formatted string built from three values in the mapping it is handed. Both are stubs. No model, no key and no network call is involved." | "LLM composes campaign content within a fixed schema." "Advisor dialogue, LLM-generated, grounded by retrieval over true state." "LLM parses input into a schema-validated intervention object." — These describe three functions that do not exist. There is no campaign-composition function, no decision-parsing function, and no retrieval of any kind: the briefing function reads three keys from a dictionary passed to it and interpolates them into a string. | **TARGET, not delivered:** model-backed proposal, briefing, campaign composition and intent parsing, each confined to the determinism boundary and versioned by model identifier, prompt version and temperature. **Note:** prompt versioning is currently a constant that no code reads, and neither model identifier nor temperature is logged anywhere. |
| **C15** | Fiction and dual-use safeguards | "The scenario file carries a free-text fiction disclaimer that no code reads and no interface displays. No schema asserts fictionality, no check runs at scenario load beyond parsing the file, and no API response or interface surface carries a fiction notice or a provenance tag. The governing licensing document states an all-rights-reserved position and contains no acceptable-use or field-of-use restriction." | "Every AI-generated advisory text carries a visible provenance tag distinguishing it from engine-computed fact, at the interface level and not merely in a documentation footnote." — No provenance tag exists at any interface. The only marker on generated text is a literal `[STUB briefing — tick N]` prefix inside the string itself. Do not present the charter's scope-and-honesty bullets as implemented controls; they are stated intentions. | **TARGET, not delivered. No longer gated on an owner decision — gated on implementation.** This is publication blocker B5, and it remains the only blocker that cannot be cleared by correcting text. **The decision it was waiting on was taken on 18 July 2026, and B5 did not clear with it.** The founder settled the dual-use position and named **eight controls**: influence mechanics only in explicitly fictional worlds; a scenario loader that requires `world_mode: fictional` and **fails closed**; real-world scenario import disabled; real persons, organisations and political populations not targetable; protected characteristics never optimisation criteria for persuasion or manipulation; fictional **aggregate** diffusion, exposure, adoption and counter-messaging still allowed; API and UI disclosing that the active world is fictional; and — governing the other seven — disclosure and any future acceptable-use language are **supplementary while technical enforcement is mandatory**. B5 therefore clears only when the eight are **implemented and verified**. **None of the eight exists in code.** An earlier draft of this row offered the audit's option menu ("enforced fictionality assertion … and/or acceptable-use terms") as alternatives; that menu is superseded — control 8 makes the licence-side and disclosure-side options supplementary rather than sufficient. Per-control criteria: `PUBLICATION-EXIT-CRITERIA.md` C6. |

---

## Claims that are settled and may be stated plainly

These are not capability claims and carry no evidential risk, but are recorded here so that nobody
reopens them:

- The founder **decision**, recorded at `HANDOFF.md:13-19`, is that the repository is private,
  deliberately, and becomes public only after the Phase 0 gates pass and the owner approves. The
  decision is settled; the remote's actual visibility **setting** has not been checked (no `gh`
  command was run, no network call was made — see inference item 7).
- There is no licence, deliberately. The all-rights-reserved position is recorded in `NOTICE.md`.
  Do not add an open-source licence.
- The default branch is `main`.
- Correct reproducibility wording is C1 above, in both its cleared and target forms.

**What is *not* settled.** Three items in the closed audit's §8 remain open and are recorded here so
that this section is not misread as the whole decision set: §8 item 3 (whether Mesa remains the ABM
substrate), §8 item 5 (whether to adopt `uv` and `pyproject.toml`), and §8 item 7 (whether
`docs/PLAN.pdf` remains the canonical plan format). None is resolved by this register.

---

## Open questions for the owner

These require a human decision. They are recorded, not resolved.

**OQ-1 — `NOTICE.md:11` states in the present indicative: "The source code is publicly visible for
evaluation and portfolio purposes."** The repository is private per `HANDOFF.md:13`. Was this
sentence intended as a statement of present fact or as a description of the intended
post-publication position? It currently reads as the same defect class this phase exists to
correct, inside the document that records the licence decision.

**OQ-2 — `README.md:27` and `README.md:80` describe `docs/PLAN.pdf` as "the full execution-ready
plan".** This describes the plan, not the codebase, and `HANDOFF.md` § Standing constraints (`:135`) on its face governs
descriptions of the codebase. Whether the constraint reaches this line is therefore a question about
the constraint's scope, and the drafter does not determine it: the register does not assert that
these lines are outside the constraint, only that the founder text does not name them. Does the
owner want the phrase changed
anyway, on the grounds that a reader encountering "execution-ready" beside a link to the scaffold may
reasonably carry it across? **This question is genuinely open**; the drafter-proposed hardening in the
standing-prohibitions section would decide it by default, which is why that hardening is marked as
not in force. Do not change these two lines until this is answered.

**OQ-3 — `README.md:96` links to `COPYRIGHT.md`, which does not exist.** The file holding that
position is `NOTICE.md`. It is the only broken link among the 16 markdown links enumerated in the
**tracked** files at commit `71fa329`, outside `docs/delivery`. The tree also currently holds
untracked documents that postdate that check — `docs/design/`, `docs/safety/`, `docs/world-model/`
and six sibling drafts in `docs/delivery/` — whose links this register has not examined. Two
options, neither preselected:
(a) re-point the link at `NOTICE.md`; (b) create a `COPYRIGHT.md`. Separately, the closed audit's
§8.1 carried a sub-instruction to "add the file so tooling can detect it" — there is still no
`LICENSE` file at the repository root, and no `NOTICE.md` equivalent that licence-detection tooling
recognises. The licence *decision* is settled (none, all rights reserved); whether a
tooling-detectable file should nonetheless exist is not, and is not resolved here.

**OQ-4 — ANSWERED 18 July 2026. Retained, not deleted, so the numbering holds.** This question asked
the owner to settle publication blocker B5 (row C15). **The owner settled it, and B5 did not clear.**
The decision is broader than the audit's option list and reorders it: the options this question put
forward — an acceptable-use or field-of-use restriction, an enforced fictionality assertion with a
real-entity check at load, surfacing the disclaimer everywhere, or staying private — are no longer
the live menu, because control 8 of the decision makes the licence-side and disclosure-side measures
**supplementary** and the technical measures **mandatory**. B5 now clears by **eight controls being
implemented and verified**, none of which exists in code. **This is not a question for the owner any
more; it is work nobody has started.** It is therefore no longer an open question in this register,
and a reader must not carry it forward as one. See row C15, and `PUBLICATION-EXIT-CRITERIA.md` C6
for the eight controls with a verifiable criterion each.

**OQ-5 — does this register become the authority that other documents are corrected against?** It is
drafted on that assumption but does not assume the answer: until the owner rules, the table is a
recommendation, not a binding clearance list (see the status note in the plain-English layer). If the
answer is yes, P0.1 correction work should cite row identifiers rather than re-deriving wording.

**OQ-5a — may this register reverse a clearance already made by the A3 verification pass?** The
concrete instance is the word "runnable". `A3-VERIFICATION-RESULTS.md:87-88` expressly classifies
`scaffold/README.md:5-6`'s "a runnable skeleton, not a finished product" as "Permitted
incompleteness" and not a publication blocker. An earlier draft of this register de-cleared it on
the drafter's own reasoning. That has been withdrawn, and C12 now records the evidentiary concern
without ruling. The phrase is live at `README.md:28` and `scaffold/README.md:5`. If the owner
answers yes to OQ-5, this sub-question needs answering with it, because it determines whether the
register sits above or below the prior verification record.

**OQ-6 — may `CHARTER.md` be edited, and where is the line between an aspirational governing
principle and a false capability claim?** This governs the scope of the whole register and is the
prior question behind rows C1 and C13. `CHARTER.md:3-5` self-declares the document non-negotiable and
governing over every other document. Three charter lines are in tension with the code:

- `CHARTER.md:58` — "same seed, same scenario, same decisions ⇒ identical numeric state". Identified
  by the closed audit; in scope for correction on any reading.
- `CHARTER.md:61-62` — "The system models a **distribution**". Also audit-identified (§6.1 item 6),
  so also in scope — but correcting it is still, in substance, an edit to the governing document.
- `CHARTER.md:59` — "Capable of producing unintended consequences". **Not** audit-identified, not in
  A3's corrections, not a blocker, not in P0.1's six areas. An earlier draft of this register ruled
  it impermissible. That ruling has been withdrawn, because making it would have expanded the
  false-claims population — which the standing constraints forbid — and amended the charter without
  the owner.

The owner's decision is needed on: (i) whether charter lines may be edited at all under P0.1; (ii) if
so, whether the test is "contradicted by the code" or the narrower "identified by the closed audit";
(iii) whether charter bullets read as *stated intent* (legitimate as written) or as *capability
claims* (must be corrected). Nothing in the charter should be changed until this is answered.

**OQ-7 — should the three standing prohibitions be hardened beyond `HANDOFF.md` § Standing constraints (`:135`)?** The founder
text names three phrases and governs descriptions of the codebase. An earlier draft of this register
presented a broader reading — extending to commit messages, interface strings and all external
communication, covering qualified constructions, and attaching to the reader's takeaway rather than
the literal phrases — as though it were founder-derived and non-negotiable. It is not; it is
drafter-authored, and it is now marked as such and held out of force. The drafter recommends adopting
it, but the extension is the owner's to make, particularly because OQ-5 would give this register
authority over other documents. Note that OQ-2 turns on the answer.

**OQ-8 — may this register prohibit wordings that appear nowhere in the repository and were not
identified by the closed audit?** Five entries in the not-permitted columns are drafter-formulated
phrase-classes rather than claims the repository actually makes: "Replayable runs." and "Replay-ready
foundations." (C7), "Production-ready." and "Ready to run." (C12), and "Macro and meso are coupled."
(C8). A repository-wide search finds zero occurrences of any of the five, and none is named at
`HANDOFF.md` § Standing constraints (`:135`). An earlier draft presented them as founder-set prohibitions; they are now marked
as drafter-proposed and not in force. A sixth, "Crises propagate through populations, media,
networks and institutions.", has been withdrawn from C8 altogether: its only source is founder
backlog text at `HANDOFF.md` § Backlog (`:112-114`), stated as a requirement under "deliberately not started" and
rewritten by an earlier draft into the present indicative. The owner's decision is needed on whether
this register may prohibit anticipated wordings at all, or only wordings the repository contains.
Note the answer interacts with OQ-7 but is not the same question: OQ-7 asks how far the founder's
three phrases extend, this asks whether the register may originate prohibitions of its own.

**OQ-9 — does the register narrow the founder-recorded critical finding, or does the owner?**
`HANDOFF.md:64-66` records, as one of the two founder-stated critical findings of the closed audit,
that "The three tiers never causally influence one another". A3's perturbation matrix covers only
macro→meso and meso→macro, and its own conclusion at `A3-VERIFICATION-RESULTS.md:167` is confined to
those two legs; the micro tier was never perturbation-tested, by A3 or here. Row C8 therefore does
not reproduce the founder's broader formulation verbatim, and states the micro leg as read from
source rather than as demonstrated. Declining to assert an unverified proposition is required of the
drafter. But whether a critical finding from a **closed** audit may be narrowed on that basis is a
judgement about the audit record, and it is the owner's to make, not the drafter's. Recorded here
rather than settled in the evidence layer.

---

## Evidence layer

File references are relative to the repository root **unless** they name a bare module or a partial
path — `engine.py`, `agents/macro_state.py`, `main.py`, `api/runs.py`, `llm_gateway.py`,
`diffusion.py`, `agent_schema.py`, `routes_simulation.py` and the like — in which case they are
relative to `scaffold/backend/app/` (or to `scaffold/backend/` for `tests/` and
`requirements.txt`). There is no `engine.py`, `agents/`, `main.py` or `tests/` at the repository
root. Line numbers are as of commit `71fa329`. Every bare `:nn` citation inherits its file from the
nearest preceding named path in the same paragraph.

**Provenance of the prohibited wordings.** Most entries in the not-permitted columns are carried
from the closed audit's §6.1, the A3 corrections list, or the five publication blockers. A few are
the same claim *re-anchored* to a current line number, because the closed audit's citations have
drifted — those are re-anchorings of already-identified claims, not new findings.

**Drafter-added citations.** `README.md:13-15` (C2), `README.md:83` (C11), `scaffold/CLAUDE.md:21`
(C1, where the determinism sentence at `CHARTER.md:58` is re-anchored to its restatement) and
`scaffold/backend/tests/test_engine.py:62-66` (C3, the test's own docstring) locate claim-classes
already in the identified set at places the closed audit did not name. No entry in this register
asserts a claim-class the identified set does not already contain.

**Drafter-formulated prohibited wordings.** Five entries in the not-permitted columns are phrase-
classes with no corresponding text anywhere in the repository, and are recommendations rather than
identified claims: "Production-ready." and "Ready to run." (C12); "Replayable runs." and
"Replay-ready foundations." (C7); "Macro and meso are coupled." (C8). Each is now labelled in its
row as drafter-proposed and not in force. See OQ-8.

**Withdrawn entries.** Two would-be new findings have been withdrawn rather than ruled on:
`CHARTER.md:59` (to OQ-6) and "Crises propagate through populations, media, networks and
institutions." (to OQ-8, being a restatement of founder backlog text at `HANDOFF.md` § Backlog (`:112-114`)).

Where a statement rests on a result recorded by an earlier verification pass rather than on
execution performed while drafting this register, that is stated explicitly. **No code was executed
while drafting this document.** Every code-side statement below rests on reading source, on the
absence of call sites confirmed by search, or on execution results already recorded in
`A3-VERIFICATION-RESULTS.md`.

**C1 — reproducibility.**
Cleared wording is quoted verbatim from `HANDOFF.md:56-57`. Target wording is quoted verbatim from
`HANDOFF.md:61-62`; `HANDOFF.md:59` is the lead-in sentence that instructs the target be labelled
clearly as a target and not a delivered capability.
The prohibited sentence "same seed, same scenario, same decisions ⇒ identical numeric state" is at
`CHARTER.md:58`, restated at `scaffold/CLAUDE.md:21`. The determinism test compares only
`a.macro_snapshot() == b.macro_snapshot()`, i.e. the final macro dictionary, at
`scaffold/backend/tests/test_engine.py:34-40`; it compares no cohort belief, no narrative adoption,
no event log and no snapshot history. Both runs call the same in-process stub, so agent output is
held constant rather than varied — stub at `scaffold/backend/app/simulation/llm_gateway.py:41-51`.
That varying only the stub's action choice moves macro numbers (0.59 → 0.39) is recorded at
`HANDOFF.md` § Reproducing the evidence (`:152`), from `docs/delivery/evidence/probe.py`.

**C2 — determinism boundary.**
`grep -rn "litellm" scaffold/backend/` returns three lines: `requirements.txt:20` and two lines
inside the module docstring at `llm_gateway.py:17-18`, which spans lines 1-29. The module's real
imports begin at `llm_gateway.py:31` and are `annotations`, `typing` and `ActionProposal` only. The
three code paths that change macro state are all invoked from `engine.py`: `engine.py:136`,
`engine.py:164` (both via `apply_deltas`) and the direct tick stamp at `engine.py:179`. The mutation
itself is `setattr(ind, key, updated)` at `agents/macro_state.py:47`, inside the single
`apply_deltas` function — i.e. the write executes outside `engine.py`, but every call to it is made
from `engine.py`. `grep -rn "apply_deltas" scaffold/backend/` returns five lines: the definition at
`agents/macro_state.py:23`, a docstring mention at `agents/macro_state.py:16`, the two call sites
`engine.py:136` and `engine.py:164`, and the string literal inside the boundary test's assertion at
`tests/test_engine.py:76`. The only call sites are the two in `engine.py`. The sole meso write is
`b.government_competence = max(0.0, b.government_competence - drift)` at
`agents/cohort_agent.py:38`, guarded by `if self.cohort.grievances:` at `:35`, with the draw at
`:36` and the binding `b = self.cohort.beliefs` at `:37`. On the absence of a model call path: a
search of `scaffold/backend/app/` for an import of any model or HTTP client (`openai`, `anthropic`,
`httpx`, `requests`, `aiohttp`, `litellm`, `urllib`) returns one line only, the docstring
`litellm` at `llm_gateway.py:17`. `llm_mode` and `llm_model` are declared at `config.py:24-25` and
the only read of either outside that file is `main.py:45`. The prohibited
"enforced in code and guarded by a test" is at `README.md:13-15`; "guards in CI" at `CHARTER.md:44`.

**C3 — the boundary test.**
Full test body at `scaffold/backend/tests/test_engine.py:61-77`. The assertions are
`isinstance(proposal, ActionProposal)` at `:74`, `not hasattr(proposal, "apply_deltas")` at `:76`
and `not hasattr(proposal, "macro_state")` at `:77`. The claim that it "guards this against
regression" is at `README.md:61-63`; the test's own docstring claim that the gateway "must not expose
any state-mutation surface" is at `scaffold/backend/tests/test_engine.py:62-66`, the phrase itself on
`:64-65`.

**C4 — legality and feasibility.**
`_validate_and_price` is defined at `scaffold/backend/app/simulation/engine.py:121`; its entire body
is `base = ACTION_EFFECTS.get(proposal.action_type, {})` and `return dict(base)` at `:128-130`. Its
signature takes only the proposal, so the agent spec is unreachable from the gate. `ACTION_EFFECTS`
is a seven-entry table at `engine.py:35-43` touching three keys. Constraint inertness was proven by
substitution, not grep: 40-tick hash identical with and without constraints
(`A3-VERIFICATION-RESULTS.md:92-98`). Prohibited wordings at `README.md:38`, `README.md:41`,
`scaffold/README.md:19`, `CHARTER.md:112`,
`scaffold/backend/app/simulation/schemas/agent_schema.py:181-183`, `engine.py:3-4`,
`agents/institutional_agent.py:4-5`, `agent_schema.py:157-158`, `agent_schema.py:377-379`, and
"accepts, rejects, or scales" at `scaffold/README.md:24`.
Note `CHARTER.md:113-114` — "the LLM may *propose* a composition; it never decides whether the
composition is legal" — is **true** and may stand.

**C5 — player decision path.**
Endpoint at `scaffold/backend/app/api/routes_simulation.py:80-101`. It opens
`model.event_log.append(` at `:91`, builds the dictionary at `:92-99` with `"effects": []`
hard-coded at `:97` and the client's full submission stored verbatim as
`"intervention": intervention.model_dump()` at `:98`, closing at `:100`. `step()` at `engine.py:147-180` never reads `event_log`; the identifier appears there only as
an append target at `:165`. The `janitor_with_no_authority` result is recorded at
`A3-VERIFICATION-RESULTS.md:120-141`, driven through the real API with `TestClient`. Prohibited
wordings at `routes_simulation.py:4-5`, `routes_simulation.py:82-84`, `README.md:41`.

**C6 — persistence.**
`SimulationRun`, `StateSnapshot` and `EventLog` are defined at `scaffold/backend/app/db/models.py:23`,
`:42`, `:56`. `grep -rn "SimulationRun\|StateSnapshot\|EventLog\|get_db" scaffold/backend/app`
returns only those definitions, their `relationship()` back-references, and the `get_db` definition
at `db/session.py:44` — no call site outside the defining modules. No `session.add`,
`session.commit` or `session.merge` exists anywhere in the scaffold. `init_db` at
`db/session.py:37-41` is invoked once, from the start-up hook at `main.py:30-39`, inside
`except Exception` that logs "Running in-memory only." and continues. Run state is the module-level
`_RUNS` dict at `api/runs.py:18`. Prohibited wordings at
`scaffold/docs/ARCHITECTURE_DECISIONS.md:29-31` (ADR-003, status Accepted, present tense),
`scaffold/README.md:41`, `scaffold/backend/app/db/models.py:1-6`.

**C7 — replay.**
`grep -rn "hashlib"` and `grep -rn "getstate"` across `scaffold/backend/app`, `scaffold/scenarios`
and `scaffold/schemas` each return nothing. That is the scope the cleared wording claims, and no
more: `scaffold/backend/tests/` and `scaffold/frontend/` are outside it, and a hash computed without
importing `hashlib` — via the builtin `hash()`, or by comparing serialised forms — would not be
caught by those two terms. Snapshots are `model_dump()` dictionaries appended to an
in-process list: `engine.py:116` (initial), `engine.py:180` (per tick), `agents/macro_state.py:49-51`.
No restore path exists. Target wording from `HANDOFF.md` § Phase 0 priority order, P0.6 (`:87-88`) and `HANDOFF.md` § Backlog (`:128-131`).

**C8 — cross-tier coupling.**
Perturbation results, executed at seed 88213 over 40 ticks, at `A3-VERIFICATION-RESULTS.md:142-175`
and reproducible via `docs/delivery/evidence/a3_rng_isolation.py`. The mechanism: the cohort draw at
`agents/cohort_agent.py:36` is guarded by `if self.cohort.grievances:` at `:35`, so a
grievance-free cohort consumes no draw; the shared stream is the single `random.Random` created at
`engine.py:83`; consumption order is fixed by `engine.py:152`, `:156`, `:176`. There is exactly one
`random.Random` instance in application code and there are exactly three draw sites —
`cohort_agent.py:36`, `diffusion.py:75`, `engine.py:135`. The "second- and third-order effects"
promise is at `CHARTER.md:25`. Target wording from `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`); the substream defect is
recorded at `A3-VERIFICATION-RESULTS.md:170-175`. **Note on that citation:** `HANDOFF.md` § Phase 0 priority order (`:68-90`)
predates the founder decision of 18 July 2026 and therefore does not list **P0.4A**, which now owns
the randomness defect and gates P0.5's implementation. Cite `PHASE-0-REMEDIATION-PLAN.md` §P0.4A for
that ownership, not `HANDOFF.md`.
**Amended 19 July 2026 — the note above is superseded.** By founder decision of 19 July 2026, P0.4A
was inserted into the canonical sequence and is now citable at `HANDOFF.md` § Phase 0 priority order,
P0.4A (`:76-83`). For P0.4A's **scope**, exit criteria and sequencing rule, continue to cite
`PHASE-0-REMEDIATION-PLAN.md` §P0.4A and `docs/adr/ADR-010-deterministic-randomness-architecture.md`;
`HANDOFF.md` states the item's existence and position, not its detail.

**Scope of that evidence, stated precisely.** The perturbation matrix covers macro→meso and
meso→macro only, and A3's own conclusion at `:167` is confined to those two: "Macro→meso is dead.
Meso→macro is also dead." **The micro tier was not perturbation-tested by A3 and was not tested
here.** The founder's summary at `HANDOFF.md:64-66` states the broader formulation — "The three
tiers never causally influence one another" — as one of the two critical findings of the closed
audit. This register does not reproduce that formulation verbatim, because the drafter cannot assert
the micro leg from the evidence available: it is read from source, not demonstrated by perturbation.
**That is a limit on what the drafter may assert, not a ruling that the founder-recorded finding is
wrong.** Whether the finding is narrowed, and by whom, is OQ-9 and is not settled here.

The micro→macro write is live and is read directly from source: `engine.py:159-164` steps each
`InstitutionalAgent`, calls `_validate_and_price(inst.last_proposal)`, and on a non-empty result
calls `self.macro.apply_deltas(deltas)` inside the same loop. The reason this is an open loop rather
than a causal channel is that the action choice reads no state: `institutional_agent.step()` passes
only `self.spec.model_dump()` plus a context of `tick`, `scenario_id` and a hard-coded
`"primary_target": None`, and the stub's `_stub_action_type` at `llm_gateway.py:41-51` is a
`table.get(agent_role, "observe")` lookup on the role alone. No macro indicator and no cohort belief
enters the decision. The effect applied is a constant from the seven-entry `ACTION_EFFECTS` table at
`engine.py:35-43` (C4, C13). That six agents each apply a non-zero delta per tick follows from the
six `kestral-strait` roles all mapping to non-`observe` entries; it is arithmetic over the role table
and that one scenario file, not an executed measurement, and it does not generalise. `observe` maps
to `{}` at `engine.py:42`, the application is gated on `if deltas:` at `engine.py:163`, and any role
absent from the stub's six-entry table falls through `table.get(agent_role, "observe")` at
`llm_gateway.py:51` — so an agent outside that table writes nothing. This is the case C10 warns
about: no second archetype has ever been loaded.

**C9 — CI.**
`ls -a .github` → no such directory. `find . -path ./.git -prune -o \( -name "*.yml" -o -name
"*.yaml" \) -print` → `./scaffold/docker-compose.yml` only. `git log --oneline` → one commit,
`71fa329`. `git branch -a` → `main`, tracking `origin/main`; `git remote -v` → a configured GitHub
remote. Note `.gitignore:16-18` pre-ignores `.mypy_cache/` and `.ruff_cache/` although neither tool
is configured anywhere in the tree. Prohibited wording at `CHARTER.md:44`. Stale audit phrasing at
`docs/delivery/CURRENT-STATE-AUDIT.md:283` and `A3-VERIFICATION-RESULTS.md:242`.

**C10 — archetype extensibility.**
Scenario loading is a path-existence check followed by `json.loads`, in `load_scenario` at
`api/runs.py:21-26` — path built at `:23`, existence check at `:24-25`, `json.loads` at `:26` — with
no content validation; cohort records are then parsed through Pydantic at `engine.py:98-101`. The
absence of an archetype branch was checked in `engine.py` only: `scenario_id` appears there at
`:52` and `:86` as a value read and stored, never as a condition, and no other archetype conditional
is present in that file. `agents/`, `diffusion.py` and the schema layer were not searched for this. `scaffold/scenarios/` contains exactly one file, `kestral-strait.json`; no second
scenario was constructed or run, so "loads and runs" is untested rather than observed.
`represents_population` occurs only at its declaration
`agent_schema.py:95` and in scenario data; `income_sensitivity_to_shipping_disruption` only at
`agent_schema.py:36`; `fiction_disclaimer` only at `scaffold/scenarios/kestral-strait.json:7`;
`self.campaign` only at its assignment `engine.py:111`. A twelve-term search over `scaffold/backend/app`
for `media_exposure`, `demographics`, `religion_majority`, `primary_language`, `existing_grievance`,
`target_cohorts`, `amplification_network`, `detection_probability`, `attribution_probability`,
`desired_behaviour`, `perceived_independence` and `truth_status`, excluding the schema definition
file, returns zero hits for all twelve. The silent-skip behaviour is `agents/macro_state.py:37-38`
(`if not hasattr(ind, key): continue`, inside the loop opened at `:36`) and `:39-41` (`getattr`
followed by the non-scalar skip); the function returns `None`
and logs nothing. Prohibited wordings at `README.md:72-74`, `scaffold/README.md:106-107`,
`scaffold/docs/ARCHITECTURE_DECISIONS.md:75`, `scaffold/CLAUDE.md:51-55`.

**C11 — test suite scope.**
Whole suite is `scaffold/backend/tests/test_engine.py`, 77 lines, five tests at `:25`, `:34`, `:43`,
`:52`, `:61`. `tests/` contains only `__init__.py` and this file. Per-test assertions: `:27-31`,
`:36-40`, `:45-49`, `:55-58`, `:70-77`. No `TestClient`, no `httpx` and no `db` import appears in
the module. The claim that a different-seed divergence cannot be distinguished from a stream shift
follows from C8's mechanism. Prohibited wordings at `README.md:61-63`, `README.md:83`.

**C12 — execution readiness.**
Standing prohibition at `HANDOFF.md` § Standing constraints (`:135`). "Runnable skeleton, not a finished product" is the
scaffold's own existing wording at `scaffold/README.md:5-6`, quoted approvingly at
`A3-VERIFICATION-RESULTS.md:87-88`, where A3 classifies it as "Permitted incompleteness" and
expressly not a publication blocker. `scaffold/README.md` is itself a document under P0.1
correction, so its self-description is not independent evidence of runnability — but that
observation is not sufficient to reverse a prior verification pass's explicit clearance, which is
why the ruling is withdrawn to OQ-5 rather than made here. Tests recorded as passing at `HANDOFF.md:43` and `HANDOFF.md:51` ("5 passed").
`HANDOFF.md:49-50` records **two** departures from the documented install, not one: everything was
installed *except* `litellm`, *and* `mesa>=2.1,<3.0` was installed with `--no-deps` to avoid a
Windows long-path failure in the solara/jupyter tree. Environment described at
`A3-VERIFICATION-RESULTS.md:27-28`. The clean-machine install failure is recorded at
`HANDOFF.md:45-48`. The A3 environment is not reconstructible from anything recorded in the
repository. A reader can check its current absence directly: run `python -c "import mesa"` from
`scaffold/backend` and list that directory for a `.venv`. This register makes no claim about the
outcome beyond that — the earlier report that both now fail comes from the Phase B engine-behaviour
verification pass, which is not itself a document in the tree, and was not re-run here.
`scaffold/backend/requirements.txt:1-24` (the file is 24 lines) declares thirteen packages, all as
open-ended ranges, with no exact pin and no hash; `websockets>=12.0` at `:13` has no upper bound.
*(Count reconciled 19 July 2026 across the Phase B records:
`grep -c -E '^[^#[:space:]]' scaffold/backend/requirements.txt` → `13`. An earlier draft of this
register said twelve.)* No
`pyproject.toml`, no lockfile, no `.python-version`, no `setup.cfg` exists anywhere in the tree —
recorded as fact, not as a defect finding, since the packaging approach is open audit §8 item 5. The
Python target
appears only in prose and in the Docker base image: `scaffold/backend/Dockerfile:1`,
`scaffold/docs/ARCHITECTURE_DECISIONS.md:11`, `scaffold/CLAUDE.md:44`.

**C13 — outcome modelling.**
`ACTION_EFFECTS` at `engine.py:35-43`; `_validate_and_price` returns `dict(base)` at `:128-130`. The
per-tick macro rule is one uniform draw applied to one indicator: `engine.py:132-136`. The absence of
opposing mechanisms — `cost`, `cooldown`, `decay`, `budget`, `resource`, `prerequisite`, `revert`,
all absent from `engine.py` — is recorded at `A3-VERIFICATION-RESULTS.md:192-200`. Saturation under
varied action selection at `A3-VERIFICATION-RESULTS.md:177-190`; readiness pegs at tick 61 per
`A3-VERIFICATION-RESULTS.md:114` and `HANDOFF.md` § Reproducing the evidence (`:149`). Absence of terminal semantics at
`A3-VERIFICATION-RESULTS.md:224`. Prohibited wordings at `CHARTER.md:61-62` (audit §6.1 item 6) and
`README.md:36` (audit §6.1 item 3). `CHARTER.md:59` is deliberately **not** listed — see OQ-6.

**C14 — language-model feature surface.**
`grep -n "^def \|^async def " scaffold/backend/app/simulation/llm_gateway.py` returns exactly three
lines: `:41` (`_stub_action_type`, private), `:54` (`propose_action`), `:85` (`generate_briefing`).
The role lookup table is `:43-51`. `generate_briefing`'s body is `:85-103` (the file is 103 lines);
it reads two keys
from the mapping it is handed — `indicators` and `tick`, at `:95-96` — then two values out of the
nested `indicators` dict, `government_approval` and `shipping_throughput_pct_of_baseline` at
`:97-98`, and returns an f-string. There is no retrieval. `PROMPT_VERSION = "v1"` is declared once at
`llm_gateway.py:38` and read nowhere; neither `model_id` nor temperature is logged anywhere.
Prohibited wordings at `README.md:39-41`; the versioning claim at
`scaffold/docs/ARCHITECTURE_DECISIONS.md:66-67` and `scaffold/CLAUDE.md:25-26`.

**C15 — fiction and dual-use.**
`fiction_disclaimer` occurs once in the whole tree, at `scaffold/scenarios/kestral-strait.json:7`,
and is read by nothing. A case-insensitive search for "fictional" across all `.py`, `.json`, `.html`
and `.js` under `scaffold/` returns that same single line. No JSON Schema validation library is
present: `grep -rn "jsonschema" scaffold/` returns nothing, so the nine published schema mirrors
validate nothing at runtime. All **five** REST responses are defined at `routes_simulation.py:47-49`
(`create_run`), `:60` (`advance`), `:71-77` (`get_state`), `:101` (`submit_decision`) and `:111`
(`get_events`), and none carries a disclaimer or provenance field. *(An earlier draft of this
register said four, omitting `submit_decision`; the conclusion is unchanged and holds for all
five.)* The frontend is a single file,
`scaffold/frontend/index.html`; a case-insensitive search of `frontend/` for "fiction",
"provenance", "AI-generated" and "disclaimer" returns nothing. The stub briefing's literal
`[STUB briefing — tick N]` prefix is at `llm_gateway.py:100`, within the return expression spanning
`:99-103`; the "interpretive layer only"
note at `routes_simulation.py:76` is a source comment and is never transmitted. `NOTICE.md`, read in
full, contains no acceptable-use or field-of-use restriction (see `NOTICE.md:11-16`). The
prohibited provenance claim is `CHARTER.md:141-142`. Blocker B5 at
`A3-VERIFICATION-RESULTS.md:245` and `HANDOFF.md` § Publication exit criteria (`:104-105`). **Both of those anchors state B5's
clearance route in superseded terms** ("owner decision"); `HANDOFF.md` § Publication exit criteria (`:104-105`) has since been
corrected in place and `A3-VERIFICATION-RESULTS.md:245` is corrected by the appended amendment at
the end of that file. They remain cited here because they are where the blocker is *defined*.

---

## Statements in this register that rest on inference rather than direct observation

Recorded explicitly, because the standard for this document is that unverified things are labelled
as unverified.

1. **"Its five tests are recorded as passing" (C12).** No test was executed while drafting this
   register. This rests on `HANDOFF.md:43` and `HANDOFF.md:51`. The wording "recorded as passing"
   was chosen deliberately over "pass".

2. **The clean-machine install failure and the `litellm` 1.92.0 / cp313 / Rust-toolchain
   explanation (C12).** Reported at `HANDOFF.md:45-48`. No installation was attempted here, so the
   failure mode is second-hand. That `litellm` is imported by no executable code *is* directly
   verified.

3. **All execution-derived results in C4, C5, C8 and C13** — the 40-tick constraint hash, the
   `TestClient` decision-endpoint run, the perturbation matrix, the saturation-under-varied-actions
   result and the tick-61 clamp — come from `A3-VERIFICATION-RESULTS.md` and its evidence scripts.
   They were not re-run. They are treated as reliable because A3 states every result in it is from
   execution (`A3-VERIFICATION-RESULTS.md:23`), but they are not first-hand here.

4. **"No language model is called" (C2, C14).** Inferred from the absence of any executable
   `litellm` import, the absence of any model or HTTP client import anywhere under
   `scaffold/backend/app/`, and the gateway's two functions being a lookup table and an f-string. It
   is an inference from absence of a call path, not from observing a run. The cleared wording says
   "no language model is called" and not "no language model *can* be called", because the latter
   would assert a structural guarantee that does not exist — `config.py:24-25` already anticipates
   the seam.

5. **"A gateway that mutated authoritative state by any other route would pass it unchanged" (C3).**
   Inferred from what the test's three assertions inspect. No such gateway was constructed and run
   against the test to demonstrate it.

6. **"Two archetypes that differ only in those fields will behave identically" (C10).** Inferred
   from the zero-read-site result for those fields, not demonstrated by constructing a second
   scenario and comparing runs. The underlying zero-read-site result is directly verified.

6a. **Whether a second scenario file loads and completes a run at all (C10).** Not inferred and not
   claimed. `scaffold/scenarios/` holds one file; no second scenario was ever constructed or
   executed in any recorded pass. An earlier draft of this register asserted in the future
   indicative that such a file "will load and run"; that assertion has been withdrawn. What is
   verified is the shape of the load path, not that an arbitrary conforming file completes a run.

6b. **That the micro→macro channel is an open loop rather than a causal channel (C8).** Read from
   source — the stub's action choice is a role-keyed `table.get` that receives no state — not
   established by perturbation testing. No micro-tier perturbation test has ever been run, by A3 or
   here. The existence of the micro→macro *write* is directly verified at `engine.py:159-164`.

6c. **That six agents each apply a non-zero delta per tick (C8, C13).** Arithmetic over the six
   `kestral-strait` roles and the role/effect tables, not an executed count. It holds for the one
   shipped scenario and does not generalise: a role absent from the stub's table resolves to
   `observe`, whose effect entry is empty, and writes nothing. C8's cleared wording is scoped
   accordingly.

7. **Repository visibility (settled-claims section).** The founder *decision* is recorded at
   `HANDOFF.md:13-19` and is settled. The actual *state* of the remote is not verified: no `gh`
   command was run and no network call was made, per standing constraint. The remote URL exists;
   its visibility setting is unknown. The settled-claims section now distinguishes the two.

8. **Whether commit `71fa329` has actually been pushed.** The local `origin/main` ref points at the
   same commit as `HEAD`, which is consistent with a completed push, but no fetch was performed. This
   register describes last-known local state.

9. **Whether `docs/PLAN.pdf` contains further capability claims requiring correction.** The PDF was
   not text-extracted. It is known to carry two DISARM framework link annotations. Any claim inside
   it is outside the coverage of this register — which is itself a gap the owner should be aware of,
   since `README.md:27` presents the PDF as a primary document.

10. **Completeness.** This register covers the claim areas named in the Phase B brief plus those
    reachable from the closed audit's section 6.1, the A3 corrections list and the five blockers. It
    is **not** the product of a fresh search for undiscovered false claims, which the standing
    constraints prohibit. It should not be read as proof that no other overstatement exists in the
    repository.
