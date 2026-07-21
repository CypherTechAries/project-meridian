# Entity graduation — risk register

**Status: RESEARCH AND PRODUCT PROPOSAL.** No entity has graduated, so no risk here has been
observed in this system. These are reasoned risks with proposed controls, and the controls are
untested. Residual uncertainty is stated for each because several of these risks have **no adequate
control**, and saying so is more useful than a table of green ticks.

Severity is judgement, not measurement.

---

## How to read this

Each risk gives: cause → consequence → detection → prevention → containment → accountable party →
residual uncertainty. Where the honest answer to "prevention" is *none that works*, it says so.

---

## A · Truth and evidence risks

### A1 · Simulation overconfidence
**Severity: high. This is the central risk of the entire concept.**

- **Cause.** A simulated entity performs well across many scenarios. People reason that it will
  perform well in reality. The reasoning feels sound and is not.
- **Consequence.** Real money, real jobs and real decisions committed on the strength of a fiction.
- **Detection.** Compare stated claims against the validation envelope. Look for any sentence about
  the entity that would still be spoken if the simulation had never run — if there are none, the
  claim rests entirely on fiction.
- **Prevention.** The evidence pack's "not shown to hold under" and "real-world tests still
  required" sections, written *before* graduation. Lifecycle gates that accept no simulated result
  as evidence.
- **Containment.** Demotion to `SUPERVISED`; public correction.
- **Accountable.** The accountable human at the wrapper.
- **Residual uncertainty. High.** Documents do not stop belief. A confident founder with a good
  deck will out-persuade a limitations appendix, and no control proposed here changes that.

### A2 · False claims of validation
- **Cause.** "Tested across 500 scenarios" said aloud in a sales conversation.
- **Consequence.** Misleading commercial practice; potential regulatory exposure; customer loss.
- **Detection.** Review of external material against the pack. Customer-facing claims audit.
- **Prevention.** A pre-agreed list of sentences that may and may not be said about a graduated
  entity. Prohibited-uses section.
- **Containment.** Withdraw and correct the material.
- **Accountable.** Whoever published.
- **Residual uncertainty. Medium.** Controllable in writing; hard to control in a meeting.

### A3 · Users believing fictional history occurred
- **Cause.** A detailed, internally consistent simulated history reads exactly like a real one.
- **Consequence.** A person forms beliefs about events that never happened.
- **Detection.** User comprehension testing — asking readers what they think they just read.
- **Prevention.** Non-removable fiction statement travelling with every artefact, not held on a
  separate page.
- **Containment.** Correction; re-labelling.
- **Accountable.** Platform.
- **Residual uncertainty. Medium-high.** Disclosure notices are reliably under-read.

### A4 · Entities acting outside their validation envelope
- **Cause.** An entity validated for one narrow context is asked a question just outside it. The
  boundary is invisible at the point of use.
- **Consequence.** Confident wrong answers, trusted because earlier answers were right.
- **Detection.** Input classification against the declared envelope; refusal logging.
- **Prevention.** Envelope encoded as a runtime check, not prose. Refuse-by-default outside it.
- **Containment.** Suspend.
- **Accountable.** Operator.
- **Residual uncertainty. High.** Encoding "context of use" precisely enough to check automatically
  is an unsolved problem for anything but narrow domains.

### A5 · Model drift
- **Cause.** Reality moves; the model does not. Or the software is updated and behaviour shifts.
- **Consequence.** Silent divergence, worst in a `TWINNED` entity where the model claims to describe
  a real thing.
- **Detection.** Scheduled comparison against real measurements; drift thresholds.
- **Prevention.** Mandatory re-validation cadence; automatic demotion on breach.
- **Containment.** Automatic demotion to `SUPERVISED`.
- **Accountable.** The engineer accountable for the correspondence claim.
- **Residual uncertainty. Medium** where real measurements exist, **high** where they do not.

---

## B · Identity and deception risks

### B1 · Undisclosed synthetic identity
**Severity: high.**

- **Cause.** A synthetic persona interacts with people who believe it is human — by omission as
  much as by design.
- **Consequence.** Deception; loss of trust; likely regulatory breach in several jurisdictions.
- **Detection.** Audit of every interaction surface for the disclosure.
- **Prevention.** Disclosure in the interaction itself, at first contact, in the entity's own
  output — not in a footer. Prohibition on any persona that denies being synthetic.
- **Containment.** Suspend; notify those affected.
- **Accountable.** Operator and wrapper.
- **Residual uncertainty. Medium.** Technically controllable; commercially tempting to weaken.

### B2 · Impersonation of a real person
**Severity: critical. Prohibit outright.**

- **Cause.** A persona built to resemble a real individual, deliberately or by drift.
- **Consequence.** Serious harm to that person; likely unlawful in multiple jurisdictions; possible
  criminal exposure.
- **Detection.** Similarity checks at creation; complaints channel.
- **Prevention.** Hard prohibition. Name and likeness screening. No real-person likeness without
  consent and a lawful basis.
- **Containment.** Immediate suspension and destruction of the persona assets.
- **Accountable.** Creator and platform.
- **Residual uncertainty. Medium.** Accidental resemblance is hard to screen at scale; deliberate
  misuse by a determined user is harder still.

### B3 · Reputation laundering
- **Cause.** A simulated reputation is presented as, or allowed to be mistaken for, a real one.
- **Consequence.** Unearned authority; a market where fictional track records compete with real ones.
- **Detection.** Monitoring how the entity is described by others, not only by us.
- **Prevention.** Prohibited-uses list; separation of simulated and real reputation in every
  display.
- **Containment.** Correction; withdrawal.
- **Accountable.** Platform.
- **Residual uncertainty. High.** Once an entity is public, we do not control how others describe it.

### B4 · Anthropomorphism and consciousness claims
- **Cause.** Rich, persistent, named entities invite it. Users do it unprompted; marketing does it
  deliberately.
- **Consequence.** Misplaced trust; emotional attachment; confusion about moral status.
- **Detection.** Language review; user research.
- **Prevention.** Prohibition on claims of consciousness, feeling, or legal personhood, in product
  copy and in the entity's own outputs.
- **Accountable.** Platform.
- **Residual uncertainty. High.** People anthropomorphise far simpler systems than this.

---

## C · Legal and commercial risks

### C1 · Unclear ownership of generated assets
- **Cause.** Authorship of purely machine-generated material is genuinely unsettled — see the legal
  section of the main report.
- **Consequence.** An asset that cannot be licensed, defended or sold with confidence.
- **Detection.** Rights status field per asset; anything `uncertain` flagged before graduation.
- **Prevention.** Record human authorship contemporaneously where it exists. Prefer human-authored
  assets for anything commercially load-bearing.
- **Containment.** Re-create the asset with documented human authorship.
- **Accountable.** Creator and platform.
- **Residual uncertainty. High.** This one is genuinely unresolved in law, not merely unresolved by us.

### C2 · Third-party IP inside exported assets
- **Cause.** Assets derived from material with its own rights holders.
- **Consequence.** Infringement claim.
- **Detection.** Input tracking in the manifest; similarity checks.
- **Prevention.** Record third-party inputs per asset; screen brand marks against existing marks.
- **Accountable.** Creator; wrapper on commercial use.
- **Residual uncertainty. Medium-high.** Inputs to generative processes are frequently untraceable.

### C3 · Unauthorised contract formation
- **Cause.** An entity's output is construed as an offer or acceptance.
- **Consequence.** Binding obligations nobody intended.
- **Detection.** Review of outbound communications.
- **Prevention.** `may_sign_contracts: never`. Explicit non-binding language on outputs. Human
  signature required for anything contractual.
- **Containment.** Repudiate quickly; take advice.
- **Accountable.** Wrapper.
- **Residual uncertainty. Medium.** Depends on facts and on how a court reads the exchange.

### C4 · Unauthorised spending
- **Cause.** A payment permission, a bug, or a manipulated instruction.
- **Consequence.** Financial loss; possible regulatory breach.
- **Detection.** Real-time spend monitoring; reconciliation.
- **Prevention.** Hard caps enforced in code and at the payment provider, not by instruction. Human
  approval above a low threshold. **Anthropic's own published vending-machine experiment is the
  instructive precedent here** — see the sources register.
- **Containment.** Freeze; reverse where possible.
- **Accountable.** Wrapper.
- **Residual uncertainty. Medium.**

### C5 · Regulated activity conducted without authorisation
- **Cause.** A "synthetic analyst" strays into regulated advice; a service becomes a regulated
  activity by accident.
- **Consequence.** Serious regulatory consequences.
- **Detection.** Scope review by someone qualified.
- **Prevention.** Assess before operation. Keep entities well clear of regulated perimeters.
- **Accountable.** Wrapper.
- **Residual uncertainty. Medium-high.** Perimeters are fact-specific and easy to cross unknowingly.

### C6 · Data protection breach
- **Cause.** Personal data read, retained or inferred without a lawful basis.
- **Consequence.** Regulatory action; harm to individuals.
- **Detection.** Data inventory; access logs.
- **Prevention.** No personal data below `REAL_DATA_READ_ONLY`. Named sources with a lawful basis
  recorded. Assessment where required.
- **Accountable.** The data controller — a real organisation, never the entity.
- **Residual uncertainty. Medium.**

### C7 · Liability gap
- **Cause.** Harm occurs and no one has clearly accepted responsibility.
- **Consequence.** Victim without remedy; dispute; reputational damage.
- **Detection.** Check every entity above state 5 has a named person and a written acceptance.
- **Prevention.** `LEGALLY_WRAPPED` gate before any operation. The entity is never the responsible
  party, because it cannot be.
- **Residual uncertainty. Medium.** Allocation between platform, creator and operator is untested.

---

## D · Technical and operational risks

### D1 · Prompt injection and tool misuse
- **Cause.** Hostile content in material the entity reads.
- **Consequence.** Actions or statements the operator never intended.
- **Detection.** Anomaly detection on actions; refusal logging.
- **Prevention.** Deny-by-default permissions; allow-listed tools; human approval for anything
  consequential; treat all ingested content as untrusted.
- **Containment.** Suspend.
- **Residual uncertainty. High.** This is an open research problem, not a solved one. Any design
  that assumes it is solved is wrong.

### D2 · Shutdown failure
- **Cause.** Untested kill switch; an action already in flight; a dependency that keeps running.
- **Consequence.** Cannot stop something that is causing harm.
- **Detection.** Scheduled shutdown drills with measured time-to-stop.
- **Prevention.** Test it. Record the measurement in the pack. An untested switch is a claim, not a
  control.
- **Residual uncertainty. Medium.** Reducible by drilling, which is easy to skip.

### D3 · Unauthorised copying or forking
- **Cause.** Pack and assets copied and run by someone else.
- **Consequence.** Uncontrolled instances; a fork misbehaving under a name associated with us.
- **Detection.** Registry checks; monitoring for the name in the wild.
- **Prevention.** Signing; licence terms; registry of authorised instances.
- **Residual uncertainty. High.** Copying is easy and detection is weak.

### D4 · Loss of audit history
- **Cause.** Retention lapse; migration; deletion.
- **Consequence.** Cannot reconstruct what happened or defend a decision.
- **Prevention.** Append-only storage; stated retention; backups. MERIDIAN's existing append-only
  history is the right pattern and would need to extend to real-world action logs.
- **Residual uncertainty. Low-medium.**

### D5 · Discrimination in outputs
- **Cause.** An entity's decision rules produce systematically different treatment.
- **Consequence.** Unlawful discrimination; harm.
- **Detection.** Outcome testing across groups.
- **Prevention.** MERIDIAN's existing B5 prohibition on protected traits and persuasion
  optimisation must extend to any graduated entity, not stop at the simulation boundary.
- **Residual uncertainty. Medium-high.** Proxies are hard to eliminate.

### D6 · Physical harm
- **Cause.** An entity influences a physical system.
- **Consequence.** Injury or damage.
- **Prevention.** Absolute prohibition at this stage. No physical-system permissions, at all.
- **Residual uncertainty. Low** while the prohibition holds; the risk is that it is relaxed.

---

## E · Risks the concept creates for MERIDIAN itself

### E1 · The honesty position becomes harder to hold
- **Cause.** MERIDIAN's value rests on being careful about what it claims. Graduation creates
  commercial pressure to claim more.
- **Consequence.** Erosion of the property that makes the product worth anything.
- **Prevention.** Treat the prohibited-claims list as a product constraint, not a legal formality.
- **Residual uncertainty. High.** This is a governance and character risk, not a technical one.

### E2 · Attention diverted from an unfinished product
- **Cause.** Graduation is a more exciting idea than the current backlog.
- **Consequence.** A speculative pillar built on an unvalidated base.
- **Prevention.** Keep this as research until the base is real.
- **Residual uncertainty. Medium**, and largely within the founder's control.

---

## Summary — the risks with no adequate control today

Stated plainly, because a register that implies everything is manageable would be dishonest:

| Risk | Why it is not controlled |
|---|---|
| A1 simulation overconfidence | Documents do not stop belief |
| A4 acting outside the envelope | Encoding context-of-use for automatic checking is unsolved |
| C1 ownership of generated assets | Genuinely unsettled in law |
| D1 prompt injection | Open research problem |
| D3 unauthorised copying | Detection is weak |
| B3 reputation laundering | We do not control how others describe a public entity |
| E1 pressure on the honesty position | Governance, not engineering |

Six of those seven sit on the critical path of the concept. That is the most important sentence in
this document.
