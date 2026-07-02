# Vial JSON Derivation Analysis

This document details the transformation from `keyboard.json` to `vial.json` for specific keyboards. Based on analysis of multiple keyboards (e.g., **egg58**, **discipline**, and **altair_x**), it is clear that there is no single universal transformation; the derivation is highly dependent on the specific physical layout and intended behavior of each keyboard.

## General Observations (Applicable to most)
- **Metadata**: `keyboard_name` maps to `name`, `usb.vid` to `vendorId`, and `usb.pid` to `productId`.
- **Lighting**: Often hardcoded (e.g., `"vialrgb"`, `"qmk_backlight"`, or derived from `backlight` pins).
- **Matrix**: Rows and columns are derived from the layout dimensions.

---

## Case Study: egg58
**Source**: `D:\GitHub2\vial-qmk\keyboards\eggsworks\egg58\keyboard.json`
**Target**: `D:\GitHub2\vial-qmk\keyboards\eggsworks\egg58\keymaps\vial\vial.json`

### Layout Logic
- **Interleaved Row Ordering**: The `keymap` follows a non-standard interleaved sequence: Rows 0, 5, 1, 6, 2, 7, 3, 8, 4, 9.
- **Coordinate Flattening**: 
    - `x` coordinates are largely preserved.
    - `y` coordinates are often "flattened" or overwritten with constant values for specific rows (e.g., Rows 1, 2, 3 in `egg58` have constant `y` values for columns 1-5).
    - Leading keys in Rows 0-3 follow a specific formula: `y = row_index + 0.93`.

---

## Case Study: discipline
**Source**: `D:\GitHub2\vial-qmk\keyboards\coseyfannitutti\discipline\keyboard.json`
**Target**: `D:\GitHub2\vial-qmk\keyboards\coseyfannitutti\discipline\keymaps\vial\vial.json`

### Layout Logic
- **Row-Sequential Ordering**: Unlike `egg58`, this layout follows a standard sequential row progression (Row 0, 1, 2, 3, 4).
- **Rich Coordinate Data**: 
    - Uses complex, non-integer `x` and `y` coordinates.
    - Includes additional properties like colors (`c`), and multi-dimensional dimensions (`w`, `h`, `w2`, `h2`, `x2`) for specific keys.
- **Stacked Keys**: Includes multi-layer key definitions (e.g., `"1,13\n\n\n0,0"`), representing keys that map to multiple matrix positions simultaneously.

---

## Case Study: altair_x
**Source**: `D:\GitHub2\vial-qmk\keyboards\ai03\altair_x\keyboard.json`
**Target**: `D:\GitHub2\vial-qmk\keyboards\ai03\altair_x\keymaps\vial\vial.json`

### Layout Logic
- **Complex Reordering**: The `keymap` order is significantly shuffled compared to standard row-by-row (e.g., Row 0, Row 4, Row 5, Row 1, Row 2, Row 6, Row 3, Row 7).
- **High Precision Coordinates**:
    - Uses highly precise `x` and `y` coordinates, often with many decimal places.
- **Advanced Key Properties**:
    - Uses rotation and scaling properties (`r`, `rx`, `ry`) for specific keys (e.g., Row 3, keys 3.4 through 7.2).
- **Stacked Keys**: Similar to `discipline`, it uses multi-layer key definitions (e.g., `"4,0\n\n\n2,0"`).

---

## Conclusion
The transformation from `keyboard.json` to `vial.json` is **not a global rule**. 

1.  **Ordering**: Can be interleaved, sequential, or arbitrarily shuffled depending on the physical layout.
2.  **Coordinates**: Can be "flattened" for simple layouts or use high-precision, multi-property data for complex ones.
3.  **Stacked Keys**: May be required for specific designs to handle complex key behaviors.
4.  **Rotations/Scaling**: Advanced layouts may introduce rotation (`r`) and relative coordinates (`rx`, `ry`).

When testing or creating new `vial.json` files, the `keyboard.json` should only be used as a reference for basic matrix indices and metadata; the actual layout, coordinates, and special behaviors must be tailored to the specific hardware.
