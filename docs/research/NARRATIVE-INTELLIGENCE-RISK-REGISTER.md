# Narrative and incentive intelligence — risk register

Part of the [Narrative and Incentive Intelligence](NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md) research
strand. **Research only. Nothing is implemented, so no risk here has been observed in this system.**
Derived use case: [Narrative Supply-Chain Analysis](../use-cases/NARRATIVE-SUPPLY-CHAIN-ANALYSIS.md).

These are reasoned risks with proposed controls, and the controls are untested. Residual uncertainty
is stated for each, because **several of these have no adequate control** and a register implying
otherwise would be dishonest.

**The register is deliberately front-loaded with the risks this concept creates for other people,
not the risks it creates for us.**

---

## A · Harm to real people and organisations

### A1 · Becoming a conspiracy generator
**Severity: critical. This is the defining risk of the concept.**

- **Cause.** The system maps ownership, funding and co-occurrence. Every such map contains
  connections. A reader — or a careless output — reads connection as coordination.
- **Consequence.** Real people accused, by implication, of organising something they did not
  organise. Reputational harm, legal exposure, and a product that produces exactly the epistemic
  damage it claims to counter.
- **Detection.** Review of every output for causal language unsupported by category-6 evidence.
- **Prevention.** The seven-category model in
  [OWNERSHIP-FUNDING-AND-INCENTIVES.md](OWNERSHIP-FUNDING-AND-INCENTIVES.md), never collapsed. No
  universal influence score. Permitted-language ladder. Human review before any output naming a real
  person.
- **Containment.** Withdraw, correct prominently, notify.
- **Accountable.** A named human reviewer, and the organisation publishing.
- **Residual uncertainty. HIGH.** We control our wording. We do not control the reader's inference,
  and a network diagram invites a causal reading no caption prevents.

### A2 · Naming an individual as a coordinated actor on inference alone
**Severity: critical.**

- **Cause.** Behavioural indicators are probabilistic. Communities, fans, activists, diaspora groups
  and newsrooms coordinate constantly and lawfully.
- **Consequence.** An ordinary person publicly characterised as a bot or an operative. This has
  happened repeatedly in this field with real harm.
- **Prevention.** **Prohibition:** no named individual is described as a participant in an influence
  operation without category-6 evidence and human sign-off. Bot-status claims prohibited outright.
- **Residual uncertainty. MEDIUM** with the prohibition, **HIGH** if it is ever relaxed under
  commercial pressure.

### A3 · Guilt by employer or association
- **Cause.** "Works for X, therefore promotes X's narrative."
- **Prevention.** Explicit prohibition. Employment is category 2 (financial dependence) at most, and
  category 2 licenses no claim about any individual's conduct.
- **Residual uncertainty. MEDIUM.**

### A4 · Defamation and malicious falsehood
- **Cause.** Publishing an inference about a named person or company that is untrue and damaging.
- **Consequence.** Litigation; for a small organisation, existential.
- **Prevention.** Human review; evidence attached to every assertion; clear separation of
  **public-record fact / model inference / allegation by a third party / finding by a competent
  authority**; no autonomous publication.
- **Accountable.** The publishing organisation, always. **The system is never the publisher.**
- **Residual uncertainty. MEDIUM-HIGH.** Legal exposure is real and is covered in the main report's
  legal section.

### A5 · Data protection — political opinions
**Severity: high, and structurally awkward.**

- **Cause.** Recording that a named person holds or promotes a political position may constitute
  processing of **special category data**.
- **Consequence.** Regulatory exposure; harm to individuals.
- **Prevention.** Avoid processing personal data about political opinions wherever the analysis can
  be done at organisational level. Where individuals are unavoidable, identify a lawful basis and an
  Article 9 condition **before** any processing, not after.
- **Residual uncertainty. HIGH** — see the legal section of the main report; the applicable
  conditions and the scope of the journalism exemption for a commercial research product are not
  settled.

### A6 · Harassment and doxxing amplification
- **Cause.** Publishing a network map naming individuals gives motivated readers a target list.
- **Prevention.** Prohibition on publishing personal identifiers; prefer organisational-level
  analysis; no aggregation of individuals' personal details even where each is individually public.
- **Residual uncertainty. HIGH.** Once published, distribution is not controllable.

---

## B · Being wrong in ways that look right

### B1 · Reproducing the dominant information environment
**Severity: high. This is the risk the founder identified, and it is the default outcome.**

- **Cause.** English-language and Western-institutional material is abundant; other material is not.
- **Consequence.** The system's picture of "what is known" is the Anglosphere's picture, presented as
  neutral analysis.
- **Detection.** Source-distribution reporting on every output.
- **Prevention.** Structural safeguards in
  [MULTILINGUAL-AND-REGIONAL-INFORMATION-BIAS.md](MULTILINGUAL-AND-REGIONAL-INFORMATION-BIAS.md);
  mandatory coverage-gap disclosure.
- **Residual uncertainty. HIGH.** Disclosure reveals the bias; it does not remove it. And the UK's
  unusually open ownership register means UK-heavy findings are an artefact of transparency law
  rather than a fact about the world.

### B2 · Inverse bias
- **Cause.** Over-correcting: treating non-Western or alternative sources as presumptively more
  honest.
- **Prevention.** Explicit rule that no source class carries a truth presumption in either direction.
- **Residual uncertainty. MEDIUM.**

### B3 · Absence read as suppression
- **Cause.** A "no PSC" filing, a missing contract notice, an unregistered lobbyist and a genuinely
  nil return are indistinguishable in the data.
- **Consequence.** Ordinary gaps presented as concealment.
- **Prevention.** Systematic distinction between **not required to disclose / required but did not /
  disclosed and genuinely nil**. Most published network analyses fail here.
- **Residual uncertainty. MEDIUM.**

### B4 · Entity-resolution error propagating
- **Cause.** UK registers share no identifiers. Every join is probabilistic.
- **Consequence.** A wrong merge creates a false central actor — and centrality is the finding most
  likely to be read as control.
- **Prevention.** Publish join method and confidence; human confirmation before any individual is
  named; treat resolution error as a quantified figure, not an assumption.
- **Residual uncertainty. HIGH.** This is a known-hard problem with no clean solution.

### B5 · Building on unverified registers
- **Cause.** Companies House, PSC, ROE and the Electoral Commission register are **self-declaration**
  systems. ECCTA 2023 verifies who is filing, not what they filed.
- **Consequence.** Confident output built on false inputs. **A confidently wrong register is worse
  than no register**, because it produces false negatives that look like findings.
- **Prevention.** Register data labelled as *declared*, never as *established*.
- **Residual uncertainty. HIGH.** We cannot verify what the registrar does not.

### B6 · Coordination detection false positives
- **Cause.** Legitimate communities coordinate. The published record on automation detection is
  poor: precision as low as 24–59%, recall 20–29%, and 27.2% of test accounts crossing the
  bot/human threshold within three months without changing.
- **Prevention.** Never claim automation. Claim observed behaviour. Publish indicator lists and
  thresholds. Version and expire detection methods.
- **Residual uncertainty. HIGH.** This is an adversarial, probabilistic problem and always will be.

### B7 · Overstating the effect of influence operations
- **Cause.** It is commercially attractive to imply that campaigns change minds at scale.
- **Consequence.** Customers make expensive decisions based on an overstated threat; the product
  becomes part of the problem it describes.
- **Prevention.** Report reach and structure, never assumed effect. Cite the sceptical literature
  where it exists.
- **Residual uncertainty. MEDIUM.**

---

## C · Adversarial and operational

### C1 · Detection methods becoming obsolete
- **Cause.** Once a method is known, operations route around it. This is the founder's point and it
  is correct.
- **Prevention.** **Versioned methods with expiry dates**, treated as temporary hypotheses;
  backtesting; documented false positives; adversarial testing.
- **Residual uncertainty. HIGH, permanently.** This does not converge.

### C2 · Being gamed
- **Cause.** If outputs matter, actors will optimise against them — manufacturing apparent
  independence, seeding decoys, or engineering a rival's profile.
- **Prevention.** Do not publish complete detection thresholds; keep a human in the loop.
- **Residual uncertainty. HIGH.**

### C3 · Data-source collapse
- **Cause.** Researcher access is contracting, not expanding: CrowdTangle shut down; EU public
  beneficial-ownership access struck down in 2022; the ClaimReview corpus lost its Search
  distribution; Aleph is introducing commercial tiers.
- **Consequence.** A pipeline built on today's access breaks.
- **Prevention.** Assume access is temporary; snapshot; prefer sources with legal durability.
- **Residual uncertainty. HIGH** and outside our control.

### C4 · Legal exposure from source material
- **Cause.** Some of the richest ownership data — Aleph in particular — includes **leaked
  databases**. Redistribution carries legal, data-protection and ethical exposure.
- **Prevention.** Verify licensing **per dataset, not per platform**. Legal review before any
  commercial use.
- **Residual uncertainty. MEDIUM-HIGH.**

---

## D · Risks to MERIDIAN itself

### D1 · The market is contracting, and for political reasons
**Severity: high, and it is the most important commercial finding in the strand.**

- **Evidence.** Logically — £30m raised, government and platform contracts — entered administration
  in July 2025 after Meta and TikTok withdrew from third-party fact-checking. Meta's coordinated-
  behaviour reporting moved from quarterly to semiannual and re-scoped toward scams. Google removed
  ClaimReview from Search. NewsGuard is litigating against the FTC and is barred from state
  contracts in Florida. Graphika has repositioned toward brand and fraud work.
- **Consequence.** Any business model depending on platform trust-and-safety budgets, or on being
  accepted as a neutral arbiter of truth, is exposed to a shock that has already happened to others.
- **INFERENCE.** The models that survived sell into **compliance, sanctions, supply-chain and
  fraud** — where demand is regulatory rather than discretionary. That is a strong argument against
  positioning MERIDIAN as a truth arbiter.
- **Residual uncertainty. HIGH** and outside our control.

### D2 · Becoming a target
- **Cause.** Analysis of powerful actors attracts legal, political and reputational pressure. The
  NewsGuard experience shows this is not theoretical.
- **Prevention.** Rigorous evidence discipline; legal review; insurance; a correction and appeal
  process **built before publication, not after the first complaint**.
- **Residual uncertainty. MEDIUM-HIGH.**

### D3 · Mission drift into surveillance
- **Cause.** The same capability that maps narratives maps people. Customers will ask.
- **Prevention.** Prohibitions treated as product constraints, not marketing copy: no persuadability
  scoring, no psychological profiling, no influence ranking for targeting, no covert collection.
- **Residual uncertainty. HIGH.** This is a governance and character risk, and no technical control
  addresses it.

### D4 · Contradicting MERIDIAN's own honesty position
- **Cause.** MERIDIAN's value rests on careful claims. This strand's outputs are inherently
  contestable and commercially rewarded for confidence.
- **Prevention.** The eight separated fields; no truth score; published error rates.
- **Residual uncertainty. HIGH.**

### D5 · Attention diverted from an unfinished product
- **Cause.** This is a more exciting idea than the current backlog. MERIDIAN has just failed its
  first usability test with a first-time user.
- **Residual uncertainty. MEDIUM**, and largely within the founder's control.

---

## Summary — the risks with no adequate control today

| Risk | Why it is not controlled |
|---|---|
| A1 conspiracy generation | We control our wording, not the reader's inference |
| A2/A6 harm to named individuals | Controlled only by a prohibition that commercial pressure will test |
| A5 political-opinion data | Legal position genuinely unsettled |
| B1 dominant-environment bias | Disclosure reveals bias; it does not remove it |
| B4 entity resolution | Known-hard, no clean solution |
| B5 unverified registers | We cannot verify what the registrar does not |
| B6 coordination false positives | Adversarial and probabilistic by nature |
| C1 method obsolescence | Does not converge, ever |
| C3 data-source collapse | Outside our control, and already happening |
| D1 contracting market | Outside our control, and already happened to others |

**Ten uncontrolled risks, and every one of them sits on the concept's critical path.** That is a
harder finding than the equivalent list in the simulation-born-entities strand, and it should weigh
heavily on any decision to proceed.
