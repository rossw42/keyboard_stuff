/**
 * Webview Content Generator
 * Generates HTML content for the DXF viewer webview
 */

class WebviewContent {
    static getHtml(config) {
        const theme = config.get('theme', 'auto');
        const lineWidth = config.get('lineWidth', 1);
        const gridEnabled = config.get('gridEnabled', true);
        const showDimensions = config.get('showDimensions', true);

        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ergogen DXF Viewer</title>
    <style>
        :root {
            --bg-color: ${theme === 'dark' ? '#1e1e1e' : theme === 'light' ? '#ffffff' : 'var(--vscode-editor-background)'};
            --text-color: ${theme === 'dark' ? '#cccccc' : theme === 'light' ? '#333333' : 'var(--vscode-editor-foreground)'};
            --border-color: ${theme === 'dark' ? '#3c3c3c' : theme === 'light' ? '#e1e4e8' : 'var(--vscode-panel-border)'};
            --button-bg: ${theme === 'dark' ? '#0e639c' : theme === 'light' ? '#0078d4' : 'var(--vscode-button-background)'};
            --button-hover: ${theme === 'dark' ? '#1177bb' : theme === 'light' ? '#106ebe' : 'var(--vscode-button-hoverBackground)'};
            --line-width: ${lineWidth}px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--vscode-font-family, 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif);
            background-color: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            overflow: hidden;
        }

        .container {
            display: flex;
            height: 100vh;
        }

        .sidebar {
            width: 300px;
            background-color: var(--bg-color);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .toolbar {
            padding: 10px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 6px 12px;
            background-color: var(--button-bg);
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            transition: background-color 0.2s;
        }

        .btn:hover {
            background-color: var(--button-hover);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .file-list {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }

        .file-item {
            padding: 8px 12px;
            margin: 2px 0;
            border-radius: 3px;
            cursor: pointer;
            transition: background-color 0.2s;
            border: 1px solid transparent;
        }

        .file-item:hover {
            background-color: var(--vscode-list-hoverBackground, rgba(255, 255, 255, 0.1));
        }

        .file-item.selected {
            background-color: var(--vscode-list-activeSelectionBackground, rgba(0, 120, 212, 0.3));
            border-color: var(--vscode-list-activeSelectionForeground, #007acc);
        }

        .file-name {
            font-weight: 500;
            margin-bottom: 2px;
        }

        .file-info {
            font-size: 11px;
            opacity: 0.7;
        }

        .viewer-container {
            flex: 1;
            position: relative;
            overflow: hidden;
        }

        #dxf-canvas {
            width: 100%;
            height: 100%;
            display: block;
            cursor: grab;
        }

        #dxf-canvas:active {
            cursor: grabbing;
        }

        .status-bar {
            padding: 5px 10px;
            border-top: 1px solid var(--border-color);
            font-size: 11px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            font-size: 14px;
            opacity: 0.7;
        }

        .error {
            color: var(--vscode-errorForeground, #f48771);
            padding: 20px;
            text-align: center;
        }

        .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            opacity: 0.7;
            text-align: center;
            padding: 20px;
        }

        .empty-state h3 {
            margin-bottom: 10px;
        }

        .zoom-controls {
            position: absolute;
            top: 10px;
            right: 10px;
            display: flex;
            flex-direction: column;
            gap: 5px;
            z-index: 100;
        }

        .zoom-btn {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background-color: var(--button-bg);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .zoom-btn:hover {
            background-color: var(--button-hover);
        }

        .layer-controls {
            padding: 10px;
            border-bottom: 1px solid var(--border-color);
        }

        .layer-item {
            display: flex;
            align-items: center;
            padding: 2px 0;
            font-size: 12px;
        }

        .layer-checkbox {
            margin-right: 8px;
        }

        .coordinates {
            font-family: monospace;
            font-size: 10px;
        }

        @media (max-width: 800px) {
            .sidebar {
                width: 250px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="toolbar">
                <button class="btn" id="run-ergogen">▶ Run Ergogen</button>
                <button class="btn" id="refresh-files">🔄 Refresh</button>
            </div>
            
            <div class="layer-controls" id="layer-controls" style="display: none;">
                <h4>Layers</h4>
                <div id="layer-list"></div>
            </div>
            
            <div class="file-list" id="file-list">
                <div class="empty-state">
                    <h3>No DXF Files Found</h3>
                    <p>Run Ergogen to generate DXF files, or check your output directory.</p>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="toolbar">
                <button class="btn" id="fit-to-window">📐 Fit to Window</button>
                <button class="btn" id="toggle-grid">${gridEnabled ? '⊞' : '⊡'} Grid</button>
                <button class="btn" id="toggle-dimensions">${showDimensions ? '📏' : '📐'} Dimensions</button>
                <span id="file-info"></span>
            </div>
            
            <div class="viewer-container">
                <canvas id="dxf-canvas"></canvas>
                <div class="zoom-controls">
                    <button class="zoom-btn" id="zoom-in">+</button>
                    <button class="zoom-btn" id="zoom-out">−</button>
                    <button class="zoom-btn" id="zoom-reset">⌂</button>
                </div>
                <div class="loading" id="loading" style="display: none;">
                    Loading DXF file...
                </div>
            </div>
            
            <div class="status-bar">
                <span id="status-text">Ready</span>
                <span class="coordinates" id="coordinates">X: 0, Y: 0</span>
            </div>
        </div>
    </div>

    <script>
        // Global state
        let currentDxfData = null;
        let currentFiles = [];
        let selectedFile = null;
        let canvas = null;
        let ctx = null;
        let viewState = {
            zoom: 1,
            panX: 0,
            panY: 0,
            isDragging: false,
            lastMouseX: 0,
            lastMouseY: 0
        };
        let config = {
            theme: '${theme}',
            lineWidth: ${lineWidth},
            gridEnabled: ${gridEnabled},
            showDimensions: ${showDimensions}
        };
        let visibleLayers = new Set();

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            initializeCanvas();
            setupEventListeners();
            requestFileList();
        });

        function initializeCanvas() {
            canvas = document.getElementById('dxf-canvas');
            ctx = canvas.getContext('2d');
            
            // Set canvas size
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);
        }

        function resizeCanvas() {
            const container = canvas.parentElement;
            canvas.width = container.clientWidth;
            canvas.height = container.clientHeight;
            
            if (currentDxfData) {
                renderDxf();
            }
        }

        function setupEventListeners() {
            // Toolbar buttons
            document.getElementById('run-ergogen').addEventListener('click', () => {
                vscode.postMessage({ command: 'runErgogen' });
            });
            
            document.getElementById('refresh-files').addEventListener('click', () => {
                vscode.postMessage({ command: 'refreshFiles' });
            });
            
            document.getElementById('fit-to-window').addEventListener('click', fitToWindow);
            document.getElementById('toggle-grid').addEventListener('click', toggleGrid);
            document.getElementById('toggle-dimensions').addEventListener('click', toggleDimensions);
            
            // Zoom controls
            document.getElementById('zoom-in').addEventListener('click', () => zoom(1.2));
            document.getElementById('zoom-out').addEventListener('click', () => zoom(0.8));
            document.getElementById('zoom-reset').addEventListener('click', resetView);
            
            // Canvas interactions
            canvas.addEventListener('wheel', handleWheel);
            canvas.addEventListener('mousedown', handleMouseDown);
            canvas.addEventListener('mousemove', handleMouseMove);
            canvas.addEventListener('mouseup', handleMouseUp);
            canvas.addEventListener('mouseleave', handleMouseUp);
        }

        // Message handling
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
                case 'updateConfig':
                    updateConfig(message.config);
                    break;
                case 'fitToWindow':
                    fitToWindow();
                    break;
            }
        });

        function updateFileList(files, error) {
            const fileList = document.getElementById('file-list');
            
            if (error) {
                fileList.innerHTML = \`<div class="error">\${error}</div>\`;
                return;
            }
            
            if (!files || files.length === 0) {
                fileList.innerHTML = \`
                    <div class="empty-state">
                        <h3>No DXF Files Found</h3>
                        <p>Run Ergogen to generate DXF files.</p>
                    </div>
                \`;
                return;
            }
            
            currentFiles = files;
            
            const html = files.map(file => \`
                <div class="file-item" data-filename="\${file.name}" onclick="selectFile('\${file.name}')">
                    <div class="file-name">\${file.name}</div>
                    <div class="file-info">
                        \${formatFileSize(file.size)} • \${formatDate(file.modified)}
                    </div>
                </div>
            \`).join('');
            
            fileList.innerHTML = html;
            
            // Auto-select first file if none selected
            if (!selectedFile && files.length > 0) {
                selectFile(files[0].name);
            }
        }

        function selectFile(filename) {
            // Update UI
            document.querySelectorAll('.file-item').forEach(item => {
                item.classList.remove('selected');
            });
            
            const selectedItem = document.querySelector(\`[data-filename="\${filename}"]\`);
            if (selectedItem) {
                selectedItem.classList.add('selected');
            }
            
            selectedFile = filename;
            
            // Load file
            document.getElementById('loading').style.display = 'flex';
            document.getElementById('status-text').textContent = \`Loading \${filename}...\`;
            
            vscode.postMessage({
                command: 'loadFile',
                filename: filename
            });
        }

        function displayDxf(filename, data) {
            document.getElementById('loading').style.display = 'none';
            
            currentDxfData = data;
            
            // Update file info
            document.getElementById('file-info').textContent = 
                \`\${filename} • \${data.entity_count} entities\`;
            
            // Update layers
            updateLayerControls(data.layers);
            
            // Reset view and render
            resetView();
            renderDxf();
            
            document.getElementById('status-text').textContent = 
                \`Loaded \${filename} (\${data.entity_count} entities)\`;
        }

        function displayError(filename, error) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('status-text').textContent = \`Error: \${error}\`;
            
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Show error message
            ctx.fillStyle = config.theme === 'dark' ? '#f48771' : '#d73a49';
            ctx.font = '14px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(\`Error loading \${filename}\`, canvas.width / 2, canvas.height / 2 - 10);
            ctx.fillText(error, canvas.width / 2, canvas.height / 2 + 10);
        }

        function updateLayerControls(layers) {
            const layerControls = document.getElementById('layer-controls');
            const layerList = document.getElementById('layer-list');
            
            if (!layers || layers.length <= 1) {
                layerControls.style.display = 'none';
                return;
            }
            
            // Initialize visible layers
            if (visibleLayers.size === 0) {
                layers.forEach(layer => visibleLayers.add(layer));
            }
            
            const html = layers.map(layer => \`
                <div class="layer-item">
                    <input type="checkbox" class="layer-checkbox" 
                           id="layer-\${layer}" 
                           \${visibleLayers.has(layer) ? 'checked' : ''}
                           onchange="toggleLayer('\${layer}', this.checked)">
                    <label for="layer-\${layer}">\${layer}</label>
                </div>
            \`).join('');
            
            layerList.innerHTML = html;
            layerControls.style.display = 'block';
        }

        function toggleLayer(layer, visible) {
            if (visible) {
                visibleLayers.add(layer);
            } else {
                visibleLayers.delete(layer);
            }
            renderDxf();
        }

        function renderDxf() {
            if (!currentDxfData || !ctx) return;
            
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Save context
            ctx.save();
            
            // Apply transformations
            ctx.translate(canvas.width / 2, canvas.height / 2);
            ctx.scale(viewState.zoom, -viewState.zoom); // Flip Y axis
            ctx.translate(viewState.panX, viewState.panY);
            
            // Draw grid if enabled
            if (config.gridEnabled) {
                drawGrid();
            }
            
            // Set line properties
            ctx.lineWidth = config.lineWidth / viewState.zoom;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            
            // Draw entities
            currentDxfData.entities.forEach(entity => {
                if (visibleLayers.size === 0 || visibleLayers.has(entity.layer || '0')) {
                    drawEntity(entity);
                }
            });
            
            // Restore context
            ctx.restore();
        }

        function drawGrid() {
            const bounds = currentDxfData.bounds;
            const gridSize = calculateGridSize();
            
            ctx.strokeStyle = config.theme === 'dark' ? '#333' : '#ddd';
            ctx.lineWidth = 0.5 / viewState.zoom;
            
            // Vertical lines
            for (let x = Math.floor(bounds.min_x / gridSize) * gridSize; x <= bounds.max_x; x += gridSize) {
                ctx.beginPath();
                ctx.moveTo(x, bounds.min_y);
                ctx.lineTo(x, bounds.max_y);
                ctx.stroke();
            }
            
            // Horizontal lines
            for (let y = Math.floor(bounds.min_y / gridSize) * gridSize; y <= bounds.max_y; y += gridSize) {
                ctx.beginPath();
                ctx.moveTo(bounds.min_x, y);
                ctx.lineTo(bounds.max_x, y);
                ctx.stroke();
            }
        }

        function calculateGridSize() {
            const bounds = currentDxfData.bounds;
            const width = bounds.max_x - bounds.min_x;
            const height = bounds.max_y - bounds.min_y;
            const maxDim = Math.max(width, height);
            
            // Calculate appropriate grid size
            const targetGrids = 20;
            let gridSize = maxDim / targetGrids;
            
            // Round to nice numbers
            const magnitude = Math.pow(10, Math.floor(Math.log10(gridSize)));
            const normalized = gridSize / magnitude;
            
            if (normalized <= 1) gridSize = magnitude;
            else if (normalized <= 2) gridSize = 2 * magnitude;
            else if (normalized <= 5) gridSize = 5 * magnitude;
            else gridSize = 10 * magnitude;
            
            return gridSize;
        }

        function drawEntity(entity) {
            ctx.strokeStyle = getEntityColor(entity);
            
            switch (entity.type) {
                case 'line':
                    drawLine(entity);
                    break;
                case 'circle':
                    drawCircle(entity);
                    break;
                case 'arc':
                    drawArc(entity);
                    break;
                case 'polyline':
                    drawPolyline(entity);
                    break;
                case 'text':
                    if (config.showDimensions) drawText(entity);
                    break;
                case 'dimension':
                    if (config.showDimensions) drawDimension(entity);
                    break;
                case 'ellipse':
                    drawEllipse(entity);
                    break;
                case 'spline':
                    drawSpline(entity);
                    break;
            }
        }

        function getEntityColor(entity) {
            // DXF color mapping (simplified)
            const colors = {
                1: '#ff0000', 2: '#ffff00', 3: '#00ff00', 4: '#00ffff',
                5: '#0000ff', 6: '#ff00ff', 7: '#ffffff', 8: '#808080'
            };
            
            if (entity.color && colors[entity.color]) {
                return colors[entity.color];
            }
            
            return config.theme === 'dark' ? '#cccccc' : '#333333';
        }

        function drawLine(entity) {
            ctx.beginPath();
            ctx.moveTo(entity.start.x, entity.start.y);
            ctx.lineTo(entity.end.x, entity.end.y);
            ctx.stroke();
        }

        function drawCircle(entity) {
            ctx.beginPath();
            ctx.arc(entity.center.x, entity.center.y, entity.radius, 0, 2 * Math.PI);
            ctx.stroke();
        }

        function drawArc(entity) {
            const startRad = entity.start_angle * Math.PI / 180;
            const endRad = entity.end_angle * Math.PI / 180;
            
            ctx.beginPath();
            ctx.arc(entity.center.x, entity.center.y, entity.radius, startRad, endRad);
            ctx.stroke();
        }

        function drawPolyline(entity) {
            if (entity.points.length < 2) return;
            
            ctx.beginPath();
            ctx.moveTo(entity.points[0].x, entity.points[0].y);
            
            for (let i = 1; i < entity.points.length; i++) {
                ctx.lineTo(entity.points[i].x, entity.points[i].y);
            }
            
            if (entity.closed) {
                ctx.closePath();
            }
            
            ctx.stroke();
        }

        function drawText(entity) {
            ctx.save();
            ctx.scale(1, -1); // Flip text back
            ctx.fillStyle = ctx.strokeStyle;
            ctx.font = \`\${entity.height || 1}px sans-serif\`;
            ctx.textAlign = 'left';
            ctx.fillText(entity.text, entity.position.x, -entity.position.y);
            ctx.restore();
        }

        function drawDimension(entity) {
            // Draw dimension line
            drawLine(entity);
            
            // Draw dimension text if available
            if (entity.text) {
                const midX = (entity.start.x + entity.end.x) / 2;
                const midY = (entity.start.y + entity.end.y) / 2;
                
                ctx.save();
                ctx.scale(1, -1);
                ctx.fillStyle = ctx.strokeStyle;
                ctx.font = '2px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(entity.text, midX, -midY);
                ctx.restore();
            }
        }

        function drawEllipse(entity) {
            ctx.save();
            ctx.translate(entity.center.x, entity.center.y);
            ctx.rotate(entity.rotation * Math.PI / 180);
            ctx.scale(entity.major_axis, entity.minor_axis);
            ctx.beginPath();
            ctx.arc(0, 0, 1, 0, 2 * Math.PI);
            ctx.stroke();
            ctx.restore();
        }

        function drawSpline(entity) {
            if (entity.control_points.length < 2) return;
            
            // Simple spline approximation using control points
            ctx.beginPath();
            ctx.moveTo(entity.control_points[0].x, entity.control_points[0].y);
            
            for (let i = 1; i < entity.control_points.length; i++) {
                ctx.lineTo(entity.control_points[i].x, entity.control_points[i].y);
            }
            
            ctx.stroke();
        }

        // View controls
        function fitToWindow() {
            if (!currentDxfData) return;
            
            const bounds = currentDxfData.bounds;
            const width = bounds.max_x - bounds.min_x;
            const height = bounds.max_y - bounds.min_y;
            
            const scaleX = (canvas.width * 0.9) / width;
            const scaleY = (canvas.height * 0.9) / height;
            
            viewState.zoom = Math.min(scaleX, scaleY);
            viewState.panX = -(bounds.min_x + width / 2);
            viewState.panY = -(bounds.min_y + height / 2);
            
            renderDxf();
        }

        function resetView() {
            viewState.zoom = 1;
            viewState.panX = 0;
            viewState.panY = 0;
            
            if (currentDxfData) {
                fitToWindow();
            }
        }

        function zoom(factor) {
            viewState.zoom *= factor;
            renderDxf();
        }

        function toggleGrid() {
            config.gridEnabled = !config.gridEnabled;
            document.getElementById('toggle-grid').textContent = 
                (config.gridEnabled ? '⊞' : '⊡') + ' Grid';
            renderDxf();
        }

        function toggleDimensions() {
            config.showDimensions = !config.showDimensions;
            document.getElementById('toggle-dimensions').textContent = 
                (config.showDimensions ? '📏' : '📐') + ' Dimensions';
            renderDxf();
        }

        // Mouse handling
        function handleWheel(e) {
            e.preventDefault();
            const factor = e.deltaY > 0 ? 0.9 : 1.1;
            zoom(factor);
        }

        function handleMouseDown(e) {
            viewState.isDragging = true;
            viewState.lastMouseX = e.clientX;
            viewState.lastMouseY = e.clientY;
        }

        function handleMouseMove(e) {
            // Update coordinates display
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX - rect.left - canvas.width / 2) / viewState.zoom - viewState.panX;
            const y = -((e.clientY - rect.top - canvas.height / 2) / viewState.zoom - viewState.panY);
            
            document.getElementById('coordinates').textContent = 
                \`X: \${x.toFixed(2)}, Y: \${y.toFixed(2)}\`;
            
            if (viewState.isDragging) {
                const deltaX = e.clientX - viewState.lastMouseX;
                const deltaY = e.clientY - viewState.lastMouseY;
                
                viewState.panX += deltaX / viewState.zoom;
                viewState.panY -= deltaY / viewState.zoom; // Flip Y
                
                viewState.lastMouseX = e.clientX;
                viewState.lastMouseY = e.clientY;
                
                renderDxf();
            }
        }

        function handleMouseUp() {
            viewState.isDragging = false;
        }

        function updateConfig(newConfig) {
            config = { ...config, ...newConfig };
            renderDxf();
        }

        // Utility functions
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
        }

        function formatDate(dateString) {
            return new Date(dateString).toLocaleString();
        }

        function requestFileList() {
            vscode.postMessage({ command: 'refreshFiles' });
        }

        // VSCode API
        const vscode = acquireVsCodeApi();
    </script>
</body>
</html>`;
    }
}

module.exports = WebviewContent;