# NuPhy Air75 V2 - Tofu Enhanced Layout

## Overview
This layout combines features from the NuPhy Air75 V2 and DZ60 Tofu keyboards, creating a productivity-focused layout with F-keys on layer 0 and enhanced macros from the Tofu layout.

## Layer 0 (Base Layer) - Key Features

### Top Row
- **F1-F12**: Full function key row for immediate access (no Fn required)
- **Mute**: Volume mute button
- **RGB_M_P**: RGB mode previous

### Navigation Cluster (Right Side)
- **HOME Position**: `TG(7)` - Toggles Layer 7 on/off
- **Delete**: Standard delete key  
- **End**: End key
- **Right Control**: `KC_RCTL` on right cluster

### Special Shift Keys
- **Left Shift**: `KC_LSPO` - Hold for shift, tap for `(` 
- **Right Shift**: `KC_RSPC` - Hold for shift, tap for `)`

### Close Tab Shortcut
- **Backslash Position**: `MACRO(15)` - Empty macro (customizable)

### Standard Keys
- Standard QWERTY layout maintained
- Backspace, Tab, Caps Lock, Enter all in normal positions
- Arrow cluster at bottom right

### Bottom Row
- **Space**: `LT(1,KC_SPC)` - Hold for Layer 1, tap for space
- **Fn Key**: `MO(2)` - Access Layer 2 while held

## Layer 1 (Productivity Layer) - Hold Space

### Media Controls (Top Row)
- **F2/F3**: Brightness down/up
- **F7/F8/F9**: Previous/Play-Pause/Next track
- **F10/F11/F12**: Mute/Vol Down/Vol Up

### Clipboard Operations (Bottom Left)
- **Z**: `MACRO(0)` - Undo (Ctrl+Z)
- **X**: `MACRO(1)` - Cut (Ctrl+X)
- **C**: `MACRO(2)` - Copy (Ctrl+C)
- **V**: `MACRO(3)` - Paste (Ctrl+V)
- **B**: `MACRO(4)` - Line Start (Cmd+Left)

### Text Editing (Home Row)
- **A**: `MACRO(7)` - Select All (Ctrl+A)
- **F**: `MACRO(8)` - Find (Ctrl+F)

### Vim-Style Navigation (HJKL)
- **H**: Left Arrow
- **J**: Down Arrow  
- **K**: Up Arrow
- **L**: Right Arrow

### Window Management (Bottom Row)
- **M**: `G(KC_LEFT)` - Move window left (Cmd+Left)
- **N**: `G(KC_RGHT)` - Move window right (Cmd+Right)
- **< (Comma)**: `G(KC_UP)` - Mission Control/Expose (Cmd+Up)
- **. (Period)**: `MACRO(5)` - Line End (Cmd+Right)

### Additional Navigation
- **Right Arrow Key**: Added for convenience

## Layer 2 (Mouse & Media) - Hold Fn

### Mouse Controls (WASD Area)
- **Q**: Mouse Button 1 (Left Click)
- **W**: Mouse Up
- **E**: Mouse Button 2 (Right Click)  
- **A**: Mouse Left
- **S**: Mouse Down
- **D**: Mouse Right

### Vim Arrows (HJKL)
- **H/J/K/L**: Arrow keys (redundant with layer 0)

### Utilities
- **Z**: `MACRO(9)` - Redo (Ctrl+Y)
- **C**: Calculator app shortcut

### RGB Controls (Bottom Right)
- **Up**: RGB Value Increase
- **Down**: RGB Value Decrease  
- **Left**: RGB Mode
- **Right**: RGB Hue Increase

### Mouse Buttons (Bottom Right Cluster)
- **RAlt**: Mouse Button 1
- **Fn Position**: Mouse Button 3 (Middle Click)
- **Right**: Mouse Button 2

## Layer 3 (Extended Navigation)

### F-Key Access (Number Row)
- **1-9, 0, -, =**: Maps to F1-F12 (redundant F-key access)

### Layer Toggles
- **1-4**: `TT(1)` through `TT(4)` - Toggle-tap layers 1-4

### Navigation Cluster (QWER)
- **Q**: Home
- **W**: Up Arrow
- **E**: End
- **R**: Page Up

### Vim Arrows (ASDF)
- **A**: Left Arrow
- **S**: Down Arrow
- **D**: Right Arrow
- **F**: Page Down

### Word Navigation
- **Z**: `MACRO(10)` - Word Back (Ctrl+Left)
- **X**: `MACRO(11)` - Word Forward (Ctrl+Right)

### RGB Controls (Bottom Right)
- Toggle, mode changes, brightness controls

## Layer 7 (Advanced) - Toggle via HOME

### Layer Control (Number Row)
- **1-8**: `TG(0)` through `TG(7)` - Toggle individual layers

### Navigation (QWER Area)
- **Q**: Home
- **W**: Up
- **E**: End  
- **R**: Page Up
- **A/S/D/F**: Left/Down/Right/Page Down

### Mouse Movement (ASDF Area)
- **A**: Mouse Left
- **S**: Mouse Down
- **K**: Mouse Up
- **D**: Mouse Right

### Volume Control
- **,** (Comma): Volume Up
- **RAlt Position**: `MACRO(12)` - Cmd+Left
- **.** (Period): Volume Down

### Quick Access
- Toggle this layer on/off using HOME key from Layer 0

## Complete Macro Reference

| # | Keycode | Function | Used On |
|---|---------|----------|---------|
| 0 | `{+KC_LCTL}z{-KC_LCTL}` | Undo (Ctrl+Z) | Layer 1: Z |
| 1 | `{+KC_LCTL}x{-KC_LCTL}` | Cut (Ctrl+X) | Layer 1: X |
| 2 | `{+KC_LCTL}c{-KC_LCTL}` | Copy (Ctrl+C) | Layer 1: C |
| 3 | `{+KC_LCTL}v{-KC_LCTL}` | Paste (Ctrl+V) | Layer 1: V |
| 4 | `{+KC_LGUI}{+KC_LEFT}{-KC_LGUI}` | Line Start (Cmd+Left) | Layer 1: B |
| 5 | `{+KC_LGUI}{+KC_RGHT}{-KC_LGUI}` | Line End (Cmd+Right) | Layer 1: Period |
| 6 | `{+KC_LGUI}{+KC_UP}{-KC_LGUI}` | Mission Control (Cmd+Up) | (Reserved) |
| 7 | `{+KC_LCTL}a{-KC_LCTL}` | Select All (Ctrl+A) | Layer 1: A |
| 8 | `{+KC_LCTL}f{-KC_LCTL}` | Find (Ctrl+F) | Layer 1: F |
| 9 | `{+KC_LCTL}y{-KC_LCTL}` | Redo (Ctrl+Y) | Layer 2: Z |
| 10 | `{KC_LCTL,KC_LEFT}` | Word Back (Ctrl+Left) | Layer 3: Z |
| 11 | `{KC_LCTL,KC_RGHT}` | Word Forward (Ctrl+Right) | Layer 3: X |
| 12 | `{KC_LGUI,KC_LEFT}` | Cmd+Left | Layer 7: RAlt pos |
| 13 | `{KC_LGUI,KC_RGHT}` | Cmd+Right | (Available) |
| 14 | `{KC_LCTL,KC_LSFT,KC_T}` | Reopen Tab (Ctrl+Shift+T) | (Available) |
| 15 | (Empty) | Customizable | Layer 0: \ position |

## Quick Reference

### Layer 1 (Hold Space)
```
Clipboard:      Z: Undo   X: Cut    C: Copy   V: Paste   B: Line Start
Text Edit:      A: Select All       F: Find
Vim Nav:        H: ←      J: ↓      K: ↑      L: →
Windows:        M: Win ←  N: Win →  ,: Expose .: Line End
```

### Layer 2 (Hold Fn)
```
Mouse:          Q: Click  W: Up     E: R-Click
                A: Left   S: Down   D: Right
Vim Nav:        H: ←      J: ↓      K: ↑       L: →
Utils:          Z: Redo   C: Calculator
```

### Layer 3
```
F-Keys:         1-9,0,-,=: F1-F12
Nav Cluster:    Q: Home   W: ↑      E: End    R: PgUp
                A: ←      S: ↓      D: →      F: PgDn
Word Nav:       Z: Word ← X: Word →
```

### Layer 7 (Toggle with HOME)
```
Layer Toggle:   1-8: Toggle layers 0-7
Navigation:     Q/W/E/R: Home/↑/End/PgUp
                A/S/D/F: ←/↓/→/PgDn
Mouse:          ASDF: Mouse movement
Volume:         ,: Vol Up  .: Vol Down
```

## Design Highlights

### 1. F-Keys Always Available
F1-F12 on layer 0 top row - never need Fn to access them

### 2. Shift Parentheses
- Tap shifts for `(` and `)`
- Hold shifts for normal shift behavior
- Reduces pinky reach for programmers

### 3. Direct Window Management
Layer 1 uses native keycodes (`G(KC_*)`) instead of macros for instant window switching on macOS

### 4. Clipboard Efficiency  
All clipboard operations (Undo/Cut/Copy/Paste) on left hand home row for fast access

### 5. Layer 7 Toggle
HOME key toggles Layer 7 for quick access to layer controls and utilities

## Installation

1. Open VIA or Vial software
2. Import: `nuphy_air75_v2_tofu_enhanced.layout.json`
3. Test F-keys on layer 0
4. Test Space+ZXCV for clipboard
5. Test Space+HJKL for arrows
6. Test HOME toggle for Layer 7
7. Customize MACRO(15) as needed

## Usage Tips

- **Clipboard workflow**: Space+Z (undo), Space+X (cut), Space+C (copy), Space+V (paste)
- **Window switching**: Space+M (left), Space+N (right), Space+Comma (expose)
- **Navigation**: Space+HJKL for arrows, Space+Period for line end
- **Mouse control**: Fn+QWEASD for complete mouse navigation
- **Layer 7**: Toggle with HOME for layer controls and volume

## Troubleshooting

**F-keys not working:**
- They should work immediately on layer 0 without Fn
- Check firmware version

**Shift parentheses not working:**
- Tap shift quickly for `(` or `)`
- Hold longer for normal shift

**Layer 7 stuck on:**
- Press HOME again to toggle off
- Check TG(7) assignment

**Import errors:**
- File must have 102 keys × 8 layers = 816 keys total
- Ensure JSON is valid

## Credits

- Base: NuPhy Air75 V2 default  
- Macros: DZ60 Tofu keyboard inspiration
- Window mgmt: Direct macOS Cmd+Arrow keycodes
- Enhanced: Custom layers 0-1 for optimal workflow
