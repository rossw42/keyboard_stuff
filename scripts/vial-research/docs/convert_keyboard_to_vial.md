# Testing Instructions for convert_keyboard_to_vial.py

## Overview
This document describes recommended tests for `D:\GitHub\keyboard_stuff\scripts\convert_keyboard_to_vial.py`.

The goal is to verify that the script **exactly replicates** existing `vial.json` files from provided `keyboard.json` files, using a temporary output file.

---

## Test Data Sources
- **Script:** `D:\GitHub\keyboard_stuff\scripts\convert_keyboard_to_vial.py`
- **Source Data:** `D:\GitHub\keyboard_stuff\scripts\vial_keyboard_pairs.csv`
  - Contains mapping: `keyboard.json` → `vial.json` paths

---

## Test Environment Setup
1. Create a temporary output directory to store generated `vial.json` files:
   ```
   D:\Keyboard Workspace\temp_vial_outputs
   ```

2. **Ensure real `vial.json` files are protected** before testing (use backups):
   - The script should be tested with backup restoration for all test runs.
   - Do NOT overwrite the original `vial.json` files directly; always restore from `.bak`.
   - Do NOT edit the keyboard.json files.

---

## Recommended Test Cases
Do not use the Tamago keyboard files.

### **Test 1: Single Keyboard Conversion & Comparison**
**Purpose:** Verify basic functionality on a single keyboard, ensuring the generated output matches the real file exactly.

**Steps:**
1. Pick one keyboard pair from `vial_keyboard_pairs.csv`:
   - Example: `alpha` (`D:\GitHub2\vial-qmk\keyboards\alpha\keyboard.json`)
   - Ground truth: `D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json`

2. Perform backup of the real `vial.json`:
   ```bash
   move D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json \
        temp_vial_outputs\alpha.bak
   ```

3. Create a temporary empty JSON file (required due to script logic):
   ```bash
   echo {} > D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json.tmp
   ```

4. Run the conversion script:
   ```bash
   python D:\GitHub\keyboard_stuff\scripts\convert_keyboard_to_vial.py \
        "D:\GitHub2\vial-qmk\keyboards\alpha\keyboard.json" \
        --output "D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json.tmp"
   ```

5. **Remove the temporary file and use proper dummy**:
   - If the script fails (KeyError), create proper dummy:
   ```python
   # Read keymap from keyboard.json to generate correct structure
   import json
   with open("keyboard.json") as kf:  # alpha\keyboard.json
       kb_data = json.load(kf)
   
   kb_name = kb_data.get("keyboard_name", "unknown")
   vendor_id = kb_data.get("usb", {}).get("vid", "0x0000")
   product_id = kb_data.get("usb", {}).get("pid", "0x0000")
   
   dummy_vial = {
       "name": kb_name,
       "vendorId": vendor_id,
       "productId": product_id,
       "lighting": "qmk_rgblight",
       "matrix": {"rows": 0, "cols": 0},
       "layouts": {"keymap": []}
   }
   
   with open("D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json.tmp", 'w') as f:
       json.dump(dummy_vial, f)
   ```

6. Run script again with the dummy:
   ```bash
   python D:\GitHub\keyboard_stuff\scripts\convert_keyboard_to_vial.py \
        "D:\GitHub2\vial-qmk\keyboards\alpha\keyboard.json" \
        --output "D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json.tmp"
   ```

7. Compare generated output (`vial.json.tmp`) with backup (`.bak`):
   ```python
   import json

   with open("temp_vial_outputs/alpha.bak") as f:
       real_data = json.load(f)
   
   with open("D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json.tmp") as f:
       gen_data = json.load(f)
   
   print(json.dumps(gen_data, indent=2))  # Print generated for inspection
   ```

8. Restore real file:
   ```bash
   move D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json.tmp \
        "temp_vial_outputs\alpha_real.json"  # backup original temporarily
   move temp_vial_outputs\alpha.bak \
        D:\GitHub2\vial-qmk\keyboards\alpha\keymaps\vial\vial.json
   ```

**Success Criteria:** `gen_data["layouts"]["keymap"]` equals `real_data["layouts"]["keymap"]` exactly.

---

### **Test 2: Batch Testing (10 Keyboards)**
**Purpose:** Run the script on a batch of keyboards and identify any inconsistencies.

**Steps:**
1. Use the automated script in `D:\GitHub\keyboard_stuff\scripts\compare_vial_conversions.py`:
   ```bash
   python D:\GitHub\keyboard_stuff\scripts\compare_vial_conversions.py
   ```

2. Inspect results:
   - **PASS:** Output shows "MATCH" for all keyboards.
   - **FAIL:** If any keyboard shows "MISMATCH", examine the specific errors printed (e.g., first row mismatches).

3. Common failure patterns to check:
   - Mismatch in `layouts["keymap"]` entry format:
     - Expected: `"0,0"` or `[{"x": N}, "N,M"]`
     - Got: `[{"x": N, "y": M}, "N,M"]` (extra y field added)
   - The script's default behavior is to include both `x` and `y` fields if present in `keyboard.json`. This may differ from the existing "real" `vial.json` format.

---

### **Test 3: Regression Testing with CSV Coverage**
**Purpose:** Iterate through all available keyboards in `vial_keyboard_pairs.csv` to ensure consistent behavior across different layouts and configurations.

**Steps:**
1. Run full batch test (already done above).
2. If any board shows mismatch, isolate it by:
   - Creating a separate backup script for individual testing.
   - Examining keyboard.json layout structure vs vial.json expected format.

---

## Known Issues / Behavior Notes

### Issue 1: Script Only Uses --output if File Exists
**Current Behavior:**
```python
# convert_keyboard_to_vial.py line ~85
if vial_path_or_output.exists():
    vial_data = load_json(vial_path_or_output)
else:
    vial_data = { ... }  # Creates from scratch with default paths
```

**Bug-like Behavior:** If `--output` file doesn't exist, the script falls back to `kb_path.parent / "vial.json"`. This causes output to go to a different directory than intended.

**Workaround Required:** Before running the script, ensure target `vial.json` exists (with minimal valid structure).

---

### Issue 2: Script Adds Extra 'y' Field When Not Expected
**Observation:**
- Real `vial.json` files have entries like `"0,0"` or `[{"x": N}, "N,M"]`.
- Generated output has `[{"x": N, "y": M}, "N,M"]` (includes `y`).

**Cause:** The script extracts `x` and `y` from `keyboard.json`'s layout definitions and always includes them.

**Potential Fix Needed:** Determine if the conversion logic should conditionally omit `y` based on existing `vial.json` format or user preference.

---

## Test Output Expectations

### Success Example:
```bash
Keyboard 1 (alpha): MATCH
Keyboard 2 (alps64): MATCH
...
[All PASS]
```

### Failure Pattern to Investigate:
```bash
Keyboard 1 (alpha): MISMATCH
  Row [{'x': 0, 'y': 0}, '0,0']: Expected ['0,0', ...], Got [{'x': 0, 'y': 0}, '0,0']
```

---

## Post-Test Cleanup
After testing, always:
1. Restore all real `vial.json` files from backups (`.bak`).
2. Remove temporary files (`temp_vial_outputs/`, `.tmp.bak` files).
3. Verify original keyboard directories are unchanged.

---

## Checklist
- [ ] Test single keyboard conversion manually (Test 1)
- [ ] Run batch test of first 10 keyboards from CSV (Test 2)
- [ ] Review differences for any failures (known format mismatch pattern)
- [ ] Document if fixes are needed in script logic
- [ ] Ensure no tamago board testing is performed (user exclusion)
