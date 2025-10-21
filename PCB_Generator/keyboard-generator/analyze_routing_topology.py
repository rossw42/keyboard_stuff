#!/usr/bin/env python3
"""Analyze routing topology and identify patterns.

This script analyzes the extracted routing data to identify:
1. Matrix routing patterns (rows and columns)
2. Power distribution patterns
3. USB routing patterns
4. Common routing strategies
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict


def load_routing_data(routing_file: Path) -> Dict[str, Any]:
    """Load routing data from JSON file."""
    with open(routing_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_matrix_routing(routing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze keyboard matrix routing patterns.
    
    Args:
        routing_data: Routing data dictionary
        
    Returns:
        Dictionary with matrix routing analysis
    """
    nets = routing_data['nets']
    traces = routing_data['traces']
    
    # Find row and column nets
    row_nets = []
    col_nets = []
    
    for net in nets:
        name = net['name']
        if '/ROW' in name or 'ROW' in name:
            row_nets.append(net)
        elif '/COL' in name or 'COL' in name:
            col_nets.append(net)
    
    # Analyze traces for each row/column
    row_traces = defaultdict(list)
    col_traces = defaultdict(list)
    
    for trace in traces:
        net_num = trace['net']
        
        # Check if this trace belongs to a row or column
        for row_net in row_nets:
            if row_net['number'] == net_num:
                row_traces[row_net['name']].append(trace)
                break
        
        for col_net in col_nets:
            if col_net['number'] == net_num:
                col_traces[col_net['name']].append(trace)
                break
    
    # Analyze routing direction (horizontal vs vertical)
    def get_trace_direction(trace):
        """Determine if trace is more horizontal or vertical."""
        dx = abs(trace['end'][0] - trace['start'][0])
        dy = abs(trace['end'][1] - trace['start'][1])
        if dx > dy:
            return 'horizontal'
        else:
            return 'vertical'
    
    row_directions = defaultdict(int)
    col_directions = defaultdict(int)
    
    for row_name, traces_list in row_traces.items():
        for trace in traces_list:
            direction = get_trace_direction(trace)
            row_directions[direction] += 1
    
    for col_name, traces_list in col_traces.items():
        for trace in traces_list:
            direction = get_trace_direction(trace)
            col_directions[direction] += 1
    
    return {
        'row_count': len(row_nets),
        'col_count': len(col_nets),
        'row_nets': [net['name'] for net in row_nets],
        'col_nets': [net['name'] for net in col_nets],
        'row_trace_count': sum(len(traces) for traces in row_traces.values()),
        'col_trace_count': sum(len(traces) for traces in col_traces.values()),
        'row_directions': dict(row_directions),
        'col_directions': dict(col_directions)
    }


def analyze_power_routing(routing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze power distribution routing.
    
    Args:
        routing_data: Routing data dictionary
        
    Returns:
        Dictionary with power routing analysis
    """
    nets = routing_data['nets']
    traces = routing_data['traces']
    vias = routing_data['vias']
    zones = routing_data['zones']
    
    # Find power nets
    power_net_names = ['VCC', 'VDD', '+5V', '+3V3', '+3.3V', 'GND']
    power_nets = []
    
    for net in nets:
        name = net['name']
        if any(pwr in name for pwr in power_net_names):
            power_nets.append(net)
    
    # Analyze traces, vias, and zones for each power net
    power_analysis = {}
    
    for power_net in power_nets:
        net_num = power_net['number']
        net_name = power_net['name']
        
        # Count traces
        net_traces = [t for t in traces if t['net'] == net_num]
        
        # Count vias
        net_vias = [v for v in vias if v['net'] == net_num]
        
        # Count zones
        net_zones = [z for z in zones if z['net'] == net_num]
        
        # Analyze trace widths
        trace_widths = [t['width'] for t in net_traces]
        avg_width = sum(trace_widths) / len(trace_widths) if trace_widths else 0
        max_width = max(trace_widths) if trace_widths else 0
        
        power_analysis[net_name] = {
            'net_number': net_num,
            'trace_count': len(net_traces),
            'via_count': len(net_vias),
            'zone_count': len(net_zones),
            'avg_trace_width': round(avg_width, 3),
            'max_trace_width': round(max_width, 3),
            'uses_zones': len(net_zones) > 0
        }
    
    return power_analysis


def analyze_usb_routing(routing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze USB differential pair routing.
    
    Args:
        routing_data: Routing data dictionary
        
    Returns:
        Dictionary with USB routing analysis
    """
    nets = routing_data['nets']
    traces = routing_data['traces']
    
    # Find USB nets
    usb_dp_net = None
    usb_dm_net = None
    
    for net in nets:
        name = net['name']
        if 'USB_D+' in name or 'D+' in name or 'DP' in name:
            usb_dp_net = net
        elif 'USB_D-' in name or 'D-' in name or 'DM' in name:
            usb_dm_net = net
    
    if not usb_dp_net or not usb_dm_net:
        return {'found': False}
    
    # Analyze traces for USB nets
    dp_traces = [t for t in traces if t['net'] == usb_dp_net['number']]
    dm_traces = [t for t in traces if t['net'] == usb_dm_net['number']]
    
    # Analyze trace widths
    dp_widths = [t['width'] for t in dp_traces]
    dm_widths = [t['width'] for t in dm_traces]
    
    return {
        'found': True,
        'dp_net': usb_dp_net['name'],
        'dm_net': usb_dm_net['name'],
        'dp_trace_count': len(dp_traces),
        'dm_trace_count': len(dm_traces),
        'dp_avg_width': round(sum(dp_widths) / len(dp_widths), 3) if dp_widths else 0,
        'dm_avg_width': round(sum(dm_widths) / len(dm_widths), 3) if dm_widths else 0
    }


def analyze_layer_usage(routing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze how layers are used for routing.
    
    Args:
        routing_data: Routing data dictionary
        
    Returns:
        Dictionary with layer usage analysis
    """
    traces = routing_data['traces']
    vias = routing_data['vias']
    zones = routing_data['zones']
    
    # Count traces by layer
    traces_by_layer = defaultdict(int)
    for trace in traces:
        traces_by_layer[trace['layer']] += 1
    
    # Count zones by layer
    zones_by_layer = defaultdict(int)
    for zone in zones:
        zones_by_layer[zone['layer']] += 1
    
    return {
        'traces_by_layer': dict(traces_by_layer),
        'zones_by_layer': dict(zones_by_layer),
        'via_count': len(vias),
        'uses_both_layers': 'F.Cu' in traces_by_layer and 'B.Cu' in traces_by_layer
    }


def analyze_pcb(routing_file: Path) -> Dict[str, Any]:
    """Analyze a single PCB's routing patterns.
    
    Args:
        routing_file: Path to routing JSON file
        
    Returns:
        Dictionary with complete analysis
    """
    routing_data = load_routing_data(routing_file)
    
    print(f"\nAnalyzing: {routing_data['project']} - {routing_data['pcb_name']}")
    
    analysis = {
        'project': routing_data['project'],
        'pcb_name': routing_data['pcb_name'],
        'source_file': routing_data['source_file'],
        'stats': routing_data['stats'],
        'matrix': analyze_matrix_routing(routing_data),
        'power': analyze_power_routing(routing_data),
        'usb': analyze_usb_routing(routing_data),
        'layers': analyze_layer_usage(routing_data)
    }
    
    # Print summary
    print(f"  Matrix: {analysis['matrix']['row_count']} rows × {analysis['matrix']['col_count']} cols")
    print(f"  Matrix traces: {analysis['matrix']['row_trace_count']} row, {analysis['matrix']['col_trace_count']} col")
    
    if analysis['matrix']['row_directions']:
        print(f"  Row routing: {analysis['matrix']['row_directions']}")
    if analysis['matrix']['col_directions']:
        print(f"  Col routing: {analysis['matrix']['col_directions']}")
    
    print(f"  Power nets: {len(analysis['power'])}")
    for net_name, info in analysis['power'].items():
        if info['trace_count'] > 0 or info['zone_count'] > 0:
            print(f"    {net_name}: {info['trace_count']} traces, {info['zone_count']} zones, {info['avg_trace_width']}mm avg width")
    
    if analysis['usb']['found']:
        print(f"  USB: {analysis['usb']['dp_trace_count']} D+ traces, {analysis['usb']['dm_trace_count']} D- traces")
    
    print(f"  Layers: {analysis['layers']['traces_by_layer']}")
    
    return analysis


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    routing_dir = script_dir / "routing_data"
    
    if not routing_dir.exists():
        print(f"Error: Routing data directory not found: {routing_dir}")
        print("Run extract_routing_patterns.py first")
        sys.exit(1)
    
    # Find all routing JSON files (except summary)
    routing_files = [f for f in routing_dir.glob("*_routing.json") if f.name != "routing_summary.json"]
    
    print(f"Found {len(routing_files)} routing files")
    
    # Analyze each PCB
    all_analyses = []
    
    for routing_file in sorted(routing_files):
        try:
            analysis = analyze_pcb(routing_file)
            all_analyses.append(analysis)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Save analyses
    output_file = routing_dir / "routing_topology_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_analyses, f, indent=2)
    
    print(f"\n✓ Analysis complete!")
    print(f"✓ Saved to: {output_file}")
    
    # Print summary of best examples
    print("\n" + "="*80)
    print("BEST EXAMPLES FOR ROUTING PATTERNS")
    print("="*80)
    
    # Find PCBs with most matrix traces
    matrix_pcbs = [a for a in all_analyses if a['matrix']['row_trace_count'] > 0]
    matrix_pcbs.sort(key=lambda x: x['matrix']['row_trace_count'] + x['matrix']['col_trace_count'], reverse=True)
    
    print("\nBest for matrix routing:")
    for analysis in matrix_pcbs[:5]:
        total_matrix = analysis['matrix']['row_trace_count'] + analysis['matrix']['col_trace_count']
        print(f"  {analysis['project']:15s} {analysis['pcb_name']:25s} {total_matrix:4d} matrix traces")
    
    # Find PCBs with USB routing
    usb_pcbs = [a for a in all_analyses if a['usb']['found']]
    print(f"\nPCBs with USB routing: {len(usb_pcbs)}")
    for analysis in usb_pcbs[:5]:
        print(f"  {analysis['project']:15s} {analysis['pcb_name']:25s}")


if __name__ == "__main__":
    main()
