#!/usr/bin/env python3
"""
Generate switch plates for keyboard PCBs
Usage: python generate_plate.py <pcb_left.step> <pcb_right.step> [output_dir]

Based on analysis of Corne and Sweep keyboards:
- Plate thickness: 1.5mm (standard for MX switches)
- Follows PCB outline with small offset
- Cutouts for switches
"""

import sys
import os
import cadquery as cq
from cadquery import exporters

# Plate parameters
PLATE_THICKNESS = 1.5  # Standard for Cherry MX switches
PLATE_OFFSET = 1.0  # How far plate extends beyond PCB edge
SWITCH_CUTOUT_SIZE = 14.0  # Cherry MX switch cutout (14x14mm)
SWITCH_SPACING = 19.05  # Standard MX spacing (0.75 inches)

def create_plate_from_pcb(pcb_file, output_name):
    """Create a switch plate following PCB outline"""
    
    print(f"\nCreating plate for {os.path.basename(pcb_file)}...")
    
    # Import PCB
    pcb = cq.importers.importStep(pcb_file)
    pcb_shape = pcb.val()
    bb = pcb_shape.BoundingBox()
    
    print(f"  PCB bounds: X({bb.xmin:.2f}, {bb.xmax:.2f}), Y({bb.ymin:.2f}, {bb.ymax:.2f})")
    print(f"  Tracing PCB outline...")
    
    try:
        # Get the PCB faces and find the largest one
        wp = cq.Workplane("XY").add(pcb_shape)
        faces = wp.faces().vals()
        
        # Find largest face by area
        largest_face = max(faces, key=lambda f: f.Area())
        print(f"  Found PCB face with area: {largest_face.Area():.2f} mm²")
        
        # Get the outer wire
        outer_wire = largest_face.outerWire()
        
        # Create offset wire for plate
        try:
            offset_wires = outer_wire.offset2D(PLATE_OFFSET)
            
            if not offset_wires:
                raise Exception("Offset failed")
            
            # Create plate by extruding offset wire
            plate = (cq.Workplane("XY")
                    .add(offset_wires[0])
                    .toPending()
                    .extrude(PLATE_THICKNESS))
            
            print(f"  ✓ Created organic plate following PCB outline")
            
        except Exception as e:
            print(f"  ⚠ Offset method failed: {e}")
            print(f"  Falling back to bounding box method...")
            return create_plate_bbox_fallback(bb)
        
    except Exception as e:
        print(f"  ⚠ PCB outline extraction failed: {e}")
        print(f"  Falling back to bounding box method...")
        return create_plate_bbox_fallback(bb)
    
    print(f"  Note: Switch cutouts not implemented yet")
    print(f"  You'll need to add {SWITCH_CUTOUT_SIZE}x{SWITCH_CUTOUT_SIZE}mm cutouts for switches")
    
    # Add mounting holes in corners
    hole_inset = 5
    hole_diameter = 2.5  # M2.5 screws
    
    hole_positions = [
        (bb.xmin + hole_inset, bb.ymin + hole_inset),
        (bb.xmin + hole_inset, bb.ymax - hole_inset),
        (bb.xmax - hole_inset, bb.ymin + hole_inset),
        (bb.xmax - hole_inset, bb.ymax - hole_inset),
    ]
    
    for x, y in hole_positions:
        hole = (cq.Workplane("XY")
               .cylinder(PLATE_THICKNESS + 1, hole_diameter / 2)
               .translate((x, y, PLATE_THICKNESS / 2)))
        plate = plate.cut(hole)
    
    print(f"  Added mounting holes (M{hole_diameter})")
    
    # Add fillets to corners
    try:
        plate = plate.edges("|Z").fillet(1.0)
        print(f"  Added 1.0mm fillets to edges")
    except:
        print("  Note: Could not fillet all edges")
    
    return plate

def create_plate_bbox_fallback(bb):
    """Fallback: Create rectangular plate from bounding box"""
    
    print(f"  ⚠ WARNING: Creating RECTANGULAR plate (not following PCB outline)")
    
    pcb_width = bb.xmax - bb.xmin
    pcb_depth = bb.ymax - bb.ymin
    
    plate_width = pcb_width + 2 * PLATE_OFFSET
    plate_depth = pcb_depth + 2 * PLATE_OFFSET
    
    plate = (cq.Workplane("XY")
            .box(plate_width, plate_depth, PLATE_THICKNESS, centered=False)
            .translate((bb.xmin - PLATE_OFFSET, bb.ymin - PLATE_OFFSET, 0)))
    
    return plate

def generate_plates(left_pcb, right_pcb, output_dir=None):
    """Generate plates for both keyboard halves"""
    
    if not os.path.exists(left_pcb):
        print(f"Error: File not found: {left_pcb}")
        sys.exit(1)
    
    if not os.path.exists(right_pcb):
        print(f"Error: File not found: {right_pcb}")
        sys.exit(1)
    
    # Default output directory
    if output_dir is None:
        output_dir = os.path.dirname(left_pcb)
    
    # Get base name
    base_name = os.path.splitext(os.path.basename(left_pcb))[0].replace('_pcb_left', '').replace('_left', '')
    
    # Create plates
    left_plate = create_plate_from_pcb(left_pcb, "left")
    right_plate = create_plate_from_pcb(right_pcb, "right")
    
    # Export
    print("\n=== Exporting files ===")
    
    left_step = os.path.join(output_dir, f"{base_name}_plate_left.step")
    left_stl = os.path.join(output_dir, f"{base_name}_plate_left.stl")
    right_step = os.path.join(output_dir, f"{base_name}_plate_right.step")
    right_stl = os.path.join(output_dir, f"{base_name}_plate_right.stl")
    
    exporters.export(left_plate, left_step)
    print(f"✓ {os.path.basename(left_step)}")
    
    exporters.export(left_plate, left_stl)
    print(f"✓ {os.path.basename(left_stl)}")
    
    exporters.export(right_plate, right_step)
    print(f"✓ {os.path.basename(right_step)}")
    
    exporters.export(right_plate, right_stl)
    print(f"✓ {os.path.basename(right_stl)}")
    
    print("\n✓ Plate generation complete!")
    print(f"\nPlate specifications:")
    print(f"  - Thickness: {PLATE_THICKNESS} mm (standard for MX switches)")
    print(f"  - Offset from PCB: {PLATE_OFFSET} mm")
    print(f"  - Mounting holes: M2.5")
    print(f"\n⚠ Note: You'll need to manually add switch cutouts")
    print(f"  Each switch needs a {SWITCH_CUTOUT_SIZE}x{SWITCH_CUTOUT_SIZE}mm cutout")

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_plate.py <pcb_left.step> <pcb_right.step> [output_dir]")
        print("\nExample:")
        print("  python generate_plate.py keyboard_pcb_left.step keyboard_pcb_right.step")
        print("  python generate_plate.py keyboard_pcb_left.step keyboard_pcb_right.step ./output")
        sys.exit(1)
    
    left_pcb = sys.argv[1]
    right_pcb = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    generate_plates(left_pcb, right_pcb, output_dir)

if __name__ == "__main__":
    main()
