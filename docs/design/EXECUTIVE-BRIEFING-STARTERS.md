# Executive Briefing — revised starters and response design

**DESIGN ONLY.** No frontend code, no engine change, no simulation behaviour changed.

Mockups: [`v6-1-executive-home.png`](mockups/v6-1-executive-home.png) ·
[`v6-2-brief-me-response.png`](mockups/v6-2-brief-me-response.png) ·
[`v6-3-public-sentiment-response.png`](mockups/v6-3-public-sentiment-response.png) ·
[`v6-4-future-intelligence.png`](mockups/v6-4-future-intelligence.png) ·
[`v6-5-future-option-comparison.png`](mockups/v6-5-future-option-comparison.png) ·
[`v6-6-future-commanders.png`](mockups/v6-6-future-commanders.png) ·
[`v6-7-narrow-screen.png`](mockups/v6-7-narrow-screen.png) ·
source [`executive-briefing.html`](mockups/executive-briefing.html)

## What was wrong

The old starters assumed you already knew the cast. *"Why is Mara still unsure?"* is meaningless to a
first-time visitor, and *"Who never received the claim?"* is a good analytical follow-up but not
something a head of government asks on entering a crisis room. **Both removed.** Mara returns later
as a follow-up chip, after the user knows who she is.

Workspace label: **EXECUTIVE BRIEFING**. Not "president" or "commander-in-chief" — the platform is
also for exercises, research, world-building and agent evaluation. Suggested questions adapt to the
declared fictional role; this mockup is the head-of-government configuration.

## Current versus future capability

| Question | Status | Rests on |
|---|---|---|
| Brief me on the current situation | **AVAILABLE NOW** | Crisis engine, nine-step chain, canonical map, cohort weights |
| How are the economy and supply chains reacting? | **AVAILABLE NOW** | Insurer, rerouting, port, employment, household, political mechanisms + counterfactuals |
| How is public sentiment changing? | **AVAILABLE NOW** | Belief slice: people, organisations, cohorts, exposure paths |
| What does MERIDIAN know — and what remains uncertain? | **AVAILABLE NOW** | Origin markers, unavailable/not-modelled states, Analysis View |
| Intelligence on external actors | **FUTURE — NOT IMPLEMENTED** | No intelligence layer, no external actors, no attribution model |
| The information environment | **FUTURE — NOT IMPLEMENTED** | No social-platform layer, no narrative coordination model |
| Diplomatic options | **FUTURE — NOT IMPLEMENTED** | No options model, no partner responses, no consequence computation |
| Military recommendations | **FUTURE — NOT IMPLEMENTED** | No commanders, no security options, no escalation model |
| Compare my options | **FUTURE — NOT IMPLEMENTED** | Depends on all of the above |

**Also true today and reflected in the wording:** the conversational interface itself, the LLM, and
Plan and Command modes are all unimplemented. Every mockup carries
`DESIGN MOCKUP — NOT IMPLEMENTED SOFTWARE`, and the four future screens carry a second banner.

## Deliberate wording choices

**"Economy and supply chains", not "financial markets."** No stock prices, currencies or market data
are modelled. Shipping, insurance, ports, jobs and households are.

**"Public sentiment" and "the information environment", not "social-media sentiment."** No
social-platform layer exists. The future card says clearly that it would show *fictional* platform
activity — never real accounts, real-person profiling, private messages, surveillance or
real-population targeting.

**"External actors" and "possible influence operations", not "hostile states."** The second assumes
guilt before evidence supports it, which is the failure mode the whole intelligence design exists to
prevent.

## Component status in every response

`E` engine · `F` fixture · `P` proposed, does not exist · `S` simulated character · `?` unavailable
or not modelled

| Component | Status |
|---|---|
| Map, coastline, blockade, routes | **E** geometry + state, `F` place names |
| Crisis status, day count | **E** |
| Affected-group names and populations | **F** name, **E** population and result |
| Group movement wording | **E** value → derived band wording |
| "Group averages… does not model individuals" | **?** permanent disclosure |
| Decision card | **E** threshold state, **F** option text |
| Person results | **E** · person **names and portraits** | **P** |
| Organisation positions, cohesion, strength | **E** · names, objectives **F** |
| Exposure path, reach figures | **E** |
| "What MERIDIAN does not know" panel | **?** |
| Intelligence: observed event | **E** *if built* — marked as such |
| Intelligence: assessment, confidence, dissent | **S** simulated character |
| Diplomatic and military options | **S** + **NOT EXECUTED** |
| Option comparison costs, risks, timings | **declared properties of a proposal**, not computed — shown as `Not modelled` |
| Commander and adviser statements | **S** + **NOT EXECUTED** |

## Intelligence honesty

Confidence is **never a single score**. The mockup splits it:

| | |
|---|---|
| Confidence the event occurred | **HIGH** — coordination observed |
| Confidence about who caused it | **LOW** |
| Confidence about intent | **LOW** |
| Source reliability | single method, uncorroborated |
| Competing explanation | domestic activists using shared material |
| Dissent | one analyst reads the timing as coincidental |
| Missing | account provenance, funding, prior history |

**Why they are separate:** one merged score lets high confidence that *something happened* carry low
confidence about *who did it* across the line into apparent certainty. That is how an assessment
becomes a fact without anyone deciding it should.

## Cabinet and commander honesty

Advisers are simulated characters — possibly incomplete, mistaken, self-interested, institutionally
biased, or working from partial evidence. In mockup 6 a commander and a legal adviser disagree, and
**MERIDIAN does not arbitrate.** It states what the engine supports (blockade active five days,
shipping rerouted, port activity down, political pressure near peak) and says plainly that escalation
risk is a stated judgement, not a computed result.

**Confidence of delivery is not evidence.** The guide never resolves a disagreement because one
account sounds surer.

## Execution boundary

**Explore** asks and retrieves, changes nothing. **Plan** produces structured proposals, changes
nothing, always shows `NOT EXECUTED`. **Command** interprets, shows the structured action, validates
fictional targets, names missing information, and requires explicit confirmation before anything
reaches the engine.

No chat message silently changes state. No cabinet recommendation silently becomes policy. No
military recommendation silently becomes an order.

## Narrow screen

Rail and context column collapse into a single column. Starters keep the same two labelled sections
and the same `FUTURE — NOT IMPLEMENTED` tags. **The context map follows the starters rather than
disappearing** — it is evidence, not decoration.

## Map

Every map preview is the canonical Briefing component — same coastline paths, route paths, blockade
geometry and CSS classes, differing only by viewBox crop and which optional layers render. **No
simplified map was introduced.**

## Confirmation

**No future feature is presented as implemented.** Future cards are dashed, dimmed, and each carries
`FUTURE — NOT IMPLEMENTED`; the four future response screens carry a full-width banner naming exactly
what does not exist. Selecting a future card would show a capability explanation, never a fabricated
answer.

PR #14 stays draft and unmerged. PR #15 unchanged.
