# QMK Keymap ASCII Generator

A modular collection of utilities for working with QMK (Quantum Mechanical Keyboard) firmware, focused on generating ASCII art representations of keyboard layouts from keymap.c files.

## What This Does

Converts QMK keymap.c files into readable ASCII art representations like this:

```
/* QWERTY
 * ,-----------------------------------------.                    ,-----------------------------------------.
 * | ESC  |  Q   |  W   |  E   |  R   |  T   |                    |  Y   |  U   |  I   |  O   |  P   |  `   |
 * |------+------+------+------+------+------|                    |------+------+------+------+------+------|
 * | Tab  |  A   |  S   |  D   |  F   |  G   |                    |  H   |  J   |  K   |  L   |  ;   |  '   |
 * |------+------+------+------+------+------|                    |------+------+------+------+------+------|
 * |LShift|  Z   |  X   |  C   |  V   |  B   |-------.    ,-------|  N   |  M   |  ,   |  .   |  /   |RShift|
 * |------+------+------+------+------+------|  [    |    |  ]    |------+------+------+------+------+------|
 * |LCTRL | LAlt | LGUI |ADJUST|LOWER |Space |-------|    |-------|Space |RAISE | Left | Down |  Up  |Right |
 * `-----------------------------------------/       /     \      \-----------------------------------------'
 *                   | LAlt | LGUI |LOWER | /Space  /       \Enter  \ |RAISE |BackSP| RGUI |
 *                   |      |      |      |/       /         \      \ |      |      |      |
 *                   `----------------------------'           '------''--------------------'
 */
```

## Features

- **18 Keyboards Supported**: Comprehensive support for popular split, ortholinear, traditional, and ergonomic keyboards
- **Smart Detection**: Automatically identifies your keyboard from the keymap file
- **Easy Extension**: Add new keyboards with simple JSON configuration files
- **QMK Integration**: Converts QMK keycodes to readable labels
- **Safe Updates**: Creates backups when modifying files
- **Modular Architecture**: Easily add support for new keyboards
- **External Configuration**: Layouts defined in JSON files with separate template files
- **Smart Parsing**: Filters out ASCII art comments and decorations
- **Auto-Detection**: Identifies keyboard layout based on LAYOUT function and key count

## Usage

### Basic Usage
```bash
# Generate ASCII for supported keyboards
python3 modular_keymap_ascii_generator.py keymap.c

# Update keymap file with generated ASCII comments
python3 modular_keymap_ascii_generator.py keymap.c --update

# List all supported keyboard layouts
python3 modular_keymap_ascii_generator.py --list

# Force use of specific layout
python3 modular_keymap_ascii_generator.py keymap.c --layout lily58
```

## Supported Keyboards

Currently supports 18 keyboard layouts organized by category:

### Split Ergonomic Keyboards
- **Alice** (65 keys) - Ergonomic staggered layout with split spacebar
- **Corne/CRKBD** (37 keys) - Compact 3x6+3 split keyboard
- **Ergodox EZ** (76 keys) - Split ergonomic keyboard with thumb clusters
- **Iris** (54 keys) - Split ergonomic with function row
- **Kyria** (50 keys) - Split ergonomic with encoder support
- **Let's Split** (48 keys) - Simple 4x12 split ortholinear
- **Lily58** (58 keys) - Split ergonomic with encoders
- **Minidox** (36 keys) - Compact 36-key split keyboard
- **Moonlander** (72 keys) - ZSA Moonlander premium split ergonomic
- **Redox** (70 keys) - Split ergonomic with thumb clusters
- **Sofle** (58 keys) - Split ergonomic with OLED and encoders

### Ortholinear Keyboards
- **Planck** (48 keys) - 4x12 ortholinear grid layout
- **Preonic** (60 keys) - 5x12 ortholinear with function row
- **Ortho75** (75 keys) - 5x15 ortholinear layout

### Traditional Keyboards
- **DZ60** (61 keys) - 60% mechanical keyboard
- **KBD67** (67 keys) - 65% layout with arrow keys
- **KBD75** (82 keys) - 75% compact layout
- **TKL** (87 keys) - Tenkeyless layout

## Adding New Keyboard Layouts

To add support for a new keyboard, create two files:

### 1. Layout Configuration (layouts/keyboard_name.json)

```json
{
  "name": "keyboard_name",
  "description": "Brief description of the keyboard",
  "key_count": 42,
  "layout_functions": ["LAYOUT_function_name"],
  "template_file": "keyboard_name.txt",
  "author": "Your Name",
  "tags": ["split", "compact", "ergonomic"]
}
```

**Required fields:**
- `name`: Unique identifier for the keyboard
- `key_count`: Total number of keys in the layout
- `layout_functions`: Array of QMK LAYOUT function names (e.g., `["LAYOUT_split_3x6_3"]`)
- `template_file`: Name of the template file in templates/ directory

**Optional fields:**
- `description`: Human-readable description
- `author`: Creator of the layout configuration
- `tags`: Array of descriptive tags

### 2. ASCII Template (templates/keyboard_name.txt)

Create an ASCII art template using Python string formatting:

```
/* {layer_name}
 * ,-----------------------------------------.
 * |{k0:^6}|{k1:^6}|{k2:^6}|{k3:^6}|{k4:^6}|{k5:^6}|
 * |------+------+------+------+------+------|
 * |{k6:^6}|{k7:^6}|{k8:^6}|{k9:^6}|{k10:^6}|{k11:^6}|
 * `-----------------------------------------'
 */
```

**Template guidelines:**
- Use `{layer_name}` for the layer name placeholder
- Use `{k0}`, `{k1}`, etc. for key positions (0-indexed)
- Use `{k0:^6}` to center-align keys in 6-character width
- Follow the physical layout of your keyboard
- Include ASCII art borders and decorations as needed

### 3. Example: Adding a new 40% keyboard

**layouts/forty_percent.json:**
```json
{
  "name": "forty_percent",
  "description": "Standard 40% keyboard layout",
  "key_count": 48,
  "layout_functions": ["LAYOUT_planck_grid"],
  "template_file": "forty_percent.txt",
  "author": "Community",
  "tags": ["40%", "compact", "ortholinear"]
}
```

**templates/forty_percent.txt:**
```
/* {layer_name}
 * ,------------------------------------------------------------------------------------.
 * | {k0:^4} | {k1:^4} | {k2:^4} | {k3:^4} | {k4:^4} | {k5:^4} | {k6:^4} | {k7:^4} | {k8:^4} | {k9:^4} | {k10:^4} | {k11:^4} |
 * |------+------+------+------+------+------+------+------+------+------+------+------|
 * | {k12:^4} | {k13:^4} | {k14:^4} | {k15:^4} | {k16:^4} | {k17:^4} | {k18:^4} | {k19:^4} | {k20:^4} | {k21:^4} | {k22:^4} | {k23:^4} |
 * |------+------+------+------+------+------+------+------+------+------+------+------|
 * | {k24:^4} | {k25:^4} | {k26:^4} | {k27:^4} | {k28:^4} | {k29:^4} | {k30:^4} | {k31:^4} | {k32:^4} | {k33:^4} | {k34:^4} | {k35:^4} |
 * |------+------+------+------+------+------+------+------+------+------+------+------|
 * | {k36:^4} | {k37:^4} | {k38:^4} | {k39:^4} | {k40:^4} | {k41:^4} | {k42:^4} | {k43:^4} | {k44:^4} | {k45:^4} | {k46:^4} | {k47:^4} |
 * `------------------------------------------------------------------------------------'
 */
```

## File Structure

```
├── modular_keymap_ascii_generator.py  # Main script
├── layouts/                           # Keyboard configurations (18 layouts)
│   ├── alice.json
│   ├── corne.json
│   ├── dz60.json
│   ├── ergodox_ez.json
│   ├── iris.json
│   ├── kbd67.json
│   ├── kbd75.json
│   ├── kyria.json
│   ├── lets_split.json
│   ├── lily58.json
│   ├── minidox.json
│   ├── moonlander.json
│   ├── ortho75.json
│   ├── planck.json
│   ├── preonic.json
│   ├── redox.json
│   ├── sofle.json
│   └── tkl.json
├── templates/                         # ASCII templates (18 templates)
│   ├── alice.txt
│   ├── corne.txt
│   ├── dz60.txt
│   ├── ergodox_ez.txt
│   ├── iris.txt
│   ├── kbd67.txt
│   ├── kbd75.txt
│   ├── kyria.txt
│   ├── lets_split.txt
│   ├── lily58.txt
│   ├── minidox.txt
│   ├── moonlander.txt
│   ├── ortho75.txt
│   ├── planck.txt
│   ├── preonic.txt
│   ├── redox.txt
│   ├── sofle.txt
│   └── tkl.txt
└── README.md
```

## Key Mapping

Keys are mapped from the QMK LAYOUT() function parameters to template positions:
- First parameter → `{k0}`
- Second parameter → `{k1}`
- etc.

The script automatically:
- Converts QMK keycodes to readable labels (KC_ESC → ESC)
- Handles layer functions (MO(1) → 1)
- Centers text within specified widths
- Filters out placeholder keys (_______, XXXXXXX)

## Examples

### Lily58 Output
```
/* QWERTY
 * ,-----------------------------------------.                    ,-----------------------------------------.
 * | ESC  |  Q   |  W   |  E   |  R   |  T   |                    |  Y   |  U   |  I   |  O   |  P   |  `   |
 * |------+------+------+------+------+------|                    |------+------+------+------+------+------|
 * | Tab  |  A   |  S   |  D   |  F   |  G   |                    |  H   |  J   |  K   |  L   |  ;   |  '   |
 * |------+------+------+------+------+------|                    |------+------+------+------+------+------|
 * |LShift|  Z   |  X   |  C   |  V   |  B   |-------.    ,-------|  N   |  M   |  ,   |  .   |  /   |RShift|
 * |------+------+------+------+------+------|  [    |    |  ]    |------+------+------+------+------+------|
 * |LCTRL | LAlt | LGUI |ADJUST|LOWER |Space |-------|    |-------|Space |RAISE | Left | Down |  Up  |Right |
 * `-----------------------------------------/       /     \      \-----------------------------------------'
 *                   | LAlt | LGUI |LOWER | /Space  /       \Enter  \ |RAISE |BackSP| RGUI |
 *                   |      |      |      |/       /         \      \ |      |      |      |
 *                   `----------------------------'           '------''--------------------'
 */
```

### Planck Output
```
/* QWERTY
 * ,------------------------------------------------------------------------------------.
 * | Tab  |  Q   |  W   |  E   |  R   |  T   |  Y   |  U   |  I   |  O   |  P   | Bksp |
 * |------+------+------+------+------+------+------+------+------+------+------+------|
 * | Esc  |  A   |  S   |  D   |  F   |  G   |  H   |  J   |  K   |  L   |  ;   |  '   |
 * |------+------+------+------+------+------+------+------+------+------+------+------|
 * | Shift|  Z   |  X   |  C   |  V   |  B   |  N   |  M   |  ,   |  .   |  /   |Enter |
 * |------+------+------+------+------+------+------+------+------+------+------+------|
 * | Ctrl | Alt  | GUI  |Lower |Space |Space |Space |Raise | Left | Down |  Up  |Right |
 * `------------------------------------------------------------------------------------'
 */
```

## Legacy Version

The original `keymap_ascii_generator.py` and `universal_keymap_ascii_generator.py` are available in the `archive/` directory for legacy compatibility, but the modular version is recommended for all new projects.

## Contributing

To contribute new keyboard layouts:
1. Create the layout JSON and template files
2. Test with a real keymap.c file  
3. Submit a pull request with both files
4. Include sample output in your PR description

Popular keyboards that could be added:
- **Ergodash** - Split ergonomic
- **Helix** - Split ortholinear  
- **Viterbi** - Split ortholinear
- **Quefrency** - Split staggered
- **Levinson** - Split ortholinear
- **Nyquist** - Split ortholinear

## Troubleshooting

### Layout Not Detected
If your keyboard isn't detected automatically:
1. Check if it's in the supported list (`--list`)
2. Verify your keymap.c uses standard QMK LAYOUT() functions
3. Force a specific layout with `--layout <name>`
4. Consider adding support for your keyboard

### Key Count Mismatch
If you get key count errors:
- Ensure your LAYOUT() function has the expected number of parameters
- Check for extra commas or missing keys in your keymap
- Verify the layout configuration matches your keyboard variant

### Template Formatting Issues
If ASCII output looks wrong:
- Check template alignment (use consistent `{k#:^width}` formatting)
- Ensure all key positions are defined in the template
- Test with a simple keymap first

## License

This project is released under the same license as QMK.
