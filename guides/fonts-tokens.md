# Research fonts and define portable tokens

Describe the reference's typographic qualities before naming fonts: width, rhythm,
contrast, weight, numeral shape, language needs and reading scale. A visual guess
is not an extracted font identity. Preserve an exact supplied family when required.

## Verify real candidates

Search current primary sources, preferably [Google Fonts](https://fonts.google.com/).
Compare a small set of appropriate families using the same actual heading, paragraph,
numerals and control labels. Connect the choice to this product's tone and task;
familiarity with an AI-generated template is not a reason to choose a family.
No font is inherently forbidden. Verify available styles, language coverage,
license and official source links rather than inventing a family or weight.

Use the [Google Fonts CSS2 API](https://developers.google.com/fonts/docs/css2)
when hosted imports fit the project. Request only used styles, include `display=swap`
and suitable fallbacks. Put the selected families in CSS custom properties such as
`--font-display` and `--font-body`. Verify actual network/font loading in the rendered
board; generated lettering cannot prove a font match. Do not bundle font binaries
in this skill or redistribute them with its sample deliverables.

## Measure artwork separately from UI colors

The bundled [palette helper](../scripts/palette_extract.py) samples at up to 256 pixels
per side, builds a 5-bit RGB histogram and six deterministic weighted clusters,
reports alpha-weighted pixel shares, and measures 32 linear-light luminance bins.
It does not recognize objects or assign semantic roles. Fully transparent images
have no visible palette. Cluster centers are representative averages, not necessarily
exact source pixels. Record the actual method and settings with each measurement.

```bash
python scripts/palette_extract.py raw.png --report palette.json
```

Run from the installed skill directory with verified current-job paths. Measure
raw and final separately if correction occurred. Different subjects can change
pixel shares; do not force a variation's histogram to reproduce unrelated content.

Choose semantic roles for background, surface, text, muted text, accent, border,
focus and relevant states. Label sampled values separately from curated or adjusted
UI values. A small image highlight may be a useful accent, but image percentages
are not mandatory layout proportions. Check colors against their actual surfaces
using [Interface rules](interface-rules.md).

## Deliver the system

Use plain CSS custom properties for fonts, colors, spacing and other decisions;
do not make the handoff depend on a framework theme object. Keep the live page
and exported tokens consistent. Show labeled semantic swatches and font specimens
inside the [composed brand kit](brand-first.md). Keep histogram data and correction
recipes in its companion details. For actual grading use [Color workflow](color-workflow.md);
measurements alone never justify an invented correction recipe.
