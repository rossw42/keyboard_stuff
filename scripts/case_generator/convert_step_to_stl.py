#!/usr/bin/env python3
"""
Simple STEP to STL converter
Converts a STEP file to STL format for visualization or 3D printing.
"""

import sys
import cadquery as cq
from pathlib import Path


def convert_step_to_stl(step_file: Path, stl_file: Path, tolerance: float = 0.001):
    """Convert STEP file to STL."""
    print(f"Loading STEP file: {step_file}")
    
    # Import STEP
    model = cq.importers.importStep(str(step_file))
    
    if model is None or not model.val():
        print(f"❌ Failed to import STEP file: {step_file}")
        return False
    
    # Get bounding box info
    shape = model.val()
    bb = shape.BoundingBox()
    print(f"  Bounds: X({bb.xmin:.2f}, {bb.xmax:.2f}), "
          f"Y({bb.ymin:.2f}, {bb.ymax:.2f}), "
          f"Z({bb.zmin:.2f}, {bb.zmax:.2f})")
    
    # Export to STL
    print(f"Exporting STL: {stl_file}")
    cq.exporters.export(model, str(stl_file), tolerance=tolerance)
    
    # Get file size
    size_mb = stl_file.stat().st_size / (1024 * 1024)
    print(f"✅ STL exported: {stl_file.name} ({size_mb:.2f} MB)")
    
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_step_to_stl.py <input.step> [output.stl]")
        print("\nConverts a STEP file to STL format.")
        print("\nExamples:")
        print("  python convert_step_to_stl.py keyboard.step")
        print("  python convert_step_to_stl.py keyboard.step output/keyboard.stl")
        return 1
    
    step_file = Path(sys.argv[1])
    
    if not step_file.exists():
        print(f"❌ File not found: {step_file}")
        return 1
    
    # Determine output file
    if len(sys.argv) >= 3:
        stl_file = Path(sys.argv[2])
    else:
        stl_file = step_file.with_suffix('.stl')
    
    # Create output directory if needed
    stl_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert
    success = convert_step_to_stl(step_file, stl_file)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
