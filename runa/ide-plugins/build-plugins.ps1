# Runa IDE Plugins Build Script for Windows
# Builds both VS Code and IntelliJ plugins for distribution

param(
    [switch]$SkipVSCode,
    [switch]$SkipIntelliJ
)

Write-Host "🚀 Building Runa IDE Plugins..." -ForegroundColor Blue

function Write-Status {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if we're in the right directory
if (!(Test-Path "vscode") -or !(Test-Path "intellij")) {
    Write-Error "Please run this script from the runa/ide-plugins directory"
    exit 1
}

# Create dist directory
New-Item -ItemType Directory -Force -Path "dist" | Out-Null

if (!$SkipVSCode) {
    # Build VS Code Plugin
    Write-Status "Building VS Code plugin..."
    Set-Location "vscode"

    # Check if Node.js is installed
    try {
        $nodeVersion = node --version
        Write-Status "Using Node.js $nodeVersion"
    }
    catch {
        Write-Error "Node.js is not installed. Please install Node.js 18+ and try again."
        exit 1
    }

    # Check if npm is installed
    try {
        $npmVersion = npm --version
        Write-Status "Using npm $npmVersion"
    }
    catch {
        Write-Error "npm is not installed. Please install npm and try again."
        exit 1
    }

    # Install dependencies
    Write-Status "Installing VS Code plugin dependencies..."
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install dependencies"
        exit 1
    }

    # Compile TypeScript
    Write-Status "Compiling TypeScript..."
    npm run compile
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to compile TypeScript"
        exit 1
    }

    # Package extension
    Write-Status "Packaging VS Code extension..."
    try {
        vsce --version | Out-Null
    }
    catch {
        Write-Warning "vsce not found, installing..."
        npm install -g vsce
    }

    vsce package --out "../dist/"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to package VS Code extension"
        exit 1
    }

    Write-Success "VS Code plugin built successfully!"
    Set-Location ".."
}

if (!$SkipIntelliJ) {
    # Build IntelliJ Plugin
    Set-Location "intellij"
    Write-Status "Building IntelliJ plugin..."

    # Check if Java is installed
    try {
        $javaVersion = java -version 2>&1 | Select-String "version"
        Write-Status "Using Java: $javaVersion"
    }
    catch {
        Write-Error "Java is not installed. Please install Java 11+ and try again."
        exit 1
    }

    # Build with Gradle
    Write-Status "Building with Gradle..."
    if (Test-Path "./gradlew.bat") {
        .\gradlew.bat clean buildPlugin
    }
    else {
        gradle clean buildPlugin
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to build IntelliJ plugin"
        exit 1
    }

    # Copy to dist directory
    Copy-Item "build/distributions/*.zip" "../dist/" -Force

    Write-Success "IntelliJ plugin built successfully!"
    Set-Location ".."
}

# Summary
Write-Success "✅ All plugins built successfully!"
Write-Host ""
Write-Status "Built plugins are available in the 'dist' directory:"
Get-ChildItem "dist" | Format-Table Name, Length, LastWriteTime
Write-Host ""
Write-Status "Installation instructions:"
Write-Host "📁 VS Code: Install .vsix file via Extensions → Install from VSIX" -ForegroundColor White
Write-Host "📁 IntelliJ: Install .zip file via Settings → Plugins → Install from Disk" -ForegroundColor White
Write-Host ""
Write-Status "For detailed installation instructions, see INSTALLATION.md"
