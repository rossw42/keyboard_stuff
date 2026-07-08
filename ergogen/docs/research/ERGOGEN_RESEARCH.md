> **Snapshot notice (added 2026-07-07):** compiled October 22, 2025. Links-based content ages well but verify against current Ergogen releases (local install is v4.1.0). See ../ERGOGEN_REFERENCE.md for the authoritative config reference.

# Ergogen Research - Working Samples & Resources

*Research compiled: October 22, 2025*

## Official Resources

### Documentation & Learning
- **Official Docs**: https://docs.ergogen.xyz/
- **Official Web UI**: https://ergogen.xyz/ (with live previews)
- **Unofficial Web UI**: https://ergogen.ceoloide.com/ (community enhanced, now merged into official)
- **Discord Community**: http://discord.ergogen.xyz/

### Key Learning Path (from official docs)
1. Watch introductory talk on core concepts
2. Read the documentation (dense but comprehensive)
3. Try web-based deployments - click things, look at outputs
4. Search `#ergogen` topic on GitHub for real-life configs
5. Ask questions on Discord

## Tutorial Series

### FlatFootFox Tutorial Series
**URL**: https://flatfootfox.com/ergogen-introduction

Comprehensive end-to-end tutorial covering Ergogen v4:
- **Part 1**: Units & Points - defining keyboard layout
- **Part 2**: Outlines - creating keyboard borders and shapes
- **Part 3**: PCBs - generating KiCAD files with footprints
- **Part 4**: Footprints & Cases - 3D case generation

**Why this matters**: 
- Written for Ergogen v4 (latest version with breaking changes)
- End-to-end example from scratch
- Addresses the "rocky onboarding process"
- Long-form written guide (not just video)

## GitHub Search Strategy

Since GitHub blocks automated searches, manual search strategies:

### Search Terms to Use
```
#ergogen (GitHub topic)
ergogen config.yaml
ergogen keyboard
language:YAML ergogen
```

### Known Keyboard Repositories to Check
Based on documentation references:
- **Absolem** by DÃ©nes BÃ¡n (the original Ergogen keyboard)
- **Sofle Choc** (popular ergonomic split)
- Keyboards by **Ben Vallack** (prolific Ergogen user)
- **ChonkV** by FlatFootFox (tutorial keyboard)

## What Makes a Good Working Sample

From the research, good examples should have:
1. **Complete config files** - all sections (units, points, outlines, PCBs, cases)
2. **Comments** - explaining design decisions
3. **Real-world features** - encoders, OLEDs, split designs
4. **Different mounting styles** - variety of case approaches
5. **Ergogen v4 syntax** - using latest version
6. **Multiple complexity levels** - from simple to advanced

## Key Ergogen Concepts (from FlatFootFox)

### What Ergogen Does
"Aims to provide a common configuration format to describe ergonomic 2D layouts and generate automatic plates, cases, as well as un-routed PCBs"

### Five Primary Sections
1. **Units** - Define custom variables for repeated values
2. **Points** - Define [x,y] positions of keys (the real magic)
3. **Outlines** - Define keyboard shape/borders (exported as .dxf)
4. **PCBs** - Generate KiCAD files with footprints (the star of the show)
5. **Cases** - Generate 3D case files

### Design Philosophy
- **Column stagger focused** - designed for ergonomic layouts
- **Parametric design** - avoid fiddly graphical CAD alignment
- **Text-based** - YAML configs instead of GUI tools
- **Declarative** - describe what you want, not how to build it

## Ergogen v4 Breaking Changes

**Important**: Many older examples use v3 syntax. Need to:
- Reference the v4 migration guide
- Check if examples are v4 compatible
- Update older configs if needed

## Community Insights

### From r/ErgoMechKeyboards
- Active community for ergonomic mechanical keyboards
- Good place to discover new designs
- See what's trending in the space

### From Discord
- Active community for specific questions
- Real-time help with configs
- Share work-in-progress designs

## Next Steps for Research

### Manual GitHub Searches to Perform
1. Search GitHub for `#ergogen` topic
2. Look for repos with `config.yaml` or `.ergogen.yaml` files
3. Filter by:
   - Recently updated (v4 compatible)
   - Stars (popular/proven designs)
   - Forks (actively used)

### Specific Keyboards to Research
- [ ] Absolem (the original)
- [ ] Sofle Choc
- [ ] ChonkV
- [ ] Ben Vallack's keyboards
- [ ] Corne/Crkbd variants
- [ ] Ferris variants
- [ ] Sweep variants

### Categories to Collect
- [ ] Simple rectangular layouts (learning examples)
- [ ] Split keyboards (most common ergonomic style)
- [ ] Unibody ergonomic (single piece)
- [ ] Macropads (simple, good for testing)
- [ ] Advanced features (encoders, OLEDs, trackballs)
- [ ] Different mounting styles (tray, gasket, etc.)

## Integration with Current Project

### Where to Store Examples
```
working_samples/
â”œâ”€â”€ simple/           # Basic rectangular layouts
â”œâ”€â”€ split/            # Split keyboard designs
â”œâ”€â”€ unibody/          # Single-piece ergonomic
â”œâ”€â”€ macropads/        # Simple test cases
â”œâ”€â”€ advanced/         # Complex features
â””â”€â”€ mounting_styles/  # Different case approaches (already exists)
```

### What to Document for Each Sample
- Source URL and author
- Ergogen version used
- Key features (split, encoders, etc.)
- Complexity level (beginner/intermediate/advanced)
- Known issues or modifications needed
- What makes it a good learning example

## Tools for Working with Examples

### Web UI Features (ergogen.xyz)
- Live preview of layouts
- Import external footprints
- KiCAD previews
- GitHub integration
- Download generated files

### Local CLI
```bash
npm i -g ergogen
ergogen input.yaml -o output_folder
```

## Resources for Footprints

Ergogen needs footprint libraries for components:
- MX switches
- Choc switches
- Pro Micro controllers
- Encoders
- OLEDs
- Diodes
- etc.

**Note**: The web UI now supports importing external footprints, making it easier to use community libraries.

---

## Action Items

1. **Manual GitHub search** for #ergogen topic
2. **Collect 10-20 working examples** across different categories
3. **Test each example** in web UI to verify it works
4. **Document each example** with metadata
5. **Organize by complexity** for learning progression
6. **Extract patterns** that work well
7. **Update lessons learned** with new insights


