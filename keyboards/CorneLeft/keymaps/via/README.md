# VIA Keymap for Cities Skylines 2 - Corne Left Macropad

This directory contains the VIA-compatible keymap configuration for the Corne Left keyboard configured as a Cities Skylines 2 macropad.

## Files

- `keymap.json` - VIA configuration file with complete keymap layout

## What is VIA?

VIA is a graphical interface for configuring QMK keyboards in real-time without needing to reflash the firmware. It allows you to:
- Remap keys instantly
- Create and modify layers
- Set up macros
- Customize lighting
- Save multiple keymap profiles

## How to Use This Keymap

### 1. Enable VIA Support in QMK

First, ensure your QMK firmware is compiled with VIA support. Add these to your `rules.mk`:

```make
VIA_ENABLE = yes
```

### 2. Load the Keymap in VIA

1. Download and install VIA from https://usevia.app/ or https://github.com/the-via/releases
2. Connect your keyboard via USB
3. Open VIA application
4. If your keyboard isn't automatically detected, load the `keymap.json` file:
   - Go to Settings (gear icon)
   - Enable "Show Design tab"
   - Go to Design tab
   - Click "Load" and select `keymaps/via/keymap.json`

### 3. Configure Your Layout

Once loaded, you can:
- Click any key to remap it
- Switch between layers using the layer dropdown
- Test keys in real-time
- Export/import your custom layouts

## Layer Structure

### Layer 0: Movement & Building Tools (Blue)
- **WASD Movement**: Standard game movement controls
- **Building Tools**: O (Auto Connect), C (Clone), M (Move Selected)
- **Quick Actions**: Tab (Next Tool), Enter (Confirm), Delete, B (Bulldozer)
- **Modifiers**: Ctrl (Straight), Shift (Snap Toggle), Alt (Curved)
- **Layer Access**: Hold first thumb key to access Zoom layer

### Layer 1: Zoom & Camera Controls (Green)
- **Zoom**: R (Zoom In), F (Zoom Out)
- **Camera**: Q (Cam Left), E (Cam Right)
- **Elevation**: PgUp (Up), PgDn (Down)
- **Alignment**: X (Align X), Y (Align Y), L (Align Z)
- **Layer Access**: Hold second thumb key to access Roads layer

### Layer 2: Roads & Advanced Tools (Yellow)
- **Road Tools**: H (Hide/Show UI), N (Node Tool), T (Grid Toggle)
- **Advanced**: G (Guides), J (Junction), K (Kerb Tool)
- **Map Tools**: F2 (Move It), F3 (Anarchy), F4 (Precision)
- **Functions**: I (Intersect), V (Vehicle), P (Path Tool)
- **Edit Tools**: Ins (Insert Node), Home (Start Point), End (End Point)
- **Adjust**: = (Increase), - (Decrease), Backspace (Undo Last)
- **Layer Access**: Hold third thumb key to access Building layer

### Layer 3: Building & Zoning (Red)
- **Zoning**: 1-6 (Residential, Commercial, Industrial, Office, Mixed Use, Roads)
- **Infrastructure**: 7-9 (Public Transport, Utilities, Parks & Rec)
- **Services**: 0 (Services)
- **Brush Control**: [ (Decrease Brush), ] (Increase Brush)
- **System**: F5 (Save), F9 (Load), F10 (Screenshot), F11 (Fullscreen), F12 (Console)
- **UI**: ` (Hide UI)

## Color Coding

The keymap uses color coding to help identify layers:
- **Blue (#4a90e2)**: Layer 0 - Movement & Building Tools
- **Green (#7ed321)**: Layer 1 - Zoom & Camera Controls  
- **Yellow**: Layer 2 - Roads & Advanced Tools (conceptual)
- **Red**: Layer 3 - Building & Zoning (conceptual)
- **Gray (#cccccc)**: Transparent/Empty keys

## Technical Details

- **Vendor ID**: 0x4653
- **Product ID**: 0x0001
- **Matrix**: 4 rows × 6 columns
- **Total Keys**: 21 keys (18 main + 3 thumb)
- **Layout**: LAYOUT_split_3x6_3 (Corne left half only)

## Customization

You can customize this keymap by:
1. Loading it in VIA
2. Making your changes in the VIA interface
3. Exporting the modified layout from VIA
4. Saving it back to this directory

## Related Files

- `../../keymap.c` - Source QMK C code
- `../../vial-keymap.json` - Vial-specific configuration with macros
- `../../cities-skylines-2-keymap.yaml` - YAML configuration for visualization

## Troubleshooting

### Keyboard Not Detected
- Ensure VIA support is enabled in firmware
- Try loading the JSON manually via Design tab
- Check USB connection

### Keys Not Working as Expected
- Verify the correct layer is active
- Check if layer toggle keys are functioning
- Review the keymap.c source for any custom behaviors

### Want to Add Macros?
- VIA supports macros in the Macros tab
- You can record key sequences
- Macros can be assigned to any key

## Contributing

To improve this keymap:
1. Test changes in VIA first
2. Export your improved layout
3. Update the keymap.json file
4. Document changes in this README

## Resources

- [VIA Documentation](https://www.caniusevia.com/docs/specification)
- [QMK VIA Documentation](https://docs.qmk.fm/#/feature_via)
- [Corne Keyboard](https://github.com/foostan/crkbd)
- [Cities Skylines 2](https://www.citiesskylines.com/)
