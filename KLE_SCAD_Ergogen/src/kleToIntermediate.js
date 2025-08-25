/**
 * KLE to Intermediate Format Converter
 * Inspired by hotswap_pcb_generator's approach for accurate KLE conversion
 */

const kle = require("@ijprest/kle-serial");

/**
 * Convert KLE data to an intermediate format suitable for various outputs
 * This approach is based on hotswap_pcb_generator's successful conversion method
 * @param {Object} keyboard - Parsed KLE keyboard object
 * @returns {Object} Intermediate format with enhanced key data
 */
function convertToIntermediate(keyboard) {
    // Process each key with proper formatting
    const formattedKeys = keyboard.keys.map((key, index) => {
        // Calculate side borders for wide keys (like in hotswap_pcb_generator)
        const sideBorder = (key.width - 1) / 2;
        
        // Create the intermediate key format
        const intermediateKey = {
            // Unique identifier
            id: `key_${index}`,
            
            // Position data (in keyboard units)
            position: {
                x: key.x,
                y: key.y,
                x_units: key.x,  // Store original units
                y_units: key.y
            },
            
            // Key dimensions
            dimensions: {
                width: key.width || 1,
                height: key.height || 1,
                width_mm: (key.width || 1) * 19.05,  // Convert to mm (1u = 19.05mm)
                height_mm: (key.height || 1) * 19.05
            },
            
            // Rotation data (note: KLE uses negative rotation)
            rotation: {
                angle: key.rotation_angle || 0,
                centerX: key.rotation_x || 0,
                centerY: key.rotation_y || 0,
                // Store the negative angle as used in SCAD
                scadAngle: -(key.rotation_angle || 0)
            },
            
            // Border calculations (for SCAD compatibility)
            borders: {
                top: 1,
                bottom: 1,
                left: sideBorder ? `1+${sideBorder}*unit*mm` : 1,
                right: sideBorder ? `1+${sideBorder}*unit*mm` : 1,
                // Numeric versions for calculations
                left_numeric: 1 + sideBorder,
                right_numeric: 1 + sideBorder
            },
            
            // Stabilizer information
            stabilizer: {
                needed: key.width >= 2 || key.height >= 2,
                size: key.width >= 2 ? key.width : (key.height >= 2 ? key.height : 0),
                type: getStabilizerType(key.width, key.height),
                spacing: getStabilizerSpacing(key.width, key.height)
            },
            
            // Labels and metadata
            labels: key.labels || [],
            primaryLabel: key.labels ? key.labels[0] : '',
            color: key.color || '#cccccc',
            
            // Matrix position (to be calculated later)
            matrix: {
                row: null,
                col: null
            },
            
            // Store original KLE data for reference
            _kleData: key,
            
            // SCAD-compatible format (like hotswap_pcb_generator)
            scadFormat: [
                [
                    [key.x, key.y],
                    key.width || 1,
                    [-(key.rotation_angle || 0), key.rotation_x || 0, key.rotation_y || 0]
                ],
                [
                    1,
                    1,
                    sideBorder ? `1+${sideBorder}*unit*mm` : 1,
                    sideBorder ? `1+${sideBorder}*unit*mm` : 1
                ],
                false  // extra_data
            ]
        };
        
        return intermediateKey;
    });
    
    // Calculate matrix positions
    assignMatrixPositions(formattedKeys);
    
    // Group keys by various criteria for easier processing
    const keyGroups = {
        byRow: groupKeysByRow(formattedKeys),
        byColumn: groupKeysByColumn(formattedKeys),
        stabilized: formattedKeys.filter(k => k.stabilizer.needed),
        regular: formattedKeys.filter(k => !k.stabilizer.needed)
    };
    
    return {
        keys: formattedKeys,
        groups: keyGroups,
        stats: {
            totalKeys: formattedKeys.length,
            stabilizedKeys: keyGroups.stabilized.length,
            uniqueWidths: [...new Set(formattedKeys.map(k => k.dimensions.width))],
            uniqueHeights: [...new Set(formattedKeys.map(k => k.dimensions.height))],
            hasRotation: formattedKeys.some(k => k.rotation.angle !== 0)
        },
        bounds: calculatePreciseBounds(formattedKeys)
    };
}

/**
 * Determine stabilizer type based on key dimensions
 * @param {number} width - Key width in units
 * @param {number} height - Key height in units
 * @returns {string} Stabilizer type identifier
 */
function getStabilizerType(width, height) {
    if (width >= 6.25) return 'spacebar_6_25u';
    if (width >= 6) return 'spacebar_6u';
    if (width >= 3) return `stab_${width.toString().replace('.', '_')}u`;
    if (width >= 2) return `stab_${width.toString().replace('.', '_')}u`;
    if (height >= 2) return `stab_vertical_${height}u`;
    return null;
}

/**
 * Get stabilizer spacing based on key size
 * @param {number} width - Key width in units
 * @param {number} height - Key height in units
 * @returns {Object} Stabilizer spacing information
 */
function getStabilizerSpacing(width, height) {
    // Standard Cherry stabilizer spacings
    const spacings = {
        2: 23.8,     // 2u stabilizer
        2.25: 23.8,  // 2.25u stabilizer
        2.5: 23.8,   // 2.5u stabilizer
        2.75: 23.8,  // 2.75u stabilizer
        3: 38.1,     // 3u stabilizer
        6: 76.2,     // 6u stabilizer
        6.25: 100,   // 6.25u stabilizer
        6.5: 114.3,  // 6.5u stabilizer
        7: 133.35    // 7u stabilizer
    };
    
    if (width >= 2) {
        return {
            type: 'horizontal',
            spacing: spacings[width] || 23.8,
            leftOffset: 0,
            rightOffset: 0
        };
    }
    
    if (height >= 2) {
        return {
            type: 'vertical',
            spacing: 23.8,  // Vertical stabilizers typically use 2u spacing
            topOffset: 0,
            bottomOffset: 0
        };
    }
    
    return null;
}

/**
 * Assign matrix positions to keys
 * @param {Array} keys - Array of intermediate format keys
 */
function assignMatrixPositions(keys) {
    // Sort keys by Y then X position
    const sortedKeys = [...keys].sort((a, b) => {
        if (Math.abs(a.position.y - b.position.y) < 0.1) {
            return a.position.x - b.position.x;
        }
        return a.position.y - b.position.y;
    });
    
    // Group into rows
    const rows = [];
    let currentRow = [];
    let lastY = sortedKeys[0]?.position.y;
    
    sortedKeys.forEach(key => {
        if (Math.abs(key.position.y - lastY) > 0.1) {
            if (currentRow.length > 0) {
                rows.push(currentRow);
            }
            currentRow = [key];
            lastY = key.position.y;
        } else {
            currentRow.push(key);
        }
    });
    
    if (currentRow.length > 0) {
        rows.push(currentRow);
    }
    
    // Assign matrix positions
    rows.forEach((row, rowIndex) => {
        row.forEach((key, colIndex) => {
            key.matrix.row = rowIndex;
            key.matrix.col = colIndex;
        });
    });
}

/**
 * Group keys by physical rows
 * @param {Array} keys - Array of keys
 * @returns {Object} Keys grouped by row
 */
function groupKeysByRow(keys) {
    const rows = {};
    const tolerance = 0.25; // Quarter unit tolerance for row detection
    
    keys.forEach(key => {
        // Find or create row
        let rowFound = false;
        for (const [rowKey, rowKeys] of Object.entries(rows)) {
            const rowY = parseFloat(rowKey);
            if (Math.abs(key.position.y - rowY) < tolerance) {
                rowKeys.push(key);
                rowFound = true;
                break;
            }
        }
        
        if (!rowFound) {
            rows[key.position.y.toString()] = [key];
        }
    });
    
    // Sort keys within each row by X position
    Object.values(rows).forEach(rowKeys => {
        rowKeys.sort((a, b) => a.position.x - b.position.x);
    });
    
    return rows;
}

/**
 * Group keys by physical columns
 * @param {Array} keys - Array of keys
 * @returns {Object} Keys grouped by column
 */
function groupKeysByColumn(keys) {
    const columns = {};
    const tolerance = 0.25; // Quarter unit tolerance for column detection
    
    keys.forEach(key => {
        // Find or create column
        let colFound = false;
        for (const [colKey, colKeys] of Object.entries(columns)) {
            const colX = parseFloat(colKey);
            if (Math.abs(key.position.x - colX) < tolerance) {
                colKeys.push(key);
                colFound = true;
                break;
            }
        }
        
        if (!colFound) {
            columns[key.position.x.toString()] = [key];
        }
    });
    
    // Sort keys within each column by Y position
    Object.values(columns).forEach(colKeys => {
        colKeys.sort((a, b) => a.position.y - b.position.y);
    });
    
    return columns;
}

/**
 * Calculate precise bounds accounting for key rotation
 * @param {Array} keys - Array of keys
 * @returns {Object} Precise boundary information
 */
function calculatePreciseBounds(keys) {
    if (!keys || keys.length === 0) {
        return { minX: 0, maxX: 0, minY: 0, maxY: 0, width: 0, height: 0 };
    }
    
    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;
    
    keys.forEach(key => {
        // Get all corners of the key accounting for rotation
        const corners = getRotatedKeyCorners(key);
        
        corners.forEach(corner => {
            minX = Math.min(minX, corner.x);
            maxX = Math.max(maxX, corner.x);
            minY = Math.min(minY, corner.y);
            maxY = Math.max(maxY, corner.y);
        });
    });
    
    return {
        minX,
        maxX,
        minY,
        maxY,
        width: maxX - minX,
        height: maxY - minY,
        width_mm: (maxX - minX) * 19.05,
        height_mm: (maxY - minY) * 19.05
    };
}

/**
 * Get the four corners of a key accounting for rotation
 * @param {Object} key - Key in intermediate format
 * @returns {Array} Array of corner coordinates
 */
function getRotatedKeyCorners(key) {
    const corners = [
        { x: 0, y: 0 },
        { x: key.dimensions.width, y: 0 },
        { x: key.dimensions.width, y: key.dimensions.height },
        { x: 0, y: key.dimensions.height }
    ];
    
    // Apply rotation if present
    if (key.rotation.angle !== 0) {
        const angleRad = (key.rotation.angle * Math.PI) / 180;
        const cos = Math.cos(angleRad);
        const sin = Math.sin(angleRad);
        
        return corners.map(corner => {
            // Translate to rotation center
            const dx = corner.x - key.rotation.centerX;
            const dy = corner.y - key.rotation.centerY;
            
            // Apply rotation
            const rotatedX = dx * cos - dy * sin;
            const rotatedY = dx * sin + dy * cos;
            
            // Translate back and add key position
            return {
                x: rotatedX + key.rotation.centerX + key.position.x,
                y: rotatedY + key.rotation.centerY + key.position.y
            };
        });
    }
    
    // No rotation, just add key position
    return corners.map(corner => ({
        x: corner.x + key.position.x,
        y: corner.y + key.position.y
    }));
}

module.exports = {
    convertToIntermediate,
    getStabilizerType,
    getStabilizerSpacing,
    assignMatrixPositions,
    groupKeysByRow,
    groupKeysByColumn,
    calculatePreciseBounds,
    getRotatedKeyCorners
};