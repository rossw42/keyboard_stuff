# Ergogen Toolkit

A collection of Ergogen-related tools and utilities for keyboard design, because apparently designing keyboards wasn't complicated enough already.

> **Philosophy**: Keep it simple, stupid. Most of these tools do one thing and try to do it well. Some succeed better than others. 🎯

## 🛠 What's Actually Here

### [`ergogen-toolkit/`](ergogen-toolkit/) ✅ **The Star of the Show**
A simple VS Code extension with **two functions**:
1. **Run Ergogen** - Execute ergogen command on YAML files
2. **View DXF Files** - Open DXF files with your system's default viewer

That's it. No complexity, no heavy dependencies, just the essentials that actually work. Born from the noble quest to avoid carpal tunnel from constantly copy-pasting YAML files to those very cool online Ergogen viewers. So I asked Claude to help dream up a local solution that's decidedly less cool but requires more button clicks - because apparently that's progress!

### [`working_samples/`](working_samples/) 📁 **The Examples Folder**
Example Ergogen YAML files that definitely worked at some point in time. Includes configs for various keyboards that may or may not generate valid PCBs. Your mileage may vary.

### [`mounting_styles/`](mounting_styles/) 📚 **The Reference Library**
Examples and documentation for different keyboard mounting approaches. Contains YAML files for tray mount, gasket mount, and other mounting styles with varying degrees of completeness. This is a research project to see if Ergogen can generate these different kinds of cases - spoiler alert: the jury's still out, but we're having fun trying! The methodology: throw documentation, YAML files, pretty pictures at an AI, then see what sticks. Results may require creative interpretation and liberal application of nano tape.

### [`kle_to_ergogen/`](kle_to_ergogen/) 🔄 **The Converter**
Converts Keyboard Layout Editor (KLE) layouts to Ergogen point definitions. Sometimes works brilliantly, sometimes produces coordinates that exist in a parallel dimension. The dream workflow: design in KLE → generate PCB with Ergogen → 3D print cases → wake up to a new keyboard ready for handwiring. Reality: usually involves more debugging than sleeping, but when it works, it's magical! 

### [`ergogen_to_qmk_converter/`](ergogen_to_qmk_converter/) 🚧 **The Ambitious Project**
Attempts to bridge the gap between Ergogen PCB design and QMK firmware. Currently in the "I have a plan" phase of development.

### [`keyboards/`](keyboards/) 🎹 **The Keyboard Collection**
Specific keyboard projects and configurations. Contains actual keyboard designs in various states of completion. Bonus feature: automatically generating keyboard connection diagrams would be pretty cool - maybe someday when the stars align and the code cooperates. Check out the [macropad connection diagram](keyboards/macropad/keyboard_connection_diagram.md) for an example of what this could look like.

## 🚀 Quick Start ( These instructions might work )

### For the VS Code Extension
1. **Install the extension** from `ergogen-toolkit/`
2. **Open a YAML file** (keyboard config)
3. **Run Ergogen**: `Ctrl+Shift+E` or Command Palette → "Run Ergogen"
4. **View DXF files**: `Ctrl+Shift+D` or Command Palette → "Open DXF Viewer"

### For Everything Else
1. **Browse the folders** - each has its own README with varying degrees of accuracy
2. **Start with `working_samples/`** - these configs probably work
3. **Check `mounting_styles/`** - learn about different mounting approaches
4. **Try `kle_to_ergogen/`** - if you have a KLE layout to convert

## 🔧 Requirements

- **Ergogen CLI** installed and available in PATH
- **DXF Viewer** application for viewing files (optional but recommended)
- **Patience** - some of these tools are more experimental than others

### Installing Ergogen

```bash
npm install -g ergogen
```


## 📄 License

MIT License - Simple and permissive.

## 🙏 Acknowledgments

- [Ergogen](https://github.com/ergogen/ergogen) - The amazing keyboard design tool that makes this all possible
- VS Code team for the excellent extension API
- The keyboard community for endless inspiration and complexity

---

**Philosophy**: Each tool in this collection tries to do one thing well. Some succeed better than others, but they're all honest about their limitations.