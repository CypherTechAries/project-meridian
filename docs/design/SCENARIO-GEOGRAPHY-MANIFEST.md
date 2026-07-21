# Scenario Geography Manifest

**Status: DESIGN — not implemented. No code reads this.**
**Written 21 July 2026.**

---

## What it is for

Every scenario must be able to answer one question without anyone having to read its source:

> **Is this a real place, and what about it is real?**

The manifest is where that answer lives. It travels with the scenario, it is exported with the run,
and **a scenario without one does not publish**.

It exists because the fiction boundary is not self-evident from a picture. A reader looking at a
coastline cannot tell whether the ports are real, whether the borders have been altered, or whether
the travel times were computed or invented. Only a declaration can carry that.

**Fail closed.** An absent or incomplete manifest means the map does not render. This matches how
MERIDIAN already treats fictional-world metadata: absence is never resolved to a permissive default.

---

## Fields

| Field | Type | Meaning |
|---|---|---|
| `geography_mode` | `REAL_NAMED` · `REAL_RENAMED` · `REAL_ALTERED` · `FICTIONAL` · `ABSTRACT` | Which of the declared modes. No default. |
| `real_geography_source` | string \| `NONE` | Dataset the geometry came from, e.g. `natural-earth-10m`. `NONE` only for `FICTIONAL`. |
| `real_geography_version` | string \| `NOT_APPLICABLE` | Upstream version or build date. |
| `real_geography_sha256` | string \| `NOT_APPLICABLE` | Hash of the exact artefact used, so the run can be reproduced. |
| `displayed_location_name` | string | What the reader sees, e.g. "Kestral Strait". |
| `underlying_region` | string \| `WITHHELD` | The real region, where one exists. `WITHHELD` must carry `withholding_reason`. |
| `names_are_real` | boolean | Whether displayed place names are the real ones. |
| `borders_are_real` | boolean | Whether political boundaries are as the source shows them. |
| `infrastructure_status` | `REAL` · `ALTERED` · `INVENTED` · `NOT_SHOWN` | Ports, roads, rail, airports. |
| `alterations` | list of `{feature, change, reason}` | **Every** alteration, individually. Required and non-empty when `infrastructure_status` is `ALTERED`. |
| `distances_physically_accurate` | boolean | Whether rendered distances correspond to real ones. |
| `travel_times` | `CALCULATED` · `DECLARED` · `NOT_SHOWN` | If `CALCULATED`, `travel_time_method` is required. |
| `travel_time_method` | string \| `NOT_APPLICABLE` | The declared method. No undeclared computation. |
| `entities_are_fictional` | `true` | **Constant.** Present so it is machine-readable, and validated to be `true`. There is no scenario in which it is false. |
| `real_world_data_present` | `NONE` · `STATIC_GEOGRAPHIC` · `CHANGING_PUBLIC` · `OPERATIONAL` | Only the first two are permitted; the last two are refused. |
| `map_data_last_updated` | date | When the underlying data was published. **Displayed to the reader.** |
| `licence` | string | SPDX-style identifier or licence name. |
| `attribution_text` | string \| `NONE_REQUIRED` | The **exact** string that must be rendered. The interface renders *this*, never a hand-typed copy. |
| `attribution_url` | string \| `NONE_REQUIRED` | Where the licence can be read. |
| `known_inaccuracies` | list of strings | Stated, not hidden. An empty list is a claim and must be justified. |
| `prohibited_interpretations` | list of strings | What this scenario must never be read as. |
| `location_review` | `{reviewed_by, date, outcome}` | The named human who approved a real location. Required unless mode is `FICTIONAL`. |

### Why `attribution_text` is a field and not markup

Attribution added by hand is attribution that a redesign deletes. Holding the required string in the
manifest and rendering *from it* means compliance cannot drift out of sync with the data, and a
single test can assert it is present. It also means changing the data source automatically changes
the credit.

---

## The required declaration

Every scenario using real geography displays this, or a per-scenario variant that preserves its
meaning:

> **This scenario uses real geography as a physical reference. Its people, organisations, events and
> outcomes are fictional. It is not a forecast or assessment of the real location.**

**Suggested improvement, preserving the meaning.** The original is accurate but abstract; a
first-time reader does not necessarily know what "physical reference" means, and the phrasing does
not say what *is* real. Recommended wording:

> **The coastlines, distances and routes on this map are real. Everything else is invented — the
> countries, the government, the companies, the people and everything that happens to them. This is
> not a prediction about the real place, and nothing here describes real events.**

It says the same thing, names the two halves concretely, and uses words a ten-year-old owns. The
formal sentence should remain available in the technical evidence view; the plain one is what the
reader meets.

For `REAL_RENAMED` scenarios, one clause must be added, because it is the thing readers most often
get wrong:

> **The place names are invented, but the geography is real and may be recognisable.**

---

## Worked example — Kestral Strait, if it moved to Mode B

```yaml
geography_mode: REAL_RENAMED
real_geography_source: natural-earth-10m-physical
real_geography_version: "5.1.2"
real_geography_sha256: "<hash of the exact TopoJSON artefact>"
displayed_location_name: "Kestral Strait"
underlying_region: "<a non-sensitive real strait, named>"
names_are_real: false
borders_are_real: true
infrastructure_status: NOT_SHOWN
alterations: []
distances_physically_accurate: true
travel_times: NOT_SHOWN
entities_are_fictional: true
real_world_data_present: STATIC_GEOGRAPHIC
map_data_last_updated: "<release date>"
licence: "public-domain"
attribution_text: NONE_REQUIRED
attribution_url: NONE_REQUIRED
known_inaccuracies:
  - "Coastline is generalised at 1:10m and is not accurate for navigation."
  - "Natural Earth boundaries follow de facto control, which is an editorial position."
prohibited_interpretations:
  - "Not a forecast about the underlying real region."
  - "No real government, port authority, company or resident is represented."
  - "Not navigational information and must not be used as such."
location_review:
  reviewed_by: "<named person>"
  date: "<date>"
  outcome: "approved — no active conflict, no disputed border, no sensitive sites in frame"
```

Note `travel_times: NOT_SHOWN`. MERIDIAN's engine does not compute travel times, so declaring
anything else would be a claim it cannot support. Real geography does **not** change that.

---

## Validation rules

These are the rules an implementation would enforce. None is implemented.

1. `geography_mode` is required and has no default.
2. `entities_are_fictional` must be `true`.
3. `real_world_data_present` of `OPERATIONAL` is **refused**, not warned about.
4. `infrastructure_status: ALTERED` requires a non-empty `alterations` list.
5. `travel_times: CALCULATED` requires `travel_time_method`.
6. `underlying_region: WITHHELD` requires `withholding_reason` — and withholding should itself be
   questioned, since a location too sensitive to name is probably too sensitive to use.
7. Any mode other than `FICTIONAL` requires `location_review`.
8. A non-public-domain `licence` requires both `attribution_text` and `attribution_url`.
9. `real_geography_sha256` is required whenever geometry comes from an external dataset — without it
   the run is not reproducible.
10. An empty `known_inaccuracies` on a real-geography scenario must be justified in review. Real data
    always has inaccuracies; an empty list usually means nobody looked.

---

## Relationship to existing metadata

MERIDIAN already emits `fictional_world` metadata on every demonstration response, "so a machine
reader cannot miss the world's status or have to infer it from prose". The geography manifest is the
same idea applied to the map, and should sit alongside it rather than inside it — the fictional-world
block answers *is this world real?*, the geography manifest answers *is this ground real?*

Those are different questions and a scenario can answer them differently.
