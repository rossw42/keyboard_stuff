@echo off
if "%~1"=="" (
    echo Usage: %0 ^<yaml-filename^>
    echo Example: %0 my-keyboard.yaml
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%~dp0run-ergogen-and-convert.ps1" "%~1"