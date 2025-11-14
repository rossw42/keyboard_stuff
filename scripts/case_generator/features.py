"""Feature application: chamfers, fillets, rubber feet, plate lips, boss placement."""

import logging
from typing import List, Tuple

import cadquery as cq

from .geometry_utils import offset_outline, calculate_bounding_box

logger = logging.getLogger(__name__)


def apply_chamfers(
    part: cq.Workplane,
    outer_chamfer: float,
    inner_chamfer: float,
    edge_selector: str = "|Z"
) -> cq.Workplane:
    """
    Apply chamfers to edges.
    
    Args:
        part: Part to chamfer
        outer_chamfer: Outer edge chamfer size
        inner_chamfer: Inner edge chamfer size
        edge_selector: Edge selection string
        
    Returns:
        Chamfered part
    """
    try:
        logger.info(f"Applying chamfers (outer={outer_chamfer}mm, inner={inner_chamfer}mm)...")
        
        # Try to apply chamfer to vertical edges
        # This is a simplified approach - in practice, you'd need to
        # distinguish between inner and outer edges
        chamfered = part.edges(edge_selector).chamfer(outer_chamfer)
        
        logger.info("  Chamfers applied successfully")
        return chamfered
        
    except Exception as e:
        logger.warning(f"Failed to apply chamfers: {e}, continuing without chamfers")
        return part


def apply_fillets(
    part: cq.Workplane,
    radius: float,
    edge_selector: str = "|Z"
) -> cq.Workplane:
    """
    Apply fillets to edges.
    
    Args:
        part: Part to fillet
        radius: Fillet radius
        edge_selector: Edge selection string
        
    Returns:
        Filleted part
    """
    try:
        logger.info(f"Applying fillets (radius={radius}mm)...")
        
        filleted = part.edges(edge_selector).fillet(radius)
        
        logger.info("  Fillets applied successfully")
        return filleted
        
    except Exception as e:
        logger.warning(f"Failed to apply fillets: {e}, continuing without fillets")
        return part


def add_rubber_feet_recesses(
    tray: cq.Workplane,
    bounding_box: Tuple[float, float, float, float],
    diameter: float,
    depth: float,
    corner_offset: float
) -> cq.Workplane:
    """
    Add rubber feet recesses to bottom surface.
    
    Args:
        tray: Bottom tray workplane
        bounding_box: (xmin, ymin, xmax, ymax) of case
        diameter: Recess diameter
        depth: Recess depth
        corner_offset: Distance from corner to recess center
        
    Returns:
        Tray with rubber feet recesses
    """
    logger.info("Adding rubber feet recesses...")
    
    xmin, ymin, xmax, ymax = bounding_box
    
    # Calculate positions (4 corners)
    positions = [
        (xmin + corner_offset, ymin + corner_offset),  # Bottom-left
        (xmax - corner_offset, ymin + corner_offset),  # Bottom-right
        (xmin + corner_offset, ymax - corner_offset),  # Top-left
        (xmax - corner_offset, ymax - corner_offset),  # Top-right
    ]
    
    for x, y in positions:
        # Create recess (cylinder subtracted from bottom)
        recess = (cq.Workplane("XY")
                 .center(x, y)
                 .circle(diameter / 2)
                 .extrude(-depth))
        
        tray = tray.cut(recess)
    
    logger.info(f"  Added {len(positions)} rubber feet recesses")
    return tray


def add_plate_mounting_lip(
    tray: cq.Workplane,
    outline: List[Tuple[float, float]],
    wall_thickness: float,
    lip_width: float,
    lip_height: float,
    lip_z_position: float,
    case_offset: float,
    wire=None
) -> cq.Workplane:
    """
    Add inward lip for plate mounting.
    
    Args:
        tray: Bottom tray workplane
        outline: PCB outline
        wall_thickness: Case wall thickness
        lip_width: Width of lip extending inward
        lip_height: Height of lip
        lip_z_position: Z position of lip bottom
        case_offset: Offset from PCB to case outer edge
        wire: Original PCB wire for smooth offsetting
        
    Returns:
        Tray with plate mounting lip
    """
    logger.info("Adding plate mounting lip...")
    
    try:
        # Use wire-based offset if available
        if wire is not None:
            try:
                # Outer edge of lip (at inner wall surface)
                # Inner wall is at: case_offset - wall_thickness from PCB
                lip_outer_wires = wire.offset2D(case_offset - wall_thickness)
                
                # Inner edge of lip (inward by lip_width)
                lip_inner_wires = wire.offset2D(case_offset - wall_thickness - lip_width)
                
                if not lip_outer_wires or not lip_inner_wires:
                    raise Exception("Wire offset returned empty")
                
                # Create lip as a ring at the specified Z position
                outer_solid = (cq.Workplane("XY")
                              .workplane(offset=lip_z_position)
                              .add(lip_outer_wires[0])
                              .toPending()
                              .extrude(lip_height))
                
                inner_solid = (cq.Workplane("XY")
                              .workplane(offset=lip_z_position)
                              .add(lip_inner_wires[0])
                              .toPending()
                              .extrude(lip_height + 0.1))
                
                lip = outer_solid.cut(inner_solid)
                
                # Add lip to tray
                tray = tray.union(lip)
                
                logger.info("  ✓ Plate mounting lip added using wire offset")
                return tray
                
            except Exception as e:
                logger.warning(f"Wire-based lip failed: {e}, falling back to point-based")
        
        # Fallback: point-based method
        lip_outer = offset_outline(outline, case_offset - wall_thickness)
        lip_inner = offset_outline(outline, case_offset - wall_thickness - lip_width)
        
        # Create lip as a ring
        outer_wire = cq.Workplane("XY").workplane(offset=lip_z_position).polyline(lip_outer).close()
        outer_solid = outer_wire.extrude(lip_height)
        
        inner_wire = cq.Workplane("XY").workplane(offset=lip_z_position).polyline(lip_inner).close()
        inner_solid = inner_wire.extrude(lip_height + 0.1)
        
        lip = outer_solid.cut(inner_solid)
        
        # Add lip to tray
        tray = tray.union(lip)
        
        logger.info("  Plate mounting lip added successfully")
        return tray
        
    except Exception as e:
        logger.warning(f"Failed to add plate mounting lip: {e}, continuing without lip")
        return tray


def auto_place_screw_bosses(
    outline: List[Tuple[float, float]],
    mounting_holes: List[Tuple[float, float]],
    boss_diameter: float,
    corner_inset: float
) -> List[Tuple[float, float]]:
    """
    Determine optimal screw boss positions.
    
    Args:
        outline: PCB outline
        mounting_holes: Detected PCB mounting holes
        boss_diameter: Boss diameter
        corner_inset: Inset from corners if no holes detected
        
    Returns:
        List of (x, y) positions for bosses
    """
    # If we have detected mounting holes, use those
    if mounting_holes:
        logger.info(f"Using {len(mounting_holes)} detected mounting holes for boss placement")
        return mounting_holes
    
    # Otherwise, place at corners
    logger.info("No mounting holes detected, placing bosses at corners")
    
    bbox = calculate_bounding_box(outline)
    xmin, ymin, xmax, ymax = bbox
    
    # Place at 4 corners with inset
    positions = [
        (xmin + corner_inset, ymin + corner_inset),
        (xmax - corner_inset, ymin + corner_inset),
        (xmin + corner_inset, ymax - corner_inset),
        (xmax - corner_inset, ymax - corner_inset),
    ]
    
    logger.info(f"Placed {len(positions)} bosses at corners")
    return positions
