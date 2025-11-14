#!/usr/bin/env python3
"""
Generate and export bottom tray 3D solid model.

This script creates a 3D solid model of the bottom tray component and exports
it to STEP format for CAD software import and visualization.

Requirements: 8.1
Output: output/3d_models/bottom_tray.step
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.geometry.solid_models import generate_bottom_tray_solid, export_step, export_stl
from src.constants import CAVITY_DEPTH


def main():
    """Generate and export bottom tray 3D model."""
    # Create output directory
    output_dir = os.path.join('output', '60_percent_standard', '3d_models')
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating bottom tray 3D solid model...")
    bottom_tray = generate_bottom_tray_solid()
    
    # Export to STEP format
    step_path = os.path.join(output_dir, 'bottom_tray.step')
    print(f"Exporting to STEP: {step_path}")
    export_step(bottom_tray, step_path)
    
    # Also export to STL for visualization
    stl_path = os.path.join(output_dir, 'bottom_tray.stl')
    print(f"Exporting to STL: {stl_path}")
    export_stl(bottom_tray, stl_path, tolerance=0.01)
    
    print("\nBottom tray 3D model generation complete!")
    print(f"  - STEP file: {step_path}")
    print(f"  - STL file: {stl_path}")
    print("\nModel specifications:")
    print(f"  - External dimensions: 295mm x 105mm x 15mm")
    print(f"  - Internal cavity: 287mm x 96.6mm x {CAVITY_DEPTH}mm deep")
    print(f"  - Standoff pillars: 6 locations, 6mm dia, 3mm high")
    print(f"  - Standoff holes: 2.2mm dia (M2 clearance)")
    print(f"  - Assembly screws: 3.2mm dia through-holes")
    print(f"  - Assembly counterbores: 6mm dia, 3mm deep")
    print(f"  - Rubber feet recesses: 10mm dia, 2mm deep, 4 corners")


if __name__ == '__main__':
    main()
