# Option B — Toolkit Descriptor Format (DESIGN PROPOSAL — NOT IMPLEMENTED)

Higher-level, machine-readable mounting-style descriptors implementing the
approach from [`../MOUNTING_STYLES_ANALYSIS.md`](../MOUNTING_STYLES_ANALYSIS.md) §4.2.

> ⚠️ **Proposal only.** There is no generator yet. These files define the data
> format a future toolkit generator would consume. Build the generator only
> after the Option A fragments (`../option_a_templates/`) are validated —
> those fragments become the golden-output test fixtures.

## Why a descriptor format instead of raw templates?

- **Validation:** parameter ranges + a `requires:` contract the generator can
  check against the user's config, failing fast with clear errors.
- **One source of truth per style:** the generator emits the Ergogen
  `outlines:`/`cases:` sections; no copy-paste drift across styles.
- **Backend-agnostic:** each piece is an ordered list of
  `(outline, extrude, z, op)` layers — trivially portable to OpenSCAD
  `linear_extrude` if Ergogen's JSCAD output proves unreliable.
- **Cross-cutting outputs:** the same `mount`/`standoff` points can later
  drive PCB mounting-hole footprint emission (ties into `ergogen-footprints`).

## Files

| File | Purpose |
|---|---|
| `mounting_style.schema.yaml` | annotated schema — the format definition |
| `styles/sandwich_mount.yaml` | example descriptor (simplest style) |
| `styles/top_mount.yaml` | example descriptor (tab/ledge style) |

Descriptors for the remaining four styles (tray, bottom, integrated, gasket)
follow the same schema; write them when the generator exists, deriving the
layer recipes from the corresponding Option A fragments.

## Intended generator pipeline (future toolkit)

```
user base config (points + _panel + _switch_cutouts)
        │
        ▼
generator (Python, lives in the consolidated ergogen-toolkit)
  1. load style descriptor + user parameter overrides
  2. check `requires:` contract  ──► clear error if unmet
  3. resolve $params (defaults ▸ overrides), validate ranges
  4. synthesize `outline_recipes` into Ergogen outlines
  5. emit `units:` + `outlines:` + `cases:` and merge into the config
        │
        ▼
complete Ergogen config ──► ergogen CLI ──► DXF/STL per piece
```

## Expression conventions used in descriptors

- `$name` — parameter reference, resolved by the generator
- `"*"` for `extrude` — full height of the piece (computed from its layers)
- `z: top - X` — measured down from the piece's top face
- `outline_recipes` mini-DSL: `panel`, `switch_cutouts`, `+`/`-` booleans,
  `rect(w, h) @tag` / `circle(d) @tag` = shape placed at all points with tag,
  `expand(x)` = outline expansion. The DSL is intentionally tiny — anything
  it can express must map 1:1 to Ergogen outline parts.