# Discipline V2 - Bill of Materials

**Note:** This BOM is extracted from the original repository documentation.  
**Source:** https://github.com/coseyfannitutti/discipline

## Components

### Microcontroller
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| U1 | 1 | ATmega32A-PU | Microcontroller (DIP-40) |
| IC Socket | 1 | 40-pin | DIP-40 IC socket (narrow) |

### Diodes
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| D1-D68 | 68 | 1N4148 | Switching diode (DO-35) |
| D69, D70 | 2 | 3.6V | Zener diode (DO-35) |

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
| R5, R6 | 2 | 5.1kΩ | 1/6W resistor (USB-C CC) |

### Other Components
| Ref | Qty | Value | Description |
|-----|-----|-------|-------------|
| F1 | 1 | 100mA | Polyfuse (resettable fuse) |
| Y1 | 1 | 16MHz | Crystal oscillator (HC49) |
| J1 | 1 | USB-C | USB-C connector (through-hole) |
| J2 | 1 | 2x3 | AVR ISP header (optional) |
| SW1, SW2 | 2 | 6x6mm | Tactile switch (Reset/Boot) |
| LED1, LED2 | 2 | 3mm | LED (status indicators) |

### Keyboard Components
| Item | Qty | Description |
|------|-----|-------------|
| MX Switches | 68 | Cherry MX compatible (PCB mount, 5-pin) |
| Stabilizers | 4-6 | PCB mount stabilizers (2u, 6.25u/7u) |
| Keycaps | 68 | Cherry MX compatible keycaps |

### Hardware
| Item | Qty | Description |
|------|-----|-------------|
| M2 Screws | varies | For case assembly |
| M2 Standoffs | varies | For case assembly |

## Notes

- This is a 65% keyboard with 68 keys
- Uses ATmega32A (DIP-40) microcontroller
- Through-hole USB-C connector
- Requires PCB mount (5-pin) switches
- Optional acrylic case available

## Sourcing

For detailed sourcing information, see the [Component Sourcing Guide](../../docs/component_sourcing_guide.md).

## License

Discipline is licensed under CC BY-NC 4.0 (personal use only).  
Kits are sold by CFTKB.com
