# Runa Rust Toolchain

## Test Organization

All Runa language test files are now located in the `tests/` directory, organized by category:

```
rust/
  src/           # Rust source code for the compiler/interpreter
  tests/
    basic/       # Basic and general Runa test cases
      test_basic.runa
      test_simple.runa
      ...
    malformed/   # Malformed or negative test cases
      test_malformed.runa
    ...          # Add more categories as needed
```

- **How to add a test:**
  1. Place new `.runa` files in the appropriate subdirectory under `tests/`.
  2. Use descriptive names and group by feature or test type.
  3. Update or create test harnesses to discover and run all `.runa` files in these directories.

- **Why this structure?**
  - Keeps implementation and tests separate for clarity and maintainability.
  - Scales well as the test suite grows.
  - Makes it easy to automate test discovery and execution.

For more details, see the main documentation or contact the maintainers. 