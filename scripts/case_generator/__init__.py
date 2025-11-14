"""
Unified Keyboard Case Generator

A PCB-first keyboard case generator that creates 3D-printable case components
from KiCad STEP exports.
"""

__version__ = "0.1.0"

from .config import CaseConfig
from .pcb_analyzer import PCBInfo, analyze_pcb
from .switch_detector import SwitchInfo, SwitchLayout, detect_switch_layout

__all__ = [
    "CaseConfig",
    "PCBInfo",
    "SwitchInfo",
    "SwitchLayout",
    "analyze_pcb",
    "detect_switch_layout",
]
