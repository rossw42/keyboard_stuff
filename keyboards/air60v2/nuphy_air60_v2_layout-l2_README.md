# NuPhy Air60 V2 - Advanced Multi-Layer Layout with Home Row Mods

## Overview

This is a comprehensive 8-layer keyboard layout featuring home row modifiers, RGB controls, media functions, mouse integration, and a powerful layer-switching system. The layout emphasizes efficiency and ergonomics while maintaining full compatibility with standard typing.

## Layer Architecture

### Universal Layer Access
- **Space Bar**: `LT(7,KC_SPC)` on ALL layers - Hold space to access Layer 7 (Control Hub)
- **Layer 7**: Acts as a "Control Hub" with direct toggles to all other layers
- **Number Row (Layer 7)**: Direct layer toggles - press number to switch to that layer

## Layer Breakdown

### Layer 0: Base QWERTY
**Theme**: Standard typing layer
- Standard QWERTY layout for normal typing
- One-Shot Modifiers (OSM) for efficient modifier use
- **Space**: Hold for Layer 7, tap for space
- **Fn Key**: Access Layer 1

**Key Features**:
- `OSM(MOD_LSFT)` - One-shot left shift
- `OSM(MOD_LCTL)` - One-shot control
- `OSM(MOD_LGUI)` - One-shot GUI/Windows key
- `OSM(MOD_LALT)` - One-shot Alt
- Mod-tap arrows with shift on arrow cluster

### Layer 1: Function Layer
**Theme**: F-keys and system functions
- F1-F12 on number row
- Audio controls (Mute, Volume Up/Down)
- Custom macros and functions
- **Space**: Hold for Layer 7, tap for space

**Key Features**:
- Complete F-key access
- `CUSTOM(3)`, `CUSTOM(4)`, `CUSTOM(5)`, `CUSTOM(2)` - Custom functions
- Volume controls on right side
- `MACRO(10)` - Custom macro

### Layer 2: Home Row Mods (CASG Order)
**Theme**: Ergonomic home row modifiers with CASG layout
- **Left Hand**: Ctrl, Alt, Shift, GUI (CASG)
- **Right Hand**: GUI, Shift, Alt, Ctrl
- F1-F12 on number row
- **Space**: Hold for Layer 7, tap for space

**Home Row Mapping**:
- `A` = `MT(MOD_LCTL,KC_A)` - Ctrl when held, A when tapped
- `S` = `MT(MOD_LALT,KC_S)` - Alt when held, S when tapped  
- `D` = `MT(MOD_LSFT,KC_D)` - Shift when held, D when tapped
- `F` = `MT(MOD_LGUI,KC_F)` - GUI when held, F when tapped
- `J` = `MT(MOD_LGUI,KC_J)` - GUI when held, J when tapped
- `K` = `MT(MOD_LSFT | MOD_RSFT,KC_K)` - Both Shift when held, K when tapped
- `L` = `MT(MOD_LALT,KC_L)` - Alt when held, L when tapped
- `;` = `MT(MOD_LCTL | MOD_RCTL,KC_SCLN)` - Both Ctrl when held, ; when tapped

### Layer 3: Clean QWERTY
**Theme**: Pure QWERTY without modifications
- Standard QWERTY layout
- Clean typing experience
- Standard modifier keys
- **Space**: Hold for Layer 7, tap for space

### Layer 4: Extended Function Layer
**Theme**: Advanced F-keys and RGB introduction
- F1-F12 on number row
- RGB speed controls (`RGB_SPD`, `RGB_SPI`)
- RGB brightness (`RGB_VAI`)
- Custom functions (`CUSTOM(19)`, `CUSTOM(20)`, `CUSTOM(21)`)
- **Space**: Hold for Layer 7, tap for space
- Access to Layer 5 and 6 for deeper RGB control

### Layer 5: Media Control Layer
**Theme**: System media and display controls
- **Brightness**: `KC_BRID` (F1), `KC_BRIU` (F2)
- **Media Keys**: Previous, Play/Pause, Next, Mute, Volume
- Advanced RGB controls
- Custom macro (`CUSTOM(22)`)
- **Space**: Hold for Layer 7, tap for space

**Media Key Layout**:
- `KC_MPRV` (F7) - Previous track
- `KC_MPLY` (F8) - Play/Pause
- `KC_MNXT` (F9) - Next track
- `KC_MUTE` (F10) - Mute
- `KC_VOLD` (F11) - Volume down
- `KC_VOLU` (F12) - Volume up

### Layer 6: RGB Control Center
**Theme**: Comprehensive RGB lighting control
- **RGB Modes**: Plain, Breathe, Rainbow, Snake, Knight, Christmas, Static Gradient
- **RGB Adjustments**: Hue, Saturation, Value, Speed
- **RGB Navigation**: Mode forward/backward, toggle
- Custom lighting functions
- **Space**: Hold for Layer 7, tap for space

**RGB Mode Layout (Number Row)**:
- `RGB_M_P` (1) - Plain mode
- `RGB_M_B` (2) - Breathe mode  
- `RGB_M_R` (3) - Rainbow mode
- `RGB_M_SW` (4) - Snake mode
- `RGB_M_SN` (5) - Knight mode
- `RGB_M_K` (6) - Christmas mode
- `RGB_M_X` (7) - Static gradient mode
- `RGB_M_G` (8) - Static gradient mode

**RGB Controls**:
- `RGB_TOG` (Backspace) - Toggle RGB
- `RGB_VAI` (0), `RGB_VAD` (-) - Brightness up/down
- `RGB_HUI` (`]`), `RGB_HUD` (`[`) - Hue adjustment
- `RGB_MOD` (`L`), `RGB_RMOD` (`;`) - Mode forward/back
- `RGB_SPI` (Right), `RGB_SPD` (Left) - Speed adjustment
- `RGB_SAI` (Up), `RGB_SAD` (Down) - Saturation adjustment

### Layer 7: Control Hub (Momentary)
**Theme**: Navigation, layer switching, mouse control, and utilities
- **Direct Layer Access**: Numbers 1-6 toggle to respective layers
- **Navigation**: Arrow keys, Home/End, Page Up/Down via mouse wheel
- **Mouse Control**: Full mouse movement and clicking
- **Utility Functions**: Macros, special functions
- **Always accessible**: Hold Space from any layer

**Layer Toggle Layout (Number Row)**:
- `TO(1)` (1) - Switch to Layer 1
- `TO(2)` (2) - Switch to Layer 2  
- `TO(3)` (3) - Switch to Layer 3
- `TO(4)` (4) - Switch to Layer 4
- `TO(5)` (5) - Switch to Layer 5
- `TO(6)` (6) - Switch to Layer 6
- `TO(0)` (Esc) - Return to base layer

**Navigation Cluster**:
- `KC_HOME` (Q), `KC_UP` (W), `KC_END` (E) - Navigation
- `KC_LEFT` (A), `KC_DOWN` (S), `KC_RGHT` (D) - Arrow keys

**Mouse Controls**:
- `KC_MS_LEFT` (H), `KC_MS_DOWN` (J), `KC_MS_UP` (K), `KC_MS_RIGHT` (L) - Mouse movement
- `KC_MS_BTN1` (I) - Left click
- `KC_MS_BTN2` (P) - Right click  
- `KC_MS_BTN3` (O) - Middle click
- `KC_MS_WH_UP` (Up arrow) - Mouse wheel up
- `KC_MS_WH_DOWN` (Down arrow) - Mouse wheel down
- `KC_MS_WH_LEFT` (Left arrow) - Mouse wheel left
- `KC_MS_WH_RIGHT` (Right arrow) - Mouse wheel right

**Utilities**:
- `MACRO(10)` (=) - Custom macro
- `MACRO(11)` (Enter) - Custom macro  
- `CUSTOM(21)` (Fn) - Custom function

## Usage Guide

### Quick Layer Access
1. **Hold Space** from any layer to access Layer 7
2. **Press number 1-6** in Layer 7 to switch to that layer  
3. **Press Esc** in Layer 7 to return to Layer 0

### Home Row Mods (Layer 2)
1. Switch to Layer 2: Space → 2
2. **Tap** home row keys normally for letters
3. **Hold** home row keys for modifiers:
   - Hold `A` + tap `C` = Ctrl+C (copy)
   - Hold `D` + tap `V` = Shift+V (shift+V)
   - Hold `F` + tap `T` = GUI+T (Windows+T, task view)

### RGB Control (Layer 6)
1. Switch to Layer 6: Space → 6  
2. Use number row for RGB modes
3. Use various keys for hue, brightness, saturation control
4. Press Backspace to toggle RGB on/off

### Media Control (Layer 5)
1. Switch to Layer 5: Space → 5
2. Use F7-F12 for media controls
3. Use F1-F2 for brightness
4. Access advanced RGB controls

## Advanced Features

### One-Shot Modifiers (Layer 0)
- Tap once to "arm" the modifier
- Next key press applies the modifier
- Great for single modifier+key combinations
- No need to hold down modifier keys

### Multi-Modal Design
- **Layer 0**: Daily typing with one-shot mods
- **Layer 2**: Power user home row mods  
- **Layer 3**: Clean fallback layer
- **Layer 7**: Command center for everything

### Mouse Integration
- Full mouse control from Layer 7
- Eliminates need to reach for mouse for basic tasks
- Scroll wheel control for document navigation
- Three mouse buttons for complete mouse replacement

## Tips for Success

### Home Row Mods (Layer 2)
- **Swift taps**: Type letters with quick, light taps
- **Deliberate holds**: Hold modifiers with intention
- **Opposite hands**: Use left mods with right-hand keys and vice versa
- **Practice gradually**: Start with simple shortcuts like Ctrl+C, Ctrl+V

### Layer Management
- **Space as hub**: Remember Space is your gateway to Layer 7
- **Number shortcuts**: Memorize 1-6 for quick layer switching
- **Escape home**: Use Esc in Layer 7 to return to base layer
- **Context switching**: Use appropriate layer for each task

### RGB Customization
- **Mode experimentation**: Try different RGB modes from Layer 6
- **Brightness adjustment**: Set comfortable brightness levels
- **Speed tuning**: Adjust animation speeds to preference
- **Toggle quickly**: Use Backspace in Layer 6 to toggle RGB

## Customization Notes

### Macros Available
- `MACRO(10)`: "2001honda" - Custom text macro
- `MACRO(11)`: "42FatHead42!!" + Enter - Login macro
- Various `CUSTOM()` functions for extended functionality

### Layer-Specific Features
- **All layers**: Space acts as Layer 7 momentary access
- **Consistent navigation**: Layer 7 always provides same controls
- **RGB throughout**: RGB controls accessible from multiple layers
- **Media integration**: Dedicated media layer with full controls

## Troubleshooting

### Home Row Mods Issues
- **Accidental modifiers**: Tap faster, lighter pressure
- **Missing modifiers**: Hold keys longer, ensure opposite hand usage
- **Inconsistent behavior**: Check layer - ensure you're on Layer 2

### Layer Switching Problems  
- **Can't switch layers**: Hold Space to access Layer 7 first
- **Stuck in layer**: Use Esc in Layer 7 to return to Layer 0
- **Forgot current layer**: Use Layer 7 number row to reset

### RGB Not Working
- **No RGB response**: Toggle RGB with Backspace in Layer 6
- **Wrong colors**: Adjust hue with `[` and `]` in Layer 6
- **Too bright/dim**: Use `0` and `-` in Layer 6 for brightness

This layout represents a sophisticated approach to keyboard customization, providing multiple workflows for different use cases while maintaining consistency and accessibility across all layers.
