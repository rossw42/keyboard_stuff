"""
Example script to generate CNC toolpaths for bottom tray component.

This script demonstrates how to generate all toolpath operations
for the bottom tray of the 60% keyboard case.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.constants import *
from src.geometry.profiles import generate_bottom_tray_profile
from src.toolpaths.bottom_tray import generate_bottom_tray_toolpaths
import json


def main():
    """Generate bottom tray toolpaths and display summary."""
    
    print("=" * 80)
    print("60% Keyboard Case - Bottom Tray CNC Toolpath Generation")
    print("=" * 80)
    print()
    
    # Generate bottom tray geometry
    print("Generating bottom tray 2D profile geometry...")
    bottom_tray_geometry = generate_bottom_tray_profile(
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
    print("✓ Bottom tray geometry generated")
    print()
    
    # Generate toolpaths
    print("Generating CNC toolpaths...")
    toolpaths = generate_bottom_tray_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=bottom_tray_geometry['external_profile'],
        internal_cavity_profile=bottom_tray_geometry['internal_cavity'],
        standoff_pillars=bottom_tray_geometry['standoff_pillars'],
        mounting_holes=MOUNTING_HOLES,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        cavity_depth=CAVITY_DEPTH
    )
    print("✓ Toolpaths generated")
    print()
    
    # Display summary
    print("=" * 80)
    print("TOOLPATH SUMMARY")
    print("=" * 80)
    print()
    
    summary = toolpaths['summary']
    setup = toolpaths['setup']
    
    print(f"Component: {toolpaths['component'].upper()}")
    print(f"Total Operations: {summary['total_operations']}")
    print(f"Workpiece Flips Required: {summary['workpiece_flips']}")
    print()
    
    print("Stock Dimensions:")
    print(f"  Length: {setup['stock_dimensions']['length']}mm")
    print(f"  Width: {setup['stock_dimensions']['width']}mm")
    print(f"  Thickness: {setup['stock_dimensions']['thickness']}mm")
    print()
    
    print("Tools Required:")
    for tool in summary['tools_required']:
        print(f"  • {tool}")
    print()
    
    print("=" * 80)
    print("OPERATIONS SEQUENCE")
    print("=" * 80)
    print()
    
    for op_name, op_data in toolpaths['operations'].items():
        op_num = op_name.split('_')[0]
        op_title = ' '.join(op_name.split('_')[1:]).title()
        
        print(f"{op_num}. {op_title}")
        print(f"   Operation: {op_data['operation']}")
        
        # Handle different operation structures
        if 'tool' in op_data:
            tool = op_data['tool']
            params = op_data['parameters']
            print(f"   Tool: {tool['description']}")
            print(f"   Diameter: {tool['diameter']}mm")
            
            if 'depth' in params:
                print(f"   Depth: {params['depth']}mm")
            if 'feed_rate' in params:
                print(f"   Feed Rate: {params['feed_rate']}mm/min")
            if 'spindle_speed' in params:
                print(f"   Spindle Speed: {params['spindle_speed']}RPM")
            
            if 'count' in op_data:
                print(f"   Count: {op_data['count']} locations")
        
        elif 'roughing' in op_data and 'finishing' in op_data:
            # Two-stage operation
            rough = op_data['roughing']
            finish = op_data['finishing']
            
            print(f"   Roughing Tool: {rough['tool']['description']}")
            print(f"   Finishing Tool: {finish['tool']['description']}")
            print(f"   Depth: {rough['parameters']['depth']}mm")
            print(f"   Stock to Leave: {rough['parameters']['stock_to_leave']}mm")
        
        print()
    
    print("=" * 80)
    print("SETUP NOTES")
    print("=" * 80)
    print()
    
    for note in setup['notes']:
        print(f"  • {note}")
    print()
    
    print("=" * 80)
    print("TOLERANCES")
    print("=" * 80)
    print()
    
    print("Critical Tolerances (±0.1mm):")
    for tol in summary['critical_tolerances']:
        print(f"  • {tol}")
    print()
    
    print("Standard Tolerances (±0.2mm):")
    for tol in summary['standard_tolerances']:
        print(f"  • {tol}")
    print()
    
    # Save toolpaths to JSON file
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', '60_percent_standard', 'cnc', 'toolpaths')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'bottom_tray_toolpaths.json')
    
    # Convert toolpaths to JSON-serializable format
    def convert_to_serializable(obj):
        """Convert numpy arrays and tuples to lists for JSON serialization."""
        if isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return list(obj)
        else:
            return obj
    
    serializable_toolpaths = convert_to_serializable(toolpaths)
    
    with open(output_file, 'w') as f:
        json.dump(serializable_toolpaths, f, indent=2)
    
    print(f"✓ Toolpaths saved to: {output_file}")
    print()
    
    print("=" * 80)
    print("Generation complete!")
    print("=" * 80)


if __name__ == '__main__':
    main()
