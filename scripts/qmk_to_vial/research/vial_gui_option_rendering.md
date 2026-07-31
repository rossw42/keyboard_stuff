# Vial GUI: How Layout Options Are Rendered

Research into how the Vial GUI (vial-kb/vial-gui, branch `main`) parses and renders
layout options, to determine what geometry generated alternative-layout keys must have
in a `vial.json` KLE keymap.

Source files fetched read-only from GitHub (raw copies saved alongside this doc):

- `src/main/python/protocol/keyboard_comm.py` -> `_tmp_keyboard_comm.py`
- `src/main/python/widgets/keyboard_widget.py` -> `_tmp_keyboard_widget.py`
- `src/main/python/editor/layout_editor.py` -> `_tmp_layout_editor.py`
- `src/main/python/kle_serial.py` -> `_tmp_kle_serial.py`

---

## 1. How labels / suffix are parsed (`layout_index`, `layout_option`)

Parsing happens in `Keyboard.reload_layout()` in
`src/main/python/protocol/keyboard_comm.py` (lines ~168-194). The KLE keymap is
deserialized with the bundled `kle_serial.py`, then each key of the resulting
12-slot aligned `labels` array is inspected:

```python
for key in kb.keys:
    key.row = key.col = None
    key.encoder_idx = key.encoder_dir = None
    if key.labels[4] == "e":
        idx, direction = key.labels[0].split(",")
        ...
        self.encoders.append(key)
    elif key.decal or (key.labels[0] and "," in key.labels[0]):
        row, col = 0, 0
        if key.labels[0] and "," in key.labels[0]:
            row, col = key.labels[0].split(",")
            row, col = int(row), int(col)
        key.row = row
        key.col = col
        self.rowcol[(row, col)] = True
        self.keys.append(key)

    # bottom right corner determines layout index and option in this layout
    key.layout_index = -1
    key.layout_option = -1
    if key.labels[8]:
        idx, opt = key.labels[8].split(",")
        key.layout_index, key.layout_option = int(idx), int(opt)
```

Key facts:

- **`labels[0]` (top-left)**: `"row,col"` matrix position. `labels[4] == "e"` (center) marks an encoder.
- **`labels[8]` (bottom-right)**: `"layout_index,layout_option"` -- the option suffix.
- With KLE default alignment `a=4`, the raw KLE label string is split on `\\n` and
  remapped via `labelMap[4] = [0, 6, 2, 8, 10, -1, 3, 5, 1, 4, 7, -1]` in
  `kle_serial.py::reorderLabelsIn`. So in the raw KLE JSON legend string
  `"row,col\\n\\n\\nlayout_index,layout_option"`, raw split index **3** maps to
  aligned `labels[8]`. This is the standard VIA convention.
- Keys with no `labels[8]` get `layout_index = layout_option = -1` (always-visible
  common keys).
- Decals participate: a decal without a matrix label still gets row=col=0, is added to
  `self.keys`, and can carry a `labels[8]` option suffix.

---

## 2. THE CRITICAL PART: show/hide and re-anchoring of option keys

This lives in `KeyboardWidget` in `src/main/python/widgets/keyboard_widget.py`.

### Splitting keys into common vs. per-layout (`add_keys`, lines 288-295)

```python
def add_keys(self, keys):
    scale_factor = self.fontMetrics().height()

    for key, cls in keys:
        if key.layout_index == -1:
            self.common_widgets.append(cls(key, scale_factor))
        else:
            self.widgets_for_layout.append(cls(key, scale_factor))
```

### Filtering + translation -- `place_widgets()` (lines 297-338, quoted verbatim)

```python
def place_widgets(self):
    scale_factor = self.fontMetrics().height()

    self.widgets = []

    # place common widgets, that is, ones which are always displayed and require no extra transforms
    for widget in self.common_widgets:
        widget.update_position(scale_factor)
        self.widgets.append(widget)

    # top-left position for specific layout
    layout_x = defaultdict(lambda: defaultdict(lambda: 1e6))
    layout_y = defaultdict(lambda: defaultdict(lambda: 1e6))

    # determine top-left position for every layout option
    for widget in self.widgets_for_layout:
        widget.update_position(scale_factor)
        idx, opt = widget.desc.layout_index, widget.desc.layout_option
        p = widget.polygon.boundingRect().topLeft()
        layout_x[idx][opt] = min(layout_x[idx][opt], p.x())
        layout_y[idx][opt] = min(layout_y[idx][opt], p.y())

    # obtain widgets for all layout options now that we know how to shift them
    for widget in self.widgets_for_layout:
        idx, opt = widget.desc.layout_index, widget.desc.layout_option
        if opt == self.layout_editor.get_choice(idx):
            shift_x = layout_x[idx][opt] - layout_x[idx][0]
            shift_y = layout_y[idx][opt] - layout_y[idx][0]
            widget.update_position(scale_factor, -shift_x, -shift_y)
            self.widgets.append(widget)

    # at this point some widgets on left side might be cutoff, or there may be too much empty space
    # calculate top left position of visible widgets and shift everything around
    top_x = top_y = 1e6
    for widget in self.widgets:
        if not widget.desc.decal:
            p = widget.polygon.boundingRect().topLeft()
            top_x = min(top_x, p.x())
            top_y = min(top_y, p.y())
    for widget in self.widgets:
        widget.update_position(widget.scale, widget.shift_x - top_x + self.padding,
                               widget.shift_y - top_y + self.padding)
```

And `update_layout()` afterwards drops decals from the drawn set (lines 340-347):

```python
def update_layout(self):
    """ Updates self.widgets for the currently active layout """
    self.place_widgets()
    self.widgets = list(filter(lambda w: not w.desc.decal, self.widgets))
    self.widgets.sort(key=lambda w: (w.y, w.x))
    ...
```

### What this means

1. **SHOW/HIDE**: For each layout index `idx`, only widgets whose
   `layout_option == layout_editor.get_choice(idx)` are shown. All other option
   groups are simply not appended to `self.widgets` -- hidden entirely.
   Common keys (`layout_index == -1`) are always shown.

2. **RE-ANCHORING -- yes, the GUI MOVES the selected option group.** For every
   `(layout_index, option)` pair, the GUI computes the **collective bounding-box
   top-left** of the whole option group (min x / min y over all keys rotated-polygon
   bounding rects). The selected option group is then translated by
   `-(topleft(opt) - topleft(opt0))`, i.e. **the selected group bounding-box
   top-left is snapped to option 0 group bounding-box top-left**. This is a pure
   rigid translation (bounding-box delta) -- no scaling, no rotation change; the
   shift is applied uniformly to every key in the group, and in the paint transform
   `qp.translate(key.shift_x, key.shift_y)` happens *before* the key rotation, so
   rotated keys move as a rigid group too.

3. Option 0 keys always draw exactly where the KLE places them (their shift is
   `layout_x[idx][0] - layout_x[idx][0] = 0`).

4. Finally the entire visible set is re-normalized so its top-left lands at
   `(padding, padding)`. Absolute KLE coordinates never matter for the final render;
   only relative geometry does.

5. **Edge case**: `layout_x[idx][opt]` defaults to `1e6`. If a layout index has NO
   keys labelled option 0, the anchor is garbage (1e6) and the selected group is
   shifted off-screen. **Every layout index must have an option-0 group** in the
   main layout.

6. **Decals**: decal keys DO contribute to the per-option `layout_x/layout_y` min
   (they are in `widgets_for_layout` when labelled) but are excluded from final
   normalization and from drawing. A labelled decal can therefore deliberately
   extend an option group bounding box to control the anchor (known VIA trick).

---

## 3. Conclusion: geometric constraints for generated alternative keys

**Alternative option keys can be placed anywhere in the KLE keymap -- the GUI
re-anchors them.** They do NOT need to be pre-positioned to overlay the default
keys. The universal VIA/Vial convention of drawing alt groups off to the side /
below the main layout works precisely because of the bounding-box-delta translation
in `place_widgets()`.

Hard requirements for generated alt keys:

1. **Option 0 (default) keys must sit in their real position within the main
   layout** (they render in place, unshifted), and every `layout_index` used must
   have at least one key with option `0` (otherwise the 1e6 default anchor breaks
   rendering).
2. **Internal geometry of each alt group must be self-consistent.** Only ONE rigid
   translation is applied per (index, option) group; relative x/y/w/h/rotation of
   keys *within* the group must already be exactly what should appear on the board.
3. **The anchor is the group collective bounding-box top-left**, not any particular
   key. The alt group bbox top-left gets mapped onto the option-0 group bbox
   top-left. Therefore:
   - Same-footprint groups (e.g. split backspace vs 2u backspace, both spanning the
     same 2u x 1u region) overlay perfectly.
   - If the alt group bbox shape differs, top-left corners align and the group
     extends right/down from there; the generator must position keys relative to
     the group own bbox top-left exactly as they should sit relative to the
     default group bbox top-left.
   - If an alt option needs to render offset from the default top-left (rare, e.g.
     ISO enter overlapping two rows), pad the group bbox with a labelled decal key
     to move the effective anchor.
4. Absolute placement of alt groups in the KLE (below the board, off to the right,
   any y offset) is purely cosmetic for the vial.json author; any location works.
5. Rotation is fine: bounding boxes are computed AFTER the rotation transform, and
   the group shift is a rigid translation of the already-rotated keys.

**Practical generator rule:** emit the default (option 0) choice in-place in the
main layout; emit each alternative choice as a compact block anywhere convenient
(e.g. a row below the board), preserving intra-block relative geometry, arranged so
the block bounding-box top-left corresponds to the default block bounding-box
top-left.

---

## 4. How the option bitfield packs

From `src/main/python/editor/layout_editor.py`. In `layouts.labels` of vial.json, a
plain string entry -> checkbox (`BooleanChoice`); a list `[label, opt0, opt1, ...]`
-> combo (`SelectChoice`).

```python
class BooleanChoice:
    def pack(self):
        return str(int(self.choice))          # exactly 1 bit

class SelectChoice:
    def pack(self):
        val = bin(self.choice)[2:]
        val = "0" * ((len(self.options) - 1).bit_length() - len(val)) + val
        return val                            # (n_options - 1).bit_length() bits
```

```python
def pack(self):
    if not self.choices:
        return 0
    val = ""
    for choice in self.choices:
        val += choice.pack()
    return int(val, 2)

def unpack(self, value):
    # we operate on bit strings
    value = "0" * 100 + bin(value)[2:]
    # VIA stores option choices backwards, we need to parse the input in reverse
    for choice in self.choices[::-1]:
        sz = len(choice.pack())
        choice.unpack(value[-sz:])
        value = value[:-sz]
```

- Per-choice bit strings are **concatenated in `labels` order**: first label occupies
  the most-significant bits, last label the least-significant bits. (The comment
  "VIA stores option choices backwards" refers to this LSB = last label layout,
  hence the reversed parse.)
- Checkbox = 1 bit; combo with N options = `(N-1).bit_length()` bits (2 opts -> 1
  bit, 3-4 -> 2 bits, 5-8 -> 3 bits), value = selected option index, big-endian
  within its field.
- The packed value is a **big-endian uint32** on the wire:
  `keyboard_comm.py::set_layout_options` does
  `struct.pack(">BBI", CMD_VIA_SET_KEYBOARD_VALUE, VIA_LAYOUT_OPTIONS, options)`
  and `reload_keymap()` reads it back with `struct.unpack(">I", data[2:6])`.
- The renderer queries the current selection per index via
  `LayoutEditor.get_choice(index)` = `int(self.choices[index].pack(), 2)`.

---

## 5. VIA (original) behavior

Not fetched in depth. Vial is a direct re-implementation of VIA conventions: VIA
(the-via/app) uses the identical KLE legend format
(`row,col\\n...\\nlayoutIndex,layoutOption` in the bottom-right legend slot), shows
only keys matching the selected option, and likewise translates non-default option
groups onto the default group origin -- VIA docs instruct authors to draw
alternative layout choices *outside* the main layout, which only works with such
re-anchoring. The Vial `unpack` comment ("VIA stores option choices backwards")
confirms bitfield compatibility with VIA firmware-side EEPROM layout-options
storage.
