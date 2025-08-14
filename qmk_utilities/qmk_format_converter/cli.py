#!/usr/bin/env python3
"""
QMK Format Converter CLI

Command-line interface for converting between KLE, VIA, and keymap.c formats.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

# Handle both standalone and module execution
try:
    from .qmk_converter import QMKFormatConverter, SupportedFormat
    from .batch_processor import BatchProcessor
except ImportError:
    # Running as standalone script
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from qmk_converter import QMKFormatConverter, SupportedFormat
    from batch_processor import BatchProcessor


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


def setup_logging(verbose: bool = False, log_file: Optional[str] = None):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    format_str = '%(asctime)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=handlers
    )


def progress_callback(current: int, total: int, filename: str):
    """Progress callback for batch operations."""
    percentage = (current / total) * 100
    print(f"\rProgress: {current}/{total} ({percentage:.1f}%) - {filename}",
          end='', flush=True)
    if current == total:
        print()  # New line when complete


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Convert between KLE, VIA, and keymap.c keyboard layout formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file conversion
  %(prog)s layout.json -o output.json --to via
  
  # Batch convert directory
  %(prog)s --batch-dir input_dir --output-dir output_dir --to via
  
  # Batch convert with file list
  %(prog)s --batch-files file1.json file2.c --output-dir output_dir --to kle
  
  # Validate files
  %(prog)s layout.json --validate
  %(prog)s --batch-validate input_dir
  
  # List supported formats
  %(prog)s --list-formats
        """
    )
    
    # Input/output options
    parser.add_argument('input', nargs='?', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--from', dest='input_format', 
                       help='Input format (kle, via, keymap, qmk_configurator)')
    parser.add_argument('--to', dest='output_format', 
                       help='Output format (kle, via, keymap, qmk_configurator)')
    
    # Batch processing options
    parser.add_argument('--batch-dir', help='Process all files in directory')
    parser.add_argument('--batch-files', nargs='+', 
                       help='Process specific list of files')
    parser.add_argument('--output-dir', help='Output directory for batch processing')
    parser.add_argument('--recursive', action='store_true',
                       help='Search directories recursively')
    parser.add_argument('--naming-pattern', default='{name}',
                       help='Output filename pattern (default: {name})')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing output files')
    
    # Validation options
    parser.add_argument('--validate', action='store_true', help='Validate input file')
    parser.add_argument('--batch-validate', help='Validate all files in directory')
    
    # Information commands
    parser.add_argument('--list-formats', action='store_true', 
                       help='List supported formats')
    parser.add_argument('--info', help='Get information about a specific format')
    
    # Logging and output options
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--log-file', help='Write logs to file')
    parser.add_argument('--quiet', action='store_true', 
                       help='Suppress progress output')
    parser.add_argument('--version', action='version', 
                       version='QMK Format Converter 1.0.0')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose, args.log_file)
    
    # Initialize converter and batch processor
    converter = QMKFormatConverter()
    batch_processor = BatchProcessor(converter)
    
    # Set up progress callback if not quiet
    if not args.quiet:
        batch_processor.set_progress_callback(progress_callback)
    
    # Handle list formats command
    if args.list_formats:
        print("Supported formats:")
        formats = converter.list_supported_formats()
        for fmt, desc in formats.items():
            print(f"  {fmt:<15} - {desc}")
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
    
    # Handle batch validation
    if args.batch_validate:
        try:
            input_format = None
            if args.input_format:
                input_format = format_from_string(args.input_format)
            
            results = batch_processor.validate_directory(
                args.batch_validate, input_format, args.recursive
            )
            
            print(f"Validation Results:")
            print(f"  Total files: {results['total_files']}")
            print(f"  Valid files: {len(results['valid_files'])}")
            print(f"  Invalid files: {len(results['invalid_files'])}")
            
            if results['invalid_files'] and args.verbose:
                print("\nInvalid files:")
                for file_path in results['invalid_files']:
                    errors = results['validation_errors'].get(file_path, [])
                    print(f"  {file_path}:")
                    for error in errors:
                        print(f"    - {error}")
            
            return 0 if len(results['invalid_files']) == 0 else 1
            
        except Exception as e:
            print(f"Error during batch validation: {e}", file=sys.stderr)
            return 1
    
    # Handle batch processing
    if args.batch_dir or args.batch_files:
        if not args.output_dir:
            parser.error("--output-dir is required for batch processing")
            return 1
        
        if not args.output_format:
            parser.error("--to (output format) is required for batch processing")
            return 1
        
        try:
            # Parse format arguments
            input_format = None
            if args.input_format:
                input_format = format_from_string(args.input_format)
            
            output_format = format_from_string(args.output_format)
            
            # Perform batch processing
            if args.batch_dir:
                result = batch_processor.process_directory(
                    args.batch_dir,
                    args.output_dir,
                    input_format,
                    output_format,
                    args.recursive,
                    args.naming_pattern,
                    args.overwrite
                )
            else:  # args.batch_files
                result = batch_processor.process_file_list(
                    args.batch_files,
                    args.output_dir,
                    input_format,
                    output_format,
                    args.naming_pattern,
                    args.overwrite
                )
            
            # Print results summary
            summary = result.summary()
            print(f"\nBatch Processing Results:")
            print(f"  Total files: {summary['total_files']}")
            print(f"  Successful: {summary['successful']}")
            print(f"  Failed: {summary['failed']}")
            print(f"  Skipped: {summary['skipped']}")
            print(f"  Success rate: {summary['success_rate']}")
            print(f"  Duration: {summary['duration']}")
            
            if result.failed_conversions and args.verbose:
                print("\nFailed conversions:")
                for file_path, error in result.failed_conversions:
                    print(f"  {file_path}: {error}")
            
            if result.skipped_files and args.verbose:
                print("\nSkipped files:")
                for file_path, reason in result.skipped_files:
                    print(f"  {file_path}: {reason}")
            
            return 0 if result.failure_count == 0 else 1
            
        except Exception as e:
            print(f"Error during batch processing: {e}", file=sys.stderr)
            return 1
    
    # Require input file for single file operations
    if not args.input:
        parser.error("Input file is required for single file operations")
        return 1
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found", file=sys.stderr)
        return 1
    
    # Handle single file validation
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
    
    # Handle single file conversion
    if not args.output:
        parser.error("Output file (-o/--output) is required for single file conversion")
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
        
        if not args.quiet:
            print("Conversion completed successfully")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
