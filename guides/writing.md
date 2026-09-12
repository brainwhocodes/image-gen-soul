# Write copy that fits the product

Use this guide for page copy, navigation labels, forms, search results and help text. Apply it when writing a new site or revising an existing one with REDESIGN. The writing should explain what the reader can do, why it is useful and what happens after they act.

These practices are adapted from [OMP Writing](https://github.com/bnivanov/omp-writing-skills), especially its rules for editing, web copy and factual preservation. See [third-party notices](../THIRD_PARTY_NOTICES.md) for sources and licenses. This guide does not require another design skill or impose a default brand voice.

## Set the brief before drafting

Reuse the established site purpose, audience and tone. Ask only about missing decisions that would change the copy. Record the reader's task, the supported offer, available evidence and the intended next action in [the copy brief](../templates/copy-brief.md).

For an existing brand, inspect its supplied writing samples and preserve useful vocabulary and cadence. When samples are absent, describe a proposed voice using the user's brief and actual product. Do not claim that a proposed voice was inferred from customers. Give each example its own register: a fixture configurator needs exact selection language; a cinema programme can describe the imagined story behind each film.

Keep a factual inventory. Protect names, prices, units, conditions, qualifications, links and implemented behavior. Identify fictional content and local demonstrations where the distinction affects a decision. Marketing copy cannot create a payment service, care diagnosis, reservation, delivery promise or customer testimonial that the product does not support.

## Write the offer and the working interface separately

The marketing page should give a visitor enough information to choose. Describe the actual product, show the relevant details and address practical questions. Give each substantial section a reason to exist. For a textile catalogue, explain pattern scale before comparing formats. For a lighting page, compare fixture forms before asking for finish and color temperature. Keep meaningful content depth and the selected mockup's composition while cutting repeated claims.

Product copy should help someone finish a task. Buttons name actions such as “Download itinerary” or “Add to lighting schedule.” Search needs a useful empty state and recovery action. A form error should identify the field or failed operation and explain the next step. Confirmations describe what happened, including whether anything was sent or only saved locally. Keep labels stable across the interface, help text and exported results.

Write production headings, labels and representative body copy before generating UI mockups so the reference reflects realistic text lengths. Keep the final copy live in HTML. Text drawn by the image generator is a visual suggestion; it is not verified product information.

## Remove formulaic prose without flattening the voice

Read the whole page before editing. Keep clear sentences and useful technical detail. Repair the passage that causes the problem instead of forcing every paragraph into the same pattern.

- Replace vague promises with a supported action or consequence. “A workspace for every possibility” tells less than “Keep each reference beside the note explaining why you chose it.”
- Remove decorative sentence fragments and repeated slogan structures. Connect related thoughts when the relationship belongs in one sentence. Short interface labels and catalogue names can remain short.
- State the useful claim directly. Avoid invented contrasts, self-answered rhetorical hooks, dramatic colon reveals and generic conclusions that repeat the page.
- Keep ordinary verbs and exact domain terms. Remove inflated adjectives when the sentence provides no evidence for them. A real textile term or a literal landscape description should survive a keyword scan.
- Keep the brand's established tone without adding fabricated anecdotes, slang, typos, forced informality or random sentence lengths. Do not optimize for an AI-detector score or claim that a pattern reveals authorship.
- Check repeated metaphors and interchangeable paragraphs across sibling sites. If the same sentence could advertise any of them, replace it with something the current product actually does or remove it.

## Protect the material behind the copy

For a copy-only edit, preserve working controls, routes, IDs, code, numbers and data contracts. Change a factual value only when the user authorizes it and the underlying source supports the change. Keep a before snapshot and review the diff.

Never rewrite an exact historical image prompt, generated asset record, reference attribution, correction recipe or timestamp to match new copy. Leave original brand boards and UI concepts labeled as generation evidence. Capture the revised implementation and record that its copy changed after the concept. A text edit alone does not require new image generation; a material change to layout or imagery returns to the mockup workflow.

## Review and lint before delivery

Read headings in sequence, then read each page as a visitor. Check the offer against the working product and trace the main action through its labels, errors and result. Read important paragraphs aloud to catch repeated cadence and unclear references. Preserve the no-emoji, no-eyebrow, text-size, contrast, pointer and keyboard rules in [Interface rules](interface-rules.md).

The optional writing checker runs OMP's cliché patterns and the pinned Slopless AST checker. It needs Node.js and a one-time local dependency install; the image and color workflows still use their existing tools.

```bash
npm install --prefix scripts/writing --ignore-scripts
node scripts/writing/lint.mjs draft.md
```

Lint plain Markdown containing the intended reader-facing copy. For a built page, extract visible text and preserve heading, list and paragraph boundaries. Exclude code, raw data and exact historical prompts. Review those protected records for integrity separately. Do not feed serialized HTML or JavaScript to a prose linter and treat its output as a page review.

Exit 0 means no findings, 1 means review is needed and 2 means the checker could not complete. Inspect every finding in context. Repair filler and misleading copy; document precise exceptions for useful enumerations, literal terminology or required warnings. A clean scan does not prove accuracy, accessibility or originality. Report any unavailable checker instead of calling an incomplete run clean.

After editing, check text wrapping, navigation, controls and downloads at desktop and narrow widths and with enlarged text. Refresh affected previews and archives. Keep the published copy, source and reusable skill in sync under the user's existing publishing authorization.

## Example request

> Rewrite this site using Image Gen Soul's writing guide. Preserve its established tone, verified product details and working behavior. Replace generic slogans with concrete descriptions and action labels, keep useful content depth, and give each page a distinct purpose. Preserve original generation prompts and artwork records. Review the copy against the product, run the writing checks and verify the edited pages before publishing within my existing authorization.
