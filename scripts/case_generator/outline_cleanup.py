"""Outline cleanup for aesthetic improvements."""

import logging
from typing import List, Tuple

from shapely.geometry import Polygon
from shapely.ops import unary_union

logger = logging.getLogger(__name__)


def smooth_outline(
    outline: List[Tuple[float, float]],
    buffer_distance: float = 0.5,
    simplify_tolerance: float = 0.5
) -> List[Tuple[float, float]]:
    """
    Smooth outline by buffering out and back in to fill small notches.
    
    This removes small cutouts and creates a cleaner aesthetic outline.
    
    Args:
        outline: Original outline points
        buffer_distance: Distance to buffer (larger = more aggressive smoothing)
        simplify_tolerance: Tolerance for simplification
        
    Returns:
        Smoothed outline points
    """
    try:
        poly = Polygon(outline)
        
        # Buffer outward then inward to fill small notches
        smoothed = poly.buffer(buffer_distance, join_style=1, resolution=32)
        smoothed = smoothed.buffer(-buffer_distance, join_style=1, resolution=32)
        
        # Simplify to reduce point count
        if simplify_tolerance > 0:
            smoothed = smoothed.simplify(simplify_tolerance, preserve_topology=True)
        
        if smoothed.is_empty:
            logger.warning("Smoothing resulted in empty polygon, returning original")
            return outline
        
        # Handle MultiPolygon
        if smoothed.geom_type == 'MultiPolygon':
            smoothed = max(smoothed.geoms, key=lambda p: p.area)
        
        coords = list(smoothed.exterior.coords[:-1])
        logger.info(f"  Smoothed outline: {len(outline)} → {len(coords)} points")
        
        return coords
        
    except Exception as e:
        logger.warning(f"Outline smoothing failed: {e}, returning original")
        return outline


def fill_small_notches(
    outline: List[Tuple[float, float]],
    max_notch_depth: float = 5.0
) -> List[Tuple[float, float]]:
    """
    Fill small notches in the outline for cleaner aesthetics.
    
    Uses a buffer operation to fill indentations smaller than max_notch_depth.
    
    Args:
        outline: Original outline points
        max_notch_depth: Maximum depth of notches to fill (mm)
        
    Returns:
        Cleaned outline points
    """
    try:
        poly = Polygon(outline)
        
        # Buffer outward by max_notch_depth to fill notches
        filled = poly.buffer(max_notch_depth, join_style=1, resolution=32)
        
        # Buffer back inward to restore original size
        filled = filled.buffer(-max_notch_depth, join_style=1, resolution=32)
        
        if filled.is_empty:
            logger.warning("Notch filling resulted in empty polygon, returning original")
            return outline
        
        # Handle MultiPolygon
        if filled.geom_type == 'MultiPolygon':
            filled = max(filled.geoms, key=lambda p: p.area)
        
        coords = list(filled.exterior.coords[:-1])
        logger.info(f"  Filled small notches: {len(outline)} → {len(coords)} points")
        
        return coords
        
    except Exception as e:
        logger.warning(f"Notch filling failed: {e}, returning original")
        return outline


def clean_outline_for_case(
    outline: List[Tuple[float, float]],
    fill_notches: bool = True,
    smooth: bool = True,
    notch_depth: float = 3.0,
    smooth_distance: float = 0.5
) -> List[Tuple[float, float]]:
    """
    Clean up PCB outline for aesthetic case generation.
    
    This removes small notches (for connectors, etc.) and smooths the outline
    to create a cleaner, more aesthetic case design.
    
    Args:
        outline: Original PCB outline points
        fill_notches: Whether to fill small notches
        smooth: Whether to smooth the outline
        notch_depth: Maximum depth of notches to fill (mm)
        smooth_distance: Distance for smoothing buffer
        
    Returns:
        Cleaned outline points
    """
    logger.info("Cleaning outline for aesthetics...")
    
    cleaned = outline
    
    if fill_notches:
        cleaned = fill_small_notches(cleaned, notch_depth)
    
    if smooth:
        cleaned = smooth_outline(cleaned, smooth_distance, simplify_tolerance=0.3)
    
    logger.info(f"  Final outline: {len(cleaned)} points")
    
    return cleaned
