#!/usr/bin/env python3
"""Debug script for KiCad parser."""

from pathlib import Path

schematic_path = Path("../pcb-library/design-files/lumberjack/kicad/lumberjack.kicad_sch")

with open(schematic_path, 'r') as f:
    content = f.read()

# Count symbol blocks
symbol_count = content.count('(symbol (lib_id')
print(f"Found {symbol_count} symbol blocks in file")

# Show first few lines of first symbol block
import re
first_symbol = re.search(r'\(symbol \(lib_id[^\)]+\).*?\n.*?\n.*?\n.*?\n', content, re.DOTALL)
if first_symbol:
    print("\nFirst symbol block (first 5 lines):")
    print(first_symbol.group(0))

# Try the extraction
from thkg.templates.kicad_parser import KiCadParser

parser = KiCadParser(schematic_path)
parser._load_file()
blocks = parser._extract_symbol_blocks()

print(f"\nExtracted {len(blocks)} blocks")

if blocks:
    print("\nFirst block:")
    print(blocks[0][:500])
