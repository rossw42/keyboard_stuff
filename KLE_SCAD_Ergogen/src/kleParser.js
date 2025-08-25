const kle = require("@ijprest/kle-serial");
const fs = require('fs').promises;

/**
 * Parse a KLE JSON file and extract keyboard layout data
 * @param {string} filePath - Path to the KLE JSON file
 * @returns {Object} Parsed keyboard data with keys and metadata
 */
async function parseKLE(filePath) {
    try {
        const kleJson = await fs.readFile(filePath, 'utf-8');
        const keyboard = kle.Serial.parse(kleJson);
        
        // Extract metadata
        const metadata = keyboard.meta || {};
        
        // Process each key
        const keys = keyboard.keys.map((key, index) => {
            return {
                id: `key_${index}`,
                // KLE uses keyboard units (1u = 19.05mm typically)
                x: key.x,           // X position in keyboard units
                y: key.y,           // Y position in keyboard units
                width: key.width || 1,    // Key width (default 1u)
                height: key.height || 1,   // Key height (default 1u)
                
                // Rotation data
                rotation: {
                    angle: key.rotation_angle || 0,
                    centerX: key.rotation_x || 0,
                    centerY: key.rotation_y || 0
                },
                
                // Additional properties
                label: key.labels ? key.labels[0] : '',  // Top label
                color: key.color || '#cccccc',
                
                // For special keys
                isStabilized: key.width >= 2 || key.height >= 2,
                
                // Store original KLE data for reference
                _kleData: key
            };
        });
        
        // Calculate keyboard bounds
        const bounds = calculateBounds(keys);
        
        return {
            metadata: {
                name: metadata.name || 'Unnamed Keyboard',
                author: metadata.author || '',
                notes: metadata.notes || '',
                background: metadata.backcolor || null,
                ...metadata
            },
            keys,
            bounds,
            stats: {
                totalKeys: keys.length,
                stabilizedKeys: keys.filter(k => k.isStabilized).length,
                maxWidth: Math.max(...keys.map(k => k.width)),
                maxHeight: Math.max(...keys.map(k => k.height))
            }
        };
        
    } catch (error) {
        throw new Error(`Failed to parse KLE file: ${error.message}`);
    }
}

/**
 * Calculate the bounding box of the keyboard layout
 * @param {Array} keys - Array of key objects
 * @returns {Object} Bounds with min/max x/y values
 */
function calculateBounds(keys) {
    if (!keys || keys.length === 0) {
        return { minX: 0, maxX: 0, minY: 0, maxY: 0, width: 0, height: 0 };
    }
    
    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;
    
    keys.forEach(key => {
        // Account for rotation when calculating bounds
        const corners = getKeyCorners(key);
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
        height: maxY - minY
    };
}

/**
 * Get the four corners of a key accounting for rotation
 * @param {Object} key - Key object with position and rotation
 * @returns {Array} Array of corner coordinates
 */
function getKeyCorners(key) {
    const corners = [
        { x: 0, y: 0 },
        { x: key.width, y: 0 },
        { x: key.width, y: key.height },
        { x: 0, y: key.height }
    ];
    
    // Apply rotation if present
    if (key.rotation && key.rotation.angle !== 0) {
        const angleRad = (key.rotation.angle * Math.PI) / 180;
        const cos = Math.cos(angleRad);
        const sin = Math.sin(angleRad);
        
        return corners.map(corner => {
            // Translate to rotation center
            const dx = corner.x - key.rotation.centerX;
            const dy = corner.y - key.rotation.centerY;
            
            // Rotate
            const rotatedX = dx * cos - dy * sin;
            const rotatedY = dx * sin + dy * cos;
            
            // Translate back and add key position
            return {
                x: rotatedX + key.rotation.centerX + key.x,
                y: rotatedY + key.rotation.centerY + key.y
            };
        });
    }
    
    // No rotation, just add key position
    return corners.map(corner => ({
        x: corner.x + key.x,
        y: corner.y + key.y
    }));
}

/**
 * Parse KLE data from a JSON string
 * @param {string} jsonString - KLE JSON string
 * @returns {Object} Parsed keyboard data
 */
function parseKLEString(jsonString) {
    try {
        const keyboard = kle.Serial.parse(jsonString);
        
        // Process similar to parseKLE but without file reading
        const metadata = keyboard.meta || {};
        const keys = keyboard.keys.map((key, index) => {
            return {
                id: `key_${index}`,
                x: key.x,
                y: key.y,
                width: key.width || 1,
                height: key.height || 1,
                rotation: {
                    angle: key.rotation_angle || 0,
                    centerX: key.rotation_x || 0,
                    centerY: key.rotation_y || 0
                },
                label: key.labels ? key.labels[0] : '',
                color: key.color || '#cccccc',
                isStabilized: key.width >= 2 || key.height >= 2,
                _kleData: key
            };
        });
        
        return {
            metadata,
            keys,
            bounds: calculateBounds(keys),
            stats: {
                totalKeys: keys.length,
                stabilizedKeys: keys.filter(k => k.isStabilized).length,
                maxWidth: Math.max(...keys.map(k => k.width)),
                maxHeight: Math.max(...keys.map(k => k.height))
            }
        };
        
    } catch (error) {
        throw new Error(`Failed to parse KLE string: ${error.message}`);
    }
}

module.exports = {
    parseKLE,
    parseKLEString,
    calculateBounds,
    getKeyCorners
};