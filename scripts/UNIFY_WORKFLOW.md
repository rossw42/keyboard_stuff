# Unify Workflow - Combine Split Keyboard Halves

The `unify` workflow allows you to take a **single half** of a split keyboard and create a **unified keyboard** by mirroring and combining both halves.

## Use Case

Perfect for when you have:
- A single half PCB design (e.g., just the left side of a Corne)
- Want to create a unified/monoblock version instead of separate halves
- Need to experiment with different gap spacing or splay angles

## Basic Usage

```bash
# Basic unification with default 15mm gap
python scripts/keyboard_case_workflow.py unify corne_left.step

# With custom gap and splay
python scripts/keyboard_case_workflow.py unify corne_left.step --gap 20 --splay 5

# With KiCad file for switch detection
python scripts/keyboard_case_workflow.py unify corne_left.step \
  --kicad-pcb corne.kicad_pcb \
  --gap 15 \
  --splay 3
```

## Parameters

### Required
- `half_step` - Path to the single half PCB STEP file

### Optional
- `--gap FLOAT` - Gap between halves in mm (default: 15.0)
- `--splay FLOAT` - Splay angle in degrees, positive = outward rotation (default: 0.0)
- `--vertical-offset FLOAT` - Vertical offset between halves in mm (default: 0.0)
- `--which-half {left,right}` - Which half is the input (default: left)
- `--kicad-pcb PATH` - KiCad PCB file for switch detection
- `-o, --output PATH` - Output directory (default: ./output)

### Case Options
- `--no-chamfers` - Disable chamfered edges
- `--enable-fillets` - Use fillets instead of chamfers
- `--no-rubber-feet` - Disable rubber feet recesses
- `--no-plate-lip` - Disable plate mounting lip

## What It Does

1. **Loads** the single half PCB
2. **Mirrors** it to create the opposite half
3. **Positions** both halves with:
   - Configurable gap spacing
   - Optional splay angle (ergonomic tilt)
   - Optional vertical offset (stagger)
4. **Combines** into a single unified PCB geometry
5. **Generates** a complete case for the unified keyboard

## Examples

### Standard Corne Unification
```bash
python scripts/keyboard_case_workflow.py unify keyboards/corne/corne_left.step \
  --gap 15 \
  --output keyboards/corne/unified_output
```

### Ergonomic Splay
```bash
# 5° outward splay for more ergonomic hand position
python scripts/keyboard_case_workflow.py unify keyboards/corne/corne_left.step \
  --gap 20 \
  --splay 5
```

### Staggered Halves
```bash
# Offset right half 10mm higher for columnar stagger
python scripts/keyboard_case_workflow.py unify keyboards/corne/corne_left.step \
  --gap 15 \
  --vertical-offset 10
```

### Right Half as Input
```bash
# If you only have the right half
python scripts/keyboard_case_workflow.py unify keyboards/corne/corne_right.step \
  --which-half right \
  --gap 15
```

## Output Files

The workflow generates:
- `<name>_unified.step` - Combined PCB STEP file
- `<name>_unified.stl` - Combined PCB STL file
- `<name>_bottom_tray.step` - Bottom case STEP
- `<name>_bottom_tray.stl` - Bottom case STL (3D printable)
- `<name>_switch_plate.step` - Switch plate STEP (solid, no cutouts)
- `<name>_switch_plate.stl` - Switch plate STL (solid, no cutouts)

**Note**: Currently, the unified workflow generates a solid switch plate without switch cutouts. You can add cutouts manually in CAD software using the STEP file.

## Tips

- **Gap**: 15-20mm is typical for comfortable typing
- **Splay**: 3-7° provides ergonomic benefits without being too extreme
- **Vertical Offset**: Useful for creating columnar stagger or matching hand positions
- **Switch Detection**: Providing the KiCad PCB file ensures accurate switch cutouts

## Standalone Script

You can also use the combine script directly:

```bash
python scripts/combine_split_halves.py corne_left.step \
  --gap 15 \
  --splay 5 \
  -o output/corne_unified.step
```

This just combines the halves without generating the case.
