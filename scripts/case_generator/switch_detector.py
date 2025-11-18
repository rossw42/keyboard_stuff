"""Switch position detection from KiCad PCB files."""

import logging
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional

from .pcb_analyzer import PCBInfo

logger = logging.getLogger(__name__)


@dataclass
class SwitchInfo:
    """Information about a switch position."""
    position: Tuple[float, float]  # (x, y) in mm
    rotation: float  # degrees
    footprint_type: str  # 'MX', 'Choc', 'Hotswap'


@dataclass
class SwitchLayout:
    """Complete switch layout information."""
    switches: List[SwitchInfo]
    side: str  # 'left', 'right', or 'both'


def parse_kicad_pcb(pcb_file: Path) -> List[SwitchInfo]:
    """
    Parse .kicad_pcb file and extract switch positions.
    
    Args:
        pcb_file: Path to .kicad_pcb file
        
    Returns:
        List of SwitchInfo objects
    """
    try:
        logger.info(f"Parsing KiCad PCB file: {pcb_file}")
        
        with open(pcb_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        switches = []
        
        # Look for footprint/module entries
        # KiCad 6+: (footprint "library:footprint_name" (at x y rotation) ...)
        # KiCad 5: (module library:footprint_name (layer F.Cu) ... (at x y rotation) ...)
        
        # Try new format first
        footprint_pattern = r'\(footprint\s+"([^"]+)"\s+.*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)'
        matches = list(re.finditer(footprint_pattern, content, re.DOTALL))
        
        # If no matches, try old format
        if not matches:
            footprint_pattern = r'\(module\s+([^\s]+)\s+.*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)'
            matches = list(re.finditer(footprint_pattern, content, re.DOTALL))
        
        for match in matches:
            footprint_name = match.group(1)
            x = float(match.group(2))
            y = float(match.group(3))
            rotation = float(match.group(4)) if match.group(4) else 0.0
            
            # Identify switch footprints
            footprint_lower = footprint_name.lower()
            footprint_type = None
            
            if any(name in footprint_lower for name in ['mx', 'cherry', 'gateron', 'kailh_socket_mx', 'sw_mx']):
                footprint_type = 'MX'
            elif any(name in footprint_lower for name in ['choc', 'pg1350', 'kailh_socket_pg1350', 'sw_pg1350']):
                footprint_type = 'Choc'
            elif 'hotswap' in footprint_lower or 'socket' in footprint_lower:
                footprint_type = 'Hotswap'
            
            if footprint_type:
                switches.append(SwitchInfo(
                    position=(x, y),
                    rotation=rotation,
                    footprint_type=footprint_type
                ))
                logger.debug(f"  Found {footprint_type} switch at ({x:.2f}, {y:.2f}), "
                           f"rotation: {rotation:.1f}°")
        
        logger.info(f"  Found {len(switches)} switches")
        return switches
        
    except Exception as e:
        logger.warning(f"Failed to parse KiCad PCB file: {e}")
        return []


def filter_switches_by_side(
    switches: List[SwitchInfo],
    pcb_center_x: float
) -> Tuple[List[SwitchInfo], List[SwitchInfo]]:
    """
    Split switches into left and right based on X position.
    
    Args:
        switches: List of all switches
        pcb_center_x: X coordinate of PCB center
        
    Returns:
        Tuple of (left_switches, right_switches)
    """
    left_switches = []
    right_switches = []
    
    for switch in switches:
        if switch.position[0] < pcb_center_x:
            left_switches.append(switch)
        else:
            right_switches.append(switch)
    
    logger.info(f"Split switches: {len(left_switches)} left, {len(right_switches)} right")
    return left_switches, right_switches


def detect_switch_layout(
    kicad_pcb: Optional[Path],
    pcb_info: PCBInfo,
    side: str = "both",
    is_unified: bool = False
) -> Optional[SwitchLayout]:
    """
    Complete switch detection pipeline.
    
    Args:
        kicad_pcb: Path to .kicad_pcb file (optional)
        pcb_info: PCB information for determining sides
        side: Which side to detect ('left', 'right', or 'both')
        is_unified: If True, mirror switches for unified keyboard
        
    Returns:
        SwitchLayout or None if no .kicad_pcb file provided
    """
    if not kicad_pcb:
        logger.info("No KiCad PCB file provided, skipping switch detection")
        return None
    
    # Parse switches
    all_switches = parse_kicad_pcb(kicad_pcb)
    
    if not all_switches:
        logger.warning("No switches found in KiCad PCB file")
        return None
    
    # Filter switches to only those within this PCB's X bounds
    # and transform Y coordinates to match STEP export
    xmin, ymin, xmax, ymax = pcb_info.bounding_box
    filtered_switches = []
    
    # Detect Y coordinate transformation needed
    # KiCad typically has Y increasing upward, STEP export may invert it
    # We'll detect this by comparing the Y range
    if all_switches:
        kicad_y_coords = [s.position[1] for s in all_switches]
        kicad_y_min = min(kicad_y_coords)
        kicad_y_max = max(kicad_y_coords)
        kicad_y_center = (kicad_y_min + kicad_y_max) / 2
        step_y_center = (ymin + ymax) / 2
        
        # Check if Y axis needs to be inverted
        # If KiCad Y is positive and STEP Y is negative (or vice versa), we need to invert
        y_needs_inversion = (kicad_y_center > 0 and step_y_center < 0) or (kicad_y_center < 0 and step_y_center > 0)
        
        if y_needs_inversion:
            # Calculate the inversion: new_y = -old_y + offset
            # The offset is chosen so the center aligns
            y_offset = step_y_center + kicad_y_center
            logger.info(f"Inverting Y coordinates: new_y = -old_y + {y_offset:.2f}")
        else:
            # Just offset to align centers
            y_offset = step_y_center - kicad_y_center
            logger.info(f"Offsetting Y coordinates by {y_offset:.2f}")
    
    # Normal filtering for split keyboards (or first half of unified)
    for switch in all_switches:
        sx, sy = switch.position
        
        # Check if switch X is within this PCB's X bounds (with margin)
        margin = 5.0  # mm
        if xmin - margin <= sx <= xmax + margin:
            # Transform Y coordinate to match STEP export
            if y_needs_inversion:
                transformed_y = -sy + y_offset
            else:
                transformed_y = sy + y_offset
            
            # Create new switch with transformed coordinates
            transformed_switch = SwitchInfo(
                position=(sx, transformed_y),
                rotation=switch.rotation,
                footprint_type=switch.footprint_type
            )
            filtered_switches.append(transformed_switch)
    
    logger.info(f"Filtered to {len(filtered_switches)} switches within PCB X bounds")
    
    # For unified keyboards, mirror the switches to create both halves
    if is_unified and filtered_switches:
        logger.info(f"Unified keyboard: mirroring {len(filtered_switches)} switches")
        
        # Find the center of the unified PCB
        pcb_center_x = (xmin + xmax) / 2
        logger.info(f"  PCB center X: {pcb_center_x:.2f}")
        
        # Mirror switches across the center
        mirrored_switches = []
        for switch in filtered_switches:
            sx, sy = switch.position
            # Mirror X coordinate across center
            mirrored_x = 2 * pcb_center_x - sx
            mirrored_switches.append(SwitchInfo(
                position=(mirrored_x, sy),
                rotation=switch.rotation,
                footprint_type=switch.footprint_type
            ))
        
        # Combine original and mirrored
        filtered_switches = filtered_switches + mirrored_switches
        logger.info(f"  Total switches after mirroring: {len(filtered_switches)}")
    
    return SwitchLayout(
        switches=filtered_switches,
        side=side
    )
