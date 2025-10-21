"""Plate generator for keyboard layouts"""

from typing import List, Tuple
from thkg.config import Switch, PlateConfig
from thkg.plate.cutouts import CutoutGenerator


class PlateGenerator:
    """Generate plate designs for keyboards"""
    
    def __init__(self):
        self.cutout_gen = CutoutGenerator()
    
    def generate_plate(self, switches: List[Switch], config: PlateConfig) -> dict:
        """Generate plate design
        
        Args:
            switches: List of switches
            config: Plate configuration
            
        Returns:
            Dictionary with plate data
        """
        # Calculate plate dimensions
        dimensions = self._calculate_dimensions(switches)
        
        # Generate switch cutouts
        switch_cutouts = []
        for switch in switches:
            cutout = self.cutout_gen.get_switch_cutout(switch, config.switch_type)
            switch_cutouts.append(cutout)
        
        # Generate stabilizer cutouts
        stab_cutouts = []
        for switch in switches:
            cutouts = self.cutout_gen.get_stabilizer_cutouts(switch, config.switch_type)
            stab_cutouts.extend(cutouts)
        
        # Generate mounting holes (placeholder - will be based on PCB)
        mounting_holes = self._get_default_mounting_holes(dimensions)
        
        return {
            'dimensions': dimensions,
            'switch_cutouts': switch_cutouts,
            'stabilizer_cutouts': stab_cutouts,
            'mounting_holes': mounting_holes,
            'thickness': config.thickness,
            'material': config.material
        }
    
    def _calculate_dimensions(self, switches: List[Switch]) -> Tuple[float, float]:
        """Calculate plate dimensions based on switches"""
        if not switches:
            return (0, 0)
        
        # Find bounding box
        min_x = min(s.x for s in switches)
        min_y = min(s.y for s in switches)
        max_x = max(s.x + s.width * 19.05 for s in switches)
        max_y = max(s.y + s.height * 19.05 for s in switches)
        
        # Add margin
        margin = 10.0  # mm
        width = (max_x - min_x) + 2 * margin
        height = (max_y - min_y) + 2 * margin
        
        return (width, height)
    
    def _get_default_mounting_holes(self, dimensions: Tuple[float, float]) -> List[Tuple[float, float, float]]:
        """Get default mounting hole positions"""
        width, height = dimensions
        margin = 10.0
        
        # Place holes in corners
        return [
            (margin, margin, 2.0),
            (width - margin, margin, 2.0),
            (margin, height - margin, 2.0),
            (width - margin, height - margin, 2.0),
        ]
