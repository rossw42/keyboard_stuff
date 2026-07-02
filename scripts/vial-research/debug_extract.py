import json
sys = __import__('sys')
sys.path.insert(0, '.')

kb_data = json.load(open('D:/GitHub2/vial-qmk/keyboards/boston/keyboard.json'))
layouts_dict = kb_data.get('layouts', {})

print('=== Checking multi-layout structure ===')
for name, data in layouts_dict.items():
    print('\nLayout: {}'.format(name))
    print('  Type:', type(data))
    if isinstance(data, dict):
        print('  Keys:', list(data.keys()))
        layout_val = data.get('layout')
        if layout_val:
            print('  "layout" value type:', type(layout_val))
            print('  "layout" first item:', layout_val[0] if layout_val else None)
            # Check if it's already a list or needs unwrapping
            if isinstance(layout_val, dict):
                print('  -> Nested dict with "layout" key')
            elif isinstance(layout_val, list):
                print('  -> Direct list of entries')
