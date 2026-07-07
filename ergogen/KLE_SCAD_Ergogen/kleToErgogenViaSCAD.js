#!/usr/bin/env node

/**
 * KLE to Ergogen via SCAD Converter
 * Uses hotswap_pcb_generator's approach as first step, then converts SCAD to Ergogen YAML
 */

const { program } = require('commander');
const path = require('path');
const fs = require('fs').promises;
const kle = require("@ijprest/kle-serial");
const { convertToErgogen, parseSCADLayout } = require('./src/scadToErgogen');

// Package info
const packageInfo = require('./package.json');

// Configure CLI
program
    .name('kle-to-ergogen-via-scad')
    .description('Convert KLE JSON to Ergogen YAML using hotswap_pcb_generator approach as first step')
    .version(packageInfo.version);

program
    .argument('<input>', 'Input KLE JSON file path')
    .option('-o, --output <path>', 'Output Ergogen YAML file path', null)
    .option('-s, --switch-type <type>', 'Switch type (mx, choc, choc_v2)', 'mx')
    .option('-k, --key-spacing <mm>', 'Key spacing in mm', '19')
    .option('-m, --microcontroller <type>', 'Microcontroller type', 'promicro')
    .option('--hotswap', 'Use hotswap sockets', true)
    .option('--no-hotswap', 'Use soldered switches')
    .option('--include-pcb', 'Include PCB generation', false)
    .option('--include-case', 'Include case generation', false)
    .option('--keep-scad', 'Keep intermediate SCAD file', false)
    .option('-v, --verbose', 'Verbose output', false)
    .action(async (input, options) => {
        try {
            await convertKLEToErgogenViaSCAD(input, options);
        } catch (error) {
            console.error('Error:', error.message);
            if (options.verbose) {
                console.error(error.stack);
            }
            process.exit(1);
        }
    });

/**
 * Main conversion function using hotswap_pcb_generator approach
 * @param {string} inputPath - Path to KLE JSON file
 * @param {Object} options - Conversion options
 */
async function convertKLEToErgogenViaSCAD(inputPath, options) {
    // Resolve paths
    const resolvedInput = path.resolve(inputPath);
    const defaultOutput = resolvedInput.replace(/\.json$/i, '.yaml');
    const outputPath = options.output ? path.resolve(options.output) : defaultOutput;
    const scadPath = resolvedInput.replace(/\.json$/i, '.scad');
    
    console.log(`Converting ${path.basename(inputPath)} to Ergogen format via SCAD...`);
    
    // Step 1: Parse KLE file using hotswap_pcb_generator approach
    if (options.verbose) console.log('Step 1: Parsing KLE file...');
    const kleJson = await fs.readFile(resolvedInput, 'utf-8');
    const keyboard = kle.Serial.parse(kleJson);
    
    console.log(`Found ${keyboard.keys.length} keys`);
    
    // Step 2: Convert to SCAD format (like hotswap_pcb_generator)
    if (options.verbose) console.log('Step 2: Converting to SCAD format...');
    const scadContent = generateSCADFromKLE(keyboard, options);
    
    // Save intermediate SCAD file
    await fs.writeFile(scadPath, scadContent, 'utf-8');
    if (options.verbose) console.log(`Intermediate SCAD saved to ${path.basename(scadPath)}`);
    
    // Step 3: Parse SCAD and convert to Ergogen
    if (options.verbose) console.log('Step 3: Converting SCAD to Ergogen...');
    const scadData = await parseSCADLayout(scadPath);
    
    const ergogenYAML = convertToErgogen(scadData, {
        switchType: options.switchType,
        keySpacing: parseFloat(options.keySpacing),
        includeOutlines: true,
        includePCB: options.includePcb,
        includeCase: options.includeCase,
        hotswap: options.hotswap,
        microcontroller: options.microcontroller
    });
    
    // Step 4: Save Ergogen YAML
    await fs.writeFile(outputPath, ergogenYAML, 'utf-8');
    console.log(`✓ Ergogen configuration saved to ${path.basename(outputPath)}`);
    
    // Clean up intermediate SCAD file unless requested to keep it
    if (!options.keepScad) {
        await fs.unlink(scadPath);
        if (options.verbose) console.log('Cleaned up intermediate SCAD file');
    }
    
    // Print summary
    printSummary(scadData, options);
}

/**
 * Generate SCAD content from KLE data using hotswap_pcb_generator approach
 * @param {Object} keyboard - Parsed KLE keyboard object
 * @param {Object} options - Generation options
 * @returns {string} SCAD content
 */
function generateSCADFromKLE(keyboard, options) {
    // Convert KLE data to hotswap_pcb_generator format
    const formatted_keys = keyboard.keys.map(key => {
        let side_border = ((key.width || 1) - 1) / 2;
        return [
            [
                [key.x, key.y],
                key.width || 1,
                [-(key.rotation_angle || 0), key.rotation_x || 0, key.rotation_y || 0]
            ],
            [
                1,
                1,
                side_border ? `1+${side_border}*unit*mm` : 1,
                side_border ? `1+${side_border}*unit*mm` : 1,
            ],
            false
        ];
    });
    
    // Generate SCAD content exactly like hotswap_pcb_generator
    let file_content = `// Generated from KLE by kle-to-ergogen-via-scad converter
// Keys: ${keyboard.keys.length}

include <parameters.scad>
include <stabilizer_spacing.scad>

use <utils.scad>

/* [Layout Values] */
/* Layout Format (each key):
    [
        [                                       // Location Data
            [x_location, y_location],
            key_size,
            [rotation, rotation_x, rotation_y],
        ],
        [                                       // Borders
            top_border,
            bottom_border,
            left_border,
            right_border
        ],
        extra_data                              // Extra data (depending on component type)
        [                                       // Trim (optional booleans)
            top_border,
            bottom_border,
            left_border,
            right_border
        ],
    ]
*/

// Keyswitch Layout
//     (extra_data = rotate_column)
`;

    file_content += formatted_keys.reduce(
        (total, key) => (
            total +  // Output accumulator
            "  " +   // Indentation
            JSON.stringify(key).replace(/"/g, "") + // Key data
            ",\n"  // End of line
        ),
        "base_switch_layout = [\n"
    );

    file_content += `];

// MCU Position(s)
base_mcu_layout = [];

// TRRS Position(s)
base_trrs_layout = [];

// Stabilizer layout
//     (extra_data = [key_size, left_offset, right_offset, switch_offset=0])
//     (see stabilizer_spacing.scad for presets)
`;

    // Add stabilizers for keys >= 2u (like hotswap_pcb_generator)
    file_content += formatted_keys.filter((k) => k[0][1] >= 2).reduce(
        (total, key) => (
            total +  // Output accumulator
            "  " +   // Indentation
            JSON.stringify([
                key[0], // Key position
                key[1], // Key borders
                `stab_${key[0][1].toString().replace('.', '_')}u`, // Convert key width to default stabilizer constant
            ]).replace(/"/g, "") +
            ",\n"  // End of line
        ),
        "base_stab_layout = [\n"
    );

    // Rest of the standard data (like hotswap_pcb_generator)
    file_content += `];

// Via layout
//     (extra_data = [via_width, via_length])
base_via_layout = [];

// Plate Layout (if different than PCB)
//     (extra_data = component_type)
base_plate_layout = [];

// Standoff layout
//     (extra_data = [standoff_integration_override, standoff_attachment_override])
base_standoff_layout = [];

module additional_plate_cutouts() {
    square(0); // Dummy geometry to fix preview bug
} 

module additional_case_cavities() {
    square(0); // Dummy geometry to fix preview bug
}

// Whether to only use base_plate_layout to generate the plate footprint
use_plate_layout_only = false;

// Whether to flip the layout (useful for split boards)
invert_layout_flag = false;

// Whether the layout is staggered-row or staggered-column
layout_type = "column";  // [column, row]

// Tenting
// Angle around y-axis (i.e. typing angle)
tent_angle_y = 0;
// Angle around x-axis
tent_angle_x = 0;
// Point around which keyboard is tented
tent_point = [0, 0, 0];

`;

    return file_content;
}

/**
 * Print conversion summary
 * @param {Object} scadData - Parsed SCAD data
 * @param {Object} options - Conversion options
 */
function printSummary(scadData, options) {
    console.log('\n--- Conversion Summary ---');
    console.log(`Keyboard: ${scadData.metadata.name || 'Unnamed'}`);
    console.log(`Total Keys: ${scadData.switches.length}`);
    console.log(`Stabilized Keys: ${scadData.stabilizers.length}`);
    console.log(`Switch Type: ${options.switchType}`);
    console.log(`Hotswap: ${options.hotswap ? 'Yes' : 'No'}`);
    console.log(`Key Spacing: ${options.keySpacing}mm`);
    
    console.log('\n✅ Conversion complete!');
    console.log('Pipeline: KLE → hotswap_pcb_generator format → SCAD → Ergogen YAML');
    console.log('You can now use the generated YAML file with Ergogen to create your PCB.');
}

// Parse arguments
program.parse();