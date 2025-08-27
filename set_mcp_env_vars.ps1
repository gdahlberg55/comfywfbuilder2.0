# PowerShell script to set MCP environment variables permanently
# Run this script as Administrator for system-wide variables

Write-Host "MCP Environment Variable Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Prompt for API keys
$braveKey = Read-Host -Prompt "Enter your Brave API Key (or press Enter to skip)"
$githubToken = Read-Host -Prompt "Enter your GitHub Token (or press Enter to skip)"

# Set Brave API Key if provided
if ($braveKey -ne "") {
    [System.Environment]::SetEnvironmentVariable("BRAVE_API_KEY", $braveKey, [System.EnvironmentVariableTarget]::User)
    Write-Host "✓ BRAVE_API_KEY set successfully" -ForegroundColor Green
} else {
    Write-Host "⚠ Skipped BRAVE_API_KEY" -ForegroundColor Yellow
}

# Set GitHub Token if provided
if ($githubToken -ne "") {
    [System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $githubToken, [System.EnvironmentVariableTarget]::User)
    Write-Host "✓ GITHUB_TOKEN set successfully" -ForegroundColor Green
} else {
    Write-Host "⚠ Skipped GITHUB_TOKEN" -ForegroundColor Yellow
}

Write-Host "`nEnvironment variables have been set at the USER level." -ForegroundColor Cyan
Write-Host "You may need to restart Claude Code for changes to take effect." -ForegroundColor Cyan

# Verify the variables were set
Write-Host "`nVerifying environment variables:" -ForegroundColor Yellow
$brave = [System.Environment]::GetEnvironmentVariable("BRAVE_API_KEY", [System.EnvironmentVariableTarget]::User)
$github = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", [System.EnvironmentVariableTarget]::User)

if ($brave) {
    Write-Host "BRAVE_API_KEY: [SET - ${brave.Length} characters]" -ForegroundColor Green
} else {
    Write-Host "BRAVE_API_KEY: [NOT SET]" -ForegroundColor Red
}

if ($github) {
    Write-Host "GITHUB_TOKEN: [SET - ${github.Length} characters]" -ForegroundColor Green
} else {
    Write-Host "GITHUB_TOKEN: [NOT SET]" -ForegroundColor Red
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")