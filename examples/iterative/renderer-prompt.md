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

---BEGIN PROMPT---

[VISUAL SCHEMA]

[Style & Meta-Instructions]
Flat 2D scientific schematic. Thin dark outlines, pastel fills, white background.
No perspective, gradients, shadows, or decorative elements.

[LAYOUT CONFIGURATION]
**Selected Layout**: cyclic
**Composition Logic**: An observation and initial state enter a horizontal three-block update loop. A broad curved return arrow runs below the update blocks. The final estimate sits to the right.
**Canvas**: 2400 x 1200 px; background #FFFFFF
**Label Mode**: render
**Coordinates**: [x,y,width,height], percentages of the whole canvas, origin top-left.

[TEXT WHITELIST]
- l_inputs: "Given"
- l_loop: "Iterative update"
- l_output: "Estimate"
- l_y: "Observation y"
- l_s0: "Initial state s_0"
- l_state: "State s_t"
- l_update: "Update block"
- l_candidate: "State s_(t+1)"
- l_estimate: "Final state"
- l_return: "Next iteration"
- l_stop: "After K updates"

[ZONE 1: z_input]
**Container**: rounded rectangle; box [2, 15, 15, 65]; fill #F0F2F5
**Visual Structure**: Two vertically separated tiles containing the given observation and initial state.
**Key Text Labels**: l_inputs: "Given"
- Object n_y: rounded rectangle; box [4, 25, 11, 14]; fill #F0F2F5; phase inference.
  Interior: A compact fixed 3 by 3 grid; decorative cells, no asserted observation dimension.
  Key Text Labels: l_y: "Observation y"
- Object n_s0: rounded rectangle; box [4, 53, 11, 14]; fill #F0F2F5; phase inference.
  Interior: Three offset horizontal sheets; an initial-state glyph.
  Key Text Labels: l_s0: "Initial state s_0"

[ZONE 2: z_loop]
**Container**: rounded rectangle; box [22, 15, 60, 65]; fill #E5F0FB
**Visual Structure**: Three horizontal blocks with a wide empty lower gutter reserved for the return arrow.
**Key Text Labels**: l_loop: "Iterative update"
- Object n_state: rounded rectangle; box [26, 48, 12, 14]; fill #E5F0FB; phase inference.
  Interior: A rectangular register containing a short row of three cells.
  Key Text Labels: l_state: "State s_t"
- Object n_update: rounded rectangle; box [45, 48, 12, 14]; fill #E5F0FB; phase inference.
  Interior: A plain computation block with two small input ports on the top and left; no invented internal algorithm.
  Key Text Labels: l_update: "Update block"
- Object n_candidate: rounded rectangle; box [65, 48, 12, 14]; fill #E5F0FB; phase inference.
  Interior: A rectangular state tile containing a short row of three cells.
  Key Text Labels: l_candidate: "State s_(t+1)"

[ZONE 3: z_output]
**Container**: rounded rectangle; box [87, 15, 11, 65]; fill #DEF1E6
**Visual Structure**: A single estimate tile.
**Key Text Labels**: l_output: "Estimate"
- Object n_estimate: rounded rectangle; box [88, 48, 9, 14]; fill #DEF1E6; phase inference.
  Interior: One state tile with the same three-cell glyph as the current-state tile.
  Key Text Labels: l_estimate: "Final state"

[CONNECTIONS]
1. e_y: n_y -> n_update; kind data; phase inference; solid stroke. Arrow from the east midpoint of n_y to (51,32), then down to the north midpoint of n_update at (51,48). Key Text Labels: none (no text)
2. e_init: n_s0 -> n_state; kind data; phase inference; solid stroke. Arrow from the east midpoint of n_s0 at (15,60), right to (20,60), up to (20,55), then into the west midpoint of n_state at (26,55). Key Text Labels: none (no text)
3. e_state: n_state -> n_update; kind data; phase inference; solid stroke. Horizontal arrow from the east midpoint of n_state to the west midpoint of n_update. Key Text Labels: none (no text)
4. e_update: n_update -> n_candidate; kind data; phase inference; solid stroke. Horizontal arrow from the east midpoint of n_update to the west midpoint of n_candidate. Key Text Labels: none (no text)
5. e_return: n_candidate -> n_state; kind feedback; phase inference; solid stroke. A broad curved arrow looping back from the south midpoint of n_candidate at (71,62), down into the empty gutter at y=73, left across the gutter, then up into the south midpoint of n_state at (32,62). This returns s_(t+1) as the next current state; place the caption below the curve. Key Text Labels: l_return: "Next iteration"
6. e_stop: n_candidate -> n_estimate; kind control; phase inference; solid stroke. Horizontal arrow from the east midpoint of n_candidate to the west midpoint of n_estimate, with its caption directly above the arrow. Key Text Labels: l_stop: "After K updates"

---END PROMPT---
