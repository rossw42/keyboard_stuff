"""
Comprehensive comparison of ALL 504 keyboards from CSV reference.
Compares generated vial.json vs real original files from vial-qmk repo.
"""

import json
import os
import sys
sys.path.insert(0, '.')
from keyboard_to_vial_converter import convert_keyboard_to_vial
import csv

BASE_PATH = r"D:\GitHub2\vial-qmk"
GEN_BASE_PATH = r"D:\GitHub\keyboard_stuff\scripts\vial-research\vials"


def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return None


def compare_vials(real_path, gen_path):
    """Compare real vs generated vial.json files."""
    result = {
        "real_entries": 0,
        "gen_entries": 0,
        "metadata_match": True,
        "issues": [],
        "status": None
    }
    
    real_exists = os.path.exists(real_path)
    gen_exists = os.path.exists(gen_path)
    
    if not real_exists:
        result["status"] = "no_reference"
        return result
    
    try:
        real_data = load_json_file(real_path)
        if not real_data:
            result["status"] = "failed_load_real"
            return result
            
    except Exception as e:
        result["status"] = f"real_load_error: {type(e).__name__}"
        return result
    
    if not gen_exists:
        result["status"] = "no_generated"
        result["real_entries"] = len(real_data.get("layouts", {}).get("keymap", []))
        return result
    
    try:
        gen_data = load_json_file(gen_path)
        if not gen_data:
            result["status"] = "failed_load_gen"
            return result
            
    except Exception as e:
        result["status"] = f"gen_load_error: {type(e).__name__}"
        return result
    
    # Check metadata
    for field in ["name", "vendorId", "productId", "lighting"]:
        real_val = str(real_data.get(field, ""))
        gen_val = str(gen_data.get(field, ""))
        if real_val != gen_val:
            result["metadata_match"] = False
            result["issues"].append({
                "field": field,
                "real": real_val,
                "gen": gen_val
            })
    
    # Count entries
    real_entries = len(real_data.get("layouts", {}).get("keymap", []))
    gen_entries = len(gen_data.get("layouts", {}).get("keymap", []))
    
    result["real_entries"] = real_entries
    result["gen_entries"] = gen_entries
    
    if real_entries != gen_entries:
        result["issues"].append({
            "type": "entry_count_mismatch",
            "delta": gen_entries - real_entries
        })
    
    result["status"] = "complete"
    return result


def main():
    print("=" * 80)
    print("COMPREHENSIVE VIAL.JSON COMPARISON - ALL 504 KEYBOARDS")
    print(f"Base path: {BASE_PATH}")
    print(f"Generated base: {GEN_BASE_PATH}")
    print("=" * 80)
    
    csv_path = r"D:\GitHub\keyboard_stuff\scripts\vial-research\vial_keyboard_pairs.csv"
    
    pairs = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) >= 2:
                kb_path, vial_path = row[0].strip(), row[1].strip()
                # Remove 'keyboards' prefix from kb_path
                if kb_path.startswith("D:\\GitHub2\\vial-qmk\\keyboards"):
                    kb_folder = os.path.basename(os.path.dirname(kb_path))
                    real_path = os.path.join(BASE_PATH, "keyboards", kb_folder, "vial.json")
                    pairs.append((kb_folder, real_path))
    
    print(f"\nFound {len(pairs)} keyboard pairs\n")
    
    results = []
    matches = 0
    mismatches = 0
    
    for i, (kb_folder, real_path) in enumerate(pairs, 1):
        gen_path = os.path.join(GEN_BASE_PATH, kb_folder, "vial.json")
        
        result = compare_vials(real_path, gen_path)
        result["name"] = kb_folder
        
        if result["status"] == "complete":
            if result["real_entries"] == result["gen_entries"]:
                matches += 1
                status_str = "MATCH"
            else:
                mismatches += 1
                status_str = f"MISMATCH ({result['gen_entries']}/{result['real_entries']})"
        else:
            status_str = result["status"]
        
        if i % 50 == 0 or status_str.startswith("MATCH"):
            print(f"[{i}/{len(pairs)}] {result['name']:25} {status_str}")
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total processed: {matches + mismatches}")
    print(f"Perfect matches: {matches}")
    print(f"Mismatches: {mismatches}")
    
    # Write detailed results
    with open(r"D:\GitHub\keyboard_stuff\scripts\vial-research\comparison_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nDetailed results saved to: comparison_results.json")


if __name__ == "__main__":
    main()
