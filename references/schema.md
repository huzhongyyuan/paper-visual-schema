# Visual Schema 1.0

The JSON document is the authoritative blueprint. The compiled Markdown is derived from it. All fields below are required unless marked optional. Unknown fields are rejected to catch misspellings; change `schema_version` and the tooling together for a future contract.

## Top level

| Field | Meaning |
| --- | --- |
| `schema_version` | The string `1.0`. |
| `layout` | `pipeline`, `cyclic`, `hierarchical`, `parallel`, `hub`, or `hybrid`. |
| `composition` | Brief physical arrangement and why it matches the computation. |
| `canvas` | Object with positive integer `width`, `height` in pixels, `background: "#FFFFFF"`, and `label_mode: "render"` or `"deferred"`. Dimensions are requested export targets, not a claim about a renderer's capabilities. |
| `labels` | Object mapping stable IDs to exact nonempty visible strings. |
| `sources` | Object mapping stable IDs to short excerpts from supplied material. Keep citations or section locators in the string if available. This is evidence linkage, not automatic factual verification. |
| `zones` | Nonempty list of region objects. 2–5 is a useful design default, not a validity requirement. |
| `nodes` | Nonempty list of drawable objects contained within zones. |
| `connections` | List of directed connections between nodes. Can be empty when the source only establishes separate components. |

IDs use ASCII letters, digits, underscores and hyphens, begin with a letter, and are unique across zones, nodes and connections. Label and source IDs have their own namespaces.

## Coordinates and appearance

`box` is `[x, y, width, height]`, measured in percentages of the **whole canvas**, including for nodes inside zones. Origin is the top-left. Values are finite numbers, widths/heights are positive, and the box stays within `[0, 100]` on both axes. A node's box must be contained in its zone. These are independent horizontal/vertical percentages; use the canvas aspect ratio when judging physical shape.

`shape` is a concrete description, such as `rounded rectangle`, `three offset document sheets`, `4 by 4 square-cell grid`, or `circle containing three linked dots`. `visual` describes physical internal objects and their arrangement. Avoid descriptions like “semantic understanding happens here.”

`fill` is a six-digit hex color. Suggested fills: blue `#E5F0FB`, orange `#FBE6D8`, mint `#DEF1E6`, gray `#F0F2F5`; use dark ink `#243247` and white background. Color is a suggestion, not the sole carrier of algorithmic meaning. Use flat fills, consistent outlines and no perspective, gradients or shadows.

`label` is either a key in `labels` or JSON `null` for an object with no text. Every declared label must be attached to at least one zone, node or connection. Reuse a label deliberately if its text appears multiple times. A visible title or legend must have an explicit object and label, rather than existing only as an unattached string.

## Zone

```json
{"id":"z_input","box":[3,10,24,75],"shape":"rounded rectangle","visual":"Two stacked input tiles with a wide central gutter.","fill":"#F0F2F5","label":"l_inputs"}
```

## Node

```json
{"id":"n_rgb","zone":"z_input","box":[7,25,16,20],"shape":"rectangular image tile","visual":"A rectangle containing three flat mountain polygons; an illustrative image glyph, not a measured output.","fill":"#E5F0FB","label":"l_rgb","phase":"both","evidence":["s1"]}
```

`phase` is `training`, `inference`, or `both`. `evidence` is a nonempty list of keys in `sources`, covering the component's claimed role. Grouping boxes do not require an evidence entry. Node `visual` may request a dashed outline for a training-only component; make the phase readable without color when it matters.

## Connection

```json
{"id":"e_rgb","source":"n_rgb","target":"n_encoder","kind":"data","phase":"both","stroke":"solid","route":"Horizontal arrow from the east midpoint of n_rgb to the west midpoint of n_encoder, through the open gutter.","label":null,"evidence":["s1"]}
```

`kind` is `data`, `control`, `loss`, `gradient`, or `feedback`. `stroke` is `solid`, `dashed`, or `dotted`; choose a consistent figure-specific meaning and label it when ambiguous. `route` specifies physical endpoints, direction, bends and arrowheads. A feedback edge must include a curved/loop/return routing instruction and the source must establish what is iterated. Any visible edge caption needs its own `label` reference.

The connection's phase must be supported by **both** endpoint nodes. For example, an inference edge cannot enter a training-only loss node. For a phase-specific diagram, set its nodes and edges accordingly. A loss or gradient arrow is not automatically algorithmic feedback; classify it by its actual role.

This format does not model nested nodes, multiple pages, automatic port placement, tensor arithmetic or orthogonal routing. Express a needed compound object in `visual`, or use a suitable vector editor. The validator does not detect overlaps, semantic hallucinations, text fit, missing scientific relationships or whether a renderer followed the blueprint.

## Files and handoff

1. The Architect supplies JSON, optionally wrapped in one `json` code fence and/or the two `---BEGIN PROMPT---` / `---END PROMPT---` marker lines.
2. `schema_tool.py validate` checks the contract. Duplicate JSON keys and non-finite values are rejected rather than silently overwritten.
3. `schema_tool.py compile` emits the standalone Renderer instructions plus a `[VISUAL SCHEMA]` in the original Markdown style: layout, whitelist, zones with nodes, and explicit connections. Evidence excerpts stay in the JSON and do not enter the rendering prompt.
4. In manual use, paste the JSON into the Renderer template directly. Metadata and evidence remain non-rendered instructions in either route.
