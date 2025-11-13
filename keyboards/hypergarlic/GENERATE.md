# How to Generate Hypergarlic Case and Plate Files

## Step 1: Export PCB from KiCad

1. Open `hypergarlic.kicad_pcb` in KiCad PCB Editor
2. Go to **File → Export → STEP**
3. Settings:
   - Output file: `hypergarlic_pcb.step`
   - Coordinate origin: **Drill/Place file origin** (recommended)
   - Check: **Substitute similarly named models**
   - Uncheck: **Overwrite old file**
4. Click **Export**

This will create `hypergarlic_pcb.step` in this folder.

## Step 2: Run Generation Scripts

Once you have the STEP file, run these commands from the repository root:

```bash
cd /Users/ross/Projects/GitHub/rossw42/keyboard_stuff

# 1. Split PCB into left and right halves
python3 scripts/split_keyboard.py keyboards/hypergarlic/hypergarlic_pcb.step

# 2. Generate case bottoms
python3 scripts/generate_case.py keyboards/hypergarlic/hypergarlic_pcb_left.step keyboards/hypergarlic/hypergarlic_pcb_right.step keyboards/hypergarlic/

# 3. Generate plates with switch cutouts
python3 scripts/generate_plate_with_cutouts.py keyboards/hypergarlic/hypergarlic.kicad_pcb keyboards/hypergarlic/hypergarlic_pcb_left.step keyboards/hypergarlic/hypergarlic_pcb_right.step keyboards/hypergarlic/
```

## Expected Output

After running all scripts, you should have:

**PCB Files:**
- `hypergarlic_pcb.step` - Original full PCB
- `hypergarlic_pcb_left.step/stl` - Left half
- `hypergarlic_pcb_right.step/stl` - Right half

**Case Files:**
- `hypergarlic_case_bottom_left.step/stl`
- `hypergarlic_case_bottom_right.step/stl`

**Plate Files:**
- `hypergarlic_plate_left.step/stl` - with 20 switch cutouts
- `hypergarlic_plate_right.step/stl` - with 17 switch cutouts

## Quick Regenerate (if STEP file exists)

If you already have `hypergarlic_pcb.step`, just run:

```bash
cd /Users/ross/Projects/GitHub/rossw42/keyboard_stuff
./regenerate_hypergarlic.sh
```
