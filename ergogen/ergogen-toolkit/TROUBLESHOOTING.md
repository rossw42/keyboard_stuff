# Troubleshooting Ergogen Toolkit Extension

## Issue: Command 'ergogen-toolkit.openViewer' not found

The extension configuration is correct, but the command isn't being registered. This usually indicates an activation issue.

### Step 1: Check Extension Activation

1. **Open the extension folder in VSCode:**
   ```
   File → Open Folder → Select ergogen/ergogen-toolkit
   ```

2. **Open the Developer Console:**
   ```
   Help → Toggle Developer Tools → Console tab
   ```

3. **Run the extension in debug mode:**
   ```
   Press F5 (or Run → Start Debugging)
   ```

4. **In the Extension Development Host window, check for activation:**
   - Open Developer Console: `Help → Toggle Developer Tools → Console`
   - Look for activation messages like:
     ```
     🚀 Ergogen Toolkit v2.0.0 activating...
     Extension activated
     🎹 Ergogen Toolkit ready!
     ```

### Step 2: Force Extension Activation

The extension should auto-activate when you open YAML files. Try:

1. **In the Extension Development Host window:**
   - Open any `.yaml` or `.yml` file
   - Or run: `Ctrl+Shift+P` → type "Ergogen" to trigger activation

2. **Check the command palette:**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Ergogen" - you should see available commands

### Step 3: Check for Errors

1. **Look for errors in the Developer Console**
2. **Check the Output panel:**
   - `View → Output`
   - Select "Ergogen Toolkit" from dropdown

### Step 4: Manual Installation (Alternative)

If development mode isn't working, try installing the packaged extension:

```bash
# Install the pre-built package
code --install-extension ergogen/ergogen-toolkit/ergogen-toolkit-3.0.0.vsix
```

Then restart VSCode and try the commands.

### Step 5: Verify Dependencies

If you still have issues, reinstall dependencies:

```bash
cd ergogen/ergogen-toolkit
npm install
```

### Expected Behavior

When working correctly, you should see:
- ✅ Status bar item with "DXF" button
- ✅ Commands available in Command Palette under "Ergogen"
- ✅ Keyboard shortcuts: `Ctrl+Shift+D` for viewer, `Ctrl+Shift+E` for running Ergogen
- ✅ Right-click context menu on YAML files

### Debug Commands to Try

In the Extension Development Host, try these commands manually:

1. Open Command Palette (`Ctrl+Shift+P`)
2. Try these exact commands:
   - `Ergogen: Open DXF Viewer`
   - `Ergogen: Run Ergogen`
   - `Ergogen: Generate Connection Diagram`

If none appear, the extension didn't activate properly.

### Common Issues

1. **Node.js version mismatch** - Extension requires Node.js for dependencies
2. **Missing dependencies** - Run `npm install` in the extension directory
3. **VSCode version compatibility** - Extension requires VSCode ^1.102.0
4. **File permissions** - Ensure you can read/write in the extension directory

### Still Not Working?

If commands still don't appear:
1. Close all VSCode windows
2. Restart VSCode completely
3. Try the manual installation method (Step 4)
4. Check VSCode Extensions view to see if it's listed and enabled
