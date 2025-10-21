#!/usr/bin/env python3
"""
BOM Parser for Multiple Formats
Parses CSV, Markdown table, and plain text BOM files
"""

import csv
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from enum import Enum


class BOMFormat(Enum):
    """Supported BOM file formats"""
    CSV = "csv"
    MARKDOWN = "markdown"
    PLAIN_TEXT = "plain_text"
    UNKNOWN = "unknown"


class BOMComponent:
    """Represents a single component from a BOM"""
    
    def __init__(self, data: Dict[str, str]):
        self.raw_data = data
        # Common field mappings
        self.component = data.get('component', data.get('Component', data.get('Part', '')))
        self.value = data.get('value', data.get('Value', data.get('Val', '')))
        self.footprint = data.get('footprint', data.get('Footprint', data.get('Package', '')))
        self.quantity = self._parse_quantity(data.get('quantity', data.get('Quantity', data.get('Qty', '1'))))
        self.reference = data.get('reference', data.get('Reference', data.get('Ref', '')))
        self.vendor_part = data.get('vendor_part', data.get('Vendor Part', data.get('Part Number', '')))
        self.notes = data.get('notes', data.get('Notes', data.get('Description', '')))
    
    def _parse_quantity(self, qty_str: str) -> int:
        """Parse quantity from string, handling various formats"""
        if not qty_str:
            return 1
        # Extract first number from string
        match = re.search(r'\d+', str(qty_str))
        return int(match.group()) if match else 1
    
    def to_dict(self) -> Dict[str, str]:
        """Convert component to dictionary"""
        return {
            'component': self.component,
            'value': self.value,
            'footprint': self.footprint,
            'quantity': str(self.quantity),
            'reference': self.reference,
            'vendor_part': self.vendor_part,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f"BOMComponent({self.component}, {self.value}, qty={self.quantity})"


class BOMParser:
    """Parser for BOM files in multiple formats"""
    
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.format = self._detect_format()
        self.components: List[BOMComponent] = []
    
    def _detect_format(self) -> BOMFormat:
        """Auto-detect BOM file format"""
        if not self.file_path.exists():
            return BOMFormat.UNKNOWN
        
        # Check file extension first
        ext = self.file_path.suffix.lower()
        if ext == '.csv':
            return BOMFormat.CSV
        elif ext in ['.md', '.markdown']:
            return BOMFormat.MARKDOWN
        
        # Read first few lines to detect format
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                first_lines = [f.readline() for _ in range(5)]
                content = ''.join(first_lines)
                
                # Check for markdown table
                if '|' in content and ('---' in content or ':-' in content):
                    return BOMFormat.MARKDOWN
                
                # Check for CSV (commas in multiple lines)
                comma_count = sum(1 for line in first_lines if ',' in line)
                if comma_count >= 2:
                    return BOMFormat.CSV
                
                # Default to plain text
                return BOMFormat.PLAIN_TEXT
        except Exception:
            return BOMFormat.UNKNOWN
    
    def parse(self) -> List[BOMComponent]:
        """Parse BOM file based on detected format"""
        if self.format == BOMFormat.CSV:
            self.components = self._parse_csv()
        elif self.format == BOMFormat.MARKDOWN:
            self.components = self._parse_markdown()
        elif self.format == BOMFormat.PLAIN_TEXT:
            self.components = self._parse_plain_text()
        else:
            raise ValueError(f"Unknown or unsupported format for {self.file_path}")
        
        return self.components
    
    def _parse_csv(self) -> List[BOMComponent]:
        """Parse CSV format BOM"""
        components = []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                # Try to detect delimiter
                sample = f.read(1024)
                f.seek(0)
                
                sniffer = csv.Sniffer()
                try:
                    dialect = sniffer.sniff(sample)
                    delimiter = dialect.delimiter
                except:
                    delimiter = ','
                
                reader = csv.DictReader(f, delimiter=delimiter)
                
                for row in reader:
                    # Skip empty rows
                    if not any(row.values()):
                        continue
                    
                    # Normalize keys (lowercase, strip spaces)
                    normalized_row = {k.strip().lower(): v.strip() for k, v in row.items() if k}
                    
                    component = BOMComponent(normalized_row)
                    if component.component or component.value:
                        components.append(component)
        
        except Exception as e:
            print(f"Error parsing CSV {self.file_path}: {e}", file=sys.stderr)
        
        return components
    
    def _parse_markdown(self) -> List[BOMComponent]:
        """Parse Markdown table format BOM"""
        components = []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find table headers
            header_line = None
            header_idx = -1
            
            for idx, line in enumerate(lines):
                if '|' in line and idx + 1 < len(lines) and ('---' in lines[idx + 1] or ':-' in lines[idx + 1]):
                    header_line = line
                    header_idx = idx
                    break
            
            if header_line is None:
                return components
            
            # Parse headers
            headers = [h.strip().lower() for h in header_line.split('|') if h.strip()]
            
            # Parse data rows (skip separator line)
            for line in lines[header_idx + 2:]:
                if '|' not in line:
                    continue
                
                cells = [c.strip() for c in line.split('|') if c.strip() or line.startswith('|')]
                
                # Handle leading/trailing pipes
                if line.strip().startswith('|'):
                    cells = cells[1:] if len(cells) > len(headers) else cells
                if line.strip().endswith('|'):
                    cells = cells[:-1] if len(cells) > len(headers) else cells
                
                if len(cells) < len(headers):
                    continue
                
                # Create row dictionary
                row = {headers[i]: cells[i] for i in range(min(len(headers), len(cells)))}
                
                component = BOMComponent(row)
                if component.component or component.value:
                    components.append(component)
        
        except Exception as e:
            print(f"Error parsing Markdown {self.file_path}: {e}", file=sys.stderr)
        
        return components
    
    def _parse_plain_text(self) -> List[BOMComponent]:
        """Parse plain text format BOM"""
        components = []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Look for common patterns in plain text BOMs
            # Pattern: "Quantity Component Value [Footprint] [Notes]"
            # Example: "68x 1N4148 Diode DO-35"
            # Example: "1 ATmega328P DIP-28"
            
            for line in lines:
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#') or line.startswith('//'):
                    continue
                
                # Try to parse quantity at start
                qty_match = re.match(r'^(\d+)x?\s+(.+)$', line, re.IGNORECASE)
                if qty_match:
                    quantity = qty_match.group(1)
                    rest = qty_match.group(2).strip()
                else:
                    quantity = '1'
                    rest = line
                
                # Split remaining parts
                parts = rest.split()
                if len(parts) < 2:
                    continue
                
                # Heuristic: first part is component, second is value
                component_data = {
                    'quantity': quantity,
                    'component': parts[0],
                    'value': parts[1] if len(parts) > 1 else '',
                    'footprint': parts[2] if len(parts) > 2 else '',
                    'notes': ' '.join(parts[3:]) if len(parts) > 3 else ''
                }
                
                component = BOMComponent(component_data)
                components.append(component)
        
        except Exception as e:
            print(f"Error parsing plain text {self.file_path}: {e}", file=sys.stderr)
        
        return components


def main():
    """Command-line interface for BOM parser"""
    if len(sys.argv) < 2:
        print("Usage: parse_bom.py <bom-file>")
        print("Parses BOM files in CSV, Markdown, or plain text format")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    parser = BOMParser(file_path)
    print(f"Detected format: {parser.format.value}")
    
    components = parser.parse()
    print(f"\nParsed {len(components)} components:\n")
    
    for comp in components:
        print(f"  {comp.quantity}x {comp.component} {comp.value} ({comp.footprint})")


if __name__ == '__main__':
    main()
