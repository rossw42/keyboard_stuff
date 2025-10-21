#!/usr/bin/env python3
"""Regenerate PCB files with complete footprint definitions."""

from pathlib import Path
from thkg.config import Configuration
from thkg.pcb.pcb_generator import PCBGenerator


def regenerate_3x3_macropad():
    """Regenerate 3x3 macropad with complete PCB."""
    print("\n" + "="*80)
    print("Regenerating 3x3 Macropad PCB")
    print("="*80 + "\n")
    
    # Configuration
    from thkg.config import Matrix, MCUType, USBType, KeyboardType
    
    config = Configuration(
        name='3x3-Macropad',
        keyboard_type=KeyboardType.MACROPAD,
        mcu_type=MCUType.ATMEGA328P,
        usb_type=USBType.USB_C_THT,
        matrix=Matrix(rows=3, cols=3)
    )
    
    # Generate PCB
    generator = PCBGenerator(config)
    output_dir = Path('output/3x3-complete')
    generator.generate(output_dir)
    
    print(f"\n✅ Generated: {output_dir}")
    print(f"   • {output_dir}/3x3-Macropad.kicad_sch")
    print(f"   • {output_dir}/3x3-Macropad.kicad_pcb")


def regenerate_4x4_macropad():
    """Regenerate 4x4 macropad with complete PCB."""
    print("\n" + "="*80)
    print("Regenerating 4x4 Macropad PCB")
    print("="*80 + "\n")
    
    # Configuration
    from thkg.config import Matrix, MCUType, USBType, KeyboardType
    
    config = Configuration(
        name='4x4-Macropad',
        keyboard_type=KeyboardType.MACROPAD,
        mcu_type=MCUType.ATMEGA328P,
        usb_type=USBType.USB_C_THT,
        matrix=Matrix(rows=4, cols=4)
    )
    
    # Generate PCB
    generator = PCBGenerator(config)
    output_dir = Path('output/4x4-complete')
    generator.generate(output_dir)
    
    print(f"\n✅ Generated: {output_dir}")
    print(f"   • {output_dir}/4x4-Macropad.kicad_sch")
    print(f"   • {output_dir}/4x4-Macropad.kicad_pcb")


if __name__ == '__main__':
    print("\n🔧 PCB Regeneration Tool")
    print("="*80)
    print("This will regenerate PCB files with complete footprint definitions")
    print("="*80)
    
    regenerate_3x3_macropad()
    regenerate_4x4_macropad()
    
    print("\n" + "="*80)
    print("✅ All PCBs regenerated successfully!")
    print("="*80)
    print("\nYou can now open these files in KiCad or an online viewer:")
    print("  • output/3x3-complete/3x3-Macropad.kicad_pcb")
    print("  • output/4x4-complete/4x4-Macropad.kicad_pcb")
    print()
