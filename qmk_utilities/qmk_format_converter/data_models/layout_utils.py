"""
Layout Utilities

This module provides utility functions for working with the universal layout data model.
"""

from typing import List, Dict, Tuple, Optional
from .universal_layout import UniversalLayout, KeyDefinition, LayerDefinition
from .keycode_mappings import KEYCODE_MAPPER


class LayoutValidator:
    """Validates universal layout data for consistency and completeness."""
    
    @staticmethod
    def validate_layout(layout: UniversalLayout) -> List[str]:
        """Comprehensive validation of a universal layout."""
        errors = []
        
        # Basic validation
        errors.extend(layout.validate())
        
        # Additional validations
        errors.extend(LayoutValidator._validate_key_positions(layout.keys))
        errors.extend(LayoutValidator._validate_layer_consistency(layout.layers, len(layout.keys)))
        errors.extend(LayoutValidator._validate_matrix_mapping(layout.keys, layout.matrix_rows, layout.matrix_cols))
        errors.extend(LayoutValidator._validate_keycodes(layout.layers))
        
        return errors
    
    @staticmethod
    def _validate_key_positions(keys: List[KeyDefinition]) -> List[str]:
        """Validate key physical positions for overlaps."""
        errors = []
        
        for i, key1 in enumerate(keys):
            for j, key2 in enumerate(keys[i+1:], i+1):
                if LayoutValidator._keys_overlap(key1, key2):
                    errors.append(f"Keys {i} and {j} overlap in physical position")
        
        return errors
    
    @staticmethod
    def _keys_overlap(key1: KeyDefinition, key2: KeyDefinition) -> bool:
        """Check if two keys overlap physically."""
        # Simple bounding box overlap check
        key1_right = key1.x + key1.width
        key1_bottom = key1.y + key1.height
        key2_right = key2.x + key2.width
        key2_bottom = key2.y + key2.height
        
        return not (key1.x >= key2_right or key2.x >= key1_right or
                   key1.y >= key2_bottom or key2.y >= key1_bottom)
    
    @staticmethod
    def _validate_layer_consistency(layers: List[LayerDefinition], key_count: int) -> List[str]:
        """Validate layer data consistency."""
        errors = []
        
        for layer in layers:
            if len(layer.keycodes) != key_count:
                errors.append(f"Layer '{layer.name}': keycode count ({len(layer.keycodes)}) "
                            f"doesn't match key count ({key_count})")
        
        return errors
    
    @staticmethod
    def _validate_matrix_mapping(keys: List[KeyDefinition], matrix_rows: int, matrix_cols: int) -> List[str]:
        """Validate matrix position mappings."""
        errors = []
        
        for i, key in enumerate(keys):
            if key.matrix_row is not None and key.matrix_col is not None:
                if key.matrix_row >= matrix_rows:
                    errors.append(f"Key {i}: matrix row {key.matrix_row} >= matrix_rows {matrix_rows}")
                if key.matrix_col >= matrix_cols:
                    errors.append(f"Key {i}: matrix col {key.matrix_col} >= matrix_cols {matrix_cols}")
        
        return errors
    
    @staticmethod
    def _validate_keycodes(layers: List[LayerDefinition]) -> List[str]:
        """Validate keycode format."""
        errors = []
        
        for layer in layers:
            for i, keycode in enumerate(layer.keycodes):
                if not keycode:
                    errors.append(f"Layer '{layer.name}', position {i}: empty keycode")
                elif not KEYCODE_MAPPER.is_valid_qmk_keycode(keycode) and not keycode.startswith(('MO(', 'LT(', 'TG(')):
                    # Allow layer switching functions even if not in basic mapping
                    errors.append(f"Layer '{layer.name}', position {i}: invalid keycode '{keycode}'")
        
        return errors


class LayoutCalculator:
    """Performs calculations on layout data."""
    
    @staticmethod
    def calculate_layout_bounds(keys: List[KeyDefinition]) -> Tuple[float, float, float, float]:
        """Calculate the bounding box of all keys."""
        if not keys:
            return (0, 0, 0, 0)
        
        min_x = min(key.x for key in keys)
        min_y = min(key.y for key in keys)
        max_x = max(key.x + key.width for key in keys)
        max_y = max(key.y + key.height for key in keys)
        
        return (min_x, min_y, max_x, max_y)
    
    @staticmethod
    def calculate_layout_size(keys: List[KeyDefinition]) -> Tuple[float, float]:
        """Calculate the total width and height of the layout."""
        min_x, min_y, max_x, max_y = LayoutCalculator.calculate_layout_bounds(keys)
        return (max_x - min_x, max_y - min_y)
    
    @staticmethod
    def calculate_key_center(key: KeyDefinition) -> Tuple[float, float]:
        """Calculate the center point of a key."""
        return (key.x + key.width / 2, key.y + key.height / 2)
    
    @staticmethod
    def find_optimal_matrix_size(keys: List[KeyDefinition]) -> Tuple[int, int]:
        """Find optimal matrix dimensions based on key positions."""
        if not keys:
            return (1, 1)
        
        # Count unique row and column positions
        rows = set()
        cols = set()
        
        for key in keys:
            if key.matrix_row is not None:
                rows.add(key.matrix_row)
            if key.matrix_col is not None:
                cols.add(key.matrix_col)
        
        if rows and cols:
            return (max(rows) + 1, max(cols) + 1)
        
        # Fallback: estimate based on physical layout
        width, height = LayoutCalculator.calculate_layout_size(keys)
        estimated_cols = max(1, int(width + 0.5))  # Round to nearest integer
        estimated_rows = max(1, int(height + 0.5))
        
        return (estimated_rows, estimated_cols)


class LayoutTransformer:
    """Transforms layout data for different purposes."""
    
    @staticmethod
    def normalize_positions(keys: List[KeyDefinition]) -> None:
        """Normalize key positions to start from (0, 0)."""
        if not keys:
            return
        
        min_x, min_y, _, _ = LayoutCalculator.calculate_layout_bounds(keys)
        
        for key in keys:
            key.x -= min_x
            key.y -= min_y
    
    @staticmethod
    def scale_layout(keys: List[KeyDefinition], scale_factor: float) -> None:
        """Scale the entire layout by a factor."""
        for key in keys:
            key.x *= scale_factor
            key.y *= scale_factor
            key.width *= scale_factor
            key.height *= scale_factor
    
    @staticmethod
    def auto_assign_matrix_positions(keys: List[KeyDefinition]) -> None:
        """Automatically assign matrix positions based on physical layout."""
        # Sort keys by row (Y position) then column (X position)
        sorted_keys = sorted(enumerate(keys), 
                           key=lambda item: (round(item[1].y * 2), round(item[1].x * 2)))
        
        current_row = 0
        current_col = 0
        last_y = None
        
        for original_index, key in sorted_keys:
            # Start new row if Y position changed significantly
            if last_y is not None and abs(key.y - last_y) > 0.5:
                current_row += 1
                current_col = 0
            
            key.matrix_row = current_row
            key.matrix_col = current_col
            
            current_col += 1
            last_y = key.y
    
    @staticmethod
    def generate_layout_variants(layout: UniversalLayout) -> Dict[str, UniversalLayout]:
        """Generate common layout variants (ANSI, ISO, etc.)."""
        variants = {}
        
        # For now, just return the original
        # In a full implementation, this would generate actual variants
        variants["original"] = layout
        
        return variants


class LayoutAnalyzer:
    """Analyzes layout characteristics and provides insights."""
    
    @staticmethod
    def analyze_layout(layout: UniversalLayout) -> Dict[str, any]:
        """Comprehensive analysis of a layout."""
        analysis = {
            "summary": layout.summary(),
            "physical": LayoutAnalyzer._analyze_physical_layout(layout.keys),
            "logical": LayoutAnalyzer._analyze_logical_layout(layout.layers),
            "compatibility": LayoutAnalyzer._analyze_format_compatibility(layout)
        }
        
        return analysis
    
    @staticmethod
    def _analyze_physical_layout(keys: List[KeyDefinition]) -> Dict[str, any]:
        """Analyze physical layout characteristics."""
        if not keys:
            return {"error": "No keys in layout"}
        
        width, height = LayoutCalculator.calculate_layout_size(keys)
        total_area = sum(key.width * key.height for key in keys)
        
        # Count key sizes
        size_counts = {}
        for key in keys:
            size = f"{key.width}x{key.height}"
            size_counts[size] = size_counts.get(size, 0) + 1
        
        return {
            "total_keys": len(keys),
            "layout_size": {"width": width, "height": height},
            "total_key_area": total_area,
            "key_size_distribution": size_counts,
            "has_rotated_keys": any(key.rotation_angle != 0 for key in keys)
        }
    
    @staticmethod
    def _analyze_logical_layout(layers: List[LayerDefinition]) -> Dict[str, any]:
        """Analyze logical layout characteristics."""
        if not layers:
            return {"error": "No layers in layout"}
        
        # Count keycode categories across all layers
        category_counts = {}
        all_keycodes = set()
        
        for layer in layers:
            for keycode in layer.keycodes:
                all_keycodes.add(keycode)
                mapping = KEYCODE_MAPPER.get_mapping(keycode)
                if mapping:
                    category = mapping.category
                    category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "layer_count": len(layers),
            "unique_keycodes": len(all_keycodes),
            "keycode_categories": category_counts,
            "has_layer_switching": any("MO(" in keycode or "LT(" in keycode 
                                     for layer in layers for keycode in layer.keycodes)
        }
    
    @staticmethod
    def _analyze_format_compatibility(layout: UniversalLayout) -> Dict[str, any]:
        """Analyze compatibility with different formats."""
        compatibility = {
            "kle": True,  # Universal format should support KLE
            "via": bool(layout.vendor_id and layout.product_id),
            "qmk": bool(layout.layout_name and layout.matrix_rows and layout.matrix_cols)
        }
        
        # Check for format-specific issues
        issues = []
        
        if not layout.keys:
            issues.append("No keys defined")
        
        if not layout.layers:
            issues.append("No layers defined")
        
        # Check matrix positions for VIA compatibility
        if compatibility["via"]:
            missing_matrix = sum(1 for key in layout.keys 
                               if key.matrix_row is None or key.matrix_col is None)
            if missing_matrix > 0:
                issues.append(f"{missing_matrix} keys missing matrix positions (VIA compatibility)")
        
        compatibility["issues"] = issues
        
        return compatibility
