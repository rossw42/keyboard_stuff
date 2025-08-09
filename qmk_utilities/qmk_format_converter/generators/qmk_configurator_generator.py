"""
QMK Configurator Generator

This module implements generation of QMK Configurator JSON format from the universal layout data model.
QMK Configurator format is used by config.qmk.fm and contains layers as flat arrays of keycodes.
"""

import json
from typing import Dict, List, Any, Optional
from data_models.universal_layout import UniversalLayout, KeyDefinition, LayerDefinition


class QMKConfiguratorGenerateError(Exception):
    """Raised when QMK Configurator generation fails."""
    pass


class QMKConfiguratorGenerator:
    """
    Generator for QMK Configurator JSON format.
    
    Converts universal layout data to QMK Configurator format suitable for config.qmk.fm
    """
    
    def __init__(self):
        pass
    
    def generate_file(self, layout: UniversalLayout, file_path: str) -> None:
        """Generate a QMK Configurator JSON file."""
        try:
            data = self.generate_data(layout)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            raise QMKConfiguratorGenerateError(f"Failed to write QMK Configurator file: {e}")
    
    def generate_json(self, layout: UniversalLayout) -> str:
        """Generate QMK Configurator JSON string."""
        data = self.generate_data(layout)
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def generate_data(self, layout: UniversalLayout) -> Dict[str, Any]:
        """Generate QMK Configurator data structure."""
        if not layout:
            raise QMKConfiguratorGenerateError("Layout cannot be None")
        
        if not layout.keys:
            raise QMKConfiguratorGenerateError("Layout must have at least one key")
        
        if not layout.layers:
            raise QMKConfiguratorGenerateError("Layout must have at least one layer")
        
        # Build QMK Configurator data structure
        data = {}
        
        # Add metadata
        self._add_metadata(data, layout)
        
        # Add keyboard and layout information
        data['keyboard'] = layout.keyboard or 'unknown'
        data['keymap'] = layout.name or 'default_keymap'
        data['layout'] = layout.layout_name or 'LAYOUT'
        
        # Convert layers to flat arrays
        layers = self._generate_layers(layout)
        data['layers'] = layers
        
        return data
    
    def _add_metadata(self, data: Dict[str, Any], layout: UniversalLayout) -> None:
        """Add metadata to QMK Configurator data."""
        # Use stored QMK Configurator metadata if available
        if hasattr(layout, 'qmk_configurator_metadata') and layout.qmk_configurator_metadata:
            metadata = layout.qmk_configurator_metadata
            data['version'] = metadata.get('version', 1)
            data['notes'] = metadata.get('notes', '')
            data['documentation'] = metadata.get('documentation', 
                '"This file is a QMK Configurator export. You can import this at <https://config.qmk.fm>. '
                'It can also be used directly with QMK\'s source code.\n\n'
                'To setup your QMK environment check out the tutorial: <https://docs.qmk.fm/#/newbs>\n\n'
                'You can convert this file to a keymap.c using this command: `qmk json2c {keymap}`\n\n'
                'You can compile this keymap using this command: `qmk compile {keymap}`"\n')
            data['author'] = metadata.get('author', layout.author or '')
        else:
            # Generate default metadata
            data['version'] = 1
            data['notes'] = ''
            data['documentation'] = (
                '"This file is a QMK Configurator export. You can import this at <https://config.qmk.fm>. '
                'It can also be used directly with QMK\'s source code.\n\n'
                'To setup your QMK environment check out the tutorial: <https://docs.qmk.fm/#/newbs>\n\n'
                'You can convert this file to a keymap.c using this command: `qmk json2c {keymap}`\n\n'
                'You can compile this keymap using this command: `qmk compile {keymap}`"\n'
            )
            data['author'] = layout.author or ''
    
    def _generate_layers(self, layout: UniversalLayout) -> List[List[str]]:
        """Convert universal layout layers to QMK Configurator flat arrays."""
        layers = []
        
        # Sort layers by index to maintain proper order
        sorted_layers = sorted(layout.layers, key=lambda x: x.index)
        
        for layer in sorted_layers:
            layer_keycodes = self._generate_layer_keycodes(layer, layout)
            layers.append(layer_keycodes)
        
        return layers
    
    def _generate_layer_keycodes(self, layer: LayerDefinition, layout: UniversalLayout) -> List[str]:
        """Generate flat keycode array for a single layer."""
        keycodes = []
        
        # Use layer keycodes if available and correct length
        if layer.keycodes and len(layer.keycodes) == len(layout.keys):
            keycodes = layer.keycodes.copy()
        else:
            # Generate keycodes from key definitions
            for key in layout.keys:
                if key.keycode:
                    keycodes.append(key.keycode)
                else:
                    keycodes.append("KC_TRNS")
        
        # Ensure we have the right number of keycodes
        while len(keycodes) < len(layout.keys):
            keycodes.append("KC_TRNS")
        
        # Truncate if too many
        if len(keycodes) > len(layout.keys):
            keycodes = keycodes[:len(layout.keys)]
        
        return keycodes
    
    def validate_layout(self, layout: UniversalLayout) -> List[str]:
        """Validate that the layout can be converted to QMK Configurator format."""
        errors = []
        
        if not layout:
            errors.append("Layout cannot be None")
            return errors
        
        if not layout.keys:
            errors.append("Layout must have at least one key")
        
        if not layout.layers:
            errors.append("Layout must have at least one layer")
        
        # Check that all layers have matching keycode counts
        key_count = len(layout.keys)
        for i, layer in enumerate(layout.layers):
            if layer.keycodes and len(layer.keycodes) != key_count:
                errors.append(f"Layer {i} ({layer.name}): keycode count mismatch "
                            f"({len(layer.keycodes)} vs {key_count} keys)")
        
        # Check for valid keyboard identifier
        if not layout.keyboard or not layout.keyboard.strip():
            errors.append("Layout must have a valid keyboard identifier")
        
        return errors


def generate_qmk_configurator_file(layout: UniversalLayout, file_path: str) -> None:
    """Convenience function to generate a QMK Configurator file."""
    generator = QMKConfiguratorGenerator()
    generator.generate_file(layout, file_path)


def generate_qmk_configurator_json(layout: UniversalLayout) -> str:
    """Convenience function to generate QMK Configurator JSON string."""
    generator = QMKConfiguratorGenerator()
    return generator.generate_json(layout)


def validate_layout_for_qmk_configurator(layout: UniversalLayout) -> List[str]:
    """Validate a layout for QMK Configurator generation."""
    generator = QMKConfiguratorGenerator()
    return generator.validate_layout(layout)
