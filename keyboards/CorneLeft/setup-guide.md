# Cities Skylines 2 Corne Left Macropad - Setup Guide

## Overview
This guide will help you set up your Corne keyboard's left side as a dedicated Cities Skylines 2 macropad using either QMK or VIAL firmware.

## Prerequisites

### Hardware Required
- Corne (CRKBD) keyboard with left side only
- USB-C cable
- Computer with QMK/VIAL software

### Software Required
- **Option A**: [QMK Toolbox](https://github.com/qmk/qmk_toolbox) + QMK CLI
- **Option B**: [VIAL](https://get.vial.today/) (Recommended for beginners)

## Setup Methods

### Method 1: VIAL Setup (Recommended)

#### Step 1: Install VIAL
1. Download VIAL from [get.vial.today](https://get.vial.today/)
2. Install the application for your operating system

#### Step 2: Flash VIAL Firmware
1. Put your Corne into bootloader mode (usually double-tap reset button)
2. Download the VIAL-compatible Corne firmware
3. Flash using VIAL or QMK Toolbox

#### Step 3: Import Keymap
1. Open VIAL application
2. Connect your Corne keyboard
3. Import the `vial-keymap.json` file from this project
4. The keymap will be automatically applied

#### Step 4: Customize Macros
1. Navigate to the Macros tab in VIAL
2. Edit the pre-configured macros or add your own
3. Test each macro in Cities Skylines 2

### Method 2: QMK Setup (Advanced)

#### Step 1: Install QMK
```bash
# Install QMK CLI
pip3 install qmk

# Setup QMK environment
qmk setup
```

#### Step 2: Create Keymap Directory
```bash
# Navigate to QMK keyboards directory
cd ~/qmk_firmware/keyboards/crkbd/keymaps/

# Create your keymap directory
mkdir cities_skylines_2
cd cities_skylines_2
```

#### Step 3: Copy Keymap Files
1. Copy the `keymap.c` file to your keymap directory
2. Create a `rules.mk` file with required features:

```makefile
# rules.mk
MOUSEKEY_ENABLE = yes
EXTRAKEY_ENABLE = yes
CONSOLE_ENABLE = no
COMMAND_ENABLE = no
NKRO_ENABLE = yes
BACKLIGHT_ENABLE = no
AUDIO_ENABLE = no
RGBLIGHT_ENABLE = yes
RGB_MATRIX_ENABLE = no
```

#### Step 4: Compile and Flash
```bash
# Compile the firmware
qmk compile -kb crkbd -km cities_skylines_2

# Flash to keyboard (put in bootloader mode first)
qmk flash -kb crkbd -km cities_skylines_2
```

## Layer Configuration

### Layer 0: CAMERA & MOVEMENT (Blue LED)
**Default layer for camera controls and basic navigation**
- Most frequently used shortcuts
- WASD movement, camera rotation (TQEG), zoom (RF)
- Quick access to info panels (IPCVX)

### Layer 1: SPEED & TOOLS (Green LED)
**Game speed and building tools**
- Speed controls (1,2,3)
- Save/Load (F5,F9)
- UI toggle, elevation controls
- Photo mode access

### Layer 2: EDITOR TOOLS (Yellow LED)
**Advanced editor functions**
- Clone, auto-connect, alignment tools
- Precise building controls
- Editor-specific shortcuts

### Layer 3: MACROS & CUSTOM (Red LED)
**Programmable macros for complex actions**
- 18 customizable macro keys
- Pre-configured building sequences
- Camera presets and tool combinations

## Pre-Configured Macros

### Macro 1: Quick Road Placement
- Selects road tool → Places road → Auto-connects

### Macro 2: Residential Zone + Utilities
- Places residential zone → Connects utilities

### Macro 3: Camera Reset
- Focuses on city center → Adjusts zoom

### Macro 4: Quick Save + Pause
- Saves game → Pauses simulation

### Macro 5: Economy Overview
- Cycles through economy → city info → statistics

### Macro 6: Photo Mode Setup
- Hides UI → Enters photo mode

## Customization Tips

### Adding New Macros
1. **VIAL Users**: Use the Macros tab to record or type new sequences
2. **QMK Users**: Edit the `process_record_user()` function in `keymap.c`

### Macro Syntax Examples
```
Simple key: {KC_A}
Key combination: {KC_LCTL,KC_C}
Sequence: {KC_A}{KC_B}{KC_C}
With delays: {KC_A}{KC_B,200}{KC_C}
Mouse click: {+KC_LCLK,-KC_LCLK}
```

### RGB Layer Indication
- **Blue**: Camera/Movement layer
- **Green**: Speed/Tools layer  
- **Yellow**: Editor layer
- **Red**: Macros layer

## Troubleshooting

### Keyboard Not Detected
1. Check USB connection
2. Try different USB port
3. Ensure keyboard is in bootloader mode for flashing

### Macros Not Working
1. Test individual keys first
2. Check macro syntax
3. Verify game is in focus
4. Adjust delay timings if needed

### Layer Switching Issues
1. Confirm thumb key assignments
2. Test layer indicators (RGB)
3. Check for conflicting keybinds

## Game-Specific Setup

### In Cities Skylines 2
1. Go to Settings → Controls
2. Verify default keybindings match the keymap
3. Disable any conflicting shortcuts
4. Test each layer systematically

### Recommended Game Settings
- Enable keyboard shortcuts
- Disable mouse edge scrolling (conflicts with WASD)
- Set appropriate camera sensitivity
- Configure auto-save intervals

## Advanced Customization

### Creating Building Sequences
Example macro for complete residential block:
```
1. Select residential tool
2. Place zone
3. Connect road
4. Add utilities
5. Zone additional plots
```

### Camera Presets
Save specific camera angles for:
- City overview
- Traffic monitoring
- Construction areas
- Problem zones

### Tool Combinations
Combine multiple tools for efficiency:
- Bulldoze → Rebuild → Connect
- Zone → Utilities → Services
- Road → Intersection → Traffic lights

## Maintenance

### Firmware Updates
- Check for VIAL/QMK updates monthly
- Backup your keymap before updating
- Test all functions after updates

### Keymap Backups
- Export VIAL configuration regularly
- Keep copies of custom `keymap.c` files
- Document any custom macros

## Support Resources

- [QMK Documentation](https://docs.qmk.fm/)
- [VIAL Manual](https://get.vial.today/manual/)
- [Corne Keyboard Guide](https://github.com/foostan/crkbd)
- [Cities Skylines 2 Community](https://www.reddit.com/r/CitiesSkylines/)

## Contributing

Found improvements or new macro ideas? Feel free to:
1. Test new configurations
2. Share useful macro combinations
3. Report any issues or bugs
4. Suggest layout optimizations

Happy city building! 🏙️