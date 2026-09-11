# Make interfaces & components

Use generated interface imagery to investigate visual direction. Build the actual controls with semantic HTML, CSS and a small amount of JavaScript when behavior requires it.

Follow the interface rules (see the companion guidance site) throughout the implementation. The concept below predates these rules and is retained as historical generation evidence; do not copy its small lettering or drawn progress controls into the live interface.

## Prompt a UI concept with constraints

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
