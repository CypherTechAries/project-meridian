# MERIDIAN — Project Charter

> **Status:** Non-negotiable. This document governs every other document and every line of
> code in this repository. Where the charter and an implementation disagree, the
> implementation is wrong.

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
(ADR-006) enforces in code and `test_llm_gateway_cannot_write_state` guards in CI.

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
