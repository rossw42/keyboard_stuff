"""
DXF export functionality for CNC toolpaths.

This module exports toolpath data to DXF format for use with CAM software.
Each operation is exported as a separate DXF file with tool specifications
included in the filename and metadata.

Requirements: 6.1, 8.2
"""

import ezdxf
from typing import Dict, Any, List, Tuple
from pathlib import Path


def export_toolpath_to_dxf(
    toolpath_data: Dict[str, Any],
    output_path: str,
    component_name: str,
    operation_name: str
) -> str:
    """
    Export a single toolpath operation to DXF format.
    
    Args:
        toolpath_data: Toolpath data dictionary from toolpath generation
        output_path: Base output directory path
        component_name: Component name (e.g., 'top_frame', 'bottom_tray')
        operation_name: Operation name (e.g., 'face_surfacing', 'pcb_opening_pocket')
        
    Returns:
        Path to the exported DXF file
        
    Notes:
        - Filename includes tool specifications
        - DXF layers separate different toolpath elements
        - Metadata included in DXF header
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract tool information - handle roughing/finishing operations
    tool_info = toolpath_data.get('tool', {})
    if not tool_info and 'roughing' in toolpath_data:
        # Use roughing tool info for filename
        tool_info = toolpath_data['roughing'].get('tool', {})
    
    tool_diameter = tool_info.get('diameter', 0)
    tool_type = tool_info.get('type', 'unknown')
    
    # Create filename with tool specifications
    filename = f"{component_name}_{operation_name}_{tool_diameter}mm_{tool_type}.dxf"
    filepath = output_dir / filename
    
    # Create new DXF document
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Add metadata to DXF header
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Create layers for different elements
    doc.layers.new('TOOLPATH', dxfattribs={'color': 1})  # Red
    doc.layers.new('REFERENCE', dxfattribs={'color': 7})  # White/Black
    doc.layers.new('DIMENSIONS', dxfattribs={'color': 3})  # Green
    
    # Export toolpath geometry based on operation type
    operation = toolpath_data.get('operation', '')
    
    if 'toolpath' in toolpath_data:
        # Simple toolpath (list of passes)
        _export_simple_toolpath(msp, toolpath_data['toolpath'])
    elif 'toolpaths' in toolpath_data:
        # Multiple toolpaths (e.g., counterbores, rubber feet)
        _export_multiple_toolpaths(msp, toolpath_data['toolpaths'])
    elif 'roughing' in toolpath_data and 'finishing' in toolpath_data:
        # Roughing and finishing operations
        _export_roughing_finishing_toolpaths(msp, toolpath_data)
    
    # Add text annotation with tool and operation info
    _add_annotation(msp, toolpath_data, component_name, operation_name)
    
    # Save DXF file
    doc.saveas(filepath)
    
    return str(filepath)


def _export_simple_toolpath(msp, toolpath_passes: List[List[Tuple[float, float]]]):
    """Export simple toolpath passes as polylines."""
    for pass_points in toolpath_passes:
        if len(pass_points) >= 2:
            # Create polyline for each pass
            points_2d = [(p[0], p[1]) if len(p) > 2 else p for p in pass_points]
            msp.add_lwpolyline(points_2d, dxfattribs={'layer': 'TOOLPATH'})


def _export_multiple_toolpaths(msp, toolpaths):
    """Export multiple toolpaths (dict or list format)."""
    if isinstance(toolpaths, dict):
        # Dictionary format (e.g., {'TL': {...}, 'TR': {...}})
        for hole_id, toolpath_info in toolpaths.items():
            if 'passes' in toolpath_info:
                # 3D helical passes
                for pass_points in toolpath_info['passes']:
                    if len(pass_points) >= 2:
                        # Project to 2D for DXF
                        points_2d = [(p[0], p[1]) for p in pass_points]
                        msp.add_lwpolyline(points_2d, dxfattribs={'layer': 'TOOLPATH'})
            elif 'center' in toolpath_info:
                # Mark center point
                center = toolpath_info['center']
                msp.add_circle(center, radius=0.5, dxfattribs={'layer': 'REFERENCE'})
    elif isinstance(toolpaths, list):
        # List format
        for toolpath_info in toolpaths:
            if 'passes' in toolpath_info:
                for pass_points in toolpath_info['passes']:
                    if len(pass_points) >= 2:
                        points_2d = [(p[0], p[1]) for p in pass_points]
                        msp.add_lwpolyline(points_2d, dxfattribs={'layer': 'TOOLPATH'})


def _export_roughing_finishing_toolpaths(msp, toolpath_data: Dict[str, Any]):
    """Export roughing and finishing toolpaths with different layers."""
    # Create additional layers
    doc = msp.doc
    doc.layers.new('ROUGHING', dxfattribs={'color': 2})  # Yellow
    doc.layers.new('FINISHING', dxfattribs={'color': 5})  # Blue
    
    # Export roughing toolpath
    if 'roughing' in toolpath_data:
        roughing = toolpath_data['roughing']
        if 'toolpath' in roughing:
            for pass_points in roughing['toolpath']:
                if len(pass_points) >= 2:
                    points_2d = [(p[0], p[1]) if len(p) > 2 else p for p in pass_points]
                    msp.add_lwpolyline(points_2d, dxfattribs={'layer': 'ROUGHING'})
    
    # Export finishing toolpath
    if 'finishing' in toolpath_data:
        finishing = toolpath_data['finishing']
        if 'toolpath' in finishing:
            for pass_points in finishing['toolpath']:
                if len(pass_points) >= 2:
                    points_2d = [(p[0], p[1]) if len(p) > 2 else p for p in pass_points]
                    msp.add_lwpolyline(points_2d, dxfattribs={'layer': 'FINISHING'})


def _add_annotation(
    msp,
    toolpath_data: Dict[str, Any],
    component_name: str,
    operation_name: str
):
    """Add text annotation with tool and operation information."""
    tool_info = toolpath_data.get('tool', {})
    params = toolpath_data.get('parameters', {})
    
    # Build annotation text
    lines = [
        f"Component: {component_name}",
        f"Operation: {operation_name}",
        f"Tool: {tool_info.get('diameter', 'N/A')}mm {tool_info.get('type', 'N/A')}",
        f"Feed Rate: {params.get('feed_rate', 'N/A')} mm/min",
        f"Spindle Speed: {params.get('spindle_speed', 'N/A')} RPM",
    ]
    
    if 'depth' in params:
        lines.append(f"Depth: {params['depth']}mm")
    
    # Add text at top-left corner with offset
    y_offset = 0
    for line in lines:
        msp.add_text(
            line,
            dxfattribs={
                'layer': 'DIMENSIONS',
                'height': 3.0,
                'insert': (-20, -10 - y_offset)
            }
        )
        y_offset += 5


def export_top_frame_toolpaths_to_dxf(
    toolpaths: Dict[str, Any],
    output_path: str = "output/60_percent_standard/cnc/toolpaths/top_frame"
) -> Dict[str, str]:
    """
    Export all top frame toolpath operations to separate DXF files.
    
    Args:
        toolpaths: Complete top frame toolpaths dictionary
        output_path: Base output directory path
        
    Returns:
        Dictionary mapping operation names to exported file paths
        
    Requirements: 6.1, 8.2
    """
    exported_files = {}
    
    operations = toolpaths.get('operations', {})
    
    for operation_key, operation_data in operations.items():
        # Extract operation name (remove numbering prefix)
        operation_name = operation_key.split('_', 1)[1] if '_' in operation_key else operation_key
        
        # Export operation to DXF
        filepath = export_toolpath_to_dxf(
            toolpath_data=operation_data,
            output_path=output_path,
            component_name='top_frame',
            operation_name=operation_name
        )
        
        exported_files[operation_key] = filepath
    
    return exported_files


def export_bottom_tray_toolpaths_to_dxf(
    toolpaths: Dict[str, Any],
    output_path: str = "output/60_percent_standard/cnc/toolpaths/bottom_tray"
) -> Dict[str, str]:
    """
    Export all bottom tray toolpath operations to separate DXF files.
    
    Args:
        toolpaths: Complete bottom tray toolpaths dictionary
        output_path: Base output directory path
        
    Returns:
        Dictionary mapping operation names to exported file paths
        
    Requirements: 6.1, 8.2
    """
    exported_files = {}
    
    operations = toolpaths.get('operations', {})
    
    for operation_key, operation_data in operations.items():
        # Extract operation name (remove numbering prefix)
        operation_name = operation_key.split('_', 1)[1] if '_' in operation_key else operation_key
        
        # Export operation to DXF
        filepath = export_toolpath_to_dxf(
            toolpath_data=operation_data,
            output_path=output_path,
            component_name='bottom_tray',
            operation_name=operation_name
        )
        
        exported_files[operation_key] = filepath
    
    return exported_files
