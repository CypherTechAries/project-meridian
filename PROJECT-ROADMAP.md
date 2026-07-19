# MERIDIAN — project roadmap

> **This is a plan, not a capability claim.** Nothing below describes working software unless it
> says so and cites evidence. The authority for what may be claimed about the current codebase is
> [`docs/delivery/CAPABILITY-CLAIMS.md`](docs/delivery/CAPABILITY-CLAIMS.md); where this roadmap and
> that register disagree, the register governs. The authority for what must be true before
> publication is [`docs/delivery/PUBLICATION-EXIT-CRITERIA.md`](docs/delivery/PUBLICATION-EXIT-CRITERIA.md).

**Status:** founder-approved two-horizon strategy, 19 July 2026.
**Created:** 19 July 2026. This file did not previously exist.

---

## The two horizons

MERIDIAN is planned in two deliberately separated horizons. Conflating them is the failure mode this
document exists to prevent: the public release must not be delayed until the long-term platform is
finished, and the long-term ambition must not be described as though it already ships.

### Horizon 1 — public v0.1

> MERIDIAN is an early simulated-society platform prototype implementing one deterministic,
> cross-tier societal-response mechanism in a fictional crisis scenario.

*(Founder-approved wording. Use it as written.)*

The objective is a credible, understandable, visually polished portfolio project that a
non-technical visitor can understand within a few minutes — not a demonstration of the entire
long-term vision.

### Horizon 2 — the enduring product

> The long-term goal is a multi-agent synthetic-society modelling platform built from first
> principles for examining information propagation and evaluating defensive interventions in
> fictional environments.

*(Founder-approved wording. Always carry the "long-term goal" framing; it is a target, not a
delivered capability.)*

The existing architecture is a foundation for that future. It does not need to be rebuilt.

---

## Horizon 1 — what public v0.1 must demonstrate honestly

| # | Must demonstrate | State today | Evidence |
|---|---|---|---|
| 1 | One deterministic cross-tier societal-response mechanism | **Built** | [`P0-5-CAUSAL-SLICE.md`](docs/delivery/P0-5-CAUSAL-SLICE.md) |
| 2 | Authoritative state and controlled transitions | **Built** | [`P0-4-STATE-CONTRACT.md`](docs/delivery/P0-4-STATE-CONTRACT.md) |
| 3 | Isolated deterministic randomness | **Built** | [`P0-4A-RANDOMNESS.md`](docs/delivery/P0-4A-RANDOMNESS.md) |
| 4 | Baseline, incident and counterfactual runs | **Built** | `POST /api/demo/kestral-strait/run` |
| 5 | A polished operational interface | **Built** | Strategic Command Centre, merged `cc1cce3` |
| 6 | Hosted CI and reproducible setup | **Built** | [`P0-3-CI-STATUS.md`](docs/delivery/P0-3-CI-STATUS.md) |
| 7 | Fictional-world safety controls | **Implemented, in review** | [`docs/safety/B5-TECHNICAL-CONTROLS.md`](docs/safety/B5-TECHNICAL-CONTROLS.md) — all eight controls, 70 tests |
| 8 | Clear limitations and roadmap | **Partial** | this file; README front door outstanding |

**Item 7 is the substantive remaining engineering, and it comes first.** Founder decision of
19 July 2026: implement and verify the B5 controls **before** the belief milestone begins. Blocker B5 was *decided* on 18 July 2026 and
deciding it **enlarged** the gate: B5 now clears only when its **eight controls are implemented and
verified**, because control 8 makes technical enforcement mandatory and disclosure merely
supplementary. None of the eight exists in code. It is the most expensive of the five publication
blockers, not the cheapest.

### Explicitly out of scope for v0.1

Public v0.1 must **not** be delayed for, and must **not** imply it has: complete persistent-person
simulation · full belief and sentiment modelling · live LLM integration · Large Behavioral Models ·
replay · event sourcing · persistence · multiplayer · distributed execution · every planned screen.

Three of those are named prohibitions in the capability register — persistence (C6), replay (C7) and
LLM execution (C2). "Replay-capable" is a standing prohibited phrase.

---

## Immediate publication sequence

| Step | Action | Status |
|---|---|---|
| 1 | Complete and merge the current visual work | **Done** — PR #4 merged to `main` |
| 2 | Implement and verify the eight B5 technical controls | **In review** — `feat/b5-publication-controls`, not merged |
| 3 | Prepare the public repository front door | Not started |
| 4 | Prepare the licence decision pack | Not started |
| 5 | Run one bounded release review | Not started |
| 6 | **Stop for explicit founder approval before changing visibility** | Gate |
| 7 | Publish v0.1 only after approval | Gate |
| 8 | Begin the bounded Belief Formation and Divergence Slice | First post-v0.1 milestone |

Step 6 is absolute. Repository visibility does not change without explicit founder approval, and no
agent may treat any earlier approval as covering it.

### Front-door goal (step 3)

The README must serve a non-technical visitor first and a technical reviewer second, in this order:

1. Logo and one-sentence description · 2. Fictional-simulation disclaimer · 3. Best screenshot ·
4. What MERIDIAN demonstrates today · 5. Simple causal-chain diagram · 6. Three-minute walkthrough ·
7. Implemented / prototype / planned table · 8. Quick start · 9. Architecture in plain language ·
10. Technical architecture · 11. Safety restrictions · 12. Known limitations · 13. Long-term roadmap ·
14. Links to deeper documentation.

The governance archive and the world-model specifications (≈875 KB) stay **out of the primary
reading path** and are linked as supporting evidence only.

### The demonstration a visitor should be able to follow

Open the Kestral Strait fictional scenario → run baseline → run incident → see insurer risk and
carrier rerouting change → see economic exposure reach population cohorts → see narrative and
collective activity develop → see political pressure alter government options → compare the
counterfactual with the insurer mechanism disabled → inspect which values came from the engine and
which remain fixture-backed.

That is the whole v0.1 story, and all of it exists today.

---

## Horizon 2 — capabilities the enduring platform requires

Persistent fictional people and organisations · relationships and trust networks ·
proposition-specific beliefs · differential exposure · source-credibility assessment · attitudes,
emotions and stances · behaviour propensities · social and media diffusion · competing narratives ·
intervention comparison · controlled behavioural-model integration · controlled LLM integration ·
immutable events, snapshots, state hashes and replay · larger synthetic populations · multiple
fictional scenarios.

None of these is claimed as present. Each is a roadmap capability until it has implementation
evidence recorded in `docs/delivery/`.

### Long-term release map

| Release | Main outcome |
|---|---|
| **v0.1** | Public crisis-propagation proof |
| **v0.2** | Persistent agents and relationships |
| **v0.3** | Belief, trust and exposure modelling |
| **v0.4** | Narrative competition and intervention comparison |
| **v0.5** | Controlled LLM and behavioural-model integration |
| **v0.6** | Events, hashes, restore and replay |
| **v0.7** | Scenario platform and authoring |
| **v1.0** | Stable synthetic-society modelling platform |

These versions are indicative, not contractual. The distinction that *is* binding is between public
proof (v0.1) and enduring platform (v0.2 onward).

### Where existing planning work lands

- The **Belief Formation and Divergence Slice**
  ([`docs/design/BELIEF-SENTIMENT-VERTICAL-SLICE.md`](docs/design/BELIEF-SENTIMENT-VERTICAL-SLICE.md),
  PR #5, unmerged) is the **first major post-v0.1 milestone**, landing toward v0.2–v0.3. Planning
  only; implementation deliberately not started. Founder decision of 19 July 2026 sets an
  **A-then-B sequence**: the eight B5 controls are implemented and verified first, then v0.1 is
  published, then the slice begins under those controls. Because B5 already blocks v0.1, building it
  serves both. The slice must not expand v0.1 scope or delay publication.
- The **world-model specifications** (`docs/world-model/`) describe v0.2–v0.3 and are specification,
  not implementation. Every one carries a not-implemented banner.
- The **entity dossier experience** (`docs/design/ENTITY-PROFILE-EXPERIENCE.md`) is v0.2–v0.3.
- **P0.6** (events, snapshots, replay) is **v0.6** and is explicitly **not required for v0.1**.

---

## Standing constraints on this roadmap

- Do not expand v0.1 scope with Horizon 2 features.
- Do not claim current use of Large Behavioral Models, live LLM execution, comprehensive society
  simulation, or production readiness.
- Do not describe a target as a delivered capability; carry the "target, not delivered" label where
  the capability register does.
- Do not change repository visibility without explicit founder approval.
- The Strategic Command Centre is accepted as the operational shell. Further broad visual redesign
  is out of scope; remaining map polish is recorded as later founder-led visual work.
