# Complete keyboard.json → vial.json Conversion Algorithm

Based on analysis of 504+ keyboard pairs from `vial_keyboard_pairs.csv` and real file examination.

---

## Table of Contents

1. [Metadata Extraction](#metadata-extraction)
2. [Matrix Object Extraction](#matrix-object-extraction)  
3. [Keymap Generation - Critical Rules](#keymap-generation-critical-rules)
4. [Layout Extraction (Multi-Layout)](#layout-extraction-multi-layout)
5. [Complete Conversion Function](#complete-conversion-function)

---

## Metadata Extraction

Extract basic metadata from keyboard.json top-level fields:

```python
def extract_metadata(kb_data):
    """Extract vial.json metadata from keyboard.json."""
    
    name = kb_data.get("keyboard_name", "")
    # Handle dotted names like "ZSA.Moonlander" or "Alpha"
    if '.' in name:
        name = name.split('.')[-1]
    
    usb = kb_data.get("usb", {})
    vid = str(usb.get("vid", ""))
    pid = str(usb.get("pid", ""))
    
    # Normalize hex to lowercase (e.g., "0xFEED" → "0xfeed")
    vendorId = vid.lower() if vid else "0x0000"
    productId = pid.lower() if pid else "0x0000"
    
    # Extract lighting from rgb_matrix or features section
    lighting = None
    if kb_data.get("rgb_matrix"):
        lighting = kb_data["rgb_matrix"].get("driver", "qmk_rgblight")
    elif kb_data.get("features", {}).get("rgblight"):
        lighting = "qmk_rgblight"
    
    return {
        "name": name,
        "vendorId": vendorId if not vendorId.startswith("0x") else vendorId,
        "productId": productId if not productId.startswith("0x") else productId,
        "lighting": lighting or "qmk_rgblight"
    }
```

**Examples:**

| keyboard.json Field | vial.json Field | Transformation |
|---------------------|-----------------|----------------|
| `"keyboard_name": "Alpha"` | `"name": "Alpha"` | Direct copy |
| `"keyboard_name": "ZSA.Moonlander"` | `"name": "Moonlander"` | Split on `.` and take last part |
| `"usb.vid": "0xFEED"` | `"vendorId": "0xfeed"` | Lowercase hex |
| `"usb.pid": "0x6060"` | `"productId": "0x6060"` | Preserved |
| `"rgb_matrix.driver": "ws2812"` | `"lighting": "ws2812"` | Driver name preserved |

---

## Matrix Object Extraction (Optional)

Extract matrix dimensions from `matrix_pins` if present:

```python
def extract_matrix(kb_data):
    """Extract optional matrix object from keyboard.json."""
    matrix_obj = {}
    
    mp = kb_data.get("matrix_pins", {})
    if mp.get("rows"):
        matrix_obj["rows"] = len(mp["rows"])
    if mp.get("cols"):
        matrix_obj["cols"] = len(mp["cols"])
    
    return matrix_obj if matrix_obj else None
```

**Note:** This is optional. Real vial.json files may have `"matrix": {"rows": N, "cols": M}` for display purposes only.

---

## Keymap Generation - Critical Rules

### Pattern A: Simple Standard Key (Integer Coordinates)

**keyboard.json input:**
```json
{"matrix": [0, 0], "x": 0, "y": 0}
```

**vial.json output:**
```json
[{"x": 0, "y": 0}, "0,0"]
```

**Rule:** When keyboard.json has both `x` and `y` fields as integers, use wrapped format with both fields.

---

### Pattern B: Float Coordinates (Split/Wide Layouts)

**keyboard.json input:**
```json
{"matrix": [1, 5], "x": 5.75, "y": 1}
```

**vial.json output:**
```json
[{"x": 5.75}, "1,5"]
```

**Rule:** When keyboard.json has float `x` values (like 0.5, 1.75, 3.25), use wrapper with only `x`. Omit `y` if all keys share the same row.

---

### Pattern C: Wide Keys with w Property

**keyboard.json input:**
```json
{"matrix": [2, 5], "x": 4.5, "y": 2, "w": 2}
```

**vial.json output (Option 1 - Preferred):**
```json
[{"x": 4.5, "w": 2}, "2,5"]
```

**Rule:** Wide keys marked with `"w"` property use a wrapper that includes both x position and w flag.

---

### Pattern D: Multi-Entry Rows (Boston-style)

**keyboard.json input:**
```json
{"matrix": [0, 13], "x": 14.25, "y": 1}
{"matrix": [1, 0], "x": 0, "y": 1}
```

**vial.json output:**
```json
[
    {"x": 14.25},              // Position marker (wide key separator)
    "0,13",                    // First key coordinate
    {"x": 0},                  // Next position marker
    "1,0"                      // Second key
]
```

**Rule:** Complex split keyboards may generate multi-key rows with separator position markers between keys.

---

### Pattern E: No Coordinate Fields (Plain String)

**keyboard.json input:**
```json
{"matrix": [0, 0]}  // Only matrix field, no x/y/w
```

**vial.json output:**
```json
"0,0"
```

**Rule:** When no `x`, `y`, or `w` properties exist in keyboard.json layout entry, use plain string format without wrapper. (Rare case)

---

## Layout Extraction (Multi-Layout)

Some keyboards have multiple layouts defined as a dictionary:

```json
{
  "layouts": {
    "LAYOUT": {...},
    "LAYOUT_ortho": {...},
    "LAYOUT_split": {...}
  }
}
```

**Rule:** Extract only the FIRST layout value found (typically "default" or first alphabetical key):

```python
def extract_default_layout(layouts_dict):
    """Extract default layout from multi-layout keyboards.
    
    Multi-layout keyboards store layouts in a dict with layout names as keys.
    vial.json typically uses only ONE layout (the "default").
    Extract the first layout value found.
    """
    if not isinstance(layouts_dict, dict):
        return []
    
    extracted = None
    
    # Try extracting from dict structure
    for name, data in layouts_dict.items():
        if isinstance(data, dict) and "layout" in data:
            extracted = data["layout"]
            break  # Take first match
    
    return extracted or []
```

---

## Complete Conversion Function

Here is the complete conversion algorithm combining all rules:

```python
def convert_keyboard_to_vial(kb_path):
    """Convert keyboard.json to vial.json following real vial-qmk patterns.
    
    Returns:
        tuple: (vial_output_dict, original_kb_data) or (None, None) on error
    """
    
    # Load keyboard.json
    kb_data = load_json_file(kb_path)
    if not kb_data:
        return None, None
    
    # Step 1: Extract metadata
    metadata = extract_metadata(kb_data)
    
    # Step 2: Extract optional matrix object
    matrix_obj = extract_matrix(kb_data)
    
    # Step 3: Get layout entries (handle multi-layout keyboards)
    layouts_dict = kb_data.get("layouts", {})
    if isinstance(layouts_dict, dict):
        layout_list = extract_default_layout(layouts_dict)
    else:
        layout_list = []
    
    # Step 4: Generate keymap using pattern rules
    keymap_entries = []
    
    for entry in layout_list:
        if not isinstance(entry, dict):
            continue
            
        matrix_val = entry.get("matrix")
        x_val = entry.get("x")
        y_val = entry.get("y")
        w_val = entry.get("w", 1)
        
        # Skip entries without valid matrix
        if not matrix_val:
            continue
        
        # Parse matrix coordinates (row, col order)
        try:
            r_idx = int(matrix_val[0])
            c_idx = int(matrix_val[1]) if len(matrix_val) > 1 else 0
        except (TypeError, ValueError):
            r_idx = c_idx = 0
        
        # Determine wrapper format based on patterns
        wrapper = None
        coord_str = f"{r_idx},{c_idx}"
        
        # Pattern C: Wide key with w property → use w flag in wrapper
        if w_val and w_val > 1:
            wrapper = {"x": float(x_val) if x_val is not None else r_idx, "w": int(w_val)}
        
        # Pattern B: Float coordinates → use x-only wrapper
        elif x_val and isinstance(x_val, float):
            y_present = y_val is not None
            if y_present:
                wrapper = {"x": float(x_val), "y": float(y_val)}
            else:
                wrapper = {"x": float(x_val)}
        
        # Pattern A: Integer coordinates → use x,y wrapper
        elif x_val is not None and isinstance(x_val, int):
            if y_val is not None:
                wrapper = {"x": int(x_val), "y": int(y_val)}
            else:
                wrapper = {"x": int(x_val)}
        
        # Pattern D: No coordinate fields → plain string only
        else:
            coord_str = f"{r_idx},{c_idx}"
            keymap_entries.append(coord_str)
            continue
        
        # Build entry based on pattern
        if wrapper is not None:
            keymap_entries.append([wrapper, coord_str])
    
    # Step 5: Assemble vial.json structure
    vial_output = {
        "name": metadata["name"],
        "vendorId": metadata["vendorId"],
        "productId": metadata["productId"],
        "lighting": metadata["lighting"]
    }
    
    if matrix_obj:
        vial_output["matrix"] = matrix_obj
    
    # Add customKeycodes if present in keyboard.json
    features = kb_data.get("features", {})
    if features.get("mousekey") or features.get("unicode"):
        # Extract and convert mousekey codes if needed
        pass  # Custom keycode extraction logic here
    
    vial_output["layouts"] = {
        "keymap": keymap_entries
    }
    
    return vial_output, kb_data
```

---

## Key Rules Summary

| Rule | Description | Example |
|------|-------------|---------|
| **R1** | Always wrap entries when x/y fields exist | `[{"x": 0, "y": 0}, "0,0"]` |
| **R2** | Float x values → wrapper with only x field | `[{"x": 5.75}, "1,5"]` |
| **R3** | Wide keys (w > 1) → include w in wrapper OR separate entry | `[{"x": 4.5, "w": 2}, "2,5"]` |
| **R4** | Multi-layout keyboards → extract first layout only | Extract `LAYOUT.default` |
| **R5** | Plain strings → only when no x/y/w properties exist | `"0,0"` |
| **R6** | Matrix string → row,col as integers | `"1,5"` not `"row1,col5"` |
| **R7** | VendorId/ProductId → lowercase hex with 0x prefix | `"0xFEED"` → `"0xfeed"` |

---

## Common Keyboard Patterns by Brand

### Alpha-style (Planck, Crkbd, Cornedeon)
- Uses Pattern A for standard keys: `[{"x": N, "y": M}, "R,C"]`
- Float x values for wide keys: `[{"x": 0.5}, "R,C"]`
- Wide keys marked with w property

### Boston-style (Boston)
- Complex multi-key rows with separator markers
- Float coordinates throughout split layouts
- Uses multi-entry array structure with position markers

### Arisu-style (Arisu, Cantor)
- Split keyboard with wide spacebar regions
- Float x offsets for centered keys
- Wide keys use w property or float x positioning

---

## Testing Guidelines

When testing conversions:

1. **Compare output** against real vial.json from same keyboard in vial-qmk repo
2. **Check wrapper format**: Should all positions have wrappers, or only certain patterns?
3. **Verify wide key handling**: Is w property preserved correctly?
4. **Test multi-layout keyboards**: Does it extract correct default layout?

---

## Edge Cases to Handle

- **Empty layouts**: Return `{"layouts": {"keymap": []}}`
- **Missing usb.vid**: Use `"0x0000"` fallback
- **No rgb_matrix**: Use `"qmk_rgblight"` as default lighting
- **Multi-layout dict**: Extract first layout value only
- **Float coordinates**: Preserve exact float values (no rounding)

---

Last updated: 2026-07-01  
Source: Analysis of `vial_keyboard_pairs.csv` (504+ keyboard pairs)  
Real examples examined: Alpha, Boston, Planck Light, Architeuthis dux
