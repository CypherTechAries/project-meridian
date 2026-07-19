# HANDOFF — resume point

**Last updated:** 18 July 2026
**Reason for handoff:** original machine too slow to continue; work moved to a faster terminal.

Read this first, then [`docs/delivery/CURRENT-STATE-AUDIT.md`](docs/delivery/CURRENT-STATE-AUDIT.md)
and [`docs/delivery/A3-VERIFICATION-RESULTS.md`](docs/delivery/A3-VERIFICATION-RESULTS.md).

---

## Repository status

**PRIVATE.** Deliberately. The founder decision is that MERIDIAN becomes public, but only after
Phase 0 corrections pass, because the repository currently contains documentation claiming
properties the code does not have. Publishing before that would put the project's weakest artefact
(documentation accuracy) in front of the audience it is meant to impress.

Flipping to public later: `gh repo edit --visibility public --accept-visibility-change-consequences`.
**Do not run it until the Phase 0 gates below pass and the owner approves.**

- Default branch: `main` (explicit founder decision; other repos using `master` are irrelevant here).
- Licence: **none, deliberately.** All-rights-reserved position recorded in [`NOTICE.md`](NOTICE.md).
  Do not add an open-source licence. Do not accept external code contributions.
- Inspiration source: deliberately unnamed in the repository. Do not name the employer or job advert.

## Where the work stopped

Completed:
- Broad nine-dimension audit (124 agents, 128 candidate findings, 112 survived, 11 refuted).
- A3 targeted re-verification of the seven outstanding checks. **Audit now CLOSED.**
- Governance notices: `NOTICE.md`, `CHARTER.md`, root `README.md` (the README still needs Phase 0
  correction; see below).

Not started, in order:
1. **Phase B — governance bootstrap.** `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`, RAID register,
   project log + policy, deduplicated corrective backlog, corrected capability claims, publication
   exit criteria, ADR template. Every record needs a plain-English layer and a technical-evidence layer.
2. **Phase C — Phase 0 correction** (P0.1 to P0.8, see below).
3. **Phase D — present results to owner. Repository creation/publication is gated on approval.**

## Current state of the code, stated honestly

The scaffold runs and its five tests pass, but:

- `pip install -r requirements.txt` **fails on a clean machine.** `litellm` resolves to 1.92.0,
  which has no cp313 wheel, falls back to sdist, and needs a Rust toolchain. Because pip resolves
  before installing, nothing installs. **`litellm` is never imported by any code** — it appears
  only in a docstring at `llm_gateway.py:17`. Removing it from the default install unblocks this.
- To run the suite meanwhile: install everything except `litellm`, plus `mesa>=2.1,<3.0`
  (`--no-deps` avoids a Windows long-path failure in the solara/jupyter tree). Then
  `python -m pytest tests -v` → 5 passed.
- **Reproducibility is real but narrower than documented.** Same seed reproduces the same numbers
  *given identical LLM output*. The engine's determinism test holds the LLM constant and then
  declares determinism. Correct claim to use, per founder decision:

  > "The existing stubbed execution path reproduces the same tested numeric outputs when the seed,
  > scenario and stubbed agent outputs remain identical."

  The target contract (label it clearly as a target, not a delivered capability):

  > "Given the same scenario version, rule-pack version, seed, ordered player inputs and recorded
  > external-agent inputs, the engine is intended to reproduce identical authoritative state hashes."

- **Two critical findings, both behavioural.** The three tiers never causally influence one another
  (apparent meso→macro coupling is shared-RNG contamination, not causality), and the macro tier
  saturates monotonically with no cost/cooldown/decay mechanism anywhere in the engine.

## Phase 0 priority order (founder-set)

- **P0.1** Correct live false claims (CI, legality validation, persistence, replay, archetype
  extensibility, execution readiness). Documentation must describe observed behaviour.
- **P0.2** Restore reproducible installation. Remove/optionalise LiteLLM. Pin supported Python.
  Clean-environment command that succeeds on Windows and Linux.
- **P0.3** Establish real CI. Only checks that genuinely exist and pass.
- **P0.4** Define the authoritative-state contract across macro/meso/micro.
- **P0.4A** Establish a deterministic randomness architecture. Isolate every authoritative random
  draw by subsystem, entity, interaction, purpose and context, so that adding, removing or
  reordering a draw in one place cannot silently shift every later draw everywhere else. Lettered
  rather than numbered so the founder-set numbering P0.1 to P0.8 survives unchanged. *(Founder
  decision, 18 July 2026. Architecture accepted 19 July 2026 —
  `docs/adr/ADR-010-deterministic-randomness-architecture.md`. **Not implemented; no code exists
  for it.** P0.5 specification may proceed in parallel, but P0.5 implementation, entity promotion
  and world-model materialisation may not begin until P0.4A passes.)*
- **P0.5** Design explicit cross-tier causal channels. No arbitrary coupling. `represents_population`
  must affect aggregation. *(Note: this is arguably the highest-value item, since it is the product's
  core mechanism, not a tidiness fix.)*
- **P0.6** Repair event, snapshot and replay foundations. Central transition mechanism, full
  snapshots, replay makes zero model/network calls.
- **P0.7** Define simulation time and horizon **before** touching saturation. No arbitrary mean reversion.
- **P0.8** Review the influence-operations targeting schema before publication.

## Publication exit criteria

Do not create a public repository until all of these pass:

- [ ] Documented clean installation works on a supported environment
- [ ] README accurately states what is and is not implemented
- [ ] False determinism and replay claims corrected
- [ ] Existing tests and their actual scope accurately described
- [ ] Unused installation-blocking dependencies removed or made optional
- [ ] Current-state audit and known-limitations document committed
- [ ] Secret, personal-data and repository-content review passes

Five deduplicated publication blockers are listed in `A3-VERIFICATION-RESULTS.md`. B1 to B4 clear by telling the truth. **B5 (dual-use schema) is DECIDED — founder decision, 18 July 2026 — and did NOT clear with that decision.** It now clears only when the **eight controls** that decision names are **implemented and verified**; disclosure and acceptable-use wording are supplementary, technical enforcement is mandatory, and **none of the eight exists in code**. Deciding B5 therefore *enlarged* this gate.
**The earlier wording of these two lines — "four clear by telling the truth; only B5 needs an owner decision" — is superseded in its second half and must not be carried forward.** It survives verbatim at `A3-VERIFICATION-RESULTS.md:247` (see the amendment at the end of that file). Controls and per-control criteria: `docs/delivery/PUBLICATION-EXIT-CRITERIA.md` C6. Decision record: `docs/delivery/RAID-REGISTER.md` DEC6.

## Backlog — captured, deliberately not started

Do not begin these until the foundation is honest and testable:

- **Synthetic-society correction.** MERIDIAN must simulate how an entire society perceives, debates,
  exploits, fears and responds to a crisis, not only how the command room manages it. Crises must
  propagate through populations, families, media, networks, markets, political organisations, foreign
  publics and institutions, affecting authoritative state and player options rather than appearing as
  generated narrative.
- **World-model documents:** `ENTITY-ONTOLOGY`, `PERSON-MODEL`, `ORGANISATION-MODEL`,
  `RELATIONSHIP-GRAPH`, `BELIEF-AND-KNOWLEDGE-MODEL`, `POPULATION-FIDELITY`,
  `ENTITY-PROFILE-EXPERIENCE`, `IDENTITY-AND-BIAS-GUIDELINES`. Entities are persistent with identity,
  history, relationships, beliefs, capabilities; profiles expose information by role/evidence/confidence
  rather than omniscient ground truth; profile detail must drive behaviour causally, not decoratively.
- **Visual system:** `VISUAL-CONSTITUTION`, `DESIGN-TOKENS`, `MOTION-SYSTEM`, `INTERACTION-PATTERNS`,
  `SCREEN-SPECIFICATIONS`, `VISUAL-QA-CHECKLIST`. Original command-system language; no trade dress
  from any named product or game.
- **Conversational interface:** `CONVERSATIONAL-INTERFACE`, `MULTIMODAL-INTERACTION`,
  `VOICE-INTERACTION`, `ACTION-CONFIRMATION`, `CONVERSATION-CONTEXT`,
  `MULTIMODAL-INPUT-THREAT-MODEL`. Three modes: EXPLORE / PLAN / COMMAND. Natural language, voice or
  image input must never directly mutate state.
- **Replay requirement (expands `ExternalAgentInput`, do not implement in Phase 0):** every text turn,
  voice transcript, uploaded image or document, map selection, annotation and confirmation that can
  influence an action is a versioned external input. Replay must preserve the interpreted structured
  input and its provenance.

## Standing constraints

- Do not describe the codebase as execution-ready, replay-capable or fully deterministic.
- Do not modify simulation behaviour merely to make an audit finding disappear.
- Do not launch another unrestricted multi-agent audit. The broad audit is closed.
- AI agents may draft records but may not approve their own decisions.
- Human approval required for architecture, dependencies, licence, migrations, auth, security
  controls, public releases, and anything affecting determinism or authoritative state.

## Reproducing the evidence

Scripts in [`docs/delivery/evidence/`](docs/delivery/evidence/). From `scaffold/backend`, with
`PYTHONPATH` set to that directory and a venv containing everything except `litellm`:

| Script | Proves |
|---|---|
| `verify_criticals.py` | 14/18 macro scalars frozen; readiness pegs at tick 61; tiers move in opposite directions |
| `a3_direct.py` | checks 1-5: no fiscal path, constraints inert, endpoint is a no-op, saturation persists under varied actions |
| `a3_rng_isolation.py` | meso→macro coupling is shared-RNG contamination, not causality |
| `probe.py` | determinism regression probes; changing only the LLM's action choice moves macro numbers 0.59 → 0.39 |

---

## Amendment record

**Amendment 1 — 19 July 2026. P0.4A inserted into the canonical Phase 0 priority order.**

**Plain English.** P0.4A (deterministic randomness) was created by founder decision on 18 July 2026,
after this document's Phase 0 list was written. Until now the list above ran P0.4 → P0.5 while every
other record — the remediation plan, the corrective backlog, the RAID register, the publication exit
criteria, ADR-010 and the world-model documents — ran P0.4 → P0.4A → P0.5. Several of those records
cited this document, by line number, as the authority for a list that omitted the item. The founder
ruled on 19 July 2026 that the canonical sequence be corrected rather than worked around. P0.4A now
sits in its correct position above.

**Technical evidence.** The item was inserted as `HANDOFF.md:76-83`, between P0.4 (`:75`) and P0.5
(`:84-86`). Nothing else in this document was altered: lines 1 to 75 are unchanged, and every line
formerly numbered 76 or higher moved down by exactly 8. No existing amendment, supersession notice
or superseded wording was removed — in particular the B5 supersession note now at `:104-105` is
carried forward verbatim. Wording of the inserted item is drawn from
`docs/adr/ADR-010-deterministic-randomness-architecture.md` and
`docs/delivery/PHASE-0-REMEDIATION-PLAN.md` §P0.4A.

**Consequential reference migration.** Every citation of the form `HANDOFF.md:NN` elsewhere in the
repository that pointed at line 76 or higher was re-anchored in the same pass. Where practical those
citations were converted to stable section anchors of the form
``` `HANDOFF.md` § Phase 0 priority order, P0.5 (`:84-86`) ``` so that a future insert does not
invalidate them again. The migration, its verification results and any unresolved citation are
recorded in `docs/delivery/HANDOFF-REFERENCE-MIGRATION.md`. Nothing under `scaffold/` was modified.

**Stable anchors for citing documents.** Prefer these to line numbers:
`§ Repository status`, `§ Where the work stopped`, `§ Current state of the code, stated honestly`,
`§ Phase 0 priority order` (items P0.1 to P0.4, P0.4A, P0.5 to P0.8), `§ Publication exit criteria`,
`§ Backlog — captured, deliberately not started`, `§ Standing constraints`,
`§ Reproducing the evidence`.
