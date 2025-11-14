"""
Export top frame CNC toolpaths to DXF files.

This script generates and exports all top frame toolpath operations
as separate DXF files for use with CAM software.

Requirements: 6.1, 8.2
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.constants import (
    CASE_LENGTH, CASE_WIDTH, TOP_FRAME_HEIGHT,
    MOUNTING_HOLES
)
from src.geometry.profiles import (
    generate_external_profile,
    generate_pcb_opening,
    generate_usb_cutout
)
from src.toolpaths.top_frame import generate_top_frame_toolpaths
from src.export.toolpath_dxf import export_top_frame_toolpaths_to_dxf


def main():
    """Generate and export top frame toolpaths to DXF."""
    print("Generating top frame toolpaths...")
    
    # Generate geometry profiles
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
        center_y=4.5 + 7.0  # border + offset from PCB edge
    )
    
    # Generate toolpaths
    toolpaths = generate_top_frame_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=external_profile,
        pcb_opening_profile=pcb_opening_profile,
        usb_cutout_profile=usb_cutout_profile,
        mounting_holes=MOUNTING_HOLES,
        top_frame_height=TOP_FRAME_HEIGHT
    )
    
    print(f"Generated {len(toolpaths['operations'])} toolpath operations")
    
    # Export to DXF files
    print("\nExporting toolpaths to DXF...")
    exported_files = export_top_frame_toolpaths_to_dxf(toolpaths)
    
    print(f"\nExported {len(exported_files)} DXF files:")
    for operation, filepath in exported_files.items():
        print(f"  {operation}: {filepath}")
    
    print("\nTop frame toolpath export complete!")


if __name__ == "__main__":
    main()
