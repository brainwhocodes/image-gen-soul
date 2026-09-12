# Production layouts and delivery

The same reference can support different assets, but different destinations need
different composition. The goal is not to stretch one image into every shape.
Use explicit project dimensions first. Where current platform restrictions,
accessibility compliance, or printer requirements matter, check the current
primary specification instead of relying on a memorized template.

## Common workflow

Decide the intended view size and crop before generation. Record a focal area,
copy-safe area, and any region that may be cropped. Generate or edit the artwork,
inspect construction, and grade the art before overlaying exact production
elements. Compose supplied marks and exact copy using layout tools. Inspect the
actual exported artifact, not just its source canvas.

When the user supplies an exact logo, product image, QR code, screenshot, or
lettering asset, use those pixels/vector paths where practical rather than asking
the image model to approximate them. Do not bundle fonts. A named font is usable
only if it is available to the host and its use is permitted; otherwise disclose
a substitution without claiming an exact match.

## Social posts and campaign series

Use the requested aspect ratio and intended placement. When absent, choose a
reasonable working canvas and label it an assumption, not an official platform
specification. Confirm current placement-specific constraints before asserting
safe-zone or upload compliance.

Keep the visual hierarchy legible at phone scale. Limit decorative competition
near the title, person, product, or action. Reserve intentional breathing room;
negative space is designed space, not permission to fill every area with detail.
Protect essential content from platform overlays where current layout evidence
is available. Test the crop, not just the outer dimensions.

For carousels and campaigns, preserve the approved treatment, type hierarchy,
margins, color intent, and subject rendering across assets. Allow composition to
change for the content. Do not use a histogram match to force unrelated slides
to have identical proportions of light and dark areas.

When exact text is important, produce art without that text and place the copy
deterministically afterward. Verify spelling, prices, dates, handles, and action
labels against user-supplied content. Do not invent an offer or event detail to
make the graphic feel complete.

## Website heroes and section backgrounds

Determine where live HTML text and controls will sit. Reserve the requested
side or center of the image and keep the visual focal point away from that area.
Default to a clean background without rasterized heading or button text unless
the user explicitly requests a flattened mockup.

Account for real container behavior. A wide desktop composition can lose its
subject when cropped vertically on mobile. Provide separately composed crops or
art-directed versions when a single crop cannot satisfy both. Record proposed
focal position and intended use of `object-position`/background positioning in
the handoff; test in the actual layout when code and rendering tools are available.
Do not claim responsive behavior was checked without rendering it.

Match the reference's actual rendering language. Do not add generic gradient
blobs, glossy 3D objects, grain, or fashionable filters that were not requested.
The background should support the interface rather than compete with it.

Use a lossless master and a delivery format supported by the project. Treat a
file-size target as a project requirement, not a universal rule. Verify that
compression does not introduce visible banding, halos, or alpha fringes. Keep
text live in the web layer and check contrast in its actual placement. Do not
claim accessibility conformance from a palette sample alone.

## Flyers, posters, and print-oriented content

Separate content accuracy from art direction. Obtain exact title, date, location,
contact details, action, and any legal copy needed for a final production file.
For an early visual draft, use clearly marked placeholders only when appropriate
and never call that draft final.

Obtain physical trim dimensions and the printer's required bleed, safe margin,
resolution, export format, and color handling. Do not treat a web PNG as
printer-certified. Keep an RGB master; create a printer-specific derivative only
with the necessary specification and color-management support.

Raster dimensions follow physical dimensions multiplied by the intended pixel
density, including any required bleed. Changing a DPI metadata tag does not
create missing image detail. Upscaling must be disclosed as upscaling, not
represented as native resolution. Use the available document tools for a requested PDF or editable file; honor
any user restriction on additional skills.

Render and inspect the final page at both whole-page and readable-text scale.
Check clipping, margin consistency, spelling, logo fidelity, and exported page
size. Produce a genuinely functional QR code from the approved payload using a
deterministic encoder, then test decoding after placement and export. Do not
rely on image-generated QR-like patterns.

## Layers, transparency, and exact assets

Use actual alpha, not a drawn checkerboard or white background mislabeled as
transparent. Inspect edges against more than one background. Avoid double
premultiplication, dark halos, missing interior gaps, and clipped strokes.

Foreground and background artwork can share a coordinated color treatment after
compositing. Place exact brand assets on top afterward, or explicitly protect
them in the grade. If the requested effect intentionally changes those colors,
record the exception rather than silently overriding the brand constraint.

## Aspect ratios and coordinated content

Plan an asset map before generation: page/region, purpose, subject, original treatment
anchor, aspect ratio, intended pixel size, focal area, copy-safe area and exclusions.
For content inside a selected UI concept, follow [Page mockups](page-mockups.md):
generate new pictures individually before implementation, never slice the mockup.

These are working compositions, not current platform specifications:

| Shape | Useful placements | Composition check |
|---|---|---|
| 3:2 or 16:9 | Hero, landscape editorial, section background | Reserve live-copy space; protect focal subjects in the actual container |
| 1:1 | Product tile, cover or compact comparison | Keep complete silhouettes and consistent scale across the set |
| 4:5 | Portrait card, lookbook or product story | Give the subject vertical room without cutting required details |
| 9:16 | Mobile artwork or tall campaign composition | Recompose for the narrow frame; keep essential details away from overlays |

Specify what changes between shapes; never stretch one image. A wide hero might
place the subject on the right with quiet space to the left, while its portrait
counterpart recenters the subject and leaves space above. Record and test focal
position in the actual HTML container. Export a separate mobile composition when
one crop cannot preserve the subject and copy area. Label requested versus returned
dimensions honestly.

For a series, keep camera logic, material treatment, lighting and the approved
identity coherent while changing the named people, products or scene elements.
Return to the original selected anchor rather than chaining derivatives. Separate
actual product identity from illustrative placeholders; label fictional sample
products and do not invent provenance, availability or performance claims.

Inspect every image in the set for composition, subject count, anatomy, product
construction, unwanted lettering and crop compatibility. Keep the inspected raw
file, exact prompt, attachments, palette, correction decision and delivery export.
Write alt text for the actual image's role; decorative backgrounds need no invented
description. Reuse the same approved file when the same image is intentionally
shown again, rather than claiming a duplicate generation.

## Delivery choices

Do not output every possible file by default. Deliver the requested final image
and any necessary alternate crop or editable file. Retain raw artwork, prompt,
recipe, masks, and QA locally when practical. Provide them when requested.

Describe uncertain or unverified items plainly: draft copy, untested responsive
crop, unavailable printer profile, missing font, or a correction not yet run.
Do not substitute a mockup for a requested production asset without saying so.
