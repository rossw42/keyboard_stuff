"""
QMK Format Converter

A utility to translate between KLE (Keyboard Layout Editor), VIA, and keymap.c formats
for the QMK community. This package provides bidirectional conversion capabilities
between the three most common keyboard layout formats.

Supported Formats:
- KLE (Keyboard Layout Editor) JSON format
- VIA JSON specification format  
- QMK keymap.c source files

Author: QMK Community
License: Same as QMK
"""

__version__ = "1.0.0"
__author__ = "QMK Community"

from .qmk_converter import QMKFormatConverter
from .data_models.universal_layout import UniversalLayout, KeyDefinition

__all__ = ['QMKFormatConverter', 'UniversalLayout', 'KeyDefinition']
