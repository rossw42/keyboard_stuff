"""
Ergogen Point Data Model

This module defines the data structures for representing Ergogen points
converted from KLE keyboard layouts.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
import math


@dataclass
class ErgogenPoint:
    """
    Represents a single point in Ergogen format.
    
    Ergogen points define key positions for PCB generation with:
    - x, y coordinates in millimeters
    - rotation in degrees
    - optional metadata and anchoring
    """
    
    name: str
    x: float
    y: float
    rotation: float = 0.0
    
    # Optional metadata
    tags: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
    
    # Original KLE properties for reference
    kle_row: Optional[int] = None
    kle_col: Optional[int] = None
    kle_width: float = 1.0
    kle_height: float = 1.0
    kle_label: Optional[str] = None
    
    def __post_init__(self):
        """Validate and normalize point data after initialization."""
        # Ensure name is valid
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Point name must be a non-empty string")
        
        # Normalize rotation to 0-360 degrees
        if self.rotation < 0:
            self.rotation = self.rotation % 360
        elif self.rotation >= 360:
            self.rotation = self.rotation % 360
    
    def to_ergogen_dict(self) -> Dict[str, Union[float, str, List[str]]]:
        """
        Convert to Ergogen YAML-compatible dictionary format.
        
        Returns:
            Dictionary suitable for YAML serialization
        """
        point_dict: Dict[str, Union[float, str, List[str]]] = {
            'x': round(self.x, 3),
            'y': round(self.y, 3)
        }
        
        # Only include rotation if non-zero
        if abs(self.rotation) > 0.001:  # Account for floating point precision
            point_dict['r'] = round(self.rotation, 1)
        
        # Add tags if present
        if self.tags:
            point_dict['tags'] = list(self.tags)
        
        # Add metadata if present
        if self.meta:
            point_dict.update(self.meta)
        
        return point_dict
    
    def distance_to(self, other: 'ErgogenPoint') -> float:
        """Calculate Euclidean distance to another point."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def translate(self, dx: float, dy: float) -> 'ErgogenPoint':
        """Create a new point translated by dx, dy."""
        return ErgogenPoint(
            name=self.name,
            x=self.x + dx,
            y=self.y + dy,
            rotation=self.rotation,
            tags=self.tags.copy(),
            meta=self.meta.copy(),
            kle_row=self.kle_row,
            kle_col=self.kle_col,
            kle_width=self.kle_width,
            kle_height=self.kle_height,
            kle_label=self.kle_label
        )
    
    def rotate_around(self, cx: float, cy: float, angle: float) -> 'ErgogenPoint':
        """Create a new point rotated around a center point."""
        # Convert angle to radians
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # Translate to origin
        x = self.x - cx
        y = self.y - cy
        
        # Rotate
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        
        # Translate back
        new_x += cx
        new_y += cy
        
        return ErgogenPoint(
            name=self.name,
            x=new_x,
            y=new_y,
            rotation=self.rotation + angle,
            tags=self.tags.copy(),
            meta=self.meta.copy(),
            kle_row=self.kle_row,
            kle_col=self.kle_col,
            kle_width=self.kle_width,
            kle_height=self.kle_height,
            kle_label=self.kle_label
        )
    
    def __str__(self) -> str:
        """String representation for debugging."""
        return f"ErgogenPoint({self.name}: x={self.x:.1f}, y={self.y:.1f}, r={self.rotation:.1f}°)"


class PointNamingStrategy:
    """Base class for point naming strategies."""
    
    def generate_name(self, row: int, col: int, index: int, label: Optional[str] = None) -> str:
        """Generate a point name based on position and context."""
        raise NotImplementedError
    
    def validate_name(self, name: str) -> bool:
        """Validate if a name follows this strategy's conventions."""
        return isinstance(name, str) and len(name) > 0


class MatrixNamingStrategy(PointNamingStrategy):
    """Matrix-based naming: r0c1, r1c2, etc."""
    
    def generate_name(self, row: int, col: int, index: int, label: Optional[str] = None) -> str:
        return f"r{row}c{col}"
    
    def validate_name(self, name: str) -> bool:
        import re
        return bool(re.match(r'^r\d+c\d+$', name))


class SequentialNamingStrategy(PointNamingStrategy):
    """Sequential naming: key_0, key_1, etc."""
    
    def generate_name(self, row: int, col: int, index: int, label: Optional[str] = None) -> str:
        return f"key_{index}"
    
    def validate_name(self, name: str) -> bool:
        import re
        return bool(re.match(r'^key_\d+$', name))


class LabelNamingStrategy(PointNamingStrategy):
    """Label-based naming: use KLE labels when possible."""
    
    def __init__(self, fallback_strategy: Optional[PointNamingStrategy] = None):
        self.fallback = fallback_strategy or MatrixNamingStrategy()
    
    def generate_name(self, row: int, col: int, index: int, label: Optional[str] = None) -> str:
        if label and self._is_valid_label(label):
            # Clean label for use as identifier
            cleaned = self._clean_label(label)
            if cleaned:
                return cleaned
        
        # Fallback to matrix naming
        return self.fallback.generate_name(row, col, index, label)
    
    def _is_valid_label(self, label: str) -> bool:
        """Check if label is suitable for use as point name."""
        if not label or len(label) > 20:
            return False
        
        # Avoid labels with special characters, newlines, etc.
        import re
        return bool(re.match(r'^[a-zA-Z0-9_+-]+$', label))
    
    def _clean_label(self, label: str) -> str:
        """Clean label for use as identifier."""
        # Remove whitespace, convert to lowercase
        import re
        cleaned = re.sub(r'[^a-zA-Z0-9_+-]', '_', label.strip())
        cleaned = cleaned.lower()
        
        # Remove multiple underscores
        cleaned = re.sub(r'_+', '_', cleaned)
        cleaned = cleaned.strip('_')
        
        return cleaned if cleaned else ""


@dataclass
class PointsCollection:
    """
    Collection of Ergogen points with metadata and validation.
    
    Represents the complete set of points for a keyboard layout
    with utilities for manipulation and export.
    """
    
    points: List[ErgogenPoint] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    naming_strategy: PointNamingStrategy = field(default_factory=MatrixNamingStrategy)
    
    def add_point(self, point: ErgogenPoint) -> None:
        """Add a point to the collection."""
        if not isinstance(point, ErgogenPoint):
            raise ValueError("Must add ErgogenPoint instance")
        
        # Check for duplicate names
        if self.get_point(point.name):
            raise ValueError(f"Point with name '{point.name}' already exists")
        
        self.points.append(point)
    
    def get_point(self, name: str) -> Optional[ErgogenPoint]:
        """Get a point by name."""
        for point in self.points:
            if point.name == name:
                return point
        return None
    
    def remove_point(self, name: str) -> bool:
        """Remove a point by name. Returns True if removed."""
        for i, point in enumerate(self.points):
            if point.name == name:
                del self.points[i]
                return True
        return False
    
    def get_bounds(self) -> Optional[Dict[str, float]]:
        """Get the bounding box of all points."""
        if not self.points:
            return None
        
        min_x = min(p.x for p in self.points)
        max_x = max(p.x for p in self.points)
        min_y = min(p.y for p in self.points)
        max_y = max(p.y for p in self.points)
        
        return {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'width': max_x - min_x,
            'height': max_y - min_y
        }
    
    def translate_all(self, dx: float, dy: float) -> 'PointsCollection':
        """Create a new collection with all points translated."""
        new_points = [point.translate(dx, dy) for point in self.points]
        
        return PointsCollection(
            points=new_points,
            metadata=self.metadata.copy(),
            naming_strategy=self.naming_strategy
        )
    
    def center_on_origin(self) -> 'PointsCollection':
        """Create a new collection centered on (0, 0)."""
        bounds = self.get_bounds()
        if not bounds:
            return self
        
        # Calculate center offset
        center_x = (bounds['min_x'] + bounds['max_x']) / 2
        center_y = (bounds['min_y'] + bounds['max_y']) / 2
        
        return self.translate_all(-center_x, -center_y)
    
    def validate(self) -> List[str]:
        """Validate the points collection and return any errors."""
        errors = []
        
        # Check for empty collection
        if not self.points:
            errors.append("Points collection is empty")
            return errors
        
        # Check for duplicate names
        names = [p.name for p in self.points]
        duplicates = set([name for name in names if names.count(name) > 1])
        for name in duplicates:
            errors.append(f"Duplicate point name: {name}")
        
        # Check for overlapping points (within 0.1mm tolerance)
        for i, point1 in enumerate(self.points):
            for j, point2 in enumerate(self.points[i+1:], i+1):
                if point1.distance_to(point2) < 0.1:
                    errors.append(f"Points {point1.name} and {point2.name} overlap")
        
        # Validate individual points
        for point in self.points:
            try:
                point.__post_init__()  # Re-validate
            except ValueError as e:
                errors.append(f"Point {point.name}: {e}")
        
        return errors
    
    def to_ergogen_dict(self) -> Dict[str, Dict[str, Union[float, str, List[str]]]]:
        """
        Convert to Ergogen YAML-compatible dictionary format.
        
        Returns:
            Dictionary with point names as keys and point data as values
        """
        return {point.name: point.to_ergogen_dict() for point in self.points}
    
    def __len__(self) -> int:
        """Return number of points."""
        return len(self.points)
    
    def __iter__(self):
        """Iterate over points."""
        return iter(self.points)
    
    def __str__(self) -> str:
        """String representation for debugging."""
        return f"PointsCollection({len(self.points)} points)"


# Utility functions for coordinate conversion

def kle_units_to_mm(kle_units: float, key_unit_size: float = 19.05) -> float:
    """
    Convert KLE key units to millimeters.
    
    Args:
        kle_units: Position in KLE key units
        key_unit_size: Size of one key unit in mm (default 19.05mm)
    
    Returns:
        Position in millimeters
    """
    return kle_units * key_unit_size


def mm_to_kle_units(mm: float, key_unit_size: float = 19.05) -> float:
    """
    Convert millimeters to KLE key units.
    
    Args:
        mm: Position in millimeters
        key_unit_size: Size of one key unit in mm (default 19.05mm)
    
    Returns:
        Position in KLE key units
    """
    return mm / key_unit_size
