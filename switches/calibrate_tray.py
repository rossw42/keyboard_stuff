#!/usr/bin/env python3
"""
Tray Calibration Tool

Click on switch positions in the tray images to calibrate the grid coordinates.
This will generate precise pixel positions for each switch location.
"""

import json
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Store calibration points
calibration_data = {
    'IMG_3218.JPG': {},  # Will store {(row, col): (x, y)}
    'IMG_3219.JPG': {},
    'IMG_3220.JPG': {}
}

current_image = None
current_ax = None
current_fig = None
calibration_points = []


def on_click(event):
    """Handle mouse clicks to mark switch positions."""
    if event.xdata is None or event.ydata is None:
        return
    
    x, y = int(event.xdata), int(event.ydata)
    print(f"\nClicked at pixel ({x}, {y})")
    
    # Ask for the row and column
    try:
        row = int(input("Enter row (0-3): "))
        col = int(input("Enter column (0-14): "))
        
        if 0 <= row <= 3 and 0 <= col <= 14:
            calibration_points.append((row, col, x, y))
            print(f"✓ Recorded: Row {row}, Col {col} at ({x}, {y})")
            
            # Draw a marker
            current_ax.plot(x, y, 'ro', markersize=8)
            current_ax.text(x, y-30, f"{row},{col}", color='red', fontsize=10, 
                          ha='center', fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
            plt.draw()
        else:
            print("Invalid row/column. Row must be 0-3, column must be 0-14")
    except ValueError:
        print("Invalid input, try again")


def calibrate_image(image_path):
    """Open an image for calibration."""
    global current_image, current_ax, current_fig, calibration_points
    
    calibration_points = []
    
    img = Image.open(image_path)
    
    fig, ax = plt.subplots(figsize=(16, 10))
    current_fig = fig
    current_ax = ax
    
    ax.imshow(img)
    ax.set_title(f'Calibration: {image_path}\nClick on switch centers, then enter row/column in console', 
                fontsize=14, fontweight='bold')
    ax.axis('on')
    
    # Connect click event
    cid = fig.canvas.mpl_connect('button_press_event', on_click)
    
    print(f"\n{'='*60}")
    print(f"Calibrating: {image_path}")
    print(f"{'='*60}")
    print("Instructions:")
    print("1. Click on the CENTER of each switch")
    print("2. Enter the row (0-3) and column (0-14) when prompted")
    print("3. Close the window when done with this image")
    print("\nTip: Start with corners and edges for best results")
    print(f"{'='*60}\n")
    
    plt.show()
    
    return calibration_points


def main():
    print("Tray Calibration Tool")
    print("=" * 60)
    print("This tool helps you mark the exact pixel positions of switches")
    print("in your tray photos for precise highlighting.")
    print()
    
    images = ['IMG_3218.JPG', 'IMG_3219.JPG', 'IMG_3220.JPG']
    
    all_calibrations = {}
    
    for img_file in images:
        try:
            print(f"\nCalibrating {img_file}...")
            points = calibrate_image(img_file)
            
            if points:
                all_calibrations[img_file] = points
                print(f"\n✓ Recorded {len(points)} calibration points for {img_file}")
            else:
                print(f"\n⚠ No calibration points recorded for {img_file}")
        except Exception as e:
            print(f"Error with {img_file}: {e}")
    
    # Save calibration data
    if all_calibrations:
        output = {
            'version': '1.0',
            'description': 'Manual calibration points for switch tray images',
            'images': {}
        }
        
        for img_file, points in all_calibrations.items():
            output['images'][img_file] = [
                {'row': row, 'col': col, 'x': x, 'y': y}
                for row, col, x, y in points
            ]
        
        with open('tray_calibration.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n{'='*60}")
        print("✓ Calibration saved to tray_calibration.json")
        print(f"{'='*60}")
        
        # Show summary
        for img_file, points in all_calibrations.items():
            print(f"\n{img_file}: {len(points)} points")
            for row, col, x, y in points:
                print(f"  Row {row}, Col {col}: ({x}, {y})")
    else:
        print("\n⚠ No calibration data to save")


if __name__ == '__main__':
    main()
