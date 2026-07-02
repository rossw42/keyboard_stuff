# **VIAL Research Directory Documentation**
## *What is Happening in `/scripts/vial-research`*

---

## **📋 Overview**

The `vial-research` directory contains research and development work focused on understanding how **QMK/VIA's `keyboard.json` format maps to VIA's `vial.json` metadata format**. 

This is investigative work by @rossw42 (the keyboard_stuff repository owner) to:
1. Understand the conversion rules between keyboard configuration formats
2. Create tools to convert keyboards from keyboard.json → vial.json automatically
3. Document patterns and exceptions in existing vial-qmk repository

---

## **📁 Directory Structure**

```
D:\GitHub\keyboard_stuff\scripts\vial-research\
├── 📄 Documentation (Markdown guides)
│   ├── convert_keyboard_to_vial.md        # Testing instructions for conversion script
│   ├── vial_keyboard_research.md          # Core research: how keyboard.json → vial.json
│   ├── vial_keymap_patterns_analysis.md   # Pattern analysis across all keyboard pairs
│   └── keymap_analysis_plan.md            # Analysis methodology plan
│
├── 📄 CSV Data
│   └── vial_keyboard_pairs.csv            # 504 keyboard.json ↔ vial.json path mappings
│
├── 🐍 Python Scripts (Tools & Tests)
│   ├── keyboard_to_vial_converter.py      # Main conversion tool being developed
│   ├── convert_keyboard_to_vial.py        # Alternative converter implementation
│   ├── find_vial_pairs.py                  # Script to discover vial.json paths
│   ├── analyze_vial_patterns.py           # Pattern analysis across keyboards
│   ├── compare_vial_conversions.py         # Batch comparison tool
│   └── comprehensive_test.py              # Regression test suite
│
├── 🧪 Testing Files
│   ├── test_converter.py                  # Individual script tests
│   ├── test_conversion.py                 # Conversion accuracy tests
│   └── verify_all_keyboards_pairs.py       # Full verification script
│
├── 📊 Results/Analysis Outputs
│   ├── vial_json_derivation_egg58.md      # Case study: Egg58 keyboard analysis
│   └── all_keyboards_findings.pkl         # Pickle file with extracted data
│
├── 🗂️ Subdirectories
│   ├── __pycache__/                       # Compiled Python bytecode
│   └── readme_/                           # (appears to be folder, unclear contents)
│
└── 📚 Additional Notes
    ├── VIAL_QMK_SUMMARY.md                 # Workspace summary for user
    └── keymap_analysis_plan.md             # Methodology documentation
```

---

## **🎯 Primary Goals**

### **Goal 1: Understand Conversion Rules**
The research aims to understand how VIA's `vial.json` format derives its structure from QMK's `keyboard.json`:

| Source Field | Destination Field | Mapping Rule |
|-------------|------------------|--------------|
| `keyboard_name` | `vial.json.name` | Direct copy |
| `usb.vid` | `vendorId` | Lowercase hex (e.g., `"0xFEED"` → `"0xfeed"`) |
| `usb.pid` | `productId` | Lowercase hex preserved |
| Layout matrix | `layouts.keymap[]` | Complex coordinate system transformation |

### **Goal 2: Create Conversion Tools**
The scripts being developed to automatically convert keyboards from keyboard.json format to vial.json format, allowing VIA to discover and display new keyboards without manual metadata creation.

### **Goal 3: Document Format Patterns**
Analyzing hundreds of keyboards to identify consistent patterns:
- When `vial.json` uses wrapped entries `[{"x": N}, "r,c"]` vs plain strings `"r,c"`
- Wide key detection rules (`"w"` property handling)
- Multi-key row structures (Boston-style complex layouts)

---

## **🔍 Key Findings Documented**

### **Finding 1: Two Coordinate Systems**
```python
# Pattern A: Float Coordinates (Boston, Arisu - split keyboards)
{"matrix": [0, 2], "x": 3.25, "y": 0} 
→ vial.json: [{"x": 3.25}, "0,2"]

# Pattern B: Integer Coordinates (Alpha, Canton - simple layouts)  
{"matrix": [0, 0], "x": 0, "y": 0}
→ vial.json: [{"x": 0, "y": 0}, "0,0"]
```

### **Finding 2: Wide Key Detection**
| keyboard.json Property | vial.json Result |
|------------------------|------------------|
| `"w": 2` | `[{"x": N, "w": 2}, "r,c"]` or `["r,c", {"w": 2}]` |
| `"x": 0.5, "w": 1.5` | `[{"x": 0.5, "w": 1.5}, "r,c"]` |

### **Finding 3: Four Row Structure Types**
1. **Type A**: Single wrapped entry `["[{"x", "y"}, "r,c"]]` - Standard keys (60% of entries)
2. **Type B**: Multi-key rows - Complex split layouts like Boston
3. **Type C**: Wide key with w property `[{"w": 2}, "r,c"]`
4. **Type D**: Color/metadata entries `["[{"x", "c"}, "r,c"]]`

### **Finding 4: What Gets Stripped**
- Switch keycode numbers (`"keycode": 63821`) → Removed (VIA handles via config)
- Modifier arrays (`"modifiers": ["ctrl"]`) → Stripped (VIA uses hotkey rules differently)
- Complex encoder pin arrays → Simplified or stripped

---

## **🛠️ Development Status**

### **Completed:**
✅ Comprehensive analysis of 504+ keyboard pairs  
✅ Pattern documentation across brands (Boston, Alpha, YMDK, ProjectD, etc.)  
✅ Multiple Python tools for conversion and testing  
✅ Mapping tables and rules documented  

### **In Progress:**
🔄 Refining `keyboard_to_vial_converter.py` - Current issues:
- Script only uses `--output` if file exists (fallback behavior causes directory confusion)
- Adds extra `y` field when some existing files omit it (format mismatch)

### **Planned/Not Yet Implemented:**
- Full multi-layout keyboard support extraction  
- Matrix pin automatic detection from layout files  
- Encoder pin mapping utilities  

---

## **📖 Documentation Files Summary**

| File | Purpose | Lines |
|------|---------|-------|
| `convert_keyboard_to_vial.md` | Testing instructions for conversion script (backup, run, compare, restore) | 208 |
| `vial_keyboard_research.md` | Core research: keyboard.json → vial.json field mappings | 456 |
| `vial_keymap_patterns_analysis.md` | Complete findings across all CSV keyboard pairs | 351 |
| `keymap_analysis_plan.md` | Methodology plan for analyzing all keyboards | 105 |

---

## **📊 Data Source**

The research is based on **`vial_keyboard_pairs.csv`**:
- Contains ~504 rows mapping keyboard.json paths → vial.json paths
- Covers major manufacturers: Alpha, Boston, Arisu, YMDK, ProjectD, etc.
- Includes multi-layout keyboards (same keyboard with different subdirectories)

---

## **🎯 Next Steps / Recommendations**

### **For Development:**
1. Fix `convert_keyboard_to_vial.py`'s output fallback behavior
2. Optionally omit `y` field when all keys share same row (matching real vial.json patterns)
3. Add color/metadata property extraction from keyboard.json keys dict

### **For Testing:**
1. Run batch tests on first 10 keyboards (`compare_vial_conversions.py`)
2. If mismatches found, examine format differences (extra `y` field pattern)
3. Document brand-specific conventions for each manufacturer

### **For Research:**
1. Extract coordinate system rules from additional keyboard brands
2. Create lookup tables per brand showing metadata preservation/stripping
3. Study edge cases: wide keys, multi-key rows, complex layouts

---

## **📚 Related Files in Workspace**

- `D:\GitHub2\vial-qmk` - Primary vial-qmk repository (contains the reference vial.json files)
- `D:\Keyboard\keyboard_stuff\keyboards/` - Example keymaps and VIAL configs
- `D:\Keyboard\keyboard_stuff\VIAL Docs/` - VIAL documentation references

---

**Summary:** This is a serious reverse-engineering effort to understand how VIA generates its keyboard metadata from QMK configuration files. The researcher has documented patterns across hundreds of keyboards, created conversion tools, and identified the core mapping rules. The work is focused on enabling automatic vial.json generation from keyboard.json inputs.
