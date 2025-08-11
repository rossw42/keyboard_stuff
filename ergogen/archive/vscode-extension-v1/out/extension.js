"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const child_process_1 = require("child_process");
function activate(context) {
    console.log('Ergogen DXF Viewer extension is now active');
    // Register command to run ergogen
    const runErgogenCommand = vscode.commands.registerCommand('ergogen-dxf-viewer.runErgogen', async () => {
        await runErgogen();
    });
    // Register command to open DXF viewer in browser
    const openViewerCommand = vscode.commands.registerCommand('ergogen-dxf-viewer.openViewer', () => {
        vscode.env.openExternal(vscode.Uri.parse('http://localhost:5173'));
    });
    context.subscriptions.push(runErgogenCommand, openViewerCommand);
    // Show welcome message for Ergogen projects
    if (vscode.workspace.workspaceFolders) {
        vscode.workspace.findFiles('**/*.yaml', null, 1).then(files => {
            if (files.length > 0) {
                vscode.window.showInformationMessage('Ergogen project detected! Make sure DXF viewer is running on localhost:5173', 'Open Viewer', 'Run Ergogen').then(selection => {
                    if (selection === 'Open Viewer') {
                        vscode.commands.executeCommand('ergogen-dxf-viewer.openViewer');
                    }
                    else if (selection === 'Run Ergogen') {
                        vscode.commands.executeCommand('ergogen-dxf-viewer.runErgogen');
                    }
                });
            }
        });
    }
}
exports.activate = activate;
async function runErgogen() {
    if (!vscode.workspace.workspaceFolders) {
        vscode.window.showErrorMessage('No workspace folder found');
        return;
    }
    const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
    // Find YAML files in workspace
    const yamlFiles = await vscode.workspace.findFiles('**/*.yaml', null, 10);
    if (yamlFiles.length === 0) {
        vscode.window.showErrorMessage('No YAML files found in workspace');
        return;
    }
    // Use keyboard.yaml if it exists, otherwise use the first YAML file
    let configFile = yamlFiles.find(file => file.fsPath.includes('keyboard.yaml'))?.fsPath;
    if (!configFile) {
        configFile = yamlFiles[0].fsPath;
    }
    // Show progress
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Running Ergogen...',
        cancellable: false
    }, async () => {
        return new Promise((resolve, reject) => {
            const ergogenProcess = (0, child_process_1.spawn)('ergogen', ['keyboard.yaml'], {
                cwd: workspaceRoot
            });
            let output = '';
            let errorOutput = '';
            ergogenProcess.stdout?.on('data', (data) => {
                output += data.toString();
                console.log(`Ergogen: ${data}`);
            });
            ergogenProcess.stderr?.on('data', (data) => {
                errorOutput += data.toString();
                console.error(`Ergogen Error: ${data}`);
            });
            ergogenProcess.on('close', (code) => {
                if (code === 0) {
                    vscode.window.showInformationMessage('✅ Ergogen completed successfully! DXF viewer should refresh automatically.');
                    resolve();
                }
                else {
                    vscode.window.showErrorMessage(`❌ Ergogen failed with code ${code}. Check terminal for details.`);
                    if (errorOutput) {
                        console.error('Ergogen error output:', errorOutput);
                    }
                    reject(new Error(`Ergogen failed with code ${code}`));
                }
            });
            ergogenProcess.on('error', (error) => {
                vscode.window.showErrorMessage(`❌ Failed to run ergogen: ${error.message}`);
                reject(error);
            });
        });
    });
}
function deactivate() {
    // Nothing to clean up
}
exports.deactivate = deactivate;
