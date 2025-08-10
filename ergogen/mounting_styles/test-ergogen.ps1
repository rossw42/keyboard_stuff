param(
    [Parameter(Mandatory=$true)]
    [string]$YamlFile
)

$outputDir = [System.IO.Path]::GetFileNameWithoutExtension($YamlFile)
New-Item -ItemType Directory -Path $outputDir -Force

Write-Host "Testing Ergogen compilation for: $YamlFile"
Write-Host "Output directory: $outputDir"
Write-Host "----------------------------------------"

ergogen $YamlFile -o $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Ergogen compilation successful!"
    
    if (Test-Path "$outputDir\cases") {
        $caseFiles = Get-ChildItem "$outputDir\cases\*.jscad"
        Write-Host "Generated case files:"
        $caseFiles | ForEach-Object { Write-Host "  - $($_.Name)" }
    }
    
    if (Test-Path "$outputDir\pcbs") {
        $pcbFiles = Get-ChildItem "$outputDir\pcbs\*.kicad_pcb"
        Write-Host "Generated PCB files:"
        $pcbFiles | ForEach-Object { Write-Host "  - $($_.Name)" }
    }
    
    if (Test-Path "$outputDir\outlines") {
        $outlineFiles = Get-ChildItem "$outputDir\outlines\*.dxf"
        Write-Host "Generated outline files:"
        $outlineFiles | ForEach-Object { Write-Host "  - $($_.Name)" }
    }
} else {
    Write-Host "✗ Ergogen compilation failed with exit code: $LASTEXITCODE"
}