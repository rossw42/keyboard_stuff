# Cyberdeck Build Checklist — Micro Journal Rev 2.1 (Pico-less Mod)

Pre-flight and bring-up checklist. Work top to bottom; don't skip ahead.
Companion docs: [`design.md`](./design.md) (architecture + pin map) · [`bom.md`](./bom.md) (parts) · [`src/README.md`](./src/README.md) (software usage).

---

## Phase 0 — Before Touching Hardware

- [ ] **Flash micro-journal-linux** to the SD card (stock prebuilt image).
- [ ] **Enable SSH + Wi-Fi and verify you can log in.** Until the GPIO keyboard works, SSH is your only input. Do this *before* removing the Pico.
- [ ] **Prepare a second recovery path:** USB keyboard + micro-USB OTG adapter on hand and tested.
- [ ] **Snapshot the working stock device:** back up the SD card image; photograph the current wiring so the stock Pico setup can be restored if the mod stalls.
- [ ] **Check the image's Debian base:** `cat /etc/os-release` over SSH — determines whether `install.sh` gets keyd from apt (trixie+) or builds from source.
- [ ] **Verify deps install cleanly:** `sudo apt install python3-lgpio python3-evdev` on the device.
- [ ] **Photograph the keyboard PCB header up close.** The build.md pin table (PCB pins 0–31) is not bench-verified; silkscreen numbering direction is the most likely wiring mistake.
- [ ] **Confirm pin 0 vs pin 31 orientation with a multimeter:** continuity from a known switch's pads to its expected row/col header pin (design.md §3 table).

## Phase 1 — Wiring (temporary first)

- [ ] **Copy `src/` to the Pi and run `sudo bash install.sh`** (installs driver, keyd, services). Then `sudo systemctl stop cyberdeck-kbd` for testing.
- [ ] **4-wire smoke test:** connect only Row 0 (PCB pin 5 → BCM 4), Col 0 (PCB pin 13 → BCM 12), and GND (PCB pin 26). Run `sudo python3 /opt/cyberdeck/matrix_test.py` and confirm **Esc registers at [0,0]**. This validates the whole concept in 10 minutes.
- [ ] **Wire all 22 conductors with temporary Dupont jumpers** per the design.md §4 pin table — do NOT crimp the final harness yet.
- [ ] **Full matrix pass with `matrix_test.py`:** press every one of the 71 key positions; confirm each reports the expected (row, col) and keycode label.
- [ ] **If phantom/wrong keys appear:** suspect a shorted or swapped row/col wire (the PCB has per-key diodes, so ghosting = wiring fault, not code).
- [ ] **Encoder raw test:** rotate both knobs in `matrix_test.py`; confirm A/B transitions print for each. Press both knob buttons — they are matrix keys [7,6] (Space) and [7,7] (Enter).
- [ ] **Fix any mismatches** in wiring or `/etc/cyberdeck/matrix_layout.json` *before* proceeding.

## Phase 2 — Permanent Harness (IDC ribbon)

- [ ] **Solder the 2x20 header** onto the Pi Zero 2W (skip if Zero 2 WH).
- [ ] **Identify ribbon conductor 1** (red stripe) and map it to physical pin 1. IDC connectors map conductors to header pins in a zigzag odd/even pattern — verify against the *physical pin* column in design.md §4, not the BCM column.
- [ ] **Crimp the keyboard-end Dupont housings** grouped by function (rows / cols / encoders / GND); label each housing (heat-shrink or labels from BOM A5).
- [ ] **Re-run the full `matrix_test.py` pass** on the finished harness — every key + both encoders again.

## Phase 3 — Driver & keyd

- [ ] **Start the driver:** `sudo systemctl start cyberdeck-kbd` — type in the console; all keys should work like a normal keyboard.
- [ ] **Console keymap sanity:** if letters come out wrong, check `/etc/default/keyboard` (console layout layer) before blaming the driver — the daemon emits US-layout physical codes.
- [ ] **keyd pass-through:** `sudo keyd monitor` shows keypresses; typing behaves identically to stock.
- [ ] **fn layer:** hold the stock fn key (emits `f13`) + number row → F1–F12; fn + hjkl → arrows.
- [ ] **Know the escape hatches:** bad keyd config → press `backspace+esc+enter` to kill keyd; driver issues → SSH in and `journalctl -u cyberdeck-kbd -e`.

## Phase 4 — Encoders (driver-level)

- [ ] **Rotate left knob:** Left/Right arrows emit (stock behavior).
- [ ] **Rotate right knob:** Up/Down arrows emit.
- [ ] **If steps skip or feel laggy:** switch to the kernel `rotary-encoder` device-tree overlay (design.md §6, option 1).

## Phase 5 — Boot Integration & Power

- [ ] **Reboot:** keyboard is live at/before the launcher. If the launcher appears first, that's service ordering — check `journalctl -u cyberdeck-kbd -b`, not the wiring.
- [ ] **Services enabled:** `systemctl is-enabled cyberdeck-kbd keyd` → both `enabled`.
- [ ] **Power sanity:** with the Pico + its hub leg gone, confirm solid 5V from the battery shield path. Watch for brownout indicators (rainbow square / lightning bolt on display) under load.
- [ ] **USB hub decision:** keep it only if you use the flash-drive backup workflow; otherwise remove (BOM §1 item 11).
- [ ] **Latency feel-check while typing under load** (e.g., during a file sync): if laggy, see design.md §8 escalation (libgpiod bulk reads / C hot loop) — don't silently accept lag.

## Phase 6 — Wrap-up

- [ ] **Re-run `install.sh`** once everything works to confirm the overlay is reproducible (it must preserve your edited configs as `*.new` handling).
- [ ] **Back up the final SD image** (working modded state).
- [ ] **Update `design.md`** with anything learned on the bench (actual PCB pinout confirmation, encoder choice, hub decision).
- [ ] **Only now** consider starting the Rev-8-style folding case design (separate document, per project rules).

---

**Golden rules:** never lose both keyboard *and* SSH at the same time; verify with `matrix_test.py` before every permanent step; design.md §4 pin table is canonical.