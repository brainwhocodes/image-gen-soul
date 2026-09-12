# Make interfaces & components

Before generating a UI mockup, use the [brand-first workflow](brand-first.md). Reuse the established answers about the site, audience, main task and tone; ask about missing decisions and present reference sites or images before generation.

Create a styled HTML board combining the generated logo, live wordmark, imported font specimens, coordinated imagery and labeled palette. Capture it after the fonts and images load, inspect the result and attach that screenshot to the mockup call. Loose files and an unstyled document do not replace the combined reference.

Write the marketing brief and product UI brief separately. The marketing and product guide (see the companion guidance site) explains their different goals, prompts and verification. The product mockup must address actual task states, not just an attractive landing page.

Use generated interface imagery to investigate visual direction. Build the actual controls with semantic HTML, CSS and a small amount of JavaScript when behavior requires it.

Generate the content images shown in the selected mockup as separate standalone assets before implementing them. Maintain a page/region-to-file asset map. Attach the mockup for composition and the kit or original for treatment, and explicitly exclude surrounding UI from each individual image prompt. Do not crop the mockup, use screenshots as artwork, or substitute generic placeholders. Already generated kit assets may be reused where they are the actual matching images; any new or changed picture requires its own generation and inspection.

Follow the interface rules (see the companion guidance site) throughout the implementation. The concept below predates these rules and is retained as historical generation evidence; do not copy its small lettering or drawn progress controls into the live interface.

## Prompt the product after the brand kit

> Use Image Gen Soul and attach the inspected brand-kit screenshot. Carry its generated logo, selected fonts, palette and content imagery into a product interface for the agreed primary task. Show the initial state and the key result or validation state. Keep the marketing promise in a separate marketing-page prompt. Use readable live-type intentions, labeled click controls, no sliders or emoji icons, and no eyebrow labels. Record the actual kit attachment and inspect the returned concept before implementation.

The twelve complete examples (see the companion guidance site) each include a working product, a separate marketing page and an exact-prompt process walkthrough.

## Historical concept

> Use image-gen-soul. Use the attached cosmic reference for dark navy, icy blue edges and a restrained ember accent. Design a square concept sheet for an ambient listening interface named ORBITAL. Include one main listening area and a small row of component states. Keep title, progress, play and volume controls distinct. Use calm spacing and flat surfaces. Avoid ornamental dashboard panels. Label this as a static UI concept.



The generated concept is an image. Its controls cannot play audio. The Orbital example (see the companion guidance site) contains a separately implemented interactive sound demo and real controls.

## Carry the mockup through the whole page

Before coding, follow the page-by-page mockup guide (see the companion guidance site). Map every navigation destination, generate actual brand-conditioned style variations, inspect and select a direction, then generate each page and significant continuation using the kit and selected mockup. A single landing-page image cannot stand in for every destination. Never generate evidence retroactively from an already-built page or merely recolor the same template across brands.

Inspect the mockup’s supporting sections as well as its hero. Plan a full vertical sequence with concrete content, varied image scale and layouts suited to the task. Grids, portrait galleries, comparison tables, editorial spreads, timelines and click-controlled carousels are options, not a checklist to apply everywhere. Follow the marketing and product guide for content depth, carousel accessibility and item-specific conversion paths. A page with only a hero and repeated short features is incomplete.

## Translate visual decisions into code

The image can suggest contrast, spacing rhythm, edge shape and emphasis. The code must add the things an image cannot prove: keyboard focus, labels, state changes, error messages, readable text and responsive layout.

```html
<button type="button" class="play-button" aria-pressed="false">
  Play ambient tone
</button>
<div role="group" aria-label="Volume">
  <button type="button" aria-label="Lower volume">Quieter</button>
  <output aria-live="polite">25%</output>
  <button type="button" aria-label="Raise volume">Louder</button>
  <button type="button" aria-pressed="false">Mute</button>
</div>
```

```css
.play-button {
  color: var(--color-background);
  background: var(--color-accent);
  border: 1px solid currentColor;
  padding: .85rem 1.2rem;
  font: inherit;
  font-size: 1rem;
  min-height: 44px;
  cursor: pointer;
}
.play-button:focus-visible {
  outline: 3px solid var(--color-text);
  outline-offset: 4px;
}
```

## Ask for all the states

> Implement the chosen listening concept in plain HTML and CSS with vanilla JavaScript. Add stopped and playing states, keyboard activation, volume buttons instead of a slider and an explicit message if audio is unavailable. Start audio only after the visitor presses Play. Keep the text and buttons live. Use CSS custom properties, not a framework-specific theme object.

## A small component contract

For each component, record its purpose, states, data, keyboard behavior and narrow-screen behavior. A button needs a meaningful action; a form needs validation and a real or explicitly local outcome. A screenshot does not establish these behaviors.

In these examples, the retreat planner and studio brief generator work entirely in the browser. They do not send enquiries or pretend to make bookings. The sound demo synthesizes a quiet tone locally; it is not a recorded commercial soundtrack.
