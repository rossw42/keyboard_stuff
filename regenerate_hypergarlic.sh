#!/bin/bash
# Regenerate all hypergarlic case and plate files

set -e  # Exit on error

KEYBOARD_DIR="keyboards/hypergarlic"
PCB_FILE="$KEYBOARD_DIR/hypergarlic_pcb.step"
KICAD_FILE="$KEYBOARD_DIR/hypergarlic.kicad_pcb"

echo "=========================================="
echo "Hypergarlic Case & Plate Generator"
echo "=========================================="

# Check if PCB STEP file exists
if [ ! -f "$PCB_FILE" ]; then
    echo ""
    echo "❌ Error: PCB STEP file not found: $PCB_FILE"
    echo ""
    echo "Please export the PCB from KiCad first:"
    echo "  1. Open hypergarlic.kicad_pcb in KiCad"
    echo "  2. File → Export → STEP"
    echo "  3. Save as: hypergarlic_pcb.step"
    echo ""
    echo "See keyboards/hypergarlic/GENERATE.md for detailed instructions"
    exit 1
fi

echo ""
echo "✓ Found PCB file: $PCB_FILE"
echo ""

# Step 1: Split PCB
echo "Step 1/3: Splitting PCB into halves..."
echo "----------------------------------------"
python3 scripts/split_keyboard.py "$PCB_FILE" "$KEYBOARD_DIR"

echo ""
echo "Step 2/3: Generating case bottoms..."
echo "----------------------------------------"
python3 scripts/generate_case.py \
    "$KEYBOARD_DIR/hypergarlic_pcb_left.step" \
    "$KEYBOARD_DIR/hypergarlic_pcb_right.step" \
    "$KEYBOARD_DIR"

echo ""
echo "Step 3/3: Generating plates with switch cutouts..."
echo "----------------------------------------"
python3 scripts/generate_plate_with_cutouts.py \
    "$KICAD_FILE" \
    "$KEYBOARD_DIR/hypergarlic_pcb_left.step" \
    "$KEYBOARD_DIR/hypergarlic_pcb_right.step" \
    "$KEYBOARD_DIR"

echo ""
echo "=========================================="
echo "✓ Generation Complete!"
echo "=========================================="
echo ""
echo "Generated files in $KEYBOARD_DIR:"
echo "  - PCB halves (left/right)"
echo "  - Case bottoms (left/right)"
echo "  - Plates with switch cutouts (left/right)"
echo ""
echo "All STL files are ready for 3D printing!"
echo ""
