"""
Technical drawing export utilities for 2D CAD formats (DXF, PDF).

This module provides functions to export 2D profile geometry as technical
drawings with dimensions, annotations, and tolerance callouts.
"""

import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment
from typing import List, Tuple, Dict, Any
import os
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors as pdf_colors


# Type aliases
Point2D = Tuple[float, float]
Profile = List[Point2D]


def create_dxf_document():
    """
    Create a new DXF document with standard setup.
    
    Returns:
        DXF document object
    """
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    return doc, msp


def add_polyline_to_dxf(msp, points: Profile, layer: str = '0', color: int = colors.WHITE, closed: bool = True):
    """
    Add a polyline to the DXF modelspace.
    
    Args:
        msp: DXF modelspace object
        points: List of (x, y) coordinates
        layer: Layer name
        color: Color index
        closed: Whether to close the polyline
    """
    if not points:
        return
    
    # Create polyline
    polyline = msp.add_lwpolyline(points, dxfattribs={'layer': layer, 'color': color})
    if closed and len(points) > 2:
        polyline.close()


def add_circle_to_dxf(msp, center: Point2D, diameter: float, layer: str = '0', color: int = colors.WHITE):
    """
    Add a circle to the DXF modelspace.
    
    Args:
        msp: DXF modelspace object
        center: Circle center (x, y)
        diameter: Circle diameter
        layer: Layer name
        color: Color index
    """
    radius = diameter / 2.0
    msp.add_circle(center, radius, dxfattribs={'layer': layer, 'color': color})


def add_dimension_linear(msp, start: Point2D, end: Point2D, offset: float, text: str = None, layer: str = 'DIMENSIONS'):
    """
    Add a linear dimension to the DXF.
    
    Args:
        msp: DXF modelspace object
        start: Start point (x, y)
        end: End point (x, y)
        offset: Offset distance from the measured line
        text: Optional dimension text override
        layer: Layer name
    """
    dim = msp.add_linear_dim(
        base=(start[0], start[1] + offset),
        p1=start,
        p2=end,
        dimstyle='EZDXF',
        dxfattribs={'layer': layer}
    )
    if text:
        dim.set_text(text)


def add_text(msp, position: Point2D, text: str, height: float = 2.5, layer: str = 'TEXT', 
             alignment: str = 'LEFT'):
    """
    Add text annotation to the DXF.
    
    Args:
        msp: DXF modelspace object
        position: Text position (x, y)
        text: Text content
        height: Text height
        layer: Layer name
        alignment: Text alignment ('LEFT', 'CENTER', 'RIGHT')
    """
    align_map = {
        'LEFT': TextEntityAlignment.LEFT,
        'CENTER': TextEntityAlignment.CENTER,
        'RIGHT': TextEntityAlignment.RIGHT,
    }
    
    msp.add_text(
        text,
        dxfattribs={
            'layer': layer,
            'height': height,
            'insert': position,
            'halign': align_map.get(alignment, TextEntityAlignment.LEFT)
        }
    )


def export_top_frame_dxf(profile_data: Dict[str, Any], output_path: str):
    """
    Export top frame profile to DXF format with dimensions and annotations.
    
    Args:
        profile_data: Dictionary containing profile geometry from generate_top_frame_profile()
        output_path: Output file path for DXF
        
    Requirements: 8.1, 8.2, 8.3
    """
    doc, msp = create_dxf_document()
    
    # Create layers
    doc.layers.add('EXTERNAL', color=colors.WHITE)
    doc.layers.add('PCB_OPENING', color=colors.CYAN)
    doc.layers.add('USB_CUTOUT', color=colors.GREEN)
    doc.layers.add('BRASS_INSERTS', color=colors.YELLOW)
    doc.layers.add('DIMENSIONS', color=colors.RED)
    doc.layers.add('TEXT', color=colors.WHITE)
    
    # Add external profile
    add_polyline_to_dxf(msp, profile_data['external_profile'], layer='EXTERNAL', color=colors.WHITE)
    
    # Add PCB opening
    add_polyline_to_dxf(msp, profile_data['pcb_opening'], layer='PCB_OPENING', color=colors.CYAN)
    
    # Add USB cutout
    add_polyline_to_dxf(msp, profile_data['usb_cutout'], layer='USB_CUTOUT', color=colors.GREEN)
    
    # Add brass insert holes
    for hole_id, hole_profile in profile_data['brass_insert_holes'].items():
        # Get center point (first point of circle)
        if hole_profile:
            center = hole_profile[0]
            # Calculate center from circle points
            xs = [p[0] for p in hole_profile]
            ys = [p[1] for p in hole_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            add_circle_to_dxf(msp, center, 5.8, layer='BRASS_INSERTS', color=colors.YELLOW)
    
    # Save DXF
    doc.saveas(output_path)
    print(f"✓ Exported top frame DXF: {output_path}")


def export_bottom_tray_dxf(profile_data: Dict[str, Any], output_path: str):
    """
    Export bottom tray profile to DXF format with dimensions and annotations.
    
    Args:
        profile_data: Dictionary containing profile geometry from generate_bottom_tray_profile()
        output_path: Output file path for DXF
        
    Requirements: 8.1, 8.2, 8.3
    """
    doc, msp = create_dxf_document()
    
    # Create layers
    doc.layers.add('EXTERNAL', color=colors.WHITE)
    doc.layers.add('CAVITY', color=colors.CYAN)
    doc.layers.add('STANDOFF_PILLARS', color=colors.GREEN)
    doc.layers.add('STANDOFF_HOLES', color=colors.YELLOW)
    doc.layers.add('ASSEMBLY_SCREWS', color=colors.MAGENTA)
    doc.layers.add('COUNTERBORES', color=colors.RED)
    doc.layers.add('RUBBER_FEET', color=colors.BLUE)
    doc.layers.add('DIMENSIONS', color=colors.RED)
    doc.layers.add('TEXT', color=colors.WHITE)
    
    # Add external profile
    add_polyline_to_dxf(msp, profile_data['external_profile'], layer='EXTERNAL', color=colors.WHITE)
    
    # Add internal cavity
    add_polyline_to_dxf(msp, profile_data['internal_cavity'], layer='CAVITY', color=colors.CYAN)
    
    # Add standoff pillars
    for pillar_id, pillar_profile in profile_data['standoff_pillars'].items():
        if pillar_profile:
            xs = [p[0] for p in pillar_profile]
            ys = [p[1] for p in pillar_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            add_circle_to_dxf(msp, center, 6.0, layer='STANDOFF_PILLARS', color=colors.GREEN)
    
    # Add standoff holes
    for hole_id, hole_profile in profile_data['standoff_holes'].items():
        if hole_profile:
            xs = [p[0] for p in hole_profile]
            ys = [p[1] for p in hole_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            add_circle_to_dxf(msp, center, 2.2, layer='STANDOFF_HOLES', color=colors.YELLOW)
    
    # Add assembly screw holes
    for hole_id, hole_profile in profile_data['assembly_screw_holes'].items():
        if hole_profile:
            xs = [p[0] for p in hole_profile]
            ys = [p[1] for p in hole_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            add_circle_to_dxf(msp, center, 3.2, layer='ASSEMBLY_SCREWS', color=colors.MAGENTA)
    
    # Add assembly counterbores
    for cb_id, cb_profile in profile_data['assembly_counterbores'].items():
        if cb_profile:
            xs = [p[0] for p in cb_profile]
            ys = [p[1] for p in cb_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            add_circle_to_dxf(msp, center, 6.0, layer='COUNTERBORES', color=colors.RED)
    
    # Add rubber feet recesses
    for recess_profile in profile_data['rubber_feet_recesses']:
        if recess_profile:
            xs = [p[0] for p in recess_profile]
            ys = [p[1] for p in recess_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            add_circle_to_dxf(msp, center, 10.0, layer='RUBBER_FEET', color=colors.BLUE)
    
    # Save DXF
    doc.saveas(output_path)
    print(f"✓ Exported bottom tray DXF: {output_path}")



def export_top_frame_pdf(profile_data: Dict[str, Any], output_path: str, 
                         case_length: float, case_width: float, 
                         pcb_opening_length: float, pcb_opening_width: float,
                         usb_cutout_width: float, usb_cutout_height: float,
                         brass_insert_diameter: float, top_frame_height: float,
                         tolerance_critical: float, tolerance_standard: float,
                         mounting_holes: Dict[str, Point2D]):
    """
    Export top frame profile to PDF format with dimensions and annotations.
    
    Args:
        profile_data: Dictionary containing profile geometry
        output_path: Output file path for PDF
        case_length: Case length (295mm)
        case_width: Case width (105mm)
        pcb_opening_length: PCB opening length (286mm)
        pcb_opening_width: PCB opening width (95.6mm)
        usb_cutout_width: USB cutout width (16mm)
        usb_cutout_height: USB cutout height (10mm)
        brass_insert_diameter: Brass insert diameter (5.8mm)
        top_frame_height: Top frame height (5mm)
        tolerance_critical: Critical tolerance (±0.1mm)
        tolerance_standard: Standard tolerance (±0.2mm)
        mounting_holes: Dictionary of mounting hole positions
        
    Requirements: 8.1, 8.2, 8.3
    """
    # Create PDF canvas (A3 landscape)
    page_width, page_height = landscape(A3)
    c = canvas.Canvas(output_path, pagesize=landscape(A3))
    
    # Scale factor to fit drawing on page (with margins)
    margin = 50 * mm
    available_width = page_width - 2 * margin - 200 * mm  # Reserve space for notes
    available_height = page_height - 2 * margin - 100 * mm  # Reserve space for title
    
    scale_x = available_width / case_length
    scale_y = available_height / case_width
    scale = min(scale_x, scale_y)
    
    # Drawing origin (bottom-left of drawing area)
    origin_x = margin
    origin_y = page_height - margin - 80 * mm
    
    def transform_point(p: Point2D) -> Tuple[float, float]:
        """Transform model coordinates to PDF coordinates."""
        return (origin_x + p[0] * scale, origin_y - p[1] * scale)
    
    # Title block
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, page_height - margin, "60% KEYBOARD CASE - TOP FRAME")
    c.setFont("Helvetica", 10)
    c.drawString(margin, page_height - margin - 15, f"Component Height: {top_frame_height}mm")
    c.drawString(margin, page_height - margin - 30, f"Material: Hardwood (Walnut, Maple, or Cherry)")
    c.drawString(margin, page_height - margin - 45, f"Stock Thickness: 6mm (mill to {top_frame_height}mm)")
    
    # Draw external profile
    c.setStrokeColor(pdf_colors.black)
    c.setLineWidth(1.5)
    points = [transform_point(p) for p in profile_data['external_profile']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # Draw PCB opening
    c.setStrokeColor(pdf_colors.blue)
    c.setLineWidth(1.0)
    points = [transform_point(p) for p in profile_data['pcb_opening']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # Draw USB cutout
    c.setStrokeColor(pdf_colors.green)
    points = [transform_point(p) for p in profile_data['usb_cutout']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # Draw brass insert holes
    c.setStrokeColor(pdf_colors.red)
    for hole_id, hole_profile in profile_data['brass_insert_holes'].items():
        if hole_profile:
            xs = [p[0] for p in hole_profile]
            ys = [p[1] for p in hole_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            center_pdf = transform_point(center)
            radius = brass_insert_diameter / 2.0 * scale
            c.circle(center_pdf[0], center_pdf[1], radius, stroke=1, fill=0)
    
    # Add dimensions and annotations
    c.setFont("Helvetica", 8)
    c.setStrokeColor(pdf_colors.black)
    
    # External dimensions
    dim_offset = 15 * mm
    c.setLineWidth(0.5)
    # Length dimension
    p1 = transform_point((0, 0))
    p2 = transform_point((case_length, 0))
    c.line(p1[0], p1[1] - dim_offset, p2[0], p2[1] - dim_offset)
    c.drawString((p1[0] + p2[0]) / 2 - 20, p1[1] - dim_offset - 10, 
                 f"{case_length}mm ±{tolerance_standard}mm")
    
    # Width dimension
    p1 = transform_point((0, 0))
    p2 = transform_point((0, case_width))
    c.line(p1[0] - dim_offset, p1[1], p2[0] - dim_offset, p2[1])
    c.saveState()
    c.translate(p1[0] - dim_offset - 10, (p1[1] + p2[1]) / 2)
    c.rotate(90)
    c.drawString(-20, 0, f"{case_width}mm ±{tolerance_standard}mm")
    c.restoreState()
    
    # Notes section
    notes_x = page_width - margin - 180 * mm
    notes_y = page_height - margin - 80 * mm
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(notes_x, notes_y, "CRITICAL DIMENSIONS")
    c.setFont("Helvetica", 8)
    y_offset = notes_y - 15
    c.drawString(notes_x, y_offset, f"Tolerance: ±{tolerance_critical}mm")
    y_offset -= 15
    c.drawString(notes_x, y_offset, f"• PCB Opening: {pcb_opening_length} × {pcb_opening_width}mm")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Brass Insert Holes: Ø{brass_insert_diameter}mm (6x)")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Insert Depth: 4mm from bottom")
    
    y_offset -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(notes_x, y_offset, "STANDARD DIMENSIONS")
    c.setFont("Helvetica", 8)
    y_offset -= 15
    c.drawString(notes_x, y_offset, f"Tolerance: ±{tolerance_standard}mm")
    y_offset -= 15
    c.drawString(notes_x, y_offset, f"• External: {case_length} × {case_width}mm")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Corner Radius: 3mm")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• USB Cutout: {usb_cutout_width} × {usb_cutout_height}mm")
    
    y_offset -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(notes_x, y_offset, "MOUNTING HOLES")
    c.setFont("Helvetica", 8)
    y_offset -= 15
    for hole_id, (x, y) in sorted(mounting_holes.items()):
        c.drawString(notes_x, y_offset, f"• {hole_id}: ({x:.1f}, {y:.1f})mm")
        y_offset -= 12
    
    y_offset -= 15
    c.setFont("Helvetica-Bold", 10)
    c.drawString(notes_x, y_offset, "HARDWARE")
    c.setFont("Helvetica", 8)
    y_offset -= 15
    c.drawString(notes_x, y_offset, "• Brass Inserts: M3 × 5.7mm OD × 4mm")
    y_offset -= 12
    c.drawString(notes_x, y_offset, "• Quantity: 6 inserts")
    
    # Legend
    legend_y = margin + 50
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, legend_y, "LEGEND:")
    c.setFont("Helvetica", 8)
    legend_y -= 15
    
    c.setStrokeColor(pdf_colors.black)
    c.setLineWidth(1.5)
    c.line(margin, legend_y, margin + 20, legend_y)
    c.drawString(margin + 25, legend_y - 3, "External Profile")
    
    legend_y -= 12
    c.setStrokeColor(pdf_colors.blue)
    c.setLineWidth(1.0)
    c.line(margin, legend_y, margin + 20, legend_y)
    c.drawString(margin + 25, legend_y - 3, "PCB Opening")
    
    legend_y -= 12
    c.setStrokeColor(pdf_colors.green)
    c.line(margin, legend_y, margin + 20, legend_y)
    c.drawString(margin + 25, legend_y - 3, "USB Cutout")
    
    legend_y -= 12
    c.setStrokeColor(pdf_colors.red)
    c.circle(margin + 10, legend_y, 3, stroke=1, fill=0)
    c.drawString(margin + 25, legend_y - 3, "Brass Insert Holes")
    
    # Save PDF
    c.save()
    print(f"✓ Exported top frame PDF: {output_path}")



def export_bottom_tray_pdf(profile_data: Dict[str, Any], output_path: str,
                           case_length: float, case_width: float,
                           cavity_length: float, cavity_width: float,
                           cavity_depth: float, wall_thickness: float,
                           standoff_diameter: float, standoff_hole_diameter: float,
                           assembly_screw_diameter: float, assembly_counterbore_diameter: float,
                           rubber_feet_diameter: float, bottom_tray_height: float,
                           tolerance_critical: float, tolerance_standard: float,
                           mounting_holes: Dict[str, Point2D],
                           rubber_feet_positions: List[Point2D]):
    """
    Export bottom tray profile to PDF format with dimensions and annotations.
    
    Args:
        profile_data: Dictionary containing profile geometry
        output_path: Output file path for PDF
        case_length: Case length (295mm)
        case_width: Case width (105mm)
        cavity_length: Cavity length (287mm)
        cavity_width: Cavity width (96.6mm)
        cavity_depth: Cavity depth (8mm)
        wall_thickness: Wall thickness (4mm)
        standoff_diameter: Standoff pillar diameter (6mm)
        standoff_hole_diameter: Standoff hole diameter (2.2mm)
        assembly_screw_diameter: Assembly screw diameter (3.2mm)
        assembly_counterbore_diameter: Counterbore diameter (6mm)
        rubber_feet_diameter: Rubber feet recess diameter (10mm)
        bottom_tray_height: Bottom tray height (15mm)
        tolerance_critical: Critical tolerance (±0.1mm)
        tolerance_standard: Standard tolerance (±0.2mm)
        mounting_holes: Dictionary of mounting hole positions
        rubber_feet_positions: List of rubber feet positions
        
    Requirements: 8.1, 8.2, 8.3
    """
    # Create PDF canvas (A3 landscape)
    page_width, page_height = landscape(A3)
    c = canvas.Canvas(output_path, pagesize=landscape(A3))
    
    # Scale factor to fit drawing on page (with margins)
    margin = 50 * mm
    available_width = page_width - 2 * margin - 200 * mm  # Reserve space for notes
    available_height = page_height - 2 * margin - 100 * mm  # Reserve space for title
    
    scale_x = available_width / case_length
    scale_y = available_height / case_width
    scale = min(scale_x, scale_y)
    
    # Drawing origin (bottom-left of drawing area)
    origin_x = margin
    origin_y = page_height - margin - 80 * mm
    
    def transform_point(p: Point2D) -> Tuple[float, float]:
        """Transform model coordinates to PDF coordinates."""
        return (origin_x + p[0] * scale, origin_y - p[1] * scale)
    
    # Title block
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, page_height - margin, "60% KEYBOARD CASE - BOTTOM TRAY")
    c.setFont("Helvetica", 10)
    c.drawString(margin, page_height - margin - 15, f"Component Height: {bottom_tray_height}mm")
    c.drawString(margin, page_height - margin - 30, f"Cavity Depth: {cavity_depth}mm")
    c.drawString(margin, page_height - margin - 45, f"Material: Hardwood (Walnut, Maple, or Cherry)")
    c.drawString(margin, page_height - margin - 60, f"Stock Thickness: 20mm (mill to {bottom_tray_height}mm)")
    
    # Draw external profile
    c.setStrokeColor(pdf_colors.black)
    c.setLineWidth(1.5)
    points = [transform_point(p) for p in profile_data['external_profile']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # Draw internal cavity
    c.setStrokeColor(pdf_colors.blue)
    c.setLineWidth(1.0)
    points = [transform_point(p) for p in profile_data['internal_cavity']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # Draw standoff pillars
    c.setStrokeColor(pdf_colors.green)
    for pillar_id, pillar_profile in profile_data['standoff_pillars'].items():
        if pillar_profile:
            xs = [p[0] for p in pillar_profile]
            ys = [p[1] for p in pillar_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            center_pdf = transform_point(center)
            radius = standoff_diameter / 2.0 * scale
            c.circle(center_pdf[0], center_pdf[1], radius, stroke=1, fill=0)
    
    # Draw standoff holes
    c.setStrokeColor(pdf_colors.orange)
    for hole_id, hole_profile in profile_data['standoff_holes'].items():
        if hole_profile:
            xs = [p[0] for p in hole_profile]
            ys = [p[1] for p in hole_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            center_pdf = transform_point(center)
            radius = standoff_hole_diameter / 2.0 * scale
            c.circle(center_pdf[0], center_pdf[1], radius, stroke=1, fill=0)
    
    # Draw assembly screw holes
    c.setStrokeColor(pdf_colors.purple)
    for hole_id, hole_profile in profile_data['assembly_screw_holes'].items():
        if hole_profile:
            xs = [p[0] for p in hole_profile]
            ys = [p[1] for p in hole_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            center_pdf = transform_point(center)
            radius = assembly_screw_diameter / 2.0 * scale
            c.circle(center_pdf[0], center_pdf[1], radius, stroke=1, fill=0)
    
    # Draw rubber feet recesses
    c.setStrokeColor(pdf_colors.brown)
    for recess_profile in profile_data['rubber_feet_recesses']:
        if recess_profile:
            xs = [p[0] for p in recess_profile]
            ys = [p[1] for p in recess_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            center_pdf = transform_point(center)
            radius = rubber_feet_diameter / 2.0 * scale
            c.circle(center_pdf[0], center_pdf[1], radius, stroke=1, fill=0)
    
    # Add dimensions
    c.setFont("Helvetica", 8)
    c.setStrokeColor(pdf_colors.black)
    
    # External dimensions
    dim_offset = 15 * mm
    c.setLineWidth(0.5)
    # Length dimension
    p1 = transform_point((0, 0))
    p2 = transform_point((case_length, 0))
    c.line(p1[0], p1[1] - dim_offset, p2[0], p2[1] - dim_offset)
    c.drawString((p1[0] + p2[0]) / 2 - 20, p1[1] - dim_offset - 10, 
                 f"{case_length}mm ±{tolerance_standard}mm")
    
    # Width dimension
    p1 = transform_point((0, 0))
    p2 = transform_point((0, case_width))
    c.line(p1[0] - dim_offset, p1[1], p2[0] - dim_offset, p2[1])
    c.saveState()
    c.translate(p1[0] - dim_offset - 10, (p1[1] + p2[1]) / 2)
    c.rotate(90)
    c.drawString(-20, 0, f"{case_width}mm ±{tolerance_standard}mm")
    c.restoreState()
    
    # Notes section
    notes_x = page_width - margin - 180 * mm
    notes_y = page_height - margin - 80 * mm
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(notes_x, notes_y, "CRITICAL DIMENSIONS")
    c.setFont("Helvetica", 8)
    y_offset = notes_y - 15
    c.drawString(notes_x, y_offset, f"Tolerance: ±{tolerance_critical}mm")
    y_offset -= 15
    c.drawString(notes_x, y_offset, f"• Standoff Pillars: Ø{standoff_diameter}mm (6x)")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Standoff Holes: Ø{standoff_hole_diameter}mm (M2)")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Pillar Height: 3mm from cavity floor")
    
    y_offset -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(notes_x, y_offset, "STANDARD DIMENSIONS")
    c.setFont("Helvetica", 8)
    y_offset -= 15
    c.drawString(notes_x, y_offset, f"Tolerance: ±{tolerance_standard}mm")
    y_offset -= 15
    c.drawString(notes_x, y_offset, f"• External: {case_length} × {case_width}mm")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Cavity: {cavity_length} × {cavity_width}mm")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Cavity Depth: {cavity_depth}mm")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Wall Thickness: {wall_thickness}mm")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Assembly Screws: Ø{assembly_screw_diameter}mm (M3)")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Counterbores: Ø{assembly_counterbore_diameter}mm × 3mm deep")
    y_offset -= 12
    c.drawString(notes_x, y_offset, f"• Rubber Feet: Ø{rubber_feet_diameter}mm × 2mm deep")
    
    y_offset -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(notes_x, y_offset, "MOUNTING POSITIONS")
    c.setFont("Helvetica", 8)
    y_offset -= 15
    for hole_id, (x, y) in sorted(mounting_holes.items()):
        c.drawString(notes_x, y_offset, f"• {hole_id}: ({x:.1f}, {y:.1f})mm")
        y_offset -= 12
    
    y_offset -= 15
    c.setFont("Helvetica-Bold", 10)
    c.drawString(notes_x, y_offset, "HARDWARE")
    c.setFont("Helvetica", 8)
    y_offset -= 15
    c.drawString(notes_x, y_offset, "• M2 Screws: 6x (PCB mounting)")
    y_offset -= 12
    c.drawString(notes_x, y_offset, "• M3 Screws: 6x (case assembly)")
    y_offset -= 12
    c.drawString(notes_x, y_offset, "• Rubber Feet: 4x (8mm diameter)")
    
    # Legend
    legend_y = margin + 80
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, legend_y, "LEGEND:")
    c.setFont("Helvetica", 8)
    legend_y -= 15
    
    c.setStrokeColor(pdf_colors.black)
    c.setLineWidth(1.5)
    c.line(margin, legend_y, margin + 20, legend_y)
    c.drawString(margin + 25, legend_y - 3, "External Profile")
    
    legend_y -= 12
    c.setStrokeColor(pdf_colors.blue)
    c.setLineWidth(1.0)
    c.line(margin, legend_y, margin + 20, legend_y)
    c.drawString(margin + 25, legend_y - 3, "Internal Cavity")
    
    legend_y -= 12
    c.setStrokeColor(pdf_colors.green)
    c.circle(margin + 10, legend_y, 3, stroke=1, fill=0)
    c.drawString(margin + 25, legend_y - 3, "Standoff Pillars")
    
    legend_y -= 12
    c.setStrokeColor(pdf_colors.orange)
    c.circle(margin + 10, legend_y, 2, stroke=1, fill=0)
    c.drawString(margin + 25, legend_y - 3, "Standoff Holes (M2)")
    
    legend_y -= 12
    c.setStrokeColor(pdf_colors.purple)
    c.circle(margin + 10, legend_y, 2.5, stroke=1, fill=0)
    c.drawString(margin + 25, legend_y - 3, "Assembly Screws (M3)")
    
    legend_y -= 12
    c.setStrokeColor(pdf_colors.brown)
    c.circle(margin + 10, legend_y, 4, stroke=1, fill=0)
    c.drawString(margin + 25, legend_y - 3, "Rubber Feet Recesses")
    
    # Save PDF
    c.save()
    print(f"✓ Exported bottom tray PDF: {output_path}")



def export_assembly_drawing_pdf(top_frame_profile: Dict[str, Any], 
                                bottom_tray_profile: Dict[str, Any],
                                output_path: str,
                                case_length: float, case_width: float,
                                top_frame_height: float, bottom_tray_height: float,
                                mounting_holes: Dict[str, Point2D]):
    """
    Export assembly drawing with exploded view and hardware callouts.
    
    Args:
        top_frame_profile: Top frame profile geometry
        bottom_tray_profile: Bottom tray profile geometry
        output_path: Output file path for PDF
        case_length: Case length (295mm)
        case_width: Case width (105mm)
        top_frame_height: Top frame height (5mm)
        bottom_tray_height: Bottom tray height (15mm)
        mounting_holes: Dictionary of mounting hole positions
        
    Requirements: 8.1, 8.4
    """
    # Create PDF canvas (A3 landscape)
    page_width, page_height = landscape(A3)
    c = canvas.Canvas(output_path, pagesize=landscape(A3))
    
    # Scale factor to fit drawing on page
    margin = 50 * mm
    available_width = page_width - 2 * margin - 200 * mm
    available_height = page_height - 2 * margin - 120 * mm
    
    scale_x = available_width / case_length
    scale_y = available_height / (case_width * 2.5)  # Space for exploded view
    scale = min(scale_x, scale_y)
    
    # Drawing origins for exploded view
    origin_x = margin
    top_frame_y = page_height - margin - 100 * mm
    bottom_tray_y = top_frame_y - (case_width * scale) - 30 * mm
    
    def transform_point_top(p: Point2D) -> Tuple[float, float]:
        """Transform model coordinates to PDF coordinates for top frame."""
        return (origin_x + p[0] * scale, top_frame_y - p[1] * scale)
    
    def transform_point_bottom(p: Point2D) -> Tuple[float, float]:
        """Transform model coordinates to PDF coordinates for bottom tray."""
        return (origin_x + p[0] * scale, bottom_tray_y - p[1] * scale)
    
    # Title block
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, page_height - margin, "60% KEYBOARD CASE - ASSEMBLY DRAWING")
    c.setFont("Helvetica", 10)
    c.drawString(margin, page_height - margin - 20, "Exploded View with Hardware Callouts")
    
    # Draw TOP FRAME
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, top_frame_y + 15, "TOP FRAME")
    
    # External profile
    c.setStrokeColor(pdf_colors.black)
    c.setLineWidth(1.5)
    points = [transform_point_top(p) for p in top_frame_profile['external_profile']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # PCB opening
    c.setStrokeColor(pdf_colors.blue)
    c.setLineWidth(0.8)
    points = [transform_point_top(p) for p in top_frame_profile['pcb_opening']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # USB cutout
    c.setStrokeColor(pdf_colors.green)
    points = [transform_point_top(p) for p in top_frame_profile['usb_cutout']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # Brass insert holes
    c.setStrokeColor(pdf_colors.red)
    for hole_profile in top_frame_profile['brass_insert_holes'].values():
        if hole_profile:
            xs = [p[0] for p in hole_profile]
            ys = [p[1] for p in hole_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            center_pdf = transform_point_top(center)
            c.circle(center_pdf[0], center_pdf[1], 5.8 / 2.0 * scale, stroke=1, fill=0)
    
    # Draw BOTTOM TRAY
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, bottom_tray_y + 15, "BOTTOM TRAY")
    
    # External profile
    c.setStrokeColor(pdf_colors.black)
    c.setLineWidth(1.5)
    points = [transform_point_bottom(p) for p in bottom_tray_profile['external_profile']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # Internal cavity
    c.setStrokeColor(pdf_colors.blue)
    c.setLineWidth(0.8)
    points = [transform_point_bottom(p) for p in bottom_tray_profile['internal_cavity']]
    if points:
        path = c.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            path.lineTo(p[0], p[1])
        c.drawPath(path, stroke=1, fill=0)
    
    # Standoff pillars
    c.setStrokeColor(pdf_colors.green)
    for pillar_profile in bottom_tray_profile['standoff_pillars'].values():
        if pillar_profile:
            xs = [p[0] for p in pillar_profile]
            ys = [p[1] for p in pillar_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            center_pdf = transform_point_bottom(center)
            c.circle(center_pdf[0], center_pdf[1], 6.0 / 2.0 * scale, stroke=1, fill=0)
    
    # Rubber feet recesses
    c.setStrokeColor(pdf_colors.brown)
    for recess_profile in bottom_tray_profile['rubber_feet_recesses']:
        if recess_profile:
            xs = [p[0] for p in recess_profile]
            ys = [p[1] for p in recess_profile]
            center = (sum(xs) / len(xs), sum(ys) / len(ys))
            center_pdf = transform_point_bottom(center)
            c.circle(center_pdf[0], center_pdf[1], 10.0 / 2.0 * scale, stroke=1, fill=0)
    
    # Hardware callouts and assembly notes
    notes_x = page_width - margin - 180 * mm
    notes_y = page_height - margin - 100 * mm
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(notes_x, notes_y, "HARDWARE REQUIRED")
    c.setFont("Helvetica", 9)
    y_offset = notes_y - 20
    
    # Brass inserts
    c.setFont("Helvetica-Bold", 9)
    c.drawString(notes_x, y_offset, "Brass Inserts (6x)")
    c.setFont("Helvetica", 8)
    y_offset -= 12
    c.drawString(notes_x + 5, y_offset, "• Type: M3 threaded")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "• Size: 5.7mm OD × 4mm length")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "• Location: Top frame (press-fit)")
    
    y_offset -= 18
    c.setFont("Helvetica-Bold", 9)
    c.drawString(notes_x, y_offset, "M2 Screws (6x)")
    c.setFont("Helvetica", 8)
    y_offset -= 12
    c.drawString(notes_x + 5, y_offset, "• Type: M2 × 8mm pan head")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "• Purpose: PCB mounting")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "• Torque: Hand-tight (0.2 Nm)")
    
    y_offset -= 18
    c.setFont("Helvetica-Bold", 9)
    c.drawString(notes_x, y_offset, "M3 Screws (6x)")
    c.setFont("Helvetica", 8)
    y_offset -= 12
    c.drawString(notes_x + 5, y_offset, "• Type: M3 × 12mm flat head")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "• Purpose: Case assembly")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "• Torque: Hand-tight (0.5 Nm)")
    
    y_offset -= 18
    c.setFont("Helvetica-Bold", 9)
    c.drawString(notes_x, y_offset, "Rubber Feet (4x)")
    c.setFont("Helvetica", 8)
    y_offset -= 12
    c.drawString(notes_x + 5, y_offset, "• Type: Adhesive rubber bumpers")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "• Size: 8mm diameter × 2mm height")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "• Location: Bottom corners")
    
    # Assembly sequence
    y_offset -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(notes_x, y_offset, "ASSEMBLY SEQUENCE")
    c.setFont("Helvetica", 9)
    y_offset -= 18
    
    c.drawString(notes_x, y_offset, "1. Install brass inserts")
    c.setFont("Helvetica", 8)
    y_offset -= 12
    c.drawString(notes_x + 5, y_offset, "Press brass inserts into top frame")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "using arbor press or soldering iron")
    
    y_offset -= 15
    c.setFont("Helvetica", 9)
    c.drawString(notes_x, y_offset, "2. Mount PCB to bottom tray")
    c.setFont("Helvetica", 8)
    y_offset -= 12
    c.drawString(notes_x + 5, y_offset, "Align PCB with standoff pillars")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "Secure with 6× M2 screws")
    
    y_offset -= 15
    c.setFont("Helvetica", 9)
    c.drawString(notes_x, y_offset, "3. Attach top frame")
    c.setFont("Helvetica", 8)
    y_offset -= 12
    c.drawString(notes_x + 5, y_offset, "Align USB cutout with connector")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "Secure with 6× M3 screws from bottom")
    
    y_offset -= 15
    c.setFont("Helvetica", 9)
    c.drawString(notes_x, y_offset, "4. Install rubber feet")
    c.setFont("Helvetica", 8)
    y_offset -= 12
    c.drawString(notes_x + 5, y_offset, "Clean recesses with alcohol")
    y_offset -= 10
    c.drawString(notes_x + 5, y_offset, "Press rubber feet into corner recesses")
    
    # Notes
    y_offset -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(notes_x, y_offset, "NOTES:")
    c.setFont("Helvetica", 8)
    y_offset -= 12
    c.drawString(notes_x, y_offset, "• Apply wood finish before assembly")
    y_offset -= 10
    c.drawString(notes_x, y_offset, "• Do not overtighten screws")
    y_offset -= 10
    c.drawString(notes_x, y_offset, "• Ensure USB connector aligns properly")
    y_offset -= 10
    c.drawString(notes_x, y_offset, "• Case can be disassembled for maintenance")
    
    # Save PDF
    c.save()
    print(f"✓ Exported assembly drawing PDF: {output_path}")
