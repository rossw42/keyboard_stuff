"""
KLE Parser

This module implements parsing of KLE (Keyboard Layout Editor) JSON format
to the universal layout data model.
"""

import json
from typing import Dict, List, Any, Union, Optional, Tuple
from data_models.universal_layout import UniversalLayout, KeyDefinition, LayerDefinition
from data_models.keycode_mappings import KEYCODE_MAPPER


class KLEParseError(Exception):
    """Raised when KLE parsing fails."""
    pass


class KLEParser:
    """
    Parser for KLE (Keyboard Layout Editor) JSON format.
    
    KLE format consists of an array where:
    - First element can be metadata object
    - Subsequent elements are arrays representing keyboard rows
    - Each row contains keys (strings) and formatting objects
    """
    
    def __init__(self):
        self.current_row = 0
        self.current_col = 0
        self.current_x = 0.0
        self.current_y = 0.0
        
        # Current formatting state
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
    
    def parse_file(self, file_path: str) -> UniversalLayout:
        """Parse a KLE JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.parse_data(data)
        except (IOError, json.JSONDecodeError) as e:
            raise KLEParseError(f"Failed to read KLE file: {e}")
    
    def parse_json(self, json_str: str) -> UniversalLayout:
        """Parse KLE JSON string."""
        try:
            data = json.loads(json_str)
            return self.parse_data(data)
        except json.JSONDecodeError as e:
            raise KLEParseError(f"Invalid JSON: {e}")
    
    def parse_data(self, data: List[Any]) -> UniversalLayout:
        """Parse KLE data structure."""
        if not isinstance(data, list) or len(data) == 0:
            raise KLEParseError("KLE data must be a non-empty array")
        
        # Reset parser state
        self._reset_state()
        
        # Create layout object
        layout = UniversalLayout()
        
        # Parse metadata if present (first element is object)
        start_index = 0
        if isinstance(data[0], dict) and not self._is_key_property(data[0]):
            metadata = data[0]
            self._apply_metadata(layout, metadata)
            start_index = 1
        
        # Parse keyboard rows
        keys = []
        for i in range(start_index, len(data)):
            row_data = data[i]
            if isinstance(row_data, list):
                row_keys = self._parse_row(row_data)
                keys.extend(row_keys)
            else:
                raise KLEParseError(f"Row {i - start_index} must be an array")
        
        # Add keys to layout
        for key in keys:
            layout.add_key(key)
        
        # Create default layer with parsed keycodes
        default_keycodes = [key.keycode or "KC_TRNS" for key in keys]
        default_layer = LayerDefinition(
            name="Default",
            index=0,
            keycodes=default_keycodes,
            is_default=True
        )
        layout.layers = [default_layer]  # Replace the auto-generated layer
        
        # Set layout properties
        layout.name = layout.name or "KLE Layout"
        layout.layout_name = "LAYOUT"
        
        # Calculate matrix dimensions
        if keys:
            max_row = max(key.matrix_row or 0 for key in keys)
            max_col = max(key.matrix_col or 0 for key in keys) 
            layout.matrix_rows = max_row + 1
            layout.matrix_cols = max_col + 1
        
        return layout
    
    def _reset_state(self):
        """Reset parser state for new parsing."""
        self.current_row = 0
        self.current_col = 0
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_props = {
            'w': 1.0, 'h': 1.0, 'x': 0.0, 'y': 0.0,
            'r': 0.0, 'rx': 0.0, 'ry': 0.0,
            'c': '#cccccc', 't': '#000000', 'f': 3, 'a': 4, 'p': 'OEM'
        }
    
    def _apply_metadata(self, layout: UniversalLayout, metadata: Dict[str, Any]):
        """Apply metadata to layout object."""
        if 'name' in metadata:
            layout.name = str(metadata['name'])
        if 'author' in metadata:
            layout.author = str(metadata['author'])
        if 'notes' in metadata:
            layout.description = str(metadata['notes'])
        if 'version' in metadata:
            layout.version = str(metadata['version'])
        
        # Store raw KLE metadata
        layout.kle_metadata = metadata.copy()
    
    def _is_key_property(self, obj: Dict[str, Any]) -> bool:
        """Check if an object contains key properties rather than metadata."""
        key_props = {'w', 'h', 'x', 'y', 'r', 'rx', 'ry', 'c', 't', 'f', 'a', 'p'}
        return bool(set(obj.keys()) & key_props)
    
    def _parse_row(self, row: List[Union[str, Dict[str, Any]]]) -> List[KeyDefinition]:
        """Parse a single keyboard row."""
        keys = []
        
        for element in row:
            if isinstance(element, dict):
                # Property object - update current formatting
                self._update_properties(element)
            elif isinstance(element, str):
                # Key label - create key
                key = self._create_key(element)
                keys.append(key)
                self._advance_position()
            else:
                raise KLEParseError(f"Invalid row element: {element}")
        
        # Move to next row
        self._next_row()
        
        return keys
    
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
    
    def _create_key(self, label: str) -> KeyDefinition:
        """Create a KeyDefinition from a key label."""
        # Parse keycode from label
        keycode = KEYCODE_MAPPER.parse_kle_key_label(label)
        
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
            
            # Visual properties
            color=str(self.current_props['c']),
            text_color=str(self.current_props['t']),
            font_size=int(self.current_props['f']),
            
            # Logical properties
            matrix_row=self.current_row,
            matrix_col=self.current_col,
            keycode=keycode,
            
            # Labels
            primary_label=self._extract_primary_label(label),
            secondary_labels=self._extract_secondary_labels(label),
            
            # Metadata
            profile=str(self.current_props.get('p', 'OEM'))
        )
        
        return key
    
    def _extract_primary_label(self, label: str) -> str:
        """Extract the primary (bottom) label from a KLE key label."""
        if not label:
            return ""
        
        # Handle multi-line labels
        lines = label.split('\n')
        if len(lines) > 1:
            # Use the bottom line as primary
            return lines[-1].strip()
        else:
            return lines[0].strip()
    
    def _extract_secondary_labels(self, label: str) -> List[str]:
        """Extract secondary labels from a KLE key label."""
        if not label or '\n' not in label:
            return []
        
        lines = label.split('\n')
        if len(lines) > 1:
            # All lines except the last (primary) are secondary
            return [line.strip() for line in lines[:-1] if line.strip()]
        
        return []
    
    def _advance_position(self):
        """Advance position after placing a key."""
        # Move X position by key width
        self.current_x += float(self.current_props['w'])
        self.current_col += 1
        
        # Reset single-use properties
        self.current_props['w'] = 1.0
        self.current_props['h'] = 1.0
        self.current_props['x'] = 0.0
        self.current_props['y'] = 0.0
    
    def _next_row(self):
        """Move to the next keyboard row."""
        self.current_row += 1
        self.current_col = 0
        self.current_x = 0.0
        self.current_y += 1.0  # Standard row spacing
    
    def validate_kle_data(self, data: List[Any]) -> List[str]:
        """Validate KLE data structure and return any errors."""
        errors = []
        
        if not isinstance(data, list):
            errors.append("KLE data must be an array")
            return errors
        
        if len(data) == 0:
            errors.append("KLE data cannot be empty")
            return errors
        
        # Check for valid structure
        start_index = 0
        if isinstance(data[0], dict) and not self._is_key_property(data[0]):
            start_index = 1
        
        if start_index >= len(data):
            errors.append("No keyboard rows found")
            return errors
        
        # Validate rows
        for i in range(start_index, len(data)):
            if not isinstance(data[i], list):
                errors.append(f"Row {i - start_index} must be an array")
                continue
            
            # Validate row contents
            for j, element in enumerate(data[i]):
                if not isinstance(element, (str, dict)):
                    errors.append(f"Row {i - start_index}, element {j}: must be string or object")
        
        return errors


def parse_kle_file(file_path: str) -> UniversalLayout:
    """Convenience function to parse a KLE file."""
    parser = KLEParser()
    return parser.parse_file(file_path)


def parse_kle_json(json_str: str) -> UniversalLayout:
    """Convenience function to parse KLE JSON string."""
    parser = KLEParser()
    return parser.parse_json(json_str)


def validate_kle_file(file_path: str) -> List[str]:
    """Validate a KLE file and return any errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        parser = KLEParser()
        return parser.validate_kle_data(data)
    except (IOError, json.JSONDecodeError) as e:
        return [f"Failed to read KLE file: {e}"]
