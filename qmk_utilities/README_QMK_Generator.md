# QMK Matrix Configuration Generator

A Python script that automatically generates QMK `keyboard.json` and `keymap.c` sections based on your matrix configuration.

## What It Does

Takes your matrix specifications and generates:
1. **`matrix_pins`** section for `keyboard.json`
2. **`layouts`** section for `keyboard.json` 
3. **`LAYOUT` macro** section for `keymap.c`

## Usage

```bash
python qmk_matrix_generator.py <num_rows> <num_cols> <row_pins> <col_pins> [layout_name] [diode_direction]
```

### Arguments

- **`num_rows`**: Number of matrix rows (integer)
- **`num_cols`**: Number of matrix columns (integer)
- **`row_pins`**: Comma-separated row pin names (e.g., `"B0,B1,B2,B3"`)
- **`col_pins`**: Comma-separated column pin names (e.g., `"C0,C1,C2,C3"`)
- **`layout_name`**: Optional layout name (default: `"LAYOUT"`)
- **`diode_direction`**: Optional diode direction `"COL2ROW"` or `"ROW2COL"` (default: `"COL2ROW"`)

## Examples

### Simple 3×4 Macropad
```bash
python qmk_matrix_generator.py 3 4 "B0,B1,B2" "C0,C1,C2,C3" "LAYOUT_3x4"
```

### 60% Keyboard (like 1up60hse)
```bash
python qmk_matrix_generator.py 5 14 "B3,B2,B1,B0,D4" "C7,F7,F6,F5,F4,F1,E6,D1,D0,D2,D3,D5,D6,D7" "LAYOUT_60_ansi"
```

### 4×12 Ortholinear (like Planck)
```bash
python qmk_matrix_generator.py 4 12 "A0,A1,A2,A3" "B0,B1,B2,B3,B4,B5,B6,B7,C0,C1,C2,C3" "LAYOUT_ortho_4x12"
```

## Output

The script generates three sections:

### 1. KEYBOARD.JSON SECTIONS
```json
{
    "matrix_pins": {
        "cols": ["C0", "C1", "C2", "C3"],
        "rows": ["B0", "B1", "B2"]
    },
    "diode_direction": "COL2ROW",
    "layouts": {
        "LAYOUT_3x4": {
            "layout": [
                {"matrix": [0, 0], "x": 0, "y": 0},
                {"matrix": [0, 1], "x": 1, "y": 0},
                // ... more positions
            ]
        }
    }
}
```

### 2. KEYMAP.C LAYOUT SECTION
```c
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT_3x4(
        // Row 0
        KC_ESC, KC_1, KC_2, KC_3,
        // Row 1  
        KC_Q, KC_W, KC_E, KC_R,
        // Row 2
        KC_A, KC_S, KC_D, KC_F
    )
};
```

### 3. MATRIX INFORMATION
- Matrix size and total positions
- GPIO pins used
- Layout name and diode direction

## Key Features

- **Sequential Layout**: Generates all matrix positions sequentially (row-by-row)
- **Default Keycodes**: Provides sensible QWERTY-based defaults for common positions
- **Validation**: Checks that pin counts match row/column counts
- **Flexible**: Works with any matrix size and microcontroller pins
- **Copy-Paste Ready**: Output is formatted for direct use in QMK files

## Notes

- This generates a **complete matrix** where every position has a key
- For keyboards with missing keys (like 60% layouts), you'll need to manually remove unused positions from the `layouts` section
- The generated keycodes are just defaults - customize them for your specific keyboard layout
- Always verify the pin assignments match your physical wiring before flashing firmware

## Related Files

- `QMK_Matrix_Guide.md` - Comprehensive guide explaining QMK matrix relationships  
- `qmk_matrix_generator.py` - The generator script

---

*This tool was created to help demystify QMK matrix configuration by automating the tedious parts of setup.*