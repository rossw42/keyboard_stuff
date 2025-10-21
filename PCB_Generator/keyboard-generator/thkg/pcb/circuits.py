"""Circuit templates for PCB generation

Based on ai03's PCB Design Guide and industry best practices.
These templates provide proven circuit patterns for keyboard PCBs.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Component:
    """Component in a circuit"""
    reference: str  # e.g., "R1", "C1", "U1"
    value: str  # e.g., "5.1kΩ", "100nF", "USBLC6-2SC6"
    footprint: str  # KiCad footprint library reference
    description: str = ""
    
    
@dataclass
class Connection:
    """Connection between components"""
    from_ref: str  # Component reference
    from_pin: str  # Pin name/number
    to_ref: str  # Component reference
    to_pin: str  # Pin name/number
    net_name: str = ""  # Optional net name


@dataclass
class CircuitTemplate:
    """Circuit template with components and connections"""
    name: str
    description: str
    components: List[Component]
    connections: List[Connection]
    notes: List[str] = None


class CircuitTemplates:
    """Collection of proven circuit templates"""
    
    @staticmethod
    def usb_c_protection() -> CircuitTemplate:
        """USB-C protection circuit (ai03 standard)
        
        Includes:
        - CC resistors for USB-C configuration
        - ESD protection (USBLC6-2SC6)
        - Ferrite beads for noise filtering
        - Polyfuse for overcurrent protection
        - Decoupling capacitors
        
        Returns:
            CircuitTemplate for USB-C protection
        """
        components = [
            Component("J1", "USB-C-Receptacle", "USB_C_Receptacle_HRO_TYPE-C-31-M-12",
                     "USB-C connector (through-hole)"),
            Component("R1", "5.1kΩ", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
                     "CC1 configuration resistor"),
            Component("R2", "5.1kΩ", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
                     "CC2 configuration resistor"),
            Component("L1", "600Ω@100MHz", "L_0805_2012Metric",
                     "Ferrite bead for D+ line"),
            Component("L2", "600Ω@100MHz", "L_0805_2012Metric",
                     "Ferrite bead for D- line"),
            Component("D1", "USBLC6-2SC6", "SOT-23-6",
                     "ESD protection IC"),
            Component("F1", "500mA", "Fuse_1206_3216Metric",
                     "Polyfuse for overcurrent protection"),
            Component("C1", "100nF", "C_0805_2012Metric",
                     "Decoupling capacitor"),
            Component("C2", "100nF", "C_0805_2012Metric",
                     "Decoupling capacitor"),
        ]
        
        connections = [
            # CC resistors to ground
            Connection("J1", "CC1", "R1", "1", "CC1"),
            Connection("R1", "2", "GND", "1", "GND"),
            Connection("J1", "CC2", "R2", "1", "CC2"),
            Connection("R2", "2", "GND", "1", "GND"),
            
            # VBUS through polyfuse
            Connection("J1", "VBUS", "F1", "1", "VBUS"),
            Connection("F1", "2", "VCC", "1", "VCC"),
            
            # D+ and D- through ferrite beads to ESD protection
            Connection("J1", "D+", "L1", "1", "USB_D+_RAW"),
            Connection("L1", "2", "D1", "1", "USB_D+"),
            Connection("J1", "D-", "L2", "1", "USB_D-_RAW"),
            Connection("L2", "2", "D1", "3", "USB_D-"),
            
            # ESD protection to MCU
            Connection("D1", "6", "MCU", "D+", "USB_D+"),
            Connection("D1", "2", "MCU", "D-", "USB_D-"),
            
            # ESD protection power
            Connection("D1", "4", "VCC", "1", "VCC"),
            Connection("D1", "5", "GND", "1", "GND"),
            
            # Decoupling capacitors
            Connection("C1", "1", "VCC", "1", "VCC"),
            Connection("C1", "2", "GND", "1", "GND"),
            Connection("C2", "1", "VCC", "1", "VCC"),
            Connection("C2", "2", "GND", "1", "GND"),
        ]
        
        notes = [
            "Place ESD protection IC close to USB connector",
            "Keep D+ and D- traces parallel and equal length",
            "Route D+ and D- as 90Ω differential pair",
            "Place decoupling caps close to ESD IC",
            "Connect shield to GND with short trace",
        ]
        
        return CircuitTemplate(
            name="USB-C Protection",
            description="Standard USB-C protection circuit with ESD, ferrite beads, and polyfuse",
            components=components,
            connections=connections,
            notes=notes
        )
    
    @staticmethod
    def atmega328p_support() -> CircuitTemplate:
        """ATmega328P supporting circuit
        
        Includes:
        - 16MHz crystal oscillator
        - Load capacitors (22pF)
        - Decoupling capacitors (100nF x4)
        - RESET pull-up resistor (10kΩ)
        - ISP header
        
        Returns:
            CircuitTemplate for ATmega328P support
        """
        components = [
            Component("U1", "ATmega328P-PU", "DIP-28_W7.62mm",
                     "ATmega328P microcontroller (DIP package)"),
            Component("X1", "16MHz", "Crystal_HC49-U_Vertical",
                     "16MHz crystal oscillator"),
            Component("C5", "22pF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Crystal load capacitor"),
            Component("C6", "22pF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Crystal load capacitor"),
            Component("C7", "100nF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Decoupling capacitor VCC1"),
            Component("C8", "100nF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Decoupling capacitor VCC2"),
            Component("C9", "100nF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Decoupling capacitor AVCC"),
            Component("C10", "100nF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Decoupling capacitor AREF"),
            Component("R3", "10kΩ", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
                     "RESET pull-up resistor"),
            Component("J2", "ISP-Header", "PinHeader_2x03_P2.54mm_Vertical",
                     "ISP programming header"),
        ]
        
        connections = [
            # Crystal oscillator
            Connection("U1", "PB6", "X1", "1", "XTAL1"),
            Connection("U1", "PB7", "X1", "2", "XTAL2"),
            Connection("X1", "1", "C5", "1", "XTAL1"),
            Connection("C5", "2", "GND", "1", "GND"),
            Connection("X1", "2", "C6", "1", "XTAL2"),
            Connection("C6", "2", "GND", "1", "GND"),
            
            # Decoupling capacitors
            Connection("U1", "VCC", "C7", "1", "VCC"),
            Connection("C7", "2", "GND", "1", "GND"),
            Connection("U1", "VCC", "C8", "1", "VCC"),
            Connection("C8", "2", "GND", "1", "GND"),
            Connection("U1", "AVCC", "C9", "1", "VCC"),
            Connection("C9", "2", "GND", "1", "GND"),
            Connection("U1", "AREF", "C10", "1", "AREF"),
            Connection("C10", "2", "GND", "1", "GND"),
            
            # RESET pull-up
            Connection("U1", "RESET", "R3", "1", "RESET"),
            Connection("R3", "2", "VCC", "1", "VCC"),
            
            # ISP header
            Connection("J2", "1", "U1", "PB4", "MISO"),
            Connection("J2", "2", "VCC", "1", "VCC"),
            Connection("J2", "3", "U1", "SCK", "SCK"),
            Connection("J2", "4", "U1", "PB3", "MOSI"),
            Connection("J2", "5", "U1", "RESET", "RESET"),
            Connection("J2", "6", "GND", "1", "GND"),
        ]
        
        notes = [
            "Place crystal within 10mm of MCU",
            "Keep crystal traces short and direct",
            "Place load capacitors close to crystal",
            "Place decoupling caps next to VCC pins",
            "Connect all GND pins to ground plane",
            "AREF can be connected to VCC through 100nF cap",
        ]
        
        return CircuitTemplate(
            name="ATmega328P Support",
            description="Supporting circuit for ATmega328P with crystal and decoupling",
            components=components,
            connections=connections,
            notes=notes
        )
    
    @staticmethod
    def atmega32a_support() -> CircuitTemplate:
        """ATmega32A supporting circuit
        
        Similar to ATmega328P but with different pinout.
        Includes USB D+/D- connections on PD2/PD3.
        
        Returns:
            CircuitTemplate for ATmega32A support
        """
        components = [
            Component("U1", "ATmega32A-PU", "DIP-40_W15.24mm",
                     "ATmega32A microcontroller (DIP package)"),
            Component("X1", "16MHz", "Crystal_HC49-U_Vertical",
                     "16MHz crystal oscillator"),
            Component("C5", "22pF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Crystal load capacitor"),
            Component("C6", "22pF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Crystal load capacitor"),
            Component("C7", "100nF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Decoupling capacitor VCC1"),
            Component("C8", "100nF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Decoupling capacitor VCC2"),
            Component("C9", "100nF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Decoupling capacitor AVCC"),
            Component("C10", "100nF", "C_Disc_D3.0mm_W1.6mm_P2.50mm",
                     "Decoupling capacitor AREF"),
            Component("R3", "10kΩ", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
                     "RESET pull-up resistor"),
            Component("R4", "1.5kΩ", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
                     "USB D+ pull-up resistor (optional)"),
            Component("J2", "ISP-Header", "PinHeader_2x03_P2.54mm_Vertical",
                     "ISP programming header"),
        ]
        
        connections = [
            # Crystal oscillator
            Connection("U1", "XTAL1", "X1", "1", "XTAL1"),
            Connection("U1", "XTAL2", "X1", "2", "XTAL2"),
            Connection("X1", "1", "C5", "1", "XTAL1"),
            Connection("C5", "2", "GND", "1", "GND"),
            Connection("X1", "2", "C6", "1", "XTAL2"),
            Connection("C6", "2", "GND", "1", "GND"),
            
            # Decoupling capacitors
            Connection("U1", "VCC", "C7", "1", "VCC"),
            Connection("C7", "2", "GND", "1", "GND"),
            Connection("U1", "VCC", "C8", "1", "VCC"),
            Connection("C8", "2", "GND", "1", "GND"),
            Connection("U1", "AVCC", "C9", "1", "VCC"),
            Connection("C9", "2", "GND", "1", "GND"),
            Connection("U1", "AREF", "C10", "1", "AREF"),
            Connection("C10", "2", "GND", "1", "GND"),
            
            # RESET pull-up
            Connection("U1", "RESET", "R3", "1", "RESET"),
            Connection("R3", "2", "VCC", "1", "VCC"),
            
            # USB connections
            Connection("USB", "D+", "U1", "PD2", "USB_D+"),
            Connection("USB", "D-", "U1", "PD3", "USB_D-"),
            
            # ISP header
            Connection("J2", "1", "U1", "PB6", "MISO"),
            Connection("J2", "2", "VCC", "1", "VCC"),
            Connection("J2", "3", "U1", "PB7", "SCK"),
            Connection("J2", "4", "U1", "PB5", "MOSI"),
            Connection("J2", "5", "U1", "RESET", "RESET"),
            Connection("J2", "6", "GND", "1", "GND"),
        ]
        
        notes = [
            "ATmega32A has native USB support on PD2/PD3",
            "Place crystal within 10mm of MCU",
            "USB D+ pull-up (R4) may be needed for USB enumeration",
            "Place decoupling caps next to VCC pins",
            "Connect all GND pins to ground plane",
        ]
        
        return CircuitTemplate(
            name="ATmega32A Support",
            description="Supporting circuit for ATmega32A with USB and crystal",
            components=components,
            connections=connections,
            notes=notes
        )
    
    @staticmethod
    def switch_matrix(rows: int, cols: int, diode_direction: str = "COL2ROW") -> CircuitTemplate:
        """Switch matrix circuit template
        
        Args:
            rows: Number of rows
            cols: Number of columns
            diode_direction: "COL2ROW" or "ROW2COL"
            
        Returns:
            CircuitTemplate for switch matrix
        """
        components = []
        connections = []
        
        # Generate switches and diodes
        switch_num = 1
        for row in range(rows):
            for col in range(cols):
                # Switch
                sw_ref = f"SW{switch_num}"
                components.append(
                    Component(sw_ref, "MX-Switch", "MX_PCB_1.00u",
                             f"Cherry MX switch at R{row}C{col}")
                )
                
                # Diode
                d_ref = f"D{switch_num}"
                components.append(
                    Component(d_ref, "1N4148", "D_DO-35_SOD27_P7.62mm_Horizontal",
                             f"Matrix diode for {sw_ref}")
                )
                
                # Connections depend on diode direction
                if diode_direction == "COL2ROW":
                    # Switch connects to column
                    connections.append(
                        Connection(sw_ref, "1", f"COL{col}", "1", f"COL{col}")
                    )
                    # Switch through diode to row
                    connections.append(
                        Connection(sw_ref, "2", d_ref, "A", f"SW{switch_num}_A")
                    )
                    connections.append(
                        Connection(d_ref, "K", f"ROW{row}", "1", f"ROW{row}")
                    )
                else:  # ROW2COL
                    # Switch connects to row
                    connections.append(
                        Connection(sw_ref, "1", f"ROW{row}", "1", f"ROW{row}")
                    )
                    # Switch through diode to column
                    connections.append(
                        Connection(sw_ref, "2", d_ref, "A", f"SW{switch_num}_A")
                    )
                    connections.append(
                        Connection(d_ref, "K", f"COL{col}", "1", f"COL{col}")
                    )
                
                switch_num += 1
        
        notes = [
            f"Matrix: {rows} rows × {cols} columns = {rows * cols} switches",
            f"Diode direction: {diode_direction}",
            "Each switch has a diode to prevent ghosting",
            "Diode cathode (K) marked with band",
            "Route matrix traces on bottom layer",
            "Keep row/column traces organized and parallel",
        ]
        
        return CircuitTemplate(
            name=f"Switch Matrix {rows}×{cols}",
            description=f"{rows}×{cols} switch matrix with {diode_direction} diodes",
            components=components,
            connections=connections,
            notes=notes
        )
