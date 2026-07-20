# Identity asset pipeline — portraits, marks and recipes

**DESIGN ONLY.** No frontend code, no engine change, no real-person data.

Mockups: [`identity-system.html`](mockups/identity-system.html) →
[`v3-1-identity-studies.png`](mockups/v3-1-identity-studies.png) ·
[`v3-2-society-roster.png`](mockups/v3-2-society-roster.png) ·
[`v3-3-person-dossier.png`](mockups/v3-3-person-dossier.png) ·
[`v3-4-organisation-dossier.png`](mockups/v3-4-organisation-dossier.png) ·
[`v3-5-belief-landscape.png`](mockups/v3-5-belief-landscape.png)

## What I could not deliver, and why

**Deliverables 1 and 2 — three realistic portrait studies with crops — are not present.**

I author SVG by hand. Hand-authored vector cannot produce a believable human face; it produces
exactly the app-avatar result already rejected, in a different flavour. Three more bad faces would
have consumed a review cycle and taught us nothing.

Instead the mockups carry **portrait slots**: production frame, eyeline, roster-crop rule, and three
silhouettes that differ in build so the layout conveys three distinct people without proposing three
faces. Each is stamped `PORTRAIT PENDING`. That is an honest placeholder, not a likeness.

Everything else — logo studies, both recipe schemas, the options study, all four revised screens,
the licensing record and the field list — is delivered.

## Organisation marks — three studies, delivered

| Mark | Construction | Reads as | Deliberately avoids |
|---|---|---|---|
| **National Government** | Compass rose inside a restrained shield, pointed base | Direction, jurisdiction | Flag, eagle, star, laurel, real state emblem |
| **Northshore Public Broadcast** | Transmission mast — emitter, crossbars, splayed legs — with **asymmetric** signal arcs, in a vertical shield | Broadcasting, transmission | **Circle-on-stem and the symmetry that produced the gender reading** |
| **Coastal Workers' Union** | Maritime bend knot joining two separate lines, rounded badge | Two lines made inseparable | Raised fist, clasped hands, hammer, generic clip art |

Each rendered at 150 / 56 / 34 / 20 px to prove it survives roster and favicon scale.

**Honest assessment.** The government mark is the strongest — it reads at 20px. The broadcaster is
much improved and unambiguously a mast, but its arcs disappear below ~34px, so a simplified
small-size variant is needed. The union knot reads more like a molecule than a rope at small sizes;
it is the weakest of the three and worth another pass.

## Face generation — you are right, and it changes the recommendation

Open-weight image models run locally and are seed-reproducible. Several are viable, and **SDXL
tooling already exists on this machine** at `C:\Users\daijo\forsyte-img-tools\` from the FORSYTE
slide work — including a regeneration kit and a working Colab path.

### Route comparison

| | **A · Diffusion (SDXL / FLUX), offline batch** | **B · MetaHuman as portrait studio** | **C · Blender modular head + batch render** | **D · Curated pre-rendered library** |
|---|---|---|---|---|
| Expected quality | **High** — photoreal faces achievable now | **Very high**, but recognisably "MetaHuman" | Medium without a strong art pass; skin and hair are hard | High, but fixed |
| Effort to first 3 portraits | **Low** — tooling exists | Medium-high (Unreal install, per-character authoring) | **Very high** (rig, library, shaders) | Low (procurement) |
| Effort to 200 | **Low** — batch script | High — largely manual per character | Medium once built | Impossible |
| Effort to 2,000 | **Low** | Impractical | **Low** — the strongest at scale | Impossible |
| Deterministic from a seed | **Conditional** — see the caveat below | Yes (saved asset) | **Yes, fully** | N/A |
| Batch render | **Yes** | Weak | **Yes** | N/A |
| Licensing | SDXL: CreativeML OpenRAIL++ · FLUX.1-schnell: Apache-2.0 · **FLUX.1-dev: non-commercial** | Unreal EULA; MetaHumans are **licensed for use in Epic-ecosystem projects** — needs legal review for a web product | **Cleanest** — you own the assets outright | Per-vendor; must permit commercial redistribution |
| Vite integration | PNG/WebP assets — trivial | Same | Same | Same |
| Repetitive-look risk | Medium — same model, same prompt style converges | **High** — the "MetaHuman look" | Low if the parts library is broad | High |

### Three caveats that matter more than the table

**1. "Seeded therefore deterministic" is conditional.** A diffusion seed reproduces the image only
if model weights, sampler, scheduler, step count, guidance, resolution *and* numeric precision are
all pinned — and even then, cross-GPU reproduction is not guaranteed. **Mitigation: do not treat the
recipe as the source of truth for the image. Render once, hash the output, and commit the PNG.** The
recipe records *how* the person was made; the committed asset *is* the person. That also removes the
"face changes between screens" risk entirely.

**2. Models trained on real face datasets can emit near-likenesses of real people.** This is a
direct B5 risk — MERIDIAN's whole boundary is that no real person is depicted. **Mitigation: a
mandatory review gate before any portrait enters the scenario, plus a documented check that the
output does not resemble a public figure.** No portrait should be auto-approved.

**3. Licensing must be settled before the first portrait is committed**, not after. FLUX.1-dev is
non-commercial and therefore unsuitable if MERIDIAN ever commercialises. FLUX.1-schnell (Apache-2.0)
and SDXL (OpenRAIL++) are the safe candidates. MetaHuman needs real legal review before its output
lands in a web product outside Unreal.

### Recommendation

**Near term — Route A.** Use the existing SDXL tooling as an offline portrait studio. Produce
12–20 art-directed portraits for the first cast, one at a time, each manually reviewed and approved.
Render three crops (roster, dossier, master), hash them, commit them as ordinary local assets. The
site consumes PNGs and knows nothing about the generator.

**Long term — Route C.** A seeded Blender modular-head pipeline is the only route that reaches
2,000 people with full determinism and clean ownership. Build it incrementally from the approved
art direction established in the near-term pass.

**MetaHuman: benchmark only.** Use it to calibrate what "good" looks like. Do not make it a
dependency.

**Not negotiable either way: Unreal and Blender never enter the runtime web application.** Portrait
generation is an offline authoring step. The site consumes approved local image assets.

## `character-appearance@1`

```jsonc
{
  "schema": "character-appearance@1",
  "character_id": "fict:kestral-strait:person:broadcast-journalist",
  "appearance_seed": 831924,
  "assets": {                      // selected library part ids
    "base_head": "head-07", "hair": "hair-mid-11", "eyewear": null,
    "clothing": "field-jacket-03"
  },
  "facial_parameters": {           // continuous, where the renderer supports it
    "jaw_width": 0.42, "nose_bridge": 0.61, "eye_spacing": 0.48,
    "brow_depth": 0.55, "age_detail": 0.34
  },
  "materials": { "skin": "skin-18", "skin_tone": 0.46, "hair_colour": "dark-brown",
                 "eye_colour": "grey-blue" },
  "camera_preset": "dossier-3q-neutral",
  "lighting_preset": "newsroom-cool-right",
  "expression_preset": "observant-neutral",
  "renderer": { "engine": "sdxl", "version": "1.0", "sampler": "dpmpp_2m",
                "steps": 40, "guidance": 5.5, "precision": "fp16" },
  "outputs": {                     // the committed assets ARE the person
    "master":  { "path": "assets/people/mara-venn/master.png",  "sha256": "…" },
    "dossier": { "path": "assets/people/mara-venn/dossier.png", "sha256": "…" },
    "roster":  { "path": "assets/people/mara-venn/roster.png",  "sha256": "…" }
  },
  "origin": "FIXTURE",
  "approval": { "status": "PROPOSED", "reviewed_by": null, "reviewed_at": null,
                "likeness_check": null }
}
```

**Structurally separate from — and unable to reach — belief state, motivations, competence,
biography and every behavioural parameter.** Appearance is visual identity, not psychology.

**Prohibited couplings, to be enforced by test:** no appearance field may influence intelligence,
competence, morality, beliefs, aggression, political position, susceptibility or persuadability. A
scar must not make someone violent. Formal clothing must not make someone competent.

## `organisation-identity@1`

```jsonc
{
  "schema": "organisation-identity@1",
  "organisation_id": "fict:kestral-strait:organisation:public-broadcaster",
  "identity_seed": 24118,
  "category": "public-broadcaster",
  "symbol_family": "signal-tower",     // tower | waves | microphone | horizon | letterform-pulse
  "badge_geometry": "vertical-shield",
  "internal_geometry": "asymmetric-arcs",
  "palette": { "primary": "violet", "secondary": "silver" },
  "wordmark": "civic-modern",
  "line_weight": 2.4,
  "complexity": "medium",
  "renderer": { "engine": "svg-compositor", "version": "1" },
  "outputs": { "mark": { "path": "…/mark.svg", "sha256": "…" },
               "mark_small": { "path": "…/mark-20.svg", "sha256": "…" } },
  "origin": "FIXTURE",
  "approval": { "status": "PROPOSED", "reviewed_by": null,
                "rejection_checks": ["gender-symbol", "real-company-mark", "national-emblem",
                                     "party-mark", "religious-symbol", "extremist-symbol"] }
}
```

**Symbol families:** broadcaster → tower · waves · microphone · horizon · letterform-pulse ·
government → civic architecture · seal · compass · restrained shield · union → connected forms ·
knot · maritime tools · shipping → vessel · route · wave · container · research → lens · grid · star.

**Every output passes the rejection checks before entering a scenario.** The v2 broadcaster mark
failed the gender-symbol check, which is why that check now exists as a named gate rather than as
taste.

## Asset origin and licensing record

| Asset | Origin | Licence | Notes |
|---|---|---|---|
| Three organisation marks | **Original**, hand-authored SVG, this repository | Repository terms (source available, all rights reserved) | No real logo referenced, traced or adapted |
| Population-group symbols | **Original**, hand-authored SVG | Same | Many marks, never one figure |
| Portrait silhouettes | **Original**, hand-authored SVG | Same | Placeholders, not likenesses |
| Portraits | **Do not exist** | — | Route A pending approval; licence decided by model choice before first commit |
| Fonts | Inter / system stack | OFL / system | Unchanged from the existing UI |
| MGSV | **Not used** | — | No asset, interface trade dress or character design used or referenced |

## Proposed vs engine-backed

**Engine-backed `E`** — belief before/after, movement, confidence, exposure and route, organisation
internal blocs, cohesion, official position, strength, direction, force, group averages, population
counts, unavailable-breakdown status, and the substitution claim.

**Fixture `F`** — role labels, biographies, organisation names and objectives, threshold rationales,
exposure paths.

**Proposed `P` — does not exist** — every personal name, every portrait, every organisation mark,
community, priority, pressure, and the "tied to" relationship line.

**Not modelled `?`** — life stage, household, relationships, recent history, memories, emotions,
cumulative stress, changing trust, information order, named individuals inside an organisation,
group internal breakdown, group confidence.

## What I recommend next

1. **Settle the model licence** — FLUX.1-schnell (Apache-2.0) or SDXL (OpenRAIL++). Blocks
   everything else.
2. **Three portraits through Route A**, manually reviewed, likeness-checked, committed as assets.
3. **Drop them into these exact slots** — the layouts are already built for them.
4. **Then** judge whether the screens feel like a serious synthetic society. That judgement is not
   available until real faces are in the frames.

Neither PR #14 nor PR #15 is affected. No frontend code was written.
