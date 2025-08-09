import json

# Load the oneshot file
with open('nuphy_air75_v2_oneshot.layout.json', 'r') as f:
    oneshot = json.load(f)

# Load the original file for reference
with open('nuphy_air75_v2.layout.json', 'r') as f:
    original = json.load(f)

print("Fixing oneshot layout to have 102 keys per layer...")

# Fix each layer by adding the missing key at the end
for layer_idx in range(len(oneshot['layers'])):
    current_layer = oneshot['layers'][layer_idx]
    original_layer = original['layers'][layer_idx]
    
    if len(current_layer) < 102:
        # Add the missing key from the original at the same position
        missing_key = original_layer[len(current_layer)]
        current_layer.append(missing_key)
        print(f"Layer {layer_idx}: Added '{missing_key}' at position {len(current_layer)-1}")

# Verify all layers now have 102 keys
print("\nVerification:")
for i, layer in enumerate(oneshot['layers']):
    print(f"Layer {i}: {len(layer)} keys")

# Save the fixed file
with open('nuphy_air75_v2_oneshot.layout.json', 'w') as f:
    json.dump(oneshot, f, indent=2)

print("\nFixed oneshot layout saved!")
