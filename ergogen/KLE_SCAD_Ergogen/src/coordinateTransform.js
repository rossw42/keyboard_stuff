/**
 * Coordinate transformation utilities for KLE to Ergogen conversion
 * KLE uses keyboard units (1u = 19.05mm) with origin at top-left
 * Ergogen uses mm with origin typically at center
 */

// Standard keyboard unit size in mm
const KEYBOARD_UNIT_MM = 19.05;

// Key spacing in Ergogen (center-to-center distance)
const KEY_SPACING = 19;  // Slightly less than 1u for tighter spacing

/**
 * Transform KLE coordinates to Ergogen coordinates
 * @param {Array} keys - Array of key objects from KLE parser
 * @param {Object} options - Transformation options
 * @returns {Array} Transformed key data for Ergogen
 */
function transformCoordinates(keys, options = {}) {
    const {
        unitSize = KEYBOARD_UNIT_MM,
        centerLayout = true,
        flipY = true,  // KLE has Y+ going down, Ergogen typically has Y+ going up
        spacing = KEY_SPACING
    } = options;
    
    // First pass: convert to mm
    let transformedKeys = keys.map(key => {
        return {
            ...key,
            // Convert KLE units to mm
            x_mm: key.x * unitSize,
            y_mm: key.y * unitSize,
            width_mm: key.width * unitSize,
            height_mm: key.height * unitSize,
            
            // Keep original units for reference
            x_units: key.x,
            y_units: key.y
        };
    });
    
    // Calculate center of layout if needed
    if (centerLayout) {
        const bounds = calculateBoundsMM(transformedKeys);
        const centerX = (bounds.minX + bounds.maxX) / 2;
        const centerY = (bounds.minY + bounds.maxY) / 2;
        
        transformedKeys = transformedKeys.map(key => ({
            ...key,
            x_mm: key.x_mm - centerX,
            y_mm: key.y_mm - centerY
        }));
    }
    
    // Flip Y axis if needed (KLE vs Ergogen convention)
    if (flipY) {
        transformedKeys = transformedKeys.map(key => ({
            ...key,
            y_mm: -key.y_mm
        }));
    }
    
    // Apply spacing adjustments
    transformedKeys = transformedKeys.map(key => ({
        ...key,
        // Use center-to-center spacing - keep in mm
        ergogen_x: Math.round(key.x_mm / spacing) * spacing,
        ergogen_y: Math.round(key.y_mm / spacing) * spacing
    }));
    
    return transformedKeys;
}

/**
 * Calculate bounds in mm
 * @param {Array} keys - Array of transformed keys with mm coordinates
 * @returns {Object} Bounds in mm
 */
function calculateBoundsMM(keys) {
    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;
    
    keys.forEach(key => {
        const halfWidth = key.width_mm / 2;
        const halfHeight = key.height_mm / 2;
        
        // For now, ignore rotation for bounds calculation
        // Can be enhanced later if needed
        minX = Math.min(minX, key.x_mm - halfWidth);
        maxX = Math.max(maxX, key.x_mm + halfWidth);
        minY = Math.min(minY, key.y_mm - halfHeight);
        maxY = Math.max(maxY, key.y_mm + halfHeight);
    });
    
    return { minX, maxX, minY, maxY };
}

/**
 * Generate Ergogen point configuration for a key
 * @param {Object} key - Transformed key object
 * @param {number} index - Key index
 * @returns {Object} Ergogen point configuration
 */
function generateErgogenPoint(key, index) {
    const point = {
        // Generate unique key name
        key: key.label || `k${index}`,
        
        // Position in Ergogen coordinates
        x: key.ergogen_x || key.x_mm,
        y: key.ergogen_y || key.y_mm,
        
        // Rotation if present
        r: key.rotation.angle || 0,
        
        // Additional metadata
        meta: {
            width: key.width,
            height: key.height,
            stabilized: key.isStabilized
        }
    };
    
    // Add rotation center if not at key center
    if (key.rotation.centerX || key.rotation.centerY) {
        point.rx = key.rotation.centerX;
        point.ry = key.rotation.centerY;
    }
    
    return point;
}

/**
 * Group keys into rows and columns for matrix wiring
 * @param {Array} keys - Array of transformed keys
 * @param {Object} options - Grouping options
 * @returns {Object} Keys grouped by rows and columns
 */
function generateMatrix(keys, options = {}) {
    const {
        rowTolerance = 10,  // mm tolerance for row detection (increased for better row grouping)
        colTolerance = 10   // mm tolerance for column detection (increased for better column grouping)
    } = options;
    
    // Sort keys by Y then X
    const sortedKeys = [...keys].sort((a, b) => {
        if (Math.abs(a.y_mm - b.y_mm) < rowTolerance) {
            return a.x_mm - b.x_mm;
        }
        return a.y_mm - b.y_mm;
    });
    
    // Group into rows
    const rows = [];
    let currentRow = [];
    let currentY = null;
    
    sortedKeys.forEach(key => {
        if (currentY === null || Math.abs(key.y_mm - currentY) < rowTolerance) {
            currentRow.push(key);
            if (currentY === null) currentY = key.y_mm;
        } else {
            rows.push(currentRow);
            currentRow = [key];
            currentY = key.y_mm;
        }
    });
    
    if (currentRow.length > 0) {
        rows.push(currentRow);
    }
    
    // Assign row and column indices
    rows.forEach((row, rowIndex) => {
        row.forEach((key, colIndex) => {
            key.matrix = {
                row: rowIndex,
                col: colIndex
            };
        });
    });
    
    return {
        rows,
        matrix: {
            rows: rows.length,
            cols: Math.max(...rows.map(r => r.length))
        }
    };
}

/**
 * Convert KLE rotation to Ergogen rotation format
 * @param {Object} rotation - KLE rotation object
 * @returns {number} Rotation angle in degrees for Ergogen
 */
function convertRotation(rotation) {
    // KLE rotation is already in degrees
    // Ergogen also uses degrees, but might need sign flip
    return -(rotation.angle || 0);  // Negative for correct direction
}

/**
 * Calculate key spacing for Ergogen columns/rows
 * @param {Array} keys - Array of keys
 * @returns {Object} Suggested column and row spacing
 */
function calculateSpacing(keys) {
    const xPositions = [...new Set(keys.map(k => k.x))].sort((a, b) => a - b);
    const yPositions = [...new Set(keys.map(k => k.y))].sort((a, b) => a - b);
    
    // Calculate minimum spacing
    let minXSpacing = Infinity;
    for (let i = 1; i < xPositions.length; i++) {
        const spacing = xPositions[i] - xPositions[i - 1];
        if (spacing > 0) minXSpacing = Math.min(minXSpacing, spacing);
    }
    
    let minYSpacing = Infinity;
    for (let i = 1; i < yPositions.length; i++) {
        const spacing = yPositions[i] - yPositions[i - 1];
        if (spacing > 0) minYSpacing = Math.min(minYSpacing, spacing);
    }
    
    return {
        columnSpacing: minXSpacing === Infinity ? 1 : minXSpacing,
        rowSpacing: minYSpacing === Infinity ? 1 : minYSpacing,
        suggestedSpacing: KEY_SPACING
    };
}

module.exports = {
    KEYBOARD_UNIT_MM,
    KEY_SPACING,
    transformCoordinates,
    calculateBoundsMM,
    generateErgogenPoint,
    generateMatrix,
    convertRotation,
    calculateSpacing
};