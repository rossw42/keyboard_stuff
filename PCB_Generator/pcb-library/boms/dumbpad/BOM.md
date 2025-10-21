# Dumbpad - Bill of Materials

**Note:** This BOM is based on the repository documentation.  
**Source:** https://github.com/imchipwood/dumbpad

## Components

### Microcontroller
| Item | Qty | Description |
|------|-----|-------------|
| Controller | 1 | Pro Micro or Teensy2.0 |

### Diodes
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| D1-D17 | 17 | 1N4148 | Switching diode (DO-35) |

### Keyboard Components
| Item | Qty | Description |
|------|-----|-------------|
| MX Switches | 16 | Cherry MX compatible (PCB mount, 5-pin) |
| Keycaps | 16 | Cherry MX compatible keycaps |

### Optional Components
| Item | Qty | Description |
|------|-----|-------------|
| Rotary Encoder | up to 2 | EC11 rotary encoder |
| Encoder Knobs | up to 2 | Knobs for rotary encoders |
| OLED Screen | 1 | 0.91" OLED display (combo_oled variant) |
| Status LEDs | 3 | LEDs for status (combo variant) |
| RGB LEDs | 16 | Per-key RGB (hotswap_rgb variant) |

### Hardware
| Item | Qty | Description |
|------|-----|-------------|
| M2 Screws | 8 | For case mounting (2mm holes) |

## Variants

### combo
- Up to 2 rotary encoders
- 3 status LEDs
- Standard switches

### combo_oled
- OLED display instead of LEDs
- Up to 2 rotary encoders

### combo_teensy
- Teensy2.0 version
- Up to 2 rotary encoders

### reversible
- Single encoder
- Reversible sockets

### hotswap_rgb
- Per-key RGB LEDs
- Hotswap sockets
- No encoders

## PCB Specifications

- **Dimensions:** 97mm × 78.5mm
- **Mounting:** Four 2mm holes in 40mm square pattern
- **Corners:** Chamfered

## Notes

- This is a 4x4 macropad
- Uses Pro Micro or Teensy2.0
- Multiple variants available
- 3D printable cases available
- Supports rotary encoders and OLED

## Firmware Support

- **QMK:** Yes

## Sourcing

For detailed sourcing information, see the [Component Sourcing Guide](../../docs/component_sourcing_guide.md).

## License

Dumbpad is licensed under GPL-2.0
