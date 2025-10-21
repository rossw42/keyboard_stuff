#!/usr/bin/env python3
"""Test complete plate generation"""

import sys
sys.path.insert(0, '.')

from pathlib import Path
from thkg.layout import LayoutPresets
from thkg.plate import PlateGenerator, DXFWriter
from thkg.config import PlateConfig

def test_generate_plate():
    """Test generating a complete plate DXF file"""
    print("Generating test plate...\n")
    
    # Load preset
    print("1. Loading macropad-3x3 preset...")
    switches = LayoutPresets.get_preset('macropad-3x3')
    print(f"   ✓ Loaded {len(switches)} switches")
    
    # Generate plate
    print("2. Generating plate design...")
    plate_gen = PlateGenerator()
    plate_config = PlateConfig(switch_type='mx', thickness=1.5)
    plate_data = plate_gen.generate_plate(switches, plate_config)
    print(f"   ✓ Generated plate: {plate_data['dimensions'][0]:.1f}mm x {plate_data['dimensions'][1]:.1f}mm")
    
    # Write DXF
    print("3. Writing DXF file...")
    output_dir = Path('PCB/tools/keyboard-generator/output/test')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    dxf_path = output_dir / 'test_plate.dxf'
    dxf_writer = DXFWriter()
    dxf_writer.write_plate(plate_data, str(dxf_path))
    print(f"   ✓ Saved to: {dxf_path}")
    
    # Verify file exists
    if dxf_path.exists():
        size = dxf_path.stat().st_size
        print(f"   ✓ File size: {size} bytes")
        print("\n✓ Plate generation successful!")
        return True
    else:
        print("   ✗ File not created")
        return False

if __name__ == '__main__':
    success = test_generate_plate()
    sys.exit(0 if success else 1)
