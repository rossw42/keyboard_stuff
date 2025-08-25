"""
KLE to Ergogen Converter

This module provides the main converter class for transforming KLE layouts 
to Ergogen points format.
"""

import sys
import os
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

# Use the simple KLE parser for standalone operation
from .simple_kle_parser import SimpleKLEParser as KLEParser, KLEParseError, UniversalLayout, KeyDefinition

from kle_to_ergogen.data_models.ergogen_point import (
    ErgogenPoint, 
    PointsCollection, 
    PointNamingStrategy, 
    MatrixNamingStrategy,
    SequentialNamingStrategy,
    LabelNamingStrategy,
    kle_units_to_mm
)


class KLEToErgogenError(Exception):
    """Raised when KLE to Ergogen conversion fails."""
    pass


class KLEToErgogenConverter:
    """
    Main converter class for transforming KLE layouts to Ergogen points.
    
    This class handles the complete conversion pipeline:
    1. Parse KLE data using existing parser
    2. Transform coordinates from KLE to Ergogen format
    3. Apply naming strategies
    4. Generate validated points collection
    """
    
    def __init__(
        self,
        key_unit_size: float = 19.05,
        naming_strategy: Optional[PointNamingStrategy] = None,
        center_on_origin: bool = True,
        invert_y_axis: bool = True
    ):
        """
        Initialize the converter.
        
        Args:
            key_unit_size: Size of one key unit in mm (default: 19.05mm)
            naming_strategy: Strategy for naming points (default: MatrixNamingStrategy)
            center_on_origin: Whether to center layout on origin (default: True)
            invert_y_axis: Whether to invert Y-axis for Ergogen (default: True)
        """
        self.key_unit_size = key_unit_size
        self.naming_strategy = naming_strategy or MatrixNamingStrategy()
        self.center_on_origin = center_on_origin
        self.invert_y_axis = invert_y_axis
        
        # Initialize KLE parser
        self.kle_parser = KLEParser()
    
    def convert_file(self, kle_file_path: str) -> PointsCollection:
        """
        Convert a KLE file to Ergogen points.
        
        Args:
            kle_file_path: Path to KLE JSON file
            
        Returns:
            PointsCollection with converted points
            
        Raises:
            KLEToErgogenError: If conversion fails
        """
        try:
            # Parse KLE file
            kle_layout = self.kle_parser.parse_file(kle_file_path)
            return self.convert_layout(kle_layout)
        
        except KLEParseError as e:
            raise KLEToErgogenError(f"Failed to parse KLE file: {e}")
        except Exception as e:
            raise KLEToErgogenError(f"Conversion failed: {e}")
    
    def convert_json(self, kle_json: str) -> PointsCollection:
        """
        Convert KLE JSON string to Ergogen points.
        
        Args:
            kle_json: KLE JSON string
            
        Returns:
            PointsCollection with converted points
            
        Raises:
            KLEToErgogenError: If conversion fails
        """
        try:
            # Parse KLE JSON
            kle_layout = self.kle_parser.parse_json(kle_json)
            return self.convert_layout(kle_layout)
        
        except KLEParseError as e:
            raise KLEToErgogenError(f"Failed to parse KLE JSON: {e}")
        except Exception as e:
            raise KLEToErgogenError(f"Conversion failed: {e}")
    
    def convert_layout(self, kle_layout: UniversalLayout) -> PointsCollection:
        """
        Convert a parsed KLE layout to Ergogen points.
        
        Args:
            kle_layout: Parsed UniversalLayout from KLE
            
        Returns:
            PointsCollection with converted points
        """
        if not kle_layout.keys:
            raise KLEToErgogenError("No keys found in KLE layout")
        
        # Create points collection
        points_collection = PointsCollection(
            naming_strategy=self.naming_strategy,
            metadata={
                'source': 'KLE',
                'key_unit_size': self.key_unit_size,
                'total_keys': len(kle_layout.keys),
                'layout_name': kle_layout.name or 'Unnamed Layout'
            }
        )
        
        # Convert each key to Ergogen point
        for index, key in enumerate(kle_layout.keys):
            try:
                point = self._convert_key_to_point(key, index)
                points_collection.add_point(point)
            except Exception as e:
                # Log warning and continue with other keys
                print(f"Warning: Failed to convert key {index}: {e}")
                continue
        
        # Apply transformations
        if self.center_on_origin:
            points_collection = points_collection.center_on_origin()
        
        # Validate result
        validation_errors = points_collection.validate()
        if validation_errors:
            print("Validation warnings:")
            for error in validation_errors:
                print(f"  - {error}")
        
        return points_collection
    
    def _convert_key_to_point(self, key: KeyDefinition, index: int) -> ErgogenPoint:
        """
        Convert a single KLE key to an Ergogen point.
        
        Args:
            key: KLE KeyDefinition
            index: Key index for sequential naming
            
        Returns:
            ErgogenPoint instance
        """
        # Extract coordinates
        x_kle = key.x or 0.0
        y_kle = key.y or 0.0
        
        # Convert units from KLE key units to millimeters
        x_mm = kle_units_to_mm(x_kle, self.key_unit_size)
        y_mm = kle_units_to_mm(y_kle, self.key_unit_size)
        
        # Handle Y-axis inversion if enabled
        if self.invert_y_axis:
            y_mm = -y_mm
        
        # Handle rotation
        rotation = key.rotation_angle or 0.0
        
        # If key has rotation center, we need to handle it
        # For now, we'll use the rotation as-is
        # TODO: Implement proper rotation center handling
        
        # Generate point name using naming strategy
        point_name = self.naming_strategy.generate_name(
            row=key.matrix_row or 0,
            col=key.matrix_col or 0,
            index=index,
            label=key.primary_label
        )
        
        # Create Ergogen point
        point = ErgogenPoint(
            name=point_name,
            x=x_mm,
            y=y_mm,
            rotation=rotation,
            kle_row=key.matrix_row,
            kle_col=key.matrix_col,
            kle_width=key.width or 1.0,
            kle_height=key.height or 1.0,
            kle_label=key.primary_label
        )
        
        # Add tags based on key properties
        tags = []
        
        # Add size tags for non-standard keys
        if key.width and key.width != 1.0:
            tags.append(f"width_{key.width}u")
        if key.height and key.height != 1.0:
            tags.append(f"height_{key.height}u")
        
        # Add rotation tag for rotated keys
        if abs(rotation) > 0.1:
            tags.append(f"rotated_{int(rotation)}deg")
        
        # Add matrix position tags
        if key.matrix_row is not None:
            tags.append(f"row_{key.matrix_row}")
        if key.matrix_col is not None:
            tags.append(f"col_{key.matrix_col}")
        
        point.tags = tags
        
        # Add metadata
        point.meta = {
            'kle_index': index,
            'kle_keycode': key.keycode,
            'kle_color': key.color,
            'original_x': x_kle,
            'original_y': y_kle
        }
        
        return point
    
    def get_conversion_stats(self, points_collection: PointsCollection) -> Dict[str, Any]:
        """
        Get statistics about the conversion.
        
        Args:
            points_collection: Converted points collection
            
        Returns:
            Dictionary with conversion statistics
        """
        if not points_collection.points:
            return {'total_points': 0}
        
        # Calculate bounds
        bounds = points_collection.get_bounds()
        
        # Count special keys
        rotated_count = sum(1 for p in points_collection.points if abs(p.rotation) > 0.1)
        wide_keys = sum(1 for p in points_collection.points if p.kle_width > 1.0)
        tall_keys = sum(1 for p in points_collection.points if p.kle_height > 1.0)
        
        return {
            'total_points': len(points_collection.points),
            'bounds': bounds,
            'layout_size_mm': {
                'width': bounds['width'] if bounds else 0,
                'height': bounds['height'] if bounds else 0
            },
            'special_keys': {
                'rotated': rotated_count,
                'wide_keys': wide_keys,
                'tall_keys': tall_keys
            },
            'naming_strategy': type(self.naming_strategy).__name__,
            'settings': {
                'key_unit_size': self.key_unit_size,
                'center_on_origin': self.center_on_origin,
                'invert_y_axis': self.invert_y_axis
            }
        }
    
    def validate_kle_file(self, kle_file_path: str) -> List[str]:
        """
        Validate a KLE file before conversion.
        
        Args:
            kle_file_path: Path to KLE JSON file
            
        Returns:
            List of validation errors (empty if valid)
        """
        try:
            # Use KLE parser validation
            errors = []
            
            # First check if file exists
            if not os.path.exists(kle_file_path):
                errors.append(f"File does not exist: {kle_file_path}")
                return errors
            
            # Try to parse the file
            try:
                kle_layout = self.kle_parser.parse_file(kle_file_path)
                
                # Check for empty layout
                if not kle_layout.keys:
                    errors.append("No keys found in layout")
                
                # Check for keys with missing coordinates
                for i, key in enumerate(kle_layout.keys):
                    if key.x is None or key.y is None:
                        errors.append(f"Key {i} missing coordinates")
                
                # Check for reasonable coordinate ranges
                for i, key in enumerate(kle_layout.keys):
                    if key.x and (key.x < -100 or key.x > 100):
                        errors.append(f"Key {i} has extreme X coordinate: {key.x}")
                    if key.y and (key.y < -100 or key.y > 100):
                        errors.append(f"Key {i} has extreme Y coordinate: {key.y}")
                
            except KLEParseError as e:
                errors.append(f"KLE parsing failed: {e}")
            
            return errors
            
        except Exception as e:
            return [f"Validation failed: {e}"]


# Convenience functions

def convert_kle_file(
    kle_file_path: str,
    naming_strategy: Optional[PointNamingStrategy] = None,
    key_unit_size: float = 19.05,
    center_on_origin: bool = True
) -> PointsCollection:
    """
    Convenience function to convert a KLE file to Ergogen points.
    
    Args:
        kle_file_path: Path to KLE JSON file
        naming_strategy: Point naming strategy (default: MatrixNamingStrategy)
        key_unit_size: Key unit size in mm (default: 19.05)
        center_on_origin: Whether to center on origin (default: True)
        
    Returns:
        PointsCollection with converted points
    """
    converter = KLEToErgogenConverter(
        key_unit_size=key_unit_size,
        naming_strategy=naming_strategy,
        center_on_origin=center_on_origin
    )
    return converter.convert_file(kle_file_path)


def convert_kle_json(
    kle_json: str,
    naming_strategy: Optional[PointNamingStrategy] = None,
    key_unit_size: float = 19.05,
    center_on_origin: bool = True
) -> PointsCollection:
    """
    Convenience function to convert KLE JSON to Ergogen points.
    
    Args:
        kle_json: KLE JSON string
        naming_strategy: Point naming strategy (default: MatrixNamingStrategy)
        key_unit_size: Key unit size in mm (default: 19.05)
        center_on_origin: Whether to center on origin (default: True)
        
    Returns:
        PointsCollection with converted points
    """
    converter = KLEToErgogenConverter(
        key_unit_size=key_unit_size,
        naming_strategy=naming_strategy,
        center_on_origin=center_on_origin
    )
    return converter.convert_json(kle_json)
