const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

// Global variables
let currentPanel = undefined;
let lastActiveYamlFile = null;
let fileWatcher = null;
let currentOutputDir = null;

function activate(context) {
    console.log('🚀 Self-contained DXF Viewer extension activating...');
    vscode.window.showInformationMessage('🎹 DXF Viewer extension loaded!');
    
    // Test command
    const testCommand = vscode.commands.registerCommand('ergogen-dxf-viewer.test', () => {
        vscode.window.showInformationMessage('✅ Test command works!');
    });
    
    // Run Ergogen command
    const runErgogenCommand = vscode.commands.registerCommand('ergogen-dxf-viewer.runErgogen', async () => {
        vscode.window.showInformationMessage('🔄 Starting Ergogen...');
        
        try {
            if (!vscode.workspace.workspaceFolders) {
                vscode.window.showErrorMessage('No workspace folder found');
                return;
            }

            const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
            const { spawn } = require('child_process');
            
            let yamlFile = null;
            let workingDir = workspaceRoot;
            
            // Get active YAML file or use remembered one
            const activeEditor = vscode.window.activeTextEditor;
            if (activeEditor) {
                const activeFile = activeEditor.document.fileName;
                const fileName = path.basename(activeFile);
                const fileDir = path.dirname(activeFile);
                
                if (fileName.endsWith('.yaml') || fileName.endsWith('.yml')) {
                    yamlFile = fileName;
                    workingDir = fileDir;
                    // Remember this file
                    lastActiveYamlFile = {
                        fileName: fileName,
                        filePath: activeFile,
                        workingDir: fileDir
                    };
                }
            } else if (lastActiveYamlFile) {
                yamlFile = lastActiveYamlFile.fileName;
                workingDir = lastActiveYamlFile.workingDir;
            }
            
            // Fallback to keyboard.yaml in workspace root
            if (!yamlFile) {
                if (fs.existsSync(path.join(workspaceRoot, 'keyboard.yaml'))) {
                    yamlFile = 'keyboard.yaml';
                    workingDir = workspaceRoot;
                }
            }
            
            if (!yamlFile) {
                vscode.window.showErrorMessage('❌ No YAML file found. Please open a YAML file or ensure keyboard.yaml exists in your workspace.');
                return;
            }
            
            console.log(`Running: ergogen ${yamlFile} in ${workingDir}`);
            
            const ergogenProcess = spawn('ergogen', [yamlFile], {
                cwd: workingDir,
                stdio: ['pipe', 'pipe', 'pipe']
            });

            let output = '';
            let errorOutput = '';

            ergogenProcess.stdout.on('data', (data) => {
                output += data.toString();
            });

            ergogenProcess.stderr.on('data', (data) => {
                errorOutput += data.toString();
            });

            ergogenProcess.on('close', (code) => {
                if (code === 0) {
                    vscode.window.showInformationMessage('✅ Ergogen completed successfully!');
                    // Set up file watching for the output directory
                    setupFileWatching(path.join(workingDir, 'output'));
                    // Refresh the viewer if it's open
                    if (currentPanel) {
                        refreshDxfViewer();
                    }
                } else {
                    vscode.window.showErrorMessage(`❌ Ergogen failed with code ${code}`);
                    console.log('Error output:', errorOutput);
                }
            });

            ergogenProcess.on('error', (error) => {
                vscode.window.showErrorMessage(`❌ Failed to run ergogen: ${error.message}`);
            });
            
        } catch (error) {
            vscode.window.showErrorMessage(`❌ Error: ${error.message}`);
        }
    });
    
    // Open viewer command
    const openViewerCommand = vscode.commands.registerCommand('ergogen-dxf-viewer.openViewer', () => {
        createDxfViewerPanel(context);
    });

    // Track active editor changes
    const editorChangeListener = vscode.window.onDidChangeActiveTextEditor(editor => {
        if (editor && editor.document) {
            const fileName = editor.document.fileName;
            if (fileName.endsWith('.yaml') || fileName.endsWith('.yml')) {
                lastActiveYamlFile = {
                    fileName: path.basename(fileName),
                    filePath: fileName,
                    workingDir: path.dirname(fileName)
                };
            }
        }
    });

    context.subscriptions.push(testCommand, runErgogenCommand, openViewerCommand, editorChangeListener);
    
    console.log('✅ Self-contained DXF Viewer extension activated successfully');
    vscode.window.showInformationMessage('🚀 DXF Viewer ready!');
}

// Detect the active YAML file for determining output directory
function detectActiveYamlFile() {
    // First, try the currently active editor
    const activeEditor = vscode.window.activeTextEditor;
    if (activeEditor) {
        const activeFile = activeEditor.document.fileName;
        const fileName = path.basename(activeFile);
        const fileDir = path.dirname(activeFile);
        
        if (fileName.endsWith('.yaml') || fileName.endsWith('.yml')) {
            lastActiveYamlFile = {
                fileName: fileName,
                filePath: activeFile,
                workingDir: fileDir
            };
            console.log(`Detected active YAML file: ${fileName} in ${fileDir}`);
            return;
        }
    }
    
    // If no active YAML file, look for common YAML files in workspace
    if (vscode.workspace.workspaceFolders) {
        const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
        const commonYamlFiles = ['keyboard.yaml', 'config.yaml', 'ergogen.yaml'];
        
        for (const yamlFile of commonYamlFiles) {
            const yamlPath = path.join(workspaceRoot, yamlFile);
            if (fs.existsSync(yamlPath)) {
                lastActiveYamlFile = {
                    fileName: yamlFile,
                    filePath: yamlPath,
                    workingDir: workspaceRoot
                };
                console.log(`Found YAML file: ${yamlFile} in workspace root`);
                return;
            }
        }
        
        // Look for any .yaml files in the workspace root
        try {
            const files = fs.readdirSync(workspaceRoot);
            for (const file of files) {
                if (file.endsWith('.yaml') || file.endsWith('.yml')) {
                    const yamlPath = path.join(workspaceRoot, file);
                    lastActiveYamlFile = {
                        fileName: file,
                        filePath: yamlPath,
                        workingDir: workspaceRoot
                    };
                    console.log(`Found YAML file: ${file} in workspace root`);
                    return;
                }
            }
        } catch (error) {
            console.log('Error scanning workspace for YAML files:', error);
        }
    }
}

// Create the DXF viewer panel
function createDxfViewerPanel(context) {
    if (currentPanel) {
        currentPanel.reveal(vscode.ViewColumn.Beside);
        return;
    }

    currentPanel = vscode.window.createWebviewPanel(
        'dxfViewer',
        'DXF Viewer',
        vscode.ViewColumn.Beside,
        {
            enableScripts: true,
            retainContextWhenHidden: true,
            localResourceRoots: []
        }
    );

    // Set initial content
    currentPanel.webview.html = getWebviewContent();

    // Handle messages from webview
    currentPanel.webview.onDidReceiveMessage(
        async message => {
            switch (message.command) {
                case 'runErgogen':
                    vscode.commands.executeCommand('ergogen-dxf-viewer.runErgogen');
                    break;
                case 'refreshFiles':
                    refreshDxfViewer();
                    break;
                case 'selectFile':
                    await loadAndSendDxfFile(message.filename);
                    break;
            }
        },
        undefined,
        context.subscriptions
    );

    // Handle panel disposal
    currentPanel.onDidDispose(() => {
        currentPanel = undefined;
        if (fileWatcher) {
            fileWatcher.dispose();
            fileWatcher = null;
        }
    });

    // Detect active YAML file and initial file scan
    detectActiveYamlFile();
    refreshDxfViewer();
}

// Set up file watching for DXF files
function setupFileWatching(outputDir) {
    if (!fs.existsSync(outputDir)) {
        return;
    }

    currentOutputDir = outputDir;

    // Dispose existing watcher
    if (fileWatcher) {
        fileWatcher.dispose();
    }

    // Create new file watcher
    const pattern = new vscode.RelativePattern(outputDir, '**/*.dxf');
    fileWatcher = vscode.workspace.createFileSystemWatcher(pattern);

    fileWatcher.onDidCreate(() => refreshDxfViewer());
    fileWatcher.onDidChange(() => refreshDxfViewer());
    fileWatcher.onDidDelete(() => refreshDxfViewer());

    console.log(`📁 Watching for DXF files in: ${outputDir}`);
}

// Refresh the DXF viewer with current files
function refreshDxfViewer() {
    if (!currentPanel) return;

    // Determine output directory
    let outputDir = currentOutputDir;
    
    // Try to detect current YAML file if we don't have one remembered
    if (!outputDir && !lastActiveYamlFile) {
        detectActiveYamlFile();
    }
    
    if (!outputDir && lastActiveYamlFile) {
        outputDir = path.join(lastActiveYamlFile.workingDir, 'output');
        console.log(`📁 Using output dir relative to YAML: ${outputDir}`);
    } else if (!outputDir && vscode.workspace.workspaceFolders) {
        // Check for ergogen directory structure
        const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
        const ergogenMacropadOutput = path.join(workspaceRoot, 'ergogen', 'keyboards', 'macropad', 'output');
        if (fs.existsSync(ergogenMacropadOutput)) {
            outputDir = ergogenMacropadOutput;
            console.log(`📁 Found ergogen macropad output: ${outputDir}`);
        } else {
            outputDir = path.join(workspaceRoot, 'output');
            console.log(`📁 Using workspace root output: ${outputDir}`);
        }
    }

    if (!outputDir || !fs.existsSync(outputDir)) {
        currentPanel.webview.postMessage({
            command: 'updateFileList',
            files: [],
            error: 'Output directory not found'
        });
        return;
    }

    // Scan for DXF files
    try {
        const files = scanForDxfFiles(outputDir);
        currentPanel.webview.postMessage({
            command: 'updateFileList',
            files: files,
            outputDir: outputDir
        });
    } catch (error) {
        currentPanel.webview.postMessage({
            command: 'updateFileList',
            files: [],
            error: error.message
        });
    }
}

// Scan directory for DXF files
function scanForDxfFiles(dir) {
    const files = [];
    
    function scanRecursive(currentDir, relativePath = '') {
        try {
            const items = fs.readdirSync(currentDir);
            for (const item of items) {
                const fullPath = path.join(currentDir, item);
                const relativeFilePath = path.join(relativePath, item);
                
                if (fs.statSync(fullPath).isDirectory()) {
                    scanRecursive(fullPath, relativeFilePath);
                } else if (item.toLowerCase().endsWith('.dxf')) {
                    files.push({
                        name: item,
                        path: relativeFilePath,
                        fullPath: fullPath
                    });
                }
            }
        } catch (error) {
            console.log(`Error scanning directory ${currentDir}:`, error);
        }
    }
    
    scanRecursive(dir);
    return files;
}

// Load and parse a DXF file, then send to webview
async function loadAndSendDxfFile(filename) {
    if (!currentPanel) return;

    console.log(`🔍 Loading DXF file: ${filename}`);

    // Determine output directory if not set
    let outputDir = currentOutputDir;
    if (!outputDir && lastActiveYamlFile) {
        outputDir = path.join(lastActiveYamlFile.workingDir, 'output');
    } else if (!outputDir && vscode.workspace.workspaceFolders) {
        outputDir = path.join(vscode.workspace.workspaceFolders[0].uri.fsPath, 'output');
    }

    if (!outputDir) {
        console.error('❌ Output directory not found');
        currentPanel.webview.postMessage({
            command: 'displayError',
            filename: filename,
            error: 'Output directory not found'
        });
        return;
    }

    try {
        // The filename passed is already a relative path (e.g., "outlines/plate.dxf")
        // So we just need to join it with the output directory
        const filePath = path.join(outputDir, filename);
        console.log(`📁 Full file path: ${filePath}`);
        
        if (!fs.existsSync(filePath)) {
            throw new Error(`File not found: ${filePath}`);
        }

        const dxfContent = fs.readFileSync(filePath, 'utf8');
        console.log(`📄 DXF content loaded, length: ${dxfContent.length} characters`);
        
        const parsedData = parseDxfContent(dxfContent);
        console.log(`✅ Parsed ${parsedData.entities.length} entities`);
        console.log(`📊 Bounds: x[${parsedData.bounds.min_x.toFixed(2)}, ${parsedData.bounds.max_x.toFixed(2)}] y[${parsedData.bounds.min_y.toFixed(2)}, ${parsedData.bounds.max_y.toFixed(2)}]`);
        
        // Log entity types for debugging
        const entityTypes = {};
        parsedData.entities.forEach(e => {
            entityTypes[e.type] = (entityTypes[e.type] || 0) + 1;
        });
        console.log('📈 Entity breakdown:', entityTypes);

        console.log('📤 Sending parsed data to webview...');
        currentPanel.webview.postMessage({
            command: 'displayDxf',
            filename: filename,
            data: parsedData
        });
        console.log('✅ Data sent to webview');

    } catch (error) {
        console.error(`❌ Error loading DXF file: ${error.message}`);
        currentPanel.webview.postMessage({
            command: 'displayError',
            filename: filename,
            error: error.message
        });
    }
}

// Simple DXF parser (converted from Python logic)
function parseDxfContent(content) {
    const lines = content.split('\n').map(line => line.trim()).filter(line => line);
    const entities = [];
    let bounds = { min_x: Infinity, min_y: Infinity, max_x: -Infinity, max_y: -Infinity };

    let i = 0;
    while (i < lines.length) {
        if (lines[i] === '0' && i + 1 < lines.length) {
            const entityType = lines[i + 1];
            
            if (entityType === 'LINE') {
                const entity = parseLine(lines, i);
                if (entity) {
                    entities.push(entity);
                    updateBounds(bounds, entity.start);
                    updateBounds(bounds, entity.end);
                }
            } else if (entityType === 'CIRCLE') {
                const entity = parseCircle(lines, i);
                if (entity) {
                    entities.push(entity);
                    updateBounds(bounds, { 
                        x: entity.center.x - entity.radius, 
                        y: entity.center.y - entity.radius 
                    });
                    updateBounds(bounds, { 
                        x: entity.center.x + entity.radius, 
                        y: entity.center.y + entity.radius 
                    });
                }
            } else if (entityType === 'ARC') {
                const entity = parseArc(lines, i);
                if (entity) {
                    entities.push(entity);
                    updateBounds(bounds, { 
                        x: entity.center.x - entity.radius, 
                        y: entity.center.y - entity.radius 
                    });
                    updateBounds(bounds, { 
                        x: entity.center.x + entity.radius, 
                        y: entity.center.y + entity.radius 
                    });
                }
            } else if (entityType === 'LWPOLYLINE' || entityType === 'POLYLINE') {
                const entity = parsePolyline(lines, i);
                if (entity && entity.points) {
                    entities.push(entity);
                    entity.points.forEach(point => updateBounds(bounds, point));
                }
            }
        }
        i++;
    }

    // Handle empty bounds
    if (bounds.min_x === Infinity) {
        bounds = { min_x: 0, min_y: 0, max_x: 100, max_y: 100 };
    }

    return {
        entities: entities,
        entity_count: entities.length,
        bounds: bounds
    };
}

// Helper functions for DXF parsing
function parseLine(lines, startIndex) {
    let x1, y1, x2, y2;
    
    for (let i = startIndex; i < Math.min(startIndex + 50, lines.length - 1); i++) {
        const code = lines[i];
        const value = lines[i + 1];
        
        if (code === '10') x1 = parseFloat(value);
        else if (code === '20') y1 = parseFloat(value);
        else if (code === '11') x2 = parseFloat(value);
        else if (code === '21') y2 = parseFloat(value);
        else if (code === '0' && i > startIndex) break;
    }
    
    if (x1 !== undefined && y1 !== undefined && x2 !== undefined && y2 !== undefined) {
        return {
            type: 'line',
            start: { x: x1, y: y1 },
            end: { x: x2, y: y2 }
        };
    }
    return null;
}

function parseCircle(lines, startIndex) {
    let cx, cy, radius;
    
    for (let i = startIndex; i < Math.min(startIndex + 50, lines.length - 1); i++) {
        const code = lines[i];
        const value = lines[i + 1];
        
        if (code === '10') cx = parseFloat(value);
        else if (code === '20') cy = parseFloat(value);
        else if (code === '40') radius = parseFloat(value);
        else if (code === '0' && i > startIndex) break;
    }
    
    if (cx !== undefined && cy !== undefined && radius !== undefined) {
        return {
            type: 'circle',
            center: { x: cx, y: cy },
            radius: radius
        };
    }
    return null;
}

function parseArc(lines, startIndex) {
    let cx, cy, radius, startAngle, endAngle;
    
    for (let i = startIndex; i < Math.min(startIndex + 50, lines.length - 1); i++) {
        const code = lines[i];
        const value = lines[i + 1];
        
        if (code === '10') cx = parseFloat(value);
        else if (code === '20') cy = parseFloat(value);
        else if (code === '40') radius = parseFloat(value);
        else if (code === '50') startAngle = parseFloat(value);
        else if (code === '51') endAngle = parseFloat(value);
        else if (code === '0' && i > startIndex) break;
    }
    
    if (cx !== undefined && cy !== undefined && radius !== undefined && 
        startAngle !== undefined && endAngle !== undefined) {
        return {
            type: 'arc',
            center: { x: cx, y: cy },
            radius: radius,
            start_angle: startAngle,
            end_angle: endAngle
        };
    }
    return null;
}

function parsePolyline(lines, startIndex) {
    const points = [];
    let closed = false;
    
    for (let i = startIndex; i < lines.length - 1; i++) {
        const code = lines[i];
        const value = lines[i + 1];
        
        if (code === '70') {
            closed = (parseInt(value) & 1) === 1;
        } else if (code === '10') {
            const x = parseFloat(value);
            // Look for the corresponding Y coordinate (code '20')
            let y = undefined;
            for (let j = i + 2; j < Math.min(i + 10, lines.length - 1); j += 2) {
                if (lines[j] === '20') {
                    y = parseFloat(lines[j + 1]);
                    break;
                }
            }
            if (!isNaN(x) && y !== undefined && !isNaN(y)) {
                points.push({ x: x, y: y });
            }
        } else if (code === '0' && i > startIndex) {
            break;
        }
    }
    
    if (points.length > 0) {
        return {
            type: 'polyline',
            points: points,
            closed: closed
        };
    }
    return null;
}

function updateBounds(bounds, point) {
    bounds.min_x = Math.min(bounds.min_x, point.x);
    bounds.min_y = Math.min(bounds.min_y, point.y);
    bounds.max_x = Math.max(bounds.max_x, point.x);
    bounds.max_y = Math.max(bounds.max_y, point.y);
}

// Generate the webview HTML content with complete canvas rendering
function getWebviewContent() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DXF Viewer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #1e1e1e; color: #cccccc; height: 100vh; display: flex; flex-direction: column; }
        .header { background: #252526; padding: 12px 16px; border-bottom: 1px solid #3c3c3c; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { font-size: 16px; font-weight: 600; color: #ffffff; }
        .controls { display: flex; gap: 8px; }
        .btn { background: #0e639c; color: #ffffff; border: 1px solid #007acc; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; transition: all 0.2s ease; }
        .btn:hover { background: #1177bb; box-shadow: 0 2px 4px rgba(0, 122, 204, 0.3); }
        .main { flex: 1; display: flex; overflow: hidden; }
        .sidebar { width: 250px; background: #2d2d30; border-right: 1px solid #3c3c3c; display: flex; flex-direction: column; }
        .sidebar-header { padding: 12px; border-bottom: 1px solid #3c3c3c; display: flex; justify-content: space-between; align-items: center; }
        .sidebar-header h3 { font-size: 14px; color: #ffffff; }
        .refresh-btn { background: #6c757d; color: white; border: none; padding: 4px 8px; border-radius: 3px; cursor: pointer; font-size: 11px; }
        .file-list { flex: 1; overflow-y: auto; padding: 8px; }
        .file-item { padding: 8px 12px; margin-bottom: 2px; background: #3c3c3c; border-radius: 4px; cursor: pointer; font-size: 13px; transition: background-color 0.2s; }
        .file-item:hover { background: #4a4a4a; }
        .file-item.selected { background: #0e639c; color: white; }
        .file-list.empty { display: flex; align-items: center; justify-content: center; color: #888888; font-style: italic; }
        .viewer { flex: 1; display: flex; flex-direction: column; background: #1e1e1e; }
        .viewer-header { padding: 12px 16px; border-bottom: 1px solid #3c3c3c; }
        .viewer-header h2 { font-size: 14px; color: #ffffff; }
        .canvas-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 16px; }
        .canvas-controls { margin-bottom: 12px; display: flex; gap: 12px; align-items: center; }
        .canvas-controls button { background: #007bff; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; }
        .canvas-controls button:hover { background: #0056b3; }
        .canvas-controls span { font-size: 12px; color: #cccccc; }
        canvas { border: 1px solid #3c3c3c; background: #2d2d30; cursor: grab; }
        canvas:active { cursor: grabbing; }
        .placeholder { color: #888888; font-size: 14px; text-align: center; }
        .error { color: #f48771; font-size: 14px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎹 DXF Viewer - Ergogen Workflow</h1>
        <div class="controls">
            <button class="btn" onclick="runErgogen()">🔄 Generate</button>
            <button class="btn" onclick="refreshFiles()">🔃 Refresh</button>
        </div>
    </div>
    <div class="main">
        <div class="sidebar">
            <div class="sidebar-header">
                <h3>DXF Files</h3>
                <button class="refresh-btn" onclick="refreshFiles()">↻</button>
            </div>
            <div id="fileList" class="file-list empty">
                <div class="placeholder">No DXF files found</div>
            </div>
        </div>
        <div class="viewer">
            <div class="viewer-header">
                <h2 id="currentFile">Select a DXF file to view</h2>
            </div>
            <div class="canvas-container">
                <div id="canvasControls" class="canvas-controls" style="display: none;">
                    <button onclick="fitToWindow()">Fit to Window</button>
                    <span id="zoomLevel">Zoom: 100%</span>
                </div>
                <canvas id="dxfCanvas" width="800" height="600" style="display: none;"></canvas>
                <div id="placeholder" class="placeholder">Select a DXF file from the sidebar to view it</div>
            </div>
        </div>
    </div>
    <script>
        const vscode = acquireVsCodeApi();
        let currentDxfData = null, transform = { scale: 1, offsetX: 0, offsetY: 0 }, isDragging = false, lastMousePos = { x: 0, y: 0 }, selectedFile = null;
        
        function runErgogen() { vscode.postMessage({ command: 'runErgogen' }); }
        function refreshFiles() { vscode.postMessage({ command: 'refreshFiles' }); }
        function selectFile(filename) { selectedFile = filename; updateFileSelection(); vscode.postMessage({ command: 'selectFile', filename: filename }); }
        
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'updateFileList': updateFileList(message.files, message.error); break;
                case 'displayDxf': displayDxf(message.filename, message.data); break;
                case 'displayError': displayError(message.filename, message.error); break;
            }
        });
        
        function updateFileList(files, error) {
            const fileList = document.getElementById('fileList');
            if (error) { fileList.className = 'file-list empty'; fileList.innerHTML = '<div class="error">' + error + '</div>'; return; }
            if (files.length === 0) { fileList.className = 'file-list empty'; fileList.innerHTML = '<div class="placeholder">No DXF files found</div>'; return; }
            fileList.className = 'file-list';
            fileList.innerHTML = files.map(file => '<div class="file-item" onclick="selectFile(\\"' + file.path + '\\")">' + file.path + '</div>').join('');
        }
        
        function updateFileSelection() {
            document.querySelectorAll('.file-item').forEach(item => {
                item.classList.toggle('selected', item.textContent === selectedFile);
            });
        }
        
        function displayDxf(filename, data) {
            currentDxfData = data;
            document.getElementById('currentFile').textContent = filename;
            document.getElementById('placeholder').style.display = 'none';
            document.getElementById('canvasControls').style.display = 'flex';
            document.getElementById('dxfCanvas').style.display = 'block';
            fitToWindow(); render();
        }
        
        function displayError(filename, error) {
            document.getElementById('currentFile').textContent = filename + ' (Error)';
            document.getElementById('placeholder').innerHTML = '<div class="error">Error: ' + error + '</div>';
            document.getElementById('placeholder').style.display = 'block';
            document.getElementById('canvasControls').style.display = 'none';
            document.getElementById('dxfCanvas').style.display = 'none';
        }
        
        function render() {
            if (!currentDxfData || !currentDxfData.entities) return;
            const canvas = document.getElementById('dxfCanvas'), ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const entities = currentDxfData.entities;
            if (entities.length === 0) { ctx.fillStyle = '#cccccc'; ctx.font = '16px Arial'; ctx.textAlign = 'center'; ctx.fillText('No entities found in DXF file', canvas.width / 2, canvas.height / 2); return; }
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = Math.max(1, 1 / transform.scale);
            ctx.lineCap = 'round';
            entities.forEach(entity => {
                ctx.beginPath();
                if (entity.type === 'line') {
                    ctx.moveTo(entity.start.x * transform.scale + transform.offsetX, canvas.height - (entity.start.y * transform.scale + transform.offsetY));
                    ctx.lineTo(entity.end.x * transform.scale + transform.offsetX, canvas.height - (entity.end.y * transform.scale + transform.offsetY));
                } else if (entity.type === 'circle') {
                    const centerX = entity.center.x * transform.scale + transform.offsetX;
                    const centerY = canvas.height - (entity.center.y * transform.scale + transform.offsetY);
                    const radius = entity.radius * transform.scale;
                    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
                } else if (entity.type === 'arc') {
                    const centerX = entity.center.x * transform.scale + transform.offsetX;
                    const centerY = canvas.height - (entity.center.y * transform.scale + transform.offsetY);
                    const radius = entity.radius * transform.scale;
                    const startAngle = -entity.end_angle * Math.PI / 180;
                    const endAngle = -entity.start_angle * Math.PI / 180;
                    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
                } else if (entity.type === 'polyline' && entity.points.length > 0) {
                    const firstPoint = entity.points[0];
                    ctx.moveTo(firstPoint.x * transform.scale + transform.offsetX, canvas.height - (firstPoint.y * transform.scale + transform.offsetY));
                    for (let i = 1; i < entity.points.length; i++) {
                        const point = entity.points[i];
                        ctx.lineTo(point.x * transform.scale + transform.offsetX, canvas.height - (point.y * transform.scale + transform.offsetY));
                    }
                    if (entity.closed) ctx.closePath();
                }
                ctx.stroke();
            });
            document.getElementById('zoomLevel').textContent = 'Zoom: ' + (transform.scale * 100).toFixed(0) + '%';
        }
        
        function fitToWindow() {
            if (!currentDxfData || !currentDxfData.bounds) return;
            const canvas = document.getElementById('dxfCanvas'), bounds = currentDxfData.bounds;
            const drawingWidth = bounds.max_x - bounds.min_x, drawingHeight = bounds.max_y - bounds.min_y;
            const scaleX = (canvas.width - 40) / drawingWidth, scaleY = (canvas.height - 40) / drawingHeight;
            const scale = Math.min(scaleX, scaleY);
            const offsetX = (canvas.width - drawingWidth * scale) / 2 - bounds.min_x * scale;
            const offsetY = (canvas.height - drawingHeight * scale) / 2 - bounds.min_y * scale;
            transform = { scale, offsetX, offsetY }; render();
        }
        
        const canvas = document.getElementById('dxfCanvas');
        canvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            const rect = canvas.getBoundingClientRect();
            lastMousePos = { x: e.clientX - rect.left, y: e.clientY - rect.top };
        });
        canvas.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const rect = canvas.getBoundingClientRect();
            const currentMousePos = { x: e.clientX - rect.left, y: e.clientY - rect.top };
            const deltaX = currentMousePos.x - lastMousePos.x;
            const deltaY = currentMousePos.y - lastMousePos.y;
            transform.offsetX += deltaX;
            transform.offsetY += deltaY;
            lastMousePos = currentMousePos;
            render();
        });
        canvas.addEventListener('mouseup', () => { isDragging = false; });
        canvas.addEventListener('mouseleave', () => { isDragging = false; });
        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
            const newScale = transform.scale * zoomFactor;
            const newOffsetX = mouseX - (mouseX - transform.offsetX) * zoomFactor;
            const newOffsetY = mouseY - (mouseY - transform.offsetY) * zoomFactor;
            transform = { scale: newScale, offsetX: newOffsetX, offsetY: newOffsetY };
            render();
        });
        
        refreshFiles();
    </script>
</body>
</html>`;
}

function deactivate() {
    if (currentPanel) {
        currentPanel.dispose();
    }
    if (fileWatcher) {
        fileWatcher.dispose();
    }
}

module.exports = { activate, deactivate };