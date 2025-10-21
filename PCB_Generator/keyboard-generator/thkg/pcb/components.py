"""Component library with part numbers and specifications

Provides standardized component definitions for BOM generation
and PCB design. All components are through-hole unless noted.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ComponentSpec:
    """Component specification with sourcing information"""
    category: str  # e.g., "Resistor", "Capacitor", "IC"
    value: str  # e.g., "5.1kΩ", "100nF", "ATmega328P"
    package: str  # e.g., "0805", "DIP-28", "SOT-23-6"
    footprint: str  # KiCad footprint library reference
    description: str
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None
    datasheet: Optional[str] = None
    vendors: Optional[List[dict]] = None  # [{"name": "Mouser", "sku": "123-456"}]
    notes: Optional[str] = None


class ComponentLibrary:
    """Standard component library for keyboard PCBs"""
    
    # Resistors (Through-Hole)
    RESISTORS = {
        "5.1k": ComponentSpec(
            category="Resistor",
            value="5.1kΩ",
            package="Axial",
            footprint="R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
            description="5.1kΩ resistor for USB-C CC configuration",
            manufacturer="Yageo",
            part_number="CFR-25JB-52-5K1",
            vendors=[
                {"name": "Mouser", "sku": "603-CFR-25JB-52-5K1"},
                {"name": "Digikey", "sku": "5.1KQBK-ND"}
            ],
            notes="1/4W, 5% tolerance"
        ),
        "10k": ComponentSpec(
            category="Resistor",
            value="10kΩ",
            package="Axial",
            footprint="R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
            description="10kΩ resistor for RESET pull-up",
            manufacturer="Yageo",
            part_number="CFR-25JB-52-10K",
            vendors=[
                {"name": "Mouser", "sku": "603-CFR-25JB-52-10K"},
                {"name": "Digikey", "sku": "10KQBK-ND"}
            ],
            notes="1/4W, 5% tolerance"
        ),
        "1.5k": ComponentSpec(
            category="Resistor",
            value="1.5kΩ",
            package="Axial",
            footprint="R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
            description="1.5kΩ resistor for USB D+ pull-up",
            manufacturer="Yageo",
            part_number="CFR-25JB-52-1K5",
            vendors=[
                {"name": "Mouser", "sku": "603-CFR-25JB-52-1K5"},
                {"name": "Digikey", "sku": "1.5KQBK-ND"}
            ],
            notes="1/4W, 5% tolerance, optional for ATmega32A"
        ),
    }
    
    # Capacitors (Through-Hole Ceramic)
    CAPACITORS = {
        "100nF": ComponentSpec(
            category="Capacitor",
            value="100nF",
            package="Disc",
            footprint="C_Disc_D3.0mm_W1.6mm_P2.50mm",
            description="100nF ceramic capacitor for decoupling",
            manufacturer="Kemet",
            part_number="C315C104M5U5TA",
            vendors=[
                {"name": "Mouser", "sku": "80-C315C104M5U"},
                {"name": "Digikey", "sku": "399-4151-ND"}
            ],
            notes="50V, X7R, ±20%, 2.5mm pitch"
        ),
        "22pF": ComponentSpec(
            category="Capacitor",
            value="22pF",
            package="Disc",
            footprint="C_Disc_D3.0mm_W1.6mm_P2.50mm",
            description="22pF ceramic capacitor for crystal load",
            manufacturer="Kemet",
            part_number="C315C220J2G5TA",
            vendors=[
                {"name": "Mouser", "sku": "80-C315C220J2G"},
                {"name": "Digikey", "sku": "399-4924-ND"}
            ],
            notes="50V, C0G/NP0, ±5%, 2.5mm pitch"
        ),
    }
    
    # Diodes
    DIODES = {
        "1N4148": ComponentSpec(
            category="Diode",
            value="1N4148",
            package="DO-35",
            footprint="D_DO-35_SOD27_P7.62mm_Horizontal",
            description="1N4148 switching diode for matrix",
            manufacturer="Vishay",
            part_number="1N4148-TAP",
            datasheet="https://www.vishay.com/docs/81857/1n4148.pdf",
            vendors=[
                {"name": "Mouser", "sku": "78-1N4148-TAP"},
                {"name": "Digikey", "sku": "1N4148TAPCT-ND"}
            ],
            notes="100V, 200mA, fast switching, through-hole"
        ),
    }
    
    # ICs (SMD - for USB protection)
    ICS_SMD = {
        "USBLC6-2SC6": ComponentSpec(
            category="IC",
            value="USBLC6-2SC6",
            package="SOT-23-6",
            footprint="SOT-23-6",
            description="ESD protection IC for USB",
            manufacturer="STMicroelectronics",
            part_number="USBLC6-2SC6",
            datasheet="https://www.st.com/resource/en/datasheet/usblc6-2.pdf",
            vendors=[
                {"name": "Mouser", "sku": "511-USBLC6-2SC6"},
                {"name": "Digikey", "sku": "497-5235-1-ND"}
            ],
            notes="Dual ESD protection, 17V clamp, SOT-23-6"
        ),
    }
    
    # Microcontrollers (Through-Hole DIP)
    MCUS = {
        "ATmega328P": ComponentSpec(
            category="MCU",
            value="ATmega328P-PU",
            package="DIP-28",
            footprint="DIP-28_W7.62mm",
            description="ATmega328P microcontroller (DIP package)",
            manufacturer="Microchip",
            part_number="ATMEGA328P-PU",
            datasheet="https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega328P-Datasheet.pdf",
            vendors=[
                {"name": "Mouser", "sku": "556-ATMEGA328P-PU"},
                {"name": "Digikey", "sku": "ATMEGA328P-PU-ND"}
            ],
            notes="8-bit AVR, 32KB Flash, 20MHz, DIP-28"
        ),
        "ATmega32A": ComponentSpec(
            category="MCU",
            value="ATmega32A-PU",
            package="DIP-40",
            footprint="DIP-40_W15.24mm",
            description="ATmega32A microcontroller (DIP package)",
            manufacturer="Microchip",
            part_number="ATMEGA32A-PU",
            datasheet="https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega32A-Datasheet.pdf",
            vendors=[
                {"name": "Mouser", "sku": "556-ATMEGA32A-PU"},
                {"name": "Digikey", "sku": "ATMEGA32A-PU-ND"}
            ],
            notes="8-bit AVR, 32KB Flash, 16MHz, DIP-40, USB capable"
        ),
    }
    
    # Crystals (Through-Hole)
    CRYSTALS = {
        "16MHz": ComponentSpec(
            category="Crystal",
            value="16MHz",
            package="HC-49S",
            footprint="Crystal_HC49-U_Vertical",
            description="16MHz crystal oscillator",
            manufacturer="ECS",
            part_number="ECS-160-20-4X",
            vendors=[
                {"name": "Mouser", "sku": "520-160-20-4X"},
                {"name": "Digikey", "sku": "X1103-ND"}
            ],
            notes="16MHz, 20pF load, HC-49S package"
        ),
    }
    
    # Ferrite Beads (SMD)
    FERRITE_BEADS = {
        "600R@100MHz": ComponentSpec(
            category="Ferrite Bead",
            value="600Ω@100MHz",
            package="0805",
            footprint="L_0805_2012Metric",
            description="Ferrite bead for USB noise filtering",
            manufacturer="Murata",
            part_number="BLM21PG601SN1D",
            vendors=[
                {"name": "Mouser", "sku": "81-BLM21PG601SN1D"},
                {"name": "Digikey", "sku": "490-1037-1-ND"}
            ],
            notes="600Ω@100MHz, 2A, 0805"
        ),
    }
    
    # Polyfuses (SMD)
    POLYFUSES = {
        "500mA": ComponentSpec(
            category="Polyfuse",
            value="500mA",
            package="1206",
            footprint="Fuse_1206_3216Metric",
            description="Resettable polyfuse for USB overcurrent protection",
            manufacturer="Bourns",
            part_number="MF-MSMF050-2",
            vendors=[
                {"name": "Mouser", "sku": "652-MF-MSMF050-2"},
                {"name": "Digikey", "sku": "MF-MSMF050-2CT-ND"}
            ],
            notes="500mA hold, 1A trip, 6V, 1206"
        ),
    }
    
    # Connectors (Through-Hole)
    CONNECTORS = {
        "USB-C-THT": ComponentSpec(
            category="Connector",
            value="USB-C Receptacle",
            package="Through-Hole",
            footprint="USB_C_Receptacle_HRO_TYPE-C-31-M-12",
            description="USB-C receptacle (through-hole)",
            manufacturer="HRO",
            part_number="TYPE-C-31-M-12",
            vendors=[
                {"name": "LCSC", "sku": "C165948"},
                {"name": "AliExpress", "sku": "Search: USB-C THT"}
            ],
            notes="Through-hole USB-C, 16-pin"
        ),
        "ISP-Header": ComponentSpec(
            category="Connector",
            value="2x3 Pin Header",
            package="2.54mm",
            footprint="PinHeader_2x03_P2.54mm_Vertical",
            description="ISP programming header",
            manufacturer="Generic",
            part_number="2x3 2.54mm Header",
            vendors=[
                {"name": "Mouser", "sku": "649-68002-206HLF"},
                {"name": "Digikey", "sku": "S9015E-03-ND"}
            ],
            notes="2x3 pin header, 2.54mm pitch"
        ),
    }
    
    # Switches (Through-Hole)
    SWITCHES = {
        "MX": ComponentSpec(
            category="Switch",
            value="Cherry MX",
            package="PCB Mount",
            footprint="MX_PCB_1.00u",
            description="Cherry MX compatible switch",
            manufacturer="Cherry/Gateron/Kailh",
            part_number="Various",
            vendors=[
                {"name": "NovelKeys", "sku": "Various"},
                {"name": "KBDfans", "sku": "Various"}
            ],
            notes="PCB mount, 5-pin, various colors/types"
        ),
    }
    
    @classmethod
    def get_component(cls, category: str, value: str) -> Optional[ComponentSpec]:
        """Get component specification by category and value
        
        Args:
            category: Component category (e.g., "Resistor", "Capacitor")
            value: Component value (e.g., "5.1k", "100nF")
            
        Returns:
            ComponentSpec if found, None otherwise
        """
        category_map = {
            "Resistor": cls.RESISTORS,
            "Capacitor": cls.CAPACITORS,
            "Diode": cls.DIODES,
            "IC": cls.ICS_SMD,
            "MCU": cls.MCUS,
            "Crystal": cls.CRYSTALS,
            "Ferrite Bead": cls.FERRITE_BEADS,
            "Polyfuse": cls.POLYFUSES,
            "Connector": cls.CONNECTORS,
            "Switch": cls.SWITCHES,
        }
        
        library = category_map.get(category, {})
        return library.get(value)
    
    @classmethod
    def generate_bom(cls, components: List[dict]) -> List[dict]:
        """Generate BOM with quantities and sourcing info
        
        Args:
            components: List of component dicts with 'category' and 'value'
            
        Returns:
            List of BOM entries with quantities and sourcing
        """
        bom = {}
        
        for comp in components:
            category = comp.get('category')
            value = comp.get('value')
            key = f"{category}_{value}"
            
            if key in bom:
                bom[key]['quantity'] += 1
            else:
                spec = cls.get_component(category, value)
                if spec:
                    bom[key] = {
                        'category': spec.category,
                        'value': spec.value,
                        'package': spec.package,
                        'description': spec.description,
                        'manufacturer': spec.manufacturer,
                        'part_number': spec.part_number,
                        'quantity': 1,
                        'vendors': spec.vendors,
                        'notes': spec.notes,
                    }
        
        return list(bom.values())
