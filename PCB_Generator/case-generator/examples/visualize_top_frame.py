#!/usr/bin/env python3
"""
Simple ASCII visualization of top frame profile geometry.

This creates a basic text-based visualization to help understand
the spatial relationships between features.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from constants import *
from geometry import generate_top_frame_profile


def create_ascii_visualization(profile, width=80, height=30):
    """Create a simple ASCII art visualization of the top frame."""
    
    # Create empty grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Scale factors
    scale_x = width / CASE_LENGTH
    scale_y = height / CASE_WIDTH
    
    def plot_point(x, y, char='*'):
        """Plot a point on the grid."""
        grid_x = int(x * scale_x)
        grid_y = int(y * scale_y)
        if 0 <= grid_x < width and 0 <= grid_y < height:
            grid[grid_y][grid_x] = char
    
    def plot_profile(points, char='#'):
        """Plot a profile path."""
        for x, y in points:
            plot_point(x, y, char)
    
    # Plot external profile
    plot_profile(profile['external_profile'], '#')
    
    # Plot PCB opening
    plot_profile(profile['pcb_opening'], 'P')
    
    # Plot USB cutout
    plot_profile(profile['usb_cutout'], 'U')
    
    # Plot brass insert holes
    for hole_id, hole_profile in profile['brass_insert_holes'].items():
        plot_profile(hole_profile, 'B')
    
    return grid


def print_visualization(grid):
    """Print the ASCII visualization."""
    print("\n" + "=" * len(grid[0]))
    print("Top Frame Profile Visualization")
    print("=" * len(grid[0]))
    print("\nLegend:")
    print("  # = External profile")
    print("  P = PCB opening")
    print("  U = USB cutout")
    print("  B = Brass insert holes")
    print("\n" + "-" * len(grid[0]))
    
    for row in grid:
        print(''.join(row))
    
    print("-" * len(grid[0]))
    print(f"\nScale: {CASE_LENGTH}mm × {CASE_WIDTH}mm")
    print()


def main():
    """Generate and visualize top frame profile."""
    
    # Generate profile
    profile = generate_top_frame_profile(
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
    
    # Create and display visualization
    grid = create_ascii_visualization(profile, width=90, height=32)
    print_visualization(grid)
    
    # Print feature locations
    print("Feature Coordinates:")
    print("-" * 60)
    print(f"Case: (0, 0) to ({CASE_LENGTH}, {CASE_WIDTH})")
    print(f"PCB Opening: ({PCB_BORDER}, {PCB_BORDER}) to ({PCB_BORDER + PCB_OPENING_LENGTH}, {PCB_BORDER + PCB_OPENING_WIDTH})")
    print(f"USB Cutout: Center at ({USB_CUTOUT_CENTER_X}, {USB_CUTOUT_CENTER_Y})")
    print("\nBrass Insert Holes:")
    for hole_id, (x, y) in MOUNTING_HOLES.items():
        print(f"  {hole_id}: ({x:.1f}, {y:.1f})")
    print()


if __name__ == '__main__':
    main()
