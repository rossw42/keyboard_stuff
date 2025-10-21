# Plaid-Pad - Bill of Materials

**Note:** This BOM is extracted from the build guide.  
**Source:** https://github.com/Keycapsss/Plaid-Pad

## Components

### Microcontroller
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| U1 | 1 | ATmega328P-PU | Microcontroller (DIP-28) |
| IC Socket | 1 | 28-pin | DIP-28 IC socket (narrow) |

### Diodes
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| D1-D16 | 16 | 1N4148 | Switching diode (DO-35) |
| D49, D50 | 2 | 3.6V | Zener diode (DO-35) |

### Capacitors
| Ref | Qty | Value | Pitch | Description |
|-----|-----|-------|-------|-------------|
| C1, C2 | 2 | 22pF | 2.5mm | Ceramic capacitor |
| C3 | 1 | 4.7µF | 1.5mm | Electrolytic capacitor |
| C4, C5 | 2 | 0.1µF (100nF) | 5.0mm | Ceramic capacitor |

### Resistors
| Ref | Qty | Value | Color Code | Description |
|-----|-----|-------|------------|-------------|
| R1, R7 | 2 | 1.5kΩ | Brown-Green-Black-Brown-Brown | 1/6W resistor |
| R2, R3 | 2 | 75Ω | Brown-Gold-Black-Green-Purple | 1/6W resistor |
| R4 | 1 | 10kΩ | Brown-Black-Black-Red-Brown | 1/6W resistor |
| R8, R9 | 2 | 5.1kΩ | Green-Brown-Black-Brown-Brown | 1/6W resistor (USB-C CC) |

### Other Components
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| F1 | 1 | 100mA | Polyfuse (resettable fuse) |
| Y1 | 1 | 16MHz | Crystal oscillator (HC49) |
| J1 | 1 | USB-C | USB-C connector (through-hole) |
| SW1, SW2 | 2 | 6x6mm | Tactile switch (Reset/Boot) |
| LED1 | 1 | 3mm | LED (power indicator, optional) |

### Keyboard Components
| Item | Qty | Description |
|------|-----|-------------|
| MX Switches | up to 16 | Cherry MX compatible (PCB mount, 5-pin) |
| Keycaps | up to 16 | Cherry MX compatible keycaps |

### Optional Components
| Item | Qty | Description |
|------|-----|-------------|
| Rotary Encoder | up to 4 | EC11 rotary encoder (Rev2+) |
| Encoder Knobs | up to 4 | Knobs for rotary encoders |
| OLED Screen | 1 | 0.91" OLED display (Rev3+) |

## Revision Notes

### Rev3 (Latest)
- OLED display support
- Up to 4 rotary encoders
- Encoder positions interchangeable with switches

### Rev2.1
- Choc V2 switch support
- Up to 4 rotary encoders

### Rev2
- Up to 4 rotary encoders
- Encoder positions interchangeable with switches

## Notes

- This is a 4x4 numpad/macropad
- Uses ATmega328P with VUSB
- Bootloader: USBaspLoader (same as Plaid)
- Supports up to 4 rotary encoders (Rev2+)
- Optional OLED display (Rev3)

## Firmware Support

- **QMK:** Yes (`keycapsss/plaid_pad`)
- **VIA:** Yes (no encoder support)
- **VIAL:** Yes (with encoder support)

## Sourcing

For detailed sourcing information, see the [Component Sourcing Guide](../../docs/component_sourcing_guide.md).

## License

Plaid-Pad is licensed under MIT
