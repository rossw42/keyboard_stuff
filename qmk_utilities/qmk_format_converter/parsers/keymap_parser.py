"""
Keymap.c Parser

This module implements parsing of QMK keymap.c files to the universal layout data model.
"""

import re
from typing import Dict, List, Any, Union, Optional, Tuple, Set

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


class KeymapParseError(Exception):
    """Raised when keymap.c parsing fails."""
    pass


class KeymapParser:
    """
    Parser for QMK keymap.c files.
    
    Keymap.c format contains:
    - Layout macro definitions (e.g., LAYOUT_60_ansi)
    - Layer definitions with keycodes
    - Custom keycode enums
    - ASCII art comments for visual layout
    """
    
    def __init__(self):
        self.custom_keycodes: Dict[str, str] = {}
        self.layout_macro = ""
        
    def parse_file(self, file_path: str) -> UniversalLayout:
        """Parse a keymap.c file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_content(content)
        except IOError as e:
            raise KeymapParseError(f"Failed to read keymap file: {e}")
    
    def parse_content(self, content: str) -> UniversalLayout:
        """Parse keymap.c content."""
        # Clean content - remove comments but preserve ASCII art
        cleaned_content = self._clean_content(content)
        
        # Extract custom keycodes
        self.custom_keycodes = self._extract_custom_keycodes(content)
        
        # Extract layout macro name
        self.layout_macro = self._extract_layout_macro(cleaned_content)
        
        # Extract keymap layers
        layers_data = self._extract_keymap_layers(cleaned_content)
        
        if not layers_data:
            raise KeymapParseError("No keymap layers found")
        
        # Create layout object
        layout = UniversalLayout()
        layout.name = f"Keymap ({self.layout_macro})"
        layout.layout_name = self.layout_macro or "LAYOUT"
        
        # Determine matrix dimensions from first layer
        first_layer = layers_data[0]
        key_count = len(first_layer['keycodes'])
        
        # Estimate matrix dimensions (assume rectangular grid)
        layout.matrix_cols = self._estimate_cols_from_layout_macro(self.layout_macro, key_count)
        layout.matrix_rows = (key_count + layout.matrix_cols - 1) // layout.matrix_cols
        
        # Create key definitions based on grid layout
        self._create_keys_from_keycodes(layout, first_layer['keycodes'])
        
        # Create layer definitions
        for layer_data in layers_data:
            layer = LayerDefinition(
                name=layer_data['name'],
                index=layer_data['index'],
                keycodes=layer_data['keycodes'].copy(),
                is_default=(layer_data['index'] == 0)
            )
            layout.add_layer(layer)
        
        # Extract metadata from comments
        self._extract_metadata_from_comments(layout, content)
        
        return layout
    
    def _clean_content(self, content: str) -> str:
        """Clean C code content, removing single-line comments but preserving multi-line comments."""
        # Remove single-line comments (// ...)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return content
    
    def _extract_custom_keycodes(self, content: str) -> Dict[str, str]:
        """Extract custom keycode definitions from enum."""
        custom_keycodes = {}
        
        # Find enum blocks
        enum_pattern = r'enum\s+\w*\s*\{([^}]+)\}'
        matches = re.findall(enum_pattern, content, re.DOTALL)
        
        for enum_content in matches:
            # Parse enum entries
            entries = re.findall(r'(\w+)(?:\s*=\s*([^,\s]+))?', enum_content)
            for name, value in entries:
                if name and name != 'SAFE_RANGE':
                    custom_keycodes[name] = value or name
        
        return custom_keycodes
    
    def _extract_layer_enum_mapping(self, content: str) -> Dict[str, int]:
        """Extract layer enum to index mapping from enum definitions."""
        layer_enum_map = {}
        
        # Find enum blocks that contain layer definitions
        enum_pattern = r'enum\s+\w*\s*\{([^}]+)\}'
        matches = re.findall(enum_pattern, content, re.DOTALL)
        
        for enum_content in matches:
            # Look for layer-like enum entries (starting with _ and containing LAYER or common layer names)
            lines = enum_content.split(',')
            current_index = 0
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Parse enum entry
                if '=' in line:
                    # Explicit value assignment
                    name_part, value_part = line.split('=', 1)
                    name = name_part.strip()
                    try:
                        value = int(value_part.strip())
                        current_index = value
                    except ValueError:
                        # Value might be a reference to another enum
                        current_index += 1
                else:
                    # Implicit value
                    name = line.strip()
                
                # Check if this looks like a layer name
                if name.startswith('_') and (
                    'QWERTY' in name.upper() or 
                    'LOWER' in name.upper() or 
                    'RAISE' in name.upper() or 
                    'ADJUST' in name.upper() or
                    'BASE' in name.upper() or
                    'FN' in name.upper() or
                    'LAYER' in name.upper()
                ):
                    layer_enum_map[name] = current_index
                    current_index += 1
        
        return layer_enum_map
    
    def _extract_layout_macro(self, content: str) -> str:
        """Extract the layout macro name (e.g., LAYOUT_60_ansi)."""
        # Look for keymaps array definition
        keymap_pattern = r'keymaps\[\]\[MATRIX_ROWS\]\[MATRIX_COLS\]\s*=\s*\{.*?\[0\]\s*=\s*(\w+)\s*\('
        match = re.search(keymap_pattern, content, re.DOTALL)
        
        if match:
            return match.group(1)
        
        # Fallback: look for any LAYOUT macro
        layout_pattern = r'\[0\]\s*=\s*(LAYOUT\w*)\s*\('
        match = re.search(layout_pattern, content)
        if match:
            return match.group(1)
        
        return "LAYOUT"
    
    def _extract_keymap_layers(self, content: str) -> List[Dict[str, Any]]:
        """Extract all keymap layers from the keymaps array."""
        layers = []
        
        # Find the keymaps array
        keymaps_pattern = r'keymaps\[\]\[MATRIX_ROWS\]\[MATRIX_COLS\]\s*=\s*\{(.*?)\};'
        match = re.search(keymaps_pattern, content, re.DOTALL)
        
        if not match:
            raise KeymapParseError("Could not find keymaps array")
        
        keymaps_content = match.group(1)
        
        # Extract enum definitions for layer mapping
        layer_enum_map = self._extract_layer_enum_mapping(content)
        
        # Extract individual layers - support both numeric [0] and enum [_QWERTY] patterns
        # Use a more comprehensive regex that handles multi-line content and balances parentheses
        layer_pattern = r'\[([_A-Z0-9]+)\]\s*=\s*' + re.escape(self.layout_macro) + r'\s*\('
        
        # Find the starting positions of each layer
        layer_starts = [(m.group(1), m.start()) for m in re.finditer(layer_pattern, keymaps_content)]
        
        layer_matches = []
        if layer_starts:
            # For each layer start, find its corresponding end by balancing parentheses
            for i, (layer_name, start_pos) in enumerate(layer_starts):
                # Find where the opening parenthesis is
                open_paren_pos = keymaps_content.find('(', start_pos)
                if open_paren_pos == -1:
                    continue
                
                # Find the matching closing parenthesis
                paren_depth = 1
                end_pos = open_paren_pos + 1
                
                while paren_depth > 0 and end_pos < len(keymaps_content):
                    if keymaps_content[end_pos] == '(':
                        paren_depth += 1
                    elif keymaps_content[end_pos] == ')':
                        paren_depth -= 1
                    end_pos += 1
                
                if paren_depth == 0:  # Found the matching closing parenthesis
                    # Extract the content inside the parentheses
                    layer_content = keymaps_content[open_paren_pos+1:end_pos-1].strip()
                    layer_matches.append((layer_name, layer_content))
        
        for layer_identifier, layer_content in layer_matches:
            # Determine layer index and name
            if layer_identifier.isdigit():
                # Numeric layer index
                layer_index = int(layer_identifier)
                layer_name = f"Layer_{layer_index}"
                if layer_index == 0:
                    layer_name = "Base"
                elif layer_index == 1:
                    layer_name = "Function"
            else:
                # Enum-based layer name
                layer_index = layer_enum_map.get(layer_identifier, len(layers))
                layer_name = layer_identifier.lstrip('_').title()  # Convert _QWERTY to Qwerty
            
            keycodes = self._parse_layer_keycodes(layer_content)
            
            # Expand keycodes to full matrix if needed
            keycodes = self._expand_keycodes_to_matrix(keycodes)
            
            layers.append({
                'index': layer_index,
                'name': layer_name,
                'keycodes': keycodes
            })
        
        # Sort layers by index to ensure proper order
        layers.sort(key=lambda x: x['index'])
        
        return layers
    
    def _parse_layer_keycodes(self, layer_content: str) -> List[str]:
        """Parse keycodes from a layer definition."""
        # Remove comments and whitespace
        cleaned = re.sub(r'/\*.*?\*/', '', layer_content, flags=re.DOTALL)
        cleaned = re.sub(r'//.*$', '', cleaned, flags=re.MULTILINE)
        
        # Split on commas, handling multiline content
        parts = re.split(r',\s*', cleaned)
        
        keycodes = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # First try to match complete function calls with parameters
            # Function calls like MO(_LOWER), LT(1, KC_TAB), etc.
            func_match = re.search(r'([A-Z_][A-Z0-9_]*\([^()]*(?:\([^()]*\)[^()]*)*\))', part)
            if func_match:
                keycodes.append(func_match.group(1))
                continue
            
            # If no function call, try to match simple keycodes
            keycode_match = re.search(r'([A-Z_][A-Z0-9_]*)', part)
            if keycode_match:
                keycode = keycode_match.group(1)
                # Skip layout macro name if it appears
                if keycode != self.layout_macro and keycode not in ['MATRIX_ROWS', 'MATRIX_COLS']:
                    keycodes.append(keycode)
        
        return keycodes
    
    def _expand_keycodes_to_matrix(self, keycodes: List[str]) -> List[str]:
        """Expand keycodes to full matrix size by adding KC_NO for unused positions."""
        # For most keyboards, the keymap.c format excludes unused matrix positions
        # but VIA format includes all positions with KC_NO placeholders
        
        # Determine expected matrix size based on keycode count and layout
        if len(keycodes) == 58:  # Lily58 case
            # Lily58 has 58 defined keys but 60 matrix positions (5x12)
            # Need to add 2 KC_NO placeholders in the right positions
            expanded = keycodes.copy()
            
            # Based on VIA format analysis, the unused positions appear to be
            # at indices 24 and 54 (encoder positions that aren't used)
            expanded.insert(24, "KC_NO")  # After left encoder position
            expanded.insert(55, "KC_NO")  # After right encoder position
            
            return expanded
        
        elif len(keycodes) in [61, 62, 87, 104]:  # Common full matrix sizes
            # Already at full matrix size
            return keycodes
        
        else:
            # For other sizes, estimate and pad to next multiple of common matrix width
            target_cols = self._estimate_cols_from_layout_macro(self.layout_macro, len(keycodes))
            target_size = ((len(keycodes) + target_cols - 1) // target_cols) * target_cols
            
            # Pad with KC_NO to reach target size
            expanded = keycodes.copy()
            while len(expanded) < target_size:
                expanded.append("KC_NO")
            
            return expanded
    
    def _estimate_cols_from_layout_macro(self, layout_macro: str, key_count: int) -> int:
        """Estimate column count based on layout macro name and key count."""
        # Common layout patterns
        layout_patterns = {
            'LAYOUT_60_ansi': 14,
            'LAYOUT_tkl': 17,
            'LAYOUT_fullsize': 19,
            'LAYOUT_planck': 12,
            'LAYOUT_preonic': 12,
            'LAYOUT_ortho_4x12': 12,
            'LAYOUT_ortho_5x12': 12,
            'LAYOUT_split_3x6_3': 6,
            'LAYOUT_split_3x5_3': 5,
        }
        
        # Check for exact matches
        if layout_macro in layout_patterns:
            return layout_patterns[layout_macro]
        
        # Check for partial matches
        for pattern, cols in layout_patterns.items():
            if pattern.replace('LAYOUT_', '') in layout_macro.lower():
                return cols
        
        # Estimate based on key count
        if key_count <= 48:  # Planck-like
            return 12
        elif key_count <= 70:  # 60% or similar
            return 14
        elif key_count <= 90:  # TKL
            return 17
        else:  # Full size
            return 19
    
    def _create_keys_from_keycodes(self, layout: UniversalLayout, keycodes: List[str]):
        """Create key definitions based on keycodes in a grid layout."""
        for i, keycode in enumerate(keycodes):
            row = i // layout.matrix_cols
            col = i % layout.matrix_cols
            
            # Calculate physical position
            x = float(col)
            y = float(row)
            
            # Get keycode mapping for label
            mapping = KEYCODE_MAPPER.get_mapping(keycode)
            primary_label = mapping.kle_label if mapping and mapping.kle_label else keycode
            
            key = KeyDefinition(
                # Physical properties
                x=x,
                y=y,
                width=1.0,
                height=1.0,
                
                # Matrix properties
                matrix_row=row,
                matrix_col=col,
                
                # Labels and keycode
                primary_label=primary_label,
                secondary_labels=[],
                keycode=keycode
            )
            
            layout.add_key(key)
    
    def _extract_metadata_from_comments(self, layout: UniversalLayout, content: str):
        """Extract metadata from file comments."""
        # Extract copyright information
        copyright_match = re.search(r'/\*\s*Copyright\s+(\d+)\s+([^*]+)', content)
        if copyright_match:
            year = copyright_match.group(1)
            author = copyright_match.group(2).strip()
            layout.author = author
            layout.description = f"QMK Keymap (Copyright {year})"
        
        # Look for keyboard name in includes
        keyboard_match = re.search(r'#include\s+"([^"]+)/keymap\.c"', content)
        if not keyboard_match:
            keyboard_match = re.search(r'#include\s+QMK_KEYBOARD_H', content)
        
        if keyboard_match:
            layout.name = f"QMK Keymap"
        
        # Extract ASCII art layouts if present
        ascii_art_blocks = re.findall(r'/\*[^*]*\*(?:[^/][^*]*\*+)*/', content, re.DOTALL)
        for block in ascii_art_blocks:
            if '┌' in block or '┬' in block or '│' in block:
                # This looks like ASCII art layout - store in description
                if not layout.description:
                    layout.description = "QMK Keymap with ASCII layout"
                break
    
    def validate_keymap_content(self, content: str) -> List[str]:
        """Validate keymap.c content and return any errors."""
        errors = []
        
        # Check for required elements
        if 'keymaps' not in content:
            errors.append("No keymaps array found")
        
        if 'MATRIX_ROWS' not in content or 'MATRIX_COLS' not in content:
            errors.append("Missing MATRIX_ROWS or MATRIX_COLS references")
        
        # Check for layout macro
        if not re.search(r'LAYOUT\w*\s*\(', content):
            errors.append("No layout macro found")
        
        # Check for valid C syntax (basic)
        if content.count('{') != content.count('}'):
            errors.append("Mismatched braces")
        
        if content.count('(') != content.count(')'):
            errors.append("Mismatched parentheses")
        
        return errors


def parse_keymap_file(file_path: str) -> UniversalLayout:
    """Convenience function to parse a keymap.c file."""
    parser = KeymapParser()
    return parser.parse_file(file_path)


def parse_keymap_content(content: str) -> UniversalLayout:
    """Convenience function to parse keymap.c content."""
    parser = KeymapParser()
    return parser.parse_content(content)


def validate_keymap_file(file_path: str) -> List[str]:
    """Validate a keymap.c file and return any errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        parser = KeymapParser()
        return parser.validate_keymap_content(content)
    except IOError as e:
        return [f"Failed to read keymap file: {e}"]
