# Mapping Stack and Data Sources

**Status: RESEARCH — nothing here is installed. No dependency was added.**
**All sources checked 21 July 2026.**

> **This is not legal advice.** Three items below are flagged as needing a qualified review. The
> recommended stack is chosen partly *because* it makes all three moot.

---

## The constraint that decides this

MERIDIAN is a **public GitHub repository with no LICENSE file** — all rights reserved, proprietary,
source-visible. It is a **browser app: Vite + TypeScript, no framework**, currently rendering
hand-written inline SVG. It may need **offline or air-gapped** deployment, and a scenario must be
able to **pin the exact map data version** used, so a run can be reproduced.

Those constraints eliminate most of the market before any comparison begins.

---

## Recommendation

### Primary — Natural Earth (public domain) + `d3-geo` + `topojson-client`, rendered as SVG

**Why.** It matches the constraints rather than tolerating them.

- **Natural Earth is public domain.** No attribution, no share-alike, no licence analysis to get
  wrong, and **no Produced-Work-versus-Derivative-Database question at all.** For a fictional
  scenario simulator this removes the entire legal surface.
- **`d3-geo`'s `geoPath()` emits SVG path `d` strings.** It *extends* the existing hand-written SVG
  renderer instead of replacing it with a WebGL canvas. No map SDK, no tile pipeline, no runtime
  network access.
- **Offline by construction, not by configuration.** The geodata is a JSON file imported at build
  time. There is no network path to disable.
- **Pinning is a file hash.** Natural Earth releases are versioned; record the version and a
  SHA-256 in the scenario.
- Natural Earth's scope — coastlines, borders, populated places, rivers, bathymetry — is exactly
  what a fictional scenario needs. We do not need street level.

**Obligations created:** reproduce the ISC copyright notice for `d3-geo` and `topojson-client` in a
third-party notices file. Natural Earth requires **nothing**. No obligation touches MERIDIAN's source
licence, and no attribution UI is required.

**One useful bonus:** Natural Earth explicitly invites remixing of its disputed-area themes —
"Please feel free to mashup our disputed area themes to match your particular political outlook."
For fictional geography that is close to a purpose-built endorsement. Note the flip side: its
boundaries follow *de facto* control, which is a declared editorial position and must be disclosed
rather than presented as neutral.

### Second choice — MapLibre GL JS 5.x + self-hosted PMTiles (Protomaps extract)

Only if street-level detail, real zoom or label rendering becomes necessary. Still offline, still
self-hosted, still no service terms — but one large dependency, a WebGL canvas rather than SVG, and
it re-introduces ODbL.

**Obligations:** BSD-3-Clause notices for MapLibre (ship its `LICENSE.txt` verbatim — it aggregates
mapbox-gl-js ≤1.13, glfx.js and d3-color) and for `pmtiles`; plus **`© OpenStreetMap contributors`**
displayed on the map with a route to `https://www.openstreetmap.org/copyright`.

### Rejected

| | Why |
|---|---|
| **Mapbox GL JS v2+** | Proprietary. Licence terminates automatically without an active Mapbox account; forbids modifying billing/telemetry code; mandates data collection. Three independent disqualifiers for an air-gapped proprietary product. |
| **`tile.openstreetmap.org`** | Explicitly not for production. Pre-seeding an offline bundle is prohibited bulk downloading, so the offline cache could not legitimately be built in the first place. |
| **OpenMapTiles hosted tiles/downloads** | The open schema does not make the distributed tiles open — those fall under MapTiler commercial terms. Even the schema route stacks a second mandatory CC-BY credit on top of OSM's. |
| **GSHHG** | LGPL v3 **on a dataset**, which is an awkward fit for proprietary bundling. Only if Natural Earth's coastline resolution proves insufficient, and then only after legal review. |

---

## Renderers

| | Licence | Version | Offline | SVG-native | Fit |
|---|---|---|---|---|---|
| **d3-geo + topojson-client** | ISC / ISC | 3.1.1 / 3.1.0 | Total — data is a JSON import | **Yes — `geoPath()` emits SVG `d`** | ★★★★★ |
| **MapLibre GL JS** | BSD-3-Clause | 5.24.0 | Yes, with local PMTiles | No (WebGL) | ★★★★ |
| **Leaflet** | BSD-2-Clause | 1.9.4 | Yes, with local tiles | Partial (SVG overlay only) | ★★★ |
| **OpenLayers** | BSD-2-Clause | 10.9.0 | Yes | No (canvas/WebGL) | ★★ |
| **Mapbox GL JS v2+** | **Proprietary (Mapbox TOS)** | — | **No — account-tethered** | No | Disqualified |

**None of the permissive renderers imposes any obligation on MERIDIAN's source code.** All require
only that their copyright notice, licence text and disclaimer be preserved in distribution.

*Caveat: Leaflet, OpenLayers, d3-geo and topojson-client licences were read from npm registry
metadata, not from LICENSE files. `topojson-client` is ISC per npm and BSD-3-Clause in some
historical sources. Read the repository LICENSE before writing a notices file.*

### Why MapLibre exists, precisely

Mapbox GL JS was BSD-3-Clause **through v1.13**. At **v2.0** Mapbox relicensed to a proprietary
licence requiring an active account, forbidding modification of billing/telemetry code, and
mandating de-identified location and usage collection. MapLibre GL JS is the community hard-fork of
the last BSD-3-Clause commit, carried forward with no account requirement and no telemetry.

The distinction that matters: **Mapbox GL JS v1 is still freely usable; v2+ is not.** Any advice
that says "Mapbox GL JS is open source" is out of date by five years.

---

## Data sources

| Dataset | Owner | Licence | Commercial | Attribution | Offline | Coverage | Key limitation |
|---|---|---|---|---|---|---|---|
| **Natural Earth** | Natural Earth / NACIS | **Public domain** | Yes | **None required** | Yes | Global, 1:10m / 1:50m / 1:110m | Coarse — not street level; *de facto* borders |
| **OpenStreetMap** | OSM contributors / OSMF | **ODbL 1.0** | Yes | **Required** — `© OpenStreetMap contributors` + licence reference | Yes | Global, street level | Share-alike on Derivative Databases; quality varies by region |
| **Protomaps basemap** | Protomaps (from OSM) | ODbL 1.0 **as a Produced Work** | Yes | Required (OSM) | Yes — single PMTiles file | Planet ≈120 GB, z0–15 | Builds retained ~1 week + latest per patch — **archive your own copy** |
| **OpenMapTiles schema/tools** | OpenMapTiles / MapTiler AG | BSD (code) + **CC-BY** (schema/cartography) | Yes | **OpenMapTiles credit + link, *plus* OSM** | Yes | Global schema | **Produced tiles governed by MapTiler commercial terms, not the repo licence** |
| **Copernicus DEM GLO-30/90** | ESA / EU | Free licence; redistribution permitted | Yes | **Required — long exact DLR/Airbus/ESA string** | Yes | Global ~149 M km² | Attribution string must be reproduced verbatim |
| **GSHHG 2.3.7** | Wessel & Smith | **LGPL v3** | Yes | Yes | Yes | Global shorelines | **LGPL-on-data is an awkward fit for proprietary bundling** |
| **SRTM** | NASA / USGS | **UNVERIFIED** | ? | ? | Yes | ~60°N–56°S | Not checked against a primary source; Copernicus DEM supersedes it technically |

---

## The ODbL question, answered plainly

**Can a proprietary, all-rights-reserved product use OpenStreetMap data and an open-source renderer?**
**Yes, comfortably.** But three different licences govern three different things, and conflating
them is where people go wrong.

### A · The renderer's licence governs **your code**

All the viable renderers are permissive (BSD-2, BSD-3, ISC). **None is copyleft. None contains any
reciprocity clause that can reach TypeScript.** MERIDIAN stays all-rights-reserved. Ship a
third-party notices file; for BSD-3-Clause additionally do not use contributor names to endorse the
product.

### B · The data's licence governs **your data and your output**

ODbL is the only licence in the stack with share-alike, and **it applies only to databases, never to
code**. ODbL §4.5(b) is explicit:

> "Using this Database, a Derivative Database, or this Database as part of a Collective Database to
> create a Produced Work does not create a Derivative Database for purposes of Section 4.4."

A rendered map — a raster, a WebGL frame, **an inline SVG you draw** — is a *Produced Work*. It
carries an attribution obligation and **no obligation to release anything**.

**Obligations, in order of certainty:**

1. **Always** — display `© OpenStreetMap contributors` on or beside the map with a route to the
   licence. Note ODbL §4.3 has **two** parts: the notice must convey both the *source* and that it
   is *available under this licence*. "© OpenStreetMap" alone is insufficient. In an interactive map
   the credit may collapse or fade after five seconds provided an info control still reaches it.
2. **Never** — any obligation to publish MERIDIAN's source.
3. **Conditionally** — if a *modified OSM database* is shipped outside the organisation, §4.4
   requires ODbL or a compatible licence.

**The architectural rule that avoids point 3 entirely:** keep OSM-derived data as an **unmodified,
separately identifiable file** that scenario data *references* rather than *merges into*. That is a
Collective Database, not a Derivative Database. Fictional overlays live in MERIDIAN's own files under
MERIDIAN's own copyright and are composited only at render time.

### C · The tile service's terms govern **your requests**

Entirely separate. A licence says what you may do with bits you already hold; terms say whether you
may ask a server for them.

- `tile.openstreetmap.org` — no production use, no bulk downloading, no SLA, may be blocked without
  notice. Its policy warns explicitly that "you may no longer be able to serve your paying customers
  if access is withdrawn." **Not shippable.**
- Mapbox / MapTiler / Stadia — metered per load, session or credit, requiring a live network call
  per user. Stadia's free tier prohibits commercial use outright; MapTiler's is labelled
  testing/personal/non-commercial. Caching rights are restricted and, at Stadia, sold separately.
- **Self-hosted PMTiles or a bundled TopoJSON file — no service terms exist**, because there is no
  service. This is the only category that survives an air-gap requirement.

**Every hosted vendor's business model depends on the client phoning home**, which is fundamentally
incompatible with air-gapped deployment. Each offers an enterprise on-prem escape hatch. Protomaps
is the only one whose *default* mode is what MERIDIAN needs.

---

## Offline and air-gapped feasibility

**Fully achievable. Two viable architectures.**

1. **Bundled TopoJSON (Natural Earth).** Imported by Vite at build time. No network path, no tile
   server, no runtime dependency. This is not "offline-capable" — it is *incapable of being online*,
   which is a far stronger guarantee for an air-gapped review.
2. **Local PMTiles archive.** A single file produced once by `pmtiles extract`, served by any static
   file server or read from disk via HTTP range requests. Its read-only nature — "not possible to
   update an archive in-place without re-writing the entire file" — is a benefit here.

**Not feasible offline:** Mapbox GL JS v2+ (account validation), any metered hosted service in its
standard configuration, and `tile.openstreetmap.org` (you cannot legitimately build the cache).

---

## Version pinning and reproducibility

A scenario must record the exact map data used, so a run replayed later renders identically.

| Approach | Pinnable | How |
|---|---|---|
| **Natural Earth TopoJSON, bundled** | ★★★★★ | Versioned releases; file in the repo. Record version + SHA-256. Byte-identical forever. |
| **PMTiles archive** | ★★★★★ | One immutable file by format design. Record filename, build date and SHA-256. **Archive your own copy** — Protomaps retains builds for about a week. |
| **Hosted tile API** | ★ | Cartography and data change with no notice or version identifier. **Fundamentally incompatible with reproducibility.** |

**Recommendation:** every scenario carries a provenance block — dataset, upstream version, SHA-256,
licence identifier, and the attribution string that must be displayed. That satisfies reproducibility
*and* generates the attribution automatically, so compliance cannot drift out of sync with the data.
This is part of the [Scenario Geography Manifest](../design/SCENARIO-GEOGRAPHY-MANIFEST.md).

---

## Not verified — do not rely on these

1. **ODbL §1 definition of "Publicly"** — not retrieved verbatim. The argument that internal or
   air-gapped distribution may never trigger §4.4 depends on it.
2. **Whether vector tiles are a Produced Work or a Derivative Database** — genuinely unsettled.
   Protomaps' "as a Produced Work" label is a distributor's characterisation, not a legal
   determination. **The single most important counsel item if the second-choice stack is adopted.**
3. **SRTM licensing** — not checked against USGS/NASA primary sources.
4. **Natural Earth ports/airports themes** — listed on the downloads site, not confirmed on the
   features page. Verify before depending on them.
5. **MapTiler Server & Data Terms** — the redirect was confirmed, the terms were not read.
6. **Mapbox tile-caching and offline permissions** — not stated on the pricing page. Moot given the
   recommendation.
7. **LGPL-v3-applied-to-a-dataset** — the practical obligations of bundling GSHHG in a proprietary
   product are not resolvable from the licence text alone. **Counsel item if GSHHG is needed.**

**Items 2 and 7, and the Derivative-Database boundary generally, are where a short qualified review
would be worth the cost. The recommended primary stack — Natural Earth, public domain — makes all of
them moot.**

---

## Sources register

All checked **21 July 2026**.

| # | URL | What it is |
|---|---|---|
| 1 | https://opendatacommons.org/licenses/odbl/1-0/ | ODbL 1.0 full text — §1, §4.3, §4.4, §4.5(b) |
| 2 | https://www.openstreetmap.org/copyright | OSM copyright and licence page |
| 3 | https://osmfoundation.org/wiki/Licence/Attribution_Guidelines | OSMF attribution guidelines |
| 4 | https://operations.osmfoundation.org/policies/tiles/ | OSMF Tile Usage Policy |
| 5 | https://raw.githubusercontent.com/maplibre/maplibre-gl-js/main/LICENSE.txt | MapLibre LICENSE — BSD-3 + bundled notices |
| 6 | https://registry.npmjs.org/maplibre-gl/latest | MapLibre current version (5.24.0) |
| 7 | https://raw.githubusercontent.com/mapbox/mapbox-gl-js/main/LICENSE.txt | Mapbox GL JS v2+ proprietary licence |
| 8 | https://docs.protomaps.com/pmtiles/ | PMTiles format — spec v3, range requests, read-only |
| 9 | https://docs.protomaps.com/basemaps/downloads | Protomaps licence, build cadence, retention, size |
| 10 | https://registry.npmjs.org/pmtiles/latest | pmtiles reader (4.4.1, BSD-3-Clause) |
| 11 | https://protomaps.com/ | Self-hosting premise, commercial position |
| 12 | https://www.naturalearthdata.com/about/terms-of-use/ | Natural Earth public-domain terms and disclaimer |
| 13 | https://www.naturalearthdata.com/features/ | Natural Earth scales and themes |
| 14 | https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/ | Natural Earth *de facto* boundaries policy |
| 15 | https://registry.npmjs.org/leaflet/latest | Leaflet 1.9.4, BSD-2-Clause |
| 16 | https://registry.npmjs.org/ol/latest | OpenLayers 10.9.0, BSD-2-Clause |
| 17 | https://registry.npmjs.org/d3-geo/latest | d3-geo 3.1.1, ISC |
| 18 | https://registry.npmjs.org/topojson-client/latest | topojson-client 3.1.0, ISC (metadata) |
| 19 | https://github.com/openmaptiles/openmaptiles/blob/master/LICENSE.md | OpenMapTiles BSD + CC-BY and attribution rules |
| 20 | https://openmaptiles.org/terms/ | **Redirects to MapTiler Server & Data Terms** |
| 21 | https://github.com/GenericMappingTools/gshhg-gmt | GSHHG licence (LGPL v3), 2.3.7 |
| 22 | https://dataspace.copernicus.eu/.../COP-DEM | Copernicus DEM licence + mandatory attribution |
| 23 | https://www.maptiler.com/cloud/pricing/ | MapTiler pricing model and free tier |
| 24 | https://stadiamaps.com/pricing/ | Stadia credit model, commercial prohibition, caching SKU |
| 25 | https://www.mapbox.com/pricing | Mapbox metering, free tiers, Atlas on-prem |

**Not retrieved:** `soest.hawaii.edu/pwessel/gshhg/` (DNS timeout — GSHHG licence taken from #21);
`spacedata.copernicus.eu/collections/...` (connection refused — taken from #22);
`openmaptiles.org/license/` (HTTP 404 — taken from #19/#20).
