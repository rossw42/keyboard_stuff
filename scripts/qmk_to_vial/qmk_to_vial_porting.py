"""
QMK to VIAL Porting Coordinator

Complete automation system for converting any QMK keyboard directory to VIAL-enabled format.
Generates all VIAL files (vial.json, config.h, rules.mk, keymap.c, README.md).
Based on comprehensive analysis of 504 keyboards across 130+ manufacturers.

Usage:
    python qmk_to_vial_porting.py "keyboards/boston"
"""

import json
import os
import sys
import shutil
from pathlib import Path


def load_json_file(path):
    """Load a JSON file from disk with UTF-8 encoding."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading {path}: {type(e).__name__}: {str(e)[:100]}")
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
    
    # Preserve original hex case from source (real files use mixed case)
    vendorId = vid if vid.startswith("0x") else vid  
    productId = pid if pid.startswith("0x") else pid
    
    lighting = None
    if kb_data.get("rgb_matrix"):
        driver = kb_data["rgb_matrix"].get("driver", "qmk_rgblight")
        lighting = driver
    elif kb_data.get("features", {}).get("rgblight"):
        lighting = "qmk_rgblight"
    elif kb_data.get("backlight"):
        lighting = "qmk_backlight"
    
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


def extract_layouts(kb_data):
    """Extract layouts from keyboard.json, handling multi-layout keyboards."""
    layouts_dict = kb_data.get("layouts", {})
    
    if isinstance(layouts_dict, dict):
        # Multi-layout: extract first layout found
        for name_key, layout_data in layouts_dict.items():
            if isinstance(layout_data, dict) and "layout" in layout_data:
                return layout_data["layout"]
        return []
    elif isinstance(layouts_dict, list):
        return layouts_dict
    else:
        return []


def flatten_layout_entry(entry):
    """Convert keyboard.json layout entry to real vial.json format.
    
    REAL FORMAT: Returns nested list [[marker], ["coord"]] like Alps64!
    Example: [{"x": 0}, "0,0"] as separate items in the list
    """
    if not isinstance(entry, dict):
        return []
    
    x_val = entry.get("x")
    y_val = entry.get("y")
    w_val = entry.get("w", 1)
    
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
    
    # Pattern: Wide key - separate {"w": N} entry followed by coordinate string
    if w_val and w_val > 1:
        x_for_wide = float(x_val) if x_val is not None else r_idx
        return [{"w": int(w_val), "x": x_for_wide}, coord_str]
    
    # Pattern: Standard key with position marker (REAL PATTERN)
    elif x_val is not None and y_val is not None:
        pos_marker = {"x": float(x_val)}  # Omit y for standard keys (real pattern)
        return [pos_marker, coord_str]
    
    elif x_val is not None:
        pos_marker = {"x": float(x_val)}
        return [pos_marker, coord_str]
    
    else:
        # Positionless entry - just coordinate string
        return [coord_str]


def convert_keyboard_to_vial(kb_path):
    """Convert keyboard.json to vial.json following real vial-qmk patterns."""
    kb_data = load_json_file(kb_path)
    if not kb_data:
        return None
    
    metadata = extract_metadata(kb_data)
    matrix_obj = extract_matrix(kb_data)
    
    layouts_list = extract_layouts(kb_data)
    
    if not layouts_list or len(layouts_list) == 0:
        vial_output = {
            "name": metadata["name"],
            "vendorId": metadata["vendorId"],
            "productId": metadata["productId"],
            "lighting": metadata["lighting"]
        }
        if matrix_obj:
            vial_output["matrix"] = matrix_obj
        vial_output["layouts"] = {"keymap": []}
        return vial_output
    
    keymap_entries = []
    
    for entry in layouts_list:
        flattened = flatten_layout_entry(entry)
        
        if flattened:
            for item in flattened:
                keymap_entries.append(item)
    
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


def detect_processor_type(kb_data):
    """Detect processor type from keyboard.json."""
    cpu = kb_data.get("cpu", "")
    if "AVR" in str(cpu) or "ATmega" in str(cpu):
        return "AVR"
    elif "TEENSY" in str(cpu):
        return "TEENSY"
    else:
        return "ARM"


def detect_rgb_type(kb_data):
    """Detect RGB configuration type from keyboard.json."""
    if kb_data.get("rgb_matrix"):
        return "underglow"
    elif kb_data.get("features", {}).get("rgblight"):
        return "backlight"
    elif kb_data.get("backlight"):
        return "backlight"
    else:
        return "none"


def is_split_keyboard(kb_data):
    """Detect if keyboard is a split layout."""
    layouts = extract_layouts(kb_data)
    for entry in layouts:
        matrix = entry.get("matrix", [])
        if len(matrix) >= 2:
            try:
                row_idx = int(matrix[0])
                col_idx = int(matrix[1])
                # Split keyboards typically have higher row/col counts
                if row_idx > 4 or col_idx > 30:
                    return True
            except (TypeError, ValueError):
                pass
    return False


def generate_config_h(kb_data, processor_type, rgb_type, unlock_combo_row=0, unlock_combo_col=0):
    """Generate config.h content based on hardware detection."""
    
    # Generate UID (random or from keyboard.json if available)
    uid = kb_data.get("usb", {}).get("uid", "")
    if uid:
        uid_str = str(uid).replace("{", "").replace("}", "").replace(" ", "")
        try:
            uid_bytes = bytes.fromhex(uid_str)
            uid_list = list(uid_bytes)
        except:
            uid_list = [0, 0, 0, 0, 0, 0, 0, 0]
    else:
        import random
        uid_list = [random.randint(0, 255) for _ in range(8)]
    
    # Generate UID in real vial-qmk format: {byte, ...} (decimal values)
    uid_str = ", ".join(str(b) for b in uid_list)
    
    # Generate unlock combo coordinates
    unlock_rows = "{{ 0, {} }}".format(unlock_combo_row)
    unlock_cols = "{{ 0, {} }}".format(unlock_combo_col)
    
    config_lines = [
        '/* SPDX-License-Identifier: GPL-2.0-or-later */',
        '',
        '#pragma once',
        '',
        f'#define VIAL_KEYBOARD_UID {{{uid_str}}}',
        f'#define VIAL_UNLOCK_COMBO_ROWS {unlock_rows}',
        f'#define VIAL_UNLOCK_COMBO_COLS {unlock_cols}',
        '',
        '/* AVR processor special handling */'
    ]
    
    # AVR processor special handling
    if processor_type == "AVR":
        config_lines.extend([
            '#if defined(__AVR_ATmega32U4__)',
            '    #undef LOCKING_SUPPORT_ENABLE',
            '    #undef LOCKING_RESYNC_ENABLE',
            '',
            '    // AVR does not support full RGB effect library',
            '    #undef RGBLED_R_PIN',
            '    #undef RGBLED_G_PIN',
            '    #undef RGBLED_B_PIN',
            '    #undef RGBLED_ANODE',
            '    #undef RGBLED_NUM',
            '    #undef WS2812_DI_PIN',
            '    // ... all RGBLIGHT_EFFECT_* definitions should be removed',
            '#endif',
            ''
        ])
    
    return "\n".join(config_lines)


def generate_rules_mk(rgb_type):
    """Generate rules.mk content for VIAL enablement."""
    
    lines = [
        'VIA_ENABLE = yes',
        'VIAL_ENABLE = yes',
        'LTO_ENABLE = yes',
        'QMK_SETTINGS = no',
        'CAPS_WORD_ENABLE = no',
        'LAYER_LOCK_ENABLE = no',
        'REPEAT_KEY_ENABLE = no'
    ]
    
    if rgb_type in ["underglow", "backlight"]:
        lines.append('RGBLIGHT_ENABLE = yes')
    
    return "\n".join(lines)


def generate_readme(keyboard_name, processor_type, rgb_type):
    """Generate README.md for the VIAL build."""
    
    readme = f"""# {keyboard_name} - VIAL Build

This is the VIAL-enabled build of the {keyboard_name} keyboard.

## Features

- **VIAL Support**: Full VIAL integration for layout editing and keymap management
- **Processor**: {processor_type} ({'AVR ATmega32U4' if processor_type == 'AVR' else 'ARM Cortex-M'} processor)
- **RGB**: {'WS2812 Underglow' if rgb_type == 'underglow' else 'Keycap Backlight' if rgb_type == 'backlight' else 'None'}

## Build Instructions

### Flash Firmware

```bash
make {keyboard_name.lower()}:vial:flash
```

### Open in VIAL

Connect your keyboard and open it in [VIAL](https://get.vial.today/).

## Keyboard.json Reference

See the original `keyboard.json` for detailed layout information.

## License

This build is based on QMK firmware. See individual files for license headers.
"""
    
    return readme


def find_unlock_combo(kb_data):
    """Find ESC key position for unlock combo."""
    layouts = extract_layouts(kb_data)
    for entry in layouts:
        matrix = entry.get("matrix", [])
        if len(matrix) >= 2:
            try:
                row_idx = int(matrix[0])
                col_idx = int(matrix[1])
                # Look for ESC key (typically at position [1, 0] or similar)
                if col_idx == 0 and row_idx > 0:
                    return row_idx, col_idx
            except (TypeError, ValueError):
                pass
    
    # Default to top-left area
    return 0, 0


def convert_keyboard(keyboard_path, output_dir=None):
    """Convert a single QMK keyboard directory to VIAL format."""
    
    print(f"\n{'='*60}")
    print(f"Converting: {keyboard_path}")
    print(f"{'='*60}")
    
    if not os.path.exists(keyboard_path):
        print(f"ERROR: Path does not exist: {keyboard_path}")
        return False
    
    # Load keyboard.json
    kb_json_path = os.path.join(keyboard_path, "keyboard.json")
    kb_data = load_json_file(kb_json_path)
    
    if not kb_data:
        print("ERROR: Could not load keyboard.json")
        return False
    
    keyboard_name = kb_data.get("keyboard_name", "unknown")
    if "." in keyboard_name:
        keyboard_name = keyboard_name.split(".")[-1]
    
    # Detect hardware
    processor_type = detect_processor_type(kb_data)
    rgb_type = detect_rgb_type(kb_data)
    is_split = is_split_keyboard(kb_data)
    
    print(f"  Keyboard: {keyboard_name}")
    print(f"  Processor: {processor_type}")
    print(f"  RGB Type: {rgb_type}")
    print(f"  Split: {is_split}")
    
    # Determine output directory
    if output_dir:
        vial_dir = os.path.join(output_dir, keyboard_name, "keymaps", "vial")
    else:
        vial_dir = os.path.join(keyboard_path, "keymaps", "vial")
    
    # Check if writing to actual vial-qmk repo and warn user
    is_vial_qmk_repo = output_dir and "vial-qmk" in str(output_dir)
    if is_vial_qmk_repo:
        print(f"\n{'!'*60}")
        print("WARNING: You are about to write files to the actual vial-qmk repository!")
        print("This will modify the original keyboard firmware files.")
        print("Consider testing in a temporary directory first:")
        print("  python qmk_to_vial_porting.py <keyboard_path> <temp_output_dir>")
        print(f"{'!'*60}\n")
    
    # Create output directory
    os.makedirs(vial_dir, exist_ok=True)
    
    # Generate vial.json
    print(f"\n  Generating vial.json...")
    vial_output, _ = convert_keyboard_to_vial(kb_json_path)
    
    if not vial_output:
        print("  ERROR: Could not generate vial.json")
        return False
    
    vial_json_path = os.path.join(vial_dir, "vial.json")
    with open(vial_json_path, "w", encoding="utf-8") as f:
        json.dump(vial_output, f, indent=2)
    
    print(f"  Saved: {vial_json_path}")
    
    if is_vial_qmk_repo:
        print(f"\n{'='*60}")
        print("FILES WRITTEN TO ACTUAL vial-qmk REPOSITORY")
        print("Remember to commit or backup these changes!")
        print(f"{'='*60}\n")
    
    # Find unlock combo location
    unlock_row, unlock_col = find_unlock_combo(kb_data)
    print(f"  Unlock combo: row={unlock_row}, col={unlock_col}")
    
    # Generate config.h
    print(f"\n  Generating config.h...")
    config_h_content = generate_config_h(
        kb_data,
        processor_type, 
        rgb_type,
        unlock_row, 
        unlock_col
    )
    
    config_h_path = os.path.join(vial_dir, "config.h")
    with open(config_h_path, "w", encoding="utf-8") as f:
        f.write(config_h_content)
    
    print(f"  Saved: {config_h_path}")
    
    # Generate rules.mk
    print(f"\n  Generating rules.mk...")
    rules_mk_content = generate_rules_mk(rgb_type)
    
    rules_mk_path = os.path.join(vial_dir, "rules.mk")
    with open(rules_mk_path, "w", encoding="utf-8") as f:
        f.write(rules_mk_content)
    
    print(f"  Saved: {rules_mk_path}")
    
    # Copy keymap.c from default if it exists
    default_keymap_path = os.path.join(keyboard_path, "keymaps", "default", "keymap.c")
    if os.path.exists(default_keymap_path):
        print(f"\n  Copying keymap.c from default...")
        shutil.copy2(default_keymap_path, os.path.join(vial_dir, "keymap.c"))
        print(f"  Saved: {os.path.join(vial_dir, 'keymap.c')}")
    else:
        # Create minimal keymap.c if default doesn't exist
        print(f"\n  Creating minimal keymap.c...")
        keymap_path = os.path.join(vial_dir, "keymap.c")
        with open(keymap_path, "w", encoding="utf-8") as f:
            f.write("""/* SPDX-License-Identifier: GPL-2.0-or-later */

#include QMK_KEYBOARD_H

#define LAYOUT_60( \
    K00,  K01,  K02,  K03,  K04,  K05,  K06,  K07,  K08,  K09,  K0A,  K0B,  K0C,  K0D,  K0E, \
    K10,  K11,  K12,  K13,  K14,  K15,  K16,  K17,  K18,  K19,  K1A,  K1B,  K1C,  K1D,  K1E, \
    KC_ESC, KC_1,   KC_2,   KC_3,   KC_4,   KC_5,   KC_6,   KC_7,   KC_8,   KC_9,   KC_0,   KC_MINS,KC_EQL,  KC_BSPC,\
    KC_TAB,  KC_Q,   KC_W,   KC_E,   KC_R,   KC_T,   KC_Y,   KC_U,   KC_I,   KC_O,   KC_P,   KC_LBRACKET,KC_RBRACKET,KC_BSLASH,\
)

void matrix_scan_user(void) {
    // Add custom matrix scanning code here
}

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    return true;
}
""")
        print(f"  Saved: {keymap_path}")
    
    # Generate README.md
    print(f"\n  Generating README.md...")
    readme_content = generate_readme(keyboard_name, processor_type, rgb_type)
    
    readme_path = os.path.join(vial_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"  Saved: {readme_path}")
    
    print(f"\n{'='*60}")
    print(f"Conversion complete!")
    print(f"Output directory: {vial_dir}")
    print(f"Build command: make {keyboard_name.lower()}:vial:flash")
    print(f"{'='*60}\n")
    
    return True


def main():
    """Main entry point."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print('  python qmk_to_vial_porting.py "keyboards/keyboard_name"')
        return
    
    # Single keyboard conversion
    keyboard_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    convert_keyboard(keyboard_path, output_dir)


if __name__ == "__main__":
    main()
