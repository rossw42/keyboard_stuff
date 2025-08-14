"""
Batch Processing System for QMK Format Converter

Handles batch conversion of multiple files with progress reporting
and detailed success/failure tracking.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
import time

# Handle both standalone and module execution
try:
    from .qmk_converter import QMKFormatConverter, SupportedFormat
except ImportError:
    # Running as standalone script
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from qmk_converter import QMKFormatConverter, SupportedFormat


@dataclass
class BatchResult:
    """Results from a batch processing operation."""
    successful_conversions: List[Path] = field(default_factory=list)
    failed_conversions: List[Tuple[Path, Exception]] = field(default_factory=list)
    skipped_files: List[Tuple[Path, str]] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    total_files: int = 0
    
    @property
    def success_count(self) -> int:
        """Number of successful conversions."""
        return len(self.successful_conversions)
    
    @property
    def failure_count(self) -> int:
        """Number of failed conversions."""
        return len(self.failed_conversions)
    
    @property
    def skipped_count(self) -> int:
        """Number of skipped files."""
        return len(self.skipped_files)
    
    @property
    def duration(self) -> float:
        """Duration of batch operation in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    @property
    def success_rate(self) -> float:
        """Success rate as percentage."""
        if self.total_files == 0:
            return 0.0
        return (self.success_count / self.total_files) * 100
    
    def summary(self) -> Dict[str, Any]:
        """Generate summary dictionary."""
        return {
            "total_files": self.total_files,
            "successful": self.success_count,
            "failed": self.failure_count,
            "skipped": self.skipped_count,
            "success_rate": f"{self.success_rate:.1f}%",
            "duration": f"{self.duration:.2f}s",
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None
        }


class BatchProcessor:
    """
    Batch processor for converting multiple keyboard layout files.
    
    Provides directory-based and file list-based batch processing
    with progress reporting and detailed error tracking.
    """
    
    def __init__(self, converter: Optional[QMKFormatConverter] = None):
        """
        Initialize batch processor.
        
        Args:
            converter: QMKFormatConverter instance (creates new if None)
        """
        self.converter = converter or QMKFormatConverter()
        self.progress_callback: Optional[Callable[[int, int, str], None]] = None
        self.logger = logging.getLogger(__name__)
        
    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        Set callback function for progress reporting.
        
        Args:
            callback: Function called with (current, total, filename)
        """
        self.progress_callback = callback
    
    def _report_progress(self, current: int, total: int, filename: str):
        """Report progress if callback is set."""
        if self.progress_callback:
            self.progress_callback(current, total, filename)
    
    def _get_output_filename(self, input_path: Path, output_dir: Path,
                           output_format: SupportedFormat,
                           naming_pattern: str = "{name}") -> Path:
        """
        Generate output filename based on input and format.
        
        Args:
            input_path: Input file path
            output_dir: Output directory
            output_format: Target format
            naming_pattern: Naming pattern with {name} placeholder
            
        Returns:
            Output file path
        """
        # Get appropriate extension for format
        extensions = {
            SupportedFormat.KLE: ".json",
            SupportedFormat.VIA: ".json", 
            SupportedFormat.KEYMAP: ".c",
            SupportedFormat.QMK_CONFIGURATOR: ".json"
        }
        
        base_name = input_path.stem
        formatted_name = naming_pattern.format(name=base_name)
        extension = extensions[output_format]
        
        return output_dir / f"{formatted_name}{extension}"
    
    def _find_input_files(self, input_dir: Path,
                         input_format: Optional[SupportedFormat] = None,
                         recursive: bool = False) -> List[Path]:
        """
        Find input files in directory based on format.
        
        Args:
            input_dir: Directory to search
            input_format: Format to look for (auto-detect if None)
            recursive: Whether to search recursively
            
        Returns:
            List of input file paths
        """
        if not input_dir.is_dir():
            return []
        
        # Define file patterns based on format
        patterns = []
        if input_format == SupportedFormat.KEYMAP:
            patterns = ["*.c"]
        elif input_format in [SupportedFormat.KLE, SupportedFormat.VIA,
                             SupportedFormat.QMK_CONFIGURATOR]:
            patterns = ["*.json"]
        else:
            # Auto-detect: look for common extensions
            patterns = ["*.json", "*.c", "*.kle"]
        
        files = []
        search_method = input_dir.rglob if recursive else input_dir.glob
        
        for pattern in patterns:
            files.extend(search_method(pattern))
        
        # Filter out files that don't match the format if specified
        if input_format:
            filtered_files = []
            for file_path in files:
                try:
                    detected = self.converter.detect_format(file_path)
                    if detected == input_format:
                        filtered_files.append(file_path)
                except Exception:
                    # Skip files that can't be processed
                    continue
            files = filtered_files
        
        return sorted(files)
    
    def process_directory(self, input_dir: Union[str, Path],
                         output_dir: Union[str, Path],
                         input_format: Optional[SupportedFormat] = None,
                         output_format: Optional[SupportedFormat] = None,
                         recursive: bool = False,
                         naming_pattern: str = "{name}",
                         overwrite: bool = False) -> BatchResult:
        """
        Process all compatible files in a directory.
        
        Args:
            input_dir: Directory containing input files
            output_dir: Directory for output files
            input_format: Input format (auto-detect if None)
            output_format: Output format (required)
            recursive: Search subdirectories recursively
            naming_pattern: Output filename pattern
            overwrite: Overwrite existing output files
            
        Returns:
            BatchResult with processing results
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        if not output_format:
            raise ValueError("Output format must be specified")
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find input files
        input_files = self._find_input_files(input_dir, input_format, recursive)
        
        return self.process_file_list(input_files, output_dir, input_format,
                                    output_format, naming_pattern, overwrite)
    
    def process_file_list(self, file_list: List[Union[str, Path]],
                         output_dir: Union[str, Path],
                         input_format: Optional[SupportedFormat] = None,
                         output_format: Optional[SupportedFormat] = None,
                         naming_pattern: str = "{name}",
                         overwrite: bool = False) -> BatchResult:
        """
        Process a list of files.
        
        Args:
            file_list: List of input file paths
            output_dir: Directory for output files
            input_format: Input format (auto-detect if None)
            output_format: Output format (required)
            naming_pattern: Output filename pattern
            overwrite: Overwrite existing output files
            
        Returns:
            BatchResult with processing results
        """
        output_dir = Path(output_dir)
        
        if not output_format:
            raise ValueError("Output format must be specified")
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize result tracking
        result = BatchResult()
        result.total_files = len(file_list)
        result.start_time = datetime.now()
        
        self.logger.info(f"Starting batch processing of {len(file_list)} files")
        
        for i, file_path in enumerate(file_list, 1):
            file_path = Path(file_path)
            
            try:
                self._report_progress(i, len(file_list), file_path.name)
                
                # Check if input file exists
                if not file_path.exists():
                    result.skipped_files.append((file_path, "File not found"))
                    continue
                
                # Generate output path
                output_path = self._get_output_filename(
                    file_path, output_dir, output_format, naming_pattern
                )
                
                # Check if output already exists
                if output_path.exists() and not overwrite:
                    result.skipped_files.append(
                        (file_path, f"Output exists: {output_path}")
                    )
                    continue
                
                # Perform conversion
                self.converter.convert_file(
                    file_path, input_format, output_path, output_format
                )
                
                result.successful_conversions.append(file_path)
                self.logger.info(f"Converted: {file_path} -> {output_path}")
                
            except Exception as e:
                result.failed_conversions.append((file_path, e))
                self.logger.error(f"Failed to convert {file_path}: {e}")
        
        result.end_time = datetime.now()
        
        self.logger.info(
            f"Batch processing completed: {result.success_count}/"
            f"{result.total_files} successful ({result.success_rate:.1f}%)"
        )
        
        return result
    
    def validate_directory(self, input_dir: Union[str, Path],
                          input_format: Optional[SupportedFormat] = None,
                          recursive: bool = False) -> Dict[str, Any]:
        """
        Validate all files in a directory.
        
        Args:
            input_dir: Directory containing files to validate
            input_format: Format to validate (auto-detect if None)
            recursive: Search subdirectories recursively
            
        Returns:
            Dictionary with validation results
        """
        input_dir = Path(input_dir)
        
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        # Find input files
        input_files = self._find_input_files(input_dir, input_format, recursive)
        
        results = {
            "total_files": len(input_files),
            "valid_files": [],
            "invalid_files": [],
            "validation_errors": {}
        }
        
        for i, file_path in enumerate(input_files, 1):
            self._report_progress(i, len(input_files), file_path.name)
            
            try:
                validation_result = self.converter.validate_file(
                    file_path, input_format
                )
                
                if validation_result["valid"]:
                    results["valid_files"].append(str(file_path))
                else:
                    results["invalid_files"].append(str(file_path))
                    results["validation_errors"][str(file_path)] = \
                        validation_result["errors"]
                        
            except Exception as e:
                results["invalid_files"].append(str(file_path))
                results["validation_errors"][str(file_path)] = [str(e)]
        
        return results