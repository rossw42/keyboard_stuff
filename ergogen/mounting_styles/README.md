# Ergogen Mounting Style Examples

This directory contains working Ergogen configuration files demonstrating different keyboard mounting styles using a simple 2x2 keyboard layout.

## Files

1. **01_tray_mount.yaml** - Simplest mounting method, PCB screws to posts in bottom case
2. **02_top_mount.yaml** - Plate attaches to tabs on top case, better typing feel
3. **03_bottom_mount.yaml** - Plate attaches to bottom case, consistent stiffness
4. **04_sandwich_mount.yaml** - Screws pass through entire assembly, balanced feel
5. **05_integrated_plate.yaml** - Plate and top case are one piece, very rigid
6. **06_gasket_mount.yaml** - Plate floats on gaskets, premium typing experience
7. **07_spring_mount.yaml** - Springs provide cushioning, unique dynamic response
8. **08_plateless_mount.yaml** - No plate, switches mount directly to reinforced PCB

## Usage

Each file is a complete, working Ergogen configuration that you can:

1. Copy into the [Ergogen web interface](https://ergogen.ceoloide.com/) to test
2. Use as a starting point for your own keyboard designs
3. Study to understand the geometric requirements of each mounting style

## Design Complexity

**Beginner Friendly:**

- Tray Mount (01) - Standard approach, minimal custom geometry
- Integrated Plate (05) - Single-piece design, straightforward

**Intermediate:**

- Top Mount (02) - Custom plate tabs required
- Bottom Mount (03) - Mounting bosses and floating top case
- Plateless Mount (08) - Reinforced PCB design

**Advanced:**

- Sandwich Mount (04) - Precise through-hole alignment critical
- Spring Mount (07) - Spring integration and wells
- Gasket Mount (06) - Most complex with gasket channels

## Key Features

- **2x2 Layout**: Simple enough to understand, complex enough to demonstrate concepts
- **Complete Configs**: Each file includes points, outlines, cases, and PCB sections
- **Proper YAML**: No syntax errors, ready to use in Ergogen
- **Realistic Parameters**: Based on standard MX switches and 3D printing tolerances
- **Comments**: Extensive documentation explaining each mounting concept

## Customization

All examples use these standard parameters that you can adjust:

```yaml
units:
  kx: 19.05 # MX key spacing
  ky: 19.05
  case_wall_thickness: 2.5 # 3D printing friendly
  case_height: 12 # Total case height
  plate_thickness: 1.6 # Standard plate thickness
  mount_hole_diameter: 2.2 # M2 screw clearance
```

## Next Steps

1. Choose a mounting style based on your priorities (cost, feel, complexity)
2. Test the example in Ergogen web interface
3. Adapt to your specific keyboard layout (more keys, different arrangements)
4. Add electronics (MCU, connectors, etc.)
5. 3D print prototypes to test fit and feel

## Mounting Style Trade-offs

| Style      | Cost   | Complexity   | Typing Feel | Sound     | Assembly |
| ---------- | ------ | ------------ | ----------- | --------- | -------- |
| Tray       | Low    | Simple       | Stiff       | Pingy     | Easy     |
| Top        | Medium | Moderate     | Good        | Balanced  | Moderate |
| Bottom     | Medium | Moderate     | Consistent  | Solid     | Moderate |
| Sandwich   | Medium | Complex      | Balanced    | Muffled   | Complex  |
| Integrated | Low    | Simple       | Very Stiff  | Solid     | Easy     |
| Gasket     | High   | Very Complex | Premium     | Dampened  | Complex  |
| Spring     | High   | Complex      | Dynamic     | Cushioned | Complex  |
| Plateless  | Low    | Moderate     | Elastic     | Direct    | Moderate |

Choose based on your priorities: beginners should start with Tray or Integrated, while experienced builders can tackle Gasket or Spring mounts for premium results.
