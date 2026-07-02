# Batch Conversion Results Summary

**Date:** 2026-07-01  
**Processed:** All 504 keyboard pairs from `vial_keyboard_pairs.csv`

---

## Key Findings

### Output Directory Structure

The generated vial.json files have been saved to:
```
D:\GitHub\keyboard_stuff\scripts\vial-research\vials\<keyboard_name>\vial.json
```

However, some keyboards have NO real reference file at their CSV-specified location (like `alpha` which has no vial.json in its keymaps directory).

---

## Major Structure Differences Discovered

### 1. Entry Structure - CRITICAL DIFFERENCE

**My Converter:** Uses combined `[wrapper_dict, coordinate_string]` format  
**Real vial.json:** Uses separate entries for position markers and coordinates

Example from Boston keyboard:
- **Generated (wrong):** 129 entries with `[{"x": N}, "M,N"]` combined
- **Real file:** ~14 entries using pattern `{"x": N}`, `"M,N"` as separate items

### 2. Wide Key (`w`) Flag Location

**My Converter:** Stores wide key in wrapper dict: `[{"x": 4.5, "w": 2}, "3,5"]`  
**Real vial.json:** Uses separate `{"w": N}` entry before coordinate string

### 3. Name Field Case Differences

- My converter: Extracts last part of dotted name (e.g., `"Boston"`)
- Real files: Sometimes includes version suffix (e.g., `"BostonV0"`)

### 4. Hex Case Preference

- My converter: Lowercase hex (`0xfeed`)  
- Real files: Mixed case (`0xAC12`, `0xFEED`)

---

## Entry Count Discrepancies

| Keyboard | Generated | Real File | Ratio |
|----------|-----------|-----------|-------|
| Boston | 129 | 14 | 9.2x |
| Alpha | 28 | 0 | N/A |
| a_dux | 34 | 8 | 4.25x |
| Cantor | 42 | 16 | 2.6x |

The ratio varies because real vial.json uses position markers to separate keys in multi-key rows, while my converter groups them differently.

---

## Files Generated

All generated vials are saved in:
```
D:\GitHub\keyboard_stuff\scripts\vial-research\vials/
├── alpha/
│   └── vial.json
├── alps64/
│   └── vial.json
├── arisu/
│   └── vial.json  
├── a_dux/
│   └── vial.json
├── boston/
│   └── vial.json
├── ... (504 total)
└── reports/
    └── batch_conversion_results.json
```

---

## Comparison Report Location

Detailed comparison results saved to:
```
D:\GitHub\keyboard_stuff\scripts\vial-research\reports\batch_conversion_results.json
```

This file contains:
- Entry counts for each keyboard
- Metadata differences (name, vid, pid, lighting)
- Structure match status
- Specific issues found per keyboard

---

## Next Steps

1. Update converter to use real vial.json structure (separate position markers)
2. Adjust wide key handling to match real format
3. Handle name version suffixes for some keyboards
4. Verify matrix dimensions extraction accuracy

---

**All 504 keyboards have been processed and generated files are ready for comparison.**
