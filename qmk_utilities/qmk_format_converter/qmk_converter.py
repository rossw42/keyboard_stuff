"""
QMK Format Converter

Main converter class that orchestrates format conversion between
KLE, VIA, and keymap.c formats using the universal data model.
"""

import json
import os
from pathlib import Path
from typing import Union, Optional, Dict, Any
from enum import Enum

# Handle both standalone and module execution
try:
    from .data_models.universal_layout import UniversalLayout
    from .parsers.kle_parser import parse_kle_file
    from .parsers.via_parser import parse_via_file
    from .parsers.keymap_parser import parse_keymap_file
    from .parsers.qmk_configurator_parser import parse_qmk_configurator_file
    from .generators.kle_generator import generate_kle_file
    from .generators.via_generator import generate_via_file
    from .generators.keymap_generator import generate_keymap_file
    from .generators.qmk_configurator_generator import generate_qmk_configurator_file
except ImportError:
    # Running as standalone script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from data_models.universal_layout import UniversalLayout
    from parsers.kle_parser import parse_kle_file
    from parsers.via_parser import parse_via_file
    from parsers.keymap_parser import parse_keymap_file
    from parsers.qmk_configurator_parser import parse_qmk_configurator_file
    from generators.kle_generator import generate_kle_file
    from generators.via_generator import generate_via_file
    from generators.keymap_generator import generate_keymap_file
    from generators.qmk_configurator_generator import generate_qmk_configurator_file


class SupportedFormat(Enum):
    """Supported keyboard layout formats."""
    KLE = "kle"
    VIA = "via"
    KEYMAP = "keymap"
    QMK_CONFIGURATOR = "qmk_configurator"


class QMKFormatConverter:
    """
    Main converter class for translating between KLE, VIA, and keymap.c formats.
    
    This class provides a unified interface for converting keyboard layouts
    between different formats using a universal intermediate representation.
    
    Usage:
        converter = QMKFormatConverter()
        
        # Convert KLE to VIA
        layout = converter.load_file("layout.json", SupportedFormat.KLE)
        converter.save_file(layout, "output.json", SupportedFormat.VIA)
        
        # Direct conversion
        converter.convert_file("input.json", SupportedFormat.KLE, 
                             "output.c", SupportedFormat.KEYMAP)
    """
    
    def __init__(self):
        """Initialize the converter with parsers and generators."""
        # Map formats to parser and generator functions
        self.parsers = {
            SupportedFormat.KLE: parse_kle_file,
            SupportedFormat.VIA: parse_via_file,
            SupportedFormat.KEYMAP: parse_keymap_file,
            SupportedFormat.QMK_CONFIGURATOR: parse_qmk_configurator_file
        }
        
        self.generators = {
            SupportedFormat.KLE: generate_kle_file,
            SupportedFormat.VIA: generate_via_file,
            SupportedFormat.KEYMAP: generate_keymap_file,
            SupportedFormat.QMK_CONFIGURATOR: generate_qmk_configurator_file
        }
    
    def detect_format(self, file_path: Union[str, Path]) -> Optional[SupportedFormat]:
        """
        Automatically detect the format of a file based on content and extension.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Detected format or None if unable to determine
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return None
        
        # Check file extension first
        extension = file_path.suffix.lower()
        if extension == '.c':
            return SupportedFormat.KEYMAP
        elif extension in ['.json', '.kle']:
            # Need to examine content to distinguish KLE vs VIA
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                if not content:
                    return None
                
                # Try to parse as JSON
                data = json.loads(content)
                
                # Detect QMK Configurator format characteristics (check first as it's most specific)
                if isinstance(data, dict):
                    qmk_configurator_indicators = ['keyboard', 'layers', 'version']
                    has_keyboard_and_layers = 'keyboard' in data and 'layers' in data
                    if has_keyboard_and_layers and isinstance(data.get('layers'), list):
                        return SupportedFormat.QMK_CONFIGURATOR
                
                # Detect VIA format characteristics
                if isinstance(data, dict):
                    # VIA files typically have these structure elements
                    via_indicators = ['name', 'vendorId', 'productId', 'layouts', 'keycodes']
                    if any(key in data for key in via_indicators):
                        return SupportedFormat.VIA
                
                # KLE format is typically an array or has KLE-specific structure
                if isinstance(data, list) or 'meta' in data:
                    return SupportedFormat.KLE
                    
            except (json.JSONDecodeError, UnicodeDecodeError):
                # If JSON parsing fails, might be keymap.c with .json extension
                return SupportedFormat.KEYMAP
        
        # Check content patterns for keymap.c files without .c extension
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for QMK keymap patterns
            qmk_patterns = ['LAYOUT(', 'const uint16_t PROGMEM', '#include QMK_KEYBOARD_H']
            if any(pattern in content for pattern in qmk_patterns):
                return SupportedFormat.KEYMAP
                
        except UnicodeDecodeError:
            pass
        
        return None
    
    def load_file(self, file_path: Union[str, Path], 
                  format_type: Optional[SupportedFormat] = None) -> UniversalLayout:
        """
        Load a keyboard layout file and convert it to universal format.
        
        Args:
            file_path: Path to the input file
            format_type: Format of the input file (auto-detected if None)
            
        Returns:
            UniversalLayout object representing the keyboard layout
            
        Raises:
            ValueError: If format cannot be determined or is unsupported
            FileNotFoundError: If the input file doesn't exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        # Auto-detect format if not provided
        if format_type is None:
            format_type = self.detect_format(file_path)
            if format_type is None:
                raise ValueError(f"Unable to detect format for file: {file_path}")
        
        # Load using appropriate parser function
        parser_func = self.parsers[format_type]
        return parser_func(str(file_path))
    
    def save_file(self, layout: UniversalLayout, 
                  file_path: Union[str, Path], 
                  format_type: SupportedFormat) -> None:
        """
        Save a universal layout to a file in the specified format.
        
        Args:
            layout: UniversalLayout object to save
            file_path: Path where to save the output file
            format_type: Format to save the file in
            
        Raises:
            ValueError: If the format is unsupported
        """
        file_path = Path(file_path)
        
        # Validate the layout before saving
        validation_errors = layout.validate()
        if validation_errors:
            print("Warning: Layout validation errors found:")
            for error in validation_errors:
                print(f"  - {error}")
        
        # Generate using appropriate generator function
        generator_func = self.generators[format_type]
        generator_func(layout, str(file_path))
    
    def convert_file(self, input_path: Union[str, Path], 
                     input_format: Optional[SupportedFormat],
                     output_path: Union[str, Path], 
                     output_format: SupportedFormat) -> None:
        """
        Convert a file from one format to another.
        
        Args:
            input_path: Path to the input file
            input_format: Format of the input file (auto-detected if None)
            output_path: Path where to save the converted file
            output_format: Format to convert to
        """
        # Load the input file
        layout = self.load_file(input_path, input_format)
        
        # Save in the target format
        self.save_file(layout, output_path, output_format)
        
        print(f"Successfully converted {input_path} ({input_format or 'auto'}) "
              f"to {output_path} ({output_format.value})")
    
    def convert_string(self, input_data: str, 
                      input_format: SupportedFormat,
                      output_format: SupportedFormat) -> str:
        """
        Convert layout data from string input to string output.
        
        Args:
            input_data: String containing the input layout data
            input_format: Format of the input data
            output_format: Format to convert to
            
        Returns:
            String containing the converted layout data
        """
        # Parse using appropriate parser
        parser = self.parsers[input_format]
        layout = parser.parse_string(input_data)
        
        # Generate using appropriate generator
        generator = self.generators[output_format]
        return generator.generate_string(layout)
    
    def validate_file(self, file_path: Union[str, Path], 
                     format_type: Optional[SupportedFormat] = None) -> Dict[str, Any]:
        """
        Validate a keyboard layout file and return validation results.
        
        Args:
            file_path: Path to the file to validate
            format_type: Format of the file (auto-detected if None)
            
        Returns:
            Dictionary containing validation results
        """
        try:
            layout = self.load_file(file_path, format_type)
            errors = layout.validate()
            summary = layout.summary()
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "summary": summary,
                "format": format_type.value if format_type else "auto-detected"
            }
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Failed to parse file: {str(e)}"],
                "summary": {},
                "format": format_type.value if format_type else "unknown"
            }
    
    def list_supported_formats(self) -> Dict[str, str]:
        """
        Get a list of supported formats with descriptions.
        
        Returns:
            Dictionary mapping format names to descriptions
        """
        return {
            "kle": "Keyboard Layout Editor JSON format (keyboard-layout-editor.com)",
            "via": "VIA keymap JSON specification format (caniusevia.com)",
            "keymap": "QMK keymap.c source file format",
            "qmk_configurator": "QMK Configurator JSON format (config.qmk.fm)"
        }
    
    def get_format_info(self, format_type: SupportedFormat) -> Dict[str, Any]:
        """
        Get detailed information about a specific format.
        
        Args:
            format_type: Format to get information about
            
        Returns:
            Dictionary containing format information
        """
        format_info = {
            SupportedFormat.KLE: {
                "name": "Keyboard Layout Editor",
                "extension": ".json",
                "description": "Visual keyboard layout format from keyboard-layout-editor.com",
                "features": ["Physical layout", "Key positioning", "Visual styling", "Key labels"],
                "url": "https://keyboard-layout-editor.com"
            },
            SupportedFormat.VIA: {
                "name": "VIA Keymap Format", 
                "extension": ".json",
                "description": "VIA/VIAL keymap specification format",
                "features": ["Keymap layers", "Keyboard metadata", "Matrix definitions", "Feature flags"],
                "url": "https://caniusevia.com/docs/specification"
            },
            SupportedFormat.KEYMAP: {
                "name": "QMK Keymap Source",
                "extension": ".c", 
                "description": "QMK firmware keymap source code",
                "features": ["Layer definitions", "Custom functions", "Compile-ready code", "QMK macros"],
                "url": "https://docs.qmk.fm"
            },
            SupportedFormat.QMK_CONFIGURATOR: {
                "name": "QMK Configurator",
                "extension": ".json",
                "description": "QMK Configurator JSON format from config.qmk.fm",
                "features": ["Flat layer arrays", "Keyboard metadata", "Direct QMK compatibility", "Web editor export"],
                "url": "https://config.qmk.fm"
            }
        }
        
        return format_info.get(format_type, {})
