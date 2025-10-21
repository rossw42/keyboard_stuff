#!/usr/bin/env python3
"""
Verify 3D model generation and validate dimensions.

This script generates all 3D models and validates their dimensions against
the design specifications to ensure accuracy.

Requirements: 8.1, 8.4
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.geometry.solid_models import (
    generate_top_frame_solid,
    generate_bottom_tray_solid,
    generate_assembly_model,
)
from src.constants import (
    CASE_LENGTH,
    CASE_WIDTH,
    TOP_FRAME_HEIGHT,
    BOTTOM_TRAY_HEIGHT,
    PCB_LENGTH,
    PCB_WIDTH,
    PCB_THICKNESS,
)


def get_bounding_box(part):
    """Get bounding box dimensions of a Part."""
    bbox = part.bounding_box()
    length = bbox.max.X - bbox.min.X
    width = bbox.max.Y - bbox.min.Y
    height = bbox.max.Z - bbox.min.Z
    return length, width, height


def verify_dimensions(name, part, expected_length, expected_width, expected_height, tolerance=0.5):
    """Verify part dimensions against expected values."""
    length, width, height = get_bounding_box(part)
    
    print(f"\n{name}:")
    print(f"  Expected: {expected_length:.1f} × {expected_width:.1f} × {expected_height:.1f} mm")
    print(f"  Actual:   {length:.1f} × {width:.1f} × {height:.1f} mm")
    
    length_ok = abs(length - expected_length) <= tolerance
    width_ok = abs(width - expected_width) <= tolerance
    height_ok = abs(height - expected_height) <= tolerance
    
    if length_ok and width_ok and height_ok:
        print(f"  ✓ Dimensions verified (within ±{tolerance}mm tolerance)")
        return True
    else:
        print(f"  ✗ Dimension mismatch!")
        if not length_ok:
            print(f"    Length error: {abs(length - expected_length):.2f}mm")
        if not width_ok:
            print(f"    Width error: {abs(width - expected_width):.2f}mm")
        if not height_ok:
            print(f"    Height error: {abs(height - expected_height):.2f}mm")
        return False


def main():
    """Verify all 3D models."""
    print("=" * 70)
    print("3D Model Verification")
    print("=" * 70)
    
    all_passed = True
    
    # Verify top frame
    print("\n[1/3] Verifying top frame...")
    top_frame = generate_top_frame_solid()
    passed = verify_dimensions(
        "Top Frame",
        top_frame,
        CASE_LENGTH,
        CASE_WIDTH,
        TOP_FRAME_HEIGHT,
        tolerance=0.5
    )
    all_passed = all_passed and passed
    
    # Verify bottom tray
    print("\n[2/3] Verifying bottom tray...")
    bottom_tray = generate_bottom_tray_solid()
    passed = verify_dimensions(
        "Bottom Tray",
        bottom_tray,
        CASE_LENGTH,
        CASE_WIDTH,
        BOTTOM_TRAY_HEIGHT,
        tolerance=0.5
    )
    all_passed = all_passed and passed
    
    # Verify assembly
    print("\n[3/3] Verifying assembly...")
    assembly = generate_assembly_model()
    total_height = TOP_FRAME_HEIGHT + BOTTOM_TRAY_HEIGHT
    passed = verify_dimensions(
        "Assembly",
        assembly,
        CASE_LENGTH,
        CASE_WIDTH,
        total_height,
        tolerance=0.5
    )
    all_passed = all_passed and passed
    
    # Summary
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All 3D models verified successfully!")
        print("=" * 70)
        print("\nAll dimensions are within tolerance.")
        print("Models are ready for export and CAD import.")
        return 0
    else:
        print("✗ Some models failed verification!")
        print("=" * 70)
        print("\nPlease review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
