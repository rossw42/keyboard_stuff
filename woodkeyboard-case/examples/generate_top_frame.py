#!/usr/bin/env python3
"""
Example script to generate top frame 2D profile geometry.

This demonstrates how to use the geometry module to create all the
2D profiles needed for CNC machining the top frame component.
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
    TOP_FRAME_HEIGHT
)
from geometry import generate_top_frame_profile


def main():
    """Generate and display top frame profile geometry."""
    
    print("=" * 60)
    print("60% Keyboard Case - Top Frame Profile Generation")
    print("=" * 60)
    print()
    
    # Generate complete top frame profile
    print("Generating top frame 2D profile geometry...")
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
    print("✓ Profile generation complete\n")
    
    # Display summary
    print("Profile Summary:")
    print("-" * 60)
    print(f"Component: Top Frame")
    print(f"Height: {TOP_FRAME_HEIGHT}mm")
    print()
    
    print(f"External Profile:")
    print(f"  - Dimensions: {CASE_LENGTH}mm × {CASE_WIDTH}mm")
    print(f"  - Corner radius: {CASE_CORNER_RADIUS}mm")
    print(f"  - Points: {len(profile['external_profile'])}")
    print()
    
    print(f"PCB Opening:")
    print(f"  - Dimensions: {PCB_OPENING_LENGTH}mm × {PCB_OPENING_WIDTH}mm")
    print(f"  - Border: {PCB_BORDER}mm (all sides)")
    print(f"  - Clearance: 0.5mm per side around PCB")
    print(f"  - Points: {len(profile['pcb_opening'])}")
    print()
    
    print(f"USB Port Cutout:")
    print(f"  - Dimensions: {USB_CUTOUT_WIDTH}mm × {USB_CUTOUT_HEIGHT}mm")
    print(f"  - Position: Centered at ({USB_CUTOUT_CENTER_X}mm, {USB_CUTOUT_CENTER_Y}mm)")
    print(f"  - Corner radius: {USB_CUTOUT_CORNER_RADIUS}mm")
    print(f"  - Points: {len(profile['usb_cutout'])}")
    print()
    
    print(f"Brass Insert Holes:")
    print(f"  - Count: {len(profile['brass_insert_holes'])}")
    print(f"  - Diameter: {BRASS_INSERT_DIAMETER}mm")
    print(f"  - Positions:")
    for hole_id, position in MOUNTING_HOLES.items():
        print(f"    {hole_id}: ({position[0]:.1f}mm, {position[1]:.1f}mm)")
    print()
    
    print("=" * 60)
    print("Next steps:")
    print("  1. Export profiles to DXF format (Task 6)")
    print("  2. Generate CNC toolpaths (Task 4)")
    print("  3. Create 3D reference model (Task 9)")
    print("=" * 60)


if __name__ == '__main__':
    main()
