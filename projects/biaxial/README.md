# BiAxial — Project Description

**Author:** Ross Warren
**Status:** V2 layout finalized (42 keys, twin rotated spaces); Ergogen project bootstrapped via kbforge — plate DXF, KiCad PCB (switches/diodes/MCU/reset/mount holes), case STLs, and BOM all generated from `ergogen/biaxial.ergogen.yaml`.

---

## What is BiAxial?

BiAxial is a 45-key (V1) column-splayed **monoblock** 40% keyboard. The core concept:

- **Ortholinear columns, splayed rotation** — each column is a straight vertical stack of 4 keys (no row stagger), rotated ("splayed") around a shared pivot line at y≈2.0443u. Columns fan outward from the center:
  - Left half: +2° / +4° / +6° / +6° / +6° / +6° (columns 0–5)
  - Right half: −6° / −6° / −6° / −6° / −4° / −2° (columns 7–11)
- **11 columns × 4 rows** = 44 alpha/mod keys, all 1u × 1u
- **1 Space key** — 1u wide × **1.25u tall** (rotated/vertical), unrotated (r=0), centered in the 2.25u gap between the two halves (matrix position 2,6)
- **Matrix:** 4 rows × 12 columns (column 6 is Space only)
- V1 includes a dedicated left pinky/modifier column (Esc / Tab / Caps / Shift)

The plate reuses the **"Omnibus Hull"** outline (a plate shape with compound-arc mounting tabs), targeting compatibility with the MiniVan/Omnibus case ecosystem.

> Note: an earlier working name for this design was **"Camber"** (visible in the KiCad build log metadata).

---

## Design Lineage: MiniVan / Omnibus

`minivan-omnibus-measurements.md` documents the dimensional targets sourced from the Trashman Wiki, 40s Wiki, and the SteamVan KiCad project:

- MiniVan PCB envelope: **242.89 mm × 76.20 mm** (12.75u × 4u at 19.05 mm/u), 3 mm corner radius, ~12 mm USB notch top-right
- Rev 2+ tray-mount pattern: **7× M2 screw holes** with exact coordinates (extracted from SteamVan); Rev 1 cases only align on 3 of 7
- Case interior: ~244–246 mm × ~78–80 mm, plus a survey of ~16 case variants
- The Omnibus is a drop-in MiniVan replacement PCB (ATmega32u4, USB-C, QMK/Vial) — reference for what a "compatible" PCB needs

`Omnibus_Hull.dxf` (project root) is the reference hull/plate outline.

---

## File Inventory

```
biaxial/
├── BiAxial_v1.json                  # Canonical V1 KLE layout (45 keys) — raw KLE JSON
├── BiAxial_v1_backup.json           # EMPTY (0 bytes) — failed save, can be deleted or refreshed
├── minivan-omnibus-measurements.md  # MiniVan/Omnibus dimensional reference (219 lines)
├── Omnibus_Hull.dxf                 # Reference hull plate outline
├── kle/
│   ├── biaxial_v1.kle.json          # V1: 45 keys (11 cols × 4 rows + Space)
│   └── biaxial_v2.kle.json          # V2: 41 keys (V1 minus Esc/Tab/Caps/Shift, re-centered)
├── scripts/
│   ├── generate_biaxial_kle.py      # Emits canonical V1 KLE (layout hardcoded)
│   ├── generate_biaxial_v2_kle.py   # Derives V2 from V1: drops pinky column, centers on Space
│   ├── generate_biaxial_dxf.py      # V1 switch plate DXF (MX cutouts + Omnibus Hull outline)
│   ├── generate_biaxial_jpg.py      # JPG preview render of the plate
│   └── generate_biaxial_stl.py      # 3D-printable plate STL
├── dxf/
│   ├── biaxial_v1_hull_plate_mx.dxf # Generated V1 plate (MX cutouts, hull outline)
│   └── biaxial_v1_hull_plate_mx.jpg # Preview render
├── stl/
│   └── biaxial_v1_hull_plate_mx.stl # Generated V1 plate STL
└── 7900e9a7-adb4-49fd-afe8-7e7bca7875c4/   # Auto-generated KiCad project (keyboard-tools/kbplacer output)
    ├── BiAxial/
    │   ├── BiAxial.kicad_pcb        # 45 SW + 45 diodes placed at splayed rotations, autorouted
    │   ├── BiAxial.kicad_sch        # Generated schematic (rows/cols matrix + per-key diodes)
    │   ├── BiAxial.kicad_pro/.prl
    │   ├── BiAxial.svg
    │   ├── fp-lib-table
    │   └── footprints/Switch_Keyboard_Cherry_MX.pretty/  # Stock Cherry MX PCB+Plate footprints (1u–7u, ISO, 90deg variants)
    └── logs/
        ├── build.log                # Generator log (layout parsed, nets added, autoroute trace)
        ├── front.svg / back.svg     # PCB renders
        └── schematic.svg
```

---

## Pipeline (how things are generated)

1. **`generate_biaxial_kle.py`** → `kle/biaxial_v1.kle.json` — the hand-tuned V1 layout is hardcoded here; each key is its own KLE row array (required for per-key rotation). This is the source of truth for geometry.
2. **`generate_biaxial_v2_kle.py`** → `kle/biaxial_v2.kle.json` — removes the 4 left-mod keys (Esc/Tab/Caps/Shift), transfers the +2° rotation to the backtick column, and shifts everything so Space sits at x=0 (centered).
3. **`generate_biaxial_dxf.py`** → `dxf/biaxial_v1_hull_plate_mx.dxf` — computes 14×14 mm MX cutouts at each splayed key position and wraps them in the Omnibus Hull outline.
4. **`generate_biaxial_jpg.py`** → preview image of the plate.
5. **`generate_biaxial_stl.py`** → 3D-printable plate.
6. **KLE → KiCad** — the V1 KLE (with `row,col` matrix labels in legend position 0) was fed through an automated KLE-to-PCB service (kbplacer-style, ran in `/tmp` on Linux), producing the `7900e9a7-…/BiAxial/` KiCad project.

---

## State of the KiCad PCB (prototype quality)

The auto-generated PCB is a starting point, not a finished board:

- 45 switches (SW1–SW45, Cherry MX PCB footprints; Space uses the 1.25u variant) + 45 diodes (D1–D45, placed on the back at a fixed offset)
- Nets: ROW0–ROW3, COL0–COL11, per-key diode nets
- Switch→diode routing succeeded for all keys, but the autorouter **failed to route between adjacent diodes whose footprints have different rotations** — the log shows many `Could not route pads when parent footprints not rotated the same` warnings at every splay-angle boundary (±2°/±4°/±6° transitions). Row/column routing is therefore incomplete.
- **No MCU, no USB, no mounting holes, no board outline matching the Omnibus Hull** — the schematic is matrix-only.

---

## Ergogen Project (`ergogen/`)

The V2 KLE was converted to an Ergogen v4 project using **kbforge** (`D:\GitHub\keyboard_stuff\ergogen\kbforge`). There are **two switch variants**, each a standalone config building into a named output dir:

| Variant | Config | Spacing | Cutout | Switch footprint | Output |
|---|---|---|---|---|---|
| MX | `biaxial_mx.ergogen.yaml` | 19.05 x 19.05 | 14.0 mm | `ceoloide/switch_mx` (hotswap) | `out_mx/` |
| Choc v1 | `biaxial_choc.ergogen.yaml` | 18 x 17 | 13.8 mm | `ceoloide/switch_choc_v1_v2` (hotswap, v1-only) | `out_choc/` |

The whole splayed layout is expressed in `kx`/`ky` units, so the Choc variant rescales all key positions automatically while the Omnibus Hull outline and MiniVan mounting holes stay at their absolute positions (giving the Choc plate extra margin inside the same hull).

```
# Build either variant (runs Ergogen + renders the plate STL):
python -m kbforge ergogen/biaxial_mx.ergogen.yaml   -o ergogen/out_mx   --footprints D:\GitHub2\ergogen-footprints
python -m kbforge ergogen/biaxial_choc.ergogen.yaml -o ergogen/out_choc --footprints D:\GitHub2\ergogen-footprints

# Regenerate from KLE if the layout changes:
python -m kbforge kle/biaxial_v2.kle.json -o ergogen -n biaxial -f ergogen docs json
```

Shared config structure (both variants):

- **outlines**: board = the EXACT Omnibus Hull outline (242.8875 x 76.2 mm body + four compound-arc mounting tab corners; 251.21 mm overall width incl. tabs) — arcs sampled into a 200-point ergogen polygon by `scripts/generate_hull_ergogen_polygon.py` since Ergogen can't import DXFs. `plate` = board minus switch cutouts minus 7 MiniVan Rev 2+ M2 holes
- **points**: 42 per-key zones with exact positions/rotations from the V2 KLE (splayed +/-2/4/6 clusters + twin rotated 1.25u spaces)
- **pcbs**: kicad8 template, hull edge cuts, ceoloide footprints — 42x switch (hotswap), 42x `diode_tht_sod123`, 1x `mcu_nice_nano` (Pro Micro-compatible, 10 col + 5 row nets pinned), 1x side reset switch, 7x NPTH mounting holes
- **cases**: `case_plate` extrusion only (walls/bottom removed — MiniVan/Omnibus-compatible cases are used instead)

Other files:

- `ergogen/biaxial.md` — docs + **BOM** (42 switches, 42 diodes, keycaps by size, controller) + wiring matrix table
- `ergogen/biaxial.layout.json` — normalized layout data
- `ergogen/out_mx|out_choc/ergogen/` — per-variant build outputs:
  - `outlines/plate.dxf` (hull outline w/ tabs + cutouts + holes; `plate.jpg` preview), `board.dxf`, `pcb_outline.dxf`
  - `pcbs/biaxial_mx.kicad_pcb` / `biaxial_choc.kicad_pcb` — open in KiCad 8, route, fabricate
  - `cases/case_plate.jscad` + rendered `case_plate.stl` (1.6 mm plate)
- `ergogen/out_*/.ergogen-build/` — staging dirs (config.yaml + footprints/ceoloide); regenerated each run

### Remaining cleanup / next steps

- [ ] Route the generated KiCad PCB (footprints placed + netted, no traces yet); consider `ceoloide/utility_router` for matrix pre-routing
- [ ] MCU placement/orientation review — currently top-center of the gap; USB egress vs the hull's top edge needs checking in KiCad
- [ ] Firmware next (QMK/Vial): matrix from `ergogen/biaxial.md` wiring table (5 rows x 10 cols)
- [ ] Clean up: delete or regenerate the empty `BiAxial_v1_backup.json`; `generate_biaxial_kle.py` output-name drift (`biaxial.kle.json` vs `biaxial_v1.kle.json`)

---

## Open Questions / Decisions to Make

- Is the auto-generated KiCad project (`7900e9a7-…`) worth iterating on, or will the real PCB be regenerated from Ergogen?
- Target controller and USB placement (Omnibus-style top-right? Pro Micro footprint? RP2040?)
- Case strategy: MiniVan/Omnibus case compatibility vs. custom case generated from the hull outline
- Space key: currently 1u × 1.25u vertical — confirm stab-free 1.25u 90° footprint is the intent