# v0.1 Parser Tests

This directory contains comprehensive tests for the v0.1 Runa parser, written in Runa-Zero and compiled with the v0.0 bootstrap compiler.

## Test Files

### Core Tests (Working)

- `test_simple_parser.runa` - Basic function with return statement
- `test_parser_functions.runa` - Function definitions with various parameter counts and nested calls
- `test_parser_control_flow_fixed.runa` - If/else statements and while loops (without for loops)

### Tests Requiring v0.0 Parser Updates

These tests use features not yet supported by v0.0:

- `test_parser_control_flow.runa` - Uses for loops (not supported in v0.0)
- `test_parser_expressions.runa` - Complex expressions
- `test_parser_variables.runa` - Variable scoping and assignments
- `test_parser_returns.runa` - Return statements in various contexts
- `test_parser_edge_cases.runa` - Edge cases and stress tests

## Running Tests

To compile and run a test:

```bash
# Compile to assembly
../v0.0/target/release/runac tests/test_name.runa -o /tmp/test_name.s --emit-asm-only

# Assemble with NASM
nasm -f elf64 /tmp/test_name.s -o /tmp/test_name.o

# Link with C runtime
ld /tmp/test_name.o -o /tmp/test_name -lc -dynamic-linker /lib64/ld-linux-x86-64.so.2

# Run test
/tmp/test_name
echo "Exit code: $?"
```

## Test Results

As of current state:
- ✅ `test_simple_parser.runa` - Returns 42 as expected
- ✅ `test_parser_functions.runa` - All function tests pass
- ✅ `test_parser_control_flow_fixed.runa` - Control flow tests pass (without for loops)
- ❌ Other tests require v0.0 parser enhancements (for loops, complex expressions)

## Notes

The v0.0 parser has limitations:
- No support for `for` loops
- No support for compound boolean expressions (`&&`, `||`)
- No support for `else if` (must use nested `else { if }`)
- No support for `break` statements

These limitations are by design - v0.0 is a minimal bootstrap compiler. The v0.1 parser being tested here will support these features when self-hosted.