# Keyboard Case Generator

Generate 3D-printable keyboard cases from KiCad PCB designs. Works with any keyboard PCB - single or split.

## Installation

```bash
pip install cadquery shapely
```

## Quick Start

**You only need one command:**

```bash
cd scripts

# Single keyboard (like a 60%, TKL, etc.)
python keyboard_case_workflow.py single path/to/keyboard.step --kicad-pcb path/to/keyboard.kicad_pcb

# Split keyboard (like Corne, Sweep, etc.)
python keyboard_case_workflow.py split path/to/keyboard.step --kicad-pcb path/to/keyboard.kicad_pcb

# Unify a single half into a complete keyboard (NEW!)
python keyboard_case_workflow.py unify path/to/keyboard_left.step --gap 15 --splay 5
```

That's it! The script will generate everything you need.

## What You Get

### Single Keyboard
- `keyboard_bottom_tray.step` / `.stl` - Bottom case with mounting posts
- `keyboard_switch_plate.step` / `.stl` - Top plate with switch cutouts

### Split Keyboard
- `keyboard_pcb_left.step` / `.stl` - Left PCB half
- `keyboard_pcb_right.step` / `.stl` - Right PCB half
- `keyboard_bottom_tray_left.step` / `.stl` - Left bottom case
- `keyboard_bottom_tray_right.step` / `.stl` - Right bottom case
- `keyboard_switch_plate_left.step` / `.stl` - Left switch plate
- `keyboard_switch_plate_right.step` / `.stl` - Right switch plate

## Step-by-Step Workflow

1. **Design your PCB in KiCad** (or use an existing design)

2. **Export STEP file from KiCad:**
   - File → Export → STEP
   - Save as `keyboard.step`

3. **Run the generator:**
   ```bash
   cd scripts
   python keyboard_case_workflow.py single ../path/to/keyboard.step \
     --kicad-pcb ../path/to/keyboard.kicad_pcb \
     --output ../path/to/output
   ```

4. **3D print the STL files** - Load them into your slicer and print!

## Common Options

```bash
# Specify output directory
--output path/to/output

# Disable chamfered edges (if they fail on complex geometry)
--no-chamfers

# Use fillets instead of chamfers
--enable-fillets

# Disable rubber feet recesses
--no-rubber-feet

# Also generate PCB STL for visualization
--generate-pcb-stl
```

## Examples

### Example 1: Basic 60% Keyboard
```bash
python keyboard_case_workflow.py single ../keyboards/my60/my60.step \
  --kicad-pcb ../keyboards/my60/my60.kicad_pcb \
  --output ../keyboards/my60/output
```

### Example 2: Split Keyboard (Corne, Sweep, etc.)
```bash
python keyboard_case_workflow.py split ../keyboards/corne/corne.step \
  --kicad-pcb ../keyboards/corne/corne.kicad_pcb \
  --output ../keyboards/corne/output
```

### Example 3: Unify a Single Half into Complete Keyboard
```bash
# Take just the left half and create a unified keyboard
python keyboard_case_workflow.py unify ../keyboards/corne/corne_left.step \
  --gap 15 \
  --splay 5 \
  --kicad-pcb ../keyboards/corne/corne.kicad_pcb \
  --output ../keyboards/corne/unified_output
```

### Example 4: Just Convert PCB to STL (for visualization)
```bash
python keyboard_case_workflow.py pcb-stl ../keyboards/my60/my60.step
```

## Features

- **Automatic switch detection** - Reads switch positions from your `.kicad_pcb` file
- **Organic outline following** - Case follows your actual PCB shape
- **Professional features** - Chamfered edges, mounting posts, plate lips, rubber feet
- **Split keyboard support** - Automatically splits and generates both halves
- **Unify workflow** - Take a single half and create a unified keyboard with configurable gap/splay
- **Multiple outputs** - STEP files (for CAD editing) and STL files (for 3D printing)

## Troubleshooting

### "Failed to import STEP file"
- Re-export from KiCad: File → Export → STEP
- Make sure the file isn't corrupted

### "No switches found in KiCad PCB file"
- Check that your switches use standard footprints (MX, Choc, PG1350)
- The generator will create a solid plate if no switches are detected
- You can manually add cutouts in CAD software later

### "Failed to apply chamfers"
- Try: `--enable-fillets` or `--no-chamfers`
- Complex geometry can cause chamfer operations to fail

### "Command not found" or "Module not found"
- Make sure you're running from the `scripts/` directory
- Check that dependencies are installed: `pip install cadquery shapely`

## Advanced Usage

If you need more control, you can use the individual scripts:

### Split a PCB manually
```bash
python split_keyboard.py keyboard.step output_dir/
```

### Combine a single half into unified keyboard
```bash
python combine_split_halves.py keyboard_left.step \
  --gap 15 \
  --splay 5 \
  -o output/keyboard_unified.step
```

### Convert STEP to STL
```bash
python convert_step_to_stl.py input.step output.stl
```

### Use the generator directly (with custom parameters)
```bash
python generate_case_unified.py keyboard.step \
  --kicad-pcb keyboard.kicad_pcb \
  --wall-thickness 2.5 \
  --case-height 10.0 \
  --case-offset 3.0
```

## Design Philosophy

This is a **PCB-first** approach - you start with an existing PCB design and generate a case to fit it. Perfect for:
- Custom keyboard designs
- Purchased PCBs that need cases
- Open-source PCB designs you found online
- Quick iteration on case designs

## Project Structure

```
scripts/
├── keyboard_case_workflow.py    ← Main script (USE THIS!)
├── generate_case_unified.py     ← Core generator
├── split_keyboard.py            ← PCB splitter
├── convert_step_to_stl.py       ← STEP→STL converter
└── case_generator/              ← Generator modules
    ├── pcb_analyzer.py          ← PCB import/analysis
    ├── switch_detector.py       ← KiCad PCB parsing
    ├── bottom_tray.py           ← Case bottom generation
    ├── switch_plate.py          ← Switch plate generation
    └── ...
```

## Need Help?

Check the other documentation files:
- `UNIFY_WORKFLOW.md` - Detailed guide for combining split halves into unified keyboards
- `WORKFLOW_GUIDE.md` - Detailed workflow examples
- `case_generator/README.md` - Technical details about the generator
- `kicad-pcb-format.md` - KiCad file format notes
