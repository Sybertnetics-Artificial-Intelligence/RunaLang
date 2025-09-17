# Runa Language Support for IntelliJ IDEA

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://plugins.jetbrains.com/plugin/runa-language-support)
[![JetBrains Plugin](https://img.shields.io/badge/JetBrains-Plugin-orange.svg)](https://plugins.jetbrains.com/plugin/runa-language-support)

Comprehensive language support for Runa - the AI-first natural programming language designed for AI-to-AI communication.

Compatible with IntelliJ IDEA, WebStorm, PhpStorm, PyCharm, and other JetBrains IDEs.

## Features

### 🎨 **Advanced Syntax Highlighting**
- Rich color schemes for Runa's natural language constructs
- Semantic highlighting with proper scoping
- Mathematical symbol enforcement visualization
- Customizable color settings

### 🧠 **Intelligent Code Completion**
- Context-aware IntelliSense with type information
- Natural language operator suggestions
- Built-in function completion with parameter hints
- Smart completion for Runa patterns

### 🔍 **Advanced Code Analysis**
- Real-time mathematical symbol enforcement
- Comprehensive syntax error detection
- Quick fixes and intention actions
- Code inspections specific to Runa

### 📋 **Live Templates**
- Extensive collection of code templates
- Context-aware template suggestions
- Customizable template variables
- Rapid code generation

### 🏗️ **Project Integration**
- Native build system integration
- Run configurations for Runa programs
- Debugging support preparation
- Project structure recognition

### 🔧 **Refactoring & Navigation**
- Smart refactoring operations
- Go to definition/declaration
- Find usages across project
- Structure view with semantic grouping

## Installation

### From JetBrains Plugin Repository
1. Open IntelliJ IDEA
2. Go to `File` → `Settings` → `Plugins`
3. Search for "Runa Language Support"
4. Click `Install` and restart IDE

### Manual Installation
1. Download the plugin `.jar` file from releases
2. Go to `File` → `Settings` → `Plugins`
3. Click `⚙️` → `Install Plugin from Disk...`
4. Select the downloaded file
5. Restart IntelliJ IDEA

## Quick Start

### Creating a New Runa File
1. **Right-click** in project explorer
2. **New** → **Runa File**
3. Enter filename and **press Enter**
4. Start coding with full IDE support!

### Basic Runa Program
```runa
Note: My first Runa program
Note: Demonstrates basic syntax and natural language constructs

Display "Welcome to Runa!"

Let user_name be "Alice"
Let user_age be 25

Display "User: " followed by user_name
Display "Age: " followed by user_age

Process called "greet user" that takes name as String and age as Integer returns String:
    Let greeting be "Hello, " followed by name
    Let age_text be "You are " followed by age followed by " years old"
    Return greeting followed by "! " followed by age_text

Let message be Greet User with name as user_name and age as user_age
Display message
```

## Configuration

### Plugin Settings
Access via `File` → `Settings` → `Languages & Frameworks` → `Runa`:

#### Compiler Settings
- **Compiler Path**: Path to Runa compiler executable
- **Compiler Options**: Additional command-line options
- **Output Directory**: Where compiled files are placed

#### Code Analysis
- **Mathematical Symbol Enforcement**: Enable/disable symbol warnings
- **Strict Mode**: Enable stricter syntax checking
- **Natural Language Validation**: Validate natural language constructs

#### Formatting
- **Auto-format on Save**: Automatically format Runa files
- **Indent Size**: Number of spaces for indentation (default: 4)
- **Symbol Conversion**: Auto-convert symbols to words

### Code Style
Customize code style via `File` → `Settings` → `Editor` → `Code Style` → `Runa`:

- **Indentation**: Spaces vs tabs, indent size
- **Spacing**: Around operators, before colons
- **Wrapping**: Line wrapping rules for long statements
- **Comments**: Comment formatting preferences

## Live Templates

Type these abbreviations and press `Tab`:

### Basic Constructs
| Abbreviation | Expands to |
|--------------|------------|
| `let` | `Let variable be value` |
| `define` | `Define constant as value` |
| `set` | `Set variable to new_value` |
| `display` | `Display message` |

### Control Structures
| Abbreviation | Expands to |
|--------------|------------|
| `if` | `If condition:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`body` |
| `ifelse` | `If condition:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`if_body`<br>`Otherwise:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`else_body` |
| `for` | `For each item in collection:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`body` |
| `while` | `While condition:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`body` |

### Functions
| Abbreviation | Expands to |
|--------------|------------|
| `process` | `Process called "name" that takes param as Type returns Type:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`Return result` |

### Error Handling
| Abbreviation | Expands to |
|--------------|------------|
| `try` | `Try:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`try_body`<br>`Catch exception:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`catch_body`<br>`Finally:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`finally_body` |

### Collections
| Abbreviation | Expands to |
|--------------|------------|
| `list` | `list containing item1, item2` |
| `dict` | `dictionary with:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`key1 as value1`<br>&nbsp;&nbsp;&nbsp;&nbsp;`key2 as value2` |

### Comments
| Abbreviation | Expands to |
|--------------|------------|
| `note` | `Note: comment` |
| `noteblock` | `Note:`<br>`comment_block`<br>`:End Note` |

## Actions & Shortcuts

### File Actions
| Action | Shortcut | Description |
|--------|----------|-------------|
| Compile Runa File | `Ctrl+Shift+B` | Compile current file |
| Run Runa File | `Ctrl+F5` | Run current file |
| Format Code | `Ctrl+Alt+L` | Format current file |
| Convert Symbols to Words | `Ctrl+Shift+C` | Convert math symbols |

### Navigation
| Action | Shortcut | Description |
|--------|----------|-------------|
| Go to Declaration | `Ctrl+B` | Navigate to definition |
| Find Usages | `Alt+F7` | Find all usages |
| Structure View | `Alt+7` | Show file structure |
| Quick Definition | `Ctrl+Shift+I` | Show definition popup |

### Code Generation
| Action | Shortcut | Description |
|--------|----------|-------------|
| Generate Code | `Alt+Insert` | Generate code templates |
| Complete Current Statement | `Ctrl+Shift+Enter` | Auto-complete statement |
| Expand Live Template | `Tab` | Expand template abbreviation |

## Debugging & Running

### Run Configurations
The plugin automatically creates run configurations for Runa files:

1. **Right-click** on a `.runa` file
2. **Run 'filename.runa'**
3. Configure run parameters if needed
4. Use debug mode for step-by-step execution (coming soon)

### Console Output
- Integrated console for program output
- Error highlighting with clickable stack traces
- Compiler output with syntax error locations

## Project Structure

### Recommended Project Layout
```
my-runa-project/
├── src/
│   ├── main.runa
│   ├── utils/
│   │   ├── helpers.runa
│   │   └── constants.runa
│   └── modules/
│       ├── math.runa
│       └── strings.runa
├── tests/
│   ├── test_main.runa
│   └── test_utils.runa
├── docs/
│   └── README.md
└── runa.toml
```

### Module Recognition
The plugin recognizes:
- Runa source files (`.runa`)
- Project configuration (`runa.toml`)
- Module imports and exports
- Package structure

## Advanced Features

### Code Inspections
The plugin includes specialized inspections for:
- Mathematical symbol enforcement
- Natural language syntax validation
- Unused variable detection
- Type checking (when available)
- Import optimization

### Refactoring
Available refactoring operations:
- Rename variables, functions, and modules
- Extract method/function
- Move declarations
- Convert symbols to natural language

### Version Control Integration
- Syntax highlighting in diff views
- Merge conflict resolution
- Change tracking for Runa files

## Troubleshooting

### Common Issues

**Plugin not loading**
- Verify IntelliJ IDEA version compatibility (2023.1+)
- Check plugin is enabled in Settings → Plugins
- Restart IDE after installation

**Syntax highlighting not working**
- Ensure file has `.runa` extension
- Check language association in Settings → Editor → File Types
- Invalidate caches: File → Invalidate Caches and Restart

**Compiler not found**
- Set correct compiler path in Settings → Languages & Frameworks → Runa
- Ensure Runa compiler is installed and accessible
- Check PATH environment variable

**Performance issues**
- Increase IDE memory allocation (Help → Change Memory Settings)
- Disable unused plugins
- Exclude large directories from indexing

### Logging & Diagnostics
Enable debug logging:
1. Go to `Help` → `Diagnostic Tools` → `Debug Log Settings`
2. Add `com.sybertnetics.runa` to logging categories
3. Reproduce issue and check `idea.log`

## Development

### Building the Plugin
```bash
# Clone repository
git clone https://github.com/sybertneticsaisolutions/runa.git
cd runa/ide-plugins/intellij

# Build plugin
./gradlew buildPlugin

# Run in development IDE
./gradlew runIde

# Package for distribution
./gradlew buildPlugin
# Output: build/distributions/runa-intellij-plugin-1.0.0.zip
```

### Testing
```bash
# Run tests
./gradlew test

# Run integration tests
./gradlew integrationTest
```

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and add tests
4. Commit changes: `git commit -m 'Add amazing feature'`
5. Push to branch: `git push origin feature/amazing-feature`
6. Submit pull request

## API & Extension Points

The plugin provides extension points for:
- Custom syntax highlighting schemes
- Additional live templates
- Code inspections
- Refactoring operations
- Build tool integrations

See the [API documentation](docs/api.md) for details.

## Support

- **Documentation**: [Runa Language Specification](../../docs/user/language-specification/)
- **Issues**: [GitHub Issues](https://github.com/sybertneticsaisolutions/runa/issues)
- **Plugin Support**: [JetBrains Plugin Page](https://plugins.jetbrains.com/plugin/runa-language-support)
- **Community**: [GitHub Discussions](https://github.com/sybertneticsaisolutions/runa/discussions)
- **Email**: support@sybertnetics.com

## Changelog

### Version 1.0.0 (2025-01-XX)
- ✨ Initial release
- 🎨 Complete syntax highlighting with semantic analysis
- 🧠 Intelligent code completion and parameter hints
- 📋 Comprehensive live template library
- 🔍 Mathematical symbol enforcement with quick fixes
- 🏗️ Build system integration and run configurations
- 🔧 Advanced refactoring and navigation features
- 📚 Structure view and project recognition
- ⚙️ Extensive configuration options

## License

This plugin is licensed under the same terms as the Runa project. See [LICENSE](../../LICENSE) for details.

---

**Developed with ❤️ by Sybertnetics AI Solutions**  
**For the future of AI-first programming**
