# Runa Testing Framework

A modular, self-contained testing framework for the Runa programming language.

## Overview

The Runa Testing Framework is designed to provide comprehensive testing capabilities without circular dependencies on the standard library. This is critical for testing the compiler and runtime themselves.

## Architecture

The framework follows a two-phase implementation strategy:

### Phase 1: Bootstrap Testing (Current)
- **Location**: `/runa/src/compiler/testing/minimal_test.runa`
- **Purpose**: Ultra-minimal assembly-based testing for compiler verification
- **Features**:
  - Direct inline assembly implementation
  - Zero dependencies on stdlib or runtime
  - Basic pass/fail semantics via exit codes
  - Simple integer and string comparisons

### Phase 2: Full Framework (Future)
- **Location**: `/runa/tests/framework/`
- **Purpose**: Complete testing framework using Runa language features
- **Status**: Currently implemented as skeleton files with NotImplemented placeholders

## Directory Structure

```
/runa/tests/framework/
├── core/
│   ├── assert.runa      # Assertion functions and validators
│   ├── runner.runa      # Test execution engine
│   └── reporter.runa    # Result reporting and formatting
├── matchers/            # (Future) Advanced matching patterns
├── mocks/              # (Future) Mocking and stubbing support
└── fixtures/           # (Future) Test data and fixtures
```

## Core Modules

### assert.runa
Provides fundamental assertion capabilities:
- Value equality assertions
- Boolean condition assertions
- Numeric comparisons
- String content assertions
- Collection assertions
- Exception handling assertions
- Custom assertion support

### runner.runa
Manages test discovery and execution:
- Test discovery from files and directories
- Sequential and parallel execution
- Test filtering and selection
- Setup/teardown hooks
- Retry mechanisms for flaky tests
- Performance profiling
- Memory leak detection

### reporter.runa
Handles result reporting and output:
- Multiple output formats (console, JSON, XML, HTML)
- Real-time streaming reporters
- Detailed failure diagnostics
- Performance metrics
- Code coverage integration
- CI/CD system compatibility

## Usage

### Phase 1: Minimal Testing

```runa
Import "compiler/testing/minimal_test" as MinimalTest

Process called "test_basic_assertion":
    Let result be MinimalTest.integers_equal(1 + 1, 2)
    MinimalTest.check_result(result)
End Process
```

### Phase 2: Full Framework (When Implemented)

```runa
Import "tests/framework/core/assert" as Assert
Import "tests/framework/core/runner" as Runner

Process called "test_example":
    Let result be Assert.assert_equals("hello", "hello", "Strings should match")
    Assert.assert_true(result.passed, "Assertion should pass")
End Process
```

## Implementation Status

| Component | Status | Description |
|-----------|--------|-------------|
| minimal_test.runa | ✅ Complete | Assembly-based bootstrap testing |
| assert.runa | 🔨 Skeleton | Assertion framework structure defined |
| runner.runa | 🔨 Skeleton | Test runner structure defined |
| reporter.runa | 🔨 Skeleton | Reporter structure defined |

## Design Principles

1. **No Circular Dependencies**: The framework must not depend on the standard library it's testing
2. **Self-Contained**: All necessary functionality implemented within the framework
3. **Modular Architecture**: Clear separation of concerns between modules
4. **Progressive Enhancement**: Start with minimal assembly, build up to full Runa
5. **CI/CD Compatible**: Output formats compatible with common CI systems

## Development Roadmap

1. **Current**: Bootstrap testing with inline assembly
2. **Next**: Implement Phase 2 skeleton functions
3. **Future**: Add advanced features:
   - Mocking and stubbing
   - Property-based testing
   - Benchmark support
   - Test generators
   - Visual test runners

## Contributing

When implementing skeleton functions:
1. Remove the `Throw Errors.NotImplemented` statement
2. Implement the complete algorithm as described
3. Ensure no dependencies on stdlib (unless explicitly allowed)
4. Add appropriate inline assembly where needed for low-level operations
5. Update this README to reflect implementation status

## Testing the Test Framework

The framework includes self-tests to verify its own correctness:
- Bootstrap tests use assembly exit codes
- Framework tests will test the assertion functions
- Meta-tests verify the test runner itself

## Platform Support

Currently targeting x86_64 Linux. Platform-specific assembly will need adjustment for:
- ARM architectures
- Windows systems
- macOS systems
- WebAssembly targets

## Known Limitations

- Phase 1 only supports basic integer and string operations
- No floating-point support in bootstrap phase
- Limited error reporting in assembly implementation
- Platform-specific assembly code

## License

Part of the Runa language project. See main repository LICENSE for details.