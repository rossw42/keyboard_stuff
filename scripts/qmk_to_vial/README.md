# QMK to VIAL Porting Script

Converts a QMK keyboard directory into a VIAL-enabled keymap folder —
generates `vial.json`, `config.h`, `rules.mk`, `keymap.c`, and a README.

For how it works internally, see [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md).

---

## Quick Start

```bash
python qmk_to_vial_porting.py "<keyboard_dir>" "<output_dir>"
```

Example:

```bash
python qmk_to_vial_porting.py "D:\GitHub2\vial-qmk\keyboards\eggsworks\tamago" "output"
```

Output:

```
output\eggsworks_tamago\keymaps\vial\
├── vial.json     # Vial layout definition
├── config.h      # Vial UID + unlock combo
├── rules.mk      # VIA/VIAL build flags
├── keymap.c      # copied from the keyboard's default keymap
└── README.md     # build instructions
```

---

## Usage Options

```bash
# Write into the keyboard directory itself (creates keymaps/vial/)
python qmk_to_vial_porting.py "path\to\my_keyboard"

# Write to a separate output directory (recommended)
python qmk_to_vial_porting.py "path\to\my_keyboard" "path\to\output"

# The script refuses to write inside a vial-qmk checkout.
# Override only if you really mean it:
python qmk_to_vial_porting.py "...\vial-qmk\keyboards\foo" --allow-vial-qmk
```

Generate just a vial.json (printed to stdout):

```bash
python keyboard_to_vial_converter.py "path\to\keyboard.json"
```

---

## Using the Output

1. Copy the generated `keymaps\vial\` folder into the keyboard's directory
   in your vial-qmk tree (back up any existing `keymaps\vial\` first).
2. Build and flash:

```bash
make <keyboard>:vial          # e.g. make eggsworks/tamago:vial
make <keyboard>:vial:flash
```

3. Open the board in [Vial](https://get.vial.today/).

---

## Notes

- Works with keyboards that use `keyboard.json` or `info.json`, including
  multi-level configs (parent/child directories), split keyboards, and
  rotary encoders.
- If the keyboard has no `keymaps/default/keymap.c`, a stub `keymap.c` is
  created — edit it before building.
- Validated against 504 real keyboards from the vial-qmk repository
  (100% pass). Details in [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md).

---

*Last Updated: July 2026*