# Wireless PCB Design Guide (ZMK/nRF52840)

Advanced guide for designing wireless keyboard PCBs using nRF52840 and ZMK firmware.

**Based on:** ebastler's ZMK Design Guide v3  
**Target:** Advanced designers with basic PCB knowledge

---

## Overview

Wireless keyboards require additional components beyond standard wired designs:
- Battery management system
- Bluetooth MCU module
- Power switching
- Battery voltage sensing
- Low-power design considerations

---

## Component Selection

### MCU Modules

**nRF52840 Modules** (Recommended)

**Option 1: Holyiot 18010**
- Pros: Compact, certified, affordable
- Cons: Fewer exposed pins
- Use case: Compact keyboards

**Option 2: E73-2G4M08S1C**
- Pros: More pins, good availability
- Cons: Larger footprint
- Use case: Full-size keyboards

**Option 3: nice!nano**
- Pros: Pro Micro compatible, easy
- Cons: More expensive, less integrated
- Use case: Quick wireless conversion

**Why Modules vs Bare Chip:**
- Pre-certified (FCC, CE, etc.)
- Easier routing (no 4-layer + microvias needed)
- Proven antenna design
- Lower risk

### Battery Management ICs

**Simple: TP4056**
- Cost: ~$0.20
- Features: Basic charging
- Current: Programmable (250-500mA)
- Limitation: Can't power load while charging properly
- Use case: Budget builds, low power draw

**Advanced: BQ24075**
- Cost: ~$2.00
- Features: PowerPath, dynamic current limiting
- Current: Up to 500mA (USB 2.0 compliant)
- Benefits: Powers board while charging, battery supplement
- Use case: Professional builds, LED underglow

### Batteries

**LiPo/Li-Ion Single Cell (3.7V nominal)**
- Capacity: 300-2000mAh typical
- Form factor: Match keyboard cavity
- Protection: Built-in PCM recommended
- Connector: JST-PH 2.0mm (standard)

**Capacity Guidelines:**
- No LEDs: 300-500mAh = months of use
- With LEDs: 1000-2000mAh = days/weeks
- Use ZMK Power Profiler: https://zmk.dev/power-profiler

**Safety:**
- Add protective layer between battery and switch pins
- Use proper polarity (red=+, black=-)
- Never short circuit
- Don't puncture

---

## Circuit Design

### USB-C with Protection

```
J1: USB-C Connector (HRO Type-C-31-M-12/14)
├── R1, R2: 5.1kΩ (CC configuration)
├── L1, L2: Ferrite beads 600Ω@100MHz (EMI filter)
├── D1: USBLC6-2SC6 (ESD protection)
├── F1: Polyfuse 500mA (overcurrent)
└── C1, C2: 100nF (decoupling)
```

**Ground Strategy:**
- Shield → Connector GND (single ferrite bead filter)
- Case → Shield/Connector GND only
- Avoid case to circuit GND connection

### Battery Management - Simple (TP4056)

```
U1: TP4056
├── PROG (R9): 5kΩ = 250mA, 2kΩ = 500mA
├── TEMP: Disabled (most batteries have built-in protection)
├── CHRG: LED indicator (charging)
├── STDBY: LED indicator (charged)
└── BAT+/BAT-: To battery connector

Q1: Ideal diode circuit (optional)
├── D2: Schottky diode (USB → MCU when plugged)
└── Q1: P-channel MOSFET (battery → MCU when unplugged)
```

**Charging Current Selection:**
- Formula: R_PROG = 1200V / I_charge
- 250mA: R = 4.8kΩ (use 5.1kΩ)
- 500mA: R = 2.4kΩ (use 2.2kΩ)
- Recommended: 0.5C to 1C of battery capacity

**Limitations:**
- TP4056 measures battery current to detect full charge
- Board current draw interferes with detection
- Solution: Ideal diode circuit or accept limitation

### Battery Management - Advanced (BQ24075)

```
U2: BQ24075 (PowerPath)
├── EN1, EN2: Configure input current limit
│   ├── Both GND: 100mA
│   ├── EN1=GND, EN2=Float: 500mA (USB 2.0)
│   └── Both Float: Unlimited (ILIM resistor)
├── ISET: Charge current programming
│   └── R = 890 AΩ / I_charge
├── SYSOFF: Power switch control
├── PGOOD: Power good indicator
└── CHG: Charging indicator LED
```

**Advantages:**
- Dynamic current management
- Powers board while charging
- Battery supplements high current draw
- Proper charge termination

**Charge Current Calculation:**
- Formula: R_ISET = 890 / I_charge(A)
- 250mA: R = 3.56kΩ (use 3.9kΩ → 228mA)
- 500mA: R = 1.78kΩ (use 1.8kΩ → 494mA)

### Power Switching

**Simple Switch:**
```
SW1: SPST switch
├── Between BAT+ and system
└── Must handle full battery current (500mA+)
```

**Advanced (with BQ24075):**
```
SW1: Momentary switch
├── Connected to SYSOFF pin
├── Doesn't carry battery current
└── Smaller footprint possible
```

**No Switch Option:**
- ZMK has very low idle draw (<100µA)
- Battery will last months even "always on"
- Simplifies design

### nRF52840 Module Integration

**Minimum Connections:**
```
Module:
├── VDD: 3.3V (from battery or regulator)
├── GND: Ground
├── SWDIO, SWDCLK: Programming (SWD header)
├── RESET: Reset button + 10kΩ pull-up
├── GPIO: Matrix rows and columns
└── Optional: Battery voltage sense
```

**Decoupling:**
- 100nF ceramic cap close to VDD pin
- 10µF bulk cap on power rail
- Keep traces short

**Programming Header:**
```
SWD 4-pin:
1. VDD (3.3V)
2. SWDIO
3. SWDCLK
4. GND
```

### Voltage Sensing (Battery Level)

**Direct ADC Method:**
```
Battery+ → Voltage divider → nRF52840 ADC pin
├── R1: 1MΩ (top)
├── R2: 1MΩ (bottom)
└── Divides voltage by 2 (4.2V → 2.1V)
```

**Why Voltage Divider:**
- nRF52840 ADC max: 3.6V
- LiPo max: 4.2V
- Divider brings into safe range

**Accuracy Considerations:**
- Use 1% tolerance resistors
- Higher values = lower current draw
- Calibrate in firmware

### LED Underglow (Optional)

**WS2812/SK6812 Support:**
```
LEDs:
├── VDD: 5V (from USB) or 3.7V (battery)
├── GND: Ground
├── DIN: nRF52840 GPIO
└── Power switch: Cut power when off
```

**Power Switching Circuit:**
```
Q1: P-channel MOSFET
├── Source: VDD
├── Drain: LED VDD
├── Gate: nRF52840 GPIO (inverted control)
└── R1: 10kΩ pull-up on gate
```

**Why Power Switch:**
- LEDs draw ~1mA each even when "off"
- 10 LEDs = 10mA = battery drain
- Switch completely cuts power
- Extends battery life significantly

---

## PCB Layout Considerations

### RF Design

**Antenna Placement:**
- Keep at edge of PCB
- No ground plane under antenna
- No traces under antenna
- Clearance: 5mm from metal objects

**Module Placement:**
- Near edge for antenna
- Away from USB connector (noise)
- Central for matrix routing

### Power Distribution

**3.3V Rail:**
- Wide traces (0.8mm+)
- Star topology from regulator
- Decoupling at each IC

**Battery Traces:**
- Handle up to 500mA
- 0.8mm minimum width
- Keep short

### Ground Plane

**Single solid plane:**
- No splits
- Connect with vias
- Avoid under antenna

---

## Firmware Configuration

### ZMK Setup

**Device Tree (.dts):**
```
/ {
    chosen {
        zmk,kscan = &kscan0;
        zmk,battery = &vbatt;
    };

    kscan0: kscan {
        compatible = "zmk,kscan-gpio-matrix";
        diode-direction = "col2row";
        row-gpios = <&gpio0 2 GPIO_ACTIVE_HIGH>,
                    <&gpio0 3 GPIO_ACTIVE_HIGH>;
        col-gpios = <&gpio0 4 (GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)>,
                    <&gpio0 5 (GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)>;
    };

    vbatt: vbatt {
        compatible = "zmk,battery-voltage-divider";
        io-channels = <&adc 0>;
        output-ohms = <1000000>;
        full-ohms = <2000000>;
    };
};
```

### Power Management

**Sleep Settings:**
```
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000  # 15 minutes
```

**Bluetooth:**
```
CONFIG_BT_MAX_CONN=5  # Multiple devices
CONFIG_BT_MAX_PAIRED=5
```

---

## Testing & Validation

### Pre-Assembly Checks

1. **Verify polarity** on all polarized components
2. **Check battery connector** pinout
3. **Measure resistance** between VDD and GND (should be >1MΩ)

### Power-On Testing

1. **Without battery:**
   - Connect USB
   - Measure 5V at USB
   - Measure 3.3V at MCU (if using regulator)

2. **With battery:**
   - Connect battery (check polarity!)
   - Measure battery voltage at MCU
   - Check current draw (<10mA idle)

3. **Charging test:**
   - Connect USB with battery
   - Verify charging LED
   - Measure charging current

### Wireless Testing

1. **Flash firmware** via SWD
2. **Pair with device**
3. **Test matrix** (all keys)
4. **Check battery reporting**
5. **Test sleep/wake**

---

## Common Issues

### Issue: Won't Charge
- Check battery polarity
- Verify charging IC connections
- Test with known-good battery
- Check USB 5V present

### Issue: High Idle Current
- Check for shorts
- Verify sleep mode enabled
- Disconnect LEDs if present
- Check for floating pins

### Issue: Won't Pair
- Verify firmware flashed correctly
- Check antenna placement
- Ensure no metal blocking antenna
- Try different Bluetooth device

### Issue: Short Battery Life
- Check idle current (<100µA expected)
- Disable LEDs or add power switch
- Verify sleep mode working
- Check for battery drain (bad cell)

---

## Bill of Materials (Wireless)

### Minimum Wireless BOM

| Component | Part Number | Qty | Notes |
|-----------|-------------|-----|-------|
| MCU Module | Holyiot 18010 | 1 | nRF52840 |
| Charge IC | TP4056 | 1 | Simple charging |
| USB-C | HRO Type-C-31-M-12 | 1 | Connector |
| ESD Protection | USBLC6-2SC6 | 1 | USB protection |
| Ferrite Beads | 600Ω@100MHz | 2 | EMI filter |
| Polyfuse | 500mA | 1 | Overcurrent |
| Resistors 5.1kΩ | 0805 | 2 | USB-C CC |
| Resistors 1MΩ | 0805 | 2 | Voltage divider |
| Resistors 10kΩ | 0805 | 2 | Pull-ups |
| Capacitors 100nF | 0805 | 5+ | Decoupling |
| Capacitors 10µF | 0805 | 2 | Bulk |
| Diodes 1N4148 | DO-35 | N | One per switch |
| Battery Connector | JST-PH 2.0 | 1 | 2-pin |
| SWD Header | 2.54mm | 1 | 4-pin |

---

## References

- **ZMK Firmware**: https://zmkfirmware.dev/
- **ZMK Power Profiler**: https://zmk.dev/power-profiler
- **ebastler's Guide**: https://github.com/ebastler/zmk-designguide
- **nRF52840 Datasheet**: https://infocenter.nordicsemi.com/
- **marbastlib**: https://github.com/ebastler/marbastlib

---

**Last Updated:** October 20, 2025  
**Version:** 1.0  
**Status:** Advanced wireless keyboard PCB design guide
