"""
Tests for bottom tray 2D profile geometry generation.

Verifies that all geometric features are generated correctly according to
the design specifications and requirements.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from constants import (
    CASE_LENGTH, CASE_WIDTH, CASE_CORNER_RADIUS,
    CAVITY_LENGTH, CAVITY_WIDTH, CAVITY_CORNER_RADIUS, WALL_THICKNESS,
    MOUNTING_HOLES,
    STANDOFF_DIAMETER, STANDOFF_HOLE_DIAMETER,
    ASSEMBLY_SCREW_DIAMETER, ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
    RUBBER_FEET_POSITIONS, RUBBER_FEET_DIAMETER,
    TOLERANCE_CRITICAL, TOLERANCE_STANDARD
)
from geometry import (
    generate_bottom_tray_profile,
    generate_internal_cavity,
    generate_standoff_pillars,
    generate_standoff_holes,
    generate_assembly_screw_holes,
    generate_assembly_screw_counterbores,
    generate_rubber_feet_recesses
)


def test_bottom_tray_profile_generation():
    """Test that bottom tray profile generates all required features."""
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
    
    # Verify all required features are present
    assert 'external_profile' in profile
    assert 'internal_cavity' in profile
    assert 'standoff_pillars' in profile
    assert 'standoff_holes' in profile
    assert 'assembly_screw_holes' in profile
    assert 'assembly_counterbores' in profile
    assert 'rubber_feet_recesses' in profile
    
    # Verify feature counts
    assert len(profile['standoff_pillars']) == 6
    assert len(profile['standoff_holes']) == 6
    assert len(profile['assembly_screw_holes']) == 6
    assert len(profile['assembly_counterbores']) == 6
    assert len(profile['rubber_feet_recesses']) == 4


def test_external_profile_matches_top_frame():
    """Test that external profile matches top frame dimensions (Requirement 5.1, 7.3)."""
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
    
    external = profile['external_profile']
    
    # Check that profile has points
    assert len(external) > 0
    
    # Find bounding box
    x_coords = [p[0] for p in external]
    y_coords = [p[1] for p in external]
    
    width = max(x_coords) - min(x_coords)
    height = max(y_coords) - min(y_coords)
    
    # Verify dimensions within tolerance
    assert abs(width - CASE_LENGTH) < TOLERANCE_STANDARD
    assert abs(height - CASE_WIDTH) < TOLERANCE_STANDARD


def test_internal_cavity_dimensions():
    """Test internal cavity dimensions and wall thickness (Requirement 4.1, 5.3, 6.5)."""
    cavity = generate_internal_cavity(
        cavity_length=CAVITY_LENGTH,
        cavity_width=CAVITY_WIDTH,
        corner_radius=CAVITY_CORNER_RADIUS,
        wall_thickness=WALL_THICKNESS
    )
    
    # Check that cavity has points
    assert len(cavity) > 0
    
    # Find bounding box
    x_coords = [p[0] for p in cavity]
    y_coords = [p[1] for p in cavity]
    
    width = max(x_coords) - min(x_coords)
    height = max(y_coords) - min(y_coords)
    
    # Verify cavity dimensions
    assert abs(width - CAVITY_LENGTH) < TOLERANCE_STANDARD
    assert abs(height - CAVITY_WIDTH) < TOLERANCE_STANDARD
    
    # Verify cavity is inset by wall thickness
    assert abs(min(x_coords) - WALL_THICKNESS) < TOLERANCE_STANDARD
    assert abs(min(y_coords) - WALL_THICKNESS) < TOLERANCE_STANDARD


def test_standoff_pillar_positions():
    """Test standoff pillar positions match mounting holes (Requirement 2.2, 2.4)."""
    pillars = generate_standoff_pillars(
        mounting_holes=MOUNTING_HOLES,
        pillar_diameter=STANDOFF_DIAMETER
    )
    
    # Verify correct number of pillars
    assert len(pillars) == 6
    
    # Verify all mounting hole IDs are present
    expected_ids = {'TL', 'TR', 'ML', 'MR', 'BL', 'BR'}
    assert set(pillars.keys()) == expected_ids
    
    # Verify each pillar is centered at the mounting hole position
    for hole_id, pillar_profile in pillars.items():
        expected_center = MOUNTING_HOLES[hole_id]
        
        # Calculate center from profile points
        x_coords = [p[0] for p in pillar_profile]
        y_coords = [p[1] for p in pillar_profile]
        center_x = (max(x_coords) + min(x_coords)) / 2
        center_y = (max(y_coords) + min(y_coords)) / 2
        
        # Verify center position within critical tolerance
        assert abs(center_x - expected_center[0]) < TOLERANCE_CRITICAL
        assert abs(center_y - expected_center[1]) < TOLERANCE_CRITICAL


def test_standoff_hole_diameter():
    """Test standoff through-holes have correct diameter (Requirement 2.3, 2.4)."""
    holes = generate_standoff_holes(
        mounting_holes=MOUNTING_HOLES,
        hole_diameter=STANDOFF_HOLE_DIAMETER
    )
    
    # Verify correct number of holes
    assert len(holes) == 6
    
    # Check diameter of one hole
    hole_profile = holes['TL']
    x_coords = [p[0] for p in hole_profile]
    y_coords = [p[1] for p in hole_profile]
    
    diameter_x = max(x_coords) - min(x_coords)
    diameter_y = max(y_coords) - min(y_coords)
    
    # Verify diameter within critical tolerance
    assert abs(diameter_x - STANDOFF_HOLE_DIAMETER) < TOLERANCE_CRITICAL
    assert abs(diameter_y - STANDOFF_HOLE_DIAMETER) < TOLERANCE_CRITICAL


def test_assembly_screw_holes():
    """Test assembly screw holes are concentric with standoffs (Requirement 2.2, 7.1)."""
    screw_holes = generate_assembly_screw_holes(
        mounting_holes=MOUNTING_HOLES,
        hole_diameter=ASSEMBLY_SCREW_DIAMETER
    )
    
    # Verify correct number of holes
    assert len(screw_holes) == 6
    
    # Verify holes are centered at mounting positions
    for hole_id, hole_profile in screw_holes.items():
        expected_center = MOUNTING_HOLES[hole_id]
        
        x_coords = [p[0] for p in hole_profile]
        y_coords = [p[1] for p in hole_profile]
        center_x = (max(x_coords) + min(x_coords)) / 2
        center_y = (max(y_coords) + min(y_coords)) / 2
        
        # Verify concentric with standoffs
        assert abs(center_x - expected_center[0]) < TOLERANCE_STANDARD
        assert abs(center_y - expected_center[1]) < TOLERANCE_STANDARD


def test_assembly_counterbore_diameter():
    """Test assembly screw counterbores have correct diameter (Requirement 7.1)."""
    counterbores = generate_assembly_screw_counterbores(
        mounting_holes=MOUNTING_HOLES,
        counterbore_diameter=ASSEMBLY_SCREW_COUNTERBORE_DIAMETER
    )
    
    # Verify correct number of counterbores
    assert len(counterbores) == 6
    
    # Check diameter of one counterbore
    counterbore_profile = counterbores['TL']
    x_coords = [p[0] for p in counterbore_profile]
    y_coords = [p[1] for p in counterbore_profile]
    
    diameter_x = max(x_coords) - min(x_coords)
    diameter_y = max(y_coords) - min(y_coords)
    
    # Verify diameter within standard tolerance
    assert abs(diameter_x - ASSEMBLY_SCREW_COUNTERBORE_DIAMETER) < TOLERANCE_STANDARD
    assert abs(diameter_y - ASSEMBLY_SCREW_COUNTERBORE_DIAMETER) < TOLERANCE_STANDARD


def test_rubber_feet_recesses():
    """Test rubber feet recesses in 4 corners (Requirement 5.4)."""
    recesses = generate_rubber_feet_recesses(
        feet_positions=RUBBER_FEET_POSITIONS,
        recess_diameter=RUBBER_FEET_DIAMETER
    )
    
    # Verify correct number of recesses
    assert len(recesses) == 4
    
    # Verify each recess has correct diameter
    for i, recess_profile in enumerate(recesses):
        x_coords = [p[0] for p in recess_profile]
        y_coords = [p[1] for p in recess_profile]
        
        diameter_x = max(x_coords) - min(x_coords)
        diameter_y = max(y_coords) - min(y_coords)
        
        # Verify diameter within standard tolerance
        assert abs(diameter_x - RUBBER_FEET_DIAMETER) < TOLERANCE_STANDARD
        assert abs(diameter_y - RUBBER_FEET_DIAMETER) < TOLERANCE_STANDARD
        
        # Verify center position matches expected position
        center_x = (max(x_coords) + min(x_coords)) / 2
        center_y = (max(y_coords) + min(y_coords)) / 2
        expected_center = RUBBER_FEET_POSITIONS[i]
        
        assert abs(center_x - expected_center[0]) < TOLERANCE_STANDARD
        assert abs(center_y - expected_center[1]) < TOLERANCE_STANDARD


def test_rubber_feet_corner_positions():
    """Test rubber feet are positioned 10mm from corners (Requirement 5.4)."""
    # Verify positions are 10mm from corners
    corner_offset = 10.0
    
    # Top-left corner
    assert RUBBER_FEET_POSITIONS[0] == (corner_offset, corner_offset)
    
    # Top-right corner
    assert RUBBER_FEET_POSITIONS[1] == (CASE_LENGTH - corner_offset, corner_offset)
    
    # Bottom-left corner
    assert RUBBER_FEET_POSITIONS[2] == (corner_offset, CASE_WIDTH - corner_offset)
    
    # Bottom-right corner
    assert RUBBER_FEET_POSITIONS[3] == (CASE_LENGTH - corner_offset, CASE_WIDTH - corner_offset)


def test_wall_thickness_minimum():
    """Test wall thickness meets minimum requirement (Requirement 5.3)."""
    # Verify wall thickness is at least 3mm (design uses 4mm)
    assert WALL_THICKNESS >= 3.0
    assert WALL_THICKNESS == 4.0


def test_cavity_corner_radius():
    """Test cavity corner radius matches tool limitation (Requirement 6.5)."""
    # 2mm radius for 4mm endmill limitation
    assert CAVITY_CORNER_RADIUS == 2.0
