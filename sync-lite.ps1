$sourceDir = "C:\Users\aaron\.gemini\antigravity\scratch\antigravity-cli-addon"
$targetDir = "$sourceDir\lite"

# Create target dir if it doesn't exist
if (-not (Test-Path "$targetDir")) {
    New-Item -ItemType Directory -Path "$targetDir" | Out-Null
}

# Clean target dir
Get-ChildItem -Path "$targetDir" | Remove-Item -Recurse -Force

# Copy all files from root to lite, excluding specific folders/files
$exclude = @(".git", ".history", "lite", "__pycache__", "sync-lite.ps1", ".githooks", "*.log", "*.txt")
Get-ChildItem -Path "$sourceDir" -Exclude $exclude | Copy-Item -Destination "$targetDir" -Recurse -Force

# Modify config.yaml
$configFile = "$targetDir\config.yaml"
if (Test-Path "$configFile") {
    $config = Get-Content "$configFile" -Raw
    
    # Remove hassio_role: manager
    $config = $config -replace "(?m)^hassio_role:\s*manager\r?\n?", ""
    
    # Change name
    $config = $config -replace '(?m)^name:\s*".*"', 'name: "Antigravity CLI (Lite)"'
    
    # Change slug
    $config = $config -replace '(?m)^slug:\s*".*"', 'slug: "antigravity_cli_lite"'
    
    # Change description slightly
    $config = $config -replace '(?m)^description:\s*".*"', 'description: "AI Agent for domotics via Home Assistant Core API"'
    
    Set-Content "$configFile" $config -NoNewline
    Write-Host "Successfully synced to /lite and modified config.yaml"
} else {
    Write-Host "Error: config.yaml not found in $targetDir"
}

