# NuPhy Air60 V2 - Home Row Mods Practice Layout

## Overview

This layout implements **home row modifiers** (home row mods) on practice layers for the NuPhy Air60 V2 keyboard. Home row mods allow you to use modifier keys (Ctrl, Alt, Shift, GUI/Win) by holding down the home row keys (A, S, D, F, J, K, L, ;) instead of reaching for traditional modifier keys.

## What Are Home Row Mods?

Home row mods are **dual-role keys** that:
- Act as **normal letters** when **tapped** quickly
- Act as **modifiers** when **held** down
- Provide ergonomic access to all modifiers without moving your hands from home position

For example:
- Tap `A` → types "a"
- Hold `A` → acts as GUI/Win key
- Hold `A` + tap `C` → GUI+C (copy on Windows/Linux)

## Implementation Details

### Safe Practice Design
- **Layer 0**: Original base layer (UNTOUCHED)
- **Layer 1**: Original function layer (UNTOUCHED) 
- **Layer 2-4**: NEW home row mods practice layers
- **Layer 5-6**: Original RGB control layers (UNTOUCHED)
- **Layer 7**: Original navigation layer (UNTOUCHED)

### Home Row Modifier Layout (GACS Order)

Following the popular **Miryoku layout**, this uses the **GACS** order:

**Left Hand:**
- `A` = **G**UI (Windows/Super key)
- `S` = **A**lt 
- `D` = **C**trl
- `F` = **S**hift

**Right Hand:**
- `J` = **S**hift
- `K` = **C**trl  
- `L` = **A**lt
- `;` = **G**UI (Windows/Super key)

### Practice Layers

#### Layer 2: Basic Home Row Mods
- Standard QWERTY layout with home row mods enabled
- Access via `MO(2)` from Layer 1
- Perfect for initial practice

#### Layer 3: Home Row Mods + Navigation
- Same home row mods as Layer 2
- Up arrow replaced with Home key for navigation practice
- Access via `MO(3)` from Layer 2

#### Layer 4: Advanced Practice
- Same home row mods as previous layers
- F-keys on number row for shortcut practice
- End key for navigation
- `TO(0)` to return to base layer
- Access via `MO(4)` from Layer 3

## Getting Started

### 1. Load the Layout
- Open VIA/Vial software
- Load `nuphy_air60_v2_home_row_mods.layout.json`
- Flash to your keyboard

### 2. Access Practice Layers
- **Layer 0** (Base) → Hold **Fn** → **Layer 1**
- **Layer 1** → Hold **Fn** + press **Left Shift** → **Layer 2** (Home Row Mods)
- **Layer 2** → press **Fn** → **Layer 3**
- **Layer 3** → press **Fn** → **Layer 4** 
- **Layer 4** → press **Fn** → **Layer 0** (Return to base)

### 3. Practice Techniques

#### Start with Swift Taps
- **Most important**: Type with quick, swift taps
- Don't linger on keys - press and release immediately
- Think "tap" not "press"

#### Common Shortcuts to Practice
- **Copy**: Hold `D` (Ctrl) + tap `C`
- **Paste**: Hold `D` (Ctrl) + tap `V`
- **Select All**: Hold `D` (Ctrl) + tap `A` (use right-hand Ctrl)
- **Window switching**: Hold `S` (Alt) + tap `Tab`
- **New tab**: Hold `D` (Ctrl) + tap `T`

#### Hand Coordination
- Use **opposite hands** for modifier + key combinations
- Hold left `F` (Shift) + tap right-hand letters for capitals
- Hold right `J` (Shift) + tap left-hand letters for capitals

## Key Concepts

### Timing
- **Tapping Term**: ~200ms window to distinguish tap vs hold
- **Quick Tap**: Fast press+release = letter
- **Hold**: Press and pause = modifier activation

### Hand Alternation
- **Left modifiers** work with **right-hand keys**
- **Right modifiers** work with **left-hand keys**
- Prevents same-finger conflicts

### Modifier Combinations
- Can combine multiple modifiers: `Ctrl+Shift+T`, `Alt+Shift+Tab`
- Use multiple fingers on same hand for complex shortcuts

## Tips for Success

### 1. Start Slowly
- Begin with simple shortcuts (Ctrl+C, Ctrl+V)
- Practice basic letter typing to build muscle memory
- Gradually add more complex combinations

### 2. Common Mistakes to Avoid
- **Don't hold too long** - causes accidental modifiers
- **Don't rush** - let timing become natural
- **Don't forget hand alternation** - use opposite hands

### 3. Practice Exercises
- Type common words: "the", "and", "for", "are"
- Practice copy/paste workflow
- Try browser shortcuts: Ctrl+T, Ctrl+W, Ctrl+Tab
- Text editing: Ctrl+A, Ctrl+X, Ctrl+V

### 4. Troubleshooting
- **Getting random capitals?** → Tap faster, hold Shift less
- **Shortcuts not working?** → Hold modifier longer
- **Typing feels weird?** → Focus on swift taps

## Advanced Features

### Layer Switching Practice
- Layer 2-4 progression builds complexity gradually
- Each layer adds new elements while maintaining home row mods
- Practice moving between layers for different tasks

### Customization Options
- Modify timeout settings in VIA if needed
- Adjust to personal typing speed
- Can disable specific home row mods if desired

## Safety & Backup

### Backup Created
- Original layout backed up as: `nuphy_air60_v2_backup_[timestamp].layout.json`
- Can always revert to original configuration

### Non-Destructive Design
- **Layers 0, 1, 7 completely preserved**
- Your existing workflow remains intact
- Practice layers are additional, not replacement

## Resources

### Documentation References
- [Precondition's Home Row Mods Guide](https://precondition.github.io/home-row-mods)
- [Miryoku Layout](https://github.com/manna-harbour/miryoku)
- [QMK Home Row Mods Documentation](https://docs.qmk.fm/#/mod_tap)

### Community
- r/ErgoMechKeyboards subreddit
- QMK Discord community
- Miryoku discussions

## Troubleshooting

### Common Issues
1. **Accidental modifiers while typing**
   - Solution: Practice faster, lighter taps
   - Check: Are you lifting fingers quickly enough?

2. **Modifiers not activating**
   - Solution: Hold keys slightly longer
   - Check: Using opposite hands for combinations?

3. **Inconsistent behavior**
   - Solution: Practice consistent timing
   - Check: Finger placement and pressure

### Getting Help
- Check VIA/Vial settings
- Verify correct layer activation
- Practice on simple text before complex shortcuts

## Next Steps

1. **Week 1**: Focus on basic letter typing with swift taps
2. **Week 2**: Add simple shortcuts (Ctrl+C, Ctrl+V)
3. **Week 3**: Practice navigation and text selection
4. **Week 4**: Advanced shortcuts and layer switching

Remember: Home row mods take time to master. Be patient and focus on building consistent muscle memory through regular practice!

---

**Created**: $(date)  
**Layout Version**: Home Row Mods Practice v1.0  
**Based on**: Miryoku GACS layout principles
