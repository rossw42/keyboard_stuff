@echo off
REM QMK Format Converter Setup Script for Windows

echo 🔧 Setting up QMK Format Converter...

REM Get the directory of this script
set SCRIPT_DIR=%~dp0

echo.
echo 🎉 Setup complete! The converter is ready to use.
echo.
echo Try these commands to get started:
echo.
echo # List supported formats
echo %SCRIPT_DIR%qmk-convert.bat --list-formats
echo.
echo # Convert KLE to VIA
echo %SCRIPT_DIR%qmk-convert.bat input.json --to via -o output.json
echo.
echo # Convert with explicit input format
echo %SCRIPT_DIR%qmk-convert.bat keymap.c --from keymap --to kle -o layout.json
echo.
echo # Validate a file
echo %SCRIPT_DIR%qmk-convert.bat layout.json --validate
echo.
echo ℹ️  You can also run the converter directly with:
echo    %SCRIPT_DIR%qmk-convert.bat [options]
echo.
pause
