# Image Gen Soul

A reference-driven skill for image generation, brand art, UI concepts, plain HTML/CSS websites, font selection, theme tokens and measured color correction.

Start with your images. Describe what to preserve and what may change. The skill carries that intent through prompting, generation, inspection, correction and implementation. It has no default aesthetic, reference library or fixed palette.

[Companion field guide](https://soul.brainwhocodes.rocks/) · [Interface rules](https://soul.brainwhocodes.rocks/guides/interface-rules/) · [Download the skill](https://soul.brainwhocodes.rocks/downloads/image-gen-soul.zip)

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

> Use image-gen-soul to build a landing page from these references in semantic HTML, plain CSS and minimal vanilla JavaScript. Start with the preserve/change/avoid contract in templates/site-brief.md. Apply the core interface rules: no emoji icons or eyebrows, 16px body text with a 14px floor, measured text and control contrast, labeled click controls instead of sliders, pointer cursors and keyboard support. Choose verified Google Fonts, define semantic CSS tokens, and generate coordinated artwork for the page. Check desktop, 320px reflow and 200% text resizing. Deliver working source, actual asset prompts, palettes and correction records.

For prompts only, explicitly ask for prompts only. For color correction only, provide an existing image and a color reference and ask for Python correction without image generation. A skill never implies permission to publish or send messages beyond the user's request.

## What is inside

| File | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Core workflow and mandatory interface rules |
| [guides/prompt-workflow.md](guides/prompt-workflow.md) | Reference roles, close recreation, variation and prompts |
| [guides/production-layouts.md](guides/production-layouts.md) | Web, social, print and layered output |
| [guides/color-workflow.md](guides/color-workflow.md) | Reference-relative grading and QA |
| [guides/brand-kits.md](guides/brand-kits.md) | Brand art, marks and applications |
| [guides/ui-components.md](guides/ui-components.md) | Concepts translated into real controls |
| [guides/fonts-tokens.md](guides/fonts-tokens.md) | Font research, palettes and CSS roles |
| [guides/aspect-ratios.md](guides/aspect-ratios.md) | Recompose for each format |
| [guides/content-images.md](guides/content-images.md) | Coordinated content imagery |
| [templates/job.json](templates/job.json) | Per-job provenance scaffold |
| [templates/site-brief.md](templates/site-brief.md) | Website brief and delivery contract |
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

## Interface rules in version 1.2

- No emoji icons or introductory eyebrow labels above headings.
- 16px body text; 14px minimum for labels, captions, code and responsive states.
- At least 4.5:1 text contrast and 3:1 essential control and focus contrast against actual surfaces.
- No sliders or dragging requirements. Use labeled buttons and other native click controls.
- Pointer cursors for all interactive elements; keyboard support, visible focus and explicit states.
- Prefer 44px targets, test 320px reflow and 200% text resizing.

The text-size floor is a project rule, not a WCAG-prescribed minimum. Read the core skill for qualifications and standards links. Automated checks are evidence for specific requirements, not a claim of complete accessibility conformance.

## Develop and verify

Edit the core and focused guides directly in this repository. Run the validation command and synthetic Python tests above before committing. The test suite creates temporary test images; it never uses the companion site's artwork or invokes a generator. GitHub Actions runs the same checks on pushes and pull requests.

Version 1.2 was checked locally with Python 3.12, Pillow 12.3 and NumPy 2.5. CI covers Python 3.10 and 3.12. See [CHANGELOG.md](CHANGELOG.md) for changes.
