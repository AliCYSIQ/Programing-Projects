param(
    [Parameter(Mandatory = $true)][string]$Name
)

$Root = 'C:\Users\hiwel\Programming Projects\C++'
$Template = Join-Path $Root '_C++_Template'
$Target = Join-Path $Root $Name

if (Test-Path $Target) {
    throw "Project already exists: $Target"
}

New-Item -ItemType Directory -Force -Path $Target | Out-Null
Copy-Item -Path (Join-Path $Template '*') -Destination $Target -Recurse -Force

Write-Host "Project created: $Target" -ForegroundColor Green

if (Get-Command code -ErrorAction SilentlyContinue) {
    code $Target
}