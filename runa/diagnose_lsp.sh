#!/bin/bash
# Diagnostic script for LSP server connection

echo "🔍 Runa LSP Connection Diagnostics"
echo "=================================="

echo "1. Checking LSP server executable..."
if [[ -f "lsp-server/target/release/runa-lsp" ]]; then
    echo "   ✅ LSP server found at: $(pwd)/lsp-server/target/release/runa-lsp"
    echo "   📏 Size: $(du -h lsp-server/target/release/runa-lsp | cut -f1)"
    echo "   🔐 Permissions: $(ls -la lsp-server/target/release/runa-lsp | awk '{print $1}')"
else
    echo "   ❌ LSP server not found!"
    exit 1
fi

echo
echo "2. Testing LSP server startup..."
echo "   🚀 Starting LSP server..."
timeout 3s lsp-server/target/release/runa-lsp --version
if [[ $? -eq 0 ]]; then
    echo "   ✅ LSP server starts correctly"
else
    echo "   ❌ LSP server failed to start"
fi

echo
echo "3. Checking extension configuration..."
if grep -q '"default": true' ide-plugins/vscode/package.json; then
    echo "   ✅ Language server enabled by default"
else
    echo "   ❌ Language server not enabled by default"
fi

echo
echo "4. Testing from VSCode extension directory..."
cd ide-plugins/vscode
EXTENSION_DIR=$(pwd)
echo "   📁 Extension directory: $EXTENSION_DIR"

# Test the path that the extension would use
LSP_PATH="../../lsp-server/target/release/runa-lsp"
if [[ -f "$LSP_PATH" ]]; then
    echo "   ✅ LSP server accessible from extension directory"
    echo "   📍 Relative path: $LSP_PATH"
else
    echo "   ❌ LSP server NOT accessible from extension directory"
    echo "   📍 Tried path: $LSP_PATH"
fi

echo
echo "5. Manual LSP test..."
cd ../../
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"processId":null,"rootUri":null,"capabilities":{}}}' | timeout 2s lsp-server/target/release/runa-lsp > /tmp/lsp_test_output.json 2>&1

if grep -q '"result"' /tmp/lsp_test_output.json 2>/dev/null; then
    echo "   ✅ LSP server responds to JSON-RPC requests"
else
    echo "   ❌ LSP server not responding properly"
    echo "   📄 Output: $(cat /tmp/lsp_test_output.json 2>/dev/null | head -1)"
fi

echo
echo "🏁 Diagnostic complete!"
echo
echo "💡 Troubleshooting tips:"
echo "   - Make sure you're opening .runa files from the runa/ directory"  
echo "   - Check VSCode Output panel (View → Output → Runa)"
echo "   - Try restarting VSCode completely"
echo "   - Use Ctrl+Shift+P → 'Runa: Restart Language Server'"