# KBIC65 - Bill of Materials

**Note:** This BOM is based on the build log and design files.  
**Source:** https://github.com/b-karl/KBIC65

## Components

### Microcontroller
| Item | Qty | Description |
|------|-----|-------------|
| Controller | 1 | Pro Micro or Nice!nano (for wireless) |

### Diodes
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| D1-D70 | 70 | 1N4148 | Switching diode (DO-35) |

### Keyboard Components
| Item | Qty | Description |
|------|-----|-------------|
| MX Switches | 70 | Cherry MX compatible (PCB mount, 5-pin) |
| Stabilizers | 4-5 | PCB mount stabilizers (2u, 6.25u/7u) |
| Keycaps | 70 | Cherry MX compatible keycaps (65% set) |

### Optional Components
| Item | Qty | Description |
|------|-----|-------------|
| Rotary Encoder | 1 | EC11 rotary encoder (optional) |
| Encoder Knob | 1 | Knob for rotary encoder |
| OLED Screen | 1 | 0.91" OLED display (I2C, optional) |

### PCB and Plates
| Item | Qty | Description |
|------|-----|-------------|
| PCB | 1 | Main PCB |
| Switch Plate | 1 | Switch plate (FR4 or acrylic) |
| Bottom Plate | 1 | Bottom plate with art |
| Acrylic Window | 1 | Acrylic window (optional) |

### Hardware
| Item | Qty | Description |
|------|-----|-------------|
| M2 Screws | varies | For plate mounting |
| M2 Standoffs | varies | For assembly |

## Notes

- This is a 65%/70-key keyboard with spaced arrows
- Uses Pro Micro footprint (Nice!nano for wireless)
- Matrix: 8x9 duplex matrix (17 pins)
- Reduced copper for better Bluetooth signal
- Plate-mounted with screws
- Two alternative bottom designs available
- Includes dithered PCB art

## Firmware Support

- **ZMK:** For wireless builds with Nice!nano
- **QMK:** For wired builds with Pro Micro

## Sourcing

For detailed sourcing information, see the [Component Sourcing Guide](../../docs/component_sourcing_guide.md).

## License

KBIC65 is licensed under MIT
