# Runa IDE Plugins Installation Guide

This guide provides step-by-step instructions for installing and using the Runa IDE plugins for VS Code and IntelliJ IDEA.

## Prerequisites

### For Both IDEs
1. **Runa Compiler/Runtime**: Ensure you have the Runa compiler installed and accessible via PATH
   ```bash
   # Verify installation
   runa --version
   ```

### For VS Code Plugin
- **VS Code** version 1.70.0 or higher
- **Node.js** 18.x or higher (for building from source)
- **npm** or **yarn** package manager

### For IntelliJ Plugin  
- **IntelliJ IDEA** 2023.1 or higher (Community or Ultimate)
- Compatible with: WebStorm, PhpStorm, PyCharm, CLion, etc.
- **Java 11** or higher (for building from source)

---

## VS Code Plugin Installation

### Option 1: Install from Marketplace (Recommended)
*Coming soon - plugin will be published to VS Code Marketplace*

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for "Runa Language Support"
4. Click **Install**
5. Restart VS Code

### Option 2: Install Pre-built Package
If you have a `.vsix` package file:

1. Open VS Code
2. Press `Ctrl+Shift+P`
3. Type "Extensions: Install from VSIX..."
4. Select the `.vsix` file
5. Restart VS Code

### Option 3: Build and Install from Source

#### Step 1: Navigate to Plugin Directory
```bash
cd runa/ide-plugins/vscode
```

#### Step 2: Install Dependencies
```bash
npm install
```

#### Step 3: Compile TypeScript
```bash
npm run compile
```

#### Step 4: Package Extension
```bash
# Install vsce if not already installed
npm install -g vsce

# Package the extension
npm run package
```

#### Step 5: Install the Package
```bash
# This creates a .vsix file
code --install-extension runa-language-support-1.0.0.vsix
```

#### Alternative: Development Mode
For development/testing:
```bash
# Open in new VS Code window for testing
npm run watch &
code .
```
Press `F5` to launch a new Extension Development Host window.

---

## IntelliJ Plugin Installation

### Option 1: Install from JetBrains Plugin Repository (Recommended)
*Coming soon - plugin will be published to JetBrains Plugin Repository*

1. Open IntelliJ IDEA
2. Go to `File` → `Settings` → `Plugins`
3. Search for "Runa Language Support"
4. Click **Install**
5. Restart IntelliJ IDEA

### Option 2: Install Pre-built Plugin
If you have a plugin `.jar` or `.zip` file:

1. Open IntelliJ IDEA
2. Go to `File` → `Settings` → `Plugins`
3. Click `⚙️` → `Install Plugin from Disk...`
4. Select the plugin file
5. Restart IntelliJ IDEA

### Option 3: Build and Install from Source

#### Step 1: Navigate to Plugin Directory
```bash
cd runa/ide-plugins/intellij
```

#### Step 2: Build Plugin
```bash
# On Windows
.\gradlew buildPlugin

# On macOS/Linux  
./gradlew buildPlugin
```

#### Step 3: Locate Built Plugin
The plugin will be created in:
```
build/distributions/runa-intellij-plugin-1.0.0.zip
```

#### Step 4: Install in IntelliJ
1. Go to `File` → `Settings` → `Plugins`
2. Click `⚙️` → `Install Plugin from Disk...`
3. Select `runa-intellij-plugin-1.0.0.zip`
4. Restart IntelliJ IDEA

#### Alternative: Development Mode
For development/testing:
```bash
# Run plugin in development IDE
./gradlew runIde
```

---

## Verification & Configuration

### VS Code Setup

#### 1. Create Test File
1. Create a new file with `.runa` extension
2. Verify syntax highlighting activates
3. Test code completion with `Ctrl+Space`

#### 2. Configure Compiler Path
1. Open Settings (`Ctrl+,`)
2. Search for "runa"
3. Set `runa.compiler.path` to your Runa compiler location

#### 3. Test Commands
- **Compile**: `Ctrl+Shift+B`
- **Run**: `Ctrl+F5`  
- **Format**: `Shift+Alt+F`
- **Convert Symbols**: `Ctrl+Shift+C`

### IntelliJ Setup

#### 1. Create Test File
1. Right-click in project → `New` → `Runa File`
2. Enter filename and press Enter
3. Verify syntax highlighting and completion work

#### 2. Configure Plugin Settings
1. Go to `File` → `Settings` → `Languages & Frameworks` → `Runa`
2. Set compiler path and preferences
3. Configure code style if needed

#### 3. Test Actions
- **Compile**: `Ctrl+Shift+B`
- **Run**: `Ctrl+F5`
- **Format**: `Ctrl+Alt+L`
- **Convert Symbols**: `Ctrl+Shift+C`

---

## Sample Runa Program

Create a file called `hello.runa` to test the plugins:

```runa
Note: Hello World program in Runa
Note: Demonstrates basic syntax and natural language constructs

Display "Hello, World!"

Let greeting be "Welcome to Runa!"
Let user_name be "Developer"

Display greeting followed by " " followed by user_name

Process called "add numbers" that takes a as Integer and b as Integer returns Integer:
    Return a plus b

Let result be Add Numbers with a as 5 and b as 3
Display "5 + 3 = " followed by result

Note: Control structures
If result is greater than 7:
    Display "Result is greater than 7"
Otherwise:
    Display "Result is 7 or less"

Note: Collections  
Let fruits be list containing "apple", "banana", "orange"
For each fruit in fruits:
    Display "Fruit: " followed by fruit
```

---

## Troubleshooting

### Common Issues

#### VS Code Plugin Not Activating
**Problem**: Extension doesn't activate for `.runa` files
**Solutions**:
- Ensure file has `.runa` extension
- Restart VS Code
- Check Extensions view - ensure plugin is enabled
- Run "Developer: Reload Window" command

#### IntelliJ Plugin Not Loading
**Problem**: Plugin doesn't appear or load
**Solutions**:
- Verify IntelliJ IDEA version (2023.1+)
- Check plugin is enabled in Settings → Plugins
- Restart IntelliJ IDEA
- Check for conflicting plugins

#### Compiler Not Found
**Problem**: "runa command not found" errors
**Solutions**:
- Install Runa compiler/runtime
- Add Runa to system PATH
- Configure explicit path in plugin settings
- Verify with `runa --version` in terminal

#### Syntax Highlighting Issues
**Problem**: Code appears without highlighting
**Solutions**:
- Verify file association in IDE settings
- Clear IDE caches (IntelliJ: File → Invalidate Caches)
- Reinstall plugin
- Check for theme conflicts

#### Performance Issues
**Problem**: IDE becomes slow with large Runa files
**Solutions**:
- Increase IDE memory allocation
- Disable unused plugins
- Exclude large directories from indexing
- Use latest plugin version

### Getting Help

If you encounter issues:

1. **Check Documentation**: [Runa Language Specification](../docs/user/language-specification/)
2. **Search Issues**: [GitHub Issues](https://github.com/sybertneticsaisolutions/runa/issues)
3. **Ask Community**: [GitHub Discussions](https://github.com/sybertneticsaisolutions/runa/discussions)
4. **Contact Support**: support@sybertnetics.com

### Logs and Diagnostics

#### VS Code Logs
- Open Developer Tools: `Help` → `Toggle Developer Tools`
- Check Console tab for extension errors
- Enable extension logging in settings

#### IntelliJ Logs
- Show logs: `Help` → `Show Log in Files`
- Enable debug logging: `Help` → `Diagnostic Tools` → `Debug Log Settings`
- Add `com.sybertnetics.runa` for plugin-specific logs

---

## Uninstallation

### VS Code
1. Go to Extensions (`Ctrl+Shift+X`)
2. Find "Runa Language Support"
3. Click **Uninstall**
4. Restart VS Code

### IntelliJ IDEA  
1. Go to `File` → `Settings` → `Plugins`
2. Find "Runa Language Support"
3. Click **Uninstall**
4. Restart IntelliJ IDEA

---

## Next Steps

After successful installation:

1. **Explore Examples**: Check `runa/examples/` directory
2. **Read Documentation**: Study the language specification
3. **Join Community**: Participate in GitHub discussions
4. **Contribute**: Report bugs, suggest features, contribute code

**Happy coding with Runa! 🚀**
