param(
    [Parameter(Mandatory=$true)]
    [string]$YamlFile
)

# Get the directory where the YAML file is located and the base name
$yamlDir = Split-Path -Parent $YamlFile
$yamlBaseName = [System.IO.Path]::GetFileNameWithoutExtension($YamlFile)

# Create output directory in the same folder as the YAML file
if ($yamlDir) {
    $outputDir = Join-Path $yamlDir $yamlBaseName
} else {
    $outputDir = $yamlBaseName
}

# Check if YAML file exists
if (-not (Test-Path $YamlFile)) {
    Write-Host "Error: File '$YamlFile' not found" -ForegroundColor Red
    exit 1
}

Write-Host "========================================"
Write-Host "Running Ergogen Pipeline"
Write-Host "========================================"
Write-Host "YAML File: $YamlFile"
Write-Host "Output Directory: $outputDir"
Write-Host "========================================"

# Create output directory
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

# Run ergogen
Write-Host ""
Write-Host "[1/2] Running Ergogen..." -ForegroundColor Cyan
ergogen $YamlFile -o $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "+ Ergogen completed successfully" -ForegroundColor Green
    
    # Check if cases directory exists and convert JSCAD files
    $casesDir = Join-Path $outputDir "cases"
    Write-Host "Checking for cases directory: $casesDir"
    
    if (Test-Path $casesDir) {
        Write-Host "+ Cases directory found" -ForegroundColor Green
        Write-Host ""
        Write-Host "[2/2] Converting JSCAD files to STL..." -ForegroundColor Cyan
        
        # Check if npx is available
        Write-Host "Checking for npx command..."
        try {
            $null = Get-Command npx -ErrorAction Stop
            Write-Host "+ npx command found" -ForegroundColor Green
        }
        catch {
            Write-Host "Warning: npx not found in PATH" -ForegroundColor Yellow
            Write-Host "Please make sure Node.js and npm are installed"
            Write-Host "Skipping STL conversion..."
            return
        }
        
        # Convert each JSCAD file to STL
        $convertedCount = 0
        $jscadFiles = Get-ChildItem "$casesDir\*.jscad"
        
        Write-Host "Looking for JSCAD files in: $casesDir"
        foreach ($jscadFile in $jscadFiles) {
            Write-Host "Converting: $($jscadFile.Name)"
            Write-Host "  Input: $($jscadFile.FullName)"
            
            # Use npx with @jscad/cli@1 and auto-confirm with echo y
            $process = Start-Process -FilePath "cmd" -ArgumentList "/c", "echo y | npx @jscad/cli@1 `"$($jscadFile.FullName)`" -of stla" -Wait -PassThru -NoNewWindow
            
            # Check if STL file was created
            $stlFile = $jscadFile.FullName -replace '\.jscad$', '.stl'
            if (Test-Path $stlFile) {
                $convertedCount++
                Write-Host "  + Created: $($jscadFile.BaseName).stl" -ForegroundColor Green
            } else {
                Write-Host "  - Failed to convert: $($jscadFile.Name)" -ForegroundColor Red
            }
        }
        
        if ($convertedCount -gt 0) {
            Write-Host "+ Converted $convertedCount JSCAD file(s) to STL" -ForegroundColor Green
        } else {
            Write-Host "No JSCAD files were successfully converted" -ForegroundColor Yellow
        }
    } else {
        Write-Host "- No cases directory found at: $casesDir" -ForegroundColor Yellow
        Write-Host "Skipping STL conversion..."
    }
} else {
    Write-Host "Error: Ergogen failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "========================================"
Write-Host "Pipeline Complete!"
Write-Host "========================================"
Write-Host "Output directory: $outputDir"

# Show generated files
if (Test-Path $outputDir) {
    Write-Host ""
    Write-Host "Generated files:"
    
    if (Test-Path "$outputDir\cases") {
        Write-Host "  Cases:"
        Get-ChildItem "$outputDir\cases\*.*" | ForEach-Object { Write-Host "    - $($_.Name)" }
    }
    
    if (Test-Path "$outputDir\pcbs") {
        Write-Host "  PCBs:"
        Get-ChildItem "$outputDir\pcbs\*.*" | ForEach-Object { Write-Host "    - $($_.Name)" }
    }
    
    if (Test-Path "$outputDir\outlines") {
        Write-Host "  Outlines:"
        Get-ChildItem "$outputDir\outlines\*.*" | ForEach-Object { Write-Host "    - $($_.Name)" }
    }
}

Write-Host ""
Write-Host "Done!"