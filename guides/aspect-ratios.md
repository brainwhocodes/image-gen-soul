# Give every format its own frame

A ratio is a composition decision. A wide hero, square tile and portrait poster have different jobs; changing width and height alone does not solve them.

## Write the destination into the prompt

| Format | Useful prompt instruction | Review |
|---|---|---|
| 3:2 source for a wide hero | Subject right; quiet left half for live text | Wide crop keeps subject and heading space |
| 16:9 banner | Recompose with a low horizon and horizontal breathing room | Top and bottom do not carry essential detail |
| 1:1 content tile | One readable focal subject with space around its silhouette | Recognizable at 240 pixels |
| 4:5 editorial image | Bring the main subject into a stable vertical grouping | Face, hands and required objects remain whole |
| 9:16 mobile story | Stack focal elements vertically; identify text-safe regions | Actual placement-specific overlays checked separately |

These are working design ratios, not claims about a social platform's current upload specifications. Verify platform-specific requirements when needed.

## Wide hero prompt

> Make a wide 3:2 source image for a landing page. Keep the focal architecture in the right third and the lower edge. Reserve the left 45 percent for two lines of live heading text. Keep the upper left quiet and dark. Avoid essential objects at the far edges. Render art only; HTML supplies the navigation, heading and buttons.

The three live examples use actual 1536 × 1024 hero sources. Their wide desktop crops are deliberate. At narrow widths, the examples place the text in a separate solid-color region and show the full source artwork below it, preserving the subject without squeezing the desktop composition.

## Portrait adaptation prompt

> Use the approved wide image as the treatment and color anchor. Make a new 4:5 composition, moving the main subject toward the lower center and reserving the upper third for text. Keep camera logic, material and color relationships. Recompose the scene; do not stretch the wide image. Return this as a new generated variant and record its actual dimensions.

This is a reusable prompting example; the guide does not claim a portrait image was generated from this prompt.

## Implement the crop intentionally

```css
.hero-art {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: 65% center;
}
@media (max-width: 700px) {
  .hero-art {
    height: auto;
    object-fit: contain;
  }
}
```

`cover` crops; it does not stretch. If neither a tested crop nor a separate text region works, generate a dedicated mobile composition and use `<picture>` with explicit sources. Verify the image tool's returned dimensions instead of claiming a requested ratio was necessarily honored.
