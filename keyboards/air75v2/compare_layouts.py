import json

# Load both files
with open('nuphy_air75_v2.layout.json', 'r') as f:
    original = json.load(f)
    
with open('nuphy_air75_v2_oneshot.layout.json', 'r') as f:
    oneshot = json.load(f)

print("=== Key Count Comparison ===")
print(f"Original file layers: {len(original['layers'])}")
print(f"Oneshot file layers: {len(oneshot['layers'])}")

for i in range(min(len(original['layers']), len(oneshot['layers']))):
    orig_len = len(original['layers'][i])
    oneshot_len = len(oneshot['layers'][i])
    print(f"Layer {i}: Original={orig_len}, Oneshot={oneshot_len}, Difference={orig_len - oneshot_len}")

print("\n=== Finding Missing Keys ===")
# Find which position is missing by comparing the layouts
for layer_idx in range(min(len(original['layers']), len(oneshot['layers']))):
    orig_layer = original['layers'][layer_idx]
    oneshot_layer = oneshot['layers'][layer_idx]
    
    if len(orig_layer) != len(oneshot_layer):
        print(f"\nLayer {layer_idx} has different lengths:")
        print(f"  Original: {len(orig_layer)} keys")
        print(f"  Oneshot: {len(oneshot_layer)} keys")
        
        # Find the missing key by position
        for i in range(max(len(orig_layer), len(oneshot_layer))):
            if i >= len(oneshot_layer):
                print(f"  Missing key at position {i}: '{orig_layer[i]}'")
            elif i >= len(orig_layer):
                print(f"  Extra key at position {i}: '{oneshot_layer[i]}'")
            elif orig_layer[i] != oneshot_layer[i]:
                # Check if keys are just shifted
                print(f"  Difference at position {i}:")
                print(f"    Original: '{orig_layer[i]}'")
                print(f"    Oneshot: '{oneshot_layer[i]}'")
                break
