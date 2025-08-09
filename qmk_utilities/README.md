# QMK Utilities

A collection of utilities for working with QMK (Quantum Mechanical Keyboard) firmware.

## 🚧 Outstanding TODOs

### QMK Format Converter Issues
- **[HIGH PRIORITY]** Fix VIA parser to handle reference VIA file format - Current parser fails with "No keymap layout found" error
- **[HIGH PRIORITY]** Fix keycode function call parsing - Function calls like `MO(_LOWER)`, `LT(2,KC_LCTL)` are being truncated to just function names  
- **[HIGH PRIORITY]** Fix key count inconsistencies across conversions - Different conversion paths produce different key counts (53-60 keys expected)
- **[MEDIUM PRIORITY]** Evaluate KLE conversion feasibility - KLE requires precise key positions that other formats lack, may need to sunset `--to kle`
- **[MEDIUM PRIORITY]** Expand testing to multiple keyboard layouts - Current testing limited to Lily58, need 60%, TKL, Planck, Corne, Ergodox validation

> These issues are tracked in [`project_management/qmk_format_converter_project.json`](project_management/qmk_format_converter_project.json). Contributions welcome!

## Project Structure

### [`ascii_keymap_gen/`](ascii_keymap_gen/)
Generates ASCII art representations of keyboard layouts in QMK keymap.c files. Supports 18+ keyboards including Lily58, Corne, Planck, and Ergodox EZ with smart keyboard detection from keymap files. Features modular architecture with JSON layout definitions and works as a standalone utility with no external dependencies.

### [`qmk_format_converter/`](qmk_format_converter/)
Converts between different QMK keyboard format specifications including KLE JSON, VIA JSON, keymap.c, and QMK Configurator JSON. Features automatic format detection, universal data model with comprehensive data preservation, and direct integration with config.qmk.fm. Requires `ascii_keymap_gen` for keymap.c generation features.

### [`ergogen_to_qmk_converter/`](ergogen_to_qmk_converter/)
Converts Ergogen YAML keyboard configurations to QMK-compatible formats. Parses Ergogen's point-based layout definitions and generates corresponding QMK info.json files, keymap templates, and configuration files. Designed to bridge the gap between Ergogen's PCB design workflow and QMK firmware development.

### [`kle_to_ergogen/`](kle_to_ergogen/)
Converts Keyboard Layout Editor (KLE) JSON files to Ergogen YAML configurations for PCB generation. Transforms KLE's visual keyboard layouts into Ergogen's point-based coordinate system, enabling automated PCB design workflows. Includes coordinate transformation utilities and sample configurations for various keyboard layouts.

### [`dxf-viewer/`](dxf-viewer/)
Web-based DXF file viewer for displaying CAD drawings and technical files in your browser. Features a Python Flask backend with ezdxf parsing and a React frontend with Canvas rendering. Perfect for viewing Ergogen-generated switch plates, keyboard cases, and other DXF files without requiring full CAD software. Supports local file browsing and real-time rendering.

### [`docs/`](docs/)
Contains project-wide documentation files including development questions, completion summaries, and architectural decisions. Serves as a central repository for project insights, requirements analysis, and development process documentation that spans across multiple utilities.

### [`samples/`](samples/)
Example and test configuration files used throughout the project including Lily58 and macropad Ergogen configurations. These files serve as test cases, reference implementations, and examples demonstrating various keyboard configurations and Ergogen YAML structures for development and testing purposes.

### [`tests/`](tests/)
Test files providing validation and quality assurance for parsing and conversion utilities across the project. Includes unit tests, integration tests, and edge case validation for QMK keymap parsing, VIA format handling, Ergogen conversion functionality, and comprehensive format validation.

### [`project_management/`](project_management/)
Task tracking and planning files for the QMK Utilities project using the Task Pulse format. Contains detailed task breakdowns, progress tracking, and development milestones for individual converter projects, providing structured project management and development roadmaps.

## Installation & Usage

Each utility includes detailed setup and usage instructions in its respective README:
- [ascii_keymap_gen setup →](ascii_keymap_gen/README.md)
- [qmk_format_converter setup →](qmk_format_converter/README.md)
- [dxf-viewer setup →](dxf-viewer/README.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.
