$sourceDir = "C:\Users\aaron\.gemini\antigravity\scratch\antigravity-cli-addon"
$targetDir = "$sourceDir\lite"

if (-not (Test-Path "$targetDir")) {
    New-Item -ItemType Directory -Path "$targetDir" | Out-Null
}

Get-ChildItem -Path "$targetDir" | Remove-Item -Recurse -Force

$exclude = @(".git", ".history", "lite", "__pycache__", "sync-lite.ps1", "deploy-local.ps1", ".githooks", "*.log", "*.txt")
Get-ChildItem -Path "$sourceDir" -Exclude $exclude | Copy-Item -Destination "$targetDir" -Recurse -Force

$configFile = "$targetDir\config.yaml"
if (Test-Path "$configFile") {
    $config = Get-Content "$configFile" -Raw
    $config = $config -replace "(?m)^hassio_role:\s*manager\r?\n?", ""
    $config = $config -replace '(?m)^name:\s*".*"', 'name: "Antigravity CLI (No Supervisor)"'
    $config = $config -replace '(?m)^slug:\s*".*"', 'slug: "antigravity_cli_lite"'
    $config = $config -replace '(?m)^description:\s*".*"', 'description: "AI Agent for domotics via Home Assistant Core API"'
    Set-Content "$configFile" $config -NoNewline
    Write-Host "Successfully synced to /lite and modified config.yaml"
} else {
    Write-Host "Error: config.yaml not found in $targetDir"
}

$linuxFiles = Get-ChildItem -Path "$targetDir" -Include "*.sh", "*.conf", "Dockerfile", "*.yaml", "*.json", "*.py" -Recurse
foreach ($f in $linuxFiles) {
    $content = [IO.File]::ReadAllText($f.FullName)
    $content = $content.Replace("`r`n", "`n")
    [IO.File]::WriteAllText($f.FullName, $content, (New-Object System.Text.UTF8Encoding($false)))
}
