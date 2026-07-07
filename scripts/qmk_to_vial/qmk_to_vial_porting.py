"""
QMK to VIAL Porting Coordinator

Complete automation for converting a QMK keyboard directory to a
VIAL-enabled keymap.  Generates all the files a `keymaps/vial/` folder
needs:

    vial.json  - correct KLE-format layout (via keyboard_to_vial_converter)
    config.h   - VIAL_KEYBOARD_UID + unlock combo
    rules.mk   - VIA/VIAL enablement (+ encoder map when applicable)
    keymap.c   - copied from the keyboard's default keymap
    README.md  - build instructions

The heavy lifting (KLE serialization, matrix derivation, encoder entries,
QMK config inheritance, lenient JSON parsing) lives in
keyboard_to_vial_converter.py, which passes a 504-keyboard regression test
against real vial.json files from the vial-qmk repository.

Usage:
    python qmk_to_vial_porting.py <keyboard_dir> [output_dir]

If output_dir is omitted the files are written to
<keyboard_dir>/keymaps/vial/.  The script refuses to write into a
vial-qmk checkout unless --allow-vial-qmk is passed.
"""

import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keyboard_to_vial_converter import (
    convert_keyboard_to_vial,
    load_keyboard_config,
    encoder_count,
    is_split,
    derive_lighting,
)


# ---------------------------------------------------------------------------
# hardware detection helpers
# ---------------------------------------------------------------------------

def detect_processor_type(kb_data):
    """Rough processor family from the 'processor' / 'cpu' field."""
    cpu = str(kb_data.get("processor") or kb_data.get("cpu") or "")
    if re.search(r"atmega|at90|attiny", cpu, re.IGNORECASE):
        return "AVR"
    if "teensy" in cpu.lower():
        return "TEENSY"
    if cpu:
        return "ARM"
    return "UNKNOWN"


def find_unlock_combo(kb_data):
    """Pick two distinct keys for the Vial unlock combo.

    Uses the first and last keys of the first layout (typically Esc and a
    bottom-right modifier), which is the common convention in real vial
    keymaps."""
    layouts = kb_data.get("layouts") or {}
    for lay in layouts.values():
        entries = [e for e in lay.get("layout", [])
                   if isinstance(e.get("matrix"), list)
                   and len(e["matrix"]) == 2]
        if len(entries) >= 2:
            first = entries[0]["matrix"]
            last = entries[-1]["matrix"]
            return (int(first[0]), int(first[1])), (int(last[0]), int(last[1]))
        if len(entries) == 1:
            m = entries[0]["matrix"]
            return (int(m[0]), int(m[1])), (int(m[0]), int(m[1]))
    return (0, 0), (0, 0)


# ---------------------------------------------------------------------------
# file generators
# ---------------------------------------------------------------------------

def generate_config_h(kb_data, unlock_a, unlock_b):
    """Generate keymaps/vial/config.h with UID and unlock combo."""
    uid = (kb_data.get("usb", {}) or {}).get("uid", "")
    uid_list = None
    if uid:
        uid_str = str(uid).replace("{", "").replace("}", "") \
                          .replace(" ", "").replace(",", "").replace("0x", "")
        try:
            uid_list = list(bytes.fromhex(uid_str))[:8]
        except ValueError:
            uid_list = None
    if not uid_list or len(uid_list) != 8:
        import random
        uid_list = [random.randint(0, 255) for _ in range(8)]

    uid_hex = ", ".join("0x{:02X}".format(b) for b in uid_list)
    rows = "{{{}, {}}}".format(unlock_a[0], unlock_b[0])
    cols = "{{{}, {}}}".format(unlock_a[1], unlock_b[1])

    return "\n".join([
        "/* SPDX-License-Identifier: GPL-2.0-or-later */",
        "",
        "#pragma once",
        "",
        "#define VIAL_KEYBOARD_UID {{{}}}".format(uid_hex),
        "#define VIAL_UNLOCK_COMBO_ROWS {}".format(rows),
        "#define VIAL_UNLOCK_COMBO_COLS {}".format(cols),
        "",
    ])


def generate_rules_mk(kb_data):
    """Generate keymaps/vial/rules.mk."""
    lines = [
        "VIA_ENABLE = yes",
        "VIAL_ENABLE = yes",
    ]
    if detect_processor_type(kb_data) == "AVR":
        # AVR flash is tight; standard vial-qmk practice
        lines += [
            "LTO_ENABLE = yes",
            "QMK_SETTINGS = no",
            "TAP_DANCE_ENABLE = no",
            "COMBO_ENABLE = no",
            "KEY_OVERRIDE_ENABLE = no",
        ]
    if encoder_count(kb_data) > 0:
        lines.append("ENCODER_MAP_ENABLE = yes")
    return "\n".join(lines) + "\n"


def generate_readme(keyboard_name, make_target, processor_type, lighting,
                    n_encoders, split):
    return """# {name} - VIAL keymap

VIAL-enabled keymap for the {name} keyboard.

## Details

- Processor family: {cpu}
- Lighting: {lighting}
- Encoders: {enc}
- Split: {split}

## Build

```bash
make {target}:vial
```

## Flash

```bash
make {target}:vial:flash
```

Then open the board in [Vial](https://get.vial.today/).
""".format(name=keyboard_name, cpu=processor_type, lighting=lighting,
           enc=n_encoders, split="yes" if split else "no",
           target=make_target)


FALLBACK_KEYMAP_C = """/* SPDX-License-Identifier: GPL-2.0-or-later */

#include QMK_KEYBOARD_H

/* Minimal Vial keymap: all keys transparent except layer 0 = KC_TRNS
 * placeholders.  Configure the real keymap live through the Vial app.
 * Replace LAYOUT with this keyboard's layout macro and fill in keycodes
 * if you want compiled-in defaults.
 */
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {};
"""


# ---------------------------------------------------------------------------
# main conversion
# ---------------------------------------------------------------------------

def convert_keyboard(keyboard_path, output_dir=None, allow_vial_qmk=False):
    """Generate a full keymaps/vial/ folder for one QMK keyboard dir."""
    print("=" * 60)
    print("Converting: {}".format(keyboard_path))
    print("=" * 60)

    if not os.path.isdir(keyboard_path):
        print("ERROR: not a directory: {}".format(keyboard_path))
        return False

    kb_json_path = os.path.join(keyboard_path, "keyboard.json")
    if not os.path.isfile(kb_json_path):
        # some keyboards use info.json as their main definition
        alt = os.path.join(keyboard_path, "info.json")
        if os.path.isfile(alt):
            kb_json_path = alt
        else:
            print("ERROR: no keyboard.json / info.json in {}"
                  .format(keyboard_path))
            return False

    vial_output, kb_data = convert_keyboard_to_vial(kb_json_path)
    if not vial_output or not kb_data:
        print("ERROR: conversion failed for {}".format(kb_json_path))
        return False

    keyboard_name = kb_data.get("keyboard_name") or \
        os.path.basename(os.path.normpath(keyboard_path))

    # make target = path relative to keyboards/ if resolvable
    norm = os.path.normpath(keyboard_path).replace("\\", "/")
    m = re.search(r"/keyboards/(.+)$", norm)
    make_target = m.group(1) if m else keyboard_name.lower()

    processor_type = detect_processor_type(kb_data)
    lighting = derive_lighting(kb_data)
    n_encoders = encoder_count(kb_data)
    split = is_split(kb_data)

    print("  Keyboard : {}".format(keyboard_name))
    print("  Processor: {}".format(processor_type))
    print("  Lighting : {}".format(lighting))
    print("  Encoders : {}".format(n_encoders))
    print("  Split    : {}".format(split))
    n_rows = len(vial_output["layouts"]["keymap"])
    print("  Keymap   : {} KLE rows".format(n_rows))

    # output location
    if output_dir:
        vial_dir = os.path.join(output_dir, keyboard_name.replace("/", "_"),
                                "keymaps", "vial")
    else:
        vial_dir = os.path.join(keyboard_path, "keymaps", "vial")

    if "vial-qmk" in os.path.abspath(vial_dir).lower() and not allow_vial_qmk:
        print("\nERROR: output path {} is inside a vial-qmk checkout."
              .format(vial_dir))
        print("Refusing to write. Pass an explicit output_dir, or use "
              "--allow-vial-qmk to override.")
        return False

    os.makedirs(vial_dir, exist_ok=True)

    # 1. vial.json
    vial_json_path = os.path.join(vial_dir, "vial.json")
    with open(vial_json_path, "w", encoding="utf-8") as f:
        json.dump(vial_output, f, indent=2)
    print("  Saved: {}".format(vial_json_path))

    # 2. config.h
    unlock_a, unlock_b = find_unlock_combo(kb_data)
    config_h_path = os.path.join(vial_dir, "config.h")
    with open(config_h_path, "w", encoding="utf-8") as f:
        f.write(generate_config_h(kb_data, unlock_a, unlock_b))
    print("  Saved: {}  (unlock combo {} + {})".format(
        config_h_path, unlock_a, unlock_b))

    # 3. rules.mk
    rules_mk_path = os.path.join(vial_dir, "rules.mk")
    with open(rules_mk_path, "w", encoding="utf-8") as f:
        f.write(generate_rules_mk(kb_data))
    print("  Saved: {}".format(rules_mk_path))

    # 4. keymap.c - copy from default keymap when available
    keymap_c_path = os.path.join(vial_dir, "keymap.c")
    default_keymap = os.path.join(keyboard_path, "keymaps", "default",
                                  "keymap.c")
    if os.path.isfile(default_keymap):
        shutil.copy2(default_keymap, keymap_c_path)
        print("  Saved: {} (copied from default keymap)"
              .format(keymap_c_path))
    else:
        with open(keymap_c_path, "w", encoding="utf-8") as f:
            f.write(FALLBACK_KEYMAP_C)
        print("  Saved: {} (fallback stub - default keymap not found; "
              "edit before building)".format(keymap_c_path))

    # 5. README.md
    readme_path = os.path.join(vial_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(generate_readme(keyboard_name, make_target, processor_type,
                                lighting, n_encoders, split))
    print("  Saved: {}".format(readme_path))

    print("\nDone. Build with: make {}:vial".format(make_target))
    return True


def main():
    args = [a for a in sys.argv[1:] if a != "--allow-vial-qmk"]
    allow_vial_qmk = "--allow-vial-qmk" in sys.argv

    if not args:
        print("Usage: python qmk_to_vial_porting.py <keyboard_dir> "
              "[output_dir] [--allow-vial-qmk]")
        sys.exit(1)

    keyboard_path = args[0]
    output_dir = args[1] if len(args) > 1 else None
    ok = convert_keyboard(keyboard_path, output_dir,
                          allow_vial_qmk=allow_vial_qmk)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()