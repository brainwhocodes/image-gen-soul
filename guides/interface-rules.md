# Interface rules


Apply these rules to websites, landing pages, UI mockups and components made with Image Gen Soul. Keep them in the production brief and check the rendered result. They govern the interface; historical source images and actual generation records remain evidence of their original jobs.

### No emoji icons

Do not use emoji or Unicode pictographs as interface icons, logos, decorative bullets or button adornments. Prefer clear text labels. If an icon communicates something useful, draw it with CSS or use an intentional SVG with an accessible name or `aria-hidden="true"` when decorative. Do not add a decorative icon to every link.

### No eyebrows

Do not place small introductory labels, uppercase kickers or redundant category lines above headings. Start each section with its heading. Put necessary context in the paragraph below. Keep useful form labels, captions and status messages in their actual roles; do not disguise an eyebrow by changing its class name.

### Readable text and AA contrast

- Use a 16px body-text default and a 14px minimum for all rendered interface text, including captions, metadata, code, placeholders and responsive layouts. Use relative units so visitor font preferences still work. This is the project's readability floor, not a minimum font size specified by WCAG.
- Require at least 4.5:1 contrast for all interface text against its actual background, including muted text, placeholder text, hover and selected states. This stricter common floor also covers large headings. WCAG AA permits 3:1 for qualifying large text (24 CSS px regular or about 18.67 CSS px bold).
- Essential control boundaries, state indicators and focus indicators need at least 3:1 contrast against adjacent colors. Decorative separators and sampled color swatches have different roles; never use a swatch's color alone to convey its value or selected state.
- Put readable text on a solid surface when artwork would make contrast uncertain. Do not claim that a dark-looking image guarantees contrast. Keep words and controls live, outside generated artwork.
- Preserve text resizing to 200% and reflow at 320 CSS pixels without loss of content or functionality. Do not shrink an interactive page into a tiny preview; use a clearly labeled artwork preview that links to the full live example.

### No sliders or dragging requirements

Do not implement range sliders, draggable comparison dividers, drag-only carousels or drag-only controls. Use labeled native buttons, radio choices, selects or number fields with clear actions. For before/after images, provide Raw, Final and Side by side buttons with visible selected states. For volume, provide quieter/louder buttons and a mute toggle with the current numeric level visible. Every action must work by a mouse click and by keyboard.

### Consistent interactive behavior

- All interactive elements must use `cursor: pointer`: links, buttons, inputs, textareas, selects, summaries, clickable cards, and their visible labels. Their descendants must not override it with grab, move, text or default cursors. Do not give static content a pointer cursor.
- Prefer 44 by 44 CSS pixel targets for controls. Never fall below WCAG 2.2 AA's 24 by 24 target requirement unless a documented exception such as an inline text link applies. Keep adjacent actions separated.
- Use native semantics, visible focus, associated labels and accurate pressed/expanded states. Do not remove keyboard activation to implement a mouse interaction. Make selected states identifiable beyond color alone.
- Avoid disabling controls silently at a bound. Keep the current value clear, clamp it safely and announce relevant changes. Do not autoplay sound.

### Alignment with real content

- Parallel cards in the same row must share a bottom action line even when titles,
  descriptions or metadata have different lengths. Stretch the cards and let the
  content region grow; anchor the final link or action group with flexible space.
  Keep a consistent gap above actions. Do not simulate alignment with blank text,
  fixed paragraph heights, truncation or absolute positioning over content.
- Align the top and bottom edges of adjacent inputs, selects and related buttons.
  Share typography, box sizing, border width, control height and vertical padding
  through tokens. Normalize native input/select sizing explicitly. Keep textareas
  taller when their purpose calls for it; an icon button may have its own size role.
- Wrapped labels, help text and validation errors must not offset neighboring
  controls. Give labels, controls, help/errors and action rows explicit layout
  tracks; use grid/subgrid or equivalent structure where it helps. Keep each error
  associated with its field. Allow the row to grow or stack without clipping text.
- Equal size applies to equivalent controls, not every element on the page. Keep
  intentional staggered, masonry and featured compositions from the selected
  mockup; align comparable actions within each actual row or panel. Reflow removes
  the need for shared baselines between components on different rows.
- Verify with the longest actual heading, unequal descriptions, wrapped labels,
  expanded disclosures, empty results and validation messages. Inspect rendered
  bounding boxes after fonts and data load, then visually check alignment at
  desktop, intermediate widths, 320px and 200% text, including the combined narrow
  and enlarged-text case. Record intentional exceptions and fix accidental drift.

### Custom video players

Every video included in a website must use a custom player designed in that site's visual language: its typography, colors, spacing, borders and button states. Do not expose the browser's default video control bar or embed an unstyled third-party player. Only include video when the page calls for it.

Build the player with semantic, labeled controls for play/pause, restart or time skipping, mute and volume; add captions, transcripts and fullscreen where appropriate to the content. Keep the current time, duration and playback status readable. Apply the same 14px text floor, contrast, focus, keyboard, target-size and pointer-cursor rules as the rest of the interface. Use buttons or discrete choices instead of sliders or drag-only seeking. Do not autoplay sound. Handle loading, ended and playback-error states visibly.

### Verify before delivery

Inspect every page, shared component and dynamic state on desktop and a narrow viewport. Check computed font sizes, actual foreground/background contrast, focus, pointer cursors, target sizes and horizontal overflow. Exercise comparison controls, forms, dialogs and any media buttons with mouse and keyboard. Check 200% text sizing. Fix failures before publishing. Refresh affected previews and downloads. Preserve historical image prompts exactly; do not pretend they were generated under new constraints.

These checks address the stated rules; they are not a claim of complete WCAG conformance. Standards: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), [target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), and [dragging movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html).

Click-controlled content carousels are allowed when the material benefits from a sequence. They are not range sliders. Provide Previous/Next, direct selection, position feedback and Show all; never require dragging or auto-advance.

Continue with [UI implementation](ui-components.md) for component contracts and complete journey checks.
