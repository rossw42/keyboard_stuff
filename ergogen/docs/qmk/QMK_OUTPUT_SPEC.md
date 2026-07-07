# QMK Output Specification

This document defines the exact QMK configuration files that will be generated and their expected content for the `config_4x5.yaml` test case.

## 📁 Target Output Structure

```
keyboard_config/
├── config.h           # Hardware configuration
├── keyboard.h         # Layout definitions  
├── rules.mk          # Build configuration
├── info.json         # QMK Configurator metadata
└── keymap.c          # Default keymap (optional)
```

## ⚙️ config.h - Hardware Configuration

### Generated Content

```c
/*
 * config.h
 * Generated from config_4x5.yaml by ergogen_to_qmk_converter
 */

#pragma once

#include "config_common.h"

// Basic keyboard information
#define VENDOR_ID    0x1234
#define PRODUCT_ID   0x5678
#define DEVICE_VER   0x0001
#define MANUFACTURER "Custom"
#define PRODUCT      "keyboard_numpad"

// Matrix configuration
#define MATRIX_ROWS 7  // 5 main rows + 2 encoder/thumb rows
#define MATRIX_COLS 6  // 4 numpad cols + 1 nav col + 1 thumb col

// Pin assignments (Pro Micro)
#define MATRIX_ROW_PINS { GP10, GP14, GP15, GP16, GP21, GP18, GP6 }
#define MATRIX_COL_PINS { GP0, GP1, GP2, GP3, GP5, GP4 }

// Matrix settings
#define COL_TO_ROW
#define DEBOUNCE 5

// Encoder configuration
#define ENCODER_ENABLE
#define ENCODERS_PAD_A { GP7, GP8, GP9 }
#define ENCODERS_PAD_B { encoder_left_b, encoder_right_b, encoder_bottom_b }
#define ENCODER_RESOLUTION 4

// OLED configuration
#define OLED_DISPLAY_128X64
#define OLED_TIMEOUT 60000
#define I2C_DRIVER I2CD1
#define I2C1_SCL_PIN GP2
#define I2C1_SDA_PIN GP3

// USB configuration
#define USB_POLLING_INTERVAL_MS 1
#define QMK_KEYS_PER_SCAN 4

// Feature flags
#define NO_ACTION_MACRO
#define NO_ACTION_FUNCTION
```

### Data Sources from Ergogen

| Config Setting | Ergogen Source | Example Value |
|---|---|---|
| `MATRIX_ROWS` | Count of unique row_net values | `5` (row0-row4) + encoders |
| `MATRIX_COLS` | Count of unique column_net values | `6` (col0-col3, col_left, col_thumb) |
| `MATRIX_ROW_PINS` | Controller params (row pins) | `P10: row0, P14: row1, ...` |
| `MATRIX_COL_PINS` | Controller params (col pins) | `P0: col0, P1: col1, ...` |
| `ENCODERS_PAD_A/B` | Encoder footprint params | `A: encoder_left_a, B: encoder_left_b` |
| `I2C1_SCL/SDA_PIN` | OLED footprint params | `P2: SCL, P3: SDA` |

## 🎹 keyboard.h - Layout Definitions

### Generated Content

```c
/*
 * keyboard.h
 * Generated from config_4x5.yaml by ergogen_to_qmk_converter
 */

#pragma once

#include "quantum.h"

// Main layout macro for the numpad with encoders
#define LAYOUT_numpad( \
    k00, k01, k02, k03,           \
    k10, k11, k12, k13,           \
    k20, k21, k22,                \
    k30, k31, k32, k33,           \
    k40,      k42,                \
    kNL0, kNL1, kNL2, kNL3, kNL4, \
    kE0, kE1, kE2,                \
    kT0                           \
) { \
    { k00,   k01,   k02,   k03,   KC_NO, KC_NO }, \
    { k10,   k11,   k12,   k13,   KC_NO, KC_NO }, \
    { k20,   k21,   k22,   KC_NO, KC_NO, KC_NO }, \
    { k30,   k31,   k32,   k33,   KC_NO, KC_NO }, \
    { k40,   KC_NO, k42,   KC_NO, KC_NO, KC_NO }, \
    { kNL0,  kNL1,  kNL2,  kNL3,  kNL4,  KC_NO }, \
    { kE0,   kE1,   kE2,   KC_NO, KC_NO, kT0   }  \
}

// Alternative compact layout
#define LAYOUT LAYOUT_numpad
```

### Layout Logic

**Matrix Mapping Strategy:**
1. **Numpad Keys**: Mapped to positions (row, col) based on their zone positions
2. **Navigation Column**: Mapped to dedicated columns  
3. **Special Keys**: 2U keys occupy single matrix position but may span visually
4. **Encoders**: Treated as regular keys with dedicated matrix positions
5. **Non-existent Positions**: Filled with `KC_NO`

**Key Position Calculation:**
```
Matrix Position = (zone_row_index, zone_col_index + zone_col_offset)
```

## ⚙️ rules.mk - Build Configuration

### Generated Content

```makefile
# rules.mk
# Generated from config_4x5.yaml by ergogen_to_qmk_converter

# MCU name
MCU = atmega32u4

# Processor frequency
F_CPU = 16000000

# Architecture
ARCH = AVR8

# Input clock frequency
F_USB = $(F_CPU)

# Interrupt driven control endpoint task
OPT_DEFS += -DINTERRUPT_CONTROL_ENDPOINT

# Bootloader selection
BOOTLOADER = caterina

# Build Options (change yes to no to disable)
BOOTMAGIC_ENABLE = yes      # Enable Bootmagic Lite
MOUSEKEY_ENABLE = yes       # Mouse keys
EXTRAKEY_ENABLE = yes       # Audio control and System control
CONSOLE_ENABLE = no         # Console for debug
COMMAND_ENABLE = no         # Commands for debug and configuration
NKRO_ENABLE = yes           # Enable N-Key Rollover
BACKLIGHT_ENABLE = no       # Enable keyboard backlight functionality
RGBLIGHT_ENABLE = no        # Enable keyboard RGB underglow
AUDIO_ENABLE = no           # Audio output

# Hardware feature enables (detected from Ergogen)
ENCODER_ENABLE = yes        # Enable rotary encoders
OLED_ENABLE = yes           # Enable OLED display support
OLED_DRIVER = SSD1306       # OLED driver type

# Additional features (disabled by default)
BLUETOOTH_ENABLE = no       # Enable Bluetooth
MIDI_ENABLE = no           # MIDI support
UNICODE_ENABLE = no        # Unicode
SPLIT_KEYBOARD = no        # Split keyboard support
```

### Feature Detection Logic

| Ergogen Feature | Detection Method | rules.mk Setting |
|---|---|---|
| Rotary encoders | `footprints: encoder_*` entries | `ENCODER_ENABLE = yes` |
| OLED display | `footprints: oled_screen` entry | `OLED_ENABLE = yes` |
| RGB LEDs | `footprints: rgb_*` entries | `RGBLIGHT_ENABLE = yes` |
| Audio | `footprints: speaker` entry | `AUDIO_ENABLE = yes` |
| Split design | Multiple `controller` entries | `SPLIT_KEYBOARD = yes` |

## 📋 info.json - QMK Configurator Metadata

### Generated Content

```json
{
    "keyboard_name": "keyboard_numpad",
    "manufacturer": "Custom",
    "url": "",
    "maintainer": "cline",
    "usb": {
        "vid": "0x1234",
        "pid": "0x5678",
        "device_version": "0.0.1"
    },
    "matrix_pins": {
        "cols": ["GP0", "GP1", "GP2", "GP3", "GP5", "GP4"],
        "rows": ["GP10", "GP14", "GP15", "GP16", "GP21", "GP18", "GP6"]
    },
    "diode_direction": "COL2ROW",
    "encoder": {
        "rotary": [
            {"pin_a": "GP7", "pin_b": "encoder_left_b", "resolution": 4},
            {"pin_a": "GP8", "pin_b": "encoder_right_b", "resolution": 4},
            {"pin_a": "GP9", "pin_b": "encoder_bottom_b", "resolution": 4}
        ]
    },
    "processor": "atmega32u4",
    "bootloader": "caterina",
    "layouts": {
        "LAYOUT_numpad": {
            "layout": [
                {"matrix": [0, 0], "x": 0, "y": 0, "w": 1, "h": 1},
                {"matrix": [0, 1], "x": 1, "y": 0, "w": 1, "h": 1},
                {"matrix": [0, 2], "x": 2, "y": 0, "w": 1, "h": 1},
                {"matrix": [0, 3], "x": 3, "y": 0, "w": 1, "h": 1},
                
                {"matrix": [1, 0], "x": 0, "y": 1, "w": 1, "h": 1},
                {"matrix": [1, 1], "x": 1, "y": 1, "w": 1, "h": 1},
                {"matrix": [1, 2], "x": 2, "y": 1, "w": 1, "h": 1},
                {"matrix": [1, 3], "x": 3, "y": 1, "w": 1, "h": 2},
                
                {"matrix": [2, 0], "x": 0, "y": 2, "w": 1, "h": 1},
                {"matrix": [2, 1], "x": 1, "y": 2, "w": 1, "h": 1},
                {"matrix": [2, 2], "x": 2, "y": 2, "w": 1, "h": 1},
                
                {"matrix": [3, 0], "x": 0, "y": 3, "w": 1, "h": 1},
                {"matrix": [3, 1], "x": 1, "y": 3, "w": 1, "h": 1},
                {"matrix": [3, 2], "x": 2, "y": 3, "w": 1, "h": 1},
                {"matrix": [3, 3], "x": 3, "y": 3, "w": 1, "h": 2},
                
                {"matrix": [4, 0], "x": 0, "y": 4, "w": 2, "h": 1},
                {"matrix": [4, 2], "x": 2, "y": 4, "w": 1, "h": 1},
                
                {"matrix": [5, 0], "x": -1.25, "y": 0, "w": 1, "h": 1},
                {"matrix": [5, 1], "x": -1.25, "y": 1, "w": 1, "h": 1},
                {"matrix": [5, 2], "x": -1.25, "y": 2, "w": 1, "h": 1},
                {"matrix": [5, 3], "x": -1.25, "y": 3, "w": 1, "h": 1},
                {"matrix": [5, 4], "x": -1.25, "y": 4, "w": 1, "h": 1},
                
                {"matrix": [6, 0], "x": 4.5, "y": 0, "w": 1, "h": 1},
                {"matrix": [6, 1], "x": 5.5, "y": 0, "w": 1, "h": 1},
                {"matrix": [6, 2], "x": 5, "y": 2, "w": 1, "h": 1},
                {"matrix": [6, 5], "x": 5, "y": 4, "w": 1.5, "h": 1}
            ]
        }
    },
    "features": {
        "bootmagic": true,
        "mousekey": true,
        "extrakey": true,
        "encoder": true,
        "oled": true,
        "nkro": true
    }
}
```

### Coordinate Conversion

**Ergogen → QMK Coordinate Mapping:**

1. **Extract Positions**: Parse `anchor.shift` and relative positions from Ergogen
2. **Calculate Absolute**: Resolve anchor references and calculate absolute mm positions  
3. **Normalize**: Translate so minimum x,y = 0,0
4. **Convert Units**: Divide by 19.05mm (1 key unit) to get key unit coordinates
5. **Round**: Round to 2 decimal places for clean JSON

**Special Key Handling:**
- **2U Width** (Zero key): `"w": 2` in layout
- **2U Height** (Plus/Enter): `"h": 2` in layout  
- **1.5U Width** (Thumb key): `"w": 1.5` in layout

## 🗂 File Generation Priority

### Phase 1: Core Files
1. **config.h** - Enables basic compilation
2. **keyboard.h** - Enables layout compilation  
3. **rules.mk** - Enables feature compilation

### Phase 2: QMK Configurator Support
4. **info.json** - Enables visual editor support

### Phase 3: User Experience
5. **keymap.c** - Provides working default keymap

## 🧪 Validation Requirements

### Compilation Test
Generated files must compile successfully with:
```bash
qmk compile -kb custom_keyboard -km default
```

### Feature Test
All detected features must work:
- Matrix scanning produces correct keycodes
- Encoders generate proper rotation events  
- OLED displays initialization messages
- Special keys (2U) produce single key events

### QMK Configurator Test
The `info.json` must:
- Load without errors in QMK Configurator
- Display correct visual layout
- Allow keymap editing for all positions
- Export functional keymap files

## 🔧 Implementation Notes

### Pin Name Conversion
Ergogen uses `GP10` format, QMK expects `GP10` (same format for Pro Micro).
Other controllers may need conversion (Elite-C uses `B0`, `D4`, etc.).

### Matrix Size Optimization
The generated matrix should use minimal rows/cols by:
1. Analyzing actual key positions
2. Eliminating unused matrix positions
3. Compacting to reduce GPIO usage

### Feature Auto-Detection
Features are enabled based on footprint presence:
```yaml
footprints:
  encoder_left: rotary     → ENCODER_ENABLE = yes
  oled_screen: oled       → OLED_ENABLE = yes  
  rgb_strip: rgb          → RGBLIGHT_ENABLE = yes
```

This specification ensures the converter generates complete, functional QMK configurations that compile successfully and support all hardware features defined in the Ergogen file.
