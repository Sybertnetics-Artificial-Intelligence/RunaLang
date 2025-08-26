#!/bin/bash
# Runa LSP Server Build Script
#
# This script builds the complete Runa Language Server including:
# 1. Runa compiler (for LSP logic)
# 2. Rust runtime (for JSON-RPC bridge)
# 3. LSP executable

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Building Runa Language Server${NC}"
echo "=================================="

# Check if we're in the right directory
if [[ ! -f "runa.toml" ]]; then
    echo -e "${RED}❌ Error: Must run from runa/ directory${NC}"
    exit 1
fi

# Step 1: Verify Runa LSP modules exist
echo -e "${YELLOW}📦 Step 1: Verifying Runa LSP modules${NC}"

echo -e "${BLUE}📝 Checking LSP module files${NC}"
if [[ ! -f "src/compiler/lsp/lsp_types.runa" ]]; then
    echo -e "${RED}❌ Missing lsp_types.runa${NC}"
    exit 1
fi

if [[ ! -f "src/compiler/lsp/lsp_server.runa" ]]; then
    echo -e "${RED}❌ Missing lsp_server.runa${NC}"
    exit 1
fi

if [[ ! -f "src/compiler/lsp/lsp_handlers.runa" ]]; then
    echo -e "${RED}❌ Missing lsp_handlers.runa${NC}"
    exit 1
fi

if [[ ! -f "src/compiler/lsp/main.runa" ]]; then
    echo -e "${RED}❌ Missing main.runa${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All LSP module files present${NC}"
echo "  • lsp_types.runa: $(wc -l < src/compiler/lsp/lsp_types.runa) lines"
echo "  • lsp_server.runa: $(wc -l < src/compiler/lsp/lsp_server.runa) lines"
echo "  • lsp_handlers.runa: $(wc -l < src/compiler/lsp/lsp_handlers.runa) lines"
echo "  • main.runa: $(wc -l < src/compiler/lsp/main.runa) lines"

# Step 2: Build the Rust runtime with LSP bridge
echo -e "${YELLOW}📦 Step 2: Building Rust runtime with LSP integration${NC}"

cd src/runtime

# Clean previous builds
echo "  • Cleaning previous builds..."
cargo clean

# Build the LSP server executable
echo "  • Building runa-lsp executable..."
cargo build --release --bin runa-lsp

# Check if build succeeded
if [[ -f "target/release/runa-lsp" ]]; then
    echo -e "${GREEN}✅ LSP executable built successfully${NC}"
    LSP_BINARY="target/release/runa-lsp"
else
    echo -e "${RED}❌ Failed to build LSP executable${NC}"
    exit 1
fi

# Step 3: Test the LSP server
echo -e "${YELLOW}🧪 Step 3: Testing LSP server${NC}"

echo "  • Testing help command..."
if $LSP_BINARY --help > /dev/null 2>&1; then
    echo -e "${GREEN}    ✅ Help command works${NC}"
else
    echo -e "${RED}    ❌ Help command failed${NC}"
    exit 1
fi

echo "  • Testing version information..."
if $LSP_BINARY --help | grep -q "Runa Language Server"; then
    echo -e "${GREEN}    ✅ Version information present${NC}"
else
    echo -e "${RED}    ❌ Version information missing${NC}"
    exit 1
fi

cd ../..

# Step 4: Create installation directory and scripts
echo -e "${YELLOW}📦 Step 4: Creating installation package${NC}"

# Create installation directory
INSTALL_DIR="dist/runa-lsp"
mkdir -p "$INSTALL_DIR"

# Copy LSP executable
echo "  • Copying LSP executable..."
cp "src/runtime/target/release/runa-lsp" "$INSTALL_DIR/"

# Create installation script
echo "  • Creating installation script..."
cat > "$INSTALL_DIR/install.sh" << 'EOF'
#!/bin/bash
# Runa LSP Server Installation Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🎯 Installing Runa Language Server${NC}"

# Determine installation directory
if [[ "$EUID" -eq 0 ]]; then
    # Root installation - system-wide
    INSTALL_TARGET="/usr/local/bin"
else
    # User installation - local bin
    INSTALL_TARGET="$HOME/.local/bin"
    mkdir -p "$INSTALL_TARGET"
fi

# Copy executable
cp runa-lsp "$INSTALL_TARGET/"
chmod +x "$INSTALL_TARGET/runa-lsp"

echo -e "${GREEN}✅ Runa Language Server installed to $INSTALL_TARGET${NC}"
echo "   The LSP server is now available as: runa-lsp"

# Test installation
if command -v runa-lsp > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Installation verified - runa-lsp is in PATH${NC}"
else
    echo "⚠️  runa-lsp not in PATH. Add $INSTALL_TARGET to your PATH:"
    echo "   export PATH=\"$INSTALL_TARGET:\$PATH\""
fi
EOF

chmod +x "$INSTALL_DIR/install.sh"

# Create uninstall script
echo "  • Creating uninstall script..."
cat > "$INSTALL_DIR/uninstall.sh" << 'EOF'
#!/bin/bash
# Runa LSP Server Uninstallation Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${RED}🗑️  Uninstalling Runa Language Server${NC}"

# Find and remove installations
REMOVED=0

for dir in "/usr/local/bin" "$HOME/.local/bin"; do
    if [[ -f "$dir/runa-lsp" ]]; then
        rm -f "$dir/runa-lsp"
        echo "  • Removed $dir/runa-lsp"
        REMOVED=1
    fi
done

if [[ $REMOVED -eq 1 ]]; then
    echo -e "${GREEN}✅ Runa Language Server uninstalled${NC}"
else
    echo "No Runa Language Server installations found"
fi
EOF

chmod +x "$INSTALL_DIR/uninstall.sh"

# Create README
echo "  • Creating README..."
cat > "$INSTALL_DIR/README.md" << 'EOF'
# Runa Language Server

This package contains the Runa Language Server Protocol (LSP) server, providing intelligent IDE support for Runa code.

## Installation

Run the installation script:

```bash
./install.sh
```

This will install `runa-lsp` to either `/usr/local/bin` (if run as root) or `~/.local/bin` (if run as user).

## Usage

The LSP server is designed to be used by IDEs and editors. It communicates via JSON-RPC over stdin/stdout.

### Command Line Options

- `--max-errors <number>`: Maximum number of errors to report (default: 100)
- `--max-warnings <number>`: Maximum number of warnings to report (default: 200)
- `--enable-incremental`: Enable incremental analysis (default: true)
- `--disable-incremental`: Disable incremental analysis
- `--cache-size <number>`: Analysis cache size (default: 1000)
- `--performance-tracking`: Enable performance tracking (default: true)
- `--no-performance-tracking`: Disable performance tracking
- `--debug`: Enable debug mode
- `--help`: Show help message

### VSCode Integration

The Runa VSCode extension will automatically detect and use this LSP server when available.

## Features

- ✅ Syntax highlighting
- ✅ Error detection and reporting
- ✅ Autocompletion
- ✅ Hover information
- ✅ Go to definition
- ✅ Find all references
- ✅ Document symbols
- ✅ Semantic tokens
- ✅ Incremental analysis
- ✅ Performance optimization

## Uninstallation

Run the uninstallation script:

```bash
./uninstall.sh
```

## Troubleshooting

If you encounter issues:

1. Check that `runa-lsp` is in your PATH
2. Run `runa-lsp --help` to verify installation
3. Enable debug mode with `--debug` for detailed logging
4. Check IDE/editor LSP configuration

For more information, visit: https://github.com/sybertneticsaisolutions/runa
EOF

# Create package info
echo "  • Creating package info..."
cat > "$INSTALL_DIR/VERSION" << EOF
Runa Language Server v0.1.0
Built on: $(date)
Commit: $(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
Rust version: $(rustc --version)
EOF

# Step 5: Final verification
echo -e "${YELLOW}🔍 Step 5: Final verification${NC}"

# Test the packaged executable
echo "  • Testing packaged executable..."
if "$INSTALL_DIR/runa-lsp" --help > /dev/null 2>&1; then
    echo -e "${GREEN}    ✅ Packaged executable works${NC}"
else
    echo -e "${RED}    ❌ Packaged executable failed${NC}"
    exit 1
fi

# Check file sizes
LSP_SIZE=$(du -h "$INSTALL_DIR/runa-lsp" | cut -f1)
echo "  • LSP executable size: $LSP_SIZE"

# Success!
echo ""
echo -e "${GREEN}🎉 Build completed successfully!${NC}"
echo ""
echo "📦 Installation package created in: $INSTALL_DIR"
echo "🚀 LSP server executable: $INSTALL_DIR/runa-lsp"
echo ""
echo "Next steps:"
echo "1. Run: cd $INSTALL_DIR && ./install.sh"
echo "2. Configure your IDE to use 'runa-lsp' as the Runa language server"
echo "3. Open a .runa file and enjoy intelligent code assistance!"
echo ""
echo -e "${BLUE}🎯 Ready to integrate with VSCode extension!${NC}"