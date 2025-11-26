#!/usr/bin/env pwsh
# QMK Keymap Live Viewer - PowerShell version

Write-Host "🎹 Starting QMK Keymap Live Viewer..." -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.x" -ForegroundColor Red
    Write-Host "You can download it from: https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install watchdog if not present
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan
pip install watchdog | Out-Null

# Find available keymap files
$keymapFiles = @(
    "macropad/keymaps/default/keymap.c",
    "4x2/keymaps/2rows-with-encoder/keymap.c", 
    "lily58/keymaps/default/keymap.c",
    "lily58/keymaps/lily58l/keymap.c",
    "4x2/keymaps/2rows-no-encoder/keymap.c",
    "lily58-hold/hold/keymaps/default/keymap.c"
)

$availableFiles = @()
foreach ($file in $keymapFiles) {
    if (Test-Path $file) {
        $availableFiles += $file
    }
}

# Handle command line argument or show menu
$targetFile = $null
if ($args.Count -gt 0) {
    $targetFile = $args[0]
    Write-Host "🎯 Using specified file: $targetFile" -ForegroundColor Yellow
} elseif ($availableFiles.Count -gt 0) {
    Write-Host "📁 Available keymaps:" -ForegroundColor Cyan
    Write-Host ""
    
    for ($i = 0; $i -lt $availableFiles.Count; $i++) {
        Write-Host "  $($i + 1). $($availableFiles[$i])" -ForegroundColor White
    }
    Write-Host ""
    
    $choice = Read-Host "Enter number (1-$($availableFiles.Count)) or press Enter to watch all"
    
    if ($choice -match '^\d+$' -and [int]$choice -ge 1 -and [int]$choice -le $availableFiles.Count) {
        $targetFile = $availableFiles[[int]$choice - 1]
    }
}

# Start the server
Write-Host ""
Write-Host "🚀 Starting server..." -ForegroundColor Green
Write-Host ""

if ($targetFile) {
    Write-Host "🎯 Watching specific file: $targetFile" -ForegroundColor Yellow
    python keymap_server.py --file $targetFile
} else {
    Write-Host "👀 Watching all keymap.c files" -ForegroundColor Yellow  
    python keymap_server.py
}

Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Cyan
Write-Host "  • The page will auto-refresh when the keymap file changes"
Write-Host "  • Use Ctrl+R to manually refresh"
Write-Host "  • Use Ctrl+Space to pause/resume auto-updates"
Write-Host "  • Press Ctrl+C here to stop the server"
Write-Host ""

Read-Host "Press Enter to exit"