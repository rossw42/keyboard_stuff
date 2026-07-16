# Cyberdeck v2 — Stock Rev 8 Case + 7.84" Screen

> **Approach change from v1** (archived: `archive/case_v1/`): instead of a from-scratch
> parametric case in the Rev 8 *style*, v2 uses unkyulee's **actual Rev 8
> STLs** — the aesthetic and all the tricky geometry (hinge, joints, hood,
> latching) are already solved. The only modification is to the lid's front
> frame so the **7.84" Wisecoco 400×1280 panel** fits instead of Rev 8's
> stock 5" display.

---

## 1. What's stock, what's modified

| Rev 8 part | Status | Notes |
|---|---|---|
| Enclosure Left / Middle / Right | **stock** | keyboard base — same 68-key plates as Rev 2.1 (`keyboard plate space/arrow` are byte-identical footprints) |
| Enclosure Lid (battery door) | **stock** | |
| Hood Top / Bottom / Left / Right | **stock** | rear electronics hood |
| Display Enclosure Left / Middle / Right | **stock** | lid back shell + hinge roll |
| Display Wire Cap | **stock** | hinge cable cover |
| **Display Panel Left / Middle / Right** | **MODIFIED** → `stl/panel_*.stl` | lid front frame — see §2 |
| Display Back Cover, Display Port | **omitted** | stock 5" display mounting hardware — not needed; the 7.84" panel mounts in the new pocket |

## 2. The modification (all in `cyberdeckv2.scad`)

Boolean edit of the three Display Panel pieces, using shared global cutters
so the stock zig-zag joints between pieces still line up:

1. **Fill** the stock ~5" aperture (probed at x[-48.6, 56] × y[-45.9, 31.3])
   in the middle piece with a solid slab.
2. **Cut the new aperture**: 207.4 × 66.2 mm (active area 205.4 × 64.2 +
   1 mm margin), centered at (0, −6) in Rev 8 lid coordinates.
3. **Cut a back-side pocket**: 214.2 × 72.5 mm (panel outline 213.6 × 71.9 +
   0.3 mm/side), leaving a 1 mm front lip. The bare panel drops in from
   behind and is retained by the stock Display Enclosure shell when the lid
   is assembled (foam tape shim behind the panel recommended — the frame is
   4 mm, panel 2.9 mm, so ~0.1 mm of float after the 1 mm lip).

Placement was chosen so the pocket clears the frame's stock screw rows
(y ≈ −43.5 and +31.2) by ~0.5–0.9 mm — all six original frame screws remain
usable. Compile-time CHECK asserts verify this.

```
Frame (322 × 98.7):     +--------------------------------------+
  screw row y=31.2  ->  |  o        o          o          o    |
                        |  +--------------------------------+  |
  new aperture/pocket   |  |      7.84" ACTIVE AREA         |  |
  centered y=-6         |  +--------------------------------+  |
  screw row y=-43.5 ->  |  o        o          o          o    |
                        +--------------------------------------+
```

## 3. Electronics placement (Pico-less, per main design.md)

- **Pi Zero 2W + 18650 shield** — in the Rev 8 base under the rear hood,
  same zone the stock build uses for its electronics. The Pico-less mod
  frees the space the Pico + USB hub occupied.
- **MIPI→HDMI driver board (~105 × 45 × 12)** — inside the lid behind the
  panel; the Display Enclosure back shell is 12 mm deep (z 23..35), panel +
  frame take ~4, leaving ~8 mm — ⚠ measure the actual driver; if it's
  thicker than 8 mm it moves down into the base hood and only the thin
  MIPI ribbon stays in the lid (preferred anyway for hinge longevity).
- **HDMI + 5 V** — through the stock hinge/Wire Cap channel, exactly the
  route Rev 8 already uses for its display cable.
- **Keyboard matrix** — Rev 8's base already routes the keyboard to the
  rear electronics zone; the 22-wire bundle goes to the Pi header directly.

## 4. Files

| File | Purpose |
|---|---|
| **`BUILDGUIDE.md`** | **Builder's assembly instructions** — print prep, step-by-step assembly, bring-up, troubleshooting |
| **`bom_v2.md`** | **Full bill of materials** — printed parts, electronics, Rev 8 case hardware, purchase links, likely-buy list |
| `cyberdeckv2.scad` | Imports Rev 8 STLs + applies the panel mods. `part=` selects `panel_left/middle/right`, `lid_frame_only`, `lid_assembly`, `full_assembly`, `aperture_check` |
| **`stl/`** | **The complete print set (20 files)**: 3 modified frame pieces (`panel_left/middle/right.stl`) + 3 stock Display Panel source STLs (used by the SCAD booleans) + 14 stock Rev 8 parts (Enclosure L/M/R + Lid, Display Enclosure L/M/R, Wire Cap, Hood ×4, keyboard plates ×2). Stock `Display Back Cover` and `Display Port` are intentionally excluded |
| `probe_aperture.py` | STL probe used to locate the stock aperture + screw rows |
| `renders/` | Previews: modified frame (front), lid assembly, Rev 8 references |

## 5. Print / build plan

1. **Print everything in `stl/`** (17 files) — that folder is the full
   part list for the build. Frame pieces face down, per unkyulee's Rev 8
   orientation guidance.
2. Assemble the lid: panel drops into the pocket from behind (foam tape
   shim), stock Display Enclosure screws on behind it.
3. Follow the Rev 8 build for the base/hinge/hood; wire per the main
   `design.md` §4 pin map (Pico-less).

## 6. Bench-verify before printing (⚠)

1. Measure the actual Wisecoco panel (outline, active area centering,
   ribbon exit side) — adjust `pan_*`/`act_*`/`disp_cy` and re-export.
2. Measure the MIPI→HDMI driver; decide lid vs base placement.
3. The pocket-to-screw clearances are ~0.5–0.9 mm; if the real panel is
   bigger than spec, shift `disp_cy` or accept relocating two screws.
4. Confirm the panel ribbon/connector doesn't collide with the Display
   Enclosure's internal ribs (check after first test fit).