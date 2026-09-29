$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $PythonPath)) {
    throw "Create the virtual environment first: py -3 -m venv .venv"
}

& $PythonPath -m pip install -r (Join-Path $ProjectRoot "requirements-dev.txt")
& $PythonPath -m pytest
& $PythonPath -m PyInstaller --noconfirm --clean (Join-Path $ProjectRoot "sob-words-finder.spec")

Write-Host "Build ready in dist\SOB-Words-Finder.exe"
