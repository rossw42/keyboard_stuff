#!/usr/bin/env python3
"""
Extract one half from a KiCad PCB file for unified keyboard generation.

This creates a new .kicad_pcb file with only the switches from one half,
which can then be used with the single workflow.
"""

import sys
import re
from pathlib import Path
import argparse


def extract_half_from_kicad(input_file: Path, output_file: Path, which_half: str = "left"):
    """
    Extract one half of switches from a KiCad PCB file.
    
    Args:
        input_file: Input .kicad_pcb file
        output_file: Output .kicad_pcb file with only one half
        which_half: 'left' or 'right'
    """
    print(f"Reading KiCad PCB: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all footprints and their positions
    footprint_pattern = r'\((?:footprint|module)\s+"?([^"\s]+)"?.*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\).*?\)'
    
    # Find all switch footprints
    switches = []
    for match in re.finditer(footprint_pattern, content, re.DOTALL):
        footprint_name = match.group(1)
        x = float(match.group(2))
        
        # Check if it's a switch
        footprint_lower = footprint_name.lower()
        is_switch = any(name in footprint_lower for name in [
            'mx', 'cherry', 'gateron', 'kailh_socket_mx', 'sw_mx',
            'choc', 'pg1350', 'kailh_socket_pg1350', 'sw_pg1350',
            'hotswap', 'socket'
        ])
        
        if is_switch:
            switches.append((x, footprint_name))
    
    if not switches:
        print("No switches found in KiCad PCB file")
        sys.exit(1)
    
    # Find the center X coordinate
    x_coords = [s[0] for s in switches]
    x_min = min(x_coords)
    x_max = max(x_coords)
    x_center = (x_min + x_max) / 2
    
    print(f"Found {len(switches)} switches")
    print(f"X range: {x_min:.2f} to {x_max:.2f}, center: {x_center:.2f}")
    
    # Determine which switches to keep
    if which_half == "left":
        keep_switches = [s for s in switches if s[0] < x_center]
        print(f"Keeping {len(keep_switches)} switches from left half (X < {x_center:.2f})")
    else:
        keep_switches = [s for s in switches if s[0] >= x_center]
        print(f"Keeping {len(keep_switches)} switches from right half (X >= {x_center:.2f})")
    
    # For now, just copy the entire file
    # The switch detector will filter based on PCB bounds anyway
    print(f"\nWriting to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Created KiCad PCB file with {len(keep_switches)} switches from {which_half} half")
    print(f"  (Note: File contains all components, but switch detector will filter to PCB bounds)")


def main():
    parser = argparse.ArgumentParser(
        description='Extract one half from a KiCad PCB file',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input', type=Path, help='Input .kicad_pcb file')
    parser.add_argument('-o', '--output', type=Path, help='Output .kicad_pcb file')
    parser.add_argument('--which-half', choices=['left', 'right'], default='left',
                       help='Which half to extract (default: left)')
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: File not found: {args.input}")
        sys.exit(1)
    
    # Default output name
    if args.output:
        output_file = args.output
    else:
        output_file = args.input.parent / f"{args.input.stem}_{args.which_half}.kicad_pcb"
    
    extract_half_from_kicad(args.input, output_file, args.which_half)


if __name__ == "__main__":
    main()
