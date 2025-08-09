"""
Universal Layout Data Model

This module defines the universal intermediate representation for keyboard layouts
that can capture data from KLE, VIA, and keymap.c formats.

The design philosophy is to create a comprehensive data model that can represent:
- Physical layout (key positions, sizes, rotations from KLE)
- Logical keymap data (layers, keycodes from VIA/keymap.c)
- Metadata (keyboard information, authoring details)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Any
from enum import Enum


class KeySize(Enum):
    """Standard key sizes in keyboard layouts."""
    UNIT_1 = 1.0      # Standard 1u key
    UNIT_1_25 = 1.25  # Common modifier size
    UNIT_1_5 = 1.5    # Tab key size
    UNIT_1_75 = 1.75  # Caps lock size
    UNIT_2 = 2.0      # Backspace size
    UNIT_2_25 = 2.25  # Left shift size
    UNIT_2_75 = 2.75  # Right shift size  
    UNIT_6_25 = 6.25  # Standard spacebar
    UNIT_7 = 7.0      # Full spacebar


@dataclass
class KeyDefinition:
    """
    Represents a single key with both physical and logical properties.
    
    This class captures all the information needed to represent a key across
    all three target formats (KLE, VIA, keymap.c).
    """
    # Physical properties (mainly from KLE)
    x: float = 0.0              # X position (in key units)
    y: float = 0.0              # Y position (in key units)
    width: float = 1.0          # Key width (in key units)
    height: float = 1.0         # Key height (in key units)
    rotation_angle: float = 0.0  # Rotation in degrees
    rotation_x: float = 0.0     # Rotation origin X
    rotation_y: float = 0.0     # Rotation origin Y
    
    # Visual properties (from KLE)
    color: str = "#cccccc"      # Key color
    text_color: str = "#000000"  # Text color
    font_size: int = 3          # Font size (KLE scale)
    
    # Logical properties (from VIA/keymap.c)
    matrix_row: Optional[int] = None    # Matrix row position
    matrix_col: Optional[int] = None    # Matrix column position
    keycode: Optional[str] = None       # Default keycode
    
    # Labels (from all formats)
    primary_label: str = ""             # Main key label
    secondary_labels: List[str] = field(default_factory=list)  # Additional labels
    
    # Layout metadata
    key_id: Optional[str] = None        # Unique identifier
    profile: str = "OEM"                # Key profile (OEM, Cherry, etc.)
    
    def __post_init__(self):
        """Validate and normalize key data after initialization."""
        # Ensure secondary_labels is a list
        if self.secondary_labels is None:
            self.secondary_labels = []
        
        # Normalize dimensions to positive values
        self.width = max(0.1, self.width)
        self.height = max(0.1, self.height)
        
        # Normalize rotation angle to 0-360 range
        self.rotation_angle = self.rotation_angle % 360


@dataclass 
class LayerDefinition:
    """
    Represents a keyboard layer with keycodes for each key position.
    
    Layers are the core concept in QMK keymaps, representing different
    key functions that can be activated.
    """
    name: str                           # Layer name (e.g., "QWERTY", "LOWER")
    index: int                          # Layer index (0-based)
    keycodes: List[str] = field(default_factory=list)  # Keycode for each key position
    description: str = ""               # Layer description
    is_default: bool = False            # Is this the default layer?
    
    # Layer activation (for complex layers)
    activation_type: str = "momentary"  # momentary, toggle, one_shot
    activation_key: Optional[str] = None # Key that activates this layer
    
    def __post_init__(self):
        """Validate layer data after initialization."""
        if not self.name:
            self.name = f"Layer_{self.index}"


@dataclass
class UniversalLayout:
    """
    Universal representation of a keyboard layout that can capture data
    from KLE, VIA, and keymap.c formats.
    
    This serves as the intermediate format for all conversions.
    """
    # Basic keyboard information
    name: str = "Untitled Keyboard"
    description: str = ""
    author: str = ""
    version: str = "1.0"
    
    # Physical layout
    keys: List[KeyDefinition] = field(default_factory=list)
    
    # Logical layout
    layers: List[LayerDefinition] = field(default_factory=list)
    
    # Keyboard metadata
    vendor_id: Optional[str] = None     # USB Vendor ID
    product_id: Optional[str] = None    # USB Product ID
    device_version: str = "0.0.1"      # Device version
    manufacturer: str = ""              # Manufacturer name
    product: str = ""                   # Product name
    keyboard: str = ""                  # Keyboard identifier (e.g., "lily58/rev1")
    
    # Layout information (for QMK)
    layout_name: str = "LAYOUT"        # QMK LAYOUT function name
    matrix_rows: int = 0                # Matrix dimensions
    matrix_cols: int = 0
    
    # Format-specific metadata
    kle_metadata: Dict[str, Any] = field(default_factory=dict)    # KLE-specific data
    via_metadata: Dict[str, Any] = field(default_factory=dict)    # VIA-specific data
    qmk_metadata: Dict[str, Any] = field(default_factory=dict)    # QMK-specific data
    qmk_configurator_metadata: Dict[str, Any] = field(default_factory=dict)  # QMK Configurator-specific data
    
    def __post_init__(self):
        """Validate and set up the layout after initialization."""
        # Ensure we have at least empty collections
        if self.keys is None:
            self.keys = []
        if self.layers is None:
            self.layers = []
            
        # Set matrix dimensions if not provided
        if self.matrix_rows == 0 or self.matrix_cols == 0:
            self._calculate_matrix_dimensions()
            
        # Ensure we have at least one layer
        if not self.layers:
            default_layer = LayerDefinition(
                name="Default",
                index=0,
                keycodes=["KC_TRNS"] * len(self.keys),
                is_default=True
            )
            self.layers.append(default_layer)
    
    def _calculate_matrix_dimensions(self):
        """Calculate matrix dimensions from key definitions."""
        if not self.keys:
            return
            
        max_row = 0
        max_col = 0
        
        for key in self.keys:
            if key.matrix_row is not None:
                max_row = max(max_row, key.matrix_row)
            if key.matrix_col is not None:
                max_col = max(max_col, key.matrix_col)
        
        self.matrix_rows = max_row + 1 if max_row > 0 else len(self.keys) // 10 + 1
        self.matrix_cols = max_col + 1 if max_col > 0 else 10
    
    def add_key(self, key: KeyDefinition) -> None:
        """Add a key to the layout."""
        self.keys.append(key)
        
        # Update layer keycodes to match new key count
        for layer in self.layers:
            if len(layer.keycodes) < len(self.keys):
                layer.keycodes.extend(["KC_TRNS"] * (len(self.keys) - len(layer.keycodes)))
    
    def add_layer(self, layer: LayerDefinition) -> None:
        """Add a layer to the layout."""
        # Ensure keycodes list matches key count
        if len(layer.keycodes) < len(self.keys):
            layer.keycodes.extend(["KC_TRNS"] * (len(self.keys) - len(layer.keycodes)))
        elif len(layer.keycodes) > len(self.keys):
            layer.keycodes = layer.keycodes[:len(self.keys)]
            
        self.layers.append(layer)
    
    def get_key_count(self) -> int:
        """Get the total number of keys in the layout."""
        return len(self.keys)
    
    def get_layer_count(self) -> int:
        """Get the total number of layers in the layout."""
        return len(self.layers)
    
    def get_layer_by_name(self, name: str) -> Optional[LayerDefinition]:
        """Get a layer by its name."""
        for layer in self.layers:
            if layer.name == name:
                return layer
        return None
    
    def get_layer_by_index(self, index: int) -> Optional[LayerDefinition]:
        """Get a layer by its index."""
        for layer in self.layers:
            if layer.index == index:
                return layer
        return None
    
    def validate(self) -> List[str]:
        """
        Validate the layout and return a list of validation errors.
        
        Returns:
            List of error messages. Empty list means valid.
        """
        errors = []
        
        # Check basic requirements
        if not self.name.strip():
            errors.append("Layout name cannot be empty")
            
        if not self.keys:
            errors.append("Layout must have at least one key")
            
        if not self.layers:
            errors.append("Layout must have at least one layer")
        
        # Validate keys
        for i, key in enumerate(self.keys):
            if key.width <= 0 or key.height <= 0:
                errors.append(f"Key {i}: Invalid dimensions ({key.width}x{key.height})")
        
        # Validate layers
        for layer in self.layers:
            if len(layer.keycodes) != len(self.keys):
                errors.append(f"Layer '{layer.name}': Keycode count mismatch "
                            f"({len(layer.keycodes)} vs {len(self.keys)} keys)")
        
        # Check for duplicate layer indices
        layer_indices = [layer.index for layer in self.layers]
        if len(layer_indices) != len(set(layer_indices)):
            errors.append("Duplicate layer indices found")
        
        return errors
    
    def summary(self) -> Dict[str, Any]:
        """Generate a summary of the layout."""
        return {
            "name": self.name,
            "author": self.author,
            "version": self.version,
            "key_count": len(self.keys),
            "layer_count": len(self.layers),
            "matrix_size": f"{self.matrix_rows}x{self.matrix_cols}",
            "layout_name": self.layout_name,
            "layers": [layer.name for layer in self.layers],
            "validation_errors": self.validate()
        }
