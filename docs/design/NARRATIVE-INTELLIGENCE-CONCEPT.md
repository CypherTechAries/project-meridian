# Narrative and incentive intelligence — concept note

**Status: RESEARCH ONLY.** Nothing described here exists. MERIDIAN does not read the web, does not
analyse real sources, and does not hold any information about real people or organisations. This
note explains the idea and where it might eventually fit; the detailed research is in
[docs/research/NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md](../research/NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md).

---

## The idea in one paragraph

Most tools that try to help you with contested information ask *"is this true?"* — and then either
label an outlet left or right, or hand you a score. That question is often unanswerable from public
information, and the answer is rarely the useful part. A different question is answerable and more
useful: **where did this claim come from, how many genuinely separate sources support it, who
benefits if you believe it, and what is missing?** Fifteen outlets reporting the same thing sounds
like corroboration. If fourteen of them trace back to one anonymous briefing, it is one source
repeated fourteen times — and knowing that changes what you should think, without anyone having to
adjudicate the truth.

## The governing principle

> **Do not tell the user what to believe. Show them how belief is being constructed.**

## Why it matters to MERIDIAN specifically

MERIDIAN simulates how societies respond to crises. People in those simulations act on information —
and real information is incomplete, strategically framed, commercially motivated and sometimes
deliberately manipulated. A crisis simulation whose people receive clean, neutral facts is modelling
a world that does not exist.

**This strand is therefore not only a possible product. It is an input the futures work needs.**

---

## What it would actually do

For a contested event, it would try to answer seven questions:

1. **What is being claimed?**
2. **Where did the claim come from?**
3. **How independent is the reporting?** — the count that matters
4. **How did the wording change** as it travelled?
5. **Who may benefit** if it is believed?
6. **What challenges it,** and what is missing?
7. **What can't be established?**

The last one is not a disclaimer. It is a section of the output with the same weight as the others.

## What it must never be

**Not a truth machine.** There is no truth score and there must never be one. Eight separate things
— evidence, independence, quality, reach, incentive alignment, coordination confidence, coverage
diversity, unresolved alternatives — stay separate, because combining them makes all of them
unfalsifiable at once.

**Not a conspiracy generator.** A financial connection is evidence of an *incentive*. It is not
evidence that anybody coordinated anything. Seven relationship categories — from direct control down
to mere correlation — are kept apart, and only one of them supports a coordination claim.

**Not a bot detector.** The published record here is poor: the tool underpinning most "X% of
discourse is bots" research has documented precision as low as 24–59%, and no live data since 2023.
The honest claim is about **observed behaviour**, not about what an account *is*.

**Not automated accusation.** No output naming a real person or organisation would be published
without a human deciding to publish it.

---

## How it differs from what exists

We looked at 24 adjacent services. The pattern is clean:

- **Consumer tools** (Ground News, NewsGuard, AllSides, Ad Fontes) measure **content slant**. With
  one partial exception they touch **none** of ownership, funding, incentives, source independence
  or coordination.
- **Threat-intelligence firms** (Graphika, Blackbird, Recorded Future, and the platform teams) do
  **coordination** — and never ownership or funding.
- **Ownership databases** (OpenCorporates, Sayari, Aleph, OpenSanctions, LittleSis) do **ownership**
  — and never narrative or amplification.

**The join is empty.** The only work that does both is hand-built investigative journalism — EU
DisinfoLab's "Indian Chronicles" is the model — which is a finding about difficulty as much as
opportunity.

---

## The honest warnings

**The market is contracting, for political rather than technical reasons.** Logically raised £30m,
held platform and government contracts, and entered administration in July 2025 after Meta and
TikTok withdrew from third-party fact-checking. Meta halved its coordinated-behaviour reporting
cadence. Google removed fact-check markup from Search. NewsGuard is litigating against a US
regulator and is barred from state contracts in Florida. **Every business model here that depended
on platform budgets or on being accepted as a neutral arbiter has been damaged since 2024.**

**Access to data is closing, not opening.** The EU's public beneficial-ownership registers were
struck down in 2022; access is now per-request and per-entity, so you cannot map a network.
CrowdTangle is gone. Aleph is moving to commercial tiers.

**The UK's openness is a trap as well as an asset.** Because the UK PSC register is one of the few
fully public ones left, any ownership analysis will be UK-heavy — and that is an artefact of UK
transparency law, not a fact about the world. And UK records are **self-declared**: identity
verification confirms *who filed*, not *what they filed*.

**85–95% of UK lobbying appears in no register at all**, and ministerial meeting entries average
eleven words. You cannot map UK influence from UK public records alone.

---

## Where it fits

**Not on the roadmap.** MERIDIAN has just failed its first usability test with a first-time user,
and that work decides whether any of this matters. This strand is worth keeping written down because
it changes how the simulation should model information — people receiving different claims, from
sources of differing independence, with strategic framing — and that is cheaper to design in than to
retrofit.

**The safest first demonstration** is deliberately unexciting: take **one historic, well-documented,
already-researched** contested event, trace **one claim** through 20–50 archived publications by
hand, work out which reports are genuinely independent, record how the wording changed, map the
disclosed ownership, compare local-language and English framing, and then compare what the method
concluded against what later turned out to be true — **documenting the false positives**.

No live monitoring. No social-media collection. No real-person profiling. No accusations. The
question it answers is whether the method produces anything a careful human could not have produced
faster on their own — and **a "no" would be a genuinely useful result.**
