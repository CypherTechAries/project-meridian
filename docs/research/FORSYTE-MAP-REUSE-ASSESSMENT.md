# FORSYTE Map Reuse Assessment

**Status: RESEARCH — no code was copied, and none may be.**
**Inspection performed 21 July 2026, read-only, against the local working copy.**

---

## Conclusion first

> **No FORSYTE mapping code can be reused by MERIDIAN. Not now, and not after refactoring.**
>
> There are **three independent, individually fatal** reasons. Any one of them alone would block it.

| # | Blocker | Why it is fatal on its own |
|---|---|---|
| **1** | **Licence** | FORSYTE is **proprietary**, © Cypher Tech Solutions Ltd, with **no public licence grant** and no root LICENSE file. It cannot lawfully be copied into a public repository at all without an explicit written relicence. |
| **2** | **GPLv3 destiny** | FORSYTE's own execution plan assigns `core-map` — including `TacticalMapView` and offline tiles — to **GPLv3 (ARC Core)**. Copying that code into MERIDIAN would make MERIDIAN GPLv3, destroying its all-rights-reserved position. |
| **3** | **Platform** | It is **MapLibre Native for Android**, in Kotlin, with no Kotlin/JS target configured. MERIDIAN is a browser TypeScript app rendering **inline SVG**. There is no shared runtime, no shared language, and no shared rendering model. |

**Realistic value: roughly 10–13% of the code as a hand-port, and 0% as a dependency.** The rest is
concepts and design. And even the hand-port requires written permission from Cypher Tech Solutions
Ltd first, because "clean-room" is doing real legal work there that a copy-paste would not survive.

**The founder's instruction — treat this as clean-room only, do not copy implementation patterns
directly — is correct and is the only lawful route.** See
[CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN](../design/CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN.md).

---

## What FORSYTE actually has

It is a large, mature, genuinely good mapping subsystem — roughly **18,000–22,000 lines** of
mapping-related production code across **90–110 files**, plus about 4,000 lines of mapping tests and
~101 vendored BRouter Java files. `TacticalMapView.kt` alone is 3,971 lines.

| Aspect | What is there |
|---|---|
| **Library** | MapLibre **Native Android** SDK 11.8.0. One map SDK only — no osmdroid, Mapbox or Google Maps. |
| **Tiles** | CARTO GL styles (Dark Matter / Voyager) bundled as assets, repointed at **OpenFreeMap**'s keyless OpenMapTiles planet tiles. Fonts and sprites from CARTO's CDN. |
| **Offline** | Raster **MBTiles (SQLite)**, user-imported, served over a **loopback HTTP server** because MapLibre Native cannot read `.mbtiles` directly. Seven files, ~1,129 lines. |
| **Attribution** | Handled properly in three places — style-embedded, offline pack (`© OpenStreetMap contributors`), and routing data (ODbL string for BRouter segments). |
| **Components** | Route drawing, markers, polygons/geofences, RF heatmaps, per-object visibility, hit-testing, camera/viewport, timeline playback, label declutter, MGRS/UTM coordinates and grid. |
| **Not present** | **No general legend component exists.** Only two passing mentions of "legend" in the entire repo. |

A positive finding worth recording: the map render path is **not tier-gated** — searching the map
packages for entitlement/tier/capability checks returned zero hits. Gating happens upstream.

---

## Three-bucket categorisation

### REUSABLE DIRECTLY — **empty**

Nothing. Not one file. The licence blocks it, the language blocks it, and the rendering model blocks
it. This bucket exists in the task template; the honest answer is that it has no members.

### REUSABLE AFTER EXTRACTION — *meaning hand-rewritten in TypeScript, with permission*

~2,500–3,000 Kotlin lines of genuinely pure logic, which would become perhaps 1,500–2,000 lines of
TypeScript. These are the modules FORSYTE itself marks "no Android / pure / unit-testable".

| Component | Lines | Why it is worth the effort |
|---|---|---|
| `CoordinateFormatter.kt` + `CoordinateFormat.kt` | 409 | WGS84 → UTM/MGRS with honest polar out-of-range handling. Hard to get right. |
| `ArcCoordinateGrid.kt` | 439 | *Solved*, not approximated, UTM grid lines. A real correctness asset. |
| `MapDeclutter.kt` | 321 | Label priority, collision and co-location stacking policy. Two trivial enum imports to strip. |
| `ArcMapOverlay.kt` | 202 | A deliberately generic shape vocabulary — polyline, polygon, circle, hex colours, stable ids. A good **schema** to learn from; must be re-targeted from MapLibre layers to SVG. |
| `MbtilesTileMath.kt` | 110 | Self-declared Android-free TMS↔XYZ flip and bounds checks — universal slippy-map maths. |
| `GeoUtils.kt` | 103 | Haversine distance, bearing, destination point. Zero dependencies. |
| `ArcMapObjectHitTest.kt` | 111 | Generic proximity hit-testing and stack picking. |
| `ArcObjectVisibility.kt` | — | Pure namespaced hide-set; ~30 lines of TypeScript. |
| `RfHeatmapPlayback.kt` | — | **Design only.** Its "scrub that refuses to interpolate" honesty pattern is excellent and generalisable. Do not port the RF plumbing. |

**Important caveat.** Most of this is not needed for the recommended MERIDIAN direction. Natural
Earth plus `d3-geo` requires no MGRS, no UTM grid, no tile maths and no MBTiles. **The genuinely
relevant items are `MapDeclutter` (label collision) and `ArcMapOverlay` (shape vocabulary), and only
as design references.** Porting the rest would be building capability MERIDIAN has no use for.

### DO NOT REUSE

| Component | Reason |
|---|---|
| `TacticalMapView.kt` (3,971 lines) | Compose + `AndroidView` + imperative MapLibre-Native layer API. Camera and fit-to-bounds logic is inseparable from it. |
| `MbtilesTileServer/Reader/Importer`, `OfflineMapController` | `SQLiteDatabase` + `ServerSocket`. **No browser equivalent exists.** |
| All `core/arc/rfheat/*` (11 files) | RF multi-node fusion. **Hard-gated out of every shipping build under UK ML21/ML11 export control.** |
| `DfBearingOverlay.kt` | Direction-finding — same export-control category. |
| `ForsyteMapSymbol`, `ForsyteMarkerCatalogue`, `ForsyteSymbolBitmap`, `ContactSymbolPainter`, `MarkerKindSymbol` | Proprietary military symbology, affiliation/threat framing, Android `Bitmap` rasterisation. Brand IP. |
| `RemoteIdMarkerStyle`, `LiveDetectionMapTab`, `FpvAlertMapper` | Detection-product logic. |
| All `core/tak/mapping/*` | TAK / Cursor-on-Target interop — operational C2. |
| `core/arc/session/*`, `ArcResyncCoordinator`, `P2pDrawingPayload`, `BftOverlayProjection`, `EmergencyAlertOverlays`, `ArcCoordPin` | ARC session, mesh and command-workflow product logic. |
| `BRouterEngine` + vendored BRouter | MIT and genuinely reusable *in Java* — useless to a browser app, and needs multi-GB `.rd5` region files. |
| CARTO style JSONs | Usable in principle by MapLibre GL JS — but MERIDIAN has no map SDK to consume a 41 KB GL style. |

---

## Export control — the assumption that must never cross

FORSYTE's `SECURITY.md` is explicit:

> "Parts of this codebase are plausibly **export-controlled under the UK Military List (ML21
> software …)**. **Publishing IS an export event.** Uploading a build … or making the repository
> accessible to a person outside the UK can constitute export. A padlocked UI does not help: if the
> controlled code is *in the artifact*, it has been exported."

Its RF heatmap is hard-gated out of every shipping build for exactly this reason — "a networked
multi-node RF-fusion picture strengthens the ML21/ML11 (ECJU) export read".

**MERIDIAN is a public repository.** Moving any export-sensitive FORSYTE code into it would be an
export event with no gate available. This is not a policy preference; it is the reason the boundary
must be absolute rather than case-by-case.

Other operational assumptions that must not transfer: the loopback tile server's single-trusted-device
model; blue-force and mesh C2 semantics; and the proprietary military symbology.

---

## Third-party obligations FORSYTE already carries

Recorded here because they show what a real map stack costs in obligations, and because MERIDIAN's
recommended stack deliberately avoids most of them.

- MapLibre Native — BSD-2-Clause.
- CARTO styles — BSD-3-Clause code, **CC-BY-4.0 design** requiring a visible `© CARTO`.
- OSM data — ODbL, attribution required; and FORSYTE's own notes record that *"if we later
  bundle/redistribute OSM-derived tiles, ODbL share-alike obligations also apply."*
- BRouter — MIT, vendored.
- Policy line worth borrowing: *"Disallowed in the shipped app: GPL and AGPL outright."*

FORSYTE also documents rejecting osmdroid (archived Nov 2024) and mapsforge (LGPL-3.0 relinking
burden), and records that Organic Maps, CoMaps and OsmAnd are **"offline-UX references only — no app
code is copied into FORSYTE."** That is precisely the posture MERIDIAN must take towards FORSYTE.

---

## What MERIDIAN should actually take

**Ideas, not code.** Specifically:

1. **The honesty patterns.** A playback scrub that refuses to interpolate between observations is a
   good idea MERIDIAN should copy *as a principle*.
2. **A generic shape vocabulary** — a small additive set of polyline/polygon/circle primitives with
   stable ids, decoupled from the renderer. FORSYTE's version proves the shape of the idea.
3. **Label declutter as pure, testable logic** kept out of the render layer.
4. **Attribution treated as a first-class obligation** with a declared string travelling alongside
   the data, rather than a footnote added later.
5. **The negative results** — the rejected libraries and the reasons — which save real time.

**And a shared mapping package is not recommended.** See the shared-package assessment in
[REAL-GEOGRAPHY-FICTIONAL-WORLDS](REAL-GEOGRAPHY-FICTIONAL-WORLDS.md) and the reasoning in
[CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN](../design/CLEAN-ROOM-MAP-IMPLEMENTATION-PLAN.md): two products
on two platforms, in two languages, with two rendering models, one proprietary and one public, one
export-sensitive and one not, cannot share a package without dragging each product's constraints into
the other.
