# MERIDIAN use-case register

MERIDIAN is being built as a deterministic simulated-society engine. As the engine develops,
research and experiments are revealing several possible ways it could be used. **This register
separates what exists today from future directions.**

Nothing on this page is a roadmap commitment.

---

## What exists today

**One thing.** A bounded fictional crisis — a blockade in the fictional Kestral Strait — can be run
through deterministic rules and inspected: a plain-language briefing, three impact areas, government
options whose status changes as the situation moves, population groups, three virtual people with
belief and information histories, and a conversational interface that answers eight declared
questions. Decisions are **selected and never executed**.

That is the whole of it. Everything else below is research.

**One caveat on the interface.** A rebuild of the Briefing — after it failed its first usability test
with a first-time user — is on the unmerged branch `fix/first-user-usability-reset`. **The screens on
`main` are the pre-reset ones.** This register describes `main`.

---

## The register

| Use case | In one sentence | Likely users | Status | What exists today | Key missing capability | Research | Reviewed |
|---|---|---|---|---|---|---|---|
| [Crisis Simulation and Decision Support](CRISIS-SIMULATION-AND-DECISION-SUPPORT.md) | Run a fictional crisis and inspect how events move through organisations, the economy, population groups and individual decisions | Analysts, planners, researchers | **EARLY DEMONSTRATION** | One scenario, ten-stage causal chain, briefing and technical views, virtual people, Ask MERIDIAN Phase 1 | A second scenario; scenario authoring; anything beyond one crisis type | [belief API](../design/BELIEF-READ-MODEL-API.md) · [VP-1…VP-5](../design/) | 2026-07-21 |
| [Training, Exercises and Wargaming](TRAINING-EXERCISES-AND-WARGAMING.md) | Repeatable fictional exercises where participants explore decisions, consequences, information gaps and competing organisational pressures | Emergency services, resilience teams, public sector | **FUTURE DIRECTION** | Nothing exercise-specific. The engine and one scenario exist | Scenario authoring, participant roles, facilitation, replay, objectives, after-action review, **multiplayer** | [entity graduation §12](../research/SIMULATION-BORN-ENTITIES.md) | 2026-07-21 |
| [Adaptive Futures Engine](ADAPTIVE-FUTURES-ENGINE.md) | Run many controlled variations of a scenario to understand plausible outcomes, risks, critical decisions and where small changes alter the path | Planners, analysts, decision-makers | **UNDER RESEARCH** | Deterministic reproducible single runs | Ensembles, parameter variation, outcome classification, **dispersion testing**, calibration, sensitivity analysis, rare-event handling, novelty | [next-strand note](../research/NEXT-STRAND-ADAPTIVE-FUTURES-ENGINE.md) · [issue #26](https://github.com/CypherTechAries/project-meridian/issues/26) | 2026-07-21 |
| [Simulation-Born Entities](SIMULATION-BORN-ENTITIES.md) | Preserve useful organisations, products, processes or characters created in simulation and potentially export them as real-world blueprints or IP | Founders, product teams, training providers | **FUTURE DIRECTION** | Typed fictional entities within a run; append-only histories; origin labels | Persistent cross-run entities, asset manifests, ownership, permissions, legal wrappers, validation envelopes, connectors, revocation | [research](../research/SIMULATION-BORN-ENTITIES.md) · [lifecycle](../research/ENTITY-GRADUATION-LIFECYCLE.md) · [evidence pack](../research/GRADUATION-EVIDENCE-PACK.md) · [risks](../research/ENTITY-GRADUATION-RISK-REGISTER.md) | 2026-07-21 |
| [Narrative Supply-Chain Analysis](NARRATIVE-SUPPLY-CHAIN-ANALYSIS.md) | Trace how claims originate, spread and change, showing source dependence, ownership, incentives and missing perspectives | Journalists, researchers, analysts — **and the futures engine** | **UNDER RESEARCH** | Information-exposure records and belief histories **inside the fiction only** | Web ingestion, multilingual sources, claim lineage, source independence, ownership graphs, entity resolution, analyst review, legal controls | [research](../research/NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md) · [supply chain](../research/NARRATIVE-SUPPLY-CHAIN.md) · [ownership](../research/OWNERSHIP-FUNDING-AND-INCENTIVES.md) · [risks](../research/NARRATIVE-INTELLIGENCE-RISK-REGISTER.md) | 2026-07-21 |

### Research priority

Separate from readiness. **Research priority is about what to investigate next; it says nothing
about what is buildable.**

| Use case | Priority | Why |
|---|---|---|
| Crisis Simulation and Decision Support | **HIGH** | It is the product. It just failed its first usability test with a first-time user |
| Adaptive Futures Engine | **HIGH** | Blocked on one measurement — [does MERIDIAN under-disperse?](https://github.com/CypherTechAries/project-meridian/issues/26) — which also matters for the current product |
| Training, Exercises and Wargaming | **MEDIUM** | Research says it is the strongest commercial direction, and it needs no truth boundary crossed |
| Narrative Supply-Chain Analysis | **MEDIUM** | High value as an internal input to the futures engine; low value and high risk as a standalone product |
| Simulation-Born Entities | **PARKED** | Coherent, well-documented, and dependent on an entity model that does not exist |

---

## Status meanings

| Status | Meaning |
|---|---|
| **WORKING NOW** | A meaningful version is implemented and usable |
| **EARLY DEMONSTRATION** | A bounded implementation exists; it is not a complete product |
| **UNDER RESEARCH** | Being investigated. Not implemented |
| **FUTURE DIRECTION** | Coherent enough to preserve; not on the roadmap |
| **NOT IMPLEMENTED** | Mentioned for clarity; does not exist |
| **RETIRED** | Abandoned. Kept visible rather than deleted |

---

## What MERIDIAN is not

Stated here so a visitor does not have to infer it:

- **Not a prediction engine.** It assigns no real-world probabilities.
- **Not a truth machine.** It calculates no truth scores.
- **Not a digital twin platform.** Nothing it produces has a real-world counterpart.
- **Not a human-behaviour predictor.**
- **Not a bot detector**, and it identifies no coordinated campaigns.
- **It does not ingest the web** and holds no information about any real person or organisation.

---

## Maintenance rules

1. **Update the register whenever research reveals a credible new use case** — and only then. Do not
   add speculative entries to make the folder look full.
2. **Update a status only when evidence on `main` supports the change.** Not when a branch exists,
   not when a PR is open, not when it feels close.
3. **Every use case must name its missing capabilities**, specifically. "More work needed" is not a
   missing capability.
4. **Every use case carries a last-reviewed date.**
5. **Abandoned ideas are marked RETIRED, not deleted.** The reasoning stays useful.
6. **A research finding links to a use case only when there is a genuine product application.**
   Interesting research without an application stays in `docs/research/`.
7. **A use case is not a roadmap commitment.**
8. **Deep research stays in `docs/research/`.** These briefs summarise and direct; they do not
   duplicate.

### Review checklist

Before changing any brief:

1. Does the description explain the value in plain English?
2. Is its implementation status honest?
3. Does it distinguish demonstrated capability from future direction?
4. Does it identify what remains missing?
5. Does it link to supporting evidence?
6. Does it avoid claiming prediction, truth or real-world validation?
7. Has it been reviewed since the latest relevant engine change?
