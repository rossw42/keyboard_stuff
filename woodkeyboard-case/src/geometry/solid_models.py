"""
3D solid model generation for keyboard case components.

This module generates 3D CAD models from 2D profiles for visualization
and STEP file export. Uses build123d for solid modeling operations.

Requirements: 8.1, 8.4
"""

from typing import Dict, Any, List, Tuple
try:
    from build123d import *
except ImportError:
    raise ImportError(
        "build123d is required for 3D model generation. "
        "Install with: pip install build123d"
    )

from src.geometry.profiles import (
    generate_top_frame_profile,
    generate_bottom_tray_profile
)
from src.constants import (
    # Top frame dimensions
    CASE_LENGTH,
    CASE_WIDTH,
    CASE_CORNER_RADIUS,
    TOP_FRAME_HEIGHT,
    PCB_OPENING_LENGTH,
    PCB_OPENING_WIDTH,
    PCB_BORDER,
    USB_CUTOUT_WIDTH,
    USB_CUTOUT_HEIGHT,
    USB_CUTOUT_CORNER_RADIUS,
    USB_CUTOUT_CENTER_X,
    USB_CUTOUT_CENTER_Y,
    MOUNTING_HOLES,
    BRASS_INSERT_DIAMETER,
    BRASS_INSERT_DEPTH,
    # Bottom tray dimensions
    BOTTOM_TRAY_HEIGHT,
    CAVITY_LENGTH,
    CAVITY_WIDTH,
    CAVITY_CORNER_RADIUS,
    CAVITY_DEPTH,
    WALL_THICKNESS,
    STANDOFF_DIAMETER,
    STANDOFF_HEIGHT,
    STANDOFF_HOLE_DIAMETER,
    ASSEMBLY_SCREW_DIAMETER,
    ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
    ASSEMBLY_SCREW_COUNTERBORE_DEPTH,
    RUBBER_FEET_POSITIONS,
    RUBBER_FEET_DIAMETER,
    RUBBER_FEET_DEPTH,
    # PCB dimensions
    PCB_LENGTH,
    PCB_WIDTH,
    PCB_THICKNESS,
)


def profile_to_wire(profile: List[Tuple[float, float]]) -> Wire:
    """
    Convert a 2D profile (list of points) to a build123d Wire.
    
    Args:
        profile: List of (x, y) coordinate tuples
        
    Returns:
        Wire object representing the profile
    """
    if not profile:
        raise ValueError("Profile must contain at least one point")
    
    # Convert points to build123d Vector objects
    points = [Vector(x, y, 0) for x, y in profile]
    
    # Create polyline from points
    return Wire.make_polygon(points, close=True)


def generate_top_frame_solid() -> Part:
    """
    Generate 3D solid model of the top frame component.
    
    Creates a 5mm thick top frame with:
    - External profile (295mm x 105mm with 3mm corner radius)
    - PCB opening pocket (286mm x 95.6mm, centered)
    - USB port cutout (16mm x 10mm, centered on top edge)
    - Brass insert counterbores (6 locations, 5.8mm dia, 4mm deep)
    
    Returns:
        Part object representing the top frame solid model
        
    Requirements: 8.1
    Tolerance: ±0.1mm (critical), ±0.2mm (standard)
    """
    # Generate 2D profile geometry
    profile_data = generate_top_frame_profile(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        case_corner_radius=CASE_CORNER_RADIUS,
        pcb_opening_length=PCB_OPENING_LENGTH,
        pcb_opening_width=PCB_OPENING_WIDTH,
        pcb_border=PCB_BORDER,
        usb_cutout_width=USB_CUTOUT_WIDTH,
        usb_cutout_height=USB_CUTOUT_HEIGHT,
        usb_corner_radius=USB_CUTOUT_CORNER_RADIUS,
        usb_center_x=USB_CUTOUT_CENTER_X,
        usb_center_y=USB_CUTOUT_CENTER_Y,
        mounting_holes=MOUNTING_HOLES,
        brass_insert_diameter=BRASS_INSERT_DIAMETER
    )
    
    # Start with external profile extrusion
    with BuildPart() as top_frame:
        with BuildSketch() as base_sketch:
            # Create external profile
            ext_wire = profile_to_wire(profile_data['external_profile'])
            make_face(ext_wire)
        
        # Extrude to create base solid
        extrude(amount=TOP_FRAME_HEIGHT)
        
        # Subtract PCB opening pocket (through full thickness)
        with BuildSketch(Plane.XY.offset(TOP_FRAME_HEIGHT)) as pcb_sketch:
            pcb_wire = profile_to_wire(profile_data['pcb_opening'])
            make_face(pcb_wire)
        extrude(amount=-TOP_FRAME_HEIGHT, mode=Mode.SUBTRACT)
        
        # Subtract USB cutout (through full thickness)
        with BuildSketch(Plane.XY.offset(TOP_FRAME_HEIGHT)) as usb_sketch:
            usb_wire = profile_to_wire(profile_data['usb_cutout'])
            make_face(usb_wire)
        extrude(amount=-TOP_FRAME_HEIGHT, mode=Mode.SUBTRACT)
        
        # Add brass insert counterbores (from bottom surface)
        for hole_id, hole_profile in profile_data['brass_insert_holes'].items():
            with BuildSketch(Plane.XY) as brass_sketch:
                brass_wire = profile_to_wire(hole_profile)
                make_face(brass_wire)
            extrude(amount=BRASS_INSERT_DEPTH, mode=Mode.SUBTRACT)
    
    return top_frame.part


def generate_bottom_tray_solid() -> Part:
    """
    Generate 3D solid model of the bottom tray component.
    
    Creates a 15mm thick bottom tray with:
    - External profile matching top frame (295mm x 105mm)
    - Internal cavity (287mm x 96.6mm, 8mm deep)
    - PCB standoff pillars (6 locations, 6mm dia, 3mm high)
    - Standoff through-holes (2.2mm dia)
    - Assembly screw holes (3.2mm dia, through full height)
    - Assembly screw counterbores (6mm dia, 3mm deep)
    - Rubber feet recesses (10mm dia, 2mm deep, 4 corners)
    
    Returns:
        Part object representing the bottom tray solid model
        
    Requirements: 8.1
    Tolerance: ±0.1mm (critical), ±0.2mm (standard)
    """
    # Generate 2D profile geometry
    profile_data = generate_bottom_tray_profile(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        case_corner_radius=CASE_CORNER_RADIUS,
        cavity_length=CAVITY_LENGTH,
        cavity_width=CAVITY_WIDTH,
        cavity_corner_radius=CAVITY_CORNER_RADIUS,
        wall_thickness=WALL_THICKNESS,
        mounting_holes=MOUNTING_HOLES,
        standoff_pillar_diameter=STANDOFF_DIAMETER,
        standoff_hole_diameter=STANDOFF_HOLE_DIAMETER,
        assembly_screw_diameter=ASSEMBLY_SCREW_DIAMETER,
        assembly_counterbore_diameter=ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        rubber_feet_diameter=RUBBER_FEET_DIAMETER
    )
    
    # Start with external profile extrusion
    with BuildPart() as bottom_tray:
        with BuildSketch() as base_sketch:
            # Create external profile
            ext_wire = profile_to_wire(profile_data['external_profile'])
            make_face(ext_wire)
        
        # Extrude to create base solid
        extrude(amount=BOTTOM_TRAY_HEIGHT)
        
        # Subtract internal cavity (8mm deep from top surface)
        with BuildSketch(Plane.XY.offset(BOTTOM_TRAY_HEIGHT)) as cavity_sketch:
            # Create cavity profile
            cavity_wire = profile_to_wire(profile_data['internal_cavity'])
            make_face(cavity_wire)
            
            # Subtract standoff pillars (these are islands to keep)
            for pillar_id, pillar_profile in profile_data['standoff_pillars'].items():
                pillar_wire = profile_to_wire(pillar_profile)
                make_face(pillar_wire, mode=Mode.SUBTRACT)
        
        extrude(amount=-CAVITY_DEPTH, mode=Mode.SUBTRACT)
        
        # Add standoff through-holes (drill through pillars)
        for hole_id, hole_profile in profile_data['standoff_holes'].items():
            with BuildSketch(Plane.XY.offset(BOTTOM_TRAY_HEIGHT)) as standoff_hole_sketch:
                hole_wire = profile_to_wire(hole_profile)
                make_face(hole_wire)
            # Drill through pillar height + into counterbore below
            extrude(amount=-(CAVITY_DEPTH + ASSEMBLY_SCREW_COUNTERBORE_DEPTH), mode=Mode.SUBTRACT)
        
        # Add assembly screw counterbores (from bottom surface)
        for hole_id, counterbore_profile in profile_data['assembly_counterbores'].items():
            with BuildSketch(Plane.XY) as counterbore_sketch:
                cb_wire = profile_to_wire(counterbore_profile)
                make_face(cb_wire)
            extrude(amount=ASSEMBLY_SCREW_COUNTERBORE_DEPTH, mode=Mode.SUBTRACT)
        
        # Add assembly screw through-holes (through full height)
        for hole_id, screw_profile in profile_data['assembly_screw_holes'].items():
            with BuildSketch(Plane.XY.offset(BOTTOM_TRAY_HEIGHT)) as screw_sketch:
                screw_wire = profile_to_wire(screw_profile)
                make_face(screw_wire)
            extrude(amount=-BOTTOM_TRAY_HEIGHT, mode=Mode.SUBTRACT)
        
        # Add rubber feet recesses (from bottom surface)
        for feet_profile in profile_data['rubber_feet_recesses']:
            with BuildSketch(Plane.XY) as feet_sketch:
                feet_wire = profile_to_wire(feet_profile)
                make_face(feet_wire)
            extrude(amount=RUBBER_FEET_DEPTH, mode=Mode.SUBTRACT)
    
    return bottom_tray.part


def generate_pcb_reference() -> Part:
    """
    Generate a reference PCB model for assembly visualization.
    
    Creates a simple rectangular solid representing the PCB:
    - Dimensions: 285mm x 94.6mm x 1.6mm
    - No detailed features (mounting holes, components, etc.)
    
    Returns:
        Part object representing the PCB reference model
        
    Requirements: 8.4
    """
    with BuildPart() as pcb:
        with BuildSketch() as pcb_sketch:
            # Create rectangle with corner at origin (not centered)
            Rectangle(PCB_LENGTH, PCB_WIDTH, align=(Align.MIN, Align.MIN))
        extrude(amount=PCB_THICKNESS)
    
    return pcb.part


def generate_assembly_model() -> Compound:
    """
    Generate complete assembly model with all components.
    
    Creates an assembly with:
    - Top frame (positioned at top)
    - Bottom tray (positioned at bottom)
    - PCB reference (positioned between components)
    
    Component positioning:
    - Bottom tray: Origin at (0, 0, 0)
    - PCB: Centered in cavity, resting on standoffs
    - Top frame: Positioned on top of PCB
    
    Returns:
        Compound object representing the complete assembly
        
    Requirements: 8.4
    
    Notes:
        - Hardware models (screws, inserts) not included in this version
        - Components positioned in assembled configuration
        - PCB centered with proper clearances
    """
    # Generate individual components
    top_frame = generate_top_frame_solid()
    bottom_tray = generate_bottom_tray_solid()
    pcb = generate_pcb_reference()
    
    # Calculate positions
    # Bottom tray at origin
    bottom_tray_pos = Vector(0, 0, 0)
    
    # PCB rests on standoffs (cavity floor + standoff height)
    pcb_z = BOTTOM_TRAY_HEIGHT - CAVITY_DEPTH + STANDOFF_HEIGHT
    # PCB is centered in the case opening
    pcb_x = PCB_BORDER
    pcb_y = PCB_BORDER
    pcb_pos = Vector(pcb_x, pcb_y, pcb_z)
    
    # Top frame sits on top of bottom tray
    top_frame_z = BOTTOM_TRAY_HEIGHT
    top_frame_pos = Vector(0, 0, top_frame_z)
    
    # Create compound assembly
    bottom_tray_positioned = bottom_tray.moved(Location(bottom_tray_pos))
    pcb_positioned = pcb.moved(Location(pcb_pos))
    top_frame_positioned = top_frame.moved(Location(top_frame_pos))
    
    # Create compound from all parts
    assembly = Compound([bottom_tray_positioned, pcb_positioned, top_frame_positioned])
    
    return assembly


def export_step(part: Part, filepath: str) -> None:
    """
    Export a Part object to STEP format.
    
    Args:
        part: Part object to export
        filepath: Output file path (should end with .step or .stp)
        
    Requirements: 8.1, 8.4
    """
    from build123d import export_step as bd_export_step
    bd_export_step(part, filepath)


def export_stl(part: Part, filepath: str, tolerance: float = 0.01) -> None:
    """
    Export a Part object to STL format for visualization.
    
    Args:
        part: Part object to export
        filepath: Output file path (should end with .stl)
        tolerance: Mesh tolerance in mm (default 0.01mm)
        
    Note: STL export is for visualization only, not for manufacturing
    """
    from build123d import export_stl as bd_export_stl
    bd_export_stl(part, filepath, tolerance=tolerance)
