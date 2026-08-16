$sourceDir = "C:\Users\aaron\.gemini\antigravity\scratch\antigravity-cli-addon"
$targetDir = "\\192.168.1.2\addons\antigravity-cli"

Write-Host "Desplegando en Local (Home Assistant)..."

$exclude = @(".git", ".githooks", "lite", "__pycache__", "deploy-local.ps1", "sync-lite.ps1", "*.log", "*.txt")
Get-ChildItem -Path "$sourceDir" -Exclude $exclude | Copy-Item -Destination "$targetDir" -Recurse -Force

$configFile = "$targetDir\config.yaml"
if (Test-Path "$configFile") {
    $config = Get-Content "$configFile" -Raw
    $config = $config -replace '(?m)^name:\s*".*"', 'name: "Antigravity CLI (Local)"'
    $config = $config -replace '(?m)^slug:\s*".*"', 'slug: "antigravity_cli_local"'
    $config = $config -replace '(?m)^panel_title:\s*".*"', 'panel_title: "Antigravity Local"'
    Set-Content "$configFile" $config -NoNewline
    Write-Host "Despliegue local completado. Se renombro a (Local) en HA con slug antigravity_cli_local."
} else {
    Write-Host "Error: config.yaml no encontrado en $targetDir"
}

# Ensure all Linux script and config files have pure Unix LF line endings (no Windows CRLF / no BOM)
$linuxFiles = Get-ChildItem -Path "$targetDir" -Include "*.sh", "*.conf", "Dockerfile", "*.yaml", "*.json", "*.py" -Recurse
foreach ($f in $linuxFiles) {
    $content = [IO.File]::ReadAllText($f.FullName)
    $content = $content.Replace("`r`n", "`n")
    [IO.File]::WriteAllText($f.FullName, $content, (New-Object System.Text.UTF8Encoding($false)))
}
Write-Host "LF line endings enforced on all config and script files in target."
