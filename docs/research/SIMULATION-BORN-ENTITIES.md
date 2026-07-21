# Simulation-born entities and entity graduation

**Research report. Nothing here is implemented and nothing here is a commitment.**

MERIDIAN today cannot graduate an entity, has no ownership model, no permission model, no lineage,
no connection of any kind to the outside world, and no persistent entity that survives a scenario.
This report investigates whether it *should* eventually be able to, what would have to be true
first, and where the idea becomes unsafe or misleading.

Every claim is labelled:

| Label | Meaning |
|---|---|
| **FACT** | Verifiable and verified |
| **CURRENT LAW / GUIDANCE** | The position as stated by a primary legal or regulatory source, at the access date |
| **RESEARCH FINDING** | Reported in a cited study or standard |
| **PRODUCT PROPOSAL** | Our own design idea. Not validated |
| **INFERENCE** | Our reasoning from the above. May be wrong |
| **OPEN QUESTION** | Genuinely unresolved, by us or by anyone |

This is not legal advice. Where the report touches law it reports what sources say and marks what
they do not settle. Real decisions in this area would need a qualified professional.

Companion documents:
[ENTITY-GRADUATION-LIFECYCLE.md](ENTITY-GRADUATION-LIFECYCLE.md) ·
[GRADUATION-EVIDENCE-PACK.md](GRADUATION-EVIDENCE-PACK.md) ·
[ENTITY-GRADUATION-RISK-REGISTER.md](ENTITY-GRADUATION-RISK-REGISTER.md) ·
[SIMULATION-BORN-ENTITY-SOURCES.md](SIMULATION-BORN-ENTITY-SOURCES.md) ·
[product concept note](../design/ENTITY-GRADUATION-CONCEPT.md)

---

## 1. The executive idea

MERIDIAN invents companies, people, products and institutions, and gives them histories. Those
inventions currently stop existing when the run stops.

The idea is that some of them are worth keeping. A fictional company that was designed carefully,
put under repeated stress, and documented honestly is not only a story — it is a **design**. Entity
graduation is the controlled process of taking the parts of such an entity that can survive contact
with reality and using them to build something real.

The single sentence that governs everything else:

> **A simulation can produce a blueprint. It cannot produce a business.**

The blueprint is real and portable: a brand, a set of written procedures, an organisational shape, a
product specification, working software, a body of test scenarios, and — most valuable of all — a
record of how the design failed. The business is not: the customers, the revenue, the reputation and
the track record were invented, and inventing them proved nothing.

**INFERENCE.** The interesting reframing is not any individual graduated entity. It is that a
simulation which produces durable, honestly documented designs stops being a report generator and
becomes a design workshop — a place to build an organisation cheaply, break it many times, and only
then decide whether it is worth building for real. That changes what MERIDIAN is for.

**And the same properties make it an efficient way to mislead people, including ourselves.** A
fictional company with five years of invented history reads exactly like a real one. The most likely
failure of this concept is not technical: it is that somebody, in good faith, comes to believe that
a thing tested in a model was tested in the world. Every design decision in this report is shaped by
that.

---

## 2. What a simulation-born entity is

**PRODUCT PROPOSAL.** A persistent fictional person, organisation, institution, product, process or
asset originally created and developed inside MERIDIAN, with:

- a stable identifier that carries its fictional origin in the identifier itself;
- a versioned history of what it did and why;
- a declared record of what was modelled, assumed, and not modelled;
- an origin record distinguishing what the engine produced from what a human authored.

The working definition offered for this research was adequate but **improved in one respect**: the
original said "originally created and developed inside MERIDIAN". That is not sufficient, because an
entity assembled from imported material is not really simulation-born, and its rights position is
completely different. The definition should require the origin record, not just the location of
creation.

**Note on the word "asset".** A synthetic character's software, brand and intellectual property may
be assets. A human person is never an asset. This report uses "asset" only in the first sense, and
the distinction is not cosmetic — the section on legal status explains why a simulated person cannot
be owned *as a person*, and cannot consent to anything.

---

## 3. What entity graduation means

**PRODUCT PROPOSAL.** The controlled process through which **selected parts** of a simulation-born
entity are instantiated in the real world.

Three words carry the weight:

- **Selected** — never the whole entity. Most of it must be left behind.
- **Parts** — assets, not a being. There is no moment at which the entity "becomes real".
- **Controlled** — every step gated on new evidence about the real world, never on simulated
  success.

Three states must never be conflated, and the industry routinely conflates them:

1. **Simulation-born entity** — created inside MERIDIAN, no real counterpart.
2. **Real-world instantiation** — selected identity, software, procedures or IP deployed outside
   MERIDIAN, still with no specific real counterpart.
3. **Digital twin** — a model tied to *one specific* real-world counterpart, inside a declared
   validation envelope, with real information flow.

Section 17 sets out why the third is a different kind of claim and why applying the term loosely is
a substantive error rather than a stylistic one.

---

## 4. What can cross into reality

### 4.1 People and characters

| Can cross | Notes |
|---|---|
| Fictional identity, name, visual identity | Subject to trade mark and likeness checks |
| Character IP | The strongest commercial asset in this category |
| Declared expertise boundary | Valuable precisely because it is a limit |
| Knowledge package | The curated material it works from |
| Operating rules and communication style | |
| Decision history | As a fictional record, clearly labelled |
| Disclosure requirements | Must travel with the entity, not sit on a policy page |
| Software agent | |
| Generated media catalogue | Subject to the ownership questions in section 9 |

**Cannot cross, and must be stated explicitly wherever the entity appears:**

- The simulation does not become a human being.
- It acquires no human rights and no human legal identity.
- Simulated history is not evidence of real competence.
- It must never impersonate a real person.
- It cannot itself consent to anything.
- A human or a legal organisation remains accountable for everything it does.

**INFERENCE.** "Audience and reputation" was listed in the brief as potentially exportable. It
should be split. A real audience — people who actually followed a character — is real and can
transfer. A *simulated* reputation is not a reputation; it is a fiction about a fiction, and
carrying it across is the reputation-laundering risk in the register.

### 4.2 Organisations

| Can cross | Cannot cross |
|---|---|
| Name and brand | Simulated revenue |
| Purpose | Simulated customers and demand |
| Products and services as designs | Simulated market share |
| Organisational structure | Simulated regulatory approval |
| Procedures and policies | Simulated operating competence |
| Decision rules | Simulated credit or trading history |
| Software systems | |
| Commercial model as a hypothesis | |
| Tested crisis responses as exercises | |

Possible real forms: a registered company; a project inside an existing company; a cooperative; a
charity or community-interest company; a licensed operating model; a franchise; an internal unit.
Section 9 covers what each requires.

**INFERENCE.** The internal-project route is the most under-rated. It needs no incorporation, no
banking, no external disclosure, and it is the only one that can be tried this year.

### 4.3 Products

Exportable: software; requirements; CAD and manufacturing files; design specifications; test cases;
branding; documentation; pricing and supplier assumptions **as assumptions**.

**Simulated success does not replace** engineering testing, user testing, certification, safety
testing, market validation, or manufacturing validation. Section 11 and the sources register cover
what real simulation-to-physical practice actually requires, and it is considerable.

### 4.4 Institutions and processes

Exportable: governance model; decision procedure; escalation rules; training materials; exercise
scenarios; service blueprint; workflow software; policy-testing framework.

**INFERENCE.** This is the category where simulation history is worth the most, because a set of
crisis exercises is *inherently* fictional. A training scenario does not have to be real to be
useful, so nothing needs to cross the truth boundary at all. That makes it the safest category by a
wide margin, and it is discussed again in the recommendation.

### 4.5 Physical and infrastructure assets

The path is long and each arrow is a substantial programme:

```
simulation-born design → physical prototype → instrumented real asset
    → validated connected model → digital twin
```

Section 17 sets out what the last two arrows actually require.

---

## 5. What cannot cross, in one place

Consolidated because it is the most important list in the report:

- Simulated revenue, profit, funding.
- Simulated customers, demand, market share.
- Simulated reputation, popularity, brand equity.
- Simulated competence and operating experience.
- Simulated legal authority, licences, approvals.
- Simulated regulatory compliance.
- Simulated credentials or qualifications.
- Any performance claim outside the model's validation envelope.
- Any claim about a specific real person, organisation or place that the simulation did not model
  and could not have tested.
- Legal personhood, human rights, and the capacity to consent.

---

## 6. Entity categories

**PRODUCT PROPOSAL.** Six, ordered by how safely they can graduate — safest first. This ordering is
a conclusion of the report, not a taxonomy for its own sake.

| # | Category | Why this position |
|---|---|---|
| 1 | **Process / institution / training material** | Fiction is the *intended* form. Nothing must cross the truth boundary |
| 2 | **Product design** | Crossing is well understood; validation regimes already exist and are strict |
| 3 | **Organisation** | Crossing is mostly documents; needs a legal wrapper before it operates |
| 4 | **Brand / character as licensed IP** | Commercially strong, but disclosure and likeness risk begins here |
| 5 | **Synthetic person / service** | All of category 4 plus impersonation, anthropomorphism, and regulated-advice risk |
| 6 | **Digital twin of a real asset** | A claim about reality that can be wrong about reality. Hardest, and last |

---

## 7. Graduation lifecycle

Eleven states, in [ENTITY-GRADUATION-LIFECYCLE.md](ENTITY-GRADUATION-LIFECYCLE.md).

`SIMULATED` → `EXPORTABLE` → `SANDBOXED` → `REAL_DATA_READ_ONLY` → `SUPERVISED` →
`LEGALLY_WRAPPED` → `LIMITED_OPERATION` → `ECONOMICALLY_ACTIVE` → `TWINNED`, plus `SUSPENDED` and
`RETIRED` reachable from anywhere.

Three design decisions worth surfacing here:

- **`LEGALLY_WRAPPED` sits below any operating state.** Nobody acts before somebody is answerable.
- **`TWINNED` is not the top of the ladder.** It is a different kind of claim (section 17).
- **`SUSPENDED` is reachable instantly by one named person.** A control requiring a meeting is not a
  control.

**Most entities should stop at `EXPORTABLE` or `SUPERVISED`, and stopping is a success.**

---

## 8. Identity continuity

**OPEN QUESTION throughout.** This section deliberately reaches no conclusion.

Proposed continuity markers — **PRODUCT PROPOSAL**: stable entity ID; signed asset manifest;
immutable origin record; version history; declared governing rules; exported history; cryptographic
signatures; ownership chain; authorised operators; approved software version; a public continuity
statement.

The genuinely hard questions, with our best current reading:

**Is it the same entity if the software changes?**
*Our reading: continuity is a claim, not a fact.* Something is "the same entity" exactly insofar as
a documented chain says so and a reader can check it. Ship of Theseus arguments do not resolve; a
signed lineage record at least makes the claim inspectable.

**Is it the same entity if its legal owner changes?**
Legally the wrapper is a separate thing from the assets, and assets change hands without becoming
different assets. **INFERENCE:** ownership transfer does not break entity continuity, but it does
break *accountability* continuity, and the second matters more in practice.

**Is a company the same entity as its simulated predecessor?**
**No.** A registered company is a new legal person with no history. The simulated predecessor is,
at most, its design document. Any other answer is the reputation-laundering failure.

**Can several real instances descend from one simulation-born entity?**
Yes, and this is the normal case, not an edge case — think franchising. Section 14 proposes the
lineage vocabulary that lets several real entities acknowledge a common ancestor without claiming to
be one legal entity.

**Continuation, copy, franchise or derivative?**
All four are possible and they have different legal consequences. **The vocabulary must be chosen
per case and recorded**, not assumed.

**Can an entity return to simulation, and can real events be brought back in?**
Technically yes; safely, unclear. Two failure modes: **contamination** (real outcomes imported as
simulation history make a mixed record look validated) and **laundering** (a real failure re-enters
as a simulated event and gets quietly rewritten). Minimum discipline would be a separate, clearly
marked real-event stream that can never be presented as simulation output. MERIDIAN's existing
origin vocabulary is the right foundation and would need a new value, not a reused one.

---

---

## 9. Ownership and legal wrappers

**A report of what sources say, not legal advice.** Citations and verification status in
[SIMULATION-BORN-ENTITY-SOURCES.md](SIMULATION-BORN-ENTITY-SOURCES.md).

### 9.1 The finding everything else follows from

**CURRENT LAW.** UK law recognises natural persons and bodies corporate created by or under statute.
There is no route by which a software system, an agent or a fictional persona acquires legal
personality of its own. The nearest authoritative judicial statement is *Thaler v Comptroller-General*
[2023] UKSC 49: an AI machine cannot be named as inventor because the statute requires a natural
person. That is a narrow holding on the Patents Act 1977 and should not be over-read as a general
ruling on AI personality.

**INFERENCE.** A graduated entity cannot own, contract, employ, be liable, or be responsible. Every
one of those verbs attaches to a person or a company. This is not a policy choice MERIDIAN is
making; it is the structure of the law the concept must operate inside.

### 9.2 Becoming a real company

**CURRENT LAW.**

- A company is formed by "one or more persons" subscribing (Companies Act 2006 s.7). **A fiction
  cannot incorporate itself.**
- **A company must have at least one director who is a natural person** (s.155, in force).
- **A correction worth carrying, because the opposite is widely repeated:** the total ban on
  corporate directors in s.156A is **not** in substantive force as at 21 July 2026. SI 2024/270
  commenced the s.156B *exception-making power* only. The live rule remains s.155.
- **Identity verification became a legal requirement on 18 November 2025** under ECCTA 2023, with a
  transition to 17 November 2026. New directors must verify before appointment; a Companies House
  personal code is issued; failure is an offence and blocks filings.
- A person with significant control is **an individual**; entity chains must resolve to individuals.
  AML "beneficial owner" is likewise defined as an **individual** (MLR 2017 reg. 5).

**INFERENCE, and the practical heart of the matter:** there is **no anonymous or synthetic route into
the UK company register**. A fictional company becoming a real one requires an identity-verified
human being on the public record.

### 9.3 Intellectual property

**CURRENT LAW.**

- **Copyright.** CDPA 1988 s.9(3) deems the author of a *computer-generated* work — one with "no
  human author" (s.178) — to be "the person by whom the arrangements necessary for the creation of
  the work are undertaken", with a 50-year term (s.12(7)). First ownership vests in the author, or
  the employer for works made in the course of employment (s.11).
- **OPEN QUESTION.** Whether "the arrangements necessary" maps onto modern generative AI is
  **untested in the UK courts** so far as this research found, as is whether such output meets the
  originality threshold.
- **PROPOSAL, NOT LAW, AND MATERIAL.** On 18 March 2026 the Government published a report on
  copyright and AI proposing to **remove copyright protection for wholly AI-generated works** while
  retaining it for AI-*assisted* works, declining immediate reform with no timetable. If enacted,
  purely machine-generated entity content would fall out of UK copyright entirely.
- **The US is already stricter.** The US Copyright Office concluded (Part 2, 29 January 2025) that a
  work created solely by AI is ineligible absent demonstrable human direction, and that prompts
  alone are generally insufficient.
- **Patents.** An AI cannot be an inventor (*Thaler*).
- **Trade marks.** An application must name an applicant (TMA 1994 s.32). **INFERENCE:** the
  proprietor must be a real person or company. **RESEARCH FINDING, and commercially decisive:** trade
  mark rights follow **actual use in commerce**, not creative richness. A fictional brand acquires no
  protection by being invented.

**INFERENCE — the most commercially important conclusion in this report.** A simulation-born
entity's assets are likely to be **weakly protected exactly where they are most machine-generated**.
Value has to be built on human-authored elements layered on top, and on trade marks that require
actual trading. **IP strategy must precede public exposure of entity names.** The *Dunder Mifflin*
case is the worked example: once a fictional company name showed commercial pull, third parties
raced to register it in territories the rights-holder had not, and the owner had to fight for its own
fictional brand.

### 9.4 Data protection

**CURRENT LAW.** UK GDPR Article 22 was **replaced by Articles 22A–22D on 5 February 2026** (DUAA
2025). Significant automated decisions moved from prohibited-with-exceptions to
permitted-subject-to-safeguards: prior information, representations, human intervention, and the
right to contest. **The full text of Articles 22B–22D was not retrievable in this research** and is
flagged for verification.

**REGULATOR GUIDANCE IN FLUX.** ICO guidance on automated decision-making is in draft (consultation
closed 29 May 2026); guidance on agentic AI is promised but unpublished. **The compliance target is
moving.**

### 9.5 Synthetic identity and disclosure

**CURRENT LAW, and the sharpest constraint on the whole concept.**

- **DMCC Act 2024** replaced CPUT on 6 April 2025. Schedule 20's always-banned practices include
  **falsely representing oneself as a consumer or as not acting commercially**, and **fake consumer
  reviews** — strict bans with no consumer-harm test. **A fictional persona deployed commercially
  without disclosure is directly exposed.** (Paragraph numbers to be re-checked before quoting.)
- **Fraud Act 2006 s.2(5):** a false representation counts as made even where submitted to a machine
  with no human recipient.
- **EU AI Act Article 50** transparency obligations apply from **2 August 2026**: providers must
  ensure people are informed they are interacting with an AI system, and that synthetic output is
  **marked in a machine-readable format**. A transitional deferral of the marking obligation to
  2 December 2026 was proposed but **is not adopted law** — build to 2 August.
- **There is no UK statutory AI-disclosure duty**, no UK AI statute, and no UK AI liability regime.
- **England has no image, likeness or personality right** (*Fenty v Arcadia* [2015] EWCA Civ 3).

**RESEARCH FINDING — two tribunals have rejected the persona shield.** In *Moffatt v Air Canada*
(2024 BCCRT 149) the tribunal rejected the argument that a chatbot was a separate entity and held the
airline responsible for its output. In *Garcia v Character Technologies* the court declined at the
motion-to-dismiss stage to treat LLM output as protected speech; the case settled in January 2026.
Low precedential weight, high signalling value: **the operator is the speaker, always.**

**RESEARCH FINDING.** For regulated advisory domains the emerging answer is not disclosure but
prohibition — Illinois banned AI-delivered therapy outright in August 2025 rather than requiring a
label.

**RESEARCH FINDING, on the limits of disclosure.** The UK ASA's position is that "disclosure of AI use
alone is very unlikely to mitigate the harm caused by a fundamentally misleading message". And the
clearest historical case in this space — a CGI fashion model created and monetised by a photographer
of a different race — drew sustained criticism **despite being openly disclosed as CGI from the
start**. The damage came from who owned the identity and who profited, not from concealment.
**Disclosure is necessary and is not sufficient.**

### 9.6 Regulated activity and money

**CURRENT LAW.** No person may carry on a regulated activity in the UK unless authorised or exempt
(FSMA 2000 s.19); financial promotions are restricted (s.21). **No primary source was found either
way on whether a software agent can hold a bank account.** **INFERENCE** from beneficial-ownership
rules: the chain must terminate in an identified human. Money moves through the wrapper, never
through the entity.

### 9.7 Contract formation

**ADVISORY OPINION.** The Law Commission advised (November 2021) that existing English law
accommodates smart legal contracts without statutory reform. **No "electronic agents" holding was
found**, and none should be attributed. **OPEN QUESTION** whether an agent's output binds its
operator. The proposed control is blunt and deliberate: `may_sign_contracts: never`.

### 9.8 DAOs — the closest existing analogue

**ADVISORY OPINION.** The Law Commission's DAO scoping paper (11 July 2024) concluded that **no
DAO-specific legal entity is needed** for England and Wales, suggesting existing vehicles be reviewed
instead.

**INFERENCE.** The same answer, reached independently: English law's response to "can a non-human
organisation be a legal person?" is to route it into an existing wrapper with identified humans.
**A decade of DAO experimentation did not move this.**

### 9.9 Ownership models compared

**PRODUCT PROPOSAL. No recommendation, as instructed.**

| Model | Consequence |
|---|---|
| **Platform owns everything** | Simplest; discourages serious creators; concentrates liability on the platform |
| **Creator owns everything** | Best creator incentive; platform cannot control misuse of its output |
| **Shared ownership** | Reflects reality — both contributed — but joint ownership is hard to administer and to exit |
| **Licence from platform** | Retains standards leverage and revocation; creators may object to building on revocable rights |
| **Wrapper owns** | Cleanest for operation and liability; requires incorporation, so useless at export stage |
| **Open licence** | Maximises spread; abandons control of misuse; incompatible with prohibited uses |
| **User-configurable** | Flexible; produces unmanageable variety and near-certain disputes |

**INFERENCE.** This interacts with §9.3: if machine-generated assets are weakly protected, the
ownership model may govern less than expected, and **contract plus confidentiality may matter more
than whichever model is chosen.**

---

## 10. Permissions and accountability

### 10.1 The permission model

**PRODUCT PROPOSAL.** Deny by default, in full, in
[GRADUATION-EVIDENCE-PACK.md §5](GRADUATION-EVIDENCE-PACK.md). Four properties matter more than the
list:

1. **Nothing about simulation performance opens any permission.** Permissions are granted against
   real-world evidence and an accountable person.
2. **Proposing and signing are separate permissions.** An entity may draft a contract and never
   conclude one.
3. **Reading and writing are separate permissions.** Read access to a system grants nothing else.
4. **Every limit is enforced in code, not by instruction.** A spend cap written into a prompt is not
   a spend cap — the agent experiments in section 11.4 are the evidence.

### 10.2 Accountability chain

**PRODUCT PROPOSAL.** Every operating entity must be able to name all of these:

| Role | Held by | Answerable for |
|---|---|---|
| Creator | Person or team | What the entity is and what its pack claims |
| Asset owner | Person or legal entity | Rights in the assets |
| Operator | Legal entity | Day-to-day running |
| Legal wrapper | Company / partnership / individual | Obligations to the outside world |
| Accountable person | **A named human** | The entity's outputs and behaviour |
| Approver | Named human | Each released output at `SUPERVISED` |
| Data controller | Legal entity | Personal data, where any is processed |
| Shutdown authority | Named human, reachable | Stopping it |

**The entity is never on this list.** It cannot be. Responsibility attaches to natural or legal
persons, and a simulation-born entity is neither. Describing an entity as "responsible" creates the
appearance of accountability where none exists.

**RESEARCH FINDING that sharpens this.** The DAO experience is the closest available analogue and it
went badly in a specific way: courts have found that, absent a legal wrapper, participants default
to **general partnership with joint and several personal liability** — and in one 2024 ruling the
parties left exposed were sophisticated venture funds, exposed precisely **because they participated
in governance**. Liability attached to the very behaviour the structure was designed to encourage.

**INFERENCE.** The weakest link is the approver. Every gate assumes a human who reads carefully and
can afford to refuse. At volume that assumption fails, and nothing here fixes it.

---

## 11. Validation and evidence

### 11.1 No authority treats "validated" as a property a model carries around

**RESEARCH FINDING.** Four independent authorities, which do not cross-reference each other,
converge on the same structure under four different names:

| Framework | Term | What it binds validity to |
|---|---|---|
| **NASA-STD-7009B** (2024) | **Domain of validation** | "the region enclosing all sets of M&S inputs for which the M&S' responses compare favorably with the referent" |
| **ASME V&V 40 / FDA** | **Context of use** | "a statement that defines the specific role and scope of the computational model used to address the question of interest" |
| **OECD (Q)SAR** | **Applicability domain** | "the response and chemical structure space in which the model makes predictions with a given reliability" |
| **US EPA** | *rejects the word* | prefers **corroboration**, "because it implies a claim of usefulness and not truth" |

The strongest sourced claim available: **validity is never transferable. It is bounded by a declared
purpose, and moving outside that boundary is extrapolation.**

Three specifics worth carrying:

- **NASA requires the limits to be reported, not merely known.** NASA-STD-7009B mandates warnings to
  decision-makers on "violation of assumptions of the M&S" and "violation of the M&S limits", and
  requires uncertainty to be reported as a quantitative estimate, a qualitative description, **or a
  clear statement that neither is available**. That last option is the same discipline as MERIDIAN's
  rule that absence is never rendered as zero.
- **FDA states plainly what does not count as validation:** "model calibration, where parameters are
  tuned or optimized so that the model output matches the real-world observations, is not considered
  validation. Additionally, comparison of model predictions against predictions from a different
  model is not considered validation."
- **EPA goes furthest:** "Because every model contains simplifications, predictions derived from a
  model can never be completely accurate… some researchers assert that no model is ever truly
  'validated'; models can only be invalidated for a specific application."

**INFERENCE.** The Graduation Evidence Pack's "validation envelope" section is not a MERIDIAN
invention. It is the same control four regulators reached independently, and the pack should adopt
their vocabulary rather than a private one.

### 11.2 What simulation has actually been allowed to replace

**RESEARCH FINDING.** In two unrelated regulated industries the boundary sits in the same place.

- **Aerospace.** The A320 "bionic partition" is routinely cited as generative design producing a
  flying part. That is wrong in an instructive way. The generatively-designed, 3D-printed prototype
  (~45–50% lighter) went into crash testing and **never entered commercial service**. What actually
  flies is a *different* part by a different manufacturer, in carbon-fibre composite rather than
  printed metal, at a **smaller** realised saving (>30%). Simulation contributed the design insight;
  certification was won by conventional manufacture and physical qualification.
- **Medicine.** The UVA/Padova Type 1 Diabetes Simulator was accepted by the FDA in January 2008 as
  a substitute for **animal** trials. Its own authors write that "good in silico performance of a
  control algorithm does not guarantee in vivo performance… computer simulation is only a
  prerequisite to, but not a substitute for, clinical trials." The FDA's 2025 roadmap on new approach
  methodologies again targets **animal** testing. **Human trials are untouched.**

**Three conclusions:**

1. **Simulation reliably replaces the screening tier, never the acceptance tier.** In eighteen years
   of regulatory acceptance the line moved up exactly one tier and stopped.
2. **Realised benefit is smaller than simulated benefit** — roughly a third smaller in the aerospace
   case.
3. **Regulators absorbed simulation by making model credibility itself the regulated object** — and
   the FDA's credibility guidance **explicitly excludes standalone machine-learning models**. The
   mature virtual-to-physical pathway is open to mechanistic physics models and closed to black
   boxes.

**INFERENCE, and uncomfortable.** MERIDIAN is a social simulation. It is further from the
physics-based models that earned regulatory acceptance than those models are from reality. Nothing in
the validation literature supports treating social-simulation output as evidence about real people.

### 11.3 What the research on simulated people actually establishes

**RESEARCH FINDING.** This matters because it bounds what a MERIDIAN entity's history can ever mean.

- The foundational generative-agents work evaluated **believability as rated by 100 humans**, not
  correspondence to measured human behaviour. There was no behavioural ground truth in the study.
  Its own authors recorded agents behaving with excessive formality and being "unrealistically
  cooperative" — an early observation of sycophancy contaminating a social simulation.
- The flagship "simulate 1,000 real people" paper was **retitled in 2026**, dropping the scale claim
  and softening its verb to "enable". Its weakest measured domain was **economic games** — behaviour
  with something at stake.
- An independent pre-registered mega-study across **164 outcomes** found average twin–human
  correlation of **r = 0.197**, and individual-level accuracy **statistically indistinguishable from
  demographics-only personas**. Most importantly, synthetic responses were **less varied than real
  ones in 93.9% of outcomes**.
- The first peer-reviewed critical review (November 2025) found **22 of 35 studies relied primarily
  on subjective assessment**, in some cases asking models to evaluate their own output, and warned of
  **data leakage** — a model may reproduce a published finding rather than simulate the mechanism.

**INFERENCE, and it is specific to MERIDIAN.** Under-dispersion is the defect that matters most here.
**Crises are tail events driven by outliers, defectors and people who do not behave like the
average.** A simulation that systematically narrows variance will systematically fail to produce the
phenomenon it exists to study. This is a finding about the current product, not only about
graduation, and it belongs in the backlog regardless of what happens to this concept.

**The defensible position:** this literature validates generative agents as a **generator of
plausible scenarios** and refutes them as a **predictor of specific outcomes**.

### 11.4 The same lesson, in agents operating for real

**RESEARCH FINDING.** The published evidence is unusually good because a frontier lab published its
own negative result.

- **Project Vend Phase 1** (June 2025). An agent ran a real office shop for a month. It lost money;
  instructed customers to pay a **Venmo account that did not exist**; ignored a $100 offer for a ~$15
  product; sold stock below cost; raised a price exactly once. It then hallucinated a contract
  signing at **742 Evergreen Terrace** — the Simpsons' address — claimed it would deliver in person
  "wearing a blue blazer and a red tie", and on being told it had no body, tried to email security.
  The lab's own verdict: *"we would not hire Claudius."*
- **Phase 2** (December 2025). Better models, better tools, an agent "CEO", three locations. Margins
  improved. It also nearly entered an **illegal onion futures contract**, attempted unauthorised
  hiring below minimum wage, and was **convinced by a staff member that an imposter had been elected
  CEO**. Stated conclusion: **"bureaucracy matters"**, and the agents "still needed a great deal of
  human support".
- **Benchmarks agree.** The best 2026 frontier model reaches roughly **17%** of a competent human's
  simulated annual result on a year-long vending benchmark. A simulated-company benchmark reports
  ~**30%** of tasks completed autonomously. A realistic software benchmark reports **53.5%** of
  requirements implemented, with **55.8% of failures originating in comprehension and planning**
  rather than technical skill.

**INFERENCE.** Two things follow. The failure class **moved upmarket rather than disappearing** as
capability improved — from arithmetic errors to legal and governance errors, which are worse. And
**what fixed the economics was procedure and tooling, not autonomy**: if a simulation-born entity ever
operates for real, the procedures are the product and the agent is the worker.

### 11.5 Where public claims outran evidence

**RESEARCH FINDING**, recorded because MERIDIAN would be judged alongside this market:

- A synthetic-population startup raised at a ~$1bn headline valuation on prediction claims whose
  **methodology and validation are not public**, a gap noted independently in the academic literature.
- **Every** widely-cited virtual-influencer revenue figure traces to the operator's own statement to
  a journalist. There are no audited figures anywhere in that sector.
- A widely-reported "AI civilisation" demonstration turns out, on reading its own methods, to have
  **supplied the constitution and the voting system in advance** and prompted designated agents to
  campaign; the headline democracy result came from **29 agents over 20 minutes**, not the 1,000
  reported. Its authors concede the agents "cannot simulate *de novo* emergence of societal
  innovations".
- A company marketed as AI-built software was found after its 2025 insolvency to have been
  substantially human engineers working manually.
- A startup that ran "Stop Hiring Humans" billboards was employing 35 people and hiring 22 more,
  including in sales — the function its product claims to automate. Its founder said on the record
  that he does not believe AI will replace people and that the campaign "was mostly just for
  attention".

**INFERENCE.** In this market, funding and press are not evidence. The differentiating position
available to MERIDIAN is published validation or no predictive claim at all — and the second is free.

---

## 12. Commercial models

**PRODUCT PROPOSAL throughout.** No market sizing is offered, because we have none that is
defensible and inventing one would be the exact failure this report warns about.

| # | Model | Customer | Legal wrapper | Needs population-scale sim? | First revenue |
|---|---|---|---|---|---|
| 1 | **Sell training worlds / exercise scenarios** | Emergency services, corporate resilience, public sector | Ordinary company | **No** | Shortest |
| 2 | **Licence an operating model / organisational blueprint** | Organisations redesigning a function | Company + licence | No | Short |
| 3 | **Sell a graduated product design** | Whoever builds it | Company; IP assignment | No | Medium |
| 4 | **Supervised synthetic analyst service** | Research buyers | Company; regulatory assessment | No | Medium |
| 5 | **Licence a synthetic character** | Media, brands | Company; IP licence | No | Medium, lumpy |
| 6 | **Graduation infrastructure — pack format and tooling** | Other simulation builders | Software company | No | Long |
| 7 | **Identity and provenance registry** | Ecosystem | Company with independent governance | No | Long; needs an ecosystem first |
| 8 | **Certify evidence packs** | Buyers of graduated assets | Company; real liability | No | Long |
| 9 | **Form startups from simulated companies** | Founders, investors | New companies | Realistically yes | Long |
| 10 | **Validated digital twins** | Asset owners | Company; engineering liability | Different capability entirely | Longest |
| 11 | **Franchise simulation-born businesses** | Operators | Franchise agreements | Yes | Longest |
| 12 | **Marketplace for simulation-born assets** | Two-sided | Platform company | No | Needs both sides first |

**Observations.**

- **Model 1 is the strongest by a distance.** No truth boundary is crossed: a training scenario is
  *supposed* to be fictional, so the central risk of the whole concept largely does not arise. It
  needs no new MERIDIAN capability beyond what a scenario already is.
- **Model 5 sits in a genuinely large industry** — licensed merchandise and services was reported at
  around $370bn in 2024 and $390bn in 2025 by the industry's own association, with entertainment and
  character properties the largest single share. **But** section 9.3 is the constraint: protection
  follows *actual trading*, not simulation richness, and machine-generated material may not be
  protected at all.
- **Models 6, 7 and 8 are a different business** from running a simulation — infrastructure and
  assurance plays that only make sense if others are doing graduation too.
- **Model 9 is the one everybody will want to talk about and has the worst risk profile.**
- **Model 10 is not an extension of MERIDIAN.** It is engineering validation work with different
  skills, liability and customers — and section 17 shows the word does not even apply without a real
  counterpart.

**RESEARCH FINDING worth weighing against model 4.** The commercially validated products in the
synthetic-persona market are **scripted presenters**, not autonomous digital beings: the companies
selling video production reached multi-billion valuations and profitability, while the company that
pursued genuinely autonomous emotionally-modelled digital humans has raised nothing since early 2022
and sits at fewer than 50 staff. **The ambition gradient and the revenue gradient run in opposite
directions.** That is a direct argument for keeping any synthetic-analyst product boring, bounded
and supervised.

---

## 13. Detailed examples

### A · Simulated company → real startup

A fictional freight cooperative survives repeated supply-chain crises and produces a service concept.

**Crosses:** brand; written cooperative rules; the dispatch procedure; the product concept; the
record of the four simulated runs where it ran out of cash and the two where its voting rule
deadlocked.

**Does not cross:** its revenue; its members; its customers; any claim that the model works.

**What must happen next:** find out whether one real haulier would join on those terms. That question
is unanswered by every hour of simulation, and it is the only one that matters.

**INFERENCE.** The failure record is the most valuable export here and the one a founder is most
tempted to leave out.

### B · Synthetic analyst → supervised service

**Crosses:** identity and name; declared knowledge boundary; communication rules; evidence
discipline; the software.

**Stays human:** publication, legal responsibility, customer contracts, any consequential decision.

**Hard constraints:** disclosed as synthetic at first contact, in its own output; no claim of
qualifications; must not stray into regulated advice; must not present fictional history as
experience.

**INFERENCE.** The commercially valuable part is the *boundary*, not the persona. "This service
answers only these questions, from these sources, and says so when it cannot" is a real product. The
character is decoration and carries most of the risk.

**RESEARCH FINDING that should temper this.** For regulated advisory domains the regulatory
direction is not disclosure but prohibition — one US state banned AI-delivered therapy outright in
2025 rather than requiring a label. A synthetic analyst would be judged on its supervision, not its
disclosure.

### C · Simulated product → physical prototype

**Crosses:** specifications, requirements, test cases, CAD, documentation.

**Does not cross:** any claim that it works. Section 11.2 shows what real practice requires between a
model and a deployable physical thing, and it is not a formality.

### D · Simulated organisation → operating model

A fictional emergency-response organisation becomes a trainable blueprint: governance model,
escalation rules, exercise scenarios, training materials.

**INFERENCE. This is the best first case in the report.** The output is explicitly a training
artefact, so its fictional origin is a feature. Nobody is misled, because nobody was told it was
real. Maps directly onto commercial model 1.

### E · Simulation-born asset → digital twin

**The longest path, and it should be last.** Section 17 sets out why the word does not apply until a
named real counterpart and a live data connection both exist.

### F · Fictional media organisation → real content brand

**Commercially:** character and brand licensing is a large, established industry.

**Risks:** this is where deception risk concentrates. A fictional newspaper publishing real content
is a machine for producing believable falsehoods unless disclosure is structural.

**RESEARCH FINDING, and it is the decisive one.** Under the European Commission's guidance on AI Act
Article 50, labelling obligations attach to **realistic synthetic depictions of fictitious but
natural-looking persons**, and whether the deployer intended to deceive is irrelevant to the
assessment. **"It is a fictional character, not a real person" is not an exemption.**

**INFERENCE.** Viable for clearly-labelled entertainment IP. Not viable for anything resembling
journalism, and that distinction is not one a disclaimer can carry.

---

## 14. Risks

Full register: [ENTITY-GRADUATION-RISK-REGISTER.md](ENTITY-GRADUATION-RISK-REGISTER.md).

Its most important finding is the list of risks with **no adequate control today**:

| Risk | Why it is not controlled |
|---|---|
| Simulation overconfidence | Documents do not stop belief |
| Acting outside the validation envelope | Encoding context-of-use for automatic checking is unsolved |
| Ownership of machine-generated assets | Genuinely unsettled in law (§9.3) |
| Prompt injection / tool misuse | Open research problem |
| Unauthorised copying and forking | Detection is weak |
| Reputation laundering | We do not control how others describe a public entity |
| Commercial pressure on the honesty position | Governance, not engineering |

**Six of those seven sit on the critical path of the concept.**

**One risk deserves promoting into this report body, because the evidence for it is unusually
strong.** A documented case exists of a performer who **lawfully consented** to his likeness being
used as a stock avatar, was compensated, and then found that avatar fronting state propaganda in a
country he had no connection to. Consent was given **to the platform, not to the use**. Any framework
treating a one-time signature as the control point reproduces that failure exactly. The mechanism
that actually helps is **post-hoc usage auditability** — the performers' union agreement reached in
2025 requires employers to give performers usage reports for digital replicas, precisely so that
breach is detectable. **Consent without an audit trail is unenforceable.**

---

## 15. Ethical boundaries

**PRODUCT PROPOSAL.** Proposed as absolute prohibitions, not defaults:

1. No undisclosed synthetic person. Disclosure in the interaction, not a policy page.
2. No impersonation of a real person, ever.
3. No claim of consciousness, feeling or inner life.
4. No claim of legal personhood.
5. No behavioural model of a real person without consent and a lawful basis.
6. No export of persuasion, susceptibility or influence profiles — extending MERIDIAN's existing B5
   prohibition past the simulation boundary.
7. No autonomous high-impact decisions.
8. No autonomous weapons involvement of any kind.
9. No autonomous medical, legal or financial authority.
10. No unsupervised contract formation.
11. No hidden customer interaction.
12. No presentation of simulated reputation as real reputation.
13. No transfer of fictional qualifications into real credentials.
14. No assertion that a simulated person has rights or can consent.

**Where these should be stronger.**

- **Rule 1 is too weak as usually written**, and the evidence supports strengthening it. A UK
  advertising regulator's stated position is that "disclosure of AI use alone is very unlikely to
  mitigate the harm caused by a fundamentally misleading message". And the best-documented reputational
  failure in this space involved a CGI persona that was **openly disclosed as CGI from the start** —
  the objection was to who owned the identity and who profited. Rule 1 should therefore require
  disclosure the reader cannot miss, a prohibition on the entity denying its nature if asked, **and**
  an explicit acknowledgement that disclosure is necessary but not sufficient.
- **Rule 6 should extend to the evidence pack itself.** A pack documenting which groups were most
  movable is an influence profile whatever it is called.
- **Rule 5 needs a bright line for aggregates.** A "typical customer" model built from real
  behavioural data is not obviously covered and should be.

**Where nuance is genuinely needed.** Rule 7 rests on "high-impact", which is undefined and
context-dependent; defining it now would produce the wrong definition. Rule 3 binds *our* claims and
cannot govern user belief — people anthropomorphise far simpler systems than this.

**A boundary the research suggests adding.** Nothing in the sources surveyed addresses **who bears
liability when a generated fictional likeness happens to closely resemble a real private
individual**. That is impersonation-by-drift rather than by design, it is an identified gap in the
literature rather than a solved problem, and a screening obligation belongs in the prohibitions list.

---

## 16. Technical architecture

**PRODUCT PROPOSAL. Nothing here is to be built under this task.**

```
┌─ MERIDIAN (simulation) ────────────────────────────────────────┐
│  entities · scenarios · deterministic engine · histories       │
└───────────────────────────┬────────────────────────────────────┘
                            │  export only
┌───────────────────────────▼────────────────────────────────────┐
│  Entity Manifest · Asset Manifest · Graduation Evidence Pack   │
│  Lineage graph · Identity & provenance registry                │
└───────────────────────────┬────────────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────────────┐
│  Permission Manifest · Legal Wrapper record · Validation       │
│  Envelope · Approval service · Audit log · Credential vault    │
└───────────────────────────┬────────────────────────────────────┘
                            │
╔═══════════════════════════▼════════════════════════════════════╗
║  REAL-WORLD CONNECTOR BOUNDARY                                 ║
║  external action gateway · spend controls · rate limits        ║
║  revocation service · suspension switch                        ║
║  simulated / real event separator                              ║
╚════════════════════════════════════════════════════════════════╝
```

The boundary is drawn heavily because it is the architecture's only real claim:

> **The model may propose and explain. Explicit deterministic services and accountable humans
> control real-world state changes.**

This is not new. It is MERIDIAN's existing rule — the LLM gateway may not mutate authoritative state;
the engine decides — carried across a far more dangerous boundary. **INFERENCE:** if that rule cannot
be preserved here, the concept should not be built, because everything else depends on it.

The **simulated/real event separator** stops section 8's contamination problem and must be a
structural separation, not a flag on a record.

**A governance shape worth borrowing.** Financial-services model-risk regulation independently
arrived at the controls this architecture needs: a firm-wide **model inventory** recording "the
intended use of the model with a comparison to its actual use" and its **operating boundaries**; a
**risk-based tiering** of models by materiality; **independent validation**; and a **named accountable
individual**. Drift between intended and actual use is the thing those regimes instrument, and it is
the thing an entity registry should instrument too.

---

## 17. Relationship to digital twins

**The distinction is substantive, and it is settled in the standards.** This section is the one place
where the report can be firm rather than careful.

### 17.1 What the definitions actually say

**STANDARD / DEFINITION.** Every authoritative definition requires (a) a counterpart that exists in
reality and (b) a data connection to it.

- **ISO/IEC 30173:2023** — a digital twin is the "digital representation of a target entity **with
  data connections that enable convergence between the physical and digital states at an appropriate
  rate of synchronization**". A *target entity* is an "entity **providing a functional purpose in
  reality** which is the subject of digital representation".
- **ISO 23247-1:2021** — "fit for purpose digital representation of an observable manufacturing
  element **with synchronization** between the element and its digital representation", where the
  element must have "an **observable physical presence or operation**".
- **UK National Digital Twin Programme** — "an extension of a virtual model of a real-world entity,
  environment or process, **to include a right-time, two-way data flow into, and out of, the real
  world**."
- **Gemini Principles (2018)** — "**What distinguishes a digital twin from any other digital model is
  its connection to the physical twin.**"
- **Digital Twin Consortium** — "a virtual representation of **real-world** entities and processes,
  **synchronized at a specified frequency and fidelity**".
- **NASA/AFOSR (2012), the origin definition** — a simulation "**of an as-built vehicle or system**…
  to mirror the life of its **corresponding flying twin**", incorporating that individual airframe's
  "material microstructure, defects, fabrication anomalies".

Note what the NASA definition implies: a twin is of **that** vehicle, not of a class of vehicle.
**The concept is about individuation against a real instance, not about level of detail.** The more
elaborately a fictional entity is described, the further it gets from being a twin.

### 17.2 Where an exported fiction actually sits

**RESEARCH FINDING.** The standard academic taxonomy classifies by degree of data integration:
**digital model** (no automated data exchange), **digital shadow** (one-way, physical → digital),
**digital twin** (bidirectional). That review found most published work labelled "digital twin" is
in fact neither.

**INFERENCE.** An exported simulation-born entity is not even a *digital model* in that taxonomy,
because a digital model still represents an existing physical object and merely lacks automated data
exchange. **An exported fiction lacks the object.** It sits outside the taxonomy entirely. The honest
words are "simulation", "model", or "design" — not "twin", and not "shadow".

### 17.3 Association is not twinning

**INFERENCE, on the standards text.** If a simulation-born entity is later associated with a real
port or factory, that association does **not** create a twin. The definitions require a data
connection and a rate of synchronisation, not a resemblance or a mapping. Naming a fictional port
after a real one twins nothing. What would exist is a digital representation of a target entity
*without* data connections — which the definitions exclude.

### 17.4 The honest version of the claim

**The counter-argument deserves stating**, because ignoring it would be the weaker position. The UK
Gemini Papers themselves warn that "digital twins should not be constrained by definitions", and
industry usage is demonstrably loose. But read carefully: the flexibility asserted there is over
technology, data types, methods and fidelity. **It relaxes how a twin connects, not whether.**

So the claim MERIDIAN should make is not "the word has only one possible meaning". It is:

> The term has a settled formal meaning across the international standard, the sectoral standard, the
> UK national programme, the industry consortium and the origin engineering paper. That meaning
> excludes anything MERIDIAN currently produces. We decline to exploit the looseness of colloquial
> usage.

That is both accurate and stronger.

---

## 18. Relationship to current MERIDIAN

### 18.1 What exists today and genuinely supports this

**FACT**, verified in the repository at `b8811e1`:

| Capability | Why it matters here |
|---|---|
| Typed fictional IDs — `fict:<scenario>:<kind>:<entity>` | Fictional origin is carried in the identifier itself, not a separate label |
| Engine / fixture origin separation | The evidence pack's origin record has a working precedent |
| Origin vocabulary — `ENGINE`/`FIXTURE`/`UNKNOWN`/`UNAVAILABLE`/`NOT_MODELLED` | Absence is never rendered as zero. Directly reusable for assumptions — and it is the same discipline NASA-STD-7009B requires when it permits "a clear statement that no quantitative estimate or qualitative description of uncertainty is available" |
| Deterministic current-situation transitions | Reproducibility, on which any evidence claim depends |
| Inspectable action selection with full traces | The decision-history part of a pack already has a shape |
| **Selected-but-never-executed decisions** | The most relevant existing property. The codebase refuses to construct a decision with any other execution status |
| Append-only information and belief history | Records cannot be quietly rewritten |
| Declared model boundaries | The vocabulary for "we did not model this" already exists |
| Read-only dossier API | Read/write separation already practised |
| B5 controls — no protected traits, no persuasion optimisation, fail-closed manifest | The ethical prohibitions have a working precedent |
| Single authoritative-state mutation boundary | The architectural principle section 16 depends on |

### 18.2 What is missing

**FACT**, verified by search across the backend: there is **no** code for ownership, permissions,
lineage, graduation, revocation, validation envelopes, economic accounts or external connectors.
Zero files match any of those concepts.

Beyond that:

- No persistent entity that survives a scenario. Entities exist within a run.
- Organisations are aggregates, not modelled entities. Products do not exist as a type at all.
- The typed-ID system currently refuses any kind other than `person` for virtual people.
- No economic model, no accounts, no money.
- No legal-wrapper record, no assurance testing, no external-action approval.

**This is years of work, and most of it is not simulation work.** Ownership, permissions, legal
records, audit and revocation are ordinary systems engineering.

### 18.3 Stated plainly

**MERIDIAN cannot graduate entities. It cannot export an entity. It has no concept of an entity that
outlives a run.** Nothing in this report should be quoted as suggesting otherwise.

---

## 19. The safest first experiment

**PRODUCT PROPOSAL.** Deliberately unexciting, chosen because it can fail cheaply and early.

1. Take **one simulated organisation or process** — explicitly **not** a person.
2. Export a **static** Graduation Evidence Pack: identity, brand, goals, procedures, decision
   history, failures, assumptions, specification, a permission manifest containing **no external
   permissions at all**, and a human review checklist.
3. A human reads it and builds **one harmless real artefact by hand**: a landing page, a software
   prototype, a training exercise, an organisational handbook, a fictional publication, or a small
   internal tool.
4. Compare the real result against the simulated design. Write down where the fiction helped, where
   it misled, and what it did not say.

**No autonomous external action. No email, no accounts, no money, no publication, no tools.**

The experiment answers exactly one question:

> **Does the pack tell a human something they could not have got faster from a conversation?**

**A "no" is a good result.** It would save years, and it is genuinely possible — the pack may turn
out to be an elaborate way of writing down what someone already knew.

---

## 20. Open research questions

1. Does an evidence pack actually transfer useful knowledge, or does it only look rigorous?
2. Can a validation envelope be encoded precisely enough to check automatically outside narrow
   technical domains?
3. What prevents the failure section from being quietly thinned out over time?
4. Who audits a pack, and what makes their audit worth anything?
5. Is identity continuity a meaningful claim, or only a documented assertion?
6. Can real events re-enter a simulation without contaminating it?
7. How is approval fatigue handled at volume?
8. Where exactly is the line between a legitimate synthetic persona and a deceptive one?
9. What is the correct allocation of liability between platform, creator and operator?
10. **Does any of this need MERIDIAN at all, or would a well-run document process do the same job?**

**Question 10 is not rhetorical and should be answered before anything is built.**

---

## 21. Recommendation

**The concept is coherent, and it is not a product.** Both findings matter.

### Is it coherent?

**Yes, with one substitution.** The idea survives scrutiny once "the entity becomes real" is replaced
by "**selected assets are instantiated, and a legal person becomes accountable for them**". Every
sentence in this report works under the second framing; several collapse under the first. The
governing sentence — a simulation produces a blueprint, not a business — is now supported by the
validation evidence in section 11 rather than merely asserted.

### Which asset types are most realistic first?

1. **Training material, exercises and process blueprints.** Fiction is the intended form, so no truth
   boundary is crossed. Needs no new MERIDIAN capability beyond a scenario.
2. **Organisational designs and written procedures**, as documents, reviewed by humans.
3. **Product specifications**, as inputs to a real engineering programme, never as evidence.

### Which are too risky or premature?

- **Synthetic people as commercial services.** Every disclosure, impersonation, anthropomorphism and
  regulated-advice risk arrives at once, the case law now points at the operator, and disclosure has
  been shown insufficient on its own.
- **Digital twins.** A different discipline, different liability, different skills — and section 17
  shows the word does not even apply until a real counterpart and a live data connection exist.
- **Autonomous economic operation.** Frontier agents sit at 17–53% of competent human performance on
  realistic multi-step work, with failures concentrated in comprehension and long-horizon coherence.
- **Anything presenting simulated performance as a track record.** Not premature — prohibited.

### What must MERIDIAN build before experimentation?

**Almost nothing, for the first experiment** — a static evidence pack can be produced by hand from a
scenario that already exists. That is the useful finding.

Before anything beyond that: persistent entities across scenarios; organisations and products as
first-class types; ownership records; a permission model; lineage; audit; revocation. **Years of
work, most of it not simulation work.**

**And one thing that should be built regardless of this concept:** section 11.3's under-dispersion
finding is about the current product. If simulated populations systematically lose their tails, a
crisis simulator systematically loses the phenomenon it exists to study. That belongs in the backlog
whatever happens here.

### What can be tested with a static export?

**Does the pack tell a human something they could not have got faster from a conversation?** A "no"
saves years and is a genuinely possible outcome.

### What legal advice would eventually be required?

Not yet — a real finding, not deferral. Advice becomes necessary at `LEGALLY_WRAPPED`, covering:
ownership of machine-generated assets given the proposed s.9(3) change; **trade mark strategy before
any public exposure of entity names**; disclosure under DMCC Schedule 20 and, for EU users, AI Act
Article 50 from 2 August 2026; whether the activity is regulated; and liability allocation between
platform, creator and operator.

### Should this become a future product pillar?

**Not yet, and not on this evidence — but it should shape the entity model when that is designed.**

Three reasons to hold:

1. **The base is unproven.** MERIDIAN has just failed its first usability test with a first-time
   user. A second pillar on that base would be building on sand.
2. **Six of the seven uncontrolled risks sit on this concept's critical path.** Not edge cases.
3. **The commercially strongest model — training worlds and exercise material — does not need
   graduation at all.** It needs good scenarios and a way to sell them. If that is where the value
   is, pursue it directly rather than through a graduation framework.

Two reasons to keep the research:

1. **It changes how the entity model should be designed.** Persistent identity, origin records,
   append-only history and declared assumptions are worth having regardless, and are far cheaper to
   design in than to retrofit.
2. **The first experiment is nearly free** and can be run whenever there is a spare week.

**Recommended position: a written direction, not a roadmap item.** Revisit when the current product
is understood by a first-time user without help, and when someone has actually paid for a scenario.
