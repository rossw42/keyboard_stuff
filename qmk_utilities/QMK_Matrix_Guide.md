# Understanding QMK Matrix Configuration: matrix_pins, layouts, and LAYOUT

This guide explains the relationships between `matrix_pins`, `layouts` definitions in `keyboard.json`, and `LAYOUT` macros in `keymap.c` files. These three components work together to map physical keys to logical positions in your QMK firmware.

## [Reasoning]
- Step 1: Found Planck and 1up60hse as contrasting examples
- Step 2: Analyzed matrix_pins configurations in both keyboards  
- Step 3: Studied layout definitions showing matrix coordinates
- Step 4: Examined LAYOUT macros in keymap.c files
- Step 5: Connected physical pins to logical positions

## Overview: The Three Components

### 1. `matrix_pins` - Physical GPIO Configuration
Defines which microcontroller pins are used for the keyboard matrix:
```json
"matrix_pins": {
    "cols": ["C7", "F7", "F6", "F5", "F4", "F1", "E6", "D1", "D0", "D2", "D3", "D5", "D6", "D7"],
    "rows": ["B3", "B2", "B1", "B0", "D4"]
}
```

### 2. `layouts` - Logical Key Mapping
Maps matrix positions to physical key locations:
```json
"layouts": {
    "LAYOUT_60_ansi": {
        "layout": [
            {"matrix": [0, 0], "x": 0, "y": 0},
            {"matrix": [0, 1], "x": 1, "y": 0},
            // ... more keys
        ]
    }
}
```

### 3. `LAYOUT` Macros - Keymap Definition
Assigns keycodes to each position in the layout:
```c
[0] = LAYOUT_60_ansi(
    KC_ESC, KC_1, KC_2, KC_3, // First row
    KC_TAB, KC_Q, KC_W, KC_E, // Second row
    // ... more rows
)
```

## How They Work Together

### Simple Example: 1up60hse (Traditional Matrix)

The 1up60hse uses a straightforward 5×14 matrix:

#### 1. Matrix Pins Configuration
- **5 rows**: `["B3", "B2", "B1", "B0", "D4"]`
- **14 columns**: `["C7", "F7", "F6", "F5", "F4", "F1", "E6", "D1", "D0", "D2", "D3", "D5", "D6", "D7"]`
- **Diode direction**: `"COL2ROW"` (current flows from column to row)

#### 2. Matrix Scanning Process
```
Row 0 (B3): [0,0] [0,1] [0,2] [0,3] [0,4] [0,5] [0,6] [0,7] [0,8] [0,9] [0,10] [0,11] [0,12] [0,13]
Row 1 (B2): [1,0] [1,1] [1,2] [1,3] [1,4] [1,5] [1,6] [1,7] [1,8] [1,9] [1,10] [1,11] [1,12] [1,13]
Row 2 (B1): [2,0] [2,1] [2,2] [2,3] [2,4] [2,5] [2,6] [2,7] [2,8] [2,9] [2,10] [2,11] --- [2,13]
Row 3 (B0): [3,0] [3,1] [3,2] [3,3] [3,4] [3,5] [3,6] [3,7] [3,8] [3,9] [3,10] --- --- [3,13]
Row 4 (D4): [4,0] [4,1] [4,2] --- --- [4,5] --- --- --- [4,9] [4,10] [4,11] --- [4,13]
```

#### 3. Layout Definition Order
The `LAYOUT_60_ansi` macro parameters must be in the same order as defined in the layout:
```c
// Layout order matches the sequence in keyboard.json
LAYOUT_60_ansi(
    // Row 0: positions [0,0] through [0,13]
    KC_ESC, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0, KC_MINS, KC_EQL, KC_BSPC,
    // Row 1: positions [1,0] through [1,13]  
    KC_TAB, KC_Q, KC_W, KC_E, KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_P, KC_LBRC, KC_RBRC, KC_BSLS,
    // etc...
)
```

**Key Insight**: The matrix coordinates `[row, col]` correspond directly to:
- `row` = index in the `rows` array 
- `col` = index in the `cols` array

### Complex Example: Planck (Split Matrix)

The Planck uses a more complex **split matrix** design with 8 rows and 6 columns:

#### 1. Matrix Pins Configuration
- **6 columns**: `["B11", "B10", "B2", "B1", "A7", "B0"]`
- **8 rows**: `["A10", "A9", "A8", "B15", "C13", "C14", "C15", "A2"]`

#### 2. Split Matrix Layout
Unlike traditional matrices, the Planck doesn't fill all positions sequentially:

```
Physical Layout:    Matrix Positions:
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐    ┌─────┬─────┬─────┬─────┬─────┬─────┐
│ │ │ │ │ │ │ │ │ │ │ │ │    │[0,0]│[0,1]│[0,2]│[0,3]│[0,4]│[0,5]│
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤    ├─────┼─────┼─────┼─────┼─────┼─────┤
│ │ │ │ │ │ │ │ │ │ │ │ │    │[1,0]│[1,1]│[1,2]│[1,3]│[1,4]│[1,5]│
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤    ├─────┼─────┼─────┼─────┼─────┼─────┤
│ │ │ │ │ │ │ │ │ │ │ │ │    │[2,0]│[2,1]│[2,2]│[2,3]│[2,4]│[2,5]│
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤    ├─────┼─────┼─────┼─────┼─────┼─────┤
│ │ │ │ │ │ │ │ │ │ │ │ │    │[3,0]│[3,1]│[3,2]│[7,3]│[7,4]│[7,5]│
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘    └─────┴─────┴─────┴─────┴─────┴─────┘

                                ┌─────┬─────┬─────┬─────┬─────┬─────┐
                Right half:     │[4,0]│[4,1]│[4,2]│[4,3]│[4,4]│[4,5]│
                                ├─────┼─────┼─────┼─────┼─────┼─────┤
                                │[5,0]│[5,1]│[5,2]│[5,3]│[5,4]│[5,5]│
                                ├─────┼─────┼─────┼─────┼─────┼─────┤
                                │[6,0]│[6,1]│[6,2]│[6,3]│[6,4]│[6,5]│
                                ├─────┼─────┼─────┼─────┼─────┼─────┤
                                │[7,0]│[7,1]│[7,2]│[3,3]│[3,4]│[3,5]│
                                └─────┴─────┴─────┴─────┴─────┴─────┘
```

#### 3. Why Split Matrix?
This design allows the Planck to:
- Use fewer GPIO pins (14 instead of 24 for a traditional 4×12 matrix)
- Route PCB traces more efficiently 
- Reduce manufacturing complexity

The trade-off is more complex firmware configuration.

## Common Confusion Points

### 1. "Missing" Matrix Positions
In both examples, you'll notice some matrix positions are unused:
- **1up60hse**: `[2,12]`, `[3,11]`, `[3,12]`, `[4,3]`, `[4,4]`, `[4,6]`, `[4,7]`, `[4,8]`, `[4,12]`
- **Planck**: Various positions not used due to split design

**This is normal!** Not every matrix position needs a physical key.

### 2. Layout Order vs Matrix Position
The order of keys in the `LAYOUT` macro matches the order in the `layouts` definition, **NOT** the matrix scanning order.

Example from 1up60hse:
```json
// In keyboard.json - this determines LAYOUT macro order
{"matrix": [0, 0], "x": 0, "y": 0},    // 1st parameter
{"matrix": [0, 1], "x": 1, "y": 0},    // 2nd parameter  
{"matrix": [0, 2], "x": 2, "y": 0},    // 3rd parameter
```

```c
// In keymap.c - parameters must match layout order
LAYOUT_60_ansi(
    KC_ESC,  // Goes to [0,0] - 1st in layout
    KC_1,    // Goes to [0,1] - 2nd in layout
    KC_2,    // Goes to [0,2] - 3rd in layout
    // ...
)
```

### 3. Physical vs Logical Coordinates
- **Matrix coordinates** `[row, col]`: Physical electrical connections
- **Layout coordinates** `"x": N, "y": N`: Visual positioning for configurators
- **LAYOUT order**: The sequence parameters appear in the macro

## Key Takeaways

1. **`matrix_pins`** defines the electrical connections - which GPIO pins are used
2. **`layouts`** maps each matrix position to a logical key location 
3. **`LAYOUT` macros** assign keycodes in the order defined by the layout
4. The three systems work together but serve different purposes
5. Complex designs like split matrices can optimize GPIO usage but require careful configuration
6. Not all matrix positions need to have physical keys
7. Always follow the layout definition order when writing keymaps

## Debugging Tips

When keys don't work as expected:

1. **Check matrix coordinates**: Verify the `[row, col]` values in your layout definition
2. **Verify pin assignments**: Ensure `matrix_pins` match your physical wiring
3. **Confirm layout order**: Make sure your `LAYOUT` macro parameters match the sequence in `layouts`
4. **Test individual positions**: Use `KC_NO` to skip problematic positions while debugging
5. **Check diode direction**: Ensure `diode_direction` matches your physical wiring

Understanding these relationships will help you troubleshoot matrix issues and create custom keyboard configurations more effectively.