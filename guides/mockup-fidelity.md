# Keep mockups, generated assets and implementation aligned

Use this guide when implementing an image-led layout or repairing drift. It adds
acceptance gates to [Page mockups](page-mockups.md) and
[UI implementation](ui-components.md); it does not require new concepts for a
small repair, nor authorize publishing or installing models. User instructions
and accessibility constraints take precedence over a mockup's accidental defects.

## Freeze the selected reference, not an approximation

Record the selected mockup's file/hash, page or section, intended viewport and
state before implementing it. Keep the untouched reference separate from browser
captures. If an image's intended viewport is unknown, record the chosen comparison
frame as an assumption; raster dimensions alone do not identify a CSS viewport.

For each important region, record the relationships that must survive:

- Headline, supporting copy and action placement, alignment, readable measure and
  relative scale; preserve the hierarchy without copying raster text errors.
- Artwork's visible subject bounds and focal point, not just the image element's
  box. Transparent padding can make equally sized elements look very different.
- Subject pose, gesture, gaze, expression, orientation, props, framing and identity.
- Layer order, intended overlap, section boundary and regions that must stay clear.
- Desktop composition and narrow adaptation: what moves, stacks, resizes or crops,
  and which essential details remain visible. Mark inferred mobile layouts as such.

An equivalent job record is enough; the optional
[fidelity record](../templates/fidelity-record.json) links these decisions to
assets and captures. Choose useful bounds or landmarks and tolerances for the
actual brief; do not invent a universal pixel-match percentage.

## Match each pictured pose before wiring the asset

Make a slot-to-asset map. “Same mascot” or “same palette” is insufficient when the
mockup depicts a different gesture, silhouette, crop or prop. A seated character
cannot silently replace a reaching hero pose. Reuse a file only when the intended
pose and composition really match; repeated uses of that same pose can share it.

Attach the selected mockup as the **composition/pose** reference and the original
approved character or product asset as the **identity/treatment** reference. Name
these roles in the prompt and pass the actual inspected images to the tool. Return
to these anchors for each pose instead of chaining progressively changed outputs.
Explicitly preserve costume, proportions, face, mark and palette when required;
specify gesture, handedness, gaze, expression, props, full silhouette, crop and
transparent gaps. Exclude the surrounding interface and its text.

Inspect each standalone output beside the selected mockup at useful scale before
implementation. Compare the silhouette, pose and negative space, not only the
face. Reject material mismatches; edit or regenerate just the affected asset with
the correct references. Do not compensate with arbitrary CSS flips, stretching,
clipping off a needed hand, or substituting another pose. Mirroring can reverse
marks, handedness and intended visual direction. An inspected exact supplied asset
can be reused; a flattened UI mockup must not become the production asset source.

## Cutout acceptance: alpha is necessary, not sufficient

When a layer is intended to be transparent:

1. Inspect the actual alpha channel. RGBA mode, a `.png` extension, clear corners
   or a successful segmentation call alone do not prove a clean cutout. A drawn
   checkerboard can remain opaque between hair strands or inside prop gaps.
2. Composite the final export on solid light, dark and actual destination colors.
   Review the full silhouette at placement size **and** edge/gap crops at 100% or
   larger. Inspect hair, fingers, fabric, straps, glass, foliage and prop openings
   where present. Thumbnail contact sheets do not replace full-resolution review.
3. Reject checker fragments, gray/white/color fringes, dark premultiplication halos,
   unwanted matte/shadows, clipped strokes, erased details and missing interior
   gaps. Check opaque interior details too: a cleaner outline with holes in a bag
   strap, face or clothing is not an improvement.
4. If local removal is permitted by the host and user, use an appropriate model or
   trimap/matting workflow. Ask only when required authorization is missing. Do not
   globally key out gray or white: those colors may belong to the subject. Protect
   real interior artwork while correcting background islands; refine mixed edge
   colors as well as alpha. Pose-specific masks belong in the job, not this skill.
5. Preserve source/raw images, masks/recipe and a lossless master. Export a versioned
   delivery file, reopen it and repeat the checks after compression. Compare against
   the original for lost detail; record dimensions and any intentional canvas trim.
   Recheck placement if bounds or transparent padding change. Update actual asset
   references/cache keys so the browser loads the reviewed export.

The optional [asset review helper](../scripts/asset_review.py) writes full-size
solid-background composites, alpha, selected detail crops and a factual report.
It never removes backgrounds or certifies visual cleanliness. For example, using
verified job paths and a project-specific background:

```sh
python scripts/asset_review.py job/mascot.webp job/qa/mascot-v2 --require-alpha --background '#eee6f4' --crop 40,20,240,280
```

The output directory must be new. Crop coordinates are displayed pixels `x,y,w,h`
after EXIF orientation is applied; choose them after inspecting the image. The
helper normalizes embedded color profiles to tagged sRGB and records the sRGB
assumption for untagged RGB/grayscale. Unsupported profiles, animation and HDR
inputs are rejected, not silently approximated. Default light/dark backgrounds
remain included. No model, network service or new dependency beyond the package's
existing Pillow/NumPy requirements is needed. A zero exit code reports only successful
artifact creation and, if requested, nonempty transparency—not visual approval.

## Preserve intentional overlap without hiding the design

Use the reference's text/art relationship, including asymmetry and modest overlap
when intended. Do not retreat into unrelated side-by-side cards just because
overlap requires layout work. Specify which layers sit behind/in front and which
parts may cross a section boundary. Check stacking contexts and ancestor overflow,
not only a large `z-index`; reserve the needed space in normal layout flow.

Keep the face, meaningful gesture, heading, actions and focus indicators visible
unless an explicit reference calls for a particular harmless crop. Decorative art
must not intercept pointer events or cover an expanded menu. Text needs contrast
over its actual background. At narrow widths, recompose intentionally—often with
reduced overlap or a separate art row—while preserving hierarchy, identity and key
pose details. Do not shrink the whole desktop design or silently hide the mascot.
Inspect intermediate widths, 320px, enlarged text and relevant expanded/error states.

## Compare with ODiff and actual browser evidence

Capture the working route after fonts and images load, at the recorded viewport,
scale and state. Stabilize only nondeterministic content relevant to the comparison;
record what was fixed or masked. Preserve live text and working interactions.

Use ODiff when available, and whenever the user specifically requests it. Inspect
the installed tool's help/API before invoking it; record the exact version, command,
inputs, options, result and output diff. If unavailable, disclose that limitation;
use an available overlay/diff tool and manual review without claiming ODiff ran.
Do not silently install tooling when the host or user's permissions forbid it.

Compare aligned full-page/section captures and focal-region crops. Keep originals
untouched; label any comparison-only resize/crop, preserve aspect ratio and coordinate
space, and never nonuniformly stretch screenshots to improve a score. A generated
mockup is not a pixel-identical browser golden: inspect the diff for geometry,
hierarchy, missing art, scale, crop and layer order rather than failing solely on
raster typography or antialiasing. A low overall difference can hide a covered face;
a high one can reflect live text rendering. Review the important regions directly.

Fix asset identity/pose, major geometry and occlusion first, then text placement,
spacing and finer treatment. Rerender and rerun affected comparisons. Do not mask
out the mascot or change thresholds just to pass. Keep visual-fidelity evidence
separate from functional/a11y checks; passing interactions does not prove a match.

If the implementation accidentally drifts, correct it against the selected mockup.
Do not regenerate a reference from the drifted page to retroactively approve it.
For a necessary accessibility/responsive change, record the reason and affected
region. For an intentional new design direction, obtain any material missing user
choice and select a new reference before implementing that direction. Preserve the
old reference as history. A repair to the selected direction needs no new mockup.

## Completion gate

Report only reviewed assets and observed pages as complete. Each changed template
needs its selected reference, actual loaded asset versions, desktop/narrow captures,
diff/overlay evidence (or stated limitation), a regional visual review and relevant
interaction checks. Include shared placements and intentional adaptations. Keep
unreviewed routes, rough cutouts or blocked tools explicit; a contact sheet or alpha
test alone cannot close this gate. Store job evidence outside this reusable package.
