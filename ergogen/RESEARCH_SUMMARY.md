# Ergogen Working Samples Research - Summary

*Research completed: October 22, 2025*

## What We Discovered

### 1. Official Learning Path
The Ergogen documentation recommends this progression:
1. Watch intro talk on core concepts
2. Read the docs (docs.ergogen.xyz)
3. Try the web UI (ergogen.xyz) - click and explore
4. **Search GitHub `#ergogen` topic** for real configs
5. Ask questions on Discord

### 2. Key Resource: FlatFootFox Tutorial
Found a comprehensive end-to-end tutorial series covering Ergogen v4:
- **Part 1**: Units & Points (keyboard layout)
- **Part 2**: Outlines (shapes and borders)
- **Part 3**: PCBs (KiCAD generation)
- **Part 4**: Footprints & Cases (3D case design)

**Why this matters**: Written specifically for v4 (latest version with breaking changes), addresses the "rocky onboarding process"

### 3. Ergogen v4 Breaking Changes
**Critical for evaluating samples:**
- v3's `rotate` → v4's `splay`
- New `rotate` property works differently
- Global `key:` definitions in zones
- Many older examples need migration

### 4. What Makes Good Working Samples
Based on research:
- Complete config sections (units, points, outlines, PCBs, cases)
- Detailed comments explaining decisions
- Real-world features (encoders, OLEDs, split designs)
- Progressive complexity (beginner → advanced)
- v4 syntax compatibility

## Key Concepts Learned

### Units System
```yaml
units:
  kx: cx  # Proxy for Choc width (or 'u' for MX)
  ky: cy  # Proxy for Choc height
  px: kx + 2  # Padded width
  py: ky + 2  # Padded height
```

### Points Patterns
- **Zones**: Groups of keys (matrix, thumbs, etc.)
- **Columns**: Vertical groups (pinky, ring, middle, index, inner)
- **Rows**: Horizontal groups (mod, bottom, home, top, num)
- **Stagger**: Vertical offset between columns
- **Splay**: Rotation of entire column
- **Spread**: Horizontal spacing between keys
- **Padding**: Vertical spacing between keys

### Multi-Zone Layouts
Most real keyboards have multiple zones that need explicit connection:
```yaml
zones:
  matrix:
    # Main keyboard
  thumbs:
    anchor:
      ref: matrix_inner_mod  # Position relative to matrix
      shift: [0, -2ky]
```

## Manual Collection Strategy

### GitHub Search Terms
```
#ergogen
ergogen config.yaml
ergogen keyboard language:YAML
topic:ergogen
```

### Known Keyboards to Find
- **Absolem** - Original Ergogen keyboard
- **Sofle Choc** - Popular split
- **ChonkV** - Tutorial keyboard
- **Corne/Crkbd** - Very popular split
- **Ferris** - Minimalist split
- **Sweep** - Ultra-minimal
- **Ben Vallack's keyboards** - Prolific user

### Suggested Organization
```
working_samples/
├── 01_simple/           # Learning examples
├── 02_split/            # Split keyboards
├── 03_unibody/          # Single-piece ergonomic
├── 04_macropads/        # Simple test cases
├── 05_advanced/         # Complex features
└── 06_mounting_styles/  # Already exists
```

## Next Steps

### Immediate Actions (You Can Do Now)
1. **Manual GitHub search** - 30 minutes collecting repository URLs
2. **Download 5-10 configs** - focus on variety and different complexity levels
3. **Test in web UI** (ergogen.xyz) - verify they work
4. **Create first organized sample** - with complete documentation
5. **Iterate** - add more as you find good examples

### What to Document for Each Sample
- Source (author, URL, license)
- Specifications (layout, switches, features)
- Complexity level (beginner/intermediate/advanced)
- Learning points (what makes it a good example)
- Known issues (modifications needed)
- Files (config, README, preview image)

### Testing Checklist
- [ ] Config loads without errors
- [ ] Points render correctly
- [ ] Outlines generate properly
- [ ] PCB exports successfully
- [ ] Case files generate (if included)
- [ ] All features work as described

## Integration with Your Project

### Current State
- **ergogen-toolkit**: VS Code extension (working)
- **kle_to_ergogen**: Converter (working)
- **ergogen_to_qmk_converter**: Planned (documented, not implemented)
- **mounting_styles**: Research (experimental)
- **working_samples**: Needs expansion ← **FOCUS HERE**

### Learning Progression
1. Simple samples (2x2, 3x3)
2. Column stagger (ergonomic basics)
3. Thumb clusters (multi-zone)
4. Features (encoders, OLEDs)
5. Mounting styles (case design)
6. Complete keyboards (full projects)

## Resources Created

1. **ERGOGEN_RESEARCH.md** - Comprehensive research notes
2. **WORKING_SAMPLES_COLLECTION_GUIDE.md** - Practical collection guide
3. **RESEARCH_SUMMARY.md** - This file (quick reference)

## Success Metrics

Collection is successful when you have:
- [ ] 10+ working samples across categories
- [ ] Clear beginner → advanced progression
- [ ] Complete documentation for each
- [ ] All samples tested and verified
- [ ] Common patterns documented
- [ ] Learning path established
- [ ] Integration with other tools shown

## Why This Matters

**The Goal**: Build a comprehensive collection of working Ergogen examples that:
1. Help beginners learn progressively
2. Provide reference implementations
3. Demonstrate best practices
4. Show real-world features
5. Support the other tools in your project

**The Impact**: 
- Faster onboarding for new users
- Better understanding of Ergogen patterns
- Reference for ergogen_to_qmk_converter development
- Validation for mounting_styles research
- Examples for VS Code extension

## Quick Start Guide

**Want to start collecting now?**

1. Open GitHub and search: `#ergogen`
2. Look for repos with stars and recent activity
3. Find the `config.yaml` or `.ergogen.yaml` file
4. Copy it to your local machine
5. Test at https://ergogen.xyz/
6. If it works, document it!
7. Organize into appropriate category
8. Repeat!

**Time estimate**: 2-3 hours for initial collection of 10 samples

---

## Final Thoughts

The research revealed that:
- **GitHub is the goldmine** - `#ergogen` topic has real configs
- **FlatFootFox tutorial is excellent** - comprehensive v4 guide
- **Web UI is powerful** - test everything there first
- **Community is active** - Discord for questions
- **v4 compatibility matters** - check for recent updates

**Your project has great potential** - the toolkit, converters, and research are all valuable. Expanding the working samples collection will tie everything together and provide concrete examples for users to learn from.

