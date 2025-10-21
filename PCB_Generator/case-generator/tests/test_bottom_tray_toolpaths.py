"""
Tests for bottom tray CNC toolpath generation.

Verifies that all toolpath operations are generated correctly with
proper parameters, feed rates, and tolerances.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.constants import *
from src.geometry.profiles import generate_bottom_tray_profile
from src.toolpaths.bottom_tray import (
    generate_face_surfacing_toolpath,
    generate_rubber_feet_recess_toolpath,
    generate_assembly_screw_counterbore_toolpath,
    generate_assembly_screw_through_hole_toolpath,
    generate_internal_cavity_pocket_toolpath,
    generate_standoff_through_hole_toolpath,
    generate_external_profile_toolpath,
    generate_bottom_tray_toolpaths
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
    assert toolpath['parameters']['depth'] == 0.5
    assert toolpath['parameters']['feed_rate'] == 1200
    assert toolpath['parameters']['spindle_speed'] == 18000
    assert len(toolpath['toolpath']) > 0


def test_rubber_feet_recess_toolpath():
    """Test rubber feet recess toolpath generation."""
    toolpath = generate_rubber_feet_recess_toolpath(
        feet_positions=RUBBER_FEET_POSITIONS,
        recess_diameter=10.0,
        tool_diameter=10.0,
        depth=2.0
    )
    
    assert toolpath['operation'] == 'rubber_feet_recesses'
    assert toolpath['tool']['diameter'] == 10.0
    assert toolpath['parameters']['depth'] == 2.0
    assert toolpath['count'] == 4
    assert len(toolpath['toolpaths']) == 4


def test_assembly_screw_counterbore_toolpath():
    """Test assembly screw counterbore toolpath generation."""
    toolpath = generate_assembly_screw_counterbore_toolpath(
        mounting_holes=MOUNTING_HOLES,
        counterbore_diameter=6.0,
        tool_diameter=6.0,
        depth=3.0
    )
    
    assert toolpath['operation'] == 'assembly_screw_counterbores'
    assert toolpath['tool']['diameter'] == 6.0
    assert toolpath['parameters']['depth'] == 3.0
    assert toolpath['count'] == 6
    assert len(toolpath['toolpaths']) == 6


def test_assembly_screw_through_hole_toolpath():
    """Test assembly screw through-hole toolpath generation."""
    toolpath = generate_assembly_screw_through_hole_toolpath(
        mounting_holes=MOUNTING_HOLES,
        hole_diameter=3.2,
        total_depth=15.0
    )
    
    assert toolpath['operation'] == 'assembly_screw_through_holes'
    assert toolpath['tool']['diameter'] == 3.2
    assert toolpath['parameters']['depth'] == 15.0
    assert toolpath['count'] == 6
    assert len(toolpath['toolpaths']) == 6


def test_internal_cavity_pocket_toolpath():
    """Test internal cavity pocket toolpath generation."""
    geometry = generate_bottom_tray_profile(
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
    
    toolpath = generate_internal_cavity_pocket_toolpath(
        cavity_profile=geometry['internal_cavity'],
        standoff_pillars=geometry['standoff_pillars'],
        total_depth=8.0,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=4.0
    )
    
    assert toolpath['operation'] == 'internal_cavity_pocket'
    assert 'roughing' in toolpath
    assert 'finishing' in toolpath
    assert toolpath['roughing']['tool']['diameter'] == 6.0
    assert toolpath['finishing']['tool']['diameter'] == 4.0
    assert toolpath['roughing']['parameters']['depth'] == 8.0
    assert toolpath['finishing']['parameters']['corner_radius'] == 2.0


def test_standoff_through_hole_toolpath():
    """Test standoff through-hole toolpath generation."""
    toolpath = generate_standoff_through_hole_toolpath(
        mounting_holes=MOUNTING_HOLES,
        hole_diameter=2.2,
        total_depth=6.0
    )
    
    assert toolpath['operation'] == 'standoff_through_holes'
    assert toolpath['tool']['diameter'] == 2.2
    assert toolpath['parameters']['hole_diameter'] == 2.2
    assert toolpath['parameters']['tolerance'] == 0.1  # Critical tolerance
    assert toolpath['count'] == 6


def test_external_profile_toolpath():
    """Test external profile toolpath generation."""
    geometry = generate_bottom_tray_profile(
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
    
    toolpath = generate_external_profile_toolpath(
        external_profile=geometry['external_profile'],
        total_depth=15.0,
        roughing_tool_diameter=6.0,
        finishing_tool_diameter=3.0
    )
    
    assert toolpath['operation'] == 'external_profile'
    assert 'roughing' in toolpath
    assert 'finishing' in toolpath
    assert toolpath['roughing']['tool']['diameter'] == 6.0
    assert toolpath['finishing']['tool']['diameter'] == 3.0
    assert toolpath['dimensions']['corner_radius'] == 3.0


def test_complete_bottom_tray_toolpaths():
    """Test complete bottom tray toolpath generation."""
    geometry = generate_bottom_tray_profile(
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
    
    toolpaths = generate_bottom_tray_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=geometry['external_profile'],
        internal_cavity_profile=geometry['internal_cavity'],
        standoff_pillars=geometry['standoff_pillars'],
        mounting_holes=MOUNTING_HOLES,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        cavity_depth=CAVITY_DEPTH
    )
    
    assert toolpaths['component'] == 'bottom_tray'
    assert len(toolpaths['operations']) == 7
    assert '1_face_surfacing' in toolpaths['operations']
    assert '2_rubber_feet_recesses' in toolpaths['operations']
    assert '3_assembly_screw_counterbores' in toolpaths['operations']
    assert '4_assembly_screw_through_holes' in toolpaths['operations']
    assert '5_internal_cavity_pocket' in toolpaths['operations']
    assert '6_standoff_through_holes' in toolpaths['operations']
    assert '7_external_profile' in toolpaths['operations']


def test_toolpath_feed_rates():
    """Test that feed rates are appropriate for hardwood."""
    geometry = generate_bottom_tray_profile(
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
    
    toolpaths = generate_bottom_tray_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=geometry['external_profile'],
        internal_cavity_profile=geometry['internal_cavity'],
        standoff_pillars=geometry['standoff_pillars'],
        mounting_holes=MOUNTING_HOLES,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        cavity_depth=CAVITY_DEPTH
    )
    
    # Check feed rates are within reasonable ranges for hardwood
    surfacing = toolpaths['operations']['1_face_surfacing']
    assert 800 <= surfacing['parameters']['feed_rate'] <= 1500
    
    cavity = toolpaths['operations']['5_internal_cavity_pocket']
    assert 800 <= cavity['roughing']['parameters']['feed_rate'] <= 1500
    assert 600 <= cavity['finishing']['parameters']['feed_rate'] <= 1000


def test_toolpath_depth_passes():
    """Test that depth passes are calculated correctly."""
    geometry = generate_bottom_tray_profile(
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
    
    toolpaths = generate_bottom_tray_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=geometry['external_profile'],
        internal_cavity_profile=geometry['internal_cavity'],
        standoff_pillars=geometry['standoff_pillars'],
        mounting_holes=MOUNTING_HOLES,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        cavity_depth=CAVITY_DEPTH
    )
    
    # Check cavity pocket depth passes (8mm depth, 2mm per pass = 4 passes)
    cavity = toolpaths['operations']['5_internal_cavity_pocket']
    assert cavity['roughing']['parameters']['num_passes'] == 4
    
    # Check external profile depth passes (15mm depth, 2.5mm per pass = 6 passes)
    profile = toolpaths['operations']['7_external_profile']
    assert profile['roughing']['parameters']['num_passes'] == 6


def test_toolpath_tolerances():
    """Test that critical and standard tolerances are correctly specified."""
    geometry = generate_bottom_tray_profile(
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
    
    toolpaths = generate_bottom_tray_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=geometry['external_profile'],
        internal_cavity_profile=geometry['internal_cavity'],
        standoff_pillars=geometry['standoff_pillars'],
        mounting_holes=MOUNTING_HOLES,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        cavity_depth=CAVITY_DEPTH
    )
    
    # Critical tolerance for standoff holes (M2 screw fit)
    standoff_holes = toolpaths['operations']['6_standoff_through_holes']
    assert standoff_holes['parameters']['tolerance'] == 0.1
    
    # Standard tolerance for cavity
    cavity = toolpaths['operations']['5_internal_cavity_pocket']
    assert cavity['finishing']['parameters']['tolerance'] == 0.2
    
    # Standard tolerance for external profile
    profile = toolpaths['operations']['7_external_profile']
    assert profile['finishing']['parameters']['tolerance'] == 0.2


def test_standoff_pillar_islands():
    """Test that standoff pillars are preserved as islands in cavity."""
    geometry = generate_bottom_tray_profile(
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
    
    toolpaths = generate_bottom_tray_toolpaths(
        case_length=CASE_LENGTH,
        case_width=CASE_WIDTH,
        external_profile=geometry['external_profile'],
        internal_cavity_profile=geometry['internal_cavity'],
        standoff_pillars=geometry['standoff_pillars'],
        mounting_holes=MOUNTING_HOLES,
        rubber_feet_positions=RUBBER_FEET_POSITIONS,
        bottom_tray_height=BOTTOM_TRAY_HEIGHT,
        cavity_depth=CAVITY_DEPTH
    )
    
    cavity = toolpaths['operations']['5_internal_cavity_pocket']
    assert 'islands' in cavity['roughing']
    assert cavity['roughing']['islands']['count'] == 6
    assert cavity['roughing']['islands']['diameter'] == 6.0
