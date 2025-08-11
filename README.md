# Keyboard Development Ecosystem

A comprehensive collection of tools, utilities, and resources for mechanical keyboard development - from initial design concepts through firmware implementation.

> **Disclaimer**: I'm not really a programmer, I dont even play one on GitHub. This entire repo is a perpetual work-in-progress that will probably never be "finished" - much like my quest for the perfect keyboard layout. Expect things to be broken, half-implemented, or completely abandoned as I chase the next shiny keyboard idea. 🤷‍♂️

## 🛠 Tool Categories

### **ergogen/** - Hardware Design & PCB Generation
Complete Ergogen ecosystem for keyboard hardware design:
- **ergogen_to_qmk_converter/** - Convert Ergogen YAML to QMK firmware configs
- **kle_to_ergogen/** - Transform KLE layouts to Ergogen point definitions  
- **vscode-extension/** & **vscode-extension-v2/** - VS Code extensions for DXF viewing
- **mounting_styles/** - Reference implementations for different mounting approaches
- **keyboards/** & **working_samples/** - Example configurations and test cases

### **keyboards/** - Layout Configurations & Designs
Real-world keyboard layouts and configurations:
- VIA/QMK layout files for various keyboards (Lily58, Corne, DZ60, etc.)
- Custom macropad and encoder configurations
- JSON layout definitions for popular keyboards

### **qmk_utilities/** - Firmware Development Tools
Comprehensive QMK workflow utilities:
- **qmk_format_converter/** - Convert between KLE, VIA, keymap.c, and QMK Configurator formats
- **ascii_keymap_gen/** - Generate ASCII art representations of keyboard layouts
- Format detection, validation, and universal data model support

### **switch_research/** - Component Research & Documentation
Mechanical keyboard switch research and databases:
- Comprehensive MX switch characteristics and databases
- Switch selection guides and comparison matrices

## 🔄 Development Workflow

This ecosystem supports the complete keyboard development pipeline:

```
Concept → KLE Design → Ergogen PCB → QMK Firmware → Physical Build
    ↓         ↓           ↓            ↓              ↓
Research  Layout     Hardware     Firmware      Testing
Switches  Editor     Generation   Config        & Tuning
    ↑         ↑           ↑            ↑              ↑
switch_   keyboards/  ergogen/    qmk_utilities/  keyboards/
research/             tools/      converters/     layouts/
```

## 🚀 Quick Start Guides

### For Hardware Design (Ergogen)
1. Start with `ergogen/working_samples/` for reference configurations
2. Use `ergogen/mounting_styles/` to understand different mounting approaches  
3. Convert existing KLE layouts with `ergogen/kle_to_ergogen/`
4. View DXF outputs with the VS Code extensions in `ergogen/vscode-extension*/`

### For Firmware Development (QMK)
1. Convert between formats using `qmk_utilities/qmk_format_converter/`
2. Generate ASCII layout documentation with `qmk_utilities/ascii_keymap_gen/`
3. Reference existing layouts in `keyboards/` for inspiration
4. Bridge hardware to firmware with `ergogen/ergogen_to_qmk_converter/`

### For Switch Selection
1. Browse `switch_research/` for comprehensive switch databases
2. Use characteristic matrices to find switches matching your preferences

## 📁 Project Structure

Each directory contains its own comprehensive documentation and tooling. Most projects include:
- Detailed README with setup instructions
- Example/sample files for testing
- Modular architecture for easy extension
- Integration points with other tools in the ecosystem

## 🎯 Current Focus Areas

- **High Priority**: QMK format converter stability (VIA parsing, keycode functions)
- **Active Development**: Ergogen to QMK conversion pipeline
- **Maintenance**: VS Code DXF viewer extensions and mounting style examples
- **Research**: Switch database expansion and characteristic analysis

## 📊 Project Maturity

| Tool                     | Status                | Usability                       |
| ------------------------ | --------------------- | ------------------------------- |
| qmk_format_converter     | 🔧 Active fixes needed | Partial - core conversion works |
| ascii_keymap_gen         | ✅ Stable              | Production ready                |
| ergogen_to_qmk_converter | 🚧 In development      | Planning phase                  |
| kle_to_ergogen           | ✅ Functional          | Working with examples           |
| VS Code extensions       | ✅ Stable              | Production ready                |
| mounting_styles          | ✅ Reference complete  | Documentation/examples          |

## 🤝 Contributing

Each project welcomes contributions! Check individual README files for specific contribution guidelines. Common areas needing help:
- Bug fixes in format converters
- Additional keyboard layout examples  
- Switch database expansion
- Documentation improvements

## Status

Forever and always: 🚧 **WORK IN PROGRESS** 🚧

_"It's not a bug, it's a feature I haven't implemented yet."_
