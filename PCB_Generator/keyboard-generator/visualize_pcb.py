#!/usr/bin/env python3
"""Visualize PCB layout as PNG."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
from thkg.config import Configuration
from thkg.pcb.pcb_generator import PCBGenerator


def visualize_pcb(generator: PCBGenerator, output_path: Path):
    """Create visual representation of PCB.
    
    Args:
        generator: PCB generator with layout
        output_path: Path to save PNG
    """
    if not generator.layout_gen:
        print("❌ No layout generated yet")
        return
    
    layout = generator.layout_gen
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Set up axes
    ax.set_xlim(0, layout.board_width)
    ax.set_ylim(0, layout.board_height)
    ax.set_aspect('equal')
    ax.invert_yaxis()  # PCB coordinates
    
    # Draw board outline
    board_rect = patches.Rectangle(
        (0, 0), layout.board_width, layout.board_height,
        linewidth=2, edgecolor='black', facecolor='#2d5016', alpha=0.3
    )
    ax.add_patch(board_rect)
    
    # Draw mounting holes
    for x, y in layout.get_mounting_holes():
        hole = patches.Circle((x, y), 1.5, color='black', alpha=0.5)
        ax.add_patch(hole)
    
    # Draw components
    for comp in generator.schematic_gen.components:
        if not comp.position:
            continue
        
        x, y = comp.position
        
        # Switches - large squares
        if comp.reference.startswith('SW') or comp.reference.startswith('MX'):
            rect = patches.Rectangle(
                (x - 7, y - 7), 14, 14,
                linewidth=1.5, edgecolor='#1f77b4', facecolor='#aec7e8', alpha=0.8
            )
            ax.add_patch(rect)
            ax.text(x, y, comp.reference, ha='center', va='center', 
                   fontsize=6, fontweight='bold')
        
        # Diodes - small rectangles
        elif comp.reference.startswith('D') and '4148' in comp.value:
            rect = patches.Rectangle(
                (x - 1.5, y - 3), 3, 6,
                linewidth=1, edgecolor='#ff7f0e', facecolor='#ffbb78', alpha=0.8
            )
            ax.add_patch(rect)
        
        # MCU - large rectangle
        elif comp.reference.startswith('U'):
            rect = patches.Rectangle(
                (x - 15, y - 8), 30, 16,
                linewidth=2, edgecolor='#d62728', facecolor='#ff9896', alpha=0.9
            )
            ax.add_patch(rect)
            ax.text(x, y, f"{comp.reference}\n{comp.value}", 
                   ha='center', va='center', fontsize=7, fontweight='bold')
        
        # USB connector
        elif 'USB' in comp.symbol.upper():
            rect = patches.Rectangle(
                (x - 8, y - 4), 16, 8,
                linewidth=2, edgecolor='#9467bd', facecolor='#c5b0d5', alpha=0.9
            )
            ax.add_patch(rect)
            ax.text(x, y, 'USB', ha='center', va='center', 
                   fontsize=8, fontweight='bold')
        
        # Resistors
        elif comp.reference.startswith('R'):
            rect = patches.Rectangle(
                (x - 1, y - 2), 2, 4,
                linewidth=0.8, edgecolor='#8c564b', facecolor='#c49c94', alpha=0.8
            )
            ax.add_patch(rect)
        
        # Capacitors
        elif comp.reference.startswith('C'):
            circle = patches.Circle((x, y), 1.5, 
                                   edgecolor='#e377c2', facecolor='#f7b6d2', 
                                   linewidth=0.8, alpha=0.8)
            ax.add_patch(circle)
        
        # Crystal
        elif comp.reference.startswith('Y'):
            rect = patches.Rectangle(
                (x - 2, y - 3), 4, 6,
                linewidth=1, edgecolor='#7f7f7f', facecolor='#c7c7c7', alpha=0.8
            )
            ax.add_patch(rect)
            ax.text(x, y, 'XTAL', ha='center', va='center', fontsize=5)
        
        # Other components
        else:
            circle = patches.Circle((x, y), 1, color='gray', alpha=0.5)
            ax.add_patch(circle)
    
    # Add title and labels
    keyboard_name = generator.config.keyboard.get('name', 'Keyboard')
    ax.set_title(f'{keyboard_name} PCB Layout', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('X (mm)', fontsize=12)
    ax.set_ylabel('Y (mm)', fontsize=12)
    
    # Add legend
    legend_elements = [
        patches.Patch(facecolor='#aec7e8', edgecolor='#1f77b4', label='Switches'),
        patches.Patch(facecolor='#ffbb78', edgecolor='#ff7f0e', label='Diodes'),
        patches.Patch(facecolor='#ff9896', edgecolor='#d62728', label='MCU'),
        patches.Patch(facecolor='#c5b0d5', edgecolor='#9467bd', label='USB'),
        patches.Patch(facecolor='#c49c94', edgecolor='#8c564b', label='Resistors'),
        patches.Patch(facecolor='#f7b6d2', edgecolor='#e377c2', label='Capacitors'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Add info text
    info_text = f"Components: {len(generator.schematic_gen.components)}\n"
    info_text += f"Connections: {len(generator.schematic_gen.connections)}\n"
    info_text += f"Board: {layout.board_width}mm × {layout.board_height}mm"
    ax.text(5, layout.board_height - 5, info_text, 
           fontsize=9, verticalalignment='bottom',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Saved visualization to {output_path}")
    plt.close()


def main():
    """Generate and visualize PCBs."""
    
    print("=" * 80)
    print("PCB Visualization Generator")
    print("=" * 80)
    print()
    
    # Generate 3x3 macropad
    print("📦 Generating 3x3 Macropad...")
    config1 = Configuration()
    config1.keyboard = {
        'name': '3x3-Macropad',
        'description': '3x3 macropad',
        'version': '1.0',
    }
    config1.layout = {
        'type': 'macropad-3x3',
        'switches': [{'row': i // 3, 'col': i % 3} for i in range(9)],
    }
    config1.hardware = {'mcu': {'type': 'atmega328p'}}
    
    gen1 = PCBGenerator(config1)
    gen1.generate(Path("output/viz-3x3"))
    visualize_pcb(gen1, Path("output/viz-3x3/pcb-layout.png"))
    
    print()
    
    # Generate 4x4 macropad
    print("📦 Generating 4x4 Macropad...")
    config2 = Configuration()
    config2.keyboard = {
        'name': '4x4-Macropad',
        'description': '4x4 macropad',
        'version': '1.0',
    }
    config2.layout = {
        'type': 'macropad-4x4',
        'switches': [{'row': i // 4, 'col': i % 4} for i in range(16)],
    }
    config2.hardware = {'mcu': {'type': 'atmega328p'}}
    
    gen2 = PCBGenerator(config2)
    gen2.generate(Path("output/viz-4x4"))
    visualize_pcb(gen2, Path("output/viz-4x4/pcb-layout.png"))
    
    print()
    
    # Generate 40% keyboard
    print("📦 Generating 40% Keyboard...")
    config3 = Configuration()
    config3.keyboard = {
        'name': '40-Percent-Keyboard',
        'description': '40% ortholinear',
        'version': '1.0',
    }
    config3.layout = {
        'type': '40-ortho',
        'switches': [{'row': i // 12, 'col': i % 12} for i in range(48)],
    }
    config3.hardware = {'mcu': {'type': 'atmega328p'}}
    
    gen3 = PCBGenerator(config3)
    gen3.generate(Path("output/viz-40percent"))
    visualize_pcb(gen3, Path("output/viz-40percent/pcb-layout.png"))
    
    print()
    print("=" * 80)
    print("✅ Visualization Complete!")
    print("=" * 80)
    print()
    print("Generated visualizations:")
    print("  • output/viz-3x3/pcb-layout.png")
    print("  • output/viz-4x4/pcb-layout.png")
    print("  • output/viz-40percent/pcb-layout.png")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
