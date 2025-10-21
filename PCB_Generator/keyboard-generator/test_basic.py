#!/usr/bin/env python3
"""Basic functionality test"""

import sys
sys.path.insert(0, '.')

from thkg.config import Configuration, Switch
from thkg.layout import LayoutPresets, MatrixCalculator, PinAssigner
from thkg.plate import PlateGenerator
from thkg.input import InputValidator

def test_basic():
    """Test basic functionality"""
    print("Testing THKG basic functionality...\n")
    
    # Test 1: Load a preset
    print("1. Loading 3x3 macropad preset...")
    switches = LayoutPresets.get_preset('macropad-3x3')
    print(f"   ✓ Loaded {len(switches)} switches")
    
    # Test 2: Calculate matrix
    print("2. Calculating matrix...")
    calc = MatrixCalculator()
    matrix = calc.calculate_matrix(switches)
    print(f"   ✓ Matrix: {matrix.rows}x{matrix.cols}")
    
    # Test 3: Assign pins
    print("3. Assigning pins...")
    from thkg.config import MCUType
    assigner = PinAssigner()
    matrix = assigner.assign_pins(matrix, MCUType.ATMEGA328P)
    print(f"   ✓ Assigned {len(matrix.row_pins)} row pins, {len(matrix.col_pins)} col pins")
    
    # Test 4: Generate plate
    print("4. Generating plate...")
    from thkg.config import PlateConfig
    plate_gen = PlateGenerator()
    plate_config = PlateConfig()
    plate_data = plate_gen.generate_plate(switches, plate_config)
    print(f"   ✓ Plate dimensions: {plate_data['dimensions'][0]:.1f}mm x {plate_data['dimensions'][1]:.1f}mm")
    print(f"   ✓ Switch cutouts: {len(plate_data['switch_cutouts'])}")
    
    # Test 5: Validate configuration
    print("5. Validating configuration...")
    config = Configuration()
    config.name = "Test"
    config.layout_preset = "macropad-3x3"
    config.matrix = matrix
    
    validator = InputValidator()
    is_valid, errors = validator.validate(config)
    if is_valid:
        print("   ✓ Configuration valid")
    else:
        print(f"   ✗ Validation errors: {errors}")
        return False
    
    print("\n✓ All basic tests passed!")
    return True

if __name__ == '__main__':
    success = test_basic()
    sys.exit(0 if success else 1)
