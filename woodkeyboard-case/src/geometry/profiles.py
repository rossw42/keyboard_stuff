"""
2D profile geometry generation for keyboard case components.

This module generates 2D geometric profiles for CNC machining operations.
All coordinates are in millimeters (mm) relative to the origin at top-left corner.
"""

import math
from typing import List, Tuple, Dict, Any

# Type aliases
Point2D = Tuple[float, float]
Profile = List[Point2D]


def generate_rounded_rectangle(
    length: float,
    width: float,
    corner_radius: float,
    origin: Point2D = (0.0, 0.0)
) -> Profile:
    """
    Generate a rectangular profile with rounded corners.
    
    Args:
        length: Rectangle length (x-direction) in mm
        width: Rectangle width (y-direction) in mm
        corner_radius: Radius of corner fillets in mm
        origin: Top-left corner position (x, y) in mm
        
    Returns:
        List of (x, y) points defining the profile path
        
    Requirements: 5.1, 6.5
    Tolerance: ±0.2mm (standard)
    """
    x0, y0 = origin
    
    # Calculate corner centers (inset by radius from edges)
    corners = [
        (x0 + corner_radius, y0 + corner_radius),  # Top-left
        (x0 + length - corner_radius, y0 + corner_radius),  # Top-right
        (x0 + length - corner_radius, y0 + width - corner_radius),  # Bottom-right
        (x0 + corner_radius, y0 + width - corner_radius),  # Bottom-left
    ]
    
    # Generate arc points for each corner (16 segments per 90-degree arc)
    segments_per_arc = 16
    profile_points = []
    
    for i, (cx, cy) in enumerate(corners):
        # Starting angle for this corner (0° = right, 90° = down, etc.)
        start_angle = math.radians(90 * i + 180)
        
        # Generate arc points
        for j in range(segments_per_arc + 1):
            angle = start_angle + (math.pi / 2) * (j / segments_per_arc)
            x = cx + corner_radius * math.cos(angle)
            y = cy + corner_radius * math.sin(angle)
            profile_points.append((x, y))
    
    # Close the profile by returning to start point
    if profile_points:
        profile_points.append(profile_points[0])
    
    return profile_points



def generate_external_profile(
    case_length: float,
    case_width: float,
    corner_radius: float
) -> Profile:
    """
    Generate the external profile for top frame or bottom tray.
    
    Args:
        case_length: Case length (295mm) in mm
        case_width: Case width (105mm) in mm
        corner_radius: Corner radius (3mm) in mm
        
    Returns:
        List of (x, y) points defining the external profile
        
    Requirements: 5.1, 6.5
    Tolerance: ±0.2mm (standard)
    """
    return generate_rounded_rectangle(
        length=case_length,
        width=case_width,
        corner_radius=corner_radius,
        origin=(0.0, 0.0)
    )



def generate_pcb_opening(
    opening_length: float,
    opening_width: float,
    case_length: float,
    case_width: float,
    border: float
) -> Profile:
    """
    Generate the PCB opening pocket profile (centered rectangular cutout).
    
    Args:
        opening_length: PCB opening length (286mm) in mm
        opening_width: PCB opening width (95.6mm) in mm
        case_length: Case length (295mm) for centering calculation
        case_width: Case width (105mm) for centering calculation
        border: Border width around PCB (4.5mm) in mm
        
    Returns:
        List of (x, y) points defining the PCB opening profile
        
    Requirements: 1.1, 2.4
    Tolerance: ±0.1mm (critical)
    
    Notes:
        - Opening provides 0.5mm clearance per side around 285mm x 94.6mm PCB
        - Centered with 4.5mm border on all sides
        - Sharp corners (no radius) for maximum PCB support
    """
    # Calculate top-left corner position to center the opening
    x_start = border
    y_start = border
    
    # Generate rectangular profile (sharp corners)
    profile_points = [
        (x_start, y_start),  # Top-left
        (x_start + opening_length, y_start),  # Top-right
        (x_start + opening_length, y_start + opening_width),  # Bottom-right
        (x_start, y_start + opening_width),  # Bottom-left
        (x_start, y_start),  # Close path
    ]
    
    return profile_points



def generate_usb_cutout(
    cutout_width: float,
    cutout_height: float,
    corner_radius: float,
    center_x: float,
    center_y: float
) -> Profile:
    """
    Generate the USB port cutout profile with rounded corners.
    
    Args:
        cutout_width: USB cutout width (16mm) in mm
        cutout_height: USB cutout height (10mm) in mm
        corner_radius: Corner radius (1mm) in mm
        center_x: X-coordinate of cutout center (case_length / 2)
        center_y: Y-coordinate of cutout center (border + offset)
        
    Returns:
        List of (x, y) points defining the USB cutout profile
        
    Requirements: 3.1, 3.2, 3.3
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - Positioned at centerline of case (horizontally centered)
        - 7mm from PCB opening edge (vertically positioned)
        - 1mm corner radius for smooth cable insertion
    """
    # Calculate top-left corner of cutout
    x_start = center_x - cutout_width / 2.0
    y_start = center_y - cutout_height / 2.0
    
    # Generate rounded rectangle centered at specified position
    return generate_rounded_rectangle(
        length=cutout_width,
        width=cutout_height,
        corner_radius=corner_radius,
        origin=(x_start, y_start)
    )



def generate_circle(
    center: Point2D,
    diameter: float,
    segments: int = 32
) -> Profile:
    """
    Generate a circular profile.
    
    Args:
        center: Center point (x, y) in mm
        diameter: Circle diameter in mm
        segments: Number of segments for circle approximation
        
    Returns:
        List of (x, y) points defining the circle
    """
    cx, cy = center
    radius = diameter / 2.0
    
    points = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    
    # Close the circle
    points.append(points[0])
    
    return points


def generate_brass_insert_holes(
    mounting_holes: Dict[str, Point2D],
    insert_diameter: float
) -> Dict[str, Profile]:
    """
    Generate brass insert hole positions at PCB mounting locations.
    
    Args:
        mounting_holes: Dictionary of mounting hole positions
                       Format: {'TL': (x, y), 'TR': (x, y), ...}
        insert_diameter: Brass insert hole diameter (5.8mm) in mm
        
    Returns:
        Dictionary mapping hole IDs to circular profiles
        Format: {'TL': [(x, y), ...], 'TR': [(x, y), ...], ...}
        
    Requirements: 2.2, 2.4, 2.5
    Tolerance: ±0.1mm (critical)
    
    Notes:
        - 6 locations matching PCB mounting hole positions
        - 5.8mm diameter for 5.7mm OD brass inserts (press-fit)
        - Positions calculated from PCB mounting hole coordinates
    """
    brass_holes = {}
    
    for hole_id, position in mounting_holes.items():
        brass_holes[hole_id] = generate_circle(
            center=position,
            diameter=insert_diameter,
            segments=32
        )
    
    return brass_holes



def generate_top_frame_profile(
    case_length: float,
    case_width: float,
    case_corner_radius: float,
    pcb_opening_length: float,
    pcb_opening_width: float,
    pcb_border: float,
    usb_cutout_width: float,
    usb_cutout_height: float,
    usb_corner_radius: float,
    usb_center_x: float,
    usb_center_y: float,
    mounting_holes: Dict[str, Point2D],
    brass_insert_diameter: float
) -> Dict[str, Any]:
    """
    Generate complete top frame 2D profile geometry.
    
    This function generates all geometric features for the top frame component:
    - External profile with rounded corners
    - PCB opening pocket (centered)
    - USB port cutout (centered on top edge)
    - Brass insert hole positions (6 locations)
    
    Args:
        case_length: Case length (295mm)
        case_width: Case width (105mm)
        case_corner_radius: External corner radius (3mm)
        pcb_opening_length: PCB opening length (286mm)
        pcb_opening_width: PCB opening width (95.6mm)
        pcb_border: Border around PCB (4.5mm)
        usb_cutout_width: USB cutout width (16mm)
        usb_cutout_height: USB cutout height (10mm)
        usb_corner_radius: USB cutout corner radius (1mm)
        usb_center_x: USB cutout center X coordinate
        usb_center_y: USB cutout center Y coordinate
        mounting_holes: Dictionary of mounting hole positions
        brass_insert_diameter: Brass insert diameter (5.8mm)
        
    Returns:
        Dictionary containing all profile geometries:
        {
            'external_profile': [(x, y), ...],
            'pcb_opening': [(x, y), ...],
            'usb_cutout': [(x, y), ...],
            'brass_insert_holes': {'TL': [(x, y), ...], 'TR': [...], ...}
        }
        
    Requirements: 1.1, 2.2, 2.4, 2.5, 3.1, 3.2, 3.3, 5.1, 6.5
    """
    return {
        'external_profile': generate_external_profile(
            case_length=case_length,
            case_width=case_width,
            corner_radius=case_corner_radius
        ),
        'pcb_opening': generate_pcb_opening(
            opening_length=pcb_opening_length,
            opening_width=pcb_opening_width,
            case_length=case_length,
            case_width=case_width,
            border=pcb_border
        ),
        'usb_cutout': generate_usb_cutout(
            cutout_width=usb_cutout_width,
            cutout_height=usb_cutout_height,
            corner_radius=usb_corner_radius,
            center_x=usb_center_x,
            center_y=usb_center_y
        ),
        'brass_insert_holes': generate_brass_insert_holes(
            mounting_holes=mounting_holes,
            insert_diameter=brass_insert_diameter
        )
    }


def generate_internal_cavity(
    cavity_length: float,
    cavity_width: float,
    corner_radius: float,
    wall_thickness: float
) -> Profile:
    """
    Generate the internal cavity pocket profile for bottom tray.
    
    Args:
        cavity_length: Cavity length (287mm) in mm
        cavity_width: Cavity width (96.6mm) in mm
        corner_radius: Internal corner radius (2mm) in mm
        wall_thickness: Wall thickness (4mm) in mm
        
    Returns:
        List of (x, y) points defining the cavity profile
        
    Requirements: 4.1, 5.3, 6.5
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - 2mm internal corner radius limited by 4mm endmill
        - 4mm wall thickness for structural integrity
        - Cavity depth is 8mm (specified in CNC operations)
    """
    # Calculate cavity origin (inset by wall thickness)
    x_start = wall_thickness
    y_start = wall_thickness
    
    return generate_rounded_rectangle(
        length=cavity_length,
        width=cavity_width,
        corner_radius=corner_radius,
        origin=(x_start, y_start)
    )


def generate_standoff_pillars(
    mounting_holes: Dict[str, Point2D],
    pillar_diameter: float
) -> Dict[str, Profile]:
    """
    Generate PCB standoff pillar positions (islands within cavity).
    
    Args:
        mounting_holes: Dictionary of mounting hole positions
                       Format: {'TL': (x, y), 'TR': (x, y), ...}
        pillar_diameter: Standoff pillar diameter (6mm) in mm
        
    Returns:
        Dictionary mapping pillar IDs to circular profiles
        Format: {'TL': [(x, y), ...], 'TR': [(x, y), ...], ...}
        
    Requirements: 2.2, 2.4
    Tolerance: ±0.1mm (critical)
    
    Notes:
        - 6 locations matching PCB mounting hole positions
        - 6mm diameter pillars provide stable PCB support
        - Pillars are 3mm high from cavity floor
        - These are islands (material to keep) within the cavity pocket
    """
    pillars = {}
    
    for pillar_id, position in mounting_holes.items():
        pillars[pillar_id] = generate_circle(
            center=position,
            diameter=pillar_diameter,
            segments=32
        )
    
    return pillars


def generate_standoff_holes(
    mounting_holes: Dict[str, Point2D],
    hole_diameter: float
) -> Dict[str, Profile]:
    """
    Generate standoff through-holes at pillar centers.
    
    Args:
        mounting_holes: Dictionary of mounting hole positions
                       Format: {'TL': (x, y), 'TR': (x, y), ...}
        hole_diameter: Through-hole diameter (2.2mm) in mm
        
    Returns:
        Dictionary mapping hole IDs to circular profiles
        Format: {'TL': [(x, y), ...], 'TR': [(x, y), ...], ...}
        
    Requirements: 2.3, 2.4
    Tolerance: ±0.1mm (critical)
    
    Notes:
        - 2.2mm diameter for M2 screw clearance
        - Drilled through standoff pillars into counterbore below
        - Critical tolerance for proper screw fit
    """
    holes = {}
    
    for hole_id, position in mounting_holes.items():
        holes[hole_id] = generate_circle(
            center=position,
            diameter=hole_diameter,
            segments=32
        )
    
    return holes


def generate_assembly_screw_holes(
    mounting_holes: Dict[str, Point2D],
    hole_diameter: float
) -> Dict[str, Profile]:
    """
    Generate assembly screw through-holes (concentric with standoffs).
    
    Args:
        mounting_holes: Dictionary of mounting hole positions
                       Format: {'TL': (x, y), 'TR': (x, y), ...}
        hole_diameter: Through-hole diameter (3.2mm) in mm
        
    Returns:
        Dictionary mapping hole IDs to circular profiles
        Format: {'TL': [(x, y), ...], 'TR': [(x, y), ...], ...}
        
    Requirements: 2.2, 7.1
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - 3.2mm diameter for M3 screw clearance
        - Positioned concentric with standoff pillars
        - Through-holes extend full 15mm height
    """
    holes = {}
    
    for hole_id, position in mounting_holes.items():
        holes[hole_id] = generate_circle(
            center=position,
            diameter=hole_diameter,
            segments=32
        )
    
    return holes


def generate_assembly_screw_counterbores(
    mounting_holes: Dict[str, Point2D],
    counterbore_diameter: float
) -> Dict[str, Profile]:
    """
    Generate assembly screw counterbores on bottom surface.
    
    Args:
        mounting_holes: Dictionary of mounting hole positions
                       Format: {'TL': (x, y), 'TR': (x, y), ...}
        counterbore_diameter: Counterbore diameter (6mm) in mm
        
    Returns:
        Dictionary mapping counterbore IDs to circular profiles
        Format: {'TL': [(x, y), ...], 'TR': [(x, y), ...], ...}
        
    Requirements: 7.1
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - 6mm diameter counterbores for M3 screw heads
        - 3mm depth from bottom surface
        - Positioned on bottom surface, concentric with assembly screws
    """
    counterbores = {}
    
    for hole_id, position in mounting_holes.items():
        counterbores[hole_id] = generate_circle(
            center=position,
            diameter=counterbore_diameter,
            segments=32
        )
    
    return counterbores


def generate_rubber_feet_recesses(
    feet_positions: List[Point2D],
    recess_diameter: float
) -> List[Profile]:
    """
    Generate rubber feet recesses in 4 corners.
    
    Args:
        feet_positions: List of rubber feet positions [(x, y), ...]
        recess_diameter: Recess diameter (10mm) in mm
        
    Returns:
        List of circular profiles for each recess
        
    Requirements: 5.4
    Tolerance: ±0.2mm (standard)
    
    Notes:
        - 10mm diameter recesses for 8mm adhesive rubber feet
        - 2mm depth from bottom surface
        - Positioned 10mm from each corner (measured to center)
        - 4 corners total
    """
    recesses = []
    
    for position in feet_positions:
        recesses.append(
            generate_circle(
                center=position,
                diameter=recess_diameter,
                segments=32
            )
        )
    
    return recesses


def generate_bottom_tray_profile(
    case_length: float,
    case_width: float,
    case_corner_radius: float,
    cavity_length: float,
    cavity_width: float,
    cavity_corner_radius: float,
    wall_thickness: float,
    mounting_holes: Dict[str, Point2D],
    standoff_pillar_diameter: float,
    standoff_hole_diameter: float,
    assembly_screw_diameter: float,
    assembly_counterbore_diameter: float,
    rubber_feet_positions: List[Point2D],
    rubber_feet_diameter: float
) -> Dict[str, Any]:
    """
    Generate complete bottom tray 2D profile geometry.
    
    This function generates all geometric features for the bottom tray component:
    - External profile matching top frame
    - Internal cavity pocket with rounded corners
    - PCB standoff pillars (6 locations)
    - Standoff through-holes for M2 screws
    - Assembly screw holes for M3 screws
    - Assembly screw counterbores
    - Rubber feet recesses (4 corners)
    
    Args:
        case_length: Case length (295mm)
        case_width: Case width (105mm)
        case_corner_radius: External corner radius (3mm)
        cavity_length: Cavity length (287mm)
        cavity_width: Cavity width (96.6mm)
        cavity_corner_radius: Internal corner radius (2mm)
        wall_thickness: Wall thickness (4mm)
        mounting_holes: Dictionary of mounting hole positions
        standoff_pillar_diameter: Standoff pillar diameter (6mm)
        standoff_hole_diameter: Standoff hole diameter (2.2mm)
        assembly_screw_diameter: Assembly screw diameter (3.2mm)
        assembly_counterbore_diameter: Counterbore diameter (6mm)
        rubber_feet_positions: List of rubber feet positions
        rubber_feet_diameter: Rubber feet recess diameter (10mm)
        
    Returns:
        Dictionary containing all profile geometries:
        {
            'external_profile': [(x, y), ...],
            'internal_cavity': [(x, y), ...],
            'standoff_pillars': {'TL': [(x, y), ...], 'TR': [...], ...},
            'standoff_holes': {'TL': [(x, y), ...], 'TR': [...], ...},
            'assembly_screw_holes': {'TL': [(x, y), ...], 'TR': [...], ...},
            'assembly_counterbores': {'TL': [(x, y), ...], 'TR': [...], ...},
            'rubber_feet_recesses': [[(x, y), ...], [(x, y), ...], ...]
        }
        
    Requirements: 2.2, 2.3, 2.4, 4.1, 5.1, 5.3, 5.4, 6.5, 7.1, 7.3
    """
    return {
        'external_profile': generate_external_profile(
            case_length=case_length,
            case_width=case_width,
            corner_radius=case_corner_radius
        ),
        'internal_cavity': generate_internal_cavity(
            cavity_length=cavity_length,
            cavity_width=cavity_width,
            corner_radius=cavity_corner_radius,
            wall_thickness=wall_thickness
        ),
        'standoff_pillars': generate_standoff_pillars(
            mounting_holes=mounting_holes,
            pillar_diameter=standoff_pillar_diameter
        ),
        'standoff_holes': generate_standoff_holes(
            mounting_holes=mounting_holes,
            hole_diameter=standoff_hole_diameter
        ),
        'assembly_screw_holes': generate_assembly_screw_holes(
            mounting_holes=mounting_holes,
            hole_diameter=assembly_screw_diameter
        ),
        'assembly_counterbores': generate_assembly_screw_counterbores(
            mounting_holes=mounting_holes,
            counterbore_diameter=assembly_counterbore_diameter
        ),
        'rubber_feet_recesses': generate_rubber_feet_recesses(
            feet_positions=rubber_feet_positions,
            recess_diameter=rubber_feet_diameter
        )
    }
