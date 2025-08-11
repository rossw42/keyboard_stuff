const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

/**
 * Connection Diagram Generator for Ergogen Configurations
 * Automatically generates keyboard connection diagrams from ergogen YAML files
 */
class ConnectionDiagramGenerator {
    constructor() {
        this.config = null;
        this.parsedData = {
            meta: {},
            layout: {
                zones: {},
                components: {}
            },
            electrical: {
                columns: {},
                rows: {},
                pins: {}
            },
            physical: {
                dimensions: {},
                components: []
            }
        };
    }

    /**
     * Generate connection diagram from ergogen YAML file
     */
    async generateFromFile(yamlFilePath, outputDir) {
        try {
            // Read and parse YAML file
            const yamlContent = fs.readFileSync(yamlFilePath, 'utf8');
            this.config = yaml.load(yamlContent);
            
            // Parse the configuration
            this.parseConfiguration();
            
            // Generate the markdown diagram
            const diagram = this.generateMarkdownDiagram();
            
            // Write to output file
            const outputPath = path.join(outputDir, 'keyboard_connection_diagram.md');
            fs.writeFileSync(outputPath, diagram, 'utf8');
            
            return {
                success: true,
                outputPath: outputPath,
                diagram: diagram
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Parse ergogen configuration into structured data
     */
    parseConfiguration() {
        // Parse meta information
        this.parsedData.meta = this.config.meta || {};
        
        // Parse units/dimensions
        this.parsedData.physical.dimensions = this.config.units || {};
        
        // Parse points/zones for layout
        if (this.config.points && this.config.points.zones) {
            this.parseZones(this.config.points.zones);
        }
        
        // Parse PCB footprints for electrical connections
        if (this.config.pcbs) {
            this.parsePCBFootprints(this.config.pcbs);
        }
    }

    /**
     * Parse zones from points section
     */
    parseZones(zones) {
        for (const [zoneName, zoneConfig] of Object.entries(zones)) {
            const zone = {
                name: zoneName,
                keys: [],
                components: [],
                layout: zoneConfig
            };

            // Parse columns and rows
            if (zoneConfig.columns) {
                for (const [colName, colConfig] of Object.entries(zoneConfig.columns)) {
                    if (colConfig.rows) {
                        for (const [rowName, rowConfig] of Object.entries(colConfig.rows)) {
                            const key = {
                                id: `${zoneName}_${colName}_${rowName}`,
                                zone: zoneName,
                                column: colName,
                                row: rowName,
                                tags: rowConfig.tags || [],
                                width: rowConfig.width || colConfig.key?.width || zoneConfig.key?.width || 'capx',
                                height: rowConfig.height || colConfig.key?.height || zoneConfig.key?.height || 'capy',
                                columnNet: colConfig.key?.column_net || rowConfig.column_net,
                                rowNet: rowConfig.row_net || (zoneConfig.rows && zoneConfig.rows[rowName] && zoneConfig.rows[rowName].row_net)
                            };
                            zone.keys.push(key);
                        }
                    }
                }
            }

            // Handle single-key zones (like encoders, OLED)
            if (zoneConfig.key && !zoneConfig.columns) {
                const key = {
                    id: zoneName,
                    zone: zoneName,
                    tags: zoneConfig.key.tags || [],
                    width: zoneConfig.key.width || 'capx',
                    height: zoneConfig.key.height || 'capy',
                    columnNet: zoneConfig.key.column_net,
                    rowNet: zoneConfig.key.row_net
                };
                zone.keys.push(key);
            }

            this.parsedData.layout.zones[zoneName] = zone;
        }
    }

    /**
     * Parse PCB footprints for electrical connections
     */
    parsePCBFootprints(pcbs) {
        for (const [pcbName, pcbConfig] of Object.entries(pcbs)) {
            if (pcbConfig.footprints && pcbConfig.footprints.controller) {
                this.parseControllerPins(pcbConfig.footprints.controller.params);
            }
            
            if (pcbConfig.footprints) {
                this.parseFootprintComponents(pcbConfig.footprints);
            }
        }
    }

    /**
     * Parse controller pin assignments
     */
    parseControllerPins(params) {
        for (const [pin, net] of Object.entries(params)) {
            if (pin.startsWith('P') && !isNaN(pin.substring(1))) {
                this.parsedData.electrical.pins[pin] = net;
                
                // Categorize as column or row
                if (net.startsWith('col')) {
                    this.parsedData.electrical.columns[net] = pin;
                } else if (net.startsWith('row')) {
                    this.parsedData.electrical.rows[net] = pin;
                }
            }
        }
    }

    /**
     * Parse footprint components for additional details
     */
    parseFootprintComponents(footprints) {
        for (const [name, footprint] of Object.entries(footprints)) {
            if (footprint.what && footprint.where) {
                const component = {
                    name: name,
                    type: footprint.what,
                    where: footprint.where,
                    params: footprint.params || {}
                };
                this.parsedData.physical.components.push(component);
            }
        }
    }

    /**
     * Generate markdown connection diagram
     */
    generateMarkdownDiagram() {
        const projectName = this.parsedData.meta.name || 'Keyboard';
        
        let markdown = `# ${this.capitalizeWords(projectName)} Connection Diagram\n\n`;
        markdown += `Analysis of the ${this.parsedData.meta.name || 'keyboard'} ergogen configuration file showing physical layout and electrical connections.\n\n`;

        // Physical Layout Diagram
        markdown += this.generatePhysicalLayoutDiagram();
        
        // Electrical Connection Matrix
        markdown += this.generateElectricalConnectionMatrix();
        
        // Special Connections
        markdown += this.generateSpecialConnections();
        
        // Matrix Scanning Logic
        markdown += this.generateMatrixScanningLogic();
        
        // Key Layout Details
        markdown += this.generateKeyLayoutDetails();
        
        // Physical Dimensions
        markdown += this.generatePhysicalDimensions();

        return markdown;
    }

    /**
     * Generate ASCII physical layout diagram
     */
    generatePhysicalLayoutDiagram() {
        let section = '## Physical Layout Diagram\n\n```\n';
        section += this.generateASCIILayout();
        section += '```\n\n';
        return section;
    }

    /**
     * Generate ASCII layout representation
     */
    generateASCIILayout() {
        // This is a simplified ASCII generator - for complex layouts, this would need
        // more sophisticated positioning logic based on anchor points and shifts
        const zones = this.parsedData.layout.zones;
        
        let layout = '┌─────────────────────────────────────────────────────────────────────────────────────┐\n';
        layout += `│                                ${this.parsedData.meta.name?.toUpperCase() || 'KEYBOARD'}                                      │\n`;
        layout += '├──────────────┬────────────────────────────────────────────┬─────────────────────────┤\n';

        // Generate layout sections based on detected zones
        const hasNav = zones.nav;
        const hasNumpad = zones.numpad;
        const hasEncoders = Object.keys(zones).some(z => z.includes('encoder'));
        const hasOLED = zones.oled_screen;

        if (hasNav) {
            layout += '│   NAV        │';
        } else {
            layout += '│              │';
        }

        if (hasNumpad) {
            layout += '             NUMPAD GRID                │';
        } else {
            layout += '             MAIN LAYOUT                │';
        }

        if (hasEncoders || hasOLED) {
            layout += '    RIGHT SECTION        │\n';
        } else {
            layout += '                         │\n';
        }

        layout += '│  COLUMN      │                                            │                         │\n';
        
        // Add more layout details based on parsed zones
        layout += this.generateZoneLayout(zones);
        
        layout += '└──────────────┴────────────────────────────────────────────┴─────────────────────────┘\n';
        
        return layout;
    }

    /**
     * Generate zone-specific layout
     */
    generateZoneLayout(zones) {
        let layout = '';
        
        // Add rows for different components
        const maxRows = Math.max(...Object.values(zones).map(zone => zone.keys.length));
        
        for (let i = 0; i < Math.min(maxRows, 8); i++) {
            layout += '│              │                                            │                         │\n';
        }
        
        // Add MCU section if present
        if (zones.mcu || this.parsedData.physical.components.some(c => c.type === 'promicro')) {
            layout += '│              │          ┌───────────────────┐             │                         │\n';
            layout += '│              │          │   PRO MICRO       │             │                         │\n';
            layout += '│              │          │      (MCU)        │             │                         │\n';
            layout += '│              │          │   18mm x 33mm     │             │                         │\n';
            layout += '│              │          └───────────────────┘             │                         │\n';
        }
        
        return layout;
    }

    /**
     * Generate electrical connection matrix tables
     */
    generateElectricalConnectionMatrix() {
        let section = '## Electrical Connection Matrix\n\n';
        
        // Column Networks
        section += '### Column Networks:\n';
        section += '| Column | Pro Micro Pin | Connected Keys |\n';
        section += '|--------|---------------|----------------|\n';
        
        for (const [colNet, pin] of Object.entries(this.parsedData.electrical.columns)) {
            const connectedKeys = this.getKeysForColumn(colNet);
            section += `| ${colNet} | ${pin} | ${connectedKeys.join(', ')} |\n`;
        }
        
        section += '\n### Row Networks:\n';
        section += '| Row | Pro Micro Pin | Connected Keys |\n';
        section += '|-----|---------------|----------------|\n';
        
        for (const [rowNet, pin] of Object.entries(this.parsedData.electrical.rows)) {
            const connectedKeys = this.getKeysForRow(rowNet);
            section += `| ${rowNet} | ${pin} | ${connectedKeys.join(', ')} |\n`;
        }
        
        section += '\n';
        return section;
    }

    /**
     * Get keys connected to a specific column
     */
    getKeysForColumn(columnNet) {
        const keys = [];
        for (const zone of Object.values(this.parsedData.layout.zones)) {
            for (const key of zone.keys) {
                if (key.columnNet === columnNet) {
                    keys.push(this.getKeyName(key));
                }
            }
        }
        return keys;
    }

    /**
     * Get keys connected to a specific row
     */
    getKeysForRow(rowNet) {
        const keys = [];
        for (const zone of Object.values(this.parsedData.layout.zones)) {
            for (const key of zone.keys) {
                if (key.rowNet === rowNet) {
                    keys.push(this.getKeyName(key));
                }
            }
        }
        return keys;
    }

    /**
     * Get human-readable key name
     */
    getKeyName(key) {
        // Map common key patterns to readable names
        const keyMappings = {
            'numpad_col0_row0': 'NumLock',
            'numpad_col0_row1': '7',
            'numpad_col0_row2': '4',
            'numpad_col0_row3': '1',
            'numpad_col0_row4': '0',
            'numpad_col1_row0': '/',
            'numpad_col1_row1': '8',
            'numpad_col1_row2': '5',
            'numpad_col1_row3': '2',
            'numpad_col2_row0': '*',
            'numpad_col2_row1': '9',
            'numpad_col2_row2': '6',
            'numpad_col2_row3': '3',
            'numpad_col2_row4': '.',
            'numpad_col3_row0': '-',
            'numpad_col3_row1': '+',
            'numpad_col3_row3': 'Enter'
        };
        
        return keyMappings[key.id] || key.id.replace(/_/g, ' ');
    }

    /**
     * Generate special connections section
     */
    generateSpecialConnections() {
        let section = '## Special Connections\n\n';
        
        // Encoders
        const encoders = this.parsedData.physical.components.filter(c => c.type === 'rotary');
        if (encoders.length > 0) {
            section += '### Encoders (Rotary + Switch functionality):\n';
            section += '| Component | Column Pin | Row Pin | Rotary A Pin | Rotary B Pin | Common |\n';
            section += '|-----------|------------|---------|--------------|--------------|--------|\n';
            
            for (const encoder of encoders) {
                const colPin = this.parsedData.electrical.columns[encoder.params.from] || 'N/A';
                const rowPin = this.parsedData.electrical.rows[encoder.params.to] || 'N/A';
                section += `| ${this.capitalizeWords(encoder.name)} | ${colPin} | ${rowPin} | ${encoder.params.A || 'N/A'} | ${encoder.params.B || 'N/A'} | ${encoder.params.C || 'GND'} |\n`;
            }
            section += '\n';
        }
        
        // OLED Display
        const oled = this.parsedData.physical.components.find(c => c.type === 'oled');
        if (oled) {
            section += '### OLED Display (I2C):\n';
            section += '| Signal | Pro Micro Pin | Description |\n';
            section += '|--------|---------------|-------------|\n';
            section += `| SDA | ${oled.params.SDA || 'P3'} | I2C Data Line |\n`;
            section += `| SCL | ${oled.params.SCL || 'P2'} | I2C Clock Line |\n`;
            section += `| VCC | ${oled.params.VCC || 'VCC'} | Power (3.3V/5V) |\n`;
            section += `| GND | ${oled.params.GND || 'GND'} | Ground |\n\n`;
        }
        
        // Diode Configuration
        section += '### Diode Configuration:\n';
        section += '- Every key switch has an anti-ghosting diode\n';
        section += '- Diode direction: `{{colrow}}` → `{{row_net}}`\n';
        section += '- Prevents current backflow during matrix scanning\n\n';
        
        return section;
    }

    /**
     * Generate matrix scanning logic section
     */
    generateMatrixScanningLogic() {
        let section = '## Matrix Scanning Logic\n\n';
        
        const totalColumns = Object.keys(this.parsedData.electrical.columns).length;
        const totalRows = Object.keys(this.parsedData.electrical.rows).length;
        const totalKeys = Object.values(this.parsedData.layout.zones)
            .reduce((sum, zone) => sum + zone.keys.length, 0);
        
        section += 'The keyboard uses a **hybrid matrix approach**:\n\n';
        section += '### Matrix Section:\n';
        section += `- **Total matrix coverage**: ${totalColumns} columns × ${totalRows} rows\n`;
        section += '- Efficient use of pins for the bulk of the keys\n';
        section += '- Standard matrix scanning: drive columns sequentially, read all rows\n\n';
        
        section += '### Pin Usage Summary:\n';
        section += `- **Total pins used**: ${totalColumns + totalRows} (${totalColumns} columns + ${totalRows} rows)\n`;
        section += `- **Total components**: ${totalKeys} keys + encoders + displays\n`;
        section += '- **Matrix efficiency**: Optimized for Pro Micro\'s limited pin count\n';
        section += '- **N-key rollover**: Full NKRO capability with diode protection\n\n';
        
        return section;
    }

    /**
     * Generate key layout details section
     */
    generateKeyLayoutDetails() {
        let section = '## Key Layout Details\n\n';
        
        // Analyze key sizes from the configuration
        const specialSizes = new Set();
        const regularKeys = [];
        
        for (const zone of Object.values(this.parsedData.layout.zones)) {
            for (const key of zone.keys) {
                if (key.width !== 'capx' || key.height !== 'capy') {
                    specialSizes.add(`${this.getKeyName(key)}: ${key.width} × ${key.height}`);
                } else {
                    regularKeys.push(this.getKeyName(key));
                }
            }
        }
        
        if (regularKeys.length > 0) {
            section += '### Standard Keys (1U):\n';
            section += `- ${regularKeys.join(', ')}\n\n`;
        }
        
        if (specialSizes.size > 0) {
            section += '### Special Size Keys:\n';
            for (const size of specialSizes) {
                section += `- **${size}**\n`;
            }
            section += '\n';
        }
        
        // Additional components
        const hasEncoders = this.parsedData.physical.components.some(c => c.type === 'rotary');
        const hasOLED = this.parsedData.physical.components.some(c => c.type === 'oled');
        const hasMCU = this.parsedData.physical.components.some(c => c.type === 'promicro');
        
        if (hasEncoders || hasOLED || hasMCU) {
            section += '### Additional Components:\n';
            if (hasEncoders) {
                const encoderCount = this.parsedData.physical.components.filter(c => c.type === 'rotary').length;
                section += `- **${encoderCount} Rotary Encoder${encoderCount > 1 ? 's' : ''}**: Each with push-button switch functionality\n`;
            }
            if (hasOLED) {
                section += '- **OLED Screen**: Display for status and information\n';
            }
            if (hasMCU) {
                section += '- **Pro Micro MCU**: Microcontroller for optimal trace routing\n';
            }
            section += '\n';
        }
        
        return section;
    }

    /**
     * Generate physical dimensions section
     */
    generatePhysicalDimensions() {
        let section = '## Physical Dimensions\n\n';
        
        const units = this.parsedData.physical.dimensions;
        
        if (units.kx || units.ky) {
            section += '### Key Spacing:\n';
            if (units.kx) section += `- **kx**: ${units.kx}mm (center-to-center horizontal)\n`;
            if (units.ky) section += `- **ky**: ${units.ky}mm (center-to-center vertical)\n`;
            if (units.capx && units.capy) {
                section += `- **Key cap size**: ${units.capx}×${units.capy}mm\n`;
            }
            section += '\n';
        }
        
        // Component distances
        const hasDistances = Object.keys(units).some(key => key.includes('_to_'));
        if (hasDistances) {
            section += '### Component Distances:\n';
            for (const [key, value] of Object.entries(units)) {
                if (key.includes('_to_')) {
                    const readable = key.replace(/_/g, ' ').replace(/to/g, 'to');
                    section += `- **${this.capitalizeWords(readable)}**: ${value}\n`;
                }
            }
            section += '\n';
        }
        
        section += `This design provides a compact, efficient ${this.parsedData.meta.name || 'keyboard'} with `;
        section += `${Object.keys(this.parsedData.electrical.columns).length} columns and `;
        section += `${Object.keys(this.parsedData.electrical.rows).length} rows, `;
        section += 'while maintaining compatibility with standard MX switches and keycaps.\n\n';
        
        return section;
    }

    /**
     * Utility function to capitalize words
     */
    capitalizeWords(str) {
        return str.replace(/\b\w/g, l => l.toUpperCase());
    }
}

module.exports = ConnectionDiagramGenerator;
