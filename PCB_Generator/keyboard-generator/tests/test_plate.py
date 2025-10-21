"""Tests for plate generation"""

import pytest
from thkg.plate import PlateGenerator, CutoutGenerator
from thkg.config import Switch, PlateConfig


def test_cutout_generator():
    """Test cutout generation"""
    gen = CutoutGenerator()
    
    # Create a switch
    switch = Switch(row=0, col=0, x=0, y=0)
    
    # Get cutout
    cutout = gen.get_switch_cutout(switch, 'mx')
    assert len(cutout) == 4  # Rectangle has 4 corners


def test_stabilizer_cutouts():
    """Test stabilizer cutout generation"""
    gen = CutoutGenerator()
    
    # Create switch with stabilizer
    switch = Switch(row=0, col=0, x=0, y=0, width=6.25, stabilizer="6.25u")
    
    # Get stabilizer cutouts
    cutouts = gen.get_stabilizer_cutouts(switch)
    assert len(cutouts) == 2  # Left and right stabilizers


def test_plate_generator():
    """Test plate generation"""
    gen = PlateGenerator()
    
    # Create simple layout
    switches = [
        Switch(row=0, col=0, x=0, y=0),
        Switch(row=0, col=1, x=19.05, y=0),
        Switch(row=1, col=0, x=0, y=19.05),
    ]
    
    config = PlateConfig()
    
    # Generate plate
    plate = gen.generate_plate(switches, config)
    assert 'dimensions' in plate
    assert 'switch_cutouts' in plate
    assert len(plate['switch_cutouts']) == 3


if __name__ == '__main__':
    pytest.main([__file__])
