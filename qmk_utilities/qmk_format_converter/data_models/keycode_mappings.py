"""
Keycode Mapping System

This module provides mapping between different keycode formats used by
KLE, VIA, and QMK keymap.c files.
"""

from typing import Dict, Optional, Set, List
from dataclasses import dataclass


@dataclass
class KeycodeMapping:
    """Represents a keycode mapping between different formats."""
    qmk_code: str           # QMK keycode (e.g., "KC_A")
    kle_label: str          # KLE label (e.g., "A")
    via_code: str           # VIA keycode (same as QMK usually)
    description: str        # Human readable description
    category: str           # Category (basic, modifier, function, etc.)


class KeycodeMappingSystem:
    """
    Central system for managing keycode mappings between formats.
    
    This class provides bidirectional mapping between:
    - QMK keycodes (KC_A, KC_LSFT, etc.)
    - KLE labels (A, Shift, etc.)
    - VIA keycodes (usually same as QMK)
    """
    
    def __init__(self):
        self.mappings: Dict[str, KeycodeMapping] = {}
        self._initialize_mappings()
    
    def _initialize_mappings(self):
        """Initialize the standard keycode mappings."""
        
        # Basic letter keys
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            mapping = KeycodeMapping(
                qmk_code=f"KC_{letter}",
                kle_label=letter,
                via_code=f"KC_{letter}",
                description=f"Letter {letter}",
                category="basic"
            )
            self.mappings[mapping.qmk_code] = mapping
        
        # Number keys
        for num in "1234567890":
            mapping = KeycodeMapping(
                qmk_code=f"KC_{num}",
                kle_label=num,
                via_code=f"KC_{num}",
                description=f"Number {num}",
                category="basic"
            )
            self.mappings[mapping.qmk_code] = mapping
        
        # Special character mappings
        special_chars = [
            ("KC_GRV", "`", "Grave/Tilde"),
            ("KC_MINS", "-", "Minus/Underscore"),
            ("KC_EQL", "=", "Equal/Plus"),
            ("KC_LBRC", "[", "Left Bracket"),
            ("KC_RBRC", "]", "Right Bracket"),
            ("KC_BSLS", "\\", "Backslash/Pipe"),
            ("KC_SCLN", ";", "Semicolon/Colon"),
            ("KC_QUOT", "'", "Quote/Double Quote"),
            ("KC_COMM", ",", "Comma/Less Than"),
            ("KC_DOT", ".", "Period/Greater Than"),
            ("KC_SLSH", "/", "Slash/Question Mark"),
        ]
        
        for qmk, kle, desc in special_chars:
            mapping = KeycodeMapping(
                qmk_code=qmk,
                kle_label=kle,
                via_code=qmk,
                description=desc,
                category="punctuation"
            )
            self.mappings[qmk] = mapping
        
        # Function keys
        for i in range(1, 25):  # F1-F24
            mapping = KeycodeMapping(
                qmk_code=f"KC_F{i}",
                kle_label=f"F{i}",
                via_code=f"KC_F{i}",
                description=f"Function Key {i}",
                category="function"
            )
            self.mappings[mapping.qmk_code] = mapping
        
        # Modifier keys
        modifiers = [
            ("KC_LCTL", "Ctrl", "Left Control"),
            ("KC_LSFT", "Shift", "Left Shift"),
            ("KC_LALT", "Alt", "Left Alt"),
            ("KC_LGUI", "Win", "Left GUI/Windows"),
            ("KC_RCTL", "Ctrl", "Right Control"),
            ("KC_RSFT", "Shift", "Right Shift"),
            ("KC_RALT", "Alt", "Right Alt"),
            ("KC_RGUI", "Win", "Right GUI/Windows"),
        ]
        
        for qmk, kle, desc in modifiers:
            mapping = KeycodeMapping(
                qmk_code=qmk,
                kle_label=kle,
                via_code=qmk,
                description=desc,
                category="modifier"
            )
            self.mappings[qmk] = mapping
        
        # Special keys
        special_keys = [
            ("KC_SPC", "Space", "Space Bar"),
            ("KC_ENT", "Enter", "Enter/Return"),
            ("KC_ESC", "Esc", "Escape"),
            ("KC_BSPC", "Backspace", "Backspace"),
            ("KC_TAB", "Tab", "Tab"),
            ("KC_CAPS", "Caps Lock", "Caps Lock"),
            ("KC_DEL", "Del", "Delete"),
            ("KC_INS", "Ins", "Insert"),
            ("KC_HOME", "Home", "Home"),
            ("KC_END", "End", "End"),
            ("KC_PGUP", "PgUp", "Page Up"),
            ("KC_PGDN", "PgDn", "Page Down"),
            ("KC_UP", "↑", "Up Arrow"),
            ("KC_DOWN", "↓", "Down Arrow"),
            ("KC_LEFT", "←", "Left Arrow"),
            ("KC_RGHT", "→", "Right Arrow"),
            ("KC_PSCR", "PrtSc", "Print Screen"),
            ("KC_SLCK", "ScrLk", "Scroll Lock"),
            ("KC_PAUS", "Pause", "Pause/Break"),
            ("KC_APP", "Menu", "Application/Menu"),
            ("KC_MUTE", "Mute", "Audio Mute"),
            ("KC_VOLU", "Vol+", "Volume Up"),
            ("KC_VOLD", "Vol-", "Volume Down"),
        ]
        
        for qmk, kle, desc in special_keys:
            mapping = KeycodeMapping(
                qmk_code=qmk,
                kle_label=kle,
                via_code=qmk,
                description=desc,
                category="special"
            )
            self.mappings[qmk] = mapping
        
        # Transparent and No-op
        self.mappings["KC_TRNS"] = KeycodeMapping(
            qmk_code="KC_TRNS",
            kle_label="",
            via_code="KC_TRNS",
            description="Transparent (use lower layer)",
            category="meta"
        )
        
        self.mappings["KC_NO"] = KeycodeMapping(
            qmk_code="KC_NO",
            kle_label="",
            via_code="KC_NO",
            description="No operation",
            category="meta"
        )
    
    def qmk_to_kle(self, qmk_code: str) -> Optional[str]:
        """Convert QMK keycode to KLE label."""
        mapping = self.mappings.get(qmk_code)
        return mapping.kle_label if mapping else None
    
    def kle_to_qmk(self, kle_label: str) -> Optional[str]:
        """Convert KLE label to QMK keycode."""
        for mapping in self.mappings.values():
            if mapping.kle_label == kle_label:
                return mapping.qmk_code
        return None
    
    def qmk_to_via(self, qmk_code: str) -> Optional[str]:
        """Convert QMK keycode to VIA keycode (usually the same)."""
        mapping = self.mappings.get(qmk_code)
        return mapping.via_code if mapping else qmk_code
    
    def via_to_qmk(self, via_code: str) -> Optional[str]:
        """Convert VIA keycode to QMK keycode (usually the same)."""
        return via_code  # VIA uses QMK keycodes
    
    def get_mapping(self, qmk_code: str) -> Optional[KeycodeMapping]:
        """Get the complete mapping for a QMK keycode."""
        return self.mappings.get(qmk_code)
    
    def get_categories(self) -> Set[str]:
        """Get all keycode categories."""
        return {mapping.category for mapping in self.mappings.values()}
    
    def get_keycodes_by_category(self, category: str) -> List[KeycodeMapping]:
        """Get all keycodes in a specific category."""
        return [mapping for mapping in self.mappings.values() 
                if mapping.category == category]
    
    def is_valid_qmk_keycode(self, keycode: str) -> bool:
        """Check if a keycode is a valid QMK keycode."""
        return keycode in self.mappings
    
    def suggest_keycode(self, partial: str) -> List[str]:
        """Suggest QMK keycodes based on partial input."""
        partial_upper = partial.upper()
        suggestions = []
        
        for qmk_code in self.mappings.keys():
            if partial_upper in qmk_code:
                suggestions.append(qmk_code)
        
        return sorted(suggestions)
    
    def parse_kle_key_label(self, label: str) -> str:
        """
        Parse a KLE key label and extract the primary keycode.
        
        KLE labels can be complex with multiple lines (e.g., "!\n1" for shift+1).
        This function extracts the most likely primary keycode.
        """
        if not label:
            return "KC_NO"
        
        # Handle multi-line labels (shift variants)
        lines = label.split('\n')
        if len(lines) > 1:
            # Use the bottom line as primary (unshifted)
            primary_label = lines[-1]
        else:
            primary_label = lines[0]
        
        # Clean up the label
        primary_label = primary_label.strip()
        
        # Direct mapping lookup
        qmk_code = self.kle_to_qmk(primary_label)
        if qmk_code:
            return qmk_code
        
        # Handle special cases
        special_mappings = {
            "Space": "KC_SPC",
            " ": "KC_SPC",
            "Backspace": "KC_BSPC",
            "Delete": "KC_DEL",
            "Return": "KC_ENT",
            "Enter": "KC_ENT",
        }
        
        if primary_label in special_mappings:
            return special_mappings[primary_label]
        
        # If no mapping found, return transparent
        return "KC_TRNS"


# Global instance for easy access
KEYCODE_MAPPER = KeycodeMappingSystem()
