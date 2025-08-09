// Simple debug version to test extension loading
const vscode = require('vscode');

// Global variables
let currentPanel = undefined;
let backendProcess = undefined;
let backendPort = 5173;

function activate(context) {
    console.log('🚀 Ergogen extension is activating...');
    
    // Force show activation message
    vscode.window.showInformationMessage('🎹 Ergogen DXF Viewer extension activated!');
    
    // Test command
    const testCommand = vscode.commands.registerCommand('ergogen-dxf-viewer.test', () => {
        vscode.window.showInformationMessage('✅ Extension is working!');
    });
    
    // Run Ergogen command
    const runErgogenCommand = vscode.commands.registerCommand('ergogen-dxf-viewer.runErgogen', async () => {
        vscode.window.showInformationMessage('🔄 Running Ergogen...');
        
        if (!vscode.workspace.workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder found');
            return;
        }

        const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
        const { spawn } = require('child_process');
        const path = require('path');
        const fs = require('fs');
        
        let yamlFile = null;
        let workingDir = workspaceRoot;
        
        // First priority: Use the currently active file if it's a YAML file
        const activeEditor = vscode.window.activeTextEditor;
        if (activeEditor) {
            const activeFile = activeEditor.document.fileName;
            const fileName = path.basename(activeFile);
            const fileDir = path.dirname(activeFile);
            
            if (fileName.endsWith('.yaml') || fileName.endsWith('.yml')) {
                yamlFile = fileName;
                workingDir = fileDir;
                console.log(`Using active YAML file: ${fileName} in ${fileDir}`);
            }
        }
        
        // Second priority: Look for common YAML files in workspace root
        if (!yamlFile) {
            const possibleFiles = ['keyboard.yaml', 'config.yaml', 'layout.yaml'];
            
            for (const file of possibleFiles) {
                if (fs.existsSync(path.join(workspaceRoot, file))) {
                    yamlFile = file;
                    workingDir = workspaceRoot;
                    console.log(`Found YAML file in workspace: ${file}`);
                    break;
                }
            }
        }
        
        // Third priority: Look for any .yaml files in workspace root
        if (!yamlFile) {
            try {
                const files = fs.readdirSync(workspaceRoot);
                const yamlFiles = files.filter(file => file.endsWith('.yaml') || file.endsWith('.yml'));
                if (yamlFiles.length > 0) {
                    yamlFile = yamlFiles[0];
                    workingDir = workspaceRoot;
                    console.log(`Found YAML file: ${yamlFile}`);
                }
            } catch (error) {
                console.log('Error reading directory:', error);
            }
        }
        
        if (!yamlFile) {
            vscode.window.showErrorMessage('❌ No YAML files found. Please open a YAML file or ensure one exists in your workspace.');
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
            console.log('Ergogen stdout:', data.toString());
        });

        ergogenProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
            console.log('Ergogen stderr:', data.toString());
        });

        ergogenProcess.on('close', (code) => {
            console.log(`Ergogen exited with code ${code}`);
            console.log('Output:', output);
            console.log('Error output:', errorOutput);
            
            if (code === 0) {
                vscode.window.showInformationMessage('✅ Ergogen completed successfully! DXF viewer should refresh.');
                
                // Refresh the webview if it's open
                if (currentPanel) {
                    currentPanel.webview.html = getWebviewContent();
                }
            } else {
                vscode.window.showErrorMessage(`❌ Ergogen failed with code ${code}. Check Developer Console for details.`);
            }
        });

        ergogenProcess.on('error', (error) => {
            console.log('Ergogen process error:', error);
            vscode.window.showErrorMessage(`❌ Failed to run ergogen: ${error.message}`);
        });
    });

    // Open viewer command - creates webview panel inside VSCode
    const openViewerCommand = vscode.commands.registerCommand('ergogen-dxf-viewer.openViewer', () => {
        createDxfViewerPanel();
    });

    // Function to create webview panel
    function createDxfViewerPanel() {
        // Check if panel already exists
        if (currentPanel) {
            currentPanel.reveal(vscode.ViewColumn.Beside);
            return;
        }

        // Create webview panel
        currentPanel = vscode.window.createWebviewPanel(
            'dxfViewer',
            'DXF Viewer',
            vscode.ViewColumn.Beside,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        // Set webview content
        currentPanel.webview.html = getWebviewContent();

        // Handle messages from webview
        currentPanel.webview.onDidReceiveMessage(
            message => {
                switch (message.command) {
                    case 'runErgogen':
                        vscode.commands.executeCommand('ergogen-dxf-viewer.runErgogen');
                        break;
                    case 'toggleAutoRun':
                        toggleAutoRun();
                        break;
                }
            },
            undefined,
            context.subscriptions
        );

        // Handle panel disposal
        currentPanel.onDidDispose(() => {
            currentPanel = undefined;
        });

        vscode.window.showInformationMessage('🎹 DXF Viewer opened in VSCode panel!');
    }

    // Function to toggle auto-run setting
    function toggleAutoRun() {
        const config = vscode.workspace.getConfiguration('ergogen-dxf-viewer');
        const currentValue = config.get('autoRunOnSave', false);
        config.update('autoRunOnSave', !currentValue, vscode.ConfigurationTarget.Workspace);
        
        const newValue = !currentValue;
        vscode.window.showInformationMessage(
            `Auto-run on save: ${newValue ? '✅ Enabled' : '❌ Disabled'}`
        );
        
        // Refresh webview to update button state
        if (currentPanel) {
            currentPanel.webview.html = getWebviewContent();
        }
    }

    // Generate webview HTML content
    function getWebviewContent() {
        const config = vscode.workspace.getConfiguration('ergogen-dxf-viewer');
        const autoRunEnabled = config.get('autoRunOnSave', false);
        
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DXF Viewer</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        iframe {
            width: 100%;
            height: 100vh;
            border: none;
        }
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #666;
            flex-direction: column;
        }
        .error {
            color: #d73a49;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #007acc;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .controls {
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
            display: flex;
            gap: 10px;
        }
        .btn {
            background: #007acc;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-family: inherit;
        }
        .btn:hover {
            background: #005a9e;
        }
        .btn.secondary {
            background: #6c757d;
        }
        .btn.secondary:hover {
            background: #545b62;
        }
        .btn.active {
            background: #28a745;
        }
        .btn.active:hover {
            background: #218838;
        }
    </style>
</head>
<body>
    <div class="controls">
        <button class="btn" onclick="runErgogen()" title="Run Ergogen to generate DXF files">
            🔄 Generate
        </button>
        <button class="btn ${autoRunEnabled ? 'active' : 'secondary'}" onclick="toggleAutoRun()" title="Toggle auto-run on YAML file save">
            ${autoRunEnabled ? '🔥 Auto: ON' : '⏸️ Auto: OFF'}
        </button>
    </div>
    
    <div id="loading" class="loading">
        <div class="spinner"></div>
        <div>
            <h3>🚀 Starting DXF Viewer...</h3>
            <p>Backend is starting automatically...</p>
            <p><small>This may take a few seconds</small></p>
        </div>
    </div>
    <iframe id="viewer" src="http://localhost:${backendPort}" style="display: none;"></iframe>
    
    <script>
        const iframe = document.getElementById('viewer');
        const loading = document.getElementById('loading');
        let retryCount = 0;
        const maxRetries = 10;
        
        function tryLoadViewer() {
            retryCount++;
            console.log('Attempting to load viewer, attempt:', retryCount);
            
            // Create a new iframe to force reload
            const newIframe = document.createElement('iframe');
            newIframe.id = 'viewer';
            newIframe.style.width = '100%';
            newIframe.style.height = '100vh';
            newIframe.style.border = 'none';
            newIframe.style.display = 'none';
            newIframe.src = 'http://localhost:${backendPort}';
            
            newIframe.onload = function() {
                loading.style.display = 'none';
                newIframe.style.display = 'block';
                console.log('DXF viewer loaded successfully');
            };
            
            newIframe.onerror = function() {
                if (retryCount < maxRetries) {
                    setTimeout(tryLoadViewer, 2000);
                } else {
                    loading.innerHTML = '<div class="error"><h3>❌ Could not connect to DXF viewer</h3><p>Backend may have failed to start</p><p>Check the VSCode Developer Console for errors</p></div>';
                }
            };
            
            // Replace old iframe
            const oldIframe = document.getElementById('viewer');
            if (oldIframe) {
                oldIframe.remove();
            }
            document.body.appendChild(newIframe);
        }
        
        // Start trying to load after a short delay
        setTimeout(tryLoadViewer, 3000);
        
        // Functions to communicate with VSCode extension
        const vscode = acquireVsCodeApi();
        
        window.runErgogen = function() {
            vscode.postMessage({
                command: 'runErgogen'
            });
        };
        
        window.toggleAutoRun = function() {
            vscode.postMessage({
                command: 'toggleAutoRun'
            });
        };
    </script>
</body>
</html>`;
    }

    // Watch for YAML file changes
    const yamlWatcher = vscode.workspace.createFileSystemWatcher('**/*.{yaml,yml}');
    yamlWatcher.onDidSave(async (uri) => {
        const config = vscode.workspace.getConfiguration('ergogen-dxf-viewer');
        const autoRun = config.get('autoRunOnSave', false); // Default to false for now
        
        if (autoRun) {
            console.log('YAML file saved, auto-running Ergogen:', uri.fsPath);
            vscode.window.showInformationMessage('🔄 Auto-running Ergogen...');
            await vscode.commands.executeCommand('ergogen-dxf-viewer.runErgogen');
        }
    });

    context.subscriptions.push(testCommand, runErgogenCommand, openViewerCommand, yamlWatcher);
    
    // Auto-start backend when extension activates
    startBackendServer();
    
    console.log('✅ Ergogen extension activated successfully');
    vscode.window.showInformationMessage('🎹 Ergogen DXF Viewer extension loaded!');
}

    // Function to start the DXF viewer backend
    async function startBackendServer() {
        if (backendProcess) {
            console.log('Backend already running');
            return;
        }

        try {
            const { spawn } = require('child_process');
            const path = require('path');
            
            // Get the extension path
            const extensionPath = context.extensionPath;
            
            // Look for the backend in the extension directory
            let backendPath = path.join(extensionPath, '..', '..', 'backend');
            
            // If not found, try relative to workspace
            if (!require('fs').existsSync(backendPath)) {
                if (vscode.workspace.workspaceFolders) {
                    backendPath = path.join(vscode.workspace.workspaceFolders[0].uri.fsPath, 'dxf-viewer', 'backend');
                }
            }
            
            const appPath = path.join(backendPath, 'app.py');
            
            if (!require('fs').existsSync(appPath)) {
                console.log('Backend app.py not found at:', appPath);
                vscode.window.showWarningMessage('DXF viewer backend not found. Please ensure the dxf-viewer is in your workspace.');
                return;
            }

            console.log('Starting backend from:', backendPath);
            
            // Start the Python backend
            backendProcess = spawn('python3', ['app.py'], {
                cwd: backendPath,
                env: { ...process.env, PORT: backendPort.toString() },
                stdio: ['pipe', 'pipe', 'pipe']
            });

            backendProcess.stdout.on('data', (data) => {
                console.log('Backend stdout:', data.toString());
            });

            backendProcess.stderr.on('data', (data) => {
                console.log('Backend stderr:', data.toString());
            });

            backendProcess.on('close', (code) => {
                console.log(`Backend process exited with code ${code}`);
                backendProcess = undefined;
            });

            backendProcess.on('error', (error) => {
                console.log('Backend process error:', error);
                vscode.window.showErrorMessage(`Failed to start DXF viewer backend: ${error.message}`);
                backendProcess = undefined;
            });

            // Wait a moment for backend to start
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Configure the backend to watch the output directory
            configureBackendDirectory();
            
            vscode.window.showInformationMessage('🚀 DXF viewer backend started automatically!');
            
        } catch (error) {
            console.log('Error starting backend:', error);
            vscode.window.showErrorMessage(`Failed to start DXF viewer: ${error.message}`);
        }
    }

    // Function to configure backend directory
    async function configureBackendDirectory() {
        if (!vscode.workspace.workspaceFolders) return;

        const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
        const path = require('path');
        const fs = require('fs');
        
        // Look for output directory
        const outputDir = path.join(workspaceRoot, 'output');
        
        if (fs.existsSync(outputDir)) {
            try {
                const http = require('http');
                const postData = JSON.stringify({ path: outputDir });
                
                const options = {
                    hostname: 'localhost',
                    port: backendPort,
                    path: '/api/directory',
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Content-Length': Buffer.byteLength(postData)
                    }
                };

                const req = http.request(options, (res) => {
                    if (res.statusCode === 200) {
                        console.log(`Configured DXF viewer to watch: ${outputDir}`);
                    }
                });

                req.on('error', (error) => {
                    console.log('Error configuring backend directory:', error);
                });

                req.write(postData);
                req.end();
            } catch (error) {
                console.log('Error configuring backend directory:', error);
            }
        }
    }

    // Function to stop backend
    function stopBackendServer() {
        if (backendProcess) {
            backendProcess.kill('SIGTERM');
            backendProcess = undefined;
            console.log('Backend server stopped');
        }
    }
}

function deactivate() {
    console.log('👋 Ergogen extension deactivated');
    
    // Stop backend when extension deactivates
    if (backendProcess) {
        backendProcess.kill('SIGTERM');
        backendProcess = undefined;
    }
}

module.exports = { activate, deactivate };