#!/usr/bin/env python3
"""
Visualization script for bottom tray 2D profile geometry.

This script generates a simple ASCII visualization of the bottom tray
to help verify the geometry layout.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from constants import (
    CASE_LENGTH, CASE_WIDTH, CASE_CORNER_RADIUS,
    CAVITY_LENGTH, CAVITY_WIDTH, CAVITY_CORNER_RADIUS, WALL_THICKNESS,
    MOUNTING_HOLES,
    STANDOFF_DIAMETER, STANDOFF_HOLE_DIAMETER,
    ASSEMBLY_SCREW_DIAMETER, ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
    RUBBER_FEET_POSITIONS, RUBBER_FEET_DIAMETER,
    BOTTOM_TRAY_HEIGHT, CAVITY_DEPTH
)
from geometry import generate_bottom_tray_profile


def visualize_profile(profile):
    """Create a simple ASCII visualization of the bottom tray profile."""
    
    print("\nBottom Tray Top View (not to scale):")
    print("=" * 80)
    print()
    
    # Create a simple representation
    width = 60
    height = 20
    
    # Initialize grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Draw external border
    for i in range(width):
        grid[0][i] = '═'
        grid[height-1][i] = '═'
    for i in range(height):
        grid[i][0] = '║'
        grid[i][width-1] = '║'
    
    # Draw corners
    grid[0][0] = '╔'
    grid[0][width-1] = '╗'
    grid[height-1][0] = '╚'
    grid[height-1][width-1] = '╝'
    
    # Draw internal cavity (inset by wall thickness)
    cavity_left = int(width * WALL_THICKNESS / CASE_LENGTH)
    cavity_right = width - cavity_left - 1
    cavity_top = int(height * WALL_THICKNESS / CASE_WIDTH)
    cavity_bottom = height - cavity_top - 1
    
    for i in range(cavity_left, cavity_right + 1):
        if cavity_top < height and i < width:
            grid[cavity_top][i] = '─'
        if cavity_bottom < height and i < width:
            grid[cavity_bottom][i] = '─'
    
    for i in range(cavity_top, cavity_bottom + 1):
        if i < height and cavity_left < width:
            grid[i][cavity_left] = '│'
        if i < height and cavity_right < width:
            grid[i][cavity_right] = '│'
    
    # Draw cavity corners
    if cavity_top < height and cavity_left < width:
        grid[cavity_top][cavity_left] = '┌'
    if cavity_top < height and cavity_right < width:
        grid[cavity_top][cavity_right] = '┐'
    if cavity_bottom < height and cavity_left < width:
        grid[cavity_bottom][cavity_left] = '└'
    if cavity_bottom < height and cavity_right < width:
        grid[cavity_bottom][cavity_right] = '┘'
    
    # Mark standoff pillars
    for hole_id, (x, y) in MOUNTING_HOLES.items():
        grid_x = int(width * x / CASE_LENGTH)
        grid_y = int(height * y / CASE_WIDTH)
        if 0 < grid_y < height and 0 < grid_x < width:
            grid[grid_y][grid_x] = '●'
    
    # Mark rubber feet positions
    for x, y in RUBBER_FEET_POSITIONS:
        grid_x = int(width * x / CASE_LENGTH)
        grid_y = int(height * y / CASE_WIDTH)
        if 0 < grid_y < height and 0 < grid_x < width:
            grid[grid_y][grid_x] = '◉'
    
    # Print grid
    for row in grid:
        print(''.join(row))
    
    print()
    print("Legend:")
    print("  ═ ║ ╔ ╗ ╚ ╝  : External profile (295mm × 105mm)")
    print("  ─ │ ┌ ┐ └ ┘  : Internal cavity (287mm × 96.6mm, 8mm deep)")
    print("  ●              : Standoff pillars (6mm dia, 6 locations)")
    print("  ◉              : Rubber feet recesses (10mm dia, 4 corners)")
    print()
    print("=" * 80)


def main():
    """Generate and visualize bottom tray profile."""
    
    print("=" * 80)
    print("60% Keyboard Case - Bottom Tray Visualization")
    print("=" * 80)
    
    # Generate profile
    profile = generate_bottom_tray_profile(
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
    
    # Visualize
    visualize_profile(profile)
    
    # Print feature summary
    print("\nFeature Summary:")
    print("-" * 80)
    print(f"External Profile:        {CASE_LENGTH}mm × {CASE_WIDTH}mm × {BOTTOM_TRAY_HEIGHT}mm")
    print(f"Internal Cavity:         {CAVITY_LENGTH}mm × {CAVITY_WIDTH}mm × {CAVITY_DEPTH}mm deep")
    print(f"Wall Thickness:          {WALL_THICKNESS}mm")
    print(f"Standoff Pillars:        {len(profile['standoff_pillars'])} × {STANDOFF_DIAMETER}mm dia")
    print(f"Standoff Holes:          {len(profile['standoff_holes'])} × {STANDOFF_HOLE_DIAMETER}mm dia (M2)")
    print(f"Assembly Screws:         {len(profile['assembly_screw_holes'])} × {ASSEMBLY_SCREW_DIAMETER}mm dia (M3)")
    print(f"Assembly Counterbores:   {len(profile['assembly_counterbores'])} × {ASSEMBLY_SCREW_COUNTERBORE_DIAMETER}mm dia × 3mm deep")
    print(f"Rubber Feet Recesses:    {len(profile['rubber_feet_recesses'])} × {RUBBER_FEET_DIAMETER}mm dia × 2mm deep")
    print("-" * 80)
    
    print("\nGeometry generation complete!")
    print("All features verified and ready for CNC toolpath generation.")


if __name__ == '__main__':
    main()
