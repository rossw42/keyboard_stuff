
#include QMK_KEYBOARD_H
enum layer_names {
    _BASE,
    _LOWER,
};


const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {

/* Keymap _0: (Base Layer) Default Layer
   * |-----------------------------.
   * |  1  |  2  |  3  |  4  | Enc/5 |
   * |-----|-----|-----|-----|-----|
   * |  6  |  7  |  8  |  9  |  0  |
   * .-----------------------------.
   */
    [0] = LAYOUT(
        KC_4,   KC_5,     KC_G,    KC_C,   KC_1,
        KC_X,   KC_P,     KC_E,    KC_9,   KC_0
    ),
    [1] = LAYOUT(
        KC_A,   KC_B,     KC_C,    KC_D,   KC_E,
        KC_F,   KC_G,     KC_H,    KC_I,   KC_J
    ),
    [2] = LAYOUT(
        KC_A,   KC_B,     KC_C,    KC_D,   KC_E,
        KC_F,   KC_G,     KC_H,    KC_I,   KC_J
    ),
    [3] = LAYOUT(
        KC_A,   KC_B,     KC_C,    KC_D,   KC_E,
        KC_F,   KC_G,     KC_H,    KC_I,   KC_J
    )
};


#if defined(ENCODER_MAP_ENABLE)
const uint16_t PROGMEM encoder_map[][NUM_ENCODERS][NUM_DIRECTIONS] = {
    [0] = { ENCODER_CCW_CW(KC_MS_WH_DOWN, KC_MS_WH_UP)  },
    [1] = { ENCODER_CCW_CW(KC_DOWN, KC_UP)  },
    [2] = { ENCODER_CCW_CW(KC_LEFT, KC_RGHT)  },
    [3] = { ENCODER_CCW_CW(KC_VOLD, KC_VOLU)  },
    };
#endif
