# Kestral Strait — Map Direction

**Status: DESIGN — nothing built. Issue [#30](https://github.com/CypherTechAries/project-meridian/issues/30) remains open.**
**Written 21 July 2026.**

---

## The test the map has to pass

A first-time reader, given five seconds, must be able to answer:

1. **What is blocked?**
2. **Who is affected?**
3. **Where is pressure building?**
4. **What trade-offs are visible?**
5. **What changed over time?**

*(These supersede the earlier list — blocked route / rerouted route / affected ports / legend /
framing — which is still the wording in [issue #30](https://github.com/CypherTechAries/project-meridian/issues/30).)*

### What the engine can actually answer

Checked against `scaffold/scenarios/kestral-strait.json` and the projection, 21 July 2026.
**The engine has no spatial model.** There is no latitude, longitude, coordinate or geometry
anywhere in the scenario or the engine.

- **There are no port entities.** "Ports" exist only as `port_activity_deficit` — a *single scalar*.
- `political_pressure` is likewise **one scalar**, with no location and no spatial distribution.
- Cohorts carry a `region` **string** (`capital-metro`, `north-strait-coast`, `central-highlands`,
  `distributed`) — declared scenario data that **no code currently reads**.
- The existing map's place names, **"Northshore" and "Southport", are hard-coded in
  `briefing-viz.ts`** — the current map labels places the scenario does not define.

| Question | Answerable from the engine? |
|---|---|
| 1 · What is blocked? | **Yes** — the incident and `rerouting_level`. |
| 2 · Who is affected? | **Partly.** Cohorts exist with employment and household pressure. *Placing* them needs the unread `region` field. |
| 3 · Where is pressure building? | **No — not spatially.** One scalar for the whole scenario. **Drawing it at a location would invent data.** |
| 4 · What trade-offs are visible? | **Yes**, from the government options — but they are not spatial at all. |
| 5 · What changed over time? | **Yes** — the 20-tick trajectory exists. The current map shows one moment. |

**Two of the five are not spatial questions, and one has no spatial answer.** So what is needed is a
**situation diagram, not a map**: it may arrange elements by *relationship* — blockade → shipping →
ports → coastal groups → government — rather than by location. A schematic may show pressure flowing
*toward* the government without claiming the government sits at a place.

**Do not invent a spatial distribution for a scalar.** That is exactly the "no simulated detail
merely to make the screen look sophisticated" rule, and it is the strongest argument yet for
candidate C below.

The current map answers none of them. It was found artificial and unhelpful in the first cold
usability test, and it is now hidden behind a control with a stated limitation.

**Three rules, from the founder, that constrain every candidate:**
no decorative points · no meaningless network lines · no simulated detail added to look sophisticated.

---

## Candidate A — Real coastline, fictional display names

**Real:** coastline geometry, relative positions, distances, the physical fact that the alternative
route is longer.
**Fictional:** every place name, the countries, the government, the ports as institutions, all
actors and events.

**What the user sees.** A recognisable-looking strait with invented labels. Two routes: one crossed
out, one going the long way round. Two or three labelled ports.

**Assumptions they may make.** That the place is real and identifiable — **and if the underlying
region is distinctive, they will be right.** Some readers will reverse-image-search it. A reader
with local knowledge may conclude the renaming was concealment.

**Five-second test:** **strong.** The reader's existing intuition does the work — they already know
that going around a landmass takes longer, without being told.

**Cost:** a geodata pipeline, a projection, a rendering path. The smallest real version is a Natural
Earth extract rendered through `d3-geo` as SVG paths.

---

## Candidate B — Real coastline, altered ports and borders

**Real:** base terrain and coastline.
**Fictional:** names, plus modified port locations, modified borders, possibly an invented chokepoint.

**What the user sees.** The same as A, but with infrastructure placed where the scenario needs it.

**Assumptions they may make.** **The worst of the three.** Part of what they see is checkable and
part is not, and nothing on the screen distinguishes them. A reader who verifies one real feature
will extend that trust to the invented ones.

**Five-second test:** **good**, comparable to A.

**Cost:** highest. Every alteration must be recorded in the manifest *and* visually marked — which
adds visual complexity to a map whose whole problem is that it must be simple. The mitigation fights
the objective.

**Assessment: not recommended for Kestral.** The scenario does not need altered infrastructure, so
this mode buys nothing and costs the most.

---

## Candidate C — Completely fictional map built from a real geographic template

**Real:** nothing rendered. Real geography is used only as a *design reference* while drawing — real
proportions, a plausible strait width, a realistic detour ratio.
**Fictional:** the entire rendered map.

**What the user sees.** A clean diagram: a channel, a blockage, a long way round, two or three ports.
Possibly closer to a transit map than a coastline.

**Assumptions they may make.** Very few. Nothing invites a real-world reading, and there is no place
to search for.

**Five-second test:** **potentially the strongest of the three** — and this is the finding that
should be taken seriously rather than treated as a consolation prize. A diagram drawn *only* to
answer the five questions can omit everything else. A real coastline cannot: it arrives with
headlands, islands and inlets that carry no meaning for this scenario and compete for attention.

**Cost:** lowest. **No new dependency, no geodata, no licence, no manifest complexity, no sensitive-
location review.** It is a rewrite of the existing SVG component with a clear brief — which is what
issue #30 already asks for.

**The catch, stated honestly.** This is *the same category* as the map that already failed. It would
only succeed if the failure was one of execution rather than of category. Reading the original
observation — "it looked artificial and did not help" — the failure looks like execution: too many
decorative points, no clear blocked route, no legend. But that is a judgement, and it could be wrong.

---

## Recommendation

**Prototype C first, then A, and decide with a cold reader — not by argument.**

**Decided 21 July 2026:** candidate C is the approved next step, tracked as
[issue #33](https://github.com/CypherTechAries/project-meridian/issues/33). **No dependency or map
code may be added until that prototype has been reviewed.** The engine's lack of any spatial model,
recorded above, strengthens this: a real coastline would have to carry invented placement for two of
the five questions, which a schematic does not.

The reasoning:

1. **C is far cheaper to test.** No dependency, no data pipeline, no licence review. A working
   version could exist in an afternoon and be put in front of someone the same day.
2. **If C passes, A is unnecessary for this scenario** — and MERIDIAN avoids adopting a mapping
   stack, a sensitive-location review process and the false-authority risk it cannot fully close.
3. **If C fails, that is decisive.** It would mean the failure was of category, not execution, and
   real geography is the answer. The cost of finding out is one afternoon.
4. **A stays the recommended direction for scenarios where physical realism carries meaning** —
   logistics, infrastructure, emergency planning. Kestral is not obviously one of those: it is a
   crisis-communication scenario about belief and political pressure, and the geography is context
   rather than mechanism.

This is a correction to the founder's stated preference for candidate A. The preference is sound for
the *general* direction — real geography is the right default for MERIDIAN — but **for this specific
scenario the map is supporting evidence, and the cheapest thing that passes the test should win.**

**Candidate B is not recommended in any case.**

---

## What either prototype must contain

**Drawn — and nothing else:**

- The blocked route, unmistakably blocked. Not a red line; something a reader reads as *closed*.
- The alternative route, unmistakably longer. The extra distance must be *visible*, not stated.
- Two or three affected ports, **labelled in plain text**, not keyed to a legend.
- A plain legend in ordinary words.

**Not drawn:**

- Decorative points, meaningless network lines, unnamed features, anything present to look technical.
- Any value the engine does not produce.
- Anything requiring a second look to interpret.

**Always visible:** the fictional-scenario disclosure, and the geography mode.

**Frame correctly at 1366×768, 1440×900 and 1920×1080**, with nothing cropped and no horizontal
overflow. This is measured, not eyeballed — the same harness used for the usability reset.

---

## What must not happen

- **Do not attach Kestral to a politically sensitive real conflict.** Not by default, and not as a
  "realistic" improvement. If candidate A proceeds, the underlying region must pass the
  sensitive-geography review in [the risk register](../research/REAL-GEOGRAPHY-RISK-REGISTER.md),
  and an active-conflict strait is excluded outright.
- Do not restore the map to the default view until it passes the acceptance test.
- Do not make a weaker miniature imitation of a good component. The Ask MERIDIAN context panel draws
  the same map and must keep drawing the same one, resized.
- Do not remove `MAP_LIMITATION` from `briefing.ts` until a cold reader has actually passed the test.

---

## Related

- [Real Geography, Fictional Worlds](../research/REAL-GEOGRAPHY-FICTIONAL-WORLDS.md) — the mode definitions and the option comparison
- [Scenario Geography Manifest](SCENARIO-GEOGRAPHY-MANIFEST.md) — what candidate A would have to declare
- [Mapping stack and data sources](../research/MAPPING-STACK-AND-DATA-SOURCES.md) — what candidate A would cost in dependencies and obligations
- [Clean-room map implementation plan](CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN.md) — how either would be built
- [Issue #30](https://github.com/CypherTechAries/project-meridian/issues/30) — the open redesign issue, **not closed by this document**
