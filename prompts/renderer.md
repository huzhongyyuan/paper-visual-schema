# The Renderer — physical blueprint to figure

Generate one professional academic architecture diagram from the visual schema below. The schema may be structured JSON or its compiled Markdown equivalent. Read metadata as instructions; depict only the method it specifies.

## Visual execution

- Follow the given canvas aspect ratio, normalized boxes, reading order, object arrangement, endpoint IDs and arrow routes. Treat dimensions as the requested export size; use the closest supported size if the tool has fixed resolutions, and report the actual size separately.
- Use flat 2D vector-like geometry, consistent thin dark outlines, soft pastel fills and a clean white background. Keep internal whitespace and visible arrowheads. No perspective, gradients, shadows, textures, watermarks or decorative objects. This describes an aesthetic; raster generation does not create an editable vector file.
- A node's `visual` describes its interior; its `shape` describes its physical boundary or glyph. Keep nodes inside their zones. Keep labels and lines clear of each other. Preserve all specified branches, phase distinctions and return paths. Do not create an extra connection to make the picture look balanced.
- Use clean sans-serif typography with consistent size hierarchy and legible weight. Fit labels at the intended final size; retain the exact scientific terms.

## Exact text contract

- Render only strings explicitly in `labels` / `[TEXT WHITELIST]`, at the zone, node or connection that references them. Render an attached string exactly, including case, signs and subscripts as supported. Do not invent titles or captions.
- Never render field names, IDs, evidence excerpts, source references or instruction headings. Examples: `ZONE 1`, `LAYOUT CONFIGURATION`, `Container`, `visual`, `training`, `n1` and `s1` are metadata unless separately attached as whitelisted labels. Words such as “Input” and “Output” are permitted when explicitly whitelisted.
- If `label_mode` is `deferred`, render **no text**, including whitelisted text, and leave the specified label spaces clear for later typesetting. A deferred-text image is an intermediate, not a finished labelled figure.

## Fidelity check

Compare the drawing with the schema before returning it: every required object exists, every arrow connects the right endpoints in the right direction, training-only paths remain distinct, and every rendered character belongs to an attached whitelisted string. Preserve mathematical and topological meaning before aesthetic refinements. Do not fabricate numerical or qualitative experimental results.

Return the image through the rendering tool. Report export dimensions, tool limitations or any unresolved discrepancy outside the image, if the interface allows prose. Do not claim that this instruction alone guarantees correct labels or topology.

# Visual Schema

Paste the Architect's JSON or the complete compiled `---BEGIN PROMPT---` … `---END PROMPT---` block below. Leave the structure intact.
