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
    
    # Create plate base
    plate = create_plate_base(
        pcb_info.outline,
        config.plate_offset,
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
