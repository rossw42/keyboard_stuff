# kbforge

**One KLE layout in → everything you need to build the keyboard out.**

`kbforge` consolidates the former `kle-to-ergogen` (Python) and
`kle-to-scad` (Node) tools into a single, dependency-free Python package.
It parses a [Keyboard Layout Editor](http://www.keyboard-layout-editor.com/)
JSON file **once** into a shared layout model, then generates every output
from that same model — so positions, rotations, matrix assignments and
stabilizers always agree across formats.

```
Step 1 — generate (review/edit the YAML before building)
                       ┌──> <name>.ergogen.yaml  (Ergogen v4 config — the file you review/edit)
KLE JSON ──> Layout ───┼──> <name>.md            (build docs: matrix, stabilizers, BOM, instructions)
                       └──> <name>.layout.json   (canonical model for future tooling, e.g. QMK)

Step 2 — build (pass the reviewed YAML back to kbforge)
<name>.ergogen.yaml ──Ergogen──> ergogen/outlines/*.dxf,
                                 ergogen/pcbs/*.kicad_pcb,
                                 ergogen/cases/*.jscad + *.stl

Optional extra formats (-f scad stl hotswap) — independent of Ergogen
                       ┌──> <name>.scad          (standalone OpenSCAD plate & case)
              Layout ──┼──> <name>.plate.stl / .bottom.stl / .walls.stl  (rendered via OpenSCAD)
                       └──> <name>.hotswap.scad  ──hotswap_pcb_generator──> printable hotswap PCB/case
```

## Why start from KLE?

KLE JSON is the simplest widely-used way to describe a keyboard: draw your
layout in the browser, download the JSON, done. It captures positions, key
sizes, rotation, and labels — everything needed to derive plates, cases,
PCBs and documentation. More expressive formats (Ergogen YAML itself) are
*outputs* of this pipeline, which you can then hand-tune.

## Requirements

* **Python 3.9+** — no packages required (stdlib only)
* Optional, for downstream artifacts:
  * **Node.js** — for the build step: runs Ergogen (`ergogen` on PATH or
    `npx ergogen`) for DXF outlines, the KiCad PCB and JSCAD cases, and
    `npx @jscad/cli@1` to render those case models to STL
  * **OpenSCAD** — used for the *standalone* `stl` format (auto-detected on
    PATH, via `OPENSCAD_PATH`, or in common install locations such as
    `C:\Program Files\OpenSCAD (Nightly)`); if not found, STL output is
    skipped with a warning and everything else still generates
  * **[hotswap_pcb_generator](https://github.com/50an6xy06r6n/hotswap_pcb_generator)** — for the `.hotswap.scad` layout file

## Quick start

```powershell
cd kbforge

# Step 1 — generate the Ergogen config, docs and layout JSON:
python -m kbforge examples\kle\numpad.json -o out\numpad

# ... review/edit out\numpad\numpad_example.ergogen.yaml ...

# Step 2 — run Ergogen on the reviewed config (DXF, KiCad PCB, JSCAD cases)
# and render the case STLs from those very models:
python -m kbforge out\numpad\numpad_example.ergogen.yaml -o out\numpad
```

The build step stages the config as `out\numpad\.ergogen-build\config.yaml`
(cloning the ceoloide footprints alongside it when the PCB needs them — or
copying from `--footprints`/`ERGOGEN_FOOTPRINTS` if you have a local clone),
runs Ergogen, and converts every `cases/*.jscad` to STL with
`npx @jscad/cli@1`. Output under `out\numpad\ergogen\`:

| File | What it is |
|---|---|
| `outlines/plate.dxf` | switch plate (14×14 mm MX cutouts) for laser/CNC |
| `outlines/board.dxf` | board outline |
| `outlines/pcb_outline.dxf` | PCB edge cuts |
| `pcbs/<name>.kicad_pcb` | KiCad PCB with hotswap MX switches + diodes, matrix pre-netted |
| `cases/case_bottom.jscad` + `.stl` | case bottom tray (extruded) |
| `cases/case_walls.jscad` + `.stl` | wall ring |
| `cases/case_plate.jscad` + `.stl` | plate as a 3D solid |

The STLs come straight from the Ergogen `cases:` section, so they always
match the Ergogen outlines and PCB — edit the `.ergogen.yaml` (or the KLE)
and rerun the build step to regenerate everything consistently. (Ergogen
itself only emits `.jscad`; the STL conversion is the OpenJSCAD CLI, which
kbforge drives for you.)

Prefer to run Ergogen by hand? The generation step prints the manual
commands; the STL conversion is:

```powershell
npx --yes @jscad/cli@1 out\numpad\ergogen\cases\case_bottom.jscad -o case_bottom.stl
```

### Alternative: standalone OpenSCAD parts (no Ergogen needed)

The `scad`/`stl` formats build a self-contained OpenSCAD plate & case
model directly from the layout — independent of Ergogen, handy for quick
prints or Customizer tweaking:

```powershell
python -m kbforge examples\kle\numpad.json -o out\numpad -f scad stl
```

| File | What it is |
|---|---|
| `<name>.plate.stl` | switch plate, printable |
| `<name>.bottom.stl` | case bottom tray (floor + walls) |
| `<name>.walls.stl` | wall ring only (for a sandwich/stacked case) |

Pick different parts with `--stl-parts` (e.g. `--stl-parts plate all`) or
point at a specific executable with `--openscad "C:\path\to\openscad.exe"`.
You can still render manually if you prefer:

```powershell
openscad -o plate.stl  -D "part=""plate"""  out\numpad\numpad_example.scad
openscad -o bottom.stl -D "part=""bottom""" out\numpad\numpad_example.scad
```

## CLI reference

```
python -m kbforge <input.json | config.ergogen.yaml> [options]

  A .json input generates the layout files (Ergogen config, docs, JSON).
  A .yaml/.yml input runs the Ergogen build on that config instead.

  -o, --out-dir DIR     Output directory (default: alongside the input)
  -n, --name NAME       Base name for outputs (default: KLE metadata name
                        or the input filename)
  -f, --formats FMT...  Any of: ergogen scad stl hotswap docs json, or "all"
                        (default: ergogen docs json)
  -u, --unit MM         Key unit size in mm (default: 19.05; use 19 for u,
                        18/17 for choc — see Ergogen units docs)
  -b, --build           (deprecated) The build is now a separate step: pass
                        the generated .ergogen.yaml as the input to run
                        Ergogen on it and render the case .jscad models to
                        STL (needs Node.js; uses `ergogen` or `npx ergogen`
                        + `npx @jscad/cli@1`)
  --footprints DIR      Local clone of ceoloide/ergogen-footprints to copy
                        into the build (default: ERGOGEN_FOOTPRINTS env var,
                        else cloned from GitHub on first build)
  --openscad EXE        Path to the OpenSCAD executable for the stl format
                        (default: auto-detect via PATH, OPENSCAD_PATH env var,
                        or common install locations)
  --stl-parts PART...   Case parts to render as STL: plate bottom walls all
                        (default: plate bottom walls)
  -q, --quiet           Suppress the summary
  --version
```

Examples:

```powershell
# Step 1: generate config + docs + JSON (default formats)
python -m kbforge board.json -o out

# Step 2: after reviewing/editing the YAML, run the Ergogen build + case STLs
python -m kbforge out\board.ergogen.yaml -o out

# Only the Ergogen config and docs
python -m kbforge board.json -f ergogen docs

# Standalone OpenSCAD 3D parts (no Ergogen)
python -m kbforge board.json -f scad stl

# Every format at once
python -m kbforge board.json -f all

# Choc spacing
python -m kbforge board.json -u 18
```

## Output formats in detail

### 1. `<name>.ergogen.yaml` — Ergogen v4 config
A complete config with:
* **points** — one zone per key, positioned with `kx`/`ky` unit expressions
  and centered on the origin. Each key carries `column_net`/`row_net`
  (position-derived matrix), size tags, and stabilizer tags.
* **outlines** — `board` (filleted union of key footprints), `plate`
  (board − 14×14 switch cutouts), `pcb_outline`, plus internal helpers.
* **pcbs** — KiCad 8 PCB scaffold (`template: kicad8`) using the
  [ceoloide/ergogen-footprints](https://github.com/ceoloide/ergogen-footprints)
  library: `ceoloide/switch_mx` (hotswap) and `ceoloide/diode_tht_sod123`
  wired `{{column_net}} → {{colrow}} → {{row_net}}`. Add a controller
  footprint (e.g. `what: ceoloide/mcu_nice_nano`) by hand and map nets.
  Pass `options={"footprint_lib": "builtin"}` to the generator to use
  Ergogen's bundled `mx`/`diode` footprints instead (no external files).

  Every position and size in the config is expressed with `kx`/`ky` unit
  math (`shift: [mid_x - 1.5kx, mid_y + 2ky]`, `width: 2kx`) instead of
  hard-coded mm, so changing `kx`/`ky` in the `units:` section (e.g. 18/17
  for choc spacing) rescales the whole board.

  The `mid_x`/`mid_y` units center the board on the KiCad sheet: Ergogen
  maps points 1:1 to KiCad coordinates with no offset, so without this the
  PCB lands at the sheet's top-left corner. Ergogen's KiCad templates use
  A3 paper (420×297 mm), so `mid_x: 210` / `mid_y: -148.5` (ergogen is
  y-up). Disable with `options={"kicad_center": False}` to keep the layout
  centered on the origin instead.
* **cases** — `case_bottom`, `case_walls`, `case_plate` extrusions.

The YAML is deterministic (stable ordering) so regenerated configs diff
cleanly in git. It is intended as a *starting point* — edit freely.

### 2. `<name>.md` — build documentation
Summary stats, position-derived wiring matrix table, stabilizer list with
Cherry stem spacing, bill of materials, and per-artifact build commands.

### 3. `<name>.layout.json` — canonical model
A stable JSON serialization of the parsed layout (positions in units *and*
mm, matrix, stabilizers, bounds). Intended for future tools (QMK keymap
scaffolding, visualizers) so they never need to re-parse KLE.

### 4. `<name>.scad` — standalone OpenSCAD plate & case (`-f scad`)
No libraries needed. Customizer-friendly parameters (plate thickness,
margin, wall, case height, cutout size). `part` selects `plate`, `bottom`,
`walls`, or `all` (assembled preview). Handles rotated keys, any key size,
and cuts Cherry plate-mount stabilizer slots at correct spacing.

### 5. `<name>.plate.stl` / `<name>.bottom.stl` / `<name>.walls.stl` — printable STLs (`-f stl`)
Rendered headlessly from the standalone `.scad` model by invoking the
OpenSCAD CLI (`openscad -o part.stl -D part="plate" model.scad`), one file
per case part. Requesting `stl` implies generating the `.scad` file too.
If OpenSCAD can't be found the STL step is skipped with a warning so the
rest of the pipeline still succeeds.

### 6. `<name>.hotswap.scad` — hotswap_pcb_generator layout (`-f hotswap`)
The exact data format the old `kle-to-scad` tool emitted
(`base_switch_layout`, `base_stab_layout`, …). Use with
hotswap_pcb_generator's own SCAD code to produce printable hotswap PCBs,
plates and cases.

## Package layout

```
kbforge/
├── README.md
├── kbforge/
│   ├── __init__.py         public API (Layout, Key, parse_kle_file, ...)
│   ├── __main__.py         python -m kbforge
│   ├── cli.py              argument parsing + orchestration
│   ├── kle_parser.py       faithful kle-serial port (rotation clusters,
│   │                       decals, secondary rects, persistent props)
│   ├── layout.py           Layout/Key model, matrix assignment, bounds
│   ├── stabilizers.py      Cherry stabilizer detection + spacing table
│   ├── yaml_emit.py        deterministic YAML emitter (no PyYAML needed)
│   └── generators/
│       ├── ergogen.py      Ergogen v4 config (points/outlines/pcbs/cases)
│       ├── ergogen_build.py  build step: runs Ergogen + renders case STLs
│       │                     via `npx @jscad/cli@1`
│       ├── scad.py         standalone SCAD + hotswap_pcb_generator layout
│       ├── stl.py          STL rendering via the OpenSCAD CLI
│       ├── docs.py         Markdown build docs
│       └── json_out.py     canonical layout JSON
└── examples/
    ├── kle/                input KLE JSON files (moved from the old tools)
    ├── generated/          pipeline outputs for each example (committed as
    │                       reference; each contains ergogen-output/ built
    │                       with Ergogen 4.1.0)
    └── legacy-outputs/     outputs produced by the old tools, kept for
                            comparison (macropad_2x2.yaml, numpad.yaml,
                            test_40percent.scad)
```

## Python API

```python
from kbforge import parse_kle_file
from kbforge.generators import ergogen, ergogen_build, scad, stl, docs, json_out

layout = parse_kle_file("board.json")

layout.stats()                       # counts, matrix size, physical size
layout.assign_matrix()               # rows of keys, also sets key.matrix_*
layout.bounds_mm()                   # rotation-aware bounding box

ergogen.generate_ergogen_yaml(layout)            # str
ergogen.build_ergogen_config(layout)             # dict, if you want to tweak
scad.generate_scad(layout, {"wall": 4.0})        # str, options override defaults
scad.generate_hotswap_layout(layout)             # str
docs.generate_docs(layout)                       # str (Markdown)
json_out.generate_layout_json(layout)            # str (JSON)

# Ergogen build + case STLs (needs Node.js; equivalent of the CLI build step)
from pathlib import Path
ergogen_build.build(Path("out/board.ergogen.yaml"), Path("out"))  # list[Path]

# Standalone-SCAD STL rendering (needs the .scad on disk + OpenSCAD installed)
stl.render_stls(Path("out/board.scad"), Path("out"), "board")   # list[Path]
stl.render_stls(..., parts=["plate"], openscad=r"C:\path\openscad.exe")
```

Generator options (pass a dict as the second argument):

| Generator | Option | Default | Meaning |
|---|---|---|---|
| ergogen | `fillet` | 2.0 | board corner fillet (mm) |
| ergogen | `plate_expand` / `pcb_expand` | 0.0 | extra margin (mm) |
| ergogen | `wall` | 3.0 | case wall thickness (mm) |
| ergogen | `bottom_height` / `wall_height` / `plate_height` | 3 / 13 / 1.6 | case extrusions (mm) |
| ergogen | `footprint_lib` | `ceoloide` | `ceoloide` (ergogen-footprints, KiCad 8, needs footprints/ceoloide folder) or `builtin` (Ergogen's bundled mx/diode) |
| ergogen | `kicad_center` | `True` | center the board on the KiCad sheet via `mid_x`/`mid_y` units |
| ergogen | `sheet_center_x` / `sheet_center_y` | 210 / 148.5 | KiCad sheet center in mm (A3 default, matching Ergogen's templates) |
| scad | `plate_thickness` | 1.6 | plate (mm) |
| scad | `plate_margin` | 3.0 | margin around keys (mm) |
| scad | `switch_cutout` | 14.0 | MX cutout (mm) |
| scad | `corner_radius` / `wall` / `bottom_thickness` / `case_height` | 3 / 3 / 3 / 13 | case geometry (mm) |

## Coordinate conventions (important when editing generators)

| Space | +y | Rotation | Origin |
|---|---|---|---|
| KLE | down | clockwise, around (`rx`,`ry`) | top-left of layout |
| Ergogen | **up** | **counter-clockwise** | layout center (we center it) |
| SCAD | up | counter-clockwise | KLE origin (y negated) |

The generators negate `y` and rotation when leaving KLE space. Key positions
are always physical *centers* (computed rotation-cluster-aware in
`Key.center_u()`), except the hotswap layout which uses KLE top-left corners
in key units, as hotswap_pcb_generator expects.

## What was consolidated (vs. the old tools)

| Capability | kle-to-ergogen (old) | kle-to-scad (old) | kbforge |
|---|---|---|---|
| KLE parsing | partial (missed rotation clusters, decals, h-reset) | via `@ijprest/kle-serial` (Node) | full kle-serial port, pure Python |
| Matrix assignment | ported copy | original | single shared implementation |
| Stabilizer table | ported copy | original | single shared implementation |
| Ergogen output | points only, no outlines/pcb/case | removed (was broken) | full config: points+outlines+plate+pcb+cases, verified against Ergogen 4.1.0 |
| SCAD output | none | hotswap layout only | hotswap layout **and** standalone plate/case model |
| Docs output | none | none | Markdown build docs |
| Runtime deps | PyYAML | Node + commander + kle-serial | none (stdlib) |

The old folders remain in place for reference; their example files were
moved here to `examples/`.

## Known limitations / future work

* PCB scaffold has no controller placed — add a `promicro`/`nice_nano`
  footprint and pin mapping in the generated YAML (see the commented note
  in the `pcbs` section).
* ISO-Enter secondary rectangles (`x2/w2/h2`) are parsed and stored but the
  plate cutout is the standard 14×14 at the switch center (correct for the
  switch; the cap overhang doesn't need plate accommodation).
* Encoders/OLEDs are not inferred from KLE (KLE can't express them);
  hand-add them in the Ergogen YAML (see
  `working_samples/uncategorized/ai_generated_numpad.yaml` for patterns).
* QMK scaffolding from `<name>.layout.json` is the planned next milestone
  (see `../TOOLKIT_PLAN.md` M5).