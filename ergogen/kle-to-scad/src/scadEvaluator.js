/**
 * SCAD Expression Evaluator
 * Simulates OpenSCAD evaluation without requiring OpenSCAD installation
 */

/**
 * Parse and evaluate SCAD parameters and expressions
 * @param {string} parametersPath - Path to parameters.scad
 * @param {string} stabilizersPath - Path to stabilizer_spacing.scad  
 * @param {string} layoutScadPath - Path to layout SCAD file
 * @returns {Object} Evaluated layout data
 */
async function evaluateSCAD(parametersPath, stabilizersPath, layoutScadPath) {
    const fs = require('fs').promises;
    
    // Read all SCAD files
    const [parametersContent, stabilizersContent, layoutContent] = await Promise.all([
        fs.readFile(parametersPath, 'utf-8'),
        fs.readFile(stabilizersPath, 'utf-8'), 
        fs.readFile(layoutScadPath, 'utf-8')
    ]);
    
    // Parse parameters and build evaluation context
    const context = parseParameters(parametersContent);
    const stabilizers = parseStabilizers(stabilizersContent, context);
    Object.assign(context, stabilizers);
    
    // Evaluate layout arrays
    const switches = evaluateArray(layoutContent, 'base_switch_layout', context);
    const stabs = evaluateArray(layoutContent, 'base_stab_layout', context);
    
    return {
        switches,
        stabilizers: stabs,
        context,
        metadata: {
            unit: context.unit,
            switchType: context.switch_type
        }
    };
}

/**
 * Parse parameters.scad and extract constants
 * @param {string} content - parameters.scad content
 * @returns {Object} Parameter values
 */
function parseParameters(content) {
    const context = {};
    
    // Extract parameter definitions
    const lines = content.split('\n');
    
    for (const line of lines) {
        const trimmed = line.trim();
        
        // Skip comments and empty lines
        if (trimmed.startsWith('//') || !trimmed || trimmed.startsWith('/*')) {
            continue;
        }
        
        // Look for variable assignments like: unit = 19.05;
        const match = trimmed.match(/^(\w+)\s*=\s*([^;]+);/);
        if (match) {
            const [, name, value] = match;
            context[name] = evaluateExpression(value.trim(), context);
        }
    }
    
    return context;
}

/**
 * Parse stabilizer_spacing.scad and extract stabilizer definitions
 * @param {string} content - stabilizer_spacing.scad content
 * @param {Object} context - Evaluation context with parameters
 * @returns {Object} Stabilizer definitions
 */
function parseStabilizers(content, context) {
    const stabilizers = {};
    
    const lines = content.split('\n');
    
    for (const line of lines) {
        const trimmed = line.trim();
        
        // Skip comments and includes
        if (trimmed.startsWith('//') || trimmed.startsWith('include') || !trimmed) {
            continue;
        }
        
        // Look for stabilizer definitions like: stab_6_25u = [6.25, 2.625*unit, 2.625*unit];
        const match = trimmed.match(/^(stab_\w+)\s*=\s*\[([^\]]+)\];/);
        if (match) {
            const [, name, arrayContent] = match;
            const elements = arrayContent.split(',').map(el => 
                evaluateExpression(el.trim(), context)
            );
            stabilizers[name] = elements;
        }
    }
    
    return stabilizers;
}

/**
 * Evaluate a SCAD array from layout content
 * @param {string} content - SCAD file content
 * @param {string} arrayName - Name of array to extract
 * @param {Object} context - Evaluation context
 * @returns {Array} Evaluated array
 */
function evaluateArray(content, arrayName, context) {
    const regex = new RegExp(`${arrayName}\\s*=\\s*\\[([\\s\\S]*?)\\];`);
    const match = content.match(regex);
    
    if (!match) {
        return [];
    }
    
    const arrayContent = match[1];
    const items = [];
    
    // Split by lines and process each array element
    const lines = arrayContent.split('\n')
        .map(line => line.trim())
        .filter(line => line && !line.startsWith('//'));
    
    for (const line of lines) {
        if (line.includes('[')) {
            try {
                const evaluated = evaluateArrayElement(line, context);
                if (evaluated) {
                    items.push(evaluated);
                }
            } catch (error) {
                console.warn(`Failed to evaluate line: ${line}`, error);
            }
        }
    }
    
    return items;
}

/**
 * Evaluate a single array element
 * @param {string} line - Line containing array element
 * @param {Object} context - Evaluation context
 * @returns {Array} Evaluated element
 */
function evaluateArrayElement(line, context) {
    // Remove trailing comma
    let cleaned = line.replace(/,$/, '');
    
    // Find nested arrays and evaluate them
    const result = [];
    let current = '';
    let depth = 0;
    
    for (let i = 0; i < cleaned.length; i++) {
        const char = cleaned[i];
        
        if (char === '[') {
            if (depth === 0 && current.trim()) {
                // This shouldn't happen in well-formed arrays
            }
            current += char;
            depth++;
        } else if (char === ']') {
            current += char;
            depth--;
            
            if (depth === 0) {
                // Evaluate this array
                const arrayContent = current.slice(1, -1); // Remove [ ]
                const elements = [];
                
                let elementCurrent = '';
                let elementDepth = 0;
                
                for (let j = 0; j < arrayContent.length; j++) {
                    const c = arrayContent[j];
                    
                    if (c === '[') {
                        elementCurrent += c;
                        elementDepth++;
                    } else if (c === ']') {
                        elementCurrent += c;
                        elementDepth--;
                    } else if (c === ',' && elementDepth === 0) {
                        if (elementCurrent.trim()) {
                            elements.push(evaluateExpression(elementCurrent.trim(), context));
                        }
                        elementCurrent = '';
                    } else {
                        elementCurrent += c;
                    }
                }
                
                // Don't forget the last element
                if (elementCurrent.trim()) {
                    elements.push(evaluateExpression(elementCurrent.trim(), context));
                }
                
                result.push(elements);
                current = '';
            }
        } else if (char === ',' && depth === 0) {
            if (current.trim()) {
                result.push(evaluateExpression(current.trim(), context));
            }
            current = '';
        } else {
            current += char;
        }
    }
    
    // Handle any remaining content
    if (current.trim()) {
        result.push(evaluateExpression(current.trim(), context));
    }
    
    return result;
}

/**
 * Evaluate a SCAD expression
 * @param {string} expr - Expression to evaluate
 * @param {Object} context - Variables and constants
 * @returns {*} Evaluated result
 */
function evaluateExpression(expr, context) {
    // Handle string literals
    if (expr.startsWith('"') && expr.endsWith('"')) {
        return expr.slice(1, -1);
    }
    
    // Handle boolean literals
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    
    // Handle array literals
    if (expr.startsWith('[') && expr.endsWith(']')) {
        const arrayContent = expr.slice(1, -1);
        if (!arrayContent.trim()) return [];
        
        const elements = [];
        let current = '';
        let depth = 0;
        
        for (let i = 0; i < arrayContent.length; i++) {
            const char = arrayContent[i];
            
            if (char === '[') depth++;
            else if (char === ']') depth--;
            else if (char === ',' && depth === 0) {
                if (current.trim()) {
                    elements.push(evaluateExpression(current.trim(), context));
                }
                current = '';
                continue;
            }
            
            current += char;
        }
        
        if (current.trim()) {
            elements.push(evaluateExpression(current.trim(), context));
        }
        
        return elements;
    }
    
    // Handle variable references
    if (context.hasOwnProperty(expr)) {
        return context[expr];
    }
    
    // Handle numeric literals
    if (/^-?\d+(\.\d+)?$/.test(expr)) {
        return parseFloat(expr);
    }
    
    // Handle mathematical expressions
    if (expr.includes('+') || expr.includes('-') || expr.includes('*') || expr.includes('/')) {
        return evaluateMathExpression(expr, context);
    }
    
    // Handle conditional expressions (basic ternary)
    if (expr.includes('?') && expr.includes(':')) {
        return evaluateConditional(expr, context);
    }
    
    // Unknown expression, return as string
    console.warn(`Unknown expression: ${expr}`);
    return expr;
}

/**
 * Evaluate mathematical expressions
 * @param {string} expr - Math expression
 * @param {Object} context - Variables
 * @returns {number} Result
 */
function evaluateMathExpression(expr, context) {
    // Replace variables with their values
    let processed = expr;
    
    // Sort variables by length (longest first) to avoid partial replacements
    const variables = Object.keys(context).sort((a, b) => b.length - a.length);
    
    for (const variable of variables) {
        const regex = new RegExp(`\\b${variable}\\b`, 'g');
        processed = processed.replace(regex, context[variable].toString());
    }
    
    try {
        // Use Function constructor for safe evaluation (safer than eval)
        return Function(`"use strict"; return (${processed})`)();
    } catch (error) {
        console.warn(`Failed to evaluate math expression: ${expr}`, error);
        return 0;
    }
}

/**
 * Evaluate conditional expressions
 * @param {string} expr - Conditional expression
 * @param {Object} context - Variables
 * @returns {*} Result
 */
function evaluateConditional(expr, context) {
    const parts = expr.split('?');
    if (parts.length !== 2) return expr;
    
    const condition = parts[0].trim();
    const outcomes = parts[1].split(':');
    if (outcomes.length !== 2) return expr;
    
    const trueValue = outcomes[0].trim();
    const falseValue = outcomes[1].trim();
    
    const conditionResult = evaluateExpression(condition, context);
    
    return conditionResult ? 
        evaluateExpression(trueValue, context) : 
        evaluateExpression(falseValue, context);
}

module.exports = {
    evaluateSCAD,
    parseParameters,
    parseStabilizers,
    evaluateArray,
    evaluateExpression,
    evaluateMathExpression
};