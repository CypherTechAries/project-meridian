# Real Geography, Fictional Worlds

**Status: RESEARCH — nothing here is implemented**
**Written 21 July 2026, against `main` at `38e81b7`**

---

## The practical choice

> **Do we need to build a fictional planet, or can we use real geography safely?**

MERIDIAN's current map is invented. It failed its first cold usability test: a first-time reader
found it artificial and could not say what it meant. That leaves three ways forward — draw a better
fictional map, use the real world, or stop drawing maps.

**The recommendation is: use real physical geography, keep every society fictional, and support
fictional and abstract maps as first-class alternatives rather than fallbacks.**

The short reason is cost and legibility. Inventing a coastline means inventing everything that
follows from it — distances, sailing times, which towns depend on which port, why the alternative
route is worse. All of that has to be authored, kept consistent, and then explained to the reader.
Real geography supplies it for free and the reader already knows how to read it. A person looking at
a real strait does not need to be told that going around the long way takes longer.

The long reason is that the honesty problem gets *easier*, not harder, if the boundary is drawn in
the right place. A fictional map invites the reader to trust everything on it, because nothing
contradicts them. A real map invites the reader to trust the geography — which is trustworthy — and
forces us to say clearly that the people are not. That is a sharper, more defensible line than the
one we have now.

**The danger is real and it runs the other way.** A real map makes the simulation feel more
authoritative than it is. Someone who sees a real coastline may reasonably conclude MERIDIAN is
forecasting what will happen there. That is the risk this whole document is organised around.

---

## 1 · The core principle

> ## GEOGRAPHICALLY REAL, INSTITUTIONALLY FICTIONAL

The physical environment may correspond to real geography. The simulated society — its actors,
institutions, events and outcomes — remains fictional.

**A scenario using real geography must never imply that MERIDIAN is predicting the real people,
government or organisations associated with that location.**

| Real | Fictional |
|---|---|
| Coastlines and terrain | Countries and jurisdictions |
| Distances and travel times | Governments |
| Transport networks | Organisations and companies |
| Ports, airports, waterways | People and communities |
| Physical constraints | Politics and economic conditions |
| | Events, decisions and outcomes |

The line is drawn where it is because of what each side can be checked against. Geography can be
verified against the world. A fictional government cannot be verified against anything, which is
precisely why it must never be attached to a real one.

---

## 2 · The four options, compared honestly

### Option 1 — Entirely fictional maps and geography

**For.** No licensing. No real place to be confused with. No political sensitivity. Total authoring
freedom. It is what MERIDIAN does today.

**Against.** Everything must be invented and kept coherent — and *this is the option that already
failed a usability test*. An invented coastline carries no intuition: the reader cannot tell whether
a route is long, whether a port matters, or whether a detour is expensive, because they have no
prior knowledge to bring. Every fact has to be stated in words, which is how you end up with a
decorative diagram nobody can read in five seconds.

There is also a quieter cost. A fictional map cannot be wrong, so it cannot be *checked* — and a
picture that cannot be checked is difficult to keep honest.

### Option 2 — Real geography with fictional societies

**For.** Immediate comprehension. Real distances and travel times. Real physical constraints that
the reader already understands. No world-rendering engine to build. Scenario authoring gets far
cheaper — you select an area instead of inventing one. Supply chains and infrastructure become
easy to express because the infrastructure is already there.

**Against.** The false-authority problem, which is severe and is the reason this is not an
unqualified recommendation. Real communities may feel represented or accused. Real borders and
infrastructure change, so a scenario silently ages. Map data contains errors. Licensing obligations
attach. Some locations are sensitive and some should be off-limits entirely.

### Option 3 — Support both

**For.** Different scenarios have genuinely different needs, and the choice is not stylistic. A
logistics disruption wants real ports and real distances. A politically sensitive scenario wants
nothing recognisable. A training exercise may want an abstract diagram precisely because it is
abstract. Supporting both means the geography mode becomes a **declared property of the scenario**
rather than a property of the software — which is also what makes it possible to state, per
scenario, what is real and what is not.

**Against.** More to build and more to test than picking one. Two rendering paths risk diverging.
Mitigated by the fact that both paths draw the same shapes from the same data structure; only the
source of the geometry differs.

### Option 4 — Abstract geography generated from real physical constraints

Take real distances, travel times and connectivity, and render them as a schematic — a transit-map
diagram rather than a coastline.

**For.** Keeps the physical truth that matters (this is far from that; this route is the only
alternative) while discarding the visual realism that causes false authority. Often *more* legible
than a real map: this is why transit maps beat street maps for the one question they answer.
No licensing on the rendered output, because the output is not a map of anywhere.

**Against.** Unfamiliar. Loses the intuition that makes real geography valuable in the first place —
a schematic strait is nearly as inert as an invented one. Needs real data underneath anyway, so it
does not avoid the data question, only the rendering question.

### The recommendation

**Option 3, with Option 2 as the default and Option 4 as a genuine tool rather than a curiosity.**

The task asked whether the evidence supports Option 3 being strongest. It does, but with one
correction worth stating plainly: **the strongest single argument for Option 3 is not flexibility,
it is honesty.** If geography mode is a declared per-scenario property, then every scenario must
state which mode it is in — and a scenario that cannot answer "is this a real place?" cannot be
published. Picking one mode globally would remove that forcing function.

The correction to the founder's framing: Option 4 deserves more weight than "supported where
needed". For the Kestral Strait specifically, an abstract diagram may beat a real basemap on the
only test that matters — five-second comprehension — because it can show *the blocked route, the
long way round, and the affected ports* with nothing else on the screen. See
[KESTRAL-STRAIT-MAP-DIRECTION](../design/KESTRAL-STRAIT-MAP-DIRECTION.md).

---

## 3 · Geography modes

Four declared modes. Every scenario is in exactly one, and says so.

### A · REAL GEOGRAPHY / FICTIONAL SOCIETY

Real terrain, real infrastructure, real names. Fictional actors and institutions.

*Example: a fictional port authority and a fictional national government operating across a real,
named coastal region.*

- **Benefits** — maximum comprehension; nothing to invent; the reader's own knowledge does the work.
- **Risks** — **highest false-authority risk of any mode.** A named real place plus a fictional
  crisis reads as a forecast about that place. Real institutions exist at those coordinates and have
  not consented to being the setting.
- **Users** — logistics and infrastructure analysis, where the physical facts are the point.
- **Authoring difficulty** — lowest.
- **Visual requirements** — real basemap, labelled.
- **Must disclose** — the real location by name; that all actors are fictional; that it is not a
  forecast about that location; map data source, version and licence.

### B · REAL GEOGRAPHY / RENAMED LOCATIONS

Real terrain and routes; displayed place names replaced with fictional ones. **This is the mode the
founder proposed for Kestral, and it needs a caveat.**

**What renaming does not hide.** Coastline shape is among the most recognisable data in the world.
Anyone with local knowledge, and any reverse-image search, will identify a distinctive strait
immediately. Renaming also does not hide: the shape of the landmass; relative positions of ports;
road and rail topology; island configuration; latitude implied by scale bars or projection; and
anything else geometric.

**So renaming is a courtesy, not a control.** It signals "we are not talking about you". It does not
prevent identification, and a scenario must not be planned as though it does. If a location is
sensitive enough that identification would cause harm, **renaming is not the answer — Mode D is.**

- **Benefits** — real physical realism without dragging a named community into a fictional crisis.
- **Risks** — false confidence in the anonymity; readers who *do* recognise it may conclude the
  renaming was an attempt to disguise a real claim, which is worse than not renaming.
- **Users** — most general scenarios.
- **Authoring difficulty** — low; a name-substitution layer over real data.
- **Visual requirements** — real geometry, fictional labels, no real labels leaking from the basemap.
- **Must disclose** — that names are fictional; **that the underlying geography is real and may be
  recognisable**; the real source region, unless there is a specific reason not to state it — and
  that reason should itself be examined.

### C · REAL GEOGRAPHY / ALTERED INFRASTRUCTURE

Real terrain as a base; ports, roads, borders or infrastructure modified for the scenario.

- **Benefits** — real physical constraints with the freedom to place a chokepoint where the scenario
  needs one; avoids implying a real facility failed.
- **Risks** — **the most confusing mode for a reader**, because part of what they see is checkable
  and part is not, and nothing on the screen distinguishes them. Alterations must be visually
  marked, not merely declared in a manifest.
- **Users** — infrastructure-disruption and contingency scenarios.
- **Authoring difficulty** — high; every alteration must be recorded and rendered as altered.
- **Visual requirements** — a distinct treatment for altered features. Not colour alone.
- **Must disclose** — every alteration, individually, in the manifest and on the map.

### D · FULLY FICTIONAL GEOGRAPHY

Invented terrain. What MERIDIAN has today.

- **Benefits** — no licensing, no real place, no sensitivity, total freedom. **The correct choice
  wherever a real location would create unwanted assumptions or genuine harm** — and the only
  honest choice for a scenario resembling an active conflict.
- **Risks** — the comprehension problem that started this work. An invented map has to earn every
  bit of understanding it delivers.
- **Users** — training exercises where fiction is the point; politically sensitive subject matter.
- **Authoring difficulty** — highest, if done well.
- **Visual requirements** — must pass the five-second test on its own merits, with no help from the
  reader's prior knowledge. This is hard, and we have already failed it once.
- **Must disclose** — that the geography is invented and corresponds to nowhere.

---

## 4 · Where real geography helps, and where it does not

**Helps:**

- **Crisis simulation and decision support** — the physical constraints are load-bearing.
- **Training and exercises** — real terrain makes an exercise recognisable to people who work in it,
  and this is the use where fiction is *expected*, so the truth boundary is least fraught.
- **Logistics and supply chains** — this is the strongest fit. Distance, route and capacity are the
  whole subject.
- **Infrastructure disruption** — likewise, though Mode C's marking problem applies.
- **Emergency planning** — real road networks and real travel times are exactly the value.
- **Adaptive futures** — only indirectly. Real geography constrains what varies; it does not help
  with the dispersion question, which is that strand's actual blocker.

**Does not help, or actively hurts:**

- **Simulation-born fictional characters** — a person has no coordinates worth modelling, and
  putting fictional individuals at real addresses is a serious risk, not a feature.
- **Abstract organisational experiments** — geography is noise.
- **Politically sensitive modelling** — real geography makes this worse, not better. Mode D.
- **Any claim of real-world prediction** — real geography is the single strongest driver of that
  misreading, and nothing in this document reduces it to zero.

---

## 5 · What must never be claimed

- That a scenario **predicts** anything about the real location, its government, its institutions or
  its people.
- That real geography makes the **simulation** more accurate. It makes the *stage* accurate. The
  behaviour on the stage is exactly as invented as it was before, and rendering it on a real
  coastline does not add a single unit of validity.
- That renaming makes a location **unidentifiable**.
- That MERIDIAN holds real-world **operational** information of any kind.
- That any real organisation, official or resident is represented, consulted or implicated.

---

## 6 · Real-world data boundary

Four categories, in strict order of risk. **The first implementation uses only the first.**

| Category | Examples | Position |
|---|---|---|
| **1 · Static geographic data** | Coastlines, terrain, roads, ports, borders | **The only category permitted in a first implementation.** Changes slowly, is checkable, is not about anyone. |
| **2 · Changing public data** | Weather, traffic, port status, infrastructure notices | **Not now.** Introduces a live dependency and a freshness obligation, and starts to blur simulated with observed. |
| **3 · Operational data** | Live positions, detections, security events | **Never in MERIDIAN.** This is a different product with different obligations. |
| **4 · Real people and organisations** | Identifiable actors, behaviour, relationships | **Never.** Explicitly prohibited by the standing constraints and by the fiction boundary. |

**Live data must not be the starting point**, and is not recommended as a second step either. Any
future real-world feed would require, before a line of code: a declared source; a timestamp on every
value; a licence; a validation method; a privacy review; a declared scenario boundary; and a visible
distinction between *simulated* and *observed* on every surface that shows both.

The last of those is the hard one. Once a screen shows both a simulated value and an observed one,
every honesty guarantee MERIDIAN currently makes has to be re-established from scratch.

---

## 7 · Sensitive geography

Some places should not be used, and some should be used only with care.

| Category | Control |
|---|---|
| Military sites | Exclude. Do not render, do not annotate, do not use as a scenario focus. |
| Critical national infrastructure | Generalise or fictionalise. Never depict a specific facility failing. |
| Prisons, shelters, refuges | Exclude entirely. |
| Vulnerable communities | Exclude as a scenario subject. |
| Disputed borders | Mode D, or explicit neutral treatment with the dispute stated. Note that Natural Earth uses *de facto* control and says so — that is a declared editorial position, not a neutral fact. |
| Active conflicts | **Do not use.** No renaming makes this acceptable. |
| Indigenous land | Do not use without consultation, which is out of scope. |
| Private property | Never at parcel level. |
| Personal addresses | **Never, at any resolution.** |
| Commercially sensitive facilities | Generalise. |

**Proposed controls:**

1. **Scenario-location review** — a written check before any real area is adopted, recorded in the
   manifest.
2. **Restricted layer categories** — some feature classes never render, regardless of the source
   data offering them.
3. **Location generalisation** — a declared minimum resolution; nothing renders below it.
4. **Fictionalisation** — Mode D as the standing answer to sensitivity, not renaming.
5. **Redaction** — the ability to remove a feature and *say that it was removed*.
6. **Human approval** — no scenario adopts a real location without a named person approving it.
7. **No precise real-person locations, ever.**

---

## 8 · Future engine direction — explicitly not current product

**CURRENT PRODUCT: none of this exists.** MERIDIAN's engine has no concept of space. Nothing in the
ten-stage causal chain reads a distance, a route or a location. The map is a picture drawn beside
the numbers; it does not feed them. **Nothing in this section is implemented and nothing is added by
this PR.**

**FUTURE ENGINE DIRECTION.** If geography were to become causal, the plausible mechanisms are: route
length; travel time; terrain accessibility; port capacity; road bottlenecks; alternative-route
availability; proximity; region membership; weather exposure; infrastructure dependency;
communication range; and supply-chain movement.

Two warnings about that future, both learned from the strands already researched:

- **Geographic detail is not geographic validity.** A model that computes real sailing times around
  a real cape is still a model whose coefficients are invented. Precision in one input does not
  propagate accuracy to the output, and a real distance will make an invented rule *look* calibrated.
- **This would need named RNG substreams first**, for the same reason the Adaptive Futures Engine
  does: adding draws in a spatial subsystem currently shifts every later draw everywhere else.

---

## 9 · The smallest safe first proof

**One question:** *can a first-time user understand the physical crisis in five seconds?*

- One real geographic base area, **not politically sensitive**.
- Fictional displayed place names (Mode B), with the underlying region declared.
- **No live data.** No real people. No real organisations.
- Exactly five things drawn: the blocked route, the alternative route, two or three affected ports
  or regions, and nothing else.
- A plain legend in ordinary words.
- A persistent fictional-scenario disclosure.
- The **same Kestral scenario state** the engine already produces.
- **No engine changes.**

**Do not build it in this PR.** And before any map code is written, produce the clean-room
implementation plan — see [CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN](../design/CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN.md).

**A "no" is a useful result.** If a real basemap does not beat the current diagram on the
five-second test, that is worth knowing before building a mapping stack, and it points at Option 4.

---

## 10 · Relationship to the existing map issue

[Issue #30 — Redesign the Kestral Strait map for five-second comprehension](https://github.com/CypherTechAries/project-meridian/issues/30)
remains open and is **not** closed by this research.

**How it should eventually be resolved:** most likely a **real basemap under fictional names**
(Mode B), because that is the cheapest route to the comprehension the issue demands. But the issue's
acceptance test is about comprehension, not about basemaps, and **an abstract diagram (Option 4) may
pass it more cheaply and with fewer obligations.** The two should be prototyped against each other
before either is committed to. A simplified fictional map — a better version of what exists — is the
weakest of the three and should only win if both others fail.

---

## Companion documents

- [Mapping stack and data sources](MAPPING-STACK-AND-DATA-SOURCES.md) — libraries, data, tiles, licences, deployment
- [FORSYTE map reuse assessment](FORSYTE-MAP-REUSE-ASSESSMENT.md) — **conclusion: no code reuse is possible**
- [Real-geography risk register](REAL-GEOGRAPHY-RISK-REGISTER.md)
- [Scenario Geography Manifest](../design/SCENARIO-GEOGRAPHY-MANIFEST.md) — the declared fiction boundary
- [Kestral Strait map direction](../design/KESTRAL-STRAIT-MAP-DIRECTION.md) — three candidate treatments
- [Clean-room map implementation plan](../design/CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN.md)
- [Use case: Real-Geography Scenarios](../use-cases/REAL-GEOGRAPHY-SCENARIOS.md)
