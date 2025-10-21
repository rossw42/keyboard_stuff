#!/usr/bin/env python3
"""
Export top frame technical drawing with dimensions.

This script generates a DXF technical drawing of the top frame component
with all critical dimensions labeled and tolerance callouts.

Task 6.1: Generate top frame technical drawing with dimensions
Requirements: 8.1, 8.2, 8.3
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
    MOUNTING_HOLES, BRASS_INSERT_DIAMETER,
    TOP_FRAME_HEIGHT, TOLERANCE_CRITICAL, TOLERANCE_STANDARD
)
from geometry import generate_top_frame_profile
from export.technical_drawings import export_top_frame_dxf, export_top_frame_pdf


def main():
    """Generate and export top frame technical drawing."""
    
    print("=" * 70)
    print("Task 6.1: Generate Top Frame Technical Drawing")
    print("=" * 70)
    print()
    
    # Generate top frame profile geometry
    print("Step 1: Generating top frame 2D profile geometry...")
    profile = generate_top_frame_profile(
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
    print("✓ Profile generation complete")
    print()
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', '60_percent_standard', 'cnc', 'drawings')
    os.makedirs(output_dir, exist_ok=True)
    
    # Export to DXF
    print("Step 2: Exporting to DXF format...")
    dxf_path = os.path.join(output_dir, 'top_frame_technical_drawing.dxf')
    export_top_frame_dxf(profile, dxf_path)
    print()
    
    # Export to PDF
    print("Step 3: Exporting to PDF format...")
    pdf_path = os.path.join(output_dir, 'top_frame_technical_drawing.pdf')
    export_top_frame_pdf(
        profile, pdf_path,
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        pcb_opening_length=PCB_OPENING_LENGTH,
        pcb_opening_width=PCB_OPENING_WIDTH,
        usb_cutout_width=USB_CUTOUT_WIDTH,
        usb_cutout_height=USB_CUTOUT_HEIGHT,
        brass_insert_diameter=BRASS_INSERT_DIAMETER,
        top_frame_height=TOP_FRAME_HEIGHT,
        tolerance_critical=TOLERANCE_CRITICAL,
        tolerance_standard=TOLERANCE_STANDARD,
        mounting_holes=MOUNTING_HOLES
    )
    print()
    
    # Display drawing information
    print("Drawing Information:")
    print("-" * 70)
    print(f"Component: Top Frame")
    print(f"Height: {TOP_FRAME_HEIGHT}mm")
    print()
    
    print("Critical Dimensions (±{:.1f}mm tolerance):".format(TOLERANCE_CRITICAL))
    print(f"  - PCB Opening: {PCB_OPENING_LENGTH}mm × {PCB_OPENING_WIDTH}mm")
    print(f"  - Brass Insert Holes: Ø{BRASS_INSERT_DIAMETER}mm (6 locations)")
    print(f"  - Mounting Hole Positions:")
    for hole_id, (x, y) in MOUNTING_HOLES.items():
        print(f"    {hole_id}: ({x:.1f}mm, {y:.1f}mm)")
    print()
    
    print("Standard Dimensions (±{:.1f}mm tolerance):".format(TOLERANCE_STANDARD))
    print(f"  - External: {CASE_LENGTH}mm × {CASE_WIDTH}mm")
    print(f"  - Corner Radius: {CASE_CORNER_RADIUS}mm")
    print(f"  - USB Cutout: {USB_CUTOUT_WIDTH}mm × {USB_CUTOUT_HEIGHT}mm")
    print(f"  - USB Position: Centered at ({USB_CUTOUT_CENTER_X:.1f}mm, {USB_CUTOUT_CENTER_Y:.1f}mm)")
    print()
    
    print("Layer Information:")
    print("  - EXTERNAL: External profile (white)")
    print("  - PCB_OPENING: PCB opening pocket (cyan)")
    print("  - USB_CUTOUT: USB port cutout (green)")
    print("  - BRASS_INSERTS: Brass insert holes (yellow)")
    print("  - DIMENSIONS: Dimension lines (red)")
    print("  - TEXT: Annotations and notes (white)")
    print()
    
    print("=" * 70)
    print("Output Files:")
    print(f"  DXF: {dxf_path}")
    print(f"  PDF: {pdf_path}")
    print()
    print("✓ Task 6.1 Complete: Top frame technical drawing generated")
    print()
    print("Next Steps:")
    print("  - Review DXF in CAD software (AutoCAD, LibreCAD, QCAD)")
    print("  - Review PDF for documentation and manufacturing")
    print("  - Proceed to Task 6.2: Bottom tray technical drawing")
    print("=" * 70)


if __name__ == '__main__':
    main()
