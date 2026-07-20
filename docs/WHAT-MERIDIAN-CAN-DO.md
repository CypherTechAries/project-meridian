# What MERIDIAN Can Do

A plain-English guide to what MERIDIAN can currently do, what it demonstrates, what it does not yet
do, and where you can inspect the technical evidence.

No background in simulation, artificial intelligence, statistics, behavioural science or software
engineering is needed to read this page.

> ### ◈ Everything here is invented
>
> Kestral Strait is a made-up place. The people, organisations and groups in it are made up too.
> MERIDIAN describes **no real country, company or person**, and nothing it produces is a forecast
> about the real world.

---

## In thirty seconds

MERIDIAN is a small, careful model of a made-up society.

Something goes wrong in that society — in the current story, ships can no longer pass through a
narrow stretch of water. MERIDIAN then works out what happens next: to businesses, to jobs, to
families, to what people believe, and to what governments and other organisations decide to do.

Two things make it unusual.

**It shows its working.** For every result, you can ask *where did this come from, what information
went into it, and what would have happened otherwise* — and get a real answer rather than a shrug.

**It admits what it does not know.** When MERIDIAN lacks the information to answer something, it says
so instead of producing a confident-looking guess.

---

## What works today

Every capability below is **IMPLEMENTED** — merged into the main branch and covered by tests that
run automatically on every change (384 for the engine, 64 for the interface).

### One problem spreads through society

A problem in one part of society causes consequences somewhere else, and those consequences arrive at
different times.

**Example.** A blockade raises shipping costs. Carriers avoid the route. Port work falls. Families
become worried. Political pressure stays high even after shipping begins to recover.

That last part matters most. The pressure on government is still near its worst *after* the original
problem has started to ease — because effects take time to travel, and they fade at different speeds.

**Status: IMPLEMENTED** ·
[The nine-step chain and how it was checked](delivery/P0-5-CAUSAL-SLICE.md)

### You can find out which step actually mattered

MERIDIAN can remove one step in the chain and re-run everything, so you can see what that step was
really carrying.

**Example.** Take out the rise in insurance costs, then check whether carriers still avoid the
strait, whether jobs are still affected, and whether political pressure still builds.

If everything downstream collapses when you remove a step, that step was doing real work. If nothing
changes, it was not. This is the difference between a genuine chain of cause and two things that
merely happened near each other.

**Status: IMPLEMENTED** ·
[Baseline, incident and counterfactual runs](delivery/P0-5-CAUSAL-SLICE.md)

### People can see the same claim and react differently

Three people hear exactly the same claim, from the same source, at the same moment — and end up
believing different things. MERIDIAN records the *reasons* for those differences, instead of assuming
that someone's job, education or background decides the answer.

**Example.** A family spokesperson already has first-hand testimony about what happened. A government
minister must follow a formal verification process before changing an official position. A
journalist's broadcaster requires more proof before treating the claim as established.

Three different reasons, three different results — and each reason is written down and checkable.

**Status: IMPLEMENTED** ·
[How belief change is worked out](design/BELIEF-UPDATE-RULE.md)

### Being unsure is a real answer

MERIDIAN does not force everyone into "believes it" or "rejects it". Sitting in the middle is a
result in its own right, and it is reported as one.

**Example.** The journalist moves slightly towards believing the claim, but still does not have
enough confidence to treat it as established. Not convinced, not dismissive — genuinely undecided,
and recorded that way.

**Status: IMPLEMENTED** ·
[How belief change is worked out](design/BELIEF-UPDATE-RULE.md)

### Not hearing something is not the same as rejecting it

Someone cannot respond to information they never received. These are two completely different
situations and MERIDIAN keeps them apart.

**Example.** Inland households never receive the new claim. Their earlier view stays exactly as it
was. MERIDIAN does not count them as having rejected the claim, and it does not quietly record them
as having no opinion.

This sounds obvious. It is very easy to get wrong, and getting it wrong makes a silent group look
like a hostile one.

**Status: IMPLEMENTED** ·
[How belief change is worked out](design/BELIEF-UPDATE-RULE.md)

### An organisation is not one mind

The views held *inside* an organisation and the position it presents *publicly* are two different
things. MERIDIAN keeps them separate.

**Example.** Half of the broadcaster is still undecided, so the broadcaster does not take a firm
public position — even though the people inside it who *have* made up their minds lean one way.

**Status: IMPLEMENTED** ·
[How belief change is worked out](design/BELIEF-UPDATE-RULE.md)

### Supporting and opposing can both lead to strong action

MERIDIAN keeps *which way* an organisation acts separate from *how strongly* it is prepared to act.

**Example.** A government can oppose a proposal just as forcefully as a workers' union supports it.
Opposition is not a weaker form of agreement.

This was a genuine mistake in an earlier version, where opposing something produced roughly a quarter
of the force of supporting the same thing for no good reason. It was found, reported and fixed.

**Status: IMPLEMENTED** ·
[How belief change is worked out](design/BELIEF-UPDATE-RULE.md)

### When MERIDIAN does not know something, it says so

The engine does not fill gaps with convincing-looking guesses.

**Example.** MERIDIAN knows the average view of a population group. It does **not** know how many
individual people within that group agree, disagree or remain unsure — because an average cannot tell
you that. So it marks the breakdown *unavailable* rather than inventing one.

An average can hide what is really happening. A score of 5 out of 10 could mean everyone is unsure —
or that half strongly agree and half strongly disagree. If MERIDIAN does not know which, it says so.

**Status: IMPLEMENTED** ·
[The eight safety controls](safety/B5-TECHNICAL-CONTROLS.md)

### Every result can show where it came from

You can ask any result which information was used, what changed, and what stayed the same.

**Example.** The inland households' earlier opinion came from the fictional story, not from the
engine. The engine decided not to change it, because they never received the new claim. Those are two
separate facts and MERIDIAN records them separately — *the engine choosing not to change a number is
not the same as the engine producing that number.*

**Status: IMPLEMENTED** ·
[The eight safety controls](safety/B5-TECHNICAL-CONTROLS.md)

### Background does not secretly decide the answer

Descriptions of education, occupation and social background are deliberately kept **outside** the
calculation. They exist to make the story readable, and they have no mathematical effect.

**Example.** Swap the fictional people's education and background descriptions around entirely. Every
calculated result stays identical, to the last decimal place. There is a test that does exactly this
and fails if anything moves.

This is a deliberate design rule, not an accident: a person's background changes the world they
experience, not the limits of who they can become.

**Status: IMPLEMENTED** ·
[The eight safety controls](safety/B5-TECHNICAL-CONTROLS.md)

---

## What MERIDIAN does not do yet

Everything below is genuinely absent. None of it is partly built.

MERIDIAN does not currently model:

- **years of personal history** — what happened to someone before the story starts;
- **memories** — nobody remembers anything from earlier in the run;
- **relationships** — no friendships, rivalries, families or working ties;
- **changing trust** — how much someone trusts a source is fixed and never moves;
- **personalised information feeds** — everyone hears the same thing the same way;
- **cumulative stress** — pressure does not build up over time;
- **the order in which information arrives** — hearing A then B is the same as B then A;
- **random life events** — nothing unexpected happens to anyone;
- **persistent people across runs** — a person exists for one run and is then gone;
- **full individual breakdowns inside population groups** — only group averages are known;
- **evaluative belief changes** — opinions about whether something is *right* do not yet update, only
  beliefs about whether something *happened*.

**A useful way to see the limit:**

> MERIDIAN can currently explain why a fictional person changed their view in response to one claim.
> It cannot yet explain how years of memories, relationships and earlier life events shaped that
> person.

The first is a mechanism. The second is a life. MERIDIAN has the first one.

Three further limits worth knowing: there is only **one** story available (Kestral Strait); nothing is
saved, so a run disappears when it finishes; and no language model is involved anywhere in producing
results.

---

## Explore the project

**See it running**

| | |
|---|---|
| [Briefing View](SCREENSHOTS.md) | The main screen — the situation in plain English |
| [Analysis View](SCREENSHOTS.md) | The machinery underneath: exact figures and where each one came from |
| [Run it yourself](../README.md#run-it-locally) | Setup instructions, about five minutes |

**Look under the bonnet**

| | |
|---|---|
| [How the system is built](../README.md#technical-architecture) | The technical architecture |
| [How belief change is worked out](design/BELIEF-UPDATE-RULE.md) | The rule, its limits, and what it deliberately does not claim |
| [The nine-step chain](delivery/P0-5-CAUSAL-SLICE.md) | How one problem reaches political consequence |
| [Safety controls](safety/B5-TECHNICAL-CONTROLS.md) | The eight boundaries enforced in code, not just in writing |
| [What may be claimed](delivery/CAPABILITY-CLAIMS.md) | The rules this project holds itself to when describing its own work |
| [Project log](delivery/PROJECT-LOG.md) | What was built, in order, including the mistakes |
| [Roadmap](../PROJECT-ROADMAP.md) | Where this is going |

**Tests.** The engine has 384 tests and the interface has 64. Both suites run automatically on every
proposed change, and no change can reach the main branch unless both pass.
