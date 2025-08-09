"""
Ergogen YAML Generator

This module provides functionality to generate Ergogen-compatible YAML 
from converted point collections.
"""

import yaml
from typing import Dict, List, Optional, Any, Union, TextIO
from io import StringIO
import sys
import os
from pathlib import Path

# Add the parent directory to Python path to import from kle_to_ergogen
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from kle_to_ergogen.data_models.ergogen_point import PointsCollection, ErgogenPoint


class ErgogenYAMLGeneratorError(Exception):
    """Raised when YAML generation fails."""
    pass


class ErgogenYAMLGenerator:
    """
    Generator for creating Ergogen-compatible YAML from point collections.
    
    This class handles the conversion of PointsCollection objects to properly 
    formatted YAML that can be used in Ergogen PCB generation configs.
    """
    
    def __init__(
        self,
        indent: int = 2,
        sort_keys: bool = True,
        include_metadata: bool = True,
        include_comments: bool = True,
        precision: int = 3
    ):
        """
        Initialize the YAML generator.
        
        Args:
            indent: Number of spaces for YAML indentation (default: 2)
            sort_keys: Whether to sort point names alphabetically (default: True)
            include_metadata: Whether to include metadata as comments (default: True) 
            include_comments: Whether to include descriptive comments (default: True)
            precision: Decimal precision for coordinates (default: 3)
        """
        self.indent = indent
        self.sort_keys = sort_keys
        self.include_metadata = include_metadata
        self.include_comments = include_comments
        self.precision = precision
    
    def generate_yaml(self, points_collection: PointsCollection) -> str:
        """
        Generate Ergogen YAML from a points collection.
        
        Args:
            points_collection: Collection of converted points
            
        Returns:
            YAML string ready for Ergogen
            
        Raises:
            ErgogenYAMLGeneratorError: If generation fails
        """
        if not points_collection or not points_collection.points:
            raise ErgogenYAMLGeneratorError("Points collection is empty")
        
        try:
            # Convert points to dictionary format
            points_dict = self._convert_points_to_dict(points_collection)
            
            # Generate base YAML
            yaml_content = self._generate_base_yaml(points_dict, points_collection)
            
            # Add comments if requested
            if self.include_comments:
                yaml_content = self._add_comments(yaml_content, points_collection)
            
            return yaml_content
            
        except Exception as e:
            raise ErgogenYAMLGeneratorError(f"Failed to generate YAML: {e}")
    
    def generate_yaml_section(self, points_collection: PointsCollection) -> str:
        """
        Generate only the points section for embedding in existing Ergogen config.
        
        Args:
            points_collection: Collection of converted points
            
        Returns:
            YAML points section string
        """
        if not points_collection or not points_collection.points:
            raise ErgogenYAMLGeneratorError("Points collection is empty")
        
        try:
            points_dict = self._convert_points_to_dict(points_collection)
            
            # Generate just the points section
            yaml_str = yaml.dump(
                points_dict,
                default_flow_style=False,
                sort_keys=self.sort_keys,
                indent=self.indent,
                allow_unicode=True
            )
            
            return yaml_str.strip()
            
        except Exception as e:
            raise ErgogenYAMLGeneratorError(f"Failed to generate YAML section: {e}")
    
    def save_to_file(
        self, 
        points_collection: PointsCollection, 
        file_path: str,
        section_only: bool = False
    ) -> None:
        """
        Save generated YAML to a file.
        
        Args:
            points_collection: Collection of converted points
            file_path: Output file path
            section_only: If True, generate only points section (default: False)
            
        Raises:
            ErgogenYAMLGeneratorError: If saving fails
        """
        try:
            if section_only:
                yaml_content = self.generate_yaml_section(points_collection)
            else:
                yaml_content = self.generate_yaml(points_collection)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
                
        except IOError as e:
            raise ErgogenYAMLGeneratorError(f"Failed to save YAML file: {e}")
    
    def _convert_points_to_dict(self, points_collection: PointsCollection) -> Dict[str, Any]:
        """Convert points collection to dictionary with proper precision."""
        points_dict = {}
        
        for point in points_collection.points:
            point_data = point.to_ergogen_dict()
            
            # Apply precision to coordinates
            if 'x' in point_data and isinstance(point_data['x'], (int, float)):
                point_data['x'] = round(float(point_data['x']), self.precision)
            if 'y' in point_data and isinstance(point_data['y'], (int, float)):
                point_data['y'] = round(float(point_data['y']), self.precision)
            if 'r' in point_data and isinstance(point_data['r'], (int, float)):
                point_data['r'] = round(float(point_data['r']), 1)  # Rotation to 1 decimal
            
            points_dict[point.name] = point_data
        
        return points_dict
    
    def _generate_base_yaml(
        self, 
        points_dict: Dict[str, Any], 
        points_collection: PointsCollection
    ) -> str:
        """Generate the base YAML structure."""
        
        # Check if this is a regular grid or irregular layout
        if self._is_regular_grid(points_collection):
            # Use matrix structure for regular grids
            config = {
                'points': {
                    'zones': {
                        'matrix': {
                            'anchor': {
                                'shift': [0, 0]
                            },
                            'key': {
                                'width': 19.05,  # Standard key unit in mm
                                'height': 19.05,
                                'tags': ['key']
                            },
                            'rows': self._generate_rows_from_points(points_dict),
                            'columns': self._generate_columns_from_points(points_dict)
                        }
                    }
                }
            }
        else:
            # Use absolute positioning for irregular layouts
            config = {
                'points': self._generate_absolute_points(points_collection)
            }
        
        # Generate YAML
        yaml_str = yaml.dump(
            config,
            default_flow_style=False,
            sort_keys=self.sort_keys,
            indent=self.indent,
            allow_unicode=True,
            width=80
        )
        
        return yaml_str
    
    def _generate_rows_from_points(self, points_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Generate row definitions from points."""
        rows = {}
        
        # Extract unique row indices from point names (r0c0, r1c0, etc.)
        row_indices = set()
        for point_name in points_dict.keys():
            if point_name.startswith('r') and 'c' in point_name:
                row_part = point_name.split('c')[0]
                if row_part.startswith('r'):
                    try:
                        row_idx = int(row_part[1:])
                        row_indices.add(row_idx)
                    except ValueError:
                        pass
        
        # Create row definitions
        for row_idx in sorted(row_indices):
            rows[f'r{row_idx}'] = {}
        
        return rows
    
    def _generate_columns_from_points(self, points_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Generate column definitions from points."""
        columns = {}
        
        # Extract unique column indices from point names (r0c0, r0c1, etc.)
        col_indices = set()
        for point_name in points_dict.keys():
            if 'c' in point_name:
                col_part = point_name.split('c')[-1]
                try:
                    col_idx = int(col_part)
                    col_indices.add(col_idx)
                except ValueError:
                    pass
        
        # Create column definitions with individual key positions
        for col_idx in sorted(col_indices):
            col_name = f'c{col_idx}'
            columns[col_name] = {
                'rows': {}
            }
            
            # Find all points in this column and add their positions
            for point_name, point_data in points_dict.items():
                if f'c{col_idx}' in point_name and point_name.startswith('r'):
                    row_part = point_name.split('c')[0]
                    if row_part.startswith('r'):
                        try:
                            row_idx = int(row_part[1:])
                            row_name = f'r{row_idx}'
                            
                            # Add the shift for this specific key position
                            columns[col_name]['rows'][row_name] = {
                                'shift': [point_data['x'], point_data['y']]
                            }
                            
                            # Add rotation if present
                            if 'r' in point_data and point_data['r'] != 0:
                                columns[col_name]['rows'][row_name]['rotate'] = point_data['r']
                            
                        except ValueError:
                            pass
        
        return columns
    
    def _is_regular_grid(self, points_collection: PointsCollection) -> bool:
        """
        Determine if the layout is a regular grid or irregular positioning.
        
        Args:
            points_collection: Collection of points to analyze
            
        Returns:
            True if layout forms a regular grid, False for irregular layouts
        """
        if not points_collection.points or len(points_collection.points) < 4:
            return False
        
        # Check for variable key sizes (indicates irregular layout)
        for point in points_collection.points:
            if point.kle_width != 1.0 or point.kle_height != 1.0:
                return False
            # Check for rotation
            if abs(point.rotation) > 0.1:
                return False
        
        # Get all X and Y coordinates
        x_coords = [point.x for point in points_collection.points]
        y_coords = [point.y for point in points_collection.points]
        
        # Sort and find unique coordinates
        unique_x = sorted(set(round(x, 1) for x in x_coords))
        unique_y = sorted(set(round(y, 1) for y in y_coords))
        
        # Check if coordinates form regular intervals
        if len(unique_x) < 2 or len(unique_y) < 2:
            return len(points_collection.points) <= 3  # Small layouts might be regular
        
        # Calculate intervals between consecutive coordinates
        x_intervals = [unique_x[i+1] - unique_x[i] for i in range(len(unique_x)-1)]
        y_intervals = [unique_y[i+1] - unique_y[i] for i in range(len(unique_y)-1)]
        
        # Check if intervals are consistent (allowing small tolerance)
        tolerance = 0.5
        x_regular = len(set(round(interval, 1) for interval in x_intervals)) <= 2
        y_regular = len(set(round(interval, 1) for interval in y_intervals)) <= 2
        
        return x_regular and y_regular
    
    def _generate_absolute_points(self, points_collection: PointsCollection) -> Dict[str, Any]:
        """
        Generate absolute positioned points for irregular layouts.
        
        Args:
            points_collection: Collection of points
            
        Returns:
            Dictionary with absolute point definitions
        """
        points_dict = {}
        
        for point in points_collection.points:
            point_config = {
                'shift': [
                    round(point.x, self.precision),
                    round(point.y, self.precision)
                ]
            }
            
            # Add rotation if present
            if abs(point.rotation) > 0.1:
                point_config['rotate'] = round(point.rotation, 1)
            
            # Create key configuration
            key_config = {
                'width': 19.05,
                'height': 19.05,
                'tags': ['key']
            }
            
            # Override dimensions for non-standard keys
            if point.kle_width != 1.0:
                key_config['width'] = round(point.kle_width * 19.05, self.precision)
            if point.kle_height != 1.0:
                key_config['height'] = round(point.kle_height * 19.05, self.precision)
            
            # Add additional tags if present
            if point.tags:
                key_config['tags'].extend(point.tags)
            
            point_config['key'] = key_config
            points_dict[point.name] = point_config
        
        return points_dict
    
    def _add_comments(
        self, 
        yaml_content: str, 
        points_collection: PointsCollection
    ) -> str:
        """Add descriptive comments to the YAML."""
        lines = yaml_content.split('\n')
        commented_lines = []
        
        # Add header comment
        header_comment = self._generate_header_comment(points_collection)
        commented_lines.extend(header_comment)
        
        # Process each line
        for line in lines:
            if line.strip().startswith('points:'):
                # Add comment before points section
                commented_lines.append('# Key switch positions for PCB generation')
                commented_lines.append(line)
            elif ':' in line and not line.strip().startswith('#'):
                # Check if this is a point definition
                point_name = line.split(':')[0].strip()
                if point_name in [p.name for p in points_collection.points]:
                    # Find the corresponding point
                    point = next((p for p in points_collection.points if p.name == point_name), None)
                    if point:
                        comment = self._generate_point_comment(point)
                        if comment:
                            commented_lines.append(f"  # {comment}")
                commented_lines.append(line)
            else:
                commented_lines.append(line)
        
        return '\n'.join(commented_lines)
    
    def _generate_header_comment(self, points_collection: PointsCollection) -> List[str]:
        """Generate header comment with conversion info."""
        comments = [
            "# Generated by KLE to Ergogen Converter",
            "# https://github.com/rossw42/qmk_utilities",
            "#"
        ]
        
        if points_collection.metadata:
            metadata = points_collection.metadata
            if 'layout_name' in metadata:
                comments.append(f"# Layout: {metadata['layout_name']}")
            if 'total_keys' in metadata:
                comments.append(f"# Total keys: {metadata['total_keys']}")
            if 'key_unit_size' in metadata:
                comments.append(f"# Key unit size: {metadata['key_unit_size']}mm")
            comments.append("#")
        
        # Add usage instructions
        comments.extend([
            "# Usage: Copy the 'points:' section into your Ergogen config",
            "# or use this file as a starting point for your PCB design.",
            "#",
            ""
        ])
        
        return comments
    
    def _generate_point_comment(self, point: ErgogenPoint) -> Optional[str]:
        """Generate a descriptive comment for a point."""
        comments_parts = []
        
        # Add KLE information if available
        if point.kle_label:
            comments_parts.append(f"Key: {point.kle_label}")
        
        # Add matrix position
        if point.kle_row is not None and point.kle_col is not None:
            comments_parts.append(f"Matrix: R{point.kle_row}C{point.kle_col}")
        
        # Add special properties
        if point.kle_width != 1.0:
            comments_parts.append(f"{point.kle_width}u wide")
        if point.kle_height != 1.0:
            comments_parts.append(f"{point.kle_height}u tall")
        if abs(point.rotation) > 0.1:
            comments_parts.append(f"rotated {point.rotation}°")
        
        return " | ".join(comments_parts) if comments_parts else None
    
    def validate_yaml(self, yaml_content: str) -> List[str]:
        """
        Validate generated YAML for syntax errors.
        
        Args:
            yaml_content: YAML content to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        try:
            # Parse YAML to check syntax
            parsed = yaml.safe_load(yaml_content)
            
            # Check structure
            if not isinstance(parsed, dict):
                errors.append("YAML root must be a dictionary")
                return errors
            
            if 'points' not in parsed:
                errors.append("YAML must contain 'points' section")
                return errors
            
            points = parsed['points']
            if not isinstance(points, dict):
                errors.append("Points section must be a dictionary")
                return errors
            
            # Validate each point
            for point_name, point_data in points.items():
                if not isinstance(point_data, dict):
                    errors.append(f"Point '{point_name}' must be a dictionary")
                    continue
                
                # Check required fields
                if 'x' not in point_data or 'y' not in point_data:
                    errors.append(f"Point '{point_name}' missing x or y coordinate")
                
                # Validate coordinate types
                for coord in ['x', 'y', 'r']:
                    if coord in point_data:
                        if not isinstance(point_data[coord], (int, float)):
                            errors.append(f"Point '{point_name}' {coord} coordinate must be numeric")
            
        except yaml.YAMLError as e:
            errors.append(f"YAML syntax error: {e}")
        except Exception as e:
            errors.append(f"Validation error: {e}")
        
        return errors
    
    def get_generation_stats(self, points_collection: PointsCollection) -> Dict[str, Any]:
        """
        Get statistics about the generated YAML.
        
        Args:
            points_collection: Points collection
            
        Returns:
            Dictionary with generation statistics
        """
        if not points_collection or not points_collection.points:
            return {'total_points': 0}
        
        # Generate YAML to get size
        yaml_content = self.generate_yaml(points_collection)
        yaml_section = self.generate_yaml_section(points_collection)
        
        # Count special features
        rotated_points = sum(1 for p in points_collection.points if abs(p.rotation) > 0.1)
        tagged_points = sum(1 for p in points_collection.points if p.tags)
        
        return {
            'total_points': len(points_collection.points),
            'rotated_points': rotated_points,
            'tagged_points': tagged_points,
            'full_yaml_size': len(yaml_content),
            'section_only_size': len(yaml_section),
            'settings': {
                'indent': self.indent,
                'sort_keys': self.sort_keys,
                'include_metadata': self.include_metadata,
                'include_comments': self.include_comments,
                'precision': self.precision
            }
        }


# Convenience functions

def generate_ergogen_yaml(
    points_collection: PointsCollection,
    indent: int = 2,
    sort_keys: bool = True,
    include_comments: bool = True
) -> str:
    """
    Convenience function to generate Ergogen YAML from points collection.
    
    Args:
        points_collection: Collection of converted points
        indent: YAML indentation (default: 2)
        sort_keys: Whether to sort point names (default: True)
        include_comments: Whether to include comments (default: True)
        
    Returns:
        Formatted YAML string
    """
    generator = ErgogenYAMLGenerator(
        indent=indent,
        sort_keys=sort_keys,
        include_comments=include_comments
    )
    return generator.generate_yaml(points_collection)


def save_ergogen_yaml(
    points_collection: PointsCollection,
    file_path: str,
    section_only: bool = False,
    **kwargs
) -> None:
    """
    Convenience function to save Ergogen YAML to file.
    
    Args:
        points_collection: Collection of converted points
        file_path: Output file path
        section_only: Generate only points section (default: False)
        **kwargs: Additional generator options
    """
    generator = ErgogenYAMLGenerator(**kwargs)
    generator.save_to_file(points_collection, file_path, section_only)
