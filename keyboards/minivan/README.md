# Minivan Layout

A Vial keyboard layout for the Minivan 40% keyboard.

### Base Layer (Layer 0)
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ Esc │  Q  │  W  │  E  │  R  │  T  │  Y  │  U  │  I  │  O  │  P  │ Bsp │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│Tb/Ct│  A  │  S  │  D  │  F  │  G  │  H  │  J  │  K  │  L  │  ;  │ Ent │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│Shift│ Z/⌘Z│ X/⌘X│ C/⌘C│ V/⌘V│  B  │  N  │  M  │ ,/[ │ ./] │  ↑  │  '  │
├─────┼─────┼─────┼─────┴─────┼─────┴─────┼─────┼─────┼─────┼─────┼─────┤
│Ctrl │ Alt │L2/⌘ │   L1/Sp   │   Space   │L3/Sp│L3/Sh│  ←  │  ↓  │  →  │
└─────┴─────┴─────┴───────────┴───────────┴─────┴─────┴─────┴─────┴─────┘
```
- **QWERTY layout** with strategic modifications
- **Mod-tap Tab/Ctrl** (`LCTL_T(KC_TAB)`) - Tap for Tab, Hold for Ctrl
- **Tap dance punctuation**:
  - Comma key: `,` on tap, `[` on double tap
  - Dot key: `.` on tap, `]` on double tap
- **Tap dance Z/X/C/V** with undo/cut/copy/paste shortcuts
- **Direct arrow keys** in bottom right for navigation
- **Layer access** via thumb keys

### Layer 1 - Numbers & Symbols
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│  `  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │  9  │  0  │ Bsp │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│  ~  │  !  │  @  │  #  │  $  │  %  │  ^  │  &  │  *  │  (  │  )  │  |  │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │     │  -  │  =  │  [  │  ]  │  \  │     │
├─────┼─────┼─────┼─────┴─────┼─────┴─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │           │           │     │     │     │     │     │
└─────┴─────┴─────┴───────────┴───────────┴─────┴─────┴─────┴─────┴─────┘
```
- **Numbers 1-0** on top row with grave and backspace
- **Shifted symbols** `~ ! @ # $ % ^ & * ( ) |` on home row
- **Common punctuation** `- = [ ] \` easily accessible
- Accessed via `LT1(KC_SPACE)` (left thumb)

### Layer 2 - Functions & Vim Navigation  
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│  ~  │ F1  │ F2  │ F3  │ F4  │ F5  │ F6  │ F7  │ F8  │ F9  │ F10 │ F11 │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │     │  ←  │  ↓  │  ↑  │  →  │     │ F12 │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │     │Home │PgDn │PgUp │ End │     │     │
├─────┼─────┼─────┼─────┴─────┼─────┴─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │           │           │     │     │     │     │     │
└─────┴─────┴─────┴───────────┴───────────┴─────┴─────┴─────┴─────┴─────┘
```
- **Function keys F1-F12** across top rows
- **Vim navigation** (H/J/K/L) for Left/Down/Up/Right
- **Page navigation** Home/PgDn/PgUp/End
- Accessed via `LT2(KC_LGUI)` (left thumb)

### Layer 3 - Developer Shortcuts & Mouse Control
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│     │     │ ⌘W  │     │ ⌘R  │ ⌘T  │     │     │     │     │     │Mute │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │ ⌘A  │ ⌘S  │     │ ⌘F  │     │     │     │     │     │⌘←   │⌘→   │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │Home │PgDn │PgUp │ End │     │     │     │     │LClk │WhlU │RClk │
├─────┼─────┼─────┼─────┴─────┼─────┴─────┼─────┼─────┼─────┼─────┼─────┤
│Prev │Play │Next │           │           │     │     │WhlL │WhlD │WhlR │
└─────┴─────┴─────┴───────────┴───────────┴─────┴─────┴─────┴─────┴─────┘
```
- **Developer shortcuts** on left side:
  - W: Ctrl+W (Close Tab), R: Ctrl+R (Reload), T: Ctrl+T (New Tab)
  - A: Ctrl+A (Select All), S: Ctrl+S (Save), F: Ctrl+F (Find)
  - Ctrl+Left/Right for word navigation
- **Mouse controls** on right side:
  - Left/Right click, Mouse wheel in all directions
- **Media controls**: Prev/Play/Next, Mute
- Accessed via `LT3(KC_SPACE)` and `LT3(KC_RSHIFT)`

## Tap Dance Definitions

| Key | Single Tap | Double Tap | Hold | Function |
|-----|------------|------------|------|----------|
| TD(0) | `,` | `[` | - | Comma/Left Bracket |
| TD(1) | `.` | `]` | - | Dot/Right Bracket |
| TD(4) | Z | Ctrl+Z | - | Z/Undo |
| TD(5) | X | Ctrl+X | - | X/Cut |
| TD(6) | C | Ctrl+C | - | C/Copy |
| TD(7) | V | Ctrl+V | - | V/Paste |
