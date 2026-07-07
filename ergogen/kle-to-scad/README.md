# kle-to-scad

Converts [Keyboard Layout Editor](http://www.keyboard-layout-editor.com/) (KLE) JSON files into **OpenSCAD layout files** compatible with [hotswap_pcb_generator](https://github.com/50an6xy06r6n/hotswap_pcb_generator).

> **Note:** This tool previously also generated Ergogen YAML, but that code path produced broken output and was removed during the 2026-07 consolidation (see `../audit/AUDIT_KLE_SCAD_Ergogen.md`). For KLE → Ergogen conversion, use [`../kle-to-ergogen`](../kle-to-ergogen/) instead.

## Requirements

- Node.js 18+

```
npm install
```

## Usage

```
node index.js <input.json> [options]
```

| Flag | Description |
|---|---|
| `-o, --output <path>` | Output SCAD file path (default: input with `.scad` suffix) |
| `-v, --verbose` | Verbose output |

### Example

```bash
node index.js test_40percent.json -o my_board.scad -v
```

Output for the included 40% test board: 40 keys, 4×12 matrix, 1 stabilized spacebar (`stab_6_25u`), 238.1mm × 76.2mm.

## Features

- **KLE parsing** via the battle-tested [`@ijprest/kle-serial`](https://github.com/ijprest/kle-serial) library
- **Stabilizer detection:** keys ≥ 2u automatically get stabilizer entries in `base_stab_layout` with correct Cherry spacing (constants in [`scad/stabilizer_spacing.scad`](scad/stabilizer_spacing.scad))
- **Matrix assignment:** row/column matrix positions computed for every key
- The generated `.scad` follows the hotswap_pcb_generator layout format (`base_switch_layout`, `base_stab_layout`, MCU/TRRS/via/plate/standoff placeholders)

## Using the output

The generated file `include`s `parameters.scad`, `stabilizer_spacing.scad`, and `utils.scad` from hotswap_pcb_generator. Copy your `.scad` output into a hotswap_pcb_generator checkout (or copy this repo's [`scad/`](scad/) reference files plus upstream `utils.scad` next to it), then open in OpenSCAD.

## Folder contents

```
index.js          CLI (KLE → SCAD)
src/
  kleToIntermediate.js   KLE → intermediate format (positions, matrix, stabilizers)
  scadToErgogen.js       (legacy helper, kept for reference)
  scadEvaluator.js       (legacy helper, kept for reference)
scad/
  parameters.scad          reference copy from hotswap_pcb_generator
  stabilizer_spacing.scad  Cherry stabilizer spacing constants per key size
examples/         sample KLE inputs (+ stale YAML outputs from the old pipeline)
test_40percent.json / .scad   40% board test input and known-good output
```
