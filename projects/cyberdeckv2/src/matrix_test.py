#!/usr/bin/env python3
"""
matrix_test.py — Wiring diagnostic for the Cyberdeck keyboard matrix.

FIRST TOOL TO RUN AFTER WIRING. Prints the (row, col) of every key press
and release so you can verify the PCB-pin -> Pi GPIO wiring against the
design.md section 4 table before final crimping.

Also polls the two EC11 encoders and prints their raw quadrature steps.

Run over SSH as root:  sudo python3 matrix_test.py
Stop with Ctrl-C.

Uses the same pins/layout file as the real driver (matrix_layout.json in
/etc/cyberdeck/ or alongside this script), so a clean pass here means the
driver will see the same thing.
"""

import json
import os
import sys
import time

import lgpio

LAYOUT_PATHS = [
    "/etc/cyberdeck/matrix_layout.json",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "matrix_layout.json"),
]


def load_layout():
    for path in LAYOUT_PATHS:
        if os.path.isfile(path):
            with open(path, "r") as f:
                layout = json.load(f)
            print(f"using layout file: {path}")
            return layout
    sys.exit(f"matrix_layout.json not found in {LAYOUT_PATHS}")


def main():
    layout = load_layout()
    rows = layout["pins"]["rows"]
    cols = layout["pins"]["cols"]
    keymap = layout.get("keymap", [])
    encoders = layout.get("encoders", [])

    chip = lgpio.gpiochip_open(layout["pins"].get("gpiochip", 0))

    for pin in rows:
        lgpio.gpio_claim_input(chip, pin, lgpio.SET_PULL_UP)
    for pin in cols:
        lgpio.gpio_claim_input(chip, pin)  # idle Hi-Z

    enc_state = {}
    for enc in encoders:
        lgpio.gpio_claim_input(chip, enc["pin_a"], lgpio.SET_PULL_UP)
        lgpio.gpio_claim_input(chip, enc["pin_b"], lgpio.SET_PULL_UP)
        a = lgpio.gpio_read(chip, enc["pin_a"])
        b = lgpio.gpio_read(chip, enc["pin_b"])
        enc_state[enc["name"]] = (a << 1) | b

    n_rows, n_cols = len(rows), len(cols)
    state = [[False] * n_cols for _ in range(n_rows)]

    print(f"matrix: {n_rows} rows x {n_cols} cols  "
          f"(rows on BCM {rows}, cols on BCM {cols})")
    print("press keys to see (row, col); Ctrl-C to quit\n")

    try:
        while True:
            for c, col_pin in enumerate(cols):
                lgpio.gpio_claim_output(chip, col_pin, 0)   # drive LOW
                for r, row_pin in enumerate(rows):
                    pressed = lgpio.gpio_read(chip, row_pin) == 0
                    if pressed != state[r][c]:
                        state[r][c] = pressed
                        name = None
                        try:
                            name = keymap[r][c]
                        except (IndexError, TypeError):
                            pass
                        label = f"  expected: {name}" if name else ""
                        action = "PRESS  " if pressed else "release"
                        print(f"{action} [row {r}, col {c}]  "
                              f"(row BCM {row_pin}, col BCM {col_pin}){label}")
                lgpio.gpio_claim_input(chip, col_pin)        # back to Hi-Z

            for enc in encoders:
                a = lgpio.gpio_read(chip, enc["pin_a"])
                b = lgpio.gpio_read(chip, enc["pin_b"])
                new = (a << 1) | b
                if new != enc_state[enc["name"]]:
                    print(f"encoder {enc['name']}: AB {enc_state[enc['name']]:02b} -> {new:02b}")
                    enc_state[enc["name"]] = new

            time.sleep(0.002)  # ~500 Hz
    except KeyboardInterrupt:
        print("\ndone")
    finally:
        lgpio.gpiochip_close(chip)


if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("run as root: sudo python3 matrix_test.py")
    main()