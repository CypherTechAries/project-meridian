# Annotated source register and data-source inventory

**All URLs accessed 21 July 2026.** This register records what was verified, how, and — as
importantly — **what was not**. Read the verification column before citing anything.

**Verification levels:** **PRIMARY** (document fetched and read) · **PRIMARY-PARTIAL** (partly read;
paywall, preview or extraction limit) · **SECONDARY** (via a reliable secondary source) ·
**METADATA** (existence and identifiers confirmed only) · **NOT VERIFIED** (**do not cite**)

**Three corrections this research produced to our own briefs**, recorded because they matter:

1. **DPA 2018 Sch 1 para 24 is "Disclosure to elected representatives"** — not the journalism
   condition. The journalism condition is **Sch 1 Part 2 para 13**. Our brief cited the wrong
   paragraph.
2. **The ICO Data protection and journalism code of practice is IN FORCE** (issued 1 Feb 2024,
   effective 22 Feb 2024). It is the *automated decision-making* guidance that is draft.
3. **There is no Nizzoli et al. paper on the 2019 Indian election.** The coordination paper is on
   the **2019 UK general election**; the Indian election work is by different authors.

---

## 1 · Coordination, automation and effectiveness

| Source | Publisher · date | Level | Class | Claim used | Limitations |
|---|---|---|---|---|---|
| Rauchfleisch & Kaiser, *The False Positive Problem of Automatic Bot Detection* — DOI 10.1371/journal.pone.0241045 | *PLoS ONE* · 2020 | SECONDARY | RESEARCH FINDING | Precision 59% at the common threshold; **24% on German politicians**; recall 20%; **27.2% of accounts crossed the threshold within 3 months** | GPT-era tools not covered; single platform |
| Gallwitz & Kreil, *Investigating the Validity of Botometer-based Social Bot Studies* — arXiv:2207.11474 | MISDOOM · 2022 | SECONDARY | RESEARCH FINDING | Manual examination found hundreds of "bots" were ordinary humans | Authors' own experiments; not independently replicated |
| Botometer X status — osome.iu.edu | Indiana OSoMe · 2023 | SECONDARY | INCIDENT | **No live data since mid-2023**; archival model pre-dates generative AI | — |
| Pacheco et al., *Uncovering Coordinated Networks on Social Media* — arXiv:2001.05658 | ICWSM · 2021 | SECONDARY | RESEARCH FINDING | The generic trace→network→cluster recipe; **top 0.5–1% edge filtering**; authors warn coordination ≠ intent, and that **news-site share buttons** create spurious coordination | Edge threshold is a tuned dial, not principled |
| Nizzoli et al., *Coordinated Behavior... 2019 UK General Election* — arXiv:2008.08370 | ICWSM · 2021 | SECONDARY | RESEARCH FINDING | Recovered **pension campaigners and loan-charge protesters** alongside partisan networks; authors state they **cannot distinguish inauthentic from authentic**; automation and coordination are **orthogonal** | **The clearest published demonstration of the false-positive problem** |
| Jakesch et al., *Trend Alert* — arXiv:2104.13259 | ACM CSCW · 2021 | SECONDARY | RESEARCH FINDING / INCIDENT | 600 WhatsApp groups, **75 hashtag campaigns**, volunteers copy-pasting from **real personal accounts** | **Off-platform coordination is invisible to every API** |
| Giglietto et al., Coordinated Link Sharing Behaviour — DOI 10.1080/1369118X.2020.1739732 | *Inf. Comm. & Society* · 2020 | SECONDARY | RESEARCH FINDING | CLSB framed as **"a signal to surface sources of problematic information"** — candidate generation, not verdict | Entity-level; URL-based; **CooRnet tooling suspended** post-CrowdTangle |
| Pantè et al., *Beyond Interaction Patterns* — arXiv:2502.17344 | 2025 | SECONDARY | RESEARCH FINDING | Re-examined published **inter-state coordination** claims with control datasets → **no evidence**; prior findings attributed to missing baselines | **A system without a baseline will manufacture findings** |
| Mannocci et al., *Detection and Characterization of Coordinated Online Behavior: A Survey* — arXiv:2408.01257 | rev. Apr 2026 | METADATA | RESEARCH FINDING | Coordination is core to healthy communities **and** to disinformation | Best single cite for "coordination is not a harm category" |
| Magelinski, Ng & Carley, *A Synchronized Action Framework* — arXiv:2105.07454 | 2021 | SECONDARY | RESEARCH FINDING | Single-signal methods misclassify authentic collective mobilisation | — |
| Eady et al., *Exposure to the IRA campaign... and attitudes and voting behavior* — DOI 10.1038/s41467-022-35576-9 | *Nature Communications* · 9 Jan 2023 | SECONDARY | RESEARCH FINDING | **No meaningful relationship** to attitudes, polarisation or voting; **1% of users = 70% of exposures**; eclipsed by domestic media | Twitter only; single campaign; **does not rule out effects on faith in elections** |
| Bail et al. — DOI 10.1073/pnas.1906420116 | *PNAS* · 2020 | SECONDARY | RESEARCH FINDING | No evidence of substantial effect across six measures | One-month window; n=1,239; post-election |
| Guess, Nyhan & Reifler — DOI 10.1038/s41562-020-0833-x | *Nature Human Behaviour* · 2020 | SECONDARY | RESEARCH FINDING | Untrustworthy sites a small share of diets; **~6 in 10 visits from the 10% most extreme** | US, 2016 |
| Allen et al. — DOI 10.1126/sciadv.aay3539 | *Science Advances* · 2020 | SECONDARY | RESEARCH FINDING | **Origin of the "0.15% of daily media diet" figure**, frequently misattributed | US |
| Budak et al., *Misunderstanding the harms of online misinformation* — DOI 10.1038/s41586-024-07417-w | *Nature* · 6 Jun 2024 | SECONDARY | RESEARCH FINDING | Exposure rare and concentrated among a motivated fringe; harms **mis-located**, not absent | Review not measurement; US/Twitter/Facebook weighted; **contested**; effect sizes NOT verified |
| Google TAG Dragonbridge bulletins | Google · 2022–2024 | SECONDARY | RESEARCH FINDING | **53,177 channels disabled; 58% zero subscribers; 42% of videos zero views**; "practically no organic engagement"; AI video **did not raise engagement** | **Reported by the platform that did the enforcement** — obvious interest. No independent audit |
| OpenAI threat reports | OpenAI · 2024–2026 | PRIMARY-PARTIAL | RESEARCH FINDING | None of the first five networks exceeded breakout category 2; **no significant engagement gain from AI**; later framing "bolting AI onto old playbooks" | **Vendor self-reporting**; survivorship bias — only detected operations counted. Oct 2025 / Feb 2026 PDFs **not retrieved** |
| Romania 2024 election annulment | DFRLab, Global Witness, Commons Library · 2024–25 | SECONDARY | INCIDENT | Court annulled round one; **no ties to the alleged foreign sponsor established** 18 months on; no ballot fraud found | **Cuts both ways.** Domestic undeclared promotion equally consistent |
| Tenet Media indictment | US DOJ / NPR / CJR · Sept 2024 | SECONDARY | INCIDENT | ~$10m covert funding; commentators say unwitting, not charged | **Undetectable by coordination analysis**; exposed by financial investigation |
| Doppelganger / CopyCop | EU DisinfoLab, Qurium, Recorded Future, VIGINUM · 2022–2026 | SECONDARY | INCIDENT | 17+ cloned media brands; 32 domains seized 2024; **still active**; 200+ new fake sites since Mar 2025 | VIGINUM PDF not read in full |
| Narrative laundering — Clemson Media Forensics Hub; CSIS; NATO StratCom COE | 2020–2025 | SECONDARY | RESEARCH FINDING | Chains from placement → obscure outlets → fake local news → sincere domestic commentators | Media Psychology Review 2025 study not read in full |

---

## 2 · Adjacent products and services

| Service | Level | Ownership | Funding | Incentives | Source independence | Amplification | Notes |
|---|---|---|---|---|---|---|---|
| **Ground News** | SECONDARY | ✅ own data (2,276 outlets) | ⚠️ partial | ❌ | ⚠️ implicit | ❌ | **Aggregates AllSides, Ad Fontes and MBFC for bias/factuality** — quality capped by theirs |
| **NewsGuard** | SECONDARY | ⚠️ disclosure only | ⚠️ disclosure only | ⚠️ conflicts only | ❌ | ❌ | Human journalists, 9 criteria. **Sued the FTC Feb 2026; barred from Florida state contracts.** No independent inter-rater reliability audit found |
| **AllSides** | SECONDARY | ❌ | ❌ | ❌ | ❌ | ❌ | Blind bias surveys, n≈381; **perception not content**; outlet-level; US axis |
| **Ad Fontes Media** | SECONDARY | ❌ | ❌ | ❌ | ❌ | ❌ | Article-level, 3-analyst balanced pods. **Score-visibility-then-discussion risks anchoring** |
| **Graphika** | SECONDARY | ❌ | ❌ | ❌ | ⚠️ structural | ✅✅ | Still independent; **repositioned toward brand/fraud** |
| **Blackbird.AI** | SECONDARY | ❌ | ❌ | ❌ | ❌ | ✅ claimed | $28m Jan 2026. **Homepage counters render "0 Trillion"**; bot detection claimed with no published methodology |
| **Logically** | SECONDARY | — | — | — | — | — | **Administration July 2025**; pre-pack to a company run by a former director. Lost Meta and TikTok contracts |
| **Recorded Future** | SECONDARY | ❌ | ❌ | ❌ | ⚠️ infrastructure | ✅ partial | **Mastercard acquisition closed 20 Dec 2024, $2.65bn** |
| **Meta CIB reporting** | SECONDARY | ❌ | ⚠️ | ⚠️ | ❌ | ✅ own platform | **Quarterly → semiannual**; H1 2026 leads with scams, not state IO |
| **Google TAG / Influence Ops Bulletin** | PRIMARY-PARTIAL | ❌ | ❌ | ❌ | ❌ | ✅ own platform | **Reports actions taken, not evidence.** No detection method, evidence standard or error rate disclosed. **Unfalsifiable by outsiders** |
| **Microsoft MTAC** | SECONDARY | ❌ | ❌ | ⚠️ | ⚠️ | ✅ | Scale/Stakes/Stickiness framing; "5% of actors = 95% of impact" **has no published derivation** |
| **EU DisinfoLab** | SECONDARY | ✅ | ✅ | ✅ | ✅ | ✅ | **The only full-axis example** — *Indian Chronicles*, 750+ fake outlets. **Hand-built journalism, not a system.** Does not disclose its own funders |
| **GDELT** | SECONDARY | ❌ | ❌ | ❌ | ❌ | ❌ | Free, 100+ languages, back to 1979. **Documented false positives; measures reporting not reality; restricted-press countries under-represented; tone unreliable across languages.** Funded by Google Jigsaw and USIP |
| **Media Cloud** | SECONDARY | ❌ | ❌ | ❌ | ❌ | ❌ | Active; 25,000+ source directory, 1bn+ stories. Attention research, not ownership |
| **OpenCorporates** | SECONDARY | ✅ legal | ⚠️ | ❌ | ❌ | ❌ | 230m+ records, 145+ jurisdictions, provenance links. **Largely does not resolve beneficial ownership** |
| **OCCRP Aleph** | SECONDARY | ✅✅ | ✅ | ⚠️ | ⚠️ | ❌ | 1bn+ records; entity cross-referencing. **Migrated to Aleph Pro Dec 2025; commercial tiers in 2026. Contains leaked databases — licence per dataset** |
| **Sayari** | SECONDARY | ✅✅ | ✅ | ⚠️ | ❌ | ❌ | Genuine beneficial-ownership resolution. **TPG majority investment Apr 2024** — PE-controlled |
| **LittleSis** | SECONDARY | ✅ | ✅ | ✅✅ | ⚠️ | ❌ | **Volunteer-curated with an explicit advocacy stance**; US-centric. Lead generation, not authority |
| **OpenSanctions** | SECONDARY | ⚠️ | ⚠️ | ✅ PEP | ❌ | ❌ | **CC-BY-NC — commercial use needs a licence.** FollowTheMoney ontology, interoperable with Aleph |
| **Wikidata** | SECONDARY | — | — | — | — | — | Identifier spine. **Many claims unsourced; vandalism detection "in its infancy"; 37.7% of persons had no link.** Use as ID crosswalk, never as evidence |
| **Media Ownership Monitor** | SECONDARY | ✅✅ | ✅ | ⚠️ | ❌ | ❌ | **Moved from RSF to Global Media Registry 2019.** 34 countries; Africa=2; **UK, US, China, Russia absent**. Snapshots, not a feed |
| **EU Media Pluralism Monitor** | SECONDARY | ✅ | ✅ | ⚠️ | ❌ | ❌ | **UK not in the annual cycle post-Brexit**; only a bespoke 2023 report for Ofcom, which rated UK media ownership transparency **HIGH RISK** |

**The pattern, and the strategic finding:** consumer tools measure slant and touch almost none of the
five axes; threat-intel does coordination and never ownership; ownership databases do ownership and
never narrative. **The join is empty.**

---

## 3 · UK public records — data-source inventory

| Source | Access · cost · licence | Update | Historic | **Limitations that matter** |
|---|---|---|---|---|
| **Companies House** | Web, REST API (600 req/5 min), streaming, monthly bulk. Free, OGL | Live | Deep per company | **Not substantively verified.** Bulk = **live companies only**. Officer identity unstable across companies. **From 26 Jan 2026 the register of members is no longer centrally public — a regression** |
| **PSC register** | Within CH products | Live | Yes | **25% threshold is the design flaw** — four holders at 25% = no PSC. ~13% filed none. **Four in five SLPs named none.** "Significant influence" almost never used. **A PSC record may be a relevant legal entity, not an individual** |
| **Register of Overseas Entities** | Within CH | Live | Since 2022 | 33,100 entities. **Trusts behind an application gate.** No published compliance rate |
| **Trust Registration Service** | **Not public** | — | — | HMRC/law enforcement/obliged entities, plus narrow "legitimate interest" per-case. **Researchers rarely succeed** |
| **NSSIF** | Web only | Ad hoc | Partial | Fund-level commitments only. **Any portfolio list built from public records is incomplete by construction** |
| **British Business Bank** | Annual PDF | Annual | PDFs | **Ultimate borrowers under guarantee schemes are not published** |
| **National Wealth Fund** | Web, annual report | Ad hoc | Both names | **Renamed from UK Infrastructure Bank Oct 2024** — searches must use both. **Not a sovereign wealth fund** |
| **The Crown Estate** | Annual report | Annual | Yes | **Not subject to FOI.** Lease terms unpublished. Crown Estate Act 2025 granted borrowing powers. *Duchies are less transparent still* |
| **LGPS funds** | Annual reports, committee papers, **FOI** | Annual | Yes | **Pooling reduces look-through.** **USS is private, not FOI-able** — commonly misclassified |
| **Find a Tender / CDP** | Web, OCDS feeds. Free | Continuous | Yes | Procurement Act live **24 Feb 2025**. **Framework call-offs under-reported; subcontractors invisible; NHS clinical under a separate regime.** No post-go-live compliance assessment found |
| **Register of Consultant Lobbyists** | Web, scrape. Free | Quarterly | Yes | **Covers 5–15% of UK lobbying.** In-house excluded. Ministers/Perm Secs only. **No subject matter.** VAT-threshold loophole exempts small and many foreign lobbyists |
| **Foreign Influence Registration Scheme** | Public register | Ongoing | Since Jul 2025 | **Most significant new influence source since 2023, and under-used.** Foreign *power* direction only; broad exemptions |
| **Electoral Commission** | Web, CSV. Free | Quarterly/weekly | To 2001 | **Unincorporated associations need not check their own donors.** ~£64m since 2001. **Max fine £20,000** |
| **Ministerial meeting returns** | Per-department, mixed formats | Quarterly | Yes | **"Purpose" field averages 11 words** (Scotland: 118). No central register, no schema, no identifiers |
| **Charity Commission** | Web, API (beta), daily extract. Free, OGL | Daily | ~5 yrs financial | **Does not show who funds a charity.** Detail only above £500k income. Trustees are names only — hard to link to CH |
| **Think-tank funding** | whofundsyou.org | Rolling | Partial | **No longer a complete annual snapshot** — moved to risk-based updates. **Transparify dormant since ~2018.** No UK legal duty to disclose funders |
| **UKRI Gateway to Research** | API. Free, OGL | Regular | To ~2006 | Best UK research-funding dataset. **No public register of university donations**; FOI is the route |
| **Ofcom / media ownership** | Licence register; periodic report | Varies | Yes | **No UK media ownership register.** Print and online have none at all |

**International:** EU public beneficial-ownership access **struck down 22 Nov 2022** (*WM and Sovim*);
replaced by legitimate-interest access, per-request and per-entity — **you cannot map a network**.
Core AMLD6 provisions due **10 July 2026**. **~39 of ~104 jurisdictions have fully public registers.**
**Open Ownership's aggregated register service is believed retired** — verify before building on it.

---

## 4 · Legal

| Source | Level | Class | Claim used | Limitations |
|---|---|---|---|---|
| UK GDPR Art 9; ICO *What is special category data?* | SECONDARY | REGULATOR GUIDANCE | Inferring with "reasonable degree of certainty" engages Art 9; processing **with intent to infer** engages it "irrespective of statistical confidence" | **ICO returned HTTP 403 to all fetches** — via search extracts only. **Re-verify by direct reading** |
| DPA 2018 Sch 1 Pt 2 **para 13** | PRIMARY | SETTLED LAW | Journalism condition — **only where the subject matter is wrongdoing** | Requires appropriate policy document. **Our brief cited para 24 in error** |
| DPA 2018 Sch 2 Pt 5 **para 26** | PRIMARY | SETTLED LAW | Disapplies Art 5(1)(a)–(e), Art 6, **Art 9**, Arts 13–17, Art 21(1). Requires **view to publication** + **reasonable public-interest belief**, judged against BBC/Ofcom/Editors' codes | **No UK judgment applies it to a commercial data product.** Biggest untested assumption |
| ICO journalism code of practice | SECONDARY | REGULATOR GUIDANCE | **In force** — issued 1 Feb 2024, effective 22 Feb 2024 | Post-DUAA update status unknown |
| Defamation Act 2013 ss.1, 3, 4 | PRIMARY | SETTLED LAW | s.3(5) defeated if **the defendant did not hold the opinion**; s.4 requires **"the defendant reasonably believed"** | **A system holds no opinion and no belief.** No UK judgment on AI-generated defamation |
| *Banks v Cadwalladr* [2023] EWCA Civ 219 | SECONDARY | CASE LAW | A s.4 defence **must be made out afresh for continuing publication** when circumstances change | **A hosted database publishes continuously** |
| *Bloomberg LP v ZXC* [2022] UKSC 5 | SECONDARY | CASE LAW | A person under criminal investigation has a **reasonable expectation of privacy before charge** | **Truth is no defence to MPI.** Hard design rule |
| CDPA s.29A + *Report on Copyright and AI*, 18 Mar 2026 | PRIMARY (gov.uk) | SETTLED LAW / POLICY | TDM exception is **non-commercial research only**; Government confirmed **no broad exception** | **A commercial product needs news licences.** No exception available |
| *Ryanair v PR Aviation* C-30/14 | SECONDARY | CASE LAW | Where no IP subsists, **contractual restrictions still bind** | "No database right" is **not** a green light |
| Copyright and Rights in Databases Regs 1997 | SECONDARY | SETTLED LAW | Catches **repeated systematic extraction of insubstantial parts** | *BHB* "obtaining not creating" is a case-by-case argument |
| *Travel Counsellors v Trailfinders* [2021] EWCA Civ 38 | SECONDARY | CASE LAW | A recipient is bound where they **knew or ought to have known** material was confidential | **Knowing a corpus is leaked supplies the element** |
| EU AI Act Art 5(1)(c) + Commission guidance | SECONDARY | SETTLED LAW + GUIDANCE | Three cumulative conditions; penalties to **€35m or 7% of turnover** | **The "unrelated context" limb is untested. No CJEU authority. Highest-consequence unresolved item** |
| DSA Art 40 delegated act | SECONDARY | REGULATORY | In force **29 Oct 2025**; DSA Data Access Portal live; 80-working-day response | **EU systemic risks only; VLOPs only; independence from commercial interests structurally disfavours a commercial product** |
| EMFA Art 6 | SECONDARY | SETTLED LAW | Applicable **8 Aug 2025**; ownership, beneficial owners and state-advertising funds must be published | Implementation uneven; EU providers only |
| PACE 1984 / Contempt of Court Act s.10 | PRIMARY-PARTIAL | SETTLED LAW | Source protection attaches to "a publication for which he is responsible" | **Doubtful that a commercial analytics product holds "journalistic material"** |

---

## 5 · What could not be verified — read before citing

**Legal**
1. **All ICO guidance** — ico.org.uk returned HTTP 403 to every fetch.
2. **UKJT Legal Statement on AI Harms** (7 Jul 2026) — secondary coverage only.
3. Defamation Act **s.2 (truth)** and **s.8 (single publication)** — not fetched.
4. **EU AI Act territorial scope** and whether the prohibited-practices guidance carves out research
   or journalism — **not checked. Material to the 7%-of-turnover question.**
5. **National Security Act 2023, Official Secrets Acts, Terrorism Act 2000 s.58, Investigatory Powers
   Act 2016** — **not researched at all**; material to leaked-material handling.
6. CJEU accuracy-of-inference line (*Nowak*, *SCHUFA*) — not researched.
7. **OCCRP Aleph terms of use** — not researched.

**Data sources**
8. **Contracts Finder retirement** — secondary sources say April 2026; no primary announcement found.
9. **TRS / ROE trust-disclosure expansion SIs** — commencement unconfirmed.
10. **ROE non-compliance rate** — no authoritative figure published.
11. **NAO/PAC assessment of Procurement Act transparency compliance** — none found.
12. **Government response to the Lobbying Act post-legislative review** — not located.
13. **Open Ownership aggregated register** — believed retired; confirm before building.
14. **US FinCEN beneficial ownership scope** — heavily litigated through 2025.
15. **EMFA national ownership databases per Member State** — not checked.

**Research**
16. **OpenAI Oct 2025 / Feb 2026 threat reports** — primary PDFs not retrieved.
17. **EEAS 4th FIMI Threat Report** (Mar 2026) — HTTP 403; all figures secondary.
18. **X/Twitter API pricing** — primary source returned 402; figures from resellers with an incentive
    to overstate. Only "no academic tier since mid-2023" is solid.
19. **Budak et al. specific effect sizes** — paywalled.
20. **VIGINUM Jan 2026 report** — located, not read in full.
21. **Exact CooRnet thresholds** as shipped — read the source before citing.
22. **NewsGuard inter-rater reliability** — no independent audit found.
23. Company-profile aggregators (Tracxn, PitchBook, CB Insights, Owler) returned **internally
    inconsistent and in one case demonstrably wrong** data. **Do not cite without primary
    confirmation.**

**Three claims that are genuinely unresolved in law — not merely unresearched:**
whether a commercial analytics product can rely on the journalism exemption; whether defamation
defences can survive machine-generated output; and whether individual influence scoring falls inside
the EU AI Act's social-scoring prohibition.
