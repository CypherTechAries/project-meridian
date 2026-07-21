# Real-Geography Risk Register

**Status: RESEARCH — no mitigation is implemented.**
**Written 21 July 2026.**

Every risk below is **uncontrolled** unless stated otherwise, because no map work has been done.
"Prevention" describes what would have to exist, not what does.

**Accountable party** is the founder throughout — MERIDIAN has one accountable human, and pretending
otherwise would be its own dishonesty.

---

## R1 · False authority from real geography

**The defining risk of this direction.**

- **Cause** — a real coastline is checkable and true, so the reader extends that trust to everything
  drawn on it. Recognition does the persuading, and no disclaimer competes with recognition.
- **Consequence** — a fictional outcome is read as a forecast about a real place. If that reading
  ever reaches a decision, MERIDIAN has caused harm it explicitly disclaims.
- **Prevention** — persistent, non-dismissible disclosure naming the geography mode; the phrase
  GEOGRAPHICALLY REAL, INSTITUTIONALLY FICTIONAL on every scenario map; fictional names by default;
  a visual grammar that never resembles operational reporting.
- **Detection** — cold usability testing, asking one question: *"is this a real place, and is this
  really happening?"* Nothing else detects it.
- **Containment** — withdraw the scenario; publish a correction.
- **Residual uncertainty** — **high, and irreducible.** Disclosure demonstrably does not stop belief.
  This risk can be reduced but not closed, and choosing real geography is choosing to carry it.

## R2 · Accidental representation of real institutions

- **Cause** — a fictional government at real coordinates occupies the position of a real one. A
  fictional port authority in a real port implies the real operator.
- **Consequence** — reputational harm to an uninvolved organisation; potential defamation exposure
  where the fictional actor behaves badly.
- **Prevention** — fictional names always; **never place a fictional actor in a role a single
  identifiable real organisation occupies**; scenario-location review before adoption.
- **Detection** — review by someone with local knowledge of the source region.
- **Containment** — switch the scenario to Mode D; withdraw.
- **Residual uncertainty** — **medium-high.** Small regions often have exactly one port operator,
  and renaming does not fix a role that maps one-to-one.

## R3 · Political sensitivity

- **Cause** — a fictional blockade on a real, contested strait reads as commentary.
- **Consequence** — the project is drawn into a real dispute it has no standing in.
- **Prevention** — the sensitive-geography exclusion list; **active conflicts excluded outright**;
  no scenario adopts a real location without named human approval.
- **Detection** — review at scenario adoption, and again before any publication.
- **Containment** — withdraw; Mode D.
- **Residual uncertainty** — **medium.** Sensitivity changes over time; a region safe at authoring
  may not be safe at publication.

## R4 · Renaming mistaken for anonymisation

- **Cause** — the assumption that fictional labels prevent identification.
- **Consequence** — a scenario is planned as anonymous, is identified immediately, and the renaming
  then reads as concealment — worse than never renaming.
- **Prevention** — state in the manifest and the interface that **the underlying geography is real
  and may be recognisable**; never rely on renaming as a control for a sensitive location.
- **Detection** — attempt to identify the region from the rendered output before publishing.
- **Containment** — disclose the source region; or move to Mode D.
- **Residual uncertainty** — **low, once documented.** Coastlines are recognisable; this is a known
  fact to design around rather than an open question.

## R5 · Outdated map data

- **Cause** — borders, ports and roads change; a pinned dataset ages by design.
- **Consequence** — the map contradicts the world; a reader who spots one error discounts everything.
- **Prevention** — record dataset version and date in the manifest; **display the map-data date**;
  a declared review interval.
- **Detection** — scheduled review; reader reports.
- **Containment** — update and re-pin, recording that the scenario's geography changed.
- **Residual uncertainty** — **low.** This is a maintenance obligation, not a hazard — provided the
  date is visible. It becomes serious only if the map is presented as current.

## R6 · Incorrect routes or distances

- **Cause** — source data errors; naive straight-line distance presented as a travel route.
- **Consequence** — a false physical claim, which is worse than an invented one because it is
  checkable and wrong.
- **Prevention** — **do not compute travel times unless the method is declared**; state whether a
  distance is physical or a route; prefer "declared" to "calculated" until a real routing method
  exists.
- **Detection** — spot-check against an independent source.
- **Containment** — mark the value UNAVAILABLE rather than showing a wrong one.
- **Residual uncertainty** — **low**, if the manifest's `distances_physically_accurate` and
  `travel_times_calculated_or_declared` fields are honoured.

## R7 · Tile-service failure

- **Cause** — dependence on a hosted service that rate-limits, changes terms or withdraws access.
- **Consequence** — the map disappears, or degrades silently to a blank frame.
- **Prevention** — **the recommended stack has no tile service.** Bundled data cannot fail this way.
- **Detection** — n/a for the recommended stack.
- **Containment** — n/a.
- **Residual uncertainty** — **eliminated by the primary recommendation**; reintroduced if the
  second-choice stack is adopted with a remote source.

## R8 · Licensing breach

- **Cause** — using data or tiles outside their terms; most likely by treating "open source" as
  meaning the *data* is free, or by pre-seeding an offline cache from a service that forbids it.
- **Consequence** — takedown; reputational damage; a share-alike obligation on data that was never
  meant to be published.
- **Prevention** — Natural Earth (public domain) as the primary source; the Collective-Database rule
  (reference, never merge); licence and attribution recorded in the manifest.
- **Detection** — the manifest's licence field is mandatory; a scenario without it does not publish.
- **Containment** — remove the data; re-render from a compliant source.
- **Residual uncertainty** — **low with Natural Earth, medium with OSM** — and see the two
  unresolved counsel items in [MAPPING-STACK-AND-DATA-SOURCES](MAPPING-STACK-AND-DATA-SOURCES.md).

## R9 · Missing attribution

- **Cause** — attribution added by hand and later lost in a redesign.
- **Consequence** — licence breach from a formatting change.
- **Prevention** — **the attribution string travels with the data in the manifest and is rendered
  from it**, so it cannot be edited away independently; a test asserting it is present.
- **Detection** — automated test.
- **Containment** — restore; the fix is trivial once detected.
- **Residual uncertainty** — **low**, and **zero** with Natural Earth, which requires none.

## R10 · Dependency on a commercial map provider

- **Cause** — adopting a hosted stack for convenience.
- **Consequence** — metered cost per user; terms changing; **reproducibility destroyed**, because
  hosted cartography changes with no version identifier.
- **Prevention** — self-hosted or bundled data only. This is a standing architectural rule.
- **Detection** — code review; any outbound map request is a violation.
- **Containment** — migrate to bundled data.
- **Residual uncertainty** — **low**, provided the rule is treated as architectural rather than a
  preference.

## R11 · Leakage of FORSYTE-specific code or data

- **Cause** — copying from a proprietary, export-sensitive, GPLv3-destined codebase into a public
  repository.
- **Consequence** — **the most severe consequence in this register.** Licence breach against Cypher
  Tech Solutions Ltd; potential GPLv3 contamination of MERIDIAN's all-rights-reserved position; and
  in the worst case an **export-control event**, since publishing is an export and a public repo has
  no gate.
- **Prevention** — clean-room only, with written permission before even that; a declared
  do-not-reuse list; no FORSYTE file open while MERIDIAN map code is being written.
- **Detection** — provenance review of any new map module; comparison against the do-not-reuse list.
- **Containment** — remove, rewrite from scratch, and **assume the published history is permanent**.
- **Residual uncertainty** — **low if the clean-room rule holds, catastrophic if it does not.** This
  is the one risk here whose containment does not work after the fact.

## R12 · Simulated and operational layers becoming confused

- **Cause** — MERIDIAN and FORSYTE adopting similar map visual languages.
- **Consequence** — a simulated overlay read as an operational one, or the reverse. In a defence or
  emergency context that is a safety issue, not an aesthetic one.
- **Prevention** — a **deliberately distinct** MERIDIAN visual grammar: different palette, patterned
  simulated areas, a persistent scenario watermark, and disclosure text FORSYTE never uses. **Not
  colour alone.**
- **Detection** — side-by-side review whenever either product's map changes.
- **Containment** — restyle MERIDIAN, never FORSYTE.
- **Residual uncertainty** — **medium**, and it grows if the two ever share components — a further
  argument against a shared package.

## R13 · Users interpreting fictional outcomes as forecasts

- **Cause** — the same mechanism as R1, applied to outcomes rather than the map.
- **Consequence** — a fictional result cited as evidence about the real world.
- **Prevention** — the existing honesty apparatus — declared limitations, NOT_EXECUTED, the "not a
  prediction" caveat already shipped on the Briefing — extended to explicitly cover geography.
- **Detection** — cold testing; watching how people describe the output afterwards.
- **Containment** — correction.
- **Residual uncertainty** — **medium-high**, and real geography raises it.

## R14 · Scenario creators using identifiable real people

- **Cause** — the natural temptation once a scenario is set in a real place.
- **Consequence** — data-protection exposure; defamation; direct harm to a named individual.
- **Prevention** — **absolute prohibition**, already a standing constraint; validation refusing
  real-person identifiers; no scenario field capable of holding one.
- **Detection** — authoring validation; review.
- **Containment** — remove and withdraw.
- **Residual uncertainty** — **low while authoring is not implemented**; must be designed in before
  it is.

## R15 · Sensitive-site exposure

- **Cause** — a general-purpose dataset includes military sites, infrastructure and prisons by
  default. Rendering "everything available" exposes them without anyone deciding to.
- **Consequence** — reputational and possibly legal exposure; an implied targeting picture.
- **Prevention** — **restricted layer categories that never render**; a declared minimum resolution;
  the scenario-location review.
- **Detection** — review of every layer added, against the exclusion list.
- **Containment** — remove the layer; re-render.
- **Residual uncertainty** — **medium.** This risk arrives by default rather than by choice, which
  makes it easy to miss.

## R16 · Map detail overwhelming the user

- **Cause** — real basemaps are dense. Everything the data offers is available, and showing it is
  the path of least resistance.
- **Consequence** — **the exact failure that started this work.** A map that cannot be read in five
  seconds is decoration, and dense realism is decoration that also looks authoritative.
- **Prevention** — a bounded default layer set; **complexity must be earned**; no decorative data
  points; the five-second test as an acceptance criterion, not an aspiration.
- **Detection** — cold testing.
- **Containment** — remove layers.
- **Residual uncertainty** — **medium.** The pressure to add detail is constant, and every addition
  looks individually reasonable.

---

## Risks on the critical path

**R1, R11 and R16 sit on the critical path and none is closed.**

- **R1** cannot be eliminated — only carried deliberately. Adopting real geography is accepting it.
- **R11** is the only risk whose containment does not work retroactively. It must be prevented.
- **R16** already caused one documented failure. Assume it recurs.

**R11 must be resolved before any implementation begins** — that is, written permission or a firm
decision to build with no reference to FORSYTE at all. The second is cleaner and is what the
[clean-room plan](../design/CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN.md) assumes.
