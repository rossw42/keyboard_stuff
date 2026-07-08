#!/usr/bin/env python3
"""
Modular QMK Keymap ASCII Generator

Parses QMK keymap.c files and generates ASCII-art comment blocks for various
keyboard layouts using external configuration files (layouts/*.json) and
templates (templates/*.txt). New keyboards can be added by creating a layout
JSON file and a matching template file - no code changes required.

Usage:
    python modular_keymap_ascii_generator.py <keymap.c>              # print ASCII
    python modular_keymap_ascii_generator.py <keymap.c> --update     # write into file
    python modular_keymap_ascii_generator.py --list                  # list layouts
    python modular_keymap_ascii_generator.py <keymap.c> --layout lily58
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Resolve resource directories relative to this file so the script (and any
# importer, e.g. qmk_format_converter) works regardless of current directory.
SCRIPT_DIR = Path(__file__).resolve().parent

# QMK keycode to readable label mapping
KEYCODE_MAP = {
    # Basic keys
    'KC_ESC': 'ESC', 'KC_TAB': 'Tab', 'KC_CAPS': 'Caps',
    'KC_LSFT': 'LShift', 'KC_RSFT': 'RShift',
    'KC_LCTL': 'LCTRL', 'KC_RCTL': 'RCTRL',
    'KC_LALT': 'LAlt', 'KC_RALT': 'RAlt',
    'KC_LGUI': 'LGUI', 'KC_RGUI': 'RGUI',
    'KC_SPC': 'Space', 'KC_ENT': 'Enter', 'KC_BSPC': 'BackSP',
    'KC_DEL': 'Del', 'KC_INS': 'Ins', 'KC_HOME': 'Home',
    'KC_END': 'End', 'KC_PGUP': 'PgUp', 'KC_PGDN': 'PgDn',
    'KC_PSCR': 'PrtSc', 'KC_SCRL': 'ScrLk', 'KC_PAUS': 'Pause',
    'KC_APP': 'Menu', 'KC_NUBS': 'NUBS', 'KC_NUHS': 'NUHS',

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
    'KC_RIGHT': 'Right',

    # Long-form aliases (older QMK keymaps)
    'KC_ENTER': 'Enter', 'KC_SPACE': 'Space', 'KC_ESCAPE': 'ESC',
    'KC_BSPACE': 'BackSP', 'KC_DELETE': 'Del', 'KC_LSHIFT': 'LShift',
    'KC_RSHIFT': 'RShift', 'KC_LCTRL': 'LCTRL', 'KC_RCTRL': 'RCTRL',
    'KC_CAPSLOCK': 'Caps', 'KC_PGDOWN': 'PgDn', 'KC_GRAVE': '`',
    'KC_MINUS': '-', 'KC_EQUAL': '=', 'KC_LBRACKET': '[', 'KC_RBRACKET': ']',
    'KC_BSLASH': '\\', 'KC_SCOLON': ';', 'KC_QUOTE': "'", 'KC_COMMA': ',',
    'KC_SLASH': '/',

    # Media
    'KC_MUTE': 'Mute', 'KC_VOLU': 'Vol+', 'KC_VOLD': 'Vol-',
    'KC_MPLY': 'Play', 'KC_MNXT': 'Next', 'KC_MPRV': 'Prev',
    'KC_BRIU': 'Bri+', 'KC_BRID': 'Bri-',

    # Special QMK codes
    '_______': '', 'XXXXXXX': '', 'KC_TRNS': '', 'KC_NO': '',
    'QK_BOOT': 'Reset', 'EE_CLR': 'EEClr', 'DB_TOGG': 'Debug',
    'RGB_TOG': 'RGB ON', 'RM_TOGG': 'RGB ON',
    'RGB_HUI': 'HUE+', 'RM_HUEU': 'HUE+', 'RGB_HUD': 'HUE-', 'RM_HUED': 'HUE-',
    'RGB_SAI': 'SAT+', 'RM_SATU': 'SAT+', 'RGB_SAD': 'SAT-', 'RM_SATD': 'SAT-',
    'RGB_VAI': 'VAL+', 'RM_VALU': 'VAL+', 'RGB_VAD': 'VAL-', 'RM_VALD': 'VAL-',
    'RGB_MOD': 'MODE', 'RM_NEXT': 'MODE',
}


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
    """Parses keymap.c files and renders per-layer ASCII diagrams."""

    # Matches e.g. `[_QWERTY] = LAYOUT_split_3x6_3(` and captures the layer name.
    LAYER_RE = re.compile(r'\[\s*_?(\w+)\s*\]\s*=\s*LAYOUT\w*\s*\(')

    def __init__(self, layouts_dir: Optional[str] = None,
                 templates_dir: Optional[str] = None,
                 verbose: bool = False):
        self.layouts_dir = Path(layouts_dir) if layouts_dir else SCRIPT_DIR / 'layouts'
        self.templates_dir = Path(templates_dir) if templates_dir else SCRIPT_DIR / 'templates'
        self.verbose = verbose
        self.keycode_map = KEYCODE_MAP
        self.layouts = self._load_layouts()

    # ------------------------------------------------------------------ #
    # Layout loading
    # ------------------------------------------------------------------ #

    def _load_layouts(self) -> Dict[str, LayoutConfig]:
        """Load keyboard layout configurations from external files."""
        layouts: Dict[str, LayoutConfig] = {}

        if not self.layouts_dir.exists():
            print(f"Warning: Layouts directory '{self.layouts_dir}' not found.", file=sys.stderr)
            return layouts

        if not self.templates_dir.exists():
            print(f"Warning: Templates directory '{self.templates_dir}' not found.", file=sys.stderr)
            return layouts

        required_fields = ('name', 'key_count', 'layout_functions', 'template_file')

        for config_file in sorted(self.layouts_dir.glob('*.json')):
            try:
                config_data = json.loads(config_file.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, OSError) as e:
                print(f"Error reading {config_file}: {e}", file=sys.stderr)
                continue

            missing = [f for f in required_fields if f not in config_data]
            if missing:
                print(f"Error: {config_file} is missing required field(s): {', '.join(missing)}",
                      file=sys.stderr)
                continue

            template_file = self.templates_dir / config_data['template_file']
            if not template_file.exists():
                print(f"Error: Template '{template_file}' not found for layout "
                      f"'{config_data['name']}'", file=sys.stderr)
                continue

            try:
                template_content = template_file.read_text(encoding='utf-8')
            except OSError as e:
                print(f"Error reading {template_file}: {e}", file=sys.stderr)
                continue

            layout_config = LayoutConfig(config_data, template_content)
            layouts[layout_config.name] = layout_config

            if self.verbose:
                print(f"Loaded layout: {layout_config.name} ({layout_config.key_count} keys)")

        return layouts

    def list_available_layouts(self) -> None:
        """List all available keyboard layouts."""
        if not self.layouts:
            print("No layouts available. Make sure layouts/ and templates/ directories "
                  "exist with configuration files.")
            return

        print("Available keyboard layouts:")
        print("=" * 50)
        for name, config in sorted(self.layouts.items()):
            print(f"{name:15} - {config.description}")
            print(f"{'':15}   Keys: {config.key_count}, Functions: {config.layout_functions}")
            if config.tags:
                print(f"{'':15}   Tags: {', '.join(config.tags)}")
            print()

    # ------------------------------------------------------------------ #
    # Detection / parsing
    # ------------------------------------------------------------------ #

    def detect_layout(self, content: str, key_count: int) -> Optional[LayoutConfig]:
        """Detect keyboard layout based on layout function name and key count."""
        # Specific layout function names + matching key count (most reliable)
        for layout_config in self.layouts.values():
            for layout_function in layout_config.layout_functions:
                if layout_function in content and key_count == layout_config.key_count:
                    return layout_config

        # Fallback: match by key count only
        for layout_config in self.layouts.values():
            if key_count == layout_config.key_count:
                return layout_config

        return None

    @staticmethod
    def _strip_comments(text: str) -> str:
        """Remove C block comments and line comments."""
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        text = re.sub(r'//[^\n]*', '', text)
        return text

    @staticmethod
    def _split_top_level_args(text: str) -> List[str]:
        """Split comma-separated arguments, respecting nested parentheses.

        This keeps multi-argument keycodes like LT(_LOWER, KC_SPC) intact.
        """
        args: List[str] = []
        depth = 0
        current: List[str] = []
        for ch in text:
            if ch == '(':
                depth += 1
                current.append(ch)
            elif ch == ')':
                depth -= 1
                current.append(ch)
            elif ch == ',' and depth == 0:
                args.append(''.join(current).strip())
                current = []
            else:
                current.append(ch)
        tail = ''.join(current).strip()
        if tail:
            args.append(tail)
        return args

    def parse_layout_keys(self, content: str, start_pos: int) -> List[str]:
        """Parse the keycodes from a LAYOUT(...) call starting at/after start_pos."""
        paren_start = content.find('(', start_pos)
        if paren_start == -1:
            return []

        # Find the matching closing parenthesis
        depth = 1
        pos = paren_start + 1
        while pos < len(content) and depth > 0:
            if content[pos] == '(':
                depth += 1
            elif content[pos] == ')':
                depth -= 1
            pos += 1

        if depth != 0:
            return []

        layout_content = self._strip_comments(content[paren_start + 1:pos - 1])
        return [k for k in self._split_top_level_args(layout_content)
                if self._is_valid_keycode(k)]

    @staticmethod
    def _is_valid_keycode(key: str) -> bool:
        """Check that a token looks like a QMK keycode (identifier or call)."""
        return bool(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(\(.*\))?', key.strip(), re.DOTALL))

    def keycode_to_label(self, keycode: str) -> str:
        """Convert a QMK keycode to a short readable label."""
        # Layer keys like MO(_LOWER) / MO(LOWER) -> layer name
        match = re.fullmatch(r'(?:MO|TG|TT|OSL|DF|TO)\(\s*_?(\w+)\s*\)', keycode)
        if match:
            return match.group(1)

        # Other function-like keycodes (LT, MT, LCTL_T, ...) -> function name
        if '(' in keycode:
            return keycode.split('(')[0]

        return self.keycode_map.get(keycode, keycode)

    def format_key_for_ascii(self, keycode: str, width: int = 6) -> str:
        """Format a key label to fit in the ASCII representation."""
        label = self.keycode_to_label(keycode)

        if not label:
            return ' ' * width

        if len(label) > width:
            return label[:width]
        return label.center(width)

    # ------------------------------------------------------------------ #
    # Generation
    # ------------------------------------------------------------------ #

    def generate_ascii(self, layout_config: LayoutConfig, layer_name: str,
                       keys: List[str]) -> str:
        """Generate ASCII representation for the specified layout."""
        if len(keys) != layout_config.key_count:
            raise ValueError(f"Expected {layout_config.key_count} keys for "
                             f"{layout_config.name}, got {len(keys)}")

        key_dict = {f'k{i}': self.format_key_for_ascii(keycode)
                    for i, keycode in enumerate(keys)}

        return layout_config.template.format(layer_name=layer_name, **key_dict).rstrip('\n')

    def parse_keymap_file(self, filename: str,
                          forced_layout: Optional[str] = None
                          ) -> Dict[str, Tuple[List[str], LayoutConfig]]:
        """Parse a keymap.c file and extract all layers with their layout configs."""
        content = Path(filename).read_text(encoding='utf-8', errors='replace')

        layers: Dict[str, Tuple[List[str], LayoutConfig]] = {}

        for match in self.LAYER_RE.finditer(content):
            layer_name = match.group(1)
            keys = self.parse_layout_keys(content, match.end() - 1)
            if not keys:
                continue

            layout_config = None
            if forced_layout and forced_layout in self.layouts:
                candidate = self.layouts[forced_layout]
                if len(keys) == candidate.key_count:
                    layout_config = candidate
                else:
                    print(f"Warning: Forced layout '{forced_layout}' expects "
                          f"{candidate.key_count} keys, but layer '{layer_name}' has "
                          f"{len(keys)} keys; falling back to auto-detection.",
                          file=sys.stderr)

            if layout_config is None:
                layout_config = self.detect_layout(content, len(keys))

            if layout_config:
                layers[layer_name] = (keys, layout_config)
            else:
                print(f"Warning: Could not detect layout for layer '{layer_name}' "
                      f"with {len(keys)} keys", file=sys.stderr)

        return layers

    def update_keymap_file(self, filename: str, backup: bool = True,
                           forced_layout: Optional[str] = None) -> None:
        """Update the keymap file in place with generated ASCII comment blocks."""
        content = Path(filename).read_text(encoding='utf-8', errors='replace')

        if backup:
            Path(f"{filename}.backup").write_text(content, encoding='utf-8')

        layers = self.parse_keymap_file(filename, forced_layout)

        for layer_name, (keys, layout_config) in layers.items():
            try:
                new_ascii = self.generate_ascii(layout_config, layer_name, keys)
            except ValueError as e:
                print(f"Error processing layer {layer_name}: {e}", file=sys.stderr)
                continue

            # Replace existing comment block for this layer, if present
            pattern = rf'/\*\s*{re.escape(layer_name)}\b.*?\*/'
            match = re.search(pattern, content, re.DOTALL)

            if match:
                content = content.replace(match.group(0), new_ascii)
            else:
                # Insert before the layer's LAYOUT definition
                layout_pattern = rf'\[\s*_?{re.escape(layer_name)}\s*\]\s*=\s*LAYOUT'
                layout_match = re.search(layout_pattern, content)
                if layout_match:
                    insert_pos = layout_match.start()
                    content = (content[:insert_pos] + new_ascii + '\n\n'
                               + content[insert_pos:])

        Path(filename).write_text(content, encoding='utf-8')


def main() -> None:
    arg_parser = argparse.ArgumentParser(
        description='Generate ASCII-art layer diagrams from QMK keymap.c files.',
        epilog='To add a new keyboard: create layouts/<name>.json and '
               'templates/<name>.txt (see README.md).')
    arg_parser.add_argument('keymap', nargs='?', help='Path to QMK keymap.c file')
    arg_parser.add_argument('--update', action='store_true',
                            help='Write generated ASCII into the keymap file '
                                 '(a .backup copy is created)')
    arg_parser.add_argument('--list', action='store_true',
                            help='List all available keyboard layouts')
    arg_parser.add_argument('--layout', metavar='NAME',
                            help='Force a specific layout (e.g. --layout lily58)')
    arg_parser.add_argument('--no-backup', action='store_true',
                            help='Skip creating a .backup file with --update')
    arg_parser.add_argument('--verbose', action='store_true',
                            help='Print layout loading details')
    args = arg_parser.parse_args()

    parser = ModularKeymapParser(verbose=args.verbose)

    if args.list:
        parser.list_available_layouts()
        return

    if not args.keymap:
        arg_parser.print_help()
        sys.exit(1)

    if args.layout and args.layout not in parser.layouts:
        print(f"Error: Layout '{args.layout}' not found. Available layouts:")
        for name in sorted(parser.layouts):
            print(f"  - {name}")
        sys.exit(1)

    try:
        layers = parser.parse_keymap_file(args.keymap, args.layout)
    except FileNotFoundError:
        print(f"Error: File '{args.keymap}' not found", file=sys.stderr)
        sys.exit(1)

    if not layers:
        print("No supported layouts found in the keymap file.")
        print("Run with --list to see available layouts.")
        sys.exit(1)

    if args.update:
        parser.update_keymap_file(args.keymap, backup=not args.no_backup,
                                  forced_layout=args.layout)
        print(f"Updated {args.keymap} with generated ASCII representations")
    else:
        for layer_name, (keys, layout_config) in layers.items():
            try:
                print(f"Layout: {layout_config.name}")
                print(parser.generate_ascii(layout_config, layer_name, keys))
                print()
            except ValueError as e:
                print(f"Error generating ASCII for {layer_name}: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()