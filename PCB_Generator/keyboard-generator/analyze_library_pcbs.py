#!/usr/bin/env python3
"""Analyze library PCBs to build knowledge base about KiCad format.

This script:
1. Parses real PCBs from the library
2. Extracts complete footprint definitions
3. Analyzes structure and patterns
4. Builds a knowledge base for generating proper PCBs
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


class KiCadPCBAnalyzer:
    """Analyze KiCad PCB files to understand structure."""
    
    def __init__(self, pcb_path: Path):
        """Initialize analyzer with PCB file path."""
        self.pcb_path = Path(pcb_path)
        self.content = ""
        self.analysis = {
            'file': str(pcb_path),
            'line_count': 0,
            'sections': {},
            'footprints': [],
            'nets': [],
            'segments': [],
            'vias': [],
            'zones': [],
            'graphics': []
        }
        
    def analyze(self) -> Dict[str, Any]:
        """Perform complete analysis of PCB file."""
        print(f"\nAnalyzing: {self.pcb_path.name}")
        
        # Load file
        with open(self.pcb_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        self.analysis['line_count'] = len(self.content.split('\n'))
        print(f"  Lines: {self.analysis['line_count']:,}")
        
        # Analyze structure
        self._analyze_sections()
        self._extract_footprints()
        self._analyze_nets()
        self._analyze_routing()
        self._analyze_graphics()
        
        return self.analysis
    
    def _analyze_sections(self):
        """Identify all top-level sections."""
        # Find all top-level tokens
        pattern = r'^\s\s\(([a-z_]+)'
        matches = re.findall(pattern, self.content, re.MULTILINE)
        
        section_counts = defaultdict(int)
        for match in matches:
            section_counts[match] += 1
        
        self.analysis['sections'] = dict(section_counts)
        print(f"  Sections: {len(section_counts)}")
        for section, count in sorted(section_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"    {section}: {count}")
    
    def _extract_footprints(self):
        """Extract complete footprint definitions."""
        # Find all footprint blocks
        footprint_blocks = self._extract_blocks('footprint')
        
        print(f"  Footprints: {len(footprint_blocks)}")
        
        for block in footprint_blocks[:5]:  # Analyze first 5 in detail
            fp_analysis = self._analyze_footprint_block(block)
            self.analysis['footprints'].append(fp_analysis)
    
    def _analyze_footprint_block(self, block: str) -> Dict[str, Any]:
        """Analyze a single footprint block."""
        # Extract library link
        lib_match = re.search(r'^\s*\(footprint\s+"([^"]+)"', block)
        library = lib_match.group(1) if lib_match else "unknown"
        
        # Extract reference
        ref_match = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        reference = ref_match.group(1) if ref_match else "unknown"
        
        # Count elements
        fp_text_count = len(re.findall(r'\(fp_text', block))
        fp_line_count = len(re.findall(r'\(fp_line', block))
        fp_circle_count = len(re.findall(r'\(fp_circle', block))
        fp_arc_count = len(re.findall(r'\(fp_arc', block))
        pad_count = len(re.findall(r'^\s*\(pad', block, re.MULTILINE))
        
        # Extract layers used
        layers = set(re.findall(r'\(layer\s+"([^"]+)"\)', block))
        
        return {
            'library': library,
            'reference': reference,
            'line_count': len(block.split('\n')),
            'elements': {
                'fp_text': fp_text_count,
                'fp_line': fp_line_count,
                'fp_circle': fp_circle_count,
                'fp_arc': fp_arc_count,
                'pads': pad_count
            },
            'layers': sorted(list(layers)),
            'sample_block': block[:500] + '...' if len(block) > 500 else block
        }
    
    def _analyze_nets(self):
        """Analyze net definitions."""
        net_pattern = r'\(net\s+(\d+)\s+"([^"]*)"\)'
        nets = re.findall(net_pattern, self.content)
        
        self.analysis['nets'] = [
            {'number': int(num), 'name': name}
            for num, name in nets[:20]  # First 20 nets
        ]
        print(f"  Nets: {len(nets)}")
    
    def _analyze_routing(self):
        """Analyze routing (segments, vias)."""
        segment_count = len(re.findall(r'^\s*\(segment', self.content, re.MULTILINE))
        via_count = len(re.findall(r'^\s*\(via', self.content, re.MULTILINE))
        zone_count = len(re.findall(r'^\s*\(zone', self.content, re.MULTILINE))
        
        self.analysis['routing'] = {
            'segments': segment_count,
            'vias': via_count,
            'zones': zone_count
        }
        print(f"  Routing: {segment_count} segments, {via_count} vias, {zone_count} zones")
    
    def _analyze_graphics(self):
        """Analyze board graphics."""
        gr_line_count = len(re.findall(r'^\s*\(gr_line', self.content, re.MULTILINE))
        gr_text_count = len(re.findall(r'^\s*\(gr_text', self.content, re.MULTILINE))
        gr_circle_count = len(re.findall(r'^\s*\(gr_circle', self.content, re.MULTILINE))
        
        self.analysis['graphics'] = {
            'gr_line': gr_line_count,
            'gr_text': gr_text_count,
            'gr_circle': gr_circle_count
        }
        print(f"  Graphics: {gr_line_count} lines, {gr_text_count} text, {gr_circle_count} circles")
    
    def _extract_blocks(self, token: str) -> List[str]:
        """Extract all blocks for a given token."""
        blocks = []
        lines = self.content.split('\n')
        
        in_block = False
        depth = 0
        current_block = []
        
        for line in lines:
            if re.match(rf'^\s*\({token}\s', line):
                in_block = True
                depth = line.count('(') - line.count(')')
                current_block = [line]
            elif in_block:
                current_block.append(line)
                depth += line.count('(') - line.count(')')
                
                if depth == 0:
                    blocks.append('\n'.join(current_block))
                    in_block = False
                    current_block = []
        
        return blocks


def analyze_library_pcbs():
    """Analyze multiple PCBs from library."""
    library_path = Path('pcb-library/design-files')
    
    # Select representative PCBs
    pcbs_to_analyze = [
        library_path / 'dumbpad/kicad/dumbpad.kicad_pcb',
        library_path / 'lumberjack/kicad/lumberjack.kicad_pcb',
        library_path / 'plaid/kicad/plaid.kicad_pcb',
    ]
    
    all_analyses = []
    
    for pcb_path in pcbs_to_analyze:
        if not pcb_path.exists():
            print(f"Skipping {pcb_path} - not found")
            continue
        
        analyzer = KiCadPCBAnalyzer(pcb_path)
        analysis = analyzer.analyze()
        all_analyses.append(analysis)
    
    # Save analyses
    output_dir = Path('keyboard-generator/kicad_knowledge_base')
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'pcb_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_analyses, f, indent=2)
    
    print(f"\n✓ Analysis saved to: {output_file}")
    
    # Generate summary
    generate_summary(all_analyses, output_dir)
    
    return all_analyses


def generate_summary(analyses: List[Dict], output_dir: Path):
    """Generate human-readable summary."""
    summary = []
    summary.append("# KiCad PCB Analysis Summary\n")
    summary.append(f"Analyzed {len(analyses)} PCB files from library\n")
    
    for analysis in analyses:
        summary.append(f"\n## {Path(analysis['file']).name}\n")
        summary.append(f"- **Lines**: {analysis['line_count']:,}\n")
        summary.append(f"- **Footprints**: {analysis['sections'].get('footprint', 0)}\n")
        summary.append(f"- **Nets**: {len(analysis['nets'])}\n")
        summary.append(f"- **Segments**: {analysis['routing']['segments']}\n")
        summary.append(f"- **Vias**: {analysis['routing']['vias']}\n")
        summary.append(f"- **Zones**: {analysis['routing']['zones']}\n")
        
        summary.append(f"\n### Sample Footprints\n")
        for fp in analysis['footprints'][:3]:
            summary.append(f"\n#### {fp['reference']} ({fp['library']})\n")
            summary.append(f"- Lines: {fp['line_count']}\n")
            summary.append(f"- Elements: {fp['elements']}\n")
            summary.append(f"- Layers: {', '.join(fp['layers'])}\n")
    
    summary_file = output_dir / 'ANALYSIS_SUMMARY.md'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.writelines(summary)
    
    print(f"✓ Summary saved to: {summary_file}")


if __name__ == '__main__':
    print("="*80)
    print("KiCad PCB Library Analysis")
    print("="*80)
    
    analyses = analyze_library_pcbs()
    
    print("\n" + "="*80)
    print("✓ Analysis Complete")
    print("="*80)
    print("\nNext steps:")
    print("1. Review kicad_knowledge_base/ANALYSIS_SUMMARY.md")
    print("2. Extract complete footprints")
    print("3. Create steering documentation")
    print("4. Update generators")
