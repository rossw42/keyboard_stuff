const fs = require('fs');

// Test the parser with the actual DXF file
const dxfContent = fs.readFileSync('../keyboards/macropad/config_4x5/outlines/switchplate.dxf', 'utf8');
const lines = dxfContent.split('\n').map(line => line.trim()).filter(line => line);

console.log('--- Searching for CIRCLE entities in DXF ---');

// Find the ENTITIES section
let entitiesStart = -1;
let entitiesEnd = -1;

for (let i = 0; i < lines.length - 1; i++) {
    if (lines[i] === '2' && lines[i + 1] === 'ENTITIES') {
        entitiesStart = i + 2;
        console.log(`ENTITIES section starts at line ${entitiesStart}: "${lines[entitiesStart]}"`);
    } else if (entitiesStart !== -1 && lines[i] === '0' && lines[i + 1] === 'ENDSEC') {
        entitiesEnd = i;
        console.log(`ENTITIES section ends at line ${entitiesEnd}: "${lines[entitiesEnd]}"`);
        break;
    }
}

console.log(`\n--- Looking for CIRCLE entities between lines ${entitiesStart} and ${entitiesEnd} ---`);

let circleCount = 0;
for (let i = entitiesStart; i < entitiesEnd; i++) {
    if (lines[i] === '0' && i + 1 < lines.length && lines[i + 1] === 'CIRCLE') {
        circleCount++;
        console.log(`\nFound CIRCLE entity #${circleCount} at line ${i}:`);
        
        // Show the next 20 lines after finding CIRCLE
        for (let j = i; j < Math.min(i + 20, entitiesEnd); j++) {
            console.log(`  ${j}: "${lines[j]}"`);
        }
    }
}

console.log(`\n--- Total CIRCLE entities found: ${circleCount} ---`);

console.log('\n--- Entity type scan ---');
const entityTypes = new Set();
for (let i = entitiesStart; i < entitiesEnd; i++) {
    if (lines[i] === '0' && i + 1 < lines.length) {
        const entityType = lines[i + 1];
        if (!['ENDSEC'].includes(entityType)) {
            entityTypes.add(entityType);
        }
    }
}
console.log('All entity types found:', Array.from(entityTypes));
