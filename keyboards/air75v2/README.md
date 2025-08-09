# NuPhy Air75 V2 Keyboard Layout

This repository contains the custom keyboard layout configuration for the NuPhy Air75 V2 mechanical keyboard. The layout is organized into multiple layers to provide extensive functionality while maintaining a compact 75% form factor.

## Layer Overview

The keyboard uses 8 layers in total, with the first 5 layers actively configured and the last 3 reserved for future use.

### Layer 0: Main Layer (Base QWERTY Layout)
The primary typing layer with standard QWERTY layout optimized for general use.

- **Standard QWERTY** alphanumeric keys
- **Function keys** (F1-F12)
- **Navigation cluster**: Home, End, Page Up, Page Down
- **Editing keys**: Insert, Delete, Print Screen
- **Arrow keys** in the bottom right
- **Modifier keys**: Ctrl, GUI/Win, Alt (in Mac order on the left side: Ctrl, GUI, Alt)
- Hold the key to the right of right Alt to access Layer 3

### Layer 1: Media & Mac Function Layer
Accessible through function combinations, this layer provides media controls and custom functions.

- **Screen brightness** controls (F1-F2)
- **Media controls**:
  - Previous track (F7)
  - Play/Pause (F8)
  - Next track (F9)
  - Mute (F10)
  - Volume down/up (F11-F12)
- **Custom functions** in number row:
  - CUSTOM(2), CUSTOM(3), CUSTOM(4), CUSTOM(5) - Likely Mac-specific functions
  - CUSTOM(18), CUSTOM(19), CUSTOM(20) - Additional custom functions
  - CUSTOM(10) - Print Screen alternative
- **RGB lighting controls**:
  - RGB speed controls (RGB_SPD, RGB_SPI)
  - RGB brightness control (RGB_VAI, RGB_VAD)
  - RGB mode/pattern (RGB_MOD)
  - RGB hue control (RGB_HUI)
- Access to Layer 4 for advanced functions

### Layer 2: Windows/Alternative Base Layer
A duplicate of Layer 0, likely maintained as a Windows-specific or alternate base layer.

- Identical to Layer 0 with QWERTY layout
- Allows for maintaining separate but similar base layouts
- Useful when switching between different operating systems

### Layer 3: Extended Function Layer
Provides access to extended functionality similar to Layer 1 but with different mappings.

- **Custom functions** in number row: CUSTOM(2), CUSTOM(3), CUSTOM(4), CUSTOM(5)
- **Additional custom functions**: CUSTOM(18), CUSTOM(19), CUSTOM(20)
- **RGB lighting controls**:
  - RGB speed controls (RGB_SPD, RGB_SPI)
  - RGB brightness control (RGB_VAI, RGB_VAD)
  - RGB mode (RGB_MOD)
  - RGB hue control (RGB_HUI)
- Access to Layer 4 for advanced functions

### Layer 4: Advanced Function Layer
The deepest function layer with specialized controls.

- **Advanced RGB controls**: CUSTOM(12), CUSTOM(13), CUSTOM(14), CUSTOM(15), CUSTOM(16), CUSTOM(17)
- Used for keyboard configuration and special functions
- Accessible from both Layer 1 and Layer 3

### Layers 5-7: Reserved
These layers are currently transparent (all keys set to KC_TRNS) and reserved for future customization.

## Custom Functions

The keyboard includes several custom functions (CUSTOM), likely programmed for specific tasks:

- **CUSTOM(2-5)**: App switching or OS-specific shortcuts
- **CUSTOM(10)**: Alternative screenshot or screen capture
- **CUSTOM(12-17)**: Advanced RGB lighting modes or effects
- **CUSTOM(18-20)**: Application launching or specialized tools

## Key Layout Diagram

```
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│Esc│F1 │F2 │F3 │F4 │F5 │F6 │F7 │F8 │F9 │F10│F11│F12│   │Del│
├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
│Ins│ ` │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ = │Bsp│
├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
│Hom│Tab│ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │ [ │ ] │ \  │
├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
│PUp│Cap│ A │ S │ D │ F │ G │ H │ J │ K │ L │ ; │ ' │   │Ent│
├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
│End│   │Sft│ Z │ X │ C │ V │ B │ N │ M │ , │ . │ / │Sft│ ↑ │
├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
│PgD│   │Ctl│GUI│Alt│   │   │   │Spc│   │   │Alt│Fn │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
│PSc│   │   │   │   │   │   │   │   │   │   │   │ ← │ ↓ │ → │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
```

## Usage Tips

1. **Layer Switching:**
   - Hold the key to the right of right Alt (MO(3)) to access Layer 3
   - From Layers 1 and 3, you can access Layer 4 with MO(4)

2. **RGB Lighting:**
   - Use Layers 1, 3, and 4 to adjust RGB lighting effects
   - Layer 4 provides advanced RGB customization options

3. **Operating System Compatibility:**
   - Layer 0 and 2 provide similar layouts, potentially optimized for different operating systems
   - Custom functions likely provide OS-specific functionality

4. **Media Controls:**
   - Access media and brightness controls through Layer 1

## Configuration

This layout is configured for use with the VIA keyboard customization tool. The JSON file can be loaded into VIA to customize the keyboard's behavior or make adjustments to the layers.
