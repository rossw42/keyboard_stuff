import json

r = json.load(open('D:/GitHub2/vial-qmk/keyboards/alps64/vial.json'))
g = json.load(open('D:/GitHub/keyboard_stuff/scripts/vial-research/vials/alps64/vial.json'))

print('=== Alps64 Entry Structure Comparison ===')
print()
print('Real file has 64 entries:')
real_entries = r['layouts']['keymap']
for i, entry in enumerate(real_entries[:5]):
    print('  [{}: {}]'.format(i, repr(entry)))

print()
print('Generated file has 142 entries:')
gen_entries = g['layouts']['keymap']
for i, entry in enumerate(gen_entries[:10]):
    print('  [{}: {}]'.format(i, repr(entry)))

# Check if wide keys exist
wide_keys_real = [i for i,e in enumerate(real_entries) if isinstance(e, dict) and 'w' in e]
wide_keys_gen = [i for i,e in enumerate(gen_entries) if isinstance(e, dict) and 'w' in e]

print()
print('Wide keys in real:', wide_keys_real[:5] if wide_keys_real else [])
print('Wide keys in generated:', wide_keys_gen[:5] if wide_keys_gen else [])

# Check first few entries more closely
print()
print('Detailed comparison of first 3 entries:')
for i in range(3):
    print('\nEntry {}:\n'.format(i))
    real = real_entries[i]
    gen = gen_entries[i]
    print('Real:   ', repr(real))
    print('Gen:    ', repr(gen))
