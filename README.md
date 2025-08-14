# Keyboard Development Ecosystem

A collection of tools and resources for mechanical keyboard development - from hardware design through firmware implementation.

> **Disclaimer**: I'm not really a programmer, I dont even play one on GitHub. This entire repo is a perpetual work-in-progress that will probably never be "finished" - much like my quest for the perfect keyboard layout. Expect things to be broken, half-implemented, or completely abandoned as I chase the next shiny keyboard idea. 🤷‍♂️

## 🛠 What's Actually Here - that probably isn't all working.

### **ergogen/** - Ergogen-focused utilities for keyboard hardware design
- **ergogen-toolkit/** - Simple VS Code extension for running Ergogen and viewing DXF files - mostly working
- **ergogen_to_qmk_converter/** - Convert Ergogen YAML to QMK firmware configs (in development)
- **kle_to_ergogen/** - Transform KLE layouts to Ergogen point definitions  
- **mounting_styles/** - Reference implementations and examples for different mounting approaches
- **working_samples/** - Example Ergogen configurations and test cases

### **keyboards/** - Layout Configurations & Designs
Keyboard layouts and configurations that Im working on or have saved from somewhere else.
- VIA/QMK layout files for various keyboards (Lily58, Corne, DZ60, etc.)
- Custom macropad and encoder configurations
- JSON layout definitions for popular keyboards
- 3D files (STL, 3MF) for some designs

### **qmk_utilities/** - QMK Firmware Development Tools
QMK workflow utilities:
- **qmk_format_converter/** - Convert between KLE, VIA, keymap.c, and QMK Configurator formats (almost works!)
- **ascii_keymap_gen/** - Generate ASCII art representations of keyboard layouts in your QMK keymap files.

### **switch_research/** - Component Research & Documentation
Mechanical keyboard switch research:
- Comprehensive MX switch characteristics database
- Switch selection guides and comparison data


## 🤝 Contributing

Each project welcomes contributions! Common areas needing help:
- Bug fixes in format converters
- Additional keyboard layout examples  
- Switch database expansion
- Documentation improvements

Check individual README files for specific guidelines.


_"It's not a bug, it's a feature I haven't implemented yet."_
