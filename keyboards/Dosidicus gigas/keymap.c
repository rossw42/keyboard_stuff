#include QMK_KEYBOARD_H

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT(
        KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,                      KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,
        KC_A,    KC_S,    KC_D,    KC_F,    KC_G,                      KC_H,    KC_J,    KC_K,    KC_L,    KC_SCLN,
        KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,                      KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH,
        LT(1, KC_ENT),                                                  LT(2, KC_SPC)
    ),
    [1] = LAYOUT(
        KC_1,    KC_2,    KC_3,    KC_4,    KC_5,                      KC_6,    KC_7,    KC_8,    KC_9,    KC_0,
        LSFT(KC_1), LSFT(KC_2), LSFT(KC_3), LSFT(KC_4), LSFT(KC_5),    LSFT(KC_6), LSFT(KC_7), LSFT(KC_8), LSFT(KC_9), LSFT(KC_0),
        KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,                      KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,
        KC_TRNS,                                                        KC_NO
    ),
    [2] = LAYOUT(
        KC_TRNS, KC_TRNS, KC_BTN3, KC_LBRC, KC_RBRC,                   KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_BTN1, KC_WH_U, KC_BTN2, KC_TRNS,                   KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_WH_D, KC_9,   KC_0,                       KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS,                                                        KC_TRNS
    ),
    [3] = LAYOUT(
        KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,                      KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS,                   KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS,
        KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,                      KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS,                                                        KC_TRNS
    )
};

// Tap Dance definitions
enum {
    TD_Z = 0,
    TD_X,
    TD_C,
    TD_V,
    TD_A,
    TD_F,
    TD_Q,
    TD_P
};

tap_dance_action_t tap_dance_actions[] = {
    [TD_Z] = ACTION_TAP_DANCE_DOUBLE(KC_Z, LCTL(KC_Z)),
    [TD_X] = ACTION_TAP_DANCE_DOUBLE(KC_X, LCTL(KC_X)),
    [TD_C] = ACTION_TAP_DANCE_DOUBLE(KC_C, LCTL(KC_C)),
    [TD_V] = ACTION_TAP_DANCE_DOUBLE(KC_V, LCTL(KC_V)),
    [TD_A] = ACTION_TAP_DANCE_DOUBLE(KC_A, KC_TAB),
    [TD_F] = ACTION_TAP_DANCE_DOUBLE(KC_F, LCTL(KC_F)),
    [TD_Q] = ACTION_TAP_DANCE_DOUBLE(KC_Q, KC_ESC),
    [TD_P] = ACTION_TAP_DANCE_DOUBLE(KC_P, KC_BSPC)
};

// Combo definitions
const uint16_t PROGMEM combo_o_p[] = {KC_O, KC_P, COMBO_END};
const uint16_t PROGMEM combo_z_x[] = {KC_Z, KC_X, COMBO_END};
const uint16_t PROGMEM combo_x_c[] = {KC_X, KC_C, COMBO_END};
const uint16_t PROGMEM combo_c_v[] = {KC_C, KC_V, COMBO_END};
const uint16_t PROGMEM combo_v_b[] = {KC_V, KC_B, COMBO_END};
const uint16_t PROGMEM combo_a_x[] = {KC_A, KC_X, COMBO_END};
const uint16_t PROGMEM combo_d_f[] = {KC_D, KC_F, COMBO_END};
const uint16_t PROGMEM combo_a_s[] = {KC_A, KC_S, COMBO_END};
const uint16_t PROGMEM combo_p_l[] = {KC_P, KC_L, COMBO_END};
const uint16_t PROGMEM combo_q_s[] = {KC_Q, KC_S, COMBO_END};

combo_t key_combos[COMBO_COUNT] = {
    COMBO(combo_o_p, TG(3)),
    COMBO(combo_z_x, LCTL(KC_Z)),
    COMBO(combo_x_c, LCTL(KC_X)),
    COMBO(combo_c_v, LCTL(KC_C)),
    COMBO(combo_v_b, LCTL(KC_V)),
    COMBO(combo_a_x, LCTL(KC_A)),
    COMBO(combo_d_f, LCTL(KC_F)),
    COMBO(combo_a_s, KC_TAB),
    COMBO(combo_p_l, KC_BSPC),
    COMBO(combo_q_s, KC_ESC)
};
