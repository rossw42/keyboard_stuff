"""Bottom tray case generation."""

import logging
from typing import List, Tuple

import cadquery as cq

from .config import CaseConfig
from .pcb_analyzer import PCBInfo
from .geometry_utils import offset_outline

logger = logging.getLogger(__name__)


def create_case_walls(
    outline: List[Tuple[float, float]],
    offset: float,
    wall_thickness: float,
    height: float,
    corner_radius: float,
    wire=None
) -> cq.Workplane:
    """
    Create case walls following PCB outline.
    
    Args:
        outline: PCB outline points
        offset: Distance to offset from PCB
        wall_thickness: Wall thickness
        height: Wall height
        corner_radius: Corner radius for external profile
        
    Returns:
        CadQuery workplane with walls
    """
    logger.info("Creating case walls...")
    
    # Use the wire object directly if available (smooth!)
    if wire is not None:
        try:
            # Use CadQuery's native offset2D on the original wire
            outer_offset_wires = wire.offset2D(offset)
            inner_offset_wires = wire.offset2D(offset - wall_thickness)
            
            if not outer_offset_wires or not inner_offset_wires:
                raise Exception("Wire offset returned empty")
            
            # Create outer shell
            outer_shell = (cq.Workplane("XY")
                          .add(outer_offset_wires[0])
                          .toPending()
                          .extrude(height))
            
            # Create inner cavity
            inner_cavity = (cq.Workplane("XY")
                           .add(inner_offset_wires[0])
                           .toPending()
                           .extrude(height))
            
            # Subtract inner from outer to create walls
            walls = outer_shell.cut(inner_cavity)
            logger.info("  ✓ Created smooth walls using wire offset")
            return walls
            
        except Exception as e:
            logger.warning(f"Wire offset failed: {e}, falling back to point-based method")
    
    # Fallback: use point-based method
    from .geometry_utils import simplify_outline, offset_outline
    simplified = simplify_outline(outline, tolerance=0.2)
    outer_outline = offset_outline(simplified, offset)
    inner_outline = offset_outline(simplified, offset - wall_thickness)
    
    outer_solid = cq.Workplane("XY").polyline(outer_outline).close().extrude(height)
    inner_solid = cq.Workplane("XY").polyline(inner_outline).close().extrude(height)
    walls = outer_solid.cut(inner_solid)
    
    return walls


def create_floor(
    outline: List[Tuple[float, float]],
    offset: float,
    thickness: float,
    wire=None
) -> cq.Workplane:
    """
    Create case floor.
    
    Args:
        outline: PCB outline points
        offset: Distance to offset from PCB
        thickness: Floor thickness
        
    Returns:
        CadQuery workplane with floor
    """
    logger.info("Creating case floor...")
    logger.info(f"  Wire object: {type(wire) if wire is not None else 'None'}")
    
    # Use the wire object directly if available (smooth!)
    if wire is not None:
        try:
            offset_wires = wire.offset2D(offset)
            
            if not offset_wires:
                raise Exception("Wire offset returned empty")
            
            # Create floor
            floor = (cq.Workplane("XY")
                    .add(offset_wires[0])
                    .toPending()
                    .extrude(thickness))
            logger.info("  ✓ Created smooth floor using wire offset")
            return floor
            
        except Exception as e:
            logger.warning(f"Wire offset failed: {e}, falling back to point-based method")
    
    # Fallback: use point-based method
    from .geometry_utils import simplify_outline, offset_outline
    simplified = simplify_outline(outline, tolerance=0.2)
    floor_outline = offset_outline(simplified, offset)
    floor = cq.Workplane("XY").polyline(floor_outline).close().extrude(thickness)
    
    return floor


def create_mounting_posts(
    positions: List[Tuple[float, float]],
    boss_diameter: float,
    boss_height: float,
    hole_diameter: float,
    floor_thickness: float
) -> cq.Workplane:
    """
    Create screw boss mounting posts.
    
    Args:
        positions: List of (x, y) positions for bosses
        boss_diameter: Boss outer diameter
        boss_height: Boss height (from top of floor to top of post)
        hole_diameter: Through-hole diameter
        floor_thickness: Thickness of floor (posts start here)
        
    Returns:
        CadQuery workplane with mounting posts
    """
    logger.info(f"Creating {len(positions)} mounting posts...")
    
    if not positions:
        return cq.Workplane("XY")
    
    # Create first boss
    result = cq.Workplane("XY").workplane(offset=floor_thickness)
    
    for x, y in positions:
        # Create boss cylinder starting at top of floor
        boss = (cq.Workplane("XY")
                .workplane(offset=floor_thickness)
                .center(x, y)
                .circle(boss_diameter / 2)
                .extrude(boss_height))
        
        # Create through-hole (only through the post, not the floor)
        hole = (cq.Workplane("XY")
                .workplane(offset=floor_thickness)
                .center(x, y)
                .circle(hole_diameter / 2)
                .extrude(boss_height + 0.1))
        
        # Subtract hole from boss
        boss = boss.cut(hole)
        
        # Add to result
        if result.val() is None:
            result = boss
        else:
            result = result.union(boss)
    
    return result


def filter_mounting_holes_away_from_switches(
    mounting_holes: List[Tuple[float, float]],
    switch_positions: List[Tuple[float, float]],
    min_distance: float = 10.0
) -> List[Tuple[float, float]]:
    """
    Filter out mounting holes that are too close to switches.
    
    Args:
        mounting_holes: List of mounting hole positions
        switch_positions: List of switch positions
        min_distance: Minimum distance between mounting hole and switch (mm)
        
    Returns:
        Filtered list of mounting hole positions
    """
    if not switch_positions:
        return mounting_holes
    
    filtered = []
    for hole_x, hole_y in mounting_holes:
        # Check distance to all switches
        too_close = False
        for switch_x, switch_y in switch_positions:
            distance = ((hole_x - switch_x)**2 + (hole_y - switch_y)**2)**0.5
            if distance < min_distance:
                logger.info(f"  Skipping mounting hole at ({hole_x:.2f}, {hole_y:.2f}) - "
                          f"too close to switch at ({switch_x:.2f}, {switch_y:.2f}), "
                          f"distance: {distance:.2f}mm")
                too_close = True
                break
        
        if not too_close:
            filtered.append((hole_x, hole_y))
    
    return filtered


def find_safe_post_positions(
    outline: List[Tuple[float, float]],
    switch_positions: List[Tuple[float, float]],
    num_posts: int = 4,
    min_switch_distance: float = 10.0,
    inset_from_edge: float = 5.0
) -> List[Tuple[float, float]]:
    """
    Find safe positions for mounting posts inside the PCB outline.
    
    Args:
        outline: PCB outline points
        switch_positions: List of switch positions to avoid
        num_posts: Number of posts to create
        min_switch_distance: Minimum distance from switches
        inset_from_edge: Minimum distance from PCB edge
        
    Returns:
        List of safe post positions
    """
    from shapely.geometry import Point, Polygon
    from shapely.ops import unary_union
    
    # Create polygon from outline
    outline_polygon = Polygon(outline)
    
    # Create buffer inward from edge
    inset_polygon = outline_polygon.buffer(-inset_from_edge)
    
    if inset_polygon.is_empty:
        logger.warning("Inset polygon is empty, using smaller inset")
        inset_polygon = outline_polygon.buffer(-2.0)
    
    # Create exclusion zones around switches
    exclusion_zones = []
    for sx, sy in switch_positions:
        exclusion_zones.append(Point(sx, sy).buffer(min_switch_distance))
    
    # Combine all exclusion zones
    if exclusion_zones:
        combined_exclusions = unary_union(exclusion_zones)
        # Find valid area (inside PCB but outside exclusion zones)
        valid_area = inset_polygon.difference(combined_exclusions)
    else:
        valid_area = inset_polygon
    
    if valid_area.is_empty:
        logger.warning("No valid area for posts after exclusions")
        return []
    
    # Get bounds of valid area
    bounds = valid_area.bounds  # (minx, miny, maxx, maxy)
    
    # Try to place posts in corners and edges of the valid area
    # Sample many points and find ones that are in valid area
    posts = []
    
    # Try corners first
    corner_candidates = [
        (bounds[0] + 2, bounds[1] + 2),  # Bottom-left
        (bounds[2] - 2, bounds[1] + 2),  # Bottom-right
        (bounds[0] + 2, bounds[3] - 2),  # Top-left
        (bounds[2] - 2, bounds[3] - 2),  # Top-right
    ]
    
    for x, y in corner_candidates:
        point = Point(x, y)
        if valid_area.contains(point):
            posts.append((x, y))
            logger.info(f"  Found safe post position at ({x:.2f}, {y:.2f})")
    
    # If we didn't find enough corners, try edges
    if len(posts) < 3:
        mid_x = (bounds[0] + bounds[2]) / 2
        mid_y = (bounds[1] + bounds[3]) / 2
        
        edge_candidates = [
            (mid_x, bounds[1] + 2),  # Bottom-center
            (mid_x, bounds[3] - 2),  # Top-center
            (bounds[0] + 2, mid_y),  # Left-center
            (bounds[2] - 2, mid_y),  # Right-center
        ]
        
        for x, y in edge_candidates:
            if len(posts) >= num_posts:
                break
            point = Point(x, y)
            if valid_area.contains(point):
                posts.append((x, y))
                logger.info(f"  Found safe post position at ({x:.2f}, {y:.2f})")
    
    # If still not enough, add centroid
    if len(posts) < 2:
        logger.warning(f"Only found {len(posts)} safe post positions, adding centroid")
        if hasattr(valid_area, 'centroid'):
            cx, cy = valid_area.centroid.x, valid_area.centroid.y
            posts.append((cx, cy))
            logger.info(f"  Added centroid post at ({cx:.2f}, {cy:.2f})")
    
    return posts


def create_bottom_tray(
    pcb_info: PCBInfo,
    config: CaseConfig,
    switch_layout=None
) -> cq.Workplane:
    """
    Generate complete bottom tray geometry.
    
    Args:
        pcb_info: PCB information
        config: Case configuration
        switch_layout: Optional switch layout to avoid collisions
        
    Returns:
        CadQuery workplane with complete bottom tray
    """
    logger.info("Generating bottom tray...")
    
    # Create floor (pass wire for smooth offsetting)
    floor = create_floor(
        pcb_info.outline,
        config.case_offset,
        config.bottom_thickness,
        wire=pcb_info.wire
    )
    
    # Create walls on top of floor (pass wire for smooth offsetting)
    walls = create_case_walls(
        pcb_info.outline,
        config.case_offset,
        config.wall_thickness,
        config.case_height - config.bottom_thickness,
        config.corner_radius,
        wire=pcb_info.wire
    )
    
    # Move walls to sit on top of floor
    walls = walls.translate((0, 0, config.bottom_thickness))
    
    # Combine floor and walls
    tray = floor.union(walls)
    
    # Add mounting posts if we have mounting holes
    if pcb_info.mounting_holes:
        # Filter out mounting holes that collide with switches
        mounting_holes = pcb_info.mounting_holes
        if switch_layout and switch_layout.switches:
            switch_positions = [(s.position[0], s.position[1]) for s in switch_layout.switches]
            mounting_holes = filter_mounting_holes_away_from_switches(
                mounting_holes,
                switch_positions,
                min_distance=10.0  # 10mm minimum clearance
            )
            logger.info(f"Using {len(mounting_holes)} of {len(pcb_info.mounting_holes)} mounting holes "
                       f"(filtered {len(pcb_info.mounting_holes) - len(mounting_holes)} due to switch collisions)")
        
        # If all holes were filtered, find safe positions for posts
        if not mounting_holes:
            logger.warning("All mounting holes filtered out due to switch collisions")
            logger.info("Finding safe positions for mounting posts...")
            
            switch_positions = [(s.position[0], s.position[1]) for s in switch_layout.switches]
            mounting_holes = find_safe_post_positions(
                pcb_info.outline,
                switch_positions,
                num_posts=4,
                min_switch_distance=3.0,  # Center-to-center distance (boss radius + switch radius)
                inset_from_edge=3.0
            )
            
            if not mounting_holes:
                logger.warning("Could not find any safe post positions!")
            else:
                logger.info(f"Found {len(mounting_holes)} safe post positions")
        
        if mounting_holes:
            # Calculate boss height (from top of floor to PCB mounting surface)
            boss_height = config.pcb_clearance
            
            posts = create_mounting_posts(
                mounting_holes,
                config.boss_diameter,
                boss_height,
                config.boss_hole_diameter,
                config.bottom_thickness
            )
            
            tray = tray.union(posts)
    else:
        logger.warning("No mounting holes detected, finding safe positions for posts...")
        
        # Find safe positions inside the PCB outline
        switch_positions = []
        if switch_layout and switch_layout.switches:
            switch_positions = [(s.position[0], s.position[1]) for s in switch_layout.switches]
        
        mounting_holes = find_safe_post_positions(
            pcb_info.outline,
            switch_positions,
            num_posts=4,
            min_switch_distance=3.0,  # Center-to-center distance (boss radius + switch radius)
            inset_from_edge=3.0
        )
        
        if mounting_holes:
            boss_height = config.pcb_clearance
            posts = create_mounting_posts(
                mounting_holes,
                config.boss_diameter,
                boss_height,
                config.boss_hole_diameter,
                config.bottom_thickness
            )
            
            tray = tray.union(posts)
            logger.info(f"Created {len(mounting_holes)} mounting posts")
        else:
            logger.warning("Could not find any safe post positions!")
    
    logger.info("Bottom tray generation complete")
    return tray
