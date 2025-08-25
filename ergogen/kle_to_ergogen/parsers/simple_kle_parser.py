"""
Simple KLE Parser for standalone operation.

This is a minimal KLE parser that can handle basic KLE JSON files
without external dependencies.
"""

import json
from typing import List, Dict, Any, Optional, Union


class KLEParseError(Exception):
    """Raised when KLE parsing fails."""
    pass


class KeyDefinition:
    """Simple key definition for KLE keys."""
    
    def __init__(self):
        self.x: float = 0.0
        self.y: float = 0.0
        self.width: float = 1.0
        self.height: float = 1.0
        self.rotation_angle: float = 0.0
        self.rotation_x: float = 0.0
        self.rotation_y: float = 0.0
        self.matrix_row: Optional[int] = None
        self.matrix_col: Optional[int] = None
        self.primary_label: str = ""
        self.keycode: str = ""
        self.color: str = "#cccccc"
        
    def __repr__(self):
        return f"KeyDefinition(x={self.x}, y={self.y}, label='{self.primary_label}')"


class UniversalLayout:
    """Simple layout representation."""
    
    def __init__(self, name: Optional[str] = None):
        self.name = name
        self.keys: List[KeyDefinition] = []
        
    def __repr__(self):
        return f"UniversalLayout(name='{self.name}', keys={len(self.keys)})"


class SimpleKLEParser:
    """
    Simple KLE parser that handles basic KLE JSON format.
    
    This parser handles the standard KLE format where:
    - Layout is an array of rows
    - Each row is an array of keys
    - Keys can be strings (labels) or objects (with properties)
    """
    
    def parse_file(self, file_path: str) -> UniversalLayout:
        """Parse KLE file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_json(content)
        except FileNotFoundError:
            raise KLEParseError(f"KLE file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise KLEParseError(f"Invalid JSON in KLE file: {e}")
    
    def parse_json(self, json_content: str) -> UniversalLayout:
        """Parse KLE JSON string."""
        try:
            data = json.loads(json_content)
            return self.parse_layout(data)
        except json.JSONDecodeError as e:
            raise KLEParseError(f"Invalid JSON: {e}")
    
    def parse_layout(self, layout_data: List) -> UniversalLayout:
        """Parse KLE layout data."""
        if not isinstance(layout_data, list):
            raise KLEParseError("KLE layout must be an array")
        
        layout = UniversalLayout("Parsed Layout")
        
        current_y = 0.0
        
        for row_index, row in enumerate(layout_data):
            if not isinstance(row, list):
                raise KLEParseError(f"Row {row_index} must be an array")
            
            current_x = 0.0
            current_key_width = 1.0
            
            # Track current properties that carry over between keys
            current_props = {
                'w': 1.0,  # width
                'h': 1.0,  # height
                'x': 0.0,  # x offset for next key
                'y': 0.0,  # y offset for next key
                'r': 0.0,  # rotation angle
                'rx': 0.0, # rotation center x
                'ry': 0.0, # rotation center y
                'a': 4,    # alignment
                'c': "#cccccc"  # color
            }
            
            for item_index, item in enumerate(row):
                if isinstance(item, dict):
                    # This is a key properties object
                    current_props.update(item)
                    
                    # Handle x/y offsets
                    if 'x' in item:
                        current_x += item['x']
                    if 'y' in item:
                        current_y += item['y']
                        
                elif isinstance(item, str):
                    # This is a key label
                    key = KeyDefinition()
                    
                    # Set position
                    key.x = current_x
                    key.y = current_y
                    
                    # Set dimensions
                    key.width = current_props.get('w', 1.0)
                    key.height = current_props.get('h', 1.0)
                    
                    # Set rotation
                    key.rotation_angle = current_props.get('r', 0.0)
                    key.rotation_x = current_props.get('rx', 0.0)
                    key.rotation_y = current_props.get('ry', 0.0)
                    
                    # Set labels and properties
                    key.primary_label = item
                    key.keycode = item
                    key.color = current_props.get('c', "#cccccc")
                    
                    # Set matrix position (if we can infer it)
                    key.matrix_row = row_index
                    key.matrix_col = len([k for k in layout.keys if k.matrix_row == row_index])
                    
                    layout.keys.append(key)
                    
                    # Advance x position by key width
                    current_x += key.width
                    
                    # Reset width for next key (height persists until explicitly changed)
                    current_props['w'] = 1.0
            
            # Move to next row
            current_y += 1.0
        
        return layout


# Create alias for compatibility
KLEParser = SimpleKLEParser