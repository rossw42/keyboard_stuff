# Mounting Styles → Ergogen Case Templates: Feasibility Analysis

**Status:** Research / design proposal (no implementation yet — per project rules, this phase is documentation only.)
**Companion docs:** [`mounting_styles_README.md`](mounting_styles_README.md), [`../docs/ergogen_design_prompt.md`](../docs/ergogen_design_prompt.md), [`../TOOLKIT_PLAN.md`](../TOOLKIT_PLAN.md)
**Authority:** `D:\Keyboard Workspace\ergogen-docs-md` (cases, outlines sections)

---

## 1. What Ergogen's case system can actually do

Before deciding what's feasible, we must be honest about the primitive set. From the docs
(`ergogen-docs-md/cases/index.md` and `outlines/index.md`), Ergogen's 3D capabilities are:

| Capability | How |
|---|---|
| Linear extrusion of any 2D outline along Z | `what: outline` + `extrude: num` |
| Positioning extrusions in 3D | `shift: [x, y, z]`, `rotate: [ax, ay, az]` |
| Boolean combination of solids | `operation: add / subtract / intersect` |
| Reusing solids as building blocks | `what: case` + `name`, `_private` names |
| Parametric dimensions | global `units:` / `variables:` referenced in every number field |
| Rich 2D shape generation feeding the above | outlines: `rectangle`, `circle`, `poly`, `outline` reuse, `expand`, `fillet`, filters/tags |

**What it can NOT do (natively):**

- No chamfers, 3D fillets, or draft angles on vertical walls
- No lofts, sweeps, or curved top surfaces
- No true countersinks/counterbores as a primitive (must be faked with stacked bores)
- No threads (rely on heat-set inserts or self-tapping screws)
- No "shell" operation (walls are made by subtracting an inner outline from an outer one)
- Whole-piece `rotate` exists, so *tenting* is possible, but *per-face* angling is not

**Key insight:** every keyboard case in Ergogen is a **Z-stack of extruded 2D layers combined
with booleans**. Every mounting style therefore has to be decomposed into:

1. a set of 2D outlines (derivable from the user's points + board shape), and
2. a per-piece recipe of `(outline, extrude, z-shift, operation)` steps.

That decomposition is exactly what a "mounting style template" should encode.

---

## 2. Feasibility verdict per style

All six styles are geometrically expressible in Ergogen. Difficulty varies with how much
Z-layering trickery is needed:

| Style | Feasibility | Difficulty | Why |
|---|---|---|---|
| **Sandwich mount** | ✅ Fully | ★ Easy | It's literally stacked extruded plates with through-holes — the construction Ergogen is best at (classic laser-cut case). |
| **Tray mount** | ✅ Fully | ★ Easy | Bottom shell + internal standoff bosses (extruded circles) + screw holes. Already demonstrated in `working_samples` (tutorial.yml, jonkey, etc.). |
| **Integrated plate** | ✅ Fully | ★★ Easy-Med | Top piece = plate outline (with switch cutouts) unioned with wall ring, extruded; walls continue downward. One-piece top. |
| **Bottom mount** | ✅ Fully | ★★★ Medium | Plate gets perimeter tabs; case bottom gets a support ledge under the tabs; screws come up from below into inserts in the tabs/ledge. |
| **Top mount** | ✅ Fully | ★★★ Medium | Same tabbed plate, but ledge hangs from the *top* case and screws come down from above. Countersunk heads must be faked with a stepped bore (see §4.3). |
| **Gasket mount** | ⚠️ Geometry yes, physics on you | ★★★★ Hard | Gasket tabs on the plate and matching channels in both halves are just more subtracted extrusions. But gasket compression (0.3–0.5 mm interference, durometer choice) is a *tolerance* problem Ergogen can't validate — templates can only expose the parameters. |

**Conclusion: yes, this is possible.** Nothing in the six styles requires geometry outside
"extrude + shift + boolean." The stretch-goal fear in the README was justified only for
aesthetics (no curved/sculpted cases), not for structural correctness.

---

## 3. The core idea: styles differ only in the *interface layer*

Comparing the cheat-sheet cross-sections, every style shares the same Z-stack skeleton:

```
Z ↑
        ┌───────────────────────────┐
        │  (top case / bezel)       │   ← optional, style-dependent
        ├───────────────────────────┤
        │  PLATE (switch cutouts)   │   ← at z = plate_z
        ├───────────────────────────┤
        │  air gap / PCB            │   ← pcb_z = plate_z - plate_pcb_gap
        ├───────────────────────────┤
        │  WALLS (outer − inner)    │
        ├───────────────────────────┤
        │  FLOOR                    │   ← z = 0
        └───────────────────────────┘
```

What changes between styles is **only how the plate (or PCB) connects to the case**:

| Style | Plate↔case interface | Fastener direction |
|---|---|---|
| Tray | *no plate connection* — PCB screws to floor standoffs | bottom → up |
| Top | plate tabs rest under a ledge in the **top** case | top → down |
| Bottom | plate tabs rest on a ledge in the **bottom** case | bottom → up |
| Sandwich | plate clamped between halves by through-bolts | through |
| Gasket | gasket tabs squeezed in channels, **no screws to plate** | (halves bolt to each other only) |
| Integrated | plate **is** the top case | (halves bolt to each other only) |

So a mounting style can be modeled as: **shared skeleton + interface strategy + fastener
strategy + parameter defaults.** That's the data format.

---

## 4. Proposed representation

Two complementary layers. Option A works today with zero tooling; Option B is what the
consolidated toolkit should eventually build.

### 4.1 Option A — Pure-Ergogen template fragments (convention-based)

A template per style, written as a partial Ergogen config containing only `units:`,
`outlines:` (the case-specific ones), and `cases:`. It works because Ergogen's preprocessor
supports `$extends` inheritance, and because outlines/cases can reference names by convention.

**The contract the user's config must fulfill:**

| The template expects... | Meaning |
|---|---|
| outline `_panel` | the closed board perimeter (poly or bound keys), *without* switch cutouts |
| outline `_switch_cutouts` | 14×14 rectangles at every key (`where: /key/`) |
| points tagged `mount` | perimeter mounting-hole / tab locations |
| points tagged `standoff` | interior PCB standoff locations (tray mount only) |
| the `units:` listed below | overridable parameters |

**Shared parameter block (template defaults, user-overridable):**

```yaml
units:
  # --- material / printing ---
  wall: 2.5           # case wall thickness
  floor: 3            # case bottom thickness
  plate_t: 1.5        # plate thickness (1.5 = MX snap-in)
  fit: 0.25           # clearance between mating parts

  # --- vertical stackup ---
  cavity: 8           # inner height: floor top -> plate bottom
  bezel: 2            # how far the case rises above the plate
  plate_pcb_gap: 3.4  # MX switch: plate underside to PCB top

  # --- fasteners ---
  screw_d: 3.2        # M3 free fit
  insert_d: 4.6       # M3 heat-set insert bore
  insert_h: 5.7
  head_d: 6           # screw head / counterbore diameter
  head_h: 1.8

  # --- style-specific (only used by some templates) ---
  tab_w: 8            # top/bottom-mount tab width
  tab_l: 4            # tab protrusion beyond plate edge
  gasket_t: 2         # uncompressed gasket thickness
  gasket_squish: 0.4  # designed compression
  channel_d: 1.6      # gasket channel depth per half
```

**Shared derived outlines every template builds the same way:**

```yaml
outlines:
  _case_inner:            # cavity boundary
    - name: _panel
      expand: fit
  _case_outer:            # outer footprint
    - name: _panel
      expand: fit + wall
      fillet: 2
  _wall_ring:             # walls = outer − inner
    - name: _case_outer
    - operation: subtract
      name: _case_inner
  _plate:                 # generic plate (used by 5 of 6 styles)
    - name: _panel
    - operation: subtract
      name: _switch_cutouts
  _screw_holes:
    - what: circle
      where: mount
      radius: screw_d / 2
```

Then each style template adds its interface outlines and a `cases:` recipe. Skeletons:

#### Sandwich (easiest — validate the pipeline with this or tray first)

```yaml
outlines:
  _bolt_holes: {what: circle, where: mount, radius: screw_d / 2}
cases:
  bottom_layer:
    - {name: _case_outer, extrude: floor}
    - {name: _bolt_holes, extrude: floor, operation: subtract}
  spacer_layer:            # print/cut N of these to reach `cavity` height
    - {name: _wall_ring, extrude: cavity}
    - {name: _bolt_holes, extrude: cavity, operation: subtract}
  plate_layer:
    - {name: _plate, extrude: plate_t}
    - {name: _bolt_holes, extrude: plate_t, operation: subtract}
```

#### Tray mount

```yaml
outlines:
  _standoff_bosses: {what: circle, where: standoff, radius: insert_d / 2 + wall}
  _standoff_bores:  {what: circle, where: standoff, radius: screw_d / 2}
cases:
  tray:
    - {name: _case_outer, extrude: floor + cavity + plate_t + bezel}
    - {name: _case_inner, extrude: cavity + plate_t + bezel,
       shift: [0, 0, floor], operation: subtract}          # hollow it out
    - {name: _standoff_bosses, extrude: floor + cavity - plate_pcb_gap}  # bosses up to PCB height
    - {name: _standoff_bores, extrude: floor + cavity, operation: subtract}
```

#### Top mount (the README's designated first target)

```yaml
outlines:
  _plate_tabs:                    # plate + tabs sticking outward at mount points
    - name: _plate
    - what: rectangle
      where: mount
      size: [tab_w, tab_l * 2]    # straddles the plate edge
  _tab_pockets:                   # ledge cutout in the top case, with clearance
    - what: rectangle
      where: mount
      size: [tab_w + 2 fit, tab_l * 2 + 2 fit]
  _tab_screws: {what: circle, where: mount, radius: screw_d / 2}
  _tab_heads:  {what: circle, where: mount, radius: head_d / 2}
cases:
  plate:
    - {name: _plate_tabs, extrude: plate_t}
    - {name: _tab_screws, extrude: plate_t, operation: subtract}
  top_case:
    # wall ring spanning plate zone + bezel
    - {name: _wall_ring, extrude: plate_t + bezel + fit}
    # ledge the tabs hang from: solid ring segment above tab pockets
    - {name: _tab_pockets, extrude: plate_t + fit, operation: subtract}
    # stepped bore ≈ countersink: head recess from the top, shank below
    - {name: _tab_screws, extrude: plate_t + bezel + fit, operation: subtract}
    - {name: _tab_heads, extrude: head_h, shift: [0, 0, plate_t + bezel + fit - head_h],
       operation: subtract}
  bottom_case:
    - {name: _case_outer, extrude: floor + cavity}
    - {name: _case_inner, extrude: cavity, shift: [0, 0, floor], operation: subtract}
    # + heat-set insert bosses at the wall joint (mount points, insert_d bores)
```

Bottom mount is the same with the ledge/screws flipped to the bottom half. Integrated plate
merges `top_case` and `plate` into one part (union `_plate` at the top of the wall ring —
drop the tabs and pockets entirely). Gasket mount replaces `_plate_tabs` screws with:

```yaml
  # gasket tabs (no holes), and channels subtracted from BOTH halves:
  _gasket_channels:
    - what: rectangle
      where: mount
      size: [tab_w + 2 fit, tab_l * 2 + 2 fit]
cases:
  # in top_case:  {name: _gasket_channels, extrude: channel_d, operation: subtract} at its rim
  # in bottom_case: same, at the top of the walls
  # channel_d * 2 + plate_t + (gasket_t*2 - gasket_squish*2) defines the stackup
```

> ⚠️ Snippets above are **design sketches**, not tested configs — they follow the documented
> `cases:`/`outlines:` grammar but must be validated against a local Ergogen run (Milestone
> work). Notably, the exact `where:`-at-case-level indirection requires the shapes to be
> generated as outlines first; cases can only reference outlines, so all `where:` filtering
> happens in the `outlines:` section as shown.

### 4.2 Option B — Toolkit descriptor format (compile to Ergogen)

For the consolidated toolkit, a higher-level machine-readable descriptor is better than raw
template fragments, because it lets one generator emit all styles and validate parameters.
Proposed schema (`mounting_style.schema.yaml`):

```yaml
# One file per style, e.g. styles/top_mount.yaml
style: top_mount
description: Plate tabs screwed to the top case from above
pieces:                       # each piece = one exported case
  - id: plate
    layers:                   # ordered (outline, extrude, z, op) recipe
      - {outline: plate_with_tabs, extrude: $plate_t, z: 0, op: add}
      - {outline: tab_screw_holes, extrude: $plate_t, z: 0, op: subtract}
  - id: top_case
    layers:
      - {outline: wall_ring, extrude: "$plate_t + $bezel + $fit", z: 0, op: add}
      - {outline: tab_pockets, extrude: "$plate_t + $fit", z: 0, op: subtract}
      - {outline: tab_screw_holes, extrude: "*", z: 0, op: subtract}
      - {outline: head_recess, extrude: $head_h, z: top - $head_h, op: subtract}
  - id: bottom_case
    layers: [...]
interface:                    # what the style does at plate<->case boundary
  type: tabs                  # tabs | gasket_tabs | standoffs | through_bolts | integrated
  at: points.tag == mount
fasteners:
  - {between: [plate, top_case], direction: down, type: m3_countersunk}
  - {between: [top_case, bottom_case], direction: up, type: m3_insert}
parameters:                   # defaults + validation ranges
  bezel: {default: 2, min: 1}
  tab_w: {default: 8, min: 6}
  ...
requires:                     # the user-config contract, checkable by the generator
  outlines: [_panel, _switch_cutouts]
  tags: [mount]
outline_recipes:              # how the generator synthesizes the style's outlines
  plate_with_tabs: "panel - switch_cutouts + rect(tab_w, 2*tab_l) @mount"
  ...
```

A small Python generator (fits naturally next to `kle_to_ergogen`/toolkit consolidation)
then:

1. loads the user's base Ergogen config (points + `_panel`),
2. checks the `requires:` contract (fail fast with clear errors — the #1 usability win),
3. resolves `$params` against defaults/overrides,
4. emits the `outlines:` and `cases:` sections and merges them into the config.

Advantages over raw fragments: parameter validation, one source of truth per style,
cross-style consistency, and it can later emit *both* the Ergogen case **and** matching
PCB mounting-hole footprints (tying into `ergogen-footprints`).

### 4.3 Known workarounds/limitations to document in templates

- **Countersinks:** stepped bore (small circle full-depth + large circle partial-depth) —
  functional, not conical. Fine for FDM printing.
- **Threads:** always design for heat-set inserts (`insert_d` bore) or through-bolts.
- **Gasket compression:** expose `gasket_t`/`gasket_squish`/`channel_d` and put the stackup
  math in comments; Ergogen cannot verify it.
- **Ergogen STL quality:** cases output is basic CSG (JSCAD); complex boolean chains can be
  slow or produce artifacts. Alternative used by the community: export outline DXFs and do
  the extrusion stack in OpenSCAD/CadQuery — the descriptor format in §4.2 is deliberately
  backend-agnostic (layers = trivially portable to OpenSCAD `linear_extrude`).
- **Tenting:** possible via `rotate` on whole pieces, but interacts badly with flat floors;
  treat as out of scope for v1 templates.

---

## 5. Recommended path (when unblocked)

1. **Sandwich first, not top mount.** It's the smallest step from what `working_samples`
   already demonstrate (pure layer stack), and it validates the whole
   contract-template-parameters pipeline with minimal 3D risk. Then top mount (tab/ledge
   mechanics), then bottom (mirror), tray (bosses), integrated (merge), gasket (channels).
2. Build **Option A fragments first** (hand-written, tested one by one in local Ergogen),
   because they double as the golden-output test fixtures for the Option B generator.
3. Only then write the **Option B generator** inside the consolidated toolkit, generating
   what the fragments prove works.
4. Keep `reference_images/` cross-sections next to each template as documentation.

## 6. Bottom line

- **Is it possible?** Yes — all six mounting styles reduce to Z-stacked extrusions and
  booleans, which is exactly Ergogen's case model. Gasket mount is the only one where
  Ergogen can produce the geometry but not guarantee the mechanics.
- **Best representation:** a shared parameter block + per-style "layer recipe," expressed
  first as convention-based Ergogen template fragments (§4.1) and later as a validated
  descriptor format compiled by the toolkit (§4.2).
- **Biggest risks:** JSCAD output quality on complex boolean stacks, and tolerance tuning
  (`fit`, insert bores) that varies per printer — both mitigated by exposing them as `units`.