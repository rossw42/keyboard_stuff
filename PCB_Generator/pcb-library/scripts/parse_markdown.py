#!/usr/bin/env python3
"""
Markdown Parser for Documentation Indexing
Extracts headings, links, tables, code blocks, and metadata from Markdown files
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass
class MarkdownHeading:
    """Represents a heading in a Markdown document"""
    level: int
    text: str
    line_number: int
    anchor: str = ""
    
    def __post_init__(self):
        # Generate anchor from text (GitHub-style)
        self.anchor = self._generate_anchor(self.text)
    
    @staticmethod
    def _generate_anchor(text: str) -> str:
        """Generate GitHub-style anchor from heading text"""
        # Convert to lowercase, replace spaces with hyphens
        anchor = text.lower().strip()
        # Remove special characters except hyphens and underscores
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'[\s]+', '-', anchor)
        return anchor


@dataclass
class MarkdownLink:
    """Represents a link in a Markdown document"""
    text: str
    url: str
    line_number: int
    is_internal: bool = False
    is_valid: bool = True
    
    def __post_init__(self):
        self.is_internal = self._check_internal()
    
    def _check_internal(self) -> bool:
        """Check if link is internal (relative path or anchor)"""
        if self.url.startswith('#'):
            return True
        if self.url.startswith('http://') or self.url.startswith('https://'):
            return False
        # Relative paths are internal
        return not self.url.startswith('/')


@dataclass
class MarkdownTable:
    """Represents a table in a Markdown document"""
    headers: List[str]
    rows: List[List[str]]
    line_number: int
    
    def row_count(self) -> int:
        return len(self.rows)
    
    def column_count(self) -> int:
        return len(self.headers)


@dataclass
class MarkdownCodeBlock:
    """Represents a code block in a Markdown document"""
    language: str
    content: str
    line_number: int
    line_count: int


@dataclass
class MarkdownMetadata:
    """Metadata extracted from a Markdown document"""
    file_path: Path
    title: str = ""
    headings: List[MarkdownHeading] = field(default_factory=list)
    links: List[MarkdownLink] = field(default_factory=list)
    tables: List[MarkdownTable] = field(default_factory=list)
    code_blocks: List[MarkdownCodeBlock] = field(default_factory=list)
    line_count: int = 0
    word_count: int = 0
    
    def get_toc(self) -> List[str]:
        """Generate table of contents from headings"""
        toc = []
        for heading in self.headings:
            indent = "  " * (heading.level - 1)
            toc.append(f"{indent}- [{heading.text}](#{heading.anchor})")
        return toc
    
    def get_internal_links(self) -> List[MarkdownLink]:
        """Get all internal links"""
        return [link for link in self.links if link.is_internal]
    
    def get_external_links(self) -> List[MarkdownLink]:
        """Get all external links"""
        return [link for link in self.links if not link.is_internal]
    
    def to_dict(self) -> Dict:
        """Convert metadata to dictionary"""
        return {
            'file_path': str(self.file_path),
            'title': self.title,
            'heading_count': len(self.headings),
            'link_count': len(self.links),
            'internal_link_count': len(self.get_internal_links()),
            'external_link_count': len(self.get_external_links()),
            'table_count': len(self.tables),
            'code_block_count': len(self.code_blocks),
            'line_count': self.line_count,
            'word_count': self.word_count
        }


class MarkdownParser:
    """Parser for Markdown documents"""
    
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.metadata = MarkdownMetadata(file_path=self.file_path)
        self.lines: List[str] = []
    
    def parse(self) -> MarkdownMetadata:
        """Parse the Markdown file and extract all metadata"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        # Read file
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
        
        self.metadata.line_count = len(self.lines)
        
        # Extract components
        self._extract_headings()
        self._extract_links()
        self._extract_tables()
        self._extract_code_blocks()
        self._calculate_word_count()
        
        # Set title (first heading or filename)
        if self.metadata.headings:
            self.metadata.title = self.metadata.headings[0].text
        else:
            self.metadata.title = self.file_path.stem
        
        return self.metadata
    
    def _extract_headings(self):
        """Extract all headings from the document"""
        for line_num, line in enumerate(self.lines, start=1):
            line = line.strip()
            
            # ATX-style headings (# Heading)
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                
                heading = MarkdownHeading(
                    level=level,
                    text=text,
                    line_number=line_num
                )
                self.metadata.headings.append(heading)
    
    def _extract_links(self):
        """Extract all links from the document"""
        for line_num, line in enumerate(self.lines, start=1):
            # Inline links: [text](url)
            inline_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            for match in re.finditer(inline_pattern, line):
                text = match.group(1)
                url = match.group(2)
                
                link = MarkdownLink(
                    text=text,
                    url=url,
                    line_number=line_num
                )
                self.metadata.links.append(link)
            
            # Reference-style links: [text][ref]
            # Note: This doesn't resolve the reference, just captures the link text
            ref_pattern = r'\[([^\]]+)\]\[([^\]]+)\]'
            for match in re.finditer(ref_pattern, line):
                text = match.group(1)
                ref = match.group(2)
                
                # Try to find the reference definition
                ref_url = self._find_reference_url(ref)
                if ref_url:
                    link = MarkdownLink(
                        text=text,
                        url=ref_url,
                        line_number=line_num
                    )
                    self.metadata.links.append(link)
    
    def _find_reference_url(self, ref: str) -> Optional[str]:
        """Find URL for a reference-style link"""
        ref_pattern = re.compile(rf'^\[{re.escape(ref)}\]:\s*(.+)$', re.IGNORECASE)
        
        for line in self.lines:
            match = ref_pattern.match(line.strip())
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_tables(self):
        """Extract all tables from the document"""
        i = 0
        while i < len(self.lines):
            line = self.lines[i].strip()
            
            # Check if this line looks like a table header
            if '|' in line and i + 1 < len(self.lines):
                next_line = self.lines[i + 1].strip()
                
                # Check if next line is a separator (contains | and -)
                if '|' in next_line and '-' in next_line:
                    # Parse table
                    table = self._parse_table(i)
                    if table:
                        self.metadata.tables.append(table)
                        # Skip past the table
                        i += 2 + len(table.rows)
                        continue
            
            i += 1
    
    def _parse_table(self, start_line: int) -> Optional[MarkdownTable]:
        """Parse a table starting at the given line"""
        if start_line >= len(self.lines):
            return None
        
        # Parse header
        header_line = self.lines[start_line].strip()
        headers = [h.strip() for h in header_line.split('|') if h.strip()]
        
        # Skip separator line
        if start_line + 1 >= len(self.lines):
            return None
        
        # Parse rows
        rows = []
        i = start_line + 2
        
        while i < len(self.lines):
            line = self.lines[i].strip()
            
            # Stop if not a table row
            if not line or '|' not in line:
                break
            
            # Parse row
            cells = [c.strip() for c in line.split('|') if c.strip() or line.startswith('|')]
            
            # Handle leading/trailing pipes
            if line.startswith('|') and len(cells) > len(headers):
                cells = cells[1:]
            if line.endswith('|') and len(cells) > len(headers):
                cells = cells[:-1]
            
            if cells:
                rows.append(cells)
            
            i += 1
        
        if not rows:
            return None
        
        return MarkdownTable(
            headers=headers,
            rows=rows,
            line_number=start_line + 1
        )
    
    def _extract_code_blocks(self):
        """Extract all code blocks from the document"""
        i = 0
        while i < len(self.lines):
            line = self.lines[i].strip()
            
            # Fenced code block (```)
            if line.startswith('```'):
                language = line[3:].strip()
                start_line = i + 1
                content_lines = []
                
                i += 1
                while i < len(self.lines):
                    if self.lines[i].strip().startswith('```'):
                        # End of code block
                        code_block = MarkdownCodeBlock(
                            language=language,
                            content='\n'.join(content_lines),
                            line_number=start_line,
                            line_count=len(content_lines)
                        )
                        self.metadata.code_blocks.append(code_block)
                        break
                    
                    content_lines.append(self.lines[i].rstrip())
                    i += 1
            
            i += 1
    
    def _calculate_word_count(self):
        """Calculate word count (excluding code blocks and tables)"""
        word_count = 0
        
        # Get line numbers to exclude (code blocks and tables)
        exclude_lines = set()
        
        for code_block in self.metadata.code_blocks:
            for i in range(code_block.line_number, code_block.line_number + code_block.line_count):
                exclude_lines.add(i)
        
        for table in self.metadata.tables:
            for i in range(table.line_number, table.line_number + table.row_count() + 2):
                exclude_lines.add(i)
        
        # Count words in non-excluded lines
        for line_num, line in enumerate(self.lines, start=1):
            if line_num not in exclude_lines:
                # Remove markdown formatting
                text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)  # Links
                text = re.sub(r'[*_`#]', '', text)  # Formatting
                
                words = text.split()
                word_count += len(words)
        
        self.metadata.word_count = word_count
    
    def validate_links(self, base_path: Path = None) -> List[Tuple[MarkdownLink, str]]:
        """Validate all links in the document"""
        if base_path is None:
            base_path = self.file_path.parent
        
        broken_links = []
        
        for link in self.metadata.links:
            if link.is_internal and not link.url.startswith('#'):
                # Check if file exists
                link_path = base_path / link.url
                if not link_path.exists():
                    link.is_valid = False
                    broken_links.append((link, f"File not found: {link_path}"))
            
            # Note: External link validation would require network requests
            # and is not implemented here to avoid dependencies
        
        return broken_links


def main():
    """Command-line interface for Markdown parser"""
    if len(sys.argv) < 2:
        print("Usage: parse_markdown.py <markdown-file> [--validate]")
        print("\nParses Markdown files and extracts structure and metadata")
        print("\nOptions:")
        print("  --validate    Validate internal links")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    validate = '--validate' in sys.argv
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    # Parse file
    parser = MarkdownParser(file_path)
    metadata = parser.parse()
    
    # Display results
    print(f"Parsed: {file_path}")
    print(f"Title: {metadata.title}")
    print(f"\nStatistics:")
    print(f"  Lines: {metadata.line_count}")
    print(f"  Words: {metadata.word_count}")
    print(f"  Headings: {len(metadata.headings)}")
    print(f"  Links: {len(metadata.links)} ({len(metadata.get_internal_links())} internal, {len(metadata.get_external_links())} external)")
    print(f"  Tables: {len(metadata.tables)}")
    print(f"  Code blocks: {len(metadata.code_blocks)}")
    
    # Display headings
    if metadata.headings:
        print(f"\nHeadings:")
        for heading in metadata.headings:
            indent = "  " * (heading.level - 1)
            print(f"  {indent}{'#' * heading.level} {heading.text}")
    
    # Display links
    if metadata.links:
        print(f"\nLinks:")
        for link in metadata.links[:10]:  # Show first 10
            link_type = "internal" if link.is_internal else "external"
            print(f"  [{link.text}]({link.url}) - {link_type}")
        
        if len(metadata.links) > 10:
            print(f"  ... and {len(metadata.links) - 10} more")
    
    # Validate links if requested
    if validate:
        print(f"\nValidating links...")
        broken_links = parser.validate_links()
        
        if broken_links:
            print(f"\nBroken links found ({len(broken_links)}):")
            for link, error in broken_links:
                print(f"  Line {link.line_number}: {link.url} - {error}")
        else:
            print("  All internal links are valid!")


if __name__ == '__main__':
    main()
