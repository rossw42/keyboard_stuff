# Mathematical Column Height Equalization Guide

## Overview
This document explains the mathematical approaches developed for equalizing column heights in keyboard layouts, specifically designed for auto-generation systems.

## Problem Statement
In keyboard designs, columns have different natural heights due to:
- Different numbers of keys per column (some rows skipped)
- Varying row configurations 
- Ergonomic stagger requirements

The goal is to mathematically calculate stagger values so all columns reach the same maximum height envelope.

## Mathematical Solutions Developed

### Method 1: Boundary Alignment (forestv1.2.yaml)
**Concept**: Define target boundaries and align all columns to them.

**Variables**:
```yaml
TopBoundary: 2U           # Target top boundary
BottomBoundary: -2U       # Target bottom boundary  
TargetHeight: TopBoundary - BottomBoundary
```

**Formulas**:
- **Top Alignment**: `stagger = TopBoundary - (natural_center + natural_height/2)`
- **Bottom Alignment**: `stagger = BottomBoundary + (natural_height/2) - natural_center`
- **Center Alignment**: `stagger = CenterAlign - natural_center`

**Use Case**: When you want all columns to fit within specific boundaries.

### Method 2: Parametric Height Matching (forestv1.3_advanced_math.yaml)
**Concept**: Analyze each column's configuration and calculate precise staggers for height equalization.

**Step-by-Step Process**:

1. **Analyze Column Configuration**:
```yaml
Col1_KeyCount: 3          # Count actual keys (exclude skipped rows)
Col2_KeyCount: 4          
# ... for each column
```

2. **Calculate Natural Heights**:
```yaml
Col1_NaturalHeight: (Col1_KeyCount - 1) * RowSpacing  # 38mm
Col2_NaturalHeight: (Col2_KeyCount - 1) * RowSpacing  # 57mm
```

3. **Find Maximum Height**:
```yaml
MaxHeight: Col2_NaturalHeight  # Use tallest column as target
```

4. **Calculate Natural Centers**:
```yaml
Col1_NaturalCenter: RowSpacing * 2      # Based on row distribution
Col2_NaturalCenter: RowSpacing * 1.5    # Centered between rows
```

5. **Compute Alignment Staggers**:
```yaml
# Strategy A: Top Alignment
Col1_TopAlignStagger: TargetTop - (Col1_NaturalCenter + Col1_NaturalHeight/2)

# Strategy B: Bottom Alignment  
Col1_BottomAlignStagger: TargetBottom - (Col1_NaturalCenter - Col1_NaturalHeight/2)

# Strategy C: Center Alignment
Col1_HeightEqualStagger: TargetCenter - Col1_NaturalCenter
```

### Method 3: Ergonomic Curve Enhancement
**Concept**: Add subtle ergonomic curves while maintaining height consistency.

```yaml
CurveAmplitude: 3         # Maximum deviation (3mm)
Col1_CurveOffset: CurveAmplitude * sin(0.5)     # ~1.5mm
Col2_CurveOffset: CurveAmplitude * sin(1.0)     # ~2.5mm
# Final stagger = base_stagger + curve_offset
```

## Auto-Generation Algorithm

### Input Parameters
```yaml
# Configuration
row_spacing: 19           # mm between rows
column_spacing: 23        # mm between columns
alignment_strategy: "top" # "top", "bottom", "center"
curve_amplitude: 0        # 0 = no curve, >0 = ergonomic curve

# Column definitions
columns:
  - name: "col_one"
    rows: [1, 2, 3]       # Which rows have keys
  - name: "col_two"  
    rows: [0, 1, 2, 3]    # Full height column
  # ... more columns
```

### Algorithm Steps

1. **Parse Column Configurations**:
```python
for each column:
    key_count = len(column.rows)
    natural_height = (key_count - 1) * row_spacing
    natural_center = calculate_center_position(column.rows, row_spacing)
```

2. **Find Target Height**:
```python
max_height = max(all_natural_heights)
target_top = define_target_boundary()
```

3. **Calculate Staggers**:
```python
for each column:
    if alignment_strategy == "top":
        stagger = target_top - (natural_center + natural_height/2)
    elif alignment_strategy == "bottom":
        stagger = target_bottom - (natural_center - natural_height/2)
    elif alignment_strategy == "center":
        stagger = target_center - natural_center
```

4. **Apply Ergonomic Curve** (Optional):
```python
for i, column in enumerate(columns):
    curve_offset = curve_amplitude * sin(i * phase_multiplier)
    final_stagger = base_stagger + curve_offset
```

## Practical Implementation

### Example: 6-Column Layout
Given columns with key counts: [3, 4, 4, 4, 3, 3]

1. **Natural heights**: [38mm, 57mm, 57mm, 57mm, 38mm, 38mm]
2. **Maximum height**: 57mm
3. **Target alignment**: Top alignment at Y=57mm
4. **Required staggers**: [9.5mm, 0mm, 0mm, 0mm, 9.5mm, 9.5mm]

### Variable Definitions for Ergogen
```yaml
units:
  # Analysis variables
  Col1_KeyCount: 3
  Col1_NaturalHeight: (Col1_KeyCount - 1) * RowSpacing
  Col1_NaturalCenter: RowSpacing * 2
  
  # Target alignment
  TargetTop: RowSpacing * 3
  Col1_TopAlignStagger: TargetTop - (Col1_NaturalCenter + Col1_NaturalHeight/2)
  
# Use in column definition  
columns:
  col_one:
    key:
      stagger: Col1_TopAlignStagger
```

## Advantages of Mathematical Approach

1. **Consistency**: All columns reach exactly the same height
2. **Parametric**: Easy to adjust for different layouts
3. **Automated**: Can be programmatically generated
4. **Flexible**: Supports multiple alignment strategies
5. **Ergonomic**: Can integrate natural finger curves
6. **Precise**: Uses exact calculations rather than trial-and-error

## Files Reference

- **forestv1.2.yaml**: Basic mathematical approaches with multiple methods
- **forestv1.3_advanced_math.yaml**: Complete parametric system with all formulas
- **forestv1.1.yaml**: Original design with manual stagger adjustments

## Next Steps for Auto-Generation

1. Implement parsing logic to analyze any column configuration
2. Create algorithm to automatically detect natural heights and centers
3. Build parameter system for different alignment strategies
4. Add ergonomic curve options with adjustable parameters  
5. Generate complete stagger calculations programmatically
6. Validate results with visual guides and mathematical analysis

This mathematical framework provides the foundation for automated keyboard layout generation with consistent column height matching.
