#!/usr/bin/env python3
"""Extract complete footprint definitions from library PCBs.

This extracts ENTIRE footprint blocks including all graphics,
not just pads. These can be reused in generated PCBs.
"""

import re
import json
from pathlib import Path
from typing import List, Dict


def extract_footprint_blocks(pcb_path: Path) -> List[Dict]:
    """Extract all complete footprint blocks from a PCB file."""
    with open(pcb_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    footprints = []
    lines = content.split('\n')
    
    in_footprint = False
    depth = 0
    current_block = []
    
    for line in lines:
        # Check for footprint start (KiCad 6+) or module start (KiCad 5)
        if re.match(r'^\s*\((footprint|module)\s', line):
            in_footprint = True
            depth = line.count('(') - line.count(')')
            current_block = [line]
        elif in_footprint:
            current_block.append(line)
            depth += line.count('(') - line.count(')')
            
            if depth == 0:
                block_text = '\n'.join(current_block)
                
                # Extract metadata
                lib_match = re.search(r'^\s*\((footprint|module)\s+"([^"]+)"', block_text)
                ref_match = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block_text)
                
                if not ref_match:
                    # Try old format
                    ref_match = re.search(r'\(fp_text\s+reference\s+"?([^"\s]+)"?', block_text)
                
                footprints.append({
                    'library': lib_match.group(2) if lib_match else 'unknown',
                    'reference': ref_match.group(1) if ref_match else 'unknown',
                    'line_count': len(current_block),
                    'block': block_text
                })
                
                in_footprint = False
                current_block = []
    
    return footprints


def main():
    """Extract footprints from library PCBs."""
    library_path = Path('pcb-library/design-files')
    output_dir = Path('keyboard-generator/kicad_knowledge_base/footprints')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # PCBs to extract from
    pcbs = [
        ('dumbpad', library_path / 'dumbpad/kicad/dumbpad.kicad_pcb'),
        ('lumberjack', library_path / 'lumberjack/kicad/lumberjack.kicad_pcb'),
    ]
    
    all_footprints = {}
    
    for name, pcb_path in pcbs:
        if not pcb_path.exists():
            print(f"Skipping {name} - not found")
            continue
        
        print(f"\nExtracting from {name}...")
        footprints = extract_footprint_blocks(pcb_path)
        print(f"  Found {len(footprints)} footprints")
        
        # Group by library
        by_library = {}
        for fp in footprints:
            lib = fp['library']
            if lib not in by_library:
                by_library[lib] = []
            by_library[lib].append(fp)
        
        print(f"  Libraries: {len(by_library)}")
        for lib, fps in sorted(by_library.items(), key=lambda x: -len(x[1]))[:5]:
            print(f"    {lib}: {len(fps)} footprints")
        
        all_footprints[name] = footprints
        
        # Save individual footprints
        project_dir = output_dir / name
        project_dir.mkdir(exist_ok=True)
        
        for fp in footprints:
            # Create safe filename
            safe_ref = re.sub(r'[^a-zA-Z0-9_-]', '_', fp['reference'])
            fp_file = project_dir / f"{safe_ref}.kicad_fp"
            
            with open(fp_file, 'w', encoding='utf-8') as f:
                f.write(fp['block'])
    
    # Create index
    index = {}
    for project, footprints in all_footprints.items():
        index[project] = [
            {
                'reference': fp['reference'],
                'library': fp['library'],
                'line_count': fp['line_count'],
                'file': f"footprints/{project}/{re.sub(r'[^a-zA-Z0-9_-]', '_', fp['reference'])}.kicad_fp"
            }
            for fp in footprints
        ]
    
    index_file = output_dir / 'footprint_index.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    print(f"\n✓ Footprints extracted to: {output_dir}")
    print(f"✓ Index saved to: {index_file}")
    
    # Generate catalog
    catalog = []
    catalog.append("# Extracted Footprint Catalog\n\n")
    
    for project, footprints in all_footprints.items():
        catalog.append(f"## {project.title()}\n\n")
        catalog.append(f"Total footprints: {len(footprints)}\n\n")
        
        # Group by library
        by_library = {}
        for fp in footprints:
            lib = fp['library']
            if lib not in by_library:
                by_library[lib] = []
            by_library[lib].append(fp)
        
        for lib in sorted(by_library.keys()):
            fps = by_library[lib]
            catalog.append(f"### {lib}\n\n")
            for fp in fps[:10]:  # First 10
                catalog.append(f"- **{fp['reference']}** ({fp['line_count']} lines)\n")
            if len(fps) > 10:
                catalog.append(f"- ... and {len(fps) - 10} more\n")
            catalog.append("\n")
    
    catalog_file = output_dir / 'FOOTPRINT_CATALOG.md'
    with open(catalog_file, 'w', encoding='utf-8') as f:
        f.writelines(catalog)
    
    print(f"✓ Catalog saved to: {catalog_file}")


if __name__ == '__main__':
    print("="*80)
    print("Complete Footprint Extraction")
    print("="*80)
    main()
    print("\n" + "="*80)
    print("✓ Extraction Complete")
    print("="*80)
