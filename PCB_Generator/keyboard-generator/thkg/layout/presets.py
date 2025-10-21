"""Predefined layout presets"""

from typing import List, Dict, Any
from thkg.config import Switch


class LayoutPresets:
    """Predefined keyboard layouts"""
    
    # Key unit size in mm
    KEY_UNIT = 19.05
    
    @staticmethod
    def get_preset(preset_name: str) -> List[Switch]:
        """Get a predefined layout
        
        Args:
            preset_name: Name of preset
            
        Returns:
            List of switches for the layout
            
        Raises:
            ValueError: If preset not found
        """
        presets = {
            # Keyboards - Staggered
            '60-ansi': LayoutPresets._60_ansi,
            '60-iso': LayoutPresets._60_iso,
            '65-ansi': LayoutPresets._65_ansi,
            'tkl': LayoutPresets._tkl,
            '40-ansi': LayoutPresets._40_ansi,
            
            # Keyboards - Ortholinear
            '60-ortho': LayoutPresets._60_ortho,
            '40-ortho': LayoutPresets._40_ortho,
            '50-ortho': LayoutPresets._50_ortho,
            
            # Numpads
            'numpad-standard': LayoutPresets._numpad_standard,
            'numpad-compact': LayoutPresets._numpad_compact,
            'numpad-extended': LayoutPresets._numpad_extended,
            
            # Macropads
            'macropad-3x3': LayoutPresets._macropad_3x3,
            'macropad-4x4': LayoutPresets._macropad_4x4,
            'macropad-2x3': LayoutPresets._macropad_2x3,
        }
        
        if preset_name not in presets:
            available = ', '.join(presets.keys())
            raise ValueError(f"Unknown preset '{preset_name}'. Available: {available}")
        
        return presets[preset_name]()
    
    @staticmethod
    def list_presets() -> Dict[str, str]:
        """List all available presets
        
        Returns:
            Dictionary of preset_name: description
        """
        return {
            # Keyboards - Staggered
            '60-ansi': '60% ANSI (61 keys, staggered)',
            '60-iso': '60% ISO (62 keys, staggered)',
            '65-ansi': '65% ANSI (68 keys, staggered, arrow keys)',
            'tkl': 'TKL - Tenkeyless (87 keys, staggered)',
            '40-ansi': '40% (47 keys, staggered)',
            
            # Keyboards - Ortholinear
            '60-ortho': '60% Ortholinear (5x12 = 60 keys, grid)',
            '40-ortho': '40% Ortholinear (4x12 = 48 keys, grid)',
            '50-ortho': '50% Ortholinear (5x10 = 50 keys, grid)',
            
            # Numpads
            'numpad-standard': 'Numpad Standard (4x5 = 20 keys)',
            'numpad-compact': 'Numpad Compact (4x4 = 16 keys)',
            'numpad-extended': 'Numpad Extended (5x4 = 20 keys)',
            
            # Macropads
            'macropad-3x3': 'Macropad 3x3 (9 keys)',
            'macropad-4x4': 'Macropad 4x4 (16 keys)',
            'macropad-2x3': 'Macropad 2x3 (6 keys)',
        }
    
    @staticmethod
    def _60_ansi() -> List[Switch]:
        """60% ANSI layout (61 keys)"""
        switches = []
        row = 0
        
        # Row 0: Esc + numbers + backspace
        for col in range(13):
            switches.append(Switch(row=row, col=col, x=col*19.05, y=row*19.05))
        switches.append(Switch(row=row, col=13, x=13*19.05, y=row*19.05, width=2))  # Backspace
        
        # Row 1: Tab + QWERTY + backslash
        row = 1
        switches.append(Switch(row=row, col=0, x=0, y=row*19.05, width=1.5))  # Tab
        for col in range(1, 14):
            switches.append(Switch(row=row, col=col, x=(col-1+1.5)*19.05, y=row*19.05))
        switches.append(Switch(row=row, col=14, x=13.5*19.05, y=row*19.05, width=1.5))  # Backslash
        
        # Row 2: Caps + ASDF + Enter
        row = 2
        switches.append(Switch(row=row, col=0, x=0, y=row*19.05, width=1.75))  # Caps
        for col in range(1, 12):
            switches.append(Switch(row=row, col=col, x=(col-1+1.75)*19.05, y=row*19.05))
        switches.append(Switch(row=row, col=12, x=(11+1.75)*19.05, y=row*19.05, width=2.25, stabilizer="2u"))  # Enter
        
        # Row 3: Shift + ZXCV + Shift
        row = 3
        switches.append(Switch(row=row, col=0, x=0, y=row*19.05, width=2.25))  # LShift
        for col in range(1, 11):
            switches.append(Switch(row=row, col=col, x=(col-1+2.25)*19.05, y=row*19.05))
        switches.append(Switch(row=row, col=11, x=(10+2.25)*19.05, y=row*19.05, width=2.75))  # RShift
        
        # Row 4: Bottom row (Ctrl, Win, Alt, Space, Alt, Win, Menu, Ctrl)
        row = 4
        for col in range(3):
            switches.append(Switch(row=row, col=col, x=col*1.25*19.05, y=row*19.05, width=1.25))
        switches.append(Switch(row=row, col=3, x=3*1.25*19.05, y=row*19.05, width=6.25, stabilizer="6.25u"))  # Space
        for col in range(4, 8):
            switches.append(Switch(row=row, col=col, x=(3*1.25+6.25+(col-4)*1.25)*19.05, y=row*19.05, width=1.25))
        
        return switches
    
    @staticmethod
    def _60_ortho() -> List[Switch]:
        """60% Ortholinear (5x12 = 60 keys)"""
        switches = []
        for row in range(5):
            for col in range(12):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
    
    @staticmethod
    def _40_ortho() -> List[Switch]:
        """40% Ortholinear (4x12 = 48 keys)"""
        switches = []
        for row in range(4):
            for col in range(12):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
    
    @staticmethod
    def _50_ortho() -> List[Switch]:
        """50% Ortholinear (5x10 = 50 keys)"""
        switches = []
        for row in range(5):
            for col in range(10):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
    
    @staticmethod
    def _numpad_standard() -> List[Switch]:
        """Standard numpad (4x5 = 20 keys)"""
        switches = []
        for row in range(5):
            for col in range(4):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
    
    @staticmethod
    def _numpad_compact() -> List[Switch]:
        """Compact numpad (4x4 = 16 keys)"""
        switches = []
        for row in range(4):
            for col in range(4):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
    
    @staticmethod
    def _numpad_extended() -> List[Switch]:
        """Extended numpad (5x4 = 20 keys)"""
        switches = []
        for row in range(4):
            for col in range(5):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
    
    @staticmethod
    def _macropad_3x3() -> List[Switch]:
        """3x3 macropad (9 keys)"""
        switches = []
        for row in range(3):
            for col in range(3):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
    
    @staticmethod
    def _macropad_4x4() -> List[Switch]:
        """4x4 macropad (16 keys)"""
        switches = []
        for row in range(4):
            for col in range(4):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
    
    @staticmethod
    def _macropad_2x3() -> List[Switch]:
        """2x3 macropad (6 keys)"""
        switches = []
        for row in range(2):
            for col in range(3):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
    
    # Placeholder for other layouts
    @staticmethod
    def _60_iso() -> List[Switch]:
        """60% ISO (placeholder)"""
        return LayoutPresets._60_ansi()  # TODO: Implement ISO layout
    
    @staticmethod
    def _65_ansi() -> List[Switch]:
        """65% ANSI (placeholder)"""
        return LayoutPresets._60_ansi()  # TODO: Implement 65% layout
    
    @staticmethod
    def _40_ansi() -> List[Switch]:
        """40% ANSI (placeholder)"""
        return LayoutPresets._40_ortho()  # TODO: Implement 40% staggered
    
    @staticmethod
    def _tkl() -> List[Switch]:
        """TKL (placeholder)"""
        return LayoutPresets._60_ansi()  # TODO: Implement TKL layout
    
    @staticmethod
    def create_grid(rows: int, cols: int) -> List[Switch]:
        """Create a simple grid layout
        
        Args:
            rows: Number of rows
            cols: Number of columns
            
        Returns:
            List of switches in grid layout
        """
        switches = []
        for row in range(rows):
            for col in range(cols):
                switches.append(Switch(
                    row=row,
                    col=col,
                    x=col * 19.05,
                    y=row * 19.05
                ))
        return switches
