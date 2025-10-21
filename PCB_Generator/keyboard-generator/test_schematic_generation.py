#!/usr/bin/env python3
"""Test schematic generation."""

from pathlib import Path
from thkg.config import Configuration
from thkg.pcb.schematic import SchematicGenerator


def main():
    """Test schematic generation."""
    
    print("=" * 80)
    print("Schematic Generation Test")
    print("=" * 80)
    print()
    
    # Create test configuration
    config = Configuration()
    config.keyboard = {
        'name': 'Test Keyboard',
        'description': 'Test 60% keyboard',
        'version': '1.0',
    }
    config.layout = {
        'type': '60-ansi',
        'switches': [{'row': i // 14, 'col': i % 14} for i in range(60)],
    }
    config.hardware = {
        'mcu': {
            'type': 'atmega328p',
        },
    }
    
    # Generate schematic
    generator = SchematicGenerator(config)
    
    output_path = Path("output/test-keyboard/test-keyboard.kicad_sch")
    
    success = generator.generate(output_path)
    
    print()
    print("=" * 80)
    
    if success and output_path.exists():
        print("✅ Schematic generated successfully!")
        print(f"📁 Output: {output_path}")
        print(f"📊 File size: {output_path.stat().st_size} bytes")
        
        # Show first few lines
        print()
        print("📄 First 20 lines:")
        with open(output_path, 'r') as f:
            for i, line in enumerate(f):
                if i >= 20:
                    break
                print(f"   {line.rstrip()}")
        
        print("   ...")
        
        return True
    else:
        print("❌ Schematic generation failed!")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
