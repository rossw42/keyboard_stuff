import csv
import json
from pathlib import Path
from collections import Counter

def analyze_pairs():
    csv_path = Path(r"D:\GitHub\keyboard_stuff\scripts\vial_keyboard_pairs.csv")
    results = []

    if not csv_path.exists():
        print(f"Error: {csv_path} not found.")
        return

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kb_path = Path(row['keyboard.json'])
            vial_path = Path(row['vial.json'])
            
            if not kb_path.exists() or not vial_path.exists():
                continue

            try:
                with open(kb_path, 'r', encoding='utf-8') as kb_f:
                    kb_data = json.load(kb_f)
                with open(vial_path, 'r', encoding='utf-8') as vial_f:
                    vial_data = json.load(vial_f)
            except Exception as e:
                print(f"Error reading {kb_path.name}: {e}")
                continue

            # Extract layouts
            kb_layout = kb_data.get('layouts', {}).get('LAYOUT', {}).get('layout', [])
            vial_layout = vial_data.get('layouts', {}).get('keymap', [])

            # 1. Determine Order
            vial_matrices = []
            for entry in vial_layout:
                if isinstance(entry, list) and len(entry) > 1:
                    vial_matrices.append(entry[1])
                elif isinstance(entry, str):
                    vial_matrices.append(entry)

            order = []
            seen_kb_rows = set()
            for m_idx in vial_matrices:
                if isinstance(m_idx, str) and "," in m_idx:
                    try:
                        row_idx = int(m_idx.split(',')[0])
                        if row_idx not in seen_kb_rows:
                            order.append(row_idx)
                            seen_kb_rows.add(row_idx)
                    except (ValueError, IndexError):
                        continue
            
            # 2. Detect Stacked Keys
            stacked_count = 0
            for entry in vial_layout:
                if isinstance(entry, list) and len(entry) > 1:
                    if "\n" in str(entry[1]):
                        stacked_count += 1

            # 3. Detect Advanced Props
            has_rot = any("r" in str(item) for item in vial_layout if isinstance(item, list) and len(item) > 1)
            has_color = any("c" in str(item) for item in vial_layout if isinstance(item, list) and len(item) > 1)

            results.append({
                "kb_name": kb_data.get('keyboard_name', 'unknown'),
                "order": order,
                "stacked": stacked_count > 0,
                "rot": has_rot,
                "color": has_color,
                "vial_name": vial_data.get('name', 'unknown')
            })

    if not results:
        print("No valid pairs analyzed.")
        return

    print(f"Analyzed {len(results)} pairs.")
    
    # Group by order
    order_counts = Counter([tuple(r['order']) for r in results])
    print("\nCommon Order Patterns:")
    for o, count in order_counts.most_common(10):
        print(f"Order {o}: {count} keyboards")

    # Group by features
    stacked_total = sum(1 for r in results if r['stacked'])
    rot_total = sum(1 for r in results if r['rot'])
    print(f"\nStacked Keys Found: {stacked_total}")
    print(f"Rotation/Scaling Found: {rot_total}")

if __name__ == "__main__":
    analyze_pairs()
