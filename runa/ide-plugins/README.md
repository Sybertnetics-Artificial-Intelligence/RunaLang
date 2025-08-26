# Runa IDE Plugins

Comprehensive IDE support for the Runa programming language - the AI-first natural programming language designed for AI-to-AI communication.

## Overview

This directory contains IDE plugins for two major development environments:

- **VS Code**: Full-featured extension for Visual Studio Code
- **IntelliJ IDEA**: Comprehensive plugin for IntelliJ IDEA and other JetBrains IDEs

Both plugins provide complete language support for Runa's unique natural language syntax, mathematical symbol enforcement, and AI-focused development features.

## Features

### 🎨 **Syntax Highlighting**
- Complete support for Runa's natural language constructs
- Proper highlighting for comments using "Note:" syntax
- Distinction between keywords, operators, and identifiers
- Special highlighting for mathematical symbol violations

### 🔧 **Intelligent Code Completion**
- Context-aware completion for keywords and operators
- Natural language operator suggestions ("plus", "minus", "multiplied by", etc.)
- Built-in function completion with documentation
- Type annotations and pattern completions

### ⚠️ **Error Detection & Quick Fixes**
- Real-time mathematical symbol enforcement warnings
- Syntax error detection with helpful suggestions
- Quick fixes to convert symbols to natural language
- Proper indentation and formatting validation

### 📝 **Code Templates & Snippets**
- Live templates for common Runa patterns
- Variable declaration: `Let variable be value`
- Function definition: `Process called "name" that takes...`
- Control structures: `If condition:`, `For each item in collection:`
- Error handling: `Try:` / `Catch:` / `Finally:`

### 🔨 **Build Integration**
- Compile and run Runa files directly from IDE
- Configurable compiler path settings
- Integrated output console with error reporting
- Build status indicators

### 📋 **Additional Features**
- Code formatting with proper indentation
- Comment/uncomment actions using Runa syntax
- Brace matching and code folding
- File templates for new Runa files
- Structure view and navigation support

## Quick Start

### VS Code Plugin
```bash
# Navigate to VS Code plugin directory
cd runa/ide-plugins/vscode

# Install dependencies
npm install

# Compile the extension
npm run compile

# Package the extension (optional)
npm run package
```

### IntelliJ Plugin
```bash
# Navigate to IntelliJ plugin directory
cd runa/ide-plugins/intellij

# Build the plugin
./gradlew buildPlugin

# The plugin will be available in build/distributions/
```

## Language Support

Both plugins provide full support for Runa's natural language syntax:

### Variables & Constants
```runa
Let greeting be "Hello, World!"
Define MAX_SIZE as 100
Set counter to counter plus 1
```

### Functions
```runa
Process called "calculate sum" that takes a as Integer and b as Integer returns Integer:
    Return a plus b
```

### Control Flow
```runa
If temperature is greater than 30:
    Display "It's hot!"
Otherwise:
    Display "It's comfortable"

For each item in shopping_list:
    Display "Buy: " followed by item
```

### Collections
```runa
Let numbers be list containing 1, 2, 3, 4, 5
Let person be dictionary with:
    name as "Alice"
    age as 30
```

### Comments
```runa
Note: This is a single-line comment

Note:
This is a multi-line comment block
that can span several lines
:End Note
```

## Mathematical Symbol Enforcement

One of Runa's unique features is mathematical symbol enforcement. The plugins will warn when mathematical symbols are used outside of mathematical contexts:

❌ **Incorrect:**
```runa
Let name be "John" + "Doe"  # Warning: + only for math
```

✅ **Correct:**
```runa
Let name be "John" followed by "Doe"
Let sum be 5 plus 3
```

## Configuration

Both plugins offer extensive configuration options:

### VS Code Settings
- `runa.languageServer.enabled`: Enable/disable language server
- `runa.formatting.convertSymbolsToWords`: Auto-convert math symbols
- `runa.diagnostics.mathSymbolEnforcement`: Enable symbol warnings
- `runa.compiler.path`: Path to Runa compiler

### IntelliJ Settings
- Compiler path configuration
- Code style settings
- Color scheme customization
- Template configuration

## Installation

### VS Code
1. Install from VS Code Marketplace (coming soon)
2. Or install manually by copying to extensions folder
3. Restart VS Code and open a `.runa` file

### IntelliJ IDEA
1. Install from JetBrains Plugin Repository (coming soon)
2. Or install manually via Settings → Plugins → Install from disk
3. Restart IntelliJ and create/open a `.runa` file

## Development

### Contributing
We welcome contributions to improve the IDE plugins! Please see the main project's contributing guidelines.

### Building from Source
Both plugins can be built from source using their respective build systems (npm for VS Code, Gradle for IntelliJ).

### Testing
The plugins include comprehensive test suites covering syntax highlighting, completion, and error detection features.

## Support

For issues, feature requests, or questions:
- GitHub Issues: [Project Repository](https://github.com/sybertneticsaisolutions/runa)
- Documentation: [Runa Language Docs](../docs/user/)
- Email: support@sybertnetics.com

## License

Both plugins are licensed under the same license as the Runa project. See the main project LICENSE file for details.

---

**Happy coding with Runa! 🚀**
