"""
Generate CNC setup sheets for both components.

This script generates comprehensive setup sheets with workpiece specifications,
work holding instructions, origin positioning, safety notes, and quality checkpoints.

Requirements: 6.2, 8.5
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.constants import (
    CASE_LENGTH, CASE_WIDTH, TOP_FRAME_HEIGHT, BOTTOM_TRAY_HEIGHT,
    MOUNTING_HOLES, RUBBER_FEET_POSITIONS
)
from src.geometry.profiles import (
    generate_external_profile,
    generate_pcb_opening,
    generate_usb_cutout,
    generate_internal_cavity,
    generate_standoff_pillars
)
from src.toolpaths.top_frame import generate_top_frame_toolpaths
from src.toolpaths.bottom_tray import generate_bottom_tray_toolpaths
from src.export.setup_sheets import generate_setup_sheets


def main():
    """Generate setup sheets for both components."""
    print("Generating toolpaths for setup sheets...")
    
    # Generate top frame toolpaths
    external_profile = generate_external_profile(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        corner_radius=3.0
    )
    
    pcb_opening_profile = generate_pcb_opening(
        opening_length=286.0,
        opening_width=95.6,
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        border=4.5
    )
    
    usb_cutout_profile = generate_usb_cutout(
        cutout_width=16.0,
        cutout_height=10.0,
        corner_radius=1.0,
        center_x=CASE_LENGTH / 2.0,
        center_y=4.5 + 7.0
    )
    
    top_frame_toolpaths = generate_top_frame_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=external_profile,
        pcb_opening_profile=pcb_opening_profile,
        usb_cutout_profile=usb_cutout_profile,
        mounting_holes=MOUNTING_HOLES,
        top_frame_height=TOP_FRAME_HEIGHT
    )
    
    # Generate bottom tray toolpaths
    cavity_profile = generate_internal_cavity(
        cavity_length=287.0,
        cavity_width=96.6,
        corner_radius=2.0,
        wall_thickness=4.0
    )
    
    standoff_pillars = generate_standoff_pillars(
        mounting_holes=MOUNTING_HOLES,
        pillar_diameter=6.0
    )
    
    bottom_tray_toolpaths = generate_bottom_tray_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=external_profile,
        internal_cavity_profile=cavity_profile,
        standoff_pillars=standoff_pillars,
        mounting_holes=MOUNTING_HOLES,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        cavity_depth=8.0
    )
    
    print("Generating setup sheets...")
    
    # Generate setup sheets
    filepaths = generate_setup_sheets(
        top_frame_toolpaths=top_frame_toolpaths,
        bottom_tray_toolpaths=bottom_tray_toolpaths
    )
    
    print("\nSetup sheets generated:")
    for component, filepath in filepaths.items():
        print(f"  {component}: {filepath}")


if __name__ == "__main__":
    main()
