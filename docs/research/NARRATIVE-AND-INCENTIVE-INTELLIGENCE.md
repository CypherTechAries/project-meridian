# Narrative and incentive intelligence

**Research report. Nothing here is implemented and nothing here is a commitment.**

> ## What MERIDIAN does today
>
> - **MERIDIAN performs no narrative intelligence.**
> - **It does not ingest the web.**
> - **It contains no information about any real person or any real organisation.**
> - **It does not detect bots.**
> - **It does not identify coordinated campaigns.**
> - **It does not calculate truth scores.**
> - **It does not generate allegations.**
>
> Nothing in this document describes a capability that exists. It investigates whether some of it
> *should* exist eventually, what would have to be true first, and where the idea becomes dangerous.

> ## Coordination detection is not a committed capability
>
> This report examines coordination and bot detection, and **recommends against treating either as a
> milestone.** They carry substantial false-positive and methodological risk, are blind to the most
> effective operations, and **are not required by any of the strongest proposed uses.**
>
> **The project may decide never to build this capability.** Nothing here should be read as a plan
> to. Where such analysis is discussed, it must never be treated as proof of intent or control, and
> any finding naming a real actor would require human review before it went anywhere.

> ## Legal research status
>
> **PROVISIONAL LEGAL RESEARCH — DO NOT RELY ON WITHOUT SPECIALIST REVIEW.**
>
> Several legal positions here rest on secondary sources because the primary source could not be
> retrieved — **every ICO position in particular**, since ico.org.uk returned HTTP 403 to every
> attempt. Claims in that condition are marked **PRIMARY-SOURCE VERIFICATION REQUIRED** at the point
> of use. This is research, not legal advice.

Every claim is labelled:

| Label | Meaning |
|---|---|
| **FACT** | Verifiable and verified |
| **CURRENT LAW / GUIDANCE** | The position per a primary legal or regulatory source, at the access date |
| **DOCUMENTED RELATIONSHIP** | An ownership, funding or contractual link on the public record |
| **RESEARCH FINDING** | Reported in a cited study, standard or investigation |
| **MODEL INFERENCE** | Something a system would conclude, not something observed |
| **PRODUCT PROPOSAL** | Our own design idea. Not validated |
| **OPEN QUESTION** | Genuinely unresolved |

This is not legal advice. Where the report touches law it reports what sources say and marks what
they do not settle.

Companion documents:
[NARRATIVE-SUPPLY-CHAIN.md](NARRATIVE-SUPPLY-CHAIN.md) ·
[OWNERSHIP-FUNDING-AND-INCENTIVES.md](OWNERSHIP-FUNDING-AND-INCENTIVES.md) ·
[MULTILINGUAL-AND-REGIONAL-INFORMATION-BIAS.md](MULTILINGUAL-AND-REGIONAL-INFORMATION-BIAS.md) ·
[COORDINATED-AMPLIFICATION-AND-BOT-METHODOLOGIES.md](COORDINATED-AMPLIFICATION-AND-BOT-METHODOLOGIES.md) ·
[NARRATIVE-INTELLIGENCE-RISK-REGISTER.md](NARRATIVE-INTELLIGENCE-RISK-REGISTER.md) ·
[NARRATIVE-INTELLIGENCE-SOURCES.md](NARRATIVE-INTELLIGENCE-SOURCES.md) ·
[product concept note](../design/NARRATIVE-INTELLIGENCE-CONCEPT.md)

**Derived use case:** [Narrative Supply-Chain Analysis](../use-cases/NARRATIVE-SUPPLY-CHAIN-ANALYSIS.md) — the public-facing name for this strand.

---

## 1. The executive idea

Most tools built for contested information ask *"is this true?"*, then either label an outlet
left-wing or right-wing, or produce a score. That question is usually unanswerable from public
information, and the answer is rarely the useful part.

A different set of questions is answerable, and more useful:

> Where did this claim come from? How many genuinely separate sources support it? Who repeated it
> and how did the wording change? Who benefits if people believe it? Who funds, owns or depends on
> the organisations spreading it? Which perspectives are missing? And what can't be established at
> all?

Fifteen outlets reporting the same thing looks like corroboration. If fourteen trace back to one
anonymous official briefing, it is **one source repeated fourteen times** — and knowing that changes
what a reader should think, without anybody adjudicating the truth.

The governing principle:

> **Do not tell the user what to believe. Show them how belief is being constructed.**

**INFERENCE — why this matters to MERIDIAN specifically.** MERIDIAN simulates how societies respond
to crises, and people in those simulations act on information. Real information is incomplete,
strategically framed, commercially motivated and sometimes deliberately manipulated. **A crisis
simulation whose people receive clean neutral facts is modelling a world that does not exist.** This
strand is therefore not only a possible product; it is an input the futures work needs.

---

## 2. Why normal AI systems reproduce dominant narratives

**INFERENCE**, supported by the sourced material in the companion documents. A system trained or
retrieving mainly on English-language material will mistake:

- the most repeated view for the most accurate view;
- Western institutional consensus for universal consensus;
- many articles copying one source for independent corroboration;
- official access for reliability;
- silence from under-represented regions for absence of disagreement;
- coordinated amplification for organic opinion;
- search visibility for importance.

Three mechanisms drive it, and none is fixed by adding more data.

**Availability.** **CURRENT LAW.** The UK's PSC register is fully public and free. Most of the EU's
equivalent is not: the CJEU struck down public access to beneficial ownership registers in November
2022, and access is now "legitimate interest" only — per request, per entity. **You cannot map a
network.** Roughly 39 of about 104 jurisdictions with a live register have a fully public one.
**Consequence: any ownership analysis will be far richer for the UK than anywhere else, purely
because of disclosure law.** A UK-heavy picture of global ownership is an artefact, not a finding.

**Dataset coverage.** **RESEARCH FINDING.** GDELT, the largest open global news monitor, has
documented false positives in event coding and — more fundamentally — **measures reporting, not
reality**, with countries under press restriction systematically under-represented: precisely where
influence activity most needs detecting. Wikidata, the practical spine for entity resolution, has
documented bias toward established, Western, male, notable entities; one study found **37.7% of
deduplicated persons had no Wikidata link at all**.

**The measuring instruments.** The consumer bias tools are built on a US left/centre/right axis
whose midpoint is definitionally the US political centre — a substantive position, not a neutral
one. Applied outside the US it degrades; applied to non-Western media it is close to meaningless.

---

## 3. What narrative and incentive intelligence means

**PRODUCT PROPOSAL.** The analysis of claim origins, source independence, ownership, funding,
access, relationships, incentives, amplification, omission, changes in framing, and uncertainty.

**A note on the name.** "Intelligence" here means *organised analysis of open information*. It must
never be used to imply secret access, privileged sourcing or certainty. **Alternatives considered:**
*narrative supply-chain analysis* (accurate, but narrow — it omits incentives); *information
provenance* (too technical, and provenance has a specific meaning we would be borrowing); *media
forensics* (implies certainty we cannot deliver); *claim origin analysis* (accurate but bloodless).

**Recommended:** keep **narrative and incentive intelligence** as the internal strand name, and use
**narrative supply-chain analysis** externally — it describes the method rather than claiming a
faculty, and it is the phrase that survives a sceptical reading.

---

## 4. Claim lineage

Full model in [NARRATIVE-SUPPLY-CHAIN.md](NARRATIVE-SUPPLY-CHAIN.md) §3.

A claim travels and changes. The transformations worth recording are specific and detectable:
certainty inflation ("may have been" → "was"), caveat loss, attribution drift ("one official" →
"officials"), source pluralisation, hedge removal, emotional loading, modal shift, scale escalation,
chronology compression, context stripping, normalisation.

**INFERENCE.** Certainty inflation and caveat loss matter most **because nobody writes anything
false**. Each step is defensible alone. The cumulative result is a claim no source ever made.

The proposed model is **versioned and append-only**, preserving original wording, original language,
translation method, evidence supplied, certainty claimed in the source's own words, and the delta
from the parent version. **Corrections attach; they do not replace** — because the uncorrected
version is what most readers saw.

---

## 5. Source independence

Full method in [NARRATIVE-SUPPLY-CHAIN.md](NARRATIVE-SUPPLY-CHAIN.md) §2.

Four situations look identical in a count: ten independent observations; ten outlets running one
wire; ten outlets citing each other; ten outlets reacting to one statement. **Only the first is
corroboration.**

**The strongest indicator of shared origin is an identical factual *error*.** Two outlets can
independently reach the same true statement; independently reproducing the same mistake is very
unlikely.

**PRODUCT PROPOSAL — the count is a triple, never a single number:**

```
17 reports · 3 independent origins identified · 6 unresolved
```

Unresolved is never folded into either side. The count is of origins, not outlets. And the honest
phrasing is "identified", not "exist".

---

## 6. Ownership and funding

Full analysis in [OWNERSHIP-FUNDING-AND-INCENTIVES.md](OWNERSHIP-FUNDING-AND-INCENTIVES.md).

> **Ownership, investment, funding, access or shared interests can explain possible incentives and
> dependencies. They do not by themselves prove editorial control, common intent or organised
> coordination.**
>
> A shared investor across a portfolio is a shared investor. It is not evidence that the investor
> directs what any of those organisations say, and it is not evidence that they act together.

**The finding that governs everything else:**

> **CURRENT LAW / RESEARCH FINDING.** Almost nothing in the UK transparency estate is verified data.
> Companies House, the PSC register, the Register of Overseas Entities and the Electoral Commission
> register are **self-declaration systems**. ECCTA 2023 verifies **who is filing**, not **what they
> filed**.

Specific gaps that any system must state rather than paper over:

- **The PSC threshold is the design flaw.** Control is reportable above **25%**. Four people at 25%
  each produce a company with **no PSC at all**, lawfully. About 13% of companies filed no PSC;
  **four in five Scottish Limited Partnerships had not named one**.
- **Trusts are the deepest hole.** The Trust Registration Service is **not public**.
- **85–95% of UK lobbying appears in no register.** In-house lobbyists register nothing; only
  contacts with Ministers and Permanent Secretaries count; no subject matter is disclosed; and a VAT
  threshold exempts small and many foreign lobbyists entirely.
- Ministerial meeting entries average **11 words** ("to discuss the industrial strategy"). The
  Scottish register averages **118**.
- **There is no UK media ownership register.** The independent report for Ofcom rated UK media
  ownership transparency **HIGH RISK**.
- **Transparency does not ratchet forward.** EU public beneficial-ownership access went backwards in
  2022; the UK register of members went backwards in **January 2026**.

**A correction worth carrying:** the UK Infrastructure Bank was renamed the **National Wealth Fund**
in October 2024, and the UK has **no sovereign wealth fund** in the accumulation sense. Conflating
them is a factual error that will be attacked.

---

## 7. Incentives

**PRODUCT PROPOSAL.** Nobody can observe motive. What is observable is **position** — what somebody
stands to gain or lose given disclosed circumstances. Four evidential tiers, and the output must
state which is in use:

| Tier | Example |
|---|---|
| **DOCUMENTED** | "A holds a disclosed shareholding in B" |
| **INFERRED** | "A's holding means A would benefit if B's sector expanded" |
| **POSSIBLE** | "A may prefer outcome X" |
| **SPECULATION** | **Not published, at all** |

**INFERENCE.** Two incentives are systematically under-weighted and explain more institutional
behaviour than conspiracy does: **organisational survival** and **risk avoidance**. An organisation
that drops a story because it fears a lawsuit produces the same silence as one that was told to, and
the two are indistinguishable from outside. An honest system says so rather than choosing the more
interesting explanation.

---

## 8. Central actors and information chokepoints

The founder's observation is empirically well founded — large systems often trace to a small number
of central actors, and network analysis has the vocabulary for it.

**It is also the single most dangerous capability in the concept.**

**INFERENCE.** Centrality is a property of *a graph you constructed*, from *sources you chose*, with
*joins you made probabilistically*. Three hazards:

1. **The graph reflects disclosure, not reality.** Because most lobbying is unregistered and trusts
   are opaque, **a well-advised actor is invisible**. Concentration findings systematically
   over-represent the compliant.
2. **Entity-resolution errors compound.** UK registers share no identifiers; every join is
   probabilistic; one wrong merge creates false centrality for a node that does not exist.
3. **Centrality invites a causal reading it cannot support.** "X is central" is one step from "X
   controls", and nothing in the mathematics licenses that step.

**Proposed rule:** centrality may be displayed with its construction visible, and may **never** be
reported as a finding about control.

---

## 9. Multilingual and regional bias

Full analysis in
[MULTILINGUAL-AND-REGIONAL-INFORMATION-BIAS.md](MULTILINGUAL-AND-REGIONAL-INFORMATION-BIAS.md).

**The wrong fix is "add more foreign articles."** That produces one pool still weighted by
abundance. The proposed safeguards are structural: original-language retrieval; regional source maps
rather than one global hierarchy; **local reporting separated from foreign reporting about the same
place**; multiple independent translations with disagreement preserved; a coverage-gap register;
and source-distribution reporting on every output.

The cheapest and most valuable is simply to say what the evidence base was:

> Seventy-eight percent of the evidence used here comes from UK and US English-language sources.
> Original-language reporting from the affected region is limited. Confidence in the international
> framing should remain constrained.

**And the rule that prevents inverse bias:** non-Western sources are not automatically more truthful;
state media is not automatically false; Western media is not automatically reliable; alternative
media is not automatically independent. **The goal is balance and visibility, not inversion.**

**INFERENCE.** Translation is not neutral and must be recorded as a transformation step in the
lineage. Machine translation flattens hedging and register — and a hedge lost in translation is
indistinguishable from certainty inflation introduced by a source, which would make the lineage
model attribute the change to the wrong step.

---

## 10. Government and commercial narratives

**PRODUCT PROPOSAL / RESEARCH FINDING.**

### 10.1 States

States shape information environments lawfully and routinely: official statements, public
broadcasting, regulated broadcasters, access journalism, briefings, strategic communications, grants
and procurement, diplomatic messaging, public-interest campaigns, classification and selective
release, embedded reporting, platform regulation, state-linked media — and, separately, covert
influence activity.

> **Most government communication is not propaganda, and a system that treats it as such is
> useless.** A health campaign, a flood warning and a covert cloned-outlet operation are not the
> same thing, and the distinguishing features are **disclosure and attribution**, not tone.

**INFERENCE.** The line that matters is whether the source of the message is **disclosed**. A
minister arguing for a policy under their own name is politics. The same message placed through an
outlet whose ownership is concealed is a different act, and it is the concealment — not the
content — that makes it so. That is why **EMFA's ownership-transparency obligations matter more to
this concept than any detection method**: they attack the mechanism directly.

**Access journalism deserves its own treatment.** It is not corruption and it is not coordination.
It is **category 5, access dependence** — an organisation that relies on continued access to
officials faces a real constraint on what it publishes, without anyone instructing anybody. It is
also **close to impossible to evidence from public records**, which is precisely why naming it as a
category matters: the alternative is that the effect is either ignored or misattributed to something
more sinister and less true.

### 10.2 Commercial actors

Public relations, investor relations, advertising, sponsored research, analyst access, industry
associations, lobbying, consultancy reports, commissioned polling, influencer marketing, search
optimisation, native advertising, reputation management, crisis communications.

**These are mostly lawful and mostly disclosed-in-principle.** The problem is that disclosure is
frequently technical rather than effective — a funding line in an appendix does not travel with the
finding when it is quoted in a newspaper.

**Narrative laundering** is the mechanism that matters, and it is the same for commercial and state
actors:

> A claim begins as promotional or political messaging, passes through intermediaries that each
> strip a layer of provenance, and reappears as independent analysis.

**RESEARCH FINDING.** Documented chains run from initial placement, through foreign or obscure
outlets, through AI-assisted fake local-news sites, into genuine domestic commentators. **By the
final hop there is nothing inauthentic to detect** — the commentator sincerely believes it, is not
coordinating with anyone, and is not being paid.

**INFERENCE, and it is the strategic point of this whole strand.** Laundering is a **provenance
problem, not a coordination problem**. It is invisible to synchrony detection by construction, and
it is exactly what claim lineage plus ownership analysis is built to see. **The two capabilities
MERIDIAN could most defensibly build are the two that address the mechanism the detection industry
cannot.**

---

## 11. Coordinated amplification

> **NOT A COMMITTED CAPABILITY.** This section reports what the field can and cannot do. It is not a
> plan, and it is not a milestone. On the evidence below, MERIDIAN may reasonably decide never to
> build coordination or bot detection at all — and **none of the strongest proposed uses requires
> it.**

Full treatment in
[COORDINATED-AMPLIFICATION-AND-BOT-METHODOLOGIES.md](COORDINATED-AMPLIFICATION-AND-BOT-METHODOLOGIES.md).

**RESEARCH FINDING.** Three things must be carried into any product decision:

**Automation detection failed, and the reason generalises.** The tool behind most published bot-
prevalence research showed **precision as low as 24–59%**, **recall of 20–29%**, and **27.2% of test
accounts crossing the bot/human threshold within three months** without changing. It has had no live
data since mid-2023. The structural cause: automation is unobservable, so proxies are used — high
volume, sparse profiles, new accounts — and **those proxies describe engaged humans, activists and
journalists.**

**Coordination detection is a better claim structure and inherits the same false positives.** A
study of the 2019 UK general election surfaced, alongside partisan networks, **pension-equalisation
campaigners and a loan-charge protest group**. Its authors state they **cannot distinguish
inauthentic coordination from authentic**. Fandoms, unions, diaspora communities and newsrooms all
coordinate.

**Published findings have already proven to be artefacts.** A 2025 re-examination of claimed
inter-state coordination, using control datasets, found **no evidence of it** — attributing prior
results to the absence of baselines. **A system without a baseline corpus will manufacture
findings.**

**And the most effective operations are out of scope entirely.** Volunteers copy-pasting
pre-written posts from their own real accounts, organised over a messaging app; or a media company
covertly funded to pay sincere commentators. **No synchrony, no duplication, no automation** — both
were exposed by financial investigation, not network analysis.

---

## 12. Adaptive influence methods

**RESEARCH FINDING.** The founder's instinct — that once a detection method is known, methods route
around it — is correct and documented.

- **Takedown is priced in.** A cloning operation that copies real outlets pixel-for-pixel survived
  the seizure of 32 domains and multiple sanctions designations; a related operation reportedly
  produced **200+ new fictional news sites since March 2025**. The architecture assumes churn.
- **Laundering removes the signal.** By the final hop there is nothing inauthentic to detect.
- **The defender is the target.** One documented operation floods fact-checkers and journalists with
  fabricated material to exhaust capacity. **A high detection count can be the adversary's
  objective** — so a dashboard rewarding volume is one the adversary can drive.
- **Sincerity is the best cover.** Recruiting people who genuinely agree defeats every
  inauthenticity signal, because there is no inauthenticity.

**PRODUCT PROPOSAL.**

> **Detection methods are versioned, tested against known campaigns, and treated as temporary
> hypotheses with expiry dates** — with documented false positives, adversarial testing, regional
> validation, analyst review, and an explicit record when a version is retired and why.

The system must be able to say *"version 2 overestimated coordination in this type of community;
version 3 changed the timing threshold"* — and must never present a past assessment as though it had
always been right.

**INFERENCE.** This is the same discipline as the append-only claim lineage in §4, applied to our own
methods rather than to other people's claims. **A system that demands provenance from its sources
and hides its own method history has not understood its own argument.**

---

## 13. Omission and framing

Full treatment in [NARRATIVE-SUPPLY-CHAIN.md](NARRATIVE-SUPPLY-CHAIN.md) §4.

Narratives are shaped more by exclusion than by falsehood. Nothing false need be published for a
reader to be badly misled.

**The rule that keeps it honest: absence is not proof of suppression.** Most omissions are ordinary —
space, deadlines, ignorance, nobody available to comment. Four graded forms only: **expected but
absent**, **coverage gap**, **unasked question**, **uncertain omission**.

**INFERENCE.** "Expected but absent" requires a baseline of what is normally present, and that
baseline encodes our own assumptions about normality. This is the weakest part of the model and
should be treated as unsolved rather than shipped confidently.

---

## 14. Truth, repetition and confidence

**PRODUCT PROPOSAL, and the strongest design commitment in this strand.** Eight things stay separate:

claim support · source independence · evidence quality · narrative reach · incentive alignment ·
coordination confidence · coverage diversity · unresolved alternatives

> **There is no truth score, and there must never be one.**

**INFERENCE.** The commercial pressure to produce a single number will be immense — it is what buyers
ask for and what demos need. **Resisting it is the product.** A single score would make all eight
fields unfalsifiable at once, and would place MERIDIAN in the position of the ratings services now
being litigated against and legislated against precisely for compressing judgement into a number.

---

## 15. Proposed output

**PRODUCT PROPOSAL.** The default view is prose, not a graph. A network diagram as the first screen
would fail the same way the Analysis screen failed its first user.

> ### What is being claimed
> The government says the disruption was caused by an external actor.
>
> ### Why this matters
> The claim supports emergency spending and a stronger security response.
>
> ### Where it came from
> Most reporting traces back to two official briefings.
>
> ### How independent the reporting is
> Seventeen outlets repeated the claim. Three appear to provide independent evidence. Six could not
> be traced.
>
> ### Who may benefit
> Several security suppliers and political actors may benefit if the response is expanded.
> **This shows potential incentive alignment, not proven coordination.**
>
> ### What challenges it
> Local witnesses and two specialist sources dispute parts of the timeline.
>
> ### What is missing
> Original-language evidence from the affected area is limited.
>
> ### What MERIDIAN cannot establish
> Who caused the event, and whether the amplification was coordinated.

Beneath it, on deliberate controls: claim lineage · source chain · ownership graph · funding
evidence · incentive assessment · amplification analysis · competing explanations · missing
perspectives · technical methodology.

**A reader should never need the technical layer to know what is claimed and what is not.**

---

## 16. Entity and relationship model

**PRODUCT PROPOSAL. Not a schema. Nothing to be implemented.**

**Entities:** claim · narrative · source · document · person · organisation · media outlet · fund ·
investor · government body · political party · regulator · company · think tank · charity · platform ·
account · campaign · asset · contract · board position · amplification event · correction ·
competing explanation.

**Relationships:** owns · funds · invests_in · controls · appoints · sits_on_board_of ·
contracts_with · advertises_with · supplies · depends_on · receives_from · cites · republishes ·
amplifies · corrects · contradicts · benefits_from · lobbies · donates_to · regulates ·
formerly_worked_for · shares_source_with · translated_from · derived_from.

Every relationship carries: **evidence · origin · confidence · date range · direction · direct or
inferred**.

> **There is no universal influence score.** Relationships are typed and separate. A system that
> reduces them to one weight has destroyed the only thing that made it honest.

**The narrative map**, which must support cycles:

```
Event → Claims → Sources → Organisations → Owners and Funders → Amplifiers
   → Audiences → Belief Changes → Decisions → Material Outcomes
        ↺ a decision produces a new official claim, restarting the chain
```

---

## 17. Legal and ethical boundaries

> **PROVISIONAL LEGAL RESEARCH — DO NOT RELY ON WITHOUT SPECIALIST REVIEW.**
>
> Statutory text cited here was read directly from legislation.gov.uk. **Regulator positions,
> case-law rationes and policy characterisations were largely read via secondary sources**, and
> **every ICO position failed primary retrieval**. Individual claims carry their own marker. The
> [sources register](NARRATIVE-INTELLIGENCE-SOURCES.md) records verification level per source and
> lists what must be re-checked before anything is implemented or published.

**A report of what sources say, not legal advice.** Verification status in
[NARRATIVE-INTELLIGENCE-SOURCES.md](NARRATIVE-INTELLIGENCE-SOURCES.md). Several important points are
**genuinely unresolved in UK law** — not merely unresearched — and are marked.

### 17.1 The three findings that most constrain the design

**(a) Recording political opinions about named people is probably special category data.**

**REGULATOR GUIDANCE — PRIMARY-SOURCE VERIFICATION REQUIRED.** *ico.org.uk returned HTTP 403 to
every retrieval attempt; the ICO positions below come from search extracts and law-firm commentary,
not from reading the ICO's own page. Re-verify before relying on any of this.*

"Political opinions" are an Article 9 special category — that much is statutory and settled. The
ICO's **reported** test is that inferring special category information **"with a reasonable degree of
certainty"** engages Article 9 — and, decisively, that processing data **with the intention of
making such inferences** engages it **"irrespective of the level of statistical confidence."**

**INFERENCE.** A system whose stated purpose is to record what positions a named person holds or
promotes sits inside that second limb by design. **Assume Article 9 applies.** This is the single
largest UK compliance obstacle in the concept, and it is a reason to do as much of the analysis as
possible at **organisational rather than individual level**.

The available routes are all narrow:

| Route | Fit |
|---|---|
| Art 9(2)(e) — "manifestly made public by the data subject" | **Partial.** Construed narrowly; requires clear affirmative action by the subject. Covers a politician's published position. **Does not cover inferences we generate** — the subject did not make our inference public — nor people who never spoke publicly |
| DPA 2018 Sch 1 Pt 2 **para 13** (journalism in connection with unlawful acts) | **Narrow.** Only bites where the subject matter is **wrongdoing**, not general narrative mapping. Requires an appropriate policy document |
| Sch 1 Pt 2 para 10 (investigating unlawful acts) | Wrongdoing-focused strands only |

**A correction worth recording**, because it was an error in our own research brief: **Sch 1 para 24
is "Disclosure to elected representatives"**, not the journalism condition. The journalism condition
is **Sch 1 Part 2 paragraph 13**. Our brief cited the wrong paragraph and the research corrected it.

**(b) The journalism exemption is broad — and it is untested for a product like this.**

**CURRENT LAW.** DPA 2018 Sch 2 Pt 5 para 26 disapplies a great deal: Art 5(1)(a)–(e) including
**accuracy**, Art 6, **Art 9**, Arts 13–14, Art 15 subject access, Art 16 rectification, Art 17
erasure, Art 21(1) objection. It is the route by which political-opinion data becomes processable at
all.

But it is **condition-led, not status-led**. It requires processing for the special purposes —
journalism, **academic**, artistic or literary — **with a view to publication**, a **reasonable
belief that publication is in the public interest**, and a reasonable belief that compliance would
be **incompatible** with those purposes. Public interest must be assessed with regard to the BBC
Editorial Guidelines, the Ofcom Broadcasting Code or the Editors' Code — **codes written for
broadcasters and newspapers, which an analytics vendor cannot straightforwardly apply.**

> **OPEN QUESTION — PROVISIONAL LEGAL RESEARCH — DO NOT RELY ON WITHOUT SPECIALIST REVIEW.**
> Whether a **commercial subscription analytics product** can claim the special-purposes exemption. **No UK judgment
> applies para 26 to a commercial data product.** A subscription feed sold to clients is materially
> different from publication. This should not be relied on without advice.

**Also worth correcting:** the ICO's **Data protection and journalism code of practice is in force** —
issued 1 February 2024, effective 22 February 2024. It is the *automated decision-making* guidance
that is in draft.

**(c) Defamation defences require a human to have held a belief.**

**CURRENT LAW (statutory text verified) + INFERENCE as to application.** The statutory wording below
was read directly. **Its application to machine-generated output is untested — no UK judgment
decides it — and the reading here is ours. PROVISIONAL: DO NOT RELY ON WITHOUT SPECIALIST REVIEW.**

- **s.3 honest opinion** is defeated if the claimant shows **the defendant did not hold the opinion**
  (s.3(5)). **A software system holds no opinion.** Where the statement was made by another and
  published by the defendant, the defence fails if the defendant knew the author did not hold it
  (s.3(6)) — and the "author" of a machine-generated inference is not a person who holds beliefs
  either.
- **s.4 public interest** requires that **"the defendant reasonably believed"** publication was in
  the public interest — an actual belief, then tested for reasonableness.

**INFERENCE.** Neither defence protects an output nobody believed. **A human must hold, and be able
to evidence, the belief** before any adverse assertion about a named person reaches a third party.
That is not a nice-to-have review step; it is what the defence is made of.

**And it does not stay fixed. (Case read via secondary sources — PRIMARY-SOURCE VERIFICATION
REQUIRED.)** ***Banks v Cadwalladr*** [2023] EWCA Civ 219 establishes that a s.4
defence **does not endure forever**: where publication continues and circumstances materially
change, the defendant must make out s.4 **afresh for the continuing publication**. **Every day an
assertion remains queryable in a database is continuing publication.** A system that does not ingest
rebuttals and re-review will lose the defence over time even if it had it at first output.

**No UK judgment yet decides a defamation claim on AI-generated output.** The UK Jurisdiction
Taskforce's Legal Statement on Liability for AI Harms (7 July 2026) reportedly concludes that
organisations **cannot automatically avoid responsibility** where they adopt AI-generated statements
as their own. Genuinely **UNRESOLVED**.

### 17.2 Four more hard constraints

**Pre-charge investigation data is off-limits.** ***Bloomberg LP v ZXC*** [2022] UKSC 5: as a
general rule a person under criminal investigation has a **reasonable expectation of privacy** in
information relating to that investigation **prior to charge**. **Truth is not a defence to misuse
of private information, and neither is the source having been public.** Recording or surfacing that
a named person is under investigation before charge is a **hard design rule**, not a risk to
balance.

**News ingestion requires licences.** **CURRENT LAW — statute verified; the March 2026 policy report
was read via the gov.uk summary rather than the full document, so treat the policy characterisation
as PRIMARY-SOURCE VERIFICATION REQUIRED.** CDPA s.29A
permits text and data mining only for **non-commercial research**, with lawful access. The
Government's March 2026 report confirmed it **will not** introduce a broad exception, and that the
previously preferred opt-out approach is no longer preferred. **There is no UK exception a
commercial product can use.**

**Scraping is a contract problem even where it is not an IP problem.** ***Ryanair v PR Aviation***
(C-30/14): where a database is *not* protected by copyright or database right, the Directive does
not limit the owner's freedom to impose **contractual** restrictions. **The weaker a site's IP
protection, the stronger its contractual position** — "no database right subsists" is not a green
light. Separately, database right catches **repeated and systematic extraction of insubstantial
parts**.

**Leaked material puts you on notice by definition.** A recipient is bound by an obligation of
confidence where they **knew or ought to have known** the information was confidential
(*Trailfinders*). **Knowing a corpus is leaked supplies the "ought to have known" element.** The
defence is public interest **per document, not per corpus**. This matters because the richest
ownership corpus available — OCCRP Aleph — contains leaked databases.

### 17.3 The one that could be existential

**EU AI Act Article 5(1)(c) — prohibited social scoring.** In force since 2 February 2025. Penalties
up to **€35m or 7% of global annual turnover**.

The Commission's guidance sets three cumulative conditions: the system is placed on the market;
it evaluates or classifies people **over a period of time** based on social behaviour or **inferred**
personal characteristics; **and** the score leads to detrimental treatment **in a context unrelated
to where the data was collected**, or treatment that is unjustified or disproportionate.

**INFERENCE.** An incentive or influence score attached to named individuals, accumulated over time
from inferred characteristics, satisfies the first two conditions comfortably. **Everything turns on
the third.** If the output is published analysis and nobody uses it to treat the individual
detrimentally in an unrelated context, the condition fails. **If customers use the scores for
hiring, funding, partnership or platform decisions, it is arguably met — and the provider placing
the system on the market is within the prohibited conduct even where the deployer inflicts the
detriment.**

> **OPEN QUESTION, highest consequence in this strand. PROVISIONAL LEGAL RESEARCH — DO NOT RELY ON
> WITHOUT SPECIALIST REVIEW.** The "unrelated context" limb is untested, there is no CJEU authority,
> the Commission guidance was read via secondary summaries only, and **we did not verify the AI Act's
> territorial scope** or whether the guidance carves out research or journalistic uses at all. Given
> the penalty exposure, this needs specialist advice before any individual-level feature is designed,
> not after.

**PRODUCT PROPOSAL.** This is a further, independent reason for the rule in §16: **no per-individual
influence score, ever.** Not as a design preference — as the cleanest way to stay outside the most
expensive prohibition in the field.

### 17.4 Ethical prohibitions

**PRODUCT PROPOSAL.** Proposed as absolute, not defaults:

1. No declaring a person a propagandist because of their employer.
2. No inferring coordination from financial connection alone.
3. No political-opinion scoring of individuals.
4. No persuadability scoring — extends MERIDIAN's existing B5 prohibition past the simulation
   boundary.
5. No targeting of vulnerable people.
6. No ranking people by influence for the purpose of manipulation.
7. No psychological profiles of real people.
8. No doxxing, and no aggregation of individuals' personal details even where each is public.
9. No covert collection of private messages.
10. No identifying anonymous users without strong lawful justification.
11. No presenting inferred motive as fact.
12. **No truth score.**
13. No black-box accusation of bot activity.
14. No unreviewed publication of harmful allegations.
15. No assumption that state media is always false.
16. No assumption that Western media is always reliable.
17. No assumption that alternative media is independent.
18. No treating popularity as truth.

**Two additions the research suggests:**

19. **No recording that a named person is under criminal investigation before charge** — *Bloomberg
    v ZXC* makes this a legal rule, and it belongs here as an ethical one too.
20. **No per-individual accumulated score of any kind** — see §17.3.

**And one boundary that needs stating because it will be tested:** the prohibitions are product
constraints, not marketing copy. The commercial pressure to relax numbers 3, 6 and 12 will be
constant, because they are what buyers ask for.

### 17.5 Distinguishing four things in every output

**PRODUCT PROPOSAL.** Never blurred:

| Category | Example |
|---|---|
| **Public-record fact** | "Companies House records A as a director of B" |
| **Model inference** | "A's disclosed holding means A would benefit if X" |
| **Allegation by a third party** | "C has alleged that A did X" |
| **Finding by a competent authority** | "A regulator found that A did X" |

**INFERENCE.** These carry completely different legal weight and completely different evidential
weight, and a system that presents them in the same typeface has already failed.

---

## 18. Human review

**PRODUCT PROPOSAL.** A human analyst must remain involved in: entity resolution; identifying
beneficial owners; interpreting cultural context; assessing coordination; evaluating motives;
resolving translations; reviewing allegations; approving publication; handling defamation risk;
distinguishing satire; assessing missing perspectives; and changing methodology.

> **MERIDIAN may organise and explain evidence. It must never autonomously publish an accusation
> about a real person or organisation.**

**INFERENCE.** This is the same boundary MERIDIAN already holds internally — the model proposes, the
engine and accountable humans decide — carried across a far more dangerous line. And it is the
boundary the case law points at: two tribunals have now declined to treat a synthetic front-end as
separable from its operator. **The operator is the publisher, always.**

**The honest problem with it:** review does not scale, and this design assumes careful human
attention at exactly the volume where careful human attention fails. That is recorded as unsolved.

---

## 19. Technical architecture

**PRODUCT PROPOSAL. Nothing to be built under this task.**

```
┌─ RETRIEVAL ────────────────────────────────────────────────────┐
│  Multilingual Retrieval · Translation Comparison               │
│  Evidence Archive (immutable copies)                           │
└──────────────────────────┬─────────────────────────────────────┘
┌──────────────────────────▼─────────────────────────────────────┐
│  Source Registry · Claim Registry · Claim Lineage Store        │
│  Entity Resolution · Ownership & Funding Graph                 │
└──────────────────────────┬─────────────────────────────────────┘
┌──────────────────────────▼─────────────────────────────────────┐
│  Source Independence · Amplification Events                    │
│  Coordination Indicators · Coverage Diversity                  │
│  Missing Perspectives · Competing Explanations                 │
│  Incentive Assessment · Versioned Method Registry              │
└──────────────────────────┬─────────────────────────────────────┘
╔══════════════════════════▼═════════════════════════════════════╗
║  ANALYST REVIEW QUEUE — nothing naming a real person passes    ║
║  without human approval                                        ║
║  Correction and Appeal Record                                  ║
╚══════════════════════════┬═════════════════════════════════════╝
┌──────────────────────────▼─────────────────────────────────────┐
│  Narrative Projection API → Adaptive Futures Engine Adapter    │
└────────────────────────────────────────────────────────────────┘
```

The rule the architecture exists to enforce:

> **The system records evidence and produces bounded assessments. It does not convert weak
> associations into accusations.**

Two components deserve emphasis. The **Versioned Method Registry** exists because detection methods
expire — they must carry version, test results, known false positives and an expiry date. The
**Correction and Appeal Record** exists because we will be wrong about real people, and a process
built after the first complaint is a process built too late.

---

## 20. Relationship to the Adaptive Futures Engine

**INFERENCE, and this is the strongest argument for the strand.**

A futures engine cannot model organisations realistically without modelling the information they act
on. Narrative analysis would supply **structured inputs and uncertainty**, not conclusions:

- different people and organisations receive different claims, at different times;
- trust varies by subject and by how a source behaved before;
- apparently independent reports share one origin — so an organisation that "confirmed" a claim from
  three sources may have confirmed it once;
- organisations act on strategically framed information;
- incentives affect what organisations publish or suppress;
- coordinated amplification changes exposure without changing underlying opinion;
- omitted evidence delays decisions;
- a correction arrives too late to matter;
- a new narrative changes which actions are politically possible.

> **Narrative analysis must never directly determine belief in the simulation.** It provides inputs
> and uncertainty; the engine's declared belief rules do the rest. Otherwise the simulation inherits
> every error in the narrative layer and hides it behind a deterministic result.

---

## 21. Relationship to Simulation-Born Entities

Simulated organisations create narratives, fund messaging, depend on particular sources and develop
communication strategies. Under the
[entity graduation](SIMULATION-BORN-ENTITIES.md) framework, that information history would be part
of a Graduation Evidence Pack — and a simulated organisation would itself be subject to narrative
analysis inside the world.

**INFERENCE — and a warning.** The two strands compound each other's central risk. Strand 1's hazard
is that simulated success is mistaken for evidence. This strand would produce *analysis about real
organisations*. **The two must never be presented in the same view without an unmissable separation**,
because a document that mixes a simulated company's invented history with real ownership records
about real people is the most misleading artefact this project could produce.

---

## 22. Relationship to current MERIDIAN

### 22.1 What exists today that genuinely supports this

**FACT**, verified in the repository at `a71c9bc`:

| Capability | Why it matters here |
|---|---|
| Fictional typed entities with world-carrying IDs | Real and fictional can never be silently mixed |
| Organisations, people and population groups modelled separately | The entity model already distinguishes what this strand must |
| Engine / fixture origin separation | The evidence-origin discipline already exists |
| **Information exposure records** | "Who received what, when" is already a modelled concept |
| **"Not received" distinct from rejection** | The single most relevant existing property — the difference between *not reached* and *rejected* is exactly what source-independence work needs |
| Belief histories, append-only | Lineage has a working precedent |
| Contextual trust | Trust varies by subject, not a single scalar |
| Declared model boundaries | The vocabulary for "we did not model this" exists |
| Deterministic explanations | Every claim traceable to its cause |
| **B5 prohibitions** — no protected-trait targeting, no persuadability optimisation | The ethical floor is already set and already enforced in code |
| Read-only dossiers | Read/write separation already practised |
| Selected-but-not-executed decisions | The proposes/decides boundary already exists |

### 22.2 What is missing

**FACT.** Everything operational: web ingestion; multilingual retrieval; source archives; ownership
graphs; financial records; claim lineage; entity resolution; translation validation; coordination
detection; campaign detection; media-ownership data; funding relationships; source-independence
analysis; incentive assessment; adversarial testing; analyst review; legal and ethical controls.

### 22.3 Stated plainly

**MERIDIAN does not perform narrative intelligence. It does not ingest, analyse or store any real
information about any real person or organisation.** Nothing in this report should be quoted as
suggesting otherwise.

---

## 22a. What to preserve for future design

**PRODUCT PROPOSAL — design directions, not current capabilities. No schema, no implementation.**

Whatever happens to this strand as a product, the research surfaced concepts MERIDIAN's own entity
and simulation model may eventually need — and which are far cheaper to design in than to retrofit:

| Concept | Why it may be needed |
|---|---|
| **Claim lineage** | A claim that travels and changes is a better model of information than a static fact |
| **Independent-origin tracking** | An organisation that "confirmed" something from three sources may have confirmed it once |
| **Source dependence** | Who relies on whom, structurally |
| **Information exposure** | Who received what, when — MERIDIAN already has this |
| **Corrections, and delayed corrections** | A correction arriving too late is a distinct and consequential event |
| **Competing narratives** | Two internally consistent accounts coexisting, unresolved |
| **Omission and coverage gaps** | What was never said, distinguished from what was denied |
| **Organisation-specific incentives** | What an organisation stands to gain or lose, per organisation |
| **Subject-specific trust** | Trust varies by topic and by how a source behaved before — MERIDIAN has a form of this |
| **Versioned assessment history** | What we thought, when, and on what basis — never rewritten |

**INFERENCE.** Every one of these is implementable **entirely inside the fiction**, with no real
ingestion, no real names and no legal exposure. That is the recommendation in §26 restated as a
design list: the valuable part of this research is available now, in the simulation, at no risk.

---

## 23. Commercial possibilities

**PRODUCT PROPOSAL.** No market sizing — we have none that is defensible.

| Model | Customer | Notes |
|---|---|---|
| **Scenario inputs for the futures engine** | Internal | No external claims, no legal exposure. **Safest** |
| **Misinformation exercise generation** | Training buyers | Fictional by design — the truth boundary is never crossed |
| **Contested-event briefings** | Journalists, analysts, NGOs | Human-produced, method-assisted |
| **Source-independence analysis** | Newsrooms, researchers | Narrow, defensible, genuinely unserved |
| **Ownership and funding maps** | Due diligence, risk | Crowded — Sayari, Aleph, OpenCorporates |
| **Narrative-risk monitoring** | Corporate comms | Crowded and politically exposed |

**RESEARCH FINDING — and it should weigh heavily.** The market is contracting for **political
rather than technical** reasons. Logically raised nearly £30m, held platform and UK government
contracts, and **entered administration in July 2025** after Meta and TikTok withdrew from
third-party fact-checking; its assets went to a company run by a former director in a related-party
pre-pack. Meta halved its coordinated-behaviour reporting cadence and re-scoped it toward scams.
Google removed ClaimReview from Search, removing the incentive that sustained the fact-check corpus.
NewsGuard sued the FTC in February 2026 and is barred from state contracts in Florida. Graphika has
repositioned toward brand and fraud work.

**INFERENCE.** Every model here that depended on **platform trust-and-safety budgets** or on being
accepted as a **neutral arbiter of truth** has been damaged since 2024. The survivors sell into
**compliance, sanctions, supply-chain and fraud**, where demand is regulatory rather than
discretionary. That is a strong argument against positioning MERIDIAN as a truth arbiter, and a
strong argument for the two safest models above.

---

## 24. Adjacent products

Full table in [NARRATIVE-INTELLIGENCE-SOURCES.md](NARRATIVE-INTELLIGENCE-SOURCES.md). The pattern
across 24 services is clean and is the strategic finding:

| Cluster | Covers | Does not cover |
|---|---|---|
| **Consumer bias tools** — Ground News, NewsGuard, AllSides, Ad Fontes | Content slant | Ownership, funding, incentives, source independence, coordination |
| **Threat intelligence** — Graphika, Blackbird, Recorded Future, platform teams | Coordination and amplification | **Ownership and funding, entirely** |
| **Ownership databases** — OpenCorporates, Sayari, Aleph, OpenSanctions, LittleSis | Ownership, sometimes funding | Narrative, amplification |

**The join is empty.** The only work doing both is hand-built investigative journalism — EU
DisinfoLab's *Indian Chronicles*, which traced 750+ fake outlets and resurrected defunct NGOs and
dead academics, is the model. **That is a finding about difficulty as much as about opportunity: it
took an investigative team, not a system.**

**What MERIDIAN should not copy:** unfalsifiable enforcement counts (platform bulletins report
actions taken, with no disclosed detection method, evidence standard or error rate); single-score
aggregation; bot-status claims without published validation; and any consumer tool's left/right axis
outside the country it was built for.

---

## 25. Open research questions

1. Can a useful ownership picture be built when the best public source covers one country and the
   rest of the world just closed access?
2. What is the honest error bar on an entity-resolution join across four UK registers?
3. How is "not required to disclose" shown to a reader without implying concealment?
4. Can access dependence be evidenced from public records at all?
5. Should concentration analysis be built, given that it will be read as control?
6. Where does one "origin" end — a press release quoting a study quoting a dataset is how many?
7. How is a paraphrase distinguished from a new claim?
8. Can translation uncertainty be shown to a non-expert?
9. Does human review scale at all, and if not, what does that imply for the product?
10. Is there a useful version of this in three languages rather than thirty?
11. **Would a careful human with a week produce a better answer than the system?** — the question
    the first experiment exists to answer.

---

## 26. Recommendation

**The idea is right, most of the product is not buildable, and the buildable part is not the part
that sounds exciting.** All three of those are findings, and the third is the useful one.

### Is the concept coherent?

**Yes — and it is more coherent than the founder's brief assumed, in one specific way.** The brief
proposed analysing origins, independence, ownership, incentives, amplification and omission
together. The research says those divide cleanly into two groups with very different evidence bases:

- **Provenance work** — claim lineage, source independence, ownership and funding, omission. Strong
  evidence base, defensible claims, and it addresses **narrative laundering**, which is the
  mechanism that matters most and the one the detection industry structurally cannot see.
- **Behavioural work** — coordination and amplification detection. Weak evidence base, high false
  positives, adversarially unstable, and blind to the most effective operations.

**The concept is coherent. The second half of it may not be worth building.**

### What is genuinely different from Ground News or ordinary media-bias tools?

Concretely, across 24 services examined:

- Consumer tools measure **content slant**. Ground News aggregates three third-party bias ratings —
  its epistemic quality is capped by theirs — plus its own ownership dataset. It has **no**
  coordination or amplification capability. AllSides and Ad Fontes touch **none** of the five axes.
- Threat-intelligence firms do coordination and **never** ownership or funding.
- Ownership databases do ownership and **never** narrative.

**The join is empty**, and the only work doing both is hand-built investigative journalism. The
difference MERIDIAN could offer is **connecting a claim's path to the disclosed interests behind the
organisations on that path** — and doing it with published error rates, which would make it an
outlier in a field where platform enforcement counts are unfalsifiable, vendor bot detection is
unvalidated, and no rating service publishes an inter-rater reliability audit.

### What is realistically buildable first?

In order:

1. **Claim lineage over a small, manually assembled, archived corpus.** No live ingestion. The
   hardest intellectual work, the lowest legal risk.
2. **Source-independence analysis** — the triple count. Genuinely unserved, narrow, defensible.
3. **Ownership context from UK public records**, clearly labelled as *declared, not verified*.
4. **Omission and coverage-gap reporting**, including the source-distribution disclosure.

### What requires human analysts?

Entity resolution; identifying beneficial owners; cultural context; assessing coordination;
evaluating motives; resolving translations; reviewing allegations; **approving publication**;
defamation risk; distinguishing satire; assessing missing perspectives; changing methodology.

**And there is a legal reason, not only an ethical one.** The defamation defences that would protect
this work — honest opinion and publication in the public interest — **require a human to have held
a belief**. A system holds none. **The human review step is not overhead on the product; it is the
product's legal defence.**

### What should never be automated?

Publication of anything naming a real person or organisation. Coordination attribution. Bot-status
claims. Motive attribution. Any per-individual score.

### What data would be required?

Archived source copies; UK company, PSC, charity, procurement, donation and lobbying records;
media-ownership data where it exists; original-language sources. **And the honest finding is that
this is getting harder, not easier:** EU beneficial-ownership access was struck down in 2022;
CrowdTangle is gone and its replacement has no historical data; the DSA research route structurally
disfavours commercial entities; **and a commercial product has no UK copyright exception for text
and data mining, so news ingestion requires licences.**

### What legal advice would be required?

Before anything touches real people: whether recording political positions engages **Article 9**;
whether a commercial product can rely on the **journalism exemption** — untested, and the single
biggest assumption; **defamation exposure** and the continuing-publication problem; **EU AI Act
Article 5(1)(c)**, where an individual scoring feature could risk a prohibition carrying penalties
of up to 7% of global turnover; database right and platform terms; and the handling of any leaked
material.

### How could it strengthen the Adaptive Futures Engine?

**This is the strongest argument in the strand.** A futures engine cannot model organisations
realistically without modelling the information they act on — different actors receiving different
claims, trusting differently, and sometimes "confirming" a claim from three sources that share one
origin. Narrative analysis supplies **structured inputs and uncertainty**, never conclusions.

**And it can do that entirely inside the fiction.** A simulated information environment needs no
real ingestion, no real names, no legal exposure and no ethics review. **That is a real capability
with none of the risk**, and it is available now.

### Should this become a future product pillar?

**Not as a standalone product. Yes as an internal capability.**

Four reasons for the split:

1. **The market contracted for political reasons.** Logically raised nearly £30m, held platform and
   government contracts, and entered administration in July 2025 when Meta and TikTok withdrew from
   fact-checking. Meta halved its reporting cadence. Google removed ClaimReview from Search.
   NewsGuard is litigating against a regulator and is barred from Florida state contracts. **Every
   model that depended on platform budgets or on being a neutral arbiter has been damaged since
   2024.** The survivors sell into compliance and sanctions, where demand is regulatory.
2. **Ten uncontrolled risks sit on the critical path** — more than the entity-graduation strand, and
   several of them are harms to other people rather than to us.
3. **The evidence does not support the impact claim a commercial product would need.** The rigorous
   literature on the best-studied campaigns finds **no detectable effect on attitudes or voting**,
   with exposure so concentrated that **1% of users accounted for 70% of it**. A product sold on the
   scale of the threat would be selling something the evidence does not support.
4. **The safest and most valuable use needs none of the risky parts.** Simulated information
   environments for the futures engine, and fictional misinformation exercises for training, are
   both entirely inside the fiction.

**And one reason to keep it written down:** it changes how MERIDIAN should model information *now*.
People receiving different claims, from sources of differing independence, with strategic framing,
is a better simulation than one where everyone gets clean facts — and that is cheaper to design in
than to retrofit.

### The safest first demonstration

**PRODUCT PROPOSAL.** One historic, well-documented, already-researched contested event where
primary sources are archived and later evidence clarified what happened. Then, by hand:

1. Assemble a small, manually reviewed source set.
2. Trace **one claim** through 20–50 archived publications.
3. Identify which reports are genuinely independent.
4. Record how the wording changed at each step.
5. Map disclosed ownership and funding.
6. Identify documented incentives.
7. Compare local-language and English framing.
8. Record what was missing at each stage.
9. Compare the bounded assessment against what later turned out to be true.
10. **Document the false positives and the uncertainty.**

**No live monitoring. No social-media collection. No real-person profiling. No accusations. No
publication without review.**

It answers one question: **would a careful human with a week have produced a better answer without
the method?** A "no" would be a genuinely useful result — and on the evidence in §24, where the only
comparable work is investigative journalism done by hand, it is a real possibility.

---

**Recommended position: an internal capability for the futures engine, a written direction for
everything else, and no external product until the core product is understood by a first-time
user.** Revisit the standalone question only if the first experiment shows the method beats a
careful human, and only with legal advice on the four questions above.
