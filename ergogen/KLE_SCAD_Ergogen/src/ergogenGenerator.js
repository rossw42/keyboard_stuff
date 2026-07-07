const yaml = require('js-yaml');
const fs = require('fs').promises;

/**
 * Generate Ergogen YAML configuration from intermediate format data
 * @param {Object} intermediateData - Data in intermediate format from kleToIntermediate
 * @param {Object} options - Generation options
 * @returns {string} Ergogen YAML configuration
 */
function generateErgogenYAML(intermediateData, options = {}) {
    const {
        switchType = 'mx',  // mx, choc, choc_v2
        includeOutlines = true,
        includePCB = false,  // Disabled for now
        includeCase = false,
        keySpacing = 19,  // Center-to-center spacing in mm
        diodeDirection = 'row',  // row or column
        microcontroller = 'promicro',
        useSplitKeyboard = false,
        metadata = {}
    } = options;
    
    // Build the Ergogen configuration object
    const config = {
        meta: {
            engine: 'v4',
            name: metadata.name || 'KLE Import',
            version: '1.0',
            author: metadata.author || 'KLE to Ergogen Converter',
            url: ''
        },
        
        // Units configuration
        units: {
            // Key spacing
            kx: keySpacing,
            ky: keySpacing,
            
            // Padding around keys
            px: 2,
            py: 2,
            
            // Key dimensions
            keycap: 18,
            switch: 14
        },
        
        // Points (key positions)
        points: generatePoints(intermediateData, options),
        
        // Outlines for case and plate
        outlines: includeOutlines ? generateOutlines(intermediateData, options) : {},
        
        // PCB configuration
        pcbs: includePCB ? generatePCB(intermediateData, options) : {},
        
        // Case configuration (optional)
        cases: includeCase ? generateCase(intermediateData, options) : {}
    };
    
    // Convert to YAML
    return yaml.dump(config, {
        indent: 2,
        lineWidth: 120,
        noRefs: true
    });
}

/**
 * Generate points section for Ergogen
 * @param {Object} intermediateData - Data in intermediate format
 * @param {Object} options - Generation options
 * @returns {Object} Points configuration
 */
function generatePoints(intermediateData, options = {}) {
    const points = {
        zones: {},
        key: {
            padding: 'ky',
            spread: 'kx'
        }
    };
    
    // Use the pre-grouped keys from intermediate format
    const zones = {
        matrix: intermediateData.keys
    };
    
    Object.entries(zones).forEach(([zoneName, keys]) => {
        const zone = {
            key: {},
            columns: {}
        };
        
        // Group keys by columns within each zone
        const columns = groupKeysIntoColumns(keys);
        
        Object.entries(columns).forEach(([colName, colKeys]) => {
            const column = {
                key: {},
                rows: {}
            };
            
            // Sort keys by Y position (top to bottom)
            colKeys.sort((a, b) => b.position.y - a.position.y);
            
            colKeys.forEach((key, index) => {
                const rowName = key.primaryLabel || `${colName}_${index}`;
                const row = {};
                
                // Add position using the intermediate format
                if (key.position.x_units !== undefined || key.position.y_units !== undefined) {
                    row.shift = [key.position.x_units * 19.05, key.position.y_units * 19.05];
                }
                
                // Add rotation if present
                if (key.rotation && key.rotation.angle !== 0) {
                    row.rotate = key.rotation.angle;
                }
                
                // Add key-specific metadata
                if (key.dimensions.width > 1 || key.dimensions.height > 1) {
                    row.width = key.dimensions.width;
                    row.height = key.dimensions.height;
                }
                
                column.rows[rowName] = row;
            });
            
            zone.columns[colName] = column;
        });
        
        points.zones[zoneName] = zone;
    });
    
    return points;
}

/**
 * Group keys into logical zones
 * @param {Array} keys - Array of transformed keys
 * @returns {Object} Keys grouped by zones
 */
function groupKeysIntoZones(keys) {
    // For now, simple single zone
    // Could be enhanced to detect split keyboards, thumb clusters, etc.
    const zones = {
        matrix: []
    };
    
    keys.forEach(key => {
        // Simple zone detection based on position
        // Could check for gaps, clusters, etc.
        zones.matrix.push(key);
    });
    
    return zones;
}

/**
 * Group keys into columns
 * @param {Array} keys - Array of keys in a zone
 * @returns {Object} Keys grouped by columns
 */
function groupKeysIntoColumns(keys) {
    const columns = {};
    const tolerance = 0.5; // Use unit-based tolerance (half a key unit)
    
    // First, get unique X positions (columns)
    const xPositions = [];
    keys.forEach(key => {
        const x = key.position.x_units;
        let found = false;
        for (let i = 0; i < xPositions.length; i++) {
            if (Math.abs(xPositions[i] - x) < tolerance) {
                found = true;
                break;
            }
        }
        if (!found) {
            xPositions.push(x);
        }
    });
    
    // Sort X positions from left to right
    xPositions.sort((a, b) => a - b);
    
    // Create columns based on X positions
    xPositions.forEach((xPos, index) => {
        const colName = `col${index}`;
        columns[colName] = [];
        
        // Add keys that belong to this column
        keys.forEach(key => {
            if (Math.abs(key.position.x_units - xPos) < tolerance) {
                columns[colName].push(key);
            }
        });
    });
    
    // Sort keys within each column by Y position
    Object.values(columns).forEach(colKeys => {
        colKeys.sort((a, b) => a.position.y_units - b.position.y_units);
    });
    
    return columns;
}

/**
 * Generate outlines section for Ergogen
 * @param {Object} intermediateData - Data in intermediate format
 * @param {Object} options - Generation options
 * @returns {Object} Outlines configuration
 */
function generateOutlines(intermediateData, options = {}) {
    return {
        plate: [
            {
                what: 'rectangle',
                where: true,
                size: [14, 14],
                fillet: 0.5
            }
        ],
        
        pcb: [
            {
                what: 'rectangle',
                where: true,
                size: [18, 18],
                fillet: 2,
                expand: 5
            }
        ]
    };
}

/**
 * Generate PCB section for Ergogen
 * @param {Object} intermediateData - Data in intermediate format
 * @param {Object} options - Generation options
 * @returns {Object} PCB configuration
 */
function generatePCB(intermediateData, options = {}) {
    const {
        switchType = 'mx',
        diodeDirection = 'row',
        microcontroller = 'promicro',
        hotswap = true
    } = options;
    
    return {
        main: {
            outlines: {
                main: {
                    outline: 'pcb'
                }
            },
            
            footprints: {
                // Switch footprints
                switches: {
                    what: switchType,
                    where: true,
                    params: {
                        hotswap: hotswap,
                        reverse: false,
                        keycaps: true,
                        from: '{{column_net}}',
                        to: '{{row_net}}'
                    }
                },
                
                // Diode footprints
                diodes: {
                    what: 'diode',
                    where: true,
                    params: {
                        from: '{{row_net}}',
                        to: '{{column_net}}'
                    },
                    adjust: {
                        shift: [0, -5]
                    }
                },
                
                // Microcontroller
                mcu: {
                    what: microcontroller,
                    where: {
                        ref: 'matrix',
                        shift: [0, -30]
                    },
                    params: {
                        orientation: 'down'
                    }
                }
            }
        }
    };
}

/**
 * Generate case section for Ergogen
 * @param {Object} intermediateData - Data in intermediate format
 * @param {Object} options - Generation options
 * @returns {Object} Case configuration
 */
function generateCase(intermediateData, options = {}) {
    return {
        bottom: {
            what: 'outline',
            name: 'pcb',
            extrude: 5,
            expand: 2,
            fillet: 3
        },
        
        plate: {
            what: 'outline',
            name: 'plate',
            extrude: 1.5
        }
    };
}

/**
 * Save Ergogen YAML to file
 * @param {string} yamlContent - YAML content to save
 * @param {string} outputPath - Output file path
 */
async function saveYAML(yamlContent, outputPath) {
    try {
        await fs.writeFile(outputPath, yamlContent, 'utf-8');
        console.log(`Ergogen configuration saved to ${outputPath}`);
    } catch (error) {
        throw new Error(`Failed to save YAML file: ${error.message}`);
    }
}

/**
 * Advanced matrix generation for complex layouts
 * @param {Array} keys - Array of transformed keys
 * @returns {Object} Matrix wiring configuration
 */
function generateMatrixWiring(keys) {
    // Analyze key layout to determine optimal matrix
    const matrix = {
        rows: [],
        cols: []
    };
    
    // Group keys by physical rows
    const rowGroups = {};
    keys.forEach(key => {
        const rowKey = Math.round(key.position.y_units * 10) / 10; // Round to nearest 0.1 unit
        if (!rowGroups[rowKey]) {
            rowGroups[rowKey] = [];
        }
        rowGroups[rowKey].push(key);
    });
    
    // Assign matrix positions
    let rowIndex = 0;
    Object.values(rowGroups).forEach(rowKeys => {
        rowKeys.sort((a, b) => a.position.x_units - b.position.x_units);
        rowKeys.forEach((key, colIndex) => {
            key.matrix = {
                row: rowIndex,
                col: colIndex
            };
        });
        rowIndex++;
    });
    
    return matrix;
}

module.exports = {
    generateErgogenYAML,
    generatePoints,
    generateOutlines,
    generatePCB,
    generateCase,
    generateMatrixWiring,
    saveYAML
};