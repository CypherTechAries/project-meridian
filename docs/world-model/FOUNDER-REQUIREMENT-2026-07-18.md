# Founder requirement — simulated society and the entity model

**Recorded:** 18 July 2026
**Status:** Founder decision. Source record.
**Disposition:** Backlog. **Does not interrupt Phase 0 remediation.** Must be captured before the
replacement simulation architecture is designed.

This document preserves the founder's requirement statement verbatim. The eight specification
documents listed at the end derive from it. Where a derived document and this record disagree,
this record is the source and the derived document is wrong.

**Nothing described in this document is implemented.** It is a specification of intent for a
future architecture, recorded so that the intent is explicit and dated. See
[`../delivery/CAPABILITY-CLAIMS.md`](../delivery/CAPABILITY-CLAIMS.md) for what may and may not
currently be claimed about MERIDIAN.

---

## Verbatim requirement

This should be treated as a **core world-model requirement**, not as optional character flavour.

The important refinement is:

> Every consequential person, organisation, business, community, institution and state should be a
> persistent entity with an identity, history, relationships, beliefs, capabilities and changing
> circumstances.

But the profile displayed to the player should not necessarily reveal everything the simulation knows.

### "Simulated" versus "synthetic"

For public-facing language, **simulated society** is probably clearer.

"Artificial society" or "synthetic society" can sound as though the world is merely generated
content. What you are describing is deeper: a persistent society in which entities have histories,
incentives and relationships that causally affect what happens.

Internally, terms such as **synthetic population**, **synthetic agent** and **synthetic data** can
still be technically useful.

---

## The entity model

Every entity should have a stable identity and a structured record. The LLM can turn that record
into readable biographies, briefings and conversations, but it must not invent or silently modify
the authoritative facts.

### A person

A detailed person record might contain:

**Identity** — name and aliases; age and date of birth; place of birth; current residence;
citizenship and nationality; ethnic, cultural and religious identities; languages and proficiency;
family and household; physical appearance; portrait or avatar; publicly known identity versus
concealed identity.

**Life history** — childhood environment; family wealth and social class; education; military or
public service; employment history; migration and travel history; significant achievements;
traumatic experiences; criminal or disciplinary history; political involvement; previous crises
they experienced.

**Psychology and worldview** — values; political beliefs; religious commitment; risk tolerance;
need for status or recognition; empathy; loyalty; ambition; patience; susceptibility to pressure;
attitude toward authority; attitude toward violence; trust in institutions; perceived grievances;
personal fears; long-term aspirations; immediate objectives.

**Capabilities** — education and expertise; leadership ability; negotiation skill; languages;
social influence; financial resources; access to institutions; security clearance; military or
technical skills; media reach; physical health; dependents and personal obligations.

**Relationships** — family; friends; rivals; mentors; employers; political patrons; financial
dependencies; romantic relationships; professional contacts; trusted sources; people they distrust;
people to whom they owe favours; people who owe them favours.

Relationships should have direction and history. "A trusts B" does not imply that B trusts A.

A relationship could include: trust; affection; fear; respect; dependency; ideological alignment;
resentment; familiarity; leverage; shared history; last interaction; important unresolved events.

**Current state** (changes during the simulation) — location; health; stress; fatigue; financial
pressure; confidence; loyalty; current intentions; knowledge; beliefs; rumours they have heard;
people they recently contacted; current role; available resources; public reputation; private
reputation; exposure to danger.

A person's biography should influence their behaviour, but it should not mechanically determine it.

A religious person should not automatically behave in a particular political way. A wealthy person
should not automatically be conservative, selfish or calm. Identity changes probabilities, social
connections and lived experience — it should not become a stereotype switch.

---

## Other entity types need equivalent depth

### Organisations

Founding history; legal status; public mission; actual priorities; leadership; internal factions;
organisational culture; membership; recruitment methods; funding; assets; capabilities; geographic
presence; decision-making process; dependencies; rivals and partners; reputation; legal exposure;
current strategy; institutional memory; internal disputes; cohesion and morale.

An organisation should not behave like one person. Different departments and factions should disagree.

For example, a shipping company could contain: a chief executive concerned about reputation; an
operations division concerned about vessel safety; insurers concerned about financial exposure;
lawyers concerned about liability; investors concerned about share price; crew unions concerned
about worker protection; regional managers with local political relationships.

The company's action should emerge from those pressures.

### Countries

Historical development; political system; constitution and legal framework; government institutions;
parties and factions; regions and local authorities; population groups; languages and religions;
economic structure; class structure; major industries; infrastructure; military and security forces;
media environment; alliances; rivalries; historical grievances; national myths; current public
sentiment; government legitimacy; elite cohesion; state capacity; international reputation.

The "country" should not be a single agent. The government, public, military, courts, businesses and
regional authorities may all react differently.

### Businesses

Ownership and shareholders; board members; executives; revenue sources; debt; workforce; supply
chain; facilities; customers; competitors; regulatory obligations; political relationships; labour
relations; insurance exposure; reputation; market confidence; operational vulnerabilities.

### Communities and population groups

Population size; geography; age structure; employment; income distribution; education; languages;
cultural identities; religious participation; political tendencies; media consumption; social
networks; historical experiences; institutional trust; grievances; important local leaders;
vulnerability to disruption; current concerns.

Population weighting is essential. A group of 20,000 people should not automatically exert the same
aggregate influence as a group of two million, although a small group may have disproportionate
influence through wealth, organisation, strategic position or political access.

---

## The profile is not the same as ground truth

This may be the most important design point.

There should be at least four different versions of an entity's profile:

**Authoritative reality** — what is actually true in the simulation. The player may never see all of this.

**The entity's self-understanding** — what the person or organisation believes about itself. A
politician may genuinely think they are acting patriotically while the public views them as opportunistic.

**Public profile** — what is publicly reported or commonly believed. This may contain propaganda,
errors, omissions and outdated information.

**Player intelligence profile** — what the player's role currently knows or assesses. This should
distinguish: **Confirmed · Reported · Assessed · Disputed · Unknown · Possibly deceptive · Outdated
· Restricted**.

A prime minister might see a security assessment that ordinary players cannot. A journalist might
see sources and public records. A business leader might know market relationships but not classified
intelligence.

The profile interface therefore becomes an intelligence product, not an omniscient encyclopaedia.

---

## What the player should see

Clicking an entity should open a structured dossier. For a person:

1. **Overview** — role, location, status, portrait and current relevance.
2. **Biography** — life history and career.
3. **Motivations** — goals, fears, values and pressures.
4. **Relationships** — interactive social graph.
5. **Beliefs and knowledge** — what they currently believe and why.
6. **Activity** — recent movements, communications and decisions.
7. **Resources and capabilities** — what they can actually do.
8. **Public perception** — sentiment by community, country or platform.
9. **Intelligence assessment** — confidence, sources and contradictions.
10. **Timeline** — every important interaction and state-changing event.

For a business, country or organisation, the tabs would change appropriately.

Profiles should support questions such as: "Why does this minister oppose the operation?" · "Who
influences this chief executive?" · "Which communities trust this media outlet?" · "What caused this
organisation to radicalise?" · "Who benefits financially if the strait closes?" · "What does this
person believe that is factually wrong?" · "How did these two individuals come to distrust one another?"

---

## Faces and visual identity

Faces would add significant emotional connection and help players remember people.

A sensible progression is: abstract avatars during early development; consistent illustrated
portraits; generated fictional faces with multiple expressions or context states; more sophisticated
visual changes for age, injury, role and circumstance.

Each generated person should have a stable visual identity. Their portrait should not randomly change
between sessions.

The asset should be: generated once from a stable entity specification; stored and versioned; clearly
fictional; not derived from or intentionally resembling a real person; accompanied by provenance and
generation metadata; consistent with age, geography, family resemblance and life history.

Portraits are presentation. The underlying identity must still be structured data.

---

## The scale problem

It is not practical — or necessary — to simulate millions of people at identical granularity every
tick. MERIDIAN needs **fidelity tiers**.

**Tier 1: focal individuals** — cabinet members, commanders, executives, journalists, activists,
family representatives, militia leaders and other directly consequential actors. Full biographies,
relationships, memories, beliefs, portraits and individual decision models.

**Tier 2: named secondary individuals** — local officials, employees, relatives, experts and
influential citizens. Substantial profiles but less expensive continuous simulation.

**Tier 3: households and local networks** — families, workplaces, neighbourhood groups and
professional networks. Behaviour partly aggregated while retaining named representatives.

**Tier 4: population cohorts** — large background populations represented statistically through
geography, demographics, values, economic exposure, social networks and sentiment.

**Promotion between tiers.** A background person may become important because they: record a viral
video; become the relative of a hostage; organise a protest; leak information; witness a military
operation; become a political candidate; gain a large online following.

At that point, the system can deterministically expand them into a more detailed individual.

Once materialised, their identity and history must remain stable. The system cannot regenerate an
entirely different biography later.

---

## Granularity must have causal value

There is a danger of producing enormous biographies that never affect the simulation. That would be
fake depth.

Each important profile attribute should connect to one or more mechanisms. For example:

```text
Childhood in an economically marginalised port town
→ stronger personal identification with maritime workers
→ greater trust in the port union
→ greater sensitivity to shipping job losses
→ different response to a government blockade
```

```text
Elite foreign education
→ international professional network
→ access to foreign officials and investors
→ different information sources
→ different perception of sanctions risk
```

```text
Previous experience surviving political violence
→ heightened threat sensitivity
→ preference for rapid security measures
→ lower tolerance for uncertain intelligence
```

These should influence behaviour probabilistically. They should not force a single predetermined choice.

---

## History should be event-sourced

Every important entity needs a persistent history. An entity's current state should be explainable
through recorded events:

```text
Event: factory closes
→ household income falls
→ economic insecurity rises
→ trust in government falls
→ anti-government narrative becomes more credible
→ protest participation becomes more likely
```

The system should be able to answer: What changed? · When did it change? · What caused it? · What
evidence did the entity observe? · Which prior experiences shaped the reaction? · What alternative
reactions were possible?

The LLM can explain this history conversationally, but the causal chain must come from recorded
simulation state.

---

## Sensitive identity attributes

Race, ethnicity, religion, gender, class and nationality can matter because real societies organise
power, identity and experience around them. But they must be modelled carefully.

The design rule should be:

> Sensitive identity affects social experience, networks, exposure, discrimination, solidarity and
> cultural interpretation — not inherent competence, morality or intelligence.

The simulation should avoid statements such as: members of religion X are inherently more aggressive;
ethnic group Y is naturally less educated; nationality Z is inherently untrustworthy.

Instead, it can model: historical exclusion; unequal access to education; residential segregation;
language barriers; social trust; family networks; discrimination; political representation; religious
institutions; shared historical memory; different media environments.

Because the world is fictional, fictional cultural, ethnic and religious identities may be preferable
for the default scenario, while the mechanisms remain grounded in real social science.

---

## What this changes architecturally

This requires more than adding columns to an `agents` table. MERIDIAN needs:

a common entity ontology; type-specific schemas; a temporal relationship graph; a belief and knowledge
model; a biography and life-event system; role-based visibility; source and confidence tracking;
population weighting; deterministic profile generation; entity promotion and demotion rules;
event-sourced state changes; persistent portrait and asset references; bias and stereotype testing.

A useful foundational rule is:

> Every entity can act, be acted upon, hold beliefs, participate in relationships, possess resources,
> experience events and be perceived differently by different observers.

Not every entity needs every capability, but the ontology should support them consistently.

---

## What should be specified now

This should not interrupt Phase 0 remediation, but it must be captured before the replacement
simulation architecture is designed.

Add these documents to the product and architecture backlog:

- `docs/world-model/ENTITY-ONTOLOGY.md`
- `docs/world-model/PERSON-MODEL.md`
- `docs/world-model/ORGANISATION-MODEL.md`
- `docs/world-model/RELATIONSHIP-GRAPH.md`
- `docs/world-model/BELIEF-AND-KNOWLEDGE-MODEL.md`
- `docs/world-model/POPULATION-FIDELITY.md`
- `docs/design/ENTITY-PROFILE-EXPERIENCE.md`
- `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md`

## The canonical requirement statement

> MERIDIAN will represent consequential people, organisations, businesses, communities, institutions
> and states as persistent simulated entities. Each entity will have a type-appropriate identity,
> history, motivations, relationships, capabilities, beliefs, resources and evolving state. Profiles
> will expose information according to player role, evidence and confidence rather than revealing
> omniscient ground truth. Profile details must influence simulation behaviour through explicit causal
> mechanisms and must not exist solely as generated narrative.

That is the level of granularity required for the game to feel like a living world rather than a
sequence of crisis prompts.
