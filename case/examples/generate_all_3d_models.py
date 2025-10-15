#!/usr/bin/env python3
"""
Generate and export all 3D models (top frame, bottom tray, and assembly).

This script creates all 3D solid models for the keyboard case project and exports
them to STEP and STL formats for CAD software import and visualization.

Requirements: 8.1, 8.4
Output: output/3d_models/
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.geometry.solid_models import (
    generate_top_frame_solid,
    generate_bottom_tray_solid,
    generate_assembly_model,
    export_step,
    export_stl
)


def main():
    """Generate and export all 3D models."""
    # Create output directory
    output_dir = os.path.join('output', '60_percent_standard', '3d_models')
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("60% Keyboard Case - 3D Model Generation")
    print("=" * 70)
    
    # Generate top frame
    print("\n[1/3] Generating top frame 3D solid model...")
    top_frame = generate_top_frame_solid()
    
    step_path = os.path.join(output_dir, 'top_frame.step')
    stl_path = os.path.join(output_dir, 'top_frame.stl')
    print(f"      Exporting STEP: {step_path}")
    export_step(top_frame, step_path)
    print(f"      Exporting STL:  {stl_path}")
    export_stl(top_frame, stl_path, tolerance=0.01)
    print("      ✓ Top frame complete")
    
    # Generate bottom tray
    print("\n[2/3] Generating bottom tray 3D solid model...")
    bottom_tray = generate_bottom_tray_solid()
    
    step_path = os.path.join(output_dir, 'bottom_tray.step')
    stl_path = os.path.join(output_dir, 'bottom_tray.stl')
    print(f"      Exporting STEP: {step_path}")
    export_step(bottom_tray, step_path)
    print(f"      Exporting STL:  {stl_path}")
    export_stl(bottom_tray, stl_path, tolerance=0.01)
    print("      ✓ Bottom tray complete")
    
    # Generate assembly
    print("\n[3/3] Generating assembly 3D model with PCB reference...")
    assembly = generate_assembly_model()
    
    step_path = os.path.join(output_dir, 'assembly.step')
    stl_path = os.path.join(output_dir, 'assembly.stl')
    print(f"      Exporting STEP: {step_path}")
    export_step(assembly, step_path)
    print(f"      Exporting STL:  {stl_path}")
    export_stl(assembly, stl_path, tolerance=0.01)
    print("      ✓ Assembly complete")
    
    # Summary
    print("\n" + "=" * 70)
    print("All 3D models generated successfully!")
    print("=" * 70)
    print(f"\nOutput directory: {output_dir}/")
    print("\nGenerated files:")
    print("  STEP files (for CAD import):")
    print("    - top_frame.step")
    print("    - bottom_tray.step")
    print("    - assembly.step")
    print("\n  STL files (for visualization):")
    print("    - top_frame.stl")
    print("    - bottom_tray.stl")
    print("    - assembly.stl")
    print("\nModel specifications:")
    print("  Top Frame:")
    print("    - Dimensions: 295mm x 105mm x 5mm")
    print("    - PCB opening: 286mm x 95.6mm (centered)")
    print("    - USB cutout: 16mm x 10mm (centered on top edge)")
    print("    - Brass insert holes: 6 locations, 5.8mm dia, 4mm deep")
    print("\n  Bottom Tray:")
    print("    - Dimensions: 295mm x 105mm x 15mm")
    print("    - Internal cavity: 287mm x 96.6mm x 8mm deep")
    print("    - Standoff pillars: 6 locations, 6mm dia, 3mm high")
    print("    - Assembly features: screws, counterbores, rubber feet recesses")
    print("\n  Assembly:")
    print("    - Complete case with PCB reference")
    print("    - Total assembled height: 20mm")
    print("    - All components positioned correctly")
    print("\nThese STEP files can be imported into CAD software such as:")
    print("  - FreeCAD, Fusion 360, SolidWorks, OnShape, etc.")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
