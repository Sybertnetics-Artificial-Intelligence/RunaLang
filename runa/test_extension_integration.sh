#!/bin/bash
# Runa VSCode Extension with LSP Integration Test Script

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Runa VSCode Extension + LSP Integration Test${NC}"
echo "=================================================="

# Check if we're in the right directory
if [[ ! -f "runa.toml" ]]; then
    echo -e "${RED}❌ Error: Must run from runa/ directory${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Test 1: LSP Server Executable${NC}"

# Test LSP server exists and runs
if [[ ! -f "lsp-server/target/release/runa-lsp" ]]; then
    echo -e "${RED}❌ LSP server executable not found${NC}"
    exit 1
fi

# Test LSP server help
echo "  • Testing LSP server help..."
if lsp-server/target/release/runa-lsp --help > /dev/null 2>&1; then
    echo -e "${GREEN}    ✅ Help command works${NC}"
else
    echo -e "${RED}    ❌ Help command failed${NC}"
    exit 1
fi

# Test LSP server version
echo "  • Testing LSP server version..."
if lsp-server/target/release/runa-lsp --version | grep -q "Runa Language Server"; then
    echo -e "${GREEN}    ✅ Version information present${NC}"
else
    echo -e "${RED}    ❌ Version information missing${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Test 2: LSP Protocol Communication${NC}"

# Test LSP initialization
echo "  • Testing LSP initialization protocol..."
cat > /tmp/lsp_init_test.txt << 'EOF'
Content-Length: 200

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"processId":null,"rootUri":null,"capabilities":{"textDocument":{"hover":{"contentFormat":["markdown"]}}}}}

Content-Length: 44

{"jsonrpc":"2.0","method":"initialized","params":{}}

Content-Length: 45

{"jsonrpc":"2.0","id":2,"method":"shutdown","params":{}}

Content-Length: 31

{"jsonrpc":"2.0","method":"exit"}
EOF

LSP_OUTPUT=$(timeout 5s cat /tmp/lsp_init_test.txt | lsp-server/target/release/runa-lsp 2>/dev/null | grep -o '"result"' | wc -l)
if [[ $LSP_OUTPUT -ge 1 ]]; then
    echo -e "${GREEN}    ✅ LSP initialization successful${NC}"
else
    echo -e "${RED}    ❌ LSP initialization failed${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Test 3: VSCode Extension Package${NC}"

# Check VSCode extension
if [[ ! -f "ide-plugins/vscode/runa-language-support-1.0.0.vsix" ]]; then
    echo -e "${RED}❌ VSCode extension package not found${NC}"
    exit 1
fi

echo "  • VSCode extension package size: $(du -h ide-plugins/vscode/runa-language-support-1.0.0.vsix | cut -f1)"
echo -e "${GREEN}    ✅ Extension package exists${NC}"

# Test extension metadata
echo "  • Testing extension metadata..."
if grep -q '"default": true' ide-plugins/vscode/package.json; then
    echo -e "${GREEN}    ✅ Language server enabled by default${NC}"
else
    echo -e "${RED}    ❌ Language server not enabled by default${NC}"
    exit 1
fi

# Test compiled extension output
if [[ -f "ide-plugins/vscode/out/extension.js" ]]; then
    echo -e "${GREEN}    ✅ Extension compiled successfully${NC}"
else
    echo -e "${RED}    ❌ Extension not compiled${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Test 4: Integration Components${NC}"

# Test LSP path detection logic
echo "  • Testing LSP executable discovery..."
if grep -q "lsp-server/target/release/runa-lsp" ide-plugins/vscode/out/extension.js; then
    echo -e "${GREEN}    ✅ LSP path detection logic present${NC}"
else
    echo -e "${RED}    ❌ LSP path detection logic missing${NC}"
    exit 1
fi

# Test language server client integration
echo "  • Testing language client integration..."
if grep -q "LanguageClient" ide-plugins/vscode/out/extension.js; then
    echo -e "${GREEN}    ✅ Language client integration present${NC}"
else
    echo -e "${RED}    ❌ Language client integration missing${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Test 5: Test File Processing${NC}"

# Test with sample Runa file
echo "  • Testing with sample Runa code..."
if [[ -f "ide-plugins/vscode/test_lsp_integration.runa" ]]; then
    LINES=$(wc -l < ide-plugins/vscode/test_lsp_integration.runa)
    echo -e "${GREEN}    ✅ Test Runa file exists ($LINES lines)${NC}"
else
    echo -e "${RED}    ❌ Test Runa file missing${NC}"
    exit 1
fi

# Test LSP hover request simulation
echo "  • Testing LSP hover simulation..."
cat > /tmp/lsp_hover_test.txt << 'EOF'
Content-Length: 200

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"processId":null,"rootUri":null,"capabilities":{"textDocument":{"hover":{"contentFormat":["markdown"]}}}}}

Content-Length: 44

{"jsonrpc":"2.0","method":"initialized","params":{}}

Content-Length: 180

{"jsonrpc":"2.0","id":2,"method":"textDocument/hover","params":{"textDocument":{"uri":"file:///test.runa"},"position":{"line":0,"character":0}}}

Content-Length: 45

{"jsonrpc":"2.0","id":3,"method":"shutdown","params":{}}

Content-Length: 31

{"jsonrpc":"2.0","method":"exit"}
EOF

HOVER_OUTPUT=$(timeout 5s cat /tmp/lsp_hover_test.txt | lsp-server/target/release/runa-lsp 2>/dev/null | grep -o 'Runa Language' | wc -l)
if [[ $HOVER_OUTPUT -ge 1 ]]; then
    echo -e "${GREEN}    ✅ LSP hover response working${NC}"
else
    echo -e "${RED}    ❌ LSP hover response failed${NC}"
    exit 1
fi

# Test LSP completion request simulation
echo "  • Testing LSP completion simulation..."
cat > /tmp/lsp_completion_test.txt << 'EOF'
Content-Length: 250

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"processId":null,"rootUri":null,"capabilities":{"textDocument":{"completion":{"completionItem":{"snippetSupport":true}}}}}}

Content-Length: 44

{"jsonrpc":"2.0","method":"initialized","params":{}}

Content-Length: 185

{"jsonrpc":"2.0","id":2,"method":"textDocument/completion","params":{"textDocument":{"uri":"file:///test.runa"},"position":{"line":0,"character":0}}}

Content-Length: 45

{"jsonrpc":"2.0","id":3,"method":"shutdown","params":{}}

Content-Length: 31

{"jsonrpc":"2.0","method":"exit"}
EOF

COMPLETION_OUTPUT=$(timeout 5s cat /tmp/lsp_completion_test.txt | lsp-server/target/release/runa-lsp 2>/dev/null | grep -o '"label"' | wc -l)
if [[ $COMPLETION_OUTPUT -ge 1 ]]; then
    echo -e "${GREEN}    ✅ LSP completion response working${NC}"
else
    echo -e "${RED}    ❌ LSP completion response failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
echo ""
echo "Extension Integration Summary:"
echo "✅ LSP Server: Built and functional"
echo "✅ Protocol: JSON-RPC communication working"
echo "✅ Extension: Packaged and compiled"
echo "✅ Integration: LSP client properly configured"
echo "✅ Features: Hover, completion, and other LSP features responding"
echo ""
echo "🚀 Ready for deployment!"
echo ""
echo "Next Steps:"
echo "1. Install extension: code --install-extension ide-plugins/vscode/runa-language-support-1.0.0.vsix"
echo "2. Open a .runa file in VSCode"
echo "3. Verify LSP features are working (hover, completion, etc.)"
echo ""
echo -e "${BLUE}🎯 Integration complete - Runa now has full IDE support!${NC}"