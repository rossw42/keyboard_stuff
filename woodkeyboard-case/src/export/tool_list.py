"""
Tool list document generation for CNC machining.

This module generates comprehensive tool lists with specifications,
feeds and speeds, and tool change sequences for efficient machining.

Requirements: 6.4, 8.2
"""

from typing import Dict, Any, List
from pathlib import Path


def generate_tool_list_document(
    top_frame_toolpaths: Dict[str, Any],
    bottom_tray_toolpaths: Dict[str, Any],
    output_path: str = "output/60_percent_standard/cnc/setup"
) -> str:
    """
    Generate comprehensive tool list document for both components.
    
    Args:
        top_frame_toolpaths: Top frame toolpaths dictionary
        bottom_tray_toolpaths: Bottom tray toolpaths dictionary
        output_path: Output directory path
        
    Returns:
        Path to the generated tool list document
        
    Requirements: 6.4, 8.2
    """
    # Create output directory
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all unique tools from both components
    tools = _collect_tools(top_frame_toolpaths, bottom_tray_toolpaths)
    
    # Generate document content
    content = _generate_tool_list_content(tools)
    
    # Write to file
    filepath = output_dir / "tool_list.md"
    with open(filepath, 'w') as f:
        f.write(content)
    
    return str(filepath)


def _collect_tools(
    top_frame_toolpaths: Dict[str, Any],
    bottom_tray_toolpaths: Dict[str, Any]
) -> Dict[str, Dict[str, Any]]:
    """
    Collect all unique tools from toolpath operations.
    
    Returns:
        Dictionary of tools with their specifications and usage
    """
    tools = {}
    
    # Process top frame operations
    for op_name, op_data in top_frame_toolpaths.get('operations', {}).items():
        _extract_tools_from_operation(tools, op_data, 'top_frame', op_name)
    
    # Process bottom tray operations
    for op_name, op_data in bottom_tray_toolpaths.get('operations', {}).items():
        _extract_tools_from_operation(tools, op_data, 'bottom_tray', op_name)
    
    return tools


def _extract_tools_from_operation(
    tools: Dict[str, Dict[str, Any]],
    operation: Dict[str, Any],
    component: str,
    operation_name: str
):
    """Extract tool information from an operation."""
    # Handle simple operations with single tool
    if 'tool' in operation:
        tool_info = operation['tool']
        params = operation.get('parameters', {})
        _add_tool(tools, tool_info, params, component, operation_name)
    
    # Handle roughing/finishing operations
    if 'roughing' in operation:
        roughing = operation['roughing']
        tool_info = roughing.get('tool', {})
        params = roughing.get('parameters', {})
        _add_tool(tools, tool_info, params, component, f"{operation_name}_roughing")
    
    if 'finishing' in operation:
        finishing = operation['finishing']
        tool_info = finishing.get('tool', {})
        params = finishing.get('parameters', {})
        _add_tool(tools, tool_info, params, component, f"{operation_name}_finishing")


def _add_tool(
    tools: Dict[str, Dict[str, Any]],
    tool_info: Dict[str, Any],
    params: Dict[str, Any],
    component: str,
    operation: str
):
    """Add tool to the tools dictionary."""
    diameter = tool_info.get('diameter', 0)
    tool_type = tool_info.get('type', 'unknown')
    
    # Create unique tool key
    tool_key = f"{diameter}mm_{tool_type}"
    
    if tool_key not in tools:
        tools[tool_key] = {
            'diameter': diameter,
            'type': tool_type,
            'flutes': tool_info.get('flutes', 2),
            'description': tool_info.get('description', ''),
            'feed_rates': set(),
            'spindle_speeds': set(),
            'operations': []
        }
    
    # Add feed rate and spindle speed
    if 'feed_rate' in params:
        tools[tool_key]['feed_rates'].add(params['feed_rate'])
    if 'spindle_speed' in params:
        tools[tool_key]['spindle_speeds'].add(params['spindle_speed'])
    
    # Add operation usage
    tools[tool_key]['operations'].append({
        'component': component,
        'operation': operation
    })


def _generate_tool_list_content(tools: Dict[str, Dict[str, Any]]) -> str:
    """Generate the tool list document content."""
    lines = [
        "# CNC Tool List",
        "",
        "Complete list of required tools for machining the 60% keyboard case.",
        "",
        "## Tool Specifications",
        ""
    ]
    
    # Sort tools by type and diameter
    sorted_tools = sorted(
        tools.items(),
        key=lambda x: (x[1]['type'], x[1]['diameter'])
    )
    
    # Group tools by type
    endmills = []
    drills = []
    
    for tool_key, tool_data in sorted_tools:
        if tool_data['type'] == 'flat_endmill':
            endmills.append((tool_key, tool_data))
        elif tool_data['type'] == 'drill':
            drills.append((tool_key, tool_data))
    
    # Add endmills section
    if endmills:
        lines.extend([
            "### Flat Endmills",
            ""
        ])
        
        for tool_key, tool_data in endmills:
            lines.extend(_format_tool_entry(tool_key, tool_data))
    
    # Add drills section
    if drills:
        lines.extend([
            "### Drills",
            ""
        ])
        
        for tool_key, tool_data in drills:
            lines.extend(_format_tool_entry(tool_key, tool_data))
    
    # Add feeds and speeds section
    lines.extend([
        "",
        "## Recommended Feeds and Speeds for Hardwood",
        "",
        "These values are optimized for hardwoods (walnut, maple, cherry).",
        ""
    ])
    
    # Create feeds and speeds table
    lines.extend([
        "| Tool | Diameter | Feed Rate | Spindle Speed | Application |",
        "|------|----------|-----------|---------------|-------------|"
    ])
    
    for tool_key, tool_data in sorted_tools:
        diameter = tool_data['diameter']
        tool_type = tool_data['type'].replace('_', ' ').title()
        
        # Get feed rates and spindle speeds
        feed_rates = sorted(tool_data['feed_rates'])
        spindle_speeds = sorted(tool_data['spindle_speeds'])
        
        feed_rate_str = f"{min(feed_rates)}-{max(feed_rates)}" if len(feed_rates) > 1 else str(feed_rates[0]) if feed_rates else "N/A"
        spindle_speed_str = f"{min(spindle_speeds)}-{max(spindle_speeds)}" if len(spindle_speeds) > 1 else str(spindle_speeds[0]) if spindle_speeds else "N/A"
        
        # Determine application
        application = _determine_application(tool_data)
        
        lines.append(
            f"| {tool_type} | {diameter}mm | {feed_rate_str} mm/min | {spindle_speed_str} RPM | {application} |"
        )
    
    # Add tool change sequence
    lines.extend([
        "",
        "## Tool Change Sequence for Efficiency",
        "",
        "Recommended tool change sequence to minimize tool changes during machining.",
        "",
        "### Top Frame Sequence",
        ""
    ])
    
    top_frame_sequence = _generate_tool_change_sequence('top_frame', tools)
    for i, (tool, operations) in enumerate(top_frame_sequence, 1):
        lines.append(f"{i}. **{tool}** - {', '.join(operations)}")
    
    lines.extend([
        "",
        "### Bottom Tray Sequence",
        ""
    ])
    
    bottom_tray_sequence = _generate_tool_change_sequence('bottom_tray', tools)
    for i, (tool, operations) in enumerate(bottom_tray_sequence, 1):
        lines.append(f"{i}. **{tool}** - {', '.join(operations)}")
    
    # Add notes section
    lines.extend([
        "",
        "## Notes",
        "",
        "- All feed rates and spindle speeds are recommendations for hardwood",
        "- Adjust based on specific wood species and machine capabilities",
        "- Use sharp tools for best results and to prevent tear-out",
        "- Climb milling recommended for better surface finish",
        "- Peck drilling recommended for holes deeper than 3x diameter",
        "- Check tool condition before starting each operation",
        ""
    ])
    
    return '\n'.join(lines)


def _format_tool_entry(tool_key: str, tool_data: Dict[str, Any]) -> List[str]:
    """Format a single tool entry."""
    lines = [
        f"#### {tool_data['diameter']}mm {tool_data['type'].replace('_', ' ').title()}",
        ""
    ]
    
    # Add specifications
    lines.append(f"- **Diameter:** {tool_data['diameter']}mm")
    lines.append(f"- **Type:** {tool_data['type'].replace('_', ' ').title()}")
    lines.append(f"- **Flutes:** {tool_data['flutes']}")
    
    if tool_data['description']:
        lines.append(f"- **Description:** {tool_data['description']}")
    
    # Add feed rates
    if tool_data['feed_rates']:
        feed_rates = sorted(tool_data['feed_rates'])
        if len(feed_rates) == 1:
            lines.append(f"- **Feed Rate:** {feed_rates[0]} mm/min")
        else:
            lines.append(f"- **Feed Rate Range:** {min(feed_rates)}-{max(feed_rates)} mm/min")
    
    # Add spindle speeds
    if tool_data['spindle_speeds']:
        spindle_speeds = sorted(tool_data['spindle_speeds'])
        if len(spindle_speeds) == 1:
            lines.append(f"- **Spindle Speed:** {spindle_speeds[0]} RPM")
        else:
            lines.append(f"- **Spindle Speed Range:** {min(spindle_speeds)}-{max(spindle_speeds)} RPM")
    
    # Add operations
    lines.append(f"- **Used in {len(tool_data['operations'])} operations:**")
    for op in tool_data['operations']:
        component = op['component'].replace('_', ' ').title()
        operation = op['operation'].replace('_', ' ').title()
        lines.append(f"  - {component}: {operation}")
    
    lines.append("")
    
    return lines


def _determine_application(tool_data: Dict[str, Any]) -> str:
    """Determine the primary application for a tool."""
    operations = tool_data['operations']
    
    # Check for common operation types
    op_names = [op['operation'].lower() for op in operations]
    
    if any('roughing' in name for name in op_names):
        return "Roughing"
    elif any('finishing' in name for name in op_names):
        return "Finishing"
    elif any('surfacing' in name for name in op_names):
        return "Surfacing"
    elif any('drill' in name or 'hole' in name for name in op_names):
        return "Drilling"
    elif any('counterbore' in name for name in op_names):
        return "Counterboring"
    elif any('profile' in name for name in op_names):
        return "Profile cutting"
    else:
        return "General"


def _generate_tool_change_sequence(
    component: str,
    tools: Dict[str, Dict[str, Any]]
) -> List[tuple]:
    """Generate optimal tool change sequence for a component."""
    # Collect operations for this component
    component_ops = {}
    
    for tool_key, tool_data in tools.items():
        for op in tool_data['operations']:
            if op['component'] == component:
                if tool_key not in component_ops:
                    component_ops[tool_key] = []
                component_ops[tool_key].append(op['operation'])
    
    # Sort by operation order (assuming numbered operations)
    sequence = []
    for tool_key in sorted(component_ops.keys(), key=lambda x: tools[x]['diameter'], reverse=True):
        tool_name = f"{tools[tool_key]['diameter']}mm {tools[tool_key]['type'].replace('_', ' ')}"
        operations = sorted(component_ops[tool_key])
        sequence.append((tool_name, operations))
    
    return sequence
