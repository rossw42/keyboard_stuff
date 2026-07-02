"""
keyboard.json → vial.json Converter (Real Format Implementation)
Converts keyboard.json layouts to PROPER vial.json format matching real vial-qmk repo patterns.

REAL FORMAT - Alps64 shows: [[marker], ["coord"], [marker2], ["coord2"]] as nested lists!
Example: keymap = [[{"x": 0}, "3,6"], [{"x": 1}, "3,7"]] (nested structure!)
"""

import json


def load_json_file(path):
    """Load a JSON file from disk with UTF-8 encoding."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("ERROR loading {}: {}: {}".format(path, type(e).__name__, str(e)[:100]))
        return None


def extract_metadata(kb_data):
    """Extract vial.json metadata from keyboard.json."""
    raw_name = kb_data.get("keyboard_name", "")
    if "." in raw_name:
        name = raw_name.split(".")[-1]
    else:
        name = raw_name
    
    usb = kb_data.get("usb", {})
    vid = str(usb.get("vid", "")) or "0x0000"
    pid = str(usb.get("pid", "")) or "0x0000"
    
    vendorId = vid.lower() if vid else "0x0000"
    productId = pid.lower() if pid else "0x0000"
    
    lighting = None
    if kb_data.get("rgb_matrix"):
        lighting = str(kb_data["rgb_matrix"].get("driver", "qmk_rgblight"))
    elif kb_data.get("features", {}).get("rgblight"):
        lighting = "qmk_rgblight"
    
    if not lighting:
        lighting = "qmk_rgblight"
    
    return {
        "name": name,
        "vendorId": vendorId,
        "productId": productId,
        "lighting": lighting
    }


def extract_matrix(kb_data):
    """Extract optional matrix object from keyboard.json."""
    matrix_obj = {}
    mp = kb_data.get("matrix_pins", {})
    if mp.get("rows"):
        matrix_obj["rows"] = len(mp["rows"])
    if mp.get("cols"):
        matrix_obj["cols"] = len(mp["cols"])
    return matrix_obj if matrix_obj else None


def extract_default_layout(layouts_dict):
    """Extract default layout from multi-layout keyboards."""
    if not isinstance(layouts_dict, dict):
        return []
    extracted = None
    for name, data in layouts_dict.items():
        if isinstance(data, dict) and "layout" in data:
            extracted = data["layout"]
            break
    return extracted or []


def extract_matrix_pins_data(kb_data):
    """Extract matrix_pins information from keyboard.json."""
    mp = kb_data.get("matrix_pins", {})
    extracted = {}
    if "x" in mp:
        extracted["x"] = mp["x"]
    if "y" in mp:
        extracted["y"] = mp["y"]
    if "w" in mp:
        extracted["w"] = mp["w"]
    if not extracted:
        extracted["x"] = 0
        extracted["y"] = 0
        extracted["w"] = 1
    return {"default": extracted}


def flatten_layout_entry(entry):
    """Convert keyboard.json layout entry to real vial.json format.
    
    REAL FORMAT: Returns nested list [[marker], ["coord"]] like Alps64!
    """
    if not isinstance(entry, dict):
        return []
    
    x_val = entry.get("x")
    y_val = entry.get("y")
    w_val = entry.get("w", 1)
    
    mp_props = extract_matrix_pins_data(entry).get("default", {})
    
    if x_val is None:
        x_val = mp_props.get("x") or 0
    if y_val is None:
        y_val = mp_props.get("y") or None
    if w_val == 1 and "w" not in entry and "w" not in mp_props:
        w_val = mp_props.get("w", 1)
    
    # Get matrix coordinates (row, col order)
    matrix = entry.get("matrix")
    if not matrix or not isinstance(matrix, list):
        return []
    
    try:
        r_idx = int(matrix[0]) if len(matrix) > 0 else 0
        c_idx = int(matrix[1]) if len(matrix) > 1 else 0
    except (TypeError, ValueError):
        r_idx = c_idx = 0
    
    coord_str = "{},{}".format(r_idx, c_idx)
    
    # Build marker dict and coordinate string as separate items for nested structure
    if w_val > 1:
        # Wide keys use standalone {"w": N} entries first (REAL FORMAT!)
        marker_dict = [{"w": int(w_val)}]
        
        if x_val is not None and y_val is not None:
            pos_marker = {"x": float(x_val), "y": float(y_val)}
            marker_dict.append(pos_marker)
        elif x_val is not None:
            marker_dict.append({"x": float(x_val)})
        
        # Coordinate string as separate item in nested list
        return [[*marker_dict, coord_str]]
    
    elif x_val is not None and y_val is not None:
        pos_marker = {"x": float(x_val), "y": float(y_val)}
        # REAL FORMAT: Return as nested list [[marker], ["coord"]]
        return [[pos_marker, coord_str]]
    
    elif x_val is not None:
        pos_marker = {"x": float(x_val)}
        return [[pos_marker, coord_str]]
    
    else:
        # Positionless entry - just coordinate string
        return [[coord_str]]


def convert_keyboard_to_vial(kb_path):
    """Convert keyboard.json to vial.json following real vial-qmk patterns."""
    kb_data = load_json_file(kb_path)
    if not kb_data:
        return None, None
    
    metadata = extract_metadata(kb_data)
    matrix_obj = extract_matrix(kb_data)
    
    layouts_dict = kb_data.get("layouts", {})
    if isinstance(layouts_dict, dict):
        layout_list = extract_default_layout(layouts_dict)
    else:
        layout_list = []
    
    if not layout_list or len(layout_list) == 0:
        vial_output = {
            "name": metadata["name"],
            "vendorId": metadata["vendorId"],
            "productId": metadata["productId"],
            "lighting": metadata["lighting"]
        }
        if matrix_obj:
            vial_output["matrix"] = matrix_obj
        vial_output["layouts"] = {"keymap": []}
        return vial_output, kb_data
    
    keymap_entries = []
    
    for entry in layout_list:
        if not isinstance(entry, dict):
            continue
        
        flattened = flatten_layout_entry(entry)
        
        if flattened:
            # Each item is already a nested list like [[marker], ["coord"]]
            for pair in flattened:
                keymap_entries.append(pair)
    
    vial_output = {
        "name": metadata["name"],
        "vendorId": metadata["vendorId"],
        "productId": metadata["productId"],
        "lighting": metadata["lighting"]
    }
    
    if matrix_obj:
        vial_output["matrix"] = matrix_obj
    
    vial_output["layouts"] = {
        "keymap": keymap_entries
    }
    
    return vial_output, kb_data


if __name__ == "__main__":
    import sys
    test_kb = r"D:\GitHub2\vial-qmk\keyboards\alpha\keyboard.json"
    if len(sys.argv) > 1:
        test_kb = sys.argv[1]
    
    vial_output, source_data = convert_keyboard_to_vial(test_kb)
    
    if vial_output:
        print("Conversion successful!")
        print("  Keyboard name: {}".format(vial_output.get('name', 'N/A')))
        keymap = vial_output["layouts"].get("keymap", [])
        print("  Keymap entries: {}".format(len(keymap)))
        
        if keymap:
            print("\nSample entries (first 5):")
            for i, entry in enumerate(keymap[:5]):
                print("  [{}: {}]".format(i, repr(entry)))
    else:
        print("Conversion failed - no valid layouts found!")
