# Format Specifications Documentation

This document outlines the key characteristics and structures of the three keyboard layout formats supported by the QMK Format Converter.

## KLE (Keyboard Layout Editor) Format

### Overview
KLE format is a JSON array structure that describes the visual layout of a keyboard. It's primarily used for creating visual representations and is the format used by the popular keyboard-layout-editor.com tool.

### Structure
- **Array of arrays**: Each sub-array represents a row of keys
- **Mixed content**: Each row can contain strings (key labels) and objects (formatting)
- **Metadata**: First element can be an object with layout metadata

### Key Elements
- **Key labels**: Strings that can contain multiple lines separated by `\n`
- **Key properties**: Objects with properties like:
  - `w`: Width (in key units, default 1)
  - `h`: Height (in key units, default 1)
  - `x`: X offset
  - `y`: Y offset
  - `c`: Color
  - `t`: Text color
  - `f`: Font size
  - `a`: Alignment

### Example Key Patterns
```json
"Q"                    // Simple key
"!\n1"                // Key with shift modifier (top/bottom labels)
{"w": 2}, "Backspace" // Wide key (2 units)
{"c": "#777777"}      // Color property affects following keys
```

## VIA Format

### Overview
VIA format is a comprehensive JSON structure that includes keyboard metadata, matrix information, layout definition, and keymap data. It's designed for the VIA keyboard configuration tool.

### Structure
```json
{
  "version": 1,
  "vendor_id": "0x1234",
  "product_id": "0x5678",
  "lighting": "none",
  "matrix": { "rows": 5, "cols": 14 },
  "layouts": { "keymap": [...] },
  "keymaps": [...]
}
```

### Key Elements
- **Metadata**: Vendor ID, Product ID, version information
- **Matrix**: Physical wiring matrix (rows/cols)
- **Layout**: Visual layout similar to KLE but with matrix positions
- **Keymaps**: Actual key assignments using QMK keycodes

### Layout vs Keymap
- **Layout**: Defines physical key positions using matrix coordinates ("0,0", "0,1", etc.)
- **Keymap**: Defines what each key does using QMK keycodes (KC_A, KC_LSFT, etc.)

### Matrix Coordinates
- Format: "row,col" (e.g., "0,0", "1,5")
- Maps to physical switch positions
- Used to correlate visual layout with electrical matrix

## QMK keymap.c Format

### Overview
The keymap.c format is a C source file that defines keyboard layouts using QMK firmware structures. It's the native format used by QMK firmware.

### Structure
```c
#include QMK_KEYBOARD_H

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT_macro(
        // Key definitions...
    ),
};
```

### Key Elements
- **Headers**: Required QMK includes
- **Keymaps array**: Multi-dimensional array defining all layers
- **Layout macro**: Keyboard-specific macro (e.g., LAYOUT_60_ansi)
- **Keycodes**: QMK keycode constants (KC_A, KC_LSFT, etc.)
- **Layers**: Multiple layers accessed via layer switching

### Layer Structure
- **Layer 0**: Usually the base/default layer
- **Layer 1+**: Function/modifier layers
- **Layer switching**: Uses MO(), TG(), LT() functions

### Common Keycodes
- **Basic**: KC_A through KC_Z, KC_1 through KC_0
- **Modifiers**: KC_LSFT, KC_LCTL, KC_LALT, KC_LGUI
- **Special**: KC_SPC, KC_ENT, KC_BSPC, KC_TAB
- **Transparent**: KC_TRNS (inherits from lower layer)

### ASCII Art Comments
- Visual representation of the layout
- Helps developers understand key positions
- Uses box-drawing characters for clear representation

## Conversion Challenges

### Key Mapping Complexity
1. **KLE to QMK**: Need to map visual labels to QMK keycodes
2. **Matrix Correlation**: VIA uses matrix positions, others use visual positions
3. **Layer Handling**: keymap.c supports multiple layers, others may not

### Data Loss Considerations
1. **KLE → VIA**: Need to generate matrix positions
2. **VIA → KLE**: May lose matrix metadata
3. **keymap.c → Others**: May lose layer information beyond base layer

### Layout Macro Dependency
- QMK keymaps depend on keyboard-specific layout macros
- LAYOUT_60_ansi, LAYOUT_tkl, etc.
- Need to handle or generate appropriate macros

## Universal Data Model Requirements

Based on this analysis, the universal data model should include:

1. **Physical Layout**: Key positions, sizes, rotations
2. **Matrix Information**: Row/column mapping for electrical matrix
3. **Key Assignments**: What each key does (keycodes)
4. **Layer Support**: Multiple layers with inheritance
5. **Metadata**: Keyboard identification and properties
6. **Visual Properties**: Colors, fonts, alignment (for KLE compatibility)

This comprehensive model will allow lossless conversion between formats while maintaining all necessary information for each target format.
