import json

with open('nuphy_air75_v2.layout.json', 'r') as f:
    data = json.load(f)
    
layer0 = data['layers'][0]
layer1 = data['layers'][1]

# Find indices where layer1 has keys but layer0 doesn't
missing_indices = []
for i in range(len(layer1)):
    if i >= len(layer0):
        missing_indices.append(i)

print(f"Layer 0 length: {len(layer0)}")
print(f"Layer 1 length: {len(layer1)}")
print(f"Missing indices in layer 0: {missing_indices}")
print("Values at these indices in layer 1:")
for idx in missing_indices:
    print(f"Index {idx}: {layer1[idx]}")
