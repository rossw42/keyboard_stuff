# Ergogen Keyboard Design Prompt

*A comprehensive prompt for creating working Ergogen configurations based on lessons learned from building keyboard mounting style examples and analyzing working samples.*

## Design Philosophy and Constraints

### Core Design Principles
- **Minimalistic aesthetic**: Focus on sleek, low-profile designs with thin walls (2-4mm) and minimal case height (<15mm)
- **Material efficiency**: Less material = lower cost, faster printing, better ergonomics
- **Incremental development**: Start simple, build complexity gradually
- **Pattern-based approach**: Use proven working patterns from successful configurations
- **Real-world assembly**: Consider physical assembly constraints and mounting system requirements

### Critical Success Factors
1. **Start with minimal working examples** - begin with 2x2 matrix before scaling up
2. **Test each addition incrementally** - add one feature at a time
3. **Use working samples as templates** - leverage proven patterns
4. **Avoid complex nested operations initially** - build complexity gradually

## Technical Requirements and Syntax Patterns

### Points Section Structure
Always use complete zone structures with proper YAML nesting:

```yaml
points:
  zones:
    matrix:
      key:
        padding: ky          # Standard spacing
        spread: kx           # Key spacing (19.05mm for MX)
        tags: [key]          # Tag for outline operations
      columns:
        col0:                # Simple column names
          key:
            column_net: C0   # Consistent net naming
        col1:
          key:
            column_net: C1
      rows:
        row0:                # Simple row names
          row_net: R0        # Consistent net naming
        row1:
          row_net: R1
```

### Outlines Section Pattern
Use systematic outline building with proper operations:

```yaml
outlines:
  # Base shapes first
  board:
    - what: polygon
      operation: stack       # Always include for polygon
      fillet: 2             # Add fillets for manufacturability
      points:
        - ref: matrix_col0_row0
          shift: [-10, -10]
        # ... more points

  # Expanded versions for case walls
  expanded_board:
    - what: outline
      name: board
      expand: 3             # Do expansion in outlines, not cases

  # Component cutouts
  switch_cutouts:
    - what: rectangle
      where: [key]          # Use defined tags
      size: 14              # Standard MX cutout
      bound: false          # Don't include in bounds calculation
```

### Cases Section Architecture
Follow proven case construction patterns:

```yaml
cases:
  # Individual components
  _outer_wall:
    - name: expanded_board  # Reference outline names, not case names
      extrude: 5.6

  _inner_cavity:
    - name: board
      extrude: 5.6

  # Combined assemblies
  case_walls:
    - what: case
      name: _outer_wall
      operation: add
    - what: case
      name: _inner_cavity
      operation: subtract
```

## Mounting System Design Requirements

### Essential Components for Any Mount Style
1. **Structural support** - mounting posts/tabs/channels
2. **Screw clearance** - properly sized holes
3. **Assembly logic** - how parts connect physically
4. **Material considerations** - wall thickness and rigidity

### Mounting Style Specifications

#### Tray Mount (Simplest)
- Large standoff posts (2.5mm radius for M2 screws)
- Small screw holes (1.1mm radius) subtracted from posts
- Triangular mounting pattern for stability
- 4mm post height for standard PCB clearance

#### Top Mount
- Plate mounting tabs that attach to top case
- Custom plate geometry with mounting features
- Top case requires corresponding mounting points
- Consider flex characteristics of mounting system

#### Bottom Mount
- Plate tabs attach to bottom case edges
- Allows suspended top case design
- More uniform rigidity than top mount
- Requires clearance for top shell assembly

#### Sandwich Mount
- Through-holes in plate aligned with case mounting
- Precise tolerances required for proper assembly
- Even force distribution across plate
- Complex but balanced typing experience

#### Gasket Mount (Most Complex)
- Gasket channels in both case halves
- Plate gasket contact surfaces
- No direct metal-to-metal contact
- Premium typing experience but complex design

#### Integrated Plate
- Single-piece top case/plate design
- Switch cutouts directly in case geometry
- Very rigid, no customization options
- Simplified assembly but limited flexibility

## Common Pitfalls and Solutions

### Critical Errors to Avoid
1. **Malformed zone structures** - always use complete columns/rows definitions
2. **Invalid key property nesting** - use proper YAML structure (`key: column_net:` not `key.column_net:`)
3. **Missing anchor references** - ensure all referenced points exist
4. **Complex outline operations** - avoid nested operations initially
5. **Inconsistent net naming** - standardize on template variables or direct names throughout
6. **Generic footprint names** - use specific names that match available libraries
7. **Missing mounting hole definitions** - define all referenced mounting points
8. **Expansion in cases section** - do outline expansion in outlines section only

### Debugging Strategy
1. **Start with points only** - verify zone structure works
2. **Add basic outlines** - test outline generation
3. **Add simple cases** - test extrusion works
4. **Add complexity incrementally** - never add multiple complex features at once
5. **Compare against working samples** - use proven patterns as templates

## Best Practices Checklist

### Design Phase
- [ ] Start with 2x2 matrix for testing
- [ ] Use standard MX spacing (19.05mm) unless specific requirements
- [ ] Plan mounting system early in design process
- [ ] Consider assembly sequence and constraints

### Implementation Phase
- [ ] Use consistent naming conventions throughout
- [ ] Include proper tags for all outline operations
- [ ] Add fillets (1-3mm) for manufacturability
- [ ] Include mounting holes and structural support
- [ ] Test incrementally with Ergogen web interface

### Validation Phase
- [ ] Verify all referenced points exist
- [ ] Check footprint names match available libraries
- [ ] Ensure net naming consistency
- [ ] Validate mounting system completeness
- [ ] Generate both individual parts and assemblies

## Footprint and Component Standards

### Switch Footprints
Use specific footprint names that match your library:
- `choc` or `choc_v1` for Choc switches
- `mx` or `cherry_mx_hotswap` for MX switches
- Include diodes for all switches in matrix

### Controller Integration
- Use specific controller names (e.g., `promicro`, `xiao`, `nice_nano`)
- Include proper pin mappings for rows/columns
- Consider placement for assembly access

### Additional Components
- **Encoders**: Include diodes in matrix design
- **OLED screens**: Use specific footprint names
- **Mounting holes**: Always define in points section if referenced

## Step-by-Step Development Process

### Phase 1: Basic Structure
1. Create minimal 2x2 matrix with proper zone structure
2. Add basic outline with polygon and points
3. Test generation in Ergogen web interface
4. Verify points and outline generation works

### Phase 2: Layout Development
1. Expand to target layout size (e.g., 4x5 macropad)
2. Add proper key spacing and tags
3. Include any special key sizes (2U keys, rotary encoders)
4. Test outline generation with new layout

### Phase 3: Component Integration
1. Add controller placement and pin mapping
2. Include diodes for all switches
3. Add any additional components (OLED, encoders)
4. Verify footprint names match available libraries

### Phase 4: Mounting System
1. Define mounting hole locations
2. Create mounting support structures
3. Add screw clearance holes
4. Test mechanical assembly logic

### Phase 5: Case Design
1. Start with basic extrusion of main outline
2. Add wall structures with inner/outer approach
3. Include mounting system integration
4. Generate assembly views for validation

### Phase 6: Refinement
1. Add fillets and manufacturability features
2. Optimize wall thickness and support structures
3. Generate final individual parts and assemblies
4. Document assembly requirements

## Validation and Testing

### Ergogen Web Interface Testing
- Test each development phase in web interface
- Verify points generation first
- Check outline operations work correctly
- Validate case generation produces expected results

### Physical Assembly Validation
- Verify mounting hole alignment and sizing
- Check component clearances and accessibility
- Ensure assembly sequence is practical
- Validate structural integrity of mounting system

### Manufacturing Readiness
- Confirm all referenced footprints are available
- Verify net names are consistent and complete
- Check that case parts can be manufactured
- Ensure proper tolerances for assembly

## Success Metrics

A successful Ergogen configuration should:
1. **Generate without errors** in Ergogen web interface
2. **Include complete mounting system** with structural support
3. **Use proven syntax patterns** from working samples
4. **Follow incremental development** approach
5. **Consider real-world assembly** constraints
6. **Maintain design consistency** throughout configuration
7. **Generate manufacturable parts** with proper tolerances
8. **Include all necessary components** for functional keyboard

## Resources and References

### Essential Documentation
- [Ergogen Official Docs](https://docs.ergogen.xyz/) - comprehensive syntax reference
- [FlatFootFox Tutorial](https://flatfootfox.com/ergogen-part4-footprints-cases/) - best case design patterns
- Working samples in `keyboard_stuff/ergogen/working_samples/` - proven patterns

### Testing Environment
- [Ergogen Web Interface](https://ergogen.xyz) - immediate feedback and testing
- Start with points and outlines before adding cases
- Use minimal examples to isolate issues

### Community Examples
Study working configurations before creating new ones:
- `berylline.yml` - excellent structure and organization
- `tutorial.yml` - proven case construction patterns
- `corney_island.yml` - comprehensive mounting system examples

## Implementation Notes

When using this prompt to create Ergogen files:

1. **Always start simple** - resist the urge to create complex designs immediately
2. **Use working samples as templates** - don't start from scratch
3. **Test frequently** - verify each addition works before proceeding
4. **Consider the physical world** - think about how the keyboard will actually be assembled
5. **Follow proven patterns** - use syntax structures that are known to work
6. **Plan for manufacturing** - include proper fillets, tolerances, and assembly features

The goal is to create keyboards that are not only functional but also manufacturable, assemblable, and provide an excellent typing experience through thoughtful mounting system design.
