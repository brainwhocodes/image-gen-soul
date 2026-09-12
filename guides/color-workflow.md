# Reference-relative color workflow

Use the current reference images and current prompt to decide what the final
colors should do. This guide contains no reference look, style profile, fixed
palette, seasonal preset, or preselected hue family. The helper's limits are
engineering safeguards, not an aesthetic prescription.

## 1. Decide whether to correct

First inspect the actual raw image next to the selected color anchor. Identify
specific discrepancies: unwanted cast, weak or excessive colorfulness, compressed
midtones, lost separation, a shifted accent, or inconsistent rendering between
variants. Distinguish these from deliberate changes requested in the prompt.
“No correction needed” is a valid conclusion.

Do not grade to fix geometry, artifacts, bad text, subject identity, or texture
that should have been established during generation. Do not apply a global
filter simply because a workflow contains a color stage.

## 2. Choose comparable evidence

Use only references assigned a color role. Use one principal anchor when possible.
When multiple references genuinely share the intended treatment, assign explicit
relative weights. The helper gives each reference its assigned total weight
rather than letting image resolution determine its influence.

Global statistics can be misleading when content changes. A reference dominated
by a dark subject does not prove the new white-background design should be dark.
Likewise, a logo screenshot's empty canvas is not a creative color target.
Choose comparable regions with masks or separate representative crops. Keep
exact logos, live text, screenshot chrome, and unrelated content out of the
measurement when they would bias it.

The helper has no semantic segmentation. You or the host agent must choose
regions and supply masks. Do not describe a whole-image statistical fit as
object-aware matching. The tool does not accept natural-language instructions;
the agent translates the prompt into a reviewed numeric recipe.

## 3. Inspect current files

From the skill directory, after installing `requirements.txt`:

```bash
python scripts/color_pipeline.py inspect /actual/reference.png /actual/raw.png \
  --report /actual/job/measurements.json
```

Use actual verified paths. Output records file hashes, orientation, dimensions,
alpha, color handling, and sampled Oklab lightness/chroma quantiles. Sampling is
deterministic and limited to a grid of at most 512 by 512 points per image.
Invisible pixels are excluded and partial alpha is weighted. A tiny selection
may require cropping or a larger analysis mask.

These are job-local measurements, not saved reference profiles. The report does
not identify objects, infer fonts, or claim any color has a particular semantic
role. The near-black/near-white channel fractions are warning indicators, not
proof that an image is clipped or defective.

## 4. Fit a restrained starting recipe

```bash
python scripts/color_pipeline.py fit /actual/raw.png \
  --reference /actual/color-anchor.png \
  --recipe /actual/job/grade.json
```

For compatible references with deliberately selected weights:

```bash
python scripts/color_pipeline.py fit /actual/raw.png \
  --reference /actual/anchor.png --reference /actual/supporting.png \
  --weights 3,1 --strength 0.30 --recipe /actual/job/grade.json
```

`fit` measures the chosen files and writes a fresh job-specific recipe. It does
not alter any image. Its automatic proposals are deliberately bounded:

- Lightness corrections are derived from measured percentile discrepancies,
  limited before blending, and represented by a monotonic curve with restrained
  slopes. Flat source/reference data skips the automatic tone fit.
- Chroma changes are derived from comparable colored-sample medians and capped
  near unity. Sparse colored evidence skips automatic chroma matching.
- There is no automatic hue-family remapping or global temperature preset.
  Low-chroma cast matching is disabled unless `--match-neutral-cast` is supplied.
  That option still uses pixel statistics, not an understanding of neutral objects.

A large palette transformation belongs in the generation brief or in explicit,
reviewed corrections. The conservative fit is not intended to turn arbitrary
images into a completely different palette in one step.

Fit does not always improve an image. View the candidate and retain the original
when the reference is semantically incomparable or the result is worse.

## 5. Use analysis masks and application masks correctly

All masks must be opaque grayscale, with the same displayed/oriented dimensions
as the image they belong to. Gray gives partial selection. The helper does not
automatically resize masks or create masks from object names.

For fit, `--source-mask` limits source measurement. Repeat `--reference-mask`
once per reference, using `-` for a reference without a mask. These masks affect
measurement only; they do NOT restrict where a subsequent grade is applied.

```bash
python scripts/color_pipeline.py fit /actual/raw.png \
  --source-mask /actual/raw-analysis-mask.png \
  --reference /actual/anchor.png \
  --reference-mask /actual/reference-analysis-mask.png \
  --recipe /actual/job/grade.json
```

For apply, `--mask` means white = apply and black = leave unchanged.
`--protect-mask` means white = protect and black = permit changes. They can be
combined. For exact logos, text, or products, keep protected interiors fully
white in the protection mask and review any feathered boundary.

## 6. Translate prompting into numeric corrections

Read the recipe and edit only fields justified by the current instruction and
visible discrepancy. Do not translate “winter” into a stored cool preset or
“luxury” into a stored warm grade. Ask what the supplied images actually show.

| Setting | Meaning |
|---|---|
| `strength` | Overall mix of all corrections, 0 to 1. Zero is a true no-op. |
| `exposure_ev` | Linear-light exposure adjustment before the other operations, blended by strength and masks. This is not RAW highlight recovery. |
| `lightness_curve` | Monotonic Oklab lightness control points; `x` runs from 0 to 1. |
| `lightness_offset` | Explicit overall lightness adjustment. |
| `chroma_scale` | Colorfulness multiplier, not a semantic or brand-specific correction. |
| `neutral_shift_ab` | Small intentional Oklab opponent-channel shift, restricted to low-chroma midrange samples. It does not mean neutralize every pale area. |
| `neutral_protection` | Reduces chroma/hue changes around nearly neutral pixels. |
| `highlight_protection` | Softens changes near the lightness ceiling to reduce unnecessary damage. |
| `hue_adjustments` | Explicit circular Oklch hue bands, empty by default. |

Every hue-band entry must explicitly name `center_deg`. Optional fields are
`width_deg`, `rotation_deg`, `chroma_scale`, and `lightness_offset`. These angles
are **Oklch**, not HSV/HSL. The helper supplies no list of preferred hue centers.
Bands use smooth falloff around the circle and do not select semantic objects.
Overlapping bands add their changes, so inspect overlaps and avoid contradictory
adjustments. Use a spatial mask to distinguish similarly colored objects.

For a correction-only request with no suitable matching reference, the agent
may write a manual recipe. Its neutral starting scaffold is:

```json
{
  "schema_version": 1,
  "source": null,
  "references": [],
  "settings": {
    "strength": 0.0,
    "exposure_ev": 0.0,
    "lightness_offset": 0.0,
    "lightness_curve": {"x": [0.0, 1.0], "y": [0.0, 1.0]},
    "chroma_scale": 1.0,
    "neutral_shift_ab": [0.0, 0.0],
    "neutral_protection": 1.0,
    "highlight_protection": 0.65,
    "hue_adjustments": []
  }
}
```

This scaffold changes nothing. Set a nonzero strength and justified adjustments
only after inspecting the actual input. Add the source hash/path returned by
`inspect` to lock it to the right file. A missing source hash produces a warning.
Never characterize a manually chosen number as automatically measured.

## 7. Apply once from the untouched original

```bash
python scripts/color_pipeline.py apply /actual/raw.png /actual/job/graded.png \
  --recipe /actual/job/grade.json --report /actual/job/color-qa.json
```

For protected regions:

```bash
python scripts/color_pipeline.py apply /actual/raw.png /actual/job/graded.png \
  --recipe /actual/job/grade.json \
  --protect-mask /actual/locked-elements.png \
  --report /actual/job/color-qa.json
```

An optional `--strength`, `--exposure`, or `--chroma-scale` overrides that numeric
field without editing the stored recipe; the QA report records the actual applied
settings. All adjustments, including exposure, are blended by strength and masks.
Zero strength leaves normalized sRGB pixels unchanged.

By default, a fitted recipe checks the input file's hash. A different source
requires refitting or explicit `--allow-new-source`. Do not reuse a fit blindly
for a new composition. For a campaign, preserve the creative target while
fitting each raw render appropriately; identical numbers are not the same as
consistent appearance.

The implementation converts sRGB to linear light and Oklab for its operations,
reduces out-of-gamut chroma rather than simply clipping every excursion, and
mixes the result in linear light. It processes rows in chunks to reduce working
memory. It performs no sharpening, blur, synthetic texture, resizing, or content
generation. All image adjustments are local computation.

Original images, references, recipes, and masks are guarded against accidental
overwriting. Existing unrelated outputs require `--overwrite`. Keep versioned
outputs anyway. When testing another recipe, begin with the raw image again,
not the previously corrected file.

## 8. Review the actual result

```bash
python scripts/color_pipeline.py compare /actual/raw.png /actual/job/graded.png \
  /actual/job/comparison.png --reference /actual/color-anchor.png
```

Inspect the preview plus full-resolution details. The preview is a convenience,
not an automatic pass/fail judge. Check whether the intended relationships are
closer, whether details survive, and whether preserved elements changed. Inspect
real alpha edges on different backgrounds with the host's image tools.

The QA report verifies the saved file's displayed dimensions and alpha, records
the applied recipe, and measures before/after statistics. It marks visual review
as not performed by the script. The agent must do that review and record the
result separately. Do not claim a measured similarity score that the tool does
not calculate.

## 9. Boundaries and delivery

The helper accepts single-frame display-referred images through Pillow. It
normalizes EXIF orientation, converts usable embedded ICC profiles to sRGB,
assumes untagged RGB/grayscale input is sRGB, and rejects ambiguous untagged
CMYK/LAB. Invalid embedded profiles are errors, not silently ignored. It rejects
common high-bit-depth inputs instead of presenting 8-bit output as HDR/RAW or
16-bit mastering. Supply a properly exported sRGB working copy when needed.

Output is 8-bit tagged sRGB PNG, JPEG, lossless WebP, or TIFF. Real alpha is kept
where the format permits it; JPEG with nonopaque alpha is rejected. Exact
protected RGB is maintained relative to the orientation-corrected, normalized
sRGB working image before encoding. JPEG's lossy encoding can change it afterward.
Color management itself may necessarily change encoded source bytes.

For 16-bit mastering, camera RAW, HDR, wide-gamut preservation, or printer-specific
CMYK proofing, use an appropriate supported color-managed pipeline rather than
claiming this helper provides those capabilities. For an external LUT/filter,
use one only when justified by the reference/brief, apply it gently, and document
it. The helper does not import LUT files. Do not add filters by default.

Implementation sources: the Oklab conversion is based on Björn Ottosson's
published transform, and color-profile/orientation handling uses Pillow's
ImageCms and ImageOps interfaces. See [Oklab](https://bottosson.github.io/posts/oklab/),
[ImageCms](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html) and
[ImageOps](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html).
Use [Production layouts](production-layouts.md) for the final export and exact overlays.
The workflow decisions, fitting bounds, and QA requirements are authored
for this skill; they are not promises of automatic visual equivalence.
