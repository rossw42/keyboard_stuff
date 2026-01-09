@echo off
setlocal enabledelayedexpansion
echo 🎹 Starting QMK Keymap Live Viewer...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.x
    echo You can download it from: https://python.org
    pause
    exit /b 1
)

REM Install watchdog if not present
echo 📦 Checking dependencies...
pip install watchdog >nul 2>&1

REM Initialize TARGET_FILE as empty
set TARGET_FILE=

REM Check if a specific file was provided as argument
if "%~1"=="" (
    echo 🔍 Searching for keymap.c files...
    echo.
    
    REM Create temporary file to store found keymaps
    set TEMP_FILE=%TEMP%\keymaps_found.txt
    if exist "!TEMP_FILE!" del "!TEMP_FILE!"
    
    REM Search for keymap.c files recursively
    set count=0
    for /r %%f in (keymap.c) do (
        set /a count+=1
        echo %%f >> "!TEMP_FILE!"
        echo   !count!. %%f
    )
    
    if !count! equ 0 (
        echo ❌ No keymap.c files found in current directory
        pause
        exit /b 1
    )
    
    echo.
    set /p choice="Enter number (1-!count!) or press Enter to watch all: "
    
    REM Read the selected file from temp file
    if not "!choice!"=="" (
        set line_num=0
        for /f "delims=" %%a in (!TEMP_FILE!) do (
            set /a line_num+=1
            if !line_num! equ !choice! set "TARGET_FILE=%%a"
        )
    )
    
    REM Clean up temp file
    if exist "!TEMP_FILE!" del "!TEMP_FILE!"
) else (
    set "TARGET_FILE=%~1"
)

REM Start the server
echo 🚀 Starting server...
echo.
if not "!TARGET_FILE!"=="" (
    echo 🎯 Watching specific file: !TARGET_FILE!
    python keymap_server.py --file "!TARGET_FILE!"
) else (
    echo 👀 Watching all keymap.c files
    python keymap_server.py
)

echo.
echo 💡 Tips:
echo   • The page will auto-refresh when the keymap file changes
echo   • Use Ctrl+R to manually refresh
echo   • Use Ctrl+Space to pause/resume auto-updates
echo   • Press Ctrl+C here to stop the server
echo.

pause