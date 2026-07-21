# Narrative Supply-Chain Analysis

**Status: UNDER RESEARCH**
**Last reviewed: 21 July 2026** (against `main` at `bfd2aa7`)

*Internal research-strand name: Narrative and Incentive Intelligence.*

> **MERIDIAN currently performs no real-world ingestion or analysis.**
>
> - It does not ingest the web.
> - It contains no information about any real person or organisation.
> - It does not detect bots.
> - It does not identify coordinated campaigns.
> - It does not calculate truth scores.
> - It does not generate allegations.

## In one sentence

Trace how claims originate, spread and change, while showing source dependence, ownership,
incentives, amplification and missing perspectives.

## The problem

Most tools for contested information ask *"is this true?"* — then label an outlet left or right, or
hand you a score. That question is usually unanswerable from public information, and the answer is
rarely the useful part.

Meanwhile, fifteen outlets reporting the same thing **looks** like corroboration. If fourteen trace
back to one anonymous briefing, it is one source repeated fourteen times — and nothing on the page
tells you which situation you are in.

## How MERIDIAN could help

Ask the answerable questions instead: where did the claim begin, how many genuinely independent
origins support it, how did the wording change on the way, which sources rely on one another, what
ownership or funding or access sits behind them, what is missing, and **what cannot be established
at all**.

> **Do not tell the user what to believe. Show them how belief is being constructed.**

## A simple example

A claim appears that a disruption was caused by an external actor. Seventeen outlets carry it. The
analysis shows three appear to provide independent evidence, six could not be traced, and the rest
lead back to two official briefings. Along the way "may have been" became "was" and a caveat
disappeared. Several parties would benefit if it were believed — **which is potential incentive
alignment, not proven coordination**. Local witnesses dispute the timeline, and original-language
reporting from the affected area is limited.

No verdict on truth. A much clearer picture of what the evidence actually is.

## Who might use it

Journalists and investigative researchers; analysts; NGOs; corporate risk teams — **and, most
usefully, the [Adaptive Futures Engine](ADAPTIVE-FUTURES-ENGINE.md)**, which cannot model
organisations realistically without modelling the information they act on.

## What MERIDIAN already has

**Inside the fiction only** — none of this touches real information:

- **Information-exposure records** — who received what, when.
- **"Not received" distinct from rejection** — the most directly relevant existing property.
- **Belief histories**, append-only.
- **Contextual trust** — trust varies by subject, not one number.
- Organisations, people and population groups modelled separately.
- Origin and absence labels; declared model boundaries.
- **B5 prohibitions** — no protected-trait targeting, no persuadability optimisation.

## What is still missing

Everything operational: **web ingestion**; multilingual retrieval; source archives; **claim
lineage**; **source-independence analysis**; ownership and funding graphs; financial records;
**entity resolution**; translation validation; coordination detection; campaign detection;
media-ownership data; incentive assessment; adversarial testing; **analyst review**; and legal and
ethical controls.

## What it must never claim

- **A truth score.** There is none, and there must never be one.
- That a connection proves control. **Ownership, investment, funding, access or shared interests can
  explain possible incentives and dependencies. They do not by themselves prove editorial control,
  common intent or organised coordination.**
- That accounts are bots.
- That activity was coordinated, without direct evidence of organised activity.
- That it measures the *impact* of a campaign. Volume measures adversary spend, not success.
- That its evidence base is neutral. Any output must state where its evidence came from.

## Key risks

- **Becoming a conspiracy generator** — the defining risk. Every ownership map contains connections,
  and readers read connection as coordination.
- **Harming a named individual** through a probabilistic inference. Legitimate communities —
  fandoms, unions, diaspora groups, campaigners — coordinate constantly and lawfully.
- **Reproducing the dominant information environment**, which is the *default* outcome of building
  on the English-language internet.
- **Legal exposure.** Recording political positions about named people probably engages special
  category data; defamation defences **require a human to have held a belief**; and individual
  scoring could risk the EU AI Act's social-scoring prohibition. **All provisional — see the research.**
- **Ten uncontrolled risks** sit on this concept's critical path.

**Coordination detection is not a committed capability**, may be unsuitable for implementation, and
is required by none of the strongest uses. The project may decide never to build it.

## Supporting research

[Narrative and Incentive Intelligence](../research/NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md) — the
full 26-section report ·
[Narrative supply chain](../research/NARRATIVE-SUPPLY-CHAIN.md) ·
[Ownership, funding and incentives](../research/OWNERSHIP-FUNDING-AND-INCENTIVES.md) ·
[Multilingual and regional bias](../research/MULTILINGUAL-AND-REGIONAL-INFORMATION-BIAS.md) ·
[Coordinated amplification and bot methodologies](../research/COORDINATED-AMPLIFICATION-AND-BOT-METHODOLOGIES.md) ·
[Risk register](../research/NARRATIVE-INTELLIGENCE-RISK-REGISTER.md) ·
[Source register](../research/NARRATIVE-INTELLIGENCE-SOURCES.md) ·
[Concept note](../design/NARRATIVE-INTELLIGENCE-CONCEPT.md)

## Next proof required

**Entirely fictional, and available now.**

Build a **simulated information environment** inside an existing scenario: different people and
organisations receiving different claims at different times, from sources of differing independence,
with strategic framing and delayed corrections. Feed it to the existing belief rules.

**It needs no real ingestion, no real names, no legal exposure and no ethics review** — and it is the
research's own recommendation for the highest-value first use.

Only after that, and only with legal advice, would a second experiment be worth considering: one
historic, archived, already-researched contested event, one claim traced through 20–50 publications
**by hand**, compared against what later turned out to be true — documenting the false positives.

**No live monitoring. No collection. No real-person profiling. No accusations.**
