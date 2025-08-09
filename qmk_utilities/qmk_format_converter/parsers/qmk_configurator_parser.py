"""
QMK Configurator Parser

This module implements parsing of QMK Configurator JSON format to the universal layout data model.
QMK Configurator format is exported from config.qmk.fm and contains layers as flat arrays of keycodes.
"""

import json
from typing import Dict, List, Any, Optional
from data_models.universal_layout import UniversalLayout, KeyDefinition, LayerDefinition
from data_models.keycode_mappings import KEYCODE_MAPPER


class QMKConfiguratorParseError(Exception):
    """Raised when QMK Configurator parsing fails."""
    pass


class QMKConfiguratorParser:
    """
    Parser for QMK Configurator JSON format.
    
    QMK Configurator format structure:
    - version: Format version (typically 1)
    - keyboard: Keyboard identifier (e.g., "lily58/rev1")
    - keymap: Keymap name
    - layout: Layout function name (e.g., "LAYOUT")
    - layers: Array of arrays, each containing keycode strings
    - notes: Optional notes
    - documentation: Optional documentation string
    - author: Optional author
    """
    
    # Known keyboard layouts - maps keyboard name to key count and layout info
    KEYBOARD_LAYOUTS = {
        "lily58/rev1": {
            "key_count": 58,
            "name": "Lily58 Rev1",
            "layout": "LAYOUT"
        },
        "lily58": {
            "key_count": 58,
            "name": "Lily58",
            "layout": "LAYOUT"
        },
        # Add more keyboards as needed
        "corne": {
            "key_count": 42,
            "name": "Corne",
            "layout": "LAYOUT_split_3x6_3"
        },
        "planck/rev6": {
            "key_count": 47,
            "name": "Planck Rev6", 
            "layout": "LAYOUT_planck_grid"
        }
    }
    
    def __init__(self):
        pass
    
    def parse_file(self, file_path: str) -> UniversalLayout:
        """Parse a QMK Configurator JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.parse_data(data)
        except (IOError, json.JSONDecodeError) as e:
            raise QMKConfiguratorParseError(f"Failed to read QMK Configurator file: {e}")
    
    def parse_json(self, json_str: str) -> UniversalLayout:
        """Parse QMK Configurator JSON string."""
        try:
            data = json.loads(json_str)
            return self.parse_data(data)
        except json.JSONDecodeError as e:
            raise QMKConfiguratorParseError(f"Invalid JSON: {e}")
    
    def parse_data(self, data: Dict[str, Any]) -> UniversalLayout:
        """Parse QMK Configurator data structure."""
        if not isinstance(data, dict):
            raise QMKConfiguratorParseError("QMK Configurator data must be an object")
        
        # Validate required fields
        errors = self.validate_qmk_configurator_data(data)
        if errors:
            raise QMKConfiguratorParseError(f"Invalid QMK Configurator format: {'; '.join(errors)}")
        
        # Create layout object
        layout = UniversalLayout()
        
        # Parse metadata
        self._parse_metadata(layout, data)
        
        # Get keyboard info
        keyboard = data.get('keyboard', 'unknown')
        keyboard_info = self.KEYBOARD_LAYOUTS.get(keyboard, {
            "key_count": len(data['layers'][0]) if data.get('layers') else 0,
            "name": keyboard,
            "layout": data.get('layout', 'LAYOUT')
        })
        
        # Parse layers
        layers_data = data.get('layers', [])
        if not layers_data:
            raise QMKConfiguratorParseError("No layers found")
        
        # Create keys based on the first layer
        first_layer = layers_data[0]
        keys = self._create_keys_from_layer(first_layer, keyboard_info)
        
        # Add keys to layout
        for key in keys:
            layout.add_key(key)
        
        # Clear default layers before adding parsed layers
        layout.layers = []
        
        # Parse all layers
        for layer_index, layer_keycodes in enumerate(layers_data):
            layer = self._parse_layer(layer_keycodes, layer_index, len(keys))
            layout.add_layer(layer)
            
            # Update key keycodes from first layer
            if layer_index == 0 and len(layer.keycodes) == len(keys):
                for i, key in enumerate(keys):
                    if i < len(layer.keycodes):
                        key.keycode = layer.keycodes[i]
                        # Update label based on keycode
                        mapping = KEYCODE_MAPPER.get_mapping(key.keycode)
                        if mapping and mapping.kle_label:
                            key.primary_label = mapping.kle_label
                        else:
                            key.primary_label = key.keycode.replace('KC_', '')
        
        # Set layout properties
        layout.name = layout.name or keyboard_info.get('name', 'QMK Layout')
        layout.layout_name = data.get('layout', keyboard_info.get('layout', 'LAYOUT'))
        layout.keyboard = keyboard
        
        return layout
    
    def _parse_metadata(self, layout: UniversalLayout, data: Dict[str, Any]):
        """Parse QMK Configurator metadata."""
        # Basic metadata
        layout.name = data.get('keymap', 'QMK Configurator Layout')
        layout.keyboard = data.get('keyboard', 'unknown')
        layout.layout_name = data.get('layout', 'LAYOUT')
        
        # Store QMK Configurator specific metadata
        layout.qmk_configurator_metadata = {
            'version': data.get('version', 1),
            'notes': data.get('notes', ''),
            'documentation': data.get('documentation', ''),
            'author': data.get('author', ''),
            'keyboard': data.get('keyboard', ''),
            'keymap': data.get('keymap', ''),
            'layout': data.get('layout', 'LAYOUT')
        }
    
    def _create_keys_from_layer(self, layer_keycodes: List[str], keyboard_info: Dict[str, Any]) -> List[KeyDefinition]:
        """Create KeyDefinition objects from a layer's keycodes."""
        keys = []
        key_count = len(layer_keycodes)
        
        # Create a simple grid layout for unknown keyboards
        # We'll estimate rows/cols based on common keyboard layouts
        if key_count <= 12:  # Small layouts like numpad
            cols = 3
            rows = (key_count + cols - 1) // cols
        elif key_count <= 30:  # 30% keyboards
            cols = 10
            rows = (key_count + cols - 1) // cols
        elif key_count <= 50:  # 40% keyboards
            cols = 12
            rows = (key_count + cols - 1) // cols
        elif key_count <= 70:  # 60% keyboards
            cols = 15
            rows = (key_count + cols - 1) // cols
        else:  # Full size keyboards
            cols = 21
            rows = (key_count + cols - 1) // cols
        
        for i, keycode in enumerate(layer_keycodes):
            # Calculate position in grid
            row = i // cols
            col = i % cols
            
            # Create key definition
            key = KeyDefinition(
                # Physical properties - simple grid layout
                x=float(col),
                y=float(row),
                width=1.0,
                height=1.0,
                rotation_angle=0.0,
                rotation_x=0.0,
                rotation_y=0.0,
                
                # Matrix properties
                matrix_row=row,
                matrix_col=col,
                
                # Labels
                primary_label=keycode.replace('KC_', '') if keycode.startswith('KC_') else keycode,
                secondary_labels=[],
                
                # Keycode
                keycode=keycode
            )
            
            keys.append(key)
        
        return keys
    
    def _parse_layer(self, layer_keycodes: List[str], layer_index: int, expected_key_count: int) -> LayerDefinition:
        """Parse a single layer from QMK Configurator format."""
        layer_name = f"Layer_{layer_index}" if layer_index > 0 else "Default"
        
        # Validate keycode count
        if len(layer_keycodes) != expected_key_count:
            # Pad or truncate to match expected key count
            if len(layer_keycodes) < expected_key_count:
                layer_keycodes = layer_keycodes + ["KC_TRNS"] * (expected_key_count - len(layer_keycodes))
            else:
                layer_keycodes = layer_keycodes[:expected_key_count]
        
        layer = LayerDefinition(
            name=layer_name,
            index=layer_index,
            keycodes=layer_keycodes.copy(),
            is_default=(layer_index == 0)
        )
        
        return layer
    
    def validate_qmk_configurator_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate QMK Configurator data structure and return any errors."""
        errors = []
        
        if not isinstance(data, dict):
            errors.append("QMK Configurator data must be an object")
            return errors
        
        # Check required fields
        required_fields = ['keyboard', 'layers']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: '{field}'")
        
        # Validate layers
        if 'layers' in data:
            layers = data['layers']
            if not isinstance(layers, list):
                errors.append("'layers' must be an array")
            elif len(layers) == 0:
                errors.append("'layers' array cannot be empty")
            else:
                # Check that all layers have the same number of keycodes
                first_layer_length = len(layers[0]) if layers else 0
                for i, layer in enumerate(layers):
                    if not isinstance(layer, list):
                        errors.append(f"Layer {i} must be an array")
                    elif len(layer) != first_layer_length:
                        errors.append(f"Layer {i} has {len(layer)} keycodes, expected {first_layer_length}")
                    else:
                        # Check that all keycodes are strings
                        for j, keycode in enumerate(layer):
                            if not isinstance(keycode, str):
                                errors.append(f"Layer {i}, key {j}: keycode must be a string, got {type(keycode)}")
        
        # Validate optional fields
        if 'version' in data and not isinstance(data['version'], int):
            errors.append("'version' must be an integer")
        
        if 'keyboard' in data and not isinstance(data['keyboard'], str):
            errors.append("'keyboard' must be a string")
        
        if 'keymap' in data and not isinstance(data['keymap'], str):
            errors.append("'keymap' must be a string")
        
        if 'layout' in data and not isinstance(data['layout'], str):
            errors.append("'layout' must be a string")
        
        return errors
    
    @staticmethod
    def detect_format(data: Dict[str, Any]) -> bool:
        """Detect if data is in QMK Configurator format."""
        if not isinstance(data, dict):
            return False
        
        # Check for required QMK Configurator fields
        required_fields = ['keyboard', 'layers']
        has_required = all(field in data for field in required_fields)
        
        # Check for typical QMK Configurator structure
        has_layers_array = isinstance(data.get('layers'), list)
        has_version = 'version' in data
        has_layout = 'layout' in data
        
        return has_required and has_layers_array and (has_version or has_layout)


def parse_qmk_configurator_file(file_path: str) -> UniversalLayout:
    """Convenience function to parse a QMK Configurator file."""
    parser = QMKConfiguratorParser()
    return parser.parse_file(file_path)


def parse_qmk_configurator_json(json_str: str) -> UniversalLayout:
    """Convenience function to parse QMK Configurator JSON string."""
    parser = QMKConfiguratorParser()
    return parser.parse_json(json_str)


def validate_qmk_configurator_file(file_path: str) -> List[str]:
    """Validate a QMK Configurator file and return any errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        parser = QMKConfiguratorParser()
        return parser.validate_qmk_configurator_data(data)
    except (IOError, json.JSONDecodeError) as e:
        return [f"Failed to read QMK Configurator file: {e}"]


def detect_qmk_configurator_format(file_path: str) -> bool:
    """Detect if a file is in QMK Configurator format."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return QMKConfiguratorParser.detect_format(data)
    except (IOError, json.JSONDecodeError):
        return False
