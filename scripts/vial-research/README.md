# VIAL Conversion Research

This directory contains tools and research for converting QMK `keyboard.json` configuration files to VIAL (Virtual Input Abstraction Layer) JSON format.

---

## Overview

This project provides automated tools for:
- Converting QMK `keyboard.json` configuration files to VIAL JSON format
- Analyzing patterns in keyboard configurations across 500+ keyboard pairs
- Comparing generated conversions against reference vial.json files

---

## Tools Available

### Primary Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `keyboard_to_vial_converter.py` | Main conversion tool - converts keyboard.json to vial.json | ✅ Active |
| `convert_keyboard_to_vial.py` | Alternative implementation | ⚠ Has known issues (extra y field) |
| `compare_vial_conversions.py` | Compare generated vs real vial.json files | ✅ Available |

### Analysis Scripts

- `analyze_vial_patterns.py` - Analyze patterns across keyboards
- `find_vial_pairs.py` - Extract path mappings from filesystem
- `read_csv.py` / `parse_csv_rows.py` - CSV data processing

---

## Usage Examples

### Convert a Single Keyboard

```bash
python keyboard_to_vial_converter.py "D:/GitHub2/vial-qmk/keyboards/your_keyboard"
```

This will:
1. Read the `keyboard.json` file from the specified keyboard directory
2. Generate a `vial.json` file in the same directory
- [x] Read compare_vial_conversions.py to understand its functionality
- [ ] Run the comparison command with specified paths
</task_progress>
</attempt_completion>
</attempt_completion>