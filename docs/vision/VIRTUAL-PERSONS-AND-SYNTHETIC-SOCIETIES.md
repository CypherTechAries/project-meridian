# Virtual persons and synthetic societies

> # ⚠ LONG-TERM VISION — NOT IMPLEMENTED
>
> **Nothing in this document exists in MERIDIAN's code, and nothing here is a commitment to a
> release.** It describes a possible future direction. No sentence below may be quoted as a
> capability. The authority for what may be claimed about the current codebase is
> [`../delivery/CAPABILITY-CLAIMS.md`](../delivery/CAPABILITY-CLAIMS.md); the authority for what is
> planned and in what order is [`../../PROJECT-ROADMAP.md`](../../PROJECT-ROADMAP.md). Where this
> document and either of those disagree, they govern and this one is wrong.

**Status:** vision note. Founder-authored direction, recorded 19 July 2026.
**Type:** possible future. Not implemented, not scheduled, not claimed.

MERIDIAN keeps three categories visibly separate, and this document is firmly in the third:

| Category | Where it is recorded |
|---|---|
| **Implemented now** | [`../delivery/CAPABILITY-CLAIMS.md`](../delivery/CAPABILITY-CLAIMS.md) — with evidence, and with the wording that may be used |
| **Planned next** | [`../../PROJECT-ROADMAP.md`](../../PROJECT-ROADMAP.md) — v0.1 scope, then the v0.2–v1.0 release map |
| **Possible future** | **this document** — direction only |

---

## Vision

MERIDIAN begins as a fictional simulated-society environment for examining how crises and
information propagate through institutions, markets, communities and political systems.

Its longer-term potential extends beyond scenario simulation.

A sufficiently mature synthetic-society platform could support persistent **virtual people**:
artificial entities with stable identities, personal histories, relationships, memories, beliefs,
skills, responsibilities and evolving goals.

These entities would not be generated biographies wrapped around a chatbot. Their identity and
history would exist as structured, persistent state. They would observe only the information
available to them, update beliefs through recorded experiences, maintain relationships, operate
within institutional constraints and remain accountable for their actions.

**No claim of consciousness, sentience, personhood or human equivalence is made or intended.**
"Virtual person" is a term for a modelled entity, not a claim about inner life.

---

## From simulated agents to virtual people

A persistent virtual person may eventually contain:

- a stable fictional identity and life history;
- long-term and short-term memory;
- proposition-specific beliefs and uncertainty;
- attitudes, emotions and issue stances;
- skills and professional experience;
- goals, obligations and commitments;
- relationships and social reputation;
- organisational roles and authority;
- an observation history;
- tools and bounded task capabilities;
- a record of decisions and consequences.

Large language models may support interpretation, planning, communication and flexible reasoning.
**They should not independently own authoritative state.** MERIDIAN's deterministic systems would
continue to control permissions, resources, accepted actions, persistent identity and consequential
state transitions — the boundary the project already treats as its most important rule.

### Memory would need structure, not transcripts

Memory would require layers — recent experience, significant long-term memory, factual knowledge,
beliefs and uncertainties, relationships, learned procedures, and unfinished commitments — together
with **forgetting, compression and selective retrieval**. Passing a synthetic person's entire
transcript to a model on every call would be both prohibitively expensive and unlike memory.

### Agency would be a loop, not a reply

Observe the permitted environment → interpret → update knowledge and beliefs → decide whether
anything requires attention → form or revise plans → use tools → act → observe the result → learn.
A deterministic system governs permissions, resources, commitments and authoritative effects at
every step.

---

## Synthetic people within synthetic societies

The central opportunity is not only better individual AI assistants. It is modelling artificial
people as **members of societies**.

A synthetic person may belong to a family, workplace, community, institution or political group. It
may trust some sources and distrust others. It may develop a reputation, form commitments, disagree
with colleagues, change roles, and influence or be influenced by others.

This makes it possible to examine behaviour that cannot be understood by modelling isolated agents:
information diffusion · institutional incentives · social trust · collective action · organisational
disagreement · market response · political pressure · community resilience · long-term cultural
change.

---

## Potential applications

- fictional crisis and information-resilience exercises;
- evaluation of defensive responses to misinformation;
- training and education;
- persistent characters in interactive worlds;
- organisational simulations;
- AI-agent evaluation environments;
- bounded digital workers with persistent responsibilities;
- research into multi-agent cooperation and institutional behaviour.

MERIDIAN's initial focus remains **fictional environments and defensive understanding**. It is not
intended to optimise manipulation of real people or populations, and the constraints in
[`../design/BELIEF-SENTIMENT-VERTICAL-SLICE.md`](../design/BELIEF-SENTIMENT-VERTICAL-SLICE.md) §5–§6
— no persuadability ranking, no susceptibility scoring, no audience optimisation — are intended to
hold as the platform grows, not only for the first slice.

### As an AI-evaluation environment

A controlled synthetic society is a way to ask questions about agents that a single conversation
cannot: does an agent preserve commitments over long horizons? Does it update beliefs appropriately
on new evidence, and resist misleading information? Can it cooperate without leaking restricted
information? Does it behave consistently under institutional pressure? What happens when many agents
interact?

---

## Computational architecture

Continuously running a large reasoning model for every simulated person would be inefficient and
unnecessary. A scalable system may combine fidelity levels:

```text
millions represented statistically
  → thousands as cohorts and social-network nodes
    → hundreds as persistent lightweight agents
      → dozens active as high-fidelity synthetic people
        → a small number using expensive reasoning at any moment
```

Most entities remain inexpensive until an event, relationship or decision makes greater fidelity
necessary. Memory is retrieved selectively. Routine updates use deterministic rules, statistical
models or small specialised models; expensive reasoning is reserved for consequential or ambiguous
situations. Promotion of an entity to higher fidelity must itself be **deterministic**, so that a
run remains reproducible.

The insight this rests on is that the enabling advance may not be a single vastly more powerful
model, but an **architecture that allocates intelligence only where and when it matters**. This is
the same fidelity-tier idea already recorded in
[`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md).

---

## Safety and identity

Virtual people must remain clearly artificial. The platform should prohibit:

- impersonation of real people;
- undisclosed artificial identity;
- unbounded accumulation of authority;
- real-population persuasion optimisation;
- exploitation of protected traits or vulnerability;
- unauditable consequential actions.

Persistent memory, identity, permissions and deletion require explicit governance. Human operators
remain responsible for systems deployed into real organisations. Consequential actions must be
explainable in terms of the state and evidence that produced them.

**A deep personality must never become a mechanism for deception.**

These requirements are continuous with, not separate from, the **B5 controls** that MERIDIAN must
implement before public v0.1 — see [`../../PROJECT-ROADMAP.md`](../../PROJECT-ROADMAP.md). B5 is the
first instalment of this safety posture, not a one-off release gate.

---

## Near-term relationship to MERIDIAN

The roadmap builds foundations that may support this direction. Mapped to the recorded release map,
so ambition and schedule stay distinguishable:

| Foundation | Release |
|---|---|
| Deterministic societal mechanisms | **v0.1** (built) |
| Persistent fictional people and organisations | v0.2 |
| Relationships, trust and beliefs | v0.3 |
| Differential information exposure | v0.3 |
| Behaviour and social influence | v0.3–v0.4 |
| Controlled behavioural-model and LLM integration | v0.5 |
| Memory, events and deterministic replay | v0.6 |
| Scalable fidelity tiers | v0.7+ |
| Bounded task execution | beyond v1.0 |

**The immediate project remains an early simulated-society prototype.** Virtual persons are a
possible future built on that foundation, not a capability MERIDIAN claims today.
