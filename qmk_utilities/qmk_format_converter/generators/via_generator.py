"""
VIA Generator

This module implements generation of VIA JSON format
from the universal layout data model.
"""

import json
from typing import Dict, List, Any, Union, Optional, Tuple

# Handle both standalone and module execution
try:
    from ..data_models.universal_layout import UniversalLayout, KeyDefinition, LayerDefinition
    from ..data_models.keycode_mappings import KEYCODE_MAPPER
except ImportError:
    # Running as standalone script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from data_models.universal_layout import UniversalLayout, KeyDefinition, LayerDefinition
    from data_models.keycode_mappings import KEYCODE_MAPPER


class VIAGenerateError(Exception):
    """Raised when VIA generation fails."""
    pass


class VIAGenerator:
    """
    Generator for VIA JSON format.
    
    Converts UniversalLayout objects back to VIA format with:
    - Metadata (version, vendor_id, product_id, etc.)
    - Matrix dimensions
    - Physical layout with matrix coordinates
    - Keymaps with layers and keycodes
    """
    
    def __init__(self):
        pass
    
    def generate_file(self, layout: UniversalLayout, file_path: str):
        """Generate VIA JSON file from layout."""
        via_data = self.generate_data(layout)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(via_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise VIAGenerateError(f"Failed to write VIA file: {e}")
    
    def generate_json(self, layout: UniversalLayout) -> str:
        """Generate VIA JSON string from layout."""
        via_data = self.generate_data(layout)
        try:
            return json.dumps(via_data, indent=2, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise VIAGenerateError(f"Failed to serialize VIA JSON: {e}")
    
    def generate_data(self, layout: UniversalLayout) -> Dict[str, Any]:
        """Generate VIA data structure from layout."""
        if not layout.keys:
            raise VIAGenerateError("Layout has no keys to generate")
        
        via_data = {}
        
        # Add basic metadata in VIA format
        via_data['name'] = layout.name or "QMK Layout"
        via_data['vendorProductId'] = int(layout.vendor_id.replace('0x', ''), 16) if layout.vendor_id else 81324845
        
        # Add macros (empty for now)
        via_data['macros'] = []
        
        # Generate layers directly
        self._generate_layers(via_data, layout)
        
        # Add encoders (empty for now)
        via_data['encoders'] = []
        
        return via_data
    
    def _generate_layers(self, via_data: Dict[str, Any], layout: UniversalLayout):
        """Generate layers directly in VIA format."""
        if not layout.layers:
            # Create default empty layer
            default_keycodes = ['KC_TRNS'] * len(layout.keys)
            via_data['layers'] = [default_keycodes]
            return
        
        # Convert layers to simple keycode arrays
        layers = []
        for layer in layout.layers:
            if len(layer.keycodes) == len(layout.keys):
                layers.append(layer.keycodes.copy())
            else:
                # Pad or truncate to match key count
                layer_keycodes = layer.keycodes.copy()
                if len(layer_keycodes) < len(layout.keys):
                    layer_keycodes.extend(['KC_TRNS'] * (len(layout.keys) - len(layer_keycodes)))
                else:
                    layer_keycodes = layer_keycodes[:len(layout.keys)]
                layers.append(layer_keycodes)
        
        via_data['layers'] = layers
    
    def _generate_metadata(self, via_data: Dict[str, Any], layout: UniversalLayout):
        """Generate VIA metadata."""
        via_data['version'] = 1
        
        # Use VIA-specific metadata if available
        if hasattr(layout, 'via_metadata') and layout.via_metadata:
            metadata = layout.via_metadata
            via_data['vendor_id'] = metadata.get('vendor_id', '0x1234')
            via_data['product_id'] = metadata.get('product_id', '0x5678')
            via_data['lighting'] = metadata.get('lighting', 'none')
        else:
            # Default values or use layout properties
            via_data['vendor_id'] = layout.vendor_id or '0x1234'
            via_data['product_id'] = layout.product_id or '0x5678'
            via_data['lighting'] = 'none'
    
    def _generate_matrix(self, via_data: Dict[str, Any], layout: UniversalLayout):
        """Generate matrix information."""
        via_data['matrix'] = {
            'rows': layout.matrix_rows,
            'cols': layout.matrix_cols
        }
    
    def _generate_layout(self, via_data: Dict[str, Any], layout: UniversalLayout):
        """Generate physical layout structure."""
        # Group keys by Y coordinate (row)
        rows_dict = {}
        for key in layout.keys:
            row_y = key.y
            if row_y not in rows_dict:
                rows_dict[row_y] = []
            rows_dict[row_y].append(key)
        
        # Sort rows by Y coordinate and keys within rows by X coordinate
        keymap_layout = []
        for y in sorted(rows_dict.keys()):
            row_keys = sorted(rows_dict[y], key=lambda k: k.x)
            via_row = self._generate_via_row(row_keys)
            keymap_layout.append(via_row)
        
        via_data['layouts'] = {
            'keymap': keymap_layout
        }
    
    def _generate_via_row(self, row_keys: List[KeyDefinition]) -> List[Union[str, Dict[str, Any]]]:
        """Generate a single VIA layout row."""
        if not row_keys:
            return []
        
        via_row = []
        
        for key in row_keys:
            # Add formatting properties if needed
            props = self._get_key_properties(key)
            if props:
                via_row.append(props)
            
            # Add matrix coordinate
            coordinate = f"{key.matrix_row},{key.matrix_col}"
            via_row.append(coordinate)
        
        return via_row
    
    def _get_key_properties(self, key: KeyDefinition) -> Optional[Dict[str, Any]]:
        """Get key properties that differ from defaults."""
        props = {}
        
        # Width (only if not 1.0)
        if abs(key.width - 1.0) > 0.001:
            props['w'] = round(key.width, 3)
        
        # Height (only if not 1.0)
        if abs(key.height - 1.0) > 0.001:
            props['h'] = round(key.height, 3)
        
        # Rotation properties
        if abs(key.rotation_angle) > 0.001:
            props['r'] = round(key.rotation_angle, 1)
        if abs(key.rotation_x) > 0.001:
            props['rx'] = round(key.rotation_x, 3)
        if abs(key.rotation_y) > 0.001:
            props['ry'] = round(key.rotation_y, 3)
        
        return props if props else None
    
    def _generate_keymaps(self, via_data: Dict[str, Any], layout: UniversalLayout):
        """Generate keymaps section."""
        if not layout.layers:
            # Create default empty keymap
            default_keycodes = ['KC_TRNS'] * len(layout.keys)
            via_data['keymaps'] = [{
                'name': 'default',
                'layers': [default_keycodes]
            }]
            return
        
        # Group layers by keymap (assuming single keymap for now)
        layers = []
        for layer in layout.layers:
            if len(layer.keycodes) == len(layout.keys):
                layers.append(layer.keycodes.copy())
            else:
                # Pad or truncate to match key count
                layer_keycodes = layer.keycodes.copy()
                if len(layer_keycodes) < len(layout.keys):
                    layer_keycodes.extend(['KC_TRNS'] * (len(layout.keys) - len(layer_keycodes)))
                else:
                    layer_keycodes = layer_keycodes[:len(layout.keys)]
                layers.append(layer_keycodes)
        
        via_data['keymaps'] = [{
            'name': 'default',
            'layers': layers
        }]
    
    def validate_layout(self, layout: UniversalLayout) -> List[str]:
        """Validate layout for VIA generation."""
        errors = []
        
        if not layout.keys:
            errors.append("Layout has no keys")
            return errors
        
        # Check matrix coordinates
        for i, key in enumerate(layout.keys):
            if key.matrix_row is None or key.matrix_col is None:
                errors.append(f"Key {i} missing matrix coordinates")
        
        # Check matrix dimensions
        if not layout.matrix_rows or not layout.matrix_cols:
            errors.append("Missing matrix dimensions")
        
        # Validate matrix coordinates are within bounds
        for i, key in enumerate(layout.keys):
            if (key.matrix_row is not None and 
                key.matrix_row >= layout.matrix_rows):
                errors.append(f"Key {i} matrix row {key.matrix_row} exceeds matrix rows {layout.matrix_rows}")
            
            if (key.matrix_col is not None and 
                key.matrix_col >= layout.matrix_cols):
                errors.append(f"Key {i} matrix col {key.matrix_col} exceeds matrix cols {layout.matrix_cols}")
        
        return errors


def generate_via_file(layout: UniversalLayout, file_path: str):
    """Convenience function to generate VIA file."""
    generator = VIAGenerator()
    generator.generate_file(layout, file_path)


def generate_via_json(layout: UniversalLayout) -> str:
    """Convenience function to generate VIA JSON string."""
    generator = VIAGenerator()
    return generator.generate_json(layout)


def validate_layout_for_via(layout: UniversalLayout) -> List[str]:
    """Validate layout for VIA generation."""
    generator = VIAGenerator()
    return generator.validate_layout(layout)
