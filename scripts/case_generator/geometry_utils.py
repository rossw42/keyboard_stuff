"""Shared geometric operations and utilities."""

import logging
import math
from typing import List, Tuple

import cadquery as cq
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

logger = logging.getLogger(__name__)


def offset_outline(
    outline: List[Tuple[float, float]],
    distance: float
) -> List[Tuple[float, float]]:
    """
    Offset a 2D outline by distance (positive = outward, negative = inward).
    
    Args:
        outline: List of (x, y) points
        distance: Offset distance in mm
        
    Returns:
        Offset outline as list of (x, y) points
    """
    try:
        # Use shapely for robust offsetting
        poly = Polygon(outline)
        # join_style=1 is round (no spikes), join_style=2 is mitered (can create spikes)
        # Higher resolution = smoother curves
        offset_poly = poly.buffer(distance, join_style=1, resolution=32)
        
        # Extract coordinates
        if offset_poly.is_empty:
            logger.warning(f"Offset resulted in empty polygon (distance={distance})")
            return outline
        
        # Handle MultiPolygon result (take largest polygon)
        if offset_poly.geom_type == 'MultiPolygon':
            logger.debug(f"Offset resulted in MultiPolygon, taking largest")
            # Get the largest polygon by area
            offset_poly = max(offset_poly.geoms, key=lambda p: p.area)
        
        # Get exterior coordinates
        coords = list(offset_poly.exterior.coords[:-1])  # Remove duplicate last point
        return coords
        
    except Exception as e:
        logger.warning(f"Failed to offset outline: {e}, returning original")
        return outline


def simplify_outline(
    outline: List[Tuple[float, float]],
    tolerance: float = 0.1
) -> List[Tuple[float, float]]:
    """
    Simplify outline by removing redundant points.
    
    Args:
        outline: List of (x, y) points
        tolerance: Simplification tolerance in mm
        
    Returns:
        Simplified outline
    """
    try:
        poly = Polygon(outline)
        simplified = poly.simplify(tolerance, preserve_topology=True)
        coords = list(simplified.exterior.coords[:-1])
        
        # If still too many points, simplify more aggressively
        if len(coords) > 500:
            simplified = poly.simplify(tolerance * 2, preserve_topology=True)
            coords = list(simplified.exterior.coords[:-1])
        
        logger.debug(f"Simplified outline from {len(outline)} to {len(coords)} points")
        return coords
        
    except Exception as e:
        logger.warning(f"Failed to simplify outline: {e}, returning original")
        return outline


def calculate_bounding_box(
    outline: List[Tuple[float, float]]
) -> Tuple[float, float, float, float]:
    """
    Calculate bounding box of outline.
    
    Args:
        outline: List of (x, y) points
        
    Returns:
        Tuple of (xmin, ymin, xmax, ymax)
    """
    xs = [p[0] for p in outline]
    ys = [p[1] for p in outline]
    return (min(xs), min(ys), max(xs), max(ys))


def point_in_polygon(
    point: Tuple[float, float],
    polygon: List[Tuple[float, float]]
) -> bool:
    """
    Test if point is inside polygon.
    
    Args:
        point: (x, y) point to test
        polygon: List of (x, y) points defining polygon
        
    Returns:
        True if point is inside polygon
    """
    try:
        pt = Point(point)
        poly = Polygon(polygon)
        return poly.contains(pt)
    except:
        return False


def distance_point_to_point(
    p1: Tuple[float, float],
    p2: Tuple[float, float]
) -> float:
    """Calculate distance between two points."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def mirror_geometry_x(
    part: cq.Workplane,
    mirror_plane_x: float = 0.0
) -> cq.Workplane:
    """
    Mirror geometry across X plane.
    
    Args:
        part: CadQuery workplane to mirror
        mirror_plane_x: X coordinate of mirror plane
        
    Returns:
        Mirrored workplane
    """
    # CadQuery doesn't have a direct mirror, so we use a transformation
    # Mirror across YZ plane at x=mirror_plane_x
    # This is equivalent to: translate to origin, scale X by -1, translate back
    
    # Get the shape
    shape = part.val()
    
    # Create mirror transformation matrix
    # For mirroring across X plane at x=mirror_plane_x:
    # 1. Translate so mirror plane is at origin
    # 2. Scale X by -1
    # 3. Translate back
    
    from cadquery import Vector, Matrix
    
    # Translate to origin
    t1 = Matrix()
    t1.translate(Vector(-mirror_plane_x, 0, 0))
    
    # Scale X by -1 (mirror)
    scale = Matrix()
    scale.scale(-1, 1, 1)
    
    # Translate back
    t2 = Matrix()
    t2.translate(Vector(mirror_plane_x, 0, 0))
    
    # Combine transformations
    transform = t2.multiply(scale.multiply(t1))
    
    # Apply transformation
    mirrored_shape = shape.transformShape(transform)
    
    return cq.Workplane("XY").add(mirrored_shape)


def rotate_point_2d(
    point: Tuple[float, float],
    angle_deg: float,
    center: Tuple[float, float] = (0, 0)
) -> Tuple[float, float]:
    """
    Rotate a 2D point around a center.
    
    Args:
        point: (x, y) point to rotate
        angle_deg: Rotation angle in degrees
        center: (x, y) center of rotation
        
    Returns:
        Rotated (x, y) point
    """
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Translate to origin
    x = point[0] - center[0]
    y = point[1] - center[1]
    
    # Rotate
    x_new = x * cos_a - y * sin_a
    y_new = x * sin_a + y * cos_a
    
    # Translate back
    return (x_new + center[0], y_new + center[1])


def create_rounded_rectangle_outline(
    width: float,
    height: float,
    corner_radius: float,
    center: Tuple[float, float] = (0, 0)
) -> List[Tuple[float, float]]:
    """
    Create outline of a rounded rectangle.
    
    Args:
        width: Rectangle width
        height: Rectangle height
        corner_radius: Corner radius
        center: Center point
        
    Returns:
        List of (x, y) points
    """
    cx, cy = center
    w2 = width / 2
    h2 = height / 2
    r = corner_radius
    
    points = []
    
    # Number of points per arc
    n = 16
    
    # Top right arc
    for i in range(n + 1):
        angle = math.radians(i * 90 / n)
        x = cx + w2 - r + r * math.cos(angle)
        y = cy + h2 - r + r * math.sin(angle)
        points.append((x, y))
    
    # Top left arc
    for i in range(n + 1):
        angle = math.radians(90 + i * 90 / n)
        x = cx - w2 + r + r * math.cos(angle)
        y = cy + h2 - r + r * math.sin(angle)
        points.append((x, y))
    
    # Bottom left arc
    for i in range(n + 1):
        angle = math.radians(180 + i * 90 / n)
        x = cx - w2 + r + r * math.cos(angle)
        y = cy - h2 + r + r * math.sin(angle)
        points.append((x, y))
    
    # Bottom right arc
    for i in range(n + 1):
        angle = math.radians(270 + i * 90 / n)
        x = cx + w2 - r + r * math.cos(angle)
        y = cy - h2 + r + r * math.sin(angle)
        points.append((x, y))
    
    return points
