// Copyright 2025 rossw42
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

// Split keyboard settings
#define SOFT_SERIAL_PIN D2
#define SPLIT_HAND_PIN B5
#define EE_HANDS

// Communication settings
#define SELECT_SOFT_SERIAL_SPEED 1

// Debounce reduces chatter
#define DEBOUNCE 5

// Vial settings
#define VIAL_KEYBOARD_UID {0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0}
#define VIAL_UNLOCK_COMBO_ROWS { 0, 0 }
#define VIAL_UNLOCK_COMBO_COLS { 0, 1 }

// Dynamic keymap settings
#define DYNAMIC_KEYMAP_LAYER_COUNT 4
