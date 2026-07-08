# Switch Converter × Ergogen Integration — Feasibility & Recommended Approach

> **STATUS: IMPLEMENTED (2026-07-08).** All three layers below are now built
> into kbforge (`D:\GitHub\keyboard_stuff\ergogen\kbforge`) and verified
> end-to-end (Ergogen 4.x build + OpenSCAD STL renders). See
> **"How to use the pipeline"** at the bottom of this document, and the
> "Switch-converter pipeline" section of the kbforge README.
> Pre-change backups of every modified kbforge file are in
> `kbforge/backup/pre_converter_2026-07-08/`.

Research findings from analyzing three sources:
- `D:\GitHub\keyboard_stuff\projects\switch_converter` (the PG1350→PG1425 adapter project)
- `D:\GitHub\keyboard_stuff\ergogen\kbforge` (our Ergogen toolkit)
- `D:\Keyboard Workspace\ergogen-docs-md` (local Ergogen docs)

---

## TL;DR — Is it possible?

**Yes, but not as a single Ergogen artifact.** Ergogen is fundamentally a 2D/2.5D tool
(points → outlines → extruded cases), so it **cannot** reproduce the adapter's full 3D
geometry (clip windows, floor pocket, bezel walls). What Ergogen *can* do is everything
2D about the integration, and it can hand off key positions to OpenSCAD for the 3D part.

The recommended path is a **hybrid pipeline**: Ergogen owns the plate/PCB 2D geometry,
OpenSCAD owns the adapter 3D geometry, and kbforge's existing `layout.json` /
per-key-tag machinery bridges the two.

---

## Key facts driving the design

### The adapter (from `OpenSCAD/pg1350_to_pg1425_adapter.scad`, v3)
- 15.00 × 15.00 mm body (matches the Choc flange), 5.00 mm tall (2.80 floor + 2.20 wall)
- **The adapter IS the plate** for the Choc switch — the top 1.2 mm of the bezel walls
  form an "effective plate" with 6.0 mm clip windows; the Choc snaps into the adapter,
  not into an external plate
- It registers to a **PG1425 (Choc X) PCB footprint**, which is a plateless/edge-mount
  standard — no conventional plate exists in this stack at all

### Ergogen capabilities (from `ergogen-docs-md/outlines`, `pcbs`, `cases`)
- **Outlines**: `rectangle` / `circle` / `poly` / `outline` parts placed at filtered
  points, with `add` / `subtract` / `intersect` booleans. Per-key customization works
  via tag filters in `where` — different keys can get different cutout shapes
- **PCBs**: arbitrary custom `.js` footprints can be loaded from a local footprints
  folder and placed at any filtered set of points
- **Cases**: extrusion of outlines only (2.5D). No arbitrary 3D import, no STL embed —
  this is the hard limitation
- Outlines export as DXF, which OpenSCAD can import

### kbforge extension points (from `kbforge/generators/ergogen.py`)
- `_build_outlines()` emits the plate as `board − _switch_cutouts`, where the cutout is
  a rectangle sized by the named unit `sw_cutout` (hardcoded `SWITCH_CUTOUT = 14.0`,
  one global value — no per-key sizes today)
- `_build_zones()` already emits per-key tags (`["key", tag]`) — the natural hook for a
  `converter` tag
- `ergogen_build.py` stages custom footprints next to the config before running the
  local `ergogen` CLI
- `<name>.layout.json` preserves every key's x/y/rotation — usable to drive OpenSCAD

---

## Recommended approach (three layers, in build order)

### Layer 1 — Plate cutouts in Ergogen (easy, do first)
Treat converter positions as a distinct key class:

1. Add a per-key attribute in kbforge (e.g. `converter: true` in the KLE metadata or a
   CLI flag) that emits a `converter` tag on those points in `_build_zones()`.
2. In `_build_outlines()`, emit two cutout parts instead of one:

```yaml
outlines:
  _switch_cutouts:
    - what: rectangle
      where: [ [key, -converter] ]   # normal keys
      size: [sw_cutout, sw_cutout]   # 14.0 (MX) or 13.8 (Choc)
    - what: rectangle
      where: [ [key, converter] ]    # converter positions
      size: [15.2, 15.2]             # adapter body + clearance
      corner: 0.5
  plate:
    - what: outline
      name: board
    - what: outline
      name: _switch_cutouts
      operation: subtract
```

This gives a plate where the adapter body drops *through* (or seats *into*, see Layer 3)
the plate at converter positions. Also parameterize `SWITCH_CUTOUT` (13.8 Choc option)
while in there — it's currently hardcoded.

### Layer 2 — Custom PG1425 footprint for the PCB (moderate)
There is no PG1425 footprint in ceoloide/ergogen-footprints. Write a custom
`switch_pg1425.js` ergogen footprint containing the Choc X pad/cutout geometry
(edge-mount notches, contact pads) and stage it via kbforge's existing footprint-staging
path in `ergogen_build.py`. Place it with `where: [ [key, converter] ]` in the `pcbs`
section. Result: one `kicad_pcb` with normal hotswap footprints on regular keys and
PG1425 footprints at converter positions.

### Layer 3 — Adapter array / integrated converter plate in OpenSCAD (the interesting one)
Ergogen cannot make the 3D adapter, but kbforge can drive OpenSCAD with ergogen-accurate
positions. Two variants, both fed from `<name>.layout.json` (or the ergogen `points`
output):

- **Variant A — panelized adapter grid:** a small generator that instantiates
  `pg1350_to_pg1425_adapter.scad` at each converter key position (x, y, rotation) with
  sprues/tabs between them for printing. One print = all adapters for the board,
  correctly spaced for assembly.
- **Variant B — integrated "converter plate":** since the adapter already *is* a 1.2 mm
  plate locally, union all adapter bodies with an extrusion of the ergogen `board`
  outline (imported as DXF) at matching Z. Result: a single 3D-printed plate with the
  bezels/clip windows built in — no individual adapters to place, and the plate itself
  provides switch retention. This is the cleanest end state for an all-converter board.

kbforge already has an OpenSCAD/STL output path (`-f scad stl`), so this slots into the
existing generator architecture rather than requiring new infrastructure.

---

## What NOT to attempt
- **Don't** try to model the adapter in Ergogen's `cases` section — extrusion-only, no
  clip windows or pockets possible.
- **Don't** rely on ergogen's case output for the integrated plate — do the 3D union in
  OpenSCAD using the exported DXF outline instead.

## Suggested implementation order
1. Parameterize `SWITCH_CUTOUT` + add `converter` key tag support in kbforge ✅
2. Emit the dual-cutout `_switch_cutouts` outline (Layer 1) ✅
3. Prototype Variant A (panelized adapter grid) from `layout.json` ✅
4. Write `switch_pg1425.js` footprint (Layer 2) ✅
5. Prototype Variant B (integrated converter plate) ✅ (implemented in
   OpenSCAD directly from the shared Layout model rather than DXF import —
   simpler and always consistent with the Ergogen positions)

---

# How to use the pipeline (implemented)

All commands run from `D:\GitHub\keyboard_stuff\ergogen\kbforge`.

## 1. Generate — mark converter keys

```powershell
# Every key takes a converter (all-converter board):
python -m kbforge board.json -o out -f ergogen docs json converter --converter-keys all

# Only specific keys — matrix refs (rXcY) and/or key labels:
python -m kbforge board.json -o out -f ergogen converter --converter-keys r0c0 r0c1 Enter

# Choc-sized cutouts for the remaining normal keys:
python -m kbforge board.json -o out -f ergogen converter --converter-keys r0c0 --switch-cutout 13.8
```

What this produces:

| File | Converter content |
|---|---|
| `<name>.ergogen.yaml` | converter points tagged `converter`; `_switch_cutouts` emits a 15.2 mm rounded opening (`conv_cutout` unit) at converter keys and `sw_cutout` at the rest; `pcbs` places `switch_pg1425` at converter keys and the normal hotswap footprint elsewhere |
| `<name>.converter.scad` | standalone OpenSCAD with the v3 adapter geometry at every converter position (`part=` selects `adapter` / `panel` / `plate`) |
| `<name>.layout.json` | each converter key carries `"converter": true` |

## 2. Build — run Ergogen (custom footprint staged automatically)

```powershell
# Optional: point at the local footprints clone to skip the GitHub clone
$env:ERGOGEN_FOOTPRINTS = "D:\GitHub2\ergogen-footprints"

python -m kbforge out\<name>.ergogen.yaml -o out
```

`ergogen_build.py` copies `kbforge/footprints/switch_pg1425.js` into
`.ergogen-build/footprints/` whenever the config references it, then runs
Ergogen. Outputs: `out\ergogen\outlines\plate.dxf` (dual cutouts),
`out\ergogen\pcbs\<name>.kicad_pcb` (PG1425 footprints at converter keys),
plus the usual case jscad/STL files.

## 3. Print — render the converter parts

```powershell
# Variant A: sprued panel of all adapters at true board spacing
openscad -o out\adapters.stl -D "part=""panel""" out\<name>.converter.scad

# Variant B: integrated converter plate (one print, built-in retention)
openscad -o out\plate.stl -D "part=""plate""" out\<name>.converter.scad

# Single adapter for fit testing
openscad -o out\adapter.stl -D "part=""adapter""" out\<name>.converter.scad
```

## Assembly (per converter position)
1. Place the adapter on the PG1425 PCB footprint — its two printed pins
   drop into the 1.3 mm non-plated alignment holes.
2. Route the Choc pins / stamped contacts through the adapter's slots into
   the two plated pin holes; solder.
3. Snap the PG1350 (Choc V1) switch into the adapter pocket — the clips
   engage the adapter's clip windows exactly like a 1.2 mm plate.

## Implementation map

| Piece | File |
|---|---|
| `converter` flag + `mark_converters()` + stats | `kbforge/kbforge/layout.py` |
| converter tags, dual cutouts, `conv_cutout` unit, `switch_cutout` option, PG1425 footprint placement | `kbforge/kbforge/generators/ergogen.py` |
| PG1425 Ergogen footprint (KiCad 8) | `kbforge/kbforge/footprints/switch_pg1425.js` |
| custom footprint staging in the build | `kbforge/kbforge/generators/ergogen_build.py` |
| adapter panel / integrated plate SCAD generator | `kbforge/kbforge/generators/converter_scad.py` |
| `--converter-keys`, `--switch-cutout`, `-f converter` | `kbforge/kbforge/cli.py` |

The `switch_pg1425.js` footprint geometry was translated from the verified
`Kailh-PG1425-X-Switch.kicad_mod` in this folder (re-centered on the switch
center: the module origin sat at (-3.4, 2.9) relative to the center). The
adapter geometry in `converter_scad.py` is inlined from
`OpenSCAD/pg1350_to_pg1425_adapter.scad` (v3) — **keep them in sync** if the
adapter design changes.

## Verified
* `numpad.json --converter-keys all` → YAML with 17 converter tags,
  `conv_cutout: 15.2`, PG1425 footprints on every key
* `numpad.json --converter-keys r0c0 r0c1 enter` → mixed board: 3 converter
  + 14 MX footprints in the built `.kicad_pcb`; plate DXF with both cutout
  sizes; full Ergogen 4.x build + case STLs pass
* `.converter.scad` renders all three parts in OpenSCAD:
  `adapter` = 15×15 mm at origin, `panel` = adapters at the 3 board
  positions, `plate` = full-board slab fused with adapters
