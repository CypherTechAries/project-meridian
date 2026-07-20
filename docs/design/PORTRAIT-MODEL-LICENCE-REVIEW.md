# Portrait model licence review

**Reviewed 20 July 2026.** Terms below were read from the licence text or model card at the URLs
given, not from third-party summaries. Where a model card states a licence *name* but not its
terms, the licence file itself was fetched — that distinction is the reason this document exists.

**No generated portrait may enter the repository before a candidate here is marked APPROVED and the
founder accepts the recommendation.**

---

## Correction to an earlier statement of mine

In `IDENTITY-ASSET-PIPELINE.md` I wrote that FLUX.1-dev is *"non-commercial and therefore unsuitable
if MERIDIAN ever commercialises."*

**That was too strong and is corrected here.** The FLUX.1-dev model card states: *"Generated outputs
can be used for personal, scientific, and commercial purposes."* The **weights** are restricted to
non-commercial use; the **outputs** are not. Since MERIDIAN would use the model offline to author
assets and would never redistribute weights, FLUX.1-dev is a legitimate candidate rather than a
disqualified one.

I have not read the full FLUX.1-dev licence file, only the model card statement, so it is marked
**REQUIRES LEGAL REVIEW** rather than approved.

---

## Candidate 1 — FLUX.1-schnell

| Field | Value |
|---|---|
| Exact model name | `black-forest-labs/FLUX.1-schnell` |
| Version | FLUX.1 [schnell], 12B parameters, Safetensors |
| Official source | https://huggingface.co/black-forest-labs/FLUX.1-schnell |
| Weights licence | **Apache 2.0** (`apache-2.0`) |
| Model/code licence | Apache 2.0 |
| Commercial use | **Permitted.** Card states the model "can be used for personal, scientific, and commercial purposes" |
| Generated-output terms | No separate output provision; Apache 2.0 imposes none |
| Attribution | Standard Apache 2.0 notice retention |
| Redistribution | Permitted under Apache 2.0 |
| Other restrictions | **None use-based** — this is the material difference from OpenRAIL |
| Licence URL reviewed | Model card, 20 July 2026 |
| Weights hash | Not recorded — **must be captured at download** |
| **Decision** | **APPROVED FOR PORTRAIT STUDY** |

**Why this is the recommendation.** Apache 2.0 carries no use-based restrictions, so nothing has to
be propagated to downstream users of MERIDIAN, and no clause interacts with a repository that is
"source available, all rights reserved". It is the only candidate with no ongoing obligation.

## Candidate 2 — Stable Diffusion XL base 1.0

| Field | Value |
|---|---|
| Exact model name | `stabilityai/stable-diffusion-xl-base-1.0` |
| Version | SDXL base 1.0 |
| Official source | https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 |
| Weights licence | **CreativeML Open RAIL++-M** (`LICENSE.md`) |
| Commercial use | **Permitted** — perpetual, worldwide, royalty-free; a fee may be charged on redistribution |
| Generated-output terms | **"Licensor claims no rights in the Output You generate using the Model."** Outputs are unencumbered |
| Attribution | Must retain all copyright, patent, trademark and attribution notices |
| Redistribution | Permitted, **with obligations** — see below |
| Other restrictions | **Use-based restrictions (Attachment A)**, including: no unlawful use · no harm to minors · **no creating or spreading deliberately false information intended to harm others** · no PII generation for harmful purposes · no defamation or harassment · no fully automated decisions affecting legal rights · no discrimination on protected characteristics · no medical advice · no law-enforcement, immigration, asylum or crime-prediction use |
| Downstream obligation | Must make the use-based restrictions an **enforceable provision** for recipients, **give notice** to subsequent users, and **supply a copy of the licence** |
| Licence URL reviewed | `.../raw/main/LICENSE.md`, 20 July 2026 |
| **Decision** | **APPROVED FOR PORTRAIT STUDY**, with one noted consideration |

**The consideration, stated plainly rather than waved past.** Attachment A prohibits using the model
to *"create or spread deliberately false information intended to harm others."* MERIDIAN generates
**portraits of admittedly fictional people, labelled FICTIONAL in the interface, inside a simulation
that exists to study how false claims move through an invented society.** That is not deception and
is not aimed at harming anyone — but it is close enough to the clause's subject matter that it
should be a conscious decision, not an assumption.

The downstream-notice obligation attaches to redistributing the **model**, which MERIDIAN would not
do. Outputs are explicitly unencumbered. So the practical risk is low — but Apache 2.0 has no such
clause to reason about at all, which is why FLUX.1-schnell is preferred.

## Candidate 3 — FLUX.1-dev

| Field | Value |
|---|---|
| Exact model name | `black-forest-labs/FLUX.1-dev` |
| Official source | https://huggingface.co/black-forest-labs/FLUX.1-dev |
| Weights licence | **FLUX.1 [dev] Non-Commercial License** (`flux-1-dev-non-commercial-license`) |
| Commercial use — weights | **Prohibited** |
| Commercial use — outputs | **Permitted.** Card: "Generated outputs can be used for personal, scientific, and commercial purposes" |
| Licence text read | **No** — model card only |
| **Decision** | **REQUIRES LEGAL REVIEW** |

Likely the highest portrait quality of the three. Not approved because I read the card, not the
licence, and the weights/outputs split is exactly the kind of asymmetry that needs the actual text.

## Candidate 4 — MetaHuman

| Field | Value |
|---|---|
| Source | Epic Games |
| Licence | Unreal Engine EULA and MetaHuman terms |
| Use outside the Epic ecosystem | **Unverified** |
| **Decision** | **REQUIRES LEGAL REVIEW** — benchmark only, not a pipeline candidate |

---

## Recommendation

**Use FLUX.1-schnell.** Apache 2.0, commercial use explicit, no use-based restrictions, nothing to
propagate downstream. SDXL is an acceptable fallback and is the model whose tooling already exists
in `C:\Users\daijo\forsyte-img-tools\`, at the cost of one clause requiring a conscious decision.

**Before the first portrait is committed:** record the exact weights file hash, the resolved model
revision, and this document's approval decision in every generation sidecar.

---

# Portrait style bible

One style, applied to every fictional person. Consistency across the cast matters more than any
single portrait being striking.

## Camera and framing

- **Crop:** chest-up. Head occupies roughly the upper third; eyeline at ~22% from the top.
- **Angle:** slight three-quarter turn, eyes to camera. Not full frontal (identity-document
  feeling), not profile.
- **Focal-length equivalent:** ~85mm portrait compression — no wide-angle facial distortion.
- **Depth of field:** shallow but not extreme; the face is sharp throughout.

## Light and background

- **Key:** single directional source, soft, slightly above eye level.
- **Fill:** low — shadow side retains detail but stays dark. Cinematic, not flat.
- **Background:** plain, near-black, subtly graded. No location, no props, no text.
- **Grade:** cool neutral, consistent across the cast, matching the interface's dark navy.

## The person

- Fictional adult. Realistic proportions, believable skin with visible texture and pores.
- Believable hair with individual strands, not a helmet mass.
- **Restrained expression.** Neutral to faintly engaged. **No smile.** No open mouth.
- Distinct facial structure per person — the cast must not look like siblings.
- Clothing appropriate to role, plausibly worn, not costume.

## Prohibitions

No exaggerated smile · no glossy app-avatar rendering · no beauty retouching or skin smoothing · no
fantasy or sci-fi styling · no military-game visual quotation · no celebrity or public-figure
reference of any kind · **no photograph of a real person as input** · no text, watermark or symbol
anywhere in frame · no role-based or background-based stereotyping.

**Photorealistic does not mean photo-derived.** Nothing enters the pipeline as a real person's
likeness, and every person stays labelled FICTIONAL in the interface regardless of how the portrait
looks.

## The three subjects

Written to specify *situation and presentation*, never capability. **Role must not determine
appearance, and appearance must never imply competence.**

| | Elian Soro | Tomas Varo | Mara Venn |
|---|---|---|---|
| Age band | 50s | 40s | 30s |
| Role | Family spokesperson | Government minister | Field correspondent |
| Build | Broader, heavier set | Narrower, upright | Medium |
| Clothing | Practical, worn, unstructured | Formal, structured, plain | Practical broadcaster field jacket |
| Expression | Tired, composed — **not** sad, not defeated | Neutral, guarded — **not** wise, **not** authoritative | Observant, guarded — **no** smile, **not** eager |
| Light | Low key, single source, left | Flat, even, institutional | Directional, cool, right |
| Explicit guard | Informality must not read as less capable | Formality must not read as more competent | Profession must not read as more intelligent |

The guard row is the point. An informal role rendered as scruffy-therefore-simple, or a ministerial
role rendered as distinguished-therefore-wise, would smuggle the exact inference the belief engine
is built to exclude — and it would do it through art, where no test can catch it.

---

# Mark review — my own QA, including a failure

Rendered sheet: [`mockups/v3-6-organisation-marks.png`](mockups/v3-6-organisation-marks.png)

| Mark | Verdict |
|---|---|
| **Government, full** | **PASS.** Compass points survive to 20px. Strongest of the set. |
| **Government, small variant** | **PASS.** Recommended below 34px. |
| **Broadcaster, full** | **PASS above 34px.** Arcs vanish below it, as predicted. |
| **Broadcaster, small variant** | **FAIL — see below.** |
| **Union A, rope and bollard** | **REJECT.** The post survives at 20px, the rope does not. Reads as a padlock. |
| **Union B, harbour geometry** | **REJECT.** Ambiguous at small size; reads as a bar chart or a bridge. |
| **Union C, chain link** | **PASS — RECOMMENDED.** Both links legible at 20px, maritime and industrial at once, no clip-art clasped hands. |

## The broadcaster small variant fails, and I am reporting it rather than shipping it

I widened the mast legs and paired the arcs specifically to break the circle-on-stem symmetry that
caused the gender-symbol reading. **It worked, and it introduced a different problem: the mark now
reads as a stick figure with raised arms.** A circle head, a body, two splayed legs and two raised
arcs is a person waving, not a transmitter.

That is a worse failure than the original, because a broadcaster whose mark looks like a human
figure implies something about the organisation that is not true — it is not a person, and the
project's whole boundary is that organisations are not human minds.

**Recommendation: do not use this variant.** Two better directions for the next pass:

1. **Drop the mast entirely below 34px** and use concentric arcs alone — a signal without a
   structure. No limbs, no head, nothing anthropomorphic.
2. **Use a letterform-pulse** — a geometric `N` with a signal pulse crossing it, from the symbol
   family already declared in `organisation-identity@1`.

Direction 1 is simpler and more likely to survive at 20px.

**The general lesson, worth recording in the recipe.** Fixing one rejection gate can trip another.
`organisation-identity@1` should require **all** gates to be re-checked after any change, not just
the one that failed — and `anthropomorphic-figure` should be added to the gate list, because it did
not exist until this attempt created it.
