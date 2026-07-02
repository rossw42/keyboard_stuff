# Biaxial Keyboard Project — AI Context

## Project Overview
Biaxial is a custom ergonomic keyboard project using:
- Ergogen for PCB generation
- KiCad for PCB layout and validation
- QMK and/or Vial-QMK for firmware
- RP2040 (or compatible MCU)

The design is highly iterative and depends on correctness of firmware-matrix alignment and generated PCB geometry.

---

## Hard Rules (IMPORTANT)

### 1. Source of truth hierarchy
Always prioritize in this order:

1. vial-qmk/ repository (if Vial features are involved)
2. qmk_firmware/ repository
3. Ergogen project files in this workspace
4. KiCad project files
5. Model knowledge (ONLY if not found above)

If a feature is not found in the repositories, explicitly say:
> "Not found in QMK/Vial source"

Do NOT guess APIs or configuration fields.

---

### 2. No hallucinated firmware behavior
Never assume:
- QMK macros
- Vial features
- matrix scanning behavior
- combo/tap dance implementation details
- encoder handling

All firmware behavior must be verified in:
- quantum/
- keyboards/
- vial integration layer (if present)

---

### 3. Ergogen constraints
Assume:
- YAML structure must match Ergogen schema exactly
- footprint generation must be validated against ceoloide / known footprints
- PCB output must be KiCad-compatible

If uncertain, reference existing Ergogen examples in repo.

---

### 4. Keyboard architecture assumptions

## Ergogen-Specific Guidance

### Point System (Critical)

All keyboard geometry starts with **points** - 2D coordinates `[x, y, rotation]`:
- X axis: positive right, negative left
- Y axis: positive up, negative down
- Rotation: 0° = pointing up, +90° = pointing left (counter-clockwise)
- Coordinates are relative to rotation (shifting obeys the point's current orientation)

**Anchors** are how we avoid manual coordinate calculation:
- `ref: <point>` - use existing point as base
- `shift: [x, y]` - translate relative to current rotation
- `rotate: <degrees>` - post-rotation after shift
- `orient: <degrees>` - pre-rotation before shift
- `aggregate: {parts: [...], method: average}` - combine multiple points

### YAML Configuration Order

1. **metadata** - project info (name, author, description)
2. **units** - define abbreviations (u: 19.05 for standard key spacing)
3. **points** - define all key positions using anchors
4. **outlines** - create board perimeter by referencing points
5. **pcbs** - add electrical elements (footprints, traces, pads)
6. **cases** - generate 3D case geometry

### Footprints (PCB Placement)

Common Ergogen footprints:
- `mx` - Cherry MX switch (standard hotswap)
- `alps` - Alps switch (50/85 gram)
- `diode` - Protection diode (usually sod-123 or sod-323)
- `smd` - Surface mount component (MCU, resistor, capacitor)
- `pad` - Simple copper pad (testing, custom connectors)

**Key rule:** Every footprint must have:
- `what:` - footprint type (mx, diode, smd, etc)
- `where:` - which point(s) to place it at
- `shift:` / `rotate:` - optional positioning adjustments

### Export Formats

Ergogen outputs:
- `.kicad_pcb` - PCB file (import to KiCad for editing)
- `.kicad_sch` - Schematic file
- `.svg` - Board outline (can be exported to PDF, DXF, PNG)
- `.dxf` - CNC cutting file
- `.step` / `.stp` - 3D case model
- `.json` - Raw Ergogen data

### Common Pitfalls

1. **Coordinate confusion:**
	- Forgetting that shifts apply AFTER rotation
	- Assuming origin [0,0] stays at origin after rotate/shift (it doesn't)
	- Solution: Use multi-anchor "treasure hunt" approach with clear reference points

2. **Footprint misalignment:**
	- Not validating footprint positions in KiCad before manufacturing
	- Assuming Ergogen's anchor calculations match physical reality
	- Solution: Always verify generated PCB visually in KiCad

3. **Scale/unit errors:**
	- Mixing mm and custom units without conversion
	- Outputting in wrong units for CNC cutting
	- Solution: Define units early, use unit abbreviations consistently

4. **Outline generation:**
	- Points not closed properly (should form polygon, not chain)
	- Offset too small/large, causing pinch-points
	- Solution: Review SVG output visually before KiCad import

### Debugging Ergogen

When Ergogen config fails or output looks wrong:

1. **Validate YAML syntax** - check for indentation, quotes, colons
2. **Test point generation** - verify points render correctly in outline
3. **Check anchor references** - ensure all referenced points exist
4. **Verify units** - confirm all measurements use defined units
5. **Export intermediate SVG** - visually inspect board outline before PCB
6. **Compare with known examples** - find similar keyboard in ergogen_repos_list.md

### Integration with QMK

Once Ergogen generates the PCB:
1. Import `.kicad_pcb` to KiCad
2. Verify all switches/diodes are placed correctly
3. Export PCB dimensions (key grid spacing)
4. Map Ergogen point names to QMK matrix[row][col]
5. Create QMK `keyboards/<name>/matrix_diagram.md` matching Ergogen layout

---

### 4. Keyboard architecture assumptions

Unless explicitly stated otherwise:

- Matrix: row/column scanned
- Diodes: per-key (standard direction must be verified per design)
- MCU: RP2040-class (PIO possible)
- Firmware: QMK with optional Vial fork
- Layout: split or monoblock ergonomic variants

---

## Project Goals

- Stable QMK/Vial firmware build
- Ergogen-generated PCB without manual patching where possible
- Clean matrix-to-firmware mapping
- Reproducible builds from YAML → PCB → firmware

---

## Key Design Philosophy

This project prioritizes:
- correctness over abstraction
- explicit mappings over clever automation
- physical reality (PCB + wiring) over firmware convenience

---

## When editing or suggesting changes

Always:

1. Check existing repo implementation first
2. Identify matching patterns in QMK/Vial codebase
3. Prefer adapting existing keyboards over inventing new structures
4. Keep changes minimal and traceable

---

## Common directories

- vial-qmk/ → Vial firmware extensions
- qmk_firmware/ → upstream firmware source
- ergogen/ → layout + PCB generation configs
- kicad/ → PCB layout outputs
- Biaxial/ → primary project definitions

---

## Failure modes to avoid

- Inventing QMK API functions
- Assuming Vial features exist in upstream QMK
- Designing Ergogen footprints without validation
- Suggesting firmware changes not present in repo
- Mixing matrix definitions across projects

---

## Preferred workflow

When asked to implement or debug:

1. Locate relevant QMK/Vial implementation
2. Identify similar keyboard in repo
3. Trace matrix → diode → MCU mapping
4. Validate against Ergogen output
5. Only then propose changes

---

## Output expectations

When responding:
- Be precise
- Prefer referencing real files over explanation
- Use code-level reasoning
- Explicitly state uncertainty when source is missing