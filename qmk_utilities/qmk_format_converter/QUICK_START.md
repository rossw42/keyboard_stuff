# QMK Format Converter - Quick Start Guide

Get up and running with the QMK Format Converter in under 2 minutes!

## 🚀 One-Time Setup

### Linux/macOS
```bash
cd qmk_format_converter
./setup.sh
```

### Windows
```cmd
cd qmk_format_converter
setup.bat
```

That's it! The converter is now ready to use.

## 💡 Basic Usage

### Convert Files
```bash
# Convert KLE to VIA (auto-detects input format)
qmk-convert layout.json --to via -o output.json

# Convert keymap.c to KLE 
qmk-convert keymap.c --from keymap --to kle -o layout.json

# Convert VIA to keymap.c
qmk-convert keymap.via.json --from via --to keymap -o keymap.c
```

### Get Help
```bash
# List all supported formats
qmk-convert --list-formats

# Get detailed help
qmk-convert --help

# Validate a file
qmk-convert layout.json --validate

# Get format information
qmk-convert --info kle
```

## 📁 Supported Formats

| Format | Description | Extension |
|--------|-------------|-----------|
| **kle** | Keyboard Layout Editor | `.json` |
| **via** | VIA/VIAL keymap format | `.json` |
| **keymap** | QMK keymap.c source | `.c` |

## 🔥 Examples

### Convert KLE from keyboard-layout-editor.com
```bash
# Download your layout from keyboard-layout-editor.com as JSON
qmk-convert my-layout.json --to keymap -o keymap.c
```

### Convert VIA keymap to visual KLE
```bash
qmk-convert my-keymap.via.json --to kle -o visual-layout.json
# Then upload visual-layout.json to keyboard-layout-editor.com
```

### Validate before converting
```bash
qmk-convert suspicious-file.json --validate
# Check if it's valid before conversion
```

## 🛠 If You Don't Have Setup Installed

You can still use the converter directly:

### Linux/macOS
```bash
cd qmk_format_converter
./qmk-convert --help
```

### Windows
```cmd
cd qmk_format_converter
qmk-convert.bat --help
```

### Python Direct (if scripts don't work)
```bash
cd qmk_format_converter
python cli.py --help
```

## 🆘 Getting Help

- Run `qmk-convert --help` for full command reference
- Run `qmk-convert --list-formats` to see supported formats
- Check the main [README.md](README.md) for detailed documentation
- Look at [samples/](samples/) for example files

## ⚡ Quick Reference

```bash
# Basic conversion
qmk-convert INPUT_FILE --to FORMAT -o OUTPUT_FILE

# With explicit input format  
qmk-convert INPUT_FILE --from FORMAT --to FORMAT -o OUTPUT_FILE

# Validation only
qmk-convert INPUT_FILE --validate

# Information
qmk-convert --list-formats
qmk-convert --info FORMAT
```

**That's it! You're ready to convert keyboard layouts!** 🎉
