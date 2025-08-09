# QMK Format Converter

A powerful and comprehensive utility for converting between different QMK keyboard layout formats: **KLE (Keyboard Layout Editor)**, **VIA keymap specifications**, **QMK keymap.c source files**, and **QMK Configurator JSON exports**.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-green.svg)](#testing)

## 🚀 Features

- **🔄 Bidirectional Conversion**: Convert seamlessly between KLE, VIA, keymap.c, and QMK Configurator formats
- **🔍 Automatic Format Detection**: Smart detection of input file formats
- **✅ Data Integrity**: Perfect preservation of keyboard layouts during conversion
- **🎯 Comprehensive Validation**: Built-in validation for all supported formats
- **⚡ High Performance**: Fast conversion with optimized parsing (< 1ms average)
- **🧪 Extensively Tested**: Comprehensive test suite with multiple component and integration tests
- **📚 Universal Data Model**: Robust intermediate representation supporting all format features
- **💻 CLI Interface**: Easy-to-use command-line interface for batch operations
- **🐍 Python API**: Programmatic access for integration into other tools

## 📋 Supported Formats

| Format | Description | Extension | Features |
|--------|-------------|-----------|----------|
| **KLE** | [Keyboard Layout Editor](http://keyboard-layout-editor.com) JSON | `.json` | Physical layout, key positioning, visual styling, labels |
| **VIA** | [VIA/VIAL](https://caniusevia.com) keymap specification | `.json` | Keymap layers, keyboard metadata, matrix definitions, feature flags |
| **keymap.c** | QMK firmware keymap source code | `.c` | Layer definitions, custom functions, compile-ready code, QMK macros |
| **QMK Configurator** | [QMK Configurator](https://config.qmk.fm) JSON export | `.json` | Flat layer arrays, keyboard metadata, direct QMK compatibility, web editor export |

## 🛠 Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required!

### Quick Install
```bash
# Clone the repository
git clone https://github.com/your-username/qmk_format_converter.git
cd qmk_format_converter

# Optional: Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# The converter is ready to use - no pip install needed!
```

## 🎯 Quick Start

### Easy Setup (Recommended)

```bash
# One-time setup
cd qmk_format_converter
./setup.sh          # Linux/macOS
# OR
setup.bat           # Windows
```

### Simple Command Line Usage

```bash
# Convert KLE to VIA (auto-detects input format)
qmk-convert layout.json --to via -o output.json

# Convert keymap.c to KLE with explicit formats
qmk-convert keymap.c --from keymap --to kle -o layout.json

# Validate a layout file
qmk-convert layout.json --validate

# List supported formats
qmk-convert --list-formats

# Get help
qmk-convert --help
```

### Alternative: Direct Python Usage (if setup not used)

```bash
# Use the CLI directly
cd qmk_format_converter
python cli.py layout.json --to via -o output.json

# Or the original Python approach
python -c "
from qmk_format_converter.qmk_converter import *
QMKFormatConverter().convert_file('layout.json', SupportedFormat.KLE, 'output.via.json', SupportedFormat.VIA)
print('Conversion complete!')
"
```

### Python API Usage

```python
from qmk_format_converter.qmk_converter import QMKFormatConverter, SupportedFormat

# Initialize converter
converter = QMKFormatConverter()

# Auto-detect and convert
layout = converter.load_file('input.json')  # Auto-detects format
converter.save_file(layout, 'output.c', SupportedFormat.KEYMAP)

# Explicit format conversion
converter.convert_file(
    'keyboard.json', SupportedFormat.KLE, 
    'keymap.c', SupportedFormat.KEYMAP
)

# Validate files
result = converter.validate_file('layout.json')
if result['valid']:
    print(f"Layout: {result['summary']['name']}")
    print(f"Keys: {result['summary']['key_count']}")
else:
    print(f"Errors: {result['errors']}")

# Get format information
info = converter.get_format_info(SupportedFormat.VIA)
print(f"{info['name']}: {info['description']}")
```

## 📖 Usage Examples

### 1. KLE to QMK Keymap Conversion

```python
from qmk_format_converter.qmk_converter import QMKFormatConverter, SupportedFormat

converter = QMKFormatConverter()

# Load KLE file from keyboard-layout-editor.com
kle_layout = converter.load_file('my_keyboard.json', SupportedFormat.KLE)

# Generate QMK keymap.c
converter.save_file(kle_layout, 'keymap.c', SupportedFormat.KEYMAP)

print(f"Converted {len(kle_layout.keys)} keys to QMK format!")
```

### 2. VIA to KLE Conversion

```python
# Convert VIA keymap to visual KLE format
converter.convert_file('keymap.via.json', SupportedFormat.VIA, 'layout.kle.json', SupportedFormat.KLE)
```


### 4. Format Detection and Validation

```python
# Auto-detect format and validate
def analyze_layout(file_path):
    converter = QMKFormatConverter()
    
    # Detect format
    detected_format = converter.detect_format(file_path)
    print(f"Detected format: {detected_format.value if detected_format else 'Unknown'}")
    
    # Validate
    result = converter.validate_file(file_path)
    
    if result['valid']:
        summary = result['summary']
        print(f"✅ Valid {result['format']} file")
        print(f"   Name: {summary.get('name', 'N/A')}")
        print(f"   Keys: {summary.get('key_count', 0)}")
        print(f"   Layers: {summary.get('layer_count', 0)}")
        print(f"   Matrix: {summary.get('matrix_size', 'N/A')}")
    else:
        print(f"❌ Invalid file:")
        for error in result['errors']:
            print(f"   - {error}")
```

## 🏗 Architecture

The converter uses a **Universal Data Model** as an intermediate representation:

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│ KLE JSON    │───▶│ Universal       │───▶│ VIA JSON    │
└─────────────┘    │ Layout Model    │    └─────────────┘
┌─────────────┐    │                 │    ┌─────────────┐
│ keymap.c    │◀──▶│ - Keys          │◀──▶│ Any Format  │
└─────────────┘    │ - Layers        │    └─────────────┘
                   │ - Matrix        │
                   │ - Metadata      │
                   └─────────────────┘
```

### Key Components

- **`qmk_converter.py`**: Main converter class and API
- **`parsers/`**: Format-specific parsers (KLE, VIA, keymap.c)
- **`generators/`**: Format-specific generators 
- **`data_models/`**: Universal layout representation
- **`cli.py`**: Command-line interface
- **`tests/`**: Comprehensive test suite



## 🔧 Advanced Usage

### Custom Key Mappings

```python
from qmk_format_converter.data_models.keycode_mappings import QMK_TO_VIA_KEYCODE_MAP

# Add custom keycode mappings
QMK_TO_VIA_KEYCODE_MAP['KC_CUSTOM'] = 'custom_key'
```

### Layout Manipulation

```python
# Load and modify layout
layout = converter.load_file('input.json')

# Add custom metadata
layout.name = "My Custom Layout"
layout.author = "Your Name"

# Modify keys programmatically
for key in layout.keys:
    if key.keycode == 'KC_CAPS':
        key.keycode = 'KC_ESC'  # Caps Lock → Escape

# Save modified layout
converter.save_file(layout, 'modified.json', SupportedFormat.VIA)
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

```bash
# Clone and setup
git clone https://github.com/your-username/qmk_format_converter.git
cd qmk_format_converter

# No external dependencies required!

# Run tests to ensure everything works
python archive/tests/test_suite.py
```

### Adding New Formats

1. **Create Parser**: Add new parser in `parsers/your_format_parser.py`
2. **Create Generator**: Add generator in `generators/your_format_generator.py`
3. **Update Converter**: Add format to `SupportedFormat` enum
4. **Add Tests**: Create test files following existing patterns
5. **Update Documentation**: Add format to README and docs

### Code Style

- Follow PEP 8 for Python code style
- Use type hints where appropriate
- Add docstrings for all public functions
- Include comprehensive tests for new features

## 📝 Format Specifications

Detailed format specifications are available in [`docs/format_specifications.md`](docs/USAGE_GUIDE.md).

## 🐛 Troubleshooting

### Common Issues

**Q: "Module not found" error**
```bash
# Ensure you're in the right directory
cd qmk_format_converter
# Use absolute imports
python -c "import sys; sys.path.append('.'); from qmk_converter import *"
```

**Q: "Format detection failed"**
```python
# Specify format explicitly
converter.load_file('file.json', SupportedFormat.KLE)
```

**Q: "Validation errors"**
```python
# Check specific errors
result = converter.validate_file('file.json')
print(result['errors'])  # See what's wrong
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **QMK Community**: For the amazing QMK firmware
- **KLE**: [keyboard-layout-editor.com](http://keyboard-layout-editor.com) for the visual layout standard
- **VIA**: [caniusevia.com](https://caniusevia.com) for the keymap specification
- **Contributors**: Everyone who helps improve this tool

## 🔗 Related Projects

- [QMK Firmware](https://github.com/qmk/qmk_firmware) - The keyboard firmware this tool supports
- [VIA](https://github.com/the-via/app) - Visual keymap editor
- [Keyboard Layout Editor](http://keyboard-layout-editor.com) - Web-based keyboard layout designer

## 📈 Project Stats

- **Languages**: Python 3.7+
- **Core Files**: 20+ source files across parsers, generators, and data models
- **Tests**: Comprehensive test suite in archive/tests/
- **Formats Supported**: 4 (KLE, VIA, keymap.c, QMK Configurator)
- **Key Preservation**: 100% in round-trip tests
- **Dependencies**: Zero external dependencies required

---

**Made with ❤️ for the QMK community**

*If this tool helps you, please ⭐ star the repository and share with fellow keyboard enthusiasts!*
