# NuPhy Air60 V2 - One Shot Enhanced Layout

This layout builds upon the base Air60 V2 configuration with advanced QMK features inspired by the Air75 V2 oneshot layout, focusing on one-shot keys and better layer switching strategies adapted for the 60% form factor.

## Key Features

### 🎯 One Shot Modifiers (OSM)
One shot modifiers stay active until the next key is pressed, allowing you to type combinations without holding keys:

- **Left Shift**: `OSM(MOD_LSFT)` - Bottom left corner
- **Right Shift**: `OSM(MOD_RSFT)` - Bottom right shift key  
- **Left Ctrl**: `OSM(MOD_LCTL)` - Bottom left modifier row
- **Right Alt**: `OSM(MOD_LALT | MOD_RALT)` - Bottom right modifier row
- **Left GUI**: `OSM(MOD_LGUI)` - Bottom left modifier row
- **Left Alt**: `OSM(MOD_LALT)` - Bottom left modifier row

**Example**: Press Left Shift once, release, then press 'A' → types 'A' (capital)

### 🎛️ Mod-Tap Keys (MT)
Keys that act as normal keys when tapped, modifiers when held:

- **Caps Lock**: `MT(MOD_LCTL,KC_CAPS)` - Tap for Caps, Hold for Left Ctrl
- **Up Arrow**: `MT(MOD_LSFT,KC_UP)` - Tap for Up, Hold for Left Shift
- **Left Arrow**: `MT(MOD_LCTL,KC_LEFT)` - Tap for Left, Hold for Left Ctrl
- **Down Arrow**: `MT(MOD_LALT,KC_DOWN)` - Tap for Down, Hold for Left Alt
- **Right Arrow**: `MT(MOD_LGUI,KC_RGHT)` - Tap for Right, Hold for Left GUI 

### 🌐 Layer Tap (LT)
- **Spacebar**: `LT(7,KC_SPC)` - Tap for Space, Hold for Layer 7 (Navigation & Layer Management)

### 🔄 Enhanced Layer Switching

**🎯 PRIMARY METHOD - Layer 7 (Navigation Hub)**:
- Hold **Spacebar** to access Layer 7, then:
  - **Number 1-6**: Layer management (toggle layers 1-5, reset to 0)
  - **QWER/ASDF**: Navigation cluster
  - **Spacebar + 6**: Emergency reset to Layer 0

**🎮 TRADITIONAL METHODS - Layer 1 (Function)**:
  - `TG(1)` - Toggle Layer 1 on/off (key 1)
  - `TG(2)` - Toggle Layer 2 on/off (key 2)  
  - `TG(3)` - Toggle Layer 3 on/off (key 3)
  - `TG(4)` - Toggle Layer 4 on/off (key 4)
  - `OSL(5)` - One Shot Layer 5 (key 5)
  - `TO(0)` - Return to base layer (key 6)
  - `MO(2)` - Momentary Symbols (key 7)

**🎨 ADVANCED - Layer 5 (RGB/Settings)**:
  - `TT(1)` - Tap-Toggle Layer 1 (key 1) - hold momentary, tap 5x to lock
  - `TT(2)` - Tap-Toggle Layer 2 (key 2)
  - `TT(3)` - Tap-Toggle Layer 3 (key 3)
  - `TT(4)` - Tap-Toggle Layer 4 (key 4)

### 📋 Layer Breakdown

**Layer 0 (Base)**: Standard QWERTY with one shot modifiers  
**Layer 1 (Function)**: Function controls, media keys, macros, layer access  
**Layer 2 (Symbols)**: Shifted number row symbols and brackets  
**Layer 3 (Navigation)**: Arrow cluster navigation and F-keys  
**Layer 4 (RGB)**: RGB lighting controls  
**Layer 5 (Settings)**: Advanced layer controls with tap-toggle  
**Layer 6**: Unused/placeholder layer  
**Layer 7 (Nav Hub)**: **Primary layer management and navigation center**  

### 🚀 Usage Tips

1. **One Shot Workflow**: 
   - Press Shift → release → press letter → get capital
   - Press Ctrl → release → press C → copy
   - No need to hold modifier keys!

2. **🎯 PRIMARY LAYER ACCESS (Hold Spacebar + Number)**:
   - **Spacebar + 1**: Toggle Function Layer (Layer 1)
   - **Spacebar + 2**: Toggle Symbols Layer (Layer 2)
   - **Spacebar + 3**: Toggle Navigation Layer (Layer 3)
   - **Spacebar + 4**: Toggle RGB Layer (Layer 4)
   - **Spacebar + 5**: One Shot Settings Layer (Layer 5)
   - **Spacebar + 6**: **RESET TO BASE LAYER (Layer 0)** 🔑

3. **🧭 NAVIGATION (Hold Spacebar + QWER/ASDF)**:
   - **Spacebar + Q**: Home
   - **Spacebar + W**: Up Arrow
   - **Spacebar + E**: End
   - **Spacebar + R**: Page Up
   - **Spacebar + A**: Left Arrow
   - **Spacebar + S**: Down Arrow
   - **Spacebar + D**: Right Arrow
   - **Spacebar + F**: Page Down

4. **🛟 EMERGENCY LAYER RESET**:
   - **Spacebar + 6**: Always returns to base layer (Layer 0)
   - **Fn + 6**: Redundant reset also available
   - These work from ANY layer state

5. **Modifier Combos**:
   - One shot modifiers can be chained
   - Press Ctrl → press Shift → press letter → get Ctrl+Shift+letter

6. **Alternative Layer Access**:
   - **Fn key**: Access function layer and some toggles
   - **Fn + 7**: Quick access to symbols layer (MO(2))
   - Layer 5 still has TT (tap-toggle) options for advanced users

### 🔄 Built-in Macros

This layout includes several useful macros for quick access to common key combinations:

#### Navigation Macros (Layer 1 - Function Layer)
Access these by holding the **Fn key** (bottom right corner):
- **Fn + Q**: `CUSTOM(3)` - Ctrl+Left Arrow - Move cursor word left
- **Fn + W**: `CUSTOM(4)` - Ctrl+Right Arrow - Move cursor word right
- **Fn + E**: `CUSTOM(5)` - GUI+Left Arrow - Window left (on macOS/Windows)
- **Fn + R**: `CUSTOM(2)` - GUI+Right Arrow - Window right (on macOS/Windows)

#### Text Editing Macros (Layer 1 - Function Layer)
Access these by holding the **Fn key**:
- **Fn + Z**: `MACRO(6)` - Ctrl+Z - Undo
- **Fn + C**: `MACRO(12)` - Ctrl+C - Copy
- **Fn + V**: `MACRO(13)` - Ctrl+V - Paste
- **Fn + X**: `MACRO(14)` - Ctrl+X - Cut
- **Fn + A**: `MACRO(8)` - Ctrl+A - Select All
- **Fn + S**: `MACRO(9)` - Ctrl+S - Save

#### Media Controls (Layer 1 - Function Layer)
Access these by holding the **Fn key**:
- **Fn + 0**: `KC_MUTE` - Mute audio
- **Fn + -**: `KC_VOLD` - Volume down
- **Fn + =**: `KC_VOLU` - Volume up
- **Fn + ,**: `KC_MPRV` - Previous track
- **Fn + .**: `KC_MPLY` - Play/Pause
- **Fn + /**: `KC_MNXT` - Next track

#### RGB Control Macros (Layer 4 - RGB Layer)
Access these by first toggling to Layer 4 (via **Spacebar + 4** or **Fn + 4**):
- **Various Keys**: Control RGB lighting modes, brightness, and effects

#### Accessing Macros
There are three ways to access these macros:
1. **Momentary access**: Hold **Fn key** + the corresponding key
2. **Toggle access**: Press **Spacebar + 1** to toggle to Layer 1, then press the macro key
3. **Tap-toggle access**: From Layer 5, tap the '1' key five times to lock into Layer 1

Most macros are conveniently placed in logical positions (e.g., C for Copy, V for Paste) when in the appropriate layer.

### 🔧 Configuration Notes

- One shot timeout: 5000ms (5 seconds) by default
- Tap-toggle count: 5 taps to lock by default
- All original macros preserved from base layout
- RGB controls maintained in dedicated layer

### 💡 Benefits

- **Reduced finger strain**: No need to hold modifier keys
- **Faster typing**: One shot modifiers eliminate timing issues
- **Better ergonomics**: Less simultaneous key presses
- **Flexible layers**: Multiple ways to access and lock layers
- **Familiar base**: Standard QWERTY layout remains unchanged

### 🧠 Layer Organization Philosophy

This layout uses deliberate duplication between layers to provide multiple access paths to the same functionality, enhancing usability:

1. **Layer 7 as Primary Control Hub**:
   - Accessed by holding spacebar (most ergonomic modifier)
   - Combines navigation and layer management in one place
   - Provides the most frequently used functions in a single, easy-to-access layer

2. **Intentional Duplications**:
   - Navigation cluster appears in both Layer 3 and Layer 7
   - Layer controls appear in both Layer 1 and Layer 7
   - This redundancy ensures functions are accessible from multiple layers

3. **Layer Access Strategy**:
   - **Quick access**: Hold spacebar for temporary Layer 7 access
   - **Traditional toggle**: Use Function layer (Fn key) to toggle layers on/off
   - **Advanced users**: Use Layer 5 for tap-toggle functionality
   - **Emergency reset**: Spacebar+6 or Fn+6 to return to base layer

4. **Layer Structure Logic**:
   - Layer 0 (Base): Daily typing with one-shot modifiers
   - Layer 1-5: Traditional function layers with specific purposes
   - Layer 6: Placeholder for future customization
   - Layer 7: Quick access hub combining the most needed functions

This multi-path approach ensures you're never more than two keystrokes away from any function, while maintaining an intuitive organization.

### 🔄 Adaptation from Air75 V2

This layout adapts the Air75 V2 oneshot layout philosophy to the Air60 V2's 60% form factor:
- Maintained the same layer structure and organization
- Adapted key placements to work within the 60% layout constraints
- Preserved all one-shot modifiers and layer access methods
- Optimized navigation for the smaller keyboard size

### 🏗️ Technical Specifications

- **Compatible with**: VIA, Vial, QMK
- **Layout Format**: JSON keymap
- **One Shot Timeout**: 5000ms default
- **Tap-Toggle Count**: 5 taps to lock

### 📚 QMK Documentation References

- [One Shot Keys](https://docs.qmk.fm/one_shot_keys)
- [Layers](https://docs.qmk.fm/feature_layers)
- [Mod-Tap](https://docs.qmk.fm/mod_tap)
- [Advanced Keycodes](https://docs.qmk.fm/feature_advanced_keycodes)

## ⚠️ Known Issues & Troubleshooting

### Layer Getting Stuck
If you get stuck on a layer and can't return to normal typing:
- **Emergency Reset**: Press `Spacebar + 6` to return to base layer (most reliable)
- **Alternative**: Press `Fn + 6` to return to base layer
- **Backup**: Press `Fn + 1` to toggle layer 1 off if it's stuck
- **Last Resort**: Unplug and reconnect keyboard

### One-Shot Modifiers Not Working
- Make sure you're using quick taps, not holding the keys
- Try tapping the modifier, then immediately tapping the letter
- If stuck with a modifier active, tap that modifier key again to clear it

### 60% Layout Adjustment
- Remember there are no dedicated F-keys, arrow keys, or navigation keys on the base layer
- Use Layer 7 (hold Spacebar) for quick navigation without leaving the home row
- For heavy navigation or function key use, toggle to Layer 3 for a more permanent solution
