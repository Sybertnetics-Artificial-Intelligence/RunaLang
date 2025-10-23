# Frequently Asked Questions

Common questions about Runa programming language.

## General Questions

### What is Runa?

Runa is a revolutionary programming language that bridges human thinking and machine execution. It features natural language syntax that reads like English while maintaining the precision needed for complex software systems.

### Why should I use Runa?

Runa offers several unique advantages:

- **Readable by anyone** - If you can read English, you can understand Runa code
- **AI-first design** - Built specifically for AI-assisted development
- **Universal translation** - Translate between 50+ programming languages
- **Production ready** - Strong typing, memory safety, and performance
- **Multiple syntax modes** - Choose between natural language (Canon) or symbolic operators (Developer)

### Is Runa open source?

Runa is licensed under the **Runa Proprietary Limited License (RPLL)**. While the source code is publicly available and you can contribute, there are restrictions on commercial use and distribution. See [LICENSE.md](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/blob/main/LICENSE.md) for details.

### Who created Runa?

Runa is created and maintained by **Sybertnetics Artificial Intelligence Solutions**.

### How mature is Runa?

Runa is currently in **Open Source Preview** status. The compiler is bootstrapped and self-hosting, but we're working toward the first public release (v0.1.0). Core features are stable, but the ecosystem is still evolving.

## Getting Started

### How do I install Runa?

See the [Installation Guide](Installation-Guide) for platform-specific instructions. The first official release (v0.1.0) will include simplified installation.

### What platforms does Runa support?

Runa supports:
- Linux (x86_64, ARM64, ARM32)
- macOS (x86_64, Apple Silicon)
- Windows (x86_64, ARM64)
- BSD variants (FreeBSD, NetBSD, OpenBSD)
- Experimental: RISC-V, MIPS, PowerPC

See [Supported Platforms](Supported-Platforms) for complete details.

### Do I need to know programming to use Runa?

Not necessarily! Runa's natural language syntax makes it accessible to beginners. However, understanding basic programming concepts (variables, loops, functions) will help. See [Quick Start Tutorial](Quick-Start-Tutorial) to begin.

### Where should I start learning Runa?

1. Read the [Quick Start Tutorial](Quick-Start-Tutorial)
2. Try the examples in [Your First Runa Program](Your-First-Runa-Program)
3. Explore the [Standard Library Overview](Standard-Library-Overview)
4. Join our [Discord community](https://discord.gg/sybertnetics-runa)

## Language Features

### What are syntax modes?

Runa supports multiple syntax modes:

- **Canon Mode** - Natural language operators (`multiplied by`, `is greater than`)
- **Developer Mode** - Symbolic operators (`*`, `>`)
- **Viewer Mode** (planned) - Full natural language for documentation

Both Canon and Developer modes produce identical compiled code. See [Syntax Modes](Syntax-Modes).

### Is Runa statically typed or dynamically typed?

Runa is **statically typed** with **type inference**. You can explicitly declare types or let the compiler infer them:

```runa
Let x be 10          # Type inferred as integer
Let y as Float be 3.14   # Explicitly typed as Float
```

### Does Runa support object-oriented programming?

Yes! Runa supports:
- Types (structs/classes)
- Methods
- Interfaces (protocols)
- Inheritance (planned)
- Polymorphism

See [Type System](Type-System) for details.

### Does Runa support functional programming?

Yes! Runa includes:
- First-class functions
- Lambda expressions
- Higher-order functions (map, filter, reduce)
- Pattern matching
- Immutability options

### How does Runa handle memory management?

Runa uses a **hybrid memory management** system:
- Automatic Reference Counting (ARC) for deterministic cleanup
- Garbage collection for cyclic references
- Manual memory management available for performance-critical code

See [Memory Management](Memory-Management).

### Is Runa's natural language syntax slow?

No! The natural language syntax is purely a parsing concern. Runa compiles to efficient native code with performance comparable to C/C++. The compiler can even output assembly or machine code directly.

## Syntax and Identifiers

### Are identifiers case-sensitive?

**Yes**, but with nuance:

- Spaces and underscores are equivalent: `user name` ≡ `user_name`
- Case matters per-word: `User Name` ≠ `user name`
- Examples:
  - `Calculate Area` ≡ `Calculate_Area` (same)
  - `Calculate area` ≡ `Calculate_area` (same)
  - `Calculate Area` ≠ `Calculate area` (different - "Area" vs "area")

See [Code Style Guide](Code-Style-Guide).

### Can I use camelCase or PascalCase?

Yes, but it's **discouraged**. Runa's idiomatic style uses spaced identifiers:

```runa
# Recommended (canonical)
Let user name be "Alice"

# Works but discouraged (non-canonical)
Let userName be "Alice"
Let UserName be "Alice"
```

The auto-formatter will convert underscores to spaces but won't change camelCase/PascalCase.

### Can I mix Canon and Developer mode?

**No**, don't mix operators from different modes in the same expression:

```runa
# WRONG - mixed modes
Let result be x * y plus z

# CORRECT - Canon mode
Let result be x multiplied by y plus z

# CORRECT - Developer mode
Let result be x * y + z
```

However, you can use different modes in different files within the same project.

## Interoperability

### Can I call C/C++ libraries from Runa?

Yes! Runa has a **Foreign Function Interface (FFI)** for C/C++ interop:

```runa
Import "libc.so.6" as libc

External Process called "printf" from libc that takes format as CString
```

See [FFI Documentation](FFI).

### Can I use existing Python/JavaScript/etc. libraries?

Not directly, but you can:
1. Use FFI to call C bindings of those libraries
2. Use code translation to convert libraries to Runa
3. Wait for language-specific interop layers (planned)

### Can I convert my Python code to Runa?

Partially! Runa includes code translation tools:

```bash
runac --translate-from python mycode.py -o mycode.runa
```

The translator handles most common patterns but may require manual adjustments for complex code. See [Code Translation](Code-Translation).

### Can Runa compile to JavaScript/WebAssembly?

**WebAssembly** support is planned for a future release.

**JavaScript** transpilation is possible using the translation tools, though not all Runa features map cleanly to JS.

## Performance

### How fast is Runa compared to Python/Java/C++?

Performance comparisons (approximate):
- **vs Python**: 10-50x faster (compiled vs interpreted)
- **vs Java**: Comparable (both compile to native/bytecode)
- **vs C++**: Comparable (both compile to native code)

Actual performance depends on the specific workload and optimizations.

### Does Runa have a JIT compiler?

Not currently. Runa uses **ahead-of-time (AOT) compilation** to native code. JIT compilation may be added in the future for certain use cases.

### Can I optimize performance-critical code?

Yes! Options include:
- Use explicit types instead of inference
- Manual memory management for critical sections
- Inline assembly for platform-specific optimizations
- Profile-guided optimization (planned)

See [Performance Optimization](Performance-Optimization) (coming soon).

## Development Tools

### What IDEs support Runa?

Official IDE support is in development. Currently:
- **VS Code**: Basic syntax highlighting (in progress)
- **Vim/Neovim**: Syntax highlighting (community-maintained)
- Any text editor works for writing Runa code

See [IDE Setup](IDE-Setup).

### Is there a debugger?

A debugger is planned for v0.1.0. For now, you can:
- Use `Display` statements for debugging
- Use platform debuggers (gdb, lldb) on compiled binaries
- Enable compiler debug output

### Is there a package manager?

A package manager is planned for a future release. Currently, you can:
- Use the module system for local dependencies
- Manually manage external dependencies

### Does Runa have a REPL?

Not yet, but it's on the roadmap for v0.2.0.

## Contributing

### How can I contribute to Runa?

We welcome contributions! See the [Contributing Guide](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/blob/main/CONTRIBUTING.md).

**Areas where we need help:**
- Standard library development
- Compiler optimizations
- Translation tools
- Documentation and tutorials
- Testing on different platforms

### Can I contribute to the core compiler?

The core compiler (lexer, parser, codegen) is **currently maintained internally**. However, we welcome:
- Bug reports and feedback
- Optimization suggestions
- Platform-specific improvements

We may open the core compiler to contributions in the future.

### Do I need to sign a CLA?

By contributing, you agree to the terms in the [Contributing Guide](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/blob/main/CONTRIBUTING.md), which includes granting Sybertnetics AI a license to use your contribution. This is standard for open source projects.

## Troubleshooting

### I get "command not found: runac"

The Runa compiler is not in your PATH. Either:
- Add the Runa `bin` directory to your PATH
- Use the full path to `runac`
- Reinstall Runa following the [Installation Guide](Installation-Guide)

### My program compiles but crashes at runtime

Common causes:
- Null pointer dereference
- Array index out of bounds
- Stack overflow (deep recursion)

Enable debug mode for more information:
```bash
runac myfile.runa --debug -o myfile
./myfile
```

### I get type errors that don't make sense

Runa's type system is strict. Common issues:
- Mixing integer and float types
- Forgetting to convert types
- Using the wrong collection type

Use explicit type annotations to help the compiler:
```runa
Let x as Integer be some value
```

### How do I report a bug?

1. Check if it's a known issue in [GitHub Issues](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/issues)
2. If not, create a new issue with:
   - Minimal reproducible example
   - Expected vs actual behavior
   - Your platform and Runa version
   - Compiler output/error messages

See [Troubleshooting](Troubleshooting) for more help.

## Community

### Where can I ask questions?

- **Quick questions**: [Discord community](https://discord.gg/sybertnetics-runa)
- **Discussions**: [GitHub Discussions](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/issues)

### Is there a Runa community?

Yes! Join us:
- [Discord](https://discord.gg/sybertnetics-runa) - Real-time chat
- [GitHub Discussions](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/discussions) - Q&A and ideas
- [Official Blog](https://sybertnetics.com/blog/runa) - News and tutorials

### How can I stay updated on Runa development?

- Follow the [Official Blog](https://sybertnetics.com/blog/runa)
- Watch the [GitHub repository](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang)
- Join the [Discord community](https://discord.gg/sybertnetics-runa)
- Check [Release Notes](Release-Notes)

## Future Plans

### When will v1.0 be released?

We're working toward v1.0, but no date is set. The roadmap:
- **v0.1.0**: First public release (coming soon)
- **v0.2.0**: REPL, package manager, improved tooling
- **v0.5.0**: Stable standard library, mature ecosystem
- **v1.0.0**: Production-ready with stability guarantees

### What features are planned?

Upcoming features include:
- Package manager and dependency resolution
- REPL (interactive shell)
- WebAssembly compilation target
- Improved IDE support
- Enhanced debugging tools
- More language interop options

See the [Roadmap](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/blob/main/docs/dev/Sybertnetics_Roadmap/) for details.

### Will Runa always be free?

The compiler and core tools will remain **free and open source** under the RPLL. Commercial support, additional tools, and enterprise features may be offered separately.

## Still Have Questions?

- Check the [Troubleshooting](Troubleshooting) page
- Search [GitHub Discussions](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/discussions)
- Ask in [Discord](https://discord.gg/sybertnetics-runa)
- Create a [GitHub Discussion](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/discussions/new)

---

**This FAQ is maintained by the community. Feel free to suggest improvements!**
