# Unify Workflow Concept

## What It Does

Takes a **single half** of a split keyboard and creates a **unified keyboard** by mirroring and positioning.

## Visual Concept

```
INPUT: Single Half
┌─────────────┐
│ ⌨ ⌨ ⌨ ⌨ ⌨ 🔌│  Left Half PCB (🔌 = MCU/TRRS)
│ ⌨ ⌨ ⌨ ⌨ ⌨ 🔌│
│ ⌨ ⌨ ⌨ ⌨ ⌨ 🔌│
└─────────────┘
 Pinky    MCU

         ↓ MIRROR + POSITION

OUTPUT: Unified Keyboard
┌─────────────┐   ←gap→   ┌─────────────┐
│ ⌨ ⌨ ⌨ ⌨ ⌨ 🔌│           │🔌 ⌨ ⌨ ⌨ ⌨ ⌨ │
│ ⌨ ⌨ ⌨ ⌨ ⌨ 🔌│           │🔌 ⌨ ⌨ ⌨ ⌨ ⌨ │
│ ⌨ ⌨ ⌨ ⌨ ⌨ 🔌│           │🔌 ⌨ ⌨ ⌨ ⌨ ⌨ │
└─────────────┘           └─────────────┘
  Left Half                 Right Half
  Pinky→MCU                 MCU→Pinky
                           (mirrored)

MCUs/TRRS on outside edges, pinkies on outside
```

## With Splay (Ergonomic Tilt)

```
OUTPUT: Unified Keyboard with 5° Splay
    ┌─────────────┐             ┌─────────────┐
   ╱  ⌨ ⌨ ⌨ ⌨ ⌨  │           │  ⌨ ⌨ ⌨ ⌨ ⌨  ╲
  ╱   ⌨ ⌨ ⌨ ⌨ ⌨  │           │  ⌨ ⌨ ⌨ ⌨ ⌨   ╲
 ╱    ⌨ ⌨ ⌨ ⌨ ⌨  │           │  ⌨ ⌨ ⌨ ⌨ ⌨    ╲
└─────────────────┘           └─────────────────┘
 ↖ 5° outward                      5° outward ↗
```

## Parameters Explained

### Gap
Distance between the two halves:
- **Small (10-15mm)**: Compact, laptop-like
- **Medium (15-20mm)**: Comfortable, balanced
- **Large (20-25mm)**: Spacious, ergonomic

### Splay
Outward rotation angle for ergonomics:
- **0°**: No rotation, traditional layout
- **3-5°**: Subtle improvement, natural hand position
- **7-10°**: Aggressive ergonomic positioning

### Vertical Offset
Stagger between halves:
- **0mm**: Symmetric, aligned
- **5-10mm**: Columnar stagger effect
- **15mm+**: Extreme offset (experimental)

## Transformation Steps

1. **Load** the single half PCB
   ```
   Input: left_half.step
   ```

2. **Mirror** across YZ plane
   ```
   Creates: right_half (flipped)
   ```

3. **Position** both halves
   ```
   Left:  translate(-gap/2, 0, 0) + rotate(-splay)
   Right: translate(+gap/2, 0, 0) + rotate(+splay)
   ```

4. **Union** geometries
   ```
   Combined: left_half ∪ right_half
   ```

5. **Generate** unified case
   ```
   Output: bottom_tray + switch_plate
   ```

## Real-World Example

### Corne Keyboard
- Original: 2 separate halves, 6 columns each
- Unified: 1 keyboard, 12 columns total
- Gap: 18mm (comfortable spacing)
- Splay: 5° (ergonomic tilt)
- Result: Unified Corne with ergonomic positioning

### Dimensions
```
Original Half:  ~120mm wide
Gap:            18mm
Unified Total:  ~258mm wide

Fits on: 300mm+ printer bed
```

## Use Cases

1. **Prototype Testing**
   - Try unified version before committing to split
   - Test different gap/splay combinations
   - Find optimal ergonomic settings

2. **Travel Keyboard**
   - Single piece, easier to transport
   - No TRRS cable needed
   - More compact than split setup

3. **Desk Space**
   - Fixed positioning, no adjustment needed
   - Cleaner desk setup
   - Integrated design

4. **Custom Builds**
   - Create unique layouts from split designs
   - Experiment with ergonomics
   - Personalized keyboard geometry

## Comparison

| Feature | Split Keyboard | Unified Keyboard |
|---------|---------------|------------------|
| Portability | Two pieces | One piece |
| Adjustability | Fully adjustable | Fixed position |
| Cable | TRRS cable needed | No cable |
| Ergonomics | Maximum flexibility | Fixed ergonomics |
| Desk Space | More space needed | Compact |
| Build Complexity | Two builds | One build |

## When to Use Unify

✅ **Good for:**
- Testing unified versions of split designs
- Creating travel keyboards
- Simplifying builds
- Fixed ergonomic positioning
- Cleaner desk setup

❌ **Not ideal for:**
- Maximum adjustability needs
- Extreme ergonomic requirements
- Very wide keyboards (printer bed limits)
- Tenting/tilting setups
