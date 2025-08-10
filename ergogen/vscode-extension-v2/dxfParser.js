/**
 * DXF Parser Module
 * Parses DXF file content and extracts entities
 */

class DxfParser {
    /**
     * Parse DXF content
     * @param {string} content - DXF file content
     * @returns {Object} Parsed DXF data with entities and bounds
     */
    static parse(content) {
        const lines = content.split('\n').map(line => line.trim()).filter(line => line);
        const entities = [];
        let bounds = {
            min_x: Infinity,
            min_y: Infinity,
            max_x: -Infinity,
            max_y: -Infinity
        };

        // Find the ENTITIES section
        let entitiesStart = -1;
        let entitiesEnd = -1;
        
        for (let i = 0; i < lines.length - 1; i++) {
            if (lines[i] === '2' && lines[i + 1] === 'ENTITIES') {
                entitiesStart = i + 2;
            } else if (entitiesStart !== -1 && lines[i] === '0' && lines[i + 1] === 'ENDSEC') {
                entitiesEnd = i;
                break;
            }
        }
        
        if (entitiesStart === -1) {
            // No ENTITIES section found
            return {
                entities: [],
                entity_count: 0,
                bounds: { min_x: 0, min_y: 0, max_x: 100, max_y: 100 },
                entity_types: {},
                layers: []
            };
        }
        
        // Process entities within the ENTITIES section
        let i = entitiesStart;
        while (i < (entitiesEnd !== -1 ? entitiesEnd : lines.length)) {
            if (lines[i] === '0' && i + 1 < lines.length) {
                const entityType = lines[i + 1];
                
                switch (entityType) {
                    case 'LINE':
                        const line = this.parseLine(lines, i);
                        if (line) {
                            entities.push(line);
                            this.updateBounds(bounds, line.start);
                            this.updateBounds(bounds, line.end);
                        }
                        break;
                        
                    case 'CIRCLE':
                        const circle = this.parseCircle(lines, i);
                        if (circle) {
                            entities.push(circle);
                            this.updateBounds(bounds, {
                                x: circle.center.x - circle.radius,
                                y: circle.center.y - circle.radius
                            });
                            this.updateBounds(bounds, {
                                x: circle.center.x + circle.radius,
                                y: circle.center.y + circle.radius
                            });
                        }
                        break;
                        
                    case 'ARC':
                        const arc = this.parseArc(lines, i);
                        if (arc) {
                            entities.push(arc);
                            // Calculate arc endpoints
                            const startRad = arc.start_angle * Math.PI / 180;
                            const endRad = arc.end_angle * Math.PI / 180;
                            
                            this.updateBounds(bounds, {
                                x: arc.center.x + arc.radius * Math.cos(startRad),
                                y: arc.center.y + arc.radius * Math.sin(startRad)
                            });
                            this.updateBounds(bounds, {
                                x: arc.center.x + arc.radius * Math.cos(endRad),
                                y: arc.center.y + arc.radius * Math.sin(endRad)
                            });
                            
                            // Check quadrant crossings for accurate bounds
                            this.updateArcBounds(bounds, arc);
                        }
                        break;
                        
                    case 'LWPOLYLINE':
                    case 'POLYLINE':
                        const polyline = this.parsePolyline(lines, i, entityType);
                        if (polyline && polyline.points.length > 0) {
                            entities.push(polyline);
                            polyline.points.forEach(point => {
                                this.updateBounds(bounds, point);
                            });
                        }
                        break;
                        
                    case 'TEXT':
                    case 'MTEXT':
                        const text = this.parseText(lines, i, entityType);
                        if (text) {
                            entities.push(text);
                            this.updateBounds(bounds, text.position);
                        }
                        break;
                        
                    case 'DIMENSION':
                        const dimension = this.parseDimension(lines, i);
                        if (dimension) {
                            entities.push(dimension);
                            this.updateBounds(bounds, dimension.start);
                            this.updateBounds(bounds, dimension.end);
                        }
                        break;
                        
                    case 'ELLIPSE':
                        const ellipse = this.parseEllipse(lines, i);
                        if (ellipse) {
                            entities.push(ellipse);
                            this.updateBounds(bounds, {
                                x: ellipse.center.x - ellipse.major_axis,
                                y: ellipse.center.y - ellipse.minor_axis
                            });
                            this.updateBounds(bounds, {
                                x: ellipse.center.x + ellipse.major_axis,
                                y: ellipse.center.y + ellipse.minor_axis
                            });
                        }
                        break;
                        
                    case 'SPLINE':
                        const spline = this.parseSpline(lines, i);
                        if (spline && spline.control_points.length > 0) {
                            entities.push(spline);
                            spline.control_points.forEach(point => {
                                this.updateBounds(bounds, point);
                            });
                        }
                        break;
                }
            }
            i++;
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
    }

    static parseLine(lines, startIndex) {
        let x1, y1, x2, y2, layer = '0', color = 7;
        
        for (let i = startIndex; i < Math.min(startIndex + 100, lines.length - 1); i++) {
            const code = lines[i];
            const value = lines[i + 1];
            
            switch (code) {
                case '8': layer = value; break;
                case '62': color = parseInt(value); break;
                case '10': x1 = parseFloat(value); break;
                case '20': y1 = parseFloat(value); break;
                case '11': x2 = parseFloat(value); break;
                case '21': y2 = parseFloat(value); break;
                case '0': 
                    if (i > startIndex) {
                        if (x1 !== undefined && y1 !== undefined && 
                            x2 !== undefined && y2 !== undefined) {
                            return {
                                type: 'line',
                                start: { x: x1, y: y1 },
                                end: { x: x2, y: y2 },
                                layer: layer,
                                color: color
                            };
                        }
                        return null;
                    }
                    break;
            }
        }
        
        if (x1 !== undefined && y1 !== undefined && 
            x2 !== undefined && y2 !== undefined) {
            return {
                type: 'line',
                start: { x: x1, y: y1 },
                end: { x: x2, y: y2 },
                layer: layer,
                color: color
            };
        }
        return null;
    }

    static parseCircle(lines, startIndex) {
        let cx, cy, radius, layer = '0', color = 7;
        
        for (let i = startIndex; i < Math.min(startIndex + 100, lines.length - 1); i++) {
            const code = lines[i];
            const value = lines[i + 1];
            
            switch (code) {
                case '8': layer = value; break;
                case '62': color = parseInt(value); break;
                case '10': cx = parseFloat(value); break;
                case '20': cy = parseFloat(value); break;
                case '40': radius = parseFloat(value); break;
                case '0':
                    if (i > startIndex) {
                        if (cx !== undefined && cy !== undefined && radius !== undefined) {
                            return {
                                type: 'circle',
                                center: { x: cx, y: cy },
                                radius: radius,
                                layer: layer,
                                color: color
                            };
                        }
                        return null;
                    }
                    break;
            }
        }
        
        if (cx !== undefined && cy !== undefined && radius !== undefined) {
            return {
                type: 'circle',
                center: { x: cx, y: cy },
                radius: radius,
                layer: layer,
                color: color
            };
        }
        return null;
    }

    static parseArc(lines, startIndex) {
        let cx, cy, radius, startAngle, endAngle, layer = '0', color = 7;
        
        for (let i = startIndex; i < Math.min(startIndex + 100, lines.length - 1); i++) {
            const code = lines[i];
            const value = lines[i + 1];
            
            switch (code) {
                case '8': layer = value; break;
                case '62': color = parseInt(value); break;
                case '10': cx = parseFloat(value); break;
                case '20': cy = parseFloat(value); break;
                case '40': radius = parseFloat(value); break;
                case '50': startAngle = parseFloat(value); break;
                case '51': endAngle = parseFloat(value); break;
                case '0':
                    if (i > startIndex) {
                        if (cx !== undefined && cy !== undefined && radius !== undefined &&
                            startAngle !== undefined && endAngle !== undefined) {
                            return {
                                type: 'arc',
                                center: { x: cx, y: cy },
                                radius: radius,
                                start_angle: startAngle,
                                end_angle: endAngle,
                                layer: layer,
                                color: color
                            };
                        }
                        return null;
                    }
                    break;
            }
        }
        
        if (cx !== undefined && cy !== undefined && radius !== undefined &&
            startAngle !== undefined && endAngle !== undefined) {
            return {
                type: 'arc',
                center: { x: cx, y: cy },
                radius: radius,
                start_angle: startAngle,
                end_angle: endAngle,
                layer: layer,
                color: color
            };
        }
        return null;
    }

    static parsePolyline(lines, startIndex, entityType) {
        const points = [];
        let closed = false;
        let layer = '0';
        let color = 7;
        
        for (let i = startIndex; i < lines.length - 1; i++) {
            const code = lines[i];
            const value = lines[i + 1];
            
            switch (code) {
                case '8': layer = value; break;
                case '62': color = parseInt(value); break;
                case '70':
                    const flags = parseInt(value);
                    closed = (flags & 1) === 1;
                    break;
                case '10':
                    const x = parseFloat(value);
                    // Look for Y coordinate
                    for (let j = i + 2; j < Math.min(i + 10, lines.length - 1); j += 2) {
                        if (lines[j] === '20') {
                            const y = parseFloat(lines[j + 1]);
                            if (!isNaN(x) && !isNaN(y)) {
                                points.push({ x: x, y: y });
                            }
                            break;
                        }
                    }
                    break;
                case '0':
                    if (i > startIndex && lines[i + 1] !== 'VERTEX') {
                        if (points.length > 0) {
                            return {
                                type: 'polyline',
                                points: points,
                                closed: closed,
                                layer: layer,
                                color: color
                            };
                        }
                        return null;
                    }
                    break;
            }
        }
        
        if (points.length > 0) {
            return {
                type: 'polyline',
                points: points,
                closed: closed,
                layer: layer,
                color: color
            };
        }
        return null;
    }

    static parseText(lines, startIndex, entityType) {
        let x, y, height, rotation = 0, text = '', layer = '0', color = 7;
        
        for (let i = startIndex; i < Math.min(startIndex + 100, lines.length - 1); i++) {
            const code = lines[i];
            const value = lines[i + 1];
            
            switch (code) {
                case '8': layer = value; break;
                case '62': color = parseInt(value); break;
                case '10': x = parseFloat(value); break;
                case '20': y = parseFloat(value); break;
                case '40': height = parseFloat(value); break;
                case '50': rotation = parseFloat(value); break;
                case '1': text = value; break;
                case '0':
                    if (i > startIndex) {
                        if (x !== undefined && y !== undefined && text) {
                            return {
                                type: 'text',
                                position: { x: x, y: y },
                                text: text,
                                height: height || 1,
                                rotation: rotation,
                                layer: layer,
                                color: color
                            };
                        }
                        return null;
                    }
                    break;
            }
        }
        
        if (x !== undefined && y !== undefined && text) {
            return {
                type: 'text',
                position: { x: x, y: y },
                text: text,
                height: height || 1,
                rotation: rotation,
                layer: layer,
                color: color
            };
        }
        return null;
    }

    static parseDimension(lines, startIndex) {
        let x1, y1, x2, y2, text = '', layer = '0', color = 7;
        
        for (let i = startIndex; i < Math.min(startIndex + 150, lines.length - 1); i++) {
            const code = lines[i];
            const value = lines[i + 1];
            
            switch (code) {
                case '8': layer = value; break;
                case '62': color = parseInt(value); break;
                case '13': x1 = parseFloat(value); break;
                case '23': y1 = parseFloat(value); break;
                case '14': x2 = parseFloat(value); break;
                case '24': y2 = parseFloat(value); break;
                case '1': text = value; break;
                case '0':
                    if (i > startIndex) {
                        if (x1 !== undefined && y1 !== undefined &&
                            x2 !== undefined && y2 !== undefined) {
                            return {
                                type: 'dimension',
                                start: { x: x1, y: y1 },
                                end: { x: x2, y: y2 },
                                text: text,
                                layer: layer,
                                color: color
                            };
                        }
                        return null;
                    }
                    break;
            }
        }
        return null;
    }

    static parseEllipse(lines, startIndex) {
        let cx, cy, major_x, major_y, ratio = 1, layer = '0', color = 7;
        
        for (let i = startIndex; i < Math.min(startIndex + 100, lines.length - 1); i++) {
            const code = lines[i];
            const value = lines[i + 1];
            
            switch (code) {
                case '8': layer = value; break;
                case '62': color = parseInt(value); break;
                case '10': cx = parseFloat(value); break;
                case '20': cy = parseFloat(value); break;
                case '11': major_x = parseFloat(value); break;
                case '21': major_y = parseFloat(value); break;
                case '40': ratio = parseFloat(value); break;
                case '0':
                    if (i > startIndex) {
                        if (cx !== undefined && cy !== undefined &&
                            major_x !== undefined && major_y !== undefined) {
                            const major_axis = Math.sqrt(major_x * major_x + major_y * major_y);
                            return {
                                type: 'ellipse',
                                center: { x: cx, y: cy },
                                major_axis: major_axis,
                                minor_axis: major_axis * ratio,
                                rotation: Math.atan2(major_y, major_x) * 180 / Math.PI,
                                layer: layer,
                                color: color
                            };
                        }
                        return null;
                    }
                    break;
            }
        }
        return null;
    }

    static parseSpline(lines, startIndex) {
        const control_points = [];
        let degree = 3, layer = '0', color = 7;
        
        for (let i = startIndex; i < lines.length - 1; i++) {
            const code = lines[i];
            const value = lines[i + 1];
            
            switch (code) {
                case '8': layer = value; break;
                case '62': color = parseInt(value); break;
                case '71': degree = parseInt(value); break;
                case '10':
                    const x = parseFloat(value);
                    // Look for Y coordinate
                    for (let j = i + 2; j < Math.min(i + 10, lines.length - 1); j += 2) {
                        if (lines[j] === '20') {
                            const y = parseFloat(lines[j + 1]);
                            if (!isNaN(x) && !isNaN(y)) {
                                control_points.push({ x: x, y: y });
                            }
                            break;
                        }
                    }
                    break;
                case '0':
                    if (i > startIndex) {
                        if (control_points.length > 0) {
                            return {
                                type: 'spline',
                                control_points: control_points,
                                degree: degree,
                                layer: layer,
                                color: color
                            };
                        }
                        return null;
                    }
                    break;
            }
        }
        return null;
    }

    static updateBounds(bounds, point) {
        bounds.min_x = Math.min(bounds.min_x, point.x);
        bounds.min_y = Math.min(bounds.min_y, point.y);
        bounds.max_x = Math.max(bounds.max_x, point.x);
        bounds.max_y = Math.max(bounds.max_y, point.y);
    }

    static updateArcBounds(bounds, arc) {
        // Check if arc crosses 0°, 90°, 180°, or 270°
        const angles = [0, 90, 180, 270];
        let start = arc.start_angle;
        let end = arc.end_angle;
        
        // Normalize angles
        if (end < start) end += 360;
        
        for (const angle of angles) {
            if ((start <= angle && angle <= end) || 
                (start <= angle + 360 && angle + 360 <= end)) {
                const rad = angle * Math.PI / 180;
                this.updateBounds(bounds, {
                    x: arc.center.x + arc.radius * Math.cos(rad),
                    y: arc.center.y + arc.radius * Math.sin(rad)
                });
            }
        }
    }

    static getEntityTypeSummary(entities) {
        const summary = {};
        for (const entity of entities) {
            summary[entity.type] = (summary[entity.type] || 0) + 1;
        }
        return summary;
    }

    static extractLayers(entities) {
        const layers = new Set();
        for (const entity of entities) {
            if (entity.layer) {
                layers.add(entity.layer);
            }
        }
        return Array.from(layers).sort();
    }
}

module.exports = DxfParser;