# MERIDIAN — Project Charter

> **Status:** Non-negotiable. This document governs every other document and every line of
> code in this repository. Where the charter and an implementation disagree, the
> implementation is wrong.

> **P0.1 amendment — 19 July 2026.** This charter states the design MERIDIAN is built to
> reach. It is **not** a description of the current codebase, which is a scaffold with a
> five-test suite. Under Phase 0 item P0.1 the original wording has been preserved and
> annotated in place with dated **[P0.1 amendment]** notes wherever a passage would otherwise
> read as a claim about working software. Nothing in the charter's substance has been
> withdrawn or rewritten; the notes record what was believed, what is now known, and when.
> One clause was edited inline — see the note under § The governing principle — because the
> closed audit instructed that specific deletion. The authority for what may be claimed is
> [`docs/delivery/CAPABILITY-CLAIMS.md`](docs/delivery/CAPABILITY-CLAIMS.md).

## The core product

MERIDIAN is not a game with realistic-looking dialogue. It is:

> **A fictional world governed by real-world causal logic.**

The countries, people, treaties and crises are fictional. The *mechanisms* behind them
behave like the real world:

- Governments have legal authority, but not unlimited authority.
- Militaries have capabilities, readiness limits, logistics and chains of command.
- Money has to come from somewhere.
- Procurement takes time.
- Officials have competing incentives.
- Courts, parliament, media, allies, businesses and citizens react independently.
- International law may not physically prevent an action, but violating it creates consequences.
- Intelligence is incomplete and sometimes wrong.
- Public opinion changes through events, narratives, economic effects and trust.
- Every action creates second- and third-order effects.

> **[P0.1 amendment — 19 July 2026]** The list above states the mechanism set MERIDIAN is
> designed around. **None of it is implemented.** In the current scaffold no tier reads another
> tier's state, each action type maps to one constant effect applied immediately and in full,
> and there is no cost, cooldown, decay, budget, prerequisite or reversal mechanism of any
> kind (`scaffold/backend/app/simulation/engine.py:35-43`, `:121-130`). The final bullet in
> particular must never be cited as evidence that the simulation propagates effects: the
> apparent macro↔meso movement in this scaffold is shared-random-stream contamination, not a
> modelled cause (`docs/delivery/A3-VERIFICATION-RESULTS.md:142-175`).

A player must be able to propose something unexpected and have the platform respond:

> You can attempt this. Here is what is required, what may stop it, who will resist, what it
> will cost, how long it will take, and what consequences are likely.

That is fundamentally different from presenting a fixed list of choices. Any design that
collapses back into a menu of pre-authored options has failed the charter.

## The governing principle

> **MERIDIAN uses real-world causal systems to govern fictional scenarios. Every material
> simulation outcome must be traceable to world state, applicable rules, institutional
> incentives, resource constraints, network effects, recorded uncertainty or seeded
> stochastic resolution. Generated narrative alone must never alter authoritative state.**

This is the charter-level statement of the determinism boundary that
[`scaffold/docs/ARCHITECTURE_DECISIONS.md`](scaffold/docs/ARCHITECTURE_DECISIONS.md)
(ADR-006) records as an architectural commitment.

> **[P0.1 amendment — 19 July 2026]** This sentence previously read: "…(ADR-006) enforces in
> code and `test_llm_gateway_cannot_write_state` guards in CI." Both halves were false and
> the clause was deleted inline on the closed audit's explicit instruction
> (`docs/delivery/CURRENT-STATE-AUDIT.md:427`; publication blocker B2). **There is no
> continuous integration** — no workflow directory, no workflow file, and the only YAML in the
> tree is `scaffold/docker-compose.yml` — so nothing runs automatically on change. And
> `test_llm_gateway_cannot_write_state` does not guard the boundary: it calls the stub gateway
> once and asserts the returned object is an `ActionProposal` with no attribute named
> `apply_deltas` and no attribute named `macro_state`
> (`scaffold/backend/tests/test_engine.py:61-77`). It performs no import-graph analysis,
> attempts no mutation and exercises no real model, so a gateway that mutated authoritative
> state by any other route would pass it unchanged. The boundary itself is currently satisfied
> trivially, because no language model is invoked at all. **TARGET, not delivered:** structural
> enforcement plus a check that would fail if a gateway acquired a write path to authoritative
> state, running on every change (Phase 0 items P0.3 and P0.1).

## What "realism" means here

It does **not** mean claiming perfect prediction. MERIDIAN is a simulation and training
system, not a forecasting tool. It means every result is:

- **Internally consistent** — it does not contradict the world state that produced it.
- **Grounded in recognised real-world mechanisms** — named, citable, and inspectable.
- **Sensitive to the facts of the scenario** — the same action in a different world state
  produces a different outcome.
- **Explainable** — the causal chain can be walked backwards.
- **Contestable where the real world is contested** — the model does not manufacture
  certainty about genuinely disputed mechanisms.
- **Reproducible** — same seed, same scenario, same decisions ⇒ identical numeric state.
- **Capable of producing unintended consequences** — including consequences no one authored.

An action may have several plausible outcomes. The system models a **distribution**, rather
than pretending there is one objectively correct future.

> **[P0.1 amendment — 19 July 2026]** Two of the seven bullets above, and the distribution
> sentence, describe intentions that the code does not support. They are preserved as stated
> intent and annotated here rather than rewritten.
>
> **"Reproducible — same seed, same scenario, same decisions ⇒ identical numeric state"**
> (audit §6.1). The `⇒` clause is not supported. Submitted decisions never reach the tick loop
> at all — `POST /runs/{id}/decision` appends to an in-memory list that `step()` never reads
> (`scaffold/backend/app/api/routes_simulation.py:80-101`;
> `scaffold/backend/app/simulation/engine.py:147-180`) — and the determinism test compares only
> the final macro dictionary, never cohort beliefs, narrative adoption, the event log or the
> snapshot history (`scaffold/backend/tests/test_engine.py:34-40`). The cleared statement of
> what is true today, to be used verbatim, is: "The existing stubbed execution path reproduces
> the same tested numeric outputs when the seed, scenario and stubbed agent outputs remain
> identical." **TARGET, not delivered:** "Given the same scenario version, rule-pack version,
> seed, ordered player inputs and recorded external-agent inputs, the engine is intended to
> reproduce identical authoritative state hashes." Both sentences are founder-settled; do not
> paraphrase or shorten either. There are also no named RNG substreams, so a draw added in one
> subsystem silently shifts every later draw everywhere else — Phase 0 item P0.4A.
>
> **"The system models a distribution"** (audit §6.1 item 6). There is no distribution. Each
> action type maps to one fixed set of constant effects: `ACTION_EFFECTS` is a seven-entry
> table (`scaffold/backend/app/simulation/engine.py:35-43`) and `_validate_and_price` returns
> `dict(base)` — a per-action constant (`:121-130`). `Outcome.confidence` is never constructed.
> The one stochastic element in the engine is a single seeded uniform draw per tick applied to
> one indicator (`engine.py:132-136`). **TARGET, not delivered.**
>
> **Deliberately not annotated:** the bullet "Capable of producing unintended consequences".
> It is not identified by the closed audit and ruling on it here would expand the false-claims
> population and amend the charter without the owner. It is open question OQ-6 in
> `docs/delivery/CAPABILITY-CLAIMS.md`.

### Worked example

**Decision:** Seize control of a foreign-operated port.

A credible causal chain the engine should be able to produce without any of it being
explicitly scripted:

```text
Emergency order issued
→ port operator challenges authority
→ software licences are suspended
→ throughput falls
→ shipping insurers raise premiums
→ government approval initially rises
→ local exporters begin losing revenue
→ foreign investor confidence declines
→ affected state threatens asset freezes
→ opposition demands publication of legal advice
→ internal documents are leaked
```

None of that requires the scenario to be real. It requires the mechanisms to be credible.

## The causal vocabulary

Unexpected player actions are translated into reusable **consequence primitives**. The
engine composes these into outcomes it was never explicitly scripted to produce — this is
where the apparent endlessness of the simulation comes from.

> **[P0.1 amendment — 19 July 2026]** Both sentences above describe a **target**, not current
> behaviour, and neither part is implemented. **No consequence-primitive vocabulary exists in
> the codebase**: the sixteen primitives tabulated below appear in this charter and in no
> module, schema or test. Nothing translates a player action into them — the decision endpoint
> appends the submission to an in-memory list and applies no effect (`routes_simulation.py:80-101`;
> see the amendment under "The standard for every state change"). And the engine composes
> nothing: every action resolves through a fixed seven-entry `ACTION_EFFECTS` table returning
> constant deltas (`engine.py:37`, `engine.py:121-130`), touching only three national indicators
> — `government_approval`, `military_readiness` and `social_stability_index`. An outcome the
> engine "was never explicitly scripted to produce" is therefore currently impossible: every
> outcome it can produce is explicitly scripted, and there are seven of them. The "apparent
> endlessness" is a design intention for the composition engine described in
> `docs/delivery/PHASE-0-REMEDIATION-PLAN.md`, not an observed property of this scaffold.
> The table below should be read as the specified vocabulary, not as an implemented one.

| Primitive | Effect class |
|---|---|
| Spend or reserve resources | Resource |
| Transfer or seize assets | Resource |
| Change legal status | Legal |
| Create an obligation | Legal |
| Trigger an approval process | Procedural |
| Delay an operation | Temporal |
| Change institutional behaviour | Institutional |
| Alter a relationship | Relational |
| Change a belief | Informational |
| Create public exposure | Informational |
| Generate economic disruption | Economic |
| Create diplomatic retaliation | External |
| Open a legal challenge | Legal |
| Expose or conceal information | Informational |
| Create operational risk | Risk |
| Enable or remove future options | Optionality |

Player intent is parsed into a composition of these primitives, then priced, validated and
resolved by the engine. The LLM may *propose* a composition; it never decides whether the
composition is legal, what it costs, or whether it succeeds.

> **[P0.1 amendment — 19 July 2026]** "then priced, validated and resolved by the engine" is
> a **target**, not current behaviour, and is publication blocker B1. Player intent is not
> parsed into primitives at all: the decision endpoint appends the client's submission to an
> in-memory list, returns `accepted: true` unconditionally, applies no effect, and stores the
> client's own `legal_check` value unexamined (`routes_simulation.py:80-101`). Nothing prices
> or validates it on that tick or any later one. On the engine side, the gate performs no
> legality check, no feasibility check and no cost computation: `_validate_and_price` looks the
> action type up in a fixed seven-entry table and returns a copy of the row
> (`engine.py:121-130`). It is never passed the agent specification, so an agent's declared
> `constraints` are structurally unreachable from it — proven by substitution, a 40-tick state
> hash identical with and without them (`docs/delivery/A3-VERIFICATION-RESULTS.md:92-98`).
> **The second sentence is unaffected and stands as written:** the LLM proposes and never
> decides legality, cost or success. Correcting the text is what clears B1; building the
> evaluator is not required for publication (`A3-VERIFICATION-RESULTS.md:241`).

## The standard for every state change

Every meaningful outcome must be able to answer all eight questions:

1. What happened?
2. What caused it?
3. Which rule or mechanism applied?
4. Which actors reacted?
5. What assumptions were used?
6. What uncertainty existed?
7. What alternative outcomes were possible?
8. What future options changed?

**If the system cannot answer these questions, the output is flavour text, and flavour text
must not be allowed to modify the simulation.**

This is the difference between fiction with realism and an LLM inventing consequences that
merely sound convincing.

## Scope and honesty constraints

- Fictional scenarios only. No real nations, organisations, named individuals, or real
  operational vulnerabilities.
- MERIDIAN is simulation and training software — **not** a predictive intelligence tool and
  **not** a real-world forecasting system.
- Every AI-generated advisory text carries a visible provenance tag distinguishing it from
  engine-computed fact, at the interface level and not merely in a documentation footnote.

> **[P0.1 amendment — 19 July 2026]** The three bullets above are **stated intentions and
> scope constraints, not implemented controls**, and must not be presented as implemented
> controls anywhere. Specifically, on the third: **no provenance tag exists at any interface.**
> None of the five REST responses carries a disclaimer or provenance field
> (`scaffold/backend/app/api/routes_simulation.py:47-49`, `:60`, `:71-77`, `:101`, `:111`), and
> a case-insensitive search of `scaffold/frontend/` for "fiction", "provenance", "AI-generated"
> and "disclaimer" returns nothing. The only marker on generated text is a literal
> `[STUB briefing — tick N]` prefix inside the string itself
> (`scaffold/backend/app/simulation/llm_gateway.py:100`). On the first: the scenario file
> carries a free-text `fiction_disclaimer` that no code reads and no interface displays
> (`scaffold/scenarios/kestral-strait.json:7`); no schema asserts fictionality and no check
> runs at scenario load beyond parsing the file. **TARGET, not delivered.** This is publication
> blocker B5, the only blocker that cannot be cleared by correcting text. The founder settled
> the dual-use position on 18 July 2026 and named eight controls; **none of the eight exists in
> code**, and B5 clears only when they are implemented and verified. See
> `docs/delivery/PUBLICATION-EXIT-CRITERIA.md` C6.
