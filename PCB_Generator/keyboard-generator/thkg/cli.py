"""Command-line interface for THKG"""

import click
from pathlib import Path
from thkg.config import Configuration, KeyboardType, LayoutStyle
from thkg.input import YAMLParser, KLEParser, InputValidator
from thkg.layout import LayoutPresets, PositionCalculator, MatrixCalculator, PinAssigner
from thkg.plate import PlateGenerator, DXFWriter


@click.group()
@click.version_option(version='0.1.0')
def main():
    """Through-Hole Keyboard Generator (THKG)
    
    Generate complete keyboard designs from high-level specifications.
    """
    pass


@main.command()
@click.option('--output', '-o', default='config.yaml', help='Output configuration file')
def interactive(output):
    """Interactive configuration builder"""
    click.echo("=== Through-Hole Keyboard Generator ===\n")
    
    # Get keyboard name
    name = click.prompt("Keyboard name", default="MyKeyboard")
    
    # Get keyboard type
    kb_type = click.prompt(
        "What are you building?",
        type=click.Choice(['keyboard', 'numpad', 'macropad'], case_sensitive=False),
        default='keyboard'
    )
    
    # Get layout style
    if kb_type == 'keyboard':
        style = click.prompt(
            "Layout style?",
            type=click.Choice(['staggered', 'ortho', 'custom'], case_sensitive=False),
            default='staggered'
        )
    else:
        style = 'ortho'  # Numpads and macropads are typically ortho
    
    # Get specific layout
    preset = _get_layout_preset(kb_type, style)
    
    # Create configuration
    config = Configuration()
    config.name = name
    config.layout_preset = preset
    
    # Save configuration
    parser = YAMLParser()
    parser.save(config, output)
    
    click.echo(f"\n✓ Configuration saved to {output}")
    click.echo(f"  Next: thkg generate {output}")


def _get_layout_preset(kb_type: str, style: str) -> str:
    """Get layout preset based on type and style"""
    presets = LayoutPresets.list_presets()
    
    # Filter presets by type and style
    if kb_type == 'keyboard':
        if style == 'staggered':
            options = ['60-ansi', '65-ansi', 'tkl', '40-ansi']
        elif style == 'ortho':
            options = ['60-ortho', '40-ortho', '50-ortho']
        else:  # custom
            kle_file = click.prompt("KLE JSON file path")
            return f"custom:{kle_file}"
    elif kb_type == 'numpad':
        options = ['numpad-standard', 'numpad-compact', 'numpad-extended']
    else:  # macropad
        options = ['macropad-3x3', 'macropad-4x4', 'macropad-2x3']
    
    # Show options
    click.echo("\nAvailable layouts:")
    for i, opt in enumerate(options, 1):
        click.echo(f"  {i}. {presets[opt]}")
    
    # Get selection
    choice = click.prompt("Select layout", type=click.IntRange(1, len(options)))
    return options[choice - 1]


@main.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--output-dir', '-o', default='output', help='Output directory')
def generate(config_file, output_dir):
    """Generate keyboard design from configuration file"""
    click.echo(f"Loading configuration from {config_file}...")
    
    # Parse configuration
    parser = YAMLParser()
    config = parser.parse(config_file)
    
    # Validate configuration
    validator = InputValidator()
    is_valid, errors = validator.validate(config)
    if not is_valid:
        click.echo("❌ Configuration validation failed:", err=True)
        for error in errors:
            click.echo(f"  - {error}", err=True)
        return
    
    click.echo(f"✓ Configuration valid: {config.name}")
    
    # Create output directory
    output_path = Path(output_dir) / config.name
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load layout
    switches = _load_layout(config)
    click.echo(f"✓ Loaded layout: {len(switches)} switches")
    
    # Calculate matrix
    matrix_calc = MatrixCalculator()
    matrix = matrix_calc.calculate_matrix(switches)
    config.matrix = matrix
    click.echo(f"✓ Matrix: {matrix.rows}x{matrix.cols}")
    
    # Assign pins
    pin_assigner = PinAssigner()
    config.matrix = pin_assigner.assign_pins(matrix, config.mcu_type)
    click.echo(f"✓ Pins assigned: {len(config.matrix.row_pins)} rows, {len(config.matrix.col_pins)} cols")
    
    # Generate plate if enabled
    if config.plate.enabled:
        click.echo("\nGenerating plate...")
        plate_gen = PlateGenerator()
        plate_data = plate_gen.generate_plate(switches, config.plate)
        
        # Write DXF
        dxf_writer = DXFWriter()
        plate_path = output_path / "plate.dxf"
        dxf_writer.write_plate(plate_data, str(plate_path))
        click.echo(f"✓ Plate saved: {plate_path}")
    
    click.echo(f"\n✓ Generation complete! Output: {output_path}")


def _load_layout(config: Configuration) -> list:
    """Load layout from configuration"""
    # Check if KLE file specified
    if config.kle_file:
        kle_parser = KLEParser()
        switches, _ = kle_parser.parse(config.kle_file)
        return switches
    
    # Check if custom switches specified
    if config.switches:
        return config.switches
    
    # Load preset
    if config.layout_preset:
        return LayoutPresets.get_preset(config.layout_preset)
    
    raise ValueError("No layout specified")


@main.command()
def list_presets():
    """List all available layout presets"""
    presets = LayoutPresets.list_presets()
    
    click.echo("Available layout presets:\n")
    
    # Group by category
    categories = {
        'Keyboards (Staggered)': [],
        'Keyboards (Ortho)': [],
        'Numpads': [],
        'Macropads': []
    }
    
    for name, desc in presets.items():
        if 'ortho' in name.lower() and 'numpad' not in name and 'macro' not in name:
            categories['Keyboards (Ortho)'].append((name, desc))
        elif 'numpad' in name.lower():
            categories['Numpads'].append((name, desc))
        elif 'macro' in name.lower():
            categories['Macropads'].append((name, desc))
        else:
            categories['Keyboards (Staggered)'].append((name, desc))
    
    for category, items in categories.items():
        if items:
            click.echo(f"{category}:")
            for name, desc in items:
                click.echo(f"  {name:20s} - {desc}")
            click.echo()


if __name__ == '__main__':
    main()
