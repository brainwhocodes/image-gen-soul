# Implement the selected interface

Start with an inspected mockup and its [page/asset inventory](../templates/page-inventory.json).
If those are missing, return to [Brand first](brand-first.md) and [Page mockups](page-mockups.md)
before writing a new layout. For an existing component use [REDESIGN](../skills/redesign/SKILL.md).
Apply [Interface rules](interface-rules.md) throughout implementation and verification.

## Translate the full composition

Use live text, semantic HTML and portable CSS custom properties. Follow the user's
framework choice; use minimal JavaScript for behavior. Map the selected mockup's
columns, image scale, density, section sequence and transitions into the full page.
Use actual drafted content from the [marketing/product briefs](market-product.md),
not repeated short features or empty padding. Preserve logical DOM reading order.

Each image slot must resolve to its inspected standalone generated asset or a
matching existing asset with true provenance. A UI screenshot cannot supply live
controls or be sliced into production artwork. Compare the implemented page to its
selected generated reference and record necessary responsive or accessibility changes.

## Align repeated components and form rows

Apply the [alignment rules](interface-rules.md#alignment-with-real-content) before
polishing individual controls. Inventory peer cards and field groups, distinguish
intentional composition offsets from accidental drift, and check their actual
action/control edges. Use flexible content regions for bottom-aligned card actions
and shared sizing tokens for equivalent inputs, dropdowns and buttons. Preserve
these relationships when labels wrap or errors appear; stack the group when needed.
Do not pad copy or constrain text to make a short-content screenshot line up.

## Define the component contract

Record purpose, trigger, label, data source, destination or endpoint, states,
transitions, keyboard/focus behavior, responsive placement and actual outcome.
Inspect expanded and failure states, not just the resting view. Preserve entered
values and useful existing behavior unless the brief changes them.


Custom controls are welcome. Derive their composition, typography, imagery, shape and feedback from the brand kit and the task. Explore an editorial search field with categorized suggestions, a product finder with removable filter chips, an illustrated navigation panel, a compact command-style search dialog or a form with a live summary when appropriate. Choose the treatment for this product; these examples are options, not a repeated template. A distinctive search bar can be a major design feature.

Use semantic HTML as the foundation and style or compose it freely. Keep familiar text editing, selection, navigation and submission behavior. Use actual links, buttons, inputs, labels and dialogs; add ARIA only for semantics or states the native elements do not provide. A clickable visual shell must contain working controls. Maintain visible labels, focus, pointer cursors, contrast and usable targets in every custom treatment.

- **Navigation:** design desktop, narrow-screen, active destination and expanded states. Preserve real destinations and expose the current page. Use buttons to expand groups and links to navigate; synchronize expanded state and keep collapsed content out of the focus order. Support touch/click and keyboard without requiring hover. Keep sticky navigation from obscuring content or focus. Ordinary site links do not need application-menu roles. Follow the [WAI disclosure navigation example](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/) for disclosure behavior; a modal overlay also follows the dialog rules below.
- **Modals and dialogs:** design the trigger, opening, content, close/cancel and result states. Give the dialog an accessible name, sensible initial focus and a visible close control. Use native modal dialog behavior where suitable; contain keyboard focus, make the background inert, allow Escape dismissal and restore focus to the opener or a logical next target. Keep long content scrollable and actions reachable on small screens. Define how cancellation treats unsaved input. See the [WAI modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).
- **Search:** design the actual query and results journey: idle, focused, typed query, suggestions when useful, loading for asynchronous data, results, no matches, failure/retry, selection and clear/reset. Provide a labeled input, an explicit mouse-usable submit action and Enter support. Make suggestions and filter chips operable by mouse and keyboard, report results changes without moving focus unexpectedly, and preserve useful query/filter state when navigating back. Define the real search corpus and matching behavior. Use the [WAI combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) when the field has an interactive suggestion popup; preserve normal input editing and implement the pattern's arrow, Enter and Escape behavior. A simple search field with a results page does not need combobox roles.
- **Forms:** design labels, instructions, grouped fields, required/optional treatment, filled values, validation, submitting, failure/retry and success. Use appropriate input types and autocomplete where applicable. Associate errors with fields, explain how to fix them, retain entered values and provide an error summary when useful. Communicate progress and outcomes accessibly, prevent duplicate submissions and handle server errors as well as client validation. See [WAI form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/). Show success only after the stated operation succeeds; label browser-only demonstrations and describe their actual local result.

Apply only states and features relevant to the component. Specify the source of data and any backend dependency before implementation; visual invention does not create search indexing, authentication, bookings or message delivery. Preserve working integrations. If an integration is unavailable, describe the limitation and implement an explicitly local demonstration only when that fits the brief.

## Verify complete journeys

Test the actual implementation with mouse and keyboard, at desktop and 320px,
and with 200% text resizing. Inspect every affected page and dynamic state for the
font, contrast, cursor, target, focus and reflow rules. Screenshots alone do not
prove interaction behavior or complete accessibility conformance.

- Follow every navigation destination and section anchor. Open and close groups,
  check active/expanded state, and confirm the narrow menu remains usable.
- Open dialogs, traverse focus, close with the visible control and Escape, and
  confirm focus restoration. Test long content and a narrow viewport.
- Search for a match and no match; select a result, clear/reset, change filters
  and return without losing useful state. Test suggestion keyboard behavior if present.
- Submit invalid and valid forms. Inspect pending, failure/retry and completion
  states where relevant, retained values, field errors and result announcements.
- Exercise selected, empty and boundary states for the product task. Verify that
  a named item action operates on that item and that a local demo states its limits.

Measure peer action baselines and control sizes with unequal content and field
errors visible. Repeat at an intermediate width and at 320px with 200% text.
Compare full-scroll screenshots with the chosen concepts and fix material drift.
Keep generated references, before captures and implemented screenshots distinct.
Record observed checks, inaccessible integrations or missing assistive-technology
coverage; refresh affected downloads and previews. Report only outcomes actually verified.
