"""Batch convert ALL keyboards from CSV to vial.json files."""

import csv
import json
import os
import sys

sys.path.insert(0, r"D:\GitHub\keyboard_stuff\scripts\vial-research")

from keyboard_to_vial_converter import convert_keyboard_to_vial

CSV_PATH = r"D:\GitHub\keyboard_stuff\scripts\vial-research\vial_keyboard_pairs.csv"
VIALS_BASE = r"D:\GitHub\keyboard_stuff\scripts\vial-research\vials"
REPORTS_DIR = r"D:\GitHub\keyboard_stuff\scripts\vial-research\reports"


def process_all_keyboards():
    """Process all keyboards from CSV reference."""
    results = []
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        
        for row in reader:
            if len(row) < 2:
                continue
                
            kb_path = row[0].strip()
            
            output_name = os.path.basename(kb_path.replace('keyboard.json', ''))
            
            vials_base_path = os.path.join(VIALS_BASE, output_name)
            
            if not os.path.exists(vials_base_path):
                os.makedirs(vials_base_path, exist_ok=True)
            
            out_path = os.path.join(vials_base_path, 'vial.json')
            
            print(f"[{len(results)+1}/504] Processing: {output_name}")
            
            vial_output, source_data = convert_keyboard_to_vial(kb_path)
            
            if vial_output is None:
                print(f"  ERROR loading {kb_path}")
                results.append((output_name, "FAILED"))
            else:
                try:
                    with open(out_path, 'w', encoding='utf-8') as vf:
                        json.dump(vial_output, vf, indent=2)
                    print(f"  OK Saved to: {out_path}")
                    keymap_count = len(vial_output.get("layouts", {}).get("keymap", []))
                    print(f"    ({keymap_count} keymap entries)")
                    results.append((output_name, "OK"))
                except Exception as e:
                    print(f"  ERROR saving {kb_path}: {type(e).__name__}")
                    results.append((output_name, "FAILED"))
    
    # Save summary
    summary_path = os.path.join(REPORTS_DIR, 'batch_all_conversion_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    ok_count = sum(1 for _, s in results if s == "OK")
    fail_count = len(results) - ok_count
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total processed: {len(results)}")
    print(f"Successful: {ok_count}")
    print(f"Failed: {fail_count}")
    print(f"\nOK results saved to: {summary_path}")


if __name__ == "__main__":
    process_all_keyboards()
