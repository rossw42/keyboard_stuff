const ConnectionDiagramGenerator = require('./connectionDiagramGenerator');
const path = require('path');

async function testConnectionDiagram() {
    console.log('🧪 Testing Connection Diagram Generator...');
    
    const generator = new ConnectionDiagramGenerator();
    const yamlFile = path.join('..', 'keyboards', 'macropad', 'config_4x5.yaml');
    const outputDir = path.join('..', 'keyboards', 'macropad');
    
    try {
        const result = await generator.generateFromFile(yamlFile, outputDir);
        
        if (result.success) {
            console.log('✅ Connection diagram generated successfully!');
            console.log(`📄 Output file: ${result.outputPath}`);
            console.log('\n📊 Preview of generated diagram:');
            console.log(result.diagram.substring(0, 500) + '...');
        } else {
            console.log('❌ Connection diagram generation failed:');
            console.log(result.error);
        }
    } catch (error) {
        console.log('❌ Test failed:');
        console.log(error.message);
    }
}

testConnectionDiagram();
