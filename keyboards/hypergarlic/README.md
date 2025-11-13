# Hypergarlic Keyboard

Split ergonomic keyboard with automatic case and plate generation.

## Quick Start

**To generate all files:**

1. Export PCB from KiCad: `File → Export → STEP` → Save as `hypergarlic_pcb.step`
2. Run: `./regenerate_hypergarlic.sh` (from repository root)
3. Print the STL files!

See `GENERATE.md` for detailed instructions.

## Files

### PCB Files
- `hypergarlic_pcb.step` - Original full PCB export from KiCad
- `hypergarlic_pcb_left.step/stl` - Left half PCB
- `hypergarlic_pcb_right.step/stl` - Right half PCB

### Case Bottom Files
- `hypergarlic_case_bottom_left.step/stl` - Left case bottom
- `hypergarlic_case_bottom_right.step/stl` - Right case bottom

**Case Specifications:**
- Height: 6.5mm (low profile)
- Wall thickness: 2.0mm
- Bottom thickness: 1.5mm
- PCB clearance: 2.5mm below PCB
- Offset from PCB edge: 2.5mm
- Filleted edges: 1.5mm radius
- Mounting: M3 screw holes in corners

### Switch Plate Files
- `hypergarlic_plate_left.step/stl` - Left switch plate with cutouts
- `hypergarlic_plate_right.step/stl` - Right switch plate with cutouts

**Plate Specifications:**
- Thickness: 1.5mm (standard for Choc switches)
- Offset from PCB edge: 1.0mm
- Mounting: M2.5 screw holes in corners
- Switch cutouts: 14x14mm (20 switches left, 17 switches right)
- **Ready to print!** No manual CAD work needed

## Dimensions

**Left Half:**
- Width: 119.4mm
- Depth: 87.7mm
- PCB thickness: 1.5mm

**Right Half:**
- Width: 119.4mm
- Depth: 87.7mm
- PCB thickness: 1.5mm

## 3D Printing

### Case Bottom
- Material: PLA, PETG, or ABS
- Layer height: 0.2mm
- Infill: 20-30%
- Supports: Not required
- Print orientation: Bottom face down

### Switch Plate
- Material: PLA or PETG (needs rigidity)
- Layer height: 0.15-0.2mm
- Infill: 100% (solid plate)
- Supports: Not required
- Print orientation: Flat on bed
- **Ready to print!** Switch cutouts already included

## Assembly

1. Print case bottoms and plates
2. Install switches into plate (after adding cutouts)
3. Mount PCB to case bottom with M3 screws
4. Attach plate to case (sandwich mount)
5. Install keycaps

## Regenerating Files

If you need to regenerate any files:

```bash
# From repository root
cd /Users/ross/Projects/GitHub/rossw42/keyboard_stuff

# Regenerate case bottoms
python3 scripts/generate_case.py keyboards/hypergarlic/hypergarlic_pcb_left.step keyboards/hypergarlic/hypergarlic_pcb_right.step keyboards/hypergarlic/

# Regenerate plates with switch cutouts
python3 scripts/generate_plate_with_cutouts.py keyboards/hypergarlic/hypergarlic.kicad_pcb keyboards/hypergarlic/hypergarlic_pcb_left.step keyboards/hypergarlic/hypergarlic_pcb_right.step keyboards/hypergarlic/
```

## Notes

- Case design follows minimal aesthetic of Sweep/Corne keyboards
- All measurements in millimeters
- STEP files can be edited in CAD software (FreeCAD, Fusion 360, etc.)
- STL files are ready for slicing and printing
