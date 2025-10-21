#!/usr/bin/env python3
"""Debug footprint reference update."""

from thkg.pcb.footprint_library import FootprintLibrary


def debug():
    """Debug footprint."""
    library = FootprintLibrary()
    
    footprint = library.get_footprint(
        "lumberjack:MX",
        "SW1",
        (50.0, 50.0),
        rotation=90,
        net_map={"1": 1, "2": 2}
    )
    
    if footprint:
        # Print first 500 characters
        print("First 500 characters:")
        print(footprint[:500])
        print("\n" + "=" * 80 + "\n")
        
        # Check for reference
        if 'SW1' in footprint:
            print("✅ 'SW1' found in footprint")
        else:
            print("❌ 'SW1' NOT found in footprint")
        
        # Check for quoted reference
        if '"SW1"' in footprint:
            print("✅ '\"SW1\"' found in footprint")
        else:
            print("❌ '\"SW1\"' NOT found in footprint")
        
        # Find all property references
        import re
        refs = re.findall(r'\(property\s+"Reference"\s+"([^"]*)"', footprint)
        print(f"\nFound {len(refs)} Reference properties:")
        for ref in refs:
            print(f"   • {ref}")


if __name__ == "__main__":
    debug()
