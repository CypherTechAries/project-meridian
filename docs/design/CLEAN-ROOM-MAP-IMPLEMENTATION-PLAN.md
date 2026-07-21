# Clean-Room Map Implementation Plan

**Status: DESIGN — no map code has been written, and none may be written until this plan is approved.**
**Written 21 July 2026.**

---

## Why "clean-room" is a legal requirement here, not a style

FORSYTE has a mature mapping subsystem. It is **proprietary**, © Cypher Tech Solutions Ltd, with **no
public licence grant**; its own execution plan assigns the map module to **GPLv3**; and parts of the
surrounding code are **export-controlled under the UK Military List**, where *publishing is an export
event*.

MERIDIAN is a **public repository**. Any of those three facts alone would block reuse. Together they
make the boundary absolute.

**The founder's instruction stands as the rule:** *do not reuse FORSYTE map code; do not copy FORSYTE
implementation patterns directly; treat it as clean-room only; do not introduce GPL, MapLibre Native
or export-gated code into MERIDIAN.*

---

## The clean-room rule, concretely

**While writing MERIDIAN map code:**

1. **No FORSYTE file is open, referenced, or consulted.** Not for structure, not for naming, not for
   "how did they handle this".
2. **No FORSYTE identifier, type name, file name or comment is reproduced.**
3. Requirements are expressed in MERIDIAN's own terms, derived from MERIDIAN's own needs.
4. Where a general technique is genuinely standard — a Mercator projection, a haversine distance,
   label collision detection — it is taken from **public sources** (published algorithms, the
   `d3-geo` documentation, textbooks), and the source is cited in the code comment.
5. **Provenance is recorded.** Each new map module states in its header where its approach came from.

**What may cross the boundary:** the *fact* that certain problems exist and matter — label collision,
attribution as a first-class obligation, playback that refuses to interpolate. Knowing a problem is
worth solving is not copying a solution.

**What may not cross:** any expression of a solution. Structure, decomposition, algorithms, naming,
data shapes, file organisation.

### If direct reuse is ever wanted

It requires **written permission from Cypher Tech Solutions Ltd**, granted before any code is looked
at, and a resolution of the GPLv3 destiny question — because permission to copy proprietary code does
not help if that code is later released under GPLv3 and MERIDIAN's copy inherits the obligation.

**The cleaner path is to not ask.** Under the recommended stack, almost nothing FORSYTE has is
relevant: Natural Earth plus `d3-geo` needs no MGRS, no UTM grid, no tile mathematics, no MBTiles and
no offline tile server. Those are the modules that would have been worth porting.

---

## No shared mapping package

The proposal to extract a neutral mapping package used by both products is **not recommended**.

| Reason | Detail |
|---|---|
| **Two languages, no shared runtime** | Kotlin/Android with no JS target; browser TypeScript. A "shared" package would be two implementations with one name. |
| **Two rendering models** | MapLibre Native GeoJSON sources and data-driven layer expressions; versus inline SVG path strings. The *layer model itself* does not transfer. |
| **Two licence positions** | Proprietary and GPLv3-destined; versus public and all-rights-reserved. A shared package must satisfy both, which means the strictest wins — GPLv3 — which MERIDIAN cannot accept. |
| **Export asymmetry** | One codebase is export-sensitive and gates accordingly; the other is public with no gate. Shared code inherits the stricter obligation permanently. |
| **The safety argument** | The two products must never look interchangeable — a simulated overlay read as operational reporting is a safety issue. Shared rendering components make divergence harder, not easier. |

**Recommendation: rebuild MERIDIAN mapping independently, from public sources.** It is the least
risky of the three options considered (copy selected components / extract a shared package / rebuild
independently), and under the recommended stack it is also the cheapest, because the dependency does
most of the work.

---

## Build order

Nothing below is implemented. Each step is gated on the one before.

### Step 0 — Decide the candidate *before* writing map code

Prototype the abstract diagram (candidate C) and, only if it fails a cold reader, the real basemap
(candidate A). See [KESTRAL-STRAIT-MAP-DIRECTION](KESTRAL-STRAIT-MAP-DIRECTION.md).

**Candidate C requires none of the steps below.** It is a rewrite of the existing SVG component with
no dependency, no data and no licence surface. If it passes, stop here.

### Step 1 — The shape vocabulary

A small, additive set of primitives — polyline, polygon, circle, point, label — with stable ids,
independent of any renderer. Written from MERIDIAN's needs, in MERIDIAN's terms.

**Gate:** unit-tested, with no import from any mapping library.

### Step 2 — Geodata acquisition, once, offline

Take a Natural Earth extract for the chosen region. Convert to TopoJSON. **Commit the artefact** with
its version and SHA-256. No build-time download, ever — a build that reaches the network is not
reproducible and cannot be air-gapped.

**Gate:** the manifest fields in [SCENARIO-GEOGRAPHY-MANIFEST](SCENARIO-GEOGRAPHY-MANIFEST.md) are
populated and validated.

### Step 3 — Projection and path generation

`d3-geo` + `topojson-client`. `geoPath()` produces SVG `d` strings that the existing renderer already
knows how to emit.

**Gate:** renders at all three viewport sizes with no clipping and no horizontal overflow, measured
by the same harness used for the usability reset. Two new dependencies, both ISC, recorded in a
third-party notices file.

### Step 4 — The bounded default layer set

Default visible: **affected area · blocked route · alternative route · affected ports · key
communities.** Nothing else.

Optional and off by default: roads, rail, airports, supply routes, weather, population, trade,
infrastructure, political boundaries, scenario events, organisational areas of responsibility.

**Complexity must be earned.** Each optional layer requires a stated reason a reader needs it.

**Gate:** the default set answers the five questions, verified with a cold reader.

### Step 5 — Visual separation and disclosure

The MERIDIAN visual grammar, deliberately distinct from FORSYTE's:

- **FICTIONAL SCENARIO** and **SIMULATED**, persistently visible.
- Scenario time or day.
- Whether the geography is real, and whether infrastructure has been altered.
- Whether each layer is engine-derived, declared or illustrative.
- **Patterned** simulated areas, a scenario watermark, an explicit legend, clear separation between
  base map and overlays.
- **Never colour alone** — the existing origin-marker rule already requires a letter and a label, and
  the map must follow it.

**Gate:** side-by-side comparison with FORSYTE confirming the two cannot be mistaken for each other.

### Step 6 — Attribution rendered from the manifest

The required string is a data field, rendered from data, asserted by a test. Never hand-typed markup.

**Gate:** a test fails if attribution is absent when the licence requires it.

---

## Standing prohibitions

- No FORSYTE code, structure, naming or file organisation.
- No GPL or AGPL dependency. No MapLibre **Native**. No export-gated capability of any kind.
- No hosted tile service. No build-time or runtime network access for map data.
- No live tracking, operational data, intelligence feed or real-person information.
- No real people or real organisations in any scenario.
- No engine change: the map draws the run, it does not feed it.
- No claim that real geography makes the simulation more accurate.

---

## What "done" means

Not "the map renders". **A first-time reader can explain the map after five seconds** — and
`MAP_LIMITATION` in `briefing.ts` is deleted because it is no longer true, not because it is
inconvenient.
