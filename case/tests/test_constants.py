"""
Tests to validate dimensional constants against requirements.
"""

import sys
sys.path.insert(0, 'src')

from constants import *


def test_pcb_dimensions():
    """Verify PCB dimensions match requirements 1.1, 1.2"""
    assert PCB_LENGTH == 285.0, "PCB length should be 285mm"
    assert PCB_WIDTH == 94.6, "PCB width should be 94.6mm"
    assert PCB_THICKNESS == 1.6, "PCB thickness should be 1.6mm"


def test_case_external_dimensions():
    """Verify case external dimensions (Requirement 5.1)"""
    assert CASE_LENGTH == 295.0, "Case length should be 295mm"
    assert CASE_WIDTH == 105.0, "Case width should be 105mm"
    assert CASE_CORNER_RADIUS == 3.0, "Corner radius should be 3mm"


def test_pcb_opening_clearance():
    """Verify PCB opening provides proper clearance (Requirement 1.1)"""
    assert PCB_OPENING_LENGTH == PCB_LENGTH + 1.0, "PCB opening should have 1mm total clearance in length"
    assert PCB_OPENING_WIDTH == PCB_WIDTH + 1.0, "PCB opening should have 1mm total clearance in width"
    assert PCB_CLEARANCE == 0.5, "PCB clearance should be 0.5mm per side"


def test_mounting_hole_count():
    """Verify 6 mounting holes are defined (Requirement 2.1)"""
    assert len(MOUNTING_HOLES) == 6, "Should have exactly 6 mounting holes"
    expected_keys = {'TL', 'TR', 'ML', 'MR', 'BL', 'BR'}
    assert set(MOUNTING_HOLES.keys()) == expected_keys, "Mounting holes should have correct identifiers"


def test_mounting_hole_positions():
    """Verify mounting hole positions match specification (Requirement 2.2)"""
    # Positions are offset by PCB_BORDER (4.5mm) from the specified PCB coordinates
    assert MOUNTING_HOLES['TL'] == (23.5, 14.0), "Top-left mounting hole position incorrect"
    assert MOUNTING_HOLES['TR'] == (270.5, 14.0), "Top-right mounting hole position incorrect"
    assert MOUNTING_HOLES['ML'] == (33.0, 51.8), "Middle-left mounting hole position incorrect"
    assert MOUNTING_HOLES['MR'] == (261.0, 51.8), "Middle-right mounting hole position incorrect"
    assert MOUNTING_HOLES['BL'] == (61.5, 89.5), "Bottom-left mounting hole position incorrect"
    assert MOUNTING_HOLES['BR'] == (232.5, 89.5), "Bottom-right mounting hole position incorrect"


def test_usb_cutout_dimensions():
    """Verify USB cutout dimensions (Requirement 3.1, 3.3)"""
    assert USB_CUTOUT_WIDTH == 16.0, "USB cutout width should be 16mm"
    assert USB_CUTOUT_HEIGHT == 10.0, "USB cutout height should be 10mm"
    assert USB_CUTOUT_CORNER_RADIUS == 1.0, "USB cutout corner radius should be 1mm"


def test_usb_cutout_position():
    """Verify USB cutout is centered and properly positioned (Requirement 3.1, 3.2)"""
    assert USB_CUTOUT_CENTER_X == CASE_LENGTH / 2.0, "USB cutout should be centered horizontally"
    assert USB_OFFSET_FROM_PCB_EDGE == 7.0, "USB cutout should be 7mm from PCB edge"


def test_brass_insert_specifications():
    """Verify brass insert specifications (Requirement 2.5)"""
    assert BRASS_INSERT_DIAMETER == 5.8, "Brass insert hole should be 5.8mm for press-fit"
    assert BRASS_INSERT_DEPTH == 4.0, "Brass insert depth should be 4mm"
    assert BRASS_INSERT_THREAD == 'M3', "Brass inserts should be M3 thread"


def test_standoff_specifications():
    """Verify standoff specifications (Requirement 2.3, 2.4)"""
    assert STANDOFF_DIAMETER == 6.0, "Standoff diameter should be 6mm"
    assert STANDOFF_HEIGHT == 3.0, "Standoff height should be 3mm"
    assert STANDOFF_HOLE_DIAMETER == 2.2, "Standoff hole should be 2.2mm for M2 screws"


def test_tolerances():
    """Verify tolerance specifications (Requirement 6.3)"""
    assert TOLERANCE_CRITICAL == 0.1, "Critical tolerance should be ±0.1mm"
    assert TOLERANCE_STANDARD == 0.2, "Standard tolerance should be ±0.2mm"


def test_wall_thickness():
    """Verify wall thickness meets minimum requirement (Requirement 5.3)"""
    assert WALL_THICKNESS >= 3.0, "Wall thickness should be minimum 3mm"
    assert WALL_THICKNESS == 4.0, "Wall thickness should be 4mm"


def test_cavity_clearance():
    """Verify cavity provides adequate clearance (Requirement 4.1)"""
    # Cavity depth (8mm) - standoff height (3mm) = 5mm clearance below PCB
    clearance_below_pcb = CAVITY_DEPTH - STANDOFF_HEIGHT
    assert clearance_below_pcb >= 5.0, "Should provide minimum 5mm clearance below PCB"


def test_rubber_feet_count():
    """Verify 4 rubber feet positions are defined (Requirement 5.4)"""
    assert len(RUBBER_FEET_POSITIONS) == 4, "Should have exactly 4 rubber feet positions"


def test_rubber_feet_specifications():
    """Verify rubber feet specifications (Requirement 5.4)"""
    assert RUBBER_FEET_DIAMETER == 10.0, "Rubber feet recess should be 10mm diameter"
    assert RUBBER_FEET_DEPTH == 2.0, "Rubber feet recess should be 2mm deep"
    assert RUBBER_FEET_CORNER_OFFSET == 10.0, "Rubber feet should be 10mm from corners"


def test_component_heights():
    """Verify component height specifications"""
    assert TOP_FRAME_HEIGHT == 5.0, "Top frame should be 5mm high"
    assert BOTTOM_TRAY_HEIGHT == 15.0, "Bottom tray should be 15mm high"
    assert CAVITY_DEPTH == 8.0, "Cavity should be 8mm deep"


def test_coordinate_system():
    """Verify coordinate system is properly defined"""
    assert ORIGIN == (0.0, 0.0, 0.0), "Origin should be at (0, 0, 0)"
    assert 'origin' in COORDINATE_SYSTEM, "Coordinate system should define origin"
    assert 'x_axis' in COORDINATE_SYSTEM, "Coordinate system should define x-axis"
    assert 'y_axis' in COORDINATE_SYSTEM, "Coordinate system should define y-axis"
    assert 'z_axis' in COORDINATE_SYSTEM, "Coordinate system should define z-axis"


def test_tool_definitions():
    """Verify CNC tool specifications are defined (Requirement 6.1)"""
    required_tools = ['endmill_6mm', 'endmill_4mm', 'endmill_3mm', 'drill_2.2mm', 'drill_3.2mm', 'endmill_10mm']
    for tool in required_tools:
        assert tool in TOOLS, f"Tool {tool} should be defined"
        assert 'diameter' in TOOLS[tool], f"Tool {tool} should have diameter specified"
        assert 'type' in TOOLS[tool], f"Tool {tool} should have type specified"


def test_material_specifications():
    """Verify material specifications are defined (Requirement 6.2)"""
    assert MATERIAL['type'] == 'hardwood', "Material type should be hardwood"
    assert 'top_frame_stock' in MATERIAL, "Top frame stock should be specified"
    assert 'bottom_tray_stock' in MATERIAL, "Bottom tray stock should be specified"
    assert MATERIAL['top_frame_stock']['thickness'] >= TOP_FRAME_HEIGHT, "Top frame stock should be thick enough"
    assert MATERIAL['bottom_tray_stock']['thickness'] >= BOTTOM_TRAY_HEIGHT, "Bottom tray stock should be thick enough"


if __name__ == '__main__':
    # Run all tests
    test_functions = [
        test_pcb_dimensions,
        test_case_external_dimensions,
        test_pcb_opening_clearance,
        test_mounting_hole_count,
        test_mounting_hole_positions,
        test_usb_cutout_dimensions,
        test_usb_cutout_position,
        test_brass_insert_specifications,
        test_standoff_specifications,
        test_tolerances,
        test_wall_thickness,
        test_cavity_clearance,
        test_rubber_feet_count,
        test_rubber_feet_specifications,
        test_component_heights,
        test_coordinate_system,
        test_tool_definitions,
        test_material_specifications,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"✓ {test_func.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__}: Unexpected error: {e}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
