# kle-to-ergogen

Converts [Keyboard Layout Editor](http://www.keyboard-layout-editor.com/) (KLE) JSON files into [Ergogen](https://ergogen.xyz) YAML — either a full starter config or just the `points:` section for embedding in an existing config.

## Requirements

- Python 3.8+
- PyYAML

```
pip install -r requirements.txt
```

## Usage

```
python cli.py <input.json> [options]
```

### Examples

```bash
# Convert to macropad-with-3-encoders.yaml (next to the input)
python cli.py examples/macropad-with-3-encoders.json

# Specific output file, with statistics
python cli.py examples/macropad-with-3-encoders.json -o my-keyboard.yaml --stats

# Only the points section, sequential naming, no comments
python cli.py examples/macropad-with-3-encoders.json --section-only -s sequential --no-comments

# Just validate the KLE file (exit 0 = valid)
python cli.py examples/macropad-with-3-encoders.json --validate-only
```

### Options

| Flag | Description |
|---|---|
| `-o, --output FILE` | Output YAML path (default: input with `.yaml` suffix) |
| `-s, --naming-strategy {matrix,sequential,label}` | Point naming (default: `matrix`) |
| `--key-unit-size MM` | Key unit size in mm (default: `19.05`) |
| `--no-center` | Don't center the layout on the origin |
| `--no-invert-y` | Keep KLE's Y orientation (default flips for Ergogen) |
| `--section-only` | Emit only the `points:` section |
| `--no-comments` | Omit provenance comments |
| `--precision N` | Coordinate decimal places (default: 3) |
| `--indent N` | YAML indent (default: 2) |
| `--no-sort` | Don't sort point names alphabetically |
| `--validate-only` | Validate input and exit |
| `--stats` | Print conversion statistics |
| `-v, --verbose` | Verbose output |

## Features

- **Naming strategies:** `matrix` (`r0c1`), `sequential` (`key_0`), or `label` (sanitized KLE labels with matrix fallback)
- **Provenance comments:** each generated point is annotated with its original KLE key label and matrix position
- **KLE metadata support:** handles KLE files with a leading metadata object (name/author)
- **Regular-grid detection:** uniform layouts emit a zone-based config; irregular layouts (wide/tall/rotated keys) use absolute `shift` positioning
- **Correct spacing:** uses 19.05 mm per key unit (Ergogen's `u`)

## Known Limitations

- Points-focused: does not yet generate `outlines`, `cases`, or `pcbs` sections (planned — see `../TOOLKIT_PLAN.md` Milestone 4)
- No stabilizer or diode/matrix wiring output yet (planned port from `../kle-to-scad`)
- The built-in KLE parser handles standard layouts; exotic KLE features (rotated clusters with `rx`/`ry` chains, ghosted keys) may need review