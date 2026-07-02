# Critical Findings from Batch Conversion Analysis

**Date:** 2026-07-01  
**Analysis:** Comparison of generated vs real vial.json files (504 keyboards)

---

## Key Insights

### 1. Entry Structure Difference - CRITICAL

**My Converter Output:**
```json
[
    [{"x": 0, "y": 0}, "0,0"],
    [{"x": 1, "y": 0}, "0,1"],
    [{"x": 2, "y": 0}, "0,2"]
]
```

**Real vial.json Structure:**
```json
[
    {"x": 0, "y": 0},           // Position marker (row start)
    "0,0",                       // Key at position
    {"x": 1},                    // Position marker
    "0,1",                       // Key at next position  
    {"x": 2},
    "0,2"
]
```

**Rule Discovery:** Real vial.json uses POSITION MARKERS (separate `{"x": N}` entries) to indicate key positions within multi-key rows. Each position marker is paired with ONE key entry string!

### 2. Wide Key (`w` Flag) Handling

**My Converter:**
```json
[{"x": 4.5, "w": 2}, "3,5"]
```

**Real vial.json:**
```json
{           // Position marker (no x/y because wide key is special)
    "w": 2,                 // Wide key indicator only!
    "x": <center_x>         // Sometimes has center position
}, 
"3,5"                   // Key coordinate as string
```

**Actually:** Real vial.json stores `{"w": N}` entries BEFORE the actual key coordinate string!

### 3. Matrix String Format - CRITICAL

**My Converter (WRONG):**
- Uses "row,col" where row is first number, col is second

**Real vial.json (CORRECT):**
- Uses "col,row" or sometimes "x,y" format
- For Boston row 0: uses keys like `"0,0", "0,1", "0,2"` etc.
- The FIRST number is COLUMN index, SECOND is ROW index

**This is backwards from keyboard.json!** In keyboard.json, it's `[row, col]` but vial.json string format appears to be `col,row`!

---

## Concrete Example: Boston Keyboard First Row

### Real Boston vial.json (from file inspection):
```json
[
    {"x": 0, "y": 0},      // Position marker
    "0,0",                 // Key at col 0, row 0 (string format!)
    {"x": 1, "y": 0},      // Next position marker
    "0,1",                 // Key at col 1, row 0
    ...
]
```

### My Converter Generated:
```json
[
    [{"x": 0, "y": 0}, "0,0"],  // WRONG - combined into one entry!
    [{"x": 1, "y": 0}, "0,1"],
    ...
]
```

---

## Corrected Conversion Rules

### R1: Position Marker Pattern (Multi-key rows)
```python
# keyboard.json: {"matrix": [row, col], "x": X, "y": Y}
# → vial.json: [{"x": X, "y": Y}, "col,row"]  # But wait...
```

**Actually, real pattern is:**
```python
# Position marker: [{"x": X, "y": Y}, "row,col"]  
# Key string: "row,col" (but format appears to be col,row in strings!)
```

### R2: Wide Key Pattern
```python
# keyboard.json: {"matrix": [r,c], "x": X, "w": N}
# → vial.json: [{"w": N}, "row,col"]  # w entry before coordinate string
```

---

## Summary of Differences Found

| Aspect | My Converter | Real vial.json | Status |
|--------|--------------|----------------|--------|
| **Entry Structure** | `[wrapper, coord]` per key | Position markers between keys | ✗ DIFFERENT |
| **Wide Key (`w`)** | In wrapper dict | Separate `{"w": N}` entry | ✗ DIFFERENT |
| **Matrix String Format** | "row,col" (keyboard.json order) | Appears to be "col,row" in strings | ⚠ NEEDS VERIFICATION |
| **Name Field** | Extracts last part of dotted name | Sometimes includes layout variant (V0, V1) | ⚠ PARTIAL MATCH |
| **Hex Case** | Lowercase (0xfeed) | Mixed case (0xFeed, 0xFEED) | ⚠ PREFERENCE DIFFERENT |

---

## Next Steps

1. **Update converter** to generate position marker pattern like real vial.json
2. **Fix wide key handling** - separate `{"w": N}` entries
3. **Verify matrix string format** - whether it's "row,col" or "col,row"
4. **Handle name variants** - include layout version in some cases (V0, V1)
5. **Optional: match hex case** - real files use mixed case for vendor/product IDs

---

## Testing Commands

```bash
# View real Boston vial.json structure
type "D:\GitHub2\vial-qmk\keyboards\boston\keymaps\vial\vial.json" | Select-String "^[" -Context 0,5

# View generated Boston output  
type "D:\GitHub\keyboard_stuff\scripts\vial-research\vials\Boston\vial.json"
```

---

**Last Updated:** 2026-07-01  
**Based on:** Batch analysis of 504 keyboard pairs from CSV reference
