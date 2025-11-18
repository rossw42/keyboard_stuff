"""Sandwich mount case generation (walls extend downward from plate)."""

import logging
from typing import List, Tuple

import cadquery as cq

from .config import CaseConfig
from .pcb_analyzer import PCBInfo

logger = logging.getLogger(__name__)


def create_sandwich_body(
    outline: List[Tuple[float, float]],
    inner_offset: float,
    outer_offset: float,
    wall_height: float,
    bottom_thickness: float,
    plate_thickness: float,
    wire=None
) -> cq.Workplane:
    """
    Create sandwich mount body with walls extending downward.
    
    The body consists of:
    - A flat top plate at Z=0 to Z=plate_thickness (for switch mounting)
    - Walls extending downward from the plate
    - A bottom floor at the bottom
    
    Args:
        outline: PCB outline points
        inner_offset: Inner wall offset from PCB (for PCB clearance)
        outer_offset: Outer wall offset from PCB (defines case size)
        wall_height: Height of walls extending downward (negative Z)
        bottom_thickness: Thickness of bottom floor
        plate_thickness: Thickness of top plate (for switch mounting)
        wire: Optional CadQuery wire for smooth offsetting
        
    Returns:
        CadQuery workplane with sandwich body
    """
    logger.info("Creating sandwich mount body...")
    logger.info(f"  Inner offset: {inner_offset}mm, Outer offset: {outer_offset}mm")
    logger.info(f"  Wall height: {wall_height}mm (downward)")
    logger.info(f"  Plate thickness: {plate_thickness}mm")
    logger.info(f"  Bottom thickness: {bottom_thickness}mm")
    
    if wire is not None:
        try:
            # Create outer and inner wires
            outer_wires = wire.offset2D(outer_offset)
            inner_wires = wire.offset2D(inner_offset)
            
            if not outer_wires or not inner_wires:
                raise Exception("Wire offset returned empty")
            
            # Create top plate (solid plate at Z=0 to plate_thickness)
            top_plate = (cq.Workplane("XY")
                        .add(outer_wires[0])
                        .toPending()
                        .extrude(plate_thickness))
            
            # Create outer shell extending downward from Z=0
            outer_shell = (cq.Workplane("XY")
                          .add(outer_wires[0])
                          .toPending()
                          .extrude(-wall_height))  # Negative = downward from Z=0
            
            # Create inner cavity
            inner_cavity = (cq.Workplane("XY")
                           .add(inner_wires[0])
                           .toPending()
                           .extrude(-wall_height))  # Negative = downward from Z=0
            
            # Subtract inner from outer to create walls
            walls = outer_shell.cut(inner_cavity)
            
            # Combine top plate and walls (no bottom floor - that's the separate bottom plate)
            body = top_plate.union(walls)
            
            logger.info("  ✓ Created smooth sandwich body using wire offset")
            return body
            
        except Exception as e:
            logger.warning(f"Wire offset failed: {e}, falling back to point-based method")
    
    # Fallback: use point-based method
    from .geometry_utils import simplify_outline, offset_outline
    
    simplified = simplify_outline(outline, tolerance=0.2)
    outer_outline = offset_outline(simplified, outer_offset)
    inner_outline = offset_outline(simplified, inner_offset)
    
    # Create top plate
    top_plate = cq.Workplane("XY").polyline(outer_outline).close().extrude(plate_thickness)
    
    # Create walls from Z=0 downward
    outer_solid = (cq.Workplane("XY")
                  .polyline(outer_outline)
                  .close()
                  .extrude(-wall_height))
    inner_solid = (cq.Workplane("XY")
                  .polyline(inner_outline)
                  .close()
                  .extrude(-wall_height))
    walls = outer_solid.cut(inner_solid)
    
    # Combine top plate and walls (no bottom floor)
    body = top_plate.union(walls)
    
    logger.info("  ✓ Created sandwich body using point-based method")
    return body


def create_sandwich_mounting_posts(
    positions: List[Tuple[float, float]],
    boss_diameter: float,
    wall_height: float,
    hole_diameter: float
) -> cq.Workplane:
    """
    Create mounting posts for sandwich mount (extend from top to bottom).
    
    Args:
        positions: List of (x, y) positions for posts
        boss_diameter: Boss outer diameter
        wall_height: Height of walls (posts extend this far down)
        hole_diameter: Through-hole diameter for screws
        
    Returns:
        CadQuery workplane with mounting posts
    """
    logger.info(f"Creating {len(positions)} sandwich mounting posts...")
    
    if not positions:
        return cq.Workplane("XY")
    
    result = None
    
    for x, y in positions:
        # Create boss cylinder from Z=0 (plate level) down to bottom
        boss = (cq.Workplane("XY")
                .center(x, y)
                .circle(boss_diameter / 2)
                .extrude(-wall_height))  # Extend downward
        
        # Create through-hole
        hole = (cq.Workplane("XY")
                .center(x, y)
                .circle(hole_diameter / 2)
                .extrude(-wall_height - 1))  # Slightly longer to ensure clean cut
        
        # Subtract hole from boss
        boss = boss.cut(hole)
        
        # Add to result
        if result is None:
            result = boss
        else:
            result = result.union(boss)
    
    return result


def create_sandwich_case(
    pcb_info: PCBInfo,
    config: CaseConfig,
    switch_layout=None
) -> cq.Workplane:
    """
    Generate complete sandwich mount case body.
    
    The sandwich mount design has:
    - Flat rim at plate level (Z=0)
    - Walls extending downward
    - Bottom floor
    - Mounting posts from top to bottom
    
    Args:
        pcb_info: PCB information
        config: Case configuration
        switch_layout: Optional switch layout
        
    Returns:
        CadQuery workplane with sandwich case body
    """
    logger.info("Generating sandwich mount case...")
    
    # Calculate offsets
    # Inner offset = PCB + tolerance (1mm)
    inner_offset = config.case_offset
    # Outer offset = inner + wall thickness
    outer_offset = inner_offset + config.wall_thickness
    
    # Wall height (how far down the walls extend from bottom of plate)
    # case_height is the total height of the top frame (plate + walls)
    # So walls = case_height - plate_thickness
    wall_height = config.case_height - config.plate_thickness
    
    # Create body
    body = create_sandwich_body(
        pcb_info.outline,
        inner_offset,
        outer_offset,
        wall_height,
        config.bottom_thickness,
        config.plate_thickness,
        wire=pcb_info.wire
    )
    
    # Add mounting posts if we have mounting holes
    if pcb_info.mounting_holes:
        mounting_holes = pcb_info.mounting_holes
        
        # Filter out holes too close to switches
        if switch_layout and switch_layout.switches:
            from .bottom_tray import filter_mounting_holes_away_from_switches
            switch_positions = [(s.position[0], s.position[1]) for s in switch_layout.switches]
            mounting_holes = filter_mounting_holes_away_from_switches(
                mounting_holes,
                switch_positions,
                min_distance=10.0
            )
            logger.info(f"Using {len(mounting_holes)} of {len(pcb_info.mounting_holes)} mounting holes")
        
        if mounting_holes:
            posts = create_sandwich_mounting_posts(
                mounting_holes,
                config.boss_diameter,
                wall_height,
                config.boss_hole_diameter
            )
            body = body.union(posts)
    
    logger.info("Sandwich mount case generation complete")
    return body
