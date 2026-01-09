/* Copyright 2024 rossw42
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include QMK_KEYBOARD_H

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT_custom(
        KC_0,   KC_A,  KC_M,  KC_8,  KC_V,     // [0,0] [0,1] [0,2] [0,3] [0,4]
        KC_1,   KC_B,  KC_P,  KC_9,  KC_F1,    // [1,0] [1,1] [1,2] [1,3] [1,4]   
        KC_2,   KC_C,  KC_I,  KC_C,  KC_F2     // [2,0] [2,1] [2,2] [2,3] [2,4]
    )
};




// Layer state management
layer_state_t layer_state_set_user(layer_state_t state) {
    return state;
}



bool process_record_user(uint16_t keycode, keyrecord_t *record) {
  // If console is enabled, it will print the matrix position and status of each key pressed
#ifdef CONSOLE_ENABLE
    uprintf("Keycode: 0x%04X, - %s, row: %2u, col: %2u\n", keycode, get_keycode_string(keycode), record->event.key.row, record->event.key.col );
#endif 
  return true;
}
