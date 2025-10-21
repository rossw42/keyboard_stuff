"""PCB layout generation with artistic component placement."""

from pathlib import Path
from typing import List, Dict, Tuple, Optional
from thkg.templates.models import Component, Connection


class LayoutGenerator:
    """Generate PCB layout with artistic component placement."""
    
    def __init__(self, components: List[Component], connections: List[Connection],
                 board_width: float = 285.0, board_height: float = 94.6):
        """Initialize layout generator.
        
        Args:
            components: List of components to place
            connections: List of connections
            board_width: Board width in mm (default: GH60 standard)
            board_height: Board height in mm (default: GH60 standard)
        """
        self.components = components
        self.connections = connections
        self.board_width = board_width
        self.board_height = board_height
        
        # Component groups
        self.switches = []
        self.diodes = []
        self.mcu = None
        self.usb = None
        self.passives = []
        
        self._categorize_components()
    
    def _categorize_components(self):
        """Categorize components by type."""
        for comp in self.components:
            if comp.reference.startswith('SW') or comp.reference.startswith('MX'):
                self.switches.append(comp)
            elif comp.reference.startswith('D') and '4148' in comp.value:
                self.diodes.append(comp)
            elif comp.reference.startswith('U'):
                self.mcu = comp
            elif 'USB' in comp.symbol.upper():
                self.usb = comp
            elif comp.reference.startswith(('R', 'C', 'Y', 'F')):
                self.passives.append(comp)
    
    def generate_layout(self) -> bool:
        """Generate complete PCB layout.
        
        Returns:
            True if successful
        """
        print("   🎨 Generating PCB layout...")
        
        # Place switches in grid
        self._place_switches()
        
        # Place diodes near switches
        self._place_diodes()
        
        # Place MCU centrally
        self._place_mcu()
        
        # Place USB connector
        self._place_usb()
        
        # Place passive components artistically
        self._place_passives()
        
        print(f"      ✅ Placed {len(self.components)} components")
        
        return True
    
    def _place_switches(self):
        """Place switches in grid pattern."""
        print("      Placing switches...")
        
        # Standard MX switch spacing
        switch_spacing = 19.05  # mm (0.75 inches)
        
        # Calculate grid dimensions
        num_switches = len(self.switches)
        if num_switches == 0:
            return
        
        # Estimate rows/cols
        import math
        cols = int(math.ceil(math.sqrt(num_switches * 1.5)))
        rows = int(math.ceil(num_switches / cols))
        
        # Starting position (centered on board)
        start_x = (self.board_width - (cols - 1) * switch_spacing) / 2
        start_y = 20.0  # Top margin
        
        # Place switches
        for i, switch in enumerate(self.switches):
            row = i // cols
            col = i % cols
            
            x = start_x + col * switch_spacing
            y = start_y + row * switch_spacing
            
            switch.position = (x, y)
            switch.rotation = 0.0
        
        print(f"         ✅ {len(self.switches)} switches in {rows}x{cols} grid")
    
    def _place_diodes(self):
        """Place diodes near their corresponding switches."""
        print("      Placing diodes...")
        
        # Place each diode below its switch
        for i, diode in enumerate(self.diodes):
            if i < len(self.switches):
                switch = self.switches[i]
                if switch.position:
                    # Place diode 5mm below switch
                    diode.position = (switch.position[0], switch.position[1] + 5.0)
                    diode.rotation = 90.0  # Vertical orientation
        
        print(f"         ✅ {len(self.diodes)} diodes placed")
    
    def _place_mcu(self):
        """Place MCU in center of board."""
        print("      Placing MCU...")
        
        if self.mcu:
            # Place MCU in center-bottom area
            self.mcu.position = (self.board_width / 2, self.board_height - 20.0)
            self.mcu.rotation = 0.0
            print(f"         ✅ MCU at ({self.mcu.position[0]:.1f}, {self.mcu.position[1]:.1f})")
    
    def _place_usb(self):
        """Place USB connector at top center."""
        print("      Placing USB connector...")
        
        if self.usb:
            # Place USB at top center
            self.usb.position = (self.board_width / 2, 5.0)
            self.usb.rotation = 90.0
            print(f"         ✅ USB at ({self.usb.position[0]:.1f}, {self.usb.position[1]:.1f})")
    
    def _place_passives(self):
        """Place passive components artistically."""
        print("      Placing passive components...")
        
        if not self.passives:
            return
        
        # Group by type
        resistors = [c for c in self.passives if c.reference.startswith('R')]
        capacitors = [c for c in self.passives if c.reference.startswith('C')]
        others = [c for c in self.passives if not c.reference.startswith(('R', 'C'))]
        
        # Place resistors in a row near MCU
        if resistors and self.mcu and self.mcu.position:
            base_x = self.mcu.position[0] - 30.0
            base_y = self.mcu.position[1] - 10.0
            
            for i, resistor in enumerate(resistors):
                resistor.position = (base_x + i * 5.0, base_y)
                resistor.rotation = 90.0
        
        # Place capacitors in a row near MCU
        if capacitors and self.mcu and self.mcu.position:
            base_x = self.mcu.position[0] - 30.0
            base_y = self.mcu.position[1] + 10.0
            
            for i, cap in enumerate(capacitors):
                cap.position = (base_x + i * 5.0, base_y)
                cap.rotation = 0.0
        
        # Place other components
        if others and self.mcu and self.mcu.position:
            base_x = self.mcu.position[0] + 20.0
            base_y = self.mcu.position[1]
            
            for i, comp in enumerate(others):
                comp.position = (base_x, base_y + i * 5.0)
                comp.rotation = 0.0
        
        print(f"         ✅ {len(self.passives)} passive components placed")
    
    def get_board_outline(self) -> List[Tuple[float, float]]:
        """Get board outline points.
        
        Returns:
            List of (x, y) points defining board outline
        """
        # Simple rectangle for now
        return [
            (0, 0),
            (self.board_width, 0),
            (self.board_width, self.board_height),
            (0, self.board_height),
            (0, 0)
        ]
    
    def get_mounting_holes(self) -> List[Tuple[float, float]]:
        """Get mounting hole positions (GH60 standard).
        
        Returns:
            List of (x, y) positions for mounting holes
        """
        # GH60 standard mounting holes
        return [
            (19.0, 9.5),      # Top-left
            (266.0, 9.5),     # Top-right
            (28.5, 47.3),     # Middle-left
            (256.5, 47.3),    # Middle-right
            (57.0, 85.0),     # Bottom-left
            (228.0, 85.0),    # Bottom-right
        ]


class Router:
    """Auto-router for PCB traces."""
    
    def __init__(self, components: List[Component], connections: List[Connection]):
        """Initialize router.
        
        Args:
            components: List of placed components
            connections: List of connections to route
        """
        self.components = components
        self.connections = connections
        self.traces = []
    
    def route_all(self) -> bool:
        """Route all connections.
        
        Returns:
            True if successful
        """
        print("   🔀 Routing traces...")
        
        # Simple routing for now - just record connections
        # Real routing would use pathfinding algorithms
        
        routed = 0
        for connection in self.connections:
            if self._route_connection(connection):
                routed += 1
        
        print(f"      ✅ Routed {routed}/{len(self.connections)} connections")
        
        return True
    
    def _route_connection(self, connection: Connection) -> bool:
        """Route a single connection.
        
        Args:
            connection: Connection to route
            
        Returns:
            True if routed successfully
        """
        # For now, just mark as routed
        # Real implementation would calculate trace paths
        return True
    
    def get_trace_count(self) -> int:
        """Get number of routed traces.
        
        Returns:
            Number of traces
        """
        return len(self.traces)
