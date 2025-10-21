#!/usr/bin/env python3
"""Complete THKG Demo - Generate full keyboard PCBs."""

from pathlib import Path
from thkg.config import Configuration
from thkg.pcb.pcb_generator import PCBGenerator


def generate_complete_60_percent():
    """Generate complete 60% keyboard PCB."""
    config = Configuration()
    config.keyboard = {
        'name': '60-percent-complete',
        'description': 'Complete 60% keyboard with PCB layout',
        'version': '1.0',
    }
    config.layout = {
        'type': '60-ansi',
        'switches': [{'row': i // 14, 'col': i % 14} for i in range(61)],
    }
    config.hardware = {
        'mcu': {'type': 'atmega328p'},
    }
    
    generator = PCBGenerator(config)
    generator.generate(Path("output/60-percent-complete"))


def generate_complete_macropad():
    """Generate complete macropad PCB."""
    config = Configuration()
    config.keyboard = {
        'name': '4x4-macropad',
        'description': 'Complete 4x4 macropad with PCB layout',
        'version': '1.0',
    }
    config.layout = {
        'type': 'macropad-4x4',
        'switches': [{'row': i // 4, 'col': i % 4} for i in range(16)],
    }
    config.hardware = {
        'mcu': {'type': 'pro_micro'},
    }
    
    generator = PCBGenerator(config)
    generator.generate(Path("output/4x4-macropad"))


def main():
    """Run complete demo."""
    print("\n" + "="*80)
    print("THKG Complete Demo - Full PCB Generation")
    print("="*80)
    print("\nGenerating complete keyboard PCBs with:")
    print("  • Schematics")
    print("  • Component placement")
    print("  • Trace routing")
    print("  • PCB layout files")
    print("\n" + "="*80 + "\n")
    
    # Generate keyboards
    generate_complete_60_percent()
    generate_complete_macropad()
    
    # Final summary
    print("\n" + "="*80)
    print("🎉 Demo Complete!")
    print("="*80)
    print("\nGenerated complete PCBs:")
    print("  • 60% keyboard (61 keys)")
    print("  • 4x4 macropad (16 keys)")
    print("\nEach includes:")
    print("  ✅ KiCad schematic (.kicad_sch)")
    print("  ✅ KiCad PCB layout (.kicad_pcb)")
    print("  ✅ Component placement")
    print("  ✅ Trace routing")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
