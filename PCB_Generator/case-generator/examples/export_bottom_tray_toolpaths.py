"""
Export bottom tray CNC toolpaths to DXF files.

This script generates and exports all bottom tray toolpath operations
as separate DXF files for use with CAM software.

Requirements: 6.1, 8.2
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.constants import (
    CASE_LENGTH, CASE_WIDTH, BOTTOM_TRAY_HEIGHT,
    MOUNTING_HOLES, RUBBER_FEET_POSITIONS
)
from src.geometry.profiles import (
    generate_external_profile,
    generate_internal_cavity,
    generate_standoff_pillars
)
from src.toolpaths.bottom_tray import generate_bottom_tray_toolpaths
from src.export.toolpath_dxf import export_bottom_tray_toolpaths_to_dxf


def main():
    """Generate and export bottom tray toolpaths to DXF."""
    print("Generating bottom tray toolpaths...")
    
    # Generate geometry profiles
    external_profile = generate_external_profile(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        corner_radius=3.0
    )
    
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
    
    # Generate toolpaths
    toolpaths = generate_bottom_tray_toolpaths(
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
    
    print(f"Generated {len(toolpaths['operations'])} toolpath operations")
    
    # Export to DXF files
    print("\nExporting toolpaths to DXF...")
    exported_files = export_bottom_tray_toolpaths_to_dxf(toolpaths)
    
    print(f"\nExported {len(exported_files)} DXF files:")
    for operation, filepath in exported_files.items():
        print(f"  {operation}: {filepath}")
    
    print("\nBottom tray toolpath export complete!")


if __name__ == "__main__":
    main()
