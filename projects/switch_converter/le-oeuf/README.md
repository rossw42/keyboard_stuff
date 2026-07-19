# Le Oeuf — PG1350→PG1425 Converter Plate

Integrated converter plate / adapter panel for the
[eggsworks le-oeuf](file:///D:/GitHub2/eggsworks/le-oeuf) — an Ergogen-generated
36-key split-monoblock keyboard whose PCB uses the **Kailh PG1425 (Choc X)**
footprint at every key. This plate puts the
[PG1350→PG1425 switch adapter](../OpenSCAD/pg1350_to_pg1425_adapter.scad) (v3.1)
at all 36 positions, so regular Kailh Choc PG1350 switches can be used on the
stock le-oeuf PCB.

## Files

| File | Description |
|---|---|
| `generate_converter_scad.py` | Generator: parses `le-oeuf.kicad_pcb` and emits the SCAD |
| `le-oeuf.converter.scad` | Generated OpenSCAD (parts: `adapter` / `panel` / `plate`) |
| `le-oeuf_plate.stl` | Integrated converter plate (default part) |
| `le-oeuf_panel.stl` | 36 loose adapters joined by snap-off sprues |
| `le-oeuf_plate_top.png`, `le-oeuf_plate_persp.png`, `le-oeuf_panel_top.png` | Render previews |

## How it works

`generate_converter_scad.py` reads the le-oeuf KiCad PCB directly (no
schematic needed):

1. **Switch positions** — extracts the `(at x y rot)` of all 36
   `le-oeuf:Kailh-PG1425-X-Switch` footprints (±7° split rotation preserved).
2. **Board outline** — chains the Edge.Cuts `gr_line`/`gr_arc` segments
   (arcs sampled at 1mm, degenerate zero-length arcs filtered) into a closed
   polygon, so the plate outline matches the actual egg-shaped PCB, including
   the center notch.
3. Converts KiCad y-down → OpenSCAD y-up and emits the SCAD in the proven
   kbforge converter format with the v3.1 adapter geometry inlined.

Regenerate after PCB changes:

```
python generate_converter_scad.py
```

## Parts (`part=` in the SCAD)

- **`plate`** (default, primary output) — one print: a **full-thickness slab
  (5.0mm — the same height as the switch converters)**, flush with the
  adapter tops and resting on the PCB, fused with all 36 adapter bodies.
  Built-in switch retention via the adapters' clip windows; relief voids
  behind each window (`clip_relief_depth`) keep the Choc clips flexible.
- **`panel`** — all 36 adapters at true board positions joined by snap-off
  sprues, if you prefer loose adapters.
- **`adapter`** — a single adapter at the origin for fit testing.

Plate parameters:

- `center_relief` (default **true**) — thins the middle bridge between the
  two key clusters from BELOW (auto-computed X span ≈ 123.3–154.4mm, 31mm
  wide), leaving `center_top_t` (default 1.5mm) of material on top. That
  gives **3.5mm of clearance** for components mounted on the PCB under the
  center section, while the top surface stays flush. Adjust
  `center_relief_x` / `center_top_t` in the customizer if the components
  need a different span or more headroom.
- `plate_edge_offset` grows/shrinks the PCB outline.
- `clip_relief_depth` sets the clip-flex relief behind each bezel window.
- `mcu_cutout` + `mcu_cutout_center/size` — full through-cutout if the
  partial center relief isn't enough. Elsewhere the slab underside sits ON
  the PCB, so any other tall top-side component also needs relief.

## Export commands

```powershell
& "D:\Program Files\OpenSCAD (Nightly)\openscad.exe" -o le-oeuf_plate.stl le-oeuf.converter.scad
& "D:\Program Files\OpenSCAD (Nightly)\openscad.exe" -o le-oeuf_panel.stl -D "part=`"panel`"" le-oeuf.converter.scad
```

## Print notes — how to handle the overhangs

Print the plate **as modeled (pockets up), flat on the bed, no supports**:

- **Bottom:** with `plate_pins = false` (the default) the plate STL has a
  completely flat z=0 underside (verified: STL z-range 0.0–5.0mm) — perfect
  first layer, zero supports. The per-key alignment pins are redundant on
  the full plate because the outline matches the PCB edge, which aligns the
  whole part. Set `plate_pins = true` only if you want the pins back (then
  print on a raft or with supports under the pins).
- **Top-facing overhangs:** everything else is either open upward (switch
  pockets, wire channels) or a short bridge any FDM printer handles:
  - clip windows / clip reliefs: 6mm bridges inside the walls
  - pin-entry pockets and wire-exit holes: small holes bridged at the
    channel membrane (0.5mm) — cleanly printable
  - center relief ceiling: a 31mm-wide flat ceiling at z=3.5mm — printed
    pockets-up this is a large bridge; enable supports **only inside the
    center relief pocket** (paint-on/blocker supports), or accept some sag
    since the underside there is cosmetic
- **Do NOT print top-face down**: that turns all 36 pocket floors into
  13.8mm bridged ceilings right where the switch seats and the pin holes
  are — sagging there ruins switch fit.
- Suggested settings: 0.2mm layers or finer, 3+ perimeters (the 0.45mm
  bezel walls need thin-wall handling or a 0.4mm nozzle with "detect thin
  walls" on), no supports, brim optional.
- Each loose adapter (`panel`/`adapter` parts) still carries the two φ1.15
  alignment pins for the PCB's non-plated φ1.30 holes; wire channels route
  the Choc pins to the PG1425 plated holes (see the main switch_converter
  project docs for wiring).
