"""Tests for layout engine"""

import pytest
from thkg.layout import PositionCalculator, MatrixCalculator, PinAssigner, LayoutPresets
from thkg.config import Switch, Matrix, MCUType


def test_position_calculator():
    """Test position calculation"""
    calc = PositionCalculator()
    
    # Create simple switches
    switches = [
        Switch(row=0, col=0, x=0, y=0),
        Switch(row=0, col=1, x=19.05, y=0),
        Switch(row=1, col=0, x=0, y=19.05),
    ]
    
    # Get bounding box
    min_x, min_y, max_x, max_y = calc.get_bounding_box(switches)
    assert min_x == 0
    assert min_y == 0
    assert max_x > 0
    assert max_y > 0


def test_matrix_calculator():
    """Test matrix calculation"""
    calc = MatrixCalculator()
    
    # Create switches
    switches = [Switch(row=i, col=0, x=0, y=i*19.05) for i in range(9)]
    
    # Calculate matrix
    matrix = calc.calculate_matrix(switches)
    assert matrix.rows > 0
    assert matrix.cols > 0
    assert matrix.rows * matrix.cols >= len(switches)


def test_pin_assigner():
    """Test pin assignment"""
    assigner = PinAssigner()
    
    # Create matrix
    matrix = Matrix(rows=5, cols=14)
    
    # Assign pins
    matrix = assigner.assign_pins(matrix, MCUType.ATMEGA328P)
    assert len(matrix.row_pins) == 5
    assert len(matrix.col_pins) == 14


def test_layout_presets():
    """Test layout presets"""
    # Test getting a preset
    switches = LayoutPresets.get_preset('60-ansi')
    assert len(switches) > 0
    
    # Test listing presets
    presets = LayoutPresets.list_presets()
    assert '60-ansi' in presets
    assert 'macropad-3x3' in presets


if __name__ == '__main__':
    pytest.main([__file__])
