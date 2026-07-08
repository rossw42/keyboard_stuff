# Option A — Pure-Ergogen Template Fragments (DESIGN SKETCHES — UNTESTED)

Per-style partial Ergogen configs implementing the approach from
[`../MOUNTING_STYLES_ANALYSIS.md`](../MOUNTING_STYLES_ANALYSIS.md) §4.1.

> ⚠️ **These are design sketches for later consideration, not validated configs.**
> They follow the documented `outlines:` / `cases:` grammar from
> `ergogen-docs-md`, but none have been run through Ergogen yet. Validation is
> Milestone work per `../../TOOLKIT_PLAN.md`.

## How they are meant to be used

Each style file contains only `units:`, `outlines:`, and `cases:` sections.
The user's base config supplies the geometry, fulfilling this **contract**:

| Required in user config | Meaning |
|---|---|
| outline `_panel` | closed board perimeter (poly or bound keys), **without** switch cutouts |
| outline `_switch_cutouts` | 14×14 mm rectangles at every key (`where: /key/`) |
| points tagged `mount` | perimeter mounting-hole / tab / gasket-tab locations |
| points tagged `standoff` | interior PCB standoff locations (tray mount only) |

Merge order: user base config → `_shared.yaml` → one style file. Merging can be
done manually, via YAML anchors, or (eventually) by the toolkit generator
(Option B). Every dimension lives in `units:` so it can be overridden.

## Files

| File | Style | Difficulty | Notes |
|---|---|---|---|
| `_shared.yaml` | — | — | parameter defaults + derived outlines used by all styles |
| `sandwich_mount.yaml` | Sandwich | ★ | recommended first validation target |
| `tray_mount.yaml` | Tray | ★ | standoff bosses; needs `standoff`-tagged points |
| `integrated_plate.yaml` | Integrated | ★★ | plate unioned into the top case |
| `bottom_mount.yaml` | Bottom | ★★★ | tabs + ledge in bottom half |
| `top_mount.yaml` | Top | ★★★ | tabs + ledge in top half, stepped-bore countersink |
| `gasket_mount.yaml` | Gasket | ★★★★ | geometry only — compression tolerances are on you |

## Validation checklist (per style, when unblocked)

1. Merge with a minimal 2x2 test config (see `../../working_samples/minimal/`)
2. Run local Ergogen; confirm all case pieces export without CSG errors
3. Inspect STL stackup: floor / walls / plate z-positions, screw hole alignment
4. Print or measure `fit` clearances; adjust defaults
5. Record the merged, working config as a golden fixture for the Option B generator