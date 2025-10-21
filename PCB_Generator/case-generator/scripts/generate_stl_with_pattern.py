#!/usr/bin/env python3
"""
Generate STL files for 3D printing with bottom patterns.

Creates both top frame and bottom tray with decorative patterns.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from build123d import *
from src.constants_lp import *
from src.geometry.profiles_lp import (
    generate_top_frame_profile,
    generate_bottom_tray_profile
)
from src.geometry.patterns import (
    generate_honeycomb_pattern,
    generate_grid_pattern,
    generate_diamond_pattern
)


def profile_to_wire_local(profile):
    """Convert profile to wire."""
    if not profile:
        raise ValueError("Profile must contain at least one point")
    points = [Vector(x, y, 0) for x, y in profile]
    return Wire.make_polygon(points, close=True)


def generate_top_frame_stl():
    """Generate top frame for 3D printing."""
    profile_data = generate_top_frame_profile(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        case_corner_radius=CASE_CORNER_RADIUS,
        pcb_opening_length=PCB_OPENING_LENGTH,
        pcb_opening_width=PCB_OPENING_WIDTH,
        pcb_border=PCB_BORDER,
        usb_cutout_width=USB_CUTOUT_WIDTH,
        usb_cutout_height=USB_CUTOUT_HEIGHT,
        usb_corner_radius=USB_CUTOUT_CORNER_RADIUS,
        usb_center_x=USB_CUTOUT_CENTER_X,
        usb_center_y=USB_CUTOUT_CENTER_Y,
        mounting_holes=MOUNTING_HOLES,
        brass_insert_diameter=BRASS_INSERT_DIAMETER
    )
    
    with BuildPart() as top_frame:
        with BuildSketch() as base_sketch:
            ext_wire = profile_to_wire_local(profile_data['external_profile'])
            make_face(ext_wire)
        extrude(amount=TOP_FRAME_HEIGHT)
        
        # PCB opening
        with BuildSketch(Plane.XY.offset(TOP_FRAME_HEIGHT)) as pcb_sketch:
            pcb_wire = profile_to_wire_local(profile_data['pcb_opening'])
            make_face(pcb_wire)
        extrude(amount=-TOP_FRAME_HEIGHT, mode=Mode.SUBTRACT)
        
        # USB cutout
        with BuildSketch(Plane.XY.offset(TOP_FRAME_HEIGHT)) as usb_sketch:
            usb_wire = profile_to_wire_local(profile_data['usb_cutout'])
            make_face(usb_wire)
        extrude(amount=-TOP_FRAME_HEIGHT, mode=Mode.SUBTRACT)
        
        # Brass insert holes
        for hole_id, hole_profile in profile_data['brass_insert_holes'].items():
            with BuildSketch(Plane.XY) as brass_sketch:
                brass_wire = profile_to_wire_local(hole_profile)
                make_face(brass_wire)
            extrude(amount=BRASS_INSERT_DEPTH, mode=Mode.SUBTRACT)
    
    return top_frame.part


def generate_bottom_tray_stl(pattern_type='honeycomb'):
    """
    Generate bottom tray with pattern for 3D printing.
    
    Args:
        pattern_type: 'honeycomb', 'grid', or 'diamond'
    """
    profile_data = generate_bottom_tray_profile(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        case_corner_radius=CASE_CORNER_RADIUS,
        cavity_length=CAVITY_LENGTH,
        cavity_width=CAVITY_WIDTH,
        cavity_corner_radius=CAVITY_CORNER_RADIUS,
        wall_thickness=WALL_THICKNESS,
        mounting_holes=MOUNTING_HOLES,
        standoff_pillar_diameter=STANDOFF_DIAMETER,
        standoff_hole_diameter=STANDOFF_HOLE_DIAMETER,
        assembly_screw_diameter=ASSEMBLY_SCREW_DIAMETER,
        assembly_counterbore_diameter=ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        rubber_feet_diameter=RUBBER_FEET_DIAMETER
    )
    
    with BuildPart() as bottom_tray:
        # Base
        with BuildSketch() as base_sketch:
            ext_wire = profile_to_wire_local(profile_data['external_profile'])
            make_face(ext_wire)
        extrude(amount=BOTTOM_TRAY_HEIGHT)
        
        # Cavity
        with BuildSketch(Plane.XY.offset(BOTTOM_TRAY_HEIGHT)) as cavity_sketch:
            cavity_wire = profile_to_wire_local(profile_data['internal_cavity'])
            make_face(cavity_wire)
            
            # Subtract standoff pillars
            for pillar_id, pillar_profile in profile_data['standoff_pillars'].items():
                pillar_wire = profile_to_wire_local(pillar_profile)
                make_face(pillar_wire, mode=Mode.SUBTRACT)
        extrude(amount=-CAVITY_DEPTH, mode=Mode.SUBTRACT)
        
        # Standoff holes
        for hole_id, hole_profile in profile_data['standoff_holes'].items():
            with BuildSketch(Plane.XY.offset(BOTTOM_TRAY_HEIGHT)) as standoff_hole_sketch:
                hole_wire = profile_to_wire_local(hole_profile)
                make_face(hole_wire)
            extrude(amount=-(CAVITY_DEPTH + ASSEMBLY_SCREW_COUNTERBORE_DEPTH), mode=Mode.SUBTRACT)
        
        # Assembly screw counterbores
        for hole_id, counterbore_profile in profile_data['assembly_counterbores'].items():
            with BuildSketch(Plane.XY) as counterbore_sketch:
                cb_wire = profile_to_wire_local(counterbore_profile)
                make_face(cb_wire)
            extrude(amount=ASSEMBLY_SCREW_COUNTERBORE_DEPTH, mode=Mode.SUBTRACT)
        
        # Assembly screw through-holes
        for hole_id, screw_profile in profile_data['assembly_screw_holes'].items():
            with BuildSketch(Plane.XY.offset(BOTTOM_TRAY_HEIGHT)) as screw_sketch:
                screw_wire = profile_to_wire_local(screw_profile)
                make_face(screw_wire)
            extrude(amount=-BOTTOM_TRAY_HEIGHT, mode=Mode.SUBTRACT)
        
        # Rubber feet recesses
        for feet_profile in profile_data['rubber_feet_recesses']:
            with BuildSketch(Plane.XY) as feet_sketch:
                feet_wire = profile_to_wire_local(feet_profile)
                make_face(feet_wire)
            extrude(amount=RUBBER_FEET_DEPTH, mode=Mode.SUBTRACT)
        
        # Create exclusion zones around mounting holes (keep solid for screw mounts)
        # Use 12mm radius around each mounting hole to keep structure solid
        exclusion_zones = [(pos, 12.0) for pos in MOUNTING_HOLES.values()]
        
        # Also exclude rubber feet areas
        for pos in RUBBER_FEET_POSITIONS:
            exclusion_zones.append((pos, 8.0))
        
        # Add decorative pattern on bottom
        if pattern_type == 'honeycomb':
            pattern = generate_honeycomb_pattern(
                CASE_LENGTH, CASE_WIDTH, hex_size=6, exclusion_zones=exclusion_zones
            )
        elif pattern_type == 'grid':
            pattern = generate_grid_pattern(
                CASE_LENGTH, CASE_WIDTH, cell_size=8, exclusion_zones=exclusion_zones
            )
        elif pattern_type == 'diamond':
            pattern = generate_diamond_pattern(
                CASE_LENGTH, CASE_WIDTH, diamond_size=10, exclusion_zones=exclusion_zones
            )
        else:
            pattern = []
        
        # Cut pattern all the way through bottom (BASE_THICKNESS = 3mm)
        for shape in pattern:
            with BuildSketch(Plane.XY) as pattern_sketch:
                shape_wire = profile_to_wire_local(shape)
                make_face(shape_wire)
            extrude(amount=BASE_THICKNESS, mode=Mode.SUBTRACT)
    
    return bottom_tray.part


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate STL files for 3D printing')
    parser.add_argument('--pattern', choices=['honeycomb', 'grid', 'diamond', 'none'],
                       default='honeycomb', help='Bottom pattern type')
    parser.add_argument('--output-dir', default='output/stl',
                       help='Output directory for STL files')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating STL files with {args.pattern} pattern...")
    
    # Generate top frame
    print("  Generating top frame...")
    top_frame = generate_top_frame_stl()
    top_path = output_dir / 'top_frame.stl'
    export_stl(top_frame, str(top_path))
    print(f"  ✓ Saved: {top_path}")
    
    # Generate bottom tray
    print(f"  Generating bottom tray ({args.pattern})...")
    bottom_tray = generate_bottom_tray_stl(pattern_type=args.pattern if args.pattern != 'none' else None)
    bottom_path = output_dir / f'bottom_tray_{args.pattern}.stl'
    export_stl(bottom_tray, str(bottom_path))
    print(f"  ✓ Saved: {bottom_path}")
    
    print(f"\nDone! Files saved to {output_dir}/")
    print(f"  - top_frame.stl")
    print(f"  - bottom_tray_{args.pattern}.stl")
