## Runa CLI Toolkit

The Runa Command-Line Interface (CLI) is the unified entry point for interacting with the entire Runa developer toolchain. It's designed to be a consistent, intuitive, and powerful tool for managing the full lifecycle of a Runa project, from creation and local development to testing and translation.

-   **Source Location**: `runa/src/dev_tools/cli/main.runa`
-   **Command Handlers**: `runa/src/dev_tools/cli/commands/`
-   **Argument Parser**: `runa/src/dev_tools/cli/parser.runa`

### Design Philosophy

The CLI is built around a verb-based command structure (e.g., `runa build`, `runa test`, `runa doctor`) common in modern development toolchains. This provides a predictable and easy-to-remember interface.

A key design principle is the **transparent integration of the toolchain**. When you execute a command like `runa run`, you aren't just running your code; you are engaging a pipeline that may also be normalizing, compiling, and caching your project's source files. This happens automatically, ensuring that advanced features like multi-language support work out of the box without requiring manual steps from the developer.

---

### Core Commands

While a detailed reference for every command and its flags can be found in the **[Commands Reference](./commands.md)**, it's helpful to understand the primary workflow commands:

| Command | Purpose |
| :--- | :--- |
| `runa new <project_name>` | Creates a new Runa project with a standard directory structure, ready for development. |
| `runa build` | Compiles your project. This includes resolving dependencies, normalizing localized source code to a canonical form, and producing an executable or library. |
| `runa run` | Builds and immediately executes your project. Ideal for local development and testing. |
| `runa test` | Builds and runs all tests in your project, typically located in the `tests/` directory. |
| `runa doctor` | Analyzes your code for potential issues. This powerful tool acts as a linter and can suggest or even automatically apply fixes for common problems. |
| `runa translate` | Translates Runa source files between supported human languages, enabling developers to write and read code in their native language. |

### The Build Normalization Pipeline

One of the most important and unique features of the Runa CLI is the **Build Normalization Pipeline**. This is the process that makes Runa's multi-language capabilities possible.

When you execute `runa build`, `runa run`, or `runa test`, the following happens automatically:

1.  **Source Discovery**: The CLI finds all relevant `.runa` source files.
2.  **Language Detection**: It detects the language of each source file (e.g., Spanish, Japanese, or the default English/Canonical form).
3.  **Normalization**: Each file is passed through the **Localization Engine**, which translates its keywords, operators, and standard library calls into the single, canonical representation that the compiler understands.
4.  **Compilation**: The compiler is then invoked on this set of normalized, canonical source files.

This has a powerful implication: **the Runa compiler only ever needs to understand one language**. The complexity of supporting multiple human languages is handled entirely by the toolchain before compilation even begins. This keeps the compiler simpler and more maintainable while providing a seamless experience for the developer.

This pipeline ensures that a team of developers, each writing Runa in a different native language, can collaborate on the same project without any friction.