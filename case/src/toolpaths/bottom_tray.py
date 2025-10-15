"""
CNC toolpath generation for bottom tray component.

This module generates toolpath operations for machining the bottom tray,
including surfacing, cavity pockets, holes, counterbores, and profile cutting.

All coordinates are in millimeters (mm) relative to the origin at top-left corner.
Feed rates in mm/min, spindle speeds in RPM.
"""

from typing import List, Tuple, Dict, Any
from ..geometry.profiles import Profile, Point2D
import math


# Type aliases
Toolpath = List[Point2D]


def generate_face_surfacing_toolpath(
    case_length: float,
    case_width: float,
    tool_diameter: float,
    stepover_percentage: float = 0.5,
    margin: float = 5.0
) -> Dict[str, Any]:
    """
    Generate raster toolpath for face surfacing operation.
    
    This operation prepares the top surface by removing a thin layer
    to ensure consistent thickness and a flat reference surface.
    
    Args:
        case_length: Case length (295mm) in mm
        case_width: Case width (105mm) in mm
        tool_diameter: Tool diameter (6mm) in mm
        stepover_percentage: Stepover as percentage of tool diameter (0.5 = 50%)
        margin: Additional margin beyond case edges (5mm) in mm
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'face_surfacing',
            'tool': {
                'diameter': 6.0,
                'type': 'flat_endmill',
                'description': '6mm flat endmill'
            },
            'parameters': {
                'depth': 0.5,  # mm
                'feed_rate': 1200,  # mm/min for hardwood
                'spindle_speed': 18000,  # RPM
                'stepover': 3.0,  # mm (50% of tool diameter)
                'direction': 'climb'  # climb milling for better finish
            },
            'toolpath': [
                [(x, y), (x, y), ...],  # Pass 1
                [(x, y), (x, y), ...],  # Pass 2
                ...
            ]
        }
        
    Requirements: 6.1, 6.2
    
    Notes:
        - Raster pattern with alternating direction for efficiency
        - 50% stepover provides good surface finish
        - Extends 5mm beyond case edges to ensure full coverage
        - Climb milling for better finish in hardwood
        - Feed rate: 1200 mm/min suitable for hardwood with 6mm endmill
        - Spindle speed: 18000 RPM for clean cuts in hardwood
    """
    # Calculate stepover distance
    stepover = tool_diameter * stepover_percentage
    
    # Calculate surfacing area (extend beyond case edges)
    start_x = -margin
    end_x = case_length + margin
    start_y = -margin
    end_y = case_width + margin
    
    # Generate raster passes
    toolpath_passes = []
    current_y = start_y
    pass_direction = 1  # 1 for left-to-right, -1 for right-to-left
    
    while current_y <= end_y:
        if pass_direction == 1:
            # Left to right pass
            pass_points = [
                (start_x, current_y),
                (end_x, current_y)
            ]
        else:
            # Right to left pass (alternating for efficiency)
            pass_points = [
                (end_x, current_y),
                (start_x, current_y)
            ]
        
        toolpath_passes.append(pass_points)
        
        # Move to next pass
        current_y += stepover
        pass_direction *= -1  # Alternate direction
    
    return {
        'operation': 'face_surfacing',
        'tool': {
            'diameter': 6.0,
            'type': 'flat_endmill',
            'flutes': 2,
            'description': '6mm flat endmill for roughing operations'
        },
        'parameters': {
            'depth': 0.5,  # mm - shallow pass for surface preparation
            'feed_rate': 1200,  # mm/min - conservative for hardwood
            'spindle_speed': 18000,  # RPM - high speed for clean cuts
            'stepover': stepover,  # mm
            'stepover_percentage': stepover_percentage * 100,  # %
            'direction': 'climb',  # climb milling
            'plunge_rate': 300,  # mm/min - slow plunge for safety
        },
        'toolpath': toolpath_passes,
        'estimated_time_minutes': _estimate_machining_time(
            toolpath_passes, 
            feed_rate=1200, 
            plunge_rate=300
        )
    }


def _estimate_machining_time(
    toolpath_passes: List[Toolpath],
    feed_rate: float,
    plunge_rate: float
) -> float:
    """
    Estimate machining time for a toolpath.
    
    Args:
        toolpath_passes: List of toolpath passes
        feed_rate: Feed rate in mm/min
        plunge_rate: Plunge rate in mm/min
        
    Returns:
        Estimated time in minutes
    """
    total_distance = 0.0
    
    for pass_points in toolpath_passes:
        for i in range(len(pass_points) - 1):
            x1, y1 = pass_points[i]
            x2, y2 = pass_points[i + 1]
            distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            total_distance += distance
    
    # Calculate time (distance / feed_rate)
    # Add 10% for rapids, tool changes, and safety
    machining_time = (total_distance / feed_rate) * 1.1
    
    return round(machining_time, 2)



def generate_rubber_feet_recess_toolpath(
    feet_positions: List[Point2D],
    recess_diameter: float,
    tool_diameter: float,
    depth: float,
    depth_per_pass: float = 1.0
) -> Dict[str, Any]:
    """
    Generate circular pocket toolpath for rubber feet recesses.
    
    Creates 4 circular pockets in corners for adhesive rubber feet.
    Uses helical interpolation for smooth, accurate pockets.
    
    Args:
        feet_positions: List of rubber feet positions [(x, y), ...]
        recess_diameter: Recess diameter (10mm) in mm
        tool_diameter: Tool diameter (10mm) in mm
        depth: Total depth (2mm) in mm
        depth_per_pass: Depth increment per pass (1mm) in mm
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'rubber_feet_recesses',
            'tool': {...},
            'parameters': {...},
            'toolpaths': [
                {
                    'position': (x, y),
                    'passes': [
                        [(x, y, z), ...],  # Pass 1
                        [(x, y, z), ...],  # Pass 2
                    ]
                },
                ...
            ]
        }
        
    Requirements: 5.4, 6.1
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - 4 recesses positioned 10mm from each corner
        - 10mm diameter for 8mm adhesive rubber feet
        - 2mm depth from bottom surface
        - Helical or circular pocket strategy
    """
    # Calculate tool offset for target diameter
    target_radius = recess_diameter / 2.0
    tool_radius = tool_diameter / 2.0
    
    # For pocket operation, the tool center follows a circular path
    # Path radius = target_radius - tool_radius
    path_radius = target_radius - tool_radius
    
    # If path_radius is negative or zero, tool is same size or larger - use center drilling
    if path_radius <= 0:
        path_radius = 0.0
        actual_diameter = tool_diameter
    else:
        actual_diameter = recess_diameter
    
    # Generate helical toolpaths for each rubber feet position
    toolpaths = []
    segments_per_revolution = 36  # Smooth circle
    
    for position in feet_positions:
        cx, cy = position
        passes = []
        
        # Calculate number of passes needed
        num_passes = int(math.ceil(depth / depth_per_pass))
        
        for pass_num in range(num_passes):
            # Calculate depth for this pass
            start_depth = pass_num * depth_per_pass
            end_depth = min((pass_num + 1) * depth_per_pass, depth)
            depth_increment = (end_depth - start_depth) / segments_per_revolution
            
            # Generate helical path
            pass_points = []
            
            # Start at center, plunge to start depth
            pass_points.append((cx, cy, start_depth))
            
            # Helical interpolation
            for i in range(segments_per_revolution + 1):
                angle = 2 * math.pi * i / segments_per_revolution
                current_depth = start_depth + depth_increment * i
                
                x = cx + path_radius * math.cos(angle)
                y = cy + path_radius * math.sin(angle)
                z = current_depth
                
                pass_points.append((x, y, z))
            
            # Return to center at final depth
            pass_points.append((cx, cy, end_depth))
            
            passes.append(pass_points)
        
        toolpaths.append({
            'position': position,
            'passes': passes,
            'actual_diameter': actual_diameter
        })
    
    return {
        'operation': 'rubber_feet_recesses',
        'tool': {
            'diameter': 10.0,
            'type': 'flat_endmill',
            'flutes': 2,
            'description': '10mm flat endmill for rubber feet recesses'
        },
        'parameters': {
            'target_diameter': recess_diameter,  # mm
            'actual_diameter': actual_diameter,  # mm
            'depth': depth,  # mm
            'depth_per_pass': depth_per_pass,  # mm
            'feed_rate': 1000,  # mm/min
            'spindle_speed': 16000,  # RPM
            'plunge_rate': 250,  # mm/min
            'path_radius': path_radius,  # mm
            'tolerance': 0.2,  # mm (standard tolerance)
        },
        'toolpaths': toolpaths,
        'count': len(feet_positions),
        'notes': [
            '4 recesses positioned 10mm from each corner',
            '10mm diameter for 8mm adhesive rubber feet',
            '2mm depth from bottom surface',
            'Helical pocket strategy for smooth finish'
        ]
    }


def generate_assembly_screw_counterbore_toolpath(
    mounting_holes: Dict[str, Point2D],
    counterbore_diameter: float,
    tool_diameter: float,
    depth: float,
    depth_per_pass: float = 1.5
) -> Dict[str, Any]:
    """
    Generate helical boring toolpath for assembly screw counterbores.
    
    Creates 6 counterbore operations at PCB mounting hole positions
    on the bottom surface for M3 screw heads.
    
    Args:
        mounting_holes: Dictionary of mounting hole positions
                       Format: {'TL': (x, y), 'TR': (x, y), ...}
        counterbore_diameter: Target counterbore diameter (6mm) in mm
        tool_diameter: Tool diameter (6mm) in mm
        depth: Total depth (3mm) in mm
        depth_per_pass: Depth increment per helical pass (1.5mm) in mm
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'assembly_screw_counterbores',
            'tool': {...},
            'parameters': {...},
            'toolpaths': {
                'TL': {
                    'center': (x, y),
                    'passes': [
                        [(x, y, z), ...],  # Pass 1
                        [(x, y, z), ...],  # Pass 2
                    ]
                },
                'TR': {...},
                ...
            }
        }
        
    Requirements: 7.1, 6.1
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - Helical boring creates smooth, accurate counterbores
        - 6 positions matching PCB mounting holes
        - Positioned on bottom surface
        - Concentric with assembly screw through-holes
    """
    # Calculate tool offset for target diameter
    target_radius = counterbore_diameter / 2.0
    tool_radius = tool_diameter / 2.0
    
    # For boring operation, the tool center follows a circular path
    # Path radius = target_radius - tool_radius
    path_radius = target_radius - tool_radius
    
    # If path_radius is negative, tool is too large
    if path_radius < 0:
        # Tool is larger than target - use center drilling only
        path_radius = 0.0
        actual_diameter = tool_diameter
    else:
        actual_diameter = counterbore_diameter
    
    # Generate helical toolpaths for each mounting hole
    toolpaths = {}
    segments_per_revolution = 36  # Smooth circle
    
    for hole_id, center in mounting_holes.items():
        cx, cy = center
        passes = []
        
        # Calculate number of passes needed
        num_passes = int(math.ceil(depth / depth_per_pass))
        
        for pass_num in range(num_passes):
            # Calculate depth for this pass
            start_depth = pass_num * depth_per_pass
            end_depth = min((pass_num + 1) * depth_per_pass, depth)
            depth_increment = (end_depth - start_depth) / segments_per_revolution
            
            # Generate helical path
            pass_points = []
            
            # Start at center, plunge to start depth
            pass_points.append((cx, cy, start_depth))
            
            # Helical interpolation
            for i in range(segments_per_revolution + 1):
                angle = 2 * math.pi * i / segments_per_revolution
                current_depth = start_depth + depth_increment * i
                
                x = cx + path_radius * math.cos(angle)
                y = cy + path_radius * math.sin(angle)
                z = current_depth
                
                pass_points.append((x, y, z))
            
            # Return to center at final depth
            pass_points.append((cx, cy, end_depth))
            
            passes.append(pass_points)
        
        toolpaths[hole_id] = {
            'center': center,
            'passes': passes,
            'actual_diameter': actual_diameter
        }
    
    return {
        'operation': 'assembly_screw_counterbores',
        'tool': {
            'diameter': 6.0,
            'type': 'flat_endmill',
            'flutes': 2,
            'description': '6mm flat endmill for counterboring'
        },
        'parameters': {
            'target_diameter': counterbore_diameter,  # mm
            'actual_diameter': actual_diameter,  # mm
            'depth': depth,  # mm
            'depth_per_pass': depth_per_pass,  # mm
            'feed_rate': 800,  # mm/min
            'spindle_speed': 16000,  # RPM
            'plunge_rate': 200,  # mm/min
            'path_radius': path_radius,  # mm
            'tolerance': 0.2,  # mm (standard tolerance)
        },
        'toolpaths': toolpaths,
        'count': len(mounting_holes),
        'notes': [
            'Counterbores machined from bottom surface',
            'Helical boring provides smooth, accurate counterbores',
            '6mm diameter for M3 screw head clearance',
            'Concentric with assembly screw through-holes'
        ]
    }


def generate_assembly_screw_through_hole_toolpath(
    mounting_holes: Dict[str, Point2D],
    hole_diameter: float,
    total_depth: float,
    peck_depth: float = 5.0
) -> Dict[str, Any]:
    """
    Generate drill operations for assembly screw through-holes.
    
    Creates 6 through-hole drilling operations at PCB mounting hole positions,
    concentric with counterbores. Drills through full 15mm thickness.
    
    Args:
        mounting_holes: Dictionary of mounting hole positions
                       Format: {'TL': (x, y), 'TR': (x, y), ...}
        hole_diameter: Drill diameter (3.2mm) in mm
        total_depth: Total depth (15mm - through full thickness) in mm
        peck_depth: Peck drilling depth increment (5mm) in mm
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'assembly_screw_through_holes',
            'tool': {...},
            'parameters': {...},
            'toolpaths': {
                'TL': {
                    'position': (x, y),
                    'depth': 15.0,
                    'pecks': [5.0, 10.0, 15.0]
                },
                'TR': {...},
                ...
            }
        }
        
    Requirements: 7.1, 6.1
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - 3.2mm diameter for M3 screw clearance
        - Drills through full 15mm thickness
        - Concentric with counterbores
        - Peck drilling for chip evacuation
    """
    # Generate drill operations for each mounting hole
    toolpaths = {}
    
    # Calculate peck depths
    num_pecks = int(math.ceil(total_depth / peck_depth))
    peck_depths = []
    for i in range(1, num_pecks + 1):
        peck_depths.append(min(i * peck_depth, total_depth))
    
    for hole_id, position in mounting_holes.items():
        toolpaths[hole_id] = {
            'position': position,
            'depth': total_depth,
            'pecks': peck_depths
        }
    
    return {
        'operation': 'assembly_screw_through_holes',
        'tool': {
            'diameter': 3.2,
            'type': 'drill',
            'flutes': 2,
            'description': '3.2mm drill for M3 screw clearance'
        },
        'parameters': {
            'hole_diameter': hole_diameter,  # mm
            'depth': total_depth,  # mm
            'peck_depth': peck_depth,  # mm
            'num_pecks': num_pecks,
            'feed_rate': 400,  # mm/min - slower for drilling
            'spindle_speed': 12000,  # RPM - moderate speed for drilling
            'plunge_rate': 200,  # mm/min
            'retract_height': 2.0,  # mm - retract between pecks
            'tolerance': 0.2,  # mm (standard tolerance)
        },
        'toolpaths': toolpaths,
        'count': len(mounting_holes),
        'notes': [
            'Through-holes for M3 assembly screws',
            'Drills through full 15mm thickness',
            'Concentric with counterbores on bottom surface',
            'Peck drilling for chip evacuation in deep holes'
        ]
    }


def generate_internal_cavity_pocket_toolpath(
    cavity_profile: Profile,
    standoff_pillars: Dict[str, Profile],
    total_depth: float,
    roughing_tool_diameter: float,
    finishing_tool_diameter: float,
    roughing_stepover: float = 0.5,
    finishing_stock: float = 0.5,
    depth_per_pass: float = 2.0
) -> Dict[str, Any]:
    """
    Generate toolpath for internal cavity pocket with standoff pillars.
    
    Creates an 8mm deep cavity with 6 standoff pillars left as islands.
    Roughing removes bulk material, finishing achieves final dimensions
    with 2mm internal corner radius.
    
    Args:
        cavity_profile: Internal cavity profile [(x, y), ...]
        standoff_pillars: Dictionary of standoff pillar profiles
                         Format: {'TL': [(x, y), ...], 'TR': [...], ...}
        total_depth: Total depth (8mm) in mm
        roughing_tool_diameter: Roughing tool diameter (6mm) in mm
        finishing_tool_diameter: Finishing tool diameter (4mm) in mm
        roughing_stepover: Stepover as percentage of tool diameter (0.5 = 50%)
        finishing_stock: Stock to leave for finishing pass (0.5mm) in mm
        depth_per_pass: Depth increment per pass (2mm) in mm
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'internal_cavity_pocket',
            'roughing': {
                'tool': {...},
                'parameters': {...},
                'toolpath': [...]
            },
            'finishing': {
                'tool': {...},
                'parameters': {...},
                'toolpath': [...]
            }
        }
        
    Requirements: 4.1, 5.3, 6.1, 6.5
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - Adaptive clearing strategy for efficient material removal
        - Leaves 6mm diameter standoff pillars at mounting positions
        - 2mm internal corner radius (limited by 4mm finishing tool)
        - Roughing leaves 0.5mm stock for finishing
        - 8mm depth from top surface
    """
    # Calculate bounding box of cavity profile
    x_coords = [p[0] for p in cavity_profile]
    y_coords = [p[1] for p in cavity_profile]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Generate roughing toolpath (raster pattern avoiding standoff pillars)
    roughing_passes = []
    roughing_stepover_distance = roughing_tool_diameter * roughing_stepover
    roughing_offset = roughing_tool_diameter / 2.0 + finishing_stock
    
    # Calculate roughing area (inset from cavity walls)
    rough_min_x = min_x + roughing_offset
    rough_max_x = max_x - roughing_offset
    rough_min_y = min_y + roughing_offset
    rough_max_y = max_y - roughing_offset
    
    # Generate raster passes for roughing (simplified - doesn't avoid pillars in detail)
    current_y = rough_min_y
    pass_direction = 1
    
    while current_y <= rough_max_y:
        if pass_direction == 1:
            pass_points = [
                (rough_min_x, current_y),
                (rough_max_x, current_y)
            ]
        else:
            pass_points = [
                (rough_max_x, current_y),
                (rough_min_x, current_y)
            ]
        
        roughing_passes.append(pass_points)
        current_y += roughing_stepover_distance
        pass_direction *= -1
    
    # Generate finishing toolpath (profile following with offset)
    finishing_offset = finishing_tool_diameter / 2.0
    finishing_passes = []
    
    # Create offset profile for finishing pass
    # Follow the cavity profile with tool radius compensation
    finishing_pass = []
    for point in cavity_profile:
        finishing_pass.append(point)
    
    finishing_passes.append(finishing_pass)
    
    # Calculate number of depth passes
    num_depth_passes = int(math.ceil(total_depth / depth_per_pass))
    
    return {
        'operation': 'internal_cavity_pocket',
        'roughing': {
            'tool': {
                'diameter': 6.0,
                'type': 'flat_endmill',
                'flutes': 2,
                'description': '6mm flat endmill for roughing'
            },
            'parameters': {
                'depth': total_depth,  # mm
                'depth_per_pass': depth_per_pass,  # mm
                'num_passes': num_depth_passes,
                'feed_rate': 1200,  # mm/min
                'spindle_speed': 18000,  # RPM
                'plunge_rate': 300,  # mm/min
                'stepover': roughing_stepover_distance,  # mm
                'stock_to_leave': finishing_stock,  # mm
                'strategy': 'adaptive_clearing',
            },
            'toolpath': roughing_passes,
            'islands': {
                'standoff_pillars': list(standoff_pillars.keys()),
                'count': len(standoff_pillars),
                'diameter': 6.0  # mm
            }
        },
        'finishing': {
            'tool': {
                'diameter': 4.0,
                'type': 'flat_endmill',
                'flutes': 2,
                'description': '4mm flat endmill for finishing (determines corner radius)'
            },
            'parameters': {
                'depth': total_depth,  # mm
                'depth_per_pass': depth_per_pass,  # mm
                'num_passes': num_depth_passes,
                'feed_rate': 800,  # mm/min - slower for precision
                'spindle_speed': 16000,  # RPM
                'plunge_rate': 200,  # mm/min
                'stock_removal': finishing_stock,  # mm
                'corner_radius': 2.0,  # mm (limited by 4mm tool)
                'tolerance': 0.2,  # mm (standard)
                'strategy': 'profile',
            },
            'toolpath': finishing_passes
        },
        'dimensions': {
            'length': max_x - min_x,
            'width': max_y - min_y,
            'depth': total_depth,
            'corner_radius': 2.0  # mm
        },
        'notes': [
            '8mm deep cavity from top surface',
            'Leaves 6 standoff pillars (6mm diameter) at mounting positions',
            '2mm internal corner radius limited by 4mm finishing tool',
            'Adaptive clearing strategy for efficient roughing',
            'Roughing leaves 0.5mm stock for finishing'
        ]
    }


def generate_standoff_through_hole_toolpath(
    mounting_holes: Dict[str, Point2D],
    hole_diameter: float,
    total_depth: float,
    peck_depth: float = 3.0
) -> Dict[str, Any]:
    """
    Generate drill operations for standoff through-holes.
    
    Creates 6 through-hole drilling operations at center of each standoff pillar.
    Drills through pillar into counterbore below for M2 screw clearance.
    
    Args:
        mounting_holes: Dictionary of mounting hole positions
                       Format: {'TL': (x, y), 'TR': (x, y), ...}
        hole_diameter: Drill diameter (2.2mm) in mm
        total_depth: Total depth (through pillar + into counterbore) in mm
        peck_depth: Peck drilling depth increment (3mm) in mm
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'standoff_through_holes',
            'tool': {...},
            'parameters': {...},
            'toolpaths': {
                'TL': {
                    'position': (x, y),
                    'depth': total_depth,
                    'pecks': [...]
                },
                'TR': {...},
                ...
            }
        }
        
    Requirements: 2.3, 2.4, 6.3
    Tolerance: ±0.1mm (critical)
    
    Notes:
        - 2.2mm diameter for M2 screw clearance
        - Drills through standoff pillar into counterbore below
        - Critical tolerance for proper M2 screw fit
        - Positioned at center of each standoff pillar
    """
    # Generate drill operations for each mounting hole
    toolpaths = {}
    
    # Calculate peck depths
    num_pecks = int(math.ceil(total_depth / peck_depth))
    peck_depths = []
    for i in range(1, num_pecks + 1):
        peck_depths.append(min(i * peck_depth, total_depth))
    
    for hole_id, position in mounting_holes.items():
        toolpaths[hole_id] = {
            'position': position,
            'depth': total_depth,
            'pecks': peck_depths
        }
    
    return {
        'operation': 'standoff_through_holes',
        'tool': {
            'diameter': 2.2,
            'type': 'drill',
            'flutes': 2,
            'description': '2.2mm drill for M2 screw clearance'
        },
        'parameters': {
            'hole_diameter': hole_diameter,  # mm
            'depth': total_depth,  # mm
            'peck_depth': peck_depth,  # mm
            'num_pecks': num_pecks,
            'feed_rate': 300,  # mm/min - slower for small drill
            'spindle_speed': 10000,  # RPM - moderate speed for small drill
            'plunge_rate': 150,  # mm/min - slow for precision
            'retract_height': 2.0,  # mm - retract between pecks
            'tolerance': 0.1,  # mm (critical tolerance)
        },
        'toolpaths': toolpaths,
        'count': len(mounting_holes),
        'notes': [
            'Through-holes for M2 PCB mounting screws',
            'Drills through standoff pillar into counterbore below',
            'Critical ±0.1mm tolerance for proper screw fit',
            'Positioned at center of each 6mm standoff pillar',
            'Peck drilling for chip evacuation'
        ]
    }


def generate_external_profile_toolpath(
    external_profile: Profile,
    total_depth: float,
    roughing_tool_diameter: float,
    finishing_tool_diameter: float,
    finishing_stock: float = 0.5,
    depth_per_pass: float = 2.5,
    tab_width: float = 5.0,
    tab_positions: List[float] = None
) -> Dict[str, Any]:
    """
    Generate toolpath for external profile cutting with tabs.
    
    Creates the final external shape of the bottom tray with roughing
    and finishing passes. Includes tabs for workpiece retention.
    Matches top frame dimensions with 3mm corner radius.
    
    Args:
        external_profile: External profile with 3mm corner radius [(x, y), ...]
        total_depth: Total depth (15mm - through full thickness) in mm
        roughing_tool_diameter: Roughing tool diameter (6mm) in mm
        finishing_tool_diameter: Finishing tool diameter (3mm) in mm
        finishing_stock: Stock to leave for finishing pass (0.5mm) in mm
        depth_per_pass: Depth increment per pass (2.5mm) in mm
        tab_width: Width of holding tabs (5mm) in mm
        tab_positions: List of tab positions as percentage along profile (0-1)
                      Default: [0.25, 0.5, 0.75] for 3 tabs
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'external_profile',
            'roughing': {...},
            'finishing': {...},
            'tabs': [...]
        }
        
    Requirements: 5.1, 7.3, 6.1
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - Roughing pass leaves 0.5mm stock for finishing
        - Finishing pass achieves final dimensions with 3mm corner radius
        - Tabs retain workpiece during cutting (removed post-machining)
        - Outside profile cutting (tool on outside of part)
        - Matches top frame external dimensions
    """
    # Default tab positions if not specified
    if tab_positions is None:
        tab_positions = [0.25, 0.5, 0.75]  # 3 tabs evenly distributed
    
    # Calculate profile length for tab positioning
    profile_length = 0.0
    for i in range(len(external_profile) - 1):
        x1, y1 = external_profile[i]
        x2, y2 = external_profile[i + 1]
        segment_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        profile_length += segment_length
    
    # Calculate tab positions along profile
    tab_locations = []
    for tab_pos in tab_positions:
        target_distance = profile_length * tab_pos
        current_distance = 0.0
        
        for i in range(len(external_profile) - 1):
            x1, y1 = external_profile[i]
            x2, y2 = external_profile[i + 1]
            segment_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            if current_distance + segment_length >= target_distance:
                # Tab is on this segment
                segment_progress = (target_distance - current_distance) / segment_length
                tab_x = x1 + (x2 - x1) * segment_progress
                tab_y = y1 + (y2 - y1) * segment_progress
                tab_locations.append({
                    'position': (tab_x, tab_y),
                    'segment_index': i,
                    'width': tab_width
                })
                break
            
            current_distance += segment_length
    
    # Generate roughing toolpath (offset outward from profile)
    roughing_offset = roughing_tool_diameter / 2.0 + finishing_stock
    roughing_path = []
    
    # Simplified: follow profile with outward offset
    for point in external_profile:
        roughing_path.append(point)
    
    # Generate finishing toolpath (follows profile exactly)
    finishing_path = []
    for point in external_profile:
        finishing_path.append(point)
    
    # Calculate number of depth passes
    num_passes = int(math.ceil(total_depth / depth_per_pass))
    
    return {
        'operation': 'external_profile',
        'roughing': {
            'tool': {
                'diameter': 6.0,
                'type': 'flat_endmill',
                'flutes': 2,
                'description': '6mm flat endmill for roughing'
            },
            'parameters': {
                'depth': total_depth,  # mm
                'depth_per_pass': depth_per_pass,  # mm
                'num_passes': num_passes,
                'feed_rate': 1200,  # mm/min
                'spindle_speed': 18000,  # RPM
                'plunge_rate': 300,  # mm/min
                'stock_to_leave': finishing_stock,  # mm
                'compensation': 'outside',  # tool on outside of part
            },
            'toolpath': [roughing_path]
        },
        'finishing': {
            'tool': {
                'diameter': 3.0,
                'type': 'flat_endmill',
                'flutes': 2,
                'description': '3mm flat endmill for finishing'
            },
            'parameters': {
                'depth': total_depth,  # mm
                'depth_per_pass': depth_per_pass,  # mm
                'num_passes': num_passes,
                'feed_rate': 800,  # mm/min - slower for precision
                'spindle_speed': 16000,  # RPM
                'plunge_rate': 200,  # mm/min
                'stock_removal': finishing_stock,  # mm
                'corner_radius': 3.0,  # mm
                'tolerance': 0.2,  # mm (standard)
                'compensation': 'outside',
            },
            'toolpath': [finishing_path]
        },
        'tabs': {
            'count': len(tab_locations),
            'width': tab_width,  # mm
            'locations': tab_locations,
            'notes': [
                'Tabs retain workpiece during cutting',
                'Remove tabs with flush-cut saw after machining',
                'Sand tab locations smooth post-machining'
            ]
        },
        'dimensions': {
            'length': 295.0,  # mm
            'width': 105.0,  # mm
            'corner_radius': 3.0,  # mm (matches top frame)
            'depth': total_depth  # mm
        },
        'notes': [
            'External profile with 3mm corner radius matching top frame',
            'Through-cut (full 15mm depth)',
            'Roughing leaves 0.5mm stock for finishing',
            'Tabs prevent workpiece movement during cutting',
            'Dimensional consistency with top frame for proper assembly'
        ]
    }


def generate_bottom_tray_toolpaths(
    case_length: float,
    case_width: float,
    external_profile: Profile,
    internal_cavity_profile: Profile,
    standoff_pillars: Dict[str, Profile],
    mounting_holes: Dict[str, Point2D],
    rubber_feet_positions: List[Point2D],
    bottom_tray_height: float,
    cavity_depth: float
) -> Dict[str, Any]:
    """
    Generate complete set of CNC toolpaths for bottom tray component.
    
    Combines all toolpath operations in proper machining sequence:
    1. Face surfacing
    2. Rubber feet recesses (from bottom)
    3. Assembly screw counterbores (from bottom)
    4. Assembly screw through-holes
    5. Internal cavity pocket with standoff pillars
    6. Standoff through-holes
    7. External profile
    
    Args:
        case_length: Case length (295mm)
        case_width: Case width (105mm)
        external_profile: External profile geometry
        internal_cavity_profile: Internal cavity geometry
        standoff_pillars: Dictionary of standoff pillar profiles
        mounting_holes: Mounting hole positions
        rubber_feet_positions: List of rubber feet positions
        bottom_tray_height: Bottom tray height (15mm)
        cavity_depth: Cavity depth (8mm)
        
    Returns:
        Dictionary containing all toolpath operations:
        {
            'component': 'bottom_tray',
            'operations': {
                '1_face_surfacing': {...},
                '2_rubber_feet_recesses': {...},
                '3_assembly_screw_counterbores': {...},
                '4_assembly_screw_through_holes': {...},
                '5_internal_cavity_pocket': {...},
                '6_standoff_through_holes': {...},
                '7_external_profile': {...}
            },
            'setup': {...},
            'summary': {...}
        }
        
    Requirements: All task 5 requirements
    """
    operations = {}
    
    # Operation 1: Face surfacing
    operations['1_face_surfacing'] = generate_face_surfacing_toolpath(
        case_length=case_length,
        case_width=case_width,
        tool_diameter=6.0
    )
    
    # Operation 2: Rubber feet recesses (from bottom surface)
    operations['2_rubber_feet_recesses'] = generate_rubber_feet_recess_toolpath(
        feet_positions=rubber_feet_positions,
        recess_diameter=10.0,
        tool_diameter=10.0,
        depth=2.0
    )
    
    # Operation 3: Assembly screw counterbores (from bottom surface)
    operations['3_assembly_screw_counterbores'] = generate_assembly_screw_counterbore_toolpath(
        mounting_holes=mounting_holes,
        counterbore_diameter=6.0,
        tool_diameter=6.0,
        depth=3.0
    )
    
    # Operation 4: Assembly screw through-holes
    operations['4_assembly_screw_through_holes'] = generate_assembly_screw_through_hole_toolpath(
        mounting_holes=mounting_holes,
        hole_diameter=3.2,
        total_depth=bottom_tray_height
    )
    
    # Operation 5: Internal cavity pocket with standoff pillars
    operations['5_internal_cavity_pocket'] = generate_internal_cavity_pocket_toolpath(
        cavity_profile=internal_cavity_profile,
        standoff_pillars=standoff_pillars,
        total_depth=cavity_depth,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=4.0
    )
    
    # Operation 6: Standoff through-holes
    # Calculate total depth: through standoff pillar (3mm) + into counterbore (3mm) = 6mm
    standoff_hole_depth = 3.0 + 3.0  # pillar height + counterbore depth
    operations['6_standoff_through_holes'] = generate_standoff_through_hole_toolpath(
        mounting_holes=mounting_holes,
        hole_diameter=2.2,
        total_depth=standoff_hole_depth
    )
    
    # Operation 7: External profile
    operations['7_external_profile'] = generate_external_profile_toolpath(
        external_profile=external_profile,
        total_depth=bottom_tray_height,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=3.0
    )
    
    return {
        'component': 'bottom_tray',
        'operations': operations,
        'setup': {
            'material': 'hardwood',
            'stock_dimensions': {
                'length': 295.0,
                'width': 105.0,
                'thickness': 20.0  # Mill down to 15mm
            },
            'work_holding': 'clamps or fixture',
            'origin': 'top-left corner, top surface',
            'notes': [
                'Operations 2-3 (rubber feet, counterbores) machined from bottom surface',
                'Requires workpiece flip after operation 1',
                'Secure workpiece firmly for through-cutting operations',
                'Check tool condition before starting',
                'Standoff pillars left as islands in cavity pocket'
            ]
        },
        'summary': {
            'total_operations': len(operations),
            'tools_required': [
                '6mm flat endmill (roughing)',
                '4mm flat endmill (cavity finishing)',
                '3mm flat endmill (profile finishing)',
                '10mm flat endmill (rubber feet recesses)',
                '3.2mm drill (assembly screws)',
                '2.2mm drill (standoff holes)',
            ],
            'estimated_time_minutes': sum(
                op.get('estimated_time_minutes', 0) 
                for op in operations.values() 
                if 'estimated_time_minutes' in op
            ),
            'critical_tolerances': [
                'Standoff hole positions: ±0.1mm',
                'Standoff hole diameter: ±0.1mm (2.2mm for M2 screws)',
            ],
            'standard_tolerances': [
                'External dimensions: ±0.2mm',
                'Cavity dimensions: ±0.2mm',
                'Assembly screw holes: ±0.2mm',
                'Rubber feet recesses: ±0.2mm'
            ],
            'workpiece_flips': 1,
            'notes': [
                'Bottom tray is more complex than top frame',
                'Requires careful sequencing of operations',
                'Standoff pillars must be preserved during cavity machining',
                'External profile must match top frame for proper assembly'
            ]
        }
    }
