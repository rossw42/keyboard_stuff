@echo off
echo 🎹 Simple Keymap Viewer
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found
    pause
    exit /b 1
)

REM Install watchdog
echo 📦 Installing dependencies...
pip install watchdog >nul 2>&1

echo 🚀 Starting Simple Keymap Viewer...
echo.

python simple_keymap_viewer.py

pause