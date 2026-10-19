# Interface craft and accessibility

Use the design judgment and default preferences in [Image Gen Soul](../SKILL.md).
This guide owns shared usability and rendering requirements, not a house style.
Choose treatments for the current product and verify them in the actual interface.

### Labels and icons

Do not use emoji as interface icons or decoration. Give labels and icons a useful
role in comprehension, navigation or feedback.
Choose their treatment to fit the product; decorative marks should not compete
with the content. Give icon-only controls accessible names and hide purely
decorative icons from assistive technology. Preserve useful form labels, captions
and status messages.

### Readable text and AA contrast

- Choose readable type sizes for the font, content and viewing conditions. A 16px body size is a useful starting point, not a universal type scale. Use relative units and inspect captions, metadata, placeholders and controls at their actual display size; do not shrink text to rescue a layout.
- Meet WCAG AA text contrast against the actual background: at least 4.5:1 for normal text and 3:1 for qualifying large text (24 CSS px regular or about 18.67 CSS px bold), subject to the standard's exceptions. Check muted text, placeholders and interaction states as well as headings.
- Essential control boundaries, state indicators and focus indicators need at least 3:1 contrast against adjacent colors. Decorative separators and sampled color swatches have different roles; never use a swatch's color alone to convey its value or selected state.
- Put readable text on a solid surface when artwork would make contrast uncertain. Do not claim that a dark-looking image guarantees contrast. Keep words and controls live, outside generated artwork.
- Preserve text resizing to 200% and reflow at 320 CSS pixels without loss of content or functionality. Do not shrink an interactive page into a tiny preview; use a clearly labeled artwork preview that links to the full live example.

### Consistent interactive behavior

- Choose controls for the task, including native range inputs when continuous adjustment helps. Provide keyboard operation and a single-pointer alternative to required dragging, such as track clicks, step buttons or numeric entry. Keep current values and selected states clear.
- Use cursors that match the action: text cursors for editing, pointer cues for clickable actions, and no misleading cues on static content. Preserve familiar native behavior.
- Make targets comfortably usable; 44 by 44 CSS pixels is a useful touch target. Meet WCAG 2.2 AA's 24 by 24 minimum or its spacing and other applicable exceptions, and keep adjacent actions separated.
- Use native semantics, visible focus, associated labels and accurate pressed/expanded states. Do not remove keyboard activation to implement a mouse interaction. Make selected states identifiable beyond color alone.
- Avoid disabling controls silently at a bound. Keep the current value clear, clamp it safely and announce relevant changes. Do not autoplay sound.

### Alignment with real content

- When parallel cards are intended to share an action line, preserve it even when
  titles, descriptions or metadata have different lengths. Stretch the cards and let the
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

### Navigation menu alignment

- Use the selected header composition and the page's content gutters. Align the
  logo, navigation row and utility actions on intentional tracks. If the logo is
  meant to be centered, keep it centered when the side groups have unequal widths;
  do not rely on equal-looking copy, spaces or manual pixel offsets.
- Give peer links, disclosure triggers, search and account/cart actions consistent
  control heights, line-height and padding. Align their box edges and label centers.
  Keep logo artwork proportional; it need not share a button's dimensions. Reserve
  space for carets, badges and active indicators so state changes do not shift labels.
- Anchor a dropdown to its owning trigger or a declared header/content boundary.
  Align its opening edge consistently and keep it within the viewport gutters.
  Prevent clipping by ancestor overflow and stacking contexts; verify the panel
  appears above page content. Keep the pointer path from trigger to panel usable.
- In multi-column menus, align equivalent headings, first links and action rows.
  Use shared tracks and the real-content rules above for unequal descriptions.
  Align carets or badges in their own column beside wrapped labels. Let links grow
  vertically; do not clip text, overlap targets or shrink type to retain one row.
- Collapse navigation when its actual labels and utilities stop fitting. In the
  narrow layout, align the menu trigger with the header controls and give expanded
  links consistent insets and full usable rows. Constrain tall panels to the available
  viewport height, allow vertical scrolling and keep dismissal reachable.
- Check resting, focused, active and expanded states after fonts load, with long
  labels, changing counts and different column lengths. Measure actual peer edges;
  inspect just above and below the collapse width, 320px, 200% text and short viewports.
  Include open-menu resizing and sticky-header anchor/focus visibility.

Use [Navigation menus](ui-components.md#navigation-menus) for semantics, dismissal
and interaction checks. Equivalent elements need intentional relationships;
distinct roles need not have identical dimensions.

### Motion and media

Use motion when it improves understanding, feedback, orientation or the intended
expression. Design its timing and transitions with the same care as the layout.
Inspect it running, including interruption and repeated interaction; a still
screenshot cannot verify motion. Honor reduced-motion preferences, keep content
and actions available without nonessential animation, and preserve focus stability.
Provide pause controls for ongoing motion when needed and avoid flashing effects.

Choose native or custom video controls according to the product. A custom player
needs accessible playback, seeking, volume and relevant caption controls, plus
clear loading, ended and error states. Supply captions, transcripts and other
media alternatives appropriate to the content; test the chosen player's actual
behavior using the shared interaction requirements above.

Use carousels when sequential viewing serves the material. Provide clear position
feedback and usable navigation without requiring dragging. Direct selection or a
view of all items can help comparison. Keep essential decision content reachable;
if auto-advance is justified, provide pause and respect interaction and motion preferences.

### Verify before delivery

Render and inspect meaningful visual changes before presenting them. Review affected
pages and states after fonts, images and data load, including a narrow viewport and
enlarged text. Measure contrast, targets and overflow where appearance alone is
insufficient. Use [UI implementation](ui-components.md#verify-complete-journeys)
for behavior checks and [Mockup fidelity](mockup-fidelity.md) for visual comparison.
Fix observed failures and refresh affected previews and downloads. Record what was
actually checked and any remaining limitation.

These checks address the stated rules; they are not a claim of complete WCAG conformance. Standards: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), [target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), and [dragging movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html).

For motion accessibility, see [Animation from interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html).
