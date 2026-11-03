"""Contract tests: graph validity, phase semantics, lossless prompt handoff."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("schema_tool", ROOT / "scripts/schema_tool.py")
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.schema = tool.load_schema((ROOT / "examples/dual-stream/visual-schema.json").read_text())

    def rejected(self, change, message):
        candidate = deepcopy(self.schema)
        change(candidate)
        with self.assertRaisesRegex(tool.SchemaError, message):
            tool.validate(candidate)

    def test_bundled_examples(self):
        for path in sorted((ROOT / "examples").glob("*/visual-schema.json")):
            with self.subTest(path=path):
                tool.validate(tool.load_schema(path.read_text()))

    def test_raw_fenced_and_marked_handoffs(self):
        raw = json.dumps(self.schema)
        for text in [raw, f"```json\n{raw}\n```", f"---BEGIN PROMPT---\n{raw}\n---END PROMPT---",
                     f"---BEGIN PROMPT---\n```json\n{raw}\n```\n---END PROMPT---"]:
            self.assertEqual(tool.load_schema(text), self.schema)

    def test_duplicate_json_keys(self):
        with self.assertRaisesRegex(tool.SchemaError, "duplicate JSON key"):
            tool.load_schema('{"a":1,"a":2}')

    def test_nonfinite_json(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.assertRaisesRegex(tool.SchemaError, "non-finite"):
                tool.load_schema('{"a":' + value + '}')

    def test_duplicate_object_ids(self):
        self.rejected(lambda s: s["nodes"][0].update(id=s["zones"][0]["id"]), "duplicate object ID")

    def test_unknown_label(self):
        self.rejected(lambda s: s["nodes"][0].update(label="missing"), "unknown label")

    def test_unused_label(self):
        self.rejected(lambda s: s["labels"].update(unused="Stray title"), "unattached labels")

    def test_unknown_evidence(self):
        self.rejected(lambda s: s["connections"][0].update(evidence=["missing"]), "unknown source")

    def test_unknown_zone(self):
        self.rejected(lambda s: s["nodes"][0].update(zone="missing"), "unknown zone")

    def test_unknown_endpoint(self):
        self.rejected(lambda s: s["connections"][0].update(target="z_input"), "unknown target node")

    def test_out_of_canvas_box(self):
        self.rejected(lambda s: s["zones"][0].update(box=[90,0,20,10]), "inside the canvas")

    def test_out_of_zone_box(self):
        self.rejected(lambda s: s["nodes"][0].update(box=[80,25,12,16]), "outside its zone")

    def test_zero_area_and_bool_boxes(self):
        for bad in ([0,0,0,10], [True,1,10,10], [0,0,float("nan"),1]):
            self.rejected(lambda s: s["nodes"][0].update(box=bad), "box|coordinates")

    def test_endpoint_phase_conflict(self):
        # The real regression: the alignment loss exists only during training.
        self.rejected(lambda s: s["connections"][-1].update(phase="inference"), "phase conflicts")
        self.rejected(lambda s: s["connections"][-1].update(phase="both"), "phase conflicts")

    def test_feedback_route(self):
        path = ROOT / "examples/iterative/visual-schema.json"
        schema = tool.load_schema(path.read_text())
        next(e for e in schema["connections"] if e["kind"] == "feedback")["route"] = "Straight arrow."
        with self.assertRaisesRegex(tool.SchemaError, "explicit curved/loop/return"):
            tool.validate(schema)

    def test_unrecognized_field(self):
        self.rejected(lambda s: s["nodes"][0].update(lable="l_rgb"), "unknown.*lable")

    def test_wrong_types_fail_cleanly(self):
        for field in ("label", "phase", "zone", "fill"):
            self.rejected(lambda s: s["nodes"][0].update({field: []}), ".")

    def test_prompt_keeps_labels_and_edges_but_omits_source_excerpts(self):
        prompt = tool.compile_prompt(self.schema)
        for value in self.schema["labels"].values():
            self.assertIn(json.dumps(value, ensure_ascii=False), prompt)
        for edge in self.schema["connections"]:
            self.assertIn(f'{edge["source"]} -> {edge["target"]}', prompt)
            self.assertIn(edge["route"], prompt)
            self.assertIn(f'phase {edge["phase"]}', prompt)
        for excerpt in self.schema["sources"].values():
            self.assertNotIn(excerpt, prompt)

    def test_unicode_label_and_deferred_text(self):
        self.schema["labels"]["l_rgb"] = '图像 x_t / "RGB"'
        self.schema["canvas"]["label_mode"] = "deferred"
        prompt = tool.compile_prompt(self.schema)
        self.assertIn('图像 x_t / \\"RGB\\"', prompt)
        self.assertIn("**Label Mode**: deferred", prompt)

    def test_components_without_arrows_are_allowed(self):
        self.schema["connections"] = []
        tool.validate(self.schema)
        self.assertIn("do not invent relationships", tool.compile_prompt(self.schema))

    def test_cli_roundtrip_and_source_overwrite_protection(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "schema.json"
            output = Path(directory) / "renderer.md"
            raw = json.dumps(self.schema)
            source.write_text(raw)
            result = subprocess.run([sys.executable, str(ROOT / "scripts/schema_tool.py"),
                                     "compile", str(source), "--output", str(output)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_text(), tool.compile_prompt(self.schema))
            denied = subprocess.run([sys.executable, str(ROOT / "scripts/schema_tool.py"),
                                     "compile", str(source), "--output", str(source)],
                                    capture_output=True, text=True)
            self.assertEqual(denied.returncode, 2)
            self.assertEqual(source.read_text(), raw)

    def test_bad_cli_input_is_visible_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.json"
            source.write_text('{"schema_version":"1.0","schema_version":"1.0"}')
            result = subprocess.run([sys.executable, str(ROOT / "scripts/schema_tool.py"),
                                     "validate", str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("duplicate JSON key", result.stderr)


if __name__ == "__main__":
    unittest.main()
