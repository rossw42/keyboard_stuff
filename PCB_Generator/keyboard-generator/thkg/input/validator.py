"""Input validation for configurations"""

from typing import List, Tuple
from thkg.config import Configuration, Switch


class ValidationError(Exception):
    """Validation error exception"""
    pass


class InputValidator:
    """Validate configuration inputs"""
    
    def validate(self, config: Configuration) -> Tuple[bool, List[str]]:
        """Validate configuration
        
        Args:
            config: Configuration to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Validate keyboard name
        if not config.name or not config.name.strip():
            errors.append("Keyboard name is required")
        
        # Validate layout
        if not config.layout_preset and not config.kle_file and not config.switches:
            errors.append("Layout must be specified (preset, KLE file, or custom switches)")
        
        # Validate switches if provided
        if config.switches:
            switch_errors = self._validate_switches(config.switches)
            errors.extend(switch_errors)
        
        # Validate matrix if provided
        if config.matrix:
            matrix_errors = self._validate_matrix(config)
            errors.extend(matrix_errors)
        
        # Validate PCB dimensions
        if config.pcb.length <= 0 or config.pcb.width <= 0:
            errors.append("PCB dimensions must be positive")
        
        if config.pcb.thickness <= 0:
            errors.append("PCB thickness must be positive")
        
        # Validate plate if enabled
        if config.plate.enabled:
            if config.plate.thickness <= 0:
                errors.append("Plate thickness must be positive")
            
            if config.plate.switch_type not in ['mx', 'alps', 'choc']:
                errors.append(f"Invalid switch type: {config.plate.switch_type}. Must be 'mx', 'alps', or 'choc'")
        
        return (len(errors) == 0, errors)
    
    def _validate_switches(self, switches: List[Switch]) -> List[str]:
        """Validate switch configuration
        
        Args:
            switches: List of switches to validate
            
        Returns:
            List of error messages
        """
        errors = []
        
        if not switches:
            errors.append("At least one switch is required")
            return errors
        
        # Check for duplicate positions
        positions = set()
        for i, switch in enumerate(switches):
            pos = (switch.row, switch.col)
            if pos in positions:
                errors.append(f"Duplicate switch position at row {switch.row}, col {switch.col}")
            positions.add(pos)
            
            # Validate switch dimensions
            if switch.width <= 0 or switch.height <= 0:
                errors.append(f"Switch {i}: Invalid dimensions (width={switch.width}, height={switch.height})")
            
            # Validate rotation
            if not (-360 <= switch.rotation <= 360):
                errors.append(f"Switch {i}: Rotation must be between -360 and 360 degrees")
        
        return errors
    
    def _validate_matrix(self, config: Configuration) -> List[str]:
        """Validate matrix configuration
        
        Args:
            config: Configuration with matrix to validate
            
        Returns:
            List of error messages
        """
        errors = []
        matrix = config.matrix
        
        if matrix.rows <= 0 or matrix.cols <= 0:
            errors.append("Matrix rows and columns must be positive")
        
        if matrix.diode_direction not in ['COL2ROW', 'ROW2COL']:
            errors.append(f"Invalid diode direction: {matrix.diode_direction}. Must be 'COL2ROW' or 'ROW2COL'")
        
        # Validate pin assignments if provided
        if matrix.row_pins:
            if len(matrix.row_pins) != matrix.rows:
                errors.append(f"Number of row pins ({len(matrix.row_pins)}) doesn't match rows ({matrix.rows})")
            
            # Check for duplicate pins
            if len(set(matrix.row_pins)) != len(matrix.row_pins):
                errors.append("Duplicate row pins detected")
        
        if matrix.col_pins:
            if len(matrix.col_pins) != matrix.cols:
                errors.append(f"Number of column pins ({len(matrix.col_pins)}) doesn't match columns ({matrix.cols})")
            
            # Check for duplicate pins
            if len(set(matrix.col_pins)) != len(matrix.col_pins):
                errors.append("Duplicate column pins detected")
        
        # Check for pin conflicts between rows and cols
        if matrix.row_pins and matrix.col_pins:
            row_set = set(matrix.row_pins)
            col_set = set(matrix.col_pins)
            conflicts = row_set & col_set
            if conflicts:
                errors.append(f"Pin conflicts between rows and columns: {conflicts}")
        
        return errors
    
    def validate_or_raise(self, config: Configuration):
        """Validate configuration and raise exception if invalid
        
        Args:
            config: Configuration to validate
            
        Raises:
            ValidationError: If configuration is invalid
        """
        is_valid, errors = self.validate(config)
        if not is_valid:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ValidationError(error_msg)
