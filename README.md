# Image Gen Soul

A reference-driven skill for image generation, brand art, UI concepts, plain HTML/CSS websites, font selection, theme tokens and measured color correction.

Start with your images. Preserve their visual language while making meaningful variations with different people, objects, items or scene elements. Describe what stays and name what changes. The skill carries that intent through prompting, generation, inspection, correction and implementation. It has no default aesthetic, reference library or fixed palette.

[Twelve working sites](https://soul.brainwhocodes.rocks/worlds/) · [Composed brand kits](https://soul.brainwhocodes.rocks/brands/) · [Companion field guide](https://soul.brainwhocodes.rocks/) · [Interface rules](https://soul.brainwhocodes.rocks/guides/interface-rules/) · [Download the skill](https://soul.brainwhocodes.rocks/downloads/image-gen-soul.zip)

## Install

Clone this repository into a folder named `image-gen-soul`:

```bash
git clone https://github.com/brainwhocodes/image-gen-soul.git
```

Place that entire folder in your assistant's configured skills directory. Keep `SKILL.md`, `guides/`, `scripts/` and `templates/` together. If your assistant accepts project attachments instead, attach the core instructions and the relevant guide files. Repository hosting does not automatically install the skill in an assistant.

The assistant needs image viewing and an image-generation tool to create images. Color measurement and correction require Python 3.10 or newer, Pillow and NumPy. The skill does not supply API keys or a hosted generator. The Python helpers make no network or image-generation calls.

```bash
python -m venv .venv
# Activate .venv using your shell's normal activation command.
python -m pip install -r requirements.txt
python scripts/validate_skill.py
python -m unittest discover -s scripts -p "test_*.py"
```

## Use it

Attach the relevant reference images and ask:

> Use image-gen-soul. Use the attached image for treatment and color. Create a wide hero and one square supporting image for my project. Preserve the material, edge behavior and lighting relationships; change the subject as described in my brief. Keep interface text live. Inspect each generated image, measure its palette and correct color only where the reference comparison supports a change. Keep the raw images, actual prompts, recipes and final exports.

For a website:

> Map every navigation destination before coding. Use the inspected HTML brand kit as an actual image attachment to generate structurally different style variations. Select a direction using my brief, then attach the kit and selected mockup to generate each designed page and the significant lower-page continuations. A homepage concept does not cover the shop, detail, pricing or app screens. Show the actual alternatives and page coverage, then build and compare each page to its selected reference. Never substitute a recolored template or a screenshot of code written before generation.

> Before generating UI mockups, ask me about the site or app, audience, main task and tone. Present reference sites or images for selection. Research suitable Google Fonts, generate an original logo, pair it with a live-type wordmark, generate coordinated product/content images, and compose a deliberately styled HTML board combining that logo, imagery, labeled palette and expressive specimens using real font imports. Render and inspect it, then attach its screenshot as the reference for separate marketing and product UI mockup prompts. Use the reviewed kit to build both working surfaces. Develop the whole vertical page with substantive content and layouts drawn from the mockup: appropriate grids, editorial sequences, comparisons or accessible click-controlled carousels. Give every section a distinct selling purpose. Keep the images, prompts, palettes and correction decisions traceable.

> Use image-gen-soul to build a landing page from these references in semantic HTML, plain CSS and minimal vanilla JavaScript. Start with the preserve/change/avoid contract in templates/site-brief.md. Apply the core interface rules: no emoji icons or eyebrows, 16px body text with a 14px floor, measured text and control contrast, labeled click controls instead of sliders, pointer cursors and keyboard support. Choose verified Google Fonts, define semantic CSS tokens, and generate coordinated artwork for the page. Check desktop, 320px reflow and 200% text resizing. Deliver working source, actual asset prompts, palettes and correction records.

For prompts only, explicitly ask for prompts only. For color correction only, provide an existing image and a color reference and ask for Python correction without image generation. A skill never implies permission to publish or send messages beyond the user's request.

When implementing a selected mockup, generate its content images separately. Ask for an asset map, individual image prompts and standalone files for every new or changed hero, product, person, illustration or background. The mockup guides composition; it must not be cropped into production artwork or used as the page itself. Reuse matching kit images only with their existing standalone generation records.

## What is inside

| File | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Core workflow and mandatory interface rules |
| [guides/prompt-workflow.md](guides/prompt-workflow.md) | Reference roles, close recreation, variation and prompts |
| [guides/production-layouts.md](guides/production-layouts.md) | Web, social, print and layered output |
| [guides/color-workflow.md](guides/color-workflow.md) | Reference-relative grading and QA |
| [guides/brand-kits.md](guides/brand-kits.md) | Brand art, marks and applications |
| [guides/brand-first.md](guides/brand-first.md) | Site/tone questions, reference selection, HTML kit and mockup gate |
| [guides/page-mockups.md](guides/page-mockups.md) | Navigation coverage, generated style alternatives and page-by-page design before code |
| [guides/market-product.md](guides/market-product.md) | Separate marketing and product UI briefs and journeys |
| [guides/ui-components.md](guides/ui-components.md) | Concepts translated into real controls |
| [guides/fonts-tokens.md](guides/fonts-tokens.md) | Font research, palettes and CSS roles |
| [guides/aspect-ratios.md](guides/aspect-ratios.md) | Recompose for each format |
| [guides/content-images.md](guides/content-images.md) | Coordinated content imagery |
| [templates/job.json](templates/job.json) | Per-job provenance scaffold |
| [templates/site-brief.md](templates/site-brief.md) | Website brief and delivery contract |
| [templates/page-inventory.json](templates/page-inventory.json) | Navigation destinations, actual mockups, variations and implementation comparison |
| [scripts/color_pipeline.py](scripts/color_pipeline.py) | Inspect, fit, apply and compare images |
| [scripts/palette_extract.py](scripts/palette_extract.py) | Histogram palette and luminance measurement |

One core skill coordinates the job; load only the focused guides needed for the current deliverable. The companion site's 62 references and generated examples are not bundled or treated as defaults. No fonts, user artwork or cloud credentials are included.

## Measure and correct

Replace these filenames with your actual current-job files. Keep the raw image unchanged and use fresh output paths.

```bash
python scripts/palette_extract.py raw.png --report palette.json
python scripts/color_pipeline.py inspect reference.png raw.png --report measurements.json
python scripts/color_pipeline.py fit raw.png --reference reference.png --recipe grade.json
python scripts/color_pipeline.py apply raw.png final.png --recipe grade.json --report color-qa.json
python scripts/color_pipeline.py compare raw.png final.png comparison.png --reference reference.png
```

`fit` creates a statistical starting point, not an automatic aesthetic judgment. Compare appropriate regions, protect exact brand colors, inspect the result and reduce or skip the grade when it does not help. The pipeline exports tagged 8-bit sRGB; it is not an HDR, RAW or print-certification system. See the color guide for masks and recipe options.

The palette helper uses a 5-bit RGB histogram and six weighted clusters over a sample of up to 256 pixels per side, with alpha-weighted shares and a 32-bin linear-light luminance histogram. It does not recognize subjects, infer original prompts or assign semantic UI roles. Fully transparent images return an empty palette.

## Interface rules

- No emoji icons or introductory eyebrow labels above headings.
- 16px body text; 14px minimum for labels, captions, code and responsive states.
- At least 4.5:1 text contrast and 3:1 essential control and focus contrast against actual surfaces.
- Every video uses a custom player styled to the site, with accessible playback controls and explicit states.
- No sliders or dragging requirements. Use labeled buttons and other native click controls.
- Pointer cursors for all interactive elements; keyboard support, visible focus and explicit states.
- Prefer 44px targets, test 320px reflow and 200% text resizing.

The text-size floor is a project rule, not a WCAG-prescribed minimum. Read the core skill for qualifications and standards links. Automated checks are evidence for specific requirements, not a claim of complete accessibility conformance.

## Develop and verify

Edit the core and focused guides directly in this repository. Run the validation command and synthetic Python tests above before committing. The test suite creates temporary test images; it never uses the companion site's artwork or invokes a generator. GitHub Actions runs the same checks on pushes and pull requests.

Version 1.2 was checked locally with Python 3.12, Pillow 12.3 and NumPy 2.5. CI covers Python 3.10 and 3.12. See [CHANGELOG.md](CHANGELOG.md) for changes.
