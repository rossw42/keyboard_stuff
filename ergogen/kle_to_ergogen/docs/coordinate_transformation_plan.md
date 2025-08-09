# Coordinate Transformation Pipeline

## Overview

This document outlines the coordinate transformation pipeline for converting KLE (Keyboard Layout Editor) layouts to Ergogen points format.

## Coordinate Systems

### KLE Coordinate System
- **Units**: Key units (1.0u = standard key width/height)
- **Origin**: Top-left of layout (0,0)
- **X-axis**: Rightward (positive)
- **Y-axis**: Downward (positive)
- **Rotation**: Degrees, clockwise positive
- **Key positioning**: Each key has x,y position, width, height, rotation

### Ergogen Coordinate System  
- **Units**: Millimeters (mm)
- **Origin**: Typically center of layout (0,0)
- **X-axis**: Rightward (positive)
- **Y-axis**: Upward (positive) - **NOTE: Inverted from KLE**
- **Rotation**: Degrees, counter-clockwise positive
- **Key positioning**: Points with x,y coordinates and rotation

## Transformation Pipeline

### Stage 1: Parse KLE Data
Using the existing `KLEParser` from `qmk_format_converter`:
- Extract key positions (x, y)
- Extract key dimensions (width, height)  
- Extract rotation data (rotation_angle, rotation_x, rotation_y)
- Extract matrix positions (matrix_row, matrix_col)
- Extract labels for naming

### Stage 2: Unit Conversion
Convert from KLE key units to millimeters:
```python
# Standard Cherry MX key unit size
KEY_UNIT_MM = 19.05  # mm per key unit

def kle_units_to_mm(kle_units: float) -> float:
    return kle_units * KEY_UNIT_MM
```

### Stage 3: Coordinate System Transformation
Transform coordinate system from KLE to Ergogen:

1. **Unit conversion**: x_mm = x_kle * 19.05, y_mm = y_kle * 19.05
2. **Y-axis inversion**: y_ergogen = -y_mm (flip vertical axis)
3. **Rotation conversion**: Keep rotation as-is (both use degrees)

### Stage 4: Origin Centering (Optional)
Center the layout on origin (0,0):
1. Calculate bounding box of all points
2. Find center point: `center_x = (min_x + max_x) / 2`
3. Translate all points: `point.x -= center_x`

### Stage 5: Point Naming
Apply chosen naming strategy:
- **Matrix**: `r{row}c{col}` (default)
- **Sequential**: `key_{index}`
- **Label-based**: Use KLE labels when valid

## Coordinate Transformation Class

```python
class KLEToErgogenTransformer:
    """Transforms KLE coordinates to Ergogen format."""
    
    def __init__(self, key_unit_size: float = 19.05):
        self.key_unit_size = key_unit_size
    
    def transform_key(self, kle_key: KeyDefinition, naming_strategy: PointNamingStrategy) -> ErgogenPoint:
        """Transform single KLE key to Ergogen point."""
        # Convert units
        x_mm = kle_key.x * self.key_unit_size
        y_mm = kle_key.y * self.key_unit_size
        
        # Invert Y-axis
        y_ergogen = -y_mm
        
        # Generate name
        name = naming_strategy.generate_name(
            row=kle_key.matrix_row or 0,
            col=kle_key.matrix_col or 0, 
            index=0,  # Will be set during conversion
            label=kle_key.primary_label
        )
        
        return ErgogenPoint(
            name=name,
            x=x_mm,
            y=y_ergogen,
            rotation=kle_key.rotation_angle or 0.0,
            kle_row=kle_key.matrix_row,
            kle_col=kle_key.matrix_col,
            kle_width=kle_key.width or 1.0,
            kle_height=kle_key.height or 1.0,
            kle_label=kle_key.primary_label
        )
```

## Handling Complex Cases

### Rotated Keys
KLE keys with rotation have:
- `rotation_angle`: Rotation in degrees
- `rotation_x`, `rotation_y`: Rotation center point

Ergogen points will store:
- Individual point rotation
- Position already calculated relative to rotation center

### Multi-unit Keys
KLE keys can have width/height > 1.0:
- For Ergogen: Generate single point at key center
- Store original width/height in metadata for reference

### Split Keyboards  
For split layouts:
- Left/right halves may need separate coordinate systems
- Consider adding tags to distinguish sides
- May need manual offset adjustment

## Validation Pipeline

### Coordinate Validation
1. **Bounds checking**: Ensure reasonable coordinate ranges
2. **Overlap detection**: Check for points too close together (< 0.1mm)
3. **Rotation validation**: Normalize to 0-360° range

### Quality Checks
1. **Grid alignment**: Warn if points don't align to common grid
2. **Spacing validation**: Check for unusual key spacing
3. **Layout symmetry**: Detect and validate symmetric layouts

## Usage Example

```python
# Parse KLE file
kle_layout = KLEParser().parse_file("layout.json")

# Transform to Ergogen points
transformer = KLEToErgogenTransformer()
naming_strategy = MatrixNamingStrategy()

points_collection = PointsCollection(naming_strategy=naming_strategy)

for i, key in enumerate(kle_layout.keys):
    point = transformer.transform_key(key, naming_strategy) 
    points_collection.add_point(point)

# Center on origin
centered_points = points_collection.center_on_origin()

# Validate
errors = centered_points.validate()
if errors:
    print("Validation errors:", errors)

# Export to Ergogen format
ergogen_dict = centered_points.to_ergogen_dict()
```

## Configuration Options

### Transform Settings
- `key_unit_size`: Size of one key unit in mm (default: 19.05)
- `invert_y_axis`: Whether to flip Y-axis (default: True)
- `center_on_origin`: Whether to center layout (default: True)
- `naming_strategy`: Point naming approach (default: Matrix)

### Validation Settings  
- `overlap_tolerance`: Minimum distance between points (default: 0.1mm)
- `check_grid_alignment`: Validate grid alignment (default: True)
- `warn_unusual_spacing`: Flag non-standard spacing (default: True)

## Error Handling

### Invalid Input
- **Missing coordinates**: Fail with clear error message
- **Invalid KLE format**: Pass through KLEParser validation
- **Malformed keys**: Skip with warning, continue processing

### Coordinate Issues
- **Extreme values**: Warn about coordinates outside reasonable ranges
- **Overlapping points**: Error on duplicate positions
- **Invalid rotations**: Normalize or warn about unusual angles

## Performance Considerations

- **Linear complexity**: O(n) transformation for n keys
- **Memory usage**: Minimal additional memory beyond input/output
- **Validation cost**: O(n²) for overlap detection on large layouts
- **Optimization**: Consider spatial indexing for large layouts (100+ keys)

## Future Enhancements

1. **Advanced rotation handling**: Better support for complex rotation scenarios
2. **Layout templates**: Pre-defined transformations for common layouts
3. **Interactive adjustment**: Tools for fine-tuning coordinate output
4. **Multi-format input**: Support for other layout formats beyond KLE
5. **Ergogen integration**: Direct validation against Ergogen parser
