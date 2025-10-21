"""Data models for circuit templates."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


@dataclass
class Component:
    """Electronic component in a circuit."""
    
    reference: str  # "U1", "R1", "C1"
    value: str  # "ATmega328P", "10kΩ", "0.1µF"
    footprint: str  # "DIP-28", "Axial-0.3", "C_Disc_D3.0mm"
    library: str  # "MCU_Microchip_ATmega", "Device"
    symbol: str  # Full symbol name
    position: Optional[Tuple[float, float]] = None  # (x, y) in mm
    rotation: float = 0.0  # degrees
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __str__(self):
        return f"{self.reference} ({self.value})"


@dataclass
class Connection:
    """Net connection between components."""
    
    net_name: str  # "VCC", "GND", "ROW0"
    pins: List[Tuple[str, str]]  # [(component_ref, pin_number), ...]
    
    def __str__(self):
        return f"{self.net_name}: {len(self.pins)} pins"


@dataclass
class CircuitTemplate:
    """Reusable circuit block extracted from library."""
    
    name: str  # "atmega328p_circuit", "usb_c_circuit"
    type: str  # "mcu", "usb", "reset", "crystal"
    source_project: str  # "lumberjack", "discipline"
    version: str  # "1.8", "2.0"
    
    components: List[Component] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)
    
    # Interface pins (for connecting to other circuits)
    input_pins: Dict[str, str] = field(default_factory=dict)  # {logical_name: net_name}
    output_pins: Dict[str, str] = field(default_factory=dict)  # {logical_name: net_name}
    
    # Power requirements
    power_nets: Dict[str, float] = field(default_factory=dict)  # {net_name: current_mA}
    
    # Metadata
    description: str = ""
    notes: str = ""
    
    def __str__(self):
        return f"{self.name} ({self.type}): {len(self.components)} components"
    
    def get_component(self, reference: str) -> Optional[Component]:
        """Get component by reference designator."""
        for comp in self.components:
            if comp.reference == reference:
                return comp
        return None
    
    def get_connections_for_component(self, reference: str) -> List[Connection]:
        """Get all connections involving a component."""
        result = []
        for conn in self.connections:
            for comp_ref, pin in conn.pins:
                if comp_ref == reference:
                    result.append(conn)
                    break
        return result


@dataclass
class Trace:
    """PCB trace segment."""
    
    start: Tuple[float, float]  # (x, y) in mm
    end: Tuple[float, float]  # (x, y) in mm
    width: float  # mm
    layer: str  # "F.Cu", "B.Cu", etc.
    net: int  # Net number
    net_name: str = ""  # Net name (e.g., "GND", "VCC")
    tstamp: str = ""  # Timestamp/UUID
    
    def __str__(self):
        return f"Trace on {self.layer}: {self.start} -> {self.end} (net {self.net})"


@dataclass
class Via:
    """PCB via."""
    
    position: Tuple[float, float]  # (x, y) in mm
    size: float  # mm (outer diameter)
    drill: float  # mm (hole diameter)
    layers: Tuple[str, str]  # ("F.Cu", "B.Cu")
    net: int  # Net number
    net_name: str = ""  # Net name
    tstamp: str = ""  # Timestamp/UUID
    
    def __str__(self):
        return f"Via at {self.position}: {self.size}mm (net {self.net})"


@dataclass
class Zone:
    """PCB copper zone (ground plane, etc.)."""
    
    net: int  # Net number
    net_name: str  # Net name (usually "GND")
    layer: str  # "F.Cu", "B.Cu", etc.
    priority: int = 0
    filled_polygons: List[List[Tuple[float, float]]] = field(default_factory=list)
    tstamp: str = ""
    
    def __str__(self):
        return f"Zone on {self.layer}: {self.net_name} (net {self.net})"


@dataclass
class Net:
    """PCB net definition."""
    
    number: int  # Net number (0 = no net)
    name: str  # Net name
    
    def __str__(self):
        return f"Net {self.number}: {self.name}"


@dataclass
class PCBRouting:
    """Complete routing information from a PCB."""
    
    nets: List[Net] = field(default_factory=list)
    traces: List[Trace] = field(default_factory=list)
    vias: List[Via] = field(default_factory=list)
    zones: List[Zone] = field(default_factory=list)
    
    def get_net_by_number(self, net_num: int) -> Optional[Net]:
        """Get net by number."""
        for net in self.nets:
            if net.number == net_num:
                return net
        return None
    
    def get_net_by_name(self, net_name: str) -> Optional[Net]:
        """Get net by name."""
        for net in self.nets:
            if net.name == net_name:
                return net
        return None
    
    def get_traces_for_net(self, net_num: int) -> List[Trace]:
        """Get all traces for a specific net."""
        return [t for t in self.traces if t.net == net_num]
    
    def get_vias_for_net(self, net_num: int) -> List[Via]:
        """Get all vias for a specific net."""
        return [v for v in self.vias if v.net == net_num]
    
    def __str__(self):
        return f"PCB Routing: {len(self.nets)} nets, {len(self.traces)} traces, {len(self.vias)} vias, {len(self.zones)} zones"


@dataclass
class TemplateMetadata:
    """Metadata about a cached template."""
    
    name: str
    type: str
    source_project: str
    version: str
    extracted_date: str
    file_path: str
    checksum: str  # MD5 of source file
    
    def __str__(self):
        return f"{self.name} from {self.source_project} v{self.version}"
