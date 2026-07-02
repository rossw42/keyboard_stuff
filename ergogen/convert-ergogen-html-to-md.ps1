# Batch convert Ergogen HTML docs to Markdown
# Usage: .\convert-ergogen-html-to-md.ps1

# Add html2text to PATH
$env:PATH = "C:\Users\garli\AppData\Roaming\Python\Python314\Scripts;" + $env:PATH

# Source and destination directories
$sourceDir = "d:\Keyboard Workspace\Ergogen Docs\docs.ergogen.xyz"
$outputDir = "d:\Keyboard Workspace\ergogen-docs-md"

# Create output directory
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
    Write-Host "✓ Created output directory: $outputDir"
}

# Find all HTML files
$htmlFiles = Get-ChildItem -Path $sourceDir -Recurse -Filter "*.html" | Where-Object { $_.FullName -notmatch "hts-cache" }

Write-Host "Found $($htmlFiles.Count) HTML files to convert"
Write-Host ""

# Convert each file
$converted = 0
$failed = 0

foreach ($file in $htmlFiles) {
    try {
        # Get relative path
        $relativePath = $file.FullName.Substring($sourceDir.Length).TrimStart('\')
        
        # Create output path (replace .html with .md)
        $outputFile = Join-Path $outputDir $relativePath
        $outputFile = $outputFile -replace '\.html$', '.md'
        
        # Create output directory if it doesn't exist
        $outputFileDir = Split-Path -Parent $outputFile
        if (-not (Test-Path $outputFileDir)) {
            New-Item -ItemType Directory -Path $outputFileDir | Out-Null
        }
        
        # Convert HTML to Markdown using python
        python -m html2text -o markdown "$($file.FullName)" | Out-File -FilePath $outputFile -Encoding UTF8 -Force
        
        Write-Host "✓ $relativePath"
        $converted++
    }
    catch {
        Write-Host "✗ $relativePath - Error: $_"
        $failed++
    }
}

Write-Host ""
Write-Host "======================================"
Write-Host "Conversion Complete"
Write-Host "======================================"
Write-Host "Converted: $converted files"
Write-Host "Failed: $failed files"
Write-Host "Output: $outputDir"
