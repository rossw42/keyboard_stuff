# Autogen Script - Mathematical Column Height Equalization

This folder contains the mathematical framework developed for automated keyboard layout generation with column height equalization.

## Files

### `forestv1.3_advanced_math.yaml`
Complete parametric system for mathematical column height equalization:
- **Column Configuration Analysis**: Automatically counts keys per column
- **Natural Height Calculations**: `(key_count - 1) * row_spacing`
- **Three Alignment Strategies**: Top, Bottom, and Center alignment
- **Ergonomic Curve Overlay**: Optional sine-wave curves for natural finger positioning
- **Mathematical Formulas**: All stagger calculations are parametrically defined
- **Visual Analysis Tools**: Alignment guides and column height visualization

### `column_height_math_guide.md`
Comprehensive implementation guide:
- **Mathematical Methods**: Detailed explanation of all approaches
- **Auto-Generation Algorithm**: Step-by-step process for programmatic generation
- **Practical Examples**: Real calculations with 6-column layout
- **Implementation Guidelines**: How to integrate into keyboard design workflows

### `forest_base_config.yaml`
Base configuration template for auto-generation:
- **Units Section**: All fundamental spacing and binding variables
- **Outlines Section**: Complete switch cutouts, plate definitions, MCU components, mounting system
- **Cases Section**: Full 3D case construction with layered body and removable lid
- **Ready for Points Generation**: Missing only the `points` section which will be generated mathematically
- **Complete Foundation**: Contains all non-geometric aspects of the keyboard design

## Mathematical Approach

The system analyzes column configurations and calculates precise stagger values to ensure all columns reach the same maximum height envelope. Key benefits:

1. **Parametric Design**: Change variables to adjust entire layout
2. **Multiple Strategies**: Choose alignment approach based on design goals
3. **Consistent Results**: Mathematical precision ensures exact height matching
4. **Ergonomic Integration**: Add natural curves while maintaining consistency
5. **Automated Generation**: Complete framework for programmatic layout creation

## Usage

1. **Configure Column Counts**: Set `ColN_KeyCount` for each column
2. **Choose Strategy**: Uncomment desired alignment method in stagger calculations
3. **Adjust Parameters**: Modify curve amplitude, target boundaries, etc.
4. **Generate Layout**: Mathematical formulas automatically calculate all staggers

## Future Development

This mathematical framework provides the foundation for:
- Automated keyboard layout generation tools
- Parametric design systems
- Multi-layout optimization
- Ergonomic curve fitting algorithms
- Consistent height matching across any keyboard configuration

*Developed as part of the Forest Keyboard project - exploring mathematical approaches to keyboard design automation.*
