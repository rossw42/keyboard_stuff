"""Switch matrix generation for keyboard schematics."""

from typing import List, Tuple, Dict
from thkg.templates.models import Component, Connection


class MatrixGenerator:
    """Generate keyboard switch matrix."""
    
    def __init__(self, num_switches: int, rows: int = None, cols: int = None):
        """Initialize matrix generator.
        
        Args:
            num_switches: Total number of switches
            rows: Number of rows (auto-calculated if None)
            cols: Number of columns (auto-calculated if None)
        """
        self.num_switches = num_switches
        
        # Calculate optimal matrix dimensions if not provided
        if rows is None or cols is None:
            self.rows, self.cols = self._calculate_matrix_dimensions()
        else:
            self.rows = rows
            self.cols = cols
    
    def _calculate_matrix_dimensions(self) -> Tuple[int, int]:
        """Calculate optimal matrix dimensions.
        
        Returns:
            Tuple of (rows, cols)
        """
        # Try to make it as square as possible
        import math
        sqrt = int(math.sqrt(self.num_switches))
        
        # Find factors close to square root
        for rows in range(sqrt, 0, -1):
            if self.num_switches % rows == 0:
                cols = self.num_switches // rows
                return (rows, cols)
        
        # Fallback: use common keyboard dimensions
        if self.num_switches <= 48:
            return (4, 12)  # 40% ortho
        elif self.num_switches <= 60:
            return (5, 12)  # 60% ortho
        elif self.num_switches <= 68:
            return (5, 14)  # 65%
        else:
            return (6, 15)  # TKL
    
    def generate_components(self) -> Tuple[List[Component], List[Component]]:
        """Generate switch and diode components.
        
        Returns:
            Tuple of (switches, diodes)
        """
        switches = []
        diodes = []
        
        for i in range(1, self.num_switches + 1):
            # Create switch
            switch = Component(
                reference=f"SW{i}",
                value="MX",
                footprint="MX:MX_PCB",
                library="Switch",
                symbol="Switch:SW_Push",
                position=None,
                rotation=0.0,
                properties={}
            )
            switches.append(switch)
            
            # Create diode
            diode = Component(
                reference=f"D{i}",
                value="1N4148",
                footprint="Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal",
                library="Device",
                symbol="Device:D",
                position=None,
                rotation=0.0,
                properties={}
            )
            diodes.append(diode)
        
        return switches, diodes
    
    def generate_connections(self, switches: List[Component], 
                           diodes: List[Component]) -> List[Connection]:
        """Generate matrix connections.
        
        Args:
            switches: List of switch components
            diodes: List of diode components
            
        Returns:
            List of connections
        """
        connections = []
        
        # Create row nets
        for row in range(self.rows):
            row_pins = []
            for col in range(self.cols):
                switch_idx = row * self.cols + col
                if switch_idx < len(switches):
                    # Connect switch pin 2 to row
                    row_pins.append((switches[switch_idx].reference, "2"))
            
            if row_pins:
                connection = Connection(
                    net_name=f"ROW{row}",
                    pins=row_pins
                )
                connections.append(connection)
        
        # Create column nets
        for col in range(self.cols):
            col_pins = []
            for row in range(self.rows):
                switch_idx = row * self.cols + col
                if switch_idx < len(diodes):
                    # Connect diode cathode to column
                    col_pins.append((diodes[switch_idx].reference, "2"))
            
            if col_pins:
                connection = Connection(
                    net_name=f"COL{col}",
                    pins=col_pins
                )
                connections.append(connection)
        
        # Connect switches to diodes
        for i, (switch, diode) in enumerate(zip(switches, diodes)):
            connection = Connection(
                net_name=f"SW{i+1}_D{i+1}",
                pins=[
                    (switch.reference, "1"),
                    (diode.reference, "1")
                ]
            )
            connections.append(connection)
        
        return connections
    
    def get_pin_assignments(self) -> Dict[str, List[str]]:
        """Get MCU pin assignments for matrix.
        
        Returns:
            Dictionary with 'rows' and 'cols' pin lists
        """
        # ATmega328P pin assignments (example)
        row_pins = ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7"]
        col_pins = ["F0", "F1", "F4", "F5", "F6", "F7", "B6", "B5", 
                   "B4", "D7", "D6", "D4", "C6", "C7", "E6"]
        
        return {
            'rows': row_pins[:self.rows],
            'cols': col_pins[:self.cols]
        }
