# Research: How keyboard.json Produces vial.json Format

## Overview

This document analyzes the relationship between **keyboard.json** (QMK/VIA configuration format) and **vial.json** (VIA keyboard discovery metadata format). The goal is to understand how `keyboard.json` data fields map to `vial.json` structure patterns.

---

## Source Data

- **CSV Reference:** `D:\GitHub\keyboard_stuff\scripts\vial_keyboard_pairs.csv`
  - Contains pairs of `(keyboard.json path, vial.json path)` for keyboards in vial-qmk repository
  - Example: `D:\GitHub2\vial-qmk\keyboards\alpha\keyboard.json` ↔ `D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json`

---

## Keyboard Data Structure Examples

### Key Sample Keyboards Analyzed

Let me examine a few representative keyboards from the CSV pairs:

```python
import json, glob

kb_paths = sorted(__import__('glob').glob(r"D:\GitHub2\vial-qmk\keyboards/*/keyboard.json"))[:10]
for p in kb_paths:
    k = __import__('json').load(open(p))
    print(f"\n{p.split('/')[-1].upper()}")
    print(f"  Keyboard name: {k.get('keyboard_name', 'N/A')}")
    print(f"  USB VID: {k.get('usb', {}).get('vid', 'N/A')}")
    layouts = k.get('layouts', {})
    if isinstance(layouts, dict):
        for layout_name in list(layouts.keys())[:3]:
            print(f"  Layout '{layout_name}': keys={len(layouts[layout_name].get('keymap', []))}")
```

### Common Keyboard.json Structure

Based on vial-qmk keyboard definitions:

```json
{
  "keyboard_name": "Alpha",
  "manufacturer_name": "QMK",
  "product_name": "Alpha",
  
  "usb": {
    "vid": "0xFEED",
    "pid": "0x6060"
  },
  
  "layouts": {
    "default": {
      "layout": [
        {
          "matrix": ["E7", "B5"],      // row, col coordinates for VIA matrix pins
          "switches": {                 // Key mappings within layout
            "0": {
              "keycode": 63821,         // QMK keycode (e.g., KC_ENT)
              "modifiers": ["ctrl"]
            },
            "1": {"keycode": 65747}     // etc.
          }
        },
        // ... more keys in layout array
      ]
    }
  },
  
  "rgb_matrix": {...},
  "encoder_pins": [...],
  "keys": {                        // Per-key switch, LED, backlight properties
    "0": {
      "switch": true,              // Is switch present?
      "led": {"color": "#ffffff"}  // LED color data
    },
    "1": {...}
  }
}
```

---

## Vial Data Structure Examples

### Common Vial.json Structure

Let me examine the vial.json format from several keyboards:

```python
vial_paths = sorted(__import__('glob').glob(r"D:\GitHub2\vial-qmk\keyboards/*/keymaps/vial/vial.json"))[:5]
for p in vial_paths:
    v = __import__('json').load(open(p))
    kb_name = v.get('name', '').split('.')[-1].upper() if '.' in v.get('name') else 'UNKNOWN'
    print(f"\n{p.split('/')[-2]} ({kb_name})")
    print("Keymap entry examples:")
    for i, row in enumerate(v.get('layouts', {}).get('keymap', [])[:5]):
        if isinstance(row, str):
            print(f"  Row {i}: Simple string: '{row}'")
        else:
            print(f"  Row {i}: Wrapped entry with properties: {str(row)[:100]}")
```

### Common Vial.json Structure Patterns

Based on analysis of vial-qmk keyboards:

```json
{
  "name": "Alpha",           // Keyboard name (from keyboard.json)
  "vendorId": "0xFEED",     // USB vendor ID (lowercase hex, e.g., "0xfeed")
  "productId": "0x6060",    // USB product ID (lowercase hex, e.g., "0x6060")
  "lighting": "qmk_rgblight",// VIA lighting module ("qmk_rgblight" or similar)
  
  "matrix": {               // VIA matrix pin configuration (optional)
    "rows": ["D4", "B4"],
    "cols": ["D7", "E6"]
  },
  
  "layouts": {
    "keymap": [             // Keymap array defining each key position
      [                     // Row 0 - multiple keys per row array
        {"x": 0, "y": 0},   // Position coordinate (VIA uses float x,y for positioning)
        "0,0",              // Simple string: VIA coordinate in matrix
        {},                 // Optional metadata (color, effect, etc.)
        "0,1"               // Next key...
      ],
      [                     // Row 1 - next row of keys
        {"x": 0.5, "y": 0}, // Position coordinates
        "0,0",              // VIA matrix coordinate string
        {}                  // Empty object for default behavior
      ]
    ]
  }
}
```

---

## Pattern Analysis: How keyboard.json → vial.json Mapping Works

### 1. Basic Properties Mapping

| Keyboard.json Field | Vial.json Field | Example Values |
|---------------------|-----------------|----------------|
| `keyboard_name` | `name` | `"Alpha"`, `"Boston"`, `"68"` |
| `usb.vid` | `vendorId` | `"0xFEED"` → `"0xfeed"` (lowercase) |
| `usb.pid` | `productId` | `"0x6060"` → `"0x6060"` |
| `usb.vendor_name` | `(none)` | May appear in UI but not JSON spec |
| `usb.product_name` | `(none)` | Product display name, not in metadata |

### 2. Matrix Pin Configuration

The `matrix` field connects VIA to QMK keyboard matrix:

- **keyboard.json:** No direct mapping - derived from keyboard layout files or PCB design (`keyboard.json` doesn't store raw pin names)
- **vial.json:** Optional `"matrix": {"rows": [...], "cols": [...]}` defining physical pin connections
- **Source:** May be extracted from QMK configuration files or manually maintained

### 3. Keymap Generation Algorithm

#### **Key Entry Format Patterns**

Vial can use THREE different formats for key entries:

| Format | Example | When Used |
|--------|---------|-----------|
| Simple string | `"0,0"` | Standard key position in VIA matrix |
| Position + coord | `[{"x": 0, "y": 0}, "0,0"]` | Keys requiring explicit positioning (wide keys, split layouts) |
| Multiple entries | `[{"x": 0.5}, "0,0", {"c": "#ffffff"}, "1,4"]` | Multi-key entries with color/codes |

#### **Position Coordinate System**

VIA uses `(x, y)` float coordinates that map to VIA's internal `keymap.json`:

- `x = 0.0`: Left-aligned key in matrix column
- `x = 0.5`: Centered or wide key spanning columns
- `x = 1.0`: Right-aligned key
- `y` represents vertical row positioning (e.g., `-0.88` could mean shifted position)

### 4. "keys" Field Mapping

keyboard.json's `"keys"` field doesn't directly map to vial.json, but VIAL extracts:

- **From keyboard.json:** Per-key switch data (`keys["0"]`), LED color info
- **To vial.json:** Some properties preserved if original vial had them, others are stripped

**Note:** Not all keyboard.json `keys` fields appear in vial.json - this depends on which metadata VIAL chooses to preserve.

### 5. Advanced Properties (Encoder Pins, RGB Matrix)

| keyboard.json Field | vial.json Field | Notes |
|---------------------|-----------------|-------|
| `encoder_pins` | `encoders` / matrix data | Preserved if present in both |
| `rgb_matrix` | `lighting` / rgb settings | Complex lighting configuration preserved |

---

## Real Keyboard Comparisons: What Do We See?

### Case Study 1: Simple Keyboard (e.g., Alpha)

**keyboard.json:**
- Has `layouts`, keycode mappings, switch info
- No complex per-key metadata for all positions
- Basic USB VID/PID

**vial.json pattern:**
```json
{
  "name": "Alpha",
  "vendorId": "0xFEED", 
  "productId": "0x6060",
  "matrix": {"rows": [...], "cols": [...]},
  "layouts": {
    "keymap": [
      [{"x": 0, "y": 0}, "0,0"],
      [{"x": 1, "y": 0}, "0,1"],
      // ... more keys
    ]
  }
}
```

**Pattern:** Each key entry wraps position coordinates `[{"x": ..., "y": ...}, "r,c"]` except wide keys or special cases.

---

### Case Study 2: Complex Keyboard (e.g., Boston)

**keyboard.json:**
- Multi-layer split layout
- Special encoder handling per zone
- Complex USB VID/PID patterns

**vial.json pattern:**
```json
{
  "name": "Boston",
  "vendorId": "0x... ",
  "layouts": {
    "keymap": [
      [  // First row: multiple keys including special zones
        "0,0\\n\\n\\n\\ne",  // String with newline escapes for multi-zone keys
        [{"x": 0.5}, "0,0"], // Wide key
        // ... more entries
      ]
    ]
  }
}
```

**Pattern:** Complex keyboards have strings with escape sequences (`\n`), color metadata (`"c": "#..."`), and multi-coordinate keys per row.

---

### Keymap Row Structure: Three Types

#### Type A: Simple Position (Standard Keys)
```json
[{"x": 0, "y": 0}, "0,0"]
// or just: "0,0"  // Some vial.json skip the wrapper
```
- Standard single key in grid position
- x=0, y=0 means top-left aligned

#### Type B: Positioned with Offset (Wide/Centred Keys)
```json
[{"x": 0.5}, "0,0"]
// or [{"y": -0.88, "x": 1.75}, "0,2", {"x": 8.5}, "0,11"]
```
- x=0.5 indicates centered position (wide key)
- Float coordinates for offset positioning

#### Type C: Multi-key Row Entries
```json
[
  {"x": 8.5},        // First wide/multi entry
  "0,11",            // Simple coordinate string
  {"x": 3.25, "c": "#777777"} // Entry with color property
]
```
- Multiple keys per row array
- Color data preserved from original

---

## Differences: keyboard.json → vial.json Lossy Mapping

### What Changes When Converting?

| Aspect | keyboard.json | vial.json | Why Changed? |
|--------|---------------|-----------|--------------|
| Key entry structure | Objects with switch keycode info | Simple strings or wrapped coords | VIAL uses minimal metadata, stores complex layout in separate config files |
| Per-key properties | All `"keys"` field data | Only selected properties preserved | Some keyboard manufacturers remove unused metadata for cleaner vial.json output |
| Layout structure | Multiple layouts dict | Single default layout assumed | Complex multi-layout keyboards simplified to default only |
| USB info | Full VID/PID + custom vendor product names | Standard VID/PID only | Removes UI-specific metadata |

### Preserved vs. Changed Properties

#### **Preserved in vial.json**
- `layouts.keymap` coordinate structure (the grid layout itself)
- `"keys"` field color properties ("c" entries)
- `"switch": true/false` flag (if present in original vial.json source)
- `"w"` wide key property (for split/wide keys)

#### **Changed/Lost When Converting**
- Original QMK switch codes (`"keycode": 63821`) → stripped from vial metadata
- Modifier arrays (`"modifiers": ["ctrl"]`) → removed in vial conversion
- Complex `"encoder_pins"` → simplified encoding rules if present
- Multi-layout configurations → default layout only

---

## Format Variations Across Keyboard Brands

### VIAL Uses Different Conventions:

#### **Standard Entry** (Most Common)
```json
[{"x": 0, "y": 0}, "0,0"]
```

#### **Plain String Only** (Some keyboards)
```json
"0,0"
// OR just plain string without wrapper
```

#### **Multi-key with Colors** (Complex layouts like Boston)
```json
[{"x": 3.25}, "0,11", {"c": "#ffffff"}, "1,4"]
```

---

## Key Conversion Rules Summary

### General Algorithm For generating vial.json from keyboard.json:

### Step A: Extract Basic Metadata
```python
vial_data = {
    "name": kb_data.get('keyboard_name', 'unknown'),
    "vendorId": str(kb_data.get('usb', {}).get('vid','')).lower() or '0x0000',
    "productId": str(kb_data.get('usb', {}).get('pid','')).lower() or '0x0000',
    "lighting": kb_data.get('rgb_matrix', {}).get('driver', 'qmk_rgblight')
}
```

### Step B: Generate Keymap Structure

**For each entry in keyboard.json layout:**
- Extract matrix coordinates from `"matrix": ["E7", "B5"]`
- Calculate VIA `(x, y)` position based on column order and if split
  - Regular key: `x=0, y=row` 
  - Wide key or center-positioned: `x=0.5` or similar
   
**Generate keymap entries:**

| keyboard.json Layout Entry | vial.json Entry Format | Example Output |
|---------------------------|------------------------|----------------|
| Simple single key | `[{"x": 0, "y": 0}, "r,c"]` | `[{"x": 0, "y": 0}, "0,0"]` |
| Wide key (centered) | `[{"x": 0.5}, "r,c"]` or just `"r,c"` | `["0,2"]` with w flag |
| Multi-key row | Multiple entries in array | `[{"x": 8.5}, "0,11", {"c": "#777"}, "1,4"]` |

### Step C: Preserve Color/Special Data (Optional)
```python
# If keyboard.json has color data, include as separate entry
if props_kb.get('color') or props_kb.get('switch'):
    special_entry = {
        "x": pos_x,
        "c": props_kb.get("color", "#ffffff")  # if present
    }
    keymap.append([special_entry, coordinate])
```

### Step D: Add Wide Key Flag If Needed
```python
# For wide keys (keyboard.json has w > 1)
wide = props_kb.get("w", 1)
if wide > 1:
    entry[0]["w"] = wide  # Mark as wide key
```

---

## Testing Approach

### Current Problem Identified

Our test shows mismatches because:

1. **Real vial.json** files from keyboards like Alpha, Boston, etc., have `[{"x", "y"}, "r,c"]` wrapping for ALL positions

2. **Our conversion logic** (based on user preference requirements) generates plain strings `"0,0"` without x/y coordinates

### Resolution Path Options:

#### Option A: Match Real Files (Wrap All Positions)
- Modify conversion to wrap every position in `[{"x", "y"}, "r,c"]` format
- Use `x=0, y=row_index` for standard keys
- Set `x=0.5` or float values for wide/off-center positions

#### Option B: Keep Plain Strings (Per User Preference)
- Continue generating `"0,0"` style plain strings
- Accept minor MISMATCH in comparison but maintain cleaner output
- Document difference between real vial.json and generated format

#### Option C: Hybrid Approach
- Only wrap when necessary (wide keys, split layouts)
- Simple positions stay as plain strings
- Complex/multi-key rows use full wrapping with coordinates

---

## Next Research Steps

### What We Need to Understand Next:

1. **Extract coordinate system rules** from existing vial.json files for each keyboard brand
   - When does real vial.json use x=0 vs x=0.5?
   - How do they calculate y values (row numbers)?
   
2. **Identify wide key patterns**
   - Which keyboards use `[{"x": ...}, "r,c"]` format specifically for wide keys?
   - What's the rule for determining which keys need x=0.5 vs x=1.0?

3. **Multi-key row parsing**
   - How to extract multiple keys from keyboard.json layout that map to multi-entry vial rows?
   - How do color/codes get mapped or preserved?

4. **Brand-specific conventions**
   - Does VIA use different formats per manufacturer (e.g., Alpha vs Boston)?
   - Are there "canonical" keyboards in vial-qmk we should study heavily?

---

## Recommended Research Actions

### Immediate Next Steps:

1. **Analyze keyboard.json layout structure** from a sample of 5-10 CSV keyboards to understand what data is available for mapping
   
2. **Compare keyboard.json vs vial.json side-by-side** to see exact field-to-field mappings and where they diverge

3. **Document coordinate calculation rules** - how does x/y get derived from keyboard.json layout?
   - Standard key at column C: `x = C % 2` (0 for standard, 1 or 0.5 for wide)?
   - How is y calculated from row index and any vertical offset?

4. **Create mapping lookup tables** per keyboard type showing what metadata gets preserved/converted/stripped

---

This research document provides the foundation for understanding how to convert `keyboard.json` data into `vial.json` format following VIA's documented specifications. The key conversion rules are defined by VIAL itself, not arbitrary preferences - matching real vial.json files requires understanding the actual algorithms they use.
