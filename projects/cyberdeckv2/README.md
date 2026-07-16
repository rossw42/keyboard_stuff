# Cyberdeck v2

A **Micro Journal Rev 8 "Melodica"** clamshell case running **Pico-less Raspberry Pi Zero 2W** electronics, modified to fit the **7.84" Wisecoco 400×1280 bar display**.

> Built on unkyulee's [Micro Journal Rev 8](https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-8) — the authentic Rev 8 aesthetic, hinge, and joint geometry is used directly. Only 3 of the 17 printed parts differ from stock.

---

![Cyberdeck v2 open](renders/full_open_front.png)

---

## What it is

- **Case:** stock Rev 8 STLs for the base, hood, and hinge — the proven clamshell design. The lid's 3-piece front frame is modified to swap the stock 5" display for the 7.84" ultrawide bar panel.
- **Electronics:** Pi Zero 2W scans the 68-key matrix directly over GPIO (no Pico, no USB hub). Keyd handles remapping; the launcher and WordGrinder run unchanged on micro-journal-linux.
- **Keyboard:** same 68-key Elecrow PCB and 2× EC11 encoders as the Rev 2.1 stock build.

---

## Quick start

1. **Parts** — see [`bom_v2.md`](bom_v2.md). Likely purchases: M3×70 screws, B-7000 glue, Costar 6.25u stab, possibly a slim HDMI cable. Everything else is on hand from the Rev 2.1 kit.
2. **Before printing** — measure your actual Wisecoco panel and MIPI→HDMI driver board, then verify dimensions match `cyberdeckv2.scad` (`pan_w`, `pan_h`, `pan_t`). Re-export the three `panel_*.stl` if different — the frame pocket has only ~0.5–0.9 mm clearance to the screw rows.
3. **Print** — everything in [`stl/`](stl/) (17 build files). PETG or ABS for the hinge parts.
4. **Build & bring-up** — follow [`BUILDGUIDE.md`](BUILDGUIDE.md) phase by phase. Don't skip the `matrix_test.py` verification before crimping the final harness.

---

## Files at a glance

| File / Folder | Purpose |
|---|---|
| [`BUILDGUIDE.md`](BUILDGUIDE.md) | Step-by-step build guide + checkbox checklist (8 phases, ~50 items) |
| [`bom_v2.md`](bom_v2.md) | Full bill of materials with purchase links |
| [`design_v2.md`](design_v2.md) | Case design — what's modified and why, panel mod diagram |
| [`design.md`](design.md) | Pico-less electronics architecture + canonical GPIO pin map |
| [`cyberdeckv2.scad`](cyberdeckv2.scad) | Parametric lid mod source. Use `part="full_assembly"` + `open_angle=-100` to visualize |
| [`stl/`](stl/) | Complete print set (17 parts to print; 3 source STLs for SCAD) |
| [`src/`](src/) | Pico-less firmware — matrix scan daemon, install script, keyd config |
| [`renders/`](renders/) | Assembly previews: open, closed, lid detail |
| [`archive/case_v1/`](archive/case_v1/) | v1 from-scratch parametric case (preserved for reference) |

---

## The modification in one picture

```
Rev 8 lid frame (322 × 98.7 mm):

  screw row y=31.2  →  |  o        o          o          o    |
                        |  +--------------------------------+  |
  new aperture          |  |      7.84" ACTIVE AREA         |  |
  centered at y = -6    |  +--------------------------------+  |
  screw row y=-43.5 →  |  o        o          o          o    |
```

The stock 5" aperture in `Display Panel Middle.stl` is filled; a new 207.4 × 66.2 mm aperture + 214.2 × 72.5 mm back-pocket are cut across all three frame pieces. All 6 original frame screws are preserved.

---

## Firmware quick-reference

```sh
# Install (run once on the Pi)
sudo bash src/install.sh

# Wiring diagnostic — press every key, confirm (row, col)
sudo systemctl stop cyberdeck-kbd
sudo python3 /opt/cyberdeck/matrix_test.py

# Remap keys (apply instantly)
sudo nano /etc/keyd/default.conf
sudo keyd reload

# Logs
journalctl -u cyberdeck-kbd -e
```

See [`src/README.md`](src/README.md) for the full usage reference.

---

## Credits

- Case design: [unkyulee/micro-journal Rev 8](https://github.com/unkyulee/micro-journal) (CC / open-source)
- Electronics mod, firmware, lid modification: this project