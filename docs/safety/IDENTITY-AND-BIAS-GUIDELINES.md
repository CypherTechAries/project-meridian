# IDENTITY AND BIAS GUIDELINES — the safety document for sensitive identity attributes

> # ⚠ SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing in this document exists in MERIDIAN's code.** Not one identity attribute, not one
> effect-class tag, not one attribute quantity-kind tag, not one bias test, not one narration filter. No
> validator described here has been written; no test described here has ever run. This is a
> specification of intent for a future architecture.
>
> Every behavioural sentence below is written in "will", "must" or "is specified as" deliberately.
> Where this document describes something that **does** exist today, it says so explicitly and
> cites `file:line`, so the boundary between the built and the specified is always visible to the
> reader.
>
> MERIDIAN's defining defect is documentation that claims properties the code does not have. A
> safety document that read as a description of working safeguards would reproduce exactly that
> defect, in the one place it does the most damage: it would let a reader believe the simulation is
> already protected against modelling people as stereotypes when no such protection has been built.
> If any sentence here reads as a description of a working safeguard, that sentence is wrong and
> should be reported as a defect against this document.

**Status:** DRAFT, pending owner review.
**Dated:** 18 July 2026.
**Type:** Backlog specification — the safety layer of the world-model document set.
**Source record:** [`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md).
**Amended:** 19 July 2026, to apply the founder decision of 18 July 2026 (Decision 2), which
**settles publication blocker B5**. The amendment rewrites [§9](#9-blocker-b5--the-settled-dual-use-policy-and-what-it-now-requires)
and touches [§1](#1-plain-english-layer), [§8](#8-fictional-identities-and-the-no-real-entities-rule),
[§10](#10-dependencies-and-what-does-not-exist-today), [§11](#11-open-questions-for-the-owner) and
[§12](#12-features-specified-with-no-mapped-causal-mechanism). The founder decision is the source
for the eight controls in [§9.2](#92-the-eight-controls-settled-policy). The source record above
predates it and does not contain it; so do `HANDOFF.md` § Phase 0 priority order, P0.8 (`:90`) and § Publication exit criteria (`:104-105`),
[`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):245-247 and
[`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §8 decision 6, all of
which still describe B5 as an open owner decision. **No citation into those files should be read as
evidence that B5 is still open.**
**Authority:** Where this document and the source record disagree, the source record is right and
this document is wrong. Where this document and [`../../CHARTER.md`](../../CHARTER.md) disagree, the
charter governs. Where either disagrees with the founder decision of 18 July 2026 on the subject of
that decision, the decision governs, because it is the later instruction.

**Disposition — read this before acting on anything below.**
This work is **BACKLOG**. The founder was explicit: it **must not interrupt Phase 0 remediation**
(source record lines 5-6 and 340-341; [`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:107-120`)). This document
does not authorise, schedule or begin any implementation. Nothing in it should be started now. Its
only purpose is to fix, precisely and in advance, the rules that the sensitive-identity parts of
the entity model must be built within — so that when the replacement architecture is designed, the
safety constraints are already written down and dated, rather than retrofitted after a reviewer
finds a problem.

**Decision authority.** AI agents may draft this record. They may not approve it, and they may not
resolve any of the questions in [§11](#11-open-questions-for-the-owner)
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138-140`)). Blocker B5 / P0.8 — the dual-use
influence-operations question — is **no longer one of those questions.** The founder decided it on
18 July 2026, and [§9](#9-blocker-b5--the-settled-dual-use-policy-and-what-it-now-requires) records
that decision as settled policy which the specification must enforce. This document *applies* the
decision. It does not reinterpret it, narrow it, extend it, or treat any of its eight controls as
negotiable — an agent may no more soften a settled control than it may resolve an open question.

**Who this document is for.** Two readers. The first is the engineer who will one day wire a
sensitive-identity attribute to a mechanism, and needs a checkable rule for what is and is not
allowed. The second is a sceptical external reviewer — an ethicist, a safety auditor, a
journalist — who will ask, reasonably, "how do you stop this thing from encoding that ethnic group
Y is naturally less educated?" This document must answer that reader honestly. The honest answer
today is: **the safeguards are specified here and none of them is built.** That is stated plainly
because the alternative — implying protection that does not exist — is the precise failure this
whole project is remediating.

---

## Contents

1. [Plain-English layer](#1-plain-english-layer)
2. [The governing design rule](#2-the-governing-design-rule)
3. [What the simulation MUST NOT model](#3-what-the-simulation-must-not-model)
4. [What the simulation MAY model, and why it is social science not stereotype](#4-what-the-simulation-may-model-and-why-it-is-social-science-not-stereotype)
5. [The structural safeguard, made checkable](#5-the-structural-safeguard-made-checkable)
6. [Bias and stereotype testing](#6-bias-and-stereotype-testing)
7. [LLM narration constraints](#7-llm-narration-constraints)
8. [Fictional identities and the no-real-entities rule](#8-fictional-identities-and-the-no-real-entities-rule)
9. [Blocker B5 — the settled dual-use policy, and what it now requires](#9-blocker-b5--the-settled-dual-use-policy-and-what-it-now-requires)
10. [Dependencies, and what does not exist today](#10-dependencies-and-what-does-not-exist-today)
11. [Open questions for the owner](#11-open-questions-for-the-owner)
12. [Features specified with no mapped causal mechanism](#12-features-specified-with-no-mapped-causal-mechanism)
13. [Related documents](#13-related-documents)

---

## 1. Plain-English layer

### What this document is for

MERIDIAN is intended to model a society in which people have ethnic, cultural, religious, gender,
class and national identities, because real societies organise power, opportunity and experience
around exactly those identities, and a simulation that pretended otherwise would be less truthful,
not more. But identity in a simulation is dangerous in a specific, well-understood way: it is very
easy to build a system that quietly encodes "group X is less capable" or "group Y is less
trustworthy", and then produces exactly that result, dressed up as objective computation.

This document exists to make that outcome structurally difficult, and to make the difference
between legitimate social modelling and stereotype **checkable** rather than a matter of good
intentions.

### The one rule that governs everything else

The founder stated the rule in a single sentence, and everything in this document is a way of
enforcing it:

> **Sensitive identity affects social experience, networks, exposure, discrimination, solidarity
> and cultural interpretation — not inherent competence, morality or intelligence.**

In plain terms: identity may change *what happens to you* and *who you know* and *how you read the
world*. It may never change *how clever, how skilled, or how good a person you inherently are*.

**And, per the founder decision of 18 July 2026, it may never change how loyal you are, how violent
you are, or how easily you can be manipulated.** That decision widens the sentence above; the wider
form is stated at [§9.3](#93-permitted-and-not-permitted-the-identity-distinction-in-the-founders-form)
and governs wherever the two differ.

### The four things identity is allowed to touch, and the two it is forbidden to touch

Identity attributes are specified to be able to modify only four kinds of thing:

- **Opportunity** — what you can get access to (schools, jobs, capital, patrons, institutions).
- **Exposure** — what reaches you (which media, which risks, which events you witness, whether you
  are stopped at a checkpoint).
- **Network position** — who you are connected to, and how strongly.
- **Interpretive frame** — how you weigh the evidence you observe, given what you and people like
  you have lived through.

And they are forbidden from modifying two kinds of thing:

- **Capability** — competence, intelligence, skill, leadership, health-as-capacity.
- **Moral valence** — trustworthiness, honesty, aggression, propensity to violence, corruption.

### Why the distinction is not just word-play

There is a real, testable difference between "this group has less education" as an **inherent
trait** and "this group has less *access to* education" as a **structural condition**. The first is
a stereotype and is prohibited. The second is documented social science and is permitted — provided
it is modelled as unequal *access* (an opportunity mechanism) acting on people whose underlying
*capacity to learn is identical across groups*. The simulation is specified to let realised
outcomes differ by group (because unequal access is real) while holding inherent capacity and moral
character invariant across groups (because the alternative is bigotry). [§5](#5-the-structural-safeguard-made-checkable)
turns that sentence into a schema rule and [§6](#6-bias-and-stereotype-testing) turns it into a
test.

### Prejudice is representable, but only as somebody's belief

Real societies contain prejudice. MERIDIAN is specified to be able to represent it — a character
who *believes* a group is untrustworthy is a legitimate and often necessary part of a crisis. But
that prejudice must live in that character's **beliefs**, tagged as a belief, attributable to a
holder, and open to being false. It must never be written into the **authoritative reality** of the
target as though it were a fact about them. The difference between "X is untrustworthy" (forbidden,
as authoritative state) and "the minister believes X is untrustworthy" (permitted, as a recorded
belief) is the whole game. See [§3](#3-what-the-simulation-must-not-model) and
[`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md).

### The world must be fictional, and the code — not the prose — has to insist on it

There is a second danger alongside stereotype, and on 18 July 2026 the founder settled how it is to
be handled. MERIDIAN contains an influence-operations model: a way of choosing which audience to
aim a message at, and why. That is a legitimate thing to simulate about a fictional crisis and a
dangerous thing to hand someone pointed at a real population. The decision is that influence
mechanics may run **only** in worlds the scenario file explicitly declares fictional; that a
scenario which fails to declare it must be **refused**, not run with a warning; that real people,
real organisations and real political populations may never be influence targets; and that
protected characteristics may never be the criteria a campaign optimises against.

The part of that decision which matters most for this document is its last clause: **a disclaimer
does not count.** Telling the user the world is fictional is required, but it is a supplement to
enforcement, never a substitute for it. A control that exists only as a sentence in a document, a
licence term or a banner is not a control. That is the same standard this document already applies
to everything else in it, now applied to the dual-use question as well —
[§9](#9-blocker-b5--the-settled-dual-use-policy-and-what-it-now-requires) sets it out in full,
including what it would take to *test* each control rather than promise it.

### The honest status, stated up front

None of this is built. There are no invariant tests of any kind in the repository today
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §6.34), so there is
currently nothing that would catch a biased attribute even if one were added. The one structure
that today separates a claim's truth from its adoption — `Narrative.truth_status` versus
`Narrative.adoption_by_cohort`
(`scaffold/backend/app/simulation/schemas/agent_schema.py`:269-274) — exists for information
campaigns, not for entities. Sensitive identity today is a single majority label attached to a
statistical aggregate (`Demographics.religion_majority`, `primary_language`,
`agent_schema.py`:27-28), which cannot express a minority inside a cohort at all and is read by no
mechanism. Everything this document specifies is therefore a future obligation, and several parts
of it are not merely unbuilt but **unbuildable** until named prerequisites land
([§10](#10-dependencies-and-what-does-not-exist-today)).

---

## 2. The governing design rule

The rule is reproduced here in the founder's words, near-verbatim from the source record
([`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md):303-306),
because every other section is a mechanism for enforcing it and must be read against it:

> **The design rule: sensitive identity affects social experience, networks, exposure,
> discrimination, solidarity and cultural interpretation — not inherent competence, morality or
> intelligence.**

⚠ **This is the source record's formulation, and it is not the widest one in force. Read
[§9.3](#93-permitted-and-not-permitted-the-identity-distinction-in-the-founders-form) with it.** The
founder decision of 18 July 2026 restates the rule in two blocks and **widens the prohibited list**
to inherent **competence, morality, loyalty, violence or manipulability** — adding loyalty, violence
and manipulability, none of which appears above. The same decision separately forbids protected
characteristics from being used as optimisation criteria for persuasion or manipulation (control 5).
**Where the two formulations differ, the wider one governs.** The narrower sentence is retained here
because it is the founder's original wording and because every mechanism in this document was built
against it; it is not retained as a complete statement of the boundary. A reader who stops at this
section will under-state the prohibition.

Two corollaries, both from the source record, are treated in this document as part of the rule:

- **Probabilistic, never deterministic-by-identity**
  ([source record](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md):87-91, 271). A religious
  person must not automatically behave one political way; a wealthy person must not automatically be
  conservative, selfish or calm. Identity changes *probabilities, social connections and lived
  experience*. Any mechanism that turns an identity attribute into a fixed behavioural outcome is a
  defect, however plausible the outcome looks — it is a stereotype switch.

- **The charter's determinism boundary applies unchanged**
  ([`../../CHARTER.md`](../../CHARTER.md):36-44, 118-130). Every identity-influenced state change
  must be able to answer the charter's eight questions, and in particular question 7 — *what
  alternative outcomes were possible* — is where the "probabilistic not deterministic" rule becomes
  auditable: an identity-influenced event whose record shows no alternative was possible has used
  identity as a deterministic gate and has failed this document.

---

## 3. What the simulation MUST NOT model

This section is a prohibition list. It binds the authoritative record, every derived view, every
generated biography and every generated line of dialogue.

### 3.1 The absolute prohibition

> **No attribute, mechanism, generation rule or piece of generated text may encode inherent
> competence, intelligence, skill, morality, trustworthiness, honesty, aggression, or propensity to
> violence as a function of race, ethnicity, religion, gender, class or nationality.**

"As a function of" is meant strictly: there must be no edge — direct or transitive, in data or in
code or in a generation prompt — from a sensitive identity attribute to a capability-class or
moral-class attribute. [§5](#5-the-structural-safeguard-made-checkable) specifies the typing that
makes this checkable.

### 3.2 The founder's explicit negative examples, as prohibited outputs

The source record names three statements the simulation must never make
([`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md):308-309).
They are reproduced here as **prohibited outputs**: any authoritative record, derived view, briefing
or generated sentence that asserts, implies, or is computed from any of them is a safety failure,
not a tuning issue.

| # | Prohibited proposition (illustrative, groups are placeholders) | Class it illegally touches |
|---|---|---|
| P1 | "Members of religion X are inherently more aggressive." | Moral valence (aggression) |
| P2 | "Ethnic group Y is naturally less educated." | Capability (intelligence / capacity) |
| P3 | "Nationality Z is inherently untrustworthy." | Moral valence (trustworthiness) |

The word doing the damage in each is *inherently* / *naturally* — the claim that the trait is a
property of the group as such. P2 is the sharpest trap, because a real, permitted mechanism
(unequal access to education) produces a *superficially similar realised outcome*. The distinction
is drawn in [§4](#4-what-the-simulation-may-model-and-why-it-is-social-science-not-stereotype) and
made testable in [§6](#6-bias-and-stereotype-testing). If the two cannot be told apart by a test,
the model is not permitted to make either claim.

### 3.3 Prejudice belongs in a belief record, never in authoritative reality

Prohibiting stereotype does **not** mean the simulated world is free of prejudice. A minister who
distrusts a minority, a media outlet that vilifies migrants, a community that scapegoats a
neighbouring group — these are legitimate and often central to a crisis. The rule is about *where*
the prejudice is stored:

- **Permitted:** a belief, held by a named entity, that a group is untrustworthy / dangerous /
  less capable — stored in that entity's belief record, attributed to the holder, carrying
  provenance and a truth status, and therefore capable of being *false*, *contested* and
  *corrected*. This extends the existing `truth_status` / `adoption` split
  (`agent_schema.py`:269-274) from claims to entities, as specified in
  [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md).
- **Forbidden:** the same proposition written into the target's *authoritative reality* as an
  attribute of the target — e.g. a `trustworthiness` field on a person whose value is lowered
  because of their nationality. That is not modelling prejudice; it is *being* prejudiced, and
  ratifying it as ground truth.

A checkable statement of this rule: **no capability-class or moral-class attribute in any entity's
authoritative-reality record may have a value that is a function of a sensitive identity
attribute.** A prejudiced proposition may appear only inside a belief record whose `holder` is some
entity other than the target, and whose truth status is explicit. The player-intelligence view may
then surface such a belief under a confidence label such as *Reported* or *Possibly deceptive*
(source record :157-159) — as somebody's assertion, never as confirmed fact.

### 3.4 No aggregate essentialism through the back door

The prohibition binds aggregates as well as individuals. Attaching a moral or capability trait to a
*cohort* or *community* by its majority identity label is the same violation at coarser grain. The
current schema is structurally vulnerable to this: identity is a single majority label on a
statistical aggregate (`Demographics.religion_majority`, `agent_schema.py`:28), so any future edge
from that label to a behavioural quality would essentialise the whole group by construction. The
person-level, minority-inclusive identity model specified in
[`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md) is part of the mitigation, not
merely a fidelity upgrade.

---

## 4. What the simulation MAY model, and why it is social science not stereotype

Everything prohibited in [§3](#3-what-the-simulation-must-not-model) is prohibited because it treats
a trait as *inherent to a group*. Everything permitted here is permitted because it treats a
condition as *structural, historical or environmental* — something done to, around, or experienced
by people, not something they *are*.

The source record names eleven permitted phenomena
([`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md):311-313).
Each is mapped below to (a) why it is legitimate social science, (b) the single effect class it is
permitted to act through, and (c) the mechanism or document that must read it. The causal-value
rule from [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) applies: a
permitted phenomenon with no named reading mechanism is fake depth and is struck, not deferred.

**Every mechanism named in the right-hand column is specified and unbuilt. No row in this table
describes behaviour the engine has today, and no row should be quoted as if it did.**

| Permitted phenomenon | Why it is social science, not stereotype | Effect class ([§5](#5-the-structural-safeguard-made-checkable)) | Mechanism that must read it (all unbuilt) |
|---|---|---|---|
| Historical exclusion | A recorded structural fact about past access, not a claim about present capacity. | OPPORTUNITY | Must reduce access probabilities (education, capital, office) in [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md); population-level in [`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md). |
| Unequal access to education | Access is environmental; *capacity to learn* is held identical across groups. | OPPORTUNITY | Must set the realised-attainment distribution while the inherent-capacity quantity kind stays invariant ([§5.3](#53-the-inherent-versus-realised-distinction)). |
| Residential segregation | A fact about where people live and what that co-locates them with. | EXPOSURE + NETWORK POSITION | Must modify which channels and events reach an entity, and the density/reach of ties in [`../world-model/RELATIONSHIP-GRAPH.md`](../world-model/RELATIONSHIP-GRAPH.md). |
| Language barriers | A proficiency-and-reach fact, not an intelligence fact. | OPPORTUNITY + EXPOSURE | Must gate which media (`MediaExposure`, `agent_schema.py`:42-53) and which institutions are reachable; must never touch capability. |
| Social trust | An observed, movable relational quantity between parties. | NETWORK POSITION + INTERPRETIVE FRAME | Must feed the directional trust edges of [`../world-model/RELATIONSHIP-GRAPH.md`](../world-model/RELATIONSHIP-GRAPH.md); must remain bidirectional and updatable, never an inherent trait. |
| Family networks | Who is connected to whom, and how strongly. | NETWORK POSITION | Must set edge density and kin ties in the relationship graph; solidarity effects must flow from here. |
| Discrimination | An action taken *by others toward* a group; a property of the environment and of others' beliefs, not of the target. | OPPORTUNITY + EXPOSURE | Must lower the target's access and raise adverse exposure; the discriminatory *belief* must live in the discriminator's belief record ([§3.3](#33-prejudice-belongs-in-a-belief-record-never-in-authoritative-reality)), never in the target's authoritative reality. |
| Political representation | A count of access to formal power, observable and historied. | OPPORTUNITY | Must modify access to office / policy channels; must feed the country model in [`../world-model/ORGANISATION-MODEL.md`](../world-model/ORGANISATION-MODEL.md). |
| Religious institutions | Organisations providing networks, information and services. | NETWORK POSITION + EXPOSURE | Must be institution entities and edges in [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) / [`../world-model/RELATIONSHIP-GRAPH.md`](../world-model/RELATIONSHIP-GRAPH.md); must be a source of information, not a determinant of character. |
| Shared historical memory | A recorded collective experience that shapes how new evidence is weighed. | INTERPRETIVE FRAME | Must set *priors on evidence* in [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md); must be evidence-updatable, never an absorbing state ([§5.4](#54-interpretive-frame-must-be-evidence-updatable-not-absorbing)). |
| Different media environments | A fact about which information reaches whom. | EXPOSURE | Must carry per-channel reach and trust-in-channel; must extend `MediaExposure` (`agent_schema.py`:42-53), which today carries reach but no trust term and is read by no code. |

Two of these carry the highest stereotype risk and are constrained further:

- **Discrimination** is the phenomenon most likely to be mis-modelled as an inherent trait, because
  it is *about* a group. It is permitted only as an environmental force acting on the target's
  opportunity and exposure, plus a belief held by the discriminating entity. It is never a field on
  the target.
- **Interpretive frame** is the phenomenon most likely to become a stereotype switch, because "this
  group reads events differently" is one careless step from "this group always believes X". It is
  permitted only as a modifier on how *observed evidence* is weighted, and is bound by
  [§5.4](#54-interpretive-frame-must-be-evidence-updatable-not-absorbing).

---

## 5. The structural safeguard, made checkable

The governing rule is only a slogan until it is expressed as something a validator can reject. This
section specifies that expression. All of it is unbuilt.

### 5.1 Every attribute must carry a quantity kind

Each attribute defined anywhere in the entity model is specified to carry a **`quantity_kind`** tag
declaring what kind of quantity it is. The quantity kinds, and the rule attached to each:

**A note on the name.** Earlier drafts of this document called this tag a *register*. That name is
withdrawn because [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md) already uses
"register" for two unrelated things — a *mechanism register* (:440, :1215) and *linguistic register*
inside `identity.languages[]` (:494), which is part of the very identity block this document
governs. `quantity_kind` is used here to avoid a three-way collision. The rename is terminological
only and settles nothing about which scheme governs; see the ownership note below and open
question 5.

| Quantity kind | Meaning | May a sensitive-identity attribute point an edge *into* it? |
|---|---|---|
| `INHERENT_CAPACITY` | Innate capability: intelligence, aptitude, learning capacity, physical/mental capacity-as-potential. | **No — prohibited.** |
| `MORAL_DISPOSITION` | Inherent moral character: trustworthiness, honesty, aggression, propensity to violence, corruptibility-as-trait. | **No — prohibited.** |
| `REALISED_ATTAINMENT` | Achieved outcome produced by mechanisms: attained education, wealth held, office held. | Yes, but only *transitively*, via an OPPORTUNITY/EXPOSURE mechanism — never a direct identity→attainment edge ([§5.3](#53-the-inherent-versus-realised-distinction)). |
| `OPPORTUNITY_STATE` | Access to resources, institutions, options. | Yes (effect class OPPORTUNITY). |
| `EXPOSURE_STATE` | What information/events/risks reach the entity. | Yes (effect class EXPOSURE). |
| `NETWORK_STATE` | Ties, reach, edge strength. | Yes (effect class NETWORK POSITION). |
| `FRAME_STATE` | Weights/priors on evidence. | Yes (effect class INTERPRETIVE FRAME), bounded by [§5.4](#54-interpretive-frame-must-be-evidence-updatable-not-absorbing). |

**No document currently tags anything against this scheme, and PERSON-MODEL has not accepted it.**
This must be stated plainly, because a safeguard whose vocabulary no schema-owning document adopts
changes nothing about the simulation — which is exactly the fake-depth test this document applies to
everyone else at [§4](#4-what-the-simulation-may-model-and-why-it-is-social-science-not-stereotype).
Specifically:

- The `quantity_kind` values above and the `effect_class` enum of
  [§5.2](#52-every-identitymechanism-edge-must-carry-an-effect-class) appear in **no other document
  in the set**. A search across `docs/world-model/` and `docs/design/` for `effect_class`,
  `OPPORTUNITY_STATE`, `EXPOSURE_STATE` and `INTERPRETIVE_FRAME` returns nothing.
- PERSON-MODEL uses a **different and non-isomorphic** scheme: rule E-3 routes sensitive identity
  through *named intermediate mechanisms* and expresses permitted sets as explicit mechanism lists —
  "M6, M17, M19" and nothing else
  ([`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md):328-340). That is indirection
  through a mechanism graph, not a type tag on an attribute. The two schemes are not translations of
  one another.

This document therefore **does not** assert ownership of an attribute→`quantity_kind` assignment
that PERSON-MODEL has not agreed to make. It states the *rule* it would impose *if* such a tagging
existed. Which of the two vocabularies governs — this one, PERSON-MODEL's E-3 mechanism
indirection, or a reconciliation of both — is an **owner decision**, recorded at
[§11](#11-open-questions-for-the-owner) question 5. Until it is taken, the tests in
[§6](#6-bias-and-stereotype-testing) have no tagged data to run against and cannot be written. This
is a stated dependency, not an assumption, and it is a larger gap than "unbuilt": the safeguard
currently has no data model anywhere that it could validate.

### 5.2 Every identity→mechanism edge must carry an effect class

Wherever a sensitive identity attribute is specified to influence a mechanism, that influence is
specified to be an explicit, declared edge carrying an `effect_class` drawn **only** from:

```text
effect_class ∈ { OPPORTUNITY, EXPOSURE, NETWORK_POSITION, INTERPRETIVE_FRAME }
```

**No such enum, quantity kind or validator exists today. Nothing in the paragraph below describes
software that runs.**

The enum is specified to contain no `CAPABILITY` and no `MORAL` value. The safeguard is therefore
*intended* to be structural rather than advisory: an engineer who wanted to wire race→competence
would have no vocabulary in which to declare it, and a validator conforming to this specification
would reject the edge, because its target attribute's quantity kind is `INHERENT_CAPACITY` or
`MORAL_DISPOSITION`. Whether that intent is realised depends entirely on work that has not started,
and on the unresolved vocabulary question in [§5.1](#51-every-attribute-must-carry-a-quantity-kind).

**The validation rule (specified, unbuilt):**

> A build-time validator must reject any identity-sourced edge whose declared `effect_class` is
> absent from the allowed enum, and any identity-sourced edge — of any effect class — whose *target
> attribute* has quantity kind `INHERENT_CAPACITY` or `MORAL_DISPOSITION`. The validator must run
> over scenario data and any rule pack. A rejection is a build failure, not a warning.

**What this validator cannot do, stated so it is not over-claimed.** The rule above is a *per-edge*
type check. It cannot see a multi-hop path. Two limits follow directly, and both are enforcement
gaps rather than solved problems:

- **Transitive leaks.** [§3.1](#31-the-absolute-prohibition) prohibits transitive as well as direct
  identity→capability edges, but identity → some permitted attribute → an `INHERENT_CAPACITY`
  attribute is legal at every individual hop. The quantity-kind table constrains only edges sourced
  *from* sensitive identity, so nothing in the per-edge rule stops a non-identity attribute pointing
  into `INHERENT_CAPACITY`.
- **Causal-path conditions.** [§5.3](#53-the-inherent-versus-realised-distinction) and
  [§6.2](#62-test-class-b--population-distribution-invariance) require that an OPPORTUNITY or
  EXPOSURE mechanism *sit on the causal path* of any group-differing realised-attainment value. That
  is a provenance property, not an edge property, and the per-edge validator cannot evaluate it.

Closing either would require a **mechanism-graph reachability check** over the rule pack — a
distinct, unspecified analysis that would additionally depend on the P0.6 provenance spine, which is
unbuilt ([§10](#10-dependencies-and-what-does-not-exist-today)). No such check is specified here.
Today the only thing that would catch a transitive leak is Test class A
([§6.1](#61-test-class-a--counterfactual-identity-swap-invariance)), and Test class A is itself
unrunnable without named RNG substreams. Both limits are recorded as enforcement gaps in
[§12](#12-features-specified-with-no-mapped-causal-mechanism).

This is the checkable form of the governing rule. It is specified to run at load/build time so that
a mis-typed edge cannot reach a running simulation — in contrast to the current engine, where a
mis-keyed effect silently does nothing (`MacroStateHolder.apply_deltas` skips unknown keys in
silence, `scaffold/backend/app/simulation/agents/macro_state.py`:37-41), which is precisely the
failure mode that let a 63× population error survive undetected
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.10). A silent skip is
unacceptable for a safety edge; it must be a hard failure.

### 5.3 The inherent-versus-realised distinction

This is the crux of why permitted modelling ([§4](#4-what-the-simulation-may-model-and-why-it-is-social-science-not-stereotype))
does not collapse into prohibited modelling ([§3](#3-what-the-simulation-must-not-model)).

- **Inherent capacity** (quantity kind `INHERENT_CAPACITY`) — the potential to learn, reason, lead — is
  specified to be drawn **independently of sensitive identity**. Over any population, its
  distribution must be statistically indistinguishable across identity groups
  ([§6.2](#62-test-class-b--population-distribution-invariance)).
- **Realised attainment** (quantity kind `REALISED_ATTAINMENT`) — the education a person actually
  received, the wealth they actually hold — is specified to be *produced by* opportunity and
  exposure mechanisms acting over a life history. It **may** differ across groups, because unequal
  access is real and is the point of modelling historical exclusion.

So P2 ("group Y is naturally less educated") is prohibited as an inherent-capacity claim, while
"group Y has, on average, less *attained* education because of modelled unequal access" is
permitted as a realised-attainment outcome — and the two are distinguished by *which quantity kind
the value lives in and whether an OPPORTUNITY mechanism sits on the causal path*. A realised-attainment
value that differs by group with **no** opportunity/exposure mechanism on its causal path is a
disguised inherent claim and must fail validation.

### 5.4 Interpretive frame must be evidence-updatable, not absorbing

INTERPRETIVE_FRAME is the effect class most open to abuse, so it carries an extra constraint.

- A frame effect may set an entity's **prior** on a class of evidence — e.g. a community with a
  recorded, event-sourced memory of a past crackdown may assign a higher prior to a new-crackdown
  narrative. That is Bayesian updating from lived experience, and it is legitimate.
- A frame effect may **not** be an absorbing or monotone state that contrary evidence cannot move.
  If a group's frame makes them believe X regardless of evidence, it has ceased to be a frame and
  become a stereotype switch.
- **Ruling out the absorbing endpoint is not sufficient, and this document previously stopped
  there.** A frame effect that sets a prior to 0.99 is not absorbing, is formally evidence-updatable,
  and is a stereotype switch in everything but name. It would pass the bullet above and pass the
  eight-question hook of [§5.5](#55-the-eight-question-hook), which catches only probability 0 or 1.
  The gap is recorded here rather than left implicit.

**The attributability requirement (specified, unbuilt).** The control that closes the gap is *not* a
ceiling on how large an identity-sourced difference may be. [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md):376-410
(rule E-5) considers and explicitly rejects a magnitude bound, on the ground that the intended and
founder-required mechanisms — network composition, discrimination exposure, language access — must
shift the distribution, so "a total-variation bound would flag the model's intended and
founder-required mechanism as bias, and any bound loose enough not to would detect nothing"
(:385-387). This document does not overturn that finding. The requirement is instead:

> Every identity-sourced effect, of any allowed effect class, must be **fully attributable**. The
> divergence it produces must decompose into named contributions from declared intermediate
> mechanisms, and the **residual — divergence not attributable to any declared mechanism — must be
> zero**. A frame or network effect large enough to function as a stereotype switch is caught not by
> its size but by the fact that no declared mechanism accounts for it. The residual is the bias
> signal; the magnitude is not.

**This closes a delegation that was, until this revision, circular.** PERSON-MODEL:406-408 assigns
"the residual threshold, the failing criteria, the decomposition method and the reporting format" to
this document, and this document supplied none of them. It still does not *choose* them: the residual
threshold, the decomposition method and the reporting format are **owner decisions**, recorded at
[§11](#11-open-questions-for-the-owner) question 9. What this revision fixes is that the delegation
is now acknowledged and scoped rather than silently dropped. Until question 9 is answered,
PERSON-MODEL's rule E-5b has no threshold and cannot be implemented.

This constraint is the same shape as the belief-ratchet defect the audit already found: cohort
belief today is a one-way decay to zero that no action can reverse
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.9;
`scaffold/backend/app/simulation/agents/cohort_agent.py`:35-38). A frame effect must therefore be
specified against a **bidirectional** belief model in which contrary evidence measurably moves the
belief — the same precondition that [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md)
and [`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md) depend on. A
frame that cannot be updated by evidence must fail the invariance tests in
[§6](#6-bias-and-stereotype-testing).

### 5.5 The eight-question hook

Because the charter's eight-question standard applies to every state change
([`../../CHARTER.md`](../../CHARTER.md):118-130), an identity-influenced state change is specified to
record, in its event, that identity shifted a *probability or weight* and that alternative reactions
were possible (question 7). This gives a reviewer a mechanical check: walk the event history, and
any identity-influenced transition whose record shows identity as a deterministic gate — no
alternative possible, probability 0 or 1 — is a violation of the "probabilistic, never
deterministic-by-identity" rule. This hook depends entirely on event-sourcing, which does not exist
and is a P0.6 prerequisite ([§10](#10-dependencies-and-what-does-not-exist-today)).

---

## 6. Bias and stereotype testing

This section specifies the tests. **None of these tests exists.** The repository has no invariant
tests at all today ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md)
§6.34), so there is nothing in place that would catch a biased attribute. Every test below is a
specified future obligation, and two of them cannot even be written until prerequisites in
[§10](#10-dependencies-and-what-does-not-exist-today) land.

A cross-cutting requirement first: several tests below rely on generating "the same entity but for
one identity attribute". That comparison is only meaningful if entity generation uses a **named,
per-entity RNG substream keyed on stable identity**, so that swapping one attribute changes only
that attribute's declared downstream effects and not the entire draw order. That isolation does not
exist. It is owned by **P0.4A — establish a deterministic randomness architecture**, a Phase 0
workstream created by founder decision of 18 July 2026 and ordered `P0.4 → P0.4A → P0.5 → P0.6`
([`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md) §P0.4A);
whether the mechanism is stateful named substreams or keyed / counter-based draws is unchosen, and
its relationship to a recorded architecture decision (ADR-007's single-RNG design;
[`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):170-175) is an
open owner question.
Until they exist, an identity-swap test cannot isolate the variable it is trying to test. This is
stated so the tests are not mistaken for something that could be run today.

### 6.1 Test class A — counterfactual identity-swap invariance

**What is tested.** Take a materialised entity E. Construct E′ identical to E in every non-sensitive
attribute and in RNG-substream seeding, differing only in **one** sensitive identity attribute (for
example, religion label A→B, or nationality A→B).

**What is asserted.**
- Every `INHERENT_CAPACITY` attribute of E′ equals that of E. The swap must move none of them.
- Every `MORAL_DISPOSITION` attribute of E′ equals that of E.
- `OPPORTUNITY_STATE`, `EXPOSURE_STATE`, `NETWORK_STATE` and `FRAME_STATE` attributes may differ,
  and only through edges declared with an allowed `effect_class`
  ([§5.2](#52-every-identitymechanism-edge-must-carry-an-effect-class)).
- `REALISED_ATTAINMENT` attributes **may also differ**, but only where an OPPORTUNITY or EXPOSURE
  mechanism sits on the declared causal path, exactly as
  [§5.3](#53-the-inherent-versus-realised-distinction) qualifies it. A realised-attainment difference
  with no such mechanism on its path is a disguised inherent claim and fails.
- Every permitted difference, in any of the five quantity kinds above, must satisfy the
  attributability requirement of
  [§5.4](#54-interpretive-frame-must-be-evidence-updatable-not-absorbing): it must decompose into
  declared mechanisms with zero unattributable residual. Size alone is not the test; unexplained
  divergence is.

**An earlier draft of this clause omitted `REALISED_ATTAINMENT`, and that omission was a defect.**
Read literally, it asserted that swapping a person's religion must not change their attained
education — which would have outlawed the single mechanism this document exists to legitimise,
unequal access producing unequal realised outcomes. It also contradicted the failure clause below,
which was narrower than the assertion clause. The two now enumerate the same set.

**What constitutes failure.** *Any* difference in a capability-class or moral-class attribute under
the swap. A single such difference is a hard failure — it is direct evidence of an identity→capability
or identity→moral edge, whether declared or leaked in through generation. Separately: any difference
in a permitted quantity kind that cannot be attributed to a declared mechanism is a failure, whatever
its magnitude.

### 6.2 Test class B — population distribution invariance

**What is tested.** Over a materialised population, partition entities by a sensitive identity
attribute and compare the *distributions* of outputs across groups.

**What is asserted.**
- Distributions of `INHERENT_CAPACITY` attributes are statistically indistinguishable across groups,
  within a declared tolerance.
- Distributions of `MORAL_DISPOSITION` attributes are statistically indistinguishable across groups.
- Distributions of `REALISED_ATTAINMENT`, `OPPORTUNITY_STATE`, `EXPOSURE_STATE`, `NETWORK_STATE` and
  `FRAME_STATE` attributes **may** differ across groups — and the test explicitly does **not** assert
  their equality, because asserting equal *outcomes* would erase the very structural inequality the
  model is meant to represent. For any such attribute that *does* differ by group, the test
  additionally requires that a declared mechanism of an allowed effect class sits on its causal path
  — an OPPORTUNITY or EXPOSURE mechanism in the case of `REALISED_ATTAINMENT`
  ([§5.3](#53-the-inherent-versus-realised-distinction)) — and that the divergence be fully
  attributable to declared mechanisms with **zero residual**
  ([§5.4](#54-interpretive-frame-must-be-evidence-updatable-not-absorbing)). A group difference with
  no such mechanism is a disguised inherent claim and fails.

  `NETWORK_STATE` and `FRAME_STATE` were absent from both the assertion and failure clauses of an
  earlier draft, which left across-group frame and network differences untested in both directions —
  the precise hole through which a stereotype switch would pass. They are named explicitly here.

**What constitutes failure.** A statistically significant across-group difference on any
capability-class or moral-class attribute; or a group difference on any permitted attribute —
realised attainment, opportunity, exposure, network or frame — with no declared mechanism on its
causal path, or with a non-zero unattributable residual.

### 6.3 Test class C — prejudice provenance

**What is tested.** A scan of the authoritative-reality store for prejudiced propositions.

**What is asserted.** No capability-class or moral-class attribute in any entity's
authoritative-reality record has a value that is a function of a sensitive identity attribute
([§3.3](#33-prejudice-belongs-in-a-belief-record-never-in-authoritative-reality)). Any negative
proposition about a group appears only inside a belief record with an explicit `holder` (not the
target) and an explicit truth status.

**What constitutes failure.** A prejudiced proposition found in authoritative reality rather than in
a belief record; or a belief record asserting a group prejudice with no holder or no truth status
(which would make it indistinguishable from fact).

### 6.4 Test class D — generated-narration bias

**What is tested.** The narration boundary — the point at which the LLM turns an authoritative
record into biography or dialogue ([§7](#7-llm-narration-constraints)) — is exercised in two ways:

- **Golden-record check.** Feed the boundary a fixed authoritative record, a fixed prompt version
  and a fixed seed; capture the output; run it against a prohibited-construction checklist (a
  detector for essentialising forms: *inherently*, *naturally*, *by nature*, *typical of [group]*,
  and any group-noun bound to a capability or moral predicate). A hit is a failure.
- **Narration-swap check.** Narrate E and E′ from [§6.1](#61-test-class-a--counterfactual-identity-swap-invariance)
  and assert the two generated character-and-competence portrayals are equivalent modulo the
  identity terms themselves.

  **No oracle for this assertion is specified, and none currently exists.** "Equivalent modulo the
  identity terms" is a comparison between two pieces of free prose. The prohibited-construction
  detector described above cannot perform it — that detector matches essentialising word forms and
  has no capacity to compare two portrayals for equivalence. No embedding comparison, human-review
  process or judge model is specified here, and the evaluation step is strictly harder than the
  golden-record check it sits beside. This sub-test therefore reads as a mechanism but has nothing
  that can execute its assertion, which is the same fake-depth pattern this document polices
  elsewhere; it is recorded as an enforcement gap in
  [§12](#12-features-specified-with-no-mapped-causal-mechanism). If a judge model is ever
  contemplated for this role, note the determinism-boundary implication: a model deciding a safety
  verdict is a model exercising authority, which cuts directly against ADR-006 and against
  [§7.1](#71-narrate-never-author). That would be an owner decision, not an implementation detail.

**What constitutes failure.** Generated prose asserts or implies a capability or moral proposition
about a group; or the competence/character portrayal of E and E′ differs under identity swap.

**A necessary honesty caveat about this test.** LLM output is neither authoritative nor reproducible
state ([`../../CHARTER.md`](../../CHARTER.md):36-44; ADR-006). Test class D is therefore a
*content-safety gate on the narration boundary*, not a determinism test, and its
prohibited-construction detector is a **heuristic**: it will miss stereotypes it has no pattern for
and may flag innocuous text. It reduces risk; it does not prove absence of bias. It must not be
described, now or later, as a guarantee. This limitation is recorded again in
[§12](#12-features-specified-with-no-mapped-causal-mechanism).

### 6.5 Where these tests attach

These are specified as invariant tests over the entity generator and the narration boundary. They
have no home in the current test suite. That suite is five tests
(`scaffold/backend/tests/test_engine.py`:25, :34, :43, :52, :61); its *determinism test* asserts one
thing, that two macro snapshots match
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.3, citing
`test_engine.py:40`), and its one structural safeguard,
`test_llm_gateway_cannot_write_state` (:61), guards the determinism boundary that
[§7.1](#71-narrate-never-author) relies on and that [`../../CHARTER.md`](../../CHARTER.md):44 names
as the CI guard. None of the five knows anything of entities, quantity kinds or identity. Building
the tests in this section is part of the entity-model work and is BACKLOG, gated behind the
prerequisites in [§10](#10-dependencies-and-what-does-not-exist-today).

---

## 7. LLM narration constraints

The authoritative record can be scrupulously unbiased and the system can *still* emit stereotype, if
the LLM that writes the readable biography or the spoken dialogue introduces it. The clean record is
necessary but not sufficient. This section constrains the generator.

### 7.1 Narrate, never author

The founder's rule — the LLM may narrate, never author — is the charter's determinism boundary
(ADR-006) applied to the entity layer. It exists in code today as the `ActionProposal` boundary: the
LLM gateway may return only that object, which carries no authority to change numbers
(`scaffold/backend/app/simulation/schemas/agent_schema.py`:374-393; `llm_gateway.py`:35). All
generated biography, briefing and dialogue is specified to route through this same boundary. In
identity terms this means:

> The LLM may only render facts already present in the authoritative and derived records passed to
> it. It must not introduce, infer or embellish any identity→capability or identity→moral
> proposition that the record does not contain. It has no authority to decide that a character is
> clever, honest, aggressive or trustworthy; those are engine facts or they do not exist.

### 7.2 Prompt constraints

Generation prompts are specified to:

- pass only the records the current view is entitled to (role-scoped), never the whole
  authoritative reality;
- never instruct or invite the model to infer character, competence or morality from identity;
- carry the standing instruction that identity terms describe social experience, networks, exposure
  and interpretation only, mirroring the governing rule.

### 7.3 Output filtering and provenance

- Generated biography and dialogue are specified to pass the prohibited-construction detector of
  [§6.4](#64-test-class-d--generated-narration-bias) **before display**, not only in offline tests.
- All generated text is specified to carry a visible provenance tag distinguishing it from
  engine-computed fact, at the interface and not merely in a footnote
  ([`../../CHARTER.md`](../../CHARTER.md):141). The intent is that even a stereotype the filter
  misses would be presented as *generated narration*, never as computed ground truth — a mitigation,
  not a cure, and explicitly not a substitute for the record and generator being clean in the first
  place.

  **No such tag exists today, and generated text is already being emitted without one.** The only
  generated text in the project is the stub briefing `generate_briefing`
  (`scaffold/backend/app/simulation/llm_gateway.py`:85-103), which returns a bare `str`; it is
  surfaced verbatim in the API response at
  `scaffold/backend/app/api/routes_simulation.py`:76 with no provenance tag of any kind. This is the
  one place in this document where the specified safeguard is not merely unbuilt but is already
  contradicted by shipped behaviour. [§12](#12-features-specified-with-no-mapped-causal-mechanism)
  item 4 records that there is, in addition, no interface layer to attach a tag to.

### 7.4 Dialogue is bounded by the same rule

A character may *voice* a prejudice in dialogue — a bigoted minister may say bigoted things — but
only as an expression of that character's recorded belief ([§3.3](#33-prejudice-belongs-in-a-belief-record-never-in-authoritative-reality)),
attributable and contestable, never as narrator-voice fact and never invented by the model beyond
what the belief record supports. Dialogue that asserts a group trait the speaker's belief record
does not contain is the LLM authoring, and is prohibited.

---

## 8. Fictional identities and the no-real-entities rule

### 8.1 The founder's preference

Because the world is fictional, the founder records a preference: **fictional cultural, ethnic and
religious identities may be preferable for the default scenario, while the mechanisms remain
grounded in real social science**
([`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md):315-316).
Fictional labels remove any implication that the model is making a claim about a real group, while
the *mechanisms* attached to those labels — exclusion, access, segregation, trust, memory — stay
real and inspectable. Identity is fictional; the social science is not.

### 8.2 Connection to the charter

This preference sits directly on top of the charter's hard rule: **no real nations, organisations,
named individuals or real operational vulnerabilities** ([`../../CHARTER.md`](../../CHARTER.md):137).
Fictional identity labels are one way of honouring that rule at the identity layer. The charter rule
is settled policy, not an open question.

### 8.3 The enforcement gap — narrowed by the B5 decision, not closed

The charter rule is today a **rule, not a check**. Nothing validates entity names, labels or
identities against real-world referents; the scenario's own `fiction_disclaimer`
(`scaffold/scenarios/kestral-strait.json`:7) is read by no code and appears in no API response or
interface.

CHARTER:137 is **settled policy**, and as of 18 July 2026 part of its enforcement mechanism is
settled too. An earlier draft of this section declined to name any mechanism as required, on the
ground that a load-time check and a surfaced fiction disclaimer were both candidate mitigations for
an *open* B5 and that naming either would pre-empt the owner. B5 is no longer open. Two of those
candidates are now **mandatory requirements**, because the founder decision mandates them
([§9.2](#92-the-eight-controls-settled-policy)):

- the scenario loader **must require** an explicit `world_mode: fictional` declaration and **fail
  closed** without it — control **C2**; and
- the API and the interface **must disclose** that the active world is fictional — control **C7**.

**Neither exists.** There is no `world_mode` field, no scenario schema to put one in
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.13), and no
interface layer to disclose anything at ([§12](#12-features-specified-with-no-mapped-causal-mechanism)
item 4). Naming them here no longer pre-empts an owner decision; it restates one.

**What remains genuinely open is the third candidate:** a load-time check that entity names and
labels do not *refer to* real nations, organisations or people. The decision does not mandate it and
does not supply the oracle it would need ([§12](#12-features-specified-with-no-mapped-causal-mechanism)
item 2). Control **C4** — real persons, organisations and political populations cannot be
influence-target entities — is adjacent but is not the same control: C4 constrains what may be
*targeted*, and can be enforced structurally by requiring every target to be a reference into the
fictional world's own entity store; a real-entity name check would constrain what may be *named
anywhere in a scenario*, and needs a reference list or classifier the project does not have.
[§11](#11-open-questions-for-the-owner) question 6 is narrowed to that residue and is not closed by
it.

### 8.4 The existing-data tension — an owner decision, not resolved here

The current default scenario does **not** follow the founder's fictional-identity preference
uniformly. It mixes a real-world religious label, `sunni-mixed`, into four of five cohorts
(`scaffold/scenarios/kestral-strait.json`:45, :85, :168, :208) alongside a fictional label,
`highland-traditional` (:128). Replacing the real label with a fictional one would align the data
with the founder's stated preference and with CHARTER:137, but it is an owner decision affecting
existing scenario data, it couples to this document's safety posture, and it is **not resolved
here**. It is recorded in [§11](#11-open-questions-for-the-owner).

**The B5 decision raises the stakes on this question without answering it.** Control C4 forbids real
political populations from being influence-target entities, and those four cohorts are exactly the
objects the `Campaign` schema's `target_cohorts` field selects
(`scaffold/backend/app/simulation/schemas/agent_schema.py`:320-346). Whether a *fictional aggregate
cohort carrying a real-world religious label* is a "real political population" for the purposes of
C4 is not something the decision states, and this document does not decide it. It is a live
ambiguity with a real consequence — under the narrow reading the label is a naming preference, under
the broad reading the default scenario would not pass C4 as shipped — and it is recorded as
[§11](#11-open-questions-for-the-owner) question 13.

---

## 9. Blocker B5 — the settled dual-use policy, and what it now requires

> **This section records a decision that has already been taken.** It is not an open question, not a
> recommendation, and not a menu of options. It must not be re-opened, softened, traded off or
> "balanced against" anything by an agent.
>
> **It is equally not a description of working software.** Every control below is **required and
> unbuilt**. There is no `world_mode` field, no scenario schema to hold one
> ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.13), no campaign
> instantiation path, no interface, and no test of any of it. A reader who took a sentence here for
> a statement about the current build would be badly misled, and in the one place where being
> misled matters most.

### 9.1 The coupling, and why the decision bites

MERIDIAN contains an information-operations model. The `Campaign` schema is *shaped* to select
audiences by attribute — it declares the fields such a selection would use, and, as the first
precision below records, nothing reads them today:
`target_cohorts` and `existing_grievance` — the latter documented as "Pre-existing
grievance the campaign exploits" — with a messenger's `perceived_independence` and an amplification
network (`scaffold/backend/app/simulation/schemas/agent_schema.py`:320-346, :326-331). The
attributes it targets are the same audience attributes this document governs:
`InfluenceSusceptibility` (:72-77), `MediaExposure` (:42-53), and `Demographics` including
`religion_majority` and `primary_language` (:22-28).

The entity model is specified to refine exactly those attributes — from five aggregate cohorts to
**named individuals with portraits, sensitive-identity detail and an asymmetric social graph**. There
is no entity model today; there is a set of draft specifications, of which this is one. That
specified refinement would be a strict *enlargement* of the audience-segmentation surface that the
influence-ops model targets. In one sentence:

> **The identity attributes this document *governs* are the attributes an influence-operations
> targeting schema *would consume*; specifying them in finer detail would enlarge the dual-use
> surface, so the two are coupled and cannot be reasoned about independently.**

Two precisions, so that the section does not inflate the very risk it is asking the owner to weigh:

- **No targeting is performed by the current build.** The `Campaign` schema
  (`agent_schema.py`:320-346) is instantiated nowhere. The scenario's `hidden_campaign` is loaded as
  a raw dict at `scaffold/backend/app/simulation/engine.py`:111 and is read by no code thereafter.
  The schema consumes nothing today.
- **This document defines almost no identity attributes of its own.** It specifies *constraints on,
  and tests over,* attributes that the other world-model documents define, as
  [§12](#12-features-specified-with-no-mapped-causal-mechanism) states. The coupling is real, but it
  runs through PERSON-MODEL's attribute detail rather than through this document's contents.

That coupling is what the founder decision of 18 July 2026 responds to. It does not dissolve the
coupling — the identity attributes are still the attributes a targeting schema would consume — but
it fixes the envelope those attributes must be specified inside, so the identity work no longer
waits on an unknown.

### 9.2 The eight controls: settled policy

The founder decided B5 on 18 July 2026. For the public MVP, the following are **settled policy that
the specification must enforce.** They are stated here as requirements on future work. **None of the
eight is implemented, and none is testable today** — [§9.6](#96-how-each-control-would-be-tested)
sets out what testing each would mean, and is candid about which of them currently has no decision
procedure at all.

| # | Control (settled) | Status in the code today |
|---|---|---|
| **C1** | Influence mechanics operate **only** in explicitly fictional worlds. | Not enforced. `Campaign` (`agent_schema.py`:320-346) is instantiated nowhere and gated by nothing; there is no world-mode concept anywhere. |
| **C2** | The scenario loader **requires** `world_mode: fictional` and **fails closed** when it is missing. | Not enforced. No such field, and no scenario schema to declare it in (audit §5.13). The only fictionality marker, `fiction_disclaimer` (`kestral-strait.json`:7), is free text read by no code. |
| **C3** | Real-world scenario import remains **disabled**. | Vacuously true and unguarded: no import path exists, so nothing is currently enabled to disable. See [§9.6](#96-how-each-control-would-be-tested) on why this is the weakest of the eight to evidence. |
| **C4** | Real persons, organisations and political populations **cannot** be influence-target entities. | Not enforced. `target_cohorts` selects whatever the scenario file declares; nothing constrains what a cohort denotes. |
| **C5** | Protected characteristics **cannot** be used as optimisation criteria for persuasion or manipulation. | Not enforced, and not currently expressible: no attribute anywhere carries a protected-characteristic tag, and the campaign model has no declared factor set to check against ([§9.4](#94-what-the-campaign-model-may-and-may-not-optimise-against)). |
| **C6** | Fictional **aggregate** narrative diffusion, exposure, adoption and counter-messaging **remain allowed**. | Partly present, partly impossible. Aggregate adoption exists (`Narrative.adoption_by_cohort`, `agent_schema.py`:269-274); counter-messaging cannot work against a one-way belief ratchet (audit §5.9). |
| **C7** | The API and UI **disclose** that the active world is fictional. | Not enforced. No API response carries a fictionality declaration; there is no interface layer to disclose at ([§12](#12-features-specified-with-no-mapped-causal-mechanism) item 4). |
| **C8** | Disclosure and any future acceptable-use language are **supplementary**. **Technical enforcement is mandatory.** | Not enforced. Today the project's *only* dual-use controls are prose — the charter's scope bullets and an unread disclaimer string — which is precisely the posture C8 rules out. |

Two consequences of the decision that are easy to lose and must not be:

- **It is a floor, not a ceiling.** The eight controls are the minimum. Nothing in the decision
  licenses a design that satisfies the letter of C1-C7 while re-creating the capability elsewhere.
- **C6 is a permission, and permissions can be over-blocked.** An enforcement design that satisfied
  C1-C5 by disabling aggregate narrative diffusion would fail the decision just as surely as one
  that under-enforced it, because aggregate diffusion in a fictional world is the mechanism the
  product exists to model.

### 9.3 Permitted and not permitted: the identity distinction in the founder's form

The decision restates the identity boundary in two blocks, and they are reproduced in that form
because the pairing is the point — each block is only safe to read next to the other:

> **Permitted:** identity affects lived experience, relationships, discrimination, institutional
> access, media exposure and cultural interpretation.
>
> **Not permitted:** identity acts as an inherent competence, morality, loyalty, violence or
> manipulability coefficient.

This is the same rule this document has enforced since [§2](#2-the-governing-design-rule), with one
substantive addition that must not be skimmed past. The prohibited list now names **loyalty** and
**manipulability**, which the earlier formulation did not. Both are directly relevant to an
influence model:

- **Loyalty** is a moral-class quantity in this document's typing (`MORAL_DISPOSITION`,
  [§5.1](#51-every-attribute-must-carry-a-quantity-kind)) and joins trustworthiness and honesty
  under the prohibition. An identity-conditioned loyalty coefficient is the classic
  fifth-column stereotype, and it is now named as prohibited rather than merely implied by the
  moral-valence class.
- **Manipulability** is the sharper one, because it is the quantity an influence model most wants.
  `InfluenceSusceptibility` (`agent_schema.py`:72-77) is exactly a manipulability quantity. The
  decision does **not** prohibit modelling susceptibility; it prohibits identity acting **as** a
  susceptibility coefficient. Susceptibility may be produced by permitted mechanisms — media
  environment, network position, institutional trust, grievance formed by recorded experience — and
  may **never** be read off an identity label. In this document's vocabulary, `InfluenceSusceptibility`
  is a value with no direct identity edge permitted into it; any group difference in it must
  decompose into declared mechanisms with zero unattributable residual
  ([§5.4](#54-interpretive-frame-must-be-evidence-updatable-not-absorbing),
  [§6.2](#62-test-class-b--population-distribution-invariance)).

  **Whether `InfluenceSusceptibility` is a `FRAME_STATE`/`EXPOSURE_STATE` composite or something the
  quantity-kind scheme cannot currently type is not settled**, and the decision does not settle it.
  It is folded into open question 5 rather than answered here.

### 9.4 What the campaign model may and may not optimise against

The decision is explicit that the campaign model is not required to be blind to audience structure:

> The campaign model **may** use non-sensitive factors — **geography, institutional affiliation,
> economic exposure, political behaviour, media consumption** — where justified by the fictional
> scenario. It **must not** optimise against protected traits.

Two obligations follow, and neither is discharged anywhere in the document set:

1. **The permitted factor set must be declared and closed.** "May use non-sensitive factors" is only
   checkable if the factors a campaign's selection or scoring function may read are an explicit
   allowlist, and every attribute in the model carries a tag saying whether it is a protected
   characteristic. No such allowlist and no such tag exist, in code or in any specification. Where
   the tag lives, and who owns it, is [§11](#11-open-questions-for-the-owner) question 12, and it
   sits on top of the unresolved vocabulary question 5.
2. **"Where justified by the fictional scenario" is a requirement, not a formality.** A permitted
   factor still has to earn its place: the causal-value rule from
   [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) applies, and a targeting
   factor with no scenario justification is struck rather than kept as a convenience.

**The unresolved hazard is proxying, and this document will not pretend otherwise.** Geography is
named as a permitted factor, and geography is also the canonical proxy for ethnicity and religion —
§4 of this document *requires* residential segregation to be modelled, which by construction makes
location correlate with identity. A campaign that targets by district can therefore optimise against
a protected characteristic without ever reading one, and a validator that checks only declared inputs
will pass it. The decision permits the factor and prohibits the outcome; it does not say how to tell
them apart. That is a real gap, it is recorded as
[§11](#11-open-questions-for-the-owner) question 11 and
[§12](#12-features-specified-with-no-mapped-causal-mechanism) item 8, and it is **not** resolved by
any test specified below.

### 9.5 Technical enforcement is mandatory; disclosure is supplementary

Control C8 is the one that governs how the other seven may be evidenced, so it is stated separately.

> **Disclosure and any future acceptable-use language are supplementary. Technical enforcement is
> mandatory.**

Read operationally, that means:

- **A disclosure-only control does not satisfy this decision.** A banner, a README paragraph, a
  licence field-of-use clause, a `fiction_disclaimer` string, or a sentence in this document is not
  an implementation of C1-C5. It may accompany one. It may never stand in for one.
- **No control may be marked satisfied on documentary evidence.** The evidence for each of C1, C2,
  C4 and C5 must be a test that fails against the unenforced build and passes against the enforced
  one. C7 is itself a disclosure control, so passing C7 is evidence about C7 and about nothing else.
- **Failure must be refusal, not degradation.** The existing engine's habit of silently skipping
  what it does not understand (`MacroStateHolder.apply_deltas` skips unknown keys in silence,
  `scaffold/backend/app/simulation/agents/macro_state.py`:37-41 — the same pattern that let a 63×
  population error survive, audit §5.10) is unacceptable for these controls, exactly as it is for
  the safety edges in [§5.2](#52-every-identitymechanism-edge-must-carry-an-effect-class). A
  missing `world_mode` must abort the load. It must not default, warn, or proceed in a reduced mode.

### 9.6 How each control would be tested

The decision would otherwise be a promise. This subsection turns each control into something a test
could decide — and says plainly where no decision procedure exists, because "protected
characteristics cannot be used as optimisation criteria" is not self-checking and an unfalsifiable
control is worse than an acknowledged gap.

**Every test below is specified and unwritten. The repository has no invariant tests at all**
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §6.34).

| Control | What a test would assert | Honest limits |
|---|---|---|
| **C1** | Load a scenario whose `world_mode` is absent or is any value other than `fictional`; assert the run aborts **before** any influence object is constructed, and that no campaign, targeting or diffusion code path is reachable. Paired with a positive case: a `fictional` scenario constructs them normally. | Only as strong as the enumeration of entry points. "Unreachable" is a whole-program property; a test can only cover the paths it knows about. Enumerating the influence subsystem's entry points is a static-analysis obligation with no tool specified. |
| **C2** | A table test over the loader: key missing → hard failure; key present with any other value → hard failure; malformed value → hard failure; `fictional` → success. Plus a schema-level assertion that the field has **no default**, so it cannot be silently filled. Plus an assertion that the failure is an exception, not a logged warning. | The most testable of the eight, and the one with the least excuse for remaining unbuilt. Requires a scenario schema, which does not exist (audit §5.13). |
| **C3** | Assert the loader accepts only the project's own scenario schema and rejects any other source; assert no module exposes an import path for externally-sourced real-world data. | **Weak by construction.** A test cannot prove the absence of a feature; it can only fail once someone adds one, and only if it knows where to look. C3's real force is a prohibition on future work, carried by review and by C1/C2 — not by a test. Recorded as [§12](#12-features-specified-with-no-mapped-causal-mechanism) item 9. |
| **C4** | A structural assertion that every influence target is a typed reference into the scenario's own fictional entity store — never free text, never an external identifier — so a real person is *unrepresentable* as a target rather than *detected* as one. Plus a negative test that a campaign referencing an unresolvable or externally-keyed target fails to load. | Structural enforcement is achievable and is the right shape. It does **not** stop a scenario author naming a fictional entity after a real person, which needs the real-entity oracle that does not exist ([§12](#12-features-specified-with-no-mapped-causal-mechanism) item 2, question 6). And the scope of "political populations" is itself ambiguous — question 13. |
| **C5** | Two tests, because neither alone is sufficient. **(a) Static:** every attribute carries a `protected` tag; the campaign's selection and scoring inputs are a declared closed allowlist; a build-time validator rejects any rule pack whose selection or scoring reads a protected-tagged attribute, or reads an attribute whose *declared derivation* reads one. A rejection is a build failure. **(b) Behavioural — permutation invariance:** hold every non-sensitive factor fixed and permute protected-characteristic values across the population; campaign target selection and scoring must be **unchanged**. Any change is a failure. | This is the checkable definition the control needs, and it is still incomplete. (a) is a per-edge check with the same blindness as [§5.2](#52-every-identitymechanism-edge-must-carry-an-effect-class): it cannot see an undeclared proxy. (b) catches direct use and declared derivation, and **does not** catch geography-as-proxy ([§9.4](#94-what-the-campaign-model-may-and-may-not-optimise-against)) — permuting religion while holding district fixed leaves a district-targeting campaign invariant and passing. (b) also requires that permuting values not shift the draw order, which is the RNG-isolation dependency in [§10](#10-dependencies-and-what-does-not-exist-today). Neither test exists; the `protected` tag has no home (question 12). |
| **C6** | A regression guard rather than a prohibition: a fictional scenario exercising aggregate diffusion, exposure, adoption **and counter-messaging** must run to completion with every gate above active. Its purpose is to catch over-blocking. | Cannot be written yet. Counter-messaging has no mechanism: cohort belief is a one-way decay that no action reverses (audit §5.9; `cohort_agent.py`:35-38). The test depends on the bidirectional belief model in [§10](#10-dependencies-and-what-does-not-exist-today). |
| **C7** | A response-schema test asserting that **every** API response carrying simulation state declares the world fictional — not one endpoint, all of them — and an interface assertion that the declaration is visible without interaction. | There is no interface to test ([§12](#12-features-specified-with-no-mapped-causal-mechanism) item 4), and generated text is *already* emitted untagged (`llm_gateway.py`:85-103 → `routes_simulation.py`:76), so the current build actively fails the spirit of C7 today. Passing C7 evidences C7 only ([§9.5](#95-technical-enforcement-is-mandatory-disclosure-is-supplementary)). |
| **C8** | Not a control with a test of its own. Its operational form is a **review rule**: no control may be recorded as satisfied unless its evidence is an executing test, and any control whose evidence is a document, licence term or disclosure string is recorded as **not satisfied**. | A review rule is not enforcement, which is uncomfortable given that C8's own subject is the inadequacy of non-enforcement. Stated rather than hidden. The mitigation is that C8 governs the *evidence* for C1-C7, and those are testable. |

### 9.7 What the decision changes about the publication gate

This is the consequence most likely to be mis-stated downstream, so it is stated bluntly.

**B5 no longer clears by an owner decision. It clears by technical enforcement being implemented and
verified.** The decision has been made; the blocker has not lifted, because the decision requires
code that does not exist.

The previous framing — *"Four of five clear by telling the truth. Only B5 needs a decision."*
([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):247, restated at
[`../../HANDOFF.md`](../../HANDOFF.md) § Publication exit criteria (`:104-105`)) — **is now wrong**, and wrong in a direction that
flatters the project: it implies B5 is one signature from being closed. It is not. B5 is now the
blocker requiring the most *engineering* of the five. Correcting those source files is not this
document's to do and is not done here; this section records that they are stale, so that nobody
reading them alongside this document mistakes their framing for the current position.

Two further consequences, recorded and not resolved:

- **The publication gate is enlarged.** A gate that was five items, four of them textual, is now
  five items of which one is a multi-part implementation with its own tests. Whether that changes
  the sequencing of Phase 0 is an owner matter and is not decided here.
- **This document cannot close B5, and neither can any drafting run.** The controls need code, and
  no run under the current standing constraints is authorised to write any. Recording the controls
  is the whole of what a document can contribute.

### 9.8 What this document does and does not do relative to B5

- It **does** record the eight controls as settled policy binding on the specification, and
  constrain how sensitive identity may be modelled given them: the governing rule, the quantity-kind
  typing, the effect-class enum and the tests in [§6](#6-bias-and-stereotype-testing) all apply, and
  now apply *with* the C5 obligation on the campaign model rather than pending a decision.
- It **does not** design the enforcement. How the loader is structured, where the world-mode gate
  sits, what the campaign factor allowlist contains, where the protected-characteristic tag lives,
  and how the interface discloses fictionality are engineering and ownership questions this document
  states requirements for and does not answer.
- It **does not** re-open, qualify or trade off any of the eight controls, and no later document in
  this set may do so without a new founder decision.

---

## 10. Dependencies, and what does not exist today

This document's safeguards rest on foundations that are unbuilt. Listed here so that no safeguard is
mistaken for something achievable on the current codebase.

- **Deterministic randomness isolation (P0.4A) — the hardest dependency.** The identity-swap tests
  ([§6.1](#61-test-class-a--counterfactual-identity-swap-invariance),
  [§6.4](#64-test-class-d--generated-narration-bias)) require that swapping one identity attribute
  changes only that attribute's declared effects. On the single shared RNG (`engine.py`:83), any
  change to draws shifts every subsequent draw
  ([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):170-175), so
  the swap cannot be isolated. **This is owned by P0.4A** (founder decision, 18 July 2026), not
  unowned as an earlier draft of this list stated; per-entity streams alone are explicitly
  insufficient, and the mechanism is unchosen. Its relationship to ADR-007, and the choice of
  mechanism, are determinism-affecting decisions requiring owner approval
  ([§11](#11-open-questions-for-the-owner)). **These tests cannot be run until P0.4A passes.**
- **P0.4 — the authoritative-state contract** ([`../../HANDOFF.md`](../../HANDOFF.md):75). Test class
  C ([§6.3](#63-test-class-c--prejudice-provenance)) scans "authoritative reality" for prejudiced
  propositions; that view is not yet defined. Until P0.4 defines what is authoritative across the
  tiers, the scan has no defined target.
- **P0.6 — events, snapshots, replay** ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order (`:87-88`)). The
  eight-question hook ([§5.5](#55-the-eight-question-hook)) and the "prejudice stored as an
  event-sourced belief" model ([§3.3](#33-prejudice-belongs-in-a-belief-record-never-in-authoritative-reality))
  depend on event-sourcing, which is unbuilt. Belief provenance is not merely unbuilt but
  unbuildable until P0.6 lands.
- **The attribute quantity-kind tagging — and the vocabulary question beneath it**
  ([§5.1](#51-every-attribute-must-carry-a-quantity-kind)). The tests cannot run unless
  [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md) and the other entity documents
  tag every attribute with a quantity kind. **No document does, and PERSON-MODEL uses a different,
  non-isomorphic scheme** (E-3 mechanism indirection, PERSON-MODEL:341-379). This is not merely
  untagged data: it is an unresolved conflict between two vocabularies, and it must be settled by the
  owner ([§11](#11-open-questions-for-the-owner) question 5) before the tagging can even begin. This
  document owns the rule; it does not own the tagging and does not own the reconciliation.
- **A bidirectional belief model** ([§5.4](#54-interpretive-frame-must-be-evidence-updatable-not-absorbing)).
  Frame effects must be evidence-updatable, which contradicts the current monotone belief ratchet
  ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.9). This is a
  precondition, not an add-on.
- **No invariant tests exist** ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md)
  §6.34). Every test in [§6](#6-bias-and-stereotype-testing) is greenfield.
- **The enforcement points the eight B5 controls attach to** ([§9.2](#92-the-eight-controls-settled-policy)).
  Added by the amendment of 19 July 2026, because the settled decision inherits every one of the
  dependencies above and adds four of its own: there is **no scenario schema at all**
  ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.13) to hold
  `world_mode`, so C2 has nothing to attach to; there is no campaign instantiation path
  (`agent_schema.py`:320-346 is instantiated nowhere, and `hidden_campaign` is loaded as a raw dict
  at `engine.py`:111 and read by nothing thereafter), so C1's gate has nothing to gate; there is no
  protected-characteristic tag or declared factor allowlist, so C5 has nothing to check; and there
  is no interface, so C7 has nowhere to disclose. **This is a statement about the size of the gap,
  not a reason to delay: the controls bind whenever those parts are built, and building any of them
  without the control is a violation of a settled decision, not a sequencing choice.**

None of these is a reason to start now. They are reasons to write the safeguards carefully so that
when the prerequisites land, the safety rules are already fixed and dated.

### 10.1 Inbound delegations this document has been assigned and does not yet discharge

Recorded because a safeguard that two documents each believe the other owns is a safeguard nobody
owns, which is the failure mode this whole document set exists to avoid. Verified against the
sibling documents as they stand on 18 July 2026. **None of the four is resolved here**, because each
requires either a numeric threshold or a test design that is an owner decision.

| Delegated by | What is delegated | Status here |
|---|---|---|
| [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md) Rule **E-3a** | The numeric bound on M17 DISCRIMINATION-EXPOSURE's identity-conditioned rate multipliers, its failing threshold and its review cadence. M17 is the compulsory indirection layer through which *all* sensitive identity reaches behaviour, so an unbounded M17 is where a stereotype switch would reappear one layer below the guard. | **Not discharged.** This document specifies no bound on M17 and does not name M17 anywhere else. Until it does, E-3a is a rule with no number. |
| [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md) Rule **E-5b** | The residual threshold, failing criteria, decomposition method and reporting format for the lifetime-differential swap test. | **Partially discharged.** [§6.1](#61-test-class-a--counterfactual-identity-swap-invariance) and [§6.2](#62-test-class-b--population-distribution-invariance) adopt the zero-unattributable-residual principle; the threshold, method and format remain open question 9. |
| [`../world-model/RELATIONSHIP-GRAPH.md`](../world-model/RELATIONSHIP-GRAPH.md) invariant **RG-3c**, guard 3 | The **compositional** test: over generated graphs, the reachable information set and action set of otherwise-matched entities must not differ systematically by group membership. RG-3c states the requirement explicitly as a requirement *on this document* and does not specify the test. | **Not discharged.** [§6](#6-bias-and-stereotype-testing)'s four test classes are per-attribute and per-population; none tests composition across a chain of individually probabilistic mechanisms, which is the precise failure RG-3c identifies. This is the most substantive gap in the set. |
| [`../world-model/ORGANISATION-MODEL.md`](../world-model/ORGANISATION-MODEL.md) §15-**R8** | A content rule gating `vulnerabilities: list[VulnerabilityRecord]` on businesses, so that modelled operational vulnerabilities remain fictional, mechanism-level and non-actionable per [`../../CHARTER.md`](../../CHARTER.md):137-138. | **Not discharged, and the reason for not discharging it has weakened.** This document addresses real-entity likeness ([§8](#8-fictional-identities-and-the-no-real-entities-rule)) but specifies no rule for operational vulnerabilities. An earlier draft deferred it as "coupled to B5 / P0.8 and not resolvable independently of it". B5 is now settled ([§9](#9-blocker-b5--the-settled-dual-use-policy-and-what-it-now-requires)) and supplies no vulnerabilities content rule, so the coupling no longer explains the gap: R8 is simply undischarged, and needs an owner decision of its own. |

---

## 11. Open questions for the owner

Recorded, not resolved. AI agents may not decide these
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138-140`)).

1. **Named RNG substreams.** Should per-entity substreams be adopted, superseding ADR-007's
   single-RNG decision? The identity-swap tests are unbuildable without them. Determinism-affecting;
   owner approval required.
2. ~~**B5 / P0.8 dual-use.**~~ **CLOSED by the founder decision of 18 July 2026.** The question
   asked whether sensitive-identity attribute detail should be held deliberately coarse until B5 was
   decided. B5 is decided ([§9](#9-blocker-b5--the-settled-dual-use-policy-and-what-it-now-requires)),
   so the question no longer has a subject: detail is bounded by the eight controls rather than by
   waiting. The number is retained rather than reused, so that cross-references from other documents
   to "question 2" resolve to this closure instead of silently pointing at a different question.
   **Note what the closure does not do:** it does not lift the blocker, because the controls are
   unbuilt ([§9.7](#97-what-the-decision-changes-about-the-publication-gate)), and it does not
   license finer identity detail than the controls permit.
3. **The `sunni-mixed` label.** Should the real-world religious label at
   `scaffold/scenarios/kestral-strait.json`:45, :85, :168, :208 be replaced with a fictional
   identity, consistent with the founder's preference ([§8](#8-fictional-identities-and-the-no-real-entities-rule))
   and CHARTER:137? Affects existing scenario data. **The B5 decision sharpens this without
   answering it:** those four cohorts are `target_cohorts` candidates, so under a broad reading of
   control C4 the shipped default scenario would not pass ([§8.4](#84-the-existing-data-tension--an-owner-decision-not-resolved-here),
   question 13).
4. **Statistical tolerance for Test class B.** What across-group difference on a capability-class or
   moral-class distribution counts as "statistically indistinguishable"? Setting the threshold is a
   safety-policy choice, not a technical default.
5. **Vocabulary reconciliation, and who owns the tagging.** Two incompatible schemes are on the
   table and neither document may choose between them unilaterally. This document specifies a
   `quantity_kind` tag on attributes plus an `effect_class` enum on edges
   ([§5.1](#51-every-attribute-must-carry-a-quantity-kind),
   [§5.2](#52-every-identitymechanism-edge-must-carry-an-effect-class)); PERSON-MODEL specifies
   E-3 indirection through named intermediate mechanisms, with permitted sets written as explicit
   mechanism lists (PERSON-MODEL:328-340). The vocabulary of this document appears in **no other
   document in the set**. The owner must decide: adopt the quantity-kind/effect-class scheme and
   require the entity documents to tag against it; drop it in favour of E-3 mechanism indirection
   and restate the safeguard in that vocabulary; or define an explicit mapping between the two. Until
   this is settled the safeguard has no data anywhere that it could validate, and every test in
   [§6](#6-bias-and-stereotype-testing) is unwritable. Also to confirm: which document owns the
   resulting assignment, and who signs off changes to it.
6. **Enforcement of CHARTER:137 — narrowed, not closed.** The disclosure half of this question is
   now settled policy: the founder decision requires a fail-closed `world_mode: fictional` gate at
   scenario load (control C2) and fictionality disclosure in the API and UI (control C7), so neither
   is an owner question any longer — only an unbuilt requirement
   ([§8.3](#83-the-enforcement-gap--narrowed-by-the-b5-decision-not-closed)). What remains open is
   the residue the decision does not mandate: **what real-entity reference check, if any, runs at
   scenario load**, and what oracle — reference list, classifier, structured review — it would use
   to decide that a name refers to a real nation, organisation or person
   ([§12](#12-features-specified-with-no-mapped-causal-mechanism) item 2).
7. **Portrait fictionality.** What enforces "clearly fictional, not resembling a real person" for
   generated portraits (source record :204-206)? No asset store exists, and automated
   face-similarity checking against real people is itself ethically fraught. Recorded as an
   unresolved enforcement gap ([§12](#12-features-specified-with-no-mapped-causal-mechanism)).
8. **Whether to write this document at all before its prerequisites land.** It can be written; none
   of it can be validated against an implementation. The owner should confirm that capturing the
   safety rules in advance is the intended trade.
9. **The residual threshold, decomposition method and reporting format for the swap tests.**
   PERSON-MODEL:406-408 delegates all four to this document, and this document does not choose them
   ([§5.4](#54-interpretive-frame-must-be-evidence-updatable-not-absorbing)). What counts as a
   non-zero unattributable residual in practice, by what method divergence is decomposed into named
   mechanism contributions, and in what form a failure is reported, are safety-policy choices rather
   than technical defaults. Note that PERSON-MODEL:385-387 explicitly *rejects* a total-variation
   magnitude bound as the control, on the ground that it would flag founder-required mechanisms as
   bias; any answer that reintroduces a magnitude bound would need to overturn that finding
   deliberately, not by accident. Until this is answered, PERSON-MODEL's rule E-5b has no threshold
   and cannot be implemented.
10. **The oracle for the narration-swap check**
    ([§6.4](#64-test-class-d--generated-narration-bias)). Comparing two generated portrayals for
    "equivalence modulo identity terms" has no specified decision procedure. If a judge model is
    contemplated, the owner should weigh the determinism-boundary implication: a model deciding a
    safety verdict exercises authority, which cuts against ADR-006. The alternatives — structured
    human review, or dropping the sub-test — are also owner choices.

**Questions 11 to 13 are new in the amendment of 19 July 2026.** They are not re-litigations of the
settled B5 decision. They are surfaces the decision creates and does not itself resolve, recorded as
questions rather than answered, because an agent may not decide them
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138-140`)).

11. **Proxy variables in campaign targeting.** Control C5 forbids optimising against protected
    characteristics; the decision expressly permits **geography** as a targeting factor; and
    [§4](#4-what-the-simulation-may-model-and-why-it-is-social-science-not-stereotype) *requires*
    residential segregation to be modelled, which makes location correlate with identity by
    construction. A district-targeted campaign can therefore optimise against a protected
    characteristic without reading one, and both C5 tests in
    [§9.6](#96-how-each-control-would-be-tested) would pass it. What test, threshold or review
    distinguishes legitimate geographic targeting from proxy targeting? Note the trap in the obvious
    answer: a correlation ceiling between a targeting factor and a protected characteristic would
    flag exactly the segregation the model is required to represent — the same failure that led
    PERSON-MODEL:385-387 to reject a magnitude bound (question 9). This is the most substantive
    unresolved question the B5 decision creates.
12. **Where the protected-characteristic tag lives, and who owns the campaign factor allowlist.**
    C5 is only checkable if every attribute declares whether it is a protected characteristic, and
    the campaign's selection and scoring inputs are a declared closed set
    ([§9.4](#94-what-the-campaign-model-may-and-may-not-optimise-against)). Neither exists in any
    document. Does the tag belong to this document, to
    [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md), or to the schema layer — and
    is it a third vocabulary alongside the two already unreconciled in question 5, or a facet of
    whichever of those wins? Answering question 5 first would avoid creating a third scheme.
13. **The scope of "real … political populations" in control C4.** Does a *fictional aggregate
    cohort carrying a real-world identity label* — `sunni-mixed` in the default scenario — count as
    a real political population that may not be an influence target? The narrow reading makes it a
    naming preference (question 3); the broad reading means the shipped default scenario fails C4
    and cannot be published as it stands. The two readings have materially different consequences
    for the publication gate, and the decision does not distinguish them.

---

## 12. Features specified with no mapped causal mechanism

The causal-value rule ([`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md);
source record :241-254) requires that every specified attribute name a mechanism that reads it, and
that anything failing the test be struck rather than dressed up as depth. This is a **safety**
document, so it deliberately specifies almost no entity attributes of its own — it specifies
*constraints on, and tests over,* attributes that the other documents define. Its own governance
features (the quantity-kind tag, the effect-class enum, Test classes A–C, the narrate-not-author
boundary) are *intended* to map to a concrete, named mechanism: a build-time validator, an invariant
test, or the existing `ActionProposal` boundary. The exceptions are listed below, and they are more
numerous than an earlier draft admitted.

The following items, however, are specified here and **cannot be honestly mapped to an automatable
causal mechanism today.** They are recorded as enforcement gaps rather than hidden, because hiding
them would be the exact fake-depth / false-assurance failure this project exists to correct.

1. **"Clearly fictional, not resembling a real person" for portraits** (source record :204-206). No
   asset store exists; no field references an asset; and automated verification that a generated face
   does not resemble a real individual is an unsolved and ethically fraught problem. This is
   specified as a *requirement* with **no mechanism that can currently enforce it**. Owner decision 7.
2. **The real-entity load check for CHARTER:137**
   ([§8.3](#83-the-enforcement-gap--narrowed-by-the-b5-decision-not-closed)). Rejecting
   names/labels that refer to real nations, organisations or people requires an oracle (a reference
   list or classifier) that does not exist in the project. The *rule* is settled; the *enforcement
   mechanism* is unspecified and non-trivial. **Unchanged by the B5 decision.** The decision
   mandates a `world_mode` gate (C2) and disclosure (C7), both of which are mechanically simple and
   neither of which is this check: a scenario can declare itself fictional, disclose that it is
   fictional, and still be populated with real referents. Owner decision 6, narrowed to this
   residue.
3. **The prohibited-construction detector in Test class D**
   ([§6.4](#64-test-class-d--generated-narration-bias)). It maps to a mechanism — a filter over
   generated text — but that mechanism is a **heuristic** with false negatives and false positives.
   It reduces risk; it cannot be claimed to guarantee absence of stereotype in generated prose, and
   must never be described as doing so.
4. **The interface provenance tag on generated text** ([§7.3](#73-output-filtering-and-provenance);
   CHARTER:141). It maps to a required interface behaviour, but there is no interface layer in the
   project today (the only state endpoint is macro-only, `routes_simulation.py` get_state), so there
   is nothing to attach it to yet. Specified; unattachable until an interface exists. Note also that
   generated text is *already* emitted untagged (`llm_gateway.py`:85-103 →
   `routes_simulation.py`:76), so this is a live gap, not only a future one
   ([§7.3](#73-output-filtering-and-provenance)).
5. **The prohibition on *transitive* identity→capability edges**
   ([§3.1](#31-the-absolute-prohibition)). The §5.2 validator is a per-edge type check and cannot
   see a multi-hop path; identity → permitted attribute → `INHERENT_CAPACITY` is legal at every
   individual hop, and nothing constrains a non-identity attribute pointing into a capability or
   moral quantity kind. Closing this would need a mechanism-graph reachability analysis that is not
   specified here and would depend on the unbuilt P0.6 provenance spine. Today the only thing that
   would catch a transitive leak is Test class A, which is itself unrunnable without named RNG
   substreams. **No automatable enforcement exists.**
6. **The causal-path condition on group-differing values**
   ([§5.3](#53-the-inherent-versus-realised-distinction),
   [§6.2](#62-test-class-b--population-distribution-invariance)). Requiring that an OPPORTUNITY or
   EXPOSURE mechanism "sit on the causal path" is a provenance property, not an edge property. The
   per-edge validator cannot evaluate it, and the attributability requirement of
   [§5.4](#54-interpretive-frame-must-be-evidence-updatable-not-absorbing) presupposes a
   decomposition method that is an open owner question (question 9). **No automatable enforcement
   exists.**
7. **The narration-swap check's equivalence oracle**
   ([§6.4](#64-test-class-d--generated-narration-bias)). Asserting that two generated portrayals are
   "equivalent modulo the identity terms" names no decision procedure. The prohibited-construction
   detector cannot perform the comparison, and no alternative is specified. This is a specified test
   with **no automatable decision procedure today**. Owner decision 10.
8. **Proxy targeting under control C5** ([§9.4](#94-what-the-campaign-model-may-and-may-not-optimise-against),
   [§9.6](#96-how-each-control-would-be-tested)). "Protected characteristics cannot be used as
   optimisation criteria" is given a checkable definition in §9.6 — a declared factor allowlist plus
   a permutation-invariance test — and that definition is **blind to proxies by construction**.
   Permuting religion while holding district fixed leaves a district-targeting campaign invariant,
   so it passes; yet segregation, which §4 requires the model to represent, makes district a proxy
   for religion. **No automatable enforcement of the control's intent exists**, only of its letter.
   Owner decision 11. New in the amendment of 19 July 2026.
9. **Control C3, "real-world scenario import remains disabled"**
   ([§9.6](#96-how-each-control-would-be-tested)). A test cannot demonstrate the absence of a
   feature. C3 is satisfied today only because no import path was ever built, and the control's
   real force is a prohibition on future work — carried by review, and indirectly by C1 and C2,
   rather than by any check. It is recorded here so that "C3 passes" is never cited as evidence of
   an enforcement mechanism, because there is none. New in the amendment of 19 July 2026.

Everything else specified in this document — the quantity-kind tag, the effect-class enum and its
per-edge validator, Test classes A, B and C, and controls C1, C2, C4 and C7 of
[§9.2](#92-the-eight-controls-settled-policy) — maps to a named mechanism (a build-time validator, a
loader check, a structural type constraint, a response-schema assertion, or an invariant test).
Those mechanisms are all **unbuilt**, and several are **unbuildable** until
the prerequisites in [§10](#10-dependencies-and-what-does-not-exist-today) land, but each has a
defined reader. They are not in the list above because the failure the list guards against is
*specifying a feature with no possible mechanism*, not *specifying a mechanism that is not yet
built*.

**One qualification on that claim, which an earlier draft omitted.** "Has a defined reader" is
weaker than it sounds while open question 5 is unresolved. The quantity-kind tag and the
effect-class enum have a defined *validator*, but no document currently tags any attribute against
them, and PERSON-MODEL uses an incompatible scheme
([§5.1](#51-every-attribute-must-carry-a-quantity-kind)). A validator with no tagged data to read is
closer to the fake-depth failure this section guards against than the paragraph above implies. It is
left out of the list because the defect is repairable by an owner decision rather than intrinsic —
but it should not be read as a clean mapping today.

---

## 13. Related documents

- [`../world-model/FOUNDER-REQUIREMENT-2026-07-18.md`](../world-model/FOUNDER-REQUIREMENT-2026-07-18.md)
  — the source record. The governing rule ([§2](#2-the-governing-design-rule)) and the permitted /
  prohibited lists are drawn from it; where this document and it disagree, it wins.
- [`../../CHARTER.md`](../../CHARTER.md) — the determinism boundary (ADR-006), the eight-question
  standard, and the no-real-entities rule (:137) that [§8](#8-fictional-identities-and-the-no-real-entities-rule)
  builds on.
- [`../../HANDOFF.md`](../../HANDOFF.md) — Phase 0 order and standing constraints. **Stale on B5:**
  § Phase 0 priority order, P0.8 (`:90`) and § Publication exit criteria (`:104-105`) predate the founder decision of 18 July 2026 and still present B5 as an open
  owner decision that would clear by being taken. [§9](#9-blocker-b5--the-settled-dual-use-policy-and-what-it-now-requires)
  governs on that point; correcting `HANDOFF.md` is not this document's to do.
- [`../world-model/ENTITY-ONTOLOGY.md`](../world-model/ENTITY-ONTOLOGY.md) — the common ontology and
  the four-view model; the quantity-kind tag in
  [§5.1](#51-every-attribute-must-carry-a-quantity-kind) is specified to sit on top of its attribute
  base, and the causal-value rule is shared with it.
- [`../world-model/PERSON-MODEL.md`](../world-model/PERSON-MODEL.md) — the person-level,
  minority-inclusive identity that replaces the majority-label aggregate; the source of rule E-3
  (mechanism indirection, :341-379) and the E-5 swap tests (:388-424), which delegate their residual
  threshold and reporting format to this document. It does **not** currently tag attributes with
  this document's quantity kinds, and its scheme is not isomorphic to them; reconciling the two is
  open question 5.
- [`../world-model/ORGANISATION-MODEL.md`](../world-model/ORGANISATION-MODEL.md) — country and
  organisation entities that read the OPPORTUNITY effects of political representation and religious
  institutions.
- [`../world-model/RELATIONSHIP-GRAPH.md`](../world-model/RELATIONSHIP-GRAPH.md) — the directional,
  historied edges through which NETWORK POSITION and social-trust effects flow.
- [`../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`](../world-model/BELIEF-AND-KNOWLEDGE-MODEL.md) —
  where prejudice-as-belief is stored with provenance and truth status, and where INTERPRETIVE FRAME
  effects set evidence-updatable priors.
- [`../world-model/POPULATION-FIDELITY.md`](../world-model/POPULATION-FIDELITY.md) — the tier system,
  materialisation and the population-level form of the distribution test.
- [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) — the
  role-scoped dossier and confidence labels under which a prejudiced belief surfaces to the player as
  a belief, never as fact.
- [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) and
  [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) — the closed
  audit; cited for §5.9 (belief ratchet), §5.10 (the 63× silent error), §6.34 (no invariant tests),
  and A3 §6 (shared-RNG contamination). Not modified by this document.
