# Image Gen Soul

A reference-driven skill for image variations, composed brand kits, UI mockups,
working HTML/CSS sites, copy, fonts, CSS tokens and measured color correction.
It preserves a reference's visual language while changing the people, objects or
scene as requested. It ships no default style, palette, artwork or website code.

[Guidance site](https://soul.brainwhocodes.rocks/) ·
[Working examples](https://soul.brainwhocodes.rocks/worlds/) ·
[Brand kits](https://soul.brainwhocodes.rocks/brands/)

## Install

Use the [Vercel skills CLI](https://github.com/vercel-labs/skills) in your project:

```bash
npx skills add brainwhocodes/image-gen-soul --skill image-gen-soul
```

For a copied Codex project installation:

```bash
npx skills add brainwhocodes/image-gen-soul --skill image-gen-soul --agent codex --copy
```

Add `--global` only for a user-wide install. Preview with `--list`. For manual
installation, clone this repository into your assistant's configured skills
directory. Keep the entire package together: [SKILL.md](SKILL.md) routes to its
guides, helpers and bundled [REDESIGN](skills/redesign/SKILL.md) sub-skill.

The host must provide image viewing/generation and browser rendering for the full
website workflow. The package supplies no generator, API keys or hosted service.
Color helpers need Python 3.10+, Pillow and NumPy; optional writing checks need Node.js.

## Ask for the outcome

Attach your images and invoke `image-gen-soul`. The main skill selects the procedure;
you do not need to paste every workflow step into your request.

> Use image-gen-soul to make a variation of this image for a wide website hero.
> Preserve its material and lighting, replace the objects with the items in my
> brief, and reserve space for live text. Return the image and actual prompt.

> Use image-gen-soul to build a running-shoe store in HTML and CSS. Ask about any
> unresolved site and tone decisions, show references, make the composed brand kit,
> generate page mockups, then implement and test the storefront.

> Use image-gen-soul's REDESIGN on this URL, including navigation and search.
> Preserve working behavior and identity, generate a structural variation before
> code, then build and verify the selected direction.

> Use image-gen-soul to fix this site's navigation and alignment. Preserve the
> composition; align header controls, dropdown edges and actions with unequal
> content. Check expanded menus, keyboard dismissal, long labels and mobile reflow.

> Use image-gen-soul to correct this existing image against the attached color
> reference without image generation. Keep the raw file and show the measured
> recipe and before/after comparison. Skip a correction that does not help.

For text only, say “prompts only.” For a copy-only rewrite, ask for the writing
route; it preserves facts and behavior without forcing new images.

## How the package works

[SKILL.md](SKILL.md) is the entry point and task router. Focused guides own each
procedure: references, production formats, brand kits, page mockups, implementation,
interface rules, hierarchy, marketing/product briefs, writing, fonts/tokens and color.
The REDESIGN sub-skill adds an existing-site audit and reuses those same guides.

For new interfaces, the order is brief/references → generated logo and imagery →
styled HTML brand-kit screenshot → generated page/state mockups → separate content
assets → working implementation and observed checks. Text, controls and exact brand
elements stay live. The [interface rules](guides/interface-rules.md) cover readable
text, contrast, pointer cursors, keyboard operation and click controls without sliders.
The [navigation contract](guides/ui-components.md#navigation-menus) covers menu
behavior and links to the shared rules for header, dropdown and control alignment.
Brand kits and page mockups are distinct from functioning products.

Job templates are optional record forms. Generated projects and private reference
images belong outside the skill repository. This repo contains only the reusable
skill package, its documentation, helper code, tests and source licenses.

## Validate and use the helpers

Run from the installed skill directory:

```bash
python -m pip install -r requirements.txt
python scripts/validate_skill.py
python -m unittest discover -s scripts -p "test_*.py"
node scripts/writing/cliche-lint.mjs --self-test
```

The validator checks package discovery, routing, portable links and templates.
GitHub Actions also installs a copied package into an isolated project. Image tests
use synthetic temporary files and do not invoke a generator or network service.

For palette measurements and inspect/fit/apply/compare commands, follow
[Fonts and tokens](guides/fonts-tokens.md) and [Color workflow](guides/color-workflow.md).
Use verified job paths; keep raw images unchanged. The color helper exports tagged
8-bit sRGB and cannot certify HDR/RAW or print production.

The [writing guide](guides/writing.md) adapts OMP practices and provides optional
cliché/AST checks with reviewable findings. Install its dependency only when needed:

```bash
npm install --prefix scripts/writing --ignore-scripts
node scripts/writing/lint.mjs draft.md
```

See [third-party notices](THIRD_PARTY_NOTICES.md) for sources and licenses, and
[CHANGELOG.md](CHANGELOG.md) for version history. A clean automated check is evidence
for its specific checks, not proof of complete accessibility or factual accuracy.
