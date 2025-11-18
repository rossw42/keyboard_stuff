"""Split keyboard to unified case conversion."""

import logging
from dataclasses import dataclass
from typing import List, Tuple, Optional

import cadquery as cq
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union

logger = logging.getLogger(__name__)


@dataclass
class SplitDetection:
    """Results of split keyboard detection."""
    is_split: bool  # True if split keyboard detected
    split_axis: str  # 'x' or 'y' (which axis is the split)
    split_position: float  # Position of split line
    left_outline: List[Tuple[float, float]]  # Left half outline
    right_outline: List[Tuple[float, float]]  # Right half outline
    left_wire: Optional[cq.Wire] = None  # Left half wire
    right_wire: Optional[cq.Wire] = None  # Right half wire


def detect_split_keyboard(
    outline: List[Tuple[float, float]],
    wire: Optional[cq.Wire] = None
) -> SplitDetection:
    """
    Detect if outline is a split keyboard and find split axis/position.
    
    A split keyboard typically has:
    - Two distinct regions separated by a gap or line
    - Symmetry across one axis (usually X for left/right split)
    - Gap between halves typically 5-20mm
    
    Args:
        outline: PCB outline points
        wire: Optional CadQuery wire for more precise analysis
        
    Returns:
        SplitDetection with split information
    """
    try:
        xs = [p[0] for p in outline]
        ys = [p[1] for p in outline]
        
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        
        width = x_max - x_min
        height = y_max - y_min
        
        logger.info(f"Analyzing outline for split keyboard:")
        logger.info(f"  Bounds: X({x_min:.2f}, {x_max:.2f}), Y({y_min:.2f}, {y_max:.2f})")
        logger.info(f"  Dimensions: {width:.2f}mm × {height:.2f}mm")
        
        # Check for X-axis split (left/right halves)
        # Look for a vertical gap in the middle
        x_split_result = _detect_x_split(outline, x_min, x_max, y_min, y_max)
        
        # Check for Y-axis split (top/bottom halves)
        # Look for a horizontal gap in the middle
        y_split_result = _detect_y_split(outline, x_min, x_max, y_min, y_max)
        
        # Determine which split is more likely
        if x_split_result and y_split_result:
            # Both detected - choose the one with larger gap
            x_gap = x_split_result[1]
            y_gap = y_split_result[1]
            
            if x_gap > y_gap:
                logger.info(f"Detected X-axis split (left/right) with gap: {x_gap:.2f}mm")
                return _create_x_split_detection(outline, wire, x_split_result[0])
            else:
                logger.info(f"Detected Y-axis split (top/bottom) with gap: {y_gap:.2f}mm")
                return _create_y_split_detection(outline, wire, y_split_result[0])
        
        elif x_split_result:
            logger.info(f"Detected X-axis split (left/right) with gap: {x_split_result[1]:.2f}mm")
            return _create_x_split_detection(outline, wire, x_split_result[0])
        
        elif y_split_result:
            logger.info(f"Detected Y-axis split (top/bottom) with gap: {y_split_result[1]:.2f}mm")
            return _create_y_split_detection(outline, wire, y_split_result[0])
        
        else:
            logger.info("No split detected - treating as single keyboard")
            return SplitDetection(
                is_split=False,
                split_axis="none",
                split_position=0,
                left_outline=outline,
                right_outline=[],
                left_wire=wire,
                right_wire=None
            )
    
    except Exception as e:
        logger.warning(f"Error detecting split: {e}, treating as single keyboard")
        return SplitDetection(
            is_split=False,
            split_axis="none",
            split_position=0,
            left_outline=outline,
            right_outline=[],
            left_wire=wire,
            right_wire=None
        )


def _detect_x_split(
    outline: List[Tuple[float, float]],
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float
) -> Optional[Tuple[float, float]]:
    """
    Detect vertical split (left/right halves).
    
    Returns:
        Tuple of (split_x_position, gap_size) or None if not detected
    """
    # Sample X positions and count how many outline points are near each X
    x_range = x_max - x_min
    num_samples = 100
    
    # Count points in vertical slices
    point_counts = []
    for i in range(num_samples):
        x_pos = x_min + (i / num_samples) * x_range
        # Count points within 1.5mm of this X position
        count = sum(1 for p in outline if abs(p[0] - x_pos) < 1.5)
        point_counts.append((x_pos, count))
    
    # Find the X position with minimum points (likely the gap)
    min_count_pos, min_count = min(point_counts, key=lambda x: x[1])
    
    # Check if this is a significant gap (less than 20% of average)
    avg_count = sum(c for _, c in point_counts) / len(point_counts)
    
    if min_count < avg_count * 0.2 and min_count < 3:
        # Found a gap - estimate gap size
        # Find the nearest points on either side
        left_points = [p for p in outline if p[0] < min_count_pos]
        right_points = [p for p in outline if p[0] > min_count_pos]
        
        if left_points and right_points:
            left_max_x = max(p[0] for p in left_points)
            right_min_x = min(p[0] for p in right_points)
            gap = right_min_x - left_max_x
            
            if gap > 1.5:  # Minimum gap of 1.5mm to be considered a split
                return (min_count_pos, gap)
    
    return None


def _detect_y_split(
    outline: List[Tuple[float, float]],
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float
) -> Optional[Tuple[float, float]]:
    """
    Detect horizontal split (top/bottom halves).
    
    Returns:
        Tuple of (split_y_position, gap_size) or None if not detected
    """
    # Sample Y positions and count how many outline points are near each Y
    y_range = y_max - y_min
    num_samples = 100
    
    # Count points in horizontal slices
    point_counts = []
    for i in range(num_samples):
        y_pos = y_min + (i / num_samples) * y_range
        # Count points within 1.5mm of this Y position
        count = sum(1 for p in outline if abs(p[1] - y_pos) < 1.5)
        point_counts.append((y_pos, count))
    
    # Find the Y position with minimum points (likely the gap)
    min_count_pos, min_count = min(point_counts, key=lambda x: x[1])
    
    # Check if this is a significant gap
    avg_count = sum(c for _, c in point_counts) / len(point_counts)
    
    if min_count < avg_count * 0.2 and min_count < 3:
        # Found a gap - estimate gap size
        top_points = [p for p in outline if p[1] < min_count_pos]
        bottom_points = [p for p in outline if p[1] > min_count_pos]
        
        if top_points and bottom_points:
            top_max_y = max(p[1] for p in top_points)
            bottom_min_y = min(p[1] for p in bottom_points)
            gap = bottom_min_y - top_max_y
            
            if gap > 1.5:
                return (min_count_pos, gap)
    
    return None


def _create_x_split_detection(
    outline: List[Tuple[float, float]],
    wire: Optional[cq.Wire],
    split_x: float
) -> SplitDetection:
    """Create SplitDetection for X-axis split."""
    # Separate outline into left and right
    left_outline = [p for p in outline if p[0] <= split_x]
    right_outline = [p for p in outline if p[0] >= split_x]
    
    # Add split line points to close the outlines
    y_values = [p[1] for p in outline]
    y_min, y_max = min(y_values), max(y_values)
    
    left_outline.extend([(split_x, y_max), (split_x, y_min)])
    right_outline.extend([(split_x, y_min), (split_x, y_max)])
    
    return SplitDetection(
        is_split=True,
        split_axis="x",
        split_position=split_x,
        left_outline=left_outline,
        right_outline=right_outline,
        left_wire=wire,
        right_wire=None
    )


def _create_y_split_detection(
    outline: List[Tuple[float, float]],
    wire: Optional[cq.Wire],
    split_y: float
) -> SplitDetection:
    """Create SplitDetection for Y-axis split."""
    # Separate outline into top and bottom
    top_outline = [p for p in outline if p[1] <= split_y]
    bottom_outline = [p for p in outline if p[1] >= split_y]
    
    # Add split line points to close the outlines
    x_values = [p[0] for p in outline]
    x_min, x_max = min(x_values), max(x_values)
    
    top_outline.extend([(x_max, split_y), (x_min, split_y)])
    bottom_outline.extend([(x_min, split_y), (x_max, split_y)])
    
    return SplitDetection(
        is_split=True,
        split_axis="y",
        split_position=split_y,
        left_outline=top_outline,
        right_outline=bottom_outline,
        left_wire=wire,
        right_wire=None
    )


def create_unified_outline(
    left_outline: List[Tuple[float, float]],
    right_outline: List[Tuple[float, float]],
    split_axis: str,
    split_position: float,
    gap_fill: float = 0.0
) -> List[Tuple[float, float]]:
    """
    Create unified outline by mirroring one half and merging.
    
    Args:
        left_outline: Left/top half outline
        right_outline: Right/bottom half outline
        split_axis: 'x' or 'y'
        split_position: Position of split line
        gap_fill: Distance to fill the gap (0 = no fill, positive = fill gap)
        
    Returns:
        Unified outline as list of points
    """
    try:
        # Mirror the right half to match the left
        if split_axis == "x":
            # Mirror across X axis
            mirrored_right = [
                (2 * split_position - p[0], p[1])
                for p in right_outline
            ]
        else:
            # Mirror across Y axis
            mirrored_right = [
                (p[0], 2 * split_position - p[1])
                for p in right_outline
            ]
        
        # Try to merge outlines using shapely with error handling
        try:
            left_poly = Polygon(left_outline)
            right_poly = Polygon(mirrored_right)
            
            # Validate polygons
            if not left_poly.is_valid:
                logger.debug("Left polygon invalid, attempting to fix")
                left_poly = left_poly.buffer(0)
            if not right_poly.is_valid:
                logger.debug("Right polygon invalid, attempting to fix")
                right_poly = right_poly.buffer(0)
            
            # Union the two polygons
            unified_poly = unary_union([left_poly, right_poly])
            
        except Exception as e:
            logger.debug(f"Shapely union failed: {e}, using convex hull approach")
            # Fallback: combine all points and create convex hull
            all_points = left_outline + mirrored_right
            unified_poly = Polygon(all_points).convex_hull
        
        # Extract coordinates
        if unified_poly.is_empty:
            logger.warning("Union resulted in empty polygon, using left outline")
            return left_outline
        
        if unified_poly.geom_type == 'MultiPolygon':
            # Take the largest polygon
            unified_poly = max(unified_poly.geoms, key=lambda p: p.area)
        
        if unified_poly.geom_type == 'LineString':
            logger.warning("Union resulted in LineString, using left outline")
            return left_outline
        
        coords = list(unified_poly.exterior.coords[:-1])
        logger.info(f"Created unified outline with {len(coords)} points")
        
        return coords
    
    except Exception as e:
        logger.warning(f"Failed to create unified outline: {e}, using left outline")
        return left_outline


def mirror_outline_x(
    outline: List[Tuple[float, float]],
    mirror_x: float
) -> List[Tuple[float, float]]:
    """
    Mirror outline across vertical line at X position.
    
    Args:
        outline: Original outline
        mirror_x: X coordinate of mirror line
        
    Returns:
        Mirrored outline
    """
    return [(2 * mirror_x - p[0], p[1]) for p in outline]


def mirror_outline_y(
    outline: List[Tuple[float, float]],
    mirror_y: float
) -> List[Tuple[float, float]]:
    """
    Mirror outline across horizontal line at Y position.
    
    Args:
        outline: Original outline
        mirror_y: Y coordinate of mirror line
        
    Returns:
        Mirrored outline
    """
    return [(p[0], 2 * mirror_y - p[1]) for p in outline]
