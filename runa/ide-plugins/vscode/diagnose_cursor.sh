#!/bin/bash

# Cursor Compatibility Diagnostics for Runa Extension
echo "=== Runa Extension Cursor Compatibility Diagnostics ==="
echo ""

# Check if Cursor is installed
echo "1. Checking Cursor installation..."
if command -v cursor &> /dev/null; then
    echo "✓ Cursor found at: $(which cursor)"
    cursor --version
else
    echo "✗ Cursor not found in PATH"
    # Check Windows AppData location
    CURSOR_PATH="/mnt/c/Users/$(whoami)/AppData/Local/Programs/cursor/cursor.exe"
    if [ -f "$CURSOR_PATH" ]; then
        echo "✓ Found Cursor at: $CURSOR_PATH"
    else
        echo "✗ Cursor not found in standard Windows location"
    fi
fi
echo ""

# Check VSCode compatibility
echo "2. Checking VSCode compatibility..."
if command -v code &> /dev/null; then
    echo "✓ VSCode found at: $(which code)"
    code --version
else
    echo "✗ VSCode not found in PATH"
fi
echo ""

# Check extension package
echo "3. Checking extension package..."
VSIX_FILE="runa-language-support-v2-2.0.3.vsix"
if [ -f "$VSIX_FILE" ]; then
    echo "✓ Extension package found: $VSIX_FILE"
    echo "   Size: $(du -h $VSIX_FILE | cut -f1)"
    echo "   Created: $(stat -c %y $VSIX_FILE)"
else
    echo "✗ Extension package not found"
fi
echo ""

# Check Node.js and npm
echo "4. Checking Node.js environment..."
if command -v node &> /dev/null; then
    echo "✓ Node.js: $(node --version)"
else
    echo "✗ Node.js not found"
fi

if command -v npm &> /dev/null; then
    echo "✓ npm: $(npm --version)"
else
    echo "✗ npm not found"
fi
echo ""

# Check TypeScript compilation
echo "5. Checking TypeScript compilation..."
if [ -d "out" ]; then
    echo "✓ Output directory exists"
    echo "   Files compiled: $(find out -name "*.js" | wc -l)"
else
    echo "✗ No output directory found - extension not compiled"
fi
echo ""

# Check package.json configuration
echo "6. Checking package.json configuration..."
if [ -f "package.json" ]; then
    echo "✓ package.json exists"
    echo "   Extension name: $(cat package.json | grep '"name"' | cut -d'"' -f4)"
    echo "   Version: $(cat package.json | grep '"version"' | cut -d'"' -f4)"
    echo "   VSCode engine: $(cat package.json | grep '"vscode"' | cut -d'"' -f4)"
else
    echo "✗ package.json not found"
fi
echo ""

# Installation instructions
echo "=== INSTALLATION INSTRUCTIONS ==="
echo ""
echo "For Cursor:"
echo "1. Open Cursor"
echo "2. Press Ctrl+Shift+P (Cmd+Shift+P on macOS)"
echo "3. Type 'Extensions: Install from VSIX'"
echo "4. Select the file: $(pwd)/$VSIX_FILE"
echo ""
echo "For VSCode:"
echo "1. Open VSCode" 
echo "2. Press Ctrl+Shift+P (Cmd+Shift+P on macOS)"
echo "3. Type 'Extensions: Install from VSIX'"
echo "4. Select the file: $(pwd)/$VSIX_FILE"
echo ""

# Debugging the specific error
echo "=== CURSOR ERROR ANALYSIS ==="
echo ""
echo "The error you're seeing appears to be related to Cursor's composer feature"
echo "trying to analyze the repository, not the Runa extension itself."
echo ""
echo "Error details:"
echo "- 'submitPromptDryRun: Canceled' suggests Cursor's AI features are having issues"
echo "- 'getRepoInfo' indicates problems reading repository metadata"
echo "- 'ms-vscode.npm-command' selector missing suggests npm extension issues"
echo ""
echo "Potential fixes:"
echo "1. Restart Cursor completely"
echo "2. Clear Cursor's extension cache"
echo "3. Disable Cursor's composer feature temporarily"
echo "4. Install Runa extension manually using VSIX file above"
echo "5. Try opening just a single .runa file instead of the whole repository"
echo ""

# Test Runa file creation
echo "Creating test Runa file..."
cat > test_cursor_compatibility.runa << 'EOF'
Note: Test file for Cursor compatibility
Note: This file should have syntax highlighting if the extension works

Process called "test_function" that takes input as String returns String:
    Let message be "Hello from Runa!"
    Display message
    Return message

Note: Test various Runa syntax
Let number be 42
If number is greater than 0:
    Display "Positive number"
Otherwise:
    Display "Not positive"

Note: Test imports (these might not exist yet)
Import "collections" as Collections
Import "os" as OS
EOF

echo "✓ Created test_cursor_compatibility.runa"
echo ""
echo "Try opening this file in Cursor to test extension functionality."
echo ""