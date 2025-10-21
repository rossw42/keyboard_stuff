#!/usr/bin/env python3
"""Test PCB generation with complete footprints."""

from pathlib import Path
from thkg.config import Configuration
from thkg.pcb.pcb_generator import PCBGenerator


def test_pcb_generation():
    """Test PCB generation with footprint library."""
    print("Testing PCB Generation with Complete Footprints")
    print("=" * 80)
    
    # Create simple test configuration
    print(f"\n📄 Creating test configuration...")
    
    from thkg.config import Switch, Matrix, KeyboardType
    
    # Create a simple 3x3 macropad
    switches = []
    for row in range(3):
        for col in range(3):
            switches.append(Switch(
                row=row,
                col=col,
                x=19.05 * col,  # 19.05mm = 0.75" spacing
                y=19.05 * row,
                width=1.0,
                height=1.0
            ))
    
    config = Configuration(
        name="Test-3x3-Macropad",
        description="Test macropad for footprint library",
        keyboard_type=KeyboardType.MACROPAD,
        switches=switches,
        matrix=Matrix(rows=3, cols=3, diode_direction="COL2ROW")
    )
    
    print(f"   ✅ Created: {config.name}")
    
    # Create output directory
    output_dir = Path("output/test-pcb")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Output directory: {output_dir}")
    
    # Generate PCB
    print("\n🔨 Generating PCB...")
    generator = PCBGenerator(config)
    success = generator.generate(output_dir)
    
    if success:
        print("\n✅ PCB generation successful!")
        
        # Check output files
        pcb_file = output_dir / f"{config.name}.kicad_pcb"
        if pcb_file.exists():
            # Read and analyze PCB file
            with open(pcb_file, 'r') as f:
                content = f.read()
            
            lines = content.count('\n')
            size = len(content)
            
            print(f"\n📊 PCB File Statistics:")
            print(f"   • File: {pcb_file.name}")
            print(f"   • Size: {size:,} bytes")
            print(f"   • Lines: {lines:,}")
            
            # Count footprints
            footprint_count = content.count('(footprint ')
            print(f"   • Footprints: {footprint_count}")
            
            # Count segments
            segment_count = content.count('(segment ')
            print(f"   • Segments: {segment_count}")
            
            # Check for complete footprints (should have fp_line, fp_text, etc.)
            fp_line_count = content.count('(fp_line ')
            fp_text_count = content.count('(fp_text ')
            pad_count = content.count('(pad ')
            
            print(f"\n📊 Footprint Details:")
            print(f"   • fp_line elements: {fp_line_count}")
            print(f"   • fp_text elements: {fp_text_count}")
            print(f"   • Pads: {pad_count}")
            
            # Compare to target
            print(f"\n📈 Comparison to Library PCBs:")
            print(f"   • Target (dumbpad): ~46,803 lines")
            print(f"   • Target (lumberjack): ~77,560 lines")
            print(f"   • Our PCB: {lines:,} lines")
            
            if lines > 5000:
                print(f"   ✅ Good! Much better than previous ~500 lines")
            elif lines > 1000:
                print(f"   ⚠️  Better, but still room for improvement")
            else:
                print(f"   ❌ Still too small - footprints may be incomplete")
            
            # Show sample of footprint
            print(f"\n📝 Sample Footprint (first 500 chars):")
            footprint_start = content.find('(footprint ')
            if footprint_start >= 0:
                sample = content[footprint_start:footprint_start+500]
                print(sample)
        else:
            print(f"   ❌ PCB file not found: {pcb_file}")
    else:
        print("\n❌ PCB generation failed!")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_pcb_generation()
