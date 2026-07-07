#!/usr/bin/env node

// kle-to-scad — Convert KLE JSON into an OpenSCAD layout file for hotswap_pcb_generator.
// Note: the former Ergogen-YAML generation path was removed during the 2026-07 consolidation
// (it produced broken output). Use ../kle-to-ergogen (Python) for KLE → Ergogen conversion.

const { program } = require('commander');
const path = require('path');
const fs = require('fs').promises;
const { convertToIntermediate } = require('./src/kleToIntermediate');
const kle = require("@ijprest/kle-serial");

// Package info
const packageInfo = require('./package.json');

// Configure CLI
program
    .name('kle-to-scad')
    .description('Convert Keyboard Layout Editor (KLE) JSON files to OpenSCAD layouts for hotswap_pcb_generator')
    .version(packageInfo.version);

program
    .argument('<input>', 'Input KLE JSON file path')
    .option('-o, --output <path>', 'Output SCAD file path', null)
    .option('-v, --verbose', 'Verbose output', false)
    .action(async (input, options) => {
        try {
            await convertKLEToSCAD(input, options);
        } catch (error) {
            console.error('Error:', error.message);
            if (options.verbose) {
                console.error(error.stack);
            }
            process.exit(1);
        }
    });

/**
 * Main conversion function
 * @param {string} inputPath - Path to KLE JSON file
 * @param {Object} options - Conversion options
 */
async function convertKLEToSCAD(inputPath, options) {
    // Resolve paths
    const resolvedInput = path.resolve(inputPath);
    const defaultOutput = resolvedInput.replace(/\.json$/i, '.scad');
    const outputPath = options.output ? path.resolve(options.output) : defaultOutput;

    console.log(`Converting ${path.basename(inputPath)} to OpenSCAD layout...`);

    // Step 1: Parse KLE file using kle-serial directly (like hotswap_pcb_generator)
    if (options.verbose) console.log('Parsing KLE file...');
    const kleJson = await fs.readFile(resolvedInput, 'utf-8');
    const keyboard = kle.Serial.parse(kleJson);

    // Step 2: Convert to intermediate format (positions, matrix, stabilizers, SCAD data)
    if (options.verbose) console.log('Converting to intermediate format...');
    const intermediateData = convertToIntermediate(keyboard);

    console.log(`Found ${intermediateData.keys.length} keys`);
    if (intermediateData.stats.stabilizedKeys > 0) {
        console.log(`Including ${intermediateData.stats.stabilizedKeys} stabilized keys`);
    }

    const matrixInfo = {
        rows: Math.max(...intermediateData.keys.map(k => k.matrix.row)) + 1,
        cols: Math.max(...intermediateData.keys.map(k => k.matrix.col)) + 1
    };
    console.log(`Matrix: ${matrixInfo.rows} rows × ${matrixInfo.cols} columns`);

    // Step 3: Generate SCAD output
    await generateSCAD(intermediateData, outputPath, options);

    // Print summary
    printSummary(intermediateData, options);
}

/**
 * Generate OpenSCAD file similar to hotswap_pcb_generator
 * @param {Object} intermediateData - Intermediate keyboard data
 * @param {string} outputPath - Output SCAD file path
 * @param {Object} options - Generation options
 */
async function generateSCAD(intermediateData, outputPath, options) {
    if (options.verbose) console.log('Generating OpenSCAD file...');

    // Use the SCAD format directly from intermediate keys
    const scadContent = `// Generated from KLE by kle-to-scad converter
// Keys: ${intermediateData.keys.length}
// Stabilized keys: ${intermediateData.stats.stabilizedKeys}

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
    ]
*/

// Keyswitch Layout
base_switch_layout = [
${intermediateData.keys.map(key => {
    // Use the pre-formatted SCAD data from the intermediate format
    return '  ' + JSON.stringify(key.scadFormat).replace(/"/g, '');
}).join(',\n')}
];

// MCU Position(s)
base_mcu_layout = [];

// TRRS Position(s)
base_trrs_layout = [];

// Stabilizer layout
//     (extra_data = [key_size, left_offset, right_offset, switch_offset=0])
base_stab_layout = [
${intermediateData.groups.stabilized.map(key => {
    const stabData = [
        key.scadFormat[0], // Position data
        key.scadFormat[1], // Borders
        key.stabilizer.type // Stabilizer type from intermediate format
    ];
    return '  ' + JSON.stringify(stabData).replace(/"/g, '');
}).join(',\n')}
];

// Via layout
base_via_layout = [];

// Plate Layout
base_plate_layout = [];

// Standoff layout
base_standoff_layout = [];

module additional_plate_cutouts() {
    square(0);
}

module additional_case_cavities() {
    square(0);
}

// Configuration flags
use_plate_layout_only = false;
invert_layout_flag = false;
layout_type = "column";
tent_angle_y = 0;
tent_angle_x = 0;
tent_point = [0, 0, 0];
`;

    await fs.writeFile(outputPath, scadContent, 'utf-8');
    console.log(`✓ OpenSCAD file saved to ${path.basename(outputPath)}`);
}

/**
 * Print conversion summary
 * @param {Object} intermediateData - Intermediate keyboard data
 * @param {Object} options - Conversion options
 */
function printSummary(intermediateData, options) {
    console.log('\n--- Conversion Summary ---');
    console.log(`Total Keys: ${intermediateData.keys.length}`);
    console.log(`Stabilized Keys: ${intermediateData.stats.stabilizedKeys}`);

    const matrixInfo = {
        rows: Math.max(...intermediateData.keys.map(k => k.matrix.row)) + 1,
        cols: Math.max(...intermediateData.keys.map(k => k.matrix.col)) + 1
    };
    console.log(`Matrix Size: ${matrixInfo.rows}×${matrixInfo.cols}`);

    if (intermediateData.bounds) {
        const width = (intermediateData.bounds.width_mm).toFixed(1);
        const height = (intermediateData.bounds.height_mm).toFixed(1);
        console.log(`Layout Size: ${width}mm × ${height}mm`);
    }

    if (intermediateData.stats.hasRotation) {
        console.log(`Note: Layout contains rotated keys`);
    }

    console.log('\n✅ Conversion complete!');
    console.log('Use the generated .scad file with hotswap_pcb_generator (requires its parameters.scad, stabilizer_spacing.scad, utils.scad).');
}

// Parse arguments
program.parse();