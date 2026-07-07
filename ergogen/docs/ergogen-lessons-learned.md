# Ergogen Keyboard Design Lessons Learned from ForestV1.yaml

*A comprehensive guide to the design patterns and concepts that make ergogen keyboard configurations work effectively*

## Overview

After analyzing the successful forestv1.yaml configuration, several critical design patterns and concepts emerge that are essential for creating functional ergogen keyboard layouts. This document captures these lessons to guide future keyboard designs.

## Critical Success Factors

### 1. Multi-Zone Layout Strategies - THE FOUNDATION

**The Reality:** Most functional keyboards have multiple zones (matrix + thumbs) that require explicit connection strategies, not just single-zone binding.

**Key Patterns from Successful Designs:**

**Zone Positioning Strategy:**
```yaml
points:
  zones:
    matrix:
      anchor.shift: [50, -100]  # Position for KiCad sheet
      # ... matrix definition
    
    thumbs:
      anchor:
        ref: matrix_index_bottom    # Position relative to matrix key
        shift: [0.5kx, -1.25ky]   # Calculated offset
      # ... thumb definition
```

**Zone Connection Strategies:**
```yaml
outlines:
  # Method 1: Glue polygons (Absolem, Samoklava)
  thumbfan_glue:
    - what: polygon
      points:
        - ref: matrix_inner_bottom
          shift: [0.5kx, -0.5ky]
        - ref: thumbfan_far_thumb
          shift: [0.5kx, 0.5ky]
        # ... more connection points

  # Method 2: Combined sections (Tempest)
  key_section: [raw, thumb_outline]
  
  # Method 3: Additive operations (Corney-island)
  base_outline:
    - "keywell"
    - "+controller_area"
```

**Why Multi-Zone Thinking is Critical:**
- Single-zone binding only works for simple rectangular layouts
- Real keyboards need explicit strategies to connect disparate zones
- Connection polygons must be calculated carefully to avoid gaps
- Each zone may need different outline generation approaches

### 2. Outline Generation Strategy Selection

**Choose the Right Approach for Your Shape Complexity:**

**Simple Rectangular Layouts - Use Binding:**
```yaml
outlines:
  plate:
    - what: rectangle
      where: true
      bound: true    # Uses binding system
      size: [kx, ky]
```

**Complex Organic Shapes - Use Polygons:**
```yaml
outlines:
  board:
    - what: polygon
      points:
        - ref: matrix_outer_top
          shift: [-0.5px, 0.5py]
        - ref: matrix_inner_top
          shift: [0.5px, 0.5py]
        # ... many carefully calculated points
      fillet: 2
```

**Hybrid Approach - Combine Both:**
```yaml
outlines:
  keywell:
    - what: rectangle
      where: true
      bound: true    # Binding for main area
      
  base_outline:
    - "keywell"
    - "+thumb_connection_polygon"  # Manual polygon for complex connection
```

**Selection Criteria:**
- **Binding:** Good for rectangular layouts, consistent spacing
- **Polygons:** Required for organic shapes, precise control
- **Hybrid:** Best for most real keyboards with mixed complexity

### 3. Helper Points and Aggregate Positioning

**Pattern for Complex Calculations:**
```yaml
points:
  zones:
    # Helper points for outline calculations
    plate_outline_bottom_1:
      key.tags: [helper]
      anchor:
        ref: matrix_ring_bottom
        shift: [kx * 0.465, -ky * 0.74]
    
    # Aggregate positioning for intersection points
    mcu_cover_bottom_left:
      key.tags: [helper]
      anchor:
        aggregate:
          method: intersect
          parts:
            - ref: mcu_cover_top_left
            - ref: mcu_cover_bottom_right
```

**Benefits:**
- Simplifies complex outline calculations
- Makes polygon points more maintainable
- Enables parametric relationships between elements
- Reduces manual coordinate calculations

### 4. The Binding System - FOR SIMPLE RECTANGULAR LAYOUTS

**What it is:**
- The `bind: [left, right, top, bottom]` parameter on keys controls how they connect to adjacent keys
- This creates a contiguous plate outline instead of individual disconnected rectangles
- Without proper binding, you get individual key cutouts instead of a unified plate

**How it works:**
```yaml
key:
  bind: [B, B, B, B]  # Default: connect on all sides with distance B
```

**Critical binding patterns:**
- **Default binding:** `bind: [B, B, B, B]` - connects keys with binding distance B
- **Edge keys:** `bind: [0, B, B, B]` - no binding on left edge (pinky outer)
- **No binding above:** `bind: [0, B, B, B]` - for top row keys
- **No binding below:** `bind: [B, B, 0, B]` - for bottom edge keys
- **Custom spacing:** `bind: [B, B+21+3, B, B]` - extra space for MCU area

**Why it's critical:**
- Creates the fundamental `plate` outline that all other components depend on
- Enables proper case_top, case_wall, and case_lip generation
- Without it, you get individual rectangles that can't form a cohesive case

### 2. Simplified Unit System

**Proven approach:**
```yaml
units:
  X: 0.9    # Extrusion width (3D printing consideration)
  B: 3*X    # Binding distance (consistent spacing)
```

**Why this works:**
- `X` represents the extrusion width for 3D printing tolerances
- `B` provides consistent binding distances
- Simple relationship (`B = 3*X`) makes calculations predictable
- Avoids complex unit hierarchies that can cause errors

**Avoid:**
- Complex nested unit definitions
- Too many interdependent variables
- Custom units without clear relationships

### 3. Outline Hierarchy Pattern

**The winning formula:**
1. **`plate`** - Contiguous outline from binding system (`bound: true`)
2. **`case_top`** - Plate minus switch holes (for switch mounting)
3. **`case_wall`** - Plate minus large inner area (creates walls)  
4. **`case_lip`** - Plate minus small inner area (creates lid lip)

```yaml
outlines:
  plate:
    - what: rectangle
      where: true
      bound: true        # Critical: creates contiguous outline
      size: 1U
      corner: 0.5

  case_top:
    - what: outline
      name: plate
    - what: outline
      name: _switch_holes
      operation: subtract

  case_wall:
    - what: outline  
      name: plate
    - what: outline
      name: _plate_inner_3    # Larger inner cutout
      operation: subtract

  case_lip:
    - what: outline
      name: plate  
    - what: outline
      name: _plate_inner_2    # Smaller inner cutout
      operation: subtract
```

**Why this structure works:**
- Builds complexity incrementally from simple base (plate)
- Each component has a clear, single purpose
- Enables proper 3D case construction
- Maintains consistent relationships between components

### 4. MCU Integration Strategy

**Key insight:** MCU space must be planned into the binding system, not added afterward.

**Effective approach:**
```yaml
inner:
  key:
    # Increased right binding to create MCU space
    bind: [B, B+3+21+0.5+3*X, B, B]
  rows:
    top:
      # Special binding adjustments for MCU area
      bind: [B, 0, B+B, B+B]
```

**MCU positioning pattern:**
- Position relative to a reliable key reference (e.g., `matrix_inner_middle`)
- Use calculated offsets: `shift: [0.5U+B+3+21/2, 0.5U + 3 - 51/2 - 0.5]`
- Create complementary cutouts for USB, reset button, etc.

**Critical elements:**
- MCU area must be integrated into plate outline via binding
- All cutouts positioned relative to same reference point
- Include access for programming (USB) and debugging (reset button)

### 5. Case Construction Pattern

**Layered extrusion approach:**
```yaml
cases:
  _body:
    # Bottom lip for lid attachment
    - name: case_lip
      extrude: 1.6

    # Main case walls  
    - name: case_wall
      extrude: 6.1
      shift: [0, 0, 1.6]      # Stack on top of lip

    # Switch mounting plate
    - name: case_top
      extrude: 2
      shift: [0, 0, 7.6]      # Stack on top of walls

    # Add mounting posts
    - name: _posts
      extrude: 4.4
      shift: [0, 0, 3.2]

    # Subtract cutouts
    - name: _switch_clips
      extrude: 1
      shift: [0, 0, 7.6]
      operation: subtract
```

**Key principles:**
- Build in layers with precise Z-axis positioning
- Use consistent shift calculations
- Add posts/bosses before subtracting holes
- Calculate heights based on switch depth + clearances

### 6. Template System for Reusability

**Parametric templates:**
```yaml
_posts_template:
  $params: [__r__]          # Parameter for radius
  top_left:
    what: circle
    adjust:
      ref: matrix_pinky_outer_top
      shift: [0.5U, -0.5U]
    radius: __r__           # Use parameter

_posts:
  $extends: outlines._posts_template
  $args: [2.6]              # Actual mounting post radius

_screw_holes:
  $extends: outlines._posts_template  
  $args: [0.8]              # Smaller radius for screws
```

**Benefits:**
- Consistent positioning across different sized elements
- Easy to modify all related components
- Reduces duplication and errors
- Enables design variants (different hole sizes, etc.)

### 7. Electronics Positioning Strategy

**Reference-based positioning:**
- Choose one reliable key as reference (e.g., `matrix_inner_middle`)
- Position all electronics relative to this reference
- Use calculated offsets that account for binding distances
- Create multiple cutouts for the same component if needed

**Cutout types needed:**
- **MCU housing:** Main component clearance
- **USB access:** Programming and power connection  
- **Reset access:** Small hole for reset button
- **Power connector:** JST or similar for battery
- **Optional:** LED access, touchpad, etc.

### 8. Common Pitfalls to Avoid

**❌ Don't do this:**
```yaml
# Forgetting to connect multiple zones
points:
  zones:
    matrix:
      # ... matrix keys
    thumbs:
      # ... thumb keys
      
outlines:
  plate:
    - what: rectangle
      where: true
      bound: true    # Only connects matrix, ignores thumbs!

# Missing zone positioning
thumbs:
  # No anchor definition = thumbs placed at origin
  columns: [...]

# Wrong outline approach for complexity
board:  # Complex organic shape
  - what: rectangle
    where: true
    bound: true    # Binding can't create organic shapes
```

**✅ Do this instead:**
```yaml
# Proper multi-zone connection
points:
  zones:
    matrix:
      anchor.shift: [50, -100]  # Position for KiCad
      # ... matrix definition
      
    thumbs:
      anchor:
        ref: matrix_index_bottom  # Position relative to matrix
        shift: [0.5kx, -1.25ky]
      # ... thumb definition
      
outlines:
  keywell:
    - what: rectangle
      where: [matrix]      # Just matrix keys
      bound: true
      
  thumb_section:
    - what: rectangle  
      where: [thumbs]      # Just thumb keys
      bound: true
      
  connection_glue:
    - what: polygon        # Manual connection
      points:
        - ref: matrix_inner_bottom
          shift: [0.5kx, -0.5ky]
        - ref: thumbs_near
          shift: [-0.5kx, 0.5ky]
        # ... connection points
        
  complete_board:
    - keywell
    - +thumb_section
    - +connection_glue

# Choose outline approach by complexity
simple_rectangular:
  - what: rectangle
    where: true  
    bound: true        # Binding works well

complex_organic:
  - what: polygon      # Manual control needed
    points: [...]
    fillet: 2
```

### 9. Advanced Techniques from Real Keyboards

**Zone Positioning Patterns:**
```yaml
# Pattern 1: Simple relative positioning (Tempest, Samoklava)
thumbs:
  anchor:
    ref: matrix_index_bottom
    shift: [0.5kx, -1.25ky]

# Pattern 2: Calculated positioning (Corney-island)
thumbs:
  anchor:
    ref: matrix_middle_bottom
    shift: [0.5 ks, -kp -3]

# Pattern 3: Complex relative positioning (Absolem)
thumbfan:
  anchor:
    ref: matrix_inner_bottom
    shift: [-7, -19]
```

**Connection Strategies by Complexity:**
```yaml
# Simple glue polygon (Samoklava)
thumbfan_glue:
  - what: polygon
    points:
      - ref: matrix_inner_bottom
        shift: [0.5 kx + 0.5px, -0.5 ky + 0.5 py]
      - ref: thumbfan_far_thumb
        shift: [0.5 kx - 0.5px, 0.5 ky + 0.5 py]
      # ... minimal connection points

# Complex connection (LambBT)  
board:
  - what: polygon
    operation: stack
    fillet: 2
    points:
      - ref: matrix_pinky_top
        shift: [-0.5px, 0.5py]
      - ref: matrix_pinky_bottom
        shift: [-0.5px, -0.5py]  
      # ... many precisely calculated points

# Helper point strategy (Corney-island)
plate_outline_bottom_1:
  key.tags: [helper]
  anchor:
    ref: matrix_ring_bottom
    shift: [ks * 0.465 + 0.005, -kp * 0.74 + 0.07]
```

**Electronics Integration Patterns:**
```yaml
# Method 1: Binding integration (ForestV1)
inner:
  key:
    bind: [B, B+21+3, B, B]  # Extra space for MCU

# Method 2: Separate area addition (Corney-island, Tempest)
base_outline:
  - keywell
  - +controller_area

# Method 3: Manual polygon inclusion (LambBT)
board:
  - what: polygon
    points:
      # ... points that include MCU area
```

## Design Process Recommendations

### 1. Start with Binding
- Define your key layout with proper binding first
- Test that the `plate` outline looks correct
- Only then add case components and electronics

### 2. Build Incrementally  
- Start with basic `plate` outline
- Add `case_top`, `case_wall`, `case_lip` one at a time
- Test each component before adding complexity

### 3. Plan MCU Integration Early
- Decide MCU position during layout phase
- Adjust binding to create necessary space
- Don't try to add MCU space afterward

### 4. Use Templates for Repeated Elements
- Mounting posts, screw holes, bosses
- Electronics cutouts
- Any element that appears multiple times

### 5. Layer Case Construction Carefully
- Calculate Z-heights precisely
- Account for switch depth, plate thickness, clearances
- Build bottom-up with proper shift values

## Conclusion

After analyzing successful keyboard designs, several key insights emerge about effective ergogen design patterns:

### The Multi-Approach Reality

**No single technique rules them all.** Different keyboard designs succeed using different strategies:

- **Simple layouts:** Binding-based outlines work excellently (Porcupine, Samoklava)
- **Complex organic shapes:** Polygon-based outlines are essential (LambBT, Corax56)
- **Multi-zone layouts:** Explicit connection strategies are mandatory (Absolem, Tempest, Corney-island)
- **Mixed complexity:** Hybrid approaches combining multiple techniques (Most real keyboards)

### The Foundation is Multi-Zone Thinking

**Most critical insight:** Real keyboards require multi-zone strategies, not just single-zone binding. The key foundation elements are:

1. **Zone Positioning:** Anchor zones relative to each other properly
2. **Zone Connection:** Use appropriate connection strategies (glue polygons, additive operations)
3. **Outline Strategy Selection:** Choose binding vs. polygons vs. hybrid based on shape complexity
4. **Electronics Integration:** Plan MCU/component space into your layout strategy

### Design Strategy Selection Guide

**Choose your approach based on keyboard complexity:**

- **Simple rectangular board:** Start with binding system
- **Single zone + MCU area:** Binding with electronics integration  
- **Matrix + thumb zones:** Multi-zone with connection polygons
- **Complex organic shape:** Polygon-based with helper points
- **Advanced layouts:** Hybrid approaches combining multiple techniques

### Success Pattern

The most successful approach is to:
1. **Understand your complexity:** Assess zones, shape complexity, electronics needs
2. **Choose appropriate techniques:** Don't force binding for organic shapes
3. **Build incrementally:** Test each layer before adding complexity
4. **Learn from examples:** Study similar complexity designs for proven patterns

**Updated critical takeaway:** Start by understanding your design complexity, then choose the appropriate combination of techniques. There's no one-size-fits-all approach - match your tools to your design requirements.
