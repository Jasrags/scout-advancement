#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Build Scout Advancement Labels .exe for Windows using PyInstaller.
#>
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir

Write-Host "=== Scout Advancement Labels - Build (Windows) ==="
Write-Host "Root: $Root"

# Activate venv if present (CI already has deps on PATH)
$VenvActivate = Join-Path $Root ".venv\Scripts\Activate.ps1"
if (Test-Path $VenvActivate) {
    & $VenvActivate
} elseif (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Error "Error: .venv not found and pyinstaller not on PATH.`nRun: python -m venv .venv && pip install -e '.[dev]'"
    exit 1
}

# Ensure dependencies
pip install --quiet "pyinstaller>=6.0,<7.0" "reportlab>=4.0,<5.0" "PySide6>=6.6,<7.0"

# Clean previous builds
$BuildDir = Join-Path $Root "build"
$DistDir = Join-Path $Root "dist"
if (Test-Path $BuildDir) { Remove-Item -Recurse -Force $BuildDir }
if (Test-Path $DistDir) { Remove-Item -Recurse -Force $DistDir }

# Build
Write-Host "`nBuilding with PyInstaller..."
$SpecFile = Join-Path $Root "packaging\scout_labels.spec"
pyinstaller $SpecFile --distpath $DistDir --workpath $BuildDir --clean --noconfirm

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n=== Build complete ==="
Write-Host "App: $DistDir\Scout Advancement Labels\"
Write-Host "Exe: $DistDir\Scout Advancement Labels\Scout Advancement Labels.exe"
