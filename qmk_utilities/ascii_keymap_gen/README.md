# Modular QMK Keymap ASCII Generator

Parses QMK `keymap.c` files and generates ASCII-art comment blocks showing the
physical layout of each layer. Layouts are fully data-driven: each supported
keyboard is described by a JSON config in `layouts/` plus a text template in
`templates/`. Adding a new keyboard requires no code changes.

## Usage

```bash
# Print ASCII diagrams for every layer found in a keymap
python modular_keymap_ascii_generator.py path/to/keymap.c

# Write the diagrams into the keymap.c file as comments (creates keymap.c.backup)
python modular_keymap_ascii_generator.py path/to/keymap.c --update

# Skip the backup file
python modular_keymap_ascii_generator.py path/to/keymap.c --update --no-backup

# List all supported keyboards
python modular_keymap_ascii_generator.py --list

# Force a specific layout instead of auto-detection
python modular_keymap_ascii_generator.py path/to/keymap.c --layout lily58

# Show layout-loading details
python modular_keymap_ascii_generator.py path/to/keymap.c --verbose
```

The script can be run from any directory — `layouts/` and `templates/` are
resolved relative to the script file itself.

## Supported keyboards (19)

Key counts are verified against the QMK `keyboard.json` layout definitions.

| Name       | Keys | Layout function(s)                   | Notes                          |
|------------|------|--------------------------------------|--------------------------------|
| 4x2        | 10   | `LAYOUT`                             | Generic 5x2 macropad           |
| alice      | 65   | `LAYOUT_alice`                       | Alice ergo 65-key              |
| corne      | 42   | `LAYOUT_split_3x6_3`                 | CRKBD split 3x6+3              |
| dz60       | 67   | `LAYOUT`                             | DZ60 generic layout            |
| ergodox_ez | 76   | `LAYOUT_ergodox_pretty`              | ErgoDox EZ (pretty order)      |
| iris       | 56   | `LAYOUT`                             | Keebio Iris                    |
| kbd67      | 67   | `LAYOUT_65_ansi_blocker`             | KBD67 65%                      |
| kbd75      | 84   | `LAYOUT_75_ansi`                     | KBD75 75%                      |
| kyria      | 50   | `LAYOUT_split_3x6_5`, `LAYOUT`       | splitkb Kyria                  |
| lets_split | 48   | `LAYOUT_ortho_4x12`                  | Let's Split                    |
| lily58     | 58   | `LAYOUT`                             | Lily58                         |
| minidox    | 36   | `LAYOUT_split_3x5_3`, `LAYOUT`       | MiniDox                        |
| moonlander | 72   | `LAYOUT_moonlander`, `LAYOUT`        | ZSA Moonlander                 |
| ortho75    | 75   | `LAYOUT_ortho_5x15`                  | 5x15 ortholinear               |
| planck     | 48   | `LAYOUT_planck_grid`                 | Planck                         |
| preonic    | 60   | `LAYOUT_preonic_grid`, `LAYOUT_ortho_5x12` | Preonic                  |
| redox      | 70   | `LAYOUT`                             | Redox                          |
| sofle      | 60   | `LAYOUT`                             | Sofle (incl. encoder keys)     |
| tkl        | 87   | `LAYOUT_tkl_ansi`                    | Tenkeyless ANSI                |

## How detection works

1. For each layer (`[_NAME] = LAYOUT_xxx(...)`) the keycodes are parsed with a
   parenthesis-aware splitter, so multi-argument keycodes like
   `LT(_LOWER, KC_SPC)` and `MT(MOD_LSFT, KC_A)` count as one key.
2. The tool matches a layout whose `layout_functions` name appears in the file
   **and** whose `key_count` equals the parsed key count.
3. If no name+count match is found, it falls back to matching by key count
   alone. Use `--layout <name>` to override when counts are ambiguous.

## Adding a new keyboard

1. **Create `layouts/<name>.json`:**

   ```json
   {
     "name": "my_keyboard",
     "description": "My Keyboard - what it is",
     "key_count": 58,
     "layout_functions": ["LAYOUT_my_keyboard"],
     "template_file": "my_keyboard.txt",
     "author": "you",
     "tags": ["split", "ergonomic"]
   }
   ```

   Required fields: `name`, `key_count`, `layout_functions`, `template_file`.
   `key_count` must exactly equal the number of arguments the LAYOUT macro
   takes (check the keyboard's `keyboard.json` / `info.json` in QMK).

2. **Create `templates/<name>.txt`** — a Python `str.format()` template
   producing a C comment block. Use `{layer_name}` for the layer name and
   `{k0:^6}` ... `{kN:^6}` for keys (0-indexed, in LAYOUT argument order,
   center-aligned to 6 chars):

   ```
   /* {layer_name}
    * ,---------------------.
    * |{k0:^6}|{k1:^6}|{k2:^6}|
    * `---------------------'
    */
   ```

   Every index from `k0` to `k{key_count-1}` must appear exactly once.

3. Run `python modular_keymap_ascii_generator.py --list` to confirm it loads,
   then test against your keymap.

## Programmatic use

`qmk_utilities/qmk_format_converter` imports this module:

```python
from modular_keymap_ascii_generator import ModularKeymapParser

parser = ModularKeymapParser()           # loads layouts/ + templates/
config = parser.layouts['lily58']        # LayoutConfig
label = parser.keycode_to_label('KC_ESC')       # 'ESC'
cellt = parser.format_key_for_ascii('KC_A')     # '  A   '
ascii_block = parser.generate_ascii(config, 'QWERTY', keys)  # keys: list[str]
```

## Notes

- All file I/O uses UTF-8 explicitly (safe on Windows).
- `--update` replaces an existing `/* LAYERNAME ... */` comment block if one
  exists, otherwise inserts a new block above the layer definition.
- Keycodes not in the built-in label map are shown as-is (truncated to fit).