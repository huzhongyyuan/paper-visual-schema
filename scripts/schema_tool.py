#!/usr/bin/env python3
"""Validate Visual Schema 1.0 and compile it to a standalone image prompt.

Python 3.10+; standard library only. This checks structure, not scientific truth.
"""

import argparse
import json
import math
from pathlib import Path
import re
import sys


class SchemaError(ValueError):
    """A blueprint violates the published contract."""


ID = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")
COLOR = re.compile(r"#[0-9A-Fa-f]{6}\Z")
PHASES = {"training": {"training"}, "inference": {"inference"},
          "both": {"training", "inference"}}


def require(ok, message):
    if not ok:
        raise SchemaError(message)


def fields(value, names, path):
    require(isinstance(value, dict), f"{path}: expected an object")
    expected = set(names.split())
    require(set(value) == expected,
            f"{path}: missing {sorted(expected - set(value))}; "
            f"unknown {sorted(set(value) - expected)}")


def nonempty(value, path):
    require(isinstance(value, str) and bool(value.strip()),
            f"{path}: expected nonempty text")


def member(value, choices, path):
    require(isinstance(value, str) and value in choices,
            f"{path}: expected one of {sorted(choices)}")


def text_map(value, path, allow_empty=False):
    require(isinstance(value, dict), f"{path}: expected an object")
    require(allow_empty or bool(value), f"{path}: cannot be empty")
    for key, text in value.items():
        require(isinstance(key, str) and ID.fullmatch(key),
                f"{path}: invalid ID {key!r}")
        nonempty(text, f"{path}.{key}")


def box(value, path):
    require(isinstance(value, list) and len(value) == 4,
            f"{path}: expected [x,y,width,height]")
    require(all(type(n) in (int, float) and math.isfinite(n) for n in value),
            f"{path}: coordinates must be finite numbers, not booleans")
    x, y, w, h = value
    require(x >= 0 and y >= 0 and w > 0 and h > 0
            and x + w <= 100 + 1e-9 and y + h <= 100 + 1e-9,
            f"{path}: box must have positive area and stay inside the canvas")


def duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise SchemaError(f"non-finite JSON number: {value}")


def load_schema(text):
    text = text.strip()
    if text.startswith("---BEGIN PROMPT---"):
        require(text.endswith("---END PROMPT---"), "missing END PROMPT marker")
        text = text[len("---BEGIN PROMPT---"):-len("---END PROMPT---")].strip()
    if text.startswith("```"):
        match = re.fullmatch(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
        require(match is not None, "expected a single JSON code fence")
        text = match.group(1)
    return json.loads(text, object_pairs_hook=duplicate_keys,
                      parse_constant=reject_constant)


def validate(schema):
    fields(schema, "schema_version layout composition canvas labels sources "
           "zones nodes connections", "schema")
    require(schema["schema_version"] == "1.0", "unsupported schema_version")
    member(schema["layout"], {"pipeline", "cyclic", "hierarchical", "parallel",
                             "hub", "hybrid"}, "layout")
    nonempty(schema["composition"], "composition")
    canvas = schema["canvas"]
    fields(canvas, "width height background label_mode", "canvas")
    for key in ("width", "height"):
        require(type(canvas[key]) is int and canvas[key] > 0,
                f"canvas.{key}: expected a positive integer")
    require(canvas["background"] == "#FFFFFF", "canvas.background: use #FFFFFF")
    member(canvas["label_mode"], {"render", "deferred"}, "canvas.label_mode")
    text_map(schema["labels"], "labels", allow_empty=True)
    text_map(schema["sources"], "sources")
    objects, used_labels = {}, set()
    for collection in ("zones", "nodes", "connections"):
        items = schema[collection]
        require(isinstance(items, list), f"{collection}: expected a list")
        require(collection == "connections" or bool(items),
                f"{collection}: cannot be empty")
        for index, item in enumerate(items):
            path = f"{collection}[{index}]"
            keys = {
                "zones": "id box shape visual fill label",
                "nodes": "id zone box shape visual fill label phase evidence",
                "connections": "id source target kind phase stroke route label evidence",
            }[collection]
            fields(item, keys, path)
            ident = item["id"]
            require(isinstance(ident, str) and ID.fullmatch(ident), f"{path}: invalid ID")
            require(ident not in objects, f"duplicate object ID: {ident}")
            objects[ident] = item
            label = item["label"]
            require(label is None or (isinstance(label, str) and label in schema["labels"]),
                    f"{ident}: unknown label reference {label!r}")
            if label is not None:
                used_labels.add(label)
            if collection != "connections":
                box(item["box"], f"{ident}.box")
                for key in ("shape", "visual"):
                    nonempty(item[key], f"{ident}.{key}")
                require(isinstance(item["fill"], str) and COLOR.fullmatch(item["fill"]),
                        f"{ident}.fill: expected a six-digit hex color")
            if collection != "zones":
                member(item["phase"], PHASES, f"{ident}.phase")
                evidence = item["evidence"]
                require(isinstance(evidence, list) and bool(evidence),
                        f"{ident}.evidence: expected a nonempty reference list")
                for ref in evidence:
                    require(isinstance(ref, str) and ref in schema["sources"],
                            f"{ident}: unknown source reference {ref!r}")
    require(used_labels == set(schema["labels"]),
            f"unattached labels: {sorted(set(schema['labels']) - used_labels)}")
    zones = {z["id"]: z for z in schema["zones"]}
    nodes = {n["id"]: n for n in schema["nodes"]}
    for node in nodes.values():
        zid = node["zone"]
        require(isinstance(zid, str) and zid in zones,
                f"{node['id']}: unknown zone {zid!r}")
        x, y, w, h = node["box"]
        zx, zy, zw, zh = zones[zid]["box"]
        require(x >= zx - 1e-9 and y >= zy - 1e-9
                and x + w <= zx + zw + 1e-9 and y + h <= zy + zh + 1e-9,
                f"{node['id']}: node box extends outside its zone")
    for edge in schema["connections"]:
        ident = edge["id"]
        for endpoint in ("source", "target"):
            value = edge[endpoint]
            require(isinstance(value, str) and value in nodes,
                    f"{ident}: unknown {endpoint} node {value!r}")
            require(PHASES[edge["phase"]] <= PHASES[nodes[value]["phase"]],
                    f"{ident}: phase conflicts with {endpoint} node {value}")
        member(edge["kind"], {"data", "control", "loss", "gradient", "feedback"},
               f"{ident}.kind")
        member(edge["stroke"], {"solid", "dashed", "dotted"}, f"{ident}.stroke")
        nonempty(edge["route"], f"{ident}.route")
        if edge["kind"] == "feedback":
            require(re.search(r"\b(curv\w*|loop\w*|return\w*)\b", edge["route"], re.I),
                    f"{ident}: feedback needs an explicit curved/loop/return route")
    return schema


def compile_prompt(schema):
    validate(schema)
    template = (Path(__file__).resolve().parents[1] / "prompts" / "renderer.md").read_text(encoding="utf-8")
    intro = template.split("# Visual Schema\n", 1)[0].rstrip()
    quoted = lambda value: json.dumps(value, ensure_ascii=False)
    label = lambda item: ("none (no text)" if item["label"] is None else
                          f'{item["label"]}: {quoted(schema["labels"][item["label"]])}')
    canvas = schema["canvas"]
    lines = [intro, "", "---BEGIN PROMPT---", "", "[VISUAL SCHEMA]", "",
             "[Style & Meta-Instructions]",
             "Flat 2D scientific schematic. Thin dark outlines, pastel fills, white background.",
             "No perspective, gradients, shadows, or decorative elements.", "",
             "[LAYOUT CONFIGURATION]", f'**Selected Layout**: {schema["layout"]}',
             f'**Composition Logic**: {schema["composition"]}',
             f'**Canvas**: {canvas["width"]} x {canvas["height"]} px; background {canvas["background"]}',
             f'**Label Mode**: {canvas["label_mode"]}',
             "**Coordinates**: [x,y,width,height], percentages of the whole canvas, origin top-left.",
             "", "[TEXT WHITELIST]"]
    lines.extend(f"- {key}: {quoted(value)}" for key, value in schema["labels"].items())
    for index, zone in enumerate(schema["zones"], 1):
        lines.extend(["", f'[ZONE {index}: {zone["id"]}]',
                      f'**Container**: {zone["shape"]}; box {zone["box"]}; fill {zone["fill"]}',
                      f'**Visual Structure**: {zone["visual"]}', f'**Key Text Labels**: {label(zone)}'])
        for node in schema["nodes"]:
            if node["zone"] == zone["id"]:
                lines.extend([f'- Object {node["id"]}: {node["shape"]}; box {node["box"]}; fill {node["fill"]}; phase {node["phase"]}.',
                              f'  Interior: {node["visual"]}', f'  Key Text Labels: {label(node)}'])
    lines.extend(["", "[CONNECTIONS]"])
    for index, edge in enumerate(schema["connections"], 1):
        lines.append(f'{index}. {edge["id"]}: {edge["source"]} -> {edge["target"]}; '
                     f'kind {edge["kind"]}; phase {edge["phase"]}; {edge["stroke"]} stroke. '
                     f'{edge["route"]} Key Text Labels: {label(edge)}')
    if not schema["connections"]:
        lines.append("No connections specified; do not invent relationships.")
    lines.extend(["", "---END PROMPT---", ""])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "compile"))
    parser.add_argument("schema", type=Path)
    parser.add_argument("--output", type=Path, help="Compile to a file; otherwise use stdout")
    args = parser.parse_args(argv)
    if args.command == "validate" and args.output:
        parser.error("--output applies only to compile")
    try:
        schema = validate(load_schema(args.schema.read_text(encoding="utf-8")))
        if args.command == "validate":
            print(f"VALID: {len(schema['zones'])} zones, {len(schema['nodes'])} nodes, "
                  f"{len(schema['connections'])} connections; scientific meaning not checked.")
        else:
            prompt = compile_prompt(schema)
            if args.output:
                require(args.output.resolve() != args.schema.resolve(),
                        "output must not overwrite the source schema")
                args.output.write_text(prompt, encoding="utf-8")
                print(f"Wrote {args.output}")
            else:
                print(prompt, end="")
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
