#!/usr/bin/env python3
"""
test_driver_sim.py — Host-side simulation tests for cyberdeck_kbd.py.

Runs on any machine (no Pi/GPIO/uinput needed) by injecting fake `lgpio`
and `evdev` modules. Verifies:
  * layout loading + keycode resolution against the real matrix_layout.json
  * ROW2COL scan behavior (col driven LOW, pressed row reads LOW)
  * 5 ms stable-state debounce
  * duplicate-keycode refcounting (spacebar vs knob-push KEY_SPACE)
  * encoder quadrature decode (one tap per 4 valid transitions, both dirs)

Usage: python test_driver_sim.py
"""

import json
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Fake lgpio
# ---------------------------------------------------------------------------
class FakeLgpio(types.ModuleType):
    SET_PULL_UP = 32

    def __init__(self):
        super().__init__("lgpio")
        self.mode = {}          # pin -> "in" | "out"
        self.out_level = {}     # pin -> level driven when output
        self.pressed = set()    # set of (row_pin, col_pin) closed switches
        self.enc_level = {}     # pin -> level for encoder input pins
        self._selected_col = None

    def gpiochip_open(self, n):
        return 100 + n

    def gpiochip_close(self, h):
        pass

    def gpio_claim_input(self, h, pin, flags=0):
        self.mode[pin] = "in"
        if pin == self._selected_col:
            self._selected_col = None
        return 0

    def gpio_claim_output(self, h, pin, level=0):
        self.mode[pin] = "out"
        self.out_level[pin] = level
        if level == 0:
            self._selected_col = pin
        return 0

    def gpio_read(self, h, pin):
        # Encoder pins: return the set level (default 1, pulled up)
        if pin in self.enc_level:
            return self.enc_level[pin]
        # Row pins: LOW if a pressed switch connects this row to the
        # currently-driven-LOW column.
        if self._selected_col is not None:
            if (pin, self._selected_col) in self.pressed:
                return 0
        return 1

    def gpio_write(self, h, pin, level):
        self.out_level[pin] = level

    def gpio_free(self, h, pin):
        self.mode.pop(pin, None)


# ---------------------------------------------------------------------------
# Fake evdev
# ---------------------------------------------------------------------------
KEYNAME_TO_CODE = {}


def _build_keycodes():
    # Minimal-but-real evdev keycode table for names used in the layout.
    # Values copied from linux/input-event-codes.h.
    table = {
        "KEY_ESC": 1, "KEY_1": 2, "KEY_2": 3, "KEY_3": 4, "KEY_4": 5,
        "KEY_5": 6, "KEY_6": 7, "KEY_7": 8, "KEY_8": 9, "KEY_9": 10,
        "KEY_0": 11, "KEY_MINUS": 12, "KEY_EQUAL": 13, "KEY_BACKSPACE": 14,
        "KEY_TAB": 15, "KEY_Q": 16, "KEY_W": 17, "KEY_E": 18, "KEY_R": 19,
        "KEY_T": 20, "KEY_Y": 21, "KEY_U": 22, "KEY_I": 23, "KEY_O": 24,
        "KEY_P": 25, "KEY_LEFTBRACE": 26, "KEY_RIGHTBRACE": 27,
        "KEY_ENTER": 28, "KEY_LEFTCTRL": 29, "KEY_A": 30, "KEY_S": 31,
        "KEY_D": 32, "KEY_F": 33, "KEY_G": 34, "KEY_H": 35, "KEY_J": 36,
        "KEY_K": 37, "KEY_L": 38, "KEY_SEMICOLON": 39, "KEY_APOSTROPHE": 40,
        "KEY_GRAVE": 41, "KEY_LEFTSHIFT": 42, "KEY_BACKSLASH": 43,
        "KEY_Z": 44, "KEY_X": 45, "KEY_C": 46, "KEY_V": 47, "KEY_B": 48,
        "KEY_N": 49, "KEY_M": 50, "KEY_COMMA": 51, "KEY_DOT": 52,
        "KEY_SLASH": 53, "KEY_RIGHTSHIFT": 54, "KEY_LEFTALT": 56,
        "KEY_SPACE": 57, "KEY_CAPSLOCK": 58, "KEY_HOME": 102, "KEY_UP": 103,
        "KEY_PAGEUP": 104, "KEY_LEFT": 105, "KEY_RIGHT": 106, "KEY_END": 107,
        "KEY_DOWN": 108, "KEY_PAGEDOWN": 109, "KEY_DELETE": 111,
        "KEY_RIGHTALT": 100, "KEY_LEFTMETA": 125, "KEY_F13": 183,
    }
    KEYNAME_TO_CODE.update(table)
    return table


class FakeUInput:
    instances = []

    def __init__(self, caps, name=None, vendor=None, product=None, version=None):
        self.caps = caps
        self.name = name
        self.events = []  # (code, value)
        FakeUInput.instances.append(self)

    def write(self, etype, code, value):
        self.events.append((code, value))

    def syn(self):
        pass

    def close(self):
        pass


def install_fakes():
    fake_lgpio = FakeLgpio()
    sys.modules["lgpio"] = fake_lgpio

    fake_evdev = types.ModuleType("evdev")
    ecodes_mod = types.SimpleNamespace()
    ecodes_mod.ecodes = _build_keycodes()
    ecodes_mod.EV_KEY = 1
    fake_evdev.UInput = FakeUInput
    fake_evdev.ecodes = ecodes_mod
    sys.modules["evdev"] = fake_evdev
    return fake_lgpio


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def main():
    fake = install_fakes()
    sys.path.insert(0, HERE)
    import cyberdeck_kbd as drv

    # Force loading the repo copy of the layout.
    drv.LAYOUT_PATHS[:] = [os.path.join(HERE, "matrix_layout.json")]

    failures = []

    def check(name, cond, detail=""):
        status = "PASS" if cond else "FAIL"
        print(f"[{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
        if not cond:
            failures.append(name)

    # --- Test 1: layout loads and resolves ---
    cfg = drv.load_layout()
    check("layout: 8 rows x 9 cols", len(cfg["rows"]) == 8 and len(cfg["cols"]) == 9)
    nkeys = sum(1 for row in cfg["codes"] for c in row if c is not None)
    check("layout: 71 matrix positions (66 keys + MO + 2 knob pushes + 2 dup)",
          nkeys == 71, f"got {nkeys}")
    check("layout: 2 encoders", len(cfg["encoders"]) == 2)

    with open(os.path.join(HERE, "matrix_layout.json")) as f:
        raw = json.load(f)
    unique = {k for row in raw["keymap"] for k in row if k}
    check("layout: all keycode names resolved", all(k in KEYNAME_TO_CODE for k in unique),
          f"missing: {[k for k in unique if k not in KEYNAME_TO_CODE]}")

    # --- Test 2: scan + debounce ---
    chip = 100
    scanner = drv.MatrixScanner(chip, cfg)
    row_pin = cfg["rows"][0]        # matrix [0,0] = KEY_ESC
    col_pin = cfg["cols"][0]
    esc = KEYNAME_TO_CODE["KEY_ESC"]

    t = 0.0
    ev = scanner.scan(t)
    check("scan: idle matrix emits nothing", ev == [])

    fake.pressed.add((row_pin, col_pin))
    ev = scanner.scan(t + 0.002)            # raw change registered
    check("debounce: no event immediately on press", ev == [])
    ev = scanner.scan(t + 0.004)            # 2 ms stable — still under 5 ms
    check("debounce: no event before 5 ms", ev == [])
    ev = scanner.scan(t + 0.010)            # 8 ms stable — fires
    check("debounce: press event after 5 ms stable", ev == [(esc, 1)], f"got {ev}")
    ev = scanner.scan(t + 0.012)
    check("scan: no repeat while held", ev == [])

    fake.pressed.discard((row_pin, col_pin))
    scanner.scan(t + 0.014)
    ev = scanner.scan(t + 0.021)
    check("debounce: release event after 5 ms stable", ev == [(esc, 0)], f"got {ev}")

    # Columns must be back to Hi-Z after a scan pass.
    check("scan: all columns idle Hi-Z after pass",
          all(fake.mode.get(p) == "in" for p in cfg["cols"]))

    # --- Test 3: duplicate-keycode refcounting ---
    refs = drv.KeycodeRefCount()
    space = KEYNAME_TO_CODE["KEY_SPACE"]
    check("refcount: first press emits", refs.press(space) is True)
    check("refcount: second press (knob) suppressed", refs.press(space) is False)
    check("refcount: first release suppressed", refs.release(space) is False)
    check("refcount: last release emits", refs.release(space) is True)
    # tap while another instance held
    refs2 = drv.KeycodeRefCount()
    refs2.press(space)                       # spacebar held
    check("refcount: tap press while held suppressed", refs2.press(space) is False)
    check("refcount: tap release while held suppressed", refs2.release(space) is False)
    check("refcount: spacebar release still emits", refs2.release(space) is True)

    # --- Test 4: encoder quadrature ---
    spec = {
        "pin_a": 7, "pin_b": 8,
        "cw": KEYNAME_TO_CODE["KEY_RIGHT"], "ccw": KEYNAME_TO_CODE["KEY_LEFT"],
        "steps_per_detent": 4,
    }
    fake.enc_level[7] = 1
    fake.enc_level[8] = 1
    enc = drv.Encoder(chip, spec)

    def step(a, b):
        fake.enc_level[7] = a
        fake.enc_level[8] = b
        return enc.poll()

    # Driver convention: "cw" = B-leads-A gray sequence 11 -> 10 -> 00 -> 01 -> 11.
    # (Physical direction depends on encoder wiring; if reversed on the bench,
    # swap the cw/ccw keycodes in matrix_layout.json.)
    taps = [step(1, 0), step(0, 0), step(0, 1), step(1, 1)]
    check("encoder: CW detent emits exactly one tap at completion",
          taps[:3] == [None, None, None] and taps[3] == spec["cw"], f"got {taps}")

    # Opposite (A-leads-B) sequence 11 -> 01 -> 00 -> 10 -> 11 : one ccw detent
    taps = [step(0, 1), step(0, 0), step(1, 0), step(1, 1)]
    check("encoder: CCW detent emits exactly one tap at completion",
          taps[:3] == [None, None, None] and taps[3] == spec["ccw"], f"got {taps}")

    # Bounce: A jitters without B moving — invalid half-transitions must not
    # accumulate a full detent.
    taps = [step(0, 1), step(1, 1), step(0, 1), step(1, 1)]
    check("encoder: bounce does not emit", all(t is None for t in taps), f"got {taps}")

    # --- Test 5: uinput capability set ---
    ui = drv.make_uinput(cfg)
    all_codes = {c for row in cfg["codes"] for c in row if c is not None}
    for e in cfg["encoders"]:
        all_codes |= {e["cw"], e["ccw"]}
    check("uinput: capabilities cover every emittable keycode",
          set(ui.caps[1]) == all_codes)

    print()
    if failures:
        print(f"{len(failures)} FAILURE(S): {failures}")
        sys.exit(1)
    print("All tests passed.")


if __name__ == "__main__":
    main()