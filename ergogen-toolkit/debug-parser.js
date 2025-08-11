const DxfParser = require('./dxfParser');
const fs = require('fs');

// Test the parser with the actual DXF file
const dxfContent = fs.readFileSync('../keyboards/macropad/config_4x5/outlines/switchplate.dxf', 'utf8');

console.log('--- DXF Content Preview ---');
const lines = dxfContent.split('\n').slice(0, 50);
console.log(lines.join('\n'));

console.log('\n--- Parsing DXF ---');
const result = DxfParser.parse(dxfContent);

console.log('Entity Count:', result.entity_count);
console.log('Entity Types:', result.entity_types);
console.log('Bounds:', result.bounds);
console.log('Layers:', result.layers);

console.log('\n--- First 10 Entities ---');
result.entities.slice(0, 10).forEach((entity, i) => {
    console.log(`${i + 1}. Type: ${entity.type}`, entity);
});

console.log('\n--- All Circle Entities ---');
const circles = result.entities.filter(e => e.type === 'circle');
console.log(`Found ${circles.length} circles:`);
circles.forEach((circle, i) => {
    console.log(`Circle ${i + 1}:`, circle);
});
