#!/usr/bin/env python3
"""
Generate a case for a keyboard PCB STEP file
Usage: python generate_case.py <pcb_left.step> <pcb_right.step> [output_dir]
"""

import sys
import os
import cadquery as cq
from cadquery import exporters

# Case parameters (configurable)
# Based on analysis of Sweep and Corne keyboards
WALL_THICKNESS = 2.0  # Thinner walls for minimal design
BOTTOM_THICKNESS = 1.5  # Thinner bottom
PCB_CLEARANCE_BOTTOM = 2.5  # Space for components
PCB_THICKNESS = 1.6  # Standard PCB thickness
SWITCH_PLATE_THICKNESS = 1.5  # Standard switch plate thickness
LIP_WIDTH = 1.5  # Width of the lip that holds the plate
LIP_HEIGHT = 0.5  # How much the lip extends above the PCB
OFFSET = 2.5  # Closer to PCB edge for compact design
FILLET_RADIUS = 1.5  # Smooth rounded edges

def create_case_from_pcb(pcb_file, output_name):
    """Create case following PCB outline"""
    
    print(f"\nCreating case for {os.path.basename(pcb_file)}...")
    
    # Import PCB
    pcb = cq.importers.importStep(pcb_file)
    pcb_shape = pcb.val()
    bb = pcb_shape.BoundingBox()
    
    print(f"  PCB bounds: X({bb.xmin:.2f}, {bb.xmax:.2f}), Y({bb.ymin:.2f}, {bb.ymax:.2f}), Z({bb.zmin:.2f}, {bb.zmax:.2f})")
    
    pcb_thickness = bb.zmax - bb.zmin
    case_height = BOTTOM_THICKNESS + PCB_CLEARANCE_BOTTOM + pcb_thickness + LIP_HEIGHT
    
    print(f"  Tracing PCB outline...")
    
    try:
        # Get the PCB faces and find the largest one (top or bottom)
        wp = cq.Workplane("XY").add(pcb_shape)
        faces = wp.faces().vals()
        
        # Find largest face by area
        largest_face = max(faces, key=lambda f: f.Area())
        print(f"  Found PCB face with area: {largest_face.Area():.2f} mm²")
        
        # Get the outer wire of this face
        outer_wire = largest_face.outerWire()
        
        # Create offset wires for case
        try:
            outer_offset_wires = outer_wire.offset2D(OFFSET)
            inner_offset_wires = outer_wire.offset2D(OFFSET - WALL_THICKNESS)
            
            if not outer_offset_wires or not inner_offset_wires:
                raise Exception("Offset failed")
            
            # Create outer shell by extruding offset wire
            outer_shell = (cq.Workplane("XY")
                          .add(outer_offset_wires[0])
                          .toPending()
                          .extrude(case_height))
            
            # Create inner cavity
            inner_cavity = (cq.Workplane("XY")
                           .add(inner_offset_wires[0])
                           .toPending()
                           .extrude(case_height - BOTTOM_THICKNESS)
                           .translate((0, 0, BOTTOM_THICKNESS)))
            
            case = outer_shell.cut(inner_cavity)
            print(f"  ✓ Created organic case following PCB outline")
            
            # Add plate lip - a ledge for the plate to sit on
            print(f"  Adding plate lip...")
            try:
                # The lip sits at the top of the PCB
                lip_z = BOTTOM_THICKNESS + PCB_CLEARANCE_BOTTOM + pcb_thickness
                
                # Create outer lip edge (at the inner wall)
                lip_outer_wire = outer_wire.offset2D(OFFSET - WALL_THICKNESS)
                
                # Create inner lip edge (inward by LIP_WIDTH)
                lip_inner_wire = outer_wire.offset2D(OFFSET - WALL_THICKNESS - LIP_WIDTH)
                
                if lip_outer_wire and lip_inner_wire:
                    # Create the lip as a thin ledge
                    lip_outer = (cq.Workplane("XY")
                                .workplane(offset=lip_z)
                                .add(lip_outer_wire[0])
                                .toPending()
                                .extrude(LIP_HEIGHT))
                    
                    lip_inner = (cq.Workplane("XY")
                                .workplane(offset=lip_z)
                                .add(lip_inner_wire[0])
                                .toPending()
                                .extrude(LIP_HEIGHT + 0.1))
                    
                    # Cut the inner from outer to create the ledge
                    lip = lip_outer.cut(lip_inner)
                    
                    # Add the lip to the case
                    case = case.union(lip)
                    print(f"  ✓ Added {LIP_WIDTH}mm wide plate lip")
                else:
                    print(f"  ⚠ Could not create lip wires")
            except Exception as e:
                print(f"  ⚠ Could not add lip: {e}")
            
        except Exception as e:
            print(f"  ⚠ Offset method failed: {e}")
            print(f"  Falling back to bounding box method...")
            return create_case_bbox_fallback(pcb_file, bb, pcb_thickness, case_height)
        
    except Exception as e:
        print(f"  ⚠ PCB outline extraction failed: {e}")
        print(f"  Falling back to bounding box method...")
        return create_case_bbox_fallback(pcb_file, bb, pcb_thickness, case_height)
    
    # Add screw holes in corners
    screw_inset = 8
    screw_positions = [
        (bb.xmin + screw_inset, bb.ymin + screw_inset),
        (bb.xmin + screw_inset, bb.ymax - screw_inset),
        (bb.xmax - screw_inset, bb.ymin + screw_inset),
        (bb.xmax - screw_inset, bb.ymax - screw_inset),
    ]
    
    for x, y in screw_positions:
        hole = (cq.Workplane("XY")
               .cylinder(case_height + 1, 1.5)
               .translate((x, y, case_height / 2)))
        case = case.cut(hole)
    
    # Add fillets for smooth edges
    try:
        case = case.edges("|Z").fillet(FILLET_RADIUS)
        print(f"  Added {FILLET_RADIUS}mm fillets to vertical edges")
    except:
        print("  Note: Some edges could not be filleted")
    
    return case

def create_case_bbox_fallback(pcb_file, bb, pcb_thickness, case_height):
    """Fallback: Create rectangular case from bounding box"""
    
    print(f"  ⚠ WARNING: Creating RECTANGULAR case (not following PCB outline)")
    
    pcb_width = bb.xmax - bb.xmin
    pcb_depth = bb.ymax - bb.ymin
    
    case_width = pcb_width + 2 * OFFSET
    case_depth = pcb_depth + 2 * OFFSET
    
    # Create outer shell
    outer = (cq.Workplane("XY")
            .box(case_width, case_depth, case_height, centered=False)
            .translate((bb.xmin - OFFSET, bb.ymin - OFFSET, 0)))
    
    # Create inner cavity
    cavity_width = case_width - 2 * WALL_THICKNESS
    cavity_depth = case_depth - 2 * WALL_THICKNESS
    cavity_height = case_height - BOTTOM_THICKNESS + 0.1
    
    cavity = (cq.Workplane("XY")
             .box(cavity_width, cavity_depth, cavity_height, centered=False)
             .translate((bb.xmin - OFFSET + WALL_THICKNESS, 
                        bb.ymin - OFFSET + WALL_THICKNESS, 
                        BOTTOM_THICKNESS)))
    
    case = outer.cut(cavity)
    return case

def generate_cases(left_pcb, right_pcb, output_dir=None):
    """Generate cases for both keyboard halves"""
    
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
    
    # Create cases
    left_case = create_case_from_pcb(left_pcb, "left")
    right_case = create_case_from_pcb(right_pcb, "right")
    
    # Export
    print("\n=== Exporting files ===")
    
    left_step = os.path.join(output_dir, f"{base_name}_case_bottom_left.step")
    left_stl = os.path.join(output_dir, f"{base_name}_case_bottom_left.stl")
    right_step = os.path.join(output_dir, f"{base_name}_case_bottom_right.step")
    right_stl = os.path.join(output_dir, f"{base_name}_case_bottom_right.stl")
    
    exporters.export(left_case, left_step)
    print(f"✓ {os.path.basename(left_step)}")
    
    exporters.export(left_case, left_stl)
    print(f"✓ {os.path.basename(left_stl)}")
    
    exporters.export(right_case, right_step)
    print(f"✓ {os.path.basename(right_step)}")
    
    exporters.export(right_case, right_stl)
    print(f"✓ {os.path.basename(right_stl)}")
    
    print("\n✓ Case generation complete!")
    print(f"\nCase specifications:")
    print(f"  - Wall thickness: {WALL_THICKNESS} mm")
    print(f"  - Bottom thickness: {BOTTOM_THICKNESS} mm")
    print(f"  - PCB clearance: {PCB_CLEARANCE_BOTTOM} mm")
    print(f"  - Offset from PCB edge: {OFFSET} mm")

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_case.py <pcb_left.step> <pcb_right.step> [output_dir]")
        print("\nExample:")
        print("  python generate_case.py keyboard_left.step keyboard_right.step")
        print("  python generate_case.py keyboard_left.step keyboard_right.step ./output")
        sys.exit(1)
    
    left_pcb = sys.argv[1]
    right_pcb = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    generate_cases(left_pcb, right_pcb, output_dir)

if __name__ == "__main__":
    main()
