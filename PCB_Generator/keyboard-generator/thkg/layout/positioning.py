"""Switch positioning calculator"""

from typing import List, Tuple
from thkg.config import Switch
import math


class PositionCalculator:
    """Calculate physical switch positions"""
    
    # Key unit size in mm (Cherry MX standard)
    KEY_UNIT = 19.05
    
    def calculate_positions(self, switches: List[Switch]) -> List[Switch]:
        """Calculate physical positions for switches
        
        Args:
            switches: List of switches with row/col assignments
            
        Returns:
            List of switches with calculated x/y positions
        """
        # If switches already have positions, return as-is
        if all(s.x != 0 or s.y != 0 for s in switches):
            return switches
        
        # Calculate positions based on row/col
        positioned = []
        for switch in switches:
            x = switch.col * self.KEY_UNIT
            y = switch.row * self.KEY_UNIT
            
            positioned.append(Switch(
                row=switch.row,
                col=switch.col,
                x=x,
                y=y,
                width=switch.width,
                height=switch.height,
                rotation=switch.rotation,
                stabilizer=switch.stabilizer,
                label=switch.label
            ))
        
        return positioned
    
    def get_bounding_box(self, switches: List[Switch]) -> Tuple[float, float, float, float]:
        """Calculate bounding box for switches
        
        Args:
            switches: List of switches
            
        Returns:
            Tuple of (min_x, min_y, max_x, max_y) in mm
        """
        if not switches:
            return (0, 0, 0, 0)
        
        min_x = min(s.x for s in switches)
        min_y = min(s.y for s in switches)
        max_x = max(s.x + (s.width * self.KEY_UNIT) for s in switches)
        max_y = max(s.y + (s.height * self.KEY_UNIT) for s in switches)
        
        return (min_x, min_y, max_x, max_y)
    
    def get_dimensions(self, switches: List[Switch]) -> Tuple[float, float]:
        """Get overall dimensions of layout
        
        Args:
            switches: List of switches
            
        Returns:
            Tuple of (width, height) in mm
        """
        min_x, min_y, max_x, max_y = self.get_bounding_box(switches)
        return (max_x - min_x, max_y - min_y)
    
    def normalize_positions(self, switches: List[Switch]) -> List[Switch]:
        """Normalize switch positions to start at (0, 0)
        
        Args:
            switches: List of switches
            
        Returns:
            List of switches with normalized positions
        """
        if not switches:
            return switches
        
        min_x = min(s.x for s in switches)
        min_y = min(s.y for s in switches)
        
        normalized = []
        for switch in switches:
            normalized.append(Switch(
                row=switch.row,
                col=switch.col,
                x=switch.x - min_x,
                y=switch.y - min_y,
                width=switch.width,
                height=switch.height,
                rotation=switch.rotation,
                stabilizer=switch.stabilizer,
                label=switch.label
            ))
        
        return normalized
    
    def check_spacing(self, switches: List[Switch], min_spacing: float = 0.5) -> List[Tuple[int, int]]:
        """Check for switches that are too close together
        
        Args:
            switches: List of switches
            min_spacing: Minimum spacing in mm
            
        Returns:
            List of (index1, index2) tuples for switches that are too close
        """
        violations = []
        
        for i, s1 in enumerate(switches):
            for j, s2 in enumerate(switches[i+1:], start=i+1):
                # Calculate distance between switch centers
                dx = s2.x - s1.x
                dy = s2.y - s1.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Calculate minimum required distance
                min_dist = (max(s1.width, s2.width) * self.KEY_UNIT / 2 + 
                           max(s1.height, s2.height) * self.KEY_UNIT / 2)
                
                if distance < (min_dist + min_spacing):
                    violations.append((i, j))
        
        return violations
