# Ergogen Keyboard Mounting Style Examples

This directory contains complete Ergogen YAML configurations demonstrating the six major keyboard mounting styles. Each configuration shows the structural differences and mounting requirements for that particular style.

## Created Files

### 1. Tray Mount (`tray_mount.yaml`)
- **Description**: PCB sits in a case tray with perimeter mounting holes
- **Key Features**:
  - Mounting holes around PCB perimeter (6 holes total)
  - Large mounting pads with M3 drill holes  
  - PCB edge clearance for tray mounting
  - Reinforced mounting points for stability

### 2. Top Mount (`top_mount.yaml`)
- **Description**: Plate attached to case from above with standoffs
- **Key Features**:
  - Countersunk holes for top-mounted screws (6 mounting points)
  - Separate switch plate from PCB
  - Larger diameter holes for screw head clearance
  - Accessible mounting from keyboard top

### 3. Bottom Mount (`bottom_mount.yaml`)
- **Description**: Plate attached to case from bottom
- **Key Features**:
  - Standard mounting holes without countersinking
  - Screws inserted from bottom of case
  - Separate switch plate and PCB layers
  - Bottom case with recessed screw head areas

### 4. Sandwich Mount (`sandwich_mount.yaml`)
- **Description**: Plate sandwiched between case layers with through-holes
- **Key Features**:
  - Through-holes that penetrate all layers (6 mounting points)
  - Multiple case layers (top, plate, PCB, bottom)
  - Long bolts connecting all components
  - Reinforced mounting pads on all layers

### 5. Integrated Mount (`integrated_mount.yaml`)
- **Description**: Plate and PCB are one unit (plateless design)
- **Key Features**:
  - Switch cutouts directly in PCB (no separate plate)
  - Minimal mounting points (4 corners only)
  - Single integrated PCB/plate component
  - Simplified case structure

### 6. Gasket Mount (`gasket_mount.yaml`)
- **Description**: Flexible gasket material between plate and case
- **Key Features**:
  - Gasket grooves cut into case perimeter
  - Gasket tabs extending from plate edges
  - No direct screw mounting of plate
  - Multiple case components with gasket channels

## Common Design Elements

All configurations include:
- **4x3 key matrix** layout for demonstration
- **Choc hotswap switches** with diodes
- **M3 mounting holes** where applicable
- **Reinforcement pads** around mounting points
- **Layer identification text** for assembly guidance

## Usage Notes

1. **Footprint Dependencies**: These configurations assume standard Ergogen footprints are available
2. **Switch Type**: All examples use Choc low-profile switches - can be modified for MX switches
3. **Mounting Hardware**: M3 screws assumed - adjust hole sizes for different hardware
4. **Case Manufacturing**: Some mounting styles require precise tolerances for proper fit

## File Structure

Each YAML file contains:
- **Meta information**: Name, version, description
- **Units**: Spacing and padding definitions  
- **Points**: Key matrix and switch definitions
- **Outlines**: Board shapes and mounting features
- **PCBs**: Layer definitions and footprint placements

## Reference Images

See the `reference_images/` directory for visual examples of each mounting style from [keyboard.university](https://www.keyboard.university/200-courses/keyboard-mounting-styles-4lpp7).

## Customization

To adapt these examples:
1. Modify the `matrix` zone for different key layouts
2. Adjust mounting hole positions and quantities
3. Change switch types in the footprint definitions
4. Scale board dimensions by modifying the outline points

## Manufacturing Considerations

- **Tray Mount**: Requires precise case machining for PCB tray
- **Top/Bottom Mount**: Need proper standoff heights for assembly
- **Sandwich Mount**: Requires long through-bolts and spacers
- **Integrated Mount**: PCB must be thick enough for switch retention
- **Gasket Mount**: Needs flexible gasket material and precise groove dimensions

Created: August 11, 2025
