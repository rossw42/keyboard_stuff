# Minivan Improved Layout

An enhanced Vial keyboard layout for the Minivan 40% keyboard with advanced tap dance, layer management, and developer-focused shortcuts.

### Base Layer (Layer 0)
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│GrEsc│  Q  │  W  │  E  │  R  │  T  │  Y  │  U  │  I  │  O  │  P  │ Bsp │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│Tb/Sf│  A  │  S  │  D  │  F  │  G  │  H  │  J  │  K  │  L  │  ;  │ Ent │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│Shift│ Z/⌘Z│ X/⌘X│ C/⌘C│ V/⌘V│  B  │  N  │  M  │ ,/[ │ ./] │  ↑  │  '  │
├─────┼─────┼─────┼─────┴─────┼─────┴─────┼─────┼─────┼─────┼─────┼─────┤
│Ctrl │ Alt │ L3/⌘│   L1/Sp   │   L2/Sp   │   RSft    │  ←  │  ↓  │  →  │
└─────┴─────┴─────┴───────────┴───────────┴─────┴─────┴─────┴─────┴─────┘
```
- **QWERTY layout** with strategic modifications
- **Grave Escape** (`KC_GESC`) - Tap for Escape, Shift+Tap for Grave
- **Mod-tap Tab/Shift** (`RSFT_T(KC_TAB)`) - Tap for Tab, Hold for Right Shift
- **Enhanced tap dance functionality**:
  - Comma key: `,` on tap, `[` on double tap
  - Dot key: `.` on tap, `]` on double tap
  - Z/X/C/V keys with integrated undo/cut/copy/paste shortcuts
- **Optimized thumb cluster** with layer-tap combinations
- **Direct arrow keys** in bottom right for navigation
- **Delete key** easily accessible on base layer

### Layer 1 - Numbers & Symbols
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│  `  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │  9  │  0  │ Bsp │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│  ~  │  !  │  @  │  #  │  $  │  %  │  ^  │  &  │  *  │  (  │  )  │  |  │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │     │  -  │  =  │  [  │  ]  │  \  │     │
├─────┼─────┼─────┼─────┴─────┼─────┴─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │           │           │           │     │     │     │
└─────┴─────┴─────┴───────────┴───────────┴─────┴─────┴─────┴─────┴─────┘
```
- **Numbers 1-0** on top row with grave and backspace
- **Shifted symbols** `~ ! @ # $ % ^ & * ( ) |` on home row
- **Common punctuation** `- = [ ] \` easily accessible
- Accessed via `LT1(KC_SPACE)` (left thumb)

### Layer 2 - Functions & Navigation  
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│  ~  │ F1  │ F2  │ F3  │ F4  │ F5  │ F6  │ F7  │ F8  │ F9  │ F10 │ F11 │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │     │  ←  │  ↓  │  ↑  │  →  │     │ F12 │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │     │     │     │     │     │PgUp │     │
├─────┼─────┼─────┼─────┴─────┼─────┴─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │           │           │     │     │Home │PgDn │ End │
└─────┴─────┴─────┴───────────┴───────────┴─────┴─────┴─────┴─────┴─────┘
```
- **Function keys F1-F12** across top rows
- **Arrow key navigation** in home row position
- **Page navigation** Home/PgUp/PgDn/End in bottom right
- Accessed via `LT2(KC_SPACE)` (right thumb)

### Layer 3 - Developer Shortcuts & Media Control
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│     │     │ ⌘W  │     │ ⌘R  │ ⌘T  │     │     │     │     │     │Mute │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │ ⌘A  │ ⌘S  │     │ ⌘F  │     │     │     │     │     │⌘←   │⌘→   │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │     │     │     │     │MBtn1│  ↑  │MBtn2│
├─────┼─────┼─────┼─────┴─────┼─────┴─────┼─────┼─────┼─────┼─────┼─────┤
│     │     │     │    Vol-   │    Vol+   │    Mute   │Home │  ↓  │ End │
└─────┴─────┴─────┴───────────┴───────────┴─────┴─────┴─────┴─────┴─────┘
```
- **Developer shortcuts** strategically placed:
  - W: Ctrl+W (Close Tab), R: Ctrl+R (Reload), T: Ctrl+T (New Tab)
  - A: Ctrl+A (Select All), S: Ctrl+S (Save), F: Ctrl+F (Find)
  - Ctrl+Left/Right for word navigation
- **Mouse controls**: Left/Right click buttons
- **Media controls**: Volume Down/Up, Mute
- **Navigation**: Home/End keys
- Accessed via `LT3(KC_LGUI)` (left thumb)

## Advanced Features

### Tap Dance Definitions

| Key | Single Tap | Double Tap | Hold | Triple Tap | Function |
|-----|------------|------------|------|------------|----------|
| TD(0) | `,` | `[` | - | Copy | Comma/Left Bracket/Copy |
| TD(1) | `.` | `]` | MO(3) | Paste | Dot/Right Bracket/Layer3/Paste |
| TD(2) | `←` | - | Copy | - | Left Arrow/Copy |
| TD(3) | `→` | MO(3) | Paste | - | Right Arrow/Layer3/Paste |
| TD(4) | Z | Ctrl+Z | - | - | Z/Undo |
| TD(5) | X | Ctrl+X | - | - | X/Cut |
| TD(6) | C | Ctrl+C | - | - | C/Copy |
| TD(7) | V | Ctrl+V | - | - | V/Paste |

### Encoder Support
- **Layer 0**: Basic encoder functionality
- **Layer 1**: Ctrl+Encoder for enhanced control
- **Layer 2**: Shift+Encoder for alternative functions  
- **Layer 3**: Ctrl+Shift+Encoder for advanced operations

### Layer Access Summary
- **Layer 1** (Numbers/Symbols): `LT1(KC_SPACE)` - Left space key
- **Layer 2** (Functions/Navigation): `LT2(KC_SPACE)` - Right space key  
- **Layer 3** (Developer/Media): `LT3(KC_LGUI)` - Left GUI key

### Configuration Details
- **Vial Protocol**: Version 4
- **VIA Protocol**: Version 9
- **Layout Options**: 4 different configurations supported
- **Tap Dance Timing**: 200ms for all tap dance keys
