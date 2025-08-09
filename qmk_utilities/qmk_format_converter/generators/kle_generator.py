"""
KLE Generator

This module implements generation of KLE (Keyboard Layout Editor) JSON format
from the universal layout data model.
"""

import json
from typing import Dict, List, Any, Union, Optional, Tuple
from data_models.universal_layout import UniversalLayout, KeyDefinition, LayerDefinition
from data_models.keycode_mappings import KEYCODE_MAPPER


class KLEGenerateError(Exception):
    """Raised when KLE generation fails."""
    pass


class KLEGenerator:
    """
    Generator for KLE (Keyboard Layout Editor) JSON format.
    
    Converts UniversalLayout objects back to KLE format with:
    - Metadata object (first element)
    - Row-based layout with key labels and formatting
    - Proper handling of key properties (width, height, rotation, colors)
    """
    
    def __init__(self):
        self.current_row = 0
        self.current_x = 0.0
        self.current_y = 0.0
        
        # Track current formatting properties
        self.current_props = {
            'w': 1.0,      # width
            'h': 1.0,      # height
            'x': 0.0,      # x offset
            'y': 0.0,      # y offset
            'r': 0.0,      # rotation angle
            'rx': 0.0,     # rotation x
            'ry': 0.0,     # rotation y
            'c': '#cccccc', # color
            't': '#000000', # text color
            'f': 3,        # font size
            'a': 4,        # alignment
            'p': 'OEM'     # profile
        }
    
    def generate_file(self, layout: UniversalLayout, file_path: str):
        """Generate KLE JSON file from layout."""
        kle_data = self.generate_data(layout)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(kle_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise KLEGenerateError(f"Failed to write KLE file: {e}")
    
    def generate_json(self, layout: UniversalLayout) -> str:
        """Generate KLE JSON string from layout."""
        kle_data = self.generate_data(layout)
        try:
            return json.dumps(kle_data, indent=2, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise KLEGenerateError(f"Failed to serialize KLE JSON: {e}")
    
    def generate_data(self, layout: UniversalLayout) -> List[Any]:
        """Generate KLE data structure from layout."""
        if not layout.keys:
            raise KLEGenerateError("Layout has no keys to generate")
        
        # Reset generator state
        self._reset_state()
        
        kle_data = []
        
        # Add metadata as first element
        metadata = self._generate_metadata(layout)
        if metadata:
            kle_data.append(metadata)
        
        # Generate layout rows
        rows = self._generate_layout_rows(layout.keys)
        kle_data.extend(rows)
        
        return kle_data
    
    def _reset_state(self):
        """Reset generator state."""
        self.current_row = 0
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_props = {
            'w': 1.0, 'h': 1.0, 'x': 0.0, 'y': 0.0,
            'r': 0.0, 'rx': 0.0, 'ry': 0.0,
            'c': '#cccccc', 't': '#000000', 'f': 3, 'a': 4, 'p': 'OEM'
        }
    
    def _generate_metadata(self, layout: UniversalLayout) -> Optional[Dict[str, Any]]:
        """Generate metadata object for KLE."""
        metadata = {}
        
        if layout.name:
            metadata['name'] = layout.name
        if layout.author:
            metadata['author'] = layout.author
        if layout.description:
            metadata['notes'] = layout.description
        if layout.version:
            metadata['version'] = layout.version
        
        # Add background color if available
        if hasattr(layout, 'background_color'):
            metadata['background'] = layout.background_color
        
        # Add switch and plate info if available
        if hasattr(layout, 'switch_mount'):
            metadata['switchMount'] = layout.switch_mount
        if hasattr(layout, 'switch_brand'):
            metadata['switchBrand'] = layout.switch_brand
        if hasattr(layout, 'switch_type'):
            metadata['switchType'] = layout.switch_type
        
        return metadata if metadata else None
    
    def _generate_layout_rows(self, keys: List[KeyDefinition]) -> List[List[Union[str, Dict[str, Any]]]]:
        """Generate layout rows from keys."""
        if not keys:
            return []
        
        # Group keys by Y coordinate (row)
        rows_dict = {}
        for key in keys:
            row_y = key.y
            if row_y not in rows_dict:
                rows_dict[row_y] = []
            rows_dict[row_y].append(key)
        
        # Sort rows by Y coordinate and keys within rows by X coordinate
        sorted_rows = []
        for y in sorted(rows_dict.keys()):
            row_keys = sorted(rows_dict[y], key=lambda k: k.x)
            sorted_rows.append(row_keys)
        
        # Generate KLE format for each row
        kle_rows = []
        for row_keys in sorted_rows:
            kle_row = self._generate_kle_row(row_keys)
            if kle_row:  # Only add non-empty rows
                kle_rows.append(kle_row)
        
        return kle_rows
    
    def _generate_kle_row(self, row_keys: List[KeyDefinition]) -> List[Union[str, Dict[str, Any]]]:
        """Generate a single KLE row from keys."""
        if not row_keys:
            return []
        
        kle_row = []
        expected_x = row_keys[0].x
        
        for key in row_keys:
            # Add positioning and formatting properties if needed
            props = self._get_key_properties(key, expected_x)
            if props:
                kle_row.append(props)
            
            # Add key label
            label = self._get_key_label(key)
            kle_row.append(label)
            
            # Update expected X position
            expected_x = key.x + key.width
        
        return kle_row
    
    def _get_key_properties(self, key: KeyDefinition, expected_x: float) -> Optional[Dict[str, Any]]:
        """Get key properties that differ from defaults."""
        props = {}
        
        # X offset (only if different from expected position)
        x_offset = key.x - expected_x
        if abs(x_offset) > 0.001:  # Floating point tolerance
            props['x'] = round(x_offset, 3)
        
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
        
        # Color properties
        if key.color and key.color != '#cccccc':
            props['c'] = key.color
        if key.text_color and key.text_color != '#000000':
            props['t'] = key.text_color
        
        # Font size
        if key.font_size and key.font_size != 3:
            props['f'] = key.font_size
        
        # Profile
        if hasattr(key, 'profile') and key.profile and key.profile != 'OEM':
            props['p'] = key.profile
        
        return props if props else None
    
    def _get_key_label(self, key: KeyDefinition) -> str:
        """Get the appropriate label for a key in KLE format."""
        # If key has secondary labels, create multi-line label
        if key.secondary_labels:
            lines = key.secondary_labels.copy()
            lines.append(key.primary_label or "")
            return '\n'.join(lines)
        
        # Use primary label if available
        if key.primary_label:
            return key.primary_label
        
        # Fall back to keycode conversion
        if key.keycode:
            mapping = KEYCODE_MAPPER.get_mapping(key.keycode)
            if mapping and mapping.kle_label:
                return mapping.kle_label
            # If no mapping, use keycode as label
            return key.keycode
        
        # Last resort: empty key
        return ""
    
    def validate_layout(self, layout: UniversalLayout) -> List[str]:
        """Validate layout for KLE generation."""
        errors = []
        
        if not layout.keys:
            errors.append("Layout has no keys")
            return errors
        
        # Check for valid key positions
        for i, key in enumerate(layout.keys):
            if key.x is None or key.y is None:
                errors.append(f"Key {i} missing position coordinates")
            
            if key.width is None or key.width <= 0:
                errors.append(f"Key {i} has invalid width: {key.width}")
            
            if key.height is None or key.height <= 0:
                errors.append(f"Key {i} has invalid height: {key.height}")
        
        # Check for overlapping keys (basic check)
        for i, key1 in enumerate(layout.keys):
            for j, key2 in enumerate(layout.keys[i+1:], i+1):
                if (abs(key1.x - key2.x) < 0.1 and 
                    abs(key1.y - key2.y) < 0.1):
                    errors.append(f"Keys {i} and {j} may be overlapping")
        
        return errors


def generate_kle_file(layout: UniversalLayout, file_path: str):
    """Convenience function to generate KLE file."""
    generator = KLEGenerator()
    generator.generate_file(layout, file_path)


def generate_kle_json(layout: UniversalLayout) -> str:
    """Convenience function to generate KLE JSON string."""
    generator = KLEGenerator()
    return generator.generate_json(layout)


def validate_layout_for_kle(layout: UniversalLayout) -> List[str]:
    """Validate layout for KLE generation."""
    generator = KLEGenerator()
    return generator.validate_layout(layout)
