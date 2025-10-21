"""Pin assignment for MCU with proper peripheral reservations"""

from typing import List, Dict
from thkg.config import Matrix, MCUType


class PinAssigner:
    """Assign MCU pins to matrix rows and columns
    
    Follows best practices from ai03's PCB Design Guide:
    - Reserves crystal oscillator pins (XTAL1/XTAL2)
    - Reserves ISP programming pins (MISO/MOSI/SCK)
    - Reserves USB pins (D+/D-)
    - Prioritizes pins by capability (digital, PWM, ADC)
    """
    
    # Pin definitions for different MCUs with capabilities
    MCU_PINS = {
        MCUType.ATMEGA328P: {
            'digital': ['D4', 'D5', 'D6', 'D7',  # Available digital pins
                       'B0', 'B1', 'B2',          # Available port B pins
                       'C0', 'C1', 'C2', 'C3', 'C4', 'C5'],  # Port C (also ADC)
            'analog': ['C0', 'C1', 'C2', 'C3', 'C4', 'C5'],  # ADC pins (A0-A5)
            'pwm': ['D5', 'D6', 'B1', 'B2'],  # PWM capable pins
        },
        MCUType.ATMEGA32A: {
            'digital': ['D4', 'D5', 'D6', 'D7',  # Available digital pins
                       'B0', 'B1', 'B2',          # Available port B pins
                       'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',  # Port C
                       'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'],  # Port A
            'analog': ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'],  # ADC pins
            'pwm': ['D4', 'D5', 'D7', 'B3'],  # PWM capable pins
        },
        MCUType.PRO_MICRO: {
            'digital': ['D4', 'D7',  # Available digital pins
                       'B1', 'B2', 'B6',  # Available port B pins
                       'C6', 'E6',  # Port C and E
                       'F4', 'F5', 'F6', 'F7'],  # Port F
            'analog': ['F4', 'F5', 'F6', 'F7'],  # ADC pins
            'pwm': ['B1', 'B2', 'C6'],  # PWM capable pins
        },
    }
    
    # Reserved pins with detailed explanations
    RESERVED_PINS = {
        MCUType.ATMEGA328P: {
            'D0': 'UART RX (USB communication)',
            'D1': 'UART TX (USB communication)',
            'D2': 'INT0 (reserved for future use)',
            'D3': 'INT1 (reserved for future use)',
            'B3': 'MOSI (ISP programming)',
            'B4': 'MISO (ISP programming)',
            'B5': 'SCK (ISP programming)',
            'B6': 'XTAL1 (16MHz crystal)',
            'B7': 'XTAL2 (16MHz crystal)',
        },
        MCUType.ATMEGA32A: {
            'D0': 'RXD (UART)',
            'D1': 'TXD (UART)',
            'D2': 'USB D+ (INT0)',
            'D3': 'USB D- (INT1)',
            'B3': 'MOSI (ISP programming)',
            'B4': 'MISO (ISP programming)',
            'B5': 'SCK (ISP programming)',
            'B6': 'XTAL1 (16MHz crystal)',
            'B7': 'XTAL2 (16MHz crystal)',
        },
        MCUType.PRO_MICRO: {
            'D0': 'RX (UART)',
            'D1': 'TX (UART)',
            'D2': 'USB D+ (INT0)',
            'D3': 'USB D- (INT1)',
            'B3': 'MISO (ISP programming)',
            'B4': 'MOSI (ISP programming)',
            'B5': 'SCK (ISP programming)',
        },
    }
    
    def assign_pins(self, matrix: Matrix, mcu_type: MCUType) -> Matrix:
        """Assign MCU pins to matrix rows and columns
        
        Args:
            matrix: Matrix configuration
            mcu_type: MCU type
            
        Returns:
            Matrix with pin assignments
            
        Raises:
            ValueError: If not enough pins available
        """
        # Get available pins
        available_pins = self._get_available_pins(mcu_type)
        
        # Check if we have enough pins
        total_needed = matrix.rows + matrix.cols
        if len(available_pins) < total_needed:
            raise ValueError(
                f"Not enough pins for matrix. Need {total_needed}, "
                f"have {len(available_pins)} available"
            )
        
        # Assign pins
        matrix.row_pins = available_pins[:matrix.rows]
        matrix.col_pins = available_pins[matrix.rows:matrix.rows + matrix.cols]
        
        return matrix
    
    def _get_available_pins(self, mcu_type: MCUType) -> List[str]:
        """Get list of available pins for MCU
        
        Args:
            mcu_type: MCU type
            
        Returns:
            List of available pin names (prioritized: digital > PWM > analog)
        """
        pins = self.MCU_PINS.get(mcu_type, {})
        reserved = self.RESERVED_PINS.get(mcu_type, {})
        
        # Get digital pins (already filtered in MCU_PINS definition)
        available = pins.get('digital', [])
        
        # Remove any reserved pins (double-check)
        available = [p for p in available if p not in reserved]
        
        return available
    
    def validate_pins(self, matrix: Matrix, mcu_type: MCUType) -> List[str]:
        """Validate pin assignments
        
        Args:
            matrix: Matrix with pin assignments
            mcu_type: MCU type
            
        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        
        # Get available pins
        available = self._get_available_pins(mcu_type)
        available_set = set(available)
        
        # Check row pins
        for pin in matrix.row_pins:
            if pin not in available_set:
                errors.append(f"Row pin {pin} not available on {mcu_type.value}")
        
        # Check column pins
        for pin in matrix.col_pins:
            if pin not in available_set:
                errors.append(f"Column pin {pin} not available on {mcu_type.value}")
        
        # Check for duplicates
        all_pins = matrix.row_pins + matrix.col_pins
        if len(all_pins) != len(set(all_pins)):
            errors.append("Duplicate pins in matrix assignment")
        
        return errors
    
    def get_pin_info(self, mcu_type: MCUType) -> Dict[str, any]:
        """Get information about MCU pins
        
        Args:
            mcu_type: MCU type
            
        Returns:
            Dictionary with pin information
        """
        pins = self.MCU_PINS.get(mcu_type, {})
        reserved = self.RESERVED_PINS.get(mcu_type, {})
        available = self._get_available_pins(mcu_type)
        
        return {
            'mcu': mcu_type.value,
            'total_pins': len(pins.get('digital', [])),
            'reserved_pins': reserved,
            'reserved_count': len(reserved),
            'available_pins': available,
            'available_count': len(available),
            'pwm_pins': pins.get('pwm', []),
            'analog_pins': pins.get('analog', [])
        }
