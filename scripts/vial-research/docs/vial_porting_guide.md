# VIAL Porting Guide: Converting QMK Keyboards to VIAL Format

## Overview

This document explains how to convert a non-VIAL QMK keyboard into a complete VIAL-enabled setup. Based on analysis of reference keyboards (`coseyfannitutti/discipline` and `jlw/bruce_the_keyboard`) in the [vial-qmk repository](https://github.com/vial-kb/vial-qmk), this guide covers all required files and their generation processes.

---

## Directory Structure Comparison

### Non-VIAL Keyboard (Default/Standard Setup)

```
keyboard_folder/
├── keyboard.json        # Layout definition for VIAL
├── info.json            # Metadata (optional, legacy)
├── rules.mk             # Build options
├── readme.md            # Documentation
└── keymaps/
    └── default/
        └── keymap.c     # Standard QMK keymap
```

### VIAL-Enabled Keyboard (Converted Setup)

```
keyboard_folder/
├── keyboard.json        # Layout definition for VIAL
├── info.json            # Metadata (optional, legacy)
├── rules.mk             # Build options (root level)
├── readme.md            # Documentation
├── RGB_UNDERGLOW_GUIDE.md  # Optional: Hardware guide
└── keymaps/
    ├── default/
    │   └── keymap.c     # Standard QMK keymap
    └── vial/
        ├── keymap.c           # VIAL-compatible keymap (can be same as default)
        ├── config.h            # VIAL-specific configuration
        ├── rules.mk            # Build options with VIAL/RGB enabled
        └── vial.json           # Layout definition for VIAL UI
```

---

## Files to Create in the `keymaps/vial` Directory

When converting a keyboard from non-VIAL to VIAL, you need to create these 4 files:

### 1. **vial.json** - Keyboard Layout Definition

**Purpose**: Defines the physical layout for the VIAL UI tool. Used by VIAL to display key positions and layouts.

**Source**: Directly generated from `keyboard.json` using the existing converter.

**Key Fields**:

- `name`: Keyboard display name (from `keyboard.json`)
- `vendorId`, `productId`: USB IDs (from `keyboard.json`)
- `lighting`: RGB backlight mode (`qmk_backlight`, `none`, or vendor-specific)
- `matrix.rows`, `matrix.cols`: Matrix dimensions from keyboard.json layouts
- `layouts.keymap`: Array of coordinate mappings with optional styling

**Generation**: Use `keyboard_to_vial_converter.py` - already implemented and tested.

---

### 2. **config.h** - VIAL-Specific Configuration

**Purpose**: Defines hardware-specific settings that only apply to VIAL-enabled builds.

**Required Fields**:

```c
#define VIAL_KEYBOARD_UID {0xXX, 0xXX, ...}   // Unique keyboard ID
#define VIAL_UNLOCK_COMBO_ROWS {r1, r2}       // Combo rows for unlock
#define VIAL_UNLOCK_COMBO_COLS {c1, c2}       // Combo columns for unlock
```

**Optional Fields** (keyboard-specific features):

```c
#define RGBLIGHT_DI_PIN XX            // LED data pin
#define RGBLED_NUM XX                 // Number of LEDs (for underglow)
#define RGBLIGHT_HUE_STEP XX          // Hue step value
#define RGBLIGHT_SAT_STEP XX          // Saturation step value
#define RGBLIGHT_VAL_STEP XX          // Brightness step value
#define RGBLIGHT_LIMIT_VAL XX         // Max brightness (0-255)
```

**RGB Effects** (uncomment to enable):

```c
#define RGBLIGHT_EFFECT_BREATHING
#define RGBLIGHT_EFFECT_RAINBOW_MOOD
#define RGBLIGHT_EFFECT_RAINBOW_SWIRL
#define RGBLIGHT_EFFECT_SNAKE
#define RGBLIGHT_EFFECT_KNIGHT
#define RGBLIGHT_EFFECT_CHRISTMAS
#define RGBLIGHT_EFFECT_STATIC_GRADIENT
#define RGBLIGHT_EFFECT_RGB_TEST
#define RGBLIGHT_EFFECT_ALTERNATING
#define RGBLIGHT_EFFECT_TWINKLE
```

**Generation Template**:

```c
/* SPDX-License-Identifier: GPL-2.0-or-later */

#pragma once

#define VIAL_KEYBOARD_UID {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}
#define VIAL_UNLOCK_COMBO_ROWS { 0, 2 }
#define VIAL_UNLOCK_COMBO_COLS { 0, keyboard_width_minus_1 }

/* Add hardware-specific settings here */
```

**Notes**:

- `VIAL_KEYBOARD_UID` can be auto-generated or manually set by user
- Unlock combo is typically `{0, row_of_ESC}, {row_of_MODIFIER, col_of_ENT}`
- Reference the discipline example: ESC at `{0, 0}`, ENT at `{2, 13}`

---

### 3. **rules.mk** - Build Configuration

**Purpose**: Enables VIAL and optional features in the build system.

**Standard Template** (Minimal):

```makefile
VIA_ENABLE = yes
VIAL_ENABLE = yes
```

**Extended Template** (with optimizations and RGB):

```makefile
VIA_ENABLE = yes
VIAL_ENABLE = yes
LTO_ENABLE = yes                    # Smaller firmware size
CAPS_WORD_ENABLE = no               # Disable unless needed
LAYER_LOCK_ENABLE = no              # Enable only if desired
REPEAT_KEY_ENABLE = no              # Enable only if desired

/* Uncomment for RGB underglow support */
# RGBLIGHT_ENABLE = yes             # Requires config.h pin settings
```

**Notes**:

- `VIA_ENABLE` enables legacy VIAL support
- `VIAL_ENABLE` enables new VIAL format
- `LTO_ENABLE` reduces firmware size but increases compile time
- RGB features should match what's in the root-level `rules.mk`

---

### 4. **keymap.c** - Keymap Definition

**Purpose**: Defines the key mappings for the keyboard. Can be identical to the default keymap or customized for VIAL.

**Standard Template** (from default):

```c
/* Copyright 2019 COSEYFANNITUTTI
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#include QMK_KEYBOARD_H

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
  [0] = LAYOUT_XXX(
      /* row 0 keys */
      KC_KEY1, KC_KEY2, ...),

  [1] = LAYOUT_XXX(
      /* layer 1 keys */
      KC_TRNS, KC_TRNS, ...),
};
```

**Notes**:

- For most conversions, the vial/keymap.c can be identical to default/keymap.c
- Customizations are optional and keyboard-specific
- VIAL supports runtime editing through its UI

---

## Optional Files (Keyboard-Specific)

### 5. **README.md** - Documentation File

**Purpose**: User-facing documentation explaining features, controls, and setup.

**Content Sections**:

1. Title and description
2. Features list (VIAL support, RGB, layers, etc.)
3. Layer descriptions
4. Control key mappings (e.g., RGB controls)
5. Hardware setup instructions
6. Build/flash commands
7. Customization guide
8. Vial configuration steps

**Template**: See discipline's README.md for reference.

## Conversion Workflow Summary

### Step 1: Analyze Source Keyboard

- Read `keyboard.json` for layout definition and metadata
- Review root-level `rules.mk` for build options
- Check if hardware-specific config exists (RGB pins, etc.)

### Step 2: Generate vial.json

```bash
python keyboard_to_vial_converter.py <input_path>
# Input can be keyboard.json or existing vial.json
```

### Step 3: Create config.h

Based on reference keyboards and hardware specs:

- Add `VIAL_KEYBOARD_UID` (auto-generated or manual)
- Add unlock combo coordinates
- Add hardware-specific settings (RGB pins, LED count, etc.)

### Step 4: Copy/Adapt keymap.c

- Default: Same as `default/keymap.c`
- Optional: Customize for VIAL features

### Step 5: Create rules.mk

```makefile
VIA_ENABLE = yes
VIAL_ENABLE = yes
LTO_ENABLE = yes

# Uncomment for RGB support if needed
# RGBLIGHT_ENABLE = yes
```

### Step 6: Create README.md (Optional but Recommended)

Document features, controls, and setup instructions.

---

## Reference Keyboard Analysis

### coseyfannitutti/discipline

**Type**: 65% ANSI keyboard with optional RGB underglow

**Root rules.mk**:

```makefile
F_CPU = 16000000
RGBLIGHT_ENABLE = no  # Disabled by default, enable in keymap
```

**VIAL rules.mk**:

```makefile
VIA_ENABLE = yes
VIAL_ENABLE = yes
LTO_ENABLE = yes
CAPS_WORD_ENABLE = no
LAYER_LOCK_ENABLE = no
REPEAT_KEY_ENABLE = no
RGBLIGHT_ENABLE = yes  # Enabled for VIAL build
```

**config.h Features**:

- RGB underglow support (WS2812B LED strip)
- 16 LEDs by default
- Multiple RGB effects enabled
- Unlock combo: ESC(0,0) + ENT(2,13)

---

### jlw/bruce_the_keyboard

**Type**: 40% keyboard with VIAL support

**Root rules.mk**: Not present (uses defaults)

**VIAL rules.mk**:

```makefile
VIA_ENABLE = yes
VIAL_ENABLE = yes
```

**config.h Features**:

- UID-based identification
- Unlock combo: ESC(0,0) + TAB(2,9)
- Custom VIAL settings (entries, layers)

---

## Key Patterns Across All VIAL Keyboards

### File Presence Requirements


| File        | Required For            | Notes                         |
| ----------- | ----------------------- | ----------------------------- |
| `vial.json` | **All**                 | Layout definition - mandatory |
| `config.h`  | **All**                 | Hardware config - mandatory   |
| `rules.mk`  | **VIAL subfolder only** | Build options - mandatory     |
| `keymap.c`  | **All**                 | Key mappings - mandatory      |
| `README.md` | **Recommended**         | Documentation - optional      |

### Root-Level vs VIAL Subfolder Differences


| File            | Root Level            | VIAL Subfolder |
| --------------- | --------------------- | -------------- |
| `keyboard.json` | **Present**           | Not needed     |
| `info.json`     | Optional/legacy       | Not used       |
| `rules.mk`      | Core features (F_CPU) | VIAL/VIA flags |

### Configuration File Naming Conventions

1. Root `rules.mk`: Keyboard-wide settings, hardware config
2. VIAL `rules.mk`: Build flags only (VIA/VIAL enablement)
3. VIAL `config.h`: Only needed for VIAL builds (UID, combo, RGB)

---

## Special Cases and Considerations

### Keyboards Without info.json

Some keyboards (like discipline) don't have an `info.json` file at root level. This is acceptable when:

- The keyboard.json is comprehensive enough
- No legacy QMK metadata is needed
- The VIAL build is the primary target

### RGB Configurations

Two approaches observed:

1. **RGB in Root rules.mk** (disable by default, enable per-keymap):

   ```makefile
   RGBLIGHT_ENABLE = no
   ```
2. **RGB in VIAL rules.mk only**:

   ```makefile
   RGBLIGHT_ENABLE = yes  # Only for VIAL builds
   ```
3. **No RGB support** (simple keyboards):

   - No `RGB_*` settings in config.h
   - `lighting: "none"` in vial.json
   - No RGB pins configured

---

## Checklist for Complete Conversion

### Before Starting

- [ ]  Read existing `keyboard.json` for layout and metadata
- [ ]  Review root-level `rules.mk` (if present)
- [ ]  Determine hardware capabilities (RGB, layers, bootloader, etc.)

### During Conversion

- [ ]  Generate `vial.json` from keyboard.json
- [ ]  Create `config.h` with appropriate settings
- [ ]  Copy/adapt `keymap.c` from default folder
- [ ]  Create `rules.mk` for VIAL subfolder
- [ ]  Write `README.md` (optional but recommended)
- [ ]  Optional: Create `RGB_UNDERGLOW_GUIDE.md` if applicable

### After Conversion

- [ ]  Test build with `make <keyboard>:vial:flash`
- [ ]  Verify VIAL detects keyboard correctly
- [ ]  Confirm layout matches physical keyboard in VIAL UI
- [ ]  Test RGB controls (if applicable)
- [ ]  Validate unlock combo works

---

## Tools Available

### Conversion Scripts


| Script                          | Purpose                        | Input                      | Output      |
| ------------------------------- | ------------------------------ | -------------------------- | ----------- |
| `keyboard_to_vial_converter.py` | Generate vial.json             | keyboard.json or vial.json | vial.json   |
| `find_vial_pairs.py`            | Discover paths from CSV        | -                          | Path list   |
| `compare_vial_conversions.py`   | Compare generated vs reference | -                          | Diff report |

### Reference Files

- `vial_keyboard_pairs.csv`: Known keyboard.json → vial.json mappings
- `keyboard_to_vial_converter.py`: Main conversion tool
- `.clinerules/vial-research.md`: Project-specific rules and guidelines

---

## Related Documentation

- [VIAL Docs](../VIAL Docs/) - Official VIAL documentation
- [QMK Docs](../QMK Docs/) - QMK firmware documentation
- `vial_keyboard_research.md` - Core conversion research
- `convert_keyboard_to_vial.md` - Converter testing guide

---

## Appendix: Sample Files

### Minimal vial.json Template

```json
{
  "name": "<KeyboardName>",
  "vendorId": 0xXXXX,
  "productId": 0xXXXX,
  "lighting": "none",
  "matrix": {"rows": 5, "cols": 15},
  "layouts": {
    "keymap": [...]
  }
}
```

### Minimal config.h Template

```c
#define VIAL_KEYBOARD_UID {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}
#define VIAL_UNLOCK_COMBO_ROWS { 0, 2 }
#define VIAL_UNLOCK_COMBO_COLS { 0, X }
```

### Minimal rules.mk Template

```makefile
VIA_ENABLE = yes
VIAL_ENABLE = yes
LTO_ENABLE = yes
```

---

*Last Updated: July 2026*
*Based on analysis of vial-qmk repository keyboards (discipline, bruce_the_keyboard, and others)*
