#!/usr/bin/env python3
"""
Combine a single keyboard half into a unified keyboard by mirroring.

Takes a single half PCB and creates a unified keyboard by:
1. Mirroring the half to create the opposite side
2. Positioning with configurable gap and splay
3. Combining into a single PCB geometry

Usage: python combine_split_halves.py <half.step> [options]
"""

import sys
import argparse
from pathlib import Path

try:
    import cadquery as cq
except ImportError:
    print("Error: cadquery not installed")
    print("Install with: pip install cadquery")
    sys.exit(1)


def combine_halves(
    input_file: Path,
    output_file: Path,
    gap: float = 15.0,
    splay: float = 0.0,
    vertical_offset: float = 0.0,
    which_half: str = "left"
):
    """
    Combine a single half into a unified keyboard.
    
    Args:
        input_file: Path to the half PCB STEP file
        output_file: Path for the combined output STEP file
        gap: Gap between halves in mm
        splay: Splay angle in degrees (positive = outward rotation)
        vertical_offset: Vertical offset between halves in mm
        which_half: Which half is the input ("left" or "right")
    """
    print(f"Loading {which_half} half from: {input_file}")
    
    # Import the half
    half = cq.importers.importStep(str(input_file))
    
    # Get bounding box
    bb = half.val().BoundingBox()
    print(f"Bounding box: X({bb.xmin:.2f}, {bb.xmax:.2f}), "
          f"Y({bb.ymin:.2f}, {bb.ymax:.2f}), Z({bb.zmin:.2f}, {bb.zmax:.2f})")
    
    # Calculate centers
    x_center = (bb.xmin + bb.xmax) / 2
    y_center = (bb.ymin + bb.ymax) / 2
    z_center = (bb.zmin + bb.zmax) / 2
    width = bb.xmax - bb.xmin
    
    print(f"Half center: ({x_center:.2f}, {y_center:.2f}, {z_center:.2f})")
    print(f"Half width: {width:.2f}mm")
    
    # Create the mirrored half
    print(f"\nCreating mirrored half...")
    print(f"  Gap: {gap}mm")
    print(f"  Splay: {splay}°")
    print(f"  Vertical offset: {vertical_offset}mm")
    
    # For split keyboards, we want MCU/TRRS on the outside edges
    # So we mirror around the INNER edge (where MCU is)
    
    # For left half: MCU is on right (inner edge), pinky is on left (outer edge)
    # For right half: MCU is on left (inner edge), pinky is on right (outer edge)
    
    if which_half == "left":
        # Left half: mirror around the inner edge (right edge, max X)
        # This puts the MCU on the outside
        mirror_x = bb.xmax
        # Original stays as left, mirrored becomes right
        left_half = half
        # Mirror across a plane at the inner edge (MCU side)
        right_half = half.mirror(mirrorPlane="YZ", basePointVector=(mirror_x, 0, 0))
    else:
        # Right half: mirror around the inner edge (left edge, min X)
        mirror_x = bb.xmin
        # Mirrored becomes left
        left_half = half.mirror(mirrorPlane="YZ", basePointVector=(mirror_x, 0, 0))
        # Original stays as right
        right_half = half
    
    # Now position the halves with gap and splay
    # After mirroring, both halves are positioned relative to the mirror edge
    # We need to move them apart by the gap amount
    
    # Apply transformations to left half
    # Move left by gap/2, apply negative splay, apply negative vertical offset
    left_transformed = (left_half
                       .translate((-gap/2, -vertical_offset/2, 0)))
    
    if splay != 0:
        # Rotate around the inner edge (where it meets the gap)
        if which_half == "left":
            rotate_x = bb.xmax - gap/2
        else:
            rotate_x = bb.xmin - gap/2
        left_transformed = (left_transformed
                           .rotate((rotate_x, y_center, z_center),
                                  (rotate_x, y_center, z_center + 1),
                                  -splay))
    
    # Apply transformations to right half
    # Move right by gap/2, apply positive splay, apply positive vertical offset
    right_transformed = (right_half
                        .translate((gap/2, vertical_offset/2, 0)))
    
    if splay != 0:
        # Rotate around the inner edge (where it meets the gap)
        if which_half == "left":
            rotate_x = bb.xmax + gap/2
        else:
            rotate_x = bb.xmin + gap/2
        right_transformed = (right_transformed
                            .rotate((rotate_x, y_center, z_center),
                                   (rotate_x, y_center, z_center + 1),
                                   splay))
    
    # Combine the halves
    print("\nCombining halves...")
    combined = left_transformed.union(right_transformed)
    
    # Get combined bounding box
    combined_bb = combined.val().BoundingBox()
    combined_width = combined_bb.xmax - combined_bb.xmin
    print(f"Combined width: {combined_width:.2f}mm")
    
    # Export
    print(f"\nExporting to: {output_file}")
    cq.exporters.export(combined, str(output_file))
    
    # Also export STL
    stl_file = output_file.with_suffix('.stl')
    print(f"Exporting STL to: {stl_file}")
    cq.exporters.export(combined, str(stl_file))
    
    print("\n✓ Successfully created unified keyboard!")
    print(f"  Combined STEP: {output_file.name}")
    print(f"  Combined STL: {stl_file.name}")
    
    return combined


def main():
    parser = argparse.ArgumentParser(
        description='Combine a single keyboard half into a unified keyboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic combination with 15mm gap
  python combine_split_halves.py corne_left.step
  
  # With custom gap and splay
  python combine_split_halves.py corne_left.step --gap 20 --splay 5
  
  # With vertical offset (stagger)
  python combine_split_halves.py corne_left.step --gap 15 --vertical-offset 10
        """
    )
    
    parser.add_argument('input', type=Path,
                       help='Input half PCB STEP file')
    parser.add_argument('-o', '--output', type=Path,
                       help='Output file path (default: <input>_unified.step)')
    parser.add_argument('--gap', type=float, default=15.0,
                       help='Gap between halves in mm (default: 15.0)')
    parser.add_argument('--splay', type=float, default=0.0,
                       help='Splay angle in degrees, positive = outward (default: 0.0)')
    parser.add_argument('--vertical-offset', type=float, default=0.0,
                       help='Vertical offset between halves in mm (default: 0.0)')
    parser.add_argument('--which-half', choices=['left', 'right'], default='left',
                       help='Which half is the input (default: left)')
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: File not found: {args.input}")
        sys.exit(1)
    
    # Determine output path
    if args.output:
        output_file = args.output
    else:
        # Default: same directory, add _unified suffix
        output_file = args.input.parent / f"{args.input.stem}_unified.step"
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Combine the halves
    combine_halves(
        args.input,
        output_file,
        gap=args.gap,
        splay=args.splay,
        vertical_offset=args.vertical_offset,
        which_half=args.which_half
    )


if __name__ == "__main__":
    main()
