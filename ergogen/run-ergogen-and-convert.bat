@echo off
setlocal enabledelayedexpansion

REM Check if filename argument is provided
if "%~1"=="" (
    echo Usage: %0 ^<yaml-filename^>
    echo Example: %0 my-keyboard.yaml
    exit /b 1
)

set "YAML_FILE=%~1"
set "BASE_NAME=%~n1"

REM Check if YAML file exists
if not exist "%YAML_FILE%" (
    echo Error: File "%YAML_FILE%" not found
    exit /b 1
)

echo ========================================
echo Running Ergogen Pipeline
echo ========================================
echo YAML File: %YAML_FILE%
echo Output Directory: %BASE_NAME%
echo ========================================

REM Create output directory
if not exist "%BASE_NAME%" mkdir "%BASE_NAME%"

REM Run ergogen
echo.
echo [1/2] Running Ergogen...
ergogen "%YAML_FILE%" -o "%BASE_NAME%"

set "ERGOGEN_EXIT=%ERRORLEVEL%"
if %ERGOGEN_EXIT% neq 0 (
    echo Error: Ergogen failed with exit code %ERGOGEN_EXIT%
    exit /b %ERGOGEN_EXIT%
)

echo + Ergogen completed successfully

REM Check if cases directory exists and convert JSCAD files
set "CASES_DIR=%BASE_NAME%\cases"
echo Checking for cases directory: %CASES_DIR%
if exist "%CASES_DIR%" (
    echo + Cases directory found
    echo.
    echo [2/2] Converting JSCAD files to STL...
    
    REM Check if npx is available (we'll use @jscad/cli@1 specifically)
    echo Checking for npx command...
    where npx >nul 2>&1
    set "NPX_CHECK=%ERRORLEVEL%"
    if %NPX_CHECK% neq 0 (
        echo Warning: npx not found in PATH
        echo Please make sure Node.js and npm are installed
        echo Skipping STL conversion...
        goto :show_results
    )
    echo + npx command found
    
    REM Convert each JSCAD file to STL
    set "CONVERTED_COUNT=0"
    echo Looking for JSCAD files in: %CASES_DIR%
    for %%f in ("%CASES_DIR%\*.jscad") do (
        set "JSCAD_FILE=%%f"
        set "STL_FILE=%%~dpnf.stl"
        
        echo Converting: %%~nxf
        echo   Input: !JSCAD_FILE!
        echo   Output: !STL_FILE!
        echo y | npx @jscad/cli@1 "!JSCAD_FILE!" -of stla
        
        REM Check if STL file was created instead of relying on exit code
        set "STL_FILE=%%~dpnf.stl"
        if exist "!STL_FILE!" (
            set /a CONVERTED_COUNT+=1
            echo   + Created: %%~nf.stl
        ) else (
            echo   - Failed to convert: %%~nxf
        )
    )
    
    if !CONVERTED_COUNT! gtr 0 (
        echo + Converted !CONVERTED_COUNT! JSCAD file(s) to STL
    ) else (
        echo No JSCAD files were successfully converted
    )
) else (
    echo - No cases directory found at: %CASES_DIR%
    echo Skipping STL conversion...
)

:show_results
echo.
echo ========================================
echo Pipeline Complete!
echo ========================================
echo Output directory: %BASE_NAME%

REM Show generated files
if exist "%BASE_NAME%" (
    echo.
    echo Generated files:
    
    if exist "%BASE_NAME%\cases" (
        echo   Cases:
        for %%f in ("%BASE_NAME%\cases\*.*") do echo     - %%~nxf
    )
    
    if exist "%BASE_NAME%\pcbs" (
        echo   PCBs:
        for %%f in ("%BASE_NAME%\pcbs\*.*") do echo     - %%~nxf
    )
    
    if exist "%BASE_NAME%\outlines" (
        echo   Outlines:
        for %%f in ("%BASE_NAME%\outlines\*.*") do echo     - %%~nxf
    )
)

echo.
echo Done!