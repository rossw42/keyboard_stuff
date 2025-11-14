"""
Example script to generate CNC toolpaths for top frame component - LOW-PROFILE VARIANT.

This script demonstrates the complete toolpath generation workflow
for the low-profile top frame (3mm height vs 5mm standard).
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.constants_lp import (
    CASE_LENGTH, CASE_WIDTH, CASE_CORNER_RADIUS,
    PCB_OPENING_LENGTH, PCB_OPENING_WIDTH, PCB_BORDER,
    USB_CUTOUT_WIDTH, USB_CUTOUT_HEIGHT, USB_CUTOUT_CORNER_RADIUS,
    USB_CUTOUT_CENTER_X, USB_CUTOUT_CENTER_Y,
    MOUNTING_HOLES, BRASS_INSERT_DIAMETER,
    TOP_FRAME_HEIGHT
)
from src.geometry.profiles_lp import (
    generate_top_frame_profile
)
from src.toolpaths.top_frame import (
    generate_top_frame_toolpaths
)
import json


def main():
    """Generate and display low-profile top frame toolpaths."""
    
    print("=" * 80)
    print("LOW-PROFILE TOP FRAME CNC TOOLPATH GENERATION")
    print("=" * 80)
    print(f"Height: {TOP_FRAME_HEIGHT}mm (LOW-PROFILE: reduced from 5mm standard)")
    print()
    
    # Step 1: Generate 2D geometry profiles
    print("Step 1: Generating 2D geometry profiles...")
    profiles = generate_top_frame_profile(
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
    print(f"  ✓ External profile: {len(profiles['external_profile'])} points")
    print(f"  ✓ PCB opening: {len(profiles['pcb_opening'])} points")
    print(f"  ✓ USB cutout: {len(profiles['usb_cutout'])} points")
    print(f"  ✓ Brass insert holes: {len(profiles['brass_insert_holes'])} locations")
    print()
    
    # Step 2: Generate CNC toolpaths
    print("Step 2: Generating CNC toolpaths...")
    toolpaths = generate_top_frame_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=profiles['external_profile'],
        pcb_opening_profile=profiles['pcb_opening'],
        usb_cutout_profile=profiles['usb_cutout'],
        mounting_holes=MOUNTING_HOLES,
        top_frame_height=TOP_FRAME_HEIGHT
    )
    print(f"  ✓ Generated {toolpaths['summary']['total_operations']} operations")
    print()
    
    # Step 3: Display operation summary
    print("Step 3: Operation Summary")
    print("-" * 80)
    
    for op_name, op_data in toolpaths['operations'].items():
        print(f"\n{op_name.replace('_', ' ').title()}:")
        print(f"  Operation: {op_data['operation']}")
        
        # Handle operations with single tool
        if 'tool' in op_data:
            tool = op_data['tool']
            params = op_data['parameters']
            print(f"  Tool: {tool['diameter']}mm {tool['type']}")
            print(f"  Depth: {params.get('depth', 'N/A')}mm")
            print(f"  Feed Rate: {params.get('feed_rate', 'N/A')} mm/min")
            print(f"  Spindle Speed: {params.get('spindle_speed', 'N/A')} RPM")
            
            if 'estimated_time_minutes' in op_data:
                print(f"  Est. Time: {op_data['estimated_time_minutes']} minutes")
        
        # Handle operations with roughing and finishing
        elif 'roughing' in op_data and 'finishing' in op_data:
            print("  Roughing:")
            rough_tool = op_data['roughing']['tool']
            rough_params = op_data['roughing']['parameters']
            print(f"    Tool: {rough_tool['diameter']}mm {rough_tool['type']}")
            print(f"    Feed Rate: {rough_params['feed_rate']} mm/min")
            
            print("  Finishing:")
            finish_tool = op_data['finishing']['tool']
            finish_params = op_data['finishing']['parameters']
            print(f"    Tool: {finish_tool['diameter']}mm {finish_tool['type']}")
            print(f"    Feed Rate: {finish_params['feed_rate']} mm/min")
        
        # Handle brass insert counterbores
        elif 'toolpaths' in op_data and isinstance(op_data['toolpaths'], dict):
            tool = op_data['tool']
            params = op_data['parameters']
            print(f"  Tool: {tool['diameter']}mm {tool['type']}")
            print(f"  Target Diameter: {params['target_diameter']}mm")
            print(f"  Depth: {params['depth']}mm (LOW-PROFILE: full {TOP_FRAME_HEIGHT}mm thickness)")
            print(f"  Count: {op_data['count']} holes")
    
    print()
    print("-" * 80)
    print("\nSetup Information:")
    print(f"  Material: {toolpaths['setup']['material']}")
    print(f"  Stock: {toolpaths['setup']['stock_dimensions']['length']}mm × "
          f"{toolpaths['setup']['stock_dimensions']['width']}mm × "
          f"{toolpaths['setup']['stock_dimensions']['thickness']}mm")
    print(f"  Work Holding: {toolpaths['setup']['work_holding']}")
    print(f"  Origin: {toolpaths['setup']['origin']}")
    
    print("\nTools Required:")
    for tool in toolpaths['summary']['tools_required']:
        print(f"  • {tool}")
    
    print("\nTolerances:")
    print("  Critical (±0.1mm):")
    for tol in toolpaths['summary']['critical_tolerances']:
        print(f"    • {tol}")
    print("  Standard (±0.2mm):")
    for tol in toolpaths['summary']['standard_tolerances']:
        print(f"    • {tol}")
    
    if toolpaths['summary']['estimated_time_minutes'] > 0:
        print(f"\nEstimated Total Time: {toolpaths['summary']['estimated_time_minutes']} minutes")
    
    print()
    print("=" * 80)
    print("LOW-PROFILE TOOLPATH GENERATION COMPLETE")
    print("=" * 80)
    print(f"\nLow-Profile Specifications:")
    print(f"  Top Frame Height: {TOP_FRAME_HEIGHT}mm (vs 5mm standard)")
    print(f"  Brass Insert Depth: {TOP_FRAME_HEIGHT}mm (full thickness)")
    print(f"  USB Cutout Height: {USB_CUTOUT_HEIGHT}mm (vs 10mm standard)")
    print()
    
    # Optional: Save to JSON file
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', '60_percent_low_profile', 'cnc', 'toolpaths')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'top_frame_toolpaths_lp.json')
    
    # Convert toolpaths to JSON-serializable format
    def make_serializable(obj):
        """Convert numpy arrays and other non-serializable objects to lists."""
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return list(obj)
        else:
            return obj
    
    serializable_toolpaths = make_serializable(toolpaths)
    
    with open(output_file, 'w') as f:
        json.dump(serializable_toolpaths, f, indent=2)
    print(f"Toolpaths saved to: {output_file}")
    print()


if __name__ == '__main__':
    main()
