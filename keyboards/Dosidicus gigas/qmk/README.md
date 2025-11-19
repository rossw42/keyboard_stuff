# Dosidicus Gigas QMK Firmware

A 32-key split ergonomic keyboard with columnar stagger and Choc switches.

## Specifications

- **Layout:** 5×3 + 1 thumb per half (32 keys total)
- **Switches:** Kailh Choc low-profile
- **Controller:** Pro Micro (ATmega32U4)
- **Connection:** TRRS cable for split communication
- **Diode Direction:** COL2ROW

## Pin Configuration

### Matrix Pins
- **Columns:** F4, F5, F6, F7, B1, B3, B2, B6
- **Rows:** D4, C6, D7, E6
- **Serial (TRRS):** D2
- **Handedness:** B5 (or EEPROM)

See `PIN_MATRIX.md` for detailed pin mapping.

## Building

### Default Keymap
```bash
qmk compile -kb dosidicus_gigas -km default
```

### Vial Keymap
```bash
qmk compile -kb dosidicus_gigas -km vial
```

## Flashing

1. Put the keyboard into bootloader mode (double-tap reset or use QK_BOOT key)
2. Flash the firmware:
```bash
qmk flash -kb dosidicus_gigas -km vial
```

## Vial Configuration

The Vial keymap includes:
- 4 layers
- Dynamic keymap support
- Unlock combo: Top-left two keys (Q + W)
- UID: `{0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0}`

Load `keymaps/vial/vial.json` into Vial configurator for GUI editing.

## Default Layers

- **Layer 0:** Base QWERTY
- **Layer 1:** Numbers and symbols
- **Layer 2:** Navigation and function keys
- **Layer 3:** System controls (includes QK_BOOT for bootloader)

## Notes

- Each half needs to be flashed separately
- Set handedness via EEPROM or hardware pin (B5)
- TRRS cable must be connected before powering on
- Never hot-plug TRRS while powered
