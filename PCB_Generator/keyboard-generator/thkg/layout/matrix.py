"""Matrix calculator for keyboard layouts"""

from typing import List, Tuple, Dict
from thkg.config import Switch, Matrix
import math


class MatrixCalculator:
    """Calculate optimal matrix configuration for switches"""
    
    def calculate_matrix(self, switches: List[Switch]) -> Matrix:
        """Calculate optimal matrix dimensions and assignments
        
        Args:
            switches: List of switches to configure
            
        Returns:
            Matrix configuration with optimal dimensions
        """
        num_switches = len(switches)
        
        # Calculate optimal dimensions (minimize rows + cols)
        rows, cols = self._calculate_dimensions(num_switches)
        
        # Assign switches to matrix positions
        matrix = Matrix(rows=rows, cols=cols)
        
        # Update switch row/col assignments if not set
        self._assign_positions(switches, rows, cols)
        
        return matrix
    
    def _calculate_dimensions(self, num_switches: int) -> Tuple[int, int]:
        """Calculate optimal matrix dimensions
        
        Args:
            num_switches: Number of switches
            
        Returns:
            Tuple of (rows, cols)
        """
        # Try to get close to square
        sqrt = math.sqrt(num_switches)
        
        # Start with square-ish dimensions
        rows = int(math.ceil(sqrt))
        cols = int(math.ceil(num_switches / rows))
        
        # Adjust to ensure we have enough positions
        while rows * cols < num_switches:
            cols += 1
        
        return (rows, cols)
    
    def _assign_positions(self, switches: List[Switch], rows: int, cols: int):
        """Assign switches to matrix positions
        
        Args:
            switches: List of switches to assign
            rows: Number of rows
            cols: Number of columns
        """
        # If switches already have row/col assignments, keep them
        if all(s.row >= 0 and s.col >= 0 for s in switches):
            return
        
        # Assign sequentially
        for i, switch in enumerate(switches):
            switch.row = i // cols
            switch.col = i % cols
    
    def optimize_matrix(self, switches: List[Switch]) -> Matrix:
        """Optimize matrix configuration to minimize rows + cols
        
        Args:
            switches: List of switches
            
        Returns:
            Optimized matrix configuration
        """
        num_switches = len(switches)
        
        # Try different configurations
        best_sum = float('inf')
        best_config = None
        
        for rows in range(1, num_switches + 1):
            cols = math.ceil(num_switches / rows)
            
            # Skip if too many positions
            if rows * cols > num_switches + 5:
                continue
            
            # Calculate score (prefer square-ish)
            sum_rc = rows + cols
            if sum_rc < best_sum:
                best_sum = sum_rc
                best_config = (rows, cols)
        
        if best_config:
            rows, cols = best_config
            matrix = Matrix(rows=rows, cols=cols)
            self._assign_positions(switches, rows, cols)
            return matrix
        
        # Fallback to simple calculation
        return self.calculate_matrix(switches)
    
    def get_matrix_map(self, switches: List[Switch]) -> Dict[Tuple[int, int], Switch]:
        """Create a map of (row, col) -> Switch
        
        Args:
            switches: List of switches
            
        Returns:
            Dictionary mapping (row, col) to Switch
        """
        return {(s.row, s.col): s for s in switches}
    
    def validate_matrix(self, switches: List[Switch], matrix: Matrix) -> List[str]:
        """Validate matrix configuration
        
        Args:
            switches: List of switches
            matrix: Matrix configuration
            
        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        
        # Check that all switches fit in matrix
        for i, switch in enumerate(switches):
            if switch.row >= matrix.rows:
                errors.append(f"Switch {i} row {switch.row} exceeds matrix rows {matrix.rows}")
            if switch.col >= matrix.cols:
                errors.append(f"Switch {i} col {switch.col} exceeds matrix cols {matrix.cols}")
        
        # Check for duplicate positions
        positions = {}
        for i, switch in enumerate(switches):
            pos = (switch.row, switch.col)
            if pos in positions:
                errors.append(f"Switches {positions[pos]} and {i} have same position {pos}")
            else:
                positions[pos] = i
        
        return errors
