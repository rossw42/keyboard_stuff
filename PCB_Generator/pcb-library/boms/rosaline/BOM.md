# Rosaline - Bill of Materials

**Note:** This BOM is based on the Lumberjack design (same designer, similar architecture).  
**Source:** https://github.com/peej/rosaline-keyboard

## Components

### Microcontroller
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| U1 | 1 | ATmega328P-PU | Microcontroller (DIP-28) |
| IC Socket | 1 | 28-pin | DIP-28 IC socket (narrow) |

### Diodes
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| D1-D48 | 48 | 1N4148 | Switching diode (DO-35) |
| D49, D50 | 2 | 3.6V | Zener diode (DO-35) |

### Capacitors
| Ref | Qty | Value | Pitch | Description |
|-----|-----|-------|-------|-------------|
| C1, C2 | 2 | 22pF | 2.5mm | Ceramic capacitor |
| C3 | 1 | 4.7µF | 1.5mm | Electrolytic capacitor |
| C4, C5 | 2 | 0.1µF (100nF) | 5.0mm | Ceramic capacitor |

### Resistors
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| R1, R7, R8 | 3 | 1.5kΩ | 1/6W resistor |
| R2, R3 | 2 | 75Ω | 1/6W resistor |
| R4 | 1 | 10kΩ | 1/6W resistor |
| R5, R6 | 2 | 5.1kΩ | 1/6W resistor (USB-C only) |

### Other Components
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| F1 | 1 | 100mA | Polyfuse (resettable fuse) |
| Y1 | 1 | 16MHz | Crystal oscillator (HC49) |
| J1 | 1 | USB-C or Mini | USB connector |
| J2 | 1 | 2x3 | AVR ISP header (optional) |
| SW1, SW2 | 2 | 6x6mm | Tactile switch (Reset/Boot) |
| LED1, LED2 | 2 | 3mm | LED (status indicators) |

### Keyboard Components
| Item | Qty | Description |
|------|-----|-------------|
| MX Switches | 45-48 | Cherry MX compatible (PCB mount, 5-pin) |
| Stabilizers | 2-4 | PCB mount stabilizers (2u, 6.25u/7u) |
| Keycaps | 45-48 | Cherry MX compatible keycaps (40% set) |

## Notes

- This is a 40% keyboard that fits in 60% cases
- Uses ATmega328P (DIP-28) microcontroller
- Matrix: 7 rows × 8 columns
- Supports split spacebar and split right shift
- Fits standard 60% tray mount cases

## Sourcing

For detailed sourcing information, see the [Component Sourcing Guide](../../docs/component_sourcing_guide.md).

## License

Rosaline is licensed under MIT
