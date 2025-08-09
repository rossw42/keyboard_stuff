#!/usr/bin/env python3
"""
QMK Format Converter CLI

Command-line interface for converting between KLE, VIA, and keymap.c formats.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Handle both standalone and module execution
try:
    from .qmk_converter import QMKFormatConverter, SupportedFormat
except ImportError:
    # Running as standalone script
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from qmk_converter import QMKFormatConverter, SupportedFormat


def format_from_string(format_str: str) -> SupportedFormat:
    """Convert string to SupportedFormat enum."""
    format_map = {
        'kle': SupportedFormat.KLE,
        'via': SupportedFormat.VIA,
        'keymap': SupportedFormat.KEYMAP,
        'keymap.c': SupportedFormat.KEYMAP,
        'c': SupportedFormat.KEYMAP,
        'qmk_configurator': SupportedFormat.QMK_CONFIGURATOR,
        'qmk-configurator': SupportedFormat.QMK_CONFIGURATOR,
        'configurator': SupportedFormat.QMK_CONFIGURATOR
    }
    
    format_str = format_str.lower()
    if format_str not in format_map:
        raise ValueError(f"Unsupported format: {format_str}")
    
    return format_map[format_str]


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Convert between KLE, VIA, and keymap.c keyboard layout formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert KLE to VIA (auto-detect input format)
  %(prog)s layout.json -o output.json --to via
  
  # Convert keymap.c to KLE with explicit formats
  %(prog)s keymap.c --from keymap --to kle -o layout.json
  
  # Validate a layout file
  %(prog)s layout.json --validate
  
  # List supported formats
  %(prog)s --list-formats
        """
    )
    
    # Input/output options
    parser.add_argument('input', nargs='?', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--from', dest='input_format', help='Input format (kle, via, keymap)')
    parser.add_argument('--to', dest='output_format', help='Output format (kle, via, keymap)')
    
    # Actions
    parser.add_argument('--validate', action='store_true', help='Validate input file')
    parser.add_argument('--list-formats', action='store_true', help='List supported formats')
    parser.add_argument('--info', help='Get information about a specific format')
    
    # Options
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version='QMK Format Converter 1.0.0')
    
    args = parser.parse_args()
    
    # Initialize converter
    converter = QMKFormatConverter()
    
    # Handle list formats command
    if args.list_formats:
        print("Supported formats:")
        formats = converter.list_supported_formats()
        for fmt, desc in formats.items():
            print(f"  {fmt:<8} - {desc}")
        return 0
    
    # Handle format info command
    if args.info:
        try:
            format_type = format_from_string(args.info)
            info = converter.get_format_info(format_type)
            print(f"Format: {info['name']}")
            print(f"Extension: {info['extension']}")
            print(f"Description: {info['description']}")
            print(f"Features: {', '.join(info['features'])}")
            print(f"Documentation: {info['url']}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        return 0
    
    # Require input file for other operations
    if not args.input:
        parser.error("Input file is required")
        return 1
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found", file=sys.stderr)
        return 1
    
    # Handle validation
    if args.validate:
        try:
            input_format = None
            if args.input_format:
                input_format = format_from_string(args.input_format)
            
            result = converter.validate_file(input_path, input_format)
            
            print(f"File: {input_path}")
            print(f"Format: {result['format']}")
            print(f"Valid: {'✓' if result['valid'] else '✗'}")
            
            if result['errors']:
                print("\nValidation errors:")
                for error in result['errors']:
                    print(f"  - {error}")
            
            if result['summary']:
                summary = result['summary']
                print(f"\nSummary:")
                print(f"  Name: {summary.get('name', 'N/A')}")
                print(f"  Keys: {summary.get('key_count', 0)}")
                print(f"  Layers: {summary.get('layer_count', 0)}")
                print(f"  Matrix: {summary.get('matrix_size', 'N/A')}")
                
            return 0 if result['valid'] else 1
            
        except Exception as e:
            print(f"Error validating file: {e}", file=sys.stderr)
            return 1
    
    # Handle conversion
    if not args.output:
        parser.error("Output file (-o/--output) is required for conversion")
        return 1
    
    if not args.output_format:
        parser.error("Output format (--to) is required for conversion")
        return 1
    
    try:
        # Parse format arguments
        input_format = None
        if args.input_format:
            input_format = format_from_string(args.input_format)
        
        output_format = format_from_string(args.output_format)
        output_path = Path(args.output)
        
        # Perform conversion
        if args.verbose:
            print(f"Converting {input_path} to {output_path}")
            print(f"Input format: {input_format.value if input_format else 'auto-detect'}")
            print(f"Output format: {output_format.value}")
        
        converter.convert_file(input_path, input_format, output_path, output_format)
        
        if args.verbose:
            print("Conversion completed successfully")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
