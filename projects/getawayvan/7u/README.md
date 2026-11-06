# GetawayVan: 7u spacebar and 2u Right Shift Vial display

This definition fixes the Vial GUI geometry for the stock 7u keymap. It does
not change the matrix wiring, key behavior, USB identity, or Vial UID.

## Review findings

The following files were reviewed on 2026-10-13:

- `D:\GitHub2\vial-qmk\keyboards\esca\getawayvan\keyboard.json`
- `D:\GitHub2\vial-qmk\keyboards\esca\getawayvan\keymaps\7u\keymap.c`
- `D:\GitHub2\vial-qmk\keyboards\esca\getawayvan\keymaps\vial\keymap.c`
- `D:\GitHub2\vial-qmk\keyboards\esca\getawayvan\keymaps\vial\vial.json`
- `D:\GitHub2\vial-qmk\.build\obj_esca_getawayvan_vial\src\default_keyboard.h`

The active Vial keymap was byte-for-byte identical to the stock 7u keymap.
Its base layer has the expected 45 LAYOUT arguments. The old Vial definition
correctly labeled those matrix coordinates, but drew the split-space layout.

## Corrected bottom row

| Matrix position | Width | Compiled base-layer action |
| --- | --- | --- |
| (3,0) | 1u | `KC_LCTL` |
| (3,1) | 1.5u | `KC_LGUI` |
| (3,6) | 7u | `LT(1, KC_SPC)` |
| (3,9) | 1.5u | `MO(2)` |
| (3,11) | 1u | `KC_LALT` |

The row is 12u wide and inset by 0.375u, centering it under the 12.75u
upper rows as in the supplied layout drawing. The upper two rows are
unchanged. Unused bottom-row switches are hidden, not electrically removed.
The spacebar still taps Space and holds layer 1.

## Corrected second-to-bottom row

The third row ends with one 2u Right Shift instead of two 1u keys, matching
the user's installed layout. It starts at x=10.75u and ends at x=12.75u.
The displayed key retains matrix coordinate (2,11), whose compiled base-layer
action is `KC_RSFT`. Coordinate (2,10), assigned `KC_NO` on the compiled base
layer, is hidden. No keymap, matrix pins, or electrical behavior are changed.
The working 7u bottom row is preserved exactly. There are 40 displayed keys.

## Applying the definition

Vial embeds this JSON in firmware; it is not a saved `.vil` keymap and changing
it alone will not update an already-flashed keyboard's display. Rebuild and
flash the Vial target using this definition in a writable working copy of
vial-qmk, keeping the existing Vial keymap, config.h, and rules.mk.

Source definition: `D:\GitHub\keyboard_stuff\projects\getawayvan\7u\vial.json`.
Destination relative to a writable firmware tree:
`keyboards\esca\getawayvan\keymaps\vial\vial.json`.

Build target: `esca/getawayvan:vial` (STM32F072). Do not build the plain `7u`
target if you want Vial support. Confirm the physical MCU first; the F042
variant is a separate target and must not be substituted without confirmation.

Export the current layout from Vial before flashing. Do not clear EEPROM merely
to fix display geometry; a reset is unnecessary for the visual change and
would discard saved settings. Firmware initialization may reset saved data
if its validity identifier changes, so keep the export even for this fix.

The upstream tree at `D:\GitHub2\vial-qmk` was not modified. This definition
has been checked for JSON syntax, coordinate validity, uniqueness, upper-two-row
equivalence, 2u Right Shift geometry, and unchanged 7u bottom-row geometry.
The Vial definition-header generator was run successfully and its compressed
output decoded back to the same JSON. No firmware rebuild, flash, or live
Vial GUI verification has been performed for the 2u change.