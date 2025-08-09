# QMK Format Converter - Usage Guide

Complete guide for using the QMK Format Converter to translate between KLE, VIA, and keymap.c formats.

## Table of Contents

- [Quick Start](#quick-start)
- [Format Overview](#format-overview)
- [Common Use Cases](#common-use-cases)
- [API Reference](#api-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Basic Conversion

```python
from qmk_format_converter.qmk_converter import QMKFormatConverter, SupportedFormat

# Initialize converter
converter = QMKFormatConverter()

# Convert KLE to VIA
converter.convert_file('layout.json', SupportedFormat.KLE, 'keymap.via.json', SupportedFormat.VIA)
```

### 2. Auto-Detection

```python
# Let the converter detect format automatically
layout = converter.load_file('keyboard_layout.json')  # Auto-detects KLE/VIA
converter.save_file(layout, 'keymap.c', SupportedFormat.KEYMAP)
```

### 3. Validation

```python
# Validate before conversion
result = converter.validate_file('input.json')
if result['valid']:
    converter.convert_file('input.json', None, 'output.c', SupportedFormat.KEYMAP)
else:
    print(f"Validation errors: {result['errors']}")
```

## Format Overview

### KLE (Keyboard Layout Editor)

**Best for**: Visual keyboard design, sharing layouts, physical key positioning

```json
{
  "meta": {
    "name": "My Keyboard Layout"
  },
  "layout": [
    ["Esc", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", {"w": 2}, "Backspace"],
    [{"w": 1.5}, "Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", {"w": 1.5}, "\\"],
    [{"w": 1.75}, "Caps Lock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", {"w": 2.25}, "Enter"]
  ]
}
```

**Features**:
- Visual representation of keyboard layout
- Key sizing and positioning (width, height, rotation)
- Key labels and legends
- Color customization
- Export/import from keyboard-layout-editor.com

### VIA Keymap Format

**Best for**: Runtime keymap editing, multiple layers, advanced QMK features

```json
{
  "name": "My Keyboard",
  "vendorId": "0x1234",
  "productId": "0x5678",
  "layouts": {
    "keymap": [
      ["KC_ESC", "KC_1", "KC_2", "KC_3", "KC_4", "KC_5", "KC_6", "KC_7", "KC_8", "KC_9", "KC_0", "KC_MINS", "KC_EQL", "KC_BSPC"],
      ["KC_TAB", "KC_Q", "KC_W", "KC_E", "KC_R", "KC_T", "KC_Y", "KC_U", "KC_I", "KC_O", "KC_P", "KC_LBRC", "KC_RBRC", "KC_BSLS"],
      ["KC_CAPS", "KC_A", "KC_S", "KC_D", "KC_F", "KC_G", "KC_H", "KC_J", "KC_K", "KC_L", "KC_SCLN", "KC_QUOT", "KC_ENT"]
    ]
  }
}
```

**Features**:
- Multiple layer support
- QMK keycode compatibility
- Keyboard metadata (vendor ID, product ID)
- Matrix definitions
- Feature flags and capabilities

### keymap.c (QMK Source)

**Best for**: Custom firmware compilation, advanced programming, version control

```c
#include QMK_KEYBOARD_H

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT(
        KC_ESC,  KC_1,    KC_2,    KC_3,    KC_4,    KC_5,    KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    KC_MINS, KC_EQL,  KC_BSPC,
        KC_TAB,  KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,    KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    KC_LBRC, KC_RBRC, KC_BSLS,
        KC_CAPS, KC_A,    KC_S,    KC_D,    KC_F,    KC_G,    KC_H,    KC_J,    KC_K,    KC_L,    KC_SCLN, KC_QUOT, KC_ENT
    )
};
```

**Features**:
- Compile-time keymap definition
- Custom function integration
- Full QMK feature access
- C preprocessor macros
- Version control friendly

## Common Use Cases

### 1. KLE to QMK Workflow

**Scenario**: You designed a keyboard layout visually in KLE and want to create a QMK keymap.

```python
# Load KLE design
layout = converter.load_file('my_design.json', SupportedFormat.KLE)

# Convert to QMK keymap
converter.save_file(layout, 'keymap.c', SupportedFormat.KEYMAP)

# The generated keymap.c is ready to compile with QMK
```

### 2. VIA to KLE Sharing

**Scenario**: You have a VIA keymap and want to share the visual layout.

```python
# Convert VIA keymap to visual KLE format
converter.convert_file('my_keymap.via.json', SupportedFormat.VIA, 'shareable_layout.json', SupportedFormat.KLE)

# Upload shareable_layout.json to keyboard-layout-editor.com
```

### 3. Keymap Migration

**Scenario**: Converting existing keymap.c files to VIA-compatible format.

```python
# Parse existing keymap.c
layout = converter.load_file('old_keymap.c', SupportedFormat.KEYMAP)

# Convert to VIA format for easy editing
converter.save_file(layout, 'editable_keymap.via.json', SupportedFormat.VIA)
```

### 4. Batch Processing

**Scenario**: Converting multiple layouts at once.

```python
from pathlib import Path

converter = QMKFormatConverter()
input_dir = Path('kle_layouts')
output_dir = Path('qmk_keymaps')

for kle_file in input_dir.glob('*.json'):
    output_file = output_dir / f"{kle_file.stem}.c"
    try:
        converter.convert_file(kle_file, SupportedFormat.KLE, output_file, SupportedFormat.KEYMAP)
        print(f"✅ Converted {kle_file.name}")
    except Exception as e:
        print(f"❌ Failed {kle_file.name}: {e}")
```

## API Reference

### QMKFormatConverter Class

#### Methods

##### `load_file(file_path, format_type=None)`

Load a keyboard layout file.

**Parameters:**
- `file_path` (str|Path): Path to the input file
- `format_type` (SupportedFormat, optional): Format of the file (auto-detected if None)

**Returns:** `UniversalLayout` object

**Example:**
```python
layout = converter.load_file('layout.json')  # Auto-detect
layout = converter.load_file('layout.json', SupportedFormat.KLE)  # Explicit
```

##### `save_file(layout, file_path, format_type)`

Save a layout to a file.

**Parameters:**
- `layout` (UniversalLayout): Layout object to save
- `file_path` (str|Path): Output file path
- `format_type` (SupportedFormat): Target format

**Example:**
```python
converter.save_file(layout, 'output.via.json', SupportedFormat.VIA)
```

##### `convert_file(input_path, input_format, output_path, output_format)`

Convert a file from one format to another.

**Parameters:**
- `input_path` (str|Path): Input file path
- `input_format` (SupportedFormat, optional): Input format (auto-detected if None)
- `output_path` (str|Path): Output file path  
- `output_format` (SupportedFormat): Target format

**Example:**
```python
converter.convert_file('input.json', SupportedFormat.KLE, 'output.c', SupportedFormat.KEYMAP)
```

##### `validate_file(file_path, format_type=None)`

Validate a keyboard layout file.

**Parameters:**
- `file_path` (str|Path): File to validate
- `format_type` (SupportedFormat, optional): Expected format

**Returns:** Dict with validation results

**Example:**
```python
result = converter.validate_file('layout.json')
if result['valid']:
    print(f"✅ Valid {result['format']} file")
    print(f"   Keys: {result['summary']['key_count']}")
else:
    print(f"❌ Validation errors: {result['errors']}")
```

##### `detect_format(file_path)`

Automatically detect the format of a file.

**Parameters:**
- `file_path` (str|Path): File to analyze

**Returns:** `SupportedFormat` or `None`

**Example:**
```python
format_type = converter.detect_format('unknown_file.json')
print(f"Detected format: {format_type.value if format_type else 'Unknown'}")
```

##### `list_supported_formats()`

Get a list of supported formats.

**Returns:** Dict mapping format names to descriptions

**Example:**
```python
formats = converter.list_supported_formats()
for name, description in formats.items():
    print(f"{name}: {description}")
```

##### `get_format_info(format_type)`

Get detailed information about a format.

**Parameters:**
- `format_type` (SupportedFormat): Format to get info about

**Returns:** Dict with format details

**Example:**
```python
info = converter.get_format_info(SupportedFormat.KLE)
print(f"Name: {info['name']}")
print(f"Extension: {info['extension']}")
print(f"Features: {', '.join(info['features'])}")
```

## Best Practices

### 1. Always Validate First

```python
# Validate before conversion to catch issues early
result = converter.validate_file('input.json')
if not result['valid']:
    print(f"Validation failed: {result['errors']}")
    exit(1)

# Proceed with conversion
converter.convert_file('input.json', None, 'output.c', SupportedFormat.KEYMAP)
```

### 2. Handle Errors Gracefully

```python
try:
    layout = converter.load_file('questionable_file.json')
    converter.save_file(layout, 'output.via.json', SupportedFormat.VIA)
except FileNotFoundError:
    print("Input file not found")
except ValueError as e:
    print(f"Format error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 3. Use Auto-Detection When Possible

```python
# Let the converter figure out the format
layout = converter.load_file('mystery_layout.json')  # Works for KLE or VIA

# Only specify format when needed
layout = converter.load_file('ambiguous.json', SupportedFormat.KLE)
```

### 4. Verify Output

```python
# Convert and verify
converter.convert_file('input.json', SupportedFormat.KLE, 'output.via.json', SupportedFormat.VIA)

# Verify the output is valid
result = converter.validate_file('output.via.json')
assert result['valid'], f"Output validation failed: {result['errors']}"
```

### 5. Preserve Metadata

```python
# Load and preserve custom metadata
layout = converter.load_file('input.json')
layout.name = "My Custom Layout"
layout.author = "Your Name"
layout.description = "Custom layout for my keyboard"

converter.save_file(layout, 'output.json', SupportedFormat.VIA)
```

## Troubleshooting

### Common Issues

#### "Format detection failed"

**Problem**: Converter can't determine file format
**Solution**: Specify format explicitly

```python
# Instead of auto-detection
layout = converter.load_file('file.json')

# Use explicit format
layout = converter.load_file('file.json', SupportedFormat.KLE)
```

#### "Key count mismatch after conversion"

**Problem**: Some keys lost during conversion
**Solution**: Check input file validity and format limitations

```python
# Validate input first
result = converter.validate_file('input.json')
if not result['valid']:
    print(f"Input issues: {result['errors']}")

# Check key count preservation
original = converter.load_file('input.json')
converted_path = 'temp_output.json'
converter.save_file(original, converted_path, SupportedFormat.VIA)
converted = converter.load_file(converted_path)

if len(original.keys) != len(converted.keys):
    print(f"Key count changed: {len(original.keys)} → {len(converted.keys)}")
```

#### "Invalid JSON" errors

**Problem**: Malformed JSON input
**Solution**: Validate JSON syntax

```python
import json

# Check JSON syntax first
try:
    with open('input.json', 'r') as f:
        json.load(f)
    print("JSON syntax is valid")
except json.JSONDecodeError as e:
    print(f"JSON error: {e}")
```

#### "Module not found" errors

**Problem**: Import issues with Python modules
**Solution**: Ensure correct path and imports

```bash
# Run from the correct directory
cd qmk_format_converter

# Use absolute imports
python -c "
import sys
sys.path.append('.')
from qmk_converter import QMKFormatConverter
"
```

### Performance Issues

#### Large file processing

```python
import time

# Time your conversions
start_time = time.time()
converter.convert_file('large_layout.json', SupportedFormat.KLE, 'output.c', SupportedFormat.KEYMAP)
duration = time.time() - start_time

print(f"Conversion took {duration:.3f} seconds")

# For large batch jobs, consider progress reporting
from pathlib import Path

files = list(Path('layouts').glob('*.json'))
for i, file in enumerate(files):
    print(f"Processing {i+1}/{len(files)}: {file.name}")
    converter.convert_file(file, SupportedFormat.KLE, f'output/{file.stem}.c', SupportedFormat.KEYMAP)
```

### Getting Help

1. **Check the logs**: Enable verbose output to see what's happening
2. **Validate inputs**: Use the validation function to check file format
3. **Test with samples**: Try with the provided sample files first
4. **Check format specs**: Review the format specifications documentation
5. **File an issue**: If problems persist, create a GitHub issue with sample files

```python
# Enable debug output (if available)
import logging
logging.basicConfig(level=logging.DEBUG)

# Test with known-good sample
result = converter.validate_file('samples/sample_kle.json')
print(f"Sample validation: {result['valid']}")
