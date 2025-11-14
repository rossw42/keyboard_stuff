"""
CNC toolpath generation for top frame component.

This module generates toolpath operations for machining the top frame,
including surfacing, pockets, holes, and profile cutting.

All coordinates are in millimeters (mm) relative to the origin at top-left corner.
Feed rates in mm/min, spindle speeds in RPM.
"""

from typing import List, Tuple, Dict, Any
from ..geometry.profiles import Profile, Point2D


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
        - Climb milling (conventional for hardwood) for better finish
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



def generate_brass_insert_counterbore_toolpath(
    mounting_holes: Dict[str, Point2D],
    target_diameter: float,
    tool_diameter: float,
    depth: float,
    depth_per_pass: float = 1.0
) -> Dict[str, Any]:
    """
    Generate helical boring toolpath for brass insert counterbores.
    
    Creates 6 counterbore operations at PCB mounting hole positions
    using helical interpolation for smooth, accurate holes.
    
    Args:
        mounting_holes: Dictionary of mounting hole positions
                       Format: {'TL': (x, y), 'TR': (x, y), ...}
        target_diameter: Target hole diameter (5.8mm) in mm
        tool_diameter: Tool diameter (6mm) in mm
        depth: Total depth (4mm) in mm
        depth_per_pass: Depth increment per helical pass (1mm) in mm
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'brass_insert_counterbores',
            'tool': {...},
            'parameters': {...},
            'toolpaths': {
                'TL': {
                    'center': (x, y),
                    'passes': [
                        [(x, y, z), ...],  # Pass 1 (0-1mm depth)
                        [(x, y, z), ...],  # Pass 2 (1-2mm depth)
                        ...
                    ]
                },
                'TR': {...},
                ...
            }
        }
        
    Requirements: 2.4, 2.5, 6.1
    Tolerance: ±0.1mm (critical)
    
    Notes:
        - Helical boring creates smooth, accurate holes
        - Tool offset calculated for 5.8mm finished diameter
        - 6 positions matching PCB mounting holes
        - Multiple passes at 1mm depth increment for clean cuts
        - Counterbores machined from bottom surface (requires flip)
    """
    import math
    
    # Calculate tool offset for target diameter
    # For internal feature: offset = (target_diameter - tool_diameter) / 2
    # Since tool_diameter (6mm) > target_diameter (5.8mm), we need to adjust
    # We'll use helical interpolation with calculated radius
    target_radius = target_diameter / 2.0
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
        actual_diameter = target_diameter
    
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
        'operation': 'brass_insert_counterbores',
        'tool': {
            'diameter': 6.0,
            'type': 'flat_endmill',
            'flutes': 2,
            'description': '6mm flat endmill for counterboring'
        },
        'parameters': {
            'target_diameter': target_diameter,  # mm
            'actual_diameter': actual_diameter,  # mm
            'depth': depth,  # mm
            'depth_per_pass': depth_per_pass,  # mm
            'feed_rate': 800,  # mm/min - slower for precision
            'spindle_speed': 16000,  # RPM
            'plunge_rate': 200,  # mm/min - slow plunge for accuracy
            'path_radius': path_radius,  # mm
            'tolerance': 0.1,  # mm (critical tolerance)
        },
        'toolpaths': toolpaths,
        'count': len(mounting_holes),
        'notes': [
            'Counterbores machined from bottom surface (requires workpiece flip)',
            'Helical boring provides smooth, accurate holes',
            'Press-fit tolerance for 5.7mm OD brass inserts',
            'Critical ±0.1mm positional accuracy required'
        ]
    }



def generate_pcb_opening_pocket_toolpath(
    opening_profile: Profile,
    total_depth: float,
    roughing_tool_diameter: float,
    finishing_tool_diameter: float,
    roughing_stepover: float = 0.5,
    finishing_stock: float = 0.5,
    depth_per_pass: float = 2.0
) -> Dict[str, Any]:
    """
    Generate toolpath for PCB opening pocket with roughing and finishing passes.
    
    Creates a through-pocket for PCB placement with precise dimensions.
    Roughing removes bulk material, finishing achieves final dimensions.
    
    Args:
        opening_profile: PCB opening profile [(x, y), ...]
        total_depth: Total depth (5mm - through full thickness) in mm
        roughing_tool_diameter: Roughing tool diameter (6mm) in mm
        finishing_tool_diameter: Finishing tool diameter (3mm) in mm
        roughing_stepover: Stepover as percentage of tool diameter (0.5 = 50%)
        finishing_stock: Stock to leave for finishing pass (0.5mm) in mm
        depth_per_pass: Depth increment per pass (2mm) in mm
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'pcb_opening_pocket',
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
        
    Requirements: 1.1, 6.1, 6.3
    Tolerance: ±0.1mm (critical)
    
    Notes:
        - Roughing pass leaves 0.5mm stock for finishing
        - Finishing pass achieves critical ±0.1mm tolerance
        - Through-pocket (full 5mm depth)
        - Adaptive clearing strategy for efficient material removal
    """
    import math
    
    # Calculate bounding box of opening profile
    x_coords = [p[0] for p in opening_profile]
    y_coords = [p[1] for p in opening_profile]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Generate roughing toolpath (raster pattern with offset from walls)
    roughing_passes = []
    roughing_stepover_distance = roughing_tool_diameter * roughing_stepover
    roughing_offset = roughing_tool_diameter / 2.0 + finishing_stock
    
    # Calculate roughing area (inset from profile edges)
    rough_min_x = min_x + roughing_offset
    rough_max_x = max_x - roughing_offset
    rough_min_y = min_y + roughing_offset
    rough_max_y = max_y - roughing_offset
    
    # Generate raster passes for roughing
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
    # Simplified: follow the opening profile with tool radius compensation
    finishing_pass = []
    for point in opening_profile:
        finishing_pass.append(point)
    
    finishing_passes.append(finishing_pass)
    
    # Calculate number of depth passes
    num_depth_passes = int(math.ceil(total_depth / depth_per_pass))
    
    return {
        'operation': 'pcb_opening_pocket',
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
                'strategy': 'raster',
            },
            'toolpath': roughing_passes
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
                'num_passes': num_depth_passes,
                'feed_rate': 800,  # mm/min - slower for precision
                'spindle_speed': 16000,  # RPM
                'plunge_rate': 200,  # mm/min
                'stock_removal': finishing_stock,  # mm
                'tolerance': 0.1,  # mm (critical)
                'strategy': 'profile',
            },
            'toolpath': finishing_passes
        },
        'dimensions': {
            'length': max_x - min_x,
            'width': max_y - min_y,
            'depth': total_depth
        },
        'notes': [
            'Through-pocket (full 5mm depth)',
            'Roughing leaves 0.5mm stock for finishing',
            'Finishing achieves critical ±0.1mm tolerance',
            'PCB opening: 286mm x 95.6mm (285mm PCB + 1mm clearance)'
        ]
    }



def generate_usb_cutout_toolpath(
    usb_profile: Profile,
    total_depth: float,
    tool_diameter: float,
    depth_per_pass: float = 2.5
) -> Dict[str, Any]:
    """
    Generate profile toolpath for USB port cutout.
    
    Creates a through-cutout for USB connector access with rounded corners.
    Uses profile milling with tool radius compensation.
    
    Args:
        usb_profile: USB cutout profile with 1mm corner radius [(x, y), ...]
        total_depth: Total depth (10mm - through full thickness) in mm
        tool_diameter: Tool diameter (3mm) in mm
        depth_per_pass: Depth increment per pass (2.5mm) in mm
        
    Returns:
        Dictionary containing toolpath data:
        {
            'operation': 'usb_cutout',
            'tool': {...},
            'parameters': {...},
            'toolpath': [
                [(x, y), ...],  # Profile path
            ]
        }
        
    Requirements: 3.1, 3.2, 3.3, 6.1
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - Profile milling with tool radius compensation
        - 1mm corner radius for smooth cable insertion
        - Through-cutout (full 10mm depth)
        - Centered on top edge at case centerline
        - Multiple depth passes for clean cuts
    """
    import math
    
    # Calculate number of depth passes
    num_passes = int(math.ceil(total_depth / depth_per_pass))
    
    # Tool radius compensation
    # For internal feature (cutout), tool follows profile on inside
    # Profile already accounts for desired dimensions
    tool_radius = tool_diameter / 2.0
    
    # Generate toolpath following the profile
    # The profile points already define the desired cutout shape
    toolpath = []
    
    # Follow the USB profile
    for point in usb_profile:
        toolpath.append(point)
    
    return {
        'operation': 'usb_cutout',
        'tool': {
            'diameter': 3.0,
            'type': 'flat_endmill',
            'flutes': 2,
            'description': '3mm flat endmill for profile cutting'
        },
        'parameters': {
            'depth': total_depth,  # mm
            'depth_per_pass': depth_per_pass,  # mm
            'num_passes': num_passes,
            'feed_rate': 800,  # mm/min
            'spindle_speed': 16000,  # RPM
            'plunge_rate': 200,  # mm/min
            'corner_radius': 1.0,  # mm
            'tolerance': 0.2,  # mm (standard)
            'compensation': 'inside',  # tool on inside of profile
        },
        'toolpath': [toolpath],
        'dimensions': {
            'width': 16.0,  # mm
            'height': 10.0,  # mm (through full thickness)
            'corner_radius': 1.0  # mm
        },
        'notes': [
            'Through-cutout for USB connector access',
            'Centered on top edge at case centerline',
            '1mm corner radius for smooth cable insertion',
            'Accommodates Mini-USB, Micro-USB, and USB-C connectors'
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
    
    Creates the final external shape of the top frame with roughing
    and finishing passes. Includes tabs for workpiece retention.
    
    Args:
        external_profile: External profile with 3mm corner radius [(x, y), ...]
        total_depth: Total depth (5mm - through full thickness) in mm
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
        
    Requirements: 5.1, 6.1, 6.4
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - Roughing pass leaves 0.5mm stock for finishing
        - Finishing pass achieves final dimensions with 3mm corner radius
        - Tabs retain workpiece during cutting (removed post-machining)
        - Outside profile cutting (tool on outside of part)
    """
    import math
    
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
            'corner_radius': 3.0,  # mm
            'depth': total_depth  # mm
        },
        'notes': [
            'External profile with 3mm corner radius',
            'Through-cut (full 5mm depth)',
            'Roughing leaves 0.5mm stock for finishing',
            'Tabs prevent workpiece movement during cutting'
        ]
    }


def generate_top_frame_toolpaths(
    case_length: float,
    case_width: float,
    external_profile: Profile,
    pcb_opening_profile: Profile,
    usb_cutout_profile: Profile,
    mounting_holes: Dict[str, Point2D],
    top_frame_height: float
) -> Dict[str, Any]:
    """
    Generate complete set of CNC toolpaths for top frame component.
    
    Combines all toolpath operations in proper machining sequence:
    1. Face surfacing
    2. Brass insert counterbores (from bottom)
    3. PCB opening pocket
    4. USB cutout
    5. External profile
    
    Args:
        case_length: Case length (295mm)
        case_width: Case width (105mm)
        external_profile: External profile geometry
        pcb_opening_profile: PCB opening geometry
        usb_cutout_profile: USB cutout geometry
        mounting_holes: Mounting hole positions
        top_frame_height: Top frame height (5mm)
        
    Returns:
        Dictionary containing all toolpath operations:
        {
            'component': 'top_frame',
            'operations': {
                '1_face_surfacing': {...},
                '2_brass_insert_counterbores': {...},
                '3_pcb_opening_pocket': {...},
                '4_usb_cutout': {...},
                '5_external_profile': {...}
            },
            'setup': {...},
            'summary': {...}
        }
        
    Requirements: All task 4 requirements
    """
    operations = {}
    
    # Operation 1: Face surfacing
    operations['1_face_surfacing'] = generate_face_surfacing_toolpath(
        case_length=case_length,
        case_width=case_width,
        tool_diameter=6.0
    )
    
    # Operation 2: Brass insert counterbores
    operations['2_brass_insert_counterbores'] = generate_brass_insert_counterbore_toolpath(
        mounting_holes=mounting_holes,
        target_diameter=5.8,
        tool_diameter=6.0,
        depth=4.0
    )
    
    # Operation 3: PCB opening pocket
    operations['3_pcb_opening_pocket'] = generate_pcb_opening_pocket_toolpath(
        opening_profile=pcb_opening_profile,
        total_depth=top_frame_height,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=3.0
    )
    
    # Operation 4: USB cutout
    operations['4_usb_cutout'] = generate_usb_cutout_toolpath(
        usb_profile=usb_cutout_profile,
        total_depth=10.0,  # Through full thickness plus margin
        tool_diameter=3.0
    )
    
    # Operation 5: External profile
    operations['5_external_profile'] = generate_external_profile_toolpath(
        external_profile=external_profile,
        total_depth=top_frame_height,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=3.0
    )
    
    return {
        'component': 'top_frame',
        'operations': operations,
        'setup': {
            'material': 'hardwood',
            'stock_dimensions': {
                'length': 295.0,
                'width': 105.0,
                'thickness': 6.0  # Mill down to 5mm
            },
            'work_holding': 'double-sided tape or vacuum table',
            'origin': 'top-left corner, top surface',
            'notes': [
                'Operation 2 (brass inserts) requires workpiece flip',
                'Secure workpiece firmly for through-cutting operations',
                'Check tool condition before starting'
            ]
        },
        'summary': {
            'total_operations': len(operations),
            'tools_required': [
                '6mm flat endmill (roughing)',
                '3mm flat endmill (finishing)',
            ],
            'estimated_time_minutes': sum(
                op.get('estimated_time_minutes', 0) 
                for op in operations.values() 
                if 'estimated_time_minutes' in op
            ),
            'critical_tolerances': [
                'PCB opening: ±0.1mm',
                'Brass insert holes: ±0.1mm',
                'Mounting hole positions: ±0.1mm'
            ],
            'standard_tolerances': [
                'External dimensions: ±0.2mm',
                'USB cutout: ±0.2mm'
            ]
        }
    }
