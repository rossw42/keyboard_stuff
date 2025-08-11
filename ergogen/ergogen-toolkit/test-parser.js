const fs = require('fs');
const DxfParser = require('./dxfParser');

// Test the parser with the board.dxf file
const content = fs.readFileSync('../mounting_styles/output/outlines/board.dxf', 'utf8');

console.log('DXF file content preview:');
console.log(content.substring(0, 500));
console.log('\n--- Parsing DXF ---');

const result = DxfParser.parse(content);
console.log('Parse result:', {
    entity_count: result.entity_count,
    entity_types: result.entity_types,
    bounds: result.bounds
});

if (result.entities.length > 0) {
    console.log('First entity:', result.entities[0]);
} else {
    console.log('No entities found!');
    
    // Debug: check what lines we're processing
    const lines = content.split('\n').map(line => line.trim()).filter(line => line);
    console.log('Total lines:', lines.length);
    
    // Look for ENTITIES section
    let inEntities = false;
    for (let i = 0; i < lines.length - 1; i++) {
        if (lines[i] === '2' && lines[i + 1] === 'ENTITIES') {
            console.log(`Found ENTITIES section at line ${i}`);
            inEntities = true;
            i += 2;
            continue;
        }
        
        if (inEntities && lines[i] === '0') {
            console.log(`Entity marker at line ${i}: "${lines[i]}" -> "${lines[i + 1]}"`);
            if (i > 60) break; // Limit output
        }
        
        if (inEntities && lines[i] === '0' && lines[i + 1] === 'ENDSEC') {
            console.log('End of ENTITIES section');
            break;
        }
    }
}