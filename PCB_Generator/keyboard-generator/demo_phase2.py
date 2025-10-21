#!/usr/bin/env python3
"""Phase 2 Demo - Generate multiple keyboard schematics."""

from pathlib import Path
from thkg.config import Configuration
from thkg.pcb.schematic import SchematicGenerator


def generate_60_percent():
    """Generate 60% keyboard schematic."""
    print("\n" + "=" * 80)
    print("Generating 60% Keyboard")
    print("=" * 80)
    
    config = Configuration()
    config.keyboard = {
        'name': '60-Percent-Keyboard',
        'description': 'Standard 60% ANSI layout',
        'version': '1.0',
    }
    config.layout = {
        'type': '60-ansi',
        'switches': [{'row': i // 14, 'col': i % 14} for i in range(61)],
    }
    config.hardware = {
        'mcu': {'type': 'atmega328p'},
    }
    
    generator = SchematicGenerator(config)
    output_path = Path("output/60-percent/60-percent.kicad_sch")
    generator.generate(output_path)
    
    return output_path


def generate_macropad():
    """Generate 3x3 macropad schematic."""
    print("\n" + "=" * 80)
    print("Generating 3x3 Macropad")
    print("=" * 80)
    
    config = Configuration()
    config.keyboard = {
        'name': '3x3-Macropad',
        'description': '3x3 macropad',
        'version': '1.0',
    }
    config.layout = {
        'type': 'macropad-3x3',
        'switches': [{'row': i // 3, 'col': i % 3} for i in range(9)],
    }
    config.hardware = {
        'mcu': {'type': 'pro_micro'},
    }
    
    generator = SchematicGenerator(config)
    output_path = Path("output/3x3-macropad/3x3-macropad.kicad_sch")
    generator.generate(output_path)
    
    return output_path


def generate_40_percent():
    """Generate 40% keyboard schematic."""
    print("\n" + "=" * 80)
    print("Generating 40% Keyboard")
    print("=" * 80)
    
    config = Configuration()
    config.keyboard = {
        'name': '40-Percent-Keyboard',
        'description': '40% ortholinear layout',
        'version': '1.0',
    }
    config.layout = {
        'type': '40-ortho',
        'switches': [{'row': i // 12, 'col': i % 12} for i in range(48)],
    }
    config.hardware = {
        'mcu': {'type': 'atmega328p'},
    }
    
    generator = SchematicGenerator(config)
    output_path = Path("output/40-percent/40-percent.kicad_sch")
    generator.generate(output_path)
    
    return output_path


def main():
    """Run demo."""
    print("=" * 80)
    print("THKG Phase 2 Demo - Schematic Generation")
    print("=" * 80)
    
    generated_files = []
    
    # Generate different keyboard types
    try:
        generated_files.append(generate_60_percent())
    except Exception as e:
        print(f"❌ Error generating 60%: {e}")
    
    try:
        generated_files.append(generate_macropad())
    except Exception as e:
        print(f"❌ Error generating macropad: {e}")
    
    try:
        generated_files.append(generate_40_percent())
    except Exception as e:
        print(f"❌ Error generating 40%: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("Demo Complete")
    print("=" * 80)
    print()
    print(f"✅ Generated {len(generated_files)} schematics:")
    for path in generated_files:
        if path.exists():
            size = path.stat().st_size
            print(f"   • {path} ({size} bytes)")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
