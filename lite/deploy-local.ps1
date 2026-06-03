$sourceDir = "C:\Users\aaron\.gemini\antigravity\scratch\antigravity-cli-addon"
$targetDir = "\\192.168.1.2\addons\antigravity-cli"

Write-Host "Desplegando en Local (Home Assistant)..."

# Copiar archivos excluyendo .git, lite, etc.
$exclude = @(".git", ".githooks", "lite", "__pycache__", "*.log", "*.txt")
Get-ChildItem -Path "$sourceDir" -Exclude $exclude | Copy-Item -Destination "$targetDir" -Recurse -Force

# Modificar el config.yaml del servidor local para que ponga "Local"
$configFile = "$targetDir\config.yaml"
if (Test-Path "$configFile") {
    $config = Get-Content "$configFile" -Raw
    $config = $config -replace '(?m)^name:\s*".*"', 'name: "Antigravity CLI (Local)"'
    Set-Content "$configFile" $config -NoNewline
    Write-Host "Despliegue local completado. Se renombro a (Local) en HA."
} else {
    Write-Host "Error: config.yaml no encontrado en $targetDir"
}
