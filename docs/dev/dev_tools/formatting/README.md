# Runa Formatter

The Runa Formatter is a deterministic tool that automatically rewrites Runa source code to a canonical, consistent style. Its primary goal is to eliminate arguments over formatting and ensure that all Runa code across a project, and even across the ecosystem, looks and feels the same.

The formatter is designed to be **safe and behavior-preserving**. It only makes changes to whitespace, indentation, and operator syntax in ways that are guaranteed not to alter the runtime behavior of the code.

-   **Source Location**: `runa/src/dev_tools/formatting/formatter.runa`

### How to Use

The formatter is most commonly invoked via the `runa doctor --fix` command, which runs the formatter in addition to other static analysis checks and fixes.

```shell
# Format a single file
runa doctor --fix src/my_file.runa

# Format all files in the project
runa doctor --fix
```

### Core Responsibility: Canonicalization

The most important role of the formatter is **canonicalization**. Runa's syntax is designed to be flexible and readable, allowing for multiple ways to express the same operation (e.g., `is equal to` vs. `equals`). The formatter simplifies this by automatically converting these variations into a single, canonical form.

This provides two key benefits:
1.  **Reduces Cognitive Load**: Developers don't have to remember or choose between different valid syntaxes.
2.  **Simplifies Tooling**: Tools that analyze Runa code (like the linter or compiler) only need to handle the canonical form, making them simpler to build and more robust.

---

### Formatting Rules and Examples

Below are the primary canonicalization rules the formatter enforces.

#### 1. String Concatenation

The canonical operator for string concatenation is `joined with`. The formatter will automatically rewrite any use of `+`, `plus`, or legacy operators (`concatenated with`, `followed by`) when used with string literals or variables inferred to be strings.

**Before:**
```runa
Let name be "World"
Let greeting be "Hello" + " " + name
Let old_greeting be "Hello" followed by " World"
```

**After:**
```runa
Let name be "World"
Let greeting be "Hello" joined with " " joined with name
Let old_greeting be "Hello" joined with " World"
```
*Note: This rule is also enforced by a semantic check in the compiler. Using `+` or `plus` with strings will produce a compiler error, which `runa doctor --fix` can then correct.*

#### 2. Equality Operator

The canonical operator for equality comparison is `equals`. The multi-word version, `is equal to`, is supported by the parser but will be rewritten by the formatter.

**Before:**
```runa
If user_role is equal to "admin":
    Console.print("Access granted")
```

**After:**
```runa
If user_role equals "admin":
    Console.print("Access granted")
```

#### 3. Mathematical Operators (Future)

*Note: While Runa supports both symbolic (`+`, `-`) and natural language (`plus`, `minus`) mathematical operators, the formatter does not yet enforce a canonical style for them. This may be added in a future release with configuration options to allow teams to choose their preferred style.*

### Configuration

The formatter is designed to be non-configurable for most rules to ensure maximum consistency. Future versions may introduce limited configuration options for aspects like operator style.