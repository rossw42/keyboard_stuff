const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Import modules
const DxfParser = require('./dxfParser');
const WebviewContent = require('./webviewContent');
const ConnectionDiagramGenerator = require('./connectionDiagramGenerator');

// Global state
let currentPanel = undefined;
let fileWatcher = null;
let outputChannel = null;
let statusBarItem = null;

// Extension state
const state = {
    lastActiveYamlFile: null,
    currentOutputDir: null,
    isProcessing: false
};

/**
 * Extension activation
 */
function activate(context) {
    console.log('🚀 Ergogen Toolkit v2.0.0 activating...');
    
    // Create output channel for logging
    outputChannel = vscode.window.createOutputChannel('Ergogen Toolkit');
    outputChannel.appendLine('Extension activated');
    
    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = '$(eye) DXF';
    statusBarItem.tooltip = 'Ergogen Toolkit';
    statusBarItem.command = 'ergogen-toolkit.openViewer';
    context.subscriptions.push(statusBarItem);
    
    // Register commands
    registerCommands(context);
    
    // Register event listeners
    registerEventListeners(context);
    
    // Auto-detect workspace
    detectWorkspace();
    
    // Show status bar if YAML files exist
    if (hasYamlFiles()) {
        statusBarItem.show();
    }
    
    vscode.window.showInformationMessage('🎹 Ergogen Toolkit ready!');
}

/**
 * Register all extension commands
 */
function registerCommands(context) {
    // Open viewer command
    context.subscriptions.push(
        vscode.commands.registerCommand('ergogen-toolkit.openViewer', () => {
            createOrShowPanel(context);
        })
    );
    
    // Run Ergogen command
    context.subscriptions.push(
        vscode.commands.registerCommand('ergogen-toolkit.runErgogen', async () => {
            await runErgogen();
        })
    );
    
    // Refresh viewer command
    context.subscriptions.push(
        vscode.commands.registerCommand('ergogen-toolkit.refreshViewer', () => {
            refreshViewer();
        })
    );
    
    // Fit to window command
    context.subscriptions.push(
        vscode.commands.registerCommand('ergogen-toolkit.fitToWindow', () => {
            if (currentPanel) {
                currentPanel.webview.postMessage({ command: 'fitToWindow' });
            }
        })
    );
    
    // Generate connection diagram command
    context.subscriptions.push(
        vscode.commands.registerCommand('ergogen-toolkit.generateConnectionDiagram', async () => {
            await generateConnectionDiagram();
        })
    );
}

/**
 * Register event listeners
 */
function registerEventListeners(context) {
    // Track active editor changes
    context.subscriptions.push(
        vscode.window.onDidChangeActiveTextEditor(editor => {
            if (editor && isYamlFile(editor.document.fileName)) {
                updateLastYamlFile(editor.document.fileName);
                statusBarItem.show();
            }
        })
    );
    
    // Auto-run on save if configured
    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(document => {
            const config = vscode.workspace.getConfiguration('ergogen-toolkit');
            if (config.get('autoRunErgogen') && isYamlFile(document.fileName)) {
                runErgogen();
            }
        })
    );
    
    // Configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('ergogen-toolkit')) {
                if (currentPanel) {
                    updateWebviewConfiguration();
                }
            }
        })
    );
}

/**
 * Run Ergogen command
 */
async function runErgogen() {
    if (state.isProcessing) {
        vscode.window.showWarningMessage('⏳ Ergogen is already running...');
        return;
    }
    
    state.isProcessing = true;
    outputChannel.clear();
    outputChannel.show();
    outputChannel.appendLine('🔄 Running Ergogen...');
    
    try {
        const yamlFile = await getYamlFile();
        if (!yamlFile) {
            throw new Error('No YAML file found');
        }
        
        const workingDir = path.dirname(yamlFile.filePath);
        const config = vscode.workspace.getConfiguration('ergogen-toolkit');
        const ergogenCmd = config.get('ergogenCommand', 'ergogen');
        
        // Create output directory based on filename
        const yamlBaseName = path.basename(yamlFile.fileName, path.extname(yamlFile.fileName));
        const outputDir = path.join(workingDir, yamlBaseName);
        
        const args = ['-o', outputDir, yamlFile.fileName];
        
        outputChannel.appendLine(`Command: ${ergogenCmd} ${args.join(' ')}`);
        outputChannel.appendLine(`Working directory: ${workingDir}`);
        outputChannel.appendLine(`Output directory: ${outputDir}`);
        
        // Show progress
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Running Ergogen",
            cancellable: true
        }, async (progress, token) => {
            return new Promise((resolve, reject) => {
                const ergogenProcess = spawn(ergogenCmd, args, {
                    cwd: workingDir,
                    shell: true
                });
                
                let output = '';
                let errorOutput = '';
                
                ergogenProcess.stdout.on('data', (data) => {
                    output += data.toString();
                    outputChannel.append(data.toString());
                });
                
                ergogenProcess.stderr.on('data', (data) => {
                    errorOutput += data.toString();
                    outputChannel.append(data.toString());
                });
                
                ergogenProcess.on('close', async (code) => {
                    state.isProcessing = false;
                    
                    if (code === 0) {
                        outputChannel.appendLine('✅ Ergogen completed successfully!');
                        
                        // Generate connection diagram if enabled
                        const config = vscode.workspace.getConfiguration('ergogen-toolkit');
                        if (config.get('generateConnectionDiagram', true)) {
                            outputChannel.appendLine('📊 Generating connection diagram...');
                            try {
                                const diagramGenerator = new ConnectionDiagramGenerator();
                                const result = await diagramGenerator.generateFromFile(yamlFile.filePath, outputDir);
                                
                                if (result.success) {
                                    outputChannel.appendLine(`✅ Connection diagram generated: ${result.outputPath}`);
                                } else {
                                    outputChannel.appendLine(`⚠️ Connection diagram generation failed: ${result.error}`);
                                }
                            } catch (error) {
                                outputChannel.appendLine(`⚠️ Connection diagram generation error: ${error.message}`);
                            }
                        }
                        
                        vscode.window.showInformationMessage('✅ Ergogen completed!');
                        
                        // Set up file watching for the filename-based output directory
                        setupFileWatching(outputDir);
                        
                        // Refresh viewer
                        if (currentPanel) {
                            refreshViewer();
                        }
                        
                        resolve();
                    } else {
                        outputChannel.appendLine(`❌ Ergogen failed with code ${code}`);
                        vscode.window.showErrorMessage(`❌ Ergogen failed! Check output for details.`);
                        reject(new Error(`Ergogen failed with code ${code}`));
                    }
                });
                
                ergogenProcess.on('error', (error) => {
                    state.isProcessing = false;
                    outputChannel.appendLine(`❌ Error: ${error.message}`);
                    vscode.window.showErrorMessage(`❌ Failed to run ergogen: ${error.message}`);
                    reject(error);
                });
                
                // Handle cancellation
                token.onCancellationRequested(() => {
                    ergogenProcess.kill();
                    state.isProcessing = false;
                    outputChannel.appendLine('⚠️ Ergogen cancelled by user');
                });
            });
        });
        
    } catch (error) {
        state.isProcessing = false;
        outputChannel.appendLine(`❌ Error: ${error.message}`);
        vscode.window.showErrorMessage(`❌ Error: ${error.message}`);
    }
}

/**
 * Generate connection diagram manually
 */
async function generateConnectionDiagram() {
    try {
        outputChannel.clear();
        outputChannel.show();
        outputChannel.appendLine('📊 Generating connection diagram...');
        
        const yamlFile = await getYamlFile();
        if (!yamlFile) {
            throw new Error('No YAML file found. Please open an Ergogen YAML file.');
        }
        
        // Determine output directory
        const outputDir = getOutputDirectory() || path.dirname(yamlFile.filePath);
        
        // Generate diagram
        const diagramGenerator = new ConnectionDiagramGenerator();
        const result = await diagramGenerator.generateFromFile(yamlFile.filePath, outputDir);
        
        if (result.success) {
            outputChannel.appendLine(`✅ Connection diagram generated: ${result.outputPath}`);
            
            // Show the generated file
            const doc = await vscode.workspace.openTextDocument(result.outputPath);
            await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
            
            vscode.window.showInformationMessage('✅ Connection diagram generated successfully!');
        } else {
            outputChannel.appendLine(`❌ Connection diagram generation failed: ${result.error}`);
            vscode.window.showErrorMessage(`❌ Failed to generate connection diagram: ${result.error}`);
        }
        
    } catch (error) {
        outputChannel.appendLine(`❌ Error: ${error.message}`);
        vscode.window.showErrorMessage(`❌ Error: ${error.message}`);
    }
}

/**
 * Create or show the webview panel
 */
function createOrShowPanel(context) {
    if (currentPanel) {
        currentPanel.reveal(vscode.ViewColumn.Beside);
        return;
    }
    
    // Create panel
    currentPanel = vscode.window.createWebviewPanel(
        'ergogenToolkit',
        'DXF Viewer',
        vscode.ViewColumn.Beside,
        {
            enableScripts: true,
            retainContextWhenHidden: true,
            localResourceRoots: []
        }
    );
    
    // Set icon
    currentPanel.iconPath = {
        light: vscode.Uri.file(path.join(__dirname, 'media', 'icon-light.svg')),
        dark: vscode.Uri.file(path.join(__dirname, 'media', 'icon-dark.svg'))
    };
    
    // Set content
    updateWebviewContent();
    
    // Handle messages
    currentPanel.webview.onDidReceiveMessage(
        async message => {
            switch (message.command) {
                case 'runErgogen':
                    await runErgogen();
                    break;
                case 'refreshFiles':
                    refreshViewer();
                    break;
                case 'loadFile':
                    await loadDxfFile(message.filename);
                    break;
                case 'log':
                    outputChannel.appendLine(`[Webview] ${message.text}`);
                    break;
                case 'error':
                    outputChannel.appendLine(`[Webview Error] ${message.text}`);
                    vscode.window.showErrorMessage(message.text);
                    break;
            }
        },
        undefined,
        context.subscriptions
    );
    
    // Handle disposal
    currentPanel.onDidDispose(() => {
        currentPanel = undefined;
        if (fileWatcher) {
            fileWatcher.dispose();
            fileWatcher = null;
        }
    });
    
    // Initial refresh
    refreshViewer();
}

/**
 * Update webview content
 */
function updateWebviewContent() {
    if (!currentPanel) return;
    
    const config = vscode.workspace.getConfiguration('ergogen-toolkit');
    currentPanel.webview.html = WebviewContent.getHtml(config);
}

/**
 * Update webview configuration
 */
function updateWebviewConfiguration() {
    if (!currentPanel) return;
    
    const config = vscode.workspace.getConfiguration('ergogen-toolkit');
    currentPanel.webview.postMessage({
        command: 'updateConfig',
        config: {
            theme: config.get('theme'),
            lineWidth: config.get('lineWidth'),
            gridEnabled: config.get('gridEnabled')
        }
    });
}

/**
 * Refresh the viewer with current files
 */
function refreshViewer() {
    if (!currentPanel) return;
    
    const outputDir = getOutputDirectory();
    if (!outputDir || !fs.existsSync(outputDir)) {
        currentPanel.webview.postMessage({
            command: 'updateFileList',
            files: [],
            error: 'Output directory not found. Run Ergogen first.'
        });
        return;
    }
    
    const files = scanForDxfFiles(outputDir);
    currentPanel.webview.postMessage({
        command: 'updateFileList',
        files: files,
        outputDir: outputDir
    });
    
    outputChannel.appendLine(`📁 Found ${files.length} DXF files in ${outputDir}`);
}

/**
 * Load and parse a DXF file
 */
async function loadDxfFile(filename) {
    if (!currentPanel) return;
    
    const outputDir = getOutputDirectory();
    if (!outputDir) {
        currentPanel.webview.postMessage({
            command: 'displayError',
            filename: filename,
            error: 'Output directory not found'
        });
        return;
    }
    
    try {
        // Find the file in the scanned files list to get the correct path
        const files = scanForDxfFiles(outputDir);
        const fileInfo = files.find(f => f.name === filename);
        
        if (!fileInfo) {
            throw new Error(`File not found in scan results: ${filename}`);
        }
        
        const filePath = fileInfo.fullPath;
        if (!fs.existsSync(filePath)) {
            throw new Error(`File not found: ${filePath}`);
        }
        
        const content = fs.readFileSync(filePath, 'utf8');
        const parsedData = DxfParser.parse(content);
        
        currentPanel.webview.postMessage({
            command: 'displayDxf',
            filename: filename,
            data: parsedData
        });
        
        outputChannel.appendLine(`✅ Loaded ${filename}: ${parsedData.entities.length} entities`);
        
    } catch (error) {
        outputChannel.appendLine(`❌ Error loading ${filename}: ${error.message}`);
        currentPanel.webview.postMessage({
            command: 'displayError',
            filename: filename,
            error: error.message
        });
    }
}

/**
 * Set up file watching for DXF files
 */
function setupFileWatching(outputDir) {
    if (!fs.existsSync(outputDir)) {
        return;
    }
    
    state.currentOutputDir = outputDir;
    
    // Dispose existing watcher
    if (fileWatcher) {
        fileWatcher.dispose();
    }
    
    // Create new watcher
    const pattern = new vscode.RelativePattern(outputDir, '**/*.dxf');
    fileWatcher = vscode.workspace.createFileSystemWatcher(pattern);
    
    const config = vscode.workspace.getConfiguration('ergogen-toolkit');
    if (config.get('autoRefresh')) {
        fileWatcher.onDidCreate(() => refreshViewer());
        fileWatcher.onDidChange(() => refreshViewer());
        fileWatcher.onDidDelete(() => refreshViewer());
    }
    
    outputChannel.appendLine(`👁️ Watching for DXF files in: ${outputDir}`);
}

/**
 * Utility functions
 */

function detectWorkspace() {
    const activeEditor = vscode.window.activeTextEditor;
    if (activeEditor && isYamlFile(activeEditor.document.fileName)) {
        updateLastYamlFile(activeEditor.document.fileName);
    } else {
        // Look for YAML files in workspace
        if (vscode.workspace.workspaceFolders) {
            const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
            const commonFiles = ['keyboard.yaml', 'config.yaml', 'ergogen.yaml'];
            
            for (const file of commonFiles) {
                const filePath = path.join(workspaceRoot, file);
                if (fs.existsSync(filePath)) {
                    updateLastYamlFile(filePath);
                    break;
                }
            }
        }
    }
}

function isYamlFile(filename) {
    return filename.endsWith('.yaml') || filename.endsWith('.yml');
}

function hasYamlFiles() {
    if (!vscode.workspace.workspaceFolders) return false;
    
    const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
    const files = fs.readdirSync(workspaceRoot);
    return files.some(file => isYamlFile(file));
}

function updateLastYamlFile(filePath) {
    state.lastActiveYamlFile = {
        fileName: path.basename(filePath),
        filePath: filePath,
        workingDir: path.dirname(filePath)
    };
}

async function getYamlFile() {
    // Check active editor first
    const activeEditor = vscode.window.activeTextEditor;
    if (activeEditor && isYamlFile(activeEditor.document.fileName)) {
        updateLastYamlFile(activeEditor.document.fileName);
        return state.lastActiveYamlFile;
    }
    
    // Use last known YAML file
    if (state.lastActiveYamlFile) {
        return state.lastActiveYamlFile;
    }
    
    // Prompt user to select
    const files = await vscode.window.showQuickPick(
        findYamlFiles(),
        { placeHolder: 'Select an Ergogen YAML file' }
    );
    
    if (files) {
        updateLastYamlFile(files);
        return state.lastActiveYamlFile;
    }
    
    return null;
}

function findYamlFiles() {
    if (!vscode.workspace.workspaceFolders) return [];
    
    const files = [];
    const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
    
    function scanDir(dir, depth = 0) {
        if (depth > 3) return; // Limit depth
        
        try {
            const items = fs.readdirSync(dir);
            for (const item of items) {
                const fullPath = path.join(dir, item);
                const stat = fs.statSync(fullPath);
                
                if (stat.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
                    scanDir(fullPath, depth + 1);
                } else if (isYamlFile(item)) {
                    files.push(fullPath);
                }
            }
        } catch (error) {
            // Ignore errors
        }
    }
    
    scanDir(workspaceRoot);
    return files;
}

function getOutputDirectory() {
    if (state.currentOutputDir && fs.existsSync(state.currentOutputDir)) {
        return state.currentOutputDir;
    }
    
    if (state.lastActiveYamlFile) {
        const workingDir = state.lastActiveYamlFile.workingDir;
        
        // Primary: filename-based directory (what the extension creates)
        const yamlBaseName = path.basename(state.lastActiveYamlFile.fileName, path.extname(state.lastActiveYamlFile.fileName));
        const filenameDir = path.join(workingDir, yamlBaseName);
        if (fs.existsSync(filenameDir)) {
            return filenameDir;
        }
        
        // Fallback: meta.name from YAML file
        const projectName = getProjectNameFromYaml(state.lastActiveYamlFile.filePath);
        if (projectName) {
            const projectDir = path.join(workingDir, projectName);
            if (fs.existsSync(projectDir)) {
                return projectDir;
            }
        }
        
        // Final fallback: simple output directory
        const config = vscode.workspace.getConfiguration('ergogen-toolkit');
        const outputDirName = config.get('outputDirectory', 'output');
        const simpleOutputDir = path.join(workingDir, outputDirName);
        if (fs.existsSync(simpleOutputDir)) {
            return simpleOutputDir;
        }
    }
    
    return null;
}

/**
 * Extract project name from YAML file's meta.name field
 */
function getProjectNameFromYaml(yamlFilePath) {
    try {
        const content = fs.readFileSync(yamlFilePath, 'utf8');
        
        // Simple regex to extract meta.name (works for most YAML structures)
        const metaNameMatch = content.match(/^\s*name:\s*(.+)$/m);
        if (metaNameMatch) {
            return metaNameMatch[1].trim().replace(/['"]/g, ''); // Remove quotes if present
        }
        
        // Alternative pattern for nested meta structure
        const lines = content.split('\n');
        let inMeta = false;
        for (const line of lines) {
            const trimmed = line.trim();
            if (trimmed === 'meta:') {
                inMeta = true;
                continue;
            }
            if (inMeta) {
                if (trimmed.startsWith('name:')) {
                    const name = trimmed.substring(5).trim().replace(/['"]/g, '');
                    return name;
                }
                // Exit meta section if we hit another top-level key
                if (line.match(/^[a-zA-Z]/)) {
                    break;
                }
            }
        }
    } catch (error) {
        outputChannel.appendLine(`Warning: Could not parse YAML file for project name: ${error.message}`);
    }
    
    return null;
}

function scanForDxfFiles(dir) {
    const files = [];
    
    function scan(currentDir, relativePath = '') {
        try {
            const items = fs.readdirSync(currentDir);
            for (const item of items) {
                const fullPath = path.join(currentDir, item);
                const relPath = path.join(relativePath, item);
                
                if (fs.statSync(fullPath).isDirectory()) {
                    scan(fullPath, relPath);
                } else if (item.toLowerCase().endsWith('.dxf')) {
                    files.push({
                        name: item,
                        path: relPath,
                        fullPath: fullPath,
                        size: fs.statSync(fullPath).size,
                        modified: fs.statSync(fullPath).mtime
                    });
                }
            }
        } catch (error) {
            outputChannel.appendLine(`Error scanning ${currentDir}: ${error.message}`);
        }
    }
    
    scan(dir);
    return files.sort((a, b) => a.path.localeCompare(b.path));
}

/**
 * Extension deactivation
 */
function deactivate() {
    if (currentPanel) {
        currentPanel.dispose();
    }
    if (fileWatcher) {
        fileWatcher.dispose();
    }
    if (outputChannel) {
        outputChannel.dispose();
    }
    if (statusBarItem) {
        statusBarItem.dispose();
    }
}

module.exports = {
    activate,
    deactivate
};
