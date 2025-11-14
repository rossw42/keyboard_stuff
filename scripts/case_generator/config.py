"""Configuration management for case generator."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any


@dataclass
class CaseConfig:
    """Configuration for keyboard case generation."""
    
    # Input files
    pcb_step_left: Optional[Path] = None
    pcb_step_right: Optional[Path] = None
    kicad_pcb: Optional[Path] = None
    output_dir: Path = Path("./output")
    side: str = "both"  # 'left', 'right', or 'both'
    
    # Case dimensions
    wall_thickness: float = 2.0  # mm
    bottom_thickness: float = 1.5  # mm
    case_height: float = 8.0  # mm
    pcb_clearance: float = 2.5  # mm
    case_offset: float = 2.5  # mm
    corner_radius: float = 1.5  # mm
    
    # Plate dimensions
    plate_thickness: float = 1.5  # mm
    plate_offset: float = 1.0  # mm
    switch_cutout_size: float = 14.0  # mm
    
    # Features
    enable_chamfers: bool = True
    outer_chamfer: float = 1.0  # mm
    inner_chamfer: float = 0.5  # mm
    enable_fillets: bool = False
    fillet_radius: float = 1.0  # mm
    
    # Screw bosses
    boss_diameter: float = 6.0  # mm (matches porne reference design)
    boss_hole_diameter: float = 2.6  # mm (M2.5 screws)
    boss_corner_inset: float = 8.0  # mm
    
    # Rubber feet
    enable_rubber_feet: bool = True
    feet_diameter: float = 10.0  # mm
    feet_depth: float = 2.0  # mm
    feet_corner_offset: float = 10.0  # mm
    
    # Plate mounting lip
    enable_plate_lip: bool = True
    lip_width: float = 1.5  # mm
    lip_height: float = 0.5  # mm
    
    # Export options
    stl_tolerance: float = 0.01  # mm
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Check input files
        if self.side == "single":
            # Single keyboard mode - only need left file
            if not self.pcb_step_left:
                errors.append("PCB STEP file required")
        elif self.side in ("left", "both") and not self.pcb_step_left:
            errors.append("Left PCB STEP file required when side is 'left' or 'both'")
        elif self.side in ("right", "both") and not self.pcb_step_right:
            errors.append("Right PCB STEP file required when side is 'right' or 'both'")
        elif self.side not in ("left", "right", "both", "single"):
            errors.append(f"Invalid side '{self.side}', must be 'left', 'right', 'both', or 'single'")
        
        # Check file existence
        if self.pcb_step_left and not self.pcb_step_left.exists():
            errors.append(f"Left PCB STEP file not found: {self.pcb_step_left}")
        if self.pcb_step_right and not self.pcb_step_right.exists():
            errors.append(f"Right PCB STEP file not found: {self.pcb_step_right}")
        if self.kicad_pcb and not self.kicad_pcb.exists():
            errors.append(f"KiCad PCB file not found: {self.kicad_pcb}")
        
        # Validate dimensions
        if self.wall_thickness < 1.5 or self.wall_thickness > 5.0:
            errors.append(f"wall_thickness must be between 1.5 and 5.0mm, got {self.wall_thickness}")
        if self.case_height < 5.0 or self.case_height > 20.0:
            errors.append(f"case_height must be between 5.0 and 20.0mm, got {self.case_height}")
        if self.plate_thickness < 1.0 or self.plate_thickness > 2.0:
            errors.append(f"plate_thickness must be between 1.0 and 2.0mm, got {self.plate_thickness}")
        if self.corner_radius < 0.5 or self.corner_radius > 5.0:
            errors.append(f"corner_radius must be between 0.5 and 5.0mm, got {self.corner_radius}")
        
        # Validate chamfers/fillets
        if self.enable_chamfers and self.enable_fillets:
            errors.append("Cannot enable both chamfers and fillets, choose one")
        if self.enable_chamfers:
            if self.outer_chamfer < 0.5 or self.outer_chamfer > 3.0:
                errors.append(f"outer_chamfer must be between 0.5 and 3.0mm, got {self.outer_chamfer}")
            if self.inner_chamfer < 0.5 or self.inner_chamfer > 2.0:
                errors.append(f"inner_chamfer must be between 0.5 and 2.0mm, got {self.inner_chamfer}")
        
        # Validate screw bosses
        if self.boss_diameter < 4.0 or self.boss_diameter > 8.0:
            errors.append(f"boss_diameter must be between 4.0 and 8.0mm, got {self.boss_diameter}")
        
        # Validate rubber feet
        if self.enable_rubber_feet:
            if self.feet_diameter < 8.0 or self.feet_diameter > 12.0:
                errors.append(f"feet_diameter must be between 8.0 and 12.0mm, got {self.feet_diameter}")
            if self.feet_depth < 1.0 or self.feet_depth > 3.0:
                errors.append(f"feet_depth must be between 1.0 and 3.0mm, got {self.feet_depth}")
        
        # Validate STL tolerance
        if self.stl_tolerance < 0.001 or self.stl_tolerance > 0.1:
            errors.append(f"stl_tolerance must be between 0.001 and 0.1mm, got {self.stl_tolerance}")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            k: str(v) if isinstance(v, Path) else v
            for k, v in self.__dict__.items()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CaseConfig":
        """Create config from dictionary."""
        # Convert string paths to Path objects
        if "pcb_step_left" in data and data["pcb_step_left"]:
            data["pcb_step_left"] = Path(data["pcb_step_left"])
        if "pcb_step_right" in data and data["pcb_step_right"]:
            data["pcb_step_right"] = Path(data["pcb_step_right"])
        if "kicad_pcb" in data and data["kicad_pcb"]:
            data["kicad_pcb"] = Path(data["kicad_pcb"])
        if "output_dir" in data:
            data["output_dir"] = Path(data["output_dir"])
        
        return cls(**data)


def load_config_file(path: Path) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def save_config_file(config: CaseConfig, path: Path) -> None:
    """Save configuration to JSON file."""
    with open(path, 'w') as f:
        json.dump(config.to_dict(), f, indent=2)
