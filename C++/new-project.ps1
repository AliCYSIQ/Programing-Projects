param(
    [Parameter(Mandatory = $true)][string]$Name
)

$Root = (Get-Location).Path
$Template = Join-Path $Root '_C++_Template'
$Target = Join-Path $Root $Name

if (-not (Test-Path $Template)) {
    throw "Template folder not found: $Template. Run this from your C++ root directory."
}

if (Test-Path $Target) {
    throw "Project already exists: $Target"
}

New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path (Join-Path $Template '*') -Destination $Target -Recurse -Force -ErrorAction Stop

Write-Host "Project created: $Target" -ForegroundColor Green

if (Get-Command code -ErrorAction SilentlyContinue) {
    code $Target
}