// Generate the webview HTML content
function getWebviewContent() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DXF Viewer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #1e1e1e;
            color: #cccccc;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: #252526;
            padding: 12px 16px;
            border-bottom: 1px solid #3c3c3c;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
        }
        
        .controls {
            display: flex;
            gap: 8px;
        }
        
        .btn {
            background: #0e639c;
            color: #ffffff;
            border: 1px solid #007acc;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s ease;
        }
        
        .btn:hover {
            background: #1177bb;
            box-shadow: 0 2px 4px rgba(0, 122, 204, 0.3);
        }
        
        .main {
            flex: 1;
            display: flex;
            overflow: hidden;
        }
        
        .sidebar {
            width: 250px;
            background: #2d2d30;
            border-right: 1px solid #3c3c3c;
            display: flex;
            flex-direction: column;
        }
        
        .sidebar-header {
            padding: 12px;
            border-bottom: 1px solid #3c3c3c;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .sidebar-header h3 {
            font-size: 14px;
            color: #ffffff;
        }
        
        .refresh-btn {
            background: #6c757d;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 11px;
        }
        
        .file-list {
            flex: 1;
            overflow-y: auto;
            padding: 8px;
        }
        
        .file-item {
            padding: 8px 12px;
            margin-bottom: 2px;
            background: #3c3c3c;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            transition: background-color 0.2s;
        }
        
        .file-item:hover {
            background: #4a4a4a;
        }
        
        .file-item.selected {
            background: #0e639c;
            color: white;
        }
        
        .file-list.empty {
            display: flex;
            align-items: center;
            justify-content: center;
            color: #888888;
            font-style: italic;
        }
        
        .viewer {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #1e1e1e;
        }
        
        .viewer-header {
            padding: 12px 16px;
            border-bottom: 1px solid #3c3c3c;
        }
        
        .viewer-header h2 {
            font-size: 14px;
            color: #ffffff;
        }
        
        .canvas-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }
        
        .canvas-controls {
            margin-bottom: 12px;
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .canvas-controls button {
            background: #007bff;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }
        
        .canvas-controls button:hover {
            background: #0056b3;
        }
        
        .canvas-controls span {
            font-size: 12px;
            color: #cccccc;
        }
        
        canvas {
            border: 1px solid #3c3c3c;
            background: #2d2d30;
            cursor: grab;
        }
        
        canvas:active {
            cursor: grabbing;
        }
        
        .placeholder {
            color: #888888;
            font-size: 14px;
            text-align: center;
        }
        
        .error {
            color: #f48771;
            font-size: 14px;
            text-align: center;
        }
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
                <div id="placeholder" class="placeholder">
                    Select a DXF file from the sidebar to view it
                </div>
            </div>
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        
        let currentDxfData = null;
        let transform = { scale: 1, offsetX: 0, offsetY: 0 };
        let isDragging = false;
        let lastMousePos = { x: 0, y: 0 };
        let selectedFile = null;
        
        // Communication with extension
        function runErgogen() {
            vscode.postMessage({ command: 'runErgogen' });
        }
        
        function refreshFiles() {
            vscode.postMessage({ command: 'refreshFiles' });
        }
        
        function selectFile(filename) {
            selectedFile = filename;
            updateFileSelection();
            vscode.postMessage({ command: 'selectFile', filename: filename });
        }
        
        // Handle messages from extension
        window.addEventListener('message', event => {
            const message = event.data;
            
            switch (message.command) {
                case 'updateFileList':
                    updateFileList(message.files, message.error);
                    break;
                case 'displayDxf':
                    displayDxf(message.filename, message.data);
                    break;
                case 'displayError':
                    displayError(message.filename, message.error);
                    break;
            }
        });
        
        function updateFileList(files, error) {
            const fileList = document.getElementById('fileList');
            
            if (error) {
                fileList.className = 'file-list empty';
                fileList.innerHTML = '<div class="error">' + error + '</div>';
                return;
            }
            
            if (files.length === 0) {
                fileList.className = 'file-list empty';
                fileList.innerHTML = '<div class="placeholder">No DXF files found</div>';
                return;
            }
            
            fileList.className = 'file-list';
            fileList.innerHTML = files.map(file => 
                '<div class="file-item" onclick="selectFile(\\'+ file.path + '\\')">' + 
                file.path + '</div>'
            ).join('');
        }
        
        function updateFileSelection() {
            const items = document.querySelectorAll('.file-item');
            items.forEach(item => {
                if (item.textContent === selectedFile) {
                    item.classList.add('selected');
                } else {
                    item.classList.remove('selected');
                }
            });
        }
        
        function displayDxf(filename, data) {
            currentDxfData = data;
            document.getElementById('currentFile').textContent = filename;
            document.getElementById('placeholder').style.display = 'none';
            document.getElementById('canvasControls').style.display = 'flex';
            document.getElementById('dxfCanvas').style.display = 'block';
            
            fitToWindow();
            render();
        }
        
        function displayError(filename, error) {
            document.getElementById('currentFile').textContent = filename + ' (Error)';
            document.getElementById('placeholder').innerHTML = '<div class="error">Error: ' + error + '</div>';
            document.getElementById('placeholder').style.display = 'block';
            document.getElementById('canvasControls').style.display = 'none';
            document.getElementById('dxfCanvas').style.display = 'none';
        }
        
        // Canvas rendering and interaction code continues...
        // (This would be the rest of the JavaScript for canvas rendering)
        
        // Initial file refresh
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