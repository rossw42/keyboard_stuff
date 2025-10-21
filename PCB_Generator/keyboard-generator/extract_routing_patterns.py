#!/usr/bin/env python3
"""Extract routing patterns from all PCBs in the library.

This script:
1. Finds all .kicad_pcb files in pcb-library/design-files
2. Parses each PCB to extract routing data (traces, vias, zones)
3. Analyzes routing patterns and topology
4. Saves routing data to JSON files for later use
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import asdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from thkg.templates.pcb_parser import parse_kicad_pcb
from thkg.templates.models import PCBRouting


def find_all_pcb_files(library_path: Path) -> List[Path]:
    """Find all .kicad_pcb files in the library.
    
    Args:
        library_path: Path to pcb-library directory
        
    Returns:
        List of paths to .kicad_pcb files
    """
    design_files_path = library_path / "design-files"
    
    if not design_files_path.exists():
        raise FileNotFoundError(f"Design files directory not found: {design_files_path}")
    
    # Find all .kicad_pcb files
    pcb_files = list(design_files_path.glob("**/kicad/*.kicad_pcb"))
    
    # Filter out plate/bottom/cover files (we want main PCBs)
    main_pcbs = []
    for pcb_file in pcb_files:
        name_lower = pcb_file.stem.lower()
        # Skip non-main PCBs
        if any(skip in name_lower for skip in ['plate', 'bottom', 'cover', 'guard', 'base_plate']):
            continue
        main_pcbs.append(pcb_file)
    
    return sorted(main_pcbs)


def extract_routing_from_pcb(pcb_path: Path) -> Dict[str, Any]:
    """Extract routing information from a PCB file.
    
    Args:
        pcb_path: Path to .kicad_pcb file
        
    Returns:
        Dictionary with routing data
    """
    print(f"\nParsing: {pcb_path.name}")
    print(f"  Project: {pcb_path.parent.parent.name}")
    
    try:
        routing = parse_kicad_pcb(pcb_path)
        
        print(f"  ✓ Nets: {len(routing.nets)}")
        print(f"  ✓ Traces: {len(routing.traces)}")
        print(f"  ✓ Vias: {len(routing.vias)}")
        print(f"  ✓ Zones: {len(routing.zones)}")
        
        # Analyze routing by layer
        traces_by_layer = {}
        for trace in routing.traces:
            layer = trace.layer
            if layer not in traces_by_layer:
                traces_by_layer[layer] = 0
            traces_by_layer[layer] += 1
        
        print(f"  Traces by layer:")
        for layer, count in sorted(traces_by_layer.items()):
            print(f"    {layer}: {count}")
        
        # Analyze routing by net
        important_nets = ['GND', 'VCC', 'VDD', '+5V', '+3V3']
        for net_name in important_nets:
            net = routing.get_net_by_name(net_name)
            if net:
                traces = routing.get_traces_for_net(net.number)
                vias = routing.get_vias_for_net(net.number)
                print(f"  {net_name}: {len(traces)} traces, {len(vias)} vias")
        
        # Convert to dictionary for JSON serialization
        result = {
            'source_file': str(pcb_path),
            'project': pcb_path.parent.parent.name,
            'pcb_name': pcb_path.stem,
            'nets': [asdict(net) for net in routing.nets],
            'traces': [asdict(trace) for trace in routing.traces],
            'vias': [asdict(via) for via in routing.vias],
            'zones': [asdict(zone) for zone in routing.zones],
            'stats': {
                'net_count': len(routing.nets),
                'trace_count': len(routing.traces),
                'via_count': len(routing.vias),
                'zone_count': len(routing.zones),
                'traces_by_layer': traces_by_layer
            }
        }
        
        return result
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def save_routing_data(routing_data: Dict[str, Any], output_dir: Path):
    """Save routing data to JSON file.
    
    Args:
        routing_data: Routing data dictionary
        output_dir: Output directory for JSON files
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    project = routing_data['project']
    pcb_name = routing_data['pcb_name']
    
    output_file = output_dir / f"{project}_{pcb_name}_routing.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(routing_data, f, indent=2)
    
    print(f"  → Saved to: {output_file.name}")


def analyze_routing_patterns(all_routing_data: List[Dict[str, Any]]):
    """Analyze routing patterns across all PCBs.
    
    Args:
        all_routing_data: List of routing data dictionaries
    """
    print("\n" + "="*80)
    print("ROUTING PATTERN ANALYSIS")
    print("="*80)
    
    total_traces = sum(data['stats']['trace_count'] for data in all_routing_data)
    total_vias = sum(data['stats']['via_count'] for data in all_routing_data)
    total_zones = sum(data['stats']['zone_count'] for data in all_routing_data)
    
    print(f"\nTotal across {len(all_routing_data)} PCBs:")
    print(f"  Traces: {total_traces}")
    print(f"  Vias: {total_vias}")
    print(f"  Zones: {total_zones}")
    
    # Find PCBs with most routing
    print(f"\nPCBs by trace count:")
    sorted_by_traces = sorted(all_routing_data, key=lambda x: x['stats']['trace_count'], reverse=True)
    for data in sorted_by_traces[:10]:
        print(f"  {data['project']:15s} {data['pcb_name']:25s} {data['stats']['trace_count']:5d} traces")
    
    # Analyze common nets
    net_names = {}
    for data in all_routing_data:
        for net in data['nets']:
            name = net['name']
            if name:  # Skip empty net names
                if name not in net_names:
                    net_names[name] = 0
                net_names[name] += 1
    
    print(f"\nMost common net names:")
    sorted_nets = sorted(net_names.items(), key=lambda x: x[1], reverse=True)
    for net_name, count in sorted_nets[:20]:
        print(f"  {net_name:20s} {count:3d} PCBs")


def main():
    """Main entry point."""
    # Find library path
    script_dir = Path(__file__).parent
    library_path = script_dir.parent / "pcb-library"
    
    if not library_path.exists():
        print(f"Error: PCB library not found at {library_path}")
        sys.exit(1)
    
    print(f"PCB Library: {library_path}")
    
    # Find all PCB files
    pcb_files = find_all_pcb_files(library_path)
    print(f"\nFound {len(pcb_files)} main PCB files")
    
    # Extract routing from each PCB
    all_routing_data = []
    output_dir = script_dir / "routing_data"
    
    for pcb_file in pcb_files:
        routing_data = extract_routing_from_pcb(pcb_file)
        if routing_data:
            all_routing_data.append(routing_data)
            save_routing_data(routing_data, output_dir)
    
    # Analyze patterns
    if all_routing_data:
        analyze_routing_patterns(all_routing_data)
        
        # Save summary
        summary_file = output_dir / "routing_summary.json"
        summary = {
            'total_pcbs': len(all_routing_data),
            'total_traces': sum(d['stats']['trace_count'] for d in all_routing_data),
            'total_vias': sum(d['stats']['via_count'] for d in all_routing_data),
            'total_zones': sum(d['stats']['zone_count'] for d in all_routing_data),
            'pcbs': [
                {
                    'project': d['project'],
                    'pcb_name': d['pcb_name'],
                    'stats': d['stats']
                }
                for d in all_routing_data
            ]
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Summary saved to: {summary_file}")
    
    print(f"\n✓ Extraction complete! Processed {len(all_routing_data)} PCBs")
    print(f"✓ Routing data saved to: {output_dir}")


if __name__ == "__main__":
    main()
