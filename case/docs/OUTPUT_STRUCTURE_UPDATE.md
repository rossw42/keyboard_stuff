# Output Structure Update

## Summary

Updated all generation scripts to use the new project-based output folder structure.

## New Structure

```
output/
├── README.md                          # Overview of all projects
│
├── 60_percent_standard/               # Standard height project
│   ├── README.md
│   ├── 3d_models/                     # STEP and STL files
│   └── cnc/
│       ├── toolpaths/                 # JSON and DXF toolpaths
│       │   ├── top_frame/
│       │   ├── bottom_tray/
│       │   ├── top_frame_toolpaths.json
│       │   └── bottom_tray_toolpaths.json
│       ├── drawings/                  # PDF and DXF drawings
│       └── setup/                     # Setup instructions
│
└── 60_percent_low_profile/            # Low-profile project
    ├── README.md
    ├── 3d_models/                     # STEP, STL, and patterned STLs
    └── cnc/
        ├── toolpaths/
        ├── drawings/
        └── setup/
```

## Updated Files

### Example Scripts (examples/)
- ✅ `generate_all_3d_models.py` → `60_percent_standard/3d_models/`
- ✅ `generate_top_frame_3d.py` → `60_percent_standard/3d_models/`
- ✅ `generate_bottom_tray_3d.py` → `60_percent_standard/3d_models/`
- ✅ `generate_assembly_3d.py` → `60_percent_standard/3d_models/`
- ✅ `generate_top_frame_3d_lp.py` → `60_percent_low_profile/3d_models/`
- ✅ `generate_bottom_tray_3d_lp.py` → `60_percent_low_profile/3d_models/`
- ✅ `generate_assembly_3d_lp.py` → `60_percent_low_profile/3d_models/`
- ✅ `generate_top_frame_toolpaths.py` → `60_percent_standard/cnc/toolpaths/`
- ✅ `generate_bottom_tray_toolpaths.py` → `60_percent_standard/cnc/toolpaths/`
- ✅ `generate_top_frame_toolpaths_lp.py` → `60_percent_low_profile/cnc/toolpaths/`
- ✅ `generate_bottom_tray_toolpaths_lp.py` → `60_percent_low_profile/cnc/toolpaths/`
- ✅ `export_top_frame_drawing.py` → `60_percent_standard/cnc/drawings/`
- ✅ `export_bottom_tray_drawing.py` → `60_percent_standard/cnc/drawings/`
- ✅ `export_assembly_drawing.py` → `60_percent_standard/cnc/drawings/`

### Source Modules (src/export/)
- ✅ `setup_sheets.py` → Default path: `60_percent_standard/cnc/setup/`
- ✅ `tool_list.py` → Default path: `60_percent_standard/cnc/setup/`
- ✅ `toolpath_dxf.py` → Default paths:
  - Top frame: `60_percent_standard/cnc/toolpaths/top_frame/`
  - Bottom tray: `60_percent_standard/cnc/toolpaths/bottom_tray/`

## Benefits

1. **Self-contained projects:** Each keyboard variant is independent
2. **Scalable:** Easy to add new projects (75%, Alice layout, etc.)
3. **Clear hierarchy:** 3D models and CNC files are organized by project
4. **Consistent structure:** Every project follows the same pattern
5. **Better documentation:** Each project has its own README

## Adding New Projects

To add a new keyboard project:

1. Create folder: `output/keyboard_size_variant/`
2. Add subdirectories: `3d_models/` and `cnc/`
3. Create project README with specifications
4. Update generation scripts to target new project folder

Example: `output/75_percent_standard/`, `output/alice_layout_low_profile/`

## Migration Notes

All existing files have been moved to the new structure:
- Standard variant files → `60_percent_standard/`
- Low-profile variant files → `60_percent_low_profile/`
- Old scattered directories removed

Scripts will now automatically create the correct directory structure when run.
