"""
Batch Comparison Tool for keyboard.json → vial.json Converter

Compares generated vial.json against real reference files to identify differences.

Usage:
    python compare_vial_conversions.py [keyboards_dir] [--csv-reference PATH]

Example:
    python compare_vial_conversions.py "D:/GitHub2/vial-qmk/keyboards"
"""

import json
import os
import sys
import glob as glob_module

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keyboard_to_vial_converter import convert_keyboard_to_vial

def load_json_file(path):
    """Load JSON file with error handling."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading {path}: {type(e).__name__}: {str(e)[:100]}")
        return None

def compare_generated_vs_real(generated_path, real_path):
    """Compare generated and real vial.json files.
    
    Returns dict with differences found.
    """
    print(f"\nComparing: {generated_path}")
    
    try:
        with open(generated_path, "r", encoding="utf-8") as f:
            generated = json.load(f)
    except Exception as e:
        print(f"  ERROR loading generated file: {e}")
        return {"error": f"Could not load {generated_path}"}
    
    real_exists = os.path.exists(real_path)
    
    if not real_exists:
        print(f"  ⚠ Real reference file does not exist at: {real_path}")
        return {
            "status": "no_reference",
            "generated": generated,
            "message": f"No real vial.json to compare against. Generated has {len(generated.get('layouts', {}).get('keymap', []))} entries."
        }
    
    try:
        with open(real_path, "r", encoding="utf-8") as f:
            real = json.load(f)
    except Exception as e:
        print(f"  ERROR loading real file: {e}")
        return {"error": f"Could not load {real_path}"}
    
    differences = []
    
    # Compare top-level fields
    for field in ["name", "vendorId", "productId", "lighting"]:
        if field in generated and field in real:
            gen_value = str(generated[field])
            real_value = str(real.get(field, ""))
            if gen_value != real_value:
                differences.append({
                    "field": field,
                    "generated": gen_value,
                    "real": real_value,
                    "match": False
                })
    
    # Compare matrix object if both exist
    if "matrix" in generated and "matrix" in real:
        gen_matrix = generated["matrix"]
        real_matrix = real["matrix"]
        
        for key in ["rows", "cols"]:
            if key in gen_matrix and key in real_matrix:
                if gen_matrix[key] != real_matrix.get(key):
                    differences.append({
                        "field": f"matrix.{key}",
                        "generated": str(gen_matrix[key]),
                        "real": str(real_matrix.get(key)),
                        "match": False
                    })
    
    # Compare keymap structure
    gen_keymap = generated.get("layouts", {}).get("keymap", [])
    real_keymap = real.get("layouts", {}).get("keymap", [])
    
    if gen_keymap and real_keymap:
        print(f"  Generated keymap entries: {len(gen_keymap)}")
        print(f"  Real keymap entries: {len(real_keymap)}")
        
        # Compare entry count
        if len(gen_keymap) != len(real_keymap):
            differences.append({
                "field": "keymap.entry_count",
                "generated": str(len(gen_keymap)),
                "real": str(len(real_keymap)),
                "match": False
            })
        
        # Compare first 5 entries (structure comparison)
        min_len = min(len(gen_keymap), len(real_keymap))
        for i in range(min_len):
            gen_entry = gen_keymap[i]
            real_entry = real_keymap[i]
            
            # Simplified structure check
            if isinstance(gen_entry, list) and len(gen_entry) >= 2:
                has_w_gen = any("w" in item for item in gen_entry)
                has_w_real = any("w" in item for item in real_entry)
                
                if has_w_gen != has_w_real:
                    differences.append({
                        "field": f"entry[{i}].wide_key",
                        "generated": "has w flag",
                        "real": "no w flag",
                        "match": False
                    })
    
    return {
        "status": "complete",
        "differences": differences,
        "generated_keymap_count": len(gen_keymap),
        "real_keymap_count": len(real_keymap)
    }


def main():
    """Run batch comparison across multiple keyboards."""
    print("=" * 80)
    print("BATCH COMPARISON: Generated vs Real vial.json Files")
    print("=" * 80)
    
    # Default keyboard directory
    keyboards_dir = sys.argv[1] if len(sys.argv) > 1 else r"D:\GitHub2\vial-qmk\keyboards"
    
    if not os.path.exists(keyboards_dir):
        print(f"ERROR: Directory does not exist: {keyboards_dir}")
        return
    
    # Find all keyboard.json files and corresponding vial.json files
    results = []
    
    kb_files = glob_module.glob(os.path.join(keyboards_dir, "*", "keyboard.json"))
    
    if not kb_files:
        print(f"ERROR: No keyboard.json files found in {keyboards_dir}")
        return
    
    print(f"\nFound {len(kb_files)} keyboard.json files to process...")
    
    # Process each keyboard
    for kb_path in kb_files[:10]:  # Limit to first 10 for testing
        filename = os.path.basename(kb_path)
        vial_generated = filename.replace("keyboard.json", "keyboard_vial.json")
        vial_real = filename.replace("keyboard.json", "vial.json")
        
        generated_path = os.path.join(os.path.dirname(kb_path), vial_generated)
        real_path = os.path.join(os.path.dirname(kb_path), vial_real)
        
        print(f"\n{'='*80}")
        print(f"Processing: {filename}")
        print("="*80)
        
        # Run conversion first if generated file doesn't exist
        if not os.path.exists(generated_path):
            kb_data = load_json_file(kb_path)
            if kb_data:
                vial_output, _ = convert_keyboard_to_vial(kb_path)
                if vial_output:
                    with open(generated_path, "w", encoding="utf-8") as f:
                        json.dump(vial_output, f, indent=2)
                    print(f"✓ Generated new vial.json at: {generated_path}")
        
        # Compare generated vs real
        comparison = compare_generated_vs_real(generated_path, real_path)
        results.append({
            "keyboard": os.path.basename(kb_path),
            "comparison": comparison
        })
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    for result in results:
        kb = result["keyboard"]
        comp = result["comparison"]
        
        if "error" in comp:
            print(f"{kb}: ERROR - {comp['error'][:50]}")
        elif "no_reference" in comp["status"]:
            print(f"{kb}: Generated {len(comp.get('generated', {}))} keymap entries (no real file)")
        elif comp["status"] == "complete":
            diffs = len(comp.get("differences", []))
            gen_count = comp["generated_keymap_count"]
            real_count = comp["real_keymap_count"]
            
            if diffs == 0 and gen_count == real_count:
                print(f"{kb}: ✓ PERFECT MATCH ({gen_count} entries)")
            else:
                print(f"{kb}: ⚠ {diffs} differences found (generated: {gen_count}, real: {real_count})")
    
    # Write results to file
    with open(r"D:\GitHub\keyboard_stuff\scripts\vial-research\comparison_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to: comparison_results.json")

if __name__ == "__main__":
    main()
