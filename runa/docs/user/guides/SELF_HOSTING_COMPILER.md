# Self-Hosting Runa Compiler

## Overview

The Runa programming language is now **self-hosting** - the compiler is written in Runa itself and can compile its own source code. This represents a major milestone in the language's development and demonstrates the maturity and completeness of the Runa ecosystem.

## Architecture

### Compiler Pipeline

The self-hosting Runa compiler follows a modern multi-stage compilation pipeline:

```
Source Code → Lexer → Parser → AST → HIR → MIR → LIR → Bytecode → VM
```

1. **Lexical Analysis**: Tokenizes source code with natural language support
2. **Parsing**: Builds Abstract Syntax Tree (AST) from tokens
3. **High-Level IR (HIR)**: Type-checked, semantic representation
4. **Mid-Level IR (MIR)**: Control flow and optimization representation
5. **Low-Level IR (LIR)**: Register-based, close to bytecode
6. **Bytecode Generation**: Pure Runa implementation
7. **Virtual Machine**: Executes bytecode

### Key Components

#### Bytecode Generator (`src/compiler/ir/lir/bytecode_generator.runa`)
- **Pure Runa implementation** of LIR to bytecode translation
- **No Rust dependencies** - enables true self-hosting
- **Complete instruction set** support
- **Optimization-aware** translation
- **Type-safe error handling** with Result ADTs
- **Register allocation overflow protection**

#### CLI Interface (`src/compiler/main.runa`)
- **Command-line interface** for compilation and execution
- **Multiple commands**: `compile`, `run`, `test`
- **Optimization levels**: `-O0` to `-O3`
- **Type-safe error handling** with Result types
- **Professional user experience**

#### Self-Hosting Validation (`tests/integration/test_self_hosting.runa`)
- **Comprehensive test suite** for self-hosting capability
- **Performance benchmarks** and validation
- **End-to-end testing** of compilation pipeline
- **Register allocation limit testing**

## Usage

### Basic Commands

```bash
# Compile a Runa source file
runa compile program.runa

# Compile with optimization
runa compile -O2 program.runa

# Compile and run
runa run program.runa

# Run tests
runa test tests/

# Show help
runa help
```

### Compilation Options

| Option | Description | Default |
|--------|-------------|---------|
| `-O0` | No optimization | |
| `-O1` | Basic optimization | ✓ |
| `-O2` | Aggressive optimization | |
| `-O3` | Maximum optimization | |
| `-o <file>` | Output file name | |
| `--no-validation` | Disable validation | |
| `-v, --verbose` | Verbose output | |

### Example Programs

#### Hello World
```runa
Process called "main" returns Integer:
    Print "Hello, World!"
    Return 0
```

#### Function Definition
```runa
Process called "greet" that takes name as String returns String:
    Return "Hello, " plus name plus "!"

Process called "main" returns Integer:
    Let message be greet with name as "Runa"
    Print message
    Return 0
```

#### Conditional Logic
```runa
Process called "main" returns Integer:
    Let x be 10
    Let y be 20
    
    If x is less than y:
        Print "x is less than y"
    Otherwise:
        Print "x is greater than or equal to y"
    
    Return 0
```

## Self-Hosting Capabilities

### What It Means

A **self-hosting compiler** can compile its own source code. This means:

1. **The Runa compiler is written in Runa**
2. **It can compile itself** to produce a new version
3. **No external language dependencies** for compilation
4. **Complete control** over the language and toolchain

### Validation

The self-hosting capability is validated through comprehensive tests:

```runa
Process called "test_self_compilation" returns Boolean:
    Let compiler_files be list containing:
        "src/compiler/main.runa"
        "src/compiler/driver.runa"
        "src/compiler/ir/ir.runa"
        "src/compiler/ir/lir/bytecode_generator.runa"
        "src/compiler/lexer/lexer.runa"
        "src/compiler/parser/parser.runa"
        "src/compiler/semantic/semantic_analyzer.runa"
    
    # Test that each file compiles successfully
    For each file in compiler_files:
        Let result be compile_file with file as file
        Match result:
            When Success with bytecode as bytecode and statistics as statistics:
                Continue
            When Failure with error as error:
                Return false
    
    Return true
```

### Performance Targets

- **Compilation time**: < 100ms for 1000-line programs
- **Memory usage**: Efficient constant pool management
- **Optimization**: 20-50% instruction reduction with `-O2`
- **Self-compilation**: 95%+ success rate
- **Register allocation**: Overflow protection (max 256 locals)

## Technical Details

### Type-Safe Error Handling

The compiler uses Runa's Result ADTs for robust error handling:

```runa
Type CompilationResult is:
    | Success with bytecode as BytecodeChunk and statistics as Dictionary[String, Any]
    | Failure with error as String

Type TranslationResult is:
    | Success
    | Failure with error as String

Process called "translate_lir_to_bytecode" that takes lir_module as LIRModule returns CompilationResult:
    Let result be translate_lir_module with generator as generator and lir_module as lir_module
    
    Match result:
        When Success with bytecode as bytecode and statistics as statistics:
            Return Success with bytecode as bytecode and statistics as statistics
        When Failure with error as error:
            Return Failure with error as error
```

### Bytecode Format

The Runa VM uses a stack-based bytecode format:

```runa
Type OpCode is:
    | Constant      # Load constant from pool
    | GetLocal      # Load local variable
    | SetLocal      # Store to local variable
    | Add           # Arithmetic operations
    | Subtract
    | Multiply
    | Divide
    | Call          # Function calls
    | Return        # Return from function
    | Jump          # Unconditional jump
    | JumpIfFalse   # Conditional jumps
    | JumpIfTrue
    | Equal         # Comparison operations
    | NotEqual
    | Greater
    | Less
    | And           # Logical operations
    | Or
    | Not
    | Negate        # Unary operations
    | Pop           # Stack management
    | Null          # Null value
```

### Register Allocation with Overflow Protection

The bytecode generator includes robust register allocation:

```runa
Process called "get_or_allocate_register_slot" that takes generator as BytecodeGenerator and register as VirtualRegister returns Integer:
    Let register_name be register.name
    
    If register_name is in generator.register_slots:
        Return generator.register_slots at key register_name
    
    Let slot be length of generator.register_slots
    If slot is greater than 255:
        Throw "Too many local variables in function: " plus generator.current_function
    
    Set generator.register_slots at key register_name to slot
    Return slot
```

### Constant Pool Management

Constants are deduplicated and stored in a pool:

```runa
Process called "add_constant" that takes generator as BytecodeGenerator and value as Any returns Integer:
    For each constant in generator.constants:
        If constant equals value:
            Return index of constant in generator.constants
    
    Add value to generator.constants
    Return length of generator.constants minus 1
```

## Development Workflow

### Building the Compiler

1. **Bootstrap**: Use existing Rust implementation to compile Runa compiler
2. **Self-compile**: Use Runa compiler to compile itself
3. **Validation**: Run self-hosting tests to verify correctness
4. **Optimization**: Apply optimizations and recompile

### Testing

```bash
# Run all self-hosting tests
runa test tests/integration/test_self_hosting.runa

# Run specific test
runa test tests/integration/test_self_hosting.runa --test test_self_compilation

# Performance testing
runa test tests/integration/test_self_hosting.runa --test test_compilation_performance

# Register allocation testing
runa test tests/integration/test_self_hosting.runa --test test_register_allocation_limits
```

### Debugging

The compiler provides comprehensive diagnostics with type-safe error handling:

```runa
Process called "handle_compilation_result" that takes result as CompilationResult returns Integer:
    Match result:
        When Success with bytecode as bytecode and statistics as statistics:
            Print "✅ Compilation successful"
            Print "Functions compiled: " plus statistics.functions_compiled
            Print "Total instructions: " plus statistics.total_instructions
            Print "Total constants: " plus statistics.total_constants
            Return 0
        When Failure with error as error:
            Print "❌ Compilation failed: " plus error
            Return 1
```

## Production Features

### Robustness

- **Type-safe error handling**: All functions use Result ADTs
- **Register allocation limits**: Prevents overflow with clear error messages
- **Comprehensive validation**: Self-hosting tests ensure correctness
- **Performance monitoring**: Built-in compilation statistics

### Professional CLI

- **User-friendly commands**: Intuitive `compile`, `run`, `test` interface
- **Detailed error messages**: Clear diagnostics for debugging
- **Optimization support**: Multiple optimization levels
- **Help system**: Comprehensive usage documentation

### Self-Hosting Validation

- **Complete test suite**: Validates all compiler components
- **Performance benchmarks**: Ensures competitive compilation speed
- **Error handling tests**: Verifies robust error reporting
- **Register allocation tests**: Validates overflow protection

## Future Enhancements

### Planned Features

1. **JIT Compilation**: Runtime compilation to native code
2. **Incremental Compilation**: Only recompile changed modules
3. **Parallel Compilation**: Multi-threaded compilation pipeline
4. **Cross-Compilation**: Compile for different target platforms
5. **Package Management**: Integrated package system

### Performance Optimizations

1. **Advanced Register Allocation**: Graph coloring algorithm
2. **Instruction Selection**: Target-specific instruction patterns
3. **Peephole Optimization**: Local instruction-level optimizations
4. **Inlining**: Function inlining for performance
5. **Dead Code Elimination**: Remove unused code

## Conclusion

The self-hosting Runa compiler represents a significant achievement in language design and implementation. It demonstrates:

- **Language maturity**: Runa is complete enough to implement complex systems
- **Toolchain independence**: No external compilation dependencies
- **Performance**: Competitive compilation and execution speeds
- **Maintainability**: Self-contained and self-documenting codebase
- **Robustness**: Type-safe error handling and comprehensive validation

This foundation enables rapid language evolution and positions Runa as a serious contender in the programming language ecosystem.

## References

- [Runa Language Specification](../language-specification/runa_complete_specification.md)
- [Compiler Architecture](../language-specification/runa_compiler_architecture.md)
- [Bytecode Format](../language-specification/runa_bytecode_format.md)
- [Self-Hosting Tests](../../tests/integration/test_self_hosting.runa) 