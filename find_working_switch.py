#!/usr/bin/env python3
"""
Find which switch coordinate actually worked
"""

import re
import cadquery as cq

# Parse switches from KiCad
with open("keyboards/hypergarlic/hypergarlic.kicad_pcb") as f:
    content = f.read()

switch_pattern = r'\((?:module|footprint)\s+"?[^"]*(?:SW_|PG1350)[^"]*"?[^)]*?\(at\s+([\d.-]+)\s+([\d.-]+)'
switches = []
for match in re.finditer(switch_pattern, content, re.IGNORECASE | re.DOTALL):
    x = float(match.group(1))
    y = float(match.group(2))
    switches.append({'x': x, 'y': y, 'kicad_x': x, 'kicad_y': y})

print(f"Found {len(switches)} switches in KiCad")

# Transform them (current transformation)
for sw in switches:
    sw['x'] -= 0  # origin_x
    sw['y'] = -(sw['y'] - 0)  # Y inverted

# Load plate and find the hole
plate = cq.importers.importStep("keyboards/hypergarlic/hypergarlic_plate_left.step")
plate_bb = plate.val().BoundingBox()

print(f"\nPlate bounds: X({plate_bb.xmin:.2f}, {plate_bb.xmax:.2f}), Y({plate_bb.ymin:.2f}, {plate_bb.ymax:.2f})")

# Find holes in plate
faces = plate.faces().vals()
hole_centers = []
for face in faces:
    for wire in face.innerWires():
        bb = wire.BoundingBox()
        # Check if it's a switch-sized hole
        width = max(bb.xmax - bb.xmin, bb.zmax - bb.zmin)
        depth = max(bb.ymax - bb.ymin, bb.zmax - bb.zmin)
        if 12 < width < 16 and 12 < depth < 16:
            center_x = (bb.xmin + bb.xmax) / 2
            center_y = (bb.ymin + bb.ymax) / 2
            hole_centers.append((center_x, center_y))
            print(f"\nHole found at: ({center_x:.2f}, {center_y:.2f})")

# Find which switch is closest to the hole
if hole_centers:
    hole_x, hole_y = hole_centers[0]
    
    # Filter to left half
    left_switches = [s for s in switches if s['kicad_x'] < 140]
    
    print(f"\nChecking {len(left_switches)} left switches...")
    print(f"\nClosest switches to hole:")
    
    distances = []
    for sw in left_switches:
        dist = ((sw['x'] - hole_x)**2 + (sw['y'] - hole_y)**2)**0.5
        distances.append((dist, sw))
    
    distances.sort()
    
    for i, (dist, sw) in enumerate(distances[:5]):
        print(f"  {i+1}. KiCad({sw['kicad_x']:.2f}, {sw['kicad_y']:.2f}) → Transformed({sw['x']:.2f}, {sw['y']:.2f}) - Distance: {dist:.2f}mm")
    
    # Calculate what the offset should be
    best_sw = distances[0][1]
    print(f"\nBest match switch:")
    print(f"  KiCad: ({best_sw['kicad_x']:.2f}, {best_sw['kicad_y']:.2f})")
    print(f"  Hole:  ({hole_x:.2f}, {hole_y:.2f})")
    print(f"\nRequired offset:")
    print(f"  X offset: {hole_x - best_sw['kicad_x']:.2f}")
    print(f"  Y offset: {hole_y - best_sw['kicad_y']:.2f}")
