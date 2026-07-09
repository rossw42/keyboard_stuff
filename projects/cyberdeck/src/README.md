# Cyberdeck Keyboard Driver — Source

Code for the Micro Journal Rev 2.1 **Pico-less mod**: the Pi Zero 2W scans
the 68-key matrix directly. See [`../design.md`](../design.md) for the full
design (architecture, pin mapping, connector plan).

## Files

| File | Deploys to | Purpose |
|------|-----------|---------|
| `cyberdeck_kbd.py` | `/opt/cyberdeck/` | Matrix scan + debounce + encoder decode + uinput virtual keyboard |
| `matrix_layout.json` | `/etc/cyberdeck/` | Physical matrix map (position → evdev keycode) + GPIO pins + encoders |
| `keyd/default.conf` | `/etc/keyd/` | User remapping: layers, tap/hold, macros (keyd) |
| `cyberdeck-kbd.service` | `/etc/systemd/system/` | Early-boot systemd unit, `Restart=always` |
| `install.sh` | — | One-shot installer/overlay for a stock micro-journal-linux image |
| `matrix_test.py` | `/opt/cyberdeck/` | Wiring diagnostic — prints (row, col) of pressed keys |

## Architecture

```
keys/knobs -> GPIO -> cyberdeck_kbd.py (physical keycodes) -> uinput
                                                        "cyberdeck-kbd" device
                                                                |
                                                              keyd  (layers/remaps)
                                                                |
                                                     console apps (WordGrinder, nano, ...)
```

- The scan daemon knows **only** the physical layout (`matrix_layout.json`).
  It should rarely change after bring-up.
- All *user* remapping lives in `/etc/keyd/default.conf`; apply with
  `sudo keyd reload` — instant, no service restart.
- The stock MO(1)/fn key (matrix `[7,1]`) is emitted as `f13`; keyd binds
  `f13 = layer(fn)`.

## Install (on the device)

```sh
# copy this src/ folder to the Pi, then:
sudo bash install.sh
```

Purely additive — never touches unkyulee's scripts/launcher. Safe to re-run
after any micro-journal-linux image update (existing configs are preserved;
new versions land as `*.new`).

## Bring-up / testing order

1. **Wiring:** wire per the `design.md` §4 pin table (verify against the
   physical PCB with a multimeter — don't trust silkscreen blindly).
2. **`matrix_test.py`:** `sudo systemctl stop cyberdeck-kbd && sudo python3 /opt/cyberdeck/matrix_test.py`
   — press every key, confirm each reports the expected `(row, col)` and
   keycode. Fix wiring/`matrix_layout.json` mismatches *before* final crimping.
3. **Driver:** `sudo systemctl start cyberdeck-kbd` — type in the console.
4. **keyd pass-through:** confirm `sudo keyd monitor` shows your keys; try the
   fn layer (`f13` + number row = F-keys).
5. **Encoders:** rotate both knobs — arrow keys should emit (stock behavior:
   left knob = Left/Right, right knob = Up/Down). If steps skip, switch to the
   kernel `rotary-encoder` overlay (design.md §6).
6. **Boot integration:** reboot; keyboard should be live before the launcher.

## Day-to-day

| Task | Command |
|------|---------|
| Remap keys / add layers | `sudo nano /etc/keyd/default.conf && sudo keyd reload` |
| See live key names | `sudo keyd monitor` |
| keyd panic kill (bad config) | press `backspace+esc+enter` together |
| Edit physical layout | `sudo nano /etc/cyberdeck/matrix_layout.json && sudo systemctl reload cyberdeck-kbd` |
| Driver logs | `journalctl -u cyberdeck-kbd -e` |

## Notes

- `matrix_layout.json` was transcribed from the stock Vial keymap
  (layer 0 of `keymaps/vial/keymap.c`, cross-referenced with
  `keyboard.json` matrix positions) — the device types identically to stock
  out of the box. `KC_NUHS` → `KEY_BACKSLASH`; encoder push switches are
  matrix keys `[7,6]` (Space) and `[7,7]` (Enter).
- The uinput device reports vendor `0x1209` / product `0xCD68`; keyd's `*`
  wildcard matches it (keyd ignores only its own virtual device).
- Everything runs as root (uinput + gpiochip access). SSH stays enabled as
  the recovery path.