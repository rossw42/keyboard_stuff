"""Switch plate generation with cutouts."""

import logging
from typing import List, Tuple, Optional

import cadquery as cq

from .config import CaseConfig
from .pcb_analyzer import PCBInfo
from .switch_detector import SwitchInfo, SwitchLayout
from .geometry_utils import offset_outline, rotate_point_2d

logger = logging.getLogger(__name__)


def create_plate_base(
    outline: List[Tuple[float, float]],
    offset: float,
    thickness: float,
    corner_radius: float,
    wire=None
) -> cq.Workplane:
    """
    Create solid plate base.
    
    Args:
        outline: PCB outline points
        offset: Distance to offset from PCB
        thickness: Plate thickness
        corner_radius: Corner radius
        
    Returns:
        CadQuery workplane with plate base
    """
    logger.info("Creating plate base...")
    logger.info(f"  Wire object: {type(wire) if wire is not None else 'None'}")
    logger.info(f"  Plate offset: {offset}mm")
    
    # Use the original wire object if available (smooth results)
    if wire is not None:
        try:
            logger.info("  Using original PCB wire for smooth outline")
            
            # Use the original wire directly
            offset_wires = wire.offset2D(offset)
            
            if not offset_wires:
                raise Exception("Wire offset returned empty")
            
            # Create plate
            plate = (cq.Workplane("XY")
                    .add(offset_wires[0])
                    .toPending()
                    .extrude(thickness))
            logger.info("  ✓ Created smooth plate using wire offset")
            return plate
            
        except Exception as e:
            logger.warning(f"Wire-based offset failed: {e}, falling back to points")
    
    # Fallback to point-based approach
    logger.info("  Using point-based approach (may have artifacts)")
    from .geometry_utils import simplify_outline, offset_outline
    simplified = simplify_outline(outline, tolerance=0.2)
    plate_outline = offset_outline(simplified, offset)
    plate = cq.Workplane("XY").polyline(plate_outline).close().extrude(thickness)
    
    return plate


def create_plate_from_switches(
    switches: List[SwitchInfo],
    cutout_size: float,
    margin: float,
    thickness: float,
    corner_radius: float = 2.0
) -> cq.Workplane:
    """
    Create plate base from switch positions with proper margins.
    
    This ensures all switch cutouts are fully enclosed by calculating
    the bounding box of all switches and adding margin.
    
    Args:
        switches: List of switch positions
        cutout_size: Size of switch cutout (14mm for MX)
        margin: Margin around switches (mm)
        thickness: Plate thickness
        corner_radius: Corner radius for rounded rectangle
        
    Returns:
        CadQuery workplane with plate base
    """
    if not switches:
        raise ValueError("No switches provided")
    
    # Calculate bounding box of all switches
    xs = [s.position[0] for s in switches]
    ys = [s.position[1] for s in switches]
    
    # Add half cutout size plus margin
    half_cutout = cutout_size / 2
    x_min = min(xs) - half_cutout - margin
    x_max = max(xs) + half_cutout + margin
    y_min = min(ys) - half_cutout - margin
    y_max = max(ys) + half_cutout + margin
    
    width = x_max - x_min
    height = y_max - y_min
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    
    logger.info(f"  Plate from switches: {width:.1f}mm × {height:.1f}mm")
    logger.info(f"  Center: ({center_x:.1f}, {center_y:.1f})")
    logger.info(f"  Margin: {margin}mm around all switches")
    
    # Create rounded rectangle
    plate = (cq.Workplane("XY")
            .center(center_x, center_y)
            .rect(width, height)
            .extrude(thickness))
    
    # Apply corner radius if specified
    if corner_radius > 0:
        try:
            plate = plate.edges("|Z").fillet(corner_radius)
        except:
            logger.warning(f"  Failed to apply corner radius, continuing without")
    
    return plate


def create_switch_cutouts(
    plate: cq.Workplane,
    switches: List[SwitchInfo],
    cutout_size: float,
    plate_thickness: float = 1.5
) -> cq.Workplane:
    """
    Add switch cutouts to plate.
    
    Args:
        plate: Plate base workplane
        switches: List of switch positions
        cutout_size: Size of square cutout (mm)
        plate_thickness: Thickness of plate (mm)
        
    Returns:
        Plate with cutouts
    """
    logger.info(f"Creating {len(switches)} switch cutouts...")
    
    # Get switch positions for batch creation
    switch_points = [(s.position[0], s.position[1]) for s in switches]
    
    # Create all cutouts at once using pushPoints and rect
    # This is more reliable than individual polyline cutouts
    try:
        cutouts = (cq.Workplane("XY")
                  .workplane(offset=-1)  # Start below plate
                  .pushPoints(switch_points)
                  .rect(cutout_size, cutout_size)
                  .extrude(plate_thickness + 2))  # Through entire plate
        
        plate = plate.cut(cutouts)
        logger.info(f"  ✓ Added {len(switches)} switch cutouts")
        
    except Exception as e:
        logger.warning(f"  Batch cutout failed: {e}, trying individual cutouts...")
        
        # Fallback: create cutouts individually
        for i, switch in enumerate(switches):
            x, y = switch.position
            try:
                cutout = (cq.Workplane("XY")
                         .workplane(offset=-1)
                         .center(x, y)
                         .rect(cutout_size, cutout_size)
                         .extrude(plate_thickness + 2))
                plate = plate.cut(cutout)
            except Exception as e2:
                logger.warning(f"  Failed to create cutout {i+1} at ({x:.2f}, {y:.2f}): {e2}")
    
    return plate


def create_mounting_holes(
    plate: cq.Workplane,
    positions: List[Tuple[float, float]],
    hole_diameter: float
) -> cq.Workplane:
    """
    Add mounting holes to plate.
    
    Args:
        plate: Plate workplane
        positions: List of (x, y) positions
        hole_diameter: Hole diameter
        
    Returns:
        Plate with mounting holes
    """
    logger.info(f"Creating {len(positions)} mounting holes...")
    
    for x, y in positions:
        hole = (cq.Workplane("XY")
               .center(x, y)
               .circle(hole_diameter / 2)
               .extrude(100))  # Through entire plate
        
        plate = plate.cut(hole)
    
    return plate


def create_switch_plate(
    pcb_info: PCBInfo,
    switch_layout: Optional[SwitchLayout],
    config: CaseConfig
) -> cq.Workplane:
    """
    Generate complete switch plate geometry.
    
    Args:
        pcb_info: PCB information
        switch_layout: Switch layout (optional)
        config: Case configuration
        
    Returns:
        CadQuery workplane with complete switch plate
    """
    logger.info("Generating switch plate...")
    
    # Calculate required offset to ensure all switches are enclosed
    if switch_layout and switch_layout.switches:
        # Find minimum distance from any switch to PCB edge
        half_cutout = config.switch_cutout_size / 2
        min_margin = float('inf')
        
        for switch in switch_layout.switches:
            x, y = switch.position
            # Calculate distance to PCB edges
            dist_to_left = x - pcb_info.bounding_box[0]
            dist_to_right = pcb_info.bounding_box[2] - x
            dist_to_bottom = y - pcb_info.bounding_box[1]
            dist_to_top = pcb_info.bounding_box[3] - y
            
            # Check if switch extends beyond PCB
            needed_left = half_cutout - dist_to_left
            needed_right = half_cutout - dist_to_right
            needed_bottom = half_cutout - dist_to_bottom
            needed_top = half_cutout - dist_to_top
            
            min_margin = min(min_margin, dist_to_left, dist_to_right, dist_to_bottom, dist_to_top)
        
        # Calculate required offset: if switches are too close to edge, expand outward
        required_margin = half_cutout + 2.0  # 7mm + 2mm safety margin
        if min_margin < required_margin:
            calculated_offset = -(required_margin - min_margin)
            logger.info(f"  Switches too close to edge (min: {min_margin:.1f}mm)")
            logger.info(f"  Expanding plate by {-calculated_offset:.1f}mm to ensure enclosure")
        else:
            calculated_offset = config.plate_offset
            logger.info(f"  Switches have adequate margin ({min_margin:.1f}mm)")
    else:
        calculated_offset = config.plate_offset
    
    # Create plate base with calculated offset
    plate = create_plate_base(
        pcb_info.outline,
        calculated_offset,
        config.plate_thickness,
        config.corner_radius,
        pcb_info.wire
    )
    
    # Add switch cutouts if we have switch data
    if switch_layout and switch_layout.switches:
        logger.info(f"Switch layout has {len(switch_layout.switches)} switches")
        plate = create_switch_cutouts(
            plate,
            switch_layout.switches,
            config.switch_cutout_size,
            config.plate_thickness
        )
    else:
        logger.info("No switch data provided, generating solid plate")
    
    # Add mounting holes
    if pcb_info.mounting_holes:
        # Use slightly larger holes for plate (clearance for screws)
        plate_hole_diameter = config.boss_hole_diameter + 0.5
        plate = create_mounting_holes(
            plate,
            pcb_info.mounting_holes,
            plate_hole_diameter
        )
    
    logger.info("Switch plate generation complete")
    return plate
