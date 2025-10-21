"""Configuration management for THKG"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class KeyboardType(Enum):
    """Keyboard type categories"""
    KEYBOARD = "keyboard"
    NUMPAD = "numpad"
    MACROPAD = "macropad"


class LayoutStyle(Enum):
    """Layout style options"""
    STAGGERED = "staggered"
    ORTHO = "ortho"
    CUSTOM = "custom"


class MCUType(Enum):
    """Supported MCU types"""
    ATMEGA328P = "atmega328p"
    ATMEGA32A = "atmega32a"
    PRO_MICRO = "pro_micro"


class USBType(Enum):
    """USB connector types"""
    USB_C_THT = "usb-c-tht"
    USB_MINI = "usb-mini"
    USB_MICRO = "usb-micro"


@dataclass
class Switch:
    """Represents a single switch in the layout"""
    row: int
    col: int
    x: float  # Physical X position (mm)
    y: float  # Physical Y position (mm)
    width: float = 1.0  # Key width (units)
    height: float = 1.0  # Key height (units)
    rotation: float = 0.0  # Rotation angle (degrees)
    stabilizer: Optional[str] = None  # None, "2u", "6.25u", "7u"
    label: str = ""


@dataclass
class Matrix:
    """Matrix configuration"""
    rows: int
    cols: int
    diode_direction: str = "COL2ROW"  # COL2ROW or ROW2COL
    row_pins: List[str] = field(default_factory=list)
    col_pins: List[str] = field(default_factory=list)


@dataclass
class USBProtectionConfig:
    """USB protection circuit components (ai03 standard)"""
    esd_protection: str = "USBLC6-2SC6"  # ESD protection IC
    esd_footprint: str = "SOT-23-6"
    ferrite_bead_value: str = "600Ω@100MHz"  # L1, L2
    ferrite_footprint: str = "0805"
    polyfuse_rating: str = "500mA"  # F1
    polyfuse_footprint: str = "1206"
    cc_resistor_value: str = "5.1kΩ"  # R1, R2 for USB-C
    cc_resistor_footprint: str = "0805"
    decoupling_cap_value: str = "100nF"  # C1, C2
    decoupling_cap_footprint: str = "0805"


@dataclass
class CrystalConfig:
    """Crystal oscillator circuit (16MHz standard)"""
    frequency: str = "16MHz"
    load_capacitance: str = "22pF"  # C5, C6
    crystal_footprint: str = "HC-49S"  # Through-hole crystal
    cap_footprint: str = "C_Disc_D3.0mm_W1.6mm_P2.50mm"  # THT ceramic cap


@dataclass
class DecouplingConfig:
    """Decoupling capacitors for MCU"""
    value: str = "100nF"  # Standard value
    footprint: str = "C_Disc_D3.0mm_W1.6mm_P2.50mm"  # THT ceramic cap
    quantity: int = 4  # One per VCC pin


@dataclass
class DiodeConfig:
    """Matrix diodes (through-hole)"""
    part_number: str = "1N4148"  # Standard switching diode
    footprint: str = "D_DO-35_SOD27_P7.62mm_Horizontal"  # THT diode
    forward_voltage: str = "1V"
    current_rating: str = "200mA"


@dataclass
class PCBLayoutRules:
    """PCB layout design rules (2-layer standard)"""
    # Trace widths (mm)
    trace_signal_min: float = 0.25
    trace_signal_recommended: float = 0.4
    trace_power_min: float = 0.5
    trace_power_recommended: float = 0.8
    trace_usb_differential: float = 0.4  # 90Ω impedance
    
    # Clearances (mm)
    clearance_min: float = 0.2
    clearance_recommended: float = 0.3
    clearance_high_voltage: float = 0.5
    
    # Vias
    via_drill: float = 0.3
    via_diameter: float = 0.6
    
    # Component spacing
    component_spacing_min: float = 0.5
    crystal_to_mcu_max: float = 10.0  # Crystal within 10mm of MCU
    decoupling_to_pin_max: float = 5.0  # Decoupling caps close to pins


@dataclass
class PCBConfig:
    """PCB specifications"""
    # Dimensions (auto-calculated from layout, or use GH60 standard)
    length: float = 285.0  # mm (GH60 standard)
    width: float = 94.6  # mm (GH60 standard)
    thickness: float = 1.6  # mm (standard)
    corner_radius: float = 2.0  # mm
    
    # Manufacturing specs
    layers: int = 2
    copper_weight: str = "1oz"  # 35µm
    surface_finish: str = "HASL"  # or "ENIG"
    solder_mask_color: str = "green"
    silkscreen_color: str = "white"
    
    # Components
    usb_protection: USBProtectionConfig = field(default_factory=USBProtectionConfig)
    crystal: CrystalConfig = field(default_factory=CrystalConfig)
    decoupling: DecouplingConfig = field(default_factory=DecouplingConfig)
    diodes: DiodeConfig = field(default_factory=DiodeConfig)
    layout_rules: PCBLayoutRules = field(default_factory=PCBLayoutRules)


@dataclass
class PlateConfig:
    """Plate configuration"""
    enabled: bool = True
    switch_type: str = "mx"  # mx, alps, choc
    thickness: float = 1.5  # mm
    material: str = "fr4"


@dataclass
class CaseConfig:
    """Case configuration"""
    enabled: bool = True
    case_type: str = "sandwich"  # sandwich, tray, integrated
    layers: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class FirmwareConfig:
    """Firmware configuration"""
    qmk: bool = True
    via: bool = True
    vial: bool = False
    default_keymap: str = "ansi"


@dataclass
class Configuration:
    """Main configuration object"""
    # Metadata
    name: str = "MyKeyboard"
    description: str = ""
    version: str = "1.0"
    
    # Layout
    keyboard_type: KeyboardType = KeyboardType.KEYBOARD
    layout_style: LayoutStyle = LayoutStyle.STAGGERED
    layout_preset: Optional[str] = None
    kle_file: Optional[str] = None
    switches: List[Switch] = field(default_factory=list)
    
    # Hardware
    mcu_type: MCUType = MCUType.ATMEGA328P
    usb_type: USBType = USBType.USB_C_THT
    
    # Matrix
    matrix: Optional[Matrix] = None
    
    # Components
    pcb: PCBConfig = field(default_factory=PCBConfig)
    plate: PlateConfig = field(default_factory=PlateConfig)
    case: CaseConfig = field(default_factory=CaseConfig)
    firmware: FirmwareConfig = field(default_factory=FirmwareConfig)
    
    # Output options
    output_gerbers: bool = True
    output_kicad: bool = True
    output_plate_dxf: bool = True
    output_case_stl: bool = True
    output_case_dxf: bool = True
    output_firmware: bool = True
    output_bom: bool = True
    output_build_guide: bool = True
