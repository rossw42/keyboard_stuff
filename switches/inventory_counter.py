#!/usr/bin/env python3
"""
Switch Inventory Counter

Reads switch_inventory_v2.md and prompts for quantities of switches that still have TBD.
- Enter a number to record quantity
- Enter 'S' to skip to next switch
- Enter 'X' to quit and save progress
- Shows tray photos for visual reference
"""

import re
import sys
import os
import json
from pathlib import Path

# Try to import image display libraries
try:
    from PIL import Image
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from scipy.interpolate import griddata
    import numpy as np
    HAS_IMAGE_SUPPORT = True
except ImportError:
    HAS_IMAGE_SUPPORT = False


def read_tray_map(filename):
    """Read the tray map to get switch positions."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the tray map to extract positions
        # Format: | 0,0  | Kailh Box Jade | ...
        switch_positions = {}
        
        for line in content.split('\n'):
            if '|' in line and ',' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    pos = parts[1].strip()
                    switch_name = parts[2].strip()
                    
                    # Parse position like "0,0" or "1,5"
                    if ',' in pos and pos[0].isdigit():
                        try:
                            row, col = pos.split(',')
                            row, col = int(row), int(col)
                            if switch_name and switch_name != '(empty)' and switch_name != '*(empty)*':
                                # Clean up the switch name
                                switch_name = switch_name.split('(')[0].strip()
                                switch_positions[switch_name] = (row, col)
                        except:
                            pass
        
        return switch_positions
    except:
        return {}


def read_inventory(filename):
    """Read the inventory markdown file and parse it."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    header_end = None
    
    # Find where the table starts (after the separator line with |---|)
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and '---' in line:
            header_end = i
            break
    
    if header_end is None:
        print("Error: Could not find table in markdown file")
        sys.exit(1)
    
    # Store everything before and including the header
    header_lines = lines[:header_end + 1]
    
    # Parse the table rows
    switches = []
    table_rows = []
    
    for i, line in enumerate(lines[header_end + 1:], start=header_end + 1):
        if not line.strip() or not line.strip().startswith('|'):
            continue
        
        # Split by | and clean up
        parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last
        
        if len(parts) >= 5:
            manufacturer, switch_name, switch_type, force, quantity = parts[0], parts[1], parts[2], parts[3], parts[4]
            switches.append({
                'manufacturer': manufacturer,
                'name': switch_name,
                'type': switch_type,
                'force': force,
                'quantity': quantity,
                'line_number': i,
                'original_line': line
            })
            table_rows.append(i)
    
    return content, lines, switches, header_lines


def write_inventory(filename, lines):
    """Write the updated inventory back to the file."""
    with open(filename, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))


def load_calibration_data():
    """Load calibration data if available."""
    try:
        with open('tray_calibration.json', 'r') as f:
            data = json.load(f)
        return data.get('images', {})
    except:
        return {}


def interpolate_position(calibration_points, row, col):
    """Use calibration points to interpolate the position of a switch."""
    if not calibration_points:
        return None
    
    # Extract known positions
    rows = [p['row'] for p in calibration_points]
    cols = [p['col'] for p in calibration_points]
    xs = [p['x'] for p in calibration_points]
    ys = [p['y'] for p in calibration_points]
    
    if len(calibration_points) < 3:
        # Not enough points for interpolation
        return None
    
    try:
        # Check if exact match exists
        for p in calibration_points:
            if p['row'] == row and p['col'] == col:
                return (p['x'], p['y'])
        
        # Interpolate using griddata
        points = np.array([[r, c] for r, c in zip(rows, cols)])
        x_interp = griddata(points, xs, [[row, col]], method='linear')[0]
        y_interp = griddata(points, ys, [[row, col]], method='linear')[0]
        
        if not np.isnan(x_interp) and not np.isnan(y_interp):
            return (int(x_interp), int(y_interp))
    except:
        pass
    
    return None


def estimate_position_fallback(img, row, col):
    """Fallback position estimation when no calibration data exists."""
    img_width, img_height = img.size
    
    # Improved estimates based on typical tray layout
    # These are rough estimates - calibration is much better!
    tray_left = int(img_width * 0.08)
    tray_right = int(img_width * 0.92)
    tray_top = int(img_height * 0.15)
    tray_bottom = int(img_height * 0.85)
    
    cols_count = 15
    rows_count = 4
    cell_width = (tray_right - tray_left) / cols_count
    cell_height = (tray_bottom - tray_top) / rows_count
    
    switch_x = tray_left + (col + 0.5) * cell_width
    switch_y = tray_top + (row + 0.5) * cell_height
    
    return int(switch_x), int(switch_y), cell_width, cell_height


def load_tray_images():
    """Load the tray images."""
    if not HAS_IMAGE_SUPPORT:
        return []
    
    # Find the image files
    image_files = ['IMG_3218.JPG', 'IMG_3219.JPG', 'IMG_3220.JPG']
    images = []
    
    for img_file in image_files:
        if os.path.exists(img_file):
            try:
                img = Image.open(img_file)
                images.append((img_file, img))
            except:
                pass
    
    return images


def show_switch_location(images, calibration_data, row, col, switch_name):
    """Display zoomed-in view of specific switch location with precise highlight."""
    if not images:
        return None
    
    # Choose the best image based on row
    if row <= 1:
        img_name, img = images[0] if len(images) > 0 else images[0]
    elif row == 2:
        img_name, img = images[1] if len(images) > 1 else images[0]
    else:
        img_name, img = images[2] if len(images) > 2 else images[0]
    
    img_width, img_height = img.size
    
    # Try to get calibrated position
    switch_x = switch_y = None
    cell_width = cell_height = None
    
    if img_name in calibration_data:
        position = interpolate_position(calibration_data[img_name], row, col)
        if position:
            switch_x, switch_y = position
            # Estimate cell size from calibration data if possible
            points = calibration_data[img_name]
            if len(points) >= 2:
                # Calculate average cell size from adjacent cells
                x_diffs = []
                y_diffs = []
                for i, p1 in enumerate(points):
                    for p2 in points[i+1:]:
                        if p1['row'] == p2['row'] and abs(p1['col'] - p2['col']) == 1:
                            x_diffs.append(abs(p1['x'] - p2['x']))
                        if p1['col'] == p2['col'] and abs(p1['row'] - p2['row']) == 1:
                            y_diffs.append(abs(p1['y'] - p2['y']))
                
                if x_diffs:
                    cell_width = sum(x_diffs) / len(x_diffs)
                if y_diffs:
                    cell_height = sum(y_diffs) / len(y_diffs)
    
    # Fallback to estimation if calibration didn't work
    if switch_x is None or switch_y is None:
        switch_x, switch_y, est_cell_width, est_cell_height = estimate_position_fallback(img, row, col)
        if cell_width is None:
            cell_width = est_cell_width
        if cell_height is None:
            cell_height = est_cell_height
        calibration_status = "⚠ Using estimated position"
    else:
        calibration_status = "✓ Using calibrated position"
    
    # Default cell sizes if still None
    if cell_width is None:
        cell_width = img_width * 0.055
    if cell_height is None:
        cell_height = img_height * 0.15
    
    # Define crop region (zoom into the switch area)
    zoom_factor = 2.5
    crop_width = cell_width * zoom_factor
    crop_height = cell_height * zoom_factor
    
    crop_left = max(0, int(switch_x - crop_width / 2))
    crop_right = min(img_width, int(switch_x + crop_width / 2))
    crop_top = max(0, int(switch_y - crop_height / 2))
    crop_bottom = min(img_height, int(switch_y + crop_height / 2))
    
    # Crop the image
    cropped_img = img.crop((crop_left, crop_top, crop_right, crop_bottom))
    
    # Create figure
    plt.clf()
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(cropped_img)
    
    # Calculate highlight box position in cropped coordinates
    highlight_x = switch_x - crop_left
    highlight_y = switch_y - crop_top
    
    # Draw rectangle around the switch
    rect = patches.Rectangle(
        (highlight_x - cell_width/2, highlight_y - cell_height/2),
        cell_width,
        cell_height,
        linewidth=4,
        edgecolor='red',
        facecolor='none'
    )
    ax.add_patch(rect)
    
    # Add crosshair
    ax.axhline(y=highlight_y, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.axvline(x=highlight_x, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    
    # Add center dot
    ax.plot(highlight_x, highlight_y, 'ro', markersize=10, markeredgewidth=2, 
           markeredgecolor='yellow', markerfacecolor='red')
    
    title = f'{switch_name}\nRow {row}, Column {col} | {os.path.basename(img_name)}\n{calibration_status}'
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    plt.ion()
    plt.draw()
    plt.pause(0.001)
    
    return fig


def match_switch_name(full_name, map_name):
    """Fuzzy match switch names from inventory to tray map."""
    # Remove common words and normalize
    common_words = ['unknown', 'verify', '(', ')', '?']
    
    full_clean = full_name.lower()
    map_clean = map_name.lower()
    
    # Check if key parts match
    if map_clean in full_clean or full_clean in map_clean:
        return True
    
    # Check for manufacturer + model match
    full_parts = full_name.split()
    map_parts = map_name.split()
    
    if len(full_parts) >= 2 and len(map_parts) >= 2:
        # Match last significant word (model name)
        if full_parts[-1].lower() == map_parts[-1].lower():
            return True
    
    return False


def format_table_row(manufacturer, name, switch_type, force, quantity):
    """Format a table row with proper spacing."""
    return f"| {manufacturer:<20} | {name:<27} | {switch_type:<15} | {force:<16} | {quantity:<8} |"


def main():
    filename = 'switch_inventory_v2.md'
    tray_map_file = 'tray_map_v2.md'
    
    try:
        content, lines, switches, header_lines = read_inventory(filename)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        sys.exit(1)
    
    # Load tray map if available
    tray_positions = read_tray_map(tray_map_file) if os.path.exists(tray_map_file) else {}
    
    # Load calibration data
    calibration_data = load_calibration_data()
    
    # Load tray images
    images = load_tray_images() if HAS_IMAGE_SUPPORT else []
    
    # Filter switches that need quantities (TBD)
    switches_to_count = [s for s in switches if s['quantity'].strip().upper() == 'TBD']
    
    if not switches_to_count:
        print("✓ All switches already have quantities recorded!")
        return
    
    print(f"Switch Inventory Counter")
    print(f"========================")
    print(f"Found {len(switches_to_count)} switches that need quantities")
    print()
    
    if HAS_IMAGE_SUPPORT:
        if images:
            print(f"✓ Loaded {len(images)} tray images")
        else:
            print("⚠ Could not load tray images")
        
        if calibration_data:
            total_points = sum(len(points) for points in calibration_data.values())
            print(f"✓ Loaded calibration data ({total_points} calibration points)")
        else:
            print("ℹ No calibration data found (run calibrate_tray.py for precise positioning)")
    else:
        print("⚠ Image support not available")
        print("   Install: pip install pillow matplotlib scipy numpy")
    
    print()
    print("Commands:")
    print("  • Enter a number to record quantity")
    print("  • S = Skip to next switch")
    print("  • X = Exit and save progress")
    print()
    
    fig = None
    
    for i, switch in enumerate(switches_to_count, 1):
        display_name = f"{switch['manufacturer']} - {switch['name']}"
        display_type = f"({switch['type']}, {switch['force']})"
        
        # Try to find tray position and show image
        position_info = ""
        found_position = None
        
        for map_name, pos in tray_positions.items():
            if match_switch_name(switch['name'], map_name):
                position_info = f" [Row {pos[0]}, Col {pos[1]}]"
                found_position = pos
                
                # Show the switch location in the tray
                if HAS_IMAGE_SUPPORT and images:
                    try:
                        if fig is not None:
                            plt.close(fig)
                        fig = show_switch_location(images, calibration_data, pos[0], pos[1], switch['name'])
                    except Exception as e:
                        print(f"⚠ Could not display image: {e}")
                
                break
        
        print(f"\n[{i}/{len(switches_to_count)}] {display_name}{position_info}")
        print(f"    {display_type}")
        
        while True:
            user_input = input("Quantity: ").strip().upper()
            
            if user_input == 'X':
                print("\nExiting and saving progress...")
                write_inventory(filename, lines)
                if fig is not None:
                    plt.close(fig)
                print(f"✓ Progress saved to {filename}")
                return
            
            if user_input == 'S':
                print("Skipped.")
                break
            
            # Try to parse as a number
            try:
                quantity = int(user_input)
                if quantity < 0:
                    print("Please enter a positive number (or S to skip, X to exit)")
                    continue
                
                # Update the line in the file
                new_row = format_table_row(
                    switch['manufacturer'],
                    switch['name'],
                    switch['type'],
                    switch['force'],
                    str(quantity)
                )
                lines[switch['line_number']] = new_row
                
                print(f"✓ Recorded: {quantity}")
                break
            except ValueError:
                print("Invalid input. Enter a number, S to skip, or X to exit.")
    
    # Save the final results
    write_inventory(filename, lines)
    if fig is not None:
        plt.close(fig)
    print(f"\n✓ All done! Inventory saved to {filename}")


if __name__ == '__main__':
    main()
