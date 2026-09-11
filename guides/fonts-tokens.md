# Find the type. Define the tokens.

A reference suggests typographic qualities. It rarely identifies a font with certainty. Describe those qualities, compare real candidates and test them in the actual layout.

## Ask the AI to look, then verify

> Use the selected garden as a mood reference. Search Google Fonts for three serif families with delicate stroke contrast, a gently organic rhythm and an editorial tone. Pair each with a readable sans for body text. Verify available styles and language coverage on the official specimen pages. Show the same headline and paragraph in all three pairs. Explain your preferred pairing without claiming it is the font in the image.

For this project, [Instrument Serif](https://fonts.google.com/specimen/Instrument+Serif) provides the expressive display voice; [DM Sans](https://fonts.google.com/specimen/DM+Sans) carries the guide's labels and body text; [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) gives Orbital and Cobalt a more geometric voice. These are chosen interpretations, not extracted font identities.

## Load only what you use

Use the [Google Fonts CSS2 API](https://developers.google.com/fonts/docs/css2) and request the families and styles you need. The site links to the hosted fonts with `display=swap` and uses system fallbacks if the service is unavailable. The downloadable skill does not distribute font files.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
```

## Measure a palette, then assign roles

The catalogue samples each image at up to 256 pixels per side. It builds a 5-bit-per-channel RGB histogram, chooses six deterministic weighted clusters and measures their pixel shares. The color room also shows a 32-bin histogram of linear-light luminance.

This is an image summary. A large dark region can dominate the histogram while a tiny highlight supplies the most useful accent. Cluster centers are representative averages, not guaranteed exact pixels. Whole-image measurements do not recognize plants, skin, products or text.

> Extract a histogram palette from the approved final artwork. Then propose semantic CSS roles for background, surface, text, muted text, accent and border. Explain which colors are sampled and which are adjusted for interface legibility. Check contrast in actual components. Do not turn image pixel percentages into mandatory layout percentages.

## Keep the tokens portable

Use plain CSS custom properties. Each worked example includes a downloadable `tokens.css` and the same values are used by its live page. The choices are job-local interpretations informed by the measured artwork.

```css
:root {
  --font-display: 'Instrument Serif', Georgia, serif;
  --font-body: 'DM Sans', Arial, sans-serif;
  --space-1: .5rem;
  --space-2: 1rem;
  --space-3: 2rem;
  --space-4: 4rem;
  --radius: 0;
}
```

Get the actual color tokens from Verdant (see the companion guidance site), Orbital (see the companion guidance site) or Cobalt (see the companion guidance site). Raw measurements and curated theme roles are shown separately in the case studies.


## Verify the actual interface

Use a 16px body-text default and never go below 14px in captions, controls, code or responsive states. This is a project rule; WCAG does not specify a universal minimum font size. Check 4.5:1 text contrast and 3:1 essential control and focus contrast on the actual surfaces. Test 200% text sizing. Follow the complete interface rules (see the companion guidance site).
