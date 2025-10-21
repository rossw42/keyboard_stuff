#!/usr/bin/env python3
"""
extract_pcb_specs.py
Extracts PCB specifications from documentation and creates per-project specification files.
Usage: python3 extract_pcb_specs.py <project_name> <source_repo_path>
"""

import sys
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ANSI color codes
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

def print_info(msg: str):
    print(f"{GREEN}[INFO]{NC} {msg}")

def print_warning(msg: str):
    print(f"{YELLOW}[WARN]{NC} {msg}")

def print_error(msg: str):
    print(f"{RED}[ERROR]{NC} {msg}")

class PCBSpecExtractor:
    """Extracts PCB specifications from various sources."""
    
    def __init__(self, project_name: str, source_repo: Path):
        self.project_name = project_name
        self.source_repo = source_repo
        self.specs = {
            'project_name': project_name,
            'pcb': {
                'dimensions': {},
                'layers': None,
                'thickness': None,
                'material': 'FR4',
                'surface_finish': None,
                'silkscreen': None,
                'mounting_holes': {
                    'count': None,
                    'diameter': None,
                    'positions': []
                },
                'usb_cutout': {}
            },
            'source': 'extracted',
            'notes': []
        }
    
    def extract_from_readme(self) -> bool:
        """Extract specifications from README files."""
        readme_files = list(self.source_repo.glob('**/README.md')) + \
                      list(self.source_repo.glob('**/readme.md'))
        
        found_specs = False
        
        for readme in readme_files:
            try:
                with open(readme, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extract dimensions
                    dim_patterns = [
                        r'(\d+\.?\d*)\s*mm\s*[x×]\s*(\d+\.?\d*)\s*mm',
                        r'dimensions?:\s*(\d+\.?\d*)\s*[x×]\s*(\d+\.?\d*)',
                        r'size:\s*(\d+\.?\d*)\s*mm\s*[x×]\s*(\d+\.?\d*)\s*mm'
                    ]
                    
                    for pattern in dim_patterns:
                        match = re.search(pattern, content, re.IGNORECASE)
                        if match:
                            self.specs['pcb']['dimensions']['length'] = f"{match.group(1)}mm"
                            self.specs['pcb']['dimensions']['width'] = f"{match.group(2)}mm"
                            found_specs = True
                            print_info(f"  Found dimensions: {match.group(1)}mm × {match.group(2)}mm")
                            break
                    
                    # Extract thickness
                    thickness_pattern = r'(\d+\.?\d*)\s*mm\s+thick'
                    match = re.search(thickness_pattern, content, re.IGNORECASE)
                    if match:
                        self.specs['pcb']['thickness'] = f"{match.group(1)}mm"
                        found_specs = True
                        print_info(f"  Found thickness: {match.group(1)}mm")
                    
                    # Extract layer count
                    layer_patterns = [
                        r'(\d+)\s*layer',
                        r'layers?:\s*(\d+)'
                    ]
                    
                    for pattern in layer_patterns:
                        match = re.search(pattern, content, re.IGNORECASE)
                        if match:
                            self.specs['pcb']['layers'] = int(match.group(1))
                            found_specs = True
                            print_info(f"  Found layer count: {match.group(1)}")
                            break
                    
                    # Extract mounting hole info
                    hole_pattern = r'(\d+)\s*mounting\s*holes?'
                    match = re.search(hole_pattern, content, re.IGNORECASE)
                    if match:
                        self.specs['pcb']['mounting_holes']['count'] = int(match.group(1))
                        found_specs = True
                        print_info(f"  Found mounting holes: {match.group(1)}")
                    
            except Exception as e:
                print_warning(f"  Error reading {readme}: {e}")
        
        return found_specs
    
    def extract_from_kicad(self) -> bool:
        """Extract specifications from KiCad files."""
        kicad_pcb_files = list(self.source_repo.glob('**/*.kicad_pcb'))
        
        found_specs = False
        
        for pcb_file in kicad_pcb_files:
            try:
                with open(pcb_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extract layer count from KiCad file
                    if '(layers' in content:
                        # Count copper layers
                        copper_layers = content.count('.Cu')
                        if copper_layers > 0:
                            self.specs['pcb']['layers'] = copper_layers
                            found_specs = True
                            print_info(f"  Found {copper_layers} copper layers in KiCad file")
                    
                    # Extract board outline dimensions
                    # This is complex and would require proper KiCad parsing
                    # For now, we'll note that KiCad files are available
                    self.specs['notes'].append(f"KiCad PCB file available: {pcb_file.name}")
                    
            except Exception as e:
                print_warning(f"  Error reading {pcb_file}: {e}")
        
        return found_specs
    
    def apply_standard_specs(self):
        """Apply standard specifications based on form factor."""
        # Check if this is a 60% keyboard
        if '60' in self.project_name.lower() or 'gh60' in self.project_name.lower():
            print_info("  Applying GH60 standard specifications")
            self.specs['pcb']['dimensions'] = {
                'length': '285.0mm',
                'width': '94.6mm',
                'thickness': '1.6mm'
            }
            self.specs['pcb']['layers'] = 2
            self.specs['pcb']['mounting_holes'] = {
                'count': 6,
                'diameter': '2.0-2.2mm',
                'positions': [
                    [19.0, 9.5],   # TL
                    [266.0, 9.5],  # TR
                    [28.5, 47.3],  # ML
                    [256.5, 47.3], # MR
                    [57.0, 85.0],  # BL
                    [228.0, 85.0]  # BR
                ]
            }
            self.specs['pcb']['usb_cutout'] = {
                'width': '16.0mm',
                'position': '142.5mm from left'
            }
            self.specs['source'] = 'GH60 standard'
        
        # Set defaults if not specified
        if not self.specs['pcb']['thickness']:
            self.specs['pcb']['thickness'] = '1.6mm'
            self.specs['notes'].append('Thickness assumed standard 1.6mm')
        
        if not self.specs['pcb']['layers']:
            self.specs['pcb']['layers'] = 2
            self.specs['notes'].append('Layer count assumed 2-layer')
        
        if not self.specs['pcb']['surface_finish']:
            self.specs['pcb']['surface_finish'] = 'HASL / ENIG'
            self.specs['notes'].append('Surface finish not specified, HASL or ENIG recommended')
    
    def extract_all(self) -> Dict:
        """Extract specifications from all available sources."""
        print_info(f"Extracting PCB specifications for: {self.project_name}")
        
        found_any = False
        
        # Try README files
        print_info("Searching README files...")
        if self.extract_from_readme():
            found_any = True
        
        # Try KiCad files
        print_info("Searching KiCad files...")
        if self.extract_from_kicad():
            found_any = True
        
        # Apply standard specs and defaults
        self.apply_standard_specs()
        
        if not found_any:
            print_warning("No specifications found in source files, using defaults")
            self.specs['notes'].append('Specifications not found in source, defaults applied')
        
        return self.specs
    
    def save_specs(self, output_dir: Path):
        """Save specifications to YAML file."""
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{self.project_name}_specs.yaml"
        
        with open(output_file, 'w') as f:
            yaml.dump(self.specs, f, default_flow_style=False, sort_keys=False)
        
        print_info(f"Specifications saved to: {output_file}")
        
        # Also create a markdown version for easy reading
        md_file = output_dir / f"{self.project_name}_specs.md"
        self.save_markdown(md_file)
        print_info(f"Markdown version saved to: {md_file}")
    
    def save_markdown(self, output_file: Path):
        """Save specifications as markdown."""
        with open(output_file, 'w') as f:
            f.write(f"# {self.project_name} PCB Specifications\n\n")
            
            # PCB Dimensions
            f.write("## PCB Dimensions\n\n")
            dims = self.specs['pcb']['dimensions']
            if dims:
                if 'length' in dims:
                    f.write(f"- **Length:** {dims['length']}\n")
                if 'width' in dims:
                    f.write(f"- **Width:** {dims['width']}\n")
            
            if self.specs['pcb']['thickness']:
                f.write(f"- **Thickness:** {self.specs['pcb']['thickness']}\n")
            
            if self.specs['pcb']['layers']:
                f.write(f"- **Layers:** {self.specs['pcb']['layers']}\n")
            
            f.write(f"- **Material:** {self.specs['pcb']['material']}\n")
            
            if self.specs['pcb']['surface_finish']:
                f.write(f"- **Surface Finish:** {self.specs['pcb']['surface_finish']}\n")
            
            # Mounting Holes
            f.write("\n## Mounting Holes\n\n")
            holes = self.specs['pcb']['mounting_holes']
            if holes['count']:
                f.write(f"- **Count:** {holes['count']}\n")
            if holes['diameter']:
                f.write(f"- **Diameter:** {holes['diameter']}\n")
            
            if holes['positions']:
                f.write("\n### Positions (from PCB top-left corner)\n\n")
                labels = ['TL', 'TR', 'ML', 'MR', 'BL', 'BR']
                for i, pos in enumerate(holes['positions']):
                    label = labels[i] if i < len(labels) else f"H{i+1}"
                    f.write(f"- **{label}:** {pos[0]}mm, {pos[1]}mm\n")
            
            # USB Cutout
            if self.specs['pcb']['usb_cutout']:
                f.write("\n## USB Cutout\n\n")
                usb = self.specs['pcb']['usb_cutout']
                if 'width' in usb:
                    f.write(f"- **Width:** {usb['width']}\n")
                if 'position' in usb:
                    f.write(f"- **Position:** {usb['position']}\n")
            
            # Notes
            if self.specs['notes']:
                f.write("\n## Notes\n\n")
                for note in self.specs['notes']:
                    f.write(f"- {note}\n")
            
            # Source
            f.write(f"\n## Source\n\n")
            f.write(f"Specifications {self.specs['source']}\n")

def main():
    if len(sys.argv) < 3:
        print_error("Usage: python3 extract_pcb_specs.py <project_name> <source_repo_path>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    source_repo = Path(sys.argv[2])
    
    if not source_repo.exists():
        print_error(f"Source repository not found: {source_repo}")
        sys.exit(1)
    
    # Get script directory and set output path
    script_dir = Path(__file__).parent
    pcb_dir = script_dir.parent
    specs_dir = pcb_dir / 'docs' / 'pcb-specs'
    
    # Extract specifications
    extractor = PCBSpecExtractor(project_name, source_repo)
    specs = extractor.extract_all()
    
    # Save specifications
    extractor.save_specs(specs_dir)
    
    print_info("")
    print_info("=" * 50)
    print_info("PCB Specification Extraction Complete")
    print_info("=" * 50)
    print_info(f"Project: {project_name}")
    print_info(f"Output: {specs_dir}")
    print_info("=" * 50)

if __name__ == '__main__':
    main()
