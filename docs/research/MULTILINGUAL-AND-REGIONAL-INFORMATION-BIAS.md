# Multilingual and regional information bias

Part of the [Narrative and Incentive Intelligence](NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md) research
strand. **Research only. Nothing here is implemented, and no collection of any kind is proposed.**
Derived use case: [Narrative Supply-Chain Analysis](../use-cases/NARRATIVE-SUPPLY-CHAIN-ANALYSIS.md).

---

## 1. The problem, stated plainly

A system that reads mostly English-language material, mostly from the US and UK, will mistake:

- **the most repeated view** for the most accurate view;
- **Western institutional consensus** for universal consensus;
- **many articles copying one source** for independent corroboration;
- **official access** for reliability;
- **silence from under-represented regions** for absence of disagreement;
- **coordinated amplification** for organic public opinion;
- **search visibility** for importance.

Ten thousand posts are not ten thousand independent people. They may be one press release, one wire
report, one campaign, several organisations with one funder, or a crowd reacting to something an
algorithm promoted.

**This is not a hypothetical risk for MERIDIAN.** It is the default outcome of building anything on
the English-language internet, and it requires structural safeguards rather than good intentions.

---

## 2. Three ways the bias enters

**INFERENCE**, drawn from the sourced material in the companion documents.

### 2.1 Source availability

The data that exists is not evenly distributed, and the gaps are not random.

- **The UK's PSC register is fully public and free. Most of the EU's is not.** The CJEU struck down
  public access to beneficial ownership registers in November 2022; access is now "legitimate
  interest" only, per-request and per-entity — **you cannot map a network**. Roughly 39 of ~104
  jurisdictions with a live register have a **fully public** one.
- **Consequence:** any ownership analysis will be far richer for the UK than anywhere else, purely
  because of disclosure regimes. **A UK-heavy picture of global ownership is an artefact of UK
  transparency law, not a finding about the world.**

### 2.2 Coverage bias in the datasets

- **GDELT** — the largest open global news monitor — has documented false positives in event coding,
  and, more importantly, **it measures reporting, not reality**. Countries with restricted press
  freedom are systematically under-represented: *precisely the places where influence activity most
  needs detecting*.
- **Wikidata**, the practical backbone for entity resolution, has documented **systematic coverage
  bias** toward established, Western, male, notable entities; one study found **37.7% of deduplicated
  persons had no Wikidata link at all**.
- **Media Ownership Monitor** covers **34 countries**, donor-funded, with **Africa represented by
  two** and the US, UK, China and Russia absent. It is a snapshot, not a feed.
- **The Media Pluralism Monitor covers EU and candidate countries. The UK is not in the annual
  cycle post-Brexit**; the only recent full UK application is a 2023 bespoke report — nearly three
  years old.

### 2.3 The rating tools themselves

The consumer media-analysis tools are built on a **US left/centre/right axis**. That axis is not
neutral: its midpoint is definitionally the US political centre, which is a substantive position.
Applied outside the US it degrades badly, and applied to non-Western media it is close to
meaningless.

---

## 3. Proposed safeguards

**PRODUCT PROPOSAL throughout. None of this is built; several items may not be buildable.**

### 3.1 Structural, not additive

**The wrong fix is "add more foreign articles to the dataset."** That produces a single pool still
weighted by whatever is abundant, in which minority-language material is outvoted by volume.

Proposed instead:

| Safeguard | What it means |
|---|---|
| **Original-language retrieval** | Retrieve in the language published, not via an English summary |
| **Regional source maps** | Per-region source lists, not one global hierarchy |
| **Local vs foreign separation** | Reporting *from* a place is a different category from reporting *about* it, and they are never pooled |
| **Multiple independent translations** | Preserve disagreement between translations rather than resolving it |
| **Translation uncertainty preserved** | A translated claim carries a marker that it is translated, by what method |
| **Competing descriptions kept side by side** | Do not merge conflicting accounts into one summary |
| **Coverage-gap register** | Explicitly record which countries, languages and communities are poorly covered |
| **Source-distribution reporting** | Every output states where its evidence came from |
| **Media-type distinction** | State media, opposition media, commercial media and local reporting are different categories |
| **Diaspora handling** | Diaspora sources are neither local nor foreign; treat as their own category |
| **Regional expertise** | A human who understands the environment reviews before publication |

### 3.2 The output that makes the bias visible

The single most valuable safeguard is also the cheapest — **say what the evidence base was**:

> **Seventy-eight percent of the evidence used for this assessment comes from UK and US
> English-language sources. Original-language reporting from the affected region is limited.
> Confidence in the international framing should therefore remain constrained.**

**INFERENCE.** This is more honest than pretending the dataset is neutral, and it is achievable
without solving any of the hard problems. A system that could do *only* this would already be
unusual.

### 3.3 The rule that prevents inverse bias

> **Non-Western sources are not automatically more truthful. State media is not automatically
> false. Western media is not automatically reliable. Alternative media is not automatically
> independent.**

The goal is **balance and visibility, not inversion**. A system that treats a state broadcaster as
presumptively lying has simply adopted a different prejudice, and will be wrong in a different
direction — including in the many cases where a state broadcaster is the only organisation with a
reporter present.

---

## 4. Translation is not a solved problem

**INFERENCE**, and under-appreciated.

- **Machine translation flattens exactly what matters here** — hedging, register, idiom, and the
  distinction between reported speech and assertion. A hedge lost in translation is
  indistinguishable from certainty inflation introduced by a source, and the lineage model in
  [NARRATIVE-SUPPLY-CHAIN.md](NARRATIVE-SUPPLY-CHAIN.md) would attribute the change to the wrong
  step.
- **Sentiment and tone across languages is unreliable.** GDELT's tone measures are known to be
  distorted by machine-translation artefacts, which makes cross-language tone comparison unsound.
- **Retrieval itself is biased.** A query written in English retrieves what an English-trained
  embedding considers similar, which is not what a Farsi or Amharic speaker would consider relevant.

**Proposed discipline:** translation is recorded as a **transformation step in the lineage**, with
method and alternatives preserved — not applied silently as though it were neutral.

---

## 5. What good practice already exists

**RESEARCH FINDING.** Two examples worth learning from, both from the sources register.

- **EU DisinfoLab's "Indian Chronicles" investigation** traced a network of 750+ fake media outlets
  and resurrected defunct NGOs and dead academics. It is the closest published example of
  *ownership-and-front-organisation* analysis combined with narrative analysis. Note what it is:
  **hand-built investigative journalism**, not a queryable system. That is a finding about
  feasibility.
- **The Scottish lobbying register** averages 118 words of description where the UK register
  averages 11. Where a comparator exists, it demonstrates that opacity is usually a design choice.

**And one caution.** EU DisinfoLab does not disclose its own funders on its About page. For an
organisation whose subject is opaque funding of information actors, that is a notable gap — and a
useful reminder that **any organisation doing this work will be asked the same question about
itself, and should be able to answer it.**

---

## 6. Honest limitations of everything above

- **We have not tested any of it.** Every safeguard is reasoned, none is validated.
- **Original-language retrieval at scale is expensive** and probably the single largest cost driver
  in the whole concept.
- **Regional expert review does not scale**, and the design assumes it anyway.
- **The coverage-gap register requires knowing what you are missing**, which is partly
  self-referential.
- **"Expected but absent" needs a baseline** of normal coverage, and that baseline encodes our
  assumptions about what normal is — the same problem this document exists to solve, one level up.
- **A system that reports its own bias may still be trusted more than it deserves**, precisely
  because the disclosure signals rigour.

---

## 7. Open questions

1. What is the minimum viable multilingual capability — is there a useful version that works in
   three languages rather than thirty?
2. Can translation uncertainty be represented in a way a non-expert reader understands?
3. How is a coverage gap distinguished from genuine absence of reporting?
4. Who decides which sources belong in a regional source map, and how is that choice audited?
5. Is a bias disclosure that nobody reads worth anything?
6. Does building this at all require regional staff — and if so, is the concept viable for a small
   team?
