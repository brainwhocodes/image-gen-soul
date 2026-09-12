# Reference analysis and prompt construction

This guide is a method, not a collection of looks. All visual decisions must come
from the current images and brief. The phrase “soul” means the handful of
observable design relationships that make those references recognizable.

## Reference roles and precedence

Separate the reference's visual treatment from its subject and its production
layout. A screenshot might supply column proportions without supplying color. A
product photo might supply product identity without supplying lighting. A poster
might supply typographic hierarchy without supplying exact event wording.

For each selected image, record its verified file identifier/path, relevant
roles, and what it should NOT contribute. Choose principal anchors by role. Use
explicit user instructions first, approved brand constraints second, then the
principal reference for that role, then compatible supporting references, then
reversible design defaults. A newly requested override can deliberately change
the existing look; do not fight it by blindly matching all original pixels.

When images conflict, name the conflict in ordinary language and choose an anchor
or ask one focused question. More references do not automatically mean more
fidelity. Do not average different seasons, white backgrounds, dark screenshots,
portraits, and logos into one image-wide grading target.

## A compact job contract

Use this small table mentally or in the current job record:

| Property | Preserve | Change | Reference or instruction |
|---|---|---|---|
| Subject/product identity | As specified | Only requested modifications | Actual subject asset |
| Composition | Relative scale, viewpoint, hierarchy as needed | Reframe for destination | Composition anchor |
| Treatment | Actual edge, material, and detail behavior | Explicit stylistic requests | Treatment anchor |
| Color | Selected relationships or brand constraints | Intentional prompt override | Color anchor |
| Copy/layout | Exact approved text and marks | New size or hierarchy as requested | User and layout anchor |

Do not fill missing facts with fabricated event details, prices, claims, brand
assets, or fake endorsements. A clearly labeled art-only draft may proceed while
final copy remains unresolved.

## What to inspect

Look at the image both small and large. At small size, identify the dominant
shape, focal hierarchy, light/dark grouping, negative space, and color-area
relationships. At large size, inspect edges, brush or grain structure, material
behavior, repeated geometry, lettering, and artifacts. A sampled color is not a
semantic label: the same hue can belong to skin, a package, or a backdrop.

Describe composition with positions and proportions when helpful. “Keep the
subject in the right third and reserve the left half for live heading text” is
more useful than “a stunning composition.” Use approximate normalized boxes
`[left, top, right, bottom]` in [0,1] for important content or quiet zones. These
are layout targets, not promises that a model obeys coordinates exactly.

Separate observation from inference. “Fine irregular dots are visible” is an
observation. “Probably screen printed” is an inference. Do not turn uncertain
medium or font identification into a hard requirement unless that is the desired
interpretation.

## A neutral prompt scaffold

Fill the fields only from the current job. Delete irrelevant fields.

> Produce [asset type] at [aspect ratio and intended dimensions]. Use [actual
> reference identifier] for [specified roles]. Preserve [specific observed
> composition/treatment relationships]. Use [other reference] only for [role],
> not for [excluded property].
>
> Depict [subject and requested content], with [viewpoint, scale, spatial
> relationships, foreground/middle/background where applicable]. Change
> [explicit requested differences]. Keep [protected details] unchanged.
>
> Arrange [focal elements] within [layout constraints]. Reserve [copy/negative
> space] and preserve it in [required alternate crops].
>
> Match [observed material/rendering behavior], [edge/detail distribution],
> [lighting/value relationships], and [reference-derived color relationships].
> Apply [explicit intentional departure] rather than matching that aspect
> literally.
>
> Keep [structural, brand, text, transparency, or crop invariants]. Avoid
> [task-specific failure modes]. Include/exclude text as specified. Deliver
> [opaque full scene, transparent foreground, clean background, or other output].

Do not leave bracket placeholders in an actual generation request. When the
user requests a reusable template, retain only intentional variables and explain
which references must accompany it. A descriptive prompt cannot capture every
property of an image; use supported image conditioning when available.

## Close recreation versus variation

For close recreation, preserve framing, major silhouettes, viewpoint, relative
scale, spacing, value blocks, texture scale, and color placement. Editing or
compositing the supplied asset is preferable when exact fidelity is the point.
A generative reconstruction is not a guaranteed identical duplicate.

For a variation, freeze the relevant visual relationships and change the stated
axis. Name the original focal subjects and their replacements: different people,
objects, items or scene elements. A barely perceptible change or recolor alone
does not satisfy a meaningful variation unless the user requested that operation. A new subject does not automatically authorize new typography, new color
grading, new lighting, or a different rendering method. A new format may require
composition changes even when color and treatment stay locked.

For several variants, keep an explicit variant table with changed fields and
locked fields. Do not change every property in every version. Once a direction
is approved, return to that approved anchor for subsequent variants so successive
derivatives do not accumulate drift. Record real returned tool settings, not
invented reproducibility claims.

## Background and foreground prompts

Decompose only when it helps editing, compositing, or the intended layout.
Independently generated layers do not automatically align. Prefer extracting or
editing layers from an approved full composition when exact alignment matters.

A background prompt must define the shared camera, horizon or plane, scale,
lighting direction, depth treatment, output size, and the areas intentionally
left open. It should continue naturally behind the future foreground; do not
create empty white holes or bake in shadows/reflections from objects that are
not yet positioned.

A foreground prompt must share the same camera, horizon, scale, lighting,
resolution, and style rules. Define its placement and silhouette, which gaps
need real transparency, and which interaction effects belong to separate layers.
Do not paint a checkerboard into the image. A flat matte is not alpha.

Generate or compose cast shadows, contact darkening, reflections, occlusion,
and atmosphere only after foreground placement is established. Protect exact
logos and text from a scene-wide grade. For naturally integrated scene elements,
use a shared artwork grade or coordinated masked grades; for brand overlays,
place locked colors afterward.

For foreground-only or background-only prompt expansion, return the requested
prompt rather than automatically generating both assets.

## Targeted failure prevention

Choose exclusions based on the scene. Architecture needs coherent perspective,
product imagery needs accurate proportions and markings, faces/hands need
plausible anatomy, diagrams need logical relationships, and layouts need exact
copy and hierarchy. Never add “no texture” to a texture-led reference or “no
photography” to a photographic reference by habit.

If a result is wrong structurally, correct the offending instruction or edit
that region. Color grading is not a substitute for fixing wrong construction.

## Generate, inspect and retain evidence

Use the actual selected references through the host's supported attachment mechanism.
Keep inputs and raw outputs unchanged; use versioned paths. For prompt-only work,
return the complete prompt with its reference requirements and do not generate.
Record only real returned settings, dimensions and tool identifiers.

Inspect the returned image at composition and detail scale. Confirm the named
substitutions, invariants, subject count, physical construction, crop and copy-safe
space. Repair structure before grading and preserve unaffected regions. Never
automatically make the result brighter, cooler, smoother or more photographic.

Use [Production layouts](production-layouts.md) for formats, series and exact
overlays; use [Color workflow](color-workflow.md) only when comparing or correcting
color. Retain actual prompts, attachment identities, raw/final files, dimensions,
measurements, the correction decision and export checks in [job.json](../templates/job.json)
or an equivalent job record. Guidance pages must distinguish originals from new
variations and show the preserve/change choices and reproducible steps. An unknown
original prompt stays unknown; a proposed reconstruction is labeled as a suggestion.
