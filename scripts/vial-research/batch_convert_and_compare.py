"""
Batch Conversion and Comparison Script for keyboard_to_vial_converter.py

Reads CSV reference file and processes all keyboards, comparing generated vial.json
against original vial.json files.

Output: Generated vials saved in D:\GitHub\keyboard_stuff\scripts\vial-research\vials\<keyboard_folder>\vial.json
"""

import json
import os
import sys
import csv
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keyboard_to_vial_converter import convert_keyboard_to_vial

def read_csv_pairs(csv_path):
    """Read CSV file and return list of (keyboard_json, vial_json) pairs."""
    pairs = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                kb_path, vial_path = row[0].strip(), row[1].strip()
                pairs.append((kb_path, vial_path))
    return pairs

def get_subfolder_from_kb_path(kb_path):
    """Extract immediate parent folder name from keyboard.json path.
    
    Example: D:\\GitHub2\\vial-qmk\\keyboards\\boston\\keyboard.json -> boston
    """
    # Normalize path separators
    kb_path = kb_path.replace('\\', '/')
    
    # Remove drive letter if present  
    if 'D:/keyboards' in kb_path:
        kb_path = kb_path.replace('D:/keyboards', '')
    
    # Split into parts and get the second-to-last (immediate parent folder)
    parts = kb_path.split('/')
    return parts[-2] if len(parts) >= 2 else "unknown"

def load_json_file(path):
    """Load JSON file with error handling."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("  ERROR loading {}: {}".format(path, type(e).__name__))
        return None

def compare_generated_vs_real(generated_path, real_path):
    """Compare generated and real vial.json files."""
    result = {
        "generated_entries": 0,
        "real_entries": 0,
        "structure_match": False,
        "metadata_match": True,
        "issues": [],
        "warnings": []
    }
    
    try:
        with open(generated_path, "r", encoding="utf-8") as f:
            generated = json.load(f)
    except Exception as e:
        result["errors"] = "Could not load {}".format(generated_path)
        return result
    
    real_exists = os.path.exists(real_path)
    
    if not real_exists:
        result["warnings"].append("No real vial.json at {}".format(real_path))
        result["status"] = "no_reference"
        result["generated_entries"] = len(generated.get("layouts", {}).get("keymap", []))
        return result
    
    try:
        with open(real_path, "r", encoding="utf-8") as f:
            real = json.load(f)
    except Exception as e:
        result["errors"] = "Could not load {}".format(real_path)
        return result
    
    # Check metadata fields
    gen_metadata = ["name", "vendorId", "productId", "lighting"]
    for field in gen_metadata:
        if field in generated and field in real:
            gen_val = str(generated[field])
            real_val = str(real.get(field, ""))
            if gen_val != real_val:
                result["metadata_match"] = False
                result["issues"].append({
                    "field": field,
                    "generated": gen_val,
                    "real": real_val
                })
    
    # Check optional matrix field
    if "matrix" in generated and "matrix" in real:
        for key in ["rows", "cols"]:
            if key in generated["matrix"] and key in real["matrix"]:
                if generated["matrix"][key] != real["matrix"].get(key):
                    result["issues"].append({
                        "field": "{}.{}".format(key),
                        "generated": str(generated["matrix"][key]),
                        "real": str(real["matrix"].get(key))
                    })
    
    # Count and compare entry structures
    gen_keymap = generated.get("layouts", {}).get("keymap", [])
    real_keymap = real.get("layouts", {}).get("keymap", [])
    
    result["generated_entries"] = len(gen_keymap)
    result["real_entries"] = len(real_keymap)
    
    # Check entry count match
    if result["generated_entries"] != result["real_entries"]:
        result["structure_match"] = False
    
    result["status"] = "complete"
    return result

def main():
    """Main batch conversion and comparison function."""
    print("="*80)
    print("BATCH CONVERSION AND COMPARISON")
    print("keyboard.json to vial.json with CSV reference")
    print("="*80)
    
    # Define paths
    csv_path = r"D:\GitHub\keyboard_stuff\scripts\vial-research\vial_keyboard_pairs.csv"
    output_dir = r"D:\GitHub\keyboard_stuff\scripts\vial-research\vials"
    reports_dir = r"D:\GitHub\keyboard_stuff\scripts\vial-research\reports"
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    print("\nReading CSV pairs from: {}".format(csv_path))
    csv_pairs = read_csv_pairs(csv_path)
    print("Found {} keyboard pairs in CSV".format(len(csv_pairs)))
    
    results = []
    
    for i, (kb_path, real_vial_path) in enumerate(csv_pairs, 1):
        # Extract subfolder from path (directory immediately before keyboard.json)
        subfolder = get_subfolder_from_kb_path(kb_path)
        
        # Generate output path: vials/<subfolder>/vial.json
        generated_vial_path = os.path.join(output_dir, subfolder, "vial.json")
        
        kb_name = os.path.basename(kb_path).replace("keyboard.json", "")
        
        print("\n[{}/{}] Processing: {}".format(i, len(csv_pairs), kb_name))
        print("  Source: {}".format(kb_path))
        print("  Output folder: {}".format(subfolder))
        print("  Generated will be: {}".format(generated_vial_path))
        
        # Convert keyboard.json to vial.json
        kb_data = load_json_file(kb_path)
        if not kb_data:
            print("  ! Failed to load source keyboard.json")
            results.append({
                "name": kb_name,
                "status": "error",
                "error": "Could not load keyboard.json"
            })
            continue
        
        vial_output, _ = convert_keyboard_to_vial(kb_path)
        
        if not vial_output:
            print("  ! Conversion returned None")
            results.append({
                "name": kb_name,
                "status": "error",
                "error": "Conversion failed"
            })
            continue
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(generated_vial_path), exist_ok=True)
        
        # Save generated vial.json
        try:
            with open(generated_vial_path, "w", encoding="utf-8") as f:
                json.dump(vial_output, f, indent=2)
            print("  OK Saved to: {}".format(generated_vial_path))
            print("    ({} keymap entries)".format(len(vial_output['layouts']['keymap'])))
        except Exception as save_err:
            print("  ! Could not save file: {}".format(save_err))
        
        # Compare with real vial.json if it exists
        comparison = compare_generated_vs_real(generated_vial_path, real_vial_path)
        comparison["keyboard_name"] = kb_name
        
        # Print summary
        gen_entries = comparison.get("generated_entries", 0)
        real_entries = comparison.get("real_entries", 0)
        
        if "error" in comparison:
            print("  ! {}".format(comparison.get('errors', 'Unknown error')))
        elif "no_reference" in comparison.get("status", ""):
            print("  i No real reference file (generated only)")
        else:
            status = "MATCH" if gen_entries == real_entries else "DIFFERS"
            print("  {}".format(status))

    # Save results to JSON file
    results_file = os.path.join(reports_dir, "batch_conversion_results.json")
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump({
            "processed_at": datetime.now().isoformat(),
            "total_keyboards": len(results),
            "results": results
        }, f, indent=2)
    print("\nOK Results saved to: {}".format(results_file))
    
    # Print summary statistics
    if results:
        matches = sum(1 for r in results if r.get("comparison", {}).get("status") == "complete" 
                     and r.get("metadata_match") and r.get("structure_match"))
        errors = sum(1 for r in results if r.get("status") == "error")
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print("Total keyboards processed: {}".format(len(results)))
        print("Perfect matches: {}".format(matches))
        print("Errors: {}".format(errors))

if __name__ == "__main__":
    main()
