# The narrative supply chain

Part of the [Narrative and Incentive Intelligence](NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md) research
strand. **Research only. Nothing here is implemented.**

---

## 1. The idea in one picture

A claim is not a fact that appears. It is a thing that **travels**, and it changes as it goes.

```
event
  → witness or first source
    → institution
      → official statement
        → wire service
          → media outlet
            → commentator
              → platform
                → amplification (organised or organic)
                  → public response
                    → political or organisational action
                      ↺ which produces a new official claim, restarting the chain
```

The cycle at the bottom matters. A decision taken because of a claim generates a *new* claim — the
announcement of the decision — which re-enters the chain with more authority than the original had.
That is how a contested assertion becomes settled background.

**The single most useful thing this model produces** is not a verdict on truth. It is this sentence:

> *Fifteen outlets reported the claim. Fourteen trace back to one anonymous official briefing. That
> is broad repetition, not fourteen independent confirmations.*

---

## 2. Source independence

### 2.1 The problem

Four situations look identical in a headline count and are completely different as evidence:

| What you see | What it is |
|---|---|
| Ten sources | Ten independent observations |
| Ten sources | Ten outlets running **one** wire report |
| Ten sources | Ten outlets **citing each other** in a circle |
| Ten sources | Ten outlets **reacting** to one official statement |

Only the first is corroboration. The other three are repetition wearing corroboration's clothes.

### 2.2 Indicators of shared origin

**PRODUCT PROPOSAL.** Ordered from strongest to weakest evidence of dependence:

| Strength | Indicator |
|---|---|
| **Strong** | Identical factual **error** appearing in multiple outputs |
| **Strong** | Identical or near-identical wording beyond quoted material |
| **Strong** | Same identified originating document, wire report or press release |
| **Strong** | Same named single source or same anonymous descriptor ("a senior official") |
| Moderate | Identical quotation chain, in the same order, with the same ellipses |
| Moderate | Same image or video asset, same crop, same provenance |
| Moderate | Copied chronology, including the same starting point |
| Moderate | Shared owner or editorial group |
| Weak | Publication within a short window |
| Weak | Similar framing or emphasis |
| **Signal, not evidence** | Circular citation — A cites B, B cites A |

**INFERENCE.** The identical-error test is the strongest single indicator and the least gameable. Two
outlets can independently reach the same true statement; independently reproducing the same *mistake*
is very unlikely. It is the textual equivalent of matching fingerprints.

### 2.3 An independent source count that does not lie

**PRODUCT PROPOSAL.** A single number invites false confidence. The proposal is a **triple**, always
reported together and never collapsed:

```
17 reports · 3 independent origins identified · 6 unresolved
```

Rules:

- **Unresolved is never folded into either side.** A report whose origin could not be traced is not
  independent and is not dependent — it is unresolved, and saying so is the point.
- **The count is of *origins*, not outlets.** Two outlets sharing a wire are one origin.
- **Independence is a claim about what was traced, not about the world.** The honest phrasing is
  "3 independent origins **identified**", not "3 independent sources **exist**".
- **A count is never shown without the chain that produced it.** If a reader cannot open it and see
  which report mapped to which origin, the number is unfalsifiable and should not be displayed.

**OPEN QUESTION.** Where does one origin end? A press release quoting a study quoting a dataset is
how many origins — one, or three? Our current view is that the answer depends on what is being
claimed, which means the boundary is a judgement, which means a human has to make it. That is an
argument for the analyst-review requirement, not against the model.

---

## 3. Claim lineage

### 3.1 What actually changes as a claim moves

**RESEARCH FINDING and observation.** The transformations worth recording, because each is a
detectable, describable event rather than a vague drift:

| Transformation | Before | After |
|---|---|---|
| **Certainty inflation** | "may have been" | "was" |
| **Caveat loss** | "according to preliminary assessment" | *(removed)* |
| **Attribution drift** | "one official said" | "officials say" |
| **Source pluralisation** | one witness | "sources" |
| **Hedge removal** | "reportedly" | *(removed)* |
| **Emotional loading** | "an incident" | "an outrage" |
| **Modal shift** | possibility | fact |
| **Scale escalation** | "a local disruption" | "a geopolitical signal" |
| **Chronology compression** | a sequence over weeks | "immediately after" |
| **Context stripping** | with background | without |
| **Normalisation** | disputed | conventional wisdom |

**INFERENCE.** Certainty inflation and caveat loss are the two that matter most, because they are
the ones that happen **without anybody writing anything false**. Each step is defensible in
isolation. The cumulative effect is a claim that no source ever made.

### 3.2 The versioned lineage model

**PRODUCT PROPOSAL. Not a schema. Not to be implemented.**

Each version of a claim would preserve:

- **Original wording**, exactly.
- **Original language**, and — where translated — *which* translation, by what method, with
  alternatives preserved rather than resolved.
- Paraphrases, distinguished from quotations.
- Source, publication time, and the evidence actually supplied.
- **Certainty claimed by that source**, in that source's own words.
- **Delta from the parent version** — which of the transformations above occurred.
- Later corrections, attached to the version they correct.

Two properties are load-bearing:

- **Append-only.** A lineage that can be rewritten is not a lineage. MERIDIAN already has
  append-only histories for belief and information exposure; this is the same discipline applied to
  a different object.
- **Corrections attach, they do not replace.** A corrected claim keeps its uncorrected version
  visible, because the uncorrected version is what most readers saw.

**OPEN QUESTION.** How is a paraphrase distinguished from a new claim? At some point rewording
becomes a different assertion, and we have no principled boundary.

---

## 4. Omission and framing

### 4.1 Why this matters more than falsehood

A narrative is shaped more often by what is left out than by what is stated wrongly. Nothing false
need be published for a reader to be badly misled.

### 4.2 Signals worth recording

- Affected groups never quoted.
- One side's figures used consistently.
- Chronology beginning at a convenient point.
- Legal, historical or financial context absent.
- Uncertainty present in the source but absent in the report.
- Alternative explanations not mentioned.
- Corrections given less prominence than the original.
- A comparison period selected favourably.
- Local sources replaced by foreign summaries.

### 4.3 The rule that keeps this honest

> **Absence is not proof of suppression.**

Most omissions are ordinary: space, deadlines, ignorance, editorial judgement, nobody available to
comment. **PRODUCT PROPOSAL** — report omission in four graded forms and never beyond them:

| Form | Wording |
|---|---|
| **Expected but absent** | "Reporting on this event usually quotes X. None of the sources reviewed did." |
| **Coverage gap** | "No original-language reporting from the affected region was found." |
| **Unasked question** | "No source reviewed addressed X." |
| **Uncertain omission** | "X is absent. Whether it was considered and excluded cannot be determined." |

**INFERENCE.** "Expected but absent" requires a baseline of what is normally present, and that
baseline is itself a modelling choice that can encode our own assumptions. This is the weakest part
of the omission model and should be treated as unsolved rather than shipped confidently.

---

## 5. Separating things that must not be one number

**PRODUCT PROPOSAL, and the strongest single design commitment in this strand.**

These are different questions with different evidence, and combining them destroys all of them:

| Field | Question | Never |
|---|---|---|
| **Claim support** | What evidence supports this? | — |
| **Source independence** | How many origins were identified? | Not "how many outlets" |
| **Evidence quality** | Primary document, or a report of a report? | — |
| **Narrative reach** | How widely did it travel? | Not a proxy for truth |
| **Incentive alignment** | Who benefits if believed? | Not "who caused it" |
| **Coordination confidence** | How strong is the evidence of organised activity? | Usually "insufficient" |
| **Coverage diversity** | Which regions, languages, perspectives are represented? | — |
| **Unresolved alternatives** | What competing explanations remain live? | — |

> **There is no truth score, and there must never be one.**

**INFERENCE.** The commercial pressure to produce a single number will be immense — it is what
buyers ask for and what demos require. Resisting it is the product. A single score would make every
one of the eight fields unfalsifiable at once, and would put MERIDIAN in the position of the
ratings services now being litigated against and legislated against precisely for aggregating
judgement into a number.

---

## 6. Coordination — what may be said

**RESEARCH FINDING.** The evidence base for detecting *automation* is far weaker than the field
assumes; the detail is in
[COORDINATED-AMPLIFICATION-AND-BOT-METHODOLOGIES.md](COORDINATED-AMPLIFICATION-AND-BOT-METHODOLOGIES.md).
The short version:

Botometer — the tool underpinning most published "social bots are X% of discourse" literature — has
documented **precision as low as 24–59%** and **recall of 20–29%**, with **27.2% of test accounts
crossing the bot/human threshold within three months** without changing. It has had **no live data
since mid-2023**.

**PRODUCT PROPOSAL — the claim ladder.** Permitted language, in order:

1. "These accounts posted the same content within N minutes." *(observation)*
2. "This pattern is consistent with coordinated amplification." *(pattern)*
3. "Possible coordinated amplification, supported by the following indicators: …" *(bounded
   assessment, indicators listed)*
4. "There is direct evidence of organised activity: …" *(only with category-6 evidence)*

**Never permitted:**

- "These accounts are bots."
- "This is a Russian operation." *(without attribution evidence)*
- "This was coordinated." *(without category-6 evidence)*
- Any named individual described as a participant in an influence operation on inference alone.

**INFERENCE.** The honest pivot is from *automation* to *behaviour*: coordination detection makes
claims about what accounts did, which is observable, rather than about what they are, which is not.
That is the direction the serious practitioners already moved in, and it is a better claim structure
as well as a safer one.

---

## 7. What this model cannot do

- **It cannot establish truth.** Tracing a claim tells you where it came from, not whether it is
  right.
- **It cannot see private coordination.** Anything organised over a phone call is invisible.
- **It cannot distinguish suppression from absence.**
- **It cannot resolve competing accounts** where both are internally consistent and evidence is
  thin.
- **It inherits every bias of its sources** — see
  [MULTILINGUAL-AND-REGIONAL-INFORMATION-BIAS.md](MULTILINGUAL-AND-REGIONAL-INFORMATION-BIAS.md).
- **It cannot tell a legitimate community from a campaign** on behaviour alone. Fans, activists,
  diaspora communities and newsrooms coordinate constantly and lawfully.

That last one is not a footnote. It is the failure mode most likely to cause real harm to real
people, and no proposed indicator resolves it.
