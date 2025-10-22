# Guide: Collecting Ergogen Working Samples

*A practical guide for expanding the working_samples collection*

## Research Summary

Based on the research, here's what we've learned about finding and organizing Ergogen examples:

### Key Resources Found

1. **Official Ergogen Docs**: https://docs.ergogen.xyz/
2. **Web UI with Live Preview**: https://ergogen.xyz/
3. **FlatFootFox Tutorial Series**: Comprehensive v4 tutorial covering Units, Points, Outlines, PCBs, and Cases
4. **GitHub Topic**: `#ergogen` - search manually for real configs
5. **Discord Community**: http://discord.ergogen.xyz/

### What Makes a Good Working Sample

From the FlatFootFox tutorial and official docs:
- **Complete sections**: units, points, outlines, PCBs, cases
- **Comments explaining design decisions**
- **Real-world features**: encoders, OLEDs, split designs
- **Ergogen v4 syntax** (important - v3 had breaking changes)
- **Progressive complexity**: simple to advanced examples

## Manual Collection Strategy

Since GitHub blocks automated searches, here's the manual approach:

### Step 1: GitHub Manual Searches

Search terms to use on GitHub:
```
#ergogen
ergogen config.yaml
ergogen keyboard language:YAML
topic:ergogen
```

Filter by:
- **Stars** (popular/proven designs)
- **Recently updated** (likely v4 compatible)
- **Forks** (actively used)

### Step 2: Known Keyboards to Find

Based on documentation references:
- **Absolem** - The original Ergogen keyboard by Dénes Bán
- **Sofle Choc** - Popular ergonomic split
- **ChonkV** - FlatFootFox's tutorial keyboard
- **Corne/Crkbd** - Very popular split
- **Ferris** - Minimalist split
- **Sweep** - Ultra-minimal split
- **Ben Vallack's keyboards** - Prolific Ergogen user

### Step 3: Categories to Organize

Suggested directory structure:
```
working_samples/
├── 01_simple/              # Learning examples
│   ├── 2x2_basic/
│   ├── 3x3_with_stagger/
│   └── 4x4_with_thumb/
├── 02_split/               # Split keyboards
│   ├── corne/
│   ├── sofle/
│   └── ferris/
├── 03_unibody/             # Single-piece ergonomic
│   ├── absolem/
│   └── sweep/
├── 04_macropads/           # Simple test cases
│   ├── numpad/
│   └── encoder_pad/
├── 05_advanced/            # Complex features
│   ├── with_oled/
│   ├── with_encoders/
│   └── with_trackball/
└── 06_mounting_styles/     # Already exists
    └── (current examples)
```

## What to Document for Each Sample

Create a README.md in each sample directory with:

```markdown
# [Keyboard Name]

## Source
- **Author**: [Name/GitHub username]
- **URL**: [Original repository]
- **License**: [License type]

## Specifications
- **Ergogen Version**: v4 / v3 (specify)
- **Layout**: [e.g., 3x5+3 split]
- **Switch Type**: MX / Choc / Both
- **Features**: 
  - [ ] Split design
  - [ ] OLED display
  - [ ] Rotary encoders
  - [ ] RGB lighting
  - [ ] Wireless support

## Complexity Level
- [ ] Beginner - Simple rectangular layout
- [ ] Intermediate - Column stagger, thumb cluster
- [ ] Advanced - Complex features, custom footprints

## Learning Points
What makes this a good example:
- [Key concept 1]
- [Key concept 2]
- [Key concept 3]

## Known Issues
- [Any modifications needed]
- [Compatibility notes]

## Files
- `config.yaml` - Main Ergogen configuration
- `README.md` - This file
- `preview.png` - Visual preview (if available)
```

## Key Concepts from FlatFootFox Tutorial

### Units Section
```yaml
units:
  # Proxy variables for easy switching
  kx: cx  # or 'u' for MX
  ky: cy  # or 'u' for MX
  # Padding for outlines
  px: kx + 2
  py: ky + 2
```

### Points Section Patterns
```yaml
points:
  zones:
    matrix:
      key:
        padding: 1ky    # Vertical spacing
        spread: 1kx     # Horizontal spacing
      columns:
        pinky:
          key.stagger: 5     # Column stagger
        ring:
          key.splay: -4      # Column rotation
      rows:
        home:
        top:
```

### Multi-Zone Layouts
```yaml
points:
  zones:
    matrix:
      # Main keyboard matrix
    thumbs:
      anchor:
        ref: matrix_inner_mod  # Position relative to matrix
        shift: [0, -2ky]       # Offset from reference
      columns:
        layer:
        space:
```

## Ergogen v4 vs v3 Differences

**Important for evaluating samples:**

### v3 → v4 Changes
- `rotate` property renamed to `splay`
- New `rotate` property works differently (fan effect)
- Global `key:` definition added to zones
- `spread:` no longer needs manual application to every column

### Checking Version
Look for these v4 patterns:
```yaml
# v4 style
zones:
  matrix:
    key:
      spread: 1kx  # Global key definition

# v3 style (needs updating)
zones:
  matrix:
    columns:
      pinky:
        spread: 19  # Manual per-column
```

## Testing Samples

### Web UI Testing
1. Go to https://ergogen.xyz/
2. Paste config into left panel
3. Check for errors in console
4. Verify preview looks correct
5. Download outputs to verify completeness

### What to Check
- [ ] Config loads without errors
- [ ] Points render correctly
- [ ] Outlines generate properly
- [ ] PCB exports successfully
- [ ] Case files generate (if included)
- [ ] All features work as described

## Integration with Current Project

### Where Samples Fit
```
Ergogen Toolkit/
├── ergogen-toolkit/        # VS Code extension
├── kle_to_ergogen/         # KLE converter
├── ergogen_to_qmk_converter/  # QMK converter (planned)
├── working_samples/        # ← EXPAND THIS
│   ├── 01_simple/
│   ├── 02_split/
│   └── ...
├── mounting_styles/        # Case research
└── keyboards/              # Specific projects
```

### Learning Progression
1. **Start with simple samples** (2x2, 3x3)
2. **Progress to column stagger** (ergonomic basics)
3. **Add thumb clusters** (multi-zone layouts)
4. **Explore features** (encoders, OLEDs)
5. **Study mounting styles** (case design)
6. **Build complete keyboards** (full projects)

## Action Plan

### Phase 1: Manual Collection (1-2 hours)
1. Search GitHub for `#ergogen` topic
2. Identify 10-15 promising repositories
3. Download config files
4. Test each in web UI
5. Document what works

### Phase 2: Organization (1 hour)
1. Create directory structure
2. Sort samples by complexity
3. Create README for each
4. Add preview images
5. Document learning points

### Phase 3: Documentation (1 hour)
1. Extract common patterns
2. Update lessons learned
3. Create quick reference guide
4. Document gotchas and tips

### Phase 4: Integration (30 min)
1. Update main README
2. Link to new samples
3. Create learning path
4. Add to VS Code extension examples

## Specific Repositories to Check

Based on community references:
- `ergogen/ergogen` - Official repo (check examples folder)
- Search for "absolem keyboard"
- Search for "sofle ergogen"
- Search for "corne ergogen"
- Search for "ferris keyboard"
- Ben Vallack's GitHub profile
- FlatFootFox's ChonkV repository

## Tips for Evaluation

### Good Signs
- Recent commits (v4 compatible)
- Complete config sections
- Detailed comments
- Multiple features
- Active issues/discussions
- Clear documentation

### Red Flags
- No recent updates (likely v3)
- Incomplete configs
- No comments
- Syntax errors
- Abandoned projects

## Next Steps

1. **Start manual GitHub search** - spend 30 minutes collecting URLs
2. **Download 5-10 configs** - focus on variety
3. **Test in web UI** - verify they work
4. **Create first organized sample** - document thoroughly
5. **Iterate** - add more as you find them

## Resources for Reference

- **Ergogen Docs**: https://docs.ergogen.xyz/
- **Web UI**: https://ergogen.xyz/
- **FlatFootFox Tutorial**: https://flatfootfox.com/ergogen-introduction
- **Discord**: http://discord.ergogen.xyz/
- **Reddit**: r/ErgoMechKeyboards

---

## Success Metrics

You'll know the collection is successful when:
- [ ] 10+ working samples across different categories
- [ ] Clear progression from simple to complex
- [ ] Each sample has complete documentation
- [ ] All samples tested and verified working
- [ ] Common patterns documented
- [ ] Learning path established
- [ ] Integration with other tools demonstrated

