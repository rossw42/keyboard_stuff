# Audit: `kle_to_ergogen\`

> Agent B audit — compiled 2026-07-07. Static review only; no scripts were run.

## Overview

A standalone **Python** KLE JSON → Ergogen YAML converter, approximately v1.0 maturity. Clean 3-layer architecture: parser → data model → YAML generator. Only external dependency is **PyYAML**. No `requirements.txt` and no README — the only documentation is a design doc in `docs/`.

## File/Folder Structure

```
kle_to_ergogen/
├── cli.py                                  (342 lines — argparse CLI entry point)
├── package.json                            (npm manifest; 1 dep: dxf-viewer — oddity, see notes)
├── package-lock.json
├── data_models/
│   ├── __init__.py                         (exports ErgogenPoint, PointsCollection)
│   └── ergogen_point.py                    (370 lines — data model + naming strategies)
├── docs/
│   └── coordinate_transformation_plan.md   (203 lines — design doc)
├── example_kle/
│   └── macropad-with-3-encoders.json       (KLE sample: macropad w/ 3 encoders, OLED)
├── generators/
│   ├── __init__.py                         (exports ErgogenYAMLGenerator)
│   └── ergogen_yaml_generator.py           (592 lines — YAML output)
└── output/                                 (Ergogen BUILD ARTIFACTS — not produced by these scripts)
    ├── cases/   case_bottom.jscad, case_top.jscad
    ├── outlines/ case_outline.dxf, numpad.dxf, pcb_outline.dxf, plate.dxf, switchplate.dxf
    └── pcbs/    keyboard_numpad.kicad_pcb
```

## Component Notes

### `cli.py`
- Polished argparse CLI with a notably good flag surface: `--validate-only`, `--stats`, `--section-only`, plus output precision and indent controls.
- Input: KLE JSON file. Output: Ergogen YAML (points section or full config).

### `data_models/ergogen_point.py`
- Clean `ErgogenPoint` / `PointsCollection` model.
- **Pluggable key-naming strategies:** matrix (`r0c1`), sequential, and KLE-label — a distinctive feature not present in the sibling tools.

### `generators/ergogen_yaml_generator.py`
- Generates Ergogen YAML with **per-point provenance comments** tracing each point back to its KLE origin (unique feature).

### `docs/coordinate_transformation_plan.md`
- The best KLE ↔ Ergogen coordinate-mapping documentation in the entire collection. Valuable regardless of which codebase wins consolidation.

### Oddities
- `package.json`/`package-lock.json` with a single `dxf-viewer` dep in a Python project — likely leftover from an abandoned viewer experiment.
- `output/` contains real Ergogen artifacts (DXF/JSCAD/kicad_pcb) that this tool doesn't produce — evidence the pipeline was run end-to-end at least once (also confirmed by `__pycache__` bytecode), but these artifacts don't belong in the source tree.

## Quality Assessment

- **Status:** Working, near-finished tool. Was actually executed end-to-end at least once.
- **Weaknesses:** No README, no requirements.txt, no tests, stray npm files, checked-in build artifacts.

## Recommendations

| Component | Recommendation |
|---|---|
| `cli.py` flag design | **Merge** — best CLI surface of the three KLE tools |
| `data_models/ergogen_point.py` | **Merge** — naming strategies are unique and valuable |
| `generators/ergogen_yaml_generator.py` | **Merge** — provenance comments are unique |
| `docs/coordinate_transformation_plan.md` | **Keep** — carry into consolidated docs |
| `example_kle/` | **Keep** — good complex test input |
| `package.json` / `package-lock.json` | **Remove** — orphaned npm files |
| `output/` artifacts | **Remove** — build artifacts, not source |

## Distinctive vs. Siblings

- vs. `KLE_SCAD_Ergogen`: this tool's Ergogen output path actually works; KLE_SCAD_Ergogen's Ergogen output is broken. But KLE_SCAD_Ergogen has stabilizer/matrix/SCAD features this tool lacks.
- vs. `ergogen-toolkit`: no overlap — ergogen-toolkit is a VS Code extension with zero KLE functionality.