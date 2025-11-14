#!/usr/bin/env python3
"""
Generate and export top frame 3D solid model.

This script creates a 3D solid model of the top frame component and exports
it to STEP format for CAD software import and visualization.

Requirements: 8.1
Output: output/3d_models/top_frame.step
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.geometry.solid_models import generate_top_frame_solid, export_step, export_stl


def main():
    """Generate and export top frame 3D model."""
    # Create output directory
    output_dir = os.path.join('output', '60_percent_standard', '3d_models')
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating top frame 3D solid model...")
    top_frame = generate_top_frame_solid()
    
    # Export to STEP format
    step_path = os.path.join(output_dir, 'top_frame.step')
    print(f"Exporting to STEP: {step_path}")
    export_step(top_frame, step_path)
    
    # Also export to STL for visualization
    stl_path = os.path.join(output_dir, 'top_frame.stl')
    print(f"Exporting to STL: {stl_path}")
    export_stl(top_frame, stl_path, tolerance=0.01)
    
    print("\nTop frame 3D model generation complete!")
    print(f"  - STEP file: {step_path}")
    print(f"  - STL file: {stl_path}")
    print("\nModel specifications:")
    print(f"  - External dimensions: 295mm x 105mm x 5mm")
    print(f"  - PCB opening: 286mm x 95.6mm (centered)")
    print(f"  - USB cutout: 16mm x 10mm (centered on top edge)")
    print(f"  - Brass insert holes: 6 locations, 5.8mm dia, 4mm deep")


if __name__ == '__main__':
    main()
