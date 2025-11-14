"""PCB analysis module for extracting geometry from STEP files."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional

import cadquery as cq

logger = logging.getLogger(__name__)


@dataclass
class PCBInfo:
    """Information extracted from PCB STEP file."""
    outline: List[Tuple[float, float]]  # 2D outline points (for compatibility)
    bounding_box: Tuple[float, float, float, float]  # xmin, ymin, xmax, ymax
    mounting_holes: List[Tuple[float, float]]  # (x, y) positions
    thickness: float  # PCB thickness in mm
    wire: any = None  # CadQuery wire object for smooth offsetting


class PCBImportError(Exception):
    """Error importing or analyzing PCB."""
    pass


def import_pcb_step(step_file: Path) -> cq.Workplane:
    """
    Import STEP file and return CadQuery workplane.
    
    Args:
        step_file: Path to STEP file
        
    Returns:
        CadQuery workplane with imported geometry
        
    Raises:
        PCBImportError: If file cannot be imported
    """
    try:
        logger.info(f"Importing PCB STEP file: {step_file}")
        pcb = cq.importers.importStep(str(step_file))
        
        if pcb is None or not pcb.val():
            raise PCBImportError(f"Failed to import STEP file: {step_file}")
        
        # Get bounding box to verify we have geometry
        shape = pcb.val()
        bb = shape.BoundingBox()
        logger.info(f"  PCB bounds: X({bb.xmin:.2f}, {bb.xmax:.2f}), "
                   f"Y({bb.ymin:.2f}, {bb.ymax:.2f}), "
                   f"Z({bb.zmin:.2f}, {bb.zmax:.2f})")
        
        return pcb
        
    except Exception as e:
        raise PCBImportError(
            f"Failed to import STEP file '{step_file}': {e}\n"
            f"  Make sure the file is a valid STEP file exported from KiCad.\n"
            f"  In KiCad: File → Export → STEP"
        ) from e


def extract_pcb_outline(pcb: cq.Workplane, tolerance: float = 0.1):
    """
    Extract 2D outline from PCB geometry.
    
    Args:
        pcb: CadQuery workplane with PCB geometry
        tolerance: Tolerance for curve approximation (mm)
        
    Returns:
        Tuple of (points, wire) where:
        - points: List of (x, y) points defining the outline
        - wire: CadQuery wire object for smooth offsetting
        
    Raises:
        PCBImportError: If outline cannot be extracted
    """
    try:
        logger.info("Extracting PCB outline...")
        
        # Get the PCB shape
        pcb_shape = pcb.val()
        
        # Get all faces and find the largest one (top or bottom)
        wp = cq.Workplane("XY").add(pcb_shape)
        faces = wp.faces().vals()
        
        if not faces:
            raise PCBImportError("No faces found in PCB geometry")
        
        # Find largest face by area
        largest_face = max(faces, key=lambda f: f.Area())
        logger.info(f"  Found PCB face with area: {largest_face.Area():.2f} mm²")
        
        # Get the outer wire of this face - THIS IS THE KEY!
        outer_wire = largest_face.outerWire()
        
        # Convert wire to list of points (for compatibility with existing code)
        # Use edges to get points with appropriate density
        points = []
        for edge in outer_wire.Edges():
            # Get points along the edge
            # For curves, use multiple points; for lines, just endpoints
            if edge.geomType() == "LINE":
                # Just add the start point (end will be start of next edge)
                points.append((edge.startPoint().x, edge.startPoint().y))
            else:
                # For curves, sample points
                num_samples = max(3, int(edge.Length() / tolerance))
                for i in range(num_samples):
                    t = i / num_samples
                    pt = edge.positionAt(t)
                    points.append((pt.x, pt.y))
        
        if len(points) < 3:
            raise PCBImportError(f"Outline has too few points: {len(points)}")
        
        logger.info(f"  Extracted outline with {len(points)} points")
        return points, outer_wire  # Return BOTH points and wire
        
    except PCBImportError:
        raise
    except Exception as e:
        raise PCBImportError(f"Failed to extract PCB outline: {e}") from e


def detect_mounting_holes(
    pcb: cq.Workplane,
    min_diameter: float = 3.0,
    max_diameter: float = 4.0
) -> List[Tuple[float, float]]:
    """
    Detect circular mounting holes in PCB.
    
    Only detects larger holes (3.0-4.0mm) for actual mounting screws.
    
    Args:
        pcb: CadQuery workplane with PCB geometry
        min_diameter: Minimum hole diameter to detect (mm) - default 3.0mm for M3 holes
        max_diameter: Maximum hole diameter to detect (mm) - default 4.0mm
        
    Returns:
        List of (x, y) positions of detected holes (limited to ~4-6 for corners/edges)
    """
    try:
        logger.info("Detecting mounting holes...")
        
        pcb_shape = pcb.val()
        all_holes = []
        
        # Look for circular edges that could be holes
        # Get all edges from all faces
        wp = cq.Workplane("XY").add(pcb_shape)
        
        # Try to find holes by looking for circular edges
        for face in wp.faces().vals():
            for wire in face.Wires():
                for edge in wire.Edges():
                    if edge.geomType() == "CIRCLE":
                        # Check if diameter is in range
                        radius = edge.radius()
                        diameter = radius * 2
                        
                        if min_diameter <= diameter <= max_diameter:
                            center = edge.Center()
                            # Check if we already have this hole (avoid duplicates)
                            pos = (center.x, center.y)
                            if not any(abs(h[0][0] - pos[0]) < 0.1 and abs(h[0][1] - pos[1]) < 0.1 
                                     for h in all_holes):
                                all_holes.append((pos, diameter))
        
        # If we have too many holes, keep only the largest ones (actual mounting holes)
        if len(all_holes) > 8:
            # Sort by diameter (largest first) and take top 6
            all_holes.sort(key=lambda x: x[1], reverse=True)
            all_holes = all_holes[:6]
            logger.info(f"  Found {len(all_holes)} holes, keeping 6 largest for mounting")
        
        # Extract just positions
        holes = [pos for pos, diam in all_holes]
        
        for pos, diam in all_holes:
            logger.info(f"  Mounting hole at ({pos[0]:.2f}, {pos[1]:.2f}), diameter: {diam:.2f}mm")
        
        logger.info(f"  Using {len(holes)} mounting holes")
        return holes
        
    except Exception as e:
        logger.warning(f"Failed to detect mounting holes: {e}")
        return []


def analyze_pcb(step_file: Path) -> PCBInfo:
    """
    Complete PCB analysis pipeline.
    
    Args:
        step_file: Path to PCB STEP file
        
    Returns:
        PCBInfo with extracted geometry including wire object
        
    Raises:
        PCBImportError: If analysis fails
    """
    # Import PCB
    pcb = import_pcb_step(step_file)
    
    # Extract outline AND wire
    outline, wire = extract_pcb_outline(pcb)
    
    # Calculate bounding box
    xs = [p[0] for p in outline]
    ys = [p[1] for p in outline]
    bounding_box = (min(xs), min(ys), max(xs), max(ys))
    
    # Detect mounting holes
    mounting_holes = detect_mounting_holes(pcb)
    
    # Get PCB thickness
    shape = pcb.val()
    bb = shape.BoundingBox()
    thickness = bb.zmax - bb.zmin
    
    logger.info(f"PCB analysis complete:")
    logger.info(f"  Outline: {len(outline)} points")
    logger.info(f"  Bounding box: {bounding_box}")
    logger.info(f"  Mounting holes: {len(mounting_holes)}")
    logger.info(f"  Thickness: {thickness:.2f}mm")
    
    return PCBInfo(
        outline=outline,
        bounding_box=bounding_box,
        mounting_holes=mounting_holes,
        thickness=thickness,
        wire=wire  # Include the wire object!
    )
