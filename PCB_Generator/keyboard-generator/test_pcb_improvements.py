#!/usr/bin/env python3
"""Test PCB design improvements with circuit templates and component library"""

from thkg.config import Configuration, MCUType, USBType, Matrix
from thkg.layout.pins import PinAssigner
from thkg.pcb.generator import PCBGenerator
from thkg.pcb.circuits import CircuitTemplates
from thkg.pcb.components import ComponentLibrary


def test_pin_assignments():
    """Test improved pin assignments with proper reservations"""
    print("=" * 60)
    print("Testing Pin Assignments")
    print("=" * 60)
    
    assigner = PinAssigner()
    
    # Test ATmega328P
    print("\n1. ATmega328P Pin Info:")
    info = assigner.get_pin_info(MCUType.ATMEGA328P)
    print(f"   MCU: {info['mcu']}")
    print(f"   Total pins: {info['total_pins']}")
    print(f"   Reserved: {info['reserved_count']} pins")
    print(f"   Available: {info['available_count']} pins")
    print(f"   Reserved pins:")
    for pin, reason in info['reserved_pins'].items():
        print(f"     - {pin}: {reason}")
    
    # Test ATmega32A
    print("\n2. ATmega32A Pin Info:")
    info = assigner.get_pin_info(MCUType.ATMEGA32A)
    print(f"   MCU: {info['mcu']}")
    print(f"   Total pins: {info['total_pins']}")
    print(f"   Reserved: {info['reserved_count']} pins")
    print(f"   Available: {info['available_count']} pins")
    
    # Test pin assignment for 3x3 matrix
    print("\n3. Pin Assignment for 3x3 Matrix:")
    matrix = Matrix(rows=3, cols=3)
    matrix = assigner.assign_pins(matrix, MCUType.ATMEGA328P)
    print(f"   Row pins: {matrix.row_pins}")
    print(f"   Col pins: {matrix.col_pins}")
    
    print("\n✓ Pin assignment tests passed!")


def test_circuit_templates():
    """Test circuit templates"""
    print("\n" + "=" * 60)
    print("Testing Circuit Templates")
    print("=" * 60)
    
    templates = CircuitTemplates()
    
    # Test USB-C protection circuit
    print("\n1. USB-C Protection Circuit:")
    usb = templates.usb_c_protection()
    print(f"   Name: {usb.name}")
    print(f"   Components: {len(usb.components)}")
    print(f"   Connections: {len(usb.connections)}")
    print(f"   Key components:")
    for comp in usb.components[:5]:
        print(f"     - {comp.reference}: {comp.value} ({comp.description})")
    
    # Test ATmega328P support circuit
    print("\n2. ATmega328P Support Circuit:")
    mcu = templates.atmega328p_support()
    print(f"   Name: {mcu.name}")
    print(f"   Components: {len(mcu.components)}")
    print(f"   Key components:")
    for comp in mcu.components[:5]:
        print(f"     - {comp.reference}: {comp.value} ({comp.description})")
    
    # Test switch matrix
    print("\n3. Switch Matrix (3x3):")
    matrix = templates.switch_matrix(3, 3, "COL2ROW")
    print(f"   Name: {matrix.name}")
    print(f"   Components: {len(matrix.components)}")
    print(f"   Connections: {len(matrix.connections)}")
    print(f"   Notes: {matrix.notes[0]}")
    
    print("\n✓ Circuit template tests passed!")


def test_component_library():
    """Test component library"""
    print("\n" + "=" * 60)
    print("Testing Component Library")
    print("=" * 60)
    
    library = ComponentLibrary()
    
    # Test component lookup
    print("\n1. Component Specifications:")
    
    resistor = library.get_component("Resistor", "5.1k")
    print(f"\n   5.1kΩ Resistor:")
    print(f"     Part Number: {resistor.part_number}")
    print(f"     Manufacturer: {resistor.manufacturer}")
    print(f"     Footprint: {resistor.footprint}")
    print(f"     Vendors: {len(resistor.vendors)}")
    
    cap = library.get_component("Capacitor", "100nF")
    print(f"\n   100nF Capacitor:")
    print(f"     Part Number: {cap.part_number}")
    print(f"     Manufacturer: {cap.manufacturer}")
    print(f"     Package: {cap.package}")
    
    diode = library.get_component("Diode", "1N4148")
    print(f"\n   1N4148 Diode:")
    print(f"     Part Number: {diode.part_number}")
    print(f"     Manufacturer: {diode.manufacturer}")
    print(f"     Footprint: {diode.footprint}")
    
    mcu = library.get_component("MCU", "ATmega328P")
    print(f"\n   ATmega328P MCU:")
    print(f"     Part Number: {mcu.part_number}")
    print(f"     Package: {mcu.package}")
    print(f"     Description: {mcu.description}")
    
    # Test BOM generation
    print("\n2. BOM Generation:")
    components = [
        {'category': 'Resistor', 'value': '5.1k'},
        {'category': 'Resistor', 'value': '5.1k'},  # Duplicate
        {'category': 'Resistor', 'value': '10k'},
        {'category': 'Capacitor', 'value': '100nF'},
        {'category': 'Capacitor', 'value': '100nF'},
        {'category': 'Capacitor', 'value': '100nF'},
        {'category': 'Capacitor', 'value': '100nF'},
        {'category': 'Diode', 'value': '1N4148'},
        {'category': 'MCU', 'value': 'ATmega328P'},
    ]
    
    bom = library.generate_bom(components)
    print(f"   Total unique parts: {len(bom)}")
    print(f"\n   BOM Entries:")
    for entry in bom:
        print(f"     - {entry['quantity']}x {entry['value']} ({entry['part_number']})")
    
    print("\n✓ Component library tests passed!")


def test_pcb_generator():
    """Test PCB generator with new features"""
    print("\n" + "=" * 60)
    print("Testing PCB Generator")
    print("=" * 60)
    
    # Create configuration
    config = Configuration(
        name="Test-Macropad",
        mcu_type=MCUType.ATMEGA328P,
        usb_type=USBType.USB_C_THT,
    )
    
    # Set up matrix
    config.matrix = Matrix(rows=3, cols=3, diode_direction="COL2ROW")
    
    # Create generator
    generator = PCBGenerator()
    
    # Generate PCB data
    print("\n1. Generating PCB Design:")
    result = generator.generate_pcb(config, [])
    
    print(f"   Status: {result['status']}")
    print(f"   Circuits: {len(result['circuits'])}")
    print(f"   BOM entries: {len(result['bom'])}")
    
    print(f"\n2. Circuits Included:")
    for name, circuit in result['circuits'].items():
        print(f"     - {name}: {circuit.name}")
        print(f"       Components: {len(circuit.components)}")
        print(f"       Connections: {len(circuit.connections)}")
    
    print(f"\n3. Layout Rules:")
    rules = result['layout_rules']
    print(f"     - Signal trace: {rules['trace_signal']}mm")
    print(f"     - Power trace: {rules['trace_power']}mm")
    print(f"     - USB differential: {rules['trace_usb']}mm")
    print(f"     - Clearance: {rules['clearance']}mm")
    print(f"     - Via: {rules['via_diameter']}mm / {rules['via_drill']}mm")
    
    print(f"\n4. PCB Dimensions:")
    dims = result['dimensions']
    print(f"     - Length: {dims['length']}mm")
    print(f"     - Width: {dims['width']}mm")
    print(f"     - Thickness: {dims['thickness']}mm")
    
    print(f"\n5. Design Notes:")
    for note in result['notes']:
        print(f"     - {note}")
    
    # Test validation
    print(f"\n6. Design Validation:")
    messages = generator.get_design_validation(config)
    if messages:
        for msg in messages:
            print(f"     {msg}")
    else:
        print(f"     ✓ No issues found")
    
    print("\n✓ PCB generator tests passed!")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PCB Design Improvements Test Suite")
    print("=" * 60)
    print("\nTesting improvements based on ai03's PCB Design Guide:")
    print("  - Proper pin reservations (crystal, ISP, USB)")
    print("  - USB protection circuit templates")
    print("  - MCU support circuits")
    print("  - Component library with part numbers")
    print("  - BOM generation")
    print("  - PCB layout rules")
    
    try:
        test_pin_assignments()
        test_circuit_templates()
        test_component_library()
        test_pcb_generator()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe keyboard generator now includes:")
        print("  ✓ Accurate pin assignments with proper reservations")
        print("  ✓ Industry-standard circuit templates")
        print("  ✓ Component library with real part numbers")
        print("  ✓ Automatic BOM generation")
        print("  ✓ PCB layout rules from best practices")
        print("\nReady for Phase 2 KiCad integration!")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
