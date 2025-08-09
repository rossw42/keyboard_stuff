import json

with open('nuphy_air75_v2_oneshot.layout.json', 'r') as f:
    data = json.load(f)
    
for i, layer in enumerate(data['layers']):
    print(f'Layer {i} has {len(layer)} keys')
