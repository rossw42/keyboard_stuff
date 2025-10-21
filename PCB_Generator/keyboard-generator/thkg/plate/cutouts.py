"""Switch and stabilizer cutout generation"""

from typing import List, Tuple
from thkg.config import Switch


class CutoutGenerator:
    """Generate cutouts for switches and stabilizers"""
    
    # Switch cutout dimensions (mm)
    SWITCH_CUTOUTS = {
        'mx': {
            'width': 14.0,
            'height': 14.0,
            'corner_radius': 0.5
        },
        'alps': {
            'width': 15.5,
            'height': 12.8,
            'corner_radius': 0.0
        },
        'choc': {
            'width': 13.8,
            'height': 13.8,
            'corner_radius': 0.5
        }
    }
    
    # Stabilizer cutout dimensions (mm)
    STABILIZER_CUTOUTS = {
        '2u': {
            'spacing': 11.95,  # Distance from switch center to stab center
            'width': 3.05,
            'height': 13.0
        },
        '6.25u': {
            'spacing': 50.0,
            'width': 3.05,
            'height': 13.0
        },
        '7u': {
            'spacing': 57.15,
            'width': 3.05,
            'height': 13.0
        }
    }
    
    def get_switch_cutout(self, switch: Switch, switch_type: str = 'mx') -> List[Tuple[float, float]]:
        """Get switch cutout rectangle
        
        Args:
            switch: Switch object
            switch_type: Type of switch (mx, alps, choc)
            
        Returns:
            List of (x, y) points for cutout rectangle
        """
        cutout = self.SWITCH_CUTOUTS.get(switch_type, self.SWITCH_CUTOUTS['mx'])
        
        # Calculate cutout center (switch center)
        center_x = switch.x + (switch.width * 19.05 / 2)
        center_y = switch.y + (switch.height * 19.05 / 2)
        
        # Calculate cutout corners
        half_w = cutout['width'] / 2
        half_h = cutout['height'] / 2
        
        return [
            (center_x - half_w, center_y - half_h),  # Bottom-left
            (center_x + half_w, center_y - half_h),  # Bottom-right
            (center_x + half_w, center_y + half_h),  # Top-right
            (center_x - half_w, center_y + half_h),  # Top-left
        ]
    
    def get_stabilizer_cutouts(self, switch: Switch, switch_type: str = 'mx') -> List[List[Tuple[float, float]]]:
        """Get stabilizer cutouts for a switch
        
        Args:
            switch: Switch object
            switch_type: Type of switch (for compatibility)
            
        Returns:
            List of cutout rectangles (each is a list of (x, y) points)
        """
        if not switch.stabilizer:
            return []
        
        stab_config = self.STABILIZER_CUTOUTS.get(switch.stabilizer)
        if not stab_config:
            return []
        
        # Calculate switch center
        center_x = switch.x + (switch.width * 19.05 / 2)
        center_y = switch.y + (switch.height * 19.05 / 2)
        
        # Calculate stabilizer positions (left and right)
        spacing = stab_config['spacing']
        width = stab_config['width']
        height = stab_config['height']
        
        cutouts = []
        
        # Left stabilizer
        left_x = center_x - spacing
        cutout = [
            (left_x - width/2, center_y - height/2),
            (left_x + width/2, center_y - height/2),
            (left_x + width/2, center_y + height/2),
            (left_x - width/2, center_y + height/2),
        ]
        cutouts.append(cutout)
        
        # Right stabilizer
        right_x = center_x + spacing
        cutout = [
            (right_x - width/2, center_y - height/2),
            (right_x + width/2, center_y - height/2),
            (right_x + width/2, center_y + height/2),
            (right_x - width/2, center_y + height/2),
        ]
        cutouts.append(cutout)
        
        return cutouts
    
    def get_mounting_hole(self, x: float, y: float, diameter: float = 2.0) -> Tuple[float, float, float]:
        """Get mounting hole specification
        
        Args:
            x: X position
            y: Y position
            diameter: Hole diameter (mm)
            
        Returns:
            Tuple of (x, y, diameter)
        """
        return (x, y, diameter)
