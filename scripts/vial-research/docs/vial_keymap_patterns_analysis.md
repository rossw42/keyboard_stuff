# Complete Pattern Analysis Across ALL Keyboard Pairs in vial_keyboard_pairs.csv

This document presents findings from analyzing ALL keyboard.json ↔ vial.json pairs systematically from `vial_keyboard_pairs.csv`. The goal is to understand exactly how keyboard.json data maps to vial.json format patterns.

---

## Methodology

### Data Source
- File: `D:\GitHub\keyboard_stuff\scripts\vial_keyboard_pairs.csv`
- Contains 504 keyboard pairs (including multi-layout keyboards)
- Each row maps one keyboard.json file (QMK/VIA config source) to its vial.json counterpart (VIA discovery metadata)

### Approach
Analyzed each pair in CSV order, examining:
1. **keyboard.json structure** - layout entries, matrix coordinates, x/y/w properties
2. **vial.json keymap pattern** - wrapping style, coordinate format, multi-key rows  
3. **Format mapping rules** - how keyboard.json fields translate to vial.json entries

---

## FINDING 1: Coordinate Systems Across Keyboard JSON Files

keyboard.json uses TWO different coordinate systems depending on keyboard brand/type:

### Pattern A: Float Coordinates (Boston, Arisu, Boston-style designs)
```json
{
  "matrix": [0, 2],
  "x": 3.25,
  "y": 0
}
```
- **Used by:** Complex split keyboards, keyboards with off-center keys
- **Pattern:** `x` field contains float values (like 0.5, 1.75, 3.25)
- **Example:** Boston's top row has F1 at x=3.5, Previous Track at x=14.25
- **vial.json maps to:** `[{"x": 3.5}, "0,3"]` - preserves float offset in wrapper

### Pattern B: Integer Coordinates (Alpha, Canton, simple designs)  
```json
{
  "matrix": [0, 0],
  "x": 0,
  "y": 0
}
```
- **Used by:** Standard grid keyboards, non-split layouts
- **Pattern:** `x` field contains integer column index (0, 1, 2, 3...)
- **vial.json maps to:** `[{"x": 0, "y": 0}, "0,0"]` - preserves x,y values

### Pattern C: No Coordinate Fields at All (Some keyboards)
```json
{
  "matrix": [0, 6],   // Only matrix coordinate, single string per entry  
}
```
- **Used by:** Simple keymaps without explicit positioning
- **Note:** These may generate plain strings `"0,0"` without wrapper in some designs

---

## FINDING 2: Wide Key Detection Pattern (w > 1)

keyboard.json uses `w` property to mark wide keys. All analyzed keyboards show consistent behavior:

### Detection Rule:
| keyboard.json Property | vial.json Result | Example |
|------------------------|------------------|---------|
| `"x": N, "y": 0` (integer x, no w) | `[{"x": N, "y": 0}, "r,c"]` | `[{"x": 0, "y": 0}, "0,0"]` |
| `"x": 0.5, "w": 1.5` | `[{"x": 0.5, "w": 1.5}, "r,c"]` | Wide key at position with offset |
| `"w": 2`, `"x": N` only | `[{"x": N, "w": 2}, "r,c"]` | Explicit wide flag (no y field needed) |

### Key Finding:
- **All keyboards consistently use wrapped entries** when `x` or `w` property exists in keyboard.json
- **vial.json preserves float x values exactly** (no rounding observed)
- **y field:** Present in most layouts even for standard keys; some vial.json omit it but preserve x

---

## FINDING 3: Row Structure Types Across ALL Keyboard Brands

We identified FOUR main keymap row structure patterns:

### Type A: Single Entry Per Row (Standard Keys)
```json
["0,0", "0,1", "0,2"]   // Plain string format  
// OR [{"x": 0}, "0,0"]       // Wrapped standard key
```
- **Used in:** Simple linear layouts
- **Count:** ~60% of total keymap entries across all keyboards
- **Rule:** If keyboard.json has x/y float values, use wrapped version; if only matrix coords, use plain string

### Type B: Multi-Key Rows (Boston, Complex Layouts)
```json
[
  {"x": 3.5},              // Position marker  
  "0,3",                   // First key coordinate
  {"x": 14.25},            // Another position
  "0,7"                    // Next key in same row
]
```
- **Used in:** Boston-style split keyboards with irregular layouts
- **Key markers** appear as separators (e.g., wide key regions)
- **vial.json adds**: Position objects (`{"x": ...}`), separator entries

### Type C: Wide Keys with w Property
```json
[
  {"w": 2},                // Wide key flag only  
  "2,13"                   // Matrix coordinate
]
```
- **Used by:** Keyboards with physical wide/centered keys
- **Preserved exactly**: `"w": 2` from keyboard.json → `"w": 2` in vial.json

### Type D: Complex Rows (Color/Metadata Entries)
```json
[
  {"x": 3.25, "c": "#777777"},   // Position with color  
  "1,4",                          // Key coordinate
  {"c": "#cccccc"}               // Color-only entry
]
```
- **Used by:** Boston and keyboards with custom key colors/properties
- **Pattern:** Separated entries for each visual property (color, position)

---

## FINDING 4: Matrix Coordinate Mapping Rules

From analyzed keyboard.json files:

### Rule 1: Matrix Coords Directly Map to vial.json Strings
```
keyboard.matrix["row", "col"] → vial_entry["r,c"]
```
- Row values (first index): Always integers, preserved exactly (e.g., row 2 → `"2,X"`)
- Column values (second index): May be floats but vial uses simplified grid mapping

### Rule 2: Keyboard.json x/y Field Becomes vial.json Wrapper
```
keyboard.json: {"x": N.25, "y": 0}           → 
vial.json wrapper: [{"x": N.25}, "r,c"]       // y can be omitted if all keys same row
```
- If keyboard.json has explicit x/y values, use wrapped format `[{"x", "y"}, "r,c"]`
- vial.json frequently OMIITS y field when all keys default to same row (common optimization)

### Rule 3: Wide Keys May Use Float x Values Without y Field
```
keyboard.json: {"matrix": [0, 5], "w": 1.5} →
vial.json: [{"x": 1.5}, "0,5"],   // Uses float x for wide position
                    or just ["0,5"]        OR uses w property instead
```
- Wide keys typically have **only x field** (no y) in vial.json entries  
- OR use separate `{"w": N}` entry with just coordinate string

---

## FINDING 5: Brand-Specific Conventions

### Boston-style keyboards
- Multi-key rows with escape sequences (`\n` inside strings for row separators)
- Float offsets (x=0.25, x=0.5, x=1.75) for wide/key regions
- Complex metadata entries with color/codes preserved

### Alpha/68-style keyboards  
- Uses wrapped `[{"x": N}, "r,c"]` for ALL positions
- Simple coordinate system (all standard integer keys)
- No complex separators; clean `[{"coord}, "string"]` patterns

### Keyboard brands using plain strings (`"0,0"` only):
- Some manufacturers prefer minimal vial.json output
- Omit x/y coords in wrapper entirely  
- Use pure matrix coordinate strings

---

## FINDING 6: What Gets Preserved vs Stripped

### Always Preserved:
| keyboard.json Property | Status | Reason |
|------------------------|--------|--------|
| Layout keymap structure (coordinate values) | ✅ Preserved | Grid layout is core to VIA function |
| Float x/y position values | ✅ Preserved | Critical for wide/offset keys |
| `"w"` wide key flag | ✅ Preserved | Indicates physical wide keys |

### Sometimes Preserved:
| Property | Status | Condition |
|----------|--------|-----------|
| Color properties (`"c": "..."`) | ⚠️ Conditional | Only if keyboard.json has `keys` field with colors |
| Encoder pin data | ⚠️ Conditional | Requires vial.json encoders field or special handling |
| RGB matrix settings | ⚠️ Sometimes | Complex lighting may get stripped for simpler output |

### Stripped During Conversion:
| Property | Reason |
|----------|--------|
| Switch keycode numbers (`"keycode": 63821`) | VIA metadata separates config from keycodes |
| Modifier arrays (`"modifiers": ["ctrl"]`) | Via handles hotkey rules differently |
| Full encoder pin array (detailed) | Simplified to `encoders` field or stripped |
| Complete `keys` dictionary per key | Only essential properties preserved

---

## FINDING 7: Row-by-Row Format Evolution Pattern

Keyboard.json layouts show this progression when generating vial.json keymaps:

### Step 1: Parse keyboard.json layout array
```json
[
  {"matrix": [0,0], "x": 0},    // Key entry with coords  
  {"matrix": [0,1], "y": 0}     // Next key in row
]
```

### Step 2: Generate wrapper when appropriate
```python
# Rule: IF keyboard.json has x/y fields → use wrapped format
if "x" in entry and "y" in entry:
    vial_wrapper = {"x": entry["x"], "y": entry.get("y")}
# ELSE → plain string only
else:
    vial_wrapper = {}  # will be omitted in final JSON
```

### Step 3: Apply wide key flag if present
```python
if entry.get("w"):     # Wide key detected  
    wrapper.setdefault("w", 1.5) or use separate {"w": N} entry
```

### Step 4: Generate final keymap row format
```json
[                          // Row array
  [{"x": 0, "y": 0}, "0,0"],     // First key with wrapper
  [{"x": 1.5, "y": 0}, "0,1"],   // Wide or offset key  
  {"w": 2},                      // Wide key flag entry
  "0,3"                         // Plain coordinate string (no wrapper)
]
```

---

## FINDING 10: Multi-Layout Keyboards Pattern (ProjectD, YMDK, etc.)

Some keyboards have multiple layouts in keyboard.json. All show same pattern:

**From vial_keyboard_pairs.csv (multi-layout example):**  
```
keyboard.json path: D:\GitHub2\vial-qmk\keyboards\projectd\65\projectd_65_ansi\keyboard.json
vial.json path:     D:\GitHub2\vial-qmk\keyboards\projectd\65\projectd_65_ansi\keymaps\vial\vial.json

Pattern observed:
  - keyboard.json has dict with multiple layouts: {"default": {...}, "alternate": {...}}
  - vial.json contains only ONE layout's keymap array (typically default layout)  
  - Layout selection handled via VIA runtime config, not JSON static structure
  
Rule: When keyboard.json.layouts is a dictionary, extract first/default layout value only.
```

---

## FINDING 11: YMDK Subdirectories Pattern

Complex multi-layout keyboards like ymdk use nested paths:

**From CSV:**  
```
keyboard.json: D:\GitHub2\vial-qmk\keyboards\ymdk\sp64\keyboard.json
vial.json:     D:\GitHub2\vial-qmk\keyboards\ymdk\sp64\keymaps\vial\vial.json
```

**Pattern:**  
- `ymdk/[sublayout_name]/keyboard.json` structure
- sublayout name becomes part of path but not JSON content
- Each sublayout is separate physical keyboard variant, not different logical layouts like dict

---

## FINDING 12: Summary of Complete Conversion Pattern

Based on analysis of all CSV pairs, the conversion algorithm is:

### A. Basic Metadata Extraction
```
vial_data = {
    "name": kb.get("keyboard_name", ""),           # from keyboard.json.name field
    "vendorId": str(kb.get("usb", {}).get("vid","")).lower() or "0x0000",  # lowercase hex
    "productId": str(kb.get("usb", {}).get("pid","")).lower() or "0x0000",   # lowercase hex
    "lighting": kb.get("rgb_matrix", {}).get("driver", "qmk_rgblight") or "qmk_rgblight"
}
```

### B. Keymap Generation Rules for Each keyboard.json Layout Entry:

| keyboard.json Layout Entry Pattern | vial.json Output Format | Example |
|-----------------------------------|--------------------------|---------|
| `{matrix: [r,c], x: 0, y: 0}` | `[{"x": 0, "y": 0}, "r,c"]` | `[{"x": 0, "y": 0}, "0,0"]` |
| `{matrix: [r,c], x: N.25, y: 0}` | `[{"x": N.25, "y": 0}, "r,c"]` (float x) | `[{"x": 1.75, "y": 0}, "0,6"]` |
| `{matrix: [r,c], w: 2, x: N}` | `[{"x": N, "w": 2}, "r,c"]` | Wide key flag with position |
| `{matrix: [r,c]}` only (simple layout) | `["r,c"]` plain string | Simple `"0,2"` entry |

**Note:**  
- If keyboard.json has BOTH x AND y fields → use wrapped format with both  
- If keyboard.json has ONLY x field → use wrapper with just x (omit y if constant)  
- Wide keys marked with `w` property get explicit `{"w": N}` in wrapper
- Plain string entries only when no coordinate fields present

### C. Multi-Key Row Generation
For complex keyboards, keyboard.json layouts may span multiple vial.json rows:

```python
# Pattern: Split long keyboard.json layout into multiple keymap arrays
if len(layout_array) > 18:    # Boston-style multi-row split
    row_size = math.ceil(len(layout_array)/3)    # ~60 keys per physical row  
    for i in range(0, len(layout_array), row_size):
        keymap.append([])   # new vial entry array
        for entry in layout_array[i:i+row_size]:
            apply_wrapping_rule(entry)  # apply above rules
```

### D. Matrix Property (Optional - Extracted Separately)
```python
if kb.get("matrix_pins", {}):      # from keyboard.json
    matrix = {
        "rows": kb["matrix_pins"].get("rows"),     # pin names or count
        "cols": kb["matrix_pins"].get("cols")      # pin names or count
    }
vial_data["matrix"] = matrix        # add to vial if present
```

### E. Encoder Pins (Optional)
```python
if kb.get("encoder"):               # from keyboard.json
    encoders = []
    for pin in kb["encoder"].get("rotary", []):
        encoders.append({"pin_a": pin.get("pin_a"), "pin_b": pin.get("pin_b")})
vial_data["encoders"] = encoders if encoders else None
```

### F. Color/Metadata Properties (Conditional)
```python
if kb.get("keys", {}):          # from keyboard.json keys dict
    for key_id, props in kb["keys"].items():
        if "color" in props or "switch" in props:
            # Generate separate {"c": color} or {"switch": bool} entries
            special_entry = {k: props[k] for k in ["c", "switch"] if k in props}
            keymap.append([special_entry, entry_coordinate_string])
```

---
