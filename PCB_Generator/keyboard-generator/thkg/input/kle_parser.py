"""KLE (Keyboard Layout Editor) JSON parser"""

import json
from typing import List, Dict, Any, Tuple
from pathlib import Path
from thkg.config import Switch


class KLEParser:
    """Parse Keyboard Layout Editor (KLE) JSON files"""
    
    # Key unit size in mm (Cherry MX standard)
    KEY_UNIT = 19.05
    
    def parse(self, kle_path: str) -> Tuple[List[Switch], Dict[str, Any]]:
        """Parse KLE JSON file
        
        Args:
            kle_path: Path to KLE JSON file
            
        Returns:
            Tuple of (switches list, metadata dict)
            
        Raises:
            FileNotFoundError: If KLE file doesn't exist
            json.JSONDecodeError: If JSON is malformed
        """
        path = Path(kle_path)
        if not path.exists():
            raise FileNotFoundError(f"KLE file not found: {kle_path}")
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        return self._parse_kle_data(data)
    
    def parse_string(self, kle_json: str) -> Tuple[List[Switch], Dict[str, Any]]:
        """Parse KLE JSON from string
        
        Args:
            kle_json: KLE JSON string
            
        Returns:
            Tuple of (switches list, metadata dict)
        """
        data = json.loads(kle_json)
        return self._parse_kle_data(data)
    
    def _parse_kle_data(self, data: List[Any]) -> Tuple[List[Switch], Dict[str, Any]]:
        """Parse KLE data structure
        
        KLE format:
        - First element may be metadata dict (optional)
        - Remaining elements are rows (arrays of keys)
        - Each key can be a string (label) or dict (properties)
        
        Args:
            data: KLE data structure
            
        Returns:
            Tuple of (switches list, metadata dict)
        """
        # Extract metadata if present
        metadata = {}
        start_index = 0
        if data and isinstance(data[0], dict) and 'name' in data[0]:
            metadata = data[0]
            start_index = 1
        
        # Parse rows
        switches = []
        row_index = 0
        col_index = 0
        
        # Current key properties (carry over between keys)
        current_props = {
            'x': 0.0,
            'y': 0.0,
            'w': 1.0,
            'h': 1.0,
            'r': 0.0,  # rotation
            'rx': 0.0,  # rotation center x
            'ry': 0.0,  # rotation center y
        }
        
        for row_data in data[start_index:]:
            if not isinstance(row_data, list):
                continue
            
            col_index = 0
            x_offset = 0.0
            
            for item in row_data:
                if isinstance(item, dict):
                    # Update current properties
                    if 'x' in item:
                        x_offset += item['x']
                    if 'y' in item:
                        current_props['y'] += item['y']
                    if 'w' in item:
                        current_props['w'] = item['w']
                    if 'h' in item:
                        current_props['h'] = item['h']
                    if 'r' in item:
                        current_props['r'] = item['r']
                    if 'rx' in item:
                        current_props['rx'] = item['rx']
                    if 'ry' in item:
                        current_props['ry'] = item['ry']
                else:
                    # It's a key label (string)
                    label = str(item)
                    
                    # Calculate position
                    x_pos = (current_props['x'] + x_offset) * self.KEY_UNIT
                    y_pos = current_props['y'] * self.KEY_UNIT
                    
                    # Determine stabilizer requirements
                    stabilizer = self._get_stabilizer(current_props['w'])
                    
                    # Create switch
                    switch = Switch(
                        row=row_index,
                        col=col_index,
                        x=x_pos,
                        y=y_pos,
                        width=current_props['w'],
                        height=current_props['h'],
                        rotation=current_props['r'],
                        stabilizer=stabilizer,
                        label=label
                    )
                    switches.append(switch)
                    
                    # Advance position
                    current_props['x'] += current_props['w']
                    col_index += 1
                    x_offset = 0
                    
                    # Reset size to default
                    current_props['w'] = 1.0
                    current_props['h'] = 1.0
            
            # Move to next row
            row_index += 1
            current_props['x'] = 0
            current_props['y'] += 1
        
        return switches, metadata
    
    def _get_stabilizer(self, width: float) -> str:
        """Determine stabilizer requirement based on key width
        
        Args:
            width: Key width in units
            
        Returns:
            Stabilizer type string or None
        """
        if width >= 6.0:
            return "6.25u" if width < 7.0 else "7u"
        elif width >= 2.0:
            return "2u"
        return None
    
    def _get_stabilizer_positions(self, switch: Switch) -> List[Tuple[float, float]]:
        """Get stabilizer positions for a switch
        
        Args:
            switch: Switch object
            
        Returns:
            List of (x, y) tuples for stabilizer positions
        """
        if not switch.stabilizer:
            return []
        
        # Stabilizer spacing from center (mm)
        spacing = {
            "2u": 11.95,      # 2u keys
            "6.25u": 50.0,    # 6.25u spacebar
            "7u": 57.15,      # 7u spacebar
        }
        
        offset = spacing.get(switch.stabilizer, 0)
        if offset == 0:
            return []
        
        # Calculate stabilizer positions (left and right of center)
        center_x = switch.x + (switch.width * self.KEY_UNIT / 2)
        center_y = switch.y + (switch.height * self.KEY_UNIT / 2)
        
        return [
            (center_x - offset, center_y),
            (center_x + offset, center_y)
        ]
