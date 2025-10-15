#!/usr/bin/env python3
"""
Export assembly drawing with hardware callouts.

This script generates a PDF assembly drawing showing both components
in an exploded view with all hardware labeled and assembly sequence notes.

Task 6.3: Generate assembly drawing with hardware callouts
Requirements: 8.1, 8.4
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from constants import (
    CASE_LENGTH, CASE_WIDTH, CASE_CORNER_RADIUS,
    PCB_OPENING_LENGTH, PCB_OPENING_WIDTH, PCB_BORDER,
    USB_CUTOUT_WIDTH, USB_CUTOUT_HEIGHT, USB_CUTOUT_CORNER_RADIUS,
    USB_CUTOUT_CENTER_X, USB_CUTOUT_CENTER_Y,
    CAVITY_LENGTH, CAVITY_WIDTH, CAVITY_CORNER_RADIUS, WALL_THICKNESS,
    MOUNTING_HOLES,
    BRASS_INSERT_DIAMETER,
    STANDOFF_DIAMETER, STANDOFF_HOLE_DIAMETER,
    ASSEMBLY_SCREW_DIAMETER, ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
    RUBBER_FEET_POSITIONS, RUBBER_FEET_DIAMETER,
    TOP_FRAME_HEIGHT, BOTTOM_TRAY_HEIGHT
)
from geometry import generate_top_frame_profile, generate_bottom_tray_profile
from export.technical_drawings import export_assembly_drawing_pdf


def main():
    """Generate and export assembly drawing."""
    
    print("=" * 70)
    print("Task 6.3: Generate Assembly Drawing with Hardware Callouts")
    print("=" * 70)
    print()
    
    # Generate top frame profile geometry
    print("Step 1: Generating top frame profile...")
    top_frame_profile = generate_top_frame_profile(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        case_corner_radius=CASE_CORNER_RADIUS,
        pcb_opening_length=PCB_OPENING_LENGTH,
        pcb_opening_width=PCB_OPENING_WIDTH,
        pcb_border=PCB_BORDER,
        usb_cutout_width=USB_CUTOUT_WIDTH,
        usb_cutout_height=USB_CUTOUT_HEIGHT,
        usb_corner_radius=USB_CUTOUT_CORNER_RADIUS,
        usb_center_x=USB_CUTOUT_CENTER_X,
        usb_center_y=USB_CUTOUT_CENTER_Y,
        mounting_holes=MOUNTING_HOLES,
        brass_insert_diameter=BRASS_INSERT_DIAMETER
    )
    print("✓ Top frame profile complete")
    
    # Generate bottom tray profile geometry
    print("Step 2: Generating bottom tray profile...")
    bottom_tray_profile = generate_bottom_tray_profile(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        case_corner_radius=CASE_CORNER_RADIUS,
        cavity_length=CAVITY_LENGTH,
        cavity_width=CAVITY_WIDTH,
        cavity_corner_radius=CAVITY_CORNER_RADIUS,
        wall_thickness=WALL_THICKNESS,
        mounting_holes=MOUNTING_HOLES,
        standoff_pillar_diameter=STANDOFF_DIAMETER,
        standoff_hole_diameter=STANDOFF_HOLE_DIAMETER,
        assembly_screw_diameter=ASSEMBLY_SCREW_DIAMETER,
        assembly_counterbore_diameter=ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        rubber_feet_diameter=RUBBER_FEET_DIAMETER
    )
    print("✓ Bottom tray profile complete")
    print()
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', '60_percent_standard', 'cnc', 'drawings')
    os.makedirs(output_dir, exist_ok=True)
    
    # Export assembly drawing to PDF
    print("Step 3: Exporting assembly drawing to PDF...")
    pdf_path = os.path.join(output_dir, 'assembly_drawing.pdf')
    export_assembly_drawing_pdf(
        top_frame_profile, bottom_tray_profile, pdf_path,
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        top_frame_height=TOP_FRAME_HEIGHT,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        mounting_holes=MOUNTING_HOLES
    )
    print()
    
    # Display assembly information
    print("Assembly Information:")
    print("-" * 70)
    print("Components:")
    print(f"  - Top Frame: {CASE_LENGTH}mm × {CASE_WIDTH}mm × {TOP_FRAME_HEIGHT}mm")
    print(f"  - Bottom Tray: {CASE_LENGTH}mm × {CASE_WIDTH}mm × {BOTTOM_TRAY_HEIGHT}mm")
    print()
    
    print("Hardware Required:")
    print("  - Brass Inserts: 6× M3 × 5.7mm OD × 4mm length")
    print("  - M2 Screws: 6× M2 × 8mm pan head (PCB mounting)")
    print("  - M3 Screws: 6× M3 × 12mm flat head (case assembly)")
    print("  - Rubber Feet: 4× 8mm diameter adhesive bumpers")
    print()
    
    print("Assembly Sequence:")
    print("  1. Install brass inserts into top frame")
    print("  2. Mount PCB to bottom tray with M2 screws")
    print("  3. Attach top frame with M3 screws from bottom")
    print("  4. Install rubber feet in corner recesses")
    print()
    
    print("=" * 70)
    print("Output Files:")
    print(f"  PDF: {pdf_path}")
    print()
    print("✓ Task 6.3 Complete: Assembly drawing generated")
    print()
    print("All Task 6 subtasks complete!")
    print("  ✓ 6.1: Top frame technical drawing")
    print("  ✓ 6.2: Bottom tray technical drawing")
    print("  ✓ 6.3: Assembly drawing")
    print()
    print("Next Steps:")
    print("  - Review all drawings for accuracy")
    print("  - Proceed to Task 7: Export CNC toolpath files")
    print("=" * 70)


if __name__ == '__main__':
    main()
