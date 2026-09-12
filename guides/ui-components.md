# Make interfaces & components

The required reference is a saved screenshot of a deliberately styled brand board: generated logo, live wordmark, imported font specimens, combined imagery and labeled palette together. Separate files or an unstyled documentation page do not satisfy the brand-kit step. See the composed-board requirements in the brand-first and brand-kit guides.
Before generating a UI mockup, follow the brand-first workflow (see the companion guidance site): ask the user about the site, audience, main task and tone; present or request reference sites/images; resolve those choices; create and inspect an HTML brand kit with loaded fonts, the generated logo, an editable live-type wordmark and coordinated imagery. Attach a screenshot of that kit to the mockup call. Do not skip these steps or invent answers that the user has not delegated.

Write the marketing brief and product UI brief separately. The marketing and product guide (see the companion guidance site) explains their different goals, prompts and verification. The product mockup must address actual task states, not just an attractive landing page.

Use generated interface imagery to investigate visual direction. Build the actual controls with semantic HTML, CSS and a small amount of JavaScript when behavior requires it.

Follow the interface rules (see the companion guidance site) throughout the implementation. The concept below predates these rules and is retained as historical generation evidence; do not copy its small lettering or drawn progress controls into the live interface.

## Prompt the product after the brand kit

> Use Image Gen Soul and attach the inspected brand-kit screenshot. Carry its generated logo, selected fonts, palette and content imagery into a product interface for the agreed primary task. Show the initial state and the key result or validation state. Keep the marketing promise in a separate marketing-page prompt. Use readable live-type intentions, labeled click controls, no sliders or emoji icons, and no eyebrow labels. Record the actual kit attachment and inspect the returned concept before implementation.

The twelve complete examples (see the companion guidance site) each include a working product, a separate marketing page and an exact-prompt process walkthrough.

## Historical concept

> Use image-gen-soul. Use the attached cosmic reference for dark navy, icy blue edges and a restrained ember accent. Design a square concept sheet for an ambient listening interface named ORBITAL. Include one main listening area and a small row of component states. Keep title, progress, play and volume controls distinct. Use calm spacing and flat surfaces. Avoid ornamental dashboard panels. Label this as a static UI concept.



The generated concept is an image. Its controls cannot play audio. The Orbital example (see the companion guidance site) contains a separately implemented interactive sound demo and real controls.

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
