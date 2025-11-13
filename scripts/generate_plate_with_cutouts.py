#!/usr/bin/env python3
"""
Generate switch plates with automatic switch cutouts from KiCad PCB file
Usage: python generate_plate_with_cutouts.py <kicad_pcb_file> <pcb_left.step> <pcb_right.step> [output_dir]
"""

import sys
import os
import re
import cadquery as cq
from cadquery import exporters

# Plate parameters
PLATE_THICKNESS = 1.5  # Standard for Cherry MX switches
PLATE_OFFSET = 1.0  # How far plate extends beyond PCB edge
SWITCH_CUTOUT_SIZE = 14.0  # Cherry MX and Choc switch cutout (14x14mm)

def parse_switches_from_kicad(pcb_file):
    """Extract switch positions from KiCad PCB file"""
    
    print(f"Parsing switches from: {os.path.basename(pcb_file)}")
    
    with open(pcb_file, 'r') as f:
        content = f.read()
    
    # Look for switch modules/footprints
    switch_pattern = r'\((?:module|footprint)\s+"?[^"]*(?:SW_|MX_|Hotswap|PG1350|Switch)[^"]*"?[^)]*?\(at\s+([\d.-]+)\s+([\d.-]+)(?:\s+([\d.-]+))?\)'
    
    switches = []
    for match in re.finditer(switch_pattern, content, re.IGNORECASE | re.DOTALL):
        x = float(match.group(1))
        y = float(match.group(2))
        rotation = float(match.group(3)) if match.group(3) else 0
        
        switches.append({'x': x, 'y': y, 'rotation': rotation})
    
    print(f"  Found {len(switches)} switches")
    
    # Try to find the aux_axis_origin (STEP export origin)
    origin_pattern = r'\(aux_axis_origin\s+([\d.-]+)\s+([\d.-]+)\)'
    origin_match = re.search(origin_pattern, content)
    
    if origin_match:
        origin_x = float(origin_match.group(1))
        origin_y = float(origin_match.group(2))
        print(f"  Found STEP origin offset: ({origin_x:.2f}, {origin_y:.2f})")
        
        # Transform all switch coordinates to STEP coordinate system
        for sw in switches:
            sw['x'] -= origin_x
            sw['y'] = -(sw['y'] - origin_y)  # Y is inverted in STEP
        
        print(f"  Transformed switches to STEP coordinates")
    else:
        print(f"  ⚠ No aux_axis_origin found, coordinates may not match STEP export")
    
    return switches

def create_plate_with_cutouts(pcb_file, switches, side='left'):
    """Create a switch plate with cutouts following PCB outline"""
    
    print(f"\nCreating {side} plate with switch cutouts...")
    
    # Import PCB
    pcb = cq.importers.importStep(pcb_file)
    pcb_shape = pcb.val()
    bb = pcb_shape.BoundingBox()
    
    print(f"  PCB bounds: X({bb.xmin:.2f}, {bb.xmax:.2f}), Y({bb.ymin:.2f}, {bb.ymax:.2f})")
    
    # Filter switches for this half
    if side == 'left':
        half_switches = [s for s in switches if s['x'] < (bb.xmax + 5)]
    else:
        half_switches = [s for s in switches if s['x'] > (bb.xmin - 5)]
    
    print(f"  Switches in this half: {len(half_switches)}")
    
    # Trace PCB outline
    try:
        wp = cq.Workplane("XY").add(pcb_shape)
        faces = wp.faces().vals()
        largest_face = max(faces, key=lambda f: f.Area())
        outer_wire = largest_face.outerWire()
        
        # Create offset wire for plate
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
        print(f"  ⚠ Outline tracing failed: {e}, using bounding box")
        pcb_width = bb.xmax - bb.xmin
        pcb_depth = bb.ymax - bb.ymin
        plate_width = pcb_width + 2 * PLATE_OFFSET
        plate_depth = pcb_depth + 2 * PLATE_OFFSET
        
        plate = (cq.Workplane("XY")
                .box(plate_width, plate_depth, PLATE_THICKNESS, centered=False)
                .translate((bb.xmin - PLATE_OFFSET, bb.ymin - PLATE_OFFSET, 0)))
    
    # Add switch cutouts
    print(f"  Adding {len(half_switches)} switch cutouts...")
    
    # Get plate Z position to ensure cutouts go through it
    plate_bb = plate.val().BoundingBox()
    plate_z_min = plate_bb.zmin
    plate_z_max = plate_bb.zmax
    
    # Collect all switch positions
    switch_points = [(sw['x'], sw['y']) for sw in half_switches]
    
    # Create all cutouts on a single workplane, starting below the plate
    cutout_wp = (cq.Workplane("XY")
                .workplane(offset=plate_z_min - 1)
                .pushPoints(switch_points)
                .rect(SWITCH_CUTOUT_SIZE, SWITCH_CUTOUT_SIZE, forConstruction=False)
                .extrude(plate_z_max - plate_z_min + 2))  # Through the entire plate
    
    # Cut all at once
    try:
        plate = plate.cut(cutout_wp)
        print(f"  ✓ Added {len(half_switches)} switch cutouts")
    except Exception as e:
        print(f"  ⚠ Failed to add cutouts: {e}")
        import traceback
        traceback.print_exc()
    
    # Add mounting holes
    hole_inset = 5
    hole_diameter = 2.5
    
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
    
    # Add fillets
    try:
        plate = plate.edges("|Z").fillet(1.0)
    except:
        pass
    
    return plate

def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_plate_with_cutouts.py <kicad_pcb_file> <pcb_left.step> <pcb_right.step> [output_dir]")
        print("\nExample:")
        print("  python generate_plate_with_cutouts.py keyboard.kicad_pcb keyboard_pcb_left.step keyboard_pcb_right.step")
        sys.exit(1)
    
    kicad_file = sys.argv[1]
    left_pcb = sys.argv[2]
    right_pcb = sys.argv[3]
    output_dir = sys.argv[4] if len(sys.argv) > 4 else os.path.dirname(left_pcb)
    
    if not os.path.exists(kicad_file):
        print(f"Error: KiCad file not found: {kicad_file}")
        sys.exit(1)
    
    if not os.path.exists(left_pcb) or not os.path.exists(right_pcb):
        print(f"Error: PCB STEP files not found")
        sys.exit(1)
    
    # Parse switches from KiCad file
    switches = parse_switches_from_kicad(kicad_file)
    
    if not switches:
        print("\n✗ No switches found in KiCad file")
        print("  Cannot generate plates with cutouts")
        sys.exit(1)
    
    # Get base name
    base_name = os.path.splitext(os.path.basename(left_pcb))[0].replace('_pcb_left', '').replace('_left', '')
    
    # Create plates
    left_plate = create_plate_with_cutouts(left_pcb, switches, 'left')
    right_plate = create_plate_with_cutouts(right_pcb, switches, 'right')
    
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
    
    print("\n✓ Plate generation complete with switch cutouts!")
    print(f"\nPlate specifications:")
    print(f"  - Thickness: {PLATE_THICKNESS} mm")
    print(f"  - Switch cutouts: {SWITCH_CUTOUT_SIZE}x{SWITCH_CUTOUT_SIZE} mm")
    print(f"  - Total switches: {len(switches)}")

if __name__ == "__main__":
    main()
