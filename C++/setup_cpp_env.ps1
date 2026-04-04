#Requires -RunAsAdministrator
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$BaseDir     = 'C:\Users\hiwel\Programming Projects\C++'
$UCRT64Bin   = 'C:\msys64\ucrt64\bin'
$TemplateDir = Join-Path $BaseDir '_C++_Template'
$NewProjectPs1 = Join-Path $BaseDir 'new-project.ps1'

function Write-Utf8NoBOM {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )
    $enc = New-Object System.Text.UTF8Encoding($false)
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    [System.IO.File]::WriteAllText($Path, $Content, $enc)
    Write-Host ("    wrote: {0}" -f $Path) -ForegroundColor DarkGray
}

function Step {
    param(
        [Parameter(Mandatory = $true)][string]$Num,
        [Parameter(Mandatory = $true)][string]$Message
    )
    Write-Host ""
    Write-Host ("[{0}] {1}" -f $Num, $Message) -ForegroundColor Cyan
}

function Good {
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Host ("  OK  {0}" -f $Message) -ForegroundColor Green
}

function Warn {
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Host ("  !!  {0}" -f $Message) -ForegroundColor Yellow
}

function Fail {
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Host ("  XX  {0}" -f $Message) -ForegroundColor Red
}

function Test-Tool {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$ExeName,
        [Parameter(Mandatory = $true)][string]$Pkg,
        [Parameter(Mandatory = $true)][bool]$Required
    )

    $full = Join-Path $UCRT64Bin $ExeName
    if (Test-Path $full) {
        $ver = & $full --version 2>&1 | Select-Object -First 1
        Good ("{0}: {1}" -f $Name, $ver)
        return $true
    }

    if ($Required) {
        Fail ("{0} not found at: {1}" -f $Name, $full)
        Warn ("Fix in MSYS2 UCRT64 terminal: pacman -S {0}" -f $Pkg)
        return $false
    }

    Warn ("{0} not found (optional): pacman -S {1}" -f $Name, $Pkg)
    return $true
}

function Ensure-Dir {
    param([Parameter(Mandatory = $true)][string]$Path)
    New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

# ----------------------------------------------------------------------
# 1) Pre-flight checks
# ----------------------------------------------------------------------
Step '1/5' 'Pre-flight checks'

$fatal = $false
if (-not (Test-Tool 'g++'    'g++.exe'    'mingw-w64-ucrt-x86_64-gcc'               $true)) { $fatal = $true }
if (-not (Test-Tool 'clangd'  'clangd.exe' 'mingw-w64-ucrt-x86_64-clang-tools-extra' $true)) { $fatal = $true }
if (-not (Test-Tool 'gdb'    'gdb.exe'    'mingw-w64-ucrt-x86_64-gdb'               $true)) { $fatal = $true }
if (-not (Test-Tool 'ninja'  'ninja.exe'  'mingw-w64-ucrt-x86_64-ninja'             $true)) { $fatal = $true }
if (-not (Test-Tool 'cmake'  'cmake.exe'  'mingw-w64-ucrt-x86_64-cmake'             $true)) { $fatal = $true }

if ($fatal) {
    Fail 'One or more required tools are missing. Fix them and rerun this script.'
    exit 1
}

$hasCodeCli = [bool](Get-Command code -ErrorAction SilentlyContinue)
if ($hasCodeCli) {
    Good "VS Code CLI 'code' is available"
} else {
    Warn 'VS Code CLI not in PATH. Extension install/uninstall will need to be manual.'
}

# ----------------------------------------------------------------------
# 2) Create or refresh template directory
# ----------------------------------------------------------------------
Step '2/5' 'Creating template directory structure'

if (Test-Path $TemplateDir) {
    $backup = "{0}_backup_{1}" -f $TemplateDir, (Get-Date -Format 'yyyyMMdd_HHmmss')
    Move-Item -Force $TemplateDir $backup
    Warn ("Existing template moved to: {0}" -f $backup)
}

Ensure-Dir $TemplateDir
Ensure-Dir (Join-Path $TemplateDir '.vscode')
Ensure-Dir (Join-Path $TemplateDir 'src')
Ensure-Dir (Join-Path $TemplateDir 'include')

Good $TemplateDir

# ----------------------------------------------------------------------
# 3) Write project files
# ----------------------------------------------------------------------
Step '3/5' 'Writing project files'

$jsonClangd = (Join-Path $UCRT64Bin 'clangd.exe').Replace('\', '/')
$jsonGpp    = (Join-Path $UCRT64Bin 'g++.exe').Replace('\', '/')
$jsonGdb    = (Join-Path $UCRT64Bin 'gdb.exe').Replace('\', '/')
$jsonCmake  = (Join-Path $UCRT64Bin 'cmake.exe').Replace('\', '/')

$cmakeContent = @'
cmake_minimum_required(VERSION 3.20)
project(CppProject VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS "src/*.cpp")

if(NOT SOURCES)
    message(FATAL_ERROR "No .cpp files found under src/. Create src/main.cpp before configuring.")
endif()

add_executable(${PROJECT_NAME} ${SOURCES})

target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_options(${PROJECT_NAME} PRIVATE
    -Wall
    -Wextra
    -Wpedantic
    -Wshadow
    -Werror=return-type
    $<$<CONFIG:Debug>:-g3>
    $<$<CONFIG:Release>:-O2>
)
'@
Write-Utf8NoBOM (Join-Path $TemplateDir 'CMakeLists.txt') $cmakeContent

$presetsContent = @'
{
    "version": 6,
    "cmakeMinimumRequired": { "major": 3, "minor": 20, "patch": 0 },
    "configurePresets": [
        {
            "name": "debug",
            "displayName": "Debug (UCRT64 GCC + Ninja)",
            "description": "Full debug symbols, no optimization.",
            "generator": "Ninja",
            "binaryDir": "${sourceDir}/build",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Debug",
                "CMAKE_CXX_COMPILER": "__GPP__",
                "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
            }
        },
        {
            "name": "release",
            "displayName": "Release (UCRT64 GCC + Ninja)",
            "description": "Optimized build.",
            "generator": "Ninja",
            "binaryDir": "${sourceDir}/build/release",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Release",
                "CMAKE_CXX_COMPILER": "__GPP__",
                "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
            }
        }
    ],
    "buildPresets": [
        { "name": "debug", "configurePreset": "debug", "displayName": "Build Debug" },
        { "name": "release", "configurePreset": "release", "displayName": "Build Release" }
    ]
}
'@
$presetsContent = $presetsContent.Replace('__GPP__', $jsonGpp)
Write-Utf8NoBOM (Join-Path $TemplateDir 'CMakePresets.json') $presetsContent

$settingsContent = @'
{
    "C_Cpp.intelliSenseEngine": "disabled",
    "C_Cpp.autocomplete": "disabled",
    "C_Cpp.errorSquiggles": "disabled",

    "clangd.path": "__CLANGD__",
    "clangd.arguments": [
        "--query-driver=__GPP__",
        "--compile-commands-dir=${workspaceFolder}/build",
        "--background-index",
        "--header-insertion=never",
        "--completion-style=detailed",
        "--function-arg-placeholders=false"
    ],
    "clangd.onConfigChanged": "restart",

    "cmake.buildDirectory": "${workspaceFolder}/build",
    "cmake.configureOnOpen": true,
    "cmake.saveBeforeBuild": true,
    "cmake.buildBeforeRun": true,

    "editor.formatOnSave": true,
    "[cpp]": { "editor.defaultFormatter": "llvm-vs-code-extensions.vscode-clangd" },
    "[c]": { "editor.defaultFormatter": "llvm-vs-code-extensions.vscode-clangd" },

    "editor.rulers": [100],
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "files.exclude": {
        "**/build": true,
        "**/.cache": true
    }
}
'@
$settingsContent = $settingsContent.Replace('__CLANGD__', $jsonClangd).Replace('__GPP__', $jsonGpp)
Write-Utf8NoBOM (Join-Path $TemplateDir '.vscode\settings.json') $settingsContent

$launchContent = @'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug (GDB)",
            "type": "cppdbg",
            "request": "launch",
            "program": "${command:cmake.launchTargetPath}",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "miDebuggerPath": "__GDB__",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                },
                {
                    "description": "Use Intel disassembly syntax",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
'@
$launchContent = $launchContent.Replace('__GDB__', $jsonGdb)
Write-Utf8NoBOM (Join-Path $TemplateDir '.vscode\launch.json') $launchContent

$extensionsContent = @'
{
    "recommendations": [
        "ms-vscode.cpptools",
        "ms-vscode.cmake-tools",
        "llvm-vs-code-extensions.vscode-clangd",
        "twxs.cmake",
        "jeff-hykin.better-cpp-syntax"
    ],
    "unwantedRecommendations": [
        "ms-vscode.cpptools-extension-pack",
        "xaver.clang-format"
    ]
}
'@
Write-Utf8NoBOM (Join-Path $TemplateDir '.vscode\extensions.json') $extensionsContent

$clangFormatContent = @'
BasedOnStyle: Google
IndentWidth: 4
TabWidth: 4
UseTab: Never
ColumnLimit: 100
BreakBeforeBraces: Attach
PointerAlignment: Left
SortIncludes: CaseSensitive
IncludeBlocks: Regroup
AllowShortFunctionsOnASingleLine: Inline
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
SpaceAfterCStyleCast: false
SpaceBeforeParens: ControlStatements
'@
Write-Utf8NoBOM (Join-Path $TemplateDir '.clang-format') $clangFormatContent

$mainContent = @'
#include <iostream>
#include <string>

int main() {
    const std::string message = "Build system is operational.";
    std::cout << message << '\n';
    return 0;
}
'@
Write-Utf8NoBOM (Join-Path $TemplateDir 'src\main.cpp') $mainContent

$gitignoreContent = @'
/build/
/.cache/
*.exe
*.obj
*.o
*.a
*.lib
*.dll
*.pdb
CMakeCache.txt
CMakeFiles/
cmake_install.cmake
install_manifest.txt
CTestTestfile.cmake
_deps/
.vscode/c_cpp_properties.json
Thumbs.db
desktop.ini
.DS_Store
'@
Write-Utf8NoBOM (Join-Path $TemplateDir '.gitignore') $gitignoreContent

$helperContent = @'
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
'@
Write-Utf8NoBOM $NewProjectPs1 $helperContent

Good 'All project files written.'

# ----------------------------------------------------------------------
# 4) Manage VS Code extensions
# ----------------------------------------------------------------------
Step '4/5' 'Managing VS Code extensions'

if ($hasCodeCli) {
    $toInstall = @(
        'ms-vscode.cpptools',
        'ms-vscode.cmake-tools',
        'llvm-vs-code-extensions.vscode-clangd',
        'twxs.cmake',
        'jeff-hykin.better-cpp-syntax'
    )

    foreach ($ext in $toInstall) {
        & code --install-extension $ext --force 2>&1 | Out-Null
        Good ("Installed: {0}" -f $ext)
    }

    & code --uninstall-extension ms-vscode.cpptools-extension-pack 2>&1 | Out-Null
    Good 'Removed: ms-vscode.cpptools-extension-pack'

    & code --uninstall-extension xaver.clang-format 2>&1 | Out-Null
    Good 'Removed: xaver.clang-format'

    Warn 'Manual step in VS Code: disable ms-vscode.cpptools-extension-pack if it still shows as enabled.'
} else {
    Warn 'Install these extensions manually in VS Code:'
    Write-Host '    INSTALL: ms-vscode.cpptools' -ForegroundColor Yellow
    Write-Host '    INSTALL: ms-vscode.cmake-tools' -ForegroundColor Yellow
    Write-Host '    INSTALL: llvm-vs-code-extensions.vscode-clangd' -ForegroundColor Yellow
    Write-Host '    INSTALL: twxs.cmake' -ForegroundColor Yellow
    Write-Host '    INSTALL: jeff-hykin.better-cpp-syntax' -ForegroundColor Yellow
    Write-Host '    REMOVE:  ms-vscode.cpptools-extension-pack' -ForegroundColor Yellow
    Write-Host '    REMOVE:  xaver.clang-format' -ForegroundColor Yellow
}

# ----------------------------------------------------------------------
# 5) Validate
# ----------------------------------------------------------------------
Step '5/5' 'Validating template with cmake --preset debug'

Push-Location $TemplateDir
try {
    $configOut = & $jsonCmake --preset debug 2>&1
    if ($LASTEXITCODE -eq 0) {
        Good 'cmake --preset debug: PASSED'

        if (Test-Path (Join-Path $TemplateDir 'build\compile_commands.json')) {
            Good 'compile_commands.json exists in build/'
        } else {
            Warn 'compile_commands.json not found in build/'
        }

        $buildOut = & $jsonCmake --build --preset debug 2>&1
        if ($LASTEXITCODE -eq 0) {
            Good 'cmake --build --preset debug: PASSED'
        } else {
            Warn 'Build failed after configure.'
            $buildOut | ForEach-Object { Write-Host ("    {0}" -f $_) -ForegroundColor Yellow }
        }
    } else {
        Warn 'cmake --preset debug failed.'
        $configOut | ForEach-Object { Write-Host ("    {0}" -f $_) -ForegroundColor Yellow }
    }
}
finally {
    Pop-Location
}

Write-Host ''
Write-Host '================================================' -ForegroundColor Green
Write-Host 'SETUP COMPLETE' -ForegroundColor Green
Write-Host '================================================' -ForegroundColor Green
Write-Host ''
Write-Host 'Template folder:' -ForegroundColor White
Write-Host ("  {0}" -f $TemplateDir) -ForegroundColor Gray
Write-Host ''
Write-Host 'New project command:' -ForegroundColor White
Write-Host ("  powershell -ExecutionPolicy Bypass -File `"{0}`" MyProjectName" -f $NewProjectPs1) -ForegroundColor Gray
Write-Host ''
Write-Host 'VS Code flow:' -ForegroundColor White
Write-Host '  1. Open the project folder' -ForegroundColor Gray
Write-Host '  2. CMake: Select Configure Preset -> debug' -ForegroundColor Gray
Write-Host '  3. Build' -ForegroundColor Gray
Write-Host '  4. F5 to debug' -ForegroundColor Gray
Write-Host ''
Write-Host 'When you add a new .cpp file:' -ForegroundColor White
Write-Host '  Put it in src/ and run CMake: Configure again before Build.' -ForegroundColor Gray
Write-Host ''
Write-Host 'If clangd shows red squiggles:' -ForegroundColor White
Write-Host '  Run CMake: Configure, then clangd: Restart Language Server.' -ForegroundColor Gray
Write-Host ''
Write-Host 'Done.' -ForegroundColor Green