"""File export utilities for STEP and STL formats."""

import logging
from pathlib import Path

import cadquery as cq

logger = logging.getLogger(__name__)


class ExportError(Exception):
    """Error exporting files."""
    pass


def export_step(part: cq.Workplane, filepath: Path) -> None:
    """
    Export part to STEP format.
    
    Args:
        part: CadQuery workplane to export
        filepath: Output file path
        
    Raises:
        ExportError: If export fails
    """
    try:
        logger.info(f"Exporting STEP: {filepath}")
        
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Export
        cq.exporters.export(part, str(filepath))
        
        logger.info(f"  ✓ Exported STEP: {filepath.name}")
        
    except Exception as e:
        raise ExportError(f"Failed to export STEP file '{filepath}': {e}") from e


def export_stl(part: cq.Workplane, filepath: Path, tolerance: float = 0.001) -> None:
    """
    Export part to STL format.
    
    Args:
        part: CadQuery workplane to export
        filepath: Output file path
        tolerance: Mesh tolerance in mm
        
    Raises:
        ExportError: If export fails
    """
    try:
        logger.info(f"Exporting STL: {filepath}")
        
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Export
        cq.exporters.export(part, str(filepath), tolerance=tolerance)
        
        logger.info(f"  ✓ Exported STL: {filepath.name}")
        
    except Exception as e:
        raise ExportError(f"Failed to export STL file '{filepath}': {e}") from e


def generate_filename(
    base_name: str,
    component: str,
    side: str = None,
    extension: str = "step"
) -> str:
    """
    Generate descriptive filename.
    
    Args:
        base_name: Base name from input PCB file
        component: Component type ('bottom_tray' or 'switch_plate')
        side: Side ('left', 'right', or None)
        extension: File extension ('step' or 'stl')
        
    Returns:
        Generated filename
    """
    parts = [base_name, component]
    
    if side:
        parts.append(side)
    
    filename = "_".join(parts) + f".{extension}"
    return filename
