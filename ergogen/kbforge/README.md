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

Optional extra formats (-f scad stl hotswap converter) — independent of Ergogen
                       ┌──> <name>.scad           (standalone OpenSCAD plate & case)
              Layout ──┼──> <name>.plate.stl / .bottom.stl / .walls.stl  (rendered via OpenSCAD)
                       ├──> <name>.hotswap.scad   ──hotswap_pcb_generator──> printable hotswap PCB/case
                       └──> <name>.converter.scad (PG1350->PG1425 switch-converter panel /
                                                   integrated converter plate, --converter-keys)
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
  -f, --formats FMT...  Any of: ergogen scad stl hotswap docs json converter,
                        or "all" (default: ergogen docs json)
  -u, --unit MM         Key unit size in mm (default: 19.05; use 19 for u,
                        18/17 for choc — see Ergogen units docs)
  --switch-cutout MM    Plate cutout for normal keys (default: 14.0 MX;
                        use 13.8 for Choc)
  --converter-keys SPEC...
                        Mark keys as PG1350->PG1425 switch-converter
                        positions: "all", matrix refs (r0c3), or key labels.
                        See "Switch-converter pipeline" below.
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

# Switch-converter board: every key takes a PG1350->PG1425 adapter
python -m kbforge board.json -o out -f ergogen docs json converter --converter-keys all
```

## Switch-converter pipeline (PG1350 → PG1425)

kbforge integrates the
[switch_converter project](../../projects/switch_converter/) — a 3D-printed
15×15×5 mm adapter that seats a Kailh Choc **PG1350** switch onto a Kailh
**PG1425 "Choc X"** PCB footprint (edge-mount, plateless). Design rationale:
`projects/switch_converter/ergogen_integration.md`.

Mark any subset of keys as converter positions and the whole pipeline
adapts:

```powershell
# 1. Generate — mark keys (all | matrix refs | labels), request the
#    converter SCAD alongside the usual outputs:
python -m kbforge board.json -o out -f ergogen docs json converter --converter-keys all
python -m kbforge board.json -o out -f ergogen converter --converter-keys r0c0 r0c1 Enter

# 2. Build the Ergogen outputs as usual (the custom PG1425 footprint is
#    staged automatically):
python -m kbforge out\board.ergogen.yaml -o out

# 3. Render the printable converter parts from the .converter.scad:
openscad -o out\adapters.stl -D "part=""panel"""  out\board.converter.scad
openscad -o out\plate.stl    -D "part=""plate"""  out\board.converter.scad
```

What each layer produces:

| Layer | Output | Converter behavior |
|---|---|---|
| **Plate (Ergogen)** | `ergogen/outlines/plate.dxf`, `cases/case_plate.*` | converter keys get a **15.2 mm rounded opening** (`conv_cutout` unit) the adapter body drops through — the adapter's own 1.2 mm bezel retains the switch; normal keys keep the `sw_cutout` opening (14.0 MX / `--switch-cutout 13.8` Choc) |
| **PCB (Ergogen)** | `ergogen/pcbs/<name>.kicad_pcb` | converter keys get the **`kbforge:switch_pg1425`** footprint (plated pin holes, alignment holes for the adapter's pins, center cutout — translated from the verified shikamiya KiCad footprint); normal keys keep the hotswap MX footprint; diodes/nets unchanged |
| **3D (OpenSCAD)** | `<name>.converter.scad` | three parts via `part=`: `adapter` (one, at origin), `panel` (all adapters at true board positions joined by snap-off sprues — print once, snap apart), `plate` (integrated converter plate: plate slab fused with the adapter bodies — one print, built-in switch retention) |

Notes:

* Points are tagged `converter` in the generated YAML, so you can hand-edit
  `where:` filters (`[key, converter]` / `[key, -converter]`) freely.
* The custom footprint lives at `kbforge/footprints/switch_pg1425.js` and is
  staged into `.ergogen-build/footprints/` automatically whenever the config
  references it.
* The adapter geometry in `<name>.converter.scad` is inlined from
  `projects/switch_converter/OpenSCAD/pg1350_to_pg1425_adapter.scad` (v3) —
  if that design changes, update `kbforge/generators/converter_scad.py` to
  match.
* The integrated `plate` part assumes an all-converter (or converter-major)
  board: the slab top sits at the adapter-stack height (5 mm above the PCB).
  Mixed boards should use the `panel` part plus the normal Ergogen plate.
* Ergogen itself can't produce the adapter's 3D features (pockets, clip
  windows) — it's a 2D/2.5D tool — which is why the 3D layer is OpenSCAD.

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

### 7. `<name>.converter.scad` — switch-converter parts (`-f converter`)
Standalone OpenSCAD model with the PG1350→PG1425 adapter geometry placed at
every `--converter-keys` position (ergogen-consistent x/y/rotation). `part`
selects `adapter`, `panel` (snap-off sprued grid), or `plate` (integrated
converter plate). See "Switch-converter pipeline" above.

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
│   ├── footprints/
│   │   └── switch_pg1425.js  custom Ergogen footprint: Kailh PG1425 "Choc X"
│   │                         (staged into builds that reference it)
│   └── generators/
│       ├── ergogen.py      Ergogen v4 config (points/outlines/pcbs/cases)
│       ├── ergogen_build.py  build step: runs Ergogen + renders case STLs
│       │                     via `npx @jscad/cli@1`
│       ├── scad.py         standalone SCAD + hotswap_pcb_generator layout
│       ├── converter_scad.py switch-converter panel / integrated plate SCAD
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
| ergogen | `switch_cutout` | 14.0 | plate cutout for normal keys (13.8 for Choc) |
| ergogen | `converter_cutout` / `converter_cutout_corner` | 15.2 / 0.5 | plate opening at converter keys (mm) |
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