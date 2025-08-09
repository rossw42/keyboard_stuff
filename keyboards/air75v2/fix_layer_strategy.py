import json

# Load the current oneshot file
with open('nuphy_air75_v2_oneshot.layout.json', 'r') as f:
    layout = json.load(f)

print("Implementing better layer management strategy...")
print("Based on Air60 V2 version 2 successful approach and QMK best practices")

# Key changes:
# 1. Change spacebar from LT(2,KC_SPC) to LT(7,KC_SPC) - navigation layer like Air60
# 2. Redesign Layer 7 as the main layer management hub
# 3. Add reliable TO(0) reset in easily accessible location
# 4. Keep layer 2 as symbols but make it more accessible

# Change spacebar in Layer 0 from LT(3,KC_SPC) to LT(7,KC_SPC)
# Position 91 is the spacebar in the Air75 layout
spacebar_pos = 91
current_spacebar = layout['layers'][0][spacebar_pos]
print(f"Current spacebar setting: {current_spacebar}")

if current_spacebar in ["LT(2,KC_SPC)", "LT(3,KC_SPC)"]:
    layout['layers'][0][spacebar_pos] = "LT(7,KC_SPC)"
    print(f"✓ Changed spacebar from {current_spacebar} to LT(7,KC_SPC)")
else:
    print(f"⚠️  Unexpected spacebar setting: {current_spacebar}")

# Redesign Layer 7 as the navigation and layer management hub
# Copy current layer 7 as backup
original_layer_7 = layout['layers'][7].copy()

# Create new Layer 7 with proper layer management
new_layer_7 = ["KC_TRNS"] * 102  # Start with all transparent

# Layer management section (number row area)
layer_mgmt_positions = {
    18: "TG(1)",     # 1 key - Toggle Function Layer
    19: "TG(2)",     # 2 key - Toggle Symbols Layer  
    20: "TG(3)",     # 3 key - Toggle Navigation Layer
    21: "TG(4)",     # 4 key - Toggle RGB Layer
    22: "OSL(5)",    # 5 key - One Shot Settings Layer
    23: "TO(0)",     # 6 key - Return to Base Layer (RELIABLE RESET)
}

# Navigation cluster (Arrow key equivalents in better positions)
nav_positions = {
    35: "KC_HOME",   # Q position - Home
    36: "KC_UP",     # W position - Up
    37: "KC_END",    # E position - End  
    38: "KC_PGUP",   # R position - Page Up
    52: "KC_LEFT",   # A position - Left
    53: "KC_DOWN",   # S position - Down
    54: "KC_RGHT",   # D position - Right
    55: "KC_PGDN",   # F position - Page Down
}

# Apply all changes to new Layer 7
for pos, keycode in {**layer_mgmt_positions, **nav_positions}.items():
    new_layer_7[pos] = keycode

# Set the spacebar to be transparent so it works normally when layer is active
new_layer_7[91] = "KC_TRNS"  # Spacebar position

# Replace Layer 7
layout['layers'][7] = new_layer_7

print("\n✓ Redesigned Layer 7 as navigation and layer management hub:")
print("  - Numbers 1-6: Layer toggles and TO(0) reset")
print("  - QWER/ASDF area: Navigation cluster")
print("  - Spacebar: Transparent (works normally)")

# Update Layer 1 to remove some layer management and focus on function keys
# Keep the toggle keys but make TO(0) more prominent
layer_1 = layout['layers'][1]
layer_1[23] = "TO(0)"  # Make position 6 also a reset for redundancy

print("✓ Added redundant TO(0) reset in Layer 1 position 6")

# Make Layer 2 more accessible by adding it to Layer 1 as well
layer_1[24] = "MO(2)"  # Position 7 - Momentary Symbols Layer

print("✓ Added MO(2) in Layer 1 for easier symbol access")

# Save the updated layout
with open('nuphy_air75_v2_oneshot.layout.json', 'w') as f:
    json.dump(layout, f, indent=2)

print(f"\n🎉 Layer management strategy updated!")
print(f"\n📋 NEW USAGE GUIDE:")
print(f"╭─ PRIMARY LAYER ACCESS ─────────────────────────╮")
print(f"│ Hold SPACEBAR + Number = Layer Management      │")
print(f"│ • Spacebar + 1 = Toggle Function Layer (1)    │")
print(f"│ • Spacebar + 2 = Toggle Symbols Layer (2)     │") 
print(f"│ • Spacebar + 3 = Toggle Navigation Layer (3)  │")
print(f"│ • Spacebar + 4 = Toggle RGB Layer (4)         │")
print(f"│ • Spacebar + 5 = One Shot Settings (5)        │")
print(f"│ • Spacebar + 6 = RESET TO BASE LAYER (0)      │")
print(f"╰────────────────────────────────────────────────╯")
print(f"")
print(f"╭─ NAVIGATION ───────────────────────────────────╮")
print(f"│ Hold SPACEBAR + QWER/ASDF = Arrow Navigation   │")
print(f"│ • Spacebar + Q = Home                          │")
print(f"│ • Spacebar + W = Up                            │")
print(f"│ • Spacebar + E = End                           │")
print(f"│ • Spacebar + R = Page Up                       │")
print(f"│ • Spacebar + A = Left                          │")
print(f"│ • Spacebar + S = Down                          │")
print(f"│ • Spacebar + D = Right                         │")
print(f"│ • Spacebar + F = Page Down                     │")
print(f"╰────────────────────────────────────────────────╯")
print(f"")
print(f"🔑 EMERGENCY RESET: Spacebar + 6 always returns to base layer")
print(f"🔑 REDUNDANT RESET: Fn + 6 also returns to base layer")
