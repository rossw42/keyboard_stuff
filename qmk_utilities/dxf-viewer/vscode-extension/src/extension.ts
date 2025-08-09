import * as vscode from "vscode";
import * as path from "path";
import * as fs from "fs";
import { spawn, ChildProcess } from "child_process";
import * as http from "http";

export function activate(context: vscode.ExtensionContext) {
  console.log("Ergogen DXF Viewer extension is now active");

  const provider = new ErgogenDxfViewerProvider(context.extensionUri);

  // Register commands
  const openViewerCommand = vscode.commands.registerCommand(
    "ergogen-dxf-viewer.openViewer",
    () => {
      provider.createOrShowPanel();
    }
  );

  const runErgogenCommand = vscode.commands.registerCommand(
    "ergogen-dxf-viewer.runErgogen",
    async () => {
      await provider.runErgogen();
    }
  );

  const refreshViewerCommand = vscode.commands.registerCommand(
    "ergogen-dxf-viewer.refreshViewer",
    () => {
      provider.refresh();
    }
  );

  context.subscriptions.push(
    openViewerCommand,
    runErgogenCommand,
    refreshViewerCommand
  );

  // Auto-detect Ergogen projects and show viewer
  if (vscode.workspace.workspaceFolders) {
    const hasErgogenFiles = vscode.workspace.workspaceFolders.some(() => {
      const yamlFiles = vscode.workspace.findFiles("**/*.yaml", null, 10);
      return yamlFiles;
    });

    if (hasErgogenFiles) {
      // Show notification to open DXF viewer
      vscode.window
        .showInformationMessage(
          "Ergogen project detected! Would you like to open the DXF viewer?",
          "Open Viewer"
        )
        .then((selection) => {
          if (selection === "Open Viewer") {
            provider.createOrShowPanel();
          }
        });
    }
  }

  // Watch for YAML file changes
  const yamlWatcher = vscode.workspace.createFileSystemWatcher("**/*.yaml");
  yamlWatcher.onDidChange(async () => {
    const config = vscode.workspace.getConfiguration("ergogen-dxf-viewer");
    if (config.get("autoRunErgogen")) {
      await provider.runErgogen();
    }
  });

  context.subscriptions.push(yamlWatcher);
}

class ErgogenDxfViewerProvider {
  private panel: vscode.WebviewPanel | undefined;
  private backendProcess: ChildProcess | undefined;
  private backendPort: number = 5002;

  constructor(private readonly extensionUri: vscode.Uri) {}

  public async createOrShowPanel() {
    const columnToShowIn = vscode.window.activeTextEditor
      ? vscode.ViewColumn.Beside
      : vscode.ViewColumn.One;

    if (this.panel) {
      this.panel.reveal(columnToShowIn);
      return;
    }

    // Start backend server
    await this.startBackend();

    // Create webview panel
    this.panel = vscode.window.createWebviewPanel(
      "ergogenDxfViewer",
      "Ergogen DXF Viewer",
      columnToShowIn,
      {
        enableScripts: true,
        retainContextWhenHidden: true,
        localResourceRoots: [this.extensionUri],
      }
    );

    // Set webview content
    this.panel.webview.html = this.getWebviewContent();

    // Handle panel disposal
    this.panel.onDidDispose(() => {
      this.panel = undefined;
      this.stopBackend();
    });

    // Configure DXF viewer directory
    await this.configureDxfDirectory();
  }

  private async startBackend() {
    try {
      // Use fixed port for now (can be made configurable later)
      this.backendPort = 5002;

      // Get backend path (bundled with extension)
      const backendPath = vscode.Uri.joinPath(this.extensionUri, "backend");
      const appPath = vscode.Uri.joinPath(backendPath, "app.py").fsPath;

      // Start Flask backend
      this.backendProcess = spawn("python3", [appPath], {
        cwd: backendPath.fsPath,
        env: { ...process.env, PORT: this.backendPort.toString() },
      });

      this.backendProcess.stdout?.on("data", (data) => {
        console.log(`Backend: ${data}`);
      });

      this.backendProcess.stderr?.on("data", (data) => {
        console.error(`Backend Error: ${data}`);
      });

      // Wait for backend to start
      await new Promise((resolve) => setTimeout(resolve, 3000));

      vscode.window.showInformationMessage(
        `DXF Viewer backend started on port ${this.backendPort}`
      );
    } catch (error) {
      vscode.window.showErrorMessage(
        `Failed to start DXF viewer backend: ${error}`
      );
    }
  }

  private stopBackend() {
    if (this.backendProcess) {
      this.backendProcess.kill("SIGTERM");
      this.backendProcess = undefined;
    }
  }

  private async configureDxfDirectory() {
    if (!vscode.workspace.workspaceFolders) return;

    // Look for output directory in workspace
    const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;
    const outputDir = path.join(workspaceRoot, "output");

    if (fs.existsSync(outputDir)) {
      // Configure backend to use this directory
      try {
        const postData = JSON.stringify({ path: outputDir });

        const options = {
          hostname: "localhost",
          port: this.backendPort,
          path: "/api/directory",
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(postData),
          },
        };

        const req = http.request(options, (res) => {
          if (res.statusCode === 200) {
            console.log(`Configured DXF viewer to watch: ${outputDir}`);
          } else {
            console.error("Failed to configure DXF directory");
          }
        });

        req.on("error", (error) => {
          console.error("Error configuring DXF directory:", error);
        });

        req.write(postData);
        req.end();
      } catch (error) {
        console.error("Error configuring DXF directory:", error);
      }
    }
  }

  public async runErgogen() {
    if (!vscode.workspace.workspaceFolders) {
      vscode.window.showErrorMessage("No workspace folder found");
      return;
    }

    const config = vscode.workspace.getConfiguration("ergogen-dxf-viewer");
    const ergogenCommand = config.get<string>("ergogenCommand", "ergogen");
    const workspaceRoot = vscode.workspace.workspaceFolders[0].uri.fsPath;

    // Find YAML files in workspace
    const yamlFiles = await vscode.workspace.findFiles("**/*.yaml", null, 10);

    if (yamlFiles.length === 0) {
      vscode.window.showErrorMessage("No YAML files found in workspace");
      return;
    }

    // Use the first YAML file or let user choose
    let configFile = yamlFiles[0].fsPath;
    if (yamlFiles.length > 1) {
      const items = yamlFiles.map((file) => ({
        label: path.basename(file.fsPath),
        description: vscode.workspace.asRelativePath(file),
        filePath: file.fsPath,
      }));

      const selected = await vscode.window.showQuickPick(items, {
        placeHolder: "Select Ergogen config file",
      });

      if (!selected) return;
      configFile = selected.filePath;
    }

    // Show progress
    vscode.window.withProgress(
      {
        location: vscode.ProgressLocation.Notification,
        title: "Running Ergogen...",
        cancellable: false,
      },
      async () => {
        return new Promise<void>((resolve, reject) => {
          const ergogenProcess = spawn(ergogenCommand, [configFile], {
            cwd: workspaceRoot,
          });

          ergogenProcess.stdout?.on("data", (data) => {
            console.log(`Ergogen: ${data}`);
          });

          ergogenProcess.stderr?.on("data", (data) => {
            console.error(`Ergogen Error: ${data}`);
          });

          ergogenProcess.on("close", (code) => {
            if (code === 0) {
              vscode.window.showInformationMessage(
                "Ergogen completed successfully!"
              );
              this.refresh();
              resolve();
            } else {
              vscode.window.showErrorMessage(
                `Ergogen failed with code ${code}`
              );
              reject(new Error(`Ergogen failed with code ${code}`));
            }
          });
        });
      }
    );
  }

  public refresh() {
    if (this.panel) {
      this.panel.webview.postMessage({ command: "refresh" });
    }
  }

  private getWebviewContent(): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ergogen DXF Viewer</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden;
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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: #666;
        }
    </style>
</head>
<body>
    <div id="loading" class="loading">
        <div>
            <h3>🚀 Starting DXF Viewer...</h3>
            <p>Loading Ergogen DXF files...</p>
        </div>
    </div>
    <iframe id="viewer" src="http://localhost:${this.backendPort}" style="display: none;"></iframe>
    
    <script>
        // Show iframe when loaded
        const iframe = document.getElementById('viewer');
        const loading = document.getElementById('loading');
        
        iframe.onload = function() {
            loading.style.display = 'none';
            iframe.style.display = 'block';
        };
        
        // Handle messages from extension
        window.addEventListener('message', event => {
            const message = event.data;
            if (message.command === 'refresh') {
                iframe.src = iframe.src; // Reload iframe
            }
        });
        
        // Show iframe after delay if onload doesn't fire
        setTimeout(() => {
            if (iframe.style.display === 'none') {
                loading.style.display = 'none';
                iframe.style.display = 'block';
            }
        }, 5000);
    </script>
</body>
</html>`;
  }
}

export function deactivate() {
  // Extension cleanup handled by panel disposal
}
