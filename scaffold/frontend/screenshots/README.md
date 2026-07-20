# Screenshots

## `current/` — approved product images

These are the **only** images that may be used in the public README, the GitHub social preview, or
release material.

| File | What it shows |
|---|---|
| `briefing-laptop.png` | Briefing View at 1440×900 — the default experience and the public hero |
| `briefing-desktop.png` | Briefing View at 1600×1000 |
| `briefing-crop.png` | Crop-safety capture: one consequence card alone, still carrying its origin marker |
| `analysis-technical.png` | Analysis View — the detailed dashboard, for technical inspection |

## `archive/` — superseded design iterations

**Archived images do not represent the current UI.** They are retained to show design progress and
must never be used publicly.

| Directory | What it contains |
|---|---|
| `c0-fixture-dashboard/` | The first fixture-only screen, before any engine integration |
| `p0-5-first-integration/` | The first live engine→UI integration and its polish pass |
| `command-centre-redesign-passes/` | The three redesign passes and the clipping correction |

## Rules

- Do not delete historical screenshots; they are the record of how the interface got here.
- Only `current/` may appear in public-facing material.
- When a screen changes materially, move the superseded image into a clearly named `archive/`
  directory rather than overwriting it.
- `scripts/shots.mjs` writes to `current/` and measures the acceptance criteria as it captures —
  clipping, ellipsised text, horizontal overflow, disclosure presence, and whether any raw engine
  machinery has leaked into Briefing View.
