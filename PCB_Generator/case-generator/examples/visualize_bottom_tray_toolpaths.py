"""
Example script to visualize bottom tray CNC toolpaths.

This script generates a simple ASCII visualization of the bottom tray
toolpath operations to help understand the machining sequence.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.constants import *
from src.geometry.profiles import generate_bottom_tray_profile
from src.toolpaths.bottom_tray import generate_bottom_tray_toolpaths


def visualize_operation_sequence():
    """Display a visual representation of the machining sequence."""
    
    print("=" * 80)
    print("BOTTOM TRAY MACHINING SEQUENCE VISUALIZATION")
    print("=" * 80)
    print()
    
    print("Stock: 295mm x 105mm x 20mm hardwood")
    print("Final: 295mm x 105mm x 15mm")
    print()
    
    print("SIDE VIEW (Cross-section):")
    print()
    print("  Top Surface")
    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │                                                         │ ← 0.5mm surfacing")
    print("  │                                                         │")
    print("  │         ┌───────────────────────────────┐             │")
    print("  │         │  8mm Cavity                   │             │")
    print("  │         │   ┌─┐    ┌─┐    ┌─┐          │             │")
    print("  │         │   │S│    │S│    │S│  Standoffs│             │ ← 15mm total")
    print("  │         └───┴─┴────┴─┴────┴─┴───────────┘             │   height")
    print("  │           ╱                                ╲           │")
    print("  │          ╱  Counterbores (3mm deep)        ╲          │")
    print("  │         ●                                    ●         │")
    print("  └─────────────────────────────────────────────────────────┘")
    print("    ●                                                    ●")
    print("    └─ Rubber feet recesses (2mm deep)                  ┘")
    print()
    
    print("TOP VIEW:")
    print()
    print("  ┌───────────────────────────────────────────────────────┐")
    print("  │ ●                                                 ●   │ ← Rubber feet")
    print("  │                                                       │")
    print("  │    ┌─────────────────────────────────────────┐       │")
    print("  │    │  Internal Cavity (287mm x 96.6mm)       │       │")
    print("  │    │                                          │       │")
    print("  │    │   ○      ○                    ○      ○   │       │ ← Standoff")
    print("  │    │                                          │       │   pillars")
    print("  │    │          ○                    ○          │       │   (6mm dia)")
    print("  │    │                                          │       │")
    print("  │    └─────────────────────────────────────────┘       │")
    print("  │                                                       │")
    print("  │ ●                                                 ●   │")
    print("  └───────────────────────────────────────────────────────┘")
    print("    295mm x 105mm external dimensions")
    print()
    
    print("MACHINING SEQUENCE:")
    print()
    
    operations = [
        ("1", "Face Surfacing", "Top surface", "6mm endmill", "0.5mm depth"),
        ("", ">>> FLIP WORKPIECE <<<", "", "", ""),
        ("2", "Rubber Feet Recesses", "Bottom surface", "10mm endmill", "2mm depth, 4 corners"),
        ("3", "Assembly Counterbores", "Bottom surface", "6mm endmill", "3mm depth, 6 locations"),
        ("", ">>> FLIP WORKPIECE <<<", "", "", ""),
        ("4", "Assembly Through-Holes", "Top surface", "3.2mm drill", "15mm depth, 6 locations"),
        ("5", "Internal Cavity Pocket", "Top surface", "6mm + 4mm endmill", "8mm depth with pillars"),
        ("6", "Standoff Through-Holes", "Top surface", "2.2mm drill", "6mm depth, 6 locations"),
        ("7", "External Profile", "Top surface", "6mm + 3mm endmill", "15mm depth with tabs"),
    ]
    
    for op in operations:
        if op[0] == "":
            print(f"\n  {op[1]}\n")
        else:
            print(f"  {op[0]}. {op[1]:<30} {op[2]:<15} {op[3]:<20} {op[4]}")
    
    print()
    print("=" * 80)
    print()


def display_toolpath_details():
    """Display detailed toolpath information."""
    
    # Generate geometry
    geometry = generate_bottom_tray_profile(
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
    
    # Generate toolpaths
    toolpaths = generate_bottom_tray_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=geometry['external_profile'],
        internal_cavity_profile=geometry['internal_cavity'],
        standoff_pillars=geometry['standoff_pillars'],
        mounting_holes=MOUNTING_HOLES,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        cavity_depth=CAVITY_DEPTH
    )
    
    print("CRITICAL FEATURES:")
    print()
    print("  Standoff Pillars:")
    print("    • Count: 6")
    print("    • Diameter: 6mm")
    print("    • Height: 3mm from cavity floor")
    print("    • Through-hole: 2.2mm (M2 screw clearance)")
    print("    • Tolerance: ±0.1mm (critical)")
    print()
    
    print("  Assembly System:")
    print("    • M3 screws from bottom into brass inserts in top frame")
    print("    • Counterbore: 6mm diameter x 3mm deep")
    print("    • Through-hole: 3.2mm diameter x 15mm deep")
    print("    • 6 locations matching PCB mounting holes")
    print()
    
    print("  Cavity Pocket:")
    print("    • Dimensions: 287mm x 96.6mm x 8mm deep")
    print("    • Wall thickness: 4mm")
    print("    • Corner radius: 2mm (limited by 4mm finishing tool)")
    print("    • Standoff pillars preserved as islands")
    print()
    
    print("  Rubber Feet:")
    print("    • Count: 4 (one per corner)")
    print("    • Recess: 10mm diameter x 2mm deep")
    print("    • Position: 10mm from each corner")
    print("    • For 8mm adhesive rubber feet")
    print()
    
    print("=" * 80)
    print()


def main():
    """Main visualization function."""
    visualize_operation_sequence()
    display_toolpath_details()
    
    print("TIP: Run 'python examples/generate_bottom_tray_toolpaths.py' for")
    print("     detailed toolpath data and JSON export.")
    print()


if __name__ == '__main__':
    main()
