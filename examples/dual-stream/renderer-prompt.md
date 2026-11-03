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
**Selected Layout**: parallel
**Composition Logic**: Two horizontal RGB/depth lanes run left to right into a shared prediction path. A separate dashed loss box sits below the lanes and is used only during training.
**Canvas**: 2400 x 1200 px; background #FFFFFF
**Label Mode**: render
**Coordinates**: [x,y,width,height], percentages of the whole canvas, origin top-left.

[TEXT WHITELIST]
- l_inputs: "Inputs"
- l_encoders: "Separate encoders"
- l_predict: "Fusion and prediction"
- l_rgb: "RGB image"
- l_depth: "Depth image"
- l_re: "RGB encoder"
- l_de: "Depth encoder"
- l_rf: "RGB features"
- l_df: "Depth features"
- l_concat: "Concatenate"
- l_classifier: "Classifier"
- l_class: "Class"
- l_loss: "Alignment loss (train only)"

[ZONE 1: z_input]
**Container**: rounded rectangle; box [2, 12, 16, 64]; fill #F0F2F5
**Visual Structure**: Two vertically separated image glyphs.
**Key Text Labels**: l_inputs: "Inputs"
- Object n_rgb: rounded rectangle; box [4, 25, 12, 16]; fill #E5F0FB; phase both.
  Interior: A rectangular image glyph with three flat colored polygons; illustrative, not an experimental image.
  Key Text Labels: l_rgb: "RGB image"
- Object n_depth: rounded rectangle; box [4, 54, 12, 16]; fill #E5F0FB; phase both.
  Interior: A rectangular tile divided into three flat gray bands; no depth values.
  Key Text Labels: l_depth: "Depth image"

[ZONE 2: z_encode]
**Container**: rounded rectangle; box [24, 12, 28, 64]; fill #F0F2F5
**Visual Structure**: Two independent horizontal lanes. Each contains an encoder block followed by a token strip.
**Key Text Labels**: l_encoders: "Separate encoders"
- Object n_re: rounded rectangle; box [27, 25, 11, 16]; fill #E5F0FB; phase both.
  Interior: Three thin vertical plates followed by a wider rectangle; an encoder glyph.
  Key Text Labels: l_re: "RGB encoder"
- Object n_de: rounded rectangle; box [27, 54, 11, 16]; fill #E5F0FB; phase both.
  Interior: Three thin vertical plates followed by a wider rectangle; a separate encoder glyph.
  Key Text Labels: l_de: "Depth encoder"
- Object n_rf: rounded rectangle; box [41, 25, 8, 16]; fill #E5F0FB; phase both.
  Interior: A row of four narrow rectangular tokens. The four glyphs do not assert a tensor dimension.
  Key Text Labels: l_rf: "RGB features"
- Object n_df: rounded rectangle; box [41, 54, 8, 16]; fill #E5F0FB; phase both.
  Interior: A row of four narrow rectangular tokens. The four glyphs do not assert a tensor dimension.
  Key Text Labels: l_df: "Depth features"

[ZONE 3: z_predict]
**Container**: rounded rectangle; box [58, 12, 40, 64]; fill #DEF1E6
**Visual Structure**: A central concatenation block followed by a classifier and class tile.
**Key Text Labels**: l_predict: "Fusion and prediction"
- Object n_concat: rounded rectangle; box [62, 39, 12, 16]; fill #DEF1E6; phase both.
  Interior: Two token strips placed end to end inside the block. No plus sign.
  Key Text Labels: l_concat: "Concatenate"
- Object n_classifier: rounded rectangle; box [78, 39, 10, 16]; fill #DEF1E6; phase both.
  Interior: Three small dots on the left linked to two dots on the right; a schematic classifier glyph.
  Key Text Labels: l_classifier: "Classifier"
- Object n_class: rounded rectangle; box [91, 39, 5, 16]; fill #DEF1E6; phase both.
  Interior: A small blank class tile with one dark circular marker; no scores.
  Key Text Labels: l_class: "Class"

[ZONE 4: z_train]
**Container**: rounded rectangle; box [25, 81, 51, 17]; fill #FBE6D8
**Visual Structure**: One centered loss block, with ample room on either side for dashed incoming connectors.
**Key Text Labels**: none (no text)
- Object n_loss: rounded rectangle; box [39, 85, 23, 10]; fill #FBE6D8; phase training.
  Interior: A rounded box with a dashed outline. Its label explicitly states the training-only phase.
  Key Text Labels: l_loss: "Alignment loss (train only)"

[CONNECTIONS]
1. e_rgb: n_rgb -> n_re; kind data; phase both; solid stroke. Horizontal arrow from the east midpoint of n_rgb to the west midpoint of n_re. Key Text Labels: none (no text)
2. e_depth: n_depth -> n_de; kind data; phase both; solid stroke. Horizontal arrow from the east midpoint of n_depth to the west midpoint of n_de. Key Text Labels: none (no text)
3. e_re: n_re -> n_rf; kind data; phase both; solid stroke. Short horizontal arrow from the east midpoint of n_re to the west midpoint of n_rf. Key Text Labels: none (no text)
4. e_de: n_de -> n_df; kind data; phase both; solid stroke. Short horizontal arrow from the east midpoint of n_de to the west midpoint of n_df. Key Text Labels: none (no text)
5. e_rf: n_rf -> n_concat; kind data; phase both; solid stroke. Arrow from n_rf east midpoint (49,33) to (55,33), down to (55,43), then right into the upper west side of n_concat at (62,43). Key Text Labels: none (no text)
6. e_df: n_df -> n_concat; kind data; phase both; solid stroke. Arrow from n_df east midpoint (49,62) to (55,62), up to (55,51), then right into the lower west side of n_concat at (62,51). Key Text Labels: none (no text)
7. e_concat: n_concat -> n_classifier; kind data; phase both; solid stroke. Horizontal arrow from n_concat east midpoint to n_classifier west midpoint. Key Text Labels: none (no text)
8. e_class: n_classifier -> n_class; kind data; phase both; solid stroke. Horizontal arrow from n_classifier east midpoint to n_class west midpoint. Key Text Labels: none (no text)
9. e_loss_rgb: n_rf -> n_loss; kind loss; phase training; dashed stroke. Dashed arrow from the bottom of n_rf at (43,41), left to (40,43), down along x=40 to y=79, then right to (47,79) and down into n_loss at (47,85). At the crossing with e_de at (40,62), use a small bridge and no junction dot: these paths do not connect. Key Text Labels: none (no text)
10. e_loss_depth: n_df -> n_loss; kind loss; phase training; dashed stroke. Dashed arrow from the bottom midpoint of n_df at (45,70), down to (45,77), right to (54,77), then down into n_loss at (54,85). Key Text Labels: none (no text)

---END PROMPT---
