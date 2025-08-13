const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

// Simplified global state - only track essential information
let outputChannel = null;

// Minimal extension state
const state = {
  lastActiveYamlFile: null,
  currentOutputDir: null,
  isProcessing: false,
};

/**
 * Extension activation
 */
function activate(context) {
  console.log("🚀 Ergogen Toolkit v4.0.0 activating...");

  try {
    // Create output channel for logging
    outputChannel = vscode.window.createOutputChannel("Ergogen Toolkit");
    outputChannel.appendLine("Extension activated");

    // Register only essential commands
    registerCommands(context);

    // Register basic event listeners
    registerEventListeners(context);

    // Simple workspace detection
    detectWorkspace();

    vscode.window.showInformationMessage("🎹 Ergogen Toolkit ready!");
  } catch (error) {
    console.error("Ergogen Toolkit activation failed:", error);
    vscode.window.showErrorMessage(
      `Ergogen Toolkit activation failed: ${error.message}`
    );
  }
}

/**
 * Register essential commands only
 */
function registerCommands(context) {
  // Run Ergogen command
  context.subscriptions.push(
    vscode.commands.registerCommand("ergogen-toolkit.runErgogen", async () => {
      await runErgogen();
    })
  );

  // Open DXF viewer command (system-based)
  context.subscriptions.push(
    vscode.commands.registerCommand("ergogen-toolkit.openViewer", async () => {
      await openSystemDxfViewer();
    })
  );
}

/**
 * Register basic event listeners
 */
function registerEventListeners(context) {
  // Track active editor changes for YAML files
  context.subscriptions.push(
    vscode.window.onDidChangeActiveTextEditor((editor) => {
      if (editor && isYamlFile(editor.document.fileName)) {
        updateLastYamlFile(editor.document.fileName);
      }
    })
  );
}

/**
 * Run Ergogen command - simplified execution
 */
async function runErgogen() {
  if (state.isProcessing) {
    vscode.window.showWarningMessage("⏳ Ergogen is already running...");
    return;
  }

  state.isProcessing = true;
  outputChannel.clear();
  outputChannel.show();
  outputChannel.appendLine("🔄 Running Ergogen...");

  try {
    const yamlFile = await getYamlFile();
    if (!yamlFile) {
      throw new Error("No YAML file found");
    }

    const workingDir = path.dirname(yamlFile.filePath);
    const config = vscode.workspace.getConfiguration("ergogen-toolkit");
    const ergogenCmd = config.get("ergogenCommand", "ergogen");

    // Create output directory based on filename
    const yamlBaseName = path.basename(
      yamlFile.fileName,
      path.extname(yamlFile.fileName)
    );
    const outputDir = path.join(workingDir, yamlBaseName);

    const args = ["-o", outputDir, yamlFile.fileName];

    outputChannel.appendLine(`Command: ${ergogenCmd} ${args.join(" ")}`);
    outputChannel.appendLine(`Working directory: ${workingDir}`);
    outputChannel.appendLine(`Output directory: ${outputDir}`);

    // Show progress
    await vscode.window.withProgress(
      {
        location: vscode.ProgressLocation.Notification,
        title: "Running Ergogen",
        cancellable: true,
      },
      async (progress, token) => {
        return new Promise((resolve, reject) => {
          const ergogenProcess = spawn(ergogenCmd, args, {
            cwd: workingDir,
            shell: true,
          });

          let output = "";
          let errorOutput = "";

          ergogenProcess.stdout.on("data", (data) => {
            output += data.toString();
            outputChannel.append(data.toString());
          });

          ergogenProcess.stderr.on("data", (data) => {
            errorOutput += data.toString();
            outputChannel.append(data.toString());
          });

          ergogenProcess.on("close", async (code) => {
            state.isProcessing = false;

            if (code === 0) {
              outputChannel.appendLine("✅ Ergogen completed successfully!");
              vscode.window.showInformationMessage("✅ Ergogen completed!");

              // Store output directory for DXF viewing
              state.currentOutputDir = outputDir;

              resolve();
            } else {
              outputChannel.appendLine(`❌ Ergogen failed with code ${code}`);
              vscode.window.showErrorMessage(
                `❌ Ergogen failed! Check output for details.`
              );
              reject(new Error(`Ergogen failed with code ${code}`));
            }
          });

          ergogenProcess.on("error", (error) => {
            state.isProcessing = false;
            outputChannel.appendLine(`❌ Error: ${error.message}`);
            
            // Provide helpful error message for command not found
            if (error.code === 'ENOENT') {
              vscode.window.showErrorMessage(
                `❌ Ergogen command not found. Please install Ergogen CLI first.`
              );
            } else {
              vscode.window.showErrorMessage(
                `❌ Failed to run ergogen: ${error.message}`
              );
            }
            reject(error);
          });

          // Handle cancellation
          token.onCancellationRequested(() => {
            ergogenProcess.kill();
            state.isProcessing = false;
            outputChannel.appendLine("⚠️ Ergogen cancelled by user");
          });
        });
      }
    );
  } catch (error) {
    state.isProcessing = false;
    outputChannel.appendLine(`❌ Error: ${error.message}`);
    vscode.window.showErrorMessage(`❌ Error: ${error.message}`);
  }
}

/**
 * Open DXF viewer in webview panel - no popup approach
 */
async function openSystemDxfViewer() {
  try {
    const outputDir = getOutputDirectory();
    if (!outputDir || !fs.existsSync(outputDir)) {
      // Create viewer panel with error message instead of popup
      createDxfViewerPanel([], "Output directory not found. Run Ergogen first to generate DXF files.");
      return;
    }

    const dxfFiles = scanForDxfFiles(outputDir);
    if (dxfFiles.length === 0) {
      // Create viewer panel with no files message instead of popup
      createDxfViewerPanel([], "No DXF files found in output directory. Run Ergogen to generate files.");
      return;
    }

    // Open DXF viewer panel directly with all files - no popup
    createDxfViewerPanel(dxfFiles);

  } catch (error) {
    outputChannel.appendLine(`❌ Error opening DXF viewer: ${error.message}`);
    // Show error in viewer panel instead of popup
    createDxfViewerPanel([], `Error: ${error.message}`);
  }
}

/**
 * Create DXF viewer webview panel
 */
function createDxfViewerPanel(dxfFiles, errorMessage = null) {
  // Create webview panel
  const panel = vscode.window.createWebviewPanel(
    'dxfViewer',
    'DXF Viewer',
    vscode.ViewColumn.Beside,
    {
      enableScripts: true,
      retainContextWhenHidden: true
    }
  );

  // Generate HTML content
  panel.webview.html = generateDxfViewerHtml(dxfFiles, errorMessage);
  
  outputChannel.appendLine(`📂 Opened DXF viewer panel with ${dxfFiles.length} files`);
}

/**
 * Parse DXF content to extract basic 2D entities
 */
function parseDxfContent(dxfText) {
  const entities = [];
  const lines = dxfText.split('\n').map(line => line.trim());
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Look for entity start markers
    if (line === 'LINE') {
      const entity = parseLineEntity(lines, i);
      if (entity) entities.push(entity);
    } else if (line === 'LWPOLYLINE') {
      const entity = parsePolylineEntity(lines, i);
      if (entity) entities.push(entity);
    } else if (line === 'ARC') {
      const entity = parseArcEntity(lines, i);
      if (entity) entities.push(entity);
    } else if (line === 'CIRCLE') {
      const entity = parseCircleEntity(lines, i);
      if (entity) entities.push(entity);
    }
  }
  
  return entities;
}

/**
 * Parse LINE entity from DXF lines
 */
function parseLineEntity(lines, startIndex) {
  const entity = { type: 'LINE', coordinates: [] };
  let x1, y1, x2, y2;
  
  for (let i = startIndex + 1; i < lines.length; i += 2) {
    const code = lines[i];
    const value = lines[i + 1];
    
    // Stop at next entity (code 0 with entity name)
    if (code === '0') break;
    
    if (code === '10') x1 = parseFloat(value);
    else if (code === '20') y1 = parseFloat(value);
    else if (code === '11') x2 = parseFloat(value);
    else if (code === '21') y2 = parseFloat(value);
  }
  
  if (x1 !== undefined && y1 !== undefined && x2 !== undefined && y2 !== undefined) {
    entity.coordinates = [[x1, y1], [x2, y2]];
    return entity;
  }
  return null;
}

/**
 * Parse ARC entity from DXF lines
 */
function parseArcEntity(lines, startIndex) {
  const entity = { type: 'ARC', coordinates: [], properties: {} };
  let cx, cy, radius, startAngle, endAngle;
  
  for (let i = startIndex + 1; i < lines.length; i += 2) {
    const code = lines[i];
    const value = lines[i + 1];
    
    // Stop at next entity (code 0 with entity name)
    if (code === '0') break;
    
    if (code === '10') cx = parseFloat(value);
    else if (code === '20') cy = parseFloat(value);
    else if (code === '40') radius = parseFloat(value);
    else if (code === '50') startAngle = parseFloat(value);
    else if (code === '51') endAngle = parseFloat(value);
  }
  
  if (cx !== undefined && cy !== undefined && radius !== undefined) {
    entity.coordinates = [[cx, cy]];
    entity.properties = { 
      radius, 
      startAngle: startAngle || 0, 
      endAngle: endAngle || 360 
    };
    return entity;
  }
  return null;
}

/**
 * Parse CIRCLE entity from DXF lines
 */
function parseCircleEntity(lines, startIndex) {
  const entity = { type: 'CIRCLE', coordinates: [], properties: {} };
  let cx, cy, radius;
  
  for (let i = startIndex + 1; i < lines.length; i += 2) {
    const code = lines[i];
    const value = lines[i + 1];
    
    // Stop at next entity (code 0 with entity name)
    if (code === '0') break;
    
    if (code === '10') cx = parseFloat(value);
    else if (code === '20') cy = parseFloat(value);
    else if (code === '40') radius = parseFloat(value);
  }
  
  if (cx !== undefined && cy !== undefined && radius !== undefined) {
    entity.coordinates = [[cx, cy]];
    entity.properties = { radius };
    return entity;
  }
  return null;
}

/**
 * Parse LWPOLYLINE entity from DXF lines
 */
function parsePolylineEntity(lines, startIndex) {
  const entity = { type: 'LWPOLYLINE', coordinates: [], properties: {} };
  const points = [];
  let closed = false;
  
  for (let i = startIndex + 1; i < lines.length; i += 2) {
    const code = lines[i];
    const value = lines[i + 1];
    
    // Stop at next entity (code 0 with entity name)
    if (code === '0') break;
    
    if (code === '70') {
      closed = (parseInt(value) & 1) === 1; // Check closed flag
    } else if (code === '10') {
      const x = parseFloat(value);
      // Y coordinate should be next (code 20)
      if (i + 2 < lines.length && lines[i + 2] === '20') {
        const y = parseFloat(lines[i + 3]);
        if (!isNaN(x) && !isNaN(y)) {
          points.push([x, y]);
        }
      }
    }
  }
  
  if (points.length > 1) {
    entity.coordinates = points;
    entity.properties = { closed };
    return entity;
  }
  return null;
}

/**
 * Convert parsed DXF entities to SVG markup
 */
function entitiesToSvg(entities) {
  if (!entities || entities.length === 0) {
    return '<p><em>No renderable entities found in DXF file</em></p>';
  }
  
  // Calculate viewport bounds
  const viewport = calculateViewport(entities);
  if (!viewport) {
    return '<p><em>Unable to calculate viewport for DXF entities</em></p>';
  }
  
  // Add padding around the content
  const padding = Math.max(viewport.width, viewport.height) * 0.1;
  const viewBox = `${viewport.minX - padding} ${viewport.minY - padding} ${viewport.width + 2*padding} ${viewport.height + 2*padding}`;
  
  // Generate SVG elements for each entity
  const svgElements = entities.map(entity => entityToSvgElement(entity)).filter(el => el);
  
  return `
    <svg viewBox="${viewBox}" class="dxf-svg">
      <g class="dxf-entities">
        ${svgElements.join('\n        ')}
      </g>
    </svg>
  `;
}

/**
 * Calculate viewport bounds from entities
 */
function calculateViewport(entities) {
  let minX = Infinity, minY = Infinity;
  let maxX = -Infinity, maxY = -Infinity;
  
  entities.forEach(entity => {
    entity.coordinates.forEach(([x, y]) => {
      minX = Math.min(minX, x);
      minY = Math.min(minY, y);
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);
    });
    
    // Handle radius for circles and arcs
    if (entity.properties && entity.properties.radius) {
      const [cx, cy] = entity.coordinates[0];
      const r = entity.properties.radius;
      minX = Math.min(minX, cx - r);
      minY = Math.min(minY, cy - r);
      maxX = Math.max(maxX, cx + r);
      maxY = Math.max(maxY, cy + r);
    }
  });
  
  if (minX === Infinity) return null;
  
  return {
    minX, minY, maxX, maxY,
    width: maxX - minX,
    height: maxY - minY
  };
}

/**
 * Convert single entity to SVG element
 */
function entityToSvgElement(entity) {
  switch (entity.type) {
    case 'LINE':
      return lineToSvg(entity);
    case 'ARC':
      return arcToSvg(entity);
    case 'CIRCLE':
      return circleToSvg(entity);
    case 'LWPOLYLINE':
      return polylineToSvg(entity);
    default:
      return null;
  }
}

/**
 * Convert LINE entity to SVG
 */
function lineToSvg(entity) {
  const [[x1, y1], [x2, y2]] = entity.coordinates;
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="dxf-entity" />`;
}

/**
 * Convert CIRCLE entity to SVG
 */
function circleToSvg(entity) {
  const [cx, cy] = entity.coordinates[0];
  const radius = entity.properties.radius;
  return `<circle cx="${cx}" cy="${cy}" r="${radius}" class="dxf-entity" />`;
}

/**
 * Convert ARC entity to SVG path
 */
function arcToSvg(entity) {
  const [cx, cy] = entity.coordinates[0];
  const { radius, startAngle, endAngle } = entity.properties;
  
  // Convert angles from degrees to radians
  const start = (startAngle * Math.PI) / 180;
  const end = (endAngle * Math.PI) / 180;
  
  // Calculate start and end points
  const x1 = cx + radius * Math.cos(start);
  const y1 = cy + radius * Math.sin(start);
  const x2 = cx + radius * Math.cos(end);
  const y2 = cy + radius * Math.sin(end);
  
  // Determine if arc is large (> 180 degrees)
  const largeArc = Math.abs(endAngle - startAngle) > 180 ? 1 : 0;
  
  return `<path d="M ${x1},${y1} A ${radius},${radius} 0 ${largeArc},1 ${x2},${y2}" class="dxf-entity" />`;
}

/**
 * Convert LWPOLYLINE entity to SVG path
 */
function polylineToSvg(entity) {
  const points = entity.coordinates;
  if (points.length < 2) return null;
  
  let pathData = `M ${points[0][0]},${points[0][1]}`;
  
  for (let i = 1; i < points.length; i++) {
    pathData += ` L ${points[i][0]},${points[i][1]}`;
  }
  
  // Close path if polyline is closed
  if (entity.properties.closed) {
    pathData += ' Z';
  }
  
  return `<path d="${pathData}" class="dxf-entity" />`;
}

/**
 * Generate HTML content for DXF viewer with sidebar layout
 */
function generateDxfViewerHtml(dxfFiles, errorMessage = null) {
  if (errorMessage) {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <title>DXF Viewer</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; background: #1e1e1e; color: #cccccc; }
          .error { color: #f44336; background: #ffebee; padding: 15px; border-radius: 4px; }
        </style>
      </head>
      <body>
        <h1>DXF Viewer</h1>
        <div class="error">${errorMessage}</div>
      </body>
      </html>
    `;
  }

  // Generate file list for sidebar
  const fileListItems = dxfFiles.map((file, index) => `
    <div class="file-item" onclick="selectFile(${index})" data-file-index="${index}">
      <div class="file-name">${file.name}</div>
      <div class="file-info">${formatFileSize(file.size)}</div>
    </div>
  `).join('');

  // Pre-process all DXF files and store data
  const fileData = dxfFiles.map(file => {
    const maxFileSize = 5 * 1024 * 1024; // 5MB
    
    if (file.size > maxFileSize) {
      return {
        name: file.name,
        error: `File too large (${formatFileSize(file.size)}). Max: ${formatFileSize(maxFileSize)}`,
        entities: 0
      };
    }
    
    try {
      const dxfContent = fs.readFileSync(file.fullPath, 'utf8');
      const entities = parseDxfContent(dxfContent);
      
      const maxEntities = 1000;
      if (entities.length > maxEntities) {
        return {
          name: file.name,
          error: `Too many entities (${entities.length}). Max: ${maxEntities}`,
          entities: entities.length
        };
      }
      
      if (entities.length === 0) {
        return {
          name: file.name,
          error: 'No supported entities found',
          entities: 0
        };
      }
      
      return {
        name: file.name,
        svg: entitiesToSvg(entities),
        entities: entities.length,
        entityTypes: getEntityTypeCounts(entities)
      };
    } catch (error) {
      return {
        name: file.name,
        error: `Parse error: ${error.message}`,
        entities: 0
      };
    }
  });

  return `
    <!DOCTYPE html>
    <html>
    <head>
      <title>DXF Viewer</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          background: #1e1e1e; 
          color: #cccccc; 
          height: 100vh;
          overflow: hidden;
        }
        
        .container {
          display: flex;
          height: 100vh;
        }
        
        .sidebar {
          width: 300px;
          background: #252526;
          border-right: 1px solid #444;
          display: flex;
          flex-direction: column;
        }
        
        .sidebar-header {
          padding: 16px;
          border-bottom: 1px solid #444;
          background: #2d2d30;
        }
        
        .sidebar-title {
          font-size: 14px;
          font-weight: 600;
          color: #cccccc;
          margin-bottom: 8px;
        }
        
        .file-count {
          font-size: 12px;
          color: #888;
        }
        
        .file-list {
          flex: 1;
          overflow-y: auto;
          padding: 8px;
        }
        
        .file-item {
          padding: 12px;
          margin: 2px 0;
          border-radius: 4px;
          cursor: pointer;
          transition: background-color 0.2s;
          border: 1px solid transparent;
        }
        
        .file-item:hover {
          background: #2d2d30;
          border-color: #444;
        }
        
        .file-item.selected {
          background: #094771;
          border-color: #4fc3f7;
        }
        
        .file-name {
          font-size: 13px;
          color: #cccccc;
          margin-bottom: 4px;
          word-break: break-all;
        }
        
        .file-info {
          font-size: 11px;
          color: #888;
        }
        
        .viewer-area {
          flex: 1;
          display: flex;
          flex-direction: column;
          background: #1e1e1e;
        }
        
        .viewer-header {
          padding: 16px;
          border-bottom: 1px solid #444;
          background: #252526;
        }
        
        .viewer-title {
          font-size: 16px;
          font-weight: 600;
          color: #cccccc;
        }
        
        .viewer-content {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
          overflow: hidden;
        }
        
        .placeholder {
          text-align: center;
          color: #888;
        }
        
        .placeholder-icon {
          font-size: 48px;
          margin-bottom: 16px;
          opacity: 0.5;
        }
        
        .dxf-display {
          width: 100%;
          height: 100%;
          display: none;
          flex-direction: column;
        }
        
        .dxf-display.active {
          display: flex;
        }
        
        .dxf-info {
          padding: 12px 16px;
          background: #2d2d30;
          border-bottom: 1px solid #444;
          font-size: 12px;
          color: #888;
        }
        
        .dxf-graphics {
          flex: 1;
          background: #1a1a1a;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
        }
        
        .dxf-svg {
          max-width: 100%;
          max-height: 100%;
          width: auto;
          height: auto;
        }
        
        .dxf-entity {
          stroke: #4fc3f7;
          stroke-width: 1;
          fill: none;
          vector-effect: non-scaling-stroke;
        }
        
        .error-display {
          padding: 20px;
          text-align: center;
          color: #f44336;
        }
        
        .error-display .error-icon {
          font-size: 32px;
          margin-bottom: 12px;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="sidebar">
          <div class="sidebar-header">
            <div class="sidebar-title">DXF Files</div>
            <div class="file-count">${dxfFiles.length} file${dxfFiles.length !== 1 ? 's' : ''} found</div>
          </div>
          <div class="file-list">
            ${fileListItems}
          </div>
        </div>
        
        <div class="viewer-area">
          <div class="viewer-header">
            <div class="viewer-title">Select a DXF file to view</div>
          </div>
          <div class="viewer-content">
            <div class="placeholder" id="placeholder">
              <div class="placeholder-icon">📐</div>
              <div>Select a DXF file from the sidebar to view it</div>
            </div>
            
            ${fileData.map((data, index) => `
              <div class="dxf-display" id="display-${index}">
                ${data.error ? `
                  <div class="error-display">
                    <div class="error-icon">⚠️</div>
                    <div>${data.error}</div>
                  </div>
                ` : `
                  <div class="dxf-info">
                    ${data.name} • ${data.entities} entities
                    ${data.entityTypes ? ` • ${Object.entries(data.entityTypes).map(([type, count]) => `${count} ${type.toLowerCase()}${count !== 1 ? 's' : ''}`).join(', ')}` : ''}
                  </div>
                  <div class="dxf-graphics">
                    ${data.svg}
                  </div>
                `}
              </div>
            `).join('')}
          </div>
        </div>
      </div>
      
      <script>
        let selectedIndex = -1;
        
        function selectFile(index) {
          // Update sidebar selection
          document.querySelectorAll('.file-item').forEach((item, i) => {
            item.classList.toggle('selected', i === index);
          });
          
          // Update viewer content
          document.getElementById('placeholder').style.display = selectedIndex === index ? 'block' : 'none';
          document.querySelectorAll('.dxf-display').forEach((display, i) => {
            display.classList.toggle('active', i === index);
          });
          
          // Update header title
          const fileName = ${JSON.stringify(dxfFiles.map(f => f.name))};
          document.querySelector('.viewer-title').textContent = fileName[index];
          
          selectedIndex = index;
        }
      </script>
    </body>
    </html>
  `;
}

/**
 * Get entity type counts for display
 */
function getEntityTypeCounts(entities) {
  const counts = {};
  entities.forEach(entity => {
    counts[entity.type] = (counts[entity.type] || 0) + 1;
  });
  return counts;
}

/**
 * Utility functions
 */

function detectWorkspace() {
  try {
    const activeEditor = vscode.window.activeTextEditor;
    if (activeEditor && isYamlFile(activeEditor.document.fileName)) {
      updateLastYamlFile(activeEditor.document.fileName);
    } else {
      // Look for common YAML files in workspace
      if (vscode.workspace.workspaceFolders) {
        const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
        const commonFiles = ["keyboard.yaml", "config.yaml", "ergogen.yaml"];

        for (const file of commonFiles) {
          try {
            const filePath = path.join(workspaceRoot, file);
            if (fs.existsSync(filePath)) {
              updateLastYamlFile(filePath);
              break;
            }
          } catch (error) {
            // Skip this file and continue
            outputChannel.appendLine(
              `Warning: Could not check ${file}: ${error.message}`
            );
          }
        }
      }
    }
  } catch (error) {
    outputChannel.appendLine(
      `Warning: Workspace detection failed: ${error.message}`
    );
  }
}

function isYamlFile(filename) {
  return filename.endsWith(".yaml") || filename.endsWith(".yml");
}

function updateLastYamlFile(filePath) {
  state.lastActiveYamlFile = {
    fileName: path.basename(filePath),
    filePath: filePath,
    workingDir: path.dirname(filePath),
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
  const files = findYamlFiles();
  if (files.length === 0) {
    throw new Error("No YAML files found in workspace");
  }

  if (files.length === 1) {
    updateLastYamlFile(files[0]);
    return state.lastActiveYamlFile;
  }

  const fileItems = files.map(file => ({
    label: path.basename(file),
    description: path.relative(vscode.workspace.workspaceFolders[0].uri.fsPath, file),
    filePath: file
  }));

  const selected = await vscode.window.showQuickPick(fileItems, {
    placeHolder: "Select an Ergogen YAML file",
  });

  if (selected) {
    updateLastYamlFile(selected.filePath);
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

        if (
          stat.isDirectory() &&
          !item.startsWith(".") &&
          item !== "node_modules"
        ) {
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
    const yamlBaseName = path.basename(
      state.lastActiveYamlFile.fileName,
      path.extname(state.lastActiveYamlFile.fileName)
    );
    const filenameDir = path.join(workingDir, yamlBaseName);
    if (fs.existsSync(filenameDir)) {
      return filenameDir;
    }

    // Fallback: simple output directory
    const config = vscode.workspace.getConfiguration("ergogen-toolkit");
    const outputDirName = config.get("outputDirectory", "output");
    const simpleOutputDir = path.join(workingDir, outputDirName);
    if (fs.existsSync(simpleOutputDir)) {
      return simpleOutputDir;
    }
  }

  return null;
}

function scanForDxfFiles(dir) {
  const files = [];

  function scan(currentDir, relativePath = "") {
    try {
      const items = fs.readdirSync(currentDir);
      for (const item of items) {
        const fullPath = path.join(currentDir, item);
        const relPath = path.join(relativePath, item);

        if (fs.statSync(fullPath).isDirectory()) {
          scan(fullPath, relPath);
        } else if (item.toLowerCase().endsWith(".dxf")) {
          files.push({
            name: item,
            path: relPath,
            fullPath: fullPath,
            size: fs.statSync(fullPath).size,
            modified: fs.statSync(fullPath).mtime,
          });
        }
      }
    } catch (error) {
      outputChannel.appendLine(
        `Error scanning ${currentDir}: ${error.message}`
      );
    }
  }

  scan(dir);
  return files.sort((a, b) => a.path.localeCompare(b.path));
}

// Utility functions for file display
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

/**
 * Extension deactivation
 */
function deactivate() {
  if (outputChannel) {
    outputChannel.dispose();
  }
}

module.exports = {
  activate,
  deactivate,
};