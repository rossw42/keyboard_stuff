#!/usr/bin/env python3
"""
Generate and export assembly 3D model with PCB reference.

This script creates a complete assembly model showing the top frame, bottom tray,
and PCB reference positioned in their assembled configuration. Exports to STEP
format for CAD software import and visualization.

Requirements: 8.4
Output: output/3d_models/assembly.step
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.geometry.solid_models import generate_assembly_model, export_step, export_stl


def main():
    """Generate and export assembly 3D model."""
    # Create output directory
    output_dir = os.path.join('output', '60_percent_standard', '3d_models')
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating assembly 3D model...")
    print("  - Creating top frame component...")
    print("  - Creating bottom tray component...")
    print("  - Creating PCB reference...")
    print("  - Positioning components in assembly...")
    
    assembly = generate_assembly_model()
    
    # Export to STEP format
    step_path = os.path.join(output_dir, 'assembly.step')
    print(f"\nExporting to STEP: {step_path}")
    export_step(assembly, step_path)
    
    # Also export to STL for visualization
    stl_path = os.path.join(output_dir, 'assembly.stl')
    print(f"Exporting to STL: {stl_path}")
    export_stl(assembly, stl_path, tolerance=0.01)
    
    print("\nAssembly 3D model generation complete!")
    print(f"  - STEP file: {step_path}")
    print(f"  - STL file: {stl_path}")
    print("\nAssembly specifications:")
    print(f"  - Top frame: 295mm x 105mm x 5mm")
    print(f"  - Bottom tray: 295mm x 105mm x 15mm")
    print(f"  - PCB reference: 285mm x 94.6mm x 1.6mm")
    print(f"  - Total assembled height: 20mm")
    print("\nComponent positioning:")
    print(f"  - Bottom tray: Origin at (0, 0, 0)")
    print(f"  - PCB: Centered in cavity, resting on standoffs")
    print(f"  - Top frame: Positioned on top of bottom tray")
    print("\nNote: Hardware models (screws, inserts) not included in this version")


if __name__ == '__main__':
    main()
