
# Cyberdeck v2 — Build Guide & Checklist

Combined step-by-step guide from parts to working device.
Work **top to bottom**; don't skip ahead.

Companion docs:
- `bom_v2.md` — parts list + purchase links
- `design.md` — electronics architecture + §4 GPIO pin map (canonical)
- `design_v2.md` — what's modified in the case and why
- `src/README.md` — firmware usage + day-to-day commands

> **Golden rules:** never lose both keyboard AND SSH at the same time. Verify
> with `matrix_test.py` before every permanent wiring step. `design.md §4`
> pin table is canonical.

---

## Phase 0 — Before Touching Anything

### Software prep (Pi over SSH)
- [ ] Flash micro-journal-linux to the SD card (stock prebuilt image).
- [ ] Enable SSH + Wi-Fi; verify you can log in. Until the GPIO keyboard works, SSH is your only input.
- [ ] Prepare a backup recovery path: USB keyboard + micro-USB OTG adapter on hand and tested.
- [ ] Back up the SD card image and photograph the current wiring so stock state can be restored if the mod stalls.
- [ ] Over SSH, check the Debian base: `cat /etc/os-release` — determines whether `install.sh` uses apt keyd (trixie+) or builds from source.
- [ ] Verify deps: `sudo apt install python3-lgpio python3-evdev` — ensure no errors.
- [ ] Copy `src/` to the Pi and run `sudo bash install.sh`. Then `sudo systemctl stop cyberdeck-kbd` so the service doesn't interfere during testing.

### Print prep (before printing final parts)
- [ ] Measure the actual **Wisecoco 7.84" panel** (outline W×H×T, active area, which edge the ribbon exits). Compare against `cyberdeckv2.scad` defaults (`pan_w=213.6, pan_h=71.9, pan_t=2.9`). Adjust + re-export the three `panel_*.stl` if different — the pocket clears the frame screw rows by only ~0.5–0.9 mm.
- [ ] Measure the **MIPI→HDMI driver board**. If it's ≤ 8 mm thick, it lives in the lid; otherwise it goes in the base hood. Decide before printing.

---

## Phase 1 — Print & Prep Parts

- [ ] Print all 17 build files from `stl/` — see `bom_v2.md §1` for orientation notes. PETG/ABS for hinge parts.
  - `panel_left.stl`, `panel_middle.stl`, `panel_right.stl` (modified lid frame, face down)
  - `Display Enclosure Left/Middle/Right.stl` (lid back shell + hinge roll)
  - `Display Wire Cap.stl`
  - `Enclosure Left/Middle/Right.stl` + `Enclosure Lid.stl` (base)
  - `Hood Top/Bottom/Left/Right.stl`
  - `keyboard plate space.stl`, `keyboard plate arrow.stl`
- [ ] Dry-fit the **three base pieces** (Enclosure L/M/R) zig-zag joints — snug; deburr if needed.
- [ ] Dry-fit the **three frame pieces** (panel L/M/R) with the actual 7.84" panel in the pocket before any glue. Panel should drop in with ~0.3 mm play, active area centered. If it binds → STOP and adjust `cyberdeckv2.scad`.
- [ ] Heat-set **M3 inserts** into base bosses, **M2 inserts** into display-frame bosses.
- [ ] Bond base pieces with B-7000 + clamp square. Tie with **M3×70** through the cross-holes.
- [ ] Bond frame pieces with B-7000 (flat surface, cure fully). Do NOT pre-glue before the dry-fit passes above.

---

## Phase 2 — Base: Keyboard

- [ ] Install switches into `keyboard plate space` + `keyboard plate arrow`; solder to the 68-key PCB. Costar 6.25u stab on the spacebar.
- [ ] Wire both **EC11 encoders** to PCB pins 0–4 / 27–31 per design.md §3 table.
- [ ] Mount the plate assembly into the base with **M3×5** screws.
- [ ] **Photograph the keyboard PCB header up close.** The build.md pin table (PCB pins 0–31) needs bench verification; silkscreen numbering direction is the most common wiring mistake.
- [ ] **Confirm pin 0 vs pin 31 orientation with a multimeter:** continuity from a known switch's pads to the expected row/col header pin (design.md §3 table).
- [ ] **Do not crimp the Pi harness yet** — bring-up first (Phase 4).

---

## Phase 3 — Base: Electronics (under the rear hood)

- [ ] Mount the **18650 shield low and central** in the rear bay (counterweights the lid; keep as low as possible).
- [ ] Mount the **Pi Zero 2W** beside it (M2 screws or carrier). Solder 2×20 header if not already present.
- [ ] Route rocker switch into the hood opening; wire: shield output → switch → Pi 5V/GND.
- [ ] Route the keyboard 22-wire bundle from the PCB header through the base's keyboard-area opening into the bay toward the Pi — **leave unterminated for now**.
- [ ] Assemble the hood (`Hood Bottom/Left/Right/Top`) loosely — you'll open it several times.

---

## Phase 4 — Wiring & Firmware Bring-up

> Do this before closing the case. Work through each step; don't move on until it passes.

### 4a. 4-wire smoke test
- [ ] Connect only **Row 0** (PCB pin 5 → Pi BCM 4), **Col 0** (PCB pin 13 → BCM 12), and **GND** (PCB pin 26). Run `sudo python3 /opt/cyberdeck/matrix_test.py` and confirm **Esc registers at [0,0]**. This validates the full concept in 10 minutes.

### 4b. Full temporary wiring
- [ ] Wire all 22 conductors with temporary Dupont jumpers per the **design.md §4 pin table** (rows→BCM 4/17/27/22/5/6/13/19, cols→12/16/20/21/26/18/23/24/25, encoders→7/8/9/10). Do NOT crimp the final harness yet.
- [ ] **Full matrix pass with `matrix_test.py`:** press every one of the 71 key positions; confirm each reports the expected (row, col). Fix any mismatch in wiring or `/etc/cyberdeck/matrix_layout.json` before continuing.
- [ ] If phantom/wrong keys appear: shorted or swapped row/col wire — the PCB has per-key diodes, so ghosting = wiring fault, not code.
- [ ] **Encoder raw test:** rotate both knobs; confirm A/B transitions print. Press both knob buttons — matrix keys [7,6] (Space) and [7,7] (Enter).
- [ ] **Check for SPI0 conflict:** if the encoder test fails with GPIO-busy errors, verify `dtparam=spi=on` is NOT in `/boot/firmware/config.txt`.

### 4c. Driver & keyd
- [ ] `sudo systemctl start cyberdeck-kbd` — type in the console; all keys should work like a normal keyboard.
- [ ] Console layout check: if letters come out wrong, check `/etc/default/keyboard` first — the driver emits US-layout physical codes.
- [ ] `sudo keyd monitor` — keypresses shown; typing behaves identically to stock.
- [ ] **fn layer:** hold fn key (emits `f13`) + number row → F1–F12; fn + hjkl → arrows.
- [ ] Know the escape hatches: bad keyd config → `backspace+esc+enter`; driver issues → `journalctl -u cyberdeck-kbd -e`.

### 4d. Encoders
- [ ] Rotate left knob → Left/Right arrows emit.
- [ ] Rotate right knob → Up/Down arrows emit.
- [ ] If steps skip or feel laggy: switch to the kernel `rotary-encoder` DT overlay (design.md §6, option 1).

### 4e. Permanent harness
- [ ] Identify ribbon conductor 1 (red stripe) and map to physical pin 1 (zigzag odd/even — use the *physical pin* column in design.md §4, not BCM).
- [ ] Crimp keyboard-end Dupont housings grouped by function (rows / cols / encoders / GND); label each housing.
- [ ] **Re-run full `matrix_test.py` pass** on the finished harness — every key + both encoders again.

---

## Phase 5 — Lid Assembly

- [ ] Seat the 7.84" panel in the pocket with a strip of **thin foam tape** on the back — removes the ~0.1 mm float and preloads it against the 1 mm front lip. No glue on the panel.
- [ ] If the driver board lives in the lid: stick it to the Display Enclosure interior (foam tape), connect the MIPI ribbon to the panel, attach the HDMI cable — leave ~15 cm of slack toward the hinge side. If it lives in the base: connect only the MIPI ribbon and route it toward the hinge.
- [ ] Screw the **Display Enclosure L/M/R** onto the frame with **M2×5** screws into the frame's inserts. The shell clamps the panel pocket shut.

---

## Phase 6 — Hinge & Cable Routing

- [ ] Mate the lid's hinge roll with the base's hinge features per the stock Rev 8 assembly. The long **M3×70** screws through the barrel serve as hinge pins.
- [ ] Route **HDMI (or MIPI) + display 5V/GND** through the hinge channel: at ~90° open, leave a gentle service loop so the cable flexes around the roll rather than kinking. Open and close the lid fully several times; watch the cable.
- [ ] Snap/screw the **Display Wire Cap** over the hinge channel.
- [ ] Verify the lid: opens smoothly, holds position (friction from the barrel/screw fit), closes flush, nothing pinches.

---

## Phase 7 — Display & Boot Integration

- [ ] Connect the HDMI cable from the driver board to the Pi's mini-HDMI port.
- [ ] Confirm the panel lights up; check `/boot/firmware/config.txt` has the right timing for 400×1280 (portrait panel — rotate in config if needed).
- [ ] **Reboot end-to-end:** keyboard live at/before the launcher, display up, battery runtime sanity check.
- [ ] If the launcher appears before the keyboard: service ordering issue — check `journalctl -u cyberdeck-kbd -b`, not the wiring.
- [ ] `systemctl is-enabled cyberdeck-kbd keyd` → both `enabled`.
- [ ] Power sanity: with the Pico + its hub leg gone, confirm solid 5V from the battery shield. Watch for brownout indicators under load.
- [ ] USB hub decision: keep only if you use the flash-drive backup workflow; otherwise remove.
- [ ] Latency feel-check while typing under load: if laggy, see design.md §8 escalation path.

---

## Phase 8 — Wrap-up

- [ ] Dress all cables, tighten the hood M3×5 screws.
- [ ] **Re-run `install.sh`** once everything works to confirm the overlay is reproducible (must preserve your edited configs as `*.new`).
- [ ] Back up the final SD image (working modded state).
- [ ] Update `design.md` with anything learned on the bench (PCB pinout confirmation, encoder choice, driver board placement, hub decision).

---

## Quick Troubleshooting

| Symptom | Check |
|---|---|
| Whole row/column of keys dead | that row/col wire at the Pi header (design.md §4 map) |
| One key dead | switch solder joint on the PCB |
| Encoder skips/reverses | swap cw/ccw in `/etc/cyberdeck/matrix_layout.json`; or kernel overlay |
| Driver crash-loops, GPIO busy | `dtparam=spi=on` set? Disable it (encoder pins 7–10 are SPI0) |
| No display | HDMI timing in config.txt; driver board power; ribbon seating |
| Lid won't hold angle | hinge screw tension (M3×70), or add friction washer |
| Panel rattles | thicker foam shim behind the panel |
| Keys work in `matrix_test.py` but not in the driver | check `systemctl status cyberdeck-kbd`; check keyd is running |
| Wrong characters typed | `/etc/default/keyboard` console layout; driver emits US physical codes |
</content>
</invoke>