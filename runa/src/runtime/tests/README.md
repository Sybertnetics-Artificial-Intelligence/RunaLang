# Runa Rust Toolchain Tests

## Directory Structure

- `basic/` — General and basic Runa language tests
- `malformed/` — Malformed or negative test cases
- (Add more subdirectories as needed for features, integration, etc.)

## Adding a Test
1. Place your `.runa` file in the appropriate subdirectory.
2. Use a descriptive filename (e.g., `test_feature_x.runa`).
3. Ensure your test is idiomatic and covers the intended feature or edge case.

## Running Tests
- Use the provided test harness (see below) to automatically discover and run all `.runa` files.
- The harness will recursively search for `.runa` files in all subdirectories.

## Example
```
tests/
  basic/
    test_basic.runa
    test_simple.runa
  malformed/
    test_malformed.runa
```

## Conventions
- All tests must be production-ready and idiomatic Runa.
- Document any non-obvious test logic in comments within the `.runa` file. 