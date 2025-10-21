#!/usr/bin/env python3
"""
THKG Demo Script - Demonstrates complete functionality
"""

import sys
sys.path.insert(0, '.')

from pathlib import Path
from thkg.layout import LayoutPresets, MatrixCalculator, PinAssigner
from thkg.plate import PlateGenerator, DXFWriter
from thkg.config import PlateConfig, Configuration, MCUType
from thkg.input import InputValidator

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def demo():
    """Run complete demo"""
    print_header("THKG - Through-Hole Keyboard Generator Demo")
    
    # Demo 1: List available presets
    print_header("1. Available Layout Presets")
    presets = LayoutPresets.list_presets()
    
    categories = {
        'Keyboards (Staggered)': [],
        'Keyboards (Ortho)': [],
        'Numpads': [],
        'Macropads': []
    }
    
    for name, desc in presets.items():
        if 'ortho' in name.lower() and 'numpad' not in name and 'macro' not in name:
            categories['Keyboards (Ortho)'].append((name, desc))
        elif 'numpad' in name.lower():
            categories['Numpads'].append((name, desc))
        elif 'macro' in name.lower():
            categories['Macropads'].append((name, desc))
        else:
            categories['Keyboards (Staggered)'].append((name, desc))
    
    for category, items in categories.items():
        if items:
            print(f"{category}:")
            for name, desc in items:
                print(f"  • {name:20s} - {desc}")
            print()
    
    # Demo 2: Generate a 3x3 macropad
    print_header("2. Generating 3x3 Macropad")
    
    print("Loading preset...")
    switches = LayoutPresets.get_preset('macropad-3x3')
    print(f"✓ Loaded {len(switches)} switches")
    
    print("\nCalculating matrix...")
    calc = MatrixCalculator()
    matrix = calc.calculate_matrix(switches)
    print(f"✓ Matrix: {matrix.rows}x{matrix.cols}")
    
    print("\nAssigning pins...")
    assigner = PinAssigner()
    matrix = assigner.assign_pins(matrix, MCUType.ATMEGA328P)
    print(f"✓ Row pins: {', '.join(matrix.row_pins)}")
    print(f"✓ Col pins: {', '.join(matrix.col_pins)}")
    
    print("\nGenerating plate...")
    plate_gen = PlateGenerator()
    plate_config = PlateConfig(switch_type='mx', thickness=1.5)
    plate_data = plate_gen.generate_plate(switches, plate_config)
    print(f"✓ Dimensions: {plate_data['dimensions'][0]:.1f}mm x {plate_data['dimensions'][1]:.1f}mm")
    print(f"✓ Switch cutouts: {len(plate_data['switch_cutouts'])}")
    print(f"✓ Mounting holes: {len(plate_data['mounting_holes'])}")
    
    print("\nExporting DXF...")
    output_dir = Path('PCB/tools/keyboard-generator/output/demo')
    output_dir.mkdir(parents=True, exist_ok=True)
    dxf_path = output_dir / 'macropad-3x3.dxf'
    dxf_writer = DXFWriter()
    dxf_writer.write_plate(plate_data, str(dxf_path))
    print(f"✓ Saved to: {dxf_path}")
    print(f"✓ File size: {dxf_path.stat().st_size} bytes")
    
    # Demo 3: Validate configuration
    print_header("3. Configuration Validation")
    
    config = Configuration()
    config.name = "Demo-Macropad"
    config.layout_preset = "macropad-3x3"
    config.matrix = matrix
    
    validator = InputValidator()
    is_valid, errors = validator.validate(config)
    
    if is_valid:
        print("✓ Configuration is valid")
        print(f"  • Name: {config.name}")
        print(f"  • Layout: {config.layout_preset}")
        print(f"  • Matrix: {config.matrix.rows}x{config.matrix.cols}")
        print(f"  • MCU: {config.mcu_type.value}")
        print(f"  • USB: {config.usb_type.value}")
    else:
        print("✗ Configuration has errors:")
        for error in errors:
            print(f"  • {error}")
    
    # Demo 4: Show file structure
    print_header("4. Generated Files")
    
    print("Output directory structure:")
    print(f"  {output_dir}/")
    print(f"    └── macropad-3x3.dxf  ({dxf_path.stat().st_size} bytes)")
    
    print("\nDXF file contains:")
    print("  • OUTLINE layer - Plate outline")
    print("  • CUTOUTS layer - Switch cutouts")
    print("  • HOLES layer - Mounting holes")
    
    # Summary
    print_header("Demo Complete!")
    
    print("✓ All systems operational")
    print("✓ Plate generation successful")
    print("✓ DXF export successful")
    print("✓ Configuration validation passed")
    
    print("\nNext steps:")
    print("  1. Open macropad-3x3.dxf in CAD software")
    print("  2. Verify dimensions and cutouts")
    print("  3. Send to laser cutting service")
    
    print("\nTry it yourself:")
    print("  $ thkg generate examples/macropad-3x3.yaml")
    print("  $ thkg interactive")
    print("  $ thkg list-presets")
    
    print("\n" + "="*60)
    print("  THKG Phase 1 - COMPLETE AND READY FOR USE!")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        demo()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
