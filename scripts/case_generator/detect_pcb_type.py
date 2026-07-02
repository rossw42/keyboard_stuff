#!/usr/bin/env python3
"""
Detect if a PCB is a single half or both halves combined.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from case_generator.switch_detector import parse_kicad_pcb


def detect_pcb_type(kicad_pcb_file: Path):
    """
    Detect if PCB contains one half or both halves.
    
    Returns:
        'single_half' - PCB is already one half
        'both_halves' - PCB contains both halves (needs splitting)
        'unknown' - Cannot determine
    """
    if not kicad_pcb_file or not kicad_pcb_file.exists():
        return 'unknown'
    
    try:
        switches = parse_kicad_pcb(kicad_pcb_file)
        
        if len(switches) == 0:
            return 'unknown'
        
        # Get X positions of all switches
        x_positions = [s.position[0] for s in switches]
        x_min = min(x_positions)
        x_max = max(x_positions)
        x_range = x_max - x_min
        x_center = (x_min + x_max) / 2
        
        # Count switches on left and right of center
        left_switches = [s for s in switches if s.position[0] < x_center]
        right_switches = [s for s in switches if s.position[0] >= x_center]
        
        # If switches are roughly evenly distributed on both sides, it's both halves
        # If most switches are on one side, it's a single half
        left_count = len(left_switches)
        right_count = len(right_switches)
        total = len(switches)
        
        # Calculate balance ratio (0.5 = perfectly balanced)
        balance = min(left_count, right_count) / total
        
        print(f"Switch distribution:")
        print(f"  Total switches: {total}")
        print(f"  Left of center: {left_count}")
        print(f"  Right of center: {right_count}")
        print(f"  Balance ratio: {balance:.2f}")
        print(f"  X range: {x_range:.2f}mm")
        
        # Additional check: look at X range
        # Split keyboards designed as two halves typically have larger X range
        # Single unified keyboards are more compact
        avg_x_per_switch = x_range / total
        
        print(f"  Avg X span per switch: {avg_x_per_switch:.2f}mm")
        
        # If balance is > 0.4 AND X range suggests two separate halves, it's both halves
        # Heuristic: if avg X per switch > 5mm, likely two halves with gap
        if balance > 0.4 and avg_x_per_switch > 5.0:
            print(f"  → Detected: BOTH HALVES (needs splitting)")
            return 'both_halves'
        elif balance < 0.25:
            print(f"  → Detected: SINGLE HALF (no split needed)")
            return 'single_half'
        else:
            # For unclear cases, assume single unified keyboard
            print(f"  → Detected: SINGLE UNIFIED KEYBOARD (no split needed)")
            return 'single_half'
            
    except Exception as e:
        print(f"Error analyzing PCB: {e}")
        return 'unknown'


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_pcb_type.py <kicad_pcb_file>")
        sys.exit(1)
    
    kicad_file = Path(sys.argv[1])
    pcb_type = detect_pcb_type(kicad_file)
    print(f"\nResult: {pcb_type}")
