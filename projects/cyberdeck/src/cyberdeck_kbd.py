#!/usr/bin/env python3
"""
cyberdeck_kbd.py — Matrix keyboard driver for the Cyberdeck
(Micro Journal Rev 2.1, Pico-less mod).

Scans the 68-key 8x9 matrix (ROW2COL) directly on the Pi Zero 2W's GPIO,
debounces keys, decodes the two EC11 rotary encoders, and emits standard
Linux input events through a uinput virtual keyboard.

Physical layout comes from /etc/cyberdeck/matrix_layout.json.
User remapping (layers, tap/hold, macros) is handled by keyd on top of
this device — do NOT add remapping logic here.

Reload layout: send SIGHUP (kill -HUP <pid>) or restart the service.

Must run as root (needs /dev/uinput and /dev/gpiochip0).
"""

import json
import os
import signal
import sys
import time

import lgpio
from evdev import UInput, ecodes

LAYOUT_PATHS = [
    "/etc/cyberdeck/matrix_layout.json",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "matrix_layout.json"),
]

UINPUT_NAME = "cyberdeck-kbd"
UINPUT_VENDOR = 0x1209   # pid.codes open-source VID (unregistered use)
UINPUT_PRODUCT = 0xCD68  # "CyberDeck 68"


def log(msg):
    print(msg, flush=True)


def load_layout():
    """Load and validate matrix_layout.json from the first path that exists."""
    for path in LAYOUT_PATHS:
        if os.path.isfile(path):
            with open(path, "r") as f:
                layout = json.load(f)
            log(f"[cyberdeck-kbd] loaded layout: {path}")
            break
    else:
        raise FileNotFoundError(f"matrix_layout.json not found in {LAYOUT_PATHS}")

    rows = layout["pins"]["rows"]
    cols = layout["pins"]["cols"]
    keymap = layout["keymap"]
    if len(keymap) != len(rows):
        raise ValueError(f"keymap has {len(keymap)} rows, expected {len(rows)}")
    for r, row in enumerate(keymap):
        if len(row) != len(cols):
            raise ValueError(f"keymap row {r} has {len(row)} cols, expected {len(cols)}")

    # Resolve keycode names -> integers once, up front.
    codes = [[None] * len(cols) for _ in rows]
    for r, row in enumerate(keymap):
        for c, name in enumerate(row):
            if name is None:
                continue
            code = ecodes.ecodes.get(name)
            if code is None:
                raise ValueError(f"unknown keycode {name!r} at [{r},{c}]")
            codes[r][c] = code

    encoders = []
    for enc in layout.get("encoders", []):
        encoders.append({
            "name": enc.get("name", "encoder"),
            "pin_a": enc["pin_a"],
            "pin_b": enc["pin_b"],
            "cw": ecodes.ecodes[enc["cw"]],
            "ccw": ecodes.ecodes[enc["ccw"]],
            "steps_per_detent": enc.get("steps_per_detent", 4),
        })

    return {
        "gpiochip": layout["pins"].get("gpiochip", 0),
        "rows": rows,
        "cols": cols,
        "codes": codes,
        "encoders": encoders,
        "rate_hz": layout.get("scan", {}).get("rate_hz", 500),
        "debounce_ms": layout.get("scan", {}).get("debounce_ms", 5),
    }


def make_uinput(cfg):
    """Create the virtual keyboard with exactly the keycodes we can emit."""
    keys = set()
    for row in cfg["codes"]:
        for code in row:
            if code is not None:
                keys.add(code)
    for enc in cfg["encoders"]:
        keys.add(enc["cw"])
        keys.add(enc["ccw"])
    caps = {ecodes.EV_KEY: sorted(keys)}
    return UInput(caps, name=UINPUT_NAME,
                  vendor=UINPUT_VENDOR, product=UINPUT_PRODUCT, version=1)


class Encoder:
    """Quadrature decoder using a state-transition table.

    Accumulates valid transitions and emits one keystroke per detent
    (typically 4 transitions). Invalid transitions (bounce/skips) are ignored.
    """

    # transition table: (prev_state << 2) | new_state -> -1, 0, +1
    _TRANS = {
        0b0001: +1, 0b0111: +1, 0b1110: +1, 0b1000: +1,
        0b0010: -1, 0b1011: -1, 0b1101: -1, 0b0100: -1,
    }

    def __init__(self, chip, spec):
        self.chip = chip
        self.pin_a = spec["pin_a"]
        self.pin_b = spec["pin_b"]
        self.cw = spec["cw"]
        self.ccw = spec["ccw"]
        self.per_detent = spec["steps_per_detent"]
        self.accum = 0
        lgpio.gpio_claim_input(chip, self.pin_a, lgpio.SET_PULL_UP)
        lgpio.gpio_claim_input(chip, self.pin_b, lgpio.SET_PULL_UP)
        self.state = self._read()

    def _read(self):
        a = lgpio.gpio_read(self.chip, self.pin_a)
        b = lgpio.gpio_read(self.chip, self.pin_b)
        return (a << 1) | b

    def poll(self):
        """Returns a keycode to tap (cw/ccw) or None."""
        new = self._read()
        if new == self.state:
            return None
        step = self._TRANS.get((self.state << 2) | new, 0)
        self.state = new
        self.accum += step
        if self.accum >= self.per_detent:
            self.accum = 0
            return self.cw
        if self.accum <= -self.per_detent:
            self.accum = 0
            return self.ccw
        return None


class MatrixScanner:
    """ROW2COL scan: drive one column LOW at a time, read rows (pull-ups).

    Columns idle as inputs (Hi-Z) to avoid pin contention; each is claimed
    as a push-pull LOW output only while selected.
    """

    def __init__(self, chip, cfg):
        self.chip = chip
        self.rows = cfg["rows"]
        self.cols = cfg["cols"]
        self.codes = cfg["codes"]
        n_keys = len(self.rows) * len(self.cols)
        self.raw = [False] * n_keys        # instantaneous reading
        self.stable = [False] * n_keys     # debounced state
        self.changed_at = [0.0] * n_keys   # when raw last changed
        self.debounce_s = cfg["debounce_ms"] / 1000.0

        for pin in self.rows:
            lgpio.gpio_claim_input(chip, pin, lgpio.SET_PULL_UP)
        for pin in self.cols:
            lgpio.gpio_claim_input(chip, pin)  # idle Hi-Z

    def scan(self, now):
        """One full matrix pass. Returns list of (keycode, value) events."""
        events = []
        idx = 0
        for c, col_pin in enumerate(self.cols):
            lgpio.gpio_claim_output(self.chip, col_pin, 0)  # drive LOW
            for r, row_pin in enumerate(self.rows):
                pressed = lgpio.gpio_read(self.chip, row_pin) == 0
                i = r * len(self.cols) + c
                if pressed != self.raw[i]:
                    self.raw[i] = pressed
                    self.changed_at[i] = now
                elif (pressed != self.stable[i]
                      and (now - self.changed_at[i]) >= self.debounce_s):
                    self.stable[i] = pressed
                    code = self.codes[r][c]
                    if code is not None:
                        events.append((code, 1 if pressed else 0))
                idx += 1
            lgpio.gpio_claim_input(self.chip, col_pin)  # back to Hi-Z
        return events


def main():
    cfg = load_layout()

    reload_requested = {"flag": False}
    running = {"flag": True}

    def on_hup(signum, frame):
        reload_requested["flag"] = True

    def on_term(signum, frame):
        running["flag"] = False

    signal.signal(signal.SIGHUP, on_hup)
    signal.signal(signal.SIGTERM, on_term)
    signal.signal(signal.SIGINT, on_term)

    while running["flag"]:
        chip = lgpio.gpiochip_open(cfg["gpiochip"])
        ui = make_uinput(cfg)
        scanner = MatrixScanner(chip, cfg)
        encoders = [Encoder(chip, spec) for spec in cfg["encoders"]]
        period = 1.0 / cfg["rate_hz"]
        log(f"[cyberdeck-kbd] scanning {len(cfg['rows'])}x{len(cfg['cols'])} "
            f"matrix @ {cfg['rate_hz']} Hz, debounce {cfg['debounce_ms']} ms, "
            f"{len(encoders)} encoder(s)")

        try:
            while running["flag"] and not reload_requested["flag"]:
                t0 = time.monotonic()

                dirty = False
                for code, value in scanner.scan(t0):
                    ui.write(ecodes.EV_KEY, code, value)
                    dirty = True

                for enc in encoders:
                    tap = enc.poll()
                    if tap is not None:
                        ui.write(ecodes.EV_KEY, tap, 1)
                        ui.write(ecodes.EV_KEY, tap, 0)
                        dirty = True

                if dirty:
                    ui.syn()

                elapsed = time.monotonic() - t0
                if elapsed < period:
                    time.sleep(period - elapsed)
        finally:
            ui.close()
            lgpio.gpiochip_close(chip)

        if reload_requested["flag"]:
            reload_requested["flag"] = False
            log("[cyberdeck-kbd] SIGHUP: reloading layout")
            cfg = load_layout()

    log("[cyberdeck-kbd] exiting")


if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("cyberdeck_kbd.py must run as root (uinput + GPIO access)")
    main()