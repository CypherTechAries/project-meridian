# Ownership, funding and incentives

Part of the [Narrative and Incentive Intelligence](NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md) research
strand. **Research only. Nothing here is implemented, and nothing here is a plan to collect data.**

Sources and verification status: [NARRATIVE-INTELLIGENCE-SOURCES.md](NARRATIVE-INTELLIGENCE-SOURCES.md).

---

## 1. The idea, and its limit

The instinct behind this document is sound and old: **follow the money**. If you want to know why a
claim is being made, look at who benefits, who pays, and who depends on whom.

The limit is equally important and is the whole reason this document exists:

> **A financial connection is evidence of an incentive. It is not evidence of coordination, and it
> is not evidence that anybody did anything.**

A system that cannot hold that distinction produces conspiracy theories with citations. That is
worse than producing nothing, because the citations make it persuasive.

---

## 2. Seven relationship categories that must never be collapsed

**PRODUCT PROPOSAL.** These are the categories the founder's brief set out, with what each requires
as evidence and what each licenses you to say.

| # | Category | What must be shown | What may be said | What may **not** be said |
|---|---|---|---|---|
| 1 | **Direct control** | Formal authority — majority shareholding, board control, editorial appointment right | "X can determine what Y publishes" | "X directed this article" |
| 2 | **Financial dependence** | Material reliance — funding, contracts, advertising, investment share | "Y derives a material share of income from X" | "Y publishes what X wants" |
| 3 | **Incentive alignment** | Both benefit from the same outcome | "Both would benefit if this were believed" | "They acted together" |
| 4 | **Shared information dependency** | Multiple outputs trace to one source | "These reports share one origin" | "These outlets colluded" |
| 5 | **Access dependence** | Reliance on continued access to officials, platforms, partners | "Y's reporting depends on access X controls" | "X threatened Y" |
| 6 | **Demonstrated coordination** | Direct evidence — documents, admissions, platform attribution, contracts | "There is evidence of organised activity" | Anything beyond what the evidence shows |
| 7 | **Correlation** | Similar behaviour, no established mechanism | "These actors behaved similarly" | Any causal claim at all |

**Only category 6 supports a coordination claim.** The other six are context.

**INFERENCE.** Category 5, access dependence, is the one most often missed and is frequently the
strongest real mechanism. A journalist who loses access loses their job. No money changes hands, no
instruction is given, and the effect on coverage can exceed anything ownership produces. It is also
almost impossible to evidence from public records, which is exactly why it should be named as a
category rather than quietly folded into "incentive alignment".

---

## 3. What UK public records can actually show

**The single most important finding in this document**, and it applies to every source below:

> **CURRENT LAW / RESEARCH FINDING.** Almost nothing in the UK transparency estate is verified data.
> Companies House, the PSC register, the Register of Overseas Entities and the Electoral Commission
> register are **self-declaration systems**. They record what someone said, not what is true.
> ECCTA 2023 verifies **who is filing** — identity — not **what they filed**.

Companies House's own reporting for 2025–26 describes blocking suspicious filings and post-hoc
cleansing, not substantive verification. In that year it took targeted action against 157,679
companies, removed 22,900 documents for inaccuracy and blocked 26,797 suspicious filings. Those
numbers are evidence of a register being actively policed — and evidence of how much bad data
reaches it.

### 3.1 Company ownership

**Companies House** — ~5.48m companies, free, Open Government Licence, REST and streaming APIs,
monthly bulk snapshot. Genuinely good infrastructure.

**Traps, all verified:**
- The **bulk product covers live companies only**. You cannot reconstruct history from it; you must
  harvest over time or use the stream.
- **Officer identity is not stable.** The same human appears under multiple officer IDs across
  companies. New personal codes should improve this going forward, not retrospectively.
- Small-company and micro-entity filing regimes mean **most of the register carries almost no useful
  financial information**.
- **From 26 January 2026 companies can no longer elect to keep the register of members on the public
  register.** That is a transparency **regression** for shareholder data, and it happened this year.

**Persons with significant control** — and here the founder-approved correction from the
simulation-born-entities strand applies directly: the statutory definition of a PSC is an
*individual*, **but a PSC register may instead record a registrable relevant legal entity**, so
control chains may legitimately pass through legal entities.

**The design flaw is the threshold.** Control is reportable at **more than 25%**. Four people at 25%
each produce a company with **no PSC at all**, entirely lawfully. Splitting to 24.9% is trivial.

**Documented gaps:** roughly 13% of companies filed no PSC at all; "significant influence or
control" — the qualitative catch-all that would capture de facto control by non-shareholders — is
almost never used; trusts can name a trustee rather than a beneficial owner; foreign entities
frequently terminate the traceable chain; and **four in five Scottish Limited Partnerships had not
named a PSC**.

**Trusts are the deepest hole.** The Trust Registration Service is **not a public register**. Access
is limited to HMRC, law enforcement, obliged entities, and "legitimate interest" requesters who must
show they are investigating **a specific instance** of money laundering — decided case by case by
HMRC, with no publication and no appeal. In practice researchers rarely succeed.

### 3.2 State investment vehicles

**A correction worth carrying:** the **UK Infrastructure Bank was renamed the National Wealth Fund
on 14 October 2024**. Historical searches must use both names — a real trap for automated matching.

**And a precision point that will be attacked if we get it wrong:** the UK has **no sovereign wealth
fund** in the accumulation sense. The National Wealth Fund is a development/impact investor funded
by government borrowing, not by surplus revenues. Conflating them is a factual error.

**NSSIF** (National Security Strategic Investment Fund, operated by the British Business Bank) —
up to £330m for FY2026-27 to 2029-30. Discloses fund-level commitments, **not a complete portfolio
list**. Because it invests largely *through* venture funds, ultimate portfolio companies are only
discoverable via fund managers' announcements or share-allotment filings. **Any NSSIF portfolio list
built from public records is incomplete by construction.**

**British Business Bank** — overwhelmingly a fund-of-funds and guarantee provider. **The ultimate
borrowers under its guarantee schemes are not published**, including the Covid-era schemes. No
transaction-level open data.

**The Crown Estate** — and the founder's instinct here was right. It is **not** the monarch's
private property and **not** government property: a statutory corporation whose assets are held *in
right of the Crown*, with net revenue going to the Treasury. The **Crown Estate Act 2025** (Royal
Assent 11 March 2025) granted borrowing and wider investment powers for the first time. It is **not
subject to FOI**, individual lease terms are unpublished, and its holdings are not available as a
complete dataset. The **Duchies of Lancaster and Cornwall are closer to private and notably less
transparent** — a separate line of enquiry.

**Public-sector pension funds** are the largest genuinely state-linked capital pools and, because
LGPS funds are **subject to FOI** and publish committee papers, by far the most researchable. But
**pooling reduces transparency in practice**: once assets sit in a pooled vehicle the individual
fund reports a pool holding, not underlying securities. **USS is a private trust-based scheme, not
public sector, and not subject to FOI** — a common misclassification.

### 3.3 Procurement, lobbying, donations

**Procurement** — the Procurement Act 2023 went live **24 February 2025**, with a Central Digital
Platform and a much richer notice set including contract performance and KPI-breach notices.
Genuinely better. But: **compliance with transparency notices is the weak point** and was
persistently poor under the old regime; **framework call-offs** carry a huge share of real spend and
are frequently under-reported; **subcontractors are largely invisible**; and NHS clinical services
sit under a separate regime entirely.

**Lobbying — this is the most important limitation in the entire document.**

> **The Register of Consultant Lobbyists covers 5–15% of UK lobbying.** In-house lobbyists —
> corporations, banks, energy firms, platforms, trade associations, charities, unions lobbying for
> themselves — register **nothing**. So **85–95% of UK lobbying appears in no register at all.**

It gets worse. Only communications with **Ministers and Permanent Secretaries** count, so lobbying
of special advisers, junior officials and regulators — where policy is actually shaped — is out of
scope. **No subject matter is disclosed**, only the client's name. And a **VAT threshold loophole**
means anyone below £90,000 turnover, **and any foreign business not required to register for UK
VAT**, can lobby ministers without appearing. The Registrar has publicly called for its removal.

The original justification for excluding in-house lobbyists was that they would be visible in
departmental transparency returns. **That justification does not hold.** Those returns average
**11 words** in the "purpose" field (down from 13 in 2024), with entries like "to discuss the
industrial strategy". The Scottish register averages **118 words** for the same period — proving the
UK design is a choice, not a constraint.

**One genuinely useful new source is under-used:** the **Foreign Influence Registration Scheme**,
in force 1 July 2025 under the National Security Act 2023, with a public register of political
influence activity directed by a foreign power. It captures direction by a foreign *power*, not
foreign commercial lobbying, and exemptions are broad — but it is the most significant new
influence-mapping source since 2023.

**Political donations** — Electoral Commission register, free, back to 2001, quarterly (weekly
during campaigns). **Unincorporated associations are the central loophole**: they are permissible
donors and are **not required to run permissibility checks on their own donors**, so foreign money
can lawfully enter through them. ~£64m since 2001. The maximum fine is **£20,000**, widely
criticised as trivial.

**Not yet law:** the Representation of the People Bill (introduced 12 February 2026, carried over)
would tighten company donations and cap donations at £100,000. **Do not describe these as in
force.** And note the Electoral Commission's own criticism: the company test is defined by
**revenue, not profits**, and only profits can fund a donation — so the "foreign money loophole
closed" framing is contestable.

### 3.4 Media ownership

**There is no single UK media ownership register.** Ofcom holds broadcast licence records and
applies media ownership rules; the Enterprise Act public-interest regime is case-by-case and
political; **print and online publishers have no ownership register at all**.

The independent CMPF report for Ofcom (28 November 2023) rated **transparency of media ownership in
the UK as HIGH RISK**, citing the lack of effective ownership disclosure rules for both traditional
and digital media. **The UK is not in the routine annual Media Pluralism Monitor cycle post-Brexit**,
so that 2023 report is the most recent full application and is nearly three years old.

The **Foreign State Influence regime** (DMCC Act 2024, regulations July 2025) bars foreign powers
from controlling UK newspapers, with an exception permitting state-owned investors up to **15%** if
genuinely passive. Criticised in Parliament as porous — "influence to any extent" is hard to police,
and multiple states could each hold 15%.

---

## 4. The international picture just got worse

**CURRENT LAW, and it reverses the assumption most people hold.**

The CJEU struck down public access to EU beneficial ownership registers on **22 November 2022**
(*WM and Sovim SA*), holding it a disproportionate interference with Charter rights. Member states
shut public access within days. **Journalists and NGOs lost access overnight.**

The 2024 AML package replaced public access with **"legitimate interest" access**, presuming
legitimate interest for journalists, civil society and academia. Core provisions are due **10 July
2026** — now. About a third of member states missed the earlier July 2025 deadline, triggering
infringement proceedings.

**Public access has not been restored, and will not be.** Bulk access, scraping and systematic
cross-border network analysis are effectively dead in the EU for non-obliged entities. Access is
per-request and per-entity: **you cannot map a network.**

**INFERENCE, and it matters for this concept.** The UK PSC register remains fully public and free.
That makes **UK data disproportionately load-bearing** for any cross-border ownership analysis —
which makes the UK register's quality problems in §3.1 more dangerous, not less. A system built on
the one good public source will inherit that source's blind spots as its own worldview.

**The direction of travel is not monotonic.** EU public access went backwards in 2022; the UK
register of members went backwards in January 2026. Transparency does not ratchet forward, and a
product that assumes it does will make plans that fail.

---

## 5. An incentive framework that does not claim to read minds

**PRODUCT PROPOSAL.** Incentives are the point of this analysis and the easiest place to overreach.
Nobody can observe motive. What can be observed is *position* — what somebody stands to gain or lose
given their disclosed circumstances.

Four evidential tiers, and outputs must state which is in use:

| Tier | Meaning | Example |
|---|---|---|
| **DOCUMENTED** | The interest is on the public record | "A holds a disclosed shareholding in B" |
| **INFERRED** | Follows from documented facts by a stated step | "A's disclosed holding in B means A would benefit if B's sector expanded" |
| **POSSIBLE** | Consistent with the facts; other readings exist | "A may prefer outcome X" |
| **SPECULATION** | Not supported | **Not published, at all** |

Incentive categories worth naming — financial gain; asset protection; procurement advantage;
regulatory advantage; political authority; public legitimacy; institutional reputation; **continued
access**; audience growth; advertising revenue; ideological commitment; legal exposure; national
security interest; organisational survival; career advancement; risk avoidance.

**INFERENCE.** Two of those deserve emphasis because they are under-weighted in most analyses of
this kind. **Organisational survival** and **risk avoidance** explain far more institutional
behaviour than conspiracy does — an organisation that avoids a story because it fears a lawsuit
produces the same silence as one that was told to, and the two are indistinguishable from outside.
An honest system should say so rather than pick the more interesting explanation.

---

## 6. Central actors and concentration — where this gets dangerous

The founder's observation is empirically well founded: large systems often trace back to a small
number of central actors. Network analysis has the vocabulary — centrality, community detection,
board interlocks, common investors, shared advisers, chokepoints.

**And this is the single most dangerous capability in the concept.**

**INFERENCE.** Centrality is a property of a *graph you constructed*, from *sources you chose*, with
*joins you made probabilistically*. It is not a property of the world. Three specific hazards:

1. **The graph reflects disclosure, not reality.** Because 85–95% of lobbying is unregistered and
   trusts are opaque, the actors who appear central may simply be the ones who file. **A well-advised
   actor is invisible.** Concentration findings will systematically over-represent the compliant.
2. **Entity resolution errors compound.** Names in Companies House, the Electoral Commission
   register, Find a Tender and the Charity Commission **do not share identifiers**. Every join is
   probabilistic, and errors do not stay local — one wrong merge creates false centrality for a
   node that does not exist.
3. **Centrality invites a causal reading it cannot support.** "X is central to this network" is one
   short step from "X controls this network", and nothing in the mathematics licenses that step.

**Proposed rule:** centrality may be *displayed* with its construction visible — which sources,
which join method, which confidence — and may **never** be reported as a finding about control.

---

## 7. What these records genuinely cannot show

Stated plainly, because a system built on them must say so:

1. **Who really controls anything.** Control by contract, debt, nominee, family, golden share, trust
   or informal understanding is invisible by design.
2. **Truth.** Nothing is verified for substantive accuracy. **A confidently wrong register is worse
   than no register**, because it produces false negatives that look like findings.
3. **Money flows.** You can see a stake, a donation, a contract award. You cannot see the payment,
   the intermediary, the consultancy fee, the retainer, the speaking fee, the subcontract or the job
   offer.
4. **Influence.** 85–95% of UK lobbying is unregistered; meeting entries average 11 words; advisers
   and officials are out of scope. **You cannot map UK influence from UK public records alone.**
5. **Trusts.**
6. **Absence is not evidence.** A "no PSC" statement, a missing award notice, an unregistered
   lobbyist and an unlisted donor all look identical to "nothing happening". A system must
   distinguish **"not required to disclose"**, **"required but did not"**, and **"disclosed and
   genuinely nil"** — most published network analyses fail exactly here.
7. **Entity resolution is the hidden cost**, and every join introduces errors that must be
   quantified rather than assumed away.

---

## 8. Open questions

1. Can a useful ownership picture be built at all when the best public source covers one country and
   the rest of the world just closed?
2. What is the honest error bar on an entity-resolution join across four UK registers?
3. How is "not required to disclose" surfaced to a reader without implying something was hidden?
4. Is there any way to evidence access dependence from public records?
5. Should concentration analysis be built at all, given §6 — or is the risk of it being read as
   control too high to justify?
