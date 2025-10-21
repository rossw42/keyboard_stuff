# Component Sourcing Guide

## Overview

This guide provides vendor recommendations, sourcing strategies, and alternative part numbers for through-hole keyboard components. It covers common components used across multiple projects in the library, helping builders source parts efficiently and cost-effectively.

## Quick Reference

### Recommended Vendors by Region

#### North America
- **Mouser Electronics** - [mouser.com](https://www.mouser.com) - Comprehensive inventory, fast shipping
- **Digikey** - [digikey.com](https://www.digikey.com) - Excellent search, technical support
- **LCSC** - [lcsc.com](https://www.lcsc.com) - Budget-friendly, slower shipping from China
- **Arrow Electronics** - [arrow.com](https://www.arrow.com) - Good for bulk orders
- **Newark** - [newark.com](https://www.newark.com) - Industrial supplier, good stock

#### Europe
- **Mouser Electronics** - [mouser.com](https://www.mouser.com) - EU warehouses available
- **Farnell/Element14** - [farnell.com](https://www.farnell.com) - Strong European presence
- **RS Components** - [rs-online.com](https://www.rs-online.com) - Industrial supplier
- **TME** - [tme.eu](https://www.tme.eu) - Eastern Europe, good prices
- **Reichelt** - [reichelt.de](https://www.reichelt.de) - Germany-based

#### Asia-Pacific
- **LCSC** - [lcsc.com](https://www.lcsc.com) - China-based, excellent prices
- **Taobao/AliExpress** - Budget options, longer lead times
- **Element14** - [element14.com](https://www.element14.com) - Asia-Pacific distribution
- **RS Components** - [rs-online.com](https://www.rs-online.com) - Regional warehouses

#### Keyboard-Specific Vendors
- **NovelKeys** - [novelkeys.com](https://www.novelkeys.com) - Switches, keycaps, kits
- **Keyhive** - [keyhive.xyz](https://www.keyhive.xyz) - Through-hole keyboard kits
- **P3DStore** - [p3dstore.com](https://www.p3dstore.com) - Keyboard components
- **Keycapsss** - [keycapsss.com](https://www.keycapsss.com) - EU-based keyboard parts
- **MechBoards UK** - [mechboards.co.uk](https://www.mechboards.co.uk) - UK keyboard supplier

## Component Categories


### Resistors (Through-Hole Axial)

#### Common Values
- **10kΩ** - Most common (pull-up/pull-down resistors)
- **5.1kΩ** - USB-C CC pull-down
- **1.5kΩ** - USB D- pull-up
- **75Ω** - USB series termination

#### Recommended Parts

**10kΩ 1/4W 5% Carbon Film**
- **Mouser:** 603-CFR-25JB-52-10K
- **Digikey:** CF14JT10K0CT-ND
- **LCSC:** C17414
- **Alternative:** YAGEO CFR-25JB-52-10K
- **Price:** $0.02-0.05 each
- **MOQ:** 1 (typically sold in packs of 10-100)
- **Notes:** Standard carbon film, adequate for keyboards

**5.1kΩ 1/4W 5% Carbon Film**
- **Mouser:** 603-CFR-25JB-52-5K1
- **Digikey:** CF14JT5K10CT-ND
- **LCSC:** C133969
- **Price:** $0.02-0.05 each
- **Notes:** Required for USB-C implementations

**1.5kΩ 1/4W 5% Carbon Film**
- **Mouser:** 603-CFR-25JB-52-1K5
- **Digikey:** CF14JT1K50CT-ND
- **LCSC:** C126045
- **Price:** $0.02-0.05 each

**75Ω 1/4W 5% Carbon Film**
- **Mouser:** 603-CFR-25JB-52-75R
- **Digikey:** CF14JT75R0CT-ND
- **LCSC:** C136039
- **Price:** $0.02-0.05 each

#### Sourcing Tips
- Buy resistor kits (E12 or E24 series) for variety
- 1/4W (0.25W) is standard for keyboards
- 5% tolerance is sufficient (1% not required)
- Carbon film or metal film both work
- Typical lead time: 1-3 days (in stock)
- Bulk pricing: 100+ units often 50% cheaper


### Diodes (Through-Hole)

#### 1N4148 Small Signal Diode (DO-35)

**Primary Use:** One per switch in keyboard matrix

**Recommended Parts**

**1N4148 Standard**
- **Mouser:** 512-1N4148
- **Digikey:** 1N4148FS-ND
- **LCSC:** C81598
- **Alternative:** 1N4148W (SMD version, not compatible)
- **Price:** $0.02-0.05 each
- **MOQ:** 1 (sold in bulk packs)
- **Package:** DO-35 (through-hole)
- **Lead time:** Usually in stock

**1N4148TR (Tape & Reel)**
- **Mouser:** 512-1N4148TR
- **Digikey:** 1N4148FSTR-ND
- **Price:** $0.01-0.03 each (bulk)
- **MOQ:** 1000+ (tape and reel)
- **Notes:** Best for large production runs

#### Alternative Diodes

**1N4007** (Higher voltage rating, larger package)
- **Mouser:** 512-1N4007
- **Digikey:** 1N4007-TPCT-ND
- **LCSC:** C106902
- **Price:** $0.03-0.06 each
- **Notes:** Works but physically larger, not recommended

**1N914** (Equivalent to 1N4148)
- **Mouser:** 512-1N914
- **Price:** $0.02-0.05 each
- **Notes:** Electrically identical to 1N4148

#### Sourcing Tips
- Buy in bulk (100+ diodes for 60% keyboard)
- 1N4148 is the standard - don't substitute unless necessary
- Check lead spacing matches your PCB (typically 7.62mm)
- Typical lead time: 1-3 days (in stock)
- Bulk pricing: 100+ units often 60% cheaper
- Consider buying 10-20% extra for mistakes


### Capacitors

#### Ceramic Capacitors (0805 SMD)

**0.1µF (100nF) Decoupling Capacitors**
- **Mouser:** 80-C0805C104K5R
- **Digikey:** 399-1168-1-ND (TDK C0805C104K5RACTU)
- **LCSC:** C49678
- **Alternative:** Any 0.1µF 0805 50V X7R
- **Price:** $0.05-0.15 each
- **MOQ:** 1
- **Voltage:** 50V minimum
- **Tolerance:** ±10% (K) is standard
- **Notes:** Used for MCU and USB decoupling

**22pF Crystal Load Capacitors**
- **Mouser:** 80-C0805C220J5G
- **Digikey:** 399-1122-1-ND
- **LCSC:** C1804
- **Alternative:** Any 22pF 0805 50V C0G/NP0
- **Price:** $0.05-0.15 each
- **Tolerance:** ±5% (J) recommended
- **Notes:** Use C0G/NP0 dielectric for crystal circuits

#### Electrolytic Capacitors (Through-Hole Radial)

**4.7µF Power Smoothing**
- **Mouser:** 647-UVR1V4R7MDD (Nichicon)
- **Digikey:** P5178-ND (Panasonic EEU-FK1V472)
- **LCSC:** C134502
- **Alternative:** Any 4.7µF 35V+ radial electrolytic
- **Price:** $0.10-0.30 each
- **Voltage:** 35V minimum (50V recommended)
- **Size:** 5mm diameter typical
- **Notes:** Polarity matters - observe +/- markings

**10µF Power Smoothing (Alternative)**
- **Mouser:** 647-UVR1V100MDD
- **Digikey:** P5180-ND
- **LCSC:** C134503
- **Price:** $0.10-0.30 each
- **Notes:** Can substitute for 4.7µF in most designs

#### Sourcing Tips
- SMD capacitors require soldering skills or hot air station
- Buy capacitor kits for variety
- X7R dielectric for general purpose (0.1µF)
- C0G/NP0 dielectric for crystal circuits (22pF)
- Electrolytic capacitors have polarity - check orientation
- Typical lead time: 1-3 days (in stock)
- Bulk pricing: 100+ units often 40% cheaper


### Microcontrollers (MCUs)

#### ATmega328P (DIP-28)

**ATmega328P-PU**
- **Mouser:** 556-ATMEGA328P-PU
- **Digikey:** ATMEGA328P-PU-ND
- **LCSC:** C14877
- **Alternative:** ATmega328-PU (older version, less common)
- **Price:** $2.00-4.00 each
- **Package:** DIP-28 (through-hole)
- **Clock:** Requires external 16MHz crystal
- **Notes:** Popular for Arduino-compatible designs

**ATmega328P-AU (SMD Alternative)**
- **Mouser:** 556-ATMEGA328P-AU
- **Digikey:** ATMEGA328P-AU-ND
- **Price:** $1.50-3.00 each
- **Package:** TQFP-32 (surface mount)
- **Notes:** Requires SMD soldering skills

#### ATmega32U4 (DIP-40)

**ATmega32U4-AU**
- **Mouser:** 556-ATMEGA32U4-AU
- **Digikey:** ATMEGA32U4-AU-ND
- **LCSC:** C44854
- **Price:** $4.00-7.00 each
- **Package:** TQFP-44 (surface mount)
- **USB:** Native USB support
- **Notes:** Most common for custom keyboards, no DIP version available

#### ATmega32A (DIP-40)

**ATmega32A-PU**
- **Mouser:** 556-ATMEGA32A-PU
- **Digikey:** ATMEGA32A-PU-ND
- **LCSC:** C7411
- **Price:** $3.00-5.00 each
- **Package:** DIP-40 (through-hole)
- **Notes:** Used in some older designs

#### Pro Micro Compatible Modules

**SparkFun Pro Micro (ATmega32U4)**
- **SparkFun:** DEV-12640
- **Price:** $20-25 each
- **Notes:** Pre-programmed bootloader, USB-C or Micro-B

**Elite-C (USB-C Pro Micro)**
- **Keyhive:** [keyhive.xyz](https://keyhive.xyz/shop/elite-c)
- **Price:** $18-25 each
- **Notes:** USB-C, improved over Pro Micro

**Generic Pro Micro Clones**
- **AliExpress/eBay:** $3-8 each
- **Notes:** Quality varies, may have USB issues

#### Sourcing Tips
- ATmega32U4 has native USB (no USB-to-serial needed)
- ATmega328P requires USB-to-serial converter
- DIP packages easier to solder but larger
- Buy from authorized distributors to avoid counterfeits
- Pro Micro modules include bootloader and USB
- Typical lead time: 1-7 days (stock varies)
- Consider buying 1-2 extra MCUs as backup


### Crystals and Oscillators

#### 16MHz Crystal (HC-49/US Package)

**Standard 16MHz Crystal**
- **Mouser:** 520-HCU1600-20X
- **Digikey:** 887-1125-ND (ECS-160-20-4X)
- **LCSC:** C13738
- **Alternative:** Any 16MHz HC-49/US 20pF load
- **Price:** $0.30-0.80 each
- **Load Capacitance:** 20pF (use 22pF caps)
- **Package:** HC-49/US (through-hole)
- **Notes:** Required for ATmega328P, ATmega32A

**16MHz Crystal (HC-49/S Package - Smaller)**
- **Mouser:** 520-HCS1600-20X
- **Digikey:** 887-1126-ND
- **Price:** $0.30-0.80 each
- **Notes:** Smaller footprint, same electrical specs

#### Alternative Frequencies

**8MHz Crystal**
- **Mouser:** 520-HCU800-20X
- **Digikey:** 887-1123-ND
- **Price:** $0.30-0.80 each
- **Notes:** Some designs use 8MHz

**12MHz Crystal**
- **Mouser:** 520-HCU1200-20X
- **Price:** $0.30-0.80 each
- **Notes:** Less common in keyboards

#### Ceramic Resonators (Alternative)

**16MHz Ceramic Resonator (3-pin with built-in caps)**
- **Mouser:** 81-CSTCE16M0V53-R0
- **Digikey:** 490-1198-1-ND (Murata CSTCE16M0V53-R0)
- **LCSC:** C32346
- **Price:** $0.20-0.50 each
- **Notes:** No external caps needed, less accurate than crystal

#### Sourcing Tips
- Match crystal load capacitance to PCB design (typically 20pF)
- Use 22pF capacitors for 20pF load crystals
- Ceramic resonators simpler but less accurate
- ATmega32U4 has internal oscillator (crystal optional)
- Typical lead time: 1-3 days (in stock)
- Buy 1-2 extras (fragile during handling)


### USB Connectors

#### USB-C Through-Hole

**USB-C 16-Pin Through-Hole Receptacle**
- **Mouser:** 640-USB4105-GF-A (GCT)
- **Digikey:** 2073-USB4105-GF-ACT-ND
- **LCSC:** C165948
- **Alternative:** Korean Hroparts TYPE-C-31-M-12
- **Price:** $0.80-1.50 each
- **Pins:** 16-pin (12 signal + 4 mechanical)
- **Notes:** Most common for modern through-hole keyboards

**USB-C 6-Pin Simplified (Power + Data only)**
- **AliExpress/Taobao:** $0.30-0.80 each
- **Notes:** Cheaper but less robust, no full USB-C spec

#### USB Mini-B Through-Hole

**USB Mini-B 5-Pin Receptacle**
- **Mouser:** 649-10033526-N3212LF (Amphenol)
- **Digikey:** 609-4050-1-ND
- **LCSC:** C46398
- **Price:** $0.50-1.20 each
- **Notes:** Older standard, still used in some designs

#### USB Micro-B Through-Hole

**USB Micro-B 5-Pin Receptacle**
- **Mouser:** 649-10118194-0001LF (Amphenol)
- **Digikey:** 609-4618-1-ND
- **LCSC:** C132563
- **Price:** $0.40-1.00 each
- **Notes:** Common in older Pro Micro designs

#### Sourcing Tips
- USB-C is preferred for new designs (reversible)
- Through-hole USB connectors more durable than SMD
- Check PCB footprint matches connector pinout
- Buy from reputable vendors (USB connectors often counterfeit)
- Consider buying 2-3 extras (most likely to fail during assembly)
- Typical lead time: 1-5 days (stock varies)
- Mechanical pins provide strain relief


### Switches and Buttons

#### Tactile Push Buttons (Reset/Boot)

**6mm x 6mm Tactile Switch (Through-Hole)**
- **Mouser:** 653-B3F-1000 (Omron)
- **Digikey:** SW400-ND
- **LCSC:** C318884
- **Alternative:** Generic 6x6mm tactile switches
- **Price:** $0.15-0.40 each
- **Height:** 4.3mm, 5mm, 7mm, 9mm (check PCB clearance)
- **Notes:** Most common for reset buttons

**12mm x 12mm Tactile Switch (Larger)**
- **Mouser:** 653-B3F-5000
- **Digikey:** SW1020-ND
- **LCSC:** C136681
- **Price:** $0.20-0.50 each
- **Notes:** Easier to press, larger footprint

#### Mechanical Keyboard Switches

**Cherry MX Switches**
- **NovelKeys:** [novelkeys.com](https://www.novelkeys.com)
- **MechBoards:** [mechboards.co.uk](https://www.mechboards.co.uk)
- **Price:** $0.50-1.00 each (bulk)
- **Types:** Red (linear), Brown (tactile), Blue (clicky)
- **MOQ:** Usually sold in packs of 10
- **Notes:** Genuine Cherry MX, premium quality

**Gateron Switches**
- **NovelKeys:** [novelkeys.com](https://www.novelkeys.com)
- **AliExpress:** $0.20-0.40 each (bulk)
- **Price:** $0.20-0.50 each
- **Types:** Red, Brown, Blue, Yellow, Black, Clear
- **Notes:** Cherry MX compatible, budget-friendly

**Kailh Switches**
- **NovelKeys:** [novelkeys.com](https://www.novelkeys.com)
- **Price:** $0.25-0.60 each
- **Types:** Box switches, Speed switches, Pro switches
- **Notes:** Various options, good quality

#### Sourcing Tips
- Buy switches in bulk (10-20% extra for testing)
- Tactile buttons: check height matches PCB clearance
- Mechanical switches: test different types before bulk order
- Consider switch testers before committing
- Typical lead time: 1-7 days (switches), 1-3 days (tactile buttons)
- Keyboard vendors often have better switch prices than electronics distributors


### LEDs and Indicators

#### Through-Hole LEDs (3mm and 5mm)

**3mm LED (Various Colors)**
- **Mouser:** 604-WP3A8HD (Red, Kingbright)
- **Digikey:** 160-1144-ND (Red)
- **LCSC:** C72038 (Red)
- **Price:** $0.10-0.30 each
- **Colors:** Red, Green, Blue, Yellow, White
- **Forward Voltage:** 1.8-3.3V (depends on color)
- **Notes:** Smaller, good for status indicators

**5mm LED (Various Colors)**
- **Mouser:** 604-WP7113ID (Red, Kingbright)
- **Digikey:** 160-1707-ND (Red)
- **LCSC:** C84256 (Red)
- **Price:** $0.10-0.30 each
- **Colors:** Red, Green, Blue, Yellow, White
- **Notes:** Brighter, more common

#### RGB LEDs (Through-Hole)

**5mm RGB LED (Common Cathode)**
- **Mouser:** 604-WP154A4SUREQBFZGC
- **Digikey:** 1125-1578-ND
- **LCSC:** C193096
- **Price:** $0.30-0.80 each
- **Pins:** 4-pin (R, G, B, Common)
- **Notes:** Requires PWM control for colors

#### WS2812B RGB LED (SMD - Addressable)

**WS2812B 5050 SMD**
- **Mouser:** 474-COM-12986
- **Digikey:** 1528-2343-ND
- **LCSC:** C114583
- **Price:** $0.10-0.30 each
- **Package:** 5050 SMD (5mm x 5mm)
- **Notes:** Addressable RGB, requires SMD soldering

#### Sourcing Tips
- Check forward voltage and current requirements
- Use appropriate current-limiting resistors (typically 220Ω-1kΩ)
- Red LEDs: ~1.8-2.2V, Green/Blue: ~3.0-3.3V
- Buy LED assortment kits for variety
- Consider brightness (mcd rating) for visibility
- Typical lead time: 1-3 days (in stock)
- Buy 2-3 extras (easy to damage during soldering)


### Headers and Connectors

#### Pin Headers (2.54mm Pitch)

**Single Row Pin Header (Male)**
- **Mouser:** 649-68000-236HLF (36-pin, break-apart)
- **Digikey:** S1012EC-36-ND
- **LCSC:** C50981 (40-pin)
- **Price:** $0.50-1.50 per 40-pin strip
- **Pitch:** 2.54mm (0.1")
- **Notes:** Break to desired length, used for ISP/programming

**Double Row Pin Header (2x3, 2x5, etc.)**
- **Mouser:** 649-77313-118-06LF (2x3)
- **Digikey:** S9169-ND (2x3)
- **LCSC:** C65114 (2x3)
- **Price:** $0.20-0.60 each
- **Notes:** Common for ISP programming headers

**Female Pin Header (Socket)**
- **Mouser:** 649-68602-140HLF (40-pin)
- **Digikey:** S7122-ND
- **LCSC:** C50982 (40-pin)
- **Price:** $0.80-2.00 per 40-pin strip
- **Notes:** Used for socketing Pro Micro or other modules

#### TRRS Connectors (Split Keyboards)

**PJ-320A TRRS Jack (3.5mm)**
- **Mouser:** 490-PJ-320A
- **Digikey:** CP-43514-ND
- **LCSC:** C7501
- **Price:** $0.30-0.80 each
- **Pins:** 4-pin (Tip, Ring1, Ring2, Sleeve)
- **Notes:** Standard for split keyboard interconnect

**PJ-324M TRRS Jack (Alternative)**
- **Mouser:** 490-PJ-324M
- **Price:** $0.40-0.90 each
- **Notes:** Different footprint, check PCB compatibility

#### IC Sockets

**28-Pin DIP Socket (for ATmega328P)**
- **Mouser:** 517-4828-6004-CP
- **Digikey:** A100206-ND
- **LCSC:** C2905
- **Price:** $0.30-0.80 each
- **Notes:** Allows MCU replacement without desoldering

**40-Pin DIP Socket (for ATmega32A)**
- **Mouser:** 517-4840-6000-CP
- **Digikey:** A100208-ND
- **LCSC:** C2906
- **Price:** $0.40-1.00 each

#### Sourcing Tips
- Buy pin headers in long strips and break to length
- Female headers useful for socketing modules (Pro Micro)
- IC sockets recommended for expensive MCUs
- TRRS jacks: verify footprint matches PCB
- Typical lead time: 1-3 days (in stock)
- Buy pin header assortment kits for flexibility


### Optional Components

#### Rotary Encoders

**EC11 Rotary Encoder (Through-Hole)**
- **Mouser:** 652-PEC11R-4215F-S24
- **Digikey:** PEC11R-4215F-S0024-ND
- **LCSC:** C255515
- **Alternative:** Generic EC11 encoders
- **Price:** $1.00-2.50 each
- **Detents:** 24 per rotation (most common)
- **Pins:** 5-pin (A, B, C, SW1, SW2)
- **Notes:** Includes push button switch

**EC11 with Knob**
- **AliExpress:** $1.50-3.00 each (with knob)
- **Notes:** Knob diameter typically 15-20mm

#### OLED Displays

**0.96" I2C OLED Display (128x64)**
- **Mouser:** 485-3650 (Adafruit)
- **AliExpress:** $2-5 each
- **LCSC:** C347501
- **Price:** $3-8 each
- **Interface:** I2C (4-pin: VCC, GND, SCL, SDA)
- **Notes:** Common in macropads, requires I2C support

**0.91" I2C OLED Display (128x32)**
- **AliExpress:** $2-4 each
- **Price:** $2-6 each
- **Notes:** Smaller, lower resolution

#### Zener Diodes (USB Protection)

**3.6V Zener Diode (DO-35)**
- **Mouser:** 512-1N4728A
- **Digikey:** 1N4728AFSCT-ND
- **LCSC:** C151000
- **Price:** $0.10-0.30 each
- **Notes:** Used for USB D+/D- ESD protection

**5.1V Zener Diode (DO-35)**
- **Mouser:** 512-1N4733A
- **Digikey:** 1N4733AFSCT-ND
- **LCSC:** C151001
- **Price:** $0.10-0.30 each

#### Polyfuses (Resettable Fuses)

**500mA Polyfuse (Radial)**
- **Mouser:** 650-RUSBF050-2
- **Digikey:** 507-1802-ND (Bourns MF-R050)
- **LCSC:** C70066
- **Price:** $0.20-0.50 each
- **Hold Current:** 500mA
- **Trip Current:** 1000mA
- **Notes:** USB overcurrent protection

#### Sourcing Tips
- Rotary encoders: verify detent count (15, 20, 24 common)
- OLED displays: check I2C address (usually 0x3C or 0x3D)
- Zener diodes: match voltage to USB spec (3.6V for D+/D-)
- Polyfuses: 500mA typical for USB 2.0
- Typical lead time: 1-7 days (varies by component)
- Optional components: buy only if design requires them


## Sourcing Strategies

### Budget-Conscious Sourcing

**Recommended Approach:**
1. **Passive components** (resistors, capacitors, diodes) - Buy from LCSC or AliExpress
2. **MCUs and ICs** - Buy from authorized distributors (Mouser, Digikey) to avoid counterfeits
3. **Mechanical switches** - Buy from keyboard vendors (NovelKeys, Keyhive) or AliExpress
4. **USB connectors** - Buy from authorized distributors (quality critical)

**Estimated Cost Breakdown (60% Keyboard):**
- Passive components (resistors, caps, diodes): $5-10
- MCU (ATmega32U4): $4-7
- USB connector: $1-2
- Crystal and caps: $1-2
- Switches (61x): $12-60 (depends on switch choice)
- Optional components: $5-15
- **Total:** $28-96 (excluding PCB, case, keycaps)

### Quality-Focused Sourcing

**Recommended Approach:**
1. Buy all components from authorized distributors (Mouser, Digikey)
2. Choose premium switches (Cherry MX, Gateron Pro)
3. Use IC sockets for MCUs
4. Add ESD protection (zener diodes, polyfuses)

**Estimated Cost Breakdown (60% Keyboard):**
- Passive components: $10-15
- MCU: $5-8
- USB connector: $1.50-2.50
- Crystal and caps: $1.50-2.50
- Switches (61x): $30-60
- Optional components: $10-20
- **Total:** $58-108 (excluding PCB, case, keycaps)

### Bulk Ordering

**When to Buy in Bulk:**
- Building multiple keyboards (5+ units)
- Starting a group buy or small production run
- Stocking components for future projects

**Bulk Pricing Examples:**
- Resistors: 50% cheaper at 100+ units
- Diodes: 60% cheaper at 100+ units
- Capacitors: 40% cheaper at 100+ units
- MCUs: 20-30% cheaper at 10+ units
- Switches: 10-20% cheaper at 100+ units

**Recommended Bulk Quantities:**
- Resistors: 100-500 per value
- Diodes (1N4148): 500-1000
- Capacitors: 100-200 per value
- MCUs: 10-25
- Switches: 100-500


### Lead Times and Availability

#### Typical Lead Times by Vendor

**North America:**
- **Mouser/Digikey:** 1-3 days (in stock), 2-8 weeks (backorder)
- **Arrow/Newark:** 2-5 days (in stock)
- **LCSC (to US):** 7-21 days (standard shipping)
- **AliExpress:** 14-45 days (varies by seller)

**Europe:**
- **Mouser/Farnell:** 1-3 days (in stock)
- **TME/Reichelt:** 2-5 days (in stock)
- **LCSC (to EU):** 10-25 days (standard shipping)

**Asia-Pacific:**
- **LCSC (domestic China):** 1-3 days
- **Element14:** 2-5 days (in stock)
- **Local distributors:** 1-3 days

#### Component Availability Notes

**High Availability (Usually In Stock):**
- Resistors (common values)
- Diodes (1N4148)
- Ceramic capacitors (0.1µF, 22pF)
- Crystals (16MHz)
- Pin headers
- Tactile switches

**Moderate Availability (May Have Lead Times):**
- MCUs (ATmega32U4, ATmega328P) - chip shortage affects availability
- USB-C connectors (through-hole)
- Electrolytic capacitors (specific values)
- Mechanical switches (popular types)

**Low Availability (Often Backorder):**
- Specialized MCUs
- Rare switch types
- Custom connectors
- Obsolete components

#### Shortage Mitigation Strategies

1. **Check stock before designing** - Verify components available
2. **Design with alternatives** - Support multiple MCU footprints
3. **Buy critical components early** - MCUs, USB connectors
4. **Use common values** - Standard resistor/capacitor values
5. **Monitor stock levels** - Set up alerts for backorder items
6. **Consider pre-orders** - For group buys or production runs


### Minimum Order Quantities (MOQ)

#### Components with MOQ Considerations

**No MOQ (Buy Single Units):**
- Most passive components from Mouser/Digikey
- MCUs (DIP packages)
- USB connectors
- Crystals
- Switches and buttons

**Small MOQ (10-100 units):**
- Mechanical switches (often sold in packs of 10)
- Pin headers (sold as 40-pin strips)
- Some specialized connectors

**Large MOQ (1000+ units):**
- Tape and reel components (production quantities)
- Custom components
- Some SMD components from LCSC

#### MOQ Workarounds

1. **Buy from distributors** - Mouser/Digikey have no MOQ
2. **Use cut tape** - Buy partial reels from distributors
3. **Group orders** - Combine with other builders
4. **Buy assortment kits** - Pre-packaged component sets
5. **Accept higher unit cost** - Small quantities cost more

### Shipping Considerations

#### Shipping Costs by Vendor

**Free Shipping Thresholds:**
- **Mouser:** $50+ (US), varies by region
- **Digikey:** $50+ (US), varies by region
- **Arrow:** Often free shipping
- **LCSC:** $20+ (standard), $50+ (express)

**Typical Shipping Costs:**
- **Mouser/Digikey (US):** $5-8 (standard), $15-25 (express)
- **LCSC (international):** $5-15 (standard), $25-40 (express)
- **AliExpress:** $0-5 (slow), $10-20 (fast)

#### Shipping Speed vs Cost

**Standard Shipping:**
- Cost: $5-10
- Time: 3-7 days (domestic), 10-25 days (international)
- Best for: Non-urgent orders, bulk components

**Express Shipping:**
- Cost: $15-40
- Time: 1-3 days (domestic), 3-7 days (international)
- Best for: Urgent orders, critical components

**Economy Shipping:**
- Cost: $0-5
- Time: 14-45 days (international)
- Best for: Budget builds, non-critical components


## Project-Specific Sourcing

### 60% Keyboard (e.g., Discipline, Tartan)

**Component Count:**
- Diodes: 60-68
- Resistors: 12-16
- Capacitors: 5-10
- MCU: 1
- USB connector: 1
- Crystal: 1
- Switches: 61
- Tactile buttons: 1-2
- LEDs: 1-3 (optional)

**Estimated Cost:** $30-100 (excluding PCB, case, keycaps)

**Recommended Vendors:**
- Passive components: LCSC or Mouser
- MCU: Mouser or Digikey
- Switches: NovelKeys or Keyhive
- USB connector: Mouser or Digikey

### 65% Keyboard (e.g., Mysterium, KBIC65)

**Component Count:**
- Diodes: 68-70
- Resistors: 12-16
- Capacitors: 5-10
- MCU: 1
- USB connector: 1
- Crystal: 1
- Switches: 68
- Tactile buttons: 1-2
- LEDs: 1-3 (optional)

**Estimated Cost:** $32-105 (excluding PCB, case, keycaps)

### TKL Keyboard (e.g., Mysterium TKL)

**Component Count:**
- Diodes: 87-104
- Resistors: 12-20
- Capacitors: 8-12
- MCU: 1
- USB connector: 1
- Crystal: 1
- Switches: 87-104
- Tactile buttons: 1-2
- LEDs: 2-5 (optional)

**Estimated Cost:** $45-140 (excluding PCB, case, keycaps)

### 40% Keyboard (e.g., Plaid, Rosaline, Litl)

**Component Count:**
- Diodes: 40-48
- Resistors: 10-12
- Capacitors: 4-8
- MCU: 1
- USB connector: 1
- Crystal: 1
- Switches: 40-48
- Tactile buttons: 1-2
- LEDs: 1-2 (optional)

**Estimated Cost:** $25-85 (excluding PCB, case, keycaps)

### Macropad (e.g., Plaid-Pad, Dumbpad, Neopad)

**Component Count:**
- Diodes: 4-16
- Resistors: 8-12
- Capacitors: 4-6
- MCU: 1
- USB connector: 1
- Crystal: 1
- Switches: 4-16
- Tactile buttons: 1
- Rotary encoders: 0-2 (optional)
- OLED display: 0-1 (optional)
- LEDs: 0-4 (optional)

**Estimated Cost:** $15-50 (excluding PCB, case, keycaps)


## Vendor Comparison

### Electronics Distributors

| Vendor | Region | Shipping | MOQ | Stock | Price | Best For |
|--------|--------|----------|-----|-------|-------|----------|
| **Mouser** | Global | Fast | None | Excellent | Medium | Quality, variety, fast shipping |
| **Digikey** | Global | Fast | None | Excellent | Medium | Technical support, datasheets |
| **LCSC** | Global (China) | Slow | Low | Good | Low | Budget builds, bulk orders |
| **Arrow** | Global | Fast | None | Good | Medium | Free shipping, samples |
| **Newark** | Global | Medium | None | Good | Medium | Industrial, bulk |
| **Farnell** | Europe | Fast | None | Excellent | Medium | EU builders, fast delivery |
| **TME** | Europe | Fast | Low | Good | Low-Medium | Eastern Europe, good prices |
| **RS Components** | Global | Medium | Low | Good | Medium | Industrial, technical |

### Keyboard-Specific Vendors

| Vendor | Region | Shipping | Specialty | Price | Best For |
|--------|--------|----------|-----------|-------|----------|
| **NovelKeys** | US | Fast | Switches, keycaps | Medium | Premium switches, US builders |
| **Keyhive** | US | Fast | Kits, components | Medium | Through-hole kits, Pro Micro |
| **P3DStore** | US | Medium | Kits, PCBs | Medium | Complete kits, cases |
| **Keycapsss** | EU | Fast | Kits, switches | Medium | EU builders, German shipping |
| **MechBoards UK** | UK | Fast | Switches, keycaps | Medium | UK/EU builders |
| **KBDfans** | China | Slow | Cases, PCBs | Low-Medium | Budget cases, stabilizers |
| **AliExpress** | China | Very Slow | Everything | Very Low | Budget builds, patience required |

### Vendor Selection Guide

**Choose Mouser/Digikey when:**
- Need components quickly (1-3 days)
- Building first keyboard (quality assurance)
- Need technical support or datasheets
- Want no MOQ restrictions
- Willing to pay medium prices

**Choose LCSC when:**
- Building multiple keyboards (bulk)
- Budget is primary concern
- Can wait 2-3 weeks for shipping
- Comfortable with Chinese vendors
- Need common components in quantity

**Choose Keyboard Vendors when:**
- Buying mechanical switches
- Need keycaps or stabilizers
- Want pre-tested component kits
- Building specific keyboard designs
- Want community-recommended parts

**Choose AliExpress when:**
- Absolute lowest cost is priority
- Can wait 3-6 weeks for shipping
- Comfortable with variable quality
- Buying non-critical components
- Willing to deal with potential issues


## Tips and Best Practices

### General Sourcing Tips

1. **Create a BOM spreadsheet** - Track components, quantities, vendors, prices
2. **Compare prices** - Check multiple vendors before ordering
3. **Check stock availability** - Verify components in stock before designing
4. **Buy extras** - 10-20% extra for mistakes and testing
5. **Consolidate orders** - Combine multiple projects to save shipping
6. **Use parametric search** - Filter by specs on Mouser/Digikey
7. **Read datasheets** - Verify specifications match requirements
8. **Check footprints** - Ensure physical package matches PCB
9. **Consider alternatives** - Have backup part numbers ready
10. **Track orders** - Keep records of what you ordered and when

### Cost Optimization

**Ways to Reduce Component Costs:**

1. **Buy from LCSC** - 30-50% cheaper than Mouser/Digikey
2. **Order in bulk** - Significant discounts at 100+ units
3. **Use generic parts** - Avoid brand-name when possible
4. **Combine orders** - Split shipping costs with friends
5. **Wait for sales** - Keyboard vendors have periodic sales
6. **Buy kits** - Pre-packaged component sets often cheaper
7. **Use standard values** - Common resistor/capacitor values cheaper
8. **Avoid expedited shipping** - Standard shipping usually adequate
9. **Buy switches in bulk** - 100+ switches often 20% cheaper
10. **Consider clones** - Pro Micro clones vs genuine SparkFun

**Cost vs Quality Trade-offs:**

- **Critical components** (MCU, USB connector) - Buy quality
- **Passive components** (resistors, caps, diodes) - Generic fine
- **Mechanical switches** - Test before bulk order
- **Connectors** - Quality matters for durability
- **LEDs** - Generic usually adequate
- **Crystals** - Quality affects timing accuracy

### Quality Assurance

**How to Avoid Counterfeit Components:**

1. **Buy from authorized distributors** - Mouser, Digikey, Arrow, Farnell
2. **Avoid too-good-to-be-true prices** - Especially for MCUs
3. **Check packaging** - Genuine parts have proper labeling
4. **Verify markings** - Compare to datasheet photos
5. **Test components** - Use multimeter to verify values
6. **Buy from reputable sellers** - Check reviews and ratings
7. **Avoid gray market** - Stick to authorized channels for ICs
8. **Document sources** - Keep records of where you bought components

**Component Testing:**

- **Resistors:** Use multimeter to verify resistance
- **Capacitors:** Check capacitance with LCR meter
- **Diodes:** Test forward voltage drop (~0.7V for 1N4148)
- **LEDs:** Test with current-limiting resistor
- **MCUs:** Program test firmware before soldering
- **Crystals:** Check frequency with oscilloscope (if available)


### Common Sourcing Mistakes

**Mistakes to Avoid:**

1. **Wrong package type** - Ordering SMD when need through-hole
2. **Incorrect footprint** - Component doesn't fit PCB pads
3. **Wrong voltage rating** - Capacitors/resistors under-rated
4. **Insufficient quantity** - Not buying enough for mistakes
5. **Ignoring lead times** - Ordering backordered components
6. **Wrong crystal load capacitance** - Mismatched caps and crystal
7. **Incompatible USB connector** - Footprint doesn't match PCB
8. **Wrong MCU variant** - DIP vs SMD, different pin counts
9. **Forgetting optional components** - Encoders, OLEDs, etc.
10. **Not checking stock** - Designing with unavailable parts

**How to Avoid Mistakes:**

- **Double-check footprints** - Compare datasheet to PCB
- **Verify specifications** - Read component descriptions carefully
- **Use parametric search** - Filter by exact requirements
- **Check stock before ordering** - Avoid backorders
- **Buy from BOM** - Use project-provided BOM when available
- **Ask community** - Check forums for component recommendations
- **Order samples first** - Test fit before bulk order
- **Keep datasheets** - Reference during assembly
- **Use component checklist** - Verify all components before ordering
- **Test components** - Verify before soldering

### Troubleshooting Sourcing Issues

**Problem: Component out of stock**
- **Solution:** Check alternative vendors, find equivalent part, consider redesign

**Problem: Component too expensive**
- **Solution:** Buy from LCSC, order in bulk, find generic alternative

**Problem: Long lead time**
- **Solution:** Order early, find in-stock alternative, use different vendor

**Problem: Wrong component received**
- **Solution:** Contact vendor, verify part number, check packaging

**Problem: Component doesn't fit PCB**
- **Solution:** Verify footprint, check datasheet, consider adapter

**Problem: Counterfeit component suspected**
- **Solution:** Buy from authorized distributor, test component, return if fake

**Problem: Minimum order quantity too high**
- **Solution:** Use different vendor, buy cut tape, group order with others

**Problem: Shipping cost too high**
- **Solution:** Consolidate orders, use slower shipping, reach free shipping threshold


## Sample BOMs and Shopping Lists

### Basic 60% Keyboard BOM (Budget Build)

**Total Estimated Cost: $30-50** (excluding PCB, case, keycaps)

| Component | Quantity | Vendor | Part Number | Unit Price | Total |
|-----------|----------|--------|-------------|------------|-------|
| 1N4148 Diode | 70 | LCSC | C81598 | $0.02 | $1.40 |
| 10kΩ Resistor | 15 | LCSC | C17414 | $0.02 | $0.30 |
| 5.1kΩ Resistor | 2 | LCSC | C133969 | $0.02 | $0.04 |
| 1.5kΩ Resistor | 1 | LCSC | C126045 | $0.02 | $0.02 |
| 75Ω Resistor | 1 | LCSC | C136039 | $0.02 | $0.02 |
| 0.1µF Capacitor (0805) | 8 | LCSC | C49678 | $0.05 | $0.40 |
| 22pF Capacitor (0805) | 2 | LCSC | C1804 | $0.05 | $0.10 |
| 4.7µF Capacitor (radial) | 2 | LCSC | C134502 | $0.15 | $0.30 |
| ATmega32U4-AU | 1 | Mouser | 556-ATMEGA32U4-AU | $5.00 | $5.00 |
| 16MHz Crystal | 1 | LCSC | C13738 | $0.40 | $0.40 |
| USB-C Connector | 1 | Mouser | 640-USB4105-GF-A | $1.20 | $1.20 |
| Tactile Switch (6x6mm) | 2 | LCSC | C318884 | $0.15 | $0.30 |
| Gateron Switches | 61 | AliExpress | - | $0.25 | $15.25 |
| 28-pin DIP Socket | 1 | LCSC | C2905 | $0.40 | $0.40 |
| Pin Header (40-pin) | 1 | LCSC | C50981 | $0.80 | $0.80 |
| **Subtotal** | | | | | **$25.93** |
| **Shipping (LCSC)** | | | | | **$8.00** |
| **Shipping (Mouser)** | | | | | **$6.00** |
| **Grand Total** | | | | | **$39.93** |

### Premium 60% Keyboard BOM (Quality Build)

**Total Estimated Cost: $60-90** (excluding PCB, case, keycaps)

| Component | Quantity | Vendor | Part Number | Unit Price | Total |
|-----------|----------|--------|-------------|------------|-------|
| 1N4148 Diode | 70 | Mouser | 512-1N4148 | $0.04 | $2.80 |
| 10kΩ Resistor | 15 | Mouser | 603-CFR-25JB-52-10K | $0.04 | $0.60 |
| 5.1kΩ Resistor | 2 | Mouser | 603-CFR-25JB-52-5K1 | $0.04 | $0.08 |
| 1.5kΩ Resistor | 1 | Mouser | 603-CFR-25JB-52-1K5 | $0.04 | $0.04 |
| 75Ω Resistor | 1 | Mouser | 603-CFR-25JB-52-75R | $0.04 | $0.04 |
| 0.1µF Capacitor (0805) | 8 | Mouser | 80-C0805C104K5R | $0.10 | $0.80 |
| 22pF Capacitor (0805) | 2 | Mouser | 80-C0805C220J5G | $0.10 | $0.20 |
| 4.7µF Capacitor (radial) | 2 | Mouser | 647-UVR1V4R7MDD | $0.20 | $0.40 |
| ATmega32U4-AU | 1 | Mouser | 556-ATMEGA32U4-AU | $6.00 | $6.00 |
| 16MHz Crystal | 1 | Mouser | 520-HCU1600-20X | $0.60 | $0.60 |
| USB-C Connector | 1 | Mouser | 640-USB4105-GF-A | $1.50 | $1.50 |
| Tactile Switch (6x6mm) | 2 | Mouser | 653-B3F-1000 | $0.30 | $0.60 |
| 3.6V Zener Diode | 2 | Mouser | 512-1N4728A | $0.20 | $0.40 |
| 500mA Polyfuse | 1 | Mouser | 650-RUSBF050-2 | $0.40 | $0.40 |
| Cherry MX Red Switches | 61 | NovelKeys | - | $0.65 | $39.65 |
| 28-pin DIP Socket | 1 | Mouser | 517-4828-6004-CP | $0.60 | $0.60 |
| Pin Header (40-pin) | 1 | Mouser | 649-68000-236HLF | $1.20 | $1.20 |
| 3mm Red LED | 2 | Mouser | 604-WP3A8HD | $0.20 | $0.40 |
| **Subtotal** | | | | | **$56.31** |
| **Shipping (Mouser)** | | | | | **Free (>$50)** |
| **Shipping (NovelKeys)** | | | | | **$5.00** |
| **Grand Total** | | | | | **$61.31** |


### Macropad BOM (4x4 with Encoder)

**Total Estimated Cost: $20-35** (excluding PCB, case, keycaps)

| Component | Quantity | Vendor | Part Number | Unit Price | Total |
|-----------|----------|--------|-------------|------------|-------|
| 1N4148 Diode | 20 | LCSC | C81598 | $0.02 | $0.40 |
| 10kΩ Resistor | 10 | LCSC | C17414 | $0.02 | $0.20 |
| 0.1µF Capacitor (0805) | 6 | LCSC | C49678 | $0.05 | $0.30 |
| 22pF Capacitor (0805) | 2 | LCSC | C1804 | $0.05 | $0.10 |
| ATmega328P-PU | 1 | Mouser | 556-ATMEGA328P-PU | $3.00 | $3.00 |
| 16MHz Crystal | 1 | LCSC | C13738 | $0.40 | $0.40 |
| USB-C Connector | 1 | Mouser | 640-USB4105-GF-A | $1.20 | $1.20 |
| Tactile Switch (6x6mm) | 1 | LCSC | C318884 | $0.15 | $0.15 |
| EC11 Rotary Encoder | 1 | AliExpress | - | $1.50 | $1.50 |
| 0.96" OLED Display | 1 | AliExpress | - | $3.00 | $3.00 |
| Gateron Switches | 16 | AliExpress | - | $0.25 | $4.00 |
| 28-pin DIP Socket | 1 | LCSC | C2905 | $0.40 | $0.40 |
| **Subtotal** | | | | | **$14.65** |
| **Shipping** | | | | | **$10.00** |
| **Grand Total** | | | | | **$24.65** |

## Additional Resources

### Online Tools

**Component Search:**
- [Octopart](https://octopart.com) - Multi-vendor component search and price comparison
- [Findchips](https://www.findchips.com) - Component availability and pricing
- [SiliconExpert](https://www.siliconexpert.com) - Component lifecycle and obsolescence

**BOM Management:**
- [KiCad BOM Plugin](https://github.com/SchrodingersGat/KiBoM) - Generate BOMs from KiCad
- [Interactive HTML BOM](https://github.com/openscopeproject/InteractiveHtmlBom) - Assembly helper
- [Google Sheets](https://sheets.google.com) - Simple BOM tracking

**Datasheets:**
- [Mouser](https://www.mouser.com) - Comprehensive datasheet library
- [Digikey](https://www.digikey.com) - Technical resources and datasheets
- [Alldatasheet](https://www.alldatasheet.com) - Datasheet search engine

### Community Resources

**Forums and Communities:**
- [r/MechanicalKeyboards](https://reddit.com/r/MechanicalKeyboards) - General keyboard discussion
- [r/olkb](https://reddit.com/r/olkb) - Custom keyboard builds
- [GeekHack](https://geekhack.org) - Keyboard enthusiast forum
- [Deskthority](https://deskthority.net) - Keyboard wiki and forum
- [QMK Discord](https://discord.gg/qmk) - Firmware and hardware help

**Build Guides and Tutorials:**
- [Keyboard University](https://keyboard.university) - Comprehensive keyboard knowledge
- [ai03 PCB Design Guide](https://wiki.ai03.com/books/pcb-design) - PCB design tutorials
- [Masterzen's Keyboard Firmware](https://www.masterzen.fr/2018/12/16/handwired-keyboard-build-log-part-1/) - Firmware guide

### Related Documentation

- [Master BOM Database](../boms/master-bom.csv) - Consolidated component list
- [BOM Consolidation Guide](bom_consolidation_guide.md) - BOM processing workflow
- [Repository Inventory](repository_inventory.md) - Project catalog with component info
- [Manufacturing Guide](manufacturing_guide.md) - PCB ordering and assembly

## Changelog

**Version 1.0** (2024-10-17)
- Initial component sourcing guide
- Added vendor recommendations by region
- Included component categories with part numbers
- Added sourcing strategies and cost optimization
- Included sample BOMs for different keyboard types
- Added troubleshooting and best practices

---

**Last Updated:** October 17, 2024

**Maintainer:** Through-Hole Keyboard Library Project

**License:** CC BY-SA 4.0 (Creative Commons Attribution-ShareAlike 4.0 International)

