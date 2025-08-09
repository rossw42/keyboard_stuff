#!/usr/bin/env python3
"""
KLE to Ergogen CLI Tool

Command line interface for converting KLE layouts to Ergogen points format.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# Add the parent directory to Python path to import from qmk_format_converter and kle_to_ergogen
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from kle_to_ergogen.parsers.kle_to_ergogen_converter import (
        KLEToErgogenConverter, 
        KLEToErgogenError,
        convert_kle_file
    )
    from kle_to_ergogen.generators.ergogen_yaml_generator import (
        ErgogenYAMLGenerator,
        ErgogenYAMLGeneratorError
    )
    from kle_to_ergogen.data_models.ergogen_point import (
        MatrixNamingStrategy,
        SequentialNamingStrategy,
        LabelNamingStrategy
    )
except ImportError as e:
    print(f"Error importing KLE to Ergogen modules: {e}")
    print("Make sure you're running from the correct directory and dependencies are installed.")
    print("Current working directory:", os.getcwd())
    print("Python path:", sys.path[:3])  # Show first 3 paths
    sys.exit(1)


def get_naming_strategy(strategy_name: str):
    """Get naming strategy instance by name."""
    strategies = {
        'matrix': MatrixNamingStrategy,
        'sequential': SequentialNamingStrategy,
        'label': LabelNamingStrategy
    }
    
    if strategy_name not in strategies:
        raise ValueError(f"Unknown naming strategy: {strategy_name}")
    
    return strategies[strategy_name]()


def validate_input_file(file_path: str) -> None:
    """Validate input file exists and is readable."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Cannot read input file: {file_path}")
    
    # Check file extension
    if not file_path.lower().endswith('.json'):
        print(f"Warning: Input file '{file_path}' does not have .json extension")


def validate_output_file(file_path: str) -> None:
    """Validate output file path is writable."""
    output_dir = os.path.dirname(file_path) or '.'
    
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            raise PermissionError(f"Cannot create output directory: {e}")
    
    if not os.access(output_dir, os.W_OK):
        raise PermissionError(f"Cannot write to output directory: {output_dir}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Convert KLE (Keyboard Layout Editor) files to Ergogen points format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s layout.json                          # Convert to layout.yaml
  %(prog)s layout.json -o ergogen_points.yaml  # Convert to specific output file
  %(prog)s layout.json -s sequential           # Use sequential naming (key_0, key_1...)
  %(prog)s layout.json --section-only          # Generate only points section
  %(prog)s layout.json --no-comments           # Generate without comments
  %(prog)s layout.json --precision 2           # Use 2 decimal places for coordinates

Naming Strategies:
  matrix     : r0c1, r1c2, etc. (default)
  sequential : key_0, key_1, etc.
  label      : Use KLE labels when possible, fallback to matrix

Dependencies:
  - PyYAML: pip install PyYAML
        """
    )
    
    # Input/Output arguments
    parser.add_argument(
        'input_file',
        help='Input KLE JSON file path'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output YAML file path (default: input_file.yaml)',
        metavar='FILE'
    )
    
    # Conversion options
    parser.add_argument(
        '-s', '--naming-strategy',
        choices=['matrix', 'sequential', 'label'],
        default='matrix',
        help='Point naming strategy (default: matrix)'
    )
    
    parser.add_argument(
        '--key-unit-size',
        type=float,
        default=19.05,
        metavar='MM',
        help='Key unit size in millimeters (default: 19.05)'
    )
    
    parser.add_argument(
        '--no-center',
        action='store_true',
        help='Do not center layout on origin'
    )
    
    parser.add_argument(
        '--no-invert-y',
        action='store_true',
        help='Do not invert Y-axis (keep KLE orientation)'
    )
    
    # YAML generation options
    parser.add_argument(
        '--section-only',
        action='store_true',
        help='Generate only points section (for embedding in existing config)'
    )
    
    parser.add_argument(
        '--no-comments',
        action='store_true',
        help='Generate YAML without comments'
    )
    
    parser.add_argument(
        '--precision',
        type=int,
        default=3,
        metavar='N',
        help='Decimal precision for coordinates (default: 3)'
    )
    
    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        metavar='N',
        help='YAML indentation spaces (default: 2)'
    )
    
    parser.add_argument(
        '--no-sort',
        action='store_true',
        help='Do not sort point names alphabetically'
    )
    
    # Validation and info options
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate input file, do not convert'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show conversion statistics'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Validate input file
        validate_input_file(args.input_file)
        
        # Determine output file
        if args.output:
            output_file = args.output
        else:
            input_path = Path(args.input_file)
            output_file = str(input_path.with_suffix('.yaml'))
        
        if args.verbose:
            print(f"Input file: {args.input_file}")
            print(f"Output file: {output_file}")
            print(f"Naming strategy: {args.naming_strategy}")
        
        # Validate output file path
        if not args.validate_only:
            validate_output_file(output_file)
        
        # Create converter with options
        naming_strategy = get_naming_strategy(args.naming_strategy)
        
        converter = KLEToErgogenConverter(
            key_unit_size=args.key_unit_size,
            naming_strategy=naming_strategy,
            center_on_origin=not args.no_center,
            invert_y_axis=not args.no_invert_y
        )
        
        # Validate input file
        if args.validate_only or args.verbose:
            print("Validating input file...")
            validation_errors = converter.validate_kle_file(args.input_file)
            
            if validation_errors:
                print("Validation errors:")
                for error in validation_errors:
                    print(f"  - {error}")
                if args.validate_only:
                    sys.exit(1)
                else:
                    print("Continuing despite validation errors...")
            else:
                print("Input file is valid.")
                
            if args.validate_only:
                sys.exit(0)
        
        # Convert KLE to points
        if args.verbose:
            print("Converting KLE to Ergogen points...")
        
        try:
            points_collection = converter.convert_file(args.input_file)
        except KLEToErgogenError as e:
            print(f"Conversion failed: {e}", file=sys.stderr)
            sys.exit(1)
        
        if args.verbose:
            print(f"Converted {len(points_collection.points)} points")
        
        # Show statistics if requested
        if args.stats or args.verbose:
            stats = converter.get_conversion_stats(points_collection)
            print("\nConversion Statistics:")
            print(f"  Total points: {stats['total_points']}")
            if stats['bounds']:
                bounds = stats['bounds']
                print(f"  Layout bounds: {bounds['width']:.1f}mm × {bounds['height']:.1f}mm")
            if stats['special_keys']['rotated'] > 0:
                print(f"  Rotated keys: {stats['special_keys']['rotated']}")
            if stats['special_keys']['wide_keys'] > 0:
                print(f"  Wide keys: {stats['special_keys']['wide_keys']}")
            if stats['special_keys']['tall_keys'] > 0:
                print(f"  Tall keys: {stats['special_keys']['tall_keys']}")
        
        # Generate YAML
        if args.verbose:
            print("Generating YAML output...")
        
        generator = ErgogenYAMLGenerator(
            indent=args.indent,
            sort_keys=not args.no_sort,
            include_comments=not args.no_comments,
            precision=args.precision
        )
        
        try:
            if args.section_only:
                yaml_content = generator.generate_yaml_section(points_collection)
            else:
                yaml_content = generator.generate_yaml(points_collection)
        except ErgogenYAMLGeneratorError as e:
            print(f"YAML generation failed: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Validate generated YAML
        validation_errors = generator.validate_yaml(yaml_content)
        if validation_errors:
            print("Warning: Generated YAML has validation issues:")
            for error in validation_errors:
                print(f"  - {error}")
        
        # Save output file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
        except IOError as e:
            print(f"Failed to write output file: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Success message
        if args.verbose or args.stats:
            yaml_stats = generator.get_generation_stats(points_collection)
            print(f"\nSuccessfully converted {yaml_stats['total_points']} points")
            print(f"Output written to: {output_file}")
            print(f"YAML size: {yaml_stats['full_yaml_size']} characters")
        else:
            print(f"Converted {len(points_collection.points)} points to {output_file}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
