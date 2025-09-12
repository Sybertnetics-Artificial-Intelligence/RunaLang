# Runa Compiler Frontend Primitives Test Suite

## Overview

This directory contains the comprehensive test suite for the Runa compiler frontend primitive operations. The test suite validates all fundamental operations including string manipulation, integer operations, memory management, assembly operations, and logical/bitwise operators.

## Test Suite Architecture

The test suite is organized into modular components that test specific primitive categories:

### Core Test Files

- **`run_all_primitive_tests.runa`** - Master test orchestrator and entry point
- **`test_string_primitive.runa`** - String manipulation and memory safety tests
- **`test_integer_primitive.runa`** - Integer operations and process management tests
- **`test_void_primitive.runa`** - Void operations and debugging primitive tests
- **`test_memory_primitives.runa`** - Memory layout and reference analysis tests
- **`test_assembly_primitives.runa`** - Assembly operations and syscall tests
- **`test_operator_primitives.runa`** - Logical and bitwise operator tests

## Test Categories

### 1. String Primitive Tests (`test_string_primitive.runa`)

**Coverage:**
- String length calculation with various encodings
- String comparison with lexicographic ordering
- String copying with memory safety validation
- String concatenation with buffer management
- Substring extraction and search operations
- Memory safety and boundary checking

**Key Test Functions:**
- `test_calculate_string_length()` - Length calculation accuracy
- `test_compare_strings()` - Comparison operations and edge cases
- `test_copy_string()` - Safe copying with boundary validation
- `test_concatenate_strings()` - String joining operations
- `test_extract_substring()` - Substring operations with bounds checking
- `test_find_substring()` - Pattern matching and search algorithms

### 2. Integer Primitive Tests (`test_integer_primitive.runa`)

**Coverage:**
- Process management (fork, exec, wait)
- Child process tracking and handle management
- Command line argument handling
- Memory allocation and deallocation
- Error handling and boundary conditions

**Key Test Functions:**
- `test_fork_process()` - Process forking and parent/child differentiation
- `test_exec_process()` - Program execution with arguments
- `test_wait_for_process()` - Process synchronization and status retrieval
- `test_add_child_handle()` - Child process tracking
- `test_allocate_memory()` - Memory management operations

### 3. Void Primitive Tests (`test_void_primitive.runa`)

**Coverage:**
- Debug breakpoint functionality
- Unreachable code detection and handling
- Branch prediction hints and optimization
- Compiler optimization primitives
- Error handling and safety mechanisms

**Key Test Functions:**
- `test_debug_breakpoint()` - Debugger integration and trap generation
- `test_assume_unreachable()` - Unreachable code termination
- `test_likely_void()` - Branch prediction hint validation
- `test_compiler_optimization_hints()` - Optimization guidance testing

### 4. Memory Primitive Tests (`test_memory_primitives.runa`)

**Coverage:**
- Memory layout calculation and alignment
- Reference analysis and compile-time optimization
- Memory operation safety and boundary checking
- Cross-platform layout compatibility
- Type-specific layout and reference handling

**Key Test Functions:**
- `test_calculate_struct_layout()` - Struct field alignment and padding
- `test_can_calculate_layout_at_compile_time()` - Compile-time analysis
- `test_validate_layout_compatibility()` - Cross-platform validation
- `test_can_analyze_references_at_compile_time()` - Reference analysis
- `test_memory_boundary_checking()` - Buffer overflow/underflow detection

### 5. Assembly Primitive Tests (`test_assembly_primitives.runa`)

**Coverage:**
- Syscall number mapping and execution
- Inline assembly syntax validation
- Instruction parsing and address resolution
- Machine code emission and encoding
- Platform-specific instruction handling

**Key Test Functions:**
- `test_get_syscall_number()` - System call mapping validation
- `test_make_syscall()` - Syscall execution and parameter passing
- `test_validate_assembly_syntax()` - Assembly code validation
- `test_parse_instruction()` - Instruction parsing accuracy
- `test_emit_instruction()` - Machine code generation

### 6. Operator Primitive Tests (`test_operator_primitives.runa`)

**Coverage:**
- Logical operations (AND, OR, NOT, XOR)
- Bitwise operations (shift, rotate, mask)
- Comparison operations and equality testing
- Short-circuit evaluation validation
- Type conversion and promotion

**Key Test Functions:**
- `test_logical_and_operations()` - AND operations and short-circuiting
- `test_bitwise_shift_operations()` - Shift operations and overflow handling
- `test_equality_operations()` - Equality comparison accuracy
- `test_and_short_circuit()` - Short-circuit evaluation validation

## Running the Tests

### Execute All Tests

```bash
# Run the complete test suite
./run_all_primitive_tests.runa
```

### Execute Individual Test Suites

```runa
# Run specific test categories
run_all_string_primitive_tests()
run_all_integer_primitive_tests()
run_all_void_primitive_tests()
run_all_memory_primitive_tests()
run_all_assembly_primitive_tests()
run_all_operator_primitive_tests()
```

### Test Output Format

The test suite provides structured output with clear pass/fail indicators:

```
=== CORE PRIMITIVE TESTS ===
[PASS] String primitive tests PASSED
[PASS] Integer primitive tests PASSED
[PASS] Void primitive tests PASSED

=== MEMORY PRIMITIVE TESTS ===
[PASS] Memory primitive tests PASSED

=== ASSEMBLY PRIMITIVE TESTS ===
[PASS] Assembly primitive tests PASSED

=== OPERATOR PRIMITIVE TESTS ===
[PASS] Operator primitive tests PASSED

=== COMPREHENSIVE TEST EXECUTION REPORT ===
Test Execution Summary:
  Total Test Suites: 7
  Passed Suites: 7
  Failed Suites: 0
  Success Rate: 100%
  Execution Duration: 2 seconds

[PASS] ALL TESTS PASSED - Primitive operations are functioning correctly
```

## Test Design Principles

### 1. Comprehensive Coverage
- Every primitive function is tested with multiple scenarios
- Edge cases and boundary conditions are explicitly validated
- Error conditions are tested to ensure proper handling

### 2. Memory Safety Validation
- All memory operations are tested for bounds checking
- Buffer overflow and underflow scenarios are validated
- Proper cleanup and resource management is verified

### 3. Cross-Platform Compatibility
- Tests validate behavior across different target platforms
- Platform-specific optimizations are tested independently
- Endianness and word-size differences are accounted for

### 4. Integration Testing
- Cross-primitive interactions are validated
- Type system integration is tested
- Memory layout compatibility across modules is verified

### 5. Performance Validation
- Critical performance paths are tested for optimization
- Compiler hints and optimization primitives are validated
- Resource usage patterns are verified

## Test Environment Requirements

### System Requirements
- Runa compiler with primitive module support
- Memory allocation capabilities (heap and stack)
- System call access for process management tests
- Debug symbol support for debugging primitive tests

### Platform Support
- **x86_64 Linux** - Primary testing platform
- **AArch64** - Cross-compilation testing
- **Embedded platforms** - Resource-constrained testing

### Memory Requirements
- Minimum 64MB available heap space for memory tests
- Stack space for nested function calls during testing
- Temporary storage for string and buffer operations

## Debugging Failed Tests

### 1. Individual Test Failure
When a specific test fails, examine the test function output and:
- Check system prerequisites (permissions, memory, etc.)
- Validate input data and expected outcomes
- Review platform-specific behavior differences
- Examine memory allocation and cleanup patterns

### 2. Systematic Failures
For widespread test failures:
- Verify test environment setup and prerequisites
- Check system resource availability (memory, file descriptors)
- Validate compiler primitive implementations
- Review recent changes to primitive modules

### 3. Platform-Specific Issues
For platform-related failures:
- Check alignment requirements and endianness handling
- Validate syscall availability and numbering
- Review platform-specific instruction encodings
- Examine memory layout and address space differences

## Contributing to the Test Suite

### Adding New Tests
1. Identify primitive functions requiring additional coverage
2. Create test functions following the established naming patterns
3. Include comprehensive edge case and error condition testing
4. Add integration tests for cross-module interactions
5. Update the master test runner to include new tests

### Test Function Guidelines
- Use descriptive function names prefixed with `test_`
- Include comprehensive `@Implementation` annotations
- Test both success and failure scenarios
- Validate all return values and side effects
- Clean up any allocated resources

### Documentation Standards
- Document test purpose and coverage in function headers
- Explain complex test scenarios and expected outcomes
- Include examples of proper and improper usage
- Reference related primitive functions and dependencies

## Integration with Build Systems

### Continuous Integration
The test suite is designed for integration with CI/CD pipelines:
- Returns appropriate exit codes (0 for success, 1 for failure)
- Provides structured output suitable for parsing
- Includes timing information for performance monitoring
- Generates detailed failure reports for debugging

### Build System Integration
```makefile
# Example Makefile integration
test-primitives:
	cd tests/compiler/frontend/primitives && ./run_all_primitive_tests.runa

.PHONY: test-primitives
```

### Automated Testing
The test suite supports automated execution with:
- Batch execution of all test categories
- Individual test suite execution for targeted testing
- Comprehensive reporting for test result analysis
- Performance metrics collection for regression detection

## Performance Benchmarks

The test suite includes performance validation for critical operations:

- **String Operations:** Sub-millisecond performance for typical string sizes
- **Memory Operations:** Microsecond-level allocation and deallocation
- **Assembly Operations:** Near-native performance for instruction parsing
- **Operator Operations:** Inline optimization verification

## Security Considerations

### Memory Safety
- All tests validate proper bounds checking
- Buffer overflow scenarios are explicitly tested
- Memory leak detection is integrated into test cleanup

### Process Security
- Process spawning tests use controlled environments
- Syscall tests validate proper permission handling
- Debug operations are tested in safe isolation

### Input Validation
- All primitive functions are tested with invalid inputs
- Edge cases that could cause security issues are validated
- Error handling prevents information disclosure

---

This comprehensive test suite ensures the reliability, performance, and security of the Runa compiler's primitive operations, providing confidence in the foundational components that support higher-level compiler functionality.