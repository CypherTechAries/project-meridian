# Coordinated amplification and bot methodologies

Part of the [Narrative and Incentive Intelligence](NARRATIVE-AND-INCENTIVE-INTELLIGENCE.md) research
strand. **Research only. No detection capability is implemented or proposed for implementation.**

---

## 1. Start with the finding that should govern the whole area

**RESEARCH FINDING.** Botometer — the tool underpinning the large majority of published "social bots
are X% of discourse" literature — has documented **precision as low as 24–59%** and **recall of
20–29%**. On German politicians' accounts, precision was **24%**: three quarters of accounts flagged
as bots were misclassified humans. **27.2% of test accounts crossed the bot/human threshold within
three months** without changing at all, which alone destroys the replicability of any prevalence
estimate built on it.

Systematic manual examination by other researchers found hundreds of accounts counted as social bots
were **operated by humans engaging in ordinary behaviour with no evidence of automation**.

It has had **no live data since mid-2023**, and its surviving archival model was trained before
generative AI was widely available.

**The structural reason it failed is worth understanding, because it generalises.** Researchers
cannot observe automation — platforms do not expose it — so they substitute proxies: high posting
volume, sparse profiles, new accounts, network position. **Those proxies also describe highly
engaged humans, activists, journalists, non-native speakers and shared institutional accounts.** The
method structurally over-counts exactly the populations most active in political discourse.

> **PRODUCT PROPOSAL: MERIDIAN must never claim an account is a bot.** Not as a default, not behind
> a confidence score, not at all.

---

## 2. Coordination detection is the honest alternative — and it inherits the problem

The field's better move was from *what an account is* (unobservable) to *what accounts did*
(observable). That is a genuinely better claim structure. It does not solve false positives; it
relocates them.

### 2.1 How it works

**RESEARCH FINDING.** The generic recipe: extract a **behavioural trace**, build an account × trace
network, project to account-account, filter to the strongest edges, cluster. Traces used in the
literature include shared account handles, shared images, identical hashtag sequences, co-retweeting,
co-sharing the same URL within an unusually short window, and synchronised timing.

**The filtering is a tuned dial, not a principled threshold.** Published work retains the top **1%**
or **0.5%** of edge weights. Coordinated-link-sharing work derives its time window *from the dataset
itself* rather than fixing it. There is no natural cut-point, which means **the analyst chooses the
false-positive rate** — and should say what they chose.

### 2.2 The false positives are not hypothetical — they dominated a real study

**RESEARCH FINDING, and the most important item in this document.**

A study of coordination in the **2019 UK general election** recovered seven coordinated communities.
Alongside the partisan amplification networks it surfaced **BackTo60** — pension-equalisation
campaigners — and a **loan-charge protest group**. Both are ordinary citizens campaigning lawfully.
They appear in the output because **that is what coordination looks like**.

The authors state plainly that they **"still cannot distinguish inauthentic coordinated behaviors
from authentic ones"**, and that automation and coordination are **orthogonal concepts**.

The originators of the general method give an equally useful warning: identical messages produced by
**news-site social share buttons** generate spurious coordination, and in two of three case studies
the majority of coordinated accounts scored as **human-like**, not automated.

**INFERENCE.** Fandoms, diaspora communities, unions, campaign volunteers, syndicated newsrooms and
grassroots movements will all appear in any coordination output. **This is the failure mode most
likely to harm real people, and no proposed indicator resolves it.**

### 2.3 Published coordination findings have already been shown to be artefacts

**RESEARCH FINDING, and it should temper any confidence in this method.**

A 2025 re-examination of published claims of **inter-state** coordination — different countries'
operations allegedly working together — applied current coordination indicators **plus control
datasets** and found **no evidence of inter-state coordination**. The authors attribute the earlier
positive findings to methods that failed to use state-of-the-art indicators **or control datasets**.

> **A coordination system without a baseline corpus will manufacture findings.** Synchrony looks
> remarkable until you measure how much synchrony occurs normally.

### 2.4 The case no on-platform method can catch

**RESEARCH FINDING.** Researchers who joined 600 political WhatsApp groups during an Indian election
documented **75 hashtag campaigns** distributed as mobilisation messages containing pre-written
tweets, often via shared documents. **Volunteers copy-pasted from their own real accounts at set
times**, producing hundreds of national trends.

Real accounts. Real people. Voluntary, sincere participation. Coordination organised **off-platform**
and therefore invisible to every API.

**And the commercial equivalent:** a 2024 US indictment alleged a media company was covertly funded
with roughly **$10m** by employees of a state broadcaster, paying prominent commentators — who say
they did not know — to produce content reaching millions. **Nothing in that operation is detectable
by coordination analysis**: no synchrony, no duplication, no automation, and the content was sincere.
It was exposed by **financial investigation and subpoena**.

**INFERENCE. A whole class of the most effective operations is out of scope for this method, and a
product must say so rather than let its silence imply coverage.**

### 2.5 Generative AI breaks the traces

**INFERENCE from the 2024–2026 literature.** Co-URL, identical-image and identical-hashtag-sequence
traces all assume **duplication**. Cheap paraphrase at scale removes exact duplication while
preserving the campaign, so detection is migrating to embedding similarity plus temporal synchrony —
**which raises the false-positive rate**, because semantic similarity is far more common among
genuine communities than byte-identical reposting. No source claims this trade-off is solved.

---

## 3. What may and may not be said

**PRODUCT PROPOSAL — the claim ladder, in permitted order:**

1. "These accounts posted the same content within N minutes." — *observation*
2. "This pattern is consistent with coordinated amplification." — *pattern*
3. "Possible coordinated amplification, supported by these indicators: …" — *bounded assessment*
4. "There is direct evidence of organised activity: …" — *only with documentary evidence*

**Never:**

- "These accounts are bots."
- "This is a [state] operation" without attribution evidence.
- "This was coordinated" on behavioural indicators alone.
- Any named individual described as a participant in an influence operation on inference alone.

The strongest published framing to copy is that coordinated link sharing is **"a signal to surface
sources of problematic information"** — a candidate-generation tool for human review, not a verdict.

---

## 4. Access to the data is closing

**RESEARCH FINDING / REGULATORY.** Any plan here depends on data that is becoming less available.

| Change | Effect |
|---|---|
| **CrowdTangle shut down 14 August 2024** | Its replacement has **no historical time-series data** — showing the platform only as it is at query time, destroying reproducibility and trend analysis. Not accessible to for-profit news organisations. Automated export not permitted. **The main coordinated-link-sharing toolchain is suspended as a result.** |
| **DSA Article 40 researcher access** — delegated act in force 29 October 2025 | Real, and a genuine opportunity — but scoped to **EU systemic risks**, VLOPs only, and requires vetting via a national coordinator with **independence from commercial interests**. **Structurally disfavours a commercial product.** |
| **DSA Transparency Database** | Billions of moderation records — but **contains no moderated content**, only reason codes; no API for its first year; data quality from one major platform called out as unreliable. |
| **X/Twitter** | Academic tier discontinued mid-2023; no replacement. Now the least accessible major platform for longitudinal work. |
| **TikTok Research API** | Independent testing found it **fails to return metadata for roughly 1 in 8 videos**, with no explanation — including TikTok's own corporate content. **The gap is non-random, so it is a bias, not noise.** |
| **EMFA Article 6** — applicable 8 August 2025 | The one thing moving the right way: EU media providers must publish ownership structure, beneficial owners and state-advertising funding, with national ownership databases. Implementation is uneven. |

**INFERENCE.** EMFA is more relevant to this concept than any detection API, because the mechanism
that matters most — narrative laundering — is a **provenance** problem, not a coordination problem.

---

## 5. Adaptive methods: how operations evolve past detection

**RESEARCH FINDING.** The founder's instinct that methods adapt once detection is known is correct
and documented.

- **Domain churn as architecture.** The best-documented cloning operation — pixel-level copies of at
  least 17 real media brands, seeding fabricated articles — survived a 2024 seizure of 32 domains
  and multiple sanctions designations. It is **architected so that takedown is a cost, not a kill**.
  A related operation reportedly created **200+ new fictional media websites since March 2025**.
- **Narrative laundering.** A claim is placed at an obscure origin, then layered through
  intermediaries that each strip provenance, until it reappears as independent commentary. By the
  final hop **there is no synchrony, no duplication, and no inauthenticity in the amplifier — the
  commentator sincerely believes it.**
- **Targeting the responder, not the audience.** One documented operation is named for flooding
  fact-checkers and journalists with fabricated material to exhaust defender capacity. **A high
  detection count can itself be the adversary's objective** — which means a dashboard that rewards
  volume is a dashboard the adversary can drive.
- **Recruiting the sincere.** Both §2.4 cases work by getting real people to genuinely agree.

**PRODUCT PROPOSAL — the principle that follows:**

> **Detection methods must be versioned, tested against known campaigns, and treated as temporary
> hypotheses with expiry dates.** Documented false positives, adversarial testing, regional
> validation, analyst review, and an explicit statement when a method version is retired and why.

The system should be able to say: *"Method version 2 overestimated coordination in this type of
community. Version 3 changed the timing threshold."* It must never present a past assessment as
though it was always right.

---

## 6. Effectiveness — the question the field under-reports

**This is the most important section for honesty, and the evidence is unusually consistent.**

**RESEARCH FINDING.**

- A *Nature Communications* study of exposure to the best-known 2016 foreign influence campaign
  found **no meaningful relationship between exposure and changes in attitudes, polarisation or
  voting behaviour**. Exposure was extraordinarily concentrated: **1% of users accounted for 70% of
  exposures**, and those users already strongly identified with the party the content favoured. The
  campaign was **eclipsed in volume by domestic news media and politicians**.
- A *PNAS* study linking a longitudinal panel to non-public platform data on the same operation
  found **no evidence of substantial effect on six measures** of political attitudes and behaviour.
- Untrustworthy sites made up **a small share of information diets**, with roughly **6 in 10 visits
  coming from the 10% with the most extreme information diets**.
- The widely-quoted figure that false news is about **0.15% of the average American's daily media
  diet** originates in a 2020 *Science Advances* paper — and is frequently misattributed.
- A 2024 *Nature* review argues the harms have been **mis-located**: exposure is rare and
  concentrated among a narrow, motivated fringe.

**And on the largest-scale operation ever run:** the platform that removed it reported that of
**53,177 channels disabled in one year, 58% had zero subscribers and 42% of videos had zero views**,
achieving **"practically no organic engagement from real viewers"**. On AI specifically, the same
source reported AI-generated video **"has not resulted in significantly higher engagement."**

**And from the model provider's side:** across 40+ disrupted operations, none exceeded the second
category of the breakout scale — multi-platform presence, **no breakout into authentic
communities** — and none showed a significant engagement increase attributable to AI. The stated
pattern is threat actors **"bolting AI onto old playbooks to move faster"**: a gain in production
cost and fluency, **not in reach**.

### 6.1 What this does *not* license

**Stated carefully, because the temptation to over-read it is strong.**

- It does **not** say influence operations are harmless. Belief in *specific* false claims does move.
- It does **not** measure second-order harms — erosion of trust in elections, chilling effects on
  journalists, defender-capacity exhaustion, or harm to targeted individuals.
- It is heavily US, Twitter and Facebook weighted, and largely pre-dates TikTok, Telegram and
  generative AI at scale.
- Null results on modest samples cannot exclude small effects, **and small effects can decide close
  elections**.
- The platform engagement figures come from **the platform that did the enforcement**, which has an
  obvious interest in reporting that what it removed had no audience.

### 6.2 The counter-case, included because omitting it would be selective

**INCIDENT / partially verified.** In December 2024, declassified intelligence alleged a highly
organised platform campaign supporting a Romanian presidential candidate who rose from around 5% to
23% in three weeks; a constitutional court **annulled the first round of a national election**.

**No ties to the alleged foreign sponsor have been established**, eighteen months on. The court
found no ballot fraud — the votes were real. Undeclared **domestic** paid promotion is at least as
consistent with the evidence.

**INFERENCE. This case cuts both ways and is the sharpest possible argument for caution.** It is the
strongest available example that coordinated online activity can precede a large political shift —
**and** an example of a state annulling an election on evidence that has still not been
substantiated. **The tooling's output became the justification.** Any product in this space should
sit with that before claiming confidence.

---

## 7. Three claims MERIDIAN must not make

**PRODUCT PROPOSAL**, drawn directly from the evidence above:

1. **"Coordination detection avoids the false-positive problem that killed bot detection."** It does
   not. It relocates it. The difference is that coordination detection is *honest about* its false
   positives.
2. **"AI has supercharged influence operations."** Every measurement found says AI improved
   **production economics and fluency**, not reach or engagement. Where AI plausibly changed things
   is in **fake-outlet manufacture at scale** — a provenance problem.
3. **"Scale indicates impact."** 53,177 channels, 58% with no subscribers. **Volume measures
   adversary spend, not adversary success. A dashboard that leads with volume will systematically
   mislead its user.**

---

## 8. Open questions

1. What baseline corpus would be needed before any synchrony finding is meaningful, and can one be
   assembled lawfully?
2. Can a coordination indicator be built that distinguishes a campaign from a community — or is that
   irreducibly a human judgement?
3. If the most effective operations are undetectable by these methods, what is the honest scope
   claim?
4. How is a method expiry date decided?
5. Given that detection volume can be an adversary objective, what metric should a product show
   instead?
6. Should MERIDIAN build any coordination detection at all, or restrict itself to claim lineage,
   source independence and ownership — where the evidence base is stronger and the harm potential
   lower?

**Question 6 is genuine.** Our current reading is that the answer may be no, and the main report's
recommendation reflects that.
