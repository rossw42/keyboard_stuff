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
| [`kle-to-ergogen/`](kle-to-ergogen/) | **Python CLI** — converts KLE JSON to Ergogen YAML (points section or full config) |
| [`kle-to-scad/`](kle-to-scad/) | **Node CLI** — converts KLE JSON to OpenSCAD layouts for hotswap_pcb_generator (with stabilizer support) |
| [`vscode-extension/`](vscode-extension/) | **VS Code extension** — Run Ergogen on the active YAML + built-in DXF viewer |
| [`scripts/`](scripts/) | Canonical command-line runner: `run-ergogen.bat` → runs Ergogen + converts JSCAD cases to STL |
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

### 2. Convert a KLE layout to Ergogen YAML
Requires Python 3 + PyYAML (`pip install -r kle-to-ergogen/requirements.txt`). Run from the repo root:
```
python kle-to-ergogen/cli.py kle-to-ergogen/examples/macropad-with-3-encoders.json -o my-keyboard.yaml
```

### 3. Run Ergogen (and get STL cases)
```
scripts\run-ergogen.bat my-keyboard.yaml
```
Outputs land in a folder named after the YAML file: `outlines/` (DXF), `cases/` (JSCAD + STL), `pcbs/` (KiCad).

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