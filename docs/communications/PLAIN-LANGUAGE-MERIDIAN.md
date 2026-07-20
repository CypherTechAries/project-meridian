# Plain-Language MERIDIAN — Message Bank

The approved public wording for every important MERIDIAN idea, with the evidence behind it and the
wording to avoid.

**The communication principle:**

> Show people the idea first, give them an example second, and show the technical evidence third.

The first paragraph creates understanding. The second creates trust. Reverse the order and a reader
who cannot follow the third paragraph never reaches the first.

## How to use this file

Copy the wording. Do not paraphrase it into something more impressive.

Every entry carries an implementation status. **Never promote wording to a public page before its
status is IMPLEMENTED**, which requires the work to be merged into `main` and passing hosted checks.

Statuses: `IMPLEMENTED` · `IN DEVELOPMENT` · `PLANNED` · `LONG-TERM VISION` · `NOT MODELLED`

## The writing test

Every public explanation must pass all six:

1. Could a ten-year-old explain the main idea after reading it?
2. Is there a concrete example?
3. Did ordinary words replace technical words wherever possible?
4. Is the statement supported by merged code and passing hosted tests?
5. Is missing capability clearly shown?
6. Can an engineer still reach the evidence?

Question 4 is the one that fails silently. A sentence can pass the first three beautifully and still
describe something that does not exist.

## The calibration example

This is the standard. Both versions are true; only one communicates.

**Too academic:**

> "A population average cannot tell you how many people agree, disagree or remain uncertain."

**Better:**

> "An average can hide what is really happening. A score of 5 out of 10 could mean everyone is
> unsure — or that half strongly agree and half strongly disagree. If MERIDIAN does not know which,
> it says so instead of guessing."

The second version is longer. That is fine. Length is not the enemy of clarity — abstraction is. The
improvement is not shorter words, it is a picture the reader can hold in their head.

## Word choices

**Avoid near the top of the README:** aggregate · denominator · provenance · contextual threshold ·
alignment · propensity · epistemic · distribution · state mass · divergence

**Prefer:** people · groups · what they saw · what they believed · what changed · why it changed ·
what the organisation said · what the system knows · what the system does not know

These words are not banned from the repository. They are precise and they belong in the design
documents. They simply must not be the first thing a visitor meets.

---

# The message bank

## 1. What MERIDIAN is

**Heading:** Simulated societies, built from first principles

**Explanation:** MERIDIAN is a small, careful model of a made-up society. Something goes wrong in it,
and MERIDIAN works out what happens next — to businesses, jobs, families, what people believe, and
what organisations decide to do.

**Example:** In the current story, ships can no longer pass through a narrow stretch of water called
the Kestral Strait. Everything that follows comes from that one event.

**Status:** IMPLEMENTED

**Evidence:** [`docs/delivery/P0-5-CAUSAL-SLICE.md`](../delivery/P0-5-CAUSAL-SLICE.md)

**Avoid:** "AI-powered", "predictive", "intelligence platform", "digital twin". None are true, and
each invites a reader to expect something MERIDIAN does not do.

## 2. One problem spreads through society

**Heading:** One problem spreads through society

**Explanation:** A problem in one part of society causes consequences somewhere else, and those
consequences arrive at different times.

**Example:** A blockade raises shipping costs. Carriers avoid the route. Port work falls. Families
become worried. Political pressure stays high even after shipping begins to recover.

**Status:** IMPLEMENTED

**Evidence:** Nine linked steps, each independently switchable ·
[`docs/delivery/P0-5-CAUSAL-SLICE.md`](../delivery/P0-5-CAUSAL-SLICE.md)

**Avoid:** "cascade", "second-order effects", "cross-tier propagation". Say what travels and where it
arrives.

## 3. Finding out which step mattered

**Heading:** You can find out which step actually mattered

**Explanation:** MERIDIAN can remove one step in the chain and re-run everything, so you can see what
that step was really carrying.

**Example:** Take out the rise in insurance costs, then check whether carriers still avoid the
strait, whether jobs are still affected, and whether political pressure still builds.

**Status:** IMPLEMENTED

**Evidence:** Baseline, incident and counterfactual runs; disabling one step leaves everything
upstream bit-identical · [`docs/delivery/P0-5-CAUSAL-SLICE.md`](../delivery/P0-5-CAUSAL-SLICE.md)

**Avoid:** "causal inference", "ablation study", "counterfactual analysis" as the *first* description.
"Remove one step and see what changes" is the same idea and everybody understands it.

## 4. Same claim, different reactions

**Heading:** People can see the same claim and react differently

**Explanation:** MERIDIAN records the reasons for those differences instead of assuming a person's
job, education or background decides the answer.

**Example:** The spokesperson already has first-hand testimony. The minister must follow a formal
verification process. The journalist's broadcaster requires more proof before treating the claim as
established.

**Status:** IMPLEMENTED

**Evidence:** Three people, one identical event; substituting one person's inputs for another's
reproduces the other's result exactly · [`docs/design/BELIEF-UPDATE-RULE.md`](../design/BELIEF-UPDATE-RULE.md)

**Avoid:** "models human psychology", "simulates cognition", "understands people". It is a bounded
first-order mechanism, not a mind. Also avoid implying the *job titles* cause the difference — the
declared reasons do.

## 5. Uncertainty is a real answer

**Heading:** Being unsure is a real answer

**Explanation:** MERIDIAN does not force everyone into "believes it" or "rejects it".

**Example:** The journalist moves slightly towards believing the claim but still does not have enough
confidence to treat it as established.

**Status:** IMPLEMENTED

**Evidence:** [`docs/design/BELIEF-UPDATE-RULE.md`](../design/BELIEF-UPDATE-RULE.md)

**Avoid:** "confidence interval", "posterior", "credence". The idea is *undecided*, and that word
already exists.

## 6. Silence is not rejection

**Heading:** Not hearing something is not the same as rejecting it

**Explanation:** Someone cannot respond to information they never received.

**Example:** Inland households never receive the new claim. Their earlier view stays the same;
MERIDIAN does not count them as having rejected it.

**Status:** IMPLEMENTED

**Evidence:** Exposure and belief are separate fields; an unexposed group keeps its earlier view and
records why · [`docs/design/BELIEF-UPDATE-RULE.md`](../design/BELIEF-UPDATE-RULE.md)

**Avoid:** treating "no data" and "no" as the same thing anywhere, in any wording. This is the most
consequential confusion on the list — it turns a silent group into a hostile one.

## 7. An organisation is not one mind

**Heading:** An organisation is not one mind

**Explanation:** MERIDIAN separates the views inside an organisation from the position the
institution officially presents.

**Example:** Half of the broadcaster is still undecided, so the broadcaster does not take a firm
public position.

**Status:** IMPLEMENTED

**Evidence:** Internal views and official position are separate results; the official position is
derived by a stated rule, not copied from an average ·
[`docs/design/BELIEF-UPDATE-RULE.md`](../design/BELIEF-UPDATE-RULE.md)

**Avoid:** saying the official position "disagrees with the average" as a general claim. Sometimes it
does and sometimes it does not — and an earlier version of this project got that wrong in public. Say
it *can* differ, and say why.

## 8. Direction and force are different

**Heading:** Supporting and opposing can both lead to strong action

**Explanation:** MERIDIAN separates which direction an organisation acts from how strongly it is
prepared to act.

**Example:** A government can strongly oppose a proposal just as actively as a workers' union
supports it.

**Status:** IMPLEMENTED

**Evidence:** Direction and force are separate results; a real bias favouring support was found and
corrected · [`docs/design/BELIEF-UPDATE-RULE.md`](../design/BELIEF-UPDATE-RULE.md)

**Avoid:** "action propensity", "alignment magnitude". Say direction and force.

## 9. Admitting what is not known

**Heading:** When MERIDIAN does not know something, it says so

**Explanation:** The engine does not fill missing information with convincing-looking guesses.

**Example:** MERIDIAN knows the average view of a population group, but it does not know how many
individual people agree, disagree or remain unsure. It marks that breakdown unavailable instead of
making one up.

**Extended version** — see the calibration example above.

**Status:** IMPLEMENTED

**Evidence:** Missing values never render as zero; unavailable results state why ·
[`docs/safety/B5-TECHNICAL-CONTROLS.md`](../safety/B5-TECHNICAL-CONTROLS.md)

**Avoid:** "handles uncertainty gracefully". That is a claim about tone. The claim here is specific:
it refuses to produce a number it cannot support.

## 10. Showing where a result came from

**Heading:** Every result can show where it came from

**Explanation:** A result can show which information was used, what changed and what stayed the same.

**Example:** The inland households' earlier opinion came from the fictional scenario. The engine
decided not to change it because they never received the new claim. The engine did not create the
original opinion.

**Status:** IMPLEMENTED

**Evidence:** Where a value came from and who decided not to change it are recorded separately ·
[`docs/safety/B5-TECHNICAL-CONTROLS.md`](../safety/B5-TECHNICAL-CONTROLS.md)

**Avoid:** "provenance", "audit trail", "lineage" in a first explanation. "Where it came from" is the
same idea.

## 11. Background does not decide the answer

**Heading:** Background does not secretly decide the answer

**Explanation:** Education, occupation and socioeconomic descriptions are kept outside the belief
calculation.

**Example:** Swapping the fictional people's education and background descriptions does not change
their calculated results.

**Status:** IMPLEMENTED

**Evidence:** Descriptive text is structurally separated from the calculation; a test swaps every
description and requires identical output ·
[`docs/safety/B5-TECHNICAL-CONTROLS.md`](../safety/B5-TECHNICAL-CONTROLS.md)

**Avoid:** any wording suggesting background predicts intelligence, competence, loyalty, morality or
how easily someone is influenced. The project rule: *a person's background changes the world they
experience, not the limits of who they can become.*

## 12. What is missing

**Heading:** What MERIDIAN does not do yet

**Explanation:** MERIDIAN does not model personal history, memories, relationships, changing trust,
personalised information feeds, cumulative stress, the order in which information arrives, random
life events, people who persist between runs, full individual breakdowns inside population groups, or
changes in opinion about whether something is right.

**Example:** MERIDIAN can currently explain why a fictional person changed their view in response to
one claim. It cannot yet explain how years of memories, relationships and earlier life events shaped
that person.

**Status:** NOT MODELLED

**Evidence:** [`docs/WHAT-MERIDIAN-CAN-DO.md`](../WHAT-MERIDIAN-CAN-DO.md)

**Avoid:** "not yet fully" and "currently limited" as softeners, and apologetic framing generally.
State the boundary plainly. An honest boundary is more useful than an impressive one, and readers
trust a project that draws one.

## 13. The fictional boundary

**Heading:** Everything here is invented

**Explanation:** Kestral Strait is a made-up place. The people, organisations and groups in it are
made up too. MERIDIAN describes no real country, company or person, and nothing it produces is a
forecast about the real world.

**Example:** There is no real Kestral Strait to look up. The map is drawn from scratch and uses no
real-world mapping data.

**Status:** IMPLEMENTED — enforced in code, not only in writing

**Evidence:** Eight technical controls ·
[`docs/safety/B5-TECHNICAL-CONTROLS.md`](../safety/B5-TECHNICAL-CONTROLS.md)

**Avoid:** "realistic", "true to life", "based on real events", and any real place name. Never soften
this disclosure to improve the pitch.
