"""Template extraction and management system.

This module handles extraction of circuit templates from the PCB library
and provides a caching system for fast reuse.
"""

from thkg.templates.extractor import TemplateExtractor
from thkg.templates.manager import TemplateManager
from thkg.templates.models import CircuitTemplate, Component, Connection
from thkg.templates.identifier import CircuitBlockIdentifier, identify_circuit_blocks
from thkg.templates.kicad_parser import parse_kicad_schematic

__all__ = [
    "TemplateExtractor",
    "TemplateManager",
    "CircuitTemplate",
    "Component",
    "Connection",
    "CircuitBlockIdentifier",
    "identify_circuit_blocks",
    "parse_kicad_schematic",
]
