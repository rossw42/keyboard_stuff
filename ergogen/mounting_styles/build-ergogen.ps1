param(
    [Parameter(Mandatory=$true)]
    [string]$YamlFile
)

$outputDir = [System.IO.Path]::GetFileNameWithoutExtension($YamlFile)
New-Item -ItemType Directory -Path $outputDir -Force
New-Item -ItemType Directory -Path "$outputDir\stl" -Force
ergogen $YamlFile -o $outputDir

if (Test-Path "$outputDir\cases") {
    Get-ChildItem "$outputDir\cases\*.jscad" | ForEach-Object { 
        npx @jscad/cli@1 $_.FullName -of stla -o "$outputDir\stl\$($_.BaseName).stl" 
    }
    Write-Host "STL files generated in $outputDir\stl\"
} else {
    Write-Host "No cases folder found - this ergogen config may not generate 3D cases"
}