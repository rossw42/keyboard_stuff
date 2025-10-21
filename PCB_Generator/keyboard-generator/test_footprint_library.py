#!/usr/bin/env python3
"""Test footprint library functionality."""

from thkg.pcb.footprint_library import FootprintLibrary
from pathlib import Path


def test_library():
    """Test footprint library."""
    print("Testing Footprint Library")
    print("=" * 80)
    
    # Initialize library
    library = FootprintLibrary()
    
    # Test 1: Find MX switch footprint
    print("\n1. Finding MX switch footprint...")
    mx_path = library.find_footprint("lumberjack:MX")
    if mx_path:
        print(f"   ✅ Found: {mx_path}")
        content = library.load_footprint(mx_path)
        if content:
            print(f"   ✅ Loaded: {len(content)} characters")
            print(f"   📊 Lines: {content.count(chr(10))}")
    else:
        print("   ❌ Not found")
    
    # Test 2: Find diode footprint
    print("\n2. Finding diode footprint...")
    diode_path = library.find_footprint("Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal")
    if diode_path:
        print(f"   ✅ Found: {diode_path}")
        content = library.load_footprint(diode_path)
        if content:
            print(f"   ✅ Loaded: {len(content)} characters")
            print(f"   📊 Lines: {content.count(chr(10))}")
    else:
        print("   ❌ Not found")
    
    # Test 3: Find by type
    print("\n3. Finding footprints by type...")
    types = ['switch', 'diode', 'resistor', 'capacitor', 'mcu', 'crystal', 'led']
    for comp_type in types:
        path = library.find_by_type(comp_type)
        if path:
            print(f"   ✅ {comp_type:12s}: {path}")
        else:
            print(f"   ❌ {comp_type:12s}: Not found")
    
    # Test 4: Get complete footprint with updates
    print("\n4. Getting complete footprint with position update...")
    footprint = library.get_footprint(
        "lumberjack:MX",
        "SW1",
        (50.0, 50.0),
        rotation=90,
        net_map={"1": 1, "2": 2}
    )
    
    if footprint:
        print(f"   ✅ Generated footprint: {len(footprint)} characters")
        print(f"   📊 Lines: {footprint.count(chr(10))}")
        
        # Check if position was updated
        if "(at 50.0 50.0 90)" in footprint:
            print("   ✅ Position updated correctly")
        else:
            print("   ⚠️  Position may not be updated correctly")
        
        # Check if reference was updated
        if '"SW1"' in footprint:
            print("   ✅ Reference updated correctly")
        else:
            print("   ⚠️  Reference may not be updated correctly")
    else:
        print("   ❌ Failed to generate footprint")
    
    # Test 5: Library statistics
    print("\n5. Library statistics...")
    total = library._count_footprints()
    print(f"   📊 Total footprints: {total}")
    print(f"   📊 Sources: {len(library.index)}")
    for source, footprints in library.index.items():
        print(f"      • {source}: {len(footprints)} footprints")
    
    print("\n" + "=" * 80)
    print("✅ Footprint library test complete!")


if __name__ == "__main__":
    test_library()
