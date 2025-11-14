#!/usr/bin/env python3
"""
Export bottom tray technical drawing with dimensions.

This script generates DXF and PDF technical drawings of the bottom tray component
with all critical dimensions labeled and tolerance callouts.

Task 6.2: Generate bottom tray technical drawing with dimensions
Requirements: 8.1, 8.2, 8.3
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from constants import (
    CASE_LENGTH, CASE_WIDTH, CASE_CORNER_RADIUS,
    CAVITY_LENGTH, CAVITY_WIDTH, CAVITY_CORNER_RADIUS, CAVITY_DEPTH, WALL_THICKNESS,
    MOUNTING_HOLES,
    STANDOFF_DIAMETER, STANDOFF_HOLE_DIAMETER,
    ASSEMBLY_SCREW_DIAMETER, ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
    RUBBER_FEET_POSITIONS, RUBBER_FEET_DIAMETER,
    BOTTOM_TRAY_HEIGHT, TOLERANCE_CRITICAL, TOLERANCE_STANDARD
)
from geometry import generate_bottom_tray_profile
from export.technical_drawings import export_bottom_tray_dxf, export_bottom_tray_pdf


def main():
    """Generate and export bottom tray technical drawing."""
    
    print("=" * 70)
    print("Task 6.2: Generate Bottom Tray Technical Drawing")
    print("=" * 70)
    print()
    
    # Generate bottom tray profile geometry
    print("Step 1: Generating bottom tray 2D profile geometry...")
    profile = generate_bottom_tray_profile(
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
    print("✓ Profile generation complete")
    print()
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', '60_percent_standard', 'cnc', 'drawings')
    os.makedirs(output_dir, exist_ok=True)
    
    # Export to DXF
    print("Step 2: Exporting to DXF format...")
    dxf_path = os.path.join(output_dir, 'bottom_tray_technical_drawing.dxf')
    export_bottom_tray_dxf(profile, dxf_path)
    print()
    
    # Export to PDF
    print("Step 3: Exporting to PDF format...")
    pdf_path = os.path.join(output_dir, 'bottom_tray_technical_drawing.pdf')
    export_bottom_tray_pdf(
        profile, pdf_path,
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        cavity_length=CAVITY_LENGTH,
        cavity_width=CAVITY_WIDTH,
        cavity_depth=CAVITY_DEPTH,
        wall_thickness=WALL_THICKNESS,
        standoff_diameter=STANDOFF_DIAMETER,
        standoff_hole_diameter=STANDOFF_HOLE_DIAMETER,
        assembly_screw_diameter=ASSEMBLY_SCREW_DIAMETER,
        assembly_counterbore_diameter=ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
        rubber_feet_diameter=RUBBER_FEET_DIAMETER,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        tolerance_critical=TOLERANCE_CRITICAL,
        tolerance_standard=TOLERANCE_STANDARD,
        mounting_holes=MOUNTING_HOLES,
        rubber_feet_positions=RUBBER_FEET_POSITIONS
    )
    print()
    
    # Display drawing information
    print("Drawing Information:")
    print("-" * 70)
    print(f"Component: Bottom Tray")
    print(f"Height: {BOTTOM_TRAY_HEIGHT}mm")
    print(f"Cavity Depth: {CAVITY_DEPTH}mm")
    print()
    
    print("Critical Dimensions (±{:.1f}mm tolerance):".format(TOLERANCE_CRITICAL))
    print(f"  - Standoff Pillars: Ø{STANDOFF_DIAMETER}mm (6 locations)")
    print(f"  - Standoff Holes: Ø{STANDOFF_HOLE_DIAMETER}mm (M2 clearance)")
    print(f"  - Mounting Positions:")
    for hole_id, (x, y) in MOUNTING_HOLES.items():
        print(f"    {hole_id}: ({x:.1f}mm, {y:.1f}mm)")
    print()
    
    print("Standard Dimensions (±{:.1f}mm tolerance):".format(TOLERANCE_STANDARD))
    print(f"  - External: {CASE_LENGTH}mm × {CASE_WIDTH}mm")
    print(f"  - Cavity: {CAVITY_LENGTH}mm × {CAVITY_WIDTH}mm × {CAVITY_DEPTH}mm deep")
    print(f"  - Wall Thickness: {WALL_THICKNESS}mm")
    print(f"  - Assembly Screws: Ø{ASSEMBLY_SCREW_DIAMETER}mm (M3 clearance)")
    print(f"  - Counterbores: Ø{ASSEMBLY_SCREW_COUNTERBORE_DIAMETER}mm × 3mm deep")
    print(f"  - Rubber Feet: Ø{RUBBER_FEET_DIAMETER}mm × 2mm deep (4 corners)")
    print()
    
    print("Layer Information:")
    print("  - EXTERNAL: External profile (white)")
    print("  - CAVITY: Internal cavity (cyan)")
    print("  - STANDOFF_PILLARS: PCB standoff pillars (green)")
    print("  - STANDOFF_HOLES: M2 screw holes (yellow)")
    print("  - ASSEMBLY_SCREWS: M3 screw holes (magenta)")
    print("  - COUNTERBORES: Screw counterbores (red)")
    print("  - RUBBER_FEET: Rubber feet recesses (blue)")
    print("  - DIMENSIONS: Dimension lines (red)")
    print("  - TEXT: Annotations and notes (white)")
    print()
    
    print("=" * 70)
    print("Output Files:")
    print(f"  DXF: {dxf_path}")
    print(f"  PDF: {pdf_path}")
    print()
    print("✓ Task 6.2 Complete: Bottom tray technical drawing generated")
    print()
    print("Next Steps:")
    print("  - Review DXF in CAD software (AutoCAD, LibreCAD, QCAD)")
    print("  - Review PDF for documentation and manufacturing")
    print("  - Proceed to Task 6.3: Assembly drawing with hardware callouts")
    print("=" * 70)


if __name__ == '__main__':
    main()
