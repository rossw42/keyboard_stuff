# Cyberdeck: Micro Journal Rev 2.1 — Pico-less Modification

## Design Document

**Base project:** [Micro Journal Rev.2.1: cyberDeck](https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-2.1) by unkyulee
**Goal:** Remove the Raspberry Pi Pico (RP2040) from the build and wire the 68-key matrix keyboard PCB directly to the Raspberry Pi Zero 2W, reducing part count and complexity.

---

## 1. Project Overview

The Micro Journal Rev 2.1 is a portable "writerdeck" built around a Raspberry Pi Zero 2W running a custom Linux image, a 7.84" 1280x400 wide LCD, and a 68-key mechanical keyboard. In the stock design, a Raspberry Pi Pico (RP2040) runs QMK/Vial firmware, scans the keyboard matrix, and presents itself to the Pi Zero 2W as a USB HID keyboard through a micro-USB hub.

This project eliminates the Pico entirely. The Pi Zero 2W's own GPIO header will scan the keyboard matrix directly, with a custom Linux userspace driver emitting standard keyboard events. The connection between the keyboard PCB and the Pi will be removable via a commercially available IDC ribbon cable on the Pi's standard 40-pin header.

### Goals

1. **Reduce the number of parts** — remove the Pico, and potentially simplify the USB hub / pigtail cabling that existed only to carry the Pico's USB keyboard connection.
2. **Write the code for the Pi Zero 2W** — a matrix-scanning keyboard driver that runs on the existing `micro-journal-linux` image.
3. **Removable wiring** — keyboard PCB connects to the Pi Zero 2W via a detachable, commercially available connector (2x20 IDC ribbon cable; screw-terminal breakout as alternative).

### Assumptions

- All parts are already on hand; nothing needs to be purchased (except possibly the ribbon cable / header, see §5).
- The stock 68-key keyboard PCB from Elecrow is used unmodified.
- The stock `micro-journal-linux` image is retained and extended (not replaced).

### Accepted Trade-offs

- **Loss of Vial live remapping.** The stock device lets users remap keys graphically with Vial because the Pico runs QMK/Vial firmware. This mod replaces that with **[keyd](https://github.com/rvaiya/keyd)**, a standard Linux key-remapping daemon that provides QMK-like layers, tap/hold overloading, macros, and instant reload — configured via a simple INI file edited with `nano` directly on the device (see §6).
- **Keyboard is not usable during early boot.** The matrix driver starts as a systemd service, so the keyboard becomes live a few seconds into boot (no BIOS/bootloader input). Acceptable for a writing appliance.
- **NKRO behavior depends on the driver**, not QMK. The matrix + per-key diodes still support full NKRO electrically; the driver reports all pressed keys.

---

## 2. Architecture: Original vs. Modified

### Original (stock Rev 2.1)

```
[68-key PCB] --32 wires--> [Pi Pico / RP2040, QMK+Vial firmware]
                                   |
                              USB (HID keyboard)
                                   |
[18650 Battery Shield] --> [Micro USB Hub w/ power input] --> [Pi Zero 2W] --HDMI--> [7.84" LCD]
```

- Pico scans 8x9 matrix + 2 rotary encoders
- Pico appears to the Pi as a plug-and-play USB keyboard
- USB hub needed to combine power input + Pico keyboard + spare port

### Modified (this project)

```
[68-key PCB] --IDC ribbon (removable)--> [Pi Zero 2W 40-pin GPIO header]
                                              |            |
                                        matrix driver    HDMI
                                        (systemd svc)      |
[18650 Battery Shield] --power--> [Pi Zero 2W]        [7.84" LCD]
```

### Parts removed

| Part | Stock role | Why removable |
|------|-----------|---------------|
| Raspberry Pi Pico (RP2040) | Matrix scanning, QMK/Vial firmware, USB HID | Pi Zero 2W GPIO scans the matrix directly |
| 1x Micro USB 2-pin pigtail (Pico power/data leg) | Connect Pico to hub | No Pico |
| Micro USB Hub (potentially) | Combine power + Pico USB + spare port | Only needed now if a spare USB port is still desired (e.g., flash-drive backup feature of micro-journal-linux). **Recommend keeping** if USB backup workflow is used; otherwise removable. |

### Parts retained

- Pi Zero 2W, LCD + HDMI cable, 68-key PCB, 2x EC11 rotary encoders, 18650 battery shield, rocker switch, enclosure hardware.

### Parts added

| Part | Purpose | Example |
|------|---------|---------|
| 2x20 male pin header (if Pi Zero is headerless) | Mate with IDC ribbon | Standard 2.54mm 2x20 header |
| 2x20 (40-pin) IDC ribbon cable, female-female | Removable Pi ↔ keyboard link | Standard Raspberry Pi GPIO ribbon cable, 10–20cm |
| Optional: 40-pin screw terminal breakout ("T-cobbler" style) | Screw-terminal serviceability at the keyboard end | Generic Pi GPIO screw terminal HAT/breakout |

---

## 3. The Keyboard PCB and Matrix

Source: [keyboard firmware config](https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-2.1/keyboard) (`keyboard.json`) and the [build guide wiring table](https://github.com/unkyulee/micro-journal/blob/main/micro-journal-rev-2.1/build.md).

- **68 keys**, wired as an **8-row x 9-column** matrix
- **Diode direction: ROW2COL** (per QMK config) — scanning must **drive columns low one at a time and read rows** (rows configured as inputs with pull-ups; a pressed key reads LOW on its row)
- **2x EC11 rotary encoders** (left + right knobs), each with A/B quadrature outputs plus a push switch. The knob wires land on PCB pins 0–4 (right) and 27–31 (left); the PCB routes the quadrature signals out on pins 22–25.
- The PCB exposes a single-row **32-pin, 2.54mm-pitch header** (pins 0–31)
- Signal count to the controller: **8 rows + 9 cols + 4 encoder A/B + GND = 22 wires**

### Stock PCB pinout (from build.md)

| PCB Pin | Stock connection | Function (derived from keyboard.json) |
|---------|-----------------|----------------------------------------|
| 0–4 | Right knob (Out B, GND, Out A, Switch, Switch GND) | Right encoder harness |
| 5 | Pico GPIO 2 | Row 0 |
| 6 | Pico GPIO 3 | Row 1 |
| 7 | Pico GPIO 4 | Row 2 |
| 8 | Pico GPIO 5 | Row 3 |
| 9 | Pico GPIO 6 | Row 4 |
| 10 | Pico GPIO 7 | Row 5 |
| 11 | Pico GPIO 8 | Row 6 |
| 12 | Pico GPIO 9 | Row 7 |
| 13 | Pico GPIO 10 | Col 0 |
| 14 | Pico GPIO 11 | Col 1 |
| 15 | Pico GPIO 12 | Col 2 |
| 16 | Pico GPIO 13 | Col 3 |
| 17 | Pico GPIO 14 | Col 4 |
| 18 | Pico GPIO 15 | Col 5 |
| 19 | Pico GPIO 16 | Col 6 |
| 20 | Pico GPIO 17 | Col 7 |
| 21 | Pico GPIO 18 | Col 8 |
| 22 | Pico GPIO 19 | Encoder 1 A |
| 23 | Pico GPIO 20 | Encoder 1 B |
| 24 | Pico GPIO 21 | Encoder 2 A |
| 25 | Pico GPIO 22 | Encoder 2 B |
| 26 | Pico GND | Ground |
| 27–31 | Left knob (Out B, GND, Out A, Switch, Switch GND) | Left encoder harness |

> Note: the encoder push switches are wired into the key matrix by the PCB (the 68-key layout includes them), so no extra GPIO is needed for the switches.

---

## 4. New Pin Mapping: Keyboard PCB → Pi Zero 2W

The Pi Zero 2W exposes 26 usable GPIOs (BCM 2–27) on its 40-pin header — enough for the 21 signals + GND. This mapping avoids BCM 2/3 (I2C, fixed 1.8kΩ pull-ups) and BCM 14/15 (UART serial console) to keep those buses free for debugging and future expansion.

| PCB Pin | Signal | Pi BCM GPIO | Pi Physical Pin |
|---------|--------|-------------|-----------------|
| 5 | Row 0 | GPIO 4 | 7 |
| 6 | Row 1 | GPIO 17 | 11 |
| 7 | Row 2 | GPIO 27 | 13 |
| 8 | Row 3 | GPIO 22 | 15 |
| 9 | Row 4 | GPIO 5 | 29 |
| 10 | Row 5 | GPIO 6 | 31 |
| 11 | Row 6 | GPIO 13 | 33 |
| 12 | Row 7 | GPIO 19 | 35 |
| 13 | Col 0 | GPIO 12 | 32 |
| 14 | Col 1 | GPIO 16 | 36 |
| 15 | Col 2 | GPIO 20 | 38 |
| 16 | Col 3 | GPIO 21 | 40 |
| 17 | Col 4 | GPIO 26 | 37 |
| 18 | Col 5 | GPIO 18 | 12 |
| 19 | Col 6 | GPIO 23 | 16 |
| 20 | Col 7 | GPIO 24 | 18 |
| 21 | Col 8 | GPIO 25 | 22 |
| 22 | Encoder 1 A | GPIO 7 | 26 |
| 23 | Encoder 1 B | GPIO 8 | 24 |
| 24 | Encoder 2 A | GPIO 9 | 21 |
| 25 | Encoder 2 B | GPIO 10 | 19 |
| 26 | GND | GND | 6 (or any GND: 9, 14, 20, 25, 30, 34, 39) |

Free for future use: BCM 2, 3 (I2C), 14, 15 (UART), 11.

> Electrical note: rows use the Pi's internal pull-ups; columns are driven push-pull LOW when selected and set to input (Hi-Z) when idle to avoid contention. Currents are microamps — well within GPIO limits.

---

## 5. Connector & Wiring Plan

### Primary: 2x20 IDC ribbon cable (recommended)

1. Solder a standard **2x20 male header** onto the Pi Zero 2W (if not already present).
2. Use a standard **40-pin IDC ribbon cable** (the classic Raspberry Pi GPIO ribbon — cheap, low-profile, fully removable) from the Pi header.
3. At the keyboard end, terminate the required 22 conductors:
   - **Option A (primary):** crimp into single-row 2.54mm Dupont/female housings grouped by function (rows, cols, encoders, GND) that plug directly onto the keyboard PCB's 32-pin header. Label each housing.
   - **Option B (alternative):** terminate the ribbon into a **40-pin screw-terminal breakout board** mounted near the keyboard PCB, then run short labeled jumpers from screw terminals to the PCB header. This gives the screw-terminal serviceability originally desired, at the cost of a little enclosure volume.

### Height/space considerations

- IDC connector stack on the Pi is ~10–12mm — low profile, no significant case impact.
- The ribbon can fold flat inside the enclosure.
- If Option B is used, the screw-terminal breakout is the tallest added part (~15–20mm); position it flat against the case floor.

### Knob wiring

The two EC11 encoders keep their stock wiring to PCB pins 0–4 and 27–31 exactly as in the original build guide. Encoders are retained in this design; whether they're mapped to volume/scroll/etc. is decided later in the keymap file.

---

## 6. Software Design: Matrix Keyboard Driver

### Approach: Python userspace daemon

A Python service scans the matrix over GPIO and injects standard Linux input events via **uinput**, so every console app (WordGrinder, nano, ranger, the launcher) sees an ordinary keyboard. No kernel modules, no firmware, easy to modify on-device.

**Stack:**

- `lgpio` (or `libgpiod` v2 bindings) — fast GPIO access, preinstalled on recent Raspberry Pi OS
- `python-evdev` (`evdev.UInput`) — create the virtual keyboard device
- Runs as root (uinput + gpio access) under systemd

### Scanning algorithm (ROW2COL)

```
setup:
  rows  -> inputs with pull-up
  cols  -> inputs (Hi-Z), idle

loop @ ~500 Hz:
  for each col:
    set col to OUTPUT LOW
    read all 8 rows          # LOW = key pressed at (row, col)
    set col back to INPUT
  debounce each key (5 ms stable-state filter)
  diff against previous state -> emit uinput press/release events
```

- 9 columns x 8 row reads per pass; comfortably fast in Python with lgpio on the Zero 2W's quad-core CPU (a dedicated core is effectively idle).
- Expected worst-case latency ≈ scan period + debounce ≈ 7–10 ms — indistinguishable from a normal keyboard for writing.

### Encoder handling

Two options, documented in order of preference:

1. **Kernel `rotary-encoder` device-tree overlay** — add two `dtoverlay=rotary-encoder,...` lines to `/boot/firmware/config.txt`. The kernel produces `REL_DIAL`/keycode events with proper quadrature decoding at interrupt speed. Zero custom code, immune to Python latency.
2. **In-daemon polling/edge detection** — handle A/B transitions inside the Python daemon via lgpio edge callbacks. Keeps everything in one program and lets encoder actions be defined in the same keymap file.

Start with option 2 for unified config; fall back to option 1 if encoder steps feel skipped.

### Key remapping: split architecture (scan daemon + keyd)

Rather than reinventing layers/remapping inside the scan daemon with a custom JSON format, remapping is delegated to **[keyd](https://github.com/rvaiya/keyd)** — a mature, purpose-built Linux remapping daemon. Responsibilities are split:

1. **Scan daemon (`cyberdeck_kbd.py`)** — translates matrix position → the key's *physical* keycode (what's printed on the keycap) and emits it via uinput. This mapping lives in `/etc/cyberdeck/matrix_layout.json` (an 8x9 grid of `evdev` keycode names, `null` for unused positions, plus encoder actions). It describes the physical PCB and should almost never change after initial bring-up.
2. **keyd** — sits on top of the virtual keyboard device (like any other keyboard) and handles all *user* remapping: layers, tap/hold, macros, swaps.

**Why keyd (evaluated alternatives):**

| Tool | Verdict |
|------|---------|
| **keyd** ✅ | C daemon, <1ms overhead, kernel-level (evdev/uinput) so it works in the console/VT (critical — micro-journal-linux is console-based, no X/Wayland). QMK-like layers, `overload()` tap/hold, macros, unicode. Simple INI config. Instant reload with `sudo keyd reload`. Packaged in Debian (trixie+); trivially built from source on bookworm (`make && make install`, no dependencies). Built-in panic sequence (`backspace+esc+enter`) if a bad config locks you out. |
| kanata / kmonad | Similar feature set, but Rust/Haskell toolchains are heavy to build for armv7/aarch64 and neither is in Debian repos — worse fit for a small appliance image. |
| `loadkeys` / console keymaps | VT-only, arcane format, no layers/tap-hold. Too limited. |
| udev hwdb scancode remaps | Static scancode→keycode only; no layers. Too limited. |
| xmodmap / xkb | Requires X — not present on this device. |
| Custom JSON in the daemon (original plan) | Would poorly reimplement what keyd already does well. Kept only for the *physical* matrix map, which is genuinely device-specific. |

**Example `/etc/keyd/default.conf`:**

```ini
[ids]
*

[main]
# tap = esc, hold = ctrl
capslock = overload(control, esc)

# fn key activates the fn layer while held
rightalt = layer(fn)

[fn]
1 = f1
2 = f2
h = left
j = down
k = up
l = right
```

- **Remapping on the device:** `nano /etc/keyd/default.conf`, then `sudo keyd reload` — instant, no PC, no flashing, no service restart.
- `keyd monitor` shows key names live, making it easy to discover what to remap.
- The default `matrix_layout.json` will be transcribed from the stock Vial keymap in the [keyboard/keymaps folder](https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-2.1/keyboard) so the device behaves identically out of the box, with keyd's config initially empty (pass-through).
- Since keyd matches all keyboards by default, a temporary USB keyboard plugged in for recovery is also remapped consistently — a feature, not a bug.

### Deliverables (code to write)

| File | Purpose |
|------|---------|
| `cyberdeck_kbd.py` | Matrix scan + debounce + uinput emission + encoder decode + physical layout loader |
| `matrix_layout.json` | Physical matrix map (position → keycode) matching the stock Rev 2.1 layout |
| `default.conf` (keyd) | Starter keyd config (pass-through + example fn layer), installed to `/etc/keyd/` |
| `cyberdeck-kbd.service` | systemd unit (start early in boot, restart on failure) |
| `install.sh` | Copies files, installs deps (incl. building/installing keyd), enables services |
| `matrix_test.py` | Diagnostic: prints (row, col) of pressed keys — first thing to run after wiring |

### systemd unit sketch

```ini
[Unit]
Description=Cyberdeck matrix keyboard driver
DefaultDependencies=no
After=local-fs.target
Before=getty.target

[Service]
ExecStart=/usr/bin/python3 /opt/cyberdeck/cyberdeck_kbd.py
Restart=always
Nice=-10

[Install]
WantedBy=sysinit.target
```

---

## 7. Extending micro-journal-linux

The [micro-journal-linux](https://github.com/unkyulee/micro-journal-linux) image is Raspberry Pi OS Lite plus documented setup scripts (ranger launcher, WordGrinder, file browser, boot-speed tweaks). Nothing about it assumes a USB keyboard specifically — it just consumes normal Linux input events. That means the extension is purely additive:

1. Flash the stock prebuilt micro-journal-linux image as usual.
2. First boot with a temporary USB keyboard (or SSH over Wi-Fi, or pre-seed via the SD card's boot partition).
3. Run `install.sh`:
   - `apt install python3-lgpio python3-evdev` (or pip equivalents)
   - install **keyd**: `apt install keyd` if the image base is Debian trixie or newer; otherwise build from source (`git clone https://github.com/rvaiya/keyd && make && sudo make install` — no dependencies beyond a C compiler) and `systemctl enable keyd --now`
   - copy `cyberdeck_kbd.py` + `matrix_layout.json` to `/opt/cyberdeck/` and `/etc/cyberdeck/`, and the starter `default.conf` to `/etc/keyd/`
   - install + enable `cyberdeck-kbd.service`
   - (if using kernel encoder overlays) append `dtoverlay=rotary-encoder,...` lines to `config.txt`
4. Reboot — the launcher comes up and the matrix keyboard just works, because to ranger/WordGrinder it's a normal keyboard.

No changes to unkyulee's scripts or launcher are needed. Document the steps so the mod can be reapplied after any image update.

---

## 8. Risks & Open Items

| Risk / Question | Mitigation |
|-----------------|------------|
| Python scan latency/jitter under load | Zero 2W is quad-core; pin the daemon at `Nice=-10`. If needed, rewrite hot loop in C or use `libgpiod` bulk reads. |
| Encoder steps skipped by polling | Use kernel `rotary-encoder` overlay (interrupt-driven) instead. |
| PCB pin numbering vs. silkscreen | Verify with `matrix_test.py` and a multimeter before final crimping; the build.md table is authoritative but should be confirmed against the physical PCB. |
| Keyboard dead if daemon crashes | `Restart=always`; keep SSH enabled as recovery path. |
| Bad keyd config locks out input | keyd's built-in panic sequence (`backspace+esc+enter`) terminates it; SSH remains as backup. |
| keyd not packaged for the image's Debian base | Build from source in `install.sh` (single C binary, no deps); packaged in Debian trixie+ if the image is rebased. |
| No keyboard during boot menus | Non-issue for this appliance; SSH covers recovery. |
| USB flash-drive backup feature needs a USB port | Keep the micro USB hub (or use the Pi's remaining micro-USB OTG port with an adapter). Decide during build. |
| GPIO conflicts with future HATs | Mapping in §4 deliberately leaves I2C, UART, and BCM 11 free. |

---

## 9. Long-Term Goal: Folding Case (Rev 8 Style)

The [Micro Journal Rev.8 "Melodica"](https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-8) uses a clamshell/folding enclosure where the display folds over the keyboard. Longer term, this project aims to redesign the Rev 2.1 case in that style.

Notes for that phase:

- Rev 2.1's Fusion 360 source file is included in its [STL folder](https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-2.1/STL), so the case is modifiable rather than from-scratch.
- The Pico-less electronics of this mod *help* the folding redesign: fewer boards and cables to package, and the ribbon cable tolerates hinge-adjacent routing better than 22 loose wires.
- Key challenges: hinge design for the 7.84" LCD's weight, HDMI + display power routing through/near the hinge, and keeping the 18650 shield low in the base for balance.
- Treat as a separate design document once the electronics mod is proven.

**Status: prototype v0.1 exists** — see `archive/case_v1/case_design.md` (design doc) and
`archive/case_v1/cyberdeck_case.scad` (parametric OpenSCAD model). Highlights:

- Full-cover clamshell like Rev 8's final design: 324 × 170 mm footprint, ~52 mm closed; flat 0° keyboard deck.
- Dimensions derived from the upstream Rev 2.1 STLs (measured with `archive/case_v1/measure_stl.py`): keyboard plates 314.4 × 104.6 mm, base redesigned around them.
- **Rev 8-style single-barrel hinge (v0.3, pinless):** the lid's rear edge is a continuous Ø22 roll that snap-fits into C-cradle segments on the base — same construction as the Rev 8 display enclosure. 60 mm center gap in the barrel for the HDMI + display-power cables. Interference-checked over the full 0–110° sweep (`archive/case_v1/interference_check.scad`).
- Rev 8 aesthetic package: 12 mm rounded corners, parametric face→side edge treatment (`edge_style` = "round" or "chamfer", size via `bev_lid`/`bev_base`), flat mating seam, front thumb scoop.
- Base & lid each split into 3 pieces (216 mm middle + 54 mm wings) for a 220 mm bed, Rev 8 style; bezel splits in 2. Ten print STLs exported to `archive/case_v1/stl/`.
- Pi Zero 2W + 18650 shield in a rear bay under the hinge (balance); panel + MIPI-HDMI driver in the lid; EC11 knobs move to top-mount on the rear strip (side wheels don't survive the fold).
- Open items (bench-verify before final print) are tracked in `archive/case_v1/case_design.md` §6.

---

## 10. References

| Resource | Link |
|----------|------|
| Micro Journal Rev 2.1 (main page) | https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-2.1 |
| Rev 2.1 Build Guide + BOM (wiring table) | https://github.com/unkyulee/micro-journal/blob/main/micro-journal-rev-2.1/build.md |
| Rev 2.1 User/Quick Start Guide | https://github.com/unkyulee/micro-journal/blob/main/micro-journal-rev-2.1/guide.md |
| 68-key keyboard firmware (QMK/Vial config, `keyboard.json`) | https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-2.1/keyboard |
| 68-key Keyboard PCB (Elecrow) | https://www.elecrow.com/micro-journal-diy-kit-68-keys-keyboard-pcb.html |
| micro-journal-linux (OS image + setup scripts) | https://github.com/unkyulee/micro-journal-linux |
| Micro Journal Rev 8 (folding case inspiration) | https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-8 |
| Rev 2.1 STL / Fusion 360 design files | https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-2.1/STL |