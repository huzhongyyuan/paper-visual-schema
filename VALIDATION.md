# Initial validation — v0.1.0

As of 2026-11-02 (America/Los_Angeles). Local checks used Python 3.14.7. This record covers the repository's contract and bundled fixtures, not image-model quality.

| Check | Observed result |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | 22 tests passed, including CLI roundtrip, visible failures, malformed references/boxes and phase conflicts. |
| `python3 scripts/schema_tool.py validate examples/dual-stream/visual-schema.json` | Valid: 4 zones, 10 nodes, 10 connections. |
| `python3 scripts/schema_tool.py validate examples/iterative/visual-schema.json` | Valid: 3 zones, 6 nodes, 6 connections. |
| Compile both examples | Completed; labels, endpoints, phase and physical routes retained. Source excerpts excluded by compiler and covered by tests. |
| Bundled Codex skill-creator `quick_validate.py` | `Skill is valid!` |
| Agent metadata | YAML parsed; display description length and explicit skill mention checked. |
| Documentation | Relative Markdown link targets existed in the package. |
| Source linkage | Every fixture excerpt occurred verbatim in its `method.md`. Method dependencies and training/inference distinctions compared with the supplied fictional text. |
| Iterative SVG | All node/zone/connection IDs present; visible strings exactly equal the label whitelist. Rasterized locally with resvg-py and inspected at 1400 × 700: return arrow, initial-state path, fixed-observation path and final-state exit present, with legible labels. |

`PyYAML` and `resvg-py` were used only for local packaging/preview checks; they are not runtime dependencies of `schema_tool.py`. The optional [CI template](ci/github-actions.example.yml) targets Python 3.10, 3.12 and 3.14; it has not run as GitHub Actions. The publishing token lacked `workflow` scope, so this release ships the configuration as an example rather than enabling a workflow or expanding credential permissions.

No Nano-Banana Pro or other image-model run was performed. No independent agent evaluation, production paper, numerical experiment, publication-size typography check or image-quality benchmark was run. A structurally valid schema can still misrepresent a method; final source comparison and rendered-image inspection remain necessary.
