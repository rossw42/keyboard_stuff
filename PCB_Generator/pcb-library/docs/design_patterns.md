# Through-Hole Keyboard Design Patterns

## Overview

This document catalogs common design patterns and best practices found across multiple through-hole keyboard projects. These patterns represent proven implementations that can be referenced when creating new designs or understanding existing projects.

**📌 For detailed schematic examples with actual component values, see [SCHEMATIC_PATTERNS.md](SCHEMATIC_PATTERNS.md)**

---

## Matrix Wiring Patterns

### Standard Diode Matrix
**Description:** Row-column matrix with one diode per switch for anti-ghosting

**Common Configurations:**
- **60% keyboards:** 5 rows × 14 columns (Discipline, Tartan)
- **65% keyboards:** 5 rows × 15 columns (Discipline V2)
- **TKL keyboards:** 6 rows × 17 columns (Mysterium)
- **40% keyboards:** 4 rows × 12 columns (Plaid, Rosaline)
- **Macropads:** 4 rows × 4 columns (Plaid-Pad, Dumbpad)

**Component:** 1N4148 diode (DO-35 package) per switch

**Diode Orientation:** Cathode (banded end) typically toward column

**Projects Using:** Discipline, Mysterium, Plaid, Tartan, Lumberjack, Rosaline, Litl, KBIC65, Plaid-Pad, Dumbpad

### Duplex Matrix
**Description:** Reduced pin count by using bidirectional scanning

**Example:** KBIC65 uses 8×9 duplex matrix (17 pins) for 70 keys

**Advantage:** Fewer MCU pins required for larger layouts

**Projects Using:** KBIC65

---

## USB Connector Implementations

### USB-C Through-Hole (12-pin)

**Common Implementation:**
- USB-C connector (12-pin through-hole or SMD)
- 2× 5.1kΩ resistors (CC1/CC2 pull-down for USB 2.0 mode)
- 2× Zener diodes (3.6V for ESD protection on D+/D-)
- 1× 1.5kΩ resistor (D- pull-up for USB 2.0 device identification)
- 1× 75Ω resistor (series termination for signal integrity)
- Decoupling capacitors (0.1µF ceramic)

**Projects Using:** Discipline V2, Mysterium, Lumberjack (Rev 1.8)

**Notes:**
- Through-hole USB-C connectors require larger PCB cutout
- SMD variants provide lower profile but require reflow soldering

### USB Mini/Micro Through-Hole

**Common Implementation:**
- USB Mini-B or Micro-B connector (through-hole)
- Simpler passive component requirements
- ESD protection diodes optional but recommended
- Decoupling capacitors (0.1µF)

**Projects Using:** Rosaline, older keyboard designs

**Notes:**
- Through-hole USB Mini/Micro connectors more readily available
- Larger footprint than USB-C

### VUSB (Software USB)

**Common Implementation:**
- Uses ATmega328P or similar AVR without native USB
- Requires 3.6V zener diodes on D+/D- lines
- Specific resistor values for USB signaling (68Ω, 1.5kΩ)
- 16MHz crystal required for timing

**Projects Using:** Plaid, Plaid-Pad

**Notes:**
- Lower cost (no USB-capable MCU required)
- Requires bootloader flashing via ISP
- Limited to USB 1.1 Low Speed

---

## MCU Integration Patterns

### DIP AVR (ATmega328P)

**Common Implementation:**
- ATmega328P-PU (28-pin DIP package)
- 16MHz crystal with 2× 22pF load capacitors
- 10kΩ pull-up resistor on RESET pin
- 0.1µF decoupling capacitors on VCC/GND pairs
- Optional IC socket for easy replacement

**Pin Usage:**
- Rows: Typically PB0-PB5, PD0-PD7
- Columns: Typically PC0-PC5, PD0-PD7
- USB D+/D-: PD2/PD3 (for VUSB) or hardware USB pins

**Projects Using:** Lumberjack, Rosaline, Plaid-Pad

**Advantages:**
- Easy to solder (through-hole)
- Replaceable if damaged
- Lower cost than USB-capable MCUs

### DIP AVR (ATmega32A)

**Common Implementation:**
- ATmega32A-PU (40-pin DIP package)
- Native USB support (no VUSB required)
- 16MHz crystal with 2× 22pF load capacitors
- 10kΩ pull-up resistor on RESET pin
- 0.1µF decoupling capacitors

**Projects Using:** Discipline, Mysterium

**Advantages:**
- More GPIO pins for larger matrices
- Native USB support
- Through-hole for easy assembly

### Pro Micro Footprint

**Common Implementation:**
- 24-pin header footprint (2× 12-pin rows)
- Compatible with Pro Micro, Elite-C, nice!nano
- No external crystal required (on module)
- USB connector on module

**Pin Mapping:**
- Varies by controller module
- Typically uses RAW, GND, VCC, and GPIO pins

**Projects Using:** Litl, KBIC65, Dumbpad

**Advantages:**
- Modular - easy to swap controllers
- Supports wireless (nice!nano with ZMK)
- Compact footprint
- USB-C available on some modules (Elite-C)

**Considerations:**
- More expensive than bare MCU
- Limited to module's available pins
- Module must be purchased separately

---

## Reset and Programming Circuits

### Standard Reset Circuit

**Components:**
- Tactile pushbutton (6mm × 6mm through-hole)
- 10kΩ pull-up resistor on RESET line
- Optional 0.1µF capacitor for debouncing

**Function:** Resets MCU to restart firmware or enter bootloader

**Projects Using:** All projects with AVR MCUs

### ISP Programming Header

**Common Implementation:**
- 2×3 pin header (0.1" pitch)
- Standard AVR ISP pinout:
  - Pin 1: MISO
  - Pin 2: VCC
  - Pin 3: SCK
  - Pin 4: MOSI
  - Pin 5: RESET
  - Pin 6: GND

**Purpose:** Initial bootloader flashing or firmware updates

**Projects Using:** Discipline, Mysterium, Plaid, Plaid-Pad, Lumberjack

**Notes:**
- Required for VUSB-based designs (no USB bootloader)
- Optional for USB-capable MCUs (can use USB bootloader)

---

## Optional Feature Implementations

### Rotary Encoders

**Common Implementation:**
- EC11 rotary encoder (through-hole)
- 2 pins for quadrature encoding (A/B phases)
- 1 pin for pushbutton switch
- Optional pull-up resistors (10kΩ) if not using internal pull-ups
- Diode on switch pin if integrated into matrix

**Mounting:**
- Can replace switch positions in matrix
- Dedicated pins outside matrix
- Multiple encoders supported

**Projects Using:** Plaid-Pad (up to 4), Litl (1-2), Dumbpad (1-2), Neopad (2)

**Firmware Support:**
- QMK: Full support with encoder map
- VIA: Limited support (no encoder configuration)
- VIAL: Full support with encoder configuration

### OLED Displays

**Common Implementation:**
- 0.91"-0.96" OLED display (128×32 or 128×64)
- I2C interface (SDA, SCL, VCC, GND)
- 4-pin header connection
- Pull-up resistors on I2C lines (typically 4.7kΩ)

**Projects Using:** Litl, Plaid-Pad (Rev3), Dumbpad (combo_oled variant)

**Display Content:**
- Layer indicators
- WPM counter
- Custom graphics/logos
- Caps Lock status

### Status LEDs

**Common Implementation:**
- 3mm or 5mm through-hole LEDs
- Current-limiting resistors (typically 220Ω-1kΩ)
- Connected to GPIO pins or directly to status signals

**Common Uses:**
- Caps Lock indicator
- Num Lock indicator
- Layer indicators
- Power indicator

**Projects Using:** Discipline, Mysterium, Lumberjack, Dumbpad

### Per-Key RGB (Advanced)

**Implementation:**
- WS2812B or SK6812 addressable LEDs
- Typically SMD, not through-hole
- Single data line daisy-chained
- Requires 5V power and level shifting for 3.3V MCUs

**Projects Using:** Dumbpad (hotswap_rgb variant)

**Notes:**
- Not common in pure through-hole designs
- Requires SMD soldering skills
- Higher power consumption

---

## Split Keyboard Patterns

### TRRS Connection

**Common Implementation:**
- TRRS jack (3.5mm audio jack, 4-conductor)
- Connects VCC, GND, and 2 data lines between halves
- Pull-up resistors on data lines
- ESD protection recommended

**Communication Protocols:**
- Serial (single wire + ground)
- I2C (SDA + SCL + ground)

**Projects Using:** Lumberjack (split ortholinear)

### Universal Daughterboard

**Common Implementation:**
- Molex Pico-EZmate connector (4-pin)
- Standardized pinout for USB daughterboards
- Allows swapping USB connectors without PCB redesign

**Projects Using:** Lumberjack (Rev 1.8)

**Advantages:**
- Modular USB connection
- Easy to replace if damaged
- Supports different USB types

---

## Power and Decoupling

### Standard Decoupling

**Common Implementation:**
- 0.1µF ceramic capacitor on each VCC/GND pair
- Placed as close to MCU pins as possible
- Additional 4.7µF-10µF bulk capacitor near power input

**Purpose:**
- Filter high-frequency noise
- Provide local charge reservoir
- Stabilize power supply

**Projects Using:** All projects

### Crystal Oscillator Circuit

**Common Implementation:**
- 16MHz crystal (HC-49/US package)
- 2× 22pF ceramic capacitors (load capacitors)
- Connected to XTAL1/XTAL2 pins on MCU

**Purpose:** Provides accurate timing for USB communication and MCU operation

**Projects Using:** All AVR-based projects (not needed for Pro Micro footprint)

---

## PCB Layout Considerations

### Component Clearances

**Through-Hole Component Heights:**
- Diodes (DO-35): ~3mm above PCB
- Resistors (axial): ~3-5mm above PCB
- DIP ICs: ~5-8mm above PCB (with socket)
- Electrolytic capacitors: ~5-13mm above PCB
- Tactile switches: ~5mm above PCB

**Recommended Clearance Below PCB:** 5.4mm minimum (accommodates solder joints)

**Recommended Clearance Above PCB:** 12mm minimum (accommodates switches and keycaps)

### Switch Spacing

**Standard MX Spacing:**
- 19.05mm (0.75") center-to-center
- 14mm × 14mm switch cutout in plate
- 5mm pin spacing on PCB

**Stabilizer Positions:**
- 2U: 11.95mm from center
- 6.25U: 50mm from center
- 7U: 57.15mm from center

### Mounting Holes

**Common Patterns:**
- 60% keyboards: 6 mounting holes (GH60 standard)
- Custom layouts: 4-6 holes depending on size
- Hole diameter: 2.0-2.2mm (for M2 screws)
- Clearance zone: 5mm radius around each hole

---

## Firmware Considerations

### QMK Firmware

**Common Features:**
- Matrix scanning
- Layer support
- Tap/hold keys
- Macros
- RGB lighting control
- Rotary encoder support

**Configuration Files:**
- `config.h`: Hardware configuration (matrix pins, features)
- `rules.mk`: Feature enables/disables
- `keymap.c`: Key layout definitions

**Projects Using:** All projects have QMK support

### VIA Support

**Requirements:**
- QMK firmware with VIA enabled
- JSON layout definition
- Unique vendor/product ID

**Limitations:**
- No rotary encoder configuration
- Limited macro support compared to VIAL

**Projects Using:** Lumberjack, Plaid-Pad, Litl

### VIAL Support

**Advantages over VIA:**
- Rotary encoder configuration
- More macro slots
- Tap dance configuration
- Combo configuration

**Projects Using:** Plaid-Pad, some community forks

### ZMK Firmware (Wireless)

**Requirements:**
- Bluetooth-capable MCU (nice!nano)
- Battery management circuit
- Lower power consumption design

**Projects Using:** KBIC65 (with nice!nano)

---

## Design Pattern Summary Table

| Pattern | Complexity | Cost Impact | Projects Using | Notes |
|---------|-----------|-------------|----------------|-------|
| Standard diode matrix | Low | Low | All | Universal anti-ghosting |
| USB-C through-hole | Medium | Medium | Discipline, Mysterium, Lumberjack | Modern connector |
| VUSB software USB | Medium | Low | Plaid, Plaid-Pad | Requires ISP programming |
| DIP AVR (328P) | Low | Low | Lumberjack, Rosaline | Easy to solder |
| DIP AVR (32A) | Low | Medium | Discipline, Mysterium | Native USB |
| Pro Micro footprint | Low | Medium-High | Litl, KBIC65, Dumbpad | Modular, supports wireless |
| Rotary encoders | Medium | Low-Medium | Plaid-Pad, Litl, Dumbpad | Adds functionality |
| OLED display | Medium | Low | Litl, Plaid-Pad, Dumbpad | Visual feedback |
| Split keyboard | High | Medium | Lumberjack | Requires TRRS/cable |

---

## References

### Project Repositories
- Discipline: https://github.com/coseyfannitutti/discipline
- Mysterium: https://github.com/coseyfannitutti/mysterium
- Lumberjack: https://github.com/peej/lumberjack-keyboard
- Plaid: https://github.com/hsgw/plaid
- Plaid-Pad: https://github.com/Keycapsss/Plaid-Pad
- Rosaline: https://github.com/peej/rosaline-keyboard
- Litl: https://github.com/mohoyt/litl
- KBIC65: https://github.com/b-karl/KBIC65
- Dumbpad: https://github.com/imchipwood/dumbpad

### Additional Resources
- QMK Firmware: https://qmk.fm/
- VIA Configurator: https://www.caniusevia.com/
- VIAL: https://get.vial.today/
- AVR Datasheets: https://www.microchip.com/

---

## Contributing

This document is a living reference. As new through-hole keyboard projects are analyzed, additional patterns and best practices should be documented here.

### Pattern Documentation Template

When documenting a new pattern, include:
1. **Pattern Name:** Clear, descriptive name
2. **Description:** What the pattern does
3. **Common Implementation:** Specific components and values
4. **Schematic/Diagram:** Visual reference (if available)
5. **Projects Using:** List of projects implementing this pattern
6. **Advantages/Disadvantages:** Trade-offs to consider
7. **Notes:** Special considerations or variations

---

*Last Updated: 2025-10-16*
