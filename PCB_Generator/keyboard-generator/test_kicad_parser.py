#!/usr/bin/env python3
"""Test script for KiCad parser."""

from pathlib import Path
from thkg.templates.kicad_parser import parse_kicad_schematic


def test_parse_lumberjack():
    """Test parsing Lumberjack schematic."""
    
    # Path to Lumberjack schematic
    schematic_path = Path("../pcb-library/design-files/lumberjack/kicad/lumberjack.kicad_sch")
    
    if not schematic_path.exists():
        print(f"❌ Schematic not found: {schematic_path}")
        return False
    
    print(f"📄 Parsing: {schematic_path.name}")
    print(f"   Path: {schematic_path}")
    print()
    
    try:
        components, connections = parse_kicad_schematic(schematic_path)
        
        print(f"✅ Parsing successful!")
        print(f"   Components: {len(components)}")
        print(f"   Connections: {len(connections)}")
        print()
        
        # Show component breakdown
        component_types = {}
        for comp in components:
            comp_type = comp.reference[0]
            component_types[comp_type] = component_types.get(comp_type, 0) + 1
        
        print("📦 Component Breakdown:")
        for comp_type, count in sorted(component_types.items()):
            type_name = {
                'U': 'ICs',
                'R': 'Resistors',
                'C': 'Capacitors',
                'D': 'Diodes',
                'J': 'Connectors',
                'SW': 'Switches',
                'Y': 'Crystals',
                'F': 'Fuses',
                'LED': 'LEDs'
            }.get(comp_type, comp_type)
            print(f"   {comp_type}: {count:3d} {type_name}")
        print()
        
        # Show some example components (skip power symbols)
        real_components = [c for c in components if not c.reference.startswith('#')]
        
        print("🔍 Example Components:")
        for comp in real_components[:15]:
            print(f"   {comp.reference:8s} = {comp.value:20s} ({comp.footprint})")
        
        if len(real_components) > 15:
            print(f"   ... and {len(real_components) - 15} more")
        print()
        
        # Show key components
        print("🔑 Key Components:")
        mcu = [c for c in components if 'ATmega' in c.value or 'MCU' in c.symbol]
        if mcu:
            print(f"   MCU: {mcu[0].reference} = {mcu[0].value}")
        
        usb = [c for c in components if 'USB' in c.symbol or 'USB' in c.footprint]
        if usb:
            print(f"   USB: {usb[0].reference} = {usb[0].value}")
        
        crystal = [c for c in components if c.reference.startswith('Y')]
        if crystal:
            print(f"   Crystal: {crystal[0].reference} = {crystal[0].value}")
        
        switches = [c for c in components if c.reference.startswith('MX') or c.reference.startswith('SW')]
        if switches:
            print(f"   Switches: {len(switches)} total")
        
        diodes = [c for c in components if c.reference.startswith('D') and '4148' in c.value]
        if diodes:
            print(f"   Diodes: {len(diodes)} (1N4148)")
        print()
        
        # Show nets
        if connections:
            print(f"🔌 Connections:")
            for conn in connections[:5]:
                print(f"   {conn.net_name}: {len(conn.pins)} pins")
            if len(connections) > 5:
                print(f"   ... and {len(connections) - 5} more")
        else:
            print("ℹ️  No explicit net labels found (connections are implicit in wires)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error parsing schematic: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("KiCad Parser Test")
    print("=" * 60)
    print()
    
    success = test_parse_lumberjack()
    
    print()
    print("=" * 60)
    if success:
        print("✅ Test PASSED")
    else:
        print("❌ Test FAILED")
    print("=" * 60)
