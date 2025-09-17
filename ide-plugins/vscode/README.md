# Runa Language Support for VS Code

[![Version](https://img.shields.io/badge/version-2.0.3-blue.svg)](https://marketplace.visualstudio.com/items?itemName=sybertnetics.runa-language-support-v2)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Comprehensive language support for Runa - the AI-first natural programming language designed for AI-to-AI communication.

## Features

### 🎨 **Advanced Syntax Highlighting**
- **Case-insensitive support**: `Process called`, `process called`, `PROCESS CALLED` all work
- Complete support for Runa's natural language syntax
- Proper highlighting for "Note:" comments (both inline and block)
- Mathematical symbol highlighting with custom Runa themes
- Distinct colors for primitive types, collection types, and keywords
- Enhanced support for compound structures like "Process called", "that takes"

### 🚀 **Intelligent Code Completion & Hover**
- **Context-aware hover**: Detailed information for compound constructs
- **Case-insensitive matching**: Works with any case combination
- Natural language operator suggestions
- Built-in function completion with signatures
- Comprehensive hover for "Process called", "Let ... be", "that takes", etc.
- Smart completion for mathematical operators and string concatenation

### ⚡ **Language Server Integration**
- **Integrated Rust LSP server**: Requires Runa compiler to be built
- Real-time hover information and completions
- Context-aware language intelligence
- Support for both WSL and native environments

### 📝 **Rich Code Snippets**
Type these prefixes and press Tab for instant code generation:

| Prefix | Expands to |
|--------|------------|
| `let` | `Let variable be value` |
| `process` | `Process called "name" that takes...` |
| `if` | `If condition:` |
| `for` | `For each item in collection:` |
| `try` | `Try:` / `Catch:` / `Finally:` block |
| `note` | `Note: comment` |
| `noteblock` | Multi-line comment block |

### 🎨 **Custom Themes**
- **Runa Dark Theme**: Optimized dark theme with mathematical symbol highlighting
- **Runa Light Theme**: Clean light theme with proper type differentiation  
- **Mathematical symbols**: Highlighted in red/orange for clear distinction
- **Type differentiation**: Different colors for primitive vs collection types

### 🔧 **Build & Run Integration**
- Compile Runa files with `Ctrl+Shift+B`
- Run Runa programs with `Ctrl+F5`
- Integrated terminal output
- Configurable compiler path

## Installation

### From VS Code Marketplace
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Runa Language Support"
4. Click Install

### Manual Installation
1. Download the `.vsix` file from releases
2. Open VS Code
3. Press `Ctrl+Shift+P` and run "Extensions: Install from VSIX..."
4. Select the downloaded file

## Quick Start

1. **Install the extension**
2. **Create a new file** with `.runa` extension
3. **Start coding!** The extension automatically activates

```runa
Note: Welcome to Runa programming!

Let message be "Hello, World!"
Display message

Process called "greet user" that takes name as String returns String:
    Return "Hello, " followed by name followed by "!"

Let greeting be Greet User with name as "Alice"
Display greeting
```

## Configuration

### Settings
Access settings via `File > Preferences > Settings` and search for "Runa":

#### Language Server
- **`runa.languageServer.enabled`** (default: `true`)
  - Enable/disable the language server for advanced features
- **`runa.languageServer.host`** (default: `"localhost"`)
  - Language server host address
- **`runa.languageServer.port`** (default: `8080`)
  - Language server port number

#### Formatting
- **`runa.formatting.enabled`** (default: `true`)
  - Enable automatic code formatting
- **`runa.formatting.convertSymbolsToWords`** (default: `true`)
  - Automatically convert mathematical symbols to natural language

#### Diagnostics
- **`runa.diagnostics.enabled`** (default: `true`)
  - Enable error diagnostics and warnings
- **`runa.diagnostics.mathSymbolEnforcement`** (default: `true`)
  - Warn when mathematical symbols are used outside mathematical contexts

#### Compiler
- **`runa.compiler.path`** (default: `"runa"`)
  - Path to the Runa compiler executable

#### Code Completion
- **`runa.completion.enabled`** (default: `true`)
  - Enable intelligent code completion
- **`runa.completion.includeBuiltins`** (default: `true`)
  - Include built-in functions in completion suggestions

### Example Configuration
```json
{
  "runa.compiler.path": "/usr/local/bin/runa",
  "runa.formatting.convertSymbolsToWords": true,
  "runa.diagnostics.mathSymbolEnforcement": true,
  "runa.completion.includeBuiltins": true
}
```

## Commands

The extension provides these commands (accessible via `Ctrl+Shift+P`):

| Command | Shortcut | Description |
|---------|----------|-------------|
| `Runa: Compile File` | `Ctrl+Shift+B` | Compile the current Runa file |
| `Runa: Run File` | `Ctrl+F5` | Run the current Runa file |
| `Runa: Format Document` | `Shift+Alt+F` | Format the current document |
| `Runa: Convert Mathematical Symbols to Words` | `Ctrl+Shift+C` | Convert math symbols to natural language |
| `Runa: Restart Language Server` | - | Restart the language server |
| `Runa: New Runa File` | - | Create a new Runa file with template |

## Runa Language Features

### Natural Language Syntax
Runa uses intuitive, natural language constructs:

```runa
Note: Variables and constants
Let user_name be "Alice"
Define PI as 3.14159
Set counter to counter plus 1

Note: Control structures
If temperature is greater than 25:
    Display "It's warm today!"
Otherwise:
    Display "It's cool today!"

For each book in library:
    Display "Title: " followed by book.title

Note: Functions
Process called "calculate area" that takes radius as Float returns Float:
    Return PI multiplied by radius multiplied by radius
```

### Mathematical Symbol Enforcement
Runa enforces natural language for better readability:

❌ **Avoid:**
```runa
Let result = a + b * c  # Mathematical symbols discouraged
```

✅ **Prefer:**
```runa
Let result be a plus b multiplied by c  # Natural language encouraged
```

### Built-in Functions
Extensive standard library with natural syntax:

```runa
Display "Hello, World!"
Let user_input be Input with prompt as "Enter your name: "
Let text_length be Length of user_input
Let uppercase_text be Uppercase of user_input
```

## Troubleshooting

### Common Issues

**Problem:** Extension not activating
**Solution:** Ensure the file has `.runa` extension and restart VS Code

**Problem:** Compiler not found
**Solution:** Check `runa.compiler.path` setting and ensure Runa is installed

**Problem:** Syntax highlighting not working
**Solution:** Reload VS Code window (`Ctrl+Shift+P` → "Developer: Reload Window")

**Problem:** Language server connection failed
**Solution:** Verify language server is running and check host/port settings

### Performance Tips
- Disable language server for very large files if needed
- Use workspace settings for project-specific configuration
- Clear extension cache if experiencing issues

## Development

### Building from Source
```bash
# Clone the repository
git clone https://github.com/sybertneticsaisolutions/runa.git
cd runa/ide-plugins/vscode

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Package extension
npm run package

# The .vsix file will be created in the current directory
```

### Contributing
We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- **Documentation:** [Runa Language Specification](../../docs/user/language-specification/)
- **Issues:** [GitHub Issues](https://github.com/sybertneticsaisolutions/runa/issues)
- **Discussions:** [GitHub Discussions](https://github.com/sybertneticsaisolutions/runa/discussions)
- **Email:** support@sybertnetics.com

## Changelog

### Version 2.0.3
- **Case-insensitive language support**: All Runa constructs work regardless of case
- **Enhanced syntax highlighting**: Mathematical symbols, type differentiation, compound structures
- **Custom Runa themes**: Dark and light themes optimized for Runa syntax
- **Improved LSP integration**: Context-aware hover and intelligent completions
- **Enhanced natural language operators**: Support for "joined with", "followed by", etc.

### Version 1.0.0
- Initial release
- Complete syntax highlighting for Runa language
- Intelligent code completion and IntelliSense
- Mathematical symbol enforcement
- Build and run integration
- Live templates and snippets
- Error detection and quick fixes
- Code formatting support

## License

MIT License - see [LICENSE](../../LICENSE) file for details.

---

**Made with ❤️ by Sybertnetics AI Solutions**
