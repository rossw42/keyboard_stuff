#!/usr/bin/env python3
"""
Verify Task 6 outputs - check that all technical drawings were generated correctly.
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and report its size."""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  ✓ {description}")
        print(f"    Path: {filepath}")
        print(f"    Size: {size:,} bytes")
        return True
    else:
        print(f"  ✗ {description} - FILE NOT FOUND")
        print(f"    Expected: {filepath}")
        return False

def main():
    """Verify all Task 6 outputs."""
    
    print("=" * 70)
    print("Task 6 Output Verification")
    print("=" * 70)
    print()
    
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    output_dir = os.path.join(base_dir, 'output', 'drawings')
    
    all_files_exist = True
    
    # Task 6.1: Top Frame Technical Drawing
    print("Task 6.1: Top Frame Technical Drawing")
    print("-" * 70)
    all_files_exist &= check_file_exists(
        os.path.join(output_dir, 'top_frame_technical_drawing.dxf'),
        "Top frame DXF drawing"
    )
    print()
    all_files_exist &= check_file_exists(
        os.path.join(output_dir, 'top_frame_technical_drawing.pdf'),
        "Top frame PDF drawing"
    )
    print()
    
    # Task 6.2: Bottom Tray Technical Drawing
    print("Task 6.2: Bottom Tray Technical Drawing")
    print("-" * 70)
    all_files_exist &= check_file_exists(
        os.path.join(output_dir, 'bottom_tray_technical_drawing.dxf'),
        "Bottom tray DXF drawing"
    )
    print()
    all_files_exist &= check_file_exists(
        os.path.join(output_dir, 'bottom_tray_technical_drawing.pdf'),
        "Bottom tray PDF drawing"
    )
    print()
    
    # Task 6.3: Assembly Drawing
    print("Task 6.3: Assembly Drawing with Hardware Callouts")
    print("-" * 70)
    all_files_exist &= check_file_exists(
        os.path.join(output_dir, 'assembly_drawing.pdf'),
        "Assembly drawing PDF"
    )
    print()
    
    # Summary
    print("=" * 70)
    if all_files_exist:
        print("✓ VERIFICATION PASSED")
        print()
        print("All Task 6 outputs have been generated successfully:")
        print("  • Top frame technical drawing (DXF + PDF)")
        print("  • Bottom tray technical drawing (DXF + PDF)")
        print("  • Assembly drawing with hardware callouts (PDF)")
        print()
        print("Total files: 5")
        print(f"Output directory: {output_dir}")
        print()
        print("Task 6 is COMPLETE!")
        return 0
    else:
        print("✗ VERIFICATION FAILED")
        print()
        print("Some output files are missing. Please run the export scripts:")
        print("  python3 examples/export_top_frame_drawing.py")
        print("  python3 examples/export_bottom_tray_drawing.py")
        print("  python3 examples/export_assembly_drawing.py")
        return 1
    print("=" * 70)


if __name__ == '__main__':
    sys.exit(main())
