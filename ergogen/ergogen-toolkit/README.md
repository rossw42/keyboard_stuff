# Connection Diagram Generator for Ergogen Toolkit

This VSCode extension now includes an automated **Connection Diagram Generator** that creates detailed markdown documentation of your keyboard's physical layout and electrical connections directly from ergogen YAML files.

## 🌟 New Feature: Automated Connection Diagrams

The Connection Diagram Generator automatically analyzes your ergogen configuration files and generates comprehensive documentation including:

- **Physical Layout Diagrams**: ASCII-art representation of your keyboard layout
- **Electrical Connection Matrix**: Complete pin mapping tables for columns and rows  
- **Special Connections**: Encoder, OLED, and other component wiring details
- **Matrix Scanning Logic**: Technical details about keyboard scanning approach
- **Key Layout Details**: Analysis of key sizes, special keys, and components
- **Physical Dimensions**: Spacing and measurement information

## 🚀 How It Works

### Automatic Generation
When you run ergogen with this extension, connection diagrams are automatically generated alongside your DXF and other output files. No LLM required!

```
Your Project/
├── config.yaml           # Your ergogen config
├── config/               # Generated ergoen outputs
│   ├── pcbs/
│   ├── outlines/
│   └── keyboard_connection_diagram.md  # 🆕 Auto-generated!
```

### Manual Generation
You can also generate diagrams manually:

1. **Command Palette**: `Ctrl+Shift+P` → "Generate Connection Diagram"
2. **Right-click menu**: Right-click on any YAML file → "Generate Connection Diagram"

## 📋 Configuration

The connection diagram generator can be configured in VSCode settings:

```json
{
  "ergogen-toolkit.generateConnectionDiagram": true,  // Enable/disable auto-generation
}
```

## 🔧 What Gets Analyzed

The generator extracts information from your ergogen YAML files including:

### Layout Information
- Zone definitions and key positions
- Special key sizes (2U, 1.5U, etc.)
- Component placement (encoders, OLED screens, MCU)

### Electrical Information  
- Column and row network assignments
- Pro Micro pin mappings
- Diode configurations
- I2C connections for displays

### Physical Information
- Key spacing and dimensions
- Component distances
- Case and mounting details

## 📊 Example Output

Here's what the generated connection diagram looks like:

```markdown
# My Keyboard Connection Diagram

## Physical Layout Diagram
```
┌─────────────────────────────────────────┐
│              MY KEYBOARD                │
├──────────┬──────────────┬───────────────┤
│   NAV    │   MAIN GRID  │  COMPONENTS   │
│          │              │               │
└──────────┴──────────────┴───────────────┘
```

## Electrical Connection Matrix

### Column Networks:
| Column | Pro Micro Pin | Connected Keys |
|--------|---------------|----------------|
| col0   | P0           | NumLock, 7, 4, 1, 0 |
| col1   | P1           | /, 8, 5, 2 |
...
```

## 🛠️ Integration Details

### How It Integrates with Ergogen
1. **Automatic Trigger**: Runs after successful ergogen execution
2. **Smart Parsing**: Analyzes YAML structure to extract layout and electrical data
3. **Template Generation**: Uses parsed data to generate structured markdown
4. **File Output**: Saves alongside other ergogen outputs

### No LLM Required!
Unlike the original manually-created diagram, this automated version:
- ✅ Parses YAML configurations programmatically
- ✅ Extracts electrical and physical data automatically  
- ✅ Generates consistent, structured output
- ✅ Updates automatically when configs change
- ✅ Works offline without any external dependencies

## 🏗️ Architecture

```
ergogen YAML → ConnectionDiagramGenerator → Markdown Diagram
     ↓                      ↓                       ↓
  Parse zones,         Extract layout,         Generate ASCII,
  footprints,         electrical, and         tables, and
  PCB configs         component data          documentation
```

### Key Components

1. **YAML Parser**: Extracts structured data from ergogen configs
2. **Layout Analyzer**: Interprets zones, keys, and component placement
3. **Electrical Mapper**: Maps pin assignments and network connections
4. **Diagram Generator**: Creates ASCII layouts and markdown tables
5. **Template Engine**: Formats everything into readable documentation

## 🎯 Supported Features

- ✅ **Matrix keyboards** (any size)
- ✅ **Numpad layouts**
- ✅ **Split keyboards** 
- ✅ **Rotary encoders** (with switch functionality)
- ✅ **OLED displays** (I2C)
- ✅ **Special key sizes** (2U, 1.5U, etc.)
- ✅ **Pro Micro controllers**
- ✅ **Custom column/row networks**
- ✅ **Mixed zone layouts**

## 🔧 Customization

The generator can be extended to support:
- Additional MCU types
- Different controller pin mappings
- Custom component types
- Alternative ASCII layout styles
- Additional documentation sections

## 🚀 Installation & Usage

1. **Install the extension** (or update if you have an older version)
2. **Open your ergogen project** in VSCode
3. **Run ergogen** as usual - diagrams generate automatically!
4. **Find your diagram** in the output folder alongside PCB files

## 🎉 Benefits

- **Save Time**: No manual documentation needed
- **Stay Synchronized**: Diagrams update automatically with config changes  
- **Reduce Errors**: Programmatic parsing eliminates human mistakes
- **Improve Communication**: Clear visuals for sharing keyboard designs
- **Enhance Understanding**: See the complete picture of your keyboard's internals

---

This feature transforms the ergogen workflow by making keyboard documentation as automated as PCB generation. Your connection diagrams will always be accurate, complete, and up-to-date! 🎹✨
