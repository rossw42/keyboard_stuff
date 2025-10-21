"""
Pattern generation for decorative cutouts in keyboard case.

Generates geometric patterns for bottom surface cutouts:
- Honeycomb (hexagonal)
- Grid (rectangular)
- Diamond (diagonal squares)
"""

from typing import List, Tuple
import math

Point2D = Tuple[float, float]


def generate_hexagon(center: Point2D, size: float) -> List[Point2D]:
    """
    Generate a hexagon centered at given point.
    
    Args:
        center: Center point (x, y)
        size: Distance from center to vertex
        
    Returns:
        List of 6 vertices forming hexagon
    """
    cx, cy = center
    points = []
    for i in range(6):
        angle = math.pi / 3 * i  # 60 degrees
        x = cx + size * math.cos(angle)
        y = cy + size * math.sin(angle)
        points.append((x, y))
    return points


def generate_honeycomb_pattern(
    length: float,
    width: float,
    hex_size: float = 8.0,
    margin: float = 15.0,
    exclusion_zones: List[Tuple[Point2D, float]] = None
) -> List[List[Point2D]]:
    """
    Generate honeycomb pattern of hexagons.
    
    Args:
        length: Pattern area length
        width: Pattern area width
        hex_size: Hexagon size (center to vertex)
        margin: Margin from edges
        exclusion_zones: List of (center, radius) tuples to exclude patterns around
        
    Returns:
        List of hexagons, each hexagon is a list of points
    """
    hexagons = []
    exclusion_zones = exclusion_zones or []
    
    # Hexagon spacing
    h_spacing = hex_size * math.sqrt(3)  # Horizontal spacing
    v_spacing = hex_size * 1.5  # Vertical spacing
    
    # Generate grid of hexagons
    y = margin
    row = 0
    while y < width - margin:
        x = margin
        # Offset every other row
        if row % 2 == 1:
            x += h_spacing / 2
        
        while x < length - margin:
            # Check if hexagon fits within bounds
            if (x - hex_size > margin and x + hex_size < length - margin and
                y - hex_size > margin and y + hex_size < width - margin):
                
                # Check if hexagon is too close to any exclusion zone
                too_close = False
                for (ex_x, ex_y), ex_radius in exclusion_zones:
                    dist = math.sqrt((x - ex_x)**2 + (y - ex_y)**2)
                    if dist < ex_radius + hex_size:
                        too_close = True
                        break
                
                if not too_close:
                    hexagons.append(generate_hexagon((x, y), hex_size))
            x += h_spacing
        
        y += v_spacing
        row += 1
    
    return hexagons


def generate_grid_pattern(
    length: float,
    width: float,
    cell_size: float = 10.0,
    spacing: float = 3.0,
    margin: float = 15.0,
    exclusion_zones: List[Tuple[Point2D, float]] = None
) -> List[List[Point2D]]:
    """
    Generate rectangular grid pattern.
    
    Args:
        length: Pattern area length
        width: Pattern area width
        cell_size: Size of each rectangular cell
        spacing: Gap between cells
        margin: Margin from edges
        exclusion_zones: List of (center, radius) tuples to exclude patterns around
        
    Returns:
        List of rectangles, each is a list of 4 corner points
    """
    rectangles = []
    exclusion_zones = exclusion_zones or []
    
    y = margin
    while y + cell_size < width - margin:
        x = margin
        while x + cell_size < length - margin:
            # Check center of rectangle against exclusion zones
            center_x = x + cell_size / 2
            center_y = y + cell_size / 2
            
            too_close = False
            for (ex_x, ex_y), ex_radius in exclusion_zones:
                dist = math.sqrt((center_x - ex_x)**2 + (center_y - ex_y)**2)
                if dist < ex_radius + cell_size:
                    too_close = True
                    break
            
            if not too_close:
                rect = [
                    (x, y),
                    (x + cell_size, y),
                    (x + cell_size, y + cell_size),
                    (x, y + cell_size),
                    (x, y)  # Close the rectangle
                ]
                rectangles.append(rect)
            x += cell_size + spacing
        y += cell_size + spacing
    
    return rectangles


def generate_diamond_pattern(
    length: float,
    width: float,
    diamond_size: float = 12.0,
    spacing: float = 3.0,
    margin: float = 15.0,
    exclusion_zones: List[Tuple[Point2D, float]] = None
) -> List[List[Point2D]]:
    """
    Generate diamond (45° rotated square) pattern.
    
    Args:
        length: Pattern area length
        width: Pattern area width
        diamond_size: Size of diamond (point to point)
        spacing: Gap between diamonds
        margin: Margin from edges
        exclusion_zones: List of (center, radius) tuples to exclude patterns around
        
    Returns:
        List of diamonds, each is a list of 4 corner points
    """
    diamonds = []
    exclusion_zones = exclusion_zones or []
    
    # Diamond spacing
    step = diamond_size + spacing
    
    y = margin + diamond_size / 2
    while y < width - margin - diamond_size / 2:
        x = margin + diamond_size / 2
        while x < length - margin - diamond_size / 2:
            # Check if diamond is too close to any exclusion zone
            too_close = False
            for (ex_x, ex_y), ex_radius in exclusion_zones:
                dist = math.sqrt((x - ex_x)**2 + (y - ex_y)**2)
                if dist < ex_radius + diamond_size:
                    too_close = True
                    break
            
            if not too_close:
                # Diamond is a square rotated 45°
                half = diamond_size / 2
                diamond = [
                    (x, y - half),  # Top
                    (x + half, y),  # Right
                    (x, y + half),  # Bottom
                    (x - half, y),  # Left
                    (x, y - half)   # Close
                ]
                diamonds.append(diamond)
            x += step
        y += step
    
    return diamonds
