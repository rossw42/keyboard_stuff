# Keyboard CAD Scripts

Python scripts for working with keyboard PCB STEP files exported from KiCad.

## Prerequisites

```bash
pip install cadquery trimesh shapely
```

## Scripts

### split_keyboard.py

Split a keyboard PCB STEP file into left and right halves.

**Usage:**
```bash
python split_keyboard.py <input.step> [output_dir]
```

**Example:**
```bash
python split_keyboard.py keyboards/myboard/myboard.step
python split_keyboard.py keyboards/myboard/myboard.step ./output
```

**Output:**
- `{name}_pcb_left.step` / `.stl`
- `{name}_pcb_right.step` / `.stl`

---

### generate_case.py

Generate minimal tray-style case bottoms for split keyboard halves.
Design based on analysis of Sweep and Corne keyboards.

**Usage:**
```bash
python generate_case.py <pcb_left.step> <pcb_right.step> [output_dir]
```

**Example:**
```bash
python generate_case.py keyboards/myboard/myboard_pcb_left.step keyboards/myboard/myboard_pcb_right.step
```

**Output:**
- `{name}_case_bottom_left.step` / `.stl`
- `{name}_case_bottom_right.step` / `.stl`

**Parameters (edit in script):**
- `WALL_THICKNESS` - Case wall thickness (default: 2.0mm)
- `BOTTOM_THICKNESS` - Bottom plate thickness (default: 1.5mm)
- `PCB_CLEARANCE_BOTTOM` - Space below PCB (default: 2.5mm)
- `OFFSET` - Distance case extends beyond PCB (default: 2.5mm)
- `FILLET_RADIUS` - Edge rounding (default: 1.5mm)

---

### generate_plate.py

Generate switch plates for split keyboard halves (without switch cutouts).
Standard 1.5mm thickness for Cherry MX switches.

**Usage:**
```bash
python generate_plate.py <pcb_left.step> <pcb_right.step> [output_dir]
```

**Example:**
```bash
python generate_plate.py keyboards/myboard/myboard_pcb_left.step keyboards/myboard/myboard_pcb_right.step
```

**Output:**
- `{name}_plate_left.step` / `.stl`
- `{name}_plate_right.step` / `.stl`

**Note:** Generates solid plates. You'll need to manually add 14x14mm switch cutouts in CAD software.

---

### generate_plate_with_cutouts.py

**NEW!** Generate switch plates with automatic switch cutouts extracted from KiCad PCB file.

**Usage:**
```bash
python generate_plate_with_cutouts.py <kicad_pcb_file> <pcb_left.step> <pcb_right.step> [output_dir]
```

**Example:**
```bash
python generate_plate_with_cutouts.py keyboards/myboard/myboard.kicad_pcb keyboards/myboard/myboard_pcb_left.step keyboards/myboard/myboard_pcb_right.step
```

**Output:**
- `{name}_plate_left.step` / `.stl` - with switch cutouts!
- `{name}_plate_right.step` / `.stl` - with switch cutouts!

**Features:**
- Automatically detects switch positions from KiCad PCB file
- Supports Cherry MX, Choc (PG1350), and other switch types
- Creates 14x14mm cutouts at each switch location
- Follows organic PCB outline
- Ready to print - no manual CAD work needed!

**Parameters (edit in script):**
- `PLATE_THICKNESS` - Plate thickness (default: 1.5mm)
- `PLATE_OFFSET` - Distance plate extends beyond PCB (default: 1.0mm)
- `SWITCH_CUTOUT_SIZE` - Switch cutout size (default: 14.0mm)

---

## Workflow

### Basic Workflow (manual switch cutouts)
1. Export your PCB from KiCad as STEP file (e.g., `myboard_pcb.step`)
2. Split it into halves: `python split_keyboard.py myboard_pcb.step`
3. Generate case bottoms: `python generate_case.py myboard_pcb_left.step myboard_pcb_right.step`
4. Generate switch plates: `python generate_plate.py myboard_pcb_left.step myboard_pcb_right.step`
5. Manually add switch cutouts in CAD software
6. Load STL files into your slicer and print!

### Advanced Workflow (automatic switch cutouts)
1. Export your PCB from KiCad as STEP file (e.g., `myboard_pcb.step`)
2. Split it into halves: `python split_keyboard.py myboard_pcb.step`
3. Generate case bottoms: `python generate_case.py myboard_pcb_left.step myboard_pcb_right.step`
4. Generate plates with cutouts: `python generate_plate_with_cutouts.py myboard.kicad_pcb myboard_pcb_left.step myboard_pcb_right.step`
5. Load STL files into your slicer and print!

## Design Philosophy

These scripts are based on analysis of popular open-source keyboards (Sweep, Corne):

**Case Design:**
- Low profile (~7-8mm total height)
- Minimal wall thickness (2.0mm)
- Thin bottom (1.5mm)
- Compact offset from PCB edge (2.5mm)
- Smooth filleted edges (1.5mm radius)
- M3 mounting holes in corners

**Plate Design:**
- Standard 1.5mm thickness for Cherry MX and Choc switches
- Minimal offset from PCB (1.0mm)
- M2.5 mounting holes
- Automatic switch cutout detection from KiCad PCB file (14x14mm per switch)
- Supports Cherry MX, Kailh Choc (PG1350), and hotswap sockets

## File Naming Convention

- `{name}_pcb.step` - Full PCB export from KiCad
- `{name}_pcb_left.step/stl` - Left half of PCB
- `{name}_pcb_right.step/stl` - Right half of PCB
- `{name}_case_bottom_left.step/stl` - Left case bottom
- `{name}_case_bottom_right.step/stl` - Right case bottom
- `{name}_plate_left.step/stl` - Left switch plate (future)
- `{name}_plate_right.step/stl` - Right switch plate (future)

## Notes

- Scripts work with any split keyboard PCB exported from KiCad
- STEP files preserve CAD geometry for further editing
- STL files are ready for 3D printing
- Cases include M3 screw holes in corners
