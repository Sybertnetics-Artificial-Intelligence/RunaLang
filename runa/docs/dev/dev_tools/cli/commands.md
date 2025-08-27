# Runa CLI Commands Reference

This document provides a detailed reference for the primary commands available in the Runa CLI.

---

### `runa new`

Creates a new Runa project with a standard, best-practices directory structure.

**Usage**

```shell
runa new <project_name>
```

**Example**

```shell
runa new my_awesome_app
```

This will create a new directory named `my_awesome_app` with the following structure:

```
my_awesome_app/
├── runa.toml      # Project manifest and configuration
├── src/           # Source code directory
│   └── main.runa  # Main entry point of your application
└── tests/         # Tests directory
    └── main_test.runa
```

---

### `runa build`

Compiles the Runa project in the current directory.

This command triggers the full **Build Normalization Pipeline**, which includes dependency resolution, source code normalization (language translation), and finally, compilation into an executable or library. The output is placed in the `target/` directory.

**Usage**

```shell
runa build [FLAGS]
```

**Flags**

-   `--release`: Compiles the project with optimizations for production use. This will result in a faster but larger binary and a longer compilation time.

**Example**

```shell
# Build for development
runa build

# Build for production
runa build --release
```

---

### `runa run`

Builds and immediately runs the project's main executable.

This is the most common command used during development. It is a convenient shorthand for `runa build` followed by executing the resulting binary.

**Usage**

```shell
runa run [FLAGS] -- [APPLICATION_ARGS]
```

**Flags**

-   `--release`: Builds and runs the project in release mode.
-   `--no-build`: Skips the build step and runs the last compiled executable. This is useful for quickly re-running your application if no code has changed.

Any arguments placed after a `--` separator are passed directly to your application.

**Example**

```shell
# Build and run in debug mode
runa run

# Run and pass arguments to the application
runa run -- --port=8080 --verbose

# Run the release version without rebuilding
runa run --release --no-build
```

---

### `runa test`

Compiles and runs all tests in the project.

The test runner will automatically discover any files in the `tests/` directory (and its subdirectories) that it identifies as test files. It compiles them and executes the test suite, reporting the results to the console.

**Usage**

```shell
runa test
```

---

### `runa doctor`

Analyzes your codebase for potential errors, style violations, and semantic issues.

`runa doctor` is a powerful static analysis tool that acts as Runa's "linter." It can detect a wide range of problems, from simple style inconsistencies to more complex issues like the misuse of operators.

**Usage**

```shell
runa doctor [FLAGS] [PATH]
```

If no `PATH` is provided, it analyzes the entire project.

**Flags**

-   `--fix`: Automatically applies safe fixes for any issues it finds. This is a powerful way to quickly clean up a codebase. For example, it can automatically rewrite incorrect string concatenations from `+` to `joined with`.
-   `--explain`: Provides more detailed explanations for the issues it finds, which can be helpful for learning Runa idioms.

**Example**

```shell
# Check the entire project for issues
runa doctor

# Automatically fix issues in a specific file
runa doctor --fix src/my_module.runa
```

---

### `runa translate`

Translates a Runa source file from one human language to another.

This command uses the **Localization Engine** to perform a token-based translation of Runa's keywords and operators. It is the core tool that enables developers to write Runa in their native language.

**Usage**

```shell
runa translate [FLAGS] <input_file>
```

**Flags**

-   `--from <lang>`: The source language of the input file (e.g., `en`, `ja`, `es`).
-   `--to <lang>`: The target language for the output (e.g., `hi`, `ru`, `zh`).
-   `--detect`: Attempts to automatically detect the source language of the input file.
-   `--in-place`: Modifies the input file directly with the translation, instead of creating a new file.
-   `--output <file>`: Specifies the path for the output file. If not provided, the output is named `filename.<lang>.runa` by default.

**Supported Languages**: `en` (English/Canonical), `hi` (Hindi), `ja` (Japanese), `es` (Spanish), `zh` (Mandarin Chinese), `ru` (Russian).

**Example**

```shell
# Translate a Japanese file to Spanish, creating main.es.runa
runa translate --from ja --to es src/main.ja.runa

# Translate a file, detecting its source language, and update it in-place
runa translate --detect --to en --in-place src/utils.runa

# Translate a file to Russian, specifying the output path
runa translate --from en --to ru src/main.runa translated/main_ru.runa
```