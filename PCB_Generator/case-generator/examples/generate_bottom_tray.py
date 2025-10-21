#!/usr/bin/env python3
"""
Example script to generate bottom tray 2D profile geometry.

This demonstrates how to use the geometry module to create all the
2D profiles needed for CNC machining the bottom tray component.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from constants import (
    CASE_LENGTH, CASE_WIDTH, CASE_CORNER_RADIUS,
    CAVITY_LENGTH, CAVITY_WIDTH, CAVITY_CORNER_RADIUS, WALL_THICKNESS,
    MOUNTING_HOLES,
    STANDOFF_DIAMETER, STANDOFF_HOLE_DIAMETER,
    ASSEMBLY_SCREW_DIAMETER, ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
    RUBBER_FEET_POSITIONS, RUBBER_FEET_DIAMETER,
    BOTTOM_TRAY_HEIGHT, CAVITY_DEPTH
)
from geometry import generate_bottom_tray_profile


def main():
    """Generate and display bottom tray profile geometry."""
    
    print("=" * 60)
    print("60% Keyboard Case - Bottom Tray Profile Generation")
    print("=" * 60)
    print()
    
    # Generate complete bottom tray profile
    print("Generating bottom tray 2D profile geometry...")
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
    print("✓ Profile generation complete\n")
    
    # Display summary
    print("Profile Summary:")
    print("-" * 60)
    print(f"Component: Bottom Tray")
    print(f"Height: {BOTTOM_TRAY_HEIGHT}mm")
    print(f"Cavity Depth: {CAVITY_DEPTH}mm")
    print()
    
    print(f"External Profile:")
    print(f"  - Dimensions: {CASE_LENGTH}mm × {CASE_WIDTH}mm")
    print(f"  - Corner radius: {CASE_CORNER_RADIUS}mm")
    print(f"  - Points: {len(profile['external_profile'])}")
    print(f"  - Matches top frame: Yes")
    print()
    
    print(f"Internal Cavity:")
    print(f"  - Dimensions: {CAVITY_LENGTH}mm × {CAVITY_WIDTH}mm")
    print(f"  - Depth: {CAVITY_DEPTH}mm")
    print(f"  - Wall thickness: {WALL_THICKNESS}mm")
    print(f"  - Corner radius: {CAVITY_CORNER_RADIUS}mm (4mm endmill)")
    print(f"  - Points: {len(profile['internal_cavity'])}")
    print()
    
    print(f"PCB Standoff Pillars:")
    print(f"  - Count: {len(profile['standoff_pillars'])}")
    print(f"  - Diameter: {STANDOFF_DIAMETER}mm")
    print(f"  - Positions:")
    for pillar_id, position in MOUNTING_HOLES.items():
        print(f"    {pillar_id}: ({position[0]:.1f}mm, {position[1]:.1f}mm)")
    print()
    
    print(f"Standoff Through-Holes (M2):")
    print(f"  - Count: {len(profile['standoff_holes'])}")
    print(f"  - Diameter: {STANDOFF_HOLE_DIAMETER}mm")
    print(f"  - Purpose: M2 screw clearance for PCB mounting")
    print()
    
    print(f"Assembly Screw Holes (M3):")
    print(f"  - Count: {len(profile['assembly_screw_holes'])}")
    print(f"  - Diameter: {ASSEMBLY_SCREW_DIAMETER}mm")
    print(f"  - Purpose: M3 screw clearance for case assembly")
    print()
    
    print(f"Assembly Screw Counterbores:")
    print(f"  - Count: {len(profile['assembly_counterbores'])}")
    print(f"  - Diameter: {ASSEMBLY_SCREW_COUNTERBORE_DIAMETER}mm")
    print(f"  - Depth: 3mm (from bottom surface)")
    print()
    
    print(f"Rubber Feet Recesses:")
    print(f"  - Count: {len(profile['rubber_feet_recesses'])}")
    print(f"  - Diameter: {RUBBER_FEET_DIAMETER}mm")
    print(f"  - Depth: 2mm")
    print(f"  - Positions:")
    for i, position in enumerate(RUBBER_FEET_POSITIONS, 1):
        corner = ["Top-left", "Top-right", "Bottom-left", "Bottom-right"][i-1]
        print(f"    {corner}: ({position[0]:.1f}mm, {position[1]:.1f}mm)")
    print()
    
    print("=" * 60)
    print("Next steps:")
    print("  1. Export profiles to DXF format (Task 6)")
    print("  2. Generate CNC toolpaths (Task 5)")
    print("  3. Create 3D reference model (Task 9)")
    print("=" * 60)


if __name__ == '__main__':
    main()
