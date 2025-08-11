# Running Ergogen Toolkit Extension in Development Mode

Since you're encountering Node.js version compatibility issues with vsce, here's how to run the extension in development mode:

## Steps:

1. **Open the extension folder in a new VSCode window:**
   - Open VSCode
   - File → Open Folder
   - Navigate to and select the `ergogen/ergogen-toolkit` folder
   - Click "Open"

2. **Run the extension:**
   - Press `F5` or go to Run → Start Debugging
   - This will open a new "Extension Development Host" window
   - The extension will be active in this new window

3. **Use the extension:**
   - In the Extension Development Host window, open your Ergogen YAML files
   - The extension commands should now be available:
     - `Ctrl+Shift+P` → type "Ergogen" to see available commands
     - `Ctrl+Shift+D` (or `Cmd+Shift+D` on Mac) to open DXF viewer
     - `Ctrl+Shift+E` (or `Cmd+Shift+E` on Mac) to run Ergogen

## Alternative: Install without packaging

If you want to install the extension permanently without packaging, you can:

1. Copy the extension folder to VSCode's extensions directory:
   ```bash
   cp -r ergogen/ergogen-toolkit ~/.vscode/extensions/ergogen-toolkit-3.0.0
   ```

2. Restart VSCode - the extension should be available globally.

## Troubleshooting Node Version (Optional)

If you want to fix the vsce packaging issue, you would need to upgrade Node.js to version 20.18.1 or higher:

```bash
# Using mise (which you appear to have):
mise install node@20.18.1
mise use node@20.18.1
```

Then try `vsce package` again.
