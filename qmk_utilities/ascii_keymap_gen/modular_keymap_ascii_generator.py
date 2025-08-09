#!/usr/bin/env python3
"""
Modular QMK Keymap ASCII Generator

This script parses QMK keymap.c files and generates ASCII representations
for various keyboard layouts using external configuration files and templates.
New keyboards can be easily added by creating layout JSON files and template files.
"""

import re
import sys
import json
import glob
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class LayoutConfig:
    """Configuration for a specific keyboard layout."""
    def __init__(self, config_data: dict, template_content: str):
        self.name = config_data['name']
        self.description = config_data.get('description', '')
        self.key_count = config_data['key_count']  
        self.layout_functions = config_data['layout_functions']
        self.template = template_content
        self.author = config_data.get('author', '')
        self.tags = config_data.get('tags', [])

class ModularKeymapParser:
    def __init__(self, layouts_dir: str = "layouts", templates_dir: str = "templates"):
        self.layouts_dir = Path(layouts_dir)
        self.templates_dir = Path(templates_dir)
        
        # QMK keycode to readable label mapping
        self.keycode_map = {
            # Basic keys
            'KC_ESC': 'ESC', 'KC_TAB': 'Tab', 'KC_CAPS': 'Caps',
            'KC_LSFT': 'LShift', 'KC_RSFT': 'RShift',
            'KC_LCTL': 'LCTRL', 'KC_RCTL': 'RCTRL',
            'KC_LALT': 'LAlt', 'KC_RALT': 'RAlt',
            'KC_LGUI': 'LGUI', 'KC_RGUI': 'RGUI',
            'KC_SPC': 'Space', 'KC_ENT': 'Enter', 'KC_BSPC': 'BackSP',
            'KC_DEL': 'Del', 'KC_INS': 'Ins', 'KC_HOME': 'Home',
            'KC_END': 'End', 'KC_PGUP': 'PgUp', 'KC_PGDN': 'PgDn',
            
            # Numbers
            'KC_1': '1', 'KC_2': '2', 'KC_3': '3', 'KC_4': '4', 'KC_5': '5',
            'KC_6': '6', 'KC_7': '7', 'KC_8': '8', 'KC_9': '9', 'KC_0': '0',
            
            # Letters
            'KC_A': 'A', 'KC_B': 'B', 'KC_C': 'C', 'KC_D': 'D', 'KC_E': 'E',
            'KC_F': 'F', 'KC_G': 'G', 'KC_H': 'H', 'KC_I': 'I', 'KC_J': 'J',
            'KC_K': 'K', 'KC_L': 'L', 'KC_M': 'M', 'KC_N': 'N', 'KC_O': 'O',
            'KC_P': 'P', 'KC_Q': 'Q', 'KC_R': 'R', 'KC_S': 'S', 'KC_T': 'T',
            'KC_U': 'U', 'KC_V': 'V', 'KC_W': 'W', 'KC_X': 'X', 'KC_Y': 'Y',
            'KC_Z': 'Z',
            
            # Function keys
            'KC_F1': 'F1', 'KC_F2': 'F2', 'KC_F3': 'F3', 'KC_F4': 'F4',
            'KC_F5': 'F5', 'KC_F6': 'F6', 'KC_F7': 'F7', 'KC_F8': 'F8',
            'KC_F9': 'F9', 'KC_F10': 'F10', 'KC_F11': 'F11', 'KC_F12': 'F12',
            
            # Symbols
            'KC_GRV': '`', 'KC_MINS': '-', 'KC_EQL': '=', 'KC_LBRC': '[',
            'KC_RBRC': ']', 'KC_BSLS': '\\', 'KC_SCLN': ';', 'KC_QUOT': "'",
            'KC_COMM': ',', 'KC_DOT': '.', 'KC_SLSH': '/',
            
            # Shifted symbols
            'KC_EXLM': '!', 'KC_AT': '@', 'KC_HASH': '#', 'KC_DLR': '$',
            'KC_PERC': '%', 'KC_CIRC': '^', 'KC_AMPR': '&', 'KC_ASTR': '*',
            'KC_LPRN': '(', 'KC_RPRN': ')', 'KC_UNDS': '_', 'KC_PLUS': '+',
            'KC_LCBR': '{', 'KC_RCBR': '}', 'KC_PIPE': '|', 'KC_TILD': '~',
            
            # Arrows
            'KC_LEFT': 'Left', 'KC_DOWN': 'Down', 'KC_UP': 'Up', 'KC_RGHT': 'Right',
            
            # Special QMK codes
            '_______': '', 'XXXXXXX': '', 'QK_BOOT': 'Reset',
            'RGB_TOG': 'RGB ON', 'RM_TOGG': 'RGB ON',
            'RGB_HUI': 'HUE+', 'RM_HUEU': 'HUE+', 'RGB_HUD': 'HUE-', 'RM_HUED': 'HUE-',
            'RGB_SAI': 'SAT+', 'RM_SATU': 'SAT+', 'RGB_SAD': 'SAT-', 'RM_SATD': 'SAT-',
            'RGB_VAI': 'VAL+', 'RM_VALU': 'VAL+', 'RGB_VAD': 'VAL-', 'RM_VALD': 'VAL-',
            'RGB_MOD': 'MODE', 'RM_NEXT': 'MODE',
        }
        
        # Load layout configurations
        self.layouts = self._load_layouts()
    
    def _load_layouts(self) -> Dict[str, LayoutConfig]:
        """Load keyboard layout configurations from external files."""
        layouts = {}
        
        if not self.layouts_dir.exists():
            print(f"Warning: Layouts directory '{self.layouts_dir}' not found.")
            return layouts
        
        if not self.templates_dir.exists():
            print(f"Warning: Templates directory '{self.templates_dir}' not found.")
            return layouts
        
        # Load all JSON configuration files
        for config_file in self.layouts_dir.glob('*.json'):
            try:
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Validate required fields
                required_fields = ['name', 'key_count', 'layout_functions', 'template_file']
                for field in required_fields:
                    if field not in config_data:
                        print(f"Error: Missing required field '{field}' in {config_file}")
                        continue
                
                # Load corresponding template file
                template_file = self.templates_dir / config_data['template_file']
                if not template_file.exists():
                    print(f"Error: Template file '{template_file}' not found for layout '{config_data['name']}'")
                    continue
                
                with open(template_file, 'r') as f:
                    template_content = f.read()
                
                # Create layout configuration
                layout_config = LayoutConfig(config_data, template_content)
                layouts[layout_config.name] = layout_config
                
                print(f"Loaded layout: {layout_config.name} ({layout_config.key_count} keys)")
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON file {config_file}: {e}")
            except Exception as e:
                print(f"Error loading layout from {config_file}: {e}")
        
        return layouts
    
    def list_available_layouts(self):
        """List all available keyboard layouts."""
        if not self.layouts:
            print("No layouts available. Make sure layouts/ and templates/ directories exist with configuration files.")
            return
        
        print("Available keyboard layouts:")
        print("=" * 50)
        for name, config in self.layouts.items():
            print(f"{name:15} - {config.description}")
            print(f"{'':15}   Keys: {config.key_count}, Functions: {config.layout_functions}")
            if config.tags:
                print(f"{'':15}   Tags: {', '.join(config.tags)}")
            print()
    
    def detect_layout(self, content: str, key_count: int) -> Optional[LayoutConfig]:
        """Detect keyboard layout based on content analysis and key count."""
        
        # Check for specific layout function names first (most reliable)
        for layout_config in self.layouts.values():
            for layout_function in layout_config.layout_functions:
                if layout_function in content and key_count == layout_config.key_count:
                    return layout_config
        
        # Fallback: match by key count only
        for layout_config in self.layouts.values():
            if key_count == layout_config.key_count:
                return layout_config
        
        return None
    
    def parse_layer_name(self, line: str) -> Optional[str]:
        """Extract layer name from a LAYOUT definition line."""
        match = re.search(r'\[_?(\w+)\]\s*=\s*LAYOUT', line)
        return match.group(1) if match else None
    
    def parse_layout_keys(self, content: str, start_pos: int) -> List[str]:
        """Parse the keys from a LAYOUT() function call."""
        # Find the opening parenthesis
        paren_start = content.find('(', start_pos)
        if paren_start == -1:
            return []
        
        # Find the matching closing parenthesis
        paren_count = 1
        pos = paren_start + 1
        while pos < len(content) and paren_count > 0:
            if content[pos] == '(':
                paren_count += 1
            elif content[pos] == ')':
                paren_count -= 1
            pos += 1
        
        if paren_count != 0:
            return []
        
        # Extract the content between parentheses
        layout_content = content[paren_start + 1:pos - 1]
        
        # Split by commas and clean up
        keys = []
        for key in layout_content.split(','):
            key = key.strip()
            if key and self._is_valid_keycode(key):
                keys.append(key)
        
        return keys
    
    def _is_valid_keycode(self, key: str) -> bool:
        """Check if a string is a valid QMK keycode, not a comment or decoration."""
        key = key.strip()
        
        # Skip empty strings
        if not key:
            return False
        
        # Skip comment lines (starting with //)
        if key.startswith('//'):
            return False
        
        # Skip lines that look like ASCII art (contain multiple dashes, dots, or pipes)
        if key.count('-') > 3 or key.count('.') > 3 or key.count('|') > 2:
            return False
        
        # Skip lines with newlines that contain ASCII art patterns
        if '\n' in key:
            lines = key.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('//') or line.count('-') > 3 or line.count('|') > 2:
                    return False
        
        # Valid keycodes typically:
        # - Start with KC_, MO(, LT(, or other QMK prefixes
        # - Are simple identifiers like XXXXXXX, _______
        # - Are custom function names
        valid_prefixes = ['KC_', 'MO(', 'LT(', 'MT(', 'LCTL(', 'LSFT(', 'LALT(', 'LGUI(',
                         'RCTL(', 'RSFT(', 'RALT(', 'RGUI(', 'QK_', 'RGB_', 'RM_', 'UG_',
                         'AU_', 'MU_', 'MI_', 'DB_', 'AG_', 'S(', 'LSFT_T(', 'RSFT_T(',
                         'LCTL_T(', 'RCTL_T(', 'LALT_T(', 'RALT_T(', 'LGUI_T(', 'RGUI_T(']
        
        # Check for valid prefixes
        for prefix in valid_prefixes:
            if key.startswith(prefix):
                return True
        
        # Check for common placeholder keycodes
        if key in ['XXXXXXX', '_______', 'TRNS', 'NO']:
            return True
        
        # Check for custom defines (alphanumeric identifiers)
        if key.replace('_', '').replace('()', '').isalnum():
            return True
        
        return False
    
    def keycode_to_label(self, keycode: str) -> str:
        """Convert a QMK keycode to a readable label."""
        # Handle layer keys like MO(_LOWER)
        if keycode.startswith('MO(_'):
            layer_name = keycode[4:-1]  # Extract layer name
            return layer_name
        
        # Handle other function-like keycodes
        if '(' in keycode:
            return keycode.split('(')[0]
        
        # Use the mapping or return the keycode as-is
        return self.keycode_map.get(keycode, keycode)
    
    def format_key_for_ascii(self, keycode: str, width: int = 6) -> str:
        """Format a key label to fit in the ASCII representation."""
        label = self.keycode_to_label(keycode)
        
        # Handle empty keys
        if not label or label in ['_______', 'XXXXXXX']:
            return ' ' * width
        
        # Truncate or pad to fit width
        if len(label) > width:
            return label[:width]
        else:
            return label.center(width)
    
    def generate_ascii(self, layout_config: LayoutConfig, layer_name: str, keys: List[str]) -> str:
        """Generate ASCII representation for the specified layout."""
        if len(keys) != layout_config.key_count:
            raise ValueError(f"Expected {layout_config.key_count} keys for {layout_config.name}, got {len(keys)}")
        
        # Create a dictionary mapping key positions to formatted labels
        key_dict = {}
        for i, keycode in enumerate(keys):
            key_dict[f'k{i}'] = self.format_key_for_ascii(keycode)
        
        # Format the template with the keys
        return layout_config.template.format(layer_name=layer_name, **key_dict)
    
    def parse_keymap_file(self, filename: str, forced_layout: Optional[str] = None) -> Dict[str, Tuple[List[str], LayoutConfig]]:
        """Parse a keymap.c file and extract all layouts with their configurations."""
        with open(filename, 'r') as f:
            content = f.read()
        
        layouts = {}
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for layer definitions
            if 'LAYOUT' in line and ('[_' in line or '[' in line):
                layer_name = self.parse_layer_name(line)
                if layer_name:
                    # Find the start of this layout in the full content
                    line_start_pos = content.find(line)
                    keys = self.parse_layout_keys(content, line_start_pos)
                    if keys:
                        # Use forced layout if specified and valid
                        if forced_layout and forced_layout in self.layouts:
                            layout_config = self.layouts[forced_layout]
                            if len(keys) == layout_config.key_count:
                                layouts[layer_name] = (keys, layout_config)
                            else:
                                print(f"Warning: Forced layout '{forced_layout}' expects {layout_config.key_count} keys, but found {len(keys)} keys")
                                # Fall back to auto-detection
                                layout_config = self.detect_layout(content, len(keys))
                                if layout_config:
                                    layouts[layer_name] = (keys, layout_config)
                        else:
                            # Auto-detect layout configuration
                            layout_config = self.detect_layout(content, len(keys))
                            if layout_config:
                                layouts[layer_name] = (keys, layout_config)
                            else:
                                print(f"Warning: Could not detect layout for layer {layer_name} with {len(keys)} keys")
            i += 1
        
        return layouts
    
    def update_keymap_file(self, filename: str, backup: bool = True) -> None:
        """Update the keymap file with generated ASCII representations."""
        if backup:
            with open(filename, 'r') as f:
                content = f.read()
            with open(f"{filename}.backup", 'w') as f:
                f.write(content)
        
        layouts = self.parse_keymap_file(filename)
        
        with open(filename, 'r') as f:
            content = f.read()
        
        # Update each layer's comment
        for layer_name, (keys, layout_config) in layouts.items():
            try:
                new_ascii = self.generate_ascii(layout_config, layer_name, keys)
                
                # Find existing comment block for this layer
                pattern = rf'/\*\s*{re.escape(layer_name)}.*?\*/'
                match = re.search(pattern, content, re.DOTALL)
                
                if match:
                    content = content.replace(match.group(0), new_ascii)
                else:
                    # If no existing comment, insert before the layout definition
                    layout_pattern = rf'\[_?{re.escape(layer_name)}\]\s*=\s*LAYOUT'
                    layout_match = re.search(layout_pattern, content)
                    if layout_match:
                        insert_pos = layout_match.start()
                        content = content[:insert_pos] + new_ascii + '\n\n' + content[insert_pos:]
                        
            except ValueError as e:
                print(f"Error processing layer {layer_name}: {e}")
        
        with open(filename, 'w') as f:
            f.write(content)

def main():
    if len(sys.argv) < 2:
        print("Modular QMK Keymap ASCII Generator")
        print("Usage: python modular_keymap_ascii_generator.py <keymap.c> [--update] [--list] [--layout <name>]")
        print("  <keymap.c>: Path to QMK keymap file to process")
        print("  --update: Update the keymap.c file with generated ASCII")
        print("  --list: List all available keyboard layouts")
        print("  --layout <name>: Force use of specific layout (e.g., --layout lily58)")
        print()
        print("To add a new keyboard layout:")
        print("  1. Create a JSON config file in layouts/ directory")
        print("  2. Create a template file in templates/ directory")
        print("  3. Run the script with your new keyboard's keymap")
        sys.exit(1)
    
    parser = ModularKeymapParser()
    
    # Handle --list command
    if '--list' in sys.argv:
        parser.list_available_layouts()
        return
    
    filename = sys.argv[1]
    update_file = '--update' in sys.argv
    
    # Handle --layout command
    forced_layout = None
    if '--layout' in sys.argv:
        try:
            layout_idx = sys.argv.index('--layout')
            if layout_idx + 1 < len(sys.argv):
                forced_layout = sys.argv[layout_idx + 1]
            else:
                print("Error: --layout requires a layout name")
                sys.exit(1)
        except ValueError:
            pass
    
    try:
        # Validate forced layout if specified
        if forced_layout and forced_layout not in parser.layouts:
            print(f"Error: Layout '{forced_layout}' not found. Available layouts:")
            for name in parser.layouts.keys():
                print(f"  - {name}")
            sys.exit(1)
        
        layouts = parser.parse_keymap_file(filename, forced_layout)
        
        if not layouts:
            print("No supported layouts found in the keymap file.")
            print("Run with --list to see available layouts.")
            print("Consider adding support for your keyboard layout.")
            sys.exit(1)
        
        if update_file:
            parser.update_keymap_file(filename)
            print(f"Updated {filename} with generated ASCII representations")
        else:
            # Just print the generated ASCII
            for layer_name, (keys, layout_config) in layouts.items():
                try:
                    ascii_repr = parser.generate_ascii(layout_config, layer_name, keys)
                    print(f"Layout: {layout_config.name}")
                    print(ascii_repr)
                    print()
                except ValueError as e:
                    print(f"Error generating ASCII for {layer_name}: {e}")
                    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
