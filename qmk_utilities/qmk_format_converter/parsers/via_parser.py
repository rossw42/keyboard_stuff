"""
VIA Parser

This module implements parsing of VIA JSON format to the universal layout data model.
"""

import json
from typing import Dict, List, Any, Union, Optional, Tuple
from data_models.universal_layout import UniversalLayout, KeyDefinition, LayerDefinition
from data_models.keycode_mappings import KEYCODE_MAPPER


class VIAParseError(Exception):
    """Raised when VIA parsing fails."""
    pass


class VIAParser:
    """
    Parser for VIA JSON format.
    
    VIA format structure:
    - Metadata: version, vendor_id, product_id, etc.
    - Matrix: physical wiring matrix (rows, cols)
    - Layouts: physical layout with matrix coordinates
    - Keymaps: logical keymaps with QMK keycodes
    """
    
    def __init__(self):
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_props = {
            'w': 1.0,      # width
            'h': 1.0,      # height
            'x': 0.0,      # x offset
            'y': 0.0,      # y offset
            'r': 0.0,      # rotation angle
            'rx': 0.0,     # rotation x
            'ry': 0.0,     # rotation y
        }
    
    def parse_file(self, file_path: str) -> UniversalLayout:
        """Parse a VIA JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.parse_data(data)
        except (IOError, json.JSONDecodeError) as e:
            raise VIAParseError(f"Failed to read VIA file: {e}")
    
    def parse_json(self, json_str: str) -> UniversalLayout:
        """Parse VIA JSON string."""
        try:
            data = json.loads(json_str)
            return self.parse_data(data)
        except json.JSONDecodeError as e:
            raise VIAParseError(f"Invalid JSON: {e}")
    
    def parse_data(self, data: Dict[str, Any]) -> UniversalLayout:
        """Parse VIA data structure."""
        if not isinstance(data, dict):
            raise VIAParseError("VIA data must be an object")
        
        # Create layout object
        layout = UniversalLayout()
        
        # Parse metadata
        self._parse_metadata(layout, data)
        
        # Detect file format type (full or simplified)
        is_simplified_format = 'layers' in data and not data.get('layouts', {}).get('keymap')
        
        if is_simplified_format:
            # Simplified format (direct layers array)
            # Estimate reasonable matrix dimensions
            layers = data.get('layers', [])
            if not layers or not layers[0]:
                raise VIAParseError("No layers found in simplified VIA format")
            
            # Use first layer to determine key count
            key_count = len(layers[0])
            
            # Estimate reasonable matrix dimensions
            if key_count <= 60:  # 60% keyboard
                layout.matrix_rows = 5
                layout.matrix_cols = 14
            elif key_count <= 87:  # TKL
                layout.matrix_rows = 6
                layout.matrix_cols = 17
            else:  # Full-size or larger
                layout.matrix_rows = 6
                layout.matrix_cols = 21
            
            # Create keys with estimated positions
            keys = self._create_keys_from_count(key_count)
        else:
            # Standard format with explicit matrix
            # Parse matrix information
            matrix_info = data.get('matrix', {})
            layout.matrix_rows = matrix_info.get('rows', 1)
            layout.matrix_cols = matrix_info.get('cols', 1)
            
            # Parse physical layout
            layouts = data.get('layouts', {})
            keymap_layout = layouts.get('keymap', [])
            if not keymap_layout:
                raise VIAParseError("No keymap layout found")
            
            keys = self._parse_layout(keymap_layout)
        
        # Add keys to layout
        for key in keys:
            layout.add_key(key)
        
        # Parse keymaps (logical layers)
        if is_simplified_format:
            # In simplified format, layers are at the top level
            layers_data = data.get('layers', [])
            for layer_index, layer_keycodes in enumerate(layers_data):
                layer_name = f"Layer_{layer_index}"
                is_default = (layer_index == 0)
                
                # Validate keycode count
                if len(layer_keycodes) != len(keys):
                    # Pad or truncate to match key count
                    if len(layer_keycodes) < len(keys):
                        layer_keycodes.extend(["KC_TRNS"] * (len(keys) - len(layer_keycodes)))
                    else:
                        layer_keycodes = layer_keycodes[:len(keys)]
                
                layer = LayerDefinition(
                    name=layer_name,
                    index=layer_index,
                    keycodes=layer_keycodes.copy(),
                    is_default=is_default
                )
                layout.add_layer(layer)
                
                # Update key keycodes from first layer
                if layer_index == 0:
                    for i, key in enumerate(keys):
                        if i < len(layer_keycodes):
                                key.keycode = layer_keycodes[i]
                                # Update label based on keycode if not None
                                if key.keycode:  # Check to ensure keycode is not None
                                    mapping = KEYCODE_MAPPER.get_mapping(key.keycode)
                                    if mapping and mapping.kle_label:
                                        key.primary_label = mapping.kle_label
        else:
            # Standard format with keymaps array
            keymaps = data.get('keymaps', [])
            if keymaps:
                for keymap in keymaps:
                    layers = self._parse_keymap(keymap, len(keys))
                    for layer in layers:
                        layout.add_layer(layer)
                        
                    # Update key keycodes from first layer
                    if layers and len(layers[0].keycodes) == len(keys):
                        for i, key in enumerate(keys):
                            if i < len(layers[0].keycodes):
                                key.keycode = layers[0].keycodes[i]
                                # Update label based on keycode if not None
                                if key.keycode:  # Check to ensure keycode is not None
                                    mapping = KEYCODE_MAPPER.get_mapping(key.keycode)
                                    if mapping and mapping.kle_label:
                                        key.primary_label = mapping.kle_label
            else:
                # Create default layer if no keymaps provided
                default_layer = LayerDefinition(
                    name="Default",
                    index=0,
                    keycodes=["KC_TRNS"] * len(keys),
                    is_default=True
                )
                layout.add_layer(default_layer)
        
        # Set layout properties
        layout.name = layout.name or "VIA Layout"
        layout.layout_name = "LAYOUT"
        
        return layout
    
    def _parse_metadata(self, layout: UniversalLayout, data: Dict[str, Any]):
        """Parse VIA metadata."""
        # Basic metadata
        if 'name' in data:
            layout.name = str(data['name'])
        if 'vendor_id' in data:
            layout.vendor_id = str(data['vendor_id'])
        if 'product_id' in data:
            layout.product_id = str(data['product_id'])
        if 'manufacturer' in data:
            layout.manufacturer = str(data['manufacturer'])
        if 'product' in data:
            layout.product = str(data['product'])
        
        # Store raw VIA metadata
        layout.via_metadata = {
            'version': data.get('version', 1),
            'lighting': data.get('lighting', 'none'),
            'vendor_id': data.get('vendor_id'),
            'product_id': data.get('product_id'),
        }
    
    def _parse_layout(self, layout_data: List[List[Union[str, Dict[str, Any]]]]) -> List[KeyDefinition]:
        """Parse VIA physical layout."""
        keys = []
        self.current_x = 0.0
        self.current_y = 0.0
        
        for row_index, row in enumerate(layout_data):
            row_keys = self._parse_layout_row(row, row_index)
            keys.extend(row_keys)
            # Move to next row
            self._next_row()
        
        return keys
    
    def _parse_layout_row(self, row: List[Union[str, Dict[str, Any]]], row_index: int) -> List[KeyDefinition]:
        """Parse a single layout row."""
        keys = []
        
        for element in row:
            if isinstance(element, dict):
                # Formatting properties
                self._update_properties(element)
            elif isinstance(element, str):
                # Matrix coordinate (e.g., "0,0", "1,5")
                key = self._create_key_from_coordinate(element, row_index)
                keys.append(key)
                self._advance_position()
            else:
                raise VIAParseError(f"Invalid layout element: {element}")
        
        return keys
    
    def _create_key_from_coordinate(self, coordinate: str, row_index: int) -> KeyDefinition:
        """Create a KeyDefinition from a matrix coordinate."""
        try:
            # Parse matrix coordinate (e.g., "0,0" -> row=0, col=0)
            parts = coordinate.split(',')
            if len(parts) != 2:
                raise ValueError(f"Invalid coordinate format: {coordinate}")
            
            matrix_row = int(parts[0])
            matrix_col = int(parts[1])
            
        except ValueError as e:
            raise VIAParseError(f"Invalid matrix coordinate '{coordinate}': {e}")
        
        # Create key definition
        key = KeyDefinition(
            # Physical properties
            x=self.current_x,
            y=self.current_y,
            width=float(self.current_props['w']),
            height=float(self.current_props['h']),
            rotation_angle=float(self.current_props['r']),
            rotation_x=float(self.current_props['rx']),
            rotation_y=float(self.current_props['ry']),
            
            # Matrix properties
            matrix_row=matrix_row,
            matrix_col=matrix_col,
            
            # Labels (will be populated from keymaps)
            primary_label=f"{matrix_row},{matrix_col}",
            secondary_labels=[],
            
            # Default keycode (will be overridden by keymap)
            keycode="KC_TRNS"
        )
        
        return key
    
    def _update_properties(self, props: Dict[str, Any]):
        """Update current formatting properties."""
        # Handle position offsets
        if 'x' in props:
            self.current_x += float(props['x'])
        if 'y' in props:
            self.current_y += float(props['y'])
        
        # Update current properties
        for key, value in props.items():
            if key in self.current_props:
                self.current_props[key] = value
    
    def _advance_position(self):
        """Advance position after placing a key."""
        # Move X position by key width
        self.current_x += float(self.current_props['w'])
        
        # Reset single-use properties
        self.current_props['w'] = 1.0
        self.current_props['h'] = 1.0
        self.current_props['x'] = 0.0
        self.current_props['y'] = 0.0
    
    def _next_row(self):
        """Move to the next layout row."""
        self.current_x = 0.0
        self.current_y += 1.0  # Standard row spacing
    
    def _parse_keymap(self, keymap_data: Dict[str, Any], key_count: int) -> List[LayerDefinition]:
        """Parse a VIA keymap (contains multiple layers)."""
        layers = []
        keymap_name = keymap_data.get('name', 'Unknown')
        layer_data = keymap_data.get('layers', [])
        
        for layer_index, layer_keycodes in enumerate(layer_data):
            layer_name = f"{keymap_name}_L{layer_index}" if keymap_name != 'default' else f"Layer_{layer_index}"
            
            # Validate keycode count
            if len(layer_keycodes) != key_count:
                # Pad or truncate to match key count
                if len(layer_keycodes) < key_count:
                    layer_keycodes.extend(["KC_TRNS"] * (key_count - len(layer_keycodes)))
                else:
                    layer_keycodes = layer_keycodes[:key_count]
            
            layer = LayerDefinition(
                name=layer_name,
                index=layer_index,
                keycodes=layer_keycodes.copy(),
                is_default=(layer_index == 0)
            )
            
            layers.append(layer)
        
        return layers
    
    def _create_keys_from_count(self, key_count: int) -> List[KeyDefinition]:
        """Create keys with estimated positions based on count."""
        keys = []
        
        # Estimate a reasonable layout based on key count
        if key_count <= 60:  # 60% or smaller
            keys_per_row = [14, 14, 13, 12, 7]  # Approximate 60% layout
            row_offset = [0, 0.25, 0.375, 0.75, 1.25]  # Standard offsets
        elif key_count <= 87:  # TKL
            keys_per_row = [14, 14, 14, 14, 12, 8, 11]  # Approximate TKL layout
            row_offset = [0, 0, 0, 0, 0, 1.5, 1]  # Standard offsets
        else:  # Full-size or larger
            keys_per_row = [15, 15, 15, 15, 13, 12, 10]  # Approximate full-size
            row_offset = [0, 0, 0, 0, 0, 1.5, 1.5]  # Standard offsets
        
        key_index = 0
        current_row = 0
        
        while key_index < key_count and current_row < len(keys_per_row):
            row_keys = keys_per_row[current_row]
            offset = row_offset[current_row]
            
            for col in range(min(row_keys, key_count - key_index)):
                # Create key with sensible position
                key = KeyDefinition(
                    # Physical properties
                    x=col + offset,
                    y=current_row,
                    width=1.0,
                    height=1.0,
                    rotation_angle=0.0,
                    rotation_x=0.0,
                    rotation_y=0.0,
                    
                    # Matrix properties - estimate reasonable matrix position
                    matrix_row=current_row,
                    matrix_col=col,
                    
                    # Labels
                    primary_label=f"{current_row},{col}",
                    secondary_labels=[],
                    
                    # Default keycode
                    keycode="KC_TRNS"
                )
                keys.append(key)
                key_index += 1
            
            current_row += 1
        
        # If we still have keys left, add them to additional rows
        row = len(keys_per_row)
        while key_index < key_count:
            # Add additional keys in rows of 12
            cols_this_row = min(12, key_count - key_index)
            for col in range(cols_this_row):
                key = KeyDefinition(
                    x=col,
                    y=row,
                    width=1.0,
                    height=1.0,
                    rotation_angle=0.0,
                    rotation_x=0.0,
                    rotation_y=0.0,
                    matrix_row=row,
                    matrix_col=col,
                    primary_label=f"{row},{col}",
                    secondary_labels=[],
                    keycode="KC_TRNS"
                )
                keys.append(key)
                key_index += 1
            row += 1
            
        return keys

    def validate_via_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate VIA data structure and return any errors."""
        errors = []
        
        if not isinstance(data, dict):
            errors.append("VIA data must be an object")
            return errors
        
        # Detect format type
        is_simplified_format = 'layers' in data and not data.get('layouts', {}).get('keymap')
        
        if is_simplified_format:
            # Simplified format validation
            if 'name' not in data:
                errors.append("Missing 'name' field")
            
            if 'layers' not in data:
                errors.append("Missing 'layers' section")
            elif not isinstance(data['layers'], list):
                errors.append("'layers' must be an array")
            elif data['layers'] and not isinstance(data['layers'][0], list):
                errors.append("Each layer must be an array of keycodes")
        else:
            # Standard format validation
            if 'layouts' not in data:
                errors.append("Missing 'layouts' section")
            elif 'keymap' not in data['layouts']:
                errors.append("Missing 'keymap' in layouts section")
            elif not isinstance(data['layouts']['keymap'], list):
                errors.append("'keymap' must be an array")
            
            if 'matrix' not in data:
                errors.append("Missing 'matrix' section")
            elif not isinstance(data['matrix'], dict):
                errors.append("'matrix' must be an object")
            else:
                matrix = data['matrix']
                if 'rows' not in matrix or 'cols' not in matrix:
                    errors.append("Matrix must have 'rows' and 'cols'")
            
            # Validate keymaps if present
            if 'keymaps' in data:
                if not isinstance(data['keymaps'], list):
                    errors.append("'keymaps' must be an array")
                else:
                    for i, keymap in enumerate(data['keymaps']):
                        if not isinstance(keymap, dict):
                            errors.append(f"Keymap {i} must be an object")
                            continue
                        if 'layers' not in keymap:
                            errors.append(f"Keymap {i} missing 'layers'")
                        elif not isinstance(keymap['layers'], list):
                            errors.append(f"Keymap {i} 'layers' must be an array")
        
        return errors


def parse_via_file(file_path: str) -> UniversalLayout:
    """Convenience function to parse a VIA file."""
    parser = VIAParser()
    return parser.parse_file(file_path)


def parse_via_json(json_str: str) -> UniversalLayout:
    """Convenience function to parse VIA JSON string."""
    parser = VIAParser()
    return parser.parse_json(json_str)


def validate_via_file(file_path: str) -> List[str]:
    """Validate a VIA file and return any errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        parser = VIAParser()
        return parser.validate_via_data(data)
    except (IOError, json.JSONDecodeError) as e:
        return [f"Failed to read VIA file: {e}"]
