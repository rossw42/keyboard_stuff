"""
Ergogen to QMK Converter

A utility for converting Ergogen hardware definition files (.yaml) to complete
QMK keyboard configurations, bridging the gap between hardware design and
firmware setup.

This package provides tools to:
- Parse Ergogen YAML hardware definitions
- Extract matrix configuration, pin assignments, and hardware features
- Generate complete QMK keyboard configurations (config.h, keyboard.h, rules.mk, info.json)
- Validate generated configurations for QMK compatibility

Main components:
- ErgogenParser: Parse Ergogen YAML files
- QMKHardwareModel: Intermediate data representation
- ConfigGenerator, KeyboardGenerator, RulesGenerator, InfoGenerator: QMK file generators
- ErgogenConverter: Main orchestration class

Example usage:
    from ergogen_to_qmk_converter import ErgogenConverter
    
    converter = ErgogenConverter()
    converter.convert_file("config_4x5.yaml", output_dir="./keyboard_config")
"""

__version__ = "0.1.0"
__author__ = "QMK Utilities Project"
__description__ = "Convert Ergogen hardware definitions to QMK keyboard configurations"

# Main converter class - will be implemented
# from .ergogen_converter import ErgogenConverter

# Make key classes available at package level when implemented
# __all__ = [
#     "ErgogenConverter",
#     "ErgogenParser", 
#     "QMKHardwareModel",
#     "ConfigGenerator",
#     "KeyboardGenerator", 
#     "RulesGenerator",
#     "InfoGenerator"
# ]
