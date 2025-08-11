/**
 * DXF Parser Module - Using gdsestimating/dxf-parser
 * Parses DXF file content and extracts entities
 */

const DxfParser = require('dxf-parser');

class ErgogenDxfParser {
    /**
     * Parse DXF content
     * @param {string} content - DXF file content
     * @returns {Object} Parsed DXF data with entities and bounds
     */
    static parse(content) {
        try {
            // Use the gdsestimating/dxf-parser library
            const parser = new DxfParser();
            const dxf = parser.parseSync(content);
            
            if (!dxf || !dxf.entities) {
                console.warn('No entities found in DXF file');
                return this.getEmptyResult();
            }
            
            // Convert entities to our expected format
            const entities = [];
            let bounds = {
                min_x: Infinity,
                min_y: Infinity,  
                max_x: -Infinity,
                max_y: -Infinity
            };
            
            // Process each entity
            for (const entity of dxf.entities) {
                const convertedEntity = this.convertEntity(entity);
                if (convertedEntity) {
                    entities.push(convertedEntity);
                    this.updateBoundsForEntity(bounds, convertedEntity);
                }
            }
            
            // Handle empty bounds
            if (bounds.min_x === Infinity) {
                bounds = { min_x: 0, min_y: 0, max_x: 100, max_y: 100 };
            }
            
            // Add padding to bounds
            const padding = Math.max(
                (bounds.max_x - bounds.min_x) * 0.05,
                (bounds.max_y - bounds.min_y) * 0.05,
                5
            );
            
            bounds.min_x -= padding;
            bounds.min_y -= padding;
            bounds.max_x += padding;
            bounds.max_y += padding;
            
            return {
                entities: entities,
                entity_count: entities.length,
                bounds: bounds,
                entity_types: this.getEntityTypeSummary(entities),
                layers: this.extractLayers(entities)
            };
            
        } catch (error) {
            console.error('Error parsing DXF:', error);
            return this.getEmptyResult();
        }
    }
    
    /**
     * Convert entity from dxf-parser format to our expected format
     * @param {Object} entity - Entity from dxf-parser
     * @returns {Object|null} Converted entity or null if not supported
     */
    static convertEntity(entity) {
        const layer = entity.layer || '0';
        const color = entity.color || 7;
        
        switch (entity.type) {
            case 'LINE':
                if (entity.vertices && entity.vertices.length >= 2) {
                    return {
                        type: 'line',
                        start: { x: entity.vertices[0].x, y: entity.vertices[0].y },
                        end: { x: entity.vertices[1].x, y: entity.vertices[1].y },
                        layer: layer,
                        color: color
                    };
                }
                break;
                
            case 'CIRCLE':
                if (entity.center && entity.radius !== undefined) {
                    return {
                        type: 'circle',
                        center: { x: entity.center.x, y: entity.center.y },
                        radius: entity.radius,
                        layer: layer,
                        color: color
                    };
                }
                break;
                
            case 'ARC':
                if (entity.center && entity.radius !== undefined && 
                    entity.startAngle !== undefined && entity.endAngle !== undefined) {
                    return {
                        type: 'arc',
                        center: { x: entity.center.x, y: entity.center.y },
                        radius: entity.radius,
                        start_angle: entity.startAngle,
                        end_angle: entity.endAngle,
                        layer: layer,
                        color: color
                    };
                }
                break;
                
            case 'LWPOLYLINE':
            case 'POLYLINE':
                if (entity.vertices && entity.vertices.length > 0) {
                    return {
                        type: 'polyline',
                        points: entity.vertices.map(v => ({ x: v.x, y: v.y })),
                        closed: entity.shape || false,
                        layer: layer,
                        color: color
                    };
                }
                break;
                
            case 'TEXT':
            case 'MTEXT':
                if (entity.startPoint && entity.text) {
                    return {
                        type: 'text',
                        position: { x: entity.startPoint.x, y: entity.startPoint.y },
                        text: entity.text,
                        height: entity.textHeight || 1,
                        rotation: entity.rotation || 0,
                        layer: layer,
                        color: color
                    };
                }
                break;
                
            case 'SPLINE':
                if (entity.controlPoints && entity.controlPoints.length > 0) {
                    return {
                        type: 'spline',
                        control_points: entity.controlPoints.map(p => ({ x: p.x, y: p.y })),
                        degree: entity.degree || 3,
                        layer: layer,
                        color: color
                    };
                }
                break;
                
            case 'ELLIPSE':
                if (entity.center && entity.majorAxisEndPoint) {
                    const majorAxis = Math.sqrt(
                        entity.majorAxisEndPoint.x * entity.majorAxisEndPoint.x + 
                        entity.majorAxisEndPoint.y * entity.majorAxisEndPoint.y
                    );
                    return {
                        type: 'ellipse',
                        center: { x: entity.center.x, y: entity.center.y },
                        major_axis: majorAxis,
                        minor_axis: majorAxis * (entity.axisRatio || 1),
                        rotation: Math.atan2(entity.majorAxisEndPoint.y, entity.majorAxisEndPoint.x) * 180 / Math.PI,
                        layer: layer,
                        color: color
                    };
                }
                break;
                
            case 'INSERT':
                // Handle block references - convert to a point for now
                if (entity.position) {
                    return {
                        type: 'insert',
                        position: { x: entity.position.x, y: entity.position.y },
                        name: entity.name || '',
                        layer: layer,
                        color: color
                    };
                }
                break;
        }
        
        return null;
    }
    
    /**
     * Update bounds for an entity
     * @param {Object} bounds - Bounds object to update
     * @param {Object} entity - Entity to include in bounds
     */
    static updateBoundsForEntity(bounds, entity) {
        switch (entity.type) {
            case 'line':
                this.updateBounds(bounds, entity.start);
                this.updateBounds(bounds, entity.end);
                break;
                
            case 'circle':
                this.updateBounds(bounds, {
                    x: entity.center.x - entity.radius,
                    y: entity.center.y - entity.radius
                });
                this.updateBounds(bounds, {
                    x: entity.center.x + entity.radius,
                    y: entity.center.y + entity.radius
                });
                break;
                
            case 'arc':
                // Add center and approximate bounds for the arc
                this.updateBounds(bounds, entity.center);
                this.updateBounds(bounds, {
                    x: entity.center.x - entity.radius,
                    y: entity.center.y - entity.radius
                });
                this.updateBounds(bounds, {
                    x: entity.center.x + entity.radius,
                    y: entity.center.y + entity.radius
                });
                break;
                
            case 'polyline':
                entity.points.forEach(point => {
                    this.updateBounds(bounds, point);
                });
                break;
                
            case 'text':
            case 'insert':
                this.updateBounds(bounds, entity.position);
                break;
                
            case 'spline':
                if (entity.control_points) {
                    entity.control_points.forEach(point => {
                        this.updateBounds(bounds, point);
                    });
                }
                break;
                
            case 'ellipse':
                // Approximate ellipse bounds
                this.updateBounds(bounds, {
                    x: entity.center.x - entity.major_axis,
                    y: entity.center.y - entity.major_axis
                });
                this.updateBounds(bounds, {
                    x: entity.center.x + entity.major_axis,
                    y: entity.center.y + entity.major_axis
                });
                break;
        }
    }
    
    /**
     * Update bounds with a point
     * @param {Object} bounds - Bounds object
     * @param {Object} point - Point with x, y coordinates
     */
    static updateBounds(bounds, point) {
        bounds.min_x = Math.min(bounds.min_x, point.x);
        bounds.min_y = Math.min(bounds.min_y, point.y);
        bounds.max_x = Math.max(bounds.max_x, point.x);
        bounds.max_y = Math.max(bounds.max_y, point.y);
    }
    
    /**
     * Get summary of entity types
     * @param {Array} entities - Array of entities
     * @returns {Object} Summary of entity types
     */
    static getEntityTypeSummary(entities) {
        const summary = {};
        for (const entity of entities) {
            summary[entity.type] = (summary[entity.type] || 0) + 1;
        }
        return summary;
    }
    
    /**
     * Extract layer names from entities
     * @param {Array} entities - Array of entities
     * @returns {Array} Sorted array of layer names
     */
    static extractLayers(entities) {
        const layers = new Set();
        for (const entity of entities) {
            if (entity.layer) {
                layers.add(entity.layer);
            }
        }
        return Array.from(layers).sort();
    }
    
    /**
     * Get empty result structure
     * @returns {Object} Empty result
     */
    static getEmptyResult() {
        return {
            entities: [],
            entity_count: 0,
            bounds: { min_x: 0, min_y: 0, max_x: 100, max_y: 100 },
            entity_types: {},
            layers: []
        };
    }
}

module.exports = ErgogenDxfParser;
