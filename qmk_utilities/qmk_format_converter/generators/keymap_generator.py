"""
Keymap.c Generator

This module implements generation of QMK keymap.c files
from the universal layout data model.
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Union, Optional, Tuple
from data_models.universal_layout import UniversalLayout, KeyDefinition, LayerDefinition
from data_models.keycode_mappings import KEYCODE_MAPPER

# Import the existing ASCII keymap generator
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "ascii_keymap_gen"))
try:
    from modular_keymap_ascii_generator import ModularKeymapParser, LayoutConfig
except ImportError:
    # Fallback if ascii_keymap_gen is not available
    ModularKeymapParser = None
    LayoutConfig = None


class KeymapGenerateError(Exception):
    """Raised when keymap.c generation fails."""
    pass


class KeymapGenerator:
    """
    Generator for QMK keymap.c files.
    
    Converts UniversalLayout objects back to keymap.c format with:
    - Copyright header and includes
    - Custom keycode enums (if needed)
    - keymaps array with proper layout macro
    - Layer definitions with keycodes
    - Optional function templates
    """
    
    def __init__(self):
        self.custom_keycodes = {}
        
    def generate_file(self, layout: UniversalLayout, file_path: str):
        """Generate keymap.c file from layout."""
        keymap_content = self.generate_content(layout)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(keymap_content)
        except IOError as e:
            raise KeymapGenerateError(f"Failed to write keymap file: {e}")
    
    def generate_content(self, layout: UniversalLayout) -> str:
        """Generate keymap.c content from layout."""
        if not layout.keys or not layout.layers:
            raise KeymapGenerateError("Layout has no keys or layers to generate")
        
        # Build the keymap content
        content_parts = []
        
        # Add header
        content_parts.append(self._generate_header(layout))
        
        # Add includes
        content_parts.append(self._generate_includes())
        
        # Add custom keycodes if needed
        custom_enum = self._generate_custom_keycodes(layout)
        if custom_enum:
            content_parts.append(custom_enum)
        
        # Add keymaps array
        content_parts.append(self._generate_keymaps_array(layout))
        
        # Add optional functions
        content_parts.append(self._generate_optional_functions())
        
        return '\n\n'.join(content_parts) + '\n'
    
    def _generate_header(self, layout: UniversalLayout) -> str:
        """Generate copyright header."""
        current_year = datetime.now().year
        author = layout.author or "QMK Format Converter"
        
        header = f"""/* Copyright {current_year} {author}
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */"""
        
        return header
    
    def _generate_includes(self) -> str:
        """Generate include statements."""
        return "#include QMK_KEYBOARD_H"
    
    def _generate_custom_keycodes(self, layout: UniversalLayout) -> Optional[str]:
        """Generate custom keycode enum if needed."""
        # Check if any layers use custom keycodes (non-standard QMK keycodes)
        custom_codes = set()
        
        for layer in layout.layers:
            for keycode in layer.keycodes:
                if keycode and not keycode.startswith('KC_') and keycode not in ['SAFE_RANGE']:
                    custom_codes.add(keycode)
        
        if not custom_codes:
            return None
        
        enum_content = "enum custom_keycodes {\n"
        for i, code in enumerate(sorted(custom_codes)):
            if i == 0:
                enum_content += f"    {code} = SAFE_RANGE,\n"
            else:
                enum_content += f"    {code},\n"
        enum_content += "};"
        
        return enum_content
    
    def _generate_keymaps_array(self, layout: UniversalLayout) -> str:
        """Generate the main keymaps array."""
        layout_macro = layout.layout_name or "LAYOUT"
        
        # Start the keymaps array
        content = f"const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {{\n"
        
        # Generate each layer
        for i, layer in enumerate(layout.layers):
            content += self._generate_layer(layer, layout_macro, layout.keys)
            if i < len(layout.layers) - 1:
                content += ",\n\n"
            else:
                content += "\n"
        
        content += "};"
        return content
    
    def _generate_layer(self, layer: LayerDefinition, layout_macro: str, keys: List[KeyDefinition]) -> str:
        """Generate a single layer definition."""
        # Add layer comment
        layer_comment = self._generate_layer_comment(layer, keys)
        content = layer_comment + "\n" if layer_comment else ""
        
        # Start layer definition
        content += f"    [{layer.index}] = {layout_macro}(\n"
        
        # Generate keycode layout
        keycode_layout = self._generate_keycode_layout(layer.keycodes, keys)
        content += keycode_layout
        
        content += "    )"
        return content
    
    def _generate_layer_comment(self, layer: LayerDefinition, keys: List[KeyDefinition]) -> str:
        """Generate ASCII art comment for a layer using existing ASCII generator."""
        layer_name = layer.name
        if layer.index == 0:
            layer_name = "Base Layer"
        elif layer.index == 1:
            layer_name = "Function Layer"
        
        # Try to use the existing ASCII keymap generator if available
        if ModularKeymapParser and len(keys) == 58:  # Lily58
            try:
                # Create a parser instance to access layout detection
                ascii_parser = ModularKeymapParser()
                
                # Get the Lily58 layout configuration
                lily58_config = ascii_parser.layouts.get('lily58')
                if lily58_config:
                    # Convert our keycodes to the format expected by ASCII generator
                    keycode_labels = []
                    for keycode in layer.keycodes:
                        label = ascii_parser.keycode_to_label(keycode)
                        keycode_labels.append(label)
                    
                    # Generate ASCII using the proper template
                    return lily58_config.template.format(
                        layer_name=layer_name,
                        **{f'k{i}': ascii_parser.format_key_for_ascii(kc) for i, kc in enumerate(keycode_labels)}
                    )
            except Exception:
                # Fall back to built-in generation if ASCII generator fails
                pass
        
        # Fallback to built-in ASCII generation
        if self._is_split_keyboard(keys):
            return self._generate_split_keyboard_comment(layer_name, keys)
        elif len(keys) <= 70:  # Assume 60% or smaller
            return self._generate_standard_keyboard_comment(layer_name)
        else:
            return f"    /* {layer_name} */"
    
    def _is_split_keyboard(self, keys: List[KeyDefinition]) -> bool:
        """Detect if this is a split keyboard layout."""
        if len(keys) == 58:  # Lily58
            return True
        if len(keys) == 42:  # Corne
            return True
        if len(keys) == 56:  # Sofle
            return True
        
        # Check for gap in X coordinates (split keyboards have a gap)
        if not keys:
            return False
        
        x_positions = sorted([key.x for key in keys])
        max_gap = 0
        for i in range(1, len(x_positions)):
            gap = x_positions[i] - x_positions[i-1]
            max_gap = max(max_gap, gap)
        
        # If there's a significant gap (>2 units), likely a split keyboard
        return max_gap > 2.0
    
    def _generate_split_keyboard_comment(self, layer_name: str, keys: List[KeyDefinition]) -> str:
        """Generate ASCII art for split keyboards."""
        if len(keys) == 58:  # Lily58
            return f"""    /* {layer_name}
     * ,-----------------------------------------.                    ,-----------------------------------------.
     * |      |      |      |      |      |      |                    |      |      |      |      |      |      |
     * |------+------+------+------+------+------|                    |------+------+------+------+------+------|
     * |      |      |      |      |      |      |                    |      |      |      |      |      |      |
     * |------+------+------+------+------+------|                    |------+------+------+------+------+------|
     * |      |      |      |      |      |      |-------.    ,-------|      |      |      |      |      |      |
     * |------+------+------+------+------+------|       |    |       |------+------+------+------+------+------|
     * |      |      |      |      |      |      |-------|    |-------|      |      |      |      |      |      |
     * `-----------------------------------------/       /     \\      \\-----------------------------------------'
     *                   |      |      |      | /       /       \\      \\ |      |      |      |
     *                   |      |      |      |/       /         \\      \\|      |      |      |
     *                   `----------------------------'           '------''--------------------'
     */"""
        else:
            return f"""    /* {layer_name} - Split Keyboard Layout
     * Left Half                          Right Half
     * ┌─────┬─────┬─────┬─────┬─────┐    ┌─────┬─────┬─────┬─────┬─────┐
     * │     │     │     │     │     │    │     │     │     │     │     │
     * ├─────┼─────┼─────┼─────┼─────┤    ├─────┼─────┼─────┼─────┼─────┤
     * │     │     │     │     │     │    │     │     │     │     │     │
     * └─────┴─────┴─────┴─────┴─────┘    └─────┴─────┴─────┴─────┴─────┘
     */"""
    
    def _generate_standard_keyboard_comment(self, layer_name: str) -> str:
        """Generate ASCII art for standard keyboards."""
        return f"""    /* {layer_name}
     * ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───────┐
     * │   │   │   │   │   │   │   │   │   │   │   │   │   │       │
     * ├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─────┤
     * │     │   │   │   │   │   │   │   │   │   │   │   │   │     │
     * ├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤
     * │      │   │   │   │   │   │   │   │   │   │   │   │        │
     * ├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────────┤
     * │        │   │   │   │   │   │   │   │   │   │   │          │
     * ├────┬───┴┬──┴─┬─┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬────┬────┤
     * │    │    │    │                        │    │    │    │    │
     * └────┴────┴────┴────────────────────────┴────┴────┴────┴────┘
     */"""
    
    def _generate_keycode_layout(self, keycodes: List[str], keys: List[KeyDefinition]) -> str:
        """Generate formatted keycode layout."""
        if len(keycodes) != len(keys):
            # Pad or truncate to match key count
            if len(keycodes) < len(keys):
                keycodes = keycodes + ['KC_TRNS'] * (len(keys) - len(keycodes))
            else:
                keycodes = keycodes[:len(keys)]
        
        # For split keyboards like Lily58, preserve the original key order from KLE file
        # since it matches the expected QMK LAYOUT macro parameter order
        if len(keys) == 58:  # Lily58 specific formatting
            return self._format_lily58_keycodes(keycodes)
        
        # For other keyboards, use row-based organization
        rows = self._organize_keys_into_rows(keys, keycodes)
        
        content = ""
        for i, row in enumerate(rows):
            content += "        "  # Indent
            content += ", ".join(f"{kc:<8}" for kc in row)
            if i < len(rows) - 1:
                content += ",\n"
            else:
                content += "\n"
        
        return content
    
    def _format_lily58_keycodes(self, keycodes: List[str]) -> str:
        """Format keycodes specifically for Lily58 layout."""
        # Lily58 has 58 keys, format them in logical groups
        # Based on the QMK Lily58 keymap structure
        content = ""
        
        # Format in groups of keys for readability
        keys_per_line = [
            # Top row (12 keys)
            12,
            # Second row (12 keys) 
            12,
            # Third row (12 keys)
            12,
            # Fourth row (12 keys)
            12,
            # Thumb cluster (10 keys)
            10
        ]
        
        idx = 0
        for i, line_count in enumerate(keys_per_line):
            content += "        "  # Indent
            line_keys = []
            for j in range(line_count):
                if idx < len(keycodes):
                    line_keys.append(f"{keycodes[idx]:<8}")
                    idx += 1
                else:
                    line_keys.append(f"{'KC_TRNS':<8}")
            
            content += ", ".join(line_keys)
            if i < len(keys_per_line) - 1:
                content += ",\n"
            else:
                content += "\n"
        
        return content
    
    def _organize_keys_into_rows(self, keys: List[KeyDefinition], keycodes: List[str]) -> List[List[str]]:
        """Organize keys and keycodes into rows for formatting."""
        # Group keys by Y coordinate (row)
        rows_dict = {}
        for i, key in enumerate(keys):
            row_y = key.y
            if row_y not in rows_dict:
                rows_dict[row_y] = []
            keycode = keycodes[i] if i < len(keycodes) else 'KC_TRNS'
            rows_dict[row_y].append((key.x, keycode))
        
        # Sort rows and keys within rows
        rows = []
        for y in sorted(rows_dict.keys()):
            row_data = sorted(rows_dict[y], key=lambda item: item[0])  # Sort by X
            row_keycodes = [item[1] for item in row_data]
            rows.append(row_keycodes)
        
        return rows
    
    def _generate_optional_functions(self) -> str:
        """Generate optional function templates."""
        functions = """bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    switch (keycode) {
        // Add custom keycode handling here
    }
    return true;
}

void matrix_init_user(void) {
    // Initialization code here
}

void matrix_scan_user(void) {
    // Runs constantly in the background
}

void led_set_user(uint8_t usb_led) {
    // LED indicator code here
}"""
        
        return functions
    
    def validate_layout(self, layout: UniversalLayout) -> List[str]:
        """Validate layout for keymap.c generation."""
        errors = []
        
        if not layout.keys:
            errors.append("Layout has no keys")
        
        if not layout.layers:
            errors.append("Layout has no layers")
        
        # Check layer keycode counts
        key_count = len(layout.keys)
        for i, layer in enumerate(layout.layers):
            if len(layer.keycodes) != key_count:
                errors.append(f"Layer {i} has {len(layer.keycodes)} keycodes but layout has {key_count} keys")
        
        # Check for valid layout macro name
        if layout.layout_name and not re.match(r'^[A-Z_][A-Z0-9_]*$', layout.layout_name):
            errors.append(f"Invalid layout macro name: {layout.layout_name}")
        
        return errors


def generate_keymap_file(layout: UniversalLayout, file_path: str):
    """Convenience function to generate keymap.c file."""
    generator = KeymapGenerator()
    generator.generate_file(layout, file_path)


def generate_keymap_content(layout: UniversalLayout) -> str:
    """Convenience function to generate keymap.c content."""
    generator = KeymapGenerator()
    return generator.generate_content(layout)


def validate_layout_for_keymap(layout: UniversalLayout) -> List[str]:
    """Validate layout for keymap.c generation."""
    generator = KeymapGenerator()
    return generator.validate_layout(layout)
