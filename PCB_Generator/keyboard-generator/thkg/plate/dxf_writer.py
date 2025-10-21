"""DXF file writer for plates"""

import ezdxf
from typing import List, Tuple


class DXFWriter:
    """Write plate designs to DXF format"""
    
    def write_plate(self, plate_data: dict, output_path: str):
        """Write plate to DXF file
        
        Args:
            plate_data: Plate data from PlateGenerator
            output_path: Path to output DXF file
        """
        # Create new DXF document
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        
        # Add plate outline
        width, height = plate_data['dimensions']
        self._add_rectangle(msp, 0, 0, width, height, layer='OUTLINE')
        
        # Add switch cutouts
        for cutout in plate_data['switch_cutouts']:
            self._add_polygon(msp, cutout, layer='CUTOUTS')
        
        # Add stabilizer cutouts
        for cutout in plate_data['stabilizer_cutouts']:
            self._add_polygon(msp, cutout, layer='CUTOUTS')
        
        # Add mounting holes
        for x, y, diameter in plate_data['mounting_holes']:
            self._add_circle(msp, x, y, diameter / 2, layer='HOLES')
        
        # Save DXF file
        doc.saveas(output_path)
    
    def _add_rectangle(self, msp, x: float, y: float, width: float, height: float, layer: str = '0'):
        """Add rectangle to DXF"""
        points = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
            (x, y)  # Close the rectangle
        ]
        msp.add_lwpolyline(points, dxfattribs={'layer': layer})
    
    def _add_polygon(self, msp, points: List[Tuple[float, float]], layer: str = '0'):
        """Add polygon to DXF"""
        # Close the polygon
        closed_points = list(points) + [points[0]]
        msp.add_lwpolyline(closed_points, dxfattribs={'layer': layer})
    
    def _add_circle(self, msp, x: float, y: float, radius: float, layer: str = '0'):
        """Add circle to DXF"""
        msp.add_circle((x, y), radius, dxfattribs={'layer': layer})
