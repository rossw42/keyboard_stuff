#!/usr/bin/env python3
"""
Documentation Indexer
Generates master indexes for build guides and technical specifications
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from collections import defaultdict

# Import our markdown parser
from parse_markdown import MarkdownParser, MarkdownMetadata


@dataclass
class DocumentEntry:
    """Represents a document in the index"""
    file_path: Path
    title: str
    description: str = ""
    category: str = ""
    project: str = ""
    metadata: Optional[MarkdownMetadata] = None
    
    def get_relative_path(self, base_path: Path) -> Path:
        """Get path relative to base directory"""
        try:
            return self.file_path.relative_to(base_path)
        except ValueError:
            return self.file_path
    
    def to_markdown_entry(self, base_path: Path) -> str:
        """Convert to markdown list entry"""
        rel_path = self.get_relative_path(base_path)
        entry = f"- [{self.title}]({rel_path})"
        
        if self.description:
            entry += f" - {self.description}"
        
        if self.project:
            entry += f" (Project: {self.project})"
        
        return entry


@dataclass
class DocumentIndex:
    """Master index of documentation"""
    base_path: Path
    documents: List[DocumentEntry] = field(default_factory=list)
    categories: Dict[str, List[DocumentEntry]] = field(default_factory=lambda: defaultdict(list))
    projects: Dict[str, List[DocumentEntry]] = field(default_factory=lambda: defaultdict(list))
    
    def add_document(self, entry: DocumentEntry):
        """Add a document to the index"""
        self.documents.append(entry)
        
        if entry.category:
            self.categories[entry.category].append(entry)
        
        if entry.project:
            self.projects[entry.project].append(entry)
    
    def sort_documents(self):
        """Sort all documents alphabetically"""
        self.documents.sort(key=lambda d: d.title.lower())
        
        for category in self.categories.values():
            category.sort(key=lambda d: d.title.lower())
        
        for project in self.projects.values():
            project.sort(key=lambda d: d.title.lower())
    
    def generate_master_index(self, output_path: Path):
        """Generate master documentation index"""
        self.sort_documents()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Documentation Index\n\n")
            f.write("Master index of all documentation in the Through-Hole Keyboard PCB Design Resource Library.\n\n")
            
            # Statistics
            f.write("## Statistics\n\n")
            f.write(f"- **Total Documents:** {len(self.documents)}\n")
            f.write(f"- **Categories:** {len(self.categories)}\n")
            f.write(f"- **Projects:** {len(self.projects)}\n\n")
            
            # Table of contents
            f.write("## Table of Contents\n\n")
            f.write("- [By Category](#by-category)\n")
            f.write("- [By Project](#by-project)\n")
            f.write("- [All Documents (Alphabetical)](#all-documents-alphabetical)\n\n")
            
            # By category
            f.write("## By Category\n\n")
            
            for category in sorted(self.categories.keys()):
                docs = self.categories[category]
                f.write(f"### {category} ({len(docs)} documents)\n\n")
                
                for doc in docs:
                    f.write(doc.to_markdown_entry(self.base_path) + "\n")
                
                f.write("\n")
            
            # By project
            if self.projects:
                f.write("## By Project\n\n")
                
                for project in sorted(self.projects.keys()):
                    docs = self.projects[project]
                    f.write(f"### {project} ({len(docs)} documents)\n\n")
                    
                    for doc in docs:
                        f.write(doc.to_markdown_entry(self.base_path) + "\n")
                    
                    f.write("\n")
            
            # All documents alphabetically
            f.write("## All Documents (Alphabetical)\n\n")
            
            for doc in self.documents:
                f.write(doc.to_markdown_entry(self.base_path) + "\n")
        
        print(f"Generated master index: {output_path}")
    
    def generate_category_index(self, category: str, output_path: Path):
        """Generate index for a specific category"""
        if category not in self.categories:
            print(f"Warning: Category '{category}' not found", file=sys.stderr)
            return
        
        docs = self.categories[category]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {category}\n\n")
            f.write(f"Index of {category.lower()} in the library.\n\n")
            f.write(f"**Total Documents:** {len(docs)}\n\n")
            
            for doc in docs:
                f.write(doc.to_markdown_entry(self.base_path) + "\n")
                
                # Add metadata if available
                if doc.metadata:
                    f.write(f"  - {doc.metadata.line_count} lines, {doc.metadata.word_count} words\n")
                    if doc.metadata.headings:
                        f.write(f"  - {len(doc.metadata.headings)} sections\n")
        
        print(f"Generated {category} index: {output_path}")


class DocumentationIndexer:
    """Indexes all documentation in the library"""
    
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.index = DocumentIndex(base_path=self.base_path)
    
    def scan_directory(self, directory: Path, category: str = "", recursive: bool = True):
        """Scan a directory for markdown files"""
        if not directory.exists():
            print(f"Warning: Directory not found: {directory}", file=sys.stderr)
            return
        
        print(f"Scanning {directory}...")
        
        # Find all markdown files
        if recursive:
            md_files = list(directory.rglob('*.md'))
        else:
            md_files = list(directory.glob('*.md'))
        
        for md_file in md_files:
            self._process_document(md_file, category)
        
        print(f"  Found {len(md_files)} documents")
    
    def _process_document(self, file_path: Path, category: str = ""):
        """Process a single document"""
        try:
            # Parse markdown
            parser = MarkdownParser(file_path)
            metadata = parser.parse()
            
            # Extract project name from path if in build-guides
            project = ""
            if 'build-guides' in file_path.parts:
                # Get project directory name
                build_guides_idx = file_path.parts.index('build-guides')
                if build_guides_idx + 1 < len(file_path.parts):
                    project = file_path.parts[build_guides_idx + 1]
            
            # Generate description from first paragraph or heading
            description = self._extract_description(metadata)
            
            # Create entry
            entry = DocumentEntry(
                file_path=file_path,
                title=metadata.title,
                description=description,
                category=category,
                project=project,
                metadata=metadata
            )
            
            self.index.add_document(entry)
        
        except Exception as e:
            print(f"  Error processing {file_path}: {e}", file=sys.stderr)
    
    def _extract_description(self, metadata: MarkdownMetadata) -> str:
        """Extract a brief description from the document"""
        # Use first heading after title, or first few words
        if len(metadata.headings) > 1:
            return metadata.headings[1].text
        
        # Read first paragraph from file
        try:
            with open(metadata.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Skip title and find first non-empty line
            in_content = False
            for line in lines:
                line = line.strip()
                
                # Skip headings
                if line.startswith('#'):
                    in_content = True
                    continue
                
                # Skip empty lines
                if not line:
                    continue
                
                # Found first content line
                if in_content and not line.startswith('|') and not line.startswith('-'):
                    # Truncate to reasonable length
                    if len(line) > 100:
                        return line[:97] + "..."
                    return line
        
        except Exception:
            pass
        
        return ""
    
    def scan_build_guides(self):
        """Scan build guides directory"""
        build_guides_dir = self.base_path / 'docs' / 'build-guides'
        self.scan_directory(build_guides_dir, category="Build Guides", recursive=True)
    
    def scan_technical_specs(self):
        """Scan technical specifications"""
        docs_dir = self.base_path / 'docs'
        
        # Scan top-level docs (excluding build-guides subdirectory)
        if docs_dir.exists():
            print(f"Scanning {docs_dir} for technical specifications...")
            
            for md_file in docs_dir.glob('*.md'):
                self._process_document(md_file, category="Technical Specifications")
    
    def scan_all(self):
        """Scan all documentation directories"""
        self.scan_build_guides()
        self.scan_technical_specs()
        
        # Scan other documentation directories
        other_dirs = [
            ('firmware/flashing-guides', 'Firmware Guides'),
            ('templates', 'Design Templates'),
        ]
        
        for dir_path, category in other_dirs:
            full_path = self.base_path / dir_path
            if full_path.exists():
                self.scan_directory(full_path, category=category, recursive=True)
    
    def generate_indexes(self, output_dir: Path):
        """Generate all index files"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate master index
        master_index_path = output_dir / 'documentation_index.md'
        self.index.generate_master_index(master_index_path)
        
        # Generate category indexes
        for category in self.index.categories.keys():
            category_filename = category.lower().replace(' ', '_') + '_index.md'
            category_path = output_dir / category_filename
            self.index.generate_category_index(category, category_path)
        
        print(f"\n✓ Generated {len(self.index.categories) + 1} index files")


def main():
    """Command-line interface for documentation indexer"""
    if len(sys.argv) < 2:
        print("Usage: index_documentation.py <base-directory> [output-directory]")
        print("\nGenerates master documentation indexes")
        print("\nExample:")
        print("  index_documentation.py PCB")
        print("  index_documentation.py PCB PCB/docs")
        sys.exit(1)
    
    base_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else base_path / 'docs'
    
    if not base_path.exists():
        print(f"Error: Directory not found: {base_path}", file=sys.stderr)
        sys.exit(1)
    
    # Create indexer
    indexer = DocumentationIndexer(base_path)
    
    # Scan all documentation
    print("Scanning documentation...")
    indexer.scan_all()
    
    if not indexer.index.documents:
        print("\nNo documentation found", file=sys.stderr)
        sys.exit(1)
    
    # Generate indexes
    print(f"\nGenerating indexes...")
    indexer.generate_indexes(output_dir)
    
    print(f"\n✓ Documentation indexing complete!")
    print(f"  Total documents: {len(indexer.index.documents)}")
    print(f"  Categories: {len(indexer.index.categories)}")
    print(f"  Projects: {len(indexer.index.projects)}")


if __name__ == '__main__':
    main()
