# Ergogen Reference

A condensed but comprehensive reference for Ergogen (the "Ergonomic Generator"), a YAML-driven keyboard generator. Compiled from the official Ergogen documentation. This document is intended as a self-contained design basis - readers are not assumed to have access to the original docs.

---

## 1. What Ergogen Is and the Config Pipeline

Ergogen is a declarative generator for ergonomic keyboards. From a single config file it generates:

- **Points** - the calculated key positions (raw/canonical YAML plus a demo visualization)
- **Outlines** - 2D board/plate/case shapes exported as **DXF and SVG**
- **Cases** - 3D-printable extrusions exported as **JSCAD** (currently)
- **PCBs** - un-routed KiCAD `.kicad_pcb` files with all footprints placed and nets pre-assigned (no schematic/project files; routing is done manually or via an auto-router)

The defining opinion of Ergogen is an explicit focus on **column stagger**: layouts are built columns-first, left-to-right, and rows bottom-to-top.

### Config format

The config is a single YAML file (JSON also works - the generator auto-detects the input format; you can even supply JavaScript code that evaluates to the config object, useful when you need loops/branching/parametric functions). The top-level keys:

```yaml
meta: <metadata>            # optional
units: <units config>       # optional
points: <points config>     # REQUIRED
outlines: <outline config>  # optional
cases: <case config>        # optional
pcbs: <pcb config>          # optional
```

### Pipeline order

1. **Preprocessing** - unnesting, inheritance ($extends), parameterization ($params/$args), skipping ($skip), math-string evaluation.
2. **Units** - resolve predefined and custom units/variables.
3. **Points** - lay out zones/columns/rows into named 2D points with rotation plus metadata.
4. **Outlines** - place shapes at (filtered subsets of) points and combine with boolean operations into 2D outlines.
5. **Cases** - extrude and combine outlines into 3D objects.
6. **PCBs** - place footprints at points, add outline-based edge cuts, and paste everything into a KiCAD template.

Each stage consumes the results of the previous one (outlines use points; cases use outlines; PCBs use both points and outlines).

Input bundles (zip/.ekb) can also carry custom footprints and templates alongside the config.

---

## 2. Config Formats and Preprocessing

Ergogen runs a separate preprocessor pass on the config before interpreting it:

### Unnesting (dot notation)

Any object key containing dots is unnested:

```yaml
nested.key.definition: value
# becomes:
# nested:
#   key:
#     definition: value
```

This works anywhere and makes deep single-value overrides terse (e.g. `points.zones.matrix.anchor.rotate: 5`).

### Inheritance ($extends)

Any declaration can inherit values from another with `$extends`, whose value is the full absolute dot-notation path of the source declaration:

```yaml
top:
  parent:
    a: 1
    b: 2
child:
  $extends: top.parent
  c: 3
# child => {a: 1, b: 2, c: 3}
```

Extension rules:

- If the new value is `undefined`, the old value is kept (acts as a default).
- If both values are defined and have the same type, the new one overrides the old.
- If the types differ, the new value takes precedence.
- If the new value is `$unset`, the result is `undefined` regardless of the previous value/type.
- Arrays and objects are extended recursively, element-wise.

### Parameterization ($params / $args)

Placeholder replacement (regex-based) within a declaration - a pseudo-variable defined once and used in multiple places:

```yaml
top:
  value: placeholder
  double_value: placeholder * 2
  $params: [placeholder]
  $args: [3]
# every occurrence of "placeholder" becomes "3"
```

### Skipping ($skip)

`$skip: true` comments out a whole declaration. Useful for abstract intermediate declarations that combine `$extends` with partial `$args` (which would otherwise error for missing arguments):

```yaml
grandparent:
  a: placeholder1
  b: placeholder2
  $params: [placeholder1, placeholder2]
parent:
  $extends: grandparent
  $args: [value1]
  $skip: true          # abstract; only supplies the first arg
child:
  $extends: parent
  $args: [,value2]     # supplies the second arg
```

### Math-string evaluation

The preprocessed result is almost plain JSON, except: every string that parses as a math formula is evaluated and converted to a number. So `3 * 2` becomes `6`, and formulas may reference units/variables (e.g. `u - 1`, `0.5 sx`). This is the mechanism behind units and shape-specific units.

If the declarative config (plus YAML anchors, `$extends`, and the preprocessor) still is not terse enough, you can write code that generates the config (branching, loops, parametric functions).

---

## 3. Units / Variables

The optional `units` top-level clause (alias: `variables`) defines values usable in math expressions everywhere in the config. Four are predefined:

```yaml
U: 19.05   # MX spacing (mm)
u: 19      # simplified MX spacing (mm)
cx: 18     # Choc X spacing (mm)
cy: 17     # Choc Y spacing (mm)
```

You may add new units, override the predefined ones, and derive units from previously defined ones (declaration order matters):

```yaml
units:
  double: 2 u
  a: cy - 7
  b: a * 1.5
```

There are also internal variables that supply overrideable defaults for key-level attributes:

```yaml
$default_stagger: 0
$default_spread: 'u'
$default_splay: 0
$default_height: 'u-1'
$default_width: 'u-1'
$default_padding: 'u'
$default_autobind: 10
```

Overriding e.g. `$default_padding: cy` in your `units` section changes the default for every key at once (handy for Choc spacing).

---

## 4. Points

### Coordinate system

A point is `[x, y]` plus rotation `r` plus metadata. X is positive to the right, Y positive upward. Rotation represents the direction of the Y axis and increases counter-clockwise (+90 deg = turn left). Points are typically the center points of keycaps. Notation used throughout: `[x, y, r deg]`.

### Anchors

Anchors compute a point from an existing starting point via translation/rotation. They appear in many sub-fields (zone anchors, `adjust`, polygon points, PCB footprint placement, mirror axes, etc.). Anchor value types:

- **string** - a reference to an existing named point, used as-is.
- **array** - a multi-anchor: each item is itself an anchor; each sub-anchor result becomes the next one starting point ("follow the dots").
- **object** - full anchor declaration with these fields:
  - **ref** - the starting point (parsed recursively as an anchor itself; simplest form is a point name).
  - **aggregate** - mutually exclusive with `ref`; combines several locations: `{parts: [<anchors>], method: average}`. Only `average` exists so far (and is the default); averaging applies to x, y, AND r.
  - **orient** - pre-rotation, before shifting. A number (added to the current rotation) or a sub-anchor (the point "turns towards" the referenced location). Affects only `r`.
  - **shift** - translation `[x, y]` (a single number expands to `[n, n]`). Shifting is relative to the current rotation - at r=90 deg a positive x shift moves visually upward.
  - **rotate** - post-rotation after shifting; same semantics as `orient`.
  - **affect** - restrict which fields the anchor writes: a string like `"xy"`/`"r"` or an array of `"x"`/`"y"`/`"r"`. E.g. copy only another point rotation: `{ref: existing, affect: r}` as the second part of a multi-anchor.
  - **resist** - `true` disables the special mirrored-point treatment (normally shifts/rotations are mirrored on mirrored points to keep symmetry - a shift of `[1, 1]` becomes `[-1, 1]` and rotations go clockwise; `resist` applies them as written, e.g. for PCB footprints that always face up).

```yaml
anchor:
  - orient: 45
    shift: [1, 0]
    rotate: 135
  - shift: [1, 0]
    rotate.shift: [0, 0]   # rotate towards the origin (sub-anchor form)
```

```yaml
anchor:
  aggregate.parts:
    - left
    - right
  shift: [1, 0]
  rotate: 180
```

### Zones

Zones declare batches of points. A zone contains **columns** (laid out left-to-right), each containing **rows** (bottom-to-top). Multiple zones separate e.g. the keywell and the thumb fan/cluster; columns can be staggered and splayed; zones can be anchored to each other.

```yaml
points:
  zones:
    <zone_name>:
      anchor: <anchor>       # optional zone position, default [0, 0, 0deg]
      columns:
        <column_name>:
          rows:
            <row_name>: <key defs>   # per-key attributes
          key: <key defs>            # column-wide attributes
      rows:
        <row_name>: <key defs>       # zone-wide row attributes
      key: <key defs>                # zone-wide attributes
  key: <key defs>                    # global attributes for ALL zones
```

### Key-level attribute inheritance

Attributes cascade from generic to specific (later levels override earlier ones):

1. Built-in hardcoded defaults
2. Global `points.key`
3. Zone-wide `points.zones.<zone>.key`
4. Column-wide `points.zones.<zone>.columns.<col>.key`
5. Row-wide `points.zones.<zone>.rows.<row>`
6. Key-specific `points.zones.<zone>.columns.<col>.rows.<row>`

Levels 2-4 use a `.key` suffix; levels 5-6 do not (those nodes hold only key attributes). Simple values replace; arrays/objects merge recursively; `$unset` removes a value. Common use: remove the top pinky key with `pinky.rows.top: $unset` while zone-wide rows still apply elsewhere.

### Key attributes with layout meaning

- **stagger** - extra vertical shift of a column starting point vs. the previous column (cumulative). Default `0`.
- **spread** - horizontal distance to the next column. Default `u`.
- **splay** - rotation applied at the start of a new column (cumulative), around optional **origin** (default `[0, 0]` = the center of where the first key of the column would go). Use e.g. `origin: [-u/2, -u/2]` to hinge at a key bottom-left corner so rotation does not overlap the previous column.
- **padding** - vertical gap between rows within a column. Default `u`.
- **orient / shift / rotate** - like the anchor fields, but applied cumulatively within the column (positioning the current key AND the starting point for the next row).
- **adjust** - a full anchor applied independently to this key only (does not affect the running column layout).
- **bind** - directional "reach" for outline binding: `num`, `[x, y]`, or `[top, right, bottom, left]` (CSS order). Default `-1` (no bind; defer to autobind).
- **autobind** - automatic binding reach in relevant directions (computed from intra-/inter-column bounding boxes). Default `10`.
- **skip** - `true` marks the point as a helper (stepping stone) only, excluded from output. Default `false`.
- **asym** - which side the key belongs to for mirroring: `source` / `clone` / `both` (default `both`). Aliases: `origin`/`image`, `base`/`derived`, `primary`/`secondary`, `left`/`right`.
- **mirror** - (key-level) overrides any key attributes for the mirrored copy of this key. Empty by default.
- **colrow** - built-in convenience name `{{col.name}}_{{row}}`, unique within a zone.
- **name** - globally unique key name, default `{{zone.name}}_{{colrow}}`. For single-key zones, `default` column/row suffixes are trimmed, so the key name equals the zone name.
- **width / height** - keycap size for the demo visualization only (default `u-1` = 18). Real cut shapes come from outlines.

Any extra custom attributes are allowed and stored in the key metadata - commonly used to pass per-key info (e.g. net names) to PCB footprints later.

**Templating:** inside strings, `{{attribute}}` is replaced by the same-named key-level attribute (`{{colrow}}` expands to e.g. `pinky_home`).

Example zone:

```yaml
points.zones.matrix:
  anchor.rotate: 5           # skew the whole zone
  columns:
    pinky:
    ring.key:
      splay: -5              # resets subsequent columns upright
      stagger: 12
      origin: [-u/2, -u/2]   # hinge at bottom-left corner of the key
    middle.key.stagger: 5
    index.key.stagger: -6
    inner.key.stagger: -2
  rows:
    bottom:
    home:
    top:
```

### Layout algorithm (how a zone unfolds)

1. The zone `anchor` sets the initial running "column anchor".
2. For each column: copy the column anchor to a running "row anchor" (key-level `orient`/`shift`/`rotate` apply here, cumulatively).
3. Place a key at the row anchor; apply `padding` to reach the next row; repeat for all rows in the column.
4. Move to the next column by applying `spread` (horizontal), `stagger` (vertical), then `splay` (rotation around `origin`), all cumulative.
5. Repeat until all columns are done; then further zones can anchor onto keys of prior zones (e.g. a thumbfan referencing `matrix_inner_bottom`).

### Global / zone-level adjustments

```yaml
points:
  zones:
    zone_name:
      rotate: <number>   # zone-level rotation (rotation origin is always [0, 0])
      mirror: <axis>     # zone-level mirror
  rotate: <number>       # global rotation (e.g. inter-half angle of one-piece boards)
  mirror: <axis>         # global mirror
```

### Mirroring

Since layouts default to the left half, `mirror` creates the right half automatically:

- If `mirror` is a number, it is the x coordinate of the axis to mirror along.
- Otherwise it is an anchor with an extra `distance` field: the anchor defines a reference point, and `distance` is how far it should be from its eventual mirror image.

Per-key `asym` controls participation: `source` (skip during mirroring - original side only), `clone` (moved to the mirrored side only), `both` (default - appears on both sides). Do not confuse `points.mirror` / `points.zones.<zone>.mirror` (axis declarations) with the key-level `mirror` attribute (attribute overrides for mirrored copies). Mirrored points get mirrored shift/rotation treatment in anchors unless `resist: true`.

---

## 5. Outlines

Outlines turn points into solid 2D shapes: select a subset of points with a **filter**, place a **shape** at each, and combine parts with **boolean operations**. Named outlines are exported (DXF/SVG) and reusable by later outlines, cases, and PCB edge cuts.

### Binding

Shapes placed at points usually do not overlap, so they cannot union into one contiguous plate. Binding makes each key shape "reach out" toward its neighbors with minimal extra margin:

- **Explicit** - key-level `bind: num | [num_x, num_y] | [num_t, num_r, num_b, num_l]` (CSS order: top/right/bottom/left).
- **Automatic** - key-level `autobind: <num>` (default `10`); Ergogen infers the relevant directions from intra- and inter-column bounding boxes. Usually setting `bound: true` on the outline part is all that is needed; raise `autobind` if the gaps are too large; fall back to explicit `bind` for complex shapes.

### Filtering (where)

Filter value types:

- **undefined** - the default `[0, 0, 0deg]` origin point.
- **boolean** - `true` = all points; `false` = no points.
- **string** - simple filter (below).
- **object, or array containing an object** at any depth - parsed as an **anchor**, yielding that single resulting point.
- **array with no objects** at any depth - complex AND/OR filter (below).

String filters match against each key **name and `tags`** (`tags` is a key-level attribute: an array of tag strings, or an object whose keys count). Extras:

- **Regex**: surround with slashes - `/^matrix_.*/` matches all keys whose name starts with `matrix_` (regex flags after the trailing slash are supported).
- **Negation**: prefix with `-` (minus) - `-matrix_pinky_home` (everything except that key), `-alpha` (everything not tagged alpha), `-/pinky/`.
- **Full form**: `something` is shorthand for `meta.name,meta.tags ~ something` (`~` is the similarity operator, the only one implemented so far). Check a custom attribute with e.g. `meta.foobar ~ something`.
- **Complex filters**: arrays nest logic - odd nesting levels are OR, even levels are AND. `[a, b]` = a OR b; `[[a, b]]` = a AND b.

### Outline structure

```yaml
outlines:
  <outline_name>:
    - <part>        # array notation
    - <part>
  <other_outline>:
    part1: <part>   # object notation also works
    part2: <part>
```

Parts are applied in order; the result is exported and available to later outlines via the `outline` shape type. Prefix a name with `_` (e.g. `_helper`) to make it private (usable as a building block, not exported).

### Common part attributes

- **what** - which shape to place: `rectangle` / `circle` / `poly` / `outline`.
- **where** - the filter selecting placement points.
- **operation** - how to combine with the running result:
  - `add` (union, the default), `subtract`, `intersect`, `stack` (draw on top without boolean math - cheap; mostly for visualizing/debugging individual parts in context).
- **bound** - `true` activates binding rectangles on each relevant shape side and unions the result; `false` places shapes as-is.
- **asym** - how filtering treats mirrored points: `source` (default - only direct matches), `clone` (only mirror images), `both`. Strict (errors if the mirror image does not exist) when the filter is an anchor; permissive for regular filters.
- **adjust** - a relative anchor applied to each shape position (place shapes near points, not just at them).
- **scale** - multiplier for the resulting shape (default `1`).
- **expand** - number in mm to expand (positive) or shrink (negative) the outline; unlike `scale`, it offsets the contour (usually changing the shape itself, not just its size).
- **joints** - corner treatment during expansion: `0`/`round`, `1`/`pointy`, `2`/`beveled`.
- **fillet** - radius (greater than the default 0) to round corners of the (almost-)complete part. Corners whose neighboring segments are shorter than the radius are skipped; already-filleted corners are not re-filleted (safe to apply successively smaller radii to catch every sharp corner).

### Shape types (what)

Each shape can add shape-specific units to the math context (e.g. `adjust.shift: [.5 sx, 0]` = half the rectangle width to the right).

- **rectangle**
  - `size`: `num` (square) or `[num_x, num_y]`. Mandatory. Introduces units `sx` (width) and `sy` (height).
  - `bevel`: optional corner bevel, default `0`.
  - `corner`: optional corner radius, default `0`.
  - `size` is the FINAL size (bevel/corner values are subtracted internally - too-small sizes or too-large bevel/corner values error). Corner radii apply after bevels, so rounded bevels are possible.
- **circle**
  - `radius`: mandatory. Introduces unit `r`.
- **poly** (custom polygon)
  - `points`: mandatory array of anchors - each anchor implicit `ref` is the previous polygon point (a continuous chain); the first point defaults to `[0, 0, 0deg]` (the polygon is placed using a `[0, 0]` origin anyway).
- **outline** (reuse an existing outline as a primitive)
  - `name`: mandatory - the outline to place.
  - `origin`: optional anchor selecting which point of the existing outline acts as its placement origin (applies BEFORE placement at target points; the globally available `adjust` applies AFTER).

### Syntactic sugar

- **String shorthand parts** - a part given as a plain string starting with one of `+ - ~ ^`, followed by a name, means add/subtract/intersect/stack the named outline, respectively. No symbol = add. E.g. `~something` expands to:

  ```yaml
  what: outline
  where: undefined     # [0, 0, 0deg], just placing the outline where it is
  name: something
  operation: intersect
  ```

- **expand suffix shorthand** - declare `expand` and `joints` at once: the number followed by `)`, `>`, or `]` (round, pointy, beveled). So `expand: 3]` translates to `expand: 3` plus `joints: beveled`.
- **Private outlines** - a leading underscore in the name (e.g. `_my_name`) prevents export; the outline is only a building block.

Typical example:

```yaml
outlines:
  _switches:
    - what: rectangle
      where: true
      size: 14           # MX plate cutout
  board:
    - what: rectangle
      where: true
      size: [u, u]
      bound: true        # bind keys into a contiguous plate
      fillet: 2
  plate:
    - board              # add the board outline (string shorthand)
    - operation: subtract
      what: outline
      name: _switches
```

---

## 6. Cases

Cases extrude 2D outlines into 3D and combine them into a printable object (exported as JSCAD):

```yaml
cases:
  <case_name>:
    - what: outline            # default option
      name: <outline ref>      # which outline to import onto the xy plane
      extrude: <num>           # extrusion along the z axis, default = 1
      shift: [x, y, z]         # default [0, 0, 0]
      rotate: [ax, ay, az]     # default [0, 0, 0]
      operation: add | subtract | intersect   # default = add
    - what: case
      name: <case ref>         # reuse a previously defined case
      # extrude makes no sense here
      shift: ...
      rotate: ...
      operation: ...
```

Notes:

- `what: outline` plus `extrude` turns a 2D outline into a solid; `what: case` reuses a previously defined case object. After the base 3D object is established, it is (relatively) rotated, shifted, and combined via `operation`.
- Case parts may be listed as arrays OR objects (like outline parts) - objects are handy for inheritance/reuse.
- The `[+, -, ~]` plus name string shorthand also works here; lookup tries cases first, then outlines. `^` (stack) is omitted as it makes no sense in 3D.
- A leading underscore makes a case private (building block only), same as outlines.
- Even private outlines (`_name`) are usable as case sources.

Example (bottom plate plus a wall, combined):

```yaml
cases:
  _bottom:
    - what: outline
      name: board
      extrude: 1
  _outerwall:
    - what: outline
      name: board_expanded   # e.g. the board outline expanded by wall thickness
      extrude: 5
    - what: outline
      name: board
      extrude: 5
      operation: subtract
  case:
    - _bottom
    - _outerwall
```

---

## 7. PCBs

Ergogen positions footprints and edge cuts so that only routing remains (manual or via an auto-router). The output is an **un-routed** `.kicad_pcb` - nets know what should connect, but nothing is traced yet.

```yaml
pcbs:
  <pcb_name>:
    outlines:
      - outline: <reference to existing outline>   # required
        layer: <which KiCAD layer to draw on>      # default = Edge.Cuts
    footprints:
      - where: <filter>                   # same filter system as outlines
        asym: source | clone | both       # same as outlines, default = both
        adjust: <anchor>                   # same as outlines
        what: <footprint to use>
        params: <param object for the footprint>
    references: <bool>       # show component references on the PCB, default = false
    template: <string>       # name of the PCB template to use, default = kicad5
    params: <anything>       # pcb-level custom parameters passed to the template
```

Both `pcbs.outlines` and `pcbs.footprints` accept arrays or objects.

### Outlines on the PCB

The most common use is defining the **edge cut** by referencing a previously defined outline. Setting `layer` instead sends arbitrary marks to silk or user-defined layers.

### Footprints

- `where`/`asym`/`adjust` behave exactly as in outlines; the matched points become footprint placement locations.
- `what` names a footprint - built-ins live in the Ergogen repo `src/footprints` folder (the file basename is the `what` value); each file top comment / `params` export documents its parameters. Custom footprints can be supplied via bundles without modifying Ergogen.
- `params` values may be booleans/numbers/strings, arrays/objects, or Ergogen-specific values:
  - **Nets** - identified by a unique string name and internally indexed; every component designated to the same net should be connected together during routing.
  - **Anchors** - pass additional points to the footprint beyond the position it is placed at.
- **Templating in params**: `{{attribute}}` pulls key-level attributes per placed point, so a single declaration can place every key with per-key nets:

```yaml
pcbs.<pcb_name>.footprints:
  - where: true          # everywhere
    what: mx             # Cherry MX type switches
    params:
      from: "{{from_net}}"   # double curly braces = templating,
      to: "{{to_net}}"       # reading from each point key-level attributes
```

(Here `from_net`/`to_net` are custom key-level attributes filled out in the `points` section.)

### Final assembly

After outlines and footprints are placed, Ergogen: shows or hides all footprint references per `references`; fills PCB metadata (name = `<pcb_name>`, version/author from `meta.version`/`meta.author`); and pastes the calculated outlines and footprints into the chosen `template`.

### Custom footprint files (authoring)

An "Ergogen-ized" footprint is a `.js` module:

```js
module.exports = {
  params: {
    designator: '_',       // the only semi-required param; component naming prefix on the PCB
    // any other param names, with default values (the default also tells Ergogen the type)
    bool_param: true,
    string_param: 'default',
    number_param: 42,
    array_param: ['a', 'b', 'c'],
    object_param: {a: 1, b: 2, c: 3},
    // expanded definitions for Ergogen-specific types:
    net_param: {type: 'net', value: 'GND'},
    anchor_param: {type: 'anchor', value: 'existing_point_name'}
  },
  body: parsed_params => {
    // procedural code returning a filled-out KiCAD footprint string
    return `
      (module something (layer something)
        ${parsed_params.at}
        ${parsed_params.any_other_param}
      )
    `
  }
}
```

- `net` params resolve to net-objects with `name`, `index`, and `str` fields (`str` = `(net ${index} "${name}")`, also the default string form).
- `anchor` params resolve to points with `x`/`y`/`r` fields plus the point metadata under `meta`.
- `designator` (default `_`) is the reference prefix; a running index suffix makes each instance name unique.

**Footprint API** (extra values Ergogen provides in `parsed_params` for all footprints):

- `ref` - the computed reference name (designator plus running index, e.g. `D4` for the fourth diode).
- `ref_hide` - boolean flag whether to hide `ref` on the silkscreen (derived from `pcbs.<name>.references`).
- `x`/`y`/`r` - plain numbers for the current point (`rot` is a deprecated synonym of `r`).
- `xy` - string form `${x} ${y}`.
- `at` - the full KiCAD positioning clause `(at ${x} ${y} ${r})`.
- `local_net('name')` - defines nets local to each footprint instance, implemented as nets prefixed by the instance `ref` (e.g. `D1_trace`, `D2_trace`) so multiple instances never collide.
- Coordinate helper functions `[i/e][s/a]xy(x, y)`, each returning `{x, y, str}` (str = `${x} ${y}`):
  - `isxy` - Internal Symmetric: for coordinates inside a KiCAD module; inverts x when the source is a mirrored point.
  - `iaxy` - Internal Asymmetric: ignores mirroring (equivalent to hardcoding coordinates within a module).
  - `esxy` - External Symmetric: for traces/segments/zones outside modules; applies the module shift/rotation context first, with mirror-aware x negation.
  - `eaxy` - External Asymmetric: same external context, but no special mirror treatment.

### Custom PCB templates

Templates (built-ins per KiCAD version live in the repo `src/templates` folder) are `.js` modules:

```js
module.exports = {
  // convert MakerJS shapes into KiCAD shapes
  convert_outline: (model, layer) => { /* ... */ },
  // create the final KiCAD PCB from the precomputed parts
  body: parts => { /* ... */ }
}
```

`convert_outline` gets a shape in MakerJS format (`model`) plus the target `layer`, and returns the shape as PCB-format text. `body` builds the final PCB using a `parts` object containing:

- `name` - the PCB name (from the config),
- `version` / `author` - from the `meta` block,
- `nets` - all nets, formatted `{name: index, ...}`,
- `footprints` - array of precomputed footprints in final text form,
- `outlines` - precomputed shapes from `convert_outline`, formatted `{name: text, ...}`,
- `custom` - user-supplied parameters from `pcbs.<pcb_name>.params`.

Ergogen relies on **MakerJS** for all its 2D geometry.

---

## 8. Running Ergogen Locally

### Web

Official web deployment: https://ergogen.xyz/ (unofficial but improved: https://ergogen.ceoloide.com/). No install needed unless you want in-development features, custom modifications, or to contribute code.

### CLI (end users)

Requires **Node v14.4.0+** with **npm v6.14.5+**.

```bash
npm i -g ergogen
ergogen input.yaml -o output_folder
ergogen --help          # full option list (includes a debug flag for extra outputs)
```

### CLI (development / cutting edge)

```bash
git clone https://github.com/ergogen/ergogen.git
cd ergogen
npm install
node src/cli.js input.yaml -o output_folder   # instead of the global command
```

### Outputs (per the file-formats reference)

The output folder is organized by stage:

- `points/` - raw input echo, canonical YAML, and a demo visualization of key positions (the `width`/`height` demo squares).
- `outlines/` - each named (non-private) outline as **DXF** and **SVG**.
- `cases/` - each case as **JSCAD** (for now).
- `pcbs/` - each PCB as **.kicad_pcb** (un-routed; no schematic or KiCAD project files).

Debugging tips: the `stack` outline operation overlays a part on the in-progress result without boolean math, letting you visually inspect individual parts in context; the `points` demo output serves the same purpose for layout debugging.

---

## 9. Metadata / Versioning

The `meta` top-level key holds arbitrary board documentation. Ergogen interprets only three fields:

- **engine** - a semver string (`major.minor.patch`, e.g. `3.1.4`) declaring which Ergogen version the config targets. Checked for **compatibility**, not exact equality: `3.1.4` means at least 3.1.4 and below 4.0.0. On mismatch Ergogen errors until you update either the config proper or the `engine` field to match the current environment.
- **version** - a string embedded into generated KiCAD PCB metadata (your board version - not the engine version; do not confuse the two).
- **author** - same, for the KiCAD PCB author field.

```yaml
meta:
  engine: 4.1.0
  version: 0.2
  author: yourname
  anything_else: "ignored by Ergogen but kept for documentation"
```

Any additional fields are allowed and simply ignored by Ergogen.

---

## Appendix: Further Learning

- Search the `#ergogen` topic on GitHub for real-world configs to reverse-engineer.
- FlatFootFox tutorial series: "Lets Design A Keyboard With Ergogen v4" (https://flatfootfox.com/ergogen-introduction/).
- The Ergogen Discord (http://discord.ergogen.xyz/) for questions.
- Built-in footprints: https://github.com/ergogen/ergogen/tree/master/src/footprints
- Built-in templates: https://github.com/ergogen/ergogen/tree/master/src/templates
