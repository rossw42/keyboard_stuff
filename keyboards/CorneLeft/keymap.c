/*
Cities Skylines 2 - Corne Left Side Macropad
QMK Keymap Configuration

This keymap transforms the left side of a Corne keyboard into a 
dedicated Cities Skylines 2 macropad with 4 layers.
*/

#include QMK_KEYBOARD_H

// Layer definitions
enum layers {
    _MOVEMENT = 0,  // Movement & Building Tools (Default)
    _ZOOM,          // Zoom/Camera Controls
    _ROADS,         // Roads & Advanced Tools  
    _BUILDING       // Building & Zoning
};

// No custom keycodes needed for this layout

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /*
     * Layer 0: MOVEMENT (Default) - Building Tools & WASD Movement
     * ┌─────┬─────┬─────┬─────┬─────┬─────┐
     * │  O  │  C  │  M  │     │  W  │     │
     * │Auto │Clone│Move │     │ Fwd │     │
     * │Conn │     │Sel  │     │     │     │
     * ├─────┼─────┼─────┼─────┼─────┼─────┤
     * │ Tab │Enter│ Del │  A  │  S  │  D  │
     * │Next │Conf │Del  │Left │Back │Right│
     * │Tool │irm  │ete  │     │     │     │
     * ├─────┼─────┼─────┼─────┼─────┼─────┤
     * │Ctrl │Shift│Space│ Alt │  U  │     │
     * │Str  │Snap │Pause│Curv │Focus│     │
     * │aight│Togg │     │ed   │     │     │
     * └─────┴─────┴─────┼─────┼─────┼─────┤
     *                   │ L1  │  B  │ Esc │
     *                   │Zoom │Bull │Back │
     *                   └─────┴─────┴─────┘
     */
    [_MOVEMENT] = LAYOUT_split_3x6_3(
        KC_O,    KC_C,    KC_M,    KC_TRNS, KC_W,    KC_TRNS,
        KC_TAB,  KC_ENT,  KC_DEL,  KC_A,    KC_S,    KC_D,
        KC_LCTL, KC_LSFT, KC_SPC,  KC_LALT, KC_U,    KC_TRNS,
                          MO(_ZOOM), KC_B, KC_ESC
    ),

    /*
     * Layer 1: ZOOM/MOVEMENT - Camera Controls & Alignment
     * ┌─────┬─────┬─────┬─────┬─────┬─────┐
     * │     │     │     │     │  R  │     │
     * │     │     │     │     │ZmIn │     │
     * ├─────┼─────┼─────┼─────┼─────┼─────┤
     * │     │     │     │  Q  │  F  │  E  │
     * │     │     │     │Cam  │ZmOut│Cam  │
     * │     │     │     │Left │     │Right│
     * ├─────┼─────┼─────┼─────┼─────┼─────┤
     * │  Y  │  X  │  L  │PgUp │PgDn │     │
     * │AlnY │AlnX │AlnZ │↑Elev│↓Elev│     │
     * └─────┴─────┴─────┼─────┼─────┼─────┤
     *                   │     │ L2  │     │
     *                   │     │Road │     │
     *                   └─────┴─────┴─────┘
     */
    [_ZOOM] = LAYOUT_split_3x6_3(
        KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_R,    KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS, KC_Q,    KC_F,    KC_E,
        KC_Y,    KC_X,    KC_L,    KC_PGUP, KC_PGDN, KC_TRNS,
                          KC_TRNS, MO(_ROADS), KC_TRNS
    ),

    /*
     * Layer 2: ROADS & TOOLS - Advanced Road Building
     * ┌─────┬─────┬─────┬─────┬─────┬─────┐
     * │  H  │  N  │  T  │  G  │  J  │  K  │
     * │Hide │Node │Grid │Guide│Junc │Kerb │
     * │Show │Tool │Togg │s    │tion │Tool │
     * ├─────┼─────┼─────┼─────┼─────┼─────┤
     * │ F2  │ F3  │ F4  │  I  │  V  │  P  │
     * │Move │Anar │Prec │Inter│Vehi │Path │
     * │ It  │chy  │ision│sect │cle  │Tool │
     * ├─────┼─────┼─────┼─────┼─────┼─────┤
     * │ Ins │Home │ End │Bksp │  =  │  -  │
     * │Ins  │Strt │End  │Undo │Inc  │Dec  │
     * │Node │Pt   │Pt   │Last │     │     │
     * └─────┴─────┴─────┼─────┼─────┼─────┤
     *                   │     │     │ L3  │
     *                   │     │     │Bld  │
     *                   └─────┴─────┴─────┘
     */
    [_ROADS] = LAYOUT_split_3x6_3(
        KC_H,    KC_N,    KC_T,    KC_G,    KC_J,    KC_K,
        KC_F2,   KC_F3,   KC_F4,   KC_I,    KC_V,    KC_P,
        KC_INS,  KC_HOME, KC_END,  KC_BSPC, KC_EQL,  KC_MINS,
                          KC_TRNS, KC_TRNS, MO(_BUILDING)
    ),

    /*
     * Layer 3: BUILDING - Zoning & System Functions
     * ┌─────┬─────┬─────┬─────┬─────┬─────┐
     * │  1  │  2  │  3  │  4  │  5  │  6  │
     * │Resi │Comm │Indu │Offi │Mix  │Road │
     * │dent │ercl │strl │ce   │Use  │s    │
     * ├─────┼─────┼─────┼─────┼─────┼─────┤
     * │  7  │  8  │  9  │  0  │  [  │  ]  │
     * │Pub  │Util │Park │Serv │Dec  │Inc  │
     * │Tran │ity  │Rec  │ice  │Brsh │Brsh │
     * ├─────┼─────┼─────┼─────┼─────┼─────┤
     * │ F5  │ F9  │F10  │F11  │F12  │  `  │
     * │Save │Load │Shot │Full │Cons │Hide │
     * │     │     │     │scrn │ole  │UI   │
     * └─────┴─────┴─────┼─────┼─────┼─────┤
     *                   │     │     │     │
     *                   │     │     │     │
     *                   └─────┴─────┴─────┘
     */
    [_BUILDING] = LAYOUT_split_3x6_3(
        KC_1,    KC_2,    KC_3,    KC_4,    KC_5,    KC_6,
        KC_7,    KC_8,    KC_9,    KC_0,    KC_LBRC, KC_RBRC,
        KC_F5,   KC_F9,   KC_F10,  KC_F11,  KC_F12,  KC_GRV,
                          KC_TRNS, KC_TRNS, KC_TRNS
    )
};

// No custom processing needed for this layout

// Optional: RGB underglow layer indication
#ifdef RGBLIGHT_ENABLE
layer_state_t layer_state_set_user(layer_state_t state) {
    switch (get_highest_layer(state)) {
        case _MOVEMENT:
            rgblight_sethsv(HSV_BLUE);
            break;
        case _ZOOM:
            rgblight_sethsv(HSV_GREEN);
            break;
        case _ROADS:
            rgblight_sethsv(HSV_YELLOW);
            break;
        case _BUILDING:
            rgblight_sethsv(HSV_RED);
            break;
    }
    return state;
}
#endif