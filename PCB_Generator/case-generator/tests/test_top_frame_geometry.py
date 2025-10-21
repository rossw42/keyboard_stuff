"""
Tests for top frame 2D profile geometry generation.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from constants import (
    CASE_LENGTH, CASE_WIDTH, CASE_CORNER_RADIUS,
    PCB_OPENING_LENGTH, PCB_OPENING_WIDTH, PCB_BORDER,
    USB_CUTOUT_WIDTH, USB_CUTOUT_HEIGHT, USB_CUTOUT_CORNER_RADIUS,
    USB_CUTOUT_CENTER_X, USB_CUTOUT_CENTER_Y,
    MOUNTING_HOLES, BRASS_INSERT_DIAMETER
)
from geometry import generate_top_frame_profile


def test_top_frame_profile_generation():
    """Test that top frame profile generates all required features."""
    
    # Generate complete top frame profile
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
    
    # Verify all features are present
    assert 'external_profile' in profile, "Missing external_profile"
    assert 'pcb_opening' in profile, "Missing pcb_opening"
    assert 'usb_cutout' in profile, "Missing usb_cutout"
    assert 'brass_insert_holes' in profile, "Missing brass_insert_holes"
    
    # Verify external profile has points
    assert len(profile['external_profile']) > 0, "External profile is empty"
    
    # Verify PCB opening has correct number of points (5 for rectangle)
    assert len(profile['pcb_opening']) == 5, f"PCB opening should have 5 points, got {len(profile['pcb_opening'])}"
    
    # Verify USB cutout has points
    assert len(profile['usb_cutout']) > 0, "USB cutout is empty"
    
    # Verify brass insert holes (should have 6 holes)
    assert len(profile['brass_insert_holes']) == 6, f"Should have 6 brass insert holes, got {len(profile['brass_insert_holes'])}"
    
    # Verify all expected hole IDs are present
    expected_holes = {'TL', 'TR', 'ML', 'MR', 'BL', 'BR'}
    actual_holes = set(profile['brass_insert_holes'].keys())
    assert actual_holes == expected_holes, f"Hole IDs mismatch: expected {expected_holes}, got {actual_holes}"
    
    print("✓ All features generated successfully")
    return profile


def test_external_profile_dimensions():
    """Test that external profile has correct dimensions."""
    from geometry import generate_external_profile
    
    profile = generate_external_profile(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        corner_radius=CASE_CORNER_RADIUS
    )
    
    # Find min/max coordinates
    x_coords = [p[0] for p in profile]
    y_coords = [p[1] for p in profile]
    
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Check dimensions (with tolerance for rounded corners)
    length = max_x - min_x
    width = max_y - min_y
    
    assert abs(length - CASE_LENGTH) < 0.01, f"Length mismatch: expected {CASE_LENGTH}, got {length}"
    assert abs(width - CASE_WIDTH) < 0.01, f"Width mismatch: expected {CASE_WIDTH}, got {width}"
    
    print(f"✓ External profile dimensions: {length:.2f}mm x {width:.2f}mm")


def test_pcb_opening_dimensions():
    """Test that PCB opening has correct dimensions and position."""
    from geometry import generate_pcb_opening
    
    opening = generate_pcb_opening(
        opening_length=PCB_OPENING_LENGTH,
        opening_width=PCB_OPENING_WIDTH,
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        border=PCB_BORDER
    )
    
    # Extract coordinates
    x_coords = [p[0] for p in opening]
    y_coords = [p[1] for p in opening]
    
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Check dimensions
    length = max_x - min_x
    width = max_y - min_y
    
    assert abs(length - PCB_OPENING_LENGTH) < 0.01, f"Opening length mismatch: expected {PCB_OPENING_LENGTH}, got {length}"
    assert abs(width - PCB_OPENING_WIDTH) < 0.01, f"Opening width mismatch: expected {PCB_OPENING_WIDTH}, got {width}"
    
    # Check centering (border should be equal on all sides)
    assert abs(min_x - PCB_BORDER) < 0.01, f"Left border mismatch: expected {PCB_BORDER}, got {min_x}"
    assert abs(min_y - PCB_BORDER) < 0.01, f"Top border mismatch: expected {PCB_BORDER}, got {min_y}"
    
    print(f"✓ PCB opening: {length:.2f}mm x {width:.2f}mm, border: {min_x:.2f}mm")


def test_usb_cutout_position():
    """Test that USB cutout is correctly positioned."""
    from geometry import generate_usb_cutout
    
    cutout = generate_usb_cutout(
        cutout_width=USB_CUTOUT_WIDTH,
        cutout_height=USB_CUTOUT_HEIGHT,
        corner_radius=USB_CUTOUT_CORNER_RADIUS,
        center_x=USB_CUTOUT_CENTER_X,
        center_y=USB_CUTOUT_CENTER_Y
    )
    
    # Find center of cutout
    x_coords = [p[0] for p in cutout]
    y_coords = [p[1] for p in cutout]
    
    center_x = (min(x_coords) + max(x_coords)) / 2
    center_y = (min(y_coords) + max(y_coords)) / 2
    
    # Check centering
    assert abs(center_x - USB_CUTOUT_CENTER_X) < 0.1, f"USB X position mismatch: expected {USB_CUTOUT_CENTER_X}, got {center_x}"
    assert abs(center_y - USB_CUTOUT_CENTER_Y) < 0.1, f"USB Y position mismatch: expected {USB_CUTOUT_CENTER_Y}, got {center_y}"
    
    print(f"✓ USB cutout centered at: ({center_x:.2f}, {center_y:.2f})mm")


def test_brass_insert_holes():
    """Test that brass insert holes are at correct positions."""
    from geometry import generate_brass_insert_holes
    
    holes = generate_brass_insert_holes(
        mounting_holes=MOUNTING_HOLES,
        insert_diameter=BRASS_INSERT_DIAMETER
    )
    
    # Verify each hole is centered at the correct position
    for hole_id, expected_pos in MOUNTING_HOLES.items():
        assert hole_id in holes, f"Missing hole: {hole_id}"
        
        hole_profile = holes[hole_id]
        x_coords = [p[0] for p in hole_profile]
        y_coords = [p[1] for p in hole_profile]
        
        center_x = (min(x_coords) + max(x_coords)) / 2
        center_y = (min(y_coords) + max(y_coords)) / 2
        
        assert abs(center_x - expected_pos[0]) < 0.01, f"Hole {hole_id} X mismatch: expected {expected_pos[0]}, got {center_x}"
        assert abs(center_y - expected_pos[1]) < 0.01, f"Hole {hole_id} Y mismatch: expected {expected_pos[1]}, got {center_y}"
    
    print(f"✓ All 6 brass insert holes positioned correctly")


if __name__ == '__main__':
    print("Testing top frame 2D profile geometry generation...\n")
    
    test_external_profile_dimensions()
    test_pcb_opening_dimensions()
    test_usb_cutout_position()
    test_brass_insert_holes()
    test_top_frame_profile_generation()
    
    print("\n✅ All tests passed!")
