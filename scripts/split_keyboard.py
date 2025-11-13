#!/usr/bin/env python3
"""
Split any keyboard STEP file into two halves for 3D printing
Usage: python split_keyboard.py <input.step> [output_dir]
"""

import sys
import os

try:
    import cadquery as cq
except ImportError:
    print("Error: cadquery not installed")
    print("Install with: pip install cadquery")
    sys.exit(1)

def clean_split_edge(half, bb, x_center, is_left=True):
    """Clean up the split edge by cutting off mouse bites"""
    try:
        # Create a cutting box that removes the split edge area
        # The mouse bites are within ~1mm of the split line
        cleanup_width = 1.0  # Cut 1mm from the split edge (just enough for mouse bites)
        
        if is_left:
            # For left half, cut from x_center inward
            cut_box = (cq.Workplane("XY")
                      .box(cleanup_width, 
                           bb.ymax - bb.ymin + 10,
                           bb.zmax - bb.zmin + 2,
                           centered=False)
                      .translate((x_center - cleanup_width,
                                 bb.ymin - 5,
                                 bb.zmin - 1)))
        else:
            # For right half, cut from x_center inward
            cut_box = (cq.Workplane("XY")
                      .box(cleanup_width,
                           bb.ymax - bb.ymin + 10,
                           bb.zmax - bb.zmin + 2,
                           centered=False)
                      .translate((x_center,
                                 bb.ymin - 5,
                                 bb.zmin - 1)))
        
        # Cut the mouse bites
        cleaned = half.cut(cut_box)
        return cleaned
    except Exception as e:
        print(f"    ⚠ Edge cleaning failed: {e}")
        return half
    
    return half

def split_keyboard(input_file, output_dir=None):
    """Split a keyboard STEP file into left and right halves"""
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    # Default output directory is same as input file
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
    
    # Get base name without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    # Remove _pcb suffix if present to avoid duplication
    if base_name.endswith('_pcb'):
        base_name = base_name[:-4]
    
    print(f"Loading STEP file: {input_file}")
    
    # Import the STEP file
    imported = cq.importers.importStep(input_file)
    
    # Get bounding box
    bb = imported.val().BoundingBox()
    print(f"Bounding box: X({bb.xmin:.2f}, {bb.xmax:.2f}), Y({bb.ymin:.2f}, {bb.ymax:.2f}), Z({bb.zmin:.2f}, {bb.zmax:.2f})")
    
    # Calculate center
    x_center = (bb.xmin + bb.xmax) / 2
    print(f"Splitting at X = {x_center:.2f}")
    
    # Create cutting boxes with margin
    margin = 10  # mm margin
    height = bb.zmax - bb.zmin + 2 * margin
    depth = bb.ymax - bb.ymin + 2 * margin
    
    # Left half: cut everything to the right of center
    print("Creating left half...")
    left_width = bb.xmax - x_center + margin
    left_cutter = (cq.Workplane("XY")
                   .box(left_width, depth, height)
                   .translate((x_center + left_width/2, (bb.ymin + bb.ymax)/2, (bb.zmin + bb.zmax)/2)))
    
    left_half = imported.cut(left_cutter)
    
    # Right half: cut everything to the left of center
    print("Creating right half...")
    right_width = x_center - bb.xmin + margin
    right_cutter = (cq.Workplane("XY")
                    .box(right_width, depth, height)
                    .translate((bb.xmin + right_width/2 - margin, (bb.ymin + bb.ymax)/2, (bb.zmin + bb.zmax)/2)))
    
    right_half = imported.cut(right_cutter)
    
    # Export as STEP files
    left_step = os.path.join(output_dir, f"{base_name}_pcb_left.step")
    right_step = os.path.join(output_dir, f"{base_name}_pcb_right.step")
    
    print(f"Saving left half STEP...")
    cq.exporters.export(left_half, left_step)
    
    print(f"Saving right half STEP...")
    cq.exporters.export(right_half, right_step)
    
    # Export as STL files for 3D printing
    left_stl = os.path.join(output_dir, f"{base_name}_pcb_left.stl")
    right_stl = os.path.join(output_dir, f"{base_name}_pcb_right.stl")
    
    print(f"Saving left half STL...")
    cq.exporters.export(left_half, left_stl)
    
    print(f"Saving right half STL...")
    cq.exporters.export(right_half, right_stl)
    
    print("\n✓ Successfully created keyboard halves!")
    print(f"  - {os.path.basename(left_step)}")
    print(f"  - {os.path.basename(left_stl)}")
    print(f"  - {os.path.basename(right_step)}")
    print(f"  - {os.path.basename(right_stl)}")
    
    # Clean up mouse bites / breakaway tabs
    print("\nCleaning up mouse bites from split edges...")
    try:
        # Clean left half
        left_cleaned = clean_split_edge(left_half, bb, x_center, is_left=True)
        cq.exporters.export(left_cleaned, left_step)
        cq.exporters.export(left_cleaned, left_stl)
        
        # Clean right half  
        right_cleaned = clean_split_edge(right_half, bb, x_center, is_left=False)
        cq.exporters.export(right_cleaned, right_step)
        cq.exporters.export(right_cleaned, right_stl)
        
        print("✓ Cleaned split edges")
    except Exception as e:
        print(f"⚠ Could not clean edges: {e}")
        print("  Using original split (with mouse bites)")

def main():
    if len(sys.argv) < 2:
        print("Usage: python split_keyboard.py <input.step> [output_dir]")
        print("\nExample:")
        print("  python split_keyboard.py keyboard.step")
        print("  python split_keyboard.py keyboard.step ./output")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    split_keyboard(input_file, output_dir)

if __name__ == "__main__":
    main()
