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

from src.geometry.solid_models_lp import generate_assembly_model, export_step, export_stl
from src.constants_lp import (
    CASE_LENGTH,
    CASE_WIDTH,
    TOP_FRAME_HEIGHT,
    BOTTOM_TRAY_HEIGHT,
    TOTAL_HEIGHT,
    PCB_LENGTH,
    PCB_WIDTH,
    PCB_THICKNESS
)


def main():
    """Generate and export assembly 3D model."""
    # Create output directory
    output_dir = os.path.join('output', '60_percent_low_profile', '3d_models')
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
    print(f"  - Top frame: {CASE_LENGTH}mm x {CASE_WIDTH}mm x {TOP_FRAME_HEIGHT}mm")
    print(f"  - Bottom tray: {CASE_LENGTH}mm x {CASE_WIDTH}mm x {BOTTOM_TRAY_HEIGHT}mm")
    print(f"  - PCB reference: {PCB_LENGTH}mm x {PCB_WIDTH}mm x {PCB_THICKNESS}mm")
    print(f"  - Total assembled height: {TOTAL_HEIGHT}mm (LOW-PROFILE)")
    print("\nComponent positioning:")
    print(f"  - Bottom tray: Origin at (0, 0, 0)")
    print(f"  - PCB: Centered in cavity, resting on standoffs")
    print(f"  - Top frame: Positioned on top of bottom tray")
    print("\nNote: Hardware models (screws, inserts) not included in this version")


if __name__ == '__main__':
    main()
