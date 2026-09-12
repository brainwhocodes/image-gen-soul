# Generate the site page by page

Use the completed [brand kit](brand-first.md) as an actual image attachment before generating interface mockups. This is a design-before-code workflow. Generating artwork alone, describing a layout in prose, or taking a screenshot after coding does not satisfy it. After selecting and preparing the required assets, continue with [UI implementation](ui-components.md).

## Map every navigation destination

Write a page inventory before generation. For every header, sidebar, menu and footer navigation link, record its visible label, exact destination, page purpose, primary action and required state. Include nested navigation and important item-detail or conversion destinations reached by the primary action. Group repeated item routes only when they use the same intentional template; generate one representative with real content and verify the longest and empty variants in code.

Classify links explicitly: designed internal page, section anchor, existing shared documentation, external destination, file download or action. Every distinct page within the requested design scope needs a page-specific generated mockup. An anchor must point to a section visible in a generated page or continuation. External sites and downloads need working links, not invented destination mockups. Existing shared documentation can retain its inspected design only when outside the redesign scope; record that boundary. Never hide an unimplemented promised page behind a hash link, route every button to one generic screen, or exempt an app screen because a marketing mockup exists.

Use `templates/page-inventory.json` as optional job-local scaffolding. The reusable skill contains no default brands or page aesthetic.

## Explore real composition variations

When the user requests different styles, or when a family of example sites risks repeating one layout, generate at least two distinct directions for the relevant page before implementation. Attach the same inspected brand-kit screenshot to both. Hold the approved identity steady, then name at least three structural axes of variation: navigation placement, headline alignment, image scale and arrangement, column structure, content density, section order, framing, or the conversion format.

For example, compare a poster-led programme with an editorial index; do not merely swap two background colors. These are examples of axes, not mandatory visual styles. Choose the actual alternatives from the reference images, site purpose and content. Preserve one coherent direction within each site; do not randomize each page independently. Across distinct brands, inspect a comparison of the actual returned mockups and reject repeated silhouettes that differ only in copy, fonts or colors.

Record what is held constant, what varies, the exact outputs, observations and selection reason. Reuse earlier user choices and delegated authority. If the user asked to choose among alternatives, show the images and wait for that choice; otherwise select using the established brief and explain the decision without adding a new approval gate.

## Generate every page in the selected direction

Attach the actual brand-kit screenshot and the selected page mockup through the host tool's supported reference mechanism. The kit controls the generated logo, typography, imagery and color roles. The selected page controls the shared design language. Each destination's content and task control its composition. Generate separate page images at a readable scale; a tiny sitemap collage does not count as complete page mockups.

For a long page, generate an opening and as many readable continuation views as needed to cover the substantial content and navigation anchors. Include concrete copy, representative products or sample data, content depth and a clear conversion route. Keep controls and labels legible rather than compressing an entire site into one tiny image. Specify the aspect ratio and which vertical portion each image covers. Generate changed or materially new compositions before implementing them, including later lower-page additions. Existing unchanged components do not need repeated generation.

Generate key task states when their visual structure changes: product detail, basket, booking selection, comparison, empty results or completion. The implementation must still support all functional, error and keyboard states even when a small state difference can reuse the selected layout. Do not replace the product brief with marketing language.

## Generate the images inside the mockup separately

A UI mockup is a composition reference, not an asset sheet. Before implementing it, inventory every pictured hero, product, person, illustration, editorial scene, thumbnail, background and other content image. Generate each required image as a separate image-generation output with its own prompt, dimensions, aspect ratio and inspection. Do not crop the UI mockup, slice a screenshot, recreate the picture with CSS, use a remote stock substitute, or bake interface text into a page-sized bitmap instead of generating the underlying artwork.

Attach the selected mockup as the composition reference for the individual asset and the actual brand kit or original image as the treatment/identity reference. Describe only the image to create: its subject, viewpoint, lighting, medium, background, crop and reserved space. Explicitly exclude surrounding UI, captions, buttons, borders and device frames. Generate different crops or compositions when hero, card and thumbnail uses require them; do not stretch an image to fit. Keep the generated logo as its own asset and implement the wordmark and exact interface copy in live type.

Already generated standalone brand-kit images satisfy the separate-generation step only where they are the actual intended assets and still match the selected mockup's subject and composition. Reuse their real generation records; do not claim to have generated them again. Any new, changed or missing image introduced by a mockup requires a fresh standalone generation before implementing that image slot. Repeated uses of the same approved asset do not require duplicate files or repeated generation.

Record an asset map from page/section and mockup region to the separate generated file, actual prompt, reference attachments, raw output, dimensions, palette, correction decision and responsive crop. Inspect that the subjects, orientation, scale, visual treatment and content agree with the mockup. Replace material mismatches before accepting the page. Keep exact product identities and supplied assets when required. Color correction cannot repair the wrong subject or composition.

## Inspect, select, implement and compare

Inspect each returned image. Check identity, composition, real content, image roles, hierarchy, section transitions, usable space and the differences promised by the variation brief. Record and repair material failures. Tiny or invented raster text is corrected with exact live HTML; it is not evidence of font loading or contrast compliance.

Only then implement that page. Record the selected mockup for each route and section, the layout decisions carried into code, and justified adjustments for responsiveness, real data and accessibility. Shared CSS tokens and components are useful; forcing every page into the same hero, three cards and FAQ is not. Compare desktop and narrow screenshots with the selected reference, inspect the full scroll, test every navigation destination and perform the interface checks. If implementation drifts into a materially different layout, revise the mockup first instead of calling a post-code screenshot the original design.

Keep an auditable order: captured kit → exact generation call with attachments → untouched mockup → visual review and selection → separate generation and inspection of required embedded images → page implementation → browser comparison. Previously generated kit assets retain their earlier real timestamps. Preserve earlier outputs as history with their actual labels. Publish generated alternatives, selected directions and implementation screenshots separately when making a guidance site.

## A reusable request

> Use Image Gen Soul with the agreed site purpose, tone and references. First finish and inspect the HTML brand kit with the generated logo, imported fonts, combined imagery and palette. Inventory every navigation link and page. Attach that kit to image generation and produce structurally distinct style alternatives before coding. Explain their differences and select according to my stated preferences. Use the kit and chosen direction to generate a separate mockup for every designed page, including readable lower-page continuations for navigation anchors and important conversion states. Inventory the images pictured inside each selected mockup and generate them as separate, inspected assets with their own prompts before implementation; reuse already generated kit assets only when they actually match. Then build the selected pages in semantic HTML and CSS, carrying over their different compositions and substantive content. Show the actual prompts, references, alternatives and page coverage; verify all links, full-page layouts and accessible interactions.
