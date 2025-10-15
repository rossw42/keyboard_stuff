"""
Tests for top frame CNC toolpath generation.

Validates toolpath operations, parameters, and data structures.
"""

import pytest
from src.constants import (
    CASE_LENGTH, CASE_WIDTH, CASE_CORNER_RADIUS,
    PCB_OPENING_LENGTH, PCB_OPENING_WIDTH, PCB_BORDER,
    USB_CUTOUT_WIDTH, USB_CUTOUT_HEIGHT, USB_CUTOUT_CORNER_RADIUS,
    USB_CUTOUT_CENTER_X, USB_CUTOUT_CENTER_Y,
    MOUNTING_HOLES, BRASS_INSERT_DIAMETER, BRASS_INSERT_DEPTH,
    TOP_FRAME_HEIGHT
)
from src.geometry.profiles import generate_top_frame_profile
from src.toolpaths.top_frame import (
    generate_face_surfacing_toolpath,
    generate_brass_insert_counterbore_toolpath,
    generate_pcb_opening_pocket_toolpath,
    generate_usb_cutout_toolpath,
    generate_external_profile_toolpath,
    generate_top_frame_toolpaths
)


def test_face_surfacing_toolpath():
    """Test face surfacing toolpath generation."""
    toolpath = generate_face_surfacing_toolpath(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        tool_diameter=6.0
    )
    
    assert toolpath['operation'] == 'face_surfacing'
    assert toolpath['tool']['diameter'] == 6.0
    assert toolpath['tool']['type'] == 'flat_endmill'
    assert toolpath['parameters']['depth'] == 0.5
    assert toolpath['parameters']['feed_rate'] == 1200
    assert toolpath['parameters']['spindle_speed'] == 18000
    assert len(toolpath['toolpath']) > 0  # Should have multiple passes
    assert 'estimated_time_minutes' in toolpath


def test_brass_insert_counterbore_toolpath():
    """Test brass insert counterbore toolpath generation."""
    toolpath = generate_brass_insert_counterbore_toolpath(
        mounting_holes=MOUNTING_HOLES,
        target_diameter=BRASS_INSERT_DIAMETER,
        tool_diameter=6.0,
        depth=BRASS_INSERT_DEPTH
    )
    
    assert toolpath['operation'] == 'brass_insert_counterbores'
    assert toolpath['tool']['diameter'] == 6.0
    assert toolpath['parameters']['target_diameter'] == BRASS_INSERT_DIAMETER
    assert toolpath['parameters']['depth'] == BRASS_INSERT_DEPTH
    assert toolpath['count'] == 6  # 6 mounting holes
    assert len(toolpath['toolpaths']) == 6
    
    # Check each hole has toolpath data
    for hole_id in ['TL', 'TR', 'ML', 'MR', 'BL', 'BR']:
        assert hole_id in toolpath['toolpaths']
        assert 'center' in toolpath['toolpaths'][hole_id]
        assert 'passes' in toolpath['toolpaths'][hole_id]
        assert len(toolpath['toolpaths'][hole_id]['passes']) > 0


def test_pcb_opening_pocket_toolpath():
    """Test PCB opening pocket toolpath generation."""
    profiles = generate_top_frame_profile(
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
    
    toolpath = generate_pcb_opening_pocket_toolpath(
        opening_profile=profiles['pcb_opening'],
        total_depth=TOP_FRAME_HEIGHT,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=3.0
    )
    
    assert toolpath['operation'] == 'pcb_opening_pocket'
    
    # Check roughing operation
    assert 'roughing' in toolpath
    assert toolpath['roughing']['tool']['diameter'] == 6.0
    assert toolpath['roughing']['parameters']['depth'] == TOP_FRAME_HEIGHT
    assert toolpath['roughing']['parameters']['stock_to_leave'] == 0.5
    
    # Check finishing operation
    assert 'finishing' in toolpath
    assert toolpath['finishing']['tool']['diameter'] == 3.0
    assert toolpath['finishing']['parameters']['tolerance'] == 0.1  # Critical tolerance


def test_usb_cutout_toolpath():
    """Test USB cutout toolpath generation."""
    profiles = generate_top_frame_profile(
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
    
    toolpath = generate_usb_cutout_toolpath(
        usb_profile=profiles['usb_cutout'],
        total_depth=10.0,
        tool_diameter=3.0
    )
    
    assert toolpath['operation'] == 'usb_cutout'
    assert toolpath['tool']['diameter'] == 3.0
    assert toolpath['parameters']['depth'] == 10.0
    assert toolpath['parameters']['corner_radius'] == 1.0
    assert toolpath['parameters']['tolerance'] == 0.2  # Standard tolerance
    assert toolpath['dimensions']['width'] == USB_CUTOUT_WIDTH
    assert toolpath['dimensions']['height'] == 10.0


def test_external_profile_toolpath():
    """Test external profile toolpath generation."""
    profiles = generate_top_frame_profile(
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
    
    toolpath = generate_external_profile_toolpath(
        external_profile=profiles['external_profile'],
        total_depth=TOP_FRAME_HEIGHT,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=3.0
    )
    
    assert toolpath['operation'] == 'external_profile'
    
    # Check roughing operation
    assert 'roughing' in toolpath
    assert toolpath['roughing']['tool']['diameter'] == 6.0
    assert toolpath['roughing']['parameters']['compensation'] == 'outside'
    
    # Check finishing operation
    assert 'finishing' in toolpath
    assert toolpath['finishing']['tool']['diameter'] == 3.0
    assert toolpath['finishing']['parameters']['corner_radius'] == 3.0
    assert toolpath['finishing']['parameters']['tolerance'] == 0.2  # Standard tolerance
    
    # Check tabs
    assert 'tabs' in toolpath
    assert toolpath['tabs']['count'] == 3  # Default 3 tabs
    assert toolpath['tabs']['width'] == 5.0


def test_complete_top_frame_toolpaths():
    """Test complete top frame toolpath generation."""
    profiles = generate_top_frame_profile(
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
    
    toolpaths = generate_top_frame_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=profiles['external_profile'],
        pcb_opening_profile=profiles['pcb_opening'],
        usb_cutout_profile=profiles['usb_cutout'],
        mounting_holes=MOUNTING_HOLES,
        top_frame_height=TOP_FRAME_HEIGHT
    )
    
    assert toolpaths['component'] == 'top_frame'
    assert 'operations' in toolpaths
    assert 'setup' in toolpaths
    assert 'summary' in toolpaths
    
    # Check all 5 operations are present
    operations = toolpaths['operations']
    assert '1_face_surfacing' in operations
    assert '2_brass_insert_counterbores' in operations
    assert '3_pcb_opening_pocket' in operations
    assert '4_usb_cutout' in operations
    assert '5_external_profile' in operations
    
    # Check summary
    summary = toolpaths['summary']
    assert summary['total_operations'] == 5
    assert len(summary['tools_required']) == 2  # 6mm and 3mm endmills
    assert len(summary['critical_tolerances']) == 3
    assert len(summary['standard_tolerances']) == 2
    
    # Check setup information
    setup = toolpaths['setup']
    assert setup['material'] == 'hardwood'
    assert setup['stock_dimensions']['length'] == CASE_LENGTH
    assert setup['stock_dimensions']['width'] == CASE_WIDTH
    assert setup['stock_dimensions']['thickness'] == 6.0


def test_toolpath_feed_rates():
    """Test that feed rates are appropriate for hardwood."""
    toolpath = generate_face_surfacing_toolpath(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        tool_diameter=6.0
    )
    
    # Feed rates should be conservative for hardwood
    assert toolpath['parameters']['feed_rate'] <= 1500  # Not too aggressive
    assert toolpath['parameters']['feed_rate'] >= 800   # Not too slow
    assert toolpath['parameters']['spindle_speed'] >= 15000  # High speed for clean cuts


def test_toolpath_depth_passes():
    """Test that depth passes are reasonable."""
    profiles = generate_top_frame_profile(
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
    
    toolpath = generate_pcb_opening_pocket_toolpath(
        opening_profile=profiles['pcb_opening'],
        total_depth=TOP_FRAME_HEIGHT,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=3.0
    )
    
    # Depth per pass should be reasonable (not too aggressive)
    assert toolpath['roughing']['parameters']['depth_per_pass'] <= 3.0
    assert toolpath['finishing']['parameters']['depth_per_pass'] <= 3.0


def test_toolpath_tolerances():
    """Test that critical and standard tolerances are correctly applied."""
    profiles = generate_top_frame_profile(
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
    
    # PCB opening should have critical tolerance (±0.1mm)
    pcb_toolpath = generate_pcb_opening_pocket_toolpath(
        opening_profile=profiles['pcb_opening'],
        total_depth=TOP_FRAME_HEIGHT,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=3.0
    )
    assert pcb_toolpath['finishing']['parameters']['tolerance'] == 0.1
    
    # USB cutout should have standard tolerance (±0.2mm)
    usb_toolpath = generate_usb_cutout_toolpath(
        usb_profile=profiles['usb_cutout'],
        total_depth=10.0,
        tool_diameter=3.0
    )
    assert usb_toolpath['parameters']['tolerance'] == 0.2
    
    # External profile should have standard tolerance (±0.2mm)
    profile_toolpath = generate_external_profile_toolpath(
        external_profile=profiles['external_profile'],
        total_depth=TOP_FRAME_HEIGHT,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=3.0
    )
    assert profile_toolpath['finishing']['parameters']['tolerance'] == 0.2
