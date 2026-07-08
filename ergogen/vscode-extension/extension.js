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
  viewerPanel: null,
  previewPanel: null,
  previewDocUri: null,
  previewTimer: null,
  ergogenModule: null,
  ergogenModulePath: null,
};

// Cache of injected custom footprints: fullPath -> { mtimeMs, name }
const footprintCache = new Map();

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

  // Live preview command (in-process ergogen, like the web UI)
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "ergogen-toolkit.openLivePreview",
      async () => {
        await openLivePreview();
      }
    )
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

        // If the live preview is open, follow the active YAML file
        if (state.previewPanel) {
          state.previewDocUri = editor.document.uri.toString();
          updateLivePreview(editor.document);
        }
      }
    })
  );

  // Live preview: re-render as the user types (debounced)
  context.subscriptions.push(
    vscode.workspace.onDidChangeTextDocument((event) => {
      if (!state.previewPanel) return;
      if (event.document.uri.toString() !== state.previewDocUri) return;

      const config = vscode.workspace.getConfiguration("ergogen-toolkit");
      const delay = config.get("previewDebounce", 400);
      clearTimeout(state.previewTimer);
      state.previewTimer = setTimeout(
        () => updateLivePreview(event.document),
        delay
      );
    })
  );

  // Auto-run Ergogen when a previously-run YAML file is saved
  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(async (document) => {
      const config = vscode.workspace.getConfiguration("ergogen-toolkit");
      if (!config.get("runOnSave", true)) return;
      if (!isYamlFile(document.fileName)) return;

      // Only auto-run for the file the user has already run Ergogen on
      if (
        state.lastActiveYamlFile &&
        state.currentOutputDir &&
        document.fileName === state.lastActiveYamlFile.filePath &&
        !state.isProcessing
      ) {
        outputChannel.appendLine("💾 YAML saved — re-running Ergogen...");
        await runErgogen();
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

    // Custom footprint support: the ergogen CLI only loads a `footprints`
    // folder when it is passed a *folder* containing a `config.yaml`.
    // If footprint sources exist (a footprints folder near the YAML and/or
    // configured footprintLibraries), stage a build folder
    // (config.yaml copy + footprints) and run ergogen on that instead.
    let targetArg = yamlFile.fileName;
    const footprintSources = getFootprintSources(yamlFile.filePath);
    if (footprintSources.length > 0) {
      const stageDir = path.join(workingDir, ".ergogen-build");
      outputChannel.appendLine(`📦 Staging custom footprints in ${stageDir}`);
      fs.mkdirSync(stageDir, { recursive: true });
      fs.copyFileSync(yamlFile.filePath, path.join(stageDir, "config.yaml"));
      const copyFilter = (src) => {
        const base = path.basename(src);
        if (base === ".git" || base === "node_modules") return false;
        try {
          if (fs.statSync(src).isDirectory()) return true;
        } catch (e) {
          return false;
        }
        return base.endsWith(".js");
      };
      for (const source of footprintSources) {
        const dest = source.prefix
          ? path.join(stageDir, "footprints", source.prefix)
          : path.join(stageDir, "footprints");
        outputChannel.appendLine(`  ${source.dir} -> ${dest}`);
        fs.cpSync(source.dir, dest, {
          recursive: true,
          force: true,
          filter: copyFilter,
        });
      }
      targetArg = stageDir;
    }

    // Quote paths since spawn uses shell:true (handles spaces in paths)
    const args = ["-o", `"${outputDir}"`, `"${targetArg}"`];

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

              // Auto-refresh the DXF viewer if it's open
              refreshViewerPanel();

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
 * ===================== LIVE PREVIEW =====================
 * Uses the ergogen node module in-process (like the ergogen web UI)
 * to render the points demo + outlines as SVG while you type.
 */

/**
 * Locate and require the ergogen node module
 */
function resolveErgogenModule() {
  if (state.ergogenModule) return state.ergogenModule;

  const config = vscode.workspace.getConfiguration("ergogen-toolkit");
  const candidates = [];

  const configured = config.get("ergogenModulePath", "");
  if (configured) candidates.push(configured);

  // Global npm root (where `npm i -g ergogen` puts it)
  try {
    const { execSync } = require("child_process");
    const npmRoot = execSync("npm root -g", {
      encoding: "utf8",
      shell: true,
      windowsHide: true,
    }).trim();
    if (npmRoot) candidates.push(path.join(npmRoot, "ergogen"));
  } catch (e) {
    outputChannel.appendLine(`Could not query npm root -g: ${e.message}`);
  }

  for (const candidate of candidates) {
    try {
      const mod = require(candidate);
      if (mod && typeof mod.process === "function") {
        outputChannel.appendLine(
          `✅ Loaded ergogen module v${mod.version} from: ${candidate}`
        );
        state.ergogenModule = mod;
        state.ergogenModulePath = candidate;
        return mod;
      }
    } catch (e) {
      outputChannel.appendLine(
        `Could not load ergogen from ${candidate}: ${e.message}`
      );
    }
  }
  return null;
}

/**
 * Find a `footprints` folder next to (or up to 3 levels above) a directory.
 * This mirrors the ergogen CLI convention of a footprints folder living
 * alongside the config file.
 */
function findFootprintsDir(startDir) {
  let dir = startDir;
  for (let i = 0; i < 4; i++) {
    const candidate = path.join(dir, "footprints");
    try {
      if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
        return candidate;
      }
    } catch (e) {
      // ignore and keep walking up
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

/**
 * Collect all footprint sources for a config file:
 *  - a `footprints` folder near the file (subfolders become namespaces,
 *    matching the ergogen CLI folder convention), and
 *  - configured global libraries from the `ergogen-toolkit.footprintLibraries`
 *    setting, an object mapping namespace -> folder path, e.g.
 *    { "ceoloide": "D:\\GitHub2\\ergogen-footprints" }.
 * Returns an array of { dir, prefix }.
 */
function getFootprintSources(documentPath) {
  const sources = [];

  if (documentPath) {
    const local = findFootprintsDir(path.dirname(documentPath));
    if (local) sources.push({ dir: local, prefix: "" });
  }

  const config = vscode.workspace.getConfiguration("ergogen-toolkit");
  const libraries = config.get("footprintLibraries", {}) || {};
  for (const [namespace, libPath] of Object.entries(libraries)) {
    if (!namespace || !libPath) continue;
    try {
      if (fs.existsSync(libPath) && fs.statSync(libPath).isDirectory()) {
        sources.push({ dir: libPath, prefix: namespace });
      } else {
        outputChannel.appendLine(
          `⚠ footprintLibraries["${namespace}"] not found: ${libPath}`
        );
      }
    } catch (e) {
      outputChannel.appendLine(
        `⚠ footprintLibraries["${namespace}"] error: ${e.message}`
      );
    }
  }

  return sources;
}

/**
 * Inject custom footprints into the in-process ergogen module so the live
 * preview works with configs that reference them (e.g. ceoloide/switch_mx).
 *
 * Replicates what the ergogen CLI's folder/zip handling (io.unpack) does:
 * every `footprints/<subpath>/<name>.js` is compiled with a sandboxed
 * require (only makerjs + package.json are available) and registered as
 * `<subpath>/<name>` via ergogen.inject('footprint', name, fp).
 *
 * Returns the number of footprints available (injected or cached).
 */
function injectCustomFootprints(ergogen, documentPath) {
  if (!ergogen || typeof ergogen.inject !== "function") return 0;

  const sources = getFootprintSources(documentPath);
  if (sources.length === 0) return 0;

  // makerjs is the only real dependency ergogen footprints may require;
  // resolve it from the ergogen module's own dependency tree.
  let makerjs = null;
  try {
    makerjs = require(
      require.resolve("makerjs", {
        paths: [state.ergogenModulePath || __dirname],
      })
    );
  } catch (e) {
    // footprints that don't require makerjs will still work
  }

  const fakeRequire = (name) => {
    if (name.endsWith("package.json")) {
      return { version: (state.ergogenModule && state.ergogenModule.version) || "0.0.0" };
    }
    if (name === "makerjs" && makerjs) return makerjs;
    throw new Error(`Unknown dependency "${name}" in custom footprint`);
  };

  let available = 0;
  const walk = (dir, prefix) => {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (e) {
      return;
    }
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === ".git" || entry.name === "node_modules") continue;
        walk(full, prefix ? `${prefix}/${entry.name}` : entry.name);
      } else if (entry.name.endsWith(".js")) {
        // io.unpack naming: path after footprints/, extension stripped
        const name = (prefix ? `${prefix}/` : "") + entry.name.split(".")[0];
        try {
          const stat = fs.statSync(full);
          const cached = footprintCache.get(full);
          if (cached && cached.mtimeMs === stat.mtimeMs && cached.name === name) {
            available++;
            continue; // already injected, footprint registry persists
          }
          const text = fs.readFileSync(full, "utf8");
          const parsed = new Function(
            "require",
            "const module = {};\n\n" + text + "\n\nreturn module.exports;"
          )(fakeRequire);
          ergogen.inject("footprint", name, parsed);
          footprintCache.set(full, { mtimeMs: stat.mtimeMs, name });
          available++;
        } catch (e) {
          outputChannel.appendLine(
            `⚠ Could not inject footprint "${name}": ${e.message}`
          );
        }
      }
    }
  };
  for (const source of sources) {
    walk(source.dir, source.prefix);
  }

  if (available > 0) {
    outputChannel.appendLine(
      `🧩 ${available} custom footprint(s) available from: ` +
        sources.map((s) => (s.prefix ? `${s.dir} as "${s.prefix}/*"` : s.dir)).join(", ")
    );
  }
  return available;
}

/**
 * Open (or reveal) the live preview panel for the active YAML file
 */
async function openLivePreview() {
  const editor = vscode.window.activeTextEditor;
  if (!editor || !isYamlFile(editor.document.fileName)) {
    vscode.window.showWarningMessage(
      "Open an Ergogen YAML file first, then run Ergogen: Open Live Preview."
    );
    return;
  }

  const ergogen = resolveErgogenModule();
  if (!ergogen) {
    vscode.window.showErrorMessage(
      "Could not load the ergogen node module. Install it globally (npm i -g ergogen) " +
        "or set 'ergogen-toolkit.ergogenModulePath' to the module folder."
    );
    return;
  }

  state.previewDocUri = editor.document.uri.toString();

  if (!state.previewPanel) {
    const panel = vscode.window.createWebviewPanel(
      "ergogenLivePreview",
      "Ergogen Preview",
      vscode.ViewColumn.Beside,
      { enableScripts: true, retainContextWhenHidden: true }
    );
    panel.webview.html = generateLivePreviewHtml();
    panel.onDidDispose(() => {
      if (state.previewPanel === panel) {
        state.previewPanel = null;
      }
    });
    state.previewPanel = panel;
  } else {
    state.previewPanel.reveal(vscode.ViewColumn.Beside, true);
  }

  await updateLivePreview(editor.document);
}

/**
 * Run ergogen in-process on the document text and push SVGs to the webview
 */
async function updateLivePreview(document) {
  if (!state.previewPanel) return;
  const ergogen = resolveErgogenModule();
  if (!ergogen) return;

  const raw = document.getText();
  const title = path.basename(document.fileName);

  try {
    // Make custom footprints (footprints/ folder next to the YAML)
    // available before processing, like the CLI does for folders.
    injectCustomFootprints(ergogen, document.fileName);

    const results = await ergogen.process(raw, true, () => {});

    const items = [];
    if (results.demo && results.demo.svg) {
      items.push({ name: "⌨ demo (points)", svg: results.demo.svg });
    }
    for (const [name, outline] of Object.entries(results.outlines || {})) {
      if (outline && outline.svg) {
        items.push({ name: `▢ ${name}`, svg: outline.svg });
      }
    }

    state.previewPanel.webview.postMessage({
      command: "update",
      title,
      items,
      error: null,
    });
  } catch (error) {
    // Keep last good render; just surface the error banner
    state.previewPanel.webview.postMessage({
      command: "update",
      title,
      items: null,
      error: error.message,
    });
  }
}

/**
 * Static HTML shell for the live preview panel.
 * Content is updated via postMessage so tab selection/zoom survive re-renders.
 */
function generateLivePreviewHtml() {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8" />
      <title>Ergogen Preview</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          background: #1e1e1e; color: #cccccc;
          height: 100vh; overflow: hidden;
        }
        .container { display: flex; flex-direction: column; height: 100vh; }
        .header {
          padding: 8px 12px; background: #252526; border-bottom: 1px solid #444;
          display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
        }
        .title { font-size: 13px; font-weight: 600; }
        .status { font-size: 11px; color: #888; }
        .error-banner {
          display: none; padding: 8px 12px; background: #5a1d1d; color: #ff8a80;
          font-size: 12px; font-family: Consolas, monospace; white-space: pre-wrap;
          border-bottom: 1px solid #7f2a2a; max-height: 120px; overflow-y: auto;
        }
        .error-banner.visible { display: block; }
        .tabs {
          display: flex; gap: 4px; padding: 6px 8px; background: #2d2d30;
          border-bottom: 1px solid #444; overflow-x: auto; flex-shrink: 0;
        }
        .tab {
          padding: 4px 10px; font-size: 12px; border-radius: 3px; cursor: pointer;
          background: transparent; color: #aaa; border: 1px solid transparent;
          white-space: nowrap;
        }
        .tab:hover { background: #3a3a3d; }
        .tab.active { background: #094771; color: #fff; border-color: #4fc3f7; }
        .canvas {
          flex: 1; display: flex; align-items: center; justify-content: center;
          overflow: hidden; background: #1a1a1a; position: relative;
        }
        .canvas svg {
          max-width: 95%; max-height: 95%; width: auto; height: auto;
        }
        .canvas svg path, .canvas svg line, .canvas svg circle, .canvas svg polyline {
          stroke: #4fc3f7 !important;
          fill: none !important;
          vector-effect: non-scaling-stroke;
        }
        .canvas svg text { fill: #cccccc !important; stroke: none !important; }
        .placeholder { color: #666; text-align: center; }
        .placeholder .icon { font-size: 42px; opacity: 0.5; margin-bottom: 12px; }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <span class="title" id="title">Ergogen Preview</span>
          <span class="status" id="status">waiting for input…</span>
        </div>
        <div class="error-banner" id="error"></div>
        <div class="tabs" id="tabs"></div>
        <div class="canvas" id="canvas">
          <div class="placeholder">
            <div class="icon">⌨</div>
            <div>Edit your Ergogen YAML — the preview updates as you type</div>
          </div>
        </div>
      </div>
      <script>
        let items = [];
        let selectedName = null;

        const tabsEl = document.getElementById('tabs');
        const canvasEl = document.getElementById('canvas');
        const errorEl = document.getElementById('error');
        const titleEl = document.getElementById('title');
        const statusEl = document.getElementById('status');

        function renderTabs() {
          tabsEl.innerHTML = '';
          items.forEach((item) => {
            const tab = document.createElement('div');
            tab.className = 'tab' + (item.name === selectedName ? ' active' : '');
            tab.textContent = item.name;
            tab.onclick = () => { selectedName = item.name; render(); };
            tabsEl.appendChild(tab);
          });
        }

        function renderCanvas() {
          const item = items.find(i => i.name === selectedName);
          if (item) {
            canvasEl.innerHTML = item.svg;
          } else if (items.length === 0) {
            canvasEl.innerHTML = '<div class="placeholder"><div class="icon">⌨</div><div>No preview available</div></div>';
          }
        }

        function render() { renderTabs(); renderCanvas(); }

        window.addEventListener('message', (event) => {
          const msg = event.data;
          if (msg.command !== 'update') return;

          titleEl.textContent = 'Ergogen Preview — ' + msg.title;

          if (msg.error) {
            errorEl.textContent = msg.error;
            errorEl.classList.add('visible');
            statusEl.textContent = 'error (showing last good render)';
            return; // keep previous good render
          }

          errorEl.classList.remove('visible');
          items = msg.items || [];
          statusEl.textContent = items.length + ' view' + (items.length !== 1 ? 's' : '') +
            ' • updated ' + new Date().toLocaleTimeString();

          // Preserve selection if possible, otherwise select first item
          if (!items.some(i => i.name === selectedName)) {
            selectedName = items.length ? items[0].name : null;
          }
          render();
        });
      </script>
    </body>
    </html>
  `;
}

/**
 * Refresh the open DXF viewer panel (if any) with the latest files
 */
function refreshViewerPanel() {
  if (!state.viewerPanel) return;
  try {
    const outputDir = getOutputDirectory();
    if (outputDir && fs.existsSync(outputDir)) {
      const dxfFiles = scanForDxfFiles(outputDir);
      state.viewerPanel.webview.html = generateDxfViewerHtml(dxfFiles);
      outputChannel.appendLine(
        `📂 Auto-refreshed DXF viewer with ${dxfFiles.length} files`
      );
    }
  } catch (error) {
    outputChannel.appendLine(`Warning: viewer refresh failed: ${error.message}`);
  }
}

/**
 * Create DXF viewer webview panel
 */
function createDxfViewerPanel(dxfFiles, errorMessage = null) {
  // Reuse existing panel if open
  if (state.viewerPanel) {
    state.viewerPanel.webview.html = generateDxfViewerHtml(dxfFiles, errorMessage);
    state.viewerPanel.reveal(vscode.ViewColumn.Beside, true);
    return;
  }

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

  state.viewerPanel = panel;
  panel.onDidDispose(() => {
    if (state.viewerPanel === panel) {
      state.viewerPanel = null;
    }
  });

  // Generate HTML content
  panel.webview.html = generateDxfViewerHtml(dxfFiles, errorMessage);
  
  // Handle messages from webview
  panel.webview.onDidReceiveMessage(
    async message => {
      switch (message.command) {
        case 'runErgogen':
          outputChannel.appendLine('🔄 Running Ergogen from DXF viewer...');
          await runErgogen();
          break;
        case 'refreshViewer':
          outputChannel.appendLine('🔄 Refreshing DXF viewer...');
          // Re-scan for DXF files and update the panel
          const outputDir = getOutputDirectory();
          if (outputDir && fs.existsSync(outputDir)) {
            const newDxfFiles = scanForDxfFiles(outputDir);
            panel.webview.html = generateDxfViewerHtml(newDxfFiles);
            outputChannel.appendLine(`📂 Refreshed viewer with ${newDxfFiles.length} files`);
          } else {
            panel.webview.html = generateDxfViewerHtml([], "No DXF files found. Run Ergogen to generate files.");
          }
          break;
      }
    },
    undefined,
    []
  );
  
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
          margin-bottom: 12px;
        }
        
        .action-buttons {
          display: flex;
          gap: 8px;
        }
        
        .action-button {
          padding: 6px 12px;
          background: #0e639c;
          color: white;
          border: none;
          border-radius: 3px;
          font-size: 11px;
          cursor: pointer;
          transition: background-color 0.2s;
        }
        
        .action-button:hover {
          background: #1177bb;
        }
        
        .action-button:disabled {
          background: #555;
          cursor: not-allowed;
        }
        
        .action-button.secondary {
          background: #555;
        }
        
        .action-button.secondary:hover {
          background: #666;
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
            <div class="action-buttons">
              <button class="action-button" onclick="runErgogen()">▶ Run Ergogen</button>
              <button class="action-button secondary" onclick="refreshViewer()">🔄 Refresh</button>
            </div>
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
        
        // Acquire VS Code API once at startup
        const vscode = (typeof acquireVsCodeApi !== 'undefined') ? acquireVsCodeApi() : null;
        
        function runErgogen() {
          console.log('Run Ergogen button clicked');
          const button = event.target;
          const originalText = button.textContent;
          
          // Disable button and show loading state
          button.disabled = true;
          button.textContent = '⏳ Running...';
          
          if (vscode) {
            vscode.postMessage({ command: 'runErgogen' });
            
            // Re-enable button after a delay
            setTimeout(() => {
              button.disabled = false;
              button.textContent = originalText;
            }, 3000);
          } else {
            console.error('VS Code API not available');
            button.disabled = false;
            button.textContent = originalText;
          }
        }
        
        function refreshViewer() {
          console.log('Refresh button clicked');
          const button = event.target;
          const originalText = button.textContent;
          
          // Disable button and show loading state
          button.disabled = true;
          button.textContent = '⏳ Refreshing...';
          
          if (vscode) {
            vscode.postMessage({ command: 'refreshViewer' });
            
            // Re-enable button after a delay
            setTimeout(() => {
              button.disabled = false;
              button.textContent = originalText;
            }, 1000);
          } else {
            console.error('VS Code API not available');
            button.disabled = false;
            button.textContent = originalText;
          }
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

    // Check if we're in a directory that already contains DXF files
    if (containsDxfFiles(workingDir)) {
      return workingDir;
    }

    // Fallback: simple output directory
    const config = vscode.workspace.getConfiguration("ergogen-toolkit");
    const outputDirName = config.get("outputDirectory", "output");
    const simpleOutputDir = path.join(workingDir, outputDirName);
    if (fs.existsSync(simpleOutputDir)) {
      return simpleOutputDir;
    }
  }

  // Last resort: scan workspace for any DXF files
  if (vscode.workspace.workspaceFolders) {
    const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
    const dxfDir = findDxfDirectory(workspaceRoot);
    if (dxfDir) {
      return dxfDir;
    }
  }

  return null;
}

/**
 * Check if directory contains DXF files
 */
function containsDxfFiles(dir) {
  try {
    const items = fs.readdirSync(dir);
    return items.some(item => item.toLowerCase().endsWith('.dxf'));
  } catch (error) {
    return false;
  }
}

/**
 * Find directory containing DXF files in workspace
 */
function findDxfDirectory(rootDir, depth = 0) {
  if (depth > 4) return null; // Limit search depth
  
  try {
    const items = fs.readdirSync(rootDir);
    
    // Check if current directory has DXF files
    if (items.some(item => item.toLowerCase().endsWith('.dxf'))) {
      return rootDir;
    }
    
    // Search subdirectories
    for (const item of items) {
      if (item.startsWith('.') || item === 'node_modules') continue;
      
      const fullPath = path.join(rootDir, item);
      try {
        if (fs.statSync(fullPath).isDirectory()) {
          const result = findDxfDirectory(fullPath, depth + 1);
          if (result) return result;
        }
      } catch (error) {
        // Skip inaccessible directories
        continue;
      }
    }
  } catch (error) {
    // Skip inaccessible directories
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