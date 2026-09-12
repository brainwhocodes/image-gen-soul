# Brand first, mockups second

A website needs a brand decision before it needs a picture of an interface. Keep the sequence visible: site brief and reference review, typography and logo, brand imagery, rendered HTML brand kit, mockups, then working marketing and product pages.

## Ask before generating UI mockups

Before the first UI mockup generation, ask the user concise questions about the site or app: what it does, who it serves, the primary task or conversion, the desired tone, and any references or constraints. Carry forward answers already supplied rather than repeating questions. If the user has delegated product selection, propose concrete product types and ask about unresolved tone or audience choices. State the proposed site purpose and tone for review.

Ask for existing reference sites or images. If none are supplied, research and present a small relevant set of real reference sites, or use the user's supplied image collection when they choose that. Show the reference links or images before generating mockups and explain each role: layout, interaction, visual treatment, typography or content. Distinguish observed reference features from your proposed design choices. Never claim to have inspected a page you could not access.

Wait for answers to the unresolved site/tone questions and the user's reference selection before generating UI mockups, unless the user explicitly delegates those decisions. Brand research, guide writing, and other independent work can continue while answers are pending. Do not turn every later revision into another questionnaire. The questions establish design direction; they are not permission to publish, buy, send messages or run external promotion.

## Build the brand kit

1. Write the audience, product promise, voice, primary task and preserve/change contract. Name the original image used as the treatment anchor. Separate the marketing goal from the product task.
2. Search for typefaces that fit those qualities, preferably on Google Fonts. Compare real candidates with the same headline, paragraph, numerals and controls. Verify the official family page, actual styles and working import. Avoid choosing a familiar default merely because it is common in AI-generated sites. No font is inherently bad; the choice must have a reason connected to this product.
3. Generate an original logo concept using image generation when the brief requests a generated logo. Attach the selected brand imagery or original treatment reference. Describe a specific symbol idea connected to the product; do not substitute a stock icon, emoji or a quick generic line glyph. Inspect the actual returned logo for coherence and small-size clarity. Keep its raw output and exact prompt. Pair the generated symbol with a live-type wordmark using the chosen font. If editable vector artwork is required, produce that as a separate, faithful production adaptation and identify it honestly; a raster concept is not an SVG. Use an exact supplied mark when required.
4. Generate coordinated product, placeholder or editorial images from the selected original. Change the objects, people or scene as the brief requires. Record exact prompts, source roles, raw files, dimensions, palettes and finishing decisions. Inspect the images before using them in the kit.
5. Compose a designed brand presentation in HTML/CSS with real font imports. Combine the generated logo, live wordmark, expressive typography specimens, a coordinated image composition, and labeled palette swatches in the same board. The board itself must express this brand: choose its composition, surfaces, image scale, framing, spacing and graphic motifs from the reference and product. Give imagery substantial visual space and use type as part of the composition. A plain documentation page, a list of fonts, isolated image cards, or a grid with only its colors changed does not satisfy this step. Keep prose explanations, CSS textareas, tool controls and implementation notes outside the captured board. Show semantic color roles separately from measured artwork colors in the companion details. Keep every label at least 14px and all live text readable; use an additional detail board if necessary instead of shrinking everything.
6. Render the complete styled board, verify that its CSS, requested fonts, generated logo and all images loaded, and inspect a screenshot before accepting it. The saved screenshot must visibly contain the combined logo, font specimens, imagery and palette; linking separate files is not a combined brand kit. Fix fallback fonts, empty image areas, clipped names, accidental crops and document-like styling before capture. Save the actual browser screenshot as a deliverable, expose its preview and download, and record its path and hash. The HTML kit remains the editable source of truth. Rebuild and recapture the board whenever its logo, imagery, fonts or layout change.

Use image generation for the board only when HTML rendering is unavailable. Label the result as a concept, record the font choices separately, and do not claim that generated lettering proves the fonts were loaded. Deliver an editable kit when the host later supports it.

## Use the kit as an actual image reference

Attach the inspected brand-kit screenshot to the mockup generation call. A filename in prose alone is not image conditioning. Specify the role of the kit and any original reference: the kit controls identity, type direction, color roles and imagery; the original controls a named visual treatment when still needed. Use the same reviewed kit for marketing and product concepts, but write separate prompts for their different jobs.

Record the kit screenshot hash in each mockup job. Generate no UI mockup before that kit exists. Inspect the returned mockup and record mismatches honestly. Implement exact fonts, logo, words and color tokens in HTML/CSS rather than reproducing raster mistakes.

## Generate every navigation page before coding

After capturing the kit, follow `guides/page-mockups.md`. Inventory every navigation link and its destination. Each distinct designed page needs its own generated mockup conditioned on the actual kit; hash links need coverage of the destination section in that page's mockup or a separate continuation. A homepage concept does not cover a shop, item detail, pricing, about, dashboard or checkout page. Shared components are reusable; a repeated page composition is not a substitute for page-specific design.

Explore composition variations when testing different styles. Keep the logo, approved fonts, semantic palette and image treatment fixed while changing hierarchy, navigation placement, grid structure, image scale, density, section order and the way the offer is presented. Generate and inspect the alternatives before selecting one. A palette swap, a renamed template or a screenshot of already-written HTML is not an image-generated design variation.

Choose a direction using existing user preferences or delegated judgment, then use that selected mockup together with the brand-kit screenshot to generate the other pages and substantial lower-page continuations. Do not implement a new page or materially different section before its generated reference has been inspected. Record the real prompt, attachments, output, selection reasons and page coverage. Compare the implemented page with its selected mockup and correct drift before delivery.

Generate the images inside each selected mockup separately before implementation. Inventory every hero, product, person, illustration, thumbnail and background; give each its own image-generation prompt and output file, using the mockup for composition and the kit/original for treatment. Never crop artwork out of a UI mockup or use the mockup itself as the working page. Reuse an already separately generated kit asset only when it is the intended matching image; new or changed images require fresh standalone generation. Record and inspect the asset map, exact prompts, raw outputs, dimensions and responsive crops. See guides/page-mockups.md for the complete asset workflow.

## Keep the stages honest

The order should be provable from files and records: reference choices, generated brand assets, rendered kit, mockup prompt with attached kit, generated mockup, implementation and verification. Reusable skill instructions contain the procedure, not this project's brand names, fixed palettes or artwork. Case studies belong to the companion site.

Use the marketing and product guide (see the companion guidance site) to write the two briefs and inspect the 12 composed brand kits (see the companion guidance site) for examples.
