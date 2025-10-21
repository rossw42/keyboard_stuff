#!/usr/bin/env python3
"""Test script for circuit block identifier."""

from pathlib import Path
from thkg.templates.kicad_parser import parse_kicad_schematic
from thkg.templates.identifier import CircuitBlockIdentifier


def test_identify_lumberjack():
    """Test identifying circuit blocks in Lumberjack."""
    
    # Path to Lumberjack schematic
    schematic_path = Path("../pcb-library/design-files/lumberjack/kicad/lumberjack.kicad_sch")
    
    if not schematic_path.exists():
        print(f"❌ Schematic not found: {schematic_path}")
        return False
    
    print(f"📄 Analyzing: {schematic_path.name}")
    print()
    
    try:
        # Parse schematic
        components, connections = parse_kicad_schematic(schematic_path)
        print(f"✅ Parsed {len(components)} components")
        print()
        
        # Identify circuit blocks
        identifier = CircuitBlockIdentifier(components)
        blocks = identifier.identify_all_blocks()
        
        print("🔍 Circuit Blocks Identified:")
        print()
        
        # MCU Block
        if blocks['mcu']:
            print("  🖥️  MCU Block:")
            for comp in blocks['mcu']:
                print(f"     {comp.reference:8s} = {comp.value:20s}")
            print()
        
        # USB Block
        if blocks['usb']:
            print("  🔌 USB Block:")
            for comp in blocks['usb']:
                print(f"     {comp.reference:8s} = {comp.value:20s}")
            print()
        
        # Reset Block
        if blocks['reset']:
            print("  🔄 Reset Block:")
            for comp in blocks['reset']:
                print(f"     {comp.reference:8s} = {comp.value:20s}")
            print()
        
        # Crystal Block
        if blocks['crystal']:
            print("  💎 Crystal Block:")
            for comp in blocks['crystal']:
                print(f"     {comp.reference:8s} = {comp.value:20s}")
            print()
        
        # Power Block
        if blocks['power']:
            print("  ⚡ Power Block:")
            for comp in blocks['power'][:5]:  # Show first 5
                print(f"     {comp.reference:8s} = {comp.value:20s}")
            if len(blocks['power']) > 5:
                print(f"     ... and {len(blocks['power']) - 5} more")
            print()
        
        # Matrix Block
        if blocks['matrix']:
            print(f"  ⌨️  Matrix Block: {len(blocks['matrix'])} components")
            switches = [c for c in blocks['matrix'] if c.reference.startswith('MX')]
            diodes = [c for c in blocks['matrix'] if c.reference.startswith('D')]
            print(f"     Switches: {len(switches)}")
            print(f"     Diodes: {len(diodes)}")
            print()
        
        # LED Block
        if blocks['leds']:
            print("  💡 LED Block:")
            for comp in blocks['leds']:
                print(f"     {comp.reference:8s} = {comp.value:20s}")
            print()
        
        # Summary
        summary = identifier.get_block_summary()
        print("📊 Summary:")
        total = sum(summary.values())
        for block_type, count in summary.items():
            if count > 0:
                print(f"   {block_type:10s}: {count:3d} components")
        print(f"   {'TOTAL':10s}: {total:3d} components")
        print()
        
        # Create templates
        print("🎨 Creating Templates:")
        
        mcu_template = identifier.create_template('mcu', 'atmega328p_circuit', 'lumberjack')
        if mcu_template:
            print(f"   ✅ {mcu_template.name}: {len(mcu_template.components)} components")
        
        usb_template = identifier.create_template('usb', 'usb_c_circuit', 'lumberjack')
        if usb_template:
            print(f"   ✅ {usb_template.name}: {len(usb_template.components)} components")
        
        crystal_template = identifier.create_template('crystal', 'crystal_16mhz', 'lumberjack')
        if crystal_template:
            print(f"   ✅ {crystal_template.name}: {len(crystal_template.components)} components")
        
        reset_template = identifier.create_template('reset', 'reset_circuit', 'lumberjack')
        if reset_template:
            print(f"   ✅ {reset_template.name}: {len(reset_template.components)} components")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Circuit Block Identifier Test")
    print("=" * 60)
    print()
    
    success = test_identify_lumberjack()
    
    print()
    print("=" * 60)
    if success:
        print("✅ Test PASSED")
    else:
        print("❌ Test FAILED")
    print("=" * 60)
