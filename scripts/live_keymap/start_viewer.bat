@echo off
REM ============================================================
REM  Live Keymap Viewer launcher
REM  Scans the repo's keyboards\ folder by default.
REM  Usage:
REM    start_viewer.bat                 (scan ..\..\keyboards)
REM    start_viewer.bat C:\path\to\dir  (scan a custom directory)
REM ============================================================

setlocal
set SCRIPT_DIR=%~dp0

if "%~1"=="" (
    set "SCAN_DIR=%SCRIPT_DIR%..\..\keyboards"
) else (
    set "SCAN_DIR=%~1"
)

echo Starting Live Keymap Viewer...
echo Scanning: %SCAN_DIR%
python "%SCRIPT_DIR%keymap_viewer.py" --dir "%SCAN_DIR%"
pause