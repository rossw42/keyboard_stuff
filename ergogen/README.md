# Ergogen Toolkit

A consolidated collection of tools for designing custom keyboards with [Ergogen](https://ergogen.xyz) — from a Keyboard Layout Editor (KLE) sketch all the way to DXF outlines, 3D-printable cases, and KiCad PCBs, using a locally run Ergogen installation.

```
Design in KLE  →  Convert to Ergogen YAML  →  Run Ergogen locally  →
Preview outputs (DXF)  →  Cases (JSCAD→STL) + PCBs (KiCad + ergogen-footprints)  →
[future] QMK firmware scaffold
```

## Directory Guide

| Folder | What it is |
|---|---|
| [`kbforge/`](kbforge/) | **⭐ Unified Python CLI** — one KLE JSON in → Ergogen YAML (points+outlines+plate+PCB+cases), standalone OpenSCAD plate/case, hotswap_pcb_generator layout, Markdown build docs, and canonical layout JSON. Supersedes the two folders below. |
| [`kle-to-ergogen/`](kle-to-ergogen/) | *(superseded by kbforge)* Python CLI — converts KLE JSON to Ergogen YAML points |
| [`kle-to-scad/`](kle-to-scad/) | *(superseded by kbforge)* Node CLI — converts KLE JSON to OpenSCAD layouts for hotswap_pcb_generator |
| [`vscode-extension/`](vscode-extension/) | **VS Code extension** — Run Ergogen on the active YAML + built-in DXF viewer |
| [`working_samples/`](working_samples/) | Community Ergogen configs (Absolem, Samoklava, Kaly, …) used as reference patterns |
| [`docs/`](docs/) | Toolkit documentation — start with [`docs/ERGOGEN_REFERENCE.md`](docs/ERGOGEN_REFERENCE.md) |
| [`mounting_styles/`](mounting_styles/) | Deferred research on keyboard mounting styles (stretch goal) |
| [`audit/`](audit/) | Audit trail from the 2026-07 consolidation (kept for provenance) |
| [`archive/`](archive/) | Parked removals — superseded/broken/duplicate items; nothing deleted until sign-off |

Planning docs: [`TOOLKIT_PLAN.md`](TOOLKIT_PLAN.md) (roadmap) · [`MASTER_TASK_LIST.md`](MASTER_TASK_LIST.md) (task tracking)

## Quick Start

### 1. Install Ergogen locally
Requires [Node.js](https://nodejs.org):
```
npm i -g ergogen
```

### 2. Convert a KLE layout to everything (Ergogen YAML, SCAD, docs, ...)
Requires only Python 3 (no packages). Run from the repo root:
```
python -m kbforge kbforge/examples/kle/numpad.json -o my-keyboard/
```
(run from inside `kbforge/`, or add it to `PYTHONPATH`)

### 3. Run Ergogen (and get STL cases)
kbforge does this in the same run — add `--build`:
```
python -m kbforge kbforge/examples/kle/numpad.json -o my-keyboard/ --build
```
This runs Ergogen on the generated config and converts the case JSCAD models to STL. Outputs land in `my-keyboard/ergogen/`: `outlines/` (DXF), `cases/` (JSCAD + STL), `pcbs/` (KiCad).

### 4. Or use the VS Code extension
Install the extension from [`vscode-extension/`](vscode-extension/) for one-click **Run Ergogen** and an in-editor **DXF viewer**.

## Documentation

- [`docs/ERGOGEN_REFERENCE.md`](docs/ERGOGEN_REFERENCE.md) — condensed reference for the entire Ergogen config format (points, outlines, cases, PCBs, units, preprocessing, CLI)
- [`docs/ergogen-lessons-learned.md`](docs/ergogen-lessons-learned.md) — practical lessons from real usage
- [`docs/ergogen_design_prompt.md`](docs/ergogen_design_prompt.md) — methodology for writing working configs
- [`docs/coordinate_transformation_plan.md`](docs/coordinate_transformation_plan.md) — KLE ↔ Ergogen coordinate mapping
- [`docs/design-math/`](docs/design-math/) — column-stagger math research and parametric config examples
- [`docs/qmk/`](docs/qmk/) — design docs for a future Ergogen → QMK converter
- [`docs/research/`](docs/research/) — Ergogen ecosystem research and repo survey (Oct 2025 snapshot)

## About `archive/`

During the 2026-07 audit, broken code, duplicates, build artifacts, and an unimplemented QMK converter were moved to [`archive/`](archive/) rather than deleted. See [`archive/README.md`](archive/README.md) and the [`audit/`](audit/) reports for the reasoning behind each item.