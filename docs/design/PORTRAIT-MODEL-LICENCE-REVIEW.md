# Portrait model licence review

**Reviewed 20 July 2026.** Terms read from the licence text or model card at the URLs given, not
from third-party summaries.

**FOUNDER DECISION, 20 July 2026: the offline Colab route is approved. Primary model
`FLUX.2 [klein] 4B`. Fallback `FLUX.1-schnell`. SDXL and FLUX.1-dev are NOT used in this proof
pack.** This is approval for a bounded fictional portrait study — not approval to distribute model
weights, bundle model code, or make broader legal claims.

---

## CORRECTION — "nothing to propagate" was wrong

I previously described Apache 2.0 as carrying *"nothing to propagate downstream."* **That is too
broad and is withdrawn.**

Apache 2.0 imposes conditions when you **distribute the licensed work or a derivative** — retaining
copyright, patent, trademark and attribution notices, including a copy of the licence, marking
modified files, and passing on any `NOTICE` file. Those obligations attach to the model and its
code, not to a generated image. They become live the moment MERIDIAN redistributes either.

**The clean engineering posture for this study, adopted:**

| | |
|---|---|
| Model weights committed? | **No** |
| Cached model files committed? | **No** |
| Third-party inference code copied into MERIDIAN? | **No** |
| Access tokens or Colab credentials committed? | **No** |
| `NOTICE` file present in this repository? | **No** — none required, because nothing licensed is redistributed |
| What enters the repository | **Only manually approved PNG outputs, plus a sidecar record** |
| Attribution retained | Model name, exact revision, licence and source URL recorded in every sidecar **even where not strictly required for a generated image** |

The generation notebook stays **outside** this repository until it has been checked for secrets,
machine paths, caches and third-party code. If a clean notebook is later committed it must contain
only MERIDIAN-authored orchestration and installation *references* — never vendored inference code.

**This is a practical engineering decision, not legal advice.** Commercially distributing bundled
model components would need dedicated legal review.

---

## Selected model — FLUX.2 [klein] 4B

| Field | Value |
|---|---|
| Model repository | `black-forest-labs/FLUX.2-klein-4B` |
| Official source | https://huggingface.co/black-forest-labs/FLUX.2-klein-4B · https://github.com/black-forest-labs/flux2 |
| Weights licence | **Apache 2.0** |
| Commercial use | Permitted |
| Consumer-hardware suitability | Stated by the vendor; the reason it is preferred over the 12B schnell package for a small proof pack |
| Exact revision | **NOT YET PINNED** — must be captured at download |
| Weight hash | **NOT YET CAPTURED** |
| **Decision** | **APPROVED FOR PORTRAIT STUDY** |

### A pinning hazard worth naming

The `FLUX.2-klein` family contains **several repositories, and they do not share one licence.**
Search results list `FLUX.2-klein-4B`, `FLUX.2-klein-4b-nvfp4`, `FLUX.2-klein-base-4b-fp8`,
`FLUX.2-klein-9b-fp8` and `FLUX.2-klein-base-9b-fp8`. **The 4B variants are Apache 2.0; the 9B
variants are under the FLUX.2-dev Non-Commercial Licence.**

So "FLUX.2 klein" is not by itself a licence statement. Pulling the wrong repository — easily done,
since the names differ by three characters — silently changes the terms from permissive to
non-commercial. **The sidecar must record the exact repository and revision, not the family name.**

I have not read the FLUX.2-klein-4B `LICENSE` file directly; the Hugging Face page returned HTTP 401
to my fetch. The Apache 2.0 designation above comes from the vendor's own licensing page and
repository listing. **Before generation, open the model repository and confirm the licence file in
place**, then record its hash.

## Fallback — FLUX.1-schnell

`black-forest-labs/FLUX.1-schnell`, Apache 2.0, 12B, model card read directly 20 July 2026.
**Use only if the primary cannot produce convincing, consistent portraits — and record why.**
Do not switch silently.

## Not used in this pack

**SDXL base 1.0** and **FLUX.1-dev** — both previously reviewed and both defensible, excluded here
to avoid carrying licence ambiguity into a question that is purely about visual design.

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
