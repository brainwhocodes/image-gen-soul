# Brand first, mockups second

A website needs a brand decision before it needs a picture of an interface. Keep the sequence visible: site brief and reference review, typography and logo, brand imagery, rendered HTML brand kit, mockups, then working marketing and product pages.

## Establish the direction

Before the first UI mockup, establish what the site does, who it serves, the primary task or conversion, tone and constraints. Reuse supplied answers and project context. Make reasonable design decisions from a workable brief; ask only about missing information that materially changes the result and cannot be inferred. State consequential assumptions while continuing independent work.

Use supplied references or research a small relevant set when useful. Show the selected links or images and explain their roles: layout, interaction, visual treatment, typography or content. Distinguish observed reference features from proposed design choices. Never claim to have inspected a page you could not access.

Wait when the user explicitly wants to choose a direction or when a consequential missing fact blocks the design. Otherwise use judgment within the brief without adding an approval gate. Keep publishing and other external actions within existing authorization.

## Build the brand kit

If the brief has no supplied visual image, state that the initial original assets
will be generated from the established direction. Reference sites can supply interaction
or content guidance without supplying a color target. Inspect the initial outputs
and use them as anchors for subsequent variations; do not invent a missing original.

1. Write the audience, product promise, voice, primary task and preserve/change contract. Name the treatment anchor when one exists. Separate the [marketing goal from the product task](market-product.md).
2. Follow [Fonts and tokens](fonts-tokens.md) to research typefaces that fit those qualities, preferably on Google Fonts. Compare real candidates with the same headline, paragraph, numerals and controls. Verify the official family page, actual styles and working import. Avoid choosing a familiar default merely because it is common in AI-generated sites. No font is inherently bad; the choice must have a reason connected to this product.
3. Generate an original logo concept using image generation when the brief requests a generated logo. Attach the selected brand imagery or original treatment reference. Describe a specific symbol idea connected to the product; do not substitute a stock icon, emoji or a quick generic line glyph. Inspect the actual returned logo for coherence and small-size clarity. Keep its raw output and exact prompt. Pair the generated symbol with a live-type wordmark using the chosen font. If editable vector artwork is required, produce that as a separate, faithful production adaptation and identify it honestly; a raster concept is not an SVG. Use an exact supplied mark when required.
4. Generate coordinated product, placeholder or editorial images from the established direction and any selected treatment reference. Change the objects, people or scene as the brief requires. Record exact prompts, source roles, raw files, dimensions, palettes and finishing decisions. Inspect the images before using them in the kit.
5. Compose a designed brand presentation in HTML/CSS with real font imports. Combine the supplied or generated logo, live wordmark, typography specimens, coordinated imagery and labeled palette in one board. Choose their scale, relationships and treatment to express this product's identity. Show enough context to judge them together; loose files or a font list are not a composed kit. Keep implementation notes outside the captured board and distinguish semantic colors from measured artwork palettes. Apply [Interface rules](interface-rules.md) to its live content.
6. Render the complete board with its fonts and assets loaded, inspect the screenshot and fix visible failures. Confirm that the intended identity, relationships and details survive the actual rendering. The HTML remains the editable source of truth; its screenshot is the visual reference for page generation.

Use image generation for the board only when HTML rendering is unavailable. Label the result as a concept, record the font choices separately, and do not claim that generated lettering proves the fonts were loaded. Deliver an editable kit when the host later supports it.

## Handoff to page design

Save the editable board, inspected screenshot and screenshot hash beside the
logo and imagery. Keep exact prompts, reference roles, raw/final files,
font source links, semantic tokens and measured palettes with the current job.
Record any intentionally skipped correction. Rebuild and recapture when the
identity or board composition changes.

For a case-study page explaining the kit, follow [Content hierarchy](content-hierarchy.md):
brief, one complete board, useful design decisions, then the working example.
The editable board and its explanatory page have different jobs.

Attach the actual inspected screenshot through the image tool's supported reference
mechanism; naming a file in prose is insufficient. Continue with [Page mockups](page-mockups.md)
for destination coverage, alternatives and separate production images. A brand-kit-only
request ends with the kit; do not generate or build an unrequested website.
