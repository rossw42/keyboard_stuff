# Through-Hole Keyboard Schematic Patterns

**Version:** 1.0  
**Last Updated:** 2025-10-20

## Overview

This document provides detailed schematic patterns extracted from actual through-hole keyboard projects in this library. Each pattern includes real component values, connection diagrams, and notes on variations across different projects.

**Purpose:** Reference these patterns when designing new keyboards or understanding existing designs.

---

## Table of Contents

1. [USB-C Through-Hole Implementation](#usb-c-through-hole-implementation)
2. [VUSB Software USB Implementation](#vusb-software-usb-implementation)
3. [ATmega328P Supporting Circuit](#atmega328p-supporting-circuit)
4. [ATmega32A Supporting Circuit](#atmega32a-supporting-circuit)
5. [Crystal Oscillator Circuit](#crystal-oscillator-circuit)
6. [Reset Circuit](#reset-circuit)
7. [ISP Programming Header](#isp-programming-header)
8. [Switch Matrix with Diodes](#switch-matrix-with-diodes)
9. [Rotary Encoder Circuit](#rotary-encoder-circuit)
10. [OLED Display Connection](#oled-display-connection)
11. [LED Indicators](#led-indicators)
12. [Power Decoupling](#power-decoupling)

---

## USB-C Through-Hole Implementation

### Pattern: USB-C with ESD Protection (Lumberjack Rev 1.8)

**Description:** USB-C connector with proper CC resistors, ESD protection, and polyfuse.

**Schematic:**
```
USB-C Connector (TYPE-C-31-M-12)
│
├─ VBUS ──[F1: 100mA Polyfuse]── +5V
│
├─ D+ ───[D61: 3.6V Zener]─── GND
│         │
│         └─[R2: 75Ω]─── MCU D+ (PD2)
│
├─ D- ───[D62: 3.6V Zener]─── GND
│         │
│         └─[R3: 75Ω]─── MCU D- (PD3)
│
├─ CC1 ──[R5: 5.1kΩ]─── GND
│
├─ CC2 ──[R6: 5.1kΩ]─── GND
│
└─ GND ─────────────── GND
```

**Component Values:**
- **F1:** 100mA Polyfuse (resettable fuse)
- **D61, D62:** 3.6V Zener diodes (DO-35 package)
- **R2, R3:** 75Ω resistors (1/6W, series termination)
- **R5, R6:** 5.1kΩ resistors (1/6W, CC pull-down for USB 2.0 mode)
- **J1:** TYPE-C-31-M-12 USB-C connector (12-pin through-hole)


**Function:**
- **Polyfuse (F1):** Protects against overcurrent (100mA limit)
- **Zener Diodes (D61, D62):** ESD protection on data lines (clamp to 3.6V)
- **Series Resistors (R2, R3):** Signal integrity and current limiting (75Ω)
- **CC Resistors (R5, R6):** Configure USB-C for USB 2.0 device mode (5.1kΩ pull-down)

**Projects Using:** Lumberjack Rev 1.8

**Notes:**
- USB-C connector must be 12-pin through-hole type
- CC resistors (5.1kΩ) tell USB-C host this is a USB 2.0 device
- Zener diodes protect MCU from ESD events
- 75Ω series resistors improve signal integrity

---

## VUSB Software USB Implementation

### Pattern: VUSB with ATmega328P (Plaid)

**Description:** Software USB implementation using V-USB library with ATmega328P.

**Schematic:**
```
USB Mini-B Connector
│
├─ VBUS ──[F1: 100mA Polyfuse]── +5V
│
├─ D+ ───[D49: 3.6V Zener]─── GND
│         │
│         └─[R1: 1.5kΩ]─── +5V (pull-up for device ID)
│         │
│         └─── MCU D+ (PD2/INT0)
│
├─ D- ───[D50: 3.6V Zener]─── GND
│         │
│         └─[R2: 75Ω]─── MCU D- (PD3)
│         │
│         └─[R3: 75Ω]─── MCU D- (PD3)
│
└─ GND ─────────────── GND
```

**Component Values:**
- **F1:** 100mA Polyfuse
- **D49, D50:** 3.6V Zener diodes (DO-35)
- **R1:** 1.5kΩ resistor (D+ pull-up for USB 2.0 device identification)
- **R2, R3:** 75Ω resistors (series termination)
- **J1:** USB Mini-B connector (through-hole)

**Function:**
- **1.5kΩ Pull-up (R1):** Identifies device as USB 1.1 Low Speed (1.5Mbps)
- **Zener Diodes:** Clamp voltage to 3.6V (USB spec requires 3.3V ±10%)
- **75Ω Resistors:** Impedance matching for USB data lines
- **Polyfuse:** Overcurrent protection

**Projects Using:** Plaid, Plaid-Pad

**Notes:**
- Requires V-USB library in firmware
- MCU must run at 16MHz for USB timing
- D+ must be on INT0 (PD2) for V-USB
- Limited to USB 1.1 Low Speed (1.5Mbps)
- Requires ISP programming (no USB bootloader)

---

## ATmega328P Supporting Circuit

### Pattern: ATmega328P-PU with Crystal (Lumberjack, Plaid)

**Description:** Complete supporting circuit for ATmega328P-PU (28-pin DIP).

**Schematic:**
```
ATmega328P-PU (28-pin DIP)
│
├─ VCC (Pin 7) ──[C4: 100nF]── GND
│
├─ AVCC (Pin 20) ──[C5: 100nF]── GND
│
├─ AREF (Pin 21) ──[C3: 4.7µF]── GND (optional)
│
├─ RESET (Pin 1) ──[R4: 10kΩ]── +5V
│                   │
│                   └─[SW1: Reset Button]── GND
│
├─ XTAL1 (Pin 9) ──[Y1: 16MHz Crystal]── XTAL2 (Pin 10)
│                   │                     │
│                   [C1: 22pF]           [C2: 22pF]
│                   │                     │
│                   GND                   GND
│
└─ GND (Pins 8, 22) ─────────────── GND
```

**Component Values:**
- **U1:** ATmega328P-PU (28-pin DIP package)
- **Y1:** 16MHz crystal (HC-49/US package)
- **C1, C2:** 22pF ceramic capacitors (2.5mm pitch, crystal load caps)
- **C3:** 4.7µF electrolytic capacitor (1.5mm pitch, AREF decoupling)
- **C4, C5:** 100nF ceramic capacitors (5mm pitch, power decoupling)
- **R4:** 10kΩ resistor (1/6W, RESET pull-up)
- **SW1:** 6×6mm tactile switch (reset button)
- **IC Socket:** 28-pin narrow DIP socket (optional but recommended)


**Function:**
- **Crystal (Y1):** Provides 16MHz clock for MCU operation and USB timing
- **Load Capacitors (C1, C2):** Required for crystal oscillation (22pF typical)
- **Decoupling Caps (C4, C5):** Filter high-frequency noise on power pins
- **AREF Cap (C3):** Stabilizes analog reference voltage (optional)
- **RESET Pull-up (R4):** Keeps MCU running (active-low reset)
- **Reset Button (SW1):** Manual reset for bootloader entry or restart

**Pin Usage (Typical):**
- **PB0-PB5:** Columns or rows (6 pins)
- **PC0-PC5:** Columns or rows (6 pins)
- **PD0-PD7:** Columns, rows, or special functions (8 pins)
- **PD2 (INT0):** USB D+ (for V-USB)
- **PD3:** USB D- (for V-USB)

**Projects Using:** Lumberjack, Rosaline, Plaid, Tartan, Plaid-Pad

**Notes:**
- IC socket recommended for easy replacement
- Crystal must be within 10mm of MCU for stable oscillation
- Decoupling caps should be placed as close to VCC pins as possible
- 22pF load caps are standard for most 16MHz crystals
- AREF capacitor optional unless using ADC

---

## ATmega32A Supporting Circuit

### Pattern: ATmega32A-PU with Native USB (Discipline, Mysterium)

**Description:** ATmega32A-PU (40-pin DIP) with native USB support.

**Schematic:**
```
ATmega32A-PU (40-pin DIP)
│
├─ VCC (Pins 10, 30) ──[C: 100nF each]── GND
│
├─ AVCC (Pin 32) ──[C: 100nF]── GND
│
├─ RESET (Pin 9) ──[R: 10kΩ]── +5V
│                  │
│                  └─[SW: Reset Button]── GND
│
├─ XTAL1 (Pin 13) ──[Y: 16MHz Crystal]── XTAL2 (Pin 12)
│                    │                    │
│                    [C: 22pF]           [C: 22pF]
│                    │                    │
│                    GND                  GND
│
├─ D+ (Pin 2) ──── USB D+
│
├─ D- (Pin 3) ──── USB D-
│
└─ GND (Pins 11, 31) ─────────────── GND
```

**Component Values:**
- **U1:** ATmega32A-PU (40-pin DIP package)
- **Y1:** 16MHz crystal (HC-49/US package)
- **C (crystal):** 2× 22pF ceramic capacitors
- **C (power):** 3× 100nF ceramic capacitors (VCC, AVCC decoupling)
- **R:** 10kΩ resistor (RESET pull-up)
- **SW:** 6×6mm tactile switch (reset button)
- **IC Socket:** 40-pin narrow DIP socket (optional)

**Function:**
- **Native USB:** ATmega32A has built-in USB controller (no V-USB needed)
- **More GPIO:** 40 pins provide more I/O for larger matrices
- **Crystal:** Required for USB timing (16MHz)
- **Decoupling:** Multiple VCC pins require multiple decoupling caps

**Pin Usage (Typical):**
- **PA0-PA7:** Columns or rows (8 pins)
- **PB0-PB7:** Columns or rows (8 pins)
- **PC0-PC7:** Columns or rows (8 pins)
- **PD0-PD7:** Columns, rows, or special functions (8 pins)
- **D+, D-:** USB data lines (hardware USB)

**Projects Using:** Discipline, Mysterium

**Notes:**
- More expensive than ATmega328P but has native USB
- Larger footprint (40-pin vs 28-pin)
- Can support larger matrices (more GPIO pins)
- No need for V-USB library (hardware USB controller)

---

## Crystal Oscillator Circuit

### Pattern: 16MHz Crystal with Load Capacitors

**Description:** Standard crystal oscillator circuit for AVR microcontrollers.

**Schematic:**
```
        XTAL1                    XTAL2
MCU ────┬──────[Y1: 16MHz]──────┬──── MCU
        │                        │
        │                        │
     [C1: 22pF]              [C2: 22pF]
        │                        │
        └────────[GND]───────────┘
```

**Component Values:**
- **Y1:** 16MHz crystal, HC-49/US package (through-hole)
- **C1, C2:** 22pF ceramic capacitors (2.5mm pitch)

**Function:**
- **Crystal:** Provides stable 16MHz clock signal
- **Load Capacitors:** Required for crystal to oscillate at correct frequency
- **Frequency:** 16MHz is standard for USB timing (12MHz × 1.333 = 16MHz)

**Load Capacitor Calculation:**
```
CL = (C1 × C2) / (C1 + C2) + Cstray

For 16MHz crystal with CL = 18pF:
C1 = C2 = 22pF (accounts for ~5pF stray capacitance)
```

**Projects Using:** All AVR-based projects (Lumberjack, Plaid, Discipline, Mysterium, etc.)

**Notes:**
- Crystal must be within 10mm of MCU XTAL pins
- Keep traces short and direct
- 22pF is standard for most 16MHz crystals (check datasheet)
- Some crystals specify 18pF or 20pF load capacitance
- Stray capacitance from PCB traces typically 3-5pF

---

## Reset Circuit

### Pattern: Active-Low Reset with Pull-up

**Description:** Standard reset circuit for AVR microcontrollers.

**Schematic:**
```
        +5V
         │
         │
      [R: 10kΩ]
         │
         ├──── MCU RESET (active-low)
         │
      [SW: Tactile]
         │
        GND
```

**Component Values:**
- **R:** 10kΩ resistor (1/6W, pull-up)
- **SW:** 6×6mm tactile switch (momentary, normally open)

**Function:**
- **Pull-up Resistor:** Keeps RESET pin HIGH (inactive) during normal operation
- **Reset Button:** Pressing button pulls RESET LOW, resetting MCU
- **Bootloader Entry:** Some bootloaders enter programming mode on reset

**Optional Debouncing:**
```
        +5V
         │
      [R: 10kΩ]
         │
         ├──[C: 100nF]── GND (optional debounce cap)
         │
         ├──── MCU RESET
         │
      [SW: Tactile]
         │
        GND
```

**Projects Using:** All projects with AVR MCUs

**Notes:**
- 10kΩ is standard value (4.7kΩ to 47kΩ acceptable)
- Debounce capacitor optional (most MCUs have internal debouncing)
- Reset button typically labeled "RESET" or "RST"
- Some designs use 2 buttons: RESET and BOOT (for bootloader entry)


---

## ISP Programming Header

### Pattern: Standard AVR ISP 6-Pin Header

**Description:** In-System Programming header for flashing bootloader or firmware.

**Schematic:**
```
2×3 Pin Header (0.1" pitch)
┌─────┬─────┬─────┐
│  1  │  2  │     │  1: MISO ──── MCU MISO (PB4)
├─────┼─────┤     │  2: VCC  ──── +5V
│  3  │  4  │     │  3: SCK  ──── MCU SCK (PB5)
├─────┼─────┤     │  4: MOSI ──── MCU MOSI (PB3)
│  5  │  6  │     │  5: RESET ─── MCU RESET
└─────┴─────┘     │  6: GND  ──── GND
```

**Component:**
- **J2:** 2×3 pin header (2.54mm pitch, through-hole)

**Pin Connections (ATmega328P):**
- **Pin 1 (MISO):** PB4 (Pin 18)
- **Pin 2 (VCC):** +5V power
- **Pin 3 (SCK):** PB5 (Pin 19)
- **Pin 4 (MOSI):** PB3 (Pin 17)
- **Pin 5 (RESET):** RESET (Pin 1)
- **Pin 6 (GND):** Ground

**Function:**
- **Initial Programming:** Flash bootloader to new MCU
- **Firmware Updates:** Update firmware without USB bootloader
- **Fuse Bits:** Configure MCU fuse settings
- **Required for V-USB:** V-USB designs need ISP for initial programming

**Programmers:**
- **USBasp:** Low-cost USB ISP programmer (~$5)
- **Arduino as ISP:** Use Arduino board as programmer
- **Atmel-ICE:** Official Atmel programmer (expensive)

**Projects Using:** Lumberjack, Plaid, Plaid-Pad, Discipline, Mysterium

**Notes:**
- Header can be omitted after initial programming (save cost)
- Some designs use pogo pins instead of soldered header
- Required for V-USB designs (no USB bootloader)
- Optional for native USB designs (can use USB bootloader)

---

## Switch Matrix with Diodes

### Pattern: COL2ROW Matrix (Plaid 4×12)

**Description:** Standard keyboard matrix with one diode per switch.

**Schematic (Single Switch):**
```
Column (MCU GPIO)
    │
    │
    ├──[SW: Cherry MX]──┬──[D: 1N4148]──┐
    │                   │               │
    │                   │ (Cathode)     │
    │                   │               │
    │                   └───────────────┴── Row (MCU GPIO)
```

**Schematic (4×12 Matrix Example):**
```
    COL0   COL1   COL2   COL3  ...  COL11
     │      │      │      │           │
     │      │      │      │           │
ROW0─┼──SW──┼──SW──┼──SW──┼───────────┼──SW──
     │  │   │  │   │  │   │           │  │
     │  D   │  D   │  D   │           │  D
     │  │   │  │   │  │   │           │  │
ROW1─┼──SW──┼──SW──┼──SW──┼───────────┼──SW──
     │  │   │  │   │  │   │           │  │
     │  D   │  D   │  D   │           │  D
     │  │   │  │   │  │   │           │  │
ROW2─┼──SW──┼──SW──┼──SW──┼───────────┼──SW──
     │  │   │  │   │  │   │           │  │
     │  D   │  D   │  D   │           │  D
     │  │   │  │   │  │   │           │  │
ROW3─┼──SW──┼──SW──┼──SW──┼───────────┼──SW──
     │  │   │  │   │  │   │           │  │
     │  D   │  D   │  D   │           │  D
     │      │      │      │           │
```

**Component Values:**
- **SW:** Cherry MX compatible switch (or Alps, Choc)
- **D:** 1N4148 diode (DO-35 package, through-hole)

**Diode Orientation:**
- **COL2ROW:** Cathode (banded end) toward row
- **ROW2COL:** Cathode (banded end) toward column

**Function:**
- **Anti-Ghosting:** Diodes prevent ghost keypresses when multiple keys pressed
- **Matrix Scanning:** MCU scans columns and reads rows (or vice versa)
- **Pin Reduction:** 4×12 matrix uses 16 pins instead of 48

**Matrix Sizes:**
- **4×12 (Plaid):** 4 rows × 12 columns = 48 keys
- **5×12 (Lumberjack):** 5 rows × 12 columns = 60 keys
- **5×14 (60%):** 5 rows × 14 columns = 70 keys
- **5×15 (65%):** 5 rows × 15 columns = 75 keys
- **6×17 (TKL):** 6 rows × 17 columns = 102 keys

**Projects Using:** All keyboard projects

**Notes:**
- Diode orientation critical (check firmware config)
- COL2ROW is more common than ROW2COL
- 1N4148 is standard diode (fast switching, low cost)
- Through-hole diodes easier to solder than SMD

---

## Rotary Encoder Circuit

### Pattern: EC11 Rotary Encoder (Plaid-Pad, Litl, Dumbpad)

**Description:** Rotary encoder with optional push button.

**Schematic:**
```
EC11 Rotary Encoder
│
├─ A (Phase A) ──[R: 10kΩ]── +5V (optional pull-up)
│                │
│                └──── MCU GPIO (e.g., PD4)
│
├─ B (Phase B) ──[R: 10kΩ]── +5V (optional pull-up)
│                │
│                └──── MCU GPIO (e.g., PD5)
│
├─ C (Common) ──── GND
│
├─ SW1 (Button) ──[D: 1N4148]── Row (if in matrix)
│                  │
│                  └──── MCU GPIO (if dedicated)
│
└─ SW2 (Button) ──── GND
```

**Component Values:**
- **Encoder:** EC11 rotary encoder (through-hole, 5-pin)
- **R (optional):** 2× 10kΩ pull-up resistors (if not using internal pull-ups)
- **D (optional):** 1N4148 diode (if integrating button into matrix)

**Function:**
- **Quadrature Encoding:** A and B phases provide rotation direction
- **Push Button:** Optional switch for encoder press
- **Pull-ups:** Required if MCU internal pull-ups not enabled

**Encoder Positions:**
- **Plaid-Pad:** Up to 4 encoders (interchangeable with switches)
- **Litl:** 1-2 encoders
- **Dumbpad:** 1-2 encoders

**Firmware Support:**
- **QMK:** Full support with encoder map
- **VIA:** Limited support (no encoder configuration)
- **VIAL:** Full support with encoder configuration

**Projects Using:** Plaid-Pad (up to 4), Litl (1-2), Dumbpad (1-2)

**Notes:**
- EC11 is standard encoder (11mm diameter)
- Can replace switch positions in matrix
- Pull-ups optional if using MCU internal pull-ups
- Button can be integrated into matrix or use dedicated pin


---

## OLED Display Connection

### Pattern: I2C OLED Display (Plaid-Pad, Litl, Dumbpad)

**Description:** 0.91"-0.96" OLED display with I2C interface.

**Schematic:**
```
OLED Display (128×32 or 128×64)
│
├─ VCC ──── +5V (or +3.3V depending on display)
│
├─ GND ──── GND
│
├─ SCL ──[R: 4.7kΩ]── +5V (I2C clock, pull-up)
│         │
│         └──── MCU SCL (e.g., PC5)
│
└─ SDA ──[R: 4.7kΩ]── +5V (I2C data, pull-up)
          │
          └──── MCU SDA (e.g., PC4)
```

**Component Values:**
- **Display:** 0.91"-0.96" OLED (128×32 or 128×64 pixels)
- **R (pull-ups):** 2× 4.7kΩ resistors (I2C pull-ups)
- **Connector:** 4-pin header (2.54mm pitch)

**I2C Pins (ATmega328P):**
- **SCL:** PC5 (Pin 28)
- **SDA:** PC4 (Pin 27)

**Function:**
- **I2C Communication:** Two-wire serial protocol (SCL clock, SDA data)
- **Pull-up Resistors:** Required for I2C bus (4.7kΩ typical)
- **Display Content:** Layer indicators, WPM, logos, status

**Display Options:**
- **128×32:** Smaller, 4 lines of text
- **128×64:** Larger, 8 lines of text or graphics
- **I2C Address:** Typically 0x3C or 0x3D

**Projects Using:** Plaid-Pad (Rev3), Litl, Dumbpad (combo_oled variant)

**Notes:**
- Pull-up resistors can be on display module or PCB
- Some displays have built-in pull-ups (check datasheet)
- 4.7kΩ is standard I2C pull-up value
- Display can be powered from 3.3V or 5V (check module)

---

## LED Indicators

### Pattern: Status LEDs (Plaid, Lumberjack)

**Description:** Simple LED indicators for status (Caps Lock, layer, power).

**Schematic:**
```
MCU GPIO ──[R: 220Ω-1kΩ]──[LED]── GND
           (current limiting)  │
                              (Cathode)
```

**Alternative (Active-Low):**
```
+5V ──[LED]──[R: 220Ω-1kΩ]── MCU GPIO
      │      (current limiting)
   (Anode)
```

**Component Values:**
- **LED:** 3mm or 5mm through-hole LED (red, green, blue, etc.)
- **R:** 220Ω-1kΩ resistor (current limiting)

**Current Limiting Resistor Calculation:**
```
R = (Vsupply - Vled) / Iled

For 5V supply, red LED (Vf = 2V), 10mA current:
R = (5V - 2V) / 0.01A = 300Ω (use 330Ω standard value)

For 5V supply, blue LED (Vf = 3.2V), 10mA current:
R = (5V - 3.2V) / 0.01A = 180Ω (use 220Ω standard value)
```

**Typical LED Forward Voltages:**
- **Red:** 1.8-2.2V
- **Green:** 2.0-3.0V
- **Blue:** 3.0-3.4V
- **White:** 3.0-3.4V

**Common Uses:**
- **Caps Lock:** Indicates Caps Lock state
- **Num Lock:** Indicates Num Lock state
- **Layer Indicator:** Shows active layer
- **Power Indicator:** Shows keyboard is powered

**Projects Using:** Plaid (2 LEDs), Lumberjack (2 LEDs), Dumbpad (3 LEDs)

**Notes:**
- Resistor value depends on LED color and desired brightness
- 220Ω-330Ω typical for 5V supply
- Higher resistance = dimmer LED, lower current
- Check MCU GPIO current limits (typically 20-40mA max)

---

## Power Decoupling

### Pattern: Decoupling Capacitors

**Description:** Capacitors to filter noise and stabilize power supply.

**Schematic:**
```
+5V ──┬──[C: 100nF]── GND (near MCU VCC pin)
      │
      ├──[C: 100nF]── GND (near MCU AVCC pin)
      │
      └──[C: 4.7µF]── GND (bulk capacitor near power input)
```

**Component Values:**
- **C (decoupling):** 100nF ceramic capacitors (5mm pitch)
- **C (bulk):** 4.7µF-10µF electrolytic capacitor (1.5mm pitch)

**Placement:**
- **Decoupling Caps:** As close to MCU VCC/AVCC pins as possible (<5mm)
- **Bulk Cap:** Near power input (USB connector or voltage regulator)

**Function:**
- **Decoupling Caps (100nF):** Filter high-frequency noise (>1MHz)
- **Bulk Cap (4.7µF):** Provide charge reservoir for current spikes
- **Stabilize Power:** Prevent voltage drops during switching

**Capacitor Types:**
- **Ceramic (100nF):** Fast response, low ESR, high-frequency filtering
- **Electrolytic (4.7µF):** Larger capacitance, bulk energy storage

**Projects Using:** All projects

**Notes:**
- One 100nF cap per VCC/AVCC pin minimum
- Bulk cap optional but recommended
- Ceramic caps have no polarity
- Electrolytic caps have polarity (+ and - marked)
- Place decoupling caps on same side of PCB as MCU

---

## Design Pattern Summary Table

| Pattern | Complexity | Key Components | Projects Using | Notes |
|---------|-----------|----------------|----------------|-------|
| USB-C Through-Hole | Medium | USB-C connector, 5.1kΩ resistors, zener diodes, polyfuse | Lumberjack | Modern, reversible connector |
| VUSB Software USB | Medium | USB Mini/Micro, 1.5kΩ pull-up, zener diodes, 75Ω resistors | Plaid, Plaid-Pad | Requires V-USB library |
| ATmega328P Circuit | Low | ATmega328P-PU, 16MHz crystal, 22pF caps, 100nF caps, 10kΩ resistor | Lumberjack, Plaid, Rosaline | Easy to solder, low cost |
| ATmega32A Circuit | Low | ATmega32A-PU, 16MHz crystal, 22pF caps, 100nF caps, 10kΩ resistor | Discipline, Mysterium | Native USB, more GPIO |
| Crystal Oscillator | Low | 16MHz crystal, 2× 22pF caps | All AVR projects | Required for USB timing |
| Reset Circuit | Low | 10kΩ resistor, tactile switch | All AVR projects | Manual reset/bootloader entry |
| ISP Header | Low | 2×3 pin header | Lumberjack, Plaid, Discipline | Required for V-USB, optional for native USB |
| Switch Matrix | Low | Cherry MX switches, 1N4148 diodes | All keyboard projects | Anti-ghosting, pin reduction |
| Rotary Encoder | Medium | EC11 encoder, optional 10kΩ pull-ups | Plaid-Pad, Litl, Dumbpad | Adds functionality |
| OLED Display | Medium | I2C OLED, 2× 4.7kΩ pull-ups | Plaid-Pad, Litl, Dumbpad | Visual feedback |
| LED Indicators | Low | LEDs, 220Ω-1kΩ resistors | Plaid, Lumberjack, Dumbpad | Status indication |
| Power Decoupling | Low | 100nF ceramic caps, 4.7µF electrolytic cap | All projects | Noise filtering, stability |

---

## References

### Project Repositories
- **Lumberjack:** https://github.com/peej/lumberjack-keyboard
- **Plaid:** https://github.com/hsgw/plaid
- **Plaid-Pad:** https://github.com/Keycapsss/Plaid-Pad
- **Discipline:** https://github.com/coseyfannitutti/discipline
- **Mysterium:** https://github.com/coseyfannitutti/mysterium
- **Litl:** https://github.com/mohoyt/litl
- **Dumbpad:** https://github.com/imchipwood/dumbpad

### Datasheets
- **ATmega328P:** https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega328P-Datasheet.pdf
- **ATmega32A:** https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega32A-Datasheet.pdf
- **1N4148 Diode:** https://www.vishay.com/docs/81857/1n4148.pdf
- **USB-C Specification:** https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification

### Additional Resources
- **V-USB Library:** https://www.obdev.at/products/vusb/index.html
- **QMK Firmware:** https://docs.qmk.fm/
- **PCB Design Guide:** See `PCB_DESIGN_GUIDE.md` in this library
- **Design Patterns:** See `design_patterns.md` in this library

---

## Contributing

This document is based on actual schematics from the library projects. If you find errors or have additional patterns to document, please contribute!

### Pattern Documentation Template

When documenting a new pattern:
1. **Pattern Name:** Clear, descriptive name
2. **Description:** What the pattern does
3. **Schematic:** ASCII art or text diagram
4. **Component Values:** Specific part numbers and values
5. **Function:** Explanation of how it works
6. **Projects Using:** List of projects implementing this pattern
7. **Notes:** Special considerations, variations, tips

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-20  
**Maintained By:** Through-Hole Keyboard Library Project

