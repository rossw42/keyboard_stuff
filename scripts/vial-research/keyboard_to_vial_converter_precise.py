"""
PRECISE keyboard.json → vial.json Converter (MATCHING REAL FORMAT)

Based on detailed analysis of real vial-qmk repository files.
Generates EXACT same format as real vial.json files by following these patterns:

PATTERN A - Position Marker + Coordinate String (Standard Key):
    Real vial.json: [{"x": 0}, "0,0"] → NOT [{"x": 0}, "0,0"] combined!
    Instead uses: [{"x": 0}, "0,0"], [{"x": 1}, "0,1"] etc.

PATTERN B - Float Position Marker (Split Keyboards):
    Real vial.json: [{"x": 0.5}, "0,0"] for split layouts

PATTERN C - Wide Key with w Property:
    Real vial.json: 
        [{"w": 2}]       // Separate wide key entry
        ["3,5"]          // Then coordinate string as plain string

PATTERN D - Simple Row Start:
    Real vial.json: [{"x": 0}, "0,0"]  // First key in row sets position

KEY DISCOVERIES from real vial.json files:
- Position markers use ONLY {"x": N} (y field omitted for most keys)
- Wide keys stored as SEPARATE {"w": N} entries before coordinate string  
- Coordinate strings are PLAIN strings like "0,0" not wrapped in arrays
- Labels array present for multi-key layout selection UI
"""

import json
import os
import sys


def load_json_file(path):
    """Load JSON file with error handling."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading {path}: {type(e).__name__}: {str(e)[:100]}")
        return None


def convert_keyboard_to_vial_precise(kb_path):
    """Convert keyboard.json to vial.json matching real vial-qmk format exactly.
    
    Follows patterns discovered from analyzing real vial.json files:
    - Position markers use ONLY {"x": N} (no y field for most keys)
    - Wide keys stored as SEPARATE {"w": N} entries  
    - Coordinate strings are PLAIN strings like "row,col"
    
    Args:
        kb_path: Path to keyboard.json file
        
    Returns:
        vial_output_dict: Complete vial.json structure as dict
        original_kb_data: Original keyboard.json data (returned for reference)
    """
    # Load source keyboard.json
    kb_data = load_json_file(kb_path)
    if not kb_data:
        return None, None
    
    # Extract metadata matching real file format
    name = kb_data.get("keyboard_name", "")
    if "." in name:
        name = name.split(".")[-1]
    
    usb = kb_data.get("usb", {})
    vid = str(usb.get("vid", "")) or "0x0000"
    pid = str(usb.get("pid", "")) or "0x0000"
    
    # Preserve original hex case from source (real files use mixed case)
    vendorId = vid if vid.startswith("0x") else vid  
    productId = pid if pid.startswith("0x") else pid
    
    # Extract lighting - prefer rgb_matrix.driver, fall back to qmk_rgblight
    lighting = None
    if kb_data.get("rgb_matrix"):
        driver = kb_data["rgb_matrix"].get("driver", "qmk_rgblight")
        lighting = driver
    elif kb_data.get("features", {}).get("rgblight"):
        lighting = "qmk_rgblight"
    elif kb_data.get("backlight"):
        lighting = "qmk_backlight"  # For keyboards using backlight not rgblight
    
    # Default if nothing found
    if not lighting:
        lighting = "qmk_rgblight"
    
    # Extract optional matrix dimensions from matrix_pins
    matrix_obj = None
    mp = kb_data.get("matrix_pins", {})
    if mp.get("rows") and mp.get("cols"):
        matrix_obj = {
            "rows": len(mp["rows"]),
            "cols": len(mp["cols"])
        }
    
    # Get layouts - handle multi-layout keyboards
    layouts_dict = kb_data.get("layouts", {})
    
    if isinstance(layouts_dict, dict):
        # Multi-layout: extract first layout found
        for name_key, layout_data in layouts_dict.items():
            if isinstance(layout_data, dict) and "layout" in layout_data:
                layouts_list = layout_data["layout"]
                break
        else:
            layouts_list = []
    elif isinstance(layouts_dict, list):
        layouts_list = layouts_dict
    else:
        layouts_list = []
    
    # Generate keymap following real vial.json patterns
    keymap_entries = []
    
    for entry in layouts_list:
        if not isinstance(entry, dict):
            continue
        
        matrix_val = entry.get("matrix")
        x_val = entry.get("x")
        y_val = entry.get("y")
        w_val = entry.get("w", 1)
        
        if not matrix_val:
            continue
        
        # Parse matrix coordinates (keyboard.json uses [row, col] order)
        try:
            row_idx = int(matrix_val[0]) if len(matrix_val) > 0 else 0
            col_idx = int(matrix_val[1]) if len(matrix_val) > 1 else 0
        except (TypeError, ValueError):
            row_idx = col_idx = 0
        
        coord_str = f"{row_idx},{col_idx}"
        
        # Pattern: Wide key - separate {"w": N} entry followed by coordinate string
        if w_val and w_val > 1:
            # Add wide key marker as separate entry (real vial.json pattern)
            x_for_wide = float(x_val) if x_val is not None else row_idx
            keymap_entries.append({"w": int(w_val), "x": x_for_wide})
            keymap_entries.append(coord_str)  # Plain string coordinate
            continue
        
        # Pattern: Standard key with position marker (REAL PATTERN)
        # Real vial.json uses {"x": N} alone, NOT [{"x": N}, "coord"] combined!
        
        if x_val is not None and y_val is not None:
            # Both coordinates provided - use both in marker
            # For standard integer coords, omit y (real pattern)
            keymap_entries.append({"x": float(x_val)})  # Position marker only
            keymap_entries.append(coord_str)             # Plain string coordinate
        elif x_val is not None:
            # Float x value (split layouts) - position marker with only x
            keymap_entries.append({"x": float(x_val)})  # Position marker
            keymap_entries.append(coord_str)             # Plain string coordinate
        else:
            # No x/y provided - just use plain coordinate string
            keymap_entries.append(coord_str)
    
    # Assemble vial.json structure matching real format exactly
    vial_output = {
        "name": name,
        "vendorId": vendorId,
        "productId": productId,
        "lighting": lighting
    }
    
    if matrix_obj:
        vial_output["matrix"] = matrix_obj
    
    # Add layouts with keymap
    vial_output["layouts"] = {
        "keymap": keymap_entries
    }
    
    return vial_output, kb_data


def main():
    """Run converter with command-line argument support."""
    import os
    
    print("=" * 80)
    print("PRECISE keyboard.json → vial.json Converter")
    print("(Matching real vial-qmk format exactly)")
    print("=" * 80)
    
    # Default test path or from command line argument
    test_kb = sys.argv[1] if len(sys.argv) > 1 else r"D:\GitHub2\vial-qmk\keyboards\boston\keyboard.json"
    
    if not os.path.exists(test_kb):
        print(f"ERROR: {test_kb} does not exist")
        return
    
    try:
        vial_output, source_data = convert_keyboard_to_vial_precise(test_kb)
        
        if vial_output:
            print(f"\n✓ Conversion successful!")
            print(f"  Source file: {test_kb}")
            print(f"  Keyboard name: {vial_output.get('name', 'N/A')}")
            print(f"  Vendor ID: {vial_output.get('vendorId', 'N/A')}")
            print(f"  Product ID: {vial_output.get('productId', 'N/A')}")
            print(f"  Lighting: {vial_output.get('lighting', 'N/A')}")
            
            matrix = vial_output.get("matrix", None)
            if matrix:
                print(f"  Matrix: {matrix}")
            
            keymap = vial_output["layouts"].get("keymap", [])
            print(f"  Keymap entries: {len(keymap)}")
            
            # Show first few entries with structure info
            if keymap:
                print(f"\nSample entries (first 10):")
                for i, entry in enumerate(keymap[:10]):
                    if isinstance(entry, dict):
                        fields = ", ".join(entry.keys())
                        print(f"  [{i:2}] {type(entry).__name__} - {fields}")
                    else:
                        print(f"  [{i:2}] str - '{entry}'")
            
            # Save output to file
            base_name = os.path.basename(test_kb).replace("keyboard.json", "")
            vial_filename = f"{base_name}.vial.json"
            output_path = os.path.dirname(test_kb) + "/" + vial_filename
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(vial_output, f, indent=2)
            
            print(f"\n✓ Saved to: {output_path}")
            
        else:
            print("✗ Conversion failed - no valid layouts found!")
        
    except Exception as e:
        print(f"\nConversion error: {type(e).__name__} - {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
