#!/bin/bash

# Runa IDE Plugins Build Script
# Builds both VS Code and IntelliJ plugins for distribution

set -e

echo "🚀 Building Runa IDE Plugins..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "vscode" ] || [ ! -d "intellij" ]; then
    print_error "Please run this script from the runa/ide-plugins directory"
    exit 1
fi

# Create dist directory
mkdir -p dist

# Build VS Code Plugin
print_status "Building VS Code plugin..."
cd vscode

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm and try again."
    exit 1
fi

# Install dependencies
print_status "Installing VS Code plugin dependencies..."
npm install

# Compile TypeScript
print_status "Compiling TypeScript..."
npm run compile

# Package extension
print_status "Packaging VS Code extension..."
if ! command -v vsce &> /dev/null; then
    print_warning "vsce not found, installing..."
    npm install -g vsce
fi

vsce package --out ../dist/

print_success "VS Code plugin built successfully!"

# Build IntelliJ Plugin
cd ../intellij
print_status "Building IntelliJ plugin..."

# Check if Java is installed
if ! command -v java &> /dev/null; then
    print_error "Java is not installed. Please install Java 11+ and try again."
    exit 1
fi

# Build with Gradle
print_status "Building with Gradle..."
if [ -f "./gradlew" ]; then
    ./gradlew clean buildPlugin
else
    gradle clean buildPlugin
fi

# Copy to dist directory
cp build/distributions/*.zip ../dist/

print_success "IntelliJ plugin built successfully!"

# Summary
cd ..
print_success "✅ All plugins built successfully!"
echo ""
print_status "Built plugins are available in the 'dist' directory:"
ls -la dist/
echo ""
print_status "Installation instructions:"
echo "📁 VS Code: Install .vsix file via Extensions → Install from VSIX"
echo "📁 IntelliJ: Install .zip file via Settings → Plugins → Install from Disk"
echo ""
print_status "For detailed installation instructions, see INSTALLATION.md"
