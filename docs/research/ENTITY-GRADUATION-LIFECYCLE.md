# Entity graduation lifecycle — states, transitions and approval gates

**Status: PRODUCT PROPOSAL.** Nothing in this document is implemented. No part of MERIDIAN today
has an entity lifecycle, a permission model, or any route to the outside world. This is a design for
discussion, not a description of software.

Companion documents: [SIMULATION-BORN-ENTITIES.md](SIMULATION-BORN-ENTITIES.md) (the main report),
[GRADUATION-EVIDENCE-PACK.md](GRADUATION-EVIDENCE-PACK.md) (what an export contains),
[ENTITY-GRADUATION-RISK-REGISTER.md](ENTITY-GRADUATION-RISK-REGISTER.md).

---

## 1. The one rule this lifecycle exists to enforce

> **Simulation success is not evidence of real-world fitness, and it never earns a permission.**

Every state below is reached by producing *new* evidence about the real world. No transition is
earned by anything that happened inside the simulation. A fictional company that survived forty
simulated crises has demonstrated exactly one thing: that it survived forty simulated crises.

A second rule follows from MERIDIAN's existing architecture and must survive into any real-world
work:

> **The model may propose and explain. Deterministic services and accountable humans decide.**

---

## 2. The states

Eleven states. Most entities should stop early, and stopping early is a success, not a failure.

| # | State | What it means | Can it touch the real world? |
|---|---|---|---|
| 0 | `SIMULATED` | Exists only inside MERIDIAN | No |
| 1 | `EXPORTABLE` | Has a complete, internally consistent evidence pack | No |
| 2 | `SANDBOXED` | Runs against synthetic data and fake tools | No |
| 3 | `REAL_DATA_READ_ONLY` | May read approved real information | Reads only |
| 4 | `SUPERVISED` | May draft outputs for a human to approve | Nothing leaves without a human |
| 5 | `LEGALLY_WRAPPED` | An accountable legal person exists and has accepted responsibility | Through the wrapper only |
| 6 | `LIMITED_OPERATION` | May take narrowly listed actions inside explicit limits | Yes, narrowly |
| 7 | `ECONOMICALLY_ACTIVE` | May provide services or receive money, through the wrapper | Yes, narrowly |
| 8 | `TWINNED` | Tied to one named real counterpart inside a declared validation envelope | Yes, and is now a claim about a real thing |
| 9 | `SUSPENDED` | All external permissions off; records intact | No |
| 10 | `RETIRED` | Permanently withdrawn; records preserved | No |

### Three things this ordering deliberately gets right

**`LEGALLY_WRAPPED` sits below `LIMITED_OPERATION`, not above it.** You cannot act in the world
before somebody is answerable for the acting. Every state from 6 upward requires 5.

**`TWINNED` is not the top of a ladder.** It is a *different kind of claim*, not a more advanced
one. States 0–7 concern an invented thing that now exists. State 8 concerns a model that asserts
something about a specific real object — a named port, a named factory. That is a claim that can be
wrong about reality in a way an invented brand cannot be. Most entities should never enter it.

**`SUSPENDED` is reachable from every state above 2, immediately, by a named human.** If suspension
requires a meeting, it is not a control.

---

## 3. Transition gates

Each gate lists what must be *produced*, not what must be *believed*. "The team is confident" is
not evidence.

### 0 → 1 · SIMULATED → EXPORTABLE

- Complete asset manifest: every exportable artefact listed, each with its origin.
- Every asset's origin resolves to a declared source. Nothing of unknown provenance.
- Declared assumptions and known failures written down *before* anyone reads the export.
- The entity's simulated history is versioned and immutable from this point.
- Explicit statement of what the simulation did **not** test.

*Gate holder: the entity's creator. Reviewer: a second person.*

### 1 → 2 · EXPORTABLE → SANDBOXED

- A permission manifest exists and is **empty of external permissions**.
- Every tool the entity can reach is a fake with no outside effect.
- All data is synthetic. No real personal data, at all.
- Logging captures every attempted action, including refused ones.

*Gate holder: engineering. Reviewer: whoever will hold the shutdown authority.*

### 2 → 3 · SANDBOXED → REAL_DATA_READ_ONLY

- Named, listed data sources. Not "public web".
- Lawful basis for each source identified and written down. If personal data is involved, this is
  where a data-protection assessment belongs — see the legal section of the main report.
- Hard technical guarantee that the read path cannot write. Not a policy: a guarantee.
- Prompt-injection handling stated, and its residual risk accepted in writing. A read-only agent
  that ingests hostile text can still be induced to produce harmful *output*.

*Gate holder: data owner. Reviewer: accountable human.*

### 3 → 4 · REAL_DATA_READ_ONLY → SUPERVISED

- Every output is drafted, queued, and released only by a named human.
- The human approving has the standing and the time to refuse. An approver who rubber-stamps at
  volume is a liability disguised as a control.
- Disclosure is attached to the output itself, not to a policy page.
- Approval and refusal are both logged, with reasons for refusal.

*Gate holder: accountable human. Reviewer: legal, if outputs go outside the organisation.*

### 4 → 5 · SUPERVISED → LEGALLY_WRAPPED

- A real legal person — a company, a partnership, an individual — exists and has **accepted in
  writing** that it is responsible for the entity's outputs.
- Ownership of each asset in the manifest is settled and recorded, including anything whose
  ownership is genuinely uncertain.
- Insurance position understood.
- A named natural person is accountable. Not a role, not a committee: a person.

*Gate holder: the legal wrapper's officers. This gate needs real professional advice.*

### 5 → 6 · LEGALLY_WRAPPED → LIMITED_OPERATION

- An allow-list of actions. Anything not listed is refused.
- Every limit is enforced by code, not by instruction: spend caps, rate limits, geography, time
  windows, recipient lists.
- A tested kill switch, with a named holder and a measured time-to-stop.
- Rehearsed incident response, including how an action already taken gets reversed or disclosed.

*Gate holder: accountable human. Reviewer: independent of the entity's creator.*

### 6 → 7 · LIMITED_OPERATION → ECONOMICALLY_ACTIVE

- Money moves through the wrapper's accounts, under the wrapper's identity checks. The entity is
  never the account holder.
- Whether the activity is regulated has been assessed by someone qualified to assess it.
- Customers are told what they are dealing with, before they pay.
- Tax and accounting treatment settled.

### 6/7 → 8 · → TWINNED

The hardest gate, and the one most likely to be waved through by wishful thinking.

- One named real counterpart. Not a class of thing.
- A written validation envelope: the conditions under which the model has been shown to correspond
  to that counterpart, and — equally — the conditions under which it has not.
- Real measurements from the real counterpart, compared against model output, with the comparison
  published internally.
- A stated update cadence and a defined drift threshold that triggers automatic return to `SUPERVISED`.
- Explicit prohibited uses: the questions this twin may not be asked.

*Gate holder: an engineer or domain specialist accountable for the correspondence claim.*

### Any → 9 · SUSPENDED

Immediate, unilateral, no quorum. Triggered by the named holder, by a drift breach, by a limit
breach, or by an unexplained action. Records are preserved exactly as they were.

### 9 → 10 · SUSPENDED → RETIRED

- Reason recorded.
- Records preserved for their stated retention period.
- Anything published externally is either withdrawn or annotated.
- Customers and counterparties told.

---

## 4. Reverse transitions

Downward movement must be cheaper and faster than upward movement. If demotion is hard, nobody
demotes.

- Any state → `SUSPENDED`: instant, one person, no review.
- `TWINNED` → `SUPERVISED`: automatic on drift breach. Not a judgement call.
- `ECONOMICALLY_ACTIVE` → `LIMITED_OPERATION`: on any financial irregularity.
- Re-promotion after demotion requires the *original* gate evidence again, refreshed. Not a note
  saying the problem was fixed.

---

## 5. Returning to simulation

**OPEN QUESTION**, and a genuinely hard one.

If an entity operates in reality and real events are fed back into MERIDIAN, the simulation stops
being clean fiction. Two failure modes:

1. **Contamination.** Real outcomes imported as simulation history make the simulated record look
   validated when it is a mixture.
2. **Laundering.** A real failure re-enters as a simulated event and is quietly rewritten.

A minimum discipline, if this is ever attempted: real events are stored in a **separate, clearly
marked stream** that can never be presented as simulation output, is never used to claim the
simulation predicted anything, and is visibly distinguishable in every view. MERIDIAN already has
the vocabulary for this — the `ENGINE` / `FIXTURE` / `UNKNOWN` origin separation — and would need a
new origin value rather than a reuse of an existing one.

Nothing here is settled. This section is a warning, not a design.

---

## 6. What must never be a gate

- Simulated revenue, popularity, customer demand or reputation.
- Number of simulated scenarios survived.
- Internal enthusiasm.
- A demonstration that impressed someone.
- The absence of a discovered problem. Not having found a failure is not evidence of safety.

---

## 7. Honest limitations of this proposal

- **Untested.** No entity has been through any of it. The gates are reasoned, not validated.
- **Approval fatigue is unsolved.** Every gate assumes a human who reads carefully. At volume, that
  assumption fails, and this design has no answer for it.
- **The twinning gate may be too weak.** Correspondence between a model and a real system is a
  research problem, not a checklist. The main report cites the standards work; a checklist is not a
  substitute for it.
- **Gate holders and reviewers overlap in a small team.** Independent review is stated as a
  requirement and would be difficult to honour with a handful of people.
- **State 8 may not belong in the same ladder at all.** It is included here for completeness, and
  the main report argues it is a different kind of claim.
