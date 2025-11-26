#!/usr/bin/env python3
"""
Convert Vial .vil keymap files to keymap-drawer JSON format.
Usage: python vil_to_keymap_drawer.py <input.vil> [output.json]
"""

import json
import sys
from pathlib import Path


def parse_vil_file(vil_path):
    """Parse a Vial .vil JSON file."""
    with open(vil_path, 'r') as f:
        return json.load(f)


def detect_layout_params(layout_data):
    """Detect keyboard layout parameters from Vial layout data."""
    if not layout_data or len(layout_data) == 0:
        return None
    
    first_layer = layout_data[0]
    
    # Count rows and columns
    rows = len(first_layer)
    cols = len(first_layer[0]) if first_layer else 0
    
    # Detect if split by checking for -1 (empty) positions
    is_split = False
    thumbs = 0
    
    # Check if it's a split keyboard (has empty rows with single key)
    if rows > 0:
        last_row = first_layer[-1]
        if len(last_row) == 1 and last_row[0] != -1:
            is_split = True
            thumbs = 1
            rows -= 1
    
    return {
        "split": is_split,
        "rows": rows,
        "columns": cols,
        "thumbs": thumbs if is_split else 0
    }


def flatten_layer(layer_data):
    """Flatten a Vial layer into a list of keys, filtering out -1 (empty) positions."""
    flattened = []
    for row in layer_data:
        for key in row:
            if key != -1:  # Skip empty positions
                flattened.append(key)
    return flattened


def convert_key(key_str):
    """Convert a QMK keycode to keymap-drawer format."""
    if isinstance(key_str, int):
        return None
    
    if not key_str:
        return None
    
    # Handle layer tap keys like "LT1(KC_ENTER)"
    if key_str.startswith("LT"):
        # Extract layer number and key
        import re
        match = re.match(r"LT(\d+)\((.*?)\)", key_str)
        if match:
            layer_num = match.group(1)
            key = match.group(2)
            key_name = convert_keycode(key)
            return {"t": key_name, "h": f"Layer{layer_num}"}
    
    # Handle toggle layer keys like "TG(3)"
    if key_str.startswith("TG"):
        import re
        match = re.match(r"TG\((\d+)\)", key_str)
        if match:
            layer_num = match.group(1)
            return {"t": f"TG{layer_num}", "type": "held"}
    
    # Handle transparent keys
    if key_str == "KC_TRNS":
        return {"t": "Trans", "type": "trans"}
    
    if key_str == "KC_NO":
        return {"t": "No", "type": "trans"}
    
    # Regular keycode
    return convert_keycode(key_str)


def convert_keycode(keycode):
    """Convert QMK keycode to display name."""
    # Remove KC_ prefix
    if keycode.startswith("KC_"):
        keycode = keycode[3:]
    
    # Common replacements
    replacements = {
        "SCLN": ";",
        "COMMA": ",",
        "DOT": ".",
        "SLASH": "/",
        "BSPC": "Bksp",
        "ENT": "Enter",
        "SPC": "Space",
        "SCOLON": ";",
        "LBRACKET": "[",
        "RBRACKET": "]",
        "BSLS": "\\",
        "TRNS": "Trans",
        "LSFT": "Shift",
        "LCTL": "Ctrl",
        "LALT": "Alt",
        "LGUI": "GUI",
        "WH_U": "WH↑",
        "WH_D": "WH↓",
        "BTN1": "BTN1",
        "BTN2": "BTN2",
        "BTN3": "BTN3",
    }
    
    for old, new in replacements.items():
        if keycode == old:
            return new
    
    # Handle shifted keys
    if keycode.startswith("LSFT("):
        import re
        match = re.match(r"LSFT\((.*?)\)", keycode)
        if match:
            inner = match.group(1)
            return convert_keycode(inner)
    
    return keycode


def build_layers(vil_data):
    """Build keymap-drawer layers from Vial layout data."""
    layers = {}
    layout_data = vil_data.get("layout", [])
    
    layer_names = ["Base", "Layer1", "Layer2", "Layer3"]
    
    for layer_idx, layer in enumerate(layout_data):
        if layer_idx >= len(layer_names):
            break
        
        layer_name = layer_names[layer_idx]
        layer_keys = []
        
        for row in layer:
            row_keys = []
            for key in row:
                if key == -1:
                    continue
                
                converted = convert_key(key)
                if converted:
                    row_keys.append(converted)
                else:
                    row_keys.append(key if isinstance(key, str) else "")
            
            if row_keys:
                layer_keys.append(row_keys)
        
        layers[layer_name] = layer_keys
    
    return layers


def build_combos(vil_data):
    """Build keymap-drawer combos from Vial combo data."""
    combos = []
    combo_data = vil_data.get("combo", [])
    
    alignments = ["top", "bottom", "left", "mid"]
    offsets = [0.5, 0.3, 0.1, -0.1, -0.5, -1.0]
    
    for idx, combo in enumerate(combo_data):
        if len(combo) < 5:
            continue
        
        trigger_keys = combo[:2]
        result_key = combo[4]
        
        # Skip empty combos
        if result_key == "KC_NO" or not trigger_keys[0] or trigger_keys[0] == "KC_NO":
            continue
        
        # Convert trigger keys to names
        trigger_names = []
        for tk in trigger_keys:
            if tk and tk != "KC_NO":
                trigger_names.append(convert_keycode(tk))
        
        if len(trigger_names) < 2:
            continue
        
        # Convert result key
        result_converted = convert_key(result_key)
        if isinstance(result_converted, dict):
            result_key_obj = result_converted
        else:
            result_key_obj = {"t": convert_keycode(result_key), "type": "held"}
        
        # Vary alignment and offset for visual interest
        alignment = alignments[idx % len(alignments)]
        offset = offsets[idx % len(offsets)]
        arc_scale = 0.8 + (idx % 3) * 0.05
        
        combo_obj = {
            "tk": trigger_names,
            "k": result_key_obj,
            "l": ["Base"],
            "a": alignment,
            "o": offset,
            "arc_scale": arc_scale,
            "d": True
        }
        
        combos.append(combo_obj)
    
    return combos


def create_keymap_drawer_json(vil_data, keyboard_name="keyboard"):
    """Create a complete keymap-drawer JSON structure."""
    layout_params = detect_layout_params(vil_data.get("layout", []))
    
    if not layout_params:
        layout_params = {
            "split": True,
            "rows": 3,
            "columns": 5,
            "thumbs": 1
        }
    
    keymap_drawer = {
        "layout": {
            "ortho_layout": layout_params
        },
        "layers": build_layers(vil_data),
        "draw_config": {
            "key_w": 64,
            "key_h": 60,
            "split_gap": 40,
            "combo_w": 36,
            "combo_h": 34,
            "key_rx": 8,
            "key_ry": 8,
            "dark_mode": "auto",
            "n_columns": 1,
            "separate_combo_diagrams": False,
            "inner_pad_w": 3,
            "inner_pad_h": 3,
            "outer_pad_w": 40,
            "outer_pad_h": 60,
            "line_spacing": 1.3,
            "arc_radius": 8,
            "append_colon_to_layer_header": True,
            "small_pad": 3,
            "legend_rel_x": 0.0,
            "legend_rel_y": 0.0,
            "draw_key_sides": False,
            "svg_extra_style": "",
            "footer_text": "Created with <a href=\"https://github.com/caksoylar/keymap-drawer\">keymap-drawer</a>",
            "shrink_wide_legends": 8,
            "style_layer_activators": True,
            "mark_alternate_layer_activators": True,
            "glyph_tap_size": 16,
            "glyph_hold_size": 13,
            "glyph_shifted_size": 11
        },
        "combos": build_combos(vil_data)
    }
    
    return keymap_drawer


def main():
    if len(sys.argv) < 2:
        print("Usage: python vil_to_keymap_drawer.py <input.vil> [output.json]")
        sys.exit(1)
    
    vil_path = Path(sys.argv[1])
    
    if not vil_path.exists():
        print(f"Error: File not found: {vil_path}")
        sys.exit(1)
    
    # Determine output path
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
    else:
        output_path = vil_path.with_suffix(".json")
    
    print(f"Converting {vil_path} to keymap-drawer format...")
    
    # Parse and convert
    vil_data = parse_vil_file(vil_path)
    keymap_drawer = create_keymap_drawer_json(vil_data, vil_path.stem)
    
    # Write output
    with open(output_path, 'w') as f:
        json.dump(keymap_drawer, f, indent=2)
    
    print(f"✓ Successfully converted to {output_path}")
    print(f"  Layers: {len(keymap_drawer['layers'])}")
    print(f"  Combos: {len(keymap_drawer['combos'])}")


if __name__ == "__main__":
    main()
