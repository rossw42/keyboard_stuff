#!/usr/bin/env python3
"""
QMK Matrix Configuration Generator

This script generates keyboard.json matrix_pins/layouts and keymap.c LAYOUT sections
based on the number of rows, columns, and pin assignments.
"""

import json
import sys

def generate_matrix_config(num_rows, num_cols, row_pins, col_pins, layout_name="LAYOUT", diode_direction="COL2ROW"):
    """
    Generate QMK matrix configuration sections.
    
    Args:
        num_rows (int): Number of matrix rows
        num_cols (int): Number of matrix columns
        row_pins (list): List of row pin names (e.g., ["B0", "B1", "B2"])
        col_pins (list): List of column pin names (e.g., ["C0", "C1", "C2"])
        layout_name (str): Name for the layout (default: "LAYOUT")
        diode_direction (str): Diode direction, "COL2ROW" or "ROW2COL"
    
    Returns:
        tuple: (keyboard_json_sections, keymap_c_section)
    """
    
    # Validate inputs
    if len(row_pins) != num_rows:
        raise ValueError(f"Number of row pins ({len(row_pins)}) doesn't match num_rows ({num_rows})")
    if len(col_pins) != num_cols:
        raise ValueError(f"Number of col pins ({len(col_pins)}) doesn't match num_cols ({num_cols})")
    
    # Generate matrix_pins section for keyboard.json
    matrix_pins = {
        "cols": col_pins,
        "rows": row_pins
    }
    
    # Generate sequential layout (all matrix positions used)
    layout_positions = []
    keymap_positions = []
    
    for row in range(num_rows):
        for col in range(num_cols):
            # Add to layout definition
            layout_positions.append({
                "matrix": [row, col],
                "x": col,
                "y": row
            })
            
            # Generate default keycode name for keymap
            if row == 0 and col == 0:
                keycode = "KC_ESC"
            elif row == 0:
                keycode = f"KC_{col}"  # Numbers for top row
            elif row == 1 and col < 10:
                # QWERTY top letter row
                qwerty_keys = ["KC_Q", "KC_W", "KC_E", "KC_R", "KC_T", "KC_Y", "KC_U", "KC_I", "KC_O", "KC_P"]
                keycode = qwerty_keys[col] if col < len(qwerty_keys) else "KC_NO"
            elif row == 2 and col < 9:
                # QWERTY middle letter row  
                asdf_keys = ["KC_A", "KC_S", "KC_D", "KC_F", "KC_G", "KC_H", "KC_J", "KC_K", "KC_L"]
                keycode = asdf_keys[col] if col < len(asdf_keys) else "KC_NO"
            elif row == 3 and col < 7:
                # QWERTY bottom letter row
                zxcv_keys = ["KC_Z", "KC_X", "KC_C", "KC_V", "KC_B", "KC_N", "KC_M"]
                keycode = zxcv_keys[col] if col < len(zxcv_keys) else "KC_NO"
            else:
                keycode = "KC_NO"  # Placeholder for unused positions
            
            keymap_positions.append(keycode)
    
    # Create layout section for keyboard.json
    layouts = {
        layout_name: {
            "layout": layout_positions
        }
    }
    
    # Create keyboard.json sections
    keyboard_json_sections = {
        "matrix_pins": matrix_pins,
        "diode_direction": diode_direction,
        "layouts": layouts
    }
    
    # Create keymap.c LAYOUT section
    keymap_lines = []
    keymap_lines.append(f"const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {{")
    keymap_lines.append(f"    [0] = {layout_name}(")
    
    # Format keymap with proper indentation and row comments
    for row in range(num_rows):
        row_start = row * num_cols
        row_end = row_start + num_cols
        row_keycodes = keymap_positions[row_start:row_end]
        
        # Add row comment
        keymap_lines.append(f"        // Row {row}")
        
        # Format keycodes with proper spacing
        formatted_row = "        " + ", ".join(f"{kc:<8}" for kc in row_keycodes)
        if row < num_rows - 1:
            formatted_row += ","
        keymap_lines.append(formatted_row)
    
    keymap_lines.append("    )")
    keymap_lines.append("};")
    
    keymap_c_section = "\n".join(keymap_lines)
    
    return keyboard_json_sections, keymap_c_section

def print_usage():
    """Print usage instructions."""
    print("""
QMK Matrix Configuration Generator

Usage:
    python qmk_matrix_generator.py <num_rows> <num_cols> <row_pins> <col_pins> [layout_name] [diode_direction]

Arguments:
    num_rows        : Number of matrix rows (integer)
    num_cols        : Number of matrix columns (integer)
    row_pins        : Comma-separated list of row pin names (e.g., "B0,B1,B2,B3")
    col_pins        : Comma-separated list of column pin names (e.g., "C0,C1,C2,C3,C4")
    layout_name     : Optional layout name (default: "LAYOUT")
    diode_direction : Optional diode direction "COL2ROW" or "ROW2COL" (default: "COL2ROW")

Examples:
    # Simple 3x4 matrix
    python qmk_matrix_generator.py 3 4 "B0,B1,B2" "C0,C1,C2,C3"
    
    # 5x14 matrix like 1up60hse
    python qmk_matrix_generator.py 5 14 "B3,B2,B1,B0,D4" "C7,F7,F6,F5,F4,F1,E6,D1,D0,D2,D3,D5,D6,D7" "LAYOUT_60_ansi"

    # 4x12 ortholinear
    python qmk_matrix_generator.py 4 12 "A0,A1,A2,A3" "B0,B1,B2,B3,B4,B5,B6,B7,C0,C1,C2,C3" "LAYOUT_ortho_4x12"
""")

def main():
    """Main function to handle command line arguments and generate configurations."""
    
    if len(sys.argv) < 5 or sys.argv[1] in ['-h', '--help']:
        print_usage()
        return
    
    try:
        # Parse command line arguments
        num_rows = int(sys.argv[1])
        num_cols = int(sys.argv[2])
        row_pins = [pin.strip() for pin in sys.argv[3].split(',')]
        col_pins = [pin.strip() for pin in sys.argv[4].split(',')]
        
        layout_name = sys.argv[5] if len(sys.argv) > 5 else "LAYOUT"
        diode_direction = sys.argv[6] if len(sys.argv) > 6 else "COL2ROW"
        
        # Generate configurations
        keyboard_json, keymap_c = generate_matrix_config(
            num_rows, num_cols, row_pins, col_pins, layout_name, diode_direction
        )
        
        # Output results
        print("=" * 60)
        print("KEYBOARD.JSON SECTIONS")
        print("=" * 60)
        print(json.dumps(keyboard_json, indent=4))
        
        print("\n" + "=" * 60)
        print("KEYMAP.C LAYOUT SECTION")
        print("=" * 60)
        print(keymap_c)
        
        print("\n" + "=" * 60)
        print("MATRIX INFORMATION")
        print("=" * 60)
        print(f"Matrix Size: {num_rows} rows × {num_cols} columns = {num_rows * num_cols} total positions")
        print(f"GPIO Pins Used: {len(row_pins) + len(col_pins)} ({len(row_pins)} rows + {len(col_pins)} columns)")
        print(f"Layout Name: {layout_name}")
        print(f"Diode Direction: {diode_direction}")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nUse -h or --help for usage instructions.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("\nUse -h or --help for usage instructions.")

if __name__ == "__main__":
    main()