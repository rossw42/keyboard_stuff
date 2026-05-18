# MiniVan & Omnibus — Measurements Reference

## Sources

- [Trashman Wiki — MiniVan](https://trashman.wiki/keyboards/minivan)
- [Trashman Wiki — MiniVan Aluminum Case](https://trashman.wiki/cases/minivan-aluminum-case)
- [Trashman Wiki — Omnibus PCB](https://trashman.wiki/community/pcbs/omnibus)
- [Trashman Wiki — Files page](https://trashman.wiki/files#minivan)
- [40s Wiki — MiniVan](https://40s.wiki/boards/minivan)
- Mount pattern PDFs: [new pattern](https://trashman.wiki/files/minivan/minivan_pcb_mount_pattern.pdf), [old pattern](https://trashman.wiki/files/minivan/old_minivan_mount_pattern_and_dimensions.pdf)

---

## MiniVan PCB Dimensions

| Parameter | Value |
|-----------|-------|
| Layout size | 4u × 12.75u |
| Width | 12.75 × 19.05 mm = **242.89 mm** |
| Height (depth) | 4 × 19.05 mm = **76.20 mm** |
| 1u key spacing | 19.05 mm (0.75 in) |
| Switch cutout | 14.0 mm × 14.0 mm (standard MX) |

## MiniVan Tray Mount Pattern (Rev 2+)

Extracted from the [SteamVan open-source KiCad PCB](https://github.com/jmdaly/steamvan) — a verified MiniVan-compatible design.

- 7× M2 screw holes (M2×4mm screws, 2mm drill, 4mm pad)
- Rev 1 cases use a different (older) 3-hole compatible pattern — avoid
- Rev 2+ cases (and all subsequent tray-mount cases/PCBs) use the standardized 7-hole pattern below

### Mounting Hole Coordinates (Rev 2+ Standard)

Coordinates are relative to the PCB origin (top-left corner of the PCB outline, at the 3mm corner radius tangent point). The SteamVan footprint origin is at absolute KiCad position (102.84, 74.63), with the PCB edge starting at relative (-31.65, -19.05).

| Hole | X from PCB left edge (mm) | Y from PCB top edge (mm) | Notes |
|------|--------------------------|--------------------------|-------|
| 1 | 31.65 | 19.05 | Top-left area |
| 2 | 30.10 | 53.80 | Bottom-left, near LShift |
| 3 | 77.00 | 65.35 | Bottom, left of spacebar |
| 4 | 107.85 | 19.05 | Top-center |
| 5 | 138.34 | 38.15 | Center-right |
| 6 | 210.89 | 16.75 | Top-right, near USB |
| 7 | 182.59 | 65.55 | Bottom-right |

**Raw relative offsets from hole 1 (for KiCad placement):**

| Hole | ΔX (mm) | ΔY (mm) |
|------|---------|---------|
| 1 | 0.00 | 0.00 |
| 2 | -1.55 | 34.75 |
| 3 | 45.35 | 46.30 |
| 4 | 76.20 | 0.00 |
| 5 | 106.69 | 19.10 |
| 6 | 179.24 | -2.30 |
| 7 | 150.94 | 46.50 |

### PCB Outline Details

- Main rectangle with 3mm radius rounded corners
- USB cutout notch on top edge: ~12mm wide (from x=175.74 to x=187.74 relative to footprint origin), extending ~3.5mm above the main top edge
- USB cutout is positioned toward the right side (top-right) for case alignment

### Official Reference Files

- `minivan_pcb_mount_pattern.pdf` — [Download](https://trashman.wiki/files/minivan/minivan_pcb_mount_pattern.pdf) (current standard)
- `old_minivan_mount_pattern_and_dimensions.pdf` — [Download](https://trashman.wiki/files/minivan/old_minivan_mount_pattern_and_dimensions.pdf) (Rev 1 only)
- SteamVan KiCad source (CC-BY-SA-4.0): [github.com/jmdaly/steamvan](https://github.com/jmdaly/steamvan)

## MiniVan Case Interior (Tray Mount)

| Parameter | Value (approx) |
|-----------|----------------|
| Internal width | ~244–246 mm (PCB + ~1–1.5 mm clearance per side) |
| Internal depth | ~78–80 mm |
| PCB sits on | Integrated standoffs (aluminum) or plastic posts |
| USB cutout | Top-right; later revisions sized for USB-C (smaller than Mini-B cutout on early cases) |
| Screw type | M2×4mm, threading into standoffs (aluminum) or directly into plastic |
| Feet | 3/4" flat adhesive (all revisions) + optional screw-in cone feet (Rev 2+) |

### Rev 1 vs Rev 2+ Mounting Compatibility

Rev 1 aluminum cases use a different (older) mounting hole pattern. Only 3 of the 7 Rev 2+ holes align with Rev 1 standoffs:
- Top-right (near USB cutout)
- Bottom-left (near left Shift)
- Bottom row (left of spacebar)

Newer PCBs can be installed in Rev 1 cases using only these 3 screws. All subsequent tray-mount cases (Rev 2+, plastic, Rackmount, MFR, etc.) use the standardized 7-hole pattern.

### Case Variants

All cases below accept the standard MiniVan PCB footprint (242.89 × 76.20 mm). Tray-mount cases use the Rev 2+ 7-hole M2 pattern directly. Non-tray-mount cases (gasket, top-mount, bottom-mount) use the same PCB outline but different plate/mounting systems.

| Case | Mount | Material | Notes |
|------|-------|----------|-------|
| Aluminum case (Rev 2+) | Tray | CNC aluminum | The classic. 7-hole pattern. Cone feet optional. |
| Plastic case (Standard/KUMO/Atom/Catalyst) | Tray | Injection-molded plastic | Same 7-hole pattern. M2×4mm into plastic. |
| Rackmount | Tray | Brass / Polycarbonate | Low-profile, built-in handle. PC variant for Airport Shuttle. |
| Hull | Bottom | Aluminum | Springy flex mount. Same PCB footprint, different plates. |
| MFR / MFR2 | Tray | Aluminum / Acrylic | Thick tray mount. MFR2 open-source (Rainkeebs). |
| Carpool | Multi | CNC / 3D printed | Open-source. Coriander/Hull plates. STL+STEP available. |
| Hubris | Top | CNC aluminum | Open-source (Rainkeebs). Uses Coriander plates. |
| Campsite | Gasket | Premium metal | Gasket mount. Uses Campiander plates. |
| Barca | Bottom | Metal | Hull-style + Coriander plates. Optional SS foot/weight. |
| KnuckHull | Hybrid | Metal | Rackmount × Hull mashup. |
| Pomelo | Top | Premium metal | USB-C daughterboard. Pen rail. Coriander/Hull plates. |
| P⁴KCR3 | Isolation | Metal | Simplified isolation mount for max flex. |
| Coriander | Sandwich | Artificial stone | Thick-bezel three-layer. Accent ring. |
| MHKB / Aria | Sandwich | Stainless steel | Heavy sandwich mount. 5mm thick alu plate. |
| P3D cases | Various | Acrylic / 3D printed | Invisibolt gasket, bolt gasket, top mount, tray mount. |
| Why Not? | Layered | Acrylic | Deskmat-sized layered acrylic (P3D). |

## Omnibus PCB Specifications

| Parameter | Value |
|-----------|-------|
| Designer | Aeternus |
| Compatibility | MiniVan (all tray-mount cases) |
| Controller | ATmega32u4 |
| Connection | USB-C (top-right, snap-off option for daughterboard) |
| Switches | Soldered MX + 1× rotary encoder option |
| LEDs | 22× RGB underglow + optional strip |
| Stabilizers | PCB-mount supported for all spacebar positions |
| Firmware | QMK + VIAL |
| Bottom rows | 25+ unique layouts supported |
| Mounting | Standard MiniVan tray-mount holes (Rev 2+ pattern) |
| Snap-off tabs | For Trolley case support (remove for MiniVan cases) |
| JST headers | 2× (one for USB daughterboard, one for RGB strip) |
| Current revision | Rev 4.0 |

### Omnibus Key Compatibility Notes

- Drop-in replacement for all tray-mount MiniVan cases
- Also supports most top-mount and bottom-mount cases
- USB-C port positioned top-right for case cutout alignment
- Snap-off USB connector + rear JST for daughterboard cases (Pomelo, MB-44)
- Supports all MiniVan, Ketch, JetVan, Minisub, m3n3van, and MB44 layouts
- Reset switch positioned for tray-mount case compatibility
- Standard stagger on top 3 rows; layout flexibility is in the bottom row
- PCB-mount stabs supported for all spacebar positions (some may interfere with Trolley gummy worm mount)
- Left JST = USB daughterboard, center JST = RGB strip (bridge solder pads if no strip installed)
- Support guide: [help.aeternus.co/omnibus](https://help.aeternus.co/omnibus/)

---

## Omnibus/Hull Plate Outline (from Omnibus_Hull.dxf)

Reference file: `Omnibus_Hull.dxf` — the Omnibus plate outline for Hull-compatible cases.

### Overall Dimensions

| Parameter | Value |
|-----------|-------|
| Main body width | 242.89 mm (x = -233.3625 to x = 9.525) |
| Main body height | 76.20 mm (y = -9.525 to y = 66.675) |
| Overall width (with tabs) | 247.54 mm (x = -235.6875 to x = 11.85) |
| Overall height | 76.20 mm |

### Snap-off Tabs (Hull Compatibility)

Both left and right sides have protruding tabs required for Hull case mounting:

| Parameter | Value |
|-----------|-------|
| Tab width | 2.325 mm per side |
| Tab height | 62.5 mm (y = -2.675 to y = 59.825) |
| Tab connection | Narrow neck profile with complex arc transitions (radii: 2.675, 1.25, 0.5 mm) |
| Left tab | x = -235.6875 to x = -233.3625 |
| Right tab | x = 9.525 to x = 11.85 |

These tabs are NOT optional for Hull plate compatibility. Any Micro Alice plate file must include them.

### Corner Details

| Location | Radius |
|----------|--------|
| Main body inner corners (where tabs meet body) | 1.5 mm |
| Tab outer corners | Complex profile (2.675 mm outer arc → 0.5 mm transition → 1.25 mm inner arc) |

### Switch Cutouts

- 14 mm × 14 mm standard MX throughout
- ~44 switch positions + 2 complex stabilizer cutout regions on the bottom row

---

## Critical Dimensions for Micro Alice Design

To fit inside any MiniVan tray-mount case, the Micro Alice PCB must:

1. **PCB outline:** Rectangular, 242.89 mm × 76.20 mm (±0.1 mm tolerance)
2. **Mounting holes:** Match the Rev 2+ 7-hole M2 pattern exactly (coordinates in table above, sourced from SteamVan KiCad)
3. **USB-C port:** Top-right edge, matching existing case cutout position
4. **Component clearance:** All components (switches, MCU, diodes) must clear the case standoffs
5. **Plate outline:** Must match the full Omnibus/Hull plate dimensions including the side tabs (247.54 mm overall width). Custom switch cutouts required for angled Alice layout — no existing MiniVan plate file will work.
6. **Tab geometry:** Left and right tabs (2.325 mm × 62.5 mm each) with the standard neck profile must be present for Hull case compatibility.

### Width Budget (inside the 12.75u envelope)

| Component | Width |
|-----------|-------|
| Available PCB width | 242.89 mm |
| 11 columns × 19.05 mm | 209.55 mm |
| Center gap (~0.5u) | ~9.5 mm |
| Remaining for edge margins | ~23.8 mm (~11.9 mm per side) |

This confirms the layout fits within the MiniVan PCB footprint with comfortable margins.

---

## Files to Download

These files from the Trashman Wiki are essential for the Micro Alice design:

- `minivan_pcb_mount_pattern.pdf` — Tray mount hole coordinates
- `minivan_universal_reference.dxf` — Universal plate outline (use as starting point for custom plate)
- `minivanfoam.dxf` — Case foam template (shows internal cavity shape)
- [MiniVan Compatibility Matrix](https://docs.google.com/spreadsheets/d/1Q1mkIIO67bMsw57uznCavpfXVzcDROpAM5NUxizeva4/) — PCB/case compatibility reference
- [MiniVanPlate.xyz](http://www.minivanplate.xyz/) — Plate file generator for various PCB/case combos
